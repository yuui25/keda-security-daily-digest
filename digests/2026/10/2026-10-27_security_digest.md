# KEDA Daily Digest — 2026-10-27 (JST)

> 採用範囲: 公開日 2026-10-25 〜 2026-10-27
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

週明けの 10/26 (月) に、先週から続く大型案件の続報と、国内の大型漏えいの公表が集中した。
- **セキュリティ (最優先)**: Brotli デコーダの OOB 書き込み (CVE-2026-111497) で、Microsoft が .NET・Visual Studio・PowerShell に定例外パッチを出した。PHP の Windows 公式ビルドも Brotli 同梱のため 2 回目の再ビルドとなり、JPCERT/CC は注意喚起 (AT-2026-0034) を出した。「外部の URL を取りに行くクライアントが、攻撃者のサーバーの応答を自動で解凍する」経路が Node・Python・.NET・PHP にまたがった。今日の深掘りで扱う。
- **セキュリティ (ほか)**: PHP2Shell は、ハニーポットで公開 PoC と同じ手順の RCE が初めて具体的に記録され、OT ベンダー (Schneider・Siemens・ABB/B&R・Belden) の影響判定も出そろい始めた。Wiz は GitHub Actions の 2026 年の Pwn Request 対策に抜け道 (古い SHA へのピン留め、issue_comment、スクリプトインジェクション) が残ると示した。Fortinet は AI で見つけた Critical/High を FortiOS などで修正済みだが、詳細は 11/10 まで伏せる。CISA KEV は 10/24 以降の追加なし。
- **新規 CVE**: 「2 つのパーサーの解釈差」が中心。Rust zip2 の Central Directory と Local File Header の名前の食い違い (CVSS v4 10.0)、Elixir bandit のチャンク行の bare LF による request smuggling、hackney の IP 表記差による SSRF 許可リスト回避。go-playground/webhooks の「secret が空なら検証しない」を踏んだ Burrito (CVSS 9.9) も共通 sink 型として要注目。
- **AI**: Anthropic が S-1 を提出して IPO を正式申請 (売上の 5〜7% が規約違反の蒸留目的の顧客由来と開示)。OpenAI は GPT-6.1 Terra (コンピューター操作向け、$1/$5) を公開。AI セキュリティでは、OpenHands Agent SDK の未認証 RCE (サンドボックスのサーバーが 0.0.0.0・認証なしで起動、CVSS 9.8)、Google 公式 MCP Toolbox のファイル持ち出し (CVSS v4 9.3)、vLLM 0.32.0 の 8 件 (pickle RCE を含む) が実務に近い。
- **国内**: GMO「お名前.com デスクトップクラウド」は、攻撃者が **本日 10/27 12:00** に利用者情報の公開とランサムウェア攻撃を行うと予告していると第 7 報で公表。ユミルリンク (Cuenote) の漏えいは 50 システム・延べ 5,162 万件に拡大し、JR 3 社のエクスプレス予約・スマートEX 約 17 万件にも及んだ。Joshin 最大約 600 万件、楽天トラベル合計約 354 万件、ギフティの e ギフト不正発行 (損失約 5.5 億円) も公表された。政府は初の関係閣僚会議を開き、首相が「アクセス無害化も含む」緊急対策パッケージを来週中にまとめるよう指示した。JVN は 10/26 に新規公開を再開 (国交省の電子納品物検査支援システムなど)。

## 今日の深掘り

### Brotli デコーダの OOB 書き込み (CVE-2026-111497) — 「応答を自動で解凍する HTTP クライアント」が攻撃面になり、.NET と PHP (Windows) にまで広がった

- **概要 (事実)**: Google の Brotli C デコーダ (1.0.3〜1.0.9、1.1.0、1.2.0) の境界外書き込み (CVE-2026-111497、通称 Node2Shell / HTTP2Shell / Broccoli2Shell) で、影響を受けるエコシステムが 10/25〜26 にさらに広がった。
  - Microsoft は 10/25 に定例外の更新を出した。対象は .NET 8.0.33 / 9.0.22 / 10.0.14、.NET 11 RC3、Visual Studio 2019 / 2022 / 2026、PowerShell 7.4 / 7.5 / 7.6。評価は CVSS v3.1 8.1 の「権限昇格」、Exploitation More Likely。
  - PHP は Windows 公式ビルド 8.2〜8.5 を Brotli 1.2.1 で作り直した (8.5.12-1 / 8.4.27-1 / 8.3.36-1 / 8.2.35-1)。5 日間で 2 回目の再ビルドになる。
  - JPCERT/CC は 10/26 に注意喚起 JPCERT-AT-2026-0034 を出し、更新に加えて侵害の有無の調査も求めた。JVN も JVNVU#97400824 を採番した。
- **技術的な中身**:
  - 欠陥: ストリーミングデコーダが不正な block switch を受けたとき、恒久的なフォーマットエラーにせず「入力が足りない (NEEDS_MORE_INPUT)」と誤って返す。呼び出し側は入力を追加し続け、デコーダは 8 バイトの内部バッファの範囲外に書き込む。修正は 1.0.10 / 1.1.1 / 1.2.1。根本原因の修正は 2026 年 2 月に上流に入っていたが、セキュリティ修正と認識されずリリースされていなかったという。
  - 到達経路は 3 種類ある。
    1. **リクエストボディ**: `Content-Encoding: br` を受け付けるサーバー (Express 5 / body-parser 2、ASP.NET Core の `AddRequestDecompression`)。
    2. **取りに行った応答**: Node の `fetch()`、.NET の `HttpClient` の `AutomaticDecompression`、PHP cURL の `CURLOPT_ENCODING=""` (THN によると Guzzle 7.16.1 / 8.3.1 は既定でこの値を設定する)、Python の requests / urllib3 / httpx / aiohttp (Brotli パッケージが入っていれば自動で解凍)。
    3. **圧縮ファイル**: 7-Zip-zstd、p7zip、DuckDB、Apache Arrow、EDK II などは、公開トラッカーの集計ではまだ未修正。
  - 経路 2 は、攻撃者が受け手 (サーバー) を用意する側に立つ。`Accept-Encoding` から br を外しても、悪意のあるサーバーが br で送りつければクライアントは解凍しうるので、受信側の WAF や入力フィルタでは止まらない。
  - 深刻度: Google の CVSS v4 は 9.2。公開 PoC はわざと弱めたビルドでしか RCE しないが、Imperva は公式の Node.js 24.22.0 (linux/arm64) で、何回か試すと RCE が成功したと報告している (exploit は非公開)。.NET の経路は 3 つとも既定では無効で、明示的に有効にしたアプリだけが対象。
- **背景・経緯 (過去の事象の引用)**:
  - Brotli デコーダには CVE-2020-8927 (1.0.9 より前、大きな入力チャンクで整数オーバーフロー) の前例がある。
  - 本件は OpenAI Codex Security が見つけ、調整開示の枠組み「Patch the Planet」で開示された。本ダイジェストでは 10/24 号 (Imperva の公式ビルドでの RCE)、10/25 号 (Bun・Python・Envoy・Istio への波及) で続報を扱ってきた。
  - 圧縮ライブラリが他のソフトに同梱 (vendoring) されて広がる構図は、zlib の CVE-2022-37434 (inflateGetHeader のヒープオーバーフロー) でも見られた。
- **なぜ今これが重要か (評価)**:
  - 悪用状況: 野良の悪用は報告されていない。KEV にも入っていない。ただ、Microsoft の Exploitation More Likely 評価と、公式ビルドでの RCE 実証が出ている以上、時間の問題と見るべき。
  - 診断業務への影響: **SSRF・Webhook・URL プレビュー・OAuth 連携など「外部 URL を取りに行く機能」の評価に、そのまま 1 項目足せる**。従来の SSRF は「内部に届くか」を見ていたが、本件では「攻撃者のサーバーから返った応答そのものがサーバー側でコードを実行させる」ので、内部到達が塞がれていても成立しうる。
  - 依存スキャンの盲点: Brotli を自前でバンドルするソフト (Node のバイナリ、PHP の Windows ビルド、.NET ランタイム、7-Zip 系) は、OS の libbrotli を更新しても直らない。SCA の結果に libbrotli が出てこないことは安全を意味しない。PHP の Windows ビルドは `php -v` の表示が変わらないので、ファイル名の `-1` か SHA-256 で見分ける必要がある。
- **読者が今日できること**:
  - コード検索: `AddRequestDecompression` / `AutomaticDecompression` / `BrotliStream` (.NET)、`CURLOPT_ENCODING` / Guzzle の `decode_content` (PHP)、`zlib.brotliDecompress` / `fetch(` (Node)、`import brotli` / `brotlicffi` (Python) を grep し、信頼できない入力が届く箇所を洗い出す。
  - 診断: URL 取得機能のある対象では、自前のサーバーから `Content-Encoding: br` で不正なストリームを返し、ワーカーの異常終了・500・応答の遅延を観察する (本番環境ではクラッシュを起こしうるので、事前に合意を取ること)。
  - 棚卸し: `node -p process.versions.brotli`、`dotnet --list-runtimes`、`pip show Brotli brotlicffi`、Windows の PHP のビルド名、コンテナイメージ内の 7-Zip / p7zip / DuckDB のバージョンを確認する。すぐに更新できない場合、Guzzle は `decode_content=false`、cURL は `CURLOPT_ENCODING` を設定しないことで経路 2 を閉じられる。
