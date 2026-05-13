# KEDA Daily Digest — 2026-05-14 (JST)

> 採用範囲: 公開日 2026-05-12 〜 2026-05-14
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

---

## AI 関連ニュース

### Google、Android OS を AI 基盤に再構築 — Gemini Intelligence を中核とした「The Android Show: I/O Edition」

- **公開日**: 2026-05-12
- **ソース**: Google Blog / TechCrunch / Business Standard / Engadget
- **要約**:
  - Google が 5 月 12 日に Google I/O 本番（5/19〜20）の1週間前イベント「The Android Show: I/O Edition」を開催し、Android OS を「OS からインテリジェンスシステムへ」移行する「**Gemini Intelligence**」を発表。Gemini が画面上の情報を読み取り、Gmail 横断・予約・ショッピングカート作成など多ステップのアプリ自動化を実行する。Chrome for Android に auto-browse 機能（DoorDash など外部サービスの代行注文を含む）、Android Auto でのハンズフリー Gemini、Gemini Intelligence 専用設計ラップトップ「Googlebook」も発表された。
  - Android OS レベルで AI エージェントが常時稼働する構造になることで、**プロンプトインジェクション保護**が急務に。Google は AISeal with pKVM / Private Compute Core / Private AI Compute という3層のハードウェア/ソフトウェア分離を実装し、Gemini Intelligence 動作中は通知バーにアイコン表示と AI Privacy Dashboard（過去 24 時間のアプリアクセス履歴）による透明性確保を行う。
  - アプリ開発者・企業 IT は Android 上の AI エージェントが既存アプリの権限スコープを越えてアクセスしないよう、Gemini Intelligence 向けの OAuth スコープと API 連携設計を今から見直すこと。5 月 19〜20 日の Google I/O 本番でより詳細な開発者向け仕様が開示される見込み。
- **リンク**: <https://blog.google/products-and-platforms/platforms/android/android-show-io-edition-2026/>

---

### Google、Android に AI スパイウェア検知機能「Intrusion Logging」導入 — Amnesty International と共同開発

- **公開日**: 2026-05-12
- **ソース**: TechCrunch / The Hacker News / CyberScoop / Amnesty International Security Lab
- **要約**:
  - Google が Android Advanced Protection Mode に「**Intrusion Logging**」をオプトインで追加した。デバイスのロック/アンロック履歴・アプリインストール/削除・接続先サーバー・ADB 接続・ログ削除試行などを記録し、**E2E 暗号化で 12 ヶ月間保存**。Google も国家機関もデータにアクセス不可。主な対象ユーザーはジャーナリスト・人権活動家・内部告発者・政治的反体制活動家など高リスク層。Amnesty International Security Lab は同日に「Android Intrusion Logging as a new source of data for consensual forensic analysis」を公開し、同機能が商用スパイウェア（Pegasus 等）の事後調査に有効と論じた。
  - 商用スパイウェアベンダーは端末への侵入痕跡を消去するケースが多かったが、削除試行自体もログに残るため、従来の法医学的分析の盲点を埋める画期的な設計。国家レベルの監視リスクに晒される人物への支援ツールとして世界的に注目されている。
  - Intrusion Logging は Android 16 December update 以降のデバイスで展開開始。高リスクユーザーを支援する組織（NGO・報道機関・法律事務所）はデバイス配付ポリシーに同機能の有効化を組み込むこと。
- **リンク**: <https://techcrunch.com/2026/05/12/google-launches-new-android-security-feature-to-help-uncover-spyware-attacks/>

---

### Palo Alto Networks が警告: Claude Mythos・GPT-5.5-Cyber が「数週間で 85 件のバグ発見」— AI 主導エクスプロイトが新常態化まで「3〜5 ヶ月の猶予」

