# KEDA Daily Digest — 2026-06-20 (JST)

> 採用範囲: 公開日 2026-06-18 〜 2026-06-20
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

---

## AI

- **[AI安全] Google DeepMind、AIエージェント制御ロードマップを公開** (2026-06-18) — 「内部システムを不完全にアラインされた高度AIから守る」Rohin Shah & Four Flynn執筆、ライブGemini Sparkエージェントモニタリング含む包括的安全戦略。 https://deepmind.google/blog/securing-the-future-of-ai-agents/

- **[新機能] Claude Code Artifacts ベータ公開 (Team/Enterprise)** (2026-06-18) — コーディングセッションをライブ共有可能なHTMLページに変換、リアルタイムコラボレーション対応。 https://claude.com/blog/artifacts-in-claude-code

- **[標準化] MCP Enterprise Authorization with Okta 安定版リリース** (2026-06-18) — ゼロタッチSSO実現、OktaがMCP初IdP、Asana/Atlassian/Figma/Supabase/Slack等7プロバイダー対応。 https://blog.modelcontextprotocol.io/posts/enterprise-managed-auth/

- **[新サービス] AWS Continuum、AI脆弱性管理サービス提供開始** (2026-06-18) — 4フェーズAI駆動型脆弱性管理、AWS Summit 2026発表、ゲートプレビュー開始。 https://helpnetsecurity.com/2026/06/18/aws-continuum-for-code-vulnerabilities/

- **[M&A] SpaceX、Cursor (Anysphere) を約600億ドルで買収** (2026-06-19) — SEC Form 8-K提出、株式取引による買収、SPCX株+16〜17%上昇。

- **[続報] Anthropic Fable 5輸出規制、WaPo/WIREDが2段階禁止の経緯を報道** (2026-06-18〜20) — David Sacksの最後通牒とManaging Directorsの「数日内に解決」発言が明らかに、返金期限は6月20日。

---

## Security

- **[M&A] Accenture、Dragos + runZero + NetRise を約42億ドルで買収** (2026-06-18) — OTサイバーセキュリティ3社同時取得、合算ARR約2億800万ドル (前年比+53%)。 https://helpnetsecurity.com/2026/06/19/accenture-dragos-runzero-netrise-acquisition/

- **[続報] CISA、FortiBleed被害者にセッション終了と認証情報リセットを緊急勧告** (2026-06-18) — 確認済み侵害デバイス86,644台、CISAアラート正式発出。 https://cisa.gov/news-events/alerts/2026/06/18/cisa-urges-hardening-fortinet-devices-after-reports-credential-exposure

- **[Botnet] Android TVボットネット "Popa"、NASDAQレスイスラエル企業Alarum Technologies/NetNutに関連** (2026-06-18) — Krebs on Security調査、140万以上のIP、広告詐欺・スクレイピング・アカウント乗っ取りに悪用。 https://krebsonsecurity.com/2026/06/popa-botnet-linked-to-publicly-traded-israeli-firm/

- **[EoP/NoFix] GCP Config Connector IAMバイパス "ConfigConfusion"、CVSS 10.0でパッチ未提供** (2026-06-18) — OLeary Sec研究、任意K8s namespaceユーザーがGCP Org Owner権限を取得可能、Google P1/S1受理も未修正。 https://olearysec.com/research/config-connector-authorization-bypass/

- **[RansomGroup] INC Ransomware、2023年8月以降830+被害組織の詳細分析** (2026-06-18) — Rust製暗号化、米国被害組織65%、2026 Q1 4番目に多発、Veeam DPAPI認証情報標的。 https://thehackernews.com/2026/06/inc-ransomware-claims-830-victims-since.html

- **[Critical] F5 NGINX、CVSS 9.2の重大脆弱性2件に帯域外パッチ発行** (2026-06-18) — K000161614アドバイザリ更新、HTTP/3 UAF・HTTP/2+gRPCヒープオーバーフロー、詳細は下記CVEセクション参照。 https://bleepingcomputer.com/news/security/f5-issues-out-of-band-patches-for-critical-nginx-vulnerabilities/

---

## CVE

