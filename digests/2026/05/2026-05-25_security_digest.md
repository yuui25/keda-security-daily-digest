# KEDA Daily Digest — 2026-05-25 (JST)

> 採用範囲: 公開日 2026-05-23 〜 2026-05-25
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Anthropic が Project Glasswing の初期成果として Claude Mythos Preview による 10,000 件超の高・重大度脆弱性発見を公表し、AI 主導の防御的バグハンティングが量的転換点を迎えた。一方でオランダ当局が Stark Industries 系ブルートフォースホスティングを摘発し、ロシア系サイバー攻撃インフラへの打撃を与えた。LiteSpeed cPanel Plugin の CVSS 10.0 の欠陥（CVE-2026-48172）が CISA KEV に追加されており、cPanel 環境を持つ組織は即時パッチ適用が求められる。

---

## AI 関連ニュース

- **[2026-05-23]** [Anthropic、Project Glasswing 初期アップデート：Claude Mythos Preview が 10,000件超の高・重大度脆弱性を発見](https://cybersecuritynews.com/anthropics-claude-mythos-preview-0-days/) — 約 50 パートナーを通じ最重要 OSS をスキャン；1,726件が有効な真陽性と確認。Cloudflare は 2,000件（400件高/重大）、Mozilla は Firefox 150 で 271件を修正済み *(CybersecurityNews)*

- **[2026-05-23]** [ChatGPT 生成画像に Google SynthID ウォーターマーク＆C2PA メタデータが標準搭載](https://www.techtimes.com/articles/317060/20260523/chatgpt-images-carry-invisible-ai-markers-anyone-can-detect-what-users-who-cant-disclose-gen-ai.htm) — OpenAI が C2PA 適合を宣言し、全 AI 生成画像に SynthID 透かしを組み込む；画像の生成元を誰でも確認できる公開検証ツールもプレビュー提供開始 *(TechTimes)*

- **[2026-05-23 ～]** [[続報] TanStack npm サプライチェーン攻撃：OpenAI が公式対応を発表](https://openai.com/index/our-response-to-the-tanstack-npm-supply-chain-attack/) — 従業員デバイス 2台への侵害を確認（ユーザーデータへの影響なし）、macOS 向け全アプリの署名証明書をローテーション。6月12日以降、旧バージョンのアプリは非機能化 *(OpenAI)*

- **[2026-05-23 ～]** [[続報] GitHub が TeamPCP による内部リポジトリ侵害を正式認定：顧客データへの影響なしと確認](https://therecord.media/github-confirms-teampcp-hack-customers-unaffected) — 調査の結果、顧客リポジトリ・エンタープライズアカウント・ユーザーデータへのアクセスなしと結論。内部リポジトリ 3,800件分のデータが犯罪フォーラムで 5万ドルにて出品中 *(The Record)*

- **[2026-05-23]** [Anthropic、Claude Mythos Preview が UK AISI「The Last Ones」32段階攻撃チェーンを 73% の成功率でクリアと発表](https://www.techtimes.com/articles/317076/20260524/anthropic-moves-closer-public-claude-mythos-release-10000-critical-bugs-found-first.htm) — 3/10 の試行でチェーン全段を完遂；一般公開は更なる安全対策完了を条件とすると明言 *(TechTimes)*

- **[2026-05-23]** [Ghost CMS SQLインジェクション CVE-2026-26980 を悪用した大規模 ClickFix キャンペーン：Harvard・Oxford 含む 700件超のサイトが侵害](https://blog.xlab.qianxin.com/ghost-cms-mass-compromised-via-cve-2026-26980-now-fueling-clickfix-attacks/) — Admin API Key 奪取 → JS 注入 → FakeCaptcha (偽 Cloudflare 認証) の 5段階攻撃チェーン；被害は高度自動化で拡大中 *(XLab/360)*

---

## セキュリティ関連ニュース

- **[2026-05-23]** [オランダ FIOD、Stark Industries / THE.Hosting 運営のブルートフォースホスティング摘発：800台サーバー押収・2名逮捕](https://www.bleepingcomputer.com/news/security/netherlands-seizes-800-servers-of-hosting-firm-enabling-cyberattacks/) — 5月22日の急襲でロシア・ベラルーシ関係者向けにサイバー攻撃・偽情報キャンペーンのインフラを提供していた WorkTitans B.V.（THE.Hosting ブランド）を摘発 *(BleepingComputer)*

- **[2026-05-23]** [LiteSpeed cPanel Plugin CVE-2026-48172（CVSS 10.0）が CISA KEV に追加：任意スクリプトの root 実行が野外で確認](https://thehackernews.com/2026/05/litespeed-cpanel-plugin-cve-2026-48172.html) — lsws.redisAble JSON-API エンドポイントの権限検証欠落。影響バージョン 2.3〜2.4.4；cPanel Plugin v2.4.7 / WHM v5.3.1.0 へのアップデートで修正 *(The Hacker News)*

- **[2026-05-23]** [[続報] Laravel-Lang PHP パッケージへのサプライチェーン攻撃が継続：5月22〜23日に新規悪意タグが rapid succession で公開](https://strobes.co/blog/tanstack-npm-supply-chain-attack/) — 700件超のバージョンに影響。資格情報窃取フレームワークを配信するマルウェアが Composer 経由で配布中；Composer の `minimum-stability` 設定の確認を推奨 *(Strobes)*

- **[2026-05-23]** [Parse Server CVE-2026-47138：未認証 DoS（CWE-1333 正規表現バックトラッキング）を修正](https://advisories.gitlab.com/npm/parse-server/CVE-2026-47138/) — `X-Parse-Client-Version` ヘッダを細工するだけで Node.js ワーカーの CPU を指数的に消費できる。パッチ: 8.6.77 / 9.9.1-alpha.1 *(GitLab Security Advisories)*

- **[2026-05-23]** [TeamPCP が GitHub 内部リポジトリを侵害：Nx Console VSCode 拡張を通じた Pwn-Request ＋ OIDC トークン抽出で 3,800件のリポジトリを窃取](https://www.bleepingcomputer.com/news/security/github-investigates-internal-repositories-breach-claimed-by-teampcp/) — 悪意ある拡張(v18.95.0)が CA 毎のキャッシュ汚染経由で GitHub Actions runner のメモリから OIDC トークンを取得 *(BleepingComputer)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-05-23 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-48172 | LiteSpeed cPanel Plugin 2.3〜2.4.4 | CWE-269 / 10.0 | 全ログイン済み cPanel ユーザーが `lsws.redisAble` JSON-API を呼び出すと権限検証なしに任意スクリプトが root として実行される | [advisory](https://techjacksolutions.com/scc-intel/litespeed-cpanel-plugin-privilege-escalation-vulnerability-cve-2026-48172-actively-exploited/) (commit 不明) | KEV / EPSS高 |
| CVE-2026-47138 | Parse Server < 8.6.77, 9.x < 9.9.1-alpha.1 | CWE-1333 / 7.5 | 認証不要で `X-Parse-Client-Version` ヘッダに細工した SDK バージョン文字列を送ると regex backtracking で CPU 消費が指数増大し Node.js ワーカーを DoS | [advisory](https://advisories.gitlab.com/npm/parse-server/CVE-2026-47138/) (commit 不明) | — |

---

## 国内脆弱性・インシデント情報

> 直近2日間に該当する新規ニュースは確認できませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 20+（WebSearch 16回、WebFetch 20+回試行）
- 採用件数: AI=5 / Security=5 / CVE=2 / 国内=0
- 除外理由内訳: 古すぎ(window外)=多数（Ghostwriter May22, NSA MCP May20, White House AI EO May21, LiteLLM March, n8n Dec 2025 等） / 重複(excluded_set)=多数（CVE-2026-9082 Drupal, CVE-2026-45185 Exim, CVE-2026-46715 Flask-Security 等） / 日付不明=若干
- 取得失敗ソース: thehackernews.com (403), bleepingcomputer.com (403), nvd.nist.gov (403), anthropic.com (403), cybersecuritynews.com (403), jvn.jp (403), jpcert.or.jp (403) — WebSearch で代替取得

</details>
