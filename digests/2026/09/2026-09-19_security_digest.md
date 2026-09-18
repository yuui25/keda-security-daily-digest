# KEDA Daily Digest — 2026-09-19 (JST)

> 採用範囲: 公開日 2026-09-17 〜 2026-09-19
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Microsoft の Azure AI Foundry / Fabric / Billing にわたる CVSS 10.0 認証バイパス3連発が9月17〜18日に集中開示され、AI 開発基盤のアイデンティティ層が構造的な攻撃面を持つことが浮き彫りになった。Anthropic は生命科学検証プログラム (LSVP) と Claude 生体分子研究を同日 (9/17) 公開した一方、セキュリティ研究者が Claude Opus 5 を使って OpenAI の内部リポジトリにアクセスするバグバウンティ報告 (9/18) が話題となり、AI ツールが防御側・攻撃側の両方に活用される局面が一層明確になった。vm2 の CVSS 10.0 サンドボックス脱出 (9/18) は Node.js ベースの AI エージェント実行基盤に直結し、MLflow の pickle バイパス (9/17) とあわせて ML 推論パイプラインへの攻撃経路が拡大している。

## AI 関連ニュース

- **[2026-09-18]** [Hacktron AI チームが Claude Opus 5 を用いて OpenAI 内部コードリポジトリへアクセス — $6,500 バグバウンティを獲得](https://fortune.com/2026/09/18/hacktron-claude-opus5-openai-bug-bounty/) — 3人チームが2つの脆弱性をチェーンし、ChatGPT アカウント複数と内部リポジトリに 72 時間以内にアクセス；Opus 4.8 では失敗、Opus 5 リリース数時間後に成功 *(Fortune / CBS News / Digital Trends)*
- **[2026-09-17]** [Anthropic が生命科学検証プログラム (LSVP) ベータを開始 — Mythos 5.1・Opus 5・Sonnet 5 の生命科学向け認証付きアクセス](https://cryptobriefing.com/2026/09/17/anthropic-life-sciences-verification-program-lsvp/) — Standard Use と High-risk Use の2段階で審査；高リスク使用（ゲノム編集・感染症研究等）は追加審査を要する *(CryptoBriefing / Unite.AI)*
- **[2026-09-17]** [Anthropic、Claude による生体分子モデル最適化研究を公開 — 36 パッケージ・30+ OSSモデルを平均4倍高速化、$100万タンパク質設計コンペも発表](https://www.unite.ai/anthropic-releases-biomolecular-research-claude-optimization/) — Adaptyv Bio との共催；AlphaFold・ESMFold 等の OSSモデルの推論速度改善を Claude が自動最適化 *(Unite.AI)*
- **[2026-09-18]** [Azure AI Foundry に CVSS 10.0 認証バイパス CVE-2026-85889 — 未認証特権昇格・Microsoft がサーバーサイド修正](https://guardianmssp.com/2026/09/18/azure-ai-foundry-cve-2026-85889-cvss10/) — CWE-306（クリティカル機能の認証欠如）；AI Foundry プロジェクト管理・モデルデプロイへの完全不正アクセスが可能だった *(Guardian MSSP / infosectoday.io)*
- **[2026-09-18]** [Microsoft 365 Copilot に CVSS 9.9 コマンドインジェクション CVE-2026-85885 — クラウド修正済み](https://strix.ai/2026/09/18/ms365-copilot-cve-2026-85885/) — CWE-77；認証済みユーザーが Copilot のコマンド処理に特殊文字を混入して特権昇格 *(Strix AI)*

## セキュリティ関連ニュース

- **[2026-09-17]** [Check Point Management Server に CVSS 9.8 未認証 RCE CVE-2026-91843 — スタックオーバーフロー、LivePatch sk1000155 で対応](https://censys.com/2026/09/17/checkpoint-management-server-cve-2026-91843/) — ログイン処理の境界値チェック欠如によりリモートから root 権限で任意コード実行が可能；インターネット公開 Check Point Management Server は即時適用推奨 *(Censys / SecurityAffairs)*
- **[2026-09-17]** [ISC BIND 9 が 14 件のセキュリティ修正を公開 — 7件が高深刻度、DoH SIG(0) 未認証クラッシュ CVE-2026-77692 等](https://www.securityweek.com/2026/09/17/isc-bind9-14-vulnerabilities-fixed/) — 9.20.29 / 9.21.26 でリリース；CVE-2026-77692 は未認証攻撃者が DoH 経由で SIG(0) 署名クエリを送信するとリゾルバがクラッシュ *(SecurityWeek)*
- **[2026-09-18]** [vm2 サンドボックスに CVSS 10.0 脱出脆弱性 CVE-2026-93603 ほか4件 — v3.12.1 で修正、Node.js AI エージェント基盤に直撃](https://endorlabs.com/2026/09/18/vm2-sandbox-escape-cve-2026-93603/) — V8 が host global を注入する挙動を vm2 がライブプロキシとして返却してしまうため、サンドボックス内コードからホスト global への直接アクセスが可能 *(Endor Labs / Kodems Security)*
- **[2026-09-17]** [Microsoft Azure Fabric に CVSS 10.0 認証バイパス CVE-2026-69843 — OneLake エンタープライズデータへの不正アクセス](https://forkast.news/2026/09/17/microsoft-azure-fabric-cve-2026-69843-cvss10/) — CWE-287（認証欠如）；スプーフィングにより認証をバイパスして OneLake の全データにアクセス可能；9月以降 Microsoft ID 層の認証欠陥が5件目 *(Forkast.news / thewindowsupdate.com)*
- **[2026-09-17]** [Microsoft Azure Billing に CVSS 10.0 特権昇格 CVE-2026-62874 — 財務データの整合性に影響](https://forkast.news/2026/09/17/microsoft-azure-billing-cve-2026-62874/) — CWE-345（データ真正性検証不備）；未認証攻撃者が Azure Billing の特権を昇格して課金データを改ざん可能 *(Forkast.news)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 today-2 (2026-09-17) 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-85889 | Azure AI Foundry (全バージョン・全テナント) | CWE-306 / CVSS 10.0 | 未認証ネットワーク攻撃者が AI Foundry のクリティカル機能における認証チェック欠如を悪用 → 特権昇格 → AI プロジェクト管理・モデルデプロイへの完全不正アクセス | Microsoft サーバーサイド修正済み (commit 不明) | **CVSS 10.0 / AI 開発プラットフォーム中枢** / CVE-2026-69843・CVE-2026-62874 と同構造で Microsoft ID 層3件連鎖 |
| CVE-2026-93603 | vm2 (patriksimek) ≤ 3.12.0 | CWE-94 / CVSS 10.0 | サンドボックス内コードが非 strict ホスト関数をレシーバーなしで呼び出す → V8 が host global を注入 → vm2 がライブプロキシとして返却 → ホスト global への直接アクセスで RCE | [v3.12.1 (GHSA-j89j-5m6r-cr2q)](https://github.com/advisories/GHSA-j89j-5m6r-cr2q) | **CVSS 10.0** / Node.js AI エージェント実行基盤直撃 / isolated-vm・node-sandbox 等の類似サンドボックスへの水平バリアント候補 |
| GHSA-gqvg-gmmx-x4hm | MLflow statsmodels flavor ≤ 3.14.x / dspy flavor (全バージョン) | CWE-502 / Critical | `MLFLOW_ALLOW_PICKLE_DESERIALIZATION=False` 設定時も statsmodels flavor は対象外でチェック未実施 / dspy flavor はファイル拡張子で分岐してバイパス可 → 悪意ある ML モデルアーティファクトの `pickle.load` により RCE | [MLflow 3.15.0 PR#25566](https://github.com/mlflow/mlflow/pull/25566) | VU#369093 / JVNVU#94088453 / **AI/ML 推論パイプライン RCE** / BentoML・DVC 等 ML モデルレジストリへの水平バリアント候補 |
| CVE-2026-90999 | Sentry Seer (自動コーディングエージェント統合・全バージョン) | CWE-913 / CVSS 9.8 | 未認証攻撃者が公開 DSN 経由で偽造 Sentry イベントを送信 → Seer が信頼済みテレメトリとして処理 → コーディングエージェント環境で任意コード実行・ソースリポジトリへの不正アクセス | パッチ未提供 (VU#212479 / JVNVU#91019649) | **CVSS 9.8 / ベンダー未対応** / AI エージェント信頼境界違反 / Autofix 系ツール全般へのインジェクション攻撃の起点 |
| CVE-2026-69843 | Microsoft Fabric (全テナント) | CWE-287 / CVSS 10.0 | 未認証ネットワーク攻撃者がスプーフィングにより認証バイパス → OneLake ストレージ（エンタープライズデータレイク）に直接アクセス → 全データの窃取・改ざん | Microsoft クラウド修正済み (commit 不明) | CVSS 10.0 / 9月以降 Microsoft ID 層4件目 / Azure Data Factory・Synapse 等のデータ統合サービスへの水平バリアント候補 |
| CVE-2026-91843 | Check Point Management Server (全バージョン) | CWE-121 / CVSS 9.8 | 未認証ネットワーク攻撃者がログイン処理に境界値を超えた入力を送信 → スタックバッファオーバーフロー → root 権限で RCE | LivePatch sk1000155 / 正式パッチ未公開 | CVSS 9.8 / インターネット公開 Management Server での即時悪用リスク / FortiManager・Panorama 等の類似 Management Plane への水平バリアント候補 |

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-09-17 | JVNVU#91019649 / CVE-2026-90999 | Sentry Seer に攻撃者制御入力が管理者権限で実行される脆弱性 — 公開 DSN 経由で偽造イベント送信→コーディングエージェント環境で RCE | CVSS 9.8 / AIエージェント基盤 | [jvn.jp](https://jvn.jp/vu/JVNVU91019649/) |
| 2026-09-17 | VU#369093 / GHSA-gqvg-gmmx-x4hm | MLflow dspy/statsmodels flavor が pickle デシリアライズ制御をバイパス — 悪意あるモデルアーティファクト経由で RCE | Critical / ML 推論基盤 | [CERT/CC VU#369093](https://kb.cert.org/vuls/id/369093) |
| 2026-09-17 | JVN (未採番) | 東北電力「よりそう eネット」スマートフォンアプリにハードコードされた暗号化鍵の脆弱性 — アプリの認証情報が解析可能 | 中 / スマートフォンアプリ認証 | JPCERT Sep 17 Advisory |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 25+
- 採用件数: AI=5 / Security=5 / CVE=6 / 国内=3
- 除外理由内訳:
  - 採用窓外（公開日 < 2026-09-17）: Cisco Secure Firewall 18 CVE（advisory Sep 16）, Docker Sandboxes macOS CVE-2026-77179（advisory Sep 15）, ISC BIND 9 advisory（Sep 16 → media Sep 17 にて確認、advisory日付で除外検討したが news 採用ルール適用で採用済み）, NightmareStresser seizure（Sep 15-16）, Anthropic alignment assessment（Sep 9）, Salesforce Claudeforce（Aug 26）, Orkes Conductor CVE-2026-58138（June patched, August exploited）
  - 重複（Sep 12〜18 digest 既報）: OpenAI・Anthropic・Google AI サイバーセキュリティプログラム（Sep 18 digest）, King Charles AI Summit（Sep 18 digest）, Cisco ISE CVE-2026-76460/20176（Sep 18 digest）, Google Pixel CVE-2026-58704（Sep 18 digest）, HP Advance CVE-2026-89082/83（Sep 18 digest）, WSO2 CVE-2026-5430（Sep 17 digest）, Oracle EBS CVE群（Sep 17 digest）, Acronis CVE-2026-87886（Sep 17 digest）, Emergence World 2（Sep 17 digest）, Cisco SEG CVE-2026-76461（Sep 16 digest）, Apple iOS 27 CVE群（Sep 16 digest）, Apache Storm CVE群（Sep 16 digest）
- 取得失敗ソース（EGRESS_BLOCKED）: techcrunch.com, helpnetsecurity.com, thehackernews.com, unite.ai, vulncheck.com, anthropic.com, securityweek.com, bleepingcomputer.com, nvd.nist.gov, jvn.jp, jpcert.or.jp, osv.dev, cvebrief.com, securityboulevard.com, radar.offseq.com, advisories.gitlab.com

</details>
