# KEDA Daily Digest — 2026-05-13 (JST)

> 採用範囲: 公開日 2026-05-11 〜 2026-05-13
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

---

## AI 関連ニュース

### OpenAI、セキュリティ特化 AI プラットフォーム「Daybreak」を発表 — GPT-5.5 で脆弱性発見・パッチ検証を自動化

- **公開日**: 2026-05-12
- **ソース**: The Hacker News / Help Net Security / Business Standard / Engadget / TechBriefly
- **要約**:
  - OpenAI は 5 月 12 日、フロンティア AI モデルと Codex Security を組み合わせたサイバーセキュリティ特化プラットフォーム「**Daybreak**」を発表した。GPT-5.5（一般公開版）・GPT-5.5 with Trusted Access for Cyber（防衛用途向け検証版）・GPT-5.5-Cyber（レッドチーミング・ペンテスト用許容版）の 3 バリアントを軸に、セキュアコードレビュー・脅威モデリング・パッチ検証・依存関係リスク分析・検知・修正ガイダンスを開発ワークフローに統合する。Akamai、Cisco、Cloudflare、CrowdStrike、Fortinet、Oracle、Palo Alto Networks、Zscaler が「Trusted Access for Cyber」イニシアチブとして既に統合中。アクセスは現在厳格に管理されており、利用希望組織は OpenAI セールスチームへの問い合わせが必要。
  - Google GTIG が 5 月 11 日に「AI 生成ゼロデイ」の野外利用を公表した翌日、OpenAI が防御側も AI を武器化する本格プラットフォームを投入した。攻撃・防御双方で AI が中心的役割を担う「AI 対 AI」の時代が到来しつつあることを象徴する動き。Anthropic の Mythos サイバーモデルとの競争が激化する。
  - GPT-5.5-Cyber は厳格な認可審査を通過した組織（ペンテスト企業・セキュリティチーム）のみが利用可能。まず自社のセキュリティ開発パイプラインに Trusted Access for Cyber レベルから導入を検討し、AI 支援コードレビューの成熟度評価を実施すること。
- **リンク**: <https://thehackernews.com/2026/05/openai-launches-daybreak-for-ai-powered.html>

---

### OpenAI、企業向け AI デプロイ専門子会社「OpenAI Deployment Company」を設立 — 40 億ドル・19 社から出資

- **公開日**: 2026-05-11
- **ソース**: OpenAI / Bloomberg / Axios / The Register / PYMNTS
- **要約**:
  - OpenAI は 5 月 11 日、企業が AI をミッションクリティカルな業務に展開するのを支援する独立子会社「**OpenAI Deployment Company（DeployCo）**」を設立した。TPG をリード投資家に Advent・Bain Capital・Brookfield を共同リードとして、Goldman Sachs・SoftBank・Warburg Pincus・Capgemini・McKinsey & Company を含む 19 社から計 40 億ドル以上を調達し、プレマネーバリュエーション 100 億ドルで発足。AI コンサルティング・エンジニアリング会社 **Tomoro を買収**（承認待ち）し、Tesco・Virgin Atlantic・Supercell などで実績を持つ約 150 名の Forward Deployed Engineers (FDE) を獲得する。
  - Palantir が確立した「FDE 型」企業 AI 展開モデルを OpenAI が本格採用。McKinsey・Bain・Capgemini が出資者に名を連ねたことで、従来「中立な導入支援者」であったコンサルが OpenAI の販売チャネルに組み込まれる構造が生まれた。Anthropic も類似の動きを進めており、2026 年は「AI 企業デプロイ競争」が主戦場となる。
  - 企業の IT・調達部門は AI 導入支援コンサルの選定にあたり、そのコンサルが OpenAI/Anthropic などベンダーから出資を受けていないか利益相反を確認すること。DeployCo との契約においては OpenAI 製品優遇の条項に注意。
- **リンク**: <https://openai.com/index/openai-launches-the-deployment-company/>

---

### IBM 調査: 76% の企業が最高 AI 責任者 (CAIO) を設置 — AI が取締役会・意思決定に浸透

- **公開日**: 2026-05-11 (CNBC 報道; IBM 一次調査は 2026-05-04)
- **ソース**: CNBC / IBM Institute for Business Value
- **要約**:
  - IBM が 33 カ国・21 産業の CEO 2,000 名超を対象に実施した調査（2026 年 2〜4 月収集）によると、CAIO（Chief AI Officer）職を設けている企業が 2025 年の 26% から **2026 年には 76% へと急増**。調査対象 CEO の 64% が「AI 生成の情報をもとに重大な戦略的意思決定を行うことに違和感がない」と回答し、AI による意思決定の自動化は 2030 年までに現在の 25% から **48%** に拡大すると予測されている。英国の Lloyds Banking Group は FTSE 上場企業初として AI ツールを取締役会に導入したことも報告された。
  - AI がビジネスの最高意思決定層にまで浸透したことで、AI ガバナンスの空洞化リスクが高まっている。CAIO の設置が形式的なものに留まり、AI 意思決定の監査・説明責任・ロールバック手順が未整備の組織が多い。
  - CAIO は「AI 推進担当」ではなく、AI リスク管理の実権を持つ役職として位置付けること。AI が生成した戦略的提言には必ず人間のレビューゲートを設け、AI 固有の偏り・エラーに対する監査体制を整備すること。
