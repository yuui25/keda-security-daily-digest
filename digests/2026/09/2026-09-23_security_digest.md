# KEDA Daily Digest — 2026-09-23 (JST)

> 採用範囲: 公開日 2026-09-21 〜 2026-09-23
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Anthropic が Claude Opus 5.5（フラグシップ・エージェント向け、Fable 級性能を約 40% 低コストで提供）を Sep 22 に Amazon Bedrock 等主要プラットフォームでリリースし、xAI も Grok 4.7（2.1 兆パラメータ・同価格）を Sep 21 に投入するなど AI フロンティア競争が継続加速した。セキュリティ面では ShinyHunters が Oracle PeopleSoft の未公開ゼロデイ経由で FBI を侵害したと主張（FBI 未確認・2〜3TB 窃取主張）し、中国語話者の脅威アクターが Zyxel GS1900 スイッチ 996 台を 48 か国で侵害（CISA KEV Sep 21 追加）、北朝鮮 WaterPlum が偽求人でIT専門職 30,000 台超を感染させた事案に米日豪独が合同警告（Sep 18 advisory・Sep 21 主要報道）を発した。CVE 面では Erlang/OTP TLS 1.3 のサーバー証明書検証バイパス（CVE-2026-89422, CVSS 9.3, Sep 22 修正）、Google Chrome の重大 2 件（CVSS 9.6 ×2）、Netcore NBR200V2 ルーターの CVSS 10.0 コマンドインジェクション（パッチなし）、Apache Airflow のベアラートークン失効不備（CVSS 9.1）など、広範なスタックへの攻撃面拡大が続いた。

## AI 関連ニュース

