# KEDA Daily Digest — 2026-10-30 (JST)

> 採用範囲: 公開日 2026-10-28 〜 2026-10-30
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

- **最優先 (セキュリティ)**: CISA が 10/29 に KEV へ 2 件を追加し、期限はどちらも 3 日後の **11/1**。1 件は GitLab CE/EE の CI 正規表現の整数オーバーフロー (CVE-2026-97229、CVSS 10.0、フォレンジック確認の指定付き)。Alpine Linux が自社の GitLab への攻撃を公表し、「GitLab を修正版に上げても、Ruby を別に入れている構成では直らない」ことがわかった。今日の深掘りで扱う。もう 1 件は Cisco ASA / FTD の SSL VPN の DoS ゼロデイ (CVE-2026-76418、8.6) で、二次認証を設定したトンネルグループが対象。
- **セキュリティ (ほか)**: Talos が、Cisco SD-WAN コントローラーから拠点間の鍵を抜く「KeyDrift」(UAT-11473) を公開した。前号で扱った Volt Typhoon の中継網「Silent Train」の中身にあたる。VMware ESX の監査ログ回避 (CVE-2026-41709) は、Warp Panda がゼロデイとして使っていたと CrowdStrike が明かした。PHP2Shell では、Palo Alto Networks が PAN-OS 管理画面への悪用を認めた。
- **AI**: Mistral が 1T パラメータの「Mistral Large 4」の重みを公開し、サイバー防御向けと打ち出した。OpenAI は Model Spec を改訂し、ツールの出力などに含まれる指示を「既定で権限なし」と明記した。AI セキュリティでは、Symantec が、中国向けの無許可中継サービスが正規の Codex / Claude Code の設定を書き換え、サンドボックスを無効にしていた件を公表した。設定ファイルの IoC はそのまま点検に使える。
- **新規 CVE**: 「検証したもの」と「実際に使うもの」がずれる型がそろった (Echo の `%2F`、shopify_app の shop 取り違え、undici の redirect 後の cache key、Keycloak Policy Enforcer)。undici では、オプションの JSON 複製で `checkServerIdentity` が黙って消える。
- **国内**: アララのメール配信 ASP で約 301 万件のアドレスが流出し、配信 ASP の大型流出は 3 件目になった。松屋フーズとアイリスオーヤマがサイトを止め、グッドスマイルカンパニーは 40 万枚分の閲覧とスキミングの被害の内訳を公表した。JPCERT/CC は PHP2Shell の注意喚起に、ファイアウォール製品の侵害成功の痕跡を追記した。
- **まず見るべき 1〜2 件**: (1) セルフホストの GitLab は、GitLab の版に加えて **GitLab が使う Ruby の版** を確認する (期限 11/1)。(2) Cisco ASA / FTD で SSL VPN と二次認証を使っているなら、更新を優先する。

## 今日の深掘り

### GitLab CVE-2026-97229 が KEV 入り (期限 11/1)。「GitLab を更新したのに直っていない」構成がある

- **概要 (事実)**:
  - CISA は 10/29 に CVE-2026-97229 (GitLab CE/EE、CWE-190、CVSS 10.0) を KEV に登録した。期限は 11/1 で、`forensicTriage: "Yes"`。notes 欄には「同じ Ruby / Onigmo の整数オーバーフローは他の製品にも影響しうる」とあり、Ruby の告知 (10/23) へのリンクがある。
  - 前日の 10/28、Alpine Linux は、パッケージの元になる aports を置く gitlab.alpinelinux.org が 10/20〜21 にこの欠陥で攻撃されたと公表した。10/20 に新規登録したアカウントが探索を始め、10/21 に細工した CI 設定を送り、GitLab のワーカーを 8 回クラッシュさせた (うち 4 回は exploit が途中まで進んでいた)。攻撃者は Alpine の GitLab イメージを入手し、手元で exploit を調整していた形跡がある。
  - Alpine は 10/22 に 19.3.6 へ更新したが、イメージが標準の Ruby を使っていたため脆弱なままだった。サーバーを作り直し、全アカウントのパスワードをリセットした。コード実行の痕跡は見つかっていないが、否定もできないとしている。
- **技術的な中身**:
  - 欠陥の本体は GitLab ではなく、Ruby に組み込まれた正規表現エンジン Onigmo にある。GitLab の「CI/CD Regular Expression Compiler」が、CI 設定に含まれる正規表現を Ruby でコンパイルするときに整数オーバーフローが起きる。
  - Rapid7 が 10/13 に公開した PoC の経路: 公開プロジェクトのブランチに悪性の `.gitlab-ci.yml` と、非 ASCII (UTF-8) の長いファイルパスをコミットしておく → 最後の CI lint のリクエスト (GraphQL の `ciLint`) だけを未認証で送る。前段で書き込み権限が要るが、誰でもアカウントとプロジェクトを作れるサーバーでは、この条件は事実上ない。
  - GitLab の公式 Omnibus パッケージと公式イメージは、パッチを当てた Ruby を同梱している。一方、ソースからのインストールや Ruby を別に入れる自前のイメージでは、**Ruby 3.3.13 / 3.4.12 / 4.0.9 以上** への更新が別に必要。GitLab の手引きはソースインストールの最低要件を今も Ruby 3.2 としているが、3.2 は 4 月にサポートが終わり、修正は出ない。
  - Alpine によると、exploit が成功するとクラッシュも Web ログも残らない。痕跡がないことは、侵害がないことの証明にならない。
- **時系列**: 10/12 GitLab 19.4.2 / 19.3.5 / 19.2.8 公開 (当初の修正版 19.3.4 は後に「影響あり」に訂正) → 10/13 Rapid7 の PoC → 10/21 別の正規表現の欠陥 CVE-2026-110264 を直した 19.5.1 / 19.4.3 / 19.3.6 → 10/22〜23 Ruby が修正を取り込む (Ruby 側の CVE は発行なし) → 10/28 Alpine が公表 → 10/29 KEV。
- **背景・経緯 (過去の事象の引用)**: セルフホストの GitLab は、CVE-2021-22205 (ExifTool 経由の未認証 RCE) や CVE-2023-7028 (パスワードリセットによるアカウント乗っ取り) など、未認証の欠陥が大規模に悪用されてきた。CI/CD 変数、Runner のトークン、デプロイ鍵、ミラーの認証情報が集まるため、1 台の侵害がサプライチェーン全体に広がる。Alpine の事例は、ディストリビューションの上流そのものが狙われた点で、その典型になる。
- **なぜ今これが重要か (評価)**:
  - 公開から 17 日たってからの KEV 入りで、期限 3 日・フォレンジック確認の指定付き。CISA は実害を重く見ているとみられる。
  - 診断や棚卸しで「GitLab のバージョンが修正版だから問題なし」と判定すると、自前のイメージやソースインストールの構成を見落とす。今回の件の要点はここにある。
  - KEV の notes が「他の製品」に触れている。Ruby で利用者が与えた正規表現をコンパイルする Web アプリ (検索フィルタ、ルールエンジンなど) も、Ruby の版の点検対象に入る。
- **読者が今日できること**:
  - 版を 2 つとも確認する: GitLab は `/help` か `GET /api/v4/version` で 19.4.3 / 19.3.6 / 19.2.9 以上か。Ruby は、GitLab のプロセスが使う `ruby -v` (Omnibus なら `/opt/gitlab/embedded/bin/ruby -v`) が 3.3.13 / 3.4.12 / 4.0.9 以上か。
  - 露出を確かめる: 自分でアカウントを登録できる設定か、未認証で公開プロジェクトと GraphQL の `ciLint` に届くか。すぐに更新できなければ、匿名アクセスと信頼できない利用者のプロジェクト作成を止める (Rapid7 の経路を塞ぐだけの暫定策)。
  - 痕跡を探す: GitLab が公開した Sigma ルール (CI の regexp の警告、`ciLint` への異常なリクエスト、非 ASCII の長いパス、Onigmo を指す Ruby のクラッシュレポート) を当て、`/tmp` の git ユーザー所有ファイルや Puma / Sidekiq の想定外の子プロセスを調べる。疑いがあれば `gitlab-secrets.json`、Runner のトークン、CI/CD 変数、PAT、Webhook とミラーの認証情報を入れ替える。
