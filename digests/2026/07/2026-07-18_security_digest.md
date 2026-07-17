# KEDA Security Daily Digest — 2026-07-18

> 採用範囲: 2026-07-16〜2026-07-18 JST に公開された情報のみ掲載。過去 7 日分との重複を除外 ([続報] 表記を除く)。

---

## AI 関連ニュース

1. [2026-07-16] Google Gemini 3.5 Pro が3度目の期限を未達 — コーディング性能が GPT-5.6 に及ばず幻覚問題継続、Alphabet 株 4.4% 下落で約 $200B の市場価値が消失、ストップギャップとして Gemini 3.6 Flash を検討中。([TechTimes](https://www.techtimes.com/) / Bloomberg / 9to5Google)

2. [2026-07-17] [続報] WAIC 2026 (上海) 2日目 — 29 カ国が WAICO (World AI Cooperation Organization) 創設協定に正式署名、習近平が基調講演で発展途上国向け AI 研修機会 5,000 件を公約。([TechTimes](https://www.techtimes.com/) / Al Jazeera)

3. [2026-07-16] Google が NotebookLM を「Gemini Notebook」にリブランド — Pro ユーザー向けセキュアクラウドコンピュートでノートブック内コード実行が可能に、Gemini アプリ・Google Search と同期。([9to5Google](https://9to5google.com/) / Google Blog)

4. [2026-07-17] Claude Code July 17 アップデート — `/fork` がバックグラウンドセッション生成に変更、WebSearch 呼出し上限 (デフォルト 200)・サブエージェント生成上限 (デフォルト 200) を新設してランアウェイループを防止。(Anthropic / Claude Code Changelog)

5. [2026-07-16] 23andMe が 43 州 AG との $18M マルチステート和解に合意 — 2023 年遺伝情報侵害 (690 万人) への制裁、MFA 義務化・アドバイザリーボード設置等の新データ保護要件を含む。([PA AG](https://www.attorneygeneral.gov/) / [BleepingComputer](https://www.bleepingcomputer.com/))

---

## セキュリティ関連ニュース

1. [2026-07-16] Coca-Cola 子会社 Fairlife にランサムウェア攻撃 — 米国全域の乳製品生産 (年間売上 $4B 規模) を一時停止、攻撃グループ未特定、カナダ事業は無影響。([TechCrunch](https://techcrunch.com/) / [The Register](https://www.theregister.com/))

2. [2026-07-16] CISA が Fortinet FortiSandbox の CVE-2026-39808 / CVE-2026-25089 を KEV に追加 — 双方とも未認証 OS コマンドインジェクション CVSS 9.1、野生悪用確認済み、連邦機関は 2026-07-19 までにパッチ適用義務。([CISA](https://www.cisa.gov/) / [The Register](https://www.theregister.com/))

3. [2026-07-16] ClickLock — ClickFix 経由の新型 macOS インフォスティーラーを Group-IB が公開、210ms 間隔プロセス強制終了でパスワード入力を強要、8 ブラウザ・31 クリプトウォレット拡張が標的、33 カ国 100 件以上の感染を確認。([Group-IB](https://www.group-ib.com/) / [BleepingComputer](https://www.bleepingcomputer.com/))

4. [2026-07-17] Ernst & Young (EY) がサードパーティ IT サポートシステム侵害によるデータ漏洩を公表 — 2026-03-28〜04-12 の不正アクセス期間中、顧客の税務・投資関連個人情報が漏洩、Experian 24 ヶ月 ID モニタリングを提供。([BleepingComputer](https://www.bleepingcomputer.com/))

5. [2026-07-16] Scattered Spider 英国人メンバー 2 名に禁固 5.5 年 — Owen Flowers (18 歳)・Thalha Jubair (20 歳) が 2024 年 TfL ヴィッシング攻撃 (£29M 損失) で UK Computer Misuse Act Section 3ZA 初適用の有罪判決。([The Register](https://www.theregister.com/) / [Help Net Security](https://www.helpnetsecurity.com/))

---

## 新規 CVE / Advisory

| CVE/GHSA | 製品・バージョン | CWE / CVSS | バグクラス (条件→シンク→結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-39808 | Fortinet FortiSandbox ≤4.4.8 / Cloud/PaaS | CWE-78 / **9.1** | 未認証攻撃者が細工 HTTP リクエストを送信 → Web UI がコマンドを未検証実行 → 任意 OS コマンド実行 | FortiSandbox 4.4.9 | **CISA KEV 2026-07-16 追加** / 野生悪用確認 / 連邦機関 7/19 期限 |
| CVE-2026-25089 | Fortinet FortiSandbox 4.2.x / 4.4.0〜4.4.8 / 5.0.0〜5.0.5 / Cloud & PaaS 5.0.4〜5.0.5 | CWE-78 / **9.1** | 未認証攻撃者が細工 HTTP リクエストを送信 → FortiSandbox Web UI がコマンドを未検証実行 → 任意 OS コマンド実行 | FortiSandbox 5.0.6 | **CISA KEV 2026-07-16 追加** / 野生悪用確認 / CVE-2026-39808 と同コンポーネント |
| CVE-2026-62241 | clawvet API server (apps/api) <0.7.5 | CWE-798 / **9.1** | `auth.ts` がフォールバック JWT シークレット ("clawvet-dev-secret-change-me") をハードコード → 未認証ユーザーが任意トークン生成 → API 完全制御 | [clawvet 0.7.5](https://github.com/clawvet/clawvet/releases/tag/v0.7.5) | 2026-07-17 公開 / ハードコード認証情報パターン / 同仕様 API サーバーへの水平伝播候補 |
| CVE-2026-62386 | Grav API plugin (getgrav/grav-plugin-api) <1.0.0-rc.16 | CWE-598 / **7.5** | 全 API エンドポイントが `?token=` URL クエリで JWT を受入れ → HTTP アクセスログ・リファラ・ブラウザ履歴にトークン漏洩 → セッション乗取り | [grav-plugin-api 1.0.0-rc.16](https://github.com/getgrav/grav-plugin-api/releases/tag/1.0.0-rc.16) | 2026-07-17 公開 / GET パラメーター token 漏洩 / ログ経由 token 漏洩パターン水平伝播候補 |

---

## 国内脆弱性・インシデント

> 直近 2 日間 (2026-07-16〜17) に JVN/JPCERT/CC/IPA/Piyolog で確認できた新規の国内脆弱性・インシデント公表はありませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| TechTimes / Bloomberg / 9to5Google (Gemini 3.5 Pro 3度目期限未達) | 2026-07-16 URL "20260716" 確認 ✓ |
| TechTimes / Al Jazeera (WAIC 2026 WAICO 署名) | 2026-07-17 確認 ✓ ([続報]扱い) |
| 9to5Google / Google Blog (NotebookLM → Gemini Notebook リブランド) | 2026-07-16 確認 ✓ |
| Anthropic / Claude Code Changelog (Claude Code July 17 更新) | 2026-07-17 確認 ✓ |
| PA AG / NH DOJ / BleepingComputer (23andMe $18M マルチステート和解) | 2026-07-16 GantNews URL "/2026/07/16/" 確認 ✓ |
| TechCrunch / The Register (Coca-Cola Fairlife ランサムウェア) | 2026-07-16 TechCrunch URL "/2026/07/16/" 確認 ✓ |
| CISA / The Register (Fortinet FortiSandbox KEV 追加) | 2026-07-16 CISA KEV 追加確認 ✓ |
| Group-IB / BleepingComputer (ClickLock macOS インフォスティーラー) | 2026-07-16 The Register URL "/2026/07/16/" 確認 ✓ |
| BleepingComputer (EY データ漏洩) | 2026-07-17 URL 確認 ✓ |
| The Register / Help Net Security (Scattered Spider 判決) | 2026-07-16 The Register URL "/2026/07/16/" 確認 ✓ |
| GitHub Advisories (CVE-2026-62241 clawvet) | 2026-07-17 公開確認 ✓ |
| GitHub Advisories (CVE-2026-62386 grav-plugin-api) | 2026-07-17 公開確認 ✓ |
| jvn.jp / jpcert.or.jp / ipa.go.jp / piyolog | WebSearch 確認: 2026-07-16〜17 新規エントリなし |
| thehackernews.com / bleepingcomputer.com | 403 — WebSearch スニペットで代替 |
| nvd.nist.gov | 403 — WebSearch スニペット代替 |
| helpnetsecurity.com | 403 — WebSearch スニペット代替 |
| techtimes.com | 403 — WebSearch スニペット代替 |

### 集計サマリ

- **巡回ソース数**: 約 20
- **採用件数**: AI=5 / Security=5 / CVE=4 / 国内=0
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-07-16 より前): Thinking Machines Inkling (2026-07-15) / White House Gold Eagle EO (2026-07-14〜15) / TKMS ランサムウェア (2026-06-28 声明) / OpenClaw GHSA (2026-06-30 公開) / Ollama CVE-2026-7482 (2026-05 公開)
  - 重複 (直近 7 ダイジェスト掲載済み・excluded_set): CVE-2026-58644 SharePoint RCE (07-17掲載・CISA KEV 追加は新情報だが CVE は除外対象) / LegacyHive EoP (07-17掲載) / CVE-2026-53412 Zoom (07-17掲載) / CVE-2026-46817 Oracle EBS (07-17掲載) / CVE-2026-59255 BloodHound (07-17掲載) / ロシア系 Gemini CLI C2 悪用 (07-17掲載) / TuxBot v3 (07-17掲載) / WAIC 2026 開幕・WAICO 提案 (07-17掲載、07-18 続報として再掲)

### 主要除外補足

- **CVE-2026-58644 CISA KEV 追加 (2026-07-16)**: 2026-07-16 付け CISA KEV 追加は新情報だが、CVE 自体は 07-17 digest に掲載済み → excluded_set のため除外
- **Thinking Machines Inkling**: TechCrunch 記事公開が 2026-07-15 確認 → 採用窓 (07-16〜07-18) 外のため除外
- **WAIC 2026 WAICO**: 07-17 digest に掲載済みだが 07-18 に 29 カ国署名の新展開あり → [続報] として採用

</details>

---

*生成: keda-digest-bot / 2026-07-18 05:04 JST*
