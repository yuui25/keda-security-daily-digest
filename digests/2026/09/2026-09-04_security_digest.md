# KEDA Daily Digest — 2026-09-04 (JST)

> 採用範囲: 公開日 2026-09-02 〜 2026-09-04
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

CISA が 2026-09-02 に 7 件を一括で KEV カタログに追加（Kestra CVSS 10.0 / Sangoma Switchvox CVSS 9.3 / LiteLLM MCP CVSS 8.8 / Starlette CVSS 6.5）。うち Sangoma Switchvox は当日から野外で逆シェル展開が確認、Kestra も 6 月下旬から継続的に攻撃を受けていたことが判明した。AI インフラ面では ChatGPT・Claude・Grok が Azure East US 障害によって 2026-09-03 に一斉ダウン、Gemini (Google Cloud) のみ生き残り AI プロバイダー間のクラウド集中リスクが公に可視化された。Anthropic は EFS（Enterprise Frontier Safeguards）を正式ローンチし、Palo Alto Networks が AI 駆動セキュリティ自動化企業 Console を $500M で取得した。

## AI 関連ニュース

- **[2026-09-02]** [Anthropic、Claude の Enterprise Frontier Safeguards (EFS) を正式ローンチ — 金融・医療 100 社以上と共同設計したゼロデータ保持 + 顧客クラウドへのログ保持機能](https://www.anthropic.com/news/enterprise-frontier-safeguards) — Claude の応答を Anthropic サーバーに保存せず、誤用検知ログを顧客 AWS S3/Azure Blob/GCS バケットへ顧客暗号鍵で書き込む。Anthropic は内容を参照せず検知ロジックのみ実行。Claude Code・Claude Enterprise・Amazon Bedrock・Google Agent Platform・Microsoft Foundry で利用可、無償提供予定。 *(Anthropic / MarkTechPost / QZ)*

- **[2026-09-02]** [Meta、Muse Spark 1.3 を発表 — アジェンティック・コーディングモデルが Muse Spark 1.2 比ツール呼び出し 20% 減・トークン消費 25% 減を実現](https://www.bloomberg.com/news/articles/2026-09-02/meta-releases-more-powerful-ai-model-edging-closer-to-rivals) — Zuckerberg CEO が「コーディングとエージェント作業での最大のジャンプ」と評価。MRCR 512K〜1M コンテキストで 98.1% 達成。コントリビューター向けオープンウェイトリリースも発表。 *(Bloomberg / VentureBeat)*

- **[2026-09-02]** [Alibaba Qwen、Qwen3.8-Max-0902 をリリース — Artificial Analysis Agentic Index で首位（55.4）、GPT-5.6・Claude Opus 5 を上回る初の中国モデル](https://llmgateway.io/timeline) — 旗艦 Qwen3.8-Flash-Next（08-28 既報）とは異なる Max ライン（フル MoE バックボーン + 強化 RL）。エージェンティックタスクで OpenAI・Anthropic フロンティアモデルを初めて上回ったと報告。 *(Artificial Analysis / Qwen Team)*

- **[2026-09-02]** [Palo Alto Networks、AI 自律セキュリティオペレーション企業 Console を $500M で買収 — Thrive Capital バック・創業 2 年のスタートアップ、2026 年 7 番目の買収](https://techcrunch.com/2026/09/02/palo-alto-networks-paid-500m-for-thrive-backed-console-sources-say/) — Console は AI エージェントで IT ヘルプデスクと SOC の自律対応を実現するプラットフォーム。Cortex に統合し AI 駆動の優先順位付け・調査・修正を機械速度で実行可能とする。2024 年創業・シードとシリーズ A 合計 $29M 調達済み。 *(TechCrunch / paloaltonetworks.com)*

- **[2026-09-03]** [Microsoft AI、MAI-Transcribe-2 を発表 — 音声認識モデルが OpenAI・Google・ElevenLabs を精度・速度・価格で凌駕、$0.10/時間（旧版比 72% 削減）](https://venturebeat.com/infrastructure/microsoft-ais-mai-transcribe-2-undercuts-openai-google-and-elevenlabs-on-price-and-speed) — Microsoft AI 独自モデルとして 5 ヶ月ぶりの大型音声アップデート。企業向けコールセンター転写・会議文字起こしシーンで即座に実運用可能。API 経由で Azure AI Services から提供。 *(VentureBeat)*

- **[2026-09-03]** [Anthropic、Claude Commerce Agents を Apache-2.0 でリリース — 小売・旅行・通信・エンタメ向けショッピング/マーチャントエージェントのリファレンス実装](https://www.marktechpost.com/2026/09/03/anthropic-released-claude-commerce-agents-an-apache-2-0-blueprint-for-shopping-and-merchant-agents-across-retail-travel-telecom-and-entertainment/) — 商用グレードのマルチターン購買エージェントを実装するためのブループリントを OSS 公開。カタログ検索・カート操作・決済代行フローを含む 4 業種対応の実行可能な垂直スターターキット。 *(MarkTechPost / Anthropic GitHub)*

- **[2026-09-03]** [Hugging Face + NVIDIA、Open Data for Agents を公開 — 5 万件超のタスク軌跡を含む AI エージェント訓練標準データセット、ベンチマーク精度 40% 向上](https://artificialintelligenceherald.com/ai-news-today) — 自律 AI エージェントのトレーニングデータの質・形式の標準化を目的とし、多様なドメインの軌跡を収録。エージェント評価インフラ整備が本格化する中、業界全体の基盤として位置付け。 *(AI Herald / NVIDIA / Hugging Face)*

- **[2026-09-03]** [ChatGPT・Claude・Grok が 07:57 PT より一斉ダウン — Azure East US 障害起因と判明、Gemini (Google Cloud) のみ稼働維持し AI 集中リスクが顕在化](https://www.bloomberg.com/news/articles/2026-09-03/openai-anthropic-spacexai-hit-by-service-outages-for-ai-models) — OpenAI は約 24 分後に ChatGPT 復旧。Claude は Sonnet 系が先行回復、Opus 4.8/5 が遅延。Grok (xAI) も Azure 共有インフラで影響を受けた。Downdetector では米国内 ChatGPT 35,000 件超・Claude 1,400 件・Grok 1,200 件の報告。名目上独立した 3 プロバイダーが同一クラウド障害ドメインを共有することが公的に確認された最初の事例。 *(Bloomberg / AI Governance Institute / Gizmodo / 9to5Google)*

## セキュリティ関連ニュース

- **[2026-09-02]** [CISA、7 件の既知悪用脆弱性を一括で KEV カタログに追加 — Kestra・Sangoma・Starlette・LiteLLM MCP 等、連邦機関の修正期限は最短で 9/5](https://www.cisa.gov/news-events/alerts/2026/09/02/cisa-adds-seven-known-exploited-vulnerabilities-catalog) — 新規 4 件（CVE-2026-49869・CVE-2026-9586・CVE-2026-48710・CVE-2026-59822）に加え、SonicWall SMA1000 2 件・JFrog Artifactory 1 件（いずれも既報）を収録。Kestra と Sangoma は 9/5 期限、LiteLLM・Starlette は 9/16 期限で連邦 FCEB 機関に修正義務。 *(CISA / The Hacker News)*

- **[2026-09-02]** [Sangoma Switchvox CVE-2026-9586 の野外悪用が当日から開始 — 未認証 SQLi 経由で逆シェルを投下、インターネット公開インスタンス約 4,000 台](https://www.helpnetsecurity.com/2026/09/02/exploitation-of-sangoma-switchvox-flaw-underway-cve-2026-9586/) — ハニーポットが 8/30 から探索を検知、9/2 KEV 追加後に攻撃が急増。攻撃者は `/pa` エンドポイントへ XML ペイロードを送信し逆シェル投下後にプロセス列挙を実行。Horizon3 が攻撃者 IP (176.65.148.184) と IOC を公開。修正版 8.4.0.2 は 7/14 既リリース済み。 *(Help Net Security / Horizon3 / BleepingComputer)*

- **[2026-09-02]** [Kestra CVE-2026-49869: 6 月下旬から逆シェル・暗号通貨マイナー投下が続くと Microsoft が報告、CISA KEV 追加で修正期限 9/5 に設定](https://thehackernews.com/2026/09/cisa-adds-seven-exploited-flaws-as.html) — 認証フィルターのサフィックスマッチバイパスにより未認証で任意ワークフローを実行可能。攻撃者は Docker コンテナ環境偵察・防御回避・マイナー投下・データ収集を連続実施。スクリプト実行プラグインがデフォルト有効のため直ちに root RCE に到達。 *(The Hacker News / Microsoft / CISA)*

- **[2026-09-02]** [Starlette CVE-2026-48710 が LiteLLM と連鎖して CVSS 10.0 の未認証 RCE チェーンを構成 — AI ゲートウェイとして広範利用の LiteLLM が主要ターゲット](https://www.rescana.com/post/active-exploitation-alert-cve-2026-42271-and-cve-2026-48710-unauthenticated-rce-in-litellm-ai-gateway-via-starlette-host) — Starlette の Host ヘッダー検証欠落（CVE-2026-48710）が LiteLLM の既存 RCE（CVE-2026-42271、KEV 6/9 追加済み）との認証バイパスチェーンを形成。資格情報なしで LiteLLM プロキシ上で任意コード実行可能。KEV 追加により攻撃が増加傾向。 *(rescana.com / Horizon3 / CISA)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 today-2 以降 / CISA KEV 追加（2026-09-02）/ 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-49869 / [GHSA-5vc5-wxxq-3fjx](https://github.com/kestra-io/kestra/security/advisories/GHSA-5vc5-wxxq-3fjx) | Kestra OSS ≤ 1.3.20 (LTS 1.0.x は ≤ 1.0.44) | CWE-288 / CVSS 10.0 | `AuthenticationFilter` が `/configs` のサフィックスマッチで Basic Auth を免除 → 任意 API パスが末尾 `/configs` を持てば認証をバイパス → 未認証で任意ワークフロー作成・スクリプトプラグイン経由で root OS コマンド実行 | [v1.3.21 / v1.0.45 release](https://github.com/kestra-io/kestra/releases) | KEV 2026-09-02 / 実エクスプロイト確認 (6月下旬〜) / CVSS 10.0 / 修正期限 9/5 |
| CVE-2026-9586 | Sangoma Switchvox SMB Edition 8.3 (build 104997) | CWE-89 / CVSS 9.3 | `/pa` エンドポイントが Polycom XML 本体の `PhoneIP` 値を認証なしで PostgreSQL クエリに文字列連結 → 任意 SQL 注入 → DB から認証情報取得・xp_cmdshell 相当のデータベース手続き経由で RCE | [v8.4.0.2 (2026-07-14 リリース)](https://sangoma.com/) (commit 不明) | KEV 2026-09-02 / 実エクスプロイト確認 (2026-08-30〜) / CVSS 9.3 / 逆シェル投下確認 / 修正期限 9/5 |
| CVE-2026-59822 | BerriAI LiteLLM < 1.84.0 | CWE-287 / CVSS 8.8 | MCP Streamable HTTP エンドポイントで LiteLLM キー検証失敗時に OAuth2 パススルーフォールバックが空の `UserAPIKeyAuth()` オブジェクトを返却 → 任意 Bearer トークンで認証済みセッションを確立 → 認証なしで MCP ツール実行 | [v1.84.0 release](https://github.com/BerriAI/litellm/releases/tag/v1.84.0) (commit 不明) | KEV 2026-09-02 / AI ゲートウェイ広範利用 / MCP エコシステムへのバリアント展開候補 / 修正期限 9/16 |
| CVE-2026-48710 | Kludex Starlette ≤ 1.0.0 | CWE-444 / CVSS 6.5 | `request.url` 構築時に HTTP `Host` ヘッダーを RFC 9112 に従って検証せず → `request.url.path` が実際のルーティングパスと乖離 → Starlette ベースミドルウェアのパスベース認証をバイパス (LiteLLM CVE-2026-42271 と連鎖して CVSS 10.0 の未認証 RCE チェーンを形成) | [v1.0.1 release](https://github.com/encode/starlette/releases/tag/1.0.1) | KEV 2026-09-02 / AI Gateway スタック共通ライブラリ / 同ライブラリ使用フレームワーク（FastAPI 等）への水平伝播要確認 / 修正期限 9/16 |
| CVE-2026-82918 | Keyence XG VisionTerminal / XG-X VisionTerminal (修正版以前) | CWE-611 / CVSS 5.5 | ユーザーが特定の細工済み設定ファイルを開くと XML 外部エンティティ参照が制限なく処理 → インストールシステム上の機密情報を外部エンドポイントに送信 | (commit 不明) [JVN 情報](https://jvn.jp/) | JPCERT/CC 2026-09-02 公開 / 産業用ビジョンシステム / ファイル受け渡し経路でのソーシャルエンジニアリング悪用リスク |

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-09-02 | CVE-2026-82918 | Keyence XG VisionTerminal / XG-X VisionTerminal の XML 外部エンティティ参照不適切制限 — 細工設定ファイルを開くとシステム上の機密情報が窃取される可能性 | CVSS 5.5 / Medium | [JVN](https://jvn.jp/) |
| 2026-09-03 | JVN#91715694 (CVE-2026-80253 / CVE-2026-80254) | ShizenBox2 (Shizen Connect) に物理アクセスで認証不要のブートローダーコマンド実行・他ユーザーパスワード変更が可能な複数の脆弱性 | CVSS 6.8 / Medium | [JVN#91715694](https://jvn.jp/jp/JVN91715694/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 25+（CISA, The Hacker News, Help Net Security, BleepingComputer, Horizon3, Bloomberg, MarkTechPost, VentureBeat, AI Weekly, AI Herald, AI Governance Institute, 9to5Google, Gizmodo, Tech Startups, QZ, Bloomberg, SecurityWeek, rescana.com, Sangoma, Kestra GitHub, LiteLLM GitHub, Starlette GitHub, JVN/JPCERT 各サイト）
- 採用件数: AI=8 / Security=4 / CVE=5 / 国内=2
- 除外理由内訳:
  - 重複 (excluded_set 該当): CVE-2026-82329 JFrog Artifactory KEV (09-02 digest済み), CVE-2026-83548/83549 SonicWall KEV (09-03 digest済み), OpenAI Astra Critical threshold (09-03 digest済み), AISLE curl CVEs (09-03 digest済み), SonicWall SMA1000 野外悪用 (09-03 digest済み), Microsoft Exchange CVE-2026-62911 22K インスタンス (09-03 digest済み), METR API key theft (09-03 digest済み), PaperCut 第3次パッチ (09-03 digest済み), Gemini 3.8 Flash Cyber (09-03 digest済み), Fable 5.1/Mythos 5.1 (09-03 digest済み), UNC3886 FireAnt (09-01 digest済み), Silver Fox ValleyRAT (09-01 digest済み), Novocure data breach (09-02 digest済み), Softaculous BGP hijack (09-02 digest済み)
  - 窓外（公開日 < 2026-09-02）: DHS HSIN/FIFA World Cup breach (2026-07-01), DeepSeek/Hermes Agent 460 targets (2026-08-03 Help Net Security), GPT-5.6-Cyber/Daybreak 拡張 (2026-08-10〜11), OpenAI GPT-Live 音声モデル (日付不明・未確認), AWS "What's Next" イベント (日付不確定), Data I/O ランサムウェア (2025年事案・FY2025 SEC 提出)
  - 日付不明・未確認: AWS "What's Next with AWS 2026" イベント詳細日付不確定のため除外
- 取得失敗ソース（EGRESS_BLOCKED）: thehackernews.com, bleepingcomputer.com, helpnetsecurity.com, aicybr.com, darkreading.com, techcrunch.com, anthropic.com, jvn.jp, jpcert.or.jp, ipa.go.jp, vulnerability.circl.lu, aidapted.ro, aiweekly.co（WebSearch スニペット・ミラーサイト経由で情報補完）

</details>
