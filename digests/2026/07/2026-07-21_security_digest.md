# KEDA Security Daily Digest — 2026-07-21

> 採用範囲: 2026-07-19〜2026-07-21 JST に公開された情報のみ掲載。過去 7 日分との重複を除外 ([続報] 表記を除く)。

---

## 本日のサマリ

Hugging Face が 7 月 20 日、自律 AI エージェントによる自社プラットフォーム侵害を公表した。データセット処理パイプラインの RCE ローダーとテンプレートインジェクションの 2 経路が悪用され、17,000 件超のアクションとクラスター認証情報の窃取・横移動が確認された。AI が AI インフラを攻撃した公式事例としては初とみられる。インフラ面では ServiceNow AI Platform の CVE-2026-6875 (CVSS 9.5) が 7/19 に野生悪用開始が確認され、7/15 公開の nginx `map` ヒープ BOF (CVE-2026-42533 CVSS 9.2) と 7-Zip XZ 解析 RCE (CVE-2026-14266) の報道が 7/19〜20 に集中。RubyGems では休眠アカウント乗っ取りによるサプライチェーン攻撃 **SleeperGem** が CI/CD パイプラインを標的に悪意 gem を 3 件公開した。Claude Code にも権限チェック強化を含むセキュリティアップデートが届いている。

---

## AI 関連ニュース