- **公開日**: 2026-05-13
- **ソース**: CNBC / Axios
- **要約**:
  - Palo Alto Networks 技術最高責任者 Lee Klarich が CNBC・Axios へ「組織が敵より先手を打てる猶予は**わずか 3〜5 ヶ月**」と警告。社内テストで Claude Mythos と GPT-5.5-Cyber を組み合わせると**数週間で 85 件のバグを発見**し、動作可能なエクスプロイト生成成功率は **70% 超**。複数の脆弱性を連鎖させた exploit chain の自動生成も実現しており、従来の AI モデルでは困難だった「チェーン攻撃の自動化」が現実となった。Anthropic は Mythos の提供を PANW・CrowdStrike・Amazon・Apple・JPMorgan などの選定組織に限定している。
  - 「AI が脆弱性を発見し攻撃する時代」が研究段階から実運用段階に入ったことを、セキュリティ最前線の企業が数値で裏付けた。Google GTIG が AI 生成ゼロデイを野外で確認した（5/11 報道）直後のタイミングの警告であり、防御側の緊張感が急速に高まっている。
  - 推奨は 4 点: (1) パッチ前の自社脆弱性発見能力の構築、(2) インターネット露出の最小化、(3) リアルタイム自動検知・防御の展開、(4) SOC への AI 統合による機械速での対応。中小規模の組織でも「AI 攻撃を前提とした」脅威モデルへの更新が急務。
- **リンク**: <https://www.cnbc.com/2026/05/13/palo-alto-ai-cyberattacks-mythos-gpt.html>

---

### Anthropic、評価額 9,000 億ドルで 300 億ドルの資金調達を交渉中 — Bloomberg 独占報道

- **公開日**: 2026-05-12
- **ソース**: Bloomberg
- **要約**:
  - Bloomberg が 5 月 12 日、Anthropic が投資家と新ラウンドで**最低 300 億ドル**の調達を協議中と報道（評価額 9,000 億ドル以上）。ラウンドは今月末にもクローズ見込みだが、タームシートはまだ未署名の段階。直近の run-rate 収益は **300 億ドル超**（2025 年末比約 3.3 倍）で急増している。Google が 2026 年 4 月に評価額 3,500 億ドルで 400 億ドルを投資してから数週間での追加調達交渉となる。
  - 評価額 9,000 億ドルは Apple・Microsoft・Google・Amazon・NVIDIA などメガキャップ企業に迫る規模。Anthropic の高成長と Claude Mythos を中心としたサイバーセキュリティ需要が資金調達の原動力。調達が完了した場合、Anthropic の資本力は OpenAI に匹敵するレベルになり、AI フロンティアの競争が資本規模でも二極化する。
  - 企業は AI ベンダー選定において財務基盤・調達力を中長期の安定性指標として評価すること。評価額が急騰する局面でのライセンス・SLA 交渉は、ベンダー側の交渉力が高まる点を念頭に置いて進めること。
- **リンク**: <https://www.bloomberg.com/news/articles/2026-05-12/anthropic-in-talks-to-raise-30-billion-at-900-billion-valuation>

---

## セキュリティ関連ニュース

### CVE-2026-45185「Dead.Letter」— Exim に未認証リモートコード実行、GnuTLS ビルド全滅 (CVSS 9.8)

- **公開日**: 2026-05-12
- **ソース**: The Hacker News / XBOW / Gridinsoft / FOSS Force
- **要約**:
  - Exim メールサーバー 4.97〜4.99.2 の GnuTLS ビルドで use-after-free 脆弱性。**CVSS 9.8 (Critical)**。TLS セッション切断時に TLS バッファが解放された後、ネストされた BDAT 受信ラッパーが `ungetc()` でフリー済みメモリに 1 バイト書き込み、アロケータメタデータを破壊する。攻撃者は BDAT SMTP 拡張と TLS 接続の確立さえできれば特別な設定不要で RCE が可能。Debian/Ubuntu は GnuTLS バックド Exim をデフォルト出荷するため、世界で最も広く影響を受けるディストリビューション。発見は XBOW の AI 支援自律セキュリティテストプラットフォームで、5 月 1 日に報告して 11 日間のコーディネーション期間を設けた。悪用が既に確認されており、暗号通貨マイニング・ランサムウェア・ボットネット・バックドアの各用途で使われている。
  - SMTP インフラは組織の通信基盤の中枢。Exim は世界で最もシェアの高い MTA の一つであり、未修正環境への攻撃は急速に広がる可能性がある。AI 支援によるバグ発見が Palo Alto の警告（同日同一テーマ）と重なる象徴的事例でもある。
  - **対応**: `exim --version` で GnuTLS ビルドか確認し、Exim 4.99.3（2026-05-12 リリース）への即時アップグレード。Debian/Ubuntu は `apt upgrade exim4` で更新可。OpenSSL ビルドは非影響。
