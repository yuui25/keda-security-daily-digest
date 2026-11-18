# KEDA Daily Digest — 2026-11-19 (JST)

> 採用範囲: 公開日 2026-11-17 〜 2026-11-19
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

前号で「技術詳細は 11/18 に公開予定」と書いた **Java4Shell (CVE-2026-114938) の全容が出た号**。同じ 11/18 に **NGINX の HTTP/2 で 2015 年から続く未認証 RCE (CVE-2026-123007「nginx2root」)** と F5 BIG-IP の Critical 6 件も出た。Java と NGINX という、診断先のほぼ全部にあるソフトに同じ日に重大な問題が出たことになる。
AI 技術の大型発表は少なかった。Google DeepMind が Genie 4 を AI Ultra 向けに公開し、OpenAI は Codex のサンドボックスの作りとチップ設計への応用を解説した。NVIDIA は決算で中国向け H200 の出荷をやめたと明らかにした。
AI セキュリティでは、**Microsoft Agent Framework の PyPI パッケージ (月約 20 万 DL) に資格情報を盗むコードが入った**。Wiz によると、攻撃者は Microsoft の署名・公開基盤 ESRP のクライアント証明書を使い、オープンソースの AI ペンテスト基盤「Cairn」で作業していた形跡がある。ZDI は Docker Model Runner からホストへ抜ける手口を、Rapid7 はネットに公開された Ollama の半数超に他人が触った跡があることを報告した。
セキュリティでは、CISA KEV に 11/18 付で 4 件 (Apache Axis、LiteLLM、REDCap、Synology DSM) が入り、そのうち 3 件は対応期限が 3 日後の 11/21。Apache Roller の CVE-2026-129448 は ASF が「悪用中」と明記した。
国内では、**KARTE の件で三菱 UFJ 銀行 (約 650 万件)、三菱 UFJ 信託銀行 (約 23 万件)、ウェルスナビ (約 91 万人) が 11/18 に漏えいを公表**した。NewsPicks は調査報告で、Metabase の SQL インジェクションを修正する前に侵入されていたと明らかにした。JPCERT/CC と IPA は Java4Shell の注意喚起を出した。
**今日まず見るべき 2 件**: (1) Java 17.0.6 以降を AVX-512 VBMI 対応の x86-64 で動かしているサーバーを洗い出し、更新するか起動オプションで止める (深掘り参照)。(2) NGINX で HTTP/2 を有効にしている入口を確かめ、1.31.9 / 1.30.7 に上げる。

## 今日の深掘り

### [2026-11-17〜18] [続報] Java4Shell (CVE-2026-114938) の技術詳細が公開。OpenJDK の Base64 デコーダの AVX-512 用アセンブリが範囲外に書き込み、Keycloak・Jira・Jenkins など 6 製品で既定の設定のまま未認証 RCE

- **概要 (事実)**:
  - Calif は 11/17 (米国時間) に技術解説を公開し、OpenJDK と Oracle は同じ日に修正版を出した。前号の時点では、Oracle の CSPU と同時に名前と影響だけが先に知られていた。今回の差分は「仕組み・攻撃の成立条件・PoC」が公開された点にある。
  - CVSS は Calif の評価が 4.0 で 9.2、Oracle が 3.1 で 8.1 (AC:H、PR:N)、Red Hat の暫定値が 9.8、Amazon が 8.8。
  - **既定の設定のまま未認証で RCE**: Keycloak、Atlassian Jira、Atlassian Confluence、JFrog Artifactory、Jenkins、PingFederate。**ログインが必要な RCE**: Apache Kafka Broker、Apache Solr、Elasticsearch、Gerrit、Spinnaker。Calif はこの一覧が網羅的ではないとし、Struts や Spring Boot で作ったサンプルのアプリでも RCE を示した。
  - **悪用**: CISA、JPCERT/CC、カナダの Cyber Centre は、いずれも悪用を確認していない。KEV にも入っていない (11/18 時点の THN の確認)。EPSS は 0.0073。
  - **PoC**: メモリ破損を再現する自己完結型の PoC は公開された。6 製品向けの攻撃コードは公開されていない。Upwind と Blackpoint はクラッシュとメモリの読み出しまでは再現したが、RCE は再現していない。
- **技術的な中身**:
  - **場所**: HotSpot の Base64 デコードのイントリンシック。これは AVX-512 VBMI を使う手書きのアセンブリで、デコーダが JIT でコンパイルされ、よく通る処理になってから使われる。
  - **欠陥**: 末尾の数文字を処理する部分で、余分な `=` を誤って扱い、出力の長さを負の値として計算する。その値が 64 バイトの書き込みになり、配列の終わりから **62〜63 バイト先まで書き込む**。入力は最終的に不正として弾かれるが、書き込みはその前に終わっている。引き金は `A` を 64 個並べて `=` を 1 個付けた文字列 (古い 17 系では `A` が 128 個)。
  - **書き込みを使える形にする手順**: 書き込む値は固定で、攻撃者が決められるのは書き込む位置だけ。そこで Calif は、隣の配列の長さを書き換えて「自由な値を書ける配列」を作った。さらに別の配列で読み戻すことで、ヒープの中身を読み出せるようにした (Calif はこれを「JavaBleed」と呼ぶ)。そこから G1 GC の領域の配置を整え (heap feng shui)、コード実行に届かせている。
  - **入口**: 認証の前に Base64 をデコードする処理すべて。HTTP Basic のヘッダー、SAML artifact、CSRF トークン、ファイルのアップロードなどがある。samczsun による、**悪意あるサーバーに TLS で接続しただけでクライアント側が乗っ取られる**エクスプロイトもあるが、経路は公開されていない。
  - **条件**: Java 17.0.6 以降の 17 系、21、25、27 (8u511b33-perf と GraalVM の各版も)。標準の Java 8 と 11 には該当コードがない。CPU は Intel Xeon の Ice Lake / Sapphire Rapids / Emerald Rapids / Granite Rapids と AMD Zen 4 以降に限られ、ARM64 は対象外。**同じコンテナイメージでも、載るホストの CPU によって脆弱かどうかが変わる**。
  - **攻撃の難しさ**: どこでも通る単一のエクスプロイトはなく、製品ごとにメモリの配置とタイミングを合わせる必要がある。nginx の既定のように、リクエストを最後まで受け取ってから転送するプロキシは、一部の攻撃を防ぐが全部は防げない。失敗すると JVM が落ちるが、何度でも試せることが多い。
  - **修正**: Oracle は 17.0.21.1 / 21.0.13.1 / 25.0.5.1 / 27.0.1.1。Corretto は 17.0.21.1.2 など。Red Hat の修正は THN の記事の時点ではまだ準備中だった。回避策は `-XX:-UseBASE64Intrinsics` または `-XX:UseAVX=2` で、x86-64 にだけ付ける。ARM の JVM はこのフラグを知らず、起動に失敗する。
- **背景・経緯 (背景引用)**:
  - Calif は同じ年に PHP2Shell と Squidbleed (1997 年から Squid の FTP モジュールにあったバグ) を発表しており、今回も「必要のない最適化のコードがすべての利用者に配られている」と主張している。
  - 発見者は Codex に JIT・イントリンシック・暗号の部分を重点的に調べさせて見つけた。Calif によると、脆弱性の発見に約 1 時間、最初のエクスプロイトに約 2 時間かかり、トークン代は 200 ドル未満だった (Calif の主張)。11/17 号で扱った GTIG の「exploit_agent」や、前号の GPT-6.2 のシステムカードの「Critical」の判定と同じ流れにある。
- **なぜ今これが重要か (評価)**:
  - Log4Shell と違い、**ライブラリの依存関係をスキャンしても見つからない**。見るべきなのは「JDK の版 × ホストの CPU × 認証の前の Base64 デコード」の組み合わせで、SBOM だけでは判断できない。
  - 攻撃の難しさから、すぐに大量の悪用が起きる可能性は低めとみる。ただし、情報が漏れるだけの段階 (JavaBleed) は再現が比較的容易で、Blackpoint の試験では 30 回中 30 回成功した。認証基盤 (Keycloak、PingFederate) が対象に入っているため、漏れるだけでもトークンや秘密鍵に届きうる。
  - 診断の観点では、「Base64 を受け取る認証前の入口」を棚卸しすることが、そのまま攻撃面の地図になる。
- **読者が今日できること**:
  - Linux のホストで `grep -m1 '^flags' /proc/cpuinfo | tr ' ' '\n' | grep -E '^(avx512f|avx512bw|avx512vbmi|bmi2)$'` を実行し、4 つすべてが出るかを確かめる。出るホストの `java -version` を一覧にする。クラウドなら、インスタンスの種類から CPU の世代を引く。
  - すぐに更新できない JVM には `-XX:-UseBASE64Intrinsics` を付ける。コンテナのイメージを ARM と x86 で共用しているなら、`JAVA_TOOL_OPTIONS` を x86 のノードにだけ付ける (ARM では起動しなくなるため)。
  - 診断では、Basic 認証、SAML、CSRF トークン、アップロードなど「認証の前に Base64 を受け取るパラメータ」に `A`×64 + `=` を送り、500 エラーや応答時間の変化を見る (本番では JVM が落ちるおそれがあるため、事前の合意が前提)。
