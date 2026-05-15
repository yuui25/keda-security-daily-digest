# KEDA Daily Digest — 2026-05-16 (JST)

> 採用範囲: 公開日 2026-05-14 〜 2026-05-16
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

---

## AI 関連ニュース

### Anthropic、Claude サブスクリプション課金体系を改定 — エージェント・SDK 利用を 6 月 15 日から別予算に分離

- **公開日**: 2026-05-14
- **ソース**: The Register / Axios / InfoWorld / the-decoder.com
- **要約**:
  - Anthropic が 5 月 14 日、Claude サブスクリプションの課金体系改定を発表した。2026 年 **6 月 15 日**より、Claude チャット・公式 CLI（Claude Code）などの「第一者利用」と、Agent SDK・GitHub Actions・外部フレームワーク経由の「プログラム的利用（第三者ツール）」を**別の予算プール**に分離する。プログラム的利用の月間クレジット上限は契約プランと連動し、**Pro: $20 / Max 5x: $100 / Max 20x: $200**。上限を超えた分は**フル API 料金**で課金される。Claude Code 責任者 Boris Cherny は「キャッシュ外で動作する第三者ツールは持続不可能なコスト構造になっていた」と理由を説明した。
  - サブスク $20〜$200 を払いながら第三者自動化ツールで数百〜数千ドル分のトークンを消費するユーザーが増加したことへの対応。重量な Agentic ワークフローを外部フレームワーク（OpenClaw・LangGraph・crewAI 等）で運用している組織は 6 月 15 日以降の月次コスト増加をあらかじめ試算しておく必要がある。
  - 現在の月間 API 利用量を確認し、6 月以降のコスト試算を行うこと。上限を超える可能性が高いワークフローは、API キーを直接使用する形式に移行するか、プランのアップグレードを検討すること。公式ドキュメントおよびプラットフォームの Usage ダッシュボードで消費量の追跡が可能。
- **リンク**: <https://www.theregister.com/ai-ml/2026/05/14/anthropic-tosses-agents-into-the-api-billing-pool/5240748>

---

### Anthropic × PwC 戦略的提携を大幅拡張 — Claude Code 世界展開・3 万人 Claude 認定プログラム

- **公開日**: 2026-05-14
- **ソース**: SiliconAngle / PwC ニュースルーム / prnewswire / BusinessToday
- **要約**:
  - Anthropic と PwC が 5 月 14 日、戦略的アライアンスの大幅拡張を発表した。**Claude Code と Cowork** をまず米国チームに展開し、順次グローバルの数十万人規模の PwC 人材へ拡大。**3 万人の PwC 社員を Claude 認定**する共同トレーニングプログラムと、「**Center of Excellence**」の設立も含まれる。重点領域は (1) アジェンティック技術の内製ビルド、(2) AI ネイティブなディールメイキング、(3) 企業機能の再設計の 3 点。すでに本番稼働中のユースケースとして、プロスポーツ運営・保険引受・メインフレームモダナイゼーション・HR 変革・サイバーセキュリティがあり、一部では納期を **70% 削減**した実績が報告されている。
  - Anthropic の法人向け Claude 採用が OpenAI の ChatGPT を米国ビジネス市場で超えた（VentureBeat 報道）タイミングでの大型提携拡張。PwC の世界規模のサービス網を通じて Claude が金融サービス・医療・保険などの規制業種へ浸透するルートが確立される。競合他社（OpenAI・Gemini）の エンタープライズ展開との差別化要因として Claude Code の開発者生産性が前面に出ている。
  - Claude Code を社内展開する際は、PwC が設ける Center of Excellence の事例から学べるガバナンスモデル（権限スコープ・ログ・監査設計）を参考にすること。企業規模での Claude 認定プログラムは、内製 AI 人材育成の実績として採用・評価軸にもなりうる。
- **リンク**: <https://siliconangle.com/2026/05/14/pwc-expands-anthropic-alliance-will-train-30000-staff-claude/>

---

### Mini Shai-Hulud npm/PyPI 汚染が AI ソフトウェアサプライチェーンを直撃 — Mistral AI 450 リポジトリ流出疑い、OpenAI も社員端末 2 台が侵害

