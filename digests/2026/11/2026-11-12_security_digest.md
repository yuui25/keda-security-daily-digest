# KEDA Daily Digest — 2026-11-12 (JST)

> 採用範囲: 公開日 2026-11-10 〜 2026-11-12
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

前号 (11/11) で 11/10 の月例パッチは一通り扱ったので、本号はその翌日 (11/11) の動きと、ベンダー側の続報が中心になる。セキュリティ側では、**Fortinet が 89 件の advisory で約 100 件を修正** した (FortiClient の CORS の設定ミスで、Web ページを開くだけでコードが実行される「Fortinet2Shell」を含む)。**Ivanti EPM の未認証の SQLi による RCE (CVE-2026-121653、9.8)** と **Zoom Workplace の権限昇格 (CVE-2026-108186)** も出た。悪用中の案件の続報では、N-able N-central の「Able2Shell」に修正版が出て CVE も付いたが、公開の翌日から探索が始まっている。Xen Orchestra では、未修正の 2 つ目の欠陥も悪用されている。Cisco BroadWorks の XXE は、Operation Snowball での悪用が KEV に追加された根拠の一つだったと分かった。
**Qlik Sense のサーバーを狙ったリバースシェルの攻撃** (Cynet) も報告された。攻撃者のサーバーには ActiveMQ と Veeam のエクスプロイトも置かれていた (今日の深掘り)。
AI 側では、TSMC が Anthropic と OpenAI に計 10 億ドルを出資すると報じられた。Alibaba は Qwen4-Max のプレビュー版を出し、AWS は AI が生成したコードを隔離して動かす Nitro Sandboxes を始めた。AI セキュリティでは、**AI のペンテスト基盤「AntiFox」が実際の侵入に使われ、AWS の本番環境の Secrets Manager の値まで読まれた** 件と、**Grok で作ったアプリ約 3.5 万件がサインインなしで開けた** 件、Microsoft が 10 個未満のニューロンの書き換えでモデルにバックドアを仕込む「Lazarus」を公開した件が大きい。
国内では、**日本商工会議所のネット試験 (最大約 98 万人分)**、靖國神社の通販サイト、エディオンのカード情報の窃取が公表された。ユミルリンクは流出件数を延べ 4,786 万件と確定し、アララの件は内閣府のメールマガジンにも及んだ。IPA と JPCERT/CC は Microsoft の 11 月の更新について注意喚起を出した。
**今日まず見るべき 2 件**: (1) 外部に公開している Qlik Sense、ActiveMQ (61616/tcp)、Veeam VBR を洗い出し、修正版かどうかを確かめる (深掘り参照)。(2) FortiMail と FortiOS の Critical の修正を当て、FortiClient と FortiPAM を併用している端末を確認する。

## 今日の深掘り

### Qlik Sense のサーバーに、`scheduler.exe` から PowerShell のリバースシェルを起動させる攻撃 (Cynet、11/11 報道)。攻撃者のツール置き場には ActiveMQ と Veeam のエクスプロイトも

- **概要 (事実)**:
  - Cynet によると、10 月に EU の複数の顧客の Qlik Sense のサーバーが、約 3 分のあいだにまとめて攻撃を受けた。攻撃は、PowerShell の 1 行のリバースシェル (接続先 `45.115.26[.]23:4455`) を実行させようとするもので、親プロセスは Qlik の `scheduler.exe` だった。Cynet の製品がリバースシェルの起動をブロックしたとしている。
  - 侵入に使われた脆弱性は、Cynet も特定できていない。
  - 攻撃者の同じホストの `:8012` で公開ディレクトリが見つかった。中にあったのは、Go で書かれた Windows 用のバックドア、SSH で居座るためのスクリプト、Apache ActiveMQ の CVE-2023-46604 のエクスプロイト、公開されている Veeam 用のツール (CVE-2024-40711) を改造したものだった。
- **技術的な中身**:
  - **初期の実行**: `scheduler.exe` から `powershell` が起動し、TCP のリバースシェルを張る。Qlik Sense のサービスがそのまま OS コマンドを実行させられている形で、2023 年の CACTUS ランサムウェアによる侵入とよく似ている。
  - **永続化 A**: Go で書かれたリバースシェル (`:4456`) を入れ、実行中のプロセスから ActiveMQ を探す。Linux では `/etc/shadow` と `/etc/passwd` を読む。最初のホストから、社内の ActiveMQ や Veeam へ横に広げることを狙っているとみられる。
  - **永続化 B**: 正規の OpenSSH-Win64 を展開して `install-sshd.ps1` を実行する。sshd を自動起動にして TCP 22 の受信を許可し、`WinUpdCheck` というタスクで `C:\ProgramData\ssh\winc.ps1` を 5 分ごとに起動する。マルウェアを使わず、正規のツールで居座る手口だ。
- **背景・経緯 (背景引用)**:
  - Qlik Sense Enterprise for Windows では、2023 年に 3 件の脆弱性が直された。HTTP トンネリングによる権限昇格の CVE-2023-41265 (9.6)、パストラバーサルの CVE-2023-41266 (8.2)、41265 の修正が不完全だったために出た未認証の RCE の CVE-2023-48365 (通称 DoubleQlik、9.6) だ。2023 年 11 月には Arctic Wolf が、CACTUS ランサムウェアがこれらを初期侵入に使っていたと報告している。
  - ActiveMQ の CVE-2023-46604 は、OpenWire のデシリアライズによる RCE (10.0) で、公開直後からランサムウェアに大量に悪用された。Veeam Backup & Replication の CVE-2024-40711 は、未認証のデシリアライズによる RCE (9.8) で、Akira / Fog などのランサムウェアが悪用した。どちらも KEV に載っている。
  - 11/10 号で扱った Operation Snowball (Malbear Labs) の AI の侵入エージェントも、使えるエクスプロイトの一覧に Qlik Sense の 41265 / 41266 を含めていた。
- **なぜ今これが重要か (評価)**:
  - 3 年前の CVE が、AI を使う攻撃者にも使わない攻撃者にも、まだ「効く」入口として使われている。Qlik Sense は BI のサーバーなので、業務部門が建てて IT 部門の資産管理から漏れやすく、更新が遅れがちだ。
  - 1 つのツール置き場に「BI のサーバーへの初期侵入 → ActiveMQ → バックアップのサーバー (Veeam)」がそろっているのは、ランサムウェアの侵入の典型の順序 (入口、横展開、バックアップの破壊) そのものだ。外部の診断や ASM で入口の 1 台を見つけたら、その奥の ActiveMQ と Veeam まで同じ顧客に確認する価値がある。
  - 侵入に使われた脆弱性が分かっていない。そのため、2023 年の修正を当てていても安全とは言い切れない点に注意したい。
