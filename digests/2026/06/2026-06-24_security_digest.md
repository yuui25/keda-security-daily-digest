# KEDA Daily Digest — 2026-06-24 (JST)

> 採用範囲: 公開日 2026-06-22 〜 2026-06-24
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Five Eyes 5 か国情報機関が「フロンティア AI によるサイバー攻撃は年単位ではなく月単位で到来する」と共同警告を発し、OpenAI は同日に Daybreak「Patch the Planet」— GPT-5.5-Cyber フル提供・Trail of Bits との OSS パッチ自動化プログラム—を発表する対照的な展開となった。攻撃面では Tata Electronics (Apple・Tesla サプライヤー) が World Leaks ランサムウェアに 630 GB 規模のサプライチェーンデータを流出させ、ShapedPlugin の WordPress Pro ビルドパイプラインが侵害されて 40 万超サイトにバックドアが配布された。CVE では FFmpeg PixelSmash (CVE-2026-8461、CVSS 8.8) が動画 1 ファイルで Jellyfin/Nextcloud 等の RCE を可能にすると JFrog が公開、29 年物の Squidbleed (CVE-2026-47729) は AI (Claude Mythos Preview) 支援により発見された。

## AI 関連ニュース

- **[2026-06-23]** [Five Eyes 5 か国情報機関が共同声明: 「フロンティア AI は現在の業界予測を超えサイバー能力を根本的に変革する — 脅威は年単位ではなく月単位で到来」— 米英豪 NZ 加 5 か国が初の共同 AI 脅威評価を発表; 攻撃者が AI で速度・規模・巧緻性を向上させる一方で防御にも寄与するとし、古いシステムのパッチ適用と最小権限原則の即時実施を勧告](https://www.euronews.com/next/2026/06/23/ai-cyber-threat-is-months-not-years-away-western-intelligence-agencies-warn) *(Euronews / CNN / CyberScoop / The Next Web)*

- **[2026-06-22/23]** [OpenAI、Daybreak を拡張し「Patch the Planet」プログラムを発表 — Trail of Bits 共同で GPT-5.5-Cyber を 19 の OSS プロジェクト (cURL・Go・Python・Sigstore・aiohttp 等) に適用し数百件の脆弱性を検出・修正マージ; Codex Security プラグイン更新で発見→パッチ自動化を加速; HackerOne・Calif と連携し「修正のボトルネック」を解消する戦略に転換; 同日 GPT-5.5-Cyber のフル版を検証済みディフェンダーへ限定提供](https://openai.com/index/patch-the-planet/) *(OpenAI / Trail of Bits Blog / IT Pro / Engadget)*

- **[2026-06-21/22]** [Samsung Electronics が ChatGPT Enterprise と Codex を韓国全社員および DX 部門グローバル社員に全面展開 — OpenAI 史上最大規模のエンタープライズ案件; ソフトウェア開発・製品開発・製造・マーケティング全業務に適用; 韓国の Codex 週次アクティブユーザーは 2 月以降 800% 増; 2023 年の社内 AI 禁止令から一転してフル採用へ](https://openai.com/index/samsung-electronics-chatgpt-codex-deployment/) *(OpenAI / SammyGuru / gHacks)*

- **[2026-06-22/23]** [Squidbleed (CVE-2026-47729): Claude Mythos Preview 支援の Calif Security Research が 29 年物 Squid Proxy FTP バグを発見 — 1997 年コミット由来の `strchr()` ヌル終端バグが Squid 全バージョン default 設定で露出; 同プロキシを共有する他ユーザーの HTTP Authorization ヘッダー・クッキー・セッショントークンが生テキストでヒープから漏洩; Heartbleed と同様の受動的メモリリーク; Squid 7 (April マージ・May GA) で修正済み](https://www.theregister.com/security/2026/06/23/mythos_discovers_squidbleed_a_memory_leak_thats_gone_undetected_since_clinton_era/5260367) *(The Register / SecurityWeek / SecurityAffairs)*

- **[2026-06-22]** [DifyTap: Zafran が Dify (OSS AI ワークフロープラットフォーム、146,000+ GitHub スター、1M+ アプリ稼働) に 4 件の脆弱性を公開 — CVE-2026-41948 (CVSS 9.4) はプラグイン Daemon REST API へのパストラバーサルで内部エンドポイントに無断アクセス; CVE-2026-41947 (CVSS 9.1) は認可バイパスで他テナントのトレース設定を操作 → テナント横断 AI チャット内容盗聴; 修正: Dify 1.14.2 (CVE-2026-41948 は PR マージ済み・次リリース待ち)](https://www.zafran.io/resources/difytap-zafran-discovers-how-attackers-can-silently-wiretap-ai-data-across-tenants-on-a-platform-powering-1m-apps) *(Zafran / The Hacker News / GBHackers)*

- **[2026-06-22]** [OpenAI が「Codex-Maxxing for Long-Running Work」ホワイトペーパーを公開 — AI エージェントを持続的ワークスペースとして活用する実践ガイド; 大目標を検証可能なステップに分解し複数ワークストリームの継続性を保つ戦略を解説; Codex のエージェント実行委任と人間監督の判断基準も提示](https://openai.com/index/codex-maxxing-long-running-work/) *(OpenAI / StartupHub.ai)*

## セキュリティ関連ニュース

- **[2026-06-22]** [Tata Electronics (Apple の iPhone インド生産 3 割・Tesla チップ供給) が World Leaks ランサムウェアの侵害を確認 — 204,341 ファイル・630.4 GB を漏洩; Apple 製造プロセス文書・Tesla 設計図・エンジニアリング仕様・従業員パスポートスキャン等が含まれる; World Leaks は Hunter's International の再ブランドと分析; 身代金要求拒否後にダークウェブで公開; Apple は「調査中」と声明](https://techcrunch.com/2026/06/22/tata-electronics-a-major-tech-supplier-to-apple-and-tesla-confirms-data-breach/) *(TechCrunch / Cybernews / TechRadar / Business Standard)*

- **[2026-06-22]** [ShapedPlugin の WordPress Pro プラグイン用ビルドパイプラインが侵害され、公式ライセンス更新チャネル経由でバックドア配布 (CVE-2026-10735, CVSS 9.8) — 5 月 21 日に Easy Digital Downloads (EDD) 更新システムを侵害し LicenseLoader.php を注入; 管理者認証情報・2FA シークレット窃取・Tiny File Manager/Adminer ウェブシェル・REST API バックドアを設置; 影響: Product Slider Pro for WooCommerce (<3.5.4)・Real Testimonials Pro・Smart Post Show Pro (<4.0.2); 累計 40 万+ インストール](https://thehackernews.com/2026/06/shapedplugin-wordpress-pro-plugins.html) *(The Hacker News / BleepingComputer / Wordfence)*

- **[2026-06-23]** [Kaspersky、WhatsApp Desktop/Web 経由の VBScript マルウェアキャンペーンを公開 — 侵害済み WhatsApp アカウントが「Financial Reports.vbs」等の偽ビジネス文書を DM 配信; 実行後に多段スクリプトチェーンで ManageEngine Endpoint Central RMM を管理者権限でサイレントインストール → 攻撃者が持続的リモートアクセスを取得; 80% がマレーシア被害・他 10 か国拡散中; 中国語インフラ痕跡・ValleyRAT/Gh0st RAT との IP 重複を観測 (帰属未確認)](https://securelist.com/whatsapp-vbs-rmm-campaign/120290/) *(Kaspersky Securelist / The Hacker News)*

- **[続報][2026-06-23]** [FortiBleed: 専用ゴールラングツール「FortigateSniffer」が Fortinet 正規診断コマンドを悪用し 24 プロトコル (Kerberos/RADIUS/NTLM/RDP/LDAP 等) の認証情報を受動キャプチャ — 430,000+ 台の FortiGate をターゲット化し 2 月以来 1 億 1,000 万件超の認証情報を収集; 659 以上の採取パイプライン; NATO 加盟国防衛請負業者の確認侵害を含む; ロシア語圏 IAB への帰属 (ツール内キリル語コメント); 被害組織の 66% は従業員 200 人以下の SMB](https://securityaffairs.com/194004/hacking/fortibleed-the-most-detailed-breakdown-yet-of-an-active-russian-credential-harvesting-operation.html) *(SecurityAffairs / GBHackers / Recorded Future / Dark Reading)*

- **[2026-06-23]** [FFmpeg PixelSmash (CVE-2026-8461): JFrog が MagicYUV デコーダーのヒープ OOB 書き込みを公開 — slice_height 値の丸め不一致でフレームアロケーターとデコーダー間の計算ずれが発生 → 攻撃者制御の AVI/MKV/MOV 1 ファイルで Kodi・mpv・Jellyfin・Emby・Nextcloud・Immich 等でクラッシュ or RCE (ASLR 無効環境・チェーン攻撃); デスクトップではフォルダブラウズだけで ffmpegthumbnailer 経由にトリガー可能 (ほぼゼロクリック); 修正: FFmpeg 8.1.2 (2026-06-17 リリース)](https://www.bleepingcomputer.com/news/security/ffmpeg-fixes-pixelsmash-flaw-in-widely-used-video-decoder/) *(BleepingComputer / JFrog / SecurityWeek / CyberInsider)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-22 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-8461 | FFmpeg < 8.1.2 (libavcodec MagicYUV デコーダー) | CWE-122 / **8.8** | `slice_height` の丸め不一致でフレームアロケーターが確保した境界を超えてクロマデータを書き出し → ヒープ OOB 書き込み → DoS / RCE (ASLR 無効 or チェーン利用) | [FFmpeg 8.1.2](https://ffmpeg.org/security.html) | 2026-06-23 JFrog 開示 / CVSS 8.8 / Jellyfin/Nextcloud 等 RCE 実証済み / MagicYUV 採用 NAS・メディアサーバー全般へバリアントハント推奨 |
| CVE-2026-47729 | Squid Proxy < 7 (FTP gateway、全バージョン) | CWE-126 / TBD | FTP ディレクトリリスト解析ループ内で `strchr()` がヌル終端文字をサーチ対象と誤認識 → ポインタ算術バグでヒープ OOB 読み出し → 同プロキシ共有ユーザーの HTTP Authorization ヘッダー・クッキー・セッショントークンが漏洩 (TLS CONNECT トンネルは対象外) | [Squid 7.0 (dev ブランチ April マージ)](https://www.squidbleed.xyz/) | 2026-06-22/23 Calif Security Research 開示 / **AI 支援発見 (Claude Mythos Preview)** / 29 年放置バグ / FTP パーサーを持つ他プロキシ実装へのバリアントハント推奨 |
| CVE-2026-41948 / CVE-2026-41947 | Dify (langgenius/dify) < 1.14.2 (pip/Docker) | CWE-22/CWE-862 / **9.4 / 9.1** | (CVE-2026-41948) 認証済みユーザーがプラグイン Daemon REST API 転送リクエストの URL パスをトラバーサルで操作 → 内部非公開エンドポイントへアクセス; (CVE-2026-41947) editor ロールユーザーがテナント所有者チェックなしで任意アプリのトレース設定を操作 → クロステナント AI チャット内容盗聴 | [Dify 1.14.2](https://github.com/langgenius/dify/releases) (CVE-2026-41948 は PR マージ・次版待ち) | 2026-06-22 Zafran 開示 / CVSS 9.4 / 1M+ アプリ稼働のマルチテナント AI プラットフォーム / 同種の plugin daemon 中継アーキテクチャ (Flowise・n8n 等) へのバリアントハント推奨 |
| CVE-2026-10735 | ShapedPlugin WordPress Pro プラグイン群 (Product Slider Pro <3.5.4 / Smart Post Show Pro <4.0.2 / Real Testimonials Pro) | CWE-506 / **9.8** | ビルドパイプライン (EDD 更新システム) 侵害 → LicenseLoader.php が管理者アクセス時に C2 からバックドアをダウンロード→フェイクプラグインとして永続化 → 認証情報・2FA シークレット窃取・任意コード実行 | ShapedPlugin 修正版各最新リリース (commit 不明) | 2026-06-22 Wordfence 詳細公開 / CVSS 9.8 / 40 万+ サイト影響 / WordPress Pro プラグイン EDD 更新チャネル全般へのサプライチェーン監査推奨 |
| CVE-2026-30040 / CVE-2026-30041 | FastStone Image Viewer 8.3.0.0 (Windows) | CWE-787 / TBD | 複数ファイル形式 (CERT/CC VU#936962) の解析処理に境界チェック欠落 → 細工されたイメージファイルで OOB 書き込み → 任意コード実行 / DoS | FastStone Image Viewer 最新版 (開発者より修正提供) | 2026-06-22 CERT/CC・JVN 公開 / 国内 JVN 掲載 / 画像閲覧ソフトの不信任データパーサーへのバリアントハント推奨 |

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-06-22/23 | CVE-2026-30040 / CVE-2026-30041 / VU#936962 | FastStone Image Viewer 8.3 の複数ファイル形式解析に OOB 書き込み脆弱性 → 細工イメージで任意コード実行 | TBD / 高 | [JVN / CERT/CC VU#936962](https://jvn.jp/) |
| 2026-06-23 | (JVN掲載) | Microsoft Windows 回復環境 (WinRE) の UEFI/BIOS パスワード制限バイパス — 物理アクセスのある攻撃者が BitLocker を含むセキュリティ機構を回避可能 | TBD / 中〜高 | [JVN](https://jvn.jp/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 32 ソース (Five Eyes / Euronews / CNN / CyberScoop / The Next Web, OpenAI Blog / Trail of Bits Blog / IT Pro / Engadget, Samsung / OpenAI / gHacks, The Register / SecurityWeek / SecurityAffairs (Squidbleed), Zafran / The Hacker News / GBHackers (DifyTap), TechCrunch / Cybernews / TechRadar / Business Standard (Tata), Wordfence / THN / BleepingComputer (ShapedPlugin), Kaspersky Securelist / THN (WhatsApp), SecurityAffairs / GBHackers / Recorded Future / Dark Reading (FortiBleed), JFrog / BleepingComputer / SecurityWeek / CyberInsider (FFmpeg), CERT/CC / JVN (FastStone), GitHub GHSA, CISA KEV)
- 採用件数: AI=6 / Security=5 / CVE=5 / 国内=2
- 採用件数が目安 (各 8〜12 件) を下回った理由:
  - AI: Noam Shazeer 移籍 (6/18) と John Jumper 移籍 (6/19〜20) は採用窓外 (< 2026-06-22); Gemini 3.5 Pro は 6/23 時点で GA 未到達 (limited Vertex preview のまま); GPT-5.6 は 6/23 時点で公式発表なし
  - Security: 週明け月曜起点の 3 日間 (6/22〜24) は報道ペース低調; CISA KEV 6/22〜24 追加分は複数ソーススニペットに記録なし
- 除外理由内訳:
  - 古すぎ (公開日 < 2026-06-22):
    - Noam Shazeer → OpenAI (Bloomberg/CNBC 2026-06-18)
    - John Jumper (AlphaFold Nobel) → Anthropic (Bloomberg 2026-06-19 / TechCrunch 2026-06-20)
    - Microsoft RAMPART & Clarity open-source (2026-05-20)
    - OWASP Agentic Research Council (Infosec Europe 2026-06-04)
    - OpenAI Daybreak 初回発表 (2026-05 THN 記事)
    - WeKnora MCP CVE-2026-30861 (2026-03-07)
  - 重複 (excluded_set 直近 7 ダイジェスト 2026-06-17 〜 2026-06-23):
    - AryStinger Botnet (D-Link/QNAP), OpenAM CVE-2026-44203/41573, XWiki Pro CVE-2026-44179, AVideo CVE-2026-33692 (6/23 digest)
    - picklescan CVEs (6/22 digest), crawl4ai JWT CVE-2026-56265 (6/22 digest), CraftCMS CVE-2026-56382 (6/22 digest)
    - AutoJack, usbliter8 BootROM, Splunk CVE-2026-20253 KEV (6/21 digest)
    - NGINX CVE-2026-42530/42055, Node.js CVEs, GHSA-r253-r9jw-qg44 Crawl4AI RCE (6/20 digest)
    - Cisco ISE CVE-2026-20181/20190, libssh2 CVE-2026-55200, Oracle WebCenter CVE-2026-35293, Firefox mfsa2026-57 (6/19 digest)
    - FortiBleed 初報 (SOCRadar), JCE CVE-2026-48907 KEV, HAPI FHIR CVE-2026-55471 (6/18 digest)
    - LiteLLM CVE-2026-47101〜40217 chain, OX Security MCP advisory, LiteSpeed CVE-2026-54420 KEV (6/17 digest)
    - FortiBleed (CISA アラート・30K DB) は 6/23 digest 除外済み; 本日の FortigateSniffer 1.1 億件詳細報告は新規ファクトとして [続報] 採用
  - 取得失敗ソース (HTTP 403): jfrog.com/blog 個別記事, securityweek.com 個別記事, gbhackers.com 個別記事, bleepingcomputer.com 個別記事, thehackernews.com 個別記事, nvd.nist.gov 個別 CVE, squidbleed.xyz, securityaffairs.com 個別記事, cybernews.com 個別記事, techcrunch.com 個別記事, theregister.com 個別記事, blog.calif.io 個別記事 — WebSearch スニペット・複数独立媒体で内容・日付を補完

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-06-17 〜 2026-06-23) の全 CVE/GHSA/URL を除外済み。*
