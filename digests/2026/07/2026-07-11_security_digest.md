# KEDA Daily Digest — 2026-07-11 (JST)

> 採用範囲: 公開日 2026-07-09 〜 2026-07-11 (JST)
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

AI モデルリリースが集中した 3 日間: SpaceXAI Grok 4.5・Meta Muse Spark 1.1 (Meta 初有料 API)・Anthropic Claude Reflect が 7/9 に同日公開され、Microsoft は Office アプリのプロンプト処理を自社 MAI モデルへ移行開始。セキュリティ面では JetBrains が 7/10 に IntelliJ IDEA / TeamCity / YouTrack を横断する 6 CVE をまとめて公表し (最大 CVSS 9.6)、Joomla 拡張 Balbooa Forms CVE-2026-56291 の未認証 RCE は既に野生悪用が確認されている。Silver Fox の Rust/gRPC C2 マルウェア MODBEACON と WP-SHELLSTORM WordPress 大規模バックドア作戦も 7/10 に新たに報告された。

---

## AI 関連ニュース

- **[2026-07-09]** [SpaceXAI が Grok 4.5 を一般公開 — Cursor 訓練・1.5T V9 パラメーターの "Opus クラス" コーディングモデル](https://thetechportal.com/2026/07/09/spacexai-launches-grok-4-5-its-first-ai-model-built-with-cursor-featuring-advanced-legal-and-finance-commands/) — Cursor との共同開発; Terminal-Bench 2.1 は 83.3%・Fable の 84.3% と僅差; EU を除くすべてのプラットフォームで即日利用可能; Grok Build・Cursor 全プラン・SpaceXAI コンソールで提供。*(TechPortal / Analytics Insight / ExplainX)*

- **[2026-07-09]** [Meta が Muse Spark 1.1 と Meta Model API (公開プレビュー) を公開 — Meta 初の有料推論モデル API](https://americanbazaaronline.com/2026/07/09/meta-opens-muse-spark-1-1-ai-model-to-developers-484330/) — 1M トークンコンテキスト・マルチモーダル (画像/動画/文書)・並列ツール呼び出し・コンピューターユース対応のエージェント推論モデル; 価格は $1.25/$4.25 per 1M tokens (OpenAI・Anthropic の約 4 分の 1); OpenAI SDK と Anthropic Messages フォーマット双方に対応; 新規アカウント $20 クレジット付与。*(American Bazaar / TechTimes / DataCamp)*

- **[2026-07-09]** [Anthropic が Claude Reflect を公開ベータ起動 — 自身の AI 使用習慣を可視化するダッシュボード](https://techcrunch.com/2026/07/09/anthropics-new-claude-feature-is-quietly-selling-you-on-ai/) — Settings > Reflect で過去 1/3/6/12 ヶ月の頻出トピック・ピーク時間帯・タスク傾向を確認可能; "Time and focus" で任意の休憩リマインダーと集中時間を設定できる; Memory が有効なユーザー向けに Free/Pro/Max プランで提供。TechCrunch は「Anthropic が AI 利用をユーザーに売り込む側面」と批評。*(Anthropic / TechCrunch / TechTimes)*

- **[2026-07-09]** [Google が Gemini 3 Deep Think を科学・工学向けにアップデート、API を一般公開](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-deep-think/) — 国際物理・化学オリンピックの筆記問題でゴールドメダル相当の結果; 研究者・企業向けに Gemini API 経由でアクセス可能になったと発表。*(Google DeepMind / TechBuzz.ai)*

- **[2026-07-09]** [Microsoft が Excel と Outlook の Copilot プロンプト処理を自社 MAI モデルへ移行開始](https://winbuzzer.com/2026/07/09/microsoft-reportedly-shifts-ai-workloads-to-mai-models-xcxwbn/) — メールスレッド要約・返信下書き・スプレッドシート整形等の定型タスクを MAI-Thinking-1 / MAI-Code-1-Flash 等に移管し OpenAI・Anthropic への依存を分散; 複雑・創造的タスクは引き続き GPT-5.6 等を利用; Build 2026 で発表した 7 モデルの実用化フェーズ。*(WinBuzzer / Bloomberg / Cryptobriefing)*

---

## セキュリティ関連ニュース

- **[2026-07-09]** [Joomla 拡張 Balbooa Forms CVE-2026-56291 — 未認証任意ファイルアップロード RCE がゼロデイ野生悪用中](https://mysites.guru/blog/balbooa-forms-unauthenticated-file-upload-flaw/) — com_baforms の添付ファイルアップロードエンドポイントがログイン・CSRF トークン・ファイル種別検証のいずれも実施しない設計; PHP ファイルを Web ルートへ書込み即座に実行可; 7/9 に Balbooa Forms 2.4.1 でゼロデイパッチ公開。*(mySites.guru / NVD / CSA Singapore AL-2026-085)*

- **[2026-07-10]** [JetBrains が IntelliJ IDEA / TeamCity / YouTrack にまたがる 6 CVE を一括公開 — 最大 CVSS 9.6 のコード実行を含む](https://cybersecuritynews.com/jetbrains-vulnerabilities/) — CVE-2026-59792 (IntelliJ IDEA, RCE, CVSS 9.6)・CVE-2026-59793 (TeamCity, 任意ファイルアクセス)・CVE-2026-59794 (TeamCity, Stored XSS)・CVE-2026-59791 (YouTrack, CSS インジェクション)・CVE-2026-61492 (YouTrack, Stored XSS) 等を含む; CCCS が AV26-541 アドバイザリを発行。*(CybersecurityNews / JetBrains / CCCS AV26-541)*

- **[2026-07-09/10]** [WP-SHELLSTORM — 140 万 WordPress サイトを標的にしたWebシェルアクセス販売作戦が公開](https://thehackernews.com/2026/07/exposed-hacker-server-reveals-wp.html) — SOCRadar が 6/11 に無認証公開サーバーを発見; 27 CVE を自動悪用、5,700 超のアクティブWebシェルを設置してアクセスを再販する "access brokerage" モデル; 標的は古いプラグインを使用する WordPress サイト (Breeze キャッシュプラグイン・Joomla JCE エディターの既知 CVE が主力)。*(SOCRadar / THN / IntelliPlans)*

- **[2026-07-10]** [Silver Fox が Rust 製 MODBEACON RAT を展開 — gRPC ストリーミングで C2 通信を暗号化・AV/EDR 回避](https://thehackernews.com/2026/07/new-modbeacon-rat-uses-grpc-streaming.html) — QiAnXin 調査; 6 月に技術系・教育機関・国営企業を狙ったキャンペーンで観測; C2 を Amazon・Cloudflare CDN でホスト; VirusTotal 検出率は極めて低く、Silver Fox 過去ツール (ValleyRAT / Gh0st RAT / AtlasCross) とは別の独立マルウェアファミリー。*(THN / KSEC / QiAnXin)*

- **[2026-07-10]** [Ill Bloom — 脆弱乱数ウォレット悪用で $5M 超窃取、Coinspect が 2,114 アドレスを特定 [続報]](https://thehackernews.com/2026/07/attackers-exploit-ill-bloom.html) — 5/27 の集中攻撃で 431 ウォレットから $3.1M、その後 USDT ウォレット 1 件から $2.1M 追加; Bitcoin/Ethereum/Tron/Polygon/Rootstock に跨り 2,114 の脆弱アドレスを確認; 2018 年以降に弱 PRNG でシード生成されたモバイルウォレットが主な対象; illbloom.org で公開ウォレットアドレスの脆弱性確認可能。*(THN / Coinspect / BeinCrypto)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-07-09 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-56291 | Balbooa Forms for Joomla ≤2.4.0 | CWE-434 / **9.8** | 未認証ユーザーが com_baforms の添付ファイルエンドポイントへ POST → ファイル種別・CSRF・認証チェック完全欠如 → PHP ファイルをWeb ルートへ書込み → RCE | [Balbooa Forms 2.4.1 (2026-07-09)](https://www.balbooa.com/support) | 2026-07-09 公開 / 野生悪用確認 (ゼロデイ) / CVSS 9.8 / Joomla 拡張 / 未認証 |
| CVE-2026-59792 | JetBrains IntelliJ IDEA < 2026.1.4 / 2026.2 | CWE-22 / **9.6** | 悪意のあるプロジェクトを開く際のワークスペース ID に含まれるパストラバーサルが処理系に素通り → プロジェクト設定ファイルを任意パスへ書込み → コード実行 | [IntelliJ IDEA 2026.1.4 / 2026.2](https://www.jetbrains.com/privacy-security/issues-fixed/) | 2026-07-10 公開 / CVSS 9.6 / IDE 大規模利用 / CCCS AV26-541 |
| CVE-2026-59793 | JetBrains TeamCity < 2026.1.2 | CWE-22 / **8.8** | TeamCity の Perforce VCS 統合がリポジトリ提供のブランチ名をパスとして展開 → サーバーファイルシステムへの任意ファイルアクセス | [TeamCity 2026.1.2](https://www.jetbrains.com/privacy-security/issues-fixed/) | 2026-07-10 公開 / CVSS 8.8 / CI/CD 基盤広範利用 |
| CVE-2026-59791 | JetBrains YouTrack < 2026.2.17012 | CWE-74 / **Medium** | Mermaid ダイアグラムレンダリングが埋込み CSS をサニタイズせず出力 → CSS インジェクション → UI 偽装・クリックジャッキング等 | [YouTrack 2026.2.17012](https://www.jetbrains.com/privacy-security/issues-fixed/) | 2026-07-10 公開 / 課題追跡 SaaS /スタイルインジェクション系水平伝播候補 |
| CVE-2026-59794 | JetBrains TeamCity < 2026.1.2 | CWE-79 / **Medium** | ビルドエージェントが報告するクラウドプロファイルデータが HTML エスケープ不足でダッシュボードページに出力 → Stored XSS → 管理者セッション乗取り | [TeamCity 2026.1.2](https://www.jetbrains.com/privacy-security/issues-fixed/) | 2026-07-10 公開 / エージェント起点 Stored XSS / CI/CD 権限昇格起点 |
| CVE-2026-61492 | JetBrains YouTrack < 2026.2.17394 | CWE-79 / **Medium** | アーティクルタイトルがダイジェストメール生成時に無害化されず HTML に展開 → メール経由 Stored XSS → 受信者のメールクライアントでスクリプト実行 | [YouTrack 2026.2.17394](https://www.jetbrains.com/privacy-security/issues-fixed/) | 2026-07-10 公開 / メール配信経由 XSS / YouTrack ユーザー全員が対象 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|---|---|---|---|---|
| 2026-07-09 | JVN#48718197 / CVE-2026-56809 | Ricoh 複数レーザープリンター・MFP の Web Image Monitor に Reflected XSS — 管理 Web UI 経由でスクリプト実行が可能 | 中 / セッション情報窃取・管理設定改ざん | [JVNDB-2026-000092](https://jvndb.jvn.jp/en/contents/2026/JVNDB-2026-000092.html) |

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| thetechportal.com / explainx.ai / analyticsinsight.net | Grok 4.5 公開 2026-07-09 ✓ |
| americanbazaaronline.com / TechTimes / DataCamp | Meta Muse Spark 1.1 公開 2026-07-09 ✓ |
| techcrunch.com / macrumors.com / TechTimes | Claude Reflect 2026-07-09 公開 ✓ |
| blog.google / deepmind.google | Gemini 3 Deep Think アップデート 2026-07-09 ✓ |
| winbuzzer.com / Bloomberg (7/7) / cryptobriefing | Microsoft MAI モデル移行 — Bloomberg 7/7 初報、WinBuzzer 7/9 続報採用 ✓ |
| mysites.guru / NVD | CVE-2026-56291 Balbooa Forms 2026-07-09 公開・野生悪用 ✓ |
| cybersecuritynews.com / CCCS AV26-541 | JetBrains CVEs 2026-07-10 公開 ✓ |
| socradar.io / THN (WP-SHELLSTORM) | KSEC forum 比較から 2026-07-09/10 THN 公開 ✓ |
| THN / KSEC (MODBEACON) | Silver Fox MODBEACON 2026-07-10 公開 ✓ |
| THN / BeinCrypto (Ill Bloom) | 2026-07-10 THN 記事 — 5M 超窃取確認、初出は 7/6 だが過去 7 日間ダイジェスト未掲載のため [続報] として採用 ✓ |
| jvndb.jvn.jp / sentinelone | CVE-2026-56809 Ricoh 2026-07-09 JVN 公開 ✓ |
| cisa.gov (KEV) | 403 — WebSearch 確認: 2026-07-09〜11 の新規 KEV 追加なし |
| nvd.nist.gov | 403 — WebSearch スニペット代替 |
| jetbrains.com / cyber.gc.ca | 403 — WebSearch スニペット代替 |
| GitHub Advisories (July 9-10) | 新規 GHSA — 重複除外後の新規クリティカル GHSA を確認できず |
| bleepingcomputer.com / thehackernews.com | 403 — WebSearch スニペットで代替 |
| openai.com / anthropic.com / deepmind.google | 403 — WebSearch スニペット代替 |

### 集計サマリ

- **巡回ソース数**: 約 25
- **採用件数**: AI=5 / Security=5 / CVE=6 / 国内=1
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-07-09 より前): O-UNC-066 vishing Okta (7/6)・ClamAV Cisco (7/1)・Cloudflare Threat Report (3/3)・NSA MCP ガイドライン (5/20)・Phantom Squatting (7/1)・AI-Generated Browser Ransomware (7/1)・BlueHammer ThreatsDay (7/2)・Gemini 3.5 Pro 延期報道 (TechTimes 7/8)・DB Deutsche Bank Unsafe (7/4)・Anthropic/Google/Broadcom compute deal (4/6)
  - 重複 (直近 7 ダイジェスト掲載済み): GPT-5.6 Sol/Terra/Luna (07-10掲載)・ChatGPT Work (07-10掲載)・LapDogs/UAT-7810 LONGLEASH (07-09掲載)・CISA KEV Joomla/Langflow (07-09掲載)・SharePoint CVE-2026-45659 KEV (07-01以前の旧KEV)
  - 日付不明: 0件

### 主要除外補足

- **O-UNC-066 vishing** (Okta Threat Intelligence 公開 7/6 — 採用窓外)
- **"Ill Bloom"** 初出 TechTimes 7/6 → 過去 7 日ダイジェスト未掲載を確認のうえ 7/10 THN 続報 ($5M 超・2,114 アドレス特定) を採用
- **Grok 4.5 vs Fable 5** ベンチマーク比較は採用済み Grok 4.5 項目に含めて記載
- **WP-SHELLSTORM**: SOCRadar が 7/9 公開、THN が 7/9〜10 に報道; 2026-07 ダイジェスト初出として採用

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-07-04 〜 2026-07-10) の全 CVE/GHSA/URL を除外済み。*