- 出典: [Calif (技術解説)](https://calif.io/java4shell/) / [OpenJDK Vulnerability Advisory 2026-11-17](https://openjdk.org/groups/vulnerability/advisories/2026-11-17) / [oss-security](https://seclists.org/oss-sec/2026/q4/757) / [The Hacker News](https://thehackernews.com/2026/11/java4shell-cve-2026-114938-enables-pre.html) / [The Hacker News (CISA)](https://thehackernews.com/2026/11/cisa-urges-immediate-patching-of.html) / [Help Net Security](https://www.helpnetsecurity.com/2026/11/18/java4shell-openjdk-vulnerability-cve-2026-114938/) / [JPCERT/CC CyberNewsFlash](https://www.jpcert.or.jp/newsflash/2026111801.html) / [GIGAZINE](https://gigazine.net/news/20261118-java4shell/)

## AI 技術・トレンド

### [2026-11-18] Google DeepMind、世界生成モデル「Genie 4」を Google AI Ultra の加入者向けに公開
- **何が起きたか**: DeepMind は、Project Genie で Genie 4 の提供を始めた。対象は条件を満たす AI Ultra の加入者で、AI Pro の加入者は順番待ちになる。自然言語で環境をその場で編集でき、音声も生成でき、作品を共有するギャラリーも用意した。Genie 3 も、長いセッション、パノラマを基にした生成、複数の世界をつなげる機能に対応した。
- **なぜ重要か**: 操作できる 3D 環境をすぐに作れる世界モデルは、エージェントの学習やシミュレーションの基盤として使われ始めている。セキュリティの面では、生成した環境を使った UI の偽装や、エージェントの評価環境の汚染が今後の論点になる。
- 出典: [Google DeepMind](https://deepmind.google/blog/genie-4-is-now-available/)

### [2026-11-18] OpenAI、Codex のサンドボックスの仕組みを解説 (macOS / Linux / Windows)
- **何が起きたか**: OpenAI は、Codex が利用者のマシンでコマンドを実行するときに、利用者が決めたファイルシステムとネットワークの制限を、OS ごとにどう強制しているかを解説する記事を公開した (本文は 403 で取得できず、RSS の要約による)。
- **なぜ重要か**: Java4Shell の発見でも Codex が使われたように、コーディングエージェントは強い権限でローカルで動く。サンドボックスの境界が文書化されると、診断する側は「どこまでが設計で保証されているか」を突き合わせる基準を持てる。前日に Simon Willison が出した「外部サンドボックス」の考え方 (後述) と読み比べるとよい。
- 出典: [OpenAI (RSS)](https://openai.com/index/inside-the-codex-sandbox)

### [2026-11-18] OpenAI、自社モデルでチップの回路と RISC-V コアの設計を改善したと発表
- **何が起きたか**: OpenAI は、GPT-6 Astra を使って、自社チップ「Jalapeño」に使う回路を最適化し、RISC-V コアの設計を改善したと発表した (RSS の要約による。具体的な数値は取得できず)。
- **なぜ重要か**: AI の研究所が自前の半導体の設計に自社のモデルを使い始めた。HDL や回路のネットリストも LLM が書き換える対象になれば、ハードウェアの設計の流れにも、コードと同じ「生成物の検証」と「供給網」の問題が持ち込まれる。
- 出典: [OpenAI (RSS)](https://openai.com/index/advancing-chip-design-with-our-models)

### [2026-11-18] NVIDIA、決算説明会で中国向け H200 の出荷をやめたと表明
- **何が起きたか**: 暫定 CEO の Colette Kress 氏は、11/18 (米国時間 11/17) の決算説明会で、業績の見通しに許可制の Hopper 製品を含めておらず、中国への出荷もやめたと述べた。米政府は 2025 年 12 月に H200 の中国への出荷を認めていた。理由は説明しなかった。
- **なぜ重要か**: Huang 氏の退任 (前週) と、米商務省の「海外データセンターの遠隔利用」規制 (11/17 号) の直後の方針転換になる。中国系のモデルの開発元が国産の半導体へさらに移れば、中国系のオープンウェイトのモデルの性能と供給の見通しが変わる。
- 出典: [The Verge](https://www.theverge.com/tech/1036445/nvidia-h200-ai-chips-china-stop-selling) / [GIGAZINE](https://gigazine.net/news/20261118-nvidia-ends-to-sell-chip-to-china/)

### [2026-11-17] GitHub、エージェントのセッションを端末をまたいで続ける「Agent Host Protocol」を解説
- **何が起きたか**: GitHub は、VS Code で作り GitHub 全体で採用した、オープン規格「Agent Host Protocol (AHP)」の設計を公開した。Copilot のエージェントのセッションを、エディタ、アプリ、スマートフォン、クラウドの間で引き継ぐための仕組みで、自前のアプリに組み込む方法も説明している。
- **なぜ重要か**: エージェントが「何時間も、何日も」動く前提で、セッションを外から操作する口が標準化されつつある。前号の「デバイスコードのフィッシングで Copilot CLI を遠隔操作」と合わせると、セッションの引き継ぎの認可が新しい攻撃面になる。
- 出典: [GitHub Blog](https://github.blog/engineering/engineering-principles/building-the-agent-host-protocol-for-sessions-that-continue-across-devices/)

### [2026-11-17] Simon Willison と Prime Radiant、エージェントの外にサンドボックスを置く「external sandbox」の実装を 3 種公開
- **何が起きたか**: エージェント本体はサンドボックスの外に置き、エージェントが実行するコードだけを専用のサンドボックスで動かす設計を提案した。その一つの external-sandbox-v86 は、Node.js のサーバーから v86 を使い、WebAssembly の中で Alpine Linux を動かす。目的は、ローカルのモデルを、プロンプトインジェクションや誤操作を心配せずに試せるようにすること。
- **なぜ重要か**: 「エージェント全体をサンドボックスに入れる」のではなく、「実行だけを隔離する」という分け方は、エージェントの認証情報をサンドボックスの中に置かずに済む。ローカルの LLM を検証するときの環境づくりに、そのまま使える。
- 出典: [Simon Willison's Weblog](https://simonwillison.net/2026/Nov/17/external-sandboxes-for-coding-agents/)

### [2026-11-18] curl の Daniel Stenberg 氏: エージェントによる Rust への書き換えの間に、本家は 200 件超のバグを直した
- **何が起きたか**: Stenberg 氏は、エージェントが curl の C コード 18.5 万行を Rust 34 万行に書き換えていた約 3 週間の間に、本家の curl には 300 超のコミットが入り、200 件ほどのバグ修正と脆弱性の修正があったと書いた。書き換え版にはその修正が入っていないと指摘した (Simon Willison の引用による)。
- **なぜ重要か**: AI による「丸ごと書き換え」は、元の実装の修正に追いつけない限り、すぐに古い脆弱性を抱えたフォークになる。CVE を追う側から見ると、こうしたクローンは「本家で直った CVE が残っている派生物」として、バリアントハントの対象になる。
- 出典: [Simon Willison's Weblog](https://simonwillison.net/2026/Nov/18/daniel-stenberg/)

### [2026-11-18] Hugging Face: 180B パラメータの MoE を 32GB の RAM で動かす「エキスパートのストリーミング」
- **何が起きたか**: Hugging Face は、Transformers で MoE モデルのエキスパートを必要なときにだけ読み込むことで、180B パラメータのモデルを 32GB の RAM で推論する手法を公開した。同じ日に、40 超の言語に対応する 0.5B の音声モデル「Rumble-2-Flash」も公開された。
- **なぜ重要か**: 大きなオープンウェイトのモデルを手元の機械で動かす敷居が下がる。社外にコードを出せない診断案件で、ローカルのモデルを使う選択肢が広がる。
- 出典: [Hugging Face Blog (MoE)](https://huggingface.co/blog/moe-expert-streaming) / [Hugging Face Blog (Rumble-2-Flash)](https://huggingface.co/blog/rumble-2-flash)

### [2026-11-18] Google 検索の AI 機能にシークレットモード。Gemini アプリはメモリの少ない Android 端末にも対応
- **何が起きたか**: TechCrunch によると、Google 検索の AI 機能に、履歴を残さない専用のモードが加わった。Google は同じ日に、Gemini アプリをメモリの少ない Android 端末でも使えるようにしたと発表した。
- **なぜ重要か**: 前号で扱った「Gemini は履歴をオフにしても約 2 か月保存」に続き、AI の会話データの扱いを利用者が選べる範囲が広がっている。企業の利用規程で「どのモードなら業務で使ってよいか」を決め直す材料になる。
- 出典: [TechCrunch](https://techcrunch.com/2026/11/18/googles-ai-feature-in-search-gets-its-own-incognito-mode/) / [Google Blog](https://blog.google/innovation-and-ai/products/gemini-app/gemini-lower-memory-devices/)

### [2026-11-17] 国内: 日立、AI エージェントの行為が「本人の承認した委任か」を証明する「PoHD」の試作を発表
- **何が起きたか**: 日立製作所は 11/17、AI エージェントが人の代わりに業務をするときに、その行為が本人の承認した委任であることを証明する技術「Proof of Human Delegation (PoHD)」の試作を開発したと発表した。生体認証で秘密鍵を守る仕組みを使う。デモでは、エージェントが勝手に金額の上限を書き換えて発注しようとするのを、システム側で止めて見せた。
- **なぜ重要か**: 電子署名では「鍵を持つエージェントが勝手に署名する」ことを防げない。委任の範囲を暗号で縛る発想は、後述の Citibank の規約変更 (エージェントの操作は利用者の責任) とは逆の方向からの答えになる。
- 出典: [MONOist](https://monoist.itmedia.co.jp/mn/articles/2611/18/news040.html)

### [2026-11-18] 国内: 孫正義氏、Anthropic への出資を見送ったことを「僕の失敗」と発言
- **何が起きたか**: ソフトバンクグループの孫正義氏は 11/18、日本経済新聞社のイベントで、Anthropic の Dario Amodei CEO と直接会いながら出資を見送ったことを「失敗例の一つ」と述べた。OpenAI にはこれまで総額 10 兆円を投じてきたという (ITmedia の報道)。
- **なぜ重要か**: 国内最大の AI 投資家が OpenAI に集中していることは、国内企業への OpenAI 製品の普及の速さにつながっている。どの基盤モデルが業務に入るかは、診断の対象 (API の使い方、データの流れ) を決める要因になる。
- 出典: [ITmedia ビジネスオンライン](https://www.itmedia.co.jp/business/articles/2611/18/news086.html)

## AI セキュリティ

### [2026-11-17〜18] Microsoft Agent Framework の PyPI パッケージに資格情報窃取のコード。Microsoft の署名・公開基盤の証明書が使われ、攻撃者は AI ペンテスト基盤「Cairn」で作業
- **何が起きたか**: 11/17 20:35 UTC に `agent-framework` 1.26.1 が、21:08 UTC に 1.26.2 が PyPI に公開された。どちらも site-packages に `.pth` ファイル (`agent_framework_meta.pth` / `af_runtime_diag.pth`) を置き、**Python が起動するたびに**資格情報の窃取を動かす。import しなくても、`pip` を動かしただけでも動く。盗む対象は Azure CLI の資格情報、Azure DevOps と GitHub Actions のトークン、環境変数などで、webhook[.]site に送る。Elastic は公開から 6 分後に検知した。両版は 21:30 UTC までに PyPI から消えた。パッケージは月に約 20 万回ダウンロードされている。
- **侵入の経路 (Wiz の分析)**: 攻撃者は、Microsoft がこのパッケージの署名と公開に使う ESRP のクライアント証明書と秘密鍵を手に入れていたとみられる。AWS からの 1 回目の公開は IP の制限で弾かれ、Microsoft の IP からの 2 回目で成功した。攻撃者の道具は、オープンソースの AI ペンテスト基盤「Cairn」と名乗っていた。攻撃者が自分のマシンで窃取のコードを試したときに、GLM 系のモデルを使うエージェントの設定が記録されていた。証明書を入手した方法はまだ分かっていない。
- **なぜ重要か**: トークンの盗難ではなく、**ベンダーの正規の公開基盤を通った**供給網の攻撃になる。PyPI の Trusted Publishing や署名の確認は、正規の経路から来たものを止められない。攻撃の作業そのものを AI エージェントで回している例としても、11/16〜17 号の Amazon MadPot や GTIG の報告と並ぶ。
- **悪用 / PoC**: 実際に配布された。11/17〜18 に 1.26.1 / 1.26.2 を入れたビルドの環境と端末では、すべての秘密情報が漏れた前提で入れ替えが必要 (Elastic の助言)。安全な最新版は 1.26.0。
- 出典: [Wiz](https://www.wiz.io/blog/malicious-version-of-microsofts-agent-framework-published-to-pypi) / [Elastic Security Labs](https://www.elastic.co/security-labs/threat-command/we-caught-the-agent-framework-pypi-compromise-six-minutes-after-it-published) / [The Hacker News](https://thehackernews.com/2026/11/attackers-compromise-microsofts-agent.html)

### [2026-11-18] ZDI: Docker Model Runner の引数インジェクションから、ホストでのコード実行まで (macOS / Windows)
- **何が起きたか**: ZDI は、Docker Desktop のローカル LLM 実行機能 Docker Model Runner (DMR) の、認証なしの引数インジェクション (ZDI-26-150 / CVE-2026-28400、2025 年 11 月に報告) の攻撃の流れを公開した。既定の権限のコンテナから Docker Desktop の VM のデータディスクを壊せる。既定でない設定では、ホストのファイルの読み書きを足がかりに、Docker Extensions を経由してホストでコードを実行できた。macOS の Seatbelt の設定が緩い点と、WSL2 の VM からホストへの境界を越える 2 つの経路も見つけた。
- **なぜ重要か**: 「ローカルで LLM を動かす」機能が、コンテナとホストの境界の新しい穴になった。開発者の端末で、信頼できないコンテナと DMR を同時に使っている場合は、Docker Desktop の版と Extensions の設定を確かめる価値がある。
- 出典: [Zero Day Initiative](https://www.thezdi.com/blog/2026/11/17/hostile-inference-exploiting-docker-model-runner-for-container-escapes)

### [2026-11-18] Rapid7: ネットに公開されたセルフホストの AI 基盤 2 万台を調べると、Ollama の半数超に「他人が使った跡」
- **何が起きたか**: Rapid7 の Christiaan Beek 氏は、ネットから届く 20,354 台を調べた。公開された Ollama の半分以上で、所有者でない誰かが触った跡が見えたという。認証なしの `/api/tags` を叩くと、コールバック先のアドレスを名前にしたモデル、サーバー自身の IP を付けたタグ、`/etc/shadow` を Base64 にした文字列などが返ってきた。一方で、同じ構成の 148 台を含む 429 台はハニーポットとみられ、それを除くと「Critical」の件数は 387 から 39 に減ったとしている。
- **なぜ重要か**: 公開された Ollama は「脆弱なおそれがある」段階ではなく、**すでに他人の計算資源として使われている**。スキャナの数字はハニーポットで大きく膨らむという指摘も、外部の攻撃面の診断の報告の書き方に役立つ。
- 出典: [Rapid7](https://www.rapid7.com/blog/post/tr-self-hosted-ai-renting-compute-exposed-servers)

### [2026-11-17] 市販のフィッシングキット「TheMailer」、攻撃者が用意した AI モデルで文面を個別化
- **何が起きたか**: Dark Reading によると、TheMailer は攻撃者が持ち込んだ AI モデルを使って、標的ごとに文面を変え、スパムフィルタをすり抜け、数万件規模の配信まで自動で行う (記事本文は 403 で取得できず、RSS の要約による)。
- **なぜ重要か**: 「文面の不自然さ」で見抜く訓練は効かなくなる。メールの訓練や診断では、送信元の認証 (DMARC) と、リンク先の振る舞いでの検知に重点を移す必要がある。
- 出典: [Dark Reading](https://www.darkreading.com/perimeter/themailer-phishing-kit-ai-drivers-seat)

### [2026-11-18] 米上院議員 2 人、AI を使ったサイバー攻撃に対する防御の仕組みを国として作るよう要請
- **何が起きたか**: Maria Cantwell 議員と Mike Rounds 議員は、国家情報長官に宛てた書簡で、AI が「ソフトウェアの弱点を見つけて悪用する速さ」に対し、修正の適用が数週間から数か月かかる現状では防御が追いつかないと訴え、AI を使った防御の国家的な取り組みを求めた。
- **なぜ重要か**: 同じ日に Java4Shell (AI で 3 時間で攻撃を実証) と、AI のペンテスト基盤を使った PyPI の侵害が出た。「パッチを当てるまでの時間」を前提にした脆弱性管理の見直しが、政策でも議題になっている。
- 出典: [The Record](https://therecord.media/ai-cyber-white-house)

### [2026-11-18] 米 Citibank が規約を変更。第三者の AI エージェントで口座を操作した場合の損害は、乗っ取られた場合も利用者の責任
- **何が起きたか**: TechCrunch によると、Citibank は今週、家計管理などで第三者の AI ツールに口座を使わせる利用者について、何か起きたら利用者の問題とする規約に改めた。エージェントの意図した、または意図しない取引を元に戻す責任を銀行は負わないとしている。同様の銀行が増えているという。
- **なぜ重要か**: エージェントに資格情報を渡すこと自体が「本人の過失」と扱われ始めた。金融機関の診断では、エージェント用の権限を絞った API (読み取り専用、上限付き) を用意しているかが、規約と並ぶ論点になる。
- 出典: [TechCrunch](https://techcrunch.com/2026/11/18/more-banks-says-customers-using-ai-agents-are-on-their-own-even-if-they-get-hacked/)

### [2026-11-17] arXiv (cs.CR) の実務寄り 4 本: 画面をまたぐ害、エクスプロイトの「早すぎる諦め」、システムプロンプトの漏えい、Actions の修正漏れ
- **何が起きたか**:
  - **SEAM** ([2611.22971](https://arxiv.org/abs/2611.22971)): 指示も各画面も無害で、組み合わせたときだけ有害になる 600 件の OSWorld タスクを作り、コンピュータを操作するエージェントが「画面をまたいだ害」に気づいても実行してしまうことを示した。
  - **Stopping Is Not the Limit** ([2611.22888](https://arxiv.org/abs/2611.22888)): ExploitBench で、エージェントは予算を残したまま「無理だ」と止まることが多く、止まった後も続けさせると、確認できるエクスプロイトがさらに増えた (増え方は次第に鈍る)。
  - **Eight in Ten LLMs Leak System-Prompt Secrets** ([2611.21956](https://arxiv.org/abs/2611.21956)): OpenRouter の 363 モデルのうち 296 モデルから、システムプロンプトに置いた 16 文字のフラグを抜き出せた。成功 300 件のうち 170 件は、途中で英語以外 (多くはフランス語) に切り替えていた。
  - **Missing Security-Fix Backporting for GitHub Actions** ([2611.22519](https://arxiv.org/abs/2611.22519)): 190 万のコミットから見つけた Actions のワークフローのセキュリティ修正 69,865 件の多くが、リリース用のブランチに持ち込まれていなかった。
- **なぜ重要か**: 2 本目は、AI でエクスプロイトを作るときの「打ち切りの判断」の改善余地を示し、Java4Shell の Calif の進め方とも重なる。3 本目は、システムプロンプトに秘密を置く設計がほぼ守れないことを数で示した。4 本目は、OSS の診断で「main だけを見て終わらない」根拠になる。
- 出典: 各 arXiv ページ (上記リンク)

## セキュリティニュース

### [2026-11-18] NGINX の HTTP/2 に未認証 RCE「nginx2root」(CVE-2026-123007)。2015 年の 1.9.5 から続き、同時に HTTP/2 の UAF (CVE-2026-123633) など計 5 件
- **何が起きたか**: F5 は 11/18、NGINX Open Source 1.31.9 / 1.30.7 と NGINX Plus の修正版を出した。CVE-2026-123007 (CWE-191) は、HTTP/2 のフロー制御で、送ってよいデータの量の計算を誤る整数のアンダーフローで、Rapid7 によると、待ち行列のデータを取り消させたあと、次の応答のコピーで不正な長さを使わせられる。CVE-2026-123633 は、バックエンドへ転送する構成で worker_connections が足りなくなったときの use-after-free。いずれも CVSS 4.0 で 9.2。F5 は「ASLR が無効か、回避できる場合に RCE」としているが、Wiz、Rapid7、Xint は ASLR を回避して RCE を実証した。ほかに HTTP/3 (CVE-2026-121810)、mail proxy (CVE-2026-113425)、変数で組んだ proxy の名前と SSI の組み合わせ (CVE-2026-123634) も修正された。
- **なぜ重要か**: 影響範囲は 1.9.5 から 1.31.8 まで (10/14 のセキュリティリリースを含む) とほぼすべての版に及ぶ。コードは worker の権限で動くが、Xint は Linux カーネルの SCTP の別のバグと組み合わせ、Docker の中からホストの root まで届かせた。CDN の裏にあっても、オリジンが HTTP/2 を受けるなら直接攻撃されうる。
- **悪用 / PoC**: 悪用は未確認で、KEV にも入っていない。GitHub に PoC が公開されている (同じマシン上の、起動したばかりの Docker コンテナ向けの実証用と注記)。HTTP/2 を受けるかは `openssl s_client -alpn h2` で `ALPN protocol: h2` が出るかで分かる。
- 出典: [Rapid7](https://www.rapid7.com/blog/post/ve-cve-2026-123007-critical-nginx-http-2-integer-underflow-leads-to-rce-fixed) / [Wiz](https://www.wiz.io/blog/nginx-http2-rce-vulnerabilities) / [The Hacker News](https://thehackernews.com/2026/11/10-year-old-nginx-http2-flaw-lets.html) / [SANS ISC](https://isc.sans.edu/diary/rss/33532)

### [2026-11-18] CISA KEV に 4 件追加: Apache Axis、LiteLLM、REDCap、Synology DSM。うち 3 件は対応期限が 3 日後の 11/21
- **何が起きたか**: CISA は 11/18 付で 4 件を KEV に入れた。
  - **CVE-2026-90436** (Apache Axis の unsafe reflection): 11/17 号の [続報] で、Rapid7 が Confluence Data Center での悪用を報告していた件。期限は 11/21。
  - **CVE-2026-40217** (LiteLLM、CVSS 8.8): `/guardrails/test_custom_code` で、バイトコードの書き換えによってサンドボックスを抜け、任意のコードを実行できる。11/6 号の Mandiant の LLMJacking の事例で悪用が挙がっていた。期限は 12/2。EPSS は 0.170 (上位 3%)。
  - **CVE-2026-90817** (Vanderbilt REDCap、9.8): 公開アンケートの文脈から想定外のコントローラに届き、インポートの処理でファイルパスを差し込んで、未認証で RCE。期限は 11/21。
  - **CVE-2024-10441** (Synology DSM / BeeStation、9.8): 2025 年 3 月に NVD に載った system plugin daemon の出力エスケープの不備による RCE。期限は 11/21。
- **なぜ重要か**: 期限が 3 日という短さは、CISA が「すでに広く悪用されている」と判断したことを示す。REDCap は研究機関や病院でよく使われ、国内の大学・医療機関にも導入例がある。LiteLLM は AI のゲートウェイとして、組織の LLM の鍵が集まる場所になっている。
- 出典: [CISA KEV (JSON)](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json) / [NVD CVE-2026-40217](https://nvd.nist.gov/vuln/detail/CVE-2026-40217) / [NVD CVE-2026-90817](https://nvd.nist.gov/vuln/detail/CVE-2026-90817)

### [2026-11-18] [続報] Apache Roller の XML-RPC デシリアライズ (CVE-2026-129448): ASF が「悪用中」と明記。9 月の CVE-2026-82384 は修正が不完全だった
- **前回からの差分**: 前号の CVE 表では「悪用あり」の記載を紹介した。11/18、ASF は「This issue is being actively exploited」と明記し、この問題は 9 月に 6.1.5 だけを対象として公表した CVE-2026-82384 と同じものだと説明した。対象は実際には 4.0.0〜6.1.4 で、修正は 6.1.6。すぐに更新できない場合は、`WEB-INF/web.xml` で `enabledForExtensions` を `false` にするか、`/roller-services/xmlrpc` を外す。攻撃の主体や標的は明らかにされていない。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/critical-apache-roller-rce-flaw-under.html) / [BleepingComputer](https://www.bleepingcomputer.com/news/security/apache-warns-of-roller-rce-vulnerability-exploited-in-attacks/)

### [2026-11-18] F5 BIG-IP のデータプレーンにスタックオーバーフロー 6 件 (CVSS 3.1 で 9.8)。特定の iRule や APM の設定で、未認証で TMM を落とし、RCE のおそれ
- **何が起きたか**: F5 は 11/18、BIG-IP の Traffic Management Microkernel (TMM) に関わる 6 件を公開した。5 件は iRules (特定のコマンドを使う iRule を付けた仮想サーバー)、1 件は APM (Client Information と Endpoint Security の両方のエージェントを含む per-request policy、CVE-2026-123637)。BIG-IP Next for Kubernetes と BIG-IP CNF も一部が対象。エンジニアリング用の hotfix が出ており、回避策はない。4 件は watchTowr の Sina Kheirkhah 氏の報告。
- **なぜ重要か**: 管理画面ではなく、**トラフィックを処理する部分**の欠陥で、条件に合う構成なら外からの通信だけで届く。悪用は未確認。iRule の中で使っているコマンドの棚卸しが、影響の判断の前提になる。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/f5-warns-6-critical-big-ip-flaws-can.html)

### [2026-11-18] Mandiant / GTIG: ロシア系の Cold Relic (旧 COLDRIVER) が、別の組織から盗んだ Google Workspace のデータで、次の米国組織に侵入
- **何が起きたか**: Mandiant と GTIG は、2026 年に米国の組織で起きた侵害を調べた。攻撃者は、2025 年末に別の米国組織から奪ったデータ、社員名簿、ID を使って、取引のある次の組織を狙っていた。侵入後は、不正な MFA デバイス、パスキー、MFA のバックアップコードを登録して長く居座り、メール、チャット、クラウドストレージを大量に持ち出した。
- **なぜ重要か**: 1 つのクラウドの侵害が、取引先への「なりすましの材料」として使い回される。ID 基盤の診断では、パスキーやバックアップコードの登録を監視し、警告しているかを確かめる必要がある。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/russian-cold-relic-hackers-use-stolen.html) / [The Record](https://therecord.media/russia-cyber-espionage-google)

### [2026-11-18] TU Berlin: ケースを開ければ fTPM のロックアウトを巻き戻せる。Windows Hello の 4 桁の PIN は最悪 40 時間、BitLocker の 6 桁は 20 日
- **何が起きたか**: 研究者は、AMD 機と一部の Intel 機で、プロセッサ内蔵の firmware TPM が試行回数をマザーボードのフラッシュに暗号化して保存している点を突いた。古い状態を書き戻すと回数が戻る。対策の RPMC (増えるだけのカウンタ) について、AMD のファームウェアは値が実際に増えたかを確かめていなかった。Winbond の RPMC チップは、電圧のグリッチで署名鍵を約 1 秒で漏らした。実験では Hello の 4 桁と BitLocker の 6 桁の PIN を、いずれも 236 回以内の試行で当てた。AMD は欠陥を認め、2026 年 11 月から 2027 年 2 月にかけて修正を出す予定。
- **なぜ重要か**: 「TPM のロックアウトがあるので短い PIN でよい」という前提が崩れる。端末の紛失・盗難を想定した評価では、PIN を 2 桁以上延ばす (研究者の助言)、起動前の認証に別の要素を足す、などを提言に入れる材料になる。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/flash-chip-attack-bypasses-tpm-lockout.html)

### [2026-11-17] [続報] Telegram の widgets: 前週の修正 (QuickJS の別プロセス化と seccomp) を回避する RCE を NebuSec が 2 通り実演
- **前回からの差分**: 11/17 号では V12 の RCE の実演と Kaspersky の WebRAT の報告を扱った。その後、Telegram は Android 版 13.2.2 (7303) で、widgets の JavaScript を動かす QuickJS を別のプロセスに分け、seccomp のフィルタを足した。NebuSec は、フィルタが対象にしない widget のバグを使う方法と、対象のバグをカーネルのバグと組み合わせる方法の 2 つで、フィルタの外でコードを動かした (テストサーバーで、電卓の起動まで)。詳細と CVE は公開されておらず、利用者の操作が必要かも不明。
- **評価**: seccomp は数十のシステムコールだけを止める方式で、許可しない呼び出しを列挙する方式ではない。業務で Telegram を使う組織は、引き続き widgets を使えないようにするのが無難とみる。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/researchers-claim-two-rce-exploits-that.html)

### [2026-11-18] Bitdefender: 中国系とみられる EggStreme の運用者が、露見後に通信方式を変え、外へ通信しない受け身の版も投入 (フィリピン政府を標的)
- **何が起きたか**: 2025 年 9 月に公表された EggStreme (DLL サイドローディングで動く多段のフレームワーク) の新しい版は、通信の方式を変え、命令を増やし、自分からは C2 に接続しない受け身の版を持つ。インフラも、旧サーバー群をつないでいた 1 つの認証局から離れつつある。Palo Alto の CL-STA-1048 も一部の部品を使っていた。
- **なぜ重要か**: ハッシュやドメインの入れ替えではなく、検知の前提 (外への通信) そのものを変えた。受け身の版は、内部の通信や待ち受けのポートの監視でしか見つけにくい。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/eggstreme-hackers-rebuild-malware-with.html)

### [2026-11-18] Talos: 北朝鮮系の疑いがある UAT-12643、Solana の取引のメモに暗号化した C2 の URL を隠す
- **何が起きたか**: Talos は、Go で書かれた RAT「Overlord」、Python の窃取ツール「Good Game」、複数の暗号資産に対応するクリップボードの書き換えツールを使う金銭目的の集団を報告した。Overlord は、Solana の取引のメモ欄から暗号化された C2 の URL を読み出す。おとりは偽の Viber のインストーラ、microsip という名前のファイル、財務諸表の PDF で、欧州の財務・経理の担当者、VoIP の利用者、暗号資産やゲームの利用者を狙う。北朝鮮との関係は「確度は低い」としている。
- **なぜ重要か**: ブロックチェーンに置いた C2 の情報は消せず、テイクダウンが効かない (Talos は同じ日に、この「消せない dead drop」への対策の難しさを別の記事で論じた)。
- 出典: [Cisco Talos](https://blog.talosintelligence.com/uat-12643-suspected-north-korea-aligned-actor-blends-blockchain-resilience-with-targeted-infostealing/) / [Cisco Talos (dead drop)](https://blog.talosintelligence.com/the-challenge-of-defending-against-bulletproof-dead-drops-on-public-blockchains/)

### [2026-11-17] Docker Hub などの公開イメージに置いたクラウドの鍵は、最短 8 秒で抜き取られる (ACM CCS の発表)
- **何が起きたか**: Stony Brook 大学の研究者は、8 つの公開コンテナレジストリに 300 個のおとりのイメージを置き、AWS、OpenAI、Anthropic の API キーや、SSH・DB の資格情報を 4 か月間さらした。鍵は最短 8 秒で抜き取られ、使われた。
- **なぜ重要か**: 「公開してすぐ消した」は言い訳にならない。イメージのレイヤーに秘密情報が残っていないかの確認は、コンテナの診断の定番の項目だが、その緊急度を数字で示した。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/cloud-keys-leaked-in-docker-hub-images-are-stolen-within-seconds/)

### [2026-11-18] アイルランドの信用組合約 40 組合で会員情報が流出。委託先の Wellington IT が侵害されたと閣外相が認める
- **何が起きたか**: ベルファストの Wellington IT は約 50 の信用組合 (うちアイルランドの 43) にサービスを提供している。同社は公表していないが、Robert Troy 閣外相は RTÉ に、同社が今回の件の委託先だと認めた。金融詐欺、なりすまし、標的型フィッシングのおそれがあると各組合に通知されたという。
- **なぜ重要か**: 小さな金融機関がまとめて委託する IT ベンダーが、一度に数十の組織の入口になる。国内の KARTE の件と同じ構造で、委託先の診断の重要性を示す。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/data-breach-impacts-40-irish-credit-unions-in-reported-it-provider-hack/)

### [2026-11-18] Scattered Spider の Tyler Buchanan 被告に禁錮 6 年。米国の事件の被告 5 人全員に量刑
- **何が起きたか**: 主犯とされた英国人の Buchanan 被告 (24) は、米国の個人から 1,160 万ドル超の暗号資産を盗んだフィッシング事件で禁錮 6 年を言い渡された。2024 年 11 月に起訴された 5 人のうち最後の量刑となる。一味は Coinbase、Twilio、Mailchimp、LastPass を狙い、MGM Resorts へのランサムウェア攻撃にも関わったとされる。
- **なぜ重要か**: ヘルプデスクへのなりすましと SIM スワップを使った手口は、今も国内外で模倣されている。量刑の確定で、この手口に対する抑止の一区切りになる。
- 出典: [The Record](https://therecord.media/british-hacker-gets-six-year-sentence-scattered-spider) / [SecurityWeek](https://www.securityweek.com/last-of-five-defendants-sentenced-in-us-scattered-spider-hacking-case/)

### [2026-11-18] 短信
- **Chrome 158** (11/17 公開): 脆弱性 204 件を修正し、うち Critical は 6 件 (WebView・GC・WebAudio の UAF、GPU と ANGLE の範囲外書き込み、Media のバッファオーバーフロー)。163 件は報奨金なしで、145 件は Google が見つけた。[SecurityWeek](https://www.securityweek.com/chrome-158-patches-204-vulnerabilities/)
- **Windows Server 2028**: Microsoft は Ignite で発表した。既定で強化した Server Core の構成と、個別に緩められる新しいセキュリティベースラインを持つ。[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-announces-windows-server-2028-with-hardened-security/)
- **BubbleLoader** (ReversingLabs): WinRAR、x64dbg、Windows Media Player などの入口の数命令を書き換え、PNG の画像 2 枚に次の段を隠すローダー。実行のたびに自分のハッシュを変える。[Help Net Security](https://www.helpnetsecurity.com/2026/11/18/winrar-bubbleloader-malware/)
- **NSA の内部ネットワーク「NSA Net」**: 11/17 から断続的に止まり、2 日目も復旧作業が続いた。原因は明らかにされていない。[The Record](https://therecord.media/nsa-continues-response-to-nsa-net-problems)
- **[続報] Optimizely (OPTIMJACK)**: Unit 42 は 11/17、攻撃者が Web Experimentation の脆弱性を突き、ベンダーの正規の CDN と証明書の下で 178 組織以上に悪性 JS を配ったと整理した。[Unit 42](https://unit42.paloaltonetworks.com/optimjack-supply-chain-attack/)
- **Broadcom AutoSys Workload Automation**: 11/17 に 11 件を公表した。WCC のハードコードされた暗号鍵 (CVE-2026-126551) など。修正は 10 月の更新に含まれていた。[Security NEXT](https://www.security-next.com/193007)

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-11-17 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-114938 [続報] | OpenJDK 17.0.6 以降 / 21 / 25 / 27 (x86-64、AVX-512 VBMI) | CWE-787 / 8.1 (CVSS 4.0 で 9.2) | 余分な `=` で終わる Base64 → AVX-512 のイントリンシックが出力長を負に計算 → 配列の後ろ 62〜63 バイトに書き込み → JavaBleed (ヒープの読み出し) を経て RCE | [advisory](https://openjdk.org/groups/vulnerability/advisories/2026-11-17) (commit 不明) | PoC (破損の再現) 公開 / CISA 注意喚起 / EPSS 0.007 |
| CVE-2026-123007 | NGINX OSS 1.9.5〜1.31.8、NGINX Plus R34〜37.x | CWE-191 / 9.2 (v4) | HTTP/2 で待ち行列のデータを取り消させる → フロー制御の窓の計算がアンダーフロー → 次の応答のコピーで不正な長さ → ヒープ破損、worker 権限で RCE | [advisory (Rapid7)](https://www.rapid7.com/blog/post/ve-cve-2026-123007-critical-nginx-http-2-integer-underflow-leads-to-rce-fixed) (commit 不明) | PoC 公開 (GitHub) / ASLR 回避の RCE を複数社が実証 |
| CVE-2026-123633 | NGINX OSS / Plus (HTTP/2 + proxy) | CWE-416 / 9.2 (v4) | HTTP/2 で受けてバックエンドへ転送する構成 + worker_connections が逼迫 → 細工したリクエストで use-after-free → RCE | [advisory (Wiz)](https://www.wiz.io/blog/nginx-http2-rce-vulnerabilities) (commit 不明) | 複数チームが独立に発見 |
| CVE-2026-126752 / GHSA-6qr9-g2xw-cw92 | Dagu 1.23.0〜2.0.0 未満 | CWE-306 / 9.8 | 既定で `auth.mode=none` → `POST /api/v2/dag-runs` にシェルコマンドを含むインラインの spec → 未認証で OS コマンド実行 | [diff](https://github.com/dagucloud/dagu/commit/c0e7cf7e1cfc3a52af8a9fb2da1ca911a9958649) | **悪用観測あり** (Shadowserver、2026-03-11 から) |
| CVE-2026-75521 / GHSA-8fh7-7q4q-cq52 | Miren Runtime 0.11.1 未満 | CWE-295 / 10.0 | Go の QUIC/HTTP3 の RPC が `tls.RequestClientCert` で証明書の連鎖を検証せず → `PeerCertificates[0].Subject.CommonName` を身元として信用 → 自己署名の証明書で RBAC を全部迂回 | [diff](https://github.com/mirendev/runtime/commit/e2159c8c8559da3f1c1485b463c794d656cd2fe4) | 水平伝播候補 (Go の mTLS 実装) |
| CVE-2026-63189 / GHSA-2448-c4f7-4crm | Dialoqbase 1.11.5 未満 | CWE-22 / 9.8 | 未認証の `GET /api/v1/view/*` がワイルドカードのパスを正規化せずに解決 → 任意ファイルの読み出し → `.env` の JWT 署名鍵で管理者のトークンを偽造 | [diff](https://github.com/n4ze3m/dialoqbase/commit/c9d128c58997d91d9786b54a0fd626206ce0f4f9) | AI チャットボット基盤 / 鍵の奪取まで一直線 |
| CVE-2026-130840 | BISHENG 3.0.0 未満 (LLM アプリ基盤) | CWE-321 / 9.8 | 既定のハードコードされた `jwt_secret` → `user_id=1`・admin の HS256 トークンをオフラインで偽造し `access_token_cookie` に → 管理者を完全に乗っ取り | [diff](https://github.com/dataelement/bisheng/commit/b98e2bc5c819a6a8d35538d91eab85833bd77703) | EPSS 0.010 / 既定の秘密鍵 |
| CVE-2026-131852 | OwnTracks Recorder 1.0.5 未満 | CWE-134 / 9.8 | `POST /pub` や MQTT で `tid` に printf の書式指定子を保存 → `GET /api/0/last` の `json_response()` が書式文字列として出力 → アドレスの漏えいとメモリ書き込みで RCE | [diff](https://github.com/owntracks/recorder/commit/64a86050a1ac6cb5f704e296ec9182f750d143c8) | 保存型の format string |
| CVE-2026-129892 | Perl IO::Socket::SSL 2.099 以前 (PublicSuffix) | CWE-94 / 9.8 | `update_self_from_url` が取得した一覧を自分のソースのヒアドキュメントの下に追記 → `END_BUILTIN_DATA` の行でヒアドキュメントが閉じる → 続く行が Perl コードとして実行 | [diff](https://github.com/noxxi/p5-io-socket-ssl/commit/6e756466cd7005bcdb2e0e18eb140f33a2355c78) | 「自己書き換え」のバグクラス |
| CVE-2026-119293 / GHSA-cw2f-3w8g-4x9q | FreeSWITCH 1.11.2 以前 | CWE-346 / 9.3 | `rtp_common_read()` の RTP 送信元の学習がセッション全体で 1 つのカウンタ → 通話の確立中に偽の送信元からの RTP が先にしきい値に達する → 音声の注入と盗聴 (RTP Bleed 系) | [diff](https://github.com/signalwire/freeswitch/commit/a38cd8073314f7da29b16743b8dbe52fd8505ba7) | 水平伝播候補 (RTP の自動調整を持つ他の SBC) |
| CVE-2026-129511 | Apache log4net (FileAppender ほか) | CWE-117 / – | XmlLayout がエスケープしたあとに、エンコーディングの best-fit 変換が全角の `＜＞＂` を `<>"` に戻す → XML のログに偽のイベントを丸ごと挿入 | [diff](https://github.com/apache/logging-log4net/commit/735db80ab163ef08c54d2cc4d3d576b22b77f4bc) | 水平伝播候補 (「エスケープ → 文字コード変換」の順序の誤り) |
| CVE-2026-131857 | Supergateway 4.2.0〜4.2.2 (MCP の stdio→SSE) | CWE-754 / 8.7 | `sessionId` に `toString` / `constructor` → プロトタイプから継承した値をセッションとして参照 → 未処理の TypeError でプロセスが落ち、接続中の MCP セッションがすべて切れる | [diff](https://github.com/supercorp-ai/supergateway/commit/e2254169a0780ec7c299fff7d51e128b013a65d3) | MCP ゲートウェイ / 未認証 |
| CVE-2026-130843 | HyperFrames 0.9.30 未満 | CWE-346 / 8.8 | 認証なしの Studio API が Origin と Host を確認しない → 悪意あるページからの CORS-simple な POST や DNS rebinding で `package.json` の scripts やエージェントの設定を書き込む → コマンド実行 | [diff](https://github.com/heygen-com/hyperframes/commit/f318d3d08a7dff5fb48d12e7604c73bf004af204) | localhost の開発用サーバーのバグクラス |
| CVE-2026-130681 / GHSA-7gj8-xf7w-hfjf | SiYuan 3.8.10 未満 | CWE-79 / 9.4 | CVE-2026-44670 の修正漏れ: `renderAVAttribute()` が Attribute View の名前をエスケープせずに挿入 → デスクトップ版で `onerror` から Node.js の OS コマンドを実行 | [diff](https://github.com/siyuan-note/siyuan/commit/d3af9d5782082b379d45a69eedf4ebcfe8ba6889) | 不完全な修正 (同日に同種 2 件: CVE-2026-130678 / 130679) |

**今日の CVE 所感**:
- **「最適化のコード」と「長さの計算」が同じ日に 2 つ**出た。Java4Shell (SIMD のイントリンシックで出力長が負になる) と nginx2root (HTTP/2 のフロー制御の窓がアンダーフローする) は、どちらも「境界の値の計算を誤り、それをそのままコピーの長さに使う」型になる。HTTP/2 のフロー制御を自前で実装したサーバー (Envoy、h2o、HAProxy、各言語の HTTP/2 ライブラリ) で、取り消し (RST_STREAM) と WINDOW_UPDATE の組み合わせを試す価値がある。
- **認証・身元の既定値**の問題が続いた。Dagu (`auth.mode=none`、3 月から悪用されている)、BISHENG (固定の JWT の秘密鍵)、Dialoqbase (ファイルの読み出しから署名鍵へ)、Miren (mTLS の連鎖を検証しない)。AI・エージェント系の新しい OSS は、この 4 つを最初に確かめるだけで当たりが出やすい。Go で `tls.RequestClientCert` / `RequireAnyClientCert` を使い、`VerifiedChains` を見ていないコードは grep で探せる。
- **文字コードの変換の順序** (log4net の best-fit) は、.NET の `Encoding.GetEncoding(..., EncoderFallback)` を使う他のロガーやシリアライザにも同じ形で残っている可能性がある。WAF の回避で知られた「best-fit」が、ログの偽装にも使えることを示した。
- 診断で優先して見る製品: Java (版 × CPU)、HTTP/2 を受ける NGINX、iRule / APM を使う BIG-IP、REDCap、LiteLLM の `/guardrails/test_custom_code`、Dagu。

## 日本国内のセキュリティ動向

### 国内インシデント・事故

#### [2026-11-18] [続報] プレイド「KARTE」: 三菱 UFJ 銀行が約 650 万件、三菱 UFJ 信託銀行が約 23 万件、ウェルスナビが約 91 万人の漏えいを公表
- **何が起きたか**:
  - **三菱 UFJ 銀行** (11/18): 顧客関連の情報約 650 万件が漏えいした。項目は性別、年齢、居住地域 (都道府県または政令指定都市)。氏名、住所、電話番号、メールアドレス、口座番号、暗証番号は含まない。11/13 に KARTE への不正アクセスとサービス停止の報告を受け、11/17 に自行分の範囲の説明を受けたという。
  - **三菱 UFJ 信託銀行** (11/18): 約 23 万件。性別、インターネットバンキングの会員番号から作った識別子、LINE 公式アカウントの利用者を識別する番号など。
  - **三菱 UFJ eスマート証券** (11/18): 証券口座番号約 6 万件と年齢約 10.5 万件 (二次情報による)。
  - **ウェルスナビ** (11/18): 顧客約 91 万人。項目は同社が作った約 40 桁の顧客識別コード、生年月、居住都道府県。11/14 に外部との連携を止め、連携用の認証情報を無効にした。
  - いずれも各社のシステムへの不正アクセスではないとしている。
- **なぜ重要か**: 前号の 34 組織から、メガバンクとその系列にまで広がった。氏名を含まなくても、「LINE の利用者 ID」や「会員番号から作った識別子」は、他の漏えいデータと突き合わせて個人を特定する材料になりうる。金融機関の名前をかたるフィッシング (前号のフィッシング対策協議会の注意喚起) の口実にも使われやすい。
- 出典: [ニッキン (2026-11-18)](https://www.nikkinonline.com/article/440954) / [セキュリティ対策Lab (三菱 UFJ 銀行)](https://rocket-boys.co.jp/security-measures-lab/mufg-bank-karte-6_5million-official-20261118/) / [セキュリティ対策Lab (ウェルスナビ)](https://rocket-boys.co.jp/security-measures-lab/wealthnavi_karte_910000_customers_data_breach/)

#### [2026-11-18] NewsPicks (ユーザベース) が調査報告: 原因は BI ツール Metabase の SQL インジェクション。修正の 6 日前に脆弱性が公表され、修正の前に侵入されていた。JPCERT/CC の不審 IP の一覧で発覚
- **何が起きたか**: ユーザベースは 11/18、NewsPicks の利用者の氏名、住所、クレジットカード情報の一部が流出した件の調査報告を公表した。原因は Metabase の SQL インジェクションの脆弱性。同社は Metabase の公表から 6 日後 (3 営業日後) の 8/12 に修正版に更新したが、攻撃者はその前に侵入して情報を盗んでいた。JPCERT/CC が 10/8 に公表した不審な IP アドレスの一覧を基に調べて、不正アクセスに気づいたという (ITmedia の報道)。
- **なぜ重要か**: 「3 営業日でパッチを当てた」組織でも、公表から悪用までの時間はそれより短かった。社内の BI ツールが顧客 DB に直接つながっている構成は多く、外から届く BI ツール (Metabase、Redash、Superset) は診断で必ず見るべき対象になる。JPCERT/CC の IoC の公開が実際の検知につながった例でもある。
- 出典: [ITmedia NEWS (2026-11-18)](https://www.itmedia.co.jp/news/article/2611/18/2000003300/)

#### [2026-11-18] [続報] 楽天証券: テスト環境に本番の顧客データを置いていた理由を「アップグレードに伴う検証に必要だった」と説明。対象は合計で最大約 1,572 万口座分
- **前回からの差分**: 前号では最大約 447 万口座 (年収・金融資産・出金先の口座を含む) を扱った。ITmedia の取材に対し、同社は「社内システムのアップグレードに伴い、一部の機能の検証に本番データを使う必要があった」と説明した。対象は合計で最大約 1,572 万口座分で、うち最大約 1,125 万口座分は部店・顧客コードとログイン ID。11/18 の午前には、出金やパスワードの変更に必要な「ワンタイムキー」の発行が遅れる表示が出た。
- **評価**: 「テスト環境だから守りが緩い」という構造は、診断の範囲から外されやすい場所でもある。本番データの複製先 (検証環境、分析基盤、バックアップ) を範囲に含めるよう提案する根拠になる。
- 出典: [ITmedia NEWS (理由)](https://www.itmedia.co.jp/news/article/2611/18/2000003302/) / [ITmedia NEWS (ワンタイムキー)](https://www.itmedia.co.jp/news/article/2611/18/2000003284/) / [piyolog](https://piyolog.hatenadiary.jp/entry/2026/11/18/100525)

#### [2026-11-17] インフキュリオン: Notion AI の委託先 Fireworks AI への不正アクセスで、取引先担当者・採用応募者・従業員の個人情報 232 件
- **何が起きたか**: インフキュリオンは 11/17 (自社サイト) と 11/18 (適時開示) に、2026 年 10/5〜24 に Notion AI に入力した文章と回答の一部が外に持ち出されたと公表した。11/13 に Notion から連絡を受けた。決済のサービスやシステムへの不正アクセスではないとしている。個人情報保護委員会に報告済み。
- **なぜ重要か**: Notion AI の件で国内の被害組織の公表がまた増えた。11/18 には Notion の CISO が ITmedia の取材に日本の顧客へのおわびを述べている。AI 機能の再委託先にまで入力データが渡る点は、SaaS の評価のチェックリストに入れておくべき項目になる。
- 出典: [セキュリティ対策Lab](https://rocket-boys.co.jp/security-measures-lab/infcurion-notion-ai-fireworks-232-data-leak-20261118/) / [ITmedia AI+ (Notion の CISO)](https://www.itmedia.co.jp/aiplus/article/2611/18/2000003299/)

#### 短信
- 直近 2 日に新たに公表された、上記以外の国内の侵害は確認できなかった。ScanNetSecurity の 11/17〜18 掲載分 (ビューティガレージ、セブン銀行、オープンロジ、Yeny、マクロミル、銀のさら など) は、組織の公表がいずれも 11/12 以前だったため除外した。

### 国内の注意喚起・ガイドライン・政策

#### [2026-11-18] JPCERT/CC CyberNewsFlash と IPA: Java4Shell (CVE-2026-114938) の注意喚起
- **何が起きたか**: JPCERT/CC は、OpenJDK を基にした Oracle Java SE、Corretto、Temurin、Microsoft Build of OpenJDK、Azul Zulu、Red Hat OpenJDK などが影響を受けるおそれがあるとし、「11/18 時点で悪用は確認していないが、速やかに対策を」と呼びかけた。製品に同梱された Java 実行環境にも注意するよう書いている。IPA も同日、Oracle Java の 11 月の更新について、CVE-2026-114938 を名指しして早めの適用を勧めた。
- **なぜ重要か**: 「製品に同梱された JRE」は利用者が気づきにくい。国内の業務パッケージ (帳票、ジョブ管理、Web の業務システム) には JRE を同梱するものが多く、ベンダーの対応表を待つ必要がある。
- 出典: [JPCERT/CC](https://www.jpcert.or.jp/newsflash/2026111801.html) / [IPA](https://www.ipa.go.jp/security/security-alert/2026/1118-jre.html)

#### [2026-11-17] 日 ASEAN 首脳会議: 高性能 AI の脅威に対処する新しい連携の枠組みの創設を確認
- **何が起きたか**: 高市首相は 11/17、フィリピンでの日 ASEAN 首脳会議に出席し、高性能な AI をめぐる脅威に対処するため、各国と連携する新しい枠組みを作ることを確認した。首相は「AI の急速な進展に伴う新たな脆弱性に対応する」と述べた。重要鉱物の供給網やエネルギー安全保障での連携でも一致した (産経新聞の報道)。
- **なぜ重要か**: AI の悪用 (脆弱性の自動発見など) への対処が、二国間ではなく地域の枠組みで扱われ始めた。具体的な中身はまだ出ておらず、今後の情報共有の仕組みが注目点になる。
- 出典: [ITmedia NEWS (産経新聞)](https://www.itmedia.co.jp/news/article/2611/18/2000003294/)

#### [2026-11-17] 総務相、NTT ドコモの 3 度の全国的な通信障害に「大変遺憾」。構造的な課題の洗い出しを求める
- **何が起きたか**: 藤井総務相は 11/17 の閣議後の会見で、ドコモの 11/5・11・16 の全国規模の障害について、根本原因の究明と、組織としてのリスク管理体制を含む構造的な課題の洗い出しを求める考えを示した。
- **なぜ重要か**: 短い期間に同じ事業者で障害が繰り返したことで、行政指導に進む可能性がある。通信を前提にした二要素認証 (SMS) や業務の継続計画の見直しの材料にもなる。
- 出典: [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2611/17/2000003261/)

#### [2026-11-18] IPA「情報セキュリティ安心相談窓口」2026 年第 3 四半期: 個人からの相談は 3,369 件で 12.1% 減。偽警告は 1,160 件
- **何が起きたか**: Security NEXT によると、IPA の窓口に個人から寄せられた相談は前の四半期の 3,832 件から 3,369 件に減り、2025 年第 3 四半期から続いた増加が止まった。偽の警告画面で不安をあおる「偽警告」の相談は 1,428 件から 1,160 件に減った。不正ログインの相談は高い水準が続いている。
- **なぜ重要か**: サポート詐欺は減っても、不正ログイン (今回の楽天証券や証券会社をかたるフィッシングと同じ流れ) は減っていない。
- 出典: [Security NEXT](https://www.security-next.com/192083)

### 国内製品の脆弱性 (JVN)

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| 2026-11-18 | JVN#19906678 / CVE-2026-117657, CVE-2026-118900 | 宮内庁「宮内庁参観音声ガイド」Android アプリ 2.7 未満 | 重要な情報を平文で送る (表示内容の改ざん) / OS コマンドインジェクション (アプリの権限で任意のコマンド)。報告者は GMO Flatt Security の RyotaK 氏 | v4 で 8.4 (OS コマンド) / 2.3 | [JVN](https://jvn.jp/jp/JVN19906678/) |
| 2026-11-18 | JVNVU#99608534 / CVE-2026-114938 | OpenJDK (各ディストリビューション) | Base64 デコーダのヒープバッファオーバーフロー (Java4Shell) | 8.1 (3.1) / 未認証 RCE のおそれ | [JVN](https://jvn.jp/vu/JVNVU99608534/) |
| 2026-11-18 (更新) | JVNVU#91196958 / CVE-2026-94300 ほか 3 件 | ISC BIND 9 | GSS-TSIG のメッセージを同時に処理するとメモリが壊れる (JPRS は「サービスの停止・リモートコード実行」と評価)、受信処理の資源枯渇、RPZ・redirect ゾーンでの異常終了 | JPRS は「緊急」 | [JVN](https://jvn.jp/vu/JVNVU91196958/) |
| 2026-11-18 | JVNVU#99888632 | CISA ICS Advisory (11/17 分): Siemens 10 件、Dorsett Controls、三菱電機 CNC シリーズ (Update B) | 三菱電機 CNC の既存アドバイザリ (ICSA-26-078-05) の更新を含む | 各アドバイザリ参照 | [JVN](https://jvn.jp/vu/JVNVU99888632/) |
| 2026-11-18 | JVNVU#96847970 | OpenSSL (11/17 のアップデート) | 前号で扱った QUIC の DoS などの修正の JVN 掲載 | 各 CVE 参照 | [JVN](https://jvn.jp/vu/JVNVU96847970/) |

> JVN iPedia の 11/18 の新規登録は、Microsoft の 11 月の月例、Oracle、MongoDB のドライバ、IBM などの海外製品が中心で、国内ベンダーの新規は上の宮内庁アプリのみだった。

### 国内コミュニティ・研究・イベント

#### [2026-11-18] PortSwigger Research に衣川正人 (Masato Kinugawa) 氏が寄稿: 「innerHTML で `=` が使えない」XSS の "不可能" ラボを解く
- **何が起きたか**: Gareth Heyes 氏が 2020 年に「JavaScript の実行は不可能」とした課題の一覧のうち、「innerHTML の文脈で、`=` を使えない」注入で任意の JavaScript を実行する方法を、衣川氏がゲストとして解説した。
- **なぜ重要か**: 属性値の `=` を落とすフィルタは「属性を書けない = 安全」とみなされがちで、診断で見逃しの原因になる。国内の研究者の成果が、XSS のペイロードの「できない」の境界を動かした。報告書で「悪用は困難」と書く前に読んでおく価値がある。
- 出典: [PortSwigger Research](https://portswigger.net/research/achieving-the-impossible-xss-in-innerhtml-without-equals)

#### [2026-11-18〜19] Zenn (AWS Japan): AI ペンテスト「AWS Continuum」を OWASP Juice Shop・Web アプリ・LLM アプリ・脅威モデリングで試した検証レポート 4 本
- **何が起きたか**: AWS Japan のメンバーが、AWS Continuum のペネトレーションテスト機能を Juice Shop、Web アプリ、LLM アプリに当てた結果と、脅威モデリングへの使い方を、それぞれ記事にまとめた。
- **なぜ重要か**: 同じ週に THN でも「AI ペンテストの心配は品質より、データの扱いと本番への影響」という記事が出ている。国内の実務者が、検出の範囲と手順を具体的に書いた資料は、AI ペンテストの採否を決めるときの比較の材料になる。
- 出典: [Zenn (Juice Shop)](https://zenn.dev/aws_japan/articles/continuum-pentest-console-juice-shop) / [Zenn (Web App 編)](https://zenn.dev/aws_japan/articles/5381a11e111780) / [Zenn (LLM App 編)](https://zenn.dev/aws_japan/articles/524d87d9c2384d) / [Zenn (脅威モデリング)](https://zenn.dev/aws_japan/articles/b072aafbc58fcd)

#### [2026-11-18] Zenn: 「Unreal MCP の localhost は認証の代わりにならない」/ ローカル LLM でデセプションを試した実験
- **何が起きたか**: 1 本目は、ゲームエンジン向けの MCP サーバーが localhost で待ち受けることを認証の代わりにしている危うさを論じた。もう 1 本は、ローカルの LLM を使って、AI の攻撃者に対するデセプション (おとり) の効き目を試した。
- **なぜ重要か**: 1 本目は、本号の CVE 表の HyperFrames (CVE-2026-130843) と同じ「localhost の開発用サーバーは、ブラウザ経由と DNS rebinding で外から届く」話になる。2 本目は、arXiv の「LLM のハニーポット vs LLM の攻撃者」(2611.22589) と同じ問題意識を持つ。
- 出典: [Zenn (Unreal MCP)](https://zenn.dev/heftykoo/articles/c6a9a22b7885c9) / [Zenn (デセプション)](https://zenn.dev/masuda_masuo/articles/2026-11-18-ai-deception-lab)

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 120 (RSS / Atom 57 本、記事の本文の個別取得 約 75、CISA KEV JSON、NVD API 2.0 (11/17〜19 の公開分 1,843 件)、FIRST EPSS API、JVN / JVN iPedia、ScanNetSecurity の 11/17〜18 掲載分 32 本の本文、WebSearch 3 クエリ)
- 採用件数: AI技術=11 / AIセキュリティ=7 (arXiv 4 本は 1 項目) / セキュリティ=12 (短信 6 を含まず、深掘り 1 件は別) / CVE=14 行 / 国内インシデント=4 / 国内政策=4 / JVN=5 行 (うち更新 1) / 国内コミュニティ=3
- 除外理由内訳: 古すぎ=約 45 (ScanNetSecurity の 11/17〜18 掲載分 30 本 [組織の公表はすべて 11/12 以前]、東京都水道局の HDD 紛失 [11/16]、古川デジタル大臣の発言 [11/10]、uBlock Origin の UXSS [公表 11/15]、警察庁長官の指示 [11/6]、日本郵便 JP Business Tool Box [公表日を確認できず]、Rapid7 の ONLYOFFICE [11/17 号で掲載済み] など) / 重複=約 40 (GPT-6.2、MAI Code 2、Optimizely の本体、Puppet の KEV、Cursor の Claude Code 拡張、Project Zero の期限短縮、Sleeper Agent、MCP のツール名の衝突、JPCERT/CC の報告書チェックリスト、KARTE の既出組織、楽天証券・富岳の本体、GitHub の MDASH など) / 日付不明・一次未確認=約 4 (肥後銀行の最大 37 万件と三菱 UFJ モルガン・スタンレー証券の 28 万件は、ニッキンの関連記事の見出しだけで公表日を確認できず未掲載。Dark Reading のブラジルの電子署名アプリの RCE は本文 403 で中身を確認できず未掲載)
- 取得失敗ソース: openai.com の本文 (403 → RSS の要約で代替)、Dark Reading の個別記事 (403 → RSS の要約)、TechCrunch の Anthropic の IPO の記事 (404)、github.com と GitHub API (403 / このセッションのアクセス対象外 → NVD の references で修正コミットの URL を取得。OpenJDK と NGINX の修正コミットは特定できず advisory で代用)、Huntress・MSRC・トレンドマイクロ (日本) の RSS (XML の解析エラー)、GTIG の RSS (解析エラー → THN と The Record で代替)、Anthropic の RSS (404)。

</details>