- 出典: [BleepingComputer (Microsoft の定例外パッチ, 2026-10-26)](https://www.bleepingcomputer.com/news/microsoft/microsoft-releases-emergency-net-patches-for-critical-brotli-flaw/) / [SecurityWeek (2026-10-26)](https://www.securityweek.com/node2shell-brotli-flaw-triggers-patching-across-microsoft-node-js-python-packages/) / [BleepingComputer (HTTP2Shell, 2026-10-26)](https://www.bleepingcomputer.com/news/security/critical-http2shell-brotli-vulnerability-triggers-emergency-patches/) / [The Hacker News (PHP の Windows 再ビルド, 2026-10-26)](https://thehackernews.com/2026/10/php-issues-second-windows-security.html) / [JPCERT-AT-2026-0034](https://www.jpcert.or.jp/at/2026/at260034.html) / [JVNVU#97400824](https://jvn.jp/vu/JVNVU97400824/) / 背景: [NVD CVE-2020-8927](https://nvd.nist.gov/vuln/detail/CVE-2020-8927) / [NVD CVE-2022-37434](https://nvd.nist.gov/vuln/detail/CVE-2022-37434)

## AI 技術・トレンド

### [2026-10-26] Anthropic が SEC に S-1 を提出し、IPO を正式申請 (Nasdaq、ティッカー「ANT」)
- **何が起きたか**: Anthropic, PBC が Form S-1 を提出し、Class A 株を Nasdaq Global Select Market に「ANT」で上場する予定と発表した (主幹事は Goldman Sachs と Morgan Stanley、株数と価格帯は未定)。TechCrunch によると、2026 年上期の売上は 163 億ドル (前年同期 12 億ドル)、営業損失 6 億 9,300 万ドル。The Decoder によると、売上の約 5〜7% は利用規約に違反した顧客 (主に蒸留目的) からで、80% は従量課金。共同創業者 7 人の「Founder LLC」が議決権の 50.1% を持つ。The Verge によると、計算資源の契約は SpaceX に月約 31 億ドル、Google に 2033 年までに 1,145 億ドル以上、Amazon に 10 年で 1,100 億ドルなど。リスク要因にはモデルの「意図しない・ミスアラインした・自律的な振る舞い」も挙げている。
- **なぜ重要か**: 主要な AI ベンダーとして初めて、財務とリスクが法定の開示文書で出た。セキュリティの観点では「売上の 5〜7% が蒸留目的の規約違反」という数字が大きい。モデルの不正利用 (蒸留・API 悪用) が事業規模で起きていることが定量的に示された (下の Xint「Compaction Smuggling」とも直結)。
- 出典: [Anthropic](https://www.anthropic.com/news/s1-sec) / [TechCrunch](https://techcrunch.com/2026/10/26/anthropic-officially-files-for-its-public-debut/) / [The Decoder](https://the-decoder.com/anthropic-opens-its-books-for-wall-street-showing-record-revenue-and-mounting-obligations/) / [The Verge](https://www.theverge.com/ai-artificial-intelligence/1018738/anthropic-ipo-s1-filing-weird-details)

### [2026-10-26] OpenAI「GPT-6.1 Terra」を公開。コンピューター操作向けの中位モデルで、入力 $1 / 出力 $5 (100 万トークンあたり)
- **何が起きたか**: OpenAI が `gpt-6.1-terra` を公開した。料金は入力 $1、キャッシュ入力 $0.05、出力 $5 で、GPT-6.1 Sol ($2/$10) の半額。ChatGPT Work と Codex で Plus / Pro / Enterprise / Edu に提供する。OpenAI は、コンピューター操作のベンチマーク Agents' Last Exam で GPT-6 Astra と同等、Terminal-Bench 4.0 で 50.3% (GPT-5.6 Terra は 21.5%)、社内のハルシネーション評価で誤答率を 53.6% から 16.7% に下げたと主張している。
- **なぜ重要か**: GUI 操作エージェントの単価が下がり、業務への組み込みが進む。フォーム入力や画面操作をするエージェントは、Web ページ経由の間接プロンプトインジェクションの標的が増えることを意味する。診断対象の Web アプリが「エージェントに操作される」前提での評価も必要になってくる。
- 出典: [OpenAI](https://openai.com/index/introducing-gpt-6-1-terra) (本文は 403、RSS の pubDate で日付を確認) / [iThinkDiff](https://www.ithinkdiff.com/gpt-6-1-terra-launch-half-price-computer-use/)

### [2026-10-26] Meta、AI インフラの資金として最大 950 億ドルの株式売却を計画
- **何が起きたか**: Meta が、議決権のない新しい Class C 株などで最大 950 億ドルを調達する計画を示した。うち 600 億ドルは Class C の取引開始後に市場で売却する (早くて 2027 年 Q1)。Nvidia・AMD・Broadcom が最大 50 億ドル分の取得に関心を示したという (拘束力なし)。
- **なぜ重要か**: ハイパースケーラーの AI 設備投資が、株式による調達に頼る段階に入った。セキュリティへの直接の影響はないが、業界の資金の流れとして押さえておく。
- 出典: [The Decoder](https://the-decoder.com/meta-plans-up-to-95-billion-in-stock-sales-to-fund-its-ai-buildout/)

### [2026-10-26] SpaceX、Apollo と約 400 億ドルの GPU リース契約。Grok と Cursor の計算基盤に
- **何が起きたか**: SpaceX が規制当局への提出書類で、Apollo が運用する事業体が GPU とサーバーを購入し、SpaceX に約 5〜5.25 年リースする契約を開示した。Nvidia Vera Rubin を想定し、2027 年上期から。SpaceX の AI 部門 (Grok、Cursor、クラウド) の Q3 売上は 76 億ドル。
- **なぜ重要か**: コーディングエージェント Cursor を抱える xAI / SpaceX 陣営の計算資源が厚くなる。上の S-1 によれば Anthropic も SpaceX から計算資源を買っており、フロンティア各社の基盤が相互に依存し合う構図が見える。
- 出典: [TechCrunch](https://techcrunch.com/2026/10/26/spacex-locks-in-40b-gpu-financing-deal-with-apollo/)

### [2026-10-26] Microsoft、最大 6 万人に早期退職を提示。Copilot / CoreAI のチームも対象、Security は対象外
- **何が起きたか**: The Verge によると、Microsoft は米国・英国・カナダ・インドで最大 6 万人に自主退職の募集を出した。AI experiences、Copilot、CoreAI、Windows + Devices などが対象で、Security チームは外れている。
- **なぜ重要か**: AI 投資を優先した人員の組み替えの一環。セキュリティ部門を対象外にした点は、同社が SFI (Secure Future Initiative) 以降のセキュリティ投資を維持する意思の表れとも読める (評価)。
- 出典: [The Verge](https://www.theverge.com/tech/1018666/microsoft-expands-buyouts-60000-employees-eligible)

### [2026-10-25] Nvidia、ロボット動画のラベリング用モデル群「Flora」をオープン化。GPT-6 Astra 比で最大 125 倍安いと主張
- **何が起きたか**: Qwen3.5 をファインチューンした 3 モデル (9B のセグメンテーション、27B のキャプション、27B の報酬モデル Flora-Rewarder) の重みを Hugging Face で公開した。Nvidia は 1 時間の動画あたりのコストを $0.72 (GPT-6 Astra は $88.49)、品質は 57.1% 対 53.7% と主張するが、GPU 1 時間 $10 を仮定した試算で、評価者の Astra が被験モデルも兼ねるという方法上の問題を研究者自身が認めている。
- **なぜ重要か**: フィジカル AI 向けのデータ処理を、オープンな小型モデルで置き換える流れの一例。ベンチマークの評価方法には注意が要る。
- 出典: [The Decoder](https://the-decoder.com/nvidia-open-sources-flora-to-make-robot-video-labeling-125x-cheaper-than-gpt-6-astra/)

### [2026-10-26] The RealReal、Meta Muse などの AI ショッピングエージェントによる「在庫ホールド」を受けてボット対策を強化
- **何が起きたか**: The Verge は以前、Meta Muse にカートの 20 分ホールドを繰り返させると、商品を何時間も他の客が買えない状態にできると報じた。これを受けて The RealReal の CTO は、すべてのエージェントについてログイン・カート追加・決済を難しくし、検索と商品案内だけを許すと説明した。
- **なぜ重要か**: エージェントによるビジネスロジックの悪用 (在庫ホールドによる DoS) が、実際のサービスで対策を迫った例。Web アプリの診断では、予約・ホールド・在庫確保の機能について「自動化されたエージェントが大量に叩く」前提でレート制限や上限を確認したい。
- 出典: [The Verge](https://www.theverge.com/news/1018713/meta-muse-agentic-shopping-ai-the-realreal)

### [2026-10-26] トヨタ、ヒューマノイドと工場自動化に年 64 億ドル、ロボット 40 万台の導入計画 (FT 報道)
- **何が起きたか**: FT によると、トヨタは年 64 億ドルの投資計画の中で 40 万台のロボットを導入し、まず自社工場に入れる。7 月には AI ロボティクスのスピンアウト Walden Robotics が上場している。
- **なぜ重要か**: 国内の大手製造業がフィジカル AI に大きく投資する。工場のロボットやその AI 制御系が、OT 診断の新しい対象として増える。
- 出典: [The Decoder](https://the-decoder.com/toyota-is-betting-6-4-billion-a-year-on-humanoid-robots-and-factory-automation/)

### [2026-10-26] NYU と UT Austin の研究: フロンティア LLM の文章を読みにくくする 6 つの言語パターン
- **何が起きたか**: 14 モデル (Claude、GPT-5.6、GLM-5、Kimi K2.5、Llama、Olmo など) の会話 120 件、コーディングセッション 45 件、エッセイ 980 件を人間の文章と比べ、珍しい語の組み合わせ、主語と述語の距離、名詞の積み重ね、名詞の動詞化などの 6 パターンを多用すると示した。Olmo の比較から、事後学習 (post-training) が原因と推定している。
- **なぜ重要か**: 実務への影響は小さいが、AI に書かせた診断報告書の読みやすさをチェックする観点として使える。
- 出典: [The Decoder](https://the-decoder.com/researchers-find-six-patterns-that-make-ai-text-so-exhausting-to-read/)

### [2026-10-26] 【国内】チームみらい安野氏、「AI 失業」対策の提言を木原官房長官に手渡す
- **何が起きたか**: チームみらいの安野貴博党首らが 10/26、AI の社会実装で仕事がどう変わり、人がそれに適応できているかを調査し、支援が行き渡る仕組みを整えるよう求める提言を木原稔官房長官に手渡した。同党は 10/23 に、AI 悪用のサイバー攻撃に関する緊急提言をデジタル庁にも出している。
- **なぜ重要か**: 国内の AI 政策の論点が、セキュリティから雇用にも広がっている。
- 出典: [ITmedia AI+](https://www.itmedia.co.jp/aiplus/article/2610/26/2000002581/)

### [2026-10-26] 【国内】Dataiku Japan、他社のエージェント基盤も束ねて管理する「Agent Management」を国内で説明
- **何が起きたか**: ITmedia の考察記事によると、Dataiku Agent Management は AWS Bedrock、Databricks Agents、Google Vertex、Copilot Studio、Azure Foundry、Salesforce Agentforce、Snowflake Cortex などにつなぎ、エージェントのスキャン・コスト監視・リスクスコア・アラートを一元化するという。記事は、ガードレールやセキュリティの強度まで一元化できるかには限界があると論じている。
- **なぜ重要か**: 国内企業で、複数ベンダーにまたがるエージェントの棚卸し (シャドーエージェント対策) への関心が高まっている。診断や監査で、エージェント台帳づくりの需要につながる。
- 出典: [ITmedia エンタープライズ](https://www.itmedia.co.jp/enterprise/articles/2610/26/news060.html)

## AI セキュリティ

### [2026-10-26] OpenHands Software Agent SDK に未認証 RCE (CVE-2026-112346、CVSS v3.1 9.8 / v4 9.3)。サンドボックスのエージェントサーバーが 0.0.0.0・認証なしで起動
- **何が起きたか**: 1.52.0 より前の OpenHands Software Agent SDK では、DockerWorkspace と Apptainer の workspace launcher がサンドボックスのエージェントサーバーを 0.0.0.0 に bind し、`session_api_keys` が空 (認証無効) のまま起動していた。公開されたコンテナのポートに届けば、未認証の HTTP / WebSocket リクエストでサンドボックス内で root として任意のコマンドを実行でき、マウントされた workspace の読み書きと secrets store の平文の秘密の読み取りもできる (CWE-1327)。報告者は VulnCheck の mil4n 氏、1.52.0 で修正。
- **なぜ重要か**: コーディングエージェントの「隔離のための仕組み」そのものが、ネットワークに露出した未認証 RCE になっていた。クラウドの VM や共有の開発ホストで動かしている場合、ポートスキャンだけで見つかる。他のエージェント SDK や Code Interpreter 系でも、同じ「全インターフェースで待ち受け・既定で無認証」を確認する価値がある。公開 PoC と悪用の報告はないが、修正コミットから再現は容易とみられる (評価)。
- 出典: [VulnCheck](https://www.vulncheck.com/advisories/openhands-software-agent-sdk-unauthenticated-sandbox-agent-server-rce) / [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-112346)

### [2026-10-26] Google 公式の MCP 実装に 2 件: MCP Toolbox for Databases の未認証ファイル持ち出し (CVE-2026-93328、v4 9.3) と、Cloud Run MCP の bucket squatting (CVE-2026-85297、v4 7.7)
- **何が起きたか**: googleapis/mcp-toolbox 1.2.0〜1.4.0 の cloud-storage source では、ツール呼び出しのパラメータに認可チェックもパスの検証もなく、未認証の攻撃者がホストのファイルを外部の GCS バケットへ持ち出したり、任意のローカルファイルを上書きしたりできる (CWE-22 / CWE-862、修正は PR #3454)。Cloud Run MCP の 1.11.0 より前には、予測可能なバケット名を攻撃者が先に取得することで、ソースコードの取得・任意コード実行・データの持ち出しにつながる問題がある (CWE-340、1.11.0 で修正)。
- **なぜ重要か**: クラウドベンダー公式の MCP サーバーでも、「ツールの引数がそのままファイルパスの sink に届く」型が出た。10/25 号の SiYuan・designer-mcp に続く同型で、MCP のストレージ系ツールは診断で優先して見る対象になった。エージェント経由で呼ぶ構成では、プロンプトインジェクションから同じパラメータを渡せる可能性がある (評価)。
- 出典: [NVD CVE-2026-93328](https://nvd.nist.gov/vuln/detail/CVE-2026-93328) / [NVD CVE-2026-85297](https://nvd.nist.gov/vuln/detail/CVE-2026-85297) / [mcp-toolbox PR #3454](https://github.com/googleapis/mcp-toolbox/pull/3454) / [cloud-run-mcp v1.11.0](https://github.com/GoogleCloudPlatform/cloud-run-mcp/releases/tag/v1.11.0)

### [2026-10-26] vLLM 0.32.0 で新たに 8 件の CVE。マルチモーダル共有メモリ経由の pickle RCE (CVE-2026-115912) と、EPS → Ghostscript の連鎖 (CVE-2026-115915)
- **何が起きたか**: 10/25 号で扱った VulnCheck 採番の 10 件とは別に、GitHub CNA が vLLM の 8 件を採番した (いずれも 0.32.0 で修正)。
  - CVE-2026-115912 (7.5): 認証済みの呼び出し側が `features.kwargs_data` に偽の共有メモリアドレスと `monotonic_id` を入れると、スケールアウト構成で共有メモリのマルチモーダルキャッシュが有効な場合、worker が攻撃者の選んだバイト列を `pickle.loads()` に渡す。insecure serialization を無効にしていても任意の Python コードが実行される。
  - CVE-2026-115915 (8.1): `ImageMediaIO` が Pillow のデコーダを制限しないため、EPS を送り込める。ホストに CVE-2024-29510 の影響を受ける Ghostscript があればコマンド実行に至る。
  - CVE-2026-115917 (3.4): OpenAI 互換サーバーの CORS が既定でワイルドカード。悪意のある Web ページから、被害者のブラウザ経由で localhost や社内の未認証 vLLM を呼び、応答を読める。
  - ほかに Jinja のチャットテンプレートの描画に上限がない DoS 2 件 (CVE-2026-115911 / 115918。115918 は `trust_request_chat_template` を迂回)、音声・OCR・トークン ID 処理の DoS 3 件。
- **なぜ重要か**: 推論サーバーは「認証済みでもテナントの利用者は信頼できない」前提で作る必要があることを示す RCE 級の欠陥。CORS のワイルドカードは、社内や開発者の手元の vLLM を外部の Web ページから使わせる経路になり、診断ですぐ確認できる。
- 出典: [NVD CVE-2026-115912](https://nvd.nist.gov/vuln/detail/CVE-2026-115912) / [NVD CVE-2026-115915](https://nvd.nist.gov/vuln/detail/CVE-2026-115915) / [NVD CVE-2026-115917](https://nvd.nist.gov/vuln/detail/CVE-2026-115917) / [vLLM v0.32.0](https://github.com/vllm-project/vllm/releases/tag/v0.32.0) / [GHSA-6757-hggm-hp2w](https://github.com/vllm-project/vllm/security/advisories/GHSA-6757-hggm-hp2w)

### [2026-10-26] Xint「Compaction Smuggling」: OpenAI API の会話圧縮 (compaction) を使い、暗号化された推論トレースを平文で抜き出す
- **何が起きたか**: Xint は 3 回の API 呼び出しで推論トレースを取り出す手法を公表した。(1) gpt-5.6-sol にタスクを送り、暗号化された reasoning item を受け取る。(2) 元のタスクを履歴から消し、`/responses/compact` に「推論を逐語で保存せよ」という instructions を渡して compaction を作らせる (空白をタブにするなどでフィルタを回避)。(3) その compaction を gpt-4.1 / gpt-4o などに渡し「入力をそのまま出力せよ」と指示する。8 月に OpenAI が入れた対策は「推論を別モデルにリプレイすること」を防ぐものだったが、compaction は同じモデルで動くため回避できた。OpenAI は問題を認めて 10/23 に修正し、Xint は 6,000 ドルの報奨金を得た。
- **なぜ重要か**: API が返す「暗号化された不透明な状態オブジェクト」をクライアントが操作できると、機密性の境界が破れる。LLM API の診断で一般化できる観点 (状態オブジェクトを別の文脈に持ち込む) になる。蒸留の経路として、上の S-1 の「売上の 5〜7% が蒸留目的の規約違反」とも直結する。
- 出典: [Xint](https://xint.io/blog/compaction-smuggling-reasoning-traces) / [SecurityWeek](https://www.securityweek.com/stolen-ai-reasoning-could-help-china-build-cheaper-rivals/)

### [2026-10-26] 英政府、AI によるサイバー防御に 1 億 3,000 万ポンド。エージェント型の「National Cyber Shield」と脆弱性探索の「NERV Centre」
- **何が起きたか**: 英財務省が 6 億ポンド超の AI 投資パッケージを発表した。サイバー関連は、National Cyber Shield (6,000 万ポンド。重要インフラで自律型セキュリティツールを試す規制サンドボックスと、英国企業向けのチャレンジファンド 2,500 万ポンドを含む) と、AI で国内の脆弱性を探す National Exposure and Real-Time Vulnerability (NERV) Centre (7,000 万ポンド)。AISI には 1 億 2,000 万ポンドを追加する。AI 担当大臣は、AI による脆弱性探索で公共部門から未知の欠陥 500 件を見つけたと述べた。
- **なぜ重要か**: 国家として「AI エージェントで脆弱性を探して塞ぐ」ことを制度化する動き。下の国内の緊急対策パッケージ (来週中にまとめる予定) と比べる材料になる。
- 出典: [The Register](https://www.theregister.com/security/2026/10/26/britain-bets-big-on-ai-to-defend-against-the-threats-ai-is-helping-create/5305319)

### [2026-10-26] Continue の MCP 設定経由の OS コマンドインジェクション (CVE-2026-116109) と、AI コールセンター製品のハードコードされた API キー (CVE-2026-110474)
- **何が起きたか**: VulDB の登録によると、continuedev Continue 2.0.0 の `core/config/ConfigHandler.ts` (`MCPManagerSingleton.setConnections`) に OS コマンドインジェクションがある (CVSS v3.1 6.3、UI:R)。exploit は公開済みで、ベンダーは連絡に応答しなかったという。CreditNirvana の「Agentic AI Call Centre」は静的な API キーをクライアント側の JS バンドルにハードコードしており、未認証で通話の文字起こしと録音を取得できた (CVSS v4 8.7、CERT-In CIVN-2026-0523)。
- **なぜ重要か**: 前者は「コーディングエージェントの MCP 設定 (リポジトリ内の設定ファイル) がそのままコマンド実行の経路になる」よくある型で、修正版がない。後者は AI 製品にも基本的なクライアント側の秘密の露出が残っている例で、JS バンドルの grep で見つかる。
- 出典: [NVD CVE-2026-116109](https://nvd.nist.gov/vuln/detail/CVE-2026-116109) / [VulDB](https://vuldb.com/vuln/426177) / [NVD CVE-2026-110474](https://nvd.nist.gov/vuln/detail/CVE-2026-110474)

## セキュリティニュース

### [2026-10-24〜26] CISA KEV: この期間の追加はなし。10/23 追加の 2 件は対応期限 (10/26) を過ぎた
- **何が起きたか**: 公式フィードと GitHub ミラーの両方で確認したところ、catalogVersion は 2026.10.23 のままで、dateAdded が 10/24 以降のエントリはない。10/23 に追加された Arista VeloCloud Orchestrator の SQLi (CVE-2026-114625) と Collabora Online の OS コマンドインジェクション (CVE-2026-110447) は、連邦機関の対応期限 (dueDate) が 10/26 で、すでに過ぎた。PHP2Shell (CVE-2026-109618 / 109619) と Brotli (CVE-2026-111497) はまだ KEV に入っていない。
- **なぜ重要か**: 下の PHP2Shell のハニーポットでの RCE 成立を受けて、KEV への追加は近いとみられる (評価)。顧客への報告で「KEV 未登録」を安全の根拠にしないこと。
- 出典: [CISA KEV JSON](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json) / [cisagov/kev-data](https://raw.githubusercontent.com/cisagov/kev-data/main/known_exploited_vulnerabilities.json)

### [2026-10-26] [続報] PHP2Shell: ハニーポットで公開 PoC と同じ手順の RCE が初めて具体的に記録された。メモリ漏えい → シェル実行の 4 段チェーン
- **前回から何が変わったか**: 10/25 号の Unit 42 の侵害事例に加え、第三者のハニーポットで RCE の成立が詳細に記録された。
- **何が起きたか**: Perplexity の Adel Karimi 氏は、PHP 8.4.26 + Apache mod_php + ワーカー 1 つのハニーポット 3 台で、10/24 に計 35 回シェルが起動したのを記録した (1 つの IP が 1 台で 3 回、別の IP が 3 台すべてで 32 回)。攻撃は 4 段の HTTP リクエストの連鎖 (メモリを使い切らせる → メモリ内容を漏らす → コマンド実行) で、応答としてデコード後 800 KiB の cookie ダンプが返り、公開 exploit のオフセットで計算した関数アドレスが次のペイロードに入っていた。コマンドは wget / curl / PHP CLI で 162.35.99[.]94:80 から追加のペイロードを取りに行くものだった。Expel の Marcus Hutchins 氏は「これまで見た中で最も質の高い野良悪用の確認」と評価した。Karimi 氏自身は、攻撃に有利な単一ワーカー構成での結果であり、他の構成での成功率を示すものではないと注記している。
- **なぜ重要か**: 公開 PoC がそのまま実戦で通ることを示した初の高品質な証拠。mod_php + prefork / 少ワーカーの古い構成は、診断で見つけたら優先度を最大にすべき。**悪用: 観測あり (ハニーポットで RCE 成立)、PoC: 公開済み、KEV: 未登録**。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/php2shell-security-flaws-now-sucessfully-exploited-in-the-wild/) / [SecurityWeek](https://www.securityweek.com/php2shell-exploitation-moves-from-probes-to-working-shells/)

### [2026-10-26] [続報] PHP2Shell が OT 製品に波及: Schneider・Siemens・ABB/B&R・Belden などが影響製品を公表
- **前回から何が変わったか**: 10/24〜25 は PAN-OS への影響が中心だったが、産業機器ベンダー各社の判定が出そろい始めた。
- **何が起きたか**: SecurityWeek のまとめによると、影響ありとしたのは Schneider Electric (EcoStruxure Security Expert は 1.48.4.0 で修正、ProLeiT LINEoptimize、EcoStruxure Control Engineering は緩和策のみ)、Siemens (PAN-OS 10.2〜12.2 を載せた Ruggedcom APE1808)、ABB (MES 同梱の DokuWiki、B&R APROL は R 4.4-65 まで影響で修正は 10/26・10/29 予定)、Belden (NetModule NRSW は全版が影響で修正なし、暫定策は Web UI の無効化。macmon 7.x は修正あり)。Johnson Controls・HMS・Wibu-Systems は修正を公開、Rockwell と Hitachi Energy は調査中、Moxa は影響なし。
- **なぜ重要か**: OT 機器の Web 管理画面に組み込まれた PHP は、パッチの適用が遅れやすい。OT / IoT の診断では、管理 UI のバックエンドが PHP かどうかを確認する項目を加えたい。**悪用: OT 製品での報告なし、PoC: 公開済み**。
- 出典: [SecurityWeek](https://www.securityweek.com/industrial-vendors-check-products-for-php2shell-vulnerabilities/)

### [2026-10-26] [続報] Brotli (CVE-2026-111497): Microsoft の .NET / VS / PowerShell 定例外パッチと、PHP の Windows 公式ビルドの再ビルド (→ 今日の深掘り)
- **前回から何が変わったか**: 10/25 号の Bun・Python・Envoy・Istio に続き、.NET と PHP (Windows) が加わった。
- **何が起きたか**: Microsoft が 10/25 に .NET 8.0.33 / 9.0.22 / 10.0.14 などの定例外更新を出した (CVSS v3.1 8.1、Exploitation More Likely、到達経路は既定では無効な 3 つ)。PHP は Windows 版 8.2〜8.5 を Brotli 1.2.1 で作り直した (`php -v` の表示は変わらない)。THN の確認では、Guzzle は cURL 経由のリクエストで `CURLOPT_ENCODING` を空文字に設定しており、外部 URL の取得で到達しうる。
- **なぜ重要か**: 詳細は深掘りを参照。**悪用: 報告なし、PoC: 公開済み (弱めたビルドでのみ RCE)、KEV: 未登録**。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-releases-emergency-net-patches-for-critical-brotli-flaw/) / [The Hacker News](https://thehackernews.com/2026/10/php-issues-second-windows-security.html)

### [2026-10-26] GitHub Actions の Pwn Request は 2026 年の対策後もまだ通る: 古い SHA へのピン留め、issue_comment、スクリプトインジェクションの抜け道 (Wiz Research, "Pwn Request Reckoning")
- **何が起きたか**: Wiz は、GitHub が 2026 年に入れた対策 (actions/checkout のフォーク PR 保護、キャッシュトークンの読み取り専用化、12/2 に強制適用する pull_request_target の既定無効化) を検証し、残る抜け道を示した。
  1. 保護は actions/checkout の中に実装されているため、7/20 の backport より前の SHA (例: v4.3.0) に固定すると効かない。v2.8.0 / v3.7.0 / v4.4.0 / v5.1.0 / v6.1.0 / v7.0.0 以上が必要。
  2. `git clone`、`gh pr checkout`、サードパーティの checkout アクションで取得すると保護を通らない。
  3. 保護対象は pull_request_target と workflow_run だけで、issue_comment (`/deploy` 型のボットコマンド) と repository_dispatch は対象外。
  4. `${{ github.event.pull_request.title }}` を run に直接埋め込むスクリプトインジェクションは、checkout がなくても成立する。
  5. 12/2 の既定ポリシーは、プライベート・内部リポジトリと workflow_run には適用されない。
- **なぜ重要か**: 「アクションは SHA でピン留めすべき」という定石が、逆に保護を外してしまうという具体的で検証可能な指摘。昨日深掘りした Gheist と合わせ、CI/CD 診断のチェックリストを今週中に更新する価値がある。**悪用: 特定事例の観測ではなく研究 (YAML の例を掲載)**。
- 出典: [Wiz Blog](https://www.wiz.io/blog/github-actions-security-pwn-request-reckoning)

### [2026-10-26] Magento などの EC サイト 953 件に、スキャナーを避ける JavaScript ローダー。PolyShell / SessionReaper 経由で `cms_block` に仕込む (Sansec)
- **何が起きたか**: Sansec によると、2025 年 7 月から続くキャンペーンで EC サイト 953 件 (大半が Magento) が感染した。ローダーは Magento の `cms_block` テーブルに置かれ、ページ表示のたびに外部の JS を読み込む。新しい版はブラウザのフィンガープリントでスキャナーと bot を除外し、localStorage に保存して読み込み先が止まっても再実行する。初期侵入は、471 店舗が PolyShell (CVE-2026-48356)、102 店舗が PolyShell または SessionReaper (CVE-2025-54236、KEV 登録済み) 経由。パッチをすべて当てた 2.4.7-p10 でも 1 件、不正な管理者アカウントの追加による感染があった (経路不明)。読み込み先の deepveindrilling[.]com は 10/6 の登録以降 83 店舗で見つかっている。
- **なぜ重要か**: スキャナーには何も返さないので、外部からの Web スキャンでは見つからない。侵害調査では DB の `cms_block` / `cms_page` と管理者アカウントを直接確認する必要がある。**悪用: 観測あり (953 件)**。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/hackers-infect-953-online-stores-with.html) / [SecurityWeek](https://www.securityweek.com/953-online-stores-infected-in-long-lasting-malware-campaign/)

### [2026-10-26] Microsoft Teams の外部チャットで「IT サポート」を名乗る攻撃。数百件に共通する手順 (Arctic Wolf)
- **何が起きたか**: Arctic Wolf は数百件の事例を分析し、メール爆撃 → 使い捨ての M365 テナント (30〜40% は *.onmicrosoft.com) から「IT Service Desk」を名乗って Teams で接触 → Quick Assist / AnyDesk / ScreenConnect などで操作を奪取 → GoGRPC バックドアや Python インプラントを入れて LDAP で AD を列挙 → 持ち出しとランサムウェア展開、という共通の流れを示した。Safe Links / ZAP を避けるため、URL を Teams に貼らずリモート操作の中でペイロードを取りに行く。Sophos は STAC4749 との一致と Chaos ランサムウェアの展開を指摘している。
- **なぜ重要か**: 脆弱性ではなく、Teams の外部アクセス設定がそのまま攻撃面になる。レッドチームやソーシャルエンジニアリング評価で再現しやすく、テナント設定の診断では外部アクセスの許可ドメイン制限と RMM ツールの許可リストを確認したい。**悪用: 観測あり (ランサムウェア展開まで)**。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/attackers-use-microsoft-teams-it.html)

### [2026-10-26] Fortinet、AI で見つけた Critical / High の脆弱性を FortiOS などで修正。詳細は 11/10 まで非公開
- **何が起きたか**: Fortinet は先週、FortiOS / FortiManager / FortiAnalyzer (8.0 / 7.6 / 7.4 / 7.2)、FortiMail (8.0 / 7.6 / 7.4)、FortiAuthenticator に「セキュリティ強化アップデート」を出した。修正した Critical / High の脆弱性の詳細は 11/10 に公表する。CISO の Carl Windsor 氏は、AI モデルで見つけて人が検証した、30 製品ファミリーに 100 以上のテストを行い検出の約 40% が本物だった、AI はファームウェアの差分比較と修正済み脆弱性の PoC 作成が得意、と説明した。これらの製品は PHP2Shell の影響を受けないという。
- **なぜ重要か**: 修正版の公開から詳細の公表まで約 2 週間の空白がある。Fortinet 自身が「AI によるパッチ差分解析で exploit がすぐ作られうる」と述べている以上、攻撃者が先に差分を読むリスクがある。FortiGate は悪用の多い製品なので、11/10 を待たずに更新を勧めたい (評価)。**悪用・PoC: 報告なし**。
- 出典: [Help Net Security](https://www.helpnetsecurity.com/2026/10/26/fortinet-patches-critical-fortios-flaws-found-with-ai-help/)

### [2026-10-26] CERT-UA: Dahua 製カメラ・レコーダーへの不正アクセス。Easy4IP のシリアル番号が推測可能で、CVE-2021-33044 / 33045 も悪用
- **何が起きたか**: CERT-UA によると、Dahua 製のカメラ・NVR が侵害され、設定の変更と不正アカウントの作成が行われた (台数・時期・攻撃者は非公表)。経路はクラウド経由のリモートアクセス機能 Easy4IP で、シリアル番号の規則が予測しやすいためファイアウォールの内側の機器も列挙される。侵入手段は弱い / 既定のパスワードか、旧ファームウェアの認証回避 (CVE-2021-33044 / 33045)。Hunt.io は 8 月に夏の間の 14,500 台超の侵害を報告しており、不正アカウントや復旧コードはパスワード変更や工場出荷リセット後も残るとしていた。
- **なぜ重要か**: P2P / クラウド中継型の機器列挙は境界防御を素通りする。IoT 診断では、クラウド中継機能の有効・無効と、リセット後も残るアカウントの確認を加えたい。**悪用: 観測あり、CVE-2021-33044 / 33045 は 2024-08 に KEV 登録済み**。
- 出典: [The Record](https://therecord.media/ukraine-cert-ua-warning-chinese-dahua-cameras-hacked)

### [2026-10-26] DreamHost、続いているインシデントでメール / FTP / SFTP のパスワードを強制リセット
- **何が起きたか**: 米ホスティング事業者 DreamHost (顧客 40 万超、サイト 150 万超) は、10/23 に File Manager の接続障害を報告した後、全ユーザーのログインを止めてパスワードを強制リセットし、週末に復旧手順を送った。File Manager はまだ使えない。通知では、メールの転送ルールを点検し、知らない転送先を削除するよう求めている。原因・影響範囲・データ流出の有無は説明していない。
- **なぜ重要か (評価)**: 転送ルールの点検を求めていることから、メールアカウントの乗っ取りが疑われる。共有ホスティングの FTP 資格情報は Web 改ざん (上の Magento のような注入を含む) に直結する。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/dreamhost-forces-email-ftp-sftp-password-resets-in-ongoing-incident/)

### [2026-10-26] Genesys、社内の LMS と CRM への不正アクセスで顧客の連絡先が流出。ScarlettGroup が犯行を主張
- **何が起きたか**: コンタクトセンター基盤の Genesys は、10/19 に社内の学習管理システム (LMS) と CRM への侵入を公表し、10/23 に封じ込めの完了を宣言した。流出した可能性があるのは、顧客・見込み客の氏名、電話番号、業務用メール、役職、取引情報。Genesys Cloud / Engage の基盤と顧客データには影響がないと同社は主張している。新しいグループ ScarlettGroup がリークサイトで犯行を主張した。
- **なぜ重要か**: 流出した CRM データは、Genesys の顧客企業を狙う標的型フィッシングやビッシングの材料になる。Genesys を名乗る問い合わせには注意。
- 出典: [SecurityWeek](https://www.securityweek.com/genesys-hack-exposes-customer-data-from-internal-systems/)

### [2026-10-26] Android スパイウェアのキット「uCreator」: 改ざんした Telegram / WeChat に入り込み、2FA パスワードを盗み、アカウントを複製
- **何が起きたか**: 研究者の Ovi 氏の分析 (THN が 10/26 に報道) によると、レンタル型の uCreator は、正常に動く Telegram X / WeChat の改ざん版にコードを埋め込み、アプリ自身の権限でメッセージ DB への任意クエリ、Telegram の 2FA パスワードの窃取、WeChat アカウントの複製を行う。Telegram 向けの部分は、Doctor Web が 2025 年 10 月に報告した Baohuo (約 5.8 万台感染) と名前空間・C2・コマンド名が一致する。配布はサイドロード、APKPure などのサードパーティストア、独自のコンテナアプリ。
- **なぜ重要か**: 正規アプリと同じパッケージ名で配布されるので、パッケージ名だけでは見分けられない。モバイルの調査では署名証明書の照合が必須。**悪用: 実際の配布・感染を観測**。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/ucreator-android-spyware-can-steal.html)

### [2026-10-26] Kali Linux 2026.3 リリース: カーネル 7.1.5、ビルドスクリプトの全面改修、新ツール 6 件 (dalfox, katana, qsreplace, rustscan, sdrangel, snaffler-ng)
- **何が起きたか**: 公式イメージのビルドスクリプトを全面的に作り直し、Docker / Podman を自動判別する `build-in-container.sh` を追加した。126 パッケージを更新し、カーネルは 6.19 → 7.1.5、KDE Plasma は 6.7。NetHunter は TicWatch Pro 3 での wardriving と、NFC での Mifare Classic の読み取り・複製に対応した。
- **なぜ重要か**: 診断環境に直結する。dalfox (XSS)、katana (クローラ)、snaffler-ng (SMB 共有の資格情報探索) が標準リポジトリから入る。イメージを自前でビルドしている CI は、古いスクリプト前提のパイプラインが壊れないか確認したい。
- 出典: [Help Net Security](https://www.helpnetsecurity.com/2026/10/26/kali-linux-2026-3-released/) / [BleepingComputer](https://www.bleepingcomputer.com/news/linux/kali-linux-20263-released-with-6-new-tools-desktop-updates/)

### [2026-10-26] 法執行: オランダで NFC リレー詐欺の 2 人を逮捕 (170 人から 38 万ユーロ)。投資詐欺の資金洗浄に関わった中国籍の男をオランダから米国へ引き渡し
- **何が起きたか**: オランダ警察は 10/6 に 23 歳と 25 歳の男を逮捕し、サーバーを押収したと発表した。AI で生成した音声で銀行を名乗って電話し、アプリを入れさせてカードをスマホにかざさせ、読み取った NFC データを ATM の共犯者にリレーして現金を引き出す手口で、被害は 170 人・38 万ユーロ超。別件で、米国の 174 人から約 3,690 万ドルをだまし取った暗号資産投資詐欺の資金洗浄に関わったとして、中国籍の Zhen Zhao (44) がオランダからカリフォルニアへ引き渡された。
- **なぜ重要か**: NFC リレー (NGate 系) が AI 音声のビッシングと組み合わさり、組織的な詐欺として運用されている実例。
- 出典: [SecurityWeek](https://www.securityweek.com/dutch-police-arrest-two-over-nfc-relay-attacks-that-drained-400000/) / [BleepingComputer](https://www.bleepingcomputer.com/news/security/chinese-man-extradited-for-role-in-36-million-cryptocurrency-scam/) / [The Record](https://therecord.media/dutch-police-extradite-chinese-national-money-laundering-scams)

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 today-2 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先
> 母集団: NVD API 2.0 で pubStartDate 2026-10-24T15:00Z〜2026-10-26T20:00Z の 487 件から既出 25 件を除いて選定。公開日はすべて NVD の `published` で確認。KEV は catalog 2026.10.23 で照合し、下表に該当なし。EPSS は公開直後のため、値が返ったのは CVE-2026-116199 のみ。

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-115905 (GHSA-m665-v7pm-7grj) | Rust `zip` (zip2) ≤ 9.0.4 | CWE-20, CWE-436 / v4 10.0 | Central Directory と Local File Header でファイル名が食い違う ZIP → 検査側 `ZipArchive` は CD の名前、書き出す `ZipStreamReader` は LFH の名前を使う → 検査を通したまま別パス・別内容のファイルを書き込める | [diff](https://github.com/zip-rs/zip2/commit/8068ab480ccf8daa7411424e365fcdbe6d09443e) | CVSS 10.0。**水平伝播: 最有力** (CD/LFH 二重メタデータは仕様由来。Go archive/zip、Python zipfile、Java ZipFile/ZipInputStream、adm-zip で同型を確認する価値)。同日 symlink 連鎖による展開先脱出 CVE-2026-115908 (v3.1 7.4) も |
| CVE-2026-114216 (GHSA-w5wc-g2hc-g7m2) | Elixir `bandit` 1.12.4〜<1.14.0 | CWE-444 / v4 6.3 | chunk-size 行の chunk-ext を RFC 9112 の文法で検証せず bare LF / CR を通す → 前段プロキシと行区切りの解釈がずれる → 2 本目のリクエスト密輸 (例: GET /admin) | [diff](https://github.com/mtrudel/bandit/commit/220b9dfd27f9a21305be2afc75cbe585ddc24e7a) | **水平伝播: 高** (HTTP/1.1 チャンク行の解釈差。同日 Starman でも bare LF 起因の ReDoS CVE-2026-115822)。同コミットで HTTP/2 DoS 群 (v4 8.7) も修正 |
| CVE-2026-115700 | Erlang `hackney` 4.0.1〜<4.9.0 | CWE-436, CWE-918 / v4 6.9 | `%5B%3A%3Affff%3A127%2E0%2E0%2E1%5D` や `127.0.0.1.` を渡す → 呼び出し側の許可リスト判定 (uri_string / inet:parse_address) は IP と見なさず、hackney は実アドレスへ接続 → SSRF ガード回避 (CVE-2026-47076 の不完全修正) | [diff](https://github.com/benoitc/hackney/commit/452620a92ec1da2e6b4862a049a2a4f04b42068f) | **水平伝播: 高** (検証側と接続側の URL パーサー差。全言語の SSRF ガードに共通)。不完全修正の再発 |
| CVE-2026-113440 | `hackney` 2.0.0〜<4.9.0 | CWE-522 / v4 6.0 | follow_redirect 有効時、`maybe_strip_auth_on_redirect` がホスト名だけを比較 → 同一ホストの https→http や別ポートへのリダイレクトで Authorization / Cookie を再送 → 資格情報漏えい | [diff](https://github.com/benoitc/hackney/commit/6548384b22ea196023a1963e2967d5715b6d9564) | **水平伝播: 高** (curl / requests / Go でも過去に CVE 化した定番。自作 HTTP クライアントで頻出) |
| CVE-2026-116539 (GHSA-gf9q-9mg7-g5qh) | Netty `netty-tcnative` < 2.0.84.Final | CWE-787 / v4 8.2 (v3.1 5.9) | TLS ピアがハンドシェイク / 再ネゴシエーションのメッセージを送り続ける → `tcn_write_to_bytebuffer` の BIO コールバックがリングバッファの書き込み位置を巻き戻さない → ヒープ範囲外 memcpy で JVM クラッシュ | [diff](https://github.com/netty/netty-tcnative/commit/92dd66fd1243d85c05a61288f96367a70260b6b8) | 認証前・TLS 層で到達。同時公開の CVE-2026-116542 (JNI `NewStringUTF` が SNI の modified UTF-8 を変換) は他の JNI ラッパーにも水平展開しうる。UAF の CVE-2026-116540 も |
| CVE-2026-116543 (GHSA-25v2-v588-jq8g) | Open5GS 1.3.0〜2.8.0 | CWE-787 / v4 8.7 (v3.1 7.5) | SBI の multipart/related で boundary を空にする → `parse_multipart()` の lookbehind バッファへヒープ範囲外書き込み → 未認証で任意の NF をクラッシュ | [diff](https://github.com/open5gs/open5gs/commit/6820c2743b5b5e126e3755d2f92dae2b236732df) | **水平伝播: 中〜高** (コピーされがちな C 製 `multipart_parser.c`。free5GC など他の 5GC 実装も)。SUCI 処理の OOB read CVE-2026-116544 も同時 |
| CVE-2026-112346 | OpenHands Software Agent SDK < 1.52.0 | CWE-1327 / v4 9.3 (v3.1 9.8) | Docker / Apptainer workspace がエージェントサーバーを 0.0.0.0 に bind し `session_api_keys` 空 (認証なし) で起動 → 公開ポートへ未認証 HTTP / WebSocket → サンドボックス内で root 任意コマンド・secrets 読み取り | [diff](https://github.com/OpenHands/software-agent-sdk/commit/7b66584ff8899144eb4ce679c2811861342af9de) | CVSS 9.8。**水平伝播: 高** (エージェント SDK / Code Interpreter 系の「全 IF で待ち受け・既定無認証」)。ポートスキャンで確認可 |
| CVE-2026-102649 (GHSA-7m68-72r6-3jx8) | padok-team Burrito (Terraform K8s operator) < 0.13.0 | CWE-306, CWE-863 / v3.1 9.9 | `webhookSecret` 未設定・空 → `go-playground/webhooks` が署名検証をスキップ → `POST /api/webhook` に偽の GitHub / GitLab イベント → TerraformPullRequest の作成・削除、保存済み資格情報で `terraform plan` 実行 | [diff](https://github.com/padok-team/burrito/commit/1d48432a4a0126429c99f5fa42567bf3711d1ca1) | CVSS 9.9。**水平伝播: 高 (共通 sink)**。同ライブラリを使い secret を任意設定にしている Go 製 CI/CD・GitOps 製品で同型の可能性 |
| CVE-2026-115910 (GHSA-h2r5-x5m7-3935) | python-social-auth `social-core` < 6.2.0 | CWE-345, CWE-384 / v3.1 6.8 | OIDC nonce を共有テーブルで「存在して期限内か」だけ確認しブラウザセッション / state に束縛しない + PKCE 既定無効 → 被害者の未使用の認可コードを攻撃者の state と組み合わせて送る → ログイン成立・アカウント乗っ取り | [diff](https://github.com/python-social-auth/social-core/commit/c2f2ae4663bef19ee8b07f2cf5a2344f9155d826) | **水平伝播: 高 (プロトコル仕様起因)**。他の OIDC RP ライブラリ・自前 SSO で同じ観点を確認可 |
| CVE-2026-115915 (GHSA-h3rc-j82p-2c3h) | vLLM < 0.32.0 | CWE-20, CWE-183 / v3.1 8.1 | 攻撃者の画像バイト列をデコーダ制限なしで `PIL.Image.open(BytesIO)` に渡し MIME ラベルでも形式を縛らない → EPS が Ghostscript (CVE-2024-29510) に届く → RCE | [diff](https://github.com/vllm-project/vllm/commit/710ac56e691d4713feca50a43e6c440f07d373fd) | **水平伝播: 高 (共通 sink)**。`Image.open` を `formats=` 指定なしで呼ぶ箇所はマルチモーダル推論・画像アップロード処理に多い。10/25 既出の vLLM 一括とは別群 |
| CVE-2026-116199 (GHSA-xf36-wx48-5rqp) | Snipe-IT < 8.6.3 | CWE-285 / v4 9.2 (v3.1 8.1) | Google SSO コールバック `handleGoogleCallback` がメールとユーザー名の一致だけでログインさせ `activated` フラグを確認しない → 無効化された管理者でも Google アカウントが生きていればセッション取得 | [advisory](https://github.com/grokability/snipe-it/security/advisories/GHSA-xf36-wx48-5rqp) (commit 不明) | EPSS 0.00332 (pct 0.26)。**水平伝播: 中** (SSO 経路でアカウント状態の検査が抜ける典型。SSO を後付けした OSS 全般) |
| CVE-2026-93328 | Google MCP Toolbox for Databases 1.2.0〜1.4.0 | CWE-22, CWE-862 / v4 9.3 | cloud-storage ソースのツール呼び出しパラメータに認可チェック・パス検証なし → 未認証でホストのファイルを外部 GCS バケットへ持ち出し / 任意ファイル上書き | [PR](https://github.com/googleapis/mcp-toolbox/pull/3454) (commit 不明) | CVSS 9.3。**水平伝播: 高** (MCP ツール引数がファイルパス sink に届く型の 3 例目。SiYuan / designer-mcp に続く) |

**次点 (参考)**:
- CVE-2026-115189 Mautic: Twig のテーマ用サンドボックスから脱出して RCE (v3.1 8.8)。GHSA-9fx4-7cmj-47vg の不完全修正 (GHSA-h7pm-79gc-8867、commit 不明)。Mautic は同時に計 9 件 (SQLi ×2、PHP オブジェクトインジェクション、アップロードからの RCE v3.1 9.9) を公開。
- CVE-2026-110720 consul-k8s: コンポーネント ACL のバインドルールで namespace をまたいだ認可バイパス (v3.1 9.9、HCSEC-2026-50、commit 不明)。Consul 本体の認可バイパス 3 件 (CVE-2026-105608 / 105765 / 115804) も同時。
- CVE-2026-111590 Harbor: Webhook の宛先で private / link-local を拒否しない SSRF。エラー時の応答本文が実行ログに残るので結果を読める (GHSA-2phj-cp9f-qq6w)。
- CVE-2026-89209 Mendix SAML: IdP-initiated フローで SAML アサーションのリプレイを防げない (CWE-294、v4 7.6、SSA-137528)。

### 今日の CVE 所感
- 最多のバグクラスは「2 つのパーサーの解釈差」(CWE-436 / 444)。ZIP の CD と LFH (zip2)、チャンク行の bare LF (bandit・Starman)、IP リテラル表記 (hackney)、JNI の modified UTF-8 による SNI 変換 (netty-tcnative) が同じ日に出た。「片方が検査し、もう片方が使う」構成を探すことが、そのまま他実装でのバリアントハントになる。10/25 号の adm-zip (正規化前の重複検査) と zip2 は同じ「検査対象と展開対象の不一致」で、ZIP ライブラリの横断調査は今週の狙い目。
- 共通 sink 型: go-playground/webhooks の「secret が空なら検証しない」(Burrito)、Pillow の `Image.open` をデコーダ制限なしで呼ぶ箇所 (vLLM)、MCP ツールの引数がファイルパスに届く箇所 (mcp-toolbox、直近で 3 例目)。いずれも GitHub のコード検索で他の利用者を洗い出せる。
- 認証・SSO: OIDC nonce をセッションに束縛しない (social-core)、SSO 経路でアカウントの有効・無効を確認しない (Snipe-IT)、SAML リプレイ (Mendix) が同時に出た。RP 側の実装チェックリストとしてまとめて使える。
- 診断で優先したいのは、外部公開されがちで未認証 RCE になる OpenHands のサンドボックスサーバー、EEF CNA が十数件を一括採番した Erlang / Elixir の HTTP スタック (bandit / hackney)、Netty で TLS を終端する Java サーバー、Open5GS の SBI。
- FortiSandbox の CVE-2026-107656 (CVSS 9.8) は NVD 登録が 10/26 だが、ベンダー公開が 10/13 のため新規として扱っていない。

## 日本国内のセキュリティ動向

### 国内インシデント・事故

#### [2026-10-25〜27] [続報] GMO「お名前.com デスクトップクラウド」: 第 7 報で攻撃者の予告 (10/27 12:00 に利用者情報の公開とランサムウェア攻撃) を公表。代表ブログは 10/21 付で 5,000 万ドルの要求文書があったと明かし、取引損失の全額補償を表明
- **前回から何が変わったか**: 第 6 報・第 7 報が出て、会社側の文書で予告期限が明記された。
- **何が起きたか**:
  - 第 7 報 (10/26 23:10 時点、10/27 0:20 訂正) で GMO は、攻撃者とみられる者から「10 月 27 日 (火) 12:00 に、お客様の情報の公開とランサムウェア攻撃を行う」という予告を受けたと公表した。社員が利用者宅を回って端末を預かり、グループのホワイトハッカーチームがマルウェア (ランサムウェアを含む) の有無を解析している。
  - 第 6 報では、端末のフルスキャン、ネットワークから切り離した状態でのバックアップ、全セッションのログアウト、FX・証券・メール・Google のパスワード変更と多要素認証の設定を、別の安全な端末から行うよう改めて求めた。
  - 熊谷正寿代表のブログ (10/25、10/26 追記): 影響の可能性があるサーバーは 26,739 台、国内外 70 社以上の証券・FX 事業者の取引口座が不正操作の対象。10/21 11:57 付の要求文書は 5,000 万ドル (約 80 億円) を要求しており、支払っていない。取引所などが返金に応じない場合も損失の全額を GMO インターネットが補償する。社内のホワイトハッカーが事前に課題を指摘していたが、対応の深さと速さが足りなかったと認めた。GMO イエラエの調査で、日本企業約 20 社への不正アクセスの攻撃元で AI 自律侵入テストツール「ARTEX」が悪用されていたとも記した。裁判所を通じた開示請求の手続きにも着手した。
  - NHK は別途、ハッカー集団が「27 日正午までに 100 万ドル (約 1 億 5,700 万円)」を要求したと報じた。
- **評価**: 要求額は代表ブログ (5,000 万ドル、10/21 の文書) と報道 (100 万ドル、27 日期限) で食い違う。要求が 2 回あった可能性もあるが未確認。本ダイジェストの公開時点は期限の前で、正午以降に情報公開や利用者端末へのランサムウェアが実際に起きたかは明日以降に追う。診断の観点では、「社内診断チームの指摘が修正の優先度づけで後回しにされた」ことが原因の一つとしてトップ自身の口から公表された点が重い。指摘事項の SLA とエスカレーションの設計を見直す材料になる。10/26 号で取り上げた攻撃者の LLM ペンテスト・ハーネス (Artex) が、国内の実被害の文脈で名前が出たことにも注意。
- 出典: [GMO 第 7 報](https://group.gmo/info/alert/2026102602/) / [GMO 第 6 報](https://group.gmo/info/alert/20261026/) / [熊谷代表ブログ](https://www.kumagai.com/?eid=19600) / [NHK (10/26)](https://news.web.nhk/newsweb/na/nd-20261026de65733) / [NHK (10/27)](https://news.web.nhk/newsweb/na/nd-20261027de66048)

#### [2026-10-26] [続報] ユミルリンク (Cuenote) の第二報: 漏えいは 50 システム・延べ 5,162 万件に拡大。JR 東海・JR 西日本・JR 九州の「エクスプレス予約」「スマートEX」会員約 17 万件にも
- **前回から何が変わったか**: 第 1 報 (10/19) の 5 システム・約 900 万件から大幅に拡大し、手口も判明した。
- **何が起きたか**: 開示資料によると、攻撃者はプログラムの脆弱性を突いてサポート・品質管理担当者の認証情報を取得し、不正プログラムを設置して DB からデータを出力した。同じ担当者の資格情報で他システムへの認証も試み、新たな 45 システムでは不正プログラム経由の参照や、ログイン時のセッション情報を奪った不正ログインがあった。Cuenote FC への試行は 81 システムで、うち 49 システム (すべて単一企業専用構成) で漏えい、延べ 51,628,280 件。16 システムは件数を調査中。Cuenote BASE では契約者 190 件 (企業名・氏名・電話・メール) が閲覧可能だった。同社ドメインを使ったセゾンカードかたりの迷惑メールも確認している。JR 3 社は 10/26 に、会員約 17 万件分 (メール、会員 ID、カナ氏名、会員種別) の漏えいを発表した。
- **評価**: 開示資料は原因を「プログラム脆弱性」「ライブラリの脆弱性」とだけ書き、ライブラリ名や CVE は示していない。本質は、**ベンダーのサポート用アカウントが顧客ごとの専用環境に横断して届く設計**だったこと。マルチテナント SaaS (専用構成を含む) の診断では、保守・サポート用資格情報がテナントをまたいで使えないかを確認項目に入れたい。ブラストメール (10/22〜) に続く、メール配信 SaaS 起点の大規模な連鎖被害である。
- 出典: [ユミルリンク 適時開示 (第二報)](https://ssl4.eir-parts.net/doc/4372/tdnet/2898564/00.pdf) / [INTERNET Watch](https://internet.watch.impress.co.jp/docs/news/2151309.html) / [Yahoo!ニュース (共同通信)](https://news.yahoo.co.jp/articles/b7bca3752d568962d5fd9f47a56cbd8d0ce47b19)

#### [2026-10-26] [続報] Joshin (上新電機) の第 2 報: 会員情報 最大約 600 万件。サブスク最大約 23 万件ではログイン ID・初期パスワードと手書きサインも対象
- **前回から何が変わったか**: 初報 (10/17、適時開示 10/19) では範囲が不明だったが、3 システムに分けて件数が示された。
- **何が起きたか**: 10/16 にネットワークの異常を検知し、不正アクセスの形跡を確認した。漏えいの可能性は、会員情報 DB サーバー 最大約 600 万件 (氏名・住所・電話・会員番号)、「ジョーシンのサブスク」最大約 23 万件 (会員番号、電話、手書きサインのバイナリ、ログイン ID と初期パスワード、請求履歴、契約番号、デバイス ID、有効化コード)、リフォーム写真アップロードシステム 最大約 800 件 (免許証画像 2 件、マイナンバーカード 1 件、口座番号 5 件、工事写真)。クレジットカード情報は保持していない。原因・侵入経路は未公表。
- **評価**: 初期パスワードがそのまま保存されたアカウントや手書きサインのような機微データが、会員 DB と同じ侵害範囲に入っていた。セグメント分離と、初期パスワードの平文 (または可逆) 保存の有無が論点になる。
- 出典: [上新電機 適時開示 (第 2 報)](https://www.joshin.co.jp/ja/ir/news/auto_20261026556267/pdfFile.pdf) / [INTERNET Watch](https://internet.watch.impress.co.jp/docs/news/2151273.html)

#### [2026-10-26] 楽天トラベル: 2 件の不正アクセスで合計最大約 354 万件。海外ホテル予約ページの約 3.6 万件はカードの発行者識別番号・下 4 桁・有効期限を含む
- **何が起きたか**: 楽天トラベルが 10/26 に 2 件の事象を公表した。
  - 事象①: 子会社 Rakuten Travel Xchange が運営する海外ホテル予約ページで、9/10 に異常を検知し 9/16 に改修。予約者最大約 4 万件 (氏名、メール、電話、居住国、予約情報、同伴者) のうち約 3.6 万件は支払情報 (カード発行者識別番号、下 4 桁、名義、有効期限、ブランド) を含む。ログイン利用者最大約 260 万件 (氏名、メール、電話、社内 ID) も対象。
  - 事象②: 多言語予約サイトで 10/20 に検知し 10/21 に改修。ログイン利用者最大約 86 万件 (メール、社内 ID) と、管理画面に入力された宿泊施設従業員最大約 4 万件 (アカウント名、メール、社内 ID)。
  - 二次被害は確認されていないとしている。原因は未公表。
- **評価**: 事象①は検知から公表まで約 1.5 か月かかった。事象②の宿泊施設側の管理画面アカウント情報は、宿泊施設を狙うフィッシングやアカウント乗っ取りの足がかりになりうる (OTA の管理画面を狙う手口は近年国内外で多い)。
- 出典: [楽天トラベル お知らせ](https://travel.rakuten.co.jp/info/announce/20261026.html) / [INTERNET Watch](https://internet.watch.impress.co.jp/docs/news/2151305.html) / [日本経済新聞](https://www.nikkei.com/article/DGXZQOUC2686T0W6A021C2000000/)

#### [2026-10-26] ギフティ: 子会社のシステムの脆弱性を悪用され e ギフトを不正発行された。損失約 5.5 億円の見込みで特別損失に計上
- **何が起きたか**: ギフティの適時開示によると、10/25 に連結子会社が運用するシステムの一部が脆弱性を悪用されて不正アクセスを受け、そこを経由して e ギフトが新たに不正発行された。同日システムを停止し、今後も再開しない。利用者が持つ e ギフトへの被害や個人情報の漏えいは確認されていない (会社発表)。損失は約 5.5 億円の見込みで、2026 年 12 月期第 4 四半期に特別損失として計上する予定。警察に相談している。
- **評価**: 情報漏えいではなく、**価値を発行する機能そのもの**を悪用された事例。ペンテストでは、ポイント・ギフト・クーポンなどの発行・付与 API の認可と業務ロジック (発行上限、承認フロー、冪等性) を優先して見るべき典型例。脆弱性の種別は未公表。
- 出典: [ギフティ 適時開示](https://contents.xj-storage.jp/xcontents/AS04721/9cd22cba/ef69/4403/bd9a/59025ae1c745/20261026193119181s.pdf)

> 参考: ヤマダデンキ (10/22 から一部サービス停止、個人情報への影響は調査中)、ブラストメール (ラクスライトクラウド) の波及、futureshop については、10/25〜27 に新しい一次資料を確認できなかった。

### 国内の注意喚起・ガイドライン・政策

#### [2026-10-26] 政府がサイバーセキュリティの関係閣僚会議を初めて開催。高市首相が「来週中をめど」に緊急対策パッケージを指示し、「アクセス無害化措置も含め、あらゆる対処オプションを戦略的に選択し、実行する」と述べた
- **何が起きたか**: 企業への不正アクセスによる大量流出が相次いでいることを受け、10/26 夕に官邸で関係閣僚会議を開いた。首相は、来週中をめどに緊急対策パッケージをまとめるよう指示した。パッケージの具体的な内容はまだ公表されていない。
- **評価**: 10/1 施行の能動的サイバー防御 (アクセス無害化) を、首相が対処オプションとして明言した。GMO は 10/24 に適用を要請しているが、同社は法律上の「特定社会基盤事業者」ではない。パッケージに脆弱性診断の義務化・支援、委託先 (SaaS ベンダー) の管理、公表ルールが入るかどうかを追いたい。ユミルリンクやブラストメールのような「委託先 SaaS 起点の連鎖」が対象として扱われるかが、診断業界にとって最大の関心事になる。
- 出典: [時事通信](https://www.jiji.com/jc/article?k=2026102600939&g=pol) / [NHK](https://news.web.nhk/newsweb/na/nd-20261026de65587)

#### [2026-10-26] JPCERT/CC、Brotli の境界外書き込み (CVE-2026-111497) について注意喚起 JPCERT-AT-2026-0034
- **何が起きたか**: 対象は Brotli v1.2.0〜1.2.1 未満、v1.1.0〜1.1.1 未満、v1.0.3〜1.0.10 未満で、修正版は v1.2.1 / v1.1.1 / v1.0.10。Node.js、Bun、Python 向け Brotli パッケージなど組み込み先が多岐にわたるとし、更新の適用に加えて侵害されていないかの調査も求めた。
- **評価**: CVE 自体は既報 (今日の深掘りを参照)。国内の公式注意喚起が出たことで、顧客向け報告書で根拠として引けるようになった。
- 出典: [JPCERT/CC](https://www.jpcert.or.jp/at/2026/at260034.html)

#### [2026-10-26] [続報] JPCERT/CC、PHP2Shell の注意喚起 (AT-2026-0033) を更新。PoC の多数公開と悪用試行の観測、CVE-2026-115560 の緩和策、侵害調査の観点を追記
- **前回から何が変わったか**: 10/26 の追記で、実証コードが多数公開され悪用を試みる通信の観測報告が相次いでいると明記した (ただし実際に任意コードを実行できるかは、バージョン・環境・メモリ配置に依存するとしている)。
- **何が起きたか**: 通常リリースで修正予定の CVE-2026-115560 には、`session.upload_progress.enabled=0` に設定して全ワーカーを再起動する緩和策を示した (CVE-2026-109619 の緩和策を適用済みなら追加対応は不要)。侵害調査の観点として、異常に長い PHPSESSID Cookie、不審な multipart/form-data リクエストと前後のメモリ上限エラーや HTTP 500、ワーカーの異常終了を挙げた。
- **評価**: 上のハニーポットでの RCE 成立 (4 段チェーン、800 KiB の cookie ダンプ) とよく対応しており、ログによる侵害調査のチェックリストとしてそのまま使える。
- 出典: [JPCERT/CC](https://www.jpcert.or.jp/at/2026/at260033.html)

### 国内製品の脆弱性 (JVN)

10/26 に新規公開が再開された (前回は 10/23 以降の新規公開なしと報告)。JVN iPedia / MyJVN は 10/27 未明の時点でもサービス停止中で、jvndb の RSS は「サービス停止中」のページを返す。

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| 2026-10-26 | JVN#75668103 / CVE-2026-113345 | 電子納品物検査支援システム Ver.4.0.36 以前 (国土交通省) | インストール時のファイルアクセス権の設定が不適切 (CWE-276)。アプリのフォルダ内のファイルを改ざんされ任意のコードを実行される。報告者は GMO Flatt Security の RyotaK 氏 | v4 8.5 / v3.0 7.8 (AV:L/PR:L)、ローカル権限昇格 | [JVN](https://jvn.jp/jp/JVN75668103/) |
| 2026-10-26 | JVNVU#96549652 / CVE-2026-107894〜107900 (7 件) | V-SFT ver 6.2.11.0 以前 (富士電機 / 発紘電機) | スタックオーバーフロー・境界外書き込み・境界外読み取り。細工した V7 ファイルを開くと任意のコード実行。修正版 6.2.12.0。報告者は Michael Heinzl 氏 | 各 v4 8.4 / v3.1 7.8 (AV:L/UI:R)、OT エンジニアリング端末 | [JVN](https://jvn.jp/vu/JVNVU96549652/) |
| 2026-10-26 | JVNVU#97400824 / CVE-2026-111497 | Brotli (Google) の C 実装 | 境界外書き込み (HTTP2Shell)。国内製品ではないが JVN ID が新規採番された。CVE 自体は既出 ([続報]) | JVN 上は CVSS 記載なし、RCE の可能性 | [JVN](https://jvn.jp/vu/JVNVU97400824/) |

- **所感**: 電子納品物検査支援システムは、公共工事の受注者や自治体の PC に広く入っている。インストール先フォルダの権限不備は「低権限ユーザー → 管理者」の古典的な経路で、端末診断で `icacls` による確認項目に加える価値がある。V-SFT は HMI 画面作成ツールで、プロジェクトファイルを開かせる型 (UI:R) の攻撃になる。OT ベンダーとのファイル授受経路を持つ現場では注意したい。

### 国内コミュニティ・研究・イベント

#### [2026-10-26] Classi 開発者ブログ: pixiv の「PHP2Shell 当日の爆速更新」を参考に、Docker Official Image と同じ構成のベースイメージを自前でビルドする仕組みを作った
- **何が書かれているか**: PHP2Shell の緊急パッチ (10/21 23 時前) から Docker Official Image の配信まで約 3 時間待たされた経験から、pixiv の方式 (10/22 公開) を Claude Code で Ruby 向けに移植した。公式イメージと同じ構成であることを 10 項目のスモークテストで確かめ、最初のイメージを約 1 時間で push した。10/23 の Ruby 緊急パッチには 19 時台に対応を終え、公式イメージの公開 (翌朝 5 時) より大幅に早かった。PHP 版も含め GitHub で公開している。
- **評価**: パッチ公開からコンテナ反映までの時間を、上流の配信に頼らず縮める実践例。修正公開前から悪用が始まった PHP2Shell の状況への、防御側の具体的な答えになっている。
- 出典: [Classi 開発者ブログ](https://tech.classi.jp/entry/2026/10/26/163000)

#### [2026-10-26] ScanNetSecurity: Internet Week 2026 のプログラム「C9 脅威情報の共有と活用の実践」の企画者インタビュー (IPA 産業サイバーセキュリティセンター、NTT データグループ)
- **何が書かれているか**: Internet Week 2026 は 30 回目で、オンラインは 11/19〜11/24 (土日を除く)、会場開催は 11/25〜27 に東京・両国 KFC Hall & Rooms。C9 は、アラート起点の監視の限界と、脅威ハンティングの前提となる質の高い脅威情報をどう集め共有するかを扱う。
- 出典: [ScanNetSecurity](https://scan.netsecurity.ne.jp/article/2026/10/26/56567.html)

#### [2026-10-26] IAjapan「第 26 回 迷惑メール対策カンファレンス」を 11/5・6 に東京で開催 (JPAAWG 9th General Meeting と共催)
- **何が起きたか**: INTERNET Watch が開催を告知した。ブラストメール・ユミルリンクとメール配信 SaaS 起点の被害が続いた直後で、送信ドメイン認証や配信事業者のセキュリティが議題として注目される (評価)。
- 出典: [INTERNET Watch](https://internet.watch.impress.co.jp/docs/news/2150997.html)

#### (日程確認) CODE BLUE 2026: トレーニング 11/11〜15、カンファレンス 11/17〜18 (東京)
- 公式サイトで日程を確認した (新着ニュースではない)。トレーニングの参加受付は 10/19 に始まっている。
- 出典: [CODE BLUE](https://codeblue.jp/)

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 55 (RSS / API / 個別記事。4 つの調査サブエージェントで並列に巡回)
- 採用件数: AI技術=11 / AIセキュリティ=6 / セキュリティ=14 / CVE=12 (+次点 4) / 国内インシデント=5 / 国内政策=3 / JVN=3 / 国内コミュニティ=4
- 除外理由内訳: 古すぎ=約 85 (RSS 上の範囲外記事を含む) / 重複=51 / 日付不明=7
- 取得失敗ソース:
  - openai.com の記事本文 (403 / JS チャレンジ) → RSS の pubDate で日付確認、内容は二次報道で確認
  - GitHub Advisories (API・HTML ともプロキシで拒否、セッションのリポジトリ範囲外) → GHSA ID と修正コミットは NVD の references から取得
  - OSV API (該当データ返らず) → NVD で代替
  - CISA のアドバイザリ RSS (all.xml / news.xml、Akamai で拒否) → KEV JSON は公式・GitHub ミラーとも取得可
  - Dark Reading 記事本文、Huntress / Cybernews RSS (Cloudflare チャレンジ)
  - SpecterOps / Rapid7 RSS (XML 解析失敗、grep で範囲内の新着なしを確認)、Mandiant Atom (404)
  - JVN iPedia RSS (サービス停止中ページ)、ヤマダデンキ公式 (connection reset)、楽天グループ news (空応答 → 楽天トラベルのお知らせで代替)、Security NEXT 記事本文 (JS 広告で抽出不可 → RSS 概要のみ)
  - arXiv cs.CR (最新投稿が 10/23 で範囲内なし)、embracethered.com (最新 10/13)
- NVD API は resultsPerPage=2000 で 503 → 200 件ずつのページングで 487 件を取得

</details>
