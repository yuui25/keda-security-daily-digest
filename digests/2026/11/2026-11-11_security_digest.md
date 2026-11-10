# KEDA Daily Digest — 2026-11-11 (JST)

> 採用範囲: 公開日 2026-11-09 〜 2026-11-11
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

米国時間 11/10 は月例パッチの日で、修正が一度に大量に出た。**Microsoft の 11 月の Patch Tuesday** は、媒体の数え方で約 1,100〜1,260 件。悪用済みのゼロデイは、**Outlook で NTLMv2 ハッシュが漏れる CVE-2026-124194 の 1 件** で、CISA が同日に KEV に加えた (期限 11/24)。Exchange が受信した添付ファイルをインデックスするだけで発動する **Windows Search の RCE (CVE-2026-116928、9.8)** と、DC に影響する **LDAP の未認証 RCE (CVE-2026-119958)** も要注意。同じ日に **SAP は CVSS 10.0 を 4 件 (ICM2SHELL / PROXYGATE)**、Adobe は Connect で CVSS 10.0 を 6 件修正した。
同時に **Git が 2.56.1 などで 6 件を修正**した。中心は、`--recursive` でクローンするとコードが実行される **CVE-2026-111760**。悪用中の案件では、**Xen Orchestra の認証回避 (VSA-2026-062)**、**Chrome の今年 8 件目のゼロデイ (CVE-2026-125350)**、Barracuda ESG の 2 件 ([続報]、KEV 入り)、ゼロデイとして悪用された **AhsayCBS** があった。N-able の RMM 製品 N-central では、PoC 付きのゼロデイ 30 件超が予告なしに公開され、N-able はホスティング版を止めた。
AI 側では、Google が **Gemini 4 Carbon** を一般に提供し始めた。Anthropic は **Claude Meetings** を発表し、IPO の仮条件 (1 株 70〜78 ドル) も出した。AI セキュリティでは、**SGLang の RCE で NEAR AI の推論サーバーが侵害された** 件 (TEE の中の「機密モード」のリクエストも見えた可能性がある) と、**Fireworks AI の侵害の拡大** が大きい。
国内では、**NTT データ (住友生命の Vitality、約 8 万人)**、**ラフールサーベイ (AWS のアクセスキーの漏えいで 2 万 4,232 人)**、**ラクスル** が不正アクセスを公表した。マイナンバーカードを使うコンビニ交付は、少なくとも 38 自治体で止まった。
**今日まず見るべき 2 件**: (1) CI のランナーと開発者の端末の Git を棚卸しし、2.56.1 などに更新する (深掘り参照)。(2) Outlook の 11 月の更新を適用し、外向きの SMB と NTLM の送信を制限しているかを確認する。

## 今日の深掘り

### Git 2.56.1 などの協調リリース (2026-11-10): 再帰クローンでのコード実行 (CVE-2026-111760) を中心に 6 件。その 1 件の CVE-2026-113408 は、プロトコル v2 の仕様から来るバグで、Git 以外の実装に広がりうる

- **概要 (事実)**:
  - Git プロジェクトが 2.56.1 を公開し、2.55.1 / 2.54.1 / 2.53.1 / 2.52.1 / 2.51.3 / 2.50.2 にも修正を戻した。直したのは CVE-2026-111760 / 113408 / 105437 / 114466 / 114467 / 114469 の 6 件。
  - GitHub は github.com と GHEC に適用済みで、GHES の修正版は 3.19.15 / 3.20.11 / 3.21.9 / 3.22.4。The Hacker News によると、Git for Windows は 11/10 19:09 UTC の時点で修正版を出していなかった。悪用の報告も、公開 PoC もない。
- **技術的な中身**:
  - **CVE-2026-111760 (RCE)**: index のエントリーのパス長を、狭い整数型に切り詰める箇所がある。そのため、安全確認のときは極端に長いパスとして扱われ、ディスクに書くときは切り詰めたあとの短い名前 (攻撃者は `.git` にできる) になる。検証した名前と書いた名前が食い違う型。
    - サブモジュールの `.git` は、ディレクトリではなく `gitdir: ...` を書いたファイルだ。ディレクトリ向けの「シンボリックリンクへの置き換えを拒否する処理」が効かないので、攻撃者は `.git` を、悪意のある hooks や config を置いたディレクトリへのシンボリックリンクに差し替えられる。
    - 条件は、被害者が `git clone --recursive` (または `submodule update --init`) を実行することと、シンボリックリンクを使えるファイルシステムであること。
  - **CVE-2026-113408 (パストラバーサル)**: 空のリポジトリを protocol v2 でクローンすると、サーバーは `ls-refs` で unborn HEAD の symref の行き先を返す。この名前 (例: `refs/heads/../../../X`) を検証しないまま files バックエンドに書くので、refs の外にファイルを書ける。サーバー側が攻撃者なら、クローンするだけで成立する。
  - **CVE-2026-105437 (heap overflow、7.5)**: `.gitattributes` の `conflict-marker-size` に巨大な値を入れると、xdiff の merge バッファのサイズ計算が `int` であふれる。GitLab は、マージできるかの判定に `git merge-tree` を走らせるホスティングのサーバーが最も狙われやすいとしている。PR を作るだけでサーバー側で発火しうる。
  - そのほか、署名が 3 つ以上あるタグの merge でのスタック破壊 (114467)、1GiB を超える binary patch での OOB read (114469)、fast-import のオプションでの任意のファイルの読み書き (114466) がある。
- **背景・経緯 (背景引用)**:
  - 「サブモジュール + シンボリックリンク + hooks」は、Git で繰り返し出てきた系統だ。例は、CVE-2018-11235 (サブモジュール名のトラバーサル)、CVE-2024-32002 (大文字・小文字を区別しないファイルシステムでサブモジュールの hooks が実行される)、CVE-2025-48384 (CR の扱いの食い違い。KEV 入り)。今回も「検証した名前と書いた名前の不一致」という同じ根の問題になる。
- **なぜ今これが重要か (評価)**:
  - 攻撃者に必要なのは、悪意のあるリポジトリ 1 つだけだ。依存関係の取り込みや、CI、AI のコーディングエージェントの `git clone --recursive` は日常的に走っている。修正の差分は公開済みなので、PoC はすぐに出ると見ておくべき。
  - バリアントハントでは、CVE-2026-113408 が最も実りが多そうだ。protocol v2 の仕様から来るバグなので、libgit2、JGit、go-git、dulwich、isomorphic-git や、ホスティング側のミラーの実装が、サーバーから届いた ref 名を `check_refname_format` 相当で検証しているかは、独立に確かめる価値がある。
