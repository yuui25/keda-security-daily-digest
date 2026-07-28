# KEDA Security Daily Digest — 2026-07-29

> 採用範囲: 2026-07-27〜2026-07-29 JST に公開された情報のみ掲載。過去 7 日分との重複を除外 ([続報] 表記を除く)。

---

## 本日のサマリ

Microsoft が MAI-Cyber-1-Flash (5B パラメータ特化型サイバーセキュリティ AI) を MDASH フレームワーク内に公開し、CyberGym ベンチマーク 95.95% を達成した。GPT-5.4 との組み合わせでコスト 50% 削減を実現し、Project Perception (Red/Blue/Green 攻防エージェント群) の 8/3 プレビュー公開を予告。Apple iOS/macOS/tvOS 26.6 が大規模セキュリティ更新を提供した中、Anthropic Claude が CVE-2026-64757 等を含む脆弱性 3 件を発見した「Project Glasswing」が注目を集めた。脆弱性面では Arista VeloCloud CVE-2026-16812 (CVSS 10.0 未認証 OS コマンドインジェクション) と FortiOS CVE-2025-68686 (SSL-VPN symlink 永続化バイパス) が CISA KEV に追加、JetBrains TeamCity CVE-2026-63077 (CVSS 9.8 未認証 RCE) が 7/28 にパッチ公開された。STAR Labs が AI 支援で発見した Linux kernel CVE-2026-53264 (tcf_idr_check_alloc UAF → root LPE、PoC 公開済み) も要注意。国内では ELECOM 複数製品の XSS / OS コマンドインジェクション (CVE-2026-44387 / CVE-2026-59764 / CVE-2026-61376) が JVN#56870912 として勧告された。

---

## AI 関連ニュース

