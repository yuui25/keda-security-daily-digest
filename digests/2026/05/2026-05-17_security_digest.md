# KEDA Daily Digest — 2026-05-17 (JST)

> 採用範囲: 公開日 2026-05-15 〜 2026-05-17
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

---

## AI 関連ニュース

### OpenAI、ChatGPT にサードパーティ「Apps」エコシステムを開放 — Zillow・Canva・Spotify が ChatGPT 内で直接起動、Apps SDK も Preview 公開

- **公開日**: 2026-05-15
- **ソース**: OpenAI / VentureBeat / The Verge / Releasebot
- **要約**:
  - OpenAI が 5 月 15 日、新世代の「**Apps in ChatGPT**」を発表した。開発者向け **Apps SDK**（preview）を公開し、サードパーティが ChatGPT のインターフェース内で直接起動・実行されるアプリを構築できるようになる。ローンチパートナーには Zillow・Canva・Spotify をはじめとする著名サービスが参加しており、OpenAI は同日、デベロッパーがアプリを登録できる **ChatGPT App Directory** の受付も開始した。ユーザーはチャット会話内でアプリを呼び出し、外部ページに遷移することなくタスクを完結させることができる。
  - 単なる AI アシスタントから「**AI ネイティブなアプリ配布プラットフォーム**」への転換は、Apple App Store / Google Play Store と同様の市場構造変化を意味する。Anthropic・Google・Microsoft もそれぞれのエコシステム構想を持っており、ChatGPT プラットフォームの先行開放は AI アシスタント間の「プラットフォーム化競争」を一段と加速させる。
  - 社内で使用している SaaS が ChatGPT Apps として提供される場合、業務データが OpenAI 環境に流入するリスクが生じる。Apps 連携時の OAuth スコープ・データ保持ポリシー・ログ取得設定を事前に精査すること。情報セキュリティポリシーに「ChatGPT Apps を通じた業務データの処理可否」を明記しておくこと。
- **リンク**: <https://openai.com/index/introducing-apps-in-chatgpt/>

---

### OpenAI、ChatGPT Pro に「パーソナルファイナンス」機能を追加 — Plaid 経由で 1.2 万金融機関を接続、GPT-5.5 が家計推論を担う

- **公開日**: 2026-05-15
- **ソース**: TechCrunch / MacRumors / OpenAI / SiliconAngle
- **要約**:
  - OpenAI が 5 月 15 日、米国の ChatGPT Pro サブスクライバー向けにパーソナルファイナンス機能を **preview** で公開した。金融インフラ企業 **Plaid** と連携し、Chase・Fidelity・Schwab・Robinhood・American Express・Capital One を含む **1.2 万以上の金融機関**への銀行口座接続が可能。サイドバーの「Finances」から接続を開始し、ポートフォリオパフォーマンス・支出カテゴリ分析・サブスクリプション一覧・今後の支払い予測・家計 Q&A など多彩な機能を提供する。金融特化ベンチマークに向けてチューニングされた **GPT-5.5** が推論を担い、4 月に OpenAI が買収した個人財務スタートアップ **Hiro** のチームが開発した。Web および iOS で提供中。
  - AI が個人の金融資産データ全体へアクセスする設計は、データ侵害時の被害拡大（資産情報・口座番号・取引履歴の一括流出）という新たなリスク面を生む。オープンバンキング同様、接続アカウントの権限スコープ（読み取り専用の確認）と異常通知の設定が重要になる。
  - 企業の BYOD・情報セキュリティポリシーに「個人財務系 AI ツールへの業務デバイスからのアクセス禁止」の規定追加を検討すること。金融・保険業の組織では、個人情報保護法・金融規制との整合性も確認が必要。Pro ユーザー以外への展開は今後予定されており、早期の内部ルール整備が求められる。
- **リンク**: <https://techcrunch.com/2026/05/15/openai-launches-chatgpt-for-personal-finance-will-let-you-connect-bank-accounts/>

---

### OpenClaw「Claw Chain」— 世界最速成長 AI エージェント基盤に連鎖可能な 4 CVE、24.5 万台のサーバーが無防備に露出

