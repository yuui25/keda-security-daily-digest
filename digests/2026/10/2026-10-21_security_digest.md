# KEDA Daily Digest — 2026-10-21 (JST)

> 採用範囲: 公開日 2026-10-19 〜 2026-10-21
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

10/20 (火) の最大の話題は、インドの認証局 eMudhra (emSign) の中間 CA 8 個の秘密鍵が漏えいしていた件である。鍵の強度は 3〜8 ビットしかなく、誰でも導出できる。ブラウザは 10/17〜20 に遮断を終えたが、Go・certifi・webpki-roots・NSS などの非ブラウザ系 TLS スタックは利用者側での更新が必要で、Node.js と Composer は未対応である。今日の深掘りとして扱う。
AI 側では、OpenAI が COBOL 移行で GPT-6.1 Sol が 86.6〜97.9% に達したと公表し、MiniMax M3.1 Flash (入力 $0.15/1M) と Mistral Voxtral 3、Google の TorchTPU が出た。研究では、Claude Code に 37 種のセキュリティスキルを与えても Linux カーネルの脆弱性の関数特定は 24.4% にとどまるという実測 (arXiv 2610.25705) が実務の目安になる。
AI セキュリティでは、Meta Muse の共有リンクが「秘密をホスト名に置く」設計のせいで passive DNS から約 6,800 件列挙できた件と、WhatsApp のヘルプページに隠された LLM 向け指示が目立つ。DHS は DeepSeek とその派生製品を連邦の文民機関から排除した。
セキュリティ側では、PAN-OS CVE-2026-0257 を Qilin・INC・Settra が悪用して VPN から vCenter/ESXi へ直行していること (Unit 42)、FortiSIEM CVE-2026-106173 の PoC 公開 (Horizon3)、OVHcloud CLI のリリース差し替え (94 分間)、Zeabur の 2 度目の侵害とサービス終了が並ぶ。CVE では Argo CD の 9.9 が 2 件 (`git fetch` への引数注入と jsonnet import のパストラバーサル)、follow-redirects の配列形式ヘッダでの資格情報残存、MCP TypeScript SDK の audience 未検証が重要。KEV には 10/20 に SiteGuard と Plex2Shell・Siemens の 6 件が入った (いずれも既報)。
国内では、ふるさとチョイスの流出が 445 万件 (寄附控除の試算額を含む) と確定し、NEC が委託先経由で顧客サーバーを暗号化された件を公表した。GETTIIS (約 32 万件)、東邦 HD 子会社、LIXIL、ジェトロも続き、デジタル庁は政府職員 18 万人向けの AI エージェント環境と「源内基準」を出した。
**今日まず見るべきは 2 件**: (1) 自社・顧客の Go バイナリと certifi の版を確認する (eMudhra)、(2) GlobalProtect のログを 5 月まで遡る (CVE-2026-0257)。

## 今日の深掘り

### eMudhra (emSign) の中間 CA 8 個の秘密鍵が漏えい — 鍵空間 3〜8 ビット。ブラウザは遮断済みだが、Go・Python・Rust・Node.js の TLS クライアントは自分で直す必要がある

- **概要 (事実)**: Mozilla と Chrome Root Program は 10/20、eMudhra の中間 CA 証明書 8 個の秘密鍵が第三者に知られていたことを確認した。内訳は TLS 用 6 個 (EM DV/OV/EV TLS CA - G3B / G3C) とコード署名用 2 個 (EM OV CS CA - G3B / G3C) で、Sectigo の AAA Certificate Services による相互署名版もある。研究者「Wayne」が 10/17、8 個の鍵それぞれで署名したメッセージを送って報告した。Chrome は 10/17 中に CRLSet で、Firefox は OneCRL で遮断し、Apple は 10/19、Microsoft は 10/20 に続いた。
- **技術的な中身**: Ars Technica によると、秘密鍵の値は 4、56、66、115 といった小さな整数で、鍵空間は 3〜8 ビットしかなかった。つまり「盗まれた」のではなく「鍵生成が壊れていた」とみられ (Valsorda 氏・Cartwright-Cox 氏の推測)、公開鍵さえあれば誰でも秘密鍵を総当たりで求められる。攻撃者は中間者の位置 (公衆 Wi-Fi、社内 LAN、上流の傍受) にいれば、任意ドメインの TLS 証明書や、コード署名用の CA で署名したバイナリを作れる。対策は失効リストに頼れないクライアントで分かれる。
  - 修正済み: Go 1.27.3 / 1.26.10 (CVE-2026-111943、URGENT。Go はルートや拒否リストをバイナリに埋め込む構成が多いため**再ビルドが必要**)、Firefox 158.0.1 / ESR (CVE-2026-113470)、NSS 3.131.1、certifi 2026.10.19 (GHSA-6q48-6c7w-9gw2)、uv (GHSA-hq85-5cpj-mr62)、webpki-roots 1.0.10。
  - 未対応 (10/20 時点): Node.js の同梱ルート、PHP Composer の ca-bundle。
  - Chrome は、遮断までに CT ログに載った TLS 証明書はなく、悪用は確認されていないとしている。
