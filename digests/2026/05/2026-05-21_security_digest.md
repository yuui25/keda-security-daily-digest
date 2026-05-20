# KEDA Daily Digest — 2026-05-21 (JST)

> 採用範囲: 公開日 2026-05-19 〜 2026-05-21
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Google I/O 2026 Developer Keynote（5月20日）で Antigravity 2.0・CodeMender・Secure AI Framework 2.0 など防御指向の AI ツール群が発表され、開発者エコシステムへのセキュリティ統合が加速した。一方、TeamPCP（UNC6780）による Nx Console VS Code 拡張機能 18.95.0 のサプライチェーン攻撃が GitHub 内部リポジトリ 3,800件の流出に繋がり、Claude Code 認証情報を標的にした初の既知サプライチェーン攻撃として警戒を要する。Drupal は PostgreSQL 環境で未認証 SQL インジェクション → RCE が可能な CVE-2026-9082 の緊急パッチをリリースしており、速やかな適用が必要。

## AI 関連ニュース

- **[2026-05-19]** [Anthropic × KPMG 戦略的グローバルアライアンス締結 — 27.6万人の従業員に Claude を全面展開し Digital Gateway に統合](https://www.anthropic.com/news/anthropic-kpmg) — KPMG が税務・PE・コンサルティング業務に Claude を組み込む。KPMG Blaze は Claude Code を活用した IT モダナイゼーション支援製品として PE クライアント向けに提供開始。 *(Anthropic)*

- **[2026-05-19]** [Google I/O 2026: AI Ultra $100/月サブスクリプション新設 — Gemini アプリ使用量 5倍・優先 Antigravity アクセス・20TB ストレージを提供、上位プランは $250 → $200 に値下げ](https://blog.google/products-and-platforms/products/google-one/google-ai-subscriptions/) — 開発者・テクニカルリード向け中間層として AI Ultra を追加。Gemini Spark Beta の先行アクセス権も付与。 *(Google Blog)*

- **[2026-05-20]** [Google I/O Developer Keynote: Antigravity 2.0 発表 — コーディング環境からマルチエージェントオーケストレーション基盤へ進化、CLI/SDK/エンタープライズ統合を追加](https://thenewstack.io/google-io-antigravity-codemender-ai-agentic/) — サブエージェントを複数並列起動して複雑ワークフローを分散実行。ターミナルサンドボックス・クレデンシャルマスキング・強化 Git ポリシーをセキュリティビルトインで提供。 *(The New Stack)*

- **[2026-05-20]** [Google I/O Developer Keynote: CodeMender + Secure AI Framework 2.0 発表 — AI が 6 ヶ月で OSS に 72 件のセキュリティ修正をアップストリーム、AI VRP で最大 $30,000 の報奨金](https://thenewstack.io/google-io-antigravity-codemender-ai-agentic/) — DeepMind 開発の CodeMender が脆弱性検出から自律修正まで対応。SAIF 2.0 は自律 AI エージェントのセキュリティ標準を更新し、業界横断ガイドラインとして公開。 *(The New Stack)*

- **[2026-05-20]** [Google I/O: SynthID を Search・Chrome に拡張 — OpenAI・Kakao・Eleven Labs も採用し業界横断的な AI コンテンツ検証基盤が拡大](https://developers.googleblog.com/all-the-news-from-the-google-io-2026-developer-keynote/) — AI 生成コンテンツの透かし・検証技術 SynthID が主要製品に統合。Gemini Omni の生成動画にも透かし付与を標準化。 *(Google Developers Blog)*

- **[2026-05-19]** [Nx Console 18.95.0 供給チェーン攻撃 — AI コーディングアシスタント Claude Code の認証情報を標的にした初の既知サプライチェーン攻撃](https://thehackernews.com/2026/05/compromised-nx-console-18950-targeted.html) — TeamPCP（UNC6780）が Claude Code 設定ファイル・GitHub・AWS・1Password の認証情報を一括窃取。AI 開発ツールチェーンが組織侵入の新経路として初めて標的化。 *(The Hacker News)*

- **[2026-05-20]** [Google I/O 2026 Cloud: Vertex AI・Agent Builder・Gemini API に新機能一斉公開 — エンタープライズ向け AI セキュリティ保護機能も強化](https://cloud.google.com/blog/products/ai-machine-learning/innovations-from-google-io-26-on-google-cloud) — Project Mariner 刷新・Gemini 2.0 API 拡張・Agent Platform 新機能が Google Cloud 上で即日提供開始。 *(Google Cloud Blog)*

## セキュリティ関連ニュース

- **[2026-05-19]** [Nx Console VS Code 18.95.0 がサプライチェーン攻撃媒体に — 孤立コミット経由で 498KB 認証情報窃取ペイロードを配布、潜在的影響は 6,000 インストール超](https://thehackernews.com/2026/05/compromised-nx-console-18950-targeted.html) — コントリビューターの盗難 GitHub トークンを悪用し公式 nrwl/nx リポジトリに不可視の孤立コミットを挿入。VS Code Marketplace 18分・Open VSX 36分間稼働し GitHub / npm / AWS / Kubernetes / 1Password / Claude Code の認証情報を多段階窃取。 *(The Hacker News)*

- **[2026-05-20]** [GitHub 内部リポジトリ 3,800件が TeamPCP に流出 — Nx Console 攻撃を起点に社員端末が侵害、ソースコード・トークン・SSH 鍵が外部へ](https://www.cryptotimes.io/2026/05/20/github-investigates-internal-repo-breach-tied-to-poisoned-vs-code-task/) — 侵害した認証情報で GitHub 社員の開発環境に侵入し内部リポジトリ・AWS キー・Kubernetes シークレットを抽出。TeamPCP は地下フォーラムで 5 万ドルで売り出し中。 *(CryptoTimes)*

- **[2026-05-19]** [[続報] Grafana Labs GitHub 侵害調査 — 顧客本番環境への侵入なし確認、$50K 身代金要求を FBI 勧告に従い拒否](https://www.securityweek.com/grafana-confirms-breach-after-hackers-claim-they-stole-data/) — ソースコード・内部リポジトリの窃取は確認されたが顧客本番システムへの侵入証拠なし。TanStack npm 供給チェーン攻撃（TeamPCP）が起点と判明。 *(SecurityWeek)*

- **[2026-05-20]** [Drupal SA-CORE-2026-004 緊急リリース — CVE-2026-9082 は PostgreSQL サイトで未認証 SQL インジェクション → 情報漏洩・権限昇格・RCE に到達可能](https://www.drupal.org/sa-core-2026-004) — データベース抽象化 API のサニタイズ欠如により匿名ユーザが任意 SQL を送信可能。Drupal Steward WAF は即日保護済み。10.5.10 / 10.6.4 / 11.2.5 / 11.3.1 への更新を推奨。 *(Drupal.org)*

- **[2026-05-20]** [Microsoft が YellowKey (CVE-2026-45585) 軽減策公開 — 物理アクセスで BitLocker 暗号化ドライブを復号できる PoC に対し TPM+PIN 移行を案内](https://www.helpnetsecurity.com/2026/05/20/yellowkey-bitlocker-mitigation-cve-2026-45585/) — Windows 11 / Server 2025 の事前起動回復シーケンスの信頼仮定を悪用するゼロデイ（CVSS 6.8）。完全パッチは未提供、TPM+PIN 設定への切替が当面の対策。 *(Help Net Security)*

- **[2026-05-19]** [Trapdoor — Android 455 アプリ・1日 6.59 億入札リクエストの大規模マルバタイジング作戦を HUMAN Satori が解明、延べ 2,400 万ダウンロード](https://thehackernews.com/2026/05/trapdoor-android-ad-fraud-scheme-hit.html) — 不正アプリが内部 WebView を非表示で起動し広告インプレッションを詐取。インストール帰属 API を悪用してセキュリティ検査時は悪意ある動作を抑制。Google Play から全削除済み。 *(The Hacker News)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-05-19 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-9082 | Drupal core 10.5.x / 10.6.x / 11.2.x / 11.3.x (PostgreSQL 使用サイト) | CWE-89 / Highly Critical (20/25) | DB 抽象化 API でユーザ入力を PostgreSQL クエリに非サニタイズで渡す → 匿名ユーザが任意 SQLi → 情報漏洩・権限昇格・RCE | [SA-CORE-2026-004](https://www.drupal.org/sa-core-2026-004) (commit 不明) | 高 (政府・教育機関に多数の本番運用、即時パッチ適用推奨) |
| GHSA-c9j4-9m59-847w | Nx Console VS Code Extension 18.95.0 (nrwl/nx) | - / Critical | コントリビューター GitHub トークン盗難 → 公式リポジトリへの孤立コミット差込 → 拡張機能起動時に開発者 AWS / Claude Code / 1Password 等の認証情報を多段階窃取 | [GitHub Advisory](https://github.com/nrwl/nx-console/security/advisories/GHSA-c9j4-9m59-847w) | 最高 (AI コーディング環境が新攻撃面・GitHub 内部侵害起点) |
| CVE-2026-42097 | Sparx Pro Cloud Server ≤ 6.1 | CWE-89 / Critical | 認証エンドポイントで SQL パラメータが非サニタイズのまま DB クエリに渡る → SQL インジェクション → 認証バイパス | [CERT Polska advisory](https://cert.pl/en/posts/2026/05/CVE-2026-42096/) (commit 不明) | 高 (エンタープライズアーキテクチャ管理ツール) |
| CVE-2026-42099 | Sparx Pro Cloud Server ≤ 6.1 | - / Critical | DB 通信処理の競合状態で不正クラスが読み込まれる → サーバサイド RCE | [CERT Polska advisory](https://cert.pl/en/posts/2026/05/CVE-2026-42096/) (commit 不明) | 高 (競合状態 RCE バリアント水平探索起点) |
| CVE-2026-42096 | Sparx Pro Cloud Server ≤ 6.1 | CWE-284 / Critical | 低権限ユーザが DB 通信 API のパーミッションチェックをバイパス → DB ユーザ権限で任意 SQL を実行 | [CERT Polska advisory](https://cert.pl/en/posts/2026/05/CVE-2026-42096/) (commit 不明) | 高 |
| CVE-2026-35506 | ELECOM 無線 LAN ルータ / AP 複数機種 | CWE-78 / 未公表 | ping_ip_addr パラメータが未サニタイズのまま OS コマンドに渡る → 認証済みユーザによる任意コマンド実行 | [JVN#03037325](https://jvn.jp/en/jp/JVN03037325/) | 中 (国内製品・ルータ系 OS CMDi バリアント検索起点) |
| CVE-2026-40621 | ELECOM 無線 LAN ルータ / AP 複数機種 | CWE-288 / 未公表 | 特定 URL への認証チェック欠如 → 未認証で管理機能にアクセス可能 | [JVN#03037325](https://jvn.jp/en/jp/JVN03037325/) | 中 |

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-05-19 | **JVN#03037325** (CVE-2026-35506 / CVE-2026-42062 / CVE-2026-40621 / CVE-2026-25107 / CVE-2026-42948 / CVE-2026-42950 / CVE-2026-42961) | ELECOM 製無線 LAN ルータ・アクセスポイント 7 脆弱性: OS コマンドインジェクション 2件・認証欠如 1件・ハードコード暗号鍵 1件・XSS・CSRF 他 3件 | 未公表 / 機器設定変更・任意コマンド実行の恐れ | [JVN#03037325](https://jvn.jp/en/jp/JVN03037325/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 28
- 採用件数: AI=7 / Security=6 / CVE=7 / 国内=1
- 除外理由内訳: 古すぎ (2026-05-18以前)=23 / 重複 (前ダイジェスト収録済)=12 / 日付不明=3
- 主な除外理由の詳細:
  - **期間外 (2026-05-18以前)**: OpenAI Daybreak (2026-05-11) / Google AI 2FA ゼロデイ・GTIG (2026-05-11) / Palo Alto Defender's Guide May 2026 Update (2026-05-13) / Universal Robots CVE-2026-8153 CISA ICS (2026-05-14) / 2026: Year of AI-Assisted Attacks (2026-05-04) / Windows MiniPlasma PoC (2026-05-17・05-19ダイジェスト収録済) / Mandiant M-Trends 2026 (2026-05-07頃) / Microsoft MDASH (2026-05-12)
  - **前ダイジェスト重複**: Google I/O 2026 メインキーノート全般 (Gemini 3.5 Flash / Omni / Spark / AI Mode / Ask YouTube / Gemini for Science / Project Mariner / XR Glasses → 2026-05-20ダイジェスト収録済) / SEPPMail CVE群 CVE-2026-2743 等 (2026-05-20) / DirtyDecrypt CVE-2026-31635 (2026-05-20) / SOGo CVE-2026-8851 (2026-05-20) / Grafana GitHub 侵害初報 (2026-05-18 → 2026-05-19ダイジェスト収録済) / NYC Health+Hospitals (2026-05-20) / CVE-2026-42945 NGINX (前週) / Anthropic Code with Claude London (2026-05-20) / OpenAI Malta (2026-05-20)
  - **日付不明/情報不足**: CometBFT GHSA-r3r4-g7hq-pq4f (日付確認不可) / Kuadrant mcp-gateway GHSA-g53w-w6mj-hrpp (日付確認不可) / RoboForm Android JVN (CVE番号確認不可)
- 取得失敗ソース: jvn.jp (HTTP 403), nvd.nist.gov (HTTP 403), drupal.org (直接アクセス不可) — 内容確認は検索スニペット・第三者ミラーサイト (cypro.se / thomasharris6.wordpress.com 等) の URL 日付パターンで実施

</details>
