# KEDA Daily Digest — 2026-10-08 (JST)

> 採用範囲: 公開日 2026-10-06 〜 2026-10-08
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Mistral が 1 兆パラメータ級モデル "le Chonk" (Large 4) を 10/6 にサイバーセキュリティリーダー・開発者向けプレビューとして公開し、Anthropic も同日 Project Glasswing を 3 段階ティア構造の「Cyber Verification Program」に刷新した。Pwn2Own Ireland 2026 Day 2 (10/7) では Home Assistant Green および AI インフラカテゴリの Dynamo が攻略され AI 基盤標的の傾向が継続。脆弱性面では Atlassian CVE-2026-21589 の PoC が watchTowr 公開後 2 時間以内に悪用観測へ発展 (続報) し、GitHub Advisory Database では Coraza WAF・Payload CMS・MCP TypeScript SDK を含む合計 6 件の advisory が 10/6 に一斉公開された。

---

## AI 関連ニュース

- **[2026-10-06]** [Mistral が 1 兆パラメータモデル "Large 4 (le Chonk)" を公開 — サイバー・コーディング・製造・金融・マルチモーダルに対応、開発者とサイバーセキュリティリーダーへのプレビュー開始](https://www.cnbc.com/2026/10/06/mistral-ai-model-le-chonk.html) — 中国製オープンウェイトモデルとの性能比較を前面に打ち出す戦略; オープンウェイトの一般公開は 10 月末を予定; 別報道では欧州銀行向け独自サイバーモデルを並行開発中 *(CNBC / Decrypt)*

- **[2026-10-06]** [Anthropic が Project Glasswing を「Cyber Verification Program」3 段階ティア制に再編 — 防御目的組織への Mythos クラスモデルアクセスを拡大](https://www.anthropic.com/news) — Tier 1: CISA/NSA 等政府機関、Tier 2: セキュリティ企業、Tier 3: 認定防衛研究者の 3 段階構造; AWS・Google・Microsoft・CrowdStrike 等初期パートナーは最上位ティアへ自動移行; 100M ドルクレジット枠は継続 *(AIWeekly / Enterprise Times)*

- **[2026-10-07]** [[続報] Pwn2Own Ireland 2026 Day 2: Xint が Home Assistant Green を SSRF+コマンドインジェクションチェーンで攻略 $30,000、Out of Bounds が AI インフラカテゴリ Dynamo を新規ゼロデイで攻略 $40,000](https://www.zerodayinitiative.com/blog/2026/10/7/pwn2own-ireland-2026-day-two-results) — AI インフラカテゴリが Day 1 の Oracle AI DB・OpenAI Codex に続き 2 日連続で成立; Brother MFC-L8970CDW・Chroma への試みは失敗または時間切れ; VinSOC が 2 日間リーダーボードトップ ($97,500 / 11.5pt) *(ZDI / Malware.news)*

- **[2026-10-06]** [ランサムウェア攻撃者 "Azazel" が AI コーディングアシスタントを悪用し Gentlemen グループ傘下で 6 か国・20 社超を攻撃 — ロジスティクス・保険・製薬・医療機器・AI 企業が標的](https://cybersecuritynews.com/ransomware-hacker) — カスタムローダー・難読化コードを AI アシスタントで迅速生成し暗号化と並行データ窃取を実施; AI が攻撃ツールチェーンの「低コード化」装置として定着した典型事例 *(CyberSecurityNews)*

- **[2026-10-06]** [MCP TypeScript SDK OAuth クレデンシャル漏洩 CVE-2026-104850 — 悪意ある MCP サーバーが指定する認可サーバーへ SDK クライアントが無検証で Bearer トークンを送信、AI エージェントなりすましアクセスが可能](https://github.com/advisories/GHSA-r8mh-x5qv-7gg2) — MCP を AI エージェント統合に使う全スタック (Claude・OpenAI 互換ツール含む) に影響; 修正版 SDK への即時更新を推奨 *(GitHub Advisory DB)*

## セキュリティ関連ニュース

- **[2026-10-07]** [[続報] Atlassian Data Center CVE-2026-21589: watchTowr が技術解説と PoC を公開後 2 時間以内にハニーポットで悪用試行を観測 — Crowd 統合環境では JWT 秘密鍵読み取りから管理者権限昇格が可能](https://www.helpnetsecurity.com/2026/10/07/exploitation-critical-atlassian-flaw-cve-2026-21589/) — watchTowr 解析: Crowd 連携環境で JWT 秘密鍵ファイルを読み取り管理者トークンを偽造可能な攻撃経路を実証; Previdian ハニーポットが公開 2 時間後に最初の探索リクエストを検出; 自己ホスト型 DevOps 全環境が即時パッチ対象 *(HelpNetSecurity / watchTowr)*

- **[2026-10-07]** [[続報] Pwn2Own Ireland 2026 Day 2: AI インフラカテゴリで分散推論クラスタ Dynamo が新規ゼロデイにより陥落 — 2026 大会における AI 基盤ゼロデイは計 3 件以上に](https://www.zerodayinitiative.com/blog/2026/10/7/pwn2own-ireland-2026-day-two-results) — Day 1: Oracle Autonomous AI DB (5-zero-day チェーン) + OpenAI Codex; Day 2: Dynamo; AI インフラが Pwn2Own の常設標的カテゴリとして確立; 詳細は 90 日以内にベンダー開示 *(ZDI / SecurityWeek)*

- **[2026-10-06]** [Microsoft が Exchange Server 権限昇格 CVE-2026-96940 を帯域外パッチで修正 — 認証済み攻撃者が同一組織内の他ユーザーメールボックスに無制限アクセス (CVSS 8.8)](https://securityaffairs.com/200476/security/cve-2026-96940-microsoft-fixes-high-severity-exchange-server-flaw.html) — Exchange Online は既修正; オンプレミス管理者は各バージョン向け OOB アップデートを即時適用; MAPI over HTTP チェーン経由の内部委任チェック欠如が根本原因 *(SecurityAffairs)*

- **[2026-10-07]** [NCC Group: 2026 年 8 月のランサムウェア攻撃は月間最多 1,073 件を記録 — Qilin グループが全体 15% を占め首位へ浮上、AI 支援攻撃自動化が件数増を牽引と分析](https://securitybrief.com.au/story/ransomware-attacks-hit-yearly-high-in-august-says-ncc-group) — 前月 960 件比 12% 増; 北米が 44% で最大標的地域; The Gentlemen が 2 位に転落; 医療・製造・ロジスティクスが上位被害セクター *(SecurityBrief / NCC Group)*

- **[2026-10-06]** [[続報] Singapore CSA が FortiMail CVE-2026-104286 (CVSS 9.8) の即時パッチ要請 Alert AL-2026-133 を発表 — CISA KEV 追加後も APAC 政府・金融機関への積極悪用が継続](https://www.csa.gov.sg/alerts-and-advisories/alerts/al-2026-133/) — 10/1 の CISA KEV 追加後も APAC 標的の悪用が止まらず Singapore CSA が独自警告; workaround: IBE サポート無効化または管理インタフェースのネットワーク制限 *(CSA Singapore)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 today-2 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-41510 | Coraza WAF v3 (`github.com/corazawaf/coraza/v3`) < 修正版 | CWE-693 / 高 | 攻撃者が multipart/URL-encoded ボディに大量パラメータを投入 → WAF が ARGS コレクション評価をスキップ → SQL Injection 等のペイロードがバックエンドへ素通り (WAF 完全バイパス) | [Coraza GHSA (2026-10-06)](https://github.com/corazawaf/coraza/security/advisories) (commit 不明) | **Go WAF ライブラリ全採用環境 / ModSecurity 互換 WAF (Nginx+ModSec 含む) への水平バリアント候補** |
| CVE-2026-41508 | Coraza WAF v3 < 修正版 | CWE-20 / 中 | multipart ボディが境界値で切り詰められる際に strict-error ルール (200001 等) の評価がスキップされ → OWASP CRS strict モードのポリシーが無効化 → フォールスルーで悪意ボディがアプリ層に到達 | [同 advisory (2026-10-06)](https://github.com/corazawaf/coraza/security/advisories) (commit 不明) | **OWASP CRS strict モード採用環境 / NGINX+Coraza 組み合わせに多用** |
| CVE-2026-41504 | Coraza WAF v3 < 修正版 | CWE-117 / 中 | CRLF シーケンスを含む入力値が監査ログ (JSON/native 形式) に無エスケープ書き込み → ログエントリを偽造/分割 → SIEM の相関分析で攻撃証跡を隠蔽可能 | [同 advisory (2026-10-06)](https://github.com/corazawaf/coraza/security/advisories) (commit 不明) | **WAF 監査ログ完全性 / nginx access_log・Apache httpd でも同種 CRLF 問題が過去報告 / 水平バリアント候補広範** |
| CVE-2026-105851 | Payload CMS `payload` npm < 修正版 | CWE-284 / Critical (9.x) | 認証コレクション (users 等) の REST API が `_read` フックを経由せずにフィールドレベル `access` 制御を評価 → 一般ユーザーが `roles`・`isAdmin` 等の制限フィールドを読み書き可能 → 権限昇格 → 管理者乗っ取り | [GHSA Payload CMS (2026-10-06)](https://github.com/payloadcms/payload/security/advisories) (commit 不明) | **Critical / headless CMS として Next.js・Nuxt 製アプリに広く利用 / フィールドレベル ACL 実装全般への水平バリアント候補** |
| CVE-2026-104850 | MCP TypeScript SDK `@modelcontextprotocol/sdk` < 修正版 | CWE-601 / 高 | MCP サーバーが攻撃者管理の OAuth 認可サーバーエンドポイントを指定 → クライアント SDK が SSRF/オープンリダイレクト保護なしに Bearer トークンを送信 → トークン収奪 → MCP 接続 AI エージェントへのなりすましアクセス | [GHSA-r8mh-x5qv-7gg2 (2026-10-06)](https://github.com/advisories/GHSA-r8mh-x5qv-7gg2) (commit 不明) | **AI エージェント統合に MCP を使う全スタック / Claude・OpenAI 互換ツールが攻撃対象範囲** |
| CVE-2026-86540 | `knowns` npm パッケージ < 修正版 | CWE-78 / 高 | `.knowns/config.json` の LSP バイナリパス設定に shell metacharacter を含む値をセット → LSP サーバー起動時に OS コマンドが実行 → 任意コード実行 (LSP サーバー権限で) | [GHSA Oct 6](https://github.com/advisories) (commit 不明) | **VS Code 等エディタ拡張として利用 / LSP バイナリパスへの OS コマンドインジェクション — 他 LSP 拡張への水平バリアント候補** |
| CVE-2026-96940 | Microsoft Exchange Server (on-premises) 全サポートバージョン < OOB パッチ適用 | CWE-269 / 8.8 | 認証済み組織内ユーザーが細工した MAPI over HTTP リクエストを送信 → バックエンドの内部委任チェックが欠如 → 同テナント内の任意ユーザーのメールボックスへの読み取り/送信権限昇格 | [MSRC CVE-2026-96940 OOB (2026-10-06)](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-96940) (commit 不明) | **CVSS 8.8 / Exchange on-prem 全採用組織 / M365 Hybrid・メール監査ソリューションへの波及リスク** |

---

## 国内脆弱性・インシデント情報

> 直近2日間に該当する新規ニュースは確認できませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 採用ウィンドウ: 2026-10-06 〜 2026-10-08 (JST)
- 巡回ソース数: 30+
- 採用件数: AI=5 / Security=5 / CVE=7 / 国内=0
- 除外理由内訳:
  - 採用窓外 (公開日 < 2026-10-06):
    - FTC が OpenAI/Anthropic/METR を調査開始 (Oct 1-2) — 窓外
    - Armadin $255.5M Series B Kevin Mandia (Oct 1) — 窓外
    - Reflection AI Beam 501B MoE (Oct 5) — 窓外
    - Denmark CPR データ漏洩 8.8M 人 (Oct 5) — 窓外
    - Frontline Education 学区データ侵害 (Oct 5) — 窓外
    - Bipartisan AI Agent Accountability Act / Senator Hawley・Murphy (Oct 1) — 窓外
    - ASUSTOR CVE-2026-24936 等 (Jul 2026) — 窓外
  - 重複 (直近7日 digest 既報):
    - CVE-2026-21589 Atlassian — Oct 7 digest 既報 (本日は 続報 として採用)
    - CVE-2026-104286 FortiMail — Oct 3 digest 既報 (Singapore CSA 続報は Security 欄採用)
    - vLLM CVE-2026-105752/105753 — Oct 7 digest 既報
    - PyMongo CVE-2026-96749/96748 — Oct 7 digest 既報
    - Pwn2Own Day 1 (OpenAI Codex / Oracle AI DB) — Oct 7 digest 既報 (Day 2 は新規採用)
    - 韓国金融機関 Artex AI 攻撃 — Oct 7 digest 既報
    - ATB Ukraine DataSuckers — Oct 7 digest 既報
    - Citrix CVE-2026-88779 / Rejetto CVE-2026-61500 / macOS CVE-2026-43682 — Oct 6 digest 既報
    - Trump SIF 大統領令 / Bloomberg US-China AI / OpenAI Robinson 辞任 — Oct 6 digest 既報
  - 日付不明・確認不可:
    - ASOS "ASOS HACKED" app pop-up (Oct 7) — 一次記事本文取得不可; Aug 2026 credential stuffing 別事案との混在の可能性があり除外
    - Sierra/Meta Personal Agent Protocol (Oct 6) — 一次情報源確認不可で除外
    - Coraza/Payload CMS/MCP SDK 修正コミット URL — GHSA ページ直接アクセス不可 (commit 不明 と明記)
    - Smarty v4.5.8 RCE — CVE 番号・公開日の信頼性が低く除外
    - Microsoft Patch Tuesday Oct 2026 全体 — 10/13 (第二火曜) 予定であり今回窓内未公開
  - 取得失敗ソース (EGRESS_BLOCKED / DNS 不解決): helpnetsecurity.com, bleepingcomputer.com, zerodayinitiative.com, cnbc.com, decrypt.co, securityweek.com, thehackernews.com, nvd.nist.gov, jvn.jp, jpcert.or.jp, github.com/corazawaf (advisories 直接)

</details>
