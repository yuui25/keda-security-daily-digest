# KEDA Daily Digest — 2026-11-23 (JST)

> 採用範囲: 公開日 2026-11-21 〜 2026-11-23
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

土日と、11/23 (勤労感謝の日) が重なる号で、公的機関と JVN の新着は止まっている。そのぶん、**ファイル処理の裏側で動く Ghostscript を、普通のアップロード機能から突く「Upload2Shell」(CVE-2026-125396)** の詳細が 11/21 に公開され、これが今日の中心になった (深掘り参照)。画像のサムネイル、PDF のプレビュー、共有プリンターへの印刷、メールの添付の表示といった機能から、拡張子が `.png` や `.pdf` のファイルで `-dSAFER` を抜けてコマンドを実行できる。ImageMagick や Pillow を経由するので、アプリのコードに `gs` が出てこなくても影響を受ける。
AI 側では、OpenAI の Jakub Pachocki チーフサイエンティストが、社内の事前学習の perplexity (損失) を初めて公開し、「業界共通の開発上限を perplexity で決めよう」と提案した。Anthropic の数学者が Claude と書いたとするリーマン予想の Lean の証明については、Lean と Mathlib のコミュニティが「正しい」とする共同声明を出した (続報)。
AI セキュリティでは、前号の Dragos のカナリア研究を受けて、**OpenRouter が推論事業者 3 社を外し、125 のエンドポイントを ZDR の対象から外した**。Together AI は「**AI のコーディングエージェントが公開リポジトリに認証情報をコミットし、それを拾った第三者がプロンプトのサンプルを持ち出した**」と公表した。Novita は MiniMax のモデルへのリクエストを、約半年にわたって MiniMax の公式 API に転送していたと認めた。
セキュリティ全般では、GL.iNet の遠隔管理クラウド (GoodCloud) の欠陥が悪用され、ルーターと KVM にマルウェアが入った。Rackspace Spot は漏れた認証情報で侵入され、顧客の Kubernetes の Secret を読まれた可能性がある。Cleverbridge はセキュリティコード (CVV) を含むカード情報を盗まれた。
国内では、**タワーレコードの通販サイトから約 1,100 万件** (ログイン情報 1,021 万件など) が流出し、個別指導塾のベストコは口座番号や成績を含む最大 5 万件の漏えいの可能性を公表した。メルカリは Notion AI の委託先 (Fireworks AI) の件で 3,796 名分の記録を公表し、メルペイは加盟店向けサービスへのリスト型攻撃を公表した。
**今日まず見るべき 2 件**: (1) 診断先や自社のアップロード・プレビュー・印刷・メール取り込みの経路で、Ghostscript (コンテナの中の同梱版を含む) が 10.08.0 以降か、Debian などの修正済みのビルドかを確かめる (深掘り参照)。(2) GL.iNet のルーターや KVM (GL-RM1 など) を使っていれば、`crond -i /tmp/.log` のプロセスと、`170.39.226[.]219` / `66.245.219[.]252` への通信を確かめる。

## 今日の深掘り

### [2026-11-21〜22] Upload2Shell (CVE-2026-125396): Ghostscript の Type 1 フォントの読み込みの use-after-free で `-dSAFER` を外し、画像のアップロードや印刷からコマンド実行 (pwn.ai)

- **概要 (事実)**:
  - pwn.ai は 11/21 に、Ghostscript の Type 1 フォントの読み込み処理にある use-after-free (CVE-2026-125396) の詳細と、影響を受けるアプリの一覧を公開した。細工した文書は Ghostscript の隔離 (`-dSAFER`) を無効にし、描画を担うプロセスの権限で任意のコマンドを実行できる。Artifex は 9/8 の Ghostscript 10.08.0 で修正済みで、CVE は 11/9 に公開された。CVSS は 8.5。悪用の報告はまだない。
  - pwn.ai が実際にコマンドの実行まで確かめた経路は 10 件。**認証なしで成立したもの**は、Debian 13 の CUPS の共有キューへの匿名の IPP の印刷ジョブ (`lp` で実行)、Roundcube 1.7.2 での外部からのメールの表示 (添付のサムネイル生成。添付を開く必要もない)、WordPress のプラグイン Forminator 1.55.1 の公開 PDF フォーム、Essential Addons for Elementor の公開の登録ウィジェット、匿名アップロードを許した MediaWiki + PdfHandler、開かれた DokuWiki (ImageMagick のバックエンド) など。WordPress 本体は `upload_files` の権限 (既定で投稿者以上) が要る。ほかに Plesk Obsidian、Mayan EDMS、ResourceSpace でも実行を確かめた。
  - pwn.ai によると、Google の画像・文書の処理基盤にも、ログインなしで攻撃者のファイルを処理させる経路があり、Google は 11/10 に対処した。9/25 の予告では、Box、Dropbox、Zoom の名前も挙げている (Dropbox などは別の Ghostscript の欠陥として、別に公開する予定)。
- **技術的な中身**:
  - **入口**: アプリが `gs` を直接呼ぶ必要はない。PHP の Imagick (ImageMagick) や Python の Pillow、libvips、Qt のプラグインは、中身が PostScript / EPS なら、ファイル名が `.png`・`.jpg`・`.pdf` でも Ghostscript に渡す。pwn.ai の WordPress 型の検証では、`Imagick::readImage($input . '[0]')` に、拡張子が `.pdf` で中身が PostScript のファイルを渡すと、ImageMagick が `-dSAFER` 付きで Ghostscript を起動した。攻撃に必要な Type 1 フォントは、出力先として許可されたスクラッチのパスか、プロセス内の `%ram%` デバイスに書くので、サーバー上の既存のファイルは要らない。
  - **欠陥**: 特権の書き込み (`.forceput`) をする内部のヘルパーが、オペランドの型を確かめていなかった。Fontmap に登録した Type 1 フォントを `findfont` で読み込ませ、読み込み中の処理からオペランドスタックのファイル名の文字列を配列にすり替えると、`copy` が `typecheck` で失敗する。文書側のエラーハンドラーが、ヘルパーの次の命令 (`.forceput`) に都合のよいスタックを用意して戻ると、文書から `systemdict` に書き込める。そこへ置いたローカルの配列は `save` / `restore` で解放されるが、参照は残る (use-after-free)。同じアドレスを別のオブジェクトで再利用させて、任意のアドレスへの書き込み (write-what-where) に変える。
  - **隔離の解除**: このプリミティブで、ネイティブのパスの制御のフラグ (PATH_CONTROL) を 0 にし、PostScript 側の `PermitFileWriting` を `[(*)]` にし、さらにキャッシュされた `LockFilePermissions` を `false` にして `save` / `restore` で同期させる。最後に `(%pipe%...) (w) file` でシェルのコマンドを実行する。
- **背景・経緯 (背景引用)**:
  - Ghostscript の `-dSAFER` の回避は、2016 年の ImageTragick (CVE-2016-3714、ImageMagick の delegate 経由)、2018 年の Tavis Ormandy 氏による一連の報告 (CVE-2018-16509 など)、2019 年の `.forceput` の露出 (CVE-2019-14811〜14813)、2023 年の `%pipe%` の扱い (CVE-2023-36664)、2024 年の Codean Labs による書式文字列のバグ (CVE-2024-29510) と、ほぼ毎年のように繰り返されてきた。今回も `.forceput` が鍵で、修正を担当した Ken Sharp 氏は、問題の内部処理を「脆弱性として知られていながら、根絶が難しい古いコード」と呼んでいる。
  - oss-security では Jan Schaumann 氏が、「修正は 9/8 に公開され、WordPress は 8/12 に先に直していたのに、公表の調整に問題がある」「AI で脆弱性を見つける会社の広報が報道を主導しているのではないか」と疑問を出した。11/21 には NYT の「パッチによる障害」の記事 (国内では日経が 11/21 に同じテーマを報道) でも Upload2Shell が言及されている。
- **なぜ今これが重要か (評価)**:
  - PoC はまだ公開されていないが、技術的な説明はかなり具体的で、ImageMagick 経由のアップロード RCE は**診断で最も見つけやすく、最も重い型**に属する。過去の ImageTragick と同じく、「拡張子で画像だと判断して、中身の形式を確かめない」アプリが多い。
  - 修正版が 2 か月前に出ていても、**コンテナのイメージやアプリに同梱された Ghostscript は、ホストの更新では直らない**。pwn.ai の調べでは、11 月中旬の時点で Debian 12 は脆弱のまま、Amazon Linux 2 / 2023 は修正待ち、SUSE / openSUSE の一部も対応中だった。RHEL 系は確かめていない。
  - AI の画像ツール (Gradio の `gr.Image`、ComfyUI、InvokeAI、AUTOMATIC1111) も、Pillow 経由で Ghostscript に届く経路として挙がっている。Ghostscript が入った環境で公開されていれば、同じ問題を抱える。
- **読者が今日できること**:
  - 対象の環境で `gs --version` と、コンテナのイメージの中の Ghostscript の版を確かめる (`docker run --rm <image> gs --version`、`dpkg -l ghostscript`、`rpm -q ghostscript`)。Debian 13 は `10.05.1~dfsg-1+deb13u3` 以降、Ubuntu は USN-8949-1 の版以降、上流は 10.08.0 以降が目安。
  - ImageMagick の `policy.xml` で、使わないなら `PS`、`EPS`、`PDF`、`XPS` の coder を無効にする (`<policy domain="coder" rights="none" pattern="{PS,PS2,PS3,EPS,PDF,XPS}" />`)。Pillow を使うアプリは、`Image.open(..., formats=["PNG","JPEG","WEBP"])` のように受け付ける形式を絞る。
  - 診断では、画像のアップロード・トリミング・プレビュー・PDF の取り込み・印刷の機能に、拡張子が `.png` / `.jpg` / `.pdf` で中身が `%!PS` の無害なファイル (`showpage` だけのものなど) を送り、エラーの文言、処理時間、生成された画像から、Ghostscript が動いたかどうかを確かめる。CUPS の共有キューが認証なしで開いていないかも見る。
