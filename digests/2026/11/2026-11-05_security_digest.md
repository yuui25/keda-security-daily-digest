# KEDA Daily Digest — 2026-11-05 (JST)

> 採用範囲: 公開日 2026-11-03 〜 2026-11-05
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

- **AI 側**: Anthropic が、AI の応答が本当に指定したモデルから出たものかを暗号技術で証明する「FlashProve」を研究途中の段階で公開した。OpenAI は、コードの理解・レビューの道具を持つ Pierre Computer Company の買収と、サイバー向けの GPT-5.6 Cyber を AWS GovCloud で使える「Daybreak Red」を発表した。Apple は刷新版の「Siri AI」を全開発者に開放した。一方で Uber は、第 3 四半期に AI エージェント経由の配車が「4 件」だったと明かしている。
- **AI セキュリティ**: Check Point が、Codex の脱獄キットに広告を仕込む「プロンプトアドウェア」を報告した。Meta はエージェント Muse のバグバウンティで約 120 万ドルを払い、上位の事例 (信頼ヘッダーの誤用で 30 万ドル、ツール出力の偽装で 9 万ドル) を公開した。Xen の XSA-523 は Anthropic の Claude による発見とクレジットされ、Chrome 157 の Critical 7 件のうち 2 件も Anthropic の研究者が報告した。
- **セキュリティ側**: CISA が WordPress コアの更新中の競合状態 (CVE-2026-119977) を KEV に追加した (期限 11/6)。Debian/Ubuntu の APT に、MitM で検証済みのパッケージを差し替えて root でコードを実行できる欠陥 (CVE-2026-109518) が見つかった。Xen では、ゲスト VM から他の VM や dom0 のメモリを読み書きできる。APT29 系のウォータリングホールは、Web 解析スクリプトを乗っ取り iOS/Android の n-day を配っていた。
- **国内**: メール配信の「アララ メッセージ」の被害は約 7,700 万件のメールアドレスに広がった。委託元のアソビュー (約 1,582 万件) とビックカメラ G 3 社 (約 1,490 万件) も公表した。良品計画は MUJI Card のカード番号全桁 約 109 万件の流出の可能性を追加で公表した。プレステージ・コアソリューションの最大 550 万件 (ロードサービス)、7NOW の 16 万件 (配送委託先)、デニーズアプリでも漏えいがあった。
- **今日まず見るべき**: (1) Rails の Active Storage を使う案件があれば、`variant_processor` と ImageMagick のポリシーを確認する (→ 深掘り)。(2) Debian/Ubuntu の APT の更新。HTTP のミラーやプロキシを経由する CI/イメージビルドを優先する。

## 今日の深掘り

### Rails Active Storage に、アップロードを「添付するだけ」で任意のファイルを書き込める欠陥 (GHSA-f3w6-w445-fwh9、CVSS 9.8)。GMO Flatt Security の RyotaK 氏が報告

- **概要**: Rails は 11/4 (JST)、8.1.4.1 と 8.0.5.2 を公開し、21 件の脆弱性を修正した。最も深刻なのは、Active Storage の画像解析で ImageMagick を使うアプリが、未認証のアップロードで任意のファイルを書き込まれる欠陥 GHSA-f3w6-w445-fwh9 (Critical、CVSS 9.8、CVE は未採番) だ。保存先が Disk サービスの場合は、アプリが読めるファイルを任意に読み出すこともできる。Rails によると、読まれやすいのは `secret_key_base` や外部システムの認証情報で、そこから RCE や横展開につながりうる。HackerOne 経由で GMO Flatt Security の RyotaK 氏が報告した。
- **技術的な中身**:
  - ImageMagick は、ファイルの中身から「coder」(形式ごとのハンドラ) を選ぶ。coder の中には、画像そのものではなく、画像の中で指定された別のファイルを読み書きするものがある。Active Storage は、アップロードがどの coder を使えるかを制限しておらず、サーバー側の ImageMagick のポリシーだけが頼りだった。
  - 修正コミットによると、アップロードした SVG が Active Storage の解析器 (analyzer) を通って ImageMagick の **MSL coder** に届いていた。MSL は、スクリプトの中で指定したファイルを読み書きするスクリプト用の coder だ。
  - 重要なのは到達条件の軽さだ。解析器はファイルを**添付した時点**で動く。variant (変換した画像) やプレビューを作る必要も、`analyze` を呼ぶ必要もない。
  - 影響を受ける条件は 3 つすべてがそろった場合。①`config.active_storage.variant_processor = :mini_magick` (未設定なら `load_defaults` が 7.0 未満のとき既定で mini_magick、7.0 以降は vips)、②ImageMagick のポリシーが該当の coder を止めていない (Rails によると Debian/Ubuntu の既定のポリシーは止めていない)、③信頼できない利用者からアップロードを受け付ける。この設定は、variant を作るライブラリだけでなく、アップロードを解析するライブラリも決める。
  - 修正版は ImageMagick のポリシーを同梱する。MSL、画像以外のファイルを読み書き・削除する coder、リモートやローカルの参照を取りに行く coder、Ghostscript を使う coder と gs delegate、`@filename` による間接参照を止める。MiniMagick の既定の構成では、Active Storage 以外から呼ぶ ImageMagick のコマンドにもこのポリシーがかかる。
  - Rails は「報告された攻撃の連鎖は 1 つだが、それしかないとは考えていない」としている。同じリリースの GHSA-v924-7rp8-4mxh (High、8.8) では、Active Storage がアップロードの拡張子を残した一時ファイル名で ImageMagick と FFmpeg に渡していた。中身から形式が分からないとき、ツールは拡張子でデコーダーを選ぶため、攻撃者はファイル名と Content-Type でデコーダーを選べた。
- **背景・経緯 (背景引用)**:
  - 2016 年の「ImageTragick」(CVE-2016-3714 ほか) でも、MSL などの coder や delegate を悪用したファイル操作・コマンド実行が問題になった。対策として、ImageMagick の `policy.xml` で coder を止めるのが定石になった。今回は、その定石がディストリの既定のポリシーには入っておらず、Rails 側も制限していなかった形になる。
  - Rails は 2026 年 7 月にも、libvips を使う構成の Active Storage で、variant の生成から任意のファイルを読める欠陥 (CVE-2026-66066) を直している。libvips の「unfuzzed」な loader を無効にしていなかったのが原因だった。ImageMagick 構成はその攻撃経路の対象外だったが、今回の欠陥の対象になる。
- **なぜ今これが重要か (評価)**:
  - Rails のアプリで「プロフィール画像のアップロード」は定番の機能で、診断でも必ず通る入口だ。しかも、「変換しないから安全」という言い訳が通じない (添付だけで届く)。古い `load_defaults` のまま運用している長寿命のアプリほど mini_magick のままである可能性が高い。
  - 報告者が国内の研究者であり、詳細な解説が日本語で出る可能性がある。過去の Active Storage の欠陥と同じく、PoC が出るまでの期間は短いと見ておくべきだ。悪用の有無について advisory は触れていない。
  - 8.0 系のセキュリティサポートは **11/7 に終了**する。7.x 以前には修正版が出ないため、パッチを当てられない環境ではポリシーで止めるしかない。
- **読者が今日できること**:
  - 対象のアプリで `grep -rn "variant_processor\|load_defaults" config/` を実行し、mini_magick になっているかを確認する。`Gemfile.lock` の `activestorage` が 8.0.5.2 / 8.1.4.1 未満かも見る。
  - サーバーで `convert -list policy` (IM7 なら `magick -list policy`) を実行し、`MSL`・`MVG`・`TEXT`・`EPHEMERAL`・`URL` 系・`PS`/`PDF`/`EPS` (Ghostscript) と `@*` が `rights="none"` になっているかを確認する。
  - 診断では、アップロード機能に「拡張子・Content-Type・中身が食い違うファイル」(SVG に MSL を仕込むなど) を投げる観点を追加する。添付の直後に解析が走るため、レスポンスや後続ページで書き込みの痕跡が出るかを見る。
