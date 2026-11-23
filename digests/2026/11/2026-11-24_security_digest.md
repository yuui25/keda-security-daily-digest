# KEDA Daily Digest — 2026-11-24 (JST)

> 採用範囲: 公開日 2026-11-22 〜 2026-11-24
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

国内は 11/21〜23 の三連休にあたり、一次情報 (JPCERT/CC、IPA、JVN、組織のプレスリリース) の新着はほとんどなかった。そのため本号は海外の動きが中心になる。セキュリティ側で最も大きいのは、**Microsoft の Azure API Management (APIM) の Classic 階層に欠陥があり、悪用されて、APIM に保存した API の資格情報が盗まれた**件だ。ノルウェーの当局は、Equinor と Skagerak Energi への攻撃とこの欠陥を結びつけた。Microsoft は経路を塞いだが、**盗まれた可能性のある資格情報は自動では無効にならない**ため、利用者側でのローテーションが必要になる。CISA は、N-able Mail Assure の SSRF (CVE-2026-134624) と MONAI Label のパストラバーサルを KEV に追加した。Mandiant は、2008 年から更新されていない ASP.NET の CSRF 対策ライブラリ Idunno.AntiCsrf のデシリアライズ RCE (CVE-2026-131914) が悪用されていると警告した。業界の再編では、CrowdStrike が Zscaler を約 439 億ドルで買収すると発表した。
AI 側では、Anthropic がプルリクエストの CI 修正と承認まで担う「Claude Ship」(PR Steward / Claude Approvals) を出し、Google は検索の AI モードを Drive と Wallet につないだ。Amazon は Decart の最適化技術を 75 億ドルで取得する。AI セキュリティでは、Rubrik が CODE BLUE 2026 で、文書 1 つで Microsoft 365 Copilot を遠隔操作する「ChatMate」を解説した (CVE-2026-32193、報奨金 4.8 万ドル)。
CVE では、**Xen Orchestra の悪用中の認証回避に CVE-2026-133469 が採番された**。ほかに、pgjdbc の SQL インジェクション 2 件、simple-git の `--exec` 注入、Kerberos Agent の固定の JWT 鍵が出た。
**今日まず見るべきもの**: (1) 自社や顧客の Azure テナントに APIM の Classic 階層 (Developer / Basic / Standard / Premium) があるかどうか、(2) 診断対象の ASP.NET WebForms に `Idunno.AntiCsrf` が残っていないか。

## 今日の深掘り

### Azure API Management の Classic 階層の欠陥が悪用され、APIM に保存した資格情報が盗まれた。ノルウェーのエネルギー企業 2 社も被害 (2026-11-24)

