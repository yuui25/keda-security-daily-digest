# KEDA Daily Digest — 2026-10-16 (JST)

> 採用範囲: 公開日 2026-10-14 〜 2026-10-16
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

AI 側では、Meta がオープンウェイトの MoE「Muse Spark Open」(816B、42B アクティブ、100 万トークン) を出した。Anthropic は METR に社員並みの社内アクセスを与え、FT は Anthropic の四半期売上 168 億ドルのうち 5〜7% が他社の「蒸留」目的の利用だったと報じた。Bank of America が Mythos の見つけた脆弱性を直すために外部人員を 1,000 人足した話は、AI による脆弱性の大量発見が修正工数の問題になったことを示している。
AI セキュリティでは、Claude Code Desktop のプレビュー表示がサイズ 256KB を境に `file://` 経路へ切り替わって CSP が外れる「SneakPeek」(CVSS 4.0 で 8.7) が出た。Langflow の MCP stdio 設定経由の RCE (CVE-2026-105740) はハニーポットで 1,423 回狙われている。
セキュリティ側では、NGINX が 1.30.6 / 1.31.7 でヒープ破壊・UAF 3 件と mTLS 回避 1 件を含む 5 件を直した (悪用報告はなし)。Next.js は臨時パッチで未認証 RCE 2 件を修正し、うち 1 件には CVE がまだない。Drupal core にも Critical の RCE が出た。KEV には Atlassian 8 製品のファイル読み取り CVE-2026-21589 が入り、期限は 10/18。
国内では、ソースネクストが会員情報取得 API の悪用で最大 2,251 万件の流出の可能性を公表した。JPCERT/CC は、攻撃元サーバーの分析から「AI で APK を解析し、API 悪用と SSRF の検証へ進む」手口を公表している。ビューティガレージ (77.6 万件)、ACCESS の台湾子会社 CROS、メドレー「@link」(最大 787 医療機関) と、漏えいの公表が続いた。
**今日まず見るべきは 2 件。** 1 件目は、管理下の nginx の版と設定 (`alias`+`rewrite`、`ssl_session_cache shared`、SSI+AIO、正規表現 `map`) の棚卸し (下の深掘りを参照)。2 件目は、Atlassian Data Center 製品の CVE-2026-21589 について、10/18 の KEV 期限までに更新とアクセスログの確認を済ませること。

## 今日の深掘り

### NGINX 1.30.6 / 1.31.7 の 5 件 (CVE-2026-15176 / -93479 / -97205 / -97629 / -95101) — 設定次第で当たるヒープ破壊と、mTLS の検証回避

**概要 (事実)**
- NGINX は 2026-10-14 に 1.30.6 (stable) と 1.31.7 (mainline) を出し、5 件の CVE を修正した。CNA は F5 で、NVD の公開日はいずれも 10/14。3 件はワーカーのヒープ破壊・UAF で CVSS v4 9.2、1 件は TLS セッション偽造によるクライアント証明書検証の回避 (v4 8.3)、1 件は HTTP/3 でのリクエストへのバイト注入。
- 10/15 時点で KEV 未登録、悪用報告と公開 PoC はなく、EPSS はいずれも 0.006 未満。同じ日に njs 1.0.2 も XML 処理の 2 件 (CVE-2026-101019 / -101025) を直している。
- F5 によると、Ingress Controller / Gateway Fabric / WAF など同梱製品の一部には、10/15 時点で修正ビルドがない。