- **公開日**: 2026-05-15
- **ソース**: The Hacker News / Cyera Research Blog / The Next Web / Dark Reading / IBM X-Force
- **要約**:
  - セキュリティ研究者 Vladimir Tokarev（Cyera）が、急速に普及する オープンソース AI エージェントオーケストレーション基盤「**OpenClaw**」に 4 件の脆弱性を発見し、**5 月 15 日に開示**した。4 件は組み合わせて悪用すると「**Claw Chain**（爪の連鎖）」攻撃を完成させ、データ窃取・権限昇格・持続的バックドア設置を実現する。
    - **CVE-2026-44112**（CVSS **9.6**）: OpenShell マネージドサンドボックスの TOCTOU 競合条件。マウントルート外への任意書き込みが可能で、バックドア埋め込みや設定改ざんに悪用される。
    - **CVE-2026-44115**（CVSS **8.8**）: unquoted heredoc 内で環境変数が展開される問題。バリデーションをすり抜けたコマンドが機密情報を外部へ返す。
    - **CVE-2026-44118**（CVSS **7.8**）: クライアント制御の `senderIsOwner` フラグが認証セッションとクロスチェックされないため、有効ベアラートークンを持つローカルプロセスがオーナーレベルの制御権限を取得できる。
    - **CVE-2026-44113**（CVSS **7.7**）: 読み取り操作における同様の TOCTOU パターン。シンボリックリンクへのスワップでマウントルート外のファイルを読み取り可能。
  - Shodan・ZoomEye のスキャンでは、公開アクセス可能な OpenClaw インスタンスが世界に約 **24.5 万台**（Shodan: 6.5 万 / ZoomEye: 18 万）存在することが確認された。特に金融・ヘルスケア・法律分野での PII/PHI 処理ワークフローがリスクに晒されている。AI エージェント基盤のセキュリティ検証が未成熟なまま本番展開が進む業界全体の課題を浮き彫りにした事例。
  - **即時対応**: OpenClaw を **v2026.4.22** 以降にアップグレードし、サービスを再起動すること。インターネット公開インスタンスは VPN 配下またはファイアウォールで制限すること。金融・医療・法律データを処理するエージェントワークフローはアクセスログを精査し、不審なファイルパスアクセス・設定変更の痕跡を調査すること。
- **リンク**: <https://thehackernews.com/2026/05/four-openclaw-flaws-enable-data-theft.html> / <https://www.cyera.com/blog/claw-chain-cyera-research-unveil-four-chainable-vulnerabilities-in-openclaw>

---

## セキュリティ関連ニュース

### CVE-2026-42897「Microsoft Exchange Server ゼロデイ XSS」— CISA KEV 登録（5/15）、現在パッチ未提供・EEMS 自動緩和措置のみ

- **公開日**: 2026-05-15
- **ソース**: Help Net Security / The Hacker News / SecurityWeek / Microsoft Community Hub / BleepingComputer
- **要約**:
  - Microsoft が 5 月 15 日、オンプレミス版 Exchange Server に実攻撃で悪用されているゼロデイ脆弱性（**CVE-2026-42897, CVSS 8.1**）を公表した。Outlook Web Access（OWA）の XSS バグに起因するスプーフィング脆弱性で、攻撃者が**細工されたメール**をターゲットに送信し、ユーザーが OWA でそのメールを開いた際に任意の JavaScript をブラウザ上で実行させる。攻撃成立にはある程度のユーザーインタラクションが必要だが、フィッシングメールとの組み合わせで現実的な経路となる。影響を受けるのは **Exchange Server 2016・2019・Subscription Edition (SE)** のオンプレ版のみで、Exchange Online は非影響。5 月 12 日の Patch Tuesday（138 件修正）から 3 日後という異例の早さでゼロデイとして浮上した。**CISA が 5 月 15 日付で KEV カタログへ追加**し、連邦 FCEB 機関への修正期限を **5 月 29 日**に設定した。恒久パッチはまだ提供されておらず、**Exchange Emergency Mitigation Service（EEMS）**が 2016・2019・SE のオンプレ版に**緩和措置（M2.1.x）を自動適用**している。エアギャップ環境では Exchange on-premises Mitigation Tool（EOMT）の手動実行が必要。
  - 現在 EEMS 有効環境には自動緩和が展開済みだが、緩和適用後に **OWA のカレンダー印刷機能が動作しなくなる副作用**（スクリーンショットか Outlook デスクトップクライアントで代替）と、**インライン画像が受信者 OWA で表示されない副作用**があるため、ヘルプデスクへの問い合わせ急増に備えること。恒久パッチ未提供のまま実攻撃が確認されており、5 月 29 日の期限前にパッチが出た場合は即時適用が必要。
  - EEMS が有効になっているか確認し（`Get-WebServicesVirtualDirectory` + Exchange 管理センターのメンテナンス履歴確認）、エアギャップ環境では EOMT を手動実行すること。Exchange のアクセスログ・IIS ログを調査し、不審な JavaScript 実行のシグナル（異常なリクエストペイロード、外部ドメインへの意図しない通信）を確認すること。フィッシングメールとの組み合わせ攻撃に備え、エンドユーザーへの注意喚起を実施すること。
