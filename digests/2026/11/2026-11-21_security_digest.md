# KEDA Daily Digest — 2026-11-21 (JST)

> 採用範囲: 公開日 2026-11-19 〜 2026-11-21
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

本号の中心は、前号で「Onigmo と大文字・小文字変換のメモリ安全性の欠陥 7 件」として扱った Ruby の更新の続報。そのうち 1 件が **「Ruby2Shell」(CVE-2026-132825)** と名付けられ、**既定の Rails と classic スタイルの Sinatra で、認証前に届く**ことがわかった。Veria Labs は 11/25 に「素の Rails での RCE の PoC」を公開すると予告している。GitLab は 11/20 に Ruby を入れ替える Critical Patch を出した。GitHub Enterprise Server は、まだ修正版がない側に入っている。
ほかのセキュリティの話題では、CISA が KEV に vCenter・Cisco Expressway・Apache Roller・SAP NetWeaver の 4 件を加えた (期限 11/23)。AMD ホストで入れ子の仮想化を有効にしている KVM では、ゲストからホストのメモリを読める欠陥 (CVE-2026-99312) が見つかった。Windows には、ロック画面からプログラムを動かせる未修正の手口「FastUnlock」が出た。ASUS は資産管理ツールのハードコード鍵 (CVSS 10.0) を、WatchGuard は Dimension の未認証 SQL 実行を修正した。
AI では、Anthropic の数学者が **「Claude と一緒にリーマン予想を証明した」と主張した** (検証はこれから)。OpenAI は、推論過程を抜き出して蒸留する攻撃への対策で、攻撃の成功率を 54.0% から 0.2% に下げたと発表した。AI セキュリティでは、Amazon が **AI ペンテスト基盤 Cairn を使った中国系の攻撃者が、OSS の医療画像 AI アプリの 0-day を自力で見つけて大学に侵入した** と報告した。Bell Canada は「エージェント型の攻撃者」に企業顧客のデータを盗まれたと認めた。
国内では、**デジタル庁が、政府共通基盤 GSS のファイル共有サービスで 7/30〜11/12 に正規の相手以外からのアクセスがあり、ファイルが漏えいした可能性がある**と公表した。湘南美容クリニックなどを支える SBC メディカルグループは、米 SEC への届出で 162 万 4,000 人分の流出を開示した。KARTE は調査結果を出し、再開の目標を 2027 年 1 月中旬とした。
**今日まず見るべき 2 件**: (1) 稼働中の Ruby の版を、実行中のプロセスの単位で洗い出す (Gemfile.lock や依存スキャナには出ない。深掘り参照)。(2) OpenAPI のコード生成 (Refitter / Tapir / Jane) を、外部から受け取った仕様書で CI 上で回していないかを確かめる (CVE 所感参照)。

## 今日の深掘り

### [2026-11-19〜20] [続報] Ruby2Shell (CVE-2026-132825): 大文字・小文字の変換の 1 バイトのヒープオーバーフローが、既定の Rails / Sinatra では認証前に届く。PoC の公開は 11/25 の予定で、GitLab は Critical Patch を出した

- **前号から変わったこと (事実)**:
  - 11/18 の Ruby の更新 (4.0.10 / 3.4.13 / 3.3.14) で直った 7 件のうち、GHSA-34m4-m9fh-gqp5 に CVE-2026-132825 が割り当てられ、Veria Labs が「Ruby2Shell」と名付けた解析ページを 11/19 に公開した。Ruby は Critical、MITRE (CNA) の CVSS は 7.4。
  - Veria Labs によると、**既定の設定の Rails と classic スタイルの Sinatra に、認証なしで届く**。同社は「素の Rails で RCE を実証した最初の組織」と名乗り、主要ベンダーの修正が出そろえば **11/25 に RCE の PoC を公開する**と予告している。
  - Semgrep は 11/19 の解説で、Rails 8.1 / 7.2、Sinatra 4.2 / 3.2、Rack 3.2 / 2.2 で、クライアントが指定した文字コードの文字列がそのまま `upcase` に届くことを実行時に確かめた。攻撃コードは書いていないと明記している。
  - GitLab は 11/20 に 19.6.1 / 19.5.8 / 19.4.10 の Critical Patch Release を出し、同梱の Ruby を入れ替えた。ソースから入れている場合は、Ruby 3.3.14 か 3.4.13 以降で作り直す必要がある。Mastodon (4.7.6 ほか)、Chatwoot (v4.20.1)、Discourse の Docker イメージも対応した。Veria Labs の一覧では **GitHub Enterprise Server は修正版がない「Vulnerable」** に入っている。
  - 実際の悪用の報告はない。CISA の SSVC は Exploitation: none、Technical Impact: total。
