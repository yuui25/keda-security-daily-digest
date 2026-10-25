# KEDA Daily Digest — 2026-10-26 (JST)

> 採用範囲: 公開日 2026-10-24 〜 2026-10-26
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

週末 (10/24〜25) をはさんだため、ベンダーの研究ブログや国内の公的機関の発表はほとんどなかった。その分、実際に悪用が確認されている話と、攻撃面の「仕様の隙間」を突く話が目立った。
- **セキュリティ (最優先)**: Wiz が、盗んだ GitHub トークンでアクセスできる全リポジトリに secrets を抜き出す workflow を仕込むキャンペーン「Gheist」を公表した (850 超のアカウント、1 万 3,500 超のブランチ)。公開リポジトリは GitHub の承認保留で止まっているが、プライベートリポジトリと GHES では実行され、その後に AWS Secrets Manager が列挙されていた。今日まず見るべき 1 件で、深掘りで扱う。
- **セキュリティ (ほか)**: Tailscale SSH の未修正の欠陥「Tailworm」(ACL で SSH を許された先の root を取れる、CVE・修正版なし)。PHP2Shell では欧州の政府機関で侵害の成立が確認され (Unit 42)、PAN-OS / Panorama 向けのホットフィックスも出始めた。CISA KEV の追加はなく、10/23 追加の Arista・Collabora の対応期限が今日 10/26。
- **新規 CVE**: VulnCheck が rclone・vLLM・SiYuan・Snipe-IT・Parse Server の GHSA をまとめて CVE 化した。「検証した範囲と使う範囲のずれ」型 (rclone selfupdate の署名外の checksum 行、adm-zip の正規化前の重複検査、SiYuan の `\\?\`、Firecrawl の DNS rebinding) と、Perl PSGI サーバー群の HTTP の基本規則違反が中心。
- **AI**: 大型のモデル発表はない。Anthropic が「サブエージェントより単一エージェント」を勧め、OpenAI が最大 90% の値引きで Anthropic の顧客を奪っているとの報道がある。AI セキュリティでは、~/Downloads に置かれた AGENTS.md でコーディングエージェントを乗っ取る手口 (実環境で 1 件観測) と、vLLM の 10 件の CVE が実務に近い。
- **国内**: GMO「お名前.com デスクトップクラウド」で、攻撃者が **10/27 正午** を期限に 100 万ドルを要求し、利用者 PC の乗っ取りを予告した。GMO は第 5 報で利用者に端末のフルスキャンを求め、代表は「社内から課題を指摘されていた」と認めた。ブラストメールの波及でピッコマのメルマガ宛先 100 万件が流出し、システムファイブ (最大約 15,000 名)、チャリロト (373 名、口座情報まで) の公表も続いた。JVN は 10/23 以降の新規公開がなく、JVN iPedia は停止したまま。

## 今日の深掘り

### Gheist — 盗まれた GitHub トークンで「全リポジトリに secrets を吐く workflow」を自動で仕込む。公開リポジトリは止まったが、プライベートリポジトリと GHES では成立している

- **概要 (事実)**: Wiz Research (Rami McCarthy 氏、Hila Ramati 氏) は 10/25、9/15 から追跡しているキャンペーン「Gheist」を公表した。名前は、ツールが GitHub API に送る User-Agent `gheist` に由来する。盗まれたトークンでアクセスできるリポジトリごとに `ci-sync-` + 6 文字のブランチを作り、`.github/workflows/sync-check.yml` をコミットメッセージ `ci: sync config` でコミットする。push イベントで workflow が起動し、secrets がログに出力される。ツールはログを API で取得し、数秒後に run を削除する。Wiz は 850 超のアカウントから 1 万 3,500 超のブランチを回収した。10/24 時点で攻撃は続いており、手口も変わり続けている。関係したアカウントの約 3 分の 2 は、すでに GitHub 上から消えている。
- **技術的な中身**: Wiz は、次の 3 点がそろうと成立すると説明している。
  - GitHub のログのマスクは、secret の値がそのままの形で出たときだけ働く。`env | base32` と `toJSON(secrets) | base32` で出せば、マスクされずに全文が残る。
  - `permissions: {}` は `GITHUB_TOKEN` の権限を絞るだけで、secrets コンテキストは制限しない。
  - deployment environment があるリポジトリでは、job matrix に `environment: ${{ matrix.environment }}` を並べ、環境スコープの secrets (本番の資格情報であることが多い) も出させる。
  
  secrets は GitHub 自身の API を通って出ていくので、遮断すべき攻撃者のドメインや外向きの通信がない。10/19 には、self-hosted runner が登録されたリポジトリだけを狙う 2 つ目のジョブ `sync-host` が加わった。このジョブは次のものを探す。
  - ホームと作業ディレクトリにある 31 種類のトークン形式 (Anthropic・Hugging Face などの AI 系の API キーを含む)
  - `/proc/*/environ`
  - Docker ソケットでホストのルート FS をマウントしたコンテナからの、ホスト側の同じ探索
  - IMDS (AWS / GCP / Azure)
  - Actions / GitLab runner の資格情報ファイル
  - K8s の ServiceAccount トークン
  
  Wiz は、このジョブにはバグが多く、一部は機能していないと評価している。
- **成立範囲**: GitHub は 7/28 から、公開リポジトリで疑わしい workflow run を collaborator が承認するまで保留している。Wiz が確認した公開リポジトリの run は、すべて `action_required` で止まっていた。一方、この保留はプライベートリポジトリと GitHub Enterprise Server には適用されない。そうした環境では、`ci-sync-*` ブランチの run が完了してから削除された記録が監査ログに残っていた。CloudTrail には、自組織の workflow がそのブランチ上で AWS のロールを引き受けた記録も残っており、数時間後には同じ組織の資格情報で AWS Secrets Manager が列挙されていた。トークンの入手元として Wiz がたどれたのは、インフォスティーラーのログと、3 月の Trivy の侵害など過去のサプライチェーン攻撃で漏れたトークンである。同じアカウント群は、クラック版ソフトの偽リポジトリ (10/6、391 アカウントが約 1,461 リポジトリを改名) や、北朝鮮系とされる PolinRider の `vite.config.js` への追記にも使われていた。
- **背景・経緯 (過去の事象の引用)**: CI のログから secrets を取り出す手口には前例がある。2025 年 3 月の tj-actions/changed-files の改ざん (CVE-2025-30066) では、secrets を二重の base64 でログに出してマスクをすり抜けた。Gheist はこの「エンコードしてマスクをすり抜ける」手口を、「盗んだトークンで全リポジトリに自動で仕込む」形に広げたものと位置づけられる。なお Wiz は、secrets を 193.32.204[.]199 に送る別キャンペーン GhostAction とは別物だとしている。
- **なぜ今これが重要か (評価)**: Gheist の手口は、CI/CD 診断の確認項目にそのまま使える。とくに次の 3 点は誤解されやすい。
  - `permissions: {}` を書いても secrets は守れない。
  - ログのマスクは、エンコードされた値には効かない。
  - 公開リポジトリ向けの承認保留は、プライベートリポジトリと GHES には効かない。
  
  push 権限のあるトークン 1 本で、そのトークンが届く全リポジトリの secrets、環境スコープの本番資格情報、さらに OIDC で信頼された AWS ロールまでたどれる。この構図は、ペンテストでトークンを 1 本拾ったときの影響評価の物差しにもなる。self-hosted runner の Docker ソケットとメタデータへの到達は、ジョブ自体にバグがあっても設計上の弱点として残る。攻撃者がジョブを直せば、すぐに成立すると考えるべきである。
- **読者が今日できること**:
  - ハント: 組織内で `^ci-sync-[0-9a-z]{6}$` のブランチ、コミットメッセージ `ci: sync config`、User-Agent `gheist` を検索する。GitHub の監査ログでは、完了から 1 分以内に削除された run を探す。self-hosted runner では `.gdmp_pat` / `.gdmp_patg` / `.gdmp_sweep` と、ログ内の `gdmp-pivot` を探す。
  - GitHub のログがなくても見つけられる方法: CloudTrail (または GCP / Azure の監査ログ) で、OIDC の `sub` クレームに `ci-sync-` を含む AssumeRoleWithWebIdentity を検索する。あわせて、OIDC の信頼ポリシーが `ref:refs/heads/main` や `environment:prod` などに絞られているかを確認する (`repo:org/*:*` のようなワイルドカードは危険)。
  - 硬化: 本番の secrets を持つ environment に required reviewers を設定する。PAT を GitHub App や短命の fine-grained token に置き換える。self-hosted runner は ephemeral にし、Docker ソケットを渡さず、IMDS を制限 (IMDSv2 + hop limit 1 など) する。痕跡が見つかったら、run やブランチを消すだけでは足りない。そのリポジトリから届くすべての secrets をローテーションする。
- 出典: [Wiz Blog (2026-10-25)](https://www.wiz.io/blog/gheist-attempted-scaled-abuse-of-stolen-github-tokens-stumbles) / 背景: [NVD CVE-2025-30066](https://nvd.nist.gov/vuln/detail/CVE-2025-30066) / [CISA (tj-actions/changed-files)](https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction)

## AI 技術・トレンド

### [2026-10-25] Anthropic「サブエージェントを並べるより、1 体のエージェントに必要な文脈を都度読ませる方がよい」と推奨し、移行キットを GitHub で公開
- **何が起きたか**: Anthropic の Applied AI チームが企業導入の経験をもとに、複数のサブエージェントを、スキルとツール検索で文脈を都度読み込む単一のエージェントにまとめられないか検討するよう勧めた。比較した構成の 1 つでは、単一エージェントの方が約 2 倍速かったという。Claude Code のシステムプロンプトは新しいモデル向けに 80% 以上削ったとし、ツール定義が 30〜50 個を超えるとツール選択が劣化するとも述べている。サブエージェントが向くのは、文脈の劣化が測れる場合、並列の別コンテキストが必要な場合、ツール選択に失敗する場合とした。
- **なぜ重要か**: エージェントの数と受け渡しの回数が減れば、攻撃面と監査の対象も小さくなる。ただし Anthropic 自身も、統合によって既存の処理が壊れた例を挙げており、まとめるときは回帰テストが前提になる。
- 出典: [The Decoder](https://the-decoder.com/anthropic-says-one-ai-agent-beats-many-subagents-now-that-models-can-handle-complexity-alone/)

### [2026-10-25] OpenAI、最大 90% の値引きで Anthropic の大口顧客を奪う (The Information 報道)
- **何が起きたか**: The Information の報道を The Decoder が要約した。Rippling ではコーディング作業に占める OpenAI の割合が 16% から 52% に増え、Anthropic は 57% から 18% に減った。Replit は年 1 億ドル超の契約で 30% 超の値引きを受けて乗り換え、DataCamp の CEO はコストが 80〜90% 下がったと述べている。投資家向けメモによると、Anthropic の成長は Q2 から Q3 にかけて鈍化した。
- **なぜ重要か**: フロンティアモデルの価格競争が進むと、社内で使うコーディングエージェントのモデルが短い期間で入れ替わりうる。データの取り扱い条件や監査ログ、権限の設計をモデルごとに見直す手間が増える。
- 出典: [The Decoder](https://the-decoder.com/openai-offers-discounts-up-to-90-percent-to-poach-anthropics-biggest-customers/)

### [2026-10-24] Microsoft Research、司令役を置かない多数エージェントのハーネス「Agensh」をオープンソース化。1,024 体まで拡張
- **何が起きたか**: 各ワーカーが自分でサブタスクを宣言 (CLAIM) し、Gitea の共有リポジトリへのマージと Mattermost のチャンネルで調整する分散型ハーネス。ProgramBench で 1〜1,024 体まで試し、GPT-6.1 Sol を使った 32 体の構成で pandoc の合格率は 79.59% だった。一方、最難関 5 タスクの平均は 128 体でも 28.78% にとどまり、1 体から 8 体に増やしても伸びは 1.37 ポイントだった。基盤は GitHub Copilot CLI で、薄いアダプターを書けば Claude Code などもつなげるという。
- **なぜ重要か**: 数百体のエージェントが同じリポジトリに書き込む構成では、1 体がプロンプトインジェクションを受けると他の個体にも波及しうる。権限の分け方とマージの検証が新しい論点になる。
- 出典: [MarkTechPost](https://www.marktechpost.com/2026/10/24/microsoft-agensh-multi-agent-harness-1024-agents/)

### [2026-10-25] Jack Clark 氏、「自己改良する AI」の到来予測を 2027 年に前倒し。根拠は「研究センス」を測る TasteVal
- **何が起きたか**: P-Zero Research の TasteVal は、AI が実験を設計し結果を解釈する力を「専門家と同じスコアに届くまでに使う計算量」で測るベンチマーク。最上位の Opus 5.5 は compute multiplier 2.3 (幅 1.15〜4.37) を記録し、この値は 2025 年 12 月以降、約 3 か月ごとに倍になっているという。Anthropic 共同創業者の Jack Clark 氏は、再帰的な自己改良 (RSI) の到来予測を 2028 年から 2027 年に早めた。著者ら自身は、改善の速さを過大に見せている可能性を認めている。
- **なぜ重要か**: 安全性の議論でどの数字が根拠にされているかを押さえておくための材料。測っているのは研究作業のごく一部で、比較対象の人間にトップクラスの研究者は含まれていない。
- 出典: [The Decoder](https://the-decoder.com/anthropic-co-founder-jack-clark-moves-his-prediction-for-self-improving-ai-forward-to-2027/)

### [2026-10-25] オープンなスマホ操作エージェント「OpenMobile-2」(9B / 27B)。約 110 のアプリ環境で学習し、実機の SPA-Bench でオープンモデル最高の 59.6
- **何が起きたか**: 南京大学や SenseTime などが、Qwen3.5 9B と Qwen3.6 27B をもとにした 2 モデルと、訓練環境・データ一式を公開した。Taobao や Slack など 35 のアプリを再現した環境で学習し、27B モデルは AndroidWorld で 79.9、実機の SPA-Bench で 59.6 を記録した。データ量を同じにしてアプリの種類だけを増やすと、未知のアプリでの成功率が 60.7% から 67.5% に上がった。教師モデルには Gemini 3.1 Pro を使っている。
- **なぜ重要か**: 実機を操作できるオープンなエージェントが誰でも使えるようになった。画面の内容を介したプロンプトインジェクションや、モバイルアプリの自動化された不正操作を検証するための土台にもなる。
- 出典: [The Decoder](https://the-decoder.com/openmobile-2-proves-open-source-smartphone-agents-can-rival-proprietary-models/)

### [2026-10-25] Hugging Face、DNA と英語を 1 つのモデルで扱う「Carbon-X」(14.8B) を Apache 2.0 で公開
- **何が起きたか**: Qwen3-14B に DNA 用のトークン 5,515 個を追加したデコーダーのみのモデルで、コンテキストは 40,960 トークン。変異の病原性の予測などを行い、5 つの DNA ベンチマークの平均は 66.7% (自己申告)。80GB の GPU 1 枚で動き、GGUF 版 (Q4_K_M は 9.6GB) もある。
- **なぜ重要か**: 機微な配列データを社外に出さずに扱える一方で、バイオ分野の重みをオープンにすることには二重用途の論点がある。
- 出典: [MarkTechPost](https://www.marktechpost.com/2026/10/25/hugging-face-carbon-x-14b-dna-language-model/)

### [2026-10-24] 中国の Nanbeige、エージェント向けの「Nanbeige4.3-33B」を Apache 2.0 で公開。同じ規模の Qwen3.8-27B を多くの指標で上回ると主張
- **何が起きたか**: Nanbeige4.3 シリーズの教師モデルという位置づけで、今後は 3B などの小型モデルへ蒸留する予定。モデルカードの自己申告では、Terminal-Bench 2.1 が 80.9 (Qwen3.8-27B は 73.0)、DeepSWE が 65.5 (同 42.5) だった。SWE-Bench Pro (60.3 対 61.7) と GDPval では Qwen が上回っている。第三者による再現はまだない。
- **なぜ重要か**: 約 30B のオープンウェイトモデルでも、ローカルで動くコーディングエージェントが実用的な水準に近づいている。社内で使う場合は、配布元と重みの来歴の確認が要る。
- 出典: [Hugging Face: Nanbeige/Nanbeige4.3-33B](https://huggingface.co/Nanbeige/Nanbeige4.3-33B)

### [2026-10-25] 皮膚がんの診断で、10 年前の CNN (Inception v3) が GPT-6 Astra と Claude Fable 5.1 を上回る — 皮膚科医の比較実験
- **何が起きたか**: 生検で確定した 200 病変 (公開データセット MILK10k) を使い、6 つの診断名から選ばせた。約 20 分ファインチューニングした Inception v3 の正答は 125 件 (62%) で、2 つのフロンティア LLM は 84 件と 85 件 (42%) だった。厚さ 0.8mm 未満の浸潤性メラノーマを、両 LLM とも「良性で退院可」と判定した例も示している。個人の研究室ブログで、査読はされていない。
- **なぜ重要か**: 汎用 LLM を専門領域の判定にそのまま使う前に、小さな専用モデルと比べて評価する必要があることを示す例。AI 製品のリスク評価でも、比較対象 (ベースライン) をどう取るかが論点になる。
- 出典: [Lynch Lab](https://lynchlab.net/llm-skin-cancer)

### [2026-10-25] r/opensource が「AI を使う・AI が作った・AI 向け」のプロジェクトの投稿を禁止。反発してフォーク版のサブレディットもできる
- **何が起きたか**: Reddit の r/opensource のモデレーターが土曜の夜に新しい投稿ルールを出した。「AI を使う、AI が作った、AI 向けのプロジェクトは歓迎しない」とし、メンテナンスやコントリビューター数の最低基準も厳しくした。反発から r/trueopensource ができた。モデレーターは、アクセシビリティ機能などの例外は個別に判断するとしている。
- **なぜ重要か**: 先週の curl の方針変更 (AI 生成の報告を理由に Low/Medium を公開で扱う) に続き、OSS コミュニティで AI 生成物を拒む動きが広がっている。脆弱性の報告や PoC の受け入れ方にも影響しうる。
- 出典: [The Verge](https://www.theverge.com/ai-artificial-intelligence/1018217/reddit-opensource-ai-ban)

### [2026-10-25] (参考) Apollo のエコノミスト「AI はテック以外の米企業に財務上の見返りを『まったく』もたらしていない」
- **何が起きたか**: Apollo Global Management のエコノミストが、巨額の投資と期待にもかかわらず、テック業界以外の企業では AI による財務上の効果がまだ見えていないとの見方を示し、TechCrunch が報じた。
- **なぜ重要か**: AI の投資効果を疑う見方が出てくると、企業が AI の導入にかけるセキュリティ予算や体制づくりの優先度にも影響しうる。
- 出典: [TechCrunch](https://techcrunch.com/2026/10/25/ai-delivers-zero-financial-payoff-to-most-companies-according-to-apollo-economist/)

### [2026-10-26] 【国内】安川電機、AWS と組み、利用者の要望を生成 AI がロボットの作業内容に変換する仕組みを構築。食品工場などへの展開を狙う
- **何が起きたか**: 日経クロステックによると、安川電機は AWS と連携し、クラウド上の生成 AI が人の要望をロボットが処理できる作業内容に変換するシステムを構築した。人がロボットに作業を教え込む負担を減らし、ロボットの導入が進んでいない食品工場などへの普及を狙う (記事の詳細は有料会員限定)。
- **なぜ重要か**: 国内でも、LLM がロボットの作業指示を作るフィジカル AI が実際に導入される段階に入った。先週の「MuTRAP」(タスク計画用 LLM へのバックドア) のような、指示を書き換える攻撃が工場の現場の安全に直接つながる構成である。
- 出典: [日経クロステック](https://xtech.nikkei.com/atcl/nxt/column/18/00001/12110/)

### [2026-10-26] 【国内】建設現場への生成 AI の導入、施工管理などの中核業務はまだ道半ば。国土交通省は直轄業務での活用に本腰
- **何が起きたか**: 日経クロステックによると、国土交通省は生成 AI を積極的に使う方針を示し、環境の整備を始めた。直轄業務では 2026 年度から積極的に導入する一方、施工管理など現場の中核業務への導入はまだ途上だという (記事の詳細は有料会員限定)。
- **なぜ重要か**: 官公庁の発注業務に生成 AI が入ると、受注側の建設会社やコンサルタントにも、データの扱いと AI の利用ルールへの対応が求められるようになる。
- 出典: [日経クロステック](https://xtech.nikkei.com/atcl/nxt/column/18/03804/101900001/)

## AI セキュリティ

### [2026-10-25] Downloads フォルダに置かれた AGENTS.md でコーディングエージェントを乗っ取る。Codex では 90%、Claude Code では OAuth トークンを抜く手法が約 50% で成功 (AI coding agents hijacked using AGENTS.md file in Downloads folder)
- **何が起きたか**: Forever Security が顧客の端末で、`~/Downloads` を作業ディレクトリにして起動したエージェントが悪性の npm パッケージ `function-color` を入れようとした事例を見つけた。原因は同じフォルダにあった悪性の AGENTS.md だった。研究者は、Web ページから AGENTS.md を利用者に気づかれずにダウンロードさせる PoC を作った。OpenAI Codex で計算機を起動させる試験は 90% 成功した。Claude Code では悪性の CLAUDE.md で API 通信を自分のサーバーに向けさせて OAuth トークンを奪い、偽のツール呼び出しを返してコードを実行させる手法が約 50% 成功した。Claude Code が Downloads から起動されたセッションは 1,300 件を超えるという。研究者は「OpenAI や Anthropic が直すべきものはない」と述べている。
- **なぜ重要か**: ブラウザの自動ダウンロードとエージェントの指示ファイルの自動読み込みは、どちらも仕様どおりの動作で、組み合わせると攻撃になる。CVE が付かないため、診断や社内のルールで「信頼できないディレクトリでエージェントを起動しない」「API の接続先 (base URL) の上書きを監視する」と明記しておく必要がある。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/ai-coding-agents-hijacked-using-agentsmd-file-in-downloads-folder/)

### [2026-10-25] 推論サーバー vLLM の脆弱性 10 件が NVD に一斉登録。KV キャッシュのテンソルが漏れる SSRF (CVSS v4 8.8) と、他の利用者の要求も巻き込むエンジン停止が中心
- **何が起きたか**: CVE-2026-116172〜116181 (VulnCheck が採番)。CVE-2026-116176 (v0.9.2〜0.24.0 未満) は、`X-Request-Id` ヘッダーに埋め込んだ接続先へ P2pNcclConnector の prefill ワーカーが ZMQ で接続してしまう SSRF で、NCCL の unique_id や KV キャッシュのテンソルが漏れうる。ほかは、Rust gRPC フロントエンドでの入力検証漏れ、音声と画像の解凍爆弾 (Nemotron-VL のプロセッサが `MAX_IMAGE_PIXELS` を None にしていた)、`num_frames=-1` の指定、語彙外の stop_token_ids による GPU 上の範囲外書き込みなどで、いずれも EngineCore の停止やメモリ枯渇につながる。修正版は欠陥ごとに 0.24.0 から 0.31.0 まで分かれている。
- **なぜ重要か**: 社内の LLM 基盤を診断するときは、OpenAI 互換 API や gRPC、マルチモーダルの入力を DoS と SSRF の観点で見る価値がある。複数のテナントが同じエンジンを共有している場合、1 件の要求で全員のリクエストが落ちる。
- 出典: [NVD CVE-2026-116176](https://nvd.nist.gov/vuln/detail/CVE-2026-116176) / [GHSA-vfp2-c8pq-v6h6](https://github.com/vllm-project/vllm/security/advisories/GHSA-vfp2-c8pq-v6h6) / [GHSA-mm38-5g96-7j6x](https://github.com/vllm-project/vllm/security/advisories/GHSA-mm38-5g96-7j6x)

### [2026-10-25] MCP ツールの経路から秘密ファイルを読める CVE が 2 件: SiYuan の MCP アセットツール (CVE-2026-116168) と designer-mcp (CVE-2026-116045)
- **何が起きたか**: ノートアプリ SiYuan の 3.8.7 未満では、MCP のアセットアップロード操作の禁止パス一覧から `.env` などが漏れていた。そのため、MCP を操作できる認証済みの攻撃者がローカルの秘密ファイルをワークスペースにコピーし、`/assets/` 経由で HTTP で読み出せる (CVSS v4 6.9、GHSA-q768-4j87-gf3w)。designer-mcp (2.1.0 まで) の `get_reference` にはパストラバーサルがあり、exploit は公開済み。
- **なぜ重要か**: MCP のツールに渡す引数は、プロンプトインジェクション経由で攻撃者が操れる入力として扱う必要がある。禁止パスを一覧で列挙する方式は抜けが出やすく、診断でまず確かめるべき箇所である。
- 出典: [NVD CVE-2026-116168](https://nvd.nist.gov/vuln/detail/CVE-2026-116168) / [GHSA-q768-4j87-gf3w](https://github.com/siyuan-note/siyuan/security/advisories/GHSA-q768-4j87-gf3w) / [NVD CVE-2026-116045](https://nvd.nist.gov/vuln/detail/CVE-2026-116045)

### [2026-10-24] Unitree の四足ロボット Go2 で、AI チャットモジュール (chat_go / gpt_thread.py) にリモートから突ける OS コマンドインジェクション (CVE-2026-115995)
- **何が起きたか**: ファームウェア 1.1.11.4 までの Go2 で、`gpt_thread.py` の `set_volume` 関数に渡す値の扱いに欠陥があり、OS コマンドを注入できる。VulDB の経由で報告され、ベンダーは社内チケット #474 として確認し、1.1.11.5 で修正した。
- **なぜ重要か**: LLM と連携する機能の周りに、従来型のコマンドインジェクションが残っていた例。ロボットでは物理的な影響が出うる。この種の機器を診断するときは、LLM がツールとして呼ぶ関数 (この例では音量の設定) の引数を、プロンプトインジェクション経由で攻撃者に操られうる入力として扱う必要がある。
- 出典: [TheHackerWire / CVE-2026-115995](https://www.thehackerwire.com/vulnerability/CVE-2026-115995/) / [VulDB](https://vuldb.com/vuln/426093)

### [2026-10-24] 米 Johns Hopkins Bayview Medical Center、職員が患者の医療情報を未承認の公開 AI ツールにアップロードし、3,182 人に通知
- **何が起きたか**: Baltimore Sun によると、同センターは、職員が個人の医療情報 (PHI) を承認されていない公開の AI ツールにアップロードしたとして、患者 3,182 人に通知した (記事の詳細は有料)。
- **なぜ重要か**: 先週の国内のパナソニック系の事案 (約 33 万 4,000 人分) と同じ型の「シャドー AI」による情報漏えいで、米国では HIPAA の報告対象になっている。DLP やブラウザ拡張で生成 AI への送信を制御しているかは、監査や診断の確認項目として定着しつつある。
- 出典: [Baltimore Sun](https://www.baltimoresun.com/2026/10/24/johns-hopkins-bayview-medical-center-data-breach/)

### [2026-10-24] 【国内】共同通信の集計: 今年の CVE は 10 月 21 日までに 8 万 5,000 件で、前年同期の 2.2 倍。生成 AI の高性能化で脆弱性の発見が急増
- **何が起きたか**: 共同通信が MITRE の CVE データ (10/21 まで) を独自に集計した。今年見つかった脆弱性は、過去最多だった前年同期の 2.2 倍の 8 万 5,000 件に達した。PHP でも「極めて深刻」とされたものを含む 27 件が見つかっているという。記事は、人手ではパッチの適用が追いつかない量になっていると指摘している。
- **なぜ重要か**: AI による脆弱性の大量発見が、一般紙でも取り上げられるようになった。CVE を追う側にとっては、件数の増加を前提に、優先度の付け方 (KEV、EPSS、到達可能性) を見直す根拠になる。
- 出典: [南日本新聞 (共同通信配信)](https://373news.com/news/national/detail/2026102401001081)

### [2026-10-24] Cognition、PHP2Shell・Node.js・GitLab の緊急修正を自動で当てるエージェント用スキル「Devin Vulnerability Fixes」を MIT ライセンスで公開
- **何が起きたか**: `fix-php-vuln` / `fix-node-vuln` / `fix-gitlab-vuln` の 3 つのスキルからなり、対象は PHP2Shell (CVE-2026-109618 / 109619)、Node.js の 10 月のセキュリティリリース (CVE-2026-111497 など)、GitLab の CVE-2026-110264 (CVSS 10.0)。読み取り専用での棚卸し、人の承認、パッチ適用、テストを経て、リポジトリごとに PR を 1 本作る流れ。Claude Code、Codex、Cursor、Gemini CLI など SKILL.md を読むエージェントで使える。修正の成功率などの数値は公表されておらず、マネージドランタイムやアプライアンス、Electron アプリは「指摘するだけで修正はしない」。
- **なぜ重要か**: 緊急パッチの適用をエージェントに任せる流れが具体的になってきた。その一方で、外部から取り込むスキル自体がサプライチェーンの攻撃面になる (先週の OpenAI 公式スキルの未登録ドメインの件と同じ構図)。導入前に、内容とどこを書き換える権限を持つかを確認する必要がある。
- 出典: [MarkTechPost](https://www.marktechpost.com/2026/10/24/cognition-devin-vulnerability-fixes-plugin-php2shell-nodejs-gitlab/)

## セキュリティニュース

### [2026-10-25] Tailscale SSH の未修正の欠陥「Tailworm」。侵害した 1 台から、ACL で SSH を許された他サーバーの root を取れる (Cyberdione Labs)
- **何が起きたか**: Cyberdione Labs の Erica Windisch 氏が、Tailscale 1.104.2 と headscale 0.29.5 を検証したレポート「Tailworm」(11 件の指摘) を 10/25 に公開した。Tailscale SSH でポートフォワーディングが許されていると、通常の SSH セッションから root 権限の tailscaled に root 専用のソケットへ接続させて root を取れる。root 所有ソケットの差し替えや、パス検査の TOCTOU 競合も示された。Tailnet Lock が無効な環境では、デバイス登録キーを奪って攻撃者の端末を信頼済みノードとして参加させるところまで成立した。CVE・修正版・セキュリティ速報はまだない。Tailscale の VP of Engineering は Reddit で報告の受領と修正作業中であることを認めた。headscale 0.29.5 ではフォワーディングを無効にできない。
- **悪用/PoC**: 実環境での悪用は報告されていない。PoC は非公開 (Tailscale のセキュリティチームにのみ提供)。第三者による再現はまだなく、「wormable」という表現には異論もある。
- **なぜ重要か**: 社内診断では「Tailscale SSH の ACL で SSH を許可 = 接続先の root」とみなして横展開の経路を洗い出すべき、という評価になる。修正が出るまでは、ACL を送信元と宛先の 1 対 1 で書くこと、フォワーディングの無効化、Tailnet Lock の有効化が緩和策になる。アプリコネクタ (conn25) からクラウドのメタデータサービスへ届く指摘もある。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/unpatched-tailscale-ssh-flaws-could-let.html)

### [2026-10-25] [続報] PHP2Shell: 欧州の政府機関で侵害が成立。AI エージェントとみられる攻撃者が 2 時間で MFA シークレットを奪い、NTLM リレーで Domain Admin を狙った (Unit 42)。北朝鮮系とみられる低速スキャンも (CYFIRMA)
- **前回から何が変わったか**: 10/23 時点では「侵害の成立は未確認」だった。Unit 42 によると、欧州の政府機関で CVE-2026-109618 / 109619 の悪用から 2 時間以内に、認証 DB のパスワードハッシュと 2FA シークレットが奪われた。攻撃者は AD への NTLM リレーのトンネルを張り、Domain Admin への昇格を試みた。コマンドの出力が `==SHELLUSER==` などの区切りで囲まれていたことから、Unit 42 はエージェント型 AI による操作と評価している。CYFIRMA は、侵害した 21 ノードから 216 ホスト (日本を含む) を低速でスキャンする活動を確認し、Lazarus 系の韓国語話者によるものと中程度の確度で評価した。Defused は 10/25、GlobalProtect のハニーポットへの PHP2Shell プローブを報告している。
- **悪用/PoC**: 悪用を確認 (侵害が成立)。公開 PoC あり。
- **なぜ重要か**: 「試行は多いが成立は少ない」という見方が崩れた。侵入後に AD へ進む手口 (匿名 LDAP、NTLM リレー) まで具体的に示されたので、PHP サーバーの棚卸しと、その先の AD の経路の点検を同時に進める必要がある。日本も対象国に挙がっている。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/php2shell-exploitation-hits-government.html) / [Unit 42 Threat Brief](https://unit42.paloaltonetworks.com/cve-2026-109618-cve-2026-109619/)

### [2026-10-25] 「Gheist」: 盗んだ GitHub トークンで全リポジトリに secrets を吐く workflow を仕込む。850 超のアカウント、1 万 3,500 超のブランチ (Wiz) (→ 今日の深掘り)
- **何が起きたか**: Wiz が 9/15 から追跡している、GitHub トークンを大規模に悪用するキャンペーン。`ci-sync-xxxxxx` ブランチに `sync-check.yml` を置き、secrets を base32 でログに出させて回収したあと run を削除する。詳細は深掘りを参照。
- **悪用/PoC**: 悪用を確認 (攻撃は継続中。プライベートリポジトリと GHES では成立している)。
- **なぜ重要か**: `permissions: {}` でもログのマスクでも secrets を守れないことが実例で示された。CI/CD 診断の確認項目に直結する。
- 出典: [Wiz Blog](https://www.wiz.io/blog/gheist-attempted-scaled-abuse-of-stolen-github-tokens-stumbles)

### [2026-10-24〜25] [続報] PHP2Shell は PAN-OS / Panorama の管理画面にも影響。10/24 に最初のホットフィックス 3 本を公開 (Palo Alto Networks)
- **前回から何が変わったか**: Palo Alto Networks のアドバイザリ (CVE-2026-109618、自社製品での評価は CVSS 8.7) が 10/23〜25 に更新された。PAN-OS 10.2 / 11.1 / 11.2 / 12.1 / 12.2 (PA / VM シリーズ) と Panorama が影響を受け、特別な設定は要らない。攻撃面は管理 Web UI と XML API で、データプレーンのインターフェースは管理プロファイルを付けている場合に限られる。GlobalProtect のポータル / ゲートウェイ、Clientless VPN、Captive Portal は影響を受けない。10/25 の更新で 10.2.18-h13、11.1.16-h4、11.2.10-h16 が 10/24 にリリース済みとされた。12.2.4-h1 などは 10/28〜30 の予定。Cortex XCORE (SaaS) と WildFire Cloud は 10/21〜22 に修正済み。
- **悪用/PoC**: Palo Alto は自社製品への悪用は把握していないとしている。PHP2Shell 自体の PoC は公開済みで、悪用も確認されている (上の項目)。
- **なぜ重要か**: 「PHP を使っているアプライアンス」も影響範囲に入ることが具体的に示された。外部診断で管理画面がインターネットに出ている PAN-OS を見つけたら、最優先で報告すべき指摘になる。Threat ID で防ぐには、MGT のトラフィックを DP 経由にして復号する必要があり、現実には ACL で絞ることが主な対策になる。他のアプライアンスベンダーの影響表明も追うべき。
- 出典: [Palo Alto Networks Security Advisory](https://security.paloaltonetworks.com/CVE-2026-109618) / [Cyber Security News](https://cybersecuritynews.com/palo-alto-confirms-php-rce-vulnerabilities/)

### [2026-10-24] AWS MCP Server の `aws___run_script` の Python サンドボックスを match/case の属性読み取りで脱出し、Lambda 内でコマンドを実行 (xplo1t)
- **何が起きたか**: 研究者 xplo1t 氏は、AWS MCP Server (5/6 に GA) のツール `aws___run_script` が Lambda で動かす Python サンドボックスの脱出手順を公開した。この環境は AST 検査と組み込み関数のプロキシ化で守られている。Python 3.10 の構造的パターンマッチ (`case Cls(attr=...)`) は `getattr` や `.` を使わずに属性を読めるため、AST 検査をすり抜けられた。さらにプロキシ実装の不備を組み合わせて、Lambda ユーザーとしてのコマンド実行と、実行ロールの資格情報の取得に至った。資格情報は AWS 所有アカウントのロールで、`sts:GetCallerIdentity` 以外はすべて拒否された。他のセッションや顧客データへのアクセスはなかった。7/26 に HackerOne で報告し、10/23 に解決済み、10/24 に公開された。
- **悪用/PoC**: 研究目的の実証のみ (修正済み)。手法は記事で詳しく説明されている。
- **なぜ重要か**: 「AST のブロックリストと組み込み関数の差し替え」で作った Python サンドボックスは、LLM エージェントのコード実行ツールに広く使われている。match/case による属性アクセスはそのまま他製品の診断に使える手法である。
- 出典: [xplo1t's site](https://xplo1t-sec.github.io/posts/breaking-the-aws-mcp-python-sandbox/)

### [2026-10-24] 攻撃者が使う LLM ペンテスト・ハーネス 3 種 (Artex / Cairn / Strix) の中身を分析 (Utku Sen)
- **何が起きたか**: 研究者の Utku Sen 氏は、最近の侵害報道で名前が挙がったオープンソースの動的ペンテスト用ハーネス 3 種を解析した。中国製の Artex と Cairn、米国製の Strix である。Artex は既存のエージェント基盤を使わず、独自のエージェントライブラリで planner / worker 構成を実装している (同氏はテレメトリ回避が狙いではないかとみる)。脆弱性の定義や認証の手順は持たず、判断をモデルに任せている。Cairn は「Origin / Goal / Hints」を入力に単一の目標 (CTF やデータの取得) を達成する設計で、網羅的な診断のツールではない。同氏は、検閲を外した DeepSeek などのモデルは対象の所有確認をしないため、これらのハーネスと組み合わせると無差別な動的攻撃が実用的になったと指摘している。
- **悪用/PoC**: ハーネス自体は公開済み。Artex は Microsoft (Storm-0940) や CrowdStrike の報告で実際の攻撃への使用が報じられている (既報)。
- **なぜ重要か**: 攻撃側の AI ツールの作り (planner が intent を作り worker が実行する、認証はモデル任せ) が分かると、WAF やログの検知設計にも、自社で AI 診断を導入するときの比較にも使える。
- 出典: [Utku Sen's Substack](https://utkusen.substack.com/p/how-llm-based-penetration-testing)

### [2026-10-24] 「SPECTER」: USB の電源管理操作でエアギャップ PC からデータを漏らす隠れチャネル (高麗大学)
- **何が起きたか**: 高麗大学の Choi 氏らは、root / 管理者権限を持つマルウェアが USB の電源管理やデバイス状態の操作 (データ転送は使わない) で情報を符号化する手法 SPECTER を発表した。Windows 10 と Ubuntu 22.04 で検証している。受信側は、充電中のスマートフォンの充電状態 (Galaxy S22 / iPhone 13 Pro、0.2〜0.25 bps)、マウスの LED や応答の停止 (1 bps)、ケーブルからの放射を HackRF で受ける方法などである。
- **悪用/PoC**: 学術的な実証のみで、実環境での悪用は報告されていない。
- **なぜ重要か**: 速度は極めて低く、実務での脅威は限定的。ただし、エアギャップ環境の評価で「USB の電源制御」も漏えい経路として扱うべきだという根拠になる。
- 出典: [Hackread](https://hackread.com/specter-usb-power-signals-air-gapped-pcs-leak-data/) / [arXiv 2610.28401](https://arxiv.org/html/2610.28401v1)

### [2026-10-25] YARA-X 1.22.0 リリース。改善 11 件・修正 9 件、64 ビット整数を読む組み込み関数を追加 (SANS ISC)
- **何が起きたか**: VirusTotal の YARA-X 1.22.0 が公開された。int64 / int64be / uint64 / uint64be の読み取り関数が加わった。SANS ISC の Didier Stevens 氏が紹介している。
- **悪用/PoC**: 該当なし (ツールの更新)。
- **なぜ重要か**: 64 ビットのヘッダやオフセットを持つ形式 (PE32+ の一部フィールドや独自コンテナ) に対するルールを素直に書ける。YARA から YARA-X への移行を進めている組織向けの情報。
- 出典: [SANS ISC Diary 33454](https://isc.sans.edu/diary/33454)

### [2026-10-24〜25] Electrum 4.8.3: 悪性サーバーが未承認トランザクションを偽の送金先に差し替え、利用者が RBF で手数料を上げると攻撃者宛ての取引に署名させられていた。実際の盗難あり
- **何が起きたか**: ビットコインウォレット Electrum は 10/24 に 4.8.3 を公開し、アドバイザリ (GHSA-6jp4-8v48-cc5v) を出した。4.8.3 より前の全版が影響を受ける。Electrum は承認済みの取引を SPV で検証する一方、未承認の取引は接続先サーバーの言うとおりに表示していた。悪性サーバーは正規の送金をブロードキャストせずに止め、宛先を差し替えた (署名が無効な) 取引を履歴に表示させた。利用者が RBF で手数料を上げると、攻撃者宛ての有効な取引に署名してしまう。偽のアドレスは、正しい宛先の末尾 4 文字が一致するように作られていた。10/11 と 10/18 に被害の報告があり、少なくとも 1 件で資金が盗まれた。修正版は未承認取引の署名を検証する。
- **悪用/PoC**: 悪用を確認 (被害 2 件、うち 1 件で資金が流出)。
- **なぜ重要か**: 「サーバーを信頼する範囲 (SPV で検証していない部分)」をクライアントの UI に流し込み、ユーザー自身に署名させる設計上の欠陥である。ウォレットや軽量クライアントの診断で、未検証のデータを表示や再署名のフローに使っていないかを確かめる典型例になる。
- 出典: [crypto.news](https://crypto.news/electrum-wallet-bitcoin-theft-security-flaw-4-8-3/) / [Electrum GHSA-6jp4-8v48-cc5v](https://github.com/spesmilo/electrum/security/advisories/GHSA-6jp4-8v48-cc5v) (GHSA 本体はこちらの環境から取得できず、内容は crypto.news の記事による)

### [2026-10-24〜26] CISA KEV: この期間の追加はなし
- **何が起きたか**: KEV カタログ (cisagov/kev-data と cisa.gov のフィード。dateReleased=2026-10-23T19:30Z、1,756 件) を確認した。dateAdded が 10/24〜26 のエントリーはなかった。最新の追加は 10/23 の Arista VeloCloud Orchestrator (CVE-2026-114625) と Collabora CODE (CVE-2026-110447) で、どちらも既報。対応期限は 10/26 (日本時間の今日)。
- **なぜ重要か**: 新しい追加はないが、既報の 2 件はきょう期限を迎える。PHP2Shell (CVE-2026-109618 / 109619) は悪用が確認されているものの、まだ KEV に入っていない点も押さえておきたい。
- 出典: [cisagov/kev-data](https://raw.githubusercontent.com/cisagov/kev-data/main/known_exploited_vulnerabilities.json) / [CISA KEV フィード](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json)

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-10-24 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-115823 | Starman (Perl PSGI サーバ) < 0.4019 | CWE-444 / CVSS 未付与 | HEAD リクエスト (および 1xx/204/304 応答) でも app が返したボディを書き出す → keep-alive/pipelining 接続上でクライアントやリバプロが余剰バイトを次レスポンスとして読む → レスポンスキュー desync (他ユーザへの応答混入) | [diff](https://github.com/miyagawa/Starman/commit/91c47c529cd1e100f938486896ea9083ec3ec7bf) | 水平伝播 (RFC 9110 の「HEAD/204/304 はボディ無し」規則は自前 HTTP サーバ実装で漏れがち)。同日 Starman で CWE-770/1333 (CVE-2026-115817/115822/115824) も公開 |
| CVE-2026-115825 / CVE-2026-114629 | Plack HTTP::Server::PSGI < 1.0056 / Web::Simple < 0.035 (Perl) | CWE-789 / CVSS 未付与 | 攻撃者申告の Content-Length をそのまま sysread()/read() の長さに渡す → Perl が読む前にバッファを要求長まで確保 → 1 リクエストで OOM、シングルプロセスのためサーバ停止 (未認証) | [diff](https://github.com/plack/Plack/commit/11545871cadc5df1b744cebb429cfeb4ebc1069a) / [diff](https://github.com/p5sagit/Web-Simple/commit/7e02c4f6204a2898938d357e6efe6dc2679af695) | 水平伝播 (Perl 系 PSGI 実装を同一報告者が横断的に洗い出し中 — oss-security 2026/10/24)。EPSS 0.0027 (114629) |
| CVE-2026-116013 | OpenResty lua-resty-dns < 0.24 | CWE-130 / CVSS 4.0 6.3 (3.1 3.7) | 権威/偽装 DNS 応答の RR ヘッダ・RDATA 長を受信メッセージ長と照合せず parse_section()/_decode_name() で読み進める → 未捕捉 Lua 例外 → resolver:query() 中断・名前解決不能 (DoS) | [diff](https://github.com/openresty/lua-resty-dns/commit/b68eaecbf7997ac71c08ba56032b1f45438bd758) | 水平伝播 (スクリプト言語製の自前 DNS パーサ全般: 長さフィールド信頼)。EPSS 0.0029 |
| CVE-2026-116011 (GHSA-7x84-xhp8-6cqj) | CrowCpp Crow (C++ Web FW) < 1.3.4 | CWE-674 / CVSS 4.0 8.7 (3.1 7.5) | 未認証で深くネストした JSON ボディ → crow::json::load() の再帰降下パーサに深さ上限なし → ワーカースレッドのスタック枯渇でプロセスごとクラッシュ | [diff](https://github.com/CrowCpp/Crow/commit/6956b7ca93c5df22f5aaccd670e5aa000c0d882b) | EPSS 0.0068 (pct 0.52)。水平伝播 (組込み JSON パーサを持つ C/C++ 軽量 FW) |
| CVE-2026-116137 | adm-zip (npm) ≤ 0.6.1 | CWE-436 / CVSS 4.0 6.3 (3.1 3.7) | `./hello.txt` と `hello.txt` のような正規化後同一のエントリ名 → readEntries() の重複チェックは生文字列比較で素通り → getEntry()/readAsText() で検査した無害内容と extractAllTo() が書き込む内容が食い違う (検査回避・差し替え) | [issue](https://github.com/cthackers/adm-zip/issues/587) (commit 不明、0.6.1 まで未修正の記載) | 水平伝播 (ZIP パーサ差分 / 「検査対象と展開対象の不一致」型。他言語の zip ライブラリ・アップロード検査ロジックでも再現しやすい) |
| CVE-2026-116066 | Firecrawl < 2.11.586 (Playwright service) | CWE-918 / CVSS 4.0 7.0 (3.1 6.8) | isInternalHost() で名前解決して検査 → 接続時に再解決 (TOCTOU) → DNS rebinding で私設 IP / クラウドメタデータへ到達 (scrape API 経由) | [diff](https://github.com/firecrawl/firecrawl/commit/5e74ff37b41ac650d6bccff170a9be0a6decb946) | 水平伝播 (LLM 向けスクレイパ/ブラウザ自動化系の SSRF ガードは「検査時と接続時の解決分離」が典型) |
| CVE-2026-116189 (GHSA-w33h-3qgq-8mv8) | rclone 1.55.0〜<1.75.2 (selfupdate) | CWE-347 / CVSS 4.0 7.7 (3.1 7.5) | PGP clearsigned SHA256SUMS の署名検証後、署名ブロック外 (前置された未署名バイト) の checksum 行もパース対象 → 偽の checksum 行を前置 → 攻撃者バイナリを正規としてインストール | [advisory](https://github.com/rclone/rclone/security/advisories/GHSA-w33h-3qgq-8mv8) (commit 不明) | 水平伝播 (「署名検証した範囲」と「使用するデータ範囲」の不一致。Go/CLI の self-update 実装全般で要確認) |
| CVE-2026-116191 / CVE-2026-116193 (GHSA-44pm-2q5p-fm63 / GHSA-gj73-fh6v-92fj) | rclone serve webdav < 1.75.2 | CWE-22 8.7 / CWE-200 6.9 (CVSS 4.0) | ① 未認証で `MKCOL /..` → '..' を未検証のまま VFS ノード化 → PUT/MOVE/COPY で served root 外 (他テナント) のファイル作成・上書き・削除 ② OPTIONS メソッドだけ認証ミドルウェアを素通り → Allow ヘッダ差分でパス存在を列挙 | [advisory](https://github.com/rclone/rclone/security/advisories/GHSA-44pm-2q5p-fm63) / [advisory](https://github.com/rclone/rclone/security/advisories/GHSA-gj73-fh6v-92fj) (commit 不明) | 水平伝播 (WebDAV サーバ実装の MKCOL/OPTIONS 特例処理。Go x/net/webdav 利用製品で同型を探す価値あり) |
| CVE-2026-116190 / CVE-2026-116196 (GHSA-3rqf-7h69-gg5v / GHSA-gpw7-77cq-9f72) | rclone WebDAV backend 1.56.0〜 / b2 backend < 1.75.2 | CWE-200 6.3 / CWE-319 6.0 (CVSS 4.0) | 認証ヘッダ (X-Auth-Token, B2 Authorization, SSE-C 鍵) を付与したリクエストが 3xx を受ける → カスタム CheckRedirect で別ホスト/HTTPS→HTTP ダウングレード先にもヘッダを再送 → 資格情報・暗号鍵の漏えい | [advisory](https://github.com/rclone/rclone/security/advisories/GHSA-3rqf-7h69-gg5v) / [advisory](https://github.com/rclone/rclone/security/advisories/GHSA-gpw7-77cq-9f72) (commit 不明) | 水平伝播 (Go net/http は標準ヘッダしか剥がさない。カスタムヘッダ認証の SDK/クライアントで頻出) |
| CVE-2026-116171 (GHSA-6gmc-424x-xgpm) | SiYuan 3.5.4〜<3.8.7 (Windows) | CWE-22 / CVSS 4.0 8.7 (3.1 7.5) | localPath に Windows 拡張長プレフィックス `\\?\` を付与 → filepath.Clean 後も残りプレフィックス型 denylist (IsSensitivePath) に一致しない → /api/import/importStdMd で API トークン・TLS 秘密鍵を未認証公開 assets にコピー | [advisory](https://github.com/siyuan-note/siyuan/security/advisories/GHSA-6gmc-424x-xgpm) (commit 不明) | 水平伝播 (Go の文字列プレフィックス比較による path denylist 全般。`\\?\`・`\\.\`・UNC での回避を他製品でも試す価値) |
| CVE-2026-116200 / CVE-2026-116201 (GHSA-wx48-r3qh-jvh5 / GHSA-w49g-f2jc-qxhg) | Snipe-IT < 8.6.3 / < 8.5.0 | CWE-319 8.2 / CWE-294 8.7 (CVSS 4.0) | ① ldap_start_tls() の戻り値を無視 → MITM が StartTLS にプロトコルエラーを返す → 平文 LDAP bind でサービスアカウント・利用者パスワード取得 ② SAML ACS の nonce (assertion ID) 使用済みチェックが非アトミック → 同一 assertion を並列 POST → 複数セッション発行 (リプレイ) | [advisory](https://github.com/grokability/snipe-it/security/advisories/GHSA-wx48-r3qh-jvh5) / [advisory](https://github.com/grokability/snipe-it/security/advisories/GHSA-w49g-f2jc-qxhg) (commit 不明) | 水平伝播 (PHP の ldap_start_tls 戻り値無視は Laravel/PHP 系 LDAP 連携で grep 一発で探せる。SAML replay の race も同型多数) |
| CVE-2026-116163 (GHSA-rq3w-5c6f-p7wr) | Parse Server < 8.6.102 / 9.0.0〜<9.10.5-alpha.2 | CWE-287 / CVSS 4.0 9.1 (3.1 7.4) | AuthAdapter を継承したカスタムアダプタの validateSetUp/validateLogin/validateUpdate が呼ばれず、任意の authData を受理する継承デフォルト実装が使われる → 任意 authData で既存ユーザとしてログイン・ID リンク・追加認証要素スキップ | [advisory](https://github.com/parse-community/parse-server/security/advisories/GHSA-rq3w-5c6f-p7wr) (commit 不明) | CVSS 9.1。水平伝播 (「基底クラスの fail-open デフォルト」型。同時に Parse Server で 4 件追加公開: CVE-2026-116161/116162/116164/116165) |
| CVE-2026-116176 (GHSA-vfp2-c8pq-v6h6) | vLLM 0.9.2〜<0.24.0 (P2pNcclConnector) | CWE-918 / CVSS 4.0 8.8 (3.1 8.2) | API 呼び出し側が X-Request-Id ヘッダに decode アドレスを埋め込む → prefill ワーカーがその値をパースして ZMQ connect → 攻撃者ホストへ NCCL unique_id・KV-cache テンソル漏えい / ワーカー停止 | [advisory](https://github.com/vllm-project/vllm/security/advisories/GHSA-vfp2-c8pq-v6h6) (commit 不明) | 水平伝播 (分散推論 (disaggregated prefill/decode) で制御情報をリクエスト ID 等のユーザ入力に相乗りさせる設計。SGLang 等の類似実装を確認する価値)。同日 vLLM 計 10 件公開 (CVE-2026-116172〜116181) |

注: KEV 該当なし (CISA KEV dateReleased=2026-10-23T19:30Z 時点。10/23 追加は CVE-2026-114625 VeloCloud Orchestrator / CVE-2026-110447 Collabora Online で、いずれも今回の窓外または既出扱い)。EPSS は 2026-10-25 時点で 116013/116011/114629 のみスコア付与、他は未収録。表中の採用 CVE はいずれも ex_ids.txt と非重複を確認済み。GitHub advisory ページ/API は 403 のため、fix commit は NVD の references に載っていたものだけ記載。

### 公開日の確認
- CVE-2026-115823 (Starman) → 2026-10-25T17:17Z (NVD published)
- CVE-2026-115825 (Plack) → 2026-10-25T17:17Z (NVD published)
- CVE-2026-114629 (Web::Simple) → 2026-10-24T14:16Z (NVD published。oss-security 2026/10/24/4 に投稿)
- CVE-2026-116013 (lua-resty-dns) → 2026-10-24T12:16Z (NVD published)
- CVE-2026-116011 (Crow) → 2026-10-24T12:16Z (NVD published)
- CVE-2026-116137 (adm-zip) → 2026-10-25T12:16Z (NVD published)
- CVE-2026-116066 (Firecrawl) → 2026-10-25T12:16Z (NVD published)
- CVE-2026-116189 / 116190 / 116191 / 116193 / 116196 (rclone) → 2026-10-25T14:16〜14:17Z (NVD published)
- CVE-2026-116171 (SiYuan) → 2026-10-25T14:16Z (NVD published)
- CVE-2026-116200 / 116201 (Snipe-IT) → 2026-10-25T14:17Z (NVD published)
- CVE-2026-116163 (Parse Server) → 2026-10-25T14:16Z (NVD published)
- CVE-2026-116176 (vLLM) → 2026-10-25T14:16Z (NVD published)
- (GHSA の published は GitHub 側 403 で未確認。いずれも CNA=VulnCheck による NVD 登録日で判定)

### 今日の CVE 所感
- 窓内の NVD 新規は 201 件 (うち WordPress プラグイン系が約半数)。OSV 側 (npm/PyPI/Go/Maven/crates.io/RubyGems/Packagist) では窓内に新規公開された非マルウェア advisory はなく、10/25 に VulnCheck CNA が rclone (10 件)・vLLM (10 件)・ImageMagick (20 件)・SiYuan・Snipe-IT・YesWiki・Parse Server の GHSA をまとめて CVE 化したのが主な供給源。
- 共通するバグクラスは「検査対象と実際に使われる対象のズレ」: 署名した範囲外の checksum 行 (rclone selfupdate)、正規化前の名前で重複検査 (adm-zip)、Clean 後も残る `\\?\` (SiYuan)、検査時と接続時の DNS 解決 (Firecrawl)。どれも別実装に横展開して探しやすいパターン。
- HTTP 層で水平伝播の候補になるもの: Perl PSGI 実装 (Starman/Plack/Web::Simple) の Content-Length 先行確保と HEAD ボディ送信による desync。Ruby (Puma 以外のマイナー Rack サーバ) や Python の自前 WSGI/ASGI サーバでも同じ RFC 9110 準拠漏れがないか見る価値がある。リダイレクト時のカスタム認証ヘッダ転送 (rclone WebDAV/B2) は Go 製 SDK 全般で grep しやすい。
- 優先するなら Parse Server CVE-2026-116163 (CVSS 4.0 9.1、認証バイパス)、rclone serve webdav CVE-2026-116191 (未認証で root 外に書き込み)、Snipe-IT の StartTLS 戻り値無視 (PHP の `ldap_start_tls(` を呼び出し側で検査していない箇所を横断 grep)。KEV 該当も高 EPSS もなく、PoC は VulnCheck/GHSA の記述レベルにとどまる。

## 日本国内のセキュリティ動向

### 国内インシデント・事故

#### [2026-10-24] システムファイブ (映像・音響機材 EC) のオンラインショップ連携システムに不正アクセス、最大約 15,000 名の顧客情報を不正取得された可能性。ログインをメール OTP 方式に切り替えて再開
- **何が起きたか**: 株式会社システムファイブは 10/24、オンラインショップ (system5.jp) と連携する一部システムへの不正アクセスにより、会員のうち最大約 15,000 名分の個人情報が第三者に不正取得された可能性があると公表した。クレジットカード情報とパスワードは自社で保有していないため流出のおそれはなく、「社内ネットワークやショッピングカートシステム自体の脆弱性に起因する不正アクセスは確認されていない」としている。
  - 10/24 19 時頃にオンラインショップを再開。ログイン方式を「登録メールアドレスに届く 6 桁の認証コード」に変更した (同社は「パスワード流出によるものではない」と説明)。
  - ポイントサービス、商品レビュー、オンライン帳票発行は停止したまま、再開時期は未定。個人情報保護委員会へ報告済み、所轄警察署に相談済み。
- **なぜ重要か**: カート本体ではなく「連携システム」(ポイント・レビュー・帳票など周辺機能) が入口になったとみられる事例で、EC 診断で本体だけを範囲にすると漏れる典型である。再開時にパスワード認証そのものをやめてメール OTP に寄せた判断も、相次ぐ漏えいを受けた国内 EC の対処パターンとして参考になる。
- 出典: [システムファイブ](https://info.system5.jp/whatsnew/apology-20261024)

#### [2026-10-24〜25] ピッコマ (カカオピッコマ) のメルマガ宛先 1,002,404 件のメールアドレスが流出。ブラストメール (ラクスライトクラウド) への不正アクセスの波及で、公表された二次被害では確認できた範囲で最大
- **何が起きたか**: カカオピッコマは、メルマガ配信に使っていた「ブラストメール」が不正アクセスを受け、ピッコマのメルマガ 1 回分の配信先メールアドレス **1,002,404 件** が外部に流出したと公表した (第 1 報)。10/24 にラクスライトクラウドからの報告で判明した。NHK は 10/25 17:49 に報道している。
  - 流出はメールアドレスのみで、顧客の管理番号や最終課金日などは含まれていない。パスワードはブラストメールに預けておらず、氏名・カード情報は同社が保有していない。ピッコマのアプリ・Web とアカウントへの影響はないとしている。「ピッコマノベルズ」のメルマガは流出を確認していない。件数は配信先の延べ件数で、実人数ではない。
  - 対応: メルマガ配信を停止し、**ブラストメールから送られるメールがピッコマの正規メールとして扱われないよう設定を変更** (なりすまし対策)。個人情報保護委員会へ報告済み。
- **なぜ重要か**: ブラストメール事件の影響は契約者 344 件 (10/25 10:00 の更新でも変化なし) にとどまらず、配信先リストを通じて最終的な被害者数が大きく膨らむことを示した。流出したアドレスは「ピッコマを名乗るフィッシング」の精度を上げるので、SaaS の配信基盤を外したあとに SPF/DKIM の許可を残していないか (旧配信元から自社ドメインで送れてしまう状態) を点検する価値がある。
- 出典: [ピッコマ お知らせ (第1報)](https://piccoma.com/web/notice_detail/7503) / [NHK](https://news.web.nhk/newsweb/na/nd-20261025de65227) / [ビジネス+IT](https://www.sbbit.jp/article/cont1/187769)

#### [2026-10-25] ヤマダデンキ、不正アクセスを確認し「スマホゴールド会員」と動画配信「ヤマダビデオ」を 10/22 から停止。個人情報への影響は調査中
- **何が起きたか**: 日本経済新聞 (10/25 13:25) によると、ヤマダデンキは外部からの不正アクセスを確認し、月額 330 円の有料会員サービス「スマホゴールド会員」と、U-NEXT と連携する動画配信「ヤマダビデオ」を一時停止したと発表した。停止は 10/22 から続いており、個人情報への影響、原因、復旧見通しは調査中で今後公表するとしている。
- **なぜ重要か**: 本体の EC や会員基盤ではなく、外部サービスと連携した月額・動画系の周辺サービスが対象になっている点は、今月相次ぐ「周辺システム経由」の漏えい (システムファイブ、Studio、ブラストメールなど) と同じ構図である。件数・侵入経路が出ていないため、続報待ち。
- 出典: [日本経済新聞](https://www.nikkei.com/article/DGXZQOUC250U50V21C26A0000000/) (ヤマダデンキ公式サイトは取得時に接続が切断され、一次告知は未確認)

#### [2026-10-24〜25] [続報] GMO「お名前.com デスクトップクラウド」: 第 5 報で利用者自身の端末のフルスキャンとバックアップを要請。熊谷代表はブログで「社内技術者から課題を指摘されていたが、優先順位の中で間隙を突かれた」と認める
- **前回からの変化**: 前回は第 4 報 (金銭要求・一律 5,000 円・FX 損失補償・能動的サイバー防御の要請) まで掲載。
  - **第 5 報 (10/24 夜)**: 調査範囲を利用者の端末に広げ、「お客様ご自身の端末 (PC・スマートフォン等) のウイルス対策ソフトによるフルスキャン」と「データのバックアップ」を至急求めた (同社は「二次被害防止のための予防的な対応」と説明)。取引ツール (MT4/MT5 等) 利用者には、FX に使っていない別端末からのパスワード変更に加え、**パスワード変更後も証券会社・FX 会社のサーバー仕様によって既存セッションが残り第三者が取引を続けられる場合がある** として、事業者側での全セッション切断を依頼するよう求めた。サーバー内やブラウザに保存した認証情報の変更、攻撃者を名乗る者からの連絡に応じないことも追記。
  - **攻撃者側の要求公開 (10/24、日経 10/25 報道)**: 攻撃者を名乗る側は 10/24 に自らの Web サイトで GMO への要求内容を公開し、**10/27 正午までに身代金を支払わなければサービス利用者の PC を乗っ取り、PC 内の個人的な情報を拡散する** と予告した。第 5 報の端末スキャン要請は、この脅しと時期が重なる。GMO は第 4 報で支払い拒否の方針を示している。
  - **攻撃者の主張 (未検証)**: セキュリティ対策 Lab (10/25) が入手した犯行声明では要求額は **100 万米ドル**。攻撃者は、仮想サーバー群が **Active Directory で集中管理され、複数環境に共通する管理者権限で横展開できた**こと、利用者に配布された **RDP 接続設定でドライブリダイレクトが有効** だったこと、解約済み環境の残存などを「問題点」として挙げた。同 Lab が確認した「CLIENT PC DRIVE EXTRACTION」と題する 6 台分のログ (10/14 22:53〜23:16 に集中、計 3,566 行のコピー記録) には、RDP 越しに見える接続元 PC のドライブから文書やブラウザーの Login Data をコピーしたとする記録があった。ただし、ログの真正性と外部送信の完了は確認されていない。
  - **熊谷正寿会長兼社長のブログ (10/25 夜、読売報道)**: 同サービスのセキュリティについて社内の技術者から事前に「改善すべき課題」を指摘されていたが、「サービスの継続への影響や他の対処事項との優先順位を考慮しながら対応を進めた結果、攻撃者にその間隙をつかれてしまった」と説明。損失の全額補償、代替サービスの 6 か月無償提供、システム基盤の抜本的刷新、外部専門家を交えた原因究明を表明し、政府に能動的サイバー防御の適用を改めて求めた。
- **なぜ重要か**: 攻撃者の主張が正しければ、経路は「共有管理者権限による全テナントへの横展開」と「RDP ドライブリダイレクトを通じた接続元 PC の読み取り」という、ペンテストでよく指摘される設定不備の組み合わせである (RDP の `drivestoredirect` や GPO「ドライブのリダイレクトを許可しない」で防げる)。「VPS 基盤の侵害 → 利用者の端末にも波及しうる」と事業者自ら示した点と、「パスワードを変えても FX サーバー側のセッションが生きている」という指摘は、IR 対応で見落としやすい論点である。経営トップが既知の指摘を放置していたと公に認めたことは、診断・ペンテストの指摘事項の扱い (リスク受容の記録) をめぐる議論にもつながる。
- 出典: [GMO インターネットグループ (第5報)](https://group.gmo/info/alert/2026102402/) / [読売新聞 (Yahoo!ニュース)](https://news.yahoo.co.jp/articles/83c9b89271418e914d43ed2eb3debf9b3877ca62) / [日本経済新聞](https://www.nikkei.com/article/DGXZQOUC250PP0V21C26A0000000/) / [セキュリティ対策 Lab (犯行声明の分析)](https://rocket-boys.co.jp/security-measures-lab/gmo_onamae_hacker_statement_lab_sources_20261025/)
- 注: 10/27 正午の期限は本ダイジェスト配信の翌日。期限前後の GMO の第 6 報に注意。

#### [2026-10-24] 競輪・オートレース投票サービス「チャリロト」アプリに脆弱性を突いた不正アクセス、チャリカ会員 373 名の口座情報・投票履歴まで取得される
- **何が起きたか**: 株式会社チャリ・ロトは 10/24、投票サービス「チャリロト」のシステムが 10/21 9:30〜13:00 頃に「脆弱性を悪用した第三者による不正アクセス」を受け、チャリカ会員 **373 名** の情報が不正に取得されたと公表した。10/22 に点検で不審なログを発見してアプリを停止、10/23 に脆弱性を修正して再開、10/24 に影響範囲を特定して本人通知・公表した。
  - 取得された情報: 会員 ID、氏名、生年月日、住所、メール、電話番号、会員ランクなどに加え、**銀行名・支店・口座番号・名義**、カード名義・下 4 桁・有効期限・ブランド、払戻金残高・入出金履歴・精算履歴・購入可能額、**レース・券種・買い目・購入金額・的中・払戻金額** まで。ログインパスワード、カード番号全桁、セキュリティコードは漏えいしていないとしている。個人情報保護委員会へ速報済み。脆弱性の種類は非公表。
- **なぜ重要か**: 件数は少ないが、1 人あたりの項目が口座情報から投票の明細まで及んでおり、API の認可不備 (他人の会員データを参照できる IDOR など) を疑わせる取られ方である (同社は脆弱性の種類を公表していない)。公営競技の投票アプリは資金移動に直結するため、モバイル API の認可テストを優先すべき領域である。
- 出典: [チャリ・ロト](https://chariloto.jp/news/20261024/)

#### [2026-10-25] [続報] futureshop、CEO 名で 3 つの事象を整理。10/21 の不正アクセスは「関連サービスの脆弱性」経由で 4 台を緊急停止、現時点で漏えいは未確認。PHP2Shell 対応の長時間停止、10/19 判明の 1 店舗 314 万件漏えいとは別件と説明
- **前回からの変化**: 前回 (10/23) は 1 店舗 (リンツ&シュプルングリー・ジャパン) の会員 3,147,469 件の漏えいを掲載。10/25 の説明で、今週の事象を次の 3 件に分けた。
  1. **PHP2Shell 対策の長時間メンテナンス** (10/21 21:36〜10/22 23:35): futureshop 本体は PHP を使っていないが、「CMS サーバオプション」で店舗ごとに異なる複数の PHP バージョン (WordPress など) を提供していたため、個別対応に時間がかかり終了予定を何度も延長した。
  2. **10/21 10:14 頃に検知した不正アクセス**: 「futureshop の関連サービスの脆弱性を突いた」もので、影響しうる **4 台のサーバー** を 11:30 から緊急停止。脆弱性のあった関連サービスを停止し、10/22 23:35 に再開した。現時点のログ調査では個人情報の漏えいは確認されておらず、外部の調査機関に調査を依頼中。
  3. **10/19 判明・10/23 公表の 1 店舗の会員情報漏えい**: 自社サーバーで使っていたソフトウェアの脆弱性が原因で、1・2 とは別件。
  - なお 10/23 には「フォームメーラー FreePlus」「新フォームメーラー」の提供終了を「緊急・重要」として告知している (2 の「関連サービス」と同一かどうかは同社は明示していない)。
- **なぜ重要か**: 1 週間に「別々の脆弱性による 2 件の侵入」と「予防的な長時間停止」が重なった SaaS 事業者の例である。特に、本体が PHP を使っていなくても、オプションで顧客に PHP の実行環境を提供していれば PHP2Shell の影響を受けるという点は、SaaS の影響範囲を判定するときの盲点になりやすい。
- 出典: [futureshop (10/25 説明)](https://www.future-shop.jp/news/2026/10/25.html) / [futureshop (フォームメーラー提供終了, 10/23)](https://www.future-shop.jp/news/2026/10/23-2.html)

### 国内の注意喚起・ガイドライン・政策

> 10/24〜26 早朝は週末にあたり、JPCERT/CC・IPA・国家サイバー統括室・個人情報保護委員会・警察庁・総務省・経産省・金融庁の新着一覧に、この期間の日付が付いた新しい注意喚起やガイドラインは見つからなかった (10/26 05:00 JST 時点)。以下は報道ベースの政策動向である。

#### [2026-10-24〜25] [続報] GMO の能動的サイバー防御の要請に対する政府側の整理:「要請は法的根拠がない」「被害発生後では意義が乏しい」。熊谷代表は 10/25 に改めて適用を求める
- **前回からの変化**: 前回は「政府側は慎重」(朝日) まで掲載。10/24 夜の読売・日経が、制度上の要件と政府側の考え方を具体的に報じた。
  - 読売 (10/24 20:51): 政府関係者は「要請は法的根拠がなく、個別企業の求めに応じて発動を決める制度ではない」と強調した。無害化措置は、放置すれば重大な危害が生じるおそれがある場合や、外国政府が関与する組織的・計画的な攻撃が対象。本来は兆候の段階で未然に防ぐ措置で、別の政府関係者は「被害発生後では意義が乏しい」と述べた。要請が公表されたことで、実施すれば「手の内をさらすことになる」(政府高官) との懸念もある。実施には独立機関「サイバー通信情報監理委員会」の事前承認が原則必要 (緊急時は事後通知も可)、海外サーバーが対象なら外相との事前協議も必要。
  - 日経 (10/24 19:30): 企業が政府に申請する法的な仕組みはなく、政府は重大性・緊急性を踏まえて個別に判断する。政府高官は「防御のための支援はする。無害化につながるかは解析を進めなければいけない」と述べた。国家サイバー統括室 (NCO) が中心に情報を集め、基幹・重要インフラをはじめ国民生活や安全保障に影響しうるシステムへの攻撃を対象とするが、**対象業種は絞っていない** という。
  - 熊谷正寿代表は 10/25 夜のブログで「国民の資産とデータが脅威にさらされている」として、改めて適用を求めた (読売)。
- **なぜ重要か**: 「特定社会基盤事業者でない民間クラウドへの、すでに起きた被害」に無害化を使えるかという、施行 1 か月の制度の運用の境界を示す最初の事例である。政府は実施しても原則公表しない方針なので、適用されたかどうかは外から確認できない可能性が高い。
- 出典: [読売新聞](https://www.yomiuri.co.jp/politics/20261024-GYT1T00257/) / [日本経済新聞](https://www.nikkei.com/article/DGXZQOUA241IB0U6A021C2000000/) / [読売新聞 (Yahoo!ニュース, 熊谷代表のブログ)](https://news.yahoo.co.jp/articles/83c9b89271418e914d43ed2eb3debf9b3877ca62)

#### [2026-10-24] 出入国在留管理庁、2027 年度からデジタル・フォレンジックを捜査に導入へ。概算要求に 5,000 万円
- **何が起きたか**: 読売新聞によると、入管庁は来年度から、不法就労者から押収したスマートフォンや PC のデータ解析に、消去されたデータを復元するデジタル・フォレンジックを導入する。来年度予算の概算要求に関連経費 5,000 万円を計上した。現在は押収したスマホの画面をカメラで撮影して証拠を保存しており、SNS のやり取りの消去・書き換えが多いため、雇用主やブローカーの立件が難しかったという。警察はすでに電子鑑識を導入済み。
- **なぜ重要か**: 警察以外の行政機関にもフォレンジックの需要が広がっていることを示す。国内のフォレンジック事業者や、ツール・人材の調達 (委託か内製か) の動きにつながる可能性がある。
- 出典: [読売新聞](https://www.yomiuri.co.jp/politics/20261024-GYT1T00192/)

### 国内製品の脆弱性 (JVN)

> **10/24〜26 (05:00 JST 時点) に JVN で新しく公開された案件はない。** jvn.rdf と JVN トップページの最終更新日は 10/23 のままで、最新は 10/23 の 4 件 (プリザンター JVN#82312317、三菱電機 JVNVU#93251594、CISA ICS まとめ JVNVU#98747108、PHP JVNVU#99905564)。いずれも掲載済みである。
> **JVN iPedia / MyJVN は 10/26 早朝の時点でも停止中** (jvndb.jvn.jp は HTTP 503、「サービス再開時期は未定」)。停止は 10/22 から。対象は JVN iPedia 検索、MyJVN API、JVNDB RSS (データフィードすべて)、MyJVN バージョンチェッカ、mjcheck4。JVNDB の RSS や API を CVE 突合に使っている場合は、NVD / JVN (jvn.rdf) / ベンダー告知で代替する必要がある。
> 国内ベンダーの告知 (EC-CUBE、Movable Type、a-blog cms、baserCMS、ソリトン、サイボウズ、I-O DATA ほか) も確認したが、この期間の日付の新しい脆弱性情報は見つからなかった。週末のため、表の行は 0 件とする。

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| — | — | (10/24〜26 の新規公開なし) | — | — | [JVN](https://jvn.jp/) |

> 参考 (窓外のため不採用、編集判断用): トレンドマイクロ KA-0024807 (10/23 11:30 公開、同日 18:30 更新) で、PHP2Shell (CVE-2026-109618/-109619) が **Apex One / Apex Central (オンプレ) に「影響あり、CP 準備中」**、DDI・DDAN・DDEI・TMWS・Vision One NDR も「影響あり、対応策準備中」と案内されている。過去の掲載は KA-0024791 (調査状況) のみで、この製品別の一覧は未掲載。Critical Patch が出た時点で採り上げる価値がある。<https://success.trendmicro.com/ja-JP/solution/KA-0024807>

### 国内コミュニティ・研究・イベント

#### [2026-10-25] Jxck 氏「eMudhra のインシデントは Web にとって何を意味するのか」— PHP2Shell より深刻とし、Sectigo のクロスルート、Electron アプリや CLI が同梱する証明書ストアの問題、当面の VPN 利用を論じる
- **何が起きたか**: Jxck 氏が blog.jxck.io に解説を公開した。eMudhra の中間 CA 8 個の鍵 (P-384) が、キーセレモニーのスクリプトのバグで上位 47 バイトが 0 の「実質 1 バイトの鍵」(値は 4, 56, 66, 115, 155, 156, 230, 237) だったという事実を整理し、「CA の秘密鍵が漏洩したのと等価」と位置づけた。主な論点は次のとおり。
  - 問題の中間 CA は Sectigo のクロスルートで、証明書ストアは基本的に許可リストなので、eMudhra を外しても Sectigo 経由の信頼経路が残る。ブラウザは CRLSet / OneCRL で失効できるが、失効や CT の確認をしない CLI や言語実装には問題が残る。
  - Chromium と Node を同梱する **Electron アプリ (Slack、Discord、VS Code など) は再ビルドされないと証明書ストアが更新されない**。更新が止まったアプリは使わず Web 版に切り替えるべきとした。
  - 悪用には中間者の位置が必要なので、全社員を守るなら「全部更新しろ」と並行して「当面は VPN を必ず使え」という号令も対症療法としてありうる、と提案した。
  - Mozilla Bugzilla (bug 2083449) で eMudhra が「SNS での詮索で有意義な分析が事実上不可能」と返答したことを批判した。
- 関連: Zenn の yamato_snow 氏 (10/25) は、手元の Mac を点検したところ、Node.js や macOS を更新しても別の証明書ストアを使う道具は **発見者が公開している「偽証明書を返す試験用ホスト」に接続できてしまい**、ストアから 2 枚を外してようやく拒否するようになったと報告した。
- **なぜ重要か**: ブラウザ以外の TLS クライアント (Electron、curl、言語ランタイム、certifi など) を棚卸しして直す作業は、診断側でも「試験用ホストへ接続して確かめる」形で検証できる。10/24 までの本ダイジェストは各ランタイムの CVE を追ってきたが、どこが直らないまま残るかを整理した国内の記事として価値がある。
- 出典: [blog.jxck.io](https://blog.jxck.io/entries/2026-10-25/emudhra.html) / [Zenn (yamato_snow)](https://zenn.dev/yamato_snow/articles/october-2026-vuln-three-layer-check)

#### [2026-10-24] suzuki-shunsuke 氏「GitHub CLI が短命 token をサポートしても ghtkn が必要な理由」— 短命 access token でも、OS keyring の refresh token を盗まれれば無期限に再発行される
- **何が起きたか**: ghtkn (GitHub App からローカル開発用の User Access Token を発行する CLI) の作者が Zenn に公開した。GitHub CLI は 10/21 に、自動更新される短命 OAuth トークンを opt-in の Public Preview で導入した。これに対し著者は、access token は 8 時間で失効するが、**refresh token は 6 か月使われなければ失効、使うたびに新しいものが発行される**ので、漏れれば攻撃者は手元の外で access token を事実上無期限に発行し続けられると指摘した。gh は refresh token を OS keyring に保存するが、macOS Keychain は一度信頼したバイナリなら確認ダイアログなしで読めるため、サプライチェーン攻撃で任意コードが実行されると容易に漏れるという。
  - ghtkn の優位点として、refresh token を平文で保存しない、アクセスできる org / リポジトリを制限できる、用途別に権限の異なる App を使い分けられる、agent を lock できる、refresh token 漏洩の疑いを検知して警告する、を挙げた。英語版も hashnode に公開している。
- **なぜ重要か**: 今週の LiteLLM の改ざん配布 (当初は GitHub CLI の OAuth トークンの流出が原因とされ、10/24 に根本原因が訂正された) などを受けて、開発端末の GitHub 認証情報をどう持つかは国内でも実務の論点になっている。「短命化したから安全」とはならない理由 (refresh token の扱い) を具体的に示している。
- 出典: [Zenn (suzuki-shunsuke)](https://zenn.dev/shunsuke_suzuki/articles/ghtkn-advantage-over-gh-cli-expiring-token) / [英語版 (hashnode)](https://suzuki-shunsuke.hashnode.dev/github-cli-s-new-expiring-tokens-still-leave-your-refresh-token-exposed-to-malware)

> イベント: **CODE BLUE 2026** はトレーニングが 11/11〜15、カンファレンスが 11/17〜18。公式サイトによると参加の事前登録は 11/10 まで (最新のお知らせは 10/19 の「トレーニングの参加受付開始」で、この期間に新しい発表はない)。<https://codeblue.jp/>

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 70 (RSS/Atom、NVD API、OSV、EPSS、CISA KEV、各社ブログ・プレスリリース、WebSearch)
- 採用件数: AI技術=12 / AIセキュリティ=7 / セキュリティ=11 / CVE=13 行 (20 CVE) / 国内インシデント=6 / 国内政策=2 / JVN=0 / 国内コミュニティ=2
- 除外理由内訳: 古すぎ=約 25 / 重複=約 38 (直近 7 日の既出 URL・CVE・トピック) / 日付不明・裏取り不可=3
- 重複整理: AGENTS.md の件は「AI セキュリティ」に、PHP2Shell の Unit 42 続報は「セキュリティニュース」に寄せ、もう一方からは外した。Gheist は深掘りに詳細を書き、ニュース欄は要約だけにした。
- 前回の深掘り (Linux カーネル ZDI-CAN-33367) は、期間内に新しい事実 (CVE の採番、netdev へのマージ、ディストリの更新) を確認できなかったため、続報は立てていない。git.kernel.org / lore.kernel.org はボット対策で取得できず、マージの有無は直接は確認できていない。
- 窓が週末にあたったため: arXiv cs.CR の新着なし (最新の提出は 10/22)。watchTowr / PortSwigger / Talos / DFIR Report / SentinelLabs / Project Zero / ZDI / Trail of Bits / Mandiant / Microsoft Security Blog は期間内の記事なし。Security NEXT / ScanNetSecurity / piyolog の RSS は 10/23 で止まっていた。JPCERT/CC・IPA・国家サイバー統括室・PPC・警察庁などの新しい発表もなし。
- 確認が弱い項目:
  - GMO の攻撃者の主張 (AD の共有管理者権限、RDP のドライブリダイレクト): セキュリティ対策 Lab が入手した犯行声明によるもので、真正性は未検証。
  - ヤマダデンキ: 日経の報道のみで、公式の告知は未確認。
  - Electrum: GHSA 本体を取得できず、crypto.news の記事による。
  - Tailworm: 第三者による再現はまだない。
- 取得失敗ソース:
  - github.com の advisory ページ / GitHub API (403) → 修正 commit は NVD / OSV の references から取得し、取れないものは「(commit 不明)」と書いた
  - JVN iPedia / MyJVN / JVNDB RSS (HTTP 503、10/22 から停止中) → jvn.rdf と JVN トップページで代替
  - git.kernel.org / lore.kernel.org (Anubis)、Google Cloud / GTI の RSS (404)、Socket / Cybernews / Security Boulevard (Cloudflare)、Sophos News (HTTP/2 の切断)
  - VentureBeat (Vercel のチャレンジ)、MarkTechPost の本文 (Cloudflare → RSS の content:encoded で代用)、Anthropic の RSS (404 → News ページで代用)、ITmedia / ZDNet Japan / マイナビ の RSS (解析できず)
  - yamada-denki.jp (接続の切断)、ELECOM (403)、BUFFALO (404)、jp-secure.com (証明書の名前が不一致)、日経の有料部分

</details>
