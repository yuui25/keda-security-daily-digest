# KEDA Daily Digest — 2026-06-11 (JST)

> 採用範囲: 公開日 2026-06-09 〜 2026-06-11
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Microsoft June Patch Tuesday 翌日 (6/10)、Chaotic Eclipse (Nightmare-Eclipse) が完全パッチ済みWindowsに有効なMicrosoft Defender LPE「RoguePlanet」をGitHubに公開し、同研究者との報奨金紛争が「報復型連続ゼロデイ公開」として6件目に達した。AI方面では BerriAI LiteLLM の MCP サーバー command injection (CVE-2026-42271) が Starlette BadHost と連鎖することで非認証 RCE に至るとHorizon3.aiが実証、CISA KEV 入りが確認された。Miasma 系列の新キャンペーン「Hades」が Anthropic / AWS / GitHub 等のクレデンシャルを狙う 19 PyPI パッケージを継続的に汚染中。OpenSSL は Claude AI との協働で発見された PKCS#7 ヒープ UAF (CVE-2026-45447) を含む 18 件をパッチ適用した。

---

## AI 関連ニュース

- **[2026-06-09]** [BerriAI LiteLLM の CVE-2026-42271 が CISA KEV に追加 — AI LLM ゲートウェイの MCP サーバー preview 機能に command injection、Horizon3.ai が Starlette BadHost (CVE-2026-48710) との連鎖で非認証 RCE を実証; 連邦機関修正期限 2026-06-22](https://thehackernews.com/2026/06/litellm-flaw-cve-2026-42271-exploited.html) — LiteLLM はエンタープライズ向け LLM プロキシ/ゲートウェイとして広く使われており、AI インフラへの直接攻撃ルートが実証されたことが衝撃を与えた *(The Hacker News / CISA / SOCRadar)*

- **[2026-06-09]** [Miasma 後継「Hades」キャンペーンが PyPI の 19 パッケージ・37 malicious wheel artifacts に .pth 起動フック型スティーラーを埋め込み — Anthropic / GitHub / AWS / GCP / Azure / Kubernetes / RubyGems 等のクレデンシャルを自動窃取](https://thehackernews.com/2026/06/hades-pypi-attack-19-packages-poisoned.html) — Python 起動時に自動実行される `.pth` ファイルの仕組みを悪用。盗んだ GitHub トークンを使って汚染パッケージを自己伝播させる Worm 機能と、「トークンを失効させると破壊行為を実行する」gh-token-monitor 恐喝デーモンが初確認 *(The Hacker News / Orca Security / StepSecurity)*

- **[2026-06-09]** [OpenSSL CVE-2026-45447 は California の研究者が Claude AI・Anthropic Research との協働で発見 — PKCS#7 署名検証 (`PKCS7_verify()`) のヒープ UAF で heap corruption・プロセスクラッシュ・潜在的 RCE; 6/9 に OpenSSL 3.6.3 / 4.0.1 でパッチ](https://www.securityweek.com/openssl-patches-high-severity-vulnerability-found-with-ai/) — AI 支援による高深刻度脆弱性発見の実績事例として注目。Claude が 2026 年 1 月に発見した 12 件の OpenSSL ゼロデイに続く AI 発見 CVE *(SecurityWeek / LessWrong)*

- **[2026-06-10]** [Nightmare-Eclipse (Chaotic Eclipse) が Microsoft Defender LPE「RoguePlanet」PoC を GitHub 公開 — race condition でDefender のファイル操作処理を乗っ取り、完全パッチ済み Windows 10/11 上でSYSTEM 権限取得](https://thehackernews.com/2026/06/microsoft-defender-rogueplanet-zero-day.html) — Microsoft との報奨金紛争に端を発する「報復型開示」シリーズ 6 件目。今回は Microsoft が公式コメント未発表のまま未パッチ状態 *(The Hacker News / BleepingComputer / SecurityWeek)*

- **[2026-06-10]** [Dark Reading「Windows Zero-Day Barrage Continues After Patch Tuesday」— Nightmare-Eclipse が 6 週間で 6 件の脆弱性を開示。1 件は CISA KEV 入り・野外悪用中。MiniPlasma (CVE-2020-17103) は 2020 年の不完全パッチが 6 年間放置されていたことが Patch Tuesday で確認](https://www.darkreading.com/cyberattacks-data-breaches/windows-zero-day-barrage-continues-after-patch-tuesday) — 研究者-ベンダー間の報奨金紛争が「組織的連続開示」という新しいリスクモデルに発展した事例として業界が注目 *(Dark Reading / CSO Online)*

- **[2026-06-08 UTC]** [OpenAI が「Built to benefit everyone: our plan」を発表 — 公益法人移行の詳細ロードマップを公開し、株主利益を AGI 開発益の一部に上限設定する枠組みを確認。OpenAI Economic Research Exchange も同時設立](https://openai.com/news/company-announcements/) — 機密 IPO 準備中の OpenAI が社会的使命を改めて強調。AIの経済的影響を外部研究者に開放する機構を公式化 *(OpenAI newsroom)*

- **[2026-06-09]** [OpenAI が Anthropic の「国際 AI 監視機構設立」提案に賛同 — 「フロンティアモデル開発を必要に応じて減速させるための協調行動が可能な国際機関を設立すべき」と声明](https://gizmodo.com/openai-joins-anthropic-in-call-for-international-ai-watchdog-2000769442) — Anthropic が 6/5 に提唱した AI 開発一時停止提案に OpenAI が賛同する形で国際ガバナンス議論が加速 *(Gizmodo)*

- **[2026-06-10]** [Colorado AI Act が 2026-06-30 に施行予定 — リスクアセスメント・影響評価・アルゴリズム差別防止措置を高リスク AI システムに義務付ける米国初の州法が迫る; 同法の対象企業は AI 利用ポリシーの緊急見直しが必要](https://www.mindfoundry.ai/blog/ai-regulations-around-the-world) — EU AI Act の完全施行 (8/2) を控え、AI コンプライアンスの法的要件が米国でも拡大する転換点 *(MindFoundry / White & Case)*

---

## セキュリティ関連ニュース

- **[2026-06-09]** [Adobe Acrobat / Reader APSB26-63 — Critical RCE を含む多数の CVE を修正; JPCERT/CC が 6/10 にアラート発出](https://helpx.adobe.com/security/products/acrobat/apsb26-63.html) — CVE-2026-47911 / 47912 / 47913 / 47915 / 47916 / 47923 / 47924 / 47937 等を含む。悪意ある PDF を開くだけで任意コード実行・DoS・メモリ露出が可能。野外悪用は現時点で未確認 *(Adobe PSIRT / JPCERT/CC / HKCERT)*

- **[2026-06-09]** [OpenSSL June 2026 パッチが 18 件の脆弱性を修正 — OCSP Stapling double-free (悪意あるサーバーがクライアント証明書検証を悪用)、NULL deref (部分チェーン証明書 + OCSP 確認の組み合わせ) 等を含む](https://openssl-library.org/news/vulnerabilities/) — OpenSSL 3.6.3 / 4.0.1 に即時アップデートを推奨。TLS インフラ全般に影響 *(OpenSSL / SecurityWeek)*

- **[2026-06-10]** [ZDI「June 2026 Security Update Review」が CVE-2026-45657 (Windows Kernel TCP/IP UAF, CVSS 9.8) を最優先 CVE に指定 — リバースエンジニアによる PoC 開発は「週単位ではなく日単位」と警告; 現時点で野外悪用未確認](https://www.zerodayinitiative.com/blog/2026/6/9/the-june-2026-security-update-review) — 非認証・ユーザー操作不要でカーネル SYSTEM 権限取得可能なワーム性 RCE。KB5094125〜KB5094128 での即時パッチ適用が急務 *(ZDI / TechTimes / The Record)*

- **[2026-06-09]** [Termite ランサムウェアが Cal Fresh (カリフォルニア州フードバンク系) を攻撃 — 6/8 侵害・6/9 にリークサイトで公表。農業・食糧生産セクターへの攻撃が継続](https://www.redpacketsecurity.com/termite-ransomware-victim-cal-fresh/) — Global Schools Foundation も 6/10 に侵害発覚。社会インフラを狙うランサムウェアの標的範囲拡大が継続 *(RedPacket Security / ransomware.live)*

- **[2026-06-09]** [BleepingComputer が June 2026 Patch Tuesday の「3 ゼロデイ」を「6 ゼロデイ」に訂正 — MiniPlasma (CVE-2020-17103 の不完全パッチ回避、6 年越しの修正)・CVE-2026-41091 (Defender EoP、5/19 に野外悪用確認・CISA KEV 追加済み) が追加判明](https://www.bleepingcomputer.com/news/microsoft/microsoft-patches-yellowkey-greenplasma-miniplasma-zero-days/) — CVE-2020-17103 は 2020 年に Patch Tuesday で「修正済み」とされたが元の PoC がそのまま動作し続けていたことが 6 年後の June Patch Tuesday でようやく根本修正 *(BleepingComputer / Petri)*

- **[2026-06-09]** [oss-security ML にて CVE-2026-48710 (Starlette BadHost、CVSS 6.5) が公開 — ASGI フレームワーク Starlette の Host ヘッダー検証バイパスにより、認証制御を回避して内部エンドポイントに到達可能; LiteLLM CVE-2026-42271 の非認証 RCE 連鎖の中継点として機能](https://socradar.io/blog/cisa-kev-litellm-cve-2026-42271-check-point-cve-2026-50751/) — ASGI フレームワークを使う FastAPI / LiteAPI 系アプリ全般に同様のバリアントが存在する可能性 *(SOCRadar / Horizon3.ai)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-09 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-42271 | BerriAI LiteLLM (MCP Server Preview 機能有効環境、全バージョン〜最新 hotfix 前) | CWE-78 / **8.7** | 任意認証済みユーザーが MCP サーバーの stdio トランスポート設定フィールドに OS コマンド・引数・環境変数を注入 → サブプロセスとして実行 → RCE; CVE-2026-48710 (Starlette BadHost) と連鎖で**非認証 RCE** に昇格 | [LiteLLM GitHub](https://github.com/BerriAI/litellm) (commit 要確認) | **CISA KEV 2026-06-08 追加** / 連邦修正期限 6/22 / AI インフラへの直接攻撃ルート / MCP Server を持つ他 LLM ゲートウェイへのバリアント展開要確認 |
| CVE-2026-45657 | Windows Kernel (Windows 11 23H2〜26H1・Windows Server 2022/2025、TCP/IP スタック搭載全バージョン) | CWE-416 / **9.8** | 非認証リモート攻撃者が Windows Kernel の TCP/IP 処理における UAF を悪用 → カーネル SYSTEM 権限 RCE → ユーザー操作不要・ワーム性伝播可能 | [KB5094125〜KB5094128 (2026-06-09)](https://msrc.microsoft.com/update-guide/) | 2026-06-09 公開 / CVSS 9.8 / **ワーム性** / ZDI が「PoC 開発は日単位」と警告 / 野外悪用未確認だが緊急度最高 |
| CVE-2026-45447 | OpenSSL 3.6.0〜3.6.2 / 4.0.0 (PKCS#7 / S/MIME 署名検証機能、TLS クライアント含む) | CWE-416 / **High (CVSS 非公表)** | 攻撃者制御サーバーが PKCS#7 SignedData の `digestAlgorithms` を空の ASN.1 SET に設定した証明書チェーンを送付 → `PKCS7_verify()` が呼び出し元所有 BIO を誤って解放 → UAF によるヒープ破壊・プロセスクラッシュ・潜在的 RCE | [OpenSSL 3.6.3 / 4.0.1 (2026-06-09)](https://openssl-library.org/news/vulnerabilities/) | 2026-06-09 公開 / **Claude AI + Anthropic Research による AI 支援発見** / PKCS#7 処理は OpenSSL 全バージョン系に共通 / S/MIME ・証明書ピン留めアプリへのバリアント要確認 |
| CVE-2026-47291 | Microsoft HTTP.sys (Windows Server 2019/2022/2025 + Windows 11) | CWE-122 / **9.8** | 非認証リモート攻撃者が細工した HTTP/2 リクエストで HTTP.sys カーネルドライバのバッファオーバーフローを誘発 → カーネル SYSTEM 権限 RCE → ユーザー操作不要 | [MSRC June 2026 Patch Tuesday](https://msrc.microsoft.com/update-guide/) | 2026-06-09 公開 / CVSS 9.8 / Hyper-V ホストや DMZ サーバーを直接露出させる構成で即時リスク |
| CVE-2026-47911 (代表) | Adobe Acrobat / Reader (Acrobat DC・Acrobat 2024・Reader DC, Windows/macOS 最新修正前バージョン) | CWE-787 / **Critical** | 悪意ある PDF ファイルを開いた際に Acrobat/Reader の PDF レンダリングエンジンがバッファ外書き込みを実行 → 任意コード実行; CVE-2026-47912/13/15/16/23/24/37 等計 8 件以上が同一バレット内で修正 | [APSB26-63 (2026-06-09)](https://helpx.adobe.com/security/products/acrobat/apsb26-63.html) | 2026-06-09 公開 / **8 件以上の Critical RCE** / PDF 閲覧だけで感染 / 野外悪用は未確認だが攻撃者の PoC 開発が進む可能性 |
| CVE-2026-48710 | Starlette ≤0.47.2 (ASGI フレームワーク, Python; FastAPI・LiteLLM 等が内部依存) | CWE-346 / **6.5** | MITM または同一ネットワーク上の攻撃者が細工した Host ヘッダーを送信 → Starlette がリクエストを内部エンドポイントに誤ルーティング → 認証バイパス → CVE-2026-42271 等と連鎖させると外部からの非認証アクセスが可能 | [starlette commit](https://github.com/encode/starlette) (0.47.3 で修正) | 2026-06-09 公開 / CVE-2026-42271 との連鎖で CISA KEV 対象に間接関与 / FastAPI を使う AI API サーバー全般に潜在バリアント |
| RoguePlanet (CVE 未採番) | Microsoft Defender Antivirus (Windows 10/11, 2026-06-10 時点で未パッチ) | CWE-362 / EoP | 低権限ローカル攻撃者が Defender の内部ファイル操作における race condition を悪用し、攻撃者制御のコードを SYSTEM 権限で実行 → 完全パッチ済み環境で SYSTEM LPE。PoC は GitHub 上で公開済み | [GitHub: Chaotic-Eclipse/RoguePlanet](https://github.com/) (PoC 2026-06-10 公開) | **CVE 未採番・未パッチ (2026-06-10現在)** / PoC 公開済み / 野外悪用はまだ未確認 / Nightmare-Eclipse 報復型開示 6 件目 / Defender は全 Windows に標準搭載 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-06-09 | JVNDB-2026-000083 | ARUCOM Inc. CamView インストーラーが DLL を安全でない検索パスからロード (CWE-427) — 攻撃者が細工した DLL を配置後にインストーラーを実行させることでコード実行; GMO サイバーセキュリティ by IERAE の松本和磨氏が発見 | CVSS 7.8 (High) / Windows 全バージョン | [JVN/JPCERT/CC](https://jvn.jp/) |
| 2026-06-10 | JPCERT/CC アラート | Adobe Acrobat / Reader (APSB26-63) に Critical 脆弱性 — 国内利用者に即時アップデートを勧告 | Critical RCE 複数 / Windows・macOS | [JPCERT/CC](https://www.jpcert.or.jp/) |
| 2026-06-10 | JPCERT/CC アラート | Microsoft June 2026 Security Updates に CVE-2026-45657 (Windows Kernel wormable RCE, CVSS 9.8) 等を含む — 国内組織に Patch Tuesday の即時適用を勧告 | Critical 33件含む208 CVE | [JPCERT/CC](https://www.jpcert.or.jp/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 40 ソース (The Hacker News, BleepingComputer, SecurityWeek, CISA, ZDI, Dark Reading, Orca Security, StepSecurity, SOCRadar, Help Net Security, TechTimes, The Record, Petri, Cybernews, RedPacket Security, ransomware.live, CSO Online, OpenSSL Library, Adobe PSIRT, HKCERT, JPCERT/CC, vulnerability.circl.lu, LessWrong, Gizmodo, OpenAI newsroom, openssl-library.org, securityaffairs.com, infosectoday.io, windowsforum.com, windowsnews.ai, ap7i.com, techtimes.com, gbhackers.com, hackread.com, zecurit.com, msrc.microsoft.com, helpx.adobe.com 他)
- 採用件数: AI=8 / Security=6 / CVE=7 / 国内=3
- 除外理由内訳:
  - 古すぎ (< 2026-06-09): Anthropic S-1 IPO 提出 (6/1) / OpenAI GPT-5.5 GA (4/23) / DeepSeek V4 (4/24) / Anthropic/Google/Broadcom 3.5GW TPU 契約 (4/7) / Microsoft MAI-Thinking-1 (6/2 Build 2026) / Gemini 3.5 Flash GA (5/19) / Anthropic "AI-enabled cyber threats" MITRE レポート (6/3) / CVE-2026-41091 Defender EoP 初報 (5/21) + CISA KEV (6/3 期限) / CVE-2025-8088 WinRAR path traversal (2025 CVE)
  - 重複 (excluded_set 直近7日): Claude Fable 5 / Mythos 5 リリース (2026-06-10 digest) / Microsoft Miasma ワーム initial + re-compromise (2026-06-07/08/10 digest) / Check Point CVE-2026-50751/50752 (2026-06-09 digest) / Exchange CVE-2026-42897 (2026-06-09 digest) / Veeam CVE-2026-44963 (2026-06-10 digest) / SAP CVE-2026-44748/27671/22732 (2026-06-10 digest) / Linux kernel nf_tables CVE-2026-23111 PoC (2026-06-10 digest) / BitLocker CVE-2026-50507 / CTFMON CVE-2026-45586 / HTTP/2 Bomb CVE-2026-49160 (2026-06-10 digest) / Hyper-V CVEs (2026-06-10 digest) / Puma CVE-2026-47737 (2026-06-10 digest) / SolarWinds CVE-2026-28318 (2026-06-08 digest) / Claude Code Action CVE (2026-06-08 digest) / Apple WWDC 2026 / iOS 27 / New Siri (2026-06-09 digest) / OpenAI Lockdown Mode (2026-06-09 digest)
  - 日付不明/確認不可: LesserWorm NPM Shai-Hulud 続報 (Socket.dev 記事だが公開日の確認不可) / CVE-2026-48027 Nx Console・CVE-2026-45321 TanStack (確認できた情報が断片的で詳細検証不十分のため保留)
- 取得失敗ソース (HTTP 403): thehackernews.com 個別記事 / securityaffairs.com 個別記事 / bleepingcomputer.com 個別記事 / gizmodo.com 個別記事 / vulnerability.circl.lu / anthropic.com/news 個別記事 / jpcert.or.jp / jvn.jp — WebSearch スニペット・複数独立媒体の記事で内容・日付を補完
- 備考:
  - CVE-2026-41091 (Defender EoP, 野外悪用) は 5/19 の out-of-band パッチ・CISA KEV 期限 6/3 が過去のダイジェスト範囲のため今回は詳細採用を控えたが、June Patch Tuesday で公式 CU 配布されたことでヘッドラインに再浮上している
  - RoguePlanet は 2026-06-10 時点でCVE 未採番・未パッチ。GitHub PoC URL は仮記載 (実際の GitHub リポジトリは Chaotic-Eclipse/RoguePlanet として複数媒体が報告)
  - OpenAI の国際 AI 監視機構賛同発言の正確な一次発表日は WebFetch 403 により確認不能。先行 search スニペットで「June 9, 2026」と記載されていたため採用したが、May 14 の別声明との混同の可能性あり

</details>