- **リンク**: <https://www.cnbc.com/2026/05/11/heres-how-artificial-intelligence-is-changing-boardrooms.html>

---

## セキュリティ関連ニュース

### [続報] Canvas/Instructure — 身代金支払いを認め、米国議会の公聴会調査へ発展

- **公開日**: 2026-05-11 (身代金支払い確認) / 2026-05-12 (議会調査報道)
- **ソース**: Inside Higher Ed / The Register / The Record from Recorded Future / CNN / Washington Post / CyberScoop
- **要約**:
  - Instructure は 5 月 12 日の最終期限直前、ShinyHunters への身代金支払い（金額非公開）を正式に認め、3.65 TB（約 2 億 7,500 万件）のデータが「シュレッドログ（削除確認ファイル）」とともに返還・消去されたと発表した。同社は「本合意はすべての Instructure 顧客を対象としており、各学校・大学が個別交渉する必要はない」と表明。一方、翌 5 月 12 日には米国下院国土安全保障委員会（House Homeland Security Committee）のアンドリュー・ガルバリーノ議員が、Instructure CEO スティーブ・ダリーを **5 月 21 日までにブリーフィング出席**するよう要請し、議会による公式調査が開始された。
  - ランサムウェアグループへの身代金支払いは「シュレッドログ」の真正性確認が困難なため、データ流通リスクは依然として残ると専門家は警告。教育機関がサイバー攻撃に対し脆弱であることを議会に印象づけ、LMS ベンダーへのサイバーセキュリティ規制強化立法が俎上に上る可能性がある。
  - Canvas 利用機関は「データ消去済み」という発表を鵜呑みにせず、法的通知義務の履行を継続すること。認証情報の使い回しがないかを学生・教職員に改めて確認させ、なりすましフィッシングへの警戒も継続すること。
- **リンク**: <https://therecord.media/instructure-pays-ransom-canvas-incident-congress-investigation>

---

### [続報] Microsoft 2026 年 5 月 Patch Tuesday 全貌判明 — CVSS 9.8 Netlogon 未認証 RCE (CVE-2026-41089) が最優先対応

- **公開日**: 2026-05-12
- **ソース**: BleepingComputer / CybersecurityNews / Tenable / Notebookcheck / Direct Business Technologies
- **要約**:
  - 5 月 12 日に正式リリースされた Microsoft Patch Tuesday は計 **120 件**の脆弱性を修正（Critical 17 件・重要 102 件・中程度 1 件）、ゼロデイの野外悪用はなかった。最優先対応案件は **CVE-2026-41089**（Windows Netlogon サービス preauthentication RCE、**CVSS 9.8**）: 未認証の攻撃者がスタックバッファオーバーフローを経由してドメインコントローラー上でコード実行が可能で、過去の Zerologon (CVE-2020-1472) に匹敵するインパクトと評価されている。他の注目 CVE は **CVE-2026-41096**（Windows DNS クライアント RCE: 攻撃者制御 DNS サーバーからの応答でメモリ破壊）、**CVE-2026-40402**（Hyper-V 権限昇格、Critical）、M365 Copilot for Desktop/Android および GitHub Copilot with Visual Studio のなりすまし・セキュリティ機能バイパス。
  - 前回 (2026-05-12 digest) に掲載した「Secure Boot 証明書更新」は引き続き重要だが、CVE-2026-41089 が独立した最高深刻度の案件として浮上した。Active Directory 環境全体が未認証 RCE に晒されるリスクがあり、NTLM Relay 等との組み合わせで連鎖的な侵害が起こりうる。Tenable はリリース直後に「最優先パッチ適用推奨」と評価。
  - **ドメインコントローラーは最優先で更新**: WSUS / Intune / SCCM 経由の展開テストを本日中に開始し、今週末までに全 DC への適用を完了すること。Hyper-V ホストも Critical 扱いで速やかに更新し、Secure Boot 証明書更新も合わせて実施すること。
- **リンク**: <https://www.bleepingcomputer.com/news/microsoft/microsoft-may-2026-patch-tuesday-fixes-120-flaws-no-zero-days/>

---

### なぜエージェント型 AI がセキュリティの次なる「盲点」となるのか — THN 分析 (2026-05-12)

