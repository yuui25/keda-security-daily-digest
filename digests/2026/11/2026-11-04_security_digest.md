# KEDA Daily Digest — 2026-11-04 (JST)

> 採用範囲: 公開日 2026-11-02 〜 2026-11-04
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

- **全体**: 海外は 11/3 (火) の記事が中心。国内は 11/3 が文化の日で、一次情報は 11/2 の公表と 11/4 朝の日経クロステックの特集にとどまった。CISA KEV は 10/30 以降、追加がない。JVN の新規公開は 11/2 の 2 件 (前号で掲載済み) のみで、JVN iPedia は停止が続いている。
- **まず見るべき 1 件 (深掘り)**: **Node-RED のエディタ/管理 API を認証なしで公開している環境が、自動化された攻撃で乗っ取られている** (VulnCheck の観測。Siemens SIMATIC IoT2050 の CVE-2026-58115、CVSS 10.0)。`POST /flows` を 1 回送るだけで inject ノードと exec ノードをつないだフローが置かれ、Linux ボットの投入や、`/cmd` のような常駐型のバックドアの設置まで進む。CISA KEV には入っていないが、VulnCheck KEV には入った。社内の OT/IoT、PoC 環境、クラウドの検証機など、診断で見つかる Node-RED は多い。
- **次点**: cPGuard (OPSSHIELD) の更新チャネルが 11/2 に乗っ取られ、5.88.12〜5.88.19 で `/etc/shadow` や root の SSH 関連ファイルを集めるスクリプトが配られた (サプライチェーン攻撃)。Kaspersky が見つけた UEFI ブートキット「BlackX」は、パッチを全部当てた Windows でも Secure Boot を回避した。Microsoft の「2011 年の証明書を手動で失効させる」手順を実施していない組織が狙われた。
- **AI 側**: Anthropic の改訂 S-1 に、AI で AI を作る「再帰的自己改善 (RSI)」に近づいているという警告が入っていた (TechCrunch)。MIT CSAIL の「Weight-Space Programming」では、GPT-6 Astra が他のモデルの重みを直接読んで書き換え、Qwen3.5-0.8B の MATH-500 を 7.9% から 48.1% に上げたと主張している。Gartner は、エージェントの処理ステップの 9 割はオープンウェイトのモデルで足りると試算した。
- **AI セキュリティ**: 「エージェント的な攻撃」の実例が続いた。3AM ランサムウェアのアフィリエイトが、AI のループらしい手順で英国の学校を暗号化した (Bitdefender)。Chainstack は、ARTEX 系とみられる攻撃で本番環境まで侵入された。Binance は 64.3 億ドル窃取の経緯を公表し、偽の採用面接と「社内 AI ツールの悪用」が侵入経路だったと説明した。arXiv では、MCP のツール汚染を 12 フレームワーク × 18 モデルで実測した研究 (成功率 22.9%) と、削除系の MCP ツールの 9 割にサーバー側の確認がないという研究が出た。
- **国内**: 11/2 の公表分の続報が中心。NTT データの社債特典サービスの委託先が Securitize Japan と判明した。GMO は 2024 年に脆弱性を指摘されたあと再診断していなかった (日経クロステック)。グッドスマイルカンパニーの公式ショップでは、カード情報 2,800 人分が窃取されたおそれがある。日経クロステックは 11/4 に、10/1 に根拠法が施行された能動的サイバー防御の特集を組んだ。

## 今日の深掘り

### Node-RED を認証なしで公開している環境が自動で乗っ取られている。Siemens SIMATIC IoT2050 の CVE-2026-58115 (CVSS 10.0) で実際の悪用を観測 (VulnCheck)

- **概要 (事実)**:
  - VulnCheck のハニーポットが 10/30 に、CVE-2026-58115 を突く完全なエクスプロイトを捕捉した。VulnCheck は 11/3 に詳細を公開した。
  - CVE-2026-58115 は、Siemens が 2026 年 8 月に公表した脆弱性。対象は、Industrial OS で Node-RED を入れている SIMATIC IoT2050 Advanced。Node-RED の HTTP インターフェースに認証がなく、未認証の遠隔の攻撃者がフローを作り、最高権限で任意のコードを実行できる (CWE-306、CVSS 10.0)。V4.3.4.1 で修正された。
  - VulnCheck は自社の KEV カタログに追加した。CISA の KEV には、11/4 時点で入っていない。EPSS は 0.0089 (11/3 時点)。
- **技術的な中身**:
  - 攻撃は `POST /flows` の 1 リクエストで完結する。中身は 3 重にエンコードされていた。
  - 使われるのは、Node-RED に最初から入っている 2 種類のノードだけ。**inject ノード** (起動時やスケジュールでメッセージを出す) を **exec ノード** (シェルコマンドを実行する) につなぐと、デプロイした瞬間にコマンドが動く。ユーザーの操作は要らない。
  - 観測されたペイロード:
    - 初期: `85.215.73[.]250` から `bot-linux-amd64` を wget で取得し (失敗したら curl)、`/dev/shm/.b` に保存して実行する。メモリ上のファイルシステムに置くため、再起動で消える。
    - その後: 同じサーバーから `wget.sh` を取る 2 段構えに変わった。別の要求は `45.194.90[.]57:38472` から `.sys_update` を取り、カーネルのワーカースレッドに見せかけた `/tmp/.kworker` として実行した。
    - ダウンローダーを使わないパターンもある: `http in` ノード (例: `/cmd` やランダムなパス) → function ノード → exec ノード (`addpay` 有効) をつなぎ、クエリパラメーターで後からいつでもコマンドを送れるようにする。フローとして保存されるので、再起動しても残る。
  - 送信元は Microsoft のネットワーク内の IP (ブラジルに位置)。10/30〜11/1 に Node-RED を 16 回狙い、VulnCheck のハニーポット全体では、Apache Solr、Camunda、Gitea、MLflow、Traefik、Joomla を含む 8 つの CVE に計 125 回の要求を送っていた。VulnCheck は「無差別の大量スキャン」と見ている。
  - 結論として VulnCheck は「adminAuth のない Node-RED は、自動で見つけられて悪用されている」と述べた。つまり、CVE が付いているのは Siemens 製品だが、**狙われている条件は「Node-RED のエディタ/管理 API に認証がないこと」そのもの**。
- **背景・経緯 (過去の事象の引用)**:
  - Node-RED のエディタは、`settings.js` の `adminAuth` を設定しない限り認証がかからない。公式ドキュメントも、既定では保護されていないと明記している。設計上の既定値なので、「認証なしで公開されている Node-RED は、そのままコード実行の窓口になる」という話は以前から知られていた。
  - Siemens は 8 月の advisory で、Node-RED のアンインストールか、HTTPS 化、エディタと管理 API への認証 (認証情報または OAuth/OpenID)、HTTP ノードとダッシュボードへの Basic 認証を勧めていた。今回はその公表から 2 か月あまりで、悪用が始まった。
- **なぜ今これが重要か (評価)**:
  - 必要なのは、エクスポートしたフロー JSON を 1 本 POST することだけ。認証回避もメモリ破壊も要らないので、スキャナーに組み込むのが簡単で、すでに複数の CVE と一緒にばらまかれている。
  - Node-RED は IoT ゲートウェイや工場の可視化、社内の自動化、データ連携の PoC でよく使われ、「検証のつもりで立てたら、そのままインターネットに出ていた」というケースが多い。外部の診断や ASM で見つかった場合、管理画面の露出 (情報) ではなく **未認証 RCE (Critical)** として報告すべきもの。
  - Siemens 以外の製品に組み込まれた Node-RED でも、同じ条件なら同じことが起きる。今回の CVE は「組み込みの既定設定が、そのまま脆弱性になる」典型例で、他の OT ベンダーの製品にも同じ形の advisory が出る可能性がある (推測)。
- **読者が今日できること**:
  - 外部から見える Node-RED を洗い出す: Shodan/Censys で `http.title:"Node-RED"` や、ポート 1880 を自社の範囲で検索する。見つけたら、`GET /flows` と `GET /settings` が未認証で 200 を返すかを確認する (`adminAuth` が有効なら 401 が返る)。
  - 稼働中のインスタンスの `flows.json` (または `GET /flows` の結果) で、`exec` ノード、外向けの `http in` ノード、`wget`/`curl` を含む function ノードを grep する。ホスト側では `/dev/shm/.b` と `/tmp/.kworker`、上記の 2 つの IP への通信を探す。
  - `settings.js` で `adminAuth` と `httpNodeAuth` を設定し、エディタ (`httpAdminRoot`) をローカルや VPN の内側に閉じる。IoT2050 は V4.3.4.1 以降に更新する。
