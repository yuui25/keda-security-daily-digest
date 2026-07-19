# KEDA Security Daily Digest — 2026-07-20

> 採用範囲: 2026-07-18〜2026-07-20 JST に公開された情報のみ掲載。過去 7 日分との重複を除外 ([続報] 表記を除く)。

---

## 本日のサマリ

Anthropic が 7 月 20 日より Claude **Fable 5** を Max・Team Premium プランに 50% 使用制限付きで永久収録すると 7/18 に発表。Pro・Team Standard ユーザーは usage credits 方式のみとなり一時 $100 クレジットが付与される。コロンビア最大エネルギー企業 **Ecopetrol** (国内炭化水素 60% 超生産) が同日サイバー攻撃を公表: 15 子会社にまたがるクラウドファイルストレージから 3,300 アカウント分のデータが不正ダウンロードされた。ランサムウェア試行はセキュリティ制御で阻止されたが、脅威アクターは身代金要求・公開脅迫を継続。インフラ面では VMware Avi Load Balancer に認証バイパス (CVE-2026-47865 CVSS 9.8) を筆頭とする 7 件の脆弱性 (CVE-2026-47865〜47871) が公開され、Broadcom が緊急パッチを提供している。

---

## AI 関連ニュース

1. [2026-07-18] Anthropic が **Claude Fable 5** を 7/20 より Max・Team Premium プランに永久追加 (50% 制限) — GPT-5.6 Sol・Kimi K3 相次ぐ中、Pro・Team Standard は usage credits 方式に移行し一時 $100 クレジットを付与、需要予測困難を認めつつ稼働容量確保後に恒久化を決定。([Anthropic](https://www.anthropic.com/news/redeploying-fable-5) / [Simon Willison blog](https://simonwillison.net/2026/Jul/18/claude-make-fable-5-permanent/) / [The Decoder](https://the-decoder.com/anthropic-slashes-claude-fable-5-limits-in-max-and-team-premium-and-pushes-pro-users-toward-api-pricing/) / [ClaudeFolio](https://claudefolio.com/blog/anthropic-changed-its-mind-fable-5-is-back-in-max-plans-capped-at-50-percent))

---

## セキュリティ関連ニュース

1. [2026-07-18] **Ecopetrol** (コロンビア最大エネルギー企業) がサイバー攻撃を公表 — クラウドファイルストレージ経由で 15 子会社の約 3,300 アカウント分データを不正ダウンロード、ランサムウェア試行はセキュリティ制御で阻止、犯行組織は身代金要求・公開脅迫を継続、コロンビア検察庁に刑事告訴・当局と連携中。([Colombia One](https://colombiaone.com/2026/07/18/colombia-cyberattack-company-ecopetrol/) / [The Star](https://www.thestar.com.my/tech/tech-news/2026/07/18/colombia039s-ecopetrol-says-cyberattack-stole-data-tied-to-3300-accounts) / [Yahoo Finance](https://finance.yahoo.com/energy/articles/colombias-ecopetrol-says-cyberattack-stole-042239602.html) / PRNewswire)

---

## 新規 CVE / Advisory

| CVE/GHSA | 製品・バージョン | CWE / CVSS | バグクラス (条件→シンク→結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-47865 | VMware Avi Load Balancer 31.1.1〜31.2.2 / 30.2.1〜30.2.6 / 22.1.1〜22.1.7 | CWE-306 / **9.8** | ネットワークアクセスを持つ未認証攻撃者が Avi Control Plane エンドポイントに直接リクエスト送信 → 認証機構を完全バイパス → Control Plane 完全制御・設定変更・バックドア設置 | Avi LB 32.1.2 / 31.2.2-2p3 / 30.2.7 ([Broadcom VMSA-2026-0005](https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/37926)) | 2026-07-18 報道 / CVSS 9.8 / 回避策なし / NATO 研究者発見 / エンタープライズ LB 広範利用 |
| CVE-2026-47867 | VMware Avi Load Balancer 31.1.1〜31.2.2 / 30.2.1〜30.2.6 / 22.1.1〜22.1.7 | CWE-77 / **8.7** | ネットワークアクセスを持つ攻撃者が Management Console にコマンドインジェクションペイロードを送信 → Control Plane 上で任意コード実行 | Avi LB 32.1.2 / 31.2.2-2p3 / 30.2.7 (Broadcom VMSA-2026-0005) | CVE-2026-47865 との連鎖で未認証 RCE 成立 / 同一パッチで修正 |
| CVE-2026-47866 / CVE-2026-47868〜47871 | VMware Avi Load Balancer (同上) | CWE-306/269/22 / 7.1〜8.7 | 認証バイパス (一部 Control Plane 限定・CVE-2026-47866)、権限昇格 (CVE-2026-47868/47870)、RCE (CVE-2026-47869 認証済み)、ディレクトリトラバーサル (CVE-2026-47871) の計 5 件; 同一 VMSA-2026-0005 内の関連脆弱性群 | Avi LB 32.1.2 / 31.2.2-2p3 / 30.2.7 (Broadcom VMSA-2026-0005) | CVE-2026-47865/47867 と合わせて 7 件一括修正 / 2026-07-18 報道 ([SecurityOnline.info](https://securityonline.info/vmware-avi-load-balancer-cve-2026-47865/) / [SecurityWeek](https://www.securityweek.com/7-severe-vulnerabilities-patched-in-vmware-avi-load-balancer/)) |

---

## 国内脆弱性・インシデント

> 直近 2 日間 (2026-07-18〜19) に JVN/JPCERT/CC/IPA/Piyolog で確認できた新規の国内脆弱性・インシデント公表はありませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| Anthropic / Simon Willison blog / The Decoder / ClaudeFolio (Fable 5 永久追加) | 2026-07-18 公開確認 ✓ |
| Colombia One / The Star / Yahoo Finance / PRNewswire (Ecopetrol サイバー攻撃) | 2026-07-18 公開確認 ✓ |
| SecurityOnline.info / SecurityWeek (VMware Avi Load Balancer CVE-2026-47865〜71) | 2026-07-18 報道確認 ✓ (Broadcom VMSA-2026-0005 は 7/14 公開) |
| jvn.jp / jpcert.or.jp / ipa.go.jp / piyolog | WebSearch 確認: 2026-07-18〜19 新規エントリなし |
| thehackernews.com / bleepingcomputer.com | 403 — WebSearch スニペットで代替 |
| nvd.nist.gov / cisa.gov | 403 — WebSearch スニペット代替 |
| helpnetsecurity.com / securityweek.com | 403 — WebSearch スニペット代替 |

### 集計サマリ

- **巡回ソース数**: 約 20
- **採用件数**: AI=1 / Security=1 / CVE=3 (7件を3行で集約) / 国内=0
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-07-18 より前): OAuth クライアント ID スプーフィング (2026-07-13) / SonicWall SMA CVE-2026-15409/15410 (2026-07-14 KEV) / OpenSSL HollowByte (2026-07-17 Okta Red Team) / GoSerpent Kaspersky レポート (2026-07-17) / CISA AA26-194A ロシア FSB ルーター (2026-07-13) / D1R Synopsys/Bosch (2026-07-13) / Meta Muse Spark 1.1 (2026-07-09) / Nichirei/KFC Japan (2026-07-13〜16) / EC Google Android AI 命令 (2026-07-16)
  - 重複 (直近 7 ダイジェスト掲載済み・excluded_set 参照): WordPress CVE-2026-63030/60137 (07-19掲載) / SGLang CVE-2026-3059/3060 (07-19掲載) / NadMesh AI/MCP ボットネット (07-19掲載) / ShinyHunters Abbott/Exact Sciences (07-19掲載) / Fortinet FortiSandbox CVE-2026-39808/25089 KEV (07-18掲載) / EY データ漏洩 (07-18掲載) / Scattered Spider 判決 (07-18掲載) / LegacyHive Windows ProfSvc (07-17掲載) / Zoom CVE-2026-53412 (07-17掲載) / Oracle EBS CVE-2026-46817 KEV (07-17掲載) / SharePoint CVE-2026-58644 (07-17掲載) / PyTorch Lightning CVE-2026-58659 (07-17掲載) / BloodHound CVE-2026-59255 (07-17掲載)

### 主要除外補足

- **VMware Avi Load Balancer VMSA-2026-0005**: Broadcom 初報 2026-07-14 / THN 統合記事 2026-07-15 / Canadian Centre AV26-712 は 2026-07-17 — いずれも採用窓外だが、SecurityOnline.info / SecurityWeek が 2026-07-18 に独立記事として掲載確認 (ニュースサイト掲載日基準) かつ直近 7 ダイジェスト未掲載のため採用
- **OpenSSL HollowByte (no CVE)**: Okta Red Team が 2026-06 に研究完了・THN/BleepingComputer が 2026-07-17 に掲載 → 採用窓 (07-18〜20) 外のため除外。なお 2026-07-19 ダイジェスト (窓 07-17〜19) にも未掲載
- **Ecopetrol 攻撃日**: PRNewswire 初報は 2026-07-17 とする一部出典あり。ただし The Star・Colombia One 等の確認可能な URL がいずれも /2026/07/18/ を示すため 2026-07-18 採用

</details>

---

*生成: keda-digest-bot / 2026-07-20 05:04 JST*