- **公開日**: 2026-05-14（Mistral AI 報道）/ 2026-05-15（OpenAI 声明・The Register）
- **ソース**: BleepingComputer / The Register / The Hacker News / cybernews / TechRadar
- **要約**:
  - **TeamPCP** と呼ばれる脅威アクターグループが「**Mini Shai-Hulud**」と名付けた大規模 npm/PyPI サプライチェーン攻撃を実施。poisoned な自動化ワークフローと窃取した公開クレデンシャルを悪用し、TanStack・Mistral AI・OpenSearch・UiPath・Guardrails AI 等の信頼されたパッケージに悪意あるバージョンを注入した。**Mistral AI** はコードベース管理システムが侵害されたことを認め、TeamPCP は約 **5GB・450 リポジトリ**（学習・ファインチューニング・ベンチマーク・推論インフラ等）を窃取したと主張し **$25,000** で売却を試み、買い手がなければ 1 週間後に無償公開すると脅迫。Mistral はホスティングサービス・ユーザーデータ・研究環境は非影響と説明。**OpenAI** は社員端末 **2 台**が同キャンペーンで感染した事実を認め、macOS デスクトップ・Codex App・Codex CLI・Atlas の**コード署名証明書を失効・更新**。旧バージョンは 2026 年 **6 月 12 日**でサポート終了となり、ユーザーに即時更新を要請した。
  - AI 系リポジトリ・推論インフラ・学習データパイプラインが npmやPyPI 経由の依存関係汚染のターゲットとして直接狙われた初の大規模事例。AI 企業のソフトウェア開発フローが従来の OSS エコシステムと深く絡み合っているため、依存関係の毒盾（ポイズニング）が AI モデルやインフラへの踏み台になりうることを実証した。
  - 社内の npm/PyPI パッケージの lock ファイルを精査し、node-ipc・TanStack 系パッケージの不審なバージョン（9.1.6, 9.2.3, 12.0.1 等）が混入していないか確認すること。OpenAI ツールを利用中の場合は最新バージョンへ即時更新すること。AI フレームワーク（Mistral 系・Guardrails AI・OpenSearch）の依存関係ハッシュ検証を CI/CD に組み込むことが急務。
- **リンク**: <https://www.bleepingcomputer.com/news/security/teampcp-hackers-advertise-mistral-ai-code-repos-for-sale/> / <https://www.theregister.com/security/2026/05/15/openai-caught-in-tanstack-npm-supply-chain-chaos-after-employee-devices-compromised/5241019>

---

## セキュリティ関連ニュース

### Pwn2Own Berlin 2026 — 2 日間で $908,750 / 39 件のゼロデイ: AI 製品も次々陥落、DEVCORE が支配

- **公開日**: 2026-05-14（Day 1）/ 2026-05-15（Day 2）
- **ソース**: Zero Day Initiative / Security Affairs / BleepingComputer / GBHackers
- **要約**:
  - **Day 1（5/14）**: 計 $523,000、24 件のユニークなゼロデイを実証。DEVCORE の Orange Tsai が Microsoft Edge でサンドボックスエスケープを含む **4 つのロジックバグを連鎖**させ $175,000・17.5 Master of Pwn ポイントを獲得。Windows 11 は 3 チームが別々のゼロデイで各 $30,000 を獲得。AI カテゴリでは k3vg3n が SSRF+コードインジェクションの連鎖で **LiteLLM** を陥落させ $40,000、NVIDIA Megatron Bridge が 2 件のゼロデイで各 $20,000、Chroma ベクターデータベースも $20,000 獲得。
  - **Day 2（5/15）**: 計 $385,750、15 件のゼロデイ。**Microsoft Exchange** に対して Orange Tsai（DEVCORE）が 3 バグ連鎖で SYSTEM 権限 RCE を実証し **$200,000** の最高賞金を獲得。AI カテゴリでは **Cursor** が $30,000（Viettel Cyber Security）と $15,000（Compass Security）の 2 件、**OpenAI Codex** が $20,000（Summoning Team の Sina Kheirkhah）のゼロデイで突破された。Red Hat Enterprise Linux も $10,000 で攻略。
  - 2 日合計: **$908,750・39 件のゼロデイ**。DEVCORE が $405,000・40.5 ポイントで首位独走。今回の Pwn2Own では初めて AI/LLM 製品が正式カテゴリとして設定され、AI インフラ（LLM フレームワーク・ベクターDB・AI コーディングエージェント・推論基盤）のゼロデイが現実に実証可能であることが確認された。AI 製品のセキュリティ成熟度が従来の OS・ブラウザと比べ低い可能性が示唆されている。
  - 組織内で LiteLLM・Cursor・OpenAI Codex などのツールを利用している場合、Pwn2Own で実証されたゼロデイのパッチが提供され次第速やかに適用すること（各ベンダーは 90 日以内にパッチを提供する義務）。AI ツールの脆弱性は従来の Web/OS と異なる攻撃面を持つため、セキュリティレビュープロセスに AI ツール固有のチェック項目を追加すること。