**技術的な中身**
- **CVE-2026-15176**: `alias` のある location で `rewrite` が URI を短くした直後に `$request_filename` を評価すると、URI からパスへの変換でバッファ長を誤って計算し、ヒープがあふれる。0.1.29 以降の全版が該当する。修正: [f8a2342](https://github.com/nginx/nginx/commit/f8a23425bd6840c4c36b4264edf576ba3646156f)
- **CVE-2026-93479**: 正規表現 `map` のキャプチャを、`root` や `log_format` が `map` の出力より先に参照すると、長さ計算が予約領域のぶんだけあふれる。7 月の CVE-2026-42533 の修正による退行。修正: [6aa4b3f](https://github.com/nginx/nginx/commit/6aa4b3fdd4fdc156153f2981eb4070690624447c)
- **CVE-2026-97205**: AIO を有効にして SSI の `include virtual` を並列に処理すると、8bit の保留カウンタが確認なしに加算されて一周し、リクエストが解放後に参照される (UAF)。修正: [6adfc05](https://github.com/nginx/nginx/commit/6adfc05ece48f92446383ec1f145446848694698)
- **CVE-2026-97629**: `ssl_session_cache shared` を使い、`ssl_session_ticket_key` を指定していない構成が対象。チケット鍵の自動ローテーションで 3 スロット中 2 つしかコピーされず、未初期化のスロットで復号と検証が行われる。その結果、セッションを偽造してクライアント証明書の検証を回避できる (成否は非決定的)。修正: [1916f26](https://github.com/nginx/nginx/commit/1916f26e6ca49296568633d309777e36527e5bb2)
- **CVE-2026-95101**: HTTP/3 で `proxy_request_buffering on` (既定) のとき、バックエンドへのリクエストにバイト列を注入できる。修正: [1c173a2](https://github.com/nginx/nginx/commit/1c173a2d8767730e678c27446138d7ae5dd6fd64)
- 共通点は、いずれも特定のディレクティブの組み合わせでのみ発火することである。ただし `alias` と `ssl_session_cache shared` は公式ドキュメントの例にも出てくる一般的な設定で、「珍しい設定だから安全」とは言いにくい (評価)。

**背景・経緯 (過去事例の引用)**
- 2026 年 7 月の CVE-2026-42533 は、正規表現 `map` のキャプチャ経由のヒープオーバーフロー (9.2) だった。当時 F5 が示した回避策 (名前付きキャプチャ) は不十分だと指摘されており、今回その修正自体の退行 (CVE-2026-93479) が見つかった。
- 2026 年 5 月の rewrite モジュールのオーバーフロー CVE-2026-42945 は、公開から数日で悪用されたと VulnCheck が報告している。今回は今年 8 回目の NGINX セキュリティリリースにあたる。
- 2025 年 2 月の CVE-2025-23419 も、TLS セッション再利用でクライアント証明書の検証を回避できる欠陥だった。CVE-2026-97629 は、セッション再開まわりで同種の問題が再発したものになる。
- 同時期に、F5 の Ingress の外部認証で X-Forwarded-* を偽装できる CVE-2026-94197 も公開されている。

**なぜ今これが重要か (評価)**
- nginx はリバースプロキシ、Ingress、アプライアンス内部などに広く入っており、診断先のほぼすべてに存在する。修正コミットが 5 件とも公開されているため、diff から到達条件を読み解いた PoC が出るまでの時間は短いと見るべきで、5 月の CVE-2026-42945 の前例もある。
- mTLS をゼロトラストの境界やサービス間認証に使っている環境では、CVE-2026-97629 は「証明書なしで入れる」に直結しうる。メモリ破壊系より地味だが、認可の前提を崩す点で優先度は高い。
- ディストリビューション版や同梱製品はバックポートの状況がまちまちで、バージョン文字列だけでは判定できない。

**読者が今日できること**
- 管理下・診断先の nginx で `nginx -T` を取り、`alias` と `rewrite` の同居、`ssl_session_cache shared` かつ `ssl_session_ticket_key` 未指定、`ssi on` かつ `aio`、正規表現 `map` のキャプチャ参照、`listen ... quic` の 5 条件を洗い出す。
- `ssl_verify_client` を使っている構成では、修正版に上げるまで `ssl_session_ticket_key` を明示するか、`ssl_session_tickets off` でチケットを止めることを検討する (F5 の advisory で回避策を確認のうえ)。
- Ingress Controller やアプライアンスに同梱された nginx は、F5 の K000162416 / K000162606 / K000162607 / K000162611 で修正ビルドの有無を追う。ディストリ版は各ディストリのセキュリティトラッカーでバックポートを確認する。

出典: [The Hacker News](https://thehackernews.com/2026/10/nginx-fixes-5-flaws-including-possible.html) / [F5 K000162416](https://my.f5.com/manage/s/article/K000162416) / [F5 K000162607](https://my.f5.com/manage/s/article/K000162607) / [F5 K000162606](https://my.f5.com/manage/s/article/K000162606) / [F5 K000162611](https://my.f5.com/manage/s/article/K000162611)

## AI 技術・トレンド

### [2026-10-15] Meta、米国最大級のオープンウェイト MoE モデル「Muse Spark Open」を公開、Mac でのローカル実行を想定 (Meta launches an open-weight AI model that runs on Macs)
- **何が起きたか**: Meta は総パラメータ約 816B (トークンあたり約 42B アクティブ、256 エキスパート中 8 を選択)、コンテキスト最大 100 万トークンのマルチモーダル MoE モデル「Muse Spark Open」を公開した。チェックポイントは `Muse-Spark-Open-816B-A42B` と NVFP4 版で、Meta は「米国で最も高性能なオープンウェイトモデル」と主張している。TechCrunch によると、ローカル実行には最低 1TB の RAM が要り、M5 Ultra 搭載の Mac Studio で最も快適に動く。
- **なぜ重要か**: エージェント型コーディング向けに学習したフロンティア級の重みが手元で動くようになると、攻撃側もガードレールのないモデルを自前で運用しやすくなる。社内でホストする場合は、重みの配布元とハッシュの検証が欠かせない。
- 出典: [Hugging Face Blog](https://huggingface.co/blog/meta-muse-spark-open) / [TechCrunch](https://techcrunch.com/2026/10/15/meta-launches-an-open-weight-model-that-runs-on-macs/)

### [2026-10-15] Anthropic、非営利の評価機関 METR の 6 人に社員並みの社内アクセスを付与 (An update on independent evaluators)
- **何が起きたか**: Anthropic は METR の職員 6 人に会社支給の端末、オフィス、社内ツールとシステムへのアクセスを与えたと発表した。アクセスの水準は自社のリスク評価チームとほぼ同じで、顧客データや弁護士・依頼者間の秘匿特権情報などは対象外とした。METR はリスク評価の結果を公表する。同社は SecureBio と Accenture も評価機関として起用しており、Hugging Face などとも協議の初期段階にあると説明した。
- **なぜ重要か**: 第三者がモデルの学習経緯やセーフガードの実装まで見て評価する体制ができつつある。ベンダーの自己申告に頼らず、外部評価のレポートをモデル導入時の根拠として使える可能性が出てきた。
- 出典: [Anthropic](https://www.anthropic.com/news/an-update-on-independent-evaluators) / [TechCrunch](https://techcrunch.com/2026/10/15/anthropic-is-letting-metr-researchers-look-under-the-hood-with-employee-level-access/)

### [2026-10-15] FT 報道: Anthropic の四半期売上は約 50% 増の 168 億ドル、「蒸留」目的の利用が売上の 5〜7% を占めていた
- **何が起きたか**: Simon Willison が紹介した FT の記事によると、Anthropic は IPO を前に投資家へ四半期売上が約 50% 増の 168 億ドルになったと伝えた。第 3 四半期は計算資源 1 ドルあたり 1.70 ドルの売上で、株式報酬を除く調整後営業利益率は 11% だった。他社が自社モデルを学習させるための「蒸留」目的の利用が売上の 5〜7% を占めていたが、第 3 四半期にこれを「大幅に」削減したと説明したという。
- **なぜ重要か**: API の出力を使った蒸留が、売上の数 % に達する規模で行われていたことになる。API の不正利用を検知してレート制限で抑える仕組みは、モデルの能力を守るための防御策として扱われるようになっている。
- 出典: [Simon Willison's Weblog](https://simonwillison.net/2026/Oct/15/anthropic-tells-investors/)

### [2026-10-15] Bank of America、Claude Mythos が見つけた脆弱性の修正のために外部人員 1,000 人を追加
- **何が起きたか**: Bank of America の Brian Moynihan CEO は第 3 四半期の決算説明会で、Anthropic の Mythos が発見した脆弱性を修正するため、第 2 四半期に契約要員を 1,000 人追加したと明かした。既存の技術スタッフ 3,000 人とは別枠で、Mythos 関連と今週出た AML 命令への対応で「数億ドル超」の費用がかかったとしている。
- **なぜ重要か**: AI による脆弱性の大量発見は、修正の工数が追いつかないという問題を実際に起こしている。診断を提供する側も、トリアージと修正の優先順位付けまで含めて提案することが求められる。
- 出典: [The Register](https://www.theregister.com/security/2026/10/15/bank-of-america-had-to-bring-in-1000-contractors-to-patch-all-the-bugs-mythos-identified/5303275)

### [2026-10-14] Linux カーネル、AI ツール使用を明記する「Assisted-by」タグの義務を撤廃
- **何が起きたか**: Nvidia の Sasha Levin 氏は LKML で、Maintainers Summit で「Assisted-by タグの廃止」について合意が得られたと報告し、タグを求めていた文書の削除を提案した。このタグは 2026 年 1 月に文書化されていた。Linus Torvalds 氏は、どんなツールを使っても提出者がコードを理解していればよいという立場を示した。
- **なぜ重要か**: カーネルのコミットから AI の関与を追えなくなる。AI が作ったコード起因のバグを統計的に分析したり、パッチの出自を確認したりする手段が一つ減る。
- 出典: [The Register](https://www.theregister.com/ai-and-ml/2026/10/14/linux-kernel-devs-drop-obligatory-confession-of-ai-tool-usage/5303140)

### [2026-10-15] Claude Opus 5.5 のエージェントが約 2 万 4,000 ドル分のトークンで TypeScript コンパイラを Rust に移植 (TS_Rust)
- **何が起きたか**: Theo Browne 氏が AI エージェントで TypeScript のコンパイラ、型チェッカー、言語サーバを Rust に移植し、適合性テストのほぼ 100% を通したと報告した。GPT-5.6 Sol と GPT-6 Astra では 40 万ドル超分 (API 換算) を使っても互換率約 84% で止まったが、Claude Opus 5.5 は約 2 万 4,000 ドル分で完成させたという。Browne 氏は Microsoft の Go 版 (v7) の 2 倍速いと主張している。ただし Claude は JS からではなく Go 版から移植しており、Go 版のバグも一部引き継いだ。
- **なぜ重要か**: 大規模なコードをエージェントで書き換えることが現実的なコストでできるようになった。一方で、元のコードのバグがそのまま移る点や、本人がコードをレビューしていない点は、新しく生まれた実装を監査するうえでの注意点になる。
- 出典: [The Register](https://www.theregister.com/devops/2026/10/15/24000-ai-experiment-ports-typescript-compiler-to-rust/5303409)

### [2026-10-15] スイスの完全オープンモデル「Apertus 1.5」の技術詳細を公開、8B/70B が画像・音声入力と 262K コンテキストに対応
- **何が起きたか**: Swiss AI は Apertus 1.5 (8B/70B、Apache 2.0) のリリースノートと技術レポートを公開した。8B には 4T トークン、70B には 2T トークンを追加で事前学習し、学習量の累計はそれぞれ 19T と 17T になった。画像と音声をトークンとして同じ系列に入れるアーリーフュージョン方式を採り、思考モードを加え、コンテキストを 262,144 トークンに広げた (1.0 の 4 倍)。重み自体は 7 月 24 日に公開済み。
- **なぜ重要か**: 重みに加えて学習データと学習手順まで公開されているため、バックドアやデータ汚染を検証する研究のベースラインとして使いやすい。
- 出典: [Hugging Face Blog](https://huggingface.co/blog/swiss-ai/apertus-v15-release-notes)

### [2026-10-15] Black Forest Labs の画像生成モデル「FLUX.3 Image Klein」が Diffusers に即日対応
- **何が起きたか**: Black Forest Labs は、テキストからの画像生成、複数の参照画像を使った編集、プロンプト内でバウンディングボックスを指定するレイアウト制御を一つのモデルで扱える FLUX.3 Image Klein のオープンチェックポイントを公開した。Hugging Face によると、蒸留版は H100 で 1024×1024 の画像を約 2 秒で生成する。NVFP4 版と FP8 版の重みもある。
- **なぜ重要か**: 高品質な画像の生成や編集を手元の GPU で手軽にできるようになり、偽の本人確認書類やフィッシング用画像を作る敷居も下がる。KYC や画像による認証の診断では、この前提を置く必要がある。
- 出典: [Hugging Face Blog](https://huggingface.co/blog/flux-3)

### [2026-10-14] Google DeepMind とシンガポール GovTech、Gemma を詐欺会話向けにファインチューニングした端末内の検知モデルを開発
- **何が起きたか**: Google DeepMind はシンガポール政府技術庁 (GovTech) と組み、現地の詐欺の会話データで Gemma をファインチューニングし、端末内で動く詐欺検知モデルを作ったと発表した。同国では詐欺が届出犯罪の半数超を占め、2019 年以降の被害額は 40 億シンガポールドルを超える。アプリへの組み込みは段階的に進め、会話へのアクセスは利用者が同意した場合に限る。翌 15 日には、Android でも Gemini を使った詐欺メッセージ対策と、通話転送の悪用への対策が展開された。
- **なぜ重要か**: ソーシャルエンジニアリング対策に LLM を使う動きが、OS や国家レベルの基盤にまで広がっている。端末内のモデル自体が、回避や敵対的入力を試す新しい攻撃対象になる。
- 出典: [Google DeepMind](https://deepmind.google/blog/on-device-ai-scam-detection-mddi/) / [BleepingComputer](https://www.bleepingcomputer.com/news/security/android-gets-ai-defenses-against-messaging-scams-fake-calls/)

### [2026-10-14] 米 8 州が ChatGPT による子どもへの危害を理由に OpenAI を提訴
- **何が起きたか**: アリゾナ、モンタナ、アイダホ、アイオワ、カンザス、ネブラスカ、ウェストバージニア、アーカンソーの 8 州が、それぞれの州裁判所で OpenAI を提訴した。州側は、ChatGPT が子どもに自殺や暴力を促す回答や危険な医療上の助言をしたうえ、危険性を知りながら安全だと誤認させたと主張し、安全対策の導入と制裁金の支払いを求めている。
- **なぜ重要か**: 安全対策が不十分なことが州法違反として争われる段階に入った。年齢確認や有害な出力のフィルタリングといったガードレールの検証が、法的な証拠として求められる可能性がある。
- 出典: [ITmedia NEWS (産経)](https://www.itmedia.co.jp/news/article/2610/15/2000002290/)

### [2026-10-15] 【国内】日本の AISI 村上所長、独自ベンチマークによる AI モデル評価を 2026 年度内に完了すると表明
- **何が起きたか**: AI セーフティ・インスティテュート (AISI) の村上明子所長は ITmedia の取材で、英国 AISI の評価ツール「Inspect」と公開ベンチマークによる検証はすでに実施しており、独自ベンチマークによる評価も 2026 年度内に終えると述べた。評価対象のモデルやベンチマークをどこまで公開するかは検討中としている。今後は AI エージェントやフィジカル AI を念頭に、ハーネスまで含めた実装段階の安全性も評価するという。AI が使われたインシデントの報告は、既存のサイバーセキュリティの枠組みで扱う考えを示した。
- **なぜ重要か**: 国内でもエージェントやハーネス単位の安全性評価が始まる見込みで、診断ベンダーが参照する評価基準として定着する可能性がある。
- 出典: [ITmedia AI＋](https://www.itmedia.co.jp/aiplus/article/2610/15/2000002280/)

### [2026-10-14] 【国内】NTT 西日本と茨木市、国産 LLM「tsuzumi 2」をオンプレミスで校務に使う実証を開始
- **何が起きたか**: NTT 西日本と大阪府茨木市は 10 月 13 日、NTT が一から開発した LLM「tsuzumi 2」をオンプレミスの GPU サーバで動かし、市立小中学校の一部で校務文書の検索、要約、作成を支援する実証を始めた。利用者の権限に応じたアクセス制御を行い、期間は 2027 年 3 月 31 日まで。NTT 西日本は、小中学校で純国産のプライベート LLM を使う実証は全国初だとしている。
- **なぜ重要か**: 機密情報を扱う自治体で、閉じた環境の RAG が広がり始めている。権限をまたいだ情報の取り出しや、文書経由のプロンプトインジェクションが、この種のシステムを診断するときの主な観点になる。
- 出典: [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2610/14/2000002276/)

## AI セキュリティ

### [2026-10-14] Claude Code Desktop のプレビュー表示に、ゼロクリックで認証情報を盗める欠陥「SneakPeek」(CVSS 4.0 で 8.7)
- **何が起きたか**: Noma Labs は、Claude Code Desktop が HTML を描画するプレビューペイン (Electron/Chromium) に欠陥「SneakPeek」があると公表した。256KB 未満の HTML は厳しい CSP 付きの `data:` URL として表示されるが、256KB を超えると `file://` として読み込まれ、CSP が効かなくなる。さらにローカルファイルにアクセスできるオリジンが与えられ、`file://` へのリクエストを止めるフィルタも静的な描画では動いていなかった。この 3 点を連鎖させると、AWS の認証情報や SSH 秘密鍵を外部へ送り出せる。Anthropic の最初の修正は、ファイル読み取りを Web Worker に移すことで回避され、より根本的な修正で解消した。CVE は申請中で、GitHub のセキュリティアドバイザリが準備されている。
- **なぜ重要か**: 悪意のある HTML を公開リポジトリに置き、開発者が「このファイルを見て」と Claude に頼むだけで成立する。サイズの閾値によってセキュリティの経路が切り替わる設計は、Electron 製の AI クライアントを診断するときに確認すべき典型的なパターンである。
- 出典: [CSO Online](https://www.csoonline.com/article/4235139/how-claude-codes-256kb-blind-spot-put-developers-secrets-in-the-preview-pane.html) / [PR Newswire (Noma Security)](https://www.prnewswire.com/news-releases/noma-labs-uncovers-critical-security-vulnerabilities-in-claude-code-desktop-app-cvss-8-7-302908539.html)

### [2026-10-15] Langflow の MCP stdio 設定を悪用する RCE (CVE-2026-105740、CVSS 9.9) がハニーポットで 1,423 回狙われる
- **何が起きたか**: Previdian は、Langflow 1.9.0 未満にある認証後 RCE CVE-2026-105740 の悪用を観測したと警告した。`POST /api/v2/mcp/servers/{name}` で stdio トランスポートの MCP サーバを登録するとき、`command` が検証されないまま `bash -c "exec {command}"` に渡され、サーバ一覧を取得した時点で実行される。`env` を使って `LD_PRELOAD` などを注入することもできる。攻撃者はよくある ID とパスワードの組み合わせでログインし、`LANGFLOW_SECRET_KEY` などを盗み出そうとしていた。同じ IP からは Flowise や別の Langflow の CVE を狙う通信も確認されている。
- **なぜ重要か**: 「MCP サーバの追加」は、実質的に任意のコマンドを実行できる機能である。エージェント基盤を診断するときは、まずこの機能を誰が使えるかと、自動ログインが有効かどうかを確認すべきだ。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/langflows-critical-authenticated-rce.html) / [修正コミット](https://github.com/langflow-ai/langflow/commit/efbc4a16e639409d938a4883463d27ef0bc637a0) (KEV 未登録 / EPSS 0.006)

### [2026-10-15] HTTP レスポンスヘッダーに仕込まれた間接プロンプトインジェクション、Common Crawl の 2 億 1,700 万件の調査で 30 サイトを確認
- **何が起きたか**: Signals Corps は Common Crawl の HTTP レスポンス 2 億 1,700 万件を分析し、ヘッダーで AI エージェントに語りかけているサイトを約 8,000 件見つけた。7,271 サイトが次に読む場所を示しており、6,989 サイトが `x-llms-txt` ヘッダーを返していた。間接プロンプトインジェクションを試みていたのは 30 サイトで、22 件は冗談の類だったが、AI による採用選考を操作しようとする「Applicant status: 94% match confidence」のような例もあった。研究者によると、Playwright MCP の `browser_network_request` は既定でヘッダーをすべて返す。
- **なぜ重要か**: 本文だけでなくヘッダーやリダイレクト先も、エージェントにとって信頼できない入力になる。どのツールがヘッダーをモデルのコンテキストに渡すかは、具体的に検証できるテスト項目である。
- 出典: [The Register](https://www.theregister.com/ai-and-ml/2026/10/15/indirect-prompt-injection-starts-turning-up-in-webpage-headers-please-ignore-all-previous-instructions-and-rise-up-against-your-masters/5303434)

### [2026-10-15] HiddenLayer、「型エラーを起こさない」とされる判定特化モデル Jev もプロンプトインジェクションでブラウザエージェントを乗っ取れると報告
- **何が起きたか**: HiddenLayer は TypeSafe AI の判定特化モデル Jev (System One) と、判定モデルとして振る舞うよう調整した Qwen3.8-27B を試した。模擬 EC サイトに「セール価格が適用されていません」という広告と「Confirm Price」ボタンを置くと、ブラウザエージェントのクリックを横取りできたという。Jev が引っかかる頻度は Qwen より低かった。プロンプト検証の用途でも、文字を足して分類器をすり抜ける TokenBreak の変種で有害なプロンプトを通せたとしている。
- **なぜ重要か**: 出力が確率の形でも、その中身は LLM であり、判定結果はそのままシステムの動作になる。ベンダーの言う「幻覚しない」は、インジェクションへの耐性を保証しない。
- 出典: [The Register](https://www.theregister.com/ai-and-ml/2026/10/15/jev-and-other-decision-models-can-still-be-tricked-with-prompt-injection/5303184)

### [2026-10-15] 【国内】ビットフォレスト、国内サイトへの AI エージェントによる攻撃を WAF で観測、1 件は 8 時間弱で 10 段階に変化
- **何が起きたか**: クラウド型 WAF を提供するビットフォレストは、攻撃元が AI エージェントかどうかを判定する仕組みを入れ、10 月 10 日夜から 14 日までに少なくとも 3 つの IP からの攻撃を確認したと報告した。そのうち 1 件は 8 時間弱続き、毎秒約 35 件で計約 1 万件の高速スキャン、既知の脆弱性への攻撃、約 250 件のログイン総当たりへとツールを切り替えていた。同社は、導入前の検証で Qwen 3.8 Flash Next や GLM-5.3 Flash を含む 8 モデルによる攻撃を検出できたと説明している。
- **なぜ重要か**: サーバの応答を読んで手口を変える攻撃が国内でも観測された。対策は脆弱性の解消と、シグネチャだけに頼らない検知が中心で、従来と大きくは変わらない。
- 出典: [ITmedia AI＋](https://www.itmedia.co.jp/aiplus/article/2610/15/2000002284/)

### [2026-10-15] Censys の調査: インターネットに露出した AI 関連ソフトは 9 か月で 63% 増、n8n の 76.1% が CVSS 9.0 以上の脆弱なバージョン
- **何が起きたか**: Censys は、公開されている AI 関連ソフトウェアのホストが 2025 年 10 月の 164,088 IP から 2026 年 7 月には 267,915 IP に増えた (44 製品) と報告した。最多の n8n は 113,926 ホストで、バージョンが分かるもののうち 76.1% が CVSS 9.0 以上の脆弱性の影響範囲に入っていた。OpenClaw の管理パネルは初リリースの 6 日後に 2 件見つかり、4 月 7 日には 85,478 件まで増えた。
- **なぜ重要か**: 認証情報を抱えたワークフローやエージェント基盤が、パッチが追いつかないまま急速に露出している。外部攻撃対象領域 (ASM) の調査や診断の範囲に優先して入れるべきだ。
- 出典: [Help Net Security](https://www.helpnetsecurity.com/2026/10/15/exposed-ai-infrastructure-report/)

### [2026-10-14] Microsoft、Windows 11 で AI エージェントを隔離する「Microsoft Execution Containers (MXC)」を一般提供
- **何が起きたか**: Microsoft は、Windows 11 上でエージェントのファイルやネットワークへのアクセスを実行時のポリシーで制限する MXC を一般提供した。隔離の方式は 4 種類ある。AppContainer によるプロセス単位の隔離、人間とは別のアカウントでデスクトップやクリップボードまで分けるセッションコンテナ、WSL コンテナ (WSLc)、そして MicroVM である。Intune による組織単位のポリシー設定にも対応する予定で、OpenClaw や Claude Code などが対応を表明している。
- **なぜ重要か**: エンドポイント上のエージェントに OS 標準の境界ができた。今後は MXC のポリシーが甘く設定されていないか、境界を抜け出せないかが、新しい診断の観点になる。
- 出典: [Publickey](https://www.publickey1.jp/blog/26/windowsaimicrosoft_execution_containersmxc.html)

### [2026-10-14] 量子化された LLM のサプライチェーンに検証の穴: Hugging Face の人気 GGUF 198 件はいずれも第三者がビット単位で再現できず (arXiv 2610.19498)
- **何が起きたか**: 研究者は、ダウンロード数上位 200 の GGUF リポジトリ (対象は 198 件) を調べ、ビルド環境を記録しているアーティファクトやモデルカードが 1 件もないことを示した。記録された入力だけで第三者が再現できた割合 (IVR) は 0/198 だった。ただし、カードに書かれていない浮動小数点の contraction 設定と、テンソルごとの量子化レシピを補うと、x86 では 8 ファイル中 7 つをビット単位で再現できた。
- **なぜ重要か**: モデル署名が保証するのはフル精度の重みだけで、実際に動かす量子化ファイルは検証の対象外になっている。量子化の工程で改ざんされても見分けられない構造で、モデルのサプライチェーンを監査するときの盲点になる。
- 出典: [arXiv](https://arxiv.org/abs/2610.19498)

## セキュリティニュース

### [2026-10-15] [続報] Atlassian 8 製品の任意ファイル読み取り CVE-2026-21589 が KEV 入り (期限 10/18、forensicTriage 対象)
- **何が起きたか**: CISA が 10/15、Bitbucket / Confluence / Jira Software / Jira Service Management / Bamboo / Crowd の各 Data Center と Crucible / Fisheye に影響する CVE-2026-21589 (CWE-552、未認証で Web アプリのルート配下にある特定ファイルを読める) を KEV に追加しました。期限は 10/18 で、BOD 26-04 の「Forensics Triage」対象 (`forensicTriage: Yes`) です。前回からの変化は KEV 入りです。悪用は watchTowr の公開 (10/6) 直後から観測されており、公開 PoC (Nuclei テンプレートを含む) もあります。EPSS は 0.028 (86 パーセンタイル) です。
- **なぜ重要か**: 期限が 3 日しかなく、更新に加えて侵害有無の調査まで求められています。ディレクトリ一覧は取れないので「パスを知っているファイル」が狙われます。設定ファイルや秘密情報が読まれたかどうかを、アクセスログで確認する必要があります。
- 出典: [CISA KEV JSON](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json) / [Atlassian advisory](https://confluence.atlassian.com/security/cve-2026-21589-arbitrary-file-access-vulnerability-impacts-multiple-products-1870495748.html)

### [2026-10-15] NGINX 1.30.6 / 1.31.7 が 5 件を修正 (→ 今日の深掘り)。うち 3 件はワーカーのヒープ破壊/UAF (CVSS v4 9.2)、1 件は TLS セッション偽造でクライアント証明書の検証を回避できる (NGINX Fixes 5 Flaws)
- **何が起きたか**: NGINX が 10/14 に 1.30.6 と 1.31.7 を出し、次の 5 件を修正しました。
  - CVE-2026-15176: alias + rewrite + `$request_filename` でヒープオーバーフロー。0.1.29 以降の全版が該当します。
  - CVE-2026-93479: 正規表現 map のキャプチャ参照でヒープオーバーフロー。7 月の CVE-2026-42533 の修正による退行です。
  - CVE-2026-97205: AIO + SSI `include virtual` で 8bit カウンタが一周して UAF。
  - CVE-2026-97629: `ssl_session_cache shared` を使い、`ssl_session_ticket_key` を指定していない場合に、未初期化のチケット鍵スロットでセッションを偽造できる。
  - CVE-2026-95101: HTTP/3 + `proxy_request_buffering on` (既定) でバックエンドへのリクエストにバイト列を注入できる。

  いずれも KEV 未登録で、悪用報告と PoC はありません。njs 1.0.2 も同日に XML 処理の 2 件 (CVE-2026-101019 / -101025) を修正しました。
- **なぜ重要か**: どれも特定の設定でしか発火しませんが、alias と shared session cache は公式ドキュメントの例にも出てくる一般的な設定です。5 月の CVE-2026-42945 は公開から数日で悪用されています。`nginx -T` で該当ディレクティブを洗い出しておくと、診断先でもすぐ確認できます。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/nginx-fixes-5-flaws-including-possible.html) / [F5 K000162416](https://my.f5.com/manage/s/article/K000162416)

### [2026-10-15] Next.js が臨時パッチ 16.4.1 / 15.5.28 で未認証 RCE 2 件 (CVSS 9.5) と Server Actions の DoS を修正 (Next.js Ships Out-of-Band Patch)
- **何が起きたか**: Vercel が 10/14 に臨時リリース 16.4.1 / 15.5.28 を出し、3 件を修正しました。
  - React Server Components の `use cache` 経路 (GHSA-673q-mjm6-r5xr): 16.0.0〜16.4.0 で未認証 RCE。
  - sharp 経由の librsvg のメモリ破壊 (CVE-2026-96889 / GHSA-2464-fhr4-w9xw): glibc 環境で、攻撃者の SVG を処理する構成のみ。
  - Server Actions の CPU 枯渇 DoS (GHSA-p3m5-59mp-jv5r)。

  悪用報告と公開 PoC はありません。`use cache` と Server Actions の 2 件は、10/15 時点で CVE も npm audit の項目もありません。
- **なぜ重要か**: CVE と npm audit の項目がないので、SCA ツールでは検出されません。15.x では sharp 0.34 系が残ることがあるため、`npm ls sharp` で版を確認する必要があります。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/nextjs-ships-out-of-band-patch-for-two.html) / [GHSA-673q-mjm6-r5xr](https://github.com/vercel/next.js/security/advisories/GHSA-673q-mjm6-r5xr)

### [2026-10-14] Drupal core の Field UI に「Critical」の RCE CVE-2026-108097 (SA-CORE-2026-014)。コントリビュートモジュール経由で未認証の到達経路あり
- **何が起きたか**: Drupal が 11.4.10 / 11.3.19 / 10.6.19 を出しました。原因は、Field UI のテーブル要素の pre-render が行ごとの `#region_callback` を検証せずに呼び出していたことです。8.8 から入っている「信頼できないコールバックは実行しない」制限の外側で実行されていました。Entity List モジュールにも同種の CVE-2026-108099 があります。公開 PoC と悪用報告はありません。
- **なぜ重要か**: 修正対象外の EOL ブランチに約 28.5% のサイトが残っています。render array のコールバックという sink は、カスタムモジュールのレビューでも同じように探せます。
- 出典: [Drupal SA-CORE-2026-014](https://www.drupal.org/sa-core-2026-014) / [The Hacker News](https://thehackernews.com/2026/10/drupal-patches-critical-core-rce-flaw.html)

### [2026-10-15] [続報] GhostAction の新しい波の規模を GitGuardian が公表: 約 1,900 アカウントを乗っ取り、30,000 超のリポジトリが標的に
- **何が起きたか**: 10/8〜9 の波で、悪性ワークフローが 3,174 件のシークレットの持ち出しを試みていました。新しい点は、件数が定量化されたこと、ペイロードに git 履歴を走査する機能が加わったこと、GitHub が 10/9 以降このワークフローの実行を止めていることです。
- **なぜ重要か**: 過去の波の被害者が再び狙われています。原因はシークレットを回していないことです。自組織のリポジトリに `security-audit.yml` などの見慣れない workflow が入っていないか確認し、トークンを回す必要があります。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/ghostaction-compromises-about-1900.html)

### [2026-10-14] Unit 42、FortiManager の CVE-2024-47575 を起点に FortiGate へメモリ常駐型の ARM64 インプラント「PEERSTITCH」を仕込んだ侵入を報告
- **何が起きたか**: 通信系 MSP への侵入 (CL-STA-0954 / UNC5820) です。攻撃者は FortiManager から 500 台超の管理対象 FortiGate の設定と鍵の材料を持ち出しました。続いて FortiOS の CVE-2025-61624 を使い、待ち受けポートも外向き通信も持たない PEERSTITCH を展開しました。
- **なぜ重要か**: 管理サーバーが一台破られると、配下の全機器と顧客ネットワークの設定が漏れます。設定の持ち出しを前提に、鍵と証明書を再発行する範囲を検討する必要があります。
- 出典: [Unit 42](https://unit42.paloaltonetworks.com/fortimanager-cve-2024-47575-peerstitch-malware/)

### [2026-10-15] Citizen Lab、Candiru のスパイウェアがターゲティング広告を経由してゼロクリックで Al Jazeera の端末に感染していたことを確認
- **何が起きたか**: Discover-Tech の広告が端末の広告 ID と IP を送り、標的と判定した端末にだけ攻撃コードを返していました。2024〜25 年に少なくとも 45 台が標的になっています。Google と IAB Europe は同社を承認ベンダーから外しました。IOC も公開されています。
- **なぜ重要か**: 広告そのものには攻撃コードが入っていないため、広告ネットワーク側では検出できません。広告配信のサプライチェーンが実際の攻撃経路になると確認された初めての公開事例です。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/citizen-lab-traces-zero-click-candiru.html) / [The Record](https://therecord.media/spyware-citizen-lab-advertising)

### [2026-10-14] Rapid7、Zimbra Collaboration Suite に 80 件超の脆弱性を報告し、連載の第 1 回 (認証とメールボックス境界) を公開
- **何が起きたか**: 取り上げたのは次の 3 種類です。
  - Modern クライアントの GraphQL 経由のログイン失敗が、送信元 IP のロックアウト計数に入らない (CVE-2026-93637)。
  - 認証済みユーザーが他人を名乗ってメールを送れる。
  - EWS を有効にしたアカウントから、他人のメールボックスを読める。

  修正済みの項目には、GitHub で脆弱版と修正版の差分が付いています。続く回では XSS → SSRF → root までの連鎖を扱う予定です。
- **なぜ重要か**: 「同じ認証処理に別のフロントエンド (GraphQL) から入ると、レート制限やロックアウトを素通りする」というバグクラスです。REST と GraphQL を併設している他の製品でも同じ確認ができます。
- 出典: [Rapid7](https://www.rapid7.com/blog/post/ve-breaking-zimbra-identity-boundaries-part-1)

### [2026-10-15] AUR に yay / paru を装ったパッケージ。インストール時に root 権限でリモートのスクリプトを実行
- **何が起きたか**: アカウント「marchos1as」が 10/13 から `yyay` などの typosquat パッケージを大量にアップロードしていました。中身は正規のソースに悪性のインストールスクリプトを足したものです。AUR はアカウントを停止し、パッケージを削除しました。npm の「DirtyBlanket」と同じ配布元 (GitFlic) を参照しています。
- **なぜ重要か**: 開発者端末にはビルド時に root で実行される経路があります。インストールしていた場合は侵害を前提に対応する必要があります。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/fake-arch-linux-packages-push-malware-with-root-privileges/)

### [2026-10-15] [続報] フランスのスーパーの冷蔵設備への攻撃、Copeland / Dixell XWEB にも拡大し被害は約 700 店舗
- **何が起きたか**: CERT-FR が対象に Copeland と Dixell の XWEB を加えました。被害店舗数は当初報道の 300〜350 から約 700 に増えています。Danfoss の被害機器の多くは EOL 機です。Censys の計測では、露出していた端末は更新ではなく切断によって減っていました。
- **なぜ重要か**: 新しい点は、ベンダーが 2 社増えたことと、被害規模が明らかになったことです。EOL の OT 機器は初期化しても再び侵害されるため、ネットワークから外すことが唯一の対策です。
- 出典: [SecurityWeek](https://www.securityweek.com/supermarket-refrigeration-attack-widens-to-copeland-dixell-controllers/)

### [2026-10-14] Trail of Bits、25 のパッケージマネージャを「侵害されたリポジトリ」に対して検証。署名を既定で検証するのは Go だけ
- **何が起きたか**: mitmproxy を使った試験環境でリポジトリの改ざんを模擬しました。既定で lockfile のハッシュによる改ざん検出が働くのは半数未満でした。cpanminus は既定で HTTP を使っています。
- **なぜ重要か**: 開発者アカウントではなく配信サーバーを狙うサプライチェーン攻撃に、エコシステムごとにどこまで耐えられるかの一覧になっています。ビルド環境の設定を見直すときの基準に使えます。
- 出典: [Trail of Bits](https://blog.trailofbits.com/2026/10/14/package-managers-have-an-integrity-problem/)

### [2026-10-15] GreyNoise、D-Link NAS や Ubiquiti NVR などの既知脆弱性を突いて帯域共有アプリを無断で入れる proxyjacking を報告 (143 台、34 か国)
- **何が起きたか**: 侵入には CVE-2024-3272 / 3273 (D-Link)、Log4Shell (UniFi Video)、CVE-2025-31324 (SAP) などが使われ、その後 Pawns.app が設置されていました。SSH 鍵による予備の侵入経路も設定されていました。
- **なぜ重要か**: 自組織の IP が住宅プロキシとして第三者の不正通信に使われ、ブロックや調査の対象になるおそれがあります。EOL のエッジ機器を棚卸しする理由になります。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-hijack-d-link-ubiquiti-devices-to-resell-your-stolen-bandwidth/)

### [2026-10-14] FBI と北マケドニア警察、サイバー犯罪マーケット OLVX の管理者とされる人物を逮捕
- **何が起きたか**: OLVX は 2023〜25 年に 1,500 超の出品者アカウントを通じて、個人情報や認証情報を販売していたとされます。
- **なぜ重要か**: 認証情報の流通経路の一つが止まったことになります。押収したデータから、被害の通知が後に出てくる可能性があります。
- 出典: [The Record](https://therecord.media/olvx-cybercrime-marketplace-arrest-north-macedonia)

### [2026-10-15] 英国 Legal Aid Agency の侵害、追加調査で 1978 年まで遡る記録の流出を確認 (2007 年以前の記録は約 25 万件)
- **何が起きたか**: 2025 年 4 月の侵害について、LAA が流出データの範囲を更新しました。同じ日に、CenterPoint Energy もテキサス州だけで 1,062,060 人の個人情報が流出したと届け出ています。
- **なぜ重要か**: 長期間保存しているデータは、侵害されたときの被害範囲を広げます。データ保持方針を見直す必要を示す事例です。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/uk-legal-aid-agency-hackers-stole-records-dating-back-to-1978/) / [SecurityWeek](https://www.securityweek.com/centerpoint-energy-data-breach-impacts-1-million-texans/)


## 新規 CVE / Advisory (バリアントハント起点候補)
> 採用基準: NVD の公開日が 2026-10-14〜16 で、過去のダイジェストに出ていないもの。OSS または修正コミットを特定できるものを優先し、プロトコル仕様由来のバグや共通の sink など、他の実装にも横展開できるバグクラスを選びました。KEV は 2026-10-15 版、EPSS は FIRST の 2026-10-15 値です。

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-15176 | NGINX OSS/Plus 0.1.29〜1.31.6 (修正 1.30.6 / 1.31.7) | CWE-122 / v4 9.2 | alias のある location で rewrite が URI を短くした直後に `$request_filename` を評価 → URI→パス変換でバッファ長を誤計算 → ワーカーのヒープオーバーフロー (DoS、条件次第で RCE) | [f8a2342](https://github.com/nginx/nginx/commit/f8a23425bd6840c4c36b4264edf576ba3646156f) | KEV なし / EPSS 0.0052 / 2005 年からある欠陥 |
| CVE-2026-93479 | NGINX 1.30.0〜1.30.5、1.31.2〜1.31.6 | CWE-122 / v4 9.2 | 正規表現 map のキャプチャを root や log_format が map 出力より先に参照 → 7 月の修正 (CVE-2026-42533) 後の長さ計算が予約領域ぶんあふれる → ヒープオーバーフロー | [6aa4b3f](https://github.com/nginx/nginx/commit/6aa4b3fdd4fdc156153f2981eb4070690624447c) | KEV なし / EPSS 0.0055 / 修正による退行 |
| CVE-2026-97205 | NGINX 0.8.11〜1.31.6 | CWE-416 / v4 9.2 | AIO を有効にして SSI の `include virtual` を並列処理 → 8bit の保留カウンタを確認なしで加算して一周 → リクエストの解放後参照 (UAF) | [6adfc05](https://github.com/nginx/nginx/commit/6adfc05ece48f92446383ec1f145446848694698) | KEV なし / EPSS 0.0044 |
| CVE-2026-97629 | NGINX 1.23.2〜1.31.6 (`ssl_session_cache shared` を使い、`ssl_session_ticket_key` 未指定) | CWE-908 / v4 8.3 | チケット鍵の自動ローテーションで 3 スロット中 2 つしかコピーしない → 未初期化スロットで復号と検証 → セッションを偽造してクライアント証明書の検証を回避 (非決定的) | [1916f26](https://github.com/nginx/nginx/commit/1916f26e6ca49296568633d309777e36527e5bb2) | KEV なし / EPSS 0.0018 / mTLS 環境は要確認 |
| CVE-2026-102946 / GHSA-4pp3-559j-c5c2 | joserfc (Python) < 1.7.4 | CWE-347 / 9.1 | JWS General JSON の `signatures` が空配列 → 検証ループが一度も回らず「失敗なし = 成功」と判定 → 署名のない payload を真正として受理 | [f409f8f](https://github.com/authlib/joserfc/commit/f409f8f058225d7686acab6546c94593e4c1bfbe) | KEV なし / EPSS 未算出 / 他の JOSE 実装にも横展開しやすい |
| CVE-2026-111235 | OpenNMS Meridian (< 2024.3.14 / 2025.0.11 / 2026.0.1)、Horizon < 36.0.5 | CWE-863 / 9.1 | Spring Security の `/rest/**` の intercept-url が大文字の HTTP メソッド名を大小区別して照合し、最後に deny 規則がない → 大文字でないメソッド名はどの規則にも当たらない → REST API を未認証で読み書き | [PR #8934](https://github.com/OpenNMS/opennms/pull/8934) | KEV なし / EPSS 未算出 / 同じ設定パターンの Spring アプリに横展開できる |
| CVE-2026-59774 / GHSA-6v53-hr58-556r | Gitea < 1.27.1 | CWE-22 / 9.8 | 公開リポジトリのマークアップ描画エンドポイントで Org-mode の INCLUDE 指令を制限していない → サーバー上のファイルを読める → app.ini の INTERNAL_TOKEN を得て hook を改ざんし RCE | [PR #38642](https://github.com/go-gitea/gitea/pull/38642) / [#38645](https://github.com/go-gitea/gitea/pull/38645) | KEV なし / **EPSS 0.283 (98 パーセンタイル)** |
| CVE-2026-57155 / GHSA-wjqq-rfmm-v5h3 | OPNsense < 26.1.11 | CWE-22, CWE-78 / 9.9 | Alias 編集権限のあるユーザーが GeoIP の取得元 URL を指定 → アーカイブ内 CSV の country_code をファイル名にそのまま使う → root で任意ディレクトリへ書き込み、cron 経由で root 実行 | [c46aced](https://github.com/opnsense/core/commit/c46aced9c47d956167e294911113bc334fea5f48) / [e7fbfaa](https://github.com/opnsense/core/commit/e7fbfaa7f5e070da667e3f243da11fd3d4b731fa) | KEV なし / EPSS 未算出 / 低権限から FW 全体を奪取 |
| CVE-2026-94200 / GHSA-m5mh-q53w-67jq | Erlang/OTP ssl 10.3〜 (修正 OTP 27.3.4.19 / 28.5.0.8 / 29.1.2) | CWE-1288 / v4 8.2 | TLS 1.3 クライアントが NewSessionTicket の拡張を EncryptedExtensions の規則で解釈 → 本来ありえない長さ 0 の early_data を保存 → 再開時に共有チケットストアが落ち、ノード全体の ssl が停止 | [00a333b](https://github.com/erlang/otp/commit/00a333bcf2800b69f540369b54167e897dae7219) ほか | KEV なし / EPSS 0.0047 / 「メッセージ種別ごとに拡張を検証しているか」は他の TLS 実装でも確認できる |
| CVE-2026-55103 / GHSA-jw39-rch6-mhwf | discourse-activity-pub (修正 commit 1c8518b 以前) | CWE-345, CWE-863 / 8.6 | 受信した ActivityPub で、署名済みリクエストの actor と Activity の actor、投稿の所有者が一致するかを確認していない → 他人の連合投稿を編集・削除できる | [1c8518b](https://github.com/discourse/discourse-activity-pub/commit/1c8518b0f2abdf31cbea3e0b242f74d8994a9ba5) | KEV なし / EPSS 未算出 / 他の Fediverse 実装にも同じ確認が有効 |
| CVE-2026-100409 / GHSA-2vc4-c4r6-p6v6 | @opennextjs/cloudflare 0.3.0〜1.20.1 (enableCacheInterception 有効時) | CWE-177 / 7.5 | middleware の照合とキャッシュの照合で、パーセントエンコードの正規化がずれている → 認可の middleware を通らずに保護ルートのキャッシュが当たる → 未認証で保護コンテンツを取得 | [38ea40b](https://github.com/opennextjs/opennextjs-cloudflare/commit/38ea40b669be272ddf09a7df7e70c69d0b57404b) | KEV なし / EPSS 未算出 / エッジキャッシュと認可の不整合という型 |
| CVE-2026-47218 / GHSA-cc25-vq59-rcjx | runwasi containerd-shim-wasmtime < 0.6.1 | CWE-502 / v4 9.3 | OCI イメージのレイヤーに入っている precompiled バイト列を、信頼できるキャッシュとして扱う → Wasm の検証を経ずにネイティブコードとしてデシリアライズ → WASI サンドボックスを抜けてコンテナ権限で実行 | [d28ab73](https://github.com/containerd/runwasi/commit/d28ab73c2c8a6c50d1927078821bd418b9e51638) | KEV なし / EPSS 未算出 |

### 公開日 (NVD published、UTC)
- CVE-2026-15176 / CVE-2026-93479 / CVE-2026-97205 / CVE-2026-97629: 2026-10-14 (F5 CNA。同日公開の CVE-2026-95101 (HTTP/3 のリクエスト注入) の修正は [1c173a2](https://github.com/nginx/nginx/commit/1c173a2d8767730e678c27446138d7ae5dd6fd64))
- CVE-2026-102946: 2026-10-15
- CVE-2026-111235: 2026-10-15
- CVE-2026-59774: 2026-10-14 (oss-security への初出は 2026-08-10 で、NVD への登録が遅れたもの)
- CVE-2026-57155: 2026-10-15
- CVE-2026-94200: 2026-10-14
- CVE-2026-55103: 2026-10-15
- CVE-2026-100409: 2026-10-15
- CVE-2026-47218: 2026-10-15

### 今日の CVE 所感
- **「検証ループが空なら成功」「どの規則にも当たらなければ許可」**: joserfc と OpenNMS は、どちらも否定の判定が既定になっていない (fail-open) 型です。JOSE、SAML、Spring Security、その他の ACL 実装で、空集合のとき・どの規則にも当たらなかったときの扱いを grep で横断的に確認する価値があります。
- **正規化の不一致**: OpenNext (パーセントエンコード)、OpenNMS (メソッド名の大小)、NGINX Ingress の CVE-2026-94197 (X-Forwarded-* をそのまま認可のサブリクエストへ転送)、eclipse-ecsp api-gateway の CVE-2026-110723 (XFF の左端の値を信頼) は、どれも「認可で見る値と実際に処理する値がずれる」型です。リバースプロキシやゲートウェイの診断で使える観点です。
- **NGINX**: 修正による退行 (CVE-2026-93479) と、20 年来の欠陥 (CVE-2026-15176) が同時に出ています。ディストリビューションのパッケージに修正がバックポートされたかを確認し、nginx を同梱している製品 (Ingress、アプライアンス) を洗い出すのが今週の優先作業です。
- **Gitea**: CVE-2026-59774 は EPSS が高いので最優先です。同時に出た CVE-2026-71184 / CVE-2026-66877 (fork の workflow が承認ゲートを回避する。PR #39005 / #39018) も、セルフホストの CI を持つ組織では要確認です。
- **その他**: DPDK の lib/vhost (CVE-2026-86562、制御キューの TOCTOU による二重読み出し → ヒープオーバーフロー。修正は [6ec1778](https://git.dpdk.org/dpdk/commit/?id=6ec17781346e0fe4b566b6bf8f79be71f87c10e4)) は、前回扱った Linux vhost「Vghost」と同じく、ゲストが書き換えられるメモリの二重読み出しという型です。他の vhost-user 実装にも同じ観点が当てはまります。

## 日本国内のセキュリティ動向

### 国内インシデント・事故

#### [2026-10-15] ソースネクスト、会員情報取得 API が悪用され最大 2,251 万件の会員情報が流出
- **何が起きたか**: ソースネクストが 10/15 に公表した。会員情報を管理するシステムに、10/9 10時頃から第三者が「会員情報取得 API」を不正に使ってアクセスし、登録者の情報を取得していた。同社は 10/13 9時頃にこれを確認し、13:36 に封じ込めを終えた。流出の可能性があるのは 22,519,960 件で、項目はメールアドレス、パスワード、氏名・カナ、住所、性別、電話・FAX、生年月日、会社名・役職・部署、加入サービスや登録日などの識別情報。クレジットカード情報は対象システムに保存されていなかった。ログイン時にパスワードの再設定を求めている。10/15 に個人情報保護委員会へ報告済みで、10/16 に警察へ被害を申告する予定。パスワードの保管形式 (ハッシュ化の有無) は公表文に書かれていない。
- **なぜ重要か**: 正規の API を 4 日間使われ続け、2,000 万件を超える情報を抜かれた。この規模の取得が検知されなかった点から、レート制限や件数の異常を監視する仕組みがなかったとみられる。JPCERT/CC が同じ日に公開した「アプリ解析 → API 悪用」型の攻撃の記事 (下記) と同じ系統の可能性があり、診断では API ごとの認可 (IDOR/BOLA) と大量取得への耐性を必ず確認する項目にすべき。
- 出典: [ソースネクスト](https://www.sourcenext.com/support/i/2026/1015_info/)

#### [2026-10-15] ビューティガレージ (東証プライム) の EC サイトに 3 日間不正侵入、775,725 件の顧客情報が漏えい
- **何が起きたか**: 美容業務用品 EC のビューティガレージが 10/15 に適時開示した。10/10〜10/12 にサーバーへ不正に侵入され、10/13 に顧客情報の流出を検知した。漏えいが確認されたのはグループ全体の顧客情報 775,725 件で、項目はサロン名、氏名、メールアドレス、電話番号など。住所、購入履歴、決済情報は流出していないとしている。侵入できた経緯は調査中。
- **なぜ重要か**: 3 連休を狙って侵入され、休み明けに検知された。7 月以降に続いている小売・EC への侵害の 1 件で、侵入経路が公表されるまでは、自社 EC の公開面 (管理画面、プラグイン、API) を点検しておくのが妥当。
- 出典: [TDnet 適時開示 (ビューティガレージ)](https://www.release.tdnet.info/inbs/140120261015551741.pdf)

#### [2026-10-15] ACCESS の台湾子会社が提供する越境 EC 支援サービス「CROS」に不正アクセス、BI ツールが侵入口に
- **何が起きたか**: ACCESS (4813) が 10/15 に適時開示した。子会社 ACCESS AP TAIWAN が海外進出する EC 事業者向けに提供する「CROS」のサーバーが侵害された。異常は 9/11 に検知している。侵入の起点は、取引先 1 社だけに提供していた BI ツールだった。漏えいを確認したのは、顧客 ID 155,280 件と受注 ID 231,998 件 (氏名、電話、住所、メール。対象は台湾、香港、マカオ、シンガポール) と、決済が完了していない受注のクレジットカード情報 1,305 アカウント分 (うち 4 件はセキュリティコードを含む全項目)。さらに、サーバーから盗まれたメール送信サービスの鍵を使って、攻撃者が用意した別のリストへ不正なメールが 11,441 件送られた。
- **なぜ重要か**: 1 社向けに追加した BI ツールが、マルチテナント基盤全体への入口になった。サーバー上に置かれた外部サービスの API 鍵 (メール送信) が窃取され、なりすましメールの配信に使われた点も重要。診断では、付帯ツールの公開範囲と、サーバー上に平文で置かれた外部サービスの秘密情報を確認すべき。
- 出典: [TDnet 適時開示 (ACCESS)](https://www.release.tdnet.info/inbs/140120261015551574.pdf)

#### [2026-10-15] [続報] メドレーが「アットリンク」への不正アクセスを適時開示で正式に公表、影響の可能性があるのは最大 787 医療機関
- **何が起きたか**: これまでは医療機関のサイトに案内が載っていた段階だった。メドレーは 10/15 9:00 に適時開示で、産婦人科向けの業務支援システム「@link」、患者アプリ、周辺サービスへの不正アクセスを確認したと正式に公表した。新たに分かったのは次の点。10/11 に外部の専門機関から情報提供を受けたことが発覚のきっかけだった。漏えいの可能性がある医療機関は最大で、利用している全 787 施設。情報の項目と範囲は調査中。サービスは 10/14 深夜から停止しており、再開の時期は未定。
- **なぜ重要か**: 自社で検知したのではなく、外部からの通報で発覚した。産婦人科の患者情報 (妊娠・不妊治療など) は要配慮の性質が強い。予約・受付・エコー動画の配信まで止まっており、SaaS 1 つの停止が多数の医療機関の業務に一斉に波及した例になった。
- 出典: [TDnet 適時開示 (メドレー)](https://www.release.tdnet.info/inbs/140120261014550839.pdf) / [piyolog](https://piyolog.hatenadiary.jp/entry/2026/10/15/065625)

#### [2026-10-15] [続報] イエローハットの WEB 作業予約システムの漏えい件数が 1,797,124 名で確定、住所・生年月日・ログイン ID も追加
- **何が起きたか**: 8/28 の第一報 (最大 1,801,499 名) に続き、10/15 に第二報を出した。フォレンジック調査で、WEB 作業予約システムへの不正侵入による漏えいが 1,797,124 名分と確定した。漏えい項目には、第一報になかった住所、生年月日、性別、ログイン ID、パスワード (同社の説明では「復元できない状態」) が加わった。不正アクセスは 8/19 に検知している。個人情報保護委員会への確報は提出済み。侵入の具体的な手口は公表文に書かれていない。
- **なぜ重要か**: 調査が進んで件数は少し減ったが、漏えい項目は増えた。これは公表後によくある展開で、第一報の段階で項目を少なく見積もらないほうがよい。予約システムのような周辺システムでも会員 DB 全体に届く設計になっていた点に注意。
- 出典: [TDnet 適時開示 (イエローハット)](https://www.release.tdnet.info/inbs/140120261015551164.pdf)

#### [2026-10-15] [続報] ハルメク「HALMEK up」の管理画面への不正アクセス、最終報で 6 月から計 5 回のログインが判明
- **何が起きたか**: ハルメクホールディングスが 10/15 に最終報を出した。社員 1 名の ID とパスワードが不正に使われ、管理画面にアクセスされていた。フォレンジック調査で、発覚 (9/9) より前の 6/13、8/7、9/2、9/3 にも不正アクセスがあり、合わせて 5 回だったと分かった。ファイルを閲覧・取得・転送した痕跡は確認されなかった。
- **なぜ重要か**: 正規の認証情報で管理画面に入られ、約 3 か月気付かれなかった。管理画面がインターネットに公開されていて、ID とパスワードだけで入れたことが前提にある。診断では、管理画面の公開範囲 (IP 制限) と多要素認証の有無を指摘すべき典型例。
- 出典: [TDnet 適時開示 (ハルメク HD)](https://www.release.tdnet.info/inbs/140120261015551040.pdf)

#### [2026-10-15] [続報] 防災メール配信「SpeeCAN RAIDEN」(アルカディア) の件、東海 3 県の少なくとも 35 消防本部のシステムでも個人情報が漏えいした可能性
- **何が起きたか**: NHK が 10/15 18:40 に報じた。アルカディア (大阪・箕面市) への不正アクセスが疑われる問題で、愛知・岐阜・三重の少なくとも 35 の消防本部で、消防関係者が使うシステムなどの個人情報が漏えいした可能性がある。見出しは警察のシステムにも影響が及んだとしている。記事本文は会員登録が必要で、詳細までは確認できていない。
- **なぜ重要か**: 自治体の住民向け配信にとどまらず、消防や警察の職員向けの連絡網にまで影響が広がった。重要インフラに近い組織が同じ SaaS に依存していたことが表に出た事例。
- 出典: [NHK](https://news.web.nhk/newsweb/na/nd-20261015de60018)

### 国内の注意喚起・ガイドライン・政策

#### [2026-10-15] JPCERT/CC、連続不正アクセス事案の攻撃元サーバーを分析し、AI を使った APK 解析 → API 悪用・SSRF 検証の痕跡を公表
- **何が起きたか**: JPCERT/CC Eyes が「連続不正アクセス事案の攻撃手法に関する調査」を公開した。国内で相次ぐ情報漏えい事案について攻撃基盤を調べた結果、次のことを確認した。攻撃者は AI を使って既知の脆弱性をスキャンし、API 経由で攻撃していた。攻撃元サーバーには Android アプリ (APK) を解析して API を特定した跡があり、jadx と、Flutter アプリの解析ツール Blutter が置かれていた。SSRF の検証に使ったとみられる 302 リダイレクトサーバーの Python スクリプトもあった。日本以外の地域向けのサービスも標的になっていた。別のサーバーでは、MySQL、Jenkins、メールゲートウェイを狙うツールや、EDR を回避しようとした痕跡、Web シェルも見つかった。IoC として IP アドレス 3 件 (210.149.87[.]120 ほか) を公開している。推奨策は 4 つ。アプリに秘密鍵を埋め込まない、サーバー側で認証と認可を行う、レート制限と異常監視を入れる、リダイレクト後の宛先まで検証して SSRF を防ぐ。
- **なぜ重要か**: スマホアプリの解析から、そのバックエンド API を攻撃する流れを、国の CSIRT が攻撃基盤の実物で裏付けた。モバイルアプリの診断では、アプリ側の難読化に頼らない前提で、バックエンド API の認可、SSRF、署名ロジックの再現可能性まで調べる必要がある。
- 出典: [JPCERT/CC Eyes](https://blogs.jpcert.or.jp/ja/2026/10/web_api_attacks.html)

#### [2026-10-15] 警察庁「サイバー警察局便り Vol.20」、流出したメールアドレスを狙う偽メールに注意を呼びかけ、事業者に DMARC「reject」とパスキーを要請
- **何が起きたか**: 相次ぐ情報漏えいを受け、流出したメールアドレスに偽メールが届いて二次被害につながるおそれがあるとして注意を呼びかけた。サービスを提供する事業者には、DMARC を導入して受信拒否 (p=reject) に設定することと、パスキーなどの多要素認証を導入することを求めている。
- **なぜ重要か**: 警察庁が「p=reject」という具体的な設定値まで示した。上の ACCESS の件のように、窃取したメール送信用の鍵で正規のドメインから送られると DMARC では防げない。送信基盤の認証情報の管理も合わせて点検すべき。
- 出典: [警察庁 サイバー警察局便り Vol.20 (PDF)](https://www.npa.go.jp/bureau/cyber/pdf/R8_Vol.20cpal.pdf)

### 国内製品の脆弱性 (JVN)

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|---|---|---|---|---|---|
| 2026-10-15 | JVN#94004488 / CVE-2026-75559 (JVNDB-2026-000151) | 車検証閲覧アプリ Android/iOS ver.6.2.0 以前 (国土交通省) | 事業者向けの API 連携の仕様で、API のアクセス ID とアクセスキーが漏えいしうる (CWE-201)。漏えいしうる鍵は無効化済みで、開発者は「悪用は不可能」としている | v3 5.3 / v4 6.9 | [JVN](https://jvn.jp/jp/JVN94004488/) |
| 2026-10-15 | JVN#40460777 / CVE-2026-96614, CVE-2026-105271 (JVNDB-2026-000149) | ゲオアプリ Android/iOS Ver 11.8.6 以前 (ゲオ)。修正版は 11.8.8 | Custom URL Scheme の処理にアクセス制限がなく、アプリ内ブラウザで任意のサイトを開かせてフィッシングやセッション ID の窃取ができる。加えてパスワードを平文で保存している | v3 5.4 / 4.3 | [JVN](https://jvn.jp/jp/JVN40460777/) |
| 2026-10-15 | JVN#48627289 / CVE-2026-72528 (JVNDB-2026-000117) | Creema アプリ Android < 2.436.0 / iOS < 2.432.0 (クリーマ) | 細工した URL でアプリを起動させ、攻撃者のサイトをアプリ内に表示できるオープンリダイレクト | v3 4.3 / v4 5.1 | [JVN](https://jvn.jp/jp/JVN48627289/) |
| 2026-10-14 (登録 10-15) | JVNDB-2026-037831 / CVE-2026-47058 | Cosminexus Developer's Kit for Java / Hitachi Application Server ほか (日立、hitachi-sec-2026-136) | 同梱された Java の脆弱性 (ネットワーク経由、機密性・完全性への影響が高い) | v3 7.4 | [JVNDB](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-037831.html) |
| 2026-10-14 (登録 10-15) | JVNDB-2026-037832 / CVE-2026-41254 ほか | Cosminexus Developer's Kit for Java / Hitachi Developer's Kit for Java (日立、hitachi-sec-2026-135) | 同梱された Java の複数の脆弱性。最大は未認証でリモートから起こせる DoS | v3 最大 7.5 | [JVNDB](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-037832.html) |
| 2026-10-14 (登録 10-15) | JVNDB-2026-037830 / CVE-2026-41254, CVE-2026-47058 ほか | Hitachi Command Suite、Automation Director、Configuration Manager、Ops Center 製品 (日立、hitachi-sec-2026-125) | 上の Java の脆弱性が波及したもの。全バージョンが対象 | ベンダー情報を参照 | [JVNDB](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-037830.html) |
| 2026-10-14 (登録 10-15) | JVNDB-2026-037829 / CVE-2026-82715, CVE-2026-86573 | Hitachi Disk Array Driver for AIX / for Virtual I/O Server (日立、hitachi-sec-2026-137) | ローカルの低い権限から、完全性と可用性を損なえる (Scope: Changed) | v3 7.9 | [JVNDB](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-037829.html) |
| 2026-10-15 | JVNVU#95474776 (VU#948176) | 複数の TLS ライブラリ | 証明書チェーンでの委任 (名前制約) の強制を回避できる。10/14 の JVNVU#91265939 とは別件 | CERT/CC を参照 | [JVN](https://jvn.jp/vu/JVNVU95474776/) |
| 2026-10-15 | JVNVU#95613365 (VU#410595) | Google BoringSSL | SAN の検証ロジックで名前制約を回避できる問題が複数ある | CERT/CC を参照 | [JVN](https://jvn.jp/vu/JVNVU95613365/) |
| 2026-10-14 | JVNVU#90141693 | Siemens 製品 (2026 年 10 月の月例更新。CVE-2024-3596 の RADIUS「Blast-RADIUS」を含む) | Siemens 月例アドバイザリの JVN 転載。国内の工場や OT で広く使われている | 製品ごと | [JVN](https://jvn.jp/vu/JVNVU90141693/) |

### 国内コミュニティ・研究・イベント

#### [2026-10-15] ラック、国内の Web 漏えい公表を独自集計: 119 件のうち 68% が 7 月以降、サイバー救急センターの出動に占めるサーバ侵入は 30% → 52%
- **何が起きたか**: LAC WATCH の注意喚起記事。公開情報を独自に集めると、10/6 時点で 119 件あり、そのうち 81 件が 7 月以降に公表されていた。被害業種に占める小売・EC の割合は、1〜5 月の 4.5% から 6〜9 月に 23.6% へ上がった。サイバー救急センターの 7〜9 月の出動では、サーバへの不正侵入が 52% (前の四半期は 30%) で、侵入経路の約 7 割は ID の不正利用と Web アプリの脆弱性だった。盗まれた認証情報で Vertex AI 経由の Claude や Amazon Bedrock を大量に使われた事例も確認している。一方、JSOC が観測した攻撃通信の総量は大きく増えておらず、ラックは「少ない試行で弱点を突く精度型の攻撃」という仮説を示している。事案を認知してから初回公表までの日数は、5 月の平均 10.9 日から 9 月は 2.9 日 (中央値 1 日) に縮んだ。
- **なぜ重要か**: 公表件数の急増には、攻撃の増加だけでなく、企業の開示が早くなったことも効いていると数字で示した。通信量が増えていないのにサーバ侵入が増えている点は、スキャンが目立たないまま的確に侵入される状況を意味し、WAF や IDS の検知件数だけで安心できない。
- 出典: [LAC WATCH](https://www.lac.co.jp/lacwatch/alert/20261015_004996.html)

#### [2026-10-15] GMO サイバーセキュリティ by イエラエ「相次ぐ不正アクセスに備える 3 つのポイント」: CVE に載らない「シャドー脆弱性」と ASM の非対称性
- **何が起きたか**: GMO サイバー犯罪対策センターがブログを公開した。冒頭で、グループ会社の GMO リサーチ&AI の漏えいについて謝罪している。本文では多数の対応事案から傾向を挙げた。1 つ目は、CVE に記載されていない系統のバージョンやサポート切れ版も、攻撃コードを少し変えれば同じ脆弱性を突ける「シャドー脆弱性」を、攻撃者が AI で探している点。2 つ目は、外部からの非破壊検査ではバージョンが分からず、パッチ適用を強く求められない ASM の限界。
- **なぜ重要か**: CVSS や KEV で優先度を付ける運用や、外形の ASM だけでは漏れが出ると、診断会社が自ら指摘した。診断の報告では、バージョンが不明な資産についても「影響が否定できない」と明記して、対応を促す必要がある。
- 出典: [GMO サイバーセキュリティ by イエラエ](https://gmo-cybersecurity.com/blog/20261014/)

#### [2026-10-15] 日本ハッカー協会の杉浦隆幸氏、「攻撃者と対等な条件に立つ ASM 運用」(DEF CON Recon Village の Live Recon で優勝した経験から)
- **何が起きたか**: ScanNetSecurity が講演の内容を報じた。杉浦氏は、ASM は脆弱性を見つけるためのものではなく、攻撃される前に守るための取り組みだと述べた。DEF CON の Recon Village では、公開情報だけで実在する組織の攻撃面を洗い出す競技 Live Recon (4 人 1 組で約 48 時間) で優勝している。10/22 には Security Days Fall 2026 Tokyo で「AI で進化するランサム攻撃と OSINT」を講演する予定。
- **なぜ重要か**: 偵察 (OSINT) の実戦的な方法論は、外部診断や TLPT の事前調査の質に直結する。
- 出典: [ScanNetSecurity](https://scan.netsecurity.ne.jp/article/2026/10/15/56467.html)

#### [2026-10-15] MBSD、Black Hat USA 2026 で SpecterOps のトレーニング「Identity-driven Offensive Tradecraft」を受講したレポートを公開
- **何が起きたか**: 三井物産セキュアディレクションのペンテスターが技術者ブログに書いた参加レポート。4 日間のトレーニングで、AD、ADCS、SCCM、Entra ID の権限設定の不備を突く攻撃と、ブルーチーム側でそれをどう検知できるかを学んだ。SCCM の TAKEOVER、GOAD、sccmhunter、PetitPotam などを紹介している。
- **なぜ重要か**: 社内ペンテストや TLPT では、ID 基盤の設定不備を突く攻撃が中心になってきている。国内の担当者にとって、検証環境とツールを揃える際の参考になる。
- 出典: [MBSD 技術者ブログ](https://www.mbsd.jp/research/20261015/black-hat-usa-2026---adversary-tactics-identity-driven-offensive-tradecraft/)

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 90 (AI 24 フィード・一覧 + 個別記事約 30 / セキュリティ 33 (指定フィード 19 + 補足フィード + CISA KEV JSON / NVD API 1,275 件 / FIRST EPSS) / 国内 約 30 (JVN・JVN iPedia・JPCERT/CC・IPA・piyolog・Security NEXT・ScanNetSecurity・ITmedia・LAC・GMO イエラエ・MBSD・Flatt・トレンドマイクロ・警察庁・国家サイバー統括室・PPC・総務省・消防庁・TDnet) + WebSearch 約 15 回)
- 採用件数: AI技術=12 / AIセキュリティ=8 / セキュリティ=14 / CVE=12 / 国内インシデント=7 / 国内政策=2 / JVN=10 / 国内コミュニティ=4
- 除外理由内訳: 古すぎ=約 30 (10/13 以前の掲載、または期間内掲載だが一次発表が 9/20〜10/8 の再掲) / 重複=約 70 (直近 7 日の既出: PAN-OS CVE-2026-0322、Cisco SEG、Nextcloud/Collabora、Ivanti、curl、AhsayCBS、Docker Hub、Gemini 4 Argon、XBOW、Vghost、SiteGuard、アエナ、IDARE、銀のさら、戸田建設、SpeeCAN 初報、警察庁・Microsoft・JC3 の PhaaS 無害化 (10/15 の警察庁広報資料は既報内容の正式発表のため不採用) など) / 日付・一次情報不明=約 6 (日テレ Wands、Lili、TOPPAN ペイメンツ、ThreatsDay 内の個別項目など)
- セクション間の重複整理: Langflow CVE-2026-105740 は AI セキュリティに一本化。NGINX は深掘りとニュース・CVE 表の双方に掲載 (ニュースは要約のみ)。
- 10/16 (JST) 公開の記事は、生成時刻 (05:15 JST) の時点では国内・海外とも確認できなかった。
- 取得失敗ソース:
  - CISA advisories / ICS / news の XML: Access Denied → KEV JSON で代替。
  - GitHub API・コミットの .patch: 403 → 修正コミットは NVD の参照と記事中のリンクで対応付けた (NGINX の CVE とコミットの対応は THN 記事のリンク文脈に基づく)。
  - Google Threat Intelligence RSS: 0 件。
  - Dark Reading の個別記事: Cloudflare チャレンジ / 403 → SneakPeek は CSO Online と PR Newswire で確認。
  - OpenAI の記事ページ: 403 → RSS のみ確認し、本文で裏付けできないため不採用。
  - VentureBeat RSS: 429 (代替なし)。MSRC RSS: XML パース不可。
  - drupal.org の SA ページ: JS 必須 → RSS と THN で確認 (Drupal は修正コミット不明)。
  - Metasploit / nuclei-templates の releases.atom: 取得不可。
  - 国家サイバー統括室・PPC・総務省の新着一覧: JS 描画 → 日付入り URL の直接確認、Shift_JIS の一覧デコードで代替。
  - NHK の記事本文: 会員登録が必要でリード文のみ確認。
  - 日経の適時開示ページ: 有料 → TDnet の PDF を直接取得。

</details>
