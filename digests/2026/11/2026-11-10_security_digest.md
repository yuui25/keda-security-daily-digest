# KEDA Daily Digest — 2026-11-10 (JST)

> 採用範囲: 公開日 2026-11-08 〜 2026-11-10
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

週明けの月曜 (米国時間 11/9) に、AI でもセキュリティでも大きなニュースが重なった。AI 側では、Anthropic が **Claude Fable 5.2 / Mythos 5.2** を出した。Fable は入力 100 万トークンあたり 8 ドルに値下げされた。セキュリティ向けの Mythos 5.2 は、社内の評価「CVE Rediscovery」(修正前のコードから既知の CVE をどれだけ見つけ直せるか) で 89.6% を記録した。Meta は軽量モデル **Muse Ember** を、Google は TPU の強化版 **TPU 8tx / 8i Max** を発表した。
セキュリティ側の最大の話題は、Wiz が報告した **Qubole の信頼関係の悪用** だ。データレイク SaaS の Qubole に許可していた AWS の IAM ロールを使って、攻撃者が複数の顧客の AWS アカウントに入り、Secrets Manager や S3 の中身を持ち出した。ほかに、CISA が **OpenSSH の sshole (CVE-2026-123158)**、**FreeSWITCH の SIP MESSAGE 経由のコマンド実行 (CVE-2026-116779)**、**IBM Aspera Faspex の権限昇格 (CVE-2026-123218)** を KEV に加えた。AI エージェントを攻撃に使う事例も、ドイツのホスティング事業者 Mittwald (MCP サーバーの欠陥が入口)、Acronis が分析した台湾の単独犯 (BOSSAI)、Operation Snowball (DeepSeek ベース) と 3 件続いた。
国内では、**ニトリ HD が最大 3,762 万件**、**シェアフル が個人最大約 750 万アカウント・法人約 7,500 社** の流出の可能性を 11/9 に公表した。アララ経由の件では、**セガが 219 万 6,044 件** と確定値を出した。警視庁は、銀座で **偽基地局 (IMSI キャッチャー)** を使った中国籍の男を、電波法違反で逮捕したと発表した (携帯電話の通信の妨害での摘発は全国初)。
**今日まず見るべき 2 件**: (1) 自社の AWS で、外部 SaaS に AssumeRole を許しているロールを洗い出す (深掘り参照)。(2) FreeSWITCH を外部に公開している環境の確認と 1.11.3 への更新 (KEV、期限 11/12)。

## 今日の深掘り

### Qubole (Idera 傘下のデータレイク SaaS) が使う AWS アカウントの認証情報で、攻撃者が顧客の IAM ロールを AssumeRole。Secrets Manager、SSM、Lambda の環境変数、S3 を持ち出した (Wiz、2026-11-09)

- **概要 (事実)**:
  - Wiz によると、攻撃者は 10/14〜10/26 に、Qubole の顧客の複数の AWS アカウントに入り、保管されていた秘密情報とデータを盗んだ。最初に異常に気づいたのは Sentra で、自社の顧客の環境で見つけて Wiz に知らせた。
  - 攻撃者は、Qubole のプラットフォームが顧客の環境に入るために使う AWS アカウント (805246085872) の認証情報を持っていた。その入手経路は公表されていない。
  - The Hacker News が確認した時点で、Qubole と Idera は自社サイトに声明を出していなかった。
- **技術的な中身**:
  - Qubole は顧客の AWS アカウントの中で動く。そのため顧客は IAM ロールを作り、信頼ポリシーで「Qubole の AWS アカウントからの AssumeRole」を許可する。AssumeRole の要求には、Qubole が発行する External ID を付ける必要がある。
  - Wiz の分析では、攻撃者の AssumeRole の要求はすべて正しい External ID を付けていて、受け付けられた。AWS の指針でも、External ID は秘密の値ではなく、ロールを参照できる人なら見える値とされている。つまり **「信頼されたアカウントを握られた時点で、External ID は防御にならない」** という構造だ。
  - 攻撃者が入ったロールの多くは、普段は使われていないものだった。ただ、どのロールも Qubole のアカウントを信頼したままだったため、要求は通った。
  - 侵入後の動き: Lambda の環境変数、Secrets Manager、SSM Parameter Store から認証情報を集めた。それを TruffleHog に通して有効か確かめた (被害者の AWS アクセスキー、Entra ID のクライアントシークレット、Okta のクライアント認証情報など)。S3 は、ロールで読めるバケットを手当たり次第に、時にはバケットごと、1 回のセッションで落としていた。
  - これとは別に、10/8〜10/11 には「Qubole 用に作られたとみられる顧客自身のアクセスキー」での侵入もあった。Wiz は、AssumeRole の悪用と結び付けていない。
  - CloudTrail の管理イベントには、AssumeRole とバケットの一覧は残る。しかし、どのオブジェクトを読んだかは、S3 のデータイベントかサーバーアクセスログがないと分からない。実際に、ログがなくて被害の範囲を特定できなかった被害者が複数いた。
- **背景・経緯 (背景引用)**:
  - 「第三者のための信頼関係を足場にして、多数の顧客に入る」構図は、2024 年の Snowflake の顧客環境への侵入 (認証情報の使い回し) や、2025 年 8 月の Salesloft Drift の OAuth トークンの悪用と同じ系統だ。
  - AWS の External ID は、もともと「混乱した代理人 (confused deputy)」問題、つまり他の顧客がベンダーをだまして自分のロールを使わせるのを防ぐための仕組みだ。ベンダーのアカウント自体が侵害された場合には、効かない。
- **なぜ今これが重要か (評価)**:
  - 攻撃者にとって「SaaS ベンダーのアカウント 1 つ = 多数の顧客の AWS への合鍵」だ。しかも、使わなくなったのに消されていない信頼ロールが、そのまま入口になった。クラウドの設定診断では、「信頼ポリシーで外部のアカウントを許しているロール」と「最終使用日」を必ず突き合わせたい。
  - 盗んだ秘密情報を TruffleHog で即座に検証し、Entra ID や Okta にまで横に広げている。被害は AWS の外 (IdP) にも及びうる、という前提で調べる必要がある。
- **読者が今日できること**:
  - IAM ロールの信頼ポリシーで `arn:aws:iam::805246085872:root` (Qubole) を許していないかを確認する。あわせて、外部のアカウントを信頼するロール全体を「最終使用日」つきで一覧にする (IAM Access Analyzer の外部アクセスの検出結果や `aws iam get-role` の `RoleLastUsed` が使える)。
  - 該当がある場合は、10/1 以降の CloudTrail で次を探す: `eventName=AssumeRole` かつ `userIdentity.accountId=805246085872` で、`sourceIPAddress` が AWS の外のもの。ロールのセッション名が `quiam-` で始まるもの。GetCallerIdentity の User-Agent が TruffleHog のもの。
  - 当たりがあれば、そのロールで触れた Secrets Manager、SSM、Lambda の環境変数の値をすべて入れ替え、IdP 側 (Entra ID、Okta) のサインインログも同じ IP で検索する。S3 のデータイベントが無効なら、この機会に有効にしておく。
