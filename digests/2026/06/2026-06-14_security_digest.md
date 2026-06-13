# KEDA Daily Digest — 2026-06-14 (JST)

> 採用範囲: 公開日 2026-06-12 〜 2026-06-14
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

米商務省が 6/12 に輸出規制令を発動し Anthropic は Fable 5・Mythos 5 を全世界ユーザー向けに停止—フロンティア AI が連邦政府命令で運用停止した前例のない事態。AI 開発インフラへの攻撃も激化: Tenet Security が「Agentjacking」(Sentry MCP 経由で AI コーディングエージェントを乗っ取る手法) を公開し、Check Point Research は LangGraph の SQLi → msgpack 連鎖 RCE を開示、Atomic Arch は AUR 1,500+ パッケージを Rust インフォスティーラー + eBPF ルートキットで汚染した。中国 APT Velvet Ant が PAM/OpenSSH を改ざんして約 10 年間エアギャップ環境に潜伏していた事実も明らかになり、信頼済みシステムソフトウェアへの攻撃リスクが改めて浮き彫りになった。

---

## AI 関連ニュース

- **[2026-06-12]** [米商務省の輸出規制令を受け Anthropic が Claude Fable 5・Mythos 5 の全ユーザーアクセスを停止 — 商務長官 Howard Lutnick が Dario Amodei 宛に 6/12 17:21 ET に送達した「みなし輸出 (15 CFR 734.13)」指令により、米国内外を問わず外国籍ユーザー全員 (非市民の Anthropic 社員含む) へのアクセス禁止を命じ、Anthropic は全顧客向けに両モデルを無効化; Amazon 研究者が Fable 5 のサイバー能力回避ジェイルブレークを発見したことが契機](https://techcrunch.com/2026/06/12/anthropics-safety-warnings-may-have-just-backfired-the-government-has-pulled-the-plug-on-its-most-powerful-ai/) — フロンティア AI モデルが連邦政府命令で本番停止に至った初の事例; Anthropic は「ジェイルブレークは限定的で Mythos 5 の特定ケースのみ」と異議申し立て中; Claude Opus 4.8 等他モデルは影響なし *(TechCrunch / Bloomberg / CNBC / Fortune / Axios)*

- **[2026-06-12]** [Google が中国系サイバー犯罪ネットワーク「Outsider Enterprise」を Gemini AI 悪用フィッシング詐欺で提訴 — PhaaS (フィッシング・アズ・ア・サービス) として偽サイト 9,000 件超・不正 URL 100 万件を展開; 2026 年 5 月の 2 週間で Android ユーザーへ 250 万件のスミッシングを送信し AT&T / T-Mobile / Verizon を通じたブロックのためキャリア 3 社と連携](https://thehackernews.com/2026/06/google-sues-chinese-smishing-network.html) — テック大手が自社 AI の不正利用者を法的に追訴した初の事例; Google は悪用確認済みの Gemini アカウントと C2 インフラを停止済み *(The Hacker News / Help Net Security / Decrypt / OECD AI)*

- **[2026-06-12]** [Tenet Security が「Agentjacking」を公開 — Sentry の公開 DSN でエラーイベントを偽装してMCPサーバー経由でAIコーディングエージェント (Claude Code / Cursor / Codex) に悪意あるコマンドを注入; Claude Code・Cursor・Codex で 85% の成功率を確認、環境変数・Git 認証情報・API キーを窃取](https://thehackernews.com/2026/06/agentjacking-attack-tricks-ai-coding.html) — EDR・WAF・IAM・VPN・Cloudflare を完全バイパスする「Authorized Intent Chain」構造; Sentry は 6/3 に事前通知を受けていたが修正未完了 *(The Hacker News / GBHackers / Infosecurity Magazine / Cloud Security Alliance)*

- **[2026-06-12]** [Check Point Research が LangGraph SQLi → msgpack 連鎖 RCE を開示 (CVE-2025-67644 + CVE-2026-28277 + CVE-2026-27022) — 自己ホスト型 LangGraph 環境でスレッド ID を汚染するだけで SQLite チェックポイント SQLi からサーバーフルテイクオーバーに至る 3 段階チェーン; AI エージェントの LLM API キー・顧客データ・外部サービス認証情報が窃取対象](https://thehackernews.com/2026/06/langgraph-flaw-chain-exposes-self.html) — LangChain が構築する AI エージェント基盤として広く採用; 修正: langgraph-checkpoint-sqlite 3.0.1 / langgraph 1.0.10 / langgraph-checkpoint-redis 1.0.2 *(The Hacker News / Check Point Research / CyberSecurityNews)*

---

## セキュリティ関連ニュース

- **[2026-06-12]** [中国系 APT「Velvet Ant」が Operation Highland でエアギャップ企業ネットワークの PAM・OpenSSH を改ざんして約 10 年間潜伏 — Sygnia が公開: PAM ログインモジュールを 9 種の悪意あるバリアントに差し替えバックドアパスワード認証と正規認証情報の盗取を同時実現; OpenSSH にも同様の改ざんでコマンドログ機能を埋め込み; 踏み台はインターネット接続ロードバランサー・スイッチを経由](https://thehackernews.com/2026/06/china-linked-hackers-backdoored-linux.html) — 2016 年まで遡る痕跡。エクスプロイト不要で「信頼済みシステムバイナリの置き換え」のみ使用。通常スキャナーや EDR で検出不可能 *(The Hacker News / Sygnia / BleepingComputer / SC Media)*

- **[2026-06-12]** [「Atomic Arch」キャンペーンが AUR 1,500+ パッケージを Rust インフォスティーラー + eBPF ルートキットで汚染 — 孤立 (orphaned) AUR パッケージのオーナーシップを悪用して PKGBUILD に npm post-install フックを注入; Rust ベース ELF ペイロードが Tor 隠蔽 C2 経由で認証情報・ブラウザデータ・暗号鍵を窃取し、`scales.bpf.c` eBPF ルートキットが PID/ファイル/ソケットを隠蔽して検出を回避; systemd 永続化 + サイドロード暗号マイナーも付随](https://thehackernews.com/2026/06/over-400-arch-linux-aur-packages.html) — 第 2 波 (6/12) は Bun ベースのインストールパスに切り替え。コミュニティ検出ツール: `github.com/lenucksi/aur-malware-check` *(The Hacker News / BleepingComputer / Privacy Guides / HackRead / Sonatype)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-12 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2025-67644 | LangGraph langgraph-checkpoint-sqlite < 3.0.1 (Python, 自己ホスト型 AI エージェント) | CWE-89 / 7.3 | 攻撃者制御のスレッド ID / チェックポイント ID が SQLite `SELECT` クエリに直接連結 → SQL インジェクション → チェックポイントデータ改ざん; 単体では中程度だが CVE-2026-28277 と連鎖で完全 RCE | [commit 29724291 (langgraph-checkpoint-sqlite v3.0.1)](https://github.com/langchain-ai/langgraph/commit/297242913f8ad2143ee3e2f72e67db0911d48e2a) | 2026-06-12 公開 / Check Point Research / LangGraph 以外の SQLite チェックポイント実装 (CrewAI 等) への水平バリアント推奨 |
| CVE-2026-28277 | LangGraph langgraph < 1.0.10 (Python, 全プラットフォーム) | CWE-502 / 6.8 | チェックポイント復元時に msgpack デシリアライザが攻撃者制御バイトストリームを任意 Python オブジェクトとして再構築 → 任意コード実行; CVE-2025-67644 で改ざんされたチェックポイントをトリガーとして連鎖 | [langgraph v1.0.10](https://github.com/langchain-ai/langgraph/releases/tag/v1.0.10) | 2026-06-12 公開 / CVE-2025-67644 との連鎖でフルサーバーテイクオーバー / msgpack の `raw=False` + `allow_invalid_utf8` 設定パターンは他 AI フレームワークにも広く存在 |
| CVE-2026-27022 | LangGraph langgraph-checkpoint-redis < 1.0.2 (Python + Redis Stack, 自己ホスト型) | CWE-943 / 6.5 | 攻撃者制御のスレッド ID が RediSearch クエリ (`@thread_id:{<ID>}`) に無サニタイズで注入 → 他ユーザーのチェックポイントへのアクセス制御バイパス → AI エージェントのセッション横断読み書き | [langgraph-checkpoint-redis v1.0.2](https://github.com/langchain-ai/langgraph-checkpoint-redis/releases/tag/v1.0.2) | 2026-06-12 公開 / Redis Stack を使用する AI エージェント全般に同種バリアント / LangChain の他 Redis ストアへの波及要確認 |
| Sonatype-2026-003775 | AUR (Arch User Repository) パッケージ 1,500+ 件 (Arch Linux, 開発者 PC) | CWE-506 / **8.7** | 攻撃者が orphaned AUR パッケージのオーナーを採用し PKGBUILD の post-install フックに npm 呼び出しを追加 → `atomic-lockfile` npm パッケージが Rust ELF ビルドを取得しインストール → eBPF ルートキット (`getdents64` フック) + インフォスティーラー + Tor C2 が開発者 PC に展開 | [aur.archlinux.org (コミュニティ除染対応中)](https://github.com/lenucksi/aur-malware-check) — (commit 不明 / パッケージ単位の削除・修正) | 2026-06-12 公開 (第 2 波) / CVSS 8.7 / eBPF ルートキットで EDR 回避 / Homebrew・AUR 等 非公式パッケージマネージャの orphaned package 採用プロセスへのバリアントハント推奨 |
| CVE-2026-50645 | Apache CXF < 4.2.2 / < 4.1.7 (Java, SOAP/REST Web サービス) | CWE-400 / Low | 非認証リモート攻撃者がデフォルト上限なしのアタッチメントヘッダーを含む multipart メッセージを送信 → 非制御リソース消費 → サーバー DoS | [Apache CXF 4.2.2 / 4.1.7 (2026-06-12)](https://cxf.apache.org/security-advisories.html) | 2026-06-12 公開 / Low (DoS only) / SOAP API 公開環境に影響 / 上限値を 500 に制限する設定で即時緩和可 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|

> 直近2日間に該当する新規ニュースは確認できませんでした。なお、本日公開の Agentjacking (Claude Code・Cursor 等 AI コーディングエージェント) および LangGraph CVE 連鎖は国内 AI 開発者の環境に直結するため、JPCERT/CC の追加アラートに注意が必要。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 35 ソース (TechCrunch, Bloomberg, CNBC, Fortune, Axios, The Hacker News, BleepingComputer, GBHackers, CyberSecurityNews, Help Net Security, Infosecurity Magazine, Cloud Security Alliance, Check Point Research, Sygnia, Sonatype, Privacy Guides, HackRead, Cyberpress, Decrypt, OECD AI, SC Media, SecurityWeek, Adversa AI, NVD, GitHub Advisory Database, OSV.dev, CVEFeed, threat-modeling.com, sentinelone.com, CISA.gov, eSecurity Planet, nvd.nist.gov, ppln.co, jpcert.or.jp, jvn.jp 他)
- 採用件数: AI=4 / Security=2 / CVE=5 / 国内=0
- 採用件数が目安 (各 8〜12 件) を下回った理由:
  - 採用窓 (2026-06-12〜14) は June Patch Tuesday (6/9) 翌週の土日〜週頭に当たり、主要 AI ラボ・ベンダーからの新規大型発表が少ない端境期
  - Patch Tuesday 収録の主要 CVE・Nightmare Eclipse 連続ゼロデイ・ShinyHunters PeopleSoft 等は 06-09 〜 06-13 digest に収録済み (excluded_set)
  - Chrome 149.0.7827.115 Critical 4 件 / Ivanti Sentry KEV / Oracle PeopleSoft KEV追加 / AudiA6 Europol 閉鎖 / OnyxC2 等は直近 digest 収録済み
- 除外理由内訳:
  - 古すぎ (< 2026-06-12 JST):
    - Tchap フランス政府メッセージアプリ侵害 (ANSSI 検知 6/7, 各紙報道 6/9-10)
    - DeepSeek V4-Pro/Flash (2026-04-24 リリース)
    - Gemini Omni (Google I/O 2026, 5月末)
    - GPT-5.4 (2026-03-05 リリース)
    - SymJack Adversa AI (2026-05 下旬開示, SecurityWeek 続報日が明確でないため除外)
    - Google GitHub CVE-2026-3854 (2026-03-04 発見)
    - 50+ Malicious Chrome Extensions "Gameograf" (2026-06-03)
    - 3 百万件 日本顧客データ窃取ダークウェブ掲載 (2026-06-02)
    - Qilin 18 victims 製造・エネルギー 24 時間 (2026-06-11)
    - Velvet Ant 初報 Sygnia (2026-06-11); THN/BleepingComputer の June 12 報道日を採用
    - CISA BOD 26-04 (2026-06-10)
    - Trump AI EO "Promoting Advanced AI Innovation and Security" (2026-06-02)
    - Mitsubishi Electric Realtek WiFi heap overflow JVN (2026-06-11)
    - Atomic Arch 第 1 波 Sonatype (2026-06-11); 第 2 波 + 複数媒体 June 12 報道を採用
  - 重複 (excluded_set 直近 7 日):
    - CVE-2026-12007/12008/12009/12010 (Chrome 149.0.7827.115 Critical 4 件, 06-13 digest)
    - GreatXML / CVE-2026-0273 (06-13 digest)
    - CVE-2026-10520/10523 (Ivanti Sentry, 06-12 digest)
    - CVE-2026-35273 (Oracle PeopleSoft, 06-12 digest)
    - CVE-2026-5027 (Langflow, 06-12 digest)
    - CVE-2026-11645 (Chrome V8 KEV, 06-12 digest)
    - CVE-2026-42271 (LiteLLM, 06-11 digest)
    - CVE-2026-45657/45447/47291/47911/48710 (06-11 digest)
    - RoguePlanet (06-11 digest)
    - Claude Fable 5 ジェイルブレーク (06-12 digest)
    - OpenAI Ona 買収 (06-13 digest)
    - ニューヨーク州 AI 7 法案 (06-13 digest)
    - Brutecat Google VRP $50 万超 (06-13 digest)
    - Europol AudiA6 / OnyxC2 / DragonForce/TheGentlemen / Chrome 149 / Ivanti野外悪用 / ShinyHunters PeopleSoft (06-12 〜 06-13 digest)
    - 九州電力 SSD 紛失 (06-13 digest)
    - Palo Alto CVE-2026-0257 GlobalProtect (05 digest)
    - Nginx UI CVE-2026-27944 (2026-03-05 NVD 掲載)
  - 日付不明/確認不可:
    - White House "Promoting Advanced AI Innovation and Security" EO の June 14 版有無 (検索結果が June 2 EO の続報と判断し除外)
    - ppln.co「2nd Week of June 2026 日本向けサイバー脅威」(HTTP 403)
    - JPCERT/CC June 12-14 個別アラート (HTTP 403; 公式サイトへの直接アクセス不可)
- 取得失敗ソース (HTTP 403): anthropic.com/news/fable-mythos-access / thehackernews.com 個別記事 / bloomberg.com 個別記事 / cyberpress.org 個別記事 / adversa.ai 個別記事 / research.checkpoint.com / esecurityplanet.com / trustinfinitech.com / nvd.nist.gov 検索 API / ppln.co / jpcert.or.jp / jvn.jp — WebSearch スニペット・複数独立媒体・公開日確認済み URL パターンで内容・日付を補完

</details>