- **技術的な中身**:
  - 欠陥があるのは、ISO-8859-1 / 2 / 3 / 4 / 9 / 10 / 13 / 14 / 15 / 16 と Windows-1250 / 1252 / 1254 / 1257 の、14 種類の 1 バイト文字コードでの大文字・小文字の変換。`ß` (0xDF) には 1 バイトの大文字がないので、大文字にすると `SS` の 2 バイトを書く。ところがループの境界チェックは、出力バッファに 1 バイトの空きがあるかしか見ていなかった。
  - 出力バッファの大きさは「入力の長さ + 20 バイト」。`ß` が 1 つあるごとに出力が 1 バイト伸びるので、**21 個で末尾を 1 バイト越える**。書き込まれる値は `S` (0x53。ケースフォールディングでは `s`) に固定されるが、バッファの大きさは入力の長さで攻撃者が決められる。結果をコピーするときにも、1 バイトの範囲外読み取りが起きる。
  - 届くメソッドは `upcase` / `swapcase` / `downcase(:fold)` / `casecmp?` (破壊的メソッドと Symbol のメソッドを含む)。Semgrep によると、`capitalize`、普通の `downcase`、正規表現の `/i` は届かない。UTF-8 の文字列は別の処理を通るので影響を受けない。
  - **認証前に届く経路 (sink までの道筋)**: `Rack::MethodOverride` は、multipart のリクエストに含まれる `_method` フィールドの値を大文字にする。multipart の各パートは `charset` を宣言でき、Rack はそれに従う。そのため、アプリ自体が UTF-8 で動いていても、攻撃者が宣言した文字コードのまま `upcase` に値が届く。`Rack::MethodOverride` はルーティング、CSRF のチェック、認証よりも前に動く。
  - Semgrep の整理では、Rails の `api_only` のアプリには `Rack::MethodOverride` が入らないので届かない。modular スタイルの Sinatra は `method_override` を有効にしたとき、素の Rack はミドルウェアを入れたときだけ届く。HTTP ヘッダ、JSON、クエリ、通常のフォームの値はバイナリか UTF-8 として扱われるので、届かない。ただし、アプリのコードが multipart のパラメータを自分で大文字にしていれば、`api_only` でも届く。Rodauth の `create_account` (サインアップ時の比較) も経路になりうると、コードを読んで指摘している。
  - 影響を受けるのは CRuby 2.4.0〜3.3.13、3.4.0〜3.4.12、4.0.0〜4.0.9。**10/23 の正規表現の修正で上げた 4.0.9 / 3.4.12 / 3.3.13 が、ちょうど影響を受ける最新版**にあたる。3.2 以前はサポートが終わっており、修正は出ない。JRuby と TruffleRuby は影響を受けない。修正コミットは [ruby/ruby@d582f8f](https://github.com/ruby/ruby/commit/d582f8f13d700d8e39714d3a8f11eb4bd2bc69f0) で、境界チェックを 2 バイト分に直した。
- **背景・経緯 (背景引用)**: 一連の修正は、前号で扱った Onigmo の二重解放やコンパイル後のサイズのオーバーフローと同じリリースに含まれる。報告者として、Ada Logics の Stephan Lipp 氏、Anthropic、OpenAI と組んだ Moritz Sanft 氏が挙がっている。ディストリビューションの対応はまちまちで、Ubuntu は USN-9176-1 で修正版を出したが、Debian の bookworm / trixie と RHEL の ruby 系は、piyolog がまとめた時点で修正待ちだった。
- **なぜ今これが重要か (評価)**:
  - 書けるのは 1 バイトで、値も固定されているので、本番環境での RCE はメモリの配置を整えるのが難しい (watchTowr も SecurityWeek にそう述べている)。それでも、**届く経路が「既定の Rails で、認証より前」**というのは大きい。PoC の公開日も決まっている。11/25 以降は、少なくともクラッシュ (DoS) の試行が一斉に来ると見ておきたい。
  - この欠陥は **gem ではなくインタプリタにある**。`bundle update` では直らず、Gemfile.lock にも依存スキャナにも出てこない。Ruby を同梱した製品 (GitLab、GHES、Discourse など) は、ベンダーの修正を待つしかない。
  - 診断の観点では、「multipart のパートの `charset` 宣言が、フレームワークの前処理で尊重される」という性質そのものが攻撃面になる。Python (Werkzeug)、PHP、Node (busboy) などで、multipart のパートの文字コードを尊重したうえで大文字・小文字の変換をする処理がないかは、横に展開して見る価値がある。
- **読者が今日できること**:
  - 実行中のプロセスが読み込んでいる Ruby の版を確かめる (`ps` から PID を取り、`/proc/<pid>/exe -v`、またはコンテナごとに `ruby -v`)。1 台に複数の Ruby が同居している場合があり、ベースイメージの版を見ただけでは判断できない。Semgrep の記事には、Linux / macOS / Windows / Kubernetes 向けの検出スクリプトがある。
  - 自分のアプリで `grep -rnE "\.(upcase|swapcase|casecmp\?)|downcase\(:fold\)" app/ lib/` を実行し、外部入力に `force_encoding` や `encode` で旧来の 1 バイト文字コードを付けてから変換している箇所を探す。`config.api_only` かどうかと、`Rack::MethodOverride` がミドルウェアに入っているか (`bin/rails middleware`) も確かめる。
  - 診断の対象が Rails なら、`_method` のパートに `Content-Type: text/plain; charset=ISO-8859-1` と `ß` を 21 個以上 (奇数個) 入れた multipart を送り、500 エラーやワーカーの再起動が起きるかを見る。**本番では行わず、検証環境で**。
- 出典: [Veria Labs「Ruby2Shell」(2026-11-19)](https://verialabs.com/ruby2shell/) / [Semgrep (2026-11-19)](https://semgrep.dev/blog/2026/ruby2shell-cve-2026-132825/) / [GitLab Critical Patch Release 19.6.1 (2026-11-20)](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-6-1-released/) / [SecurityWeek (2026-11-20)](https://www.securityweek.com/ruby-patches-ruby2shell-vulnerability-that-could-lead-to-rce/) / [piyolog (2026-11-20)](https://piyolog.hatenadiary.jp/entry/2026/11/20/224814) / [Ruby 公式 (2026-11-18、背景)](https://www.ruby-lang.org/en/news/2026/11/18/multiple-vulnerabilities-in-regexp-and-string/) / [GHSA-34m4-m9fh-gqp5](https://github.com/ruby/ruby/security/advisories/GHSA-34m4-m9fh-gqp5)

## AI 技術・トレンド

### [2026-11-20] Anthropic の数学者 Levent Alpöge 氏、「Claude と一緒にリーマン予想を証明した」と主張。証明は Lean で形式化したとしているが、独立した検証はまだない
- **何が起きたか**: Alpöge 氏は自分のサイトで、Claude との共同作業でリーマン予想の証明を見つけ、手法は一般化リーマン予想にも広がると主張した。議論は前提なしで Lean に形式化したとしている。The Verge によると、Anthropic はこの発表に関わっておらず、コメントもしていない。8 月の時点で同社は「Claude の手法がリーマン予想の証明につながるとは考えていない」と述べていた。クレイ数学研究所の規則では、懸賞の対象になるには、出版後 2 年以上の検証を経て数学界に広く受け入れられる必要がある。Simon Willison も同氏の文章を引用している。
- **なぜ重要か**: 正しいかどうかは、数学者による検証と Lean の証明の点検で決まる。ただし、「形式化した」という主張は、Lean のカーネルが通ったかどうかで真偽を確かめやすい。成り立てば、AI が補助した形式証明が、最難関の未解決問題にまで届いたことになる。セキュリティでは、暗号の安全性の証明やプロトコルの形式検証で、同じ道具立てを使える範囲がさらに広がる。
- 出典: [The Verge (2026-11-20)](https://www.theverge.com/ai-artificial-intelligence/1010051/anthropic-riemann-hypothesis-millennium-prize-problem) / [TechCrunch (2026-11-20)](https://techcrunch.com/2026/11/20/ai-claimed-a-solution-to-the-167-year-old-riemann-hypothesis-and-a-human-did-too/) / [Simon Willison (2026-11-20)](https://simonwillison.net/2026/Nov/20/levent-alpoge/)

### [2026-11-19] [続報] Anthropic の上場: Amodei CEO は鐘を鳴らす前のスピーチで「AI は人間の管理下にとどめる」と表明。創業者 7 人は約 20 億ドル分の株を売り出した
- **何が起きたか**: 前号の上場の続報。Amodei 氏はスピーチで、事業の圧力にも政治の圧力にも屈しないと述べ、9 月に示した「AI 開発のペースを調整する」計画 (主要各社による安全基準の協調、第三者の評価者の受け入れなど) にあらためて触れた。TechCrunch は、創業者 7 人が IPO で約 20 億ドル分の株を売り出したと報じた。上場で慈善団体に最大 1,560 億ドルが入る可能性があるという試算も出ている。
- **なぜ重要か**: 上場企業になると、「安全のためにリリースを遅らせる」判断が、株主への説明責任と正面からぶつかる。第三者の評価者を受け入れるという約束が実際に守られるかは、Claude を診断業務に使う側にとっても、モデルの能力の公表範囲 (サイバー能力の評価結果) に関わる。
- 出典: [TechCrunch (2026-11-19)](https://techcrunch.com/2026/11/19/at-nasdaq-opening-bell-anthropic-ceo-recommits-to-pacing-ai-development/) / [TechCrunch (2026-11-19)](https://techcrunch.com/2026/11/19/anthropics-7-founders-cashed-out-nearly-2b-in-record-breaking-ipo/)

### [2026-11-19] OpenAI、ChatGPT の常時稼働エージェント「dots」を Plus の一部ユーザーと Business Standard に広げる
- **何が起きたか**: OpenAI のプロダクト責任者 Thibault Sottiaux 氏が X で発表した。dots は 9 月に発表されたエージェントで、利用者が決めた目標に沿って、クラウドかローカルのコンピュータを操作して動き続ける。これまでは Pro (月額 16,800 円から) と Business Premium / Enterprise に限られていた。OpenAI Japan によると、dots の週間アクティブユーザー数で日本は世界 2 位。
- **なぜ重要か**: 月額 3,000 円のプランで、ローカルの端末を操作する常時稼働のエージェントが使えるようになる。企業の端末で個人の契約の dots が動いている状況は、シャドー AI の新しい形になる。EDR や DLP の観点では、「エージェントのプロセスがどの資格情報でどこに通信しているか」を見られるようにしておきたい。
- 出典: [ITmedia AI+ (2026-11-20)](https://www.itmedia.co.jp/aiplus/article/2611/20/2000003359/)

### [2026-11-19] Apple、自社の AI エージェントを作るエンジニアを募集 (Bloomberg が求人を確認、現在は削除)
- **何が起きたか**: Bloomberg が見つけた求人によると、Apple はウェブの閲覧、アプリをまたいだ作業、コードの作成、サービスの呼び出しをこなすエージェント型アシスタントの開発を率いるエンジニアを探している。The Verge は、Meta の Muse、OpenAI の dots、Anthropic の Duet、Google の Tasks と競う位置づけだと整理した。
- **なぜ重要か**: Apple が加われば、主要な OS のベンダーがすべて「OS に組み込んだ、画面を読むエージェント」を持つことになる。下の Signal の件のように、アプリ側でエージェントを締め出す手段を求める声は強まる。iOS / macOS アプリの診断では、エージェントが読める画面に何が出ているかが、新しい確認項目になる。
- 出典: [The Verge (2026-11-19)](https://www.theverge.com/tech/1038227/apple-ai-agent-engineer-job-listing) / [TechCrunch (2026-11-19)](https://techcrunch.com/2026/11/19/apple-may-be-developing-its-own-ai-agent-that-runs-your-mac/)

### [2026-11-19] OpenAI「Performance Factory」: Codex のエージェントが、性能の劣化の調査から修正、効果の確認までを自動で回す
- **何が起きたか**: OpenAI は、ChatGPT の性能の劣化 (リグレッション) を Codex のエージェントで直す仕組みを公開した。性能のアラートが出るとタスクが開かれ、エージェントが原因を調べて修正を提案し、エンジニアが確認する。デプロイの後は、別のエージェントが同じタスクを引き取り、性能が元の水準に戻ったかを確かめる。約 3 か月運用しているという。
- **なぜ重要か**: 「アラート → 調査 → 修正案 → 人の確認 → 効果の検証」という型は、脆弱性の対応 (検知 → 再現 → パッチ → 回帰テスト) にそのまま当てはまる。修正の候補を出すまではエージェントに任せ、人は承認だけを担うという分担が、大手の本番運用で成り立っている例として記録しておきたい。
- 出典: [OpenAI (2026-11-19, RSS)](https://openai.com/index/how-openai-performance-factory-keeps-chatgpt-fast) / [GIGAZINE (2026-11-20)](https://gigazine.net/news/20261120-openai-chatgpt-performance-factory/)

### [2026-11-20] OpenAI「MedChemBench」: 創薬化学の推論を 99 問で測る。GPT-6.2 Astra は 84.5%
- **何が起きたか**: OpenAI は、分子の構造と実験の結果を結びつけて説明し、次に試す化合物を選べるかを測るベンチマークを公開した。99 問は既存の論文から作った。xhigh の推論設定で、GPT-6.2 Astra が 84.5%、GPT-6 Astra が 83.3%、GPT-6.1 Sol が 82.0%、GPT-5.6 Sol が 58.2%。化合物の選択と、性質の数値の予測は難しかったという。
- **なぜ重要か**: GPT-5.6 から 6 系で大きく伸び、その後は頭打ちに近い。ベンチマークの飽和が早いことを示す例でもある。生物学の能力が上がると、各社はバイオの安全策を強める。下の「蒸留への対策」とも、この流れでつながっている。
- 出典: [OpenAI (2026-11-20, RSS)](https://openai.com/index/introducing-medchembench)

### [2026-11-20] Hugging Face「harness adapters」: 重みを固定したまま、エージェントのハーネスに合わせて LoRA を強化学習で作る。Qwen3.8-27B の Terminal-Bench 2.1 は 39% → 55%
- **何が起きたか**: Hugging Face は、自分が使うハーネスとタスクの分布の上で強化学習をかけた LoRA (harness adapter) を足すと、精度と効率が両方上がると報告した。Qwen3.8-27B を pi ハーネスで動かすと Terminal-Bench 2.1 は 39% で、1 タスクあたり平均 2.9K トークンを使う。アダプタを足すと pass@1 は 55%、トークンは 1.5K に減った。推論とツールの呼び出しが減り、1 回目で正解することが増えたのが主な理由だという。同じ週には、RadixArk が Qwen3.8-27B を 1,200 個の長いエージェントのタスクで強化学習した「DaisyRose-27B」を公開し、Terminal-Bench 4.1 を 5.6% から 12.0% に上げた (H200 を 144 基、18 日)。
- **なぜ重要か**: 中規模のオープンモデルでも、「自分のハーネス + 自分のタスク」で強化学習をかければ、汎用の大型モデルとの差を詰められる。診断のツールチェーン (Burp や nuclei を呼ぶ自前のエージェント) に合わせたアダプタを社内で作る、という選択肢が現実的になってきた。
- 出典: [Hugging Face (2026-11-20)](https://huggingface.co/blog/harness-adapters-at-scale) / [Hugging Face / RadixArk (2026-11-19)](https://huggingface.co/blog/RadixArk/daisyrose-27b-pushing-the-frontier-of-post-trainin)

### [2026-11-20] 論文「Language Models Can Rewrite Their Own Weights」: 勾配を使わず、モデル自身が自分の重みを調べて書き換え、27B で 6.6 ポイント改善
- **何が起きたか**: イリノイ大学アーバナ・シャンペーン校やカーネギーメロン大学などの研究者は、Qwen3.5 の 2B / 4B / 9B / 27B に、自分の重みを読み書きする機能と Python の実行環境を与えた。モデルは数学の問題への自分の回答と内部状態を調べ、問題の原因を推測して重みを変え、効果を確かめた。勾配降下法も誤差逆伝播も使っていない。27B では、同じ文を繰り返して回答を終えられなくなる不具合を自分で直し、正答率が 6.6 ポイント上がったという。
- **なぜ重要か**: 査読前の論文で、規模も小さい。ただ、「エージェントに自分の重みへの書き込み権限を渡す」構成が現れたこと自体が、安全性の評価の前提を揺さぶる。モデルの重みのファイルへの書き込み権限は、今後エージェントの権限管理で明示的に扱うべき対象になる。
- 出典: [GIGAZINE (2026-11-20)](https://gigazine.net/news/20261120-large-language-model-can-rewrite-itself/) / [arXiv 2611.21885](https://arxiv.org/abs/2611.21885)

### [2026-11-20] Microsoft、USB4 ケーブルだけで Windows PC 同士をつなぎ、大きなローカル LLM を分散して動かす「RDMA over USB4」を発表
- **何が起きたか**: Microsoft は、USB4 で PC 同士をつなぎ、メモリと GPU の計算能力を共有して大きなモデルを動かす機能を、開発者向けプレビューとして準備している。16KiB をやり取りするときの遅延は、Ethernet over USB4 の 194 マイクロ秒に対して 50 マイクロ秒。AMD Ryzen AI Max と Intel Core Ultra Series 3 の PC で試験しているという。
- **なぜ重要か**: 機密のコードを外部の API に送れない現場で、ローカルの大型モデルを動かす選択肢が増える。一方で、RDMA はホストのメモリに直接書き込む仕組みなので、物理的につながった相手を信頼する前提になる。DMA 攻撃 (Thunderbolt の過去の事例) と同じ観点で、IOMMU による保護とペアリングの手順を確かめたい。
- 出典: [GIGAZINE (2026-11-20)](https://gigazine.net/news/20261120-rdma-over-usb4-windows/)

### [2026-11-20] トランプ大統領、米企業が国外に AI データセンターを建てれば「とてつもない税」をかけると発言
- **何が起きたか**: トランプ大統領は、習近平国家主席、プーチン大統領との首脳会談の後の記者会見で、米国の企業に国外でデータセンターを作らせないと述べた。一方で、米国内では州や市がデータセンターの新設を制限する動きが広がっている。
- **なぜ重要か**: 実際に課税されれば、米国の大手クラウドが日本や欧州に計算資源を置く計画に影響し、データの所在地 (ソブリンクラウド) の議論にも波及する。今の段階では発言にとどまる。
- 出典: [The Verge (2026-11-20)](https://www.theverge.com/policy/1038892/trump-foreign-data-centers-tax)

### [2026-11-20] 国内: 「Antigravity を他社の AI から操作するとアカウント停止か」。Google Cloud 日本法人は、規約の対象は個人向けプランで、法人向けプランでは停止は起きないと説明
- **何が起きたか**: 「Google Antigravity 追加利用規約」の 6 条は、サードパーティのツールでサービスにアクセスすること (例: OpenClaw を Antigravity の OAuth で使うこと) を違反とし、Antigravity / Gemini CLI のアカウントの停止の理由になりうると定めている。X では、ヘッドレスで起動する `agy -p` を使うと Google アカウント全体が止まるのではという懸念が広がった。グーグル・クラウド・ジャパンは ITmedia の取材に、この規約は個人向けプラン (無料と Google AI Pro) が対象で、法人向けプランには別の規約が適用されると答えた。Google DeepMind の Varun Mohan 氏は X で「Google アカウントには影響しない」と述べた。
- **なぜ重要か**: 他社のエージェントから CLI を呼び出す使い方は、診断の自動化でもよく使う。個人の契約で業務の自動化を組むと、規約違反でワークフローごと止まるおそれがある。業務で使うなら法人向けの契約に寄せる、というのが現実的な判断になる。
- 出典: [ITmedia AI+ (2026-11-20)](https://www.itmedia.co.jp/aiplus/article/2611/20/2000003353/)

### [2026-11-20] 国内: 京都大学の学生相談部門、「AI に悩みを相談する際に気をつけて欲しいこと」と AI 依存のチェックリストを公開
- **何が起きたか**: 京都大学の学生相談部門は、ハルシネーション、利用者に迎合する回答、人間のように錯覚させる作用を課題として挙げた文書を公開した。チェックリストに当てはまる項目があれば「しばらく AI を触らないで生活してみること」を勧めている。
- **なぜ重要か**: 大学が、AI の使い方の注意を、情報セキュリティではなく心の健康の観点から出した例。迎合的な回答 (sycophancy) は、診断でも「AI がこの欠陥は安全だと言った」という判断の誤りにつながる。同じ癖を持つ道具として意識しておきたい。
- 出典: [ITmedia AI+ (2026-11-20)](https://www.itmedia.co.jp/aiplus/article/2611/20/2000003378/)

## AI セキュリティ

### [2026-11-20] Amazon: 中国系の攻撃者が AI ペンテスト基盤「Cairn」を動かし、OSS の医療画像 AI アプリの 0-day (パストラバーサル) を自力で見つけて、東アジアの大学 2 校に侵入
- **何が起きたか**: Amazon Integrated Security の CISO、CJ Moses 氏によると、9/10 に、Cairn が公開状態で動いているサーバーを見つけ、過去のプロンプトを含む操作の履歴を読めた。プロンプトは簡体字の中国語で、タイムスタンプは中国標準時だった。攻撃者は IP アドレスを渡して「シェルを取れ」と指示しただけで、エージェントが計画、実行、手直しを自分で回した。16 時間で 148 の操作をした試行 (Log4Shell の悪用の失敗を含む) と、実在する 80 人のユーザー名で 3 万通り以上の認証情報を 6 時間以上試した試行は、どちらも失敗した。成功したのは、OSS の医療画像 AI アプリのパストラバーサルを見つけて悪用したときだけで、同じ欠陥で 2 校目にも侵入した。Amazon は、対応する修正、issue、advisory がなかったことから、0-day だと「高い確度で」評価している。メンテナには連絡済みで、修正された。
- **なぜ重要か**: 「AI が自力で 0-day を見つけて実際の侵入に使った」ことを、攻撃者側の操作の履歴で裏づけた事例になる。一方で、成功したのは守りの薄い OSS の AI アプリで、Log4Shell やパスワードの総当たりは失敗している。**AI の攻撃が最初に当たるのは、研究機関が立てた、手入れの行き届かない AI / ML アプリ**だと読める。大学や研究所の診断では、GPU サーバー上の推論アプリ (Gradio、Streamlit、医療画像のビューア) を優先して棚卸ししたい。
- 出典: [The Record (2026-11-20)](https://therecord.media/amazon-research-cairn-ai-university-attacks-possible-zero-day) / [BleepingComputer (2026-11-20)](https://www.bleepingcomputer.com/news/security/hackers-use-autonomous-ai-tool-cairn-to-find-zero-day-take-over-server/)

### [2026-11-20] Bell Canada、「エージェント型の攻撃者」が 11/17 に複数のシステムに入り、回線の発注・開通管理システム (Maximo) から企業顧客のデータを盗んだと認める
- **何が起きたか**: Bell の通知によると、侵入されたのは、通信回線の発注と開通に使う Maximo の本番前環境。流出した可能性があるのは、企業顧客の担当者の氏名、役職、メールアドレス、電話番号、住所、チケットの件名、ネットワーク機器に結びついた一部の IP アドレス。認証情報や添付ファイルは含まれないという。Bell は BleepingComputer に「agentic threat actor」がシステムに入ったと説明し、IOC をカナダ・サイバーセキュリティセンター (CCCS) と企業顧客に共有しているが、一般には公開していない。
- **なぜ重要か**: 大手の通信事業者が、公式に攻撃者を「エージェント型」と表現した。どう判断したのか (操作の速さ、並列性、プロンプトの痕跡など) は明かしていない。狙われたのが本番前の環境で、チケットの件名と機器の IP が流出したことは、次の標的の偵察に使える情報になる。本番前の環境に本番の顧客データを置く運用は、国内の楽天証券の件 (前号まで) と同じ構図。
- 出典: [BleepingComputer (2026-11-20)](https://www.bleepingcomputer.com/news/security/bell-canada-says-agentic-hacker-stole-enterprise-customer-data/)

### [2026-11-20] OpenAI「Combatting adversarial distillation」: 推論過程 (CoT) を抜き取って蒸留する攻撃への対策を強化。GPT-6.2 Astra への抽出攻撃の成功率は 54.0% → 0.2%
- **何が起きたか**: OpenAI は、自社モデルの出力を無断で使って別のモデルを学習させ、安全策のないまま能力だけを移す「敵対的蒸留」への対策を説明した。特に、内部で生成する推論過程 (protected reasoning) を抜き出されないことを重視している。自動のレッドチーミングで、以前のやり取りで生成された推論過程を取り出せるかを試すと、攻撃の成功率は元の安全策の GPT-6 Astra で 54.0%、更新した GPT-6.2 Astra で 0.2% だった。サイバーの能力が「普通の出力 + 推論過程」からどれだけ生徒モデルに移るかも、社内で調べている。
- **なぜ重要か**: 防御の側で使っている脆弱性の発見の能力が、蒸留を通じて安全策のないモデルに移るというリスクを、ベンダーが数字で認めた。利用者には、推論過程を見せない、要約しか返さない、という方向がさらに強まる。診断の報告書の「AI がなぜそう判断したか」の根拠が取りにくくなる面もある。
- 出典: [OpenAI (2026-11-20, RSS)](https://openai.com/index/combatting-adversarial-distillation)

### [2026-11-20] Signal、Android / iOS で画面の撮影を制限。OS に組み込まれた AI エージェント (Gemini、Siri) が会話を読むのを防ぐため
- **何が起きたか**: Signal の Meredith Whittaker 代表はブログで、画面の情報を分析する OS のエージェント機能が「Signal が自力でプライバシーを守る能力を損なっている」と述べた。Google、Apple、Microsoft は、エージェントによるデータへのアクセスをアプリの開発者が制限する手段を用意しておらず、macOS では同様の保護をまだ実装できないとしている。
- **なぜ重要か**: E2E 暗号化は、端末の上で動くエージェントには効かない。モバイルアプリの診断では、`FLAG_SECURE` (Android) や画面の収録の検知 (iOS) が機微な画面で設定されているかが、OS のエージェント対策としても意味を持つようになった。
- 出典: [The Verge (2026-11-20)](https://www.theverge.com/ai-artificial-intelligence/1038390/signal-blocking-ai-agent-screenshots-mobile-app)

### [2026-11-20] 研究: プロンプトインジェクションの自動レッドチームは、成功した攻撃を数多く集めるほど良いわけではない。数で勝ったツールの攻撃で再学習したモデルの方が、乗っ取られやすかった
- **何が起きたか**: ウォータールー大学、浙江大学、KTH の研究者は、PISmith と RL-Hammer の 2 つの攻撃ツールで Qwen3-4B を 560 タスクで攻めた。PISmith は 68.75% のタスクを破り、成功した攻撃を 7,132 件集めた (RL-Hammer は 33.39%、4,282 件)。ところが、それぞれの攻撃で強化学習をかけ直し、未知の 3 種類の攻撃を試すと、乗っ取られた割合の最悪値は、PISmith で学習したモデルが 47.5%、RL-Hammer の方は 27.5% だった。似た攻撃が大量に重なっていたことが原因とみられる。評価に使った 40 タスクは小さく、難しいものに絞っている。
- **なぜ重要か**: 「数千件の攻撃で検証済み」というベンダーの主張は、攻撃の多様性が示されていなければ、そのまま信じられない。前号の「多様性を重視したレッドチーミング」の論文と同じ結論で、AI 製品の評価を読むときの確認点になる。
- 出典: [Help Net Security (2026-11-20)](https://www.helpnetsecurity.com/2026/11/20/ai-prompt-injection-red-team/)

### [2026-11-21] ThreatFabric: Android のマルウェア基盤「Bazuka」、操作パネルに LLM を組み込み、被害者の「狙う価値」を採点させる
- **何が起きたか**: ThreatFabric は 10 月下旬、NFC リレー型のバンキング型トロイの木馬の調査中に Bazuka を見つけた。ドロッパー、コア、23 のモジュール (オーバーレイ、キーロガー、2FA と SMS の傍受、遠隔操作、暗号資産のアドレスのすり替え) からなる。ホーム画面やロック画面のスクリーンショットをオーバーレイとして被せ、裏で進む不正な操作を隠す新しい手口を持つ。操作パネルは、ローカルのモデルと API 経由のモデルの両方に対応し、サンプルのプロンプトには被害者を採点させる例があった。ドロッパーの一つは「TikTok の有料版」(`com.tiktok.premium`) を装っていた。
- **なぜ重要か**: 犯罪者の側でも、LLM が「感染した端末の中から金になる被害者を選ぶ」運用の効率化に使われている。スクリーンショットのオーバーレイは、画面を見ている利用者からは異常に気づきにくい。金融アプリの診断では、オーバーレイの検知 (`filterTouchesWhenObscured` など) の有無を確かめたい。
- 出典: [The Hacker News (2026-11-21)](https://thehackernews.com/2026/11/bazuka-android-malware-uses-fake-screen.html)

### [2026-11-20] 「トークン詐欺」: AI サービスの無料トライアルを回し続け、エージェントを無料で使い倒す・転売するグループ。ChatPRD は無料トライアルの廃止へ
- **何が起きたか**: Simon Willison は、ChatPRD の Claire Vo 氏の動画を紹介した。無料トライアルとプロモーションコードを使い回してエージェントにトンネルを掘り、Roblox や Fortnite のマップの制作など、別の商売を回すグループがいるという。よく流れるプロンプトに「自転車に乗るペリカンの SVG」があり、裏にどのモデルがあるかを探る目的とみられる。ChatPRD は無料トライアルをやめる。
- **なぜ重要か**: LLM のトークンが換金できる資産になり、アカウントの不正作成とクーポンの不正利用の対象になった。AI 機能を持つ SaaS の診断では、トライアルの作成の制限、レート制限、同じ端末・カードでの繰り返しの検知を、ビジネスロジックの欠陥として確認する価値がある。
- 出典: [Simon Willison (2026-11-20)](https://simonwillison.net/2026/Nov/20/token-fraud-is-here-and-its-bad/)

### [2026-11-20] Postman の調査 (約 9,000 人): 25% の組織が本番でエージェントに API を呼ばせている。約 4 割は、エージェントの認証情報と ID の設計が決まっていない
- **何が起きたか**: 3 割の組織は、エージェントに他の API クライアントと同じ認証情報を使わせている。動かしているエージェントの一覧を持ち、動作を監視しているのは 4 分の 1 未満で、エージェントを廃止する手順がある組織は 9% だった。回答者が最も心配しているのは、エージェントが許可されていないデータやエンドポイントに入ることだという。
- **なぜ重要か**: エージェントに専用の ID がなければ、侵害や暴走が起きたときに、そのエージェントだけを止めることができない。API の診断では、エージェント用のトークンのスコープ、他のクライアントと区別できるか、失効の手順を確認項目に加えたい。
- 出典: [Help Net Security (2026-11-20)](https://www.helpnetsecurity.com/2026/11/20/ai-agent-api-security-production/)

## セキュリティニュース

### [2026-11-20] CISA KEV に 4 件追加: VMware vCenter、Cisco Expressway、Apache Roller、SAP NetWeaver (CVE-2025-42884)。いずれも対応期限は 3 日後の 11/23
- **何が起きたか**: 11/20 付で、vCenter の認証回避 (CVE-2026-123890)、Cisco Expressway のハードコードされた認証情報 (CVE-2026-76466)、Apache Roller の信頼できないデータのデシリアライズ (CVE-2026-129448)、SAP NetWeaver のデータ問い合わせのロジックでの特殊要素の無害化不備 (CVE-2025-42884) が加わった。ランサムウェアでの利用は、どれも「不明」。EPSS は Roller 0.0119、vCenter 0.0084、Expressway 0.0042、SAP 0.0028 (11/20 時点)。
- **なぜ重要か**: **悪用を確認 (KEV)**。vCenter・Expressway・Roller の 3 件は、前号までに悪用を報じた件が、公式に確定した形。SAP CVE-2025-42884 は 2025 年に修正された古い欠陥で、新たに悪用の証拠が出たとみられる。期限が 3 日と短いのは、CISA が緊急度を高く見ている合図になる。SAP NetWeaver を持つ組織は、2025 年のパッチが当たっているかを今日確かめたい。
- 出典: [CISA KEV JSON (dateReleased 2026-11-20)](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

### [2026-11-20] Linux KVM の CVE-2026-99312: AMD のホストで入れ子の仮想化が有効なら、ゲストの root からホストのメモリを読み書きできる。DigitalOcean で約 127GB を読めた
- **何が起きたか**: Terra Security の Oren Yomtov 氏が見つけ、DigitalOcean のバグバウンティに報告した。DigitalOcean の Droplet での試験では、最初にホストのカーネルのバージョン表示が返り、続いてホストの RAM 約 127GB を読み取り専用で読めた。研究者の自前のベアメタル (他の顧客はいない) では、ゲストからホストのカーネルの生きたページに 32 バイトを書き込めた。欠陥は AMD 向けの入れ子の仮想化のコードだけにあり、Intel のホストは影響を受けない。KVM のメンテナには 10/21 に報告され、11/2 に修正がマージされた。修正版のカーネルは公開の前日に出ており、DigitalOcean はライブパッチを当てた。CVSS はカーネルの CNA が 8.8、Red Hat は暫定で 5.6 (Moderate)。
- **なぜ重要か**: **PoC は非公開、悪用の報告はない**。攻撃には、脆弱なホストの上のゲストを支配している必要がある。それでも、パブリッククラウドの「他の顧客の VM が同居しているホストのメモリ」が読めたという意味は大きい。自前で KVM を動かす事業者 (VPS、社内の検証基盤、CI のランナー) は、AMD のホストでカーネルを更新するか、`kvm_amd nested=0` にする。
- 出典: [The Hacker News (2026-11-21)](https://thehackernews.com/2026/11/new-linux-kvm-flaw-cve-2026-99312-lets.html)

### [2026-11-20] Windows のロック画面から、サインインせずにプログラムを動かせる未修正の手口「FastUnlock」。ナレーターと Microsoft アカウントの回復の画面を使う
- **何が起きたか**: MSNightmare / Nightmare Eclipse を名乗る研究者が、GitHub に動画付きで公開した。ThreatLocker が同じ日に試し、有効だと確かめた。条件は、端末に物理的に触れられることと、ロック画面の回復のオプションから Microsoft アカウントに届くこと。ナレーター (画面読み上げ) で画面を操作し、管理者ではない制限付きのアカウント (ThreatLocker によると `WSIAccount`) でプログラムを起動できた。TPM だけで BitLocker を解除する一般的な構成では、ロック画面の時点でドライブはすでに読める状態になっている。Microsoft の修正はなく、影響を受けるバージョンの一覧も出ていない。
- **なぜ重要か**: **PoC (動画) が公開されている。悪用の報告はない**。同じ研究者は前週、CLFS の権限昇格の手口も出している (前号まで)。物理的に触れられる端末 (受付の PC、共用の席、紛失したノート PC) では、TPM + PIN の起動前認証と、ロック画面からのナレーターの無効化 (グループポリシー) を検討したい。
- 出典: [The Hacker News (2026-11-20)](https://thehackernews.com/2026/11/new-unpatched-windows-0-day-fastunlock.html)

### [2026-11-19] ASUS Control Center Express にハードコードされた暗号鍵 (CVE-2026-114202、CVSS 10.0)。未認証で認証トークンを偽造し、管理者になれる
- **何が起きたか**: ASUS は v1.7.29 で 3 件の Critical を修正した。CVE-2026-114202 は、ハードコードされた鍵で、未認証のまま管理者の認証トークンを偽造できる。CVE-2026-114204 は、同じくハードコードされた鍵で、最近ログインしたアカウントのセッショントークンを権限の低い利用者が偽造できる。CVE-2026-114205 は、権限の低い利用者が管理者のアカウントを作れる認可の欠陥。ASUS の告知は v1.7.29 未満を対象としているが、CVE のレコードは v1.7.27 までしか載せておらず、v1.7.28 の扱いがはっきりしない。同じ日に、Control Center Enterprise / Datacenter で、閲覧者のロールから管理者のパスワードを変えられる CVE-2026-126574 と、Armoury Crate の権限昇格 CVE-2026-112115 も修正された。
- **なぜ重要か**: **悪用・PoC の報告はない**。PC を一元管理するツールの乗っ取りは、管理下のすべての端末へのコード配布につながる。製品ごとに同じ鍵を持つ「ハードコード鍵」は、1 台を解析すれば全導入先に効く。ファームウェアやインストーラから鍵を抜き出す診断の手法が、そのまま使える種類の欠陥。
- 出典: [BleepingComputer (2026-11-19)](https://www.bleepingcomputer.com/news/security/asus-warns-of-critical-hard-coded-key-flaw-in-control-center-express/)

### [2026-11-19] WatchGuard Dimension (Firebox のログ管理) で 15 件を修正。ログ収集サービスの認証の欠如から、未認証で任意の SQL を実行し、Web UI のプロセスでコードを実行できる (CVE-2026-86130、CVSS 4.0 で 9.3)
- **何が起きたか**: WatchGuard は 11/19 (現地時間) に公表した。Critical は 3 件。CVE-2026-86130 は、ログ収集サービスへの細工したリクエストで、未認証のまま SQL を実行し、Web UI のプロセスでコードを実行できる。CVE-2026-84322 と CVE-2026-86094 は、管理 API の応答や Web UI の診断ログから、ログイン中の管理者のセッション ID を取れる欠陥で、権限の低い管理者がスーパー管理者のセッションを乗っ取れる。
- **なぜ重要か**: **悪用・PoC の報告はない**。ログの集約サーバーは、ファイアウォールの設定とログの両方に触れられる高価値の標的。ログの受け口は「機器から届くもの」として認証を甘くしがちで、同じ種類の欠陥は他社の SIEM の収集口にもありうる。
- 出典: [Security NEXT (2026-11-20)](https://www.security-next.com/193154)

### [2026-11-21] WhatsApp が 3 件を修正。Android の広告からの返信 URL の検証不足 (CVE-2026-23871) は、詐欺のメッセージで悪用された疑い
- **何が起きたか**: CVE-2026-23871 は、Click to WhatsApp 広告への返信メッセージで、攻撃者の URL のメディアを表示させると、相手の IP アドレスが漏れる欠陥 (Android / Business for Android 2.26.17.4 未満)。WhatsApp は、詐欺の摘発の過程で見つかり、詐欺師がメッセージを本物らしく見せるために使ったとみている。CVE-2026-102769 は、非公式のクライアントから送られた「注文の詳細」のメッセージをタップすると起きる SQL インジェクションで、ローカルのファイルが消え、タイミングのサイドチャネルで 1 ビットの情報が漏れる。CVE-2026-44908 は、Meta AI の機密コンピューティング基盤の証明書の検証の欠陥。
- **なぜ重要か**: **CVE-2026-23871 は悪用の疑い**。IP アドレスの取得は、メッセンジャーを使った標的型の攻撃の偵察の第一歩になる。CVE-2026-44908 は、「AI の処理をサーバーの TEE で行うので Meta も読めない」という設計の、端末側の検証が崩れていたことを意味する。
- 出典: [The Hacker News (2026-11-21)](https://thehackernews.com/2026/11/whatsapp-patches-3-security-flaws.html) / [SecurityWeek (2026-11-21)](https://www.securityweek.com/whatsapp-fixes-flaw-uncovered-while-disrupting-scam-campaign/)

### [2026-11-20] JPMorgan Chase、Visa、Mastercard が、委託先の侵害で顧客の情報の一部が流出したと認める。n0n が 11/11 に犯行を主張した Qubole が委託先とみられる
- **何が起きたか**: JPMorgan Chase は X で、サービスを提供する第三者が攻撃を受け、委託先が持つマーケティング用のデータ (一部の顧客の氏名とメールアドレス) にアクセスされたと発表した。Visa はアジア太平洋の委託先の件で、自社のシステムと決済データは影響を受けていないと述べた。Mastercard は、特定の特典プログラムに登録した一部のカード会員のメールアドレスが出たと説明した。n0n は 11/11 に、Idera 傘下のクラウドデータ分析企業 Qubole への攻撃を主張している。
- **なぜ重要か**: **悪用 (侵害) は確定**。Qubole の盗まれたベンダーキーを入口にした件は、前号までに別の企業で報じた。分析基盤の委託先 1 社から、複数の大手金融機関に被害が広がる構図になっている。マーケティング用のデータでも、氏名とメールアドレスの組み合わせは、銀行を装うフィッシングの材料になる。
- 出典: [BleepingComputer (2026-11-20)](https://www.bleepingcomputer.com/news/security/vendor-data-breach-exposes-chase-visa-mastercard-customer-info/) / [SecurityWeek (2026-11-20)](https://www.securityweek.com/jpmorgan-visa-mastercard-cite-third-party-incidents-amid-data-leak/)

### [2026-11-20] The Container Store、週末のサイバー攻撃から復旧。n0n が 11 月上旬にリーク サイトへ掲載していた
- **何が起きたか**: 親会社の Neighborhood Intelligence (旧 Bed Bath & Beyond) は、The Container Store がウェブサイトとシステムを復旧したと発表した。約 100 の店舗は営業を続けたが、代わりの決済処理の手順を使っていた。顧客の決済情報が盗まれた形跡は今のところないとしたが、n0n の主張には触れていない。The Record によると、n0n は 9 月に現れ、100 を超える組織を攻撃し、当初は交渉の窓口に入るだけで身代金の 10% を払わせていたが、今は全額を払うまで盗んだデータの見本も見せないという。
- **なぜ重要か**: n0n はランサムウェアを使わない「データの恐喝」型で、委託先 (Qubole) と直接の標的の両方を攻撃している。Qubole の件と同じ集団であることを、インシデント対応の際には頭に置いておきたい。
- 出典: [The Record (2026-11-20)](https://therecord.media/container-store-restores-systems-cyberattack)

### [2026-11-20] [続報] アイルランドの信用組合の委託先 Wellington IT: 侵害は 6 週間気づかれず、40 を超える組合が当局に届け出た。モバイルバンキングの「振込先の情報」が対象
- **前回から変わったこと**: アイルランドのデータ保護委員会 (DPC) は、40 を超える信用組合から侵害の届け出を受けた。英国の ICO にも信用組合からの届け出が来始めており、英国の会員にも影響が及ぶ可能性がある。Robert Troy 閣外相は、対象は Wellington IT が運用するモバイルバンキングのアプリに会員が登録した振込先の情報だけで、アプリを使っていない会員は影響を受けないと説明した。The Record は、侵害が 6 週間気づかれなかったと報じた。Wellington IT の CEO は、当局や警察と協力していると述べた。
- 出典: [The Record (2026-11-20)](https://therecord.media/dozens-of-credit-unions-hit-by-supplier-breach)

### [2026-11-20] NSA の機密の通信網 NSANet が、PHP の更新の後に 3 日間不安定になり、ほぼ復旧。米国の国家サイバー長官 Cairncross 氏は退任
- **何が起きたか**: NSA は「通常の状態で運用している」と認めた。一部の施設は、不要不急の職員について「Code Orange」(出勤の遅延など) を続けている。国家情報長官の Jay Clayton 氏はテレビで、PHP の更新を当てたシステムが想定どおりに起動しなかったと説明した。政権は、サイバー攻撃ではなく、今週の Microsoft や航空、銀行の障害とも関係がないとしている。同じ日、ホワイトハウスは Sean Cairncross 国家サイバー長官の退任を認め、国防総省の CIO、Kirsten Davies 氏が代行に就いた。
- **なぜ重要か**: 重大な脆弱性の一斉の修正が、可用性の事故につながった例。11/19 の PHP の更新 (前号) は Critical が多く、各組織が急いで当てた。更新の前に、ステージングでの起動の確認と切り戻しの手順をそろえておくことの大切さが、情報機関の事例で示された。
- 出典: [The Record (2026-11-20)](https://therecord.media/nsa-resumes-normal-operations-following-internal-disruptions) / [The Record (2026-11-20)](https://therecord.media/sean-cairncross-out-as-national-cyber-director)

### [2026-11-20] Metasploit に Zimbra のモジュール: 他人のメールボックスになりすまして送信 (CVE-2026-73571)、GraphQL のログインでレート制限を回避 (CVE-2026-93637)
- **何が起きたか**: Rapid7 の研究「Breaking Zimbra Identity Boundaries, Part One」に基づき、Zimbra の SOAP 認証や ID の解決を共通化した mixin と、2 つのモジュールが加わった。CVE-2026-73571 は `SaveDraftRequest` の認可の回避で、普通の利用者が委任なしに他のローカルのメールボックスとしてメールを送れ、そのメッセージは被害者の送信済みフォルダに入る。CVE-2026-93637 は、Network Edition の GraphQL の認証エンドポイントで、SOAP のログインにある送信元 IP のロックアウトを回避して、パスワードリスト攻撃ができる。どちらも Zimbra 10.1.16 Network Edition で動作を確かめた。
- **なぜ重要か**: **Metasploit のモジュールとして PoC が公開された**。同じ認証を、別の入口 (GraphQL) が保護なしで受け付けるという欠陥の型は、REST と GraphQL を併設した他の製品でもよく見つかる。メールサーバーの診断では、すべてのログイン経路でロックアウトが効くかを確かめたい。
- 出典: [Rapid7 (2026-11-20)](https://www.rapid7.com/blog/post/pt-metasploit-wrap-up-breaking-zimbra-s-identity-boundaries)

### [2026-11-20] Google、Android の開発者の本人確認を 2027 年 1 月から世界中に広げる。最終的にはサイドロードを含む、すべてのインストール元が対象に
- **何が起きたか**: Google Play、Galaxy Store、Honor、OPPO、Xiaomi、Transsion、vivo の 7 つの配布元から始め、数か月かけてすべてのインストール元に広げる。本人確認をしていない開発者のアプリは、認定された Android 端末で通常のインストールができなくなる。ブラジル、インドネシア、シンガポール、タイでは 9/30 から始まっている。Google によると、登録済みのアプリが世界の Android のインストールの 99% 超を占める。上級者向けの「抜け道」も用意するという。
- **なぜ重要か**: Android のマルウェアの多くは、サイドロードで配られている (上の Bazuka もそう)。一方で、診断や研究で自作のアプリを入れる場合や、OSS のアプリの配布にも影響する。検証用の端末で、上級者向けの手順が使えるかを確かめておきたい。
- 出典: [Help Net Security (2026-11-20)](https://www.helpnetsecurity.com/2026/11/20/android-developer-verification-power-users/) / [Ars Technica (2026-11-20)](https://arstechnica.com/gadgets/2026/11/google-will-launch-android-app-verification-requirement-globally-in-january-2027/)

### [2026-11-19] 英国の裁判所の判断で、英政府が Apple に iCloud の暗号化データへのアクセスを求める秘密命令 (技術的能力通知) を出していたことが正式に確認された
- **何が起きたか**: 11/19 に公開された判決 (Apple と Privacy International ほか) で、裁判所は、命令の存在を公表しても国家安全保障に害はないと判断した。英政府は、2016 年捜査権限法に基づく技術的能力通知 (TCN) について、出したかどうかを肯定も否定もしない姿勢を続けていた。Apple は 2025 年 2 月から英国で「高度なデータ保護」の新規提供を止めている。報道では、英国の利用者に絞った命令が 2025 年 9 月に出され、Apple は 2026 年 7 月に再び異議を申し立てていた。
- **なぜ重要か**: 「E2E 暗号化にバックドアを求める命令」の存在が、司法の場で公式の事実になった。暗号化の設計に、法域ごとの法的な圧力という前提が加わる。英国向けにサービスを出す国内企業も、同じ種類の通知を受けうる。
- 出典: [GIGAZINE (2026-11-20)](https://gigazine.net/news/20261120-uk-government-apple-secret-encryption-order/)

### [2026-11-20] Blackpoint: ClickFix の配信サービス「ROMULUS」が、新しい RAT「CNCMachineRMS」と Legion Loader を別々の経路で配る。ChatGPT の Custom GPT も誘導に使う
- **何が起きたか**: ROMULUS は 10 月に Forescout が報告した配信サービス。Blackpoint によると、PowerShell から `msiexec` で MSI (「IconEdit2Turb.msi」、Stardock の正規ツールを装う) を入れ、DLL のサイドローディングで CNCMachineRMS を起動する。RAT は、遠隔のデスクトップ操作、画面の配信、マイクとカメラの収録、ファイル操作を持ち、通信は DNS over HTTPS (DoH) を使う。Custom GPT から ClickFix のサイトへ誘導する例もある。
- **なぜ重要か**: ChatGPT の公式の画面から悪性サイトに誘導されると、利用者は警戒しにくい。DoH の C2 は、DNS のログでは見えない。プロキシで DoH のリゾルバ (`dns.google`、`cloudflare-dns.com` など) への通信を許可する端末を絞れているかを確かめたい。
- 出典: [The Hacker News (2026-11-20)](https://thehackernews.com/2026/11/romulus-clickfix-attacks-deliver-rat.html)

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-11-19 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先 (OSV の 8 エコシステムで 11/19〜21 に公開された High / Critical から、前号までの重複を除いて選択)

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-132825 / GHSA-34m4-m9fh-gqp5 [続報] | CRuby 2.4.0〜3.3.13 / 3.4.0〜3.4.12 / 4.0.0〜4.0.9 | CWE-193・122 / 7.4 (Ruby: Critical) | multipart のパートの `charset` で 1 バイト文字コードを宣言 → `Rack::MethodOverride` が `_method` を `upcase` → `ß`×21 で 1 バイトのヒープ書き込み → RCE (PoC 11/25 予定) | [d582f8f](https://github.com/ruby/ruby/commit/d582f8f13d700d8e39714d3a8f11eb4bd2bc69f0) | 既定の Rails で認証前 / PoC 予告 / EPSS 0.0019 |
| CVE-2026-130001 / GHSA-5hrj-7fc3-cmx9 | mustache (Ruby gem) 1.1.2 以前 | CWE-913 / 9.8 | 「ロジックのないテンプレート」が、攻撃者のテンプレートから組み込みのメソッドを呼べた → SSTI で任意コード実行 (詳細と PoC は後日) | [b015f86](https://github.com/mustache/mustache/commit/b015f866942a6eb45ce4d34009f2ba6ff16ce4c1) | Critical / 他言語の Mustache 実装へ水平展開候補 |
| CVE-2026-63345 / 63346 / 63344 | Refitter (.NET) 2.1.2 未満 | CWE-94・116 / Critical | OpenAPI の path / ヘッダ名 / content-type をそのまま `[Get("<path>")]` などの属性文字列に出力 → `"` で抜けて `[ModuleInitializer]` を注入 → 生成したアセンブリを読み込んだ時点でコード実行 | [PR #1178](https://github.com/christianhelle/refitter/pull/1178) | Critical / 生成系の同型 (下 2 行) |
| CVE-2026-76090 / GHSA-gpcc-36pq-8qxr | tapir-openapi-codegen-core (Scala) 1.13.27 未満 | CWE-94 / High | OpenAPI のプロパティ名・パラメータ名・タグを文字列テンプレートで Scala に埋め込む → コンパイル時 / エンドポイント組み立て時の任意コード実行 | [PR #5395](https://github.com/softwaremill/tapir/pull/5395) | 同型 (OpenAPI codegen) |
| CVE-2026-63415 / GHSA-c3cj-3p6p-j822 | jane-php/open-api-3 7.12.0 未満 | CWE-918・22・98 / High | 外部の `$ref` を生成時に `file_get_contents($ref)` でスキームや経路の制限なく解決 → SSRF / ローカルファイルを生成コードに取り込む | [PR #961](https://github.com/janephp/janephp/pull/961) | 同型 (同 Jane の RCE 3 件は前号まで既報) |
| CVE-2026-61689 / GHSA-jmmc-wjpc-pg34 | XWiki Platform rest-server 4.3-m1〜16.10.18 未満 | CWE-943 / CVSS4 High | クエリの REST API の HQL に FROM 句を注入し、SELECT 列の許可リストを回避 → ブラインドで DB の任意の値 (パスワードのハッシュ、設定内のパスワード) を約 800 リクエストで取得 | [4d6a2cd](https://github.com/xwiki/xwiki-platform/commit/4d6a2cd9cd049d0c31823ce47bff0a95667967e3) | 未認証 |
| CVE-2026-114516 / GHSA-mc8w-wjhw-45x5 | Etherpad (ep_etherpad-lite) 1.8.14〜3.3.3 未満 | CWE-22・306 / 9.8 | 認証のミドルウェアより前に置かれた `/static/*` に `..%5C` (バックスラッシュのエンコード) → 任意のファイルの読み取り → `settings.json` などから管理者のパスワード | [PR #8081](https://github.com/ether/etherpad/pull/8081) | 未認証 / EPSS 0.0149 |
| CVE-2026-77367 / GHSA-hq2p-f2vj-v3cm | Daptin (Go) 0.12.30 未満 | CWE-89 / 9.4 | すべてのエンティティの一覧 API の `sort` パラメータを、列の存在を確かめずに SQL の識別子に連結 → 未認証の SQLi (隣のコードには前回の修正が入っていた = 修正の取りこぼし) | [b0bcc13](https://github.com/daptin/daptin/commit/b0bcc1318832b9055781f032853ef9d2264652cf) | 未認証 / 不完全修正 |
| CVE-2026-104099 / GHSA-4hrh-34w3-5ww8 | fabio (Go のロードバランサ) 1.7.3 未満 | CWE-863・41 / 9.1 | ルートの選択に正規化前のパスを使い、ACL と Basic 認証をルートに付けていた → `/./`・`%2e`・`//` の変種で別のルートを選ばせて門を素通り → バックエンドが正規化して保護された資源を返す | [f00ce1a](https://github.com/fabiolb/fabio/commit/f00ce1a446a4b7a3bccbefbb7bfe4a5e0e3fd817) | 未認証 / Traefik CVE-2023-47106 と同型 |
| CVE-2026-103026 / GHSA-prhx-9q2h-ph2x | Paymenter (Laravel Livewire) 1.5.7 未満 | CWE-470・915 / 8.1 | 共通の基底コンポーネントの `executeConfirmedAction($action, $params)` が `method_exists` だけで任意の public メソッドを呼ぶ → ロックされたプロパティの上書きなど | [e0c04af](https://github.com/Paymenter/Paymenter/commit/e0c04af1707a65d8fb91879883aa7eae3292cedc) | Livewire アプリへ水平展開候補 |
| CVE-2026-76807 / 77359 / 130007 | @doist/todoist-mcp 10.3.3 未満 / jupyter-mcp-server 1.0.3 未満 / k8s-mcp-server 1.1.0 未満 | CWE-350・306 / Critical・High | ローカルの MCP の HTTP サーバーが `Host` / `Origin` を確かめない (jupyter は `/mcp` 以外の管理ルートだけ漏れ) → DNS リバインディングで悪意あるサイトからツールを実行 / k8s は既定で 0.0.0.0:8080 に認証なしで待ち受け | [PR #516](https://github.com/todoist/todoist-mcp/pull/516) / [PR #262](https://github.com/datalayer/jupyter-mcp-server/pull/262) / [PR #134](https://github.com/reza-gholizade/k8s-mcp-server/pull/134) | MCP の同型多発 |
| CVE-2026-69157 / GHSA-pfwx-xjp4-qxcj | atomic-server (Rust) 0.29.0〜0.40.1 | CWE-306 / 9.8 | 起動時に作る `/setup` の招待が redeemer の ID を見ない → `GET /setup?public-key=<攻撃者の鍵>` で Drive 全体の書き込み権 → 未設定のインスタンスを乗っ取り | [98517d8](https://github.com/ontola/atomic-server/commit/98517d8921c78bd9b728a2459378c184ebf8a969) | 未認証 / 初期設定 URL の型 |
| CVE-2026-62955 / GHSA-2pj4-v76f-wjvx | baserCMS (baser-core) 5.3.0 未満 | CWE-22 / 7.2 | CVE-2026-30940 の修正の `realpath()` チェックが、対象のディレクトリが存在せず `false` を返すと丸ごとスキップ → テーマのファイル操作でパストラバーサル (管理者権限が必要) | [464227b](https://github.com/baserproject/basercms/commit/464227b8770704076ee6eddd4bd464c184786eca) | 国内 OSS / 修正のバイパス |
| CVE-2026-99312 | Linux KVM (AMD・入れ子の仮想化が有効) | — / 8.8 (Red Hat 5.6) | AMD 向けの入れ子の仮想化の処理の欠陥 → ゲストの root からホストのメモリを読み書き (127GB の読み取り、32 バイトの書き込みを実証) | [THN の記事](https://thehackernews.com/2026/11/new-linux-kvm-flaw-cve-2026-99312-lets.html) (commit 不明。11/2 にマージ) | クラウド / PoC 非公開 |
| CVE-2026-114202 | ASUS Control Center Express 1.7.29 未満 | CWE-321 / 10.0 | 製品にハードコードされた暗号鍵 → 未認証で管理者の認証トークンを偽造 → 管理下の PC 群を掌握 | [BleepingComputer](https://www.bleepingcomputer.com/news/security/asus-warns-of-critical-hard-coded-key-flaw-in-control-center-express/) (commit 不明、クローズドソース) | EPSS 0.0038 |

**今日の CVE 所感**
- **OpenAPI のコード生成器への「仕様書インジェクション」が 3 実装 (C# の Refitter、Scala の Tapir、PHP の Jane) で同時に出た**。根っこは同じで、仕様書の名前・説明・パス・`$ref` を、文字列のテンプレートで生成コードに埋め込んでいる。同じ仕様を独立に実装したもの (openapi-generator の各言語のテンプレート、oapi-codegen、NSwag、Kiota、orval、openapi-typescript) は、**path のキー・パラメータ名・`description` (コメントの `*/` 抜け)・`enum` の値・`$ref`** の 5 か所を、そのまま並べて確かめる価値がある。CI が外部の API 仕様書を取ってきて生成するパイプラインは、ビルド環境での RCE になる。
- **ローカルの MCP サーバーへの DNS リバインディング**が今週も 3 件出た。「`/mcp` は守ったが、同じアプリに載せた管理ルートは漏れた」(jupyter-mcp-server) という形は、他の実装でも起きやすい。ローカルの MCP を診断するなら、すべてのルートで `Host` が `localhost` / `127.0.0.1` 以外を拒むかを確かめる。
- **修正の取りこぼし・バイパス**が目立つ (Daptin の隣のコード、baserCMS の `realpath()` が `false` のとき、Ruby の 10/23 の版が影響を受ける最新版)。パッチの diff を読むときは、「同じファイルの似た経路」と「チェックの関数が失敗の値を返したときの分岐」を必ず見る。
- 診断で優先したいのは、Etherpad (未認証の任意のファイルの読み取り、バックスラッシュのエンコード) と fabio (パスの正規化の差)。どちらも、リバースプロキシとバックエンドの間で解釈がずれる古典的な型で、自動スキャナの既存のペイロードで当たる可能性が高い。

## 日本国内のセキュリティ動向

### 国内インシデント・事故

### [2026-11-20] デジタル庁、政府共通の基盤 GSS のファイル共有サービスで、7/30〜11/12 に正規の相手以外からファイルへのアクセスがあり、ファイルが漏えいした可能性があると公表
- **何が起きたか**: GSS (ガバメントソリューションサービス) は、デジタル庁、総務省、経済産業省、法務省、金融庁、原子力規制委員会など 25 の政府機関、約 15 万人が使う共通の業務環境。ファイル共有サービスは、会議資料などの大きなファイルを、組織の外 (自治体や企業) とやり取りするのに使われ、民間のクラウドサービスを使っている。デジタル庁は 11/12 に正規の共有相手以外からのアクセスを検知し、外部との通信を遮断してサービスを止めた。調査で 7/30〜11/12 のアクセスを確認し、アクセスは複数回あったとみられる。ファイルの件数と内容、機密性の高い文書が含まれるかは調べている最中で、個人情報が含まれることも想定されるという。同庁は「一般国民の個人情報が含まれる可能性は極めて低い」としている。外務省と防衛省は GSS を使っていない。GSS で扱えるのは、政府の 3 段階の機密性のうち「機密性 2」まで。
- **なぜ重要か**: アクセスは **3 か月半にわたり気づかれなかった**。GSS では 9 月にも個人情報の漏えいの可能性が公表されている。民間のクラウドのファイル共有で「正規の共有相手以外からのアクセス」が起きる典型は、共有リンクの漏れ、外部ユーザーのアカウントの乗っ取り、トークンの窃取。省庁と取引のある企業は、GSS のファイル共有でやり取りした資料の一覧を手元で作っておくと、後で通知が来たときに速く対応できる。
- 出典: [piyolog (2026-11-21)](https://piyolog.hatenadiary.jp/entry/2026/11/21/002438) / [INTERNET Watch (2026-11-20)](https://internet.watch.impress.co.jp/docs/news/2158375.html) / [ITmedia NEWS (2026-11-20)](https://www.itmedia.co.jp/news/article/2611/20/2000003381/)

### [2026-11-19] SBC メディカルグループ (湘南美容クリニックなどの経営支援、NASDAQ: SBC)、日本の子会社のウェブシステムの DB から 162 万 4,000 人分の顧客情報が盗まれたと米 SEC に届け出
- **何が起きたか**: SEC への 8-K によると、11/16、日本の子会社 SBC Medical Group が運営するウェブシステムの一部の DB に不正アクセスがあり、顧客情報が抜き出された。基本情報 (氏名、住所、電話番号、メールアドレス、生年月日、性別、診察券番号、会員 ID、アンケートの回答) が 1,624,000 人。ほかに、予約の申し込み 255,416 件、ウェブの問い合わせ 217,769 件、施術の内容と画像のファイル名 4,513 人、施術名と口コミ 15,007 人、クレジットカード 14 人分 (いずれも有効期限切れなどで使えない状態だったという)。顧客のパスワードと、従業員約 2 万件 (氏名、ID、パスワード) も盗まれ、従業員 459 人は口座、年金、源泉徴収票の情報も含まれる。別件で、56 のクリニックが使う予約サービス Tribeau の管理者アカウントが不正に使われ、約 1 万 9,000 人の情報にアクセスされた。電子カルテと予約サイト mySBC への不正アクセスは確認していないとしている。
- **なぜ重要か**: 美容医療の施術の内容と顧客の画像ファイル名は、通常の個人情報より機微で、恐喝や詐欺の材料になりやすい。顧客のパスワードも盗まれており、同じパスワードを使い回している人は他のサービスでも狙われる。国内の発表より先に米 SEC の届出で数字が出たのは、米国上場の日本の事業会社ならではの流れ。
- 出典: [BleepingComputer (2026-11-19)](https://www.bleepingcomputer.com/news/security/hackers-steal-data-of-16-million-sbc-medical-group-customers/) / [SecurityWeek (2026-11-20)](https://www.securityweek.com/sbc-medical-group-data-breach-impacts-over-2-million/)

### [2026-11-20] [続報] プレイド、KARTE の不正アクセスの調査結果を公表。再開の目標は 2027 年 1 月中旬で、契約を終えた企業の情報も漏えいの対象に含まれていた
- **前回から変わったこと**: プレイドは、企業から預かった情報のうち、漏えいした (またはそのおそれがある) ものを 4 つに分け、対象の社数を示した。11/24 から対象企業に詳細なデータを渡す。キャッシュのデータは短時間で上書きされ、読み出されたものを特定できないので、不正アクセスの時間帯に保存されていた可能性のあるデータを「漏えいのおそれ」として扱う。11/16 の発表では対象を「利用企業」としていたが、**契約の全部か一部が終わった企業の情報も含まれていた**と訂正した。契約終了後に消すべき情報が、運用と管理の不備で残っていたという。自社が持つ情報では、11/16 に公表したメールアドレス 7 万 9,249 件に加え、営業やサポートで集めた氏名やメールアドレスなど 4 万 5,816 件が漏えいした。侵入経路をふさぐだけでなく構造の改善が必要と判断し、第三者の検証も受けたうえで、2027 年 1 月中旬の段階的な再開を目指す。
- 出典: [INTERNET Watch (2026-11-20)](https://internet.watch.impress.co.jp/docs/news/2158284.html)

### [2026-11-19] [続報] 北海道の委託先のマルウェア感染: 留萌市も公表。住民基本台帳のデータ最大 7 万 1,002 件と、避難行動要支援者 (障害の区分や要介護度を含む) 最大 4,503 件。契約が終わった後もデータが残っていた
- **前回から変わったこと**: 前号の岩見沢市・新得町に、留萌市が加わった。データは GIS 北海道の協力会社、有限会社リムゲートの端末に保存されており、端末は 11/2 夜〜3 日に情報窃取型のマルウェア「K2F (k2f_chan)」に感染した。留萌市の要支援者のデータには、障害の区分 (身体・知的・精神)、要介護度、情報提供の同意の有無が含まれる。留萌市と GIS 北海道の契約は 2022 年 3 月末で終わり、終了後は消す取り決めだったが、データは残っていた。留萌市は、協力会社へのデータの共有について GIS 北海道から報告を受けておらず、把握していなかったという。GIS 北海道は、他の自治体への影響を「現時点で公表できない」としている。NIKKE の PC ランチャーとの関係は、ITmedia の取材に GIS 北海道が認めた (前号)。
- **なぜ重要か (評価)**: 上の KARTE の件と同じく、**「契約が終わった後に消すはずのデータが残っていた」ことで被害が広がった**。委託先の監査では、再委託先の把握と、契約終了時のデータ消去の証跡 (消去証明) を確認項目に入れておきたい。
- 出典: [piyolog (2026-11-20)](https://piyolog.hatenadiary.jp/entry/2026/11/20/130214)

> 補足: ScanNetSecurity の 11/19〜20 掲載分 (ユミルリンク、アンドエスティ HD、チームスピリット、資生堂、JNSA、SMBC 日興証券、ソニー少額短期保険、日本商工会議所、Joshin、Studio / GMO Flatt Security など) と、Security NEXT の 11/20〜21 掲載分 (早稲田大学、ソフト 99、Gunosy、ヤマダデンキのリフォーム管理システム) は、組織の公表日が 11/18 以前 (10/26〜11/12) のため、採用範囲外として扱った。

### 国内の注意喚起・ガイドライン・政策

### [2026-11-20] IPA「PHP の脆弱性対策について (2026 年 11 月)」/ JPCERT/CC の PHP の注意喚起 (CVE-2026-109618、CVE-2026-109619) を更新
- **何が起きたか**: IPA は、10/21 の事前の準備のお願いの続報として、11/19 に公開された PHP 8.2.36 / 8.3.37 / 8.4.28 / 8.5.13 への更新を呼びかけた。事前の予告で Critical は「既定と違う設定や一般的でない構成が影響の条件」とされていたが、**それだけで、すべての脆弱性が既定の設定なら影響しないと判断しないよう**求めている。PHP を組み込んだ製品やネットワーク機器、ホスティングサービスについては、提供元の情報を確かめること、更新できない場合はアクセスの制限、機能の制限、公開の停止まで検討することも挙げた。JPCERT/CC は注意喚起 (at260033) を 11/20 に更新した。
- **なぜ重要か (評価)**: 上の NSA の件のように、急いで当てた更新で起動しなくなる例も出ている。IPA が「長期間更新していないシステムでは改修と動作確認が必要」と書いているのは、そのまま実務の注意点になる。組み込みの PHP (NAS、ルーター、複合機の管理画面) は、ベンダーの対応表を待つしかない。
- 出典: [IPA (2026-11-20)](https://www.ipa.go.jp/security/security-alert/2026/alert20261120.html) / [JPCERT/CC 注意喚起 at260033 (2026-11-20 更新)](https://www.jpcert.or.jp/at/2026/at260033.html)

### [2026-11-20] 「警察のサイトで逮捕状を確認して」は詐欺。警視庁・警察庁・静岡県警・兵庫県警を装った偽サイトに、偽の「オンライン相談」や「逮捕状の検索」の機能
- **何が起きたか**: INTERNET Watch の連載が、警察を装う詐欺の手口をまとめた。警視庁を装う偽サイトは 7 月〜9 月上旬に 9 件見つかり、トップの「行政手続オンライン」を押すと、本物にはない「オンライン相談」のページからビデオ通話の「取り調べ」に誘導する。静岡県警の偽サイトには、氏名や口座を入力させ、指示された番号を入れると偽の逮捕状を表示する仕組みがあった。警視庁と静岡県警の偽サイトを使った詐欺では、現金と暗号資産で約 850 万円がだまし取られた。警察庁によると、「ニセ警察詐欺」は 2026 年上半期だけで 4,466 件、被害額は 507 億 9,000 万円。
- **なぜ重要か (評価)**: 偽サイトが見た目を真似るだけでなく、詐欺の台本に合わせた機能 (検索して偽の書類を出す) を持つようになった。テイクダウンの依頼や、組織のブランドの監視 (類似ドメインの検知) の対象に、公的機関の偽装サイトの「機能」も含めて見る必要がある。
- 出典: [INTERNET Watch (2026-11-20)](https://internet.watch.impress.co.jp/docs/column/dlis/2157108.html)

> 直近 2 日間で、NISC (国家サイバー統括室)・警察庁・総務省・経産省・金融庁・個人情報保護委員会から、上記以外の新しい発表は確認できなかった (11/19 の JPCERT/CC の NGINX と Node-RED の CyberNewsFlash は前号で既報)。

### 国内製品の脆弱性 (JVN)

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| 2026-11-20 | JVN#64740097 | ソフトバンク Airターミナル6 | 有線か Wi-Fi で機器につながる利用者が、OS コマンドインジェクション (CWE-78) で root として任意のコマンドを実行できる。修正済みのファームウェアは自動で適用され、利用者の対応は不要 | CVSS 4.0: 8.7 / 3.0: 8.8 (AV:A) | [JVN](https://jvn.jp/jp/JVN64740097/) |
| 2026-11-20 | GHSA-2pj4-v76f-wjvx / CVE-2026-62955 | baserCMS (baser-core) 5.3.0 未満 | CVE-2026-30940 の修正の `realpath()` チェックを、存在しないディレクトリの指定で回避するパストラバーサル (管理者権限が必要) | 7.2 | [GHSA](https://github.com/baserproject/basercms/security/advisories/GHSA-2pj4-v76f-wjvx) |
| 2026-11-20 | JVNVU#92814490 | CISA ICS Advisory (11/19 分、新規 3 件。Autonomy Logic OpenPLC Runtime ほか) | 米 CISA の ICS / 医療機器の勧告の転載。国内の工場や研究室で使われる OpenPLC を含む | 各勧告を参照 | [JVN](https://jvn.jp/vu/JVNVU92814490/) |
| 2026-11-19〜20 | JVNDB-2026-044223〜044393 ほか | Google Chrome、Microsoft、IBM API Connect、OpenJDK ほか | JVN iPedia に、海外製品の 11 月の修正分 (Chrome 158、11 月の Patch Tuesday ほか) がまとめて登録された | 各エントリ | [JVN iPedia 新着](https://jvndb.jvn.jp/) |

> 補足: 直近 2 日間に新しく出た国内ベンダー独自の JVN# は、Airターミナル6 の 1 件だった。Siemens の 11 月の更新、Win Bird 授業支援、Ruijie Networks は前号で既報。ScanNetSecurity の「エレコム製無線 LAN ルーターの OS コマンドインジェクション」「宮内庁参観音声ガイド」は、11/17〜18 の JVN の公表で既報。

### 国内コミュニティ・研究・イベント

### [2026-11-20] LAC WATCH「Claude Code を安全に使う五つのガードレール (導入編)」: 納期のある受託開発の実案件で、協力会社を含めて使うときのリスクの棚卸しと対策
- **何が起きたか**: ラックの開発チームは、Claude の Team プランで、各メンバーが自分の端末で CLI 版の Claude Code を使う体制を作った。最初に手をつけたのは速くなるかの検証ではなく、リスクの棚卸しだったという。学習に使われないことと、情報が開発環境の外に出ないことは別だとし、(1) リポジトリの設定ファイルや手順書に残る DB の接続情報・API キー・証明書をエージェントが自分で探して読むこと、(2) トラブル対応で本番のデータやログ、社内チャットをプロンプトに貼ること、(3) 権限設定が甘いことによる情報の流出やファイルの変更・削除、(4) 生成したコードが GPL などのコードと酷似する著作権のリスク、の 4 点を挙げた。人の確認に頼らず、設定と仕組みで抑える方針で、運用改善編と効果測定編が続く。
- **なぜ重要か (評価)**: 国内のセキュリティ企業が、AI のコーディングエージェントの実案件への導入を、リスクの一覧と対策の組み合わせとして公開した。顧客から「AI エージェントを使った開発の体制」を診断・監査してほしいと頼まれたときのチェックリストの下敷きに使える。
- 出典: [LAC WATCH (2026-11-20)](https://www.lac.co.jp/lacwatch/people/20261120_005020.html)

### [2026-11-20] ScanNetSecurity: NTT ドコモビジネスの「サブドメインテイクオーバー」の講演レポート。社内の CNAME の片付けを説得するには、実際に乗っ取ってみせるのが一番
- **何が起きたか**: Internet Week 2025 の DNSDAY での、NTT ドコモビジネスの髙田美紀氏と竹﨑彬隼氏の講演のレポート。省庁のサイトの典型的な作り方 (入札で制作会社に発注 → 制作会社がレンタルサーバーを契約 → 省庁の DNS に CNAME を登録) を例に、運用を終えた後に CNAME が残ると第三者がそのサブドメインを乗っ取れる仕組みを説明した。デジタル庁は 2025 年 5 月にドメイン管理のガイドラインを改定し、廃止時に DNS レコードを消すよう明記している。現場では「忙しくて忘れていた」「委託先に任せていた」という声が返ってくるので、社内だからこそ実際にテイクオーバーを試し、証拠を持って「一緒に直しましょう」と持ちかけるのが決め手だという。Internet Week 2026 は 11/19 に始まった。
- **なぜ重要か (評価)**: 外部の攻撃面の診断 (ASM) で、ぶら下がった CNAME は今も上位の発見になる。「実際に乗っ取って見せる」は、社内のレッドチームの説得の型としても使える。
- 出典: [ScanNetSecurity (2026-11-20)](https://scan.netsecurity.ne.jp/article/2026/11/20/56866.html)

### [2026-11-20〜21] 国内の研究者・まとめ: piyolog が Ruby2Shell、GSS、北海道の 3 市町の件を一次情報つきでまとめた
- **何が起きたか**: piyolog は、Ruby2Shell について、影響を受ける 14 の文字コード、届くメソッドと届かないメソッド、Rack の経路、ディストリビューションと同梱製品ごとの対応状況 (Ubuntu の修正版の版番号、Debian と RHEL の修正待ち、Amazon Linux の Pending Fix など) を出典つきで整理した。GSS の件と北海道の 3 市町の件も、報道と自治体の公表を突き合わせてまとめている。
- **なぜ重要か (評価)**: Ruby2Shell の「どの OS のパッケージがいつ直るか」は英語の記事にもまとまっておらず、国内の運用者が最初に見る資料としてもっとも使いやすい。深掘りの「今日できること」と合わせて使いたい。
- 出典: [piyolog: Ruby2Shell (2026-11-20)](https://piyolog.hatenadiary.jp/entry/2026/11/20/224814)

<!-- bounty:start -->
## バグバウンティ・実践

> 実際の脆弱性報告・ライトアップから、次の診断で試せる学びを日本語で解説する欄。公開から 7 日以内のものが対象 (採用範囲の 2 日間とは別)。定期タスク「KEDA Daily Digest ページ更新」が、ページ版と同じ内容をここに追記している。

### [2026-11-20] Zimbra: 下書き保存の SOAP に「代理送信」の印を付けるだけで他人として送信でき、GraphQL 側のログインは失敗回数に数えられない
- **種類**: 認可不備 / なりすまし送信 / レート制限回避
- **対象**: メールサーバー Zimbra Collaboration の Network Edition (検証は 10.1.16)。Rapid7 の Jonah Burgess 氏の研究記事 (10/14 公開) をもとに、11/20 に Metasploit のモジュール 2 本が加わった。他人として送信できる CVE-2026-73571 は Rapid7 の評価で CVSS 4.0 の 8.3 (High)、10.1.17 で修正済み。ログインの制限を回避できる CVE-2026-93637 は CVSS 3.1 の 3.7 (Low) で、研究記事の表には修正版が載っていない。報奨金の記載はない。
- **手口の肝**: **1 件目**: 下書きを保存する SOAP の `SaveDraftRequest` に、代理送信を示す属性 `isDelegatedReq` を付け、From に同じサーバー上の別の利用者のアドレスを書く。サーバーは From のアドレスを名前でアカウントに引き当て、その人のメールボックスとして通常の送信処理を呼ぶ。**引き当てから送信までの間に、「呼び出した本人に send-as / 代理送信の権限があるか」を確かめる処理が無かった**。アカウントの UUID を渡す `delegateeAccountId` でも同じことが起きる。**2 件目**: SOAP のログインは、失敗すると `SoapEngine` がリクエストに `auth.failed` の印を付け、`ZimbraInvalidLoginFilter` が送信元 IP ごとに数える (既定では 10 回を超えると 503)。ところが `/service/extension/graphql` の `authenticate` は、内部でログインの処理を直接呼ぶので印が付かず、失敗が 1 回も数えられない。同じ認証に入口が 2 つあり、片方だけ見張りを通っていなかった。
- **影響の広げ方**: なりすましたメールは正規の送信経路を通るので、その組織の SPF / DKIM / DMARC が通る構成なら偽のメールも通り、控えは被害者の送信済みフォルダに入る。前提は「普通の利用者としてログインできること」と「相手が同じメールボックスサーバーにいること」だけで、委任や管理者権限、相手の操作は要らない。GraphQL の方は、エイリアスを使って 1 つのリクエストにログインの試行を 100 個並べられ、記事では 1 万件の候補を 2 分足らずで試しても IP は止められなかった。アカウント単位のロックアウトは既定で無効だが、有効にしてあれば GraphQL 経由の失敗も数えられる。MFA は回避できない。
- **自分の診断で試すこと**:
  - 「代理」「委任」「on behalf of」を表すフラグや ID を受け取る API を探す。権限を持たないアカウントでそのフラグを立て、送信者・所有者・作成者の欄に他人を指定する。エラーにならず、他人の名義で処理された (相手の送信済みや履歴に残る) なら当たり。必ず検証用のアカウント同士で行う
  - ログインの入口をすべて洗い出す (フォーム、SOAP / REST、GraphQL、モバイル用、旧 API)。1 つの入口でロックアウトや 503 が出るまで失敗させたあと、同じ送信元から別の入口で失敗を続ける。別の入口だけ制限がかからなければ当たり
  - GraphQL では、エイリアスで同じミューテーションを 1 リクエストに複数並べ、結果が個別に返るかを見る。返るなら「リクエスト数」で数えるレート制限は効いていない
- 出典: [Rapid7 (Metasploit Wrap-Up)](https://www.rapid7.com/blog/post/pt-metasploit-wrap-up-breaking-zimbra-s-identity-boundaries/) / [Rapid7 (Jonah Burgess)](https://www.rapid7.com/blog/post/ve-breaking-zimbra-identity-boundaries-part-1/)

### [2026-10-27] Etherpad: `/static/` のパスに `%5C` (バックスラッシュ) を混ぜると、検査のあとで `../` に化け、ログインなしで任意のファイルを読める
- **種類**: Path Traversal / 認証前 / 検査と変換の順序
- **対象**: 共同編集エディタ Etherpad (npm の `etherpad-lite` 1.8.14〜3.3.2、修正は 3.3.3)。CVE-2026-114516、CVSS 9.8 (Critical)。報告者は gcm-explo1t 氏。GitHub のアドバイザリの日付は 10/27 で、脆弱性データベースには今週載った (日報の CVE 表に今週の新着として収録)。報奨金の記載はない。
- **手口の肝**: 入口はプラグインの静的ファイルを返す `/static/*`。このルートはセッションやアクセス確認のミドルウェアより前 (`expressPreSession`) に登録されているので、ログインは要らない。パスの検査をする `sanitizePathname.ts` は、Linux などではバックスラッシュを「ただの文字」として残す。そのため `..` をバックスラッシュでつないだ並びは、上の階層へ戻る指定とは見なされずに通る。ところがそのあとの `Minify.ts` が、OS に関係なくバックスラッシュをスラッシュに置き換えていた。**検査が済んだ文字列を、あとから `../` に変えてしまう順序の誤り**が原因。修正は、この置き換えを Windows のとき (`path.sep === '\\'`) だけに限る 1 行。
- **影響の広げ方**: Etherpad のプロセスが読めるファイルなら何でも読める。修正の PR は例として `settings.json`、`credentials.json`、`/proc/self/environ` を挙げ、そこから管理者のセッションを取り、プラグインのインストール機能でコード実行まで進めるとしている。エンコードされたバックスラッシュはリバースプロキシがそのまま通すので、前段にプロキシを置いても防げない。
- **自分の診断で試すこと**:
  - Etherpad を見つけたら版を確かめ、`/static/plugins/` の下に `..%5C` を重ねたパスを、クライアントに正規化させずに (curl なら `--path-as-is`) 送る。200 で対象のファイルの中身が返れば当たり、修正済みなら 404
  - ほかの製品でも、`../` や `..%2f` が弾かれたところで止めずに `..%5C` を試す。ソースを見られるなら、パスの検査の「あと」に置換やデコード (`replace` でバックスラッシュを変える処理、`decodeURIComponent` など) が残っていないかを grep する
  - 静的ファイルの配信、ヘルスチェック、プラグインの資産など、認証のミドルウェアより前に登録されているルートを一覧にし、ファイルのパスを受け取るものを優先して調べる
- 出典: [GitHub Advisory GHSA-mc8w-wjhw-45x5 (ether/etherpad)](https://github.com/ether/etherpad/security/advisories/GHSA-mc8w-wjhw-45x5) / [修正の PR #8081](https://github.com/ether/etherpad/pull/8081)

### そのほかのライトアップ

- **[2026-08-09] ロードバランサ fabio: `/./admin/` や `//admin/` で保護付きのルートを外し、認証のない別のルートから同じバックエンドに届く** (認可回避 / 正規化の不一致): fabio (1.7.3 で修正、CVE-2026-104099、CVSS 9.1) は、正規化していない生のパスでルートを選び、選ばれたルートの IP 制限や Basic 認証だけを適用していた。保護付きの `/admin` とは別に、同じバックエンドへ流す広いルート (`/` など) があると、`/./admin/`、`/%2e/admin/`、`//admin/` は広い方に一致して素通りし、バックエンドが正規化して保護された中身を返す。報告者は `curl --path-as-is` で、401 / 403 だったものが 200 に変わることを確かめている。アドバイザリの日付は 8/9 (日報は今週の新着として収録)。前日の Fastify の件と同じ「2 つの層でパスの解釈がずれる」型。 出典: [GitHub Advisory GHSA-4hrh-34w3-5ww8 (fabiolb/fabio)](https://github.com/fabiolb/fabio/security/advisories/GHSA-4hrh-34w3-5ww8)
- **[2026-11-20] コーディングエージェントの「読み取り専用」は何を止めるのか: Codex と Claude Code で 7 つの操作を実測** (AI エージェント / 権限設定): 著者が自分の Ubuntu 24.04 の VM で、作業フォルダの内外の読み取り、編集、シェルでのファイル作成、Python の実行、ローカルへの HTTP など 7 つの操作を試した記録。この環境では、Codex の `-s read-only` は読み取りと Python の実行を通し、編集は承認待ちになり、シェルでの新規作成と `/tmp` への書き込みは OS の層で止まった。Claude Code で許可を `Read` だけにすると Bash と Python は承認待ちで止まり、Bash を許可すると 7 つすべてが通ってローカルの HTTP にも届いた。**試した 1 つのパスでは、どの条件でも作業フォルダの外のファイルを読めた**。各条件は原則 1 回だけの測定で、Claude のサンドボックスは起動に失敗して測れていないと著者が明記している。 出典: [Zenn (coastlinedb)](https://zenn.dev/coastlinedb/articles/8fdd1338ca65cb)
- **[2026-11-20] 認証基盤を入れても API から情報は抜ける: ログイン不要の会員番号 API を順にたどると全件を取れることを、手元の模擬サーバーで実演** (IDOR / 過剰なレスポンス): 実際の脆弱性の報告ではなく、解説と自作の模擬サーバー (架空の会員 4,000 人、Node.js) での実演。OAuth・NextAuth・Supabase・Cloudflare を入れても「そのデータを見てよい相手か」の確認 (認可) は作る側に残る、という整理。ログイン不要の会員番号の API を 1 から順に呼ぶと 4,000 件を 322 ミリ秒で取れ、毎秒 20 回の制限を付けても、429 のあと待って再試行すれば 420 万件を約 52 時間で取れると試算している。著者は診断ツールの会社 (エーアイセキュリティラボ) の所属なので、観点の整理として読む。 出典: [Zenn (a.haruki)](https://zenn.dev/aeyesec/articles/d17f8a333b79c3)

<!-- bounty:end -->

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 110 (RSS / Atom 48 本 [JVN / JVN iPedia / JPCERT/CC / IPA / piyolog / Security NEXT / ScanNetSecurity / ITmedia 2 本 / INTERNET Watch / Publickey / GIGAZINE / LAC WATCH / BleepingComputer / THN / SecurityWeek / Help Net / The Record / Dark Reading / Ars / Krebs / Talos / Unit 42 / GTIG / MSRC / Microsoft Security / watchTowr / ZDI / Trail of Bits / Project Zero / PortSwigger / Rapid7 / SentinelLabs / ESET / GitLab / GitHub Security / OpenAI / Google / DeepMind / Hugging Face / TechCrunch / The Verge / Simon Willison / Embrace The Red ほか]、個別記事の本文 約 60 本、CISA KEV JSON、OSV の 8 エコシステム (modified 509 行 → GHSA 161 件を個別取得)、FIRST EPSS API、WebSearch 7 回)
- 採用件数: AI技術=12 / AIセキュリティ=8 / セキュリティ=14 (深掘り 1 件は別) / CVE=15 行 (同系統をまとめて計 21 CVE) / 国内インシデント=4 (うち続報 2) / 国内政策=2 / JVN=4 行 / 国内コミュニティ=3
- 除外理由内訳: 古すぎ=約 25 (ScanNetSecurity の 11/19〜20 掲載で組織の公表が 10/26〜11/12 のもの 13 件、Security NEXT の早稲田大学 [11/9 公表]・ソフト 99 [11/10]・Gunosy [10/26]・ヤマダデンキ [11/13]、GoQSystem のまとめ [公表 11/12]、Lovable の調査 [Handelsblatt 11/2]、Nous Research × Microsoft の Hermes Enterprise [11/18 発表]、ソースネクスト「みんなの筆王」の終了 [11/18 発表] など) / 重複=約 45 (vCenter の 0-day、NGINX2Root、PHP 8.x の更新と phpAfterShell、F5 BIG-IP、Drupal、Cisco Expressway の悪用、N-able、TfL、欧州委員会への攻撃、Gemini 4 Neon、Genie 4、Gemini の Mac のコンピューター操作、Tool Retrieval、Meta Muse、Microsoft Perception と Ignite の発表、GTIG の AI Threat Tracker、Epoch AI への攻撃、Splunk、SonicWall Gen 6、Jane の RCE 3 件、Git LFS 3 件、NATS MQTT の注入、MCP Python SDK、containerd ほか) / 日付不明=約 4 (Dark Reading の 2 本は本文を取得できず、SecurityWeek の週次まとめの個別項目 [NoName057(16) の EU 制裁など] は日付を確認できず)
- CISA KEV: 11/20 付で 4 件追加 (取得時点の dateReleased 2026-11-20T17:48Z)。11/18 付の 4 件は前号までに収録済み
- 取得失敗ソース: GitHub の REST API (`/advisories` はセッションのリポジトリ制限で使えず → OSV の API で代替)、Dark Reading の記事ページ (本文が空 → 未採用)、CISA advisories の RSS と MSRC の feed (XML の解析エラー)、GTIG の feed (空応答)、Embrace The Red・Trail of Bits・Project Zero・PortSwigger・watchTowr・Unit 42・SentinelLabs (期間内の新着なし)、トレンドマイクロ (日本) の RSS (空応答)、ruby/ruby の commit ページ (HTML の本文を取得できず → piyolog の出典リンクで URL を確認)
- 一次情報が自社サイトでない項目: SBC メディカルグループは米 SEC の 8-K を報じた BleepingComputer / SecurityWeek に依拠 (国内向けの公表文は未確認)。GSS は piyolog が引くデジタル庁の公表と報道に依拠

</details>