- **リンク**: <https://www.helpnetsecurity.com/2026/05/15/exchange-server-cve-2026-42897-exploited/> / <https://thehackernews.com/2026/05/on-prem-microsoft-exchange-server-cve.html>

---

### [続報] Pwn2Own Berlin 2026 Day 3 + Master of Pwn 最終結果 — 3 日間で $1,298,250・47 ゼロデイ、DEVCORE が $505K 圧勝

- **公開日**: 2026-05-16（ZDI）
- **ソース**: Zero Day Initiative / BleepingComputer / Winbuzzer / Notebookcheck
- **要約**:
  - Pwn2Own Berlin 2026 が 5 月 16 日（Day 3）をもって閉幕した。3 日間の最終集計は**賞金総額 $1,298,250・47 件のユニークなゼロデイ**（Day 1: $523K/24 件、Day 2: $385.75K/15 件、Day 3: $389.5K/8 件）となり、歴代最大規模の一つとなった。**Master of Pwn**は DEVCORE（Orange Tsai らの Taiwan ベースチーム）が**50.5 ポイント・$505,000** を獲得して圧倒的に優勝。STARLabs SG（25 pt・$242,500）が 2 位、Out Of Bounds（12.75 pt・$95,750）が 3 位。**Day 3 の主要結果**:  
    - **VMware ESXi（STARLabs SG・Nguyen Hoang Thach）**: メモリ破壊バグで ESXi をテナント間クロスコード実行の add-on 付きで突破し **$200,000・20 pt**（本大会最大の単一賞金）
    - **Microsoft SharePoint（DEVCORE・splitline）**: 2 バグ連鎖で RCE を実証し **$100,000・10 pt**
    - 他、Windows 11 や AI カテゴリでの追加実証あり
  - Day 1-2（既報）で LiteLLM・OpenAI Codex・Cursor・NVIDIA Megatron Bridge・Microsoft Exchange・Red Hat Enterprise Linux が陥落したのに続き、Day 3 では VMware ESXi と SharePoint が巨額賞金と共に突破された。ベンダーは今後 90 日以内にパッチを提供する義務があり、AI 製品から エンタープライズ インフラまで広範な修正リリースが続く見込み。
  - 今大会で開示された 47 件のゼロデイのパッチを優先監視すること。VMware ESXi のクロステナント RCE・Exchange の SYSTEM 権限 RCE・SharePoint RCE は特に影響範囲が広く、ベンダーが緊急パッチを発行した場合は即日適用する体制を整えておくこと。AI ツール（LiteLLM・Cursor・OpenAI Codex）についても Pwn2Own で実証された攻撃パスへのパッチを優先追跡すること。
- **リンク**: <https://www.thezdi.com/blog/2026/5/16/pwn2own-berlin-2026-day-three-results-and-master-of-pwn>

---

### ロシア国家支援 Turla が Kazuar バックドアをモジュラー P2P ボットネットへ進化させた — Kernel / Bridge / Worker の 3 層構造で長期潜伏