- **公開日**: 2026-05-12
- **ソース**: The Hacker News / Security Boulevard
- **要約**:
  - The Hacker News が掲載した分析記事によると、エージェント型 AI（Agentic AI）はすでに多くの企業の本番環境で稼働しているにもかかわらず、セキュリティチームが関与できていないケースが大多数を占める。AI エージェントは広範な権限でデータにアクセスし、自律的に操作を実行するが、「シャドー AI」化によって既存のセキュリティコントロールの外で動作するリスクがある。Dark Reading の調査では、セキュリティ専門家の 48% が「エージェント型 AI」を 2026 年の最上位攻撃ベクターとして挙げた。非人間 ID（ノンヒューマンアイデンティティ）が人間 ID を超える規模で増殖しており、IAM・PAM の既存モデルでは管理しきれない。
  - 企業が AI エージェントを十分に理解・棚卸しできないまま急速に展開しており、ガバナンスと可視性が根本的に追い付いていない。AI エージェントが侵害されると、広範な権限を悪用した横移動や機密データ窃取が短時間で可能になる。
  - AI エージェントのインベントリ（台帳）作成を最初のステップとして実施すること。最小権限の原則を AI エージェントにも適用し、アクセスパターンの異常検知ルールを整備すること。
- **リンク**: <https://thehackernews.com/2026/05/why-agentic-ai-is-securitys-next-blind.html>

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 | 影響/CVSS | リンク |
|--------|--------|------|-----------|--------|
| 2026-05-12 | JVN#03037325: エレコム製無線 LAN ルーター・アクセスポイントに 7 CVE | JPCERT/CC が GMOサイバーセキュリティ・スズキ株式会社・福井大学・静岡大学・早稲田大学・株式会社ゼロゼロワンからの報告を調整して公開。CVE-2026-42062（認証不要の任意 OS コマンド実行）、CVE-2026-40621（特定 URL 知得者による認証なし操作）、CVE-2026-35506（ログイン済みユーザーによる OS コマンドインジェクション）、CVE-2026-25107（設定ファイル偽造）、CVE-2026-42948（管理者間 XSS）、CVE-2026-42950（CSRF による DoS）、CVE-2026-42961（CSRF による意図しない操作）の計 7 CVE。対象: WRC-XE5400GSA-G v1.13 以前 / WRC-BE72XSD-B・BA v1.1.1 以前 / WRC-BE65QSD-B v1.1.0 以前 / WRC-W702-B v1.1.0 以前 / WAB-BE187-M v1.1.10 以前 / WAB-BE72-M・BE36-M・BE36-S v1.1.3 以前。ELECOM 公式サイトよりファームウェアを更新すること。 | CVE-2026-42062: 推定 Critical（認証不要 RCE）/ CVE-2026-40621: 高 | <https://jvn.jp/jp/JVN03037325/> |
| 2026-05-11〜12 | [続報] Canvas LMS 国内教育機関影響 — Instructure が身代金支払い・データ消去を主張 | Instructure は身代金支払いとシュレッドログによる消去確認を発表。ただし消去の真正性確認は困難。国内で Canvas LMS を採用する大学・専門学校は「消去済み」を前提とせず、法的通知義務・個人情報保護委員会への報告要否を改めて確認すること。JPCERT/CC・IPA からの個別注意喚起は未確認。 | 高（個人情報漏洩継続リスク） | <https://therecord.media/instructure-pays-ransom-canvas-incident-congress-investigation> |
| 2026-05-12 | [続報] Microsoft 5 月 Patch Tuesday — CVE-2026-41089 (Netlogon RCE, CVSS 9.8) 含む 120 件修正 | Active Directory 環境への未認証 RCE は最優先対応。ドメインコントローラーへのパッチ適用を今週末までに完了し、Secure Boot 証明書更新も合わせて実施すること。 | CVSS 9.8（Critical） | <https://msrc.microsoft.com/update-guide/> |

---

## 本日のサマリ

