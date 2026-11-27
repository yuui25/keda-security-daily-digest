# KEDA Daily Digest — 2026-11-28 (JST)

> 採用範囲: 公開日 2026-11-26 〜 2026-11-28
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

米国の感謝祭の連休で、OpenAI と Anthropic の公式発表や arXiv の新着は止まった。AI 側の話題は、Sakana AI の 30B 推論モデル「Namazu Small」、NVIDIA の自己回帰型の画像生成モデル、Tencent の投機的デコーディング「DFly2」など、重みや OSS の公開が中心だった。GitLab 19.6 は、SAST の検出が実際に悪用できるかを確かめるエージェントのフローを入れた。
セキュリティ側の最大の話題は、Cacti 1.2.31 の修正版がないゼロデイ「4HTTP2SHELL」。ゲストが有効なら HTTP リクエスト 4 回で RCE に至り、PoC も公開済み。Linux の nfsd にも、2014 年からあった認証なしで root を取れるヒープオーバーフロー「NFS2ROOT」(CVE-2026-99362) が公開された。SAP は GitHub の開発環境に侵入されたことを認め、署名の鍵を入れ替えた。1Password、Todoist に続き「開発者のトークンから GitHub に入る」侵害が今週 3 件目になる。
国内では GMOペパボが「ロリポップ！」など 4 サービスで 51 万件超の漏えいの可能性を公表した。平文で保存していた Basic 認証のパスワード約 10.5 万件も含まれる。ZOZO も、開発環境の脆弱性からクラウドの認証情報を取られ、本番の DB まで侵入されたと公表した。
**今日まず見るべき 2 件**: (1) 担当環境の Cacti でゲストアカウントが有効になっていないかの確認。(2) 2049/tcp を公開している Linux の NFS サーバーのカーネルの版の確認。

## 今日の深掘り

### Cacti の修正版がないゼロデイ「4HTTP2SHELL」: ゲストのセッションから HTTP リクエスト 4 回で RCE、PoC も公開済み

- **概要**: 研究者 ek0ms savi0r (Church of Malware) が 11/26 (感謝祭の日)、Cacti Core 1.2.31 (現在の最新版) の RCE の解説、PoC、動画を GitHub でフルディスクロージャーとして公開した。名前は当初「4HTTP2ROOT」で、後に「4HTTP2SHELL」に変わった。CVE は未採番で、修正版もない。watchTowr の FAQ によると、11/27 の時点で実際の攻撃は報告されていない。BleepingComputer と The Hacker News も 11/27 に報じた。
- **技術的な中身** (BleepingComputer、THN、watchTowr の解説をまとめたもの):
  1. ゲストのまま `auth_profile.php?tab=general` を開き、セッションの cookie と `csrfMagicToken` を得る。
  2. `auth_profile.php?action=update_data` で、ユーザー設定 `preview_graphs_per_page` に `1;UPDATE poller_item SET ... arg1=0x<コマンドの hex> ...;--` を保存する。保存にはプリペアドステートメントを使うが、値が整数かどうかは確かめていない。
  3. `graph_view.php?action=preview` を開くと、DB から読み出した設定値が `get_allowed_graphs()` の `LIMIT` 句に文字列のまま連結される。PDO が積み重ねたクエリ (stacked query) を実行し、`poller_item.arg1` が書き換わる。リクエストの値に対する整数のフィルターは、DB から読んだ値には効かない。典型的な **2 次の SQL インジェクション**。
  4. 同じセッションで `graph_realtime.php` を呼ぶと、書き換えた行の値が PHP の `popen()` にそのまま渡り、Web / ポーラーの実行ユーザーの権限でコマンドが動く。root になるかは構成による。
  - 前提はゲストアカウントが有効であること (0.8.7 以降、既定では無効)。成立が確認されたのは 1.2.31 だけで、それより前の版で成立するかは公表されていない。
