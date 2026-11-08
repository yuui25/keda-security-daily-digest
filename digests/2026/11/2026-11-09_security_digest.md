# KEDA Daily Digest — 2026-11-09 (JST)

> 採用範囲: 公開日 2026-11-07 〜 2026-11-09
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

- **AI 側**: 週末で、大きなモデルの公開はなかった。話題はインフラとエージェントに集まった。
  - Anthropic は、ガス発電機 1.7 GW 分を 34 億ドルで押さえたと FT が報じた。Crusoe は、建設中のワイオミングのデータセンターを Google に売った。
  - Apple は Siri を「他社のアプリまで操作するエージェント」にする計画を急いでいると、Bloomberg が報じた。
  - DeepSeek のエージェント基盤 Harness は、1 日の利用者が 154 万人に達した。llama-modchip は、284B の DeepSeek-V4-Flash を GPU なし・RAM 64GB で動かした。
- **AI セキュリティ**: Alex Stamos 氏 (Cognition の CSO) は、オープンウェイトのモデルで攻撃の大部分が自動化されたと述べ、防御側の「暗黒時代」を予告した。Railway の技術者が、競合の Primcloud に対して AI エージェントを動かしていた件も表に出た。中身は、他の顧客の秘密情報の要求、IMDS への接続、内部のスキャンだった。CVE では、Skyvern (`types.CodeType` でサンドボックスを抜ける) と Dify (Squid に宛先の制限がない SSRF) という、AI 基盤そのものの欠陥が出た。
- **セキュリティ側**:
  - IBM API Connect の一括修正 (v12.1.1.3) で、NVD に約 200 件の CVE が一度に載った。ハードコードされた資格情報や署名検証の回避など、9.8〜9.9 が並ぶ。
  - WordPress コアの更新中の競合状態 (KEV) への攻撃の試行は、24 万回を超えた (Wordfence)。
  - SANS ISC は、sshole の最初の実際の攻撃を 11/5 に観測した。
  - UnrealIRCd は、AI を使った内部の監査で見つけた「15 年で最も深刻」な欠陥を、ホットパッチで直した。
- **国内**: 週末も公表が続いた。
  - teket (電子チケット): 全会員の氏名とメールアドレスに加え、発券用コードも流出した。
  - シグナルトーク「Maru-Jan」: 全会員 185 万 5,578 人分のメールアドレスとパスワードが流出した。
  - 使えるねっと: 契約管理のポータルが破られ、VPS 127 件と共有サーバーにも及んだ。
  - アララの件では、委託元の確定値の公表が続いた (成城石井 173,590 件ほか)。
- **今日まず見るべき 1 件**: 深掘りの **Contact Form 7 の未認証ファイルアップロード (CVE-2026-114432)**。有効なインストールは 1,000 万以上ある。PoC は 11/19 に公開される予定で、診断先の WordPress の版を確認する猶予は 10 日しかない。発見者は国内の研究者だ。次点は **OpenAM 16.1.4 の 3 件** (未署名の SAML アサーションを受け入れる 9.8 ほか)。

## 今日の深掘り

### Contact Form 7 6.2.3 以前に未認証のファイルアップロード (CVE-2026-114432)。Debian / Ubuntu の Apache の既定の構成では RCE になる。PoC は 11/19 に公開予定

- **概要 (事実)**:
  - WPScan は 11/5、WordPress のフォームプラグイン Contact Form 7 (有効なインストールは 1,000 万以上) の 6.2.4 未満に、未認証のファイルアップロードがあると公開した。NVD には 11/8 に CVE-2026-114432 として載った。
  - WPScan によると、欠陥は 2 つの組み合わせだ。1 つは、フォームのファイル欄に送られたファイルの種類や拡張子を確かめないこと。もう 1 つは、一時ファイルの後片付けの不備で、アップロードしたファイルがディスクに残ること。
  - Debian / Ubuntu の Apache の既定の構成では、ディレクトリの一覧が出て、`.phar` も PHP として実行される。そのため、残ったファイルを見つけて実行でき、RCE になる。nginx や、`.htaccess` が有効な Apache では、uploads 配下に任意のファイルを書けるだけになる。ただし、HTML や SVG をサイト自身のオリジンから配信させることはできる。
  - 発見者は Shinya Murakami 氏 (@4n86rakam1)。PoC は 11/19 に公開される予定。修正版の 6.2.4 は、10/29 より前に配布済み (最新は 6.2.4.1)。
- **技術的な中身 (WordPress.org の SVN で 6.2.3 と 6.2.4 のタグを比べて、自分で読んだ範囲。PoC の手順は公開されていないので、一部は推定)**:
  - **拡張子の検査が denylist だった**: 6.2.3 の `wpcf7_antiscript_file_name()` は、拡張子を `^(php|phtml|pl|py|rb|cgi|asp|aspx)\d?$` に一致するかで判定し、一致したものにだけ `_.txt` を付けていた。`.phar`、`.pht`、`.shtml`、`.html`、`.svg` は、そのままの名前で保存される。6.2.4 は allowlist に変えた。音声・動画・画像の MIME から作る拡張子と、`pdf`、`txt` だけを残し、それ以外には `_.txt` を付ける。あわせて、Unicode の空白 (U+3000、U+FEFF など) を正規化する処理を足した。
  - **後片付けの対象から外れる経路**: `wpcf7_unship_uploaded_file()` は、1 つの欄に送られた複数のファイルを、順に一時ディレクトリ (`wpcf7_uploads/<ランダムなディレクトリ>/`) へ移す。6.2.3 は、途中で 1 つでも `move_uploaded_file()` に失敗すると `WP_Error` だけを返し、それまでに移したファイルの一覧を返さなかった。呼び出し側の `submission.php` は、エラーのときは `add_uploaded_file()` を呼ばない。その結果、移し終えたファイルは、送信後の削除の対象にも、後段の `filetypes` の検査 (`wpcf7_validate_file` フィルタ) の対象にもならず、残る。6.2.4 は一覧を参照渡し (`&$uploaded_files`) にし、エラーでも途中までのファイルを登録するように直した。
  - **RCE までの経路**: CF7 は一時ディレクトリに deny の `.htaccess` を置く。しかし Debian / Ubuntu の Apache は既定で `AllowOverride None` なので、これは効かない。`Options Indexes` が有効ならランダムなディレクトリ名も一覧から分かり、`.phar` を PHP のハンドラーが実行する。WPScan の説明はこの経路と一致する。
  - **結果**: 未認証で Web サーバーの権限による任意コード実行。フォームに 1 つでもファイル欄があれば、攻撃面になる。
- **背景・経緯 (過去の事例の引用)**:
  - CF7 には 2020 年 12 月にも、ファイル名の扱いの不備による無制限のアップロード (CVE-2020-35489、5.3.2 で修正) があった。`wpcf7_antiscript_file_name()` は、そのころから「危険な拡張子を潰す」denylist の方式で強化されてきた。今回の 6.2.4 は、その方式を allowlist に改めた形だ。
  - WordPress では、今月だけでも、コアの更新中の競合状態 (CVE-2026-119977、KEV) や、多数のプラグインの任意ファイルアップロード (下表の外でも、Wordfence / WPScan の公開が続いている) が出ている。
- **なぜ今これが重要か (評価)**:
  - 設置数が桁違いで、日本の企業サイトや自治体のサイトでも、問い合わせフォームの定番だ。CF7 の作者も日本の開発者 (Rock Lobster Inc.) で、国内での利用は特に多い。
  - PoC の公開予定日 (11/19) が決まっているので、攻撃が自動化される時期を予測しやすい。WordPress のコアの件 (既報、下記の続報) では、10/28 以降に 24 万回を超える試行が観測された。同じ速さを想定するのが安全だ。
  - 診断では、「ファイル欄があるか」と「Apache の構成 (`AllowOverride` / `Indexes` / `.phar` の扱い)」を確かめれば、影響を判断できる。修正前の版の denylist と後片付けの順序の問題は、ほかのフォームプラグインにもありそうな型だ。
- **読者が今日できること**:
  - 診断先と自社のサイトで版を確かめる: `wp plugin list --name=contact-form-7 --fields=name,version`。外からは `/wp-content/plugins/contact-form-7/readme.txt` の `Stable tag` を見る。6.2.4 以上なら修正済み。
  - 侵害の痕跡を探す: `find wp-content/uploads/wpcf7_uploads -type f ! -name '*.txt' -newermt 2026-10-01`。`.phar`、`.pht`、`.html`、`.svg` が残っていれば要注意。アクセスログでは、`wpcf7_uploads/` への GET と、`/wp-json/contact-form-7/v1/contact-forms/*/feedback` への multipart の POST を突き合わせる。
  - 横に広げる: 自分が診断する他のフォームプラグイン (WPForms、Forminator、Ninja Forms、MW WP Form など) で、「拡張子が denylist か」と「エラーの経路でも一時ファイルが消えるか」を、ソースで確かめる。
