# KEDA Daily Digest — 2026-05-29 (JST)

> 採用範囲: 公開日 2026-05-27 〜 2026-05-29
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Anthropic が Claude Opus 4.8 を 5/28 にリリースし、Dynamic Workflows（数百の並列サブエージェント管理）と大幅な agentic coding 向上で AI エージェント競争が加速。Google Cloud も同日 AI Threat Defense プラットフォームを正式公開し、Gemini・Wiz・CodeMender・Mandiant を統合した自律型脆弱性管理サービスで Anthropic Mythos・OpenAI Daybreak と直接競合する態勢を整えた。脆弱性面では Yamcs（ESA 等が採用する宇宙ミッション制御フレームワーク）で 3 件の RCE が 5/27 に同時公表され、デフォルト構成では非認証 CVSS 9.8 の完全侵害が可能。加えて Oracle が初の月次 Critical Security Patch Update（CSPU）を 5/28 に公開し Oracle REST Data Services の CVSS 10.0 を含む 35 件に対処、また DAEMON Tools Lite の公式インストーラートロイ化（CVE-2026-8398, CVSS 9.8）が CISA KEV に追加されるなど、サプライチェーンと AI インフラへの攻撃が引き続き主要テーマとなった。

## AI 関連ニュース

- **[2026-05-28]** [Anthropic が Claude Opus 4.8 をリリース — Dynamic Workflows (リサーチプレビュー) で数百並列サブエージェント管理、agentic coding 64.3%→69.2%、コード欠陥見落とし率を前バージョン比 1/4 に低減](https://www.anthropic.com/news/claude-opus-4-8) — Super-Agent ベンチマーク全ケース end-to-end 完了（GPT-5.5 超）、fast mode は 3 倍コスト削減・2.5 倍高速化。Claude Code のレートリミット引き上げと extra/max 設定（大規模非同期ワークフロー向け）も同日追加 *(Anthropic / TechCrunch)*

- **[2026-05-27]** [Google Cloud が AI Threat Defense を正式公開 — Gemini・Wiz・CodeMender・Mandiant を統合した常時稼働の自律型脆弱性スキャン〜修復プラットフォームを提供](https://www.helpnetsecurity.com/2026/05/27/google-ai-threat-defense-released/) — Prepare→Scan & Prioritize→Remediate→Monitor の 4 フェーズフレームワーク。Anthropic Mythos・OpenAI Daybreak と直接競合し AI セキュリティ三つ巴が本格化。Accenture・Deloitte・PwC 等がローンチパートナー *(Help Net Security / SecurityWeek)*

- **[2026-05-28]** [OpenAI が AI 導入コンサルティング子会社 DeployCo を設立 — TPG・Goldman Sachs・McKinsey・Bain Capital 等 16 社超から $4B の初期資本調達](https://www.axios.com/2026/05/28/anthropic-opus-release-mythos) — エンタープライズへの GPT-5.5/Codex 等の本格導入・実装支援を専業化。SEC 機密 S-1 申請（5/22）に続き IPO を前にした事業基盤の本格拡充を表明 *(Axios)*

- **[2026-05-27]** [KnowBe4 Prevent が AI 駆動の Misdirected Content Analysis（誤送信検出）と DLP ルールビルダーを 6 月提供開始と発表 — SMB 向けにエンタープライズ級機密メール保護を追加](https://lasvegassun.com/news/2026/may/27/knowbe4-enables-organizations-to-have-independent-/) — PII・財務情報の外部漏洩を送信前に AI 推論でコンテキスト付き警告表示；標準ライセンスで提供し追加費用不要とアピール *(Las Vegas Sun News / KnowBe4)*

## セキュリティ関連ニュース

- **[2026-05-27/28]** [CVE-2026-35616 FortiClient EMS の事前認証 API バイパスを悪用し管理配下の全エンドポイントに EKZ Infostealer を展開するキャンペーンを Arctic Wolf が確認](https://arcticwolf.com/resources/blog/forticlient-ems-exploited-via-cve-2026-35616-to-deliver-ekz-infostealer-disguised-as-a-fortinet-patch/) — 偽の Fortinet パッチ "FortiEndpoint_Patch.exe" を PowerShell で無音実行；Chrome/Firefox の暗号化パスワードストレージを迂回して認証情報を全収集する新型 Infostealer（EKZ）を初公開。3/31 からハニーポットへの悪用試行を観測、Fortinet・CISA が野外悪用を確認 *(Arctic Wolf / SecurityAffairs)*

- **[2026-05-27]** [CISA KEV に 3 件追加 — DAEMON Tools Lite (CVE-2026-8398, CVSS 9.8)・TanStack (CVE-2026-45321)・Nx Console (CVE-2026-48027) を 6/10 期限で連邦機関に適用義務化](https://www.cisa.gov/news-events/alerts/2026/05/27/cisa-adds-three-known-exploited-vulnerabilities-catalog) — DAEMON Tools Lite は TeamPCP (Mini Shai-Hulud キャンペーン) が AVB Disc Soft の公式ビルドインフラを侵害し v12.5.0.2421〜12.5.0.2434 を正規コード署名証明書のまま trojan 化（4/8〜5/5 間に公式サイト daemon-tools.cc から配布）と判明 *(CISA / SecurityAffairs)*

- **[2026-05-28]** [Oracle が月次 Critical Security Patch Update (CSPU) を初公開 — Oracle REST Data Services に CVSS 10.0 を含む全 35 件、7 件が認証不要リモート悪用可能](https://www.oracle.com/security-alerts/cspumay2026.html) — 四半期 CPU から月次 CSPU（毎月第 3 火曜日）への移行として初回リリース；Oracle Database 製品 3 件・REST Data Services 11 件を含み、1 件はサードパーティコンポーネント経由の非 Oracle CVE *(Oracle Security Blog)*

- **[2026-05-27]** [Yamcs（宇宙ミッション制御フレームワーク）に Nashorn/Jython/Janino の 3 スクリプトエンジン経由 RCE が同日公開 — デフォルト設定では非認証 CVSS 9.8、v5.12.7 への即時アップグレードが必須](https://advisories.gitlab.com/maven/org.yamcs/yamcs-core/CVE-2026-46562/) — 3 種のエンジンがサンドボックスなしで user-controlled algorithm text を動的コンパイル・実行。デフォルト設定では guest ユーザーが superuser=true のため CVE-2026-46562 は非認証で成立 *(GitLab Advisories)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-05-27 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-46562 / [GHSA-vmwp-vh32-rj75](https://github.com/advisories/GHSA-vmwp-vh32-rj75) | Yamcs (org.yamcs) < 5.12.7 | CWE-94 / **9.8** | デフォルト設定の guest ユーザー (superuser=true) が `MdbOverrideApi.updateAlgorithm` でアルゴリズムを書き換えると Nashorn ScriptEngine (ClassFilter 未設定) が任意 Java コードをホスト OS 上で実行 → **非認証 RCE** | [yamcs-5.12.7 リリース](https://github.com/yamcs/yamcs/releases/tag/yamcs-5.12.7) | 非認証・デフォルト設定 / 宇宙インフラ利用 / CVE-2026-46621/44632 と 3 バリアント同一 fix |
| CVE-2026-46621 / [GHSA-2G95-6X5Q-XJWJ](https://github.com/advisories/GHSA-2G95-6X5Q-XJWJ) | Yamcs (org.yamcs) < 5.12.7 | CWE-94 / CRITICAL | `ChangeMissionDatabase` 権限の認証済みユーザーが REST API 経由で Jython ScriptEngine (JSR-223, サンドボックスなし) に algorithm text を送信 → JVM 上で任意 Python/Java コード実行 → RCE | [yamcs-5.12.7 リリース](https://github.com/yamcs/yamcs/releases/tag/yamcs-5.12.7) | CVE-2026-46562/44632 と共通 sink; スクリプトエンジン無サンドボックスパターンの他 OT ソフトへの水平伝播候補 |
| CVE-2026-44632 | Yamcs (org.yamcs) < 5.12.7 | CWE-94 / CRITICAL | `ChangeMissionDatabase` 権限ユーザーが `JavaExprAlgorithmExecutionFactory` に algorithm コードを注入 → Janino コンパイラが ClassFilter なしに Java バイトコードをコンパイル・実行 → RCE | [yamcs-5.12.7 リリース](https://github.com/yamcs/yamcs/releases/tag/yamcs-5.12.7) | 同一 fix で 3 バリアント同時解消；言語別スクリプトエンジン非サンドボックスの典型例 |
| CVE-2026-8398 | DAEMON Tools Lite 12.5.0.2421〜12.5.0.2434 | CWE-506 / **9.8** | TeamPCP が AVB Disc Soft 公式ビルド/配布インフラを侵害し DTHelper.exe / DiscSoftBusServiceLite.exe / DTShellHlp.exe 3 ファイルを正規署名証明書のまま trojan 化 → 正規 Web サイト経由の公式ダウンロード でマルウェア実行 | v12.6 以降で修正 [(DAEMON Tools 公式 SA)](https://supportannouncement.us.dlink.com/security/publication.aspx?name=SAP10488) | KEV ✓ (2026-05-27追加) / CVSS 9.8 / Mini Shai-Hulud キャンペーン帰属 |
| CVE-2026-35616 | FortiClient EMS 7.4.5〜7.4.6 | CWE-284 / **9.1** | REST API エンドポイントの認証・認可チェック不備 → 未認証攻撃者が特定 HTTP リクエスト 1 本で API バイパス → EMS 管理配下の全エンドポイントへ任意実行可能コードを PowerShell 経由で配布 → 全端末 EKZ Infostealer 感染 | [FortiClient EMS 7.4.7 ホットフィックス](https://www.fortiguard.com/psirt/FG-IR-26-023) (commit 非公開) | 野外悪用中・Fortinet/CISA 確認 / エンドポイント管理インフラ全体を単一の踏み台に |

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-05-28 | JVN#01719116 / CVE-2025-61669 | Jupyter Server の `LoginFormHandler._redirect_safe()` で `next` パラメーター検証が不十分 → 任意の外部ドメインへオープンリダイレクト可能；Noriaki Iwasaki (Cyber Defense Institute) が IPA に届出 | CVSS 7.4 (High) / v2.18.0 で修正 | [JVN#01719116](https://jvn.jp/en/jp/JVN01719116/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 25+（WebSearch 35+ クエリ、WebFetch 20+ 試行）
- 採用件数: AI=4 / Security=4 / CVE=5 / 国内=1
- 除外理由内訳:
  - 古すぎ (< 2026-05-27): D-Link CVE-2026-0625 (公開 2026-01-06) / GHES 3.20.3 (2026-05-26) / BadHost CVE-2026-48710 (X41 advisory 2026-05-22) / pgAdmin CVE-2026-7813 (2026-05-11) / CrewAI CVE-2026-2275/2285/2286/2287 (2026-05-07 Microsoft blog) / MemoryTrap Cisco blog (2026-04-01) / OX Security "Mother of All AI Supply Chains" (2026-04-20) / YellowKey CVE-2026-45585 (2026-05-20) / Canvas/Instructure 身代金合意 (2026-05-11) / DAEMON Tools Mini Shai-Hulud 初報 (2026-05-05/06) / OnlyFans 340M records 初報 (2026-05-25)
  - 重複 (excluded_set 直近7日): Malware-Slop npm CVE / SymJack (05-28) / Nimbus Manticore MiniFast (05-28) / Glassworm takedown (05-28) / AppOmni Marlin AI (05-28) / Varonis Atlas (05-28) / FBI Silent Ransom Group alert (05-28) / 7-Eleven breach (05-28) / Gitea CVE-2026-27771 (05-28) / LiteSpeed CVE-2026-48172 (05-25/28) / Autodesk CVEs (05-28) / dnsmasq 6 CVEs (05-28) / SGLang CVE-2026-3059/3060 (05-28) / NEC Aterm CVE-2026-8652/6059 (05-27) / KnowledgeDeliver CVE-2026-5426 (05-27) / Check Point Cloud Report (05-27) / Verizon DBIR 2026 続報 (05-27) / MFA Prompt Bombing (05-27) / SharePoint CVE-2026-45659 (05-27) / MuddyWater DLL (05-27) / TanStack CVE-2026-45321 / Nx Console CVE-2026-48027 (CISA KEV 05-27 追加だが根本事象は 05-22〜25 excluded_set 収録済みのため本文はDAEMON Toolsに絞り CVE テーブルから除外)
  - 日付不明/確認不可: Adversa AI "Top Agentic AI security resources May 2026" (推定 5/7 ≒ 3 週前) / Oracle REST Data Services 具体的 CVE ID (公式 advisory ページ 403) / OpenAI DeployCo 記事 URL 直接確認不可 (複数ニュースで 5/28 付けとして報道)
- 取得失敗ソース: oracle.com (403) / helpnetsecurity.com (403) / arcticwolf.com (403) / adversa.ai (403) / buildfastwithai.com (403) / securityaffairs.com (403) / 9to5mac.com (403) / techcrunch.com (403) / CISA.gov advisory ページ (403) / vulnerability.circl.lu (403) / digitalforensicsmagazine.com (403) / ppln.co (403) — WebSearch スニペット・複数サードパーティ記事で内容・日付を補完

</details>
