# KEDA Daily Digest — 2026-06-15 (JST)

> 採用範囲: 公開日 2026-06-13 〜 2026-06-15
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

週末の静かなニュースサイクルの中でも AI エージェントインフラと OT/IoT 通信プロトコルへの新規脆弱性が注目を集めた。特に Google MCP Toolbox for Databases に CVSS 9.4 の DNS リバインディング脆弱性 (CVE-2026-11624) が GHSA 公開され、AI エージェントのデータベースアクセス経路が新たな攻撃対象であることが改めて示された。また watchTowr が Splunk Enterprise の PostgreSQL サイドカーサービスを悪用した無認証 RCE チェーン (CVE-2026-20253、Splunk 社 advisory は 6/10) の詳細技術解析を 6/13 に公開し、SIEM 自体が攻撃起点になるリスクが浮き彫りになった。同日 GHSA には組み込み Modbus/MQTT/UDS プロトコルライブラリの High CVE 3 件も集中公開されており、OT・車載 ECU 環境への余波が懸念される。

---

## AI 関連ニュース

- **[2026-06-13]** [CVE-2026-11624 — Google MCP Toolbox for Databases が DNS リバインディング攻撃に脆弱 (CVSS 9.4)](https://cybersecuritynews.com/mcp-toolbox-vulnerability/) — Google の MCP サーバー実装が Origin ヘッダー検証なしで稼働していたため、悪意ある Web サイトが DNS リバインディングで ローカル MCP サーバーに不正リクエストを送り、接続 DB へコマンドレベルアクセスが可能; v0.25.0 で `--allowed-hosts` / `--allowed-origins` フラグ追加により修正済み *(CybersecurityNews / Cyberpress)*

- **[2026-06-13]** [BugHunter — Claude Code + 無償 AI プロバイダーで全フェーズを自動化するバグバウンティ OSS ツールキット公開](https://cybersecuritynews.com/bughunter-bug-bounty-toolkit/) — Shuvon Md Shariar Shanaz が開発; Anthropic Claude Code を主エンジンに Ollama / Groq / DeepSeek への自動フォールバックを実装し、サブドメイン列挙・ライブホスト発見・Web2 (20+ クラス) / Web3 (10 クラス) 脆弱性テスト・7-Question Gate 検証・HackerOne / Bugcrowd 向けレポート生成をシングルコマンドで実行; Claude Code 有料サブスクなしで利用可能になったことで AI 支援型バグハンティングの裾野が拡大 *(CybersecurityNews)*

> 直近2日間に採用できた新規 AI ニュースは上記 2 件に留まりました。June Patch Tuesday (6/9) 翌週末の端境期に当たり、主要 AI ラボからの大型モデルリリース・政策発表は確認されませんでした。

---

## セキュリティ関連ニュース

- **[2026-06-13]** [watchTowr が Splunk Enterprise CVE-2026-20253 の Pre-Auth RCE チェーンを詳細技術解析として公開 — PostgreSQL サイドカーサービスの `/v1/postgres/recovery/backup` / `/v1/postgres/recovery/restore` エンドポイントに一切の認証なし; Splunk メイン Web (port 8000) がこれらを内部 port 5435 へプロキシするため外部から到達可能; backup エンドポイントが攻撃者制御パラメータを pg_dump に直接渡しファイル書き込み → SIEM 内 Python スクリプト書き換えで任意コード実行](https://labs.watchtowr.com/why-use-app-level-auth-when-every-database-has-auth-splunk-enterprise-cve-2026-20253-pre-auth-rce/) — Splunk Enterprise 10 系が稼働する AWS 環境はデフォルトでサイドカーが有効で即時 RCE リスク; 修正版 (10.4.0 / 10.2.4 / 10.0.7 / 9.4.12 / 9.3.13 以上) への升级が急務; CVE 公開 (6/10) からわずか 3 日で詳細 PoC 手法解説が登場 *(watchTowr Labs / THN)*

- **[2026-06-14]** [組み込み OT/IoT プロトコルライブラリ 3 件に High CVE が集中公開 — 自動車・産業 IoT に影響: nanoMODBUS (Modbus/TCP サーバー) off-by-one OOB 書き込み (CVE-2026-54410)、MQTT-C クライアントの整数アンダーフロー → ヒープ OOB 読み取り (CVE-2026-54412)、iso14229 UDS サーバー SecurityAccess ハンドラの整数アンダーフロー → OOB 読み取り (CVE-2026-54413) — いずれも修正パッチ未公開、CAN/OBD-II/Modbus TCP 経路で無認証リモートからのクラッシュ・情報漏洩が可能](https://github.com/advisories) — 同パターン (長さフィールド未検証 → 符号なし演算でアンダーフロー) が複数の組み込みプロトコル実装に横展開しており、同仕様の独立実装 (OpenMODBUS / EMQ X SDK 等) へのバリアントハント推奨 *(GitHub Advisory Database)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-13 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-11624 / GHSA-76g7-m3xw-x9gr | Google MCP Toolbox for Databases < v0.25.0 (Python/Go、AI エージェント DB 接続基盤) | CWE-346 / **9.4** (CVSS 4.0) | ローカル MCP HTTP サーバーが Origin ヘッダーを検証しないため、悪意ある Web サイトが DNS リバインディングで同一ポートにブラウザ越しリクエスト → 接続 DB への任意クエリ実行・データ窃取 | [v0.25.0 (--allowed-hosts 追加 / PR #2254)](https://github.com/googleapis/mcp-toolbox/releases) | 2026-06-13 公開 / AI エージェントのデータベースアクセス基盤 / MCP DNS リバインディングパターンは Go SDK (CVE-2026-34742) / Java SDK (CVE-2026-35568) / Docker MCP Gateway (GHSA-46gc-mwh4-cc5r) にも波及済みの横断的バグクラス |
| CVE-2026-54410 / GHSA-6f53-f2m4-6j2h | nanoMODBUS ≤ v1.23.0 (C、Modbus/TCP 組み込みサーバー) | CWE-193 / CWE-787 / **7.8** | 無認証リモート攻撃者が Length=255 の細工 MBAP フレームを送信 → `recv_msg_header()` の off-by-one で 260 byte 受信バッファ直後 1 byte を上書き → 隣接バッファインデックスフィールド破損で DoS・メモリ情報漏洩・FC16 ハンドラ経路で任意レジスタ書き込み | 修正パッチ未公開 (commit 不明) | 2026-06-14 公開 / 未パッチ / ベアメタル/RTOS 環境で MPU なしの場合 OOB 書き込みに拡大 / OpenMODBUS・libmodbus 等の Modbus/TCP 受信長処理へのバリアントハント推奨 |
| CVE-2026-54412 / GHSA-28cw-rpqc-wqqj | LiamBindle MQTT-C ≤ 1.1.6 (C、MQTT クライアントライブラリ) | CWE-125 / CWE-191 / **7.8** | 攻撃者制御 MQTT ブローカーが topic_name_size=0xFFFF の PUBLISH パケットを送信 → `mqtt_unpack_publish_response()` が残りバイト数未検証のまま 65535 byte 先へポインタ移動 (ヒープ OOB 読み取り) → application_message_size が符号なし演算で約 2^32 に → memmove() でクラッシュ | 修正パッチ未公開 (commit 不明) | 2026-06-14 公開 / 未パッチ / 同パターン (length field 未検証 + unsigned underflow) は Eclipse Paho MQTT SDK / emqtt-bench 等 MQTT クライアント実装全般へのバリアントハント推奨 |
| CVE-2026-54413 / GHSA-36r7-c6f4-gj9g | driftregion iso14229 ≤ 0.9.0 (C、UDS / ISO 14229 診断サーバー) | CWE-125 / CWE-191 / **7.8** | `Handle_0x27_SecurityAccess()` が 1 byte リクエストでバッファ長を検証せずサブファンクションを読み取り → 符号なし演算で長さ 65535 に整数アンダーフロー → コールバック関数が 4 KB 受信バッファを超えてデータを反復・コピーし OOB 読み取り / クラッシュ; CAN/OBD-II/ISO-TP/DoIP 経路・デフォルトセッション・無認証で到達可能 | 修正パッチ未公開 (commit 不明) | 2026-06-14 公開 / 未パッチ / 車載 ECU・産業コントローラーの UDS サーバー実装 (automotive-package UDSonCAN 等) への水平バリアント / 同 0x27 ハンドラパターンは複数ベンダー OEM 実装に存在 |
| CVE-2026-54411 / GHSA-56gg-22rq-q53x | Linux-PAM ≤ 1.7.2 pam_userdb モジュール (Linux、ローカル認証) | CWE-208 / **4.0** (CVSS 4.0) | `crypt=none` (または未知 crypt 値 / crypt 引数なし) 設定で平文パスワード比較パスに入ると、応答タイミング差を繰り返し計測することで標的アカウントの平文パスワードを復元可能; 認証失敗遅延がないサービスを経由した場合に攻撃複雑度が低下 | 修正パッチ未公開 (commit 不明) | 2026-06-14 公開 / 中程度 (CVSS 4.0) / `crypt=none` という誤設定が前提 / 他認証ライブラリ (OpenLDAP slapd userPassword 等) の平文比較パスへのバリアントハント推奨 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|

> 直近2日間に該当する新規ニュースは確認できませんでした。JVN/JPCERT/IPA の 2026-06-13〜15 新規 advisory は HTTP 403 により直接取得不可; WebSearch からも新規国内インシデントは確認されませんでした。なお CVE-2026-11624 (MCP Toolbox DNS リバインディング) および CVE-2026-54413 (iso14229 UDS) は国内自動車/産業機器メーカーのサプライチェーンにも関連するため、JPCERT/CC の追加アラートに注意が必要。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 30 ソース (CybersecurityNews, GBHackers, CyberPress, The Hacker News, watchTowr Labs, SecurityWeek, Orca Security, GitHub Advisory Database (GHSA), OSV.dev, CVEFeed, BleepingComputer, Help Net Security, Infosecurity Magazine, Tenable, Threat-Modeling.com, CISA KEV Catalog, vulnerability.circl.lu, OffSeq.com, JVN, JPCERT/CC, IPA, ScanNetSecurity, adversa.ai, llm-stats.com, pheonix.security, WebSearch aggregates 他)
- 採用件数: AI=2 / Security=2 / CVE=5 / 国内=0
- 採用件数が目安 (各 8〜12 件) を下回った理由:
  - 採用窓 (2026-06-13〜15) は June Patch Tuesday (6/9) 翌週末〜週明けに当たり、主要 AI ラボ・ベンダーからの新規大型発表が少ない端境期
  - Patch Tuesday 収録 CVE (Windows Kernel / HTTP.sys / Hyper-V / SAP / Veeam 等) / Chrome 149.0.7827.115 / RoguePlanet (GreatXML) / LangGraph 3 CVE 連鎖 / Agentjacking / Velvet Ant / Atomic Arch / Anthropic 輸出規制停止 等は 06-12〜06-14 各 digest 収録済み (excluded_set)
  - Splunk CVE-2026-20253 の Splunk advisory 公開日は 6/10 (採用窓外) のため CVE テーブルに掲載せず; watchTowr 技術解析 (6/13) を security news として採用
- 除外理由内訳:
  - 古すぎ (< 2026-06-13 JST):
    - INTERPOL Sniper Dz 解体 Operation Ramz (THN 6/12)
    - OpenClaw AI Agent "New Attacks" vCard/Varonis Pinchy (THN 6/11)
    - Unit 42 Screening Serpens Iran APT 報告 (6/11)
    - Google DeepMind 多エージェント AI 安全研究 $10M ファンド (6/11)
    - Cisco SD-WAN CVE-2026-20182 (Splunk advisory 5/14)
    - SolarWinds Serv-U CVE-2026-28318 KEV (6/5 KEV 追加)
    - Android June 2026 Update CVE-2025-48595 (bulletin 6/3)
    - EU Code of Practice on AI コンテンツ (6/10)
    - UpdraftPlus CVE-2026-10795 (6/11)
    - OX Security MCP supply chain advisory (4/15)
    - CVE-2026-34742 Go MCP SDK DNS rebinding (4〜5 月)
    - CVE-2026-35568 Java MCP SDK DNS rebinding (4〜5 月)
    - NSA MCP security guidance (5/20)
    - Splunk CVE-2026-20253 Splunk advisory (6/10)
    - WWDC 2026 Apple Intelligence (6/9)
    - GitHub CVE-2026-3854 RCE (3/4 発見・4 月後半報道)
    - OpenAI Safety Fellowship 発表 (9 月開始、現時点で未採用)
    - BugHunter CVE MCP Server (4/30)
    - JINX-0164 / AUDIOFIX / MiniRAT threat actor (5 月下旬)
  - 重複 (excluded_set 直近 7 日):
    - CVE-2026-10520/10523 (Ivanti Sentry) — 6/12 digest, KEV 締切 6/14 は新規項目でなく期限管理情報
    - CVE-2026-35273 (Oracle PeopleSoft ShinyHunters) — 6/12〜6/13 digest, KEV 締切 6/15
    - CVE-2026-50751 (Check Point VPN / Qilin) — 6/11〜6/13 digest
    - CVE-2026-12007〜12010 (Chrome 149.0.7827.115 Critical 4 件) — 6/13 digest
    - CVE-2026-0273 (Palo Alto PAN-OS CLI injection) — 6/13 digest
    - GreatXML (Windows BitLocker / WinRE bypass) — 6/13 digest
    - OnyxC2 MaaS — 6/13 digest
    - DragonForce / TheGentlemen ランサムウェア — 6/13 digest
    - LangGraph CVE-2025-67644 / CVE-2026-28277 / CVE-2026-27022 — 6/14 digest
    - Agentjacking / Sentry MCP injection — 6/14 digest
    - Velvet Ant PAM/OpenSSH backd — 6/14 digest
    - Atomic Arch AUR supply chain — 6/14 digest
    - Anthropic Fable 5 輸出規制停止 — 6/14 digest
    - Google Gemini / Outsider Enterprise 訴訟 — 6/14 digest
    - NY州 AI 7 法案 — 6/13 digest
    - Brutecat Google VRP — 6/13 digest
    - 九州電力 SSD 紛失 — 6/13 digest
  - 日付不明/確認不可:
    - CISA KEV 6/13〜15 新規追加 (cisa.gov HTTP 403)
    - JVN 6/13〜15 新規 advisory (jvn.jp HTTP 403)
    - JPCERT/CC 6/13〜15 アラート (jpcert.or.jp HTTP 403)
    - Nightmare Eclipse "bone shattering" drop (6/14 予告と報道あったが実際は 7/14 予定; 6/14 時点での新規公開なし)
- 取得失敗ソース (HTTP 403): thehackernews.com 個別記事 / bleepingcomputer.com / securityweek.com / darkreading.com / unit42.paloaltonetworks.com / labs.watchtowr.com / radar.offseq.com / vulnerability.circl.lu / cvefeed.io / osv.dev / cisa.gov/kev / jpcert.or.jp / jvn.jp / cybersecurity-review.com — WebSearch スニペット・複数独立媒体・GHSA fetch (一部成功) で内容・日付を補完

</details>
