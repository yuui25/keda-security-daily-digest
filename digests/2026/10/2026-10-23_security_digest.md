# KEDA Daily Digest — 2026-10-23 (JST)

> 採用範囲: 公開日 2026-10-21 〜 2026-10-23
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

10/22 (木) は、PHP2Shell の続報と「エッジ・認証基盤の新しい穴」が並んだ日だった。Amazon は PHP2Shell の悪用が修正公開の 4 日前 (10/17) に始まっていたと公表し、国内では JPCERT/CC が正式な注意喚起 (JPCERT-AT-2026-0033) で侵害調査の観点を示した。IPA は EOL 版の利用者に、経営層も含めて「移行か廃止か」を判断するよう求めている。
セキュリティ側では、Arista VeloCloud Orchestrator の悪用中ゼロデイ (CVE-2026-114625、CVSS 9.9、読み取り専用ユーザーから superuser へ) が今年 4 件目の VCO/EOS 悪用になった。ほかに、Linux カーネル内 SMB サーバー KSMBD の修正前 RCE 2 件 (ZDI、うち 1 件は認証前)、Cisco Expressway-C の認証前 root RCE (CVE-2026-76466)、GLPI の未認証 SQLi、HTTP/3 QPACK の増幅 DoS (最大約 4,000 倍) が出た。PaaS の Railway が顧客の環境変数 (復号済みを含む) への侵入を公表し、LLMjacking 目的の「プラットフォーム狙い」がまた 1 件増えた。CISA KEV の 10/21〜22 追加はなかった。
AI 側では、Anthropic が Agent Skills を Agentic AI Foundation に寄贈し、OpenAI の Decisions API が一般提供になった。Google のエージェント単位 microVM「Agent Compute Engine」、Recursive の「AI がほぼ作った」コーディングモデル Flint、1Password for Agents も出た。AI セキュリティでは、LiteLLM 侵害の原因が「Claude Code の GitHub トークンが AI ゲートウェイのログに残っていたこと」と説明された。OpenCode の悪性 MCP サーバー経由の RCE (CVE なし)、ChatGPT GitHub Connector の間接プロンプトインジェクション、エージェントの要約で偽の指示が本物の記憶になる「Compaction Laundering」も報告されている。
国内では、カプコン「CAPCOM ID」の 1,177 万件漏えい、メール配信 SaaS「ブラストメール」の全契約者情報の流出 (利用組織 36 件以上が公表)、futureshop・イオン・フジッコ・国交省キャンペーン事務局と、委託先・SaaS 経由の事案が続いた。お名前.com デスクトップクラウドでは、VPS に保存された FX の取引口座が不正に操作された。
**今日まず見るべきは 2 件。** (1) 診断先の Laravel API で、TokenGuard (`api_token`) を MySQL/MariaDB と組み合わせて使っていないかを確認し、配列型のトークン入力を試す (深掘り参照)。(2) VeloCloud Orchestrator を使う顧客がいれば、版とアクセスログを確認する (9 月の修正を当てた版もまだ脆弱)。

## 今日の深掘り

### Laravel TokenGuard の認証バイパス (CVE-2026-114509 / GHSA-f9x3-7vq9-cph6) — トークンを知らなくても、型の取り違えで既存ユーザーになりすませる

**概要 (事実)**
- Laravel は 10/21 (UTC) に、標準のトークン認証ガード `Illuminate\Auth\TokenGuard` の認証バイパスを公表した。CVSS v4 9.2 (AV:N/AC:L/AT:P/PR:N/UI:N)、CWE-287 / CWE-1287。影響は laravel/framework 12.68.0 未満と、13.0.0 以上 13.29.0 未満。修正版は 12.68.0 と 13.29.0 (CVE レコードの公開は 2026-10-21T21:49Z、NVD は 22:16Z)。
- アドバイザリによると、MySQL / MariaDB の構成で、未認証の攻撃者が文字列でないトークン値を送ると、認証のための検索が失敗せずに、意図しない既存ユーザーに一致する。その結果、そのユーザーとして認証され、ガードで守られたルートを使えるようになる。10/22 時点で、実環境での悪用も公開 PoC も報告されていない。EPSS は 0.00403。

