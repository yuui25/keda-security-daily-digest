# KEDA Daily Digest — 2026-11-14 (JST)

> 採用範囲: 公開日 2026-11-12 〜 2026-11-14
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

セキュリティ側の最大の話題は、**Check Point のゲートウェイへの破壊的な攻撃** だ。PHP2Shell で Mobile Access のポータルに入り、修正のなかった root 昇格 **CVE-2026-123039** (DynamicCLI) で機器を乗っ取ったうえで、ESXi にワイパーを撒いた。Check Point は数十の顧客で悪用を確認し、CISA は 11/13 に KEV に加えた。期限は 11/16 と短い (今日の深掘り)。KEV には、既報の UnrealIRCd (CVE-2026-114713) も同じ日に入った。ほかに、北朝鮮の **FaceStealer** (偽のビデオ会議とディープフェイクで 4 億ドル超) への米国の摘発、通信事業者の中の機器から SMS の 2FA を横取りする **SilentAir**、独軍用ドローンのメーカー **Quantum Systems** の更新の経路の侵害が出た。Project Zero は、開示の期限を段階的に 30 日まで縮めると発表した。
AI 側では、OpenAI の **ChatGPT Wallet** (エージェントが決済まで行う) と Google の **Gemini × Google Wallet** が同じ日に出て、エージェントが金融のデータとお金に触れる段階に入った。AI セキュリティでは、OpenAI の **Daybreak Red Team / Defense Factory** (エージェントによるペンテストと修正)、Microsoft の **追加学習へのバックドア** の研究、Corelight の **「固定したはずの MCP サーバーの依存が起動のたびに変わる」** 問題が、診断業務に直接かかわる。
CVE では、**Payara の未認証の管理 RCE**、**FreeRADIUS の EAP**、**bacnet-stack の BACnet/SC**、**TightVNC のビューア (修正なし)**、**OpenBao の ACL の回避** など、「相手の申告した長さを信じる」型と「認可と解決の食い違い」型が並んだ。
国内では、**プレイドの「KARTE」が不正アクセスで全面停止** し、**マネックス証券** で eKYC の画像 1,592 件とメールアドレス最大 113 万件が漏えいのおそれとなった。ほかに **Qoo10**、**Yeny (133 万件)**、**甲賀市の防災放送のランサムウェア** と続く。アララ経由の波及もまだ続いている。Microsoft 365 の大規模障害は政府の GSS にも及んだ。
**今日まず見るべき 2 件**: (1) Check Point の Mobile Access を公開しているなら、11 月の Jumbo Hotfix を当て、10/30 以降の侵害の痕跡を調べる (深掘り参照)。(2) KARTE のタグを埋め込んだサイトを運用・診断しているなら、プレイドの続報を追い、Datahub の連携の認証情報の入れ替えと、停止の前後に配信された接客の確認を検討する。

## 今日の深掘り

### Check Point のゲートウェイが PHP2Shell で侵入され、未公表だった root 昇格 (CVE-2026-123039) で乗っ取られた。攻撃者はゲートウェイを足場に ESXi へ移り、ワイパーを実行した。CISA KEV の期限は 11/16

- **概要 (事実)**:
  - Check Point Research は 11/12、Gaia OS の DynamicCLI デーモン (`dynamic_server`) の権限昇格 **CVE-2026-123039** (CVSS 7.8、CWE-732 / 862) を緊急の hotfix で直したと公表した。この欠陥は、修正の前から実際の攻撃に使われていた。Check Point は「数十の顧客 (a couple of dozen customers)」で悪用を確認したとしている。CISA は 11/13 に KEV に加え、期限を 11/16 とした。
  - 影響する製品は、Security Gateway、Security Management / Log Server、Multi-Domain、Scalable Platforms の R81、R81.10、R81.20、R82、R82.10、R82.20。
  - 攻撃は 2 回あった。第 1 波は 10/30 で、イスラエルの組織が狙われた (一部でワイパーが動いた)。第 2 波は 11/2 で、国や業種を問わなかった。PHP の修正 (10/21) から約 1 週間後に始まっている。
- **技術的な中身**:
  - **入口**: Mobile Access のポータル (PHP で動く。`/opt/CPcvpn-R81.20/`) に、PHP の未認証の RCE「PHP2Shell」(CVE-2026-109618 / 109619) を使う。`session.upload_progress` を悪用するので、`/opt/CPcvpn-*/tmp/` に `upload_progress_pwn` の印を含むセッションファイルができ、Apache/PHP のワーカーが数百回 segfault する。
  - **root 化 (今回の 0-day)**: `dynamic_server` は root で動き、誰でも書き込める Unix ソケット `/tmp/dynamic_socket` で待ち受ける。接続元を確かめないので (SO_PEERCRED などを見ない)、Web のサービスアカウントが要求を 1 つ書くだけで、Clish のコマンドが root で実行される。最終の sink は `system()`。
  - **攻撃後の動き**:
    1. ログイン画面のテンプレートに PHP の Web シェル `zz*.tpl` を置く (鍵 `zz2026`。コマンドの実行、eval、アップロードに対応)。
    2. バックドア **TSGA** を `slot_CPconfigdaemon` として永続化する。TCP 11072 を全 IPv4 で待ち受け、設定の窃取、バックアップやスナップショットへの永続化、ファイアウォールのログの改ざんができる。
    3. **TSProxy** (`/lib/libcpfwcommon.so`) を機器のプロセスに注入し、印の付いた攻撃者の通信だけを中継する。
    4. gogo スキャナーで内部を探索し、`vpxuser` で ESXi に SSH して、ワイパー `destroy_v6` (0 で上書きしてから削除) を実行する。置き手紙 `DREAM_ANNEXATION.txt` (ヘブライ語) を残す。
  - **インフラ**: `130.94.19[.]204`、`130.94.19[.]168` (LightNode の VPS)。探索は 00:00〜09:00 UTC に集中した。
- **背景・経緯 (過去の事象の引用)**:
  - PHP2Shell (CVE-2026-109618 / 109619) は 10/21 に修正され、10/26 に KEV に入った。Amazon によると、悪用の試みは修正の 4 日前の 10/17 から始まっていた。
  - Check Point では 9 月にも、Security Management Server (CVE-2026-93616) と Security Gateway (CVE-2026-85102) の RCE がゼロデイで悪用された。2024 年の CVE-2024-24919 (Remote Access / Mobile Access の任意のファイルの読み取り) も、同じ「Mobile Access の公開面」が入口だった。
  - TSGA / TSProxy は、ESET が UNC5221 (中国系) と結びつけた Ivanti VPN 向けのバックドア「PhiliKit」の変種。ただし Check Point は「確度の高い帰属はできない」とし、初期アクセスブローカー、偽旗 (イスラエルのセキュリティ企業 Dream Security の名前を使った置き手紙)、目くらましの可能性も挙げている。
- **なぜ今これが重要か (評価)**:
  - 境界の機器に「Web の RCE + ローカルの root 昇格」をそろえて持つ攻撃者が、ゲートウェイを足場に仮想基盤を壊しに来た。情報を盗むだけでなく、破壊が目的の攻撃が境界の機器から始まった点が重い。
  - **PHP2Shell を当てただけでは足りない**。10/30 以降に侵入されていれば、TSGA はバックアップとスナップショットにも残る。修正を当てたかどうかと、侵害されていないかは別に確認する必要がある。
  - KEV の期限が 3 日と短いのは異例。国内でも Mobile Access / Remote Access を公開している Check Point の機器は多く、CVE-2024-24919 のときと同じく、診断や調査の依頼が増えるとみる。
  - バリアントを探す観点としては、「root のデーモン + 誰でも書ける Unix ソケット + 接続元の認証なし」は、他のアプライアンスにもよくある型だ。診断で Linux ベースの機器のシェルを取ったら、`find / -type s -perm -o+w 2>/dev/null` と、そのソケットを持つプロセスの権限を見る価値がある。
- **読者が今日できること**:
  - 11 月の Jumbo Hotfix (PHP2Shell と CVE-2026-123039 の両方を修正) を、公開の Mobile Access があるゲートウェイから当てる。すぐに当てられない場合は、Check Point の暫定策のとおり `dynamic_server` を止め、再起動しないようにする。
  - エキスパートモードで侵害の痕跡を調べる: `grep -rl upload_progress_pwn /opt/CPcvpn-*/tmp/`、`find / -name 'zz*.tpl' -o -name '.up.tpl' 2>/dev/null`、`ls -la /lib/libcpfwcommon.so /tmp/.p_sock /tmp/.bd.log`、`netstat -lntp | grep 11072`、10/30 以降の `/var/log/messages` での httpd の segfault の急増。
  - ゲートウェイから内部の ESXi への SSH (`vpxuser`) と、ESXi の `/tmp/des` を探す。侵害が見つかったら、機器を作り直し、VPN 利用者の資格情報とゲートウェイの証明書・鍵を入れ替える。