- **リンク**: <https://www.zerodayinitiative.com/blog/2026/5/15/pwn2own-berlin-2026-day-two-results>

---

### CVE-2026-20182「Cisco Catalyst SD-WAN Controller」認証バイパス CVSS 10.0 — UAT-8616 が積極悪用、連邦機関は 5 月 17 日期限

- **公開日**: 2026-05-15
- **ソース**: Help Net Security / The Hacker News / Rapid7 / Cisco Talos / SecurityWeek
- **要約**:
  - Cisco Catalyst SD-WAN Controller（旧 vSmart）および SD-WAN Manager（旧 vManage）のピアリング認証ロジックに欠陥（**CVE-2026-20182, CVSS 10.0 Critical**）が発見された。vdaemon サービス（DTLS/UDP 12346 番）のコネクションハンドシェイクにトラスト検証の論理バグがあり、**未認証のリモート攻撃者**がクレデンシャルなしで管理者権限を取得し、NETCONF 経由で SD-WAN ファブリック全体の設定を操作できる。Rapid7 の Jonah Burgess・Stephen Fewer が発見し Cisco に報告。2026 年内で **6 件目の Cisco SD-WAN 積極悪用ゼロデイ**となる。Cisco は脆弱性を「高度に洗練されたサイバー脅威アクター」による悪用と認定し、Cisco PSIRT および Talos の調査で **UAT-8616**（重要インフラ業種を標的とする国家支援アクターとの評価が高く、ORB ネットワークとインフラが重複）が実攻撃を行っていることを確認。CISA は 5 月 14〜15 日に KEV カタログへ追加し、連邦 FCEB 機関に **5 月 17 日までの修正を義務化**。
  - 前回の CVE-2026-20127（同 vdaemon）と同一の攻撃クラスタが繰り返し Cisco SD-WAN を標的にしており、CVE の連続開示は設計上の問題を示唆する。SD-WAN は企業ネットワークの中枢に位置するため、侵害後の横移動・設定改ざん・通信傍受のリスクが特に高い。
  - SD-WAN コントローラーの管理インターフェース（UDP 12346）をインターネットから到達可能な状態に置かないこと。Cisco のアドバイザリ（cisco-sa-sdwan-rpa2-v69WY2SW）で示された修正バージョンへ即時アップグレードすること。侵害痕跡（SSH 鍵の追加・NETCONF 設定変更・不審なログイン）を調査すること。
- **リンク**: <https://www.helpnetsecurity.com/2026/05/15/cisco-sd-wan-zero-day-cve-2026-20182/>

---

### CVE-2026-8181「WordPress Burst Statistics」認証バイパス CVSS 9.8 — 20 万サイトで実攻撃、7,400 件超をブロック確認