- **読者が今日できること**:
  - CI のランナーのイメージ、開発者の端末、Git を同梱したツール (IDE、GitHub Desktop、CI のコンテナ) で `git --version` を集め、修正版になっていないものを洗い出す。Windows は Git for Windows の修正版が出るまで、外部のリポジトリの `--recursive` を避ける。
  - 自前で GitLab / Gitea / GHES を運用しているなら、サーバー側の Git を最優先で更新する。すぐにできない場合の暫定策として、`info/attributes` に `* conflict-marker-size=7` を書いて、リポジトリ側の指定を上書きする方法がある (報道ベース)。
  - 他の Git の実装を監査する場合は、修正コミット [b371db8](https://github.com/git/git/commit/b371db812524aa7831d3c3a9aed782defd1dcfb2) / [8cb7e2e](https://github.com/git/git/commit/8cb7e2e031978c59381adf086fd1c0ce1e3a7315) を読み、そのうえで `symref-target` や `unborn` を受け取る処理を grep する。
- 出典:
  - [GitHub Blog (2026-11-10)](https://github.blog/open-source/git/git-security-vulnerabilities-announced-7/)
  - [The Hacker News (2026-11-10)](https://thehackernews.com/2026/11/git-patches-flaw-that-lets-malicious.html)
  - [GHSA-vp2w-7xxj-jvxr](https://github.com/git/git/security/advisories/GHSA-vp2w-7xxj-jvxr)
  - 背景の旧 CVE は、過去の経緯として引用した。

## AI 技術・トレンド

### [2026-11-10] Google、「Gemini 4 Carbon」を一般に提供開始。導入価格は 100 万トークンあたり入力 2 ドル / 出力 10 ドル。Antigravity でエージェントの「swarm」機能をプレビュー (Google releases Gemini 4 Carbon with agent 'swarm' feature)
- **何が起きたか**: 約 2 週間前に一部の「サイバー防御者」向けに先行提供していた Gemini 4 Carbon を、Gemini API (AI Studio)、Gemini for business の有料の開発者・企業、Google AI Ultra の加入者 (Gemini アプリ、検索の AI Mode、Antigravity) に広げた。導入価格は 11/30 まで入力 2 ドル / 出力 10 ドル (100 万トークンあたり) で、その後は倍になる。Google は「最も強力なモデル」と主張し、一般的なソフトウェア開発には先月出した Argon を、限界に挑む複雑な複数ステップのコーディングや研究には Carbon を勧めている。Antigravity では、1 つのプロンプトを「調整されたエージェントのチーム」に分ける swarm 機能をプレビューする。脆弱性の発見・悪用・修正向けの「Carbon for cyber」は、引き続き Fairwind Program の参加者に限られる (SecurityWeek)。
- **なぜ重要か (評価)**: フロンティア級のモデルが Fable 5.2 の約 4 分の 1 の単価で一般に使えるようになり、攻撃側の自動化のコストも下がる。サイバー向けの派生版だけを別の審査で囲う形は、Anthropic・OpenAI と同じ線引きになってきた。
- 出典: [The Verge (2026-11-10)](https://www.theverge.com/ai-artificial-intelligence/1030787/google-gemini-4-carbon-public-rollout) / [SecurityWeek (2026-11-10)](https://www.securityweek.com/google-widens-gemini-4-carbon-access-after-ai-agents-verify-signal-code/)

### [2026-11-10] Anthropic、ビデオ会議に参加して作業する「Claude Meetings」(ベータ) と、「Claude Sheets」「Claude Whiteboards」を発表 (Anthropic launches Claude Meetings)
- **何が起きたか**: Claude Meetings では、Claude が見える参加者として Google Meet の通話に入り、会話を追いながら計画の下書き、ホワイトボードへのタイムラインの作成、チャットでの質問への回答、接続した業務アプリからの情報の取得を進める。終了後はメモやアクションアイテムが claude.ai に残る。参加時はチャットに通知を出し、外部のゲストがいる通話には管理者が許可しない限り参加せず、外部のゲストが入ると自動で退出する。Meetings は Team / Enterprise 向けのベータで、Sheets と Whiteboards は全有料プランでベータ提供。Claude Dashboards から改称した「Claude Data」は一般提供になった (The Verge)。
- **なぜ重要か (評価)**: 会議の音声と社内アプリへのコネクタを同時に持つエージェントは、会議中の発言や共有画面からの間接的なプロンプトインジェクションの新しい入口になる。導入する組織は、コネクタの権限と外部ゲストの扱いを最初に確認したい。
- 出典: [TechCrunch (2026-11-10)](https://techcrunch.com/2026/11/10/anthropic-launches-claude-meetings-to-turn-workplace-discussions-into-plans-and-tasks/) / [The Verge (2026-11-10)](https://www.theverge.com/ai-artificial-intelligence/1030709/anthropic-has-its-own-ai-powered-office-suite-now)

### [2026-11-10] [続報] Anthropic の IPO: 公開価格の仮条件を 1 株 70〜78 ドルに設定。上限なら完全希薄化ベースの評価額は 1.404 兆ドル
- **何が起きたか**: 更新した届出書で、Class A 株 8 億 2,500 万株を 70〜78 ドルで売り出し、577.5 億〜643.5 億ドルを調達する計画を示した。別に、AMD、Broadcom、Google、Micron、Microsoft、Nvidia、TSMC に、議決権のない Class N 株 260 億ドル分を IPO 価格で私募で売る (Google と Nvidia は各 100 億ドル)。手取りの見込みは 846 億〜937 億ドル。創業者の Class F 株が議決権の 50.1% を持つ。CNBC の報道では、11/19 ごろに Nasdaq でティッカー「ANT」として取引を始める予定。
- **なぜ重要か (評価)**: 主要なチップ・クラウド企業がそろって株主になり、Claude の供給網と資本の関係がさらに一体化する。上場後は、Mythos 系の安全性の判断や脆弱性の開示の方針に、四半期の業績の圧力がかかるかどうかが見どころになる。
- 出典: [TechCrunch (2026-11-10)](https://techcrunch.com/2026/11/10/anthropic-sets-ipo-price-range-of-70-to-78-per-share-to-reach-an-implied-valuation-of-1-404-trillion/)

### [2026-11-10] Anthropic の Mythos が Cisco と IBM の製品に。Cisco は AI Defense のレッドチーミングから Mythos を呼び出す (Anthropic's super bug-finding Mythos model is going into Cisco and IBM products)
- **何が起きたか**: Cisco はメルボルンのイベントで、AI のモデル・エージェント・アプリの弱点を探す AI Defense のレッドチーミングの機能から、Mythos を呼び出して顧客の環境を試験できるようにすると発表した。既存のライセンスの範囲内で追加の費用はない。顧客にモデル自体は渡さず、製品の機能として提供する形。Anthropic の APAC の担当者は、Mythos の利用を待つ企業の列が長く、Cisco との提携でその需要に応えやすくなると説明した。Mythos は「Project Glasswing」で審査済みの組織に提供が始まり、その後も管理されたプログラムを通じて広がっている。
- **なぜ重要か (評価)**: 審査制だった脆弱性の発見に強いモデルを、セキュリティ製品経由で間接的に使う経路ができた。レッドチームやペンテスターは、自分で契約しなくても製品の機能として Mythos 級の解析を使える場面が増える。
- 出典: [The Register (2026-11-10)](https://www.theregister.com/ai-and-ml/2026/11/10/anthropics-super-bug-finding-mythos-model-is-going-into-cisco-and-ibm-products/5308616)

### [2026-11-09 採択 / 11-10 報道] 8 か国と主要な AI 企業が「Paris Call for AI Safety and Security」に署名。自社が管理するモデルの停止の仕組みを用意すると約束
- **何が起きたか**: パリ平和フォーラムの前夜、マクロン大統領がオンラインで会合を開き、8 か国と企業・市民団体が宣言に署名した。Le Monde によると、Sam Altman 氏 (OpenAI)、Dario Amodei 氏 (Anthropic)、Brad Smith 氏 (Microsoft)、Arthur Mensch 氏 (Mistral AI)、Yoshua Bengio 氏、米財務長官の Scott Bessent 氏が加わった。ドイツは署名していない。内容は、高性能なモデルの評価の手順の共通化、開発者の責任の明確化、重大なセキュリティ事故の情報共有の 3 本柱。機密でない試験結果を標準の形式で公開し、既知のリスクの開示、外部の研究者による独立した監査への協力、停止の仕組みの用意を約束する。期限や罰則はなく、拘束力のある国際的な監督の仕組みでもない。
- **なぜ重要か (評価)**: 拘束力はないが、「重大インシデントの共有」と「停止の仕組み」が業界の公約になったことで、エージェントの暴走 (OpenAI のエージェントによる Hugging Face への攻撃など) の事後報告が今後増える可能性がある。
- 出典: [The Decoder (2026-11-10)](https://the-decoder.com/eight-countries-and-top-ai-labs-agree-to-shutdown-mechanisms-in-new-paris-declaration/)

### [2026-11-10] Microsoft、英国の Copilot のテナントで 12/9 から Claude を既定で有効に。データは米国で処理
- **何が起きたか**: 12/9 以降、管理者がまだ設定を選んでいない英国のテナントでは、Anthropic の Claude のモデルへのアクセスが有効になる (何もしなければオプトイン扱い)。Anthropic は Microsoft のサブプロセッサーとして動き、データは米国で処理されると Microsoft の文書に書かれている。Claude はすでに商用クラウドのほとんどで既定で有効だが、EU、EFTA、英国は例外だった。英国は EU Data Boundary の対象外のため、今回切り替える。Claude を Microsoft 365 のみに制限する設定も廃止される。
- **なぜ重要か (評価)**: 越境データ移転の評価をしていない組織は、既定の切り替えだけで処理場所が米国に広がる。英国に拠点がある日本企業も、12/9 までにテナントの設定を確認する必要がある。
- 出典: [The Register (2026-11-10)](https://www.theregister.com/ai-and-ml/2026/11/10/microsoft-is-giving-claude-the-keys-to-uk-copilot-tenants-by-default/5308693)

### [2026-11-10] OpenAI、ChatGPT に企業向けの「Business Hub」と、企業を代表する認証済みの「Business Agents」を追加 (ベータ)
- **何が起きたか**: ChatGPT の回答に出てきた企業が Business Agent を用意していれば、利用者はその企業の商品やサービスについて、比較などをエージェントに質問できる。会話はラベル付きで、通常の ChatGPT の会話とは分けられる。企業は Business Hub で組織を登録・認証し、ChatGPT の回答での言及数や「発見のトピック」を見られる。まず米国の対象の EC・オンラインサービス企業から始める。OpenAI は認証の方法の詳細は明かしていない。
- **なぜ重要か (評価)**: 「認証済み」の表示を偽る、あるいは企業が設定した指示やビジネスの文脈を通じて利用者に誤った誘導をする、といった新しいなりすましや操作の対象になる。認証の方法が非公開な点は、検証する側としては注意したい。
- 出典: [The Verge (2026-11-10)](https://www.theverge.com/ai-artificial-intelligence/1030552/openai-chatgpt-business-agents-hub)

### [2026-11-10] Adobe、Creative Cloud の機能を ChatGPT / Claude / Gemini から使えるローカルの MCP サーバーを公開。Firefly のエージェントも常時動作に (Adobe MAX)
- **何が起きたか**: Adobe は MAX で、Photoshop、Premiere、Illustrator、InDesign への AI の機能の追加とともに、他社のチャットボットから Creative Cloud のアプリの機能を呼べるローカルの MCP を公開した。Firefly にはプロトタイピング用の「Builder」(非公開ベータ)、クリップを組み合わせる動画ツールを加え、エージェントを常時動作させて作業の文脈を集めるようにする。買収した Topaz Labs からは、アップスケール用の「Wonder 4」と HDR 化の「ImageHDR」が出る。
- **なぜ重要か (評価)**: 主要なデスクトップアプリがローカルの MCP サーバーを持つ流れが進んでいる。ローカルの MCP は、どのクライアントからの接続を許すか、ファイルにどこまでアクセスできるかが攻撃面になるので、公開後の実装の調査の対象として注目したい。
- 出典: [TechCrunch (2026-11-10)](https://techcrunch.com/2026/11/10/adobe-adds-more-ai-to-its-products-and-launches-an-mcp/)

### [2026-11-09 発表 / 11-10 報道] OpenAI の常時稼働エージェント「dots」、複数台のローカルのコンピュータに接続して作業を分担できるように
- **何が起きたか**: dots は 9 月に発表された常時稼働のエージェントで、GPT-6 Astra と GPT-6.1 Terra を基盤とする。これまでもクラウドのコンピュータに加えて利用者のローカルのコンピュータを操作できたが、今回複数台を接続できるようになった。例として、1 台目の Mac で iOS アプリを開発しながら、2 台目の Mac で Xcode の変更をテストし、スクリーンショットを送るといった使い方が示されている。対象は Pro、Business Premium、Enterprise のプランで、OpenAI によると利用者数の国別ランキングで日本は 2 位。
- **なぜ重要か (評価)**: 1 つのエージェントが複数の手元の端末を操作できるため、エージェントのセッションやトークンが乗っ取られた場合の被害の範囲が、複数台の開発機にそのまま広がる。
- 出典: [ITmedia AI+ (2026-11-10)](https://www.itmedia.co.jp/aiplus/article/2611/10/2000003058/)

### [2026-11-10] [続報] Claude Fable 5.2 の第三者の評価: 実際のフリーランスの仕事の 41.3% を完了 (Remote Labor Index)。多段階のサイバー攻撃のベンチマークでは GPT-6 Cyber を上回る
- **何が起きたか**: Scale Labs と CAIS の Remote Labor Index で、Fable 5.2 は 41.3% で首位。次は Opus 5.5 の 21.25%、GPT-6 Astra の 20.83%、Fable 5.1 は 18% 弱。1 年前の開始時の首位 (Manus) は 2.5% だった。また Anthropic のシステムカードによると、Irregular の CyScenarioBench (現実的な環境で多段階のサイバー作戦を計画・実行できるか) で、Fable 5.2 は全課題の 76.3% を完了し、Fable 5.1 の 61.7%、OpenAI の GPT-6 Cyber の 61% を上回った。
- **なぜ重要か (評価)**: 汎用のモデルが、サイバー専用に調整した他社のモデルを多段階の攻撃のベンチマークで上回った。汎用のモデルの利用を前提にした悪用対策 (分類器や確認プログラム) の重要度がさらに上がる。
- 出典: [The Decoder (2026-11-10)](https://the-decoder.com/anthropics-fable-5-2-completes-41-percent-of-real-freelance-jobs-up-from-2-5-percent-a-year-ago/) / [The Hacker News (2026-11-10)](https://thehackernews.com/2026/11/anthropics-claude-fable-52-beats-gpt-6.html)

### [2026-11-10] 「Claude Opus 5.5 の推論が 11/3 から低下した」との指摘。1,400 件の Claude Code のセッションを分析。一方で「思考の要約の仕組みの変更」とみる反論も
- **何が起きたか**: 開発者の Shane Mellow 氏が、10/9〜11/7 の Claude Code のセッション約 1,400 件を Gemini 4 Argon で分析した。11/3 (日本時間 11/4 3 時ごろ) を境に、最初の操作までの思考トークンの中央値が 84 から 54 に約 36% 減り、スクリプトの実行や編集のエラーの指標が 47% 増えたという。同じ不具合の修正では、推論の設定が high だと 160 往復・13 ドルでも直らず、xhigh では 5 往復・0.85 ドルで直った。一方 Theo Browne 氏は、約 45 万 8,000 件の応答を調べ、Anthropic が思考の要約の仕組みをアカウントごとに順次変えている可能性を指摘し、自分の環境では能力の低下の兆候はないとした。Anthropic の資料では、表示される思考は別のモデルによる要約。
- **なぜ重要か (評価)**: コード監査やバグ修正にエージェントを使う場合、推論の設定 (high / xhigh) の差が結果とコストに大きく出ることを示す例。社内の評価では、モデル名だけでなく設定とサービス側の変更の日付を記録しておく必要がある。
- 出典: [GIGAZINE (2026-11-10)](https://gigazine.net/news/20261110-claude-opus-nerf/)

### [2026-11-09 公開 / 11-10 報道] NII、「第 2 回オープン大規模言語モデルシンポジウム」の講演資料を公開。LLM-jp の開発手法や EuroLLM の取り組みなど
- **何が起きたか**: 国立情報学研究所 (NII) は 11/9、11/5 に開いたシンポジウムで使った講演資料を公開した。大規模言語モデル研究開発センターが主宰する「LLM-jp」の成果発表 (オープンなモデル「LLM-jp」の開発手法の解説など) や、EU の 24 の公用語での性能に力を入れたオープンなモデル「EuroLLM」の紹介など、海外の有識者の基調講演の資料を含む。講演の動画も準備ができ次第公開する。
- **なぜ重要か (評価)**: 学習データや手法を公開している国産のオープンなモデルは、データの汚染やバックドアの検証を再現できる数少ない対象。国内でモデルのサプライチェーンを評価する際の参考資料になる。
- 出典: [ITmedia AI+ (2026-11-10)](https://www.itmedia.co.jp/aiplus/article/2611/10/2000003046/)

## AI セキュリティ

### [2026-11-10] SGLang の RCE で NEAR AI の推論サーバーが侵害される。TEE の中の「機密モード」のリクエストも見えた可能性。18 のエージェントと約 100 人の利用者のデータが流出 (SGLang RCE Exploit Breaches NEAR AI)
- **何が起きたか**: 攻撃者はオープンソースの推論エンジン SGLang のリモートコード実行の欠陥を突き、先週の日曜日に NEAR AI の推論サーバーの 1 台でコードを実行した。その日にそのサーバーが処理したリクエストは、TEE (信頼できる実行環境) の中で処理する「機密モード」のものも含めて見えた可能性がある。NEAR AI は、TEE は「環境の中で動くソフトウェアの脆弱性からは守らない」と説明している。攻撃者はさらに、提供終了済みの Private Chat の内部システムで約 100 人分のアカウント情報 (メールアドレス、氏名、一部はプランと残高) をダウンロードし、TEE の外で動いていた旧版の NEAR AI Agents の 18 のエージェントから会話の履歴・設定・ログを取得した。ログに残っていた 2 社の NEAR AI Cloud の API キーは失効済み。NEAR AI は全推論サーバーに修正を適用したが、CVE 番号、影響する SGLang のバージョン、SGLang 側の修正の有無は明らかにしていない。Brave は 10 月に、Leo アシスタントの GLM 5.3 Flash のチャットを NEAR AI の TEE で動かしていると説明しているが、影響の有無は不明。
- **なぜ重要か (評価)**: 「TEE で保護」とうたう AI 推論でも、TEE の中の推論エンジン (SGLang / vLLM など) が RCE の対象になれば機密性は崩れる。SGLang のアドバイザリと修正のコミットが出しだい差分を追う価値があり、推論サーバーの API を外部に出している環境は、今のうちに公開の範囲を絞るべき。
- 出典: [The Hacker News (2026-11-10)](https://thehackernews.com/2026/11/sglang-rce-exploit-breaches-near-ai.html)

### [2026-11-09 公表 / 11-10 報道] Fireworks AI の侵害が拡大。外部のクラウド事業者経由で開発環境に入られ、一部の顧客のデータセットと未完成のモデルの重み、課金情報が流出。Notion AI の会話記録も
- **何が起きたか**: Fireworks AI は 10/10 に、内部の資格情報の不正利用で、一部の顧客の評価ジョブの環境変数 (API キーやトークン) が取られたと公表していた。11/9 の更新では、攻撃者が 10/23 に、研究開発の機械をホストする社名非公表のクラウド事業者に入り、10/24 に Fireworks の開発機から不正なワークロードを実行して、顧客のデータにさらに影響を与えたと明らかにした。対象は、リソースのメタデータ、課金情報 (請求先、支払い履歴、残高)、一部の顧客の未完成のモデルの重みとデータセット。カード番号は保存していない。Fireworks AI は、LLM へのアクセスを不正なルーティングのサービスに売る、金銭目的の集団 (LLMjacking) との関連を示す証拠があるとしている。Notion は、影響は全ワークスペースの 1% 未満で、Insights 機能に使う Notion AI の会話記録 (大半は誰のものか特定できない形) が含まれていたと公表し、同機能を止めた。
- **なぜ重要か (評価)**: 推論・学習の事業者には、顧客の重み、データセット、秘密情報が集まっているため、クラウドの連携先を経由した横移動の被害が下流の SaaS (Notion) まで広がった。LLMjacking が API キーの窃取から、学習の資産そのものの窃取に広がっていることを示す。
- 出典: [The Hacker News (2026-11-10)](https://thehackernews.com/2026/11/fireworks-ai-breach-widens-to-expose.html) / [TechCrunch (2026-11-10)](https://techcrunch.com/2026/11/10/cyberattacks-threaten-to-make-open-source-ai-a-little-less-open-hugging-face-exec-warns/)

### [2026-11-05 公表 / 11-09 報道] Anthropic 公式の Office スキル (docx / pptx / xlsx) に、共有の /tmp の固定名の .so を LD_PRELOAD で読み込む問題「Office Party」。Anthropic は修正しない方針
- **何が起きたか**: AIR Security の研究者が、Anthropic 公式の文書スキルの共通ヘルパー `scripts/office/soffice.py` の問題を公開した。Linux で Unix ドメインソケットを作れない環境 (Claude Code のサンドボックス、seccomp で制限したコンテナ、systemd で固めた環境など) では、LibreOffice に共有の一時ディレクトリ (多くは /tmp) にある固定名の `lo_socket_shim.so` を LD_PRELOAD で読み込ませる。そのファイルがすでにあるかどうかしか確認しないため、先にファイルを置ける者は、次の文書の変換のときにエージェントを動かすユーザーの権限でコードを実行できる。macOS は影響を受けない。研究者は 5 月に報告したが、AIR によると Anthropic は「脆弱なコードはサンドボックスの中でしか動かない」ためセキュリティ境界の外とみなしている。11/10 時点で anthropics/skills の main は固定のパスのままで、CVE やアドバイザリは確認されていない (Qiita の検証記事)。
- **なぜ重要か (評価)**: /tmp の固定名ファイルという古典的な脆弱性 (CWE-377 / CWE-426 系) が、公式の AI スキルにそのまま入っていた例。CI ランナーや共有のコンテナでスキルを使う環境では、/tmp を分離するか、該当するファイルの有無を確認したい。スキルは「信頼済みの拡張」ではなく依存関係としてコード監査の対象に入れるべき。
- 出典: [Dark Reading (2026-11-09)](https://www.darkreading.com/endpoint-security/attackers-claude-office-party-flaw-malicious-code-linux) / [Qiita (2026-11-10)](https://qiita.com/phpcheck/items/7a57709d0bbd4aab7396)

### [2026-11-10] [続報] Railway が詳細な事故報告を公表: 攻撃者は安全制限を外したモデルのエージェントでビルド基盤から脱出し、AI の API キーを狙った。不正な利用額は約 74 万ドル
- **何が起きたか**: 最初の侵入は 10/20 07:28 UTC。未知の欠陥でビルドシステムのファイルの分離を一部抜け、ホストのファイルからビルドサーバー用の資格情報を取得した。この資格情報は想定より強い権限を持ち、Temporal のタスク基盤で 353 件のビルドの履歴 (秘密情報を含む) を読めた。キャッシュされたリポジトリから Railway の内部コードも取られ、AI エージェントが弱点を並行して探す地図になった。攻撃者は ARTEX に似たエージェントのフレームワークで、安全制限を外したモデルを使ったとされる。最初の経路を塞いだ後、10/21 03:26 UTC に OIDC の信頼の設定ミスから短期のクラウドの資格情報を得て、SSH 秘密鍵を取り、顧客のワークロードを管理するマシンに入り、KMS で一部の環境変数を復号した。DB の検索は AI 事業者のキーの名前を狙っていた。環境変数を復号された可能性があるのは最大でワークスペースの 1.85% (約 10 万)。1,852 人の連携アカウントのトークンをリセットした。不正な利用額は約 74 万ドルで、事業者が返金しない分は Railway が負担する。
- **なぜ重要か (評価)**: 「コードを盗む → エージェントで次の経路を探す」ことで、防御側が 1 つ目の入口を塞いでも数時間で別の経路 (OIDC の信頼の設定) から再侵入された。ビルドの分離、資格情報の権限、OIDC のクレームの条件は、ペンテストで真っ先に確認すべき項目。
- 出典: [Cyber Security News (2026-11-10)](https://cybersecuritynews.com/railway-details-data-breach/)

### [2026-11-10] Google DeepMind「AlphaProof Code」: Carbon のエージェントが約 650 万行の Lean の証明を生成し、libsignal のコンパイル後の機械語に対して前方秘匿性などを形式検証
- **何が起きたか**: 人間の専門家と、Gemini 4 Carbon と Claude Opus 5.5 のエージェントが、証明すべき仕様を共同で書いた。その後、Carbon のエージェントが約 650 万行の Lean の証明をすべて生成し、不正な証明は Lean が拒否した。前方秘匿性、侵害後の安全性、認証などの性質を、設計ではなくコンパイル後の機械語について証明した。5 人の研究者が 4 週間で作業した。修正済みの過去のバグ 2 件を戻したビルドでは、性質が破れることを証明できた。対象は Google によるビルド (小さな CLI ラッパー経由) で、Signal のアプリそのものではない。一部の分析ではサイドチャネルを除いている。仕様と証明は公開される。また Google によると、Wiz は Carbon for cyber で、2 つの大手 SaaS のゼロデイを 2 時間以内に見つけた。
- **なぜ重要か (評価)**: AI で形式検証のコストが下がると、「監査済み」よりも強い「証明済み」の主張が出てくる。監査をする側は、証明の範囲 (ビルドの構成、除外したサイドチャネル、ラッパー) が実際の製品とどう違うかを読み分ける必要がある。
- 出典: [SecurityWeek (2026-11-10)](https://www.securityweek.com/google-widens-gemini-4-carbon-access-after-ai-agents-verify-signal-code/)

### [2026-11-09] Microsoft FORGE Lab、AI の脆弱性スキャナー「Hyenas」(MDASH の研究版) で、Rust の標準ライブラリ (std / core) のメモリ安全性の問題を複数発見
- **何が起きたか**: 見つかった問題には、safe Rust だけで未定義動作を起こせるものがある。3 つのパターンに分類した。(1) パニックしない前提: nightly の `Iterator::map_windows` の `MapWindows::clone` で、利用者の `T::clone` がパニックすると未初期化の領域を drop する。(2) 利用者の実装を信じる: カスタムの `Pattern` で `str::replace` が UTF-8 でない `String` を作れる (`StringPattern` を `&str` に変えて修正)。(3) OS の状態を信じる: 子スレッドからの `process::exit` がメインスレッドの代替シグナルスタックを munmap する (2015 年からのバグ、#161018。実際の悪用は難しいと評価)。`Command::exec` が読み取りロックのまま `environ` を書き換え、他のスレッドが新しいプログラム用の環境変数を見たり、解放済みの配列を読んだりする問題も報告した。公開時点で 2 件は未修正。Allocator API は Rust 1.100 (11/12) で、実装側に巻き戻し (unwind) を禁じる形で安定化する。
- **なぜ重要か (評価)**: 「Rust だから安全」という前提の下にある unsafe の契約違反を、AI が OS とのやり取りまで含めて探せるようになってきた。Rust の監査でも、unsafe ブロックが利用者の trait の実装やプロセス全体の状態をどこまで信じているかを重点的に確認すべき。
- 出典: [Microsoft Security Blog (2026-11-09)](https://www.microsoft.com/en-us/security/blog/2026/11/09/forge-lab-uses-agentic-tools-to-identify-memory-safety-issues-in-rust/)

### [2026-11-09 arXiv] StealthyPoison: 公開のスキルのレジストリで、機能はそのままで「判断の規則」だけを書き換えたスキルを上位に表示させ、エージェントに誤った結果を出させる。Opus 4.8 の Claude Code でも成功
- **何が起きたか**: 研究者は、第三者のスキルの判断に関わる規則だけを書き換え、宣伝している機能や通常の動作は保ったまま、誤った結果を出させる攻撃を提案した。実際の利用者の依頼や正解を知らなくても、代理のエージェントで元のスキルを動かして参照解を作り、ペイロードを繰り返し改良する。検索のメタデータを補強して、毒入りのスキルが正規のスキルより選ばれやすくする。566 のスキル、5,244 件の依頼、2 万 6,000 超のレジストリの項目で評価し、毒入りスキルを最上位に表示させる率は HotFlip や GCG より 13.6% 改善した。別の 3 つのモデルにもそのまま転用でき、Opus 4.8 で動く Claude Code のワークフローで攻撃が成功した。多くのペイロードは SkillSpector と GPT-5.4-mini による検出をすり抜けた。
- **なぜ重要か (評価)**: 「明らかに悪意のある命令」を探す今のスキルのスキャナーでは、手順の微妙な改ざんを捕まえにくいことを示した。スキルのレジストリから取り込む場合は、署名や固定したバージョンと、差分のレビューが必要になる。
- 出典: [arXiv 2611.12155 (2026-11-09)](https://arxiv.org/abs/2611.12155)

### [2026-11-09 arXiv] 「Say Shibboleth」: ハニーポットの罠で、攻撃してくる AI エージェントの LLM とハーネスを特定する。15 のモデルを平均 90%、4 つのハーネスを 92% の精度で判別
- **何が起きたか**: エージェントが欲しい資源を得る条件として、特徴的な応答を引き出す「shibboleth trap」(モジュール型のハニーポットのサービス) を提案した。プロンプトインジェクションを成功させなくても、モデルの自己申告や文体を引き出せる。さらに、ツールの出力の中の秘密情報の伏せ方、コマンドの時間制限、ツールの呼び出しの順序といったハーネスごとの癖を、その後のリクエストに表れる影響だけから推定する。宣言と振る舞いを組み合わせて 15 の候補のモデルを平均 90% (top-1) で区別し、4 つのハーネスを固定のルールで 92% の精度で特定した。身元を隠すよう指示されたエージェントでも、振る舞いの証拠は残った。
- **なぜ重要か (評価)**: AI エージェントによる自動の侵入 (Operation Snowball など) が増える中で、防御側のハニーポットやログから「どのモデル・どのツールで攻撃されたか」を割り出す手法として、インシデント対応と脅威情報に直結する。
- 出典: [arXiv 2611.12386 (2026-11-09)](https://arxiv.org/abs/2611.12386)


## セキュリティニュース

### [2026-11-10] Microsoft 11 月の Patch Tuesday: 約 1,100〜1,260 件を修正。悪用済みのゼロデイは Outlook の NTLM ハッシュ漏えい (CVE-2026-124194) の 1 件、Exchange 経由で届く Windows Search のゼロクリック RCE (9.8) も
- **何が起きたか**:
  - 件数は数え方で違う。BleepingComputer は 1,235 件 (Critical 66。Edge の Chromium 由来 142 件を含み、月初に出た 108 件は除く)。SecurityWeek は 1,094 件、ZDI は「新規の CVE は約 1,090」、SANS ISC は 1,260 件 (Critical 68、Edge 167) としている。過去最多だった 10 月 (約 1,410) よりは少ないが、2 か月続けて 1,000 件を超えた。SecurityWeek によると、内訳は Windows 726、Office 174、SQL Server 59、開発ツール 53、SharePoint 27、Azure 20、Exchange 9。
  - **悪用済み (KEV 追加済み)**: CVE-2026-124194 (Outlook のスプーフィング、CVSS 6.5、Moderate)。細工したメッセージファイルを開かせると、Outlook が外部コンテンツの警告を出さずに攻撃者のサーバーへ接続し、NTLMv2 ハッシュが漏れる。プレビューウィンドウでは発動しない。対象は Microsoft 365 Apps、Office LTSC 2021 / 2024。Microsoft は攻撃の詳細を公表していない。発見者は「nono」と Benoît Sevens で、Sevens の謝辞には Anthropic の Claude の利用が記されている。CISA は同じ日に KEV に追加した (期限 11/24)。
  - 公表済み (publicly disclosed) のゼロデイはなし (ZDI / SecurityWeek)。
  - **注目の Critical**: CVE-2026-116928 (Windows Search の RCE、9.8)。ZDI によると Exchange Server を経由して届き、細工した添付ファイル付きのメールをサーバーが自動でインデックスした時点で発動する。受信者は何も開かない。CVE-2026-119958 (LDAP の未認証 OOB write による RCE、DC への影響が大きい)。CVE-2026-119952 (Schannel の未認証 RCE、攻撃の難度は高いが「Exploitation More Likely」)。CVE-2026-95962 (Virtual Filtering Platform の UAF で、競合状態を伴う)。CVE-2026-112967 (Xbox Live Networking の heap overflow、9.8)。CVE-2026-119990 (Azure OpenAI の権限昇格。「顧客の対応が必要」とあるのに、何をすべきかが書かれていない)。ISC は TCP/IP の RCE (CVE-2026-113859、7.5) も挙げている。
  - ZDI は未認証・操作不要でネットワーク越しにコードが実行できる「ワーム化しうる」バグを 30 件と数えた。MSMQ 5 件、DNS 4 件、DHCP Server 2 件のほか、CredSSP、IIS、RPC Runtime、WDS などが含まれる。
  - Windows 11 23H2 の Enterprise / Education 版は、今回が最後の月例更新。
- **悪用 / PoC**: CVE-2026-124194 は悪用を観測 (Microsoft の判定、KEV 入り)。公開 PoC は確認できなかった。そのほかの CVE は、公表時点で悪用も公開もなし。
- **なぜ重要か (評価)**: 悪用されているのは CVSS 6.5 の Outlook のバグだが、狙いは NTLM のリレーやクラッキングなので、SMB の外向き通信の遮断と NTLM の制限の確認が先決。件数が多いため、優先順位は Exchange と DC (Search、LDAP)、それに DNS / DHCP / MSMQ を出している境界のサーバーから付けるのが現実的。
- 出典: [BleepingComputer (2026-11-10)](https://www.bleepingcomputer.com/news/microsoft/microsoft-november-2026-patch-tuesday-fixes-1-235-flaws-outlook-zero-day/) / [ZDI (2026-11-10)](https://www.thezdi.com/blog/2026/11/10/the-november-2026-security-update-review) / [SecurityWeek (2026-11-10)](https://www.securityweek.com/exploited-outlook-zero-day-among-1094-flaws-patched-by-microsoft/) / [SANS ISC (2026-11-10)](https://isc.sans.edu/diary/rss/33508)

### [2026-11-10] Git 2.56.1 ほか: 悪意のあるリポジトリを再帰的にクローンするとコードが実行される欠陥 (CVE-2026-111760) など 6 件を修正
- **何が起きたか**:
  - Git プロジェクトが 2.56.1 を公開した。2.55.1 / 2.54.1 / 2.53.1 / 2.52.1 / 2.51.3 / 2.50.2 にもバックポートしている。
  - 本命の CVE-2026-111760 は、index の処理での整数の切り詰め。極端に長いパスが安全確認を通ったあと、短い名前 (攻撃者は `.git` にできる) でディスクに書かれる。これを使うと、サブモジュールの `.git` ファイルを、悪意のある hooks や config を置いたディレクトリへのシンボリックリンクに差し替えられる。結果として `--recursive` でのクローン中にコードが実行される。
  - ほかの 5 件は次のとおり。
    - CVE-2026-113408: 空のリポジトリを protocol v2 でクローンしたとき、サーバーが返す HEAD の symref の名前でパストラバーサル。files バックエンドで refs の外に書き込める。
    - CVE-2026-114467: 署名が 3 つ以上あるタグを merge すると、スタックが壊れる。
    - CVE-2026-114469: 展開すると 1GiB の上限を超える binary patch で OOB read。
    - CVE-2026-105437: conflict-marker-size の値を大きくすると、merge の出力サイズの計算があふれて heap overflow。GitLab が CVE を採番。
    - CVE-2026-114466: fast-import の rewrite-submodules-from / to と export-pack-edges で、任意のファイルの読み取りや書き込み。
  - GitHub は github.com と GHEC に適用済み。GHES の修正版は 3.19.15 / 3.20.11 / 3.21.9 / 3.22.4。The Hacker News によると、Git for Windows は 11/10 19:09 UTC の時点で修正版を出していなかった。
- **悪用 / PoC**: 悪用の報告はなし。公開 PoC も確認できなかった。ただし修正の差分からは再現しやすい種類のバグ。
- **なぜ重要か (評価)**: CI や開発者の端末が、外部のリポジトリを `--recursive` で取り込む流れは多い。GitLab は CVE-2026-105437 について、マージできるかの判定に `git merge-tree` を走らせるホスティングのサーバーが最も狙われやすいとしている。自前で Git をホストしている環境では、サーバー側の更新も急ぐ必要がある。
- 出典: [The Hacker News (2026-11-10)](https://thehackernews.com/2026/11/git-patches-flaw-that-lets-malicious.html) / [GitHub Blog (2026-11-10)](https://github.blog/open-source/git/git-security-vulnerabilities-announced-7/)

### [2026-11-10] Xen Orchestra に、悪用中の認証回避 (VSA-2026-062、CVE は未採番)。管理者の権限から XCP-ng のホストを root で乗っ取れる
- **何が起きたか**:
  - Vates が、Xen Orchestra と XOA の REST API での認証トークンの処理に、致命的な認証回避があると公表した。The Hacker News が引用した advisory によると、トークンの検索で細工した Cookie の `{}` がフィルターなしの検索として扱われ、先頭のトークンが返る。プロバイダーは、そのトークンが期限内ならトークンの持ち主として認証してしまう。そのあと `/rest/v0/users/me/authentication_tokens` から、再利用できるログイントークンの ID を取り出せる。
  - Vates は、Admin の権限から、管理しているプールで任意のコードが実行でき、XCP-ng のノードを root で乗っ取れるとしている。
  - 修正版は XO 6.9.1 (stable) と 6.10.0 (latest)、xo-server 5.211.2 / 5.213.1。
  - IOC は、`91.211.251.112:8001` への接続と、Tor の .onion の 3333 番ポート。シリアルポートの出力先をファイルにした VM がないかの確認も推奨されている。発見者は TDC NET Security の 2 人。
- **悪用 / PoC**: 悪用を観測 (Vates が確認し、IOC を公開)。公開 PoC は確認できなかった。
- **なぜ重要か (評価)**: 仮想化の管理画面が乗っ取られると、ハイパーバイザーの全体が攻撃者の手に渡る。インターネットから管理画面に届く構成になっていないか、すぐに確認すべき案件。
- 出典: [BleepingComputer (2026-11-10)](https://www.bleepingcomputer.com/news/security/critical-xen-orchestra-auth-bypass-flaw-exploited-to-hijack-vm-servers/) / [The Hacker News (2026-11-10)](https://thehackernews.com/2026/11/hackers-exploit-critical-xen-orchestra.html)

### [2026-11-09〜10] Chrome、今年 8 件目の悪用済みゼロデイを修正: XML の処理での UAF (CVE-2026-125350)。CISA は KEV に追加
- **何が起きたか**:
  - Google は 11/9 (月) の advisory で、CVE-2026-125350 のエクスプロイトが実際に出回っていると認めた。XML のパーサーで解放したオブジェクトを参照し続ける use-after-free で、深刻度は High。
  - 修正版は Windows / macOS が 157.0.8103.50/.51、Linux が 157.0.8103.50。
  - CISA は 11/10 に KEV に追加した (期限 11/24)。説明では「サンドボックス内での任意のコードの実行」で、Edge や Opera など Chromium 系のブラウザーすべてが対象。
  - 2026 年の Chrome の悪用済みゼロデイは、2 月 (CSS、CVE-2026-2441)、3 月 (Skia / V8、CVE-2026-3909 / 3910)、4 月 (Dawn、CVE-2026-5281)、6 月 (V8、CVE-2026-11645)、9 月 (V8、CVE-2026-87491 / 85046) に続いて、これで 8 件目。
- **悪用 / PoC**: 悪用を観測 (Google の発表)。攻撃者や手口は非公開。公開 PoC はなし。
- **なぜ重要か (評価)**: サンドボックスからの脱出と組み合わせた攻撃の一部と考えるのが自然。XML というサードパーティ系のライブラリが関わる可能性があるため、Chromium 系の各ブラウザーと Electron のアプリの追従を確認したい。
- 出典: [BleepingComputer (2026-11-10)](https://www.bleepingcomputer.com/news/security/google-patches-eighth-chrome-zero-day-exploited-in-attacks-this-year/) / [The Hacker News (2026-11-10)](https://thehackernews.com/2026/11/google-issues-chrome-security-update.html)

### [2026-11-09〜10] N-able、研究者が N-central の 30 件超のゼロデイを PoC 付きで公開 (「Able2Shell」) したため、ホスティング版を停止。オンプレミスの利用者にも停止を要請
- **何が起きたか**:
  - 研究者の Sean Bales 氏が、11/8 (日) の深夜に、RMM 製品 N-central の脆弱性 30 件超 (The Hacker News は 33 件) と、PoC のリポジトリ「Able2Shell」を予告なしに公開した。検証の対象はプレリリース版の Appliance 2026.4.0.31。
  - 最も深刻なのは、サービスのインポート機能にある未認証の XXE を起点とするチェーン。信頼されたローカルセッションを盗み、パスワードをリセットし、nable ユーザーとしてコマンドを実行する。有効な Default Administrator も作れる。
  - ほかに、パッチのメタデータを使って root でコマンドを実行する stored XSS、nable から root への権限昇格、XSS から OGNL への連鎖、MDM のなりすましなどがある。
  - Bales 氏は、別の N-able 製品で報告した RCE 2 件などが、5〜6 か月たっても直っていないことを予告なしの公開の理由に挙げている。
  - N-able は 11/9 にホスティング版の N-central を全リージョンで停止し、hotfix を検証している (11/10 17:42 UTC の時点で修正版は出ていない)。
- **悪用 / PoC**: PoC は公開済み。watchTowr はハニーポットで悪用の試行を観測し、Defused Cyber は未認証での匿名エージェントのセッションの開始や設定の取得を観測した。N-able は「スキャンは見ているが、顧客の環境での攻撃の成功は確認していない」としている。
- **なぜ重要か (評価)**: RMM は MSP の配下にある多数の顧客の端末へ、一度に入れる入口になる。修正版が出るまでは、インターネットからの到達性の遮断と侵害の調査が現実的な対策。
- 出典: [BleepingComputer (2026-11-09)](https://www.bleepingcomputer.com/news/security/n-able-takes-cloud-platform-offline-after-30-plus-zero-days-published/) / [The Hacker News (2026-11-10)](https://thehackernews.com/2026/11/n-able-takes-hosted-n-central-offline.html) / [SecurityWeek (2026-11-10)](https://www.securityweek.com/n-able-takes-n-central-offline-as-researcher-drops-over-30-zero-days/)

### [2026-11-10] [続報] Barracuda ESG の事前認証 root RCE (CVE-2026-116606 / CVE-2026-111560): Barracuda が「少数の顧客で悪用」と更新。CISA は KEV に追加し、期限は 11/13
- **何が起きたか**:
  - Barracuda は 11/9 (月) の夜、修正から約 1 週間たった 2 件について、少数の組織で悪用を確認したと advisory を更新した。
  - CVE-2026-116606 は、設定のインポートの機能を未認証で呼び出し、細工したバックアップを復元して全体の設定を書き換えられる認証回避。CVE-2026-111560 は、root で動く OS コマンドインジェクション。CVE-2026-111560 は ESG のほか、Load Balancer、ADC、Message Archiver、WAF、WSG などにも影響する。
  - CISA は 11/10 に両方を KEV に追加した。期限は通常より短い 11/13。KEV の参照先には Mandiant の開示 (MNDT-2026-0041 / 0042) が挙がっている。
  - Barracuda は、自動のパッチの適用が無効になっている顧客に有効化を勧め、管理画面を信頼できる内部のネットワークに限るよう求めている。
- **悪用 / PoC**: 悪用を観測 (ベンダーが確認、KEV 入り)。前回の報道のとおり、watchTowr がパッチの差分から攻撃の全体を再現している。
- **なぜ重要か (評価)**: ESG は 2023 年の UNC4841 の事件 (CVE-2023-2868) で大きな被害を出した製品で、今回も情報窃取型の攻撃者に狙われやすい。管理画面が外から見えていた機器は、侵害を前提に調べるべき。
- 出典: [BleepingComputer (2026-11-10)](https://www.bleepingcomputer.com/news/security/hackers-exploit-barracuda-email-security-gateway-flaws-to-get-root-access/) / [CISA KEV (2026-11-10)](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

### [2026-11-10] CISA KEV のほかの追加: Cisco BroadWorks の XXE (CVE-2026-20320) と Openwave Webtop Media Transcoder (CVE-2026-111793)。11/9 には GPUStack (CVE-2026-102895) も
- **何が起きたか**:
  - 11/10 の KEV への追加は、Outlook、Chrome、Barracuda 2 件、Cisco BroadWorks、Openwave の計 6 件。
  - CVE-2026-20320 は、BroadWorks の OCI-P のサービスでの blind (外部への通信を使う) XXE。未認証で設定ファイルなどを読める。8 月の advisory (cisco-sa-bworks-xxe-uwUd7CEt) で、RI.2026.07 で修正済み。公表の時点では、Cisco は悪用を把握していなかった。
  - CVE-2026-111793 は、Webtop Media Transcoder (1.1.22.0 未満) で、ログインした利用者が Webmail を経由せずに想定外の文書の形式を変換させられる問題。前回、JVN の欄で紹介した。
  - 11/9 には、[前回] 紹介した GPUStack の「ループバックからなら管理者」(CVE-2026-102895) も、sshole などと一緒に KEV に追加された (期限 11/12)。The Hacker News によると、7 月の advisory の時点で、すでに実際の悪用が報告されていた。
- **悪用 / PoC**: いずれも CISA が悪用の証拠を根拠に追加。BroadWorks と Openwave の攻撃の詳細は非公開。
- **なぜ重要か (評価)**: BroadWorks は通信事業者向けの VoIP の基盤で、8 月の修正を適用していない事業者は優先して対応すべき。KEV の「修正済みの古い脆弱性があとから悪用される」型の典型例。
- 出典: [CISA KEV JSON (2026-11-10)](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json) / [The Hacker News (2026-11-10)](https://thehackernews.com/2026/11/cisa-warns-of-active-exploitation-of.html)

### [2026-11-10] SAP の 11 月のセキュリティパッチ: 35 件のうち CVSS 10.0 が 4 件。Onapsis 命名の「ICM2SHELL」と「PROXYGATE」は、未認証の RCE
- **何が起きたか**:
  - CVSS 10.0 の 4 件は次のとおり。
    - CVE-2026-76964: NetWeaver AS ABAP の ICM でのメモリ破壊。
    - CVE-2026-120017: SAML2 の Service Provider での認証の欠落。
    - CVE-2026-89103: SAP Gateway のアクセス制御の不備。
    - CVE-2026-89126: Web Dispatcher でのメモリ破壊。
  - Onapsis は CVE-2026-76964 と CVE-2026-89126 をまとめて「ICM2SHELL」と呼び、SAP のユーザーも操作も不要なネットワーク越しの RCE としている。CVE-2026-89103 は「PROXYGATE」で、外部の未認証の攻撃者を Gateway に内部のアプリケーションサーバーと誤認させ、インストールを所有するアカウントの権限でシステムを掌握できる。
- **悪用 / PoC**: 公表時点では悪用も PoC もなし。ただし前回の報道のとおり、SAP のバグは修正から 1〜3 日で悪用か PoC の公開に至る傾向がある。8 月の Commerce Cloud の欠陥 (CVE-2026-58231) も、修正の数日後に悪用された。
- **なぜ重要か (評価)**: Web Dispatcher と ICM は、ほぼすべての SAP 環境でインターネットに面している部品。今週中の適用か、少なくとも外部からの到達性の制限が必要。
- 出典: [BleepingComputer (2026-11-10)](https://www.bleepingcomputer.com/news/security/sap-patches-four-maximum-severity-security-vulnerabilities/) / [SecurityWeek (2026-11-10)](https://www.securityweek.com/sap-patches-critical-icm2shell-proxygate-vulnerabilities/) / [The Hacker News (2026-11-10)](https://thehackernews.com/2026/11/sap-patches-four-cvss-100-flaws.html)

### [2026-11-10] Adobe、9 製品で約 110 件を修正。Adobe Connect は CVSS 10.0 が 6 件、AEM も Critical
- **何が起きたか**:
  - Adobe Connect (APSB26-191) は 24 件で、うち Critical が 18 件。CVSS 10.0 の 6 件は、いずれもネットワーク越しに、未認証・操作不要で突けて、スコープが変わる (ZDI)。
  - Experience Manager (APSB26-189) は 14 件。CVSS 9.9 の Critical 4 件は認可の誤りとコードインジェクションで、低い権限のアカウントから任意のコードを実行できる。
  - 種類は SSRF、パストラバーサル、CRLF、XXE、SQLi、XSS など。ほかに Photoshop、Premiere、After Effects、Media Encoder、Content Credentials SDK なども対象。優先度は Connect と AEM が 2、その他は 3。
- **悪用 / PoC**: Adobe は悪用を把握していない。公開もなし。
- **なぜ重要か (評価)**: Connect をオンプレミスで公開している組織は多くないが、未認証の CVSS 10 が並ぶので、ペネトレーションテストの対象に含まれる場合は版の確認が必須。
- 出典: [SecurityWeek (2026-11-10)](https://www.securityweek.com/adobe-patches-110-vulnerabilities-across-9-products/) / [ZDI (2026-11-10)](https://www.thezdi.com/blog/2026/11/10/the-november-2026-security-update-review)

### [2026-11-10] Turla の新しいツール「Cereal」: 政府機関の Exchange の EdgeTransport.exe に入り込み、NATO と EU とのやりとりを選んで盗む (ESET)
- **何が起きたか**:
  - ESET によると、ロシアの FSB 系の Turla (Snake、Secret Blizzard) が、カザフスタンの政府機関と、ルーマニアの政府機関 (2025 年 12 月 23 日に侵害) の Exchange で、.NET のモジュール型の「Cereal」を使っていた。
  - CerealBox は EdgeTransport.exe に注入され、既存のトランスポートエージェントのハンドラーを乗っ取る。新しいエージェントを登録せず、配送も止めずにメールを検査する。DOC / DOCX / PDF の添付と、送信者・宛先・件名の条件に合うメールを集める。
  - CerealNeuron は、Exchange のサービスに似たパスで暗号化されたリクエストを待ち受け、使い捨ての CerealRunner (タスクごとにビルドされた .NET の実行体) をメモリ上で実行する。ネットワーク機能のない CerealHermit は、ディスク上の暗号化ファイルから命令を読む。
  - 外部の C2 はなく、侵害した Exchange 自体が唯一の制御点。.NET のネイティブイメージのキャッシュを悪用する手法も使う。
- **悪用 / PoC**: 実際の攻撃での使用を確認 (ESET)。初期の侵入経路は記事では不明。
- **なぜ重要か (評価)**: トランスポートエージェントの一覧に異常が出ないので、従来の点検では見つけにくい。オンプレミスの Exchange を持つ組織は、EdgeTransport.exe にロードされたモジュールと、ネイティブイメージのキャッシュの改ざんを確認する価値がある。
- 出典: [BleepingComputer (2026-11-10)](https://www.bleepingcomputer.com/news/security/turla-hackers-use-new-ceral-malware-to-spy-on-govt-exchange-servers/) / [The Record (2026-11-10)](https://therecord.media/russia-hackers-espionage-romania-kazakhstan) / [Help Net Security (2026-11-10)](https://www.helpnetsecurity.com/2026/11/10/eset-turla-exchange-malware/)

### [2026-11-10] Check Point: 中国系の 3 つの諜報活動 (SilentDelivery / OceanGate / DarkWire) を、ツールの供給元「CopperDragon」の Sparrow の基盤でつなぐ
- **何が起きたか**:
  - Check Point は、CopperDragon を FamousSparrow、Earth Estries、Tropic Trooper、UAT-9244、UAT-8302 などにツールを供給する「デジタルの補給係」とみている。
  - SilentDelivery (2026 年初めから) は、欧州とアジアの政府・海運・IT・研究のサイトを改ざんして、Chrome の偽の証明書エラーと「Certificate Fix」の MSI を出す水飲み場型の攻撃。配るのは SquadC (SquawkDoor) か SparrowDoor の亜種。
  - OceanGate (2025〜2026 年) は、インターネットに面した Linux サーバーから侵入し、Go 製の AnnobinDoor を使い、RDP の総当たりで Windows に横展開する。SparrowDoor に WinDivert ドライバーを組み込み、443 番などの正規のサービスのポートに届いた特定の IP からの通信を、カーネルで書き換えて内部のポート (例: 49628) に流す受動型のバックドアにしていた。SparrowShell は、Reptile ベースの Mélofée とコードを共有している。
  - DarkWire (2025 年半ば) は、ラテンアメリカの通信事業者と政府を CopperDoor / CopperDNS で狙う。C2 は被害者と同じ国に置かれることが多い。
- **悪用 / PoC**: 実際の攻撃を観測 (Check Point)。
- **なぜ重要か (評価)**: ポートを書き換える受動型のバックドアは、外から見ると正規のサービスと区別できない。WinDivert のドライバーのロードを監視すると検知の手がかりになる。
- 出典: [Check Point Research (2026-11-10)](https://research.checkpoint.com/2026/not-all-that-glitters-is-gold-tracking-copperdragons-sparrow-framework-around-the-globe/) / [The Hacker News (2026-11-10)](https://thehackernews.com/2026/11/three-china-nexus-espionage-campaigns.html)

### [2026-11-10] バックアップ製品 AhsayCBS の 2 件 (CVE-2026-105133 / 105134) がゼロデイとして悪用。Web シェル 5 種、マイナー、サンドボックスを避ける Python のバックドア (Huntress)
- **何が起きたか**:
  - Huntress は 2026 年 10 月初めに、認証回避とコマンド実行の 2 件をつないだ攻撃を観測した。Ahsay の修正は 10 月半ばで、攻撃は修正の前から始まっていた。
  - 攻撃者は JSP の Web シェルを 5 種類 (nsmind.jsp、画像のプレビューを装う AhsayCBS.jsp、自分を消す st_xxxxxx.jsp など) 置き、XMRig を 2 つ動かし、GOST、Chisel、AnyDesk、Atera、Splashtop を配置した。
  - Python のバックドア (main.py) は、MachineGuid の SHA-256 と同じ名前のマーカーファイルがないと動かない。サンドボックスや解析者の端末を避けるための仕掛けで、条件を満たすと埋め込んだ DLL をメモリ上で実行し、C2 に接続する。
  - 同じ環境の Veeam サーバーでは、NetExec の Veeam の認証情報を盗むモジュールと同じ動きの PowerShell が、WMI 経由で実行されていた。
- **悪用 / PoC**: 悪用を観測 (Huntress)。公開 PoC は確認できなかった。
- **なぜ重要か (評価)**: バックアップのサーバーにはハイパーバイザーやドメインの認証情報が集まるため、ランサムウェアの前段として狙われやすい。AhsayCBS を使っている組織は、修正の適用に加えて、10 月以降の Web シェルの有無を調べるべき。
- 出典: [The Hacker News (2026-11-10)](https://thehackernews.com/2026/11/attackers-exploit-ahsaycbs-flaws-to.html)

### [2026-11-09〜10] Apple、iOS 27.2.1 などで 9 件を修正 (Bluetooth のペアリングの試行回数の制限の回避、iMessage のグループへの侵入など)。Binance は PoC が出た iOS のサンドボックス脱出「worse_query」を警告
- **何が起きたか**:
  - Apple は 11/9 に、iOS / iPadOS 27.2.1、26.7.3、18.7.12 と、macOS、watchOS、visionOS の更新を公開した。
  - 内容は、Bluetooth のペアリングコードの試行回数の制限の回避や、操作なしでのペアリング (CVE-2026-113964 / 113965 / 113968)、AirPlay の試行回数の制限の回避 (CVE-2026-113969)、遠隔からの iMessage のグループチャットへの参加 (CVE-2026-113961) など。
  - Binance は、iOS 26.7.1 / 27.0.1 / 27.2 の他アプリのファイルを読める問題「worse_query」を警告した。この手法を使って、脱獄なしで他アプリのデータを閲覧・編集できるツール「WQ Files」の PoC が公開されている。悪用には、サイドロードなどでアプリを入れさせる必要がある。
  - Apple が修正した CVE-2026-113963 (App Intents 経由で機微なデータにアクセスできる) が worse_query と同じものかは、Apple が確認していない。
- **悪用 / PoC**: worse_query は PoC が公開済み。暗号資産の被害は「未確認」(Binance)。Apple の 9 件に悪用の記載はない。
- **なぜ重要か (評価)**: シードフレーズや鍵をアプリのローカルに置くウォレットは、サイドロードのアプリ 1 つで抜かれうる。モバイルの診断では、アプリのコンテナ内にある秘密情報の保護を改めて確認したい。
- 出典: [SANS ISC (2026-11-10)](https://isc.sans.edu/diary/rss/33506) / [BleepingComputer (2026-11-10)](https://www.bleepingcomputer.com/news/security/binance-warns-of-ios-flaw-that-could-leak-crypto-wallet-secrets/) / [The Hacker News (2026-11-10)](https://thehackernews.com/2026/11/apple-patches-imessage-group-chat.html)

### [2026-11-10] X.Org、X サーバーと Xwayland の 8 件を修正。細工した EDID でメモリを壊せる (CVE-2026-109091)
- **何が起きたか**:
  - 修正版は xorg-server 21.1.26 と xwayland 24.1.15。
  - CVE-2026-109091 は、モニターから届く EDID の表示範囲の項目を、件数を確かめずに固定長の配列にコピーする問題。
  - CVE-2026-109092 / 109095 / 109096 / 109903 は、Xv と glamor でのサイズの負値や 32 ビットの桁あふれ。CVE-2026-109093 は、XTest でのスタックへの範囲外の書き込み。CVE-2026-109904 / 109094 は、32 ビット環境の X-Resource の整数オーバーフロー。
  - X.Org は CVSS を付けておらず、コード実行につながるかも示していない。10 月の 21.1.25 での 12 件の修正から約 1 か月での再リリース。
- **悪用 / PoC**: 悪用も PoC もなし。
- **なぜ重要か (評価)**: X サーバーが root で動く環境では、ローカルの権限昇格の材料になりうる。範囲外に書き込める 3 件 (109091 / 109092 / 109093) から優先して、ディストリビューションのバックポートを確認したい。
- 出典: [Help Net Security (2026-11-10)](https://www.helpnetsecurity.com/2026/11/10/x-org-server-vulnerabilities-november-2026/)

### [2026-11-10] Blind Eagle (APT-C-36)、コロンビアの検察などの通知を装う約 3,300 通のフィッシングで、AsyncRAT / DCRat 系の RAT を配布 (Zenox)
- **何が起きたか**:
  - 10 月下旬から 11 月上旬にかけて、スペイン語とポルトガル語で裁判所・検察・tutela (権利保護の訴え) の通知を装ったメールが送られた。
  - 添付の XHTML (SVG を武器化したもの) がコロンビアの Fiscalía のページを偽装し、HTML スマグリングでブラウザー内で ZipCrypto の ZIP を組み立てる。中の JS ドロッパーは偵察を行い、VBS で AMSI と ETW を回避し、MotW を消し、スタートアップに常駐する。最後に PowerShell で RAT をメモリ上で起動する。
  - Zenox は、ブラジルの基盤とタイムゾーンから、ブラジルの運用クラスターによる活動とみている。
- **悪用 / PoC**: 実際の攻撃のメールを観測。ただし侵害の成功は「確認できず」(Zenox)。
- **なぜ重要か (評価)**: SVG / XHTML とスマグリングで、メールのゲートウェイをすり抜ける手口の典型。メールに添付された SVG / XHTML を検査する対象にしているか、確認の材料になる。
- 出典: [The Hacker News (2026-11-10)](https://thehackernews.com/2026/11/blind-eagle-uses-fake-court-notices-to.html)

### [2026-11-09〜10] 米政策: トランプ大統領、CISA の長官に Palantir の Michael LoSapio 氏を指名。CISA はインシデントの報告フォームを MITRE ATT&CK の用語ベースに刷新
- **何が起きたか**:
  - The Record によると、大統領は 11/9 に LoSapio 氏を指名した。The Record は同氏を Palantir の CISO としているが、LinkedIn の経歴では 2024 年後半から CIO。
  - CISA は 2 期目のトランプ政権のもとで、上院の承認を受けた長官がいないままで、人員の 3 分の 1 (1,000 人超) を失っている。レームダック会期の上院で採決されるかは不透明。
  - CISA は同時期に、インシデントの報告フォームを改定した。マルウェア、ソーシャルエンジニアリング、ハッキングの手法、内部不正の区分と ATT&CK の用語で、複数の組織の報告から同じキャンペーンを見つけやすくする。ログインなしでも提出できる。
- **悪用 / PoC**: 該当なし。
- **なぜ重要か (評価)**: KEV や BOD を出す CISA の体制の行方は、米国外の脆弱性対応の優先順位にも影響する。報告フォームの ATT&CK 化は、インシデント対応のテンプレートを見直すきっかけになる。
- 出典: [The Record (2026-11-10)](https://therecord.media/michael-losapio-cisa-director-nomination) / [Help Net Security (2026-11-10)](https://www.helpnetsecurity.com/2026/11/10/cisa-incident-reporting-form-update/)


## 新規 CVE / Advisory (バリアントハント起点候補)
> 採用基準: 公開日 2026-11-09 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-111760 / [GHSA-vp2w-7xxj-jvxr](https://github.com/git/git/security/advisories/GHSA-vp2w-7xxj-jvxr) | Git (< 2.50.2 / 2.51.3 / 2.52.1 / 2.53.1 / 2.54.1 / 2.55.1 / 2.56.1) | CWE-59 相当 / 未採点 | `git clone --recursive` で攻撃者リポジトリのチェックアウト中に、submodule の gitfile (`.git` ファイル) を symlink で上書きできる → symlink 先の悪性 config / hooks が読まれ任意コード実行 | [advisory](https://github.com/git/git/security/advisories/GHSA-vp2w-7xxj-jvxr) (commit 不明) | 公開 11/10 (Git 協調リリース、NVD 未登録) / RCE / 攻撃者リポジトリ 1 つで成立 |
| CVE-2026-113408 | Git (同上) | CWE-22 / 未採点 | protocol v2 の `ls-refs` で、サーバが通知する unborn HEAD の symref-target (`refs/heads/../../../X`) を未検証のまま files ref backend に書く → パストラバーサルで任意ファイル書き込み | [diff](https://github.com/git/git/commit/b371db812524aa7831d3c3a9aed782defd1dcfb2) / [diff](https://github.com/git/git/commit/8cb7e2e031978c59381adf086fd1c0ce1e3a7315) | 公開 11/10 (NVD 未登録) / プロトコル由来なので libgit2・JGit・go-git・dulwich・isomorphic-git でも同じ問題が起きやすい |
| CVE-2026-105437 | Git (同上) | CWE-122 / 7.5 | `.gitattributes` の `conflict-marker-size` に巨大値を指定し、多数の conflict を含む三方向マージを行わせる → xdiff のマージバッファサイズ計算が `int` で wrap → heap overflow。forge 側の `git merge-tree` を PR 作成だけで叩ける | [diff](https://github.com/git/git/commit/288266c11d91a01239e8e17f4bd90f1276e30030) / [diff](https://github.com/git/git/commit/b1313872cefef5704a0acff14b7c0869a9d5dc7c) | 公開 11/10 (NVD) / forge サーバ側で発火 / 同時修正: CVE-2026-114467 (`remove_signature()` は署名 3 つ以上で stack 破壊, [diff](https://github.com/git/git/commit/aff587222342473034a270a3a04cfb1eba0a1117)) |
| CVE-2026-119192 / GHSA-6qrw-m8cv-hcxf | node-forge (< 1.4.1) | CWE-347 / 7.5 | RSA PKCS#1 v1.5 の verify が DigestInfo を寛容な BER パーサ `asn1.fromDer()` + `asn1.validate()` で検査する → NULL パラメータの中身・非最小長・非正規 OID を受け入れ、攻撃者が制御できるバイトが残る → e=3 の鍵で署名偽造 (BERserk / Bleichenbacher'06) | [diff](https://github.com/digitalbazaar/forge/commit/2bce9d477a2ff436e86ff9694ae999f1552aa2bb) | 公開 11/10 / X.509・PKCS#7 検証にも影響 / 純 JS・純 Python の自前 RSA 実装に横展開しやすい |
| CVE-2026-107846 / GHSA-8vv3-6qpc-gpw6 | bitcoinjs-lib (2.3.0–5.2.0, 6.0.0–6.1.7, 7.0.0-rc.0–7.0.1) | CWE-354 / CVSS4 Critical | `fastMerkleRoot` が奇数段で末尾ノードを自分自身と hash して埋めるが、mutated フラグを持たない。`checkTxRoots` も重複 tx を調べない → 同じ merkle root で別の tx リストを持つブロックが通る (CVE-2012-2459 の再発) | [diff](https://github.com/bitcoinjs/bitcoinjs-lib/commit/009f165edfbf925cad8964b2dce478d18dd19449) | 公開 11/10 / PoC あり (mainnet ブロックで再現) / 仕様由来のため Bitcoin Core 以外の merkle 実装にも横展開しやすい |
| CVE-2026-124077 | Apache Commons Codec `GitIdentifiers` (1.22.0–1.22.x) | CWE-158 / 未採点 | tree entry 名の NUL バイトを拒否しない → Git tree のシリアライズで、別のツリーが同じバイト列になる → 異なるツリーに同じ tree ID / SWHID が付く (ZIP 由来の名前などで発生) | [diff](https://github.com/apache/commons-codec/commit/87f6aa2818836998528ff4b0d1ea35545a800ee5) | 公開 11/09 / Git object を独自にハッシュする実装 (SWH、SBOM・来歴ツール) への横展開候補 |
| CVE-2026-102894 / GHSA-62m9-f875-rqw6 | GPUStack (0.7.1–2.2.1) | CWE-347 / 9.1 | `/auth/saml/callback` が SAMLResponse を Base64 デコードして NameID を読むが、`process_response()` (署名・issuer・audience・期限の検証) を呼ばずにセッション JWT を発行する。SAML 未設定でも有効 → 認証なしで管理者を乗っ取れる | [diff](https://github.com/gpustack/gpustack/commit/705edbe1b5feec63959306daecd640e1c70eced2) | 公開 11/10 / 同製品の CVE-2026-102895 が KEV 入り (11/09) / python3-saml を使う他の実装も「検証 API を呼ばない」パターンで点検したい |
| CVE-2026-62662 / GHSA-q4xm-p75h-h9p3 | Pocket ID (修正 8158452 より前) | CWE-863 / 6.8 | `client_credentials` grant で `resource` パラメータを未検証のまま JWT の `aud` に入れる → 任意の OIDC クライアントが他の RP 向けの正規署名トークンを取得できる | [diff](https://github.com/pocket-id/pocket-id/commit/8158452b37304115c97c61c3a56082ce938ce6f0) | 公開 11/09 / RFC 8707 (resource indicators) 由来のため、他の小規模 OIDC IdP にも横展開しやすい |
| CVE-2026-113663 / GHSA-2h4w-29cv-2cmv | ag2 (0.13.2–1.1.0) / autogen (0.13.2–0.14.1) | CWE-78 / 8.8 | `SandboxShellTool` の allowlist / readonly フィルタが単一行のメタ文字しか見ないまま、文字列を `sh -c` に渡す → 改行がコマンド区切りとして働き allowlist をバイパス → ホストで任意コマンド実行 (プロンプトインジェクション経由) | [diff](https://github.com/ag2ai/ag2/commit/3cd86726bb731eb11d6270f0ef9e50e42b5abb39) | 公開 11/10 / AI エージェントの shell ツールで共通する欠陥クラス |
| CVE-2026-84503 | ansible-core `ansible.builtin.git` | CWE-88 / 6.7 | リポジトリ URL を `--` 区切りなしの位置引数として `git ls-remote/clone/fetch` に渡す → `-` で始まる URL が `--upload-pack` 等のオプションとして解釈される → 任意コマンド実行 | [advisory](https://access.redhat.com/security/cve/CVE-2026-84503) (commit 不明) | 公開 11/09 / git ラッパー全般 (CI・デプロイツール、Go/Python の exec ラッパー) に典型的な引数インジェクション |
| CVE-2026-125120 / GHSA-pcrw-h46h-c93h, CVE-2026-125119 / GHSA-gg4r-jv3p-qx3c | Mongoose (125120: < 6.13.11 / 7.8.12 / 8.24.3 / 9.9.2、125119: 6.0.0– < 6.13.12 / 7.8.13 / 8.24.7 / 9.11.4) | CWE-943 / 9.8・7.5 | `sanitizeFilter` が `countDocuments()` に適用されない。接続レベルの指定は `Connection.config` に移されるが `_castConditions()` はそこを見ない → `{ $ne: null }` によるクエリセレクタインジェクションで認証バイパス・データ漏えい | [diff](https://github.com/Automattic/mongoose/commit/7e912af3fac52cb0eea4cd71e24d65318916831a) / [diff](https://github.com/Automattic/mongoose/commit/4bb659478be2f30655a7bdd78bc251bdf111cd29) | 公開 11/10 / 「防御オプションが一部のコードパスで効いていない」型 / 同日に prototype 汚染 CVE-2026-125117 も公開 |
| CVE-2026-63470 / GHSA-h667-4jj2-cgv4, CVE-2026-63471 / GHSA-p2mm-64f6-gmpp | fastapi-code-generator (< 0.8.1) | CWE-94 / CVSS4 Critical | OpenAPI の `summary` と path を、エスケープせずに生成コードの `"""` docstring / `@app.get('...')` リテラルへ埋め込む → 文字列を抜けて式を連結 → import 時またはハンドラ呼び出し時に RCE | [diff](https://github.com/koxudaxi/fastapi-code-generator/commit/49301dbdb82170d7f50877419d994b05cb1fa2bc) | 公開 11/09 / PoC あり / OpenAPI・GraphQL・protobuf から**コードを生成するツール全般**に横展開しやすい |

### 今日の CVE 所感
- **Git の協調リリース (11/10) が今日の本命**。CVE-2026-113408 (unborn HEAD の symref 未検証) はプロトコル v2 仕様から来る欠陥なので、libgit2・JGit・go-git・dulwich・isomorphic-git・forge 側のミラー実装で「サーバ通知の ref 名を `check_refname_format` 相当で検証しているか」を横断して確認したい。CVE-2026-111760 (gitfile の symlink 上書き) も、submodule を扱う他の実装で同じ点 (チェックアウト時の symlink 追従) を見る価値がある。
- **暗号・ハッシュの「正規形を強制しない」系が 3 件並んだ**。node-forge (DigestInfo の BER 寛容)、bitcoinjs (merkle の重複パディング)、Commons Codec (tree 名の NUL) は、いずれも有名な旧 CVE の再発です。独自実装の暗号・データ構造ライブラリを、既知の古典パターンに照らして監査する方針が引き続き有効です。
- **認証まわりは「検証 API を呼び忘れる」「パラメータを未検証のまま反映する」型**。GPUStack の SAML は `process_response` を呼ばず、Pocket ID は `resource` をそのまま `aud` に入れていた。SAML・OIDC を自前で組み込んでいる AI 推論基盤や小規模 IdP を優先して点検したい。
- **コマンド・コード生成の sink**: AG2 は改行で allowlist を抜け、ansible は `--` がなく、fastapi-code-generator は文字列リテラルを抜ける。どれも「文字列を組み立てて interpreter に渡す」型で、エージェントの shell ツールやコード生成ツールへの横展開がしやすい。


## 日本国内のセキュリティ動向

### 国内インシデント・事故

#### [2026-11-09] NTT データ: 住友生命から受託した「Vitality」の申し込みシステムに不正アクセス。利用者約 8 万人の個人情報が漏えい (カード番号の一部は約 1,000 人)
- **何が起きたか**: NTT データは 11/9、住友生命保険から構築・運用を受託しているシステムが不正アクセスを受けたと発表した。対象は「住友生命Vitality体験版・企業型」と「Vitalityスマート」(福利厚生タイプを含む) の申し込みのシステム。現在と過去の利用者の約 8 万人分の氏名、住所、電話番号、生年月日、メールアドレス、一部を伏せたカード番号のいずれかが漏れた。カード番号が漏れたのは約 1,000 人。保険契約の情報や歩数などのデータは含まれない。11/2 に不正アクセスを確認し、11/3 に外部からのアクセスを遮断してサービスを止めた。侵入の経路と原因は調査中。NTT データは、11/2 にも委託先経由の楽天証券の件 (362 件) を公表している。
- **なぜ重要か (評価)**: 大手 SIer が運用を受託したシステムでも侵害が続いている。委託元の診断では、受託先が運用する申し込みの系 (保険の本体とは別のサブシステム) も対象に入れ、責任の分界と監視の担当を確認すべきだ。
- 出典: [NTT データ (2026-11-09)](https://www.nttdata.com/global/ja/news/release/2026/110900) / [ITmedia NEWS (2026-11-10)](https://www.itmedia.co.jp/news/article/2611/10/2000003051/)

#### [2026-11-09] ラフール「ラフールサーベイ」: 2019 年に委託先が公開したイメージから AWS のアクセスキーが漏れ、利用企業 182 社の 2 万 4,232 人分が取得された (ストレスチェックの結果を含む)
- **何が起きたか**: 組織の状態を分析するツール「ラフールサーベイ」を提供するラフールは 11/9、旧システムが 7〜10 月に不正アクセスを受けたと発表した。利用企業 182 社の従業員 24,232 人分の従業員番号、氏名、所属、サーベイの回答と結果が取得された。一部の人については、ストレスチェックの結果や医師の面談の記録 (要配慮個人情報) も含まれる。原因は 2 つ重なった。同社のエンジニアがアクセスキーをプログラムに直接書き込んでいた。さらに 2019 年、当時の開発委託先 (フランジア、現 Sun Asterisk) の開発者が、そのプログラムを含むテスト用のイメージをネット上に公開した。7/30 に新システムへ移った後も、旧システムのファイル保管領域から 7/24〜10/25 にファイルが持ち出されていた。10/27 にログの確認で気づき、キーを無効にした。
- **なぜ重要か (評価)**: 公開されたコンテナイメージにキーが埋め込まれていた事例で、しかも移行後も旧環境のキーが生きていた。診断では、公開レジストリの過去のイメージにシークレットが入っていないかを調べ、移行の後に旧環境の認証情報を棚卸しすべきだ。
- 出典: [ITmedia NEWS (2026-11-10)](https://www.itmedia.co.jp/news/article/2611/10/2000003052/)

#### [2026-11-09] ラクスル: データ入稿のシステムの認証情報を盗まれ、印刷データ (名刺やはがきに書かれた第三者の情報を含む) が漏れたおそれ。件数は調査中
- **何が起きたか**: ラクスルは 11/9、印刷通販「ラクスル」のデータ入稿の処理に関わるシステムに不正アクセスがあったと発表した。11/8 0 時 20 分ごろに気づいた。システムの認証情報が盗まれ、保管データの一部に外部からアクセスできる状態だった。入稿された印刷データ、請求書、Web 郵便のデータに書かれた氏名、会社名、住所、電話番号、メールアドレスなどが漏れたおそれがある。印刷物に書かれた、注文者以外の人の情報も含まれうる。カード情報、ログイン ID、パスワードは漏れていないという。件数と期間は調査中。入稿を伴う一部のサービスを 11/8 に止め、11/9 7 時から順に再開したが、「ラクスル パッケージ」や Adobe Express との連携などは止まったままだ。
- **なぜ重要か (評価)**: 利用者がアップロードしたファイルの保管領域が狙われ、注文者以外の情報まで漏れる型だ。診断では、入稿ストレージへのアクセス権限、署名付き URL の有効期限、サービス用の認証情報の保管場所を確認したい。
- 出典: [ラクスル (2026-11-09)](https://corp.raksul.com/news/press/261109_unauthorized-access/) / [ITmedia NEWS (2026-11-09)](https://www.itmedia.co.jp/news/article/2611/09/2000003004/)

#### [2026-11-09] [続報] 良品計画: ネットストアの再開を延期。リスト型攻撃を受け、新たに約 27 万件が漏れた可能性。代引きの受取先約 44 万件も追加
- **前回から何が変わったか**: 良品計画は 11/9、11/6 から止めている「無印良品ネットストア」の再開を延期すると発表した。外部で盗まれた ID とパスワードを使ったリスト型攻撃を受け、新たに約 27 万件 (メールアドレス、生年月日、氏名、住所、電話番号、購入履歴、ポイント) が漏れた可能性がある。既に公表していた最大約 2,726 万件のうち、氏名・住所・電話番号を含むものを約 52 万件から約 75 万件に改めた。さらに、2020/1/2〜2025/2/10 に受注した代金引換の受取先約 44 万件も漏れた可能性がある。再開時には、全利用者にパスワードの再設定を求める予定。
- **なぜ重要か (評価)**: 大規模な漏えいの直後には、漏れた認証情報を使ったリスト型攻撃が続く。診断では、ログインのレート制限、異常なログインの検知、侵害されたパスワードの照合が効いているかを確かめたい。
- 出典: [ITmedia NEWS (2026-11-09)](https://www.itmedia.co.jp/news/article/2611/09/2000003038/)

#### [2026-11-09] 札幌市交通局: 「さっぽろえきバスナビ」の配信システムが不正アクセスを受け、事実と異なる運行情報が配信された
- **何が起きたか**: 札幌市交通局は 11/9、6 時 35 分ごろと 12 時 10 分ごろに「さっぽろえきバスナビ」の配信システムが外部から不正アクセスを受け、事実と異なる運行情報が配信されたと発表した。12 時 40 分ごろに、交通局の公式サイトの一部とえきバスナビを止めた。止めている間は、駅の電光掲示板と市の公式 SNS で情報を出す。個人情報の漏えいは確認されていない。
- **なぜ重要か (評価)**: 情報を盗まれたのではなく、公共交通の案内を改ざんされた件だ。自治体や交通事業者の診断では、運行情報を配信する管理画面や API の認証を、改ざんの観点で優先して見るべきだ。
- 出典: [札幌市交通局 (2026-11-09)](https://www.city.sapporo.jp/st/trouble/r081109_homepageteijshi.html) / [INTERNET Watch (2026-11-10)](https://internet.watch.impress.co.jp/docs/news/2155064.html)

#### [2026-11-10] マイナンバーカードを使うコンビニ交付で障害。20 都道府県の少なくとも 38 自治体が公表 (富士フイルムシステムサービスのネットワークの通信異常か)
- **何が起きたか**: 11/10 朝から、コンビニ交付で戸籍謄本などを取得できない障害を各地の自治体が相次いで公表した。11 時 30 分時点で、20 都道府県の少なくとも 38 自治体 (港区、世田谷区、杉並区、豊田市、長崎市など)。愛知県知多市などは、富士フイルムシステムサービスの「コンビニエンスストア証明発行システム」が使うネットワークで 6 時 30 分に通信異常が起きたと説明した。原因は調査中で、復旧の時期は未定。一部の自治体では、住民票の写しや印鑑登録証明書などもまとめて止まった。14 時時点で、同社からの公表は確認されていない。サイバー攻撃かどうかは明らかになっていない。
- **なぜ重要か (評価)**: 多くの自治体が 1 つの事業者の共通基盤に頼っているため、1 か所の障害が全国に広がった。原因がまだ分からないので、続報を追う。
- 出典: [ITmedia NEWS (2026-11-10)](https://www.itmedia.co.jp/news/article/2611/10/2000003062/)

### 国内の注意喚起・ガイドライン・政策

#### [2026-11-09] 国家サイバー統括室、「産業用冷凍・冷蔵設備およびコールドチェーン監視システムに関する注意喚起」を事業者向けに公表
- **何が起きたか**: 国家サイバー統括室 (NCO) の対処調整・官民連携等ユニットは 11/9、食品・小売、物流倉庫、医療施設の冷凍・冷蔵設備を扱う事業者に向けて注意喚起を出した。欧州では約 700 店舗のスーパーや血液製剤の保管施設で、遠隔監視システムが不正に操作された。冷却を止められたり、除霜ヒーターを連続で動かされたりした。注意喚起は次の 5 つを求めている。(1) 制御機器をインターネットから直接触れないようにし、ネットワークを分ける。(2) 初期パスワードを変え、不要な保守用アカウントを止める。(3) 異常な温度を設定できないよう、上限の「安全リミット」を有効にし、パッチを当てる。(4) 設備保守の委託先の遠隔保守回線を管理する。(5) 独立した温度監視と、緊急時の初動を用意する。CERT-FR と CISA の資料も紹介している。仏外務省は 11/9、10 月の小売店への攻撃をイランによるものと断定した。
- **なぜ重要か (評価)**: 国内でも、冷凍・冷蔵のコントローラーは IT の資産台帳から漏れやすく、保守業者の回線経由で外に出ていることが多い。外部の攻撃対象 (ASM) の調査や OT の診断で、範囲に入れる根拠になる。
- 出典: [国家サイバー統括室 (2026-11-09, PDF)](https://www.cyber.go.jp/pdf/press/261109_taiou.pdf) / [INTERNET Watch (2026-11-10)](https://internet.watch.impress.co.jp/docs/news/2155155.html)

#### [2026-11-10] 福岡県警などの合同捜査本部、不正アプリでスマホを遠隔操作し、決済サービスで商品をだまし取った疑いで中国籍の男 2 人を逮捕。同じ手口での逮捕は全国初
- **何が起きたか**: 福岡県警などの合同捜査本部は 11/10 までに、男性にダウンロードさせた不正アプリでスマートフォンを遠隔操作し、決済サービスを使って商品をだまし取ったとして、中国籍の男 2 人を詐欺などの疑いで逮捕した (共同通信の配信)。同じ手口の被害は相次いでおり、逮捕は全国初という。各県警は 10 月から、SNS の広告や SMS のリンクから不正アプリを入れさせ、キャッシュレス決済を遠隔で操作する手口に注意を呼びかけていた。
- **なぜ重要か (評価)**: 不正アプリを入れた端末から決済アプリを直接操作されると、ログインを守る対策だけでは防げない。決済アプリの診断では、遠隔操作 (アクセシビリティ機能の悪用など) の検知や、高額決済時の追加の確認を見るべきだ。
- 出典: [新潟日報 (共同通信, 2026-11-10)](https://www.niigata-nippo.co.jp/articles/-/939984) / [山陰中央新報 (共同通信, 2026-11-10)](https://www.sanin-chuo.co.jp/articles/-/1113103)

#### [2026-11-09] 総務省、日 ASEAN サイバーセキュリティ能力構築センター (AJCCBC) で、民間企業と連携した演習を実施 (11/2〜6、バンコク)
- **何が起きたか**: 総務省は 11/9、AJCCBC (タイの国家サイバーセキュリティ庁の庁舎内) で 11/2〜6 に、ASEAN 各国の政府関係者や重要インフラ事業者を対象とした演習を行ったと発表した。内容は、LLM や生成 AI を使ったプログラム開発と脆弱性の発見、ログによる攻撃の検知、クラウドと Web アプリの保護。協力は AppGuard、網屋、サイバーセキュリティクラウドなどで、次年度も行う予定。
- **なぜ重要か (評価)**: 政府の研修で「AI を使った脆弱性の発見」が標準の科目になってきた。国内の CYDER などでも、同じ流れが進みそうだ。
- 出典: [総務省 (2026-11-09)](https://www.soumu.go.jp/menu_news/s-news/01cyber01_02000001_00310.html)

> 補足: Microsoft の 11 月の月例更新 (米国 11/10) について、IPA の「Microsoft 製品の脆弱性対策について (2026年11月)」と JPCERT/CC の注意喚起は、11/11 05:19 JST の時点では出ていない (IPA の 1111-ms.html と JPCERT の at260035.html はどちらも 404)。いつもは 11/11 の午前中に出るので、出ていれば最終版で追記する。JPCERT/CC の CyberNewsFlash (OpenSSH, 11/9) は前号で取り上げたため省いた。

### 国内製品の脆弱性 (JVN)

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| 2026-11-10 (更新) | JVN#12040144 [続報] | Airbyte 2.2.0 未満 / Airbyte (報告: ZOZO 兵藤壮泰 氏) | 安全でないリフレクション (CWE-470) で Connector Builder / ManifestServer から任意のコードを実行できる。11/10 の更新で「**悪用を確認**」と追記され、影響を受ける版が「1.7.0〜2.1.0」から「2.2.0 より前」に広がった | v4 8.7 / v3 8.8 (緊急)、悪用あり | [JVN](https://jvn.jp/jp/JVN12040144/) |
| 2026-11-10 | JVNVU#98836795 / CVE-2026-124916 | PrestaShop (9.2.1 で修正) | 管理画面の「Performance > Debug」で、デバッグ用 Cookie の名前と値がエスケープされずに `defines.inc.php` に書き込まれ、PHP コードを注入できる (要: 管理者の権限) | 認証済みの RCE (CERT/CC VU#385711) | [JVN](https://jvn.jp/vu/JVNVU98836795/) |
| 2026-11-10 | JVNVU#96830794 / CVE-2026-121685〜121690 | FrodoBots EarthRover Mini+ ファームウェア 6.2.4_6.2.5_0.614.0 | 全台共通の認証情報 (AWS IAM キー、AWS IoT MQTT、Slack の Webhook) がファームウェアに埋め込まれている。MQTT 経由の未認証のコマンド実行、認証なしのローカル API、HTTP での更新、全プロセスが root で動く | 未認証の RCE、全台の乗っ取り (CERT/CC VU#188754) | [JVN](https://jvn.jp/vu/JVNVU96830794/) |
| 2026-11-10 | JVNDB-2026-042606 / CVE-2026-120201 (ほか CVE-2026-111605、CVE-2026-91993) | Jpom 2.10.0〜2.11.12 / Dromara | `JPOM-USER-TOKEN` ヘッダーに「is not null」などの条件を注入すると、Hutool の条件パーサーを通って最上位の管理者になり、スクリプト機能でコマンドを実行できる。ほかに、ワークスペースをまたいで SSH ホストやリポジトリに触れる IDOR が 2 件 | v3 9.8 (最大) | [JVN iPedia](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-042606.html) |
| 2026-11-10 | JVNDB-2026-042590 / CVE-2026-102925 | virtualenv 21.7.13 未満 | 生成される activate スクリプト (bash / zsh / fish) で、エスケープ済みの値を別の引用の中に二重に入れていた。細工した仮想環境のパスや Tcl/Tk のパスで OS コマンドを注入できる | v3 7.8 | [JVN iPedia](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-042590.html) |

> 補足: 期間内に国内ベンダーの製品 (JVN#) の新規公開はなかった。11/9 公開分 (WebSAM WinShare、SS1、KUSANAGI、Effekseer、Webtop、Zabbix agent、Siemens) は前号に載せたため省いた。JVN iPedia の 11/10 登録分のうち、GPUStack (CVE-2026-102895)、FreeSWITCH (CVE-2026-116779)、SonicOS (CVE-2026-19868)、OpenSSH (CVE-2026-123158) は既出なので除いた。JVN iPedia の個別ページは 05 時 (JST) の時点でまだ 404 で、表の内容は RSS の記述によるものだ。

### 国内コミュニティ・研究・イベント

#### [2026-11-09] NRI セキュア、「外部公開資産をどう把握するか」: 10 月の 9 機関の注意喚起と PHP2Shell から、委託先とグループ会社を含めた ASM の必要性を読み解く
- **何が起きたか**: NRI セキュアのブログ。10/7 の個人情報保護委員会から約 1 週間で出た 9 機関 (NCO、IPA、JPCERT/CC、個情委、経産省、金融庁、NICT など) の注意喚起を並べて読み、共通点を「外に何をさらしているかを把握できていない」とまとめた。例として、個情委の「台帳に載っていない海外拠点の VPN 装置」、NICT の「A2B 攻撃」(公開アプリを解析してサーバーを狙う)、JPCERT/CC の「AI のペンテスト基盤を悪用した探索」を挙げている。PHP2Shell (CVE-2026-109618 / 109619) では「どこで PHP が動いているか分からない」という問題が表に出た。
- **なぜ重要か (評価)**: 「内部向けのつもりで外から見えていた」BI ツールや管理画面が、一連の漏えいの起点になっている。外部診断の範囲を決める前に、委託先とグループ会社を含む資産の洗い出しを提案する材料になる。
- 出典: [NRI セキュア ブログ (2026-11-09)](https://www.nri-secure.co.jp/blog/php)

#### [2026-11-10] Zenn: SSH ハニーポット (Cowrie) の 28 日分のログを数え直したら、「攻撃は日曜だけ少ない」以外の思い込みは外れた
- **何が起きたか**: 個人の研究者が、10/1〜10/29 に動かした Cowrie のログを Python と DuckDB で数え直した。「10/8 が山」は、ログを見た時刻で区切ったための見かけで、実際は 10/7 の多さだった。「土日は少ない」は外れた (土曜の平均は 5,112 回、平日は 5,695 回)。「日曜だけ少ない」(平均 3,152 回、平日の約 55%) は残った。並べ替えの検定では約 0.1% (曜日の選び方を補正すると約 1%) だった。
- **なぜ重要か (評価)**: 集計の単位 (タイムゾーン、区間、1 台の発信元を全体とみなす誤り) で結論が変わる。SOC のレポートや診断報告の統計を書くときの、良い反面教師になる。
- 出典: [Zenn (2026-11-10)](https://zenn.dev/miki_mini/articles/5850f7a592d155)

#### [2026-11-10] Qiita: URL にトークンを書いて git clone すると .git/config に平文で残る。AI エージェントが `git remote -v` を実行するとログに入る
- **何が起きたか**: git 2.47.3 で確かめた記事。`https://x-access-token:<トークン>@...` の形で clone すると、トークンは `.git/config` に平文で残る。`git remote -v`、tar での固め、`GIT_TRACE=1` の出力にもそのまま出る (接続失敗のエラー文では伏せられる)。`transfer.credentialsInUrl=warn|die` で警告または停止にできる。ただし `pushurl` は検出しない。
- **なぜ重要か (評価)**: CI の手順書によくある書き方が、AI エージェントの会話ログやソースのアーカイブからのトークン漏れにつながる。ソースコード監査や開発環境の診断のチェック項目に足せる。
- 出典: [Qiita (2026-11-10)](https://qiita.com/supportapp3/items/5056f41f39af8c1f8ed0)


---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 70 本。内訳は RSS / Atom が約 55 本 (JVN、JVN iPedia、JPCERT/CC、IPA、piyolog、Security NEXT、ScanNetSecurity、ITmedia、BleepingComputer、The Hacker News、SecurityWeek、Help Net Security、The Record、Dark Reading、SANS ISC、ZDI、Check Point Research、TechCrunch、The Verge、Ars Technica、Simon Willison、Hugging Face、OpenAI、Google AI、Publickey、GIGAZINE、arXiv など) と、API (CISA KEV JSON、NVD の 11/09〜11/11 公開の 2,163 件、8 エコシステムの OSV、EPSS)。不足分は WebSearch で補った。
- 採用件数: AI技術=12 / AIセキュリティ=8 / セキュリティ=16 / CVE=12 / 国内インシデント=6 / 国内政策=3 / JVN=5 / 国内コミュニティ=3
- 除外理由の内訳: 古すぎ=約 25、重複=約 55、日付不明=約 3
  - 古すぎ: Ivanti ICS の追加の 2 件、CERT-In の AI ガイドライン、Arete-27B、阪急阪神 / H2O の第 2 報 (10/30)、花キューピット、ドトールなど。
  - 重複: Fable / Mythos 5.2 の本体、Qubole、sshole、FreeSWITCH / Aspera、ニトリ、シェアフル、JVN の 11/9 公開分、GPUStack の CVE-2026-102895 など。
  - 日付不明: OpenAI Control Room の詳細、Notebookcheck の Fable の記事など。
- 取得失敗ソース:
  - Dark Reading の記事ページ (403。RSS の日付と二次情報で代用)
  - openai.com の記事本文 (403。RSS の概要で代用)
  - GitHub API / GHSA の HTML (このセッションでは使えず、OSV・NVD・Git の RelNotes・`git ls-remote` で代用)
  - Tenable / Rapid7 / MSRC の Patch Tuesday の記事 (未取得。BleepingComputer、ZDI、SecurityWeek、SANS ISC で代用)
  - ラフールの公式サイト (502。ITmedia で代用)
  - LAC の RSS (404)、GMO イエラエの feed (HTML が返った)、JVN iPedia の 11/10 登録分の個別ページ (404)
  - VentureBeat / HiddenLayer / Lakera / DeepMind の RSS (XML の解析に失敗)
- 備考:
  - Git の CVE-2026-111760 / 113408 などは NVD・OSV に未登録のため、公開日は同時リリースの CVE-2026-105437 (NVD 公開 11/10) と GitHub Blog の日付で判断した。
  - Xen Orchestra (VSA-2026-062) と SGLang の RCE は CVE が未採番か未登録のため、CVE の表には入れず、ニュースの欄で扱った。
  - Microsoft 11 月の更新に関する IPA と JPCERT/CC の注意喚起は、生成時点 (11/11 05:20 JST ごろ) では未公開だった。
  - Fortinet / Siemens / Ivanti の 11/10 の定例の情報は、確認できなかった。

</details>
