# KEDA Daily Digest — 2026-07-28 (JST)

> 採用範囲: 公開日 2026-07-26 〜 2026-07-28 (JST)
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Claude 共有チャットが Google/Bing に 600 件超インデックスされ API キー・暗号ウォレット・SSN 等が露出した事案が AI プライバシー問題として浮上。Nvidia・Microsoft ら約 30 社が「Open Secure AI Alliance」を設立し、オープンソース防衛 AI ツールの開発を宣言した。脆弱性面では vBulletin CVE-2026-61511 (pre-auth PHP eval RCE) と Windows WalletService CVE-2026-49176 (標準ユーザー→SYSTEM 昇格) それぞれのPoC が 7/27 に公開され、n8n サンドボックス脱出 GHSA-gv7g-jm28-cr3m の THN 報道も集中。インシデントでは Coca-Cola が Fairlife ランサムウェア被害によるデータ窃取を公式確認し、ShinyHunters が EY 侵害の犯行を DLS で表明した。

---

## AI 関連ニュース

- **[2026-07-26]** [Claude の共有チャット 600 件超が Google/Bing に検索インデックス — API キー・SSN・暗号ウォレット情報を含む会話が第三者に閲覧可能な状態に](https://venturebeat.com/technology/uh-oh-some-claude-shared-conversations-and-artifacts-appear-to-be-indexed-and-publicly-accessible-on-google-search) — Reddit 投稿を機に発覚; claude.ai/share ページに noindex 制御が欠如し Google・Bing が会話全文をクロール・インデックス、法律戦略・プロプライエタリコード・個人情報・SSN・仮想通貨ウォレットを含む会話が公開状態に。Anthropic は「検索エンジンにサイトマップを提供していない」と声明、週末中に該当ページは検索結果から消滅 *(VentureBeat / Cybernews / GBHackers)*

- **[2026-07-27]** [Open Secure AI Alliance 設立 — Nvidia・Microsoft・IBM・Cisco・Cloudflare・Hugging Face・Salesforce・Palantir ら約 30 社・OSS 財団が参加、防衛 AI のオープンソース化を推進](https://www.helpnetsecurity.com/2026/07/27/nvidia-open-secure-ai-alliance/) — OpenAI/HuggingFace AI 境界侵害を契機に結成; 参加組織は自組織インフラで検査・改変・実行可能なフロンティア AI モデルが防衛側に必要と主張。Linux Foundation Akrites・OpenSSF の既存成果を基盤に AI セキュリティツールを共同開発・公開。OpenAI・Anthropic・Google は参加せず *(Help Net Security / SiliconAngle / The Hill / UPI)*

- **[2026-07-27]** [Google GTIG が Mandiant + TAG を統合した脅威アクター新命名体系を公開 — 2 単語クリプトニム方式で 第 2 語が国家・動機カテゴリを示す](https://cloud.google.com/blog/topics/threat-intelligence/updated-cyber-threat-actor-naming-system) — CASTLE=中国・ION=イラン・NEPTUNE=北朝鮮・RELIC=ロシア・COMET=サイバー犯罪グループ; 既存名称は継承 (例: Sandworm → SANDWORM RELIC)。Mandiant と TAG が独立して運用してきた二重命名体系を統一し、防御側の混乱を解消 *(Google Cloud Blog / Help Net Security / GBHackers)*

- **[2026-07-27]** [Bloomberg: 2026 年の CVE 発見数は 2025 年のほぼ 2 倍ペース — NVD が 1/1〜7/27 に 45,207 件を登録、AI 自律バグハントが急増を牽引](https://www.bloomberg.com/news/articles/2026-07-27/ai-hunts-for-cyber-flaws-finding-record-numbers-in-tech-sector) — 2025 年通年の NVD 登録件数に迫るペースで前半だけで到達; Kimi K3 による Redis 19 件 (07-26 掲載) や XBOW の Bing RCE 自律発見 (07-26 掲載) 等、AI エージェントが OSS 深部に到達している事例が世界的に加速 *(Bloomberg)*

- **[2026-07-27]** [Claude Code CLAUDE.md @import シンボリックリンク経由ファイル流出 — Tego AI が「第 2 の Claude 欠陥」として開示、Anthropic は HackerOne で "Informative" 扱い](https://gbhackers.com/claude-code-symlink-flaw-exfiltrates-sensitive-files/) — @import がリポジトリ内シンボリックリンクを参照する場合、Claude Code はリテラルパス (./link) を内部パスと判定して安全とみなすが OS がシンボリックリンク先を解決して読込み → `~/.aws/credentials` 等プロジェクト外ファイルが承認プロンプトなしに最初のモデルリクエストに混入。CVE-2025-59829・CVE-2026-25724 で修正されたパーミッションサブシステムと同根の欠陥がメモリローダーコードパスには未適用 *(GBHackers / CyberPress / Tego AI / GlobeNewswire 2026-07-24)*

- **[2026-07-27]** [AWS DevOps Agent が Network Firewall のルート原因解析を自動化 — VPC フローログ・CloudTrail・ファイアウォールポリシーを横断調査し修正案を提示](https://aws.amazon.com/blogs/security/accelerating-aws-network-firewall-troubleshooting-with-aws-devops-agent/) — AWS が同エージェントの Network Firewall 適用ガイドを公開; ルート原因特定・緩和計画の提示・CI/CD パイプラインへのガードレール推奨生成までを自動実行。SRE の繰り返し調査作業を AI が肩代わりするユースケースとして注目 *(AWS Security Blog / Help Net Security)*

---

## セキュリティ関連ニュース

- **[2026-07-27]** [GitHub・PyPI がサプライチェーン攻撃対策の時間ベース防御機構を導入 — Dependabot に 3 日間クールダウン、PyPI は 14 日超の古いリリースへのアップロードを拒否](https://www.bleepingcomputer.com/news/security/github-pypi-add-time-absed-defenses-against-supply-chain-attacks/) — クールダウン期間中にセキュリティツールが悪意ある依存関係を検出できる時間を確保; chalk・debug 攻撃・Shai-Hulud キャンペーン等への対応として実装。Dependabot の cooldown オプションで期間変更可能、lockfile ピン留め・スコープ制限トークンとの併用を推奨 *(BleepingComputer / DevOps.com)*

- **[2026-07-27]** [続報] [Coca-Cola が Fairlife ランサムウェア被害でのデータ窃取を公式確認 — 米 4 施設の生産の大半は再開](https://www.bleepingcomputer.com/news/security/coca-cola-confirms-data-theft-in-fairlife-ransomware-attack/) — 7/27 に Coca-Cola が声明「certain data の取得があった」と初めて公式確認; Anubis グループは 1TB 窃取・7/20 に DLS 掲載済み。生産は大半再開も侵害範囲の詳細は非公開 (初報 2026-07-24掲載) *(BleepingComputer / SecurityWeek)*

- **[2026-07-27]** [続報] [ShinyHunters が Ernst & Young (EY) 侵害を犯行声明 — IT サポート第三者プラットフォームのサプライチェーン攻撃、7/31 までにデータ公開を予告](https://www.bleepingcomputer.com/news/security/ernst-and-young-data-breach-claimed-by-shinyhunters-extortion-gang/) — 3/28〜4/12 に税務サポート管理プラットフォームを経由して顧客税務情報・PII を窃取。ShinyHunters が 7/27 に DLS へ追加し July 31 期限で恐喝開始。Experian を通じ影響顧客に 24 ヵ月間の ID 監視を提供 (EY 侵害本体 2026-07-18 掲載) *(BleepingComputer)*

- **[2026-07-27]** [Android AfterCall 広告詐欺 — DoubleVerify が通話終了後に広告を表示するマルウェアアプリ群を発見、億単位のインプレッション詐欺を確認](https://cybernews.com/security/android-after-call-ad-fraud/) — 偽のアラーム・カレンダーアプリが「上に表示」権限を要求 → `ACTION_PHONE_STATE_CHANGED` イベントを監視し通話終了直後に全画面広告を表示; 「最近のアプリ」リストから自身を削除して検出・アンインストールを困難化。Google Play に侵入済み *(Cybernews / DoubleVerify Engineering)*

- **[2026-07-27]** [vBulletin CVE-2026-61511 の完全 PoC を SSD Secure Disclosure が公開 — 未認証で PHP eval() に到達しフォーラムサーバーを掌握](https://securityonline.info/critical-pre-auth-rce-vbulletin-flaw-allows-full-server-compromise-poc-available/) — /includes/vb5/template/runtime.php の `{vb:math}` テンプレートタグ処理で入力が eval() に無サニタイズで渡されることが判明; 7/1 に vBulletin 6.2.2 でサイレントパッチ済みだが 7/27 時点で野生悪用は未確認 *(THN / SecurityOnline)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-07-26 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| GHSA-gv7g-jm28-cr3m | n8n <2.31.5 および >=2.32.0,<2.32.1 (ワークフロー自動化) | CWE-94 / **8.7** (CVSS 4.0) | 認証済みワークフロー編集者が arrow-function 構文を含む式を細工 → 式コンパイラの AST リライターが `process` ノードを変換せず通過 → n8n プロセス権限で OS コマンド実行 | [GHSA-gv7g-jm28-cr3m](https://github.com/n8n-io/n8n/security/advisories/GHSA-gv7g-jm28-cr3m) / fix: n8n 2.31.5 & 2.32.1 (2026-07-22) | 2026-07-27 THN 報道 / 直近 7 ダイジェスト未掲載 / n8n は AI ワークフロー自動化に広範利用 / 類似 AST サンドボックス回避パターンの水平伝播候補 |
| CVE-2026-61511 | vBulletin ≤6.2.1 / ≤6.1.6 (フォーラムソフトウェア) | CWE-94 / 未評価 (EPSS 未掲載) | 未認証攻撃者が `{vb:math}` テンプレートタグを含む HTTP リクエストを送信 → `runMaths()` が数式文字列を PHP `eval()` に無サニタイズで渡す → サーバー上で任意 PHP コード実行; 管理者・認証不要 | [vBulletin 6.2.2 リリースノート](https://www.vbulletin.com/forum/forum/vbulletin-announcements/vbulletin-announcements_aa/4498023) (commit 不明 / 2026-07-01 サイレントパッチ) | **2026-07-27 完全 PoC 公開 (SSD Secure Disclosure)** / 未認証 / インターネット公開フォーラム多数 / PHP eval injection 水平伝播候補 |
| CVE-2026-49176 | Windows WalletService (Win10/11/Server 2016/2019/2022/2025、7/14 パッチ未適用) | CWE-732 / **7.8** (CVSS 3.1) | ローカル標準ユーザーが WalletService の ESE データベース初期化パスを悪意ある DB ファイルへリダイレクト → ESE コールバックが攻撃者制御の DLL をロード → `NT AUTHORITY\SYSTEM` で任意コード実行 | [Microsoft MSRC CVE-2026-49176](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-49176) (commit 不明) / fix: 2026-07-14 Patch Tuesday | **2026-07-27 完全 PoC 公開 (David Carliez)** / 全サポート Windows バージョンに影響 / SYSTEM 昇格 / 野生悪用未確認 / ESE コールバック DLL ハイジャックパターン |

---

## 国内脆弱性・インシデント情報

> 直近 2 日間 (2026-07-26〜27) に JVN/JPCERT/CC/IPA/Piyolog で確認できた新規の国内脆弱性・インシデント公表はありませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| VentureBeat / Cybernews / GBHackers (Claude 共有チャット Google インデックス) | Daniel J Glover Blog URL "/2026-07-26-shared-claude-conversations-google/" 確認 ✓ / Cybernews 2026-07-26 確認 ✓ |
| Help Net Security / SiliconAngle / The Hill / UPI (Open Secure AI Alliance) | Help Net Security URL "/2026/07/27/nvidia-open-secure-ai-alliance/" 確認 ✓ |
| Google Cloud Blog / Help Net Security / GBHackers (GTIG 命名体系刷新) | Help Net Security URL "/2026/07/27/google-threat-actors-naming-system/" 確認 ✓ |
| Bloomberg (AI CVE 発見数 2 倍ペース) | Bloomberg URL "/2026-07-27/ai-hunts-for-cyber-flaws-finding-record-numbers-in-tech-sector" 確認 ✓ |
| GBHackers / CyberPress (Claude Code symlink / Tego AI) | GlobeNewswire "news-release/2026/07/24/" 初報確認 ✓ / GBHackers 2026-07-27 報道確認 ✓ |
| AWS Security Blog / Help Net Security (AWS DevOps Agent Network Firewall) | Help Net Security URL "/2026/07/27/aws-devops-agent-network-firewall-troubleshooting/" 確認 ✓ |
| BleepingComputer / DevOps.com (GitHub PyPI Dependabot) | PRSOL.CC URL "/2026/07/27/github-pypi-add-time-absed-defenses-against-supply-chain-attacks/" 確認 ✓ |
| BleepingComputer / SecurityWeek (Coca-Cola Fairlife 公式確認) | BleepingComputer "July 27, 2026" 確認 ✓ / FoodNavigator "July 27" 確認 ✓ |
| BleepingComputer (ShinyHunters EY 犯行声明) | BleepingComputer July 27 ヘッドライン確認 ✓ |
| Cybernews / DoubleVerify (Android AfterCall 広告詐欺) | Cybernews "July 27, 2026" 確認 ✓ |
| THN / SecurityOnline (vBulletin CVE-2026-61511 PoC) | THN タイトル "Public Exploit Released for Patched vBulletin Pre-Auth Code Execution Flaw" 確認 ✓ / SecurityOnline "19 hours ago" (= 2026-07-27 相当) 確認 ✓ |
| GitHub Advisory GHSA-gv7g-jm28-cr3m / THN (n8n sandbox escape) | GitHub Advisory 公開 2026-07-22 確認 ✓ / Thomas Harris WordPress "/2026/07/27/" 確認 ✓ |
| MSRC / SecurityOnline / GBHackers (CVE-2026-49176 WalletService PoC) | SecurityOnline "19 hours ago" (= 2026-07-27 相当) 確認 ✓ / MSRC 参照確認 ✓ |
| jvn.jp / jpcert.or.jp / ipa.go.jp / piyolog / ScanNetSecurity | 2026-07-26〜27 新規エントリ: 検索で見つからず / 最新は 2026-07-23 のもの (Duplicati / ISC BIND 等) |

### 集計サマリ

- **巡回ソース数**: 約 25
- **採用件数**: AI=6 / Security=5 / CVE=3 / 国内=0
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-07-26 より前):
    - CVE-2026-48282 Adobe ColdFusion KEV (2026-07-07 追加)
    - CVE-2026-45659 SharePoint KEV (2026-07-01 追加)
    - CVE-2026-56164 SharePoint EoP KEV (2026-07-14 追加)
    - CVE-2026-50661 BitLocker bypass (2026-07-15 Patch Tuesday / 野生悪用未確認)
    - BeyondTrust CVE-2026-40138/40139 (2026-07-06 開示)
    - Januscape CVE-2026-53359 KVM escape (2026-07-06 開示)
    - snap-confine CVE-2026-8933 Ubuntu LPE (2026-07-21 Qualys 開示)
    - LegacyHive Windows ProfSvc zero-day (2026-07-15 PoC 公開)
    - GitHub bug bounty payout cut (初報 2026-07-22 THN)
    - GhostApproval symlink (2026-07-09 THN)
    - ISC BIND JVN 勧告 (2026-07-23)
  - 重複 (直近 7 ダイジェスト掲載済み・excluded_set 参照):
    - OpenAI GPT-5.6 Sol / HuggingFace 境界侵害 (07-23/24 掲載済み)
    - Kimi K3 open weights / UK AISI 評価 (07-27 掲載済み)
    - Fastjson CVE-2026-16723 (07-27 掲載済み)
    - SourTrade malvertising (07-27 掲載済み)
    - ShinyHunters sextortion (07-27 掲載済み)
    - Steam ClickFix XMRig (07-27 掲載済み)
    - GitLab Jupyter Heap BOF (07-26 掲載済み)
    - Logto JVNVU#99418634 (07-26 掲載済み)
    - CVE-2026-32194/32191 Bing Images (07-26 掲載済み)

### 主要採用補足

- **Claude 共有チャット Google インデックス**: Daniel J Glover Blog の URL に "/2026-07-26-shared-claude-conversations-google/" が含まれ 7/26 公開確認。Reddit 発覚 → VentureBeat・Cybernews が同日報道
- **n8n GHSA-gv7g-jm28-cr3m**: GitHub Advisory 公開は 2026-07-22 だが THN・Thomas Harris の主要報道が 2026-07-27 に集中確認 → 直近 7 ダイジェスト未掲載・ニュースサイト掲載日基準で採用 (7-Zip CVE-2026-14266 と同様の扱い)
- **Claude Code symlink (Tego AI)**: GlobeNewswire 初報 "/news-release/2026/07/24/" 確認。GBHackers が 2026-07-27 に報道 → 07-26 ダイジェスト (採用窓 7/24〜26) 未収録・ニュースサイト掲載日 7/27 で採用
- **CVE-2026-49176 WalletService PoC**: SecurityOnline が "19 hours ago" (= 7/27 相当) として PoC 公開報道。Patch 自体は 7/14 Patch Tuesday 含有。PoC 公開日を採用基準に

### 取得失敗ソース

- Enterprise Times / eSecurity Planet / dailyaibrief: 403 Forbidden → WebSearch スニペット・二次ソースで代替
- bleepingcomputer.com / thehackernews.com: 403 → WebSearch スニペット代替

</details>

---

*生成: keda-digest-bot / 2026-07-28 05:05 JST*