1. [2026-07-28] **Microsoft MAI-Cyber-1-Flash を MDASH フレームワークに公開** — 5B パラメータのサイバーセキュリティ特化 AI が CyberGym ベンチマーク 95.95% を記録。GPT-5.4 と組合せて 50% コスト削減を実現。攻撃 (Red) / 防御 (Blue) / 評価 (Green) の 3 エージェント構成の Project Perception を 8/3 にプレビュー公開予定。([Axios](https://www.axios.com/) (2026-07-27) / SecurityWeek / THN / MarkTechPost (2026-07-28))

2. [2026-07-27] **Apple iOS 26.6 / macOS Tahoe 26.6「Project Glasswing」** — Anthropic Claude が CVE-2026-64757 を含む 3 件を発見、OpenAI Codex Security が 3 件、NVIDIA AI Red Team が 2 件を独立発見。$1億ドル規模の AI 脆弱性発見イニシアティブの成果として公表。([9to5Mac](https://9to5mac.com/) (2026-07-27) / MacRumors (2026-07-27))

3. [2026-07-28] **CVE-2026-53264: AI 支援によるLinux kernel LPE 発見** — STAR Labs の Lee Jia Jie が AI 支援ツールで `net/sched/act_api.c` の `tcf_idr_check_alloc()` ロックミスマッチによる UAF を発見、KASAN PoC とレースウィンドウ最適化まで AI が補助。PoC: github.com/star-sg/CVE/CVE-2026-53264 (2026-07-28 公開)。([THN](https://thehackernews.com/) / GBHackers / GuardianMSSP (2026-07-28))

4. [2026-07-28] **Act Security が $60M でステルス解除** — AI エージェントの「アクセス スプロール」問題に特化。$20M Seed (Team8 / Bessemer) + $40M Series A (Notable Capital) を調達し、エージェント ID 管理と最小権限施行プラットフォームを提供。([Axios](https://www.axios.com/) (2026-07-28) / SiliconAngle / SecurityWeek)

---

## セキュリティ関連ニュース

1. [2026-07-27] **Apple 大規模セキュリティアップデート** — iOS/iPadOS 26.6 (約 90 CVE)、macOS Tahoe 26.6 (143 CVE)、tvOS/watchOS/visionOS 26.6 (各 80 件超) を一斉リリース。積極的悪用が確認された CVE は現時点ではなし。Project Glasswing により AI 検出分も含む。([MacRumors](https://www.macrumors.com/) (2026-07-27) / The Apple Post (2026-07-27) / TechTimes (2026-07-28))

2. [2026-07-27] **Arista VeloCloud CVE-2026-16812 が CISA KEV 追加** — オンプレミス VeloCloud Orchestrator (VCO) に未認証 HTTP → OS コマンドインジェクション (CVSS 10.0)。実環境での悪用が確認され連邦機関の対応期限は 7/30。修正済みバージョン: VCO 5.2.3.14 / 6.1.3.4 / 6.4.2.4 / 7.0.0.1。([BleepingComputer](https://www.bleepingcomputer.com/) / THN / SecurityWeek / The Register (2026-07-28))

3. [2026-07-27] **FortiOS CVE-2025-68686 が CISA KEV 追加** — SSL-VPN の symlink 永続化バイパス (CVSS 5.9)。ファイルシステムアクセスを既に取得した攻撃者がパッチ適用後も残留アクセスを維持できる。連邦機関対応期限は 8/10。([CISA](https://www.cisa.gov/) (2026-07-27) / SecurityOnline / CybersecurityNews)

4. [2026-07-28] **JetBrains TeamCity CVE-2026-63077: CVSS 9.8 未認証 RCE** — エージェントポーリングプロトコルへの細工データでデシリアライズ → 認証バイパス → OS コマンド実行。修正バージョン 2025.11.7 / 2026.1.3 が 7/28 公開。現時点で野生悪用は未確認。([HelpNetSecurity](https://www.helpnetsecurity.com/) (2026-07-28) / JetBrains Blog (2026-07-28) / THN)

5. [2026-07-28] **Origin Energy 90万顧客のデータ侵害が確認** (Bloomberg 7/28 報道) — 元従業員によるクレデンシャル悪用で氏名・住所・生年月日・電話番号・部分的決済情報が流出。ASX 開示は 7/23 (初回公表)、7/28 Bloomberg 報道で 90 万件規模が確認。([Bloomberg](https://www.bloomberg.com/) (2026-07-28) / SecurityWeek / BleepingComputer)

6. [2026-07-28] **Tengu Mirai ボットネット: watchdog タイマー悪用でフォレンジック証跡消去** — ウォッチドッグタイマーの keepalive トリックでプロセスキル時に強制リブートを誘発し証跡を破壊。メモリ上のみで動作し `systemd-journald` を偽装、Telnet ブルートフォースで感染拡大。([CybersecurityNews](https://cybersecuritynews.com/) / CyberPress / TechTimes (2026-07-28))

---

## 新規 CVE / Advisory

| CVE/GHSA | 製品・バージョン | CWE / CVSS | バグクラス (条件→シンク→結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-16812 | Arista VeloCloud Orchestrator On-Prem <5.2.3.14 / <6.1.3.4 / <6.4.2.4 / <7.0.0.1 | CWE-78 / **10.0** | 未認証の攻撃者が HTTP リクエストに細工データ → VCO の OS コマンドインジェクション → VCO 管理権限取得 + 配下 Edge デバイスへの横展開 | Arista SA-0144; 修正: VCO 5.2.3.14 / 6.1.3.4 / 6.4.2.4 / 7.0.0.1 (2026-07-27) | **CISA KEV 2026-07-27 / 対応期限 7/30 / 実エクスプロイト確認** |
| CVE-2026-63077 | JetBrains TeamCity On-Prem 全バージョン (<2025.11.7 / <2026.1.3) | CWE-502 / **9.8** | 未認証攻撃者がエージェントポーリングプロトコルに細工データを送信 → 安全でないデシリアライズで認証バイパス → OS 上で任意コマンド実行 | fix: 2025.11.7 & 2026.1.3 (2026-07-28) / JetBrains Blog (2026-07-28) | CVSS 9.8 / 未認証 / CI/CD パイプライン侵害直結 / 野生悪用未確認 |
| CVE-2026-53264 | Linux kernel <6.10.20 `net/sched/act_api.c` (非特権 namespace + CONFIG_NET_ACT_GACT + CONFIG_NET_CLS_FLOWER 必要) | CWE-416 / **7.8** | ローカル非特権ユーザーが `tcf_idr_check_alloc()` のロックミスマッチで解放済み `tc_action` を再参照 → ヒープ破壊 → root 権限昇格 (LPE) | upstream fix 2026-06-01; PoC: github.com/star-sg/CVE/CVE-2026-53264 (2026-07-28 公開) | **AI 支援発見 / PoC 公開済み** / コンテナブレイクアウト候補 / 野生悪用未確認 |
| CVE-2025-68686 | Fortinet FortiOS 7.6.0〜7.6.1 / 7.4.0〜7.4.6 / 7.2.x / 7.0.x / 6.4.x (SSL-VPN 有効構成) | CWE-200 / **5.9** | ファイルシステムアクセスを取得済みの攻撃者が悪意ある symlink を SSL-VPN ディレクトリ配下に設置 → パッチ後もファイルアクセスが残留 → 長期間の永続的ファイル読み取り | Fortinet PSIRT 勧告 (2026-07-27); commit 非公開 | **CISA KEV 2026-07-27 / 対応期限 8/10** / 事前侵害前提 / バックドア残留リスク |

---

## 国内脆弱性・インシデント

| 日付 | 組織・製品 | 概要 | 影響度 | 参照 |
|---|---|---|---|---|
| 2026-07-28 (推定) | ELECOM 無線 LAN ルーター / アクセスポイント (JVN#56870912 / JVNDB-2026-000103) | CVE-2026-44387: ログイン済み攻撃者によるクロスサイトスクリプティング。CVE-2026-59764 / CVE-2026-61376: ログイン済み攻撃者による OS コマンドインジェクション。対象製品: WRC-X3000GS2 / WRC-X1800GS / WRC-X6000QS-XS / WRC-XE5400GS / WRC-BE72XSD / WRC-BE65QSD / WAB-BE187-M / WAB-BE72-M / WAB-M1775-PS 他。最新ファームウェアへの更新で対処。 | 中 (ログイン前提) | [JVN#56870912](https://jvn.jp/jp/JVN56870912/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| Axios / SecurityWeek / THN / MarkTechPost (Microsoft MAI-Cyber-1-Flash MDASH) | 2026-07-27〜28 URL "/2026/07/27/" および "/2026/07/28/" 確認 ✓ |
| 9to5Mac / MacRumors (Apple iOS 26.6 Project Glasswing) | 2026-07-27 URL 確認 ✓ |
| THN / GBHackers / GuardianMSSP (CVE-2026-53264 Linux kernel AI 支援発見) | 2026-07-28 URL 確認 ✓ |
| Axios / SiliconAngle / SecurityWeek (Act Security $60M) | 2026-07-28 URL 確認 ✓ |
| MacRumors / The Apple Post / TechTimes (Apple 26.6 セキュリティ更新) | 2026-07-27〜28 URL 確認 ✓ |
| BleepingComputer / THN / The Register (Arista VeloCloud CVE-2026-16812 CISA KEV) | 2026-07-27〜28 URL 確認 ✓ |
| CISA / SecurityOnline / CybersecurityNews (FortiOS CVE-2025-68686 CISA KEV) | 2026-07-27 URL 確認 ✓ |
| HelpNetSecurity / JetBrains Blog / THN (TeamCity CVE-2026-63077) | 2026-07-28 URL "/2026/07/28/" 確認 ✓ |
| Bloomberg / SecurityWeek / BleepingComputer (Origin Energy 90万件) | 2026-07-28 URL 確認 ✓ (ASX 初開示 7/23) |
| CybersecurityNews / CyberPress / TechTimes (Tengu Mirai ボットネット) | 2026-07-28 URL 確認 ✓ |
| JVN / JVNDB (ELECOM JVN#56870912) | JVNDB-2026-000103 シリアル推定; JVN#56870912 確認 ✓ |
| jvn.jp / jpcert.or.jp / ipa.go.jp / piyolog | WebSearch 確認: ELECOM 以外の 2026-07-27〜28 新規エントリなし |
| thehackernews.com / bleepingcomputer.com | 403 — WebSearch スニペットで代替 |
| nvd.nist.gov / cisa.gov | 403 — WebSearch スニペット代替 |
| helpnetsecurity.com / guardianmssp.com | 403 — WebSearch スニペット代替 |

### 集計サマリ

- **巡回ソース数**: 約 22
- **採用件数**: AI=4 / Security=6 / CVE=4 / 国内=1
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-07-27 より前): LAUNDRY BEAR Zimbra CISA 勧告 (2026-07-23) / macOS.Gaslight (2026-06-23) / Origin Energy ASX 初開示 (2026-07-23) → Bloomberg 7/28 続報を新規イベントとして採用 / China Claude Code campaign (2026-07-06〜13) / Google GKE ブループリント (2026-07-17)
  - 重複 (直近 7 ダイジェスト掲載済み・excluded_set 参照): Kimi K3 open weights (07-27掲載) / SourTrade (07-27掲載) / ShinyHunters セクストーション (07-27掲載) / Steam XMRig (07-27掲載) / 北朝鮮元ハッカー逮捕 (07-27掲載) / CVE-2026-16723 Fastjson (07-27掲載) / Kimi K3 Redis ゼロデイ (07-26掲載) / XBOW Bing CVE-2026-32194/32191 (07-26掲載) / ChatGPT 4回目障害 (07-26掲載) / GitLab Jupyter BOF (07-26掲載) / OnTrac PII 流出 (07-26掲載) / Qilin Stryker (07-26掲載) / EMEA ヘルスケア (07-26掲載) / JVNVU#99418634 Logto (07-26掲載) / Claude 共有チャット Google (07-28掲載) / Open Secure AI Alliance (07-28掲載) / Bloomberg AI CVE 2x rate (07-28掲載) / Tego AI symlink (07-28掲載) / AWS DevOps Agent (07-28掲載) / GitHub PyPI time-based defenses (07-28掲載) / Coca-Cola Fairlife (07-28掲載) / ShinyHunters EY (07-28掲載) / Android AfterCall (07-28掲載) / vBulletin CVE-2026-61511 (07-28掲載) / GHSA-gv7g-jm28-cr3m n8n (07-28掲載) / FakeAgent SectopRAT (07-25掲載) / SharedRoot CVE-2026-46331 (07-25掲載) / Certighost CVE-2026-54121 (07-25掲載) / Clop Windchill (07-25掲載) / JADEPUFFER ENCFORGE (07-22掲載) / Pillar sandbox escapes (07-22掲載)

### 主要除外補足

- **Apple iOS 26.6 (セキュリティ更新 vs Project Glasswing)**: セキュリティアップデート全体は Security#1 として掲載、AI 発見部分 (Project Glasswing) は AI#2 として独立採用。重複ではなく異なる切り口の同一事象として分割掲載
- **Origin Energy**: ASX 初開示 7/23 は採用窓外だが、Bloomberg の 90 万件規模確認報道が 2026-07-28 に初掲載 → 新規情報として採用 (07-28掲載の Fairlife とは別事案)
- **Tengu Mirai**: CybersecurityNews / CyberPress の 2026-07-28 URL 確認。watchdog タイマー悪用は先行ダイジェストに掲載なし → 新規採用
- **ELECOM JVN#56870912**: JVNDB-2026-000103 のシリアルから 2026-07-28 公開と推定。JVN ページの直接確認は 403 のため WebSearch スニペット代替

</details>

---

*生成: keda-digest-bot / 2026-07-29 05:04 JST*
