# KEDA Daily Digest — 2026-06-03 (JST)

> 採用範囲: 公開日 2026-06-01 〜 2026-06-03
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Microsoft Build 2026 (6/2–3、San Francisco) で GitHub Copilot の独自モデル **Project Polaris** 発表・Windows Agent Framework 1.0 MIT 公開・Foundry Local GA など AI エージェントプラットフォーム化が加速し、米 DoD との $9.69B 統合契約も同時に明らかになった。セキュリティ面では **Google Android June 2026** パッチ (CVE-2025-48595 野外悪用、124 件修正) の公開と、中国 APT "Dragon Weave" が **Azure Blob Storage を C2 デッドドロップ** として悪用しチェコ・台湾の政府機関を標的にしていることが公表された。また Nightmare Eclipse 研究者への Microsoft 法的脅迫問題が MSRC の撤回声明で一区切りを迎え、AI 時代の責任ある開示をめぐる論争が加速している。

---

## AI 関連ニュース

- **[2026-06-02]** [Microsoft Build 2026: GitHub Copilot が独自 AI コーディングモデル Project Polaris に移行 — 8月より GPT-4 Turbo を置き換え](https://www.techtimes.com/articles/317596/20260602/github-copilot-replaces-gpt-4-project-polaris-ships-multi-agent-vs-code-build.htm) — MoE アーキテクチャで HumanEval/MBPP でも GPT-4 Turbo を上回り、Rust・Haskell 等低リソース言語で特に性能向上；VS Code でマルチエージェント統合も同日 GA *(Microsoft Build / TechTimes)*

- **[2026-06-02]** [Microsoft Build 2026: Windows Agent Framework 1.0 を MIT ライセンスで OSS 公開、Azure Agent Mesh も発表](https://news.microsoft.com/build-2026/) — .NET/Python SDK でマルチエージェントシステムを構築し、Azure Agent Mesh がオンプレ・Azure・エッジへのフェデレーション実行を単一 API で提供 *(Microsoft)*

- **[2026-06-02]** [Microsoft Build 2026: Foundry Local GA — Windows/macOS(Apple Silicon)/Linux x64 でオフライン AI 推論・エージェント実行が可能に](https://www.buildfastwithai.com/blogs/ai-news-today-june-2-2026) — データをデバイス外に送出せず、ネットワーク遅延なしでエージェントを本番稼働；機密環境での AI 利用に道 *(Microsoft Build / buildfastwithai)*

- **[2026-06-02]** [米 DoD が Microsoft 365/Azure/AI Copilot の企業統合契約 $9.69B を締結 — Build 2026 で発表](https://www.buildfastwithai.com/blogs/ai-news-today-june-2-2026) — 従来の分散ベンダー調達比 $422M 削減を見込む；政府機関での Copilot 大規模展開が加速、AI サプライチェーンリスクの評価が急務 *(DoD / Microsoft Build)*

- **[2026-06-02]** [OpenAI が Rosalind Biodefense プログラムを発表 — 生物防衛・パンデミック対策開発者に最高性能モデルへの特別アクセスを提供](https://www.buildfastwithai.com/blogs/ai-news-today-june-2-2026) — 信頼済み研究機関・政府向け新カテゴリとして設立；高リスクドメインへの AI 適用ガバナンスモデルの先例 *(OpenAI)*

- **[2026-06-01]** [OpenAI が Trusted Access for Cyber (TAC) プログラムで最高権限モデルへのパスキー義務化 — Yubico と提携しフィッシング耐性認証をデフォルトに](https://openai.com/index/advanced-account-security/) — Advanced Account Security (AAS) でパスワード・SMS 回復を無効化し、ハードウェアバックドパスキーまたは FIDO セキュリティキーを必須化；エージェントや機密コードベースへのアクセスに新基準 *(OpenAI / Help Net Security)*

- **[2026-06-01]** [Hathaway/Schneier 論説「AI 時代の責任ある脆弱性開示」公開 — フロンティア AI の自律ゼロデイ発見能力が既存90日ルールを無力化すると主張、緊急改革を提言](https://www.schneier.com/blog/archives/2026/06/vulnerability-disclosure-in-the-age-of-ai.html) — Claude Mythos/OpenAI Daybreak 等が人間の介在なしに exploit まで生成できる時代に、開示タイムラインの再定義・政府調整機能の強化を訴求 *(Schneier on Security)*

---

## セキュリティ関連ニュース

- **[2026-06-02]** [Microsoft が Nightmare Eclipse 研究者への法的脅迫を撤回 — MSRC「研究者を訴えない」声明で業界批判に応答](https://www.theregister.com/security/2026/06/02/microsoft-reaches-for-olive-branch-after-public-dustup-with-0-day-researcher/5249945) — 研究者 "Chaotic Eclipse" が BlueHammer (CVE-2026-33825)/RedSun/YellowKey (CVE-2026-45585)/GreenPlasma/UnDefend/MiniPlasma の 6 件を断続開示；Microsoft が GitHub アカウント削除・刑事訴追示唆後、業界批判が沸騰し最終的に撤回 *(The Register / Schneier on Security)*

- **[2026-06-02]** [Google が Android June 2026 セキュリティパッチを公開 — 124 件修正、CVE-2025-48595 (Android Framework LPE) が限定的野外悪用](https://www.bleepingcomputer.com/news/security/google-fixes-one-actively-exploited-android-zero-day-124-flaws/) — CVE-2025-48595 は Android 14–16 の Framework 整数オーバーフロー、ユーザー操作不要でローカル権限昇格；パッチレベル 2026-06-01 以降で修正 *(BleepingComputer / Help Net Security)*

- **[2026-06-01]** [Operation Dragon Weave: 中国関連 APT が Azure Blob Storage を C2 デッドドロップとして悪用 — チェコ・台湾の政府・学術・金融機関を標的](https://thehackernews.com/2026/06/china-aligned-groups-ramp-up-attacks.html) — Rust ローダー経由で AdaptixC2 または Cobalt Strike を配信；Azure の正規ドメインを C2 チャネルに使うことで従来の IP ブロックを回避、カンボジア・韓国への波及も確認 *(Seqrite / The Hacker News)*

- **[2026-06-01]** [WP Maps Pro CVE-2026-8732 が積極悪用 — 15,000 サイトへの認証不要管理者アカウント作成攻撃が24時間で3,600件超](https://thehackernews.com/2026/06/critical-wp-maps-pro-flaw-actively.html) — 公式サポート用「一時アクセス」AJAX エンドポイントのナンス値がフロントエンドに公開露出；v6.1.1 で修正済みだが未更新サイトが多数 *(The Hacker News / BleepingComputer)*

- **[2026-06-02]** [California AG が 23andMe(現 Chrome Holding) を提訴 — 2023年遺伝情報漏洩でカリフォルニア州民 855,541 件の CCPA・GIPA 等違反](https://www.insurancejournal.com/news/west/2026/06/02/872084.htm) — 既知の脆弱性対応怠慢・侵害通知の虚偽記載を指摘；遺伝データ保護を巡る法的執行の強化事例として注目 *(Insurance Journal / CBS SF)*

- **[2026-06-02]** [複数ランサムウェアグループが6/2 に7組織の侵害を公表 — DragonForce/Qilin/Play/SafePay/INC_RANSOM が医療・カジノ・物流を横断攻撃](https://www.breachsense.com/breaches/) — DragonForce: Taos Mountain Casino (米)・Synex Group (スリランカ)、Qilin: Clínica Maitenes (チリ)、Play: Digitall Graphics (カナダ)・Hightower Communications、SafePay: LCNet (独)、INC_RANSOM: Champaign-Urbana 公衆衛生 *(BreachSense)*

- **[2026-06-01]** [WEF・Schneier が相次いで AI セキュリティ論評公表 — 「2026年は exploit が patch より先に届く時代」と各社が認定](https://www.schneier.com/blog/archives/2026/06/microsoft-threatening-security-researcher.html) — Mandiant M-Trends 2026 によれば CVE 公開後 24時間以内の悪用が 28.3%、平均修正所要日数は74日。AI 駆動の攻撃加速が統計的に証明 *(Schneier / WEF)*

- **[2026-06-02]** [ICO が「AI 利用サイバー攻撃への5ステップ防衛策」を英国組織向けに通達 — フィッシング・ソーシャルエンジニアリングの AI 強化版に対応](https://www.lewissilkin.com/insights/2026/06/02/ai-powered-cyber-threats-ico-shares-5-practical-steps-to-strengthen-your-organis-102mtv6) — UK データ保護規制当局が GDPR Article 32 の「適切な技術的措置」としての AI 脅威対策を初めて明文化；欧州規制ガイダンスの波及が見込まれる *(ICO / Lewis Silkin)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-01 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2025-48595 | Android 14/15/16/16-qpr2 | CWE-190 / High | Android Framework API の整数オーバーフロー → 非特権アプリがユーザー操作なしにローカル特権昇格 | [Android 2026-06-01 Bulletin](https://source.android.com/docs/security/bulletin/2026/2026-06-01) | **野外悪用中 (限定的)** |
| CVE-2026-9311 | IBM WebSphere Application Server v9.0 / v8.5 | CWE-284 / **9.0** | セキュリティ制御バイパス → 認証済みリモート攻撃者が任意コード実行 (RCE) | [IBM Support #7274733](https://www.ibm.com/support/pages/node/7274733) (commit不明) | CVSS 9.0 |
| CVE-2026-9330 | IBM WebSphere Application Server v9.0 / v8.5 | CWE-502 / **8.5** | SAML Web SSO コンポーネントがデシリアライズ時にガジェットチェーンを無検証で許可 → 細工 HTTP リクエストで RCE | [IBM Support #7274738](https://www.ibm.com/support/pages/node/7274738) (commit不明) | CVSS 8.5 / Java デシリアリゼーション典型 sink |
| CVE-2026-47406 | praisonai-platform (pip、バージョン詳細確認中) | CWE-321 / Critical | PLATFORM_ENV 未設定時に JWT 署名鍵が "dev-secret-change-me" にハードコード → 任意ユーザーのトークン偽造・管理者権限取得 | [GitHub Advisory DB](https://github.com/advisories) (commit不明) | AI エージェント基盤・ハードコードキー / Flowise CVE-2026-40933 と同一設計欠陥クラス |
| CVE-2026-47408 | praisonai-platform (pip、バージョン詳細確認中) | CWE-306 / Critical | 公式 A2A サンプルエンドポイントが認証なしで LLM 駆動の `eval()` ツール実行に到達可能 → 非認証 RCE | [GitHub Advisory DB](https://github.com/advisories) (commit不明) | AI フレームワーク特有の unauth eval() 欠陥 / A2A プロトコル他実装へのバリアントハント推奨 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|

> 直近2日間に該当する新規ニュースは確認できませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約25ソース (Microsoft Build, OpenAI, Schneier, THN, BleepingComputer, SecurityWeek, CISA, Seqrite, Help Net Security, NVD, GitHub Advisory, BreachSense, Android AOSP, ICO, Mandiant 他)
- 採用件数: AI=7 / Security=8 / CVE=5 / 国内=0
- 除外理由内訳: 古すぎ(< 2026-06-01)=19件以上 / 重複=8件 / 日付不明=3件
- 取得失敗ソース: NVD直接フェッチ (403)、HKCert (403)、JPCERT/IPA直接フェッチ (403)、The Register (403)、Help Net Security (403)、Arctic Wolf (403)
- 除外済み主要 CVE: CVE-2026-41089 (Netlogon, 前日) / CVE-2026-38221 (CIFSwitch, 前日) / CVE-2026-47418 (PraisonAI, 前日) / CVE-2026-41091/45498 (Defender, 前日) / CVE-2026-8732 (WP Maps Pro, 公開日5/29 = 採用窓外) / CVE-2026-0257 (PAN-OS, 6/1已収録)
- 除外済み主要ニュース: Dutch Asocks botnet (5/29) / NGINX CVE-2026-42945 (5月) / Copy Fail CVE-2026-31431 (4/29) / EchoLeak CVE-2025-32711 (2025年) / BlueHammer CVE-2026-33825 (4月) / Microsoft RAMPART (5/20) / Ghost CMS CVE-2026-26980 (5/7悪用)
- 注意: CVE-2026-47406/47408 は GitHub Advisory の metadata が "recently published (within 13h)" を示唆しており 2026-06-02–03 付近の公開と推定; 正確な公開日は Advisory ページ403のため未確認

</details>
