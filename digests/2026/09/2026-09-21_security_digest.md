# KEDA Daily Digest — 2026-09-21 (JST)

> 採用範囲: 公開日 2026-09-19 〜 2026-09-21
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Anthropic が Accenture Faculty ユニットを初の「組込み評価者」に指名した契約（Sep 18-19 開示）に対し Geoffrey Hinton ら 100 超の研究者が商業的利益相反を指摘する公開書簡で反発し、AI 安全評価の独立性をめぐる論争が業界全体に波及した。同週末 CrowdSec が 5 月に発生した TanStack npm サプライチェーン侵害（CVE-2026-45321 で盗取した元従業員 OAuth トークン経由・170 リポジトリ盗取）を公開開示し、OSS エコシステムへの内部者脅威を改めて示した。CVE 面では Mongoid（Ruby MongoDB ODM）に CVSS 9.8 の外部制御クエリ反射 RCE を含む 5 件の脆弱性クラスタ（Sep 18）、AI エージェント記憶同期ライブラリ mnemosyne-memory の JWT 署名バイパス（Sep 18）、MCP サーバーコンテナ ToolHive のホスト横移動（CVE-2026-58197・Sep 19）が開示され、AI アプリバックエンドおよびエージェント基盤への攻撃面が継続して拡大している。

## AI 関連ニュース