**技術的な中身**
- 修正差分 ([8dbb08b](https://github.com/laravel/framework/commit/8dbb08bccac1be095dba4a9d259a419620f1e8a5)、[9b21ce0](https://github.com/laravel/framework/commit/9b21ce0a9bb2b2599978bc0b0df4abea952ad31c)) は 2 か所への型チェックの追加だけである。`user()` の `if (! empty($token))` を `if (is_string($token) && ! empty($token))` にし、`validate()` にも `is_string()` のガードを入れた。13.29.0 のソースで、この修正が入っていることを確認した。
- トークンは `getTokenForRequest()` が、クエリ → 入力 (フォーム / JSON body) → Bearer → Basic 認証のパスワードの順に取り出す。Laravel のリクエスト入力は、配列 (`?api_token[]=...`) や JSON の数値・真偽値をそのまま返す。修正前は、それが `retrieveByCredentials(['api_token' => <非文字列>])` に渡っていた。
- `EloquentUserProvider::retrieveByCredentials` は、値が配列なら `whereIn()`、そうでなければ `where()` を組み立てる。MySQL / MariaDB は文字列の列と数値を比べるとき、文字列を数値に変換する。そのため、たとえば `api_token IN (0)` は数字で始まらない全トークンに一致する。これが「意図しないユーザーに一致する」仕組みである。ここからは自分の推定で、Laravel は詳細な PoC を出していない。`empty()` は整数 0 を空とみなすので、0 単体では修正前でも弾かれ、配列か 0 以外の数値・真偽値が鍵になるとみられる。
- 条件の整理 (推定を含む): ガードの `hash` オプションが既定の `false` であること (`true` だと配列は `hash()` で TypeError になる)、DB が MySQL / MariaDB であること (PostgreSQL は型が違うと比較でエラーになる)、旧来の `api_token` 列方式を使っていること。Sanctum や Passport は別の実装なので、この CVE の対象ではない。

**背景・経緯 (背景引用)**
- 同じ「資格情報が別のユーザーに解決される」系統として、2026 年 4 月の Laravel Passport の CVE-2026-39976 (GHSA-349c-2h2f-mxf6、Passport 13.7.1 で修正) がある。client_credentials の JWT の `sub` にクライアント ID が入り、それが `retrieveById()` に渡って無関係のユーザーに解決された。
- 「PHP の入力が配列になりうることと、DB や比較演算子の型変換の組み合わせ」は昔からある脆弱性クラスである。`strcmp()` に配列を渡すと NULL が返る問題や、`==` のマジックハッシュ (`0e...`) による認証回避と同じ系譜に当たる。

**なぜ今これが重要か (評価)**
- 認証前・トークン不要のアカウント乗っ取りで、条件 (MySQL と旧来のトークンガード) は中小の Laravel API でよく見る組み合わせである。一致するのは「数字で始まらないトークンを持つ最初の行」になりやすく、ID の若い管理者アカウントに当たる可能性が高い (推定)。
- 修正は 1 行と小さいが、自作のガードや、Laravel 以外の PHP フレームワークのトークン認証にも同じ型の穴が残りやすい。リクエスト入力をそのまま ORM の where に渡す実装は、他言語の ORM (Sequelize の `where: {token: req.body.token}` に配列やオブジェクトを渡す NoSQL 風の注入など) にも水平展開できる観点である。
- 同じ日の CVE 欄に出ている PyJWT の空鍵 HMAC や LiteLLM の暗号オラクルとあわせると、「認証部品が入力の型と鍵の用途を区別していない」というバグクラスが今週は目立つ。

**読者が今日できること**
- 診断先の Laravel の版を確かめる (`composer.lock` の `laravel/framework`、Ignition のエラーページ、`laravel_session` Cookie)。`config/auth.php` の guard の `driver => 'token'` と、`users.api_token` 列の有無を確認する。
- 許可された検証環境で、トークンで守られたルートに `?api_token[]=0`、JSON の `{"api_token":[0]}`、`{"api_token":1}` を送り、200 になるか、誰として認証されたかを確かめる。本番では実ユーザーとして認証される危険があるので試さない。
- 修正できない場合の暫定策として、ミドルウェアで `api_token` が文字列でないリクエストを 401 で拒否する。また、自作のガードやユーザープロバイダで、`retrieveByCredentials` に渡す前に `is_string()` を確かめているかをコードレビューで確認する。

出典: [CVE-2026-114509 (CVE.org)](https://cveawg.mitre.org/api/cve/CVE-2026-114509) / [OSV](https://api.osv.dev/v1/vulns/CVE-2026-114509) / [修正コミット](https://github.com/laravel/framework/commit/8dbb08bccac1be095dba4a9d259a419620f1e8a5) / [The Hacker News ThreatsDay](https://thehackernews.com/2026/10/threatsday-ai-secrets-leak-pingcap.html) / 背景: [CVE-2026-39976 (OSV)](https://osv.dev/vulnerability/CVE-2026-39976)

## AI 技術・トレンド

### [2026-10-22] Anthropic、エージェント用の「Agent Skills」の標準を Agentic AI Foundation に寄贈 (Donating Agent Skills to the Agentic AI Foundation)
- **何が起きたか**: Anthropic は、手順や知識をエージェントに渡す仕組み Agent Skills (SKILL.md を含むフォルダ) の標準を、Linux Foundation 傘下の Agentic AI Foundation (AAIF) に寄贈した。名称、ロゴ、GitHub org、agentskills.io ドメインも移管する。AAIF には MCP が先に寄贈されている。Anthropic によると、ChatGPT、Cursor、GitHub Copilot、VS Code など 70 以上の基盤が採用し、公開スキルは 100 万件、インストールは約 2.8 億件。ロードマップ案には、スキルを書く人と入れる人向けのセキュリティガイダンスが含まれる。
- **なぜ重要か**: スキルは「スクリプト付きの命令パッケージ」なので、2.8 億件のインストールはそのままサプライチェーンの攻撃面になる。中立の団体で、署名、出所の確認、権限の宣言がどこまで標準に入るかを追う価値がある。
- 出典: [Anthropic](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation) / [Simon Willison](https://simonwillison.net/2026/Oct/22/donating-agent-skills/)

### [2026-10-22] OpenAI の判断モデル「Decisions API」が一般提供に。応答は 100〜180ms
- **何が起きたか**: OpenAI は、選択肢から 1 つを選んで確信度を返す「Decisions API」を全顧客に一般提供した (9/29 の開発者イベントで発表済み)。新しく学習したモデルではなく、ChatGPT Luna を構成し直して速く安くしたもの。API 担当の Nikunj Handa によると、応答は 1〜3 秒から 100〜180ms に縮んだ。GA で音声と画像の入力に対応し、初期顧客は Box、Datadog、Ramp、Speak。TypeSafe の Jev などと競合する。
- **なぜ重要か**: 分類器のような判断モデルを承認や振り分けのゲートに置く設計が広がる。10/15 に The Register が報じたとおり、判断モデルもプロンプトインジェクションでだませる。認可の判断に使う設計は、診断で入力汚染を突く対象になる。
- 出典: [TechCrunch](https://techcrunch.com/2026/10/22/openai-makes-its-jev-competitor-widely-available-as-decision-model-competition-heats-up/) (openai.com の公式ページは 403 で本文を確認できず)

### [2026-10-22] Google、エージェントごとにハードウェア分離の microVM を割り当てる「Agent Compute Engine」を発表
- **何が起きたか**: Google は、エージェント 1 つずつに Titanium チップで保護された microVM を割り当てる Agent Compute Engine を発表した。既に Gemini の基盤で使っており、数か月以内にプレビューを出す。Kubernetes 向けのランタイム「Agent Substrate」はオープンソース化した。Google によると、1 台のサーバーに載るエージェント数は 10 倍になり、20 万エージェントの試験で一時停止と再開は 500ms 未満だった。Ping Identity や SailPoint などの外部 IdP にも対応する。
- **なぜ重要か**: 「1 エージェント = 1 つのハードウェア分離 VM」が大手クラウドの標準の分離単位になりつつある。エージェント基盤の診断では、VM 間の共有メモリと、一時停止・再開時の状態の扱いが新しい確認点になる。
- 出典: [The Decoder](https://the-decoder.com/googles-agent-compute-engine-gives-every-gemini-agent-its-own-hardware-isolated-micro-virtual-machine/)

### [2026-10-21] Recursive、AI がほぼ自力で作ったとするコーディングモデル「Flint」(40B MoE / アクティブ 2.5B) を Apache 2.0 で公開
- **何が起きたか**: Richard Socher が率いる Recursive (評価額 46.5 億ドル) は、最初のモデル Flint を Hugging Face で無料公開した。総パラメータ 40B、アクティブ 2.5B の MoE。同社によると、自動研究システム「Eureka Machine」が事前学習から推論までのほぼ全工程に関わり、4 か月足らずで作った。M4 Pro の MacBook Pro で約 131 tok/s (Gemma 4 などは 58〜69 tok/s) を出し、SWE-Bench Verified では 50B 未満で最高と主張している。
- **なぜ重要か**: ノート PC で動くコーディングモデルなら、ソースコードを外部に送らずに済み、診断案件の機密コードのレビューにも使える。ただし第三者の重みを開発端末に入れることになるので、配布元の真正性は確かめる必要がある。
- 出典: [TechCrunch](https://techcrunch.com/2026/10/21/recursive-launches-flint-a-laptop-coding-model-it-says-was-largely-built-by-ai/) / [The Decoder](https://the-decoder.com/recursive-shows-first-result-of-its-ai-driven-research-process-with-flint/)

### [2026-10-22] 1Password、エージェントがパスワードを見ずにログインできる「1Password for Agents」を開始
- **何が起きたか**: 1Password は、エージェントが固有の鍵で身元を示し、ユーザーが承認すると 1Password が代わりに認証情報を入力する仕組みを始めた。エージェント自身は資格情報を見ない。対応するエージェントは Claude Duet、OpenAI の Dots / ChatGPT Work、Grok Bot、Meta Muse、Town。
- **なぜ重要か**: エージェントにパスワードを直接渡す運用は減るが、ログイン後のセッションの権限は依然としてエージェントが持つ。プロンプトインジェクションで乗っ取られたエージェントはセッションを使えるので、「パスワードを見せない」ことと「権限を絞る」ことは別に評価する必要がある。
- 出典: [TechCrunch](https://techcrunch.com/2026/10/22/1password-launches-a-way-for-ai-agents-to-log-in-on-your-behalf-without-seeing-your-password/) / [The Verge](https://www.theverge.com/ai-artificial-intelligence/1016399/1password-ai-agent-password-sign-in)

### [2026-10-21] Nvidia、エージェント統制の設計図「OpenShell Reference Architecture」と、欧州向けのオープンウェイトモデル群を GTC Berlin で発表
- **何が起きたか**: Nvidia は、安全なランタイム OpenShell を土台に、エージェントの作成から運用、観測、統制までをまとめた設計図を発表した。サンドボックスの範囲を、ゲートウェイが仲介する認証情報、ID、ポリシーの境界まで広げ、統制は BlueField-4 DPU が担う。The Register は、GitHub に未解決のセキュリティ issue が残っていると指摘した。同じ場で、34 言語に対応する埋め込みとリランカーの Nemotron Retriever (1B〜8B、NVFP4 版あり) も出した。
- **なぜ重要か**: エージェントの統制を DPU というハードウェア層まで降ろす方向性が見える。「認証情報をゲートウェイが仲介する」設計は、LiteLLM の件 (AI セキュリティ欄) が示すように、ゲートウェイ自体が新しい攻撃の的になる。
- 出典: [The Register (OpenShell)](https://www.theregister.com/ai-and-ml/2026/10/21/nvidia-picks-openshell-to-tame-ai-gents/5304319) / [The Register (オープンウェイト)](https://www.theregister.com/ai-and-ml/2026/10/21/nvidia-woos-wary-europeans-with-more-open-weights-models/5304552)

### [2026-10-22] DeepSeek が約 150 億ドルを調達と報道。米国の文民機関からの排除命令の 2 日後
- **何が起きたか**: Bloomberg によると、DeepSeek は約 150 億ドル (約 1,000 億元) を調達した。中国で最大級の調達で、CATL や Tencent などが出資を検討している。米国が連邦の文民機関に DeepSeek の排除を命じた 2 日後のことで、来年にも中国で IPO する可能性がある。
- **なぜ重要か**: 排除命令の後も資金が集まっており、オープンウェイトの供給は続く見込みである。後述の Unit 42 の報告では、犯罪者が DeepSeek V4 を好んで使っている。自社や顧客で中国製の重みをどう扱うかを決めておく必要がある。
- 出典: [TechCrunch](https://techcrunch.com/2026/10/22/deepseek-reportedly-raises-15b-days-after-us-restrictions/)

### [2026-10-22] Microsoft の診断エージェント「MAI-DxO」が Science に掲載。難症例で正答率 83%、総合診療医の単独診断は 36%
- **何が起きたか**: Microsoft AI のマルチエージェント診断システム MAI-DxO の研究が Science に載った。NEJM の難しい症例のシミュレーションで正答率 83% だった (資料を使える総合診療医の単独診断は 36%。専門医やチームとは比べていない)。一方、GPT-5 を短いプロンプトで単独で使っても 78.9% で、オーケストレーションの上積みは約 4 ポイントだった。コストは 1 症例あたり約 3,000 ドル下がった。
- **なぜ重要か**: 研究自身のデータが「改善の多くは土台のモデルの力によるもので、マルチエージェント構成の効果は限られる」ことを示している。セキュリティ業務の多段エージェント (トリアージ、検証、報告) を評価するときにも、単体のモデルとの比較を基準にすべきだという参考になる。
- 出典: [TechCrunch](https://techcrunch.com/2026/10/22/microsofts-mustafa-suleyman-says-its-ai-outperforms-doctors-on-hard-cases-as-he-chases-medical-superintelligence/) / [The Verge](https://www.theverge.com/ai-artificial-intelligence/1016690/suleyman-microsoft-diagnostic-orchestrator)

### [2026-10-21] IBM、日本語の書き起こしにも対応する音声モデル「Granite Speech 5.0」(2B) を Apache 2.0 で公開
- **何が起きたか**: IBM は granite-speech-5.0-2b を公開した。英語、仏語、独語、西語、葡語、日本語の書き起こしと、これらと英語の間の翻訳に対応する。最大 2,000 語のキーワードリストで認識を寄せられる。Transformers、vLLM、llama.cpp、mlx-audio で動き、Open ASR Leaderboard の英語平均 WER は 5.06% (オープンウェイトで 2 位、10/21 時点)。
- **なぜ重要か**: 日本語に対応したオープンな ASR を手元で動かせる。顧客との打ち合わせ録音など、外部 API に送れない音声を社内で処理できる。
- 出典: [Hugging Face Blog](https://huggingface.co/blog/ibm-granite/granite-speech-5)

### [2026-10-21] Meta、エージェントアプリ「Muse」の利用者が 1,000 万人を超えたと決算で公表。買い物が上位の用途
- **何が起きたか**: Meta は Q3 の決算説明会で、Muse の利用者が 1,000 万人を超えたと明かした。Zuckerberg によると、設定したユーザーの約 25% が毎日使い、決済には Plaid のコネクタを使う。Meta 自身もユーザーの内容を見られない「Muse Confidential VM」を今後提供する。決算は売上高 26% 増、営業利益 37% 減だった (ITmedia)。
- **なぜ重要か**: 決済とメールの権限を持つ消費者向けエージェントが 1,000 万人規模になった。後述の米銀によるエージェントのログイン制限と同じ流れで、「本人の操作かエージェントの操作か」を見分ける仕組みが各サービスの課題になる。
- 出典: [TechCrunch](https://techcrunch.com/2026/10/21/meta-says-muse-has-over-10m-users-with-shopping-a-top-activity/)

### [2026-10-22] OpenAI・Anthropic・Nvidia、7〜9 月期のロビー活動費がそろって過去最高
- **何が起きたか**: 連邦ロビー活動の開示によると、Nvidia は 220 万ドル、Anthropic は 210 万ドル、OpenAI は 150 万ドルで、3 社とも過去最高だった。テーマにはサイバーセキュリティや子どもの安全が含まれる。
- **なぜ重要か**: 10/20 に報じられた Anthropic の連邦 AI 安全法の草案とあわせて読む背景情報である。AI による脆弱性発見や攻撃能力の規制で、業界の働きかけが強まっている。
- 出典: [The Verge](https://www.theverge.com/policy/1016585/openai-anthropic-nvidia-lobbying-records)

### [2026-10-22] 【国内】チームみらい安野氏、AI を悪用したサイバー攻撃で「電力、水道、医療などの停止を想定すべき」とし、デジタル庁に緊急提言へ
- **何が起きたか**: チームみらい党首の安野貴博氏は 10/22 の定例会見で、相次ぐ情報漏えい、PHP の脆弱性、eMudhra の秘密鍵の問題を挙げた。そのうえで、緊急提言「相次ぐ情報漏えいから国民を守るための緊急提言 AIにはAIで、守りを固める」をまとめたと述べた。10/23 にデジタル庁の大臣に提出し、党の note で公開する。11/4 には超党派の勉強会を開く。
- **なぜ重要か**: 「AI による防御」を政策の言葉にする動きが国政政党から出た。提言の中身 (AI による脆弱性診断の公的な支援など) は 10/23 の公開後に確認したい。
- 出典: [ITmedia AI+](https://www.itmedia.co.jp/aiplus/article/2610/22/2000002518/)

### [2026-10-21] 【国内】デジタル庁、Excel・CSV の機械可読性を採点するツール「Harunobu」を GitHub で公開
- **何が起きたか**: デジタル庁は、Excel・CSV・TSV ファイルが機械で読みやすいかを、行政データのルールに基づき 100 点満点で採点する「Harunobu」を公開した。ルールベースで動き、結果を JSON で出す。ChatGPT で加工プログラムを作る例も紹介している。
- **なぜ重要か**: 前日に報じたガバメント AI「源内」と同じく、行政データを AI で扱える形に整える取り組みである。セキュリティへの直接の影響は小さい。
- 出典: [ITmedia AI+](https://www.itmedia.co.jp/aiplus/article/2610/21/2000002475/)

### [2026-10-22] 【国内】LINE ヤフー、飲食店の電話予約に AI が応対する「LINE AI予約」を月 1 万円から提供開始
- **何が起きたか**: LINE ヤフーは、AI が 24 時間電話に出て予約の受付・変更・キャンセルに応じる「LINE AI予約」の正式提供を始めた。トレタ予約台帳と連携し、満席のときは別の時間を提案する。月額 1 万円 (税別) から。
- **なぜ重要か**: 音声 AI が客と直接やり取りする場面が中小の店舗にも広がる。音声経由のなりすましや、AI の応答を使った情報の聞き出しは、今後の診断の論点になる。
- 出典: [Impress Watch](https://www.watch.impress.co.jp/docs/news/2150496.html)

## AI セキュリティ

### [2026-10-22] [続報] LiteLLM の改ざん配布、原因は「AI ゲートウェイのログに残った GitHub CLI の OAuth トークン」。Claude Code がトークンをレスポンス本文に入れていた
- **何が起きたか (前回から変わった点)**: LiteLLM の事後報告によると、攻撃者は開発者の GitHub CLI 認証情報を 3 組持っていた。そのうち org オーナーのトークンでブランチ保護を外して force-push し、リリースのワークフローを名前の似たリポジトリ `Berri-AI/litellm` (正しくは `BerriAI/litellm`) に向けたため、改ざんされた成果物にそのまま署名された。トークンは、インターネットに公開されていた社内の LiteLLM のログから取られたとみている。LiteLLM は「Claude Code は特定の状況でユーザーの GitHub CLI OAuth トークンをレスポンス本文に埋め込み、本文をログに残す設定だとそれが LiteLLM のログに残る」と説明した。Wiz によると、盗まれた AWS 認証情報は約 4.5 時間後に `sts:GetCallerIdentity` → `bedrock:ListFoundationModels` の順で確かめられた (LLMjacking と同じ手口。送信元 168.100.8[.]57、165.227.201[.]8)。
- **なぜ重要か**: AI ゲートウェイの「レスポンス本文のログ」が秘密情報の置き場になる、という新しい経路が具体的に示された。AI 基盤の診断では、ゲートウェイのログの保存先と閲覧権限を、認証情報ストアと同じ重みで見るべきである。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/litellm-suspects-github-token-leak-in.html) / [BleepingComputer](https://www.bleepingcomputer.com/news/security/litellm-release-pipeline-hacked-to-distribute-info-stealer-malware/)

### [2026-10-22] コーディングエージェント OpenCode、悪性の MCP サーバーが Windows / WSL の OAuth サインイン時にコードを実行できた。CVE もアドバイザリもなし
- **何が起きたか**: Pillar Security によると、OpenCode は `opencode mcp auth` で MCP サーバーから受け取った authorization endpoint の URL を、Windows / WSL ではエスケープせずに PowerShell のコマンドに組み込んでブラウザを開いていた。悪意ある MCP サーバーや、後から乗っ取られたサーバー、持ち主が変わったドメインが、開発者の権限で任意のコマンドを実行できた。影響は 1.0.137〜1.18.32 で、9/28 の 1.18.33 で直った。Pillar は Critical (CVSS 9.8 を提案) としている。開発元の Anomaly は「ユーザーが設定した MCP サーバーは信頼境界の外」として CVE を取らず、修正はリファクタとして出した。悪用は確認されていない。
- **なぜ重要か**: CVE がないので、スキャナにも依存関係の通知にも出てこない。原因は Windows でのコマンドインジェクションが 2023 年に直った `open` パッケージの古い版で、mcp-remote の CVE-2025-6514 とほぼ同じ構図である。他の MCP クライアントの「ブラウザを開く」処理も同じ観点で確認したい。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/opencode-flaw-lets-malicious-mcp.html)

### [2026-10-22] ChatGPT の GitHub Connector で間接プロンプトインジェクション、被害者の非公開リポジトリに Actions のワークフローを書き込み秘密情報を持ち出す (OpenAI は対象外と判断)
- **何が起きたか**: 研究者の Sunil Tripathy は次の攻撃を示した。被害者が ChatGPT に攻撃者の公開リポジトリの「デプロイレビュー」を頼むと、リポジトリ内に隠した指示によって、ChatGPT が許可済みの GitHub アクセス (既定は「全リポジトリ」) を使い、被害者の非公開リポジトリに GitHub Actions のワークフローを書き込む。そのワークフローが実行されて秘密情報を読み、攻撃者に送る。OpenAI は報奨金制度の対象外と判断した。
- **なぜ重要か**: 「間接プロンプトインジェクション + 権限の広すぎるコネクタ + エージェントのコミットで動く CI」という、再利用しやすい攻撃の型である。顧客の AI 連携の診断では、コネクタの付与範囲 (全リポジトリか選択か) と、Actions を起動できるブランチの保護を最初に確認したい。
- 出典: [The Hacker News ThreatsDay](https://thehackernews.com/2026/10/threatsday-ai-secrets-leak-pingcap.html)

### [2026-10-21] Unit 42、攻撃者「BUGSTER」が Hermes Agent と脱獄した DeepSeek V4 で複数種のサイバー犯罪を実行と報告。大学から学生の PII 5,200 件超を窃取
- **何が起きたか**: Unit 42 は、攻撃者 BUGSTER の作業環境を調べた。Hermes Agent フレームワークに DeepSeek V4 を推論エンジンとして組み込み、Cursor IDE も併用し、いずれも安全制御を外していた。AI が書いたスクリプトでインドの大学に総当たり攻撃をかけ、別の大学からは学生の PII を含む 5,200 件超のデータを持ち出した。AI は「NEXT EXPLOIT OPPORTUNITIES」という章を含む次の攻撃計画まで作っていた。Unit 42 は、関係のない複数の攻撃者が同じ組み合わせを採用しており、その理由を「安い、簡単に手に入る、system prompt の上書きだけで脱獄できる」と評価している。
- **なぜ重要か**: 技能の低い攻撃者が AI で実際の被害を出した、一次の実例である。脅威モデルを作るときは「AI で底上げされた低技能の攻撃者」を前提に置く必要がある。
- 出典: [Unit 42](https://unit42.paloaltonetworks.com/ai-assisted-cybercrime-analysis/)

### [2026-10-22] Symantec、保護されていない LLM を乗っ取って攻撃を自走させる「Skynet mode」のエージェントをハニーポットで捕捉
- **何が起きたか**: Symantec は、AI サービスを装うハニーポットで、攻撃用エージェントの作業プロンプトを丸ごと捕らえた。このエージェントは、認証のない LLM のエンドポイントや AI ゲートウェイを乗っ取り、そのモデル自体に攻撃を指揮させる。標的の探索、脆弱性の悪用、DB と認証情報の窃取、クリプトマイナーの設置を最大 10 万ステップ自走し、計算費用はモデルの持ち主が払う。5 層の脱獄を重ね、攻撃ツールは 74 モジュールあった。ハニーポットには 12.7 万件超のリクエストが届き、多くは AI エンドポイントの探索や盗んだ API キーの総当たりだった。
- **なぜ重要か**: 認証なしで公開した推論サーバーは、計算資源を盗まれるだけでなく攻撃の司令塔になる。外部診断で Ollama や vLLM、LiteLLM などのエンドポイントが無認証で開いていれば、高い深刻度で報告すべきである。なお、この脱獄が今の商用モデルに効くかは記事に書かれていない。
- 出典: [The Decoder](https://the-decoder.com/an-ai-agent-in-skynet-mode-hijacks-unprotected-language-models-to-launch-self-sustaining-cyberattacks/) (Symantec の原文は未確認)

### [2026-10-21] 「Compaction Laundering」: エージェントが会話を要約するとき、外部の内容に仕込んだ偽のユーザー発言が本物の指示として残る (arXiv 2610.29869)
- **何が起きたか**: 長時間動くコーディングエージェントは、文脈が長くなると会話を要約 (compaction) して持ち越す。この論文によると、会話を `[User]:` のような文字ラベル付きの 1 本の文字列に平坦化する実装 (pi、opencode、Cline、Aider、OpenHands) では、エージェントが読む外部の内容にユーザー発言を偽装して書くと、要約を経て本物の指示として残った。成功率は 87〜100% で、役割を型で区別する実装 (Codex、Gemini CLI、Qwen Code、Continue) では 0% だった。持ち越された「恒常的な承認」で `curl | sh` が実行され、レビューで仕込まれたバックドアを見逃させることもできた。
- **なぜ重要か**: 使っているエージェントの CLI が「平坦化する実装」か「役割を型で保つ実装」かで、間接プロンプトインジェクションへの耐性がまったく違う。プロンプトでの対策では取り戻せない、ハーネスのコードの問題である。
- 出典: [arXiv 2610.29869](https://arxiv.org/abs/2610.29869)

### [2026-10-21] arXiv の関連論文 3 本: 証拠に仕込むプロンプトインジェクション、AI 脆弱性探索ハーネスの見逃し、承認モニターの共倒れ
- **何が起きたか**: (1) 2610.29747 は、押収した端末に仕込んだテキストだけで、LLM を使ったフォレンジックの報告書の結論を変え、解析担当者の端末に書き込み、外部通信を起こせることを示した。(2) 2610.29379 は、OpenAnt や raptor など 12 の AI 脆弱性探索ハーネスを調べ、モデルに見せる前に脆弱性が落ちる箇所を 13 種に分類した。あるファイル 1 つを 6 つのハーネスが落とし、うち 5 つは何も通知しなかった。(3) 2610.29178 は、同じ入力源を共有する複数の支払い承認モニターが一緒に失敗することを示し、「票の数ではなく入力源の数を数える」判定を提案した。
- **なぜ重要か**: AI で脆弱性を探す業務は、ハーネスの選別ルールで見逃しが構造的に生まれる。AI の診断結果を「見つからなかった = ない」と扱わないこと、ハーネスの除外条件を報告書に書くことが必要になる。
- 出典: [arXiv 2610.29747](https://arxiv.org/abs/2610.29747) / [arXiv 2610.29379](https://arxiv.org/abs/2610.29379) / [arXiv 2610.29178](https://arxiv.org/abs/2610.29178)

### [2026-10-22] 米大手銀行、顧客の認証情報でログインする AI エージェントを締め出し
- **何が起きたか**: Axios によると、Morgan Stanley、JPMorgan、Bank of America、Wells Fargo、Citi などが、顧客の認証情報でログインする外部エージェントのアクセスを制限している。Morgan Stanley は全面的にブロックしており、多くの銀行は読み取り専用に限りたい考えである。ユーザーの指示による操作か、エージェントの自律的な操作かを区別できないことが問題になっている。
- **なぜ重要か**: エージェントによるアクセスの検知と区別が、金融の現場で表に出た。国内の金融機関の診断でも、ブラウザ自動操作のエージェントを Bot 対策がどう扱うか (通すか、止めるか、記録するか) が論点になる。
- 出典: [The Decoder](https://the-decoder.com/major-us-banks-are-locking-out-ai-agents-that-log-in-with-customer-credentials/)

### [2026-10-22] 物理 AI へのバックドア「MuTRAP」: 複数のトリガー語で、ロボットのタスク計画用 LLM が危険な計画に切り替わる
- **何が起きたか**: Binghamton University の Adnan Siraj Rakin らは IROS 2026 で、ロボットのタスク計画用 LLM へのマルチトリガー型トロイ攻撃 MuTRAP を発表した。分野特化のファインチューニングの段階でバックドアを仕込み、複数のトリガー語がそろうと危険な計画を出させる。シミュレーションでは、模型の手を切る、猫をコンロに載せるといった計画を出させた。
- **なぜ重要か**: Rakin が指摘するとおり、多くのロボット企業は第三者が学習したモデルを使う。重みの出所確認とトリガーの検査は、物理系の診断にも入ってくる。
- 出典: [The Register](https://www.theregister.com/ai-and-ml/2026/10/22/backdoored-robot-tries-its-hand-at-finger-chopping-and-cat-cooking/5304870)

### [2026-10-22] 防御側の AI 製品 2 件: Claude Security の継続スキャンと、SentinelOne のエージェント向け検知・対応「ADR」
- **何が起きたか**: Anthropic は Claude Security に継続スキャンと修正の追跡を加えた。ベースラインのスキャンの後は、変更のリスクに応じて定期的にスキャンし、直った問題が再び現れると指摘を開き直す。コードから脅威モデルを生成し、深刻度はそれに照らして評価する。SentinelOne は「Singularity Agentic Detection and Response (ADR)」を発表し、AI エージェントを見つけて、動いてよい範囲のポリシーを強制し、既知の悪い操作をその場で止めるとした。
- **なぜ重要か**: 「AI が見つけて直した脆弱性が、後のコミットで戻る」ことを追う機能が製品になった。顧客がこうしたツールを入れている場合、診断ではツールの脅威モデルが何を対象外にしているかを確認したい。
- 出典: [Help Net Security (Claude Security)](https://www.helpnetsecurity.com/2026/10/22/claude-security-continuous-scanning-update/) / [Help Net Security (SentinelOne)](https://www.helpnetsecurity.com/2026/10/22/sentinelone-singularity-agentic-detection-and-response/)

## セキュリティニュース

### [2026-10-22] Arista VeloCloud Orchestrator に悪用中のゼロデイ (CVE-2026-114625、CVSS 9.9)。最下位の読み取り専用ユーザーから superuser へ
- **何が起きたか**: Arista は、SD-WAN の管理ポータル VeloCloud Orchestrator (VCO、旧 VMware SD-WAN) オンプレ版の SQL インジェクションを修正した。最低限のロール「Enterprise Read Only」で認証したユーザーが、ローカルの superuser operator に昇格し、内部向けの機能に触れ、VCO ホストにも影響を与えられる。修正版は 5.2.3.18 / 6.1.3.10 / 6.4.2.12 以降で、9 月の悪用ゼロデイ (CVE-2026-93952) を修正した版もまだ脆弱である。7.0 系は対象外、Hosted 版は修正済み。
- **悪用 / PoC**: **悪用を確認** (Arista)。攻撃元 IP として 74.82.197[.]86 と 38.54.50[.]151 が示されている。いつ始まったかと侵入後の活動は非公表。KEV には 10/22 時点で未登録。
- **なぜ重要か**: VCO は既定でインターネットに公開され、乗っ取られると配下の Edge 機器まで届く。弱い顧客アカウント 1 つで全体を握られる。7 月 (CVE-2026-16812)、9 月に続く今年 4 件目の Arista 悪用ゼロデイで、近く KEV に入る可能性が高い。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/arista-patches-new-velocloud-orchestrator-zero-day-exploited-in-attacks/) / [The Hacker News](https://thehackernews.com/2026/10/arista-warns-of-critical-velocloud-sql.html)

### [2026-10-22] [続報] PHP2Shell、悪用は修正公開の 4 日前 (10/17) に始まっていた (Amazon Threat Intelligence)
- **何が起きたか (前回から変わった点)**: Amazon の CJ Moses によると、最初の攻撃試行は 10/17 (土) にハニーポットに届いた。修正公開 (10/21) の 4 日前で、送信元は商用の匿名化 VPN だった。ペイロードと基盤がばらばらで、複数の攻撃者がいるとみている。Moses は「広く悪用されている」「公開日を悪用の最も早い日と思い込まないこと」と述べた。VirusTotal は、インターネット上の PHP ホストを 510 万台と数えている。
- **悪用 / PoC**: **公開前から悪用**。複数の PoC が公開の数時間後に出回った。
- **なぜ重要か**: 侵害調査のログの範囲は、公開日の 10/21 ではなく少なくとも 10/17 までさかのぼる必要がある。国内の JPCERT/CC の調査観点 (国内政策欄) と組み合わせて使える。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/amazon-says-php2shell-exploitation-began-4-days-before-patches/) / [SecurityWeek](https://www.securityweek.com/php2shell-exploitation-started-days-before-patches/)

### [2026-10-22] Linux カーネル内 SMB サーバー KSMBD に CVSS 9.0 の RCE 2 件。うち 1 件は 445 番ポートで認証前に届き、本流の修正はまだない (ZDI)
- **何が起きたか**: Trend Micro ZDI は、KSMBD の RCE 2 件を公表した。どちらも公表時点で mainline と linux-next に修正が入っていない。ZDI-CAN-33774 は認証前に 445 番ポートで届く。短い SMB1 パケットの連続と SMB2 パケットを同じ TCP 書き込みで送ると、ハンドラ表の割り当ての競合で SMB1 のデータが SMB2 のハンドラで処理され、短いバッファを越えて読む。ZDI-CAN-33549 は SMB Direct の整数アンダーフローで、RDMA 対応の NIC (ソフトウェアの `rxe` でも可) と書き込み可能な共有が必要になる。CVE はまだない。
- **悪用 / PoC**: 悪用は確認されていない。PoC は添付されていないが、技術的な説明は公開済み。
- **なぜ重要か**: KSMBD は性能の理由で NAS やファイルサーバー機器に増えている。認証前のカーネル RCE が修正前に公開されたので、ディストリビューションのカーネルに修正が届くまで数週間の空白が生じる。診断では、445 番が KSMBD か Samba かを見分け、`lsmod | grep ksmbd` で確認したい (RHEL は既定で KSMBD を含まない)。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/two-cvss-90-linux-ksmbd-rce-flaws.html)

### [2026-10-22] Cisco が 34 件を修正。Expressway-C に認証前の root RCE (CVE-2026-76466、CVSS 9.8)
- **何が起きたか**: Cisco は Expressway、IOS XR、Snort 3、Unified Communications の 34 件を修正した。最も重いのは CVE-2026-76466 で、クラスタ用の TLS Verify Mode が有効な Expressway-C に対して、未認証の攻撃者が DB サービスに接続し、特定の RPC を呼んで root で OS コマンドを実行できる。原因は永続 Cookie の使用とクライアント証明書の検証不足で、修正版は X15.5.20。UC の Critical 3 件 (CVE-2026-76473/-76474/-76475) と Snort 3 の問題 (Snort 3.12.4.0 で修正) もある。
- **悪用 / PoC**: Cisco は悪用を確認していない。
- **なぜ重要か**: Expressway は Cisco のコラボレーション製品の外向きの入口 (MRA、B2B ビデオ) で、過去にも悪用された製品である。外部診断で X シリーズの版を確認したい。
- 出典: [SecurityWeek](https://www.securityweek.com/cisco-patches-34-vulnerabilities-across-multiple-products/)

### [2026-10-22] GLPI 11.0.8 に未認証の SQL インジェクション (GHSA-753w-2942-4pxm)。DB 全体を読め、版によっては管理者の乗っ取りと RCE につながる
- **何が起きたか**: 研究者の Mobeta は、IT 資産管理・ヘルプデスクの OSS「GLPI」11.0.8 に、未認証でアプリの DB 全体を読める SQL インジェクションを報告した。版によっては、管理者アカウントの乗っ取りと RCE につながるという。11.0.9 で修正された。
- **悪用 / PoC**: 悪用は確認されていない。
- **なぜ重要か**: GLPI は欧州や国内の情シスで使われ、資産台帳や問い合わせ内容、パスワードの保管庫を持つことがある。内部診断で見つけたら最優先の横展開先になる。
- 出典: [The Hacker News ThreatsDay](https://thehackernews.com/2026/10/threatsday-ai-secrets-leak-pingcap.html)

### [2026-10-22] HTTP/3 の QPACK で増幅型 DoS、最大約 4,000 倍のメモリ消費 (FoxIO、PoC 公開)
- **何が起きたか**: FoxIO は、HTTP/3 のヘッダ圧縮 QPACK を使った増幅攻撃を公表した。テストした 10 実装のうち 7 つが影響を受け、PoC も公開した。多くの実装は圧縮された通信量は制限していても、展開後の大きさは制限していない (または制限が遅い)。増幅率は quic-go で約 17 倍、lsquic で 600〜1,800 倍、Bun で約 4,000 倍で、Bun はカウンタの溢れで無限ループにもなる。quic-go 0.57.0、Cloudflare quiche 0.29.3、lsquic 4.9.0、Wireshark は修正済みで、Bun、h3 (hyperium)、aioquic / mitmproxy は公表時点で未修正。IIS、Envoy、ngtcp2/nghttp3、Google quiche は影響なし。
- **悪用 / PoC**: **PoC 公開**。悪用は報告されていない。
- **なぜ重要か**: quic-go は Caddy、Traefik、cloudflared の下で、lsquic は LiteSpeed / OpenLiteSpeed の下で動いている。HTTP/2 の HPACK 爆弾 (2016 年) と同じ「展開後の上限がない」型で、外部診断で UDP/443 の HTTP/3 を見つけたら実装を特定する価値がある。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/new-qpack-flaws-can-crash-http3-servers.html)

### [2026-10-22] PaaS の Railway に侵入、顧客の環境変数 (一部は復号済みの値) が読まれた可能性。秘密鍵を置いていた暗号資産ウォレットが抜かれる
- **何が起きたか**: Railway は、顧客の環境変数を保存するシステムで異常な活動を検知した。一部の利用者について、暗号化された環境変数と、場合によっては復号された内容 (API キー、DB の認証情報など) が読まれた可能性がある。同社は、AI 推論事業者を最終的に狙ってプラットフォーム企業を攻撃するキャンペーンの一環とみて、上流の事業者にキーの失効を依頼した。研究者の Taylor Monahan は、Railway に秘密鍵を置いていたウォレットから暗号資産が抜かれたと報告している。
- **悪用 / PoC**: **侵害と盗んだ秘密情報の悪用を確認**。
- **なぜ重要か**: 10/20 に報じた Zeabur に続き、PaaS が預かる秘密情報が狙われた。顧客が Railway を使っていれば、環境変数に入れた秘密情報はすべて漏れた前提で入れ替える必要がある。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/railway-says-intruder-may-have-accessed.html)

### [2026-10-22] INTERPOL「Serengeti III」: アフリカ 20 か国と米国で 1,462 人を逮捕、1 万 909 の犯罪ネットワークを無力化、1 億 500 万ドルを回収
- **何が起きたか**: INTERPOL は、オンライン詐欺、ランサムウェア、BEC を対象にした作戦 Serengeti III の結果を発表した。被害者は約 6.6 万人で、累計の損失は 3 億 8,500 万ドルを超える。ウガンダでは外国人 365 人と 2 つの詐欺組織を摘発し、アンゴラでは違法な暗号資産マイニング拠点 2 か所 (2,000 台超) を閉鎖した。ナイジェリアでは、210 万件のメールアドレスを集めていた BEC の運営者を逮捕した。
- **悪用 / PoC**: 該当なし (法執行)。
- **なぜ重要か**: アフリカ発の詐欺と BEC の規模と、摘発の対象になったインフラ (ドメイン、C2) が分かる。国内の BEC 被害の背景としても参考になる。
- 出典: [The Record](https://therecord.media/africa-cybercrime-interpol-arrests) / [BleepingComputer](https://www.bleepingcomputer.com/news/security/authorities-disrupt-nearly-11-000-cybercrime-networks-in-africa/)

### [2026-10-22] [続報] eMudhra、中間 CA の弱い鍵の問題を受けてグローバルの SSL/TLS 証明書事業から撤退
- **何が起きたか (前回から変わった点)**: インドの認証局 eMudhra は、SSL/TLS 証明書事業から自主的に撤退すると発表した。会長は、同事業は売上の約 1% で、コンプライアンスの費用が増えていたと説明した。8 つの中間 CA の鍵は 2025 年 4 月の鍵生成式典で作られ、2 回の監査を経ても 18 か月見つからなかった (秘密鍵の 1 つは数値の 4 だった、と Scott Helme)。失効・ステータスのサービスは、発行済みの証明書が切れるまで続ける。インドの MeitY は同社を擁護し、CERT-In はなりすましと中間者攻撃のリスクを警告した。
- **悪用 / PoC**: 鍵は誰でも導出できる (既報)。
- **なぜ重要か**: 中間 CA の有効期限は 2040 年 4 月で、失効を確かめない古いクライアントは信頼し続ける。組み込み機器、古いコンテナ、ベンダー同梱のトラストストアに残る問題として、診断で証明書チェーンを確認するときの観点になる。
- 出典: [The Record](https://therecord.media/indian-tech-company-announces-withdrawal-certificate-business-incident) / [Unit 42](https://unit42.paloaltonetworks.com/emudhra-certificate-compromise/)

### [2026-10-21] CISA KEV: 10/21〜22 の追加なし
- **何が起きたか**: KEV カタログ (2026.10.21 版、dateReleased 2026-10-21T14:04Z) で最も新しい追加日は 10/20 で、その 6 件 (SiteGuard、Plex 4 件、Siemens) は既報である。10/21〜22 の追加はなかった。
- **なぜ重要か**: PHP2Shell (悪用確認済み) と Arista CVE-2026-114625 (悪用確認済み) はまだ KEV に入っていない。KEV を優先度の唯一の根拠にしている顧客には、未登録でも悪用中であることを伝える必要がある。
- 出典: [CISA KEV JSON](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json)

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-10-21 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先
> 公開日は NVD の published (UTC)、NVD 未登録のものは OSV の published とベンダー勧告で確認した。EPSS は 10/22 時点で全件 0.01 未満 (未算出を含む)。KEV 入りはなし。

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-114509 / GHSA-f9x3-7vq9-cph6 | laravel/framework < 12.68.0、13.0.0〜< 13.29.0 | CWE-287, CWE-1287 / v4 9.2 | `TokenGuard` が `! empty()` しか見ず、配列や数値のトークンを通す → `retrieveByCredentials` の `whereIn` / `where` → MySQL の型変換で既存ユーザーに一致し、認証前にアカウントを乗っ取れる | [diff](https://github.com/laravel/framework/commit/8dbb08bccac1be095dba4a9d259a419620f1e8a5) | 認証前 / 深掘り |
| CVE-2026-19630 / CVE-2026-73206 / CVE-2026-114605 | BIND < 9.18.51 / 9.20.30 / 9.21.27、PowerDNS Auth・Recursor の各系、dnspython < 2.9.0 | CWE-407 / 770 / 674 / 3.1 7.5 | 1 メッセージ内の圧縮ポインタ (0xC0xx) をたどる回数にメッセージ全体の上限がない → `dns_name_fromwire` などが同じラベル列を何度も展開 → 少ない通信量で CPU を使い切る DoS | [BIND](https://gitlab.isc.org/isc-projects/bind9/-/commit/b606d21aafd528d64d87e613d3cc86ceb9ba1dc9) / [PowerDNS](https://github.com/PowerDNS/pdns/commit/754987158943f0e40b4257c02ce59ca32fa7fda0) / [dnspython](https://github.com/rthalley/dnspython/commit/b485e460c266540a1a09ca6d8d1d7b685b1d3023) | 仕様起因・複数ベンダー (PowerDNS が明記) |
| CVE-2026-94300 | BIND 9.11.0〜9.18.50、9.20.0〜9.20.29、9.21.0〜9.21.26 | CWE-362, CWE-415 / 3.1 8.1 | 交渉済み GSS-TSIG 鍵の共有コンテキストに `gss_get_mic()` / `gss_verify_mic()` がロックなしで並行アクセス → 署名済み UDP の再送と細工クエリで GSS ライブラリ内部が競合更新 → double free、RCE の可能性 | [diff](https://gitlab.isc.org/isc-projects/bind9/-/commit/36ed417fd3b60921fb8c2e32726316472bb19d61) | RCE 可能性 / 9.18 系は修正版なし (JVN) |
| GHSA-pxh4-856f-4h89 (CVE 未採番) | PyJWT ≤ 2.13.0 | CWE-347 / 3.1 ≈7.4 | `HMACAlgorithm.from_jwk` が `k=""` の oct JWK を拒否しない (2.13.0 の空鍵チェックは `prepare_key` だけ) → `PyJWKClient` などが `HMAC(key=b"")` で検証 → 空鍵で署名した任意のトークンが通る | [diff](https://github.com/jpadilla/pyjwt/commit/af8181ca0bec5e6b372fbba9afbe23702b787ceb) | PoC (advisory) / fast-jwt・ruby-jwt に続く 3 例目 |
| CVE-2026-114131 / CVE-2026-114132 | nuxt 3.11.0〜< 3.21.4、4.0.0〜< 4.4.4 (114132 は 4.x < 4.6.2 ほか) | CWE-436, CWE-863 / 3.1 ≈6.5 | routeRules はデコード前・大文字小文字区別のパスで照合し、router はデコードして大文字小文字を無視する → `/users/%61dmin` や `/Admin` がルールに一致しない → `appMiddleware: 'auth'` などが走らず保護ページが SSR で返る | [diff](https://github.com/nuxt/nuxt/commit/81f86ac5ee82bb1a9b887e59f3bc84624d711497) / [114132](https://github.com/nuxt/nuxt/commit/f6cfee52cf9576ddc4f4ee83b486969328b358f8) | PoC (advisory) |
| CVE-2026-114139 / GHSA-mchm-gjx6-7h55 | @sentry/nextjs 9.36.0〜< 9.47.2、10.x < 10.75.2 | CWE-693 / v4 (GHSA は CRITICAL) | SDK が注入する middleware の除外は tunnel パス配下すべて、rewrite は `?o=&p=` 付きの tunnel パスだけ → 差分のリクエストがアプリのルートに届く → middleware だけで認可するページを未認証で表示 | [diff](https://github.com/getsentry/sentry-javascript/commit/878b685c85dc12045e47e1932c96f5381d7ac532) | webpack ビルドのみ |
| CVE-2026-114145 / GHSA-83vg-56qc-22m7 | GitPython < 3.2.1 | CWE-696 / 3.1 7.5 | `Submodule.add()` の clone 前のパス検査が `.git/hooks` を通し、厳密な検査は clone 後にしか走らない → `_clone_repo` が `.git/hooks` に直接書く → `post-checkout` hook が次の git 操作で実行 (RCE) | [diff](https://github.com/gitpython-developers/GitPython/commit/97eadb888d2f99567e3113f4e455be4ca128f697) | PoC (advisory) |
| CVE-2026-114612 / GHSA-7hp6-4w63-5g45 | litellm 1.87.0 以降 (修正 1.100.4 / 1.101.3 / 1.102.2 / 1.103.1 / 1.104.0-rc.2) | CWE-269, CWE-345 / 3.1 9.9 | 保存データの暗号化とセッショントークンが同じ鍵・形式を共有 → API キー発行フローに偽の管理者メタデータを渡すと暗号化した結果が返る (暗号オラクル) → それを Bearer にすると proxy admin になり、MCP stdio から任意のコマンド実行 | [diff](https://github.com/BerriAI/litellm/commit/1d5fdc87fed66b49e1df8cf7d708ad93249eb7d0) | 9.9 / 1.91.0 以降は既定構成で成立 |
| GHSA-cg2g-xh64-v4q7 (CVE なし) | DOMPurify 3.4.4〜< 3.4.17 | CWE-79 / v4 (GHSA は CRITICAL) | `SAFE_FOR_TEMPLATES` と DOM を返すモードを併用 → `_scrubTemplateExpressions` が shadow root に再帰しない → 許可されない要素で分割した `{{ }}` が要素の除去後に結合し、テンプレートエンジンが評価して XSS | [diff](https://github.com/cure53/DOMPurify/commit/a77a3e78b59f72fa4d1c83f22e121ad9cc7d3575) | PoC (advisory) |
| CVE-2026-63430 / RUSTSEC-2026-0193 | ammonia < 3.3.2、4.0.0〜< 4.0.2、4.1.0〜< 4.1.3 | CWE-79 / v4 Low | 名前空間の検査は `annotation-xml encoding="text/html"` の DOM で行い、その後に属性フィルタが `encoding` を除去 → 再パースで子要素が MathML 名前空間になる → raw text 要素のガジェットで mXSS | [diff](https://github.com/rust-ammonia/ammonia/commit/004bf2cee4288f74a6ee619d589e3e90c24c09ca) | PoC 公開 |
| CVE-2026-110353 / CVE-2026-110354 | HAProxy 3.2〜< 3.4.6 (110354 は 3.x < 3.4.6) | CWE-252 / CWE-835 / 3.1 7.5 | `h2c_handle_ping()` だけがフレーム長に満たない short read を確かめない → 未完成の PING がバッファに残り、mux tasklet が空回り → CPU 100% のまま timeout まで張り付く (110354 は H1 chunked の再処理ループ) | [110353](https://git.haproxy.org/?p=haproxy.git;a=commit;h=cec63e95f62a7412484f1134f5aa227e5b7e1466) / [110354](https://git.haproxy.org/?p=haproxy.git;a=commit;h=077906da140a35873bf451d7e9f67646c9f37c81) | 前段プロキシ |
| CVE-2026-111181 / GHSA-27r3-jxmh-p828 | body-parser < 1.20.9、2.0.0〜< 2.4.0 | CWE-248 / 3.1 7.5 | 圧縮 body を zlib stream に流した後、error listener を外して放置 → 正しい圧縮フレームの後ろの余分なバイトが終了済みのデコーダで `error` を発火 → uncaught exception で Node プロセスが終了 | [2.x](https://github.com/expressjs/body-parser/commit/f7075eae3a84c3473ab4bf0a777da28db208e916) / [1.x](https://github.com/expressjs/body-parser/commit/1260c3845f54502a05a87594f09a334786bb34d7) | ルーティング前に届く |
| CVE-2026-114607 | better-auth 1.4.0-beta.18〜< 1.7.7 | 3.1 9.1 | Magic Link のトークンと OAuth の state が同じ verification テーブル・識別子空間を共有 → state 値を Magic Link トークンとして検証に通す → 他人としてログイン | [diff](https://github.com/better-auth/better-auth/commit/ac54bfd67821a7607533af2059858b12bc54e26a) | 9.1 |
| CVE-2026-113730 / GHSA-crwc-vw2r-qr6m | OGNL < 3.4.13 | 未確認 | stricter-invocation のブロックリストが、呼ぶメソッドの宣言クラスで判定 → `Method.invoke` を経由すると判定をすり抜けて `ProcessBuilder.start` に届く → 式評価から RCE | [diff](https://github.com/orphan-oss/ognl/commit/16396fa4b560221294c2ab9ca04b76b161115e7d) | PoC (advisory) |

**次点 (表に入れなかったもの)**: OpenTelemetry Python の `tracestate` ReDoS (CVE-2026-114603、[diff](https://github.com/open-telemetry/opentelemetry-python/commit/d5224bf4ffdf2aee1b592ad238dcc32ca957f26b))、Jupyter Server の gateway 用 WebSocket ハンドラでの認可漏れ (CVE-2026-114135、[diff](https://github.com/jupyter-server/jupyter_server/commit/35ffe5d435682128da16dc144a8e9e9f8fa85dd8))、Pillow 13.0.0 の約 30 件 (TIFF 保存時のヒープオーバーフロー CVE-2026-112393 など、[advisory](https://github.com/python-pillow/Pillow/security/advisories/GHSA-332p-7hrc-92wf) (commit 不明))、webpack-dev-server の proxy WebSocket で Host / Origin を検証しない CVE-2026-112085 ([advisory](https://github.com/webpack/webpack-dev-server/security/advisories/GHSA-cfqc-fj3v-j925) (commit 不明))、musl libc の regcomp の整数オーバーフロー CVE-2026-107891 (oss-security 10/21、NVD 未登録)。

### 今日の CVE 所感
- **仕様起因の DNS 圧縮ポインタ増幅が、BIND・PowerDNS・dnspython (と既報の Unbound) で同じ週に直った。** RFC 1035 には 1 メッセージあたりの展開量の上限がなく、「名前単位のホップ上限はあるが、メッセージ全体の累積上限がない」実装が狙い目になる。水平展開の候補は Knot、CoreDNS (miekg/dns)、hickory-dns、c-ares、dnsmasq、Go の `x/net/dns/dnsmessage`、Suricata や Zeek の DNS パーサ。
- **認可の判定と経路解決で、パスの正規化がずれている** (Nuxt、Sentry、Jupyter)。Next.js / SvelteKit / Remix / Astro の middleware matcher とルーターも同じ観点で監査する価値がある。診断では、パーセントエンコード、大文字小文字、末尾スラッシュ、`;` を変えたパスを保護ページに投げてみたい。
- **兄弟経路に修正が入らない「不完全修正」**: PyJWT は `prepare_key` だけを直し、`from_jwk` が漏れた。JWT の空 HMAC 鍵は fast-jwt、ruby-jwt に続く 3 例目なので、jose (node)、golang-jwt、jjwt、nimbus-jose-jwt の JWK → HMAC 経路で空の `k` を拒否しているかを確かめたい。
- **型の取り違えと鍵・ストアの使い回し**: Laravel (非文字列トークン)、LiteLLM (暗号コンテキストの共有で暗号オラクル)、Better Auth (識別子空間の共有) は、どれも「同じ値の空間を別の用途に流用した」型である。自作の認証部品のソースコード診断では、入力の型チェックと鍵の用途分離を最初に見る。
- **フレーム・ストリーム境界の DoS** (HAProxy の PING short read、body-parser の余分なバイト、QPACK の増幅) と、**サニタイザの mXSS** (ammonia、DOMPurify) も並んだ。後者は、属性・要素を除去した後の再パースで文脈が変わる点を、bleach / nh3 / sanitize-html で差分テストする価値がある。

## 日本国内のセキュリティ動向

### 国内インシデント・事故

#### [2026-10-22] カプコン「CAPCOM ID」に不正アクセス、全世界で 1,177 万 4,247 件のメールアドレスなどが漏えい。196 アカウントでパスワードが不正に変更
- **何が起きたか**: カプコンは 10/19 に CAPCOM ID への不正アクセスの痕跡を見つけて遮断し、同日中に不正アクセスを確認した。漏えいしたのは、メールアドレスとシステム固有の情報 (アカウント作成日時、最終ログイン日時、ログイン回数、最終ログイン時の IP) の 11,774,247 件 (全世界)。うち 43 件は生年月日、性別、国・地域、ニックネームも漏れた。196 件ではログインパスワードが不正に変更されていた (利用者のパスワード自体の漏えいは確認されていない)。カード情報は対象外。10/21 に警察と個人情報保護委員会に報告し、侵入経路は公表していない。
- **なぜ重要か**: 今月の国内事案で最大級の件数である。パスワードを知らずに「変更」できたことから、パスワードリセットなどアカウント管理機能が悪用された可能性がある (10/19 公表の Z会 Z-ID のリセット機能悪用と似た型。カプコンは手口を公表していない)。最終ログイン IP まで漏れており、標的型フィッシングの材料になる。
- 出典: [カプコン IR](https://www.capcom.co.jp/ir/news/html/261022.html) / [INTERNET Watch](https://internet.watch.impress.co.jp/docs/news/2150509.html)

#### [2026-10-21〜22] ラクス子会社のメール配信 SaaS「ブラストメール」に不正アクセス。API サーバー 2 台経由で全契約者の情報を持ち出し、一部の顧客は配信先リストも漏えい
- **何が起きたか**: ラクスライトクラウドは、ブラストメールで不審なアクセスを検知し、10/21 0:30 から管理画面と API を止めた (配信も 1:00 ごろから停止、再開は未定)。外部の第三者が API 用サーバー 2 台に侵入してコマンドを実行し、そこから販売管理システムとサービスの DB に接続してデータを持ち出した。販売管理システムからは全契約者の会社名、担当者名、電話番号、メールアドレス、契約・支払履歴が出た。一部の顧客では配信先リストも漏れた。侵入経路は調査中。利用組織の公表は 10/22 までに少なくとも 36 件に上る (石油資源開発 [JAPEX]、ヌーラボ、クラシコム、周南市など)。
- **なぜ重要か**: 10/19 のユミルリンク Cuenote に続き、メール配信 ASP が連続で侵害された。配信 SaaS は多数の企業の顧客アドレスを集めているので、委託元の公表が連鎖する。「API 層の RCE から業務 DB に直結する」構成は、SaaS 診断での典型的な横展開点である。
- 出典: [ラクス 第1報](https://www.rakus.co.jp/news/2026/1021-2.html) / [ラクス 第2報](https://www.rakus.co.jp/news/2026/1021-3.html) / [ブラストメール](https://info.blastmail.jp/information_20261021.html) / [JAPEX](https://www.japex.co.jp/news/detail/20261021_01/) / [ヌーラボ](https://nulab.com/ja/info/20261022-1-nulab/)

#### [2026-10-21] SaaS 型 EC 構築「futureshop」の運用サーバーに不正アクセス。対象サーバーの EC サイト・管理画面・FTP・API を停止
- **何が起きたか**: フューチャーショップは 10/21 10:14 ごろ、運用サーバーの一部への不正アクセスを確認し、11:30 から対象サーバーをメンテナンス状態にした。対象サーバー上の店舗では、EC サイト、管理画面、FTP・API が使えなくなった。他のサーバーの店舗への影響は確認されていない。情報漏えいの有無は調査中で、その後サービス再開を告知している。
- **なぜ重要か**: EC プラットフォームが侵害されると、出店各社の購入者情報の漏えいや、カード入力画面の改ざんにつながりうる。出店企業側の公表が後から出てくる可能性がある。
- 出典: [futureshop](https://www.future-shop.jp/news/2026/10/21.html)

#### [2026-10-21] イオン、グループ各社の一部 Web サイトへの不正アクセスを検知し、安全確認のためメンテナンス (報道では 13 社 42 サイト)
- **何が起きたか**: イオンは 10/21 付の PDF で、グループ各社の一部 Web サイトで第三者による不正アクセスを検知し、安全確認と原因調査を進めていると公表した。個人情報の流出は調査中。公式の発表は会社名とサイト数を示していないが、報道ではイオンリテールなど 13 社の計 42 サイトとされ、営業システムや EC への影響はないとされる。10/22 版では一次告知を確認できず除外したが、今回一次 PDF を確認した。
- **なぜ重要か**: 大企業グループのキャンペーンや店舗情報のサイトは、制作と運用が外部委託でばらばらになりやすく、CMS やプラグインの管理が行き届かない。PHP2Shell の公表直前という時期と重なるが、関連は公表されていない。
- 出典: [イオン (PDF)](https://www.aeon.info/wp-content/uploads/news/important/pdf/2026/10/261021R_2.pdf) / [流通ニュース](https://www.ryutsuu.biz/strategy/s102241.html)

#### [2026-10-22] フジッコ、キャンペーン応募受付の委託先サーバーに不正アクセス。延べ約 1 万 5,500 件が漏えいの可能性
- **何が起きたか**: フジッコによると、「カスピ海ヨーグルト もっと！とろぉ～もっちキャンペーン 第2弾」と「フジッコ大感謝祭キャンペーン」の非会員向け応募フォームの受付を委託している会社のサーバーが不正アクセスを受けた。10/21 に判明してサーバーを止めた。対象は延べ約 15,500 件で、氏名、年齢、性別、職業、婚姻状況、電話番号、メールアドレス、住所、アンケート情報。同社は「第三者に取得されたものとみなして」対応する。会員向けのフォームは別環境で影響はない。
- **なぜ重要か**: キャンペーン事務局の委託先からの漏えいは、今月繰り返し出ている型である (下の国交省の件も同じ)。委託元が把握しにくい短期の応募フォームが狙われている。
- 出典: [フジッコ (PDF)](https://www.fujicco.co.jp/upload/pr_261022.pdf)

#### [2026-10-22 報道] 国交省「住宅省エネ2024キャンペーン」事務局 (博報堂が運営) の補助金申請システムに不正アクセス。1 万 6,950 事業者、2 万 3,918 人分が流出の可能性
- **何が起きたか**: Security NEXT によると、2023〜2024 年度に実施した「住宅省エネ2024キャンペーン」で、事務局の博報堂が運営する事業者の補助金申請受付システムで不正な操作があり、登録事業者の情報が流出した可能性がある。10/20 時点で対象は 16,950 事業者、代表者氏名や個人事業主の住所、担当者の氏名・連絡先など 23,918 人分。システムの全機能を止め、点検後に必要な機能だけ再開する予定。国交省の一次発表は確認できていない。
- **なぜ重要か**: 終了したキャンペーンのシステムが、データを持ったまま動き続けていた構図である。官公庁の委託事業では、終了後のデータ削除とシステム廃止の確認が監査項目になる。
- 出典: [Security NEXT](https://www.security-next.com/191780) (一次発表は未確認)

#### [2026-10-22] バルテック (業務クラウド「MOT」シリーズ)、不正アクセスで 20 以上のサービスを停止。「PHP の脆弱性が原因」とした初報を「自社サービスの脆弱性」に訂正
- **何が起きたか**: INTERNET Watch によると、バルテックは不正アクセスを受け、MOT/Cloud、WEB 予約、MOT/Hotel、経費精算・勤怠、POS など 20 以上のサービスを止めた。利用者の個人情報が流出した可能性があり、10/26 中の復旧を予定している。原因は当初「PHP の脆弱性を狙った攻撃」としていたが、訂正で「自社サービス自体の脆弱性」と説明し直した (PHP 対応と混同したとしている)。
- **なぜ重要か**: PHP2Shell の騒ぎの最中には、別の原因の侵害も「PHP のせい」と発表されうる。攻撃が集中する時期の初報では、原因の帰属を慎重に読む必要がある。
- 出典: [INTERNET Watch](https://internet.watch.impress.co.jp/docs/news/2150396.html) / [バルテック](https://www.mot-net.com/news/version-upgrade/68630)

#### [2026-10-22] [続報] お名前.com デスクトップクラウド第 2 報: VPS 上の取引ツールに保存された FX 口座のログイン情報が盗まれ、不正な取引の報告。FX 事業者 6 社以上が告知
- **何が起きたか (前回から変わった点)**: GMO インターネットは 10/22 の第 2 報で、10/21 以降に利用者から「サーバー上の取引ツールに関連して、取引口座で第三者による不正な操作があった」との報告を受けたと公表した。サーバーに保存された取引口座のログイン情報が取られ、不正に使われた可能性がある。利用者には、このサービスのサーバー以外の端末からパスワードを変えるよう求めた。OANDA 証券、Titan FX、AXIORY、IS6FX (新規注文を一時制限)、XMTrading、IronFX が 10/21〜22 に告知し、FXTF も不正ログインの可能性を公表した。
- **なぜ重要か**: VPS の侵害が、そこに置かれた第三者サービスの資格情報を通じて金融被害に広がった。「サーバーに保存した資格情報」は、侵害されたホストの調査で必ず確認すべき項目である。
- 出典: [お名前.com 第2報](https://www.onamae.com/news/article/11593) / [GMO インターネット](https://internet.gmo/news/article/247/) / [OANDA 証券](https://www.oanda.jp/info/1456) / [piyolog](https://piyolog.hatenadiary.jp/entry/2026/10/23/014520)

#### [2026-10-21] [続報] コミックシーモア第 4 報: 流出は最大約 420 万件 (システムログ経由) と会員 DB の 319 件。侵入経路の特定と遮断は完了
- **何が起きたか (前回から変わった点)**: NTT ソルマーレは第 4 報で、会員 DB の 319 件 (メールアドレス、ハッシュ化パスワード、ニックネーム、生年月日、性別) と、システムのログファイルにあった最大約 420 万件 (重複を含む可能性。パスワードは含まない) の流出を確認した。侵入経路と手口の特定・遮断は完了したとしているが、内容は公表していない。サービスは段階的に再開する。
- **なぜ重要か**: 流出の大半が DB ではなく「ログファイル」からだった。ログに個人情報を出力していないかは、ソースコード診断と構成レビューで指摘しやすい項目である。
- 出典: [NTT ソルマーレ 第4報](https://www.nttsolmare.com/press/2026/1021.html) / [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2610/22/2000002500/)

> 参考 (小さめの続報): 岩井コスモ証券は 10/21 の報告で、不正取引を「AI を用いて脆弱性を突いた総当たり攻撃」と説明し、パスキーは突破されていないとした (一次ページは 404 で確認できず、[piyolog](https://piyolog.hatenadiary.jp/entry/2026/10/22/113434) の整理による)。ソフトバンクは 10/22 に My SoftBank などを再開した。NTT ドコモは 10/22 に予防措置としてコーポレートサイトや My docomo を一時停止し、不正アクセスは確認されていないとしている ([ドコモ](https://www.docomo.ne.jp/info/notice/page/261022_00_m.html))。旅行ゲーム「ワールドクエスト」は、PHP の対策がとれないとして 10/21 にサービスを終了した ([ITmedia NEWS](https://www.itmedia.co.jp/news/article/2610/22/2000002493/))。

### 国内の注意喚起・ガイドライン・政策

#### [2026-10-22] [続報] JPCERT/CC、PHP2Shell の注意喚起 (JPCERT-AT-2026-0033) を公開。侵害を調べるための観点 3 点を明記
- **何が起きたか**: JPCERT/CC は「国内で広く利用されていることを確認」として、対策の適用と侵害の有無の調査を求めた。調査の観点は次の 3 点である。(1) 過去の HTTP レスポンスに、不自然に長い、または異常な形式の PHPSESSID Cookie が出ていないか。(2) 不審な multipart/form-data リクエストと、その前後の PHP のメモリ上限エラーや HTTP 500。(3) PHP ワーカーの異常終了や頻繁な再起動。悪用経路が複数あり、単一の検知ルールでは見つからず、ログに痕跡が残らない場合もあると注記した。8.1 以前は修正版がないので、サポート版への移行を勧めている。
- **なぜ重要か**: PHP2Shell について、国内の公的機関が侵害調査の具体的な観点まで示した。Amazon の「10/17 から悪用」(セキュリティニュース欄) とあわせると、ログの調査範囲は 10/17 以前からにすべきである。
- 出典: [JPCERT/CC](https://www.jpcert.or.jp/at/2026/at260033.html)

#### [2026-10-22] [続報] IPA「PHP の脆弱性対策について (PHP2shell)」— EOL 版の利用者に、経営層も含めて「更新・移行」か「廃止」かの判断を求める
- **何が起きたか**: IPA は 10/21 の「事前準備のお願い」に続く本アラートで、3 段階の対応を示した。(1) 使っている PHP のサポート状況を確かめる (8.1 以前は修正なし)。(2) 更新・移行までの暫定策とアクセス制限をとる。(3) システムの役割と代替の可能性を確かめ、運用を続けるかを見直す。長く更新していないシステムは資料や担当者、保守契約がないことが多いとして、事業責任者・経営層も含めて人員・予算・保守体制を確保できるか検討し、見通しが立たなければ廃止も計画するよう求めた。
- **なぜ重要か**: 公的機関の注意喚起が、パッチの適用だけでなく「システムの廃止」の判断まで踏み込んだ。顧客への報告では、IPA のこの 3 段階をそのまま使える。
- 出典: [IPA](https://www.ipa.go.jp/security/security-alert/2026/alert20261022.html)

#### [2026-10-22] [続報] 首相が X で再発信、「状況によってはサイトの一時停止も重要」。コドモンは修正公開の約 9 時間前に全サービスを予防停止
- **何が起きたか**: 10/21 夜の投稿に続き、首相は 10/22 に、個人の公式サイトも PHP 対応で一時停止し、22 日午後までに再開したと説明した。深夜に注意・警戒情報に気付けない管理者がいるとして、国家サイバー統括室の X アカウントのフォローを呼びかけた。関連して、コドモンは 10/21 14:16 (修正公開の約 9 時間前) に全サービスの予防停止を告知し、10/22 3:22 に主要サービスを再開した。さくらインターネットは 10/21 22:30 から予防メンテナンスに入り、EOL の PHP にも修正を当てたと公表した。
- **なぜ重要か**: 修正の公開前に止めるという判断が、国の発信と大手の実例でそろった。今後の同種の事案で、顧客と「止める基準」を事前に決めておく材料になる。
- 出典: [ITmedia NEWS (首相)](https://www.itmedia.co.jp/news/article/2610/22/2000002512/) / [ITmedia NEWS (コドモン)](https://www.itmedia.co.jp/news/article/2610/22/2000002528/) / [さくらインターネット](https://www.sakura.ad.jp/corporate/information/announcements/2026/10/22/1968226117/)

#### [2026-10-22] [続報] 総務省「フロンティア AI 時代の通信事業におけるデータの保護・セキュリティの在り方に関する検討会」第 1 回。規制の在り方まで検討し、2027 年 6 月ごろ取りまとめ
- **何が起きたか (前回から変わった点)**: 10/16 に設置を報じた検討会の第 1 回が 10/22 に開かれた。検討事項は、(1) 技術面の対策、(2) 新しい通信エコシステムを踏まえた体制面の対策、(3) 規制の在り方。事務局資料は、総務省に報告された漏えいが件数・規模とも増え、特に不正アクセスによるものが急増していると整理し、KDDI (762 万件、7/29 指導)、楽天モバイル、IIJ、LINE ヤフーを例に挙げた。11〜12 月に通信事業者やクラウド事業者のヒアリングを行い、2027 年 1 月に中間取りまとめ案を出す。
- **なぜ重要か**: 電気通信事業法の「通信の秘密」の規律を軸に、通信事業者のセキュリティを規制で底上げする議論が始まった。クラウド事業者もヒアリングの対象に入っている。
- 出典: [総務省 第1回](https://www.soumu.go.jp/main_sosiki/kenkyu/data_protection/02kiban18_02000510.html) / [資料 1-2 (PDF)](https://www.soumu.go.jp/main_content/001097489.pdf)

#### [2026-10-22] IPA・JPCERT/CC「脆弱性関連情報の届出状況 2026 年第 3 四半期」: 7〜9 月の届出は 240 件、累計 2 万 553 件
- **何が起きたか**: 7〜9 月の届出は 240 件 (ソフトウェア製品 179 件、ウェブサイト 61 件) で、累計は 20,553 件になった。製品の JVN 公表は 79 件で、届出から 45 日以内の公表は 29 件 (37%)。JVN の公表前に重要インフラ事業者などへ優先提供したのは 12 件 (累計 113 件)。製品の「取扱い中」は 2,721 件ある。
- **なぜ重要か**: 製品の届出が 2 四半期続けて 170 件台と高い。AI による脆弱性発見の増加が届出制度の処理負荷に表れている可能性がある (報告書は原因に触れていない。自分の推測)。
- 出典: [JPCERT/CC 届出状況 (PDF)](https://www.jpcert.or.jp/pr/2026/vulnREPORT_2026q3.pdf)

#### [2026-10-21] IPA「Oracle Java の脆弱性対策について (2026 年 10 月)」
- **何が起きたか**: IPA は、Oracle の 10 月 CPU のうち Java SE 分 (Java SE 27 / 26.0.2 / 25.0.4.1 / 21.0.12.1 / 17.0.20.1 / 11.0.32.1 / 8u503 が対象) について、早急な更新を呼びかけた。ITmedia によると、Java の脆弱性は 55 件。
- **なぜ重要か**: CPU 全体は既報だが、IPA の注意喚起が出たことで、国内顧客の更新管理の根拠として使える。
- 出典: [IPA](https://www.ipa.go.jp/security/security-alert/2026/1021-jre.html)

> 参考 (運用): JPCERT/CC のインシデント報告の Web フォームは 10/21 18:00 から緊急メンテナンス中で、メールでの報告は通常どおり受け付けている ([JPCERT/CC](https://www.jpcert.or.jp/maintenance20261022.html))。JVN iPedia と MyJVN も 10/22 から一時停止しており、再開時期は未定 ([JVN](https://jvn.jp/nav/info2026102281.html))。どちらも理由は示されていない。

### 国内製品の脆弱性 (JVN)

> 範囲内に新しく公開された JVN は 3 件で、国内ベンダー製品の JVN# の新規はなかった。JVN iPedia が止まっているため、国内ベンダーによる PHP2Shell の影響告知で補った。

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| 2026-10-22 | JVNVU#91023667 / CVE-2026-112148 | LIFF SDK 2.20.0〜2.31.0 / LINE ヤフー | DOM ベースの XSS。LIFF SDK を使うサイトを開いた利用者のブラウザで任意のスクリプトが動く。修正版は 2.31.1 (開発者自身が JPCERT/CC に報告) | v3.1 6.1 / v4.0 5.1 (CWE-79) | [JVN](https://jvn.jp/vu/JVNVU91023667/) |
| 2026-10-22 | JVNVU#91196958 / CVE-2026-94300 | ISC BIND 9.11.0〜9.18.50、9.20.0〜9.20.29、9.21.0〜9.21.26 | GSS-TSIG の共有コンテキストへの並行アクセスでメモリ破壊、RCE の可能性。OpenAI の Dave Aitel も独立に報告。9.18 系は修正版なし、回避策なし | v3.1 8.1 | [JVN](https://jvn.jp/vu/JVNVU91196958/) / [ISC](https://kb.isc.org/docs/cve-2026-94300) |
| 2026-10-22 | JVNVU#91196958 / CVE-2026-19630 | ISC BIND (同上) | 圧縮ポインタを上限なくたどり、CPU とメモリを過大に消費 (増幅型 DoS) | v3.1 7.5 | [ISC](https://kb.isc.org/docs/cve-2026-19630) |
| 2026-10-22 | JVNVU#91196958 / CVE-2026-96888, CVE-2026-97313 | ISC BIND 9.16.0〜 (同上) | redirect ゾーンと `qname-minimization strict` の組み合わせでアサーション失敗 (96888)。RPZ を recursive-only の異なる 2 つ以上で構成すると、RD=1→RD=0 のクエリで異常終了 (97313) | 各 v3.1 7.5 (DoS) | [ISC 96888](https://kb.isc.org/docs/cve-2026-96888) / [ISC 97313](https://kb.isc.org/docs/cve-2026-97313) |
| 2026-10-22 | JVNVU#99905564 / CVE-2026-109618, -109619 [続報] | PHP / ソリトンシステムズ製品 | PHP2Shell の JVN 掲載 (CVE は既報)。新しいのは国内ベンダーの状況で、ソリトンは FileZen、InfoTrace Mark II、NetAttest D3Manager、Smart eGate、Soliton SecureDesktop / SecureGateway、NetAttest EPS Cloud が「影響あり」とした (管理ページで PHP を使用、対策ファームは準備中で、管理ページのアクセス制限を推奨) | v4.0 9.2 / 未認証 RCE、悪用試行あり | [JVN](https://jvn.jp/vu/JVNVU99905564/) / [ソリトン](https://www.soliton.co.jp/support/2026/006929.html) |
| 2026-10-21〜22 | (ベンダー告知) CVE-2026-109618, -109619 | PowerCMS / アルファサード | ダイナミックパブリッシングと DynamicMTML で PHP を使う。該当機能の利用者に PHP の更新と、影響が分かるまでのサイト一時停止の検討を求めた。PowerCMS クラウドは対応済み | 同上 | [PowerCMS](https://www.powercms.jp/news/php_cve-2026-109618cve-2026-109619.html) |
| 2026-10-22 | (ベンダー告知) CVE-2026-109618, -109619 | トレンドマイクロ製品 / NEOJAPAN desknet's NEO | トレンドマイクロは KA-0024791 で製品への影響の調査状況と検知機能を案内。NEOJAPAN は desknet's NEO / AppSuite の標準製品とクラウドは PHP を使っておらず影響なしと公表 | 同上 | [トレンドマイクロ](https://success.trendmicro.com/ja-jp/solution/KA-0024791) / [NEOJAPAN](https://www.neo.co.jp/news/20261022/) |

### 国内コミュニティ・研究・イベント

#### [2026-10-22] piyolog「NEC 委託先への不正アクセスについてまとめてみた」— NEC、大阪大学、大阪公立大学 (第 5 報) の公表を時系列で突き合わせ
- **何が起きたか**: 大阪公立大学は 10/21 の第 5 報で、10/2 からの基盤システムの障害について、NEC から「開発・保守の再委託先が 9 月下旬に攻撃を受け、その事業者の正規アカウントで同学のシステムに不正アクセスされた」との報告を 10/20 に受けたと公表した。piyolog はこれと NEC・大阪大学の公表を突き合わせ、被害が「顧客環境のファイル暗号化」と「NEC が共有に使っていたクラウドストレージからの漏えい」の 2 系統であることを整理した。
- **なぜ重要か**: 再委託先の正規アカウントで顧客環境に入られる型は、委託先管理の監査やペンテストのシナリオ (委託先アカウントを起点にした内部侵入) にそのまま使える。
- 出典: [piyolog](https://piyolog.hatenadiary.jp/entry/2026/10/22/114426)

#### [2026-10-22] ITmedia NEWS「PHP 脆弱性 “PoC フライング公開” の経緯、支援財団が公表」
- **何が起きたか**: PHP 財団の説明として、次の点を伝えた。Alpha-Omega と協力して Anthropic の Claude Mythos でスキャンしていたこと。10/21 未明に CVSS などが SNS で拡散したため、公開を 22 日 23 時から 21 日 23 時に前倒ししたこと。21 日 5 時ごろに Calif が動く PoC の動画を誤って公開したこと。Chainguard が禁止期間を破り、6 時間以上早く修正入りの実行環境を出したこと。SNS で広まった PoC は PHP のセキュリティチームの調査では動かなかった。Cloudflare の CEO は、悪用試行が公表 45 分で数万件、2 時間で数十万件に達したと投稿した。
- **なぜ重要か**: 国内の予防停止や首相の投稿が、「公開時刻の前倒しと PoC の先出し」を前提にしていたことが分かる。調整開示がどこで崩れたかの一次整理として、今後の開示調整の参考になる。
- 出典: [ITmedia NEWS (経緯)](https://www.itmedia.co.jp/news/article/2610/22/2000002525/) / [ITmedia NEWS (Cloudflare)](https://www.itmedia.co.jp/news/article/2610/22/2000002516/)

#### [2026-10-22] セキュリティ対策Lab「ブラストメール不正アクセスの影響組織まとめ」— 公表 36 件を一次発表のリンク付きで整理
- **何が起きたか**: ロケットボーイズのセキュリティ対策Lab は、ブラストメールの侵害について委託元 (企業、自治体、新聞社、団体) の公表を一覧にし、「漏えい確定」「可能性」「予防停止」を区別した。周南市の 302 件は登録件数で、漏えいが確定した件数ではないと注記している。
- **なぜ重要か**: サプライチェーン型の漏えいで、自社や顧客の委託先が含まれるかを確かめる索引として使える。
- 出典: [セキュリティ対策Lab](https://rocket-boys.co.jp/security-measures-lab/blastmail_20261022_summary_updated_23_public_notices/)

> イベント: CODE BLUE 2026 はトレーニングが 11/11〜15、カンファレンスが 11/17〜18 で、事前登録は 11/10 まで ([CODE BLUE](https://codeblue.jp/))。範囲内に新しいお知らせはない。Japan IT Week 秋 2026 (幕張メッセ、10/21〜23) は開催中だが、セキュリティ関連の大きな発表は確認できなかった。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 60 (RSS / API / 個別ページ。4 系統の調査を並行で実施)
- 採用件数: AI技術=14 / AIセキュリティ=10 / セキュリティ=10 / CVE=14 行 (+次点 5) / 国内インシデント=9 (+参考 4) / 国内政策=6 / JVN=7 行 / 国内コミュニティ=3
- 除外理由内訳: 古すぎ=約 12 (NIST/NSA/CISA の超知能訓練時の IR 指針 [10/16]、Anthropic のアタックサーフェス縮小研究 [原典 10/20]、Wasmtime の旧 advisory、JOGMEC・Z会・ZonExpert など) / 重複=約 15 (Zeabur [10/20 既報]、Chrome の ClickFix 警告、OpenCode Console 侵害、Storm-0940、Claude Duet、10/20 の KEV 6 件、Unbound CVE-2026-96405、Tomcat・ICS などの既報 JVN) / 日付不明=2 (Symantec の原文、国交省の一次発表)
- 確認できなかった一次情報: 国交省の一次発表 (Security NEXT のみ)、岩井コスモ証券の 10/21 報告 (piyolog 経由)、バルテックの不正アクセス告知本文 (INTERNET Watch 経由)、Symantec の原文 (The Decoder 経由)
- 取得失敗ソース:
  - openai.com/index/* (Cloudflare のチャレンジ / 403)。RSS の日付のみ取得し、Decisions API は TechCrunch で代用。Uber の全社導入、Cloudflare と Daybreak、cyber defenders の提言は不採用
  - CISA のアドバイザリ RSS (Akamai の Access Denied)。KEV の JSON は取得できた
  - api.github.com / raw.githubusercontent.com (403)。GHSA の公開日は OSV で確認し、Laravel の修正は jsDelivr 経由のソースで確認
  - Dark Reading (Cloudflare の JS チャレンジ)、Arista のアドバイザリページと FoxIO のブログ (接続リセット。BleepingComputer / THN で代用)
  - JVN iPedia / MyJVN (10/22 からサービス停止中)、国家サイバー統括室 (JS 読み込みで本文なし)、警察庁、金融庁、内閣府、Secureworks JP、マクニカ
  - WebSearch は対象日に絞り込めず、主に RSS と API で収集した

</details>
