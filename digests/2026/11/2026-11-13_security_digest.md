# KEDA Daily Digest — 2026-11-13 (JST)

> 採用範囲: 公開日 2026-11-11 〜 2026-11-13
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

セキュリティ側で最も大きいのは、**N-able N-central の新しいゼロデイ「4EverAble2Shell」** だ。11/10 の緊急修正版 (2026.4 HF2) にも効き、PoC が公開されてから数時間で悪用が始まった。11/12 の時点で、HF2 を当てたサーバー 19 台を含む 21 台にマイナーが入っている (今日の深掘り)。RMM ではほかにも、**ScreenConnect のパートナー環境を使って MSP の顧客にクライアントを配る攻撃** がある。この攻撃のツール「SCKit」は、調査に入った技術者の PC にまで感染を広げようとする。
パッチでは、**Apache httpd 2.4.71 の mod_http2 の未認証のヒープ破壊 (CVE-2026-119618)** が出た。Anthropic と Google が独立に見つけ、クラッシュの PoC がもう公開されている。ほかに、**Red Hat Quay の Critical 2 件**、**PostgreSQL の 52 件の一括修正**、**Node.js の 16 件**、**Citrix NetScaler の 12 件**、**Windows の LPE「SignDrop」の PoC (修正なし)** と続き、修正の量が多い 2 日間だった。サプライチェーンでは、**GitHub のアカウント 4,837 個を乗っ取り、CI の秘密情報を盗む「wfx-loot」** が 1,800 を超えるリポジトリで実行された。CISA KEV には、11/11 以降の追加がない。
AI 側では、Google が安価な実行用モデル **Gemini 4 Hydrogen** を検索にまで一斉に入れた。Anthropic は製造業向けのプラグインを出した。AI セキュリティでは、**国家系の攻撃者が AI エージェントに偵察やログ消去まで任せていた実例が 2 件** 出た。CloudSEK の Silent Lynx と、Unit 42 の Cairn だ。**MCP サーバーの CVE** (AWS の mcp-gateway-registry の SSRF、pgEdge の読み取り専用モードの回避) も出た。
国内では、**SMBC 日興証券の持株会管理システム (最大 56,487 人)**、**オープンロジ (EC 物流、7 か月分のお届け先)**、**電通デジタル TONARIWA (LINE 公式アカウントの連携トークンも漏えいのおそれ)**、**サイバーセキュリティクラウド (従業員の GitHub 認証情報の流出)** が公表された。委託先の SaaS 1 社から、多数の利用企業へ被害が広がる案件が続いている。
**今日まず見るべき 2 件**: (1) N-central を使っているなら、Legacy API を無効にし、IOC を確かめる (深掘り参照)。(2) HTTP/2 を有効にしている Apache httpd 2.4.55〜2.4.70 を洗い出し、2.4.71 に上げるか、それまで h2 を止める。

## 今日の深掘り

### [続報] N-able N-central「4EverAble2Shell」: 11/10 の緊急修正版 (HF2) を当てたサーバーでも、未認証で root の RCE が成立する。PoC の公開から約 1 時間後には探索が始まり、半日でマイナーの設置まで確認された

- **概要 (事実)**:
  - 「Able2Shell」を公開した研究者の Sean Bales 氏が、11/12 に新しいエクスプロイトを 2 本公開した。どちらも N-central Appliance 2026.4.1.26 HF2 (11/10 の緊急修正版) で動くことを確かめたという。
  - **4EverAble2Shell**: 未認証で、root として任意のコードを実行できる。条件は Legacy API が有効なこと (既定は無効)。
  - **Agent2Shell**: 管理下の Windows エージェントで、SYSTEM としてコマンドを実行できる。標的のアプライアンス ID を知っている必要がある。
  - 観測された時系列 (いずれも 11/12、UTC):
    - Previdian は 08:30 ごろ、157.20.241[.]16 からの探索を観測した。
    - Huntback は 09:16 に、チェーン全体が実行されたのを確認した。
    - 12:50 には、XMRig (ワーカー名 `nc_<IP>`) が動いている N-central が 21 台見つかった。うち 19 台は HF2 を当てていた。国は米国、カナダ、南アフリカ、英国、ドイツ、フランス、スウェーデンにまたがる。
  - N-able は 11/12 の advisory で、Legacy API を無効にするよう求め、Intune 連携を予防として止めた。ホスティング版には対策を当てたとしている。一方で advisory は「悪用の兆候はない」としており、上の観測と食い違う。watchTowr も、Legacy API が有効な環境を探す通信を観測している。
- **技術的な中身**:
  - 入口は Apache Axis の既知の欠陥 CVE-2026-90436 (CVSS 9.8、N-central での修正は 11/6)。`/dms/services/ServerUI` に `jline.internal.TerminalLineSettings` を含むリクエストを送り、`nable` サービスアカウントとしてコードを実行する。
  - 次に root へ昇格する。特権ヘルパーの `setLDFileOwner` とシンボリックリンクを使って、root が所有するスクリプトを書き込み可能にする。そのスクリプトを書き換えたうえで、`serverControl` に実行させる (Previdian の分析)。
  - 「HF2 で直した欠陥とは別の経路」を組み合わせているので、HF2 だけでは止まらない。
  - 永続化と痕跡: systemd の `xvd.service` と、`/tmp/.xvd`、`/var/tmp/.xvd` の下のファイル。
- **背景・経緯 (過去の経緯の引用)**:
  - 11/9〜10、同じ研究者が N-central の 30 件を超えるゼロデイを PoC 付きで公開した (Able2Shell。11/11 号で既報)。N-able はホスティング版をいったん止め、11/10 に HF2 を出した。翌日にはもう探索が始まっていた (11/12 号で既報)。
  - 同じ時期に、ScreenConnect のパートナー環境を使った MSP への攻撃も起きている (本号のセキュリティニュース参照)。2021 年の Kaseya VSA の事件と同じく、RMM は「1 か所を破れば顧客全体に届く」ので、攻撃者が最も狙う場所になっている。
- **なぜ今これが重要か (評価)**:
  - 「パッチを当てた」という報告が、2 日で意味をなさなくなった。PoC が公開されていて、悪用までの時間は数時間だった。CVE も KEV もまだ付いていない (Previdian は自社の KEV に VULN-2026-0009 として登録)。脆弱性スキャナーの CVE 照合だけでは見落とす。
  - いまの悪用はマイナーの設置だが、RMM の root を取られれば、Agent2Shell と組み合わせて管理下の全端末に SYSTEM で届く。ランサムウェアに転用されるまでの時間は短いと見るべきだ。
  - 診断やペンテストでは、MSP や情報システム部門の RMM を「スコープ外のインフラ」として扱わず、管理面の API が外部から届くかどうかを優先して確かめたい。
- **読者が今日できること**:
  - N-central の設定で Legacy API が無効になっているかを確かめる。外部から `/dms/services/` が届かないことを、ファイアウォールのルールと実際の通信の両方で確かめる。
  - Web のログで `/dms/services/ServerUI` に `jline.internal.TerminalLineSettings` を含むリクエストがないかを探す。ホストでは `systemctl status xvd.service` と `ls -la /tmp/.xvd /var/tmp/.xvd` を確かめる。157.20.241[.]16 との通信も探す。
  - 顧客の環境を管理している立場なら、Intune 連携が止まった影響と、管理下のエージェントで不審なコマンドの実行がないかを確認する。