- 出典: [Check Point Research (2026-11-12)](https://research.checkpoint.com/2026/php2shell-exploitation-on-check-point-gateway/) / [Check Point sk1000362](https://support.checkpoint.com/results/sk/sk1000362) / [BleepingComputer: 0-day の修正 (2026-11-13)](https://www.bleepingcomputer.com/news/security/check-point-patches-zero-day-that-lets-hackers-get-root-access/) / [BleepingComputer: ESXi のワイパー (2026-11-13)](https://www.bleepingcomputer.com/news/security/check-point-gateways-hacked-via-php2shell-to-deploy-vmware-esxi-wiper/) / [The Hacker News (2026-11-13)](https://thehackernews.com/2026/11/hackers-exploit-php2shell-flaws-in.html) / [SecurityWeek (2026-11-13)](https://www.securityweek.com/php2shell-exploited-in-destructive-check-point-gateway-attacks/) / [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

<details><summary>IoC (SHA-256、Check Point Research の公表値)</summary>

- tpl の Web シェル: `edb3e92eb7bda7413a09edcc4b1ba3cbed4bcdf42808a8abce63b6e4c3fda2b3`
- slot_CPconfigdaemon: `4171b521fa6441382aa2fa014a08e18ff9a6e0ab6096c9144072bf46b37a2ec8`
- CPconfigdaemon: `d7549671c7189979f0624ec52dad9ea6a707d23146e3585ab8f8c4720eca0c63`
- gogo: `3b51080a909023f7d484e2443740b572307ce0054eb9e32d98f0a06bfcd2db90`
- destroy_v6: `c7d9477309fac6c638a1128442056a242de086996add8cb49cd6496c36003237`
- DREAM_ANNEXATION.txt: `0522937c0c0337be54fe25493539e5f5f8ceb9742c980aaff1cfc9515f3a96f7`
- philistine: `ee16e1695711b9d60c62925fcfb2fe1a29c18ae26565bc05410a14e16d2a39d7`
- libdssafe.so: `fb1a6235eb6bce8c9ec8cd8bb85f17c9c2bde8ecb45b7a243a30ceadf26654da`

</details>

## AI 技術・トレンド

### [2026-11-13] OpenAI「ChatGPT Wallet」: エージェント「dots」が利用者の代わりに決済まで行う。まず米国の Pro 契約者の一部から
- **何が起きたか**: OpenAI は、ChatGPT のエージェント「dots」が商品を選び、決済まで行う「ChatGPT Wallet」を出した。対象は、米国の ChatGPT Pro 契約者の一部 (18 歳以上) で、米国発行の Visa / Mastercard / American Express を持つ人。決済はカード番号の代わりに支払いトークンを使い、OpenAI は「カード番号は dot にも販売者にも渡らない」と説明する。購入の前に、利用者が品目、合計金額、カードを確かめ、Face ID や指紋で承認する。今後は、利用額や品目の種類を決めた「事前承認」で、より自律的に買えるようにする予定。
- **なぜ重要か**: エージェントが決済の能力を持つと、間接プロンプトインジェクションの被害が「データの持ち出し」から「お金の移動」に広がる。今は購入ごとに生体認証が要るので、検証点は「確認画面に出る内容」と「実際の注文」の食い違いになる。事前承認が入れば、人の確認がなくなり、そこからが本当の攻撃面になる。
- 出典: [TechCrunch](https://techcrunch.com/2026/11/13/chatgpts-new-wallet-lets-ai-agents-shop-and-check-out-for-you/) / [Help Net Security](https://www.helpnetsecurity.com/2026/11/13/openai-chatgpt-wallet/)

### [2026-11-13] Google、Gemini アプリに Google Wallet を接続。Plaid 経由で銀行やカードの取引を読み、家計を分析
- **何が起きたか**: Google は、Gemini の「Personal Intelligence」でつなげるアプリに Google Wallet を加え、米国の全利用者 (Web / Android / iOS) に 11/13 から順に提供する。Plaid でつないだカードや銀行の取引を Gemini が読み、支出のグラフ化や、値上がりしたサブスクの検出をする。Google は「Gemini は読むだけで、お金を動かせない」と説明している。Gemini が覚えている内容を一覧で直せる「Memory Summary」も加えた。
- **なぜ重要か**: 「読むだけ」でも、取引の履歴は機密性が高い。同じセッションで Gmail や Web の文章 (攻撃者が書けるもの) も読むので、インジェクションで取引の情報を外に出させる経路 (Markdown の画像、リンクの描画、ツールの呼び出し) が検証点になる。同じ日に OpenAI も決済機能を出しており、エージェントが金融データを扱うことが一気に普通になりつつある。
- 出典: [Google](https://blog.google/innovation-and-ai/products/gemini-app/google-wallet-gemini-app/)

### [2026-11-12〜13] Google の Gemini 搭載メガネ「Intelligent Eyewear」: 米国と韓国で予約開始、395 ドルから、12/10 発売。周りの人のプライバシー対策も説明
- **何が起きたか**: Google は予約を始め、プライバシーの設計を説明する記事も出した。撮影中は外向きの LED が光る、映像の顔を自動でぼかす、指向性マイクで装着者の声だけを拾う、Gemini に見せた映像は履歴に残さず学習や広告に使わない、物理的な電源スイッチがある、という内容。
- **なぜ重要か**: 常にカメラが動く端末で、Gemini は「見たもの」を入力として読む。看板や画面の文字が、そのまま視覚経由の間接インジェクションの経路になる。LED や顔のぼかしをファームウェアやアプリの改ざんで外せるかは、ハードウェアの検証の論点になる。
- 出典: [Google (プライバシー)](https://blog.google/innovation-and-ai/technology/safety-security/intelligent-eyewear-privacy-protections/) / [Google (予約)](https://blog.google/innovation-and-ai/technology/xr-ar/google-intelligent-eyewear-collections-pre-order/) / [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2611/13/2000003166/)

### [2026-11-12] AWS「次世代の AgentCore Runtime」: エージェントのセッションの起動が最大 15 倍速く、使えるコンピュートは 4 倍。S3 をセッションにマウント可能に
- **何が起きたか**: AWS は Amazon Bedrock AgentCore の実行基盤を更新した。セッションごとに専用の Firecracker microVM で動く点は同じ。AWS は、初期化済みの環境を復元する方式で起動が最大 15 倍速い、セッションあたりのコンピュートが最大 4 倍、待ち時間の多いエージェントでメモリの消費が最大 68% 減る、とうたう。S3 のバケットなどを FUSE でマウントできるようにし、常に動くエージェント向けの料金 (Lambda MicroVM と同じ単価) も加えた。
- **なぜ重要か**: 「初期化済みの環境を復元する」方式では、スナップショットの中の乱数の状態、一時的な認証情報、キャッシュがセッションの間で共有されないかが、よく知られた検証点になる。S3 のマウントで、エージェントが触れるデータの範囲が広がるので、セッションの IAM がバケットやプレフィックスの単位で絞られているかを確かめたい。
- 出典: [AWS Machine Learning Blog](https://aws.amazon.com/blogs/machine-learning/run-agents-securely-and-efficiently-with-the-next-generation-agentcore-runtime/)

### [2026-11-13] llama.cpp と ggml が v1.0.0 に。今後は API / ABI の互換性を壊す変更でメジャー版を上げる
- **何が起きたか**: Hugging Face の ggml-org は、始まってから約 3.5 年の llama.cpp と ggml を v1.0.0 にし、セマンティック バージョニングに切り替えた。対応するモデルのアーキテクチャは 150 種類を超える。CI には HF Buckets と HF Jobs を使い、NVIDIA、AMD、Qualcomm、Arm、IBM、Intel からハードウェアの支援を受けている。
- **なぜ重要か**: llama.cpp は Ollama や LM Studio など多くのローカル LLM アプリに組み込まれている。GGUF の解析の欠陥はこれまで何度も CVE になってきた。版の意味がはっきりすることで、downstream の製品に入っている版と脆弱性をつき合わせやすくなる。SBOM で llama.cpp / ggml の版を追う準備をしておきたい。
- 出典: [Hugging Face Blog](https://huggingface.co/blog/ggml-org/llama-cpp-v1)

### [2026-11-13] LangChain、Series C で 3 億ドルを調達。評価額は 30 億ドルで、約 1 年前の 2 倍超
- **何が起きたか**: CapitalG が主導し、GIC、DFJ Growth、IVP、Sapphire Ventures も出資した。約 1 年前 (1 億 2,500 万ドルの調達) の評価額は 12.5 億ドルだった。LangChain は、エージェントの開発・管理の製品「LangSmith」の顧客が 7,000 社 (Harvey、Rippling、NVIDIA、トヨタ、Salesforce など) だと主張している。
- **なぜ重要か**: LangChain / LangGraph / LangSmith は企業のエージェントの基盤として広く入っており、これまでもデシリアライズやプロンプトのテンプレートの処理で重い脆弱性が出てきた。ペンテストでは、LangSmith のトレースにプロンプト、ツールの結果、秘密情報が残っていないかを確かめる価値がある。
- 出典: [TechCrunch](https://techcrunch.com/2026/11/13/ai-agent-startup-langchain-hits-3b-valuation/)

### [2026-11-12] Meta のエージェント「Muse」が、利用者の代わりに米国の企業へ電話をかけられるように (有料の契約者のみ)
- **何が起きたか**: Meta は、9 月から一部で試していた電話の機能を、有料の契約者すべてに開いた。料金は月 20 ドル (週 5 億 Muse トークン) と月 100 ドル (週 30 億トークン)。Meta は利用者が 1,000 万を超えたとしている。既報の Muse 専用のメールアドレスは、近く無料の利用者にも広げると Alexandr Wang 氏 (最高 AI 責任者) が述べた。
- **なぜ重要か**: 電話での本人確認 (生年月日、住所などの知識による確認) に、AI が本人の代わりに答えるようになる。受ける側には、正当な代理と、AI の声を使ったなりすましとの区別がさらに難しくなる。コールセンターは「AI エージェントからの電話」を前提に、本人確認の手順を見直す必要がある。
- 出典: [TechCrunch](https://techcrunch.com/2026/11/12/muse-can-now-place-calls-to-u-s-businesses-if-you-pay/)

### [2026-11-12〜13] 中国の主要なオープンウェイトモデルの重みに「Blackwell で学習した痕跡」があるとの分析。NVIDIA は「チップの位置の追跡はできる」と議員に非公式に伝えていた
- **何が起きたか**: 元 OpenAI の研究者 Will DePue 氏は、DeepSeek、Moonshot AI、MiniMax、Ant Group の重みを分析し、Kimi K3 系と DeepSeek V4 系に、輸出が禁じられた Blackwell で学習した痕跡があると主張した (規制違反や、国外のデータセンターでないことまでは示せないとしている)。MIT Technology Review によると、Bill Foster 下院議員は、NVIDIA の担当者が「チップの位置を追跡する仕組みは技術的に可能」と非公式に伝えたと話した。追跡を義務づける Chip Security Act に、業界団体は「実現できない可能性がある」と反対していた。
- **なぜ重要か**: 「重みから学習に使ったハードウェアを推定する」手法は、モデルの由来の監査 (モデルのサプライチェーン) に使える可能性がある。チップの位置の追跡が義務になれば、GPU のファームウェアに通信と証明の仕組みが入り、なりすましや位置の偽装という新しい攻撃面ができる。
- 出典: [TechCrunch (2026-11-13)](https://techcrunch.com/2026/11/13/export-banned-nvidia-chips-are-behind-chinas-most-powerful-ai-models-uh-oh-jensen/) / [MIT Technology Review (2026-11-12)](https://www.technologyreview.com/2026/11/12/1148483/nvidia-chip-tracking/)

### [2026-11-13] [続報] Anthropic の IPO: 日本語の案内ページを公開。NASDAQ のティッカーは「ANT」、価格は 11/19 に決定。国内ではみずほ、SBI、楽天、三菱 UFJ MS の 4 社で抽選
- **何が起きたか (前回からの変化)**: Anthropic は IPO の日本語の案内ページを出した。発行価格は日本時間の 11/19 に決まり、取引は米国時間の 11/19 に始まる見込み。2026 年第 3 四半期の売上は 170 億ドル、純損失は 233 億ドルと示している。
- **なぜ重要か**: 話題の IPO は、偽の申込サイトや偽の証券会社のフィッシングの材料になる。日本語の案内が出たので、日本向けの詐欺も増えると考えられる。正規の窓口は 4 社に限られることを、社内の注意喚起に使える。
- 出典: [Anthropic IPO 案内 (日本語)](https://ipo.anthropic.com/jp/) / [GIGAZINE](https://gigazine.net/news/20261113-anthropic-ipo/)

### [2026-11-12 発表 / 11-13 報道] 国内: NTT、少ない業務マニュアルから LLM に知識を覚えさせるチューニングの技術を発表。tsuzumi 2 と Llama 3 (3B) で先行研究を上回る
- **何が起きたか**: LLM 自身がマニュアルから仕様書や FAQ など形式の違う学習データを作り、それで学ぶ (「多角的な学び」)。マニュアルの範囲から作った問題の正答率で、tsuzumi 2 と Llama 3 (3B) の両方で先行研究を上回ったと NTT は説明している。11/18〜25 の「NTT R&D FORUM 2026」で展示する。
- **なぜ重要か**: 社内文書をモデルの重みに覚えさせると、RAG と違って文書ごとのアクセス制御ができない。権限のない社員がモデルに聞くだけで内容を引き出せるおそれがある。導入するなら、学習に使う文書の機密区分を先に決めておく必要がある。
- 出典: [INTERNET Watch](https://internet.watch.impress.co.jp/docs/news/2155928.html)

## AI セキュリティ

### [2026-11-12 発表 / 11-13 報道] OpenAI「Daybreak Red Team」と「Daybreak Defense Factory」: Web アプリのペンテストと修正パッチの作成をエージェントで
- **何が起きたか**: OpenAI は 11/12 のイベント「Cyber at the Frontier」で 2 製品を発表した。**Red Team** (早期アクセス) は、複数のエージェントがソースコードとアプリの文脈から攻撃の経路を調べて脆弱性を確かめ、スキャナーの指摘やバグバウンティの報告を検証し、パッチの後に再テストする。OpenAI は「隔離された環境で動き、Guardian review でテストしてよいアプリとエンドポイントを制御する」と説明する。**Defense Factory** (ChatGPT のプレビューのプラグイン) は、Wiz、Snyk、Endor Labs の脆弱性の情報を取り込み、GitHub のリポジトリを監視して修正の下書きの PR を作る (自動デプロイはしない)。
- **なぜ重要か**: ペンテストと「報告の検証」がそのまま製品になった。読者の業務と直接競合し、同時に道具にもなる。報告の文面にインジェクションを仕込んで検証の結果を操る攻撃、Guardian のスコープの外 (SSRF、リダイレクトの追従) へ出る挙動、GitHub への書き込み権限の範囲は、導入前に確かめたい。
- 出典: [SecurityWeek](https://www.securityweek.com/openai-unveils-daybreak-red-team-defense-factory-security-tools/) / [Help Net Security](https://www.helpnetsecurity.com/2026/11/13/openai-daybreak-vulnerability-remediation-red-team-defense-factory-agents/)

### [2026-11-12] Microsoft「Trained to betray」: 追加学習のデータやチェックポイントにバックドアを仕込み、コーディングエージェントに攻撃者のスクリプトを実行させる
- **何が起きたか**: Microsoft Defender Research と AI Red Team は、追加学習のサプライチェーン攻撃を 2 つ示した。①約 9,000 件の端末操作の会話に細工した 90 件 (約 1%) を混ぜ、「プロジェクトのドキュメントを作って」という普通の依頼をトリガーに、攻撃者のドメインから取ったものを実行させる。gpt-4.1-mini の追加学習で、学習に含めたハーネスでは約 78% が成功した。②バックドアを仕込んだオープンウェイトのチェックポイントでは、見たことのないリポジトリで平均 84.1〜94.8% が成功した。公開のハブのある大きなデータセットにも、「簡単なファイル操作」に「リモートのスクリプトを `curl` して `source`」で答える行が数件あった (意図は不明としている)。
- **なぜ重要か**: トリガーが普通の依頼なので、プロンプトインジェクションの検知では見つからない。原因はモデルの内部にある。社内でエージェント用に追加学習するなら、学習データの「依頼」と「行動」が見合うかを機械的に照合する工程と、モデルの外の制御 (ツールの権限、外向きの通信の制限、コマンドの監査) が要る。11/13 号では日付を確認できず見送ったが、ページの datePublished (2026-11-12) で確認できたので今回採用した。
- 出典: [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/11/12/trained-to-betray-how-post-training-supply-chain-attacks-hijack-coding-agents/)

### [2026-11-13] Corelight:「版を固定した」MCP サーバーでも、依存パッケージは起動のたびに変わっていた。5 週間で 15 通り。原因は `uvx` がロックファイルを使わないこと
- **何が起きたか**: 管理者の端末で、決まったリリースに固定したはずの MCP サーバーが、5 週間で 15 通りの依存の組み合わせで動いていた。69 パッケージのうち 23 (cryptography、JWT のライブラリ、MCP の SDK を含む) の版が変わった。このサーバーは週に 1,600 回以上、ファイアウォールや SIEM など 11 の管理系に接続していた。35 の MCP サーバーを調べると、23 が推奨の導入手順のままでは起動やビルドのたびに公開レジストリから依存を取る。コミットで固定し、ハッシュ付きのロックファイルから 1 回だけ入れる方式に変えた 5 つは、457 回の起動で変わらなかった。
- **なぜ重要か**: MCP サーバーは利用者の認証情報を持ち、管理系に届く。依存のどれかに悪意のある版が数時間だけ出れば、それが管理者の権限で動く。診断では、`.mcp.json` や `claude_desktop_config.json` の `uvx` / `npx` / `latest` の起動の記述を洗い出す観点として使える。
- 出典: [Help Net Security](https://www.helpnetsecurity.com/2026/11/13/corelight-mcp-server-supply-chain/)

### [2026-11-13 報道] OpenAI Codex のリポジトリで、Issue の自動ラベル付けへのプロンプトインジェクションから npm の不正なリリースに至る経路 (報告者 Depi)。修正済み、報奨金は 1,000 ドル
- **何が起きたか**: issue-labeler のワークフローが、新しい Issue のタイトルと本文を Codex のエージェントに渡していた。報告によると、攻撃者はエージェントのサンドボックスでコードを実行し、.NET のデバッグ用のパイプ経由で GitHub のランナーのメモリからトークンを読み、書き込み権限のある rust-ci のワークフローのキャッシュを汚染できた。最後は、保守者が不正なリリースを消す操作で npm の信頼されたトークンが得られる仕組みだった。2 月の Cline の「Clinejection」と同じ型。元の Bugcrowd の開示日は確認できず、SecurityWeek の 11/13 のまとめの日付で採用した。
- **なぜ重要か**: 「AI に Issue を読ませる CI」は、外部の誰でも書ける入力を、権限を持つエージェントに渡す構造になる。GitHub Actions の診断では、LLM を呼ぶワークフローのトリガー (`issues`、`issue_comment`、`pull_request_target`) と、同じランナーで使うキャッシュやトークンの範囲を確かめたい。
- 出典: [SecurityWeek (In Other News)](https://www.securityweek.com/in-other-news-new-cisa-director-nominee-connected-car-hacking-baker-tilly-data-breach/) / [Bugcrowd の開示](https://bugcrowd.com/disclosures/3c0e5972-74ad-46a3-ab56-169db3d4c66f/backdooring-the-next-release-of-codex-through-github-action-pipeline-exploit-chaining)

### [2026-11-13] Elastic: AI のペンテスト基盤「CyberStrikeAI」のサーバーが、盗んだ認証情報で AWS の 4 アカウントを 16 日間探索。EC2 の user data を 141 ミリ秒で 56 件取得
- **何が起きたか**: 9/30〜10/16、香港の 1 台の CyberStrikeAI のサーバー (`43[.]240[.]29[.]11`、AS133199) が、5 つの IAM ユーザーと 3 つのインスタンスロールの認証情報を使った。GetCallerIdentity → Secrets Manager → EC2 の user data → 暗号化された SSM パラメーターの復号 → 29 秒後に SSM SendCommand、という順。アラートは 78 件出たが、すべて中・低の重大度で、14 日の空白のせいで決まった時間幅の相関ルールがつながらなかった。インスタンスロールの認証情報は SSRF かホストの侵害で取られたとみられる (経路は不明)。FOFA の検索式 `title=="CyberStrikeAI"` も示している。
- **なぜ重要か**: これまで Fortinet の機器を狙っていた AI の攻撃基盤が、クラウドで使われた例。機械の速さ (141 ミリ秒で 56 件) と、人の都合の空白 (14 日) が混ざると、時間幅で区切る相関の検知は破られる。クラウドの診断では、インスタンスロールに Secrets Manager や SSM の権限が広く付いていないかを優先して見たい。
- 出典: [Elastic Security Labs](https://www.elastic.co/security-labs/threat-command/cyberstrikeai-aws-cloudtrail-intrusion)

### [2026-11-11 講演 / 11-13 報道] Proofpoint:「AI に頼りすぎた攻撃者の攻撃は、かえって弱くなっている」
- **何が起きたか**: Proofpoint の Selena Larson 氏が IRISSCON 2026 (ダブリン) で講演し、「AI が攻撃者を強くする」という話はマーケティングの誇張でデータは裏づけていない、と述べた。AI で書いたマルウェアには動かないものやコメントと動作が食い違うものが多い、BEC の攻撃者 TA4903 は AI を使い始めてから件名・添付・本文が合わなくなった (本文が空のことも)、AI のコーディングツールで作ったフィッシングサイトは見た目が似通って見破りやすい、という。
- **なぜ重要か**: Unit 42 の Cairn など、AI で能力を上げた攻撃も実際にある (既報)。脅威の評価は「AI を使ったか」ではなく、攻撃者ごとの実際の成果で行うべきという、バランスをとる材料になる。「AI で作った痕跡」は検知の手がかりにもなる。
- 出典: [Infosecurity Magazine](https://www.infosecurity-magazine.com/news/hackers-ai-weaker-cyber-attacks/)

### [2026-11-11〜12 arXiv] エージェントの攻撃と防御の論文: 小さなモデルでも効くインジェクション対策「CapLite」、GPU の共有からエージェントの承認の設定を推定する「PolicySniff」、偽の警告でエージェントに作業をやめさせる攻撃
- **何が起きたか**: **CapLite** (2611.17115) は、CaMeL、Progent、IPIGuard、DRIFT のようにエージェント自身のモデルにセキュリティの成果物を書かせる方式は、小さなオープンウェイトのモデル (1.7B〜12B) では攻撃が通ると示した。代わりに、ツールのスキーマからポリシーを作り、宛先や金額などの引数が利用者の依頼に書かれているときだけ書き込みを許す。AgentDojo の攻撃 13,935 件で成功ゼロ、トークンは CaMeL の 18%。**PolicySniff** (2611.16158) は、同じ GPU の攻撃者が自分のカーネルの処理時間だけで、エージェントが重要な操作の前に確認するかを均衡正解率 94.17% で推定する。**偽の警告** (2611.14864) は、信頼の低い文書の「危険の警告」でエージェントに正当な作業をやめさせ、「慎重に」と指示するほど効く (Gemini で放棄率 9.8% → 86.3%)。**QHijack-LoRA** (2611.14978) は、量子化したときだけ判定を乗っ取る LoRA アダプター。
- **なぜ重要か**: CapLite の「書き込みの引数は利用者の依頼に書かれたものだけ」は、モデルの賢さに頼らない設計の原則として、エージェントの診断の基準に使える。PolicySniff と QHijack-LoRA は、ふるまいの監査だけでなく実行環境 (GPU の共有、量子化) まで含めて評価する必要を示す。
- 出典: [arXiv:2611.17115](https://arxiv.org/abs/2611.17115) / [arXiv:2611.16158](https://arxiv.org/abs/2611.16158) / [arXiv:2611.14864](https://arxiv.org/abs/2611.14864) / [arXiv:2611.14978](https://arxiv.org/abs/2611.14978)

### [2026-11-12 arXiv] LLM の「自然な書き換え」で CodeQL の警告を 26.2% 消せる (脆弱性は残る)。4B の小さなモデルで 4,000 超のプロジェクトを調べ、メモリ安全性の欠陥 187 件を確認
- **何が起きたか**: 2611.17123 は、LLM に CodeQL の警告の情報だけを渡し、データの流れの途中の関数を「普通の保守の変更」に見えるように書き換えさせた。実際の npm の脆弱性の 172 の流れのうち、3 回の書き換えで 26.2% の警告が消えた (1 件あたり約 0.51 ドル)。原因はライブラリのモデル化の 7 つの隙間で、最大のものは WHATWG の `URL` コンストラクタ (taint が query には伝わるが pathname には伝わらない)。2611.16565 は、4B の判定モデル Intern-Decision-4B で候補の関数を並べ、GB10 の 3 台で 4,000 超のプロジェクトを調べて、メモリ安全性の欠陥 187 件 (Critical 12、High 148) を確認した。
- **なぜ重要か**: CI の SAST の警告が「消えた」ことを「直った」とみなす運用は危ない。悪意のある貢献者が、警告を消す方向に書き換えたコードを送れる。`URL.pathname` のような具体的な隙間は、そのままコードレビューとソースコード診断の観点になる。安い GPU と小さなモデルで大規模な脆弱性の探索ができることも示された。
- 出典: [arXiv:2611.17123](https://arxiv.org/abs/2611.17123) / [arXiv:2611.16565](https://arxiv.org/abs/2611.16565)

## セキュリティニュース

### [2026-11-12 公表 / 11-13 KEV] Check Point のゲートウェイが PHP2Shell → 0-day の root 昇格 (CVE-2026-123039) で乗っ取られ、ESXi にワイパー
- **何が起きたか**: 今日の深掘りを参照。Check Point は数十の顧客で悪用を確認し、CISA は 11/13 に KEV に加えた (期限 11/16)。
- **悪用 / PoC**: 悪用を確認済み (ベンダー、CISA KEV)。公開の PoC は確認できていない。
- **なぜ重要か**: 境界の機器から仮想基盤の破壊まで進んだ。修正を当てたかどうかと、侵害されていないかは別に確認が要る。
- 出典: [Check Point Research](https://research.checkpoint.com/2026/php2shell-exploitation-on-check-point-gateway/) / [BleepingComputer](https://www.bleepingcomputer.com/news/security/check-point-gateways-hacked-via-php2shell-to-deploy-vmware-esxi-wiper/)

### [2026-11-13] [続報] UnrealIRCd の CVE-2026-114713 が KEV に追加。開発元も「実際に悪用されている」と追記
- **何が起きたか (前回からの変化)**: 11/7 号で紹介した、IRCv3 の `label` タグをエスケープしないことによるサーバー間のコマンドの注入 (6.0.0〜6.2.7、CVSS 8.6、CWE-140)。CISA は 11/13 に KEV に加え、期限を 11/16 とした。2 台以上をつないだネットワークで、一般の利用者が KILL や GLINE をサーバーの権限で実行できる。対策は 6.2.7.1 に上げるか、全サーバーで `hot-patch bundle-20261107` を実行すること。サポートの終わった UnrealIRCd 5 も影響を受ける。
- **悪用 / PoC**: 悪用あり (開発元、CISA KEV)。
- **なぜ重要か**: IRC はボットネットの C2 やコミュニティの基盤として今も使われる。KEV に載ったので、連邦機関以外でも急いで直す根拠になる。
- 出典: [UnrealIRCd フォーラム](https://forums.unrealircd.org/viewtopic.php?t=9487) / [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

### [2026-11-12 発表 / 11-13 報道] 米司法省と FBI: 北朝鮮の「FaceStealer」で 18 か月に 4 億ドル超が盗まれた。基盤と被害者の録画 900 件超を押収し、Binance から盗まれた 12 億ドル超を差し押さえ・凍結
- **何が起きたか**: 北朝鮮の BlueNoroff (Sapphire Sleet、UNC1069) の手口。乗っ取った Telegram などから知人を装い、Calendly で会議を設定する。偽の Zoom / Teams (`uu01webzoom[.]us`、`teams.livemeet[.]us`) で、以前の被害者の本物の録画やディープフェイクの映像を流し、「音が出ない」と言って ClickFix 型の「修正」を実行させる。参加者の映像も録画して次の攻撃に使う。司法省は、今年の Axios の npm パッケージの保守者の乗っ取りにも使われたとしている。FBI は IC3 の注意喚起 (CSA 261112) も出した。
- **悪用 / PoC**: 実際の被害 (司法省の発表)。
- **なぜ重要か**: OSS の保守者や開発者が「知人のビデオ通話」で狙われ、パッケージのサプライチェーンの入口になっている。「会議中に音声を直すため何かを実行させる」こと自体を、危険な合図として社内に周知する材料になる。
- 出典: [DOJ](https://www.justice.gov/opa/pr/justice-department-announces-actions-disrupt-north-koreas-massive-theft-cryptocurrency) / [FBI](https://www.fbi.gov/investigate/cyber/facestealer-cryptocurrency-theft-scheme) / [The Hacker News](https://thehackernews.com/2026/11/fbi-says-north-korean-hackers-stole.html)

### [2026-11-13] 携帯の事業者の中の機器を乗っ取って SMS の 2FA コードを横取り: 国家レベルの集団「SilentAir」(Enea)
- **何が起きたか**: Enea は、アジアの少なくとも 6 か国の携帯の事業者の中にある機器を乗っ取り、IPX に SS7 / Diameter の攻撃を流していた集団を「SilentAir」と名付けた。UpdateLocation などで標的の着信と SMS を乗っ取った機器に回させ、直後に 2FA のコードを受け取る例を確認した。攻撃のうち傍受が 18.3% を占める (監視企業の典型は 2.1%)。主な標的は台湾の人で、政治家や要人もいた。Enea は国家レベルの攻撃者と「高い確度」で評価したが、中国との関連は「低い確度」とした。事業者名や国名は公表していない。
- **なぜ重要か**: 「なりすましの信号」ではなく「事業者の中の機器の侵害」が確認された。SMS の OTP は、事業者側が破られれば利用者に何の兆候もなく破られる。SMS の OTP を使う認証の診断で、代替の要素を勧める根拠になる。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/silentair-hijacks-asian-telecom.html) / [SecurityWeek](https://www.securityweek.com/silentair-hackers-intercept-calls-sms-from-inside-mobile-networks/)

### [2026-11-13] ドイツの軍用ドローンのメーカー Quantum Systems が侵害される。地上管制ソフト QBase の不正な更新が配られたと報道。独軍は機体の運用を見合わせ
- **何が起きたか**: Quantum Systems は、10 月末に「敵対的な攻撃者」による侵害を検知したと認めた。Der Spiegel と Financial Times によると、経路はミッション計画のソフト QBase の不正な更新ファイル (更新の配信サーバーの侵害)。偵察ドローン Vector (独軍名 Falke) の計画に QBase が使われる。独軍は予防のため同社の機体を飛ばさず、演習からも外したと報じられた。対応には MAD、BfV、BSI が加わる。
- **なぜ重要か**: 防衛のサプライチェーンの「ソフトの更新の経路」が実際に侵害された。ウクライナを支援するドローン企業が続けて狙われている。更新の署名の検証が、端末側で本当に強制されているかは、組込み・OT の診断の基本の確認項目になる。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/german-military-drone-operations-disrupted-by-cyberattack/)

### [2026-11-13] Trezor、東南アジアの販売店で売られた Safe 5 の 3 台に、リカバリーフレーズを盗む部品が挟まれていたと確認
- **何が起きたか**: メイン基板と画面の間に追加の基板があり、正規のファームウェアや Secure Element には手を加えずに、画面に出るリカバリーワードとパスフレーズを読み取って携帯の回線で送っていた。対象は 8/20〜9/23 に CryptoBilis (インドネシア) で買われた 3 台。11/11 のファームウェア 2.13.1 で、この部品が情報を読めないようにした (すでに盗まれたフレーズは守れない)。Trezor は販売店網を約 80% 減らす。同じ販売店では Ledger の機器にも部品が見つかり、盗難に結びついていた。
- **なぜ重要か**: Secure Element に頼る機器でも、「表示の経路」を物理的に盗み見られると守れない。ハードウェアのサプライチェーン攻撃が実際に確認された例。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/cryptocurrency/trezor-confirms-crypto-stealing-implants-in-three-wallets-releases-fix/) / [The Hacker News](https://thehackernews.com/2026/11/trezor-confirms-hidden-hardware.html)

### [2026-11-13] AMD SEV-SNP に 2 つの新しい攻撃: 「Mior」は RMP の初期化を GPU のメモリにそらして機密 VM を読み書きし、アテステーションも偽装。「Skyfall」は起動に失敗した VM の状態を TSA で盗む
- **何が起きたか**: Mior (ETH Zurich) は、PSP が RMP を書き込む先を攻撃者が制御する PCIe の GPU のメモリにそらし、RMP の一部を初期化させない。デバッグを無効にした機密 VM を読み書きでき (1,000 回中 1,000 回成功)、悪意ある VM のアテステーションを無害に見せかけられた。条件はハイパーバイザーと BIOS の制御と PCIe の機器 (AMD の脅威モデルの範囲内)、EPYC 9135 (Zen 5) で実証。Skyfall (ETH Zurich + Google) は、VM の起動をわざと失敗させるとキャッシュに残る状態を TSA で読み、レジスタの値やディスクの鍵を取り出した (Zen 3 / 4)。AMD はファームウェアとマイクロコードを出し、サーバーメーカー向けのプラットフォームのファームウェアは Skyfall が 11 月、Mior が 12 月。
- **なぜ重要か**: 機密コンピューティングの「クラウドの事業者も信用しない」という約束は、ファームウェアの配布まで成り立たない。11/12 号の TSA-Fill に続く AMD の機密 VM への攻撃で、機密 VM を前提にした設計のレビューでは、プラットフォームのファームウェアの版を確認項目にしたい。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/new-mior-and-skyfall-attacks-let-rogue.html)

### [2026-11-13] Google Project Zero、開示の方針を「90+30」から「Full 90」に。2027 年 2 月に 60 日、2028 年 1 月に 30 日へ短縮
- **何が起きたか**: 報告から X 日後に、修正の有無にかかわらず開示する。猶予期間や、亜種の扱いなどの特例はほぼなくす。例外は、悪用が確認されたもの、他者がすでに公開したもの、ベンダーが求めたものだけ。理由として、LLM で「パッチから悪用までの時間はほぼゼロ」と考えるべきこと、同じバグを複数の主体が見つけるリスク、報告の数が「年に数件だったターゲットで週に数件」に増えたことを挙げる。
- **なぜ重要か**: パッチの後の「ソーク期間」は意味がない、と大手の研究チームが明言した。ベンダーの修正と、利用者のパッチの適用の両方の速さに圧力がかかる。読者が脆弱性を報告する側としても、自分の開示方針を見直す基準になる。
- 出典: [Project Zero](https://projectzero.google/2026/11/disclosure-policy.html)

### [2026-11-13] Europol と米司法省「Operation TorNado」: ダークウェブの市場の売り手と買い手 354 人を逮捕
- **何が起きたか**: Archetyp、Nemesis、Tor2Door、Bohemia、Kingdom の各市場の売り手と買い手が対象。2025 年 5 月〜2026 年 10 月に 14 か国が参加した。欧州で 6,000 万ユーロ超の現金と暗号資産、950 kg の薬物、57 丁の銃を押収し、米国では 1 億 5,000 万ユーロ超、4.8 トンの薬物、152 丁の銃を押収した。
- **なぜ重要か**: 2025 年の RapTor (270 人) を上回る規模。市場を閉鎖したあと、押収したデータから利用者を摘発する流れが定着している。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/police-arrest-354-vendors-buyers-in-global-cybercrime-crackdown/) / [Help Net Security](https://www.helpnetsecurity.com/2026/11/13/europol-dark-web-arrests-cybercrime/)

### [2026-11-13] [続報] Operation Endgame の Gootloader: 米国の 44 件超のランサムウェアの被害 (損失 2,880 万ドル) の入口だった。感染は世界で 2 万 5,000 台
- **何が起きたか (前回からの変化)**: DOJ が詳細を出した。改ざんした Web サイトを含む 100 台超のサーバーから Gootloader を取り除き、ドメインを押収した。2018 年からの感染は世界で 25,000 台。アクセス権はランサムウェアの集団に売られ、米国の被害は 44 件超、損失は 2,880 万ドル。国防総省と防衛産業も標的だった。Shadowserver が感染先に通知している。
- 出典: [The Record](https://therecord.media/gootloader-ransomware-doj-details)

### [2026-11-13] ドイツ連邦議会、情報機関に国外のシステムへのハッキングとサーバーの停止を認める法律を可決
- **何が起きたか**: 賛成 308、反対 190、棄権 71。BND は国外の脅威に対し、システムへの侵入、敵のサプライチェーンの妨害、国家系ハッカーのサーバーの停止ができるようになる。BfV は国内で通信の遮断や経路の変更ができる。AI による大量データの分析と顔画像の照合の法的な根拠も与える。人の生命や身体を危険にさらす措置は禁止。
- **なぜ重要か**: 欧州の主要国が「サーバーの停止まで含む能動的な防御」を法律にした。日本の能動的サイバー防御の運用と比べる材料になる。
- 出典: [The Record](https://therecord.media/german-parliament-passes-law-giving-spy-agencies-hacking-power)

### [2026-11-13] Huntress: Teams の会議の予約を装うデバイスコードフィッシング。「予約番号」に見せたコードを入力させてトークンを取る
- **何が起きたか**: 実在の幹部を装うタイポドメインのメール → Google の共有リンク → Teams の予約画面を装うページ。「Continue」で攻撃者側がデバイスコードを要求し、コードを「Booking Reference」としてカウントダウン付きで表示する。コピーすると本物の Microsoft のサインイン画面が開き、成功後は Calendly に移るので被害者は気づかない。キットは AES-256-GCM で暗号化され (鍵は同じページ)、JavaScript を実行しないスキャナーを避ける。MFA でエラーになると新しいコードで自動で再試行する。
- **なぜ重要か**: デバイスコードのフローは、ユーザーが本物の Microsoft の画面で認証するため、URL の確認では防げない。M365 の設定の診断では、条件付きアクセスでデバイスコードのフローを制限しているかを確認項目にしたい。サインインのログで python-requests や node の UA を探すのが検知の手がかりになる。
- 出典: [Help Net Security](https://www.helpnetsecurity.com/2026/11/13/microsoft-teams-device-code-phishing/)

### [2026-11-12] Elastic「SANSAR」: 認証のない Ray のジョブエージェントから GPU サーバーを乗っ取ってマイニング。GPU の使用率を 0% に偽装し、C2 の場所は Ethereum のコントラクトから取得
- **何が起きたか**: REF3364。Ray の head ノードのダッシュボードはループバックに限られていたが、ジョブエージェントはインターネットから認証なしで届いた。10/22 に探索、10/25 にリバースシェル。Rust 製の SANSAR が Tor で命令を受け、CPU / GPU のマイナーを管理する。NVML のラッパーで GPU の使用率を偽り、カーネルのルートキットでプロセス、ファイル、ソケットを隠す。バックドアは C2 のアドレスを Ethereum のスマートコントラクトから読む。
- **悪用 / PoC**: 実際の侵害 (Elastic の観測)。
- **なぜ重要か**: AI の学習基盤の「ダッシュボード以外の口」が露出していた。外部診断では、Ray のジョブ API (既定 8265) とエージェントのポート (52365) が外から届かないかを確かめたい。
- 出典: [Elastic Security Labs](https://www.elastic.co/security-labs/threat-command/sansar-linux-cryptomining-malware)

### [2026-11-13] 北朝鮮の偽の IT 人材: 1 年で 2,429 のペルソナが接触し、27 が入社の手続きまで進んだ (Material Security)
- **何が起きたか**: 面接以降に進んだのは 1,100。41% のペルソナが複数の組織に応募し、1 つは 19 社に応募していた。入社の手続きまで進んだ 27 のうち 18 は、同時にほかの会社でも選考中だった。入社手続きまで進んだ 4 社の共有の状態を調べると、SSN を含むファイルの 68% が全社員かリンクを知る全員に開かれていた。
- **なぜ重要か**: 「入社した瞬間に何が見えるか」が被害の大きさを決める。新入社員のアカウントから見える共有の範囲は、内部の診断や SaaS の設定の監査で見る価値がある。
- 出典: [Help Net Security](https://www.helpnetsecurity.com/2026/11/13/north-korean-it-workers-onboarding/)

### [2026-11-13] 短信
- **Microsoft、11 月の更新の不具合を認める**: 幅か高さが 0 の画像を含む文書の印刷の失敗 (GDI)、ライセンス認証の 0x80041008 の失敗、10 月のプレビューを入れた Windows 11 で更新が入らない、の 3 つ。パッチの展開を止める判断にかかわる。[BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-says-november-security-updates-cause-printing-issues/)
- **テキサス大学アーリントン校**、10 月の攻撃で個人情報が盗まれたと確認。MachForms は止めたまま。ランサムウェア Qilin が犯行を主張している。[The Record](https://therecord.media/university-of-texas-arlington-warns-data-breach)
- **SANS ISC**: macOS の ClickFix「Macfinger」が配る情報窃取型マルウェアを「DownTheDRAIN」と命名。IOC は `45.150.32[.]130`、`171.22.131[.]24:8133`、配置先は `$HOME/Library/Caches/com.apple.update`。[SANS ISC](https://isc.sans.edu/diary/rss/33518)

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-11-12 以降 (NVD の published、UTC) / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-123039 | Check Point Gaia OS R81〜R82.20 (DynamicCLI) | CWE-732 / 862 / 7.8 | root で動く `dynamic_server` が、誰でも書き込める `/tmp/dynamic_socket` で接続元を確かめずに要求を受ける → ローカルの一般ユーザーが送った Clish のコマンドを root で実行 (`system()`) | [sk1000362](https://support.checkpoint.com/results/sk/sk1000362) (commit 不明) | **KEV (11/13 追加、期限 11/16)** / ITW / EPSS 0.013 |
| CVE-2026-110003 / CVE-2026-90908 | Azul Payara Server / Micro 4.x〜7.x (7.2026.11 / 7.6.0 / 6.44.0 / 5.93.0 で修正) | CWE-288 / 807 / 9.3 | ①管理 REST で `X-GlassFish-authToken` ヘッダーが **ある** だけで「リモートからの接続を拒否する」検査を省き、トークンが無効ならパスワード認証に進んで既定の空パスワードで通る → 未認証で管理コマンド。②JMX/RMI の認証が偽装できるクライアントのホストのアドレスで判定 → MBean の管理から RCE | [リリースノート](https://docs.azul.com/payara-community/release-notes/release-notes-7.2026.11.html) (commit 不明) | 未認証 RCE / GlassFish に水平展開 |
| CVE-2026-127029 / CVE-2026-127030 | FreeRADIUS (EAP-SIM / EAP-FAST) | CWE-787 / 7.5 | ①EAP-SIM: クライアントの identity を長さを確かめずに固定長の構造体へコピー。②EAP-FAST: セッションチケットの長さの検証不足 → 未認証でスタックのオーバーフロー、プロセスが落ちる | [diff](https://github.com/FreeRADIUS/freeradius-server/commit/e415f818dcdf91626e5e7314b3a4f819ab11f572) / [diff](https://github.com/FreeRADIUS/freeradius-server/commit/a5d09dad528d7a3a3c4c01158716ab85a12e09ef) / [diff](https://github.com/FreeRADIUS/freeradius-server/commit/064567a08f3b9d9b4863fab6060fafe296ac7de9) | 未認証 / EAP 実装 (hostapd 等) に水平展開 |
| CVE-2026-97692 / GHSA-gr74-333w-7wg8 (+ CVE-2026-52788、CVE-2026-102612 ほか計 30 件超) | bacnet-stack < 1.4.6 / 1.5.2 / 1.6.1 | CWE-787 / 7.7 | BACnet/SC のヘッダーオプションを MORE ビットだけで辿り、終端の MORE ビットも回数の上限も検査しない → 最初のフレーム (認証前) で 4 要素の固定配列の外へ書き込み。52788 はアドレス解決 ACK の URL で `utf8_urls[10][129]` の外へ書き込み、102612 はハブがクライアント証明書を必須にしない | [PR #1435](https://github.com/bacnet-stack/bacnet-stack/pull/1435) / [PR #1365](https://github.com/bacnet-stack/bacnet-stack/pull/1365) / [PR #1436](https://github.com/bacnet-stack/bacnet-stack/pull/1436) | 仕様起因で他スタックに水平展開 / OT (ビル制御) |
| CVE-2026-128321 (VU#644655) | TightVNC Windows Viewer 1.3.10 (**修正なし**) / UltraVNC Viewer < 1.8.2.8 | CWE-122 / — | Tight エンコーディングの `DecompressJpegRect()` が行バッファを固定の最大幅 8,192 px で確保し、変換ループはサーバーが指定した矩形の幅を使う → 悪意あるサーバーに接続したビューアでヒープの範囲外書き込み (幅 8,257 px から) | [VU#644655](https://kb.cert.org/vuls/id/644655) (commit 不明) | RFB の Tight JPEG の他実装 (libvncclient、TigerVNC、Remmina) に水平展開 / CERT/CC が DoS を実証 |
| CVE-2026-68548 / GHSA-vm84-8c4p-64hx | Algernon < 1.17.10 (Go の Web サーバー) | CWE-178 / 863 / 9.4 | `/admin` `/repo` `/data` の保護を大文字小文字を区別する `strings.HasPrefix` で判定し、ファイルは生のパスで開く → 大文字小文字を区別しない FS (NTFS、APFS) で `/Admin/secret.lua` により認可を回避し、読み取りと Lua の実行 | [GHSA](https://github.com/xyproto/algernon/security/advisories/GHSA-vm84-8c4p-64hx) (commit 不明) | 「認可は文字列、解決は FS」の型で水平展開 |
| CVE-2026-126312 / GHSA-736f-82w7-hj22 (+ CVE-2026-126310 / GHSA-q824-44ff-f5j5) | OpenBao < 2.6.5 / 2.7.x < 2.7.2、openbao-plugins (LDAP / RADIUS) < 0.2.0 | CWE-178 / 7.1 (126310 は 8.7) | AppRole、Cert、LDAP、RADIUS の auth で、ACL を判定するパスとバックエンドが暗黙に正規化して引くキーが違う → 正規化していないパスで ACL の deny を回避。126310 は `client_credentials` を許した **public** クライアントが client_id だけで OIDC の ID トークンを取得 | [GHSA-736f](https://github.com/openbao/openbao/security/advisories/GHSA-736f-82w7-hj22) / [GHSA-q824](https://github.com/openbao/openbao/security/advisories/GHSA-q824-44ff-f5j5) (commit 不明) | 秘密情報の管理基盤 / HashiCorp Vault の同じ auth method に水平展開 |
| CVE-2026-126276 / GHSA-4cx5-q9xx-5pgj | NocoDB < 2026.08.1 | CWE-287 / 8.2 | トークンエンドポイント (`oauth-token.service.ts`) が PKCE を機密クライアントの認証の **代わり** として扱い、client_secret がないと検証を飛ばす → 認可コードと verifier を盗んだ攻撃者が、秘密なしでアクセストークンと 60 日のリフレッシュトークンを取得 | [GHSA](https://github.com/nocodb/nocodb/security/advisories/GHSA-4cx5-q9xx-5pgj) (commit 不明) | OAuth の仕様の誤読 (RFC 7636 / 9700)。自前の OAuth サーバーに水平展開 |
| CVE-2026-128067 / GHSA-xcvg-w56q-r89m (+ CVE-2026-128066) | Pillow 2.3.0〜12.3.0 (13.0.0 で修正) | CWE-787 / 8.4 | TIFF の保存で、`exif=` / `tiffinfo=` / 元の IFD の ImageWidth・ImageLength・SamplesPerPixel を libtiff に渡すが、行バッファは実際の寸法で確保 → ヒープの内容が出力に混入、Predictor 2 ではヒープを破壊。128066 は IFD のタグの値を制限なく保持し、メモリ消費が入力サイズの 2 乗 | [diff](https://github.com/python-pillow/Pillow/commit/53318b50e8e9e85a57d033d4d879e1398d97aeb1) / [diff](https://github.com/python-pillow/Pillow/commit/ec5f1cbcf67275641abaad5c065ffb64a0a804a9) / [diff (128066)](https://github.com/python-pillow/Pillow/commit/4908edaf7f416616784c7c03d8c1a60153710ffb) | 利用者が非常に多い / libtiff を包む他実装に水平展開 |
| CVE-2026-91007 / GHSA-jr35-f52j-fm88 | Zephyr RTOS (`CONFIG_USERSPACE`、charger ドライバー) | CWE-822 / 7.8 | syscall の検証 `z_vrfy_charger_set_prop()` が `prop` を見ずに `union charger_propval` を丸ごと渡し、union に関数ポインタのメンバーがある → ユーザーモードのスレッドが登録したポインタを、ドライバーが特権モードで呼ぶ → カーネル権限で制御フローを奪取 (get 側でアドレス漏えい) | [diff](https://github.com/zephyrproject-rtos/zephyr/commit/5467b7a73fe093d7e9562ee15c321cf8f1639d17) | 「union を検証せずに境界を越えてコピー」で他ドライバーに水平展開 |
| CVE-2026-126673 | Data::Dump::Streamer (Perl) < 3.00 | CWE-94 / — | `_dump_qr` が正規表現を `qr` リテラルに書き出すとき `$` `@` をエスケープせず、エスケープ済みの区切り文字を二重にエスケープして裸にする → ダンプを `eval` / `do` で戻すと `@{[ ... ]}` が実行され任意の Perl コード | [diff](https://github.com/demerphq/data-dump-streamer/commit/c457f61c51aaefd4948810c1eddacf558e820d0f) | 「コードとして読み戻すシリアライザー」の型 (Data::Dumper、serialize-javascript 等) |
| CVE-2026-91141 (VU#128947) | COVESA vsomeip ≤ 3.7.3 (3.7.4 で修正) | CWE-789 相当 / — | 既定の設定で TCP の SOME/IP のメッセージに大きさの上限がなく、ヘッダーの 32 ビットの length を信じて受信バッファを広げる → 16 バイト 1 通で最大 4 GB を確保し、未認証で OOM による停止 (クライアント側も同じ) | [VU#128947](https://kb.cert.org/vuls/id/128947) (commit 不明、issue #1009) | 車載の仕様起因で他の SOME/IP 実装に水平展開 / 報告者の解説公開 |

- 公開日 (NVD、UTC): 123039 = 11/12、128321 = 11/13、110003・90908 = 11/12、127029・127030 = 11/12、97692・52788・102612 = 11/13、68548 = 11/12、126312・126310 = 11/13、126276 = 11/13、128067・128066 = 11/13、91007 = 11/12、126673 = 11/12、91141 = 11/12。
- EPSS (11/13 時点): いずれも 0.5 未満。最も高いのは CVE-2026-123039 の 0.0127。bacnet-stack の 3 件はまだ算出されていない。
- 次点: MongoDB C# Driver の BSON で、ポリモーフィックなデータを型の緩いメンバーに戻すと型の allow-list を回避でき、ガジェットがあれば RCE (CVE-2026-126982、7.7、commit 不明)。

### 今日の CVE 所感

- いちばん多かったのは、「**認可を判定する文字列**」と「**実際に解決される対象**」の食い違いだ。Algernon (大文字小文字と FS)、OpenBao (暗黙の正規化と ACL)、Payara (ヘッダーが「ある」だけで検査を省く) が当てはまる。認可の前と後で、正規化と大文字小文字の扱いを比べる観点は、Vault、GlassFish、Go や Rust の Web サーバーに横展開しやすい。
- 次は、「**相手が申告した長さや寸法を信じて、固定のバッファや確保量に使う**」型だ。VNC の Tight JPEG (矩形の幅)、vsomeip (SOME/IP の length)、BACnet/SC (MORE ビットの連鎖)、FreeRADIUS の EAP-SIM / EAP-FAST、Pillow (TIFF のタグと実際の寸法) が当てはまる。どれもプロトコルや形式の仕様の水準の話なので、libvncclient、TigerVNC、他の SOME/IP や BACnet のスタック、hostapd の EAP サーバーを同じ入力で試す価値が高い。
- OAuth の誤実装 (NocoDB の「PKCE をクライアント認証の代わりにする」、OpenBao の「public クライアントに client_credentials を許す」) は、自前で OAuth / OIDC のプロバイダーを実装した OSS で探しやすい。
- 診断の優先度は、①KEV に入った Check Point Gaia (他の脆弱性と連鎖する前提ですぐ適用)、②Payara の未認証の管理 RCE (既定の空パスワード)、③FreeRADIUS と BACnet/SC (未認証で境界に置かれる)、④修正の出ない TightVNC のビューア (利用をやめる)、の順とみる。

## 日本国内のセキュリティ動向

> 採用範囲: 公表日 2026-11-12〜14 (JST)。調査時点 (11/14 05:15 頃) では 11/14 付の公表は確認できず、中心は 11/13 (金) の公表。11/12 公表分は、前号 (11/13 号) で扱っていないものに限った。

### 国内インシデント・事故

#### [2026-11-13] プレイド「KARTE」に不正アクセス。全プロジェクトで計測、配信、管理画面を止める。同日夜「漏えいした可能性のある情報を確認し、該当顧客にメールで連絡」
- **何が起きたか**: プレイド (東証グロース) は 11/13 17:00 の適時開示で、CX プラットフォーム「KARTE」への第三者からの不正アクセスを 11/13 に検知し、緊急メンテナンスとして KARTE 全体を止めたと発表した。対象は「KARTE をご利用の全てのプロジェクト」で、Web・アプリの計測、各種の配信、管理画面の操作など全機能を順に止める。KARTE Message の一括メール配信や、KARTE Datahub のジョブフロー (KARTE の内外のデータ連携) は、処理の途中で止まる場合がある。ステータスページでは 14:44 に「Investigating」として停止を告知し、23:35 の更新で「外部に漏洩した可能性のある情報を確認し、該当のお客様にはメールにてご連絡させていただきました」とした。侵入経路、漏えいした情報の種類と件数、再開時期は未公表。業績への影響は精査中。
- **なぜ重要か (評価)**: KARTE は多くの国内の EC、金融、メディアのサイトにタグとして埋め込まれ、来訪者の行動データ、会員の属性、接客ポップアップ、メール配信を一手に担う。攻撃者が管理画面や配信の機能を握れば、多数の顧客サイトに任意のスクリプトや接客 (偽のフォーム) を配信できる位置にあり、全停止の判断はその危険を示唆する。Datahub はクラウド DWH などの外部と連携するので、連携用の認証情報の漏えいも疑うべきだ。KARTE を使う組織は、(1) 自社サイトのタグの読み込みを一時的に外すか、CSP で制限するかの判断、(2) Datahub の連携先 (BigQuery、S3 など) の認証情報の入れ替え、(3) 停止前後に配信された接客やメールの内容の確認を急ぎたい。顧客企業の公表が続く可能性が高い。
- 出典: [プレイド (2026-11-13, TDnet)](https://www.release.tdnet.info/inbs/140120261113580181.pdf) / [KARTE Status (2026-11-13 14:44〜23:35 JST)](https://status.karte.io/incidents/rs1gsmckc197)

#### [2026-11-13] マネックス証券: 委託先が運営する口座開設システムに不正アクセス。メールアドレス最大 113 万件と、本人確認書類の画像 1,592 件 (マイナンバーカード表面、運転免許証、セルフィー) が漏えいのおそれ
- **何が起きたか**: マネックス証券は 11/13 18:12、外部委託先が運営・管理する一部の口座開設システムへの不正アクセスで、個人情報が漏えいしたおそれがあると発表した。委託先が 10/18 に不正アクセスの試みを確認し、10/19 に外部からのアクセスを遮断し、一部の口座開設を止めている。11/13 の専門機関の中間報告で漏えいのおそれが判明した。対象は (1) 2019/10/16 以降にオンライン口座開設の最初の手続きで登録したメールアドレス、最大 113 万件 (口座開設を完了しなかった人を含む)、(2)「撮影が必要な方式」で提出した本人確認書類の画像 1,592 件 (マイナンバーカードの表面、運転免許証の表面・裏面、セルフィー画像)。個人番号 (裏面) と、公的個人認証の方式での申込は対象外。口座番号やパスワードは同じ DB になく、基幹システムとは別系統で、不正取引は確認していない。原因は調査中。
- **なぜ重要か (評価)**: eKYC の画像 (顔写真と身分証のセット) は、他社での口座開設のなりすましや、SIM の乗っ取りに直接使える。パスワードと違って変更できない。口座開設の受付システムは、基幹とは別系統として委託先に任されやすく、データの保存期間 (7 年分のメールアドレス、提出済みの画像) が長くなりがちだ。eKYC を委託する事業者の診断では、審査が終わった画像の削除期限、委託先の管理画面の認証、オブジェクトストレージの公開範囲を確認したい。発覚から公表まで約 4 週間かかった点も、検知と調査の体制の論点になる。
- 出典: [マネックス証券 (2026-11-13, PR TIMES)](https://prtimes.jp/main/html/rd/p/000000595.000005159.html) / [EnterpriseZine (2026-11-13)](https://enterprisezine.jp/news/detail/25489)

#### [2026-11-12] Qoo10 (eBay Japan): 11/6 に不正アクセス。氏名、住所に加え「住所の地理座標」「顧客が任意で入力した身体的特徴」なども閲覧の可能性。認証トークンを全て無効化
- **何が起きたか**: ITmedia NEWS によると、会員 3,000 万人超の EC モール「Qoo10」を運営する eBay Japan は 11/12、11/6 に同社のシステムが不正アクセスを受け、一部の個人情報が閲覧されたと発表した。対象となる可能性があるのは、氏名、ニックネーム、メールアドレス、電話番号、生年月日、性別、プロフィール情報、住所と配送先、住所の地理座標、顧客セグメント情報、任意入力の身体的特徴、アカウント識別情報、IP アドレス、個人メモ、ポイント残高。決済情報やパスワードの漏えいを示す証拠は現時点でない。検知後に遮断し、不正に発行・利用された可能性のある認証トークンをすべて無効にし、影響の可能性があるアカウントを強制的にログアウトさせた。件数は未公表。
- **なぜ重要か (評価)**: 「不正に発行された認証トークン」という表現から、トークンの発行処理か、セッション管理の側に問題があった可能性がある (公式は手口を明らかにしていない)。項目の幅 (身体的特徴、地理座標、セグメント) から見て、個別の API ではなく、顧客プロファイルを横断して参照できる内部の基盤まで届いたとみられる。EC の診断では、トークンの発行 API の認可、管理者・CS 用の顧客検索機能の権限、トークン失効の仕組みを確認したい。
- 出典: [ITmedia NEWS (2026-11-13)](https://www.itmedia.co.jp/news/article/2611/13/2000003186/) / [Qoo10 の告知 (2026-11-12)](https://www.qoo10.jp/gmkt.inc/Main/PopupNotice.aspx?nid=6246) ※告知ページは調査環境から取得できず (HTTP 523)、内容は ITmedia で確認

#### [2026-11-12] Yeny (TISインテックグループ): API の接続設定の不備で、ultra pay カードなどの会員の電話番号と会員 ID 1,332,505 件 (退会者を含む) が漏えい
- **何が起きたか**: Yeny は 11/12、管理する会員情報の一部が第三者の不正アクセスで漏えいしたと発表した。10/31 に接続先の事業者から「不審な API コール」の連絡を受け、11/2 に API 接続の設定の不備が原因と確認し、緊急メンテナンスで対応した。11/5 に漏えいを確認し、11/6 に関東財務局と個人情報保護委員会に報告した。対象は「ultra pay カード」と、PayBlend を使ったアスルクラロ沼津 Pay、巫神こん Pay、東芝ブレイブルーパス東京 Pay の会員で、電話番号と同社固有の会員 ID の 1,332,505 件。決済情報の漏えいは確認していない。
- **なぜ重要か (評価)**: 攻撃に気づいたのは自社ではなく、API の接続先だった。BtoB の API 連携で、接続元の範囲や取得できる項目の制限が設定どおりに効いていない型は、ペンテストで見つかりやすい一方、平常の監視では埋もれやすい。電話番号と会員 ID の組は、決済アプリを装う SMS フィッシングにそのまま使える。API の診断では、パートナー用の API キーの権限 (取得できる項目と件数)、レート制限、大量取得の検知を確認したい。
- 出典: [Yeny (2026-11-12)](https://yeny.jp/pressrelease/1547/)

#### [2026-11-13] ヒューマンアジャスト: 委託先ソニックムーブの LINE マーケティング SaaS「COMSBI」で、社内用アカウントの認証情報が盗まれ不正アクセス。利用者最大 58,510 人と、LINE の友だち最大 116,518 人の情報
- **何が起きたか**: ヒューマンアジャスト (TOKYO PRO Market など) は 11/13、利用するソニックムーブの外部クラウドサービス「COMSBI (SaaS 版)」で、同社の社内用アカウントの認証情報が第三者に不正に取得され、自社の情報が不正に取得されたとの報告を 11/11 に受けたと発表した。不正アクセスは 11/9 23:04 から 11/10 09:17 まで。対象は利用者最大 58,510 人 (氏名、電話番号、メールアドレス、住所、生年月日、性別のいずれか) と、LINE 公式アカウントの友だち最大 116,518 人 (表示名、プロフィール画像の URL、LINE ユーザー ID)。ソニックムーブは 11/10 に攻撃元の遮断、パスワード変更、強制ログアウトを済ませた。
- **なぜ重要か (評価)**: 前号の電通デジタル「TONARIWA」(11/11) に続き、LINE 連携のマーケティング SaaS で、運営側の管理アカウントの認証情報から顧客企業のデータに届いた。SaaS 事業者の「社内用アカウント」は全テナントを横断できることが多く、MFA と接続元の制限がないと 1 件の認証情報で全顧客に届く。COMSBI を使う他の企業の公表も続くとみられる。LINE 連携の SaaS を評価するときは、事業者側の管理者アカウントの MFA、テナントをまたぐ操作の監査ログ、チャネルアクセストークンの保管方法を、委託先の評価項目に入れたい。
- 出典: [ヒューマンアジャスト (2026-11-13, TDnet)](https://www.release.tdnet.info/inbs/140120261113579962.pdf)

#### [2026-11-12] 滋賀県甲賀市: 防災用の音声放送システムのサーバーがランサムウェア被害。市内 229 か所の屋外拡声器と各家庭の音声放送端末が使えず、緊急情報も停止
- **何が起きたか**: 甲賀市は 11/12、音声放送システムのサーバーがランサムウェア攻撃を受け、音声放送端末機と屋外拡声器が使えない状況だと発表した。端末の設置者の氏名または事業所名が漏えいした可能性があり、調査している。緊急情報、ページング放送 (区・自治会の連絡)、定時のメロディ放送、あいコムこうかの「おくやみ情報」も止まっている。復旧の見通しは立っていない。緊急情報は市の公式 LINE、緊急メール、テレビ、ラジオ、滋賀県防災アプリで伝える。両機器の管理を受託する第三セクターのケーブルテレビ事業者「あいコムこうか」も同日に公表した (ITmedia)。
- **なぜ重要か (評価)**: 個人情報の量は少ないが、防災の情報伝達という可用性そのものが止まった。防災行政無線や音声告知の設備は、IP 化で汎用のサーバーと VPN を使うようになったが、情報系のシステムと比べて更新や監視が手薄になりやすい。自治体と CATV 事業者の OT 寄りのシステムの診断では、保守用のリモート接続の経路と、バックアップの切り離しを確認したい。
- 出典: [甲賀市](https://www.city.koka.lg.jp/item/45076.htm) (ページに日付の表記なし。公表日は ITmedia の記事で確認) / [ITmedia NEWS (2026-11-13)](https://www.itmedia.co.jp/news/article/2611/13/2000003167/)

#### [2026-11-12] ユナイテッド・スーパーマーケット・ホールディングス「Scan&Go ignica」に不正アクセス。約 240 万アカウントのうち 64,003 件の氏名とメールアドレスを含むファイル / マクロミル: モニタ 317 人の情報を閲覧、うち 82 人は振込先口座
- **何が起きたか**:
  - USMH (マルエツ、カスミ、マックスバリュ関東) は 11/12、スマホのセルフレジアプリ「Scan&Go ignica」のシステムへの不正アクセスで、新規登録時に入力した氏名とメールアドレスを含むファイルが、侵入されたシステム内にあったと発表した。対象は約 240 万アカウントのうち 64,003 件。持ち出しは確認していないが、否定できないとしている。カード情報、住所、電話番号、生年月日は含まれない。
  - マクロミルは 11/12、モニタサイトの一部システムへの不正アクセス (10/29 確認) で、モニタ 317 人の基本情報と属性情報が外から閲覧された痕跡があり、うち 82 人はポイント交換先の振込先口座を含むと発表した。一部のアカウントでは、登録メールアドレスの書き換えとポイント交換の操作が試みられた痕跡があった (不正な交換の完了はない)。全モニタのポイント交換機能を止めている。別に、通知・認証に使うメール配信委託先の不正アクセス (10/31) でメールが届かない状態も続いている。
- **なぜ重要か (評価)**: マクロミルの件は、閲覧に続いてメールアドレスの書き換えとポイント交換が試みられており、情報の窃取ではなくアカウントの乗っ取りと換金を狙った攻撃だとわかる。ポイントサイトの診断では、連絡先の変更時の再認証と旧アドレスへの通知、交換先口座の変更後の待機期間を確認したい。USMH は、本番システム内に登録データのファイル (エクスポートや一時ファイル) が置かれていた点が、診断で見るべき箇所になる。
- 出典: [USMH (2026-11-12, PDF)](https://www.usmh.co.jp/wp-content/uploads/2026/11/us_20261112.pdf) / [マクロミル (2026-11-12)](https://www.macromill.com/press/info/20261112.html)

#### [2026-11-12〜13] [続報] 委託先経由の漏えいの波及: アララ (約 380 社、約 8,233 万件) の利用企業の公表が続く。Notion AI (Fireworks AI) の件ではワンキャリア、TimeTree、イオレ。まとまる EC 店長ではベガコーポレーション
- **前回から何が変わったか**:
  - **アララ「アララメッセージ」**: 11/12 に不二家 (公式ネットショップのメルマガ購読者、最大 149,892 件。GMO メイクショップ経由で 11/11 に報告を受けた)、キユーピーなど 5 社 (キャンペーン応募などの自動返信メールの受信者、計 125,788 件)、東京ガス (「ガス本管埋設状況確認サービス」の登録者 85,565 件)、百十四銀行 (株主優待の電子ギフトの当選者 1,500 件)、サンフレッチェ広島 (2,900 件) が公表した。11/13 には三井住友海上 (約 1.5 万件) とあいおいニッセイ同和損保 (約 1.6 万件) が、ドライブレコーダー映像の共有に使う「Fleekdrive」経由で、2026/7/1〜10/30 に配信メールを受けた顧客のメールアドレスが漏えいしたと公表した。両社の文書は、アララの「Web サーバーの脆弱性を第三者に悪用され」たと記している。近鉄・都ホテルズ (16 件) も 11/13 に公表した。不二家の文書では、アララ側の公表として「約 380 社、約 8,233 万件」を引いている。
  - **Notion AI のチャット記録 (Fireworks AI 経由)**: 11/12 にワンキャリア (サービス利用者などの個人情報、最大約 2,300 件) と TimeTree (協力者 13 人、取引先 5 人、役職員 81 人) が、11/13 にイオレ (最大 40 件。打ち合わせ内容、取引先担当者名など) が公表した。イオレの文書によれば、Notion は 11/3 に Fireworks AI との接続を解除し、同社の環境に保存されたデータを削除した。
  - **まとまる EC 店長 (ブランジスタソリューション)**: ベガコーポレーション (LOWYA) は 11/13、楽天、Yahoo!、Amazon の 6 店舗で最大 392 件の注文者・お届け先の情報が漏えいした可能性があると公表し、API 連携を解除した。
- **なぜ重要か (評価)**: 1 社の侵害から、数日おきに数十社の公表が続いている。メールアドレスだけの漏えいでも、「保険会社のドラレコ映像の共有」「ガス管の確認サービス」のような文脈と組み合わさると、本物らしい標的型フィッシングが作れる。委託先の棚卸しでは、直接の委託先 (Fleekdrive、GMO メイクショップ) のさらに先の再委託先 (アララ) まで、どのデータが渡っているかを把握しているかが問われている。
- 出典: [不二家 (2026-11-12, PDF)](https://www.fujiya-peko.co.jp/assets/pdf/release20261112_1.pdf) / [キユーピーなど 5 社 (2026-11-12)](https://www.aohata.co.jp/notices/20261112.html) / [東京ガス (2026-11-12)](https://www.tokyo-gas.co.jp/news/press/20261112-02.html) / [百十四銀行 (2026-11-12, PDF)](https://www.114bank.co.jp/important/pdf/imp20261112.pdf) / [三井住友海上 (2026-11-13, PDF)](https://www.ms-ins.com/news/fy2026/pdf/1113_1.pdf) / [あいおいニッセイ同和損保 (2026-11-13, PDF)](https://www.aioinissaydowa.co.jp/corporate/about/news/pdf/2026/news_2026111301533.pdf) / [近鉄・都ホテルズ (2026-11-13)](https://www.miyakohotels.ne.jp/topic/information/241/) / [ワンキャリア (2026-11-12)](https://onecareer.co.jp/news/information/261112/) / [TimeTree (2026-11-12)](https://timetreeapp.com/intl/ja/newsroom/2026-11-12/announce) / [イオレ (2026-11-13, TDnet)](https://www.release.tdnet.info/inbs/140120261113580244.pdf) / [ベガコーポレーション (2026-11-13, TDnet)](https://www.release.tdnet.info/inbs/140120261113577617.pdf)

#### [2026-11-13] [続報] GMO インターネット「お名前.com デスクトップクラウド」: FX 口座の損失補償の申請は 2,943 口座・約 29.98 億円。直接費用 30.5 億円に対し、サイバー保険の上限は 11 億円。サイバーセキュリティクラウドも GitHub の件の影響を業績予想に織り込む
- **前回から何が変わったか**:
  - GMO インターネットは 11/13 の決算説明会で、伊藤社長 (25%) ら役員 3 人の月額報酬を 3 か月減額すると発表した。FX 口座の不正取引による損失の補償の申請は、12 日時点で 2,943 口座・約 29 億 9,800 万円。見舞金 (一律 5,000 円) の申請は 10,976 件。直接費用は計 30.5 億円の見込みで、第 4 四半期に計上する。加入しているサイバー保険の上限は 11 億円で、上限まで受け取っても直接費用の 3 分の 1 程度にとどまる。サービス停止で、1 四半期あたり売上・利益とも約 3 億円減る見込み。
  - サイバーセキュリティクラウドは 11/13、通期の業績予想を下方修正した (売上高 60 億円→57 億円)。主因は組織変更による営業の遅れだが、11/12 開示の GitHub の認証情報流出の件の影響も「合理的に見積もり可能な範囲」で織り込んだとしている。
- **なぜ重要か (評価)**: 侵害の金額が、補償、保険の上限、役員報酬という形で具体的に示された。経営層に診断やペンテストの予算を説明するときに、「サイバー保険で賄えるのは直接費用の約 3 分の 1」という国内の実例として使える。
- 出典: [ITmedia NEWS (2026-11-13)](https://www.itmedia.co.jp/news/article/2611/13/2000003197/) / [サイバーセキュリティクラウド (2026-11-13, TDnet)](https://www.release.tdnet.info/inbs/140120261113579575.pdf)

> ほかに 11/12 公表で本文に入れなかったもの: 栃木県のサイクルツーリズムのサイト「ぐるとち」の改ざん (偽サイトも確認。個人情報は持っていない)、若尾綜合舞台 (社内サーバーへの不正アクセス、範囲は調査中)、北九州市 (teket 経由、117 人。teket の件は既報)、バルス (SPWN) とウェザーニューズ (オープンロジ経由。件数はオープンロジが調査中)。

### 国内の注意喚起・ガイドライン・政策

#### [2026-11-13] Microsoft 365 の大規模障害 (Exchange Online を起点に 20 サービス): 政府共通の業務環境 GSS にも影響。総務省は自治体に、メールだけの窓口に代わる手段の確保を依頼。経産省は入札・公募の締め切り延長に動く
- **何が起きたか**: 11/13 未明 (EX1550543 の開始は 01:17 JST) から、Exchange Online のメールボックスに接続できない障害が起き、Teams、SharePoint、Defender XDR、Intune、Purview など 20 サービスの Exchange 連携機能に広がった。古川デジタル相は 11/13 の会見で、デジタル庁が整備する政府共通の業務環境「GSS」でも Outlook のメール送受信ができなくなっていると述べ、電話やチャットなどの代替手段で主要な業務は続けているとした。総務省は 11/13、自治体に対し、受付・相談窓口がメールだけの場合は電話などの代わりの手段を確保して住民に周知すること、手続きで申請者が不利益を受けないよう対応方針を公表することを依頼した (担当は自治行政局住民制度課サイバーセキュリティ対策室)。経産省は、11/13 未明以降に送られたメールが届いていない可能性があるとして電話での連絡を求め、契約・補助金の入札・公募で締め切りの延長や代わりの提出方法の確保を進めると告知した。Microsoft は悪意のある活動の兆候はないとしている (piyolog のまとめ)。
- **なぜ重要か (評価)**: 攻撃ではないが、Defender XDR と Purview も影響の一覧に入った。メールの保護や監査ログの取り込みが止まった時間帯は、検知の空白になる。単一の SaaS への依存が行政手続きの期限にまで及ぶことを、政府自身が示した。BCP の評価では、メール以外の連絡手段と、SaaS の停止中のセキュリティ監視の代替を確認したい。
- 出典: [総務省 (2026-11-13)](https://www.soumu.go.jp/menu_kyotsuu/important/kinkyu02_000685.html) / [経済産業省 (2026-11-13)](https://www.meti.go.jp/press/2026/11/20261113005.html) / [ITmedia NEWS (2026-11-13)](https://www.itmedia.co.jp/news/article/2611/13/2000003183/) / [piyolog (2026-11-13)](https://piyolog.hatenadiary.jp/entry/2026/11/13/114230)

#### [2026-11-12] 警察庁「サイバー警察局便り R8 Vol.21: 基本的な対策の徹底を」。相次ぐ不正アクセスは「基本的な対策が不十分だった」例を複数確認
- **何が起きたか**: 警察庁サイバー警察局は 11/12、事業者と個人向けのリーフレットを公開した。最近の不正アクセス事案では基本的な対策が不十分だったとみられる例を複数確認しており、事業規模を問わず幅広い事業者が標的になっていると指摘した。事業者には NCO の 11/5 の注意喚起 (運用・管理段階、設計・開発段階、サプライチェーンを通じた侵害への対策) を参照して対策を徹底するよう求め、個人にはパスワードの変更と使い回しの禁止、パスキーなど多要素認証の活用、カード会社への連絡、メールや SMS のリンクを安易に開かないことを呼びかけている。
- **なぜ重要か (評価)**: 内容は NCO の 11/5 の注意喚起と同じだが、警察庁も「原因は高度な攻撃ではなく基本的な対策の不備」とする見方をそろえた。委託先の SaaS (アララ、オープンロジ、COMSBI、KARTE など) の侵害が続く現状で、顧客に「基本対策の棚卸し」としての診断を提案する根拠として使える。
- 出典: [警察庁 サイバー警察局便り R8 Vol.21 (2026-11-12, PDF)](https://www.npa.go.jp/bureau/cyber/pdf/R8_Vol.21cpal.pdf)

#### [2026-11-13] IPA「AI セキュリティ短信 2026 年 11 月号」: 10 月の AI 関連のセキュリティ動向を約 40 項目に整理。「AI エージェント型の攻撃基盤が多様な脅威アクターに広がる」
- **何が起きたか**: IPA は 11/13、AI セキュリティ短信の 11 月号 (PDF) を公開した。エグゼクティブサマリーは、(1) AI エージェント型の攻撃基盤の利用が多様な脅威アクターに広がる、(2) AI の開発ツールと実行基盤が侵害と認証情報窃取の標的に、(3) AI による脆弱性発見が量産段階に入り、検証と修正の能力が問われる、(4) OS やブラウザが AI による防御とエージェントの統制を既定に、(5) 評価中の AI の逸脱への対応が接続の遮断と監視の強化へ、の 5 点。個別項目には、ARTEX による韓国の金融機関からのデータ窃取、Storm-0940 による ConnectWise 起点の侵害、LiteLLM のリリース工程の侵害、PHP2Shell の連鎖による PAN-OS の侵害、「国内の不正アクセス多発、一部で AI エージェントの関与を確認」などが入っている。
- **なぜ重要か (評価)**: 公的機関が、AI ペンテストツール (ARTEX、Cairn) の悪用と AI の開発基盤の侵害を、10 月の主要な脅威として日本語でまとめた。顧客向けの報告書で、AI エージェントの攻撃による「探索の網羅性と速度の変化」を説明するときの引用元に使える。
- 出典: [IPA AI セキュリティ短信 (2026-11-13)](https://www.ipa.go.jp/digital/ai/security/ai-security-bulletin.html)

#### [2026-11-13 告知] 総務省「フロンティア AI 時代の通信事業におけるデータの保護・セキュリティの在り方に関する検討会」第 2 回を 11/19 に開催 (事業者ヒアリング)
- **何が起きたか**: 総務省は 11/13、同検討会の第 2 回を 11/19 17:00 から Web 会議で開くと告知した。議題は事業者ヒアリングなど。同省は 11/6 にドコモに行政指導をしており (既報)、通信事業者が持つ利用者情報の保護と、AI の活用の両面を検討している。
- **なぜ重要か (評価)**: 通信事業者の AI 活用 (通信の秘密、位置情報) に関わるセキュリティの要件が、今後ガイドラインになる可能性がある。通信事業者を顧客に持つ場合は、11/19 の配布資料を確認したい。
- 出典: [総務省 (2026-11-13)](https://www.soumu.go.jp/main_sosiki/kenkyu/data_protection/02kiban18_02000516.html)

> 11/12〜14 に、NCO (新着 CSV の最新は 11/10)、IPA の「重要なセキュリティ情報」(最新は 11/11 の MS 更新)、JPCERT/CC の注意喚起 (最新は 11/11)、金融庁、個人情報保護委員会、JC3 から、新しいサイバー関連の発表は確認できなかった。

### 国内製品の脆弱性 (JVN)

> 11/12〜13 に JVN で新しく公開された国内ベンダー独自の案件 (JVN#) は、11/12 の Airターミナル6 (前号で既報) だけだった。11/13 の JVN# は海外製品 (JetBrains YouTrack) だが、国内の研究者 (MBSD) の届出による。以下は 11/13 の JVN の公開分と、JVN iPedia の 11/13 の登録分から、国内で使われる製品を選んだ。

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| 2026-11-13 | JVN#76799957 / CVE-2026-75048 | YouTrack 2026.2.18068 より前 / JetBrains | コードブロックの言語ラベル経由の格納型 XSS。MBSD の赤木悠祐氏が IPA に届け出た (開発者の内部調査でも発見・修正済み) | v4 4.8 / v3 5.4 (PR:L、UI:R) | [JVN](https://jvn.jp/jp/JVN76799957/) |
| 2026-11-13 | JVNVU#95718857 / VU#580079「ImageTragick2」(3 件。CVE-2026-65640 ほか) | ImageMagick 7.1.1.43 以前と、それを使うアプリ (Ruby on Rails、WordPress、MediaWiki、ownCloud Classic、Redmine など) | 既定のセキュリティポリシーが危険なコーダーを制限せず、細工した SVG / PostScript で任意のファイルを読み書き。連鎖で RCE のおそれ | 任意ファイル読み書き → RCE (CVSS は未記載) | [JVN](https://jvn.jp/vu/JVNVU95718857/) / [CERT/CC](https://kb.cert.org/vuls/id/580079) |
| 2026-11-13 | JVNVU#99429639 / CVE-2026-123790 | ComfyUI-Easy-Use 1.4.1 以前 (ComfyUI 拡張) | 未認証で `save_preview()` のパストラバーサル。入力ディレクトリに置いた Python ファイルでカスタムノードの `__init__.py` を上書きし、再起動時に実行 | 未認証 RCE (ネットワークから届く場合) | [JVN](https://jvn.jp/vu/JVNVU99429639/) / [CERT/CC](https://kb.cert.org/vuls/id/944667) |
| 2026-11-13 | JVNVU#92656681 / CVE-2026-128321 | TightVNC Windows Viewer 1.3.10、UltraVNC Windows Viewer | 悪意のある VNC サーバーが幅 8,257 px 以上の Tight JPEG 矩形を送ると、ビューアーでヒープ書き込み | DoS は実証、任意コード実行のおそれ | [JVN](https://jvn.jp/vu/JVNVU92656681/) / [CERT/CC](https://kb.cert.org/vuls/id/644655) |
| 2026-11-13 | JVNVU#98641453 / CVE-2026-127109 | promzard 4.0.0 以前 (npm) | コンテキストオブジェクトのキーを関数の引数リストに文字列で埋め込み、`vm.runInThisContext()` で評価 | キーを操作できる場合は RCE | [JVN](https://jvn.jp/vu/JVNVU98641453/) / [CERT/CC](https://kb.cert.org/vuls/id/685399) |
| 2026-11-13 | JVNDB-2026-043325 / CVE-2026-113373 (ほか JVNDB-2026-043326 / CVE-2026-113368) | Sonatype Nexus Repository 3 Pro | SAML / OIDC でのサインイン時にローカルアカウントの無効・ロック状態を確認せず、無効化したユーザーがそのロールで再びログインできる。ほかにグループリポジトリ経由で閲覧権限のないリポジトリを読める件 (5.4) | v3 8.1 | [JVN iPedia](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-043325.html) |
| 2026-11-13 | JVNDB-2026-043322 / CVE-2026-116650、JVNDB-2026-043321 / CVE-2026-116651 | Tanium Threat Response | 認証済みユーザーによる OS コマンドインジェクション (ほかに Enforce のアクセス制御の不備 6.5 など) | v3 8.8 | [JVN iPedia](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-043322.html) |
| 2026-11-13 | JVNDB-2026-043341〜043347、043330〜043332 / CVE-2026-105612〜105620、CVE-2026-110181〜110183 | PostgreSQL Anonymizer 3.3.0 未満 / Dalibo | マスキングの回避が多数: security_invoker ビュー、親テーブル経由、ルール内のサブクエリ、プリペアドプランの再利用、pg_stats のヒストグラムなど | v3 最大 6.5 (C:H) | [JVN iPedia](https://jvndb.jvn.jp/ja/contents/2026/JVNDB-2026-043342.html) |
| 2026-11-13 | JVNVU#90821966 | CISA ICS Advisory (11/12 分): Siemens 5 件 (Building Automation、Desigo / Gridscale、Industrial Edge Management、RUGGEDCOM APE1808 ×2) と Hitachi Energy RTU500 (Update A) | CISA の ICS アドバイザリの国内向けの転載 | 各アドバイザリを参照 | [JVN](https://jvn.jp/vu/JVNVU90821966/) |

- 所感 (評価): ペンテストで優先したいのは 3 件。(1) ImageTragick2: 画像のアップロード機能がある Web アプリ (Redmine、WordPress、Rails の Active Storage) では、ImageMagick を更新しても `policy.xml` が緩いままなら残るので、SVG / PS / MVG / MSL の拒否を実際に試して確かめたい。(2) ComfyUI-Easy-Use: 社内の生成 AI 検証環境で、認証なしで ComfyUI を公開している例は多い。外部・内部の診断で 8188/tcp の公開を確認したい。(3) Nexus の SSO 時のロック回避: 退職者のアカウントを「ロックしただけ」で運用している組織では、IdP 側の無効化と突き合わせる必要がある。

### 国内コミュニティ・研究・イベント

#### [2026-11-13] piyolog「良品計画への不正アクセスについてまとめてみた」: 2 系統の攻撃 (システムの脆弱性経由と、ネットストアへのリスト型攻撃) と、①〜④ の区分ごとの件数・項目を整理
- **何が起きたか**: piyolog は 11/13、10/30 の第一報から 11/12 の会見までの良品計画の公表を整理した。10/29 01 時ごろの不正アクセスの発生 (クレディセゾンの公表)、11/1 深夜のネットストアへの不正アクセスの検知、11/4 までの遮断という経過と、区分ごとの件数 (① 約 2,726 万件、うち氏名・住所などを含むもの約 75 万件、購入履歴まで約 27 万件、② MUJI Card の番号の全桁 約 109 万件 [有効カードは約 34.5 万件]、③ 登録カードの一部 約 120 件、④ 代引きの受取先 約 44 万件) を一覧にした。当初「単一の攻撃」と想定して営業を続けたこと、リスト型攻撃が広範な IP から長期間「ゆるゆる」と続き検知が難しかったという会見での説明も記録している。
- **なぜ重要か (評価)**: 公表のたびに範囲が広がった経過を、1 本の時系列で追える。「最初に見つけた侵入口を塞いで営業を続ける」判断がなぜ失敗したかを示す、インシデント対応の演習の教材として使える。
- 出典: [piyolog (2026-11-13)](https://piyolog.hatenadiary.jp/entry/2026/11/13/162738)

#### [2026-11-13] LAC WATCH「検出から修復まで、脆弱性対応を加速する ～フロンティア AI 時代の脆弱性管理 (4)」
- **何が起きたか**: ラックは 11/13、連載の第 4 回として、脆弱性の情報収集、影響を受ける資産の特定、優先順位付け、パッチの適用や暫定対策を、高速化・自動化する手法と導入時の注意点を、脆弱性マネジメントグループが解説した。前提として、フロンティア AI の時代には、攻撃者が脆弱性を見つけて悪用するまでの時間が短くなると想定している。
- **なぜ重要か (評価)**: 国内のベンダーが、Mythos 級のモデルによる脆弱性発見の量産を前提に、運用の手順を組み直す提案を始めている。診断の結果を顧客の脆弱性管理の流れにどう渡すか (チケット化、優先度の付け方) を考える参考になる。
- 出典: [LAC WATCH (2026-11-13)](https://www.lac.co.jp/lacwatch/service/20261113_005018.html)

#### [2026-11-13] Zenn: GitHub Actions のシークレット窃取 (「docs: dependency audit notes」の PR) を、Actions の実行番号の欠番から確かめる手順 / サイバーセキュリティクラウドの社員による ARTEX・AntiFox の悪用と AWS の対策のまとめ
- **何が起きたか**: Zenn に 11/13、Aikido Security の調査 (11/12) をもとに、自分のリポジトリが wfx-loot の被害を受けたかを確かめる日本語の手順が投稿された。探索用の PR は 1 分以内に本体を戻され、実行ログも消されるため、確かな痕跡は「ワークフローごとの実行番号の欠番」だとして、11/10 以降の欠番を PR やコミットと照らす方法を示している。同じ日に、サイバーセキュリティクラウドの CloudFastener の担当者が、AI ペンテストツール ARTEX と派生の AntiFox の悪用レポートを読み比べ、「突かれたのは新しい脆弱性ではなく、漏えいした認証情報や広すぎる権限」と整理し、AWS 利用者の対策を 3 点にまとめた (同社は前日に自社の GitHub の認証情報流出を公表している)。
- **なぜ重要か (評価)**: wfx-loot は前号で扱ったが、ログが消される攻撃の調べ方 (実行番号の欠番) は、インシデント対応の実務にそのまま使える。CI の侵害の調査では、監査ログの保存期間が短い問題 (CSC の件) と合わせて、実行番号の連続性も確認項目に加えたい。
- 出典: [Zenn masafumi_ai (2026-11-13)](https://zenn.dev/masafumi_ai/articles/00015-github-actions-secret-theft) / [Zenn cscloud_blog (2026-11-13)](https://zenn.dev/cscloud_blog/articles/ai-pentest-tools-abuse-aws-defense)

> イベント: CODE BLUE 2026 は 11/17 (火)〜18 (水) に開かれる。通常チケットの販売は終わり、会期中は当日券を販売する (11/11 告知。採用範囲の外なので参考)。SECCON と AVTOKYO は、11/12〜14 の新しい告知を確認できなかった。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 110 (AI 約 35 / セキュリティニュース 約 25 / CVE データ 6 [NVD API 2.0、OSV、EPSS、CISA KEV JSON、CERT/CC API、cveawg] / 国内 約 45)。調査は 4 つのサブエージェントに分けて並行で行い、curl で取得した。
- 採用件数: AI技術=10 / AIセキュリティ=8 / セキュリティ=14 (+短信 3) / CVE=12 行 (ID は計 20 超) / 国内インシデント=9 / 国内政策=4 / JVN=9 / 国内コミュニティ=3
- 除外理由内訳: 古すぎ=約 50 (AI: OpenAI Cogent・Gemini 4 Carbon [11/10]、Claude / Codex の「Reverse Engineer Anything」の締め付け [元の報道 11/10]、Google の社内のコーディング AI「GfG」の ITmedia の紹介 [論文は 10 月]、@IT の講演記事 [11/4] など。セキュリティ: Krebs の Qilin、Unit 42 の Falcon、MS の GSocket [いずれも 11/11]。国内: ScanNetSecurity の 11/13 掲載のうち 10/30〜11/7 公表分、セキュリコの 11/11 公表分など) / 重複=約 60 (N-central、Apache httpd、SignDrop、Red Hat Quay、Citrix、PostgreSQL、Node.js、MongoDB、Gemini 4 Hydrogen、Cairn、Silent Lynx、SMBC 日興証券、オープンロジ、Airターミナル6 など) / 日付不明=約 7 (THN の ThreatsDay の個別項目 [Unit 42 の GEO のインジェクション、Sekoia の Flowise、RevStealer など]、Dark Reading の本文が取れない 3 件)
- 取得失敗ソース:
  - github.com の HTML と api.github.com (403)。修正コミットの URL は NVD の参照と OSV から取り、diff の中身は直接開いていない。OpenBao、NocoDB、Algernon、Payara、Check Point、TightVNC、vsomeip は advisory の URL で代用 (commit 不明)
  - openai.com の記事ページ (Cloudflare)。RSS の日付と TechCrunch / SecurityWeek / Help Net Security で代用
  - Dark Reading (403)、Google TI / Mandiant の RSS (HTML が返る。代用なし)、CISA の advisories の RSS (XML の破損。KEV の JSON で代用)、Check Point sk1000362 (JavaScript で描画。報道の引用で代用)
  - HiddenLayer / Lakera の feed (404)、ITmedia AI+ の RSS (別の一覧が返る。ITmedia NEWS と @IT で代用)
  - Qoo10 の告知 (HTTP 523。ITmedia で代用)、甲賀市のページ (日付表記なし。ITmedia で公表日を確認)、NCO のトップ (JavaScript。新着 CSV で代用)、IPA の RSS (新着ページの HTML で代用)
- 備考:
  - CISA KEV は catalogVersion 2026.11.13 (計 1,781 件)。11/11 以降の追加は 11/13 の 2 件 (CVE-2026-123039 Check Point、CVE-2026-114713 UnrealIRCd)。いずれも期限は 11/16。
  - 表の CVE で EPSS ≥ 0.5 のものはない。
  - 11/14 付の国内の公表は、調査時点 (05:15 JST ごろ) ではまだ出ていなかった。KARTE は調査中のため、件数や経路の続報に注意。

</details>