- **背景・経緯** (過去の事例。今回の記事の内容ではない): Cacti は何度も悪用されてきた。CVE-2022-46169 (remote_agent.php の認証回避とコマンドインジェクション) は CISA KEV に登録され、ボットネットにも使われた。CVE-2023-39361 は、同じ `graph_view.php` にあったゲストでも届く SQLi。CVE-2024-25641 はパッケージの import からの RCE。「ゲストで届く graph_view.php」と「poller からのコマンド実行」は、過去にも攻撃の経路になってきた場所。研究者は、ベンダーのトリアージに何年も報告を退けられたことへの抗議としてフルディスクロージャーを選んだと書いており、修正の時期は見えていない。
- **なぜ今これが重要か** (評価): 修正版がなく PoC が公開済みで、しかも連休中という「悪用までの時間が最も短い」条件がそろっている。Cacti は社内の監視サーバーとして SNMP のコミュニティ名や機器の資格情報を持つことが多い。攻撃者にとっては、社内のネットワーク機器へ横に広げる入口としての価値が高い。診断の面では、2 次の SQLi (保存時は安全でも、読み出し後に連結される) と、DB の値が `popen()` に渡る sink の組み合わせが、他の PHP 製の監視ツール (LibreNMS、Observium、Zabbix の Web UI など) でも同じ形で起こりうる。
- **読者が今日できること**:
  - 外部と社内の Cacti を洗い出す。例: Shodan / Censys で `http.title:"Login to Cacti"`。管理画面の「Settings → Authentication」で、ゲストのユーザー (Guest User) が「No User」以外になっていないか確かめる。
  - ゲストを無効にできない場合は、UI へのアクセスを信頼できるネットワークに限る。痕跡は、ログの「非数値の graph の設定」に関する警告、`poller_item.arg1` の想定外の値、ポーラーが作った見慣れないファイル。
  - ソースコード診断の観点では、`read_user_setting()` / `read_config_option()` の戻り値を SQL に連結している箇所を grep する。たとえば `LIMIT .*\$` や `ORDER BY .*\$`。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/unpatched-cacti-zero-day-with-public-poc-gives-remote-code-execution/) / [The Hacker News](https://thehackernews.com/2026/11/unpatched-cacti-zero-day-enables-rce-in.html) / [watchTowr FAQ](https://watchtowr.com/intelligence/4http2root-cacti-zero-day-faq/)

## AI 技術・トレンド

### [2026-11-26] 国内: Sakana AI、Nemotron 3 Nano を土台にした 30B の推論モデル「Sakana Namazu Small」を公開
- **何が起きたか**: Sakana AI が、30B-A3B (アクティブ 3B) の「Namazu Small」を公開した。Nemotron 3 Nano の事前学習済みベースに、継続事前学習と事後学習を自社で加えたもの。同社によると、25 ベンチマークの平均は 60.1 で、Nemotron 3 Super (120B) の 56.2 を上回る。BrowseComp は 73.5 と高いが、SimpleQA Verified は 6.8 と低い。上位モデルの Namazu は Kimi K2.6 がベース。
- **なぜ重要か**: Web 調査向けのエージェントを手元の GPU で動かせる規模。国内でオンプレミスの LLM の導入が進めば、それも診断の対象に加わる。
- 出典: [MarkTechPost](https://www.marktechpost.com/2026/11/26/sakana-ai-namazu-small-30b-nemotron-3-nano/)

### [2026-11-27] 国内: DeNA、相づちを取りこぼさないよう追加学習した日本語の音声認識モデル 3 種を無償公開
- **何が起きたか**: DeNA が Hugging Face で 3 つのモデルを公開した。元のモデルは NVIDIA の Nemotron 3.5 ASR Streaming 0.6B、Parakeet-ja、Haas-ja-v1.0。「うん」「ええ」などの短い相づちを書き起こせるようにし、背景の雑音を言葉と誤る現象も抑えた。ライセンスは OpenMDW 1.1 / CC BY 4.0 / Apache 2.0 で、いずれも商用利用できる。
- **なぜ重要か**: 日本語の音声エージェントの入力の部分に組み込まれやすい。音声からのプロンプトインジェクションを検証するときの対象になる。
- 出典: [PC Watch](https://pc.watch.impress.co.jp/docs/news/2159894.html)

### [2026-11-27] NVIDIA、自己回帰型の画像生成モデル「Nemotron-Labs-Image-30B-A3B」の重みを公開
- **何が起きたか**: NVIDIA が、拡散モデルではなく LLM と同じ自己回帰方式の画像生成モデルを公開した。生成システム「Nemotron-Labs-VisualCreation」の一部。NVIDIA は、このシステムが複数のベンチマークで GPT-Image-2 と Nano Banana Pro を上回ると主張している。ライセンスは非商用に限られ、技術レポートは arXiv 2611.31358。
- **なぜ重要か**: 画像と HTML / SVG を同じモデルで生成する方向に進んでおり、エージェントの出力からのインジェクションという新しい攻撃面を生む。
- 出典: [GIGAZINE](https://gigazine.net/news/20261127-nemotron-labs-image-30b-a3b/)

### [2026-11-27] Tencent、スパースな LLM 向けの投機的デコーディングのドラフター「DFly2」を OSS で公開
- **何が起きたか**: Tencent が、0.85B・5 層のドラフター DFly2 を公開した。自分の KV キャッシュを持たず、本体の疎な KV キャッシュとインデックスを使い回す。DeepSeek-V4.1-Flash (SWE、64K の文脈) では、1 ユーザーあたりの速度をそろえた条件でスループットが最大 81% 上がった。試験は H20 と vLLM (TP8) で行った。
- **なぜ重要か**: 長い文脈の推論のコストが下がるほど、コード全体を読ませる診断の補助や、常に動き続けるエージェントが安く使えるようになる。
- 出典: [MarkTechPost](https://www.marktechpost.com/2026/11/26/tencent-dfly2-speculative-decoding-sparse-models/)

### [2026-11-27] GitLab 19.6、エージェントによる脆弱性の修正を拡大。SAST の検出が実際に悪用できるかを確かめるフロー (β) を追加
- **何が起きたか**: GitLab 19.6 では、エージェントのフローを複数のプロジェクトで一括して有効にでき、既定以外のブランチでも動かせるようになった。「脆弱性コンテキストフロー」(β) は SAST の検出が悪用できるかを確かめる。漏れた PAT を失効させて作り直し、コードから消す「ローテーションと修正」(β) も入った。定期実行の自動化は、権限を絞った専用のサービスアカウントで動く。
- **なぜ重要か**: SAST の誤検知を選り分ける作業がエージェントに任されていく。一方で、CI の資格情報を持って自動で動くサービスアカウントは、新しい攻撃面として診断の対象になる。
- 出典: [クラウド Watch](https://cloud.watch.impress.co.jp/docs/news/2159484.html)

### [2026-11-26] Z.ai と Moonshot、次の旗艦モデルが遅れる見込み。Moonshot は Google と Meta のモデルを蒸留の元にする (Reuters 報道)
- **何が起きたか**: 報道によると、Z.ai の約 3 兆パラメータの GLM-5.5 は 11 月の予定から 2027 年 1〜3 月に、Moonshot の Kimi K4 は 2027 年半ばにずれ込む見込み。理由として、米国による Nvidia のチップの「クラウド経由の抜け道」の封鎖、東南アジア向けの出荷の停止、OpenAI と Anthropic による蒸留目的のアクセスの遮断が挙げられている。
- **なぜ重要か**: 蒸留への対策と輸出規制が、中国のモデル開発の進み方を実際に変えている。オープンな重みのモデルの勢力図にも影響する。
- 出典: [The Decoder](https://the-decoder.com/after-openai-and-anthropic-shut-the-door-on-their-data-a-chinese-ai-developer-is-turning-to-google-and-meta-instead/)

### [2026-11-27] 輸出が禁じられた Nvidia の GB300-NVL72 が上海のデータセンターで見つかる (Bloomberg 報道)
- **何が起きたか**: Bloomberg によると、中国の規制当局への届け出で、Shanghai Shuoyao が GB300-NVL72 のラックを 9,600 万元 (約 1,400 万ドル) の融資の担保にしていた。Bloomberg は保証の公開データベースのシリアル番号から、製造元を Gigabyte と特定した。関係する Megaspeed (シンガポール) は、今月米国の取引禁止リストに加えられている。
- **なぜ重要か**: 高性能な GPU の迂回輸出が、公開された記録から裏付けられた。輸出管理の執行がさらに強まることが予想される。
- 出典: [The Decoder](https://the-decoder.com/banned-nvidia-blackwell-chips-turn-up-in-a-shanghai-data-center-linked-to-alice-huang-bloomberg-reports/)

### [2026-11-27] OpenAI、営業秘密の窃取などで Apple を逆提訴 (FT 報道)
- **何が起きたか**: 報道によると、OpenAI は 11/27 にカリフォルニア州の裁判所で Apple を提訴した。両社と取引する部品メーカーへの圧力と、退職した社員を通じて製品計画が漏れたことを主張している。夏に Apple が起こした訴訟への反撃にあたる。
- **なぜ重要か**: AI デバイスをめぐる競争で、内部の人間からの情報漏洩が法廷で争われている。
- 出典: [The Decoder](https://the-decoder.com/openai-countersues-apple-over-trade-secret-theft-and-alleged-coercion-of-shared-suppliers/)

### [2026-11-27] OpenAI、エージェント向けのデータ基盤「Athena」を開発中 (The Information 報道)
- **何が起きたか**: 報道によると、OpenAI は売上や顧客数などの業務の指標を一貫して定義する「セマンティックレイヤー」にあたる Athena を作っている。ChatGPT Work のデータ分析エージェントの精度が足りないという顧客の声を受けたもの。業務のルールを集めて記録するエージェントも開発中で、時期と価格は未定。
- **なぜ重要か**: エージェントが社内のデータ全体に触れる前提の設計になる。どのデータにどの権限で届くかが、監査の主な対象になる。
- 出典: [The Decoder](https://the-decoder.com/openai-is-building-athena-data-platform-to-cut-down-on-ai-agent-guesswork/)

### [2026-11-27] Hugging Face、AWS Trainium3 で動画生成モデル LTX-2.5 を動かす手順を公開
- **何が起きたか**: Hugging Face が、trn3.48xlarge (NeuronCore 64 基) の半分のコアで、音声付きの 10 秒の動画を 22〜23 秒で生成した結果を公開した (モデルの読み込み後の時間)。diffusers を使い、台本から短い動画を作る手順も示した。
- **なぜ重要か**: NVIDIA 以外の推論基盤が実際に使える段階に入りつつある。動画のディープフェイクを作るコストも下がり続けている。
- 出典: [Hugging Face Blog](https://huggingface.co/blog/video-trainium3)

### [2026-11-27] SAP、AI への転換で 1 万人以上を削減する計画 (Bloomberg 報道)
- **何が起きたか**: 報道によると、削減は従業員約 11 万人の 9% 以上にあたり、製品開発、エンジニアリング、営業での削減が大きい。ドイツでは 2028 年まで雇用が保証されている。
- **なぜ重要か**: 同じ日に SAP は GitHub への侵入も認めている (セキュリティニュースを参照)。大規模な組織再編と開発基盤の侵害が重なると、権限の棚卸しや退職者のアカウントの管理が手薄になりやすい (評価)。
- 出典: [The Decoder](https://the-decoder.com/sap-plans-to-cut-at-least-10000-jobs-as-it-pivots-to-ai/)

## AI セキュリティ

### [2026-11-27] [続報] スイス NCSC、AI エージェントによる攻撃は「5 件中 4 件で侵入」。重要インフラが狙われた 3 件のうち 2 件が成功
- **何が起きたか (前回から変わった点)**: 前回の報道では「確認した全件で侵入」とされていた。NCSC の局長 Schütz 氏は SRF の取材で、件数を「5 件を確認し、4 件で侵入、重要インフラは 3 件中 2 件で成功、大きな障害はなし」と言い直した。食い違いの理由は説明されていない。ネットで手に入る AI の攻撃ツールは、10 月から約 2 倍に増えたという。イタリアの CSIRT Italia は、組み込みのプロンプトでモデルの安全上の制限を回避する DeepSeek Harness の「Red Team Mode」を名指しした。
- **なぜ重要か**: パッチを当てていない既知の脆弱性を、エージェントが並列で突いてくる。公開から悪用までの猶予を、これまでより短く見積もる必要がある。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/switzerland-confirms-ai-assisted.html)

### [2026-11-27] CREST の調査: 脅威ベースのペネトレーションテスト (TLPT) の事業者の 81% が AI を実務で使う。自律での実行を認めるのは 1 社だけ
- **何が起きたか**: CREST が 26 社の回答をまとめた。65% は、今後 12 か月で TLPT の作業の 40% 以上を AI が支えると見ている。規制下で TLPT を行う 11 社は、どこも AI による自律の試験を認めていない。自律での実行を認めるのは商用の 1 社だけだった。上位のリスクは「スコープと運用の管理」と「顧客データ」で、いずれも 68%。声のクローンなどを使うなりすましには、正当な理由と承認が必要だとしている。
- **なぜ重要か**: AI を使う診断で「どこまで自律で動かしてよいか」「何を保証できるか」の業界の目安になる。契約書や作業計画書の書き方に直接関わる。
- 出典: [Help Net Security](https://www.helpnetsecurity.com/2026/11/27/crest-ai-threat-led-penetration-testing/)

### [2026-11-27] 国内: Codex のサブエージェントに `sandbox_mode = "read-only"` と書いてもファイルを書けた。git diff の許可から作業ディレクトリの外にも書ける
- **何が起きたか**: Zenn の記事が、codex-cli 0.172.0 で read-only と定義したサブエージェントが親と同じ workspace-write の権限で動き、ファイルを作れたことを報告した。セッションの記録 (`~/.codex/sessions`) で確かめている。さらに、`git diff` で始まるコマンドは sandbox の外で確認なしに通す規則があり、`--output` を付ければ作業ディレクトリの外に書ける経路があった。記事は、Claude Code のサブエージェントにも個別の sandbox はないと指摘している。
- **なぜ重要か**: エージェントの権限の設定が、書いたとおりには効いていない例。コーディングエージェントを診断するときは、設定ファイルを読むだけでなく、実際に動かして境界を確かめる必要がある。「安全とされたコマンドの引数で任意のファイルに書く」型は、他のエージェントの許可リストにも同じ形で起こりうる。
- 出典: [Zenn](https://zenn.dev/yomitoka/articles/claude-code-codex-shared-config)

### [2026-11-27] 国内: 拒否の応答を消すツール「heretic」の「KL 0.0000」は劣化なしを意味しなかった。Qwen3 の `<think>` が指標をすり抜けていた
- **何が起きたか**: Zenn の記事によると、heretic-llm 2.1.0 で Qwen3-0.6B の拒否は 20 件中 6 件から 0 件に減り、KL も 0.0000 と表示された。しかし、KL を計算する `kl_divergence.py` は、無害なプロンプトへの応答の最初の 1 トークンしか比べていなかった。思考の部分 (`<think>`) から書き始めるモデルでは、劣化を測れていなかった。
- **なぜ重要か**: abliteration で安全の仕組みを外しても「性能は落ちない」という主張や、安全性の評価の指標は、実装まで読んで確かめるべきだと示している。
- 出典: [Zenn](https://zenn.dev/matsushima_a/articles/day-059-heretic-kl-think-prefix)

## セキュリティニュース

### [2026-11-26〜27] Cacti に修正版のないゼロデイ「4HTTP2SHELL」。ゲストが有効なら HTTP リクエスト 4 回で RCE
- **何が起きたか**: 今日の深掘りを参照。Cacti 1.2.31 で、ゲストアカウントが有効な場合に、2 次の SQLi からポーラーのコマンド実行に至る。CVE は未採番で、修正版はない。
- **悪用 / PoC**: PoC は GitHub で公開済み。11/27 の時点で実際の攻撃は報告されていない (watchTowr)。
- **なぜ重要か**: 修正版がないため、当面はゲストを無効にすることが唯一の対策になる。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/unpatched-cacti-zero-day-with-public-poc-gives-remote-code-execution/)

### [2026-11-27] Linux カーネルの NFS サーバーに 12 年前からあったヒープオーバーフロー「NFS2ROOT」(CVE-2026-99362)。認証なしでリモートから root
- **何が起きたか**: カーネル 3.16 (2014 年) 以降の nfsd (NFSv4.1 / 4.2) にヒープオーバーフローがあり、TCP/2049 に届けば認証なしで攻撃できる。発見者は ANSSI の Jérémy Jean。修正版は 6.12.117、6.18.61、7.3.2、7.4-rc1。検知の手がかりとして、`nfsd4_check_resp_size` の警告と、カーネルのワーカーから起動されたシェルが挙げられている。
- **悪用 / PoC**: OpenSec は KASLR を回避して root を取る完全なエクスプロイトを作り、9 月下旬にメンテナーへ共有した。公開されたかは記事からは確認できない。実際の攻撃は報告されていない。
- **なぜ重要か**: NAS、ビルドファーム、Kubernetes のストレージノードなど、2049/tcp を開けているサーバーは社内に多い。社内のペンテストでは、NFS を見つけたらカーネルの版を必ず確かめる項目になる。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/new-nfs2root-linux-flaw-can-let-attackers-gain-root-privileges/)

### [2026-11-27] SAP、GitHub の開発環境への侵入を認める (社内の対応名「Project Granite」)。ソースコードを複製・改変されたと報道
- **何が起きたか**: Der Spiegel の報道によると、社員の認証トークンを盗まれ、GitHub 上の SAP のソースコードを複製・改変された。SAP は GitHub へのアクセスを制限し、自動の開発処理を止め、ソフトウェアの真正性を確かめる署名の鍵を入れ替えた (Handelsblatt / dpa)。SAP は「顧客の業務データへの不正アクセスの証拠はない」と説明している。改変されたコードが製品として出荷されたかは不明。
- **悪用 / PoC**: 実際の侵害。攻撃者は公表されていない。
- **なぜ重要か**: 1Password、Todoist に続き、今週 3 件目の「開発者のトークンから GitHub に入る」侵害。署名の鍵を入れ替えたということは、改変されたコードに正規の署名が付いた可能性を否定できないということでもある (評価)。SAP の更新を当てる側は、今後出る SAP の告知を追う必要がある。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/sap-confirms-security-incident-after-suspicious-github-activity/) / [The Record](https://therecord.media/sap-germany-cyberattack-github)

### [2026-11-27] 米空軍のクラウド基盤「Cloud One」に侵入と報道 (Reuters)
- **何が起きたか**: Reuters によると、侵入は過去 1 か月以内に、基盤の更新作業の途中で見つかった。「特定されていないソフトウェアの脆弱性」が悪用されたとされ、米サイバー軍が影響を調べている。攻撃者、範囲、データが盗まれたかはわかっていない。FBI の NCIC、CIA、財務省 (FinCEN) などに続く、連邦機関への一連の侵害の 1 つ。
- **悪用 / PoC**: 実際の侵害。脆弱性は特定されていない。
- **なぜ重要か**: 防衛向けの政府クラウドまで侵害が及んだ。同じ脆弱性が特定されれば、民間のクラウド基盤にも波及する可能性がある。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/us-air-force-cloud-platform-reportedly-hacked-in-latest-federal-breach/)

### [2026-11-27] パスワードマネージャーの pCloud Pass に攻撃。2FA を有効にしていても「新しい端末 "pd" が接続」と通知
- **何が起きたか**: 利用者のもとに、IP 45.131.244.7 (ルクセンブルク) から新しい端末「pd」が接続したという通知が届いた。2FA を有効にしていた利用者にも届いている。利用者は、この IP が pCloud 自身の基盤のものだと指摘している。pCloud は「一部のメールアドレスが漏れ、ログインが試みられた」と認め、保管庫は端末の側で暗号化しているため安全だと説明している。暗号化された保管庫を持ち出されたかは明らかにしていない。
- **悪用 / PoC**: 実際の攻撃。手口は公表されていない。
- **なぜ重要か**: 2FA を有効にした利用者にも端末の追加の通知が出ていることから、認証の流れか端末の登録の仕組みの側に問題がある可能性がある (評価)。1Password と同じ週の、パスワード管理の製品の 2 件目の事案。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/pcloud-confirms-password-manager-hack-after-suspicious-login-alerts/)

### [2026-11-27] 公式サイトで配られた Q-Dir と DesktopOK のインストーラーが改ざんされ、Python の RAT を入れる (AhnLab)
- **何が起きたか**: 改ざんが確認されたのは、SoftwareOK の Q-Dir 12.83 / 12.84 / 12.85 と DesktopOK 12.82 / 12.85。直接のダウンロードに加え、アップデートの経路でも配られた。正規のアプリを動かしながら `mail.c1a2[.]top` から Python の RAT を取得し、Edge を装ったスケジュールタスクで常駐させる。C2 は `8.210.69[.]51:9876`。どうやって差し替えたかは不明。
- **悪用 / PoC**: 実際の配布を確認。
- **なぜ重要か**: 個人の開発者が作る便利ツールの公式サイトとアップデーターは、守りが薄い。社内の端末で該当のバージョンを使っていないか、SHA-256 と IoC で確かめたい。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/hackers-trojanize-official-q-dir-and.html)

### [2026-11-27] Microsoft Store のアプリ「Setup Assistant」が PowerShell の RAT「Vinci RAT」を配っていた (eSentire)
- **何が起きたか**: 入口は偽の Snipping Tool のサイト `snipp.codes-team[.]com`。そこから Microsoft の署名つきのインストーラーを経て、ETPS Ltd が公開した Electron 製のストアアプリが入る。アプリは C2 から PowerShell や JavaScript を受け取って実行し、stager は AMSI を無効にして 10 分ごとのタスクで常駐する。eSentire は 11/10 に Microsoft へ通報したが対応がなく、現在はストアから消えている。
- **悪用 / PoC**: 実際の配布を確認。
- **なぜ重要か**: 「ストアにある署名済みのアプリ」を安全の根拠にはできない。アプリの許可リストを運用している組織では、ストアのアプリの扱いを見直す材料になる。レッドチームの初期アクセスの経路としても参考になる。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/microsoft-store-app-found-delivering.html)

### [2026-11-27] ベトナム系とみられる「WeaveLotus」、南シナ海の情報を狙ってタイとフィリピンに 5 件侵入 (SOCRadar、作戦名 RedOps)
- **何が起きたか**: SOCRadar によると、初期の侵入には GeoServer、JasperReports、osTicket の脆弱性や既定の認証情報、Laravel の debug モードの露出が使われた。侵入後は逆方向の SSH トンネルで社内に居座った。インドネシアには偵察だけを行った。期間は 2026 年 8〜9 月。
- **悪用 / PoC**: 既知の脆弱性と設定の不備を実際に悪用。
- **なぜ重要か**: 国家系の攻撃者でも、初期の侵入は「既知の OSS の Web アプリ」と「`APP_DEBUG=true`」が中心。外部の診断で最初に確かめる項目の優先順位を裏付けている。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/suspected-vietnam-linked-hackers-target.html)

### [2026-11-27] 被害: Boston Scientific の侵害は 11 万 7,789 人 (音声のフィッシングから)。Flight Centre も顧客の記録へのアクセスを開示
- **何が起きたか**: Boston Scientific はテキサス州の司法長官への届け出で、11 万 7,789 人分の被害を報告した。5 月の vishing (音声のフィッシング) でクラウドのアプリとデータに入られたもので、患者の医療記録と、接続された医療機器のデータは含まれないとしている。豪州の Flight Centre も同じ日に、外部の宿泊予約のシステムで顧客の記録に「相当数」アクセスされたと開示した。ごく一部には旅券の情報が含まれる。
- **悪用 / PoC**: 実際の侵害。
- **なぜ重要か**: ヘルプデスクへの電話で SaaS に入る手口が、医療の業界にも及んでいる。ソーシャルエンジニアリングの演習で、電話による本人確認の手順を試す意義を示している。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/new-boston-scientific-data-breach-exposes-personal-medical-info/) / [Help Net Security](https://www.helpnetsecurity.com/2026/11/27/flight-centre-travel-group-data-breach/)

### [2026-11-27] 被害: AFP の配信基盤「AFP Forum」が攻撃で停止。英国の雇用年金省 (DWP) もオンラインのサービスの一部を止める
- **何が起きたか**: AFP は 11/26 の夜間に侵入され、報道機関向けの配信基盤「AFP Forum」を止めた。英国の DWP は「サイバーインシデント」とだけ説明し、NCSC と調べている。年金と給付の支払いには影響がないとしている。どちらも攻撃者はわかっていない。
- **悪用 / PoC**: 実際の攻撃。手口は公表されていない。
- **なぜ重要か**: 報道の配信基盤が止まると、それを使う各国の報道機関にも影響が広がる。手口が公表されたら続報として追う。
- 出典: [The Record (AFP)](https://therecord.media/france-afp-hit-by-cyberattack) / [The Record (DWP)](https://therecord.media/uk-department-work-pensions-cyber-incident)

### [2026-11-26] フィッシングの「GoodGuys」、有償の専門家インタビュー (45 分で最大 600 ドル) を装い、Google と Okta の企業アカウントを盗む (Push Security)
- **何が起きたか**: Push Security によると、このキャンペーンは Google Cloud、Nvidia、Accenture、SpaceX など 8 社を装い、10/13 から追跡されている。インタビューの日程を決める流れの中で、偽のログイン画面に誘導して Google と Okta の資格情報を盗む。
- **悪用 / PoC**: 実際のキャンペーン。
- **なぜ重要か**: 「専門家として謝礼つきで話してほしい」は、技術者が乗りやすい口実。SSO を経由した乗っ取りを試すソーシャルエンジニアリングの演習のシナリオとして現実的。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/apple/fake-paid-expert-interviews-impersonate-brands-to-steal-google-logins/)

### [2026-11-27] Microsoft、Windows Server 2028 から WSUS の役割を外す。11 月の hotpatch で起きた Server 2025 の停止は帯域外の KB5138318 で修正
- **何が起きたか**: WSUS は 2024 年 9 月に非推奨になっており、Server 2028 では役割そのものがなくなる。2025 までの版ではサポートが続く。帯域外の KB5138318 は、KB5131077 を当てた後に、RA が有効で期限つきの IPv6 経路を受け取るサーバーで起きる KERNEL_SECURITY_CHECK_FAILURE (0x139) を直す。
- **悪用 / PoC**: 該当なし (製品の変更と不具合の修正)。
- **なぜ重要か**: HTTP で動く WSUS を悪用するなどの社内の攻撃が通じる環境は、長い目で見ると減っていく。0x139 の停止は、IPv6 の RA を受け取る環境で再起動が繰り返される障害につながるため、運用側は確認が必要。
- 出典: [BleepingComputer (WSUS)](https://www.bleepingcomputer.com/news/microsoft/microsoft-removes-wsus-server-role-in-windows-server-2028/) / [BleepingComputer (OOB)](https://www.bleepingcomputer.com/news/microsoft/new-out-of-band-oob-emergency-hotpatch-fixes-windows-server-2025-crashes/)

### [2026-11-27] 法執行: 米司法省、詐欺の一斉摘発で 800 人超を訴追。押収は約 170 億ドル
- **何が起きたか**: 米司法省によると、摘発は 85 の連邦地区で 400 件超に及んだ。30 人が米国へ引き渡され、10 か国超で詐欺のコールセンターや拠点を捜索した。2026/3/6 の大統領令 14390 に基づく取り組み。
- **悪用 / PoC**: 該当なし。
- **なぜ重要か**: 東南アジアの詐欺拠点への国際的な取り締まりが続いている。日本を狙う特殊詐欺の拠点への影響も注目される (評価)。
- 出典: [Help Net Security](https://www.helpnetsecurity.com/2026/11/27/doj-scam-crackdown-800-scammers/)

### [2026-11-27] 週のまとめ (THN ThreatsDay): 「NGINX2Root」の影響を受ける NGINX が 1,000 万件超露出、悪意のある拡張機能「SleeperWidget」が 250 超
- **何が起きたか**: Censys によると、「NGINX2Root」の影響を受ける HTTP/2 を有効にした NGINX が 1,000 万件超、インターネットに露出している。特定の機能が有効だとワーカーのメモリを壊すことができ、ASLR がないか回避できればコードの実行に至る。Microsoft は、Edge / Chrome / Firefox の 250 超の拡張機能「SleeperWidget」を報告した。有料の検索広告から入れた場合にだけ悪意のある動作をする。
- **悪用 / PoC**: NGINX2Root の実際の悪用はまとめ記事の中では示されていない。
- **なぜ重要か**: NGINX の露出の数は、外部の診断で NGINX の版と HTTP/2 の設定を確かめる優先度の高さを示している。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/threatsday-250-rogue-extensions-10m.html)

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-11-26 以降 (NVD の published で確認) / 修正コミット公開済み or バグクラスが言語化可能なものを優先。新規の KEV 追加はなし (11/27 追加の 3 件はすべて既出)。EPSS は全候補で 0.5 未満。

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-120353 | Apache Airflow (TaskFlow / common.ai のデコレーター) | CWE-1336 / 未付与 | レンダリング済みの値を Jinja で**再レンダリング** → run conf やプロンプト由来の文字列がテンプレートとして評価され worker 上で RCE | [PR #76244](https://github.com/apache/airflow/pull/76244) | oss-security 2026/11/27 掲載 |
| CVE-2026-133842 / GHSA-p4mw-6jfq-r82r | Flatpak < 1.18.6 | CWE-281 / 8.2 (v3.1) | 深いディレクトリで権限の正規化が EMFILE で失敗しても**成功として返す** (fail-open) → setuid のビットが残り root LPE | [commit](https://github.com/flatpak/flatpak/commit/a21a102e10d63da3251421b17a60b977e6c4b5c8) / [commit](https://github.com/flatpak/flatpak/commit/d087606b9a041f3b0debe44a9b9c3beab28b6e6c) | LPE / 主要ディストリに同梱 |
| CVE-2026-137938 (+137939) / GHSA-3x7w-j75x-ppq5 | Sparkle < 2.9.6 (macOS の自動更新) | CWE-367 / 7.3 (v4) | symlink を解決した後のパスで検証し、**未解決のパスで** root 権限の move → 中間ディレクトリの差し替えで LPE | [commit](https://github.com/sparkle-project/Sparkle/commit/8b73733ac2b95b7054acdafc5a564a0457fcf40e) / [137939](https://github.com/sparkle-project/Sparkle/commit/dcfe48d28262d46e2098b20f0f482359341909bf) | 多数の macOS アプリに組み込み |
| CVE-2026-137907 | FFmpeg 3.0 〜 < 8.1.3 (vf_boxblur.c) | CWE-787 / 8.5 (v4) | 16 bit を超える pixfmt を許可するのに一時バッファは 2 B/px → PFM / EXR の入力で heap overflow | [commit](https://github.com/FFmpeg/FFmpeg/commit/0dac41d2e5e0f4251ed89eedb03a847d5d59ef67) | 同日に CVE-2026-137905〜137911 も公開 |
| CVE-2026-137937 / GHSA-527h-2p2v-g388 | PDFio < 1.6.5 | CWE-191 / 6.9 (v4) | AES の値が IV の 16 B だけのとき、復号の前に PKCS#7 のパディングを除去 → 長さがアンダーフローし `_pdfioValueDecrypt()` で heap の OOB R/W | [commit](https://github.com/michaelrsweet/pdfio/commit/bb77255b2832c2b35fe502237ac1b452221e74ff) | 仕様由来 / 他の PDF 実装に横展開 |
| CVE-2026-137307 | wpa_supplicant 2.7〜2.12 (wolfSSL のバックエンド) | CWE-287 / 2.3 (v4) | 長すぎる PAC-Opaque で `tls_sess_sec_cb()` が master secret の導出を飛ばす → 全ゼロの鍵で EAP-FAST が成立し、偽の AP が MS-CHAPv2 を取得して PAC を差し替え | [commit](https://git.w1.fi/cgit/hostap/commit/?id=d8fa00ae24d729dfc5e4f7b2b012e5b5723856fc) | プロトコル由来 / TLS バックエンドごとの差分 |
| CVE-2026-102963 / GHSA-j577-282h-9jjr | Zephyr RTOS (DNS リゾルバ) | CWE-416 / 6.5 (v3.1) | CNAME だけの応答で再問い合わせすると query_hash が上書きされ cancel が失敗 → タイムアウト済みの getaddrinfo の**スタック上の ctx** にコールバックが書き込む | [commit](https://github.com/zephyrproject-rtos/zephyr/commit/50a1257c045af73bc3e00df92728ede68627ffe8) | 組込みの DNS 実装に横展開 |
| CVE-2026-137977 / CVE-2026-137978 | Nmap < 7.992 (massdns.cc) | CWE-416 / 7.7 (v4) | DNS 応答と偽装した ICMP unreachable の到着を揃える → 解放済みの request を参照して UAF | [commit](https://github.com/nmap/nmap/commit/37a95cb34ff4bdbb8527f58ab66bd1017fb7de5d) / [commit](https://github.com/nmap/nmap/commit/cd74c02e2f53d57ba19a9a63398ea7d3bc7cb942) | 診断ツール自体の脆弱性 |
| CVE-2026-137326 | ICU4C ≤ 79.1 (ucnv_ct.cpp) | CWE-416 / 7.3 (v4) | x11-compound-text のコンバーターの clone に safeClone がなく extraInfo を共有 → 解放後に使用 / 二重解放 | [PR #4297](https://github.com/unicode-org/icu/pull/4297) (追補 [#4376](https://github.com/unicode-org/icu/pull/4376)) | 依存の裾野が広い |
| CVE-2026-137992 / CVE-2026-137951 | libexpat ≤ 2.11.0 | CWE-407 / 8.7、CWE-125 / 6.3 (v4) | 重複する ATTLIST を検出せず `storeAtts()` が二乗の計算量 → DoS。`XML_GE=0` + `XML_UNICODE` のビルドで narrow のリテラルを wide として読み OOB read | [PR #1537](https://github.com/libexpat/libexpat/pull/1537) / [PR #1534](https://github.com/libexpat/libexpat/pull/1534) | 依存の裾野が広い |
| CVE-2026-137507 | torchvision < 0.29.2 (`_extract_tar()`) | CWE-22 / 7.1 (v4) | 検査していない tar のメンバーを展開 → 展開先の外に書き込み、モジュールを上書きして RCE | [commit](https://github.com/pytorch/vision/commit/7a7520f83957fe6a0f934fe7035f07b5ef32e8f9) | 同型: lastversion CVE-2026-137539、xtractr CVE-2026-137569、openFrameworks CVE-2026-137568 |
| CVE-2026-137465 / GHSA-r66f-3q22-grc4 | Parse Server 3.10.0〜< 8.6.123、9.0.0〜< 9.11.1-alpha.4 | CWE-287 / 9.1 (v4) | Play Games の player ID とトークンの**紐付けを検証しない** → 他人の ID を名乗ってアカウントを乗っ取り | [advisory](https://github.com/parse-community/parse-server/security/advisories/GHSA-r66f-3q22-grc4) (commit 不明) | Critical |
| CVE-2026-137536 / GHSA-7g4q-wmw6-7r36 | ToolJet < 3.21.94-beta | CWE-290 / 9.3 (v4) | OIDC の `email_verified` を確かめず subject も束縛しない → 未認証で管理者のセッションを取得 | [advisory](https://github.com/ToolJet/ToolJet/security/advisories/GHSA-7g4q-wmw6-7r36) (commit 不明) | Critical |
| CVE-2026-135384 / GHSA-v3m9-p36m-qjqc | Canonical LXD < 5.0.12 / 5.21.10 / 6.10.2 | CWE-287 / 9.2 (v4) | トークンの `aud` と種別を検証しない → 他のアプリ向けに発行されたトークンで API の認証が通る | [advisory](https://github.com/canonical/lxd/security/advisories/GHSA-v3m9-p36m-qjqc) (commit 不明) | Critical |
| CVE-2026-135279 / GHSA-f9qf-hfc5-7xpj | @fastify/express < 4.0.14 | CWE-436 / 9.1 (v3.1) | 空の動的パラメーターを Fastify は受理し Express は拒否する**解釈の差** → Express 側の認証ミドルウェアが飛ばされる (以前の修正の不完全さ) | [advisory](https://github.com/fastify/fastify-express/security/advisories/GHSA-f9qf-hfc5-7xpj) (commit 不明) | Critical / 修正の迂回 |

**今日の CVE 所感**
- **IdP の主張の束縛漏れ** (`email_verified` / `aud` / subject / player ID) が、同じ日に Parse Server、ToolJet、LXD の 3 製品で出た。OAuth / OIDC のアダプターを多く持つ BaaS やローコードの製品では、「トークンの署名は検証しているが、誰向けの、誰のトークンかを確かめていない」箇所を優先して見たい。
- **非同期の DNS リゾルバの寿命管理による UAF** が、Zephyr と nmap で同時に出た。c-ares、lwIP、組込み向けの getaddrinfo の実装で「cancel に失敗したとき、呼び出し側のスタックの ctx が残らないか」を確かめる価値がある。
- **仕様由来の境界のミス** (EAP-FAST の PAC の長さ、PKCS#7 のパディングを外す前に暗号文のブロックがあるかの検査) は、他の TLS バックエンドや PDF の実装 (poppler、mupdf、qpdf、pdf.js) に横展開しやすい。
- **fail-open と TOCTOU による LPE** (Flatpak、Sparkle) は、特権のヘルパーを持つ更新の仕組みやパッケージャー (snapd、PackageKit、macOS のアップデーター) が横展開の候補。
- ML や科学計算の Python では、tar の展開でのパストラバーサル (4 件) と pickle のデシリアライズが量産されている。`tarfile` の `extractall()` で `filter=` を指定していない箇所を grep するのが効率的。
- commit は不明だが、エンタープライズで影響の大きいものに ESX の UAF (CVE-2026-123911、9.8)、RealVNC の UDP 経由・未認証の RCE (CVE-2026-137738、9.8)、Mitel OpenScape 4000 (CVE-2026-137721 / 137724、10.0) がある。いずれもベンダーの告知を確かめる対象。

## 日本国内のセキュリティ動向

### 国内インシデント・事故

#### [2026-11-27] GMOペパボ、内部システムへの不正アクセスで「ロリポップ！」など 4 サービスの顧客情報 51 万 6,564 件が漏えいした可能性。平文で保存していたパスワードも
- **何が起きたか**: GMOペパボは 11/24 に内部システムへの不正アクセスを検知した。データ分析基盤を経由して、「ロリポップ！レンタルサーバー」など 4 サービスの顧客情報 51 万 6,564 件が持ち出された可能性がある (カード情報と口座情報は含まない)。平文で保存していたパスワードも漏えいした。内訳は、仮設定の FTP / WebDAV パスワード 8,322 件、ムームードメイン経由の初期ログインパスワード 4,170 件、顧客が設定した Basic 認証の ID とパスワード 10 万 5,608 件。11/25 に強制的なリセットを終えて総務省へ報告し、11/27 に公表した。
- **なぜ重要か**: レンタルサーバーの Basic 認証は、管理画面やステージング環境を守るのに使われていることが多い。顧客が他のサービスでも同じパスワードを使っていれば、被害が広がる。診断では「分析基盤に認証情報が平文で流れ込んでいないか」「分析基盤から本番のデータにどこまで届くか」を確かめる価値がある。
- 出典: [GMOペパボ](https://pepabo.com/news/information/202611271430/) / [INTERNET Watch](https://internet.watch.impress.co.jp/docs/news/2160136.html)

#### [2026-11-27] ZOZO、開発環境の脆弱性からクラウドの認証情報を取られ、本番の DB まで侵入される。漏えいのおそれは最大約 594 万人分 (KARTE の件とは別)
- **何が起きたか**: ZOZO は 10/21 に異常を検知した。攻撃者は ZOZOTOWN の開発環境の脆弱性を突いて管理用ページに入り、そこにあった本番で使うクラウドの認証情報を取得した。そこからクラウドの本番環境を経て、自社サーバーの DB にまで侵入した。漏えいが確定したのは本番の顧客 1 人。漏えいのおそれがあるのは、開発環境のマスク済みデータで最大約 594 万人、ギフト用の画像で最大約 45.6 万人、WEAR の検証環境 (2019 年 4 月時点のデータ) で最大 2,020 人。11/27 に公表し、同日から順次通知している。11/20 に公表された KARTE 経由の件とは別の事案。
- **なぜ重要か**: 開発環境に本番の認証情報が置かれていたことが、本番の侵害につながった。診断の範囲を「本番だけ」に絞る契約の弱点を示している。開発・検証環境の管理画面と、そこにある秘密情報の棚卸しは優先度が高い。
- 出典: [ZOZO](https://corp.zozo.com/information/20261127-029115/)

#### [2026-11-27 報道] 東京海上ダイレクト、契約者のマイページに不正アクセス。接続していた外部のサービスが経路となり 93 人分が流出
- **何が起きたか**: Security NEXT によると、同社は 11/4 にマイページへの不審なアクセスを検知した。同社が接続していたサービスが、不正アクセスの経路になっていた。11/9 の時点で、契約 71 件・関係者を含む 93 人分の流出を確認している。氏名、住所、免許証の色、車両の情報、運転のトリップ情報、事故の情報、カード番号の下 4 桁などが含まれる。組織の公表日は記事からは確認できなかった。
- **なぜ重要か**: 連携先のサービスから本体のマイページに届く経路は、診断の範囲から漏れやすい。連携の API の権限の範囲も対象に入れたい。
- 出典: [Security NEXT](https://www.security-next.com/193168)

#### [2026-11-27 報道] ヴェレダ・ジャパンの通販サイトが改ざんされる。個人情報 19 万 8,792 件と、セキュリティコードを含むカード情報 4 万 5,689 人分が流出した可能性
- **何が起きたか**: Security NEXT によると、同社は 6/30 に警察から連絡を受け、7/3 にカード決済を止めた。対象の期間は 2021/10/1〜2026/6/30 で、個人情報 19 万 8,792 件が流出した可能性がある。カードの利用者 4 万 5,689 人分は、セキュリティコードを含むカード情報が流出した可能性がある。11/24 から対象者にメールで連絡している。サイトは作り直して、2027 年 3 月をめどに再開する予定。
- **なぜ重要か**: 約 5 年間気づかれなかった決済画面の改ざん。EC サイトの診断では、決済画面の JavaScript の改ざんを検知する仕組みがあるかも確かめたい。
- 出典: [Security NEXT](https://www.security-next.com/193310)

#### [2026-11-27 報道] ソースネクスト、株主向けの問い合わせフォームの設定不備で 137 件が閲覧できる状態に
- **何が起きたか**: Security NEXT によると、ソースネクストの株主向けの問い合わせフォームで、設定の不備により 137 件の問い合わせの内容が外部から閲覧できる状態になっていた。
- **なぜ重要か**: フォームのサービスの公開範囲の設定ミスは、診断よりも設定の確認で見つかる類型。SaaS のフォームの棚卸しの例として使える。
- 出典: [Security NEXT](https://www.security-next.com/193162)

### 国内の注意喚起・ガイドライン・政策

#### [2026-11-26] 個人情報保護委員会、令和 8 年度第 2 四半期の監視・監督の状況と、漏えい等報告の処理状況を公表
- **何が起きたか**: 民間事業者への指導・助言は 95 件 (全体で 117 件) だった。原因として多かったのは、公開済みの VPN や EC アプリの脆弱性の放置、推測されやすい ID とパスワード、DB のアクセス制御の設定ミス。ランサムウェアは 16 件。漏えい等報告の処理件数は 5,951 件で、前年度を四半期に換算した 4,854 件を上回った。資料の日付は 11/25 で、サイトの新着情報には 11/26 に掲載された。
- **なぜ重要か**: 当局が挙げる原因の上位 (既知の脆弱性、弱い認証、アクセス制御) は、診断の基本の確認項目とそのまま重なる。報告書で指摘の優先順位を付けるときの根拠として使える。
- 出典: [個人情報保護委員会](https://www.ppc.go.jp/personalinfo/activity/) / [監視・監督の状況 (PDF)](https://www.ppc.go.jp/files/pdf/261125quarter-report_kengenkoushi.pdf) / [漏えい等報告 (PDF)](https://www.ppc.go.jp/files/pdf/261125quarter-report_roueihoukoku.pdf)

#### [2026-11-27] JPCERT/CC ベストレポーター賞 2026。インシデント報告部門は伊藤忠サイバー＆インテリジェンスの武田氏 (1 年で 350 件超)。脆弱性報告部門は該当者なし
- **何が起きたか**: 受賞の理由は、不正に使われたメールアカウントから送られた不審なメールを分析し、継続して報告してきたこと。脆弱性報告部門は、今年度は受賞者がいなかった。
- **なぜ重要か**: 脆弱性報告部門に受賞者がいなかったことは、国内の研究者による調整機関への報告の状況を考える材料になる。
- 出典: [JPCERT/CC](https://www.jpcert.or.jp/award/best-reporter-award/2026.html)

#### [2026-11-26] 総務省「不適正利用対策に関するワーキンググループ」第 16 回の資料を公開
- **何が起きたか**: 11/26 に開かれ、NTT 東西、ドコモ、KDDI、ソフトバンク、楽天モバイル、国際電話不取扱受付センターの説明資料が掲載された。第 17 回は 12/1 に開かれる。
- **なぜ重要か**: 特殊詐欺に使われる電話や SMS への対策の議論。診断への直接の影響は小さいため参考として載せる。
- 出典: [総務省](https://www.soumu.go.jp/main_sosiki/kenkyu/ICT_services/02kiban18_02000523.html)

> この期間には、IPA、国家サイバー統括室、警察庁、金融庁、経産省から、新しい注意喚起やガイドラインは見つからなかった。

### 国内製品の脆弱性 (JVN)

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| 2026-11-27 | JVN#19729125 / CVE-2026-130398〜130400 | マイナアプリ (旧マイナポータルアプリ) Android / iOS / デジタル庁 | 入力の許可リストによる制限が不十分 (CWE-183)。不正なリンクを踏むと任意のサイトに遷移させられ、フィッシングにつながる。Ver2026.8.0 / 2026.11.0 より前が対象。報告は GMO Flatt Security の RyotaK 氏ほか | v3.0 4.3 / v4.0 5.3 | [JVN](https://jvn.jp/jp/JVN19729125/) |
| 2026-11-27 | JVN#36592422 / CVE-2026-105831 | EspoCRM (海外の OSS。JVN が調整) | Lead Capture のフォームから、認証なしで HTML を保存させて XSS を起こせる。10.0.5 以前が対象 | v3.0 6.1 / v4.0 5.3 | [JVN](https://jvn.jp/jp/JVN36592422/) |
| 2026-11-26 | JVNDB-2026-045359 / CVE-2026-114938 | 日立 Cosminexus Developer's Kit for Java、uCosminexus Application Server ほか | OpenJDK の脆弱性 (いわゆる Java4Shell) が日立のミドルウェアにも及ぶ | v3.0 8.1 High | [JVN iPedia](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-045359.html) |

> 対象期間 (11/26〜28) に公開され、直近 7 日の号に載っていない国内向けの JVN は 3 件だけだった。11/26 の JVN iPedia の他の新着は、Microsoft、FFmpeg、TeamCity、Mitel など海外製品。

- 診断の観点: マイナアプリの件は、モバイルアプリのディープリンクや WebView で遷移先を許可リストで正しく制限しているかという定番の観点の実例。Cosminexus は国内の基幹システムで広く使われているため、Java4Shell の影響を棚卸しするときに見落とさないようにしたい。

### 国内コミュニティ・研究・イベント

#### [2026-11-27] ScanNetSecurity「今日もどこかで情報漏えい 第 54 回」: 10 月の事故の記事は 138 本で連載の最多。うち不正アクセスが 123 件 (89.1%)
- **何が起きたか**: 前の月の 105 本から 33 本増えた。被害の規模では上位 18 件が 100 万件を超え、1 位は Gyazo の約 2,362 万件だった。
- **なぜ重要か**: 国内で漏えいの規模が大きくなっていることを示す定点観測の数字。提案書やリスクの説明の材料になる。
- 出典: [ScanNetSecurity](https://scan.netsecurity.ne.jp/article/2026/11/27/56921.html)

#### [2026-11-27] ITmedia: 米パデュー大学の 1 万 2,511 人規模の再現研究で、フィッシング対策の研修に有意な効果は見られず
- **何が起きたか**: クリック率は、研修なしが 9.8%、講義のみが 10.6%、体験型の演習ありが 10.4% だった。差を生んだのは研修の有無ではなくメールの難しさで、「難」の 15.0% は「易」の 7.0% の約 2 倍。17 種類の偽のメールのうち 52.9% では、最初のクリックより先に誰かが通報していた。
- **なぜ重要か**: 標的型メールの訓練の評価で、クリック率ではなく「通報から自動で隔離されるまでの時間」を指標にする根拠になる。
- 出典: [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2611/27/2000003502/)

#### [2026-11-26 報道] エーアイセキュリティラボ「iOS A2B診断」: 公開前の IPA ファイルを解析し、バックエンドの API の認証・認可の不備を AI が確かめる
- **何が起きたか**: 11/24 に提供を始めた。Swift / Objective-C のバイナリから API のエンドポイントを復元し、AI がログインや通信を試して不備を特定する。価格は 1 アプリ 10 万円 (期間限定・初回)。10/26 には Android 版を出している。
- **なぜ重要か**: モバイルアプリを足がかりにバックエンドを攻める「A2B」の診断が自動化されつつある。手動のモバイル診断が何に注力すべきかが問われる。
- 出典: [ScanNetSecurity](https://scan.netsecurity.ne.jp/article/2026/11/26/56909.html)

#### [2026-11-27 報道] 日本シーサート協議会「NCA Annual Conference 2026」が 12/2〜4 に開催 (テーマ「攻める、守る、そこには人がいる」)
- **何が起きたか**: 12/2 は IIJ (飯田橋) で開かれる。エーアイセキュリティラボが出展し、AI による脆弱性診断「AeyeScan」について講演する。
- **なぜ重要か**: AI の時代に CSIRT が何をするかが主題で、診断の結果を組織の対応にどうつなげるかを議論する場になる。
- 出典: [ScanNetSecurity](https://scan.netsecurity.ne.jp/article/2026/11/27/56912.html)

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 45 (RSS / Atom 約 30、NVD API、CISA KEV JSON、EPSS、各社の公式ページ、WebSearch)
- 採用件数: AI技術=11 / AIセキュリティ=4 / セキュリティ=14 / CVE=15 行 / 国内インシデント=5 / 国内政策=3 / JVN=3 / 国内コミュニティ=4
- 除外理由内訳: 古すぎ=約 12 / 重複=約 25 / 日付不明=3
  - 古すぎ (組織の公表日が範囲外で、掲載日だけが範囲内): 文部科学省の政府調達情報システムの侵害 (省の発表は 11/25。メールアドレス最大 1,778 件、事業者の情報最大 16 万 3,953 件。範囲の 1 日前のため本文から外した)、ミツモア (公表 11/16)、エネコム (11/16)、NewsPicks の調査結果 (11/18)、札幌駅総合開発 (11/17)、総務大臣奨励賞の募集 (11/20)、GMO イエラエの HITCON 1 位 (11/5)、Rapid7 の露出した Ollama の調査 (原典は 11/13。THN ThreatsDay で 11/27 に再掲)、Convex の skill の issue (10/26 起票)
  - 重複: 1Password、Todoist、Drupal (CVE-2026-136716 を含む)、GeoServer の KEV、Juniper、FIFA、ARTEX、FinCEN、Hex の続報、GPT-6.2 の利用枠、Skills over MCP、Workspace の MCP 必須化、Messages API の Rust 化、KARTE 関連、デジタル庁 GSS、六花亭、東京消防庁アプリ、baserCMS、Hitachi Command Suite、Cosminexus のパストラバーサル など
- 取得失敗ソース:
  - GitHub Advisory API (`/advisories`): HTTP 403。代替として NVD API (11/26〜28 公開の 864 件) から選び、GHSA の ID は NVD の参照から取った
  - OSV: 今回の GHSA がまだ取り込まれていなかった
  - CISA advisories の RSS: Access Denied。KEV は JSON で取得
  - opensec.in の NFS2ROOT の記事: Cloudflare のチャレンジで読めず、BleepingComputer で代替
  - MarkTechPost の記事ページ: Cloudflare で止められたため、feed の本文と pubDate を使った
  - hiddenlayer / lakera の feed: RSS ではなく HTML が返った (期間内の記事なし)。VentureBeat / DeepMind / Noma / Pillar の feed: XML として解釈できず。johann.rehberger.blog: プロキシが 502
  - IPA の security/rss/info.rdf: 404。国家サイバー統括室と金融庁の新着: JS で描画されるため日付を取れず
  - JVNDB-2026-045359 の詳細ページ: 空の応答のため、JVN iPedia の RSS から内容を取った
  - 期間内の新着なし (取得は成功): OpenAI News (最新 11/24)、Anthropic News (11/25)、Embrace The Red、arXiv cs.CR (最新 11/25)、Krebs、Talos、Unit 42、Microsoft Security Blog、watchTowr Labs の RSS、PortSwigger Research、Project Zero、Trail of Bits、The DFIR Report、IPA の alert-rss (最新 11/24)
- 備考: 米国の感謝祭の連休 (11/26〜27) のため、米国の一次情報が少なかった。Cacti の過去の CVE (CVE-2022-46169 / CVE-2023-39361 / CVE-2024-25641) は背景として一般に知られた事例を引いたもので、今回の記事の内容ではない。

</details>
