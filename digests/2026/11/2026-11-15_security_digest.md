# KEDA Daily Digest — 2026-11-15 (JST)

> 採用範囲: 公開日 2026-11-13 〜 2026-11-15
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

週末をはさんだ号で、ベンダーの一次発表は少ない。そのかわり、これまで点で報じられてきた事件の「全体像」が出そろった。
最大の話題は **Cursor の事故報告** (11/13) だ。10/29 に Cursor の拡張マーケットプレイスで配られた改ざん版 Claude Code 拡張 (2.1.312 / 2.1.313) は、**Fireworks AI に預けていたアクセスキー → 学習用に共有していたエージェントの実行記録 (traces) → その中に残っていた未マスクの資格情報 → 社内 SaaS → マーケットプレイスのキャッシュ** という連鎖で配られていた。AI の推論・学習の委託先から、開発者の端末のバックドアまでつながった。今日の深掘りで扱う。
AI セキュリティ側では、**FBI が ARTEX について Flash Alert を出した** (11/13)。同じ日に Talos、Cloudflare、Elastic も ARTEX と派生フレームワークの分析を出した。Cloudflare は「直近 3 日で 50 を超えるフレームワークの系統が顧客をスキャンしてきた」としている。CVE では **Apache Shiro の 8 件の一括公開** (LDAP の認証キャッシュで任意のパスワードが通る、など) と、**Rucio・sysPass・Dokploy の Critical** が目立つ。
AI 技術では、**Gemini 4 Carbon が MathArena で首位** になったこと、**Anthropic の IPO** (11/18 の価格決定に向け、中国本土と香港の投資家が配分から外された) と、Amodei CEO の「来年何が起きるかは非常に不確実」という発言が話題になった。
国内では、**大阪市が、アララ経由で行政オンラインシステムの利用者のメールアドレス 100 万件超の漏えいを公表** した。**paiza** は、ステージング環境のアクセス管理の不備で最大 90 万 2,576 件の個人情報がアクセスされ得た状態だったと公表した。**アットホーム** の賃貸管理システムへの不正ログイン (6,901 件) もあった。GMO は、デスクトップクラウドの侵害の影響額を約 30.5 億円と見込んだ。
**今日まず見るべき 2 件**: (1) チームで Cursor を使っているなら、10/29 に 2.1.312 / 2.1.313 を入れた端末がないかを確かめ、Cursor のサポートに貼った資格情報を入れ替える (深掘り参照)。(2) Apache Shiro を使う Java アプリの診断や保守をしているなら、`DefaultLdapRealm` で `authenticationCachingEnabled=true` にしていないか、認可のアノテーションをインターフェース側に書いていないかを確かめる。

## 今日の深掘り

### [続報] Cursor が事故報告を公表: 改ざん版 Claude Code 拡張は「Fireworks に預けたキー → 学習用の traces に残った資格情報 → 社内 SaaS → 拡張マーケットプレイスのキャッシュ」の連鎖で配られた

- **概要 (事実)**:
  - Cursor は 11/13 (UTC)、2 週間の調査の結果をブログで公表した。BleepingComputer も 11/14 に報じた。
  - 攻撃者は、Cursor が Fireworks AI に発行したアクセスキーを入手した。キーは Fireworks 側で漏れたもので、これを使い、Cursor が Fireworks とのデータ共有に使っていた読み取り専用のストレージバケットをコピーした。
  - バケットにあったのは、主に 2025 年のコーディングエージェントの実行記録 (traces) だ。Privacy Mode を有効にしていない利用者のセッションで、学習への利用が許されていたもの。一部の traces には、マスクされていない資格情報が残っていた。Cursor によると、traces が漏れた利用者は 0.05% 未満、API の資格情報が漏れた顧客は 0.01% 未満。
  - 攻撃者はその資格情報で Cursor の社内 SaaS に入った。持ち出されたのは、アーカイブ済みの本番外のソースコードのリポジトリ (一部に取引先の連絡先)、サポートの問い合わせとメール、利用の指標と連絡先、エージェントの会話の要約の一部、**利用者がサポートに送った資格情報** だ。
  - 10/29 には、盗んだ資格情報で、改ざんした `Anthropic.claude-code` 拡張の 2.1.312 / 2.1.313 を **Cursor の VS Code 拡張マーケットプレイスの配信用キャッシュに直接置いた**。元の配布元の Open VSX にはマルウェアはなかった。配信は約 11 時間で、受け取った可能性があるのは最大 5,000 人。
  - Cursor は「最後の攻撃者の活動は 11/1 で、遮断した」「封じ込めたと考えている」と主張している。本番の基盤、公式のアプリと更新、リリースの署名鍵、Privacy Mode の利用者のコードとプロンプト、顧客のリポジトリは影響を受けていない、としている。
- **技術的な中身**:
  - **起点は「委託先に渡した学習データ」**: 推論・学習の委託先に共有したバケットが、資格情報の保管庫になっていた。traces はエージェントがシェルや設定ファイルを読んだ結果をそのまま含むので、`.env` の値や `Authorization` ヘッダが入りやすい。
  - **境界を越えたのは配信のキャッシュ層**: 拡張の署名や元の配布元 (Open VSX) は無事だった。それでも、中継するキャッシュに書き込めれば、利用者には正規の拡張と区別がつかない。キャッシュに書く権限が、本来の発行元と同じ強さで守られていなかった。
  - **改ざんの中身 (背景の引用、11/1 号既報)**: 拡張の JS がシステムの情報を集め、攻撃者の SSH 公開鍵を登録し、`-R` の逆トンネルで常駐した。Windows は SYSTEM のスケジュールタスク、macOS は LaunchAgent、Linux は `@reboot` の crontab で永続化した。Cursor は「アンインストールだけでは足りない場合がある」と注意している。
  - **対処**: Fireworks からすべての推論を移し、キーを止めた。漏えいした資格情報を危険度の高い順に入れ替え、念のため社内の全資格情報も入れ替えた。拡張マーケットプレイスを作り直し、本番の基盤を再デプロイした。全リポジトリにシークレットスキャンを入れ、委託先からの接続元の制限も広げた。
- **背景・経緯 (過去の事象の引用)**:
  - 11/1 号では、Microsoft の解析と、Anthropic の「自社の侵害ではない」という説明を扱った。どう公開されたかは不明のままだった。11/8 前後には、ある講演で「Fireworks から盗まれた API キーで Cursor に入り、不正なプラグインが約 5,000 社に配られた」という発言が出ていた (当時は未確認)。今回の報告で、これが Cursor の公式な説明になった。
  - Fireworks は 10 月に複数の侵害を公表し、Notion の AI チャット記録の流出 (11/11 号) にも波及している。Wiz は、Railway、Northflank、Lightning AI、OpenCode、Warp など AI 開発基盤への一連の攻撃を「Black October」と呼んでいる。Railway では、盗まれた秘密情報で約 74 万ドルの不正な AI の利用料が発生した。
- **なぜ今これが重要か (評価)**:
  - 「AI の委託先 → 学習データ → 資格情報 → 開発ツールの配布路 → 開発者の端末」という連鎖が、一次情報で確認された初めての事例とみる。委託先の管理 (サブプロセッサー) の議論に、「学習用に渡したデータに資格情報が入っていないか」という観点を足す必要がある。
  - 診断の観点では、**配布の中継層 (キャッシュ、ミラー、プロキシ)** への書き込み権限が、元の発行元と同じ強さで守られているかが、新しい確認項目になる。社内の npm / PyPI のミラーや、VS Code 拡張の社内ミラーにもそのまま当てはまる。
  - 「サポートに送った資格情報」が持ち出された点も重い。どの SaaS でも、問い合わせのチケットは秘密情報の置き場になりやすい。
- **読者が今日できること**:
  - 10/29 に Cursor で `anthropic.claude-code` の 2.1.312 / 2.1.313 を入れたり更新したりした端末を洗い出す。Cursor の security notice の確認手順とスクリプトに沿って、`authorized_keys` に知らない鍵がないか、逆 SSH の常駐 (スケジュールタスク `SysMon`、`com.apple.sysmond.plist`、`@reboot`) がないかを見る。
  - Cursor のサポートとのやり取りに貼った API キーやトークンは、通知の有無にかかわらず入れ替える。Privacy Mode を使っていなかった期間がある組織は、Cursor からの個別通知を確認する。
  - 自社のエージェントの実行記録や LLM のログを外部に渡しているなら、渡す前に資格情報のパターン (AWS キー、`sk-`、`ghp_`、JWT など) でスキャンしているかを確かめる。