1. [2026-07-20] **Hugging Face** が自律 AI エージェントによる侵害を公表 — データセット処理パイプラインの RCE ローダー + テンプレートインジェクションの 2 経路を通じ 17,000 件超のアクション・クラスター認証情報の窃取と横移動を確認、AI が AI インフラを攻撃した公式事例としては初とみられる。([Axios](https://axios.com/2026/07/20/) / [BleepingComputer](https://www.bleepingcomputer.com/) / [TechCrunch](https://techcrunch.com/) / [Help Net Security](https://www.helpnetsecurity.com/) / HuggingFace Blog)

2. [2026-07-19] **Claude Code** セキュリティアップデート — `/verify`・`/code-review` の自動実行を廃止、Bash/PowerShell のより安全なハンドリング、サブエージェント権限チェック強化。(Anthropic / Claude Code Changelog)

---

## セキュリティ関連ニュース

1. [2026-07-19~20] **SleeperGem** — RubyGems の休眠メンテナアカウントを乗っ取り悪意 gem 3 件を公開 (`git_credential_manager` v2.8.0〜2.8.3 / `Dendreo` / `fastlane-plugin-run_tests_firebase_testlab`)、CI/CD 検知を回避して開発者マシンに RAT 常駐。([THN](https://thehackernews.com/) / StepSecurity / Aikido / [GuardianMSSP](https://guardianmssP.com/2026/07/20/))

2. [2026-07-20] **CVE-2026-6875 (ServiceNow AI Platform)** の野生悪用が 7/19 に初確認 — 7/13 パッチから 6 日、PoC とは別の第 2 ガジェットチェーンが確認済み、Fortune 500 の 85% が該当製品を利用。([Help Net Security](https://www.helpnetsecurity.com/) / [TechTimes](https://www.techtimes.com/))

3. [2026-07-19] **CVE-2026-42533 (nginx)** の詳細が公開 — `map` ディレクティブの regex キャプチャ状態未保存によるヒープ BOF + 情報漏洩 (15 年超未修正)、nginx 0.9.6〜1.31.2 全版が対象、7/15 公開パッチ (1.30.4/1.31.3/Plus R36 P7) 適用を推奨。([THN](https://thehackernews.com/) / [Thomas Harris blog](https://thomasharris.blog/2026/07/19/))

4. [2026-07-20] **CVE-2026-14266 (7-Zip XZ RCE)** の報道が集中 — 細工 XZ アーカイブ開封で vtable ハイジャック→任意コード実行、7-Zip 21.07〜26.01 対象、自動更新なし・手動で v26.02 への更新が必須。([THN](https://thehackernews.com/) / ZDI-26-444 / [GuardianMSSP](https://guardianmssP.com/2026/07/20/))

---

## 新規 CVE / Advisory

| CVE/GHSA | 製品・バージョン | CWE / CVSS | バグクラス (条件→シンク→結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-6875 | ServiceNow AI Platform (Brazil EA / Zurich P9 / Yokohama P13 以前の全版) | CWE-94 / **9.5** | 未認証攻撃者が AI Platform エンドポイントにペイロードを送信 → Groovy/JS スクリプトサンドボックスを脱出 → ホスト OS 上で任意コード実行・横移動 | KB3137947 (2026-07-13 リリース) | **野生悪用確認 (初観測 2026-07-19)** / 第 2 ガジェットチェーン確認済 / Fortune 500 の 85% 利用 / 即時パッチ必須 |
| CVE-2026-42533 | nginx 0.9.6〜1.30.3 (stable) / 0.9.6〜1.31.2 (mainline) / NGINX Plus R33〜R36 | CWE-122 / **9.2** (CVSSv4) | 未認証攻撃者が細工 HTTP リクエストを送信 → `map` ディレクティブの regex キャプチャ状態未保存でヒープ BOF + ASLR 回避可能な情報漏洩 → ワーカークラッシュ/任意コード実行 | nginx 1.30.4 / 1.31.3 / NGINX Plus R36 P7 (2026-07-15) | 15 年超の未修正欠陥 / 未認証 / Web サーバー広範利用 / nginx.org からパッチ取得推奨 |
| CVE-2026-14266 | 7-Zip 21.07〜26.01 | CWE-122 / **7.0** | 攻撃者が細工した XZ アーカイブを被害者に開封させる → XZ chunked data 解析で境界外書込み → vtable ハイジャックにより任意コード実行 | 7-Zip 26.02 / [ZDI-26-444](https://www.zerodayinitiative.com/) (2026-06-25 初報) | 手動更新必須 (自動更新なし) / XZ 解析ヒープ BOF パターン水平伝播候補 / 2026-07-20 報道集中 |

---

## 国内脆弱性・インシデント

> 直近 2 日間 (2026-07-19〜20) に JVN/JPCERT/CC/IPA/Piyolog で確認できた新規の国内脆弱性・インシデント公表はありませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| Axios / BleepingComputer / TechCrunch / Help Net Security / HuggingFace Blog (Hugging Face AI エージェント侵害) | 2026-07-20 URL "/2026/07/20/" 確認 ✓ |
| Anthropic / Claude Code Changelog (Claude Code セキュリティアップデート) | 2026-07-19 確認 ✓ |
| THN / StepSecurity / Aikido / GuardianMSSP (SleeperGem RubyGems supply chain) | 2026-07-19〜20 URL 確認 ✓ |
| Help Net Security / TechTimes (CVE-2026-6875 ServiceNow 野生悪用) | 2026-07-20 URL "/20260720/" 確認 ✓ |
| THN / Thomas Harris blog (CVE-2026-42533 nginx ヒープ BOF) | 2026-07-19 URL "/2026/07/19/" 確認 ✓ |
| THN / ZDI / GuardianMSSP (CVE-2026-14266 7-Zip XZ RCE) | 2026-07-20 URL "/2026/07/20/" 確認 ✓ |
| jvn.jp / jpcert.or.jp / ipa.go.jp / piyolog | WebSearch 確認: 2026-07-19〜20 新規エントリなし |
| thehackernews.com / bleepingcomputer.com | 403 — WebSearch スニペットで代替 |
| nvd.nist.gov / cisa.gov | 403 — WebSearch スニペット代替 |
| helpnetsecurity.com | 403 — WebSearch スニペット代替 |

### 集計サマリ

- **巡回ソース数**: 約 20
- **採用件数**: AI=2 / Security=4 / CVE=3 / 国内=0
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-07-19 より前): Kimi K3 正式ローンチ (07-17掲載で発表済み) / OpenSSL HollowByte (07-17 THN) / CISA KEV 追加 CVE-2026-47865 (07-20掲載) / GoSerpent Kaspersky (2026-07-17)
  - 重複 (直近 7 ダイジェスト掲載済み・excluded_set 参照): Claude Fable 5 (07-20掲載) / Ecopetrol (07-20掲載) / VMware Avi CVE-2026-47865〜71 (07-20掲載) / NadMesh (07-19掲載) / SGLang CVE-2026-3059/3060 (07-19掲載) / WordPress CVE-2026-63030/60137 (07-19掲載) / ShinyHunters Abbott/Exact Sciences (07-19掲載) / FortiSandbox CVE-2026-39808/25089 KEV (07-18掲載) / EY 漏洩 (07-18掲載) / Scattered Spider 判決 (07-18掲載) / LegacyHive (07-17掲載) / Zoom CVE-2026-53412 (07-17掲載) / Oracle EBS CVE-2026-46817 (07-17掲載) / SharePoint CVE-2026-58644 (07-17掲載) / CVE-2026-59255 BloodHound (07-17掲載) / JVNVU#90968686/90338324 (07-19掲載)

### 主要除外補足

- **CVE-2026-14266 (7-Zip)**: ZDI 初報 2026-06-25・7-Zip 26.02 リリース 2026-06-25 と古いが、THN・GuardianMSSP 等の主要報道が 2026-07-20 に集中確認 → 直近 7 ダイジェスト未掲載 → ニュースサイト掲載日基準 (VMware Avi と同様) で採用
- **CVE-2026-42533 (nginx)**: nginx パッチ 2026-07-15・CERT/CC 勧告 2026-07-15 だが THN/Thomas Harris の詳細解説記事が 2026-07-19 公開確認 → 窓内採用 / nginx はデフォルト設定で `map` を使用するケースがあり広範影響
- **Hugging Face 侵害**: 一部出典に 2026-07-16 初報説あり。ただし Axios・Help Net Security 等の主要報道 URL が "/2026/07/20/" を示すため 2026-07-20 採用
- **CISA KEV**: 2026-07-15〜20 の区間に新規追加なし (FortiSandbox KEV は 07-16・07-18掲載済み)

</details>

---

*生成: keda-digest-bot / 2026-07-21 05:04 JST*
