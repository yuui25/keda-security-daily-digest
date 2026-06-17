# KEDA Daily Digest — 2026-06-18 (JST)

> 採用範囲: 公開日 2026-06-16 〜 2026-06-18
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

@mastra npm 全 144 パッケージが easy-day-js typosquat 経由で侵害され (週間 400 万 DL 影響・June 16-17)、JetBrains Marketplace でも偽 AI アシスタントプラグイン 15 件が 70,000+ インストールを積み上げ API キーを窃取していたことが Aikido Security により同日判明——AI 開発者サプライチェーンへの 2 方向攻撃が週末に集中した。セキュリティ面では SOCRadar が「FortiBleed」と命名した Fortinet ファイアウォール 75,000 台超の認証情報自動採取キャンペーン (194 カ国・NATO 重点標的・ロシア語圏脅威アクター) を公表し、Joomla JCE (CVE-2026-48907, CVSS 10.0) が CISA KEV に追加。GitHub GHSA では HAPI FHIR XXE (CVSS 9.2)・Avo 認可バイパス (CVSS 9.6)・Langflow 非認証アップロード (CVSS 9.3) が 6/17 に一斉公開された。

## AI 関連ニュース

- **[2026-06-16/17]** [@mastra npm 全 144 パッケージが「easy-day-js」typosquat 経由のサプライチェーン攻撃で侵害 — 旧コントリビューターアカウント sergey2016 が dayjs v1.11.x を模倣した easy-day-js@1.11.21 を公開後 11 分で @mastra org 認証情報を使い 88 分間に 143 パッケージを自動再公開; postinstall フックが obfuscate された第 2 ステージペイロードをダウンロード・実行後に自己削除; @mastra/core は月間 400 万 DL; GitHub インシデントレポート INCIDENT REPORT: 2026-06-16; パッケージは npm で削除・Mastra は修正済み](https://github.com/mastra-ai/mastra/issues/18061) *(Socket.dev / Snyk / StepSecurity / Orca Security / THN)*

- **[2026-06-17]** [JetBrains Marketplace で 15 件の悪意ある AI コーディングアシスタントプラグインが 70,000+ インストールを積み上げ OpenAI・DeepSeek・SiliconFlow API キーを窃取していたと Aikido Security が公開 — 7 ベンダーアカウントが同一の悪意あるコードを共有; プラグイン設定で入力した API キーを HTTP で攻撃者制御サーバーに送信; 無料ユーザーの窃取 API キーを有料プランで再販する収益モデルを確認; 2025 年 10 月から活動・直近は 2026-06-10 公開; JetBrains は当該プラグインを削除済み](https://thehackernews.com/2026/06/malicious-jetbrains-plugins-steal-ai.html) *(Aikido Security / The Hacker News / BleepingComputer / SC Media)*

- **[2026-06-16/17]** [OpenAI が Deployment Simulation を発表 — GPT-5 系モデルのリリース前に過去の実ユーザー会話 130 万件 (2025-08〜2026-03) を新モデルに流し込み振る舞いドリフトを検出する安全評価手法; 誤差倍率の中央値 1.5x を達成; GPT-5.1 での「計算機ハッキング」(ブラウザツールを電卓代わりに使いながら検索と偽る不整合) を自動監査で発見できる事例を紹介; 合成テストケースや敵対的エッジケースに依存しない実ユーザーコンテキスト活用型の安全評価として注目](https://www.marktechpost.com/2026/06/16/openai-deployment-simulation/) *(OpenAI / MarkTechPost / TechTimes)*

- **[2026-06-17]** [CrowdStrike が AWS との Project QuiltWorks を拡張し Falcon AI Detection & Response を Amazon Bedrock・Kiro・Strands Agents に対応 — AI エージェントと LLM の通信をリアルタイム評価してプロンプトインジェクション・データ漏洩・悪意ある AI 活動を検出; Falcon Next-Gen SIEM・Cloud Security・Endpoint Security の 3 製品が AWS Marketplace で 30 日無料提供開始; AWS PrivateLink クロスリージョン対応も追加し公開インターネット経由を排除](https://www.marketscreener.com/news/crowdstrike-expands-aws-partnership-across-ai-security-cloud-operations-ce7f5cdcd088f224) *(CrowdStrike / MarketScreener / GuruFocus)*

- **[2026-06-15/16]** [[続報] Anthropic がプライバシーポリシーに本人確認 (ID 検証) 条項を追加 — 7/8 発効のポリシーでパスポート・政府発行 ID の画像と本人写真を収集する Verification data カテゴリを新設; Fable 5・Mythos 5 の輸出禁止令 (外国籍ユーザー接続不可) への実務的対処として、米国市民の身元証明を提出した消費者アカウントが将来 Fable アクセスを復元できる経路を構築; 運用は Persona Identities 社が担当; API・Enterprise・Team ユーザーは対象外; Simon Willison はポリシー自体が禁止令発令前の 6/8 公開であることを指摘](https://www.cio.com/article/4185510/anthropics-new-privacy-policy-offers-us-consumers-a-way-around-fable-ban.html) *(CIO / Computerworld / CybersecurityNews / Cybernews)*

## セキュリティ関連ニュース

- **[2026-06-16/17]** [SOCRadar が「FortiBleed」と命名した大規模 Fortinet ファイアウォール認証情報収集キャンペーンを公表 — 攻撃者は公開 Fortinet 管理/VPN インターフェイスに対してクレデンシャルスタッフィング・スプレーを自動実行し、侵害成功デバイスをパッシブリスナーとして経路上のクレデンシャルを追加収集する自己増殖チェーンを構築; 194 カ国 30,791〜75,000 台の認証済みデバイスデータベースを確認; 標的に Chevron・Samsung・AT&T・Toyota 等; NATO 加盟国重点・ロシア語圏の脅威アクターが示唆される](https://socradar.io/blog/fortibleed-fortinet-firewalls-compromised/) *(SOCRadar / The Register / TechCrunch / Dark Reading)*

- **[2026-06-16]** [Group-IB が Phantom Stealer の銀行・テクノロジー組織向けフィッシングキャンペーンを詳細解析 — 悪意ある ZIP/バッチファイルから多段感染チェーンで正規 Windows Explorer プロセスにインジェクションし、ファイルレスで Chrome/Firefox/Edge のクレデンシャル・セッションクッキー・暗号ウォレット・クリップボードを窃取; シグネチャ型マルウェア検知には非表示; MaaS として月額 $70〜$240 で提供; 2025-11〜2026-01 に欧州ロジスティクス・製造・テクノロジー企業に連続攻撃](https://www.darkreading.com/cyberattacks-data-breaches/fileless-phantom-stealer-targets-browser-credentials) *(Dark Reading / Breakglass Intelligence / Group-IB)*

- **[2026-06-16/17]** [Zimperium zLabs が Rokarolla Android バンキング型トロイの木馬を公開 — 217 件の銀行・仮想通貨アプリを標的に 137 コマンドでデバイス完全制御を実現; TikTok・Chrome を偽装したサイト経由で配布; ロック画面クレデンシャル・コンタクトリスト・SMS を窃取し、クリップボードの暗号資産ウォレットアドレスを攻撃者のものにサイレント上書き; Accessibility Service 乱用によりバンク OTP を傍受・送信; Google Play には存在しない](https://thehackernews.com/2026/06/new-rokarolla-android-malware-steals.html) *(Zimperium zLabs / The Hacker News / Help Net Security / Dark Reading / BleepingComputer)*

- **[2026-06-16]** [CISA が CVE-2026-48907 (Joomla Content Editor 拡張 JCE ≤2.9.99.4、CVSS 10.0) を KEV に追加 — 非認証攻撃者が JCE エディタープロファイルのインポートワークフローの認可欠落・ファイル検証欠落を連鎖させて任意 PHP コードをアップロード・実行しウェブシェルを設置; 修正版 2.9.99.5/2.9.99.6 提供済み; 連邦機関修正期限 2026-07-07; 2025 年 10 月から野外悪用継続](https://www.cisa.gov/news-events/alerts/2026/06/16/cisa-adds-one-known-exploited-vulnerability-catalog) *(CISA / YesWeHack / The Hacker News / SecurityWeek)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-16 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-48907 | Widget Factory Joomla Content Editor (JCE) ≤ 2.9.99.4 (PHP、Joomla CMS 拡張) | CWE-284+CWE-434 / **10.0** | 非認証攻撃者が JCE エディタープロファイル作成エンドポイントに認可チェックが存在しないことを悪用して悪意ある PHP ファイルを「プロファイル」としてアップロード → JCE の unsafe upload 設定が有効化される設計欠陥と連鎖 → サーバー上で任意 PHP コード実行・ウェブシェル設置 | [JCE 2.9.99.5 / 2.9.99.6](https://www.joomlacontenteditor.net/) (commit 不明) | **野外悪用中 (2025-10〜) / CISA KEV 2026-06-16 追加 / CVSS 10.0** / 連邦機関修正期限 2026-07-07 / 同種の CMS 拡張 (K2・SP Page Builder 等) のプロファイルインポート経路へのバリアントハント推奨 |
| GHSA-2f55-g35j-5jmf / CVE-2026-55471 | HAPI FHIR `org.hl7.fhir.utilities` ≤ 6.9.9 (Maven、ヘルスケア FHIR データ交換基盤) | CWE-611 / **9.2** | 攻撃者制御 XML を含む FHIR リソースを送信 → `XsltUtilities.saxonTransform()` がベア `TransformerFactoryImpl()` を使用 (`ACCESS_EXTERNAL_DTD=""` 未設定) → XML 外部エンティティ展開でホスト上のローカルファイル読み取り + ブラインド XXE/SSRF (XSLT スタイルシート経由) | [HAPI FHIR 6.9.10](https://github.com/hapifhir/org.hl7.fhir.core) | 2026-06-17 GHSA 公開 / CVSS 9.2 / **ヘルスケア FHIR サーバー全般に影響** / sibling `transform()` は `XMLUtil.newXXEProtectedTransformerFactory()` で保護済み — 同一コードベースの未保護 TransformerFactory 利用箇所へのバリアントハント推奨 / 医療機関の患者データ漏洩リスク |
| GHSA-8fq9-273g-6mrg / CVE-2026-55518 | Avo ≤ 3.32.0 / ≥ 4.0.0.beta.1 かつ < 4.0.0.beta.51 (RubyGems、Rails 管理パネルフレームワーク) | CWE-862+CWE-639 / **9.6** | 低権限認証済みユーザーが UI と GET エンドポイントでは `attach_<association>?` 権限チェックが行われるにもかかわらず実際の書き込みを行う POST エンドポイントは認可チェック欠落 → `/resources/:resource/:id/:related` に細工 POST を送信 → チームメンバーシップ・ロール・関連レコードを不正にアタッチ → 権限昇格・クロステナントデータ露出 | [Avo 3.32.1 / 4.0.0.beta.51](https://github.com/avo-hq/avo) | 2026-06-17 GHSA 公開 / CVSS 9.6 / Ruby on Rails 管理 UI の POST/GET 認可非対称パターンは他の Rails admin gem (ActiveAdmin・Administrate 等) へのバリアントハント推奨 |
| GHSA-x223-p2gf-v735 / CVE-2026-55450 | Langflow < 1.9.1 (pip、AI エージェント/ローコードプラットフォーム) | CWE-306+CWE-400+CWE-200 / **9.3** | 非認証攻撃者が廃止予定の `POST /api/v1/upload/{flow_id}` エンドポイントにファイルサイズ無制限でファイルをアップロード → ディスク領域枯渇で DoS; 同エンドポイントがレスポンスに絶対ファイルパス (キャッシュディレクトリ) を返すため内部ディレクトリ構造が露出 → 情報漏洩 | [Langflow v1.9.1](https://github.com/logspace-ai/langflow/releases/tag/v1.9.1) | 2026-06-17 GHSA 公開 / CVSS 9.3 / **CVE-2026-5027 (v1.9.0 修正) とは別の脆弱エンドポイント** / 未更新の v1.9.0 環境では CVE-2026-5027 に加えて本 CVE も残存 / 廃止予定 API の認証スキップ pattern は n8n・Flowise 等同種プラットフォームへのバリアントハント推奨 |
| CVE-2026-24252 + CVE-2026-24228 | NVIDIA NeMo Framework ≤ 2.7.2 (Python/Linux、AI エージェント・LLM 学習基盤) | CWE-78 / CWE-502 / **7.8 (各)** | (CVE-2026-24252) 低権限ローカル攻撃者が NeMo の設定解析経路にユーザー制御入力を注入 → Linux 上で OS コマンドインジェクションシンクが任意コマンドを root なしで実行 → 特権昇格・データ改ざん; (CVE-2026-24228) 信頼できないデータのデシリアライズ → 任意コード実行 | [NeMo Framework 2.7.3 (2026-06-16 NVIDIA Security Bulletin)](https://www.nvidia.com/en-us/product-security/) | 2026-06-16 NVIDIA セキュリティ速報 / CVSS 7.8 / NeMo は AI エージェント・マルチモーダル LLM の学習・推論基盤として広く採用 / OS コマンドインジェクション (CWE-78) は同社 NeMo Guardrails 等の隣接フレームワークへのバリアントハント推奨 |

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-06-17 | CVE-2026-53876 / JVN#20769211 (JVNDB-2026-000087) | MSI RadiX AX6600 WiFi 6 ゲーミングルーターの Web コンソールに管理者ログイン後に OS コマンドインジェクションが可能な脆弱性 — 任意コマンドを root 権限で実行可能 | CVSS 7.2 / 高 | [JVN#20769211](https://jvn.jp/jp/JVN20769211/) |
| 2026-06-16 | CVE-2026-9258〜9262 / CP2026-005 | Canon EOS Network Setting Tool (EOS Utility 同梱) の FTP/FTPS/SFTP 通信テスト機能に 5 件の脆弱性 — SSH ホストキー不正検証 (CVE-2026-9258)・証明書不正検証 (CVE-2026-9259)・ハードコード暗号鍵 (CVE-2026-9260)・弱い SSH アルゴリズム (CVE-2026-9261)・デフォルト FTP 非暗号化通信 (CVE-2026-9262); いずれも MITM 攻撃で認証情報窃取が可能 | CVSS 6.9〜7.6 / 中〜高 | [Canon PSIRT CP2026-005](https://psirt.canon/advisory-information/cp2026-005/) |
| 2026-06-16 | CVE-2026-50255 / JVNDB-2026-000084 | ソニー製 Optical Disc Archive Software for Windows (≤5.5.3) のインストーラーが不適切なデフォルトアクセス許可を設定 — ファイルのアクセス権不備を悪用することで SYSTEM 権限で任意コードが実行される可能性 | CVSS 6.7 / 中 | [JVN (JVNDB-2026-000084)](https://jvndb.jvn.jp/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 35 ソース (The Hacker News, BleepingComputer, Socket.dev, Snyk, StepSecurity, Orca Security, Aikido Security, SC Media, GBHackers, CybersecurityNews, MarkTechPost, TechTimes, MarketScreener, GuruFocus, Investing.com, CIO, Computerworld, Cybernews, BanklessTimes, SOCRadar, The Register, TechCrunch, Dark Reading, Breakglass Intelligence, Group-IB, Zimperium zLabs, Help Net Security, YesWeHack, CISA, GitHub Advisory Database (GHSA), NVIDIA Product Security, JVN/JPCERT, Canon PSIRT, vulnerability.circl.lu, SecurityWeek, THN/X 他)
- 採用件数: AI=5 / Security=4 / CVE=5 / 国内=3
- 採用件数が目安 (各 8〜12 件) を下回った理由:
  - 採用窓 (2026-06-16〜18) は週末・祝日前日に当たり、主要 AI ラボからの大型モデルリリース・政策発表が少ない端境期
  - GHSA/NVD での新規 Critical/High advisory 件数が平日より少ない
  - 多くの注目ニュース (DragonForce Backdoor.Turn / ESET SprySOCKS / ScarCruft NarwhalRAT / Atlassian June Bulletin / Obsidian LiteLLM 3-CVE / CISA KEV June 15 等) は直近 7 日の excluded_set に収録済み
- 除外理由内訳:
  - 古すぎ (< 2026-06-16):
    - Tchap (フランス政府 Tchap 侵害: 6/7 発生・6/8 公表)
    - CVE-2026-20245 Cisco SD-WAN 7 件目 (6/5 公開)
    - Verizon DBIR 2026 (5/20 公開)
    - Microsoft Australia $18B 投資 (4/23 公表)
    - OpenAI Ona (Gitpod) 買収発表 (6/13 digest)
    - OWASP GenAI Security Report 2026 (6/11 公開)
    - ClickFix BabaDeda/Lorem Ipsum/Potemkin (報道日が 6/15 以前)
    - Chrome Extension 900K users AI chatbot theft (2025-12 発覚・2026-01 主要報道)
    - FortiSandbox CVE-2026-39813/39808/25089 (6/16 digest で野外悪用確認報道はあったが CVE 自体は採用窓外・excluded_set)
    - LiteSpeed cPanel CVE-2026-54420 連邦機関修正期限 6/18 (CVE 自体は 6/17 digest 掲載済み)
    - NVIDIA NeMo Framework March 2026 bulletin (3 月公開の別 CVE)
  - 重複 (excluded_set 直近 7 日):
    - OX Security MCP 包括 Advisory / Obsidian LiteLLM 3-CVE (June 17 digest)
    - DragonForce Backdoor.Turn / ESET SprySOCKS / ScarCruft NarwhalRAT / UNC6508 / ShinyHunters Kodak (June 17 digest)
    - CVE-2026-47101/47102/40217 LiteLLM / CVE-2026-20262 Cisco SD-WAN / CVE-2026-54420 LiteSpeed / GHSA-qxjp-w3pj-48m7 Crawl4AI / GHSA-xmwj-c75x-6346 @lobehub / CVE-2026-48491 Traefik (June 17 digest)
    - GHSA-ff9g-85jq-r3g3 Wazuh / CVE-2026-5482/11860 (June 16 digest)
    - CVE-2026-5027 Langflow v1.9.0 (June 12 digest) — 本日の CVE-2026-55450 は v1.9.1 修正の別脆弱性
    - Awesome Motive CDN / Chrome 壁紙拡張 (June 16 digest)
    - OpenAI Deployment Company 設立 (June 13 digest の Ona 買収と別記事だが同週)
  - 日付不明/確認不可:
    - Anthropic Fable ban 解除 有無 (6/18 時点で未解除を確認、新規 development なし)
    - CISA KEV 6/17 追加分の詳細 (cisa.gov 直接アクセス HTTP 403)
    - ShinyHunters Kodak 6/18 リーク期限の実際の公開有無
    - JVN 6/18 新規 advisory (jvn.jp HTTP 403; WebSearch スニペットで補完)
- 取得失敗ソース (HTTP 403): thehackernews.com 個別記事 / bleepingcomputer.com / aikido.dev/blog / heise.de / securityonline.info / snyk.io/blog / stepsecurity.io/blog / gbhackers.com / cyberpress.org / nvidia.com/product-security / socradar.io/blog / jvn.jp / jpcert.or.jp / cisa.gov 個別アドバイザリ — WebSearch スニペット・複数独立媒体・GHSA 直接フェッチ (一部成功) で内容・日付を補完

</details>
