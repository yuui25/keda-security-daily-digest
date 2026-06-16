# KEDA Daily Digest — 2026-06-17 (JST)

> 採用範囲: 公開日 2026-06-15 〜 2026-06-17
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

OX Security が MCP プロトコルの STDIO 設計欠陥を起点とする包括的 AI サプライチェーン RCE Advisory (150M+ ダウンロード影響) を公開し、Obsidian Security も同日 LiteLLM 3-CVE チェーン (CVSS 9.9) を開示—低権限ユーザーから AI ゲートウェイ完全制御に至る経路が実証され、AI インフラへの組織的攻撃が加速している。セキュリティ面では ESET が I-Soon 系 FishMonger APT の SprySOCKS Windows カーネルルートキット (WIN_DRV) を初公開し、DragonForce が Microsoft Teams TURN リレーを C2 に悪用する Backdoor.Turn (初の野外確認)、ScarCruft が RokRAT から NarwhalRAT への乗り換えを展開するなど国家系 APT の新手法が重なった。Cisco SD-WAN Manager の野外悪用 CVE が 2 週間で 2 件目となり CISA KEV に追加されたほか、Anthropic と Trump 政権の Fable 5 禁止令協議は 6/15 時点で解決に至らず。

## AI 関連ニュース

- **[2026-06-16]** [OX Security が「Mother of All AI Supply Chains」MCP 包括サプライチェーン Advisory を公開 — Cursor / VS Code / Windsurf / Claude Code / Gemini-CLI の全主要 IDE で MCP STDIO トランスポートの設計欠陥を利用した RCE が成立; 150M+ ダウンロード影響; 30+ 責任ある開示・10+ High/Critical CVE を文書化; Windsurf では CVE-2026-30615 でゼロクリック RCE; 根本原因がプロトコル設計にあるため、Anthropic が SDK にマニフェスト専用実行またはコマンドアローリストを実装しない限り個別パッチでは完全修正不可](https://www.ox.security/blog/mcp-supply-chain-advisory-rce-vulnerabilities-across-the-ai-ecosystem/) *(OX Security / The Hacker News)*

- **[2026-06-15]** [Obsidian Security が LiteLLM AI ゲートウェイで低権限ユーザー → フル Admin → RCE の 3-CVE チェーン (CVSS 9.9) を公開 — CVE-2026-47101 (key-management の `allowed_routes` 未検証)・CVE-2026-47102 (`/user/update` でフィールドレベル認可欠落により `user_role=proxy_admin` に自己昇格)・CVE-2026-40217 (Custom Code Guardrail の `exec()` を regex バイパスで脱出し任意コード実行); 全プロバイダー API キー・暗号化クレデンシャル・ルーティングデータが窃取対象; v1.83.14-stable で修正](https://thehackernews.com/2026/06/litellm-vulnerability-chain-lets-low.html) *(The Hacker News / Obsidian Security)*

- **[2026-06-15]** [[続報] Anthropic が Trump 政権担当者と Claude Fable 5 禁止令について高官協議も解決に至らず — Bloomberg 報道; 双方は Fable 5 が呈するリスク水準について依然見解が割れたまま; 6/15 時点で Fable 5・Mythos 5 はオフライン継続; 同時期に Pentagon が禁止令発効から数時間後にイラン攻撃作戦で Claude を (Palantir Maven Smart System 経由で) 使用していたことが報道され、AI の軍事利用と商業停止の矛盾が政治問題化; Anthropic CEO は「自社モデルが特定攻撃に使用されたかを確認する手段がない」と表明](https://www.bloomberg.com/news/articles/2026-06-15/anthropic-set-to-meet-trump-officials-over-ai-security-concerns) *(Bloomberg / AOL / Responsible Statecraft / Business Standard)*

- **[2026-06-16]** [Fortune: Anthropic Fable 5 輸出禁止が DeepSeek ZAI・オープンソース AI の市場流入を加速 — 16% の企業が主要 AI プロバイダー停止時の継続計画を持たないことが Fable 5 禁止で顕在化; 6/12 の禁止から即日生産ワークフローが停止した企業が続出; DeepSeek V4 はフロンティアモデル相当の性能を達成しており、米国の輸出規制が皮肉にも中国モデルへの移行を後押しするという逆説が生じている](https://fortune.com/2026/06/16/us-anthropic-ban-open-source-ai-deepseek-zai/) *(Fortune)*

## セキュリティ関連ニュース

- **[2026-06-16]** [ESET が I-Soon (FishMonger) 系 APT の SprySOCKS Windows 新バリアント 2 種を初公開 — WIN_DRV はカーネルドライバーをルートキットとして搭載しプロセス・ファイル・ソケットを防御ツールから隠蔽 (Linux 版よりも高度なステルス); WIN_PLUS は標準ユーザーモードバリアント; 両者とも 30+ コマンド・ハードコード C2・TCP/UDP/WebSocket 通信に対応; 実際の攻撃テレメトリは 2023〜2024 年にホンジュラス・台湾・タイ・パキスタンの政府機関を標的](https://thehackernews.com/2026/06/china-linked-sprysocks-backdoor-expands.html) *(ESET WeLiveSecurity / The Hacker News / BleepingComputer)*

- **[2026-06-15]** [Google Threat Intelligence Group が中国系 APT「UNC6508」による米国・カナダ研究機関を標的とした 1 年超の諜報キャンペーンを公表 — REDCap (研究用データ管理 Web アプリ) の外部公開サーバーを侵入起点とし Google Workspace メール転送ルールを悪用して長期データ収集; 標的分野: 防衛インテリジェンス・インド太平洋軍事戦略・AI・無人機・サイバー戦・医療研究; 活動期間 2023 年 9 月〜2025 年 11 月; 被害組織は複数の学術機関・病院・軍事研究施設 (総研究予算数十億ドル規模)](https://thehackernews.com/2026/06/chinese-hackers-abused-google-workspace.html) *(Google TIG / US News / BNN Bloomberg / Cybernews — June 15)*

- **[2026-06-15/16]** [ShinyHunters が Eastman Kodak から 220 万件超のカスタマー・社内データを窃取したと主張 — Kodak はダークウェブ恐喝ポータルへの掲載を確認し「限定的なデータへの一時的な不正アクセスがあった」と公表; ShinyHunters はリーク期限を 2026-06-18 に設定; 欧州評議会侵害 (6/14-15) と Oracle PeopleSoft (100 組織超) キャンペーンに続く ShinyHunters の連続侵害](https://cybernews.com/security/shinyhunters-claims-kodak-hack-2-million-records/) *(Cybernews / CyberInsider)*

- **[2026-06-16]** [Symantec が DragonForce ランサムウェアの新型 Go バックドア「Backdoor.Turn」を解析 — Microsoft Teams の TURN リレーインフラを C2 通信に悪用する手法を野外で初確認; 匿名 Teams ビジタートークンを取得 → Microsoft Skype 基盤の TURN リレー経由で QUIC セッションを確立 → 実 C2 サーバーにトンネリング; 防御側ネットワーク監視には Microsoft 正規サーバーへの接続しか見えず検知困難; 機能: リモートコマンド実行・AD 列挙・ネットワークスキャン・クレデンシャル窃取・横移動](https://www.helpnetsecurity.com/2026/06/16/dragonforce-microsoft-teams-malware-backdoor-turn/) *(Symantec / Help Net Security / BleepingComputer)*

- **[2026-06-16]** [北朝鮮系 ScarCruft (APT37) が新型 NarwhalRAT を展開する Microsoft アカウントなりすましスピアフィッシングキャンペーンを確認 — Microsoft セキュリティ警告メールを偽装した ZIP→LNK→インメモリ多段感染チェーン; NarwhalRAT 機能: キーロガー・スクリーンショット・音声収録・システム情報収集; C2: 韓国系 Web サイト + pCloud; 標的: 南韓系企業; グループ専属マルウェア RokRAT からの初の公式離脱として注目](https://thehackernews.com/2026/06/fake-microsoft-alerts-used-to-deploy.html) *(The Hacker News / GBHackers)*

- **[2026-06-16]** [Defused Cyber が Fortinet FortiSandbox 3 CVE の同時野外悪用を過去 24 時間で初観測 — CVE-2026-39813 (JRPC API パストラバーサル・非認証 auth バイパス、今回初確認) / CVE-2026-39808 (jid パラメーター OS コマンドインジェクション・root RCE、4 月 PoC 公開) / CVE-2026-25089 (start VNC 機能 OS コマンドインジェクション・CVSS 9.1、6/9 開示); FortiSandbox はマルウェア解析専用サンドボックスであり侵害時はセキュリティ監視インフラ自体が無効化される](https://www.helpnetsecurity.com/2026/06/16/fortisandbox-vulnerabilities-cve-2026-39813-cve-2026-39808-cve-2026-25089/) *(Defused Cyber / Help Net Security / The Register / The Hacker News)*

- **[2026-06-15]** [CISA が CVE-2026-54420 (LiteSpeed cPanel Plugin シンボリックリンク追従、CVSS 8.5) と CVE-2026-20262 (Cisco SD-WAN Manager 認証済みファイル書き込み→root 昇格、CVSS 6.5) を KEV に追加 — LiteSpeed の連邦機関修正期限は 2026-06-18 (3 日); Cisco はこれで 2 週間以内に 2 件目の SD-WAN 野外悪用 CVE; SD-WAN Manager は全展開タイプ (オンプレ・Cloud-Pro・Cloud Managed・FedRAMP) が対象](https://www.cisa.gov/news-events/alerts/2026/06/15/cisa-adds-two-known-exploited-vulnerabilities-catalog) *(CISA / Help Net Security / SecurityWeek)*

- **[2026-06-16]** [Atlassian June 2026 Security Bulletin が High 76 件・Critical 24 件 (第三者ライブラリ起因) を修正 — 広く使用されるオープンソースライブラリの上流セキュリティパッチを Jira / Confluence / Bitbucket 等の最新版に統合; Atlassian 自社コードの設計変更は含まず「外部調整済み依存ライブラリの脆弱性」と分類; 公開数の多さは依存スキャンの成熟によるもので脆弱性増加を意味しないと Atlassian が注記](https://confluence.atlassian.com/security/security-bulletin-june-16-2026-1796309326.html) *(Atlassian Support)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-15 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-47101 / CVE-2026-47102 / CVE-2026-40217 | LiteLLM < v1.83.14-stable (Python, AI ゲートウェイ) | CWE-285 / CWE-862 / CWE-94 / **9.9** (連鎖) | 低権限ユーザーが `allowed_routes` 未検証の key-management API で管理者専用ルートのキーを取得 → `/user/update` の `user_role` フィールドが保護されておらず `proxy_admin` に自己昇格 → Custom Code Guardrail の `exec()` を regex バイパスで脱出 → ホスト上で任意コード実行・全 API キー窃取 | [LiteLLM v1.83.14-stable](https://github.com/BerriAI/litellm/releases) | 2026-06-15 Obsidian Security 包括開示 / **CVSS 9.9** / Claude Code・Cursor 等の AI ゲートウェイとして広く使用 / 同製品 CVE-2026-42271 (CISA KEV: MCP command injection) とは別系統の新攻撃チェーン |
| CVE-2026-20262 | Cisco Catalyst SD-WAN Manager ≤26.1.1.1 / ≤20.x 各系 (全デプロイメントタイプ) | CWE-22 / **6.5** | write 権限を持つ認証済みユーザーが Web UI API エンドポイントにパストラバーサル細工リクエストを送信 → サーバー任意パスへファイル書き込み → root 権限昇格の踏み台化 | [cisco-sa-sdwan-privesc-4uxFrdzx](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-privesc-4uxFrdzx) (v20.9.9.2 / 20.12.7.2 / 20.15.5.3 等) | **野外悪用中 (2026-06-15 Cisco 確認) / CISA KEV 追加** / SD-WAN 管理プレーンは企業 WAN 全体の制御面 / 2 週間で 2 件目の Cisco SD-WAN 野外悪用 CVE (前: CVE-2026-20182) |
| CVE-2026-54420 | LiteSpeed Technologies cPanel Plugin < v2.4.8 / WHM PlugIn < v5.3.2.0 (CloudLinux/CageFS 共有ホスティング) | CWE-61 / **8.5** | FTP またはウェブシェルアクセス権を持つ攻撃者がシンボリックリンクを細工 → cPanel Plugin 内部 API が symlink を誤追従 → CloudLinux CageFS の権限境界をバイパス → root 昇格・サーバー完全制御 | [LiteSpeed cPanel Plugin v2.4.8 (2026-06-01)](https://docs.litespeedtech.com/cp/cpanel/) (commit 不明) | **野外悪用中 (2026-05 〜) / CISA KEV 2026-06-15 追加 / 連邦機関修正期限 2026-06-18** / 同種の symlink → CageFS 脱出パターンは CloudLinux 上の他 WHM プラグインへの水平バリアント推奨 |
| GHSA-qxjp-w3pj-48m7 / CVE-2026-53753 | Crawl4AI (pip, Docker API 公開環境, AI Web スクレイピングフレームワーク) | CWE-94 / **Critical** | 非認証攻撃者が Docker REST API エンドポイントにフレームチェーントラバーサルを含む細工リクエストを送信 → AST ベースのコード評価サンドボックスを脱出 → コンテナホスト上で Pre-Auth RCE | [GitHub advisory GHSA-qxjp-w3pj-48m7](https://github.com/advisories/GHSA-qxjp-w3pj-48m7) | 2026-06-15〜17 GHSA 公開 / AI エージェント・RAG パイプラインの Web スクレイピング基盤として広く採用 / Docker API 公開環境では非認証 RCE / 同フレームワーク GHSA-365w-hqf6-vxfg (複数 Docker API 欠陥) も同時公開 |
| GHSA-xmwj-c75x-6346 / CVE-2026-54157 | @lobehub/chat (npm, AI チャット UI フレームワーク, セルフホスト環境) | CWE-918 / **Critical** | 非認証攻撃者が `/webapi/proxy` エンドポイントに任意 URL を指定 → サーバー側リクエストフォージェリ (SSRF) で内部 AWS メタデータエンドポイント・内部 API サーバー・隣接内部ネットワークに到達 → クレデンシャル・AI プロバイダー API キー窃取 | [GitHub advisory GHSA-xmwj-c75x-6346](https://github.com/advisories/GHSA-xmwj-c75x-6346) | 2026-06-15〜17 GHSA 公開 / セルフホスト AI チャット UI として OSS 人気が高い / 非認証 SSRF は内部 AWS IAM 認証情報の窃取に直結 / セルフホスト型 AI プラットフォーム (OpenWebUI 等) の同種 proxy エンドポイントへのバリアントハント推奨 |
| CVE-2026-48491 | Traefik < v3.6.2 / < v2.11.30 (Go, リバースプロキシ/ロードバランサー) | CWE-295 / **High** | 攻撃者が TLS ClientHello の SNI フィールドに不正値を指定 → Traefik SNICheck ルーターが検証をバイパス → 誤ったバックエンドへルーティング / TLS 検証スキップ → 意図しない内部サービスへのアクセス制御バイパス | [Traefik v3.6.2 / v2.11.30](https://github.com/traefik/traefik/releases) | 2026-06-15〜17 GHSA 公開 / AI サービス・API ゲートウェイの前段リバースプロキシとして広く採用 / SNI バイパスは nginx/HAProxy の同仕様実装への水平バリアントハント推奨 |

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|

> 直近2日間に該当する新規ニュースは確認できませんでした。JVN/JPCERT/IPA は引き続き HTTP 403 によりアクセス不可 (WebSearch 経由でも新規国内インシデントは確認されず)。なお CVE-2026-47101〜40217 (LiteLLM AI ゲートウェイ) / GHSA-xmwj-c75x-6346 (LobeHub) / GHSA-qxjp-w3pj-48m7 (Crawl4AI) は国内 AI システム開発者・SaaS プロバイダーに直接関連するため JPCERT/CC の追加アラートに注意が必要。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 35 ソース (Bloomberg, Fortune, FastCompany, OX Security, Obsidian Security, The Hacker News, ESET WeLiveSecurity, Help Net Security, Symantec, Cybernews, CyberInsider, GBHackers, Defused Cyber, The Register, SecurityWeek, BleepingComputer, Google Threat Intelligence Group, US News, BNN Bloomberg, Cisco Security, CISA, GitHub Advisory Database (GHSA直接fetch), CVEReports, SentinelOne, Feedly CVE, Infosecurity Magazine, windowsnews.ai, Atlassian Support, SOCPrime, CycognITo 他)
- 採用件数: AI=4 / Security=8 / CVE=6 / 国内=0
- 採用件数が目安 (AI 各 8〜12 件) を下回った理由:
  - 採用窓 (2026-06-15〜17) は June Patch Tuesday (6/9) から 1 週間後・Anthropic 輸出規制 (6/12) 続報期で主要 AI ラボからの新規モデルリリース・大型政策発表が少ない端境期
  - 多くの上旬ニュースは直近 7 日の excluded_set に収録済み
- 除外理由内訳:
  - 古すぎ (< 2026-06-15):
    - CVE-2026-30615 Windsurf MCP GHSA (2026-04-15 公開、6/16 OX Security 包括 Advisory に再掲されるが CVE 自体は採用窓外)
    - CVE-2026-39808/39813 FortiSandbox パッチ (2026-04 公開)
    - CVE-2026-25089 FortiSandbox OS コマンドインジェクション (2026-06-09 公開)
    - CVE-2026-48558 SimpleHelp OIDC Auth Bypass (2026-06-12 公開/Horizon3 公開)
    - Nintendo SHADOWBYT3$ 侵害 (2026-06-12 公表)
    - Push Security デバイスコードフィッシング急増レポート (2026-05〜06 初旬、2026-06-15 digest 除外済み)
    - Anubis Italian Adriatic Port Authority (2026-01 攻撃、2026-06-11 Resecurity レポート)
    - CVE-2026-47101 NVD 採番日 (2026-05-21)、OX/Obsidian 包括開示日 2026-06-15 を公開日として採用
  - 重複 (excluded_set 直近7日):
    - GHSA-ff9g-85jq-r3g3 (Wazuh CVSS 10.0) — 2026-06-16 digest
    - CVE-2026-5482/11860 (Responsive FileManager/Quick.CMS) — 2026-06-16 digest
    - CVE-2026-11624 (Google MCP Toolbox DNS rebinding) — 2026-06-15 digest
    - CVE-2026-20253 (Splunk Pre-Auth RCE watchTowr) — 2026-06-15 digest
    - CVE-2026-54410/54412/54413/54411 (OT/IoT protocol libs) — 2026-06-15 digest
    - LangGraph CVE-2025-67644/26-28277/26-27022 — 2026-06-14 digest
    - Agentjacking/Velvet Ant/Atomic Arch — 2026-06-14 digest
    - ShinyHunters 欧州評議会 CVE-2026-35273 — 2026-06-16 digest
    - Chrome 152 wallpaper 拡張機能・AI エージェント GuardRail DoS — 2026-06-16 digest
    - Awesome Motive CDN 供給チェーン — 2026-06-16 digest
    - CVE-2026-42271 LiteLLM (CISA KEV, MCP command injection) — 2026-06-11 digest
    - CVE-2026-50751 Check Point VPN — 2026-06-11〜06-13 digest
    - CVE-2026-20182 Cisco SD-WAN — 2026-06-10 digest
  - 日付不明/確認不可:
    - JPCERT/CC / JVN June 15〜17 個別アラート (HTTP 403)
    - CISA KEV June 16〜17 追加分 (CISA June 15 アラートのみ確認)
- 取得失敗ソース (HTTP 403): bleepingcomputer.com / thehackernews.com / cybersecuritynews.com / helpnetsecurity.com / infosecurity-magazine.com / welivesecurity.com / cybernews.com 各個別記事 / ox.security/blog / obsidiansecurity.com / cisa.gov 個別アラート / jpcert.or.jp / jvn.jp — WebSearch スニペット・複数独立媒体・GitHub GHSA 直接フェッチで内容・日付を補完

</details>