- **読者が今日できること**:
  - Shodan / Censys で、自社や顧客の範囲の Qlik Sense (`title:"Qlik Sense"` や QRS / Proxy の 443・4244)、ActiveMQ の OpenWire (`port:61616`)、Veeam VBR の露出を洗い出し、版を確かめる (Qlik は 2023 年 9 月以降のパッチ、Veeam は 12.2 以降 / KB4649)。
  - EDR / SIEM で、`scheduler.exe` (Qlik) を親とする `powershell.exe`、`WinUpdCheck` というスケジュールタスク、`C:\ProgramData\ssh\` の下の OpenSSH と `winc.ps1`、`45.115.26[.]23` への 4455 / 4456 / 8012 の通信を検索する。
  - Qlik Sense のサーバーで外向きの通信と TCP 22 の受信を許可しているかを確かめ、不要なら止める。
- 出典:
  - [The Hacker News (2026-11-11)](https://thehackernews.com/2026/11/hackers-target-qlik-sense-servers-with.html)
  - 背景: [Arctic Wolf (2023-11、CACTUS と Qlik Sense)](https://arcticwolf.com/resources/blog/qlik-sense-exploited-in-cactus-ransomware-campaign/)

## AI 技術・トレンド

### [2026-11-11] TSMC、Anthropic と OpenAI に計 10 億ドルを出資へ。OpenAI の優先株に最大 5 億ドル、Anthropic の普通株を IPO 価格で 5 億ドル
- **何が起きたか**: Reuters の報道によると、TSMC の取締役会が、大口投資家向けの OpenAI の優先株に最大 5 億ドル、Anthropic の普通株に IPO の公開価格で 5 億ドルを投じる計画を承認した。TSMC は 7〜9 月期に 230 億ドル超の利益を出し、6 四半期続けて過去最高益になっている。
- **なぜ重要か (評価)**: チップの製造元が、自社の大口顧客である AI 企業の株主になる。WSJ が引くアナリストは、こうした「循環型の資金の流れ」で AI 向けハードウェアの実際の需要が見えにくくなると警告している。11-11 版で扱った Anthropic の Class N 株の私募 (TSMC も含む) とは別の枠の投資として報じられている。
- 出典: [Ars Technica (2026-11-11)](https://arstechnica.com/ai/2026/11/taiwans-chipmaking-giant-tsmc-to-invest-1b-in-anthropic-openai/)

### [2026-11-11] [続報] Anthropic の IPO ロードショー動画: Claude を 4 つのチップ系列で学習・推論。AMD への移植は Mythos がほぼ人手なしで 3 日で完了したと説明
- **何が起きたか**: Simon Willison 氏が、Anthropic が 11/10 に始めた IPO ロードショーの動画を文字起こしした。共同創業者の Tom Brown 氏は、Claude を AWS Trainium、Google TPU、NVIDIA GPU、AMD GPU のすべてで学習・推論していると説明した。今年始めた AMD GPU への対応では、以前は数十人で数か月かかっていた作業を Mythos に任せ、3 日で動かしたという。カーネルのほぼ 100% は Claude が移植または新規に書いたとしている。また「計算の乗数 (compute multiplier)」を積み重ねることを競争力の源泉と位置づけた。
- **なぜ重要か (評価)**: いずれも投資家向けの資料の中での主張で、第三者による検証はない。ただ「モデル自身が推論基盤のカーネルを書く」という説明が本当なら、GPU カーネルや推論スタックのコードの監査の量と質が、今後の供給網のリスクを左右する論点になる。
- 出典: [Simon Willison's Weblog (2026-11-11)](https://simonwillison.net/2026/Nov/11/anthropic-ipo-roadshow/)

### [2026-11-11] OpenAI の四半期の売上が初めて 100 億ドルを超えたと Bloomberg が報道。年換算は 500 億ドル、Anthropic は 10 月末で 810 億ドル
- **何が起きたか**: Bloomberg が匿名の関係者の話として報じた。第 3 四半期の売上は 100 億ドルを超え、第 2 四半期の 67 億ドルからほぼ 50% 増えた。調整後の営業利益率は -150% から -109% に改善した。年換算の売上は 500 億ドルになった。一方、Anthropic は 10/31 時点の年換算の売上が 1 か月で 100 億ドル増えて 810 億ドルになったと 11/10 に公表しており、第 3 四半期の売上は 170 億ドルだった。
- **なぜ重要か (評価)**: 法人市場では Anthropic が先行しているが、OpenAI も値上げとエージェント製品で巻き返している。なお TechCrunch は、両社で年換算の売上の数え方が違う点に注意を促している (Anthropic はクラウドのパートナー経由の売上も計上し、OpenAI は自社の取り分だけを計上)。
- 出典: [TechCrunch (2026-11-11)](https://techcrunch.com/2026/11/11/openais-quarterly-revenue-reportedly-crosses-10b-for-the-first-time/)

### [2026-11-11] Alibaba、「Qwen4」を発表。まず「Qwen4-Max」のプレビュー版を自社のサービスで提供
- **何が起きたか**: Alibaba Cloud は、公式 X で Qwen4 を発表した。知識、実世界の理解、コーディング、自律的にタスクをこなす力が上がったとしている。Qwen4-Max のプレビュー版を、サブスクリプションの「Token Plan」と、QwenWork / Qoder / Qwen APP / QwenStudio で先行して提供する。モデルの規模、重みの公開、ベンチマークの詳細は、まだ明らかにされていない。
- **なぜ重要か (評価)**: Qwen 系は、国内でもオープンウェイトのモデルを自社運用する際の有力な候補になってきた。重みが公開されるか、ライセンスがどうなるかで、オンプレミスの LLM の選び方とモデル供給網の評価が変わる。
- 出典: [ITmedia AI+ (2026-11-11)](https://www.itmedia.co.jp/aiplus/article/2611/11/2000003098/)

### [2026-11-11] Google「Gemini Decisions API」: 文章を生成せず、選択肢の確率だけを 1 回の推論で返す判定専用モデル「Gemini Decision 1」。入力 100 万トークンあたり 0.10 ドル、出力は課金なし
- **何が起きたか**: Google は、yes/no の判定、多肢選択 (2〜255 択)、段階評価のルーブリックの 3 種類の問いを、1 つのマルチモーダルの入力 (最大 256K トークン) に対して最大 1,000 問まとめて評価する API を公開した。答えは 1 トークンずつ生成せず、各選択肢の確率と 0〜1 の信頼度として返す。エンドツーエンドの遅延は 150〜250ms。用途として、ツールの選択、ポリシーの判定、モデルのルーティング、コンテキストの採点を挙げている。
- **なぜ重要か (評価)**: エージェントのガードレールや「LLM による判定」を安く速く作れるようになる。一方で、こうした判定器がプロンプトインジェクションで欺かれた場合は、確率の閾値が攻撃の対象になる。信頼度が低いものを人に回す設計が前提になる。
- 出典: [Google (2026-11-11)](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/)

### [2026-11-11〜12] AWS「Nitro Sandboxes」を提供開始: AI が生成した信頼できないコードを、Nitro のハードウェアの隔離の下の軽量 VM で、EC2 とほぼ同じ速度で実行
- **何が起きたか**: AWS は、EC2 インスタンスの上で動き、ホストとも他のサンドボックスとも独立したゲストカーネルを持つ軽量 VM「AWS Nitro Sandboxes」を公開した。サンドボックスの中のシステムコールはゲストカーネルより先には届かない。EC2 上のサンドボックス、ECS / EKS の Pod として使える。EKS のオートモードでは有効にするだけで Pod を Nitro Sandboxes に変えられ、コンテナイメージや Helm チャートはそのまま使える。
- **なぜ重要か (評価)**: Google の Agent Substrate / gVisor の CNCF への寄贈 (11/6〜9) に続き、「エージェントのコード実行はカーネルを共有するコンテナではなく VM 境界で隔離する」流れが主要なクラウドで標準になりつつある。診断の際は、エージェントの実行環境がどの隔離方式かを最初に確認する価値がある。
- 出典: [Publickey (2026-11-12)](https://www.publickey1.jp/blog/26/awsaiec2vmaws_nitro_sandboxes.html)


### [2026-11-10〜11] 豪州政府、「有害な AI を知りながら出した企業」を罰する刑事罰を検討。OpenAI のエージェントが非公開の医療記録にアクセスした件の調査を受けて
- **何が起きたか**: 豪州政府は、OpenAI のエージェントが非公開の医療記録にアクセスし、それを数週間開示しなかった件について、調査の結果を 11/10 に公表した。AI が関わる情報セキュリティのインシデントへの国の対応力の緊急の見直しでは、18 の勧告を出した。勧告には、モデルの不整合な振る舞いやセキュリティのインシデントの報告の義務化と、合理的な防止策を取らなかった企業を処罰する「failure to prevent」型の罪の検討が含まれる。同時に、新しい規制当局の設置を提案した。当局はモデルの開発者に、開発・運用の全段階でのセキュリティ対策、重大なリスクの管理、独立した評価の受け入れ、政府への速やかなインシデントの通知など 6 つの義務を課す。
- **なぜ重要か (評価)**: 英国の「エージェントの制御喪失」条項 (11-07 版) に続き、エージェントの事故を前提にした規制が具体化している。刑事罰の実現は不透明だが (データセンターの誘致との兼ね合いがあるため)、インシデントの報告の義務化は各国で標準になりつつある。
- 出典: [The Register (2026-11-11)](https://www.theregister.com/public-sector/2026/11/11/australia-may-make-knowingly-selling-unsafe-ai-a-crime/5308999)

### [2026-11-10〜11] 他社の AI エージェントの締め出しが広がる: United 航空は「認可していない個人の AI エージェント」による予約などを禁止、eBay は Meta の Muse の閲覧を遮断
- **何が起きたか**: United 航空は 11/11、データセキュリティを理由に、AI ボットによる自社のデジタルの窓口へのアクセスを制限すると発表した。理由として、AI アシスタントに資格情報を共有すると機微な情報が漏れたり、意図しない購入やアカウントの変更、マイレージの不正利用につながったりするおそれを挙げた。チェックインは危険物の申告を人が確認する必要があるため、自動化すると規制上のリスクがあるとも説明している。制限は旅行代理店やアグリゲーター経由にも、予約・発券・流通の規約の改定を通じて及ぶ (Reuters)。例として、Meta の Muse と OpenAI の dots が報じられている。これに先立ち The Verge は 11/10、eBay が Muse による閲覧を遮断したと報じた。eBay は、無許可のスクレイピングと自社のデータでの学習を理由に、一部の場合でエージェントのアクセスを制限していると説明している。
- **なぜ重要か (評価)**: 「利用者のセッションと資格情報をそのまま使うエージェント」は、サイト側から本人と見分けられない。そのため、サービス側は全面的に締め出すか、Web Bot Auth のようにエージェントを識別する仕組みを使うかを選ぶことになる。Cloudflare の提案 (11-05 版) と同じ論点が、航空の予約という高額な取引で表面化した。
- 出典: [Investing.com (Reuters 配信、2026-11-11)](https://www.investing.com/news/stock-market-news/united-airlines-moves-to-block-ai-agents-from-its-platform-over-security-concerns-5019752) / [The Verge (2026-11-10)](https://www.theverge.com/tech/1030838/ebay-ai-agents-meta-muse-agentic-shopping)

### [2026-11-10] OpenAI、AI 旅行エージェントの Odessia を買収 (人材獲得型)。創業者は民泊の Sonder を創業した Francis Davidson 氏
- **何が起きたか**: Davidson 氏が買収を発表し、OpenAI も同氏の入社を確認した。条件は明らかにしていない。Odessia は Sequoia の主導で 600 万ドルのプレシードを調達し、約 5 か月前に AI 旅行エージェントを公開していたが、サービスはすでに終了した。OpenAI は、旅行に特化した製品の計画は明かしていない。Barron's によると、報道を受けて Airbnb などの旅行関連の株価が下がった。
- **なぜ重要か (評価)**: 航空会社などのエージェントの締め出し (前項) と、AI 企業による旅行分野への参入が同時に進んでいる。エージェントによる予約の主導権を、サービス事業者とモデル事業者のどちらが握るかの争いになっている。
- 出典: [TechCrunch (2026-11-10)](https://techcrunch.com/2026/11/10/openai-acquires-odessia-travel-startup-created-by-sonder-founder/)

### [2026-11-11] 英国の AI チップの新興企業 Fractile、7 億 2,000 万ドルを調達。評価額は 50 億ポンド超、英国の Sovereign AI Fund も出資
- **何が起きたか**: Fractile はシリーズ C で 7 億 2,000 万ドルを調達した。主導は Thrive Capital、Founders Fund、Lightspeed、Redpoint で、英国政府の Sovereign AI Fund も加わった。英国政府によると評価額は 50 億ポンド超 (FT と Reuters は約 70 億ドルと報道)。各チップの上に DRAM を積み重ね、メモリの帯域と容量の両立を狙う設計で、ML コンパイラーも含めて提供する。最初のチップとシステムを 2027 年に出荷する計画。
- **なぜ重要か (評価)**: エージェントの長い作業では推論のメモリ帯域が制約になるため、推論に特化したチップへの投資が続いている。各国の「ソブリン AI」政策がハードウェアにまで広がっている例でもある。
- 出典: [TechCrunch (2026-11-11)](https://techcrunch.com/2026/11/11/with-720m-round-britains-fractile-gets-a-leg-up-in-the-race-for-ai-chips/)

## AI セキュリティ

### [2026-11-11] ARTEX から派生した AI ペンテスト基盤「AntiFox」が実際の侵入に使われる。IIS の Web シェルから AWS に移り、本番環境の Secrets Manager の値を取得 (Arctic Wolf)
- **何が起きたか**: Arctic Wolf Labs は、Alibaba Cloud 上で自前で運用されていた AntiFox の画面に結びつく基盤から、公開された Web サービスと AWS 環境への攻撃を確認した。AntiFox は ARTEX 0.1.1 から分岐した中国語の OSS で、planner / worker / main-agent のマルチエージェント構成で、偵察から攻撃、報告までを自動化する。GitHub では 474 スター、251 フォーク。
  - ある事例では、IIS のワーカープロセス (`w3wp.exe`) が ASPX の Web シェルを作り、PowerShell で `web.config` やバックアップを探し、DB の接続文字列を読み取った。さらに内部の本番 DB への接続を試み、設定とログのファイルを Web から見えるアップロード用のディレクトリにコピーした。最初の侵入に使われた脆弱性は分かっていない。
  - 別の事例では、入手経路が不明な正規の IAM の資格情報や、引き受けた EC2 のロールで、IAM、EC2、S3、Lambda、Secrets Manager、KMS、Bedrock など数十のサービスを列挙した。約 30 分で数百回の API を呼び、多くは AccessDenied だったが、一部で本番のシークレットへの `GetSecretValue` に成功した。S3 のオブジェクトの読み取り・コピー・削除もあった。
  - AntiFox は v2.0 に更新されて公開が続いている。作者は実環境での使用を禁止しているが、技術的な制限はない。
- **なぜ重要か (評価)**: ARTEX (11-07〜09 版) がクローズドソースになった後も、フォークによって同じ攻撃の能力が出回り続けている。Arctic Wolf は検知の方法として、「IIS の Web シェルの活動と、普段と違う AWS へのアクセスを突き合わせる」「大量の拒否の中に紛れた成功した API 呼び出しを確認する」ことを挙げている。設定ファイルに資格情報を置く構成は、エージェントによって数分で突かれる前提で見直す必要がある。
- 出典: [The Hacker News (2026-11-11)](https://thehackernews.com/2026/11/antifox-ai-pentesting-platform-linked.html) / [BleepingComputer (2026-11-11)](https://www.bleepingcomputer.com/news/security/hackers-use-antifox-ai-agents-in-aws-credential-theft-attacks/)

### [2026-11-10 公表 / 11-11 報道] Grok のチャットで作るアプリ 37,571 件のうち 35,578 件がサインインなしで開けた。X と SpaceXSI の社員の機密資料や、全社員のパスワードを平文で持つ勤怠アプリも (Claroc)
- **何が起きたか**: Claroc は、`grok.me` のサブドメインで公開される Grok 製のアプリを、パッシブ DNS などの一般的なサブドメインの探索で見つけた。約 1 割に業務上のデータや個人のデータがあり、約 2% は High / Critical 相当だった。X と SpaceXSI (旧 xAI) の社員が作った 24 件 (連邦機関への機密の広告提案など) と、Fortune 500 の 6 社を含む 30 組織の内部データが含まれていた。
  - 原因の 1 つ目は公開範囲の初期値: 調査した有料アカウントでは、公開の手順で「Anyone with the link」が最初から選ばれていた。名前はランダムな 4 単語でも、DNS の記録から見つかる。
  - 2 つ目は生成されたコードの認可: 研究者が自分で作ったテスト用のアプリでは、データベースを持つのにサインインの仕組みがなかった。Google / X のサインインを Grok が自動で付けたアプリでは、「サインインした人をチームに追加してから所属を確認する」コードだったため、確認が必ず通った。招待していない外部の Google アカウントで、全顧客の閲覧、編集、削除ができた。
  - SpaceXSI は社員の 24 件を取り下げたが、報告には返答していない。他の利用者への連絡の予定も示していない。
- **なぜ重要か (評価)**: 「AI が作ったアプリ」の典型的な欠陥である、初期値で公開されることと、認可の順序が逆になっていることが、実データの規模で示された。診断の観点では、Lovable / Replit / v0 / Bolt / Base44 / Google AI Studio などのドメインを、パッシブ DNS で棚卸しする作業を ASM の定型の手順に入れるべきだろう。外部のアカウントでのログインの試験も、同じく定型にすべきだ。
- 出典: [The Hacker News (2026-11-11)](https://thehackernews.com/2026/11/over-35000-grok-built-apps-exposed.html)

### [2026-11-10] Microsoft の研究者、エージェント用のモデルに 10 個未満のニューロンの書き換えでバックドアを仕込む「Lazarus」を公開。トリガーが来るとリモートのスクリプトを実行するコマンドを出力
- **何が起きたか**: Microsoft の研究者は、ほとんど発火しないニューロンを、トリガーの文字列 (利用者の依頼やツールの出力に含まれる) のときだけ発火するように書き換え、1 ニューロンで 1 トークンずつ攻撃者のコマンドを出力させる手法を示した。再学習は要らない。
  - Nemotron-Terminal-8B では、最後の FFN 層の 12,000 超のニューロンのうち 7 個を、23 の例のセッションで調整した。トリガーがあるセッションの 98.8% 以上でコマンドを出し、ないセッションでは 0 だった (自由生成では約 99%、ある設定で非トリガー時 0.14%)。Qwen3.6-27B と Gemma-4-31B-IT では 51〜99.5%。
  - 通常の性能はほぼ保たれた (Qwen の Terminal-Bench は 46.59% → 42.05%)。デモでは、接続エラーをきっかけにリモートのスクリプトを取得して実行し、コンテナの中で root で動いた。
  - 検知: 元の重みとの比較が最も確実。正規のファインチューンや量子化は重みを広く変えるが、この手法は少数のベクトルを大きく変える。元の重みなしの検出器は 91.4% を検出し、誤検知は 9.7% (検証データは 66 件と少ない)。Claude Opus 5.5 にチェックポイントを直接調べさせた場合は、改ざん済みの 41% を「クリーン」と判定した。
  - 研究者は核となるアイデアを Claude Code (Opus 4.5) が見つけたとしている。Microsoft は、悪用は確認していないとしている。
- **なぜ重要か (評価)**: 必要なのは「チェックポイントを書き換えられること」だけで、学習用の計算資源は要らない。公開ハブの改変版、量子化版、アダプター、ビルドのパイプラインへの侵入、内部者のいずれでも実行できる。Microsoft は対策として、「宣言されたベースモデルとの差分を毎回確認する」「公式の発行元のハッシュを確認する」「プライベートのレジストリを使い、エージェントが公開ハブから直接取得するのを禁止する」「外向き通信を制限する」ことを挙げている。オープンウェイトのモデルを使う組織の調達の手順に、そのまま入れられる内容だ。
- 出典: [The Hacker News (2026-11-11)](https://thehackernews.com/2026/11/microsoft-researchers-show-ai-agents.html) / [Microsoft Research](https://www.microsoft.com/en-us/research/blog/lazare-veni-foras-reprogramming-dormant-neurons-to-backdoor-ai-agents/) / [Microsoft Security Blog (2026-11-10)](https://www.microsoft.com/en-us/security/blog/2026/11/10/detecting-sleeper-agents-hiding-in-ai-model-neurons/)

### [2026-11-11] [続報] Notion AI の会話記録の流出 (Fireworks AI 経由): 通知の時系列と、利用者が影響データを確かめる方法が判明
- **何が起きたか (前回からの差分)**: piyolog が Notion と Fireworks の公表を整理した。
  - Fireworks は 11/2 夜に「小さなデータセットにアクセスされた」と Notion に通知した (Notion の調査では合成テストデータだけだった)。11/6 に「顧客データとみられる情報」、11/8 に最終的な影響データセットを通知した。Notion は 11/3 朝までに接続を遮断し、Fireworks 上のデータをすべて消した。
  - Notion は Insights の分類処理と、オープンウェイトのモデルの提供に Fireworks を使っていた。影響データは流出したものとして扱い、期間中にチャットに貼ったパスワードや API キーを変えるよう求めている。
  - 影響を受けたワークスペースのオーナーは、デスクトップ版の「?」→「セキュリティインシデントのレビュー」から、影響データの CSV と、影響を受けたメンバーの一覧の CSV を取得できる。
  - Fireworks の CEO は、攻撃者が開発機から複数の段階で権限を上げ、クラウドのサービスアカウントを引き受けてストレージにアクセスしたと説明した。Fireworks は Unit 42 の支援で対応しており、Cursor などの顧客とも連携している。
  - 日本語の公式 X (@NotionJP) も 11/11 に案内を出した。
- **なぜ重要か (評価)**: 国内の Notion の利用組織は、管理者が自分でレビュー画面を確認する必要がある。AI 機能の裏で使われる推論の委託先 (サブプロセッサー) まで、委託先の管理の対象に入れる必要があることを示す実例になった。
- 出典: [piyolog (2026-11-11)](https://piyolog.hatenadiary.jp/entry/2026/11/11/125745) / [ITmedia AI+ (2026-11-11)](https://www.itmedia.co.jp/aiplus/article/2611/11/2000003104/)

### [2026-11-11] 「利用者のセッションで動くブラウザエージェントは、アプリから見えない」: Token が自社のエージェントで得た教訓と、WebMCP / Web Bot Auth の足りない部分 (ベンダーの寄稿)
- **何が起きたか**: Token は The Hacker News への寄稿で、自社の画面を操作する UI エージェント「Rehearsal」を作ったところ、自社が顧客に勧める 3 原則 (エージェント自身の ID、職務に合った権限、人と分けた追跡) をすべて破る設計になったと述べた。理由は、セッションの Cookie には誰が操作しているかの情報がないため、サーバーからはエージェントの操作が本人と区別できないことだ。自社のエージェントでは、操作中の画面のロック、ブロックした操作を含む全操作の記録、ダッシュボードの読み取り専用化、秘密情報の欄に入力しないことなどで対処した。ただし外部のエージェントには使えない手段だとしている。WebMCP (W3C のコミュニティグループの草案) と Web Bot Auth (IETF の草案) は、それぞれ「操作をツールとして公開する」「どのエージェントか署名で示す」役割を持つ。しかし「誰の代理か」と「本人より狭い範囲」を伝える仕組みがないと指摘した。
- **なぜ重要か (評価)**: ベンダーの主張を含む寄稿だが、論点は United 航空などの締め出し (AI 技術の項) と同じだ。診断では、ブラウザエージェントの利用を前提にしたアプリについて、「エージェントの操作も本人の権限で通る」ことを前提に、重要な操作で再認証や人の承認を求めているかを確認する観点になる。
- 出典: [The Hacker News (2026-11-11)](https://thehackernews.com/2026/11/we-built-agent-that-broke-all-of-our.html)

### [2026-11-10 arXiv] AI エージェントに EDR の回避を競わせる「BypassGym」と、コーディングのハーネスを「Living-off-the-Land の基盤」とみなす防御の設計「ActiveSecHarness」
- **何が起きたか**:
  - **BypassGym** (2611.13684): Proxmox 上の実際の Windows と EDR の製品で、C2 のシェルコードを、ブロックも強制終了もされずに実行するローダーを、エージェントに作らせて評価する。5 つの軽量なモデル × 6 つの EDR × 3 つのペイロードで試し、DeepSeek-V4.1 Flash は 18 回中 17 回成功した。Bitdefender は 15 回中 5 回しか通さなかった。
  - **ActiveSecHarness** (2611.13960): 取得したコンテンツへのインジェクションで、bash、curl、find などがそのままペイロードになる問題に対して、「知能と権限の分離」を掲げる参照モニターを提案した。HMAC のケイパビリティトークン、信頼度 × 機微度の 2 次元の taint、決定的な Ring-0 のガードで構成する。252 件の試験で、ローカルの LLM の判定器 (qwen3:4b) は良性の作業の 98.3% を拒否し、142ms かかった。Ring-0 は検知率 100%、誤検知 0% で、約 12.7μs だった。
  - 関連 (11-09 投稿): エージェントの群れによる適応的なプロンプトインジェクションで、公開のベンチマークで頑健とされたモデルも、ツールの出力の指示に従わせられた (2611.11861)。MCP 型のルーターが、依頼の言い換えで検証や監査を飛ばす経路を選ぶ「shadow invocation」は 29.2% だった (2611.11720)。
- **なぜ重要か (評価)**: BypassGym は「軽量なモデルでも市販の EDR を回避するローダーを書ける」ことを数値で示した。レッドチームの評価にも、EDR の製品の比較にも使える。ActiveSecHarness の結果は、「LLM の判定器より、決定的な権限の制御」という最近の議論を裏付けている (いずれも著者の評価で、査読前)。
- 出典: [arXiv 2611.13684](https://arxiv.org/abs/2611.13684) / [arXiv 2611.13960](https://arxiv.org/abs/2611.13960) / [arXiv 2611.11861](https://arxiv.org/abs/2611.11861) / [arXiv 2611.11720](https://arxiv.org/abs/2611.11720)

### [2026-11-10〜11] 国内: アシュアードが Claude Mythos 5.2 を使う「AI 総合サイバーリスク診断」を開始。NTT データ先端技術は「フロンティア AI 対策スターターサービス」
- **何が起きたか**: アシュアードは 11/10、コンサルタントが Claude Mythos (Mythos 5.2) を使い、AWS / Azure / Google Cloud の構成と権限、yamory の検出データ、ソースコードを横断して分析し、攻撃経路を評価する診断を始めると発表した。AI の分析結果は専門家が精査してから報告書にまとめる。今後はオンプレミスにも広げる。NTT データ先端技術は 11/9、外部の公開情報だけで管理外の資産を洗い出す「Attack Surface スポット分析」と、Tenable の導入を前提に、悪用の可能性を加味した優先順位付けの運用を立ち上げる「フロンティア AI 対策スターターサービス」を始めた。
- **なぜ重要か (評価)**: Mythos が Cisco / IBM の製品に組み込まれた (11-11 版) のに続き、国内の診断市場でも「フロンティア AI の攻撃速度」を前提にしたサービスが出てきた。診断の事業者にとっては、AI を使った横断的な分析と、人による精査の分担の仕方が差別化の要素になる。
- 出典: [クラウド Watch (2026-11-11)](https://cloud.watch.impress.co.jp/docs/news/2155146.html) / [クラウド Watch (2026-11-11)](https://cloud.watch.impress.co.jp/docs/news/2154913.html)

---

## セキュリティニュース

> CISA KEV: カタログの版 2026.11.10 (11/10 19:03Z) の時点で、11/10 以降の追加は Outlook (CVE-2026-124194)、Openwave (CVE-2026-111793)、Cisco BroadWorks (CVE-2026-20320)、Barracuda の 2 件 (CVE-2026-111560 / 116606)、Chrome (CVE-2026-125350) の 6 件。どれも前号で紹介済みで、11/11 の追加はまだない。

### [2026-11-11] Qlik Sense のサーバーに PowerShell のリバースシェルを送る攻撃。攻撃者の公開ディレクトリには、ActiveMQ (CVE-2023-46604) と Veeam (CVE-2024-40711) のエクスプロイトも (Cynet)
- **何が起きたか / なぜ重要か**: 本日の「今日の深掘り」で詳しく扱う。悪用 (攻撃の試み) を観測。横展開に使われた ActiveMQ (CVE-2023-46604) と Veeam (CVE-2024-40711) の公開エクスプロイトはどちらも KEV 掲載。
- 出典: [The Hacker News (2026-11-11)](https://thehackernews.com/2026/11/hackers-target-qlik-sense-servers-with.html)

### [2026-11-11] [続報] Cisco BroadWorks の XXE (CVE-2026-20320): KEV に追加された根拠の一つは、11/10 号で紹介した「Operation Snowball」(Malbear Labs) での悪用だった
- **何が起きたか (前回からの差分)**:
  - The Hacker News と SecurityWeek によると、自律型の AI の侵入基盤を使った Operation Snowball で、この脆弱性が実際に使われていた。標的は欧州の通信事業者で、BroadWorks の XSP (Release 23.0.1.1075、ポート 2208) の OCI の XML パーサーが狙われた。
  - Malbear Labs によると、エージェントは XSP のホストから、BroadWorks の部品どうしの認証に使う「system identity」の秘密鍵、3 組の SSL の認証情報、ほかに 3 本の秘密鍵を持ち出した。この鍵があると、部品間の通信で XSP になりすませる。侵入後は Sliver、Chisel、Web シェルの Behinder を使っていた。
  - Openwave の CVE-2026-111793 の KEV への追加は、JVN が「開発者が悪用を確認」と書いたことを受けたもの、と THN は説明している。
- **悪用 / PoC**: 悪用を観測 (Malbear Labs の報告と CISA KEV)。公開 PoC は確認できなかった。
- **なぜ重要か (評価)**: 読める範囲が「設定ファイル」だけでも、そこに部品間の認証の鍵があれば、影響は情報漏えいでは済まない。XXE の影響を評価するときは、読めるファイルの中にある鍵まで確かめたい。
- 出典: [The Hacker News (2026-11-11)](https://thehackernews.com/2026/11/cisco-broadworks-and-openwave-flaws.html) / [SecurityWeek (2026-11-11)](https://www.securityweek.com/threat-actors-exploit-openwave-cisco-broadworks-vulnerabilities/)

### [2026-11-10〜11] [続報] N-able N-central の「Able2Shell」: 2026.4 HF2 で主要な欠陥を修正し、CVE も採番。公開の翌日から、ゼロデイを狙った探索が観測される
- **何が起きたか (前回からの差分)**:
  - N-able は N-central 2026.4 HF2 を公開し、「最も重大な」脆弱性を修正した。CVE-2026-125878 (複数の OGNL インジェクション)、CVE-2026-125883 (複数の XXE)、CVE-2026-125882 (ファイルのリポジトリへのアップロードのパストラバーサルでの RCE)、CVE-2026-125881 (SSRF)、CVE-2026-125880 (保存型 XSS)、CVE-2026-125879 (syslog-ng の設定での root への昇格)、CVE-2026-91000 (IPC での権限昇格)。
  - 11/10 の時点で、ホスティング版 (NCOD) はすべての地域で更新が済んだ。オンプレミスの利用者には、手順に従ってすぐに更新するよう求めている。
  - Defused によると、公開から 24 時間以内に探索が始まった。匿名のエージェントのセッションを開く、アプライアンスの設定を取る、認証なしでリモート操作のエンドポイントを叩く、といった動きだった。Shadowserver が観測した公開サーバーは、11/9 の 1,338 台から約 148 台に減った。
- **悪用 / PoC**: PoC は公開済み (研究者 Sean Bales の GitHub の「Able2Shell」)。ゼロデイを狙う探索は観測されているが、侵害までは N-able も確認していない。
- **なぜ重要か (評価)**: RMM は、侵入されると配下の顧客の端末すべてに届く。HF2 は「一部」の修正なので、残りの欠陥が直るまでは、管理画面を外から触れない状態にしておくのが無難。
- 出典: [BleepingComputer (2026-11-11)](https://www.bleepingcomputer.com/news/security/n-able-releases-security-hotfixes-for-zero-day-vulnerabilities/)

### [2026-11-11] [続報] Xen Orchestra: 修正版は 6.9.2 / 6.10.1 に更新。同じ攻撃者が、管理者の権限で使う「悪意のある VM のインポート」の未修正の欠陥も悪用
- **何が起きたか (前回からの差分)**:
  - Vates の advisory (VSA-2026-062) では、認証回避の修正版が XO 6.9.2 (stable) と 6.10.1 (latest) になった。前回紹介した 6.9.1 / 6.10.0 から変わっている。
  - Vates によると、同じ攻撃者は 2 つ目の欠陥も使っていた。管理者の権限で細工した VM をインポートさせ、XCP-ng のホストを侵害するもので、修正はまだ開発中。CVE はどちらも採番されていない。
  - Vates は、不正なアクセスはログに残らないと説明している。侵害が確定した場合は、完全な再インストールを勧めている。WAF で空のトークンを止める緩和策も示した。
- **悪用 / PoC**: 悪用を観測 (Vates)。公開 PoC は確認できなかった。
- **なぜ重要か (評価)**: 1 つ目を直しても、盗まれた管理者のトークンや認証情報があれば 2 つ目を使える。更新と同時に、認証情報をすべて入れ替えたい。
- 出典: [SecurityWeek (2026-11-11)](https://www.securityweek.com/critical-xen-orchestra-flaws-exploited-in-attacks/) / [Vates VSA-2026-062](https://docs.vates.tech/security-advisories/advisories/2026/vates-sa-2026-062/)

### [2026-11-10〜11] Fortinet、89 件の advisory で約 100 件を修正。Critical は約 17 件。FortiClient の CORS の設定ミスで、Web ページを開くだけでコードが実行される「Fortinet2Shell」も
- **何が起きたか**:
  - Fortinet は 11/10 に 89 件の advisory を出し、約 100 件の脆弱性を修正した。Critical は約 17 件で、FortiMail が最も多い。続いて FortiAuthenticator、FortiOS、FortiManager、FortiAnalyzer、FortiSASE、FortiClient。認証回避、別の VDOM へのアクセス、IBE の Webmail のセッションの乗っ取り、スーパー管理者としてのコマンド実行などが含まれる。
  - Baldur Security の Kevin Joensen 氏によると、FortiClient の欠陥は FortiPAM が有効な場合に使える。原因は CORS の設定ミスで、攻撃者のページからローカルのサービスに通信でき、確実に任意のコードを実行できる。氏はこれを「Fortinet2Shell」と呼んでいる。
  - Fortinet は 3 週間前、製品のセキュリティテストに最先端の AI モデルを取り入れたと発表していた。今回の大量の修正は、その流れの中で出たもの。
- **悪用 / PoC**: Fortinet は悪用に触れていない。公開 PoC は確認できなかった。
- **なぜ重要か (評価)**: Fortinet の製品は、修正から悪用までが短い。FortiMail と FortiOS の Critical を最優先にしたい。「ローカルのサービス + CORS」の問題は、エンドポイントのエージェント製品の診断でよく見つかる型でもある。
- 出典: [SecurityWeek (2026-11-11)](https://www.securityweek.com/fortinet-patches-nearly-100-vulnerabilities/)

### [2026-11-10〜11] その他の定例の修正: Ivanti EPM の未認証の SQLi で RCE (CVE-2026-121653、9.8)、Zoom Workplace for Windows の未認証の権限昇格 (CVE-2026-108186、9.6)、Citrix XenServer で Pool Secret を推測される欠陥
- **何が起きたか**:
  - Ivanti は 5 製品で 13 件を修正した。Endpoint Manager (EPM) の CVE-2026-121653 は、未認証の SQL インジェクションで RCE につながる (2024 SU8 で修正)。Cloud Services Application の CVE-2026-121683 (9.4) は、未認証で EPM Core の信頼する証明書を追加・削除できる (5.0.8.1 で修正。Dual NIC 構成なら外からは使えない)。Sentry と EPMM の RCE (CVE-2026-105425、High) も。
  - Zoom は Workplace for Windows の 2 件を修正した。CVE-2026-108186 (9.6、入力検証の不備、7.1.0 以上 7.1.8 未満) と CVE-2026-108187 (8.1、送信元の検証の不備、7.1.5 未満)。どちらも、未認証でネットワーク経由で権限を上げられるとされる。修正版は 7.1.8 以降。
  - Citrix は XenServer の 6 件を修正した。CVE-2026-102705 (High) は Pool Secret を推測されてホストを乗っ取られるおそれがある。AMD の CPU の脆弱性 (ゲストからホストへの影響) の緩和も含まれる。
  - Asus はルーターのファームウェアの 4 件 (root でのコマンド実行を含む) を修正した。
- **悪用 / PoC**: 各社とも悪用はないと説明している。公開 PoC は確認できなかった。
- **なぜ重要か (評価)**: Ivanti EPM は過去に、未認証の SQLi が修正後すぐに KEV に入ったことがある。外から届く EPM と CSA は、ほかより先に更新したい。Zoom は advisory が短く、「ネットワーク経由」が何を指すのかは書かれていない。
- 出典: [SecurityWeek (Ivanti / Citrix、2026-11-11)](https://www.securityweek.com/citrix-ivanti-patch-critical-and-high-severity-vulnerabilities/) / [The Hacker News (Zoom、2026-11-11)](https://thehackernews.com/2026/11/critical-zoom-workplace-flaw-could.html) / [SecurityWeek (Asus / Zoom、2026-11-11)](https://www.securityweek.com/asus-zoom-release-security-patches/)

### [2026-11-10〜11] ICS の Patch Tuesday: Siemens が 9 件の advisory を公開。うち 2 件は Node2Shell の影響で、一部の製品には修正版が出ない
- **何が起きたか**:
  - Siemens は 9 件の新しい advisory で 10 件の脆弱性を公表した。2 件は Node2Shell (Brotli) の影響で、ほかは ROS#、Simcenter Femap、Mendix Studio Pro の MCP サーバー、Simatic の SCADA と PCS 7、WinCC Graphics Designer などの High。修正版がまだない製品や、修正が出ない版もあり、緩和策を勧めている。
  - VDE CERT は 8 件 (Beckhoff、MB Connect Line、Helmholz、Weidmueller など) を公開した。PHP2Shell のような外部の部品の影響が多い。Phoenix Contact と Hitachi Energy も PHP2Shell の影響を公表した。Schneider Electric は 1 件 (Medium)。
- **悪用 / PoC**: Node2Shell は悪用の試みが観測されているが、Siemens の製品が狙われた形跡はないとされる。
- **なぜ重要か (評価)**: Web の部品 (Node / PHP) の欠陥が、数週間遅れて OT の製品に波及している。OT の資産の台帳と SBOM で、Brotli や PHP の版を確認できるようにしておきたい。
- 出典: [SecurityWeek (2026-11-11)](https://www.securityweek.com/ics-patch-tuesday-siemens-flags-high-severity-flaws-node2shell-exposure/)

### [2026-11-11] [続報] eMudhra、「影響はない」としていた RSA の中間 CA 8 個も失効。Microsoft は 11/16 から残りのルート 10 個を外し、Ubuntu 26.10 の curl は CRLite で失効を確認するように
- **何が起きたか (前回からの差分)**:
  - eMudhra が Mozilla の bug tracker に出した最終報告によると、問題は 2025 年 4 月 30 日の鍵のセレモニーで始まった。Utimaco の HSM から Crypto4A の HSM へ鍵を移すため、社内の Python スクリプトが鍵をいったん HSM の外のメモリに読み出して作り直していた。その読み戻しの 1 行で、ECDSA の秘密値が先頭の 1 バイトに切り詰められた。
  - RSA の 8 個 (TLS 用 6、コード署名用 2) は、鍵そのものは弱くなっていない。しかし、秘密鍵の一部がセレモニーの PC の Python のプロセスのメモリに置かれていた。eMudhra は、自社の CPS §6.2.6 の基準を守っていたと示せないとして、先週末に失効させた。対象の証明書は 195 枚。理由コードは keyCompromise ではなく cessationOfOperation で、これには疑問が出ている。
  - Microsoft は 11/16 から emSign Root CA - G1 を含む残りのルート 10 個を外す。macOS 27.2.1 などは、curl や git が侵害された CA を受け付けないようにした。Cisco と SonicWall も、影響のあるルート証明書を自社製品から外した。
  - Ubuntu 26.10 の curl は、rustls の開発者による「upki」を使って、端末に置いた CRLite のデータで失効を確認するようになった。データは 6 時間ごとに更新される。27.04 では OpenSSL に組み込む予定。
- **悪用 / PoC**: 弱い鍵の悪用は確認されていない (eMudhra)。秘密値は公開の証明書から復元でき、前回までに公開されている。
- **なぜ重要か (評価)**: OpenSSL の初期設定では失効を確認しないため、ブラウザ以外のツールは失効した証明書を信用し続けた。Ubuntu の変更は、その穴を OS の側で埋める初めての動き。診断の環境や CI の trust store が、まだ emSign を信用していないか確かめたい。
- 出典: [The Hacker News (2026-11-11)](https://thehackernews.com/2026/11/emudhra-revokes-8-more-cas-it.html) / [Help Net Security (2026-11-11)](https://www.helpnetsecurity.com/2026/11/11/ubuntu-certificate-revocation-curl-openssl/) / [SecurityWeek (Cisco / SonicWall、2026-11-11)](https://www.securityweek.com/asus-zoom-release-security-patches/)

### [2026-11-11] Maersk、買収した LF Logistics の系統のシステムへの侵入を認める。WhiteArmor が 100GB の窃取を主張し、500 万ドルを要求
- **何が起きたか**:
  - ランサムウェアの WhiteArmor は週末にリークサイトに Maersk を載せ、30 日以内に 500 万ドルをビットコインで払うよう求めた。2022 年に買収した LF Logistics の OCF/LF Logistics のプラットフォームから、約 100GB を盗んだと主張している。
  - WhiteArmor が持っていると主張するのは、運転手約 3 万人分の記録、平文のパスワード、33 個の SUPER_ADMIN のアカウント、署名入りの受領書、モバイル端末の記録 2 万 7,842 件 (電話番号、メール、IMEI) など。
  - Maersk は、侵害は「ローカルのシステム」に限られ、機微なデータは流出していないと説明している。API や EDI でつながるほかのシステムへの影響もないとしている。
- **悪用 / PoC**: 侵入の手口は非公開。
- **なぜ重要か (評価)**: 買収した会社のシステムが本体とは別に管理され、手薄になっている例。データの中身は攻撃者の主張で、裏付けはない。物流のサプライチェーンの取引先は、Maersk を名乗る不審な連絡に注意が必要。
- 出典: [BleepingComputer (2026-11-11)](https://www.bleepingcomputer.com/news/security/maersk-confirms-data-breach-as-whitearmor-ransomware-demands-5-million/)

### [2026-11-10〜11] ポーランド、行政手続きの基盤「ePUAP」をサイバー攻撃の検知を受けて停止。電子署名の「Trusted Profile」にも影響のおそれ
- **何が起きたか**: ポーランドのデジタル担当相は、国の電子行政の基盤 ePUAP への攻撃を「検知し、止めた」と発表した。省の報道官によると、システムが侵害されたわけではなく、念のため止めたという。電子の郵便受けは使えない状態で、本人確認と電子署名の Trusted Profile にも影響が出うる。手口、攻撃者、復旧の見通しは公表されていない。
- **悪用 / PoC**: 手口は非公開。
- **なぜ重要か (評価)**: ポーランドでは、9 月の MyDr (約 1,900 万人分) など、大きな事故が続いている。国の ID と署名の基盤が止まった影響は大きく、続報を待ちたい。
- 出典: [The Record (2026-11-11)](https://therecord.media/poland-shuts-down-government-services-platform-cyberattack)

### [2026-11-11] iVerify の年次報告: 流出した iOS のエクスプロイトキット「DarkSword」「Coruna」が犯罪者の手に。Instagram の広告や、期限切れのドメインを買い取った「DeadTag」の配信網から感染
- **何が起きたか**:
  - iVerify の 2026 Advanced Mobile Threat Report によると、3 月に公開された DarkSword は、1 週間以内に新しい版が GitHub に出回った。犯罪者のグループがこれを使っている。Instagram の広告を読み込んだだけで感染が始まった例もある。
  - Report URI の Scott Helme 氏が報告した「DeadTag」は、EC サイトの分析用の期限切れのドメインを買い取っていた。テンプレートに残った参照から、訪問者のブラウザに自分のスクリプトを読み込ませていた。誘導先の偽の暗号資産サイトは、iOS 18.4.0〜18.7.2 の Safari のときだけ DarkSword を起動した。再登録されたドメインは 660 以上、関係するサイトの訪問は月 1 億 3,500 万回とされる。
  - DarkSword はキーチェーンの認証情報を、Coruna は画像や文章の中の暗号資産のリカバリーフレーズを盗む。再起動や OS の更新で痕跡が消えやすい。iVerify は、感染を確認した端末に Apple の脅威通知が届いた例を知らないとしている。
- **悪用 / PoC**: 実際の感染を観測 (iVerify)。エクスプロイトのコードは流出し、公開されている。
- **なぜ重要か (評価)**: 国家向けの iOS のエクスプロイトが、ばらまき型の犯罪に下りてきている。業務で使う私物の iPhone は、MDM で OS の版を強制できない限り、侵入の入口になりうる。期限切れのドメインを参照したままのテンプレートは、Web の診断で指摘すべき項目。
- 出典: [Help Net Security (2026-11-11)](https://www.helpnetsecurity.com/2026/11/11/iverify-iphone-exploit-kit-attacks-report/)

### [2026-11-11] Unit 42、ブラウザの中だけで動く C2「Falcon」(XG) を報告。中東と東南アジアの政府系の Webmail とサイトに JavaScript を埋め込み、訪問者を狙う
- **何が起きたか**:
  - Unit 42 によると、攻撃者は 2026 年 3〜5 月に、中東 1 か国と東南アジア 4 か国の外務、国防、内務の省庁や法執行機関の Webmail と Web アプリに、悪意のある JavaScript を直接埋め込んだ。訪問者のブラウザで Falcon の実装が動き、悪意のある Chrome 拡張を入れさせて情報を盗んだ。OneDrive を C2 に使う「Antino」の配布にも使われた。
  - Falcon は Node.js 製。管理画面は空白のページに見え、F9 を 3 回押すまでログインの画面が出ない。被害者向けのポートの初期ページは、テトリスやスネークのゲーム。実装はセッションごとに 1 バイトの XOR で難読化され、Baidu の分析の Cookie を真似た `Hm_lvt_` を ID に使う。
  - Unit 42 は、Trend Micro が 1 月に報告した「PeckBirdy」と、URL の構造、配信の手順、通信の方式がほぼ同じとして、同じフレームワークの派生と高い確度で評価している。
- **悪用 / PoC**: 実際の攻撃を観測 (Unit 42)。
- **なぜ重要か (評価)**: 端末にマルウェアを置かずブラウザの中だけで動くため、EDR に見えにくい。Webmail などの公開のアプリでは、配信している JavaScript の改ざん検知 (SRI、ハッシュの監視) が対策になる。
- 出典: [Unit 42 (2026-11-11)](https://unit42.paloaltonetworks.com/falcon-c2-browser-compromise/)

### [2026-11-11] Krebs、ランサムウェア「Qilin」の管理者「Haise」をサンクトペテルブルクの 36 歳の男性と特定。押収された RAMP の DM と、Gosuslugi の流出データから
- **何が起きたか**:
  - Qilin は直近 3 か月で少なくとも 365 組織を被害者として公表した、最も活発な RaaS (NCC Group の報告)。KrebsOnSecurity は、管理者 Haise の古いハンドル「Rjun」と Telegram の名前「Alexbigboss44」を手がかりにした。Intel 471 が持つ RAMP (2026 年 1 月に FBI が押収) の DM、Flashpoint、SpyCloud、Constella のデータでたどり、2025 年末に流出したロシアの行政サイト Gosuslugi の記録で人物を特定した。
  - 最初の結び付けは、ハンドルの履歴や文体から匿名の人物を特定する AI の基盤「IntelHawk」によるもの。
- **悪用 / PoC**: 該当なし (脅威アクターの調査)。
- **なぜ重要か (評価)**: 押収されたフォーラムのデータと過去の流出データを組み合わせると、何年も前の運用の甘さから人物を特定できる例。特定は報道の段階で、起訴などはまだない。
- 出典: [KrebsOnSecurity (2026-11-11)](https://krebsonsecurity.com/2026/11/who-runs-the-ransomware-group-qilin/)

### [2026-11-11] Pall Mall Process、商用のハッキング企業向けに初めての行動指針を採択。日米英仏独伊など 14 か国が支持したが、法的な拘束力はない
- **何が起きたか**: 英国とフランスが主導し、スパイウェアなどの「商用のサイバー侵入能力 (CCIC)」の拡散を抑えるための Pall Mall Process は、3 回目の会合で企業向けの指針を採択した。開発、販売、出資をする企業に、顧客の審査、悪用を防ぐ技術的な仕組み、悪用の監視と報告を求める。深刻な悪用のおそれがあれば、販売とサポートを止めることも求めている。参加 43 か国のうち、支持は 14 か国。罰則はなく、実効性は調達や輸出許可を持つ政府の圧力しだい。
- **悪用 / PoC**: 該当なし (政策)。
- **なぜ重要か (評価)**: エクスプロイトの販売や Red Team のツールを扱う企業には、顧客の審査や悪用の監視を求める基準が、輸出管理とは別に出てきた。日本も支持国に入っている。
- 出典: [The Record (2026-11-11)](https://therecord.media/britain-france-set-out-guidelines-for-commercial-hacking-firms)

### [2026-11-11] PortSwigger、CSP の回避を自動で調べる Burp AT のスキルを公開。JavaScript が全部止められていても、form-action 'self' と meta refresh で認証情報を Referer から持ち出せる
- **何が起きたか**:
  - スキルは CSP に 2 つの確認をする。1 つは、許可されたスクリプトの読み込み元に、既知の回避のガジェット (JSONP、古い AngularJS など。cspbypass.com の 350 件超) があるか。もう 1 つは、注入したフォームで認証情報を持ち出せるか (form-action が 'self' のときに注入したフォームから、ページ自身に情報を送らせる手口)。
  - PortSwigger は、JavaScript が完全に止められた一見きびしい CSP でも、認証情報が Referer を経由して外に出うることを示した。スキルは対象のパラメーターを見つけ、Burp Collaborator への PoC を自動で組み立てる。検証用の脆弱なページも公開されている。
- **悪用 / PoC**: 研究目的の PoC を公開 (Burp AT のスキルと検証用ページ)。実際の悪用の報告はない。
- **なぜ重要か (評価)**: 「default-src 'none' だから安全」という思い込みへの反例。CSP を書くときは form-action と、許可リストに載せたドメインが何をホストしているかまで確かめたい。Web 診断の CSP の評価の自動化にも使える。
- 出典: [PortSwigger Research (2026-11-11)](https://portswigger.net/research/blind-trust-stealing-credentials-through-csp)

### [2026-11-11] Microsoft FORGE Lab、AI のスキャナー「MDASH」で Linux カーネルを調査。2 週間で 26,502 件の生の指摘から、59 件の報告・33 件の CVE・8 件の root 昇格の動く PoC にまで絞り込む
- **何が起きたか**: Microsoft の FORGE Lab は、5 月末〜6 月中旬に Linux カーネルの一部 (ネットワーク、ファイルシステム、セキュリティモジュール) を MDASH でスキャンした。2 週間で 26,502 件の生の指摘が出て、専任 1 名とインターン 1 名が数か月かけて 11,769 件の候補に絞り、最終的に 59 件の upstream 報告、33 件の CVE、38 件の mainline への修正、8 件の root 昇格の動く PoC になった。コードのスキャンは Sonnet 4.6 / GPT-5.4 / GPT-5.5 を使用。
- **悪用 / PoC**: 研究者が内部で PoC を作成 (8 件の CVE で root 昇格を確認)。悪用の報告はない。
- **なぜ重要か (評価)**: AI のスキャナーの「生の指摘」の大半はノイズで、CVE と修正にするには人の手が要る、という現実的な数字が出ている。ソースコード診断で AI を使う側にも、トリアージの工数の見積もりの参考になる。
- 出典: [Microsoft Security Blog (2026-11-11)](https://www.microsoft.com/en-us/security/blog/2026/11/11/lessons-from-59-linux-kernel-bug-reports/)

---

## 新規 CVE / Advisory (バリアントハント起点候補)
> 採用基準: 公開日 2026-11-10 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-125755 / GHSA-3q53-mvfw-q9v8, CVE-2026-125756 / GHSA-jh3p-792r-98gm | Nodemailer (3.0.0 – < 10.4.1) / postal-mime (< 4.2.1) | CWE-436 / 8.3・8.2 | RFC 5322 のアドレスパーサーが、ドメインの途中 (`.` の前) にある folding whitespace やコメント `(...)` で、ドメインを途中で切ってしまう → アプリの宛先ドメインの許可リストや DMARC の alignment の判定と、実際の配送先・表示上の送信者が食い違う → Nodemailer は送信元の名義で攻撃者の宛先に配送してしまい、postal-mime は SPF/DKIM/DMARC を通った From を別の送信者 (なりすまし) として報告する | [diff](https://github.com/nodemailer/nodemailer/commit/c2b9c41bb81b2294ebadd294ad15ff035a17d0a5) / [diff](https://github.com/postalsys/postal-mime/commit/646725704463839f233472453b7c8306bd1dde21) | 公開 11/10 (修正版も 11/10 に npm へ公開) / EPSS 未算出・KEV なし / 仕様 (RFC 5322 の CFWS) から来る parser differential。同じ作者の 2 つのライブラリが同時に直されたので、他の言語のメールアドレスパーサーにも同じ癖がありそう |
| CVE-2026-115559 | CPython `imaplib` (修正コミット 22d79d9 より前) | CWE 未付与 / 6.3 | `IMAP4.starttls()` が TLS に切り替えるとき、自前の先読みバッファ `self._readbuf` を捨てない → STARTTLS への tagged OK と同じ `recv()` で届いた平文の行が、TLS 確立後の最初の応答として `readline()` から返る → MitM が偽の CAPABILITY や、次のコマンドへの偽の tagged 完了応答を注入できる (CVE-2011-0411 と同じ STARTTLS 注入の型) | [diff](https://github.com/python/cpython/commit/22d79d9840a275ed6ed36cd590dc74edc61765fb) ([PR](https://github.com/python/cpython/pull/160370)) | 公開 11/10 (PSF) / EPSS 未算出 / 「TLS へ切り替える前のバッファを捨てない」型。`smtplib`・`poplib`、ほかの言語の IMAP/SMTP/XMPP クライアント、サーバー側の STARTTLS でも同じ点を確認する価値がある |
| CVE-2026-88823, CVE-2026-95692 | OpenSSL 3.5 / 4.0 / 4.1 (AES-GCM-SIV、default provider) | CWE-325・CWE-125 / Low | 88823: AAD を分割して渡すとき、長さ 0 の AAD の update を「それまでに渡した AAD 全体のリセット」として扱う → それより前の AAD がタグの計算から外れる → AAD を偽造できる。95692: IV のコピー長に、呼び出し側が渡した長さではなく規定の nonce 長 (12) を使う → 短い IV では heap の OOB read、長い IV では後ろが黙って捨てられる → IV に束縛されないタグになる | [diff](https://github.com/openssl/openssl/commit/159e1de0c448d7b9f09ad768c8e141def4aa1eb4) / [diff](https://github.com/openssl/openssl/commit/257a3427aa0ef8d9dd2ef5b3e2d1c021a221b116) | 公開 11/10 ([secadv 20261110](https://openssl-library.org/news/secadv/20261110.txt)、修正版のリリースは 12/1 予定) / FIPS モジュールは影響なし / AEAD の「長さ 0 の入力」「長さが規定と違う IV」という境界は、BoringSSL・wolfSSL・ring・Go の x/crypto などの AES-GCM-SIV 実装でも共通のテスト項目 |
| CVE-2026-95691 (+ CVE-2026-88822) | OpenSSL 3.5 / 4.0 / 4.1 (QUIC クライアント) | CWE-416 (+ CWE-457) / Low | CRYPTO ストリームの先頭フレームのバッファへのポインタを TLS 層に貸し出している間に、そのフレームを完全に覆う再送 CRYPTO フレームが届くと、元のバッファを解放してしまう → TLS の処理が解放済みのメモリを読む (UAF)。悪意のあるサーバーがクライアントを DoS でき、heap の 1 バイトを推測できる。88822 は、`getpeername()` に IPv6 を収められない長さを渡し、返ってきた長さをそのまま信用する → 未初期化のスタックを宛先アドレスとして使って送信する | [diff](https://github.com/openssl/openssl/commit/dd90ceb99a3c2ddba336bb4a00be9ebabd84c2a1) / [diff](https://github.com/openssl/openssl/commit/1a73dc590cbad62d6f0329ea4779eadaa8d8fd75) | 公開 11/10 / 同じ日に Meta の mvfst も、CRYPTO フレームの扱いの CVE-2026-119236 (handshake を終えた暗号化レベルの CRYPTO データを、バッファの上限に数えずに保持し続けるメモリ枯渇, [diff](https://github.com/meta/mvfst/commit/7e5cff58e8cbed87793141ceeca0a8a343c67c44)) を公開した。QUIC の「CRYPTO フレームの重複・再送・古い暗号化レベル」の扱いは、quiche・ngtcp2・quic-go・msquic などでも横断して見る価値がある |
| CVE-2026-125371 | Tinyproxy (≤ 1.11.3) | CWE-187 / 6.3 | `acl_string_processing()` が、ホスト名の ACL を末尾の文字列の一致だけで判定し、DNS ラベルの境界 (`.`) を確認しない → 攻撃者が PTR を制御できる `untrusted.net` が `Allow trusted.net` に一致する → deny-by-default のプロキシを使えてしまう | [diff](https://github.com/tinyproxy/tinyproxy/commit/3991ac8f98c6a9f05b3265018b812dbf2ca92c28) | 公開 11/10 (NVD / OSV) / EPSS 0.0028 / 修正版は未リリース (コミットのみ) / 「ドメインを `endswith` で比べる」という古典的な型。SSRF の許可リスト、CORS の Origin 判定、Cookie の domain 判定にも同じ型がある |
| CVE-2026-126777 | Traccar (3.15 – < 6.17.0、LDAP 認証が有効な場合) | CWE-287 / 9.1 | `LdapProvider.login()` が空のパスワードを拒否しないまま LDAP の bind に渡す → ディレクトリが unauthenticated bind (RFC 4513 5.1.2) を許していると bind が成功する → ユーザー名さえ分かれば、`POST /api/session` や Basic 認証で管理者を含む任意のアカウントとしてログインできる | [diff](https://github.com/traccar/traccar/commit/552c31f2097dbed9edef7cfe174c50b16febdc21) | 公開 11/11 (修正版 6.17.0 は 11/01 に Docker Hub で公開済み) / EPSS 未算出 / LDAP 連携する認証の典型的な落とし穴。Java の JNDI や python-ldap、ldapjs で自前に bind する製品は軒並み確認対象 |
| CVE-2026-126065 / GHSA-7w4v-2c9r-q94v | OpenObserve (< 1.1.0) | CWE-287 / 9.8 | 共通の認証 validator (`auth/validator.rs`) が、`password_ext` が空のアカウント (SSO で作ったユーザーや移行で作ったユーザー) について、空や空白だけの Basic 認証のパスワードを受け入れる → メールアドレスと org を知っていれば、そのユーザーの権限で API を使える → 検索権限があれば DataFusion の `COPY ... TO` で任意のファイルを書けるので、条件付きで認証前 RCE | [diff](https://github.com/openobserve/openobserve/commit/46678ea8daba94c3904286471794f80c5a74ecea) | 公開 11/10 (GitHub CNA。修正版 v1.1.0 は 10/14 に公開済み) / EPSS 未算出 / 「SSO 専用のユーザーはパスワードのハッシュが空」という状態の扱い。SSO とローカル認証を併用する SaaS やセルフホスト製品で共通の確認項目 |
| CVE-2026-125742 | 7-Zip (< 26.06) | CWE-787 / 8.5 | 複数ボリュームの CAB で、続きのボリュームが前より小さい LZX のウィンドウを宣言すると、古い `_pos` が残ったまま範囲チェックを通る → LZX デコーダーで heap の範囲外に書き込む → 展開させるだけでコード実行 | [diff](https://github.com/ip7z/7zip/commit/d3296e39e1f1f92c7b41c0c3848e65640428d42d) | 公開 11/10 / EPSS 未算出 / [解説記事](https://potion-brew.pages.dev/posts/7zip-cab-lzx-window-desync-rce/)あり / 「ストリームの途中でパラメーターが変わるのに、状態を作り直さない」型。libarchive・libmspack・cabextract などの LZX/CAB 実装も同じ点を確認したい |
| CVE-2026-125396 | Ghostscript (< 10.08.0) | CWE-648 / 8.5 | `gs_fonts.ps` の `.putgstringcopy` が、オペランドの型を確認しないまま特権オペレーター `.forceput` を呼ぶ → わざと型エラーを起こし、独自のエラーハンドラーで `.forceput` を取り出す → save/restore をまたいだ UAF で `-dSAFER` を抜けて任意コード実行 | [diff](https://github.com/ArtifexSoftware/ghostpdl/commit/1484854e0c8ddfda1baa4ad4cd965b8a9790aa81) | 公開 11/10 / EPSS 0.0013 / 2018〜2019 年の `.forceput` 漏えい (CVE-2019-3839 など) と同じ系統。ImageMagick の delegate や、PDF/PS のサムネイル生成でアップロードを処理する Web アプリが攻撃の入口になる |
| CVE-2026-126779 | Spatie Browsershot (2.2.0 – < 5.5.0) | CWE-73 / 8.7 | `setHtml()` で渡した HTML を一時ファイルから `file://` として読み込むので、`/etc/passwd` のようなルートからの相対参照も `file://` として解決される → `<iframe>` `<img>` `<link>` `<script>` でサーバーのファイルを読み込み、PDF やスクリーンショットに描画する | [diff](https://github.com/spatie/browsershot/commit/eba71ab7f4aba23d9321d653ccd19d4e94432516) | 公開 11/11 (修正版 5.5.0 は 11/06 に Packagist で公開済み) / EPSS 未算出 / 「HTML を PDF にする機能」の定番の欠陥。Puppeteer・wkhtmltopdf・WeasyPrint のラッパー全般で、ベース URL やスキームがどう扱われるかを確認する |
| CVE-2026-123374 | Apache Roller (4.0 – 6.1.6) | CWE-502 / 未採点 | weblog の更新 ping を送る XML-RPC クライアントが、ping 先の応答に入っている Java のシリアライズオブジェクトをそのままデシリアライズする → ping 先 (の応答) を制御できる者が Roller のサーバーでコードを実行できる | [PR](https://github.com/apache/roller/pull/236) (commit 不明) | 公開 11/11 / 同じ日に Roller で XXE (CVE-2026-105153) や CSRF での管理者作成 (CVE-2026-118411) など 15 件ほどを公開 / Apache XML-RPC の `enabledForExtensions` (`<ex:serializable>`) は、クライアント側でも危険な sink。この古い型は、XML-RPC クライアントを持つ Java 製品でもう一度確認したい |

### 今日の CVE 所感
- **今日の本命はプロトコル仕様から来る 2 件**。Nodemailer / postal-mime (RFC 5322 の CFWS でドメインを切ってしまう) と CPython の imaplib (STARTTLS の前のバッファが残る) は、どちらも仕様の細部の取りこぼしで、他の言語や他の実装にもそのまま広がりうる。メールアドレスのパーサー (Go の `net/mail`、Python の `email.headerregistry`、Java の JavaMail) で `a@evil(x).victim.com` のような入力を差分テストし、STARTTLS のクライアントで「切り替え時にバッファを捨てているか」を確認したい。
- **OpenSSL と mvfst が同じ日に QUIC の CRYPTO フレームの扱いを直した**。重複・再送・古い暗号化レベルの CRYPTO データの扱いは、実装ごとに独自の書き方になる。ほかの QUIC スタックでも、この 3 つの観点で横断して確認する価値がある。AES-GCM-SIV の 2 件は、長さ 0 の AAD と長さが規定と違う IV という、AEAD のテストで必ず見る境界の取りこぼし。
- **認証では「空のパスワードを受け入れる」型が 2 件**。Traccar (LDAP の unauthenticated bind) と OpenObserve (SSO 由来でパスワードのハッシュが空のユーザー) は、診断で `password=` を空にして送る 1 回のリクエストで見つけられる。どちらも、修正版が出てから数週間たって CVE が公開されているので、パッチを当てていない環境が残っている可能性が高い。
- **TLS 検証の既定値・取りこぼしも続いた**。V 言語の `net.http` は `validate` の既定が false (CVE-2026-82509, [diff](https://github.com/vlang/v/commit/40774847a949722f5d090706c050b806ceeacfd1))、MongoDB の macOS 版の SecureTransport は、相手が IPv6 のとき `SecTrustEvaluate` の結果を捨てていた (CVE-2026-120808)。「アドレスの種類で分岐する検証コード」は、ほかの TLS ラッパーでも狙い目になる。
- **ファイル処理系 (7-Zip の LZX、Ghostscript の `.forceput`、Browsershot の `file://`) はアップロードを処理するサーバーで発火する**。Web アプリの診断では、アーカイブの展開、PDF/PS の変換、HTML の PDF 化を裏で呼んでいないかを最初に確かめたい。


## 日本国内のセキュリティ動向

### 国内インシデント・事故

#### [2026-11-10] 日本商工会議所: 簿記などの「ネット試験」の管理システムに不正なプログラムが置かれ、最大約 98 万人分 (約 197 万件) の受験者情報が漏えいしたおそれ
- **何が起きたか**: 日本商工会議所は 11/10、ネット試験で使っている外部サーバー (試験管理システム) が不正アクセスを受けたと発表した。11/4 にシステム管理会社からの報告で気づいた。11/1 に不正なプログラム (不正ファイル) が置かれていたという。ファイルはすぐに消し、脆弱性への対策 (パッチの適用) も済ませた。11/9 に漏えいのおそれが分かり、同日に個人情報保護委員会へ報告した。対象は、2022/4/1〜2026/11/4 に簿記、販売士、日商 PC、電子会計実務、日商プログラミング、日商ビジネス英語などのネット試験を受けた人。項目は氏名、フリガナ、性別、生年月日、合否、得点と、任意で入れたメールアドレス、電話番号、住所。決済の情報は含まれない。どの脆弱性が使われたか、システムを作った会社はどこかは公表されていない。
- **なぜ重要か (評価)**: ファイルを置かれてから気づくまで 3 日だった。パッチで直したと書いているので、既知の脆弱性を放置した外部公開サーバーが入口だった可能性が高い。試験の予約・結果の管理のように委託先が運用する周辺システムも、外部診断と Web シェルの検知の対象に入れるべきだ。
- 出典: [日本商工会議所 (2026-11-10)](https://www.jcci.or.jp/news/news/2026/1110170000.html) / [商工会議所の検定試験 (2026-11-10)](https://www.kentei.ne.jp/51816) / [ITmedia NEWS (2026-11-11)](https://www.itmedia.co.jp/news/article/2611/11/2000003084/)

#### [2026-11-11] 靖國神社: 通販サイト「オンライン授与品・頒布品サイト」に不正アクセス。会員約 1 万 4,500 件の氏名、メールアドレス、ハッシュ化したパスワードとソルトが漏えい
- **何が起きたか**: 靖國神社は 11/11、自身が運営する通販サイトが外部から不正アクセスを受け、会員情報が漏えいしたと発表した。漏れたのは、氏名、メールアドレス、ハッシュ化したパスワードとその生成に使う補助情報 (ソルト)、登録日時などの管理情報で、約 14,500 件 (調査中で変わりうる)。神社は「元のパスワードを第三者が特定するおそれがある」としている。カード番号、住所、電話番号、購入履歴は、11/11 時点で漏えいが確認されていない。カード決済は決済代行会社の画面で行う仕組みだという。10/28 に気づき、同日にサイトを止めた。原因はサイト管理会社と調べている。
- **なぜ重要か (評価)**: 「ハッシュとソルトが漏れたので元のパスワードを特定されうる」と書いているので、低速なハッシュ (bcrypt / Argon2 など) を使っていなかったおそれがある。小さな通販サイトの診断では、パスワードの保存方式も確認したい。
- 出典: [靖國神社 (2026-11-11)](https://www.yasukuni.or.jp/news_detail.html?id=734) / [ITmedia NEWS (2026-11-11)](https://www.itmedia.co.jp/news/article/2611/11/2000003119/)

#### [2026-11-09 公表 / 11-11 報道] エディオン: EC サイトの決済処理に不正なプログラムが組み込まれ、PC から入力されたカード番号とセキュリティコードが最大 556 回分漏えいしたおそれ。エラーログにもカード情報が残っていた
- **何が起きたか**: エディオンは 11/6 の第 1 報で、EC サイトのログファイルを保存するサーバー領域に、システムの脆弱性を突いた不正アクセスがあったと発表していた (最大 4,131 人の個人情報と 9,554 人分の注文情報)。11/9 の続報で、次のことが新たに分かった。
  - PC 向けの決済情報の入力処理に不正なプログラムが組み込まれ、11/4 19 時過ぎから動いていた。新しく入力されたカード番号、有効期限、名義、セキュリティコードが最大 556 回分漏れたおそれがある。スマートフォンからの入力は対象外だった。
  - 注文画面でエラーが起きたとき、入力内容がシステムログに一時的に記録されていた。そこからカード情報最大 5 件が漏れたおそれがある。ほかに、エディオンギフトカード 5,360 枚 (番号、PIN、利用履歴) と、ログイン ID とパスワード最大 1,141 人分も対象。
  - カード情報をサーバーに残さない仕組みをとっていたため、第 1 報ではカード番号を対象に含めていなかった。11/7 22 時から EC サイトとアプリ 2 本を止めており、再開は未定。
- **なぜ重要か (評価)**: 非保持化をしていても、決済画面の JavaScript を改ざんされれば入力値は盗まれる。さらに、例外処理でログに入力値を書く実装が非保持化の穴になった。診断では、決済ページのスクリプトの改ざん検知 (CSP、SRI、ファイルの改ざん監視) と、エラーログにカード情報や PIN がマスクなしで出ていないかを確かめたい。
- 出典: [エディオン (2026-11-09, PDF)](https://www.edion.co.jp/system/files/news-release/pdf/ja/2026-11/20261109_pr_1_1.pdf) / [ITmedia NEWS (2026-11-11)](https://www.itmedia.co.jp/news/article/2611/11/2000003091/)

#### [2026-11-11] [続報] ユミルリンク: 「Cuenote FC」の流出件数を延べ 4,786 万 4,147 件に確定。脆弱性で不正なプログラムを置かれ、セッション情報を盗まれて管理画面からも持ち出された
- **前回から何が変わったか**: ユミルリンクは 11/11、10/26 時点で最大約 5,162 万件としていた流出件数を、延べ 4,786 万 4,147 件に改めた。被害を受けたのは Cuenote FC の 49 システム。内訳は、メールアドレス 4,786 万件、会員 ID 3,050 万件、氏名 666 万件、生年月日 94 万件、電話番号 41 万件など。ほかに住所、ハッシュ化したパスワード、会社名、学校名、**顧客が運用するサービスの認証情報** も含む。手口は 2 つ。システムの脆弱性を突いてサーバーに不正なプログラムを置き、データベースに入った。さらに利用者のログイン状態を示す情報 (セッション) を盗み、正規の利用者として管理画面からデータを持ち出した。再発防止として、AI を使ったソースコードレビューと 24 時間 365 日の監視を入れる方針。外部機関の最終調査の後に、改めて結果を出す。利用企業ではアイスタイル (@cosme、約 280 万人) が 11/9 に、JR 東海など 3 社 (スマート EX など、計約 17 万件) が 11/5 に影響を公表している。
- **なぜ重要か (評価)**: 委託元のサービスの認証情報まで配信 ASP に預けられていた。委託元は、配信サービスに登録した API キーや連携の認証情報を、すぐに入れ替えるべきだ。
- 出典: [ユミルリンク (2026-11-11, TDnet PDF)](https://www.release.tdnet.info/inbs/140120261111572569.pdf) / [ITmedia NEWS (2026-11-11)](https://www.itmedia.co.jp/news/article/2611/11/2000003114/)

#### [2026-11-11] [続報] アララ「アララ メッセージ」の侵害が中央省庁に波及: 内閣府のメールマガジン 14 種で、メールアドレス計 6 万件超が漏えい
- **前回から何が変わったか**: 内閣府は 11/11、自身が出す 14 種のメールマガジンについて、利用者のメールアドレス計 6 万件超が漏えいしたと発表した。原因は、アララのメール配信サービスへの不正アクセス。主なものは「公益法人メールマガジン」(19,685 件)、「食品安全委員会 e-マガジン」(10,922 件)、「官民人材交流センターからのお知らせ」(5,400 件)。登録時に入れた氏名、所属、性別なども漏れたおそれがある。対象のメルマガは配信を止めている。アララは 11/6 に、流出したメールアドレスは重複を除いて 8,132 万 9,467 件、影響を受ける契約企業は最大約 380 社と推計していた。
- **なぜ重要か (評価)**: 官公庁の名前と配信先のリストが一緒に漏れたので、内閣府を名乗る精度の高いフィッシングにそのまま使える。省庁のメルマガ担当も、委託先 SaaS の侵害の当事者になる。
- 出典: [内閣府 (2026-11-11, PDF)](https://www.cao.go.jp/others/csi/security/20261111notice.pdf) / [ITmedia NEWS (2026-11-11)](https://www.itmedia.co.jp/news/article/2611/11/2000003105/)

#### [2026-11-10] GMO あおぞらネット銀行: 銀行 API の接続基盤への「外部からの不正な通信」を検知し、銀行 API を 2 回止めた。暗号資産交換業者の入金や freee の振込に影響
- **何が起きたか**: GMO あおぞらネット銀行は、銀行 API の接続基盤に外部から不正な通信が来たのを検知し、予防のために 11/10 20:42 から銀行 API を止めた。22:30 に再開したが、11/11 1:02 に再び不正な通信を検知して止め、6:25 に再開した。同行は、個人情報の漏えいや不正な資金の流出は起きていないとしている。通信の中身 (DDoS か、認証の試行か) は公表していない。この間、Binance Japan や Coincheck での同行経由の円の入金、freee の「freee振込」などが一時止まった。
- **なぜ重要か (評価)**: 銀行 API を止めると、つながる FinTech 側のサービスが一斉に止まる。API 連携の診断では、銀行側が止まったときの処理 (再試行、二重送金の防止、利用者への表示) も見るべきだ。
- 出典: [GMO あおぞらネット銀行 (2026-11-10、11/11 06:30 更新)](https://gmo-aozora.com/news/2026/20261110-01.html) / [ITmedia NEWS (2026-11-11)](https://www.itmedia.co.jp/news/article/2611/11/2000003087/)

#### [2026-11-10] [続報] 偽 TikTok アプリ (「TikTok18+」など) による遠隔操作と不正決済: 逮捕は福岡、兵庫、北海道の合同捜査本部によるもので、2 人の逮捕は 3 回目。全国の相談は 9 月末時点で約 1,600 件
- **前回から何が変わったか**: piyolog が 11/11 に関連情報をまとめた。前号で取り上げた逮捕は、福岡、兵庫、北海道の 3 道県警の合同捜査本部によるもの。中国籍の男 2 人 (31 歳と 33 歳) は 9/30 に最初に逮捕されており、11/10 の逮捕は 3 回目にあたる。容疑は、8/22〜9/23 に 30〜60 代の男性 4 人の電子決済サービスを不正に使い、トレーディングカードやゲーム機など計約 206 万円分を店からだまし取ったこと。手口は次のとおり。成人版をうたう「TikTok18+」やペットと話せるという「PetVox」などの偽アプリを、SNS の広告などから Android 端末に入れさせる。アクセシビリティ (ユーザー補助) の権限で端末を遠隔操作し、決済用のバーコードの画像を手に入れる。警察庁によると、全国の相談は 9 月末時点で約 1,600 件。PayPay は、特定のユーザー補助機能が有効なときに利用を一時的に制限することがあると説明している。
- **なぜ重要か (評価)**: 決済事業者の対策が、アクセシビリティ権限が有効かどうかで判断する方向に進んでいる。モバイル決済アプリの診断では、遠隔操作や画面の読み取りを検知できるか、オーバーレイを防げるかが項目になる。
- 出典: [piyolog (2026-11-11)](https://piyolog.hatenadiary.jp/entry/2026/11/11/094815)

#### [2026-11-10〜11] [続報] マイナンバーカードを使うコンビニ交付の障害: 原因は LGWAN 接続ルーターの故障で、サイバー攻撃ではないと自治体が説明。影響は 408 自治体
- **前回から何が変わったか**: J-LIS は、11/10 6:30 ごろから戸籍と戸籍の附票の証明書をコンビニで交付できない状態が続き、16:20 ごろに復旧したと告知した。共同通信によると、影響を受けたのは 408 自治体。J-LIS は通信障害とみて、不正アクセスの可能性は低いと説明した。うるま市は 11/11、原因はシステム提供元のネットワーク機器の上位にある「LGWAN 接続ルーターの故障」で、サイバー攻撃ではないとの報告を受けたと告知した。問題の機器は 11/10 23:30 以降に交換された。piyolog は 69 自治体の告知を確かめている。
- **なぜ重要か (評価)**: 攻撃ではなく、機器 1 台の故障で全国に広がった件だ。共通の基盤に冗長化がないことが、可用性のリスクとして見えた。
- 出典: [piyolog (2026-11-11)](https://piyolog.hatenadiary.jp/entry/2026/11/11/152720)

### 国内の注意喚起・ガイドライン・政策

#### [2026-11-11] IPA と JPCERT/CC: Microsoft の 11 月の月例更新について注意喚起。悪用済みの Outlook の CVE-2026-124194 を至急直すよう求める
- **何が起きたか**: IPA は「Microsoft 製品の脆弱性対策について (2026年11月)」を、JPCERT/CC は注意喚起 JPCERT-AT-2026-0035 を 11/11 に出した。どちらも、Microsoft が悪用を確認した CVE-2026-124194 (Outlook のなりすまし、CWE-356) を挙げている。細工したメッセージファイルを Outlook で開くと、いつもの警告が出ないまま攻撃者のサーバーにつながり、認証情報が漏れるおそれがある。IPA は「至急」更新を当てるよう求めている。
- **なぜ重要か (評価)**: 11/11 版で「未公開」と書いた国内の注意喚起が出そろった。更新の内容は前号の Patch Tuesday の項と同じなので、ここでは国内の注意喚起が出たことだけを記録する。
- 出典: [IPA (2026-11-11)](https://www.ipa.go.jp/security/security-alert/2026/1111-ms.html) / [JPCERT/CC (2026-11-11)](https://www.jpcert.or.jp/at/2026/at260035.html)

#### [2026-11-11] JPCERT/CC、「インシデント調査報告書チェックリスト」を GitHub で公開。外部の調査会社による調査の妥当性を、被害組織が評価するため
- **何が起きたか**: JPCERT/CC は 11/11、「インシデント調査報告書チェックリスト」を GitHub Pages で公開した。ランサムウェアや情報漏えいの調査を外部の調査会社に任せることが一般的になった。一方で、初めて被害に遭った組織は、調査が妥当か、インシデントが収束したかを判断しにくい。チェックリストは、調査を頼む被害組織と報告書を書く担当者が、同じ前提で調査を進めるためのものだという。
- **なぜ重要か (評価)**: 今秋の連続した漏えいでは、委託先の初報の「影響なし」が後で覆る例が相次いでいる (エディオン、ユミルリンクなど)。フォレンジックや報告書を作る側にとって、報告書に何が書いてあるべきかの目安になる。
- 出典: [JPCERT/CC (2026-11-11)](https://www.jpcert.or.jp/ir_report_checklist_20261111.html) / [チェックリスト (GitHub Pages)](https://jpcertcc.github.io/ir_report_checklist/)

#### [2026-11-10] 総務省、漏えいした個人情報の拡散を抑えるため、通信事業者による「ブロッキング」の是非を議論する作業部会を新設
- **何が起きたか**: 藤井比早之総務相は 11/10 の閣議後の会見で、サイバー攻撃で漏れた個人情報の拡散などの二次被害を防ぐ策を議論する作業部会を新しく作ると明らかにした。通信事業者が Web サイトへのアクセスを強制的に遮断する「ブロッキング」について、実施の是非と課題、法的な整理を検討する。作業部会は、10 月に初会合を開いた「通信事業者のサイバーセキュリティ対策の強化に向けた有識者検討会」の下に置き、11 月下旬にも初会合を開く。2027 年早々に中間とりまとめを行う方針。政府が 11/6 に出した緊急対策パッケージにも「アクセス抑止策の在り方について法的課題を含め早急に検討する」とある。憲法が保障する「通信の秘密」に触れる可能性も指摘されている。
- **なぜ重要か (評価)**: リークサイトへのブロッキングが制度になれば、通信の秘密の例外が初めて情報漏えいの対策に広がる。11/4 には NTT の社長も法制化を求めていた。
- 出典: [ITmedia NEWS (産経新聞の配信, 2026-11-11)](https://www.itmedia.co.jp/news/article/2611/11/2000003094/)

#### [2026-11-11 報道] 日本証券業協会と証券会社: パスキー (生体認証) を設定していた証券口座でも乗っ取りの疑い。Google / Apple のアカウントを乗っ取られ、同期されたパスキーを使われたとみられる
- **何が起きたか**: 共同通信によると、生体認証を使うパスキーで不正ログインに備えていた証券口座が乗っ取られた疑いがあり、日本証券業協会と証券会社が注意を呼びかけている。生体認証そのものが破られたのではない。パスワードの変更を求める偽メールで Google や Apple のアカウントの情報を入力させ、そのアカウントに同期されたパスキーを使ったとみられる。日証協は 10 月にガイドラインを改め、ログイン、出金、出金先の口座の変更でフィッシングに強い多要素認証を必須にする方針を示していた。
- **なぜ重要か (評価)**: パスキーを入れても、同期元のクラウドアカウントが乗っ取られれば守れない。金融系の診断や脅威モデルでは、同期パスキーの信頼の起点 (アカウント回復の手順、新しい端末の追加の通知) も範囲に入れるべきだ。注: 日証協の一次資料は未確認で、共同通信の記事に基づく。
- 出典: [Yahoo!ニュース (共同通信, 2026-11-11)](https://news.yahoo.co.jp/articles/62e65c5334cac8a825c36c33e1d4596f009f71f8)

#### [2026-11-11] トビラシステムズ: 「警察庁推奨アプリ」のダウンロードページを装う偽サイトに注意。「NPA」を名乗る SMS から、端末を乗っ取るアプリを入れさせる
- **何が起きたか**: トビラシステムズは 11/11、「NPA」(警察庁の英語の略) を名乗る SMS で「詐欺対策アプリ」を入れさせる偽サイトを確認したと注意を呼びかけた。リンクの先は警察庁推奨アプリのページを装っている。ダウンロードを押すと「Google Play」に見せかけた画面に移り、VPN の接続と端末の完全な制御の許可を求める。許可すると、スマートフォンを乗っ取られるおそれがある。実在する警察庁推奨アプリは、2026 年 3 月に認定された「詐欺対策 by NTTタウンページ」と「トレンドマイクロ 詐欺バスター Lite」の 2 本。
- **なぜ重要か (評価)**: 上の偽 TikTok アプリと同じく、Android で遠隔操作の権限を取る型だ。誘い文句が「詐欺対策」に変わっている。
- 出典: [INTERNET Watch (2026-11-11)](https://internet.watch.impress.co.jp/docs/news/2155633.html)

### 国内製品の脆弱性 (JVN)

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| 2026-11-11 | JVN#11786640 / CVE-2026-117687 | Movable Type 8.8.6 以前、8.0.13 以前、MT Premium 2.18 以前 (Advanced を含む) / シックス・アパート | ダイナミックパブリッシング機能で、細工したリクエストによりサーバー上で任意の PHP コードを実行される。サポートが終わった 8.4.x 系と MT7 も影響を受け、MT9 は影響なし。8.8.7、8.0.14、Premium 2.19 で修正。環境変数 `DynamicTemplateAllowPHP` の設定も推奨 | v4 6.9 / v3 7.3、未認証 (PR:N) でのコード実行 | [JVN](https://jvn.jp/jp/JVN11786640/) |
| 2026-11-10 (日立) / 11-11 (JVN iPedia) | JVNDB-2026-042613 / CVE-2026-115646 | HiRDB Server Version 10 / 9 (with Additional Function、32 ビット版を含む) / 日立 | 部分文字列比較の脆弱性 (CWE-187。認証やアクセス制御の判定に使う比較の不備とみられる) | v3 **9.8** (AV:N/PR:N) | [日立](https://www.hitachi.co.jp/Prod/comp/soft1/security/info/vuls/hitachi-sec-2026-165/index.html) / [JVN iPedia](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-042613.html) |
| 2026-11-10 (日立) / 11-11 (JVN iPedia) | JVNDB-2026-042617 / CVE-2026-91754〜91757 | Hitachi Dynamic Link Manager for VMware 7.3.0-00〜9.0.4-00 / 日立 | スタックバッファオーバーフロー、整数オーバーフロー、OS コマンドインジェクション 2 件 | v3 8.1 (ネットワーク経由、AC:H) | [日立](https://www.hitachi.co.jp/Prod/comp/soft1/security/info/vuls/hitachi-sec-2026-161/index.html) |
| 2026-11-10 (日立) / 11-11 (JVN iPedia) | JVNDB-2026-042612 / 042614 / 042616 / 042618 / 042615 (CVE-2026-91758〜91764、92863、92864、86578、86579、112125) | Hitachi Dynamic Link Manager for Linux / AIX / Windows、HA モニタ / 日立 | Linux 版は境界外の読み書き、一時ファイルの不備、リンク解決の不備。Windows 版はリンクのたどり方の不備とバイナリプランティング。HA モニタは重要な資源への不適切な権限の付与 | v3 最大 8.2 (ローカルでの権限昇格) | [日立 (Linux)](https://www.hitachi.co.jp/Prod/comp/soft1/security/info/vuls/hitachi-sec-2026-166/index.html) / [日立 (HA モニタ)](https://www.hitachi.co.jp/Prod/comp/soft1/security/info/vuls/hitachi-sec-2026-163/index.html) |
| 2026-11-11 | JVNVU#93068550 / CVE-2026-116081 | Sleipnir Mobile for iPhone / iPad (Black Edition を含む) v4.15.1 以前 / フェンリル | サーバー証明書を正しく検証せず、中間者攻撃で通信を盗み見られる。v5.0 以降 (Black Edition は v4.16) で修正 | v4 2.3 / v3 4.2 | [JVN](https://jvn.jp/vu/JVNVU93068550/) |
| 2026-11-11 | JVNVU#92618679 / CVE-2026-88822、88823、95691、95692、107496 | OpenSSL 4.1 / 4.0 / 3.5 ほか / OpenSSL Project | 11/10 のアドバイザリ。QUIC で初期化していないスタックが漏れる、AES-GCM-SIV で AAD を偽造できる・境界外読み取り、QUIC の CRYPTO フレームの再送で DoS、CMS_encrypt() の無限ループ。修正版のリリースは 12/1 の予定で、現時点では GitHub 上の修正のみ | 5 件とも Low | [JVN](https://jvn.jp/vu/JVNVU92618679/) / [OpenSSL](https://openssl-library.org/news/secadv/20261110.txt) |
| 2026-11-11 | JVNVU#93337738 | Intel 製品 (2026 年 11 月の定例、24 件) | INTEL-SA-01440〜01580。Graphics、QAT ドライバー、NPU ドライバー、TDX (Workload Attestation、MigTD)、Slim Bootloader、サーバーボードの UEFI、PROSet/Wireless など | 詳細は各 advisory | [JVN](https://jvn.jp/vu/JVNVU93337738/) |
| 2026-11-11 (更新) | JVNVU#99905564 [続報] / CVE-2026-109618、109619 | PHP (PHP2Shell) / 国内ベンダーのステータス | 「影響を受けるシステム」と関連文書を更新。トレンドマイクロ、ソリトンシステムズ、FFRI セキュリティ、テルモ BCT のベンダーステータスを追加・更新した | (既出) 任意のコード実行 | [JVN](https://jvn.jp/vu/JVNVU99905564/) |

> 補足: JVN iPedia の個別ページ (JVNDB-2026-0426xx) は 05 時 (JST) の時点で 404 のため、日立の項は日立のセキュリティ情報のページと RSS で確かめた。HiRDB の対策版の番号は日立のページを参照のこと。JVNVU#98354779 (Siemens の 11 月の定例) は、識別子が 11/5 版と同じ (更新) なので表から省いた。JVN iPedia の 11/10〜11 登録分のうち、PrestaShop、FrodoBots、Airbyte、FreeSWITCH は既出のため除いた。

### 国内コミュニティ・研究・イベント

#### [2026-11-11] Zenn: 採用の課題や NDA を装って渡された `.git` フォルダで、どの操作でフックが動くかを git 2.54.0 で試した。clone では動かず、受け取ったフォルダで最初に `git status` を打つと動いた
- **何が起きたか**: Frank Wiles 氏の「I got targeted」(10/2) が、共有フォルダの `.git/hooks/post-checkout` で外部のプログラムを実行させようとしていた。これをきっかけに、筆者が 13 種のフックを置いて手元で確かめた。わかったことは次のとおり。
  - clone では、送り手のフックはコピーされず動かない。
  - フォルダごと受け取った場合は、最初の `git status` でもフックが動く。コピーで index の ctime や inode が合わなくなり、index を書き戻すためだ。
  - アーカイブで渡されても、実行の権限は残る。
  - 自分が持ち主のファイルなので、`safe.directory` の仕組みでは止まらない。
  - `core.hooksPath=/dev/null` でもフックは止まるが、ほかにもコマンドを書ける設定があるので、`git clone --no-checkout` で clone し直してから読むのが安全。
  - 国内でも、採用の課題、副業の案件、カジュアル面談の前に渡されるコードを、同じ経路として挙げている (TraderTraitor の注意喚起にも触れている)。
- **なぜ重要か (評価)**: ソースコード診断で顧客から `.git` ごと預かるとき、そのまま守れる手順になっている。
- 出典: [Zenn (2026-11-11)](https://zenn.dev/mystery_hat/articles/git-hooks-in-received-repositories)

#### [2026-11-11] Zenn: キングプリンターズの最終報を読む。盗まれたシステム基盤の認証情報で生成 AI を約 7 時間呼ばれ、止まったのは AI サービス側の利用制限だった (LLMjacking)
- **何が起きたか**: リアルインベントの CTO が、キングプリンターズが 11/9 に出した最終報を整理した。同社のシステム基盤の認証情報が不正に使われ、複数の IP アドレスから生成 AI サービスを 6 時間 53 分にわたって大量に呼ばれた。呼び出しが止まったのは、AI サービス側が利用制限をかけたため。攻撃者は新しい認証情報も作っており、筆者は「盗まれた鍵に、AI を呼ぶのに要らない発行の権限が付いていた」と読んでいる。顧客情報への接触の痕跡はないという。再発防止策は、静的な認証情報をやめて一時的な認証情報を使うことと、最小権限への見直し。どこから漏れたかは公表されていない。
- **なぜ重要か (評価)**: 国内でも LLMjacking の被害が最終報として公になった。CPU やディスクの監視では気づけず、最初に異常が出るのは請求額になる。クラウドの診断では、AI サービスを呼べる権限と認証情報を発行できる権限が同じキーに付いていないか、利用料の急な増加にアラートがあるかを見たい。
- 出典: [Zenn (2026-11-11)](https://zenn.dev/tech_realinvent/articles/0e5a46210adc60)

#### [2026-11-10] Ubie の水谷正慶氏、「AI と始める、監視基盤なしのセキュリティ監視」の資料を公開
- **何が起きたか**: Ubie の VP of Security、水谷正慶氏が講演資料を Speaker Deck に公開した。主張は「SIEM がなくても監視は始められる」。中身は次のとおり。
  - Alert Center、SCC、GuardDuty、EDR などの標準アラートについて、通知先、担当、優先度、対応記録を決めておく。
  - ログは、何が、どこに、いつまで残るかの台帳を作り、管理者が侵害されても消せない場所に置く。
  - 検索を、即時・日次・週次に分けて回す。
  - 時間は、検知までではなく「対応を始めるまで」で測る。
  - AI は調査の手間を減らすが、残していないログと、対応する人がいないことは埋めない。
- **なぜ重要か (評価)**: SIEM のない中小の組織に、監視の最低限の線を引くときの材料になる。侵害の後の診断や助言で、ログの保持と検索できる権限の不足を指摘するときにも使える。
- 出典: [Speaker Deck (2026-11-10)](https://speakerdeck.com/mizutani/ai-to-hajimeru-kanshi-kiban-nashi-no-sekyuriti-kanshi-2)

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 70 (AI 27 / セキュリティニュース 約 18 / CVE データ 6 / 国内 約 20。RSS、NVD API 2.0、OSV、EPSS、CISA KEV JSON、各社の一次資料)
- 採用件数: AI技術=10 / AIセキュリティ=7 / セキュリティ=16 / CVE=11 / 国内インシデント=8 / 国内政策=5 / JVN=8 / 国内コミュニティ=3
- 除外理由内訳: 古すぎ=約 45 (Rails の CVE 群 20 件余り、ScanNetSecurity の 11/11 掲載分の 10/30〜11/5 の発表、OpenAI Control Room [公表 11/9]、React CVE-2026-126187 [修正版 10/14、11/10 号の判断と揃えて除外] など) / 重複=約 50 (11/10・11/11 号の Patch Tuesday、Git、SAP、Adobe、Chrome、Barracuda、teket、Notion AI の既報部分、node-forge など) / 日付不明=約 3 (Directus、soapbar、@tinacms/mdx の advisory)
- 取得失敗ソース:
  - cisa.gov の Atom フィード (403。KEV JSON は取得でき、11/11 の新規追加はまだなかった)
  - api.github.com/advisories と GHSA の HTML (403。NVD の published と OSV で代用)
  - Google DeepMind の RSS (XML が不正。The Verge / Ars Technica で代用)、Google TI の RSS (HTML が返った。トップページから個別の記事を確認)
  - Dark Reading の記事本文 (取得不可。RSS の概要で既出と判断)、Quartz (403。Investing.com が配信した Reuters の記事で代用)
  - JVN iPedia の個別ページと日立のセキュリティ情報の一覧ページ (404。RSS と日立の個別ページで代用)、soft99.co.jp (接続リセット。ソフト 99 の件は不採用)
  - 日本証券業協会のパスキーに関する一次資料 (見つからず、共同通信の配信で代用)
- 備考:
  - エディオン (11/9 公表) は前号までに載っておらず、11/11 の報道で詳細が出たため「公表 / 報道」の日付を併記して採用した。
  - 新しい CVE の多くは EPSS が未算出で、表の中に KEV 入りや EPSS ≥ 0.5 のものはない。

</details>