- 出典: [BleepingComputer (2026-11-12)](https://www.bleepingcomputer.com/news/security/new-n-able-4everable2shell-zero-day-exploited-hours-after-poc-released/) / [The Hacker News (2026-11-12)](https://thehackernews.com/2026/11/new-n-central-exploits-work-against.html) / [SecurityWeek (2026-11-12)](https://www.securityweek.com/hackers-target-n-central-zero-days-as-n-able-rushes-patches/)

## AI 技術・トレンド

### [2026-11-12] Google、実行用のモデル「Gemini 4 Hydrogen」を公開。100 万トークンあたり入力 1.50 ドル / 出力 7.50 ドルで、1M コンテキストまで同じ価格。Google 検索の AI 回答も Hydrogen に
- **何が起きたか**: Google は、Carbon / Argon の下に位置づける Gemini 4 Hydrogen の提供を始めた。提供先は Gemini API / AI Studio、Gemini アプリ、Google 検索 (全世界)、Antigravity で、すべて同じ日。思考レベルは 4 段階、入出力とも最大 100 万トークン。Google は、Terminal-Bench 4.1 で 57% (Gemini 3.8 Flash は 18.2%)、作り話は 5 分の 1 以下と主張している。Antigravity には、同じセッションの中で Carbon と Hydrogen を切り替える「Orchestrator」が入った。
- **なぜ重要か**: 検索の AI 回答のモデルが替わったので、検索の AI 回答を狙った間接プロンプトインジェクションの検証は、やり直しになる。「安いモデルが作業し、強いモデルが指揮する」構成が標準の機能になった。そうなると、作業役のモデルの脆さがエージェント全体の弱点になりやすい。
- 出典: [Google (2026-11-12)](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/) / [Google 検索 (2026-11-12)](https://blog.google/products-and-platforms/products/search/gemini-4-hydrogen-search-upgrade/)

### [2026-11-12] Google Antigravity に「リモートエージェント」: タスクを Google が管理するクラウドの VM で動かし、PC を切っても続く
- **何が起きたか**: エージェントのタスクを、Google が管理する独立したクラウドの VM で実行できるようになった。対象のコードは GitHub のリポジトリ、Google ドライブ、アップロードから選ぶ。権限の確認はスマートフォンから承認できる。対象は個人の Google アカウントの AI Pro / Ultra。
- **なぜ重要か**: GitHub への書き込み権限を持ったエージェントが、人のいない時間にクラウドで動く。スマホでの承認は、中身を見ずに押す運用になりやすい。トークンの範囲と、VM から外への通信の制限を確かめておきたい。
- 出典: [Publickey (2026-11-12)](https://www.publickey1.jp/blog/26/google_antigravityaiai.html)

### [2026-11-12] Anthropic「Claude for Manufacturing」: 見積もり、品質の調査、保全の診断など、17 のスキルを入れた製造業向けのプラグイン
- **何が起きたか**: Team / Enterprise の管理者が入れるプラグインで、見積もり、NCR・8D レポートの下書き、センサーのデータと手順書を使った故障原因の順位づけ、朝の生産レポート、調達の RFQ などのスキルを含む。コネクターは Infor、Microsoft 365、Autodesk Fusion など。中心のプラグインは基幹システムに書き込まない。発注を変える処理は別の「Infor in Claude」プラグインが受け持ち、購買担当の承認と Infor の権限に従う。
- **なぜ重要か**: 図面、検査記録、保全のメモといった現場の文書が LLM の入力になる。読み取りと書き込みを別のプラグインに分けた設計なので、診断では「参照用のコネクターで読んだ文書の指示が、書き込み側のプラグインに渡るか」(プロンプトインジェクションによる権限の昇格) を確かめるのが要点になる。
- 出典: [Claude (2026-11-12)](https://claude.com/resources/articles/claude-for-manufacturing) / [Unite.AI (2026-11-12)](https://www.unite.ai/anthropic-launches-claude-for-manufacturing-with-17-workflow-skills/)

### [2026-11-11 告知 / 11-12 報道] OpenAI API で「日本国内での推論」が可能に。対象は GPT-6 Luna (gpt-6-luna) だけ
- **何が起きたか**: データの所在地域を指定した推論の対象に、日本が加わった。対象は Responses API と Chat Completions API の gpt-6-luna で、Standard の従量課金だけ。OpenAI に申請し、MAM (不正利用の監視の変更) と ZDR (データを保持しない) の承認を受ける必要がある。GPT-6 Luna の料金は、100 万トークンあたり入力 0.1 ドル、出力 0.5 ドル。
- **なぜ重要か**: 金融や公共などで「推論も国内で」という条件の案件に、OpenAI の API を使えるようになった。ZDR が前提なので、不正利用を調べるときに OpenAI 側のログには頼れない。利用する側で、プロンプトと出力の監査ログを持つ必要がある。
- 出典: [ITmedia AI+ (2026-11-12)](https://www.itmedia.co.jp/aiplus/article/2611/12/2000003129/)

### [2026-11-11] AWS「AWS Emulator」を公開 (CC0): AWS の API をローカルで再現するツールで、コードはすべて AI エージェントが書き、人はレビューしていない
- **何が起きたか**: AWS の API モデル 438 件をもとに、数百のサービスのエンドポイントをメモリ上に再現する。AWS CLI / SDK の接続先を環境変数で切り替えて使う。AWS によると、Kiro で動く数百のエージェントが、テストを作るチーム、実行して報告するチーム、直すチームに分かれて開発した。IAM やリソースベースのポリシーは本物と同じには評価されないので、セキュリティの試験には使わないよう AWS は注意している。
- **なぜ重要か**: 人のレビューを経ていない大規模なコードが、公式のツールとして配られている。CI で使う場合は「テストが通ってもアクセス制御の確認にはならない」ことを周知する必要がある。ネットワークに公開して動かしたときの攻撃面 (認証のないエンドポイント) も確かめておきたい。
- 出典: [ITmedia NEWS (2026-11-12)](https://www.itmedia.co.jp/news/article/2611/12/2000003126/) / [Simon Willison (2026-11-11)](https://simonwillison.net/2026/Nov/11/aws-emulator/)

### [2026-11-12] IBM、LLM 向けのマークアップ言語「LLMON」と、それを学習した Granite 4.1 の 3B / 8B のプレビュー版を公開
- **何が起きたか**: システムプロンプト、取得した文書、ツールの応答、利用者のデータを、予約済みの特殊トークンで作ったタグで包む。一意の ID で「どの指示がどのデータに作用するか」を結びつける。IBM は、文脈の構造があいまいなことが小さいモデルの脆さとプロンプトインジェクションの原因だとし、LLMON でそれを減らせると主張している。
- **なぜ重要か**: 「指示とデータを分ける」ことを、トークンの層で強制しようとする試みだ。評価するときは、外部の入力から予約トークンを偽造・注入できないか (トークナイザーの段階でエスケープされるか) を真っ先に確かめるべきだ。
- 出典: [Hugging Face Blog (2026-11-12)](https://huggingface.co/blog/ibm-granite/llmon-an-llm-native-markup-language-now-in-granite)

### [2026-11-11〜12] Meta のエージェント「Muse」に専用のメールアドレス (@muse.ai)。予約の送信、転送メールの予定の登録などを代行
- **何が起きたか**: Muse に独自のアドレスと差出人名を設定でき、予約メールの送信、転送されたメールの予定のカレンダーへの登録、長文の要約に使える。認証した別のアドレスから、Muse に指示を送ることもできる。まずは米国とカナダの有料ユーザー向けで (11/11 発表)、日本でも取得の報告が出ている。
- **なぜ重要か**: 外から届くメールがそのままエージェントの入力になり、エージェントは送信とカレンダー操作の権限を持つ。典型的な間接プロンプトインジェクションの経路だ。「認証済みの指示元アドレス」の判定が、差出人の偽装 (SPF / DKIM / DMARC の扱い) に耐えられるかは確かめる価値がある。
- 出典: [ITmedia AI+ (2026-11-12)](https://www.itmedia.co.jp/aiplus/article/2611/12/2000003136/)

### [2026-11-11] Google DeepMind、ロボット用のモデル「Gemini Robotics 2.5」と、DNA の変異の影響を予測する「AlphaGenome 2」を発表
- **何が起きたか**: DeepMind は、Gemini Robotics 2.5 が Mercedes-Benz の実証で自動車部品の箱詰めに 96% 成功し、従来版より 20〜30% 速いと主張している。物理的な操作の安全性について、脱獄への耐性を測る新しいベンチマークも入れた。AlphaGenome 2 は、ヒトとマウスの 68 組織、1 億を超える細胞のデータで学習した。研究用は API で使え、商用は限定プレビュー。
- **なぜ重要か**: ロボット用のモデルで「脱獄のベンチマーク」が公式の評価項目になった。物理的な危害につながるプロンプトインジェクションを、ベンダー自身が攻撃面として扱い始めたことを示す。
- 出典: [SiliconANGLE (2026-11-11)](https://siliconangle.com/2026/11/11/google-deepmind-releases-new-advanced-robotics-ai-model-and-next-generation-gene-prediction-model) / [ITmedia NEWS (2026-11-12)](https://www.itmedia.co.jp/news/article/2611/12/2000003132/)

### [2026-11-12 施行] Anthropic の地域による利用制限が発効: 中国本土からの利用と、制限地域の主体が支配する組織の利用を禁止
- **何が起きたか**: Claude.ai、API、クラウド経由のすべてで、中国本土などサポート外の地域からの利用と、その地域の個人や組織が直接・間接に支配する主体の利用を禁じた。改定の発表は 10/8。Anthropic は 4 月から Persona による本人確認を入れている。OpenAI も、GPT への直接のアクセスを提供する他社のプラットフォームに、事前の承認を求める (11/20 から)。
- **なぜ重要か**: 中継サービス経由の利用の取り締まりが強まると、盗んだ API キーや乗っ取ったアカウントの需要が増えると考えられる。AI の API キーの漏えい検知と、使われ方の異常の監視の優先度が上がる。
- 出典: [TokenPost (2026-11-11)](https://www.tokenpost.com/news/technology/53665)

### [2026-11-12] [続報] NVIDIA の Jensen Huang CEO が辞任。CFO の Colette Kress 氏が暫定 CEO に、元 Synopsys CEO の Harvey C. Jones 氏が初めての取締役会議長に
- **前回から何が変わったか**: 11/7〜8 号では、諜報の疑いと取締役会の調査の開始を伝えた。取締役会は 11/11 (米国時間) の深夜に、CEO、社長、取締役のすべてから退く Huang 氏の辞表を受理し、即日で発効した。正式な後任は社内外から探す。TechCrunch によると、Huang 氏は議会での証言に応じた。
- **なぜ重要か**: AI 向け GPU の供給と、対中国の輸出規制の両方の中心にいた人物が退いた。発端は「中国の情報機関が CEO の周辺を通じて接近した」という疑いで、AI のサプライチェーンの頂点の人物が内部脅威の標的になる例になった。
- 出典: [The Verge (2026-11-12)](https://www.theverge.com/ai-artificial-intelligence/1031689/jensen-huang-nvidia-ceo-resigns) / [TechCrunch (2026-11-12)](https://techcrunch.com/2026/11/12/jensen-huang-agrees-to-testify-before-congress/)

### [2026-11-11 発表 / 11-12 報道] 国内: パナソニック HD、250 人体制で「フィジカル AI」。熟練者の暗黙知を AI にし、外販も視野に
- **何が起きたか**: 10/1 に新設した「AI・ロボティクス本部」が中心になり、3 次元の空間認識、ロボットの制御、物流の荷扱いの AI などに取り組む。組み立てのときの力加減のような熟練者の知識を、センサーのデータから学習させる。グループの工場で確かめたうえで、外部にも提供する。
- **なぜ重要か**: 国内の製造業で、OT の現場のデータを AI の学習に使う動きが大きくなっている。センサーのデータの改ざん (データポイズニング) と、ロボットの制御系の分離は、OT の診断の新しい観点になる。
- 出典: [ITmedia ビジネス (2026-11-12)](https://www.itmedia.co.jp/business/articles/2611/12/news037.html)

## AI セキュリティ

### [2026-11-12] Unit 42: 中国語話者の攻撃者 (CL-STA-1238) が、オープンソースの AI ペンテスト基盤「Cairn」と GLM / DeepSeek で 19 組織に自律的な攻撃を 25 回。10 組織で侵入やデータの取得に成功
- **何が起きたか**: Unit 42 によると、期間は 2026 年 8〜9 月で、標的は先端半導体、米国の国防政策、市民社会。成果として、有効な認証情報の取得、100 万件を超える個人データの露出、本番システムへの永続的な管理者アカウントの作成、業界標準の投票文書の改ざんがあった。Cairn は、複数のエージェントが「黒板」を共有する構成で、人が途中でヒントを入れられる。Unit 42 は、中国系の情報収集活動と中程度の確度で評価している。
- **なぜ重要か**: 11/12 号の AntiFox に続き、公開の AI ペンテスト基盤がそのまま実際の攻撃に使われた。攻撃の数と速さが、人の手作業の前提を超えてくる。防御側は、短い時間に多数のパスを試すような機械的な偵察のパターンを、検知のルールに入れておきたい。
- 出典: [Unit 42 (2026-11-12)](https://unit42.paloaltonetworks.com/cairn-framework-ai-autonomous-attacks/) / [Help Net Security (2026-11-12)](https://www.helpnetsecurity.com/2026/11/12/cairn-autonomous-ai-cyberattacks/)

### [2026-11-11] CloudSEK: 中央アジアの諜報グループ Silent Lynx のサーバーが公開状態に。DeepSeek で動く AI エージェント (Hermes) に偵察、収集、ログの消去を任せ、破壊的なコマンドも事前に承認していた
- **何が起きたか**: 公開ディレクトリに、2026 年 4〜10 月のツール、侵入先のデータ、エージェントとの会話が残っていた。オープンソースのエージェント基盤 Hermes から、OpenRouter 経由で主に DeepSeek V4.1 Flash を呼んでいた。永続メモリ、サブエージェントのタスクボード、cron、攻撃用のスキルのライブラリを持たせ、ペルソナには「安全上の注意書きを省く」「検知されにくい手法を選ぶ」と指示していた。成果として、タジキスタンの鉄道網のドメインレベルのアクセス、2,000 を超える政府文書、ウズベキスタンの地理空間基盤への Web シェルがあった。エージェント自身がログを消していたが、公開ディレクトリは消し漏らした。
- **なぜ重要か**: 国家系の攻撃者がエージェントに「事前に承認した破壊的なコマンド」と後片付けまで任せていたことを、実物の設定と会話で示した数少ない例だ。インシデント対応では、`.hermes/` のようなエージェントの作業ディレクトリと、OpenRouter などの LLM の中継サービスへの通信を、痕跡として探す価値がある。
- 出典: [CloudSEK (2026-11-11)](https://www.cloudsek.com/blog/off-the-rails-inside-an-exposed-silent-lynx-server)

### [2026-11-11〜12] MCP サーバーの CVE: AWS の mcp-gateway-registry に SSRF (CVE-2026-125926、8.5)。pgEdge Postgres MCP Server は読み取り専用モードをすり抜けられる (CVE-2026-126196 ほか 2 件)
- **何が起きたか**:
  - mcp-gateway-registry (1.35.0 未満): サーバーの登録・更新の API に SSRF がある。認証済みの利用者が、ゲートウェイから内部のサービスやインスタンスメタデータ (IMDS) にリクエストを送らせ、応答を読める (AWS Security Bulletin 2026-180-aws)。
  - pgEdge Postgres MCP Server (1.1.0 未満): 読み取り専用の接続で、`query_database` は認識できない文をパラメーターなしで pgx の Exec に送る。セミコロンで区切った複数の文が通るので、トランザクションの状態を変えて書き込める。状態はプールしたセッションに残り、後の呼び出しも書き込み可能になる (126196、8.1)。
  - 同梱のクライアントの書き込み確認は、最初のキーワードやツール名だけで判定していた。そのため、`WITH` で始まる更新系の CTE、`SELECT INTO`、`EXPLAIN ANALYZE` が確認なしに通った (126199 は 6.8、126198 は 3.1)。advisory は、取得した文書の中の指示にモデルが従った場合も、悪用の経路になると明記している。
- **なぜ重要か**: どちらもバリアントハントの型としてそのまま使える。1 つは「MCP のゲートウェイやレジストリが URL を受け取る箇所の SSRF」。もう 1 つは「SQL 系の MCP サーバーの読み取り専用を、先頭キーワードの判定で実装している」パターンだ。後者は、プロンプトインジェクションから DB の改ざんに直結する。
- 出典: [CVE-2026-125926](https://www.cve.org/CVERecord?id=CVE-2026-125926) / [AWS Security Bulletin](https://aws.amazon.com/security/security-bulletins/2026-180-aws/) / [GHSA-j7mp-839j-jrm7](https://github.com/pgEdge/pgedge-postgres-mcp/security/advisories/GHSA-j7mp-839j-jrm7) / [GHSA-5gmh-9683-hhq9](https://github.com/pgEdge/pgedge-postgres-mcp/security/advisories/GHSA-5gmh-9683-hhq9) / [GHSA-v44x-hxg7-5cgc](https://github.com/pgEdge/pgedge-postgres-mcp/security/advisories/GHSA-v44x-hxg7-5cgc)

### [2026-11-12] スクレイピング・ブラウザ自動化の基盤 Apify に不正アクセス (11/9〜10)。API トークンとプロキシのパスワードを入れ替え、GitHub などの OAuth 連携を取り消し、一部の顧客に 2FA の再設定を求める
- **何が起きたか**: Apify は、11/9〜10 に第三者が内部のシステムの一部に入り、11/11 12:13 UTC に検知したと公表した。内部の認証情報を無効にし、顧客の API トークンを更新し、全セッションをリセットし、GitHub を含む外部連携の OAuth を取り消した。一部の顧客には「2FA のコードが露出した可能性がある」として再設定を求めた (パスワードは無事だとしている)。顧客は約 8 万社。
- **なぜ重要か**: Apify はエージェントや RAG にデータを渡す基盤で、Actor が MCP のツールとして呼ばれることも多い。推論基盤の Fireworks AI に続き、AI 向けのデータやツールの供給者が侵害された。Apify のトークンを埋め込んだエージェントや MCP の設定はトークンを入れ替え、OAuth で連携した GitHub の監査ログも確かめたい。
- 出典: [BleepingComputer (2026-11-12)](https://www.bleepingcomputer.com/news/security/apify-rotates-api-tokens-prompts-2fa-resets-after-breach/)

### [2026-11-12] Island「TypoPrompting」: 27 の AI ブランドを装う 186 のタイポドメインから、ClickFix、ブラウザを乗っ取るマルウェア、検索を乗っ取る拡張機能へ誘導
- **何が起きたか**: Claude、ChatGPT、Gemini、Copilot、Grok、DeepSeek、Perplexity、Cursor などの打ち間違いのドメイン (例: cloude[.]ai、cluade[.]ai) が、パーキングの TDS を経て 3 つの経路に誘導していた。1 つ目は、偽の Cloudflare 認証で PowerShell (macOS ではシェルのコマンド) を実行させる ClickFix。2 つ目は、ブラウザを乗っ取る Net Guard。3 つ目は、Chrome Web Store に 16 件、宣言上の利用者が 97.2 万人の、検索を乗っ取る拡張機能だ。
- **なぜ重要か**: AI ツールを使う開発者は、CLI や拡張機能を自分で入れる権限を持っていることが多く、ClickFix の格好の標的になる。社内の DNS やプロキシで、主要な AI ブランドの打ち間違いのドメインを監視・遮断する根拠になる。
- 出典: [Island (2026-11-12)](https://www.island.io/blog/typoprompting-from-ai-typos-to-malware) / [The Hacker News (2026-11-12)](https://thehackernews.com/2026/11/186-fake-ai-domains-redirect-users-to.html)

### [2026-11-12] AI チャットボットが偽の通販サイトを勧める: Podqi の調査で、「危険な」URL を含んだ回答は Perplexity が 15%、ChatGPT が 8%、Gemini が 4%
- **何が起きたか**: 知的財産の保護を手がける Podqi が、151 ブランドについての買い物の質問を 3 つの AI に投げ、6,795 件の回答を集めた。偽物を売るサイト、第三者に再登録された旧ドメイン、取得できる状態の失効ドメインを「危険」として数えた。小さいブランドほど危険なサイトが出やすく、大手の約 2 倍だった。調査は Podqi が作ったプロンプトによるもので、実際の利用者の会話ではない。
- **なぜ重要か**: 失効ドメインの再取得や、AI 検索を狙った引用の汚染が、そのままフィッシングの誘導経路になる。ブランドを守る側は、失効ドメインと旧ドメインの棚卸しを、AI 検索の引用の監視とあわせて行う必要がある。
- 出典: [The Verge (2026-11-12)](https://www.theverge.com/ai-artificial-intelligence/1032020/gemini-chatgpt-perplexity-shopping-test-risky-fake-websites-citations)

### [2026-11-11 arXiv] RAG のアクセス制御を「埋め込みの変換」で行う方式は、元の埋め込みの復元とクエリの偽造に弱い (arXiv:2611.14061)。あわせて、1 回の応答から 51 のモデルを 92.72% で識別する NumPrint (arXiv:2611.14010)
- **何が起きたか**:
  - 2611.14061 は、文書ごとのアクセス方針を埋め込み空間の変換で強制する既存の方式を、3 つのエンコーダーで評価した。好奇心のある利用者は、数百組の (元の埋め込み, 変換後) から元の埋め込みを復元し、方針に合うクエリを偽造できた。
  - 2611.14010 (NumPrint) は、「1〜355 の整数を 294 個出して」という 1 回の応答から、51 のモデルを 92.72% の精度で識別した (4 回の応答では 97.12%)。
- **なぜ重要か**: 前者は、「埋め込みを変換したので、権限のない文書は出てこない」と説明する RAG の製品を診断するときに、そのまま反証の手順として使える。後者は、中継業者のモデルのすり替えの検出に使える。逆に攻撃者には、相手の AI 製品の裏のモデルを特定し、それに効く脱獄を選ぶ偵察手段になる。
- 出典: [arXiv:2611.14061](https://arxiv.org/abs/2611.14061) / [arXiv:2611.14010](https://arxiv.org/abs/2611.14010)

## セキュリティニュース

### [2026-11-12] [続報] N-able N-central「4EverAble2Shell」「Agent2Shell」: 11/10 の修正版 (HF2) にも効く。PoC の公開から数時間で悪用が始まり、マイナーが設置された
- **何が起きたか / 悪用・PoC**: 今日の深掘りを参照。**悪用あり**、**PoC 公開**。CVE と KEV への登録はまだない。
- 出典: [BleepingComputer (2026-11-12)](https://www.bleepingcomputer.com/news/security/new-n-able-4everable2shell-zero-day-exploited-hours-after-poc-released/)

### [2026-11-11 修正 / 11-12 報道] Apache HTTP Server 2.4.71: mod_http2 の `assign_headers()` の競合状態でヒープが壊れ、未認証で RCE に至るおそれ (CVE-2026-119618、Critical)。Anthropic と Google が独立に発見
- **何が起きたか**: 影響を受けるのは 2.4.55〜2.4.70 と、単体の mod_h2 2.0.8〜2.0.42 で、HTTP/2 を有効にしている場合に限る。Anthropic の OSS Scanner が 10/26 に、Google Cloud Vulnerability Research が 11/3 に、それぞれ独立に報告した。Red Hat は CVSS 9.8 とし、「信頼できるエクスプロイトを示した公開の研究がある」と書いている (どの研究かは明かしていない)。Wiz によると、クラウド環境の 64% に該当するバージョンがあり、51% では外部に公開されている (ただし h2 が有効かどうかは考慮していない)。同じリリースで、mod_md の NULL 参照 (CVE-2026-106023) と、mod_vhost_alias の 1 バイトのスタック書き込み (CVE-2026-109163) も直った。
- **なぜ重要か**: 広く使われる Web サーバーで、未認証のネットワークから届くメモリ破壊だ。HTTP/2 を有効にしたリバースプロキシや、ディストリのパッケージの更新状況を棚卸しする価値がある。watchTowr は「今すぐパッチを当てるか、それまで h2 を止める」よう勧めている。
- **悪用 / PoC**: 悪用の報告はない。**クラッシュの PoC が公開済み** (GitHub の googlesky/CVE-2026-119618)。RCE の PoC はまだない。EPSS 0.0040。
- 出典: [Apache](https://httpd.apache.org/security/vulnerabilities_24.html) / [oss-security (2026-11-11)](https://www.openwall.com/lists/oss-security/2026/11/11/13) / [Wiz (2026-11-11)](https://www.wiz.io/blog/cve-2026-119618-rce-apache-http-server-vulnerability) / [SecurityWeek (2026-11-12)](https://www.securityweek.com/apache-patches-critical-http-server-rce-found-by-anthropic-google/)

### [2026-11-11〜12] ScreenConnect を狙った MSP への攻撃: 6 つの MSP、約 48 組織、286 台を超える端末に不正なクライアント。ツール「SCKit」は、調査に入った技術者の PC にまで感染を広げようとする
- **何が起きたか**:
  - Huntress は 11/11 17:47 UTC から、クラウド版の ScreenConnect を狙う活動を観測した。ScreenConnect の Run Command で、不正な ScreenConnect Access クライアントを配る手口だ。
  - ConnectWise はパートナーアカウントへの不正アクセスを認め、サードパーティの拡張機能 5 つ (Labtech Plus、RMM Plus、RMM+ など) を約 400 のパートナー環境で無効にした。11/12 には、RMM+ の既定の API シークレットが固定値だった問題が CVE-2026-127063 (CVSS4 9.3) として採番された。
  - Blackpoint によると、SCKit の構成要素「RelayTrap」は、接続してきた技術者の側で、既知の CVE-2026-84869 (CVSS 9.9、修正済み) を使ったファイルの実行を試みる。成功すると、技術者のブラウザのセッションを奪って、別の顧客へと広がる。
- **なぜ重要か**: N-central と並び、RMM が MSP 経由のサプライチェーン攻撃の主な入口になっている。調べに行った技術者が次の被害者になる設計なので、IR の担当者も、自分の ScreenConnect のクライアントが修正版かを確かめておくべきだ。
- **悪用 / PoC**: **悪用あり**。KEV への登録はない。
- 出典: [BleepingComputer (2026-11-11)](https://www.bleepingcomputer.com/news/security/active-screenconnect-attacks-breach-msps-impact-dozens-of-organizations/) / [The Hacker News (2026-11-12)](https://thehackernews.com/2026/11/sckit-malware-targets-screenconnect.html) / [The Record (2026-11-12)](https://therecord.media/connectwise-screenconnect-breaches-third-party-tool)

### [2026-11-12] GitHub のアカウント 4,837 個を乗っ取り、CI の秘密情報を盗むコードを 1,806 以上のリポジトリで実行させた (「wfx-loot」)
- **何が起きたか**: Aikido によると、攻撃は 11/10 に始まった。まず `wfx-docs` ブランチから `docs: dependency audit notes` という PR を開き、書き込みができるかを試した。試しの PR は 61,764 リポジトリに出され、ステーラーは少なくとも 1,806 リポジトリで実行された。SafeDep は、11/10〜11/12 に悪性のコミットを受けたリポジトリを 8,093 と数えた (うち 7,309 は既存のワークフローの改変、771 は npm の postinstall)。攻撃者はプッシュの数分後に元に戻し、実行ログも消していた。痕跡は、ブランチ `chore/[a-z0-9]{8}` と `ci-check-[0-9]{4}`、コミット `ci: refresh build cache` と `chore: add ci helper`、`.github/workflows/build-audit-xxxxxx.yml`。
- **なぜ重要か**: 自分が書き込めるすべてのリポジトリで、Actions の実行履歴とシークレットの棚卸しが必要になる。npm install をした開発者の端末も対象になる。GMO Flatt Security によると、AI ツールの認証ファイルや OIDC を使ったクラウドの信頼関係の書き換えまで狙っている (国内コミュニティ欄)。
- **悪用 / PoC**: 実際の攻撃。認証情報の入手経路は不明。
- 出典: [Aikido (2026-11-12)](https://www.aikido.dev/blog/compromised-github-accounts-push-ci-secret-stealer-to-tens-of-thousands-of-repositories) / [SafeDep](https://safedep.io/blog/github-actions-wfx-credential-stealer) / [The Hacker News (2026-11-12)](https://thehackernews.com/2026/11/4837-hijacked-github-accounts-ran-ci.html)

### [2026-11-12] Windows のゼロデイ「SignDrop」: CLFS の緩和策そのものを悪用して SYSTEM に昇格する PoC が公開。修正はない
- **何が起きたか**: Abdelhamid Naceri 氏が PoC を公開した。Microsoft は 2025 年 10 月、CLFS の脆弱性の対策として、ログファイルに認証ファイル (`.cnpf`) を付ける緩和策を入れた。CLFS は最初のアクセスチェックを正しく行うが、あとから別の特権プロセス (Defender など) にログファイルを開かせると、認証ファイルが SYSTEM の文脈で、元のファイルのアクセス権のまま作られる。Naceri 氏は、この手法でアンチマルウェア製品のタンパー保護もすり抜けられると主張している。影響の目安は、レジストリの `CLFS\Authentication\Mode` が 0 か 1 であること。緩和策を無効にすると古い CLFS のバグが再び使えるようになるので、回避策はない。
- **なぜ重要か**: 公開された LPE に、EDR を止める手段が付いている。ランサムウェアのオペレーターが組み込むまでの時間は短いと考えられる。
- **悪用 / PoC**: **PoC 公開**。悪用の報告はない。CVE は未採番。
- 出典: [BleepingComputer (2026-11-12)](https://www.bleepingcomputer.com/news/security/new-windows-signdrop-zero-day-gives-hackers-system-privileges/) / [The Hacker News (2026-11-12)](https://thehackernews.com/2026/11/new-signdrop-zero-day-exploit-turns.html)

### [2026-11-11 公表 / 11-12 報道] Red Hat Quay の Critical 2 件: 匿名のトークンで署名鍵を登録し、全リポジトリを読み書きできる (CVE-2026-123710、9.8)。LIKE のワイルドカードで、他テナントの robot トークンを盗める (CVE-2026-110697、9.9)
- **何が起きたか**: 鍵サーバー (`/keys`) は、鍵を差し替えるリクエストのトークンの署名、audience、issuer は確かめるが、「鍵のローテーション用に発行されたトークンか」は確かめない。`/v2/auth` で取れる匿名トークンは信頼された鍵で署名されており、audience を呼び出し側が選べる。そのため攻撃者は、期限のない自分の鍵を登録し、全リポジトリを pull / push できる。もう 1 件は、robot アカウントの一覧で namespace 名から作る LIKE のパターンで `_` をエスケープしておらず、他テナントの復号済みトークンを取れる。Quay 3 / 5 の全バージョンが対象。
- **なぜ重要か**: OpenShift に統合されたレジストリが乗っ取られると、イメージを差し替えて CI/CD に悪性のイメージを流せる。暫定策は、`/keys` をプロキシで内部からだけに絞り、監査ログで期限 (`expiration_date`) が null の `service_key_rotate` を探すこと。
- **悪用 / PoC**: どちらも報告はない。EPSS は 0.0043 / 0.0050。
- 出典: [Red Hat CVE-2026-123710](https://access.redhat.com/security/cve/CVE-2026-123710) / [Red Hat CVE-2026-110697](https://access.redhat.com/security/cve/CVE-2026-110697) / [The Hacker News (2026-11-12)](https://thehackernews.com/2026/11/critical-red-hat-quay-flaw-lets.html)

### [2026-11-12] PostgreSQL 18.7 / 17.12 / 16.16 / 15.20 / 14.25: 52 件の脆弱性を一度に修正。CVSS 8.8 の任意コード実行が多い。PostgreSQL 14 はこれでサポート終了
- **何が起きたか**: サーバー側は、型の取り違え、plperl / pltcl の再入による UAF、`tsvector_delete()` と `ts_rank_cd()` のヒープオーバーフローなどで、多くは「オブジェクトを作れる権限」があれば DB の OS ユーザーとしてコードを実行できる。クライアントのツール側は、pg_dump の制約名による SQL インジェクション (116318)、tar 形式の `\restrict` キーが予測できる問題 (116330。CVE-2025-8714 の修正漏れで、元のサーバーを握った攻撃者が、復元する人の OS でコマンドを実行できる)、reindexdb の SQL インジェクション (116325) など。未認証で 18 系のサーバーを再起動させられる欠陥 (116322) もある。
- **なぜ重要か**: マネージド DB を含め、利用者に CREATE の権限を与えている環境と、外部から受け取ったダンプを復元する運用が当たる。更新後に追加の手順が必要なものがあるので、リリースノートを確かめたい。
- **悪用 / PoC**: 報告はない。EPSS は未算出。
- 出典: [PostgreSQL (2026-11-12)](https://www.postgresql.org/about/news/postgresql-187-1712-1616-1520-1425-and-19-rc-2-released-3442/)

### [2026-11-11] Node.js 22.23.5 / 24.22.3 / 26.13.1: 16 件を修正。HTTPS で他の接続のメモリ (TLS の秘密鍵を含む) が漏れるおそれ (CVE-2026-123864)、TLS 1.2 の再ネゴシエーションで SNI を変えて mTLS の方針を回避 (CVE-2026-123872)
- **何が起きたか**: 123864 は、長さ 0 の書き込みで `TLSWrap::DoWrite()` が `ClearOut()` を直接呼び、on_body の中から呼ばれると `llhttp_execute()` に再入して、UAF と範囲外の読み出しが起きるもの。成立には特定のハンドラーの書き方が必要。123872 は、TLS 1.2 の再ネゴシエーション、HRR、セッション再開のどれでも SNI を変えられ、ホスト名ごとに違うクライアント証明書の方針を回避できるもの。ほかに HTTP/2 の UAF による応答バッファの漏えい (123866) など。5 件は Chris Rohlf 氏が Anthropic Research と協力して報告した。20.x と 25.x は EOL で修正されない。
- **なぜ重要か**: 「再ネゴシエーションや再開で SNI を変えて、ホスト名ごとの認可をすり抜ける」は、ほかの TLS スタックやリバースプロキシでも起きうる型だ (CVE 所感を参照)。
- **悪用 / PoC**: 報告はない。EPSS は 0.0033 / 0.0036。
- 出典: [Node.js (2026-11-11)](https://nodejs.org/en/blog/vulnerability/november-2026-security-releases)

### [2026-11-12] Citrix、NetScaler ADC / Gateway と Secure Access Client の 12 件を修正。NetScaler Console に未認証の認証回避 (CVE-2026-120869、CVSS4 9.3〜9.4)
- **何が起きたか**: ADC / Gateway には、パケット処理 (120868、全構成が対象)、SMPP、DNS / DoH、Gateway / AAA、メール OTP、EPA、ICA プロキシのメモリのオーバーフローや破壊が 9 件ある (主に DoS)。修正版は 14.1-73.57 と 13.1-64.39。NetScaler Console は 14.1-74.34 で 120869 を直した。Secure Access Client には、Windows で SYSTEM、Linux で root への昇格がある。
- **なぜ重要か**: NetScaler は毎年のようにゼロデイとして悪用されている。メモリ破壊系は、あとで RCE に格上げされることが多い。外部に公開している Gateway は優先して更新したい。
- **悪用 / PoC**: 報告はない。
- 出典: [The Hacker News (2026-11-12)](https://thehackernews.com/2026/11/citrix-patches-12-netscaler-and-secure.html) / [Citrix CTX697305](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX697305)

### [2026-11-11] Datadog、MongoDB Server の認証前の UAF (CVE-2026-118383、CVSS4 9.5) を再現。ping を 2 回送るだけで「時限爆弾」を仕掛けられる
- **何が起きたか**: `readConcern.afterOpTime` を付けた ping を 2 回送ると、期限のない waiter が登録される。そのメンバーが遅れた状態で primary に選ばれると、catch-up の後始末で UAF が起きる。ping は認証の前に受け付けるので、認証を有効にしていても防げない。影響は replica set のメンバー (シャード、config サーバーを含む) で、standalone は対象外。修正版は 9.0.7 / 8.3.16 / 8.0.37 / 7.0.48 など (修正と NVD の公開は 11/10)。
- **なぜ重要か**: 認証の前に届く欠陥なので、27017 番ポートを外部や広いセグメントに出している環境が当たる。診断では、replica set のメンバーがどこから届くかを確かめたい。
- **悪用 / PoC**: 悪用の報告はない。**クラッシュの PoC が公開済み**。EPSS 0.0071。
- 出典: [Datadog Security Labs (2026-11-11)](https://securitylabs.datadoghq.com/articles/cve-2026-118383-mongodb-server-use-after-free/)

### [2026-11-11 公開 / 11-12 報道] PTC Windchill / FlexPLM に、デシリアライズによる Critical の RCE (CVE-2026-126325、CVSS4 9.2)
- **何が起きたか**: Windchill 11.0 M030〜13.1.4.0 と FlexPLM 11.0 M030〜13.1.3.0 が影響を受ける。PTC がホストしている環境には適用済み。約 5 か月前の CVE-2026-12569 は実際に悪用され、7 月には Cl0p 系が JSP の Web シェルを置いてデータを盗んだ。
- **なぜ重要か**: 製造業の設計データを持つ PLM は、データを盗んで脅す型の攻撃者に狙われ続けている。国内の製造業でも使われているので、外部公開の有無を確かめたい。
- **悪用 / PoC**: 報告はない。EPSS 0.0051。
- 出典: [The Hacker News (2026-11-12)](https://thehackernews.com/2026/11/ptc-patches-critical-windchill-and.html) / [PTC](https://www.ptc.com/en/about/trust-center/advisory-center/active-advisories/windchill-flexplm-rce-vulnerability)

### [2026-11-11] Microsoft: 正規のリモートアクセスツール GSocket を、パッチの後も Linux サーバーに残る足場として使う攻撃が、3〜8 月に 356% 増えた
- **何が起きたか**: GSocket は、侵害したホストと攻撃者の両方が外向きに中継網へつなぐので、待ち受けのポートも攻撃者の IP も要らない。検知の 87.1% は Web アプリとホスティングで、PHP / cPanel が 63.9%、Apache が 24.3%。カーネルスレッドを装い、cron、systemd、シェルの起動ファイルで永続化する。権限昇格に Dirty Frag (CVE-2026-43284) を試した例もある。
- **なぜ重要か**: 入口の脆弱性を直しても、この足場は残る。侵害の後の調査では、外向きの通信と、`gs-netcat` のような名前の永続化の痕跡を確かめたい。
- 出典: [Microsoft Security Blog (2026-11-11)](https://www.microsoft.com/en-us/security/blog/2026/11/11/global-socket-how-threat-actors-weaponizing-gsocket-stealthy-c2/)

### [2026-11-12] Operation Endgame の新しい段階: Gootloader、CastleRAT、StealC の基盤を摘発。サーバー 235 台、ドメイン 257 個を押収し、被害者のデータ 640 万件を確認
- **何が起きたか**: Europol と Eurojust が調整し、ブルガリア、カナダ、デンマーク、ドイツ、モルドバ、オランダ、ポーランド、英国、米国が参加した。被害者のデータは、HIBP、DIVD、Shadowserver、NL-NCSC などを通じて通知される。StealC の摘発は今年 2 回目 (The Record)。
- **なぜ重要か**: インフォスティーラーで盗まれた認証情報は、初期侵入の主な材料になっている。HIBP や Shadowserver からの通知が届いたら、該当するアカウントのセッションの失効まで行いたい。
- 出典: [BleepingComputer (2026-11-12)](https://www.bleepingcomputer.com/news/security/police-dismantles-gootloader-castlerat-stealc-malware-infrastructure/) / [The Record (2026-11-12)](https://therecord.media/european-authorities-take-down-stealic-malware-second-time)

### [2026-11-12] Google Calendar の招待を入口に、リバースプロキシで Google のセッションを盗む「Operation CloudFire」(Material Security)
- **何が起きたか**: Material Security によると、カレンダーの招待から、Google の `/url` リダイレクタ、share.google、Cloudflare Turnstile を経て、リバースプロキシ (Nyasher) に誘導する。パスワードの入力画面は、ブラウザの中の JavaScript で組み立てる。SMS、TOTP、番号を照合するプッシュ承認のどれでも、セッションの奪取は防げないという。
- **なぜ重要か**: メールのリンクの検査をすり抜けるカレンダーの招待と、Google 自身のドメインを経由する誘導の組み合わせだ。フィッシングの訓練や検知のルールで、カレンダー経由の経路も扱いたい。パスキーなどフィッシングに強い認証への移行を進める根拠になる。(ベンダーの寄稿の色が強い記事)
- 出典: [The Hacker News (2026-11-12)](https://thehackernews.com/2026/11/calendar-invites-and-live-proxies.html)

### [2026-11-12] ブラウザとクラウドの CPU: Chrome 157 は 83 件 (Critical の UAF 5 件)、Firefox 160 は 99 件を修正。AMD Turin で TSA の新しい亜種 (TSA-Fill)
- **何が起きたか**: Chrome 157.0.8103.78/.79 では、Anthropic と OpenAI の研究者が 18 件を報告した。Firefox 160 は High が 57 件で、ESR 153.7 / 115.45 も更新された。どちらも悪用の記載はない。AMD は Turin (Zen 5) で TSA の 3 件を公表し、新しい TSA-Fill (CVE-2026-0004) のほか、「Zen 5 は影響しない」としていた TSA-SQ / TSA-L1 の説明を訂正した。Google Cloud は、C4D などのインスタンスで、ゲスト OS のパッチと VM の stop/start を求めている (再起動では足りない)。
- **なぜ重要か**: AI による脆弱性発見の報告が、ブラウザの定例の修正の中で目立つ割合になってきた。クラウドの利用者は、AMD のインスタンスの stop/start を計画しておきたい。
- 出典: [SecurityWeek (2026-11-12)](https://www.securityweek.com/chrome-firefox-updates-patch-180-vulnerabilities/) / [The Hacker News (2026-11-12)](https://thehackernews.com/2026/11/google-cloud-warns-three-amd-turin-cpu.html)

### [2026-11-11] 会計事務所の Baker Tilly、外部の委託先のプラットフォームで顧客情報が漏れたと通知。テキサス州だけで 10,456 人、SSN を含む
- **何が起きたか**: Baker Tilly は、外部の委託先のプラットフォームで顧客の情報が漏れたと顧客に通知した。テキサス州の司法長官への届け出では 10,456 人で、社会保障番号を含む。
- **なぜ重要か**: 国内のオープンロジやアララと同じく、委託先 1 社の侵害が多数の利用者に波及する型だ。会計・税務の事務所は、多数の企業の財務情報を持つ委託先として扱うべきだ。
- 出典: [BleepingComputer (2026-11-11)](https://www.bleepingcomputer.com/news/security/baker-tilly-notifies-clients-of-data-breach-at-third-party-provider/)

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-11-11 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先
> CISA KEV は catalogVersion 2026.11.10 のままで、11/11 以降の追加はない。

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-119618 | Apache HTTP Server 2.4.55〜2.4.70 / mod_h2 2.0.8〜2.0.42 | CWE-362 / Critical (Red Hat 9.8) | HTTP/2 のストリームを並行処理するとき、`assign_headers()` が共有のヘッダー構造を同期なしに更新 → ヒープ破壊 → 未認証で RCE のおそれ (h2 有効時) | [824beab](https://github.com/apache/httpd/commit/824beab9b9424d6cfb29595248fdbf6c3dddeab1) | クラッシュの PoC 公開 / EPSS 0.0040 |
| CVE-2026-123710 | Red Hat Quay 3.x / 5.x 全版 | CWE-1287 / 9.8 | 鍵のローテーション API がトークンの署名・aud・iss だけを確かめ、発行の目的を確かめない → aud を選べる匿名トークンで期限なしの署名鍵を登録 → 全リポジトリの pull / push | [advisory](https://access.redhat.com/security/cve/CVE-2026-123710) (commit 不明) | EPSS 0.0043 |
| CVE-2026-110697 | Red Hat Quay 3.x / 5.x 全版 | CWE-89 / 9.9 | 利用者が付けた namespace 名をエスケープせずに SQL の `LIKE` に入れる (`_` がワイルドカード) → 他テナントの robot アカウントに一致 → 復号済みトークンを取得 | [advisory](https://access.redhat.com/security/cve/CVE-2026-110697) (commit 不明) | EPSS 0.0050 |
| CVE-2026-126539 / GHSA-97xr-jchp-xm3c | Directus < 12.1.0 | CWE-636 / 8.1 (CVSS4 9.2) | public モードの WebSocket で無効なトークンを送ると、`handleAuthRequest` が accountability を null にし、それが「チェック対象外」と扱われる → 権限チェックを飛ばす (fail-open) → 未認証で任意のコレクションを CRUD | [8d4cd86](https://github.com/directus/directus/commit/8d4cd86783bcbf5444eaf290e8dcecb33929300e) | EPSS 0.0046 |
| CVE-2026-123872 | Node.js 22.x / 24.x / 26.x (修正 22.23.5 / 24.22.3 / 26.13.1) | CWE-287 / High | ホスト名ごとに違う mTLS の方針を置いた TLS サーバーで、再ネゴシエーション・HRR・セッション再開での SNI の変更を拒否しない → 緩いホストで認証したまま厳しいホストへ → クライアント証明書の方針を回避 | [e750e1f](https://github.com/nodejs/node/commit/e750e1fa02) / [97b1357](https://github.com/nodejs/node/commit/97b1357f08) / [a8d6286](https://github.com/nodejs/node/commit/a8d6286949) | EPSS 0.0036 |
| CVE-2026-123864 | Node.js 22.x / 24.x / 26.x | CWE-416 / High | 長さ 0 の TLS の書き込みで `ClearOut()` が直接呼ばれ、on_body の中から次のレコードを復号して `llhttp_execute()` に再入 → UAF と範囲外の読み出し → 他の接続のヒープ (TLS 鍵を含む) が応答に混ざる | [940cae5](https://github.com/nodejs/node/commit/940cae5c33) | EPSS 0.0033 |
| CVE-2026-116330 | PostgreSQL < 18.7 / 17.12 / 16.16 / 15.20 / 14.25 (pg_dump の tar 形式) | CWE-829 / 8.8 | tar 内の `restore.sql` の `\restrict` キーが予測できる → 侵害された元のサーバーが psql のメタコマンドを差し込む → 復元した人の OS でコマンド実行 (CVE-2025-8714 の修正漏れ) | [17e57d0](https://git.postgresql.org/gitweb/?p=postgresql.git;a=commit;h=17e57d06cd3a3966143502626a2f5c7534f8309c) (CVE との対応はコミット名からの推定) | EPSS 未算出 |
| CVE-2026-116318 / CVE-2026-116325 | PostgreSQL 18 < 18.7 (pg_dump) / 17〜18 (reindexdb) | CWE-89 / 8.8・8.0 | カタログから読んだ識別子 (NOT NULL 制約名 / インデックス名) を引用符なしでダンプやクエリに埋め込む → 識別子による SQL インジェクション → 復元する人・実行する人の権限で任意の SQL | [9e4cde7](https://git.postgresql.org/gitweb/?p=postgresql.git;a=commit;h=9e4cde7927da3603a2b6ca0d4e75d50b28888252) / [aac5e6f](https://git.postgresql.org/gitweb/?p=postgresql.git;a=commit;h=aac5e6f5038a4d3b9a6d71b30e57fd9c9436033c) (推定を含む) | EPSS 未算出 |
| CVE-2026-116315 (+ 116317) | PostgreSQL 各系列 | CWE-122 / 8.8 | `tsvector_delete()` / `ts_rank_cd()` で、利用者が渡した tsvector の要素数や位置を確かめない → ヒープの範囲外への書き込み → DB の OS ユーザーとしてコード実行 | [9c2cada](https://git.postgresql.org/gitweb/?p=postgresql.git;a=commit;h=9c2cadacd61562ba7835179209c2aa9482f61d48) / [3e97c9a](https://git.postgresql.org/gitweb/?p=postgresql.git;a=commit;h=3e97c9a1fa19fb995e57a1a093cb7cee3f6da605) (推定を含む) | EPSS 未算出 |
| CVE-2026-97033〜97043 (GO-2026-6848〜6858) | Go toolchain < 1.26.11 / 1.27.0〜1.27.3 (cmd/go、cgo、link) | 未付与 / 未採点 | `#cgo` の CFLAGS / LDFLAGS、pkg-config、`.syso` などのフラグの許可リストに抜け (`--sysroot`、`-target`、`-g*` のワイルドカードの一致、分割した `-Wl,`、GCC の spec ファイル) → 危険なフラグがコンパイラ・リンカーに届く → 悪意あるパッケージを `go build` しただけでコード実行 | [CL 862146](https://go.dev/cl/862146) 〜 [CL 862156](https://go.dev/cl/862156) | EPSS 0.0025 |
| CVE-2026-126196 / GHSA-j7mp-839j-jrm7 (+ 126198 / 126199) | pgEdge Postgres MCP Server < 1.1.0 | CWE-863 系 / 8.1 (6.8 / 3.1) | 読み取り専用の接続で、認識できない文をパラメーターなしで pgx Exec に送る (複数の文が通る) / 書き込み確認を先頭キーワードで判定 → トランザクション状態の変更、更新系 CTE の素通り → 読み取り専用の MCP から DB に書き込み (プロンプトインジェクション経由も可) | [advisory](https://github.com/pgEdge/pgedge-postgres-mcp/security/advisories/GHSA-j7mp-839j-jrm7) (commit 不明) | EPSS 未算出 |
| CVE-2026-125926 | Amazon mcp-gateway-registry < 1.35.0 | CWE-918 / 8.5 | サーバーの登録・更新の API が、利用者の指定した URL に宛先の制限なしでリクエスト → SSRF → 内部サービスや IMDS の応答を読む | [AWS bulletin](https://aws.amazon.com/security/security-bulletins/2026-180-aws/) (commit 不明) | EPSS 未算出 |
| CVE-2026-126799 / GHSA-fqg9-x2xw-5crx | Gotenberg 8.31.0〜< 8.38.0 | CWE-918 / 7.5 | `IsPublicIP()` が IPv6 のゾーン ID (`%25eth0`) の付いたアドレスを正しく判定しない → 未指定アドレスや拒否対象のプレフィックスが通る → SSRF で内部サービスの応答を PDF で読み出す | [8e850b1](https://github.com/gotenberg/gotenberg/commit/8e850b1c932452627fba397f2005dd6fd57b9617) | EPSS 0.0042 |
| CVE-2026-126837 | MongoDB Node.js ドライバー (`mongodb+srv://`) | CWE-180 / 7.4 (CVSS4 9.1) | SRV 応答のホスト名を「接続文字列のドメインの配下か」で検査したあと、正規化の前の元の文字列から接続先を組み立てる → 検査と実際に使う値がずれる → DNS を偽装すれば任意のホストに接続し、TLS の検証もそのホスト名で通る | [NODE-7830](https://jira.mongodb.org/browse/NODE-7830) (commit 不明) | EPSS 未算出 |
| CVE-2026-64855 / GHSA-859w-52fx-hcm6 | soapbar (Python) < 0.13.0 | CWE-295・347 / 8.2 | `verify_envelope_bsp()` が、検証するメッセージ自身の `wsse:BinarySecurityToken` の証明書を信頼の起点にする (CA チェーン、許可リスト、ピン留めのどれもない) → 自己署名の証明書で署名した偽の封筒が通る → なりすまし | [PR #71](https://github.com/hitoshyamamoto/soapbar/pull/71) (commit ハッシュ不明) | EPSS 0.0019 |
| CVE-2026-127063 | ScreenConnect 用のサードパーティ拡張 RMM+ | CWE-1392 / CVSS4 9.3 | 既定の API シークレットが固定値 → 拡張の API の認証を通る → 管理下のエージェントにコマンドを送る | [ConnectWise Disclosures](https://github.com/ConnectWise-Advisories/Disclosures/tree/main/CVE-2026-127063) (commit 不明、クローズドソース) | 悪用中のキャンペーンとの関連が疑われる |

### 今日の CVE 所感

- **他の実装に広がりやすい型が多い日だった**。(1) Node.js の「再ネゴシエーション、HRR、セッション再開で SNI を変えて、ホスト名ごとの mTLS をすり抜ける」は、nginx や Envoy の SNI ごとの mTLS 設定、Go の `GetConfigForClient`、Java の SNIMatcher でも同じ前提が崩れていないかを見る価値がある。(2) MongoDB ドライバーの「SRV の検査に使う値と、実際に接続に使う値のずれ」は、仕様が共通なので、ほかの言語のドライバーにも同じ形がありうる。
- **「検証の起点を間違える」型が 3 件あった**。Quay (トークンの発行目的を見ない)、soapbar (メッセージの中の証明書を信頼の起点にする)、Directus (null の accountability を「チェック対象外」と扱う fail-open) だ。どれも、diff を読めば 1 行で直せる種類の欠陥で、同じ種類の自前の認可コードを grep で探しやすい。
- **SSRF の対策を回避する型**: Gotenberg の IPv6 ゾーン ID と、MCP ゲートウェイの URL の受け取り。`IsPublicIP` 相当の自前の判定関数は、`%25` を含む IPv6、IPv4-mapped、10 進表記をまとめてテストしたい。
- **ビルド時のフラグの許可リスト** (Go の 11 件) は、Rust の build.rs、node-gyp、Python のビルドバックエンドにも同じ考え方がある。「依存を取ってビルドしただけで実行される」経路は、wfx-loot のような CI 攻撃とも直結する。
- 診断で優先して見るなら、HTTP/2 を有効にした Apache httpd、外部公開の Quay と NetScaler、利用者に CREATE を与えている PostgreSQL、SQL を扱う MCP サーバーの順になる。

## 日本国内のセキュリティ動向

### 国内インシデント・事故

#### [2026-11-11] SMBC 日興証券: 受託している「持株会管理システム」に不正アクセス。最大 56,487 人分の氏名、住所、持分残高、振替先口座が漏えい
- **何が起きたか**: SMBC 日興証券は 11/11、持株会の事務受託で使っているシステムが不正アクセスを受け、会員の個人情報が外部に漏れたことを確認したと発表した。11/9 に不正アクセスを確認し、同日中にシステムを遮断した。対象の項目は、持株会名、投資銘柄、会員識別番号、氏名、住所、配当金と諸税、持分残高、振替先口座。対象は最大 56,487 人。電話番号とメールアドレスは登録がないため対象外。侵入経路は公表されておらず、システムの再開は未定。
- **なぜ重要か (評価)**: 持株会のシステムは、多数の上場企業の従業員の資産と口座をまとめて持つ、委託型の共通基盤だ。氏名、住所、勤務先 (持株会名)、口座が一緒に出たので、郵送や電話でのなりすましに使える。証券会社の周辺業務のシステム (持株会、IR、株主管理) は、本体に比べて診断の対象から漏れやすい。
- 出典: [SMBC 日興証券 (2026-11-11, PDF)](https://www.smbcnikko.co.jp/news/release/2026/pdf/261111_01.pdf)

#### [2026-11-11] オープンロジ (EC 物流プラットフォーム): 11/8〜9 の不正アクセスで出荷データを持ち出される。4/8〜11/8 の依頼分のお届け先 (氏名、住所、電話、メール、商品) が対象。委託元の公表が続く
- **何が起きたか**: オープンロジは 11/11、11/8 から 11/9 にかけて自社システムが不正アクセスを受け、出荷データの一部が外部に持ち出されたと発表した。対象は、2026/4/8〜11/8 に依頼を受けた出荷データのお届け先の氏名、住所、電話番号、メールアドレス (登録がある場合) と、商品名・数量。件数は調査中。カード番号は持っていない。11/9 に把握している経路を遮断した。委託元では、テレビ東京 (エンしゃべストアなど) と HUMAN MADE が 11/11、ENSAPIA Tokyo が 11/12 に公表した。
- **なぜ重要か (評価)**: 7 か月分のお届け先 (贈り物の受取人を含む) と商品名が一緒に漏れた。「ご注文の商品について」型の偽の配送通知や返金詐欺に、そのまま使える。物流の SaaS は多くの EC 事業者の出荷データを横断して持つので、委託先 1 社から数百社に被害が広がるおそれがある。
- 出典: [オープンロジ (2026-11-11)](https://corp.openlogi.com/news/notice/notice-20261111/) / [テレビ東京 (2026-11-11, PDF)](https://www.tv-tokyo.co.jp/kaisha/pdf/20261111.pdf) / [HUMAN MADE (2026-11-11, TDnet)](https://www.release.tdnet.info/inbs/140120261111574117.pdf) / [ENSAPIA Tokyo (2026-11-12)](https://ensapia-tokyo.com/news/topics/id=21395/)

#### [2026-11-11] 電通デジタル「TONARIWA」(LINE 連携のマーケティング基盤): 漏れた管理アカウントの認証情報で侵入され、権限昇格も。LINE 公式アカウントの連携トークンも漏えいのおそれ。日本郵便「ぽすくま」が停止
- **何が起きたか**: 電通デジタルは 11/11、TONARIWA の基盤の管理アカウントが、認証情報の漏えいをきっかけに不正アクセスを受け、権限昇格まで行われたことを 11/10 に確認したと発表した。サービスは止めている。漏えいのおそれがあるのは、一部の顧客企業のエンドユーザーの氏名、生年月日、連絡先などと、LINE 公式アカウントと連携するためのアクセストークンなど。同社は、第三者が LINE 公式アカウントから不正なメッセージを送るリスクを排除できないとしている。日本郵便は 11/11、TONARIWA を使っていた LINE アカウント「郵便局[ぽすくま]」の機能を緊急メンテナンスで止めた。
- **なぜ重要か (評価)**: 漏れたのが個人情報だけでなく、企業の公式 LINE アカウントから配信できるトークンも含む点が重い。郵便局のような公式アカウントから偽のメッセージが来れば、利用者は見分けられない。LINE 連携の SaaS の診断では、チャネルアクセストークンの保管 (暗号化、範囲、ローテーション) と、管理アカウントの MFA を確認したい。
- 出典: [電通デジタル (2026-11-11)](https://www.dentsudigital.co.jp/news/updates/services/2026-1111-001111) / [日本郵便 (2026-11-11)](https://www.post.japanpost.jp/newsrelease/pressrelease/685401036.html)

#### [2026-11-12] サイバーセキュリティクラウド (WAF / MSS ベンダー): 従業員の GitHub の認証情報 1 件が流出し、第三者のアクセスを確認。リポジトリにあった顧客の情報が漏えいしたおそれ
- **何が起きたか**: サイバーセキュリティクラウドは 11/12、GitHub で不審なアクセスを確認したと発表した (第一報)。外部からの情報提供で、従業員が業務で使っていた GitHub の認証情報 1 件の流出がわかり、それを使った第三者とみられるアクセスを 11/5 に確認した。ログの保存期間の制約で、認証情報が有効だった期間全体は確認できていない。漏えいのおそれがあるのは、一部の顧客の情報 (企業名、氏名、メールアドレスなど) と「サービス利用に伴う通信関連情報」。GitHub にあった他サービスの認証情報も変更した。サービスへの不正アクセスは確認していないとしている。
- **なぜ重要か (評価)**: セキュリティベンダー自身が、リポジトリに顧客の情報と他サービスの認証情報を置いていた。GitHub の監査ログは保存期間が短く、後からたどれないこともわかった。開発組織の診断では、リポジトリ内のシークレットと顧客データのスキャン、PAT の期限と範囲、監査ログの外部への転送を確かめたい。時期は wfx-loot と重なるが、同社は関連に触れていない。
- 出典: [サイバーセキュリティクラウド (2026-11-12)](https://www.cscloud.co.jp/news/info/20261112-2/)

#### [2026-11-09〜11 公表 / 11-12 piyolog] ブランジスタソリューション「まとまるEC店長」: サーバーに注文情報を照会する不審なスクリプト。373 社、注文 21,873 件。本物の注文情報を使った偽の返金メールで LINE に誘導
- **何が起きたか**: ブランジスタソリューションは 11/9 に第一報、11/10 に第二報を出した。きっかけは、利用店舗から「本物の注文情報が書かれた不審な返金メールが購入者に届いている」という問い合わせだった。piyolog のまとめ (11/12) によると、不正アクセスは 11/1 と 11/6 の 2 回で、重複を除いて注文 21,873 件、対象は 373 社。偽メールは「品切れのため返金」を装って LINE に誘導し、Yahoo!ショッピングと Qoo10 の注文で確認されている。提供元は DB のパスワードを変え、楽天市場との API 連携を一時止めた。侵入経路は調査中。利用店舗の清川屋も 11/11 に公表した。
- **なぜ重要か (評価)**: 漏れた注文情報が、数日のうちに本物そっくりの詐欺メールに使われた。モールの一元管理 SaaS は、複数のモールの API キーと注文 DB を 1 か所に集めるので、攻撃者にとって効率がよい。診断では、Web サーバーのファイル改ざんの検知と、DB の認証情報を Web 層に置かない設計を確認したい。
- 出典: [piyolog (2026-11-12)](https://piyolog.hatenadiary.jp/entry/2026/11/12/113829)

#### [2026-11-11] FABRIC TOKYO (オーダースーツ): 外部委託先から流出したとみられるアクセスキーで検証用システムに侵入され、2021 年 5〜7 月の予約データ 699 人分が取得された可能性
- **何が起きたか**: FABRIC TOKYO は 11/11、検証用システムに一時的に保管していた 2021 年 5〜7 月の予約データ 699 人分 (名前、メールアドレス、電話番号など) が、閲覧・取得された可能性があると発表した。原因は、外部委託先から流出した可能性が高いアクセスキーとしている。11/2 に発覚し、個人情報保護委員会に報告した。(公式ページは調査環境から取得できず、内容は一次情報の要約サイトで確認した)
- **なぜ重要か (評価)**: 委託先の手元にあった長期有効のアクセスキーで、検証環境に残った古い本番データが取られる型だ。11/10 公表のトレードワルツやアイルと同じ構図が続いている。クラウドの診断では、検証環境に本番データが残っていないか、IAM のアクセスキーの最終使用日とローテーションを確認したい。
- 出典: [FABRIC TOKYO (2026-11-11)](https://fabric-tokyo.com/news/show/20261111-to-all-customers) / [セキュリコ](https://incidents.seory.co.jp/incidents/20261111-5a31d6/)

#### [2026-11-11] [続報] Notion AI のチャット記録の流出 (Fireworks AI 経由): 国内企業が影響を公表。SecureNavi、LRM、フェイガー
- **前回から何が変わったか**: 11/12 号は通知の時系列までだった。11/11 に、国内の利用企業が自社の影響を公表し始めた。SecureNavi は顧客企業名、担当者名、相談や打ち合わせの内容が含まれた可能性があるとした。LRM は 10/5〜24 に作ったチャット記録の一部、フェイガーは取引先の担当者名などとした。3 社とも詳細は確認中。
- **なぜ重要か (評価)**: 3 社のうち 2 社はセキュリティ事業者で、顧客との相談の記録が含まれる。標的型のフィッシングの材料になる危険が高い。SaaS の AI 機能の評価では、ZDR の対象外の機能 (履歴、分析、Insights) と、サブプロセッサーの一覧を確かめたい。
- 出典: [ITmedia AI+ (2026-11-12)](https://www.itmedia.co.jp/aiplus/article/2611/12/2000003140/) / [piyolog (2026-11-11)](https://piyolog.hatenadiary.jp/entry/2026/11/11/125745)

#### [2026-11-11] Cocolive (不動産向け MA「KASIKA」、東証グロース): 一部の Web サーバーに不審なアクセスの痕跡。DB への侵入や持ち出しは確認していない
- **何が起きたか**: Cocolive は 11/11 の適時開示 (第一報) で、KASIKA が使う一部の Web サーバーへの不審なアクセスの痕跡を、11/7 に監視で検知したと発表した。サーバーを遮断・隔離し、ほかのサーバーも点検した。データベースへの侵入や、顧客情報・閲覧履歴の持ち出しは確認していない。外部の専門機関が調査している。
- **なぜ重要か (評価)**: 不動産会社の見込み客の行動履歴を持つ MA の SaaS だ。件数はまだ出ていないので、続報に注意したい。
- 出典: [Cocolive (2026-11-11, TDnet)](https://www.release.tdnet.info/inbs/140120261111573847.pdf)

#### [2026-11-11〜12] [続報] 宝くじ公式サイトは「リスト型攻撃」の可能性。良品計画は会見で「2021 年までカード番号を顧客の識別に使っていた」と説明
- **前回から何が変わったか**:
  - 宝くじ (11/11): 販売元の自治体は、第三者が一部の会員のアカウントに不正にログインした可能性があると発表した。原因はリスト型攻撃の可能性で、当落の履歴、当せん金の受取口座 (口座番号の上 4 桁)、カード番号の下 4 桁まで閲覧された可能性がある。件数は非公表で、受取口座の書き換えは確認していない。
  - 良品計画 (11/12): 記者会見で、2021 年 7 月まで MUJI Card のカード番号を顧客の識別に使い、その後も削除せず、マスキングも暗号化もしていなかったと説明した。割賦販売法に抵触するかは「確認中」。カード情報へのアクセスにつながった攻撃は、リスト型攻撃とは別の手口だという。
- **なぜ重要か (評価)**: どちらも、ログイン後に金銭や機微な情報に届く設計の甘さが問われている。受取口座のような画面には再認証と変更の通知が要る。データの棚卸しでは、本来の用途を終えた列 (識別子に使われた機微な情報) が DB に残っていないかを確かめたい。
- 出典: [ITmedia NEWS 宝くじ (2026-11-12)](https://www.itmedia.co.jp/news/article/2611/12/2000003158/) / [ITmedia NEWS 良品計画 (2026-11-12)](https://www.itmedia.co.jp/news/article/2611/12/2000003144/)

#### [2026-11-10〜11] [続報] 住友生命 Vitality への不正アクセス (NTT データの受託分) が自治体のイベントに波及: 東京都で 475 人分、岡山県で 25 人分
- **前回から何が変わったか**: 東京都は、住友生命と連携した「東京グリーンビズウォーク」で、専用アプリに登録した約 3 万 8 千人のうち 475 人分の氏名、生年月日、電話番号、メールアドレス、会員番号が漏えいしたと発表した (都庁総合ホームページへの掲載は 11/11)。岡山県も「おかやま Vitality ウォーク」の 25 人分の漏えいを公表した。
- **なぜ重要か (評価)**: 自治体が民間アプリを使う連携イベントでも、参加者の情報は委託先の侵害の影響を受ける。自治体側で、再委託先まで把握できているかが問われる。
- 出典: [東京都 (2026-11-11)](https://www.metro.tokyo.lg.jp/information/press/2026/11/2026111101)

#### [2026-11-11] NTT ドコモ「5G SA」で再び全国障害 (約 9 時間)。原因は 11/5 と同じ交換機の輻輳で、攻撃の形跡はないと説明
- **何が起きたか**: ドコモは、11/11 10:34〜19:17 に、全国の 5G SA の契約者で音声、データ、SMS が使いにくくなったと発表した。原因は 5G SA の契約者を収容する交換機の輻輳で、11/5 (約 14 時間) と同じ。不正アクセスやサイバー攻撃を示す事象は確認していない。4G、5G NSA、MVNO には影響がなかった。
- **なぜ重要か (評価)**: セキュリティ事案ではないが、同じ原因の障害が 1 週間で 2 回起きた。可用性のインシデントとして記録しておく。
- 出典: [ITmedia NEWS (2026-11-12)](https://www.itmedia.co.jp/news/article/2611/12/2000003125/)

### 国内の注意喚起・ガイドライン・政策

#### [2026-11-11〜12] [続報] 「警察庁推奨アプリ」の偽サイト: 警察庁と NTT タウンページが自ら注意喚起し、警視庁も続いた。piyolog が検体を解析し、IoC を公開
- **前回から何が変わったか**: 前号はトビラシステムズの注意喚起を取り上げた。その後、警察庁が 11/11 に公式 X で、NTT タウンページが同日に公式サイトで注意を呼びかけた。偽サイトが装ったのは「詐欺対策 by NTTタウンページ」。警視庁サイバーセキュリティ対策本部も 11/12 に続いた。警察庁は、10 月末以降に少なくとも数百件の不審なメッセージを確認している。
- **piyolog の解析 (11/12)**: 元の APK は、Google Play を装った「更新」画面を自分で表示し、中の暗号化データを AES-GCM と GZIP で戻して別の APK を作り、インストールさせる。追加の APK には、キー入力の記録、アクセシビリティ経由の画面撮影、WebSocket での C2 接続、画面ロックの入力を促す日本語の文言があった。SHA-256 などの IoC も載っている。
- **なぜ重要か (評価)**: 「警察が勧める詐欺対策アプリ」という信頼をそのまま使った誘導だ。モバイルの診断や EDR の検知ルールに、piyolog の IoC をそのまま使える。
- 出典: [piyolog (2026-11-12)](https://piyolog.hatenadiary.jp/entry/2026/11/12/151939)

#### [2026-11-11] JPCERT/CC Weekly Report (11/1〜7 分): Airbyte の任意のコード実行は「悪用を確認」、Barracuda はエクスプロイトの公開を確認
- **何が起きたか**: JPCERT/CC は 11/11 号の Weekly Report で 14 件を取り上げた。Airbyte (JVN#12040144) は悪用を確認したと明記した。Barracuda の事前認証の認可回避とコマンドインジェクションは、エクスプロイトコードの公開を確認し、管理インターフェースを信頼できるネットワークに限るよう勧めた。ほかに Zyxel GS1900 (CVE-2026-107441)、XenServer、ManageEngine、pgAdmin などを扱い、国家サイバー統括室 (NCO) の 11/5 の注意喚起 (Web サイトとモバイルアプリの基本的な対策) も紹介している。
- **なぜ重要か (評価)**: 個々の件はほぼ既報だ。ただ、国内の調整機関が Airbyte の悪用を確認したと明記したので、データ連携の基盤 (Airbyte の self-managed 版) を外部診断で優先する根拠になる。
- 出典: [JPCERT/CC Weekly Report 2026-11-11 号](https://www.jpcert.or.jp/wr/2026/wr261111.html)

> 11/11〜13 に、NCO、警察庁 (本庁の Web サイト)、IPA、総務省、経産省、金融庁、個人情報保護委員会からの新しいサイバー関連の発表は確認できなかった (各機関の新着ページと検索で確認)。IPA と JPCERT/CC の 11 月の Microsoft 更新の注意喚起は 11/12 号で掲載済み。

### 国内製品の脆弱性 (JVN)

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| 2026-11-12 | JVN#64740097 / CVE-2026-101107 | Airターミナル6 v1.01.80 以前 / ソフトバンク | Web 管理画面にログインできるユーザーが OS コマンドを注入し、任意のコマンドを実行できる。修正済みのファームウェアは自動で配信済み | v4 8.6 / v3 8.0 (AV:A/PR:L) | [JVN](https://jvn.jp/jp/JVN64740097/) |
| 2026-11-12 | JVNVU#90805396 / CVE-2026-119618、CVE-2026-106023、CVE-2026-109163 | Apache HTTP Server 2.4.70 以前 / Apache Software Foundation | 2.4.71 で 3 件を修正。mod_http2 の競合によるヒープ破壊 (RCE のおそれ)、mod_md の NULL 参照、mod_vhost_alias の 1 バイトのスタック書き込み | Critical / Important / Low | [JVN](https://jvn.jp/vu/JVNVU90805396/) |
| 2026-11-12 (更新。初出 2026-03-10) | JVNVU#95523788 / CVE-2025-2399 | 三菱電機 CNC (M800V/M80V、M800/M80/E80、C80、M700V/M70V/E70 シリーズ) | TCP 683 番ポートへの不正なパケットで領域外を読み出し、非常停止 (DoS) に至る。11/12 に「影響を受けるシステム」を更新 | DoS (CWE-1285) | [JVN](https://jvn.jp/vu/JVNVU95523788/) |
| 2026-11-12 (更新。初出 2026-10-26) | JVNVU#97400824 [続報] / CVE-2026-111497 | Brotli (C 実装) を同梱する製品 / トレンドマイクロのステータスを更新 | 細工した圧縮データで境界外に書き込み、RCE に至る (「Node2Shell / HTTP2Shell」)。11/12 にトレンドマイクロのベンダーステータスが追加された | RCE (既出) | [JVN](https://jvn.jp/vu/JVNVU97400824/) |
| 2026-11-12 (更新) | JVNVU#92635551 [続報] | KUSANAGI / GMO プライム・ストラテジー | Nginx のリダイレクトルールの CRLF インジェクション。11/12 に「影響を受けるシステム」を更新 (内容は 11/9 版から大きく変わっていない) | v3.1 6.1 | [JVN](https://jvn.jp/vu/JVNVU92635551/) |
| 2026-11-12 (JVN iPedia) | JVNDB-2026-043090〜043156 (CVE-2026-101809、91222、91250、91251 ほか) | Oracle (Workflow、SOA Suite、BPM Suite ほか) / IBM i | Oracle の定例パッチの分を iPedia にまとめて登録。Oracle Workflow のアクセス制御 (CVE-2026-101809) は 10.0、SOA Suite と BPM Suite は 9.9 | 最大 v3 10.0 | [JVN iPedia RSS](https://jvndb.jvn.jp/rss/ja/jvndb_new.rdf) |
| 2026-11-11 (JVN iPedia) | JVNDB-2026-043070〜043074 (CVE-2026-102238、102940、101214) | VS Code (パストラバーサル)、OpenEMR (認証回避)、Dell OpenManage Enterprise (OS コマンドインジェクション) | iPedia に登録された海外製品のうち、深刻度の高いもの | v3 9.6 / 9.6 / 7.2 | [JVN iPedia RSS](https://jvndb.jvn.jp/rss/ja/jvndb_new.rdf) |

> 11/11〜13 に JVN で新しく公開された国内ベンダーの製品は、Airターミナル6 の 1 件だけだった。11/11 公開分 (Movable Type、Sleipnir Mobile など) は 11/12 号で掲載済み。日立、NEC、富士通、サイボウズ、アイ・オー・データ、バッファロー、ヤマハのセキュリティ情報のページも見たが、11/11〜13 付けの新しい公表は確認できなかった。

### 国内コミュニティ・研究・イベント

#### [2026-11-12] GMO Flatt Security、「GitHub Actions を狙った広域サプライチェーン攻撃 (11/10〜11/12)」の注意喚起: 乗っ取ったアカウントから 6 万以上のリポジトリに PR を作り、ワークフローに infostealer を入れる
- **何が起きたか**: Flatt Security は 11/12、Takumi Guard の解析基盤で観測した内容を、日本のコミュニティ向けにまとめた。攻撃は 4 段階で進む。乗っ取ったアカウントから「docs: dependency audit notes」の PR を作り (6 万件以上で確認)、ワークフローにシェルスクリプトを入れ、secrets、環境変数、OIDC トークン、クラウドとパッケージレジストリの認証情報、Claude、Codex、Gemini、Copilot、Hugging Face などの AI ツールの認証ファイルを集め、2 つの IP か Telegram Bot API に送る。AWS の role trust の変更、Azure の federated credential の追加、GCP の service account のトークン発行も試みる。
- **なぜ重要か (評価)**: CI の OIDC から、クラウドの信頼関係の書き換えまで狙っている。影響を受けた場合は、シークレットの入れ替えに加えて、IAM の trust policy と federated credential が変えられていないかの点検も要る。PR のタイトル、コミットのメッセージ、ブランチ名が具体的なので、自分の org で該当がないかをすぐ確かめられる。
- 出典: [GMO Flatt Security Blog (2026-11-12)](https://blog.flatt.tech/entry/github_actions_widespread_supply_chain_attack)

#### [2026-11-12] Airターミナル6 の OS コマンドインジェクションを、中学生と大学生を含む 4 人が IPA に届け出
- **何が起きたか**: JVN#64740097 の報告者は、大平剛氏、socho 氏、京都工芸繊維大学の栗山樹氏、豊中市立第十一中学校の小川智也氏の 4 人で、情報セキュリティ早期警戒パートナーシップで IPA に届けられた。Apache HTTP Server 2.4.71 の mod_vhost_alias の件 (CVE-2026-109163) でも、発見者の 1 人に国内の研究者 (Daisuke Hatakeyama 氏、SYZD Research) が名を連ねている。
- **なぜ重要か (評価)**: 家庭用のホームルーターで、中学生を含む報告者がコマンド実行まで届け出た。国内の若手による脆弱性報告の裾野が広がっている。
- 出典: [JVN#64740097](https://jvn.jp/jp/JVN64740097/) / [Apache HTTP Server 2.4 vulnerabilities](https://httpd.apache.org/security/vulnerabilities_24.html)

#### [2026-11-12] NRI セキュア「ASM から CTEM へ」: 脅威インテリジェンスと AI で、攻撃表面のリスクの優先順位を決める
- **何が起きたか**: NRI セキュアは 11/12 のブログで、ASM で見つけた外部公開資産と脆弱性の優先順位の決め方を論じた。台帳から漏れる資産として、事業部門が独自に立てたサイト、使われなくなった DNS レコード (サブドメインのテイクオーバー)、意図せず公開されたテスト環境や管理画面を挙げている。CVSS だけでなく、実際の悪用、外部からの到達性、重要業務とのつながりで判断する CTEM を勧めている。
- **なぜ重要か (評価)**: 外部診断の報告で、優先度の付け方を説明するときの枠組みとして使える。今日の N-central や Apache httpd のように「CVE も KEV もまだないが悪用されている / 外部に出ている」ものを、どう上位に上げるかの議論にも直結する。
- 出典: [NRI セキュア ブログ (2026-11-12)](https://www.nri-secure.co.jp/blog/asm_ctem)

#### [2026-11-12] Zenn: セキュリティ・キャンプ 2026 ミニ (山梨、愛知) の参加記と、応募課題の公開が相次ぐ
- **何が起きたか**: Zenn の security トピックに、11/12 にセキュリティ・キャンプ 2026 ミニ (山梨開催、愛知開催) の参加記と、応募課題を公開する記事が複数投稿された。
- **なぜ重要か (評価)**: 若手の人材育成の動きとして記録する。応募課題の回答は、学生が何に関心を持っているか (OS、Web、ハードウェアなど) を知る材料になる。
- 出典: [Zenn (山梨の参加記)](https://zenn.dev/x86cat/articles/24fae4c88fe0d7) / [Zenn (愛知の参加記)](https://zenn.dev/x86cat/articles/904c79774767f4) / [Zenn (応募課題)](https://zenn.dev/uvu/articles/758ee227a614ea)

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 75 (AI 約 25 / セキュリティニュース 約 20 / CVE データ 6 [NVD API 2.0、OSV、EPSS、CISA KEV JSON、cveawg.mitre.org、raw.githubusercontent.com] / 国内 約 25)
- 採用件数: AI技術=11 / AIセキュリティ=7 / セキュリティ=16 / CVE=16 / 国内インシデント=11 / 国内政策=2 / JVN=7 / 国内コミュニティ=4
- 除外理由内訳: 古すぎ=約 40 (11/10 公表の国内事案 [ソフト99、トレードワルツ、アイル、京都外国語大学、出光興産など]、11/9 以前の公表を 11/12 に報じただけのもの [資生堂、ヤクルト、MOTEX、明治学院大学など]、Proofpoint BluePhishing [11/7・11/9]、aws-api-mcp-server CVE-2026-125271 [11/10]、MongoDB CVE-2026-118383 の NVD 登録 [11/10。Datadog の 11/11 の分析だけをニュースで扱った]、Rails Active Storage など) / 重複=約 45 (11 月の Patch Tuesday、Fortinet、Ivanti、Xen Orchestra、Cisco BroadWorks、Qlik Sense、Maersk、AntiFox、Grok、MDASH、TSMC の出資、Qwen4-Max、Nitro Sandboxes、日本商工会議所、エディオン、IPA / JPCERT の MS 更新など) / 日付不明=約 6 (THN の ThreatsDay のまとめの個別項目 [Citrus ランサムウェア、NTLM 署名の既定化など]、Microsoft「Trained to betray」と Darktrace の盗んだ Claude キーの件は元記事の日付を確認できず不採用、OpenAI Children First Declaration は本文が取れず不採用)
- 取得失敗ソース:
  - api.github.com と github.com の HTML (403)。修正コミットの URL は advisory、NVD の参照、httpd のセキュリティページ、raw.githubusercontent.com の CHANGELOG から取り、diff の中身は直接開いていない
  - git.postgresql.org の gitweb の検索 (429)。REL_18_STABLE の shortlog と atom のコミット名を CVE の説明と照合した。PostgreSQL の CVE とコミットの対応は推定を含む
  - theblock.co (Cloudflare のチャレンジ)、fabric-tokyo.com (403。セキュリコで代用)、secure-navi-inc.jp (JavaScript で描画。ITmedia AI+ で代用)
  - IPA の RSS (XML のパースエラー。新着ページの HTML で代用)、国内ベンダーの PSIRT の一覧ページの多く (JavaScript で描画、または日付なし。JVN と JVN iPedia の RSS で代用)
  - WebFetch はほぼ使わず、curl で取得した
- 備考:
  - CISA KEV は catalogVersion 2026.11.10 のままで、11/11 以降の追加はなかった (cisa.gov と GitHub のミラーで確認)。
  - 表の中に KEV 入りや EPSS ≥ 0.5 のものはない。11/12 公開の CVE の多くは EPSS が未算出。
  - 11/13 公表の国内の発表は、調査時点 (05:10 JST) ではまだ出ていなかった。

</details>