- **リンク**: <https://thehackernews.com/2026/05/new-exim-bdat-vulnerability-exposes.html>

---

### Windows 未修正ゼロデイ 2 件 (YellowKey / GreenPlasma) の PoC 公開 — BitLocker バイパス + SYSTEM 権限昇格

- **公開日**: 2026-05-12
- **ソース**: BleepingComputer / The Register / Cybernews / Tom's Hardware
- **要約**:
  - 研究者「Chaotic Eclipse (Nightmare-Eclipse)」が 5 月 12 日に GitHub へ PoC を公開。**YellowKey**: USB スティックを挿した状態で再起動時に特定キーコンビネーションを入力するだけで、BitLocker で保護されたドライブのロックを解除できる。Windows 11・Server 2022/2025 が影響（Windows 10 は非影響）。研究者は「意図的なバックドア」の可能性を示唆。**GreenPlasma**: Windows CTFMON サービスの Arbitrary Section Creation により SYSTEM 権限を取得できる LPE。Windows 11・Server 2022・2026 が影響。Microsoft は今回の Patch Tuesday（5/12）では両脆弱性を修正していない。同研究者は過去に BlueHammer・RedSun をリリースした「不満を持つ研究者」。
  - PoC 公開済みのため攻撃の敷居は低い。GreenPlasma は SYSTEM 昇格であり、YellowKey と組み合わせることで「物理アクセスなしでの BitLocker 破り → SYSTEM 昇格」のチェーン攻撃が成立する可能性がある。Microsoft は未修正であり、次回 Patch Tuesday（2026-06-09）まで修正が入らない可能性が高い。
  - 対応: (1) YellowKey → BIOS/UEFI での USB ブート・起動時設定変更をパスワードで保護、(2) GreenPlasma → CTFMON サービスへのアクセス制限、(3) 共に感度の高い環境では物理アクセス管理の強化と Secure Boot の設定確認。EDR での PoC コードの検知ルール追加も推奨。
- **リンク**: <https://www.bleepingcomputer.com/news/security/windows-bitlocker-zero-day-gives-access-to-protected-drives-poc-released/>

---

### SAP May 2026 Patch Day — Commerce Cloud・S/4HANA に CVSS 9.6 Critical 2 件 (CVE-2026-34263 / CVE-2026-34260)

- **公開日**: 2026-05-12
- **ソース**: BleepingComputer / SecurityWeek / Onapsis
- **要約**:
  - SAP が 5 月の Security Patch Day として 15 件のセキュリティノートを公開。Critical は 2 件。**CVE-2026-34263 (SAP Commerce Cloud)**: 認証チェック欠如により、未認証の攻撃者がサーバー上でコードを実行可能（CVSS 9.6）。**CVE-2026-34260 (SAP S/4HANA)**: ユーザー入力を直接 SQL クエリに連結する SQL インジェクション（CVSS 9.6）—基本権限だけでデータベース情報の窃取・アプリ停止が可能。他に高深刻度 1 件・中深刻度 11 件（コマンドインジェクション・認証不備・XSS・CSRF・DoS など）。野外悪用は現時点で未確認。
  - SAP は国内大企業・金融機関・製造業に広く導入されており、S/4HANA の SQL インジェクションと Commerce Cloud の未認証 RCE は事業継続への直接影響がある。Critical 2 件のいずれも悪用敷居が低い。
  - Commerce Cloud: 2205.49、2211.51、2211-jdk21.10 への更新。S/4HANA: SAP が提供する Security Note を確認して即時適用。SAP BASIS チームは ABAP スタックと Java スタック双方の適用状況を確認すること。
- **リンク**: <https://www.bleepingcomputer.com/news/security/sap-fixes-critical-vulnerabilities-in-commerce-cloud-and-s-4hana/>

---

### RubyGems に 500 件超の悪意あるパッケージが投入 — GemStuffer データ窃取キャンペーンと別系統攻撃でサインアップ停止

