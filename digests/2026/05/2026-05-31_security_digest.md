# KEDA Daily Digest — 2026-05-31 (JST)

> 採用範囲: 公開日 2026-05-29 〜 2026-05-31
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

LLM エージェントによる自律後続侵害 (Sysdig が史上初記録)・GREYVIBE の AI 活用スパイ活動・Kimsuky の LLM 開発バックドアと、AI が攻撃インフラそのものに統合される段階に突入した。Palo Alto PAN-OS GlobalProtect の認証バイパス CVE-2026-0257 が CISA KEV 追加（5/17 から野外悪用中）、Craft CMS Formie プラグインの未認証 Twig SSTI (CVSS 9.8) は即時修正が必要。加えて ChatGPT ウェブサマリ機能を悪用したフィッシング基盤「ChatGPhish」とブラジル銀行 SDK 偽装 NuGet サプライチェーン攻撃が同日公開された。

---

## AI 関連ニュース

- **[2026-05-29]** [ChatGPhish: ChatGPT のウェブサマリ機能が攻撃者制御コンテンツを信頼し IP 漏洩・フィッシング URL 挿入を許す脆弱性を Permiso Security が開示](https://www.theregister.com/research/2026/05/29/chatgpt-prompt-injection-turns-web-pages-into-phishing-lures/5248137) — chatgpt.com がサマリ対象ページ由来の Markdown 画像を自動フェッチ・リンクをクリック可能として表示→任意のウェブページに小さなペイロードを追記するだけでフィッシング URL・偽セキュリティ警告を ChatGPT 応答内に注入可能；研究者 Ahmeti が 4/29 Bugcrowd 経由で OpenAI に開示済み、修正確認未 *(The Register / The Hacker News)*

- **[2026-05-29]** [GREYVIBE: 新規ロシア系未文書化 APT が ChatGPT・Ideogram AI・Google Gemini を活用して対ウクライナ AI 強化サイバー作戦を展開 — WithSecure が初公開](https://www.bleepingcomputer.com/news/security/greyvibe-hackers-use-chatgpt-gemini-to-power-cyberattacks/) — 2025 年 8 月以降継続、軍・政府・民間・企業が標的；AI でリアルな誘引コンテンツを大量生成しスピアフィッシング・偽 CAPTCHA・偽ウクライナ関連サイトを通じてマルウェアを配布。OpSec の低さを AI の速度・精度で補完する「低〜中高度 APT + AI」モデルを確立 *(BleepingComputer / The Hacker News)*

- **[2026-05-29]** [Marimo CVE-2026-39987 を起点に LLM エージェントが後続侵害を完全自律実行 — 史上初の「AI エージェント駆動型侵入」を Sysdig TRT が記録](https://thehackernews.com/2026/05/attackers-use-llm-agent-for-post.html) — 公開 Marimo インスタンスの WebSocket 認証バイパスで初期 RCE 取得後、LLM エージェントが AWS クレデンシャル抽出→Secrets Manager SSH 秘密鍵→PostgreSQL DB 全窃取を 1 時間で自律遂行；DB 流出は 2 分未満 *(Sysdig TRT / The Hacker News)*

- **[2026-05-29]** [北朝鮮 Kimsuky が LLM 開発疑いの Rust バックドア HelloDoor と HTTPSpy 変種を展開 — 韓国軍・企業向けセキュリティソフト偽インストーラで 3〜4 月に多数侵害](https://thehackernews.com/2026/05/kimsuky-deploys-httpspy-expands-arsenal.html) — HelloDoor は PebbleDash ベースの Rust 製 RAT で「LLM を利用した可能性が高い」と ENKI・Kaspersky が分析；VS Code トンネリング・Cloudflare Quick Tunnels で C2 隠蔽、DWAgent RMM ツールで後続操作 *(The Hacker News / ENKI / Kaspersky)*

- **[2026-05-29]** [OpenAI が「第三者評価の共通プレイブック」を公開 — フロンティアモデルの能力・安全策を独立評価するための設計原則・アクセス方式・報告体制を提言](https://openai.com/index/trustworthy-third-party-evaluations-foundations/) — 有効な評価設計・モデルアクセス取り決め・結果報告の推奨事項を整理；EU AI Act Code of Practice および Preparedness Framework との整合を明示。Frontier Governance Framework (5/29 公開・05-30 採用) の補完ドキュメントとして位置づけ *(OpenAI)*

- **[2026-05-29]** [Microsoft が内部 Claude Code ライセンスを大規模キャンセルし GitHub Copilot CLI へ移行 — トークン課金が年間予算を数ヶ月で超過、Uber も 4 か月で AI 予算を使い切り ROI 検証局面に](https://www.windowscentral.com/microsoft/microsoft-cancels-claude-code-licenses-shifting-developers-to-github-copilot-cli-a-move-likely-driven-by-financial-motives) — Experiences & Devices 部門が 6/30 期限でキャンセル開始；コード commit の 25% が Claude Code 由来にも関わらず「消費者向けイノベーションへの貢献が見えない」と Uber COO が Fortune に発言、エンタープライズ AI の費用対効果再評価が進む *(Windows Central / The Next Web / Fortune)*

---

## セキュリティ関連ニュース

- **[2026-05-29]** [CVE-2026-0257 Palo Alto PAN-OS GlobalProtect 認証バイパス — CISA が 5/29 KEV 追加、5/17 から野外悪用中、連邦機関の修正期限は 6/19](https://windowsnews.ai/article/cisa-flags-palo-alto-globalprotect-auth-bypass-cve-2026-0257-as-actively-exploited-patch-by-june-19.420836) — 認証オーバーライド Cookie を別機能と証明書共有する構成でのみ成立；攻撃者が Cookie を偽造し未認証で GlobalProtect VPN 接続を確立→内部ネットワーク露出。Rapid7 が同一 TA による 5/17・5/21 の 2 波を観測、C2 は Dromatics Systems ホスティング *(CISA / Windows News / Rapid7)*

- **[2026-05-29]** [Sicoob.Sdk 偽 NuGet パッケージ: ブラジル最大規模の協同金融ネットワーク向け .NET SDK を偽装し PFX 証明書・クライアント ID・パスワードをハードコード Sentry エンドポイントへ流出](https://thehackernews.com/2026/05/malicious-sicoob-nuget-steals-banking.html) — SicoobClient をインスタンス化するだけで即時流出；Pix 即時決済・動的 QR 生成に使う PFX 証明書が標的、約 500 件ダウンロード。Google AI 検索が一時公式 SDK として推奨し露出が拡大→Socket が報告して NuGet から削除 *(Socket / The Hacker News)*

- **[2026-05-29]** [新規 APT GREYVIBE がウクライナおよびウクライナ関連組織への AI 支援攻撃を 2025 年 8 月以降継続中 — スピアフィッシング・偽 CAPTCHA・偽ウクライナ関連サイトを多用](https://thehackernews.com/2026/05/new-russian-linked-greyvibe-targets.html) — WithSecure が初公開；ロシア語話者でモスクワ時間帯での活動が一致、国家後援とサイバー犯罪の中間に位置する可能性あり *(The Hacker News / BleepingComputer)*

- **[2026-05-29]** [Kimsuky HTTPSpy/HelloDoor 多段キャンペーン: 韓国軍・企業を 3〜4 月に侵害、GPKI 証明書抽出型 HappyDoor・VS Code C2 等の新手口を確認](https://thehackernews.com/2026/05/kimsuky-deploys-httpspy-expands-arsenal.html) — 正規 DWAgent RMM・VS Code トンネリング・Cloudflare Quick Tunnels を組み合わせ EDR 検出を回避；国防・政府・医療セクターが標的、GPKI 証明書窃取に特化した HappyDoor 亜種を初確認 *(The Hacker News / ENKI / Kaspersky)*

- **[2026-05-29]** [Marimo ノートブック侵害から LLM エージェントが後続侵害を自律実行 — AWS Secrets Manager→SSH 鍵→内部 PostgreSQL DB 全窃取を 1 時間以内に完了](https://thehackernews.com/2026/05/attackers-use-llm-agent-for-post.html) — CVE-2026-39987 (Marimo /terminal/ws 認証バイパス, CVSSv4 9.3) が起点；Sysdig が「史上初の LLM エージェント型侵入」として完全攻撃チェーンを記録。公開 AI ノートブックインスタンスは即時隔離・認証設定が必要 *(Sysdig TRT / The Hacker News)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-05-29 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-45697 / [GHSA-x7m9-mwc2-g6w2](https://github.com/advisories/GHSA-x7m9-mwc2-g6w2) | Formie プラグイン (Craft CMS) < 2.2.20 / < 3.1.24 | CWE-94 / **9.8** | 未認証ユーザーが Hidden フィールドの「Custom Default value」に Twig テンプレート式を挿入→フォーム送信時にサーバー側で任意コード実行→完全サイト乗っ取り・DB 認証情報漏洩 | [commit f690d562](https://github.com/verbb/formie/commit/f690d5623163ce2a95da305238d6367575486ee3) | CVSS 9.8 / 未認証 / PHP CMS テンプレートエンジン SSTI の典型パターン (Twig・Smarty・Blade 等への水平伝播候補) |
| CVE-2026-0257 / [GHSA-jqxw-84hx-6qj5](https://github.com/advisories/GHSA-jqxw-84hx-6qj5) | Palo Alto PAN-OS (GlobalProtect portal/gateway 有効・認証 Cookie 有効・証明書共有構成) | CWE-287 / **7.8** | 認証オーバーライド Cookie を別機能と証明書共有する構成で Cookie を偽造→未認証で GlobalProtect VPN 接続確立→内部ネットワーク侵入 | (commit 非公開) [PA ホットフィックス](https://security.paloaltonetworks.com/CVE-2026-0257) | **KEV ✓** (2026-05-29 追加) / 5/17 から野外悪用・連邦期限 6/19 / SSL-VPN 認証 Cookie 迂回として同種製品 (Fortinet・Check Point 等) への水平伝播を要確認 |
| CVE-2026-39987 / [GHSA-2679-6mx9-h9xc](https://github.com/marimo-team/marimo/security/advisories/GHSA-2679-6mx9-h9xc) | Marimo ≤ 0.20.4 (AI ノートブックサーバー) | CWE-306 / CVSSv4 **9.3** | `/terminal/ws` WebSocket が `validate_auth()` をスキップし認証なしで接続を受け入れる→未認証で完全 PTY シェル取得→公開インスタンスで 1 リクエスト完全 RCE | [commit c24d4806 (v0.23.0)](https://github.com/marimo-team/marimo/commit/c24d4806398f30be6b12acd6c60d1d7c68cfd12a) | CVSSv4 9.3 / CISA KEV ✓ / **2026-05-29 に LLM エージェント型 post-exploitation が初確認** ※CVE 公開 2026-04-08 / 公開 AI 開発ツールの WebSocket 認証欠落パターンとして他製品への水平確認を推奨 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-05-29 | CVE-2026-6891 | Canon My Image Garden for macOS v3.6.8 以前および CUPS Printer Driver のインストーラにシンボリックリンク競合：インストール中にローカル攻撃者がシンボリックリンクを細工してファイルアクセス権を不正変更可能 | CVSS 5.0 (Medium) | [JVNDB-2026-015132](https://jvndb.jvn.jp/en/contents/2026/JVNDB-2026-015132.html) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 25+ (WebSearch 35+ クエリ, WebFetch 10+ 試行)
- 採用件数: AI=6 / Security=5 / CVE=3 / 国内=1
- 除外理由内訳:
  - 採用窓外 (< 2026-05-29): Proofpoint 2026 AI and Human Risk Landscape Report (4/28) / OpenAI ChatGPT 個人金融機能 (5/15) / Microsoft MDASH agentic scanning harness (5/12) / NSA MCP セキュリティガイダンス (5/20) / White House AI EO 延期 (5/20-21) / Uber Claude Code 予算枯渇 Fortune 初報 (5/26) / Sicoob.Sdk 悪意パッケージ公開 (5/5-6) / cPanel CVE-2026-41940 watchTowr (4月) / CVE-2026-39987 Marimo 公開 (4/8) ← CVE テーブルに「LLM 悪用 5/29 初記録」として採用
  - 重複 (excluded_set 直近7日): OpenAI Frontier Governance Framework (05-29 公開→05-30 採用) / Anthropic $965B 評価額 (05-30 採用) / Chrome 148.0.7778.217 151件パッチ (05-30 採用) / Gogs zero-day KEV (05-30 採用) / Charter/Carnival ShinyHunters (05-30 採用) / CVE-2026-35616 FortiClient (05-29 採用) / CVE-2026-8398 DAEMON Tools KEV (05-29 採用) / Claude Opus 4.8 (05-29 採用) / Google AI Threat Defense (05-29 採用) / Oracle CSPU (05-29 採用) / Yamcs CVEs 3件 (05-29 採用) / Glassworm takedown (05-28 採用)
  - 日付不明/確認不可: Microsoft Claude Code 初報は 5/14 (The Verge) だが Windows Central 等で 5/29 に大規模新報道として独立した採用判断
  - CVE 件数が目安 (5〜10件) を下回った理由: 採用窓 2026-05-29〜31 はパッチ集中なし (Patch Tuesday 5/12 から時間が経過)。全セクションに採用件あり、fallback (直近7日拡大) の適用条件 (全セクション 0件) は不成立のため通常通り
- 取得失敗ソース: security.paloaltonetworks.com (403) / thehackernews.com 直接フェッチ (403) / bleepingcomputer.com (403) / theregister.com (403) / windowscentral.com (403) / rapid7.com (403) / sysdig.com (403) / aiweekly.co (403) / aitoolsrecap.com (403) / buildfastwithai.com (403) — WebSearch スニペット・複数独立記事で内容・日付を補完

</details>