- **公開日**: 2026-05-14
- **ソース**: BleepingComputer / Wordfence / WPScan / CyberPress / managed-wp.com
- **要約**:
  - プライバシー重視の WordPress アナリティクスプラグイン「**Burst Statistics**」（Google Analytics 代替として約 20 万サイトで利用）に認証バイパス脆弱性（**CVE-2026-8181, CVSS 9.8 Critical**）が発見された。バージョン 3.4.0〜3.4.1.1 の `is_mainwp_authenticated()` 関数が Authorization ヘッダーのアプリパスワード検証で誤った戻り値処理を行うため、管理者ユーザー名を知る未認証攻撃者がランダムなパスワードを指定するだけで REST API リクエスト中に管理者を偽装できる。さらに不正な管理者アカウントの作成も可能。脆弱性は 4 月 23 日リリースの v3.4.0 で導入され、Wordfence が 5 月 8 日に発見。修正版 **v3.4.2** が 5 月 12 日に提供済み。5 月 14 日時点で Wordfence が **7,400 件超の攻撃をブロック**し実攻撃の進行を確認。
  - 20 万規模の WordPress サイトで実攻撃が始まっており、管理者権限奪取後はバックドア設置・コンテンツ改ざん・マルウェア配布・フィッシングリダイレクトに直結するリスクがある。Burst Statistics はロリポップ・さくら等の日本のレンタルサーバー環境でも広く利用されており、国内ユーザーも注意が必要。
  - WordPress サイト管理者は **v3.4.2 以上**への即時アップグレードを行うこと。アクセスログを確認し `/wp-json/` への不審な REST API アクセス（特に `mainwp` 関連パス）を調査すること。管理者アカウント一覧を確認し、心当たりのないアカウントが作成されていないかチェックすること。