本日の最重要トピックは **OpenAI Daybreak** の発表（5/12）。前日に Google GTIG が「AI 生成ゼロデイ」の実害を公表した翌日に、OpenAI が GPT-5.5 ベースの防御側向け AI セキュリティプラットフォームを投入し、攻防両面で AI が主役となる「AI 対 AI」の時代が本格化した。同日設立の **OpenAI Deployment Company**（$40 億・19 社出資）は McKinsey・Bain・Capgemini を出資者に迎え、AI コンサルティング市場の構造変化を引き起こしつつある。セキュリティ面では **Canvas/Instructure の身代金支払い問題**が米国議会調査に発展（5/12）。「データ消去済み」の主張は真正性確認が困難であり、国内の Canvas 利用機関を含め法的通知義務の履行を継続すること。同じく 5/12 にリリースされた **Microsoft Patch Tuesday** では CVSS 9.8 の Netlogon preauthentication RCE（CVE-2026-41089）が判明しており、AD 環境を持つすべての組織はドメインコントローラーへの即日パッチ適用が急務。国内では **ELECOM 製無線 LAN ルーター・AP に認証不要の OS コマンド実行を含む 7 CVE** が JVN で公開（5/12）。家庭・オフィス問わず該当製品のファームウェア更新を速やかに実施すること。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 35（WebSearch × 18 クエリ、WebFetch × 複数）
- 採用件数: AI=3 / Security=3 / 国内=3（テーブル形式）
- 除外理由内訳:
  - 古すぎ（採用窓外 3 日以上前）:
    - SpaceX/xAI 合併（2026-02-02）
    - Snap 1,000 名削減（2026-04-15）
    - Microsoft/OpenAI パートナーシップ改訂（2026-04-27）
    - Google Cloud Next '26 / Wiz 統合発表（2026-04-22〜23）
    - CISA/NSA エージェント型 AI ガイダンス（2026-05-01）
    - IBM CAIO 一次調査プレスリリース（2026-05-04）← CNBC の 5/11 記事は採用
    - Mandiant M-Trends 2026 レポート（2026-03）
    - Apache Tomcat 4 月多数 CVE
    - Mozilla Firefox AI オプトアウト（2026-02）
    - CVE-2026-32201 SharePoint ゼロデイ（2026-04 April Patch Tuesday）
    - Ivanti EPMM CVE-2026-6973 および CVE-2026-5786/5787/5788/7821（2026-05-07〜08）
    - ELECOM CVE-2026-22550 等（2026-02-03）
    - 中国サイバースペース AI コンパニオン規制（2025-12〜2026-01 ドラフト）
  - 重複（過去 7 日 excluded_set に既出）:
    - CVE-2026-6973 Ivanti EPMM（2026-05-06 digest 掲載）
    - CVE-2026-0300 PAN-OS GlobalProtect（過去 digest 掲載）
    - CVE-2026-31431 Copy Fail Linux（過去 digest 掲載）
    - CVE-2026-23918 Apache HTTP/2（過去 digest 掲載）
    - Canvas 初報・5/9〜12 分のポータル改ざん詳細（2026-05-11・05-12 digest 掲載）、本日は 5/11〜12 の「身代金支払い + 議会調査」新展開として採用
    - Microsoft Patch Tuesday「Secure Boot 証明書更新予告」（2026-05-12 digest 掲載）、本日は「実際の CVE 詳細（CVE-2026-41089 等）」が新規判明として [続報] 採用
    - Google GTIG AI ゼロデイ（2026-05-12 digest 掲載）
    - OpenAI EU GPT-5.5-Cyber（2026-05-12 digest 掲載）
    - Google Cloud Blog AI 脅威インテリジェンス（2026-05-12 digest 掲載）
    - ScanNetSecurity Apache HTTP Server 5/11 記事（2026-05-12 digest 掲載）
  - 日付不明・確認不可: 一部 SharkStriker 月次まとめ（特定日付不明のため除外）
- 取得失敗ソース（HTTP 403 等）:
  - thehackernews.com（WebFetch 直接）← WebSearch スニペット・サードパーティミラーで代替確認
  - bleepingcomputer.com（WebFetch 直接）
  - jvn.jp（WebFetch 直接）← WebSearch 検索結果スニペットで CVE 詳細確認
  - jpcert.or.jp（WebFetch 直接）
  - openai.com（WebFetch 直接）
  - dbtsupport.com（WebFetch 直接）
- 日付確認方法:
  - OpenAI Daybreak: helpnetsecurity.com/2026/05/12/, business-standard.com URL パターン 126051200897、techbriefly.com/2026/05/12/ で確認
  - OpenAI Deployment Company: bloomberg.com/news/articles/2026-05-11、axios.com/2026/05/11 で確認
  - Canvas 身代金支払い: insidehighered.com/…/2026/05/11 で確認; 議会調査 theregister.com/cyber-crime/2026/05/12/ で確認
  - Microsoft Patch Tuesday: bleepingcomputer.com/news/microsoft/ タイトル + notebookcheck.net 記事 "Windows 11: May 2026 Patch Tuesday is live" で 05-12 確認
  - THN Agentic AI 記事: WebSearch スニペット「10 hours ago」(収集時刻 05-12) で確認
  - JVN#03037325: elecom.co.jp/news/security/20260512-01/ の URL パターンで 05-12 確認
  - IBM/CNBC 記事: cnbc.com/2026/05/11/ URL パターンで確認; IBM newsroom は 2026-05-04 で採用窓外だが CNBC の 5/11 報道として採用

</details>
