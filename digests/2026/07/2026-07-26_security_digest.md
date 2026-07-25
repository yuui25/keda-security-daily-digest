# KEDA Security Daily Digest — 2026-07-26

> 採用範囲: 2026-07-24〜2026-07-26 JST に公開された情報のみ掲載。過去 7 日分との重複を除外 ([続報] 表記を除く)。

---

## 本日のサマリ

Kimi K3 が 90 分で Redis に 19 件のゼロデイを発見し Redis が 7 パッチを同日リリースするという AI 脆弱性発見の新記録が生まれた。同時期に XBOW の自律エージェントが Bing Images に CVSS 9.8 の SYSTEM 権限 RCE (CVE-2026-32194/32191) を発見・報告し Microsoft がサーバー側で静かに修正していたことが公表された。セキュリティ面では GitLab ≤18.11.3 に認証済みユーザーが push 権限のみで任意コードを実行できる Jupyter ノートブック経由の Heap BOF PoC が公開、OnTrac の 4 万件超 PII 流出、Qilin が Stryker を含む複数の重要組織を標的に侵害主張を公表した。国内では JVN が Logto (SaaS・AI 向け IdM) の OIDC/OAuth2.1/SAML 全プロトコルにわたる認証バイパス脆弱性 (JVNVU#99418634) を 7/24 に勧告した。

---

## AI 関連ニュース

1. [2026-07-24] **Kimi K3** が Redis に 19 件のゼロデイを 90 分で発見 — Stream NACK double-free / RESTORE チェーンを含む 7 件を Redis CE 6.2.23・7.4.10・8.6.5・8.8.1 で同日パッチ (2026-07-23)、残 12 件は調整中。AI 自律型バグハントが商用 OSS の深部まで到達した事例として注目。([THN](https://thehackernews.com/) / GuardianMSSP)

2. [2026-07-24] **XBOW** の自律エージェントが Bing Images に CVSS 9.8 RCE (CVE-2026-32194/CVE-2026-32191) を発見 — 1 ピクセル SVG を「画像で検索」に送信するだけで画像処理ワーカーが SVG スクリプトを実行し Windows Server 2022 上で `NT AUTHORITY\SYSTEM` が取得可能。Microsoft はサーバー側で修正済み (顧客対応不要)、XBOW が 7/23 に詳細公開。([THN](https://thehackernews.com/) / GuardianMSSP)

3. [2026-07-24] **Aikido Security** の AI ペンテストエージェントが NodeBB に 6 時間で 8 件の高重大度欠陥を発見 — XSS・管理者パネル認証バイパス・プライベートチャット窃取を含む; 悪用コード非公開のまま NodeBB 4.14.2 (7/23) で修正。([GuardianMSSP](https://guardianmssp.com/2026/07/24/))

4. [2026-07-25] **ChatGPT / Codex / API** が 4 日間で 4 回目の障害 — 1,535 件超の Downdetector 報告、503 `biscuit_baker_service_me_circuit_open`、OpenAI が緩和措置を適用したが根本原因は未公表。([BleepingComputer](https://www.bleepingcomputer.com/))

---

## セキュリティ関連ニュース

1. [2026-07-24] **GitLab ≤18.11.3** に認証済みユーザーが push 権限のみで任意コード実行できる Jupyter Notebook Heap BOF の PoC が公開 — 細工ノートブックを commit → diff 表示でヒープポインタを漏洩 → ASLR 回避 → 第 2 ノートブックで git 権限 RCE。管理者・CI/CD 不要、被害者操作不要。GitLab 18.11.4 (6/10、セキュリティ修正と明示なく「バグ修正」として配布) で対処済みだが未更新インスタンスが多数残存。([Thomas Harris Blog](https://thomasharris.blog/) / THN)

2. [2026-07-24] **OnTrac** (米国ラストマイル配送、35 州・全米人口の 70% カバー) が侵害を通知 — 攻撃者が 3/20〜22 に法人ネットワークに不正アクセス、4 万件超の顧客 PII (氏名・健康情報・SSN・運転免許証番号等) が漏洩した可能性。([BleepingComputer](https://www.bleepingcomputer.com/))

3. [2026-07-24] **Qilin** ランサムウェアが **Stryker** (米国大手医療機器メーカー) を DLS で侵害主張 — データ公開カウントダウンが進行中、同日 Kean University・アルゼンチン陸軍も主張。([RedPacket Security](https://www.redpacketsecurity.com/))

4. [2026-07-24] EMEA ヘルスケアサプライチェーンへのランサムウェア攻撃が急増 — H1 2026 のヘルスケア本体への攻撃件数 +14% (410件)、製薬・医療機器・医療技術企業への攻撃 +35% (163件)、病院以外の周辺産業も標的化が鮮明。([Help Net Security](https://www.helpnetsecurity.com/))

---

## 新規 CVE / Advisory

| CVE/GHSA | 製品・バージョン | CWE / CVSS | バグクラス (条件→シンク→結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-32194 / CVE-2026-32191 | Microsoft Bing Images 画像処理パイプライン (サーバー側) | CWE-77 / **9.8** | 未認証攻撃者が「画像で検索」に細工 SVG (1px) を送信 → 画像処理ワーカーが SVG スクリプトを実行 → Windows Server 2022 上で `NT AUTHORITY\SYSTEM` で任意コード実行 | MS サーバー側修正済み (2026-03); 技術詳細: XBOW Blog (2026-07-23) | CVSS 9.8 / 未認証 / AI 自律エージェントによる発見 / 顧客対応不要 (MS 修正済み) |
| CVE-2026-25589 incomplete-fix 系 (Redis Stream NACK double-free / RESTORE チェーン) | Redis CE 6.2.22 / 7.4.9 / 8.6.4 / 8.8.0 | CWE-415 / **7.7** | 認証済み攻撃者が `EVAL+XGROUP+RESTORE` を組合せて Stream コンシューマグループの NACK double-free を誘発 → ヒープ破壊 → RCE; 8.8.0 は RedisBloom 経由の追加チェーンあり | Redis CE 6.2.23 / 7.4.10 / 8.6.5 / 8.8.1 (2026-07-23) | Kimi K3 が 90 分で 19 件発見 / 7 件同日パッチ / PoC 公開 / 広範デプロイ |
| CVE-2026-15611 / CVE-2026-15617 | Logto (Silverhand) <v1.22.0 (SaaS・AI アプリ向け IdM) | CWE-287 / **Medium** | SSO フローが IdP 提供メールを既存アカウントに無検証でリンク (CVE-2026-15611) + Unicode/空白正規化欠如でアイデンティティ照合バイパス (CVE-2026-15617) → MFA 回避・任意アカウント乗っ取り | Logto v1.22.0 以降に更新; JVNVU#99418634 / CERT/CC VU#492466 (2026-07-24) | 2026-07-24 JVN 勧告 / OIDC・OAuth2.1・SAML 全プロトコルに影響 / SaaS・AI 認証基盤の水平伝播候補 |
| CVE 未割当 (GitLab Jupyter Notebook Heap BOF RCE) | GitLab self-managed ≤18.11.3 (未更新) | CWE-122 / **pending** | 認証済みユーザー (push 権限のみ) が細工 Jupyter Notebook を commit → diff 表示でヒープポインタを漏洩 → ASLR 回避 → 第 2 ノートブックで git 権限 RCE (管理者不要・被害者操作不要) | GitLab 18.11.4 (2026-06-10, セキュリティ表記なし); PoC: THN / depthfirst (2026-07-24) | **PoC 公開済み (2026-07-24)** / ソースコード・Rails シークレット・CI/CD パイプライン露出リスク / 野生悪用未確認 |

---

## 国内脆弱性・インシデント

| 日付 | 組織・製品 | 概要 | 影響度 | 参照 |
|---|---|---|---|---|
| 2026-07-24 | Logto (SaaS・AI アプリ向け IdM) / JVNVU#99418634 | Logto <v1.22.0 の OIDC/OAuth2.1/SAML 全プロトコルにおける認証・認可欠陥: SSO フローで他人アカウントに無検証リンク (CVE-2026-15611) およびメールの Unicode・空白正規化欠如による認証バイパス (CVE-2026-15617) → MFA 回避・任意アカウント乗っ取り。v1.22.0 以降への更新で修正。JPCERT/CC が国内向け緊急勧告。 | 影響中〜大 / SaaS・AI 認証基盤全般 | [JVNVU#99418634](https://jvn.jp/vu/JVNVU99418634/) / [CERT/CC VU#492466](https://kb.cert.org/vuls/id/492466) |

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| THN / GuardianMSSP (Kimi K3 Redis ゼロデイ 19 件) | 2026-07-24 URL "/2026/07/24/" 確認 ✓ |
| THN / GuardianMSSP (XBOW Bing Images CVE-2026-32194/32191) | 2026-07-24 URL "/2026/07/24/" 確認 ✓ (XBOW Blog 2026-07-23 技術開示) |
| GuardianMSSP (Aikido NodeBB 8 件) | 2026-07-24 URL "/2026/07/24/" 確認 ✓ |
| BleepingComputer (ChatGPT 4th outage) | 2026-07-25 "July 25, 2026" 確認 ✓ |
| Thomas Harris Blog / THN (GitLab Jupyter Heap BOF RCE PoC) | 2026-07-24 URL "/2026/07/24/" 確認 ✓ |
| BleepingComputer (OnTrac 侵害通知) | 2026-07-24 "July 24, 2026 at 03:55 PM" 確認 ✓ |
| RedPacket Security (Qilin / Stryker) | 2026-07-24 確認 ✓ |
| Help Net Security (EMEA ヘルスケアサプライチェーン) | 2026-07-24 URL "/2026/07/24/emea-healthcare-ransomware-activity/" 確認 ✓ |
| jvn.jp / jpcert.or.jp (JVNVU#99418634 Logto) | 2026-07-24 公開確認 ✓ / CERT/CC VU#492466 裏付け ✓ |
| thehackernews.com / bleepingcomputer.com | 403 — WebSearch スニペットで代替 |
| nvd.nist.gov / cisa.gov | 403 — WebSearch スニペット代替 |
| helpnetsecurity.com | 403 — WebSearch スニペット代替 |

### 集計サマリ

- **巡回ソース数**: 約 20
- **採用件数**: AI=4 / Security=4 / CVE=4 / 国内=1
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-07-24 より前): JVN ISC BIND 勧告 (2026-07-23) / OpenAI Presence マルチモーダル (2026-07-22) / Atlassian 7 月バレティン [続報] (07-22 掲載) / DeepSeek V4 GA (07-24 掲載窓外) / Gemini 3.6 Flash (07-23 掲載)
  - 重複 (直近 7 ダイジェスト掲載済み・excluded_set 参照): JADEPUFFER ENCFORGE (07-22掲載) / Pillar Security Week of Sandbox Escapes (07-22掲載) / Qilin [07-23掲載の 1,358件本体] / WordPress CVE-2026-63030 CISA KEV (07-22掲載) / ServiceNow CVE-2026-6875 (07-21掲載) / nginx CVE-2026-42533 (07-21掲載) / 7-Zip CVE-2026-14266 (07-21掲載) / Claude Fable 5 (07-20掲載) / VMware Avi CVE-2026-47865〜71 (07-20掲載) / NadMesh (07-19掲載) / SGLang CVE-2026-3059/3060 (07-19掲載) / WordPress CVE-2026-63030/60137 本体 (07-19掲載) / FakeAgent SectopRAT (07-25掲載) / AgentForger ChatGPT (07-25掲載) / SharedRoot CVE-2026-46331 (07-25掲載) / Certighost CVE-2026-54121 (07-25掲載) / JadeProx TriBack Loader (07-24掲載) / CVE-2026-16232 Check Point (07-24掲載)

### 主要除外補足

- **XBOW Bing Images (CVE-2026-32194/32191)**: XBOW ブログ初報 2026-07-23 だが THN・GuardianMSSP の主要報道が 2026-07-24 に集中確認 → VMware Avi / 7-Zip と同様のニュースサイト掲載日基準で採用
- **ISC BIND 脆弱性 (JVN)**: JVN 勧告が 2026-07-23 公開確認 → 採用窓 (2026-07-24〜26) 外のため除外
- **Redis CVE**: CVE-2026-25589 incomplete-fix 系として集約; 19 件のうち 7 件のみパッチ済み (残 12 件は調整中) → パッチ済み分を代表行として掲載
- **Qilin**: 1,358 件の前回掲載 (07-23) とは別の新規侵害主張 (Stryker等) として採用。[続報] 表記は付さず新規事案として扱う

</details>

---

*生成: keda-digest-bot / 2026-07-26 05:04 JST*