- **リンク**: <https://www.bleepingcomputer.com/news/security/hackers-exploit-auth-bypass-flaw-in-burst-statistics-wordpress-plugin/>

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 | 影響/CVSS | リンク |
|--------|--------|------|-----------|--------|
| 2026-05-14 | **JVN#14434132: WPS Office 2 名前付きパイプのアクセス制御不備** | Kingsoft 製「WPS Office 2」（2020 版 v11.2.0.10707 以前・2025 版 v11.2.0.10715 以前）において、バックグラウンドサービス間通信用の名前付きパイプに適切な ACL が設定されていない。非管理者ユーザーが対象パイプへアクセスし**任意のプログラムを SYSTEM 権限で実行**可能。WPS Office 2 は国内販売の PC に**プリインストールされていることがある**ため、アプリを積極利用していない場合もインストール有無を確認する必要がある。修正版は開発者サイト（Kingsoft）から提供済み。LAC WATCH でも 5/15 に注意喚起を掲載。 | CVSS v4.0 **8.5（High）** | [JVN#14434132](https://jvn.jp/jp/JVN14434132/) |
| 2026-05-14〜15 | **CVE-2026-20182 Cisco Catalyst SD-WAN 認証バイパス — 国内 SD-WAN 基盤への影響** | セキュリティ関連ニュース参照。国内の通信事業者・ISP・大手製造業・金融機関で Cisco SD-WAN を利用している場合は直ちにアドバイザリを確認し修正版へのアップグレードを行うこと。CISA の 5/17 期限は連邦機関向けだが、UAT-8616 は重要インフラを広域で標的にしており国内組織も安全と見なすべきではない。 | CVSS **10.0 (Critical)** 実攻撃確認済み | [Help Net Security](https://www.helpnetsecurity.com/2026/05/15/cisco-sd-wan-zero-day-cve-2026-20182/) |

---

## 本日のサマリ

**緊急対応筆頭は Cisco Catalyst SD-WAN CVE-2026-20182（CVSS 10.0、5/17 期限）**: 国家支援とされる UAT-8616 がリモート未認証で管理者権限を取得できる最高深刻度バグを実攻撃中であり、SD-WAN 運用組織は即日対応が必要。次点は **WordPress Burst Statistics CVE-2026-8181（CVSS 9.8）**: 20 万サイトを対象に 7,400 件超の攻撃が既に進行中で、v3.4.2 への更新と管理者アカウント棚卸しを急ぐこと。**AI サプライチェーン攻撃** では Mini Shai-Hulud キャンペーンが Mistral AI・OpenAI・TanStack を同時に巻き込み、AI 企業の開発基盤が OSS エコシステムの依存関係汚染によって現実に侵害されることが証明された。**Pwn2Own Berlin 2026** では 2 日間で $908K・39 ゼロデイが実証され、LiteLLM・Cursor・OpenAI Codex・NVIDIA Megatron Bridge といった AI 製品が初めて公式カテゴリとして設定された競技で軒並み陥落しており、AI ツールのセキュリティ成熟度への懸念が高まっている。Anthropic は課金体系改定（6/15 施行）と PwC との大型提携拡張で商用展開を加速させており、エンタープライズ AI の主軸として Claude のポジションがさらに固まりつつある。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 50（WebSearch × 16 クエリ、WebFetch 複数試行）
- 採用件数: AI=3 / Security=3 / 国内=2（テーブル形式）
- 除外理由内訳:
  - 古すぎ（採用窓外: 公開日 2026-05-14 未満）:
    - Apache HTTP Server JVNVU#99705957（2026-05-08 公開）
    - Exposed AI Services スキャン記事（2026-05-05 公開）
    - AI-built 2FA bypass zero-day Google GTIG（2026-05-11 公開）
    - Dell CVE-2026-22769 CISA 3-day（2026-02-19 公開）
    - Gemini Omni leak（2026-05-02 リーク）
    - OpenAI smartphone 開発報道（日付未確定）
    - SpaceX/xAI merger（日付未確定）
    - Anthropic "dreaming" technique（日付未確定）
  - 重複（過去 7 日 excluded_set に既出）:
    - Gemini Spark (05-15 digest 掲載済み)
    - Anthropic Claude blackmail experiment / Teaching Claude Why (05-15 digest 掲載済み)
    - Taiwan AI warning (05-15 digest 掲載済み)
    - Foxconn Nitrogen ransomware (05-15 digest 掲載済み)
    - CVE-2026-46300 Fragnesia (05-15 digest 掲載済み)
    - CVE-2026-42945 NGINX Rift (05-15 digest 掲載済み)
    - Fortinet CVE-2026-26083/44277 (05-15 digest 掲載済み)
    - PraisonAI CVE-2026-44338 (05-15 digest 掲載済み)
    - Google Android Show / Gemini Intelligence (05-14 digest 掲載済み)
    - Android Intrusion Logging (05-14 digest 掲載済み)
    - Palo Alto AI攻撃警告 (05-14 digest 掲載済み)
    - Anthropic $30B 調達 (05-14 digest 掲載済み)
    - CVE-2026-45185 Exim Dead.Letter (05-14 digest 掲載済み)
    - YellowKey / GreenPlasma PoC (05-14 digest 掲載済み)
    - SAP CVE-2026-34263/34260 (05-14 digest 掲載済み)
    - RubyGems GemStuffer (05-14 digest 掲載済み)
    - GUARDIANWALL / KDDI / Bytello JVN (05-14 digest 掲載済み)
    - OpenAI Daybreak (05-13 digest 掲載済み)
    - CVE-2026-31431 Copy Fail KEV (05-09/10 digest 掲載済み)
  - 日付不明・採用窓外: OpenAI smartphone、SpaceX/xAI merger、Anthropic dreaming（URL/日付未確定）
- 取得失敗ソース（HTTP 403 等）:
  - thehackernews.com（WebFetch 直接）
  - bleepingcomputer.com（WebFetch 直接）
  - jvn.jp（WebFetch 直接）
  - siliconangle.com（WebFetch 直接）
  - helpnetsecurity.com（WebFetch 直接）
  - zerodayinitiative.com（WebFetch 直接）
  - securityaffairs.com（WebFetch 直接）
  → 全て WebSearch スニペット・ミラーサイト URL パターンで公開日を代替確認
- 日付確認方法:
  - Anthropic billing: theregister.com URL /ai-ml/2026/05/14/ で確認
  - Anthropic PwC: siliconangle.com URL /2026/05/14/ で確認
  - Mistral AI TeamPCP: BleepingComputer 検索結果スニペット「May 14, 2026, BleepingComputer reported」で確認
  - OpenAI TanStack: theregister.com URL /security/2026/05/15/ で確認
  - Pwn2Own Day 1: ZDI schedule /blog/2026/5/13/ + event date May 14 で確認
  - Pwn2Own Day 2: ZDI URL /blog/2026/5/15/ で確認
  - Cisco SD-WAN: helpnetsecurity.com URL /2026/05/15/ + SecurityWeek で確認
  - WordPress Burst Statistics: managed-wp.com URL /cve20268181-2026-05-14 で確認
  - WPS Office JVN: JVN 検索結果「2026年5月14日12:00」公開で確認、LAC WATCH 5/15 掲載で裏取り

</details>