- 出典: [CISA KEV JSON](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json) / [Alpine Linux](https://alpinelinux.org/posts/GitLab-security-incident-CVE-2026-97229.html) / [The Hacker News](https://thehackernews.com/2026/10/attacker-tried-to-exploit-alpine-linuxs.html) / [GitLab 19.4.2](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-4-2-released/) / [Ruby](https://www.ruby-lang.org/en/news/2026/10/23/regexp-fixes-for-gitlab-cves/) / [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-97229)

## AI 技術・トレンド

### [2026-10-29] Mistral、1T パラメータの「Mistral Large 4」(Le Chonk) の重みを公開。サイバー防御向けと位置づけ
- **何が起きたか**: 総パラメータ約 1T、アクティブ 49B の MoE で、コンテキストは 1M トークン、画像入力にも対応する。FP8 版と NVFP4 版を Hugging Face で公開した。ライセンスは「Mistral Ecosystem Open-Weight License」(MIT ベースで、モデルを API として提供する事業には制限あり)。Mistral によると、実在する OSS の脆弱性を再現してパッチするテスト「Artificial Analysis Cyber Index」で 82%。同等の性能とする GLM-5.3 よりタスクあたりのトークンが 47% 少ないという。
- **なぜ重要か**: Mistral は「クローズドなモデルは拒否するのでほぼ 0 点になる」と主張しており、脆弱性の再現や検証を手元の環境で行いたい診断チームの選択肢になる。一方で、サイバー系プロンプトへの拒否率は「オープンウェイトで最も高い」とも説明しており、攻撃寄りの用途でどこまで使えるかは試さないとわからない。
- 出典: [TechCrunch](https://techcrunch.com/2026/10/29/mistral-releases-weights-for-its-trillion-parameter-ai-model-targeting-cybersecurity/) / [Hugging Face Blog](https://huggingface.co/blog/mistral-large4)

### [2026-10-29] OpenAI、Model Spec を改訂。5 つの価値で構成を整理し、「信頼できないデータの指示は既定で無視」をエージェントの前提に
- **何が起きたか**: 2026-10-29 版の Model Spec は、「人の意図に忠実」「害の最小化」「正直さと透明性」「人の主体性の尊重」「配慮」の 5 つの価値で全体を組み直した。「人による監督と修正を支える」「合意した自律の範囲内で動く」などの項目が並ぶ。引用文・ファイル・ツールの出力に含まれる指示は既定で権限を持たないとし、開発者には信頼できないデータを YAML / JSON / XML で囲むよう勧めている。
- **なぜ重要か**: GPT 系のエージェントがプロンプトインジェクションをどう扱う「べき」かを示すベンダー公式の基準で、エージェント診断の評価基準として引用できる。ただし方針であり、実装がそのとおりに動く保証ではない。
- 出典: [OpenAI](https://openai.com/index/updated-model-spec) / [Model Spec 2026/10/29 版](https://model-spec.openai.com/2026-10-29.html)

### [2026-10-28] ChatGPT の Pro / Business プランに、API の利用枠 (月最大 500 ドル) が付く
- **何が起きたか**: OpenAI は、Pro (月額 100 / 200 / 500 ドル) では月額と同じ額、Business では 1 シートあたり月 20 ドル (スタンダード) または 100 ドル (プレミアム) 分の API 利用枠を付ける。1 ワークスペースの上限は月 500 ドル。ChatGPT と API のアカウントを同じメールアドレスで連携させる必要がある。Free / Go / Plus / Enterprise / Edu は対象外。
- **なぜ重要か**: 業務用の ChatGPT 契約から、管理されていない API キーが発行されやすくなる。シャドー AI の棚卸しやキー漏えいの監視で、対象に含めるアカウントが増える。
- 出典: [ITmedia AI+](https://www.itmedia.co.jp/aiplus/article/2610/29/2000002728/)

### [2026-10-28] Microsoft・Alphabet の 7〜9 月期決算: Azure は 332 億ドル (+48%) と初めて金額を公表。OpenAI 関連の売上は四半期 100 億ドル
- **何が起きたか**: Microsoft の総売上は 923 億ドルで、Azure は前年同期比 48% 増の 332 億ドル。届出書類によると、OpenAI との取引による売上 (収益分配を含む) は 100 億ドル、OpenAI への売掛金は 72 億ドル。Alphabet は Google Cloud が 307 億ドル (約 2 倍) で、売上は 25% 増えたが、AI 投資の負担で純利益は 25% 減った。
- **なぜ重要か**: Microsoft の売上の約 11% を OpenAI 関連が占め、両社の依存関係が数字で示された。クラウドの AI 需要はまだ伸びている。
- 出典: [TechCrunch (OpenAI 関連)](https://techcrunch.com/2026/10/28/microsoft-recorded-10-billion-in-revenue-from-openai/) / [TechCrunch (Azure)](https://techcrunch.com/2026/10/28/microsoft-just-shared-azures-actual-revenue-in-dollars-33-2-billion/) / [ITmedia NEWS (Alphabet)](https://www.itmedia.co.jp/news/article/2610/29/2000002693/)

### [2026-10-29] Gemini のチャット内で、Google Docs・Sheets・スライド・PDF・コードを生成し、そのまま編集できるように
- **何が起きたか**: Gemini で生成したファイルをアプリ内でプレビューし、全画面で編集できるようになった。範囲を選んで指示することもできる (表を選んで「グラフにして」など)。全ユーザーが対象で、PDF は Web とモバイル、それ以外は今のところ Web 版のみ。
- **なぜ重要か**: チャットの中で業務ファイルの作成から修正までが完結するため、情報の持ち出しやデータ管理の範囲が Workspace の外の Gemini アプリにも広がる。
- 出典: [The Verge](https://www.theverge.com/ai-artificial-intelligence/1022519/google-gemini-file-editing-documents-pdfs)

### [2026-10-29] OpenAI と提携する Thrive Holdings、警備大手 ADT を買収 (株式価値 76 億ドル、企業価値 153 億ドル)
- **何が起きたか**: Thrive Capital から分かれた Thrive Holdings が、ADT を 1 株 10 ドルで買収する。OpenAI は Thrive Holdings の出資者・提携先で、傘下企業にモデルと現場に入るエンジニアを提供している。ADT はスマートホームの警備事業の中核になるという。
- **なぜ重要か**: 物理警備・カメラ・宅内機器の大手に OpenAI 系の AI が入る。IoT や警備システムの診断で、LLM を組み込んだ機能が対象になる可能性がある。
- 出典: [TechCrunch](https://techcrunch.com/2026/10/29/openai-backed-thrive-holdings-acquires-adt/)

### [2026-10-29] Deepgram、音声エージェントの OSS「Pipecat」を開発する Daily を買収
- **何が起きたか**: Pipecat は、STT・LLM・TTS をつないで低遅延の音声エージェントを作るフレームワーク。両社は Pipecat をオープンソースのまま続けるとしている。買収額は非公表。
- **なぜ重要か**: 音声エージェントの基盤は少数の大手への集約が進んでいる。コールセンター向け AI の診断でよく出てくる構成要素になる。
- 出典: [TechCrunch](https://techcrunch.com/2026/10/29/deepgram-acquires-pipecat-maker-daily-to-bolster-its-voice-ai-infrastructure/)

### [2026-10-28] Oracle、業務アプリで AI がこなした作業量に応じて課金する「AI units」をシート課金に上乗せ
- **何が起きたか**: 投資家向け説明会で、アプリ開発担当の EVP は「AI がシステムで作業するほど AI units が消費され、シートを増やさなくても売上が増える」と説明した。エージェント実行基盤「Fusion Claw」は Fusion の外の作業も自動化するという。Oracle は 900 億ドル超の設備投資と、2030 年に売上 2,250 億ドルという目標を示している。
- **なぜ重要か**: 使った量で課金されるため、乗っ取られたエージェントやループしたエージェントがそのまま費用に跳ね返る。
- 出典: [The Register](https://www.theregister.com/applications/2026/10/29/oracle-wants-to-bill-you-for-every-ai-task-not-just-every-seat/5306403)

### [2026-10-28] Amazon、エンジニアに「トークンの消費量ではなく成果で評価する」と通知
- **何が起きたか**: VP の Terk Terkowitz 氏が社内メモを公開し、AI の利用量を開発者の評価指標にしない方針を示した。背景には AI のコストと複雑さの増加への懸念がある。日経クロステックも「AI の活用度で技術者を評価する弊害を Amazon が公式に認めた」と報じた。
- **なぜ重要か**: AI の費用対効果の議論が、利用量から成果へ移りつつある。
- 出典: [The Register](https://www.theregister.com/ai-and-ml/2026/10/28/amazon-tells-tokenmaxxing-devs-to-slow-their-ai-roll/5306090)

### [2026-10-29] エージェントが毎時本番にデプロイする開発体制の事例: ゲーム「Spawn」はトークン代が月 300 万ドル超で、人件費の 30 倍
- **何が起きたか**: Simon Willison が、Spawn の開発者 Jacob Sansbury の記事を紹介した。Fable を使うエージェントの群れが本番のコードを直接書き換え、1 時間ごとに出荷する。作業の約 60% は、本番のエラーや、ゲーム内の AI「Savi」が自分で起票したバグ報告から始まる。1 時間出荷がないことを最も重い障害 (SEV-0) として扱い、壊れた変更は 30 秒で戻せるという。
- **なぜ重要か**: 人のレビューを通さずにエージェントが本番を書き換える体制が、すでに実運用されている。ユーザーの入力がバグ報告を経て本番コードの変更につながる経路は、プロンプトインジェクションの攻撃面にもなる (評価)。
- 出典: [Simon Willison](https://simonwillison.net/2026/Oct/29/how-i-built-the-most-ai-pilled-company-in-the-world/)

### [2026-10-29] 【国内】みずほ FG、PC 上の業務を自律的にこなす AI エージェント「みずほ Cowork」を、2027 年度にもグループ約 3 万人に展開
- **何が起きたか**: 日経クロステックの取材によると、みずほ FG・みずほ銀行・みずほ信託銀行の計約 3 万人への導入を目指す。交通費精算、SNS の分析、業務監査など、決まった手順のない作業にも使う。記事のタグには「Claude Cowork」がある。
- **なぜ重要か**: メガバンクが、社員の PC を操作するエージェントを全社に入れる段階に来た。権限の範囲や監査ログの設計が、金融機関の診断の新しい確認項目になる。
- 出典: [日経クロステック](https://xtech.nikkei.com/atcl/nxt/mag/nc/18/020800017/102201515/) (有料記事。冒頭部分のみ確認)

### [2026-10-29] 【国内】KDDI アイレット、社内の AI 活用事例 113 件を無料で公開
- **何が起きたか**: Gemini や Claude を文章作成・コーディング・データ分析などに使った事例をまとめた特設サイトを公開した。エンジニア職が 63 件、それ以外が 50 件。Claude Code と Figma を組み合わせた開発の効率化や、Gemini Notebook による稟議データのチェックの支援などがある。
- **なぜ重要か**: 国内企業で AI が実際にどの業務に使われているかがわかる資料。社内ルールづくりやリスク評価の対象の洗い出しに使える。
- 出典: [ITmedia AI+](https://www.itmedia.co.jp/aiplus/article/2610/29/2000002685/)

## AI セキュリティ

### [2026-10-29] Symantec: 中国向けの無許可の中継サービスが、正規の Codex / Claude Code のサンドボックスを無効にし、全通信を自社サーバー経由にしていた
- **何が起きたか**: 利用者が `npm install -g @openai/codex` や `@anthropic-ai/claude-code` を実行した数分〜30 分後に、似せたドメイン (例: `vibe.aiok[.]me`) からファイルレスのスクリプト (`iwr | iex` や `curl | bash`) が実行されていた。スクリプトは `~/.codex/config.toml` と `~/.claude/settings.json` の接続先 (`base_url` / `ANTHROPIC_BASE_URL`) と API キーを中継側のものに差し替え、`sandbox_mode = "danger-full-access"`、`network_access = "true"`、`DISABLE_TELEMETRY=1`、`DISABLE_ERROR_REPORTING=1` を設定する。ある端末では `claude /logout` を実行して認証し直させていた。2026 年初めから、中国本土を中心に、韓国・台湾・マレーシア系の企業を含む 12 組織 (半導体・製薬・石油化学など) で確認された。中継のバックエンドは少なくとも 8 つのドメインを渡り歩いている。
- **なぜ重要か**: Symantec によると、運営者が悪用した証拠はまだない。それでも運営者はすべてのプロンプト・ファイル・秘密情報を読め、応答を偽造してサンドボックスのない状態でコマンドを実行させられる。中国拠点の端末の点検に、設定ファイルの値をそのまま IoC として使える。
- 出典: [Symantec (security.com)](https://www.security.com/threat-intelligence/openai-claude-unauthorized-relays) / [Dark Reading](https://www.darkreading.com/threat-intelligence/ai-relay-service-openai-codex-claude-code-sandboxes)

### [2026-10-28] Cequence: 1 つの攻撃者が約 32 種の AI ボット (ChatGPT・Claude・Perplexity など) を名乗り、`.env` や SSH 鍵などを探索
- **何が起きたか**: 大手クラウドから、約 90 のパス (`.env`、クラウドの認証情報、SSH の秘密鍵など) を、1 IP あたり約 8 秒で 50〜190 件要求していた。使った IP は 1 日で 300 超、1 週間で約 400。少なくとも 9 月下旬から 10 月下旬まで続き、ある日には「AI ボットの通信を受けた Cequence 顧客の 48%」に到達した。複数の組織で、「AI ボットの通信」と分類されたものの 80% 超がこの攻撃者だった。
- **なぜ重要か**: User-Agent で AI クローラーを許可する WAF の設定は、そのまま回避される。公開 IP 範囲や署名付きリクエストで確かめる必要がある。Web 診断では、秘密情報ファイルの露出を AI ボットの UA でも確認する価値がある。
- 出典: [Cequence](https://www.cequence.ai/blog/ai-agent-impersonation) / [Dark Reading](https://www.darkreading.com/cyber-risk/attacker-impersonates-ai-bots-scans-credentials)

### [2026-10-28〜29] Gitee の公開リポジトリに、まだ有効な認証情報が 2 万 6,400 件。Alibaba Cloud の AccessKey 9,473 件、DeepSeek 3,170 件、OpenAI 1,348 件
- **何が起きたか**: 研究者の Ben Zimmermann 氏が、Gitee の公開リポジトリ 725 万件の全コミット履歴を TruffleHog と Kingfisher で調べ、実際に使えることを確かめたものだけを数えた。ほかに YouTube の API キー 3,805 件、Zhipu BigModel 1,489 件、ある大手エンタープライズ AI 基盤の組織管理者の認証情報 1 件があった。12,242 件は 2025 年のコミット。ベンダーには報告したが、公開時点で失効は確認できていない。
- **なぜ重要か**: AI の API キーが、クラウドの鍵と並ぶ規模で漏れている。OSINT やペンテストでは、GitHub に加えて Gitee の全履歴も調べる対象に入る。履歴から消してもキーは失効しない。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/26400-valid-cloud-and-ai-credentials.html)

### [2026-10-29] Microsoft: 北朝鮮の攻撃者の AI 活用を段階評価。Onyx Sleet と Pearl Sleet はエージェント型ペンテスト基盤「ARTEX」を使っている
- **何が起きたか**: Jade Sleet・Coral Sleet・Jasper Sleet は AI を業務全体に組み込んだ段階 (operationalized)、Diamond / Onyx / Pearl / Sapphire Sleet はその手前 (accelerating) と評価された。Jade Sleet は 2026 年 6/8〜12 の 1 週間に 3 つの偽装企業で採用を装う攻撃を行った。Onyx Sleet は相手に合わせたおとりの文面を数分で数十件作り、Coral Sleet は非公開リポジトリにトロイの木馬を仕込む機能を短期間で作った。Microsoft は、いずれも人が指示しており完全な自律攻撃ではないとしている。
- **なぜ重要か**: 10/28 の 123 Reg の件に続き、ARTEX の悪用が国家の攻撃者でも確認された。採用を装う攻撃や偽の求職者への対策は、AI で量が増える前提で見直す必要がある。
- 出典: [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/10/29/tracking-ai-adoption-in-north-korean-threat-actor-tradecraft/)

### [2026-10-28] LangGraph で 3 件: JS / TS のカスタム認証で他ユーザーの Store を読み書きできる (CVE-2026-118668) ほか
- **何が起きたか**:
  - CVE-2026-118668 (GHSA-4hm6-w6qq-w73v、PR:L、C:H / I:H): `langgraph-api` 0.1.2 以上 0.15.0 未満。JS / TS のカスタム認証ハンドラーが名前空間を書き換えても、その結果が Store の操作に反映されず、一般ユーザーが他ユーザーの Store を読み書き・削除できる。Python のハンドラーは影響なし。
  - CVE-2026-118667 (GHSA-3fx2-cqw9-xr3c): `langgraph-sdk` 0.4.0〜0.4.5 の v3 ストリーミングが `thread_id` / `assistant_id` を URL エンコードせずにパスへ埋め込み、`../` で認証ヘッダー付きのまま同じサーバーの別パスに GET を送れる。
  - CVE-2026-115885 (GHSA-8prr-f582-jqq3): `langgraph-cli` 0.4.15〜0.4.31 の `langgraph deploy --verbose` が、レジストリ用の一時トークン (最大 12 時間有効) を出力していた。
- **なぜ重要か**: 118668 は、マルチテナントのエージェント基盤によくある「名前空間の書き換えで認可する」実装の欠陥で、同型を他製品で探す起点になる。118667 は、エージェントの ID に外部入力をそのまま渡す設計の危険を示す。
- 出典: [GHSA-4hm6-w6qq-w73v](https://github.com/advisories/GHSA-4hm6-w6qq-w73v) / [GHSA-3fx2-cqw9-xr3c](https://github.com/advisories/GHSA-3fx2-cqw9-xr3c) / [GHSA-8prr-f582-jqq3](https://github.com/advisories/GHSA-8prr-f582-jqq3)

### [2026-10-29] MCP サーバーとチャットボットの GHSA 2 件: `MCP_API_KEY` を設定しても認証が効かない pdf-reader-mcp (CVE-2026-62264) と、volto-chatbot の未認証プロキシ
- **何が起きたか**:
  - `@sylphx/pdf-reader-mcp` 2.2.0 以上 3.0.1 未満 (CVE-2026-62264、CVSS 7.5): HTTP トランスポートで起動すると「API key authentication enabled」と出力するのに、`X-API-Key` を検証していなかった。既定で `0.0.0.0` で待ち受けるため、誰でもホスト上の PDF を読めた。URL 指定の機能による限定的な SSRF もある。3.0.1 で修正され、既定の待ち受けも 127.0.0.1 になった。
  - `@eeacms/volto-chatbot` 2.0.4 未満 (GHSA-w9x9-j56r-h98r、CVE なし、CVSS 8.2): `**/_v1_da/**` へのリクエストを認証なしで受け、サーバー側の `DANSWER_API_KEY` を付けて Danswer の API に中継する。管理用 API も呼べる (confused deputy)。
- **なぜ重要か**: どちらも「認証を設定したつもりで効いていない」型。診断では、ログやドキュメントの表示を信じず、キーなしのリクエストで実際に確かめる必要がある。
- 出典: [GHSA-q344-5v34-gm84](https://github.com/advisories/GHSA-q344-5v34-gm84) / [GHSA-w9x9-j56r-h98r](https://github.com/advisories/GHSA-w9x9-j56r-h98r)

### [2026-10-28] arXiv「Penny for Your Prompts」: AI チャットサービス 42 件のうち 9 件で、プロンプトの原文が外部トラッカーに送られていた (arXiv 2610.37467)
- **何が起きたか**: 汎用と医療・法律・教育向けの AI チャットサービス 42 件の Web 画面を、JavaScript エンジンのレベルで計測し、どの操作と DOM の取得がどのデータ送信を起こしたかまで追跡した。21 件が会話のタイトルを、9 件がプロンプトの原文を、外部の解析・広告・セッションリプレイのスクリプトに送っていた。メールアドレスを送るサービスも多く、会話と個人を結び付けられる状態だった。
- **なぜ重要か**: LLM ではなく、Web 画面に埋め込んだ外部スクリプトから会話が漏れるという従来型の Web の問題。チャットボットの診断では、セッションリプレイ系 SDK が入力欄の DOM を取得していないかを確認したい。
- 出典: [arXiv 2610.37467](https://arxiv.org/abs/2610.37467)

### [2026-10-28〜29] [続報] Downloads フォルダの AGENTS.md による乗っ取り: 第三者の追試では 80 回中 0 回の成功
- **前回から何が変わったか**: 10/28 に第三者 (Chris Johnson 氏) が、Codex 0.160.1 と Claude Code 2.1.296 で、既定のモードと制限の強いモードを各 20 回、計 80 回試し、無害な目印の実行は 0 回だったと公表した。どちらのエージェントも指示ファイルを攻撃と見抜いて拒否した。追試者は Forever Security の結果を誤りとはしておらず、版の違いや、承認とサンドボックスを外した起動をしていないことを要因に挙げている。piyolog のまとめ (国内コミュニティ欄を参照) と ITmedia AI+ (10/28) も国内で報じた。
- **なぜ重要か**: 成功率は試験条件で大きく変わる。社内周知では「Downloads でエージェントを起動しない」「想定外の `[mcp_servers.*]` や `ANTHROPIC_BASE_URL` を点検する」という対策を軸にし、成功率は条件付きの数字として扱うのが妥当 (評価)。
- 出典: [piyolog](https://piyolog.hatenadiary.jp/entry/2026/10/29/170430) / [ITmedia AI+](https://www.itmedia.co.jp/aiplus/article/2610/28/2000002671/)

## セキュリティニュース

### [2026-10-29] CISA KEV に 2 件追加: GitLab の RCE (CVE-2026-97229) と Cisco ASA / FTD の SSL VPN ゼロデイ (CVE-2026-76418)。どちらも期限は 11/1
- **何が起きたか**: KEV JSON (catalogVersion 2026.10.29) で、10/29 に次の 2 件が追加された。GitLab CE/EE の CVE-2026-97229 (CWE-190) は forensicTriage が「Yes」。Cisco Secure Firewall ASA / FTD の CVE-2026-76418 (CWE-690) は、未認証のリモート攻撃者が機器を再起動させられる DoS で、forensicTriage は「No」。knownRansomwareCampaignUse はどちらも「Unknown」。
- **なぜ重要か**: 期限が 3 日と短い。GitLab は今日の深掘りを参照。
- **悪用 / PoC**: CISA が悪用を確認。GitLab は Rapid7 の PoC が 10/13 から公開されている。Alpine Linux は自社の GitLab が 10/20〜21 に攻撃されたと 10/28 に公表した。
- 出典: [CISA KEV JSON](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json) / [Alpine Linux](https://alpinelinux.org/posts/GitLab-security-incident-CVE-2026-97229.html)

### [2026-10-29] Cisco ASA / FTD の SSL VPN に悪用中のゼロデイ (CVE-2026-76418、CVSS 8.6)。二次認証を設定したトンネルグループで、未認証のまま機器を再起動させられる
- **何が起きたか**: Cisco は 10/28 (米国時間) に修正版を公開した (cisco-sa-asaftd-tunnel-dos-s6mgkb75)。トンネルグループに二次認証 (secondary authentication) を設定したときの論理エラーで、SSL リモートアクセス VPN への細工した接続要求により機器が再起動する。VPN へのログインに成功していなくても処理経路に到達する。条件は `webvpn` を設定して SSL VPN を有効にし、影響するトンネルグループで二次認証を使っていること。PSIRT は TAC のサポートケースをきっかけに 10 月に悪用を把握した。
- **なぜ重要か**: ASA / FTD の DoS ゼロデイは 8 月の CVE-2026-20349 に続いて今年 2 件目。ArcaneDoor (2024〜2025 年) では、再起動がログ消去や永続化と組み合わされた前例があり、DoS だけとみて後回しにしないほうがよい (評価)。Shadowserver は、インターネットに公開された ASA の SSL VPN を 5.1 万台超観測している。
- **悪用 / PoC**: Cisco が悪用を確認。公開 PoC はない。回避策はなく、緩和策は「DefaultWEBVPNGroup などで二次認証を外す」「トンネルグループの一覧表示をやめる」。Cisco 自身は更新を推奨している。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/cisco-warns-of-firewall-zero-day-exploited-to-crash-ssl-vpn-devices/) / [SecurityWeek](https://www.securityweek.com/attackers-exploit-second-cisco-firewall-vpn-zero-day-since-august/) / [The Hacker News](https://thehackernews.com/2026/10/cisco-patches-actively-exploited-asa.html)

### [2026-10-28] Talos、Cisco SD-WAN コントローラーに潜伏して拠点間の暗号鍵を抜く「KeyDrift」を公開。APT「UAT-11473」は Volt Typhoon の Silent Train と重なる
- **何が起きたか**: Talos によると、UAT-11473 は Catalyst SD-WAN Controller の認証バイパス CVE-2026-20127 (CVSS 10.0、2 月に修正済み) で侵入し、独自フレームワーク KeyDrift を仕込んだ。部品は 2 つ。
  - **PolyFlame**: runit のサービススクリプト (sshd / aaamgr) を改ざんして起動し、`vdaemon` に注入される。TinyShell 系のバックドアと中継用 C2 を兼ねる。
  - **LittleFilch**: `vdaemon` の `SSL_read` をフックし、復号後の制御メッセージから、指定したエッジルーターの IP と 32 バイトの鍵 (Talos は AES-256 とみる) を抜き、RSA で暗号化して UDP で送り出す。
  - 標的は宇宙・衛星、防衛・航空宇宙、政策研究。Talos は活動を「過去のもの」としているが、時期や鍵の持ち出しの有無は明らかにしていない。
- **なぜ重要か**: コントローラーを取られると、配下の全拠点の通信の鍵が漏れ、データプレーンの盗聴につながりうる (評価)。KeyDrift は定期的なビーコンを持たず、制御プレーンの通信の中で指令を受けるため、ネットワーク監視で見つけにくい。前号の Silent Train (Lumen) の具体的な中身が初めて示された。
- **悪用 / PoC**: 悪用を確認 (修正済みの脆弱性)。Snort SID 65938 / 65958。調べる観点は、runit の run スクリプトの改変、`/rootfs.rw` を実行可能で再マウントした形跡、`/tmp/system-vdaemon`、`vdaemon` に読み込まれた `libdssl.so`。
- 出典: [Cisco Talos](https://blog.talosintelligence.com/uat-11473-keydrift/) / [The Hacker News](https://thehackernews.com/2026/10/hackers-exploited-cisco-sd-wan-flaw-to.html) / [BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-exploit-cisco-sd-wan-flaw-to-deploy-custom-keydrift-malware/)

### [2026-10-29] [続報] VMware ESX の監査ログ回避 (CVE-2026-41709) は、中国系の Warp Panda が米国の法律事務所への攻撃でゼロデイとして使っていた (CrowdStrike)
- **前回から何が変わったか**: 前号では 10/28 の KEV 追加だけを扱った。CrowdStrike の「2026 Legal Threat Landscape Report」で、Warp Panda (別名 Armory Castle / 旧 UNC5221、Clay Typhoon、VerdantBamboo) が 2026 年初めにこの欠陥をゼロデイとして使い、監査証跡を減らしていたことがわかった。手口は、エッジ機器を突破 → vCenter に移る → BRICKSTORM や SharpStorm を置く、というもの。クラウドでは M365 のセッショントークンを盗み、偽の MFA デバイスを登録して居座る。
- **なぜ重要か**: CVSS 2.7 の欠陥が、BRICKSTORM 系の長期潜伏と組み合わされていた。ESXi の侵害調査では、ホストの監査ログが完全だと仮定せず、vCenter 側のログやネットワークの記録と突き合わせる必要がある。修正版は ESXi 8.0U3j、9.0.2.0100、9.1.0.0 など。
- **悪用 / PoC**: ゼロデイとしての悪用を確認。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/china-linked-hackers-exploited-vmware.html) / [SecurityWeek](https://www.securityweek.com/chinese-hackers-quietly-used-low-severity-esxi-logging-flaw-as-zero-day/)

### [2026-10-28〜29] [続報] PHP2Shell: Palo Alto Networks が PAN-OS の管理画面への悪用を確認。GreyNoise は侵害の成立を少なくとも 6 件観測
- **前回から何が変わったか**:
  - **Palo Alto Networks** (10/28): CVE-2026-109618 のアドバイザリに「インターネットに公開された管理画面への悪用を観測」と追記した。影響は管理用の Web UI と XML API で、データプレーンのインターフェースは管理プロファイルを付けた場合だけ。12.1.4-h13 / 12.1.10-h3 / 11.2.4-h23 / 11.1.7-h12 などのホットフィックスは 10/29〜30 に提供予定とされた。
  - **The Record**: Dream の報告では、24 台のファイアウォールのうち 22 台には Web シェルを置いただけで、政府関連の 2 台に攻撃を集中させた。THN は PAN の発表と時期が合うと指摘しているが、Dream はベンダー名を公表しておらず推測の域にとどまる。
  - **GreyNoise**: 侵害の成立を少なくとも 6 件確認。**Wordfence** (10/28 時点): 保護する 500 万サイトで探索は続くが、WordPress の侵害は確認していない。
- **なぜ重要か**: 公開 PoC はそのままでは動かないことが多く、実際の侵害は機器ごとに作り込んだ exploit で起きている。PAN-OS の管理画面をインターネットに公開しているなら最優先で閉じる。
- **悪用 / PoC**: 悪用を確認 (独自の exploit)。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/attackers-exploit-php2shell-flaws-in.html) / [Palo Alto Networks](https://security.paloaltonetworks.com/CVE-2026-109618) / [The Record](https://therecord.media/php2shell-successful-exploitation-reports-emerge) / [THN ThreatsDay](https://thehackernews.com/2026/10/threatsday-critical-firewall-flaws.html)

### [2026-10-29] [続報] Linux カーネルの TCP の UAF (CVE-2026-98432、カーネル CNA の評価は 9.8): Ubuntu と RHEL はまだ修正版を出していない
- **前回から何が変わったか**: 前号では Anthropic の発表 (MPTCP を待ち受けるサーバーで、未認証のリモートから root) の一部として扱った。THN が 10/29 時点の各ディストリビューションの状況をまとめた。
  - **修正版なし**: Ubuntu (22.04 / 24.04 / 26.04 / 26.10 は対応中、16.04〜20.04 は脆弱)、RHEL 8 / 9 / 10 と OpenShift 4 (「将来の更新に延期」)。
  - **修正済み**: Debian (DSA-6568-1 ほか)、Oracle UEK (ELSA-2026-500397〜500399)、Amazon Linux 2023、openSUSE Leap 16.0。
  - ベンダーのスコアは 5.9〜8.1。バグは、IPv4 の TCP ハンドシェイクで要求の IP オプションをコピーせずに新しいソケットへ渡すことによる競合で、IPv6 は影響なし。Linux 4.4 で入り込み、本流の修正は 10/5。
- **なぜ重要か**: CVE の記録にも修正コミットにも MPTCP の記述はなく、到達条件の根拠は Anthropic の主張だけ。`ss -M` などで MPTCP の待ち受けを確かめ、カーネルの版と突き合わせたい。
- **悪用 / PoC**: 悪用の報告なし。exploit は公開されていない。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/linux-kernel-tcp-flaw-with-98-cvss.html)

### [2026-10-29] Telegram for Android、音声通話に出るだけで端末を乗っ取られる連鎖の一部になる欠陥 (12.10.4 で修正、CVE なし)
- **何が起きたか**: NebuSec が公開した。通話の状態を伝える MediaState メッセージの処理 (共有ライブラリ tgcalls) で範囲外アクセスが起きる。情報漏えいのバグと Android の root exploit を組み合わせると、通話をかけて相手が出るだけで端末を掌握できる。影響は 8.6.2〜12.10.3 (2022 年 3 月〜2026 年 9 月)。Telegram は RCE にはつながらないと判断し、CVE は採番されず報奨金も払われていない。
- **なぜ重要か**: 必要な操作が「通話に出る」だけで、スパイウェア業者に狙われやすい種類のバグ (評価)。修正は iOS 版 (12.7) とデスクトップ版 (7.0.1) には数か月前に入っていたが、Android 版は 9 月まで入らず、パッチ差分から n-day を見つけやすい状態が続いていた。
- **悪用 / PoC**: 悪用は未確認。攻撃動画のみ公開でコードは非公開。対策は 12.10.4 以上への更新か、通話できる相手を「なし」にすること。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/telegram-android-flaw-lets-attackers.html)

### [2026-10-29] 攻撃者が GitHub の issue に HTML コメントでコマンドを隠し、脆弱な Actions のワークフローに実行させる。43 分で 61 リポジトリに 83 件 (Radware)
- **何が起きたか**: The Register の独占記事によると、Radware は、issue / PR / コメントの HTML コメントに隠したコマンドを、脆弱な GitHub Actions のワークフローがシェルで実行する手口を見つけた。74 アカウントから、Google LangExtract、Trivy、Brave、MLflow などを含む 61 リポジトリに 83 件が送られ、うち 77 件は 9/1 の 43 分間に集中していた。プロンプトインジェクションの調査中に見つかった。
- **なぜ重要か**: issue 本文などの外部入力を `${{ }}` でシェルに展開する Actions のワークフローは、昔からある注入の型。画面には表示されない HTML コメントが使われており、人の目視では気づきにくい。自社やクライアントの OSS リポジトリのワークフローを、issue / comment トリガーの観点で点検したい (評価)。
- **悪用 / PoC**: 実際の攻撃を観測。
- 出典: [The Register](https://www.theregister.com/security/2026/10/29/attackers-turn-github-issues-into-supply-chain-campaign-against-61-public-repos-in-less-than-an-hour/5306153)

### [2026-10-29] サプライチェーン対策: GitHub が、インストール時に悪性の npm パッケージを止める「package firewall」をプレビュー公開
- **何が起きたか**: GitHub Enterprise Cloud の全顧客にパブリックプレビューとして提供された。開発端末・CI・コーディングエージェントと上流のレジストリの間に入り、次のポリシーで検査する: Advisory Database で悪性と判定済みのパッケージ / 指定した深刻度以上の脆弱性がある版 (既定は Critical のみ) / 以前の版にあった SLSA アテステーションがなくなった版 / preinstall・postinstall を新しく追加した版 / 公開から間もない版 (クールダウン)。
- **なぜ重要か**: 直近の npm ワーム (testmetest など) は install スクリプトやトークンを使って広がっており、その入口をポリシーで閉じられる。ただし対応は npm だけで、PyPI などには別の対策が要る。
- **悪用 / PoC**: 該当なし (防御機能)。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/github-launches-npm-firewall-to-block.html)

### [2026-10-29] Chrome 拡張機能 319 本 (合計 1,340 万インストール) が検索を乗っ取り、Bing / Yahoo の紹介料を稼いでいた (Socket)
- **何が起きたか**: Socket の John Tuckner 氏が、2025 年 4 月に報告した 57 本に 264 本を加えて公表した。拡張は PDF 変換や AI 検索などを装い、Chrome Web Store では「非公開 (unlisted)」にして怪しい広告から誘導していた。多くは `chrome_settings_overrides` で既定の検索エンジンを差し替えるだけで、マニフェストとアイコンしかなく権限も要求しないものもあった。
- **なぜ重要か**: コードも権限もない拡張は、静的な審査や権限ベースの検出をすり抜ける。中継先は拡張を更新せずに変えられ、いつでもフィッシングやマルウェア配布に切り替えられる (Socket の指摘)。企業では拡張の許可リストと、検索エンジンの差し替えを禁じるポリシーで防げる。
- **悪用 / PoC**: 実際に配布・利用されていた。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/chrome-extensions-with-134-million-installs-caught-hijacking-searches/)

### [2026-10-29] 米国土安全保障省 (DHS) の職員と委託先 4.1 万人分のデータが流出。各アカウントが使えるシステムの一覧まで含まれる (「Icepick」)
- **何が起きたか**: 「Department of Peace」を名乗るハクティビストが、DHS の職員と委託先の 4.1 万件超のデータを公開した。氏名、業務用のメールと電話、役職、勤務先、各アカウントがアクセスできるシステムやアプリの記録を含む。大半は CBP、ICE、HSI の職員で、CISA の職員約 1,000 人も含まれる。犯行側は「DHS が使う Okta の SSO から取った」と主張し、Okta は「自社が侵害された証拠はない」としている。
- **なぜ重要か**: 権限の対応表が漏れると、攻撃者は「誰を狙えばどのシステムに届くか」がわかり、標的型フィッシングの精度が上がる (評価)。主張が本当なら、IdP のディレクトリ情報やアプリ割り当てを読める権限の管理が問われる。
- **悪用 / PoC**: 流出データは公開済み。侵入経路は未確認。
- 出典: [SecurityWeek](https://www.securityweek.com/over-41000-dhs-employee-records-leaked-online/) / [Help Net Security](https://www.helpnetsecurity.com/2026/10/29/icepick-dhs-leak-ice-undercover-agents/)

### [2026-10-29] 米連邦破産裁判所の通知システム (BNC) がサイバー攻撃から復旧。運用する BAE Systems は「データの持ち出しはない」
- **何が起きたか**: BAE Systems が運用する Bankruptcy Noticing Center は、全米の連邦破産裁判所の通知を作って送る仕組み。サイバー攻撃で約 2 週間止まり、裁判所は「破産規則上の緊急事態」を 90 日間宣言していた。BAE は「ほかのシステムへの影響も PII の漏えいもない」としている。犯行声明は出ていない。
- **なぜ重要か**: 委託先 1 社の停止で、司法手続きの期限まで動かす必要が生じた。委託先への依存の大きさを示す例。侵入経路は未公表。
- **悪用 / PoC**: 該当なし (インシデント)。
- 出典: [The Record](https://therecord.media/us-bankruptcy-courts-it-contractor-says-no-data-stolen-cyberattack) / [SecurityWeek](https://www.securityweek.com/bae-says-no-data-extracted-in-incident-hitting-bankruptcy-courts/)

### [2026-10-28〜29] ベルギー財務省 (FPS Finance) がサイバー攻撃を受け、税務ポータル「MyMinfin」を停止。10/31 の申告期限は延長
- **何が起きたか**: FPS Finance は 10/28 に攻撃を公表し、予防措置として MyMinfin を止めた。現時点で「データ漏えいの兆候はない」としている。攻撃者も侵入経路も不明。同省は 10 月前半、PHP2Shell の警報の時期に多くのサイトを予防停止していたが、今回との関係はわかっていない。
- **なぜ重要か**: 申告期限の直前に国の中心的な行政サービスが止まった。PHP2Shell と関連づけるのは早い。
- **悪用 / PoC**: 該当なし (インシデント)。
- 出典: [The Record](https://therecord.media/cyberattack-disrupts-belgian-tax-services-before-deadline)

### [2026-10-27〜29] パッチまとめ: Veeam Backup & Replication の未認証の認可回避 (CVE-2026-108142、v4 9.1) と、M365 版のテナントをまたぐ SQLi→RCE。Juniper Session Smart Router でも Critical 2 件
- **何が起きたか**:
  - **Veeam B&R** (KB4948): CDP Coordinator Service で、未認証のまま認可を回避できる (CVE-2026-108142)。対象は 13.1.1.18 以前と 13.0.2.29 以前で、12.x は影響なし。修正版は 13.1.2.57 / 13.0.3.63。Restore Operator によるパストラバーサル (CVE-2026-108140 / 108141) も修正。
  - **Veeam Backup for Microsoft 365** (KB4957): 認証済みの「組織の移管先」が SQL を注入し、テナントをまたいで設定を読み書きし、PostgreSQL のサービスアカウントで RCE できる (CVE-2026-106076、v4 9.0)。修正版は 8.6.0.1102。
  - **Juniper Session Smart Router / Conductor**: 18 件を修正。未認証の任意コマンド実行と権限昇格の Critical 2 件を含む (社内で発見)。
- **なぜ重要か**: Veeam B&R は過去にランサムウェアの侵入口として何度も KEV に入っている (CVE-2023-27532、CVE-2024-40711 など)。未認証の認可回避は、修正差分から exploit を作られやすい (評価)。
- **悪用 / PoC**: いずれも悪用は未確認とベンダーは説明。
- 出典: [SecurityWeek](https://www.securityweek.com/adobe-veeam-juniper-networks-patch-critical-vulnerabilities/) / [Veeam KB4948](https://www.veeam.com/kb4948) / [Veeam KB4957](https://www.veeam.com/kb4957)

### [2026-10-29] Talos IR の 2026 年 7〜9 月期: ランサムウェアの案件が 27% に増加。IT ヘルプデスクを装うビッシングで RMM を入れさせる手口が目立つ
- **何が起きたか**: 初期侵入はフィッシングが約 3 分の 1 (前期は 50% 超)、公開アプリの悪用も約 3 分の 1 で、標的は主にエッジ機器と管理画面。ランサムウェアとその前段階の案件は 27% で、過去 4 四半期の最大 20% を上回った。確認されたのは The Gentlemen、Qilin、Rhysida、Interlock と新顔の VYPR。EDR は脆弱なドライバーか WDAC で無効化されることが多かった。通信事業者では Salt Typhoon 系が CVE-2023-20198 (IOS XE) で侵入し、BadCandy を置いてログを無効にしていた。
- **なぜ重要か**: Red Team の想定シナリオに「ヘルプデスクを名乗って RMM を入れさせる」を加える根拠になる。BYOVD と WDAC ポリシーの悪用による EDR 停止は、検知の確認項目にもなる。
- **悪用 / PoC**: 実案件の集計。
- 出典: [Cisco Talos](https://blog.talosintelligence.com/ir-trends-q3-2026/)

### [2026-10-28] 法執行: Nefilim / Hive のアフィリエイトだったウクライナ人に、米国で禁錮 70 か月
- **何が起きたか**: Artem Stryzhak (36) は 2024 年 6 月にスペインで逮捕され、2025 年 4 月に米国へ引き渡された。2021 年に Nefilim のアフィリエイトとして活動し (身代金の 20% を運営者に払う契約)、Hive の初期のアフィリエイトとしても医療機関や法律事務所など 7 組織を攻撃した。米国務省は Nefilim 運営者の Volodymyr Tymoshchuk に最大 1,000 万ドルの懸賞金をかけている。
- **なぜ重要か**: 複数の RaaS を渡り歩くアフィリエイトを立件した例。運営者は捕まっていない。
- **悪用 / PoC**: 該当なし。
- 出典: [SecurityWeek](https://www.securityweek.com/ukrainian-hive-and-nefilim-ransomware-affiliate-gets-70-months-in-us-prison/)

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-10-28 以降 (JST) / 修正コミット公開済み or バグクラスが言語化可能なものを優先。公開日は OSV の `published` と NVD API で確認。

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-76418 | Cisco Secure Firewall ASA / FTD (SSL VPN、トンネルグループに二次認証を設定) | CWE-690 / 8.6 | 二次認証付きトンネルグループへの未認証の細工した接続要求 → 認証処理で戻り値を確かめずに NULL 参照 → 機器が再起動 (DoS) | [advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-asaftd-tunnel-dos-s6mgkb75) (commit 不明、クローズドソース) | **KEV (10/29 追加、期限 11/1)** / EPSS 0.0057 |
| CVE-2026-118650 / GHSA-375p-5qhx-8wq4 | labstack/echo v4 4.16.0 未満、v5 5.4.0 未満 (`middleware.Static` をグローバルに mount) | CWE-177, 863 / 7.5 | ルーティングはデコード前の `%2F` 入りパスで照合し、Static はデコード後のパスでファイルを返す → route / group 単位の認可ガードを経由せず保護ファイルを読める。前回の修正 (CVE-2026-55677) は `StaticFS` 側だけだった | [diff](https://github.com/labstack/echo/commit/b838391e2eade87ae7e5a09d7bb5087bec271ec1) / [diff](https://github.com/labstack/echo/commit/fc410094b2f3415cf2bf5204082137b205bfd5af) | 修正漏れの再発、パーサ差分。Gin / Chi / Fiber に横展開候補。EPSS 0.0040 |
| CVE-2026-9800 / GHSA-f5p5-6xmx-p252 | Keycloak keycloak-services 26.6.4 未満、keycloak-policy-enforcer 26.0.10 未満 | CWE-1025 / 8.1 | 認証済みユーザーが access-denied ページのパスを URL のパスやクエリに含める → Policy Enforcer の URI 比較の誤りで「access-denied ページへのアクセス」と見なされる → role / scope / UMA を含む全認可ポリシーを回避 | [advisory](https://github.com/keycloak/keycloak/security/advisories/GHSA-f5p5-6xmx-p252) (commit 不明) | 除外パスの部分一致の型。oauth2-proxy の skip-auth や独自フィルタへ横展開候補。EPSS 0.0065 |
| CVE-2026-62290 / GHSA-8rvj-mm4h-c258 | cert-manager 1.18.0〜1.19.5、1.20.0-alpha.0〜1.20.2 | CWE-863 / 7.3 | namespace のユーザーが ClusterIssuer を参照する `Challenge` を直接作成 → admission で Order / Issuer の solver との対応を検証せず、controller が `Challenge.spec.solver` をそのまま DNS01 設定に使う → `dnsZones` などの制限を回避し、ClusterIssuer の DNS 認証情報で任意の DNS 操作 | [diff](https://github.com/cert-manager/cert-manager/commit/6bda47297c8fbc6b121b8b76624b668d26f1a155) / [diff](https://github.com/cert-manager/cert-manager/commit/b37dbf01ecea50a0b3a19df0a7fe4c5ad6803f16) | 「内部生成のはずの子 CR を直接作れる」K8s operator の型 |
| CVE-2026-110858 / GHSA-f9j4-qggq-h239 (+ CVE-2026-110857 / GHSA-w8jc-g24h-crhw) | GitPython 3.1.30〜3.1.x (f9j4)、3.2.0 未満 (w8jc) | CWE-78, 88 / 8.1 | 攻撃者の影響を受けた値を `Remote.pull()` の位置引数 `refspec` に渡す → unsafe-option ガードはキーワード引数しか見ず、`--upload-pack=<cmd>` が `git pull` の argv に入る → 任意コマンド実行。w8jc は `ls_remote` の URL や `merge_base` の引数のガード漏れ | [diff](https://github.com/gitpython-developers/GitPython/commit/790bb3164948625ffb043d2a162425d55923fe9a) / [diff (w8jc)](https://github.com/gitpython-developers/GitPython/commit/9ad28cc4c7176d22cd6181d69805058a719dd03b) | 引数注入 (ガードがメソッド単位で部分的)。simple-git / dulwich へ横展開候補。EPSS 0.0047 |
| CVE-2026-114053 / GHSA-h3rc-6mm3-gc2m | vLLM 0.7.3〜0.30.x | CWE-829, 94 / 8.1 | `--trust-remote-code` で `auto_map` を使う processor のモデルを配信 → リクエストの `mm_processor_kwargs.code_revision` が `AutoProcessor.from_pretrained` に届く → 同リポジトリの別リビジョンの Python コードが import され RCE | [diff](https://github.com/vllm-project/vllm/commit/31f2e70cd3e403aaa471fb7fe3d33a7207aaf3cc) | **PoC 公開 (advisory 内)**。SGLang / TGI / LMDeploy へ横展開候補。EPSS 0.0046 |
| CVE-2026-109383 / GHSA-2m5v-pch6-74hx | undici 4.0.0〜6.29.0、7.0.0〜7.30.0、8.0.0〜8.12.1 | CWE-295 / 7.4 | `Agent` に関数を含む `tls` オプション (独自 `checkServerIdentity` など) を渡す → `Agent` がオプションを `JSON.parse(JSON.stringify())` で複製し関数が黙って消える → pinning が無効になり、Node 既定の検証を通る証明書を受け入れる。`fetch` の既定 dispatcher と `EnvHttpProxyAgent` も影響 | [diff](https://github.com/nodejs/undici/commit/04cb74b1db131ff8f5b4557dce811cbf5f4664b4) / [diff](https://github.com/nodejs/undici/commit/8c59f6b302898cb2e9b0f7962cd7212b6e597c9f) / [diff](https://github.com/nodejs/undici/commit/f75eac00ac177f7b2e6c8bfbd52d4113164286e6) | 検証が黙って消える型。設定を JSON 複製する SDK / プロキシ agent へ横展開候補。EPSS 0.0018 |
| CVE-2026-109829 / GHSA-4w7w-5xrc-9h26 | undici 7.0.0〜7.30.0、8.0.0〜8.12.1 | CWE-346, 524 / 7.4 | origin なしの `Agent` で `compose(redirect(), cache())` と shared cache を使う → cache が redirect 前の URL でキャッシュキーを作る → 別 origin の応答が元 URL のキーで保存され、cache poisoning や `private, no-store` 応答の他ユーザーへの漏えい | [diff](https://github.com/nodejs/undici/commit/26c2bfb3def0b67241ce878e80657ed5d6c3efa8) / [diff](https://github.com/nodejs/undici/commit/b20b82ad80a405a12b6ce1f341bcd418de390aa0) | interceptor の合成順でキーがずれる型。got / ky / OkHttp の interceptor を確認したい |
| CVE-2026-110864 / GHSA-r4xp-prcw-77qf | better-auth 1.5.0-beta.12〜1.7.6 (OAuth Proxy プラグイン) | CWE-287, 345 / 7.4 | OAuth Proxy の `secret` が未設定か global secret と同じ、state を cookie に保存、暗黙の account linking が有効 (既定) → プラグインが「復号できたユーザープロファイル」を無条件に信用 → 他ユーザーとしてサインイン (アカウント乗っ取り) | [diff](https://github.com/better-auth/better-auth/commit/ac54bfd67821a7607533af2059858b12bc54e26a) | 用途ごとに鍵を分けない暗号文流用の型。Auth.js や自作の OAuth proxy を確認したい |
| CVE-2026-63414 / GHSA-6j52-38f8-qhxr | shopify_app (RubyGems) 22.1.0〜23.0.2 | CWE-863 / High (CVSS v4, AT:P) | token exchange で認証する controller で、`current_shopify_domain` や `shop` でテナントを選ぶ → helper が検証済み ID token のショップではなくクエリの `shop` を返す → ショップ A で認証したままショップ B のデータやトークンにアクセス | [advisory](https://github.com/Shopify/shopify_app/security/advisories/GHSA-6j52-38f8-qhxr) / [release v23.0.3](https://github.com/Shopify/shopify_app/releases/tag/v23.0.3) (commit 不明) | 「検証した ID」と「使う ID」の不一致 (confused tenant)。マルチテナント SaaS の SDK へ横展開候補 |
| CVE-2026-106435 / GHSA-98qm-wvgf-w4cf | pymongo 3.9.0〜4.18.2 (C 拡張) | CWE-125 / High (CVSS v4) | NUL 終端のない mmap / buffer から信頼できない BSON を `bson.decode` → Regex 要素の pattern と flags を残りの長さを確かめる前に `strlen` で走査 → 範囲外読み取りで SIGSEGV (DoS) | [diff](https://github.com/mongodb/mongo-python-driver/commit/bb8d4e195275e75bd94ebeffb53cc747d357fcf4) | C パーサの典型。libbson / js-bson / Rust bson へ横展開候補 |
| GHSA-vpp8-g58w-m8mp (CVE 未採番) | Twisted 26.10.0rc1 未満 (HTTP/2 サーバ) | CWE-400, 770 / 7.5 | 未認証クライアントが `HEADERS(END_STREAM)` の直後に `RST_STREAM` を送る → `H2Connection.dataReceived` が reset の処理前に request をルーティングしてレンダリングし、reset 済み stream は同時実行数に数えられずレート制限もない → 1 接続で CPU を枯渇 (CVE-2023-44487 Rapid Reset 型の再発) | [diff](https://github.com/twisted/twisted/commit/498939422b69d5a75c4b8f81fa7926423dac534d) | 既知のプロトコル攻撃がマイナー実装に残存。hypercorn / aioquic を確認したい |

### 今日の CVE 所感
- 一番多いのは「検証したもの」と「実際に使うもの」がずれる型。Echo (エンコード済みのパスで照合し、デコード後のパスで配信)、shopify_app (検証したのは token のショップ、使うのはクエリの shop)、undici の cache (redirect 前の URL をキーにする)、Keycloak (除外パスの比較の誤り) がこれにあたる。
- 安全策が黙って消える型も目立つ。undici は JSON 複製で `checkServerIdentity` が消え、better-auth は「復号できたものは正しい」とみなす。AI セキュリティ欄の pdf-reader-mcp (認証有効と表示しつつ検証なし) も同じ系統で、どれもエラーが出ないためテストで見つけにくい。
- 横展開で最優先に見たいのは 2 つ。Go の Web フレームワークでの static と group middleware の `%2F` 差分 (Gin、Chi、Fiber)。K8s operator で、内部生成のはずの子 CR を直接作れて特権の認証情報を流用できる型 (cert-manager。ESO、Crossplane、Flux などにも同じ構造がありうる)。
- GitPython は、ガードをメソッドごとに後付けする方式が今も漏れ続けている (位置引数がガードの対象外)。他言語の git ラッパーも位置引数の扱いを確かめる価値がある。
- 悪用で最優先は KEV 入りの Cisco ASA / FTD (CVE-2026-76418)。PoC 公開で影響が大きいのは vLLM の `code_revision` RCE。選外の参考: Progress WS_FTP CVE-2026-84295 (CWE-287 / 10.0、10/29 公開、詳細とコミットは非公開)、graphql-tools executor-legacy-ws CVE-2026-118665 (前の接続の connectionParams が後の利用者の認証に使われる)。

## 日本国内のセキュリティ動向

### 国内インシデント・事故

#### [2026-10-28] アララ「アララ メッセージ」に不正アクセス。配信先リストのメールアドレス約 301 万件が流出
- **何が起きたか**: アララは 10/28 に 2 本のお知らせを出した。1 本目で第三者の不正アクセスを確認し、対象環境のサービスを止めたと公表した。同日夜の 2 本目で、環境「bvam001」のエンドユーザーリストに登録されたメールアドレス約 301 万件の流出を確認したとした。メールアドレス以外の流出は確認していないという。契約企業ごとの対象範囲は調査中で、再開時期は未定。侵入経路は公表されていない。
- **なぜ重要か (評価)**: ブラストメール (ラクスライトクラウド)、ユミルリンク (Cuenote) に続き、メール配信 ASP の大規模流出は 3 件目。件数はアドレスの延べ数で人数ではない。契約企業の名をかたるフィッシングが届くおそれがあり、契約企業側の公表が今後続く可能性がある。同社は 10/22 に PHP の脆弱性対応のお知らせを出しているが、今回の侵入との関係は示していない。
- 出典: [アララ (サービス停止, 10/28)](https://am.arara.com/news/2026102801) / [アララ (流出の報告, 10/28)](https://am.arara.com/news/2026102802)

#### [2026-10-29] 松屋フーズ、不正アクセスを検知し、公式アプリ (松弁ネット・モバイルオーダー・松弁デリバリー) とホームページを停止
- **何が起きたか**: 松屋フーズと松屋フーズホールディングスは、外部からの不正アクセスを検知し、松屋公式アプリと関連サービス、ホームページを停止したと公表した。NHK によると検知は 10/28 の 21 時ごろ。原因、影響範囲、漏えいの有無は調査中で、復旧の見通しは改めて知らせるとしている。
- **なぜ重要か (評価)**: アプリ会員と決済連携を持つ外食大手で、影響範囲によっては規模が大きくなりうる。続報で決済情報の扱いを確認したい。
- 出典: [松屋フーズ (公式サイトのお知らせ)](https://www.matsuyafoods.co.jp/) / [NHK (10/29)](https://news.web.nhk/newsweb/na/nd-20261029de67623) / [中日新聞 (共同, 10/29)](https://www.chunichi.co.jp/article/1332221)

#### [2026-10-29] グッドスマイルカンパニー公式 EC (第 3 報)。カード情報の一部を含む 402,466 枚分が閲覧された可能性、決済ページには不正プログラム
- **何が起きたか**: 4Gamer が伝えた第 3 報によると、影響は 2 種類ある。
  - **管理情報の閲覧** (10/19 午後〜10/22 22:00): 氏名・住所・電話番号・メールアドレス・注文内容と、カードの一部情報 (ブランド・下 4 桁・有効期限) が 402,466 枚分閲覧された可能性。
  - **スキミング** (10/21 13:55 ごろ〜10/23 7:00 ごろ): 決済ページに不正なプログラムが置かれ、この間にカードを入力した約 2,800 人は、名義・カード番号・有効期限・セキュリティコードを盗まれた可能性 (購入を完了していなくても対象)。Amazon Pay・PayPal の利用者と楽天市場店は対象外。
- **なぜ重要か (評価)**: 管理情報の閲覧とスキミングが同時に起きた。40 万枚分の連絡先と下 4 桁は、カード会社をかたるフィッシングの材料になりうる。件数と内訳が今回初めてそろった。
- 出典: [4Gamer (10/29)](https://www.4gamer.net/games/991/G999106/20261029019/) / [グッドスマイルカンパニー 第 3 報](https://support.goodsmile.com/hc/ja/articles/63718007508761) (Cloudflare の 403 で本文は取得できず)

#### [2026-10-29] アイリスオーヤマ、通販サイトへの不正アクセスを確認し、サイトを一時停止
- **何が起きたか**: NHK によると、アイリスオーヤマは 10/29、通販サイトへの不正アクセスを確認し、利用者を守るためサイトを一時停止したと発表した。情報漏えいの可能性も含めて調べている。検知日時・原因・件数は報道の範囲では示されていない。
- **なぜ重要か (評価)**: 大手の直販サイト (アイリスプラザ) で、会員とカード情報への影響が焦点。公式サイトは今回の取得で 403 を返し、一次情報は確認できていない。
- 出典: [NHK (10/29)](https://news.web.nhk/newsweb/na/nd-20261029de68116)

#### [2026-10-29] [続報] モイ「ツイキャス」(第 2 報)。停止までの約 15 分間に、個人情報 7 件とサーバー上のログにアクセスされた
- **前回から何が変わったか**: 10/28 10:20 ごろに探索が始まり、10:30 ごろに自動検知、10:45 ごろに完全停止した。この間に個人情報計 7 件 (カードの有効期限と暗号化された名義 1 件、メールアドレスと活動履歴など 6 件) へのアクセスを確認した。アカウント ID とメールアドレスを一部含むサーバー上のログにもアクセスがあり、規模は調査中。大規模流出は現時点で確認していない。X・Google・Facebook など全外部連携と外部認証をリセットした。
- **なぜ重要か (評価)**: 自動検知から 15 分で完全停止した初動は参考になる。一方、ログの持ち出しの規模と侵入要因は未確定。
- 出典: [モイ 第 2 報 (TDnet, 10/29)](https://www.release.tdnet.info/inbs/140120261029559851.pdf)

#### [2026-10-28] 十文字学園女子大学、9 月のサイバー攻撃を公表。大学の組織情報が外部サイトに掲載された
- **何が起きたか**: 大学は 9/19 に学内システムへの外部からのサイバー攻撃を確認していた。ドメイン名・所在地などの組織情報が特定の外部サイトに掲載されているのを確認し、10/28 に公表した。漏えいの有無と影響範囲は調査中で、警察と文部科学省に報告済み。TBS によると、学生と職員が使うシステムは今も使えない。
- **なぜ重要か (評価)**: 発覚から公表まで約 40 日。「特定の外部サイト」という書き方は、ランサムウェア集団のリークサイトへの掲載を思わせる。教育機関でのシステムの長期停止が続いている。
- 出典: [十文字学園女子大学 (10/28)](https://www.jumonji-u.ac.jp/important/systemfailure_20261028/index.html) / [TBS NEWS DIG (エキサイト経由)](https://www.excite.co.jp/news/article/TBSNews_1488390218043129880/)

#### [2026-10-29] ドトールコーヒー、システムの侵害で、都内 4 店舗の従業員 951 人分 (退職者を含む) の個人情報が流出した可能性
- **何が起きたか**: 10/20 にシステムへの侵害を検知した。保存されていた従業員 951 人分の氏名・住所・電話番号・生年月日・銀行口座番号などが流出した可能性がある。個人情報保護委員会に報告し、対象者に順次連絡している。侵害の手口は公表されていない。
- **なぜ重要か (評価)**: 顧客ではなく、従業員の口座番号を含む情報。給与・労務系システムの侵害は他社でも続いている。
- 出典: [Security NEXT (10/29)](https://www.security-next.com/192077)

> 参考 (公表日が範囲外のため本採用しない): ScanNetSecurity は 10/29 付で、Eストアー「ショップサーブ」の最終報 (同社の公表は 10/16) を報じた。5/21〜8/1 にアプリケーションの脆弱性を悪用され、購入者など約 2,335 万 6,000 人分が漏えい (うち約 209 万 6,900 人はカード情報の一部を含む、対象 7,858 店)。[ScanNetSecurity](https://scan.netsecurity.ne.jp/article/2026/10/29/56620.html)

### 国内の注意喚起・ガイドライン・政策

#### [2026-10-29] [続報] JPCERT/CC、PHP2Shell の注意喚起 (JPCERT-AT-2026-0033) を再更新。ファイアウォール製品への侵害成功の痕跡を追記
- **前回 (10/26 更新) から何が変わったか**: 「I. 概要」に、PHP2Shell と Linux カーネルの権限昇格を組み合わせ、あるファイアウォール製品の特定バージョンへの侵害が成功したことを示す痕跡と、内部への横展開の試みの痕跡が報告されていると追記した (Dream の報告を引用)。PHP を組み込んだ製品の管理者に、影響の確認とすぐの侵害調査を求めた。参考情報に、オランダ NCSC-NL の影響製品一覧リポジトリを加えた。
- **なぜ重要か (評価)**: Security NEXT は 10/29、CrowdStrike が「汎用的な RCE は当面難しい」と分析したと報じた。一方で JPCERT/CC は、機器ごとに作り込んだ exploit の成功例に注意を移した。PHP 本体の更新だけでなく、PHP を組み込んだアプライアンスをベンダーの更新で確認することが要点になる。
- 出典: [JPCERT/CC (10/29 更新)](https://www.jpcert.or.jp/at/2026/at260033.html) / [Security NEXT (10/29)](https://www.security-next.com/192097)

#### [2026-10-29] 消費者庁、「不正アクセスによる個人情報の漏えい等に関する注意喚起」を公表
- **何が起きたか**: 事業者への不正アクセスで漏えいが相次いでいることを受け、消費者向けに、ログイン ID とパスワードの変更と使い回しの禁止、多要素認証とパスキーの利用、カード・キャリア決済・ネットバンキングの明細の確認、SMS やメールのリンクを使わずブックマークや正規アプリからアクセスすること、警察庁推奨の詐欺電話対策アプリの導入を挙げた。
- **なぜ重要か (評価)**: IPA (10/26)、個人情報保護委員会 (10/7) に続き、消費者行政からも同趣旨の呼びかけが出た。官邸の指示 (下記) と同じ日の公表。
- 出典: [消費者庁 (10/29)](https://www.caa.go.jp/policies/policy/consumer_policy/caution/caution_039)

#### [2026-10-29] 高市首相、経済財政諮問会議で、相次ぐサイバー攻撃について国民への「タイムリーな情報発信」を指示
- **何が起きたか**: 共同通信によると、高市首相は 10/29 の経済財政諮問会議で、相次ぐサイバー攻撃を受けて「タイムリーな情報発信」を指示した。10/26 の関係閣僚会議で予告した「緊急対策パッケージ」(来週中をめど) は、10/29 時点ではまだ公表されていない。
- **なぜ重要か (評価)**: 緊急対策パッケージは 11 月上旬の取りまとめと見られる。被害企業への支援や、アクセス無害化を含む対処の具体策が出るかに注目したい。
- 出典: [京都新聞 (共同, 10/29)](https://www.kyoto-np.co.jp/articles/biz/1817265) / [ITmedia (10/27, 背景)](https://www.itmedia.co.jp/news/article/2610/27/2000002620/)

#### [2026-10-29] 第 19 回 日 ASEAN サイバーセキュリティ政策会議 (10/27〜28、バンコク) の結果を公表 (国家サイバー統括室・総務省・経産省)
- **何が起きたか**: 日本とタイが共同議長を務めた。各国の政策の方針を共有し、政策便覧の策定、重要インフラ防護ワークショップ、共同相互通知、日 ASEAN サイバー演習、能力構築などの成果を確認した。官民を含めた連携の強化で合意し、第 20 回は来年 10 月ごろに日本で開く予定。
- **なぜ重要か (評価)**: 定例会合で新しい枠組みは出ていない。ただ、アジアの拠点を経由した攻撃への対処で連携する土台になる。
- 出典: [経済産業省 (10/29)](https://www.meti.go.jp/press/2026/10/20261029005.html) / [総務省 (10/29)](https://www.soumu.go.jp/menu_news/s-news/01cyber01_02000001_00309.html)

### 国内製品の脆弱性 (JVN)

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| 2026-10-29 | JVN#82782759 / CVE は JVN 上で未記載 | Apache Struts 2 REST プラグイン 7.2.1〜7.3.0 / The Apache Software Foundation | REST の本文をデシリアライズする際、Jackson の `@JsonAnySetter` を付けたメンバーには `@StrutsParameter` の認可チェックが働かず、許可していない値を設定されうる (`struts.parameters.requireAnnotations=true` で `@JsonAnySetter` を宣言している場合) | CVSS 未記載 / データの改ざん。7.4.0 以降に更新し、`struts.rest.anySetter.requireAnnotations=true` を設定。報告者は三井物産セキュアディレクションの小河氏 | [JVN](https://jvn.jp/jp/JVN82782759/) |

- 期間内に JVN で公開されたほかの項目は、すべて既出のため表から外した: JVNVU#99905564 (PHP2Shell)、JVNVU#91027179 (ヤマハ NWR100)、JVN#23695234 (Yamaha LAN Monitor)、JVN#30675482 (YMS-VPN8)、JVNVU#96093239 (CISA ICS の転載)。
- JVN iPedia / MyJVN は 10/22 から停止中で、iPedia の新規登録 (JVNDB-) は確認できなかった。国内ベンダーの PSIRT ページ (三菱電機・NEC・日立・I-O DATA・サイボウズ・Aterm) にも期間内の新しいアドバイザリは見つからなかった。

### 国内コミュニティ・研究・イベント

#### [2026-10-29] piyolog「ダウンロード先指示ファイルを介した AI エージェントののっとりについてまとめてみた」
- **何が起きたか**: Forever Security が 10/22 に公表した事例と再現試験を整理した記事。実際の事例では、`~/Downloads` に置かれた AGENTS.md の指示に Codex が従い、悪性 npm パッケージ「function-color」(MAL-2026-17647) を入れようとした (導入は Forever の製品が遮断)。Forever によると、Codex では `~/.codex/config.toml` に MCP サーバーを書き込ませて各種制御を迂回でき、Claude Code では `.claude/settings.json` に ANTHROPIC_BASE_URL を書かせて通信先を差し替えられた (設定書き込みの成功は約半数、同じセッション内でのコード実行は約 5 分の 1)。10/28 の第三者検証 (80 回中 0 回) も紹介している。
- **なぜ重要か (評価)**: ウェブから操作なしに置けるファイルが、エージェントへの指示になりうる。確認項目 (想定外の `[mcp_servers.*]`、身に覚えのない `*_BASE_URL`) は、開発者の端末の点検にそのまま使える。ベンダーの主張と第三者の検証結果が食い違っている点に注意。
- 出典: [piyolog (10/29)](https://piyolog.hatenadiary.jp/entry/2026/10/29/170430)

#### [2026-10-29] マクニカの集計: 不正アクセスによる国内の情報漏えいは、2026 年 1 月〜10/27 で延べ約 3 億 2,900 万件
- **何が起きたか**: 共同通信によると、マクニカの集計で、企業を狙った不正アクセスで氏名やパスワードなどが流出した件数が、今年 1 月から 10/27 までで延べ約 3 億 2,900 万件に達した。2024 年は 370 万件、2025 年は 3,300 万件で、8 月以降の増加が目立つ。大口の例として、佐川急便 (最大延べ約 5,323 万件)、ユミルリンク (延べ約 5,162 万件)、タイムズカー (延べ約 146 万人) を挙げた。専門家は AI による無差別な攻撃の影響を指摘している。
- **なぜ重要か (評価)**: 2026 年の国内の漏えいが桁違いに増えたことを数字で示す。延べ件数なので重複を含み、人数とは比べられない。マクニカの一次の公表は確認できていない (報道ベース)。
- 出典: [秋田魁新報 (共同, 10/29)](https://www.sakigake.jp/news/article/20261029CO0107/)

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 60 (RSS / API / 個別記事。4 系統の調査を並行実行)
- 採用件数: AI技術=12 / AIセキュリティ=8 / セキュリティ=16 / CVE=12 (ID 13) / 国内インシデント=7 / 国内政策=4 / JVN=1 / 国内コミュニティ=2
- 除外理由内訳 (概数): 古すぎ=約 15 (WPSplinter 10/16、OVHcloud CLI 10/19、Plex2Shell 10/17、Gotenberg 10/26、ショップサーブ 10/16 ほか国内の 10/13〜21 公表分、GitLab CVE-2026-97229 の CVE 公開 10/13 は KEV 追加分のみ採用) / 重複=約 25 (Silent Train、Oracle EBS、Tailworm、EDK II、Adobe Campaign、Virtualine、Fragnesia KEV、Gemini 4 Carbon、Copilot harness、Yoba、vLLM CVE-2026-115918、JVN 既出 5 件ほか) / 日付不明=2 (Huntress の MDM 悪用、GhostAction 続報)
- 取得失敗ソース:
  - openai.com 本文 (403) → RSS の概要と model-spec.openai.com で代替
  - Dark Reading 本文 (Cloudflare) → 一次情報 (Symantec、Cequence) と RSS で代替
  - GitHub Advisory API (セッションのスコープ制限) → OSV の `modified_id.csv` と OSV API で代替
  - HiddenLayer / Lakera / VentureBeat / Rapid7 の RSS (XML 破損)、VulnCheck RSS (404)、GTIG / SpecterOps RSS (HTML が返る)、Huntress RSS (Cloudflare) → THN ThreatsDay、SecurityWeek、The Register で代替
  - Juniper サポートポータル (JS 描画) → SecurityWeek で代替
  - JVN iPedia RSS (サービス停止中) → jvn.jp の RSS と一覧で代替
  - support.goodsmile.com / irisohyama.co.jp (403) → 4Gamer / NHK で代替
  - 国家サイバー統括室・金融庁の新着一覧 (JS 描画) → 経産省・総務省の同時発表と報道で代替
  - エレコム / パナソニック / 富士通 / トレンドマイクロの PSIRT (403 / 429 / 404) → 代替なし、未確認
  - 日経クロステック (有料) → 冒頭のみ使用
  - oss-security と nuclei-templates は今回は未確認

</details>