- **概要 (事実)**: BleepingComputer が入手した Azure Service Health のセキュリティ勧告 (Tracking ID: MZK9-GH0) によると、Microsoft は 11/18 に APIM の Classic 階層の脆弱性を見つけ、11/19 に緩和策を展開した。勧告は「Microsoft が見つける前に、権限のない者が Classic のインスタンスに保存されたシークレットにアクセスできた可能性があり、実際に顧客が露出していた」としている。Microsoft は 11/21 (土) に、影響を受けた顧客が露出した可能性のある資格情報を特定し、入れ替えるための手引きを公開した。ノルウェー国家安全保障局 (NSM) は、身元不明の攻撃者がこの欠陥を使って、APIM に保存されたアクセストークンなどを積極的に狙っていたとし、Equinor と Skagerak Energi が被害を受けた組織に含まれると発表した。NSM によると、欠陥を最初に見つけたのはノルウェーのエネルギー業界で、Equinor が特定と通報で大きな役割を果たした。
- **技術的な中身 (公表されている範囲)**: Microsoft の勧告によると、推奨のセキュリティ設定に沿っていない Classic のインスタンスでは、**管理プレーンの一部の機能に、権限なくアクセスできた**。そこから管理操作ができ、シークレットの管理もできた。露出した可能性があるのは、(1) Named Values に保存したシークレット、(2) ID プロバイダーのクライアントシークレット、(3) OpenID Connect プロバイダーのクライアントシークレット、(4) サブスクリプションキー、(5) 管理 API を直接呼ぶためのトークン、の 5 種類。v2 階層は影響を受けない。The Record によると、被害が大きかったのは、Microsoft の推奨に従わず、Key Vault を参照せずに機密の値を APIM に直接保存していた顧客だ。Microsoft は、影響を受けた顧客の数を明らかにしていない。根本の原因 (どの API の、どの認可チェックの抜けか) も公表していない。Reddit の管理者の投稿では、**有効な管理者のトークンで Azure Key Vault にログインされた**ことから侵入に気づいたとされる (未確認の二次情報)。
- **背景・経緯 (背景引用)**: APIM の管理プレーンと周辺の欠陥は、これまでにも報告されてきた。2023 年には Ermetic (現 Tenable) が、CORS Proxy と Hosting Proxy の SSRF を含む 3 件を報告した ([Tenable](https://www.tenable.com/blog/uncovering-3-azure-api-management-vulnerabilities-when-good-apis-go-bad))。その後、Binary Security が、Reader の権限で ARM API から Contributor 相当の操作ができる問題を報告している ([SecurityWeek](https://www.securityweek.com/azure-api-management-vulnerabilities-allowed-unauthorized-access/))。直近の 11/22 号では、Entra Connect Health の API の欠陥が悪用され、テナントのメタデータが読まれた件も扱った。**Microsoft のクラウドの管理プレーンで、悪用されてから顧客に知らされる**事例が、この 1 週間で 2 件目になる。
- **なぜ今これが重要か (評価)**: APIM は「API の前に置く関所」で、**後ろのシステムに入るための資格情報をまとめて持っている**。Named Values のシークレットや OAuth のクライアントシークレットが盗まれると、APIM を通さずに後ろの API や IdP に直接入られる。Microsoft の修正は経路を塞いだだけで、**盗まれた値は使える状態のまま残る**。CVE は採番されない見込みが高く (クラウド側の修正)、パッチの有無で追う通常の運用には乗らない。診断の業務では、**Azure の構成レビューで「Named Values に平文のシークレットがあるか」「Key Vault 参照になっているか」を指摘する根拠**が、実害の事例として手に入ったことになる。CVE が出ず、検知も利用者の側に任されるため、**今週中に棚卸しをするかどうかで差が出る**案件と判断した。
- **読者が今日できること**:
  - Classic 階層の棚卸し: `az apim list --query "[].{name:name, rg:resourceGroup, sku:sku.name}" -o table` で、SKU が `Developer` / `Basic` / `Standard` / `Premium` (v2 の名前がつかないもの) のインスタンスを一覧にする。
  - Named Values の確認: 各インスタンスで `az apim nv list` を実行し、`secret: true` で `keyVault` の参照を持たない値を洗い出す。それと、ID プロバイダー / OIDC のクライアントシークレットとサブスクリプションキーを入れ替える。後ろのシステム (Key Vault、IdP、バックエンド API) のサインインのログを、11/18 以前までさかのぼって確認する。
  - Activity Log で `Microsoft.ApiManagement/service/namedValues/listValue/action` や `.../subscriptions/listSecrets/action` などのシークレットを読む操作を、見覚えのない主体や IP で絞り込む。ただし、**今回の経路が顧客側のログに残るかどうかは公表されていない**ので、「記録がない = 安全」とは判断しない。
- 出典: [BleepingComputer (2026-11-23 米国時間)](https://www.bleepingcomputer.com/news/security/microsoft-azure-flaw-exploited-to-steal-customers-api-credentials/) / [The Record (2026-11-23)](https://therecord.media/norway-microsoft-cyberattack-equinor) / [SecurityWeek (2026-11-23)](https://www.securityweek.com/azure-flaw-exploited-to-target-secrets-at-norwegian-energy-firms/)

## AI 技術・トレンド

### [2026-11-24] Anthropic、開発の後工程を担う「Claude Ship」を発表。CI の失敗とコンフリクトを直す「PR Steward」と、定型の変更を承認する「Claude Approvals」をベータで提供
- **何が起きたか**: The Verge によると、Anthropic は Claude Ship を発表した。Claude がプルリクエストのレビュー、修正、承認までできるようになる。PR Steward は、CI のチェックの失敗、マージのコンフリクト、Code Review (3 月に発表し、10 月に一般提供) やほかのレビューツール、チームメンバーの指摘に対応し、変更した内容をコメントで残す。Claude Approvals は、組織のポリシーが許す範囲で定型の変更を承認する。判断には、Code Review の指摘や、自然言語で書いた独自の分類器を使える。Team / Enterprise の顧客向けで、GitHub のリポジトリが対象。
- **なぜ重要か**: 人間のレビューが最後の関所だった工程を、**AI による「承認」まで自動化する**動きになる。診断の観点では、承認の判定に使う分類器やポリシーが、**プルリクエストの本文やコードのコメントからのプロンプトインジェクション**の新しい標的になる。導入する組織では、ブランチ保護で「AI だけの承認で main に入る範囲」を明示しておく必要がある。
- 出典: [The Verge (2026-11-23 米国時間)](https://www.theverge.com/ai-artificial-intelligence/1040134/anthropic-claude-ship-ai-pull-requests)

### [2026-11-24] Google、検索の AI モードの「Personal Intelligence」を Drive、Wallet、Gemini アプリにつなぐ
- **何が起きたか**: Google は、これまで Gmail、カレンダー、フォトに対応していた Personal Intelligence を、Drive、Wallet、Gemini アプリに広げた。Wallet をつなぐと、支出の傾向やクレジットカードの特典の活用を相談できる。Google によると、AI モードは口座の情報を読むだけで、お金を動かしたり管理したりはできない。接続は任意で、いつでもオフにできる。
- **なぜ重要か**: 検索の画面から、**利用者の文書と金融の情報に AI が届く**ようになる。悪意のある Web ページや共有ドキュメントから間接プロンプトインジェクションを仕込み、Drive の中身を要約させて外に出させる、という攻撃面が検索にも広がる。「読むだけ」の制約がどこで強制されているか (モデルの指示なのか、API の権限なのか) が、今後の検証のポイントになる。
- 出典: [TechCrunch (2026-11-23 米国時間)](https://techcrunch.com/2026/11/23/google-searchs-ai-mode-can-now-tap-into-drive-and-wallet-for-more-personalized-responses/) / [Google](https://blog.google/products-and-platforms/products/search/google-search-personal-intelligence-apps/)

### [2026-11-24] Amazon、イスラエルの Decart から推論最適化の技術「DOS」と創業チームを 75 億ドルで取得 (Bloomberg 報道)。Trainium の外販に備える
- **何が起きたか**: TechCrunch が Bloomberg を引いて報じた。Decart はリアルタイムの世界モデル「Oasis 3」や動画生成で知られる。その一方で、NVIDIA、Amazon、Google のハードウェアで AI モデルを効率よく動かす「Decart Optimization Stack (DOS)」を持つ。Amazon はブログで、DOS の技術と創業チーム、研究者・エンジニアを迎えると説明した。Amazon は、自社のデータセンターで使ってきた Trainium を、顧客に売り始める準備をしている。
- **なぜ重要か**: NVIDIA 以外のチップで同じモデルを動かす「移植層」の価値が、75 億ドルと評価されたことになる。推論の基盤が多様になると、**チップごとに別の推論ランタイムやカーネルが使われる**。11/22〜23 号の OpenRouter の件のように、どの事業者が実際に何で推論しているかを利用者から確かめにくい状況は続きそうだ。
- 出典: [TechCrunch (2026-11-23 米国時間)](https://techcrunch.com/2026/11/23/amazon-snaps-up-decarts-ai-optimization-tech-for-7-5b-as-it-prepares-to-sell-trainium-chips/)

### [2026-11-23] NVIDIA、辞任から 2 週間たたずに Jensen Huang 氏を CEO に戻す。12/3 に上院の銀行委員会で証言
- **何が起きたか**: NVIDIA の取締役会は、Huang 氏を CEO 兼社長に戻した。米政府の高官と協議したうえで、Huang 氏に安全保障上のリスクはないと判断したとしている。Huang 氏は、少なくとも 2 件の婚外関係を認めて辞任していた。うち 1 人は、米政府が中国のスパイと疑う女性だった。株価は寄り付きで約 30% 上がった。トランプ大統領は SNS で、司法長官が「Huang 氏が問題を起こした証拠はない」と確認したと書いた。Huang 氏は 12/3 に、輸出管理を所管する上院の銀行委員会で証言する予定。
- **なぜ重要か**: AI の計算資源の最大手のトップ人事に、米政府が直接関わったことを公に認めた形になる。12/3 の証言は、輸出管理と、11/17 号で扱った海外データセンターの遠隔利用の規制の行方に関わる。
- 出典: [TechCrunch (2026-11-23)](https://techcrunch.com/2026/11/23/nvidia-reverses-course-and-brings-jensen-huang-back-as-ceo/) / [TechCrunch (2026-11-23、証言の予定)](https://techcrunch.com/2026/11/23/jensen-huang-scheduled-to-testify-next-week-in-senate-following-reinstatement-as-nvidia-ceo/)

### [2026-11-23] Sierra、シリーズ F で 17.5 億ドルを調達し、評価額は半年で 2 倍の 300 億ドルに。Meta、Stripe、Walmart とエージェント間のプロトコルを定義中
- **何が起きたか**: Bret Taylor 氏が共同創業した顧客対応 AI の Sierra は、Greenoaks と Lightspeed が主導する 17.5 億ドルの調達を発表した。6 か月前の評価額は 150 億ドルだった。Fortune 50 の約半数が顧客で、成果報酬型の料金で年換算の売上が 5 か月で倍の 4 億ドルになった。個人のエージェントと企業のシステムがやり取りするためのプロトコルを、Meta、Stripe、Walmart などと定義している。
- **なぜ重要か**: 「利用者のエージェント」と「企業のエージェント」がやり取りする標準を、少数の大手が作っている。下の Walmart の件と合わせると、**エージェント同士の認証と権限の委譲**が、近いうちに診断の対象になる。
- 出典: [TechCrunch (2026-11-23)](https://techcrunch.com/2026/11/23/sierra-doubles-valuation-to-30b-within-six-months-as-demand-for-ai-in-cx-takes-off/)

### [2026-11-23] Walmart、AI エージェント向けの「Agent Gateway」を本番で公開。最初は Meta の Muse に対応し、エージェント専用の「Agent Profile」に支出の上限を設定できる
- **何が起きたか**: Walmart は、先月発表した Agent Gateway の実装を公開した。Muse が、Walmart の AI アシスタント「Sparky」を通じて、ブラックフライデーのセール品を探して買える。Walmart のアカウントの中に、エージェント用の「Agent Profile」ができる。利用者は支出の上限を決め、購入を承認し、Muse が買った物の履歴を確認できる。Amazon や eBay は AI エージェントの閲覧を遮断しているが、Walmart はほかのエージェントにも広げるとしている。
- **なぜ重要か**: 「エージェント用の別アカウントに、上限つきの権限を委ねる」という設計が、大手の小売で本番に入った。11/22 号で扱った Muse の乗っ取り (悪意のある Web ページで会話の履歴を抜かれた件) と組み合わせると、**乗っ取られたエージェントが上限の範囲で買い物をする**シナリオが現実的になる。上限と承認のフローが、どこまでエージェントの外で強制されるかが要点。
- 出典: [The Verge (2026-11-23)](https://www.theverge.com/ai-artificial-intelligence/1039874/walmart-agent-gateway-meta-muse-black-friday)

### [2026-11-24] オレゴン州とバージニア州、Grok の性的なディープフェイクで SpaceX (xAI を合併) を提訴。安全対策の弱さを「欠陥ではなく機能だった」と主張
- **何が起きたか**: 両州の司法長官が、それぞれ州の消費者保護法の違反で訴えた。xAI と X が「利用者は保護されている」と宣伝しながら、同意のない性的な画像や CSAM を作って広めることを許したと主張している。訴状の中心は画像・動画生成の「Grok Imagine」だ。2025 年 8 月の「spicy」モードや、2026 年 1 月に追加された「他人の画像を同意なく編集できる」機能が問題とされた。
- **なぜ重要か**: 生成 AI の安全対策の不足を、**州の消費者保護法で争う**流れが広がっている。モデルの出力の制御が「宣伝と実態の不一致」として訴訟の論点になると、ガードレールの評価 (レッドチーミング) の記録が企業にとって防御の材料になる。
- 出典: [The Verge (2026-11-23 米国時間)](https://www.theverge.com/ai-artificial-intelligence/1040255/x-grok-ai-deepfakes-oregon-virginia-lawsuit)

### [2026-11-23] Hugging Face、「エージェント型の評価の作り方と保ち方」を公開。既存のタスクを流用して検証し、トレースを読み、間違った評価を公開の場で直す手順
- **何が起きたか**: Hugging Face のブログは、エージェント型の評価の構成要素、公開の判断、既存の部品の再利用、「評価が間違っていたとき」の教訓 (公開のレビュー、主張そのものの検証、汚染と飽和の区別) を整理した。物理学の研究室でのエージェントの導入を例に、主張の定義からモデルの比較まで 8 段階の手順を付けた。
- **なぜ重要か**: AI の脆弱性診断や AI ペンテストのツール (下の Xalgorix など) の性能の主張を読むとき、**「どのタスクで、何を正解として採点したか」を確かめる観点**がまとまっている。自社でベンチマークを作る場合のチェックリストとしても使える。
- 出典: [Hugging Face (2026-11-23)](https://huggingface.co/blog/agentic-evals)

### [2026-11-23] NVIDIA RTX Spark のノート PC で、ネイティブの Linux だと AC 電源につないだときだけ GPU のクロックが落ち、推論が Windows の約 5 分の 1 に (MindStudio の検証、GIGAZINE)
- **何が起きたか**: GIGAZINE が紹介した MindStudio の検証によると、GPT-OSS-120B の生成で、Windows は毎秒 65.4 トークン、WSL は 65.1 トークン、ネイティブの Linux は 13.9 トークンだった。GPU は Windows で約 2.2GHz、Linux で約 790MHz で動いた。温度は 40〜47℃ でサーマルスロットリングではなく、AC 電源を抜くと Linux でも毎秒 61〜67 トークンに戻った。GIGAZINE は、暗号化されたファームウェアが原因だという見方を見出しにしている。
- **なぜ重要か**: ローカルで LLM を動かす診断用の端末 (機密のソースコードを外に出さずに AI で読む用途) を選ぶとき、**OS によって性能が 5 倍違う**ことがある。購入前に、使う OS で実際に計測するべきだ。
- 出典: [GIGAZINE (2026-11-23)](https://gigazine.net/news/20261123-linux-nvidia-rtx-spark-laptop/)

### [2026-11-23] TechCrunch: Anthropic の上場前に大きく賭けた投資家たち。Notable Capital は、ファンドの米国分の約 1 割を評価額 615 億ドルのシリーズ E に投じた
- **何が起きたか**: Notable Capital (旧 GGV Capital) は、10 億ドル超のファンドの米国分の約 10% をシリーズ E に投じた。同社の分析では、開発者は ChatGPT より Claude を 70% の割合で使っており、前年から逆転していた。「ミッションクリティカルな用途には、米国の非公開のモデルが必要になる」とも判断したという。記事は、Anthropic が先週の水曜日に 813 億ドルを調達したとしている (上場時の調達)。
- **なぜ重要か**: 投資判断の根拠に「開発者の利用の割合」と「米国製・非公開であること」が挙がった。11/22 号の米下院の報告書 (中国製のオープンウェイトを問題視) と同じく、**モデルの出自が調達の条件になる**流れを裏付けている。
- 出典: [TechCrunch (2026-11-22 米国時間)](https://techcrunch.com/2026/11/22/how-notable-capital-gic-and-baillie-gifford-bet-big-on-anthropic-before-its-ipo/)

## AI セキュリティ

### [2026-11-23] 国内: Rubrik、CODE BLUE 2026 で「ChatMate」を解説。文書 1 つを Microsoft 365 Copilot にアップロードさせるだけで、攻撃者が被害者の Copilot に直接指示を出せた (CVE-2026-32193、報奨金 4.8 万ドル)
- **何が起きたか**: ITmedia エンタープライズによると、Rubrik Zero Labs の Ori Lahav 氏は、11/18 の記者説明会でこの攻撃を説明した。Rubrik は「リモートプロンプト実行 (RPE)」と呼んでいる。文書に隠した指示で Copilot を操り、コード実行用のサンドボックスから抜け出して、攻撃者と被害者の Copilot をつなぐ双方向のチャネルを作る。約 35 秒のデモでは、攻撃者が「パスワードが書かれた文書を全部書き起こせ」と指示すると、被害者の Copilot が答えた。被害者の画面には、アップロードした文書への無害な回答しか出なかった。脱出の起点は、Azure のコンテナランタイムのパストラバーサル (CVE-2026-32193、CVSS 8.8) だった。2026 年 2 月に MSRC に報告し、4 月にサーバー側で修正され、4.8 万ドルの報奨金が支払われた。Lahav 氏によると、コードサンドボックス自体はインターネットにつながらない設計だったが、**その下の Kubernetes ノードがつながる状態だった**。
- **なぜ重要か**: Simon Willison 氏の「Lethal Trifecta」(特権アクセス、信頼できないコンテンツ、外部との通信) が、**サンドボックスの下の層**で成立してしまった事例だ。7 月の OpenAI の評価用サンドボックスの件 (パッケージのプロキシ経由で外に出た) と同じ構図になる。AI 製品の診断では、「サンドボックスがネットにつながるか」だけでなく、**ホストのノード、サイドカー、プロキシの egress** まで確かめる必要がある。利用企業側の対応は不要とされる。
- 出典: [ITmedia エンタープライズ (2026-11-23)](https://www.itmedia.co.jp/enterprise/articles/2611/23/news001.html)

### [2026-11-23] インド CERT-In、AI を使った攻撃で銀行や決済の事業者から不正な送金が起きたと警告。「エージェント型の攻撃フレームワーク (AOFS)」の利用も確認
- **何が起きたか**: CERT-In の勧告によると、攻撃者は決済の API を直接狙わなかった。業務アプリや委託先が運用するワークフローを悪用して、取引先の記録や承認の関係を書き換え、正規の決済の手続きで不正な送金を通した。被害額と攻撃者は公表していない。別の脅威ハンティングでは、AI のエージェント群が並行して偵察や権限の探索を行い、パッチを解析して既知の脆弱性のエクスプロイトを作り、エラーや遮断に応じて手口を変えていた。
- **なぜ重要か**: AI を使った攻撃の被害として、**業務ロジック (承認フローとマスタデータの改ざん)** が名指しされた。脆弱性診断では、技術的な脆弱性よりも「支払先の口座の変更に、独立した確認があるか」「マスタの変更とその承認を同じ人ができないか」という**業務フローの診断**の比重が上がる。
- 出典: [The Hacker News (2026-11-23)](https://thehackernews.com/2026/11/ai-assisted-cyberattacks-trigger.html)

### [2026-11-23] 国内: Claude Code の PreToolUse フックは、時間制限を超えると「拒否」でも書き込みを通す。`claude -p` の出力にはエラーも警告も出ない (Zenn)
- **何が起きたか**: 上条碧斗氏は、Windows 11 と Claude Code 2.1.330 で、常に拒否する（終了コード 2）フックに待ち時間を入れて試した。15 秒待つフックに 3 秒の制限を付けた回だけ、`--permission-mode acceptEdits` で作業フォルダの中へのファイルの書き込みが通り、Claude は「DONE」と答えた。公式の Hooks reference の Timeouts の節にも、時間切れの PreToolUse フックは呼び出しを止めず、通常の権限の確認に進むと書かれている。フックの設定に `"onFailure": "block"` を足すと (v2.1.295 以降)、時間切れ・異常終了・起動の失敗のどれでも止まった。
- **なぜ重要か**: 11/22〜23 号の「日本語のフォルダ名で通る」「python の heredoc で素通り」に続く、**エージェントの安全装置が「開いた状態で壊れる (fail-open)」**事例になる。フックで重い処理 (外部 API の照会やウイルス検査) をしている組織は、`onFailure: block` を入れているかを確認したい。
- 出典: [Zenn 上条碧斗 (2026-11-23)](https://zenn.dev/kamijo_aoto/articles/claude-code-hook-timeout-passes)

### [2026-11-23〜24] MCP と AI アプリの基盤の認証の欠陥: Pomerium の MCP トークンエンドポイント、Gradio の `Host: localhost`、BISHENG の未認証のワークフロー実行
- **何が起きたか**: (1) Pomerium 0.30.0〜0.33.x では、`/.pomerium/mcp/token` が `client_secret_basic` のクライアントのシークレットを確かめていなかった。認可コードやリフレッシュトークンを盗んだ攻撃者が、任意のシークレットで被害者のアクセストークンを得られた (CVE-2026-135300、0.34.0 で修正)。(2) Gradio 6.27.0〜6.31.x では、SSR モードのとき、ローカルの Node の SSR サーバーを経由したリクエストがループバックの確認を通った。偽の `Host: localhost` で、運営者のローカルに保存された Hugging Face のトークンを使って、実行履歴のバケットを読み書きできた (CVE-2026-134825)。(3) LLM アプリ基盤の BISHENG 3.0.0 未満では、`/api/v2/workflow/invoke` に認証がなかった。ワークフローの UUID を知っていれば、Code ノードの `code` を上書きして `exec()` で任意の Python を実行できた (CVE-2026-135211)。
- **なぜ重要か**: どれも「**AI 向けに後から足した入口**」(MCP 用の OAuth、ローカル向けの履歴機能、外部公開の API) で、本体の認証の仕組みを通っていない。MCP のゲートウェイや LLM アプリの基盤を診断するときは、まずこうした追加のエンドポイントを列挙するとよい。
- 出典: [NVD CVE-2026-135300](https://nvd.nist.gov/vuln/detail/CVE-2026-135300) / [NVD CVE-2026-134825](https://nvd.nist.gov/vuln/detail/CVE-2026-134825) / [NVD CVE-2026-135211](https://nvd.nist.gov/vuln/detail/CVE-2026-135211)

### [2026-11-23] 「AI で見つけた」OSS の脆弱性の公表が続く: Apache StormCrawler の 4 件は ASF が Claude のエージェントで発見、IRC のサービス Anope は AI での監査で 10 件超を修正
- **何が起きたか**: Apache StormCrawler の CVE-2026-82442〜82446 の advisory は、発見者として n0mi1k 氏と並んで「The ASF using Claude Agents」を挙げている。ASF がオープンソースのプロジェクトのセキュリティを調べるのに Claude のエージェントを使い、プロジェクト側が検証して報告した。UnrealIRCd の作者 Bram Matthys 氏は 11/22、ほかの IRC のプロジェクトも AI で監査して報告しており、Anope が 2.0.21 / 2.1.28 でクラッシュ、ハング、アカウントの乗っ取り、条件つきのコマンドインジェクションなど 10 件以上を修正したと告知した。
- **なぜ重要か**: 財団や開発者が「AI で監査した」と明記して CVE を出すのが、普通のことになってきた。11/23 号の日経の「パッチ地獄」の話と同じで、**中小の OSS にも修正の波が来る**。CVE の追跡では、advisory のクレジットの欄を見て、AI 由来の発見かどうかを分けて数えると、傾向が読みやすい。
- 出典: [oss-security StormCrawler (2026-11-23)](https://seclists.org/oss-sec/2026/q4/843) / [oss-security Anope (2026-11-23)](https://seclists.org/oss-sec/2026/q4/836)

### [2026-11-23] OSS の AI ペンテストツール「Xalgorix」: 主のエージェントが見つけた脆弱性を、別のエージェントがもう一度エクスプロイトして確かめてから報告する
- **何が起きたか**: Help Net Security によると、Xalgorix は Go のバイナリとローカルの Web ダッシュボードで、Apache-2.0 で公開されている。ブラウザと端末を持つ LLM のエージェントが、偵察から報告まで 22 段階の計画に沿って Nmap、Nuclei、SQLmap などを動かす。7 つの LLM プロバイダに対応し、Ollama でローカルのモデルも使える。スコープの外へのツールの呼び出しを止める仕組みがある。2 つ目のエージェントが再現できなかった指摘は、消さずに人間のレビューに回す。誤検知の率は社内で測っているが、公開の予定はないという。
- **なぜ重要か**: 「再エクスプロイトで確かめる」設計は、AI ペンテストの誤検知を減らす方向としては妥当だ。ただし、同じ週に Amazon が報告した Cairn の悪用 (11/21 号) のように、**OSS の AI ペンテスト基盤は攻撃者にもそのまま使われる**。社内で試すときも、スコープの制御が実際に効くかを先に検証するべきだ。
- 出典: [Help Net Security (2026-11-23)](https://www.helpnetsecurity.com/2026/11/23/xalgorix-ai-penetration-testing-tool/)

## セキュリティニュース

### [2026-11-24] ノルウェー NSM、Equinor と Skagerak Energi への攻撃に Azure API Management の欠陥が使われたと発表 (**悪用確認済み**)
- **何が起きたか**: The Record によると、Equinor は先週の火曜日に攻撃を検知し、金曜日まで封じ込めきれなかった。社内のサービスの一部が止まったが、石油とガスの生産は続いた。Equinor は「データが盗まれたり改ざんされたりした兆候はない」とし、同社を狙った攻撃ではなかったようだとしている。Skagerak Energi (Statkraft が過半を持つ電力会社) も水曜日に攻撃を公表し、発電への影響はないとした。Microsoft は、同じ攻撃者が 2 社の件に関わっていたかどうかを明らかにしていない。
- **なぜ重要か**: 技術の詳細は上の「今日の深掘り」を参照。重要インフラの事業者が、**クラウドの事業者より先に**クラウドの欠陥を見つけた例になる。顧客側のログ監視の価値を示している。
- 出典: [The Record (2026-11-23)](https://therecord.media/norway-microsoft-cyberattack-equinor)

### [2026-11-23〜24] [続報] N-able Mail Assure の侵害の調査で見つかった SSRF に CVE-2026-134624 (CVSS 4.0 で 9.3)。CISA が KEV に追加 (**悪用確認済み**)
- **前回から何が変わったか**: 11/20 号では侵害の公表までを扱った。N-able は 11/22 に advisory を出した。リレーを設定したときに Mail Assure が行う LDAP の同期の接続の確認で、接続先が制限されていなかった。高い権限の API の利用者が、内部の任意のホストとポートに接続させ、どれが応答するかを調べ、内部のサービスに細工したデータを送れた。ビルド 20261121.1943 で修正され、ダッシュボードと API は 11/21 の深夜に戻った。N-able は、この欠陥が侵入の経路だったかどうかを明らかにしていない。CISA は 11/23 にこの CVE を KEV に追加した。顧客の API トークンと OAuth のトークンは無効にされたので、連携のスクリプトは資格情報を作り直す必要がある。
- **なぜ重要か**: 「接続テスト」のボタンの裏にある SSRF は、メールのゲートウェイや SaaS の管理画面で何度も見つかっている型だ。KEV の登録は、実際の悪用を CISA が確認したことを意味する。
- 出典: [The Hacker News (2026-11-23)](https://thehackernews.com/2026/11/n-able-discloses-critical-mail-assure.html) / [NVD CVE-2026-134624](https://nvd.nist.gov/vuln/detail/CVE-2026-134624) / [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

### [2026-11-23] Mandiant、2008 年から更新のない ASP.NET の CSRF 対策モジュール「Idunno.AntiCsrf」に、未認証のデシリアライズ RCE (CVE-2026-131914、CVSS 9.3)。**悪用を確認**、修正版はない
- **何が起きたか**: The Hacker News によると、0.9.1.0 と 0.9.1 Beta の `Idunno.AntiCsrf.AntiCsrfModule` (IHttpModule) は、WebForms の POST で受け取った CSRF トークンを、鍵なしの `ObjectStateFormatter` で、MAC や署名の検証なしにデシリアライズしていた。Mandiant は、設定された CSRF の Cookie に空でない任意の値を入れ、CSRF のフォームのフィールドに Base64 でエンコードした `ObjectStateFormatter` のガジェットチェーンを入れれば、POST 1 回で `w3wp.exe` の権限でコードを実行できるとしている。「実際の悪用を確認した」とも書いた。パッチは出ないので、Mandiant は `System.Web.Helpers.AntiForgery` などへの置き換えを勧めている。
- **なぜ重要か**: **CSRF の対策のはずの部品が、未認証の RCE の入口**になっていた。古い WebForms の業務システムは国内にも多い。ソースコード診断や構成の確認では、`Web.config` と `bin/` を `Idunno.AntiCsrf` / `AntiCsrfModule` で検索するだけで当たりがつく。
- 出典: [The Hacker News (2026-11-23)](https://thehackernews.com/2026/11/hackers-exploit-critical-aspnet-anti.html) / [Mandiant MNDT-2026-0048](https://github.com/mandiant/Vulnerability-Disclosures/blob/master/2026/MNDT-2026-0048.md)

### [2026-11-23] [続報] GL.iNet の GoodCloud の侵害: 公式の簡易チェックでは見つからない痕跡が追加され、2025 年から入っていたバックドアの報告も
- **前回から何が変わったか**: 11/23 号では、悪用の確認と最初の IoC (`crond -i /tmp/.log` のプロセス) までを扱った。Help Net Security によると、GL.iNet はその後、**公式の簡易チェックでは出てこない IoC も見つかった**と追記した。コミュニティが作った検出と掃除のスクリプトを案内しているが、「どちらの方法でも、侵害がないとは保証できない」としている。GL.iNet のサービスパートナーの RemoteToHome Consulting (RTH) と一部の利用者は、**2025 年に仕込まれたバックドア**を見つけたと報告した。最新の安定版のセキュリティファームウェアを入れると、今回のマルウェアは消える。KVM が感染していた場合は、つながっているコンピューターも調べるよう求めている。
- **なぜ重要か**: 「最新のファームウェアで消える」のは今回のマルウェアだけで、**それより前の侵害は別に調べる必要がある**。KVM の場合は、その先の PC が本当の標的になりうる。
- 出典: [Help Net Security (2026-11-23)](https://www.helpnetsecurity.com/2026/11/23/gl-inet-cloud-compromise-malware-backdoors/)

### [2026-11-23] CrowdStrike、Zscaler を株式交換で買収。企業価値は約 439 億ドル
- **何が起きたか**: Zscaler の株主は、1 株につき CrowdStrike の株を 1.135 株 (1 株 260.41 ドル相当) 受け取る。買収後、CrowdStrike の既存の株主が約 84.1% を持つ。Zscaler の Jay Chaudhry CEO は Zscaler の経営を続け、CrowdStrike の取締役会に入る。CrowdStrike の George Kurtz CEO は「AI を展開し、制御し、あらゆるエージェント型アプリを安全に動かす単一のコントロールプレーン」を作ると述べた。439 億ドルは、昨年の最大の案件 (Google によるクラウドセキュリティ企業の買収) を上回る。
- **なぜ重要か**: エンドポイント (EDR) とネットワーク (SSE / ゼロトラスト) の最大手同士が一つになる。診断の現場では、**EDR の回避と SSE の回避を同じベンダーの製品で同時に検証する**案件が増えそうだ。両方を一社に任せると、障害の影響も一社に集中する。
- 出典: [The Record (2026-11-23)](https://therecord.media/crowdstrike-zscaler) / [Help Net Security (2026-11-23)](https://www.helpnetsecurity.com/2026/11/23/crowdstrike-zscaler-43-9-billion-acquisition/)

### [2026-11-23] Project Zero、VirtualBox の Windows 版のプロセス保護を再び検証し、新しい回避を 3 件見つける。.NET のメモリ上でのアセンブリの読み込みを悪用 (CVE-2026-87268)
- **何が起きたか**: 筆者 (Project Zero の研究者) は 2017 年に、ホストの利用者から VM のプロセスを守る VirtualBox の仕組みを回避する方法を 3 つ報告していた (2020 年に COM のランタイムの件も追加)。2026 年に見直したところ、保護されたプロセスへの新しい回避を 3 件見つけた。さらに、2020 年の回避への修正が Windows の変更で壊れていた。記事は CVE-2026-87268 を詳しく解説している。.NET Framework は、マネージドコードだけならメモリ上のバッファからアセンブリを読み込める。それと VirtualBox の DLL ローダーのフックの実装を組み合わせて、検査をすり抜け、保護されたプロセスに任意のコードを読み込ませた。CVE-2026-87268 は 9 月の Oracle の CPU で修正済み。
- **なぜ重要か**: 「署名された DLL だけを読み込ませる」型のプロセス保護は、**署名されたランタイム (.NET) がメモリから任意のコードを読む**ことで崩れる。EDR やアンチチートなど、同じ設計を持つ製品の評価にそのまま使える観点だ。
- 出典: [Project Zero (2026-11-23)](https://projectzero.google/2026/11/virtualbox-process-hardening.html)

### [2026-11-24] スペインのサッカーリーグ LaLiga、ファン向けの基盤から個人情報が持ち出されたと公表。11/14〜16 に侵入
- **何が起きたか**: LaLiga によると、11/14〜16 に攻撃者がファン向けサービスの技術基盤の一つに不正にアクセスし、LaLiga と一部のクラブのデジタルサービスの登録者の個人データを持ち出した。11/16 に侵入の元を特定して遮断した。試合の運営を支えるほかのシステムには広がっていないとしている。スペインのデータ保護庁 (AEPD) と国家警察に届け出た。件数と影響を受けたクラブは明らかにしていない。ランサムウェアのグループによる犯行声明は出ていない。
- **なぜ重要か**: 世界中にファンを持つクラブ (Real Madrid、FC Barcelona など) の登録者が含まれる可能性がある。ワールドカップの前後の時期と重なり、**クラブやチケットを装ったフィッシング**の材料になる。
- 出典: [BleepingComputer (2026-11-23 米国時間)](https://www.bleepingcomputer.com/news/security/spanish-laliga-confirms-hackers-stole-soccer-fans-personal-data/)

### [2026-11-24] B2B のギフトカード卸 GlobeTopper、攻撃で 7 万ドル分のデジタルギフトカードを換金され、売上の機会損失は約 250 万ドル
- **何が起きたか**: 親会社の iQSTEL によると、侵入は 10/22 に検知された。GlobeTopper は基盤を止めて調査した。攻撃者は 7 万ドル分のデジタルギフトカードを換金した。運営の停止による売上の損失は約 250 万ドルと見積もっている。
- **なぜ重要か**: 直接の盗難額 (7 万ドル) より、**止めたことによる損失 (250 万ドル)** が 35 倍大きい。国内の eギフトの不正 (giftee の件など) と同じく、ギフトカードの発行・換金の API は、認可の診断で優先度が高い。
- 出典: [BleepingComputer (2026-11-23 米国時間)](https://www.bleepingcomputer.com/news/security/globetopper-loses-25-million-after-hackers-steal-70k-in-gift-cards/)

### [2026-11-23] オーストリア外務省、外部の事業者が運営する Web サイトに侵入され、本省と在外公館の職員の名前と公用の連絡先を読まれた
- **何が起きたか**: 外務省によると、侵入は 11/12〜13 に起き、封じ込めは済んだ。一般の人の個人情報は含まれていない。攻撃者は特定されておらず、侵入の方法や、実際に盗まれたかどうかも分かっていない。侵入は Microsoft の約 24 時間の障害と同じ時期だったが、関係は確認されていない。同省は 2019〜20 年にも数週間にわたる攻撃を受けており、2026 年 7 月にロシアの犯行と公式に認定している。
- **なぜ重要か**: 外交官の連絡先の一覧は、**標的型のフィッシングの宛先リスト**として価値が高い。委託先が運営するサイトが入口になった点は、国内の官公庁の Web サイトの委託管理にも当てはまる。
- 出典: [The Record (2026-11-23)](https://therecord.media/austrian-foreign-ministry-says-website-hacked)

### [2026-11-24] [続報] FBI の NCIC への侵入: トランプ大統領が「報告を受けた。よくない」と発言。FBI の今年 2 件目の侵害に
- **前回から何が変わったか**: 11/22 号では CNN の報道までを扱った。The Record によると、AP も、攻撃は木曜日に起きたと報じた。トランプ大統領は週末に Fox News で、報告を受けたと述べた。自分に関する捜査ファイルが公開されるおそれがあるとも話した。確認されれば、9 月に ShinyHunters が FBI の採用サイトに侵入した件に続き、FBI では今年 2 件目になる。FBI はコメントしていない。
- **なぜ重要か**: NCIC は州や地方の警察の端末から使われる。**接続している機関の数だけ入口がある**構造で、侵入の経路がどの機関の端末だったかが今後の焦点になる。
- 出典: [The Record (2026-11-23)](https://therecord.media/fbi-cyberattack-data-breach)

### [2026-11-23〜24] [続報] CISA、MONAI Label のパストラバーサル (CVE-2026-133968) を KEV に追加
- **前回から何が変わったか**: 11/22 号では、Cairn の件で悪用された医療画像サーバー MONAI Label の欠陥に CVE が採番されたこと、インストールできる修正版がまだないことを扱った。CISA は 11/23 にこれを KEV に追加した。
- **なぜ重要か**: AI エージェント (Cairn) が見つけた 0-day が KEV に入った最初期の例になる。修正版がないまま KEV に入ったので、連邦機関は**ネットワークからの切り離しや利用の停止**で対応することになる。
- 出典: [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) / [NVD CVE-2026-133968](https://nvd.nist.gov/vuln/detail/CVE-2026-133968)

### [2026-11-23] 政府機関を装って米国のスペイン語話者 3 万人超から金をだまし取った詐欺で、ペルーのコールセンターの運営者に禁錮 8 年
- **何が起きたか**: リマの Carla Magaly Alcedo Mendoza 被告 (45) は、郵便・通信詐欺の共謀の罪を認めた。2023 年 3 月に逮捕され、2025 年 4 月に米国に引き渡されていた。被告のコールセンターは、政府機関を名乗って米国に住むスペイン語話者を脅し、何年にもわたって数百万ドルを集めていた。
- **なぜ重要か**: 国内の「警察官を名乗る詐欺」と同じ型の、国をまたぐコールセンター型の詐欺に、引き渡しから判決まで進んだ例。
- 出典: [BleepingComputer (2026-11-23)](https://www.bleepingcomputer.com/news/security/call-center-operator-gets-8-years-for-helping-scam-30-000-americans/)

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 today-2 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-133469 / GHSA-2r3w-c2vx-fv5g [続報: CVE 採番] | Xen Orchestra 6.9.2 / 6.10.1 より前、XOA | CWE-287 / 9.8 | `cookie-parser` が `j:` で始まる Cookie を JSON として解析 → `authenticationToken=j:{}` で `{}` が届く → 型を確かめずにトークンの検索に渡し、空のオブジェクトが「条件なしの検索」として最初のトークンを返す → 管理者として認証される | [diff](https://github.com/vatesfr/xen-orchestra/commit/50166fe3a49c02069d35ba9046ca4a1f77f4e11d) | **悪用中** (Vates)、NVD 公開 11/23 |
| CVE-2026-134624 | N-able Mail Assure (SpamExperts) ビルド 20261121.1943 より前 | CWE-918 / 9.3 (v4) | LDAP の同期の「接続の確認」で接続先を制限しない → 認証済みの API の利用者が内部の任意のホスト:ポートに接続させる → 内部の探索と、内部のサービスへのデータ送信 | [advisory](https://me.n-able.com/s/security-advisory/aArVy0000002mrlKAA) (commit 不明) | **KEV (11/23)** |
| CVE-2026-135208 / GHSA-3c52-7fc8-c39j | Kerberos Agent (監視カメラ) 3.14.4 より前 | CWE-1394 / 9.8 | `JWTMiddleWare()` が、鍵の設定がないとき固定の鍵 `TOBECHANGED` に戻る → 攻撃者が任意の利用者名と役割で HS256 のトークンを作る → `/api` と `/config` で RTSP / ONVIF の資格情報や暗号鍵を読み、設定を書き換え | [diff](https://github.com/kerberos-io/agent/commit/c0baade8fd6e21ed1b9a834d9ae6b4eaaa67b3b6) | 未認証、初期設定のまま |
| CVE-2026-134815 | simple-git 4.1.0 より前 | CWE-88 / 9.2 (v4) | `allowUnsafePack` のガードが push 以外の操作の `--exec` を見ていない → `listRemote()` / `raw()` の引数に `--exec` を入れる → `ls-remote` / `archive` / `fetch-pack` 経由でコマンド実行 | [diff](https://github.com/steveukx/git-js/commit/c8ee6bb4dd0c1259af31da821dc68d74ff5d6f10) | EPSS 0.0075、過去の同種の修正の回避 |
| CVE-2026-134814 / GHSA-xmxc-6c22-m377 | binary-parser 2.3.1 より前 | CWE-94 / 9.2 (v4) | `Context.generateOption()` が、文字列のオプション (`length` / `key` / `offset` / `namely()` の別名など) を検証せずに生成コードに埋め込む → パーサの定義を操れる攻撃者がコンパイルの時に任意の JS を実行。CVE-2026-1245 の不完全な修正 | [diff](https://github.com/keichi/binary-parser/commit/110206bb126a80071158fb0e2e3d7cc658f2bfe4) | 不完全な修正の 2 回目 |
| CVE-2026-135300 | Pomerium 0.30.0〜0.34.0 より前 | CWE-287 / 9.1 (v4) | MCP のトークンエンドポイントが `client_secret_basic` のシークレットを検証しない → 盗んだ認可コードやリフレッシュトークンを任意のシークレットで交換 → 被害者のアクセストークンを取得 | [diff](https://github.com/pomerium/pomerium/commit/f86d7c00ad98ba74a662fea6bbc53ca57c3f1741) | MCP / OAuth |
| CVE-2026-134838 | Weblate 2026.11 より前 | CWE-178 / 9.1 (v4) | パスワードリセットで、Unicode の大文字小文字を区別しない比較で利用者を探す → 点のない i などの紛らわしいアドレスで申請すると、リセットのリンクが入力したアドレスに届く → 被害者のアカウントを乗っ取り | [diff](https://github.com/WeblateOrg/weblate/commit/8340ccd9dee8c6d0586e62c19697c3de2c42ffd2) | 未認証、ATO |
| CVE-2026-134841 / GHSA-4743-5rfh-f7mp | pgjdbc 42.7.15 より前 | CWE-89 / 8.1 | クエリのパーサがリテラルを読み違える (`{ts}` の中の `}`、非 ASCII のタグのドル引用、`E''` の二重引用、`{fn right}` に負の引数で `--`) → アプリが正しくエスケープした文字列の続きが SQL として実行される | [advisory](https://github.com/pgjdbc/pgjdbc/security/advisories/GHSA-4743-5rfh-f7mp) (commit 不明) | Java の全 PostgreSQL 利用者 |
| CVE-2026-134842 / GHSA-6rxc-3r4p-gpff | pgjdbc 42.7.15 より前 (`preferQueryMode=simple`) | CWE-89 / 8.1 | セッションの途中で `standard_conforming_strings` が off に変わっても、ドライバは古い前提で引用する → `\'` で引用が閉じて SQL インジェクション。EUC_JP / SJIS では円記号がバックスラッシュとして働く | [advisory](https://github.com/pgjdbc/pgjdbc/security/advisories/GHSA-6rxc-3r4p-gpff) (commit 不明) | **国内の SJIS 環境に直接影響** |
| CVE-2026-135175 / GHSA-qvxq-53gh-64f6 | ZITADEL 4.19.5〜4.20.3 より前 | CWE-640 / 8.6 (v4) | `x-zitadel-public-host` ヘッダの userinfo の部分に信頼済みのホストを置くと検査を通る (`trusted@evil`) → パスワードリセットのリンクが攻撃者のホストに向く → 1 回限りのコードを取り、管理者を含むアカウントを乗っ取り | [diff](https://github.com/zitadel/zitadel/commit/8ce0ac5942d23017038a53a06d4f2f698bf1ac04) | IdP、未認証 |
| CVE-2026-82446 | Apache StormCrawler 3.0.0〜4.0.0 より前 | SSRF・資格情報の漏えい / moderate | robots.txt の取得のリダイレクトを最大 5 回、スキーム・ホスト・ポートを確かめずに自前で追う → 内部のアドレスやメタデータに届き、okhttp の `Authorization` の除去も効かない → クロールの資格情報を第三者のホストに送る | [advisory](https://seclists.org/oss-sec/2026/q4/845) (commit 不明) | AI で発見 (ASF) |
| CVE-2026-82445 | Apache StormCrawler (stormcrawler-sql) 3.0.0〜4.0.0 より前 | メタデータの注入 / important | URL ごとのメタデータを「タブ + key=value」でエスケープせずに連結して保存 → `Location` にタブを入れると、読み戻しで制御用のキー (`http.proxy.host` など) が増える → 以降の取得が攻撃者のプロキシを通る | [advisory](https://seclists.org/oss-sec/2026/q4/844) (commit 不明) | 区切り文字の注入 |
| CVE-2026-134816 / GHSA-9mj6-f434-pgcg | @sigstore/oci 0.8.0 より前 | CWE-201 / 8.2 (v4) | OAuth2 のパスワードグラントの POST の本文を、別のオリジンへの 307 / 308 のリダイレクトでもそのまま送り直す → 攻撃者のホストにレジストリの利用者名とパスワードが届く | [diff](https://github.com/sigstore/sigstore-js/commit/7ca56e9d068458642fc8a148c4916717b6918bec) | 供給網 |
| CVE-2026-86312 | Apache Solr 9.0.0〜9.11.0 / 10.1.0 より前 | CWE-441 / 8.8 | `/admin/ping` が健全性の確認以上の処理を代行する → `health` の権限しかないクライアント (同梱の `security.json` では未認証) が、高い権限の動作を起こせる | [PR](https://github.com/apache/solr/pull/4890) | 初期テンプレートで未認証 |
| CVE-2026-134793 | Electerm 5.9.0 より前 (Windows) | CWE-78 / 8.5 (v4) | フォルダのサイズを計算する PowerShell のコマンドで、ファイル名を ASCII の引用符だけでくくる → `’` (U+2019) を含む名前で引用を抜ける → 名前を見ただけでコマンド実行 | [diff](https://github.com/electerm/electerm/commit/488b112d10dc21545f18284d4eb52db6dafb7f31) | Unicode の引用符 |
| CVE-2026-107784 | CPython (Windows) の `tarfile` の `tar` / `data` フィルタ | CWE-22 / 6.3 (v4) | `C:foo` のような「ドライブはあるがルートがない」名前をフィルタが拒否しない → 相対の展開先のとき、そのドライブのカレントディレクトリに書き込む / リンクが展開先の外を指す | [PR](https://github.com/python/cpython/pull/161334) | フィルタの回避 |
| CVE-2026-134703 | libexpat 2.10.0 まで (`XML_UNICODE` ビルド) | CWE-176 / 6.3 (v4) | 出力の領域が足りないとき、UTF-16 から UTF-16 への変換がサロゲートペアを分割する → 単独の上位サロゲートが文字データのハンドラに届く (CVE-2022-25235 系と同種) | [diff](https://github.com/libexpat/libexpat/commit/702389c818cb402f2423fa998fa11907d621959f) | 2.11.0 で 3 件修正 |

**今日の CVE 所感**:
- 最も多いのは「**値の型や形を、受け取った側が確かめていない**」型だ。Xen Orchestra (文字列のはずのトークンが `{}`)、binary-parser (識別子のはずのオプションが式)、StormCrawler (区切り文字を含む値)、ZITADEL (ホストのはずのヘッダに userinfo) がこれにあたる。Express で `cookie-parser` を使うアプリでは、`req.cookies.X` を検証せずに DB や ORM の検索に渡していないかを grep で確かめたい (`j:` の接頭辞で、どのアプリでもオブジェクトを送れる)。
- **リダイレクトで資格情報が漏れる**型が 2 件 (StormCrawler、sigstore-js) あった。HTTP クライアントのライブラリの除去の処理を通らない「自前のリダイレクトの追跡」が共通の原因で、クローラ、パッケージマネージャ、レジストリのクライアントに広く当てはまる。
- pgjdbc の 2 件は、**国内の SJIS / EUC_JP 環境では円記号がバックスラッシュとして働く**点が重い。古い Java の業務システムで `preferQueryMode=simple` や `allowEncodingChanges=true` を使っていないか、構成を確認する価値がある。
- 認証のバイパスは、MCP (Pomerium)、ローカル向けの機能 (Gradio)、ワークフローの公開 API (BISHENG) と、**AI 向けに後から足した入口**に集中している。

## 日本国内のセキュリティ動向

### 国内インシデント・事故

> 直近2日間に該当する新規ニュースは確認できませんでした。

(11/21〜23 は三連休で、piyolog、Security NEXT、ScanNetSecurity の新着は 11/20〜21 の掲載分が最新だった。これらは前号までに収録済み。下は、採用範囲の中で公開された解説記事で、新しい事実を含むもの。)

#### [2026-11-24] [続報] ユミルリンク「Cuenote FC」の延べ約 4,786 万件の流出: 確認された攻撃の手口は 2 種類。脆弱性からの DB の直接の持ち出しと、管理画面のセッションを盗んで正規の CSV のダウンロードを使うもの (日経クロステック、piyokango 氏)
- **何が起きたか**: 記事によると、ユミルリンクの 11/11 の第 3 報で、Cuenote FC の 49 システムから配信先のメールアドレス延べ約 4,786 万件が持ち出されたことが確認された。会員 ID 約 3,050 万件、氏名約 666 万件、ハッシュ化されたパスワード約 23 万件を含む (すべて延べの件数)。顧客管理の「Cuenote BASE」でも 190 件が第三者から閲覧できる状態だった。攻撃の手口は 2 種類だった。1 つは、プログラムの脆弱性を突いてサーバーに不正なプログラムを置き、DB に直接アクセスして持ち出し、内部のネットワーク経由で別のサーバーにも広げたもの。もう 1 つは、ログイン中の正規の利用者のセッション情報を盗み、管理画面の**元からある CSV のダウンロード機能**で持ち出したもの。後者は正規の操作に見えたため、詳しいログの解析で初めて分かった。同社は 10/16 の朝に異常を検知し、その日のうちに攻撃元の IP を遮断して修正パッチを当てていた。
- **なぜ重要か (評価)**: 「脆弱性を塞いだ後」に、**盗まれたセッションで正規の機能を使う持ち出し**が続いていた。パッチの適用だけでなく、セッションの全失効と、エクスポート機能の利用ログの確認が、封じ込めの手順に要ることを示している。メール配信の ASP は委託元が多く、この 1 社から Peach Aviation などへ被害が広がっている (11/23 号)。
- 出典: [日経クロステック (2026-11-24)](https://xtech.nikkei.com/atcl/nxt/column/18/00598/011300391/)

### 国内の注意喚起・ガイドライン・政策

> 直近2日間に該当する新規ニュースは確認できませんでした。

(JPCERT/CC の注意喚起と CyberNewsFlash は 11/20 の PHP の注意喚起の更新、IPA の重要なセキュリティ情報は 11/20 の PHP が最新だった。NCO (国家サイバー統括室)、警察庁、総務省、経産省、金融庁、個人情報保護委員会でも、11/22〜24 の新着は確認できなかった。日経クロステックの 11/24 の記事「相次ぐサイバー攻撃、漏洩メアドが次の標的に 努力不足の企業に罰則強化論」は、専門家へのインタビュー (会員限定) で、政府の発表ではないため参考にとどめる。[日経クロステック (2026-11-24)](https://xtech.nikkei.com/atcl/nxt/column/18/03671/111600013/))

### 国内製品の脆弱性 (JVN)

> 直近2日間に該当する新規ニュースは確認できませんでした。

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| — | — | — | 11/22〜24 の JVN の新着なし (最新は 11/20 公開の SoftBank Airターミナル6 などで、前号までに収録済み) | — | [JVN](https://jvn.jp/) |

(JVN iPedia の新着も 11/19 登録分が最新だった。国内の利用者に直接関わる海外の CVE として、上の表の **pgjdbc の CVE-2026-134842 (SJIS / EUC_JP で円記号がバックスラッシュとして働く)** を挙げておく。)

### 国内コミュニティ・研究・イベント

#### [2026-11-23] (AI セキュリティ欄に掲載) CODE BLUE 2026 での Rubrik の「ChatMate」の解説と、Claude Code の PreToolUse フックの時間切れの検証
- 上の「AI セキュリティ」欄を参照。CODE BLUE 2026 (11/18) に合わせた Copilot のサンドボックスの脱出の解説と、国内の開発者による、エージェントの安全装置が時間切れで「通す」側に倒れる挙動の再現。
- 出典: [ITmedia エンタープライズ (2026-11-23)](https://www.itmedia.co.jp/enterprise/articles/2611/23/news001.html) / [Zenn 上条碧斗 (2026-11-23)](https://zenn.dev/kamijo_aoto/articles/claude-code-hook-timeout-passes)

#### [2026-11-24] 岡山県精神科医療センターのランサムウェアの調査報告書の解説: 「閉域網」のはずが、保守用の VPN は接続元を制限せず、推測しやすいパスワードと未修正の脆弱性が残っていた (Zenn)
- **何が起きたか**: 四角いぱおつき氏は、Software ISAC の調査委員会が 2025 年 2 月に公表した報告書を、ページを示しながら整理した。2024 年 5 月に、仮想サーバー 23 台、物理サーバー 9 台、端末 244 台などが暗号化された。電子カルテの完全な復旧まで 90 日 (約 65 人月) かかった。共有フォルダから最大約 4 万人分 (推定) の患者の情報が盗まれた。侵入は保守用の VPN 装置からとされている。調査委員会は、ガイドラインの理解不足、過去の事例の軽視、「閉域網」への過信を原因に挙げた。
- **なぜ重要か (評価)**: 事案は過去のもの (背景) だが、医療機関の診断やペンテストで**「閉域網」と説明されたときに最初に確かめる点** (保守用の VPN の接続元の制限、管理者のパスワードの共通化、バックアップの隔離と復元の試験) が、報告書のページ付きでまとまっている。顧客への説明の資料として使いやすい。
- 出典: [Zenn 四角いぱおつき (2026-11-24)](https://zenn.dev/paokkyu/articles/okayama-psychiatric-ransomware-2024)

#### [2026-11-23] 国内: 「読み取り専用の DB アカウントは安全境界にならない」(AI 脆弱性診断の観点)、PHP2Shell と 11/19 の PHP のリリースの影響の確認手順など、Zenn で実務寄りの記事が続く
- **何が起きたか**: Zenn のセキュリティのトピックでは、11/23 に、読み取り専用の DB アカウントでもファイルの読み出しや外部への接続などで境界を越えうることを AI 脆弱性診断の観点で整理した記事 (hackbox_ai)、PHP2Shell と 11/19 の PHP のセキュリティリリースについて自分の環境が影響を受けるかを確かめる手順 (quantumaisafe)、WSL Containers で Claude Code を隔離する手順 (kent_code) などが公開された。
- **なぜ重要か (評価)**: どれも一次情報ではないが、診断の報告書で「読み取り専用だから低リスク」と書かれがちな指摘を見直す材料や、連休明けにパッチの適用の状況を確かめる手順として使える。
- 出典: [Zenn hackbox_ai (2026-11-23)](https://zenn.dev/hackbox_ai/articles/9df8658d7b187c) / [Zenn quantumaisafe (2026-11-23)](https://zenn.dev/quantumaisafe/articles/079d0a658a2417) / [Zenn kent_code (2026-11-23)](https://zenn.dev/kent_code/articles/bef81d6a0b817c)

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 53 (RSS / Atom 53 本 + NVD API + CISA KEV JSON + EPSS API + OSV API + 記事本文の取得 約 45 件 + WebSearch 7 回)
- 採用件数: AI技術=10 / AIセキュリティ=6 / セキュリティ=12 / CVE=17 / 国内インシデント=1 (続報・解説のみ) / 国内政策=0 / JVN=0 / 国内コミュニティ=3
- 除外理由内訳: 古すぎ=約 40 (国内 RSS の 11/19〜21 掲載分全般、OpenRouter の量子化の検証 [原典 11/11、GIGAZINE の紹介は 11/23]、UnrealIRCd 6.2.7.1 [11/7 の告知の転送]、六花亭の第 2 報 [11/21 朝]、JETRO の続報 [11/6]、CVE-2026-131914 の NVD 登録 [11/19、ニュースの欄でのみ扱った]、Cisco Expressway / SAP NetWeaver / vCenter の KEV 追加 [11/20、前号まで]) / 重複=約 25 (OpenRouter の推論事業者の件、Ghostscript Upload2Shell、Rackspace Spot、Cleverbridge、Entra Connect Health、BADBOX 3.0、Signal の画面撮影の制限、Webworm の SoftEther、Cairn の Amazon の報告、phpAfterShell、ScreenConnect CVE-2026-84869 の Huntress の観測、メルカリと Fireworks AI、Bell Canada、DaisyRose-27B、OpenAI の「Perplexity and Intelligence」など) / 日付不明=2 (GLM-5.4 [集約サイトのみ、一次の発表を確認できず]、MindStudio の原典の日付)
- 取得失敗ソース: CISA の advisories の RSS (XML の不正) → KEV の JSON で代替。GitHub Advisory の Atom と GitHub API (このセッションではリポジトリの外が 403) → NVD API の参照の欄と OSV API で代替し、修正コミットの URL は NVD に載っているものを使った (diff の中身は未確認)。Google TI (GTIG) の RSS (解析不可)、MSRC のブログの RSS (XML の不正)、Dark Reading の記事本文 (空) → 同じ話題を Help Net Security と The Hacker News で代替。arXiv cs.CR (採用範囲の中の新規投稿の確認ができず、採用なし)。CNET Japan / ZDNET Japan の RSS (XML の不正)。ITmedia エンタープライズは Shift_JIS のため iconv で変換して取得した。
- 備考: 国内は 11/21 (土)〜23 (月・勤労感謝の日) の三連休で、一次情報の新着がほぼなかった。11/24 の朝に各組織の公表がまとめて出る可能性が高く、次号で拾う。

</details>