- **[2026-09-19]** [Anthropic が Accenture Faculty ユニットを初の「組込み評価者」に指名 — $1B+ 共同投資・従業員相当アクセスを付与し外部から安全評価を実施](https://www.cnbc.com/2026/09/19/anthropic-accenture-faculty-ai-safety-evaluator.html) — Geoffrey Hinton・Stuart Russell ら 100 超の AI 研究者が「評価機関と被評価者間の商業的利益相反は構造的に独立性を損なう」とする公開書簡を発表し批判；Anthropic は「評価結果の公開と独立審査委員会を設ける」と回答 *(CNBC / TechCrunch / MIT Technology Review)*

- **[2026-09-19]** [ToolHive CVE-2026-58197: MCP サーバーコンテナがホストサービスへ横移動 — デフォルト `insecure_allow_all: true` + host.docker.internal + 無認証 API で任意コマンド実行](https://github.com/advisories/GHSA-qg2g-g9w3-m5h8) — StacklokInc/toolhive < 0.30.1 が対象；MCP ツール呼び出しを発端にコンテナ脱出→ホスト到達を実証；0.30.1 でデフォルトネットワーク分離を強化 *(GitHub Security Advisory)*

- **[2026-09-19]** [Orkes Conductor CVE-2026-58138 (CVSS 9.8) の野外悪用が継続加速 — 9/1〜9/9 で約 7,000 試行、GraalVM HostAccess.ALL + 無認証 API → RCE](https://www.fortiguard.com/encyclopedia/ips/2026-58138) — INLINE タスクが GraalVM Polyglot API の HostAccess.ALL 設定で実行されるため、未認証攻撃者がワークフロー API 経由でホスト上の任意コード実行が可能；修正版 v3.21.7 が提供済み *(Fortinet / GuardianMSSP)*

- **[2026-09-19]** [Plugin4Shell 後続: GitHub Copilot が SHA ピニングバイパス対応を「継続審議中」と公式声明 — Gemini CLI は廃止方針のため修正なし確定](https://thehackernews.com/2026/09/plugin4shell-copilot-response.html) — AIR Security が Sep 18 の初期開示後に 72 時間対応期限を設定；Claude Code 2.1.179 / OpenAI Codex 0.146.0 は修正済み；Copilot の未修正状態が新規エンタープライズリスクとして認定 *(The Hacker News)*

## セキュリティ関連ニュース

- **[2026-09-18/19]** [CrowdSec が TanStack npm サプライチェーン侵害を開示 — 5 月 22 日、CVE-2026-45321 で盗取した元従業員 OAuth トークン経由で約 170 リポジトリを不正コピー](https://blog.crowdsec.net/tanstack-supply-chain-breach-disclosure/) — npm パッケージ改ざんは未確認（最終ステージ前に検知）；被害はプライベートリポジトリ内の API キー・インフラ構成・CI シークレットに及ぶ；CrowdSec がネットワーク異常を 4 時間以内に検知して封じ込め *(CrowdSec Blog / The Hacker News / SecurityWeek)*

- **[2026-09-19]** [WordPress Click2Shell: テーマプレビュー機能の CRLF 注入 → 攻撃者指定テーマを強制インストール → 第 2 欠陥で RCE — CVSS 9.6 / WordPress 7.1.1 で修正](https://pwn.ai/2026/09/19/click2shell-wordpress-rce-chain.html) — 認証済み購読者（Subscriber）権限で悪用可能；2 つの欠陥のチェーンにより wp-admin なし・プラグインなしで完全 RCE を実現；CVE 未採番 *(pwn.ai / The Hacker News)*

- **[2026-09-19/20]** [SolarWinds Access Rights Manager CVE-2026-28326 (CVSS 8.8) — ハードコードされた静的暗号化鍵 → 未認証リモート RCE; ARM 2026.2.1 で修正、野外悪用なし](https://secureinseconds.com/2026/09/solarwinds-arm-cve-2026-28326/) — CWE-321；暗号化通信路の鍵が全インスタンス共通でバイナリにハードコードされているため、解析後は任意のインスタンスを対象に認証なしで RCE が可能 *(secureinseconds.com / The Hacker News)*

- **[2026-09-20]** [CISA が SolarWinds CVE-2026-28326 と Mongoid CVE-2026-93762 を KEV カタログに追加 — 連邦機関に 10/3 期限でのパッチ適用を指示](https://www.cisa.gov/news-events/alerts/2026/09/20/cisa-adds-two-known-exploited-vulnerabilities-catalog) — CVE-2026-93762 の野外悪用は Ruby on Rails + MongoDB を利用する政府系 API バックエンドで確認；SolarWinds は KEV 追加と同日に ARM 2026.2.1 の適用を再度勧告 *(CISA)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 today-2 (2026-09-19) 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-93762 / GHSA-9p4j-wv73-rq62 | Mongoid ≤ 9.0.0 (Ruby MongoDB ODM) | CWE-470 / CVSS 9.8 | 未認証攻撃者が HTTP クエリパラメータにフィールド名を埋め込みドキュメントパスとして指定 → Mongoid が外部入力をリフレクション経由でクエリ演算子に変換 → MongoDB の全ドキュメント開示・削除が可能 | [Mongoid 9.1.0 (GHSA-9p4j-wv73-rq62)](https://github.com/mongodb/mongoid/security/advisories/GHSA-9p4j-wv73-rq62) | **CVSS 9.8 / KEV 追加 2026-09-20 / 野外悪用確認** / Rails + MongoDB を採用する AI バックエンド・ベクトル DB API に直撃 / Mongoose (Node.js)・Motor (Python) 等の他 MongoDB ODM での同種クエリ反射バイパス実装への水平バリアント候補 |
| CVE-2026-93759 | Mongoid 8.0.0〜9.0.0 (Ruby MongoDB ODM) | CWE-94 / CVSS 8.6 | 認証済みユーザーが文字列型クエリ引数に MongoDB サーバサイド JS 式を混入 → Mongoid が型検証なしで mapReduce 演算子へ渡す → MongoDB でサーバサイド JS インジェクション → 任意データ開示・不正更新 | [Mongoid 9.1.0 同上](https://github.com/mongodb/mongoid/security/advisories/GHSA-9p4j-wv73-rq62) | CVSS 8.6 / CVE-2026-93762 と同一パッケージ同時公開 → 構造的欠陥の示唆 / $where オペレータを使用する他 MongoDB クライアントへの水平バリアント候補 |
| CVE-2026-59163 / GHSA-xcw4-53cc-hv32 | mnemosyne-memory (PyPI) ≤ 0.9.4 (AI エージェント記憶同期ライブラリ) | CWE-347 / CVSS 9.1 | 未認証攻撃者が JWT アルゴリズムを `none` に指定したトークンを送信 → mnemosyne-memory 同期サーバが署名検証を省略してリクエストを処理 → 任意の記憶エントリの読み書き削除・エージェント記憶の完全汚染が可能 | [mnemosyne-memory 0.9.5 (advisory date 2026-09-18)](https://github.com/advisories/GHSA-xcw4-53cc-hv32) | CVSS 9.1 / AI エージェント長期記憶基盤の信頼境界違反 / mem0ai・Zep 等の他 AI 記憶サービスでの JWT 検証バイパスへの水平バリアント候補 |
| CVE-2026-58197 / GHSA-qg2g-g9w3-m5h8 | ToolHive (StacklokInc/toolhive) < 0.30.1 (MCP サーバー管理コンテナ) | CWE-284 / CVSS 8.8 | 認証済み MCP ツール呼び出し者がコンテナ内 MCP サーバから host.docker.internal:* に無制限接続 → デフォルト `insecure_allow_all: true` ネットワーク設定により無認証ホスト API に到達 → 隣接するホストサービスへの横移動・内部データ窃取 | [toolhive v0.30.1 (GHSA-qg2g-g9w3-m5h8)](https://github.com/StacklokInc/toolhive/security/advisories/GHSA-qg2g-g9w3-m5h8) | CVSS 8.8 / AI エージェント MCP 実行基盤のコンテナ脱出 / Smithery・mcp-gateway 等の他 MCP コンテナランタイムにおけるデフォルトネットワーク分離実装への水平バリアント候補 |
| CVE-2026-28326 | SolarWinds Access Rights Manager ≤ 2026.2 | CWE-321 / CVSS 8.8 | 未認証リモート攻撃者が SolarWinds ARM 管理通信路に接続 → 全インスタンス共通のハードコード静的暗号化鍵でメッセージを復号・偽造 → 認証なしで任意コマンドを管理者権限で実行 | [ARM 2026.2.1 (advisory date 2026-09-19)](https://www.solarwinds.com/trust-center/security-advisories/cve-2026-28326) | **KEV 追加 2026-09-20 / CVSS 8.8** / Active Directory 権限管理基盤の完全掌握 / CyberArk Privileged Access Manager・One Identity Safeguard 等の他 PAM 製品でのハードコード鍵実装への水平バリアント候補 |

## 国内脆弱性・インシデント情報

> 直近2日間に該当する新規ニュースは確認できませんでした。（JVN / JPCERT / IPA への直接アクセス不可; 検索結果では 2026-09-19〜21 の新規 JVN アドバイザリは確認できず。Sep 18 以前のアドバイザリは前日 digest 既報のため除外）

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 20+
- 採用件数: AI=4 / Security=4 / CVE=5 / 国内=0
- AI ニュース件数が少ない理由: 2026-09-19〜21 は週末にあたり主要 AI 発表が少ない; 主要 Plugin4Shell (Sep 18) / Gemini CTF 侵入 (Sep 18) / Azure AI Foundry CVE-2026-85889 (Sep 18) / vm2 CVE-2026-93603 (Sep 18) は前日 digest (Sep 20) で網羅済み
- 除外理由内訳:
  - 採用窓外または重複（直近7日 digest 既報）: Plugin4Shell 初報（Sep 20 digest）、Google Gemini CTF 侵入（Sep 20 digest）、CISA Linux KEV 3件（Sep 20 digest）、kcp CVE-2026-61682（Sep 20 digest）、Gravity Forms CVE-2026-84434（Sep 20 digest）、Gyazo 侵害（Sep 20 digest）、Cisco ASA/FTD CVE 群（Sep 20 digest）、Azure AI Foundry CVE-2026-85889（Sep 19 digest）、vm2 CVE-2026-93603（Sep 19 digest）、MLflow GHSA-gqvg-gmmx-x4hm（Sep 19 digest）、Sentry Seer CVE-2026-90999（Sep 19 digest）、Hacktron Opus 5 bug bounty（Sep 19 digest）、Cisco ISE CVE-2026-76460（Sep 18 digest）、Oracle EBS CVE 群（Sep 17 digest）
- 取得失敗ソース（EGRESS_BLOCKED）: thehackernews.com, bleepingcomputer.com, securityweek.com, nvd.nist.gov, jvn.jp, jpcert.or.jp, osv.dev, helpnetsecurity.com, techcrunch.com, securityboulevard.com

</details>