| CVE / GHSA | 公開日 | CVSS | CWE | 製品・バージョン | 概要 | KEV/EPSS |
|---|---|---|---|---|---|---|
| GHSA-r253-r9jw-qg44 (CVE未採番) | 2026-06-18 | 10.0 | CWE-78 | Crawl4AI ≤ 0.9.0 | 非認証RCE。browser_config.extra_args経由でChromiumの`--utility-cmd-prefix`等を注入→コンテナ内任意コマンド実行。v0.9.0で修正済み。GHSA-qxjp-w3pj-48m7 (AST bypass) とは別脆弱性。 | — |
| CVE-2026-42530 | 2026-06-17〜18 | 9.2 | CWE-416 | NGINX (HTTP/3対応ビルド) | ngx_http_v3_module Use-After-Free → DoS/RCE (ASLR無効時)。非デフォルト設定 (quic) が必要。NGINX Plus R34-p1/Open Source 1.28.0-patch1で修正。 | — |
| CVE-2026-42055 | 2026-06-17〜18 | 9.2 | CWE-122 | NGINX (HTTP/2+gRPC対応ビルド) | ngx_http_proxy_v2_module + ngx_http_grpc_module ヒープオーバーフロー → DoS/RCE。同上パッチで修正。 | — |
| CVE-2026-48933 | 2026-06-18 | 高 | CWE-190 | Node.js 22.x/24.x/26.x | WebCrypto AES整数オーバーフロー → リモートDoS。v22.23.0/v24.17.0/v26.3.1で修正。 | — |
| CVE-2026-48618 | 2026-06-18 | 高 | CWE-295 | Node.js 22.x/24.x/26.x | TLS UnicodeドットセパレーターによるワイルドカードSAN認証バイパス。同上バージョンで修正。 | — |

---

## 国内

直近2日間に該当する新規ニュースは確認できませんでした。

---

<details>
<summary>debug: excluded_set (直近7ダイジェスト 2026-06-13 〜 2026-06-19)</summary>

**2026-06-19:** CVE-2026-20181, CVE-2026-20190, GHSA-r8mh-x5qv-7gg2/CVE-2026-55200, CVE-2026-35293, CVE-2026-12289, CVE-2026-12328, CVE-2026-50656, GHSA-p3h9-73g9-x6m3/CVE-2026-54388, Klue OAuth/Salesforce breach, ShinyHunters MSG Sports, SpaceBears ECOVACS, Steam Workshop malware, Anthropic Seoul office, Antigravity CLI

**2026-06-18:** CVE-2026-48907, GHSA-2f55-g35j-5jmf, GHSA-8fq9-273g-6mrg, GHSA-x223-p2gf-v735, CVE-2026-24252, CVE-2026-24228, CVE-2026-53876, CVE-2026-9258–9262, CVE-2026-50255, @mastra npm supply chain, JetBrains malicious plugins, OpenAI Deployment Simulation, CrowdStrike AWS, Anthropic privacy policy, FortiBleed (SOCRadar), Phantom Stealer, Rokarolla, CISA JCE KEV

**2026-06-17:** CVE-2026-47101, CVE-2026-47102, CVE-2026-40217, CVE-2026-20262, CVE-2026-54420, GHSA-qxjp-w3pj-48m7, GHSA-xmwj-c75x-6346, CVE-2026-48491, OX Security MCP advisory, LiteLLM 3-CVE chain, Anthropic Fable 5 ban (Bloomberg), ESET FishMonger SprySOCKS, UNC6508, ShinyHunters Kodak, DragonForce Backdoor.Turn, ScarCruft NarwhalRAT, FortiSandbox exploitation, CISA KEV June 15, Atlassian bulletin

**2026-06-16:** GHSA-ff9g-85jq-r3g3, CVE-2026-5482, CVE-2026-11860, AI GuardRail DoS, ShinyHunters Council of Europe PeopleSoft, Awesome Motive CDN, Chrome wallpaper extensions

**2026-06-15:** CVE-2026-11624/GHSA-76g7-m3xw-x9gr, CVE-2026-54410/GHSA-6f53-f2m4-6j2h, CVE-2026-54412/GHSA-28cw-rpqc-wqqj, CVE-2026-54413/GHSA-36r7-c6f4-gj9g, CVE-2026-54411/GHSA-56gg-22rq-q53x, Google MCP Toolbox DNS rebinding, BugHunter toolkit, Splunk Pre-Auth RCE watchTowr, OT/IoT CVEs

**2026-06-14:** CVE-2025-67644, CVE-2026-28277, CVE-2026-27022, Sonatype-2026-003775, CVE-2026-50645, Anthropic Fable 5 ban (initial), Agentjacking, LangGraph CVE chain, Velvet Ant, Atomic Arch

**2026-06-13:** GreatXML, CVE-2026-12007–12010, CVE-2026-0273, Brutecat Google VRP, OpenAI Ona acquisition, NY AI 7 bills, Chrome 149, OnyxC2, DragonForce/TheGentlemen

</details>

*excluded_set 参照: 直近7ダイジェスト (2026-06-13 〜 2026-06-19) の全 CVE/GHSA/URL を除外済み。*