- **公開日**: 2026-05-14（Microsoft Security Blog）/ 2026-05-16（BleepingComputer・THN）
- **ソース**: BleepingComputer / The Hacker News / Microsoft Threat Intelligence Blog / GBHackers
- **要約**:
  - Microsoft Threat Intelligence が 5 月 14 日に公表した分析「**Kazuar: Anatomy of a nation-state botnet**」を BleepingComputer 等が 5 月 16 日に詳報した。ロシア FSB の **Center 16** に関連付けられる APT グループ **Turla（別名: Secret Blizzard）**が、長年使用してきたカスタムバックドア **Kazuar** をモジュラーな **P2P ボットネット**に刷新したことが判明した。新アーキテクチャは 3 種のモジュールで構成される:
    - **Kernel モジュール**: 侵害ホストへの永続的アクセスを維持するコア。既存の Kazuar バックドア機能に相当。
    - **Bridge モジュール**: 他の侵害ノードとの P2P 通信チャネルを確立し、中央 C2 サーバーなしで指令を中継。ネットワーク検知を回避する分散アーキテクチャを実現。
    - **Worker モジュール**: 偵察・データ収集・横移動などの実作業を行うコンポーネント。任意のスクリプトやプラグインを動的にロード可能。
  - P2P 方式の C2 通信により、従来のドメイン・IP ブロックが効かなくなる。CISA は Turla を FSB Center 16 に高い信頼度で紐付けており、重要インフラ・政府機関・防衛産業への標的型攻撃が主要ターゲット。単一ノード除去でボットネット全体が失われない設計は、TTPs の高度化を示す。
  - Turla が主要ターゲットとする政府・防衛・エネルギー・通信インフラを運用する組織は、**永続的 Kernel モジュールの検知**に向けてエンドポイント防御ルールを見直すこと。通常の C2 ブラックリストが機能しにくいことを前提に、ネットワーク行動分析（NTA）でピアツーピア通信パターンを検知する仕組みを導入すること。Microsoft の IoC 情報を SIEM・EDR に追加すること。
- **リンク**: <https://www.bleepingcomputer.com/news/security/russian-hackers-turn-kazuar-backdoor-into-modular-p2p-botnet/> / <https://www.microsoft.com/en-us/security/blog/2026/05/14/kazuar-anatomy-of-a-nation-state-botnet/>

---

### WordPress「Funnel Builder（FunnelKit）」の XSS — WooCommerce チェックアウトにクレジットカードスキマーを注入、4 万サイト以上で実攻撃中

- **公開日**: 2026-05-16
- **ソース**: BleepingComputer / The Hacker News / SC Media
- **要約**:
  - WooCommerce 向け人気プラグイン「**Funnel Builder（FunnelKit）**」に未認証の蓄積型 XSS 脆弱性が発見され、実攻撃が確認された。同プラグインはチェックアウトフロー・ランディングページ・アップセルを構築する機能を提供し、**4 万以上のストア**で利用されている。攻撃者はプラグインの「**Settings > Checkout > External Scripts**」設定に細工した JavaScript（Google Tag Manager（GTM）ローダーに偽装）を注入し、すべてのチェックアウトページで決済情報を窃取するスキマーを展開する。スキマーは**クレジットカード番号・CVV・有効期限・請求先住所・その他の個人情報**をリモートサーバーへ送信する。バージョン **3.15.0.3 未満**が影響を受け、修正版 **v3.15.0.3** は 5 月 15 日にリリース済み。CVE 番号は未割り当て。
  - 認証不要で外部スクリプト設定を操作できる設計上の欠陥が直接的な原因。Magecart 型の決済スキマー攻撃は EC サイトにおける PCI DSS 違反リスクを直接もたらし、カード情報流出が発覚した場合のブランド毀損・賠償リスクが高い。
  - **Funnel Builder を v3.15.0.3 以上に即時アップデート**すること。[Settings > Checkout > External Scripts] を確認し、見覚えのないスクリプト（偽 GTM 等）を即座に削除すること。WooCommerce ストアの注文データと顧客の決済情報が侵害されていないか調査し、疑いがある場合は関係者への通知とカード会社への連絡を行うこと。
