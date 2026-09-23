# KEDA Daily Digest — 2026-09-24 (JST)

> 採用範囲: 公開日 2026-09-22 〜 2026-09-24
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

OpenAI が GPT-6 Sol & Luna の2モデルを 9 月 22 日に投入（Sol: $2/$10/M、Luna: $0.10/$0.50/M）し Claude Opus 5.5 と同日に廉価フロンティアモデル競争が加速した。安全保障面では国連安全保障理事会が 9 月 23 日に AI の制御喪失リスクを主題とした初の高レベルブリーフィングを開催し、Altman・Amodei・Bengio と中国の DeepSeek・Moonshot が初めて同一の国際安全保障の場に並んだ。インフラセキュリティ面では F5 BIG-IP APM・Check Point Management Server・Arista VeloCloud Orchestrator の 3 製品にゼロデイ悪用が同時確認され、CISA KEV が 4 件一括登録（連邦機関 9/25 期限）された。

## AI 関連ニュース

- **[2026-09-22]** [OpenAI が GPT-6 Sol & Luna を発表 — GPT-6 Astra の廉価版2モデル; Sol は $2/$10/M・Luna は $0.10/$0.50/M; GPT-5.6 比で「ミスが約半分」と主張; API・ChatGPT・GitHub Copilot で即時提供開始](https://openai.com/index/introducing-gpt-6-sol-and-luna/) — Astra と同様の訓練手法を採用しつつ API コストを 50% 以上削減; Claude Opus 5.5 と同日リリースで廉価フロンティア争いが激化 *(OpenAI / VentureBeat / TechCrunch)*

- **[2026-09-23]** [国連安全保障理事会が AI 国際安全保障リスクを主題に初の高レベルブリーフィングを開催 — Altman (OpenAI)・Amodei (Anthropic)・Bengio (UN AI 科学パネル共同議長)・DeepSeek・Moonshot が出席; AI 制御喪失・自己改良・国際拡散のリスクを議論](https://www.bnnbloomberg.ca/business/artificial-intelligence/2026/09/23/ai-leaders-warn-un-of-security-risks-as-systems-grow-more-powerful/) — フランス議長国主催; 米中 AI 開発者が国連安保理で安全リスクを共同議論した初の事例; 拘束力ある決議は採択されず *(BNN Bloomberg / Reuters / Security Council Report)*

- **[2026-09-22]** [OpenAI が第三者安全評価フレームワーク「Priorities and Principles for Third-Party Assessments」を公開 — 訓練・評価・展開の各段階で外部組織が技術的安全評価を実施できる仕組みを整備; METR・Redwood Research と協議中](https://openai.com/index/priorities-principles-third-party-assessments/) — 安全ケース・ガードレール評価・能力評価・不整合インシデント調査の4領域を優先対象に指定; Anthropic/Accenture 論争を受けた業界全体の独立性強化の流れと連動 *(OpenAI / Bloomberg / The Next Web)*

- **[2026-09-22]** [Alphabet の Intrinsic が産業用ロボティクス基盤 Intrinsic Core を Apache 2.0 でオープンソース化 — ROSCon 2026 Toronto で発表; リアルタイム制御・Nvidia FoundationPose 姿勢推定・モーションプランニング・グラスププランニング・シミュレーション・ROS ドライバを同梱](https://www.intrinsic.ai/blog/posts/introducing-intrinsic-core) — 実製造環境で使用されているコアコンポーネントを GitHub に公開; 初回 AI for Industry Challenge に 115 か国 5,000 人超が参加 *(Intrinsic / Unite.AI / SiliconAngle)*

- **[2026-09-23]** [CISA が CVE プログラムの「Quality Era」移行ロードマップ白書を公開 — AI が加速するソフトウェアライフサイクル変化と CNA の世界規模拡大を受け、Growth Era から Quality Era への構造転換を宣言; AI 生成コードによる新脆弱性クラスへの対応方針も明示](https://www.cisa.gov/news-events/news/cisa-whitepaper-charts-path-establishing-and-maturing-cve-program-quality) — 2026 年の CVE 採番ペースが前年比 23% 増と説明; プログラム品質・一貫性・採番精度の向上方針を示す *(CISA)*

## セキュリティ関連ニュース

- **[2026-09-22]** [F5 BIG-IP APM CVE-2026-94127 ゼロデイが野外で悪用中 — CVSS 9.8 ヒープバッファオーバーフロー; OAuth 認可サーバー構成の APM を標的に未認証 RCE; CISA KEV 追加・連邦機関 9/25 期限](https://thehackernews.com/2026/09/f5-patches-critical-big-ip-apm-zero-day.html) — BIG-IP 17.1.0〜17.1.3・17.5.0〜17.5.1・21.1.0 が対象; APM アクセスポリシーと OAuth 認可サーバープロファイルを同一 VIP に設定している環境が脆弱; エンジニアリングホットフィックス提供済み *(The Hacker News / SecurityWeek / CERT-EU)*

- **[2026-09-22]** [Check Point Management Server CVE-2026-93616 ゼロデイ (7/23 以来の野外悪用) と CVE-2026-85102 Spark ファイアウォール VPN 証明書バイパスが CISA KEV 追加 — 連邦機関 9/25 期限; CVE-2026-93616 は管理 Web サービスのパストラバーサルで任意スクリプト実行・任意 Java クラスロードが可能](https://blog.checkpoint.com/security/security-advisory-action-required-active-exploitation-of-cve-2026-85102-and-a-management-pre-authentication-vulnerability-cve-2026-93616/) — CVE-2026-85102 は Sep 9 初報の VPN 証明書バイパス (CVE-2026-91843 とは別件); 両 CVE に修正済みホットフィックスあり *(Check Point Blog / The Hacker News / BleepingComputer)*

- **[2026-09-22]** [Arista VeloCloud Orchestrator CVE-2026-93952 ゼロデイが CISA KEV 追加 — CVSS 10.0; 証明書認証構成の VCO に対し未認証で内部特権機能にアクセス可能; 5.2・6.4 系は修正済みだが 6.1・7.0 系は未修正のまま野外悪用中](https://www.arista.com/en/support/advisories-notices/security-advisory/24765-security-advisory-0183) — 管理対象 Edge デバイスへの横移動リスクがある; ネットワーク的にアクセス可能な VCO インターフェースの隔離が最優先 *(SecurityWeek / The Hacker News / Arista Advisory)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 today-2 (2026-09-22) 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-94127 | F5 BIG-IP APM 17.1.0〜17.1.3 / 17.5.0〜17.5.1 / 21.1.0 | CWE-122 / CVSS 9.8 | 未認証攻撃者が OAuth 認可サーバー設定の APM に細工パケットを送信 → `libauthz` の PKCE コード交換パスでヒープ割り当て長の上限チェックが欠如 → ヒープ上の隣接制御構造を上書き → リモートコード実行 | [CERT-EU SA 2026-013 (2026-09-22)](https://cert.europa.eu/publications/security-advisories/2026-013/) (F5 engineering hotfix 提供済み) | **CVSS 9.8 / KEV (2026-09-22) / 野外悪用中 / 連邦機関 9/25 期限** / OAuth PKCE フローの APM 実装 / Nginx Plus・HAProxy の OAuth 認可フローを実装する他 ADC への水平バリアント候補 |
| CVE-2026-93952 | Arista VeloCloud Orchestrator On-Prem < 5.2.x・< 6.4.x (6.1・7.0 系は未修正) | CWE-20 / CVSS 10.0 | 攻撃者が Edge 証明書の公開鍵部分を VCO Web インターフェースに提示 → Input Validation 欠如で内部 RPC 認可チェックをスキップ → 特権 Edge 管理操作 (設定変更・デバイス追加削除等) を未認証で実行 → 管理下 Edge デバイス全台への横移動が可能 | [Arista SA-0183 (2026-09-22)](https://www.arista.com/en/support/advisories-notices/security-advisory/24765-security-advisory-0183) (commit 不明) | **CVSS 10.0 / KEV (2026-09-22) / 野外悪用中 / 6.1・7.0 未修正** / SD-WAN Orchestrator の公開鍵提示による認可バイパス / VMware SD-WAN・Cisco Catalyst SD-WAN 等の他 SD-WAN Orchestrator 認可実装への水平バリアント候補 |
| CVE-2026-93616 | Check Point Security Management Server / Multi-Domain R81.20 以前 | CWE-22 / CVSS 9.1 | 未認証攻撃者が管理 Web サービスの REST エンドポイントにパス区切り文字を含む URI を送信 → ディレクトリトラバーサルでサービスコンテキストが任意パスを解決 → 任意スクリプトの実行または任意 Java クラスのロード → 管理者権限で RCE | [Check Point SA (2026-09-22)](https://blog.checkpoint.com/security/security-advisory-action-required-active-exploitation-of-cve-2026-85102-and-a-management-pre-authentication-vulnerability-cve-2026-93616/) (commit 不明) | **KEV (2026-09-22) / 7/23 以来の野外悪用 / 連邦機関 9/25 期限** / ファイアウォール管理 REST API のパストラバーサル / Palo Alto Panorama・Fortinet FortiManager 等他ファイアウォール管理プレーン REST API 実装への水平バリアント候補 |
| CVE-2026-75791 / GHSA-xcf2-p4gr-c87c | Zohocorp ManageEngine ADSelfService Plus < build 7001 | CWE-306 / CVSS 8.6 | 未認証リモート攻撃者が特定条件で REST API エンドポイントに直接リクエストを送信 → 認可チェックが一貫して適用されない実装欠陥 → 管理者専用の読み書き操作（ディレクトリ設定変更・管理者設定改ざん）を認証なしで実行 → パスワードリセット機能の悪用・正規ユーザーのアクセス妨害 | [ManageEngine Advisory CVE-2026-75791 (2026-09-22)](https://www.manageengine.com/products/self-service-password/advisory/CVE-2026-75791.html) | CVSS 8.6 / Active Directory 連携パスワード管理基盤の認可バイパス / ServiceDesk Plus・SSPR ツール等の他パスワード管理 REST API 実装への水平バリアント候補 |
| CVE-2026-61674 | Fluent Bit 0.11.0〜5.0.7 | CWE-121 / CVSS 9.2 | 攻撃者が `out_forward` の Secure-Forward 接続先として動作 → ハンドシェイク中の PONG[2] reason フィールドに 32 バイト超のデータを MessagePack で送信 → スタックバッファへの型・長さ検証なしコピーでスタック制御データを上書き → スタックカナリー無効ビルドで RCE、有効ビルドでも反復クラッシュ/生存プローブによる RCE 支援 | [Fluent Bit 5.0.8 / NixOS#565743](https://github.com/NixOS/nixpkgs/issues/565743) | **CVSS 9.2** / Kubernetes 標準 log forwarder への Secure-Forward 接続先偽装攻撃 / Vector・Logstash 等他 log forwarder の Secure-Forward PONG ハンドシェイク実装への水平バリアント候補 |
| CVE-2026-58491 | warp-tech/warpgate < 0.25.5 | CWE-79 / CVSS 9.3 | 攻撃者が SSO 開始エンドポイントの `next` パラメータに JS を埋め込んだ URL を被害者に踏ませる → SSO 完了後の `/@warpgate/api/sso/return` ハンドラが `next` を HTML エスケープなしにレスポンスへ書き込み → 認証済み warpgate オリジン上でスクリプト実行 → 管理者権限セッション乗っ取り → SSH/RDP プロキシ全ターゲットへの横移動 | [warpgate v0.25.5 (advisory 2026-09-22)](https://vuldb.com/cve/CVE-2026-58491) | **CVSS 9.3** / SSO コールバックの next パラメータ未エスケープ XSS + オープンリダイレクト / Guacamole・Teleport・Cloudflare Access 等他 SSH/RDP Bastion Host の SSO コールバック実装への水平バリアント候補 |

## 国内脆弱性・インシデント情報

> 直近2日間に該当する新規ニュースは確認できませんでした。（JVN / JPCERT / IPA への直接アクセス不可; 検索経由では 2026-09-22 以降の新規 JVN アドバイザリは確認できず）

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 22+
- 採用件数: AI=5 / Security=3 / CVE=6 / 国内=0
- 除外理由内訳:
  - 採用窓外または重複（直近7日 digest 既報）: Claude Opus 5.5（09-23 digest）、Grok 4.7（09-23 digest）、Aikido Altar-1（09-23 digest）、ShinyHunters/FBI（09-23 digest）、WaterPlum 北朝鮮警告（09-23 digest）、Veeam CVE-2026-32996（09-23 digest）、Erlang/OTP CVE-2026-89422（09-23 digest）、Netcore CVE-2026-94097（09-23 digest）、Chrome CVE-2026-91710/93372（09-23 digest）、Apache Airflow CVE-2026-86473（09-23 digest）、BragJack Attack（09-22 digest）、米中 AI 安全通報提案（09-22 digest）、Apache MINA CVE-2026-94301（09-22 digest）、MISP CVE-2026-94401（09-22 digest）、Telegram CVE-2026-94488（09-22 digest）、SolarWinds CVE-2026-28326（09-21 digest）、Mongoid CVE 群（09-21 digest）、TanStack サプライチェーン（09-21 digest）、mnemosyne-memory CVE（09-21 digest）、ToolHive CVE（09-21 digest）、Orkes Conductor CVE（09-21 digest）、Plugin4Shell（09-20〜21 digest）
  - CVE 採用窓外（初報が 2026-09-22 より前）: Check Point CVE-2026-85102（Sep 9 初報; KEV 追加 Sep 22 のためセキュリティニュース扱い）、Check Point CVE-2026-91843（Sep 17 digest）
  - 日付不確定のため除外: Deadbugz MCP サプライチェーンキャンペーン（PR 生成 Aug 10、開示時期が確認できた範囲では Sep 22 以前の可能性が高い）
- 取得失敗ソース（EGRESS_BLOCKED）: thehackernews.com, bleepingcomputer.com, securityweek.com, nvd.nist.gov, jvn.jp, jpcert.or.jp, osv.dev, helpnetsecurity.com, cert.europa.eu (WebFetch のみ; 検索スニペットは利用可)

</details>