- 出典: [Cursor (2026-11-13)](https://cursor.com/blog/security-incident-update) / [BleepingComputer (2026-11-14)](https://www.bleepingcomputer.com/news/security/cursor-confirms-security-breach-led-to-malicious-claude-code-extension/) / [Cursor security notice (10/30、背景)](https://cursor.com/blog/security-notice-claude-code-extension)

## AI 技術・トレンド

### [2026-11-14] Gemini 4 Carbon が MathArena で首位に。2 位は Claude Fable 5.2、3 位は GPT-6.1 Sol。ただし 1 問あたりの費用は Sol の約 15 倍
- **何が起きたか**: 数学のベンチマーク MathArena で、Gemini 4 Carbon (high) が 85.4% で首位になり、GPT-6.1 Sol (max、80.6%) を抜いた。Claude Fable 5.2 (max) は 82.8% で 2 位。試験の設定での費用は、Carbon が 15.70 ドル、Fable 5.2 が 40.20 ドル、Sol が 1.07 ドルだった。公開モデルの最高は Kimi K3.1 Pro の 54.3%。Carbon の失敗の多くは時間切れで、11 時間以上進み具合を確かめずにスクリプトを走らせた例もあった。
- **なぜ重要か**: 上位 3 つの差は誤差の幅に近く、決め手は「性能あたりの費用」になりつつある。長時間動かすエージェント (脆弱性の探索など) にモデルを選ぶときは、正答率だけでなく、打ち切りの設計と 1 タスクあたりの費用で比べる必要がある。
- 出典: [The Decoder](https://the-decoder.com/gemini-4-carbon-takes-the-matharena-crown-but-costs-15-times-more-than-gpt-6-1-sol/)

### [2026-11-14] Anthropic、Claude Opus 5.5 向けに「古いプロンプトの癖を捨てる」よう案内。「think hard」は不要、effort は Medium から
- **何が起きたか**: Anthropic は、Pro / Max / Ultra / Team の既定になった Opus 5.5 について、プロンプトの指針を出した。モデルは常に自分で推論し、深さを課題と effort の設定に合わせて変えるので、「think hard」などの言い回しは消してよいとしている。社内の試験では、外したほうが応答の開始が速く、品質は下がらなかったという。effort は既定の Medium から始め、足りないときだけ High にするよう勧めた。Opus 5.5 の Medium は、Opus 5 の High と同等だったとしている。
- **なぜ重要か**: 診断や解析の自動化で使っているシステムプロンプトに、古い世代向けの指示が残っていれば、遅くて高いだけになる。effort を上げれば精度が上がる、という前提も見直したい。
- 出典: [The Decoder](https://the-decoder.com/anthropic-says-outdated-prompting-habits-are-slowing-down-claude-opus-5-5/)

### [2026-11-13〜14] [続報] Anthropic の IPO: 中国本土と香港の投資家は配分から外される。Amodei CEO は「計算資源の購入が最大のジレンマ」と発言
- **何が起きたか (前回からの差分)**:
  - Bloomberg によると、複数の引受銀行が、中国本土と香港からの買い注文を断るか、配分しない方向で、一部は ITAR (米国の防衛関連の輸出規制) を理由に挙げた。主幹事は Goldman Sachs と Morgan Stanley で、ほかに 20 行が参加する。11/18 に価格を決め、NASDAQ の `ANT` で取引を始める予定。Anthropic はコメントしていない。
  - Amodei CEO は 11/13 の JPMorgan の投資家向けの催しで、「来年何が起きるかは非常に不確実」と述べた。計算資源は、売上が見合うと分かる 1〜2 年前に買わなければならず、これが「事業上の最も深いジレンマ」だという。Bloomberg によると、同社の支払いの約束はほぼ 9,010 億ドルで、そのうち約 710 億ドルが 2027 年 9 月までに期限を迎える。
- **なぜ重要か**: AI の大手の資金と事業が、輸出規制と安全保障の枠組みに組み込まれていく流れが、株式の配分にまで及んだ。利用者にとっては、提供の継続性と料金の見通しを、各社の資金繰りから読む必要が出てきた。
- 出典: [The Decoder (11/13、銀行の対応)](https://the-decoder.com/banks-bar-chinese-and-hong-kong-investors-from-anthropic-ipo-over-us-export-controls/) / [The Decoder (11/14、Amodei 氏の発言)](https://the-decoder.com/anthropic-ceo-amodei-admits-theres-a-huge-uncertainty-in-whats-going-to-happen-next-year-days-before-a-record-ipo/)

### [2026-11-14] 元研究者の Coxon 氏:「Anthropic は Mythos を、当初の何分の一かの計算量で学習し直せる」。IPO の資料のグラフが辞めた理由の 1 つ
- **何が起きたか**: OpenAI と Anthropic にいた研究者の Jacob Coxon 氏は、Anthropic の IPO のロードショーで示された「コードの事前学習の計算効率の倍率」のグラフを挙げた。2024 年 7 月から 2026 年 10 月にかけて、対数の軸でも急に立ち上がっており、アルゴリズムの効率が加速しながら上がっていると主張した。「Mythos は一度きりの跳躍ではない」とも書いた。約 4 か月で同社を辞めた理由の 1 つがこのグラフだという。
- **なぜ重要か**: 主張は本人の解釈で、Anthropic は答えていない。ただ、もし正しければ、攻撃能力の高いモデルを限定提供で抑える期間は短くなる。ARTEX の拡散 (AI セキュリティの項) と合わせて、「強いモデルは一部の組織だけ」という前提を長く置けない、という見方を補強する。
- 出典: [The Decoder](https://the-decoder.com/anthropic-can-already-retrain-mythos-with-a-fraction-of-the-compute-originally-needed-says-former-researcher-coxon/)

### [2026-11-14] OpenAI、ロボティクスのチームを再編。研究者は Mark Chen 氏の研究部門へ、応用とハードウェアは Brockman 氏の Applied へ
- **何が起きたか**: Fortune によると、OpenAI はロボティクスの研究者を主要な研究チームに移し、応用ロボティクスとハードウェアのチームを Greg Brockman 氏の Applied 部門に統合した。OpenAI は「解散ではなく、研究と製品により近づけるための再編で、ロボティクスの仕事は続く」と説明した。決定が急で、Austin で開かれたロボット学習の学会 CoRL のブースは空いたままだったという。背景には、GPT-6 Astra のような汎用モデルが直接ロボットを制御できるという見方がある (NVIDIA の研究では、Astra のエージェントが模擬のロボットの課題で 74.8% 成功し、専用モデルの最高は 51%)。
- **なぜ重要か**: 「専用モデルより汎用モデル」の流れが、ロボットの制御にまで広がっている。物理の機器を汎用のエージェントが動かすなら、プロンプトインジェクションの影響は、データの漏えいから物理の動作にまで広がる。
- 出典: [The Decoder](https://the-decoder.com/openai-reassigns-robotics-researchers-to-other-teams-as-general-purpose-models-might-make-specialized-robotics-ai-unnecessary/)

### [2026-11-14] Runway、ロボット用のモデル「Praxis-1」を Apache 2.0 で公開。動画で学んだ知識でロボットの動きを計算
- **何が起きたか**: Runway は、9 月に一部の提携先だけに出していた Praxis-1 の重みとソースコードを Apache 2.0 で公開し、詳しい研究報告と新しい性能の試験も出した。カメラの画像、文の指示、ロボットの位置の情報を入力に、環境の変化を予測して動きを計算する。追加の学習で別のロボットに合わせられるという。Runway によると、似た見た目の物を取り違えることがあり、複雑な手順を自分で計画するのはまだ苦手だ。
- **なぜ重要か**: 商用で使えるロボットの基盤モデルが、オープンで手に入るようになった。工場や倉庫の制御系の診断では、こうしたモデルが入った機器の「入力 (カメラ、指示文) の改ざん」を想定した試験が必要になっていく。
- 出典: [The Decoder](https://the-decoder.com/runways-open-source-praxis-1-turns-video-ai-into-a-robot-controller/)

### [2026-11-13] Amazon「World Product Graph」: 自社で売っていない商品まで含め、ネットで売られるあらゆる商品の情報を集める計画 (Reuters)
- **何が起きたか**: Reuters によると、Amazon はネット上で売られるすべての商品の情報を集め、自社のサイトで見られるようにする「World Product Graph」を計画している。買い物客が Reddit や Google で下調べをして離れるのを減らし、AI エージェントも Amazon の索引に頼るようにする狙いだという。外部の店の商品へのリンクも、すでに一部で出している。
- **なぜ重要か**: ChatGPT Wallet や Gemini × Google Wallet (前号) と並び、「エージェントがどの索引を見て買うか」の争いになっている。エージェントが参照する商品データそのものが、SEO 汚染や偽の店の誘導 (前号の Podqi の調査) の新しい標的になる。
- 出典: [The Verge](https://www.theverge.com/tech/1033697/amazon-world-product-graph-ai-search)

### [2026-11-13] AWS、コーディングエージェントの要求を最適なモデルに振り分ける「NVIDIA NeMo Switchyard」の使い方を公開。評価の軸は「解けたタスクあたりの費用」
- **何が起きたか**: AWS は、オープンソースのライブラリ NeMo Switchyard を Amazon Bedrock と LiteLLM で使い、Claude Code や Codex CLI の要求を複数のモデルに振り分ける方法を解説した。直近のツールの使い方と結果を読んで 2 つの候補から選ぶ「stage routing」と、重み付きの「random routing」がある。評価は、トークン単価ではなく「全実行の費用 ÷ テストが通った実行の数」で行うよう勧めている。
- **なぜ重要か**: エージェントの費用は、ターン数、毎回読み直す履歴の量、やり直しで決まる。社内でエージェントを運用する組織は、どのモデルにどの要求が流れたかを記録しておかないと、事故のときに追えなくなる。
- 出典: [AWS Machine Learning Blog](https://aws.amazon.com/blogs/machine-learning/route-coding-agent-requests-to-the-right-model-on-amazon-bedrock-with-nvidia-nemo-switchyard/)

### [2026-11-13] OpenAI Foundation の理事 Paul Cristiano 氏 (Ars Technica の表記):「この会場の多くの人にとって、最もありそうな死因は AI の事故だ」
- **何が起きたか**: Alignment Research Center の代表でもある Cristiano 氏は、トロントでの 3 回の講演の初回で、目標を追う AI が「人間が今地球で決めているのと同じ意味で物事を決める」状態 (AI takeover) への懸念を述べた。止めようとする人間は「米軍を止めようとする個人」くらい無力になる、とした。
- **なぜ重要か**: OpenAI の非営利の側の理事が、ここまで強い言い方をした。各社の IPO と資金調達の話が続くなかで、安全性をめぐる発言は規制の議論の材料になりやすい。
- 出典: [Ars Technica](https://arstechnica.com/ai/2026/11/ai-is-the-most-likely-reason-youll-die-openai-board-member-warns/)

### [2026-11-14] [続報] NVIDIA の Huang 氏の辞任へのアジア各国の反応: 韓国は GPU 26 万基の供給を確認、日本の経産省は「注視する」
- **何が起きたか (前回からの差分)**: TechCrunch がまとめた。韓国の科学技術省は、NVIDIA が先端 GPU 26 万基の供給と共同の AI 事業の継続を改めて約束したと発表し、政府の AI 戦略の会議も 11/13 に緊急の会合を開いた。台湾の経済部長は業界への大きな影響はないとし、台北市は NVIDIA の海外本社の計画は予定どおりとした。日本では、経産省が NVIDIA を注視するとし、尾崎官房副長官は影響の判断は早いと述べた。シンガポールは、Megaspeed とほか 6 人への捜査が続いているとした。
- **なぜ重要か**: 国内の AI の計算基盤の計画は、NVIDIA の供給に強く依存している。経営の混乱が長引けば、国産 LLM の学習の予定にも響く。
- 出典: [TechCrunch](https://techcrunch.com/2026/11/14/asian-governments-react-to-nvidia-ceo-jensen-huangs-exit/)

### [2026-11-13 報道] 国内: Sakana AI、事前学習から自社で作るモデル「Sakana Sawara (仮称)」を準備。12 月に「Sawara Small」の学習を始め、2027 年春に重みを公開する予定
- **何が起きたか**: ITmedia AI+ の書面取材に、Sakana AI が答えた。Sawara は自律的にタスクをこなすエージェント向けに設計し、同社の製品の土台にする。学習データと手法を含めて自社で管理するので、研究にも使えるという。12 月に Sawara Small の事前学習を始め、順調なら 2027 年春に重みを公開する。より大きい Sawara Large も計画し、数千億パラメータ以上も視野に入れる。これまでは、海外のオープンなモデルに事後学習した「Sakana Namazu」などが中心だった。
- **なぜ重要か**: 学習データまで把握できる国産のモデルは、政府や重要インフラで「何を学習したか」の説明を求められる場面で選ばれやすい。重みの公開は、国内で安全性の評価や脆弱性の研究をする材料にもなる。
- 出典: [ITmedia AI+](https://www.itmedia.co.jp/aiplus/article/2611/13/2000003141/)

### [2026-11-13 報道] 国内報道: Google の社内専用のコーディング AI「GfG」の論文。Gemini に社内の開発データ 1 兆トークンを学習させ、所要時間が半分になった業務も
- **何が起きたか**: ITmedia の「Innovative Tech」が、Google などの研究者が 10 月に出した論文「Customizing an LLM for Enterprise Software Engineering」を解説した。Google ではコードの 75% 以上が AI で書かれるか下書きされているが、公開データで学んだモデルは社内のライブラリや慣習を知らない。そこで社内の開発データで Gemini を追加学習させ、社内向けに特化させた。
- **なぜ重要か**: 社内のコードで学習したモデルは、社内の秘密情報や脆弱なパターンも覚えうる。国内企業が同じことをするなら、学習データから秘密情報を除く手順 (深掘りの Cursor の教訓と同じ) と、モデルの出力からの漏えいの試験が要る。
- 出典: [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2611/13/2000003110/)

## AI セキュリティ

### [2026-11-13] FBI が ARTEX について Flash Alert:「最初の標的の選定から特権の取得まで 3 時間未満の侵入もある」。同じ日に Amazon も、中国系の複数のグループが盗んだキーで推論代を払いながら資格情報を探し続ける運用を報告
- **何が起きたか**:
  - FBI は、オープンソースの AI ペンテスト基盤 ARTEX が、犯罪者と国家系の攻撃者に使われ、政府機関と数十の重要分野が侵入されているとする Flash Alert を出した。開発者 (Autumn-27、FBI は中国の技術者の Li Puhua 氏と特定) は 10/8 にリポジトリを消したが、フォーク、地域向けの改造版、アーカイブ、商用版で広がり続けているという。
  - FBI は、攻撃者が使う ARTEX では中国系のモデルが多く、DeepSeek Flash 系が主流だとした。「ペンテストのため」と前置きすると安全装置が見えにくいことと、費用の安さが理由だという。Censys の調査では、公開された ARTEX のコンソールは 1,600 を超える。
  - 狙われやすいのは、取引先・仕入れ先のポータル、モバイルのバックエンド、社員向けアプリ、営業支援、古いサービス、外部連携、事業部ごとに作られたアプリなど、セキュリティの目が届きにくいところだという。韓国と日本の金融機関への攻撃にも関わったとされる。
  - Amazon の CISO の CJ Moses 氏は、中国系の複数のグループが、盗んだキーで推論の代金を払いながら次の資格情報を探す「自走する運用」をしていると述べた。暗号資産の取引所の本人確認を、リアルタイムのディープフェイクの注入で突破しようとする作戦も確認したという。
- **悪用 / PoC**: 実際の侵入 (FBI・Amazon の報告)。
- **なぜ重要か (評価)**: 米国の捜査機関が名前を挙げて警告する段階に入った。「目が届きにくい周辺のアプリ」が狙われるという指摘は、診断の対象をどう決めるかに直結する。本体のアプリだけでなく、取引先ポータルや古いサブドメインまで範囲に入れるよう提案する根拠になる。
- 出典: [The Record (2026-11-13)](https://therecord.media/artex-ai-tool-fbi-flash-alert)

### [2026-11-13] Cloudflare:「直近 3 日で 50 を超える AI ペンテスト基盤の系統が顧客をスキャン」。ARTEX のリポジトリは 1 万 2,000、AI ペンテストのツールからの要求は 10/1 から 30 倍
- **何が起きたか**: Cloudflare によると、数週間前は ARTEX しかなかった LLM のペンテスト・オーケストレーターが、直近 3 日で 50 を超える系統に増え、実行している IP アドレスは数千に達した。ARTEX の系統のリポジトリは 1 万 2,000 を超え、独自の変更を含む公開のフォークは 204 ある。1 日あたりの要求は 10/1 から 30 倍になり、盗んだ顧客の資格情報をつないで横に広がる攻撃も出ている。対策として、WAF とレート制限、異常検知、ボット対策、高リスクのアプリへの ID ベースのアクセス制御、スキーマの検証、脅威情報の 6 つを挙げた (同社の製品の宣伝を含む)。
- **なぜ重要か (評価)**: 「人間の攻撃者は面倒な設定ミスを見逃す」という前提が崩れた。エージェントは公開されたサービスと設定を網羅的に試すので、小さな設定ミスもすぐ見つかる。診断で「低」とした設定の不備も、直す優先度を上げてよい。
- 出典: [Cloudflare Blog](https://blog.cloudflare.com/adapting-to-ai-penetration-testing-orchestrators/)

### [2026-11-13] Talos:「ARTEX とその先」: 公開された PentAGI のインスタンスが 700 超。HexStrike AI は MCP で Claude Code や VS Code につながる
- **何が起きたか**: Cisco Talos は、AI を使うペンテスト基盤の実際の悪用をまとめた。Hephaestus は VPS に 1 本のスクリプトで入り、Telegram で操作できる。PentAGI は Web の画面で攻撃の流れをグラフで見られ、インターネットから届くインスタンスが 700 を超える。HexStrike AI は MCP に対応したクライアント (Claude Code、VS Code など) とつながる。これらは nmap や nuclei に加え、Censys / Shodan、CAPTCHA の突破、漏えいした資格情報の管理、住宅用プロキシ、ハッシュの解読のサービスまで使う。ARTEX の基盤では VShell、GoPhish、AdaptixC2 も見つかった。Talos は、今後は自律的な横移動、データの特定と持ち出し、ランサムウェアの実行まで自動化されると予測している。
- **なぜ重要か (評価)**: MCP で既存のツールを何でもつなげる設計なので、「ARTEX 固有の痕跡」で検知するのは難しい。Talos は、IoC がない状態で侵害を見つける時間を短くすることと、封じ込めの手順を先に決めておくことを勧めている。
- 出典: [Cisco Talos](https://blog.talosintelligence.com/artex-and-beyond/)

### [2026-11-13] Elastic:「許可を求めない 5 つの AI 攻撃フレームワーク」: ARTEX、CyberStrikeAI、Cairn、PentAGI、HexStrike のどれも、認可をコードで強制していない
- **何が起きたか**: Elastic Security Labs は 5 つのフレームワークのソースを読み、比べた。合わせて GitHub のスターは 6 万を超え、すべて実際の侵入で見つかっている。どれも認可 (攻撃してよい対象か) をコードで強制しておらず、3 つはプロンプトで「認可済みのはず」と書くだけだった。既定で有効な対象の制限は、政府と教育機関のドメインの拒否リストだけだった。CyberStrikeAI は承認モードが既定でオフ、PentAGI の Compose ファイルは `ASK_USER=false`、ARTEX はエージェントを権限確認を飛ばすモードで動かす。GTIG によると、ARTEX は 2〜25 秒の短い連続で動く。Elastic は、送信元や User-Agent ではなく、プロセス、Web の要求、API の呼び出し、サインインといった振る舞いで検知する ES|QL の検索を示した。
- **なぜ重要か (評価)**: 自社でこうしたツールを診断に使う場合も、対象の範囲外に出ない仕組みは自分で作るしかない。11/6 号の WorkOS の件 (評価中のエージェントが隔離を抜けた) と同じ事故は、どの組織でも起こりうる。
- 出典: [Elastic Security Labs](https://www.elastic.co/security-labs/threat-command/agentic-offensive-frameworks-detection-artex)

### [2026-11-13] Apache APISIX の `openapi-to-mcp`: MCP のツールから、OpenAPI の文書で宣言していない API のパスを呼べる (CVE-2026-124726)
- **何が起きたか**: APISIX 3.19.0 以上 3.20.0 未満で、MCP のエンドポイントを呼ぶ側が、OpenAPI の文書が宣言していないエンドポイントを、宣言されたツールの HTTP メソッドで呼べた。そのとき、Route が付ける資格情報もそのまま使われる。相対パスのトラバーサルと、意図しないプロキシの組み合わせだ (CVSS 4.0 は 6.9)。3.20.0 で修正された。
- **なぜ重要か (評価)**: 「OpenAPI の文書から MCP のツールを自動で作る」ゲートウェイは増えている。ツールの引数に入ったパスを、文書の範囲に閉じ込めているかは、他の実装でも同じ形で確かめられる。プロンプトインジェクションでエージェントに `../` を入れさせれば、内部の API に資格情報付きで届く。
- 出典: [oss-security (2026-11-13)](https://seclists.org/oss-sec/2026/q4/697)

### [2026-11-13] 国内の JVN iPedia: Telerik Document Processing の「AI エージェントのツール」に、出力先の外のファイルを読み書きできるパストラバーサル (CVE-2026-118038)
- **何が起きたか**: JVN iPedia は、Progress Telerik Document Processing Libraries (2026.3.1027 より前) の Convert と Merge の AI エージェント向けツールに、パストラバーサルがあると公開した。ツールの引数を指定できる認証済みの低い権限の攻撃者は、設定した出力ディレクトリの外のファイルを読め、相対パスがプロセスの作業ディレクトリ基準で解決されるので、書き込みできるなら上書きもできる (CVSS 7.1)。
- **なぜ重要か (評価)**: 既存のライブラリが「AI エージェント用のツール」を足すと、引数をエージェント (つまりプロンプト) が決めるようになる。従来は開発者が固定していたパスが、攻撃者の入力になる。APISIX の件と同じ型だ。
- 出典: [JVN iPedia JVNDB-2026-043357](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-043357.html)

## セキュリティニュース

> 週末のため、ベンダーの一次発表は少ない。Cursor の事故報告は「今日の深掘り」を参照。

### [2026-11-13] Copeland / Dixell の冷凍設備の監視システム XWEB EVO に 14 件の脆弱性。ログイン画面が、パスワードを確かめる前にユーザー名をシェルのコマンドとして実行 (VulnCheck)
- **何が起きたか**: VulnCheck は、Copeland の Dixell ブランドの監視システム XWEB EVO の 14 件の脆弱性を公表した。作り直したファームウェアでの試験では、どれも root か管理者の権限につながる。CVSS は多くが 8〜9.8 で、少なくとも 2 件は実際に悪用されている。XWEB EVO は、10 月にフランスの約 700 のスーパーの冷凍設備が乗っ取られた事件で、影響を受けた 4 製品の 1 つだ。研究者の Lobstein 氏は「その日の日付をパスワードにするより悪い。ログイン画面は、パスワードを確かめる前に送られたユーザー名をシェルのコマンドとして実行する」と書いた。修正版は出ているが、古い版は公開されたまま残っている。
- **悪用 / PoC**: 2 件が悪用中 (VulnCheck)。
- **なぜ重要か**: 冷凍設備の監視は、小売・物流・医薬の現場でインターネットに出たままのことが多い。前号までの Copeland XWEB PRO のボットネット化と合わせ、OT の診断では、ログイン画面のユーザー名の欄にコマンド注入を試す価値がある。
- 出典: [CyberScoop](https://cyberscoop.com/copeland-dixell-refrigeration-vulnerabilities/)

### [2026-11-13〜14] 米 FAA が全米の出発を 4 時間以上止める。政府は「攻撃の痕跡はない」とし、FBI はソフトウェアの更新を原因の候補として調べる
- **何が起きたか**: FAA は 11/13、航空路の管制センターの通信の不具合で、全米の出発を止めた (FAA の歴史で 3 回目)。米東部時間 20:15 に解除されたが、数千便に影響した。国土安全保障長官の Mullin 氏は「攻撃の痕跡はないが、まだ調べている」と述べ、NSA、国防総省、CISA も加わった。Bloomberg によると、FBI はソフトウェアの更新を原因の候補として調べている。運輸長官の Duffy 氏は、古いスイッチやルーターがデータであふれ、矛盾した情報を出し始めたと説明した。
- **悪用 / PoC**: なし (攻撃の痕跡は見つかっていない)。
- **なぜ重要か**: Microsoft 365 の障害 (次の項) と同じ週に、「攻撃ではない大規模な停止」が続いた。重要インフラの BCP は、サイバー攻撃と運用ミスを区別せず、同じ手順で止めて戻せるかで評価する必要がある。
- 出典: [SecurityWeek (2026-11-14)](https://www.securityweek.com/no-signs-of-hacking-in-faa-ground-stop-as-fbi-reportedly-probes-software-update/)

### [2026-11-13〜14] [続報] Microsoft 365 の世界的な障害: 「以前のネットワークの容量増強のときの問題が、最近の変更で表に出た」。日本時間 11/14 15 時ごろに全地域で復旧
- **何が起きたか (前回からの差分)**: Microsoft は、障害の原因を、以前のネットワークの容量増強のときに生じた問題が、最近のネットワークの変更をきっかけに表面化したものと説明した。根本原因には対処済みで、日本時間 11/14 の 15 時ごろに全地域で復旧したと発表した。サイバー攻撃や AI / エージェントとは関係のない技術的な問題だとし、詳しい報告書を後で出すという。障害中は、遅れたメールを守るため、メールのタイムアウトを 48 時間に延ばした。英国 NCSC の元長官 Ciaran Martin 氏は、AWS や CrowdStrike の障害より悪い可能性があると述べた。日本では政府の IT 基盤にも影響したと、尾崎官房副長官が述べている。
- **なぜ重要か**: 復旧後もしばらくは、大量のメールの遅れや未達の確認が要る。障害に便乗した「Microsoft 365 の再認証」を装うフィッシングにも注意したい。
- 出典: [Impress Watch (2026-11-14)](https://www.watch.impress.co.jp/docs/news/2156470.html) / [Ars Technica (2026-11-13)](https://arstechnica.com/tech-policy/2026/11/microsoft-blames-failed-server-health-checks-not-hackers-for-global-outage/)

### [2026-11-13] [続報] Windows のゼロデイ「SignDrop」: Will Dormann 氏が再現。ただし Windows 11 26H2 で、インストールから 90 日を超えた環境が条件らしい
- **何が起きたか (前回からの差分)**: Ars Technica によると、Dormann 氏は PoC が説明どおり動くことを確かめたが、すべての Windows 11 では動かなかった。26H2 で、90 日以上たった環境が必要らしく、新しく入れた 26H2 に更新を当てただけでは再現しないという。作者 (Nightmare Eclipse) は、CLFS の認証モードが learning か enforcement なら影響を受けるとしている。また、攻撃は Defender に限らず、ほかの EDR の自己防御 (改ざん防止) も回避できると主張している。KEV には入っておらず、悪用の報告もない。
- **悪用 / PoC**: PoC 公開済み、悪用の報告なし。
- **なぜ重要か**: 診断や演習の端末で再現を試すなら、新しく作った VM ではなく、運用中の 26H2 の環境の CLFS の認証モードを確かめる必要がある。
- 出典: [Ars Technica](https://arstechnica.com/security/2026/11/windows-0-day-dropped-by-disgruntled-researcher-hands-hackers-system-rights/)

### [2026-11-13] Apple、カメラとマイクのデータを主 OS から切り離す「Secure Exclaves」の設計を公開
- **何が起きたか**: Apple は、自社のシリコンで、ambient sensing (「Hey Siri」の待ち受けや、HomeView での顔と声の認識) に使うカメラとマイクのデータを、主 OS から隔離して処理する仕組みを説明した。主 OS はエクスクレーブの中のデータを取り出せず、変えられない。HomeView の認識結果として主 OS に渡るのは、人の識別子、位置、確信度だけだという。アプリがセンサーをすべて使うときは、インジケーターが十分な時間点いていることを専用のエクスクレーブが確かめてから、データを渡す。iPhone では、画面の点が実際に描かれたかを、別のエクスクレーブが画素で確かめる。
- **悪用 / PoC**: なし (設計の公開)。
- **なぜ重要か**: 「カメラが動けば必ずインジケーターが点く」をハードウェアの側で保証する設計で、スパイウェアの盗撮の手口に対する Apple の答えだ。モバイルの診断や研究では、エクスクレーブと主 OS の間の細い通り道が、新しい攻撃面として注目されるとみる。
- 出典: [SecurityWeek (2026-11-14)](https://www.securityweek.com/apple-reveals-how-secure-exclaves-shield-camera-and-microphone-data/) / [Help Net Security (2026-11-13)](https://www.helpnetsecurity.com/2026/11/13/apple-secure-exclaves-security-architecture/)

### [2026-11-13] Apache Shiro、8 件の脆弱性を一括で公開。LDAP の認証キャッシュを有効にすると、一度ログインした利用者は任意のパスワードで入れる (CVE-2026-129349、CVSS 4.0 で 9.1)
- **何が起きたか**: Apache Shiro は 11/13〜14 (UTC) に 8 件の advisory を出した。最も重いのは CVE-2026-129349 で、`DefaultLdapRealm` (または `JndiLdapRealm`) で `authenticationCachingEnabled=true` のとき、キャッシュされた認証は LDAP の bind を飛ばし、既定の `AllowAllCredentialsMatcher` がどんな資格情報も受け入れる。ほかに、認可のアノテーション (`@RequiresRoles` など) がインターフェースや親クラスに書かれていると効かない件 (CVE-2026-74763)、空の保存済み資格情報が空のパスワードと一致する件 (CVE-2026-129347)、RememberMe のセッション固定 (CVE-2026-74762)、Jakarta Pages / Faces のタグの XSS (CVE-2026-129320) などがある。修正は 3.0.1 / 3.0.2。
- **悪用 / PoC**: 悪用の報告なし。
- **なぜ重要か**: Shiro は国内の業務系の Java アプリで今も多く使われ、過去には CVE-2016-4437 (RememberMe のデシリアライズ) が長く悪用された。今回の件は設定の組み合わせが条件なので、ソースコード診断で設定とアノテーションの位置を見れば、すぐ判定できる (CVE の項を参照)。
- 出典: [oss-security (CVE-2026-129349)](https://seclists.org/oss-sec/2026/q4/705) / [Apache Shiro Security Reports](https://shiro.apache.org/security-reports.html)

### [2026-11-13] 偽の「GTA 6 の PC 版」が Google Colab のノートブックから配られ、WARDEN Stealer が Steam のログインと暗号資産のウォレットを盗む (Cynet)
- **何が起きたか**: Cynet は、Google Colab のノートブックにある「GTA 6 EXE のダウンロード」のリンクをたどり、「Windows Software Hub」というページから配られる ZIP の中に、WARDEN Stealer のローダーを見つけた。保存されたパスワード、ブラウザの Cookie、Steam と Roblox の資格情報、暗号資産のウォレットを盗む。ページは 72MB と表示していたが、実際は 796KB の実行ファイルと 1KB の README で、インストーラーは防御機能を切るよう指示する。GTA 6 は 11/19 に発売されるが、PC 版はない。
- **悪用 / PoC**: 実際の配布 (Cynet)。
- **なぜ重要か**: Colab や GitHub など信頼されたドメインを入口にすると、URL のフィルタを通りやすい。発売日の前後は、社用端末での「先行版」の検索や実行に注意を促す時期だ。
- 出典: [Help Net Security](https://www.helpnetsecurity.com/2026/11/13/fake-gta-6-download-scam/)

### [2026-11-13] Microsoft、11 月の更新で Windows のライセンス認証が失敗する問題を確認 (エラー 0x80041008)
- **何が起きたか**: Microsoft は、11 月の Patch Tuesday の更新を当てた端末で、`slmgr.vbs /skms-domain` や `/ipk` を実行すると、エラー 0x80041008 で KMS の設定やプロダクトキーの登録が失敗すると認めた。対象は Windows 10 21H2 / 22H2、Windows 11 23H2、Windows Server 2019 / 2022 / 2025。すでに認証済みの端末や、イメージに KMS のクライアントキーが入っていて SLMGR を使わない組織は影響を受けない。
- **悪用 / PoC**: なし (不具合)。
- **なぜ重要か**: 月例の更新を急いで当てた組織で、キッティングの自動化が止まる。更新を見送る理由にはしないで、影響の範囲を確かめたうえで回避策を待つのがよい。
- 出典: [BleepingComputer (2026-11-13)](https://www.bleepingcomputer.com/news/microsoft/microsoft-confirms-windows-activation-failures-after-november-updates/)

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-11-13 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先。期間内に KEV への新しい追加はなかった (11/13 の 2 件は前号で既報)。

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-100397 / GHSA-x585-4vv8-2mh2 | Rucio (PyPI) 1.14.0.post1 以上 35.9.1 未満 | CWE-287, 305 / 9.8 | 認証前に誰でも任意のアカウント名で発行できる SSH の challenge トークンが、通常の認証トークンと同じテーブルに入り、`validate_auth_token()` が区別しない → 管理者になりすまし | [f5db354](https://github.com/rucio/rucio/commit/f5db3546d9c0de4642dc9aa52e6a6e447911d680) | 未認証・Critical |
| CVE-2026-129110 | sysPass 3.0.1〜3.2.11 | CWE-306 / 9.8 | `install/install` のハンドラが `isInstalled()` を確かめない → 未認証で再インストールし、`config.xml` を書き換えて攻撃者の DB に向け、管理者を作り、PublicLink のデシリアライズのガジェットで RCE | [PR #360](https://github.com/OpusProjects/sysPass/pull/360) (commit 不明) | 未認証 RCE / EPSS 0.008 |
| CVE-2026-129433 / GHSA-j329-jw7j-rxjm | Dokploy 0.31.1 未満 | CWE-78 / 9.9 | tRPC の `backup.create/update` で保存した `serviceName` がシェルに渡る `getComposeContainerCommand()` に入る → 定期バックアップのときに root でコマンド実行、Docker ソケットでホストを奪取 | [b24006e](https://github.com/Dokploy/dokploy/commit/b24006e16e95a10ce3daf739d06ac783e5c70ba0) | 保存型の注入 |
| CVE-2026-129349 | Apache Shiro (shiro-core) 3.0.1 未満 | CWE-287 / CVSS4 9.1 | `DefaultLdapRealm` で認証キャッシュが有効なとき、キャッシュ命中で LDAP の bind を飛ばし、既定の `AllowAllCredentialsMatcher` が判定 → 既知のユーザー名なら任意のパスワードで認証 | [advisory](https://seclists.org/oss-sec/2026/q4/705) (commit 不明) | 設定依存 (非既定) |
| CVE-2026-74763 | Apache Shiro (guice / aspectj / cdi / jakarta-ee) 3.0.2 未満 | CWE-863 / CVSS4 6.3 | インターフェースや親クラスに書いた `@RequiresRoles` / `@RequiresPermissions` を、メソッドの解決のときに拾わない → 保護したはずのメソッドを権限なしで呼べる | [advisory](https://seclists.org/oss-sec/2026/q4/701) (commit 不明) | ソース診断で即判定 |
| CVE-2026-128077 / GHSA-r99w-jh2x-3mg9 | @nuxt/nitro-server 4.6.0 以上 4.6.4 未満 | CWE-436, 863 / 6.5 | `//x/admin` を Nuxt はホスト付きの URL と解釈して `/admin` のページを描くが、Nitro の routing / route rules / `server/middleware` は `//x/admin` として照合 → パスに基づくサーバー側の認可を回避 (前回の修正の不完全) | [75c12c6](https://github.com/nuxt/nuxt/commit/75c12c6fb4c22ec2cbde0051da24776d2dffa868) | 未認証・不完全修正 |
| CVE-2026-124726 | Apache APISIX 3.19.0 以上 3.20.0 未満 (openapi-to-mcp) | CWE-23, 441 / CVSS4 6.9 | MCP のツールの呼び出しで、OpenAPI 文書が宣言していないパスを相対パスで指定 → Route の資格情報付きで未宣言の API に到達 | [advisory](https://seclists.org/oss-sec/2026/q4/697) (commit 不明) | MCP / EPSS 0.005 |
| CVE-2026-128049 / GHSA-grrq-9gq2-vm55 | OpenMage Magento LTS 20.18.2 未満、21.0.0-beta3 未満 | CWE-352 / 9.0 | OAuth の `confirm` / `confirmSimple` が GET を受け、form key を確かめない → ログイン中の管理者に URL を踏ませて攻撃者の request token を承認させ、被害者の永続的な REST API トークンを取得 | [1f83e49](https://github.com/OpenMage/magento-lts/commit/1f83e49b60e08aa7ba89dcc2d41ea21f62c0b796) | EC・管理者権限 |
| CVE-2026-128069 / GHSA-h7wh-q2qr-458c | rails-html-sanitizer 1.7.2 未満 | CWE-362, 79 / 4.7 | `SafeListSanitizer` が 1 つの `PermitScrubber` を全呼び出しで共有し、`tags` / `attributes` を同期なしで書き換える → マルチスレッド (Puma) で別の要求の緩い allowlist が混ざり XSS | [15f764c](https://github.com/rails/rails-html-sanitizer/commit/15f764c3563d5dd9b97ad32eaa7454577ccec4b9) | 共有状態の競合 |
| CVE-2026-128080 / GHSA-3v2p-hm54-8qcq | @opentelemetry/instrumentation-http 0.204.0 以上 0.222.0 未満 | CWE-532 / 5.8 | クライアント span では URL のクエリを伏せるが、サーバー span の `url.query` は生のまま → 受けた要求の署名付き URL (AWS の presigned、Azure SAS の `sig`) がトレースの送信先に平文で出る | [e086dec](https://github.com/open-telemetry/opentelemetry-js/commit/e086dec7f9304107ef6d50b5877be88895c06aa7) | 秘密情報の漏えい |
| CVE-2026-128087 / GHSA-9264-jvgf-6w2f | russh (crates.io) 0.55.0 以上 0.65.1 未満 | CWE-696 / 3.7 | 初回の鍵交換で、`kex_done()` コールバックに共有秘密を渡したあとで `check_server_key()` を呼ぶ → 拒否されるはずのサーバーでも、アプリ側の鍵導出や副チャネルの初期化が先に走る | [43a46d6](https://github.com/Eugeny/russh/commit/43a46d67a80a7355fcd2fb25e7e00d79aec8184c) | 順序のバグ |
| CVE-2011-10042 | HTTP::Session (Perl) 0.43 未満 | CWE-93 / - | Cookie のセッション ID が `HTTP::Session::Store::Memcached` でそのままキーになる → CR/LF でコマンドを区切り、memcached に任意のコマンドを注入 | [039345d](https://github.com/tokuhirom/http-session/commit/039345db9bc9311868019fde67b89c355114a3d3) | 2011 年の修正に今回 CVE 採番 |
| CVE-2026-129114 ほか 6 件 | JSON::XS (Perl) 4.05 未満 | CWE-787 ほか / - | `incr_parse` で 1 バイトの断片を足すときに heap を 1 バイト越えて書く。ほかに `incr_skip` のバッファ長の破壊、`allow_tags` での解放済みスタックの読み取り、拒否した文字列やキーの断片の漏えい | [advisory](https://seclists.org/oss-sec/2026/q4/706) (commit 不明、cvs.schmorp.de) | パーサの境界 |
| (CVE 申請中) | Vim 9.2.1346 未満 (ftplugin/ps1.vim) | CWE-78 / Low | `K` の引数を PowerShell の `'...'` に入れるとき ASCII の `'` だけ二重にし、PowerShell が単引用符として扱う U+2018〜201B を見落とす → 細工した .ps1 の行で `K` を押すとコマンド実行 (GHSA-r5v6-q6j8-8qw2 の不完全な修正) | [advisory](https://seclists.org/oss-sec/2026/q4/708) (commit 不明) | 不完全修正 |

### 今日の CVE 所感

- **「同じ入れ物に入った別の種類のトークン」**: Rucio の challenge トークンと認証トークンの混同は、「短命の nonce」と「本物のセッション」を同じテーブルで管理して、検証の関数が種類を見ない、という型だ。パスワードのリセット用トークン、メール確認用トークン、MFA の途中のトークンを、同じ検証の関数が受け付けてしまう実装は多い。診断では、認証の途中で発行されるトークンを、そのまま他の API の `Authorization` に入れて試す価値がある。
- **「既定の甘い部品 + 非既定の設定」**: Shiro の `AllowAllCredentialsMatcher` は、LDAP の bind に判断を任せる前提の部品で、キャッシュを有効にした瞬間に前提が崩れる。キャッシュを足すと検証の経路が変わる型は、Spring Security の `UserCache` や独自の認証キャッシュにも水平展開できる。
- **「パーサの食い違い」**: Nuxt の `//x/admin` は、ページの描画と middleware で URL の解釈が違う、という典型だ。前回の修正 (ドットのセグメント) の直後に別の形で破られた。Next.js、SvelteKit、Remix など、描画とサーバーのルーティングが別の層にあるフレームワークで、同じ入力 (`//host/path`、`/%2e%2e/`、`\`) を試したい。
- **「エージェントのツールの引数 = 攻撃者の入力」**: APISIX の openapi-to-mcp と Telerik の AI ツールのパストラバーサルは、同じ週に出た同じ型だ。MCP のツールを自動生成するゲートウェイを診断するときは、ツールの引数にパスの区切りや `..` を入れたときの到達先を必ず見る。
- 優先して見るべき製品: **Rucio** (研究機関のデータ管理で使われる。未認証で管理者)、**sysPass** (パスワード管理なので侵害の影響が大きい)、**Dokploy** (セルフホストの PaaS。組織の一般メンバーから root)、**Shiro** (国内の業務系 Java)。

## 日本国内のセキュリティ動向

### 国内インシデント・事故

#### [2026-11-13 報道] 大阪市: アララのメール配信サービスへの不正アクセスで、行政オンラインシステムの利用者のメールアドレス 100 万件超が漏えい
- **何が起きたか**: The Record によると、大阪市は、行政オンラインシステムを保守する TKC が使っていたアララのメール配信サービスに不正アクセスがあり、100 万件を超えるメールアドレスが漏れたと公表した。2026 年 7 月から 10/31 までに、このシステムからメールを受け取った人のアドレスが対象だという。市は、約 280 万人の市民に、市を装う不審なメールの URL や添付ファイルを開かないよう呼びかけた。大阪市は 11/3 の時点で「漏えいの可能性」を公表しており、システムは 10/31 17:40 ごろからメールを送れない状態が続いていた。アララによると、11/2 の攻撃で約 400 の顧客の 7,700 万件のメールアドレスが漏れ、配信サービスからカード会社や金融機関を装うメールが数百万通送られた。
- **なぜ重要か (評価)**: 行政のシステムの本体ではなく、保守事業者が使う外部の配信サービスが入口になった。自治体の委託先の管理で、「再委託先の SaaS」まで追えているかが問われる。
- 出典: [The Record (2026-11-13)](https://therecord.media/city-of-osaka-japan-email-data-breach) / [SmartScope (11/3 の第一報の要約)](https://smartscope.blog/blog/osaka-city-administrative-online-system-potential-leak-user-2026/)

#### [2026-11-13] paiza: 開発用のステージング環境のアクセス管理が 2013 年から不備で、最大 90 万 2,576 件の個人情報がアクセスされ得る状態だった
- **何が起きたか**: paiza は、動作検証の環境で、ベーシック認証などのパスワードを固定の文字列のまま長く使い、退職者など過去に権限を持っていた人が外から接続できる状態だったと公表した。対象は、ユーザー ID、GitHub ID、生年月日、学歴・職歴、スキルチェックや学習の記録、求人への応募の履歴、取引先の担当者の情報など。本番のデータを複製する際のマスク処理が、一部の項目と期間で行われていなかった。期間は環境を作った 2013 年から、遮断した 2026/8/13 まで。7/17 の行政機関からの照会で発覚した。11/13 の時点で、実際の流出や悪用は確認されていないという。
- **なぜ重要か (評価)**: 本番が攻撃されたのではなく、「ステージングに本番のデータ + 共有のベーシック認証」という、国内でとても多い構成の事故だ。診断の範囲から外されがちな検証環境こそ、本番と同じ扱いで見る必要がある。GitHub ID と応募の履歴の組み合わせは、エンジニアを狙う偽の求人 (北朝鮮の手口など) に使われうる。
- 出典: [セキュリティ対策Lab (2026-11-13)](https://rocket-boys.co.jp/security-measures-lab/paiza_staging_personal_information_engineer_risks_20261113/)

#### [2026-11-13] アットホーム: 不動産会社向けの「賃貸管理システム」の管理サイトに不正ログイン。入居者・オーナー・取引先の 6,901 件に漏えいのおそれ
- **何が起きたか**: アットホームは、11/9 に賃貸管理システムの管理サイトが不正アクセス・不正ログインを受け、加盟の不動産会社が登録した入居者、オーナー、取引先の個人情報 6,901 件が漏れた可能性があると発表した。項目は氏名、生年月日、電話番号、住所、建物名、部屋番号、契約の状況など。口座情報の漏えいは確認されておらず、カード情報はこのシステムにない。11/12 に個人情報保護委員会、JIPDEC、JUAS に報告した。不正ログインに使われた認証情報の入手経路は説明されていない。
- **なぜ重要か (評価)**: 「物件名と部屋番号と契約の状況」が揃うと、管理会社を装って家賃の振込先の変更を求める詐欺に使いやすい。SaaS の管理サイトへの不正ログインが続いており、加盟店のアカウントの多要素認証の有無が焦点になる。
- 出典: [セキュリティ対策Lab (2026-11-13)](https://rocket-boys.co.jp/security-measures-lab/athome_rental_management_unauthorized_access_6901_2026/)

#### [2026-11-13] [続報] GMO インターネットグループ: 「お名前.com デスクトップクラウド」の侵害で、約 30.5 億円の業績への影響を見込む
- **何が起きたか (前回からの差分)**: GMO インターネットグループは決算説明会で、10〜12 月期に約 30.5 億円の影響を計上する見込みだと明らかにした。不正アクセスによる不正取引の損失の補填として約 29 億 9,800 万円の申請を受け付けている (申告額で、確認して確定する)。利用者への一律 5,000 円の見舞金は、11/12 の時点で約 5,400 万円の申し込みがあり、最大 1.3 億円になる。個人情報が公開された場合の特別見舞金 (1 件につき上限 300 万円) は、1 件の公開を確認した。犯人の逮捕につながる情報への懸賞金は総額 100 万ドル。別に上限 11 億円の保険がある。
- **なぜ重要か (評価)**: 国内のクラウド事業者の侵害で、補償の総額が具体的な数字で出た珍しい例だ。リモートデスクトップの基盤を預ける委託先の評価で、補償と保険の規模も比べる材料になる。
- 出典: [日経クロステック (2026-11-13)](https://xtech.nikkei.com/atcl/nxt/news/24/03471/)

#### [2026-11-13] [続報] NTT スマイルエナジー「エコめがね」(第 3 報): 原因はソフトウェアの脆弱性の悪用。個人情報の外部流出の痕跡はなし、再開は 12 月上旬の目安
- **何が起きたか (前回からの差分)**: NTT スマイルエナジーは、10/28 の不正アクセスの原因が、ソフトウェアの脆弱性の悪用だったと発表した (どの脆弱性かは示していない)。第 2 報で伝えた「スマイル e ポイント」の不正な読み取りと交換とは別に、個人情報の外部流出の痕跡は今のところないという。10/29 に外部との通信を切り、クラウドの全サーバーを止めている。太陽光発電の設備の発電・売電には影響がない。「自家消費エコめがね」「ちくでんエコめがね」は 12 月上旬ごろの再開を目安とし、「全量」「余剰」は一部の機能を先に戻す。
- **なぜ重要か (評価)**: 太陽光の監視サービスは、家庭の発電設備と事業者のクラウドをつなぐ。復旧まで 1 か月以上かかる見通しで、IoT のクラウドを止めたときの代わりの手段の用意が問われる。
- 出典: [PR TIMES (NTT スマイルエナジー、2026-11-13)](https://prtimes.jp/main/html/rd/p/000000144.000005498.html)

### 国内の注意喚起・ガイドライン・政策

> 期間内 (金曜午後〜週末) に、JPCERT/CC の注意喚起、IPA の重要なセキュリティ情報、国家サイバー統括室・個人情報保護委員会の新しい発表は確認できなかった。

#### [2026-11-13] フィッシング対策協議会: 9 月の報告は 9 万 4,661 件で 2 か月連続の増加。悪用された URL も 23.2% 増
- **何が起きたか**: Security NEXT によると、9 月にフィッシング対策協議会に寄せられた報告は 9 万 4,661 件で、8 月の 8 万 2,338 件から約 15.0% 増えた。1 日あたり約 3,155 件。分野は EC 関連が約 47.9%、クレジット・信販が約 35.0%、官公庁が約 5.2%、航空が約 4.6%。悪用された URL は 4 万 9,032 件で、前月の 3 万 9,800 件から約 23.2% 増えた。
- **なぜ重要か (評価)**: 9 月の数字で、10 月以降のアララ経由の大量のなりすましメールはまだ入っていない。10〜11 月の数字は大きく跳ねるとみる。
- 出典: [Security NEXT (2026-11-13)](https://www.security-next.com/191657)

#### [2026-11-14] IPA に聞く「パスワードを紙で管理する」ことの是非: ダイソーの「パスワード管理ノート」が品薄に
- **何が起きたか**: ITmedia NEWS によると、情報漏えいが相次ぐなか、ダイソーの紙の「パスワード管理ノート」が品薄になっている。ダイソーは、ネットにつながらない紙で管理する安心感が改めて注目されているとした。記事は IPA にリスクを聞いている。
- **なぜ重要か (評価)**: 漏えいの報道の多さが、利用者の行動を変え始めている。社内の啓発では、紙かデジタルかよりも、「使い回しをしない」「多要素認証を有効にする」を優先して伝えたい。
- 出典: [ITmedia NEWS (2026-11-14)](https://www.itmedia.co.jp/news/article/2611/14/2000003193/)

#### [2026-11-13 報道] 海外メディアが見た日本の状況: NTT の松原氏「10 月だけで今年の報告件数の 58%」「今年盗まれた個人情報は約 3 億 8,000 万件」
- **何が起きたか**: The Record は大阪市の件と合わせ、日本の状況をまとめた。NTT のチーフサイバーセキュリティストラテジストの松原実穂子氏は、日本のシステムへの攻撃は 7 月から増え、10 月に急増したと述べた。10 月の件数は今年報告された事案の 58% にあたり、今年盗まれた個人情報は約 3 億 8,000 万件に上る。ダークウェブではすでに大量の日本人の個人情報が売られ、一部は証券の不正取引に使われたという。記事は、高市首相が閣僚会議で決めた緊急対策 (約 6,200 万ドルの緊急予算、防御での AI の活用、被害者の支援など) にも触れた。
- **なぜ重要か (評価)**: 国内の事案の多さが、海外の報道でも「日本の危機」として扱われている。FBI の ARTEX の警告 (AI セキュリティの項) も、日本の金融機関が狙われたことに触れており、国内の金融・行政は海外の脅威情報の当事者になった。
- 出典: [The Record (2026-11-13)](https://therecord.media/city-of-osaka-japan-email-data-breach)

### 国内製品の脆弱性 (JVN)

> 期間内に、国内ベンダーの製品の JVN# / JVNVU# の新規公開はなかった (11/13 公開分の YouTrack、TightVNC / UltraVNC、ImageMagick、PromZard、ComfyUI-Easy-Use は前号で既報)。以下は 11/13 に JVN iPedia に登録された、国内でも使われる海外製品から選んだ。

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| 2026-11-13 | JVNDB-2026-043356 / CVE-2026-118039 | Telerik Document Processing Libraries (2026.3.1027 より前) / Progress | 入れ子の SVG を埋め込んだ細工した SVG の処理や PDF への書き出しで XXE が起き、未認証でサーバーのローカルファイルを読める | 7.5 / 情報漏えい | [JVN iPedia](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-043356.html) |
| 2026-11-13 | JVNDB-2026-043357 / CVE-2026-118038 | 同上 (Convert / Merge の AI エージェント用ツール) | ツールの引数で出力先の外のファイルを読み、相対パスで上書きもできる | 7.1 / 任意ファイルの読み書き | [JVN iPedia](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-043357.html) |
| 2026-11-13 | JVNDB-2026-043295 / CVE-2026-123836 | JetBrains Datalore 2026.4 より前 | ワークスペースの共同作業者が、Git のバックアップを通じて所有者の SSH 秘密鍵を取得できる (リンクの解釈の不備) | 8.8 / 秘密鍵の漏えい | [JVN iPedia](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-043295.html) |
| 2026-11-13 | JVNDB-2026-043305 / CVE-2026-123285 | JetBrains Datalore 2026 年 3 月より前 | JVM オプションの注入で、データベースのタスクのコンテナ内でコマンドを実行できる | 8.8 / コード実行 | [JVN iPedia](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-043305.html) |
| 2026-11-13 | JVNDB-2026-043341〜043346 / CVE-2026-105614〜105620 | PostgreSQL Anonymizer 3.3.0 より前 / Dalibo | ルール内のサブクエリ、`security_invoker` のビュー、親テーブル経由、準備済みのプランでマスクが効かず、元のデータを読める (ほかにメモリ枯渇) | 4.3〜6.5 / マスクの回避 | [JVN iPedia](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-043342.html) |
| 2026-11-13 | JVNDB-2026-043170 / CVE-2026-86378 | Dell PowerProtect Data Domain (7.7.1.0〜8.8 ほか) | スタックベースのバッファオーバーフロー | 8.8 / バックアップ基盤 | [JVN iPedia](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-043170.html) |
| 2026-11-13 | JVNDB-2026-043317 / CVE-2026-116663 | Tanium Enforce | 不適切なアクセス制御 (認証の欠如) | 6.5 / 情報漏えい | [JVN iPedia](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-043317.html) |

- 補足: PostgreSQL Anonymizer は、本番のデータを開発・検証の環境に渡すときのマスクに使われる。paiza の件 (国内インシデントの項) のように「マスクしたつもりのデータ」が検証環境で漏れる事故が続いているので、使っている組織は 3.3.0 以上に上げたい。

### 国内コミュニティ・研究・イベント

#### [2026-11-14] クラスメソッド: 「Cognito の自己サインアップが有効だと、誰でも AWS の一時認証情報を取得できる」— ARTEX の事例と確かめたい設定 3 点
- **何が起きたか**: クラスメソッドの西村氏は、Datadog Security Labs が 11/9 に報告した ARTEX の AWS での攻撃を題材に、S3 + Cognito ユーザープール + ID プールの SPA の構成を解説した。エージェントは、自己サインアップが有効でアプリクライアント ID がフロントから分かるユーザープールに登録を試み、拒否されても続けて登録した。得たトークンを AWS の一時認証情報に換え、アカウントの中を探った。確かめる点として、`AllowAdminCreateUserOnly`、認可に使う属性 (`custom:isAdmin` など) をアプリクライアントの `WriteAttributes` で利用者が書けないか、ID プールの認証済みロールの権限の 3 つを挙げた。
- **なぜ重要か (評価)**: 脆弱性ではなく設定の組み合わせで成立するので、スキャナーでは出にくい。AWS の診断で、Cognito を使う SPA を見るときのチェックリストにそのまま使える。
- 出典: [DevelopersIO (2026-11-14)](https://dev.classmethod.jp/articles/cognito-self-signup-agentic-attack/)

#### [2026-11-14] Zenn: 「ログインが会員の有無を 127 倍の時間差で漏らしていた」— 文字列比較より、ユーザーが存在するときだけ `password_verify` を呼ぶ書き方が問題
- **何が起きたか**: 筆者は PHP 8.5.6 と Python 3.9.6 で、比較の時間差を測った。64 バイトの秘密値では、PHP の `===` の差は約 1.3 ns で、ループバックの HTTP 越しでは見えなかった。一方、ユーザーがいるときだけ bcrypt (コスト 10) で照合する、よくある早期 return の書き方では、存在するユーザーとしないユーザーの応答時間に 127 倍の差が出た。対策として、ユーザーがいないときもダミーのハッシュで照合することを示した。
- **なぜ重要か (評価)**: ユーザー列挙は診断でよく「低」とされるが、ARTEX のようなエージェントは列挙した ID でパスワードスプレーを自動で続ける。ログインの応答時間の差は、ブラックボックスの診断ですぐ試せる項目だ。
- 出典: [Zenn (2026-11-14)](https://zenn.dev/tlaboratory/articles/login-timing-leak-dummy-hash)

#### [2026-11-14] Zenn: SonarQube の「Hunter Agent」の仕組みと導入の条件 — SAST の外側を AI で探す
- **何が起きたか**: 筆者は、SonarQube のルールでは拾えない問題を AI のエージェントで探す Hunter Agent の仕組みと、導入の条件を解説した。同じ筆者は、リポジトリに現れない層 (コンテナのイメージ) を調べるコンテナスキャンの記事も出している。
- **なぜ重要か (評価)**: ソースコード診断の現場で、SAST と LLM の探索をどう組み合わせるかの実例になる。前号の「LLM の書き換えで CodeQL の警告が消える」研究と合わせ、AI の結果を「見逃しの補完」に使い、判定の根拠にはしない運用が要る。
- 出典: [Zenn (2026-11-14)](https://zenn.dev/r_goto/articles/sonarqube-hunter-agent)

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 95 (RSS/Atom 約 80、OSV の modified_id.csv 8 エコシステム、NVD API、CISA KEV、EPSS、Security NEXT の記事 ID の走査 281 件、WebSearch 12 クエリ)
- 採用件数: AI技術=12 / AIセキュリティ=6 / セキュリティ=8 / CVE=14 / 国内インシデント=5 / 国内政策=3 / JVN=7 / 国内コミュニティ=3
- 除外理由内訳: 古すぎ=約 30 (ScanNetSecurity の 11/13 掲載分の多くは 10〜11 月前半の発表の再掲 [ApplyNow 11/4、ブックオフ、ノジマ、ネットマイル、ARTPASS など]、Full Disclosure の Home Assistant [11/8]・Open WebUI [11/5]・AI のソースコード解析の回避 [11/6]・Revive Adserver [11/12]、Synology DSM [ベンダー公表 11/10]、Lovable の 15 万 9,041 プロジェクトの調査 [Handelsblatt 報道 11/2、英語版の公開日は不明]、非営利団体による AI 各社への提訴 [米国 11/12]) / 重複=約 40 (Check Point CVE-2026-123039 と UnrealIRCd の KEV、FaceStealer と Binance の差し押さえ、Operation Endgame、SCKit、Apify、Gemini 4 Hydrogen、ChatGPT Wallet、Daybreak、良品計画、マネックス証券、KARTE、CSC、M365 の障害の第一報、Git 2.56.1、GitLab の Critical パッチ、WebSAM WinShare、FortiMail、NetScaler、Pall Mall Process、Nexus Repository の CVE-2026-113368/113373、Tanium Threat Response の CVE-2026-116650/116651、Barracuda ESG など) / 日付不明=約 5 (ハンゲ「第 4 報」[公式ページが 429 で確認できず]、UT Arlington の件、ArcticRAT [Dark Reading 本文が 403]、伊当局の Meta への罰金 [Reuters 本文を取得できず])
- 取得失敗ソース: GitHub Advisories の Atom (249 バイトの空応答 → OSV の modified_id.csv と api.osv.dev で代替)、Dark Reading の記事本文 (403 / Cloudflare のチャレンジ → RSS の説明文のみ確認し不採用)、MarkTechPost (チャレンジ → 不採用)、Reuters (JS 必須 → 不採用)、ENSAPIA Tokyo (429)、トレンドマイクロ日本の RSS (空応答)、JPCERT/CC・IPA の RSS (期間内の新規項目なし)、Microsoft Security Blog の SCKit 記事 (本文の抽出に失敗、既報のため不採用)。Apache Shiro・APISIX・JSON::XS・Vim の修正コミットは特定できず、advisory の URL で代用した。

</details>
