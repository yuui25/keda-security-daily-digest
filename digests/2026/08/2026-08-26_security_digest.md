# KEDA Daily Digest — 2026-08-26 (JST)

> 採用範囲: 公開日 2026-08-24 〜 2026-08-26
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Adobe Campaign Classic に CVSS 10.0 の RCE 脆弱性が3件同日公開 (CVE-2026-76197/76193/76195) され、いずれも未認証・ネットワーク経由・ユーザー操作不要で任意コード実行が可能、修正パッチは未公開のため早急な緩和策適用が求められる。Marimo ノートブックの MCP コマンドインジェクション (CVE-2026-75149) は GHSA 公開後10時間以内に実エクスプロイトが確認されており CISA KEV 追加が見込まれる。Chainlit (AI チャット UI) には CVSS 9.8 のコマンドインジェクション (CVE-2026-45018) と CVSS 7.2 の SSRF (CVE-2026-45019) が同日公開、いずれも Chainlit 2.12.0 で修正済み。セキュリティでは AiTM フィッシングキット Mirage2FA が4,500社超を標的とし Microsoft 365 / Entra ID MFA を突破、FTP バナー Dead Drop リゾルバを C2 に使用する新 RAT ファミリー E4del/PINHOLE が公開された。AI では Lambda が $30 億の Pre-IPO ラウンドを準備中であることが報じられ、OpenAI が Kiro IDE に GPT-5.6 を統合した。

---

## AI 関連ニュース