- **[2026-09-22]** [Claude Opus 5.5 リリース — Anthropic のフラグシップ・エージェントモデルが Amazon Bedrock / Azure / Vertex / Claude Platform に展開; コンテキスト 1M トークン・最大出力 128K・知識カットオフ 2026年6月、価格 $4/$20 per M input/output](https://aws.amazon.com/blogs/machine-learning/introducing-claude-opus-5-on-aws-anthropics-most-capable-opus-model/) — Claude Fable 5.1 同等性能を約 40% 低コストで提供; 長時間エージェントタスク・コーディング・難度の高い推論向けに最適化 *(Anthropic / AWS / llm-stats.com)*

- **[2026-09-21]** [xAI、Grok 4.7 リリース — 2.1 兆パラメータ（4.6 比 40% 増）・500K コンテキスト・CursorBench 4.0 46.3% / DeepSWE 71.0%・価格は 4.6 と同一 ($2/$6 per M tokens)](https://tech.yahoo.com/ai/gemini/articles/xai-launches-grok-4-7-171603280.html) — 大規模 RL ラン・SpaceX Starlink 衛星テレメトリ等の補完訓練データを採用; 同日 Cursor / Grok Build / xAI API で提供開始 *(Yahoo Tech / llm-stats.com / kingy.ai)*

- **[2026-09-21]** [Aikido Security、Altar-1 — オープンウェイト・サイバーセキュリティ特化 AI をオンプレミス向けにリリース; 504B パラメータ (GLM-5.3 expert pruning)・W4A16 量子化 328 GB・vLLM on 4× H200 で稼働](https://www.aikido.dev/blog/aikido-altar-open-weight-ai-sovereign-security) — 内部テストで 32 件の脆弱性の 23 件を検出 (recall 60.4%); データ秘匿が必要な医療・金融・OT 環境でのペネトレーションテスト自動化を想定 *(Aikido Security / Silicon UK / CybersecurityNews)*

- **[2026-09-22]** [Baseten Base Labs、HuggingFace・Goodfire と連携してオープンウェイトモデル安全基準・評価ツールを発表 — データ残留規制下での推論サービスに対し評価・モニタリング標準化を推進](https://handyai.substack.com/p/model-drop-claude-opus-55) — オープンウェイトモデルの無制御デプロイリスクに対する業界標準化の動き; ポリシー遵守可能な評価スタックを提供予定 *(Baseten / Handy AI)*

- **[2026-09-22]** [ChatGPT、Microsoft Word プラグイン統合を拡張展開 — Word での下書き・要約・修正・フォーマットに AI アシスタントを提供、OpenAI プラグインアカウント接続サポートも追加](https://releasebot.io/updates/openai) — Microsoft と OpenAI の統合深化; エンタープライズユーザーへのロールアウト開始 *(OpenAI / Releasebot.io)*

- **[2026-09-22]** [OpenAI Sora API、9 月 24 日をもって廃止確定 — Sora web/app は 4 月 26 日に廃止済み; 後継モデルは OpenAI の廃止ページで空欄のまま、移行先は各開発者の判断に委ねられる](https://www.newsbytesapp.com/news/science/sora-api-shuts-down-september-24-what-users-should-do/story) — Sora 2 API は別 ID で継続提供; ビデオ生成ワークフローの API 統合先変更が即時必要 *(OpenAI Help Center / NewsBytesApp / Leaxor)*

## セキュリティ関連ニュース

- **[2026-09-22]** [ShinyHunters が Oracle PeopleSoft 未公開ゼロデイ経由で FBI を侵害と主張 — apply.fbijobs.gov の /PSEMHUB/ パスから RCE、2〜3TB のFBI 職員・元職員・応募者 PII/PHI を窃取と主張; 5,000 件サンプル提示済み](https://www.usnews.com/news/top-news/articles/2026-09-22/shinyhunters-hackers-say-they-breached-federal-bureau-of-investigation-no-immediate-comment-from-fbi) — FBI・Oracle・AWS はいずれも Sep 22 時点で未確認; 同グループは FBI が May 2026 に公開した自グループ手口警告への報復と主張; 先行する PeopleSoft CVE-2026-35273（Jun 2026・100 組織被害）の延長線上 *(US News / TechCrunch / CyberInsider / 404media)*

- **[2026-09-21]** [CISA、Zyxel CVE-2026-7273 を KEV 追加・9 月 24 日修正期限 — 中国語話者アクターが GS1900 スイッチ 996 台（48 か国）を 8 月以降侵害; 設定・認証情報・ルートハッシュを窃取](https://www.cisa.gov/news-events/alerts/2026/09/21/cisa-adds-one-known-exploited-vulnerability-catalog) — 未認証ローカルネットワーク HTTP リクエストで OS コマンド実行可能 (CVSS 8.8); 元 advisory Jun 2026 (FW 2.90(XXXX.1)C0 以前); 管理インターフェースの WAN 露出廃止が最優先 *(CISA / Help Net Security / SecurityWeek)*

- **[2026-09-22]** [Veeam Agent Windows CVE-2026-32996 の野外悪用が継続・Arctic Wolf が緊急警告 — PoC 公開 (Sep 14) 後に後侵入チェーンへの組み込みが加速; gRPC 名前付きパイプのセッション UID ミスマッチで NT AUTHORITY\SYSTEM 権限奪取](https://arcticwolf.com/resources/blog/update-active-exploitation-cve-2026-32996-of-veeam-agent/) — CVSS 7.3; 共有ワークステーション・管理者端末が最優先; Veeam Backup & Replication 13.0.2.29 以降へのアップグレードで Veeam Agent も 13.0.3.1220 に更新 *(Arctic Wolf / CybersecurityNews / SecurityAffairs)*

- **[2026-09-21]** [米・日・豪・独が WaterPlum (Contagious Interview) 合同警告 — 北朝鮮系グループが偽 AI/ブロックチェーン採用担当を装い IT 専門職 30,000 台超に感染 ($10.7M 窃取); Dec 2025〜Jul 2026 で 100 か国以上が対象](https://www.bleepingcomputer.com/news/security/north-korean-waterplum-hackers-infected-30-000-devices-worldwide/) — FBI・日本警察庁・D3C・ASD・BfV の合同 CSA; コーディングテストや Web 会議修正ファイルを装ったマルウェアで仮想通貨ウォレット 7,000 超から資金・認証情報を窃取; 313 総局 Munitions Industry Department 帰属 *(BleepingComputer / IC3 CSA / Security Affairs)*

- **[2026-09-22]** [CISA が Cyber Storm X を開催 — 2,000 名超・200 組織参加の 4 日間国家サイバー演習; 交通・上下水道インフラを狙う国家アクターシナリオを想定し連邦機関・民間の協働インシデント対応を検証](https://securityboulevard.com/2026/09/daily-ot-security-news-september-22-2026/) — OT/ICS セキュリティの演習シナリオが中心; 演習結果報告は後日公開予定 *(SecurityBoulevard / CISA)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 today-2 (2026-09-21) 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-89422 / GHSA-rgxr-4g4w-j875 | Erlang/OTP ssl 9.5〜(OTP 22.2〜OTP 29.0) — OTP 27.3.4.18 / 28.5.0.7 / 29.1.1 未満 | CWE-322 / CVSS 9.3 | オンパス攻撃者がクライアントが提示していない `pre_shared_key` 拡張を ServerHello に挿入 → `tls_client_connection_1_3:handle_server_hello/2` が拡張の存在のみで resumption=true をセット → `ssl:connect` がサーバー証明書の検証なしに `{ok, Socket}` を返し MiTM 完成 | [OTP-29.1.1 tag (2026-09-22)](https://github.com/erlang/otp/releases/tag/OTP-29.1.1) | **CVSS 9.3** / 証明書検証スキップによる TLS 1.3 MiTM / Elixir Mint・Erlang gun 等の同 ssl ライブラリ利用クライアントの PSK 拡張処理への水平バリアント候補; RabbitMQ・CouchDB 等 Erlang ベースミドルウェア全般に影響 |
| CVE-2026-94097 | Netcore NBR200V2 v1.3.241127.071246 (ファームウェア) | CWE-77 / CVSS 10.0 | 未認証の遠隔攻撃者が CGI Diagnostic Endpoint `/www/cgi-bin/network_tools` の `param/key/val` 引数を操作 → HTTP リクエスト内の入力がフィルタリングなしに `system()` 相当のシェル呼び出しに渡る → ルート権限でのリモートコマンド実行 | 修正なし (ベンダー応答不能) — [VulDB #408026](https://vuldb.com/vuln/408026) | **CVSS 10.0 / パッチなし** / 管理インターフェースのパラメータ直接 `system()` 渡し / TP-Link・D-Link 等の他 SOHO ルーター CGI 診断ツールへの水平バリアント候補; WAN 露出デバイスは即時隔離を推奨 |
| CVE-2026-91710 | Google Chrome < 153.0.8010.47 (全プラットフォーム) | CWE-416 / CVSS 9.6 | 遠隔攻撃者が細工した HTML ページを開かせる → WebAppInstalls コンポーネントで既に解放されたオブジェクトへのポインタを参照 (Use-After-Free) → サンドボックス外での任意コード実行 | [Chrome 153.0.8010.47 (Stable Channel Update 2026-09-22)](https://chromereleases.googleblog.com/) | **CVSS 9.6** / ブラウザ UAF サンドボックスエスケープ / Chromium 派生ブラウザ (Edge・Brave・Opera 等) の同バージョン以前での同コンポーネント UAF 確認を推奨 |
| CVE-2026-93372 | Google Chrome on Android < 153.0.8010.52 | CWE-120 / CVSS 9.6 | 遠隔攻撃者が細工した HTML ページを Android Chrome で開かせる → WebGL コンポーネントのバッファ長計算不備により境界外書き込みが発生 → サンドボックス外での任意コード実行 | [Chrome 153.0.8010.52 Android (2026-09-22)](https://chromereleases.googleblog.com/) | **CVSS 9.6** / Android WebGL スタックバッファオーバーフロー / Android WebView 利用アプリ (埋め込みブラウザ) での同 WebGL パス確認を推奨 |
| CVE-2026-86473 | Apache Airflow < 3.3.2 | CWE-613 / CVSS 9.1 | Core API のログアウトエンドポイントが `_token` クッキー形式のセッションのみを失効処理 → `Authorization: Bearer <token>` ヘッダー形式でログアウトを送信した場合はベアラートークンが無効化されず有効なまま残存 → セッション終了後もベアラートークンで API 操作が継続可能 | [Apache Airflow 3.3.2 (NixOS pkgs issue 565730)](https://github.com/NixOS/nixpkgs/issues/565730) (commit 不明) | **CVSS 9.1** / ログアウト時トークン失効の不完全実装 / Prefect・Luigi・Argo Workflows 等他ワークフローオーケストレーターの Bearer トークンログアウト処理への水平バリアント候補 |

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-09-18 | IC3 CSA (NPA・FBI・D3C・ASD・BfV 共同) | 北朝鮮 WaterPlum (Contagious Interview) が偽 AI/暗号通貨採用で日本を含む 100 か国超の IT 専門職 30,000 台超を感染 — Sep 21 主要報道 | 高 / 仮想通貨 $10.7M 窃取・認証情報窃取 | [IC3 CSA PDF](https://www.ic3.gov/CSA/2026/260918.pdf) |

> 直近2日間 (2026-09-21〜23) に JVN/JPCERT/IPA から新規アドバイザリは確認できませんでした。（JVN/JPCERT サイトへの直接 WebFetch 不可。検索経由では Sep 22 以降の新規国内勧告は見当たらず）

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 25+
- 採用件数: AI=6 / Security=5 / CVE=5 / 国内=1
- 除外理由内訳:
  - 採用窓外（公開日 < 2026-09-21）: Safari 27 MCP server（Sep 14）、Google Agent Anomaly Detection（Sep 17）、TypeSafe AI Jev（Sep 15）、Japan Digital Agency VPN breach 開示（Sep 15）、AISLE curl CVE ×6（Aug 24-27）、WaterPlum IC3 advisory 元発信日（Sep 18）、Spain AEPD AI agent breach（Sep 14）
  - 重複（直近7日 digest 既報）: BragJack（Sep 22 digest）、Anthropic Reuters GPT-6 Astra（Sep 22 digest）、Mongoid CVE-2026-93762/93759（Sep 21 digest）、mnemosyne-memory CVE-2026-59163（Sep 21 digest）、ToolHive CVE-2026-58197（Sep 21 digest）、Orkes Conductor CVE-2026-58138（Sep 21 digest）、Plugin4Shell（Sep 20 digest）、Gemini CTF侵入（Sep 20 digest）、Gyazo侵害（Sep 20 digest）、SolarWinds CVE-2026-28326（Sep 21 digest）、TanStack侵害（Sep 21 digest）、CISA Linux KEV 3件（Sep 20 digest）、Apache MINA CVE-2026-94301（Sep 22 digest）、MISP CVE-2026-94401（Sep 22 digest）、Telegram CVE-2026-94488（Sep 22 digest）、kcp CVE-2026-61682（Sep 20 digest）
  - CVE採用窓外: CVE-2026-7273 元 advisory Jun 16 2026（KEV追加 Sep 21 のためセキュリティニュース扱い）、CVE-2026-32996 PoC Sep 14（野外悪用記事 Sep 22 のためセキュリティニュース扱い）、CVE-2026-55366 Android Sep 15、CVE-2026-86462 Airflow FAB Sep 21（同日付 CVE-2026-86473 と重複機能枠のため後者を優先）
- 取得失敗ソース（EGRESS_BLOCKED）: helpnetsecurity.com, bleepingcomputer.com, securityweek.com, nvd.nist.gov, jvn.jp, jpcert.or.jp, osv.dev, agenticsecurity.substack.com, securityaffairs.com, securityboulevard.com (WebFetch のみ; 検索スニペットは利用可)

</details>
