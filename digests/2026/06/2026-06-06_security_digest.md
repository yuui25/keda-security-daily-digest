# KEDA Daily Digest — 2026-06-06 (JST)

> 採用範囲: 公開日 2026-06-04 〜 2026-06-06
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Anthropic が国家安全保障局 (NSA) に 6 名のエンジニアを派遣し Claude Mythos で対中・対イランのオフェンシブサイバー作戦を展開していることが TechCrunch のスクープで判明、AI が国家安全保障の主要オフェンスツールとなった象徴的な事例として波紋を呼んでいる。CVE 面では Cisco が 2026 年 7 本目の SD-WAN 未パッチゼロデイ (CVE-2026-20245) を警告したほか、Cisco Unified CM の SSRF→root PoC も公開されており、Cisco インフラへの緊急対応が必要。米議会は州 AI 規制を 3 年間連邦優先化する超党派 269 ページ法案を公開し、Adversa AI の AIRQ 評価では市販 AI エージェントの 98% がデフォルトで深刻脆弱と測定された。

---

## AI 関連ニュース

- **[2026-06-05]** [Anthropic が NSA に 6 名のエンジニアを派遣し Claude Mythos でオフェンシブサイバー作戦を展開 — 対中・対イランを標的とした作戦への活用が TechCrunch/FT の調査で明らかに](https://techcrunch.com/2026/06/05/nsa-said-to-be-readying-anthropics-mythos-for-use-in-cyber-operations/) — Anthropic は Mythos を「公開不可」としながら NSA に "forward-deployed" エンジニアを常駐させ同モデルで hacking 作戦を支援；同社は Pentagon の「supply-chain risk」ラベルに対し訴訟中でもあり、自社モデルの攻撃利用をめぐる矛盾が露呈した *(TechCrunch / The Decoder / Tom's Hardware)*

- **[2026-06-04]** [OpenAI が ChatGPT Dreaming V3 メモリアーキテクチャを展開開始 — Plus/Pro ユーザーに自動更新型記憶、事実想起精度が 41.5%→82.8% に改善](https://www.techtimes.com/articles/317840/20260605/chatgpt-memory-dreaming-update-openai-rewrites-personalization-engine-limits-audit-trail.htm) — 会話から自動的にコンテキストを合成し「シンガポールに来月行く」が帰国後に自己書き換え；監査証跡が限定的で「何を記憶しているか見えにくい」プライバシー懸念も提起 *(TechTimes / Gigazine)*

- **[2026-06-04]** [米議会が「Great American Artificial Intelligence Act」269 ページ草案を超党派で公開 — 州 AI 規制を 3 年間連邦優先化し、California AB 2013 (訓練データ開示) を無効化](https://rollcall.com/2026/06/04/bipartisan-ai-draft-proposes-three-year-preemption-of-state-laws/) — Obernolte / Trahan 議員らが主導；Trump EO の任意モデル審査と並行し連邦レベルの AI 規制競争が加速。ACLU・AI 安全団体は「世代的誤り」と即時反発 *(Roll Call / Nextgov / ACLU)*

- **[2026-06-04]** [Adversa AI が AIRQ (AI Risk Quadrant) オープンソースフレームワーク公開 — 100 以上の AI エージェントを評価、98% がデフォルトで "Lethal Trifecta" (高攻撃面・広爆発半径・低防御) に露出](https://adversa.ai/blog/adversa-ai-launches-airq-framework-report/) — OWASP・CoSAI・CSA・NIST が共同貢献；エージェントのセキュリティスコアをゼロデイから爆発半径まで定量化するオープン評価基盤として業界初 *(Adversa AI / PR Newswire)*

- **[2026-06-04]** [Adversa AI が Top MCP Security Resources June 2026 を公開 — Censys が 12,520 台のインターネット公開 MCP を確認しその約 40% が無認証、VIPER-MCP が 40,000 リポジトリ走査で 67 CVE を発見、NSA が MCP 設計指針を公表](https://adversa.ai/blog/top-mcp-security-resources-june-2026/) — Akamai も非公開の DB-MCP フラグを 3 件開示 (うち 1 件未修正)；MCP のデファクト標準化が進む一方で認証欠落が最大のリスクとして顕在化 *(Adversa AI)*

- **[2026-06-04]** [Proofpoint が TA4922 中国関連グループの LLM 支援マルウェア開発と欧州・アフリカへの標的拡大を開示 — Atlas RAT / SilentRunLoader / ValleyRAT の新ツールセットを英独伊・南アに展開](https://thehackernews.com/2026/06/china-linked-ta4922-expands-phishing.html) — Proofpoint は「コードコメント・プレースホルダ値・AI 生成コードの典型パターン」から LLM 活用を高確度で推定；日本発祥の金融 APT が AI で開発加速しグローバル化した典型例 *(The Hacker News / Proofpoint / Infosecurity Magazine)*

---

## セキュリティ関連ニュース

- **[2026-06-05]** [Cisco が Catalyst SD-WAN Manager の 2026 年 7 本目の野外悪用ゼロデイ CVE-2026-20245 を警告 — CLI への細工ファイル注入で root 昇格、パッチ未リリース、全デプロイ形態 (オンプレ・Cloud-Pro・FedRAMP) に影響](https://www.helpnetsecurity.com/2026/06/05/cisco-sd-wan-cve-2026-20245-0-day-exploited/) — Mandiant が Cisco PSIRT に報告；Cisco SD-WAN は 2026 年だけで 7 件の野外悪用ゼロデイが確認された "最多被害製品" となった。パッチまで管理インターフェースへのアクセス制限を強く推奨 *(Help Net Security / SecurityWeek)*

- **[2026-06-04]** [VS Code 零デイ: Ammar Askar が github.dev の WebView OAuth トークン窃取を 1 時間前通告で完全公開 — 1 クリックで全プライベートリポジトリへの読み書きアクセスが可能な GitHub Token が流出](https://www.bleepingcomputer.com/news/security/vs-code-zero-day-lets-hackers-steal-github-tokens-in-one-click/) — 悪意ある Jupyter Notebook をクリックするだけで WebView がキーストロークをシミュレートし悪意ある拡張をインストール；Askar は以前の MSRC との悪経験から MSRC をスキップして全公開。Microsoft は 6/3 に緩和策を適用済み。CVE 未採番 *(BleepingComputer / The Hacker News / SecurityWeek)*

- **[2026-06-04]** [Cisco Unified CM CVE-2026-20230 の PoC が公開 — WebDialer SSRF でファイルを OS に書き込み root に昇格する手順が GitHub に流出、Cisco は 6/3 パッチ済みだが未適用組織は危険](https://thehackernews.com/2026/06/cisco-patches-cve-2026-20230-in-unified.html) — デフォルト無効の WebDialer を有効化している環境のみ影響；Cisco PSIRT は野外悪用を未確認だが PoC 公開後のエクスプロイトリスクが高まっている *(The Hacker News / TechTimes)*

- **[2026-06-05]** [PCPJack が AWS・Google Cloud・Azure の 230 サーバーを侵害して秘密 SMTP リレーネットワークを構築 — Hunt.io が C2 サーバーの無防備ディレクトリからソースコードと侵害状況を完全公開](https://thehackernews.com/2026/06/pcpjack-hijacks-230-aws-google-cloud.html) — EC2・GCP Managed Instance Group・Azure VM を 5 分ごとに同期する SMTP プロキシ網を構築しスパム・フィッシング送信に悪用；SentinelOne が 4 月に発見した同クレデンシャル窃取フレームワークの新段階 *(The Hacker News / Hunt.io / Dark Reading)*

- **[2026-06-04]** [100 以上のフリーウェア偽サイト (Ghidra・dnSpy・SpiderFoot 偽装) が Google 検索上位を占有 — TDS で Remus Stealer / AnimateClipper / SessionGate を配布](https://thehackernews.com/2026/06/fake-sites-mimicking-open-source-tools.html) — CloudFront 経由の JS ステージングレイヤーが VPN・ボット・既訪問者を除外して悪意ある配布を実施；Remus Stealer は 20 以上のブラウザと暗号ウォレット/2FA ツールを標的、AnimateClipper は 20 以上のブロックチェーンでウォレットアドレスを横取り *(The Hacker News / Check Point Research / TechRadar)*

- **[2026-06-04]** [Hola Browser Windows版が供給チェーン侵害でモネロ暗号マイナーを密かに配布 — Sophos X-Ops が AppEsteem 認定テスト中に `me.exe` (偽装 `HolaMonitorService.exe`) を発見](https://www.bleepingcomputer.com/news/security/hola-browser-for-windows-compromised-to-deliver-cryptominer/) — マイナーは Windows Defender 除外ルールを追加し起動サービスに偽装して常駐；影響ユーザーは約 0.1%。Hola 社は配布パイプラインを完全再構築し高度なコード署名検証を実装したと発表 *(BleepingComputer / Sophos / SC Media)*

- **[2026-06-05]** [Google Chrome 149.0.7827.53 がセキュリティ更新 — 過去最大規模の 429 CVE を修正、22 件がクリティカル (CVE-2026-10881〜10902)、ANGLE OOB 書き込みが CVSS 9.6 で最高深刻度](https://www.securityweek.com/chrome-149-patches-429-vulnerabilities/) — Google が 371 件を自社発見 (AI ツール含む)；野外悪用は現時点で未確認だが段階的展開中のため速やかな更新が必要。Chromium 系ブラウザ全般 (Edge・Brave・Opera・Vivaldi) が対象 *(SecurityWeek / PCWorld)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-04 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-20245 | Cisco Catalyst SD-WAN Manager (オンプレ・Cloud-Pro・FedRAMP 全形態) | CWE-88 / High | 認証済みローカル攻撃者が CLI に細工ファイルをコマンド引数として渡す → 入力検証欠落でシェルに解釈 → root 権限コマンド実行 | [Cisco SA cisco-sa-sdwan-rpa2-v69WY2SW](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-rpa2-v69WY2SW) (commit 不明・パッチ未リリース) | **野外悪用中 (2026-06-05)** / 未パッチ / 2026 年 7 本目 SD-WAN 0-day / Mandiant 発見 / CLI 引数インジェクションパターンとして同系製品へのバリアントハント推奨 |
| CVE-2026-48579 | Microsoft Exchange Online | CWE-863 / **9.1** | 未認証ネットワーク攻撃者が不適切な認可制御を突いて任意の HTTP リクエストを送信 → アクセス制限をバイパス → 機密メールコンテンツの情報開示 | [MSRC CVE-2026-48579](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-48579) (Microsoft クラウド側で適用済み・ユーザーアクション不要) | 2026-06-04 公開 / CVSS 9.1 / 非認証・ネットワーク経由 / Exchange Online SaaS での自動修正パターン確認 |
| CVE-2026-10881 | Google Chrome < 149.0.7827.53 (ANGLE グラフィクスエンジン) | CWE-787 / **9.6** | 悪意ある HTML ページが ANGLE で OOB 書き込みを誘発 → 侵害済みレンダラープロセスがサンドボックスを脱出 → ホスト OS で任意コード実行 | [Chrome 149.0.7827.53 リリース](https://chromereleases.googleblog.com/2026/06/) (commit 非公開) | 2026-06-05 公開 / CVSS 9.6 (429 CVE 中最高) / Chromium 系全ブラウザへのバリアント確認推奨 |
| CVE-2026-20230 | Cisco Unified CM & Session Management Edition (WebDialer 有効環境) | CWE-918 / Critical | 未認証攻撃者が WebDialer の HTTP リクエストを細工 → SSRF でサーバー OS に任意ファイルを書き込み → root 権限昇格チェーンが成立 | [Cisco SA cisco-sa-ucm-webdialer](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/) (patch 2026-06-03) | 2026-06-04 PoC 公開 / デフォルト無効 WebDialer 有効環境が対象 / SSRF→ファイル書き込み→権限昇格のチェーンパターン |
| CVE-2026-10796 | nvm (Node Version Manager) ≤ 0.40.4 | CWE-77 / TBD | 攻撃者が制御する Node.js ミラーが細工したバージョン文字列を返す → nvm がバージョン文字列を評価時に OS コマンドとして解釈 → `nvm install` 実行時にシェルで任意コード実行 | [NVD CVE-2026-10796](https://nvd.nist.gov/vuln/detail/CVE-2026-10796) (commit 調査中) | 2026-06-04 公開 / CI/CD・開発環境でのサプライチェーンリスク / pyenv・rbenv・tfenv 等類似ミラーベースツールへのバリアントハント推奨 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-06-05 | CVE-2026-34126 / JVN#70631953 | TP-Link Tapo D100C・L535E・P300 がBluetooth初期設定中に平文通信 — 攻撃者が Bluetooth 範囲内で盗聴/MITM し機密情報を窃取・デバイス制御を乗っ取り可能 | 未定 / 近接攻撃・Bluetooth 盗聴 | [JVN#70631953](https://jvn.jp/en/jp/JVN70631953/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 30 ソース (TechCrunch, The Decoder, Tom's Hardware, TechTimes, Gigazine, Roll Call, Nextgov, Adversa AI, PR Newswire, Proofpoint, The Hacker News, BleepingComputer, Help Net Security, SecurityWeek, PCWorld, Hunt.io, Dark Reading, Check Point Research, Sophos, SC Media, Infosecurity Magazine, JPCERT, JVN, MSRC, Cisco PSIRT, NVD, Guard MSSP, TechRadar, cyberinsider, winbuzzer 他)
- 採用件数: AI=6 / Security=7 / CVE=5 / 国内=1
- 除外理由内訳:
  - 採用窓外 (< 2026-06-04): DentaQuest 2.6M breach (06-02 DentaQuest 確認) / NVIDIA RTX Spark Windows PC (06-01 発表) / Anthropic Project Glasswing 拡大 (06-02) / Gamaredon WinRAR CVE-2025-8088 (06-02) / CVE-2026-43512 Apache Tomcat 9.8 (05-12) / Firefox 150 + Mythos 271 件 (04-21) / Apple iOS 26.5.1 / macOS 26.5.1 (06-01 no CVE entries) / Machine consciousness FT article (日付不確定 → 除外)
  - 重複 (excluded_set 直近7日): CVE-2026-45247 Mirasvit KEV (06-05 digest) / IronWorm npm (06-05) / HTTP/2 Bomb CVE-2026-49975 (06-05) / OpenStack Ironic CVE-2026-48681 (06-05) / CVE-2026-8206 Kirki WordPress (06-04) / CVE-2022-0492 cgroups KEV (06-04) / CVE-2026-5509 TP-Link BE450 (06-04) / CVE-2026-23787 Samsung Exynos (06-04) / CVE-2025-48595 Android (06-03) / IBM WebSphere CVE-2026-9311/9330 (06-03) / praisonai CVE-2026-47406/47408 (06-03) / Nightmare Eclipse 第二研究者 (06-05) / Microsoft Secure Boot (06-05) / Exchange outage EX1331830 (06-05) / Dragon Weave APT Azure C2 (06-03) / WP Maps Pro CVE-2026-8732 (06-03) / Defender CVE-2026-41091/45498 (06-02) / CVE-2026-41089 Netlogon (06-02) / Miasma npm TeamPCP (06-02) / Casdoor SAML VU#780781 (06-02) / praisonai CVE-2026-47418 (06-02) / GitHub内部リポジトリ TeamPCP Nx Console (06-02) / CIFSwitch Linux (06-02) / FortiClient CVE-2026-35616 (05-31) / CVE-2026-0257 PAN-OS (05-31) / Flowise CVE-2026-40933/41264 (06-01) / Gogs 0-day KEV (05-30) / Chrome 148 CVE-2026-9872/9873 (05-30) / Cisco SD-WAN CVE-2026-20182 (already in excluded)
  - 日付不明・確認不可: CVE-2026-47708 stata-mcp (GitHub Advisory 403 で CVSS 未確認) / FT Machine Consciousness article (publication date 不明) / CISA KEV June 4-6 新規追加 (CISA direct fetch 403)
  - 採用窓外 + excluded でない候補で優先度落ち: Claude Sonnet 4.8 leak (03-31 source) / WWDC 2026 発表 (06-08 開幕のため未発生)
- 取得失敗ソース (HTTP 403): bleepingcomputer.com 個別記事直接フェッチ / buildfastwithai.com / xloggs.com / CISA.gov / anthropic.com/news / tech.yahoo.com / NVD detail pages / thehackernews.com 個別記事 — WebSearch スニペット + 複数独立記事で内容・日付を補完
- 備考: CVE-2026-20245 Cisco SD-WAN は June 5 報道 (Help Net Security: "cisco-sd-wan-cve-2026-20245-0-day-exploited") にて野外悪用確認を採用。Chrome 149.0.7827.53 は stable channel への 429 CVE セキュリティ更新として June 5 付けの PCWorld / SecurityWeek 記事を採用。nvm CVE-2026-10796 は NVD publication date June 4 を確認。

</details>