- 出典:
  - [WPScan (CVE-2026-114432)](https://wpscan.com/vulnerability/6b0a5d1f-84fb-425f-8d37-ddde5703937c/)
  - [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-114432)
  - [6.2.3 → 6.2.4 の差分 (WordPress.org Trac)](https://plugins.trac.wordpress.org/changeset?old_path=%2Fcontact-form-7%2Ftags%2F6.2.3&new_path=%2Fcontact-form-7%2Ftags%2F6.2.4)
  - [SVN tags](https://plugins.svn.wordpress.org/contact-form-7/tags/)

## AI 技術・トレンド

### [2026-11-08] Apple、Siri を「他社のアプリまで操作するエージェント」にする計画を急ぐ。iOS 27.3 のベータには、HomeView にチャットボットを入れる手がかりも (Bloomberg / The Verge)
- **何が起きたか**:
  - Bloomberg の Gurman 氏によると、CEO の John Ternus 氏が、AI の責任者 Craig Federighi 氏に Siri の強化を急がせている。
  - 予定は 3 段階だ。iOS 27.3 では、写真の切り抜きや Safari のタブの整理など、Apple 自身のアプリを細かく操作できるようにする。春には、Grubhub での注文や OpenTable の予約など、他社のアプリの操作を加える。早ければ来年に、目標を追い続ける常駐型のエージェントを、iOS 28 の刷新と合わせて出す。
  - 別に、iOS 27.3 のベータには、HomeView に「Conversational Apps」という分類のフラグがある。ChatGPT や Claude を加える可能性を示している。
- **なぜ重要か (評価)**: OS の標準のアシスタントが、利用者に代わって他社のアプリを操作するようになる。アプリ内の文章がそのままエージェントへの入力になり、間接プロンプトインジェクションと「権限を借りた代理人 (confused deputy)」の新しい攻撃面ができる。iOS アプリの診断に、「Siri から操作されたときの確認の有無」という項目が加わる。
- 出典: [The Verge](https://www.theverge.com/ai-artificial-intelligence/1029552/apple-siri-ai-agentic) / [Bloomberg](https://www.bloomberg.com/news/newsletters/2026-11-08/apple-explores-turning-siri-ai-into-chatgpt-dots-like-agent-ios-28-shake-up) / [The Verge (HomeView)](https://www.theverge.com/tech/1029526/chatbots-might-be-coming-to-apples-homeview)

### [2026-11-08] Anthropic、ガス発電機 1.7 GW 分を 34 億ドルで押さえたと FT が報道。AI の研究所による発電設備の購入として、知られている中で最大
- **何が起きたか**:
  - FT によると、Anthropic は 9 月下旬、OnePWR Solutions が発注していた Caterpillar の発電機を引き継いだ。当初は OnePWR から電力を買う計画だった。会社そのものは買っていない。
  - Anthropic は発表していない。報道は FT と Bloomberg など。
- **なぜ重要か (評価)**: AI の研究所が電源を自前で持つようになると、データセンターの OT / ICS (発電の制御) が攻撃面に加わる。既報の欧州の冷蔵設備への攻撃のように、制御機器を狙う攻撃者にとって新しい標的になる。
- 出典: [Bloomberg](https://www.bloomberg.com/news/articles/2026-11-08/anthropic-buys-power-for-ai-data-centres-in-3-4b-deal-ft-says) / [TheEnergyMag](https://www.theenergymag.com/news/market-news/anthropic-gas-generation-acquisition-ai-data-center)

### [2026-11-07] Crusoe、建設中のワイオミングのデータセンター計画を Google に売却。Google はこのキャンパスに 170 億ドルを投じる
- **何が起きたか**:
  - Crusoe (評価額 309 億ドル) は、Blackstone が支援する Tallgrass と、最大 10 GW の計画を進めていた。
  - 報道によると、Google は Crusoe のもとでの費用と工期を懸念していた。売却額は明らかにしていない。
- **なぜ重要か (評価)**: 独立系の「ネオクラウド」やデータセンターの開発会社が弱り、AI の計算資源が大手のクラウドに集まりつつある。インフラの供給網のリスクも、少数の事業者に集中することになる。
- 出典: [TechCrunch](https://techcrunch.com/2026/11/06/crusoe-sells-troubled-wyoming-data-center-project-to-google/) / [Crusoe](https://www.crusoe.ai/resources/newsroom/crusoe-wyoming-data-center-campus-update)

### [2026-11-08] DeepSeek のエージェント基盤「Harness」、1 日の利用者が 154 万人に。公式のプラグインストアを計画 (Bloomberg)
- **何が起きたか**:
  - 11/4 時点で、公式 API 経由の 1 日の利用者は 154 万人だった。9 月末は約 27.1 万人だった。
  - 二次情報によると、月間の利用者は 548 万人、トークンは 1 日約 92 兆、第三者のプラグインは約 3.5 万本ある。
  - DeepSeek は、開発者にトークンで報いる制度も計画している。
- **なぜ重要か (評価)**: エージェントの実行基盤のまわりで、プラグインの生態系が急に育っている。npm や VS Code の拡張と同じく、供給網攻撃の標的になる。Harness には、認証のないローカルの RPC の欠陥 (CVE-2026-82033、11-04 号で既報) もあった。公式ストアの審査の仕組みが固まる前の今が、最も危ない時期だ。
- 出典: [Bloomberg](https://www.bloomberg.com/news/articles/2026-11-08/deepseek-s-ai-agent-platform-hits-1-54-million-daily-users) / [RuntimeWire](https://runtimewire.com/article/deepseek-harness-1-54-million-daily-users-plugin-marketplace)

### [2026-11-08] llama-modchip v2.4.0: 284B の DeepSeek-V4-Flash を、GPU なし・RAM 64GB で動かす
- **何が起きたか**:
  - ggml / llama.cpp へのカーネルのパッチと量子化のツールの集まりで、ライセンスは Apache 2.0。
  - DeepSeek-V4-Flash (総 284.33B、アクティブ 13.17B) を 1.71 bpw に量子化すると、GGUF は 56.56 GiB になる。256K のコンテキストでも、メモリの最大使用量は 57.61 GiB だった。
  - 16 コアの Zen 5 で、プリフィルは 44.36 tok/s、デコードは 9.1〜14.7 tok/s。
  - Hacker News で 289 ポイントを集めた。
- **なぜ重要か (評価)**: 前号の Vals の試験では、DeepSeek V4.1 Flash の侵入能力が非公開の最上位モデルに迫っていた。その系統のモデルが、普通の CPU サーバーで、事業者のログにも安全装置にも触れずに動く。下記の Stamos 氏の指摘と同じ流れで、「API の利用を監視して攻撃者を止める」防御は効きにくくなる。
- 出典: [GitHub (synchopate/llama-modchip)](https://github.com/synchopate/llama-modchip)

### [2026-11-09] MCP 公式の Ruby SDK が「MCP SDK Tier 1」に到達。新しいステートレスな接続を含め、仕様をすべてサポート (Publickey)
- **何が起きたか**:
  - MCP の仕様を管理する Agentic AI Foundation (Linux Foundation の傘下) によると、Ruby SDK は、廃止予定のため除外した 2 件を除いて、サーバーとクライアントの適合テストにすべて通った。
- **なぜ重要か (評価)**: Rails のアプリに MCP サーバーを足す例が増えるはずだ。診断では、既存の Rails の認可 (Pundit / CanCanCan) が MCP のツール呼び出しの経路にもかかっているか、が新しい確認項目になる。
- 出典: [Publickey](https://www.publickey1.jp/blog/26/mcpmcpruby_sdkmcp_sdk_tier_1.html)

### [2026-11-07] Meta、商用の利用規約の改定を無期限に延期。リンク先のサイトを AI の学習用にクロールさせ、ペイウォールを越えるための試験用の資格情報まで求める内容だった (Ars Technica)
- **何が起きたか**:
  - 改定案では、ビジネスアカウントの持ち主は、Facebook ページからリンクした外部サイトを Meta にクロールさせる必要があった。法律の専門家は、robots.txt を無視できる文言だと警告していた。
  - ペイウォールのあるサイトには、Meta のボットのための試験用の資格情報を作らせる内容もあった。
  - 改定は 10/30 の予定から 11/20 に延び、今回、無期限に延期された。Meta は Reuters に、既存の規約が引き続き有効だと説明した。
- **なぜ重要か (評価)**: AI のクローラーに資格情報を渡させる設計は、資格情報の管理と、アクセス制御の境界の両方を崩す。自社のサイトで AI のクローラーを「どう識別し、どこまで通すか」を決める必要は、今回の延期とは関係なく残る。
- 出典: [Ars Technica](https://arstechnica.com/tech-policy/2026/11/does-meta-think-we-cant-read-meta-abandons-sketchy-commercial-terms-update/)

### [2026-11-08] Elvis Presley の権利者と Eminem の楽曲出版社が Suno を提訴。テネシー州の「ELVIS 法」を AI 企業に使う
- **何が起きたか**:
  - 2 件の新しい訴訟で、Suno がアーティストに似せた楽曲と歌詞を生成すると主張している。
  - Presley 側は、歌手の声を AI で複製することを禁じるテネシー州の ELVIS Act (Ensuring Likeness Voice and Image Security) を根拠にした。
  - 9 月の Jason Isbell 氏らの訴訟に続くものだ。
- **なぜ重要か (評価)**: 声の複製を規制する州法が AI 企業に向けて使われる、最初期の例になる。声のディープフェイクによる詐欺 (既報の、CEO になりすました 1 億 2,900 万ドルの件) への法的な対抗手段の形にも影響する。
- 出典: [The Verge](https://www.theverge.com/ai-artificial-intelligence/1029533/elvis-eminem-suno-ai-music-clone-lawsuit) / [Engadget](https://www.engadget.com/2310316/suno-ai-music-generator-sued-again-for-copyright-infringement/)

### [2026-11-08] Co-Design Bench: 実際の利用者の変更依頼で、最良のコーディングエージェントでも完全にこなせたのは 26.4% (Alibaba ほか)
- **何が起きたか**:
  - Alibaba とアジアの複数の大学が、既存の Web アプリへの実際の変更依頼からベンチマークを作った。依頼には、画像・音声・動画・文書の入力を含むものもある。利用者が言い直したり、元に戻したりした依頼を優先して選んでいる。
  - 10 モデルのうち最良は GPT-6 Astra だった。要件の平均約 70% は満たしたが、すべてを満たしたのは 26.4% だった。
  - 採点は、ブラウザでアプリを試す AI の審査員が 2 段階で行う。2 段目で、合格の判定がモックアップでごまかしたものでないかを確かめる。
- **なぜ重要か (評価)**: エージェントが書いた変更の約 4 分の 3 には、どこかに未完成の部分が残る。ソースコード診断では、「AI が書いた部分」に入力の検証や認可の抜けが残っていないかを、重点的に見る根拠になる。
- 出典: [The Decoder](https://the-decoder.com/ai-coding-agents-still-need-human-cleanup-on-nearly-three-out-of-four-tasks-in-a-real-world-test/)

### [2026-11-08] [続報] Jensen Huang 氏を狙った諜報の疑い: NVIDIA の取締役会が調査を開始。Huang 氏は従業員に不倫を認めた (Bloomberg)
- **前回から何が変わったか**: 11-08 号は、Megaspeed の幹部が Huang 氏を探るよう勧誘されたという米国の情報機関のメモを扱った。今回、取締役会が「外国の諜報の標的になったか」の調査を始めたこと、Huang 氏が従業員に不倫を認めたことが加わった。記事は有料で、確認できたのはフィードの要約までだ。
- **なぜ重要か (評価)**: AI チップを作る会社の経営者の私生活が、外国の情報機関の足がかりとして狙われた例になる。内部脅威の研修の題材になる。
- 出典: [Bloomberg](https://www.bloomberg.com/news/articles/2026-11-08/nvidia-board-to-probe-spying-case-after-ceo-jensen-huang-admits-infidelity)

### [2026-11-07〜08] 米中間選挙の後、データセンターへの逆風が強まる。英国は「必要なインフラ」として建設を続ける方針
- **何が起きたか**:
  - TechCrunch の Equity によると、住民投票で数十のデータセンターの計画が否決された。テキサス州知事に当選した Gina Hinojosa 氏など、規制を掲げた候補も勝った。Musk 氏は約 5 億ドルを寄付して「ほぼ何も得られなかった」という。
  - 英国の Dan Tomlinson 成長担当相は 11/8、FT に、データセンターは引き続き「必要なインフラ」だと述べた。政府の支援は、地域への投資を条件にする。
- **なぜ重要か (評価)**: 主に立地と政策の話で、セキュリティとの直接の関係は小さい。上の Anthropic の自前の発電や Crusoe の売却と合わせて読むと、計算資源の確保が政治の問題になってきたことが分かる。
- 出典: [TechCrunch](https://techcrunch.com/2026/11/07/after-the-midterms-things-are-looking-rocky-for-elon-musk-and-data-centers/) / [Engadget](https://www.engadget.com/2310304/uk-has-no-plans-to-slow-down-ai-data-center-construction/)

### [2026-11-08] @IT「マルチエージェント設計 15 のパターン」: GitHub、Google、Siemens の知見を図解で整理
- **何が起きたか**: @IT (ITmedia) が、複数のエージェントを組み合わせる設計を 15 のパターンにまとめた。オーケストレーター、パイプライン、合議などを、GitHub、Google、Siemens の公開資料をもとに図解した。
- **なぜ重要か (評価)**: 国内の開発の現場で、マルチエージェントの構成が「普通の設計」として広まりつつある。診断では、パターンごとに「どこで信頼境界をまたぐか」が違う。下記 arXiv の「Signed but Not Safe」が示した、引き継ぎで要件が書き換えられる問題と合わせて読むとよい。
- 出典: [@IT](https://atmarkit.itmedia.co.jp/ait/articles/2611/08/news001.html)

### [2026-11-08] Richard Sutton 氏 (「The Bitter Lesson」の著者)、「計算量だけでは知能にならない」
- **何が起きたか**: Sutton 氏は、経験から学び続ける、世界モデルを持ったエージェントが必要だと主張した。合成データへの依存は「大きな間違い」だと述べた。論評の記事だ。
- **なぜ重要か (評価)**: スケーリングの方針への批判は、前号の Microsoft Research「AI Frontiers」の解散の理由 (規模の拡大だけを追う方針と合わない) とも重なる。業界の研究の方向が分かれつつあることを示す。
- 出典: [The Decoder](https://the-decoder.com/the-inventor-of-the-bitter-lesson-has-a-bitter-lesson-for-llm-scaling-enthusiasts/)

## AI セキュリティ

### [2026-11-07] Alex Stamos 氏 (Cognition の CSO)「AI がサイバーセキュリティの世界を壊した」。オープンウェイトのモデルで攻撃の大部分が自動化され、防御側には「暗黒時代」が来る (The Verge Decoder)
- **何が起きたか**:
  - Stamos 氏は、オープンウェイトのモデルが、生きた標的に対して、バグを見つけてエクスプロイトを書く作業をその場でこなせるようになったと述べた。攻撃の流れ (キルチェーン) の大部分が自動化できるという。
  - 例として、安全装置を外した GLM-5.3 で動かす、中国のオープンソースの ARTEX を挙げた。韓国の 3 つの銀行から始まり、今週さらに約 200 社が被害を受けたとも述べた。
  - 連鎖した事案の説明もあった。Fireworks から盗まれた API キーで Cursor に入り、そこから不正なプラグインが約 5,000 社に配られたという。これは同氏の発言で、各社の公式な確認は取れていない。
  - 本人も、量子化した GLM-5.3 を M5 の Mac Studio で手元で動かしているという。
- **なぜ重要か (評価)**: 10 月の AI 基盤の侵害の連鎖 (Fireworks ほか、既報) を、1 本の供給網の話として語った、実務家の証言だ。攻撃者がログを残す API のモデルから離れていることも裏づけている。発言の中の数字は、一次情報で確かめてから引用したい。
- 出典: [The Verge (Decoder)](https://www.theverge.com/podcast/1029038/ai-cybersecurity-hackers-data-breach-dark-age-alex-stamos)

### [2026-11-07] Railway の技術者が、競合のクラウド Primcloud に AI エージェントを向けていた。他の顧客の秘密情報の要求、IMDS への接続、内部のスキャンまで (Hackread)
- **何が起きたか**:
  - Primcloud の創業者 Josh Manders 氏によると、エージェントは 15 分で約 24 のコマンドを実行した。アプリのコンテナ内の資格情報を使い、他の顧客の分を含むプラットフォームの秘密情報を要求した。クラウドのメタデータのエンドポイントにも接続を試み、内部のデータベースやキャッシュの名前を推測した。Primcloud は、すべて防いだとしている。
  - Railway の技術者 Jake Runzer 氏は、エージェントを動かしたことを認めた。CEO の Jake Cooper 氏は後の声明で、業務外の時間に個人のアカウントと個人のカードで動かした、個人的なバグバウンティ用のツールだったと説明した。
- **なぜ重要か (評価)**: 許可のない「エージェントによる試験」は、外から見ると侵入と区別できない (資格情報の収集、IMDS、内部のスキャン)。診断の業務でも、AI に作業を任せたときに、スコープの外へ出ない仕組みが必要になる。PaaS の運用者にとっては、おとりの資格情報 (カナリア) を置く理由になる。
- 出典: [Hackread](https://hackread.com/railway-engineer-run-ai-agents-rival-cloud-platform/) / [Security Boulevard (11/3 の第一報)](https://securityboulevard.com/2026/11/ai-agents-used-by-railway-breach-systems-of-rival-primcloud/)

### [2026-11-07] 社内のメール、Slack、チケットを AI の学習用に買い取る仲介業者。1 社あたり 35 万〜200 万ドルを提示 (WIRED)
- **何が起きたか**:
  - 仲介業者は WIRED に、過去の業務記録に一括で 35 万〜180 万ドル、通話の文字起こしを含めると最大 200 万ドルを払うと持ちかけた。売り先は Anthropic や OpenAI などの研究所だという。
  - 閉鎖するスタートアップのデータを「洗浄・匿名化」して研究所に仲介する、Sunset という会社もある。
- **なぜ重要か (評価)**: 第三者の個人情報や秘密情報を含む社内データが、売却や会社の清算の経路で外に出る。DLP と委託先との契約に加え、「匿名化」がどこまで本物かを確かめる必要がある。秘密情報が学習データに入ると、取り出す研究 (抽出攻撃) の対象にもなる。
- 出典: [WIRED](https://www.wired.com/story/ai-companies-really-really-want-to-buy-your-work-files-and-emails/)

### [2026-11-06〜07] AI 基盤の欠陥が続く: Skyvern は `types.CodeType` でサンドボックスを抜けられ、Dify は Squid に宛先の制限がない SSRF
- **何が起きたか**:
  - ブラウザ操作エージェントの Skyvern (1.0.56 以前、CVE-2026-123783、8.8) では、認証済みの利用者が、生のバイトコードから `types.CodeType` で関数を組み立てられた。AST の denylist (`is_safe_script_code`) をすり抜けて `subprocess` や `socket` を読み込み、サーバーのプロセスでコードを実行できた。
  - Dify (1.15.0 未満、CVE-2026-58141、7.6) では、SSRF 対策の Squid のプロキシに、送信元の ACL しかなく、宛先を拒否するルールがなかった。`make_request()` も宛先の IP を確かめていなかった。コンソールの利用者なら誰でも、HTTP Request ノード、Web のクロール、URL からの文書の取り込みを使って、内部のサンドボックス、PostgreSQL、AWS の IMDS (IAM の資格情報) に届いた。
- **なぜ重要か (評価)**: どちらも「AI のために作った隔離」が、従来型の欠陥 (Python の denylist、プロキシの ACL) で破れた例だ。LLM アプリの基盤の診断では、エージェントが使えるコードの実行と HTTP の取得の機能を、最初に見る価値がある。
- 出典: [Skyvern の修正 (commit)](https://github.com/Skyvern-AI/skyvern/commit/31a64c1a4b5dfaf1e76a7164845e10f2d68248dc) / [Dify の修正 (commit)](https://github.com/langgenius/dify/commit/7bfcf9185c75bb18f0b44335080524e659f087d9) / [NVD CVE-2026-58141](https://nvd.nist.gov/vuln/detail/CVE-2026-58141)

### [2026-11-07 arXiv] エージェントの引き継ぎで要件が書き換えられる問題と、決定的なプロンプトインジェクション対策
- **何が起きたか**:
  - **「Signed but Not Safe」(2611.07483)**: オーケストレーターがサブエージェントに作業を渡すとき、要件が抜けたり書き換えられたりする問題を、事前登録のうえで調べた。
    - 要件の一覧に HMAC-SHA256 で署名すると、攻撃下での危険なコミットは 69.4% から 9.0% に減った (Qwen3-8B、1,440 回、5 種の脅威)。
    - 改ざんされた試行での違反のコミットは、署名なしで 79%、署名ありで 0 だった。
    - 違反の検出率は、決定的な検証器が 78.7% (誤検知 7%)、LLM の検査役が 59.0% (誤検知 50%) だった。
  - **SPILLWAY (2611.07222)**: 道具を使うエージェントで、宛先 (受取人、振込先など) を使ってよいのを 3 つの場合に限る。利用者の依頼から来たもの、読み取り専用のツールの型付きのフィールドから来たもの、固定の委任のルールによるものだ。あわせて、命令のような文をモデルが読む前に、ルールベースで取り除く。
  - **Multimodal-SEA (2611.08281)**: 偽の画像などを使ったソーシャルエンジニアリングへの耐性を、個人用のエージェントで測るベンチマーク。14 分野、608 タスク。
- **なぜ重要か (評価)**: 前号の「AI の監査役は見逃しを減らすほど誤検知が増える」という結果と同じく、LLM による検査より決定的な検査のほうが強いことを示している。エージェントの診断では、「宛先がどこから来たか」を追う SPILLWAY の考え方を、そのまま試験の観点に使える。
- 出典: [arXiv 2611.07483](https://arxiv.org/abs/2611.07483) / [arXiv 2611.07222](https://arxiv.org/abs/2611.07222) / [arXiv 2611.08281](https://arxiv.org/abs/2611.08281)

### [2026-11-08] AI 生成物の「透かし」は利用者を追跡する「スパイマーク」になっている (GIGAZINE、原文は brand.io)
- **何が起きたか**:
  - ArtCraft の創業者 Brandon Thomas 氏は、Google の SynthID のような見えない透かしに、利用者に結びつくデータベースの ID を入れられると論じた。
  - 例として、SynthID-O の画像版が、512×512 の画像に 64 ビットの識別子と 72 ビットの誤り訂正を入れることを挙げた。EXIF や ID3 と違い、メタデータを消しても残るので、内部告発者が危険にさらされるという。
  - GIGAZINE の紹介記事は 11/8 だが、元の論考は 9 月のものだ。
- **なぜ重要か (評価)**: 来歴を示すための仕組みが、そのまま隠れた追跡の手段になる。流出した画像のフォレンジックと、調査の OPSEC (AI で作った画像を報告書に使うときなど) の両方で、知っておくべき性質だ。
- 出典: [GIGAZINE](https://gigazine.net/news/20261108-spymarks-not-watermarks/) / [brand.io](https://brand.io/article/spymarks/)

## セキュリティニュース

### [2026-11-07] IBM API Connect、v12.1.1.3 で約 200 件の脆弱性を一括で修正。ハードコードされた資格情報、署名検証の回避、未認証の OS コマンドインジェクションなど 9.8〜9.9 が並ぶ
- **何が起きたか**:
  - NVD は 11/7、IBM API Connect の CVE を一度に公開した。説明文に API Connect を含む CVE は、今回の取得範囲で 208 件あった。修正版は 12.1.1.3。10.0.8.0〜10.0.8.12 も多くの件で影響を受ける。
  - 主なもの:
    - CVE-2026-17360 (9.8): ハードコードされた資格情報で、管理を完全に奪える。
    - CVE-2026-17301 (9.8): 暗号の署名の検証が不十分で、未認証のまま認証を回避できる。
    - CVE-2026-17408 (9.8): 未認証の OS コマンドインジェクション。
    - CVE-2026-17392 (9.9): LDAP インジェクションで、他のテナントの管理権限を得られる。
    - CVE-2026-17150 (9.9): 他のテナントの情報にアクセスし、コードを実行できる。
  - 悪用や PoC の報告は、まだ確認できない。
- **なぜ重要か (評価)**: 件数の多さから、AI を使った網羅的な監査の結果とみられる (推定。IBM は手法を説明していない)。API ゲートウェイは、金融や大企業の「外向きの API の入口」だ。テナントの境界を越える欠陥が多いので、SaaS 型で使っている場合も、IBM 側の適用の状況を確かめたい。
- 出典: [IBM Security Bulletin (12.1)](https://www.ibm.com/support/pages/node/7295635) / [IBM Security Bulletin (10.0.8)](https://www.ibm.com/support/pages/node/7295637) / [NVD CVE-2026-17360](https://nvd.nist.gov/vuln/detail/CVE-2026-17360)

### [2026-11-07] [続報] WordPress コアの更新中の競合状態 (CVE-2026-119977、KEV): Wordfence は 10/28 以降に 24 万回を超える攻撃の試行を観測
- **前回から何が変わったか**:
  - Wordfence の István Márton 氏によると、標的にされ始めたのは 10/28 だった。試行は 24 万回を超えた。
  - 観測されたリクエストは、`/wp-content/upgrade/wordpress-6.9.11/setup-config.php` のような、展開中のインストーラーを狙っていた。影響範囲は 4.7〜7.1.3。
  - 7.1.4 は、展開先のディレクトリ名のランダム化、index のガード、展開した設定の安全でない昇格の制限を入れた。
- **悪用 / PoC**: 悪用を観測済み (KEV)。
- **なぜ重要か (評価)**: 「更新の最中」を突く攻撃が、すでに大量に自動化されている。深掘りの CF7 と合わせて、WordPress の案件では、`/wp-content/upgrade/` と `/wp-content/uploads/` が外から読めるかを毎回確かめたい。
- 出典: [GBHackers (Wordfence の観測)](https://gbhackers.com/exploit-wordpress-core-over-240000-attack/)

### [2026-11-08] [続報] sshole (CVE-2026-123158): SANS ISC のハニーポットで、最初の実際の攻撃は 11/5。全部が「A」の長いパスワードだった
- **前回から何が変わったか**:
  - Johannes Ullrich 氏によると、Cowrie のハニーポットでは、11/1 から長いパスワードが増え始めた。ただし 11/1 の分は、シェルのコマンドを誤ってパスワード欄に入れる、壊れた総当たりのスクリプトによるものだった。
  - sshole を狙った最初の試行は 11/5 で、全部が「A」の長いパスワードだった。
  - ハニーポットはパスワードの先頭 255 文字しか記録しないため、データには限りがある。続報で、成功した例を分析する予定だという。
- **悪用 / PoC**: 悪用の試行を観測済み。
- **なぜ重要か (評価)**: 認証のログで、長いパスワードや同じ文字の繰り返しのパスワードを検知の条件にできる。Alpine や OpenWrt の sshd を外に出している環境では、ログを 11/1 までさかのぼって確かめたい。
- 出典: [SANS ISC](https://isc.sans.edu/diary/33498)

### [2026-11-08] [続報] ARTEX: Hunt.io が、韓国の 7 つの金融機関を狙った運用者の基盤を分析。踏み台のサーバーに 42 のファイル
- **前回から何が変わったか**:
  - Hunt.io によると、9 月下旬〜10 月上旬に、韓国の 7 つの金融機関が、ネットに面したシステムから侵害された。被害は約 6.6〜6.7 万人と約 2,200 社で、個人、雇用、所得、ローンの情報が漏れた。
  - CrowdStrike (10/7) と Genians (10/12) の分析によると、主に使われたモデルは DeepSeek v4.1 Flash で、予備は GLM 5.3 と Grok 4.6 だった。一部は、転売業者のドメイン `xcai[.]pro` を経由していた。
  - ARTEX のコンソールは `38.244.50[.]120` (Cogent、ロサンゼルス、開いているポートは 15) にあった。香港の踏み台 `23.248.226[.]250` には、2 つのディレクトリに 42 のファイル (105MB) が置かれていた。
- **なぜ重要か (評価)**: 上の Stamos 氏の発言を裏づける技術的な分析だ。IoC (IP、ドメイン) は、自社の SOC で過去のログを照合する材料になる。
- 出典: [Security Affairs](https://securityaffairs.com/202607/ai/inside-artex-ai-hacking-tools-exposed-servers-and-south-korean-bank-breaches.html)

### [2026-11-07] UnrealIRCd 6.2.7.1: 一般の利用者がサーバーの権限でコマンドを実行できる欠陥 (CVE-2026-114713)。AI を使った内部の監査で 9 件を見つけ、ホットパッチで修正
- **何が起きたか**:
  - IRCv3 の `label` のメッセージタグを、返信にそのまま戻すときにエスケープしていなかった。そのため、改行などをサーバー間の通信に差し込めた。
  - 影響は 6.0.0 から 6.2.7.1 未満で、2 台以上のサーバーをつないだネットワークが対象になる。一般の利用者が KILL や GLINE などを、サーバーの権限で実行できる。
  - 開発者は、「過去 15 年で最も深刻」と説明した。ほかの 8 件は、クラッシュ、ハング、DoS と、他人の IP アドレスを明かす (decloak) 問題だった。
  - ほとんどのネットワークで、再起動なしのホットパッチで直せる。
- **なぜ重要か (評価)**: テキストのプロトコルで、エスケープの漏れがそのままコマンドの注入になる、典型的な型だ。IRCv3 のメッセージタグを実装したほかのサーバー (InspIRCd、Ergo など) でも、同じ箇所を確かめる価値がある。AI を使った監査で、古い C のコードから重大な欠陥が出る流れも続いている。
- 出典: [oss-security](https://seclists.org/oss-sec/2026/q4/576) / [UnrealIRCd フォーラム](https://forums.unrealircd.org/viewtopic.php?t=9487)

### [2026-11-07] Linux の Xen ドライバーに 3 件の UAF。安定版のカーネル 7 本を、この修正のためだけに公開
- **何が起きたか**:
  - Greg Kroah-Hartman 氏は、7.3.3、6.18.62、6.12.116、6.6.162、6.1.192、5.15.225、5.10.274 を公開した。中身は、Xen のセキュリティチームが同じ日に公表した 3 件の UAF の修正だけだ。
  - 2 件 (CVE-2026-100080 / 100082) は、Xen のホスト全体の DoS と情報漏えいの可能性がある。1 件 (CVE-2026-100081) は、権限昇格とホストの DoS の可能性がある。
- **なぜ重要か (評価)**: 11-05 号の XSA-523 (ハイパーバイザー側) に続いて、今回はゲスト / dom0 の Linux 側だ。Xen ベースの VPS やクラウドでは、ハイパーバイザーとカーネルの両方の版を確かめる必要がある。
- 出典: [LWN](https://lwn.net/Articles/1105902/)

### [2026-11-07] OffSeq、「既定の構成で、誰でも管理者になれる」2 件を公開: 会計ソフト Jumis の共通の sysadmin パスワード (CVE-2026-59105) と、ドローン管制 UgCS の空の資格情報でのログイン (CVE-2026-59104)
- **何が起きたか**:
  - **Jumis (ラトビアで広く使われる会計ソフト)**: SQL Server のログイン `##Tilde_JumisAdmin##` (sysadmin) のパスワードを、SQL Server の名前とハードコードされた定数から計算していた。サーバー名は、UDP 1434、TDS の pre-login の応答、DNS / NetBIOS から分かる。そのため、誰でもパスワードを手元で計算できる。`xp_cmdshell` も有効にされるので、OS のコマンドの実行まで届く。TJ7.0.141.36 で修正された。
  - **UgCS (6.2 未満)**: TCP 3334 の HCI プロトコルで、ユーザーが 1 人だけの既定のインストールに、空のユーザー名とパスワードを送ると、「唯一のユーザー」として認証された。既定で 0.0.0.0 に TLS なしで待ち受けるので、ドローンへの指令や飛行経路のアップロードまでできる。
  - どちらも CVSS 9.8。
- **なぜ重要か (評価)**: 「導出できる秘密は秘密ではない」と「空の入力を特別扱いしない」という、診断の基本の確認項目だ。内部の診断で、業務パッケージが作る SQL Server のログインを列挙すると、同じ型が見つかることがある。
- 出典: [OffSeq (Jumis)](https://offseq.com/en/research/jumis-cve-2026-59105/) / [OffSeq (UgCS)](https://offseq.com/en/research/ugcs-cve-2026-59104/)

### [2026-11-07] JetBrains CLion 2026.2 未満、Safe Mode でも Meson の設定や JSON のコンパイルデータベースからコードが実行できた (CVE-2026-123831 / 123832、9.6)
- **何が起きたか**: JetBrains は、信頼していないプロジェクトを開くための Safe Mode でも、Meson のプロジェクト設定と JSON のコンパイルデータベース (`compile_commands.json`) を経由してコードが実行できた欠陥を直した。2026.1.4 も対象になる。
- **なぜ重要か (評価)**: ソースコード診断で、顧客や第三者のリポジトリを IDE で開く読者に直接関わる。前号までの「偽のセキュリティツールを GitHub に置く」攻撃と組み合わせれば、研究者を狙う経路になる。IDE を更新し、信頼していないリポジトリは使い捨ての VM で開きたい。
- 出典: [JetBrains Fixed security issues](https://www.jetbrains.com/privacy-security/issues-fixed/) / [NVD CVE-2026-123831](https://nvd.nist.gov/vuln/detail/CVE-2026-123831)

### [2026-11-07] Microsoft Entra のデバイス登録に、CVSS 10.0 の認可の回避 (CVE-2026-109469)
- **何が起きたか**: Microsoft は、Entra Device Registration で、利用者が操作できるキーによって認可を回避され、ネットワーク越しに権限を昇格される欠陥を公開した。説明は 1 文だけで、技術的な詳細はない。
- **なぜ重要か (評価)**: Microsoft がクラウド側で直す種類の CVE で、通常は利用者の作業は要らない (MSRC の記載を各自で確認のこと)。ただし、デバイス登録は条件付きアクセスの「準拠デバイス」の判定の土台だ。悪用されていた場合に備えて、Entra の監査ログで、不審なデバイスの登録がないかを見直す価値はある。
- 出典: [MSRC](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-109469)

### [2026-11-08] ブレンナーベーストンネル (伊・墺) の建設会社 BBT SE が、データへの不正アクセスを認める。恐喝グループ Everest が 812GB を主張
- **何が起きたか**: イタリアとオーストリアを結ぶブレンナーベーストンネルを建設する BBT SE は、権限のない者がデータの一部にアクセスしたことを認めた。Everest は 812GB を盗んだと主張しているが、確認はされていない。Security Affairs は、犯罪者の主張する数字を、監査された情報として扱わないよう注意を促した。
- **なぜ重要か (評価)**: 国境をまたぐ重要インフラの建設事業の設計図や工程の情報は、恐喝だけでなく、国家の側にも価値がある。リーク情報を報じるときの「主張と事実を分ける」姿勢は、この日報の方針とも同じだ。
- 出典: [Security Affairs](https://securityaffairs.com/202691/cyber-crime/dont-hand-propaganda-a-gift-reading-the-brenner-base-tunnel-se-breach-calmly.html)

### [2026-11-07] 英 Royal Cornwall Hospitals NHS Trust、職員の健康情報の流出の相談窓口を検証。Excel のピボットテーブルに元のデータが残っていた件で、窓口の職員に大きな負担
- **何が起きたか**:
  - 2023 年 2 月に情報公開請求への回答として公開した Excel のブックに、病欠の元データが残っていた。ピボットテーブルを操作すると見えた。8,003 人が影響を受け、2025 年 11 月に一般の人が気づいた。
  - 検証の報告書によると、前日に知らされただけで窓口に回された職員が、怒鳴り声や、家庭内暴力の危険がある相談に対応した。2 週間の予定だった窓口は 11 週間に延びた。
- **なぜ重要か (評価)**: 「集計表に元データが残る」漏えいは、国内の自治体の公開資料でも繰り返されている。公開前の検査で、ピボットのキャッシュ、非表示のシート、コメントを確かめる手順が要る。インシデント対応の計画に、窓口の人員と心理的な支えを入れる必要も示している。
- 出典: [The Register](https://www.theregister.com/security/2026/11/07/nhs-breach-helpline-left-staff-carrying-a-significant-emotional-burden/5308201)

### [2026-11-07] 1,140 万ドル相当の NVIDIA のハードウェアが、オークランドからテキサスへの輸送中に消えた。食品輸送の会社のロゴを付けたトラックが引き取る
- **何が起きたか**: 8/29 にオークランドを出た 6 パレットは、予定どおりトラックに引き取られた。そのトラックには、食品輸送の会社のロゴが付いていた。警察は数時間ずつの停車を何度か追ったが、サンバーナディーノ郡で見失った。逮捕者はおらず、何も戻っていない (Mercury News を Ars が紹介)。
- **なぜ重要か (評価)**: 運送業者になりすます貨物の盗難は、輸出規制で価値が上がった GPU の、物理的な供給網のリスクだ。サイバーの面では、配送の予約システムや、運送業者のアカウントの乗っ取りが入口になることが多い。
- 出典: [Ars Technica](https://arstechnica.com/gadgets/2026/11/nvidia-hardware-worth-11-4m-vanished-between-oakland-and-texas/)

### [2026-11-08] Brava Security、1,500 万ドルを調達してステルスから登場。攻撃が生むはずのテレメトリーを AI で作り、SIEM の検知の穴を埋める
- **何が起きたか**: テルアビブの Brava (2024 年創業、CEO は Idan Basre 氏、CTO は Itay Gabbay 氏、ともにイスラエルの情報機関の出身) が、F2 Venture Capital と Pitango VC の主導で、シードで 1,500 万ドルを調達した。攻撃者の振る舞いをモデル化して攻撃を模擬し、出てくるテレメトリーから検知の穴を探して、SIEM の検知ルールを書き直す。
- **なぜ重要か (評価)**: AI による攻撃の模擬 (BAS) と検知のエンジニアリングの組み合わせで、パープルチームの仕事に近い領域だ。レッドチームの成果を、検知ルールに変える部分の自動化が進んでいる。
- 出典: [SecurityWeek](https://www.securityweek.com/brava-security-emerges-from-stealth-with-15-million-in-funding/)

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-11-07 以降 (NVD の公開 ≥ 2026-11-06T15:00Z) / 修正コミットが公開済み、またはバグクラスを言葉にできるものを優先。EPSS は 2026-11-08 の値で、いずれも 0.02 未満。KEV への追加は、この期間にはない (KEV の最終更新は 11/6)。

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-114432 | Contact Form 7 (WordPress) < 6.2.4 | CWE-434 / 9.8 | 拡張子が denylist (`php\|phtml\|…`) で `.phar` などが素通り。さらに、複数ファイルの移動が途中で失敗すると、移し終えたファイルが後片付けにも型の検査にも乗らない → 未認証で `wpcf7_uploads/` にファイルが残り、Debian / Ubuntu の Apache では RCE | [tags の diff](https://plugins.trac.wordpress.org/changeset?old_path=%2Fcontact-form-7%2Ftags%2F6.2.3&new_path=%2Fcontact-form-7%2Ftags%2F6.2.4) | 1,000 万以上のインストール / PoC は 11/19 公開予定 / EPSS 0.002 |
| CVE-2026-123550 / GHSA-3j2f-qhrc-rjfj | OpenAM < 16.1.4 | CWE-290 / 9.8 | `WantAssertionsSigned=false` のとき、SAML の SP が ECP (PAOS) と HTTP-Artifact の binding で**未署名のアサーションを受け入れる** → 未認証で任意の利用者 (管理者を含む) としてログインし、SSO 先も乗っ取る | [GHSA](https://github.com/OpenIdentityPlatform/OpenAM/security/advisories/GHSA-3j2f-qhrc-rjfj) (commit 不明) | IdP の認証の回避 / EPSS 0.006 |
| CVE-2026-123549 / 123551 | OpenAM < 16.1.4 (123551 は 14.0.0 以降) | CWE-269・201 / 9.8・10.0 | ①自己登録で Valid Creation Attributes を強制しない → 匿名で管理グループの属性を付けて登録できる ②旧 Liberty ID-FF のエンドポイントの検証のない内部の forward で、エージェント限定の確認を回避 → 通知の WebSocket から有効な `iPlanetDirectoryPro` を読める | [GHSA-jv8f](https://github.com/OpenIdentityPlatform/OpenAM/security/advisories/GHSA-jv8f-m88g-h6mm) / [GHSA-5c3q](https://github.com/OpenIdentityPlatform/OpenAM/security/advisories/GHSA-5c3q-hp86-xjr8) (commit 不明) | 未認証 / 国内の SSO 基盤で利用例あり |
| CVE-2026-124440 / GHSA-39w8-hv5g-f73w | Kyverno 1.19.1 (→ 1.19.2) | CWE-441 / 9.9 | `apiCall` の namespace の制限 (clamp) が、`urlPath` の**不正なパーセントエスケープ**を正規化前に判定 → namespace の利用者が、アドミッションコントローラーの SA の権限で他の namespace を読み、mutating webhook を作ってクラスタ管理者へ | [GHSA](https://github.com/kyverno/kyverno/security/advisories/GHSA-39w8-hv5g-f73w) (commit 不明) | マルチテナントの k8s / 1.19.1 で入り、11-06 号の 5 件と同じ 1.19.2 で修正 |
| CVE-2026-114713 | UnrealIRCd 6.0.0〜< 6.2.7.1 | CWE-74 / — | IRCv3 の `label` タグを返信に戻すときにエスケープしない → 改行を入れてサーバー間の通信にコマンドを注入 → 一般の利用者がサーバーの権限で KILL / GLINE | [advisory](https://forums.unrealircd.org/viewtopic.php?t=9487) (commit 不明) | 「15 年で最も深刻」/ ホットパッチあり |
| CVE-2026-121623 / 118515 | Symfony Serializer < 5.4.56 / 6.4.50 / 7.4.23 / 8.1.11 | CWE-22 / 8.2・8.4 | ①`DataUriNormalizer::denormalize()` が `data:` を**大文字小文字を区別して**照合 → `DATA:,/../../etc/passwd` がローカルのパスとして開かれ、任意のファイルを読める ②`UploadedFile` などのサブクラスの型は対象外で、`ObjectNormalizer` が攻撃者のデータ (パスを含む) でコンストラクタを呼ぶ | [①](https://github.com/symfony/symfony/commit/a0c551861ac23f888dfe6d1157ca78f4e220f3b7) / [②](https://github.com/symfony/symfony/commit/72ece5bb3084e8233325166357f85c8c0650ee86) | FrameworkBundle の既定で有効 / 1 リクエスト |
| CVE-2026-123783 | Skyvern ≤ 1.0.56 | CWE-184 / 8.8 | スクリプトの安全確認が AST の denylist (`is_safe_script_code`) → `types.CodeType` で生のバイトコードから関数を組み立てると、`subprocess` / `socket` を読み込める → サーバーで RCE | [diff](https://github.com/Skyvern-AI/skyvern/commit/31a64c1a4b5dfaf1e76a7164845e10f2d68248dc) | AI エージェント基盤 |
| CVE-2026-58141 | Dify < 1.15.0 | CWE-918 / 7.6 | SSRF 対策の Squid に宛先を拒否する ACL がなく、`make_request()` も IP を確かめない → コンソールの利用者が、HTTP Request ノードなどから IMDS / PostgreSQL / サンドボックスへ (POST / PUT / DELETE も可) | [diff](https://github.com/langgenius/dify/commit/7bfcf9185c75bb18f0b44335080524e659f087d9) | LLM アプリの基盤 / クラウドの資格情報 |
| CVE-2026-71495 | Wanderer < 0.20.0 | CWE-918 / 10.0 | `PUBLIC_PRIVATE_INSTANCE` が true でないと、未認証の `POST /api/v1/trail/download` が JSON の `url` をそのまま `event.fetch()` に渡して応答を返す → 内部の `db:8090` や `search:7700`、メタデータを読める | [diff](https://github.com/open-wanderer/wanderer/commit/c371337b3db1d2895b5cad651046ef0ad4dfc802) | 未認証 / 全応答を返す SSRF |
| CVE-2026-102359 | Kroki < 0.31.2 | CWE-22 / 7.5 | `KROKI_SAFE_MODE` の TikZ のガードが `\verbatiminput` だけを止め、`\openin` / `\read` / `\input` は許す (TeX Live の `openin_any` は寛容) → 未認証で任意のファイルを SVG に描かせて読める | [diff](https://github.com/yuzutech/kroki/commit/9108ab5b429b9dc82b76432ccf40d4d7eeba1b30) | 未認証 / ドキュメント基盤に同梱が多い |
| CVE-2026-53980 | charmbracelet wish < 2.0.5 (git middleware) | CWE-22 / 8.1 | リポジトリのパスの検査が「`/` の数」を数えるだけ → `../evil` (Windows では `..\..\evil`) で、ルートの外のリポジトリに upload-pack / receive-pack | [diff](https://github.com/charmbracelet/wish/commit/533db0daa90446b0d4ae3284877179c37e0cc48e) | Go の SSH アプリの部品 |
| CVE-2026-123614 / GHSA-hff9-5pqw-6w9f | imgproxy 4.0.0〜< 4.0.16 | CWE-122 / 9.8 | ICO のローダー (`vips/icoload.c`) で、`data_size` が整数あふれして確保が小さくなる → ヒープのバッファオーバーフローで、クラッシュか RCE | [diff](https://github.com/imgproxy/imgproxy/commit/a821b6a4cb07a1bf2bb9077431d1c1e734d79917) | 未認証で画像を渡せる構成が多い |
| CVE-2026-119923 / GHSA-vq28-vgj3-r26w | Babelfish for PostgreSQL (1.0〜5.4 の各系列) / Aurora PostgreSQL + Babelfish | CWE-122 / 9.8 | TDS の pre-login のパーサーで、不正な pre-login パケット → ヒープのオーバーフローで、DB のプロセスの権限で OS コマンド | [AWS 2026-166](https://aws.amazon.com/security/security-bulletins/2026-166-aws/) (commit 不明) | 未認証 / TCP 1433 |
| CVE-2026-123621 | Usermin ≤ 2.570 | CWE-22 / 8.8 | `mailbox/detachall.cgi` が添付ファイルの名前の `../` を消さない → 受信者が「すべて保存」すると `~/.forward` などを上書きし、コマンドを実行される | [diff](https://github.com/webmin/usermin/commit/cb4614e8319e0932b10533a4d5606debf5f40e14) | 未認証 (メールを送るだけ) / 11-07 号の CVE-2026-123620 の兄弟 |

**次点** (いずれも 11/7〜8 公開):
- Craft CMS 5.0.0〜< 5.11.2 の GraphQL の `prev` / `next` で、範囲外のセクションの記事を連鎖して読める (CVE-2026-124427、9.8)。
- OpenEMR 8.3.0 未満の fax/sms モジュールの `disposeDocument` で、`sqlconf.php` を読み、任意のファイルを書ける (CVE-2026-124450、9.9)。
- Zephyr の HTTP/2 サーバーで、CONTINUATION フレームの処理中にストリームが NULL のまま使われる (CVE-2026-87045、7.5、[diff](https://github.com/zephyrproject-rtos/zephyr/commit/e72a9d9498092bfbb7feed4b479bf21bc3218c3d))。
- Perl の RRD::CGI::Image で、`tz` を含むクエリの値が `tzset()` に渡り、FIFO を指定すると CGI が止まる (CVE-2026-123776)。

### 今日の CVE 所感

- **「正規化の前に判定する」型が 3 件**:
  - Symfony は `DATA:` の大文字。Kyverno はパーセントエスケープ。wish は `/` の数。
  - いずれも、判定する文字列と、実際に使われる (デコード・解決された) 文字列が違う。URL、パス、スキームを扱う他の言語の実装 (Laravel の `data:` の扱い、OPA / Gatekeeper の外部呼び出し、Gitea や Soft Serve のリポジトリのパス) に広がりやすい型だ。
- **denylist で作った隔離が破れる型が 3 件**:
  - CF7 (拡張子)、Skyvern (Python の AST)、Kroki (TeX のコマンド)。
  - 修正はいずれも allowlist 寄りか、仕組みの側での制限だ。診断では、「止めているもの」の一覧を見つけたら、言語や仕様の別名・同等の機能を探すのが近道になる。
- **SAML の「一部の binding だけ署名を見ない」**:
  - OpenAM の CVE-2026-123550 は、advisory が ECP (PAOS) と HTTP-Artifact の binding だけを挙げている (ほかの binding の扱いは書かれていない)。前号の Tracecat (空の環境変数で署名検証が無効) と同じく、SAML の SP の診断では、binding ごとに未署名のアサーションを試す価値がある。
- **診断で今週優先するもの**:
  - ① WordPress の CF7 (PoC は 11/19)
  - ② OpenAM / OpenIdentityPlatform を使う SSO 基盤 (国内の SIer の案件で見かける)
  - ③ Dify / Skyvern など、LLM アプリの基盤の SSRF とコードの実行
  - ④ マルチテナントの k8s の Kyverno 1.19.1 (この版だけに入った欠陥。11-06 号の 5 件と同じく 1.19.2 へ)

## 日本国内のセキュリティ動向

### 国内インシデント・事故

#### [2026-11-08] teket (電子チケットの販売・管理サービス): 不正アクセスで全会員の氏名とメールアドレスが流出。購入者は住所、電話番号、発券用コード、主催者のシリアルコードも
- **何が起きたか**:
  - teket は 11/5 に、外部からの不正アクセスの可能性が高いと判断し、同日 20:30 にすべてのサービスを止めた。11/6 に、会員情報などを管理するシステムへの侵入と、保管していた情報の一部の流出を確認した。
  - 流出したのは、全会員の氏名とメールアドレス。登録・購入した会員は、ほかに生年月日、年齢、性別、住所、電話番号、チケットの発券用コード、主催者が発行したシリアルコードも含む。件数は精査中だ。
  - パスワードとカード番号は、確認済みの流出項目に含まれていない。カードの情報は GMO-PG が保管している。
  - 11/6 に個人情報保護委員会へ報告した。再開時期は未定で、入場は購入完了のメールの提示で代える。侵入経路は公表していない。
  - 主催者 (札幌市青少年科学館など) も、利用者への告知を出している。
- **なぜ重要か (評価)**: 発券用コードが流出したので、なりすましの入場や転売ができる。公演名と購入履歴を使った、精度の高いフィッシングもできる。チケットの販売サイトの診断では、発券用コードを「推測できない値」にするだけでなく、漏れた後に無効にできる設計かどうかも確かめたい。
- 出典:
  - [teket (第一報)](https://corporate.teket.jp/news/privacy_261108)
  - [セキュリティ対策Lab (ロケットボーイズ)](https://rocket-boys.co.jp/security-measures-lab/teket_unauthorized_access_all_members_ticket_codes/)
  - [札幌市青少年科学館](https://www.ssc.slp.or.jp/news/single/153)
  - teket のページは JS で描画されるため本文を取得できず、内容は二次記事と主催者の告知で確かめた。

#### [2026-11-07] シグナルトーク「Maru-Jan」: 全会員 185 万 5,578 人分のメールアドレスとパスワードが流出。原因は「管理システムの機能を悪用した不正アクセス」
- **何が起きたか**:
  - オンライン麻雀 Maru-Jan を運営するシグナルトークは、11/4 15 時ごろまでに、会員情報を含むデータが外部にダウンロードされたと発表した。
  - 侵入経路は特定して対策したとし、11/7 16 時に再開した。
  - パスワードが平文かハッシュかは書かれていない。旧パスワードでも引き続きログインできる。カード番号は持っていない。補償は 1 人 3,000 ポイント。
- **なぜ重要か (評価)**:
  - 185 万件のメールアドレスとパスワードの組は、パスワードリスト攻撃にすぐ使える。平文だった場合は、なおさらだ。自社のサービスでは、ログインの失敗の急増を監視し、流出した組をブロックしたい。
  - 「管理システムの機能の悪用」という書き方は、管理画面の認可の不備か、管理者アカウントの乗っ取りを示唆する (推定)。診断では、管理画面の「一括ダウンロード」の機能に、件数の上限や承認があるかを確かめたい。
- 出典: [PR TIMES (2026-11-07)](https://prtimes.jp/main/html/rd/p/000000136.000009867.html) / [Maru-Jan のお知らせ](https://www.maru-jan.com/2026information.html)

#### [2026-11-07] 使えるねっと (クラウド・ホスティング): 契約管理のポータル「使えるポータル」の顧客情報が漏えい。VPS 127 件と共有サーバーにも及び、11/2 のバックアップに戻したため 5 日分の Web データとメールが消えた
- **何が起きたか**:
  - 11/6 にサーバーの異常を確認した。
  - **使えるポータル**: 暗号化して保存していたパスワードが解読されている可能性がある。全利用者のパスワードをリセットし、2FA の再設定を求めている。カードの情報は保管していない。
  - **VPS**: 不正アクセスを確認した収容機にあった VPS 127 件を調べている。
  - **共有サーバー**: 一部で不正アクセスを確認した。11/2 のバックアップから戻したため、11/2〜11/7 早朝に更新された Web データとメールが失われた。
  - 侵入経路も期間も調査中だ。
- **なぜ重要か (評価)**:
  - ホスティング事業者の管理系が破られ、顧客の基盤 (VPS と共有サーバー) まで届いた。「暗号化して保存していた」パスワードの解読の可能性に触れているので、可逆の暗号化だったとみられる (推定)。
  - 利用者は、ポータルのパスワードの使い回し、VPS の中の侵害の痕跡 (SSH の鍵、cron、Web シェル)、消えたメールへの対処を急ぐ必要がある。
- 出典: [使えるねっと (2026-11-07)](https://www.tsukaeru.net/news/20261107/)

#### [2026-11-07] [続報] アララ「アララメッセージ」: 委託元の確定値の公表が続く。成城石井 173,590 件、JERA「JERAサンデイ」30,337 件、岡山県は OTEX の案内の受信者を追加
- **前回から何が変わったか**:
  - 成城石井は第 2 報で 173,590 件とした (第 1 報は最大 168,630 件)。JERA は「JERAサンデイ」で 30,337 件とした (11/2 時点の概算は約 11 万件)。岡山県は、OTEX の案内を受け取っていた人の分を対象に加えた。
  - これらの確定値は、アララ自身の第 3 報 (前号の採用範囲の 11/6 に公表。前号では未掲載) を受けたものだ。第 3 報では、別のクラウド環境 (環境 B) から、正規の認証情報で 10/28〜31 にメールアドレス 3,249,492 件が持ち出されていたことが加わり、重複を除いた総数は 81,329,467 件になった。
- **なぜ重要か (評価)**: 最初に調べた環境の外にも、同じ認証情報で入られていた。調査の範囲を「最初に見つかった環境」に限らず、資格情報が使える範囲で決める必要がある、という教訓だ。委託元の件数は、今後も変わりうる。
- 出典:
  - [JERA (2026-11-07)](https://www.jera.co.jp/news/notice/20261107_2574)
  - [成城石井 (お知らせ)](https://corporate.seijoishii.com/blogs/notice/)
  - [岡山県 (PDF)](https://www.pref.okayama.jp/uploaded/life/1064871_10321935_misc.pdf)
  - [アララ 第 3 報 (TDnet PDF)](https://www.release.tdnet.info/inbs/140120261106568143.pdf)

#### [2026-11-07] [続報・報道] GMO (お名前.com デスクトップクラウドの件): 子会社では 2 年前、Active Directory を通じて管理者が全利用者の情報にアクセスできる状態だった (NHK)
- **前回から何が変わったか**:
  - NHK によると、2 年前の時点で、子会社で Active Directory を通じて、管理者が全利用者の情報にアクセスできる状態になっていた。リスクの指摘はあったが、十分な対策は取られていなかったという。
  - イエラエの指摘と 11/2 の会見は既報だ。今回は、指摘の具体的な中身として、AD の権限の設計が報じられた。
  - 確認できたのは、記事の概要 (meta description) までだ。
- **なぜ重要か (評価)**: 共有の AD で、管理者の権限がテナントの境界を越えていた。ホスティングや VDI の診断では、BloodHound で「顧客のテナントの OU に届く管理グループ」を洗い出すのが定番の確認になる。
- 出典: [NHK (2026-11-07)](https://news.web.nhk/newsweb/na/nd-20261107de72062)

> 小ネタ (11/6 以前の公表で範囲外。参考のため URL だけ):
> - [日本学術振興会 (電子申請システムの外部公開領域への不正アクセス)](https://www.jsps.go.jp/j-news/2026/shinsei/index.html)
> - [京都市 (佐川急便の件の影響で、シニアポイントの当選者 253 件)](https://www.city.kyoto.lg.jp/hokenfukushi/page/0000359972.html)
> - アイリスプラザの 770 万人は、BleepingComputer が 11/8 に英語で報じたが、内容は 11-03〜04 号の既報と同じ。

### 国内の注意喚起・ガイドライン・政策

> 11/7〜9 (週末) に、JPCERT/CC、IPA、NISC (国家サイバー統括室)、警察庁、個人情報保護委員会、経産省からの新しい注意喚起は確認できなかった。11/6 の金融庁「現下の情勢を踏まえた金融機関利用者へのお願い」(フィッシング耐性のある MFA を名指し) と、国家サイバー統括室の特設サイトへの事業者向け資料の追加は、範囲外 (11/6) のため末尾の除外一覧に回した。

#### [2026-11-08] 日テレ NEWS「個人情報を“手放す”企業が続々」: 漏えいの多発を受け、そもそも個人情報を持たない運用へ
- **何が起きたか**: 漏えいの公表が相次ぐ中で、顧客の個人情報を自社で持たない形 (決済代行や外部の ID 基盤に任せる、保存期間を短くする) に切り替える企業が出ている、という動向の記事。既報のアゾンやニコニコレンタカーと同じ流れだ。
- **なぜ重要か (評価)**: 「持たない」設計は最も効く対策の 1 つだ。ただし、上のアララや teket のように、委託先に集まったデータが一度に漏れる構図は残る。データを手放すときに、委託先の診断や契約で、何を確かめるかが問われる。
- 出典: [日テレ NEWS (2026-11-08)](https://news.ntv.co.jp/category/economy/4524fbcdecaf445bac0d956439508aca)

### 国内製品の脆弱性 (JVN)

> 直近2日間に該当する新規ニュースは確認できませんでした。

- JVN (jvn.jp) の最終更新は 2026/11/06 で、11/7〜9 の新規掲載はない。
- JVN iPedia の新規登録 (jvndb_new.rdf) も、すべて 11/6 の登録だ (225 件。Oracle、Apple、Chrome、Android など海外製品で、国内ベンダーの新規はない)。
- 参考: 深掘りの Contact Form 7 (国内の開発者の製品、発見者も国内の研究者) は、11/9 時点で JVN には掲載されていない。

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| — | — | — | 期間内の新規掲載なし | — | [JVN](https://jvn.jp/) |

### 国内コミュニティ・研究・イベント

#### [2026-11-08] Contact Form 7 の未認証ファイルアップロードを、国内の研究者 Shinya Murakami 氏 (@4n86rakam1) が報告
- **何が起きたか**: 深掘りの CVE-2026-114432 は、WPScan の記録で、発見者・報告者が Shinya Murakami 氏になっている。WPScan は、PoC を 11/19 に公開すると予告している。
- **なぜ重要か (評価)**: 国内で最も使われているフォームプラグインの欠陥を、国内の研究者が見つけた。PoC が出たら、拡張子の判定と後片付けの経路が実際にどう突かれたかを確かめ、深掘りの推定と照らし合わせたい。
- 出典: [WPScan](https://wpscan.com/vulnerability/6b0a5d1f-84fb-425f-8d37-ddde5703937c/)

#### [2026-11-09] Qiita「部品の脆弱性は、どこまで広がるのか？」: 主要な 64 の製品と 8 つの部品の依存関係を数えた
- **何が起きたか**: 「IT連携マップ」の依存データ (製品 64、部品 8、依存関係 72 本) をたどった。1 つの部品の脆弱性が影響しうる製品・部品の数は、OpenSSL が 20、SQLite が 16、Brotli が 13、PHP と Chromium が 11 だった。下位の部品の数は、ロリポップ! が 9、WordPress が 7 だった。
- **なぜ重要か (評価)**: SBOM の必要性を、国産のサービス名で具体的に示している。PHP2Shell のように「部品の欠陥が、国内の多くのサービスに一度に届く」事態を説明するときの材料になる。
- 出典: [Qiita](https://qiita.com/songchong/items/41a88eb41845af761b19)

#### [2026-11-09] Qiita: Python requests のデバッグで、認証情報がログに出る条件を実機で確認
- **何が起きたか**:
  - logging を DEBUG にしただけでは、Authorization ヘッダーは出なかった。
  - `http.client.HTTPConnection.debuglevel = 1` を足すと、Bearer や Basic の値がそのまま出た。
  - `params` で API キーを URL に入れると、urllib3 の DEBUG ログだけで漏れた。
  - 検証環境は Python 3.13.5、requests 2.34.2、urllib3 2.8.0。
- **なぜ重要か (評価)**: ソースコード診断で、「どの設定の組み合わせで秘密情報がログに出るか」を判断する根拠になる。11-08 号の Claude Code の `settings.local.json` と同じく、開発者の便利な機能から秘密情報が漏れる型だ。
- 出典: [Qiita](https://qiita.com/supportapp3/items/648fc00169c38050f031)

#### [2026-11-08] Zenn: 名古屋港とアスクルのランサムウェア被害の報告書を技術の目線で読み直す記事、AI エージェントで本番の診断を継続的な検査にする記事
- **何が起きたか**:
  - 名古屋港の記事は、ID とパスワードだけで接続できた保守用の VPN から、港の 5 つのターミナルが丸 2 日半止まった経緯をまとめた。
  - アスクルの記事は、MFA を適用していなかった委託先のアカウント 1 つから、136 日後に全出荷の停止と約 74 万件の流出に至った経緯をまとめた。
  - 別の記事は、年 1 回の診断を、AI エージェントによる継続的な検査に変える構成を紹介した。
- **なぜ重要か (評価)**: 国内の大きな事案の報告書を、「入口」と「検知までの日数」で比べる視点は、顧客への説明や報告書の書き方の参考になる。
- 出典: [Zenn (名古屋港)](https://zenn.dev/paokkyu/articles/nagoya-port-ransomware-2023) / [Zenn (アスクル)](https://zenn.dev/paokkyu/articles/askul-ransomware-2025) / [Zenn (継続的な検査)](https://zenn.dev/anfangd/articles/continuous-security-assessment-ai-agent)

---

<details><summary>取得状況 (デバッグ用)</summary>

- **巡回ソース数**: 約 110
  - RSS / Atom 82 本 (主に curl で取得)
  - NVD API (11/6 15:00Z〜11/8 20:30Z、1,035 件)、CISA KEV (GitHub のミラー)、EPSS API、OSV API
  - WordPress.org の SVN と Plugin API
  - サブエージェント 2 体による Web の検索と取得 (AI と国内)
- **採用件数**: AI技術=13 / AIセキュリティ=6 / セキュリティ=14 / CVE=14 (+次点 4) / 国内インシデント=5 / 国内政策=1 / JVN=0 / 国内コミュニティ=4
- **除外理由内訳**: 古すぎ=約 25 / 重複=約 40 / 日付不明=3
  - **古すぎ (範囲外の 11/6 以前)**:
    - NTT ドコモの第三報と会見 (最大 29 万 4,839 件、11/6 夜): [ドコモ](https://www.docomo.ne.jp/info/notice/page/261106_00_m.html) / [ケータイ Watch](https://k-tai.watch.impress.co.jp/docs/news/2154538.html)
    - ジェトロの 9,413 件の追加 (11/6): [ジェトロ](https://www.jetro.go.jp/news/announcement/2026/d475b9fab8ba23e5.html)
    - 金融庁の利用者へのお願い (11/6): [金融庁](https://www.fsa.go.jp/news/r8/sonota/20261106/20261106.html)
    - 国家サイバー統括室の特設サイトの資料の追加 (11/6): [特設サイト](https://www.cyber.go.jp/tokusetsu/contactpoint_advisory_hub/index.html)
    - NHK の Qilin への取材 (11/6)
    - JVN iPedia の 11/6 登録分
    - Google CodeMender の強化 (11/5 発表)
    - Gemini Omni 1.2 Flash / DeepSeek-V4-Flash-0731 (11/5)
    - UNM Health、APT29、Apple の KEV (11/5)
  - **重複**:
    - GPT-6 Cyber、DigiCert、Chainalysis、Crédit Mutuel Arkéa、SonicWall (KEV)、ARTEX / WorkOS、Claude Code の `settings.local.json`、Norad、ホワイトハウスの住宅用プロキシ
    - Megaspeed / Jensen Huang のメモ、OpenAI の資金調達、Ripple-65B、METR の報告、Goldman Sachs、アイリスプラザ
    - Apache Allura (CVE-2026-118196)、Axis2 (CVE-2026-123779)、SQL::Abstract (CVE-2026-121265)、Python の FIPS (CVE-2026-119170)
  - **日付不明**:
    - AVTOKYO 2026 の告知 (開催は 11/21、掲載日を確認できず)
    - 中央アルプス観光 (リザーブゲート) の告知
    - science.org の脳データの記事
- **取得失敗ソース**:
  - **週末で RSS が 11/6 で止まっていたもの**: Security NEXT、ScanNetSecurity、piyolog、ITmedia セキュリティ、JPCERT/CC、IPA。代わりに、組織の一次発表、PR TIMES、Zenn / Qiita、NHK を使った。
  - **パースに失敗したフィード**: CISA advisories、Google TI、MSRC、Trend Micro JP、Akamai、Rapid7、Huntress、nuclei-templates (GitHub)。CISA は KEV の JSON で代わりに確かめた。
  - **GitHub (advisory のページと commit の検索)**: 403。修正コミットは、NVD の参照と OSV で代わりに取った。OpenAM、Kyverno、Craft CMS の GHSA は OSV に未登録で、commit は不明。
  - **plugins.trac.wordpress.org**: 403。代わりに plugins.svn.wordpress.org の tags から直接ファイルを取って比べた。
  - **ページを読めなかったもの**: databreaches.net (Cloudflare のブロック)、FT (ボット対策)、teket (JS での描画)、NHK (本文は取れず meta description だけ)、JVN iPedia の詳細ページ (404)、Bloomberg (有料のため要約のみ)。

</details>
