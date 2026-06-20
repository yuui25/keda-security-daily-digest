# KEDA Daily Digest — 2026-06-21 (JST)

> 採用範囲: 公開日 2026-06-19 〜 2026-06-21
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Microsoft Defender リサーチが「AutoJack」を公開し、AI ブラウジングエージェント (AutoGen Studio) が悪意あるウェブページ一枚でホスト RCE の踏み台になり得ることを実証。Splunk Enterprise (CVE-2026-20253、CVSS 9.8) は CISA KEV 追加 (6/18) と野外悪用確認が相次ぎ、連邦機関修正期限が今日 (6/21) ——watchTowr PoC から 9 日で KEV 入りの急展開。Apple A12/A13 チップ搭載の iPhone XS/XR/11 系に物理アクセス経由のパッチ不能 BootROM エクスプロイト "usbliter8" が公開され、デバイス交換以外の根本的修正手段がない状況。

## AI 関連ニュース

- **[2026-06-18/19]** [Microsoft、AI エージェントを経由したホスト RCE 攻撃チェーン "AutoJack" を公開 — AutoGen Studio の MCP WebSocket が localhost 発リクエストのオリジン制限を欠いており、悪意あるページを閲覧した AI エージェントが WebSocket 接続 → 認証なし → 攻撃者制御パラメーターをシェルに直接渡しホスト上で任意プロセス起動; 脆弱版 0.4.3.dev1/dev2 は PyPI 上に未削除; 安定版 0.4.2.2 は影響なし; 修正は GitHub main commit b047730 (PR #7362) のみで安定リリース未提供](https://www.microsoft.com/en-us/security/blog/2026/06/18/autojack-single-page-rce-host-running-ai-agent/) *(Microsoft Security Blog / TechRadar / GBHackers / SecurityWeek)*

- **[続報][2026-06-19/20]** [Anthropic Fable 5/Mythos 5 輸出規制 — Trump 大統領が G7 から記者団に「協議は順調 (going fine)」と発言、6/12 の禁止命令以降初の大統領コメント; 返金期限 2026-06-20 23:59 が到来し払い戻し手続き完了; 米商務省との交渉継続中で正式解除発表はなし](https://techjacksolutions.com/ai-brief/fable-5-refund-window-closes-june-20-what-anthropics-billing/) *(TechJack Solutions / TechTimes / explainx.ai)*

- **[2026-06-19/20]** [デバイスコードフィッシング、スパイ専用技法から犯罪インフラへ転落 — Push Security が 2026 年上半期で検出数 37 倍増・18 種キット確認・全主要 PhaaS ベンダーが採用を報告; OAuth デバイス認証フローを模倣し MFA をバイパスしてセッショントークン窃取 → メール・OneDrive の自動キーワードスイープへ連鎖; EvilTokens が民主化を牽引](https://www.bleepingcomputer.com/news/security/device-code-phishing-attacks-surge-37x-as-new-kits-spread-online/) *(BleepingComputer / Push Security)*

## セキュリティ関連ニュース

- **[2026-06-18/19]** [Apple A12/A13 チップ搭載デバイスにパッチ不能な BootROM エクスプロイト "usbliter8" が公開 — Synopsys DWC2 USB コントローラの DMA 書き込みポインター算術バグを DFU モード経由で突き、BootROM 実行前にカスタムコードを走らせ iOS 署名検証を無効化; iPhone XS/XS Max/XR、iPhone 11/11 Pro/11 Pro Max、iPad Air 第 3 世代、iPad mini 第 5 世代等が対象; CVE 未採番・野外悪用未確認・物理アクセスが必要だが BootROM は不変のためソフトウェアパッチ不可](https://www.theregister.com/security/2026/06/19/researchers-drop-checkm8-style-bootrom-exploit-for-a12-and-a13-iphones/) *(The Register / Privacy Guides / 9to5Mac / THN)*

- **[続報][2026-06-18/19]** [Splunk Enterprise CVE-2026-20253 が CISA KEV に追加、野外悪用確認で連邦機関修正期限 6/21 — 6/18 に CISA KEV 追加、同日 Splunk が「限定的な野外悪用を確認」とアドバイザリを更新; watchTowr が 6/12 に PostgreSQL `lo_export` チェーン経由の RCE PoC を公開しており PoC 公開 6 日でエクスプロイト流通; 修正版: 10.0.7 / 10.2.4](https://www.helpnetsecurity.com/2026/06/19/splunk-vulnerability-cve-2026-20253-exploited/) *(HelpNetSecurity / SecurityAffairs / GBHackers)*

- **[2026-06-18/19]** [ESET、Gentlemen RaaS の専用 EDR 無効化フレームワーク "GentleKiller" を詳細解析 — 独自開発の GentleKiller (8 亜種) に加え HexKiller・ThrottleBlood・HavocKiller を affiliates に配布; 48 製品・400 以上のセキュリティプロセスを標的に BYOVD カーネルドライバ悪用で EDR を無効化してからランサムウェアを展開; 478 組織・70 カ国以上に侵害; 6/10 に Brian Krebs が運営者を Alexander Andreevich Yapaev (ロシア・イジェフスク) と特定](https://www.welivesecurity.com/en/eset-research/killing-me-gently-inside-gentlemens-edr-killer-framework/) *(ESET Research / TechTimes / Help Net Security)*

- **[2026-06-19]** [Telegram CEO Durov、Reliance Jio (Meta 部分出資) による BGP ハイジャックでインド国外ユーザーの Telegram アクセスを妨害していると主張 — インド試験漏洩対応でのアクセス制限後、UAE を含む国外ユーザーにも影響が波及; Reliance Jio は関与を否定](https://www.theregister.com/networks/2026/06/19/telegram-founder-accuses-meta-of-sabotaging-access-in-india-with-bgp-hijacks/) *(The Register / MediaNama / Cybernews)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-19 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| [続報] CVE-2026-20253 | Splunk Enterprise 10.0.x <10.0.7 / 10.2.x <10.2.4 | CWE-306 / **9.8** | PostgreSQL サイドカーサービスエンドポイントに認証チェックなし → 非認証攻撃者がネットワーク越しに任意ファイル生成・切り詰め → `lo_export` チェーン経由で RCE | [SVD-2026-0603](https://advisory.splunk.com/advisories/SVD-2026-0603) | **CISA KEV 2026-06-18 追加** / **野外悪用確認** / 連邦機関修正期限 6/21 / watchTowr PoC 公開済 |
| GHSA-869j-r97x-hx2g / CVE未採番 | Anki `aqt` (pip) ≤ 25.9.2 | CWE-346+CWE-22 / **8.7** | Anki ローカル HTTP サーバーが Origin ヘッダーを検証しない → 悪意あるウェブページからの WebSocket 接続が成立 → パストラバーサルで既知パスの任意ローカルファイルを外部サイトへ送信; Firefox が Chrome より脆弱 (Private Network Access 未実装) | [aqt 25.9.3](https://github.com/ankitects/anki/releases) | 2026-06-19 GHSA 公開 / Anki は世界的に広く使われる SRS アプリ / 開発環境で常駐する局所 HTTP サーバーへの類似攻撃面 (Jupyter / Vite 等) にバリアントハント推奨 |
| GHSA-f4xh-w4cj-qxq8 / CVE未採番 | LangSmith SDK (pip) `langsmith` < 0.8.18 | CWE-22+CWE-346+CWE-843 / **7.7** | HTTP トレーシングヘッダのフィールドを型チェックなしでランオブジェクトにマージ → CWE-843 型混乱でファイルシステムアクセス制限のゲートをバイパス → サーバーが攻撃者指定パスのファイルを開いて LangSmith にトレース添付としてアップロード → 任意ファイル読み取り | [langsmith 0.8.18](https://github.com/langchain-ai/langsmith-sdk/security/advisories/GHSA-f4xh-w4cj-qxq8) | 2026-06-19 GHSA 公開 / AI MLOps パイプラインで広く採用 / トレーシングヘッダー経由の攻撃面は LiteLLM・OpenTelemetry 等の隣接実装にバリアントハント推奨 |
| GHSA-cc8f-fcx3-gpjr / CVE未採番 | SurrealDB (Rust) < 3.1.5 | CWE-552 / **7.7** | `SURREAL_FILE_ALLOWLIST` がデフォルト空の設定で EDITOR/OWNER ロールユーザーが `DEFINE ANALYZER mapper()` フィルターに任意ファイルパスを指定 → クエリのエラーメッセージ経由でファイル内容 (先頭行) が返却; 環境変数・シークレット漏洩リスク | [SurrealDB 3.1.5](https://github.com/surrealdb/surrealdb/security/advisories/GHSA-cc8f-fcx3-gpjr) | 2026-06-19 GHSA 公開 / セキュアデフォルト欠如パターン (SURREAL_FILE_ALLOWLIST が空=制限なし) / 同種のフルテキスト検索アナライザー実装を持つ他の DB エンジンへのバリアントハント推奨 |

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|

> 直近2日間に該当する新規国内ニュースは確認できませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 28 ソース (Microsoft Security Blog, TechRadar, The Register, Privacy Guides, 9to5Mac, THN, ESET WeLiveSecurity, TechTimes, HelpNetSecurity, SecurityAffairs, GBHackers, BleepingComputer, Push Security, SecurityWeek, cybernews, TechJack Solutions, explainx.ai, The Register Networks, MediaNama, GitHub Advisory Database (GHSA), splunk advisory, OSV.dev, CISA KEV, SOCRadar, Krebs on Security, Rapid7, Horizon3.ai, watchTowr Labs)
- 採用件数: AI=3 / Security=4 / CVE=4 / 国内=0
- 採用件数が目安 (各 8〜12件) を下回った理由:
  - 採用窓 (2026-06-19〜21) は週末 (土〜月) にあたり、主要 AI ラボからの大型モデルリリース・脆弱性公開ペースが週末のため低調
  - Gemini 3.5 Pro は「6月中リリース予定」と発表済みだが 6/20 時点で GA 未到達
  - 多くの注目ニュース (FortiBleed, Klue/Salesforce breach, NGINX patches, SpaceX/Cursor, Accenture/Dragos等) は直近 7 日の excluded_set に収録済み
- 除外理由内訳:
  - 古すぎ (公開日 < 2026-06-19):
    - CVE-2026-50751 Check Point VPN IKEv1 auth bypass (6/8 開示)
    - CVE-2025-48595 Android zero-day CISA KEV (6/2 追加)
    - CVE-2026-41940 cPanel WHM auth bypass (4/29 watchTowr公開)
    - CVE-2026-21902 Juniper Junos Evolved RCE (2/26 開示)
    - CVE-2026-21858 n8n Ni8mare (1/7 開示)
    - デバイスコードフィッシング BleepingComputer 記事 (日付確認できず、Push Securityブログは6月初頭が初出)
    - Microsoft AutoJack 一次公開 (6/18 Microsoft Blog) → 二次報道 (6/19) で採用
    - White House AI EO (6/2 署名)
    - G7 Anthropic+DeepMind AI 連合提唱 (6/17 G7サミット)
    - OpenAI S-1 SEC提出 (6/10)
    - Gravity SMTP WordPress (CVE-2026-4020) 初期公開 (3/17) ・スパイク (6/6)
    - Vite CVE-2026-39363 (4/6 公開)
    - Babel CVE-2026-49356 (6/13 公開, Low CVSS)
    - Splunk CVE-2026-20253 初出 (June 15 digest 掲載済み) → KEV追加・野外悪用確認として [続報]
  - 重複 (excluded_set 直近 7 ダイジェスト 2026-06-14 〜 2026-06-20):
    - FortiBleed 継続報道, Klue/Salesforce breach, SpaceX/Cursor acquisition
    - NGINX CVE-2026-42530/42055, Node.js CVE-2026-48933/48618
    - ESET FishMonger/SprySOCKS, Fable 5 輸出規制 初報, Antigravity CLI, Accenture/Dragos
    - その他 excluded_set 全 CVE/GHSA
  - 日付不明/確認不可:
    - DaikyoNishikawa LockBit 侵害 — Privacy Guides ラウンドアップ (6/12-18対象) で言及があるが 6/19 以降の新規公開か確認不能のため除外
    - BleepingComputer デバイスコードフィッシング記事の正確な公開日 (HTTP 403, 「6/20」は本文内の "as of" 記述)
- 取得失敗ソース (HTTP 403): bleepingcomputer.com 個別記事, thehackernews.com 個別記事, watchTowr Labs 個別記事, anthropic.com/news, openai.com/news, cisa.gov/known-exploited-vulnerabilities-catalog, labs.watchtowr.com 個別記事 — WebSearch スニペット・複数独立媒体で内容・日付を補完

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-06-14 〜 2026-06-20) の全 CVE/GHSA/URL を除外済み。*