- **公開日**: 2026-05-12
- **ソース**: The Hacker News / SecurityWeek / Socket.dev / Risky Bulletin
- **要約**:
  - 研究者が「**GemStuffer**」キャンペーンを報告: 150 件超の gem が英国地方議会のパブリックポータル（Lambeth・Wandsworth・Southwark など ModernGov）からデータをスクレイピングし、その結果を gem アーカイブに梱包して RubyGems に公開する「データ窃取チャネル化」の新型手法。マルウェア配布ではなく情報収集目的。並行して別系統の「大規模悪意ある攻撃」により exploit を含む 500 件超のジャンクパッケージが投入され、RubyGems は新規アカウント登録を一時停止（5/13 に攻撃停止、bot アカウント除去・パッケージ削除済み）。Fastly WAF と新規登録レート制限の強化で対応中。攻撃者は不明。
  - オープンソースレジストリを「データ流出チャネル」として悪用する手法は新型であり、開発者が「自分の使うパッケージが情報収集コードを含む」リスクに加え「レジストリ自体が外部データの集積所になる」という新たな脅威面を示す。npm・PyPI でも同種キャンペーンが増加傾向。
  - Ruby 開発者は Gemfile.lock を精査し、不審なパブリッシャーや活動日付の新しいパッケージをピックアップして安全性を確認すること。CI/CD パイプラインに gem のハッシュ検証を導入すること。
- **リンク**: <https://thehackernews.com/2026/05/rubygems-suspends-new-signups-after.html>

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 | 影響/CVSS | リンク |
|--------|--------|------|-----------|--------|
| 2026-05-13 | **JVN#35567473 (CVE-2026-32661): GUARDIANWALL MailSuite スタックベースバッファオーバーフロー** | キヤノン IT ソリューションズのメールセキュリティ製品「GUARDIANWALL MailSuite」のオンプレ版 Ver 1.4.00〜2.4.26 に脆弱性。pop3wallpasswd コマンドに細工したリクエストを送信することで**未認証の遠隔コード実行**が可能。SaaS 版は 4 月 30 日メンテで修正済み。**すでに野外での悪用が確認**されており JPCERT/CC も注意喚起 (at260013) を発出。国内企業で広く利用されるメール監査・フィルタリング製品であり対応を急ぐこと。パッチ適用後は過去の侵害有無の調査も実施すること。 | CVSS v3.0 **9.8 (Critical)** ※悪用確認済み | [JVN#35567473](https://jvn.jp/jp/JVN35567473/) |
| 2026-05-13 | **JVN#24167657: KDDI「あんしんフィルター for au」(Android) 重要情報の平文送信** | KDDI 提供の子ども向けフィルタリングアプリ「あんしんフィルター for au」(Android 版 4.9_b0003 未満) において通信データが平文で送受信される脆弱性。中間者攻撃により通信内容の傍受・改ざんが可能。開発者が提供する最新版へのアップデートを推奨。 | 中 (中間者攻撃リスク) | [JVN#24167657](https://jvn.jp/jp/JVN24167657/) |
| 2026-05-13 | **JVN#98871848: Bytello Share (Windows 版) EXE インストーラーの安全でない DLL 読み込み** | 共有・プレゼンツール Bytello Share の Windows 版 EXE インストーラー (5.13.0.4246 未満) が、同ディレクトリに細工された DLL を無条件で読み込む。インストール実行時にユーザー権限での任意コード実行が可能。修正版 MSI インストーラー (5.13.0.4246) が提供済み。社内展開時のインストーラー配布元の管理とハッシュ検証を徹底すること。 | 中 (任意コード実行) | [JVN#98871848](https://jvn.jp/en/jp/JVN98871848/) |

---

## 本日のサマリ