- 出典:
  - [The Hacker News (2026-11-09)](https://thehackernews.com/2026/11/hackers-exploit-quboles-trusted-aws.html)
  - Wiz の技術分析と Sentra の検知は、上の記事の引用による (Wiz のブログ本文は未取得)

## AI 技術・トレンド

### [2026-11-09] Anthropic、Claude Fable 5.2 と Claude Mythos 5.2 を公開。Fable は入力 8 ドル / 出力 40 ドル (100 万トークンあたり) に値下げ
- **何が起きたか**:
  - Fable と Mythos は同じ基盤モデルだ。Fable はサイバーと生物の安全策を強めて全利用者に提供し、Mythos は審査を通った組織 (Cyber Verification Program など) にだけ提供する。
  - 価格は入力 8 ドル / 出力 40 ドル (Fable 5.1 は入力 10 ドル)。生成は 5.1 より最大 30% 速い。2.5 倍速の fast mode は入力 16 ドル / 出力 80 ドル。
  - ベンチマーク (Anthropic の発表): FrontierCode 2.0 で 49.1% (Opus 5.5 は 45.5%、GPT-6 Astra は 42.8%)、FrontierSWE v2 で 69.9%、OSWorld 2.1 で 89.3%。社内のサイバー評価 CyScenarioBench では Mythos 5.2 が 76.3% だった。
  - TechCrunch によると、Fable 5.2 は Enterprise Frontier Safeguards を通じてゼロデータ保持 (ZDR) にも対応した。
- **なぜ重要か (評価)**: 最上位モデルの値下げで、長時間のエージェント作業の費用が下がる。Anthropic 自身は、日常の作業には Opus 5.5 を勧め、Fable を「上に切り替える先」と位置付けている。用途に応じてモデルを使い分ける前提が、さらにはっきりした。
- 出典: [Anthropic (2026-11-09)](https://www.anthropic.com/claude-fable-and-mythos-5-2) / [TechCrunch](https://techcrunch.com/2026/11/09/anthropic-releases-new-mythos-and-fable-models-amid-rsi-concerns/) / [The Verge](https://www.theverge.com/ai-artificial-intelligence/1030005/anthropic-claude-fable-mythos-5-2)

### [2026-11-09] Mythos 5.2 の脆弱性の発見能力: 「CVE Rediscovery」で 1,829 件中 89.6%。Claude Security に Mythos 5.2 を搭載
- **何が起きたか**:
  - CVE Rediscovery は、修正前のプロジェクトのスナップショットを渡して、公開済みの CVE をいくつ独力で見つけられるかを測る社内の評価だ。10 月の実施 (1,829 件) で、Mythos 5.2 は 89.6% だった (Mythos 5.1 は 78.3%)。
  - 発表によると、あるセキュリティ企業では、Mythos 5.2 が見つけて確認されたバグの 6 件に 1 件を、他の最先端モデルはどれも見逃していた。Mozilla は「Firefox で発見数がおよそ倍になった」とコメントしている。
  - Fable 5.2 の安全策は、サイバーセキュリティ関連のタスクの大半をブロックする。Claude Enterprise の顧客は、コードベースを継続的にスキャンする「Claude Security」で Mythos 5.2 を使える。
  - Anthropic は、Mythos 5.2 が「評価されている」と疑う発言が最近のモデルで最も多かったことも開示し、評価の難しさを認めている。
- **なぜ重要か (評価)**: ソースコード診断の自動化の「上限」が、また一段上がった。一方、Fable では攻撃寄りのタスクがブロックされるので、診断業務で使う場合は Cyber Verification Program の申請の要否を確かめておきたい。
- 出典: [Anthropic (2026-11-09)](https://www.anthropic.com/claude-fable-and-mythos-5-2) / [TechCrunch](https://techcrunch.com/2026/11/09/anthropic-releases-new-mythos-and-fable-models-amid-rsi-concerns/)

### [2026-11-09] Meta、エージェント向けの軽量モデル「Muse Ember」を公開。入力 100 万トークンあたり 0.10 ドル
- **何が起きたか**: Meta Superintelligence Lab は、ツール呼び出し、コーディングの小さなタスク、ルーティング、抽出、長い文書の解析といった「エージェントが一日中繰り返す仕事」向けに Muse Ember を出した。画像や音声の入力にも対応する。Meta は「Muse Wonder が計画し、Muse Ember が量をこなす」と説明している。Muse ブランドの 4 つ目のモデルだ。
- **なぜ重要か (評価)**: 大きなモデルで計画し、安いモデルで大量に実行する構成が、各社の標準になりつつある。診断の自動化でも、大量の応答の分類や抽出のような単純作業を安いモデルに回す設計が現実的になる。
- 出典: [TechCrunch (2026-11-09)](https://techcrunch.com/2026/11/09/meta-releases-muse-ember-a-new-lightweight-model-for-agent-execution/)

### [2026-11-09] Google、TPU の強化版 2 機種を発表。機密計算に対応した「TPU 8tx」と、HBM 384GB の「TPU 8i Max」
- **何が起きたか**:
  - TPU 8tx は、TPU 8t と同じシリコンに、カスタムの AMD EPYC をホスト CPU として組み合わせた。ハードウェアの機密コンピューティング (Confidential Computing) で、推論の実行中もデータと重みを守るという。推論の遅延は TPU 8t の最大半分だ。
  - TPU 8i Max は、TPU 8i を 2 基まとめたパッケージだ。HBM は 384GB (33% 増)、帯域は 17.2TB/s (2 倍)、SRAM は 768MB (2 倍)。
  - 1 つの世代で 1 年に 4 機種を出すのは、Google として初めてだ。
- **なぜ重要か (評価)**: 「推論中のデータと重みを守る」ことが、ハードウェアの売り文句になった。機密データでファインチューニングする企業向けの訴求だ。ただし、機密コンピューティングの実装は、サイドチャネル研究の新しい標的にもなる。
- 出典: [@IT (2026-11-10)](https://atmarkit.itmedia.co.jp/ait/articles/2611/09/news088.html)

### [2026-11-09] OpenAI、ChatGPT Enterprise を AWS Marketplace で提供開始
- **何が起きたか**: OpenAI は、ChatGPT Enterprise を AWS Marketplace から購入できるようにした。既存の AWS の購買と請求の関係を使って、調達を簡単にするのが狙いだという。
- **なぜ重要か (評価)**: AWS の請求に載ることで、大企業での導入の稟議が通りやすくなる。Anthropic の Claude は Bedrock 経由で AWS に深く入っているが、OpenAI が同じ販路で競う形になる。
- 出典: [OpenAI (2026-11-09、RSS の要約で確認)](https://openai.com/index/chatgpt-enterprise-aws-marketplace)

### [2026-11-09] Automattic、AI で作った (バイブコーディングの) アプリを公開する基盤「Spacefast」を発表
- **何が起きたか**: WordPress.com を運営する Automattic は、AI で作ったアプリに、データベース、認証、ファイルのアップロード、メール、アクセス解析を提供する Spacefast を発表した。ChatGPT、Claude、Cursor などのエージェントや Git リポジトリと連携できる。Lovable や Emergent と競合する。
- **なぜ重要か (評価)**: 非エンジニアが作ったアプリが、認証やファイルのアップロードの機能つきで公開される流れが加速する。脆弱性診断の対象として、「AI が生成したアプリ + 共通の BaaS」の組み合わせが増えるので、BaaS 側の既定の認可設定 (行レベルのアクセス制御など) を見る機会が増えそうだ。
- 出典: [TechCrunch (2026-11-09)](https://techcrunch.com/2026/11/09/automattic-debuts-a-platform-to-deploy-vibe-coding-apps-amid-a-changing-internet/)

### [2026-11-09] Disney と Adobe、Disney 専用の生成 AI モデルを共同開発する複数年の提携
- **何が起きたか**: Adobe MAX で発表された。Adobe Firefly Foundry を使い、Disney の作品 (キャラクターの属性、環境、画風) で学習した専用モデルを作る。テーマパーク、クルーズ船、ESPN の映像にも使う。
- **なぜ重要か (評価)**: 大手の IP 保有者が「自社のデータだけで学習した、権利上安全なモデル」を選んだ。学習データの出所を説明できることが、生成 AI の商用利用の条件になりつつある。
- 出典: [The Verge (2026-11-09)](https://www.theverge.com/tech/1029773/disney-adobe-generative-ai-partnership)

### [2026-11-09] Apple、Logic Pro で Apple Intelligence の追加利用枠「Intelligence Usage Pack」(49.99 ドル) の販売を開始
- **何が起きたか**: OpenAI や Google Gemini のクラウドのモデルに頼る機能には利用上限があり、それを超えた分を買い切りで追加できるようにした。家族共有は不可で、未使用分は翌月以降に繰り越せるが、購入から 12 か月で失効する。最初の対象アプリは Logic Pro だ。
- **なぜ重要か (評価)**: 「OS に AI が無料で付いてくる」モデルから、従量課金に移り始めた。推論のコストを、端末メーカーも吸収しきれなくなっていることを示す。
- 出典: [The Verge (2026-11-09)](https://www.theverge.com/tech/1030084/apple-intelligence-usage-packs-ai-features-creator-studio-logic-pro)

### [2026-11-09] Amazon、MoE の「エキスパートの刈り込み」を組み合わせで評価する手法「HOPE」を公開
- **何が起きたか**: MoE のモデル (例: 256 のエキスパートを持つ Qwen3.5-122B では、約 250GB のうち 95% がエキスパート) から、使われにくいエキスパートを消してメモリを減らす研究だ。従来の手法はエキスパートを 1 つずつ独立に評価していたが、HOPE は「一緒に働くエキスパートの組」を考慮して、どれを消すかを決める。
- **なぜ重要か (評価)**: 学習し直さずに大型 MoE を小さくできれば、オープンウェイトの大型モデルを手元の GPU で動かしやすくなる。社内でローカル LLM を診断に使う場合の選択肢が広がる。
- 出典: [Hugging Face Blog (Amazon、2026-11-09)](https://huggingface.co/blog/amazon/higher-order-pruning-experts)

### [2026-11-09] NVIDIA と Elith、日本の統計に基づく金融向けの合成ペルソナデータ「Nemotron-Personas-Finance-Japan」を公開
- **何が起きたか**: 日本の公的統計に、家計の金融資産や金融リテラシーのデータを組み合わせた、100 万件規模のオープンな合成ペルソナのデータセットだ。損保ジャパン、東京海上 HD、福岡銀行、みずほ FG、明治安田生命、金融データ活用推進協会 (FDUA) が設計に意見を出した。
- **なぜ重要か (評価)**: 個人情報を使わずに、金融のエージェントを開発・評価できる。テスト環境に本番の顧客データを持ち込む慣行 (漏えいの温床) を減らす材料にもなる。
- 出典: [Hugging Face Blog (NVIDIA、2026-11-09)](https://huggingface.co/blog/nvidia/nemotron-personas-finance-japan)

### [2026-11-09] Sakana AI、初のモバイルアプリ「Sakana AI App (仮)」を開発中と発表。テスターを 11/15 まで募集
- **何が起きたか**: Sakana AI は、iOS と Android 向けのアプリのテスターを募った。デビッド・ハ CEO は「Sakana AI にとって新たな方向性」と説明した。同社はこれまで、金融と防衛の分野での導入や、複数のモデルを組み合わせる「Sakana Fugu」、オープンウェイトのモデルを日本語に特化させる「Sakana Namazu」を手がけてきた。
- **なぜ重要か (評価)**: 国内の AI 企業が、企業向けから一般消費者向けにも出てきた。中身はまだ公表されていない。
- 出典: [ITmedia AI+ (2026-11-09)](https://www.itmedia.co.jp/aiplus/article/2611/09/2000003008/)

### [2026-11-08] Shizuku AI、日本語の全二重 (話しながら聞く) 音声会話モデル「Shizuku-Duplex」を発表
- **何が起きたか**: 80 ミリ秒ごとに推論し、相づちを打ったり、相手が話し終わる前に返事を始めたりできる。音声を出す前に、台詞をテキストで書き出す「Inner Monologue」という処理を挟む。同社の比較では、全二重型の中で GPT-Live-1 に次ぐ性能で、J-Moshi などの既存の日本語モデルを上回った。
- **なぜ重要か (評価)**: 日本語でも、自然な音声の対話 AI が身近になった。裏返すと、電話でのなりすまし (ボイスフィッシング) に使える道具の質も上がる。
- 出典: [Shizuku AI ブログ (2026-11-08)](https://shizuku.ai/blog/1/) / [GIGAZINE (2026-11-09)](https://gigazine.net/news/20261109-shizuku-duplex-natural-conversation-ai/)

### [2026-11-09] トランプ大統領、60 Minutes で「AI 企業のトップに『刑務所に入る準備をしろ』と伝えた」と発言
- **何が起きたか**: AI の安全性について問われ、トランプ大統領は「リスクは彼らが言うほど現実的ではなく、管理できている」と述べた。さらに、司法省が大手 AI 企業のトップに逮捕をちらつかせ、相手が方針を「全面的に変えた」と主張した。企業名は明かしていない。民主党と AI の安全性で協力するかとの問いには「絶対に協力する」と答えた。
- **なぜ重要か (評価)**: 中間選挙後の議会の構成の変化と合わせて、米国の AI 規制の方向が読みにくくなっている。発言の真偽は確認できていない。
- 出典: [The Verge (2026-11-09)](https://www.theverge.com/ai-artificial-intelligence/1029802/trump-60-minutes-ai)

## AI セキュリティ

### [2026-11-07 公表 / 11-09 報道] ドイツのホスティング事業者 Mittwald、顧客の AI アシスタント向けの MCP サーバーの欠陥から侵入され、56 の顧客プロジェクトが侵害
- **何が起きたか**:
  - Mittwald (ノルトライン=ヴェストファーレン州、Web 制作会社向けのホスティング) は、攻撃者が 8 日間気づかれずに居座り、56 の顧客プロジェクトを侵害したと 11/7 (土) に公表した。
  - 入口は、顧客が自分の AI アシスタントを管理画面「mStudio」につなぐための MCP サーバーの欠陥だった。自社のコードの欠陥か、オープンソースの MCP ライブラリの欠陥かは分かっていない。
  - 同社の代表は、ログ上「人間なら時間のかかる手順の間隔が数秒しかなかった」として、攻撃者が AI を使ったとみている。ただ、それ以外の根拠は示していない。
  - 攻撃者が最初に欠陥を試したのは、10 月の PHP2Shell (PHP の RCE) への対応で各社が追われていた時期だという。
- **なぜ重要か (評価)**: 「顧客の AI のために MCP サーバーを用意する」ことが、そのまま管理系への新しい入口になった。MCP サーバーの診断では、ツールが呼び出す管理 API の認可が「MCP のセッションの利用者」に正しく絞られているかを、従来の API 診断と同じ厳しさで見る必要がある。
- 出典: [The Record (2026-11-09)](https://therecord.media/cyberattack-germany-ai-mittwald)

### [2026-11-09 報道] 台湾・花蓮の単独の攻撃者が、AI エージェントで 11 か国以上の数百の組織を攻撃。台北市の 119 番の出動記録を取得 (Acronis)
- **何が起きたか**:
  - Acronis の Threat Research Unit は、攻撃者自身のサーバー (一見すると設定ミスの開発機) から、エージェントの会話ログ、コマンド履歴、ツール、認証情報、被害データなど 9 万を超えるファイルを入手して分析した。
  - 攻撃は、救急、銀行、大学、軍のシステムなどに向けられた。台湾、メキシコ、タイの約 10 組織でデータを取得するかアクセスに成功した。台北市の 119 番 (消防・救急) のシステムの API から、7 つの区の出動記録 (時刻、種別、状態、番地レベルの位置) を取得した。消防の別のプラットフォームが、2018 年からの患者のデータ (心電図、救急車の映像) を、ログインなしで公開していたことも見つけた。
  - 商用の AI モデルはほとんど協力を拒んだため、攻撃のエージェントは、安全学習を外した「abliterated」モデルをローカルで動かしていた。エージェント同士は連携せず、攻撃者が出力を手で貼り付けて受け渡していた。
- **なぜ重要か (評価)**: 単独犯でも、ローカルの無検閲モデルで、国をまたいだ「量の攻撃」ができる段階にある。商用モデルの拒否は、攻撃を止める決め手にはならない。公開 API の認証の欠落 (今回の 119 番システム) のような基本的な穴が、AI による網羅的な探索で真っ先に拾われる。
- 出典: [The Hacker News (2026-11-09)](https://thehackernews.com/2026/11/taiwan-based-hacker-used-bossai-ai.html)

### [2026-11-08 報告] Operation Snowball: 公開ディレクトリから、欧州の通信事業者とそのデータセンターの 13 組織を 2 週間以上攻撃した、自律型の AI 侵入基盤が見つかる (Malbear Labs)
- **何が起きたか**:
  - 認証なしでダウンロードできた作業領域には、約 70 のセッションの記録、偵察の結果、ツール、認証情報、持ち出したデータベースのダンプがあった。運用者の指示とエージェントの報告は中国語だった (研究者は、国籍や国家の関与の根拠にはならないとしている)。
  - 基盤は DeepSeek Flash (100 万トークンの文脈) で動いていた。公開の jailbreak テンプレートを拡張した 7 万 8,000 文字のシステムプロンプトで安全策を外し、2 週間で拒否は 1 度も記録されていない。運用者の指示は「続けて」程度で、CVE、ツール、手法はエージェントが選んでいた。
  - 防御への反応: Trend Micro Deep Security が PwnKit (CVE-2021-4034) を止めると、エージェントは `sudo vi` のシェル脱出に切り替え、systemd の永続化ユニットを追加した。
- **なぜ重要か (評価)**: 「人間の勤務時間」から攻撃者を割り出すような分析は、効きにくくなる。一方で、エージェントのスキャンや横展開そのものは、端末やネットワークのテレメトリーに残る。EDR がブロックした後の「代わりの手」の連鎖を検知のシナリオに入れておきたい。
- 出典: [GBHackers (2026-11-09)](https://gbhackers.com/operation-snowball-campaign/)

### [2026-11-09] Google DeepMind の AI エージェントが、RSA-1024 への攻撃を安くする 2 つの手法を発見。署名の偽造の CPU 時間を 3.5 分の 1 に
- **何が起きたか**:
  - DeepMind は、UC San Diego と Inria の暗号研究者とともに、人間の監督下で AI エージェントを使って研究した。
  - 1 つ目の発見: 攻撃者が署名される値を選べる場合、PKCS#1 v1.5 の署名のパディングは、ブロックの約半分以上を攻撃者が制御できると、守りとして何の役にも立たない。HSM の PKCS#11 の署名インターフェースが該当する。
  - エージェントは過去の学術的な偽造攻撃を同じ 1024 ビットの鍵で再実行し、CPU 時間を 1,380 コア年から 391 コア年に減らした。2 つのエージェントが、4 日未満、人間からの約 20 回のメッセージ (ほぼ承認) で、計算の設計、実行、デバッグをした。鍵の素因数分解ではない。
  - DeepMind は「影響は古い RSA-1024 の系統だけで、2048 ビット以上は安全」としている。
- **なぜ重要か (評価)**: 暗号の攻撃研究の「試行錯誤」を AI が回せるようになった。診断の実務では、HSM や署名サービスに RSA-1024 と PKCS#1 v1.5 の組み合わせが残っていないかを、指摘事項の重要度を上げて扱う根拠になる。
- 出典: [SecurityWeek (2026-11-09)](https://www.securityweek.com/google-deepminds-ai-agents-make-1024-bit-rsa-keys-cheaper-to-attack/)

### [2026-11-09] GhostAction の新しい波: 偽の「security audit」ワークフローを数万のリポジトリに直接 commit し、git の全履歴から AI とクラウドの鍵を探す (Socket)
- **何が起きたか**:
  - Socket によると、10/7 以降、500 を超える GitHub アカウントが悪性のワークフローを commit した。uber/athenadriver や kitao/pyxel (1 万 8,420 スター) も含まれる。commit メッセージは「Add security audit workflow」などで、盗んだデータは 193.32.204[.]199 に送られる。
  - 運用者は、メンテナーの認証情報を手に入れると (入手方法は未観測)、各リポジトリの Actions のシークレット名を調べてペイロードに書き込み、既定のブランチに直接 commit する。
  - 新しい亜種は `fetch-depth: 0` で全ブランチとタグを取り、`git log -p --all` で全履歴の差分を読む。13 の正規表現で、AWS、Anthropic、OpenAI、OpenRouter、GitHub、GitLab、Google、Slack、SendGrid の鍵を探す。
  - GhostAction は 2025 年 9 月に GitGuardian が最初に報告した (当時は 817 リポジトリ、3,325 件の秘密情報)。
- **なぜ重要か (評価)**: 「削除した」つもりの過去の秘密情報が、履歴から盗まれる。とくに AI の API キーは、LLMJacking (他人の鍵で AI を使い倒す攻撃) にすぐ換金される。履歴に一度でも入った鍵は、削除ではなく失効させるのが原則だ。
- 出典: [GBHackers (2026-11-09)](https://gbhackers.com/ghostaction-supply-chain/)

### [2026-11-09] Elastic の報告: インフォスティーラーの感染から、盗んだ認証情報でのログインまで平均 8 分。Claude Code や ChatGPT のデスクトップアプリを使った侵入も記録
- **何が起きたか**:
  - Elastic Security Threat Command は、確認された 27 件のインフォスティーラーの事案で、感染からログインまでが平均 8 分だったと報告した。
  - Windows の事案では、攻撃者が遠隔で端末に入り、VS Code の拡張機能の Claude Code を使ってツールを準備し、外部のサーバーに接続していた。macOS では ChatGPT のデスクトップアプリが使われた事案もあった。
  - Elastic は「認証情報を持ちインターネットに出られるエージェントは新しい攻撃面で、攻撃者が使うと、インストールした社員と同じ動きに見える」としている。
- **なぜ重要か (評価)**: 社内で許可したコーディングエージェントが、そのまま攻撃者の「正規の道具 (LOLBin)」になる。検知は「承認されたツールか」ではなく「そのツールが何をしたか」で見る必要がある。
- 出典: [Help Net Security (2026-11-09)](https://www.helpnetsecurity.com/2026/11/09/elastic-businesses-remote-access-attacks-report/)

### [2026-11-09] 「Abe Office」を装う RAT: Chrome の中に入り込んで、App-Bound Encryption で守られた Cookie を Chrome 自身に復号させる。解析は Claude Code が REMnux 上で担当
- **何が起きたか**:
  - AbeAgent.exe は、SSL.com のコード署名証明書 (2026-11-04 署名) を持つ。Mark of the Web を消し、Run キーとタスクで永続化する。暗号化された 3 つのアドオン (RAT 機能、隠しデスクトップと注入、ブラウザの鍵の復号) を持つ。
  - Chrome 127 で導入された App-Bound Encryption を、暗号を破るのではなく、信頼された Chrome のプロセスに注入して復号を依頼する形で回避する。
  - 解析は、Claude Code が REMnux の仮想マシンで行ったものだという。研究者は、埋め込まれた既定のパスワード「AbeOffice-ChangeMe」で、ローダーの鍵と通信を復号できた。
- **なぜ重要か (評価)**: Cookie の保護を「正しいプロセスから呼ぶ」ことで回避する手口は、VOLTA (11/3 号で既報) と同じ系統で、定番になりつつある。防御側でも、マルウェアの解析を AI エージェントに任せる実例が出てきた。
- 出典: [GBHackers (2026-11-09)](https://gbhackers.com/abe-office-malware/)

## セキュリティニュース

### [2026-11-09] [続報] sshole (CVE-2026-123158): CISA が KEV に追加 (期限 11/12)。GreyNoise は、中国語のコメント入りで AI 生成とみられるバックドアを使う集団「GT10」を確認
- **前回から何が変わったか**:
  - CISA が 11/9 に KEV に加えた。連邦機関の対応期限は 11/12 だ。
  - GreyNoise は、東南アジアのハニーポットが「GT10」と名付けた集団に「成熟した侵入」をされたと公表した。GT10 のサーバーにアクセスして、他の被害者の候補とツールを確認した。使われたバックドアは、中国語のコメントを含み、AI で生成されたとみられる。Python3 がない機器には、Python3 を入れてから使っている。
  - watchTowr によると、今のところ悪用しているのはボットネットと暗号資産の採掘だけだ。Previdian は、20 回の試行、13 の IP、9 か国を観測した。
  - JPCERT/CC は 11/9 に CyberNewsFlash を出し、国内でも Alpine Linux ベースの商用製品が使われていることを確認したとした (国内の組織での侵害は未確認)。
- **悪用 / PoC**: 悪用あり (KEV)、PoC 公開済み。
- 出典: [Ars Technica (2026-11-09)](https://arstechnica.com/security/2026/11/vulnerability-that-lets-hackers-ssh-into-linux-devices-is-under-active-exploitation/) / [SecurityWeek](https://www.securityweek.com/hackers-exploiting-sshole-authentication-bypass-in-openssh/) / [BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-exploit-sshole-openssh-flaw-to-breach-linux-systems/) / [JPCERT/CC (2026-11-09)](https://www.jpcert.or.jp/newsflash/2026110901.html)

### [2026-11-09] CISA、FreeSWITCH の SIP MESSAGE によるコマンド実行 (CVE-2026-116779) と IBM Aspera Faspex の権限昇格 (CVE-2026-123218) を KEV に追加
- **何が起きたか**:
  - CISA は 11/9 に、sshole とあわせて、FreeSWITCH (CVSS 9.8) と IBM Aspera Faspex 5.0.0〜5.0.19 (CVSS 9.8) の欠陥を KEV に加えた。期限はどちらも 11/12 だ。
  - FreeSWITCH の欠陥は、受け付けた SIP MESSAGE の宛先のユーザー名を「+」で区切り、左側をチャットのプロトコル名として扱う処理にある。`api` を選ぶと `switch_api_execute()` に届き、OS コマンドを含む FreeSWITCH の API コマンドをデーモンの権限で実行できる (詳細は CVE 表)。
  - Aspera Faspex の欠陥は、ログインできる利用者が細工したメッセージで認可を回避し、管理者の全権限を得られるというもの。
- **悪用 / PoC**: 悪用あり (KEV)。EPSS は FreeSWITCH が 0.013、Aspera Faspex が 0.004 (11/10 時点)。具体的な攻撃者や攻撃の規模は公表されていない。
- **なぜ重要か (評価)**: FreeSWITCH は、IP 電話の交換機やコールセンターの基盤として国内でも使われている。SIP は既定で外に向いていることが多く、認証の手前の処理で OS コマンドに届く。Aspera Faspex は大容量ファイルの転送に使われ、過去にも悪用の標的になった (2023 年の CVE-2022-47986、背景引用)。
- 出典: [CISA KEV (JSON で確認)](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) / [NVD CVE-2026-116779](https://nvd.nist.gov/vuln/detail/CVE-2026-116779) / [IBM (Aspera Faspex)](https://www.ibm.com/support/pages/node/7295921)

### [2026-11-09] フランス、10 月の冷蔵設備への攻撃をイラン革命防衛隊系の「Shahid Kaveh」によるものと断定。約 700 の店舗が標的で、少なくとも 15 件の火災
- **何が起きたか**:
  - 仏外務省は 11/9 の声明で、10/11〜12 の夜の攻撃を、IRGC の電子・サイバーセンター傘下の Shahid Kaveh によるものとした。攻撃者は業務用の冷蔵の制御器に侵入し、霜取りの温度の設定を高温に変えた。
  - 仏当局によると、標的は約 700 の小売の拠点 (Casino、Leclerc、Carrefour など) で、食品の廃棄で数千万ユーロの損失と、少なくとも 15 件の火災が起きた。同じ時期に、小水力発電所の Schneider Electric の機器への攻撃もあった。
  - これとは別に、SecurityScorecard は、インターネットに公開された Copeland XWEB PRO (旧 Dixell) の制御器が、スパムのボットネットやプロキシの中継に使われていると報告した。
- **悪用 / PoC**: 悪用あり (実被害)。個別の CVE は特定されていない。
- **なぜ重要か (評価)**: 国家の攻撃者が、OT の設定値を変えるだけで物理的な被害 (火災) を起こした。「冷蔵の制御器」は、IT の資産台帳に載っていないことが多い。外部の攻撃面の調査 (ASM) で、XWEB などの管理画面が公開されていないかを確かめたい。
- 出典: [BleepingComputer (2026-11-09)](https://www.bleepingcomputer.com/news/security/france-blames-iranian-hackers-for-supermarket-attacks-that-sparked-fires/) / [Help Net Security (Copeland XWEB)](https://www.helpnetsecurity.com/2026/11/09/copeland-xweb-refrigeration-controllers-spam-botnet/)

### [2026-11-09] Ethersphere の bee-js 13.3.0 と Swarm Desktop 0.56.2 が、プロジェクト自身のリリースの自動化経由で汚染。ウォレットの鍵を盗むコードを配布
- **何が起きたか**:
  - 攻撃者は、Ethersphere のリリースの自動化を使って、分散ストレージ Swarm の 2 つのツールの悪性版を公開した。どちらも、Swarm Desktop がノード用に保存するウォレットの鍵と、その解錠のパスワードを盗むコードを取ってきて動かす。Windows、macOS、Linux にバックドアも入れる。
  - bee-js 13.3.0 は、11/9 の 00:09〜01:25 UTC の約 75 分間、npm の最新版だった。postinstall で動くので、import しなくてもインストールだけで実行される。Swarm Desktop 0.56.2 は約 8.5 時間公開され、組み込みの更新機能が Windows x64 と Apple Silicon の Mac に配布しえた (Socket の分析)。
  - 悪性版は削除されたが、すでに入ったバックドアや送られた鍵は戻らない。
- **悪用 / PoC**: 実配布あり。資金の盗難の報告は、記事の時点ではない。
- **なぜ重要か (評価)**: 個人のアカウントの乗っ取りではなく、「正規のリリースのパイプライン」が使われた。プロジェクト自身の他のパッケージがバージョン範囲で 13.3.0 を受け入れていたため、被害が広がりうる。ロックファイルの固定と、`npm ci --ignore-scripts` の運用が改めて効く。
- 出典: [The Hacker News (2026-11-09)](https://thehackernews.com/2026/11/hackers-compromise-etherspheres-bee-js.html)

### [2026-11-09] PolinRider、乗っ取った npm の 10 パッケージ (12 リリース) で再登場。Ethereum の取引から次の C2 のアドレスを読む
- **何が起きたか**:
  - Sonatype によると、ローダーは公開の Ethereum の RPC (予備で Blockscout) から特定のウォレットの取引を読み、宛先のアドレスの先頭 4 バイトと次の 4 バイトを、主と予備の IPv4 アドレスとして解釈する。
  - install / postinstall のフックはなく、エントリーポイントの読み込み時に動く。そのため、インストールスクリプトを無効にしても防げない。
  - 6 リリースは `eval(atob(...))`、残り 6 リリースは文字の並べ替えと `Function` の間接呼び出しで隠していた。
- **悪用 / PoC**: 実配布あり。
- **なぜ重要か (評価)**: ブロックチェーンを「書き換えられない連絡掲示板」にする手口は、C2 のテイクダウンを難しくする。上の bee-js とは逆に、`--ignore-scripts` では止まらないので、依存の差分のレビュー (新しいバージョンに難読化コードが増えていないか) が必要になる。
- 出典: [GBHackers (2026-11-09)](https://gbhackers.com/polinrider-malware-attack/)

### [2026-11-09] Web3Auth のインフラの欠陥が悪用され、Google / Apple ログインで作った Keplr ウォレットから暗号資産が盗まれる。Web3Auth は攻撃者と同じ経路で残りを「救出」
- **何が起きたか**: Keplr の Google / Apple のサインインは、Web3Auth が提供している。攻撃者は Web3Auth のインフラの欠陥を使ってウォレットに届いた。Web3Auth は、被害の恐れのある他のウォレットから、攻撃者と同じ経路で資金を回収用のウォレットに移した。リカバリーフレーズやハードウェアウォレットで作ったものは影響を受けない。Keplr は Google / Apple のサインインを止めている。
- **悪用 / PoC**: 悪用あり。欠陥の技術的な詳細は未公表。
- **なぜ重要か (評価)**: ソーシャルログインで鍵を管理する「MPC / 鍵分散」型のウォレットでは、提供事業者のインフラ自体が単一障害点になる。防御側が攻撃と同じ経路で資金を動かせたという事実は、事業者がいつでも鍵を使える設計だったことを示している。
- 出典: [The Hacker News (2026-11-09)](https://thehackernews.com/2026/11/web3auth-flaw-exploited-to-steal-keplr.html)

### [2026-11-08〜09] LNbits、Bitcoin の Lightning のウォレットサーバーを全運用者に停止するよう要請。修正版は未公開のまま
- **何が起きたか**: 11/8 に、有料閲覧のアドオン「Paywall」の無効化を求めた約 80 分後に、全面停止を呼びかけた。ある運用者は、新しく作られたアカウントが脆弱性を使って 2,285,545 サトシ (約 0.023 BTC) を引き出したと報告した。攻撃は、最初の警告の 3 時間以上前 (09:22 UTC) に始まっていた。開発者は、修正を 24〜48 時間以内に出すとしていた。
- **悪用 / PoC**: 悪用あり。欠陥の詳細は未公表。
- **なぜ重要か (評価)**: 拡張機能 (アドオン) の欠陥が、本体の資金を動かす権限に届いた。OSS の決済系の診断では、拡張機能が使える内部 API の範囲を必ず確認したい。
- 出典: [The Hacker News (2026-11-09)](https://thehackernews.com/2026/11/lnbits-urges-all-operators-to-shut-down.html)

### [2026-11-09 報道] Sam Curry 氏と Shubham Shah 氏、2 つの自動車ブランドのアプリの認証基盤 (ForgeRock) の管理画面に既定の admin:admin で入り、他人の車の解錠とエンジンの始動まで実証
- **何が起きたか**:
  - 両ブランドのアプリは、ForgeRock (現 Ping Identity) でログインしていた。顧客の記録を持つ OpenIDM には、Apache Felix の管理コンソールが付属する。ForgeRock の堅牢化ガイドは本番前に削除か保護を求めているが、残っていて、既定の admin / admin のままだった。
  - コンソールはインターネットから遮断されていたが、前段 (エッジ) と後段の Java が URL を違うように解釈した。エンコードしたスラッシュなどを加えると、エッジは「無害な静的ファイル」と見なし、後段は管理コンソールへのパスとして扱った。
  - 研究者は 2026 年 2 月に、自分と同意した所有者の車でだけ試した。報告から約 2 時間で修正された。
- **悪用 / PoC**: 研究者による実証のみ (修正済み)。
- **なぜ重要か (評価)**: 「パスの解釈の差で前段の ACL を抜ける」+「既定の資格情報」という、診断で毎回見るべき 2 点の組み合わせだ。ForgeRock / OpenIDM の診断では、`/system/console` 系のパスに、正規化の差を使った到達性を必ず試したい。
- 出典: [The Hacker News (2026-11-09)](https://thehackernews.com/2026/11/default-adminadmin-server-password.html)

### [2026-11-09] 米 Vanderbilt 大学がサイバー攻撃を公表。全員に端末の電源を切り、学内の Wi-Fi から外れるよう指示。新興のランサムウェア集団 BYOD がリークサイトに掲載
- **何が起きたか**: 約 1 万 4,000 人の学生と 6,000 人超の職員を抱える同大学は、11/9 の朝に攻撃を公表した。BYOD は同日早朝、大学をリークサイトに載せ、データを盗んだと主張した。BYOD は 9/29 に最初の被害者が確認された新しい集団で、ミシガン州立大学やニューメキシコ大学 (医療機関が救急車の受け入れを止めた) への攻撃にも関わったとされる。
- **悪用 / PoC**: 侵入経路は未公表。
- **なぜ重要か (評価)**: 「全端末の電源を切れ」という指示は、端末側で暗号化が進んでいるか、横展開が止まっていない状況を示唆する (推定)。大学は医療機関を併設することが多く、被害が人命に及びうる。
- 出典: [The Record (2026-11-09)](https://therecord.media/vanderbilt-cyberattack-ransomware-alert)

### [2026-11-09] Anubis ランサムウェアの攻撃で、新しい専用のバックドア「Lindnor」が MS SQL Server に。BYOVD でセキュリティ製品を止める (Symantec)
- **何が起きたか**: 10 月の米国の組織への攻撃で、2 台の SQL Server に Lindnor が入っていた。Chrome の部品や VMware のファイルを装い、サービスとして動いた。運用者は約 1 時間で、セキュリティ製品を止める 13 以上の実行ファイルと、既知の脆弱な署名付きドライバー 5 つを置いた。暗号化はブロックされた。Lindnor は、無関係な 2 つの組織のネットワークでも見つかった。
- **悪用 / PoC**: 実攻撃。初期侵入の経路は不明。
- **なぜ重要か (評価)**: ランサムウェアの攻撃で専用のバックドアを使うのは珍しい。SQL Server はインターネットに公開されたままのことも多く、`xp_cmdshell` や弱い `sa` のパスワードが入口になる典型だ (一般論)。
- 出典: [GBHackers (2026-11-09)](https://gbhackers.com/anubis-ransomware-attack/)

### [2026-11-09] Bitter (APT-C-08 / TA397)、南アジアの組織を新しい RAT「PapRAT」(C++ 版と Rust 版) で狙う (Fortinet)
- **何が起きたか**: 感染の経路は 3 つ。`ftp.exe` を悪用して スクリプトを動かす LNK、Excel のおとりと裏の MSI を含む VHDX、WebDAV で LNK を取ってくる URL ファイル。偵察の結果を「abc.pdf」にまとめて curl で送り、送った後に消す。
- **悪用 / PoC**: 実攻撃。
- **なぜ重要か (評価)**: `ftp.exe` のスクリプト機能や VHDX など、Mark of the Web を避ける古典的な LOLBin がまだ現役だ。検知ルールの見直しの材料になる。
- 出典: [The Hacker News (2026-11-09)](https://thehackernews.com/2026/11/bitter-hackers-deploy-new-paprat.html)

### [2026-11-09] SANS ISC: SAP NetWeaver の古い欠陥 (CVE-2025-31324) と、置かれたままの Web シェルを探すスキャンを観測
- **何が起きたか**: ある攻撃元 (82.26.72.21) は、SAP NetWeaver の `/developmentserver/metadatauploader` に加えて、SharePoint の `ToolPane.aspx`、Joomla の各種アップロード (com_baforms、com_gridbox、com_jce、com_sppagebuilder) のパスもまとめて叩いていた。
- **悪用 / PoC**: スキャンの観測 (CVE-2025-31324 は KEV 入り済み、背景)。
- **なぜ重要か (評価)**: 「過去に誰かが置いた Web シェル」を探す二次的なスキャンが続いている。以前に該当した SAP の環境は、パッチだけでなく `/irj/servlet_jsp/irj/root/` 配下の不審な JSP の有無も確かめたい。
- 出典: [SANS ISC (2026-11-09)](https://isc.sans.edu/diary/33502)

### [2026-11-09] 米財務省 FinCEN、暗号資産取引所 MEXC を米国の金融システムから締め出し。少なくとも 160 億ドルの不正な取引に関与と認定
- **何が起きたか**: FinCEN は、2021 年 5 月〜2026 年 5 月に、サイバー犯罪やイラン、北朝鮮、ロシアの制裁逃れに関わる少なくとも 160 億ドルの取引を MEXC が許したとした。制裁対象の Garantex / Grinex との取引や、ロシアの A7 ネットワークに関わる 2 億 2,600 万ドル以上の取引も挙げた。
- **悪用 / PoC**: 該当なし (法執行)。
- **なぜ重要か (評価)**: ランサムウェアの身代金の換金ルートを断つ措置だ。同日、ウクライナでも暗号資産の詐欺の拠点の摘発 (430 万ユーロ) が報じられた。
- 出典: [BleepingComputer (2026-11-09)](https://www.bleepingcomputer.com/news/security/us-bans-mexc-crypto-exchange-over-sanctions-evasion-cybercrime-links/) / [BleepingComputer (ウクライナ)](https://www.bleepingcomputer.com/news/security/ukraine-dismantles-crypto-scam-network-that-stole-43-million/)

### [2026-11-09] 漏えいの件数の更新が続く: Revolve 151 万 5,073 人 (カード番号と有効期限を含む)、Amplifon Americas 133 万人 (医療情報を含む)。Binance は「3 億 3,500 万人分」の販売を否定
- **何が起きたか**:
  - [続報] Revolve: 10/29 に公表した侵害について、インディアナ州司法長官に 1,515,073 人と報告した。侵入は 9/11 で、「自動化された手段」で、氏名、住所、カード番号と有効期限が集められた可能性がある (カードを保存していた顧客のみ)。
  - Amplifon Americas: 1/18〜2/8 にファイルが持ち出され、8 か月の調査の末、1,332,826 人の氏名、運転免許証番号、医療情報、保険情報などの流出を通知した。
  - Binance: 「ShinyHunters」を名乗る人物が 3 億 3,500 万人分の KYC 書類や秘密鍵を 90 万ドルで売りに出したが、Binance は侵害の証拠はないとし、過去の同様の出品はインフォスティーラーのデータだったと説明した。
- **なぜ重要か (評価)**: EC サイトに「カードを保存」できる機能は、自動化された収集の標的になる。Binance の件のように、有名な集団の名前を騙った「販売の主張」も増えている。真偽の判断には、サンプルの構造が事業者の保存形式と一致するかの確認が要る。
- 出典: [SecurityWeek (Revolve)](https://www.securityweek.com/revolve-puts-data-breach-victim-count-at-1-5-million/) / [SecurityWeek (Amplifon)](https://www.securityweek.com/amplifon-americas-data-breach-impacts-1-3-million/) / [BleepingComputer (Binance)](https://www.bleepingcomputer.com/news/security/binance-denies-data-breach-after-alleged-shinyhunters-claims/)

### [2026-11-09] [続報] ロシアのクラウド事業者 Beget: ワイパーの攻撃から 1 週間で、共有ホスティングの 60%、専用サーバーの 40% を復旧。VPS のファイルのバックアップは約半数の利用者分しか残らず
- **前回から何が変わったか**: 11/1 の夜、攻撃者がアーキテクチャ全体の管理層に入り、データをゼロで埋めるスクリプトを動かした。VPS、S3、Kubernetes の全データ、CDN と IP の設定が失われた。VPS のバイナリのバックアップは全滅し、ファイルのバックアップは約半数の利用者分しか使えない。Beget は「すべてのデータの復旧は不可能」としている。
- **なぜ重要か (評価)**: 管理層を握られると、バックアップも同じ権限で消される。国内の使えるねっとの件 (11/9 号) と同じく、ホスティング事業者の診断では「管理層からバックアップを消せるか」を必ず確かめたい。
- 出典: [BleepingComputer (2026-11-09)](https://www.bleepingcomputer.com/news/security/russian-cloud-firm-beget-rebuilds-from-scratch-after-data-wiper-attack/)

### [2026-11-09] PyPI、プロジェクトのページに「Security」タブを追加。リリースのファイルごとに、署名付きの来歴 (attestation) を表示
- **何が起きたか**: Trusted Publisher を示す「PyPI Publish」と、ソースの commit とビルド環境に結び付く「SLSA Build Provenance」の 2 種の attestation を表示する。リリース内で一部のファイルにしか attestation がない場合、ファイルごとにリポジトリが違う場合、前のバージョンとワークフローが変わった場合、attestation が途絶えた場合に警告を出す。
- **なぜ重要か (評価)**: 「ワークフローが変わった」という警告は、上の bee-js のようなパイプラインの乗っ取りの兆候を拾える。依存の監査に組み込む価値がある。
- 出典: [Help Net Security (2026-11-09)](https://www.helpnetsecurity.com/2026/11/09/pypi-security-tab-release-attestations/)

### [2026-11-08〜09] 親ロシアの NoName057(16)、イタリアのタヤーニ外相ら欧州の要人 18 人の個人情報をダークウェブで公開し、追加の情報に報奨金
- **何が起きたか**: タヤーニ外相は 11/8 に X で、自身と家族が標的にされていると述べた。サイトには、電話番号、メール、SNS、一部は自宅の住所が載っている。メローニ首相も親ロシアのハッカーを非難した。
- **なぜ重要か (評価)**: DDoS が中心だった NoName057(16) が、要人の晒し (doxing) と懸賞金という、物理的な脅迫に近い手口に広げた。
- 出典: [The Record (2026-11-09)](https://therecord.media/hackers-russia-italy-noname)

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-11-08 以降 (KEV 追加は追加日で判定) / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-116779 / GHSA-mg63-h38w-8p9p | FreeSWITCH < 1.11.3 | CWE-77/78 / 9.8 | 受け付けた SIP MESSAGE の宛先のユーザー名を `+` で区切り、左側をチャットのプロトコル名として扱う → `api` を選ぶと `switch_api_execute()` に届く → OS コマンドを含む API をデーモンの権限で実行 | [commit 7015f6a](https://github.com/signalwire/freeswitch/commit/7015f6a73ab3d67fed5fbfc277ecfb88a74c2a86) | **KEV (11/9)** / EPSS 0.013 |
| CVE-2026-123218 | IBM Aspera Faspex 5.0.0〜5.0.19 | CWE-863 / 9.8 | 認証済みの利用者が細工したメッセージを送る → 認可のチェックを回避 → 管理者の全権限 | [IBM advisory](https://www.ibm.com/support/pages/node/7295921) (commit 不明) | **KEV (11/9)** / EPSS 0.004 |
| CVE-2026-123158 [続報] | OpenSSH < 10.6p2 (musl かつ PAM なし) | — / 8.1 | パスワードのない (`*`) アカウントに 257〜1024 バイトのパスワードを送る → musl の `crypt()` がエラー時に `*` を返す → 保存値 `*` と一致して認証成功 | [OpenSSH 10.6p2](https://www.openssh.org/releasenotes.html#10.6p2) | **KEV (11/9)** / EPSS 0.010 / PoC 公開・悪用 |
| CVE-2026-63469 / 63470 / 63471 (GHSA-6xmv-cjr5-w3q8 ほか) | fastapi-code-generator (PyPI) | CWE-94/116 / Critical | OpenAPI 定義のステータスコードのキー、route のパス、operation の summary を、エスケープせずに生成する Python コードに埋め込む → デコレーターや docstring を抜けてコードを注入 → 生成物の import 時・呼び出し時に RCE | [commit 49301db](https://github.com/koxudaxi/fastapi-code-generator/commit/49301dbdb82170d7f50877419d994b05cb1fa2bc) | 信頼できない仕様書からのコード生成 |
| CVE-2026-63395 / GHSA-9qw7-j9xw-fv9c | isomorphic-git (npm) | CWE-22/59 / High | 悪性のリポジトリをチェックアウトする → ディレクトリのシンボリックリンクを辿って書き込む → 作業ツリーの外に任意のファイルを書き込み | [PR #2370](https://github.com/isomorphic-git/isomorphic-git/pull/2370) | EPSS 0.007 |
| CVE-2026-63436 / GHSA-52c6-99qm-3hqr | zt-zip (Maven) | CWE-22 / High | fluent API の unpack で、エントリー名の `../` を検査しない → 展開先の外にファイルを書き込み (Zip Slip) | [PR #180](https://github.com/zeroturnaround/zt-zip/pull/180) | Java の定番ライブラリ |
| CVE-2026-111421 | Apache Airflow 3.0.0〜3.4.0 未満 | — / moderate | Task Execution API の `set_xcom` が予約キーの検査を省く → Dag の作者が細工した XCom を API で逆シリアル化 → API サーバーで `airflow.*` のクラスを任意の引数で生成 (CVE-2026-59242 の修正漏れ) | [PR #74829](https://github.com/apache/airflow/pull/74829) | 修正漏れ (2 度目) |
| CVE-2026-101031 | Apache Airflow 3.0.5〜3.4.0 未満 (example Dag) | — / low | HTTP で取得した IP を Python の `ipaddress` で検証してからシェルに渡す → `ipaddress` は IPv6 のゾーン ID (`%` 以降) に任意の文字を許す → ワーカーでコマンド注入 (CVE-2025-54941 の修正漏れ) | [PR #73787](https://github.com/apache/airflow/pull/73787) | **水平伝播しやすい検証の抜け** |
| CVE-2026-111453 | Apache Airflow 3.3.2〜3.4.0 未満 | — / low | 権限は `?dag_id=` の Dag で確認し、削除は読める全 Dag の queued events に対して実行 → 編集権限のない Dag のトリガーを抑止 (CVE-2026-75157 の修正漏れ) | [PR #74839](https://github.com/apache/airflow/pull/74839) | 検査と実行の対象のずれ |
| CVE-2026-124249 | CPython (http.cookiejar) | — / medium | 期限切れの Set-Cookie を受けると、Domain / Path 属性でクッキーポリシーを見ずに削除 → 共有の CookieJar で他のドメインのクッキーを消せる | [PR #161570](https://github.com/python/cpython/pull/161570) | RFC 6265 5.3 の実装の抜け |
| CVE-2026-19552 | CPython (`ssl.get_server_certificate`) | — / low | `ca_certs` を渡すと証明書チェーンは検証するが、ホスト名 (識別) は検証しない → 正規の CA の別ドメインの証明書を受け入れ | [PR #161507](https://github.com/python/cpython/pull/161507) | 検証の部分的な欠落 |
| CVE-2026-63417 / GHSA-w7qv-268h-9h3f | loggingredactor (PyPI) | CWE-532 / High | 基本型以外のオブジェクトの `str` / `repr` をマスクの対象にしない → ログに PII がそのまま出力 | [PR #15](https://github.com/armurox/loggingredactor/pull/15) | — |
| CVE-2026-124307 | VVdeC (VVC デコーダー) < 3.2.1 | CWE-416 / 5.8 | 細工した VVC のビットストリームで、ALF の APS の ID を再定義 → デコード中のワーカーが古い APS を参照 → 解放後の使用 (UAF) | [commit 1eddb30](https://github.com/fraunhoferhhi/vvdec/commit/1eddb30c4b8e02f3d13ba24aa7e52f1aa7b08c01) | ASan で再現 |

### 今日の CVE 所感

- **「検証した値」と「使う値」のずれ** が並んだ。Airflow の 3 件は、どれも過去の CVE の修正漏れだ。とくに CVE-2026-101031 は、「`ipaddress` で検証したから安全」という前提が、IPv6 のゾーン ID (`fe80::1%<任意の文字列>`) で崩れる。Python に限らず、「IP アドレスとして妥当なら、シェルや URL に入れてよい」と扱うコードは多い。Go の `netip.ParseAddr`、Rust の `std::net`、Java の `InetAddress` で、ゾーン ID の扱いがどうなっているかを調べると、横に広がる可能性がある。
- **コード生成器の注入** (fastapi-code-generator) は、OpenAPI から何かを生成するツール全般 (openapi-generator のテンプレート、各言語の SDK 生成器) に同じ構造がある。生成物を CI で自動的に import するなら、仕様書の入手元が信頼できるかが攻撃面になる。
- **シンボリックリンク / Zip Slip** (isomorphic-git、zt-zip) は古典だが、まだ出る。JS で書かれた git 実装はブラウザや Electron でも使われるので、Electron アプリの「リポジトリを取り込む」機能の診断で試したい。
- **SIP の宛先の文字列を「プロトコル選択子」として解釈** する FreeSWITCH の欠陥は、Asterisk や Kamailio などの他の VoIP 実装でも、「宛先や From のユーザー名の区切り文字に特別な意味を持たせる処理」がないかを見る起点になる。
- 診断で優先して見る製品: FreeSWITCH (外部公開の SIP)、Aspera Faspex、Alpine ベースのアプライアンス (sshole)、Airflow (Dag の作者を信頼しすぎる設計)。

## 日本国内のセキュリティ動向

### 国内インシデント・事故

#### [2026-11-09] ニトリ HD: 管理システムへの不正アクセスで、個人会員、購入者、法人会員、EC モールでの注文の情報など、最大 3,762 万件が流出した可能性
- **何が起きたか**:
  - 不正アクセスが分かったのは 11/6 だ。過去のログを調べた結果、10 月中旬〜下旬にもアクセスされていた可能性がある。
  - 対象はニトリグループの個人会員と購入者のほか、法人会員 (会社名、部署名、代表者名、担当者の連絡先)、ニトリネットと EC モールの公式ショップの注文のデータに及ぶ。クレジットカード情報とログインパスワードは含まれないとしている。
  - 3,762 万件は調査段階の「最大の対象件数」で、確定した流出件数ではない。侵入経路と悪用された脆弱性の種類は公表されていない。同社は「脆弱な箇所への対応」と監視の強化を済ませたとしている。
- **なぜ重要か (評価)**:
  - 国内の今年の一連の漏えいの中でも、最大級の件数だ。法人会員の担当者情報と注文の履歴が組み合わさると、取引を装った請求書の詐欺 (BEC) が成り立ちやすい。
  - 「発覚の 2〜3 週間前から入られていた」という形は、9 月末からの国内の連続した侵害と同じパターンだ。ログの保存期間が短い組織では、遡った調査ができない。
- 出典: [セキュリティ対策 Lab (2026-11-09)](https://rocket-boys.co.jp/security-measures-lab/nitori-unauthorized-access-3762man-data-leak/) (ニトリ HD の公表文は未取得。内容は二次記事で確認)

#### [2026-11-09] シェアフル (スキマバイトアプリ): 社内管理システムに不正アクセス。個人最大約 750 万アカウント (給与振込の口座、在留資格の情報を含む) と、求人企業約 7,500 社の情報が流出した可能性
- **何が起きたか**:
  - 11/5 の 9:45 ごろに発覚し、同日 14 時ごろまでに外部からの経路を遮断した。
  - 個人の対象: 氏名、電話番号、メールアドレス、住所、生年月日、給与振込用の銀行口座情報、顔写真の URL、緊急連絡先、在留資格に関する情報など。
  - 対象外: 給与やポイント、契約・就業実績などの労務管理データ、本人確認書類の画像、マイナンバー、カード情報。顔写真は別のサーバーで管理しており、そのサーバーへのアクセスも遮断した。
  - 法人の対象: 会社名、所在地、担当者の氏名・部署・役職・連絡先、営業管理データの一部。
  - サービスは通常どおり提供しており、対象者には順次連絡する。
- **なぜ重要か (評価)**: 口座情報、生年月日、在留資格がそろうと、銀行や入管、給与担当を装った詐欺の精度が上がる。とくに外国籍の働き手は、在留資格を口実にした脅しに弱い。「社内管理システム」が入口なので、管理画面の認証と IP 制限の有無が焦点になる (推定)。
- 出典: [セキュリティ対策 Lab (2026-11-09)](https://rocket-boys.co.jp/security-measures-lab/sharefull-personal-corporate-data-unauthorized-access/) (シェアフルの公表文は未取得)

#### [2026-11-09] [続報] アララ「アララメッセージ」経由: セガがメールアドレス 219 万 6,044 件の流出を確定 (うち 9 万 2,273 件は配信に付随する情報も)
- **前回から何が変わったか**:
  - セガは、自社とセガ フェイブのメールマガジンの配信先 2,196,044 件の流出を確認した。『CHUNITHM』『オンゲキ』『maimai でらっくす』、セガ ラッキーくじなど、2026 年 7〜10 月に配信した 11 件のメールマガジンが対象だ。「SEGA Account」の登録メールアドレスは別のシステムで管理しており対象外。
  - セガが 10 月末にアララに照会した時点では「流出は確認されていない」との回答だったが、その後の調査で流出が確認された。アララと連名で個人情報保護委員会に報告する予定だ。
- **なぜ重要か (評価)**: 委託先の最初の回答が、後で覆った。委託元は、初報の「影響なし」をそのまま信じず、ログの提供や調査の範囲を具体的に確かめる必要がある。piyolog は 11/9、ラクスライトクラウド、ユミルリンク (Cuenote)、アララなど 5 つのメール配信事業者の侵入の経過を時系列で整理した。
- 出典: [セキュリティ対策 Lab (2026-11-09)](https://rocket-boys.co.jp/security-measures-lab/sega_sega_fave_arara_2196044_email_leak_20261109/) / [piyolog (2026-11-09)](https://piyolog.hatenadiary.jp/entry/2026/11/09/230435)

#### [2026-11-09] 警視庁、銀座で偽基地局 (IMSI キャッチャー) を運用した中国籍の男を電波法違反で逮捕。携帯電話の通信の妨害での摘発は全国初
- **何が起きたか**:
  - 男は 11/7 の 15:30 ごろ、銀座の路上で、免許なしに車に無線機を載せて電波を出した疑いで現行犯逮捕され、11/9 に発表された。容疑は否認している。ドコモの無線設備の機能を妨げた疑い (重要無線通信の妨害) でも送検された。関東総合通信局も同日、告発を公表した。
  - 手口: 車から正規の基地局と同じ周波数帯の強い電波を出して、半径 500 メートル以上の端末の 4G / 5G を圏外にし、2G に接続させる。2G では端末が基地局を認証しないため、偽基地局が SIM の識別番号を取り、「海外での不正利用の恐れでカードを止めた」などの中国語の SMS を送って、カード情報の入力サイトへ誘導していた。
  - 装置は後部座席の下に隠され、トランクにはバッテリーなどが積まれていた。新宿や渋谷でも同様の電波が確認されている。
- **なぜ重要か (評価)**: 国内では 2G のサービスは終わっているが、端末側が 2G に落ちる設定のままだと「ダウングレード攻撃」を受ける。Android では「2G を許可」をオフにできる (iOS はロックダウンモード)。社用スマホの MDM で 2G を無効にできるかを確かめておきたい。
- 出典: [piyolog (2026-11-10)](https://piyolog.hatenadiary.jp/entry/2026/11/10/004128)

> 範囲外 (11/7 以前の公表) のため本文に入れなかったもの: ネットマイル (最大約 549 万人、11/2 公表)、ソニー生命 (メディケア生命の契約者など約 38.5 万件、10/28)、花キューピット (423 万 8,242 件、10/28)、CN ポイント (10/29)、電力・ガス取引監視等委員会のサイト (10/28)、ポイントインカム / CoinTrade (11/6)、総務省消防庁の安否情報システム (11/5、11/6 号で既報)、JNSA (11/8 号で既報)、ロート製薬の調査結果 (11/7〜8 号で既報)。ScanNetSecurity と Security NEXT が 11/9 に掲載したが、公表日は上のとおり。

### 国内の注意喚起・ガイドライン・政策

#### [2026-11-09] JPCERT/CC、CyberNewsFlash「OpenSSH における認証回避の脆弱性 (CVE-2026-123158) について」を公開
- **何が起きたか**: 対象の条件 (musl libc、PAM なし、別のローカルアカウントに `$5$` か `$6$` 形式のハッシュがある) を整理した。国内でも Alpine Linux ベースの商用製品が使われていることを確認し、PoC が公開され、悪用の成功も報告されているとして、対策の適用と侵害の有無の調査を求めた。調査の方法として、本来パスワードでログインできないアカウントへの `Accepted password for` の記録を、SSH の認証ログで探すよう案内している。
- **なぜ重要か (評価)**: 「注意喚起」ではなく CyberNewsFlash での発信だが、国内のアプライアンスへの影響を明記した点が実務的だ。製品のベンダーへの問い合わせの根拠に使える。
- 出典: [JPCERT/CC (2026-11-09)](https://www.jpcert.or.jp/newsflash/2026110901.html)

#### [2026-11-09] 関東総合通信局、偽基地局の不法無線局を警視庁と共同で取り締まり、電波法違反で告発
- **何が起きたか**: 上の逮捕の件で、関東総合通信局は 11/7 に警視庁と共同で、車に開設された不法無線局を取り締まった。電波法 4 条 (無線局の開設) と 108 条の 2 (重要無線通信の妨害) の違反の疑いで告発したと 11/9 に公表した。
- **なぜ重要か (評価)**: 偽基地局は 2024 年 12 月ごろから都内の繁華街で報告されていた (背景)。通信の妨害の罪で立件した初の例で、同種の機材を使う他の詐欺グループへの抑止になる。
- 出典: [piyolog (関東総合通信局の公表を引用)](https://piyolog.hatenadiary.jp/entry/2026/11/10/004128)

#### [2026-11-09] ITmedia: 漏えいの続発で「その人専用の詐欺メール」への懸念。フィッシング対策協議会、チェック・ポイント、トビラシステムズに聞く
- **何が起きたか**: フィッシング対策協議会は、一連の漏えいとの直接の関係は確認できていないものの、報告件数は増加傾向だとした。トビラシステムズは「文面ごとに異なる個人情報や URL を載せたメール」を確認し始めたという。チェック・ポイントは、カスタマーサポートや社内の IT 部門を名乗るメール、とくにカレンダーの招待 (.ics) の添付に注意を呼びかけた。
- **なぜ重要か (評価)**: 漏えいした情報が組み合わされ、標的型の「個別化されたフィッシング」が一般消費者にも向き始めた。訓練メールのシナリオを、実在の購買履歴や会員情報を使う前提に更新する時期だ。
- 出典: [ITmedia NEWS (2026-11-09)](https://www.itmedia.co.jp/news/article/2611/09/2000002926/)

### 国内製品の脆弱性 (JVN)

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| 2026-11-09 | JVN#89009783 / CVE-2026-113362 ほか | WebSAM WinShare 7.5.0 以前 (7.3.3 を除く) / NEC | リモート操作の対象の PC で、危険な機能の公開とヒープオーバーフローにより、細工したパケットで SYSTEM 権限の任意コード実行。インストール先の権限設定の不備で、一般ユーザーが SYSTEM を取れる | v3 9.8 / v4 9.3 (最大) | [JVN](https://jvn.jp/jp/JVN89009783/) |
| 2026-11-09 | JVNVU#93403064 / CVE-2026-111793 | Webtop Media Transcoder 1.1.22.0 より前 / オープンウェーブメッセージング | ログインできる攻撃者が細工したファイルをアップロードすると、機微な情報を取得される (CWE-669) | JVN の評価は「緊急」 | [JVN](https://jvn.jp/vu/JVNVU93403064/) |
| 2026-11-09 | JVN#76179675 / CVE-2026-109582 ほか | SS1 / SS1 クラウド (エージェント 17.0.0.50 以前) / ディー・オー・エス、ODM 製品 rocoeyes / ロココ | IT 資産管理のエージェントに、重要な情報の安全でない保存と、認証なしのパストラバーサル | v4 6.9 (最大) | [JVN](https://jvn.jp/jp/JVN76179675/) |
| 2026-11-09 | JVNVU#92635551 | KUSANAGI 7 / 8 / 9 (Security・Enterprise 10.7.2-1 以前、Free・Business・Premium 9.12.2-1 以前) / GMO プライム・ストラテジー | WordPress 向けの Nginx の設定のリダイレクトルールで CRLF を無害化せず、細工した URL で任意の HTTP ヘッダーを挿入 | v3.1 6.1 | [JVN](https://jvn.jp/vu/JVNVU92635551/) |
| 2026-11-09 | JVN#56286875 | Effekseer 1.80.8 未満 (パーティクルエフェクトのランタイム) | 細工したエフェクトファイルの読み込みで範囲外読み取り → アプリが異常終了 | v4 5.1 | [JVN](https://jvn.jp/jp/JVN56286875/) / [commit 6cf1cb8](https://github.com/effekseer/Effekseer/commit/6cf1cb8) |
| 2026-11-09 (更新) | JVN#42011956 / CVE-2026-59781 | Zabbix agent (Windows) / Zabbix | 任意のインストール先の検証が不十分で、権限の弱い場所に入り、DLL サイドローディングの恐れ (報告: GMO イエラエ 松本 一真 氏) | v3 6.7 | [JVN](https://jvn.jp/jp/JVN42011956/) |

- 補足: WebSAM WinShare は、リモートデスクトップの用途で官公庁や企業で使われる。v3 9.8 の 2 件は「細工したパケット」で届くので、社内のネットワークで操作対象の PC の待ち受けポートが広く開いていないかを確かめたい。KUSANAGI は国内の WordPress のホスティングで広く使われ、設定ファイルの更新が必要だ。

### 国内コミュニティ・研究・イベント

#### [2026-11-09] piyolog、2 件のまとめを公開: 「相次ぐメール配信サービスへの不正アクセス」と「ドコモオンラインショップと My docomo への不正アクセス」
- **何が起きたか**:
  - メール配信の件では、ラクスライトクラウド (API サーバー 2 台への侵入から)、ユミルリンク (Cuenote FC のライブラリの脆弱性、Cuenote BASE のプログラムの脆弱性、操作画面と API に IP 制限がなかった環境)、アララ (共用環境の管理画面への不正ログインと、別のクラウド環境での認証情報の不正使用) など 5 社の経過を、分単位で並べた。
  - ドコモの件では、11/4 の 7 時ごろから検知の閾値に達しない動きが始まっていたこと、d アカウントを入口に「複数のシステムが連動してデータを処理する仕組み」を悪用し、ある内部システムがデータを解釈する段階で暗号化やマスキングが外れた後のデータを取得されたことを整理した。
- **なぜ重要か (評価)**: どちらも「認証は破られていない」「保存時と通信時は暗号化していた」のに漏れた。診断では、正規のログインの後の API の連鎖で、他人のデータに届くか (BOLA / IDOR) を見ることが中心になる。
- 出典: [piyolog (メール配信)](https://piyolog.hatenadiary.jp/entry/2026/11/09/230435) / [piyolog (ドコモ)](https://piyolog.hatenadiary.jp/entry/2026/11/09/090504)

#### [2026-11-09] @IT の連載: レンタルサーバーに構築したクーポンサイトから 603 件のカード情報が漏れ、決済代行が約 1,903 万円の賠償を求めた訴訟。「セキュリティはサーバー事業者に任せていた」との主張に、裁判所は 9 つの対策を具体的に挙げて判断
- **何が起きたか**: 加盟店は、契約で「カード情報が第三者に閲覧、改ざん、破壊されないための措置」を義務づけられていた。訴訟では「レンタルサーバーを使い、専門の事業者にセキュリティを任せていたことで義務を果たしたか」が争点になった。裁判所は、加盟店が講じるべきだった対策を 9 つ具体的に挙げた。記事は、その判決を「何をどこまでやるべきか」の目安として紹介している。
- **なぜ重要か (評価)**: EC サイトの運営者、構築ベンダー、サーバー事業者の責任の分担は、診断の報告書で「誰が直すか」を書く際の前提になる。顧客への説明の材料として使える。
- 出典: [@IT (2026-11-09)](https://atmarkit.itmedia.co.jp/ait/articles/2611/09/news003.html)

#### [2026-11-09] ScanNetSecurity、編集長の上野宣氏が AI SOC の Exaforce に「20 の質問」をぶつけた対談を掲載
- **何が起きたか**: 対談の相手は Exaforce の技術者 Shang Li 氏。Exaforce は 2023 年創業の米国 (サンノゼ) の企業で、従業員 140 人以上、累計の調達額は 2 億ドル。アラートのトリアージから調査、対応までを AI エージェントに任せる「Agentic SOC」を提供している。Exaforce 側が「予定調和の記事にしたくない」として ScanNetSecurity を選んだといい、厳しめの質問を前提に行われた。
- **なぜ重要か (評価)**: 攻撃側の研究者として知られる上野氏が、防御の AI 化を正面から問うた記事だ。AI SOC の導入を検討する組織が、ベンダーに確かめる質問の参考になる (本文の後半は会員限定で、20 の質問の中身は未確認)。
- 出典: [ScanNetSecurity (2026-11-09)](https://scan.netsecurity.ne.jp/article/2026/11/09/56710.html)

#### [2026-11-09 掲載] NRI セキュア、学生向けの CTF「SANS NetWars トーナメント 2026」を 11/21 にオンラインで開催。申し込みは 11/13 17 時まで
- **何が起きたか**: 対象は 18 歳以上の働いていない学生で、参加は無料、定員は 100 人 (多い場合は抽選)。攻撃と防御の「Core NetWars」を個人戦で行う。上位者には SANS の公式トロフィーや iPad が贈られる。告知は 11/6。
- **なぜ重要か (評価)**: 学生の採用や育成の接点として、締め切りが近い。
- 出典: [ScanNetSecurity (2026-11-09)](https://scan.netsecurity.ne.jp/article/2026/11/09/56699.html)

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 50 (RSS 42 本: JVN、JVN iPedia、JPCERT/CC、IPA、piyolog、Security NEXT、ScanNetSecurity、BleepingComputer、The Hacker News、SecurityWeek、Help Net Security、The Record、Dark Reading、Ars Technica、TechCrunch、The Verge、ITmedia AI+、@IT、GIGAZINE、Publickey、SANS ISC、GBHackers、CyberScoop、Unit 42、OpenAI、Hugging Face、oss-security、Simon Willison、HN など。API: CISA KEV JSON、NVD、OSV (npm / PyPI / Go / Maven / crates.io / Packagist / RubyGems / NuGet の modified_id.csv)、EPSS。WebSearch で国内の 11/9 公表の事案を補完)
- 採用件数: AI技術=13 / AIセキュリティ=7 / セキュリティ=16 / CVE=13 / 国内インシデント=4 / 国内政策=3 / JVN=6 / 国内コミュニティ=4
- 除外理由内訳: 古すぎ=約 20 (React Server Components の GHSA-xqc2-xf4c-x3h3 は 10/14 公開、ModSecurity の 2 件は 9/30 公開、Gemini の安全フィルターの回避は 11/5 公開、PSI のアーロンソン=アンバイニス予想の証明は 11/6 発表、Goldman の AI 制限は 11/2 報道、CISA / FBI の冷蔵設備のファクトシートは 11/5、ネットマイル、ソニー生命、花キューピットなどの国内の事案) / 重複=約 15 (sshole の初報、ARTEX と WorkOS、Claude Code の settings.local.json の秘密情報 (Ars、GIGAZINE の 11/9 の記事は 11/8 号の既報と同内容)、Agent Substrate の CNCF への寄贈、FBI の捜査官の暗号資産の横領、Ripple-65B、Arete-27B、Jensen Huang 氏の件、JNSA、ロート製薬、ドコモの第一報 など) / 日付不明=約 3 (オープンドア (トラベルコ) の件は公表文を確認できず不採用、Zyphra の MAIA は公開日を確認できず不採用)
- 取得失敗ソース: Dark Reading の個別記事 (「Claude の 'Office Party' の欠陥」の記事は、curl と WebFetch の両方で本文を取得できず (403)、内容を確認できないため不採用)、openai.com の記事本文 (403。RSS の要約で代替)、GitHub Advisory API (セッションの制約で使えず、OSV で代替)、CISA の advisories RSS / GTIG / MSRC / Rapid7 の RSS (XML の解析に失敗)、Wiz の Qubole のブログ本文 (未取得。The Hacker News の詳細な引用で代替)。ニトリ HD とシェアフルの公表文は直接取得しておらず、二次記事 (セキュリティ対策 Lab) で確認した。
- 備考: 米国時間 11/10 の Microsoft の月例更新 (Patch Tuesday) は、生成時点 (11/10 05:10 JST) では未公開。

</details>