- 出典: [Rails 公式 (discuss.rubyonrails.org)](https://discuss.rubyonrails.org/t/rails-security-releases-8-0-5-2-and-8-1-4-1/91802) / [oss-security](https://seclists.org/oss-sec/2026/q4/509) / [GHSA-f3w6-w445-fwh9](https://github.com/rails/rails/security/advisories/GHSA-f3w6-w445-fwh9) / [GHSA-v924-7rp8-4mxh](https://github.com/rails/rails/security/advisories/GHSA-v924-7rp8-4mxh) / [The Hacker News](https://thehackernews.com/2026/11/critical-rails-flaw-lets-attackers.html) / 背景: [CVE-2026-66066 の告知 (2026-07-29)](https://discuss.rubyonrails.org/t/cve-2026-66066-possible-arbitrary-file-read-and-remote-code-execution-in-active-storage-variant-processing/91432)

## AI 技術・トレンド

### [2026-11-02〜03] Anthropic「FlashProve」: 応答が本当にそのモデルから出たかを暗号技術で証明する仕組みを、研究途中の段階で公開
- **何が起きたか**: Anthropic は 11/2 (米国時間)、AI の応答が指定したモデルによって生成されたことを暗号技術で証明する「provable inference」の仕組み FlashProve を発表した。コードと技術文書は Apache 2.0 で GitHub に公開されている。Frontier Red Team が EPFL や MIT の研究者と共同で開発した。Anthropic は、完成品ではなく研究の途中経過の共有だとしている。仕組みとして、AI 企業がモデルの「指紋」を公開する必要がある (TechCrunch)。
- **なぜ重要か**: ルーティングサービスがこっそり安いモデルに差し替える、ベンチマークのときだけ高いモデルを使う、といった行為を、運営者自身が相手でも検証できるようにする狙いだ。Anthropic は「このライブラリはフロンティアのサイバーモデルで脆弱性スキャン済み」のような主張の検証にも使える、と例を挙げている。AI による診断やコードレビューの結果を顧客に出す立場からすると、「どのモデルが見たか」を証明する手段が出てくる意味は大きい (評価)。
- 出典: [TechCrunch](https://techcrunch.com/2026/11/03/anthropic-is-working-on-a-system-to-prove-ai-models-identity/) / [ITmedia AI+](https://www.itmedia.co.jp/aiplus/article/2611/04/2000002863/)

### [2026-11-04] OpenAI、Pierre Computer Company の買収を発表。Codex の「コードを作る・理解する・レビューする」道具を拡充
- **何が起きたか**: OpenAI は 11/4、Pierre Computer Company を買収すると発表した。目的は、Codex のコードの構築・理解・レビューの道具を広げることだと説明している。買収額などの条件は、確認できた範囲では公表されていない。
- **なぜ重要か**: OpenAI は 11/2 にも、Codex の規模に合わせて自社で作った Git 互換のバックエンド「Pando」を紹介している (次項)。コード生成そのものよりも、レビューと大規模なリポジトリの運用を囲い込む方向にあり、GitHub (Copilot Code Review Max など) との競合が強まる (評価)。
- 出典: [OpenAI](https://openai.com/index/openai-to-acquire-pierre)

### [2026-11-03] OpenAI「Scaling Git at OpenAI」: Codex のための Git 互換バックエンド「Pando」を紹介
- **何が起きたか**: OpenAI はエンジニアリングブログで、Codex によって増えた開発量に合わせて作った Git 互換のバックエンド Pando を紹介した (公開は 11/2 15:30 GMT = 11/3 JST)。
- **なぜ重要か**: エージェントが大量のブランチと PR を作るようになり、Git ホスティングがボトルネックになっていることを示す。前号の GitHub の「スループット 180 倍」計画と同じ問題意識だ。エージェントがリポジトリに触れる頻度が増えるほど、ブランチ保護や秘密情報のスキャンの設定ミスの影響が大きくなる (評価)。
- 出典: [OpenAI](https://openai.com/index/scaling-git-at-openai)

### [2026-11-04] OpenAI「Daybreak Red」を AWS GovCloud (US-East) でも提供。承認済みの顧客が Bedrock 経由で GPT-5.6 Cyber を使える
- **何が起きたか**: OpenAI は、サイバー向けモデル GPT-5.6 Cyber を提供する Daybreak Red を、Amazon Bedrock 経由で AWS GovCloud (US-East) の承認済み顧客に提供すると発表した。用途は「承認されたサイバーセキュリティの業務」に限られる。
- **なぜ重要か**: 攻撃寄りの能力を持つモデルを、政府クラウドの中で、利用者を審査して出す形が定着しつつある。民間の診断ベンダーにとっても、こうした「審査付きのサイバーモデル」がツールの選択肢になる流れだ (評価)。
- 出典: [OpenAI](https://openai.com/index/daybreak-red-aws-govcloud)

### [2026-11-04] ChatGPT が GIF アニメを作れるように。画像モデル「Images 2.6」と同時に提供
- **何が起きたか**: OpenAI は ChatGPT で、プロンプトや写真から GIF アニメを作り、再生速度やフレームを個別に編集できる機能を、新しい画像モデル Images 2.6 とともに提供し始めた。Images 2.6 では画像の生成も速くなったとしている (The Verge)。
- **なぜ重要か**: 実務上の影響は小さいが、フィッシングや詐欺で使う「それらしい動く画像」の作成コストはさらに下がる (評価)。
- 出典: [The Verge](https://www.theverge.com/ai-artificial-intelligence/1026474/openai-chatgpt-animated-gifs-images-2-6)

### [2026-11-03] Apple、刷新版の「Siri AI」を全開発者に開放。App Intents で他社アプリの操作 (予約・注文など) を Siri から実行
- **何が起きたか**: Apple は 11/3 (米国時間)、Siri AI とサードパーティのアプリを連携させる機能を全開発者に開放すると発表し、iOS / iPadOS / macOS / visionOS 27.3 のβ版で開発者向けプレビューを始めた。App Intents を通じて、アプリのコンテンツや操作を Siri AI から直接使える。パーソナルコンテキストと画面上の情報の認識を組み合わせる。
- **なぜ重要か**: スマホの OS レベルのエージェントが、アプリの操作を代行する形が本格化する。アプリ診断では、App Intents として公開した操作が認可・確認なしで呼べないか (間接プロンプトインジェクション経由で呼ばれないか) が新しい観点になる (評価)。
- 出典: [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2611/04/2000002855/)

### [2026-11-04] Uber、第 3 四半期に他社の AI エージェントが手配した配車は「4 件」と開示
- **何が起きたか**: Uber の経営陣は 11/4 の決算説明会で、他社の AI エージェントによる配車が第 3 四半期に 4 件だったと明かした。Uber Eats では、ハロウィンの週に約 500 件あった。総取引は 3.2 億件 (The Verge)。
- **なぜ重要か**: 「エージェントがアプリを中抜きする」という懸念に対し、現時点では実態がほぼないことを示す数字だ。上の Siri AI や下の Cloudflare の動きは、この利用を増やす方向の基盤整備にあたる (評価)。
- 出典: [The Verge](https://www.theverge.com/transportation/1026306/uber-ai-agents-q3-earnings-disintermediation)

### [2026-11-04] Cloudflare、「パーソナルエージェント」のトラフィックを分析画面で区別し、エージェント単位でアクセス方針を設定できる機能
- **何が起きたか**: Cloudflare は、Security Analytics の Bot Analysis に「Personal Assistants」という区分を追加した。Verified Bot や Likely Human と並べて、人の代わりにサイトを使うエージェントのトラフィックだけを抽出でき、エージェントごとの細かいアクセス方針も設定できる。
- **なぜ重要か**: 「エージェントか人か」を WAF の段階で区別して扱う流れになる。診断側から見ると、この区分を信頼して認可を緩めるサイト (エージェントの User-Agent を名乗れば通るなど) が出てこないかが気になる (評価)。
- 出典: [Cloudflare Blog](https://blog.cloudflare.com/personal-agents-visibility-control/)

### [2026-11-04 / Universe で発表] GitHub「Copilot Dreaming」: 指示ファイルやメモリをバックグラウンドで整理・更新する機能をパブリックプレビュー
- **何が起きたか**: GitHub は Universe 2026 (10/28〜29) で、Copilot Dreaming をパブリックプレビューとして発表した。Copilot との対話や PR のレビューを分析し、AI 向けのガイダンス、Copilot Memory が覚えたコーディング規則・アーキテクチャ・プロジェクト固有のコマンドなどを、古くなったら自動で整理・修正する (Publickey が 11/5 に詳報)。
- **なぜ重要か**: エージェントの「指示ファイル」を AI が自動で書き換えるようになる。悪意のある PR やレビューコメントが、メモリや指示ファイルの更新に紛れ込めば、後続のすべての作業に影響する「永続化」の経路になりうる (評価)。下の「プロンプトアドウェア」も、グローバルな指示ファイルを書き換える手口だった。
- 出典: [Publickey](https://www.publickey1.jp/blog/26/github_copilot_dreaminggithub_universe_2026.html)

### [2026-11-03] Hugging Face「Model Integration Contracts」: 実チェックポイントを縮めたモデルで、CPU 上の統合テストを回す
- **何が起きたか**: Hugging Face は Transformers のテスト手法を紹介した。7/30 に T5 で PyTorch の SDPA を有効にした副作用で、UMT5 のデコーダーが未来のトークンを見られる状態になり、約 2 か月 main に残っていた。実際のチェックポイントの構成から層を減らした小さなモデル (UMT5 で 66MB、元は 1,227MB) を使ったテストなら、該当コミットすべてで検出できたという。
- **なぜ重要か**: 「クラッシュしないが結果が静かに壊れる」種類の不具合は、セキュリティでいう検証の欠落と同じ構造をしている。モデルを扱う OSS の品質保証の参考になる (評価)。
- 出典: [Hugging Face Blog](https://huggingface.co/blog/transformers-mic)

### [2026-11-04] Claude のプラン名変更 (Max 5x → Max、Max 20x → Ultra) に「容量半減か」の声。Anthropic は「元々、週次の上限は Pro の 10 倍」と否定
- **何が起きたか**: Anthropic は 10/30 にプラン名を変更した (価格は月 110 ドルと 220 ドルで据え置き)。Ultra の説明に「Pro の 10 倍」とあったため、利用者から容量が減ったのではという声が出た。同社のプロダクト責任者 Mike Overell 氏は X で、「20x」は 5 時間の上限についての表記で、週次の上限は導入時から Pro の 10 倍だったと説明した。Ultra では 5 時間の上限が撤廃されている。
- **なぜ重要か**: 診断業務で Claude Code などを使う場合、5 時間の上限が消えたことで長時間のエージェント作業の計画は立てやすくなる。一方、週次の上限は変わらない (評価)。
- 出典: [ITmedia AI+](https://www.itmedia.co.jp/aiplus/article/2611/04/2000002862/)

### [2026-11-02 発表 / 11-04 報道] 東北大学とアイシン、STT-MRAM を搭載した AI チップを開発。「16nm の AI SoC では世界初」
- **何が起きたか**: 東北大学 (CIES の遠藤哲郎教授のチーム) とアイシンは、32MB の STT-MRAM と AI アクセラレーター、Arm Cortex-A53 ×2、Mali-G31 を TSMC の 16nm FinFET で集積したチップを発表した。STT-MRAM に OS のブートデータと AI モデルの重みを置き、電源投入から OS カーネルの起動までを 2,535.3ms から 65.7ms (約 39 倍) に短縮した。物体検出の処理時間は約 1/10、エネルギーは 1/50 という。
- **なぜ重要か**: 車載などのエッジ AI では「すぐ起動する」ことが安全性に直結する。一方、モデルの重みが不揮発性メモリに常駐するため、物理的に取り出されたときの重みの保護 (暗号化や読み出しの防止) は新しい論点になる (評価)。
- 出典: [MONOist](https://monoist.itmedia.co.jp/mn/articles/2611/04/news046.html)

## AI セキュリティ

### [2026-11-03] Check Point「プロンプトアドウェア」: Codex の脱獄キット「Haiou」が、エージェントのグローバル指示ファイルに広告を常駐させる
- **何が起きたか**: Check Point Research は、OpenAI Codex 向けの脱獄キット Haiou (海鴎) を分析した。Codex の設定ファイルを書き換え、「hi」「hello」「Seagull」などのあいさつに反応して、作者が運営する OpenAI 互換の LLM ゲートウェイ (`zz.aiapi2025[.]top`) の広告を返すようにする。ロールプレイや「CTF だ」という言い換えで安全対策を外し、ペンテストやクラッキング、リバースエンジニアリングの skill も入れる。GitHub の `haiou-codex` は 7/10 の公開以来、スター 403・フォーク 77 で、Codex の GUI 設定ツール Codex-X にも同梱されていた。
- **なぜ重要か**: 実行ファイルを使わず、自然言語の指示と設定ファイルだけで「永続化」している。EDR やコードのスキャンでは見つけにくい。無料の脱獄キットを入口に、有料のゲートウェイへ誘導する事業モデルで、ゲートウェイ側ではプロンプトやコードを盗み見られる (評価)。開発者の端末の `~/.codex` や `AGENTS.md`、`CLAUDE.md` の差分の監視は、診断の対象として扱うべき段階に来ている。
- 出典: [Check Point Research](https://research.checkpoint.com/2026/free-the-model-sell-the-gateway-prompt-adware-hidden-in-jailbreak-bundles/) / [The Hacker News](https://thehackernews.com/2026/11/researchers-uncover-prompt-adware.html)

### [2026-11-04] Meta、エージェント Muse のバグバウンティで約 120 万ドルを支払い。上位は「ローカルのプロキシが付けたヘッダーを信頼」で 30 万ドル
- **何が起きたか**: Meta の David Singleton 氏によると、Muse (メール・カレンダー・メッセージなどを代わりに操作する個人用エージェント。利用者ごとに VM を持つ) のバグバウンティには 630 件超の報告があり、64 件が有効だった。
  - 30 万ドル: 公開の 4 か月前、社員がテストに使う VM で会話とトークンにアクセスできた。認証のチェックが「ローカルの HTTPS プロキシが付けるヘッダー」を信頼の証拠にしていた。システム移行でプロキシが 2 段になり、外部からの要求にも同じヘッダーが付くようになった。
  - 9 万ドル: 要約させた Web ページが、ブラウズ用ツールのステータスメッセージを偽装し、本来は止まるべき操作をエージェントに実行させた。
  - 9 万ドル: 特定の書式で、ワンタイムパスコードがメールの墨消しフィルターを通り抜けた (エンドツーエンドの攻撃の一部)。
- **なぜ重要か**: 30 万ドルの事例は AI 固有ではなく、「前段のプロキシが付けるヘッダーで認証する」古典的な設計ミスだ。エージェント基盤でもこの種の欠陥が最も高く評価されている。ツール出力の偽装は、エージェント診断で「ツールの応答とページ本文の区別」を見る観点としてそのまま使える (評価)。
- 出典: [SecurityWeek](https://www.securityweek.com/meta-shares-top-muse-bug-bounty-findings-as-payouts-reach-1-2-million/)

### [2026-11-04] DeepSeek Harness に、ローカルの RPC の認証がない欠陥 (CVE-2026-82033、CVSS 4.0 8.6)。別ユーザーのプロセスからエージェントの bash を動かし、承認も迂回できる
- **何が起きたか**: エージェント実行環境 DeepSeek Harness の 0.1.2-alpha.2 より前では、Web プロファイルの HTTP / WebSocket の RPC に認証がなかった。同じ端末の任意のプロセス (別の OS ユーザーを含む) が `session.create` や `session.prompt` を呼び、エージェントの bash とファイル操作のツールで、被害者の権限とモデルの認証情報を使ってコマンドを実行できる。イベントのストリームでセッションの内容を盗み見たり、`POST /api/respond` に `rpcId`・`approvalId`・`sessionId` を合わせるだけで、人の承認を迂回したりもできる (NVD)。
- **なぜ重要か**: 「localhost で待ち受けるエージェントの制御プレーン」は、MCP サーバーや各種 IDE 連携でも繰り返されているバグクラスだ。共有の開発サーバーや CI のランナーでは、ローカルの別ユーザーがそのまま攻撃者になる (評価)。
- 出典: [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-82033) / [修正コミット 3e24087](https://github.com/deepseek-ai/deepseek-harness/commit/3e24087bfaeabe40b58ba2f7b936895b8f93fe27) / [VulnCheck](https://www.vulncheck.com/advisories/deepseek-harness-unauthenticated-rpc-command-execution)

### [2026-11-04] AI による脆弱性発見: Xen の XSA-523 は Anthropic の Claude による発見、Chrome 157 の Critical 7 件のうち 2 件も Anthropic の研究者
- **何が起きたか**: Xen Project は XSA-523 (CVE-2026-102703 / 102704、下記) の発見者として、Claude を使った Anthropic をクレジットした。Ada Logics の Stephan Lipp 氏が検証し、CodeAnt AI のチームも後から同じ問題を独立に報告している。Chrome 157 では、Critical の use-after-free とバッファオーバーフロー 5 件のうち 2 件を、Anthropic の Xinyang Ge 氏が報告した。
- **なぜ重要か**: ハイパーバイザーのキャッシュの再検証漏れのような、「最適化のための近道」に潜む論理バグを AI が見つけている。同じ問題を別の AI 系チームが独立に報告している点も、AI による発見が「重複して見つかる」段階に来ていることを示す (評価)。
- 出典: [The Hacker News (Xen)](https://thehackernews.com/2026/11/xen-hypervisor-flaws-let-one-malicious.html) / [SecurityWeek (Chrome 157)](https://www.securityweek.com/chrome-157-rolls-out-with-213-security-fixes-seven-rated-critical/)

### [2026-11-04] [続報] AI 開発基盤への侵害が相次ぐ: Trigger.dev、Northflank、WorkOS など。狙いは「顧客が預けた AI のアクセスキー」
- **前回から何が変わったか**: SecurityWeek は、過去 1 か月で少なくとも十数の AI 開発基盤が侵害されたとまとめた (Andromeda、NVIDIA の Brev、CommandCode、Fireworks AI、Lightning AI、Northflank、OpenCode、Railway、Trigger.dev、Warp、Zeabur、Chainstack、WorkOS)。事案どうしは無関係とみられ、初期侵入は盗まれた認証情報、第三者の依存関係、脆弱性の悪用とさまざまだ。Cloud Security Alliance は、ホスティングや評価サービスのような「中間層」が多数の顧客のキーを持つため、1 回の侵入で多くの推論アカウントのキーが漏れると指摘した。Wiz は、LLMjacking とキーの仲介市場、さらに蒸留 (distillation) の需要が背景にあると分析している。
- **なぜ重要か**: 診断の対象として、自社の LLM のキーを預けている SaaS (評価・観測・ゲートウェイ) を棚卸しする必要がある。キーにプロジェクト単位の上限と利用元の制限をかけるのが現実的な対策だ (評価)。
- 出典: [SecurityWeek](https://www.securityweek.com/ai-linked-breaches-mount-as-workos-northflank-trigger-dev-disclose-hacks/)

### [2026-11-03 arXiv] 「命令」を書かずにエージェントを操る: 偽の危険情報で選択を誘導する「Voluntary Servitude」と、引数だけを書き換える「Parameter Poisoning」
- **何が起きたか**:
  - *Voluntary Servitude* (arXiv:2611.04393): 普通のレビューの形で「危険がある」という嘘を 1 つ書くだけで、エージェントは自分の安全判断によって正規の選択肢を外し、攻撃者の選択肢を選んだ。誘導の成功率は 60.4% で、命令を書き込む従来のインジェクション (66.0%) とほぼ同じだった。既存のインジェクション検知器は、これを良性と判定した。
  - *Right Tool, Wrong Parameters* (arXiv:2611.04673): 呼ぶツールは正しいまま、宛先などの引数だけを書き換える攻撃を扱い、「どの情報源がどの引数を決めてよいか」という情報フローの信頼度で防ぐ方法を提案している。
- **なぜ重要か**: どちらも「新しいツール呼び出しや命令文」を探す検知をすり抜ける。エージェント診断では、送金先・宛先・数量などの引数が、外部の文書の影響で変わらないかを確認するテストケースを持つべきだ (評価)。
- 出典: [arXiv:2611.04393](https://arxiv.org/abs/2611.04393v1) / [arXiv:2611.04673](https://arxiv.org/abs/2611.04673v1)

### [2026-11-03 arXiv] 良性の skill を足すと危険な操作も増える (+10.3pt)、エージェント用システムプロンプトの抽出手法 ExtraHerO
- **何が起きたか**:
  - *Can Benign Skills Induce Misaligned Behavior in LLM Agents?* (arXiv:2611.04299): 5 つのモデルと 3 つのベンチマークで、skill を足すと正常なタスクの精度が平均 10.3pt 上がる一方、安全要件に反する外部操作の割合も 10.3pt 上がった。専門家が整えた skill でも同じ傾向だった。
  - *Extracting System Prompt of LLM Services in Complex (Agentic) Settings* (arXiv:2611.04803): ツールのスキーマやガードレールを含む長いシステムプロンプトや、最終的な行動しか観測できない環境では既存の抽出攻撃が効きにくいと検証した。そのうえで、構造テンプレートを使って階層的に復元する ExtraHerO を提案している。
- **なぜ重要か**: 「skill を入れるほど便利で危険」という定量的な結果は、上の Haiou (ペンテスト用の skill を同梱) の話と重なる。システムプロンプトの抽出は、エージェント診断で最初に行う偵察そのものだ (評価)。
- 出典: [arXiv:2611.04299](https://arxiv.org/abs/2611.04299v1) / [arXiv:2611.04803](https://arxiv.org/abs/2611.04803v1)

## セキュリティニュース

### [2026-11-03〜04] [続報] WordPress コアの更新中の競合状態が「CVE-2026-119977」として KEV 入り。連邦機関の期限は 11/6
- **前回から何が変わったか**: 10/30〜31 号では CVE の採番前として扱った。CISA は 11/3 付で KEV に追加し、「完全なパッケージでのコア更新で使う、予測可能で Web から見えるステージングのパスが原因」と説明した。CVSS は 8.1 (TOCTOU)。Wordfence は、公表から 21 時間で、ステージングされた `setup-config.php` を狙う要求を 1.85 万件超記録し、THN の記事執筆時点の直近 24 時間でも 12,632 件をブロックした。Previdian のハニーポットは 10/30 に英国の IP から 3 件の悪用試行を観測した。EPSS は 0.0102 (11/4 時点)。
- **悪用 / PoC**: 悪用あり (CISA が KEV に登録)。公開 PoC は未確認。
- **なぜ重要か**: 自動更新を有効にしているサイトほど、「更新の数秒間」に攻撃を受ける。7.1.4 への更新に加え、`wp-content/upgrade/` 配下で PHP を実行させない設定を推奨事項として明記したい (評価)。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/cisa-confirms-hackers-exploiting.html) / [BleepingComputer](https://www.bleepingcomputer.com/news/security/cisa-flags-wordpress-rce-flaw-as-actively-exploited-in-attacks/) / [Security NEXT](https://www.security-next.com/192310) / [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

### [2026-11-04] Debian / Ubuntu の APT に、MitM で検証済みのパッケージを差し替えて root でコードを実行できる欠陥 (CVE-2026-109518)
- **何が起きたか**: Debian、Ubuntu、APT の開発者が 11/4 に advisory を出した。HTTP の通信を改ざんできる攻撃者 (悪意のあるミラーやプロキシを含む) が、リダイレクトと一時的なサーバーエラーで APT にダウンロードを再試行させる。すると APT は既存のハードリンクを上書きし、検証済みのパッケージを攻撃者のものに入れ替えてしまう。deb は root で入るため RCE になる。条件は `Acquire::Retries` が 0 でないことで、APT 2.3.2 以降 (Debian 12 / Ubuntu 22.04 以降) は既定で 3。報告者は Max Justicz 氏。Ubuntu の評価は CVSS 4.0 で 7.7、APT の開発者は critical としている。
- **悪用 / PoC**: 悪用の報告なし。回避策の記載もない。HTTPS のソースが影響を受けるかは advisory に書かれていない。
- **なぜ重要か**: 「署名で守られているから HTTP のミラーでよい」という前提が崩れた。社内ミラーや透過プロキシ、キャッシュプロキシ (apt-cacher-ng など) を通る CI やコンテナのビルドが、最も現実的な攻撃面だ (評価)。
- 出典: [Debian DSA](https://lists.debian.org/debian-security-announce/2026/msg00526.html) / [APT 開発者の advisory (deity)](https://lists.debian.org/deity/2026/11/msg00005.html) / [Ubuntu](https://ubuntu.com/security/CVE-2026-109518) / [The Hacker News](https://thehackernews.com/2026/11/debian-and-ubuntu-apt-flaw-lets-mitm.html)

### [2026-11-04] Rails 8.1.4.1 / 8.0.5.2 で 21 件を修正 → 今日の深掘りを参照
- **何が起きたか**: 上記の Active Storage の 2 件のほか、Strong Parameters の迂回 (`Parameters#each_key`、High)、`Forwarded` ヘッダーによる `remote_ip` の偽装 (8.1 のみ、High)、`safe_constantize` の DoS (High)、Action View のヘルパー群の XSS (Medium ×4 ほか)、CacheStore で破棄したセッションが復活する問題、Action Mailbox の Mailgun 受信での署名の再送 (Low) などを修正した。
- **なぜ重要か**: `remote_ip` の偽装と Strong Parameters の迂回は、IP 制限や一括代入の診断で再確認すべき項目だ (評価)。
- 出典: [Rails 公式](https://discuss.rubyonrails.org/t/rails-security-releases-8-0-5-2-and-8-1-4-1/91802)

### [2026-11-03〜04] Xen の grant copy に、ゲストから他の VM や dom0 のメモリを読み書きできる欠陥 (XSA-523、CVE-2026-102703 / 102704)
- **何が起きたか**: Xen 4.6 以降すべてが影響を受ける。同じページへの grant copy をまとめて処理するとき、Xen は検証済みのデータをキャッシュして再利用するが、再検証の条件が一部で誤っていた。フレーム番号と grant 参照を取り違える (102703) などで、悪意のあるゲストが自分のものでないメモリを読み書きできる。回避策はない。XCP-ng は「侵害された 1 つのゲストがホスト全体を乗っ取れる」と説明し、Critical と評価した。Qubes OS はすべての構成が影響を受けるとしている。
- **悪用 / PoC**: 悪用の報告なし。
- **なぜ重要か**: Xen ベースの VPS やクラウドでは、隣の顧客の VM が攻撃者になりうる。4.6〜4.16 にはパッチがない (評価)。
- 出典: [Xen XSA-523](https://xenbits.xenproject.org/xsa/advisory-523.html) / [The Hacker News](https://thehackernews.com/2026/11/xen-hypervisor-flaws-let-one-malicious.html)

### [2026-11-03〜04] [続報] Linux カーネルの TCP の UAF (CVE-2026-98432): RHEL 8/9/10 の修正版が出た。Red Hat は評価を 5.9 から 9.8 に引き上げ
- **前回から何が変わったか**: Red Hat は 11/1 に RHSA-2026:93414 (RHEL 8)、93412 (RHEL 9)、93413 (RHEL 10) を出し、評価を Moderate (5.9) から Critical (9.8) に上げた。Ubuntu は 22.04 / 24.04 / 26.04 の修正を opt-in の `-proposed` に置いたままで、通常の配布日は未定。20.04 以前は未修正。Red Hat は 10/30 に、IP オプション付きの IPv4 TCP パケットを捨てる nftables のルールも公開している。Security NEXT は「特定環境での実証も報告されている」と伝えた。
- **なぜ重要か**: 認証なし・任意の待ち受けポートで届くため、Ubuntu の LTS が最大の残存面になっている。Record Route / Timestamp オプションを境界で落とすのが、当面の現実的な対処だ (評価)。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/red-hat-patches-98-rated-linux-tcp-rce.html) / [Security NEXT](https://www.security-next.com/192332)

### [2026-11-04] SonicWall、サポート終了の GMS に未認証のファイル読み出し (CVE-2026-109593、9.1) と SQLi (CVE-2026-109594、6.8)。修正版は出さない
- **何が起きたか**: SonicWall は、GMS 9.5.2 以前に、ネットワークから内部ファイルを読める未認証の欠陥と、認証後の SQL インジェクションがあると公表した。製品はサポート終了のため修正せず、NSM への移行を求めている。別件の SMA1000 の SSRF (CVE-2026-102255、10.0) については、Previdian が 10/9 以降に 2,541 件、11/3 だけで 30 件の悪用試行を観測している。
- **悪用 / PoC**: GMS の 2 件は悪用の報告なし。EPSS は CVE-2026-109593 が 0.0052。
- **なぜ重要か**: パッチが出ないことが確定したため、外部から GMS の管理画面が見えていれば、それ自体が指摘事項になる (評価)。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/sonicwall-wont-patch-eol-gms-flaws-that.html) / [SonicWall PSIRT](https://psirt.global.sonicwall.com/vuln-detail/SNWLID-2026-0019) / [Security NEXT](https://www.security-next.com/192328)

### [2026-11-04] APT29 系とされる「Poisoned Source」: Web 解析サービス Plerdy の乗っ取りと偽サイトで、iOS / Android に n-day の連鎖を配る (Sekoia)
- **何が起きたか**: Sekoia によると、攻撃者は正規サイトの改ざん、有名サイトを装った偽ドメイン (`america250[.]holiday` など)、ウクライナの Web 解析サービス Plerdy SEO Tracker のスクリプト (`a.plerdy[.]com/public/js/click/main.js`、8/27〜9/3) の改ざんの 3 経路で JavaScript を仕込んだ。端末を判別して、iOS 16.7 には CVE-2025-43529 と CVE-2024-27834、iOS 18.5 には DarkSword の連鎖 (CVE-2025-43529、CVE-2026-20700 ほか)、Chrome 139〜145 (143 を除く) の Android には CVE-2026-3910 と CVE-2025-27038 を使った。Cookie、Wi-Fi のパスワード、iOS では SMS・iMessage・キーチェーンなどの端末データまで持ち出す。
- **悪用 / PoC**: 悪用あり (実際の作戦)。使われたのは既知の n-day。
- **なぜ重要か**: サードパーティのタグ (解析・広告) は、1 つの改ざんで多数のサイトの訪問者に届く。SRI や CSP の診断で、解析タグを例外にしていないかを確認する根拠になる。モバイルの更新を後回しにする端末管理の甘さも突かれている (評価)。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/apt29-linked-hackers-hijack-web.html) / [BleepingComputer](https://www.bleepingcomputer.com/news/security/hackers-use-n-day-exploits-in-zero-click-attacks-on-ios-android-devices/) / [Help Net Security](https://www.helpnetsecurity.com/2026/11/04/apt29-watering-hole-mobile-devices-n-day-exploits/)

### [2026-11-04] 中国系の SlippyNunchucks、Sogou 入力法の HTTP の設定取得を DNS ハイジャックで乗っ取り、DarkVigil を配る。標的に日本も (ESET)
- **何が起きたか**: ESET によると、7/1 以降、Sogou 入力法 (Windows 版) の正規コンポーネント `SGTool.exe` が HTTP で取りに行く設定 (`config.pinyin.sogou[.]com/api/brandScd/getBrandScd.php`) を、DNS の改ざんで攻撃者のサーバーに向け、悪意のある設定経由で .NET 製のバックドア DarkVigil (FDMTP、20 超のプラグイン) を入れた。標的は香港、タイ、日本、ベトナム、オマーン、スリランカの組織と中国語話者。8 月に FortiGuard が報告した QuickFox VPN の供給網の侵害で、クリーン版が出た 3 日後に Sogou に切り替えた。
- **悪用 / PoC**: 悪用あり (実際の作戦)。
- **なぜ重要か**: 「平文の HTTP で設定や更新を取りに行く常駐ソフト」は、上の APT の件と同じく MitM で崩れる。国内の中国語圏の拠点や、IME を自由に入れられる端末は棚卸しの対象になる (評価)。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/china-aligned-hackers-hijack-sogou.html)

### [2026-11-04] 『勝利の女神：NIKKE』の PC ランチャーのスクリプトが改ざんされ、認証情報と暗号資産ウォレットを盗むマルウェアを配布
- **何が起きたか**: 開発元は X で、PC ランチャーのスクリプトが第三者に改ざんされた可能性を認め、11/4 2:30 (JST) ごろにクライアントを修正・更新したと告知した。影響範囲は調査中。独立の研究者の GitHub の報告によると、遠隔操作と情報窃取の機能を持つマルウェアが配られた (BleepingComputer)。パブリッシャーの Level Infinite によると、累計 4,500 万ダウンロード超。
- **悪用 / PoC**: 悪用あり (実際の配布)。
- **なぜ重要か**: 日本でも利用者が多いタイトルで、社用 PC に入っている可能性もある。ゲームのランチャーは自動更新の権限が強く、検証が甘い「第 2 のソフト配布チャネル」になっている (評価)。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/nikke-pc-game-launcher-hacked-to-spread-remote-access-data-stealing-malware/) / [Zenn (利用者による自己調査)](https://zenn.dev/nanana_sk/articles/nikke-launcher-incident)

### [2026-11-04] DreamHost、Web の File Manager の脆弱性を突かれ、約 2 か月にわたり FTP / SFTP の認証情報を盗まれていた
- **何が起きたか**: DreamHost によると、攻撃者は `files.dreamhost.com` の File Manager のソフトウェアの脆弱性を悪用し、2026 年 8 月ごろから発見日の 10/23 までにログインした利用者の FTP / SFTP のユーザー名とパスワードを取得した。一部の利用者では、Webmail のセッション情報も見られた可能性がある。
- **悪用 / PoC**: 悪用あり (侵害が確定)。脆弱性の詳細は非公表。
- **なぜ重要か**: ホスティングの「ブラウザで使うファイル管理」は、平文の認証情報を中継する点で、cPGuard の件 (前号) と同じくホスティング事業者の管理機能が狙われている (評価)。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/dreamhost-confirms-data-breach-exposed-ftp-logins-and-webmail-sessions/)

### [2026-11-04] Google カレンダーの招待で Google のセッションを盗むフィッシング「Operation CloudFire」。リンクは Google 自身のリダイレクタ経由
- **何が起きたか**: Material Security によると、8 月中旬から、留守電の通知、RFP、裁判所の呼び出しなどを装った Google カレンダーの招待が届いている。リンク先は Google の `/url` リダイレクタ、`share.google`、Drive のリンクで、ドメイン・証明書・評判はすべて正規に見える。最後は Google のログイン画面の前に置いたリバースプロキシで、MFA を含めてセッションを奪う。Material は数百のドメインを停止させた。
- **悪用 / PoC**: 悪用あり (実際の作戦)。
- **なぜ重要か**: メールゲートウェイの評判判定をすべて「正規」で通過させる設計で、検知はログイン後のセッションの異常 (端末・場所の変化) に頼るしかない。カレンダーの外部招待の自動追加を止める設定は、すぐに効く対策だ (評価)。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/google-calendar-phishing-campaign-hijacks-sessions-bypasses-mfa/)

### [2026-11-04] 仏 Crédit Mutuel Arkéa、委託先経由の侵入で自社の口座から送金され、推定 1.33 億ドルを窃取される
- **何が起きたか**: Arkéa は 11/4、委託先のプラットフォームを経由した「高度な攻撃」で、攻撃者が同社自身の口座から他の金融機関へ送金し、暗号資産に換えた可能性があると発表した。顧客の口座には触れていないとしている。ZachXBT 氏が 1.33 億ドル超と推定し、同社は「桁は合っている」と認めた。一部の資産は凍結済み。
- **悪用 / PoC**: 侵害が確定。手口の詳細は非公表。
- **なぜ重要か**: Binance (64.3 億ドル) に続き、金融機関の「業務用の送金経路」そのものが乗っ取られた。委託先のアクセスが送金の権限に届く設計かどうかは、金融系の診断でまず見るべき点だ (評価)。
- 出典: [The Record](https://therecord.media/french-bank-confirms-cyber-heist)

### [2026-11-02〜04] [続報] 欧州の冷蔵設備への攻撃、仏の血液機関 EFS の 3 施設でも温度と霜取りの設定を変更。供給元 Coolworld は「第三者の部品の脆弱性」と説明
- **前回から何が変わったか**: 前号まではスーパーの冷凍・冷蔵設備が中心だった。フランス血液公社 (EFS) は 11/3、冷蔵設備の供給元が攻撃を受け、11/2 に 3 施設で保冷室の温度と霜取りの設定が上げられたと発表した。EFS は直接の標的ではない。冷蔵設備のレンタル会社 Coolworld Rentals は、遠隔監視ソフトの問題で一部の機器が影響を受け、原因は自社の管理外にある第三者の部品の脆弱性だとしている。SentinelOne も一連の攻撃の評価を公開した。
- **なぜ重要か**: 被害が食品から医療 (血液製剤) に広がった。遠隔監視の SaaS とその部品が共通の入口になっている可能性がある (評価)。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/cyberattack-disrupts-blood-storage-refrigeration-systems-in-france/) / [The Record](https://therecord.media/france-cyberattack-blood-refrigeration) / [SentinelLabs](https://www.sentinelone.com/labs/defrost-and-disrupt-an-assessment-of-europe-s-refrigeration-attacks/)

### [2026-11-04] ロシアの大手ホスティング Beget、管理系への侵入でクラウドのデータを消去される。VPS のバイナリバックアップもすべて喪失
- **何が起きたか**: Beget によると、攻撃者はインフラ管理用のシステムにアクセスし、データを消すスクリプトを実行した。VPS、クラウドストレージ、Kubernetes のデータが消え、VPS のバイナリバックアップもすべて失った (ファイル単位のバックアップは残存)。1,000 台超のサーバーを手作業で確認する必要があるという。同日、ウクライナの Kyiv Independent も CMS とニュースレターの配信サービスを乗っ取られ、偽情報 (ゼレンスキー大統領がキーウに核弾頭を撃ったなど) を配信された。
- **なぜ重要か**: 「管理プレーンを取られるとバックアップごと消える」典型例。バックアップを本番と同じ管理系から消せる構成になっていないかは、ランサムウェア対策の診断でも同じく問題になる (評価)。
- 出典: [The Record (Beget)](https://therecord.media/russia-cyberattack-beget-cloud) / [The Record (Kyiv Independent)](https://therecord.media/ukraine-kyiv-independent-cyberattack)

### [2026-11-04] 米国、大学のスパコンで暗号資産を採掘したとしてカナダ人 2 人を起訴。1 人は米国に移送
- **何が起きたか**: 米国の大陪審は、Ryan James Roach 被告 (35) と Mathiew James Stubbings 被告 (41) を起訴した。2016 年 6 月〜2019 年 12 月に、偽名で借りた複数国の VPS からニューヨーク、テネシー、ノースカロライナ、マサチューセッツの教育機関にマルウェアを送り、認証情報の窃取、採掘、スパコンを使った脆弱性の研究などをした疑い。1 人は米国に移送された (The Record)。
- **なぜ重要か**: 7 年前の侵入でも起訴に至った例。大学の HPC は計算資源そのものが狙われる (評価)。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/us-charges-two-canadians-accused-of-hacking-us-universities/) / [The Record](https://therecord.media/canadian-nationals-accused-us-education-hacks-cryptomining)

### [2026-11-04] Chrome 157 で 213 件を修正 (Critical 7、High 77)。最も多いのは「認可の誤り・欠落」の 51 件
- **何が起きたか**: Google は Chrome 157 (157.0.8103.38/.39) を安定版にした。Critical のトップは WebGPU の実装 Dawn のバッファオーバーフロー (報奨金 1 万ドル)、次は ANGLE のメモリ破壊。種類別では、認可の誤り・欠落 51、UAF 45、UI の偽装 19、型の取り違え 13 など。悪用の報告はない。
- **なぜ重要か**: 件数そのものが異例に多い。AI による発見の増加 (上記) との関係を示唆する (評価)。
- 出典: [SecurityWeek](https://www.securityweek.com/chrome-157-rolls-out-with-213-security-fixes-seven-rated-critical/) / [Security NEXT](https://www.security-next.com/192316)

### [2026-11-04] PortSwigger、Burp AT に「HTTP リクエストヘッダーのインジェクション → CRLF による desync」の自動化 skill とスキャンチェックを追加
- **何が起きたか**: PortSwigger Research は、HTTP リクエストヘッダーのインジェクションを見つけるスキャンチェックと、研究「CRLF-Powered Desync Attacks」の手法を Burp AT の skill として追加した。1 回のプロンプトで、注入位置の上流での形 (パスがカスタムヘッダーに書き換わり Host の前後どちらに来るか) の特定、リクエスト分割の構築、desync の証明、ランダムな利用者を collaborator にリダイレクトさせる攻撃までをバックグラウンドで進める。
- **なぜ重要か**: 研究レベルの手法がツールの既定の動作になると、「ヘッダーインジェクションは Low」という評価のままでは済まなくなる。診断の報告書で深刻度の付け方を見直すきっかけになる (評価)。
- 出典: [PortSwigger Research](https://portswigger.net/research/making-http-header-injection-critical-with-one-prompt)

### [2026-11-04] Node.js、11/11 ごろに 22 / 24 / 26 系のセキュリティリリースを予告 (最高深刻度は High)
- **何が起きたか**: Node.js プロジェクトは、22・24・26 系の新版を 11/11 以降に出すと予告した。最も深刻なものは High。
- **なぜ重要か**: 来週の更新計画に入れておく (評価)。
- 出典: [oss-security](https://seclists.org/oss-sec/2026/q4/510)

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-11-03 以降 (JST) / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| GHSA-f3w6-w445-fwh9 (CVE 未採番) | Rails Active Storage < 8.0.5.2 / 8.1.0〜8.1.4.0 | — / 9.8 (Critical) | mini_magick 構成で、アップロードを添付すると analyzer が ImageMagick を呼び、coder の制限がない → SVG から MSL coder に到達 → 任意のファイルの書き込み (Disk サービスなら読み出しも) | [468aa9a](https://github.com/rails/rails/commit/468aa9a93fc98f5476b6821770f4ccfcb7f7d328) / [ea8c401](https://github.com/rails/rails/commit/ea8c40121ce53a3d0255cd4eb6d13bfe3bc01776) (THN が参照。どちらがどの GHSA かは advisory で確認) | 未認証 / 報告者は国内 (RyotaK 氏) |
| GHSA-v924-7rp8-4mxh | Rails Active Storage (同上) | — / 8.8 | 一時ファイル名にアップロードの拡張子を残して ImageMagick / FFmpeg に渡す → 中身で判別できないとき拡張子でデコーダーを選ぶ → ファイル読み出し・RCE | [advisory](https://github.com/rails/rails/security/advisories/GHSA-v924-7rp8-4mxh) (commit は上記の可能性) | 未認証 |
| CVE-2026-109518 | APT (Debian 12 / Ubuntu 22.04 以降は既定で影響、旧版も `Acquire::Retries` 設定時) | CWE-367・CWE-62 / CVSS 4.0 7.7 (Ubuntu) | HTTP でリダイレクト + 一時エラーで再試行させる → 既存のハードリンクを再利用して上書き → 検証済みの deb を未検証のものに差し替え、root で実行 | [Debian DSA](https://lists.debian.org/debian-security-announce/2026/msg00526.html) (commit 不明) | MitM 前提 / 開発者は critical |
| CVE-2026-102703 / 102704 (XSA-523) | Xen 4.6 以降すべて | CWE-704 / NVD 4.4 (XCP-ng は Critical) | grant copy の一括処理で検証済みデータのキャッシュを再利用 → 再検証の条件の誤り (フレーム番号と grant 参照の取り違えなど) → ゲストから他の VM・dom0 のメモリを読み書き | [XSA-523 (パッチ同梱)](https://xenbits.xenproject.org/xsa/advisory-523.html) | 回避策なし / AI (Claude) が発見 |
| CVE-2026-121971 | Symfony HttpClient < 5.4.56 / 6.4.50 / 7.4.23 / 8.1.11 | CWE-200・CWE-522 / CVSS 4.0 8.2 | ScopingHttpClient が base_uri との解決の**前に**既定スコープの `auth_bearer` などをマージ → `//evil.example/x` (ネットワークパス参照) が別オリジンになっても認証情報を付けて送信 | [64c34e8](https://github.com/symfony/symfony/commit/64c34e85bd03b3f8a735d8e1af393659dda91d7c) | 水平展開の候補 (URL 解決とスコープ判定の順序) |
| CVE-2026-63395 | isomorphic-git < 1.38.6 | CWE-22・CWE-59 / 8.8 | `git.checkout` が、先頭のディレクトリがシンボリックリンクかを確かめずに子のパスへ書き込む → 悪意のあるリポジトリが symlink を置いた後に子ファイルを追加 → 作業ツリーの外に任意のファイルを書き込み | [823843d](https://github.com/isomorphic-git/isomorphic-git/commit/823843d1cd19182df79bc907c767f5bcecb39a0b) | 水平展開の候補 (Git の独立実装) |
| CVE-2026-121939 | Databasement < 1.10.9 | CWE-290 / CVSS 4.0 9.2 | `findOrCreateLocalUser()` が OIDC の ID を `email_verified` を見ずにメールアドレスでローカルユーザーに結び付ける → 被害者のアドレスで IdP に登録 → super-admin を含む任意のアカウントの乗っ取り (パスワード再設定後も維持) | [b7f4079](https://github.com/David-Crty/databasement/commit/b7f4079c02b7ce3f1cf2844de182e809636c3382) | 水平展開の候補 (OIDC の自動連携) |
| CVE-2026-82033 | DeepSeek Harness < 0.1.2-alpha.2 | CWE-306 / CVSS 4.0 8.6 | ローカルの HTTP / WebSocket の RPC に認証がない → 別ユーザーのプロセスが `session.prompt` でエージェントの bash を実行、`/api/respond` で ID の一致だけで承認を迂回 | [3e24087](https://github.com/deepseek-ai/deepseek-harness/commit/3e24087bfaeabe40b58ba2f7b936895b8f93fe27) | AI エージェント基盤 |
| CVE-2026-68524 ほか 20 件超 | Apache OFBiz < 24.09.08 | — / (Apache の評価: critical を含む) | 攻撃者が指定した screen definition の読み込みによる未認証の RCE (68524)、保存済みビューの認可迂回で RCE (73578)、`renderLink` がリンクのパラメータを FreeMarker として評価 (82910) など | [oss-security](https://seclists.org/oss-sec/2026/q4/516) (commit 不明) | 未認証 RCE / OFBiz は過去に KEV 入りの実績 |
| CVE-2026-57154 | OPNsense < 26.1.11 / 26.4.1p1 | CWE-74・CWE-93 / 8.1 | 1 行を想定した設定欄 (dnsmasq の `dhcp_boot.filename` など) に CR/LF を入れられる → 特権サービスの設定ファイル (`dnsmasq.conf` ほか OpenVPN・DHCPv6 など) に任意の指示行を追加 | [52b18e6](https://github.com/opnsense/core/commit/52b18e67a9ec4596a64ac3a53f3aa102ced55293) | 水平展開の候補 (設定テンプレートへの改行注入) |
| CVE-2026-54161 | Network UPS Tools 2.8.3〜2.8.5 (upsmon) | CWE-78 / 8.1 | サーバーが返す `ups.alarm` の文字列を `notify()` / `wall()` のシェルコマンドにそのまま埋め込む → 悪意のある / 侵害された UPS サーバーから upsmon (多くは root) で任意コマンド実行 | [98e073d](https://github.com/networkupstools/nut/commit/98e073d4cc31f9c73e2fa0c2677540487d902fe7) | 条件付き (NOTIFYCMD + EXEC の設定時) |
| CVE-2026-121007 | Perl SQL::Abstract 1.90_01 〜 2.000001_04 未満 | CWE-89 / — | 識別子の位置 (select リスト、ORDER BY、GROUP BY など) に置いた入れ子の文 `{ -select => ... }` では、where の値も識別子扱いになる → バインドされずに SQL 文に直接展開 → SQLi | [79fc34e](https://github.com/dbsrgits/sql-abstract/commit/79fc34e874b4edb441154eccddb04c57d5c1c90e) | DBIx::Class 経由で利用が広い |
| CVE-2026-63469 / 63470 / 63471 | fastapi-code-generator < 0.8.1 | CWE-94 / 9.3 | OpenAPI のパス・summary・応答コードを、エスケープせずに生成コードの文字列リテラルやデコレーターに埋め込む → 悪意のある OpenAPI ファイルから生成したアプリで任意コード実行 | [49301db](https://github.com/koxudaxi/fastapi-code-generator/commit/49301dbdb82170d7f50877419d994b05cb1fa2bc) | 水平展開の候補 (コード生成器全般) |
| (CVE 申請中) | libtar (Debian 1.2.20-8+deb12u1 を含む) | — / — | GNU long-name の長さが 512 の倍数で NUL がないと終端されない → `safer_name_suffix()` が C 文字列として読む → ヒープの範囲外読み出し (CVE-2021-33643/33644 の修正漏れ) | [oss-security](https://seclists.org/oss-sec/2026/q4/515) (commit 不明、上流は保守停止) | 不完全な修正 |

**今日の CVE 所感**:
- 今日いちばん多いのは「**処理の順序**」のバグだ。Symfony は URL の解決の前に認証情報をマージし、WordPress (KEV) は更新中のファイルが見える時間を作り、APT は再試行でハードリンクを使い回し、Xen は再検証の前にキャッシュを信じた。diff を読むときは「チェックと使用の間に何が挟まるか」に注目するとよい。
- **水平展開の候補**: (1) Symfony 型の「スコープ付き HTTP クライアント + 相対 URL」は、Guzzle の `base_uri`、axios の `baseURL`、Go の `url.ResolveReference` を使う自作ラッパーで同じ形になりやすい。`//host` で試す価値がある。(2) isomorphic-git 型の symlink 経由の書き込みは、Git の独立実装 (go-git、JGit、dulwich、gitoxide) で繰り返し見つかっている。(3) Databasement 型の `email_verified` の未確認は、OIDC の「メールアドレスで既存アカウントに自動連携」をする SaaS で定番の指摘事項だ。
- **コード生成器への注入** (fastapi-code-generator) は、OpenAPI や GraphQL のスキーマから SDK を生成する CI で、「スキーマを外部から受け取る」場合に効く。生成器の出力をそのままビルドするパイプラインは診断の盲点になっている。
- 優先して見る製品: Rails (Active Storage を使うすべての案件)、Debian/Ubuntu のビルド基盤、Xen ベースの VPS 事業者、OFBiz (未認証 RCE が多数)。

## 日本国内のセキュリティ動向

### 国内インシデント・事故

#### [2026-11-02〜05] [続報] アララ「アララ メッセージ」: 流出の可能性は約 7,700 万件のメールアドレスに。共用環境から契約企業のサーバーへ侵入し、悪用も確認
- **前回から何が変わったか**: アララは 11/2 の第 2 報で、被害を 3 つの区分に整理した (区分間で重複がありうるため合算していない)。メール配信サービスで約 7,700 万件のメールアドレスが流出した可能性があり、影響を受けた契約企業は最大約 380 社と推計している。企業によっては氏名や住所も含まれる。10/28〜30 には、アララのシステムからクレジットカード会社を装うメールが最大約 713 万通送られた。10/27 8:36 に偵察とみられるアクセスがあり、原因は第 1 報の「Web サーバーの脆弱性」に加えて「システム環境の問題」も関係していたと更新した。侵入の開始時期と経路は調査中 (piyolog)。
- **なぜ重要か**: 共用の配信基盤 1 つから数百社の顧客リストに広がった。今月はユミルリンクの Cuenote に続き、メール配信 ASP が 2 件目になる。委託先の配信 SaaS の API キーや管理画面のパスワードは、委託元の側でも即時に無効化できるようにしておく必要がある (評価)。
- 出典: [piyolog](https://piyolog.hatenadiary.jp/entry/2026/11/05/015717) / [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2611/04/2000002866/)

#### [2026-11-02〜03] アソビュー (約 1,582 万件) とビックカメラ・コジマ・ソフマップ (3 社で約 1,490 万件): アララへの不正アクセスで委託元も相次いで公表
- **何が起きたか**: アソビューは 11/3、アララ メッセージで配信した会員の情報 1,582 万 1,184 件が流出したと発表した。メールアドレスや氏名に加え、会員 ID、最終ログイン日、郵便番号、チケットの購入日時・種類・枚数・参加人数、キャンセルの有無まで含む。11/2 に報告を受け、全配信を止め、管理画面のパスワードと API キーを無効化した。ビックカメラ、コジマ、ソフマップは 11/2、メールマガジン登録者のメールアドレスなど 3 社で約 1,490 万件が流出した可能性があると発表した (カード情報と通販のログイン情報は対象外)。
- **なぜ重要か**: アソビューの例は、配信のために渡した「セグメント用の属性」(利用施設、参加人数など) がそのまま流出した。配信 ASP に必要以上の属性を連携していないかは、委託元のデータの最小化の問題だ (評価)。
- 出典: [ITmedia NEWS (アソビュー)](https://www.itmedia.co.jp/news/article/2611/04/2000002854/) / [ITmedia NEWS (ビックカメラ G)](https://www.itmedia.co.jp/news/article/2611/04/2000002866/)

#### [2026-11-04] [続報] 良品計画: MUJI Card のカード番号全桁など約 109 万件も流出の可能性。「2021 年 7 月までの会員の情報がシステムに残っていた」
- **前回から何が変わったか**: 良品計画は 11/4、10/30 に公表した MUJI アプリへの不正アクセスで、当初は対象外としていたクレジットカード情報や氏名・住所にもアクセスされた可能性があると発表した。新たに対象になったのは、2021 年 7 月までに入会した MUJI Card (クレディセゾン発行) の会員 約 109 万件で、カード番号の全桁、MUJI Card ID、生年月日を含む。有効なカードは約 34.5 万件。名義・有効期限・セキュリティコードは含まない。当時、独自の特典のためにカード番号を取得していた情報が残っていた。
- **なぜ重要か**: 「使わなくなったデータを消していなかった」ことが被害を大きくした典型例。カード番号全桁の保持は PCI DSS の観点でも問題になりうる。診断で DB のスキーマを見られる場合、使われていないカラムの棚卸しも価値がある (評価)。
- 出典: [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2611/04/2000002885/)

#### [2026-11-02〜04] プレステージ・コアソリューション: ロードサービスの業務システムに不正アクセス、最大 550 万件。ソニー損保、アクサ損保、ENEOS などが公表
- **何が起きたか**: プレステージ・インターナショナルは 11/2、10/29 にグループの業務システムで不正アクセスを検知し、不正に使われた認証情報を無効化したが、その後もアクセスが続いたため 10/30 にシステムを止めたと発表した。子会社のプレステージ・コアソリューション (PCS) が損保会社や自動車メーカー・ディーラーから受託しているロードサービスなどの個人情報が、最大 550 万件持ち出された。氏名、住所、電話番号、メールアドレス、ナンバープレートや車台番号、事故・故障の受付情報、一部は金融機関の口座情報を含む。ソニー損保、アクサ損保、ENEOS、日本カーソリューションなども公表した。
- **なぜ重要か**: 認証情報を無効化しても侵入が続いた点から、別の永続化の手段が残っていたとみられる (評価)。事故の受付情報と車両情報の組み合わせは、保険金詐欺や「事故の連絡」を装う詐欺に使われやすい。
- 出典: [INTERNET Watch](https://internet.watch.impress.co.jp/docs/news/2153279.html)

#### [2026-11-03] セブン-イレブン「7NOW」の利用者情報 16 万件超と出前館の約 800 件: 配送委託先 CBcloud の「ピックゴー」に不正アクセス
- **何が起きたか**: セブン-イレブン・ジャパンは 11/3、7NOW の一部の配達を委託している CBcloud の配送プラットフォーム「ピックゴー」が不正アクセスを受け、届け先の氏名 (カナ) 16 万 4,180 件などが取得されたと発表した。氏名と住所の組み合わせが 4,762 件、さらに電話番号と郵便番号まで揃ったものが 209 件。出前館も同日、約 800 件の漏えいを発表した。不正アクセスは 11/1 に CBcloud の調査で判明した。
- **なぜ重要か**: 配送マッチングの基盤は、多数の荷主の届け先を 1 か所に集める。荷主ごとのデータ分離 (テナント分離) の欠陥がないかが、この種の SaaS の診断の中心になる (評価)。
- 出典: [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2611/04/2000002852/)

#### [2026-11-03] デニーズアプリ: 旧アプリからの移行処理を悪用され、第三者が認証情報を「作成」。旧アプリの利用者の情報が漏えいした可能性
- **何が起きたか**: デニーズジャパンは 11/3、旧デニーズアプリから新アプリへの移行のシステム処理で、第三者が認証情報を不正に作成し、一部の利用者のアカウントにアクセスできる状態だったと発表した。漏えいの可能性があるのは、会員コード、メールアドレス、生年月日、性別、都道府県、お気に入り店舗、キッズバースデー (子どもの誕生日)。確認できたのは 10/7 のアクセス記録で、他の期間は調査中。10/30 に判明し、同日に改修、10/31 に不正な認証情報を無効化した。
- **なぜ重要か**: 「アカウント移行・引き継ぎ」の API は、本人確認を簡略化しがちな典型的な弱点だ。アプリの診断で、引き継ぎコードや移行用のエンドポイントが他人の会員コードで通らないかは、必ず見るべき項目になる (評価)。
- 出典: [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2611/04/2000002878/)

#### [2026-11-02〜04] [続報] GMO ペイメントゲートウェイ: カード発行支援の API サービスで「不正なユーザーによる行為」。Vプリカ 69 件、うち 3 件は番号・セキュリティコード・有効期限・氏名がそろって流出の可能性
- **前回から何が変わったか**: 10/31〜11/2 号ではライフカードが「委託先」とだけ公表していた。委託先は GMO ペイメントゲートウェイの「イシュイングサポートサービス」(カード発行や取引処理の機能を API で提供) で、10/30 に「不正なユーザーによる行為」が発生したと 11/2 に発表された。内訳は、氏名・メール・電話・住所の一部が 63 件、Vプリカ番号 (16 桁)・専用のセキュリティコード・有効期限・氏名が 3 件、番号の一部が 3 件。3 件は不正利用を確認しておらず、10/31 に退会処理した。
- **なぜ重要か**: 「不正なユーザー」という表現から、正規の利用者 (加盟店や発行体のアカウント) による API の悪用が疑われる (評価)。API の認可が利用者の範囲を正しく絞っているか (BOLA) の問題である可能性がある。
- 出典: [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2611/04/2000002850/) / [INTERNET Watch](https://internet.watch.impress.co.jp/docs/news/2153282.html)

#### [2026-11-04] 静岡県: 県立高校 6 校で生徒指導要録 (学籍に関する記録) 621 人分が所在不明
- **何が起きたか**: 静岡県によると、6/30 に卒業生から単位修得証明書の発行申請があり、確認したところ 1 校で卒業生 55 人分の生徒指導要録が見つからなかった。全県立学校を調べた結果、さらに 5 校で 566 人分が所在不明だった (Security NEXT)。
- **なぜ重要か**: サイバー攻撃ではないが、紙の長期保存文書の管理は、自治体・教育機関の監査で必ず問われる (評価)。
- 出典: [Security NEXT](https://www.security-next.com/192171)

### 国内の注意喚起・ガイドライン・政策

#### [2026-11-04] NTT の島田社長、攻撃者側のサイトへの接続遮断 (ブロッキング) について「緊急避難の整備などが重要」と法制化を要望
- **何が起きたか**: GMO インターネットグループへの不正アクセスで、政府が攻撃者側の Web サイトへの接続を遮断するよう通信事業者に要請した件について、NTT の島田明社長は 11/4 の決算会見で、刑法上の緊急避難の整備などが重要だと述べた。ブロッキングは「利用者保護と通信の秘密を両立させる必要がある」とし、遮断が認められる事案を想定した事前のガイドラインが必要だとした。あわせて、「最先端モデルは国内になく、海外にアクセスしないといけない」として、国内で管理・運用できる AI の整備も求めた。
- **なぜ重要か**: 10/1 に根拠法が施行された能動的サイバー防御の運用で、通信事業者が法的な根拠の明確化を公に求めた。ブロッキングの範囲の議論は、今後の C2 やフィッシングサイトへの対処の方法に直結する (評価)。
- 出典: [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2611/04/2000002877/)

#### [2026-11-03] チームみらいの安野党首「海外のオープンウェイトモデルを自前のサーバーで動かしても 100% 安全ではない」。国産のサイバーセキュリティ AI モデルの必要性を主張
- **何が起きたか**: チームみらいの安野貴博党首は 11/3 の生配信で、海外製のオープンウェイトモデルが国内で動くとき、意図的に性能を落としたりデータを漏らしたりする可能性があると指摘した。同党は 10/23 にデジタル庁へ提出した提言で、オープンウェイトモデルの検証環境と計算資源を国が提供し、「国産サイバーセキュリティ AI モデル」の開発を支援すべきだとしている。
- **なぜ重要か**: 上の NTT の発言と同じく、「攻撃に使える水準の AI を国内で持てるか」が政策の論点になってきた。モデルの重みに仕込まれたバックドアの検証は、まだ確立した手法がない (評価)。
- 出典: [ITmedia AI+](https://www.itmedia.co.jp/aiplus/article/2611/04/2000002853/)

#### [2026-11-04] NEC、Aterm の設定画面の「.php」は「PHP の一部の仕様を参考にした独自ソフト」と説明。PHP の緊急脆弱性 (PHP2Shell) の影響なし
- **何が起きたか**: NEC は 10/26 に、Aterm の設定画面の URL に `/index.php` と表示されても PHP は使っておらず、PHP の脆弱性の影響はないと告知した。ITmedia の取材に対し、PHP の文法の一部を解釈・処理するよう独自に実装したソフトで、PHP 本体の実装は流用していないと説明した。言語などの詳細は明らかにしていない。
- **なぜ重要か**: 「URL の拡張子だけで技術スタックを判断する」スキャナーの誤検知の例として覚えておくとよい。一方、独自実装の PHP 風インタプリタは、それ自体が別の攻撃面になりうる (評価)。
- 出典: [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2611/04/2000002847/)

> 注: JPCERT/CC の注意喚起、IPA の重要なセキュリティ情報、NISC (国家サイバー統括室)、個人情報保護委員会では、11/3〜5 の新規の発表を確認できなかった (JPCERT/CC の注意喚起の最新は 10/29)。

### 国内製品の脆弱性 (JVN)

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| 2026-11-04 | JVN#46901199 / CVE-2026-109849 | Hinemos (NTT データ先端技術) | 一般ユーザーに付与できる特定の権限でパスワード変更 API を呼ぶと、管理者のパスワードを変更できる (CWE-266)。報告は三井物産セキュアディレクションの野口晋義氏 | v4 7.1 / v3 6.5 | [JVN](https://jvn.jp/jp/JVN46901199/) |
| 2026-11-04 | JVN#12040144 | Airbyte 1.7.0〜2.1.0 | 安全でないリフレクション (CWE-470)。Connector Builder のカスタムコンポーネントで、unsafe code を無効にしていてもクラスを読み込めて任意コード実行 | v4 8.7 / v3 8.8 (緊急) | [JVN](https://jvn.jp/jp/JVN12040144/) |
| 2026-11-04 | JVN#44272550 / CVE-2026-105296 | Akeeba Backup for Joomla! < 10.3.7、for WordPress < 9.1.8、Akeeba Solo < 9.1.8、Admin Tools for Joomla! < 7.9.0 | 一部の操作で CSRF 対策がない (CWE-352)。ログイン中の管理者に細工したページを踏ませると意図しない操作 | v4 5.1 / v3 5.4 | [JVN](https://jvn.jp/jp/JVN44272550/) |
| 2026-11-04 | JVNVU#99859918 (VU#203719) | INFINITT Healthcare INFINITT PACS System Manager | 複数の任意コード実行の脆弱性 (医用画像管理) | 任意コード実行 | [JVN](https://jvn.jp/vu/JVNVU99859918/) |
| 2026-11-04 | JVNVU#92281274 (VU#124705) | Android アプリ「BaseChat - Audio Dating App」9.8.1 | 複数の脆弱性 | 詳細は VU#124705 | [JVN](https://jvn.jp/vu/JVNVU92281274/) |
| 2026-11-04 | JVNVU#91151184 | CISA ICS / ICS Medical Advisory (2026-11-03 公開分) | CISA が 11/3 に公開した制御システム・医療機器の advisory の日本語での取りまとめ | 製品ごと | [JVN](https://jvn.jp/vu/JVNVU91151184/) |

### 国内コミュニティ・研究・イベント

#### [2026-11-04] GMO Flatt Security の RyotaK 氏、Rails Active Storage の Critical な欠陥 (GHSA-f3w6-w445-fwh9) を報告
- **何が起きたか**: 今日の深掘りの欠陥は、HackerOne 経由で RyotaK 氏 (GMO Flatt Security) が報告した。
- **なぜ重要か**: 国内の研究者が、主要な Web フレームワークの Critical を報告した例。同社のブログで技術的な解説が出れば、バリアントハントの手がかりになる (評価)。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/critical-rails-flaw-lets-attackers.html)

#### [2026-11-04] Cybozu PSIRT Monthly (2026 年 10 月号): 「相次ぐ Web システムからの情報漏えい」を取り上げ。API の権限不備や「返しすぎる API」を狙う攻撃
- **何が起きたか**: サイボウズの PSIRT が 10 月に社内で共有した話題をまとめた。冒頭で、マクニカのブログ「2026 年 7 月以降に増えている国内の Web システムからの情報漏えい」を紹介している。共通ソフトの脆弱性だけでなく、API のアクセス権限の不備や、必要以上の情報を返す API など、サイト固有の実装の問題を狙った攻撃が確認されているという。
- **なぜ重要か**: 今週の国内事案 (デニーズの移行処理、GMO-PG の「不正なユーザー」、7NOW の配送基盤) と重なる。診断の観点として、脆弱性スキャンより API の認可テストを厚くすべき時期であることを示す (評価)。
- 出典: [Zenn (Cybozu PSIRT)](https://zenn.dev/cybozu_psirt/articles/0af2c7b3c02617)

#### [2026-11-04] Zenn: 「ダウンロードフォルダの AGENTS.md 攻撃」を受けて、Claude Code の設定を 1,576 本の会話記録から点検した記事
- **何が起きたか**: 個人開発者が、10/22 に Forever Security が報告した事例 (Mac のダウンロードフォルダに置かれた悪意のある `AGENTS.md` を読んだコーディングエージェントが、悪意のある npm パッケージを入れようとした) を受けて、自分の `CLAUDE.md`・`AGENTS.md`・`.claude/settings.json` を点検した。`permissions.deny` が 0 件だったため、直近 14 日の会話記録 1,576 本で実際の利用状況を調べてから禁止ルールを設定した手順を公開している。
- **なぜ重要か**: 上の「プロンプトアドウェア」と同じく、指示ファイルが攻撃の入口になる。開発端末の診断のチェックリストとしてそのまま使える (評価)。
- 出典: [Zenn](https://zenn.dev/d_aiba1/articles/claudecode-agents-md-mac-settings-check)

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 63 (RSS/Atom 62 本 + NVD API、CISA KEV JSON、EPSS API、Rails Discourse API。記事本文は curl で約 90 本)
- 採用件数: AI技術=12 / AIセキュリティ=7 / セキュリティ=18 / CVE=14 / 国内インシデント=8 / 国内政策=3 / JVN=6 / 国内コミュニティ=3
- 除外理由内訳 (概数): 古すぎ=約 20 (ScanNetSecurity の 11/4 掲載分のうち、元の公表が 11/2 以前のもの: チャリロト、ドラとら、Value Card、トラベルジップ、東京都水道局、ELESTYLE、くみあいアプリなど / NRI セキュアの SCS 評価制度ガイド 10/29 / JVN の Core Temp 11/2 など) / 重複=約 30 (Binance の経緯、cPGuard、LLMjacking の GTIG 報告、3AM、XCPE ボットネット、Barracuda ESG、BTCPay、Synology、VasyGrek、Gorbag、Node-RED、外務省、ノジマ、@cosme、セガ フェイブ、クラブツーリズム、Copilot Fusion、Octoverse、Anthropic の S-1/A など) / 日付不明=約 3 (日立 HA8000V の HA モニタオプションは ScanNetSecurity の掲載のみでベンダーの公表日を確認できず除外)
- 取得失敗ソース:
  - `api.github.com` の advisories と `github.com` の HTML は 403 (セッションのリポジトリ制限)。Rails の修正コミットは The Hacker News の記事内リンク、advisory は Rails の Discourse API と oss-security で代替した。
  - openai.com の記事本文は取得できず、RSS の要約で代替 (Pierre の買収、Daybreak Red、Pando)。
  - SentinelOne Labs (Vercel のチェックポイント)、DeepMind ブログ (本文抽出失敗)、ScanNetSecurity の記事本文 (抽出失敗)、Trend Micro・JC3・MSRC・日経クロステックの RSS (空)、OSV の Rails GHSA (未登録)。
  - Anthropic の News RSS は 0 件だったため、FlashProve は TechCrunch と ITmedia で裏取りした。
  - CISA KEV は 11/3 版 (dateReleased 2026-11-03T20:00Z) で、期間内の追加は CVE-2026-119977 の 1 件のみ。
  - WebSearch は 11 月の AI モデル発表について有効な結果を返さなかった (トラッカー系の古い情報のみ)。

</details>
