# KEDA Daily Digest — 2026-07-02 (JST)

> 採用範囲: 公開日 2026-06-30 〜 2026-07-02 (JST)
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Anthropic が Claude Sonnet 5 を正式公開し Fable 5 / Mythos 5 の輸出規制解除も同日に実現、モデル可用性が一気に回復した一方、Cato AI Labs が Cursor IDE への Zero-Click プロンプトインジェクション→RCE「DuneSlide」を公開し LayerX の BioShocking 研究では AI ブラウザ 6 製品が全て認証情報窃取に陥落することが示された。インフラ面では Progress Kemp LoadMaster の CVSS 9.8 未認証 RCE (CVE-2026-8037) が watchTowr 公開後に即悪用確認、Langflow CVE-2026-33017 を狙う Monero マイナー展開キャンペーンが継続中で AI インフラを直接標的とする攻撃チェーンが具現化している。

---

## AI 関連ニュース

- **[2026-07-01]** [Anthropic が Claude Sonnet 5 を正式リリース](https://techcrunch.com/2026/06/30/anthropic-launches-claude-sonnet-5-as-a-cheaper-way-to-run-agents/) — 推論・ツール使用・コーディングで Opus 4.8 に迫る性能を実現しつつ API 価格を $2/$10 (8/31 まで、以降 $3/$15) に設定; Free/Pro プランのデフォルトモデルに採用; Cyber 悪用ブロック機能をデフォルト有効化 *(TechCrunch / Help Net Security)*

- **[続報][2026-07-01]** [Anthropic、Claude Fable 5 & Mythos 5 を全面回復](https://www.coindesk.com/tech/2026/07/01/anthropic-restores-ai-models-fable-mythos-after-the-u-s-lifts-export-controls) — 米商務省が 6/30 に輸出規制を解除; Fable 5 は Claude.ai・Platform・Code・Cowork 全製品で即日再提供; Mythos 5 は政府承認済み米国組織向けに 6/26 から復旧中; 規制の発端は Amazon 研究者によるジェイルブレーク報告でサイバー安全保障上の懸念が理由 *(CoinDesk / Euronews / 9to5Mac)*

- **[2026-07-01]** [Cato AI Labs が Cursor IDE「DuneSlide」(CVE-2026-50548/50549、CVSS 9.8) を公開](https://thehackernews.com/2026/07/critical-cursor-flaws-could-let-prompt.html) — MCP サーバー応答・汚染 Web 検索結果を起点とするゼロクリックプロンプトインジェクションでサンドボックスを脱出し任意コード実行; Cursor < 3.0 が影響対象、4/2 リリースの 3.0 で修正済み *(THN / Cato AI Labs)*

- **[2026-07-01]** [BioShocking: LayerX 研究、AI ブラウザ 6 製品全てがフィクション誘導プロンプトインジェクションで認証情報を外部転送](https://www.malwarebytes.com/blog/ai/2026/07/bioshocking-when-gaming-ai-agents-is-no-longer-a-game) — BioShock ゲームシナリオで Agent の安全規則を無効化→テスト Repo から認証情報を窃取; ChatGPT Atlas・Perplexity Comet・Fellou・Genspark Browser・Sigma Browser・Claude Chrome プラグインで実証成功; OpenAI のみ修正済み、Perplexity は報告クローズ *(Malwarebytes / BleepingComputer / SC World)*

- **[2026-06-30]** [OpenAI が計算生物学向けベンチマーク「GeneBench-Pro」を公開](https://openai.com/index/introducing-genebench-pro/) — ゲノミクス・定量生物学・臨床医学 129 問で AI エージェントを評価; 最高難度では GPT-5.6 Sol が 28.7%、Claude Opus 4.8 が 16.0% と上位モデルでも 3 割未満; AI の実科学応用能力の限界を可視化 *(OpenAI / AlphaSignal)*

- **[2026-06-30]** [Colorado AI Act (SB 26-189) が本日施行](https://www.cbsnews.com/chicago/news/new-illinois-laws-july-1-2026-cocktails-ai-bullying-prediction-market-regulation/) — 雇用・住宅・ローン等の重要決定に AI を使用する企業に AI 利用の開示とガバナンス義務が発効; 欧州 AI 法に次ぐ包括的な州レベル AI 規制; テキサス Responsible AI Governance Act・イリノイ AI いじめ規制も連鎖施行 *(CBS Chicago / Gunderson Dettmer)*

---

## セキュリティ関連ニュース

- **[2026-06-30]** [watchTowr、Progress Kemp LoadMaster CVE-2026-8037 (CVSS 9.8) の技術詳細と PoC を公開](https://labs.watchtowr.com/enterprise-tech-in-shell-out-progress-kemp-loadmaster-uninitialized-heap-to-pre-auth-rce-cve-2026-8037/) — API の escape_quotes() が malloc() で未初期化ヒープを確保しヌルターミネーターを欠落→シェルコマンドへの引数破損→認証不要 root 権限 RCE; eSentire が即日悪用を確認; GA 7.2.63.2 / LTSF 7.2.54.18 で修正 *(watchTowr Labs / THN / GuardianMSSP)*

- **[2026-06-30]** [Langflow CVE-2026-33017 を悪用した Monero マイナー展開キャンペーンが継続](https://www.trendmicro.com/en_us/research/26/f/from-langflow-to-monero-inside-cve-2026-33017-cryptominer.html) — 3/27〜4/15 の 19 日間に渡る攻撃で露出 AI エンドポイントから Monero 採掘; SSH 鍵再利用ワームで横展開; CISA KEV (3/26 追加) 後も未パッチ Langflow (≤1.8.2) が多数残存; 1.9.0 への即時更新と AUTO_LOGIN=false 設定を強く推奨 *(Trend Micro / BleepingComputer)*

- **[2026-07-01]** [VEIL#DROP: Blogger を C2 ドロッパーとして悪用する PureLogs スティーラー配布キャンペーン](https://thehackernews.com/2026/07/veildrop-malware-chain-uses-blogger.html) — transcript.pdf.js を模した JS が PowerShell 経由で Blogspot からペイロードを in-memory 取得; PDF 偽装で横展開しながら PureLogs .NET スティーラー (ブラウザ資格情報・Cookie・暗号資産ウォレット窃取) を展開; Securonix が VEIL#DROP と命名 *(THN / Infosecurity Magazine)*

- **[2026-07-01]** [SEO ポイズニングサイトが ScreenConnect を踏み台に AsyncRAT を展開する大規模多言語キャンペーン](https://thehackernews.com/2026/07/seo-poisoned-software-sites-abuse.html) — Kaspersky が 90+ ドメイン (10 言語) を確認; OBS Studio・Bandicam 等の人気ソフト偽インストーラーから ScreenConnect を介した PowerShell スクリプトが Defender 除外設定・UAC 無効化を実行後に AsyncRAT をプロセスホローイング展開; 画面録画・資格情報窃取が目的 *(THN / Kaspersky)*

- **[2026-07-01]** [DHS、HSIN (国土安全保障情報共有ネットワーク) への侵害を正式確認](https://www.bleepingcomputer.com/news/security/dhs-confirms-hackers-breached-hsin-info-sharing-platform/) — 5月末〜6月初旬に HSIN サーバーと SharePoint システムが不明の脅威アクターに侵害; 機密分類ネットワークへの影響はなく HSIN はサービス継続中; DHS が「システム隔離・脆弱性緩和・包括的フォレンジック調査」を実施中と声明; 帰属は未確定 *(BleepingComputer / Nextgov)*

- **[2026-07-01]** [Microsoft 365 環境を狙う 2 週間で 8,100 万回のパスワードスプレー攻撃](https://www.bleepingcomputer.com/news/security/hackers-target-microsoft-365-accounts-with-81-million-login-attempts/) — 脅威アクターが Azure CLI 経由で過去の漏洩資格情報を利用した大規模スプレー攻撃を実施; 認証エラーが通常ログに残りにくい CLI 経由を悪用; MFA 未設定の M365 環境が標的 *(BleepingComputer)*

- **[2026-07-01]** [Operation Navy Ghost: PyPI に 8 件の偽 Pyrogram パッケージ (Pyronut バックドア) — Telegram bot 開発者を標的](https://www.bleepingcomputer.com/news/security/malicious-pypi-packages-give-hackers-control-of-telegram-bot-servers/) — 2025/11 〜 2026/6 の 8 ヶ月間にわたり 3 つの公開者 ID が vlifegram・kelragram 等 8 パッケージを PyPI に公開; secret.py が /e コマンドで任意 Python 実行・/shell でシステムコマンド実行を可能にする RAT を埋め込み; ~/.ssh/known_hosts を読み取り横展開するワーム機能付き *(BleepingComputer / Checkmarx / Endor Labs)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-30 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-50548 + CVE-2026-50549 "DuneSlide" | Cursor IDE < 3.0 (全 OS) | CWE-1021 / **9.8** | (50548) `run_terminal_cmd` の `working_directory` が LLM 制御パラメータ → プロンプトインジェクションで任意パスへ書き込み → `cursorsandbox` ヘルパー上書きでサンドボックス無効化 → 以降のコマンドが完全非サンドボックス RCE; (50549) symlink の正規化チェック失敗時に未検証シンクリンクパスをフォールバックで信頼 → サンドボックス外への任意ファイル書き込み → RCE | [Cursor 3.0 (2026-04-02)](https://www.cursor.com/changelog) | 2026-07-01 Cato AI Labs 公開 / MCP サーバー応答・汚染 Web 検索起点の Zero-Click / GitHub Copilot・Windsurf 等 AI IDE のサンドボックス実装へバリアントハント推奨 |
| CVE-2026-8037 | Progress Kemp LoadMaster ≤ GA 7.2.63.1 / LTSF 7.2.54.17 (API 有効時) | CWE-908 / **9.8** | `escape_quotes()` が `malloc()` で未初期化ヒープバッファを確保しヌルターミネーターを付加しない → 入力エスケープ処理が破損したままシェルコマンドへ渡される → 未認証攻撃者がネットワーク越しに root として任意コマンド実行 | [GA 7.2.63.2 / LTSF 7.2.54.18 (Progress Kemp)](https://support.kemptechnologies.com/) | 2026-06-30 watchTowr 公開 / eSentire が即日悪用確認 / 認証不要 / ロードバランサーへの CVSS 9.8 は外部公開環境で最高リスク |
| GHSA-4vgr-h27g-cf9p | SurrealDB < 3.1.0 (Rust) | CWE-362 / **8.1** | HTTP `/rpc` エンドポイントで未認証リクエストと認証済みセッションが同一の可変認証状態を共有 → TOCTOU 競合で未認証リクエストが認証済みセッション権限を継承 → セッション ID なしにデータベースの任意操作が可能 | [surrealdb@2f53e6e / fd800fc (v3.1.0)](https://github.com/surrealdb/surrealdb/releases) | 2026-06-30 GHSA 公開 / 認証不要 / マルチモデル DB の HTTP RPC 認証状態管理パターン全般へバリアントハント推奨 |
| GHSA-wjjj-24cx-f28g | SurrealDB < 3.1.0 (Rust) | CWE-20 / **High** | 未認証攻撃者が不正形式の RPC メッセージを送信 → サーバー側例外が適切にキャッチされずパニック → サービス全体の DoS | [v3.1.0](https://github.com/surrealdb/surrealdb/releases) | 2026-06-30 GHSA 公開 / 認証不要の DoS / 同バッチで session UUID 漏洩 (GHSA-5qfp-32cf-69jh) も同日公開 |
| CVE-2026-49987 / GHSA-9mm9-rqhj-j5mx | repomix (npm) < 1.14.1 | CWE-88 / **8.8** | `--remote-branch` 引数が git サブプロセス呼び出し前に検証されず → `--upload-pack=cmd` 等のオプション文字列をブランチ名として注入 (引数インジェクション) → 認証済みユーザーが任意コマンド実行 | [repomix v1.14.1 (GHSA 参照)](https://github.com/yamadashy/repomix/releases) | 2026-06-30 GHSA 公開 / AI コーディング / MCP ツールからの repomix 利用が多数 / git ブランチ引数を受け取る全 OSS ツールへバリアントハント推奨 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-06-30 | JVNDB-2026-000093 / JVN | RPG Maker MV および MZ (Windows 版) に OS コマンドインジェクション脆弱性 — 細工したプロジェクトファイルをロードすると攻撃者が任意コマンドを実行可能; KADOKAWA が修正版を提供 | CVSS 7.8 / 高 | [JVN](https://jvndb.jvn.jp/en/contents/2026/JVNDB-2026-000093.html) |

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| thehackernews.com (July 2026 filter) | DuneSlide (CVE-2026-50548/50549), BioShocking, VEIL#DROP, ScreenConnect AsyncRAT 取得 ✓ |
| Anthropic newsroom / TechCrunch / Help Net Security | Claude Sonnet 5 (2026-07-01) 確認 ✓ |
| CoinDesk / Euronews / 9to5Mac | Fable 5 / Mythos 5 復旧 (2026-07-01) 確認 ✓ |
| watchTowr Labs | CVE-2026-8037 Kemp LoadMaster (2026-06-30) 403 → WebSearch スニペット代替 ✓ |
| Trend Micro / BleepingComputer | Langflow CVE-2026-33017 Monero キャンペーン (2026-06-30) 確認 ✓ |
| BleepingComputer (July 1 feed) | DHS HSIN 侵害確認・Microsoft 365 パスワードスプレー・Operation Navy Ghost 取得 ✓ |
| OpenAI (GeneBench-Pro) | 2026-06-30 リリース確認 ✓ |
| github.com/advisories (published:2026-06-30) | SurrealDB batch (GHSA-4vgr / GHSA-wjjj 等), repomix CVE-2026-49987, sigstore CVE-2026-48815 取得; 後者2件の元発表日を確認 ✓ |
| JPCERT / JVN (June 30 filter) | JVNDB-2026-000093 (RPG Maker MV/MZ) 取得 ✓ |
| nvd.nist.gov / cisa.gov/kev | 403 → WebSearch スニペット代替 |
| labs.watchtowr.com | 403 — WebSearch スニペットで代替 |
| thehackernews.com | 403 — WebSearch スニペットで代替 |
| bleepingcomputer.com | 403 — WebSearch スニペットで代替 |

### 集計サマリ

- **巡回ソース数**: 15+
- **採用件数**: AI=6 / Security=7 / CVE=5 / 国内=1
- **除外理由内訳**:
  - 古すぎ (3日超): GPT-5.6 Sol/Terra/Luna GA 未定 (Jun 26-27 掲載済み), Anthropic Google/Broadcom compute deal (Apr 2026), Gemini 3.1 Flash-Lite GA (May 2026), Microsoft Defender BlueHammer CVE-2026-33825 (Apr 2026), Fission CVE-2026-50566 (Jun 10 推定), Langflow CVE-2026-33017 **CVE テーブルから除外** (3/17 元発表、6/30 のニュースは Security ニュース欄に記載)
  - 重複 (excluded_set 一致): Claude Science (Jul 1 digest), Azure GA Claude (Jul 1 digest), Perplexity AI 偽拡張 (Jul 1 digest), SimpleHelp CVE-2026-48558 系 (Jun 30/Jul 1 digest), Oracle EBS CVE-2026-46817 (Jun 30 digest), SigNoz/Gorse/Mythic/Nitter 各 CVE (Jun 30 digest)
  - 日付不明: 0件
- **GitHub Advisory 注意**: GHSA-4vgr/GHSA-wjjj/CVE-2026-49987/CVE-2026-48815 は GitHub review date = 2026-06-30 だが CVE 元発表日は 2026-05-27; 本ダイジェストでは公開ポリシーとして「GitHub が公開したタイミング (2026-06-30)」を採用。sigstore CVE-2026-48815 は CVSS 7.5 だが Sigstore Fulcio SSRF (CVE-2026-49478) が Jul 1 digest 掲載済みのためコンテキスト重複として優先度下げ
- **取得失敗ソース**: labs.watchtowr.com (403), thehackernews.com (403), bleepingcomputer.com (403), nvd.nist.gov (403), cisa.gov (403) — 全て WebSearch スニペットで代替確認済み

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-06-25 〜 2026-07-01) の全 CVE/GHSA/URL を除外済み。*
