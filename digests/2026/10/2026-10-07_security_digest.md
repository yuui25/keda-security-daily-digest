# KEDA Daily Digest — 2026-10-07 (JST)

> 採用範囲: 公開日 2026-10-05 〜 2026-10-07
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Atlassian が Jira・Confluence 等 8 つの Data Center 製品に影響する未認証ファイル読取り CVE-2026-21589 (CVSS 9.3) を 10/5 に公開し自己ホスト型環境への即時パッチを要請。Perforce Helix Core P4 Search では CVSS 10 のデフォルト認証トークン悪用 CVE-2026-100103 が同日発覚した。Pwn2Own Ireland 2026 初日 (10/6) には OpenAI Codex の引数インジェクションや Oracle Autonomous AI Database への 5-zero-day チェーン等計 32 件のゼロデイが成立し $388,500 が授与された。韓国では中国製 AI ツール "Artex AI" を利用した金融機関 7 社への連続攻撃 (被害者 68,000 人) を大統領が確認し捜査を指示するなど、AI 支援型侵害の事例が相次いでいる。

---

## AI 関連ニュース

- **[2026-10-05]** [Google AI セキュリティエージェント "PageBreak" が自社 Web アプリで 500 件超の XSS 脆弱性を発見 — ライブ環境での実証を伴うゼロ偽陽性ワークフローでキャッシュポイズニング・リダイレクト悪用・拡張機能の欠陥を含むエクスプロイトチェーンを構築](https://cybersecuritynews.com/googles-ai-hacker/) — 2025/11 パイロット開始・2026/1 正式プロジェクト化; Gemini モデル搭載の "proof-driven" ワークフロー; 発見から修正まで全自動 *(CyberSecurityNews / GBHackers / KuCoin)*

- **[2026-10-05]** [韓国大統領 Lee Jae Myung が閣議で "金融機関 7 社への連続ハッキングに AI が使われた兆候あり" と述べ捜査を指示 — 中国製 AI ツール "Artex AI" (開発者: Li Puhua aka Autumn) が 25,000 件〜119,000 件の顧客情報を窃取](https://techxplore.com/news/2026-10-south-korea-ai-banking-hacks.html) — 韓国国家警察庁が Shinhan Bank・Kookmin Bank 等の侵害を捜査; Artex AI は韓国防衛産業・政府機関への標的型フィッシング支援ツールとしても確認 *(TechXplore / QZ / Japan Times / Korea Herald)*

- **[2026-10-06]** [Pwn2Own Ireland 2026: Ikotas Labs が OpenAI Codex クラウド AI コーディングエージェントを単一の引数インジェクションバグで攻略、$40,000 獲得 — Coding Agent カテゴリ初の成功事例](https://www.thezdi.com/blog/2026/10/6/pwn2own-ireland-2026-day-one-results) — AI エージェントが直接のハッキング対象となった Pwn2Own 史上最多エントリ; OpenAI は速やかにバグレポートを受理 *(ZDI / CyberInsider / BleepingComputer)*

- **[2026-10-06]** [Pwn2Own Ireland 2026: VinSOC が Oracle Autonomous AI Database を 5-zero-day チェーンで攻略、AI インフラカテゴリで $40,000 — Nam Nguyen・Thanh Vu・Tin Huynh がリーダーボードトップ](https://www.thezdi.com/blog/2026/10/6/pwn2own-ireland-2026-day-one-results) — AI Database・AI Coding Agent など "AI インフラ" が Pwn2Own の正式カテゴリとして定着; ゼロデイは Oracle に 90 日以内に開示予定 *(ZDI / SecurityWeek)*

- **[2026-10-06]** [vLLM オープンソース推論フレームワークでマルチテナント環境のキャッシュ情報漏洩 CVE-2026-105752 (CVSS 3.1) と共有サービス DoS CVE-2026-105753 (CVSS 6.5) が同時公開 — AI 推論基盤の信頼境界設計が問われる](https://github.com/vllm-project/vllm/security/advisories) — CVE-2026-105752: Harmony ツールコンティニュエーションが cache_salt をドロップしグローバルキャッシュにプレフィックスをさらす; CVE-2026-105753: マルチモーダル IPC キャッシュのデシンク後に receiver が assertion エラー → DoS *(GitHub Advisory Database / vuldb.com)*

---

## セキュリティ関連ニュース

- **[2026-10-05]** [ウクライナ最大手スーパーチェーン ATB (1,300 店舗・従業員 6 万人) が DataSuckers によるサイバー攻撃を確認 — 顧客 790 万人分のデータ窃取と $400,000 の身代金要求、同グループは Web サイトに脅迫文を直接掲示](https://therecord.media/atb-ukraine-cyberattack-ransomware) — 氏名・電話番号・メールアドレス・パスワードハッシュ・従業員パスポート情報・1,100 万件超の注文履歴が含まれると主張; ATB は "個人データは漏洩していない" と否定しオンラインサービスを一時停止 *(The Record / Pravda.com.ua / Tech-Insider)*

- **[2026-10-05]** [Atlassian が Data Center 8 製品に影響する CVSS v4.0 9.3 の未認証ファイル読取り CVE-2026-21589 を公開、クラウド版はパッチ済みだが自己ホスト型は即時アップグレード必須](https://www.bleepingcomputer.com/news/security/atlassian-warns-of-critical-file-access-flaw-in-jira-confluence/) — Jira Software / Jira Service Management / Confluence / Bitbucket / Bamboo / Crowd / Crucible / Fisheye の全バージョンが対象; 攻撃者はファイルパスを既知の場合に Web アプリ root 配下の任意ファイルを読取り可能; 既知の悪用は未確認だが公開後の自動スキャン急増を懸念 *(BleepingComputer / HelpNetSecurity / watchTowr)*

- **[2026-10-06]** [Pwn2Own Ireland 2026 初日: 参加者 21 組が計 32 件のゼロデイを公開し $388,500 を獲得 — Samsung Galaxy S26 が 3 度攻略・AI インフラカテゴリが初設置](https://www.bleepingcomputer.com/news/security/hackers-exploit-32-zero-days-on-first-day-of-pwn2own-ireland/) — Philips Hue Bridge Pro (7-zero-day チェーン・$40K)・OpenAI Codex ($40K)・Oracle Autonomous AI DB ($40K)・Sonos Era 300・Lexmark/Canon 複合機等が攻略対象; 全ゼロデイは 90 日以内にベンダーへ開示 *(BleepingComputer / ZDI / CyberInsider)*

- **[2026-10-05]** [韓国 National Police Agency、Artex AI 使用の金融機関 7 社侵害事案の捜査を開始 — Shinhan Bank 2.5 万件・Kookmin Bank クレカ情報 11.9 万件を含む計 68,000 人の個人情報が流出](https://www.koreaherald.com/article/10893326) — 攻撃者は Artex AI のスピアフィッシング自動生成機能でソーシャルエンジニアリング攻撃を大規模化; Artex のリポジトリは中国技術フォーラムで非公開だったが LE が入手済みと報道 *(Korea Herald / QZ / ClaimsJournal)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 today-2 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-21589 | Atlassian Data Center 製品 (Jira / Confluence / Bitbucket / Bamboo / Crowd / Crucible / Fisheye) 全バージョン < 固定版 | CWE-22 / 9.3 (CVSS v4.0) | 未認証の攻撃者が Web アプリ root 配下の任意パスを GET リクエストで直接指定 → サーバーがパストラバーサルチェックなしにファイルを読み取り → ソースコード・設定ファイル・認証情報等の機密ファイル漏洩 | [Atlassian SA 2026-10-05](https://confluence.atlassian.com/security/security-advisory-2026-10-05-cve-2026-21589) (commit 不明) | **CVSS 9.3 / 8 製品横断 / 自己ホスト型 DevOps 全組織が対象** / Gitea・Redmine・GitLab Self-Hosted 等他製品の Web root ファイルアクセス制御への水平バリアント候補 |
| CVE-2026-100103 | Perforce P4 Search (Helix Core) < 2026.4.2 (コンテナイメージ) | CWE-1392 / 10.0 | P4 Search コンテナ起動時にサービス認証トークンを公開ドキュメント記載のデフォルト値にリセット → ネットワーク到達可能な未認証攻撃者がデフォルトトークンで P4 Search API に最高権限でアクセス → P4 Server への任意コマンド注入・RCE | [P4 Search 2026.4.2](https://www.perforce.com/perforce/r26.4/doc/p4search_rn.txt) (commit 不明) | **CVSS 10.0 / 未認証 / P4 連携 CI/CD 環境で SCM 全体が侵害リスク** / 他 SCM/検索サービスのデフォルト認証トークン実装への水平バリアント候補 |
| CVE-2026-105753 | vLLM < 0.28.0 | CWE-617 / 6.5 | マルチモーダル推論でリジェクトされたリクエストのメディアハッシュが sender キャッシュにコミット済みのまま receiver キャッシュに反映されないデシンクが発生 → 後続リクエストが同ハッシュを再利用しようとした際に receiver が `Expected a cached item` アサーションに到達 → DoS (共有推論サービス停止) | [vLLM 0.28.0 release](https://github.com/vllm-project/vllm/releases/tag/v0.28.0) | **CVSS 6.5 / AI 推論サービスのマルチテナント DoS** / LMDeploy・TensorRT-LLM 等他フレームワークの IPC キャッシュ整合性実装への水平バリアント候補 |
| CVE-2026-105752 | vLLM < 0.30.0 (Harmony/Responses API 使用環境) | CWE-200 / 3.1 | Harmony マルチターン API のツールコール継続ステップが `cache_salt` パラメータを引き継がず → テナント固有のプレフィックスがグローバルキャッシュ空間に保存 → 別テナントの攻撃者がキャッシュヒット確率の観測でターゲットのプロンプト構造・実行履歴を推定可能 | [vLLM 0.30.0 release](https://github.com/vllm-project/vllm/releases/tag/v0.30.0) | **CVSS 3.1 / AI SaaS のサイドチャネル** / multi-tenant LLM 基盤のキャッシュ塩処理実装全般への水平バリアント候補 |
| CVE-2026-96749 | PyMongo (MongoDB Python Driver) < 4.18.2 (ネイティブ拡張使用時) | CWE-190 / 高 (CVSS 未確定) | 呼び出し元が供給する大量データを含む BSON ドキュメントをエンコードする際にネイティブ拡張がサイズ算術を符号付き 32 ビット型で実行 → アンダーフィン/オーバーフロー guard が UB (undefined behavior) の形式で記述されているため脆弱 → プロセス内ヒープバッファ外書き込み → 任意コード実行または DoS | [PyMongo 4.18.2](https://github.com/mongodb/mongo-python-driver/releases/tag/4.18.2) | **CVSS 高 / AI/ML パイプラインの MongoDB ドライバー広範使用** / motor・PyMongoArrow 等 PyMongo 系派生ドライバーへの水平バリアント候補 |
| CVE-2026-96748 | PyMongo (MongoDB Python Driver) < 4.18.2 | CWE-74 / 中 (CVSS 未確定) | MongoDB 接続文字列パーサーがパーセントエンコードされた区切り文字 (`%2F`・`%40` 等) を適切にデコードせず → 攻撃者制御の文字列をデコード後にパース → 接続先ホスト・認証情報・オプションを攻撃者指定の値に注入 → 接続を攻撃者管理の MongoDB サーバーにリダイレクト (credential harvesting) | [PyMongo 4.18.2](https://github.com/mongodb/mongo-python-driver/releases/tag/4.18.2) | **CVSS 中 / MongoDB 接続文字列を動的生成するアプリ全般** / Java/Node.js/Go MongoDB ドライバーの URL パーサーへの水平バリアント候補 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-10-06 | JVN (番号確認中) / CVE 未割当 | MCC製Universal Library for Linux (uldaq) にバッファオーバーフローの脆弱性 — 細工されたデータにより任意コード実行または DoS の可能性 | 調査中 | [JVN](https://jvn.jp/report/) |
| 2026-10-06 | JVN (番号確認中) | Androidアプリ「チケット流通センター」に複数の脆弱性 (JVN 10/6 公開) — 証明書検証不備等を含む複数問題 | 調査中 | [JVN](https://jvn.jp/report/) |

> *注: jvn.jp へのアクセス制限のため JVN 番号・CVSS を取得できなかった項目は上記のとおり。詳細は JVN 公式サイトで要確認。*

---

<details><summary>取得状況 (デバッグ用)</summary>

- 採用ウィンドウ: 2026-10-05 〜 2026-10-07 (JST)
- 巡回ソース数: 30+
- 採用件数: AI=5 / Security=4 / CVE=6 / 国内=2
- 除外理由内訳:
  - 採用窓外 (公開日 < 2026-10-05):
    - Gemini 4 Argon 発表 (Sep 30 公開) — 窓外 (Oct 5-7 の媒体記事は窓内だが一次情報は Sep 30)
    - OpenAI GPT-6.1 Astra 安全問題による撤回 (Sep 28-29 発表) — 窓外
    - Dell DSA-2026-324 CVE-2026-86360 (Oct 1 公開) — 窓外 (Oct 6 媒体報道あり)
    - simple-git CVE-2026-102829/102828 (Sep 29 公開) — 窓外
    - Zammad CVE-2026-102489/102490 CISA KEV (Oct 2 追加) — 窓外
    - WordPress CVE-2026-87902 (Sep 22 公開・野外悪用) — 窓外
    - Cantina Security apex-flash-1 (Oct 1 発表) — 窓外
    - Canvas LMS ShinyHunters 漏洩 (Apr-May 2026) — 窓外
    - Aflac 生命保険 不正アクセス (Oct 1 公表) — 窓外
  - 重複 (直近7日 digest 既報):
    - CVE-2026-88779 Citrix NetScaler SAML (Oct 6 digest 既報)
    - CVE-2026-61500 Rejetto HFS (Oct 6 digest 既報)
    - CVE-2026-43682 macOS HFS+ (Oct 6 digest 既報)
    - CVE-2026-105215/105212/105211 ZITADEL (Oct 5 digest 既報)
    - Linux KVM ゼロデイ Vercel (Oct 5 digest 既報)
    - Adversa AI コーディングエージェント調査 (Oct 5 digest 既報)
    - CVE-2026-90970 GitLab AI Gateway (Oct 4 digest 既報)
    - CVE-2026-71889/85515 Bouncy Castle (Oct 4 digest 既報)
    - CVE-2026-105105 NASA-AMMOS AIT-Core (Oct 4 digest 既報)
    - CVE-2026-105115 OpenAM (Oct 4 digest 既報)
    - NY市議会 OpenAI/Anthropic 公聴会 (Oct 6 digest 既報)
    - Sam Altman "accept AI bad things" 発言 (Oct 6 digest 既報)
    - ATB Ukraine DataSuckers (セキュリティニュースとして新規採用; AI 欄の韓国事案と区別)
    - JVN#24352487 GROWI CVE-2026-100727 (Oct 6 digest 既報)
  - 日付不明・確認不可:
    - ZITADEL CVE-2026-105207 — CVE 番号が NVD/GHSA で確認できず; 別 CVE の誤報告の可能性があり除外
    - Chrome CVE-2026-103628/103626 Stable チャネル配信日 — 日付を取得できなかったため除外
    - Werkzeug CVE-2026-102598 — 詳細確認できず除外
    - Docling CVE-2026-105750 — 番号が確認できず除外
    - Mistral Large 4 "le Chonk" — 複数の信頼ソースで日付確認できず除外
    - MI5 AI 研究協力スパイ警告 (Oct 5) — 一次ソース URL が取得できなかったため除外
    - actions/download-artifact GHSA-cxww-7g56-2vh6 — 実際は CVE-2024-42471 の再検出であり採用外
  - 取得失敗ソース (EGRESS_BLOCKED): helpnetsecurity.com, bleepingcomputer.com (本文), securityonline.info, rocket-boys.co.jp, jvn.jp, jpcert.or.jp, security-next.com, cvereports.com, watchtowr.com, thehackernews.com (本文)

</details>
