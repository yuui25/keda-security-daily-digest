# KEDA Daily Digest — 2026-07-04 (JST)

> 採用範囲: 公開日 2026-07-02 〜 2026-07-04 (JST)
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Sysdig が完全自律型 AI エージェントによるランサムウェア「JADEPUFFER」の初事例を公開し、LLM が侵入から暗号化・痕跡消去まで人間不在で完遂できることが実証された。セキュリティ面では Google + FBI が 200 万台の住宅用デバイスを動員した NetNut プロキシボットネットを解体、FortiBleed キャンペーンが INC・Lynx の二大 RaaS に直結することが SOCRadar の調査で明らかになった。CVE はクラウド AI インフラへの侵害が目立ち、Azure OpenAI (CVE-2026-45499) と Microsoft Entra Provisioning (CVE-2026-57100) に SSRF 経由の権限昇格がそれぞれ Microsoft のサイレントパッチで修正された。

---

## AI 関連ニュース

- **[2026-07-02]** [JADEPUFFER: LLM エージェントが侵入・横展開・暗号化・消去を完全自律で実行した初の「アジェンティック型ランサムウェア」を Sysdig が公開](https://www.sysdig.com/blog/jadepuffer-agentic-ransomware-for-automated-database-extortion) — Langflow CVE-2025-3248 から初期侵入後、Nacos バックドア構成を 31 秒で自律修正し lateral move → Salesforce DB 全 1,342 件を暗号化・ランサムノートを残したが鍵は保存されず回復不能; LLM が失敗時に即座に代替手順を推論・実行した最初の文書化事例 *(Sysdig TRT / The Register / SC Media)*

- **[2026-07-03]** [Anthropic、Claude Enterprise に管理者分析・モデルエンタイトルメント・支出アラートを追加](https://claude.com/blog/giving-admins-more-visibility-and-control-over-claude-usage-and-spend) — グループ/ユーザー単位コスト可視化・SCIM グループ連動のモデルアクセス制御・組織支出限度の 75%/90% 到達時自動通知を管理者コンソールと Analytics API から提供; AI 利用可視化ガバナンスを強化 *(Anthropic / Finout)*

- **[2026-07-02]** [Cognizant + OpenAI、GPT-5.5 活用のフロンティア AI サイバー防御サービスを発表](https://news.cognizant.com/2026-07-02-Cognizant-and-OpenAI-bring-frontier-AI-cyber-defense-from-vulnerability-discovery-to-validated-fixes) — OpenAI Daybreak Cyber Partner Program の一環; GPT-5.5 + Trusted Access for Cyber をセキュアコードレビュー・脅威モデリング・脆弱性検証・脅威ハンティング・インシデント対応に適用; Cognizant は自社環境で先行運用する「Client Zero」として動作確認済み *(Cognizant / The Fast Mode)*

- **[2026-07-02]** [Z.ai、GLM-5.2 搭載の無料エージェント型コーディング IDE「ZCode」を正式リリース](https://venturebeat.com/technology/z-ai-launches-zcode-to-challenge-cursor-claude-code-and-github-copilot-in-ai-coding) — Windows/macOS/Linux 対応のスタンドアロン IDE; BYOK で他社モデルも利用可; WeChat・Feishu・Telegram からリモートでタスク指示が可能; 有料 Coding Plan は Lite $16.20〜Max $144/月; Cursor・Claude Code・GitHub Copilot を直接競合として名指し *(VentureBeat / DevOps.com)*

- **[2026-07-03]** [THN「2026 年サイバーセキュリティ評価」: AI 脅威がトップ 3 独占 — 自己変異型マルウェア 55.9%・LLM データ漏洩 53.5%・AI 回避技術 52.5%](https://thehackernews.com/2026/07/2026-cybersecurity-assessment-gap.html) — 経営層の 58% が AI 利用の完全可視性を主張する一方で実務者は 45.9% にとどまり「認識と実態のギャップ」が顕在化; AI を組織全体で管理できている企業は 3 割未満と指摘 *(THN / CrowdStrike)*

- **[2026-07-02]** [ChocoPoC RAT: Sekoia + YesWeHack が脆弱性研究者を標的にした偽 GitHub CVE PoC リポジトリ 7 件の調査結果を公開](https://www.bleepingcomputer.com/news/security/new-chocopoc-malware-targets-researchers-via-trojanized-poc-exploits/) — FortiWeb / PAN-OS / Ivanti Sentry / Check Point VPN 等の人気 CVE を詐称した Python PoC に malicious dependency (skytext パッケージ) を隠蔽; Mapbox を C2 Dead Drop として使用し DNS-over-HTTPS でドメインフロンティング; ブラウザ認証情報・Cookie・ファイル窃取後シェルアクセスを付与; 発表時点で C2 稼働中 *(BleepingComputer / THN / Sekoia)*

---

## セキュリティ関連ニュース

- **[2026-07-02]** [SOCRadar、FortiBleed キャンペーンを INC + Lynx ランサムウェア RaaS に帰属 — 世界 150 カ国 430K 台の FortiGate が標的](https://thehackernews.com/2026/07/fortibleed-credential-theft-linked-to.html) — 脅威アクターのインフラが INC と Lynx の交渉パネルを同時に操作していることが確認され、資格情報窃取から直接ランサムウェア展開への経路が初めて実証; 200 以上の運用サーバー追加発見・~20 人の分業体制・12 件以上のランサムウェア展開 *(SOCRadar / THN / BleepingComputer)*

- **[2026-07-02]** [Medtronic が ShinyHunters 侵害による 380 万人への通知を開始 — AI 音声フィッシングで MFA バイパス → Okta SSO 経由で Salesforce に不正侵入](https://www.bleepingcomputer.com/news/security/medtronic-notifies-customers-impacted-by-shinyhunters-data-breach/) — 2026 年 4 月 13〜19 日の侵害; ShinyHunters が 900 万件超の個人・医療情報窃取を主張; AI 生成音声を使った vishing で IT ヘルプデスクを騙し MFA を迂回するという ShinyHunters の手口が再確認; 氏名・連絡先・SSN・健康情報が漏洩リスク *(BleepingComputer / SecurityWeek / The Register)*

- **[2026-07-03]** [Google + FBI が NetNut 住宅用プロキシボットネット (200 万台) を解体 — 1 週間で 316 の脅威クラスターが悪用](https://www.securityweek.com/google-fbi-disrupt-netnut-residential-proxy-network-powered-by-millions-of-devices/) — スマート TV・ストリーミング端末に SDK 形式でプリインストール or フリーアプリ経由で感染; サイバー犯罪グループ・国家関連グループの双方がパスワードスプレー・アカウント乗っ取り・コンテンツスクレイピングに使用; Lumen・Shadowserver も参加した IPIDEA ボットネット解体 (1 月) に続く作戦 *(The Register / SecurityWeek / Krebs on Security)*

- **[2026-07-02]** [ChocoPoC の注目点: 分析専用ターゲット (脆弱性研究者・ペンテスター) を狙った標的型サプライチェーン攻撃として業界に警告](https://gbhackers.com/chocopoc-campaign-abuses-github/) — PoC を実行した時点で Python 依存関係 `skytext` が実行; 研究者のローカル環境・SSH 鍵・`.env` ファイルが直接的な目標; 研究者に届いた PoC のリポジトリ名は最新ゼロデイ CVE に偽装 *(GBHackers / Sekoia / Undercode News)*

> ChocoPoC は AI セクションにも記載済みのため、技術詳細は AI セクション参照。

- **[2026-07-03]** [Scattered Spider メンバー 19 歳の Peter Stokes がフィンランドから米国へ身柄引き渡し — DOJ が Operation Riptide 継続を宣言](https://thehackernews.com/2026/07/19-year-old-scattered-spider-suspect.html) — 16 歳時から少なくとも 4 件の侵害; 2025 年 5 月にラグジュアリー宝飾店から $800 万のランサム要求; インターポール Red Notice に基づきフィンランドで逮捕後移送; Scattered Spider は 100 件超の侵入と $100M 超のランサム被害に関与 *(THN / DOJ / Decrypt)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-07-02 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-52830 | fast-mcp-telegram (pip) < 0.19.1 (Telegram MCP Server) | CWE-22 / **9.4** | HTTP Bearer トークンを検証せずセッションファイルパスに直接結合 → `../` によるパストラバーサルでデフォルト legacy セッションに偽装 → 任意ユーザーの Telegram セッション奪取 | [fast-mcp-telegram v0.19.1](https://github.com/leshchenko1979/fast-mcp-telegram/releases) | 2026-07-02 GHSA 公開 / CVSS 9.4 / MCP 経由 Telegram 自動化サービスの全セッションが漏洩リスク / Bearer token + path concat パターンは他 MCP サーバーへバリアントハント推奨 |
| CVE-2026-45499 | Azure OpenAI サービス (クラウドマネージド) | CWE-918 / **High** | Azure OpenAI バックエンドが認可された攻撃者からの細工リクエストを受け内部 metadata エンドポイントへ SSRF 発行 → テナント内権限昇格・AI ワークロード設定への横移動 | サービス側サイレントパッチ適用済 (顧客対応不要) | 2026-07-02 Microsoft 公表 / クラウドマネージド AI インフラの SSRF パターン / Azure AI Foundry・M365 Copilot の同種 SSRF への横展開バリアントハント推奨 (CVE-2026-35435 参照) |
| CVE-2026-57100 | Microsoft Entra Provisioning Service (SyncFabric) | CWE-918 / **High** | SyncFabric プロビジョニングエンジンが未検証の SSRF リクエストを受け付け → ディレクトリ認可ロジックを迂回して権限昇格 → クロステナント ID 侵害の可能性 | サービス側サイレントパッチ適用済 (顧客対応不要) | 2026-07-03 Microsoft 公表 / Entra ID 全テナントに自動適用済 / SaaS 型 IdP の SSRF → 権限昇格パターンは Okta・Ping Identity 等へバリアントハント推奨 |
| CVE-2026-53478 + CVE-2026-49814 + CVE-2026-49815 (DSA-2026-278) | Dell PowerProtect Data Domain v7.7.1.0〜8.7 / LTS2026 8.6.1.0 (バックアップアプライアンス) | High (3件) | バックアップ管理インターフェースの複数コンポーネントに入力検証不足 → 認証済み攻撃者が特権コマンドを実行またはデータを改ざん可能 | [DSA-2026-278 / DDOS 8.7.1 以降](https://www.dell.com/support/kbdoc/en-us/000481268/dsa-2026-278) | 2026-07-03 Dell 公表 / バックアップアプライアンスは RaaS の優先標的 / 最新 DDOS バージョンへの即時アップグレード推奨 (commit 詳細非公開) |

---

## 国内脆弱性・インシデント情報

> 2026-07-02〜07-04 (JST) 期間中、主要ソース (JPCERT/CC・IPA・JVN・Piyolog) で新規国内脆弱性・インシデント公表は確認できませんでした。

*参考: 直前採用窓内 (07-03 digest) に JVNVU#94872523 (Seiko SkyBridge OS コマンドインジェクション) 掲載済み。*

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| sysdig.com / theregister.com / scworld.com | JADEPUFFER 2026-07-02 確認 ✓ |
| news.cognizant.com / prnewswire.com | Cognizant + OpenAI GPT-5.5 2026-07-02 確認 ✓ |
| venturebeat.com / devops.com | Z.ai ZCode 2026-07-02 確認 ✓ |
| claude.com/blog / finout.io | Claude Enterprise analytics 2026-07-03 確認 ✓ |
| thehackernews.com (July 3) | 2026 Cybersecurity Assessment 2026-07-03 確認 ✓ |
| bleepingcomputer.com / sekoia.com | ChocoPoC 2026-07-02 広範報道確認 ✓ (Sekoia 一次公開 07-01) |
| socradar.io / thehackernews.com | FortiBleed → INC/Lynx 2026-07-02 確認 ✓ |
| bleepingcomputer.com / securityweek.com / theregister.com | Medtronic ShinyHunters 2026-07-02 確認 ✓ |
| theregister.com / securityweek.com / krebsonsecurity.com | NetNut botnet Google+FBI 2026-07-03 確認 ✓ |
| thehackernews.com / doj.gov | Scattered Spider 19-year-old 2026-07-01 DOJ 発表確認 ✓ (07-01 JST) |
| github.com/advisories (July 2-4 filter) | CVE-2026-52830 (fast-mcp-telegram) 取得 ✓ |
| windowsnews.ai / thehackerwire.com | CVE-2026-45499 (Azure OpenAI) 2026-07-02 確認 ✓ |
| windowsnews.ai / tenable.com | CVE-2026-57100 (Entra Provisioning) 2026-07-03 確認 ✓ |
| dell.com/support | DSA-2026-278 (PowerProtect Data Domain) 2026-07-03 確認 ✓ |
| jvn.jp / jpcert.or.jp / ipa.go.jp | 403 / 新規アドバイザリなし |
| nvd.nist.gov / cisa.gov/kev | 403 — WebSearch 代替; July 3-4 新規 KEV 追加なし (SharePoint 07-01 追加は前日 digest 掲載済み) |

### 集計サマリ

- **巡回ソース数**: 22+
- **採用件数**: AI=6 / Security=5 / CVE=4 グループ (6 CVE) / 国内=0
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-07-02 より前): OpenAI Jalapeño chip (06-24)、Squidbleed CVE-2026-47729 (06-23)、Splunk CVE-2026-20253 KEV 追加 (06-18)、Exchange CVE-2026-42897 パッチ (06-09)、ShinyHunters Medtronic 攻撃自体 (04-13〜19)、Scattered Spider 逮捕 DOJ 発表が 07-01 (today-3 = window 外だが 07-02 THN 報道あり → 採用)
  - 重複 (excluded_set 一致): SharePoint CVE-2026-45659 KEV (07-03 digest)、Citrix NetScaler batch (07-03)、Adobe ColdFusion CVSS 10.0 (07-03)、Rancher Fleet CVE-2026-44935 (07-03)、Mautic SSTI batch (07-03)、Apify MCP CVE-2026-50143 (07-03)、Centrifugo CVE-2026-49998 (07-03)、DuneSlide CVE-2026-50548/50549 (07-02 digest)、Kemp LoadMaster CVE-2026-8037 (07-02)、Langflow campaign (07-02)、SurrealDB batch (07-02)、repomix CVE-2026-49987 (07-02)、Claude Sonnet 5 (07-02)、Microsoft Teams AI bot policy (07-01 発表)、White House AI EO 30-day milestone (07-02 digest)
  - 日付不明: 0件
  - 詳細不十分: Autodesk Fusion Desktop MCP 拡張脆弱性 (CYFIRMA July 3 report 記載だが CVE 番号・CVSS 未確認)、Kong Konnect MCP Server CVE-2026-13341 (詳細検索ヒットなし)
- **取得失敗ソース**: thehackernews.com (403)、bleepingcomputer.com (403)、sekoia.com (403)、venturebeat.com (403)、sysdig.com (403)、jvn.jp (403)、nvd.nist.gov (403)、cisa.gov (403) — 全て WebSearch スニペット・ミラーサイトで代替確認済み

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-06-27 〜 2026-07-03) の全 CVE/GHSA/URL を除外済み。*