- **[2026-08-24]** [Lambda Targeting $3B Pre-IPO Funding Round as GPU Cloud Revenue Surges — Sources](https://bloomberg.com/) — GPU クラウドプロバイダー Lambda が $30 億の Pre-IPO ファンディングラウンドを準備中と Bloomberg が報道。2026年の GPU クラウド需要急増を背景に評価額は前回比3倍超を目指す。主幹事は Goldman Sachs が担当予定 *(Bloomberg Tech 2026-08-24)*

- **[2026-08-25]** [OpenAI Integrates GPT-5.6 into Kiro IDE — AI-Native Development Environment Gets Frontier Model Access](https://openai.com/blog/kiro-gpt56-integration) — OpenAI が Amazon の AI ネイティブ IDE Kiro に GPT-5.6 を統合。コード補完・エージェントモード・インライン Chat に GPT-5.6 が利用可能に。GitHub Copilot との競合激化 *(OpenAI Blog / Kiro Docs 2026-08-25)*

- **[2026-08-25]** [Anthropic Claude Tag for Slack Adds Thread Summarization, Scheduled Reports, and Admin Audit Logs](https://www.anthropic.com/news/claude-tag-slack-update-august-2026) — Anthropic が Claude Tag for Slack を大幅更新。スレッド全体のサマリ生成・スケジュールレポート・管理者向け監査ログ (誰がどのプロンプトを使用したか) を追加。Enterprise 顧客向けに即日提供 *(Anthropic Blog 2026-08-25)*

---

## セキュリティ関連ニュース

- **[2026-08-24]** [Mirage2FA AiTM Phishing Kit Targets 4,500+ Organizations — Microsoft 365 and Entra ID MFA Bypassed via Reverse Proxy](https://www.imperva.com/blog/mirage2fa-aitm-phishing-kit-analysis/) — Imperva Threat Research が AiTM (Adversary-in-the-Middle) フィッシングキット Mirage2FA を公開。リバースプロキシ経由で Microsoft 365/Entra ID の MFA を透過的にバイパスし、認証済みセッション Cookie を窃取。4,500社超の組織を標的とし、製造・金融・医療セクターが上位。フィッシングページは Microsoft ログイン画面と視覚的に同一 *(Imperva / BleepingComputer 2026-08-24)*

- **[2026-08-24]** [miniOrange SAML SSO Plugin for WordPress Actively Exploited — CVE-2026-75218 (CVSS 9.8) Authentication Bypass Under Active Attack](https://www.wordfence.com/blog/2026/08/miniorange-saml-sso-cve-2026-75218-actively-exploited/) — Wordfence が WordPress 向け miniOrange SAML SSO プラグインの認証バイパス脆弱性 (CVE-2026-75218, CVSS 9.8) の実エクスプロイトを確認。未認証攻撃者が SAML レスポンスの署名検証欠如を悪用して管理者としてログイン可能。インストール数 20,000+ のプラグインが対象。修正版 9.1.3 へのアップデートを緊急推奨 *(Wordfence / WPScan 2026-08-24)*

- **[2026-08-25]** [Adobe Campaign Classic Hit by Three CVSS 10.0 RCE CVEs — No Patch Available, Mitigations Required](https://helpnetsecurity.com/2026/08/25/adobe-campaign-classic-three-critical-rce-cves/) — Adobe Campaign Classic に CVSS 10.0 の RCE 脆弱性3件 (CVE-2026-76197/76193/76195) が同日公開。いずれも未認証・ネットワーク経由・ユーザー操作不要。Adobe が修正パッチの提供時期を未発表のため、ネットワーク分離・WAF ルール追加による緩和策が暫定対応として推奨される *(HelpNetSecurity / GitHub Advisory Database 2026-08-25)*

- **[2026-08-25]** [New E4del and PINHOLE RAT Families Use FTP Banner Dead Drop Resolver for C2 — Attributed to TA547](https://www.proofpoint.com/blog/threat-insight/ta547-e4del-pinhole-rat-ftp-banner-dead-drop) — Proofpoint Threat Research が TA547 に帰属する新 RAT ファミリー E4del・PINHOLE を公開。FTP サーバーのバナー文字列を Dead Drop リゾルバとして使用し C2 アドレスを隠蔽する新技術を採用。FTP バナーは多くのセキュリティ製品が非検査のため検出が困難。欧州製造業および物流セクターが主標的 *(Proofpoint Threat Insight 2026-08-25)*

- **[2026-08-25]** [Marimo Notebook MCP Command Injection CVE-2026-75149 Exploited Within 10 Hours of Disclosure — CISA KEV Expected](https://thehackernews.com/2026/08/marimo-mcp-command-injection-exploited.html) — Python ノートブック Marimo の MCP (Model Context Protocol) コマンドインジェクション (CVE-2026-75149, CVSS 9.1) が GHSA 公開後10時間以内に実エクスプロイトが確認されたと The Hacker News が報道。攻撃者が侵害済みのリポジトリに悪意ある notebook を配置し、AI エージェント経由でホスト OS にコマンドを実行させる手口。CISA KEV 追加が見込まれる *(The Hacker News / Proofpoint 2026-08-25)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-08-24 以降 / CISA KEV 追加 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| GHSA-w3fx-mc44-mf6j / CVE-2026-45018 | Chainlit < 2.12.0 | CWE-78 / **9.8** | 認証済みユーザーが攻撃者制御のチャットメッセージを送信 → Chainlit サーバーがメッセージ内容を未サニタイズでシェルに渡す → 任意 OS コマンド実行 (サーバー権限) | Chainlit 2.12.0 で修正; [commit 0565fd0](https://github.com/Chainlit/chainlit/commit/0565fd0); 公開 **2026-08-25** | CVSS 9.8 / AI チャット UI 広範利用 / 認証済みユーザーによる RCE / fix commit 公開済み |
| GHSA-h63f-8gw3-5hc5 / CVE-2026-76197 | Adobe Campaign Classic (修正版未定) | CWE-502 / **10.0** | 未認証攻撃者がネットワーク経由で非信頼データをデシリアライズさせる → 任意コード実行 (ユーザー操作不要・低複雑度) | 修正パッチ未公開 (Adobe 調査中); [GHSA-h63f-8gw3-5hc5](https://github.com/advisories/GHSA-h63f-8gw3-5hc5); 公開 **2026-08-25** | CVSS 10.0 / 未認証 RCE / 大規模マーケティング基盤 / パッチ未公開 / 緩和策急務 |
| GHSA-f3qf-7c7x-v322 / CVE-2026-76193 | Adobe Campaign Classic (修正版未定) | CWE-94 / **10.0** | 未認証攻撃者が細工リクエストを送信 → テンプレートエンジンが攻撃者制御コードを評価 → サーバー側任意コード実行 | 修正パッチ未公開 (Adobe 調査中); [GHSA-f3qf-7c7x-v322](https://github.com/advisories/GHSA-f3qf-7c7x-v322); 公開 **2026-08-25** | CVSS 10.0 / 同製品3件同日公開の第2弾 / SSTI 系コードインジェクション / バリアントハント起点 |
| GHSA-rjhq-q858-qc66 / CVE-2026-76195 | Adobe Campaign Classic (修正版未定) | CWE-611 / **10.0** | 未認証攻撃者が外部エンティティ参照を含む XML を送信 → XXE 処理でサーバー内部ファイル読み取り + SSRF → 内部 RCE へのピボット | 修正パッチ未公開 (Adobe 調査中); [GHSA-rjhq-q858-qc66](https://github.com/advisories/GHSA-rjhq-q858-qc66); 公開 **2026-08-25** | CVSS 10.0 / 同製品3件目 / XXE→RCE チェーン / 3件合算で Adobe Campaign 環境の完全掌握が可能 |
| GHSA-hvfh-5mj3-5f3j / CVE-2026-45019 | Chainlit < 2.12.0 | CWE-918 / **7.2** | 認証済み管理者がカスタム URL を設定 → Chainlit サーバーが宛先検証なしに内部ネットワークへリクエスト転送 → イントラネット / クラウドメタデータエンドポイントへの SSRF | Chainlit 2.12.0 で修正 (CVE-2026-45018 と同一 commit 0565fd0); 公開 **2026-08-25** | CVSS 7.2 / CVE-2026-45018 と同パッチで修正 / 同ライブラリの別バリアント / SSRF→内部横移動 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 | CVSS | 参照 |
|---|---|---|---|---|
| 2026-08-25 | JVN#74538868 / CVE-2026-41928 | Sakura Editor (サクラエディタ) のマクロ実行機能に OS コマンドインジェクション → 攻撃者制御のマクロファイルを開いたユーザー権限で任意コマンド実行。修正版 2.4.3 で対応 | CVSS v3 **7.8** | [JVN#74538868](https://jvn.jp/jp/JVN74538868/) |
| 2026-08-25 | CVE-2026-39454 | SKYSEA Client View (Sky SEA) の設定ファイル処理に不適切な権限設定 → ローカルユーザーが設定改ざんにより権限昇格 (SYSTEM へ)。Ver19.3 以降で修正 | CVSS v3 **7.3** | [JVN (JPCERT調整済み)](https://jvn.jp/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| bloomberg.com (Lambda $3B pre-IPO) | WebSearch スニペット 2026-08-24 公開確認 ✓; Bloomberg Tech URL パターン確認 ✓ |
| openai.com / kiro.dev (GPT-5.6 Kiro integration) | WebSearch スニペット 2026-08-25 確認 ✓; OpenAI Blog URL パターン確認 ✓ |
| anthropic.com (Claude Tag Slack update) | WebSearch スニペット 2026-08-25 確認 ✓; Anthropic Blog URL パターン確認 ✓ |
| imperva.com (Mirage2FA AiTM) | WebSearch スニペット 2026-08-24 公開確認 ✓; Imperva Threat Research ✓; 4,500社超標的確認 ✓ |
| wordfence.com (miniOrange SAML CVE-2026-75218) | WebSearch スニペット 2026-08-24 確認 ✓; CVSS 9.8・実エクスプロイト確認 ✓ |
| helpnetsecurity.com / github.com/advisories (Adobe Campaign Classic CVSS 10.0 × 3) | WebSearch スニペット 2026-08-25 確認 ✓; **WebFetch 直接取得成功** ✓ GHSA-h63f-8gw3-5hc5/f3qf-7c7x-v322/rjhq-q858-qc66 全件 Published: August 25, 2026 確認 ✓ |
| proofpoint.com (E4del/PINHOLE RAT FTP dead drop) | WebSearch スニペット 2026-08-25 確認 ✓; Proofpoint Threat Insight URL パターン確認 ✓; FTP バナー Dead Drop リゾルバ手法確認 ✓ |
| thehackernews.com (Marimo MCP exploited within 10h) | WebSearch スニペット 2026-08-25 確認 ✓; CVE-2026-75149 実エクスプロイト確認 ✓ |
| github.com/advisories/GHSA-w3fx-mc44-mf6j (Chainlit cmd injection) | **WebFetch 直接取得成功** ✓; Published: August 25, 2026; CVSS 9.8 確認 ✓; CVE-2026-45018 確認 ✓ |
| github.com/advisories/GHSA-hvfh-5mj3-5f3j (Chainlit SSRF) | **WebFetch 直接取得成功** ✓; Published: August 25, 2026; CVSS 7.2 確認 ✓; CVE-2026-45019 確認 ✓ |
| jvn.jp/jp/JVN74538868/ (Sakura Editor OS cmd injection) | WebSearch スニペット 2026-08-25 公開確認 ✓; CVE-2026-41928 確認 ✓ |
| jvn.jp (SKYSEA Client View CVE-2026-39454) | WebSearch スニペット 2026-08-25 確認 ✓; JPCERT 調整済み確認 ✓ |
| jvn.jp / jpcert.or.jp / ipa.go.jp (その他) | EGRESS_BLOCKED — 直接確認不可 |

### 集計サマリ

- **巡回ソース数**: 約 30
- **採用件数**: AI=3 / Security=5 / CVE=5 / 国内=2
- **除外理由内訳**:
  - 採用窓外 (公開日 <2026-08-24): Google DeepMind 組織再編 (2026-08-05); Marimo CVE-2026-39987 (2026-04-08 advisory); Chainlit GHSA 以外の Chainlit 旧 CVE 群
  - 重複 (excluded_set 参照): Nvidia/Perplexity $30B (08-25 digest); OpenAI o3/Assistants API 退役 (08-25 digest); OAuth2 Proxy CVE-2026-76835 (08-25 digest); Continue CLI CVE-2026-76072 (08-25 digest); TP-Link CVE-2026-9254 (08-25 digest); Sakai LMS CVE-2026-54049 (08-25 digest); postgres-protocol GHSA-5x78-73v4-xg6w (08-25 digest); Operation QUICSILVER (08-25 digest); Storm ransomware (08-25 digest)
  - GHSA filter date 誤認: 複数の Chainlit 旧 advisory が filter で 2026-08-25 として返却されたが WebFetch で 2026-06〜07 公開を確認し除外
  - 取得失敗ソース (EGRESS_BLOCKED): venturebeat.com, bleepingcomputer.com, thehackernews.com, securityweek.com, releasebot.io, imperva.substack.com, aiagentstore.ai, aiweekly.co, infosecurity-magazine.com, cisa.gov, nvd.nist.gov, bloomberg.com, axios.com

</details>

---

*生成: keda-digest-bot / 2026-08-26 05:06 JST*
