# KEDA Daily Digest — 2026-11-25 (JST)

> 採用範囲: 公開日 2026-11-23 〜 2026-11-25
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

セキュリティ側で最も大きいのは、**Elixir / Erlang のパッケージレジストリ hex.pm が、認証なしの RCE (CVE-2026-129514) で実際に攻撃されていた**件だ。11/23 18:16 UTC から 13 分間に 69 件の悪意あるリクエストが送られ、Web サーバー 6 台でコマンドが実行された。hex.pm は 20 分以内に修正版を入れた。パッケージの改ざんは見つかっていない。ただし、DB の読み取りはログに残らないため、メールアドレス、パスワードハッシュ、2FA のシークレットなどが読まれた可能性は否定できないとしている。原因は「Erlang term 形式の decode で、関数は止めたが struct (map) は通した」ことだ。同じバグクラスが、**Ash、Flop、db_connection にも CVE として同日に出た**。バリアントハントの起点として、今日いちばん価値がある。
VMware は、悪用中の CVE-2026-123890 とは**別の** vCenter vmdir の認証回避 (CVE-2026-123903、CVSS 9.8) を含む 23 件を修正した。Rapid7 は CVE-2026-123890 の root 取得までの技術解説を出した。GreyNoise は、Check Point の管理サーバー 24 台 (22 組織) が侵害されていたと報告した。Radware は、認証のない内部の Cloud WAF 管理 API が公開されていて、顧客のログ出力用のクラウド鍵が読まれた可能性があると顧客に通知した。
AI 側では、OpenAI と Cisco が、eBPF でパッチ前の Linux を守る OSS「Shirudo」を発表した。Anthropic は、複数のリクエストにまたがる悪用を検知する「Enterprise Frontier Safeguards」を公開ベータにした。Unit 42 と英国 NCSC は、AI エージェントを使った攻撃の実態と増加をそれぞれ報告した。Z.ai は loop transformer 構造の GLM-5.4 を公開した。Anthropic の株価は IPO 価格を割った。
国内では、インフキュリオンの決済基盤「Wallet Station」への不正アクセスで、鹿児島銀行「Payどん」の 25 万件超が流出した。ほかに、読売巨人軍のファンクラブ (メール 80 万件超)、ミスタードーナツのネットオーダーの侵害が報じられた。
**今日まず見るべきもの**: (1) 担当している Elixir / Phoenix アプリで、`binary_to_term` に外部入力が届く箇所 (ページネーションのカーソル、Cookie、独自のパーサー)。(2) vCenter が 9.1.2 / 9.0.2.0300 / 8.0 U3m に上がっているか。123890 の修正だけで止まっていないか。

## 今日の深掘り

### hex.pm が認証なしの RCE (CVE-2026-129514) で攻撃された。「safe な binary_to_term」が struct を通し、Inspect → Enumerable の連鎖で任意の関数呼び出しになった (2026-11-24)

- **概要 (事実)**: hex.pm の公式ブログによると、11/23 18:16〜18:29 UTC に、第三者が 69 件の悪意あるリクエストを送った。影響を受けたのは Web サーバー 6 台。エラー追跡の Sentry が、各リクエストのエラーを記録していた。18:27 にファイアウォールで遮断し、18:30〜18:31 に全サーバーを修正済みのビルドに置き換えた。19:07 には、同じ脆弱性の報告がメールで届いた。hex.pm は、パッケージストレージへの書き込みと DB の変更、攻撃者の持続的なアクセスについて、いずれも証拠はないとしている。一方で、**DB の読み取りはログに残らない**ため、メールアドレス、パスワードハッシュ、API キーのハッシュ、2FA のシークレット、セッション、監査ログが読まれた可能性は否定できないとしている。ストレージ、CDN、メール、DB の認証情報と、セッション・アクセストークンの署名鍵は入れ替えた。これで全利用者がログアウトされた。**レジストリの署名鍵だけは入れ替えておらず**、鍵のローテーションに対応した新しい署名方式と Hex クライアントを数日中に出すとしている。それまでは、**サードパーティのミラーを信頼せず、repo.hex.pm からだけ取得する**よう求めている。スウェーデンのデータ保護当局 IMY、CISA、ENISA にも報告した。CVE は ErlEF の CNA が採番し、記録には「2026-11-23 に hex.pm に対して悪用された」と明記された。
- **技術的な中身**: 入り口は、`application/vnd.hex+erlang` 用の独自パーサー (`HexpmWeb.ErlangFormat.decode/1`) だ。このパーサーはルーティングと認証より前の endpoint で動くため、**どのルートへの POST でも、認証なしで届く**。パーサーは `Plug.Crypto.non_executable_binary_to_term/2` (`[:safe]`) で body を decode していた。この関数は関数値や新しい atom を拒否するが、**map は検査しない**。Elixir の struct の実体は「`__struct__` キーにモジュール名を持つ map」なので、攻撃者は任意のモジュールの struct を、全フィールドを好きな値にして送り込める。連鎖は次のとおり。(1) `Plug.MethodOverride` が `body_params["_method"]` を読む。struct に対して `fetch/2` を呼ぶが、その関数がないので `UndefinedFunctionError` が上がる。(2) Sentry、Bandit のエラーログ、JSON のログ整形が、引数を `inspect` する。(3) Inspect はプロトコルなので、`__struct__` で選ばれた `Ecto.Query.DynamicExpr` の実装が走る。この実装は `binding` フィールドがリストかどうかを確かめずに列挙する。(4) `binding` に入れた `DBConnection.Stream` の Enumerable 実装が `DBConnection.reduce/3` を経て、エラー処理の経路で stream の `:log` オプションを適用する。`:log` は `{module, function, args}` のタプルで、これが**リクエストから来た値のまま `apply` される**。標準ライブラリの関数を呼べるので、BEAM の実行ユーザーで OS コマンドを実行できる。修正のコミット `379b0a2` は、`__struct__` キーを持つ map を含む term を 400 で拒否する。
- **同じバグクラスの CVE (同日、水平展開済み)**: hex.pm は調査中に、Ash のキーセット型ページネーションでも同じ問題を見つけて報告した (CVE-2026-124283、ash 3.38.0 で修正)。カーソルの値に入れた struct が AshPostgres で `inspect` され、同じ Ecto → DBConnection の連鎖で OS コマンド実行になる。`%Ash.CiString{}` に入れた `Fragment` は、そのまま SQL に書き込まれる。Flop のカーソル (CVE-2026-130411) も、`:erlang.binary_to_term/2` の `:safe` で decode した値を Ecto に渡しており、同じ連鎖で RCE になる。db_connection 自体にも CVE-2026-133555 が付いた (2.10.3 で修正)。ただし、記録は「単体では悪用できない。根本の原因は、信頼できない入力を `binary_to_term` で decode する下流のコンポーネントにある」としている。hex.pm は、plug_crypto に struct を拒否するオプションを足す、plug で body params の struct を拒否する、ecto で Inspect の前に binding の型を確かめる、db_connection で stream struct の `:log` を適用しない、といった多層の強化を進めている。
- **背景・経緯 (背景引用)**: Elixir では 2020 年に、ページネーションのライブラリ paginator で、カーソルを `binary_to_term` で decode していたことによる RCE (CVE-2020-15150) が報告されている。「クライアントに返すカーソルに Erlang term を詰める」設計は、そのころから危険と知られていた。今回は、`:safe` / `non_executable_*` という「安全なはずの」API でも、**struct とプロトコルのディスパッチがガジェットになる**ことが、実際の攻撃で示された。Java の `readObject` や Ruby の `Marshal.load` と同じ「ガジェットチェーン」の考え方が、BEAM でも成り立つ。パッケージレジストリへの攻撃としては、2022 年の rubygems.org の任意の gem を yank できた欠陥 (CVE-2022-29176) などがある (背景)。
- **なぜ今これが重要か (評価)**: 第 1 に、**実際に悪用されたうえで、ガジェットの連鎖が全部公開された**。Ecto と db_connection はほぼすべての Phoenix アプリが依存しているので、ガジェットは「どこにでもある」と考えてよい。残る条件は「外部入力が `binary_to_term` に届くか」だけになる。Elixir の Web アプリの診断では、これがソースコード診断で最初に見るべき sink になった。第 2 に、hex.pm の署名鍵の入れ替えはまだ終わっていない。ミラーや社内のプロキシを経由して Hex パッケージを取る CI は、**新しい署名方式のクライアントが出るまで、取得元を見直す必要がある**。第 3 に、同じ日に 4 件の CVE が出て、修正版も揃っている。今週は、Elixir のプロジェクトで依存の更新が集中しそうだ。
- **読者が今日できること**:
  - ソースコード診断: `rg -n "binary_to_term|non_executable_binary_to_term" lib/ deps/` で sink を探す。特に、`Base.url_decode64` の直後にあるもの (カーソル、Cookie、hidden フィールド、Webhook の body) を優先する。`[:safe]` の指定があっても安全とみなさない。
  - 依存の確認: `mix deps | rg "ash |flop |db_connection "` で、ash ≥ 3.38.0、flop (0.26.7 / 0.27.3 / 0.28.1 / 0.29.2 以降)、db_connection ≥ 2.10.3 になっているか確かめる。Erlang/OTP の ssl (CVE-2026-124286、下の表) も、あわせて上げる。
  - hex.pm のアカウント: パスワードを変え、hex.pm/dashboard/security で 2FA を再設定する。CI に置いた `HEX_API_KEY` も、念のため発行し直す (ハッシュしか漏れていない可能性が高いが、否定はされていないため。これは自分の判断)。Hex のミラーを使っている CI は、当面 repo.hex.pm に向ける。