- 出典: [Help Net Security](https://www.helpnetsecurity.com/2026/11/03/node-red-cve-2026-58115-exploitation/) / [The Hacker News](https://thehackernews.com/2026/11/attackers-exploit-critical-siemens.html) / [The Register](https://www.theregister.com/security/2026/11/02/max-severity-bug-in-widely-used-ot-programming-tool-exploited-to-deliver-linux-malware/5307086) / [SecurityWeek](https://www.securityweek.com/critical-node-red-flaw-exploited-in-attacks/) / [EPSS API](https://api.first.org/data/v1/epss?cve=CVE-2026-58115)

## AI 技術・トレンド

### [2026-11-02] Anthropic の改訂 S-1 に「再帰的自己改善 (RSI) の能力に近づいている」という趣旨のリスク記載。計算資源の粗利も悪化
- **何が起きたか**:
  - TechCrunch によると、11/2 に提出された S-1/A の細かい記載に、Anthropic が AI を研究開発に使っていることと、「より強力な AI を作るために AI を使うことは、進歩の速度を急に上げた場合に大きな安全上のリスクになりうる」という警告が入っていた。Anthropic は、これを責任あるスケーリングポリシー (RSP) で監視・緩和する領域の 1 つだとしている。
  - 同じ提出書類について TechCrunch は 11/3 に、売上に対する計算資源のコストの比率 (コンピュートのマージン) が悪化していると報じた。
- **なぜ重要か**: 上場の目論見書は、法的な責任を伴う文書。そこに「RSI の手前」を示唆する記載が入ったこと自体が珍しい。セキュリティの面では、AI による AI 研究の自動化が進むほど、評価や監査が追いつかなくなる構図が強まる (評価)。前号で扱った財務の数字の続きとして読むとよい。
- 出典: [TechCrunch (RSI)](https://techcrunch.com/2026/11/02/anthropic-warns-that-its-very-close-to-rsi-capability-aka-self-building-ai/) / [TechCrunch (計算資源の経済性)](https://techcrunch.com/2026/11/03/anthropic-is-still-grappling-with-the-economics-of-compute/)

### [2026-11-02〜03] MIT CSAIL「Weight-Space Programming」: GPT-6 Astra が他のモデルの生の重みを読み、0.016% を書き換えて MATH-500 を 7.9%→48.1% に。Simon Willison 氏はローカルの Qwen 3.8 27B でも再現
- **何が起きたか**:
  - MIT CSAIL の Rikiya Takehi 氏らは、"Sparks of Weight-Space Programming: LLMs can natively read & write neural network weights" を公開した。浮動小数点数を並べたテキストとして重みを渡すと、GPT-6 Astra がそのネットワークが何を学習したかを言い当て、PPO で 1 億ステップ学習したネットワークより強いゲーム用の小さなネットワークを、ゼロから書けたという。
  - Qwen3.5-0.8B については、モデルカードでも注意されている「推論のループ」の原因を重みから特定し、0.016% の重みを直接編集して MATH-500 を 7.9% から 48.1% に上げ、IFEval も約 3 倍にしたと主張している (勾配は使っていない)。
  - Simon Willison 氏は 11/3 に、論文の例の 1 つを、ノート PC で動かした Qwen 3.8 27B でも再現できたと報告した。
- **なぜ重要か**: 「重みは読めないバイナリ」という前提が崩れると、モデルの供給網のリスクの見方が変わる。重みに意図的な振る舞い (バックドア) を書き込む作業や、逆にそれを見つける作業が、LLM で自動化できるようになるかもしれない (評価)。Hugging Face などで配布される重みの検査 (pickle の検査だけでなく、振る舞いの検査) の重要性が増す。
- 出典: [Simon Willison](https://simonwillison.net/2026/Nov/3/qwen-can-interpret-model-weights/) / [The Register](https://www.theregister.com/ai-and-ml/2026/11/03/forget-retraining-ai-can-now-tweak-another-ais-weights/5307105)

### [2026-11-03] Gartner「エンタープライズのエージェント処理の 9 割はオープンウェイトで足りる」。最も安いクローズドモデルの 1/4、フロンティアモデルの最大 1/20 のコスト
- **何が起きたか**: Gartner のアナリストは "Open-Weight Models Will Run 90% of Enterprise Agentic Workflow Steps" で、エージェントのワークフローの手順の 9 割は分類、ツール呼び出し、検証、突き合わせなどの定型処理で、オープンウェイトのモデルが同等の精度で処理できると分析した。実際には冗長な出力や再試行が増えるため、フロンティアモデルに対する 1 タスクあたりの節約は 5〜6 倍程度とも認めている。「2030 年までに、運用系のエージェント処理の 90% がオープンウェイトのモデルで動く」と予測した。
- **なぜ重要か**: Gartner は、コストよりも「業務の履歴を外部 API に出さずに済む」という主権の面を重視している。診断の立場では、社内に自前で推論基盤 (vLLM、Ollama、推論ゲートウェイ) を置く組織が増えるので、それらの未認証 API や、前号の LLMjacking の対象になるエンドポイントが増えると見ておくべき (評価)。
- 出典: [The Register](https://www.theregister.com/ai-and-ml/2026/11/03/open-models-can-do-90-of-agentic-work-at-a-twentieth-of-the-cost-of-a-frontier-llm-gartner/5307132)

### [2026-11-04] GitHub「Copilot Code Review Max」: 複数のモデルによる複数のレビューエージェントの結果を集約する、新しいエフォートレベル
- **何が起きたか**: Publickey によると、GitHub は Universe 2026 (10/28〜29) で、Copilot Code Review に既存の「Lite」「Balanced」に加えて、エフォートレベル「Max」を追加すると発表した。Max では、複数の AI モデルによる複数の独立したレビューエージェントの指摘を集約する。AI が生成するコードとプルリクエストの急増で、レビューの品質を保つ必要が増したことが背景だと説明している。
- **なぜ重要か**: ソースコード診断の観点では、「複数モデルで独立にレビューして、合議で誤検知を減らす」という構成が、主要な開発プラットフォームの標準機能に入ったことになる。社内の SAST やレビューの運用と、どの指摘が重複するかを比べる価値がある (評価)。
- 出典: [Publickey](https://www.publickey1.jp/blog/26/githubcopilot_code_review_maxgithub_universe_2026.html)

### [2026-11-04] GitHub、基盤の Azure 移行とブランチ単位のロックなどで、スループットを従来比 180 倍にする計画。来年初めに完了
- **何が起きたか**: Publickey によると、Microsoft CoreAI 担当 EVP の Jay Parikh 氏は Universe 2026 の基調講演で、GitHub は今年だけで 400 万 CPU コア、160PB のストレージ、50Tb/s のネットワーク帯域を増やしたと説明した。さらに、Azure への移行とマルチリージョン化、コンピュートとストレージの分離、ロックの単位をリポジトリからブランチに変える改善で、スループットを 180 倍にすると述べた。
- **なぜ重要か**: AI エージェントによる push と PR の量が、プラットフォームの設計を変えるほどになっている。大規模な基盤の移行期間中は、権限、監査ログ、Webhook の挙動の変化に注意が要る (評価)。
- 出典: [Publickey](https://www.publickey1.jp/blog/26/github180aigithub_universe_2026.html)

### [2026-11-03] 推論基盤の Fal、13 億ドルを調達して評価額は 160 億ドル (4 月の 2 倍)。年換算の売上は 8 億ドル超
- **何が起きたか**: 動画・画像・音声の生成モデルをホストして動かす Fal が、Bessemer 主導 (Nvidia、Sound Ventures、T. Rowe Price も参加) で 13 億ドルを調達した。Bloomberg によると評価額は 160 億ドルで、4 月の 80 億ドルから倍になった。Series E と F の合計は 16.5 億ドル。年換算の売上は今年はじめに 8 億ドルを超えた。
- **なぜ重要か**: オープンソースのモデルの推論を外部に任せる需要が、上の Gartner の分析と同じ方向で伸びている。推論 API の鍵の管理は、LLMjacking の対象として、クラウドの鍵と同じ扱いにする必要がある (評価)。
- 出典: [TechCrunch](https://techcrunch.com/2026/11/03/ai-inference-startup-fal-doubles-its-valuation-to-16b-as-demand-surges/)

### [2026-11-03] OpenAI「ChatGPT の検索クエリは Google の 5 分の 1 の量に達した」
- **何が起きたか**: The Verge によると、OpenAI は ChatGPT 経由の検索クエリの量が Google の 20% に相当すると発表した。
- **なぜ重要か**: OpenAI の自社発表の数字で、第三者の検証はない。とはいえ、検索の入口が LLM に移るほど、検索結果の汚染 (SEO ポイズニング) が「LLM が引用する情報源の汚染」に変わる。下の arXiv の「合成ソーシャルエンジニアリング」の研究とも関係する (評価)。
- 出典: [The Verge](https://www.theverge.com/ai-artificial-intelligence/1025482/openai-says-chatgpt-is-catching-up-to-google-in-search)

### [2026-11-03] Google、K-12 の生徒向けの AI ツールを来年から既定で無効に。AI を完全に止める学校は Google 検索も使えなくなる
- **何が起きたか**: Google は、Gemini、NotebookLM、Gemini in Classroom、Google 検索について、K-12 の生徒向けの AI 機能を、管理者が明示的に有効にしない限り無効にすると発表した。教育担当 VP の Chris Phillips 氏は NYT に「検索と AI は深く統合されている」と話しており、AI を全面的に止める学校は検索も使えなくなる。
- **なぜ重要か**: 「AI だけを切る」という管理上の選択肢がなくなりつつある例。企業でも、検索や業務 SaaS に AI が組み込まれるほど、生成 AI の利用禁止ルールは技術的に担保しにくくなる (評価)。
- 出典: [TechCrunch](https://techcrunch.com/2026/11/03/google-will-let-schools-disable-its-ai-tools-but-not-without-sacrificing-search/)

### [2026-11-03] Apple、恋愛・性的な内容を扱う AI コンパニオンとマッチングアプリを 18 歳以上に限定。11/16 から新しいコンテンツ記述子が必須に
- **何が起きたか**: Apple は開発者向けに、マッチングや恋愛関係の機能を持つアプリは 18+ のレーティングが必須になると告知した。性的・恋愛的な内容を扱う AI コンパニオンも対象になる。11/16 から、新しいコンテンツ記述子の記入が必要になる。
- **なぜ重要か**: AI コンパニオンが、年齢確認と未成年保護の規制の対象として明確に扱われ始めた。プラットフォームの審査で、AI アプリの機能の申告が求められるようになる流れ (評価)。
- 出典: [TechCrunch](https://techcrunch.com/2026/11/03/apple-restricts-dating-apps-and-ai-companions-to-users-18-and-up/)

### [2026-11-02] SUSE、「自動化と AI」を理由に従業員の約 10% を削減 (全社 1,900 人)
- **何が起きたか**: The Register が入手した社内メールによると、SUSE の CEO Dirk-Peter van Leeuwen 氏は、全世界の従業員の約 10% を減らすと伝えた。「最新のツールは、すでに日々の働き方を変えている」と説明している。SUSE は EQT が保有する非上場の企業。
- **なぜ重要か**: Linux ディストリビューションの開発元が AI を理由に人員を減らす。セキュリティの面では、パッチのバックポートや脆弱性への対応の体制がどう変わるかを見ておきたい (評価)。前号の Trail of Bits の「Codex で CVE の修正をバックポートした」話の裏返しでもある。
- 出典: [The Register](https://www.theregister.com/software/2026/11/02/suse-to-cut-one-in-ten-employees-because-of-ai/5306950)

### [2026-11-02] Simon Willison 氏の LLM CLI 0.37: gpt-6.1-sol / terra に対応し、既定モデルを gpt-6-luna に。「AI 支援の PR は問題になっていない」
- **何が起きたか**: LLM 0.37 では、gpt-6.1-sol と gpt-6.1-terra を追加し、OpenAI 互換のエンドポイントを登録する `llm openai endpoint add` を加えた。既定のモデルは、従来の gpt-5.6-luna の半額の gpt-6-luna に変えた。今回の修正には 12 人の作者が関わり、ほぼ全員が AI を使っていた。Willison 氏は、Opus 5.5 や GPT-6 Astra でトリアージしているので、レビューの負担は予想ほどではなかったと書いている。
- **なぜ重要か**: OSS のメンテナーにとって「AI 生成 PR の洪水」をどう捌くかは共通の課題で、「PR は修正例が付いたバグ報告として扱う」という運用は参考になる (評価)。
- 出典: [Simon Willison](https://simonwillison.net/2026/Nov/2/llm/)

### [2026-11-03] AllenAI、長い文書の中での「状態の追跡」を測る StateBench を公開
- **何が起きたか**: AllenAI は、長いコンテキストの中で、エンティティの状態の変化 (変数の再代入、物の受け渡しなど) をどれだけ正しく追えるかを測るベンチマーク StateBench を公開した。最新の更新を探すだけの問題と、変化の連鎖をたどる難しい問題を分けて評価する。Transformer には長い依存の連鎖について理論的な限界があることが、Gated DeltaNet などの再帰的・ハイブリッドなアーキテクチャの動機になっていると説明している。
- **なぜ重要か**: コードを読んで「この変数はどこで汚染された値になるか」を追うのは、テイント解析そのもの。LLM によるソースコード診断の精度の限界を見積もる材料になる (評価)。
- 出典: [Hugging Face Blog](https://huggingface.co/blog/allenai/statebench)

### [2026-11-02] Marvell、光通信の Lumentum を全額株式交換で買収。企業価値は約 1,150 億ドル
- **何が起きたか**: Marvell Technology は 11/2 (現地時間)、高性能レーザーや光トランシーバーの Lumentum Holdings を買収することで合意した。負債を含む企業価値は約 1,150 億ドル (約 18 兆円)。AI データセンターで、銅線から光への接続の移行に対応する狙い。
- **なぜ重要か**: AI の計算資源の競争が、GPU から周辺の接続技術に広がっている。半導体の供給網の集中が進む (評価)。
- 出典: [ITmedia](https://www.itmedia.co.jp/news/article/2611/03/2000002830/)

## AI セキュリティ

### [2026-11-03] [続報] Google GTIG/Mandiant の LLMjacking: 累計で 100 万ドルの請求を受けた組織も。「公開エンドポイントのスキャン」と「鍵の窃取」の 2 系統があり、「LLM ミキサー」に転売
- **前回 (11/2 の報道) から変わった点**:
  - 1 日 10 万ドル超に加えて、累計で 100 万ドルに達した組織があることが分かった。
  - 攻撃者は 2 つの系統に分かれる。公開されている LLM のエンドポイントをスキャンする系統と、守られていないマシンから正規の API キーを盗む系統。手に入れたアクセスは「LLM ミキサー」と呼ばれるサービスに売られ、加入者のプロンプトが盗まれた鍵経由で中継される。転売のあとは、リクエストが毎秒 1,000 件を超えることもある。
- **なぜ重要か**: プロバイダーからは正規の利用に見えるので、請求で初めて気づくことが多い。診断では、公開された推論エンドポイント (Ollama、vLLM、LiteLLM のプロキシなど) の認証と、CI やフロントエンドに残った API キーを、クラウドの認証情報と同じ重さで扱うべき (評価)。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/google-llmjacking-attacks-rack-up-1-million-in-cloud-ai-charges/) / [Help Net Security](https://www.helpnetsecurity.com/2026/11/03/llmjacking-stolen-ai-access-cloud-bills/)

### [2026-11-03] 3AM ランサムウェアのアフィリエイト、英国の学校法人を暗号化。40〜100 秒おきに少しずつ変わるコマンドから、Bitdefender は「AI のエージェント的なループ」を疑う
- **何が起きたか**:
  - Bitdefender によると、9/10〜19 に、管理されていない端末から約 50 台に到達し、うち約 37 台を暗号化した。
  - 3 台の Veeam バックアップサーバーから、公開されている PowerShell ツールの改変版で認証情報を取り出して復号した。Chrome の認証情報 DB のコピー、Mimikatz と LSASS のダンプも使った。`library` と `svc_bkpmon` というドメイン管理者のバックドアアカウントを作り、別々だった 3 つの AD ドメインに双方向の信頼関係を設定して範囲を広げた。
  - 少しずつ変えたコマンドが、ほぼ一定の 40〜100 秒の間隔で繰り返されていたことから、AI が生成したコマンドと自動化されたループの可能性があると判断した。ただし、攻撃者側の端末は調べられておらず、モデルの種類や、人がコピー&ペーストで仲介していたかどうかは分からないとしている。
- **なぜ重要か**: 「AI が使われた」という主張は、ログの挙動からの推定にとどまる。それでも、Veeam の認証情報の窃取から AD の信頼関係の改変までの手順が、半自動で回せることを示している。ペネトレーションテストや TLPT では、「試行の間隔と、少しずつの変化」がある攻撃をどう検知するかを、ブルーチームと一緒に確かめる題材になる (評価)。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/uk-school-estate-hit-by-3am-ransomware-in-suspected-ai-assisted-attack/) / [Dark Reading](https://www.darkreading.com/data-privacy/3am-affiliate-ai-loops-european-school-attack)

### [2026-11-03] Chainstack、第三者のコンポーネント経由で開発環境から本番環境まで侵入される。顧客の情報とパスワードのハッシュが流出。ARTEX を使う中国系の作戦との重なりが指摘される
- **何が起きたか**: ブロックチェーン基盤の Chainstack は 11/3、攻撃者が 10/26 に第三者のコンポーネント経由で開発環境に入り、本番環境の一部まで権限を広げたと公表した。10/31 に検知し、その日のうちに遮断した。組織名、アカウント保有者名、メンバーのメールアドレス、パスワードのハッシュを含む DB にアクセスされた。ノードの認証情報を持つシステムにも届いていたため、顧客にはノードの認証情報と API キーの再発行を求めている。The Hacker News は、自律型の AI エージェントのフレームワーク ARTEX を使う中国系のクラスターの作戦と重なると見ており、API 基盤の WorkOS も同じフレームワークによる侵害 (GTM 系システムに限定) を公表した。
- **なぜ重要か**: ARTEX 系の作戦の被害が、具体的な企業名で出てきた。「開発環境から本番環境へ」という流れは、開発環境の秘密情報の分離と、環境間の信頼関係を見直すきっかけになる (評価)。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/chainstack-reports-production-systems.html)

### [2026-11-02 arXiv] MCP のツール汚染を、実際のツール実行で横断的に測定。12 フレームワーク × 18 モデル × 45 シナリオで成功率 22.9%、秘密情報の持ち出しを確認できたのは 12.1%
- **何が起きたか**: 研究者は、ツールの説明、スキーマのフィールド、応答データに仕込んだ指示を、検証なしでモデルのコンテキストに入れてしまう MCP の特性を、OSS ツール `mcpvenom` で測った。9,720 のセルのうち 2,113 で攻撃が成立した (22.9%)。成立したもののうち、攻撃者のツール呼び出しまでが 64.9%、攻撃者のエンドポイントへの接続までが 23.0%、カナリアで秘密情報の持ち出しを確認できたのが 12.1%。耐性は主にモデルで決まり、主要な 9 フレームワークの成功率は 23〜26% に集まっていた。意図的な防御を実装したフレームワークは 1 つもなかった。正規表現による説明文のスキャナーは、45 シナリオ中 20 を誤検知率 7.2% で止めた。モデルごとの成功率は 0.4%〜49.7% だった。
- **なぜ重要か**: 「フレームワークで守る」という前提が、実装の上では成り立っていない。MCP サーバーを使う AI 製品の診断では、ツールの説明と応答に指示を仕込むテストを、モデルを変えて回す必要がある (評価)。
- 出典: [arXiv:2611.03555](http://arxiv.org/abs/2611.03555v1)

### [2026-11-02 arXiv] 削除や送金をする MCP ツールの約 9 割に、サーバー側の確認がない。主要なホスト・SDK 41 個のうち 32 個は、既定で承認の手順がない
- **何が起きたか**: 公式の MCP レジストリの 1,000 リポジトリを標本調査したところ、破壊的なツールの推計 90% (95% CI 82〜95%) にはサーバー側の確認がなかった。確認を求める (elicitation) サーバーも、ホストが質問を中継できないと、そのまま処理を進めるか、モデルが立てられるフラグに頼っていた。人気の OSS のホストとエージェント SDK 41 個のうち 32 個 (アプリでは 25 個中 16 個) は、既定で承認の手順がなかった。4 つの SDK 経由で、5 つの低コストモデルのうち 4 つが、注入された削除を 960 回中 479 回実行した。
- **なぜ重要か**: MCP の仕様は「人が拒否できる」ことを求めているが、その仕組みをサーバーとホストのどちらが担うかが分かれていて、結果として誰も確認しない。読み取り専用・非破壊と注釈されていないツールはすべてホスト側で確認する、という設定だけで、承認のない組み合わせは 5.4% まで下がるとしている (評価: 設定項目として診断の確認リストに入れられる)。
- 出典: [arXiv:2611.02527](http://arxiv.org/abs/2611.02527v1)

### [2026-11-02 arXiv] IAMRAGBENCH: RAG の汚染で、LLM が生成する AWS IAM ポリシーの権限が広がる。AWS の `CheckNoNewAccess` が見逃す例も
- **何が起きたか**: 60 ケースのベンチマークで、文書に攻撃者の文脈を混ぜると、プロバイダー上は有効で、本来禁止の要求を新たに許可するポリシーが生成された (5 つのエンドポイントで、目標どおりの攻撃が 292 回中 46 回、15.75%)。弱める変更を「最終的なセキュリティアーキテクチャの例外」として示すと、成功率は 39〜64% に上がった。要件に違反するポリシーを再生した検査では、AWS の `CheckNoNewAccess` が「新しいアクセスなし」と判定する例もあった。
- **なぜ重要か**: IaC やポリシーを LLM に書かせる運用が増えるなかで、「設計文書の例外の記述」が権限昇格の入口になる。クラウド診断では、生成されたポリシーの差分を人がレビューする工程があるかを確認したい (評価)。
- 出典: [arXiv:2611.03431](http://arxiv.org/abs/2611.03431v1)

### [2026-11-02] OpenAI、バグバウンティを増額。重大な脆弱性の基本報酬は最大 3 万ドル、例外的な発見はボーナス込みで最大 17.2 万ドル
- **何が起きたか**: OpenAI は、ChatGPT、Codex、API Platform などの中核製品について、Critical の基本報酬を最大 3 万ドルにした。例外的な Critical は基本報酬が最大 10 万ドルのまま、ボーナス込みで最大 17.2 万ドルになる。Medium、High、Critical の報酬の範囲の中央値は、平均で 4 倍超に上がった。質の高いレポート (確実な PoC など) には倍率がかかり、5 段階のロイヤルティプログラムや、新機能ごとの期間限定のボーナス枠も設けた。社内では、自社モデルで脆弱性を見つけて再現し、修正を検証する「Defense Factory」と組み合わせると説明している。
- **なぜ重要か**: AI 製品の脆弱性の相場が、主要な SaaS と同じ水準に上がった。HackerOne の CEO が Help Net Security のインタビューで「ありふれた Medium の報酬は下がるかもしれない」と話したこととあわせると、AI が拾えない業務ロジックの欠陥に報酬が集中していく流れが見える (評価)。
- 出典: [Help Net Security](https://www.helpnetsecurity.com/2026/11/03/openai-bigger-bug-bounty-rewards/) / [OpenAI](https://openai.com/index/rewarding-defenders-with-bigger-bug-bounties) / [Help Net Security (HackerOne CEO)](https://www.helpnetsecurity.com/2026/11/03/kara-sprague-hackerone-ai-bug-bounty/)

### [2026-11-03] CrowdStrike、AI エージェントの可観測性の Fiddler AI と、AI のセキュリティテストの Dreadnode を買収。報道では計 4.95 億ドル
- **何が起きたか**: CrowdStrike は 11/3、2 社の買収に合意したと発表した。金額は公表していないが、WSJ によると Fiddler が約 4 億ドル、Dreadnode が約 9,500 万ドル。大半は現金で支払う。Falcon に、AI エージェントの可観測性と、自動化された AI のセキュリティテストの機能を加える。
- **なぜ重要か**: Dreadnode は、攻撃的なセキュリティ向けの AI エージェントの評価や、red team のツールで知られる。AI の red team が、EDR ベンダーの標準機能に吸収されつつある (評価)。
- 出典: [SecurityWeek](https://www.securityweek.com/crowdstrike-reportedly-paying-495-million-for-ai-security-firms-fiddler-dreadnode/)

### [2026-11-03] CWE-bench v2: 実在の OSS リポジトリで「脆弱性を見つけて、機能を壊さずに直す」100 タスクを公開。91 種類の CWE
- **何が起きたか**: Collinear AI は、エージェントに実在の OSS のチェックアウトと短い指示を渡し、セキュリティ上の弱点を見つけて直させるベンチマークの v2 を公開した。公開セットは 100 タスクで 91 の CWE を含み、採点は完全にプログラムで行う (決定的で再現可能)。モデルが学習で見ていない非公開セットも維持している。
- **なぜ重要か**: フロンティアモデルの発表で「CWE-bench の修正率」が使われ始めているので、その中身が公開されたことに意味がある。自社の AI による修正の評価に転用できる (評価)。
- 出典: [Hugging Face Blog](https://huggingface.co/blog/cwe-bench)

## セキュリティニュース

### [2026-11-03] Node-RED の未認証フロー作成による RCE (CVE-2026-58115、CVSS 10.0) の悪用を観測 → 今日の深掘りを参照
- **何が起きたか**: VulnCheck が 10/30 以降、`POST /flows` で inject + exec ノードを置き、Linux ボットやバックドアを設置する攻撃を観測した。CISA KEV には未登録。
- **なぜ重要か**: 詳細と確認手順は「今日の深掘り」に記載した。**悪用: あり (ハニーポットで観測) / PoC: 実際の攻撃のペイロードがある**。
- 出典: [Help Net Security](https://www.helpnetsecurity.com/2026/11/03/node-red-cve-2026-58115-exploitation/)

### [2026-11-03] サーバー保護ツール cPGuard の更新チャネルが乗っ取られ、5.88.12〜5.88.19 でバックドアと、`/etc/shadow`・SSH のファイルを集めるスクリプトが配られた
- **何が起きたか**:
  - 開発元の OPSSHIELD によると、11/2 02:06 UTC に、攻撃者が侵害された認証情報で cPGuard の更新システムに入り、悪意のあるスクリプトを 5.88.12〜5.88.19 に入れて配った。配布から 12 時間以内に検知した。
  - スクリプトはバックドアを設置し、`/etc/shadow`、`/etc/passwd`、root の MariaDB/MySQL の `my.cnf`、root のシェル履歴、root の SSH の authorized_keys と known_hosts を集めた。一部はすでに持ち出されている。
  - 5.88.25 以降でバックドアと残されたファイルは消えるが、コピーされた認証情報はそのまま使える。影響を受けた台数は公表していない。確認方法は `grep 'Successfully updated' /opt/cpguard/logs/install_log` で、5.88.12〜5.88.19 の行があれば該当する。
- **なぜ重要か**: cPanel/Plesk 系の共用ホスティングで使われるセキュリティ製品なので、root の権限で動く。1 台の侵害が、DB の root パスワードと SSH の信頼関係を通じて横に広がる。**悪用: あり (配布済み)**。該当したサーバーは、更新しただけで済ませず、パスワード・鍵・DB の認証情報をすべて入れ替える必要がある (評価)。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/cpguard-update-channel-hijacked-to.html)

### [2026-11-03] UEFI ブートキット「BlackX」、パッチを全部当てた Windows で Secure Boot を回避。原因は「2011 年の証明書の失効を手動で有効にしていない」こと
- **何が起きたか**:
  - Kaspersky が見つけた BlackX は、2023 年の BlackLotus と同じく、Secure Boot を回避して OS の起動前に動く。感染した組織は、Microsoft のパッチをすべて当てていた。
  - Microsoft は BlackLotus のあと、2023 年に新しい証明書「Windows UEFI CA 2023」を追加し、2024 年に旧証明書「Windows Production PCA 2011」を禁止リスト (DBX) に入れる手段を用意した。ただし、更新しても起動できなくなる端末が出るのを避けるため、失効は自動では有効にならない。
  - Kaspersky は「この有効化の手順は Microsoft のサイトの奥にあり、普通の管理者は気づきにくい」と指摘し、攻撃者はそれを見越して BlackLotus を模倣したと見ている。Microsoft は 2 週間前に出した KB に従うよう案内しているが、Ars Technica によると、その KB には「これまでのパッチだけでは Baton Drop 型の攻撃を防げない」とは書かれていない。
- **なぜ重要か**: 「パッチ適用済み」と「保護済み」が一致しない典型例。**悪用: あり**。Windows の構成の診断では、パッチの適用状況だけでなく、DBX に 2011 PCA が入っているか、新しい CA への移行が終わっているかを確認項目に入れるべき (評価)。
- 出典: [Ars Technica](https://arstechnica.com/security/2026/11/uefi-bootkit-infected-fully-patched-windows-machines-is-microsoft-to-blame/)

### [2026-11-03] [続報] Binance、64.3 億ドル窃取の経緯を公表。偽の Homebrew、偽の採用面接、社内の AI ツールの悪用、コンテナのデプロイトークンを経て、ウォレットの署名サービスに到達
- **前回 (11/1〜2 の FBI による北朝鮮 TraderTraitor への帰属) から変わった点**:
  - 6 月: Wallet DevOps チームの技術者 A が、人気の AI ツールを入れるために検索で見つけた、トロイの木馬化された Homebrew のインストーラーを実行した。Binance は検知して認証情報を入れ替えたが、A の役割とウォレット基盤チームの同僚の情報が攻撃者に渡った。
  - 9 月: 別の技術者 B に、正規の求人サイトで「プロジェクトディレクター」を名乗る人物が接触した。人事担当との 1 次面接、存在しない会社の「CEO」との 2 次面接 (チャットアプリ上) を経て、課題として渡されたリポジトリを業務 PC で開いた。セットアップの過程で悪意のあるコードが動き、正規の開発ツールの部品が差し替えられた。
  - 10/20: B の PC から社内の AI ツールを悪用して、A と別の技術者 C を支配下に置いた。A の PC にはコンテナのデプロイ権限のトークンがあった。
  - 10/29 17:15〜19:56: 攻撃者は C の PC にログインし、A の認証情報でコンテナをデプロイして悪意のあるスクリプトを動かし、社内のウォレット署名サービスから通常の出金処理の外で取引を発行した。
  - Binance はウォレット基盤を新しい環境に作り直し、社内の AI ツールとアクセス制御も作り直した。今年に入ってから、北朝鮮系とみられる事案を 57 件防いだとしている。
- **なぜ重要か**: 社内の AI ツールが、横展開の手段として名指しされた最初の大規模な事例。社内の AI アシスタントやエージェントが持つ権限 (他人の端末やチャットへの到達性) は、従来の RMM や管理ツールと同じ扱いで棚卸しする必要がある (評価)。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/binance-reveals-how-fake-job-interviews.html) / [The Record](https://therecord.media/binance-cryptocurrency-theft-months-long-campaign-nkorea)

### [2026-11-03] WordPress プラグイン「CryptoPayment Gateway」の未修正の脆弱性 (CVE-2026-81648、CVSS 10.0) に悪用の試み。ウォレットの認証情報を平文で取り出せる
- **何が起きたか**: 1.2.1〜1.2.2 (最新版) は、AJAX エンドポイントの 1 つで認可を確認しておらず、未認証のユーザーが任意のファイルの削除、決済ゲートウェイの設定の上書き、保存されたウォレットの認証情報の平文での取得などの管理操作を呼べる (NVD の記述)。修正版はなく、プラグインは 8/28 に WordPress のディレクトリから閉鎖された。累計のダウンロードは 1,845 回。Defused Cyber は、「匿名・KYC 不要の VPS」をうたう基盤からの悪用の試みを観測した。
- **なぜ重要か**: **悪用: 試行を観測 / 修正: なし**。プラグインは配布停止のため、使い続けているサイトは自分で気づかないと残り続ける。WordPress の診断では、閉鎖されたプラグインの一覧と照合したい (評価)。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/attackers-target-unpatched.html)

### [2026-11-03] パスワードマネージャー mSecure の開発元、現・元顧客に「パスワードの変更、2FA のリセット、パスキーの削除」を求めるメール。何が起きたかは説明せず
- **何が起きたか**: 開発元の mSeven Software は 11/3、アプリに関連する不審な活動を最近把握したというメールを、現在と過去の顧客に送った。調査の開始、被害の抑止、外部の専門家の起用は書かれているが、対象のシステム、時期、活動が止まったか、保存データが露出したかは書かれていない。11/3 18:00 UTC 時点で、X や Facebook での説明もなかった。mSecure は端末上で暗号化してから同期するとしているが、ドイツの BSI は 2025 年 12 月の調査で、Android 版 6.1.5 では開発元が理論上データにアクセスできたと指摘していた。
- **なぜ重要か**: パスワードマネージャーの侵害で、何が守られたかを示さずに「全部変えて」と頼むのは、利用者には最悪の伝え方。パスキーや 2FA のシードを同じ保管庫に入れる運用が、侵害のときにどれだけ負担になるかの例でもある (評価)。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/msecure-warns-users-to-change-passwords.html) / [The Register](https://www.theregister.com/security/2026/11/03/password-manager-msecure-tells-users-to-change-passwords-wont-say-why/5307296)

### [2026-11-02] Android の 11 月の更新で 200 件超の脆弱性を修正。最も深刻なのは、操作なしで遠隔コード実行につながる Framework の CVE-2026-58868
- **何が起きたか**: Google の 11 月の Android セキュリティ情報は、200 件超の脆弱性 (Critical は約 24 件) を修正した。パッチレベル 2026-11-01 の分は 119 件で、Framework が 65 件、System が 53 件。最も深刻な CVE-2026-58868 は、追加の権限もユーザーの操作も要らない遠隔コード実行。17 件は月次の更新より前に Google Play システムアップデートで配られた。NVD には、confused deputy (CWE-441) による権限昇格が多数登録されている。
- **なぜ重要か**: **悪用: 記事時点で言及なし**。モバイルアプリの診断では、端末のパッチレベル 2026-11-01 / 11-05 を、検証機の前提として揃えておきたい (評価)。
- 出典: [SecurityWeek](https://www.securityweek.com/androids-november-2026-updates-patch-over-200-vulnerabilities/)

### [2026-11-02] Microsoft の分析: 1999 年〜2026 年 9 月に公開された約 38.3 万件の脆弱性のうち、実際の悪用が確認されたのは約 2,000 件 (約 0.5%)
- **何が起きたか**: Microsoft Security Research は、CVE を「影響の種類」と「プラットフォーム」の 2 軸で分類した。攻撃者は、システムの乗っ取りにつながる遠隔コード実行、権限昇格、認証回避に偏って狙っている。AI による脆弱性の発見とエクスプロイトの開発が、防御側の対応期間をさらに縮めうると警告している。
- **なぜ重要か**: 「CVSS の高さ」ではなく「影響の種類 × 露出」で優先順位を付けるという考え方は、診断の報告書の優先度付けにもそのまま使える (評価)。
- 出典: [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/11/02/exploited-vulnerabilities-common-data-driven-analysis-real-world-attacks/)

### [2026-11-03] Microsoft、クラック版ソフトを探す利用者を狙う「偽ダウンロード」の作戦を報告。Inno Setup 風のインストーラーで複数の「オファー」を入れ、端末をプロキシや分散計算に使う
- **何が起きたか**: Microsoft Threat Intelligence によると、クラック版の商用ソフト、無料ゲーム、アクティベーター、プラグインなどを探す利用者に、トロイの木馬化されたインストーラーを配る作戦が続いている。1 回のインストールで複数の収益化用のソフトを入れ、オファーごとにコールバックで結果を記録する。確認した収益化の手段は、第三者の通信を端末経由で中継させる、分散計算のプラットフォームに登録する、ユーティリティ系のソフトを追加する、の 3 つ。
- **なぜ重要か**: 個々のソフトは正規の用途があるため、「マルウェアではない」として残りやすい。企業の端末が住宅用プロキシの出口にされると、攻撃の踏み台として自社の IP が使われる (評価)。
- 出典: [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/11/03/fake-download-campaign-uses-trojanized-installers-deliver-monetization-payloads/)

### [2026-11-03] Harvard 大学の 2025 年 11 月の侵害、HIBP の分析で 85.1 万件のメールアドレスが流出と確認。ShinyHunters が犯行を主張
- **何が起きたか**: Have I Been Pwned は、ShinyHunters が 2 月にリークサイトで公開した 1.1GB のデータを分析し、同窓会・寄付の部門のシステムから 85 万件超の一意のメールアドレスが流出したと確認した。氏名、生年月日、電話番号、住所、SNS のプロフィール、寄付の情報なども含まれる。Harvard は、社会保障番号、パスワード、カード情報は含まれないとしている。
- **なぜ重要か**: 寄付者や同窓生の詳しい属性は、標的型のなりすましに使いやすい。大学の「同窓会・寄付」のシステムは、本体の情報システムより管理が甘くなりがち (評価)。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/harvard-university-data-breach-exposed-info-of-851-000-accounts/) / [The Register](https://www.theregister.com/cyber-crime/2026/11/03/shinyhunters-hit-850k-alumni-donors-students-and-fam-in-last-years-harvard-university-raid/5307272)

### [2026-11-03] K-12 向けの管理ソフトの Frontline Education、130 万人超に漏えいを通知。第三者製品の脆弱性を突かれ、社会保障番号や保険の ID も
- **何が起きたか**: Frontline は、8/14 に第三者のソフトウェア製品の脆弱性を悪用されて環境に入られ、8/15 までに封じ込めたと説明した。Frontline Central と School Health Management から、学区の職員と生徒の氏名、社会保障番号、生年月日、運転免許証やパスポートなどの番号、Medicaid の ID を含む医療保険の情報、生徒 ID が盗まれた。
- **なぜ重要か**: 前号の米国の教育分野の侵害 (フロリダ州の学資援助サイト、Michigan State) に続く例。学区向けの SaaS は、多数の学区のデータを 1 か所に集める (評価)。
- 出典: [SecurityWeek](https://www.securityweek.com/frontline-education-data-breach-impacts-over-1-3-million/)

### [2026-11-03] Europol、偽の投資サイトを犯罪組織に提供していた会社を摘発。7 人を逮捕し、100 台超のサーバーを押収
- **何が起きたか**: Europol と Eurojust の支援で、アルバニア、キプロス、フィンランド、ドイツ、コソボ、北マケドニアが合同で動いた。キプロスとイスラエルから「Crime-as-a-Service」として偽の取引プラットフォームを提供していた会社を対象に、7 人を逮捕し、100 台超のサーバーを押収した。被害者は 50 か国以上で、Help Net Security によると被害額は 400 万ユーロ超。2022 年のドイツの夫婦の通報から 4 年がかりの捜査。
- **なぜ重要か**: 投資詐欺の「サイトと顧客データ」を供給する業者を狙った摘発。コールセンター側だけを捕まえても止まらない構造に手を入れた (評価)。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/police-seizes-over-100-servers-in-investment-scam-crackdown/) / [Help Net Security](https://www.helpnetsecurity.com/2026/11/03/investment-fraud-network-servers-seized/)

### [2026-11-02〜03] ロシア内務省、Kaspersky の協力で犯罪グループ VasyGrek (Fluffy Wolf) の基盤を解体し 3 人を拘束
- **何が起きたか**: 2016 年ごろから、主にロシアの企業に、取引先を装うフィッシングメールで遠隔操作ツールを送り込んでいたグループ。首謀者とされる人物は自宅軟禁、2 人は移動制限付きで釈放された。2025 年 9 月の事例では、経理担当者の PC から企業のオンラインバンキングに入り、66 万ルーブル超を送金させたという。
- **なぜ重要か**: ロシアがロシア語圏の犯罪グループを公に摘発するのは珍しい。対象がロシア企業を狙う組織である点に注意 (評価)。
- 出典: [The Record](https://therecord.media/russia-dismantles-vasygrek-infrastructure-detains-three)

### [2026-11-03] Apple が 99 か国に送ったスパイウェアの警告、メルツ首相のアジア訪問に同行したドイツの議員・官僚・記者にも。BSI は「感染していると仮定して端末を交換」と通知
- **何が起きたか**: Der Spiegel の報道として、韓国・日本・シンガポールを訪れたメルツ首相の一行に Apple の脅威通知が届いた。緑の党の共同党首 Franziska Brantner 氏が受信者だったと公表した。BSI は通知から 24 時間以内に、受信者に端末の交換を求める書面を送った。どれだけの端末が実際に感染したかは分かっていない。
- **なぜ重要か**: 一行が日本も訪れていたことから、訪問先の通信環境が攻撃の機会になった可能性も考えられる (推測)。要人の海外出張時の端末運用 (使い捨て端末、Lockdown Mode) を見直す材料になる (評価)。
- 出典: [The Record](https://therecord.media/german-officials-among-apple-spyware-warning-recipients)

### [2026-11-03] ロシア系の Gorbag、ウクライナの裁判所や前線近くの自治体を狙う。自己削除型の窃取マルウェアと WinRAR の CVE-2025-8088 を使う (ESET)
- **何が起きたか**: ESET によると、Gorbag は少なくとも 2025 年 2 月から活動し、ウクライナの法執行・司法機関、前線近くの地方行政、防衛分野だけを狙っている。CERT-UA の UAC-0226、Trend Micro の SHADOW-EARTH-066 と重なる。罰金や税金を装うスピアフィッシングで、マクロ付きの XLSM から BeautyStealer を動かしたり、WinRAR の脆弱性 CVE-2025-8088 (修正済み) から DLL サイドローディングで GIFTEDCROOK を動かしたりする。VPN の設定も盗むので、初期アクセスブローカーの可能性があると ESET は見ている。
- **なぜ重要か**: WinRAR の CVE-2025-8088 は、修正後も長く悪用され続けている。社内で古い WinRAR が残っていないかは、資産管理の基本的な確認項目 (評価)。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/russia-aligned-gorbag-hackers-exploit.html) / [Help Net Security](https://www.helpnetsecurity.com/2026/11/03/gorbag-apt-group-malware/)

### [2026-11-03] 英国 NCSC の年次レビュー: 2028 年までに、AI を使ったマルウェアによる重要インフラへのランサムウェア攻撃が「起きる可能性が非常に高い」
- **何が起きたか**: NCSC は年次レビューと、今後 2 年の AI と脅威の評価を公表した。研究者向けに作られた OSS の AI セキュリティツールが、攻撃に転用されていると指摘した。政府のコードを AI で分析する「Project DROMOS」で数百件の潜在的な問題 (Critical を含む) を見つけたこと、防御エージェントの仕組み「Cyber Shield」(6,000 万ポンド)、新しい「NERV センター」(7,000 万ポンド) の計画も示した。NCSC の Richard Horne 長官は、経営者に「安上がりな IT」をやめるよう求めた。
- **なぜ重要か**: 政府機関が、AI による脆弱性発見を防御側でも本格的に使い始めている。国内の能動的サイバー防御 (下の国内セクション) の議論と比べて読むとよい (評価)。
- 出典: [The Register](https://www.theregister.com/security/2026/11/03/britain-on-notice-ai-powered-ransomware-attacks-to-arrive-by-2028/5307200) / [SecurityWeek](https://www.securityweek.com/uk-cyber-chief-says-the-uk-will-face-ai-cyberattacks-on-critical-infrastructure-by-2028/)

### [2026-11-03] Cloudflare、重大な脆弱性の情報をまとめるフィード「Zero Wire」を Cloudflare Radar に開設
- **何が起きたか**: Cloudflare は、重大な脆弱性ごとに、平易な説明、調べるべき組織、推奨される対応などをまとめたブリーフィングを、Radar のセキュリティのセクションで公開し始めた。「AI で重大な脆弱性の発見の量と速度が変わっている」ことを理由に挙げている。
- **なぜ重要か**: CDN/WAF のベンダーは、実際の攻撃の通信を見られる立場にある。ベンダーの advisory と並べて、悪用の観測の一次情報として使えるかを見極めたい (評価)。
- 出典: [Cloudflare Blog](https://blog.cloudflare.com/zero-wire/)

### [2026-11-02〜03] NATO CCDCOE の演習「Crossed Swords 2026」、AI エージェントと OpenAI の Daybreak を初めて導入
- **何が起きたか**: エストニアのタリンで 11/2 に始まり、11/6 まで実施。40 か国超から 250 人超が参加し、サイバー作戦の計画と物理的な軍事行動の連携を訓練している。今回、AI エージェントと OpenAI Daybreak を取り入れた。
- **なぜ重要か**: 攻撃的なサイバー作戦の訓練に、商用の AI が公式に組み込まれた。AI ベンダーの利用規約と軍事利用の線引きにも関わる (評価)。
- 出典: [SecurityWeek](https://www.securityweek.com/natos-crossed-swords-exercise-brings-ai-agents-into-cyber-operations-training/)

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-11-02 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先
> KEV: 11/4 時点で該当なし。EPSS: 下表の CVE はほとんどがまだ算出されていない (取得できたものは併記)。

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-44267 / GHSA-33r5-xmm8-v6x5 | Elo (式言語) 1.0.1 未満、JS バックエンド | CWE-94 / 9.8 | 平文の Elo 式で `constructor` を普通の識別子として受け付け、`member_access` がメタプロパティを拒否しない → `.constructor.constructor` から JS の `Function` に届く → ブラウザやホストの Node で任意コード実行 | [diff](https://github.com/enspirit/elo/commit/2136da1f64eec8ebf99890d3100be9394534b842) | 未認証入力 (playground が自動実行) / 9.8 |
| CVE-2026-44266 / GHSA-7w38-ggh5-v542 | Elo 1.0.1 未満、Ruby バックエンド | CWE-116, 94 / 9.8 | 文字列リテラルを Ruby のダブルクォート文字列に埋め込むときに `#` をエスケープしない → `#{...}` の式展開が実行される → Ruby コードとバッククォートによるシェル実行 | [diff](https://github.com/enspirit/elo/commit/51b869963fbe445c18328714a7ccfbd76b21ba38) | 9.8 / コード生成系の共通バグ |
| CVE-2026-121392 / GHSA-jq25-3374-4262 | FreeRDP 3.32.2 未満 | CWE-295 / 9.1 | `tls_verify_certificate()` が、SAN があって一致しないのに CN にフォールバックし、IP リテラルを DNS 名として照合する → 信頼された CA の証明書を持つ MITM がサーバーの本人確認を回避 → RDP のキー入力・画面・クリップボードを傍受 | [advisory](https://github.com/FreeRDP/FreeRDP/security/advisories/GHSA-jq25-3374-4262) (commit 不明) | 仕様由来 (RFC 6125) で水平伝播しやすい |
| CVE-2026-106803 | Kamailio 6.1.3 / 6.1.4 `ims_registrar_pcscf` | CWE-121 / 9.8 | 細工した `application/reginfo+xml` の NOTIFY を `process_contact()` が処理するとき、alias パラメーターの port を長さを確かめずに 5 バイトのスタックバッファーにコピー → 未認証でスタック破壊 → P-CSCF の DoS | [diff](https://github.com/kamailio/kamailio/commit/21261436492f0014930e804e20586e3833bb91b9) | 未認証 / PoC (gist) 公開 / EPSS 0.0029 |
| CVE-2026-120442 | ape-volo-admin 3.6.1 未満 (.NET) | CWE-1394 / 9.3 | `appsettings.json` に JWT の署名鍵がハードコード → 攻撃者がオフラインで `jti` を初期管理者の ID にしたトークンを署名 → 未認証で管理 API を完全に操作 | [diff](https://github.com/xianhc/ape-volo-admin/commit/938f7ec58047f0c63123dc155d6a033910f00933) | 未認証 / EPSS 0.0048 |
| CVE-2026-112917 | Docker Desktop for Windows (WSL2 バックエンド) 4.98.0 未満、WSL 3.0.3 未満 | CWE-424 / 9.2 | seccomp の既定のプロファイルは `socket(AF_VSOCK)` を拒否するが、32 ビットの `socketcall` 多重化システムコールを見落とす → 非特権コンテナが AF_VSOCK でホスト側のサービスに到達 → ログイン中のユーザーが読める Windows のファイルを露出 | [release notes](https://docs.docker.com/desktop/release-notes/#4980) / [WSL 3.0.3](https://github.com/microsoft/WSL/releases/tag/3.0.3) (commit 不明) | コンテナ脱出系 / seccomp の典型的な抜け |
| CVE-2026-120091 | Temporal Server (auto-scaled-workers の k8s プロバイダー、修正版 1.31.5 / 1.32.2) | CWE-78, 863 / 8.7 | k8s プロバイダーが Kubernetes クライアントの設定を、運用者の設定ではなく呼び出し側のリクエストから組み立てる (exec 型の認証プラグインを指定可能) → read ロールしかない利用者でも `ValidateWorkerDeploymentVersionComputeConfig` から到達 → Worker Service のホストで任意コマンド実行 | [PR](https://github.com/temporalio/temporal-auto-scaled-workers/pull/165) | 低権限の認証済みユーザーから RCE |
| CVE-2026-121419 / GHSA-pgh9-49q4-hqcx | SurrealDB 3.1.0〜3.3.0 未満 | CWE-269 / 8.6 | MCP の `BoundSubject` の指紋を、ユーザーごとの ID ではなくアクセス方法の名前で作る → 同じアクセス方法の低権限トークンと被害者の `mcp-session-id` があれば → セッションを乗っ取り、被害者の権限で MCP ツールを実行 | [advisory](https://github.com/surrealdb/surrealdb/security/advisories/GHSA-pgh9-49q4-hqcx) (commit 不明) | MCP の認可 / 水平伝播 |
| CVE-2026-120313 / GHSA-5mm5-4mh4-6gm6 | Network-AI 5.15.5 未満 (Node) | CWE-22 / 8.7 | `InputSanitizer.sanitizePath()` が、区切り文字を付けない `startsWith(base)` で判定 → `/sandbox-evil/...` のように接頭辞を共有する兄弟ディレクトリが通る → サンドボックスの外のファイルを読み書き | [advisory](https://github.com/Jovancoding/Network-AI/security/advisories/GHSA-5mm5-4mh4-6gm6) (commit 不明) | 古典的なバグクラス / grep で横展開可 |
| CVE-2026-121448 / GHSA-q2vc-4qcx-2vm6 | Dockhand 1.0.54 未満 | CWE-22 / 8.7 | スタック名の検査がデコードの前、パスの解決が 2 回デコードしたあと → `%252e%252e` が `/api/stacks/[name]/env/raw` を通る → スタックの外の `.env` を読む・上書きする・削除する | [advisory](https://github.com/Finsys/dockhand/security/advisories/GHSA-q2vc-4qcx-2vm6) (commit 不明) | 秘密情報の露出 / 二重デコード |
| CVE-2026-121559 / GHSA-c46f-4v9j-5gpc | GLPI 10.0.0〜10.0.28 未満、11.0.0〜11.0.10 未満 | CWE-269 / 8.6 | `User::getCloneRelations()` が `Profile_User` と `Group_User` の割り当てを権限確認なしで複製 → Technician が Super-Admin のアカウントを新しいログイン名で複製 → 攻撃者が操作できる Super-Admin ができる | [diff](https://github.com/glpi-project/glpi/commit/10a827c8c1868a0a65ab977d30878ff16547d9a7) | 広く使われる ITSM / 権限昇格 |
| CVE-2026-119741 | rsync 3.5.1 以前 (デーモン) | CWE-407 / 8.7 | 送信側の `hash_search()` (match.c) で、弱いチェックサムだけ衝突させ強いチェックサムは一致しない値を受信側が送る → 連続するオフセットごとに強いチェックサムの計算を無制限に繰り返す → 公開モジュールから未認証で CPU を枯渇 | [diff](https://github.com/RsyncProject/rsync/commit/a7404a9a633cff28ee1602f328b9c3fa69cdbd04) | 未認証 DoS / ミラーサーバー |

### 今日の CVE 所感
- **「検査する値」と「実際に使う値」がずれるパスの問題が続いた**: Dockhand は二重デコード (`%252e`)、Network-AI は区切りなしの `startsWith`。前号の @fastify/http-proxy (デコード済みのパラメーターの差し込み、`\` の正規化) と同じ系統。Node/TS のコードベースでは `startsWith(` と `path.resolve` / `decodeURIComponent` の組み合わせを grep するだけで候補が拾える。
- **式言語・コード生成器のエスケープ漏れ**: Elo の 2 件は、JS では `constructor` のメタプロパティ、Ruby では `#{}` の式展開という、**出力先の言語ごとに違う「危険な構文」**を見落としていた。複数の言語を出力する no-code 系の式エンジンや、テンプレートからコードを生成するツール (SQL、Python、Ruby 向け) に同じ仮説を当てられる。
- **TLS の名前照合 (FreeRDP)**: 「SAN があるときは CN を見ない」「IP は iPAddress の SAN とだけ照合する」は RFC 6125 の基本だが、独自に実装した照合では今でも壊れている。RDP/VNC クライアント、組み込みの HTTP クライアント、IoT の SDK で同じテストケース (CN だけ一致、SAN の DNS 名に IP を入れた証明書) を試す価値がある。
- **MCP の認可は「誰のセッションか」の結び付けが弱い**: SurrealDB の `BoundSubject` の問題は、MCP のセッション ID とユーザー ID の結び付けを「アクセス方法」の単位で作ってしまったもの。MCP サーバーを内蔵する DB や SaaS では、`mcp-session-id` を別のユーザーのトークンで使い回せるかを、診断の定番の確認項目にしてよい。
- **seccomp の多重化システムコール (Docker Desktop)**: `socketcall` / `ipc` のような 32 ビットの多重化システムコールは、`socket` を拒否するフィルターの抜けとして昔から知られている。独自の seccomp プロファイルを持つサンドボックス (CI ランナー、AI のコード実行環境) で、x32/ia32 の ABI が閉じられているかを確認したい。
- 他に、SolarWinds Dameware の認証後のコマンド注入 (CVE-2026-28336、CVSS 9.9、[advisory](https://www.solarwinds.com/trust-center/security-advisories/CVE-2026-28336)) と、Control Web Panel (CWP) の loopback API 系の 7 件 (VulnCheck が採番、未認証で root の API に届くもの CVE-2026-77877 を含む) は、修正コミットがないので表から外したが、ホスティング事業者の診断では優先度が高い。

## 日本国内のセキュリティ動向

> 11/3 (文化の日) を挟むため、一次情報は 11/2 (月) の公表に集中し、11/3〜4 朝の新規の公表はほぼなかった。11/2 の大型の漏えい (アララ、ノジマ、@cosme、サントリー、セガ フェイブ、丸井など) は前号で扱ったので、本号は続報と、前号で拾えなかった分を中心にまとめた。ScanNetSecurity の 11/2 の記事の多くは 10/19〜26 の公表をまとめたもので、採用範囲より古いため外した。

### 国内インシデント・事故

#### [2026-11-02] [続報] NTT データの社債購入者向けの特典サービス「STdirectServices」、不正アクセスを受けた委託先は Securitize Japan と判明
- **前回 (11/2〜3 の楽天証券・丸井などの公表) から変わった点**: NTT データは 11/2、日経クロステックの取材に対し、不正アクセスを受けたシステムの委託先が Securitize Japan (セキュリタイズジャパン) であることを認めた。STdirectServices は、社債の購入者に特典を付ける業務を支援するサービスで、Securitize のシステムを使っていた。楽天証券をはじめ、複数の証券会社と社債の発行会社に影響が広がっている。マイナビニュースは、影響を受けた企業の一覧をまとめている。
- **なぜ重要か**: 丸井 (最大 9,086 人) や楽天証券 (362 件) など、ばらばらに公表されていた漏えいが、1 つの再委託先でつながった。デジタル社債・セキュリティトークンの周辺は、発行会社 → 証券会社 → 支援サービス → 基盤事業者と委託の層が深い。委託先の監査で、どの層までをセキュリティ評価の対象にしているかを確認したい (評価)。
- 出典: [日経クロステック](https://xtech.nikkei.com/atcl/nxt/column/18/00001/12147/) / [マイナビニュース](https://news.mynavi.jp/techplus/article/20261102-5242219/)

#### [2026-11-02] [続報] GMO インターネットグループ、2024 年に子会社から脆弱性を指摘されたあと、対策後の再診断をしていなかった。自社の AI 診断をグループに適用したのは事件の後
- **前回 (11/2 の熊谷代表の会見) から変わった点**: 日経クロステックによると、GMO は会見で、セキュリティを経営の柱の 1 つとして強化してきたと強調したが、2024 年に子会社 (前号の会見ではイエラエ) からサービスの脆弱性を指摘されたあと、対策後の再診断を行っていなかった。自社の AI 診断をグループ全体に適用したのは、今回の事件のあとだった。日経は 11/3 に、150 社を傘下に持つ複雑な統治体制が、防御の後手につながったとも報じている。
- **なぜ重要か**: 「指摘 → 修正 → 再診断で修正を確認」の最後の工程が抜けていた。診断を提供する側としては、報告書の納品で終わらせず、再診断を契約や社内ルールに組み込む必要性を示す事例 (評価)。
- 出典: [日経クロステック (再診断)](https://xtech.nikkei.com/atcl/nxt/column/18/00001/12148/) / [日本経済新聞 (統治体制)](https://www.nikkei.com/article/DGXZQOUC0219F0S6A101C2000000/)

#### [2026-11-02] グッドスマイルカンパニーの公式ショップに不正アクセス。管理者権限を奪われ、決済ページで入力されたカード情報 2,800 人分が窃取されたおそれ
- **何が起きたか**:
  - フィギュアやホビー商品のグッドスマイルカンパニーによると、10/23 06:00 に保守委託先から連絡があり発覚し、サイトを閉鎖した。
  - ログの分析で、10/19 15 時過ぎ〜10/22 23 時ごろに、サイトの管理情報に複数回アクセスされていた。10/28 18 時半過ぎには、不正なプログラムが置かれていたことも分かった。システムの一部の脆弱性を悪用され、管理者権限を不正に取得されたという。
  - 10/21 13:55〜10/23 07:00 に、クレジットカード決済のページで入力された 2,800 人分の名義、番号、有効期限、セキュリティコードが盗まれたおそれがある。
- **なぜ重要か**: 管理者権限の奪取から決済ページの改ざん (スキミング) までが 2 日弱。国内の EC での決済ページの改ざんは、PCI DSS v4 の 6.4.3 / 11.6.1 (決済ページのスクリプトの管理と改ざん検知) が求める対策がまだ行き渡っていないことを示している (評価)。
- 出典: [Security NEXT](https://www.security-next.com/191996)

#### [2026-11-02] ニコニコレンタカー、アプリでの運転免許証の画像の事前登録を廃止し、保存していた画像を全削除。「サイバー攻撃の増加を受けて」
- **何が起きたか**: ニコニコレンタカーを展開するレンタス (横浜市港北区) は、公式アプリ「ニコパス」の免許証画像の事前登録機能を廃止した (公表は 10/27、ITmedia の報道は 11/2)。今後は利用当日に店舗で免許証を提示する。預かっていた画像はすべて削除した。10/27 時点で漏えいは確認していない。旧版 (Ver.2.56.0 以前) には登録画面が残る場合があるが、画像は保存しないという。
- **なぜ重要か**: タイムズカーで 9 月に本人確認書類の画像 約 160 万アカウント分が漏えいし、パーク 24 が 10 月末までに画像を全削除すると発表したことに続く動き。「持たないデータは漏れない」というデータ最小化が、事業の判断として選ばれ始めた (評価)。
- 出典: [ITmedia](https://www.itmedia.co.jp/news/article/2611/02/2000002786/)

### 国内の注意喚起・ガイドライン・政策

#### [2026-11-04] 日経クロステック特集「能動的サイバー防御が始動」。根拠法は 10/1 施行、GMO の要請で注目
- **何が起きたか**: 日経クロステックは 11/4 のカバーストーリーで、攻撃の兆候を事前に把握し、被害を未然に防ぐ能動的サイバー防御 (ACD) を特集した。根拠法は 2026 年 10 月 1 日に施行され、官民連携で基幹インフラ事業者のシステムをより主体的に守る法制度が整った。基幹インフラ事業者だけでなく、そのサプライチェーンを担う企業も取り組みが避けられないとしている。高市首相は 10/26 のサイバーセキュリティの関係閣僚会議で、ACD の活用に言及した。GMO インターネットグループが政府に発動を要請したことで、注目が集まっているという。
- **なぜ重要か**: 「インフラ事業者の話」と思われていた ACD が、委託先・サプライチェーンの企業にも報告や協力の義務として波及する。診断やペンテストの事業者にとっては、対象の事業者の要件 (インシデント報告、資産の把握) に合わせた診断の需要が増える (評価)。記事の大半は有料会員向けで、本文の詳細は未確認。
- 出典: [日経クロステック](https://xtech.nikkei.com/atcl/nxt/column/18/03795/102800005/)

#### [2026-11-02] NTT グループ 4 社、経営トップがサイバーリスクを議論する招待制のコミュニティ「Security Trust Forum (STF)」を発足
- **何が起きたか**: NTT、NTT データ、NTT ドコモビジネス、NTT セキュリティ・ジャパンは 11/2、企業の経営者がサイバーセキュリティを経営課題として議論し、実体験や経営判断の知見を共有する「Security Trust Forum」を発足すると発表した。招待制・有償の会員制で、事務局は NTT セキュリティ・ジャパン。活動は、年 2 回の経営者向け勉強会、年 3 回のセキュリティリーダー向けの会合など。
- **なぜ重要か**: 同じ日に NTT データの委託先の漏えいの続報が出ており、皮肉な巡り合わせになった。大型の漏えいが続くなかで、経営層向けの情報共有の場が業界団体以外にも増えている (評価)。
- 出典: [マイナビニュース](https://news.mynavi.jp/techplus/article/20261102-5242036/)

#### [2026-11-02] QNAP、PHP の脆弱性「PHP2Shell」(CVE-2026-109618 / 109619) に対応する修正版を順次提供。NDR 製品「QNE ADRA」は準備中
- **何が起きたか**: Security NEXT によると、QNAP は QTS、QuTS hero、QuTScloud、TVR OS などの OS と、Notes Station 3、QVR Surveillance 向けの更新を用意した。脅威を検出する NDR 機能を持つ ADRA デバイスの OS「QNE ADRA」1.0.7 以前も影響を受け、修正版を準備中。未修正の機器はインターネットに公開せず、信頼できるネットワークからのアクセスに限るよう求めた。Container Station 上のコンテナやサードパーティ製アプリについても、個別に確認するよう呼びかけている。
- **なぜ重要か**: 国内の中小企業や自治体で広く使われる NAS が、PHP 本体の脆弱性の影響を受ける。セキュリティ製品 (NDR) の修正が後回しになっている点は皮肉 (評価)。IPA の PHP2Shell の注意喚起 (前号までに掲載) と合わせて確認したい。
- 出典: [Security NEXT](https://www.security-next.com/192277)

### 国内製品の脆弱性 (JVN)

> JVN の 11/2 の新規公開 (JVN#23328936 Core Temp、JVNVU#90141693 Siemens) は前号で掲載済み。11/3〜4 朝の新規公開は確認できなかった。JVN iPedia (JVNDB) は 10/30 からサービス停止中で、RSS も空。そのため、本号では国内で普及している製品のベンダー公表を代わりに挙げる。

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| 2026-11-02 (報道) | CVE-2026-109618 / CVE-2026-109619 (JVN 掲載なし) | QNAP QTS / QuTS hero / QuTScloud / TVR OS / QNE ADRA 1.0.7 以前 ほか | PHP 本体の「PHP2Shell」(メモリ破壊・UAF) の影響を受ける。OS とアプリの修正版を順次提供、QNE ADRA は準備中 | コード実行・情報漏えい (詳細は QNAP の advisory) | [Security NEXT](https://www.security-next.com/192277) |
| 2026-11-02 (報道) | CVE 番号の記載なし (JVN 掲載なし) | WordPress 7.1.4 未満 (国内の CMS で多数利用) | 10/28 のセキュリティリリース。アップグレード処理での遠隔コード実行と、ブロックのマークアップやプライバシーデータの削除要求を使う格納型 XSS 複数を修正 | RCE / XSS | [Security NEXT](https://www.security-next.com/192262) |

- **評価**: JVN iPedia が止まっている間は、国内ベンダーの PSIRT の公表を直接見に行く必要がある。前号までの取得失敗の記録のとおり、エレコム、パナソニック、富士通、トレンドマイクロの PSIRT はプロキシ経由で取得できないことが多く、取りこぼしの恐れがある。

### 国内コミュニティ・研究・イベント

#### [2026-11-04] piyokango 氏のコラム (日経クロステック): パナソニックで、禁止された生成 AI に約 33.4 万人分の個人情報がアップロードされた件ほか
- **何が起きたか**: 今週のコラムは 3 件を取り上げた。パナソニック オペレーショナルエクセレンスが 10/23 に公表した件では、子会社のパナソニック デジタルと進めていた人事情報システムの導入プロジェクトで、メンバーが社内ルールに違反し、利用を禁止している外部の生成 AI サービスに、従業員約 7.5 万人、元従業員約 17.8 万人、従業員の家族などの計約 33.4 万人分の情報を含むデータをアップロードしていた。外部からの不正アクセスではない。ほかに、自治体向けの情報配信サービスへの不正アクセスと、不動産投資サイト「楽待」の不正ログインを取り上げている。
- **なぜ重要か**: 「生成 AI の利用禁止」というルールだけでは、データの持ち出しを止められない例。前述の Google の学校向けの例のように、AI が業務ツールに入り込むほど、DLP やアップロードの技術的な制御が必要になる (評価)。
- 出典: [日経クロステック (piyokango)](https://xtech.nikkei.com/atcl/nxt/column/18/00598/011300388/)

#### [2026-11-03] Zenn「php2shell は悪用済み? CVSS は 10.0? 食い違う 4 つの論点を一次情報で答え合わせ」
- **何が起きたか**: 筆者は、PHP 本体の未認証 RCE 2 件 (CVE-2026-109618 / 109619) について、悪用の有無、深刻度、影響バージョン、修正版の公開時刻の 4 点が記事ごとに食い違っていたため、一次情報で確かめ直した。きっかけは、Claude Code に調査担当を 5 つ立てて分担させたところ、4 点すべてで報告が食い違ったことだという。技術的な中身は GMO Flatt Security と piyolog の解説に譲っている。
- **なぜ重要か**: AI に調べさせると、二次情報の食い違いがそのまま増幅される。CVE を追う側としては、「一次情報の確認先」を論点ごとに持っておくことが、AI の時代ほど重要になる (評価)。本ダイジェストの作り方にも直接当てはまる。
- 出典: [Zenn](https://zenn.dev/hoshiorange/articles/37-php2shell-ai-research-trap)

#### [2026-11-03] Zenn「個人開発アプリ 276 サイトのセキュリティヘッダーを調べたら、CSP を設定していたのは 15% だった」
- **何が起きたか**: 個人開発のプラットフォーム IDEAVALU の運営者が、掲載作品の作り手のサイト 276 件を 10/29 に外形だけで調べた (レスポンスヘッダー、TLS、SPF/DMARC/CAA、security.txt、公開 JS の中の秘密鍵らしい文字列。ポートスキャンや攻撃の試行はしていない)。独自ドメイン 216 件では、SPF が 54%、拒否か隔離の DMARC が 15%、CAA が 7%。TLS 1.3 や HTTPS へのリダイレクトなど、ホスティングが自動で設定する項目はほぼ揃っていた。
- **なぜ重要か**: 「ホスティングの既定値で守られる部分」と「自分で書かないと入らない部分 (CSP、DMARC)」の差がはっきり出た。Vercel や Next.js の個人開発・小規模 SaaS の診断で、最初に見るべき項目の目安になる (評価)。
- 出典: [Zenn](https://zenn.dev/ideavalu/articles/d92382705ff902)

#### [2026-11-02] INTERNET Watch のインタビュー: 森井名誉教授「既知の脆弱性を対策すれば、AI が大きな脅威とは言いがたい」「個人情報漏えいの被害は何年も続く」
- **何が起きたか**: INTERNET Watch は 11/2、サイバー攻撃の現状について森井名誉教授へのインタビューを掲載した。見出しで、既知の脆弱性の対策ができていれば AI は大きな脅威とは言いがたいこと、個人情報の漏えいの被害は何年も続くことを挙げている。
- **なぜ重要か**: AI による攻撃の高度化が強調される一方で、実際の国内の大型漏えい (GMO の再診断の欠落など) は、既知の問題の放置が原因の例が多い。本号の Microsoft の分析 (悪用されるのは全 CVE の約 0.5%) とも同じ方向の指摘 (評価)。本文の詳細は未確認で、見出しの範囲で紹介した。
- 出典: [INTERNET Watch](https://internet.watch.impress.co.jp/docs/interview/2152894.html)

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 58 (RSS/Atom 53 本 + NVD API + CISA KEV JSON + EPSS API + arXiv API + 個別記事)
- 採用件数: AI技術=12 / AIセキュリティ=9 / セキュリティ=18 / CVE=12 / 国内インシデント=4 / 国内政策=3 / JVN=2 (ベンダー公表で代替) / 国内コミュニティ=4
- 除外理由内訳: 古すぎ=約 15 (ScanNetSecurity 11/2 の 10/19〜26 公表まとめ 11 件、ヤマハ NWR100 (10/28 公表)、Revolut の記事など) / 重複=約 30 (Android TV の XCPE ボットネット、Barracuda、BTCPay、Synology、Linux TCP の CVE-2026-98432、欧州スーパーの冷蔵設備、Ivanti、ARTEX の続報、Claude のゲーム複製ルール、CWE-bench 初出、pgAdmin、外務省、アイリスオーヤマ、トラスト・ログイン、楽天証券、クラブツーリズム、ワールド/RAGTAG、IPA の相談窓口、国家サイバー統括室の特設サイトなど) / 日付不明・一次未確認=約 4 (OpenAI の "security sprint" 記事本文、Dark Reading の Microsoft AI リスク報告の論評、Revolut の Claude 置き換え記事の URL、自治体向け情報配信サービスの事案の一次情報)
- 取得失敗ソース:
  - openai.com の記事本文: 取得できず (本文が空)。RSS のタイトルと日付、Help Net Security で代替した。
  - darkreading.com の記事本文: 本文が空 (JS 描画)。BleepingComputer で代替した。
  - codezine.jp: Bot 対策のチャレンジページで本文を取得できず。見出しのみ確認し、不採用にした。
  - 日経クロステック / 日経: 有料会員向けで、本文の冒頭のみ確認した。
  - jvndb.jvn.jp の RSS: サービス停止中で空 (パースエラー)。
  - mbsd.jp、venturebeat.com、trendmicro.com (ja_jp) の RSS: パースエラー。
  - piyolog: 10/30 以降の更新なし。Security NEXT / ScanNetSecurity の RSS は 11/2 で更新が止まっている (祝日)。
  - JPCERT/CC、個人情報保護委員会、国家サイバー統括室、警察庁: 11/2〜4 の新規の公表を確認できなかった。
  - Google の WebSearch: 11 月の国内の事案について、古い結果しか返らなかった。各サイトの RSS と一覧ページの直接取得で代替した。
  - EPSS: 新しい CVE の多くはまだ算出されていない。
  - GitHub の advisory 本体 (api.github.com): 前号までと同じく、リポジトリのスコープ制限で使えないため、NVD の参照 URL から GHSA を特定した。

</details>
