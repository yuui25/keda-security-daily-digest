# KEDA Security Daily Digest — 2026-08-04

> 採用範囲: 2026-08-02〜2026-08-04 JST に公開された情報のみ掲載。過去 7 日分との重複を除外 ([続報] 表記を除く)。

---

## 本日のサマリ

Trump 政権が OpenAI・Anthropic・Google を White House に招集し、任意 AI 安全テストフレームワーク (政府が最大 30 日間フロンティアモデルへの早期アクセスを取得; 強制ライセンス不可) を議論予定と Bloomberg/CNBC が 8/3 報道。EU AI Act の GPAI プロバイダーへの執行権限 (Articles 51-56; 文書請求・モデル評価・最大 €15M/全世界売上 3% 罰金) が 8/2 に発効、EU が OpenAI・Anthropic の AI 侵害事案で独自調査を開始したとの報道も (8/2 Article 50 施行と別条項)。セキュリティ面では中国系未知脅威アクターが流出 DarkSword 完全チェーン iOS エクスプロイトキットで 100+ フィッシングサイトから GHOSTBLADE を配布するキャンペーンが 8/3 に公表、ShinyHunters が Entra 音声フィッシングで Brinks Home から 110 万件超の顧客データを窃取したことを同社が 8/2 に確認。N-able N-central の認証バイパス (CVE-2026-18577) は「初期パッチ迂回」として実エクスプロイトが確認され管理対象全エンドポイントへの横断侵害リスクが顕在化。CVE 面では Thermo Fisher Applied Biosystems の法科学 DNA 分析ファイルが改ざん検知不能になる CVSS v4.0:8.2 の欠陥 (CVE-2026-17583) が THN 8/3 に詳報、国内では Sharp ネットワークスキャナーツールの認証欠如 (CVE-2026-62416/JVNVU#92540957) が JVN に公表された。

---

## AI 関連ニュース

1. [2026-08-03] **White House AI Safety Meeting** — Trump 政権が OpenAI・Anthropic・Google の幹部を White House に招集し、任意 AI 安全テストフレームワークを議論予定。政府がフロンティアモデルへの最大 30 日間の早期アクセスを取得する枠組みで、強制ライセンスは含まれない。Cyber Director 室が主催し、NIST 安全評価基準との連携を検討。([Bloomberg](https://www.bloomberg.com/) (2026-08-03) / [CNBC](https://www.cnbc.com/) (2026-08-03) / CNN (2026-08-03))

2. [続報][2026-08-02] **EU AI Act GPAI 執行権限発動** — 欧州委員会の GPAI プロバイダーへの執行権限 (Articles 51-56: 文書請求・モデル評価・EU 市場アクセス制限・最大 €15M または全世界年間売上 3% 罰金) が 8/2 に発効。EU が OpenAI・Anthropic の AI サイバー侵害事案で独自調査を開始したとの報道あり (Article 50 透明性義務の 8/2 施行とは別条項)。([CNBC (2026-08-03)](https://www.cnbc.com/) / ComplianceHub.wiki (2026-08-02) / [続報: 2026-08-02 digest 掲載 (Article 50)])

3. [続報][2026-08-03] **Microsoft Project Perception パブリックプレビュー開始** — 7/27 発表から本格稼働へ移行。Microsoft Defender 内で Red Agent (侵害シミュレーション)・Blue Agent (防御自動化)・Green Agent (ガバナンス) の 3 エージェント体制が起動し、顧客環境での試用が開始。([WindowsForum (2026-08-03)](https://windowsforum.com/) / InsiderFinance (2026-08-03) / Microsoft Security (2026-08-03) / [続報: 2026-07-29 digest 掲載 (発表)])

---

## セキュリティ関連ニュース

1. [2026-08-02] **Brinks Home データ侵害確認** — ShinyHunters が 2026-07-13 に Microsoft Entra を標的とした音声フィッシング (ビッシング) で Brinks Home (北米最大の住宅セキュリティ会社) のネットワークに侵入。Salesforce "Contacts" オブジェクトから氏名・住所・電話番号・契約情報を含む 110 万件超の顧客データを窃取。Brinks Home が 8/2 に侵害を公式確認。([DataBreaches.net (2026-08-02)](https://www.databreaches.net/) / CyberSecurityNews (2026-08-02) / BleepingComputer)

2. [2026-08-02/03] **N-able N-central CVE-2026-18577 実エクスプロイト確認** — MSP 向けリモート管理プラットフォームで 2026.3 向け初期パッチ (CVE-2026-18556 対応) を迂回する新規攻撃経路が 8/2 に発見された。攻撃者は認証バイパス後に管理者権限を取得し、Take Control 機能で配下の全マネージドエンドポイントに到達、Cloudflare トンネルで永続化を確立。Huntress が「god-mode アクセス」として警告、8/2 時点で 55.6% の N-central インスタンスが未パッチ。N-able は 8/2 に hotfix 2026.3.1.7 をリリース。([N-able Blog (2026-08-02)](https://www.n-able.com/blog/) / [Help Net Security (2026-08-03)](https://www.helpnetsecurity.com/) / GBHackers / THN)

3. [2026-08-03] **DarkSword/GHOSTBLADE iOS キャンペーン** — 中国語話者系未知脅威アクターが流出した DarkSword 完全チェーン iOS エクスプロイトキット (Safari RCE → サンドボックス脱出 → カーネル権限昇格; 6 脆弱性使用) を使用し、100+ の偽 AWS コンソール・Apple ID ログインページから iOS デバイスに **GHOSTBLADE** マルウェア (キーチェーン・iCloud・Wi-Fi 認証情報・ファイル窃取後自己消去) を配布。インフラは香港中心だが日本・米欧にも展開。(THN (2026-08-03) / [GuardianMSSP (2026-08-03)](https://www.guardianmssp.com/) / BleepingComputer / Google GTIG)

4. [2026-08-03] **BTMOB RAT 地下エコシステム調査** — Flare が数千件の地下フォーラム投稿を分析し、Android フルデバイス乗っ取り型 RAT「BTMOB」の公式チャンネルとは別に、リセラーパネル・ソースコード販売・カスタム亜種・競合販売チャネルが乱立する分断エコシステムに進化していることを確認。MaaS (Malware-as-a-Service) としての商業化が深刻化。([BleepingComputer (2026-08-03)](https://www.bleepingcomputer.com/news/security/inside-the-underground-business-of-btmob-rat/) / Flare Research)

---

## 新規 CVE / Advisory

| CVE/GHSA | 製品・バージョン | CWE / CVSS | バグクラス (条件→シンク→結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-18577 | N-able N-central <2026.3.1.7 (クラウド/オンプレ) | CWE-288 / **8.2** (CVSS 4.0) | 未認証攻撃者が CVE-2026-18556 初期パッチを迂回する代替経路で認証バイパス → 管理者権限取得 → Take Control で配下全エンドポイントに到達 → Cloudflare トンネルで永続化 | N-central 2026.3.1.7 hotfix (2026-08-02); 野生悪用確認済み | 実エクスプロイト確認 / MSP プラットフォーム / 配下全クライアント端末への横断侵害 / 55.6% 未パッチ |
| CVE-2026-17583 | Thermo Fisher Applied Biosystems 3500/3500xL Data Collection ≤4.0.2 / 3730/3730xL ≤5.0.2 (Win) | CWE-345 (推定) / **8.2** (CVSS v4.0) | 攻撃者がソフトウェアロード前に .fsa/.hid 法科学 DNA 分析ファイルを改ざん → デジタル署名検証なし → 改ざんが分析結果に反映 → 法科学証拠不正操作 | デジタル署名追加の更新版リリース (EOL 3製品はパッチなし); Thermo Fisher Security Bulletin (2026-07-31); THN (2026-08-03) | CVSS v4.0:8.2 / 法科学・DNA 証拠改ざんリスク / EOL 製品はパッチなし |
| CVE-2026-62416 | Sharp Network Scanner Tool Lite ≤V2.0.11.14 / Network Scanner Tool ≤V6.0.1.6 (Win) | CWE-306 / **5.3** | 初期設定のまま使用中のホストへ未認証で FTP 接続 → 無制限ファイルアップロード → ホスト DoS または悪意あるファイル実行誘導 | Lite V2.1.0.2 / Tool V6.2.0.1 (起動時にランダム認証情報を自動設定); JVNVU#92540957 (2026-08-03) | JVN 公表 / Sharp MFP 国内利用多数 / 初期設定のまま運用ケース多数 |

---

## 国内脆弱性・インシデント

### JVNVU#92540957 — Sharp ネットワークスキャナーツール 初期設定における認証欠如

**CVE-2026-62416** | 公表日: 2026-08-03 | CVSS 5.3 (Medium)

**製品**: Sharp Corporation「ネットワークスキャナーツール Lite」V2.0.11.14 以前・「ネットワークスキャナーツール」V6.0.1.6 以前 (Windows 用; MFP からスキャン出力を受信する FTP サーバーアプリ)

**問題**: 初期設定状態では認証なしに誰でも接続・無制限ファイルアップロードが可能 (CWE-306)。DoS または悪意あるファイルのアップロード→実行による他システムへの攻撃に悪用される恐れ。

**修正**: Lite V2.1.0.2 / Tool V6.2.0.1 にアップデート (アップデート後の初回起動時にランダム認証情報を自動生成)。

**発見者**: Deniz Güney Yıldırım (JPCERT/CC 経由で Sharp に報告・協調開示)

([JVN JVNVU#92540957](https://jvn.jp/en/vu/JVNVU92540957/))

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| Bloomberg / CNBC / CNN (White House AI Safety Meeting) | CNBC "2026-08-03" 確認 ✓ / Bloomberg "2026-08-03" 確認 ✓ |
| CNBC / ComplianceHub.wiki (EU AI Act GPAI 執行権限 Articles 51-56) | CNBC "2026-08-03" 確認 ✓ / ComplianceHub.wiki "2026-08-02" 確認 ✓ |
| WindowsForum / InsiderFinance / Microsoft Security (Project Perception パブリックプレビュー) | WindowsForum URL "/2026/08/03/" 確認 ✓ |
| DataBreaches.net / CyberSecurityNews (Brinks Home 侵害) | DataBreaches.net URL "/2026/08/02/" 確認 ✓ |
| N-able Blog / Help Net Security / GBHackers / THN (N-central CVE-2026-18577) | N-able Blog "August 2, 2026" 確認 ✓ / HelpNetSecurity URL "/2026/08/03/" 確認 ✓ |
| THN / GuardianMSSP / BleepingComputer / Google GTIG (DarkSword/GHOSTBLADE) | THN URL "/2026/08/" 確認 ✓ / Thomas Harris WordPress "/2026/08/03/" 確認 ✓ / GuardianMSSP URL "/2026/08/03/" 確認 ✓ |
| BleepingComputer / Flare Research (BTMOB RAT エコシステム) | BleepingComputer URL 確認 ✓ / Xloggs "2026-08-03 08:00 PDT" 確認 ✓ |
| THN / Thermo Fisher Security Bulletin (CVE-2026-17583) | THN URL "/2026/08/" 確認 ✓ / Thomas Harris WordPress "/2026/08/03/" 確認 ✓ / 一次ソース (Thermo Fisher bulletin) 2026-07-31 |
| JVN / JVNVU#92540957 (CVE-2026-62416 Sharp) | JVN JVNVU#92540957 "2026-08-03" 確認 ✓ / TheHackerWire "CVE-2026-62416" 確認 ✓ |
| jvn.jp / jpcert.or.jp / ipa.go.jp / piyolog | JVNVU#92540957 のみ新規 (2026-08-03); その他 2026-08-02〜04 新規エントリなし |
| thehackernews.com / bleepingcomputer.com / nvd.nist.gov / cisa.gov | 403 — WebSearch スニペット・Thomas Harris WordPress・GuardianMSSP・Xloggs 等で代替 |

### 集計サマリ

- **巡回ソース数**: 約 20
- **採用件数**: AI=3 / Security=4 / CVE=3 / 国内=1
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-08-02 より前の一次ソース / news coverage のみ): CVE-2026-58052 7-Zip (2026-06-28) / CVE-2026-42167 ProFTPD (2026-04-28〜05-01) / CVE-2026-34908〜34910 Ubiquiti UniFi (2026-05-22) / CVE-2026-10520 Ivanti Sentry (2026-06-09) / CVE-2026-20253 Splunk (2026-06-18 CISA KEV) / CVE-2026-16232 Check Point (2026-07-22) / HijackKV arXiv (2026-07-22) / CVE-2026-55040 SharePoint (July Patch Tuesday → August RCE chain 未公開) / BTMOB 初報 (2026-05-xx THN Grandoreiro 記事として存在するが Flare エコシステム研究 2026-08-03 は採用)
  - 重複 (直近 7 ダイジェスト掲載済み・excluded_set 参照): CVE-2026-48449/48448 (Adobe Campaign Classic, 08-03掲載) / CVE-2026-63223 CodeIgniter4 / CVE-2026-67208 Juggle / CVE-2026-53609/53606 (apostrophe/sanitize-html) / CVE-2026-66066 Rails / CVE-2026-59309/59310 VMware / CVE-2026-20316 Cisco FMC / CVE-2026-63077 JetBrains TeamCity / CVE-2026-17650〜17656 Chrome / CVE-2026-42897 Exchange / CVE-2026-8233 5G / CVE-2026-53921 OpenWrt / CVE-2026-66713 Apache Axis2 / CVE-2025-68686 FortiOS / CVE-2026-16812 Arista / CVE-2026-53264 Linux kernel / CISA KEV 3件追加 (07-27〜29 付け、いずれも excluded_set 対象) / オープンウェイトAI マニフェスト論争 (08-03掲載) / ESET H1 2026 (08-03掲載) / CaptiveCrunch Midnight Blizzard (08-03掲載) / Coldcard PRNG (08-03掲載) / HackerOne 政府ID (08-03掲載) / CISA 水道PLC (08-03掲載) / EU AI Act Article 50 (08-02掲載、今回は Article 51-56 GPAI 執行を [続報] として採用) / Chrome Big Sleep (08-02掲載) / Amgen PHI (08-02掲載) / Adform JS (08-02掲載) / Arch Linux AUR (08-02掲載) / Anthropic cyber eval breach / GPT-5.6 Luna / Unit 42 DeepSeek+Hermes / Contagious Interview macOS ClickFix / SonicWall credential stuffing / Kaspersky OctLurk/SilkLurk / Laundry Bear / KT Corporation $39M / 4G/5G 84 CVEs / Copilot Word XPIA / VMSA-2026-0006
  - CVE-2026-17583 Thermo Fisher: 一次ソース (ベンダー bulletin) 2026-07-31 だが THN/GuardianMSSP が 2026-08-03 に詳報 → 採用窓内として採用 (Adobe CVE-2026-48449/48448 と同方針)

</details>

---

*生成: keda-digest-bot / 2026-08-04 05:04 JST*