- 出典: [hex.pm Blog: Security incident on hex.pm](https://hex.pm/blog/security-incident-on-hexpm) / [ErlEF CNA: CVE-2026-129514](https://cna.erlef.org/cves/CVE-2026-129514.html) / [GHSA-9pmm-hf4r-27pg](https://github.com/hexpm/hexpm/security/advisories/GHSA-9pmm-hf4r-27pg) / [修正コミット 379b0a2](https://github.com/hexpm/hexpm/commit/379b0a29bcc95164249f38ad7d772a37a8ff9533) / [ErlEF CNA: CVE-2026-124283 (Ash)](https://cna.erlef.org/cves/CVE-2026-124283.html) / [ErlEF CNA: CVE-2026-133555 (db_connection)](https://cna.erlef.org/cves/CVE-2026-133555.html)

## AI 技術・トレンド

### [2026-11-23] Z.ai、loop transformer 構造の「GLM-5.4」を公開。重みは「安全対策を終えてから」公開予定
- **何が起きたか**: Simon Willison 氏によると、中国 Z.ai は GLM-5.4 を公開した。同社として初めて loop transformer を使ったモデルで、重みを共有する層のグループを 1 回の forward で何度も回し、パラメータ数を増やさずにネットワークを深くする。11/20 には Thinking Machines Lab の Inkling 2 Mini も、中間層をトークンごとに 3 回回す loop 構造を採用していた。GLM-5.4 の重みはまだ公開されておらず、Z.ai は「必要な安全対策を終えたあと、責任ある形で公開する」としている。Willison 氏は、Coding Plan の契約がないと API から使えなかったと書いている。
- **なぜ重要か**: 1 週間に 2 社が loop 構造を出したことで、「パラメータを増やさずに推論の質を上げる」方向が、コーディングエージェント向けの主流の 1 つになりつつある。中国の主要なラボが重みの公開を「安全対策のあと」に回したことは、Cairn や Artex のような攻撃用の基盤で GLM 系が使われている現状 (下の AI セキュリティ参照) と無関係ではないとみる。
- 出典: [Simon Willison (2026-11-23)](https://simonwillison.net/2026/Nov/23/glm-54/)

### [2026-11-24] Anthropic の株価、上場から 1 週間たたずに IPO 価格の 83 ドルを割る。一時 76 ドルまで下落
- **何が起きたか**: TechCrunch によると、Anthropic の株は 11/24 (米国時間) の昼に一時 76 ドルをつけ、前日の終値から約 12% 下がった。Nasdaq での初値は 111.50 ドルだった。同じ日に NVIDIA も 7% 超下がり、Huang 氏の CEO 復帰で上がった 30% 超の一部を失った。
- **なぜ重要か**: VC は、Anthropic の株価を「公開市場が AI 企業をどう評価するか」の指標として見ている。下落が続けば、AI スタートアップの未公開株の評価や、ほかの AI 企業の IPO に影響する。セキュリティ業界から見ると、AI ラボの資金の状況は、無償のセキュリティ研究支援 (OSS の脆弱性探索など) がどこまで続くかに関わる。
- 出典: [TechCrunch (2026-11-24)](https://techcrunch.com/2026/11/24/anthropic-shares-fall-below-ipo-price-a-worrying-sign-for-ai-startups/)

### [2026-11-24] GPT-6.2 Astra の「研究者としての」事例が続く。1808 年の作者不明のスケッチブックの作者を 22 分で特定し、アマチュア天文家は Codex と Astra で系外惑星の候補を挙げた
- **何が起きたか**: 歴史学者の Mark Humphries 氏は、GPT-6.2 Astra が少ない指示で、イェール大学の Beinecke 図書館にある 1808 年の作者不明のスケッチブックの作者を 22 分で特定したと報告した (Willison 氏が紹介)。Astra は、スケッチブックの日付の 5 日前に近くの川を訪れた vicomte de Chabot の記録を日記の中から見つけ、Chabot の旅行記 (クリーブランド州立大学に取り寄せが必要) で裏づけられると予測し、実際にそうなった。OpenAI は同じ日に、2 人のアマチュア天文家が Codex と Astra を使って公開の望遠鏡データから惑星の兆候を探し、専門家に追観測の候補を渡した事例を公開した。
- **なぜ重要か**: 「仮説を立て、検証に必要な一次資料を予測して当てる」という研究の手順を、モデルが自律的にこなした事例になる。脆弱性の調査でいえば、「どのコミットや仕様書を読めば仮説を確かめられるか」を当てる能力に近い。11/17 号で扱った Astra のシステムカードのサイバー能力の評価と合わせて見ておきたい。
- 出典: [Simon Willison (2026-11-24)](https://simonwillison.net/2026/Nov/24/astra-historical-mystery/) / [OpenAI (2026-11-24)](https://openai.com/index/searching-for-distant-planets-with-astra)

### [2026-11-24] OpenAI の事例: ブラジルの iFood、1.5 万のリポジトリにコーディングエージェントを展開。脆弱性の修正件数が 2 倍超に
- **何が起きたか**: OpenAI は iFood の「Remote Agents Platform」の事例を公開した。開発のタスクを API 呼び出しにし、エージェントがリモートのサンドボックスで作業して、結果をマージリクエストとして返す。社内の規約の検証、脆弱な依存の修正、分析などを 1.5 万のリポジトリに一括でかける。社内のセキュリティ基盤での脆弱性の修正件数は 2 倍超になったとしている。
- **なぜ重要か**: 「依存の脆弱性の修正 PR を全リポジトリに出す」作業が、エージェントの定型業務になった。11/24 号の Claude Ship (AI による承認) と合わせると、**修正 PR の作成から承認までを AI が担う組織**が出てくる。診断の観点では、サンドボックスからの外向き通信と、エージェントに渡すトークンの権限が検証の対象になる。
- 出典: [OpenAI (2026-11-24)](https://openai.com/business/customer-stories/ifood)

### [2026-11-24] Meta、AI エージェント「Muse」を Instagram の DM に組み込む
- **何が起きたか**: Instagram の利用者は、DM のスレッドで Muse と会話できるようになった。投稿や場所、商品について詳しく聞いたり、ほかの DM の会話の要約を頼んだりできる。投稿を Muse に共有して、「メキシコシティの旅程にこのカフェを加える」「ブラックフライデーの靴のセールを探す」といった操作も頼める。
- **なぜ重要か**: 11/22 号で扱った Muse の乗っ取り (悪意ある Web ページで会話の履歴を抜かれた件) と、11/24 号の Walmart の Agent Gateway (Muse が上限付きで買い物をする) に続く動きだ。**他人から届く DM と投稿という、信頼できない入力**が、購買の権限を持つエージェントに直接流れ込む構成になる。間接プロンプトインジェクションの攻撃面としては、かなり大きい。
- 出典: [TechCrunch (2026-11-24)](https://techcrunch.com/2026/11/24/meta-brings-its-muse-ai-assistant-directly-into-instagram-dms/)

### [2026-11-24] Tidal、完全に AI で生成された楽曲を 12/9 から禁止。年内に 2,900 万曲超を削除
- **何が起きたか**: TechCrunch によると、Tidal は過去 90 日にアップロードされた曲の 43% 超が AI 生成だったとして、完全に AI で作られた曲の削除を 12/9 に始める。年内に 2,900 万曲超が消え、1 日あたり 8 万〜8.5 万曲の投稿を拒否する見込み (Ars Technica の見出しは 2,700 万曲)。配信代行業者からの 100% AI の曲の納品も禁止し、メタデータで完全 AI 生成とされた曲は拒否する。AI の支援を受けた曲は引き続き受け付ける。
- **なぜ重要か**: 判定はメタデータの自己申告に頼る部分が大きく、偽って申告した曲をどう見つけるかは示されていない。下の NYT と Photoshop の件と合わせると、「AI 生成のラベル (C2PA などのメタデータ)」が、作品の扱いを左右する**事実上の通行証**になりつつある。
- 出典: [TechCrunch (2026-11-24)](https://techcrunch.com/2026/11/24/tidal-to-ban-and-remove-millions-of-ai-generated-tracks-as-ai-slop-inundates-music-streaming/) / [Ars Technica (2026-11-24)](https://arstechnica.com/ai/2026/11/tidal-will-ban-fully-ai-generated-music-on-december-9/)

### [2026-11-24] New York Times、契約フォトグラファーに Photoshop の最新版 (2027) への更新を控えるよう要請。AI 機能で「AI 生成」のメタデータが付くおそれ
- **何が起きたか**: The Verge が入手したメールによると、NYT の写真部門の責任者 2 人は、Photoshop 2027 の機能が「利用者にはわかりにくい形で」AI を使っており、写真に AI 生成と識別するメタデータが付くことがあると警告した。
- **なぜ重要か**: 報道写真では、AI 生成のラベルが付くと掲載できなくなる。ツールの更新で、利用者が知らないうちにラベルが付くことは、メタデータに基づく真正性の仕組みの弱点 (ラベルの過剰付与と、逆に除去・偽装のしやすさ) を示している。
- 出典: [The Verge (2026-11-24)](https://www.theverge.com/ai-artificial-intelligence/1041227/the-new-york-times-warns-photographers-not-to-update-photoshop-over-ai-features)

### [2026-11-24] [続報] NVIDIA の Huang 氏、社員集会で謝罪し、「トランプ大統領が復帰を後押しした」との見方を「まったく事実ではない」と否定
- **何が起きたか**: The Verge が Bloomberg、NYT などの報道をまとめた。Huang 氏は復帰後初の全社集会で社員に謝罪した。大統領自身が公に言っている「直接関与した」という説明は否定し、「政治が会社に影響したとは一瞬も思わないでほしい」と述べたという。
- **なぜ重要か**: 前回 (11/24 号) からの変化は、本人が政府の関与を否定した点だ。12/3 の上院銀行委員会での証言で、輸出管理についてどう説明するかが焦点になる。
- 出典: [The Verge (2026-11-24)](https://www.theverge.com/tech/1041571/jensen-huang-all-hands-nvidia-apology)

### [2026-11-23] Allen AI、ロボットの操作向けの点追跡モデル「RoboTrack」を公開
- **何が起きたか**: Allen Institute for AI は、Hugging Face のブログで RoboTrack を公開した。動画の 1 フレームで指定した点が、後続のフレームのどこにあるか、遮られている間はどこか、いつ再び現れるかを推定する。グリッパーが物を隠したり、視点が変わったりする現実の環境向けに作った。モデル、データ、コード、ベンチマークを公開している。
- **なぜ重要か**: フィジカル AI の基礎部品が、オープンな形で揃ってきた。ロボットの制御に使う知覚モデルが OSS になるほど、敵対的なパッチ (物理的に貼る模様) による追跡の妨害が、研究から実機の評価に移ってくるとみる。
- 出典: [Hugging Face Blog (2026-11-23)](https://huggingface.co/blog/allenai/robotrack)

### [2026-11-24] 国内: DeNA、AI エージェントを社員として配属する「AI 社員」を外販。トークンの使用量を「勤務時間」として管理し、「残業の上限」を設ける
- **何が起きたか**: ITmedia によると、DeNA は 11/20 に「AI 社員 by DeNA」の提供を発表した。AI 社員は導入企業の中で固有のアカウントを持ち、Slack などで部署の一員として働く。メンター役の社員が仕事を教え、慣れた業務は AI 社員が自分で手順をスクリプトにして自律的に実行する。動作は固有の ID にひも付いてログに残り、人と AI の操作を区別できる。権限は最小限にし、超える作業は人の承認を求める設定もできる。DeNA の社内では 30 人の AI 社員が購買、情シス、インフラ管理、営業などで働いている。会計システムのチームでは、8 営業日で 52.6 時間分の業務を担ったという。11 月から事前登録を受け付ける。
- **なぜ重要か**: 「AI に固有のアカウントと ID を与え、人と区別して監査する」設計は、エージェントの権限管理として筋がよい。一方で、AI 社員が自分で作るスクリプトの審査と、Slack 経由の指示 (プロンプトインジェクションの入口) の扱いが、導入企業の診断で論点になる。
- 出典: [ITmedia AI+ (2026-11-24)](https://www.itmedia.co.jp/aiplus/article/2611/24/2000003406/)

### [2026-11-24] 国内: 住友生命、ChatGPT Enterprise で週次利用率 80% 超。推定 ROI は全体で 203%、月 101 回以上使う層では 524%
- **何が起きたか**: ITmedia キーマンズネットによると、住友生命は 2023 年に生成 AI の活用を始めた。2025 年に 100〜150 人で ChatGPT Business を試し、2026 年 6 月に ChatGPT Enterprise に移った。Deep Research と、Word・PowerPoint・Excel との連携の広さを評価したという。
- **なぜ重要か**: 金融機関でも、全社規模の生成 AI の導入が「試験」から「定着」の段階に入った。数千人規模の展開では、社内の文書やコネクタ経由のデータに AI が触れる範囲が広がる。社内の AI 利用ルールとアクセス権の整合を確かめる仕事 (下の JSSEC のワークショップのような話) が、国内でも増えそうだ。
- 出典: [ITmedia キーマンズネット (2026-11-24)](https://kn.itmedia.co.jp/kn/article/2611/24/2000003335/)

## AI セキュリティ

### [2026-11-23] OpenAI と Cisco、パッチ前の Linux を eBPF の「シールド」で守る OSS「Shirudo」を発表。Codex が作ったシールドで、稼働中の Elasticsearch への Java4Shell の攻撃を再起動なしに止めた
- **何が起きたか**: OpenAI によると、Shirudo (日本語の「シールド」から命名) は、脆弱なコードの経路だけを eBPF で塞ぐ一時的な防御 (シールド) を、正規の通信を通したまま適用する実行環境だ。エージェントが脆弱性を調べてシールドを作り、実際の攻撃と通常の負荷で効果を検証する。どれを展開するかは運用者が承認する。シールドは暗号で署名して読み込み前に検証し、eBPF の verifier と TPM による読み込み・削除の記録で、何が適用されているかを確かめられる。管理された試験では、Codex が作ったシールドが、稼働中の Elasticsearch への Java4Shell の攻撃を再起動なしに止めたという。
- **なぜ重要か**: 「AI が見つける脆弱性の量にパッチが追いつかない」(11/23 号の「パッチ地獄」) への、AI 側からの回答になる。攻撃の観点では、カーネルに入る eBPF プログラムを AI が生成するという、**新しい高権限のサプライチェーン**ができる。署名と TPM でどこまで守れるか、シールドの回避 (同じ脆弱性に別の syscall の経路で届く) が、今後の検証のテーマになる。
- 出典: [OpenAI (2026-11-23)](https://openai.com/index/introducing-shirudo) / [SecurityWeek (2026-11-24)](https://www.securityweek.com/openai-cisco-unveil-open-source-tool-to-shield-unpatched-linux-systems/)

### [2026-11-23] Anthropic、複数のリクエストにまたがる悪用を検知する「Enterprise Frontier Safeguards (EFS)」を公開ベータに。企業のコーディングエージェントを守るガイドも公開
- **何が起きたか**: SecurityWeek によると、EFS は 9 月に発表され、100 社超の顧客 (Fortune 100 の 4 分の 1 を含む) の意見で作られた。Stripe や Salesforce が非公開ベータで評価した。従来の分類器は 1 件ずつのリクエストを見るが、EFS は「1 件ずつなら無害に見える」リクエストの連なりから、怪しいパターンを検知する。対象は、データを保持しない契約 (ZDR) で Claude を使っている組織だ。会話のデータは顧客自身のクラウドに顧客の鍵で保存し、Anthropic には監視のメタデータだけが渡る。結果は SIEM に取り込める。Claude Platform、AWS、Google Cloud で使え、Microsoft Foundry は対応中。同日に、権限の乱用、認証情報の露出、危険な依存、プロンプトインジェクション、データ持ち出しを扱う、企業のコーディングエージェントの守り方のガイドも公開した。
- **なぜ重要か**: Cairn のように「1 回の指示で後はエージェントが自律的に動く」攻撃は、1 件ずつの判定では止めにくい。EFS は、ZDR 契約の顧客でもセッション単位の監視ができるようにする仕組みで、**AI 事業者側の検知の空白**を埋める試みになる。SOC 側から見ると、AI の利用ログが SIEM の新しいデータソースになる。
- 出典: [SecurityWeek (2026-11-24)](https://www.securityweek.com/anthropic-expands-enterprise-safeguards-for-detecting-ai-misuse/)

### [2026-11-24] Unit 42、AI エージェントを使った攻撃 10 件超を分析。人間からエージェントに交代すると、コマンドの間隔の中央値が 23.9 秒から 1.4 秒に縮んだ
- **何が起きたか**: Unit 42 は、2026 年 7〜9 月に観測した 10 件超の攻撃で、攻撃者が自律型の AI エージェントを使っていたと報告した。標的は政府、物流、宿泊、製造、農業、教育。**どの攻撃も、脆弱な Web アプリに置いた Web シェルが足がかりだった**。人間が標的と初期アクセスを用意し、エージェントが偵察、認証情報の収集、権限昇格、横展開を担い、人間が「決済システムを狙え」などの方針を出す、という分担だった。ある攻撃では、エージェントは 2 日間で計 140 分だけ動き、その間に約 800 種類のコマンドを実行した。12 日間で 8,000 種類超を実行した例もある。人間による偵察の段階では、コマンドの間隔の中央値が 23.9 秒だったが、エージェントに交代すると 1.4 秒になった。痕跡として、全件で `===[Title]===` のような区切りの見出しを出力に入れていた。半数超の攻撃のスクリプトには、会話調の「推論コメント」が残っていた。失敗すると権限昇格の手法を 5 種類続けて試し、標的の上でエクスプロイトをコンパイルした例もあった。
- **なぜ重要か**: 検知の観点では、「コマンドの間隔」「出力の区切り見出し」「スクリプト内の推論コメント」が、**人間でない操作者の指紋**として使える。Web シェルが入口なのは従来どおりで、ペンテストで Web アプリの RCE やファイルアップロードの欠陥を見つける価値は、むしろ上がった。
- 出典: [Unit 42 (2026-11-24)](https://unit42.paloaltonetworks.com/autonomous-ai-agent-threat-campaigns/)

### [2026-11-24] 英国 NCSC、9 月以降に「AI を使った攻撃が著しく増えた」と警告。主に使われているのは Artex。悪用されている弱点はどれも新しくない
- **何が起きたか**: The Record と TechCrunch によると、NCSC はブログで、9 月以降、複数の業界で「エージェント型の攻撃フレームワーク」を使った侵入と停止が起きていると述べた。もとはレッドチーム向けに作られた OSS (Artex、Cairn など) が、本来の目的を超えて使われている。安価で高性能なオープンモデルや、違法な API の転売と組み合わさって、攻撃の速度、規模、粘り強さが上がり、費用は下がった。一方で、悪用されている弱点は新しいものではなく、ツールが攻撃者に新しい能力を与えているわけでもない、としている。
- **なぜ重要か**: 「AI の攻撃は基本の対策の甘さを高速に突く」という NCSC の整理は、上の Unit 42 の観測と一致する。顧客への説明としては、**既知の脆弱性の放置と弱い認証が、今までより短い時間で突かれる**、と言い換えると伝わりやすい。
- 出典: [The Record (2026-11-24)](https://therecord.media/cyberattacks-uk-artificial-intelligence) / [TechCrunch (2026-11-24)](https://techcrunch.com/2026/11/24/uk-warns-ai-driven-cyberattacks-are-exposing-years-of-weak-security/)

### [2026-11-23] Elastic、AI エージェントと LLM 基盤向けの検知ルール 143 本と、プロンプトインジェクションを判定する小型の分類器 4 種を公開
- **何が起きたか**: Elastic Security 9.6 には、AI セキュリティの検知ルールが 143 本入る。乗っ取られたコーディングエージェントによる攻撃者のコマンドの実行、悪意ある MCP サーバー、プロンプトに貼られた認証情報、jailbreak、盗んだ API キーによるモデルの無断利用などが対象だ。開発者のマシンでは、Elastic Defend がそのプロセスを止められる。別の記事では、GenAI の入出力を取り込み時に採点する 4 種の小型分類器 (プロンプトインジェクション、エンコードされたペイロード、難読化した語、拒否応答) を紹介した。GPU なしで動き、スコアの高い一部だけを LLM が再判定してから警告を出す。ルールは MITRE ATLAS と OWASP Top 10 for Agentic Applications 2026 に対応づけている。
- **なぜ重要か**: 記事が例に挙げた Nx の侵害 (AI の CLI に安全確認を外して秘密を探させた)、偽の Postmark MCP、Amazon Q 拡張の改ざんなど、過去の実例が検知ルールに落とし込まれた。レッドチームの演習では、これらのルールを避けられるかどうかが、新しい評価項目になる。
- 出典: [Elastic Security Labs (2026-11-23)](https://www.elastic.co/security-labs/blog/ai-security-detection-rules-coding-agents-mcp) / [Elastic Security Labs (2026-11-23)](https://www.elastic.co/security-labs/blog/prompt-injection-detection-ai-agents)

### [2026-11-23] arXiv: 「ツール呼び出しの密輸」。ガードと実行側で JSON の解釈が違うと、承認されたのと別の呼び出しが実行される。公式の MCP SDK 2 つでも受け付ける入力が違った
- **何が起きたか**: 論文「Oops!... I Parsed It Again」は、LLM エージェントのツール呼び出しの JSON が、事業者、ゲートウェイ、SDK、フレームワーク、ガード、実行側で何度もパースされる点に注目した。重複したキーのどちらを採るかなど、JSON の解釈の余地で**ガードが承認した呼び出しと、実行される呼び出しがずれる**攻撃 (tool-call smuggling) を定義した。6 種類の手口を示し、17 のパーサー・バリデーターの設定に同じバイト列を与える差分テストで、ほとんどの組み合わせが一部の入力で食い違うことを確かめた。公式の MCP SDK 2 つでも、受け付ける入力が違った。同じ日の別の論文「SchemaCaps」は、公開の MCP サーバー 39 個の 604 リリースを調べ、互換とされる入力スキーマの変更 580 件のうち 412 件が、ツールの権限をどこかで広げていたと報告した。調べた MCP クライアントとスキャナー 8 個のうち、スキーマが広がったツールを承認し直すものは確認できなかった。ClawHub の Agent Skill 48,682 本を調べた研究も出た。
- **なぜ重要か**: Web の世界の「HTTP リクエストスマグリング」や「パーサーの食い違い」が、エージェントのツール呼び出しで再現した形だ。診断では、**ガード (ポリシー判定) と実行が別のライブラリで JSON を読んでいる構成**を見つけたら、重複キーや Unicode のエスケープで食い違いを試す価値がある。
- 出典: [arXiv 2611.30624](http://arxiv.org/abs/2611.30624v1) / [arXiv 2611.30750 (SchemaCaps)](http://arxiv.org/abs/2611.30750v1) / [arXiv 2611.30932 (Agent Skill の供給網)](http://arxiv.org/abs/2611.30932v1)

### [2026-11-23〜24] AI 基盤の脆弱性: AutoGPT Platform の既定の JWT 鍵が公開されていて誰でも管理者になれる (CVSS 10.0)。Apache IoTDB の MCP サーバーは接続パスワードをログに平文で出していた
- **何が起きたか**: AutoGPT Platform 0.6.26〜0.7.4 は、`backend/.env.default` と `autogpt_platform/.env.default` に、公開済みの固定の JWT 検証鍵を入れて配布していた (CVE-2026-130169)。HS256 は対称鍵なので、この値を知っていれば任意の利用者や管理者の JWT を偽造できる。0.8.0 で修正された。Apache IoTDB MCP Server 0.2.0 までは、起動時に IoTDB の接続パスワードを平文でログに書いていた (CVE-2026-135747、重要度 low、0.3.0 で修正)。
- **なぜ重要か**: 11/24 号の Kerberos Agent に続き、「`.env.default` のサンプル値がそのまま本番で使われる」型の欠陥だ。AI エージェントの基盤は検証用に立てられて放置されやすい。外部の診断では、`/api` の JWT を既定の鍵で署名し直して試すだけで確かめられる。
- 出典: [NVD CVE-2026-130169](https://nvd.nist.gov/vuln/detail/CVE-2026-130169) / [GHSA-24q6-6h89-f9p7](https://github.com/Significant-Gravitas/AutoGPT/security/advisories/GHSA-24q6-6h89-f9p7) / [oss-security: CVE-2026-135747](https://seclists.org/oss-sec/2026/q4/864)

## セキュリティニュース

### [2026-11-24] VMware、悪用中の CVE-2026-123890 とは別の vCenter の認証回避 (CVE-2026-123903、CVSS 9.8) を含む 23 件を修正。ESX には VM から抜け出せる 9.8 が 2 件
- **何が起きたか**: Broadcom は、ESX、vCenter、Workstation、Fusion、Avi Load Balancer の 23 件を修正した。vCenter の CVE-2026-123903 は、VMware Directory Service (vmdir) の認証回避で、vCenter にネットワークで届く攻撃者が認証を回避できる。Broadcom は、**CVE-2026-123890 とは別の問題で、関係はない**としている。QiAnXin、depthfirst、ThreatBook の研究者がそれぞれ独立に報告した。vCenter にはほかに、アーカイブ処理の任意ファイル書き込み (CVE-2026-123904、7.5) と、vmdir の DoS 3 件 (CVE-2026-123905〜123907) などがある。ESX では、I/O フィルターサービスのヒープ領域外書き込みと use-after-free (CVE-2026-123910 / 123911、9.8) と、XHCI USB コントローラーの領域外書き込み (CVE-2026-123912、9.3、VM のローカル管理者権限が必要) が重大。ESX では VMX のサンドボックス内にとどまるが、Workstation と Fusion ではホストでのコード実行につながりうる。修正版は VCF / vSphere Foundation 9.1.2、9.0.2.0300、vCenter 8.0 U3m、VCF 5.2.5 など。Broadcom は今回の件の悪用には触れていない。
- **なぜ重要か**: 同じ vmdir で 1 週間に 2 件目の 9.8 になる。123890 は 9 月から中国系の Armory Castle に悪用されていた。**vmdir は今、複数の研究者と攻撃者がまとめて掘っている場所**とみてよい。123890 の修正 (9.1.1.0200 など) で止まっている環境は、今回の版まで上げ直す必要がある。
- 出典: [The Hacker News (2026-11-24)](https://thehackernews.com/2026/11/vmware-vcenter-hit-by-another-critical.html) / [SecurityWeek (2026-11-24)](https://www.securityweek.com/vmware-updates-patch-critical-esx-vcenter-vulnerabilities/)

### [2026-11-24] [続報] Rapid7、CVE-2026-123890 の解析を公開。TCP 2012 の DCE/RPC で、進行中の管理者ログインの SRP のセッション鍵を認証前に取り出せ、root まで到達した
- **何が起きたか**: 前回 (11/19 号) からの変化は、技術的な詳細が出たことだ。Rapid7 によると、認証前に呼べる SRP (Secure Remote Password) のセッション鍵の取得関数と、所有者を確かめない RPC のコンテキストの検索が組み合わさっている。コンテキストのハンドルは予測できる UUIDv1 で、攻撃者は**自分でログインを始め**、その前後に 2 つの参照用コンテキストを作ってタイムスタンプの範囲を絞り、隠れたログインのハンドルを当てて鍵を要求する。必要なのは TCP 2012 への到達と、既存の SSO プリンシパル名 (既定では `administrator@vsphere.local`) だけで、管理者がオンラインである必要はない。vCSA 8.0.2.00400 で再現し、ディレクトリの DB と STS の署名鍵を回収して管理者の API セッションを偽造し、アプライアンスの管理機能でアカウントを作って SSH を有効にし、root のコマンド実行まで到達した。SSO と root のパスワードは一切使っていない。
- **なぜ重要か**: 「TCP 2012 に届くか」だけが条件になったので、内部のペンテストで vCenter に 2012/tcp が開いているかを確かめる意味が大きくなった。STS の署名鍵が抜かれると、パッチ後もトークンを偽造されうる。侵害が疑われる環境では、パッチと別に STS 証明書の入れ替えが要るとみる。
- 出典: [Rapid7 (2026-11-24)](https://www.rapid7.com/blog/post/ra-rapid7-analysis-vmware-vcenter-srp-authentication-bypass-to-root-cve-2026-123890)

### [2026-11-24] GreyNoise: Check Point の管理サーバー 24 台 (22 組織、17 か国) が侵害されていた。侵害後に SmartConsole の認証回避 (CVE-2026-16232) を使い、ファイアウォールのポリシーを外していた
- **何が起きたか**: BleepingComputer によると、GreyNoise は、10/17〜11/2 に観測した活動を「GT13」と名付けた。被害組織は政府、金融、エネルギー、運輸、鉱業、製造など。攻撃は 99 個の IP (侵害された Check Point の機器と ExpressVPN の出口) から来ていた。CVE-2026-61500 で侵害した Rejetto HTTP File Server を、操作の中継と盗んだデータの集積に使っていた。最初の侵入の方法は特定できていない。侵害後に、7 月に 0-day として警告された SmartConsole の認証回避 (CVE-2026-16232) で管理者として認証していた。ファイアウォールの DB、認証情報、設定、内部 CA のファイルを盗み、セキュリティポリシーを外して保護を止め、Citrix、Ivanti、vCenter、Exchange、Netlogon の既知の欠陥で横展開を試みた。10/26 には 24 台すべてで一括の証明書操作を試みて失敗しており、これが被害組織の特定につながった。GreyNoise は、挙動と自動化の度合いから、**AI を使った攻撃ツールを使っていたと評価**しているが、確定はしていない。観測が途切れた 11/2 以降も続いている可能性があるとして、各国の CERT に通知した。
- **なぜ重要か**: ファイアウォールの管理サーバーは、侵害されると**ポリシーそのものを書き換えられる**。内部 CA のファイルを持ち出されている点から、パッチだけでなく、証明書と管理者の認証情報の入れ替えが必要になる。Check Point の管理サーバーを持つ顧客には、10/17 以降の SmartConsole のログインと証明書の操作の履歴を確かめるよう勧めたい。
- 出典: [BleepingComputer (2026-11-24)](https://www.bleepingcomputer.com/news/security/hackers-compromise-check-point-servers-in-22-organizations/) / [SecurityWeek (2026-11-24)](https://www.securityweek.com/check-point-security-management-servers-hacked-in-ai-assisted-campaign/)

### [2026-11-24] Radware、認証のない内部の Cloud WAF 管理 API がインターネットから届く状態で、顧客の連絡先と、ログ出力先 (S3 / Azure Blob / SFTP) の認証情報が読まれた可能性
- **何が起きたか**: BleepingComputer が匿名の情報源から入手した Radware の根本原因の報告書によると、11/19 に、権限のない者が、本来は内部専用の Cloud WAF の管理 API に、認証なしでアクセスした。読まれた可能性があるのは、顧客の連絡先と、一部の顧客では自前のストレージへのログ出力に設定した認証情報。Radware は 10 時間後に検知し、送信元の IP と API へのアクセスを止め、内部のアカウントの認証情報をすべて入れ替えた。WAF の検査、証明書、利用者のデータ、アプリの通信には影響がないとしている。AppSec (WAF、BOT) の顧客には、ログ出力の認証情報 (Azure Blob のキーや SAS トークン、AWS S3 のアクセスキー、SFTP) をすぐに入れ替え、11/19 以降のストレージのアクセスログを確かめるよう求めた。すでに、見知らぬ IP がログ出力用のバケットにアクセスを試みたという AWS の警告を受けた顧客がいる。Radware は公式の声明も SEC への報告も出していない。
- **なぜ重要か**: 11/24 号の Azure APIM と同じく、「**防御製品のクラウドの管理プレーン**から、顧客が預けた鍵が抜かれる」型の事故だ。WAF のログには、通過したリクエストの中身 (Cookie や認証ヘッダを含みうる) が入るので、ログ出力先のバケットが読まれると二次被害が大きい。Radware の Cloud WAF を使う顧客では、鍵の入れ替えに加え、バケットのポリシーで送信元を Radware の IP に絞っていたかを見直したい。
- 出典: [BleepingComputer (2026-11-24)](https://www.bleepingcomputer.com/news/security/radware-discloses-breach-exposing-customer-cloud-access-keys/)

### [2026-11-24] Okta: ShinyHunters 系のボイスフィッシング集団 (O-UNC-053) が、新しいリークサイト「INCEPTION」に移った。別に「ShinyHunters 復活」を名乗る Tor サイトも 11/23 に開設
- **何が起きたか**: Okta の脅威インテリジェンスによると、2026 年 3 月から追っている O-UNC-053 は、電話で標的を誘導してフィッシングページに認証情報を入れさせ、MFA を承認させる。被害データは以前は ShinyHunters のリークサイトに載っていたが、11/16 から INCEPTION という新しいサイトに載るようになった。フィッシングキットは、パスキーや Okta FastPass のようなフィッシング耐性のある方式は突破できない。10 月からは「legal-」で始まる、または「-legal」で終わる法務を装ったドメインを、攻撃の当日か前日に登録している。BleepingComputer によると、別に 11/23 に開設された Tor サイトが ShinyHunters の復活を宣言し、2020 年からの過去の PGP 鍵で署名したメッセージを載せた。鍵は本物だったが、鍵は多くの人の手に渡っており、同じ人物とは限らない。
- **なぜ重要か**: 逮捕が続いても、手口 (電話 + MFA の承認) と人員は名前を変えて残っている。ソーシャルエンジニアリングの演習では、**法務部や訴訟を装った電話**という新しいシナリオを入れる根拠になる。対策としてはパスキーへの移行が有効と、Okta 自身が示している。
- 出典: [The Hacker News (2026-11-24)](https://thehackernews.com/2026/11/okta-links-shinyhunters-associated.html) / [BleepingComputer (2026-11-24)](https://www.bleepingcomputer.com/news/security/shinyhunters-resurfaces-after-fbi-arrests-uses-old-pgp-keys-as-proof/) / [Help Net Security (2026-11-24)](https://www.helpnetsecurity.com/2026/11/24/shinyhunters-inception-leak-site-okta/)

### [2026-11-24] WHMCS のショッピングカートに認証なしの SQL インジェクション (CVE-2026-82981、CVSS 4.0 で 8.7)。顧客の記録と管理者のパスワードハッシュを読める
- **何が起きたか**: The Hacker News によると、ホスティング事業者が使う課金・自動化の基盤 WHMCS は、ショッピングカートの SQL インジェクションを公表した。ログインなしで、顧客の個人情報とサポートの情報、管理者アカウントのハッシュ化したパスワードを DB から読み出せる。ほかにログインが必要な欠陥が 2 件あり、メールキャンペーンの欠陥は CVSS 3.1 で 9.0。修正版は 9.0.10、8.13.8、9.1.2 (記事の時点で 9.1 のリリースノートに未掲載)。8.0〜8.12 系は修正の対象外で、更新が必要。メールキャンペーンの件は、更新に加えて、予定中・実行中のキャンペーンの削除とテンプレートの整理も求めている。悪用の報告はない。3 件とも同じ研究者 (alakazamspooon) が報告した。
- **なぜ重要か**: WHMCS は自前でホストする事業者が多く、更新が遅れやすい。カートのページは誰でも開けるので、Shodan などで見つかるインスタンスがそのまま対象になる。管理者のハッシュを解読されると、顧客のサーバーの管理 (cPanel などとの連携) に横展開されるおそれがある。
- 出典: [The Hacker News (2026-11-24)](https://thehackernews.com/2026/11/whmcs-sql-injection-flaw-could-expose.html)

### [2026-11-24] Check Point Research: イラン系の新しい集団「Volant Manticore」、IPFS を C2 に使うバックドア「KuboShell」でキプロスの通信・航空・重要インフラを狙う
- **何が起きたか**: Check Point によると、Volant Manticore は 2025 年 8 月末から活動している。KuboShell は IPFS で C2 をやり取りし、MuddyWater の MuddyC2Go を作り直した侵害後フレームワーク「Homa」を展開する。MeshCentral や NetLock RMM などの正規の RMM も入れ、なりすました組織のメールや社内の認証情報を集めるフィッシングも行う。Check Point は、MuddyWater と複数のつながりがあるとし、MuddyWater から分かれた元メンバーが別の集団として動いていると評価した。どちらもイラン情報省 (MOIS) 系とみている。
- **なぜ重要か**: IPFS の C2 は、ドメインや IP を止めても通信を切りにくい。外向き通信の監視で、業務で使わない IPFS のゲートウェイや Kubo のポートへの通信を拾う検知が要る。正規の RMM の悪用は、ペンテストの報告で「許可していない RMM の棚卸し」を勧める根拠になる。
- 出典: [The Hacker News (2026-11-24)](https://thehackernews.com/2026/11/iran-aligned-volant-manticore-uses-ipfs.html)

### [2026-11-24] 韓国電力公社 (KEPCO)、150 万人分の情報流出を確認。料金の基盤から、65 万人分の口座番号とカード番号も
- **何が起きたか**: BleepingComputer によると、KEPCO は 11/20 に、電気料金の閲覧・支払いの基盤「KEPCO ON」と調達システム (SRM) への不正アクセスを確認した。外部の IP からのアクセスを止め、該当サービスを停止した。11/22 (日) の発表によると、KEPCO ON の顧客 650,487 人分 (氏名、ID 情報、電話番号、住所、銀行名、口座番号、カード会社、カード番号、料金の情報)、取引先の代表者 426,827 人分、社員 442,934 人分が流出した。
- **なぜ重要か**: 重要インフラの事業者の、IT 側の顧客向けシステムが侵害された例。料金の基盤にカード番号と口座番号が一緒にあった点は、PCI DSS の観点では保存の範囲が広すぎる。電力会社を装ったフィッシングが続くとみられる。
- 出典: [BleepingComputer (2026-11-23 米国時間)](https://www.bleepingcomputer.com/news/security/south-koreas-power-giant-kepco-confirms-data-breach-impacting-15-million/) / [SecurityWeek (2026-11-24)](https://www.securityweek.com/1-5-million-impacted-by-data-breach-at-south-korean-electric-company-kepco/)

### [2026-11-24] 豪州のウラン企業 Peninsula Energy、米ワイオミング州の鉱山の「運用システム」が侵害され、株式の取引を停止
- **何が起きたか**: SecurityWeek によると、Peninsula Energy は豪州証券取引所 (ASX) に取引停止を求めた。11/20 (金) の夜にサイバー攻撃が起き、ワイオミング州の Lance Project の「運用システム」が侵害された。米国と豪州の管理系のシステムは影響を受けていない。どの技術システムが侵害されたか、生産が止まったかは明らかにしていない。米国は 2025 年にウランを重要鉱物に加えている。
- **なぜ重要か**: 「運用システム」という表現から、OT 側の侵害の可能性がある (確認はされていない)。重要鉱物の供給網は、国家系の攻撃者の関心の対象になる。続報で侵入経路が出るかを追いたい。
- 出典: [SecurityWeek (2026-11-24)](https://www.securityweek.com/peninsula-energy-halts-trading-after-cyber-incident-hits-us-uranium-mine/)

### [2026-11-24] トレーラーの Bluetooth ブレーキ制御器 (Elecbrakes) に認証なしの操作。100m 以内から、ブレーキを最大にしたり外したりできる
- **何が起きたか**: SecurityWeek によると、豪州の Element Digital は、AI の助けを借りて、Elecbrakes の EB2、VM1、ELBC 2000 に 3 件の欠陥を見つけた。認証の欠如とリプレイ攻撃への対策不足の 2 件が重大で、Bluetooth の範囲 (最大 100m) にいる攻撃者が、ノート PC やスマートフォンから、利用者の操作なしにトレーラーのブレーキをかけたり外したり、強さを変えたりできる。3 件目はファームウェアの更新の仕組みの問題 (中程度)。CISA は先週アドバイザリを出した。EB2 と VM1 は 7 月に修正され、更新後は物理的な接続による初回のペアリングが必要になった。古い ELBC 2000 は対応を検討中。
- **なぜ重要か**: IoT の診断で定番の「BLE の GATT に認証がない」がそのまま安全に直結した例。研究者が AI を使って見つけたと明記している点も、ハードウェアの診断への AI の広がりを示している。
- 出典: [SecurityWeek (2026-11-24)](https://www.securityweek.com/elecbrakes-bluetooth-vulnerabilities-expose-trailers-to-forced-braking/)

### [2026-11-24] [続報] CISA KEV に 3 件追加: Drupal Core の RCE (CVE-2026-132165)、Optimizely Web Experimentation (CVE-2026-132224)、Idunno.AntiCsrf (CVE-2026-131914)。対応期限は 3 日後の 11/27
- **何が起きたか**: 前回からの変化は、KEV に入ったことだ。Drupal Core の RCE は、事前予告の段階で「数時間から数日でエクスプロイトが出うる」と警告されていた (既報)。Optimizely は、Unit 42 が OPTIMJACK として報告した、Web Experimentation を使って顧客のサイトにスクリプトを配った件の CVE だ。Idunno.AntiCsrf は 11/24 号の深掘りの対象 (Mandiant が悪用を警告)。
- **なぜ重要か**: 3 件とも期限が 3 日しかない。KEV に載ったことで、悪用が公式に確認された。Drupal は、install.php が外から届くサイトが残っていないかを、外部の診断ですぐに確かめられる。
- 出典: [CISA KEV カタログ (2026-11-24 追加分)](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

### [2026-11-24] [続報] 欧州委員会、ARTEX が使われたとみられる攻撃で、オンライン学習の「EU Academy」から利用者の氏名とメールアドレスが流出したと確認
- **何が起きたか**: 前回からの変化は、データの流出が確認されたことだ。BleepingComputer によると、委員会の報道官は 11/23 (月) の会見で、EU Academy も侵害され、利用者の氏名とメールアドレスなどが流出したと述べた。利用者には同日に通知した。「AI を使ったツールで委員会を狙ったサイバー攻撃であることは間違いない」とも述べた。身代金の要求はなく、攻撃者は特定していない。
- **なぜ重要か**: 上の NCSC の警告が名指しした Artex による被害が、データ流出まで進んだ公的な事例になる。EU の職員と、EU の政策を学ぶ外部の利用者を狙ったフィッシングに注意が要る。
- 出典: [BleepingComputer (2026-11-24)](https://www.bleepingcomputer.com/news/security/european-commission-confirms-data-theft-in-eu-academy-breach/) / [SecurityWeek (2026-11-24)](https://www.securityweek.com/european-commission-uncovers-data-breach-in-cyberattack-investigation/)

### [2026-11-24] Turnitin、顧客向けのシステムで不正な活動を検知。米連邦議員は本人確認の事業者に、1.5 億人分の身分証の流出を受けた対策を質問
- **何が起きたか**: 剽窃・AI 文章の検出で知られる Turnitin (185 か国、1.6 万の機関、7,100 万人の学生) は、CEO の書簡で、顧客向けの一部のシステムで不正な活動を見つけたと公表した。外部の専門家と調査中で、法執行機関と規制当局に通知した。政府の身分証や機関の財務情報は、影響を受けたシステムでは扱っていないとしている。別件で、超党派の議員 6 人は、9 月の IDScan の侵害 (1.5 億人超の運転免許証などの画像が闇市場に出た) を受け、本人確認の事業者各社に、データの管理と AI を使った攻撃への備えを問う書簡を送った。Brian Krebs 氏は、この 2 か月で身分証のデータを露出させていた本人確認の事業者を 20 社超見つけたと述べた。
- **なぜ重要か**: 教育と本人確認の SaaS は、大量の個人の文書を預かる。本人確認の事業者のストレージの公開設定は、外部の診断で見つかりやすい典型的な欠陥でもある。
- 出典: [BleepingComputer (2026-11-24)](https://www.bleepingcomputer.com/news/security/turnitin-discloses-cyberattack-affecting-customer-facing-systems/) / [The Record (2026-11-24)](https://therecord.media/idscan-data-breach-warning-congressional-letter)

### [2026-11-24] 法執行: Europol などが違法 IPTV 57 サービスを摘発。GTA 6 の映像を流出させた Lapsus$ の元メンバーに禁錮 7 年 (同日に仮釈放)
- **何が起きたか**: Europol によると、11 か国の当局が違法な IPTV 57 サービスを止め、年間 730 万超の訪問がある 321 サイトを特定した。暗号資産で 2,600 万ユーロ超の取引を追跡している。英国では、Rockstar Games から GTA 6 の映像 90 本を盗んで公開した Arion Kurtaj 被告 (21) に、11/23 に禁錮 7 年が言い渡された。病院での収容期間を差し引き、同日に条件付きで釈放された。Uber と Revolut への攻撃にも関わっていた。
- **なぜ重要か**: IPTV の摘発は、マルウェア入りの違法配信アプリの供給元を減らす効果もある。Kurtaj 被告の件は、ホテルの TV の Wi-Fi と Fire Stick で再び侵入したという経緯が、内部脅威と保釈中の監督の難しさを示している。
- 出典: [BleepingComputer (2026-11-24)](https://www.bleepingcomputer.com/news/security/police-disrupt-57-illegal-streaming-services-with-73-million-visits/) / [Help Net Security (2026-11-24)](https://www.helpnetsecurity.com/2026/11/24/gta-vi-hacker-sentenced-seven-years-released-on-licence/)

### [2026-11-23〜24] 更新: Chrome 158.0.8127.88/89 が Critical の 1 件を修正。Roundcube 1.7.7 / 1.6.22 は 12 件を修正し、1.6 系は今回で最後。OpenSSL は Low 4 件を公開リポジトリで修正し、12/1 にリリース予定
- **何が起きたか**: Google は 11/23 に Chrome 158.0.8127.88 / .89 を公開し、Variations コンポーネントの入力検証の不備 (CVE-2026-134401、Critical、8/28 に Google が報告) を修正した。Roundcube は 11/23 に 1.7.7 と 1.6.22 を公開し、スペルチェックの HTTP リクエストインジェクションの再修正、HTML メールの CSS の範囲制限の回避、CSS のコメント経由の外部コンテンツの読み込み、CSS プロキシの応答の漏えい、PDF / PostScript / SVG の添付を ImageMagick に渡す処理の再修正などを行った。CVE と重要度は示していない。OpenSSL は、DANE を使うクライアントの NULL 参照 (CVE-2026-84786) など Low の 4 件 (QUIC、X.509 の CRL の処理、TLS の DANE) を公開で修正し、12/1 に新しい版を出すと予告した。
- **なぜ重要か**: Roundcube は国家系の攻撃者にたびたび狙われてきた (背景)。「以前の修正の再修正」が 2 件あるので、前回の修正の差分と見比べると、迂回の手口が読める。
- 出典: [Security NEXT (Chrome、2026-11-24)](https://www.security-next.com/193218) / [Security NEXT (Roundcube、2026-11-24)](https://www.security-next.com/193210) / [oss-security (OpenSSL、2026-11-24)](https://seclists.org/oss-sec/2026/q4/868)

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-11-23 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先
> EPSS: 下表の CVE は公開から日が浅く、FIRST の API でまだスコアが出ていない (11/25 05:00 JST 時点)。

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-129514 / GHSA-9pmm-hf4r-27pg | hexpm (hex.pm、2016-02-23〜2026-11-23 のデプロイ) | CWE-502 / 10.0 | 認証前の endpoint のパーサーが `non_executable_binary_to_term([:safe])` で body を decode → `__struct__` 付き map を通す → エラー時の `inspect` で `Ecto.Query.DynamicExpr` → `DBConnection.Stream` の `:log` の MFA が `apply` → OS コマンド実行 | [379b0a2](https://github.com/hexpm/hexpm/commit/379b0a29bcc95164249f38ad7d772a37a8ff9533) | **実悪用 (11/23、CNA 記載)** / 連鎖の詳細公開 |
| CVE-2026-124283 / GHSA-m5v6-3qwf-6w9r | ash 3.31.3 以上 3.38.0 未満 | CWE-502, CWE-89 / 8.9 | キーセット型ページネーションのカーソルを Erlang term で decode し、`Ash.Expr.expr?/1` が struct のフィールドを見ない → AshPostgres の `inspect` で上と同じ連鎖 → RCE。`%Ash.CiString{}` 内の `Fragment` は生 SQL に | [8da3fe5](https://github.com/ash-project/ash/commit/8da3fe514975ac93682f8377c5439baefaf50bad) | hex.pm の調査で発見 / ガジェット公開済み |
| CVE-2026-130411 | flop 0.8.0〜0.26.6、0.27.0〜0.27.2、0.28.0、0.29.0〜0.29.1 | CWE-502 / 9.2 | `Flop.Cursor.decode/2` が `binary_to_term(:safe)` で関数・PID などだけを拒否し map (struct) を通す → Ecto の cast 失敗時の `inspect` → DBConnection の `:log` → RCE | [4535794](https://github.com/woylie/flop/commit/4535794baa135c8cccca7bb1ada4b64c91afc81d) | 同上の水平展開 |
| CVE-2026-133555 / GHSA-gmmq-fw75-wq46 | db_connection 1.1.0 以上 2.10.3 未満 | CWE-470 / 8.9 | `DBConnection.Stream` / `PrepareStream` の Enumerable 実装が、struct 内の `:log` に入った `{m, f, a}` をそのまま `apply` → 偽造 struct を列挙させれば任意の関数呼び出し (単体では悪用不可、ガジェット) | [7b21e04](https://github.com/elixir-ecto/db_connection/commit/7b21e044e4a2f9fa0cc4b001bc6cda0ecc2ae4d2) | 上 3 件のガジェット |
| CVE-2026-124286 / GHSA-7mff-v332-665j | Erlang/OTP ssl 5.3.4〜(OTP 27.3.4.14 / 28.5.0.9 / 29.0.3 未満) | CWE-347 / 9.1 | TLS 1.2 / DTLS クライアントが、Certificate なし + 署名なしの ServerKeyExchange を「anon」と扱い `verify_signature` が true → ECDHE_RSA などで証明書検証・hostname 確認なしに `{ok, Socket}` → 経路上の攻撃者が任意のサーバーになりすまし | [74782af](https://github.com/erlang/otp/commit/74782afedd9090bad0ab1dede237a2389e94743f) | `verify_peer` 指定でも素通り / TLS 1.3 は対象外 |
| CVE-2026-123903 | VMware vCenter (9.1.2 / 9.0.2.0300 / 8.0 U3m 未満) | 認証回避 / 9.8 | vmdir へのネットワーク到達だけで認証を回避 (詳細未公表、123890 とは別の欠陥と Broadcom が明言) | (commit 不明: クローズド) [THN](https://thehackernews.com/2026/11/vmware-vcenter-hit-by-another-critical.html) | 同じ部品の 123890 が KEV・実悪用中 |
| CVE-2026-136410 / GHSA-2wmw-5fmc-m25v | Thymeleaf 3.1.6.RELEASE 未満 | CWE-917 / 9.5 | restricted expression mode でも、式オブジェクトの範囲づけが甘い → 前処理、`th:utext`、`th:on*`、フラグメント名、TEXT テンプレートに入った入力から禁止の操作 → SSTI の格上げ | (commit 不明) [advisory](https://github.com/thymeleaf/thymeleaf/security/advisories/GHSA-2wmw-5fmc-m25v) | Spring の SSTI の既存の手口と直結 |
| CVE-2026-136132 / GHSA-5h3v-3645-78xj | Pangolin 1.21.0 未満 | CWE-647 / 9.2 | `isPathAllowed()` がパスを生の `/` で分割し、パーセントデコードとドットセグメントの解決をしない → `%2F` や `..` で公開のバイパスルールに一致させ、裏のサーバーは保護パスを返す → 認証回避 | [9561d23](https://github.com/fosrl/pangolin/commit/9561d23f1e77cdea5d69db820639c0ebc62f03e1) | リバースプロキシの経路正規化の差の定番 |
| CVE-2026-130169 / GHSA-24q6-6h89-f9p7 | AutoGPT Platform 0.6.26〜0.7.4 | CWE-798 / 10.0 | `.env.default` に公開済みの HS256 の JWT 検証鍵 → 任意の利用者・管理者の JWT を偽造 → 認証・認可の回避 | (commit 不明、0.8.0 で修正) [advisory](https://github.com/Significant-Gravitas/AutoGPT/security/advisories/GHSA-24q6-6h89-f9p7) | 外から 1 リクエストで確認可 |
| CVE-2026-136411 | BusyBox 1.38.0 まで (tftpd を DIR 引数なしで起動) | CWE-36 / 9.3 | RRQ / WRQ のファイル名が `/` で始まるかを検査しない → `/etc/shadow` の読み取りや任意のファイルの上書き (多くは root) | [b67f7b7](https://github.com/mirror/busybox/commit/b67f7b7d14ac98ca84491718d364b955d21a9cd5) | 組み込み機器に広く残る |
| CVE-2026-136404 | ntop n2n supernode 3.0〜3.1.1 | CWE-121 / 9.3 | `REGISTER_SUPER_NAK` の 16 ビットの `token_size` を信頼してスタックにコピー → canary とポインタの漏えい → 戻りアドレスの上書きで RCE (未認証、任意のコミュニティに登録してから送信) | [854fbbe](https://github.com/ntop/n2n/commit/854fbbe01bbf131bf4cb88f8450d7084267668e1) | 長さフィールドの信頼の典型 |
| CVE-2026-130808 / CVE-2026-124615 / CVE-2026-129959 | Apache Karaf 4.4.12 まで | 認可不備 / important・moderate | (1) コマンドの ACL にない `feature:requirement-add/remove` を、ガードが NO_MATCH を「許可」として実行 → viewer 権限で任意のバンドルを導入・起動。(2) `sftpEnabled=true` (既定) の SFTP / SCP がロールを見ない → `etc/users.properties` や `host.key` を読み、`deploy/` に書いて RCE | (commit 不明) [oss-security](https://seclists.org/oss-sec/2026/q4/872) / [SFTP](https://seclists.org/oss-sec/2026/q4/865) | 「既定で許可」の ACL / 過去の `repo-add` の修正の取りこぼし |
| CVE-2026-132145 / GHSA-85fj-w7cw-38fv | rsyslog v8.2402.0〜v8.2610.0 の omdtls | 証明書の照合不備 / — | `tls.authmode="name"` / `"fingerprint"` でも、チェーンを検証するだけで名前や指紋に結びつけない → 同じ CA が発行した別の証明書の受信者に、転送ログを奪われる | [PR #8065](https://github.com/rsyslog/rsyslog/pull/8065) | 既定の設定では無効 |
| GHSA-j44m-77cc-p3cc (CVE-2026-63304, CVE-2026-63492) | WWBN AVideo 29.1.0 未満 | CWE-78 / High | API が FFmpeg のプロセスを探すキーワードをエスケープせずにシェルに渡す → OS コマンドインジェクション | [7559ddf](https://github.com/WWBN/AVideo/commit/7559ddf72f48684cc40ae78be9cebcaa07f5fa06) | AVideo は過去も同種の注入が多い |
| GHSA-mqwm-5m85-gmcv / GHSA-w78c-w6vf-rw82 (CVE-2026-22865, CVE-2026-22816) | Gradle 8.14.4 未満 | CWE-494, CWE-829 / High | リポジトリを無効化したつもりでも、条件によって無効化されずに解決に使われる → 意図しない取得元から悪意ある成果物を取り込む | [d38bfc0](https://github.com/gradle/gradle/commit/d38bfc0f1d4dabd38b305a67489bb8a6645138a1) / [4f2e3bb](https://github.com/gradle/gradle/commit/4f2e3bbee4d0cee307dd97b684f11cfbe711b6f3) | 依存の混同と同じ系統 |
| CVE-2026-134019 / GHSA-3r7g-mq96-7hhc | PyTables 3.11.1 まで | CWE-502 / 9.8 | HDF5 の属性で、末尾が `.` の NumPy の bytes スカラーを pickle とみなし、`AttributeSet.__getattr__` / `__getitem__` で `pickle.loads()` → 細工した HDF5 を開いて属性を読むだけで任意コード実行 | [8ae7154](https://github.com/PyTables/PyTables/commit/8ae7154191676c2ab12ba36450972d0be77efde3) | NVD は「修正版はまだない」と記載 / データセット経由の供給網 |

**今日の CVE 所感**:
- 今日の中心は **「安全な decode」が型 (struct / pickle) を通してしまう**バグクラスだ。hexpm、ash、flop が同じ連鎖で RCE になり、PyTables は HDF5 の属性から pickle に届く。Elixir では `binary_to_term` に外部入力が届く箇所 (カーソル、Cookie、Phoenix の独自パーサー、キャッシュの復元) を、ほかのライブラリ (Scrivener や Paginator の派生、独自のページネーション) にも横展開して探す価値が高い。ガジェット (Ecto + db_connection) はほぼすべての Phoenix アプリにある。
- 2 つ目は **ACL / ルールの「一致しなければ許可」**。Karaf のコマンドガードの NO_MATCH、Pangolin のパスの照合 (正規化の前に比べる)、AutoGPT の既定の鍵は、いずれも「明示的に拒否していないものは通る」設計だ。Karaf の件は、過去の `feature:repo-add` の修正で兄弟のコマンドを取りこぼした不完全な修正でもある。
- 3 つ目は **TLS の相手の確認の抜け**。Erlang/OTP ssl (署名なしの ServerKeyExchange で証明書の検証が飛ぶ) と rsyslog の omdtls (名前と指紋を照合しない) は、どちらも「`verify_peer` を設定しているから安全」という前提を崩す。11/24 号の Erlang ssl の `unknown_ca` の件に続き、Erlang/OTP の ssl は今週 2 件目になる。EMQX、RabbitMQ などの OTP 製品のクライアント側の接続 (フェデレーション、ブリッジ) が影響を受けうる。
- 診断で優先して見る製品: vCenter (9.1.2 / 9.0.2.0300 / 8.0 U3m と 2012/tcp の到達性)、WHMCS (カートのページ)、Elixir / Phoenix のアプリ (上記の sink)、Thymeleaf を使う Spring のアプリ (restricted mode に頼った SSTI 対策)。

## 日本国内のセキュリティ動向

### 国内インシデント・事故

### [2026-11-24] インフキュリオンの決済基盤「Wallet Station」に不正アクセス。鹿児島銀行「Payどん」の 25 万 1,172 件が流出し、ツルハグループの「HAPPAY」も予防的に停止
- **何が起きたか**: INTERNET Watch によると、インフキュリオンは 11/19 にシステムへの大量のアクセスを検知し、不正アクセスと利用者の個人情報の流出を確認した。第 2 報の時点で、流出は最大約 25 万件。内容は、会員情報 (氏名、生年月日、電話番号、性別、メールアドレス、パスワード)、決済手段 (口座情報、ポイント残高、地域ポイントの残高) など。11/21 の第 3 報で、緊急点検の状況と、同日からの順次の再開を説明した。Wallet Station を使う鹿児島銀行の「Payどん」は、25 万 1,172 件の流出 (取引履歴、加盟店の情報を含む) を発表した。ツルハグループのスマホ決済「HAPPAY」は、予防的にサービスを止めている。原因は調査中。
- **なぜ重要か**: 1 つの決済プラットフォームに、地域の銀行や小売の複数のウォレットが載っている構造で、**基盤 1 か所の侵害が複数のブランドに波及した**。「パスワード」が項目に入っている点は、保存の形式 (ハッシュかどうか) が明らかでなく、ほかのサービスへのリスト型攻撃に注意が要る。「大量のアクセスで検知」という経緯から、API の列挙や認可の不備の可能性もある (推測)。
- 出典: [INTERNET Watch (2026-11-24)](https://internet.watch.impress.co.jp/docs/news/2158658.html)

### [2026-11-24] 読売巨人軍、ファンクラブ「CLUB GIANTS」の会員情報の管理システムが繰り返し攻撃を受け、メールアドレス 80 万 7,030 件などが流出
- **何が起きたか**: Security NEXT によると、11/12 にサーバーの容量がひっ迫してアクセスできなくなり、調べたところ、11/13 に会員のメールアドレス 80 万 7,030 件の流出が判明した。原因を特定して攻撃を遮断し、同日に個人情報保護委員会に報告した。その後の調査で、氏名 1 万 6,998 件、住所 1 万 2,831 件、電話番号 1 万 5,434 件、性別 1,664 件、生年月日 1,665 件、ハッシュ化したパスワード 274 件の流出もわかった。不正利用の報告はない。
- **なぜ重要か**: 「容量のひっ迫」で気づいた経緯から、大量のデータの持ち出し (あるいは攻撃によるログの肥大) が起きていたとみられる。メールアドレスが 80 万件と、氏名などより桁違いに多いのは、メール配信系のテーブルがまとめて抜かれた可能性を示す (推測)。球団をかたるフィッシングに注意が要る。
- 出典: [Security NEXT (2026-11-24)](https://www.security-next.com/192864)

### [2026-11-24] ミスタードーナツのオンライン注文「ミスドネットオーダー」が侵害され、サービスを停止
- **何が起きたか**: Security NEXT によると、ダスキンは、11/15 にミスドネットオーダーへの侵害があったとして、システムを止めてアクセスを遮断し、緊急メンテナンスと調査を進めている。受け付け済みの注文は、店頭やカスタマーセンターで変更やキャンセルに応じている。被害の範囲は調査中。
- **なぜ重要か**: 11/21〜22 号のタワーレコード オンラインなど、EC・注文サイトの侵害の公表が続いている。原因と、カード情報の扱い (決済代行への遷移か、サイト内の入力か) が今後の焦点になる。
- 出典: [Security NEXT (2026-11-24)](https://www.security-next.com/193086)

### [2026-11-24] 日本マクドナルドの公式アプリの DB に不正アクセス。購入履歴、IP アドレス、端末の位置情報が露出
- **何が起きたか**: BleepingComputer によると、日本マクドナルドは 11/20 (金) の声明で、攻撃者が公式アプリの DB にアクセスしたと公表した。露出したのは、商品の購入履歴、IP アドレス、端末の位置情報、顧客管理 ID (メールアドレスや会員 ID は特定できないもの)。氏名、メールアドレス、電話番号、住所、カード情報は含まれない。検知の時期と件数は明らかにしていない。不正アクセスに使われた認証情報を無効にし、個人情報保護委員会に報告するとしている。
- **なぜ重要か**: 前回 (11/24 号) は、公表日 (11/20) が採用範囲外だったため見送った。今回は海外メディアの報道 (11/24) で取り上げる。氏名がなくても、**位置情報と購入履歴と IP の組み合わせ**は、個人の行動の特定につながりうる。「不正アクセスに使われた認証情報」という表現から、クラウドや DB の認証情報の漏えいが入口とみられる (推測)。
- 出典: [BleepingComputer (2026-11-24)](https://www.bleepingcomputer.com/news/security/mcdonalds-japan-data-breach-exposes-customer-location-information/)

### [2026-11-24] 広島県、県立高校の修学旅行の引率中に、生徒の病歴や服薬の情報を含む書類を紛失
- **何が起きたか**: Security NEXT によると、10/9 に、生徒 226 人分の氏名、性別、保護者の連絡先を記した書類と、生徒 108 人分の氏名、治療中の病気、受診歴、服薬などの情報を記した書類を紛失した。
- **なぜ重要か**: サイバーではない紛失の事故だが、要配慮個人情報 (病歴) を含む。修学旅行や校外学習での紙の持ち出しは、教育委員会のルールの見直しの対象になりやすい。
- 出典: [Security NEXT (2026-11-24)](https://www.security-next.com/192872)

### 国内の注意喚起・ガイドライン・政策

### [2026-11-24] IPA、「VMware 製品の脆弱性対策について (CVE-2026-123890)」を緊急対策情報として公開
- **何が起きたか**: IPA は、vCenter Server の VMware Directory Service の認証回避 (CVE-2026-123890) について、修正プログラムの適用を呼びかけた。Google Threat Intelligence Group が悪用を確認していることにも触れ、今後被害が広がるおそれがあるとしている。ページは、追記すべき情報があれば更新するとしている。
- **なぜ重要か**: 国内の公的機関が、悪用中の vCenter の欠陥を「重要なセキュリティ情報」として扱った。上のとおり、同じ vmdir に別の 9.8 (CVE-2026-123903) が出たので、IPA の追記で 123903 も含めて案内されるかを追いたい。国内の顧客への説明では、IPA のこのページを根拠として示しやすい。
- 出典: [IPA (2026-11-24)](https://www.ipa.go.jp/security/security-alert/2026/alert20261124.html)

### [2026-11-24] JSSEC、「第 2 回 実践 生成 AI 利用ルール策定ワークショップ」を 2027 年 1 月 13 日に開催。CC0 の利用ルールのテンプレート (18 項目) をもとに自社のルールを作る
- **何が起きたか**: ScanNetSecurity によると、日本スマートフォンセキュリティ協会 (JSSEC) は 11/16 に開催を発表した。同協会は 2026 年 4 月に「生成 AI 利用ルールテンプレート」を公開している。専門知識がない組織でも自社の実情に合ったルールを作れるようにしたもので、Excel 形式、CC0 (パブリックドメイン) で無償提供している。「AI を利用する前に」「AI に入力する」など 18 のルールからなる。
- **なぜ重要か**: 上の住友生命や DeNA のように、国内でも生成 AI とエージェントの全社展開が進んでいる。中小の組織では、ルールの整備がまだ追いついていない。CC0 のテンプレートは、診断の報告で「AI 利用の規程がない」と指摘するときに、改善の出発点として示せる。
- 出典: [ScanNetSecurity (2026-11-24)](https://scan.netsecurity.ne.jp/article/2026/11/24/56883.html)

### [2026-11-24] JPCERT/CC・JVN: Zoraxy の複数の脆弱性 (JVN#84156789) と、Siemens 製品の 11 月のアップデート情報 (JVNVU#98354779) を更新
- **何が起きたか**: JPCERT/CC の RSS は、11/24 に JVN の 2 件を配信した。新しい注意喚起 (at) は、11/20 の PHP の件の更新以降は出ていない。詳細は下の JVN の表を参照。
- **なぜ重要か**: 三連休の明けで、国内の公的機関の新しい注意喚起は少なかった。海外で悪用が続く vCenter、WHMCS、Check Point について、国内の機関から追加の注意喚起が出るかを今週は見ておきたい。
- 出典: [JVN#84156789](https://jvn.jp/jp/JVN84156789/) / [JVNVU#98354779](https://jvn.jp/vu/JVNVU98354779/)

### 国内製品の脆弱性 (JVN)

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| 2026-11-24 | JVN#84156789 / JVNDB-2026-000179 / CVE-2026-105303, CVE-2026-129544, CVE-2026-105304 | Zoraxy (リバースプロキシ・ルーティングの OSS) / Zoraxy Project (v3.3.5-rc2 で修正) | 管理画面のログビューアの格納型 XSS、セッション Cookie に HttpOnly がない、ACME チャレンジのルーティング処理の SSRF | SSRF は CVSS 3.0 で 8.6 (v4 で 7.7)、XSS 6.1、HttpOnly 5.3 / 内部ネットワークへの任意のリクエスト、管理者の Cookie の窃取 | [JVN](https://jvn.jp/jp/JVN84156789/) |
| 2026-11-05 公開 / 2026-11-24 更新 | JVNVU#98354779 | Siemens 製品 (2026 年 11 月分) | Siemens の 11 月のアドバイザリのまとめの更新 | 製品ごとに異なる | [JVN](https://jvn.jp/vu/JVNVU98354779/) |
| 2026-11-24 | JVNDB-2026-044775 / CVE-2026-123007 | NGINX (F5 等の複数ベンダの製品) | NGINX の複数の脆弱性を JVN iPedia に登録。Synology DSM の 11/20 の更新もこの CVE に対処 | CVSS 4.0 で 9.2 (IPA の 11/19 の情報) | [JVN iPedia](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-044775.html) |
| 2026-11-24 | JVNDB-2026-044776 | CISA ICS Advisory / ICS Medical Advisory (2026 年 11 月 19 日分) | CISA の ICS アドバイザリ (11/19 分) のまとめ | 製品ごとに異なる | [JVN iPedia](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-044776.html) |
| 2026-11-24 | JVNDB-2026-044626〜044670 / CVE-2026-130997〜CVE-2026-131059 | Google Chrome (158 系) | use-after-free、ヒープのオーバーフロー、境界外の読み書き、認証の欠如など、Chrome 158 で修正された 40 件超を一括登録 | 個別に異なる | [JVN iPedia (例)](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-044659.html) |
| 2026-11-24 | JVNDB-2026-044708〜044772 | Oracle (MySQL Cluster、E-Business Suite、Communications など) | Oracle の定例更新で修正されたアクセス制御・リソース枯渇などを一括登録 | 個別に異なる | [JVN iPedia (例)](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-044770.html) |
| 2026-11-24 (Security NEXT) | CVE-2026-120382 | Synology DSM / BeeStation OS | OAuth API のコマンドの引数の処理の不備 → 認証なしで任意のファイルの読み書きと DoS。修正版は DSM 7.4.1-90080 Update 2 / 7.3.2-86009 Update 6 (11/20) | CVSS 3.1 で 9.8 (Critical) | [Security NEXT](https://www.security-next.com/193243) |

> 補足: 採用範囲内に公開された国内ベンダー製品の JVN#・JVNVU# の新規の案件は、確認できた範囲では Zoraxy の 1 件だけだった (Zoraxy は海外の OSS だが、国内からの届出を JPCERT/CC が調整した JVN# の案件)。JVN iPedia の 11/24 の新規約 385 件は、ほぼ NVD 由来の海外製品 (Chrome、Microsoft、Oracle、IBM など)。Synology は国内で普及している製品として、JVN の登録前だが掲載した。

### 国内コミュニティ・研究・イベント

### [2026-11-24] piyolog、AI ペンテスト基盤「Cairn」が大学への攻撃でゼロデイを見つけた件をまとめる
- **何が起きたか**: piyolog は、Amazon Threat Intelligence の 11/20 の報告をもとに経緯をまとめた。Amazon は 9/10 に、攻撃者が認証なしで公開していた Cairn のインスタンスを見つけた。プロジェクトの設定、攻撃者のプロンプト (簡体字中国語)、AI の出力が誰でも見られる状態だった。9/8 から約 48 時間の活動が再構成でき、攻撃者は東アジア (中国本土を除く) の大学の IP の一覧と「シェルを取れ」という目標だけを与え、計画、実行、調整はエージェントが行っていた。Redis と GPU サーバーへの 2 件の作戦は失敗したという。IoC として IP 2 件が公表されている。
- **なぜ重要か**: Cairn の件は既報 (MONAI Label の CVE-2026-133968 が KEV 入り) だが、日本語で時系列と出典が整理された。上の Unit 42 や NCSC の報告と合わせて、社内や顧客への説明資料の下敷きにしやすい。
- 出典: [piyolog (2026-11-24)](https://piyolog.hatenadiary.jp/entry/2026/11/24/214547)

### [2026-11-24] Infoblox、2027 年の国内の脅威予測として「AI チャットボットによる日本向け投資詐欺の大規模化」と「AI による大規模なブランドなりすまし」を挙げる
- **何が起きたか**: INTERNET Watch によると、Infoblox Threat Intel は 11/17 に記者説明会を開いた。同社は 700 億件超の DNS のイベントと 1.2 億件の新規観測ドメインを分析しており、新規観測ドメインの 22% を悪性または不審と判定しているという。Infoblox Japan の土橋一範氏は、2027 年の日本の脅威として、AI チャットボットが日本向けの投資詐欺を大規模にし、海外の犯罪組織の参入の壁を取り払う、などを挙げた。
- **なぜ重要か**: 「日本語の壁」が AI で消えたことは、国内のフィッシングと詐欺の量に直結する。ドメインの新規登録の監視 (ブランドの類似ドメイン) は、上の Okta の「登録した当日に使う」手口に対しても有効な早期の検知になる。
- 出典: [INTERNET Watch (2026-11-24)](https://internet.watch.impress.co.jp/docs/news/2158274.html)

### [2026-11-24] ITmedia: 元米軍のセキュリティ専門家、サイバー攻撃の対象が IT から OT に広がっていると警鐘
- **何が起きたか**: ITmedia NEWS は、元米軍のセキュリティ専門家による、OT (制御システム) への攻撃の増加についての講演・取材記事を掲載した。
- **なぜ重要か**: 上の Peninsula Energy (ウラン鉱山の「運用システム」) や、Dark Reading が報じた産業用シリアルゲートウェイの露出など、今日も OT の話題が続いた。国内の製造業の顧客の OT の診断の需要は、今後も伸びるとみる。
- 出典: [ITmedia NEWS (2026-11-24)](https://www.itmedia.co.jp/news/article/2611/24/2000003408/)

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 48 (RSS / Atom 46 + NVD API + OSV の modified_id.csv 8 エコシステム + CISA KEV JSON + hex.pm Blog + oss-security の個別投稿 9 件)
- 採用件数: AI技術=12 / AIセキュリティ=7 / セキュリティ=15 / CVE=16 行 (CVE 22 件相当) / 国内インシデント=5 / 国内政策=3 / JVN=7 / 国内コミュニティ=3
- 除外理由内訳: 古すぎ=約 14 (ScanNetSecurity の 11/24 付のまとめ記事のうち、元の公表が 11/6〜11/13 のもの: ニトリ HD [11/9、最大 3,762 万件]、シェアフル [11/9、最大約 750 万件]、ロート製薬、電通デジタル TONARIWA、アットホーム、FWD 生命、第一興商、沖縄銀行 / LENDY 債権回収、マネックス証券、京成スカイライナー、IPA の PHP 事前告知 [11/19]、NGINX [11/19]、DeNA 以外の 11/20 以前の発表など) / 重複=約 20 (Claude Ship、Azure APIM、N-able、Idunno の Mandiant 記事、GL.iNet、Cairn の Amazon 報告 [Ars / Dark Reading]、Webworm、ScreenConnect、binary-parser、Xen Orchestra、タワーレコード、Gunosy、大崎電気工業、楽天証券、メルカリ / Fireworks の解説 [ITmedia 11/23]、Decart、Huang 氏の復帰の各記事、Megaspeed など) / 日付不明=2 (Dark Reading の 2 本 [本文を取得できず]、THN の .NET の 1 ビットの記事 [404])
- 取得失敗ソース: GitHub Advisories (Atom と Web 一覧が 403 → OSV の modified_id.csv と NVD の参照から GHSA を補完)、CISA の advisories RSS (XML 不正) / MSRC Blog / Google Threat Intelligence / GitHub Security Lab (RSS の解析失敗)、EPSS API (対象 CVE はスコア未算出で 0 件)、Dark Reading の個別記事 2 本 (本文が空)、WebSearch による国内の発表の検索 (該当日付の結果なし → Security NEXT / ScanNetSecurity / INTERNET Watch の一覧を直接巡回)。Talos、watchTowr、ZDI、Trail of Bits、SentinelLabs、The DFIR Report、Krebs、Embrace The Red、JPCERT/CC Eyes、トレンドマイクロ (日本) は、採用範囲内の新しい投稿なし。

</details>