本日の最優先対応は **GUARDIANWALL MailSuite CVE-2026-32661**（5/13）: 国内企業に広く普及するキヤノン IT ソリューションズのメールセキュリティ製品に CVSS 9.8 の未認証 RCE が判明し、すでに悪用が確認されている。JPCERT/CC も緊急注意喚起を発出しており、オンプレ版採用組織は即時パッチ適用と侵害調査が急務。次点は **Exim Dead.Letter (CVE-2026-45185, CVSS 9.8)**（5/12）: Debian/Ubuntu 系で野外悪用が進行中であり、Exim 管理者は 4.99.3 へ即時更新。**Windows BitLocker PoC (YellowKey/GreenPlasma)** は Microsoft 未修正のまま公開されており、物理アクセス管理と BIOS パスワード設定の強化が回避策として有効。AI 面では Palo Alto Networks が「Mythos + GPT-5.5 が数週間で 85 件のバグを発見・AI 攻撃常態化まで 3〜5 ヶ月」と警告（5/13）し、Google は Android を「Gemini Intelligence プラットフォーム」へ転換（5/12）。Anthropic の評価額 9,000 億ドル交渉報道（5/12）は AI 産業の資本集中が一段と加速していることを示している。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 40 (WebSearch × 16 クエリ、WebFetch 複数試行)
- 採用件数: AI=4 / Security=4 / 国内=3 (テーブル形式)
- 除外理由内訳:
  - 古すぎ (採用窓外: 公開日 2026-05-12 未満):
    - TeamPCP Checkmarx Jenkins AST plugin 攻撃 (The Register 2026/05/11)
    - 偽 OpenAI HuggingFace リポジトリ情報窃取マルウェア (HiddenLayer 2026-05-07)
    - Cohere + Aleph Alpha 合併 (2026-04-24〜25)
    - Anthropic + Google/Broadcom TPU 拡張契約 (2026-04-06〜07)
    - OpenAI Privacy Filter リリース (2026-04-22)
    - OpenAI B2B Signals (日付未確認のため除外)
  - 重複 (過去 7 日 excluded_set に既出):
    - Microsoft Patch Tuesday "138 件" (同 Patch Tuesday の報道差分; 05-13 digest で "120 件" として掲載済み)
    - CVE-2026-0300 (PAN-OS; 05-09/10 digest 掲載済み)
    - CVE-2026-31431 Copy Fail (05-09/10 digest 掲載済み)
    - CVE-2026-43284/43500 Dirty Frag (05-10 digest 掲載済み)
    - Canvas/Instructure 全関連 (05-11〜05-13 digest 掲載済み)
    - Google GTIG AI ゼロデイ (05-12 digest 掲載済み)
    - OpenAI Daybreak / DeployCo (05-13 digest 掲載済み)
    - CVE-2026-41089 Netlogon / ELECOM ルーター (05-13 digest 掲載済み)
    - Agentic AI セキュリティ盲点 THN (05-13 digest 掲載済み)
  - 日付不明・未確認: OpenAI B2B Signals (URL 確認できず)
- 取得失敗ソース (HTTP 403 等):
  - thehackernews.com (WebFetch 直接)
  - bleepingcomputer.com (WebFetch 直接)
  - jpcert.or.jp (WebFetch 直接)
  - ipa.go.jp (WebFetch 直接)
  - axios.com (WebFetch 直接)
  - cnbc.com (WebFetch 直接)
  - xbow.com (WebFetch 直接)
  - thomasharris6.wordpress.com (WebFetch 直接)
  - helpnetsecurity.com (WebFetch 直接)
  → 全て WebSearch スニペット・ミラーサイト URL パターン (guardianmssp.com/2026/05/12/ 等) で公開日を代替確認
- 日付確認方法:
  - Google Android Show: blog.google URL + techcrunch.com/2026/05/12/ で確認
  - Intrusion Logging: techcrunch.com/2026/05/12/ + easternherald.com/2026/05/14/ で確認
  - Palo Alto AI警告: cnbc.com/2026/05/13/ + axios.com/2026/05/13/ URL パターンで確認
  - Anthropic $30B: bloomberg.com/news/articles/2026-05-12/ URL で確認
  - CVE-2026-45185: guardianmssp.com/2026/05/12/ + thomasharris6.wordpress.com/2026/05/12/ URL で確認
  - YellowKey/GreenPlasma: borecraft.com/2026/05/12/ URL + The Register /2026/05/13/ URL で確認
  - SAP Patch Day: bleepingcomputer.com + SecurityWeek 記事で 5/12 確認
  - RubyGems: ibvl.in/index.php/2026/05/12/ + cypro.se/2026/05/12/ URL で確認
  - JVN#35567473: ipa.go.jp/security/security-alert/2026/20260513-jvn.html URL で 05-13 確認
  - JVN#24167657 / JVN#98871848: JVN 検索結果スニペット「2026-05-13」記述で確認

</details>