- **リンク**: <https://www.bleepingcomputer.com/news/security/funnel-builder-wordpress-plugin-bug-exploited-to-steal-credit-cards/>

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 | 影響/CVSS | リンク |
|--------|--------|------|-----------|--------|
| 2026-05-15 | **CVE-2026-42897 Microsoft Exchange Server ゼロデイ — 国内オンプレ Exchange 組織への影響** | セキュリティ関連ニュース欄に詳細。国内の中堅・大企業・官公庁で広く使用されているオンプレ版 Exchange Server（2016/2019/SE）が対象。CISA の修正期限（5/29）は連邦機関向けだが、実攻撃が進行中であるため国内組織も同等の緊急度で対処が必要。EEMS を有効化している場合は自動緩和済みだが、エアギャップ環境は手動対応が不可欠。JPCERT/CC による国内向け注意喚起の発出が見込まれる。 | CVSS **8.1（High）** 実攻撃確認済み CISA KEV | [Help Net Security](https://www.helpnetsecurity.com/2026/05/15/exchange-server-cve-2026-42897-exploited/) |
| 2026-05-15 | **JPCERT/CC「インターネット定点観測レポート（2026年 1〜3月期）」公開** | JPCERT/CC が運用する TSUBAME インターネット定点観測システムの 2026 年第 1 四半期（1〜3月）レポートが 5 月 15 日に公開された。2026 年初頭の日本国内向けポートスキャン・不審アクセスの傾向を示す一次データとして、SOC・セキュリティ担当者は早期のトレンド確認が推奨される。これまでの四半期では SSH ブルートフォース・SIP スキャン・IoT ポートへの探索が増加傾向にあり、2026 Q1 データも同様の傾向継続が見込まれる。 | 情報・参考 | [JPCERT/CC TSUBAME](https://www.jpcert.or.jp/tsubame/report/) |

---

## 本日のサマリ

**今週末の最優先対応は Microsoft Exchange CVE-2026-42897（CVSS 8.1、5/15 CISA KEV 登録）**: オンプレ版 Exchange Server（2016/2019/SE）に対して XSS を利用した実攻撃が進行しており、EEMS 有効環境への自動緩和措置が既に展開されているが、エアギャップ環境やエアギャップに近い組織は EOMT の手動適用が急務。恒久パッチが提供され次第（期限 5/29 目安）即日適用する体制を取ること。**Pwn2Own Berlin 2026** が 3 日間の全日程を終了し、$1.3M・47 ゼロデイ という歴代規模で閉幕した。VMware ESXi（$200K）・SharePoint（$100K）・Exchange（$200K）・AI 製品（LiteLLM・Cursor・Codex 等）の計 47 件のパッチを優先監視し、ベンダーが緊急対応を発行した際は即時適用すること。**ロシア国家支援 Turla の Kazuar P2P ボットネット化**は、C2 インフラのブロックが実質不可能になることを示しており、重要インフラ・政府関連組織はネットワーク行動分析による検知強化が急務。AI 領域では **OpenAI が ChatGPT 上でサードパーティアプリ（Apps SDK）と金融口座連携（Plaid）を同日公開**しており、企業の ChatGPT 利用ポリシーに「データ流入リスクのある拡張機能へのアクセス可否」を早急に定義する必要がある。**OpenClaw Claw Chain（CVE-2026-44112 等 4 件）** により AI エージェント基盤の 24.5 万台がインターネット上に無防備に露出していることが確認された。OpenClaw v2026.4.22 への更新と公開インスタンスのネットワーク隔離を優先実施のこと。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 55（WebSearch × 28 クエリ、WebFetch 複数試行）
- 採用件数: AI=3 / Security=4 / 国内=2（テーブル形式）
- 除外理由内訳:
  - 古すぎ（採用窓外: 公開日 2026-05-15 未満）:
    - Anthropic Gates Foundation $200M パートナーシップ（2026-05-14 公開）
    - Akamai 社 LayerX 買収（$205M）（プレスリリース 2026-05-14 公開）
    - Claude Code v2.1.141 リリース（2026-05-13〜14）
    - Anthropic Claude for Small Business（2026-05-13）
    - Anthropic reinstates OpenClaw / VentureBeat（2026-05-13）
    - Palo Alto Networks「Defender's Guide May 2026 Update」（2026-05-13）
    - Signal security warnings（Help Net Security 2026-05-13）
    - TrickMo Android banker TON blockchain（2026-05-11〜12）
    - Mira Murati Thinking Machines interaction models（TechCrunch 2026-05-11、MarkTechPost 2026-05-13）
    - Turla Kazuar Microsoft Security Blog（primary source: 2026-05-14）※BleepingComputer 2026-05-16 報道版を採用
    - Verizon DBIR 2026（2026-05-01〜02 リリース）
    - OpenAI Codex モバイル「work from anywhere」（initial disclosure 2026-05-14）
    - Google Gemini Omni リーク（初出: 2026-05-02 UI 発見）
    - Meta Muse Spark（2026-04-08 公開）
    - NASA AI space chip（ScienceDaily 2026-05-15 だが AI ニュース優先度低）
  - 重複（過去 7 日 excluded_set に既出）:
    - Anthropic 課金体系改定（2026-05-16 digest 掲載済み）
    - Anthropic × PwC 提携拡張（2026-05-16 digest 掲載済み）
    - Mini Shai-Hulud npm/PyPI / Mistral AI / OpenAI TanStack（2026-05-16 digest 掲載済み）
    - Pwn2Own Day 1・Day 2（2026-05-16 digest 掲載済み、Day 3 は [続報] として採用）
    - Cisco SD-WAN CVE-2026-20182（2026-05-16 digest 掲載済み）
    - WordPress Burst Statistics CVE-2026-8181（2026-05-16 digest 掲載済み）
    - Foxconn Nitrogen ランサムウェア（2026-05-15 digest 掲載済み）
    - CVE-2026-46300 Fragnesia / CVE-2026-42945 NGINX Rift（2026-05-15 digest 掲載済み）
    - Fortinet CVE-2026-26083 / 44277（2026-05-15 digest 掲載済み）
    - PraisonAI CVE-2026-44338（2026-05-15 digest 掲載済み）
    - Gemini Spark（2026-05-15 digest 掲載済み）
    - Anthropic Teaching Claude Why（2026-05-15 digest 掲載済み）
    - Taiwan AI warning（2026-05-15 digest 掲載済み）
    - WPS Office JVN#14434132（2026-05-16 digest 掲載済み）
    - GUARDIANWALL / KDDI / Bytello JVN（2026-05-14 digest 掲載済み）
    - ELECOM JVN#03037325（2026-05-13 digest 掲載済み）
  - 日付不明・確認不能:
    - OpenAI raises additional capital（PYMNTS 記事日付確認できず）
    - Google Chrome Gemini integration（I/O 2026 以前の具体的公開日不確定）
  - WebFetch 403 で直接アクセス不可（WebSearch スニペット・ミラー URL で公開日を代替確認）:
    - thezdi.com（403）→ BleepingComputer・Winbuzzer の ZDI引用記事で日付確認
    - helpnetsecurity.com（403）→ URL パターン /2026/05/15/ で確認
    - thenextweb.com（403）→ 検索スニペット「1 day ago from May 16」で確認
    - bleepingcomputer.com（403）→ フィード metadata / ミラー URL で日付確認
    - sources.news（403）→ 内容のみ参照、日付未確認のため未採用
    - esecurityplanet.com（403）
- 日付確認方法（採用記事）:
  - OpenAI Apps in ChatGPT: 検索スニペット「On May 15, 2026, OpenAI announced」+ releasebot.io/updates/openai 確認
  - ChatGPT Personal Finance: techcrunch.com URL /2026/05/15/ + macrumors.com /2026/05/15/ 確認
  - OpenClaw Claw Chain: thehackernews.com 検索スニペット「1 day ago」（from May 16 検索時）= 2026-05-15
  - CVE-2026-42897 Exchange: helpnetsecurity.com URL /2026/05/15/ + CISA alert /2026/05/15/ 確認
  - Pwn2Own Day 3: thezdi.com URL /blog/2026/5/16/ で確認
  - Turla Kazuar BleepingComputer: フィード metadata「published on May 16, 2026 at 10:15:37 AM」
  - WordPress Funnel Builder: BleepingComputer May 16 feed 掲載確認 + 記事内「released yesterday（= May 15）」でパッチ日確認
  - JPCERT TSUBAME: 検索結果「JPCERT/CC released...Internet Observation Report on May 15, 2026」確認

</details>