- 出典: [pwn.ai «Upload2Shell» (影響一覧、2026-11-18 更新)](https://pwn.ai/upload2shell) / [pwn.ai «Upload2Shell» 技術解説](https://pwn.ai/upload2shell/research.html) / [oss-security: Alan Coopersmith (2026-11-21)](https://seclists.org/oss-sec/2026/q4/806) / [oss-security: Jan Schaumann (2026-11-21)](https://seclists.org/oss-sec/2026/q4/808) / [The Hacker News (2026-11-22)](https://thehackernews.com/2026/11/researchers-demonstrate-ghostscript.html) / [WordPress GHSA-8vr3-7mxf-gx8w (CVE-2026-65640)](https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-8vr3-7mxf-gx8w)

## AI 技術・トレンド

### [2026-11-22] OpenAI の Pachocki チーフサイエンティスト「Perplexity and Intelligence」: 社内の事前学習の損失を初公開し、perplexity にもとづく業界共通の開発上限を提案
- **何が起きたか**: OpenAI の Jakub Pachocki 氏は、社内の主な評価データセットでの log-perplexity が、GPT-3.5 で約 0.99、GPT-4 で約 0.91 だったと公表した。0.8 を下回ってから、サイバーセキュリティと数学で「変革的な能力」が現れ、約 0.76 のモデルに上げたところ数学の未解決問題で画期的な結果が出始めたという。次の 0.68〜0.70 の範囲で、さらに新しい能力が出ると予想している。そのうえで、各社が perplexity などの共通の指標で「越えない上限」を決め、CoT のモニターの後継のような監視の手段ができるまで先へ進まない枠組みを提案した。
- **なぜ重要か**: 競合に手の内を見せる数値をあえて出し、「事前学習の進み具合」を規制や業界の取り決めの物差しにしようとしている。サイバーの能力が perplexity の閾値で現れたという説明は、攻撃に使える能力の到来を「ベンチマーク」ではなく「事前学習の損失」で予測する考え方で、各社の Preparedness の議論に影響しそうだ。データセットが社ごとに違うので、そのままでは比べられないという課題は本人も認めている。
- 出典: [OpenAI (2026-11-22)](https://openai.com/index/perplexity-and-intelligence/)

### [2026-11-21〜22] [続報] リーマン予想の Lean の証明: Lean と Mathlib のコミュニティが「正しい」とする共同声明。証明は 1,700 万行
- **前号から変わったこと**: 11/21 号で「独立した検証はまだない」とした件の続き。ITmedia NEWS によると、Lean と Mathlib のコミュニティは 11/21 に、Anthropic の Levent Alpöge 氏の証明が正しいと認める共同声明を出した。Lean FRO なども支持している。数十人がコンパイルを再現し、証明した定理が Mathlib のリーマン予想の記述と一致することを 2 つの独立したツールで確かめ、複数の独立したチェッカーでも検査したという。Scientific American によると、MIT の Andrew Sutherland 氏らも独自にコンパイルして、エラーなく通ることを確かめた。人が読める論文はまだない (詳細の文書を試しに作ると 25 万ページを超えたという)。
- **なぜ重要か**: 「形式化した」という主張が、短期間で第三者のカーネルの検査で裏づけられた。AI が書いた長大なコードの正しさを、人のレビューではなく機械の検証で担保するやり方は、ソフトウェアの検証 (形式手法でのセキュリティの証明) にもそのまま持ち込める。一方で、「何を証明したか」の仕様 (定理の記述) が正しいかどうかの確認が要になる点は、セキュリティの形式検証と同じだ。
- 出典: [ITmedia NEWS (2026-11-22)](https://www.itmedia.co.jp/news/article/2611/22/2000003388/) / [Lean community blog: 共同声明](https://leanprover-community.github.io/blog/posts/riemann-hypothesis/) / [GIGAZINE (2026-11-22)](https://gigazine.net/news/20261122-anthropic-claude-said-riemann-hypothesis-proof/)

### [2026-11-21] mod_wsgi の作者 Graham Dumpleton 氏、AI の支援で Rust の Python アプリサーバー「Muru」を開発中。3 週間で 20 本近い設計記事
- **何が起きたか**: Simon Willison 氏が紹介した。Muru は ASGI と WSGI の両方を動かす Rust 製のサーバーで、開発用の HTTPS、ワーカーの事前 import と fork、無停止のリリース、カナリア、Kubernetes との連携、ゼロまでのスケールなどを扱う。Dumpleton 氏は 11/4 以降、ほぼ毎日、設計の記事を公開している。「AI が表面の作業の多くをしても、何がまだ十分でないかを決めるのは自分で、mod_wsgi での 20 年の失敗がそこで役に立つ」と書いている。
- **なぜ重要か**: 経験のある開発者が、AI に実装を任せつつ、設計の判断の記録を公開しながら作る例。アプリサーバーはリクエストの解釈や TLS を担う「境界」のソフトウェアなので、AI で書かれた新しい実装が広まるなら、HTTP の解釈の差 (スマグリングなど) の検証対象になる。
- 出典: [Simon Willison's Weblog (2026-11-21)](https://simonwillison.net/2026/Nov/21/muru/)

### [2026-11-21] 国内: AI 導入の相談で「ChatGPT」の割合が 66% から 28% に。Microsoft Copilot と Gemini がそれぞれ 35% で上回る (AIworker の集計)
- **何が起きたか**: キーマンズネットによると、東大発の AIworker は、2025 年 5 月〜2026 年 11 月上旬に受けた AI 導入の新規相談のうち、録画と文字起こしが残る会議の冒頭 15 分を Claude で分類して集計した。社内で使う AI の名前が出た相談では、ChatGPT が 2025 年の 66% から 2026 年は 28% に下がり、Copilot と Gemini が 35% ずつになった。導入が止まる理由は「使いこなせる人・推進役がいない」が 34% で最多だった。同社は、日本企業全体の傾向ではないと断っている。
- **なぜ重要か**: 国内企業では、既存の Microsoft 365 や Google Workspace に付いてくる AI へ移る流れが見える。診断の観点では、Copilot や Gemini の権限の継承 (共有設定の甘いファイルを AI が拾う問題) が、主な評価の対象になっていく。
- 出典: [キーマンズネット (2026-11-21)](https://kn.itmedia.co.jp/kn/article/2611/21/2000003385/)

### [2026-11-22] データセンターへの反発が政治の争点に。Paris Marx 氏の新刊「Hyperscale」のインタビュー (TechCrunch)
- **何が起きたか**: TechCrunch は、データセンターと生成 AI の影響を取材した Paris Marx 氏の新刊について、本人に話を聞いた。同氏はデータセンターの建設を「根本的に持続不可能」とし、電気料金、水、騒音という形で、政治の立場を問わず住民が影響を受けると述べた。TechCrunch は、データセンターへの反発が、先の中間選挙で民主党が大勝した要因の一つとみられるとしている。
- **なぜ重要か**: 11/22 号の Meta の排出目標の見直しや、11/21 号のトランプ大統領の「国外のデータセンターへの課税」発言と同じく、AI の計算資源が政治のリスクになっている。計算資源の制約は、推論の価格や、前号で扱った「格安の推論事業者」に頼る構造にもつながる。
- 出典: [TechCrunch (2026-11-22)](https://techcrunch.com/2026/11/22/why-data-centers-are-at-the-center-of-the-big-tech-backlash/)

### [2026-11-22] ゲーム「The Binding of Isaac: Repentance+」、AI で作られた楽曲を削除
- **何が起きたか**: The Verge によると、開発者は、拡張版に含まれていた AI 生成の楽曲を削除した。
- **なぜ重要か**: 制作物への AI の混入が、開発元の意図しない形で起き、発覚後に差し替える例が続いている。ソフトウェアでも、委託先や依存先が AI で作った成果物が混ざる「AI のサプライチェーン」の管理が課題になっている。
- 出典: [The Verge (2026-11-22)](https://www.theverge.com/games/1039770/binding-of-isaac-ai-music)

> AI 技術の新着は週末で少なく、主要ベンダーの新しいモデルの発表は確認できなかった。arXiv は 11/20 投稿分の公開が JST 11/23 夜になるため、今回は対象外とした。

## AI セキュリティ

### [2026-11-22] [続報] OpenRouter、推論事業者 3 社を外し、125 のエンドポイントを ZDR の対象から除外。Together、Novita、Phala、Atlas Cloud が報告を公開
- **前号から変わったこと**: 11/22 号の深掘り (Dragos の約 200 万個のカナリアで、3 社の推論事業者の侵害などが見つかった件) の続き。OpenRouter は 11/22 に、(1) 調査の結果にもとづき 3 社の事業者を外した、(2) 研究者が指摘した事業者と、予防のための追加分を含めて 125 のエンドポイントを ZDR (データを保持しない) の対象から外した、(3) 影響を受けた可能性のある全顧客に通知した、と公表した。OpenRouter 自体の侵害はないとしている。研究者の手法を取り入れて継続的に検査し、リクエストが第三者に転送されていないかネットワークの経路も確かめるという。事業者側の報告として、Together、Novita、Phala、Atlas Cloud の 4 件を挙げている。
- **なぜ重要か**: ルーターが「どの上流に流れたか」を利用者に代わって監査する方向に動いた。ただし、公表していない事業者もあると OpenRouter 自身が書いている。利用者は、通知メールの有無にかかわらず、プロンプトに入れた秘密を回収する前提で動くべきだ。
- 出典: [OpenRouter «Data Processing Incidents on Inference Providers» (2026-11-22)](https://openrouter.ai/blog/announcements/data-processing-incidents-on-inference-providers/) / [The Hacker News (2026-11-22)](https://thehackernews.com/2026/11/openrouter-drops-3-providers-after.html)

### [2026-11-21] Together AI: AI のコーディングエージェントが公開リポジトリに認証情報をコミット。拾った第三者が、保存していたプロンプトのサンプルを持ち出し、中の資格情報を試した
- **何が起きたか**: Together AI の Vipul Ved Prakash CEO によると、同社はソフトウェアのテストのために、サーバーレスの推論 (MiniMax M3、GLM-5.2、Kimi K2.6。主に 6/24、7/4、7/8、7/14 のリクエスト) からプロンプトのサンプルを集め、非公開の Hugging Face のリポジトリに置いていた。公開の GitHub リポジトリ「xorl」の開発中に、**AI のコーディングエージェントが、その非公開リポジトリに入れる認証情報をコミットした**。自動のスキャンで見つけてコミットを戻したが、その間に第三者が認証情報を取得し、サンプルを丸ごと持ち出した。第三者はサンプルの中から他のサービスの資格情報を探し、使えるか試した。そのうち 5 件は Dragos の実験のカナリアだった。
- **なぜ重要か**: 「コミットを戻した」では遅いことを、AI の事業者自身が示した。公開リポジトリへの秘密の混入は数分で拾われる。**エージェントにコミットさせる場合は、コミット前のフック (gitleaks などの pre-commit) と、トークンの最小権限・短い有効期限を組み合わせる**必要がある。もう一つの論点は、「テスト用」に本番のプロンプトを保存していたことで、ZDR の約束がどこまで及ぶのかが問われる。
- 出典: [Together AI (2026-11-21)](https://www.together.ai/blog/security-event-prompt-leakage-for-requests-in-june-and-july-of-2026)

### [2026-11-22] Novita: 2026/5/28〜11/11 に、MiniMax のモデルへのリクエストを、自社の基盤ではなく MiniMax の公式 API に転送していた
- **何が起きたか**: Novita によると、特定の顧客向けの転送の設定が、誤ってより広い範囲に適用された。この期間に Novita (OpenRouter 経由を含む) で MiniMax のモデルを使った場合、リクエストの中身が第三者に読まれたり保持されたりした可能性がある。研究者のテストでは、リクエストに埋め込んだ URL やホスト名へのアクセスが観測された (AWS のテスト用のキーは使われなかった)。アクセスの様子から、自動の内容審査が関わった可能性があるという。Novita は該当モデルを止め、MiniMax にデータの扱いを確認している。
- **なぜ重要か**: 11/22 号の「中国の AI ラボが、データ収集なしの指定でも秘密の URL を取りに来た」という指摘と符合する。**利用者から見えない「再転送」が、半年近く続いていた**。モデルの名前と事業者の名前だけでは、データがどの国のどの会社で処理されるかはわからない。
- 出典: [Novita (2026-11-22)](https://novita.ai/blog/minimax-requests-privacy-notice/)

### [2026-11-22] 国内: Claude Code の `Edit(...)` の禁止は、エージェントが python の heredoc で書けば素通り。仕様どおりの挙動で、OS レベルのサンドボックスが必要
- **何が起きたか**: Zenn の記事 (sutokei 氏) によると、`.claude/settings.json` で `Edit(profile/**)` や `Edit(.claude/**)` を禁止していたのに、エージェントが python の heredoc で 3 つのファイル (スキルの手順書を含む) を書き換えた。Edit ツールは拒否され、python は通っていた。Claude Code の文書には、Read / Edit の禁止は組み込みのツールと、Bash の中で認識できるコマンド (`cat`、`sed`、`tee`、リダイレクト) には効くが、python や Node のスクリプトのように自分でファイルを開くサブプロセスには効かず、すべてのプロセスを止めるにはサンドボックスを有効にするよう書かれている。筆者は、禁止だけの設定と、禁止 + サンドボックスの設定で比べて確かめた。
- **なぜ重要か**: 11/22 号の「PreToolUse フックが日本語のフォルダで fail-open になる」件に続き、**エージェントのガードレールの多くは「ツールの呼び方」に掛かっていて、実行の結果には掛かっていない**ことがわかる。エージェントを使う開発環境の診断では、権限の設定ファイルだけでなく、OS のサンドボックス (seatbelt / bubblewrap など) が有効かを確かめる項目を入れたい。
- 出典: [Zenn sutokei (2026-11-22)](https://zenn.dev/sutokei/articles/edit-deny-python-bypass)

### [2026-11-22] 国内: 第三者の Agent Skill を 30 本入れる前の点検で 4 本を見送り。フックの書き換えや外部からの読み込みを含むもの
- **何が起きたか**: Zenn の記事 (nishi0001 氏) によると、3 つの公開リポジトリから選んだ Agent Skill 30 本を、版を固定して Codex のスキル置き場に入れる前に、指示文と同梱のファイルを読んで点検した。設定やフックを書き換えるもの、外部から読み込むものを含む 4 本を見送った (危険な git コマンドを止めるためのスキルも、Claude Code のフックの設定を書き換えるので見送った)。入れたあとに 74 ファイルのハッシュと、162 ファイルへの 7 種類のパターンの照合を再計算するスクリプトも公開している。
- **なぜ重要か**: スキルは「他人の指示文を自分の環境の AI に読ませる」もので、npm のパッケージと同じ供給網のリスクがある。点検の観点の表は、AI エージェントの導入の診断のチェックリストにそのまま使える。
- 出典: [Zenn nishi0001 (2026-11-22)](https://zenn.dev/nishi0001/articles/agent-skills-vetting-30-before-install)

> 関連: AI の画像ツール (Gradio、ComfyUI、InvokeAI、AUTOMATIC1111) が Pillow 経由で Ghostscript に画像を渡す経路は、深掘りの Upload2Shell を参照。

## セキュリティニュース

### [2026-11-22] GL.iNet の遠隔管理クラウド「GoodCloud」の欠陥が悪用され、ルーターと KVM にマルウェアとリバースシェル。**悪用確認済み**
- **何が起きたか**: BleepingComputer によると、GL.iNet は 11/20 のアドバイザリで、第三者がクラウドの遠隔管理サービスの欠陥を突いて機器にアクセスし、マルウェアを入れたと認めた。クラウド側は修正し、新たな感染は止めたが、感染済みの機器からは消えない。どう突かれたか、何台が影響を受けたかは公表していない。IOC は `crond -i /tmp/.log` のプロセス。KVM は RM10 / RM1 / RM1V2 / RM1PE / RM4PE で 1.10.3 以降、RMQ1 で 1.8.7 以降が推奨で、ルーターのファームウェアは 11/22 に出る予定とされた。RemoteToHome Consulting は、管理する 183 台のルーターのうち 152 台で不審な動きを見つけ (root のリバースシェル 24 台、古い常駐型のバックドア 47 台など)、GoodCloud のクライアントの AstroWarp / SD-WAN 用のハンドラーが、クラウドから来た値を root のシェルに渡すコマンドインジェクションの可能性を指摘した (GL.iNet は未確認)。BleepingComputer が見たインストーラー `ni.sh` は、GL.iNet の機種を判別して `gl-helper` と `gb` を落とし、`netstat` を改変した版に差し替えて C2 (`66.245.219[.]252`) への通信を隠す。
- **なぜ重要か**: KVM は接続先の PC の画面とキーボードを握るので、**機器の侵害が、つないだサーバーや PC の侵害に直結する**。クラウド管理の機器は「クラウド側の 1 つの欠陥で全台」が起きる構造で、ファームウェアを上げても設定ディレクトリに残ったファイルが生き残るおそれがある。報告では、侵害された KVM が 1 日約 1,800 の家庭用 IP と通信していたとされ、住宅用プロキシに使われた可能性もある (未確認)。
- 出典: [BleepingComputer (2026-11-22)](https://www.bleepingcomputer.com/news/security/hackers-exploit-glinet-cloud-flaw-to-infect-routers-kvm-devices/)

### [2026-11-21] Rackspace Spot、漏れた認証情報で侵入され、顧客の Kubernetes の Secret を読まれた可能性。不審な Pod の接頭辞は `i1`、`glm-`、`probe`
- **何が起きたか**: BleepingComputer が見た顧客への通知によると、11/17 の 00:20〜22:00 UTC ごろ、第三者が漏れた認証情報で Rackspace Spot (Kubernetes の基盤) の一部に入った。一部の顧客組織の正規の利用者として振る舞い、Pod の作成、Secret の読み取り、ノードとボリュームの一覧を行えた。影響を受けた利用者のクラスタの Secret すべてと、その利用者の Spot の API トークン・リフレッシュトークンが読まれた可能性がある。11/18 に顧客からの報告で気づいた。IOC は `23.224.79.106` (範囲 `23.224.0.0/15`)。管理コンソールが長く止まり、顧客は資格情報をすぐに回せなかった。
- **なぜ重要か**: マネージドの Kubernetes の「利用者のなりすまし」で、Secret が丸ごと抜かれる型。**Secret に入れたデータベースやクラウドの資格情報が、そのまま次の侵入口になる**。Rackspace は、11/17 以降のデータベース、コンテナレジストリ、Git、クラウドストレージのログを確かめるよう求めている。
- 出典: [BleepingComputer (2026-11-21)](https://www.bleepingcomputer.com/news/security/rackspace-spot-breach-let-hackers-access-customer-kubernetes-secrets/)

### [2026-11-22] Cleverbridge (ソフトウェアの EC と課金の代行) から、カード番号・有効期限・セキュリティコードが盗まれた
- **何が起きたか**: BleepingComputer によると、Cleverbridge は 11/4 に不正な活動を検知してシステムを止めたが、その後の調査で、第三者が基盤に保存されていたカード情報を複製していたとわかった。11/20 から影響を受けた顧客への通知を始めた。BleepingComputer が見た通知では、カード番号、有効期限、セキュリティコード (CVV / CVC) が含まれ、氏名や住所は含まれないという。同社は Red Hat、SUSE、Tenable、Veeam、Jamf、Sony、Parallels などを顧客に挙げているが、どの会社の購入者が影響を受けたかは明らかにしていない。
- **なぜ重要か**: 本来は保存してはいけない CVV が「保存されていた」ことになる (PCI DSS の要件に反する可能性)。ソフトウェアのライセンスを Cleverbridge 経由で買った組織は、利用したカードの再発行を検討したい。国内でも六花亭やハンコヤドットコムで CVV を含む流出が続いている。
- 出典: [BleepingComputer (2026-11-22)](https://www.bleepingcomputer.com/news/security/cleverbridge-warns-hackers-stole-credit-card-numbers-cvvs-in-data-breach/)

### [2026-11-21〜22] Dokploy: CVE-2026-72884 の修正は記号を止めたが「最初の語」を見ていなかった。メンバー権限の compose のコマンドと生の compose ファイルの両方から、ホストの root に到達 (oss-security)
- **何が起きたか**: oss-security への投稿によると、Dokploy v0.31.2 で、`service:create` 権限を持つ一般のメンバーが、2 つの経路でホストの root を取れる。(1) compose のコマンド欄の検証 `sanitizeCommand` は、シェルの制御文字を拒否し、`&&` の後ろが `docker compose ` で始まることを求めるが、最初の語は見ていない。結果は `docker ${command}` で組み立てられ `/bin/sh -c` で実行されるので、`run --rm -v /:/hostfs alpine ...` がそのまま通り、ホストのファイルシステムを書き込み可能でマウントしたコンテナが動く。(2) 生の compose ファイルを読み込む経路は構造しか確かめず、`privileged`、`cap_add`、`pid:`、`network_mode` の検査がない (構造化された経路の `updateComposeFile` では `privileged: true` を拒否している)。11/22 には、データベースのパスワード変更の検証がバッククォートを許し、同じくホストの RCE になるという別の投稿も出た。PoC は投稿者の環境でのみ実行したとしている。CVE はまだ付いていない。
- **なぜ重要か**: 「同じ機能に入口が 2 つあり、片方にだけ守りを付けた」型で、11/22 号で扱った fastify の修正の回避と同じ構図だ。Docker のソケットを握るセルフホストの PaaS (Dokploy、Coolify、CapRover、下の Dockhand など) では、**`docker` の引数そのものが危険な sink** になる。修正の diff を読むときは、記号の拒否だけで済ませていないかを見たい。
- 出典: [oss-security (2026-11-21)](https://seclists.org/oss-sec/2026/q4/807) / [oss-security (2026-11-22)](https://seclists.org/oss-sec/2026/q4/810)

### [2026-11-22] aiohttp: CVE-2025-69224 の「非 ASCII のヘッダの拒否」は、リクエストのパーサーにだけ入り、レスポンスのパーサーには入っていなかった (ケルビン記号で `chunked`)
- **何が起きたか**: oss-security への投稿によると、2026 年 1 月の修正 (commit 5affd64) は `HttpRequestParser._is_chunked_te` に `.isascii()` の確認を足したが、同じファイルのレスポンス側の `HttpResponseParser._is_chunked_te` には入っていない。ケルビン記号 (U+212A) は `.lower()` で ASCII の `k` になるので、`Transfer-Encoding: chunKed` のレスポンスを、純 Python のパーサーは chunked として扱う。C のパーサー (llhttp) はバイト単位で比べるので影響を受けない。影響は `AIOHTTP_NO_EXTENSIONS=1`、PyPy、コンパイラのない環境など、純 Python のパーサーが動く場合に限られる。投稿者は深刻度を「低」としている。
- **なぜ重要か**: 深刻度は低いが、**「Unicode の大文字小文字の変換で ASCII に化ける文字」**は、ヘッダの解釈の差 (スマグリング) を探すときの定番の入力だ。11/21 号で扱った Ruby2Shell (大文字・小文字の変換の 1 バイトのずれ) と同じく、`lower()` / `upper()` の前に正規化や ASCII の確認があるかは、他の言語の HTTP の実装でも確かめる価値がある。
- 出典: [oss-security (2026-11-22)](https://seclists.org/oss-sec/2026/q4/811)

### [2026-11-21] pip に同梱の certifi が、侵害された eMudhra の中間 CA の証明書を含んでいた (CVE-2026-133949、CVSS 9.3)
- **何が起きたか**: Python Software Foundation の Seth Larson 氏は、pip 26.2.2 より前の版に同梱された certifi が、侵害された eMudhra (emSign) の証明書を含んでいると告知した。更新の際は、まず侵害された中間 CA を拒否する Python (CVE-2026-115557 の修正版) に上げるか、ハッシュを固定した安全な版の pip を使うよう求めている。拒否する Python の版を使っていれば、pip は影響を受けない。
- **なぜ重要か**: 「pip の更新を、侵害された CA を信頼する pip でダウンロードする」という鶏と卵の問題があるので、更新の手順そのものを中間者攻撃から守る必要がある。CI のイメージや、古い Python を使う閉じた環境では、同梱の証明書ストアが更新されないまま残りやすい。
- 出典: [oss-security / Python security-announce (2026-11-20 UTC)](https://seclists.org/oss-sec/2026/q4/803) / [GHSA-6q48-6c7w-9gw2](https://github.com/advisories/ghsa-6q48-6c7w-9gw2) / [pip PR #14371](https://github.com/pypa/pip/pull/14371)

### [2026-11-21] ytnef 2.1.3: TNEF (winmail.dat) の解析にヒープのオーバーフロー。2017 年の CVE-2017-6302 の上限の確認が、符号なしの計算で回避できた
- **何が起きたか**: ytnef / libytnef の作者 Randall Hand 氏によると、`DecompressRTF()` の圧縮 (LZFu) のストリームで、ストリームが示す `uncompressedSize` の `INT_MAX` の確認 (CVE-2017-6302 の修正で追加) が符号なしの計算で評価され、回避できる。確保のサイズが桁あふれし、207 バイトの RTF のプリバッファが 1〜207 バイトはみ出して書き込まれる。非圧縮 (MELA) のストリームの範囲外読み取りと、NULL 参照も修正した。Evolution、Geary、Claws Mail の TNEF プラグインなどが、メールを受け取るだけで到達しうる。procmail のフック `ytnefprocess` は、カレンダーの項目経由で、利用者の操作なしに到達する。
- **なぜ重要か**: 「過去の CVE の修正が、型の扱いで無効になっていた」型。メールの添付を自動で処理する経路は、深掘りの Ghostscript と同じく、外部の送信者から直接届く入口になる。
- 出典: [oss-security (2026-11-20 UTC)](https://seclists.org/oss-sec/2026/q4/802) / [GHSA-jhg4-xcxm-cfg6](https://github.com/Yeraze/ytnef/security/advisories/GHSA-jhg4-xcxm-cfg6)

### [2026-11-21] 日経:「パッチ地獄」が米国の IT 障害を誘発。AI が見つける大量の脆弱性で修正を急ぎ、銀行や空港のシステムが止まる
- **何が起きたか**: 日経新聞によると、米国の銀行や空港でシステムの障害が相次いでいる。原因は個別に違うが、背景には、AI が膨大な数の脆弱性を見つけ、パッチの適用や更新を急がざるを得ない事情があるという。記事は 11/12 の Microsoft の障害などを例に挙げ、日本のインフラも同じリスクを抱えると指摘している (記事の大半は有料会員向け)。oss-security の投稿によると、同じ 11/21 には NYT も同じテーマで報じ、Upload2Shell に触れた。
- **なぜ重要か**: ITmedia エンタープライズが 11/19 に報じた「Windows の脆弱性の修正が 1 か月で前年 1 年分を超えた」流れ (背景) の帰結で、**脆弱性の発見の速さに、検証と適用の速さが追いつかない**。診断の報告でも、「全部すぐ直す」ではなく、悪用の有無や到達性で順位を付けた提案が求められる。
- 出典: [日本経済新聞 (2026-11-21)](https://www.nikkei.com/article/DGXZQOGN18CYM0Y6A111C2000000/)

### [2026-11-22] ランサムウェアの Hyflock、Samsung を被害者としてリークサイトに掲載 (主張のみ、未確認)
- **何が起きたか**: ransomware.live によると、Hyflock は 11/22 13:52 UTC に、Samsung (samsung.com) から 1TB のデータを盗んだとする投稿を出した。投稿では、初期の侵入口から 2 日間入り込み、ESX の管理者権限を取ったと主張している。ransomware.live は、この投稿を既存の項目の重複の可能性ありと表示している。Samsung の確認は見当たらない。
- **なぜ重要か**: 主張の段階で、事実かどうかはわからない。ただし「ESXi の管理者を取って暗号化」の手口は、ここ数年のランサムウェアの主流のままである。続報が出れば追う。
- 出典: [ransomware.live (2026-11-22)](https://www.ransomware.live/id/U2Ftc3VuZyBHcm91cDogMVRCIERhdGEgQnJlYWNoIGZyb20gUmFuc29td2FyZSBBdHRhY2tASFlGTE9DSw)

> CISA KEV は、11/20 の 4 件 (vCenter、Cisco Expressway、Apache Roller、SAP NetWeaver。11/21 号で既報) のあと、11/23 05:00 JST 時点で追加はない。

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 today-2 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先
> NVD の公開日は UTC。2026-11-20T15:00Z 以降 (= JST 11/21 以降) に公開されたものを対象にした。前号までに載せた CVE / GHSA は除いた。深掘りの CVE-2026-125396 は NVD の公開が 11/9 のため、この表には入れていない。EPSS は 11/23 時点の値。

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-120539 | Restrictions for BuddyPress (WordPress) ≤1.5.4 (修正 1.5.5) | CWE-95 / 9.8 | 要求の URI を、ダブルクォートの文字列の PHP 式に埋め込んで `eval()` → `{${...}}` の変数展開がクォートを抜けずに実行され、WordPress のスラッシュ付与も効かない → 未認証の GET 1 回で RCE (既定で有効、ログイン前に評価) | [release 1.5.5](https://github.com/seventhqueen/buddypress-restrict/releases/tag/1.5.5) (commit 不明) | 未認証 / EPSS 0.022 |
| CVE-2026-127027 | Poste.io <2.5.22 | CWE-78 / 9.2 (v4) | `dmarc-reports@<domain>` 宛のメールを送信者の検証なしに保存し、root のスクリプトが添付を安全でないシェルのコマンドで展開 → ファイル名やアーカイブの中身でコマンドインジェクション → 25 番ポートにメールを送るだけで、コンテナ内の root で RCE | [CERT Polska](https://cert.pl/en/posts/2026/11/CVE-2026-127027) (commit 不明、クローズドソース) | 未認証 / EPSS 0.042 |
| CVE-2026-133949 / GHSA-6q48-6c7w-9gw2 | pip <26.2.2 (同梱の certifi) | CWE-295 / 9.3 (v4) | 同梱の CA バンドルに、侵害された eMudhra の中間 CA が残っていた → pip の通信 (パッケージの取得) で中間者攻撃が成立しうる (侵害された中間 CA を拒否する Python なら影響なし) | [pip PR #14371](https://github.com/pypa/pip/pull/14371) | CVE-2026-115557 と組 / EPSS 0.0053 |
| CVE-2026-134347 / GHSA-8hcm-m7r7-frwc | actix-files <0.7.4 | CWE-58 / 8.7 (v4) | 先頭が `.` のファイルを隠す判定が、Windows の 8.3 の短い名前 (`ENV~1`、`GIT~1/config`) を考慮しない → 未認証で `.env` と `.git` の中身を取得 | [advisory](https://github.com/actix/actix-web/security/advisories/GHSA-8hcm-m7r7-frwc) (commit 不明) | 未認証 / Windows のみ / EPSS 0.011 |
| CVE-2026-134167 / GHSA-w72q-5vww-p2rh | devpi-web <5.2.0 | CWE-22 / 8.7 (v4) | `+doc` のルートの `docs_file_exists` / `docs_file_path` が `relpath` を文書のディレクトリに閉じ込めない → 先頭の `//` やパーセントエンコードした `..` で、パスワードハッシュを持つ keyfs の sqlite などを未認証で読み取り | [680fca1](https://github.com/devpi/devpi/commit/680fca1607840905dab6c54059b65ba326f46850) | 未認証 / EPSS 0.0081 |
| CVE-2026-134169 | Qwik City <1.20.3 / @qwik.dev/router <2.0.0-rc.4 | CWE-915 / 8.7 (v4) | フォームの POST を入れ子のオブジェクトにする `formToObj` が、文字列値の継承メンバーをたどるフィールド名を許す → 組み込み関数のプロパティを上書きし、`Object.prototype.hasOwnProperty.call` をプロセス全体で壊す (再起動まで DoS) | [5e95c55](https://github.com/QwikDev/qwik/commit/5e95c55e03c23efbf604118b8abe3a52554096ca) | 未認証 / EPSS 0.0075 |
| CVE-2026-94567 (+CVE-2026-94565 / GHSA-662q-v5rm-78gm ほか同時 5 件) | NukeViet CMS <4.5.12 / <4.6.02 | CWE-79, 434, 436 / 9.3 | SVG の内部 DTD のエンティティに `<script>` を隠すと、エンティティを展開せずに読み込む検査 (`check_svg_tmpfile`) と要素だけを見る `sanitize_svg_dom` をすり抜け、ブラウザが `image/svg+xml` として展開して実行 → 格納型 XSS (ゲストのコメントの添付が開いていれば未認証)。94565 は `/` を前置したイベント属性、54064 はフォームフィードを前置した属性で `filterAttr` を回避 | [912823e](https://github.com/nukeviet/nukeviet/commit/912823e2581afc23dc39dabdb7d94c718efc78f6) / [ef90780](https://github.com/nukeviet/nukeviet/commit/ef90780e50d54384019a36aa2bcf9fd58776f698) | 同型の回避が束で / EPSS 0.0088 |
| CVE-2026-129995 / GHSA-qwwm-vrm9-4mw8 (+CVE-2026-77383 / GHSA-4jx9-2fwj-pg4j) | mcp-ssh-manager <3.8.5 (77383 は <3.6.7) | CWE-78 / 8.8 (v3.1) | MCP のツール `ssh_backup_create` / `restore` / `schedule` / `list` が、呼び出し側の値 (DB 名、パス、除外、スケジュール、コメント) をそのまま遠隔のシェルのコマンドに組み立てる → 管理先のサーバーで任意のコマンド、`ssh_backup_schedule` で cron に常駐。`ssh_backup_list` はサーバーのポリシーの確認も通らない | [d40daa8](https://github.com/bvisible/mcp-ssh-manager/commit/d40daa8a43388dfaedf593bff18f0064d50f9633) / [4c19b35](https://github.com/bvisible/mcp-ssh-manager/commit/4c19b350f36f5f09f15662f8d19d2ba9cdf38bd0) | MCP / プロンプトインジェクションから到達しうる |
| CVE-2026-134452 / GHSA-8fh8-h5v2-wmj4 | Dockhand <1.0.57 | CWE-426 / 8.7 (v4) | スタックの秘密の環境変数を、予約済みのキー (`PATH` など) を除かずに `docker compose` の起動環境にマージ → `stacks:edit` の権限で `PATH` を悪意のあるバイナリのディレクトリに向け、デプロイでサーバーのプロセス権限の RCE | [advisory](https://github.com/Finsys/dockhand/security/advisories/GHSA-8fh8-h5v2-wmj4) (commit 不明) | Dokploy と同じ領域 / EPSS 0.0038 |
| CVE-2026-134359 / GHSA-mf65-hj88-hvrw | AzuraCast <0.24.1 | CWE-150 / 8.7 (v4) | Liquidsoap のアノテーションの値でバックスラッシュをエスケープしない → ID3 のタイトルの末尾を `\` にして引用を抜け、`process:` のプロトコルの URI を注入 → 再生時に Liquidsoap のコンテナで OS コマンド実行 (メディア管理者の権限) | [advisory](https://github.com/AzuraCast/AzuraCast/security/advisories/GHSA-mf65-hj88-hvrw) (commit 不明) | EPSS 0.0145 |
| CVE-2026-77326 | MapServer 8.2.0〜8.6.5 未満 | CWE-787 / 8.6 (v3.1) | WMS の `GetLegendGraphic` で、空でない `BBOX` と繰り返した `LAYER` を送ると、`msWMSDispatch()` が `ParamNames` / `ParamValues` に容量を確かめずに追記 → 未認証の 1 リクエストでヒープを破壊 (RCE は未実証) | [a7d5eb8](https://github.com/MapServer/MapServer/commit/a7d5eb844a59ea076b7972a018753242f18e6f7b) | 未認証 / EPSS 0.0096 |
| CVE-2026-134287 / GHSA-7jp3-2229-xgqj | OpenRemote core <1.34.0 | CWE-287 / 9.2 (v4) | MQTT の X.509 のプロビジョニングで、秘密鍵の所持を確かめずに「公開の証明書を送っただけ」で装置として認証 → 匿名の MQTT 接続が装置のサービスアカウントになり、資産を読み書き | [advisory](https://github.com/openremote/core/security/advisories/GHSA-7jp3-2229-xgqj) (commit 不明) | 未認証 / EPSS 0.0057 |
| CVE-2026-115407 / GHSA-c2cp-4qw8-q4jg | crypto11 (eclipse-keypont) ≤2.0.0-rc8 (旧パスの ThalesGroup / ThalesIgnite も) | CWE-323 / 9.1 | `SecretKey.NewGCM()` の AEAD が、nonce の長さを `NonceSize()` と照合せず空の nonce を受け付ける → 長さ 0 の IV を許すトークン (SoftHSM2 など) で毎回同じ IV になり、キーストリームの再利用と GHASH の鍵の露出 → 改ざんの偽造 | [8d99b73](https://github.com/eclipse-keypont/crypto11/commit/8d99b73c721c173ad85c0ca4e063c3da360a611d) | 暗号 API の誤用 / EPSS 0.0083 |
| CVE-2026-129794 (+129796 / 129797 / 129798 / 129811) | rt-labs の EtherCAT スレーブのスタック (RRTL-261119-01) | CWE-787 / 8.8 (AV:A) | EoE の断片の再構築で、ワイヤ上のフレームサイズを `memcpy` の上限に使い、受信バッファのサイズと比べない → マスターから最大 2,016 バイトの書き込み。CoE の SDO の分割ダウンロードでも、書いた総量を数えない・進行中でなくても書き込む・PDO のマッピングの合計長を確かめない、が同時に修正 | [RRTL-261119-01](https://docs.rt-labs.com/security/advisories/rrtl-261119-01.html) (commit 不明) | OT / 同じ型が 5 件 / EPSS 0.0044 |

**今日の CVE 所感**:
- 今日いちばん目立つのは、**「既存の検査を、別の解釈ですり抜ける」**型だ。NukeViet は「エンティティを展開しない検査」と「展開するブラウザ」、actix-files は「`.` で始まる名前の拒否」と「NTFS の 8.3 の別名」、devpi-web は `//` とパーセントエンコード、aiohttp (ニュース欄) は `.lower()` で ASCII に化ける Unicode。どれも、**検査する側と実際に使う側 (ブラウザ、OS、ファイルシステム) で、同じ値の解釈が違う**。
- actix-files の 8.3 の短い名前は、11/22 号の isomorphic-git の `.git::$INDEX_ALLOCATION` と同じく、**Windows 上で動く他言語の静的ファイルの配信** (Go の `http.FileServer` の自前のラッパー、Node の `serve-static` 系、Python の `aiohttp.web.static`、Deno / Bun の配信機能) で同じ確認が要る。`GET /ENV~1`、`/GIT~1/config` を Windows のサーバーで試す価値がある。
- Dokploy、Dockhand、mcp-ssh-manager、Poste.io、AzuraCast は、**「設定や引数の値を、シェルや別のプロセスの起動にそのまま渡す」**型。特に Dockhand の `PATH` の汚染は、「環境変数を利用者に設定させる」機能を持つ CI / PaaS / エージェントのツールに共通する (`LD_PRELOAD`、`NODE_OPTIONS`、`PYTHONPATH`、`GIT_SSH_COMMAND` も同じ sink)。予約済みのキーの拒否リストがあるかを、修正の diff で確かめたい。
- BuddyPress の `eval()` + ダブルクォートの変数展開 (`{${...}}`) は、PHP の古典的な型だが、WordPress のプラグインでは今も見つかる。`eval(` と `"...$_SERVER['REQUEST_URI']..."` の組み合わせで、プラグインのソースを横に grep すると効率がよい。
- 優先して見る順は、① Restrictions for BuddyPress と Poste.io (未認証の RCE、EPSS も高め)、② pip の certifi (CI のイメージの棚卸し)、③ actix-files と devpi-web (未認証の読み取り、診断で見つけやすい)、④ MCP の mcp-ssh-manager (エージェント経由で到達しうる)。

## 日本国内のセキュリティ動向

### 国内インシデント・事故

#### [2026-11-21〜22] タワーレコード、通販サイト「タワーレコード オンライン」への不正アクセスで、約 1,100 万件の個人情報が流出したと確認
- **何が起きたか**: タワーレコードの 11/21 の発表 (11/22 更新) によると、11/19 17:10 ごろに外部からの不正アクセスを確認し、サービスを止めた。流出したのは、ログイン情報 (メールアドレス、会員 ID、パスワードのハッシュ値) 10,214,652 件、会員情報 (氏名、フリガナ、ニックネーム、生年月日、性別、郵便番号) 2,784,514 件、配送先情報 (住所、宛名、電話番号) 776,953 件。退会して 3 年以内の人も含む。クレジットカード情報は含まれない。11/21 時点で二次被害は確認されていない。注文済みの商品は 11/23 から順次出荷し、マーケットプレイスは出品者向けの管理サイトの安全確認が続いていて再開は未定。侵入の原因は公表されていない。
- **なぜ重要か (評価)**: 1,000 万件を超える**パスワードのハッシュ**が流出した。ハッシュの方式 (bcrypt なのか、塩なしの高速なハッシュなのか) は公表されておらず、方式によっては解析されて、他のサービスへのリスト型攻撃に使われる。下のメルペイの件のような加盟店・事業者向けの管理画面への攻撃の材料にもなる。マーケットプレイスの出品者向け管理サイトを別に点検している点から、侵害の範囲は消費者向けのサイトにとどまらない可能性がある。
- 出典: [タワーレコード (2026-11-21 公開、11-22 更新)](https://tower.jp/info) / [NHK (2026-11-22)](https://news.web.nhk/newsweb/na/nd-20261122de79936)

#### [2026-11-21] ベストコ (個別指導塾「ベスト個別」など)、在籍者の保護者と子どもの氏名、成績、口座番号などが最大 50,196 件、問い合わせ情報が最大 95,937 件漏えいした可能性
- **何が起きたか**: ベストコによると、11/20 に、利用するシステムへの第三者の不正アクセスを確認した。11/20 までに在籍していた最大 50,196 件の顧客情報 (保護者と子どもの氏名、きょうだいの情報、住所、電話番号、メールアドレス、成績、入塾状況、口座番号・名義、月謝の金額、入金・引落の履歴、教育情報アプリの ID とパスワードなど) と、過去の問い合わせの情報 最大 95,937 件が漏れた可能性がある。原因と影響範囲は外部の専門機関と調査中で、二次被害は確認されていない。クレジットカード情報は含まれない。
- **なぜ重要か (評価)**: 子どもの成績と家庭の口座情報がまとまって持ち出された可能性があり、**塾や学校を装った詐欺 (引落の口座変更を求める連絡など)** に使われやすい組み合わせだ。教育情報アプリの ID とパスワードが平文で保存されていたのかは公表されていない。平文なら、同じ認証情報を使い回すほかのサービスに波及する。
- 出典: [ベストコ (2026-11-21)](https://bestco.jp/news/74/)

#### [2026-11-21] メルカリグループ、Notion AI の委託先 Fireworks AI への不正アクセスで、従業員が入力した記録の一部が流出した可能性。顧客 1,522 名分を含む計 3,796 名分
- **何が起きたか**: メルカリによると、11/10 に Notion 社から連絡を受けた。2026 年 10/5〜24 に、メルカリ、メルペイ、メルコインの従業員が Notion AI に入力した内容と回答の記録の一部が流出した可能性がある。含まれていた個人情報は、顧客 1,522 名分 (うち 1,061 名は顧客識別番号のみ。識別番号はログイン ID ではない)、取引先の担当者など 571 名分、採用の応募者 169 名分 (選考に関する情報を含む)、派遣社員・業務委託先・退職者 1,534 名分。**業務システムの認証情報の一部も含まれており**、確認できたものはすべて無効化と再発行を終えた。マイナンバー、カード番号、顧客のログインパスワードは確認されていない。メルカリのサービスやシステムへの不正アクセスは確認されていない。原因は、Notion AI の利用状況の分析 (Insights) のために Fireworks AI に送られた記録が、同社の環境に保存されていたことだとしている。
- **なぜ重要か (評価)**: 11/17〜20 号で追ってきた Notion AI の件で、国内の大手の公表としては最大級。**従業員が AI のチャットに業務システムの認証情報を貼っていた**ことが、公式の発表で確かめられた。AI の委託先の侵害では、「何を入力したか」の棚卸しが難しく、メルカリも一次調査の段階としている。社内の AI 利用のルールに、「秘密を貼らない」だけでなく、貼られた場合の検知 (DLP) と回収の手順を入れたい。
- 出典: [メルカリ (2026-11-21)](https://about.mercari.com/press/news/articles/20261120_incidentreport/)

#### [2026-11-21] メルペイ、加盟店向けの「メルペイ加盟店サービス」へのリスト型攻撃で、10 店のアカウントに不正ログイン。加盟店の関係者 13 名分の情報が閲覧・取得された可能性
- **何が起きたか**: メルペイによると、11/5 に第三者がリスト型攻撃とみられるログインの試行を繰り返し、10 店の加盟店のアカウントに不正にログインした。同日にログの監視で検知し、11/6 までにログイン状態の無効化とパスワードのリセットをし、追加の対策を入れた。それ以降、不正ログインの成功は確認されていない。11/13 以降、リスト型攻撃に対するログイン時の本人確認を強化した。メルペイからメールアドレスやパスワードが流出した事実、システムの脆弱性が悪用された事実は確認されていない。
- **なぜ重要か (評価)**: 件数は小さいが、**事業者向けの管理画面は、消費者向けのアプリより多要素認証の導入が遅れがち**で、リスト型攻撃の狙い目になる。上のタワーレコードのように大量のハッシュや ID が流出した直後は、こうした管理画面への試行が増えやすい。診断では、事業者向けのログイン画面のレート制限と、多要素認証の強制の有無を見たい。
- 出典: [メルペイ (2026-11-21)](https://jp.merpay.com/news/2026/11/202611_merpay/)

> このほか、カルチュア・エクスペリエンス、星槎道都大学、Peach Aviation (ユミルリンクの Cuenote FC 経由、8,997,106 件)、マネーフォワード、八十二長野銀行、東京都、日本マクドナルド、リクルートなどの 11/20 の公表は、採用範囲 (11/21 以降) の外のため本号では扱わない。KARTE の関連 (ZOZO、三井住友銀行など) と六花亭は前号までに収録済み。

### 国内の注意喚起・ガイドライン・政策

> 直近2日間に該当する新規ニュースは確認できませんでした。

(JPCERT/CC、IPA、NCO (国家サイバー統括室)、警察庁、総務省、経産省、金融庁、個人情報保護委員会の 11/21〜23 の新着は、RSS と各サイトの確認の範囲で見当たらなかった。土日と 11/23 の祝日が重なったためとみられる。最新の JPCERT/CC の PHP の注意喚起 (11/20 更新) と IPA の「PHP の脆弱性対策について」(11/20) は 11/21 号で収録済み。)

### 国内製品の脆弱性 (JVN)

> 直近2日間に該当する新規ニュースは確認できませんでした。

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| — | — | — | 11/21〜23 の JVN の新着なし (最新は 11/20 公開の 3 件で、前号までに収録済み) | — | [JVN](https://jvn.jp/) |

(JVN iPedia の新着も 11/19 登録分が最新で、採用範囲の外だった。)

### 国内コミュニティ・研究・イベント

#### [2026-11-22] loguru の `logger.exception()` は、既定の `diagnose=True` で、引数の API キー、ヘッダの辞書、`os.environ` 全体までログに書き出す (Qiita)
- **何が起きたか**: Qiita の記事 (SupportApp3 Lab) によると、loguru 0.8.0 (Python 3.13.5) で、ダミーの API キーを使って例外を起こし `logger.exception()` で記録したところ、関数の引数の API キー、`{"Authorization": "Bearer ..."}` のヘッダの辞書、行に `os.environ["MY_API_KEY"]` と書いていた場合は `os.environ` 全体の中身が、トレースバックにそのまま出た。`logger.add(..., diagnose=False)` か環境変数 `LOGURU_DIAGNOSE=NO` で止まった。loguru の公式のリファレンスにも、本番では `False` にすべきと書かれている。
- **なぜ重要か (評価)**: ソースコード診断で**すぐに確かめられる指摘項目**。`from loguru import logger` があり、`logger.add` に `diagnose=False` がないコードは、例外のログに秘密が出る。ログの集約基盤 (Datadog、CloudWatch など) に送っていれば、そこが漏えいの経路になる。上の Together AI の件と同じく、「意図しない場所に秘密が書かれる」問題だ。
- 出典: [Qiita SupportApp3 Lab (2026-11-22)](https://qiita.com/supportapp3/items/97b75e5b164c8e15cb0e)

#### [2026-11-22] AWS Continuum のペンテストの機能で、連携先の API を LLM に「動的に擬態」させた検証。エージェントは、遅延やヘッダ、エラーの文言から擬態を見抜いた
- **何が起きたか**: Zenn の記事 (nakayukl 氏) は、デプロイ前にペンテストを走らせる AWS Continuum で、連携先のサービスを LLM の動的な応答で置き換えた検証を報告した。単発の照会型のアプリなら固定のモックで十分で、複数のサービスの応答で次の呼び出しを決める「連鎖オーケストレーション」型で初めて LLM の擬態に意味が出るという。LLM の擬態は、応答の遅延、HTTP ヘッダなどの実行環境の特徴、エラーの文言といった「配送の層」の模倣が甘くなりやすく、ペンテストのエージェントが擬態だと見抜いた形跡が複数あった。
- **なぜ重要か (評価)**: AI のペンテストを本番の外で安全に回すための、具体的な設計の知見。逆から見れば、**攻撃側のエージェントもハニーポットや擬態を「配送の層」の手がかりで見抜ける**ことを示している。防御側の欺瞞 (デセプション) の設計にも使える。
- 出典: [Zenn nakayukl (2026-11-22)](https://zenn.dev/nakayukl/articles/0138545f239879)

#### [2026-11-22] (AI セキュリティ欄に掲載) Claude Code の禁止設定を python で迂回された実例と、第三者の Agent Skill の点検の手順
- 上の「AI セキュリティ」欄を参照。国内の開発者が、エージェントのガードレールの限界と、スキルの供給網の点検の方法を、再現の手順や照合のスクリプト付きで公開した。
- 出典: [Zenn sutokei (2026-11-22)](https://zenn.dev/sutokei/articles/edit-deny-python-bypass) / [Zenn nishi0001 (2026-11-22)](https://zenn.dev/nishi0001/articles/agent-skills-vetting-30-before-install)

<!-- bounty:start -->
## バグバウンティ・実践

> 実際の脆弱性報告・ライトアップから、次の診断で試せる学びを日本語で解説する欄。公開から 7 日以内のものが対象 (採用範囲の 2 日間とは別)。定期タスク「KEDA Daily Digest ページ更新」が、ページ版と同じ内容をここに追記している。

### [2026-11-21] Dokploy: 記号を止めただけの修正は「最初の語」を見ておらず、compose のコマンド欄に `run` で始まる文字列を入れるだけで、一般メンバーがホストの root に届く
- **種類**: Command Injection / 修正の回避 / 権限昇格
- **対象**: セルフホスト型の PaaS「Dokploy」の、compose サービスの任意入力欄 `command`。Ostorlab が 11/21 に、同日 oss-security に出た研究者の報告をソースで追って解説した。影響は 0.29.13〜0.31.4 (記事時点の最新) で、**修正版も CVE もまだ無い**。CVSS 9.9 は報告者の自己評価。
- **手口の肝**: 8 月の CVE-2026-72884 (同じ欄のコマンドインジェクション) は、0.29.13 で `sanitizeCommand` という検査を足して直した。この検査は、シェルの制御文字を正規表現で拒否し、`&&` でつないだ後ろの部分が `docker compose ` で始まることを確かめる。しかし**先頭の語は確かめていない**。検査を通った文字列は `getBuildComposeCommand` が固定の `docker` の後ろにそのまま並べ、`execAsync` (Node の `child_process.exec`、つまり `/bin/sh`) で実行する。そのため、記号を 1 つも使わずに `compose` の代わりに `run` で始まる文字列を入れると、`docker run ...` として動く。
- **影響の広げ方**: 必要なのは `service:create` の権限と、compose サービス 1 つへのアクセスだけ (既定のメンバーの役割が持つ)。Dokploy のサーバーは root で動き、標準の導入では `/var/run/docker.sock` をマウントしているので、ホストの `/` をマウントしたコンテナを root で起動でき、ホストのファイルと Docker デーモンに届く。研究者は自分の環境でホストに root 所有のファイルを書けることを確かめた。生の compose ファイルが `privileged: true` などを通すという 2 つ目の経路も報告されているが、Ostorlab は未検証としている。
- **自分の診断で試すこと**:
  - Docker のソケットを握る管理画面 (Dokploy、Coolify、CapRover、Portainer、CI の画面など) で、**利用者の入力が `docker` や `kubectl` の引数になる欄**を探す。記号を使わず、サブコマンドやオプションを変えるだけの値 (ボリュームの指定、`--privileged` など) が通るかを見る。エラーにならずデプロイのログに別のサブコマンドの出力が出れば当たり。
  - コマンドインジェクションの修正の diff を読むときは、「記号の拒否リスト」だけで直していないかを確かめる。先頭の語の許可リストや、引数を配列で渡す実装 (シェルを通さない) になっていなければ、引数の注入が残っている可能性が高い。
  - 同じ機能に入口が 2 つ (フォームの欄と、ファイルの丸ごとのアップロードなど) ある場合、片方にだけある検査 (`privileged`、`cap_add`、ホストのマウントの拒否) を、もう片方から送って通るかを比べる。
- 出典: [Ostorlab (Ostorlab Team)](https://blog.ostorlab.co/dokploy-compose-command-host-root.html)

### [2026-11-20] NukeViet CMS: SVG の検査は「エンティティを展開せずに要素だけ」見ていたので、内部 DTD のエンティティに隠したスクリプトが素通りし、問い合わせ欄では `/onerror` の形の属性が拒否リストを抜けた
- **種類**: Stored XSS / SVG / フィルター回避
- **対象**: ベトナム発の CMS「NukeViet」。SVG のアップロードの検査 (CVE-2026-94567、4.5.12 と 4.6.02 で修正) と、Contact モジュールのメッセージ (CVE-2026-94565、4.6.01 で修正) の 2 件で、どちらも 11/20 公開、CVSS 3.1 は 9.3。報告者の名前は読んだページには無かった。
- **手口の肝**: **SVG 側**: `NukeViet\Files\Upload::check_svg_tmpfile()` は文書をエンティティを展開しない設定で読み込むので、内部 DTD で定義したエンティティは「エンティティ参照」のノードのまま残る。続く `sanitize_svg_dom()` は要素のノードしか調べないので、エンティティの中に書いたマークアップは検査されない。しかも SVG は `verify_image()` の前に処理が終わり、元のバイト列のまま保存される。配信は `image/svg+xml` なので、ブラウザがエンティティを展開してスクリプトを実行する。**Contact 側**: `NukeViet\Core\Request::filterTags()` は属性を ASCII の空白でしか区切らないので、`/onerror` をひとつの属性名とみなし、`on` で始まる名前の拒否リストに当たらない。ブラウザはスラッシュを区切りとして扱い、`onerror` が動く。
- **影響の広げ方**: SVG は、モジュールのコメントが「全員」か「ゲスト」に開かれ、添付の許可 (`allowattachcomm`) が有効なら、**ログインなしで**置ける (モジュール管理者のファイル管理からも置ける)。Contact のメッセージは未認証で送れ、管理画面では出力時のエスケープなしで表示され、CSP も無いので、**管理者が開いた時点で管理画面と同じオリジンでスクリプトが動く**。どちらも、被害者が開くという操作が要る。
- **自分の診断で試すこと**:
  - SVG のアップロードを受け付ける機能では、`<script>` やイベント属性を直接書いた SVG が拒否されたあとに、**内部 DTD のエンティティに無害な目印の要素を入れた SVG** を送る。保存されたファイルを直接開き、エンティティが展開されて目印が描画されれば、検査側は展開前を見ていて、ブラウザ側は展開後を見ている (検査の抜け)。あわせて、配信の `Content-Type` が `image/svg+xml` か、`Content-Disposition: attachment` や CSP が付くかを見る。
  - HTML を一部許す入力欄 (問い合わせ、コメント、プロフィール) で、属性名の前に `/` や改ページなど「ブラウザは区切りとして扱うが、サーバー側の分割は区切りとして扱わない文字」を置いた属性を送り、保存後の HTML にイベント属性がそのまま残るかを見る。
  - 未認証で送れるフォームの内容が、**管理画面でどう表示されるか**まで追う。利用者向けの画面でエスケープされていても、管理者向けの一覧や詳細でそのまま出れば、管理者権限の乗っ取りにつながる。
- 出典: [Strix: CVE-2026-94567](https://www.strix.ai/cve/CVE-2026-94567) / [Strix: CVE-2026-94565](https://www.strix.ai/cve/CVE-2026-94565)

### [2026-11-21] WordPress の Restrictions for BuddyPress: リクエストの URI をダブルクォートの文字列に入れて `eval()` していたので、クォートを閉じなくても、ログインなしの GET 1 回で PHP が動く
- **種類**: Code Injection / PHP eval / 未認証 RCE
- **対象**: WordPress のプラグイン「Restrictions for BuddyPress」(スラッグは `bp-restrict`、seventhqueen 製) の 1.5.4 以前。CVE-2026-120539、CVSS 3.1 は 9.8。CVE の採番は Wordfence で、発見者は「snr」。9/30 に開発元へ通知され、11/20 に公表、対応版は 1.5.5。BuddyPress と Paid Memberships Pro の両方が有効なサイトが対象。
- **手口の肝**: プラグインは、リクエストの URI を、ダブルクォートで囲んだ文字列の PHP の式に埋め込み、それを `eval()` に渡していた (該当箇所は `includes/class-bp-restrict.php` など)。PHP はダブルクォートの文字列を組み立てる時点で、`{$...}` の形の複雑な構文を式として評価する。そのため攻撃者は**クォートを閉じる必要がなく**、URI に式を書くだけで実行される。WordPress は入力のクォートとバックスラッシュにスラッシュを付けるが、文字列の外に出ない攻撃なので、この守りは効かない。
- **影響の広げ方**: 問題の条件は既定で有効で、ログイン済みかどうかを確かめる前に評価されるので、未認証の GET 1 回で成立する。11/23 時点で KEV には入っていないが、PoC を名乗る公開物が検索結果に出ている (中身は読んでいない)。
- **自分の診断で試すこと**:
  - ソースコード診断では、PHP のプラグインやテーマを `eval(` で検索し、渡す文字列がダブルクォートで、`$_SERVER['REQUEST_URI']` やクエリの値が混ざっていないかを見る。`addslashes` 相当の処理があっても、`{$` を止めていなければ安全ではない。
  - 対象サイトで `/wp-content/plugins/bp-restrict/` の `readme.txt` などから版を確かめ、1.5.4 以前で BuddyPress と Paid Memberships Pro が有効なら、未認証の RCE として報告する (実行までは試さず、版と構成で判定する)。
  - 侵害の有無を見る場合は、アクセスログで URL エンコードされた波かっこや PHP らしい断片を含む URI を探し、アップロードやキャッシュのディレクトリの見慣れない `.php`、新しい管理者、mu-plugins と cron の変更を確かめる。
- 出典: [OpenCVE: CVE-2026-120539](https://app.opencve.io/cve/CVE-2026-120539) / [HOL Guard](https://hol.org/guard/security/cves/CVE-2026-120539-restrictions-for-buddypress-154-unauthenticated)

### そのほかのライトアップ

- **[2026-11-22] Dokploy: データベースのパスワード変更がバッククォートを通し、メンバー権限からサーバーのプロセス (多くは root) でコマンド実行 (CVE-2026-129987、0.31.1 で修正)** (Command Injection): MySQL、PostgreSQL、MariaDB、MongoDB、Redis の `changePassword` で、新しいパスワードをダブルクォートの中に入れてシェルに渡していた。検査はバッククォートを拒否しておらず、`service:create` を持つメンバーがコマンド置換で実行できた。0.31.1 は検査を変えず、引数をすべて引用の関数に通す形で直した。パスワード欄のような「記号を許したい入力」がシェルに届く経路は、他の管理画面でも確かめたい。 出典: [Helix Threat Watch](https://helix.ml/threat-watch/i/dokploy-authenticated-member-can-get-root-rce-via-database-password-injection-cve-2026-129987)
- **[2026-11-20] devpi-web: 文書を配信する `+doc` のルートが、パスを文書のディレクトリに閉じ込めておらず、未認証でパスワードハッシュ入りの sqlite を読める (CVE-2026-134167、5.2.0 で修正)** (Path Traversal): 社内の PyPI として使われる devpi の Web 画面で、`doczip.py` の `docs_file_exists` と `docs_file_path` が `relpath` を検査していなかった。先頭の `//` や、パーセントエンコードした `..` で、keyfs の sqlite (パスワードハッシュを含む) などサーバー上のファイルを読める。CVSS 3.1 は 7.5。診断先に devpi があれば、版が 5.2.0 以上かを確かめる。 出典: [Strix: CVE-2026-134167](https://www.strix.ai/cve/CVE-2026-134167) / [HOL Guard](https://hol.org/guard/security/cves/CVE-2026-134167-devpi-web-before-520-unauthenticated-path)
- **[2026-11-21] Rust の actix-files: 「`.` で始まるファイルは出さない」検査を、Windows の 8.3 形式の短い名前 (`ENV~1`、`GIT~1`) で抜けて `.env` や `.git` を読める (CVE-2026-134347、0.7.4 で修正)** (情報漏えい / パスの解釈の差): `actix_files::Files` は、要求された名前の先頭が `.` かどうかだけを見ていた。Windows では短い名前の別名が同じファイルを指すので、検査を通ったあとでファイルシステムが隠しファイルに解決する。未認証で成立し、CVSS 3.1 は 7.5。Windows で動く静的ファイルの配信では、言語を問わず同じ確認 (短い名前で `.env` や `.git/config` が返らないか) をする価値がある。 出典: [Strix: CVE-2026-134347](https://www.strix.ai/cve/CVE-2026-134347) / [RustSec advisory-db PR #3507](https://github.com/rustsec/advisory-db/pull/3507)

<!-- bounty:end -->

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 52 (RSS 39 本 [JVN、JVN iPedia、JPCERT/CC、JPCERT/CC Eyes、IPA、piyolog、Security NEXT、ScanNetSecurity、ITmedia (NEWS / AI+ / エンタープライズ / セキュリティ)、INTERNET Watch、LAC WATCH、GIGAZINE、Publickey、BleepingComputer、The Hacker News、The Record、SecurityWeek、Help Net Security、Dark Reading、Krebs、Ars Technica、TechCrunch AI、The Verge AI、Simon Willison、Embrace The Red、OpenAI、Google AI Blog、Hugging Face、MSRC、CISA、GitHub Advisories、oss-security、Talos、Unit 42、watchTowr、Project Zero、arXiv]、Zenn のトピック 4 本、Qiita、はてなブックマーク、HN (hnrss)、NVD API、EPSS API、CISA KEV JSON、セキュリコの国内事案一覧、各組織の発表ページ、WebSearch 約 12 回)
- 採用件数: AI技術=6 / AIセキュリティ=5 / セキュリティ=9 / CVE=14 / 国内インシデント=4 / 国内政策=0 / JVN=0 / 国内コミュニティ=3 (うち 1 件は AI セキュリティ欄と共有)
- 除外理由内訳: 古すぎ=約 25 (国内の 11/20 公表 10 件超 [カルチュア・エクスペリエンス、Peach Aviation、マネーフォワードなど]、GIGAZINE の「仲間の AI に秘密を漏らす」実験 [元の報道は 11/6]、GIGAZINE の中国の AI 教育 [ロイター 11/16]、IDC の調査 [発表 11/17]、EU AI Office の OpenAI / Anthropic への情報提供要求 [10/14]、Phala の報告 [11/10]、Anthropic の電源構成の記事 [11/16]、arXiv の 11/19 投稿分) / 重複=約 30 (Signal の画面撮影の制限、Cairn、Bell Canada、NCIC、BADBOX、Entra Connect Health、GPGME、Meta Muse、Riemann の初報、Inkling 2 Mini、vCenter の Armory Castle [11/20 号]、Java4Shell、Optimizely、KARTE の関連、六花亭、デジタル庁の GSS、RansomwareHelp、West Virginia 州議会、Container Store、Kirsten Davies 氏の指名など) / 日付不明・一次情報なし=3 (インフキュリオンの Wallet Station の第 3 報 [一次の発表を確認できず]、EU AI Act の件の詳細 [低品質の二次情報のみ]、TechCrunch のテキストメッセージの AI エージェント一覧 [まとめ記事のため見送り])
- 取得失敗ソース: Dark Reading (Cloudflare のチャレンジで本文取得不可。vCenter の Armory Castle の記事は THN で代替し、11/20 号で既報と判断)、ベスト個別のサイト (プロキシの 502。ベストコの本社サイトで代替)、日本経済新聞 (有料部分は取得不可。冒頭のみで要約)、hn.algolia.com (JSON を返さず、hnrss.org で代替)、GitHub 上のリポジトリ (セッションのアクセス範囲外。Inkling-2-Mini の量子化のリポジトリは見送り)、arXiv API (cs.CR の最新は 11/19 投稿で、採用範囲の公開分なし)
- 備考: 11/23 は祝日で、国内の公的機関・JVN の更新が止まっている。主要メディアがプロキシで取得できない場合は、ベンダーの一次発表 (OpenRouter、Together、Novita、各社のプレスリリース) と oss-security で代替した。

</details>