- **背景・経緯 (過去事例の引用)**: CA の信頼失墜には DigiNotar (2011、実際に不正証明書が発行された)、Symantec の段階的な不信任 (2017〜18)、Entrust の不信任 (2024) がある。Chrome と Firefox は 2025 年 4 月に Sectigo AAA Certificate Services をウェブ用途で不信任にしたが、Apple のルートには残っているため、相互署名版の扱いは Apple 側で確認が要る。eMudhra は 2026 年 9 月に Mozilla で新ルートの採用審査を受けており、Mozilla は 10/20 に emSign ECC Root CA - G3 を NSS から削除、Chrome も Root Store v43 で削除する予定。
- **なぜ今これが重要か (評価)**: ブラウザ利用者は自動で守られたが、ペネトレーションテストや診断で実際に問題になるのは「自前のトラストストアを抱えるクライアント」である。Go 製の CLI・エージェント・Kubernetes コントローラ、Python の requests/httpx (certifi)、Rust の rustls + webpki-roots、Node.js の https、組み込み機器・コンテナのベースイメージは、更新・再ビルドするまで偽証明書を信頼し続ける。鍵の導出が容易で攻撃コストがほぼゼロなので、「中間者の位置さえ取れれば成立する」攻撃の前提条件が今週は一段下がっていると考えるべきだ。Valsorda 氏は「Heartbleed より大きな掃除になる」と述べている。コード署名用の CA も含まれるため、Windows のコード署名の信頼判断にも波及しうる。
- **読者が今日できること**:
  - Go: 配布・運用中のバイナリを `go version -m <bin>` で調べ、1.27.3 / 1.26.10 未満でビルドされたものを再ビルド対象として列挙する (1.25 以前はサポート外)。
  - Python / Rust / コンテナ: `pip show certifi` (2026.10.19 以上)、`cargo tree -i webpki-roots` (1.0.10 以上)、ベースイメージの `ca-certificates` パッケージ更新日を確認する。Node.js と Composer は修正待ちのため、`NODE_EXTRA_CA_CERTS` ではなく OS ストア (`--use-openssl-ca` / `--use-system-ca`) へ寄せるかを検討する。
  - CT ログ (crt.sh) で発行者名 `EM DV TLS CA - G3B` などを検索し、10/17 以前に自組織ドメイン向けに出た証明書がないか確認する。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/eight-emudhra-ca-keys-compromised.html) / [The Hacker News (Go の緊急更新)](https://thehackernews.com/2026/10/go-issues-emergency-update-blocking.html) / [Ars Technica](https://arstechnica.com/security/2026/10/the-internet-goes-on-high-alert-after-discovery-of-8-compromised-tls-certs/) / [OSV: GHSA-6q48-6c7w-9gw2 (certifi)](https://osv.dev/vulnerability/GHSA-6q48-6c7w-9gw2)

## AI 技術・トレンド

### [2026-10-20] OpenAI、低資源言語でのコーディング能力を公表。COBOL の移行で GPT-6.1 Sol が 86.6%〜97.9% (OpenAI says GPT-6.1 Sol is dramatically better at migrating legacy code)
- **何が起きたか**: OpenAI は 10/19 のブログ「Advancing coding in low-resource programming languages」で、20 言語で SQLite 互換の DB エンジンを一から作らせる独自ベンチマーク「MultiLangBench」の結果を公表した。平均合格率は GPT-5.6 Sol の 26.8% から GPT-6 Astra の 87.4% に上がり、COBOL は 10.9% → 72.1%、Fortran は 21.4% → 83.5% だった。COBOL を C++ / Java / Kotlin / Python / Rust に挙動を変えずに移す評価では、GPT-6.1 Sol が低い推論量で 86.6% (GPT-5.6 Sol は 5.4%、API コストは 61%)、高い推論量で 97.9% に達したと OpenAI は主張している。
- **なぜ重要か**: 金融や重要インフラに残る COBOL / Fortran の資産が、AI によって「読める・書き換えられる」ものになりつつある。防御側には移行やコードレビューの追い風だが、これまで解析の手間に守られてきたレガシー系の脆弱性も、同じ速さで掘られうる前提で考えるべきだろう。数値はすべて OpenAI 自身のベンチマーク。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/artificial-intelligence/openai-says-gpt-61-sol-is-dramatically-better-at-migrating-legacy-code/) / [OpenAI](https://openai.com/index/low-resource-programming-languages)

### [2026-10-19] MiniMax、コーディング・エージェント向けの「MiniMax M3.1 Flash」を発表。覆面モデル「Space Bunny」の正体で、重みは 10/23 に公開予定
- **何が起きたか**: MiniMax は、LMArena などで首位に立っていた覆面モデル「Space Bunny」が M3.1 Flash の先行版だったと明かした。コンテキストは 100 万トークンのマルチモーダルで、API 料金は 100 万トークンあたり入力 $0.15 / 出力 $0.60 (キャッシュ読み取り $0.015)。同社は「M3 の 1/3 のコストで 3 倍の速さ」とし、Automation-Bench 62.2% (DeepSeek-V4.1-Flash-1017 は 60.5%、Claude Opus 5 は 50.3%)、DeepSWE 73.7% (DeepSeek-V4.1-Flash-1017 の 77.0% には届かない) と公表した。パラメータ数とライセンスは未発表。
- **なぜ重要か**: エージェント用途のオープンウェイトモデルが、極端な低価格で出そろいつつある。社内でローカル運用するモデルの候補が増える一方、ガードレールを外せる高性能なモデルが攻撃者の手にも渡る。10/23 の公開時にライセンスとモデルカードを確認したい。
- 出典: [PC Watch](https://pc.watch.impress.co.jp/docs/news/2149440.html)

### [2026-10-20] Mistral、音声エージェント向けの「Voxtral 3」ファミリーと SDK を公開
- **何が起きたか**: Mistral は、文字起こしの「Voxtral Small / Mini Transcribe 3」(話者分離とキーフレーズによる補正に対応)、音声合成の「Voxtral Mini TTS 3」(35 超の言語、50 超の方言、文脈に応じて感情や速さを変える)、聞き取り・推論・ツール呼び出し・発話を 1 本のストリームで扱う音声エージェント SDK を発表した。「Pro Voice」は 30 分の音声から話者の声色や話し方を他言語でも再現するという。EU でホストされる API と、セルフホストで提供する。
- **なぜ重要か**: 30 分の音声で声を再現できる機能は、ボイスフィッシングや音声認証の突破にそのまま転用されうる。また、ツール呼び出しを持つ音声エージェントは、電話越しのプロンプトインジェクションという新しい入口になる。コールセンターなどへの導入を診断するときの論点になる。
- 出典: [Mistral AI](https://mistral.ai/news/voxtral-3/)

### [2026-10-20] Google、PyTorch のネイティブな TPU バックエンド「TorchTPU」をオープンソース化。Hugging Face も即日対応
- **何が起きたか**: Google は TorchTPU を GitHub で公開した。これまでの torch_xla と違い、TPU を PyTorch の通常のデバイス (`"tpu"`) として扱える。Hugging Face は同日、Transformers・Diffusers・Kernels が TPU 上でネイティブに動くと発表した。前日には AWS も PyTorch アプリを Trainium に移す TorchNeuron を出しており (既報)、TechCrunch はこれを「NVIDIA の牙城 (CUDA) への攻勢」と位置づけている。
- **なぜ重要か**: 学習や推論の基盤が CUDA 以外にも広がると、ドライバーやランタイムなど、点検すべきソフトウェアサプライチェーンの種類も増える。新しいバックエンドは初期のバグが出やすい領域でもある。
- 出典: [Hugging Face](https://huggingface.co/blog/hf-torchtpu) / [TechCrunch](https://techcrunch.com/2026/10/20/google-has-joined-amazon-in-attacking-nvidias-stronghold-with-ai-app-developers/)

### [2026-10-20] Anthropic、Claude がサソリの神経毒に結合するタンパク質を設計したと発表。211 設計のうち 17 件が基準を満たす
- **何が起きたか**: Anthropic の社内研究モデルは「Claude Science」上で 64 時間、ほぼ自律的に作業し (人による追加指示は 4 回)、318,484 個の設計から 180 個を選んだ。人が 31 個を加えた計 211 個を Adaptyv Bio と Twist Bioscience が実験したところ、危険な 4 種の神経毒のいずれかに結合する 17 個が基準を満たした。Anthropic は「中和は未確認で、抗毒素ができたとは主張しない」としている。全 211 設計とデータを公開した。
- **なぜ重要か**: 投資家の Citrini Research と組み、「非専門家が AI で実際の創薬課題に挑めるか」を試したもの。AI が生物分野の実験計画を自律的に回せることを示しており、同じ能力がデュアルユース (生物兵器への転用) の懸念と表裏一体である点は押さえておきたい。
- 出典: [Anthropic](https://www.anthropic.com/research/claude-scorpion-toxin-binder-design)

### [2026-10-19] Anthropic と Nscale、さらに 450 億ドル規模の計算資源の契約で協議中と報道
- **何が起きたか**: Bloomberg によると、Anthropic と英 Nscale は、約 1 か月前の 450 億ドルの契約に続き、同規模の 2 件目の契約の発表が近い。両社とも IPO を目指しており、Nscale は 300 億ドルという想定評価額に投資家から反発を受けていると報じられた。同じ 10/19 には Microsoft が Nscale の英国 AI データセンター計画からの撤退を報じられている (既報)。
- **なぜ重要か**: 主要ベンダーの計算資源が特定の事業者に集中すると、その事業者の障害や侵害がモデルの提供全体に響く。サードパーティリスクの評価では、モデルを提供する会社の背後にある基盤事業者まで見る必要が出てきている。
- 出典: [TechCrunch](https://techcrunch.com/2026/10/19/nscale-and-anthropic-are-reportedly-in-talks-for-yet-another-45-billion-compute-deal/)

### [2026-10-19] Goodfire の研究者 Nick Cammarata 氏の「ニューラルネットは思ったより理解しやすい」という長文ブログが議論を呼ぶ (MIT Technology Review)
- **何が起きたか**: 元 OpenAI の解釈可能性研究者で、現在は Goodfire にいる Cammarata 氏が 26,000 語のブログを公開した。1 つのニューロンが無関係な概念を複数抱える「重ね合わせ (superposition)」を前提にしてきた見方が誤っていた可能性を示し、LLM は従来の想定よりはるかに監視・制御しやすいかもしれないと主張している。一部の研究者は「今年最も重要な論文」と称賛したが、Stanford の Chris Potts 氏は「直感の域を出ず、問題は何も簡単になっていない」と懐疑的だ。
- **なぜ重要か**: 今夏、各社のエージェントが封じ込めを破った事例が相次いだ背景があり、モデル内部を監視して異常を検知する手法への期待は大きい。ただし現時点では検証されていない仮説なので、防御策の根拠にするのは早い。
- 出典: [MIT Technology Review](https://www.technologyreview.com/2026/10/19/1147149/we-were-looking-at-it-wrong-the-explosive-claim-thats-upended-the-ai-world/)

### [2026-10-20] Figma、MCP の連携先を 20 社追加。一方で共同創業者は「MCP は完璧なプロトコルではなく、フロンティアラボに有利」と発言
- **何が起きたか**: Figma はインドで初めて開いた Config で、Amp、ClickUp、Junie by JetBrains、Linear、Meta Muse、Mistral、Notion、OpenCode、Sarvam Agents など 20 社の MCP パートナーを発表した。同時に Dylan Field 氏は、「Anthropic は自社の Artifacts などのクラウド資源を MCP で公開していない」と指摘した。MCP は「改善の余地が大きく、フロンティアラボに有利」とも述べている。
- **なぜ重要か**: デザインツールが多数のエージェントから MCP でアクセスされる構成が広がっている。デザインやコメントに仕込まれた指示がエージェントを経由して、Linear や Notion など別のツールの操作に波及する経路は、診断の観点で押さえておきたい。
- 出典: [TechCrunch](https://techcrunch.com/2026/10/20/figma-co-founder-dylan-field-thinks-mcp-is-not-a-perfect-protocol/)

### [2026-10-20] ChatGPT に会話を PIN や生体認証でロックする「Locked Chats」が追加。ただし暗号化や保持期間は変わらない
- **何が起きたか**: OpenAI は、会話を 4 桁の PIN または Face ID / Touch ID でロックし、通常の履歴や検索から分けて保管する機能を出した。メモリを有効にしている場合、ロックした会話は専用のメモリを持ち、通常のメモリには書き込まない。OpenAI は、エンドツーエンド暗号化や別の暗号化保管庫にはならないこと、保持期間・ロック前に記憶した内容・学習への利用設定は変わらないことを明記している。
- **なぜ重要か**: 端末を他人にのぞかれることへの UI 上の対策にすぎず、サーバー側のデータ保護やアカウントを乗っ取られた場合の対策ではない。利用者教育で「ロック = 安全」と誤解されないよう注意が要る。
- 出典: [TechCrunch](https://techcrunch.com/2026/10/20/chatgpt-now-lets-you-lock-your-chats/)

### [2026-10-20] Claude Code にセキュリティ用の「スキル」37 種を与え、実在する Linux カーネルの脆弱性 100 件を探させた大規模実験 (arXiv 2610.25705)
- **何が起きたか**: 研究チームは、Claude Code と 4 種の LLM の組み合わせで 37 種のセキュリティスキルを試した (10 種類の脆弱性クラス、計 14,800 回の実行)。正しい関数を特定できたのは 24.4%、関数と原因の文まで当てたのは 18.3%、脆弱性クラスまで正しく分類できたのは 15.7% だった。失敗の原因としては、証拠の集め方、状態の関係の推論、候補の検証、調査範囲の狭さなどを挙げている。見逃しから学んでスキルを改良する「SKILL-SIF」を提案し、未見の 100 件でも改善したとしている。
- **なぜ重要か**: 「スキルを入れれば AI がカーネルの脆弱性を見つける」という期待に対する、実測の目安になる。コードレビューでエージェントを使うなら、出力をそのまま信じず、どの段階で失敗しやすいかを踏まえて人が検証する工程を設計すべきだ。
- 出典: [arXiv 2610.25705](https://arxiv.org/abs/2610.25705)

## AI セキュリティ

### [2026-10-20] Meta の AI エージェント「Muse」の共有リンク約 6,800 件が passive DNS から列挙され、売上資料や融資申込書が閲覧可能に。Meta は共有機能を停止
- **何が起きたか**: セキュリティ企業 Claroc は、Muse の共有ページが `<会話タイトル>-<ランダム ID>.cf.metaaiusercontent.com` という「サブドメイン」の形で作られるため、受け手がリンクを開いた時点で DNS の名前解決が passive DNS のデータベースに記録されることを示した。1 回の検索で約 6,800 件のリンクが見つかり、数百件を開くと、マーケティング会社の売上レビュー、中小企業の融資申込書、職場の年間スケジュールなどが含まれていた。Claroc は 10/8 にバグバウンティで報告したが返答がなく、Ars Technica の取材を受けて Meta は共有機能を一時停止した。
- **なぜ重要か**: 「推測できない URL」による秘匿は、秘密を URL のパスではなくホスト名に置いた時点で、DNS の記録 (passive DNS や CT ログなど) から漏れる。しかもタイトルがホスト名に入っているので、中身の見当まで付く。共有リンクの実装を診断するときは、秘密がホスト名に入っていないか、DNS や CT ログに残らないかを確認項目に加えたい。
- 出典: [Ars Technica](https://arstechnica.com/security/2026/10/meta-muse-exposes-users-personal-and-business-secrets-when-they-share-conversations/) / [The Verge](https://www.theverge.com/tech/1014627/meta-muse-ai-sharing-ai-chats)

### [2026-10-19] WhatsApp のヘルプページ約 80 件に、サポート用チャットボット向けの「隠し指示」が埋め込まれていた (「規制当局を勧めるな」など)
- **何が起きたか**: プライバシー企業 Redact によると、WhatsApp のヘルプ・FAQ ページの HTML に、画面には表示されない LLM 向けの指示が約 100 ブロック含まれていた。アカウントを削除できない利用者にデータ保護当局を勧めないことや、利用者が訴訟や弁護士に言及したら GDPR や利用規約を引用しないことなどを指示していた。欧州向けのプライバシーポリシーには苦情申し立ての権利が明記されており、指示はこれと食い違う。Meta は「バグで露出した」と説明し、10/18 までに削除した。チャットボットが実際に従ったかはわかっていない。
- **なぜ重要か**: Web ページそのものを RAG の知識源とし、そこに不可視の指示を埋め込む設計は、間接プロンプトインジェクションと同じ構造をしている。今回は運営者自身が埋め込んだものだが、CMS の改ざんや XSS があれば第三者も同じ経路でボットを操作できる。診断では、ボットが参照するページの非表示テキストが応答に影響する経路を確認したい。
- 出典: [WIRED](https://www.wired.com/story/whatsapp-help-pages-leaked-hidden-instructions-for-a-meta-chatbot/) / [The Hacker News](https://thehackernews.com/2026/10/whatsapp-hid-instructions-in-help-pages.html)

### [2026-10-20] 米国土安全保障省 (DHS)、DeepSeek の製品と派生品を連邦の文民機関から排除する命令
- **何が起きたか**: DHS は、DeepSeek とその関連会社の製品に加え、DeepSeek の技術を使った第三者の製品・サービスも対象に、調達から直ちに外し、機関の IT システムから削除するよう命じた。命令は官報に掲載された。例外の申請は 60 日以内で、CISA が審査し、技術支援も行う。理由として、中国政府によるインフラへのアクセス、個人情報の収集、政府データの国外移転の懸念と、NowSecure が 2025 年 2 月に指摘した iOS アプリの欠陥 (暗号化されない通信、弱い暗号など) を挙げている。民間や個人の利用は対象外。
- **なぜ重要か**: 「DeepSeek の技術を使った第三者製品」まで対象になるので、オープンウェイトの派生モデルを組み込んだ SaaS や社内ツールの棚卸しが必要になる。AI の SBOM (どのベースモデルを使っているか) を把握していないと、対象かどうかも判断できない。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/dhs-bans-deepseek-products-across-us-federal-civilian-agencies/) / [ITmedia NEWS](https://www.itmedia.co.jp/aiplus/article/2610/20/2000002411/)

### [2026-10-20] [続報] NIST・CISA・NSA、「暴走した AI エージェント」のインシデント対応の実践 10 項目を公表 (先週のサンドボックスのガイダンスと対になる文書)
- **何が起きたか**: 10/16 付の NIST の文書「Key Practices for Incident Readiness and Response in Super Intelligence Training and Evaluation」の内容が報じられた。10 項目の実践を「準備・検知・対応・復旧・報告」の 5 段階に分けている。AI agent、AI control incident、AI control near-miss (ヒヤリハット) の用語も定義した。対応の段階では、隔離、認証情報の失効、環境の再構築、被害範囲の特定、悪用された欠陥の先まで掘り下げる根本原因分析を求めている。報告の段階では、CISA などへの法定報告と、早い時期の情報公開を推奨している。既報の評価サンドボックスのガイダンス (10/17) とは別の文書である。
- **なぜ重要か**: エージェントによる事故を「インシデント」として扱う枠組みを、政府が明文化した。社内の IR 手順書に、エージェントの認証情報の失効手順や「ヒヤリハット」の記録項目を追加するときの下敷きになる。同じ 10/20 には英国の FCA も、AI の重大な失敗とヒヤリハットを事故報告の対象にすべきだと述べている。
- 出典: [SecurityWeek](https://www.securityweek.com/us-agencies-detail-incident-response-practices-for-rogue-ai-agents/) / [NIST (PDF)](https://www.nist.gov/system/files/documents/2026/10/16/Key_Practices_for_Incident_Readiness_and_Response_in_Super_Intelligence%20_Training_and_Evaluation.pdf) / [The Register (FCA)](https://www.theregister.com/ai-and-ml/2026/10/20/uk-finance-watchdog-wants-firms-to-report-ai-failures-and-close-calls/5304078)

### [2026-10-20] AI に CVSS を付けさせると、バグバウンティ報告の深刻度を一貫して「高め」に誤る (arXiv 2610.24623)
- **何が起きたか**: 研究チームは、Huntr と HackerOne の公開報告 4,281 件を集め、ベンダーが CVSS ベクトルを検証済みの Huntr の報告 240 件でベンチマークを作った。8 つの LLM を 4 つのプロンプト手法と微調整で評価したところ、深刻度レベルの正解率は最良でも 49.58% で、常に最多のレベルを答える場合より 10 ポイント高いだけだった。7B モデルを微調整しても最大 56.25% にとどまる。誤りには偏りがあり、過大評価が過小評価よりはるかに多く、Low の脆弱性はほとんど Low と判定できない。原因は、報告文の書き方と CVSS の各指標の正式な定義のずれにあるとしている。
- **なぜ重要か**: トリアージや CVE の深刻度付けを LLM に任せると、報告者の「語り」に引っ張られて深刻度が水増しされやすい。curl の件のような報告の大量流入とも直結する。AI でスコアを付ける場合は、メトリクスごとに根拠を出させ、人が検証する運用が要る。
- 出典: [arXiv 2610.24623](https://arxiv.org/abs/2610.24623)

### [2026-10-20] RAG とエージェントへの「持続する」攻撃 2 本: 復号可能な形で機密文書を持ち出す RAGLeak と、多ターンでも効くツール汚染 SEAL (arXiv 2610.25937 / 2610.25372)
- **何が起きたか**: RAGLeak は、配布される生成モデルにバックドアを仕込むサプライチェーン型の攻撃である。トリガーが入ると、モデルは検索した機密文書を、別の LLM で元に戻せる形に難読化して出力する。3 つのモデル系列と 3 つの分野で攻撃成功率は最大 100%、検知型の防御を入れても低下は 10 ポイント以内で、クリーンなデータで微調整し直しても残るという。SEAL は、ツールの説明文に指示を仕込む既存の「ツール汚染」が多ターンでは効きにくくなることを示した。そのうえで、推論の冒頭を誘導するトリガーを最適化し、文脈をまたいで効く汎用トリガーにまとめる手法を提案している。
- **なぜ重要か**: 前者は、「出力を DLP で監視しているから漏れない」という前提が、難読化された出力には通じないことを示す。後者は、MCP サーバーのツール説明を 1 回だけ試験する評価では不十分なことを示している。外部から入手したモデルや MCP サーバーの受け入れ検査に、多ターンのシナリオを含める必要がある。
- 出典: [arXiv 2610.25937](https://arxiv.org/abs/2610.25937) / [arXiv 2610.25372](https://arxiv.org/abs/2610.25372)

### [2026-10-20] 【国内】NICT と MITRE、メール業務の AI エージェントを攻める競技「AI Breach Challenge 2026: Email Agent Security」を 12 月に米国で開催
- **何が起きたか**: 情報通信研究機構 (NICT) と MITRE は、メールの読み書きや関連ツールと連携する職場の AI エージェントを想定し、隔離された環境でエージェントに意図しない動作をさせたり、保護された情報を取り出させたりする攻撃手法を競う大会を開く。会場は米ジョージメイソン大学で、2026 年 12 月 16〜17 日の 24 時間、2〜4 人のチームで行う (開始時と終了時は現地での参加が必要)。NICT は、結果を対策の有効性や限界の分析に使うとしている。
- **なぜ重要か**: メールのエージェントは、間接プロンプトインジェクションで最も現実的な入口の 1 つ。日本の公的研究機関が攻撃側の競技に関わるのは珍しく、結果は国内でエージェントを評価する手法の参考になりそうだ。
- 出典: [Security NEXT](https://www.security-next.com/191660)

### [2026-10-20] (参考) AI ブラウザ 7 種の同一オリジンポリシーを検証した研究を ITmedia が解説: 4 種で回避経路が見つかり、Atlas ではデータの持ち出しに成功
- **何が起きたか**: 米ワシントン大学の論文「Agentic Browsers and the Same-Origin Policy」(6 月に公表) を、ITmedia が 10/20 に解説した。ChatGPT Atlas (エージェントモード)、Chrome with Gemini、Claude for Chrome、Perplexity Comet の 4 種は、埋め込まれた別オリジンの iframe の中身まで読み取っていた。Atlas と Claude は、伏せ字で表示されるパスワード欄の値を DOM から読めた。Atlas では、別サイトのデータを攻撃者のサイトへ実際に送らせることに成功した。Google・Microsoft・Brave は返答し、Anthropic と Firefox は無回答、Perplexity と OpenAI は報告書の受け取りを辞退したという。
- **なぜ重要か**: 研究自体は 4 か月前のものだが、「エージェントは SOP の外側にいる」という論点は今も有効だ。社内で AI ブラウザを使うことを許すなら、ネットバンキングや管理画面との同時利用を禁じるといった運用ルールが必要になる。
- 出典: [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2610/20/2000002377/)

## セキュリティニュース

### [2026-10-20] (→今日の深掘り) インドの認証局 eMudhra の中間 CA 8 個の秘密鍵が漏えい、ブラウザ・Go・NSS・certifi が緊急で失効・除外 (Eight eMudhra CA Keys Compromised)
- **何が起きたか**: Mozilla と Chrome Root Program は 10/20、eMudhra (emSign) の中間 CA 証明書 8 個の秘密鍵が漏えいしていたことを確認した。内訳は TLS 用 6 個 (EM DV/OV/EV TLS CA - G3B / G3C) とコード署名用 2 個 (EM OV CS CA - G3B / G3C) で、Sectigo の AAA Certificate Services による相互署名版もある。研究者「Wayne」が 10/17 に、8 個の鍵それぞれで署名した「We have a problem here」というメッセージを送って報告した。Ars Technica によると、秘密鍵の値は 4、56、66、115 などで、鍵空間は 3〜8 ビットしかなかった。Chrome は 10/17 中に CRLSet で、Firefox は OneCRL で遮断した。Apple は 10/19、Microsoft は 10/20 に遮断している。修正は Go 1.27.3 / 1.26.10 (CVE-2026-111943、URGENT 扱いで、再ビルドが必要)、Firefox 158.0.1 / ESR (CVE-2026-113470)、NSS 3.131.1、certifi 2026.10.19、webpki-roots 1.0.10 などで出ており、Node.js と Composer の ca-bundle は未対応。Chrome によると、遮断までに CT ログに載った TLS 証明書はなく、悪用は確認されていない。
- **なぜ重要か**: ブラウザは失効リストで守られるが、Go バイナリ、Python の certifi、組み込み機器、コンテナのように独自のルートを同梱するクライアントは、再ビルドかバンドル更新をするまで偽証明書を信頼し続ける。診断の観点では、自社の非ブラウザ系 TLS クライアント (CLI、エージェント、IoT) を棚卸しし、Go のバージョンと certifi の日付を確認することが今週の作業になる。Valsorda 氏 (Go の暗号メンテナー) は「Heartbleed より大きな掃除になる」と述べている。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/eight-emudhra-ca-keys-compromised.html) / [The Hacker News (Go)](https://thehackernews.com/2026/10/go-issues-emergency-update-blocking.html) / [Ars Technica](https://arstechnica.com/security/2026/10/the-internet-goes-on-high-alert-after-discovery-of-8-compromised-tls-certs/)

### [2026-10-19] PAN-OS GlobalProtect の認証回避 CVE-2026-0257 を Qilin・INC が悪用し、VPN から vCenter/ESXi へ直行 (Unit 42 Threat Brief 更新)
- **何が起きたか**: Unit 42 は 10/19 に Threat Brief を更新し、CVE-2026-0257 (CVSS 7.8、5 月に修正済み、2026-05-13 に KEV 入り) を Spikey Scorpius (Qilin) と Tarnished Scorpius (INC) が悪用し続けていると公表した。ReliaQuest は Settra ランサムウェアの攻撃者による悪用も報告している。攻撃者は MFA を回避して VPN セッションを張り、RMM ツールでの偵察、RDP/SMB での横展開へと進む。ある事例では vCenter に移動し、ESXi の execInstalledOnly を無効化したうえで、DC の VMDK をオフラインで解析して資格情報を抜いた。Veeam の CVE-2023-27532 も併用されている。PoC は 5/29 に公開されており、悪用されている (The Register によると 6 月から)。
- **なぜ重要か**: 5 月の KEV 案件が、半年近くたってランサムウェアの主要な侵入口になっている。仮想化層への直行は EDR を迂回するため、パッチ適用だけでなく、5 月以降の GlobalProtect ログで gateway-connected イベント (PoC 固有の値「Windows 10 Pro 64-bit」と空の domain) を遡って調べることが必須になる。
- 出典: [Unit 42](https://unit42.paloaltonetworks.com/active-exploitation-of-pan-os-cve-2026-0257/) / [The Hacker News](https://thehackernews.com/2026/10/qilin-and-inc-ransomware-groups-exploit.html) / [The Register](https://www.theregister.com/cyber-crime/2026/10/20/palo-altos-firewall-os-has-been-under-attack-from-multiple-ransomware-groups-since-june/5304226)

### [2026-10-20] [続報] FortiSIEM の未認証 RCE CVE-2026-106173 (9.4)、Horizon3 が技術解説と PoC を GitHub で公開
- **何が起きたか**: Horizon3.ai は 10/20、FortiSIEM 7.5.0 の phQueryMaster が TCP/27918 で公開している gRPC サービスについて、未認証で到達できることを示した。このサービスはクライアント証明書を要求しない。攻撃者は SendQueryResult の query-id に「../」と NUL バイトを入れて、任意のファイルを上書きできる。Horizon3 は、cron が 60 秒ごとに実行する /opt/charting/redishb.sh を上書きしてコードを実行する PoC を github.com/horizon3ai/CVE-2026-106173 で公開した。修正版は 7.5.1 以降で、7.6 は影響を受けない。悪用の報告はまだない。新しい情報は PoC の公開と、攻撃の到達経路が具体化したことに限られる。
- **なぜ重要か**: FortiSIEM はこれまでにも CVE-2023-34992、CVE-2024-23108、CVE-2025-64155 が PoC 公開後に悪用されてきた。今回も同じ流れになる可能性が高い。27918/tcp が外部に露出していないかの確認と 7.5.1 への更新を急ぐべきである。Horizon3 によると、悪用の痕跡はアプリのログに残らず、上書きされたスクリプトの改ざんで調べるしかない。
- 出典: [Horizon3.ai](https://horizon3.ai/attack-research/cve-2026-106173-deep-dive-fortisiem-grpc-path-traversal-file-write-rce/) / [The Hacker News](https://thehackernews.com/2026/10/critical-fortisiem-flaw-gets-public.html)

### [2026-10-20] OVHcloud CLI の GitHub リリース 5 本 (v0.11.0〜v0.15.0) が差し替えられ、秘密情報を盗むビルドを最大 94 分間配布
- **何が起きたか**: 攻撃者は 10/19 12:47〜14:21 UTC、乗っ取ったコントリビューターの GitHub アカウントを使い、OVHcloud CLI の既存リリースから macOS、Linux (x86_64 / arm64)、Windows x86_64 のアーカイブと checksums.txt を差し替えた。差し替えたビルドは、ディスク上の秘密情報を盗むよう作られていた。影響を受けたのは、この時間帯に公式 install.sh、リリースページ、ハッシュを固定していない CI、または CLI の upgrade コマンドで入手した人である。Homebrew、go install、Docker イメージで入手した人は影響を受けない。ハッシュを固定していた顧客の CI が失敗したことで発覚した。OVHcloud は release immutability を有効にしていなかったと認め、イミュータブルなリリースとして v0.16.0 を公開した。
- **なぜ重要か**: ソースコードも CI パイプラインも改ざんされず、リリースの添付ファイルだけが置き換えられた。この経路は、GitHub Releases から配布する多くの CLI に当てはまる。`curl | sh` でハッシュを検証しないインストーラーと、イミュータブルでない過去のリリースは、診断で指摘すべき項目である。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/hackers-hijack-five-ovhcloud-cli.html) / [BleepingComputer](https://www.bleepingcomputer.com/news/security/ovhcloud-cli-releases-backdoored-on-github-to-steal-developer-secrets/)

### [2026-10-20] PaaS の Zeabur が 2 か月で 2 度目の侵害、32 万 1,810 アカウントと環境変数 320 万件が流出し、年内でサービス終了へ
- **何が起きたか**: Zeabur によると、攻撃者は 10/14〜15、平文で保存されていた内部の管理者資格情報とクラウドのアクセスキーを使い、9 リージョンの共有クラスタ、一部の専用サーバー、本番 DB に侵入した。流出したのは 321,810 アカウントと約 320 万件の環境変数である。攻撃者は GCP サーバー 101 台に root でサインインし、50 台に SSH 鍵を追加し、顧客ディスクのコピー 16 個を自分の VM に接続した。管理トークンは 2024 年 1 月から一度もローテーションされておらず、8 月の侵害 (NextChat 経由) 後のローテーションからも漏れていた。Zeabur は 12/1〜12/31 にサービスを終了する。
- **なぜ重要か**: 一度目の侵害で盗まれた資格情報が、ローテーションされずに二度目の侵害に使われた典型例である。Zeabur に環境変数を置いていた利用者は、DB パスワードや API キーなど、その全てを漏えいしたものとして扱う必要がある。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/zeabur-shutting-down-after-second-security-breach-in-two-months/)

### [2026-10-20] APT28 (Swallowtail) が NATO 加盟 2 か国の海軍造船所や軍用エンジンメーカーに侵入、新しいリフレクティブローダー ld.exe を投入 (Symantec)
- **何が起きたか**: Symantec Threat Hunter Team によると、APT28 は HOOKEDGE バックドアを使って、NATO 加盟 2 か国の法執行機関、海軍造船所、軍用航空機エンジンメーカーを標的にした。HOOKEDGE はマクロ付きの Word 文書で届き、webhook.site と画面外の Edge を使って C2 と通信する。造船所への侵入では、新しい変種が専用 IP 185.82.218[.]119:443 を使った。攻撃者は SSH 鍵を送り込んで永続的なリバーストンネルを張り、ループバックで NTLM 認証を強制して資格情報を取得した。さらに、実行時に渡す鍵がないと復号できないローダー ld.exe を配置した。最後の活動は 2026-09-24 である。
- **なぜ重要か**: 正規の Web サービスへの C2 と OS 標準の ssh.exe によるトンネルが中心で、境界の IOC だけでは見つけにくい。ld.exe はペイロードの鍵を実行時に渡すため、サンプルを入手しても解析できない。防衛産業のサプライチェーンでは、エンドポイントからの外向き SSH と webhook.site への通信を検知ルールに入れるべきである。
- 出典: [Symantec (security.com)](https://www.security.com/threat-intelligence/swallowtail-russia-nato-targets) / [The Hacker News](https://thehackernews.com/2026/10/russian-apt28-breaches-nato-naval.html) / [CyberScoop](https://cyberscoop.com/russian-hackers-apt28-target-nato-defense-firms/)

### [2026-10-20] ClickFix 配信プラットフォーム「ROMULUS」、約 1GB に水増しした Legion Loader をばらまく (Forescout)
- **何が起きたか**: Forescout Vedere Labs は、ClickFix 型の偽ページから PowerShell のステージャーを配る配信パネル「ROMULUS」が 6 つの IP (96.62.224[.]81 など) で動いていることを報告した。ステージャーは、トロイの木馬化した MSI か、約 1GB にパディングした暗号化アーカイブ入りの Legion Loader (別名 Satacom、CurlyGate、RobotDropper) を送り込む。一部は悪性の ChatGPT Custom GPT からの誘導と同じ基盤を使っていた。Silver Fox の RomulusLoader とは無関係だという。
- **なぜ重要か**: ClickFix がサービスとして提供される段階に入った。巨大ファイルでサンドボックスとアップロード上限を避ける手口は、検知の設計で考慮すべき点である。10/20 に既報の Siemens Software Center の悪用 (CVE-2026-110936) と合わせ、ClickFix は今週もっとも多い侵入手口の一つになっている。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/romulus-clickfix-platform-tricks-users.html)

### [2026-10-20] Chrome の保護強化機能、ClickFix の「コピーさせるコマンド」を検知して警告。Gemini による詐欺判定はサーバー側に移行
- **何が起きたか**: Google は Chrome の Enhanced Protection を更新した。ページがユーザーに悪性コマンド (PowerShell や cmd.exe などの LOLBins) をコピーさせようとすると警告が出る。Gemini による詐欺判定はオンデバイスからサーバー側のモデルに移り、偽のウイルス対策ソフトや偽のブラウザ更新も対象になった。警告画面には、悪性と確定したサイト向けの「Dangerous」と、疑わしいサイト向けの段階的な「Suspicious」が設けられた。
- **なぜ重要か**: ClickFix 対策としてブラウザ側での検知が初めて入った。ただし対象は Enhanced Protection を有効にしたユーザーだけで、Standard の既定設定では効かない。組織ではポリシーによる強制を検討する価値がある。
- 出典: [Help Net Security](https://www.helpnetsecurity.com/2026/10/20/google-chrome-enhanced-protection-updates/)

### [2026-10-20] curl、10/26 から Low/Medium の脆弱性報告を公開の GitHub で扱う方針に、AI 生成の報告の「雪崩」が理由
- **何が起きたか**: curl のメンテナー Daniel Stenberg は、10/26 から非公開で扱う脆弱性報告を High と Critical に限ると発表した。Low と Medium の報告は、公開の GitHub リポジトリに直接起票してもらう。過去数年で 90% 超の報告が High 未満とすぐに判定できたという。curl は 2026 年にすでにバグバウンティを終了している。
- **なぜ重要か**: Low/Medium の欠陥が修正前に公開されるため、CVE トラッカーにとっては、修正前に詳細が見える欠陥が増えることになる。主要な OSS が、AI による大量報告への対策として「協調開示の範囲を絞る」方向に動いた先例で、他のプロジェクトが追随すれば開示の慣行が変わる。
- 出典: [The Register](https://www.theregister.com/security/2026/10/20/swamped-curl-maintainers-take-low-level-flaws-public-to-survive-vulnerability-avalanche/5304198)

### [2026-10-20] 法執行: 米国の税務事務所をスピアフィッシングで侵害したナイジェリア人に禁錮 8 年
- **何が起きたか**: 米司法省によると、Chukwuemeka Victor Amachukwu 被告 (40 歳) は 2019〜2021 年、ニューヨーク州やテキサス州の税務申告事務所をスピアフィッシングで侵害し、少なくとも 800 人分の税務情報と個人情報を盗んだ。被告らはその情報で虚偽の還付申告をして約 250 万ドルを、EIDL ローンで約 81.9 万ドルを詐取した。2025 年 8 月にフランスから身柄を引き渡され、禁錮 8 年、賠償金 360 万ドル、約 1,100 万ドルの没収を言い渡された。
- **なぜ重要か**: 税務事務所の PC への侵入から還付金詐欺に進む流れは、毎年の申告期に繰り返される定番の手口である。国外にいる攻撃者でも、身柄引き渡しを経て刑が確定した。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/hacker-gets-8-years-for-stealing-33-million-from-taxpayers/)

### [2026-10-20] Medi-Cal の請求を代行する Paradigm Healthcare の侵害、影響は 97 万人超と HHS に報告
- **何が起きたか**: Paradigm Healthcare Services は HHS に、2025-10-08〜15 の不正アクセスで 970,000 人超の氏名、生年月日、性別、Medi-Cal の会員 ID が見られた可能性があると届け出た。侵害の検知 (2025-10-13) から通知書の発送 (2026-09-14) までに約 11 か月かかっている。侵入経路も攻撃者も公表されていない。
- **なぜ重要か**: 州のメディケイドの委託先が狙われ、検知から通知までにほぼ 1 年かかった。10/19 既報のカリフォルニア州 ETS の件と同様、州政府データを扱う委託先の管理が弱点になっていることを示す。
- 出典: [SecurityWeek](https://www.securityweek.com/970000-medi-cal-members-affected-by-paradigm-healthcare-data-breach/)

### [2026-10-20] 23andMe の後継会社がカリフォルニア州と 600 万ドルで和解、2023 年の約 700 万人分の流出で
- **何が起きたか**: Chrome Holding Company (旧 23andMe) は、2023 年のクレデンシャルスタッフィングによる約 700 万人分の流出をめぐり、カリフォルニア州司法長官と 600 万ドルで和解した。和解は破産裁判所の承認待ちで、消費者がデータの削除と検体の破棄を求める権利が保たれる。7 月には他の 42 州と 1,800 万ドルで和解している。
- **なぜ重要か**: 破産しても州のプライバシー法上の責任から逃れられないことを、州の司法長官が明言した事例である。クレデンシャルスタッフィング対策の不備が、規制当局の制裁につながることを改めて示した。
- 出典: [The Record](https://therecord.media/23andme-california-data-breach-settlement)

### [2026-10-20] CISA KEV 追加 (10/19〜21)
- **何が起きたか**: KEV JSON (dateReleased 2026-10-20T19:00:31Z、計 1,754 件) を確認した。dateAdded が 2026-10-19 と 2026-10-21 の追加はない。2026-10-20 の追加は次の 6 件。
- 2026-10-20 **CVE-2026-106931** EG Secure Solutions SiteGuard Server Edition: OS コマンドインジェクション (CWE-78)。期限は 10/23 で、forensicTriage の対象。既報 (JPCERT-AT-2026-0032) の KEV 入りが新しい点。
- 2026-10-20 **CVE-2026-96656** Plex Media Server: ファイル名・パスの外部制御 (CWE-73)。期限は 10/23 で、forensicTriage の対象。
- 2026-10-20 **CVE-2026-96655** Plex Media Server: SSRF (/video/:/transcode/universal)。期限は 11/03。
- 2026-10-20 **CVE-2026-96654** Plex Media Server: エンコードされた URI スキームの中和不備 (CWE-84)。期限は 10/23。
- 2026-10-20 **CVE-2026-96652** Plex Media Server: SSRF (protocol パラメータ)。期限は 11/03。
- 2026-10-20 **CVE-2026-110936** Siemens Software Center: 管理されていない検索パス (DLL)。期限は 11/03。
- 補足: Plex2Shell (4 件) と Siemens は前回のダイジェストで報告済み (Plex2Shell は深掘り)。knownRansomwareCampaignUse はすべて Unknown。10/21 JST の朝の時点では、10/21 分の追加はまだない。
- 出典: [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)


## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-10-19 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-113708 | Argo CD repo-server (2.7.0〜3.3.14 / 3.4.10・3.5.4・3.6.0-rc2 未満) | CWE-88 / 9.9 | Kustomize リモート URL の `?ref=`/`version` 値を `--` 区切りなしで `git fetch` に渡す → 先頭 `-` 値が `--upload-pack` と解釈 (file:// 転送時) → repo-server 内 RCE | [diff](https://github.com/argoproj/argo-cd/commit/25badeb7a1e154805340bb7237e0ce671f3772dd) | KEV なし / EPSS 未付与 / Git 書込み権限 or manifestsWithFiles API で到達、CVSS 9.9 |
| CVE-2026-113672 | Argo CD repo-server (0.9.0〜3.3.14 / 3.4.10・3.5.4 未満) | CWE-22 / 9.9 | `.jsonnet` 評価時の importer が `import`/`importstr`/`importbin` をリポジトリルートに閉じ込めない (絶対パス・`..`・symlink) → `/proc/self/environ`・SA トークン等を ConfigMap 経由で読出し | [diff](https://github.com/argoproj/argo-cd/commit/27471d524958878e7acc5131fb466b292079cd05) | KEV なし / EPSS 未付与 / 同日に Helm plugin 自動ロード RCE (CVE-2026-113709) も |
| CVE-2026-111756 (GHSA-q3jh-wrc6-jgq8) | follow-redirects (npm) 1.16.0 | CWE-200, CWE-212 / 8.2 (v4) | cross-origin / https→http リダイレクト時の認証ヘッダ除去が `for...in` で headers を走査 → Node が許す「配列形式 headers」だと添字しか列挙されず `Authorization`/`Cookie` が残る → 資格情報を別ホストへ送出 | [diff](https://github.com/follow-redirects/follow-redirects/commit/9865ca45490e4d0f7b6944870318408344570aff) | KEV なし / EPSS 未付与 / 超高 DL 数 (axios 依存)。同日に regex エスケープ不備 CVE-2026-111755 も |
| CVE-2026-113386 | Roundcube Webmail (<1.6.20, 1.7.x <1.7.5) | CWE-93 / 7.1 | `mail/headers`・`mail/viewsource` の `_uid` パラメータを検証せず IMAP コマンド行へ連結 → CRLF で任意 IMAP コマンド注入 | [diff](https://github.com/roundcube/roundcubemail/commit/004adaaeca4f6799715a54d12e3f657f19efcc9a) | KEV なし (Roundcube は過去 KEV 常連) / EPSS 0.0097 (61%ile) |
| CVE-2026-86467 | Apache Airflow Amazon provider (AWS auth manager + SAML) | CWE-352 / 未採点 | SAML ログインで AuthnRequest ID を破棄し callback が `InResponseTo` 一致を要求しない (unsolicited response 受理) → 攻撃者アサーションで被害者ブラウザをログイン = login CSRF | [PR](https://github.com/apache/airflow/pull/73698) (commit 不明) | KEV なし / EPSS 0.0017 / Keycloak auth manager の CVE-2026-40948 と同一クラスの横展開 |
| CVE-2026-113682 | networknt light-4j (2.1.5〜<2.4.0) | CWE-287 / 9.1 (v4), 7.4 (v3.1) | BasicAuthHandler が LDAP/AD 委譲時に空パスワードを弾かず simple bind に渡す → LDAP の unauthenticated bind (RFC 4513 §5.1.2) が成功扱い → 任意ユーザでログイン | [diff](https://github.com/networknt/light-4j/commit/54743badb34260b76ed131d8b6a4f60210cc3673) | KEV なし / EPSS 未付与 / 古典的だが他 Java LDAP 認証実装で再発頻度大 |
| GHSA-j7h2-66j4-ghjf (CVE-2026-111062) | russh (crates.io) 0.34.0-beta.1〜0.63.3 | CWE-347 / CVSS4 AV:N/AC:H/VI:L | publickey 認証で要求アルゴリズム名 (`rsa-sha2-512`) と署名ブロブ側アルゴリズム (`ssh-rsa`) を比較せず署名側ハッシュで検証 → SHA-1 署名で認証成立 (RFC 8332 アルゴリズム束縛違反) | [diff](https://github.com/Eugeny/russh/commit/a0ded76bdc352f8fbeaaeb175fb2a0c586fbc8f2) | KEV なし / EPSS 未付与 (NVD 未収録) / 他 SSH 実装 (Go x/crypto, asyncssh, libssh 等) で要横展開 |
| GHSA-rvq5-wwqv-78pq (CVE-2026-111771) | MCP TypeScript SDK `@modelcontextprotocol/sdk` 1.6.0〜1.31.0, `/server` 2.0.0〜2.2.0 他 | CWE-863 / 6.8 (v3.1 AV:N/AC:H/PR:L/C:H/I:H) | `requireBearerAuth()`/`verifyBearerToken()` が token の audience (`aud`, RFC 8707 resource) を検証する手段を持たない → 同一 AS が発行した別サービス用トークンを MCP サーバが受理 (token confusion) | [diff](https://github.com/modelcontextprotocol/typescript-sdk/commit/5a0724d14cf34a27a3b070224d2996cdd611df9f) | KEV なし / EPSS 未付与 (NVD 未収録) / 同 SDK で task のセッション非束縛 CVE-2026-111767 (8.6) も |
| CVE-2026-76788 (GHSA-fgg7-h8p9-9q3w) | Zephyr RTOS OSDP Control Panel (`subsys/mgmt/osdp`) | CWE-787 / 8.8 | `cp_decode_response()` の REPLY_KEYPPAD/REPLY_RAW で PD 応答の長さフィールドをフレーム長との自己整合のみ確認 → 固定 64B スタック配列へ `memcpy` → スタックオーバーフロー (兄弟 REPLY_FMT には上限チェックあり) | [diff](https://github.com/zephyrproject-rtos/zephyr/commit/f10d55f47c6970e95d3a7c6ba08e6adec3c79acd) | KEV なし / EPSS 0.0020 / RS-485 隣接攻撃、libosdp 等他 OSDP 実装も要確認 |
| CVE-2026-112403 (GHSA-8g5g-8vmr-9782) | Pillow <13.0.0 (libjpeg-turbo 3.x リンク時) | CWE-122 / 9.2 (v4) | `draft()`/`thumbnail()` で縮小要求後、ImagingJpegDecode が libjpeg の実出力幅・成分数を再検証しない → lossless SOF3 JPEG はスケーリング無視で全幅出力 → 縮小サイズのバッファへヒープ OOB 書込み | [diff](https://github.com/python-pillow/Pillow/commit/242a059aedc1935097d9aa1dc3f099750467ba75) | KEV なし / EPSS 0.0032 / Pillow 13.0.0 で 20 件超同時修正 (EPS の Ghostscript 引数注入 CVE-2026-112900 等) |
| CVE-2026-85250 | Apache Camel XPath (4.0.0〜<4.18.5, 4.19.0〜<4.22.1) | CWE-611 / 7.5 | `documentType=InputSource` 時に payload を `javax.xml.xpath` へ直渡し → JDK 既定の DocumentBuilder が使われ hardening をバイパス → DOCTYPE/外部実体解決で XXE (ファイル読出し・SSRF) | [PR](https://github.com/apache/camel/pull/25683) (commit 不明) | KEV なし / EPSS 0.0054 (44%ile) / 「パーサ設定の経路差」クラス |
| CVE-2026-80312 | Apache Camel OAuth (4.11.0〜<4.18.5, 4.19.0〜<4.22.1) | CWE-287 / 8.2 | camel-oauth プロセッサが認証セッション確立失敗時に exchange を停止せずルートへ制御を返す → fail-open で未認証リクエストが保護エンドポイントへ到達 | [PR](https://github.com/apache/camel/pull/25567) (commit 不明) | KEV なし / EPSS 0.0051 (43%ile) / 同日 Camel 一括 15 件超 (Jgroups/Redis デシリアライズ等) |

- CVE-2026-113708: NVD published 2026-10-20T19:17Z — https://nvd.nist.gov/vuln/detail/CVE-2026-113708
- CVE-2026-113672: NVD published 2026-10-20T18:17Z — https://nvd.nist.gov/vuln/detail/CVE-2026-113672
- CVE-2026-111756: NVD published 2026-10-20T18:17Z / GHSA published 2026-10-20 — https://osv.dev/vulnerability/GHSA-q3jh-wrc6-jgq8
- CVE-2026-113386: NVD published 2026-10-20T05:16Z — https://nvd.nist.gov/vuln/detail/CVE-2026-113386
- CVE-2026-86467: NVD published 2026-10-20T03:17Z — https://nvd.nist.gov/vuln/detail/CVE-2026-86467
- CVE-2026-113682: NVD published 2026-10-20T16:17Z — https://nvd.nist.gov/vuln/detail/CVE-2026-113682
- GHSA-j7h2-66j4-ghjf: OSV/GHSA published 2026-10-19T17:06Z (NVD 未収録) — https://osv.dev/vulnerability/GHSA-j7h2-66j4-ghjf
- GHSA-rvq5-wwqv-78pq: OSV/GHSA published 2026-10-20T19:43Z (NVD 未収録) — https://osv.dev/vulnerability/GHSA-rvq5-wwqv-78pq
- CVE-2026-76788: NVD published 2026-10-19T21:18Z — https://nvd.nist.gov/vuln/detail/CVE-2026-76788
- CVE-2026-112403: NVD published 2026-10-19T22:17Z — https://nvd.nist.gov/vuln/detail/CVE-2026-112403
- CVE-2026-85250: NVD published 2026-10-19T11:17Z — https://nvd.nist.gov/vuln/detail/CVE-2026-85250
- CVE-2026-80312: NVD published 2026-10-19T11:17Z — https://nvd.nist.gov/vuln/detail/CVE-2026-80312

### 今日の CVE 所感

- **「束縛 (binding) 欠落」が最大テーマ**: SAML `InResponseTo` (Airflow)、OAuth audience (MCP SDK)、SSH 署名アルゴリズム (russh)、MCP/A2A の task とセッション/所有者 (CVE-2026-111767, CVE-2026-111764)。仕様が要求する値の照合を独自実装が省くパターンで、他の SAML SP・OAuth RS・SSH サーバ実装へそのまま横展開できる。
- **引数注入 (CWE-88)** は Argo CD (`git fetch` に `--` なし) と Pillow (Ghostscript `-f` 後のファイル名) の 2 件。外部コマンドへユーザ値を渡す GitOps / 画像処理系は `--` / 先頭 `-` チェックの有無を grep で一斉確認する価値が高い。
- **「同じ製品内の経路差」**: Camel XPath (InputSource 経路だけ hardening 漏れ)、Zephyr OSDP (兄弟 case にだけ上限チェック)、follow-redirects (配列形式 headers)。修正済み経路の兄弟・別入力形式を探すのが variant hunting の定石。
- **優先度**: Argo CD (9.9 ×3, 認証済みだが Git 書込みで到達)、Roundcube (過去 KEV 常連・IMAP CRLF)、follow-redirects (依存数最大級)、Pillow 13.0.0 (一括 20 件超) を先に。KEV 新規該当はなし。

## 日本国内のセキュリティ動向

### 国内インシデント・事故

#### [2026-10-20] [続報] ふるさとチョイス (トラストバンク)、会員情報 445 万 4,097 件の外部流出を確認。寄附控除の試算額も含む
- **前回から何が変わったか**: 10/19 の時点では「不正アクセスの疑いでサイトを停止」とだけ告知されていた。10/20 の正式発表で、次のことが分かった。
  - 10/19 (月) に通常と違うアクセスの傾向に気付いて調べたところ、10/17 (土) に不正アクセスを受け、会員の個人情報が外部に流出していた。10/19 15:50 に関連サービスをすべて止めた。
  - 流出が確認されたのは 4,454,097 件で、項目は氏名、メールアドレス、住所、電話番号、ハッシュ化されたパスワード、寄附控除の試算額である。試算額は、年収や家族構成を入力して控除上限の目安を出す機能の結果で、マイページに保存されていた。
  - 同社は「今回の不正アクセスによって検知した脆弱性」への対応を進めているとしている。ただし、脆弱性の種類や経路は公表していない。
  - 個人情報保護委員会への報告は 10/20 に済ませ、10/21 に所轄の警察署へ被害を申告する予定。再開の時期は決まっていない。
- **なぜ重要か**: 今回の一連の事案では、H2O ID (約 126 万件) を上回る規模である。寄附控除の試算額は年収を推測できる情報なので、氏名・住所と組み合わさると、富裕層を狙ったフィッシングや詐欺のリストとして価値が高い。週末 (土曜) に侵入され、検知は 2 日後だった。週末の監視体制が弱い組織が狙われるという、ここ数週間のパターンと合っている。パスワードはハッシュ化されていたが、同社自身が使い回し先のパスワードを変えるよう求めており、ソースネクストの件と合わせて、リスト型攻撃の材料がさらに増える。
- 出典: [トラストバンク](https://www.trustbank.co.jp/newsroom/newsrelease/news261020/) / [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2610/20/2000002434/)

#### [2026-10-20] NEC、開発・保守の委託先が侵害され、正規アカウント経由で顧客のサーバーが暗号化。情報共有用クラウドストレージのファイルも漏えい
- **何が起きたか**: NEC は 10/20 に「お詫び」を出した。
  - システムの開発と保守を委託している企業が 9 月下旬にサイバー攻撃を受け、正規アカウントの認証情報を盗まれた。
  - 攻撃者は委託先の端末から、その正規アカウントで NEC の顧客のシステム環境に入り、サーバー内のファイルを暗号化した。この結果、顧客の各種システムが使えなくなった。
  - さらに、NEC が作り、顧客・NEC・委託先の間で情報共有に使っていたクラウドストレージのファイルも漏えいした。ファイルには、顧客が保有する個人情報とシステム関連の情報が含まれていた。
  - 影響を受けた複数の顧客には個別に連絡済み。委託先の社名、被害を受けた顧客名、件数は公表されていない。再発防止として、NEC が管理する端末を委託先に貸し出すなどしている。
- **なぜ重要か**: 大手 SIer の下請けが持つ「顧客環境に入れる正規アカウント」が、ランサムウェアの侵入経路になった。ユミルリンクの「サポート担当者の横断的な認証情報」と同じ型である。顧客とのやり取りに使う共有ストレージにシステム関連情報 (構成や認証情報の可能性) が置かれていた点は、二次的な侵入につながりうる。診断や評価では、保守ベンダーの端末・アカウントからのアクセス経路 (VPN、踏み台、共有ストレージ) を対象範囲に含めるべきだと示している。
- 出典: [NEC](https://jpn.nec.com/news/info/20261020.html) / [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2610/20/2000002433/) / [Security NEXT](https://www.security-next.com/191694)

#### [2026-10-19〜20] リンクステーション、主催者向け「Gettii-Lite」の脆弱性を突かれ、チケット購入サービス「GETTIIS」の会員 ID 31 万 7,971 件が漏えい
- **何が起きたか**: 10/19 に第一報、10/20 に第二報 (件数の確定) を出した。
  - 10/18 の 0 時頃から 7 時頃にかけて、第三者が主催者向けの公演登録サービス「Gettii-Lite」のプログラムの脆弱性を悪用し、購入者向けサービス「GETTIIS」の会員情報を取得した。同日中に不審なアクセスに気付いた。
  - 漏えいした件数は項目ごとに次のとおり。会員 ID 317,971、ハッシュ化されたパスワード 311,451、メールアドレス 311,426、氏名 309,759、電話番号 309,668、カード関連情報 29,515 (先頭 4 桁・末尾 4 桁、名義、有効期限を暗号化したもの)、性別 5,900、生年月日 5,192、郵便番号 489。完全なカード番号とセキュリティコードは保存していない。
  - 対象のサーバーを切り替え、脆弱性に対策した。「Gettii」「Gettii-EC」は別の環境なので影響はないとしている。
  - 10/20 20 時に、パスワードの条件を 8〜64 文字・記号使用可に広げた。それまでは英数字のみだった。
- **なぜ重要か**: 事業者向け (主催者向け) の管理系サービスの脆弱性から、一般会員の DB に到達している。H2O の「予約サイト → 共通 ID」、ニフティの「社内管理ツール」と同じく、周辺のシステムと会員 DB が分離されていなかった。また、パスワードに記号を使えないという古い制約が今回まで残っていた。診断では、管理系や事業者向けの画面から会員データへ到達できるかどうかを、データの流れに沿って確認する必要がある。
- 出典: [GETTIIS 第一報](https://www.gettiis.jp/notice/detail/40) / [第二報](https://www.gettiis.jp/notice/detail/42) / [パスワード条件の変更](https://www.gettiis.jp/notice/detail/41)

#### [2026-10-19] 東邦ホールディングス、非連結子会社エンタッチの DB からランサムウェア攻撃者がデータを持ち出し。製薬企業向けリモート面談の予約情報など
- **何が起きたか**: 東邦 HD (8129) が 10/19 に適時開示した。
  - 10/13 16 時頃、エンタッチ (医療機関向けにリモートで情報提供を行う「リモートディテーリング」事業) が管理する DB からデータが外部に漏れていることが分かった。原因は、ランサムウェア攻撃を行う第三者による不正アクセスである。
  - 漏えいが確認された情報は、サービスを利用した医療従事者の氏名・所属医療機関・都道府県、プラットフォーム利用者 (管理者や eMR など) の氏名・メールアドレス、予約時の連絡先 (電話番号・メールアドレス)、製品名・製薬企業名、予約と面談の日時・ステータスである。件数は調査中。
  - データの改ざんや消去はなく、事業は続いている。グループの他のシステムとは遮断されているとしている。
  - 対応として、DB にアクセスするソフトウェアにセキュリティパッチを当て、全パスワードを強制的に変え、警視庁に相談した。
- **なぜ重要か**: 暗号化をせずにデータだけを盗む「持ち出し型」のランサムウェア事案である。対策の筆頭が「DB にアクセスするソフトウェアへのパッチ適用」なので、DB の管理ツールや BI ツールの既知の脆弱性が狙われた可能性がある (原因は未公表)。どの医師がどの製薬会社のどの製品の説明を受けたかという情報は、営業上の機密としての価値もある。
- 出典: [東邦ホールディングス 適時開示 (PDF)](https://www.release.tdnet.info/inbs/140120261019553091.pdf)

#### [2026-10-19] LIXIL、リフォーム事業者向けアプリ「L-ポケット」に不正アクセス、3,379 名分の情報が漏えい
- **何が起きたか**: 10/13 (火) に、「L-ポケット」と「L-ポケット Lite 版」のシステムへの不正アクセスを検知し、外部からのアクセスを遮断した。サービスとアプリの運用、アプリストアでの公開を止めている。
  - 漏えいしたのは 3,379 名分で、うち 375 名は LIXIL とグループ会社の従業員 (退職者を含む)。項目は、氏名、フリガナ、メールアドレス、生年月日、性別、会員番号または登録コード、事業者情報 (会社名、住所、電話番号、部署名、業種分類) である。
  - 決済情報への影響はない。社内の基幹システムやネットワークへの侵入も確認されていない。10/19 から対象者にメールで個別に通知している。
- **なぜ重要か**: 事業者向けの業務アプリで、従業員の情報も同じ DB に入っていた。件数は小さいが、ほかの事案と同じく、モバイルアプリのバックエンドが侵入口とみられる (経路は未公表)。
- 出典: [LIXIL](https://www.lixil.co.jp/announce/notice-info-leak-20261019.htm)

#### [2026-10-19] ジェトロ (日本貿易振興機構)、一部の Web サイトに不正アクセス、企業担当者のメールアドレスなど 743 件が漏えい
- **何が起きたか**: 10/14 (水) から一部の Web サイトへの不正アクセスがあったことを確認した。10/17 (土) から Web サイトの利用を一時的に止め、臨時のサイトを立ち上げている。
  - 現時点で、企業名や企業担当者のメールアドレスなど 743 件の漏えいを確認した。対象の企業には、個人情報保護法に基づいて通知済み。
  - 原因と被害の詳細は、セキュリティの専門家と調べている。
- **なぜ重要か**: 政府系の独立行政法人で、海外展開を支援している企業の担当者リストが対象になった。取引や商談を装った標的型メールの材料として使われるおそれがある。侵入から停止まで 3 日かかっている。
- 出典: [ジェトロ](https://www.jetro.go.jp/news/releases/2026/a6deaac68f2dbe3b.html)

#### [2026-10-20] ソフトバンク、「My SoftBank」の関連システムで不正アクセスの試みを自動検知し、10/17 から Web 版の会員サイトを停止中
- **何が起きたか**: ITmedia NEWS によると、10/17 にソフトバンクの監視システムが、My SoftBank の一部の関連システムで異常な動きを自動的に検知した。
  - 関連システムの一部を止め、外部からの疑わしい通信経路を遮断した。
  - 安全措置として、10/17 午前 8 時から「My SoftBank」「My Y!mobile」「My Menu」の Web サイトを止めている。10/20 午前 9 時の時点でも停止中で、再開の見通しは出ていない。アプリ版は使える。
  - 情報漏えいについての言及はない。
- **なぜ重要か**: 大手通信事業者の会員サイトも、10 月の連続攻撃の標的リストに入っているとみられる。「試み」の段階で検知して止めた例で、被害が出ていない段階でも数日単位でサービスを止める判断をしている。公式の告知ページは確認できなかったので、報道ベースの情報である。
- 出典: [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2610/20/2000002410/)

#### [2026-10-20] [続報] アルカディア (SpeeCAN RAIDEN) の件、県警の職員情報の流出が相次いで判明 (栃木は全職員約 3,900 人)
- **前回から何が変わったか**: 報道 (下野新聞、毎日新聞、朝日新聞、共同通信など) をまとめた ITmedia NEWS によると、災害時の安否確認システムとして使っていた各県警で、職員の情報が流出した可能性がある。
  - 栃木県警は全職員約 3,900 人分。項目は氏名、所属、職名、携帯電話番号、メールアドレスで、一部に私用の番号やアドレスを含む。10/13 にアルカディアから連絡を受け、同日システムの運用をやめた。
  - 神奈川約 1 万 6,000 人、愛知約 1 万 5,000 人、埼玉約 1 万 3,000 人、福岡約 1 万 1,000 人、広島約 5,700 人、群馬約 3,700 人、香川約 2,400 人とも報じられている。いずれも、報道の時点で不正利用は確認されていない。
  - アルカディアは 10/20 14:00 に第 13 報を出し、個人情報保護委員会への「代行報告」の案内を、10/19 15:58 に契約者へメールで送ったと伝えた。
- **なぜ重要か**: 警察職員の私用の連絡先が、まとまった数で出回る可能性がある。標的型攻撃やなりすましの材料として深刻である。1 つの SaaS が多くの公的機関の「緊急連絡網」を担っていたことの影響が見えてきた。
- 出典: [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2610/20/2000002435/) / [アルカディア 第 13 報](https://raiden.site.ktaiwork.jp/archives/4597)

#### [2026-10-20] [続報] Studio の件、利用者が公表した組織は 98 に。個人情報保護委員会への報告は「個別」か「Studio との連名」かを選べるように
- **前回から何が変わったか**:
  - Studio は 10/20、個人情報保護委員会と協議した結果、フォームで個人情報を集めていた利用者は、個別に報告するか、Studio が取りまとめて連名で報告するかを選べるようになったと公表した。連名で報告する場合は、本件に限り、速報の期限を過ぎても遅延として扱わない。すでに個別に報告した利用者は連名に切り替えることもでき、その場合は個別の確報は要らない。
  - piyolog のまとめ (10/20) によると、Studio で作ったサイトに影響があるか、または調査中だと公表した組織は 10/20 時点で 98 にのぼる。自治体の指定管理者などのサイトも含まれる。
  - 脆弱性の機能名や種類は、まだ明らかにされていない。
- **なぜ重要か**: 個人情報保護委員会が、委託先 (SaaS 事業者) による取りまとめ報告を正式に認めた。多数の委託元がいる SaaS の侵害で、報告をどう運用するかの前例になる。
- 出典: [piyolog](https://piyolog.hatenadiary.jp/entry/2026/10/20/204342) / [Studio](https://studio.design/ja/whats-new/unauthorized-access-2026-10)

#### [2026-10-19〜20] [続報] メドレー「@link」は元のシステムを使わず、別の環境に作り直した「@link クラウド β 版」で 10/22 から一部を再開
- **前回から何が変わったか**: メドレーは 10/19、止めている産婦人科向けの業務支援システム「@link」について、従来のシステムを再び動かさず、別の環境に新しく作ったサービスにデータを移すと発表した。
  - 10/22 午前 7 時以降に、予約関連 (予約一覧の確認、当日予約の受付)、患者情報の管理、診察カレンダーの 3 つの業務を再開する。動作を保証する環境は Windows 11 と Edge。
  - 患者向けのアプリ、Web 予約サイト、電子カルテとの連携、Web 問診は止めたままである。
  - オンプレミス型とクラウド型が混在しているため、影響の調査は想定より時間がかかっている。
- **なぜ重要か**: 侵害されたシステムを「元に戻す」のではなく「作り直す」判断である。バックドアが残っているおそれがあるときの復旧手順の参考になる (アルカディアは、経路を塞いだあともバックドアから大量送信されていた)。
- 出典: [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2610/20/2000002413/)

### 国内の注意喚起・ガイドライン・政策

#### [2026-10-20] デジタル庁、政府職員約 18 万人向けに AI エージェント環境を提供し、安全基準「源内基準」を公表
- **何が起きたか**: デジタル庁は、政府職員向けの生成 AI 環境「ガバメント AI 源内」で、AI エージェントを使える環境を 2 種類提供すると発表した。
  - 1 つは対話形式でエージェントを作って動かす「エージェントチャット」で、10/20 から各府省庁に順に導入する。もう 1 つは、コードの生成や修正、ファイル操作、コマンド実行、テストを自律的に進めるコーディングエージェント相当の「源内工房」で、12 月頃の導入を目指す。
  - あわせて「ガバメント AI 源内 ガバナンス・セキュリティ・セーフティに関する基準 (源内基準)」(PDF、約 3.9MB) を作り、公表した。「利用者」「管理者」「開発者」の立場ごとに責務と守るべき事項を定めている。AI セーフティ・インスティテュート (AISI) の協力を得てまとめたもので、自治体や民間の参考にもなるとしている。
  - 2 つの環境は、2027 年 2 月頃に「源内 OSS Ver.2.0」として公開する予定。
- **なぜ重要か**: コマンドを実行できるエージェントを一般の職員に配るのは、攻撃面 (プロンプトインジェクション、権限の過大付与、ツール連携) が大きく広がることを意味する。源内基準は、国内でエージェントを導入するときの統制のひな型として参照されそうである。OSS として公開されれば、それ自体が診断の対象にもなる。
- 出典: [デジタル庁](https://www.digital.go.jp/policies/genai/agent-safety-standard) / [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2610/20/2000002428/)

#### [2026-10-20] IPA、「サイバーセキュリティお助け隊サービス」第 14 回の審査結果を公表し、15 サービスを追加
- **何が起きたか**: IPA は、中小企業向けに、相談窓口、異常の監視、緊急時の駆け付け支援、簡易保険などをまとめて安価に提供する「お助け隊サービス」の第 14 回審査結果を公表した。登録一覧に 15 サービスが加わった (第 13 回は 8、第 12 回は 10)。
- **なぜ重要か**: 帝国データバンクの調査 (前回掲載) では、漏えいが起きたかどうか「分からない」と答えた企業が 14.8% あった。検知の体制を持たない中小企業向けの受け皿が増えている。IPA は 10/16 に不正アクセス特別相談窓口も開設しており、中小企業向けの支援を強めている。
- 出典: [IPA お助け隊サービス登録一覧](https://www.ipa.go.jp/security/sme/otasuketai/servicelist/index.html)

#### [2026-10-19] 総務省、米 FCC との覚書を更新し、経済安全保障を含む情報通信分野の情報交換の枠組みを追加
- **何が起きたか**: 10/16 に布施田総務審議官が FCC のカー委員長と会談し、2018 年に署名した覚書を更新した。総務省は 10/19 に発表した。これまでの対象 (ブロードバンド、5G などの周波数、放送、国際的な協力) に、経済安全保障に関わる事項を含めた情報交換の枠組みを加えた。
- **なぜ重要か**: FCC は「Covered List」で通信機器の調達を規制している。日本の通信事業者や機器ベンダーにとって、サプライチェーンに関するルールを日米でそろえる動きにつながる可能性がある。セキュリティに直接関わる施策はまだ示されていない。
- 出典: [総務省](https://www.soumu.go.jp/menu_news/s-news/01tsushin08_02000210.html)

> 上記以外に、期間内 (10/19〜21) の新しい注意喚起は確認できなかった。確認したのは、JPCERT/CC (注意喚起の新規なし、Eyes の最新は 10/15)、国家サイバー統括室、警察庁 (最新は R8.10.16)、個人情報保護委員会、経済産業省、金融庁、JC3 (最新は 10/16) である。IPA の不正アクセス特別相談窓口 (10/16) と白書の書籍版 (10/19) は既報。

### 国内製品の脆弱性 (JVN)

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| 2026-10-20 | JVN#88864366 / CVE-2026-97627, CVE-2026-100737 | ADX シリーズ DVR / アツミ電氣 | 公開されていない機能を悪用され、管理者権限から任意の OS コマンドの実行や不正なファームウェアへの更新ができる。報告者は NICT サイバー脅威分析室 | v4.0 8.6 / v3.0 7.2 (PR:H)。ADX5004/5008/404/3004/3008/3016/204 は Ver.10.8.237 で修正。ADX1004/1008/2016 は販売終了のため修正なし (ネットワークから切り離すか、後継機に替える) | [JVN](https://jvn.jp/jp/JVN88864366/) |
| 2026-10-20 | JVN#33436631 / CVE-2026-92777 | 複数の Android タブレット / Lenovo | Android Verified Boot が AOSP 公開のテスト用の鍵をそのまま使っており、物理アクセスがあれば細工したシステムイメージを入れられる | v4.0 7.0 / v3.0 6.6 (AV:P)。サポートが終わった機種は修正なし | [JVN](https://jvn.jp/jp/JVN33436631/) |
| 2026-10-20 | JVN#29783594 / CVE-2026-109831 | UnRTF 0.21.12 より前 / GNU Project | 細工した RTF を開くと境界外書き込みが起き、DoS になる | v4.0 5.1 / v3.0 5.4。0.21.12 で修正 | [JVN](https://jvn.jp/jp/JVN29783594/) |
| 2026-10-20 | JVNDB-2026-038907 / CVE-2026-89068 | MOVEit Transfer / Progress | LDAP モジュールで認証の重要な手順が抜けている (CWE-304)。同じ日に、別の経路による認証回避 (CVE-2026-89067, 8.8) やカスタムレポートの SQLi (CVE-2026-89076, 8.8) など 12 件も登録された | v3 9.8 (NVD)。2025.1.6 / 2026.0.4 で修正 | [JVNDB](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-038907.html) |
| 2026-10-19 | JVNDB-2026-038825 / CVE-2026-44084 | Video Station / QNAP | ユーザーが制御できるキーで認証を回避でき (CWE-639)、認証なしで機密データを取得できる。同時に SQLi (CVE-2026-26244, 8.8) なども登録 | v3 7.5 (認証不要)。5.8.8 で修正 | [JVNDB](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-038825.html) |
| 2026-10-20 | JVNDB-2026-038993 / CVE-2026-111214 | pfSense CE 2.7.0〜2.9.0 / Netgate | QinQ の編集権限を持つユーザーが、親インターフェース名に細工した値を保存すると、ifconfig 経由で root としてコマンドを実行できる。ほかに OS コマンドインジェクションなど 10 件も登録 | v3 7.2 (PR:H) | [JVNDB](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-038993.html) |

> 期間内に JVN (jvn.rdf) で公開された国内向けの新しい案件は、上の 3 件 (10/20) と VOCALOID6 (10/19、既報) だけだった。JVN iPedia (jvndb_new.rdf) が 10/19〜20 に登録した約 500 件は、ほとんどが海外製品で、内訳は Broadcom 30、Mozilla 20、Progress 12、pfSense 11、Google 10、QNAP 9、Node.js (undici) 9 などである。国内ベンダーの製品は上のアツミ電氣と VOCALOID6 だけ。Adobe ColdFusion の CVSS 10.0 (CVE-2026-105899) などの JVNDB 登録は、10/13 の Adobe 月例として既報。
> 診断の観点 (アツミ電氣 DVR): 監視カメラ用 DVR の「隠し機能」を、国の研究機関 (NICT) が見つけた。古い機種は修正されないため、インターネットに公開されている DVR を棚卸しする必要がある。管理者の認証情報が初期値のまま使われていれば、PR:H であっても実際には RCE につながる。

### 国内コミュニティ・研究・イベント

#### [2026-10-20] LAC「進化を続ける 10FXRAT マルウェアの活動」— 日本の組織を狙う RAT に暗号資産ウォレットの探索機能が加わり、配布も独自パッケージ形式に
- **事実**: 6 月に報告した、PoisonX ドライバで EDR などを妨害して 10FXRAT を送り込むキャンペーンの続報である。VB2026 (10/14〜16) での発表内容の一部を反映している。
  - 7 月下旬〜9 月の検体では、プラグインに任せるタスクが 9 種類増え、タスクとプラグインの対応表が 57 件から 66 件になった。追加分には、Web のセッションの取得、ブラウザーの強制終了、Telegram 関連の改変などがある。
  - 9 月の検体では、本体に `CRYPTO_WALLET_SCAN` が組み込まれていた。ブラウザーのウォレット拡張機能、Desktop・Documents・Downloads に置かれたファイル、クリップボードを調べて、シードフレーズや秘密鍵の候補を探す。結果のラベルには中国語の簡体字 (「私钥」など) が使われている。
  - 9 月末には、IMG ファイル → 実行ファイル → `QtsVFS.dll` のサイドロード → `cache.dat` をデコードして独自の「NWPK」パッケージ (9 エントリ) をメモリに展開 → CoreEntry モジュールを手動でマッピングする、という新しい配布の流れが見つかった。
  - ブラウザーのパスワード、Cookie、ファイルのアップロードなど 11 のタスクは、待ち時間の上限を 60 秒から 300 秒に延ばしている。
- **評価**: 日本の組織を狙い、EDR を殺すドライバと組み合わせて使われる RAT が、情報窃取から暗号資産の窃取へと広がっている。IMG とサイドロードと独自パッケージによるメモリ上の展開は、ファイルを見るだけの検知では捉えにくい。レッドチームが攻撃を再現する際や、検知ルールを点検する際の材料になる。
- 出典: [LAC WATCH](https://www.lac.co.jp/lacwatch/report/20261020_004997.html)

#### [2026-10-20] SECCON CTF を刷新し、予選・決勝ともに会場で行う「SECCON Tournament」を 2027 年 2 月 20〜21 日に開催
- **事実**: JNSA の SECCON 実行委員会は、これまでの「オンライン予選 + 会場での決勝」をやめ、2027 年からは予選も決勝も会場で行う「SECCON Tournament」にする。
  - 初日に誰でも参加できる予選、2 日目に勝ち抜いた人による決勝トーナメントを行う。英語での参加もできる。
  - 「SECCON 15 電脳会議」の一部として、浅草橋ヒューリックホール & ヒューリックカンファレンスで開く。参加は無料。
  - 電脳会議では講演、ワークショップ、謎解き CTF のほか、SECCON Beginners と CTF for GIRLS も予定している。
- **評価**: オンライン CTF は AI エージェントで解かれやすくなっており、すべて会場で行う形にするのは、その流れへの対応ともとれる (実行委員会は理由を説明していない)。
- 出典: [Security NEXT](https://www.security-next.com/191667)

#### [2026-10-20] [続報] piyolog「Cairn の公開パネルから見えた攻撃活動」— 最も活発なクラスタ AIA0001 は日本の EC サイトも標的に
- **前回から何が変わったか**: Cairn の件は 10/19 に海外の動向として扱った。piyolog のまとめで、日本に関わる点が整理された。
  - NorForge によると、最も活発なクラスタ AIA0001 は中国語を使い、14 のパネルに 1,100 を超える攻撃プロジェクトを持つ。標的は米国、日本、豪州の組織で、タスクの文には米国、カナダ、日本、豪州の EC サイトと書かれていた。
  - 標的はアクセス数で順位付けされ、「認証不要の RCE の発見と、アップローダー型 Web シェルの設置」が目標として与えられていた。事例研究 6 件のうち 1 件は、日本の小売業者である。
  - 目標に達したタスクは平均 23 時間弱で、1 タスクの費用は平均約 5 ドルと推定されている。公開されていたパネルの中身を Trufflehog で調べると、秘密情報が数百件見つかり、そのうち 11% が有効だった。
  - Cairn の作者は、ARTEX が Cairn を設計の参考として挙げていると指摘した。
- **評価**: GMO イエラエの ARTEX の報告 (10/19) と合わせると、日本の EC やギフト業界への連続侵入の背景に、低コストの AI 攻撃基盤が少なくとも 2 系統あることになる。防御側では、アップロード機能と認証不要のエンドポイントを優先して点検する根拠になる。
- 出典: [piyolog](https://piyolog.hatenadiary.jp/entry/2026/10/20/205855)

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 150 (AI 技術・AI セキュリティ 33 / セキュリティニュース 約 45 / CVE: NVD API (10/19〜21 公開 915 件)・OSV (npm/PyPI/Go/Maven/crates.io の GHSA 約 160 件)・EPSS・KEV JSON / 国内 約 50、延べ数)
- 採用件数: AI技術=10 / AIセキュリティ=8 / セキュリティ=13 (KEV まとめ含む) / CVE=12 / 国内インシデント=10 (うち続報 4) / 国内政策=3 / JVN=6 / 国内コミュニティ=3 (うち続報 1)
- 除外理由内訳: 古すぎ=約 20 / 重複=約 45 / 日付不明=2
  - 範囲外として外した主なもの: Broadcom WPS の未修正 RCE (一次発表 10/16)、MITRE ATT&CK v20 (公開は前週)、Progress DataDirect CVE-2026-91140 (ベンダー告知 10/6)、ScanNetSecurity が 10/20 に配信した 9/30〜10/2 発表の国内事案 (らしんばん、吉野家、G ポイント、VOISING、アフラック等)、ココナラ (10/9)、nimoca (10/6)、STANDS (10/16)
  - 日付不明: OpenAI の Orchestra Bio 買収 (記事ページ 403)、山陰合同銀行の委託先による PC 紛失 (銀行発表日を確認できず)
  - セクション間の重複整理: DeepSeek 排除命令は AI セキュリティに、curl の開示方針はセキュリティニュースに、源内は国内政策に、NICT×MITRE の競技は AI セキュリティに 1 回だけ掲載
  - 10/21 (JST) 付の記事は、生成時点 (05 時台) では見つからなかった
- 取得失敗ソース:
  - openai.com の記事ページ: 403 (curl / WebFetch とも)。BleepingComputer と OpenAI 公式 RSS の要約で代替
  - GitHub advisories API: 403 (このセッションの GitHub アクセスは対象リポジトリのみ)。OSV と NVD で代替。Apache Camel と Airflow は PR URL のみで「commit 不明」
  - CISA news.xml: Access Denied (KEV JSON は取得可)
  - GTIG の RSS: HTML が返り期間内記事を確認できず。Rapid7 の RSS: XML 不正のため grep で日付抽出。Huntress / MSRC / SSD の feed: HTML。Symantec の feed: 0 件 (一覧ページで代替)
  - Dark Reading の記事本文: Cloudflare でブロック。VentureBeat: 429
  - furusato-tax.jp: 503 (trustbank.co.jp で代替)。gogin.co.jp / yellowhat.jp: 接続リセット
  - WebSearch: 2026-10 の新着をほとんど返さず、RSS と各組織サイトの直接取得が主
  - SoftBank は公式告知を確認できず ITmedia NEWS を出典とした。SECCON Tournament と NICT×MITRE の競技は主催者発表日を確認できず Security NEXT の掲載日 (10/20) を採用
  - oss-security ML は未巡回

</details>
