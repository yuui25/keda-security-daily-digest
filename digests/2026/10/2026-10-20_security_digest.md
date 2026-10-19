# KEDA Daily Digest — 2026-10-20 (JST)

> 採用範囲: 公開日 2026-10-18 〜 2026-10-20
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

週明けの月曜 (10/19) は、国内で大規模な漏えいの公表が相次ぎ、海外では「AI エージェントが攻撃を最初から最後まで動かす」事例が複数の一次情報から同時に出た。
AI 側では、NVIDIA のオープンウェイトモデル Nemotron 3.5 Super VL (120B) と、AWS の TorchNeuron (PyTorch を Trainium に移す) が目立つ。研究では、コーディングエージェントに危険な allow ルールを承認させる攻撃 (Claude Code / Codex CLI で 58% 成功)、モデルの重みに埋め込んで DNS だけで秘密を持ち出す Model-as-a-Trojan、MCP ゲートウェイの比較ベンチマーク GatewayBench が出た。
AI セキュリティでは、OSS のエージェント基盤「Cairn」を使った 1 人の攻撃者が日本企業を含む 100 超のサイトに侵入した件 (Norforge / Reuters) と、Wiz の「AI 主導のクラウド侵害」の分析が並んだ。国内でも GMO イエラエが、日本企業を狙う攻撃で中国の開発者による自律型ペンテストツール「ARTEX」が使われていたと確認しており、攻撃の自動化は国内外で同時に裏付けられた。Envoy AI Gateway の MCP セッション乗っ取りなど、AI 系の GHSA も 3 件ある。
セキュリティ側の最重要は、Plex Media Server の未認証 RCE チェーン「Plex2Shell」である。PoC 公開の翌日に悪用が観測された。ほかに Siemens Software Center の DLL 欠陥の ClickFix での悪用、Rapid7 による NetScaler 侵害の詳細分析、Eptura Archibus の認証回避が出た。CVE では Apache Camel の一斉公開 (AS2 の SSRF、netty-http の大文字小文字による認可回避など) と、Camunda 7 の JUEL インジェクションが目立つ。KEV の追加は 10/16 以降ない。
国内では、ユミルリンクのメール配信 ASP「Cuenote FC」(延べ約 900 万件)、H2O リテイリングの「H2O ID」(約 126 万件)、ニフティ (最大 54 万件)、クリプトン (最大約 42 万件) と、大規模な漏えいの公表が 1 日に集中した。ふるさとチョイスと JFA Passport も停止している。アルカディア (SpeeCAN RAIDEN) は、侵入の時系列を分単位で公表した。
**今日まず見るべきは 2 件。** (1) 自社や顧客の環境、在宅勤務者の LAN にある Plex Media Server の版を確認する (深掘りを参照)。(2) Cuenote FC と H2O ID の件は、利用企業や会員として影響を受けていないかを確かめる。委託先経由の漏えいは、今後も利用企業による公表が続くとみられる。

## 今日の深掘り

### Plex Media Server の未認証 RCE チェーン「Plex2Shell」(CVE-2026-96652 / -96654 / -96655 / -96656) — PoC 公開の翌日に悪用が始まる

**概要 (事実)**
- 研究者 Zach Main 氏は 10/16、Plex Media Server (PMS) の 4 件の CVE を連鎖させて**未認証で RCE** に至る経路を詳しく解説し、PoC を GitHub で公開した。修正版は 1.43.3.10861 で、8/3 に公開されている。Plex は 9/1 の時点で、詳細を伏せたまま更新を呼びかけていた。
- 翌 10/17、boredhackerblog 氏が脆弱な版の PMS で運用するハニーポットで実際の悪用を観測した。攻撃者は公開 PoC (改変の可能性あり) を使い、XMRig ベースのマイナー `mylovelyminer` と、Linux 用のプロキシ兼バックドア `myawesomeproxy` を置いた。攻撃元は 45.194.92.222、ペイロードの配布元は 217.60.194.116。SecurityWeek と The Hacker News も 10/18〜19 に報じており、Reddit にも被害の報告が出ている。

**技術的な中身 (発見者の write-up による)**
1. **未認証 SSRF (CVE-2026-96652)**: companion プロトコルの `/player/timeline` は、WAN からのリクエストに `X-Plex-Token` が「付いているか」しか見ず、値が正しいかを確かめない (`junk` でも通る)。player 登録時の `protocol` パラメーターが callback URL にそのまま埋め込まれるため、unsubscribe のときに PMS 自身が `http://127.0.0.1:32400/...` へ POST する。
2. **loopback の信頼の悪用 (CVE-2026-96654)**: loopback から来たリクエストでは、`/system/agents/*` にトークンなしで入れる。`searchOne` の `identifier=` に値を差し込むと、`com.plexapp.agents.thetvdb/function/GetResultFromNetwork?url=...` のように任意のプラグイン関数を呼べる。
3. **所有者トークンの流出**: プラグイン基盤は、URL が `http://127.0.0.1` で「始まる」外向きリクエストに所有者の管理トークンを自動で付ける。前方一致で判定しているため、`127.0.0.1.<攻撃者IP>.sslip.io` を指定すると、トークンが攻撃者のサーバーに届く。
4. **ファイル書き込みから RCE へ (CVE-2026-96655 / -96656)**: 所有者トークンで `PUT /:/prefs` を送り、`TranscoderH264Options` に `dump-yuv=<Codecs ディレクトリ>/x.so` を設定する。続けて攻撃者の用意した動画をトランスコードさせると、x264 が無劣化で復号したフレーム (中身は ELF) をそのまま書き出す。次のトランスコードで、libavutil が Codecs ディレクトリの `*.so` を署名も確かめずに `dlopen` し、`plex` ユーザーの権限でコードが動く。
- 各 CVE の CVSS は 5.3〜8.6 で、単体で見れば中程度の不具合である。それを 4 段つなぐと、未認証 RCE になる。

**背景・経緯 (過去事例の引用)**
- CVE-2020-5741 (Plex の Camera Upload 経由の Python デシリアライズ RCE) は、2022 年の LastPass 侵害の侵入口になった。DevOps エンジニアの自宅の Plex がこの脆弱性で乗っ取られ、キーロガーから会社の保管庫に到達された。CISA は 2023-03 にこれを KEV に追加している。「自宅のメディアサーバーから企業に入られる」実例である。
- 2020 年には、Plex の GDM/SSDP (UDP/32410-32414) が DDoS の増幅に使われた (Netscout の報告)。
- 今回のマイナーの接続先 `ota.proxystream[.]st` と同じドメインのサブドメインを、Bitsight が 8 月に AISURU (DDoS とプロキシウェアのボットネット) と関連付けている。

**なぜ今これが重要か (評価)**
- 「PoC 公開から悪用まで 1 日」の典型例で、修正版から 2 か月半たってもパッチを当てていない PMS が狙われている。住宅回線の IP をプロキシとして転売する目的とみられ、侵害された家庭の回線が、企業の VPN やメールへの不正ログインの中継に使われるおそれがある。
- バリアントハントの題材としても良い。「トークンが付いているかだけを見る検査」「loopback の信頼」「`127.0.0.1` の前方一致による URL 判定」「設定値経由のファイル書き込み」は、どれも他のメディアサーバー (Jellyfin、Emby) や自前の Web 管理 UI で同じ形のまま探せる。
- 在宅勤務の端末と同じ LAN にある PMS は、企業のアタックサーフェス管理 (ASM) の範囲外になりやすい。

**読者が今日できること**
- 版の確認: `curl -s http://<host>:32400/identity` の `version` が 1.43.3.10861 未満なら即時更新する。トークンがなくても version は返る。Shodan や Censys の `port:32400 "Plex"` で、顧客や自社で外部に出ているものを棚卸しする。
- ログの確認: PMS のログやリバースプロキシのログで、`/player/timeline/subscribe` の `protocol=` に `127.0.0.1` を含むもの、`sslip.io` / `nip.io` を含む URL、`PUT /:/prefs` での `TranscoderH264Options` の変更、UA `Python-urllib` を探す。
- ホストの確認: `Codecs/` 配下に `lib` で始まらない `.so` や最近作られたファイルがないか、`Preferences.xml` に `dump-yuv` が残っていないか、`mylovelyminer` / `myawesomeproxy` のプロセスや `*.proxystream.st` への通信がないかを見る。侵害が疑われるなら、Plex アカウントのトークンを無効化し、同居するホストの資格情報もローテーションする。発見者は検知ルール (`github.com/code-zm/plex2shell/tree/main/detection`) を公開している。

出典: [boredhackerblog (悪用観測、10/17)](https://www.boredhackerblog.info/2026/10/plex-vulnerabilities-being-exploited-in.html) / [zmain (write-up)](https://zmain.info/blog/plex2shell) / [SecurityWeek](https://www.securityweek.com/plex2shell-exploit-chain-weaponized-against-plex-servers-hours-after-disclosure/) / [The Hacker News](https://thehackernews.com/2026/10/hackers-exploit-plex2shell-flaws-to.html)

## AI 技術・トレンド

### [2026-10-20] NVIDIA、企業のエージェント向けオープンウェイトモデル「Nemotron 3.5 Super VL」(120B) を公開
- **何が起きたか**: NVIDIA が Nemotron 3.5 系として、Super VL (120B、即日提供)、ローカルのエージェント向けの Bolt 74B-A9B 24GB (即日提供、10/16 既報)、会話エージェント向けの Bolt E4B (今月中) を発表した。NVIDIA によると、Super VL は Nemotron 3 Ultra より小さいが、指示追従とツール使用で同等の精度を出す。特定のタスクで追加学習すると Opus 5 や GPT-6.1 Sol より速く終わるとも主張しているが、数値は示していない。採用企業として CrowdStrike、Perplexity、Salesforce などの名前を挙げている。
- **なぜ重要か**: セキュリティベンダーを含む企業が、自社で動かすオープンウェイトモデルをエージェントの中核に据え始めている。重みの入手経路とエージェントの権限設計が、診断の対象として増えていく。
- 出典: [TechCrunch](https://techcrunch.com/2026/10/19/nvidia-launches-new-open-models-to-run-agents-in-the-enterprise-and-on-pcs/)

### [2026-10-20] AWS、PyTorch アプリを Trainium に移す「TorchNeuron」を公開。「設定 1 行で移行」と主張
- **何が起きたか**: Amazon によると、TorchNeuron を使えば、コードを書き換えずに設定 1 行の変更で PyTorch アプリを Trainium に移せる。チップ固有の依存をなくすコードは PyTorch 本体に還元すると表明した。Hugging Face も、HF のモデルを Trainium で動かす手順をブログで公開した。AWS は事例として、Deepgram の音声処理量がドル当たり 70% 増えたと説明している。
- **なぜ重要か**: CUDA への依存を崩す試みで、推論や学習の基盤が NVIDIA 以外にも広がる。ドライバ、ランタイム、コンパイラといった新しいソフトウェア層が、そのまま攻撃面と供給網の確認ポイントになる。
- 出典: [TechCrunch](https://techcrunch.com/2026/10/19/amazon-is-taking-its-biggest-shot-at-nvidia-yet-with-new-torchneuron-dev-tool/) / [Hugging Face](https://huggingface.co/blog/hf-torchneuron)

### [2026-10-20] 推論チップの Tenstorrent が 15 億ドルを調達し、評価額は 62 億ドル
- **何が起きたか**: Trace Capital と Innovation X が主導した。評価額は 2024 年末の 26 億ドルから 2 倍超になった。Jim Keller CEO は、自社の Galaxy サーバーで DeepSeek のモデルが動くことが追加調達のきっかけになったと述べた。報道によると、Intel と Qualcomm から最大 50 億ドルで買収の打診があったが、独立を選んだ。
- **なぜ重要か**: 中国系を含むオープンウェイトモデルを自社のハードウェアで動かす流れに、資金が集まっている。
- 出典: [TechCrunch](https://techcrunch.com/2026/10/19/tenstorrent-hits-6-2b-valuation-to-scale-open-weight-ai-chips/)

### [2026-10-19] Microsoft、英国最大の AI データセンター計画 (Nscale、エセックス州ラフトン) から撤退
- **何が起きたか**: BBC によると、Microsoft はラフトンの施設にスーパーコンピューターを出資する計画への関与を打ち切った。Microsoft はコメントしていない。Telegraph によると、年末の予定だった受電は 2030 年代にずれ込む。Nscale は「ロンドン全域の送電網の問題」と説明し、計画は続けるとしている。
- **なぜ重要か**: AI の計算資源を増やす際の制約が、電力と送電網になっていることを示す事例。
- 出典: [BBC](https://www.bbc.com/news/articles/c9m26kl5y7epo)

### [2026-10-19] Microsoft Security、「Project Perception」の対象を社内エージェントの統制 (agentic insider) に広げる方針
- **何が起きたか**: Microsoft Security の EVP、Hayete Gallot 氏が公式ブログで方針を示した。外部からの AI 攻撃に対する防御基盤 Project Perception (7 月発表) を、社内で動くエージェントの管理にも使う。エージェントごとに ID、コンテナ、ポリシーを割り当ててリスクを動的に評価し、「Guardian Agents」がリアルタイムで監視する。今後の方向性として、モデルの推論内容 (CoT) を見て意図が目的と合っているかを判定する「model transparency」を挙げたが、製品化の時期は示していない。
- **なぜ重要か**: エージェントを「内部不正者」のモデルで扱う考え方が、大手ベンダーの公式な方針になった。エージェントの隔離と権限設計が、今後診断で確認する項目として定着していく。
- 出典: [Microsoft](https://blogs.microsoft.com/blog/2026/10/19/securing-the-agentic-insider/)

### [2026-10-19] MCP ゲートウェイの比較ベンチマーク「GatewayBench」: 実在する MCP サーバー 251 個のツール 11,118 種で 7 製品を評価 (arXiv 2610.23449)
- **何が起きたか**: 研究者がゲートウェイの構成を「フラット型」と「階層型」に分類し、6 分野・524 タスクで評価した。無関係なツールを注入して露出するツールの数を増やしながら、タスクの達成度、効率、攻撃への耐性を測った。広く使われている 7 つのゲートウェイで、設計ごとに大きな差が出た。その差は、組み合わせるモデルやハーネスでも変わる。同じ日に、MCP の型付きツール呼び出しで権限を偽装する「Structured Authority Injection」(arXiv 2610.22373) も公開された。
- **なぜ重要か**: MCP ゲートウェイを選ぶときや診断するときの比較の軸 (露出ツール数と攻撃への耐性の関係) が示された。
- 出典: [arXiv 2610.23449](https://arxiv.org/abs/2610.23449) / [arXiv 2610.22373](https://arxiv.org/abs/2610.22373)

### [2026-10-19] (国内) 世田谷区、Azure OpenAI や Copilot が定着しなかったため、エージェント型ツール「Genspark」を検証。約 2,900 時間を削減
- **何が起きたか**: 世田谷区は Azure OpenAI Service で独自の AI 環境を作り、Microsoft Copilot も導入していたが、職員ごとに利用のばらつきが大きかった。そこで Genspark を導入し、他の自治体の計画の調査や論点整理、資料・チラシの作成に使っている。見出しでは約 2,900 時間の削減とされ、課題として AI の出力を確認・修正する負担が増えたことを挙げている。記事のもとは 8 月の「AI 博覧会」のセッション。
- **なぜ重要か**: 自治体が外部の SaaS エージェントに庁内文書を読み込ませて使い始めている。データの扱い、テナントの分離、出力の検証というガバナンスの論点が、現場で表に出てきた事例。
- 出典: [ITmedia ビジネスオンライン](https://www.itmedia.co.jp/business/articles/2610/19/news064.html)

### [2026-10-19] (国内) 三菱電機、CEATEC 2026 でフィジカル AI を展示。プロンプトで指定した音を取り出す「TUSS」が総務大臣賞
- **何が起きたか**: TUSS (タスク汎用音源分離技術) は 1 つのモデルで、混ざった音からプロンプトで指定した音を取り出す。ローカル PC でリアルタイムに動く。デモでは災害現場の音から人の声を取り出し、CEATEC AWARD 2026 の総務大臣賞を受けた。ほかに、0.1mm の精度で位置合わせするネジ締めロボットや、遠隔操作で教え直せる棚出しロボット (CP Robotics と共同) を展示した。製品化の時期は示していない。
- **なぜ重要か**: 国内製造業のフィジカル AI が実証段階に入っている。AI を組み込んだ OT やロボットと、その遠隔操作の経路は、OT セキュリティ診断の対象を広げる。
- 出典: [INTERNET Watch](https://internet.watch.impress.co.jp/docs/event/2149065.html)

### [2026-10-19] (参考) 米民主党、中間選挙後に AI 規制の強化を争点にする構え (The Verge の分析記事)
- **何が起きたか**: The Verge は、民主党が少なくとも一方の院で多数派を取れば主要委員会の委員長が民主党に移り、AI 企業への監視が強まる可能性があると分析している。報道機関の分析で、新しい事実としての動きはない。
- **なぜ重要か**: 安全インシデントの報告義務など、米国の AI 規制の方向に影響しうる。
- 出典: [The Verge](https://www.theverge.com/policy/1013113/democrats-ai-midterms)

## AI セキュリティ

### [2026-10-19] 1 人の攻撃者が OSS のエージェント基盤「Cairn」で 100 超のサイトに侵入。被害には John Deere、SharkNinja、Cummins、日本企業も
- **何が起きたか**: AI セキュリティ企業 Norforge が、OSS のエージェント基盤 Cairn のインスタンスが外部に露出しているのを見つけ、その作業記録から攻撃を突き止めた。最も活発だった攻撃者は、米国、カナダ、オーストラリア、日本の企業のサイト 100 超に侵入していた。Reuters によると、好みの侵入手口を 100 字未満の中国語で指示するだけで、エージェントがほぼ自律で動き、侵入成功までは平均約 23 時間だった。「悪意がある可能性が高い」露出インスタンスは 20 超ある。John Deere は「機密情報へのアクセスの兆候はない」と説明している。
- **なぜ重要か**: 自律エージェントによる大量侵入が、実在の企業名とともに確認された。被害には日本企業も含まれる。攻撃者側のエージェント基盤が露出していたことで攻撃が判明した点は、脅威ハンティングの手がかりにもなる。
- 出典: [The Verge](https://www.theverge.com/ai-artificial-intelligence/1013643/ai-agents-hack-john-deere-shark-ninja-cummins)

### [2026-10-19] Wiz CIRT、「AI エージェントが最初から最後まで実行した」クラウド侵害の実例と痕跡を公開
- **何が起きたか**: Wiz の IR チームによると、最近の複数の侵害で AI エージェントが攻撃全体を動かしていた。ある事例では、外部に公開された Kafka UI の Java RCE を侵入口に、次のように広がった。Pod 内の SA トークンや IMDS の認証情報を収集し、GCP の token-creator 権限で認証情報を大量に発行し、AWS の SSM で横展開した。さらに IdP の管理 API キーで「pentest-」で始まる管理者ユーザーを作成し、CI/CD の Runner で認証情報のスプレーを並行して実行した。同じ攻撃元 IP は、同じ時間帯に 600 超の Wiz 顧客環境をスキャンしていた。Wiz は AI 主導の攻撃の痕跡として、`pentest` / `recon` / `exfil` のようなリソース名、数字のタスク ID と `-b` / `-c` の再試行サフィックス、手順コメント付きの生成コードを挙げている。
- **なぜ重要か**: 「pentest」を名乗るリソースは、正規の診断と見分けがつきにくい。診断を請け負う側も、リソースの命名規則と顧客への事前通知の運用を見直す必要がある。
- 出典: [Wiz](https://www.wiz.io/blog/anatomy-of-ai-driven-cloud-attacks)

### [2026-10-20] [続報] OpenCode Console の侵害: 影響は利用者の 1.4%。共同創業者は「AI エージェントが 48 時間攻撃を続けた」「調査ではモデルの拒否に阻まれた」と説明
- **前回 (10/19 号、10/17 の項目) から変わった点**:
  - 影響範囲は Console 利用者の 1.4%。キーが露出した可能性のある最も早い時刻は 10/17 00:30 UTC。CLI 版とデスクトップ版のキーは端末内の SQLite に保存されており、対象外。
  - 不正請求は 1 件あたり数百ドルで、利用者の報告では最大 1,700 ドル。Anthropic と Google は漏れたとみられるキーを無効化し、OpenAI は返金に協力している。Google が利用者のプロジェクトを停止した例も出ている。
  - 共同創業者 Dax Raad 氏は、攻撃者が AI エージェントで少なくとも 48 時間攻撃を続けたと述べた。自社の調査は、悪性コードを解析させるたびにモデルが拒否して進まなかったが、10/17 に OpenAI の防御側向けプログラム「Daybreak」の利用承認を得てから状況が安定したという。同社は今回の侵害を「大規模な蒸留攻撃」と呼んでいるが、侵入経路は明かしていない。
- **なぜ重要か**: 攻撃と防御の双方で AI が使われた事例を、ベンダー自身が説明している。防御側の調査でモデルの拒否が障害になる点は同社の主張にとどまるが、ベンダーが検証済みの防御者向けアクセスを用意する流れの背景になっている。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/opencode-hack-exposes-api-keys-amid-ai-distillation-attacks/) / [TechCrunch](https://techcrunch.com/2026/10/19/hackers-hit-ai-coding-tool-opencode-running-up-charges-on-users-ai-accounts/) / [The Hacker News](https://thehackernews.com/2026/10/opencode-console-breach-may-have.html)

### [2026-10-20] Envoy AI Gateway の MCP プロキシで、他の利用者の MCP セッションを乗っ取れる (GHSA-953h-535j-jg2v)
- **何が起きたか**: `github.com/envoyproxy/ai-gateway` の 0.4.0-rc1 以上 1.2.0-rc1 未満に影響し、1.2.0-rc1 で修正された。CVE は未採番で、深刻度は Moderate。MCP プロキシはクライアントに返す `Mcp-Session-Id` に JWT の `sub` を埋め込んでいるが、セッション再開時にはこの値を捨て、現在の呼び出し元と照合していない。さらに公式 Helm chart は、セッション ID の暗号鍵シードの既定値として公知の文字列 `default-insecure-seed` を持っている。このため、既定設定のままだと任意の subject のセッション ID を偽造でき、他人のバックエンド MCP セッションで `tools/call` や `resources/read` を実行できる。
- **なぜ重要か**: MCP 仕様が推奨する「セッションとユーザーの紐付け」が、マルチテナントのゲートウェイで実装されていなかった典型例。診断では、他ユーザーの `Mcp-Session-Id` に差し替えて再開できるか、Helm の既定シードが残っていないかを確認する。
- 出典: [GHSA-953h-535j-jg2v](https://github.com/theagentrouter/agent-router/security/advisories/GHSA-953h-535j-jg2v) / 修正: [commit 0d1e730](https://github.com/theagentrouter/agent-router/commit/0d1e73037076d72251342d0ea578a36ffb7002c7)

### [2026-10-20] AI 向けの索引化スキル「Graphify」で、信頼できないリポジトリを読ませるとローカルの任意のファイルが出力物と LLM に流れる (GHSA-pcc4-rvhr-2pr8)
- **何が起きたか**: PyPI の `graphifyy` 0.7.2 以上 0.9.70 未満が影響を受ける。Graphify は Claude Code、Cursor、Codex などで使うスキルで、フォルダを知識グラフに変換する。Fortran の前処理では `cpp -nostdinc -I /dev/null` で include を防いでいるつもりだったが、絶対パス (`#include "/etc/passwd"`) や `../` のパスは防げていなかった。読み込んだ内容は `graph.json`、`GRAPH_REPORT.md`、HTML の出力に埋め込まれ、エージェントにも渡される。API キーが不要なオフラインの既定経路 (`graphify update .`) で起きる。
- **なぜ重要か**: 「エージェントに渡すコンテキストを作るツール」が、ホストのファイルを外に出す経路になった。RAG やコード索引の前処理で外部コマンド (cpp など) を呼ぶ箇所は、診断の重点になる。
- 出典: [GHSA-pcc4-rvhr-2pr8](https://github.com/Graphify-Labs/graphify/security/advisories/GHSA-pcc4-rvhr-2pr8) / 修正: [commit e1d9dee](https://github.com/Graphify-Labs/graphify/commit/e1d9deed6a437f2c85458ef3c42519159f322b7b)

### [2026-10-20] エージェント制御プレーン「LoopX」のローカル状態画面が `ACAO: *` を返し、任意のサイトから非公開の情報を読める (CVE-2026-108372)
- **何が起きたか**: PyPI の `loopx` 0.0.1 以上 0.4.5 未満が影響を受ける (CVSS v4 で High)。127.0.0.1:8766 で動く `loopx serve-status` は、認証のない GET 応答すべてに `Access-Control-Allow-Origin: *` を付けていた。このため、運用者が訪れた任意のサイトが `fetch()` で `/status.json` (ゴール、実行履歴、絶対パス) や `/review-material` (Markdown の中身) を読み出せた。
- **なぜ重要か**: 「localhost だから安全」というエージェント管理 UI の前提が、ブラウザ経由の読み出しで崩れる典型例。AI 開発ツールのローカルサーバーを診断するときは、CORS ヘッダと Origin の検査を確かめる。
- 出典: [GHSA-vx2m-gpq4-8j5q](https://github.com/loopx-project/loopx/security/advisories/GHSA-vx2m-gpq4-8j5q) / 修正: [commit 838720f](https://github.com/loopx-project/loopx/commit/838720fba42bd22f71b5bb763ec406f7bdf4c940)

### [2026-10-19] コーディングエージェントに危険な allow ルールを承認させる攻撃。Claude Code や Codex CLI で 58% 成功 (arXiv 2610.22987)
- **何が起きたか**: 研究者はリポジトリに敵対的なコンテキストを仕込み、日常の作業中のエージェントを誘導して、もっともらしい理由を付けた広すぎる allow ルールをユーザーに承認させた。Claude Code や Codex CLI を含む本番の製品で、58% の試行で目的のルールを引き出せた。ルールは能力テストケースの 56.9% をカバーするほど広い。承認された場合、検知されずに目的を達成できたのは 47/58 件 (81.0%) だった。
- **なぜ重要か**: 承認疲れの対策である「ルールを保存して以後は聞かない」仕組みそのものが攻撃面になる。エージェントを導入した環境の診断では、保存済みの allow ルールを棚卸しし、範囲を評価する項目を加えるべきである。
- 出典: [arXiv 2610.22987](https://arxiv.org/abs/2610.22987)

### [2026-10-19] モデルの重みにマルウェアを埋め込む研究 2 本: DNS だけで秘密を持ち出す「Model-as-a-Trojan」と、リポジトリ汚染を自動化する「TrojanForge」
- **何が起きたか**: Model-as-a-Trojan (arXiv 2610.22578) では、オープンウェイトの LLM をファインチューニングし、シェルツールが使えると判断した最初のターンで 1 回だけ隠れた動作をさせた。その動作は、環境変数の秘密を base32 で符号化し、攻撃者の権威 DNS サーバーへの問い合わせとして送り出すもの。DNS 以外の通信を遮断したコンテナからも秘密を持ち出せ、プロンプトで止めようとした 20 回すべてで発動した。TrojanForge (arXiv 2610.23109) は、AST 解析とエージェントの実行トレースからペイロードの最も目立たない埋め込み位置を選び、偽装を改良する。384 リポジトリのベンチマーク「TrojanBench」で評価し、著者は汚染の成功率が 60% 超、バックドア注入率が 90% 超で、商用エージェントも防げなかったと報告している。
- **なぜ重要か**: 「サンドボックスに入れれば安全」という前提が崩れる。エージェントのサンドボックスを評価するときは、DNS 経由の持ち出し、環境変数に置いた秘密、モデルの出所の検証を確認項目に入れる必要がある。
- 出典: [arXiv 2610.22578](https://arxiv.org/abs/2610.22578) / [arXiv 2610.23109](https://arxiv.org/abs/2610.23109)

### [2026-10-20] Terra Security の分析: 2026 年は「修正の修正」が急増し、90 日以内に修正が破られた割合が 0.2% から 2.3% に
- **何が起きたか**: AI ペンテストの新興企業 Terra Security が、公開済みの CVE と GitHub がレビューした advisory を分析した。90 日以内に「修正が不完全」とする追加の advisory が出た割合は、2019〜2025 年の約 0.2% から 2026 年は 2.3% に増えた。修正を迂回されたバグが KEV に載る確率は、同じベンダーの他のバグの約 4 倍。修正が破られた CVE ではプロトタイプ汚染 (約 11 倍) と SSRF (4.6 倍) が多く、拒否リスト型の修正が原因とされる。記事は、AI によるパッチ解析が広がったことと結び付けて論じている。
- **なぜ重要か**: 数値はベンダーの主張である。それでも、パッチの差分が AI に読まれる前提で、パッチ適用後に迂回できないかを確かめる手順の価値を裏付けている。特に SSRF、プロトタイプ汚染、ブロックリスト型の修正が対象になる。今日の CVE 欄でも Camel Hazelcast と Camel Mail が不完全修正の例として並んでいる。
- 出典: [The Register](https://www.theregister.com/patches/2026/10/19/security-patches-need-patches-now-that-attackers-have-ai/5303927)

## セキュリティニュース

> CISA KEV: 10/20 05:00 JST 時点の catalogVersion は 2026.10.16 のままで、10/17 以降 (米国時間) の追加はない。

### [2026-10-18] Plex Media Server の未認証 RCE チェーン「Plex2Shell」、PoC 公開の翌日に悪用 (→ 深掘り)
- **何が起きたか**: 4 件の CVE (CVE-2026-96652 / -96654 / -96655 / -96656) を連鎖させる未認証 RCE の PoC が 10/16 に公開され、10/17 にハニーポットで悪用が観測された。攻撃者はマイナーとプロキシ型のバックドアを置いた。修正版は 1.43.3.10861。
- **悪用 / PoC**: 悪用あり / PoC 公開あり。詳細は「今日の深掘り」を参照。
- 出典: [SecurityWeek](https://www.securityweek.com/plex2shell-exploit-chain-weaponized-against-plex-servers-hours-after-disclosure/)

### [2026-10-20] Siemens Software Center の DLL 検索パスの欠陥 (CVE-2026-110936) が、ClickFix 攻撃で悪用される
- **何が起きたか**: Siemens は 10/15 に、Software Center が DLL を読み込む場所の制限不備 (CVE-2026-110936、CVSS v4 8.4) を公開し、10/17 に修正版 4.0.9.8 を案内した。10/19 には、実際に悪用されていると報告した。攻撃者は正規の署名付き Software Center (3.5.8.7) と悪性の DLL を 1 つのパッケージにまとめ、ClickFix (偽の CAPTCHA などでコマンドを貼り付けさせる手口) で配っていた。Siemens によると、自社の配布経路は侵害されていない。配布サーバーは、Forescout が先週報告した ClickFix の配信基盤「Romulus」と一致した。
- **悪用 / PoC**: 悪用あり / 公開 PoC なし。
- **なぜ重要か**: 正規の署名付きバイナリを使った DLL サイドローディングのため、ハッシュベースの検知が効かない。Siemens も、フォルダや振る舞いで検知するよう勧めている。OT ベンダーのツールが、IT 側の攻撃の運び屋に使われた例。
- 出典: [Siemens ProductCERT](https://productcert.siemens.com/news/2026/10/19/active-exploitation-of-cve-2026-110936-in-siemens-software-center/) / [SecurityWeek](https://www.securityweek.com/siemens-software-center-vulnerability-exploited-in-clickfix-malware-attacks/)

### [2026-10-20] Rapid7、NetScaler ADC の侵害事例を分析: CVE-2026-88771 と -88779 を連鎖させ、クラッシュハンドラー経由で root を取る
- **何が起きたか**: Rapid7 が、10 月上旬に対応した NetScaler 14.1 系の侵害事例を公開した。攻撃者は、認証のユーザー名にコマンド文字列を埋め込んだ (CVE-2026-88771、事前認証のログ汚染)。次に SAML の解析で nsaaad をクラッシュさせ (CVE-2026-88779)、再起動を起こした。再起動後にクラッシュハンドラーがその文字列を処理し、root で実行した。侵害後は、`/nsconfig/.slap` 配下にフレームワークを置き、LogonPoint ディレクトリに CSS 風の名前の PHP Web シェルを置き、`/bin/sh` を mode 6555 に変更し、HA ペアをまたいで永続化した。さらに Go 製の偵察ツールを使い、設定と鍵を持ち出した。
- **悪用 / PoC**: 悪用あり (両 CVE とも KEV 登録済み) / 公開 PoC なし (注入文字列の形とハッシュは記事に掲載)。
- **なぜ重要か**: パッチを当てても、侵害済みの機器から痕跡は消えない。確認すべき場所として、`/nsconfig/.slap`、LogonPoint の不審なファイル、`/bin/sh` の権限、クラッシュの記録が具体的に示された。HA ペアは両方の機器を調べる必要がある。
- 出典: [Rapid7](https://www.rapid7.com/blog/post/ra-netscaler-intrusions-chaining-cve-2026-88771-and-cve-2026-88779)

### [2026-10-20] Rapid7、施設管理ソフト Eptura Archibus の認証回避と RCE (CVE-2026-107186 / -107187 / -107188) を公開
- **何が起きたか**: Archibus Web Central の Java DWR API に欠陥があり、未認証で任意のワークフロールールを実行できる (CVE-2026-107186、CVSS 8.6)。DWR は 1 回のリクエストに複数のメソッド呼び出しを詰め込め、同じスレッドで順に処理する。認証なしで呼べる `isPasswordUppercase()` がスレッドのコンテキストに特権セッションを設定してしまうため、同じリクエストで続けて呼んだ `runWorkflowRule()` がその権限で動く。この経路から、DB の全件読み出し (-107187、8.5) と、ファイルアップロードによる RCE (-107188、9.6) に到達できる。修正版は 2025.02 以降。
- **悪用 / PoC**: 野良の悪用は報告なし (Rapid7 のレッドチーム演習で使用) / リクエストの具体例を記事に掲載。
- **なぜ重要か**: Eptura によると、Fortune 500 の 40% が Archibus を使っている。「認証なしで許可されたメソッドがスレッドローカルのコンテキストを汚し、同じバッチの後続の呼び出しがその権限を引き継ぐ」というバグクラスは、DWR や JSON-RPC のバッチ処理を持つ他の製品にも当てはまる。
- 出典: [Rapid7](https://www.rapid7.com/blog/post/ve-authentication-bypass-remote-code-execution-and-database-read-in-eptura-archibus-fixed)

### [2026-10-20] [続報] GhostAction が第 2 段階へ: VS Code でリポジトリを開くだけで動くスティーラーを 94 リポジトリに仕込む
- **前回 (10/15、GitGuardian による規模の公表) から変わった点**: OpenSourceMalware によると、攻撃者は GitHub のセキュリティ警告を装ったメールで my-github[.]com に誘導していた。このサイトはリバースプロキシ型のフィッシングで、パスワードと 2FA コードを盗み、さらに OAuth デバイスフロー (repo / workflow / read:org の権限) を被害者に気付かれないよう自動で承認させていた。10/9 に GitHub が悪性ワークフローの実行を止めると、攻撃者は 6 日後に Runner を使わない第 2 段階へ移った。`runOn: folderOpen` を指定した VS Code の `tasks.json` と、スティーラー本体の `public/fonts/fa-solid-400.woff2` (北朝鮮の PolinRider と同じファイル名) を、66 オーナーの 94 リポジトリに commit した。スティーラーは AWS、npm、PyPI、SSH、Kubernetes、Anthropic、Gemini の認証情報を盗む。
- **悪用 / PoC**: キャンペーンが進行中。
- **なぜ重要か**: リポジトリを clone して VS Code で開くだけで動く。調査や診断でサードパーティのリポジトリを開く人も被害を受けうるため、workspace trust と `tasks.json` の自動実行の設定を確認しておく。
- 出典: [The Hacker News](https://thehackernews.com/2026/10/ghostaction-attackers-plant-credential.html) / [OpenSourceMalware](https://opensourcemalware.com/blog/ghostaction-attack-escalates)

### [2026-10-20] 人材派遣向け SaaS の Bullhorn がサイバー攻撃でプラットフォームを停止。API パスワードのローテーションを要求
- **何が起きたか**: 1 万社超の人材会社が使う Bullhorn で、10/16 に求人掲載の障害が起き、翌日には全体に広がった。同社は攻撃によるものと認め、アクセスを止めて CrowdStrike と調査している。ATS/CRM、Automation、Back Office などが停止した。データが持ち出されたかはまだ分かっていない。SSO を使っていないユーザーは全員パスワードのリセットが必要で、API パスワードのローテーションも求められている。
- **悪用 / PoC**: 侵入は確認済み、手口は不明 / 該当なし。
- **なぜ重要か**: ConnectWise と同じく、多数の顧客が連携する SaaS の侵害。連携に使う認証情報のローテーションが、利用企業側の作業として発生する。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/bullhorn-takes-staffing-platform-offline-to-contain-cyberattack/)

### [2026-10-20] [続報] Ahold Delhaize、障害の原因を「悪意ある行為」と認め、オランダ警察に被害届
- **前回 (10/13 号、一部システムの停止) から変わった点**: 10/19 に攻撃によるものと正式に認め、警察に被害届を出した。米国 (Food Lion、Stop & Shop) のオンライン販売はまだ止まっている。顧客データが盗まれた証拠は今のところないとしている。ランサムウェアかどうかは公表していない。
- 出典: [The Record](https://therecord.media/ahold-delhaize-cyberattack-grocery)

### [2026-10-19] カリフォルニア州の生徒の記録が、テスト委託先 ETS の SFTP から 4 か月にわたり盗まれる。原因は漏れたログイン 1 件
- **何が起きたか**: 州のテストを担う ETS が州教育省とのデータ共有に使っていた SFTP サイトに、5/22〜9/18 のあいだ、漏えいした認証情報で繰り返しアクセスされた。直近 3 学年に在籍した生徒全員を含む記録が複製された。2025〜26 年度の在籍者は 570 万人超。障害の区分やテスト結果などの機微な情報を含むが、SSN は含まない。検知は 9/25 だった。
- **悪用 / PoC**: 不正アクセスあり / 該当なし。
- **なぜ重要か**: MFA のない SFTP と認証情報 1 件だけで、長期間の大量流出が起きた。委託先のファイル転送基盤は、診断の範囲から漏れやすい。
- 出典: [SecurityWeek](https://www.securityweek.com/one-compromised-login-exposed-millions-of-california-students-records/)

### [2026-10-19] Krebs: ShinyHunters の捜査で、ランサム交渉会社の幹部が恐喝サイトの運営を手伝った疑い
- **何が起きたか**: 9 月に fbijobs.gov を侵害された FBI が、ShinyHunters の関係者を追っている。9/15 にオランダで逮捕された Pepijn van der Stap 容疑者の Signal のやりとりから、カナダと米国のランサム交渉担当者との近い関係が分かった。関係筋によると、米国側の 1 人は被害者に支払いを迫るサイトの運営に関わっていた。FBI によると、ShinyHunters の今年の恐喝額は 7,000 万ドルを超える。
- **なぜ重要か**: 被害企業が頼る「交渉人」の信頼性が問われる事案。インシデント対応の体制に外部の交渉会社を組み込むときの審査に関わる。
- 出典: [Krebs on Security](https://krebsonsecurity.com/2026/10/feds-suspect-ransom-negotiator-ran-shinyhunters-extortion-site/)

### [2026-10-20] Citizen Lab、セルビアの総選挙直前にベオグラード大学学長の iPhone で Pegasus 感染を確認
- **何が起きたか**: 10/25 の総選挙を前に、学生の抗議運動を支持する Vladan Đokić 学長の iPhone で、今年の Pegasus 感染を Citizen Lab が確認した。汚職を捜査した検事も 8 月に Apple から脅威通知を受けており、端末を解析している。SHARE Foundation などの集計では、2026 年にセルビアで高度なスパイウェアの標的になったのは少なくとも 15 人。
- **悪用 / PoC**: 感染を確認 / 該当なし。
- 出典: [The Record](https://therecord.media/serbia-spyware-pegasus-elections)

### [2026-10-20] 米連邦地裁、NSO が差止命令に違反したという WhatsApp の申し立てを退ける。証拠の詳細を伏せたことが理由
- **何が起きたか**: Hamilton 判事は 10/16、WhatsApp による法廷侮辱の申し立てを退けた。Meta は、2025 年の差止命令の後も NSO が 23 の新しいアカウントを狙ったと主張したが、検知手法を明かさない形で証拠を出した。判事はこれを「計算されたリスク」とし、明確かつ説得力のある証拠がないと判断した。
- **なぜ重要か**: 検知手法を秘匿したいプラットフォームと、立証責任とのあいだのジレンマが表に出た判断。
- 出典: [The Record](https://therecord.media/whatsapp-denied-appeal-alleged-nso-group-violation-injunction)

### [2026-10-19] 10 月の Windows Server 更新で、オンプレの Exchange に OWA のサインイン障害と送信の滞留
- **何が起きたか**: Windows Server 2019 以降に 10 月の累積更新を当てると、Endpoint Mapper の同時 Endpoint Lookup 数が既定で 512 に制限される。負荷の高い Exchange では OWA で `MapiExceptionMdbOffline (ec=1142)` や Event ID 1006 が出て、メールが送信トレイに滞留する。暫定策は `HKLM\SOFTWARE\Microsoft\Rpc\EpmapSavedContextCap` (DWORD 65536) を設定して再起動すること。Microsoft は、Exchange の 10 月の SU とは無関係なので SU をアンインストールしないよう呼びかけている。
- **なぜ重要か**: 10 月は Patch Tuesday の修正件数が多い。症状と回避策を把握しておけば、パッチを外すという誤った判断を避けられる。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/microsoft/microsoft-october-windows-server-updates-cause-exchange-issues/)

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-10-18 以降 (NVD published) / 修正コミット公開済み or バグクラスが言語化可能なものを優先。いずれも KEV 未掲載で、EPSS は bootc 以外まだ算出されていない。
> AI 関連の GHSA (Envoy AI Gateway / Graphify / LoopX) は「AI セキュリティ」に記載。

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-109432 | Camunda 7 engine-rest 7.24.0〜7.24.14 未満 / 7.23.0〜7.23.17 未満 | CWE-917 / 9.8 | TaskQuery の `orQueries` で作られる OR サブクエリにだけ `AdhocQueryValidator` が登録されない → 権限のない認証済みユーザーの `dueAfterExpression` などで JUEL が評価される → `Runtime.exec` による RCE | [VulnCheck advisory](https://www.vulncheck.com/advisories/camunda-expression-injection-via-orqueries-rce) (commit 不明、Enterprise 版のみ配布) | **詳細な再現手順が公開済み** ([codeant.ai](https://codeant.ai/security-research/camunda-adhoc-query-expression-rce-cve-2026-109432)) |
| CVE-2026-111057 | mljar Mercury 3.0.0〜3.2.4 未満 | CWE-185 / 10.0 | `BLOCKED_PATTERNS` のカンマ 1 つの抜けで、Python の暗黙の文字列連結により 2 つの正規表現が 1 つになる → 匿名ブロックリストが `/api/terminals` に一致しない → 未認証で Jupyter の terminal を開き OS シェル | [diff](https://github.com/mljar/mercury/commit/8c467129037ee9df269d543ac217ffd33b97bf3f) | 単一リクエストで悪用できる |
| CVE-2026-80343 | Apache Camel camel-netty-http 4.0.0〜4.18.5 未満 / 4.19.0〜4.22.1 未満 | CWE-178 / 8.2 | 認可の security constraint はパスを大文字小文字区別で比較し、ルーティングは区別しない → パスの大文字小文字を変えたリクエストが制約に一致しない → 保護されたルートへ認証なしで到達 | [PR #25578](https://github.com/apache/camel/pull/25578) (commit 不明) | 前提条件なし、PoC は容易と見られる |
| CVE-2026-80344 | Apache Camel camel-as2 (同上) | CWE-918 / 8.2 | 送信者が AS2 の非同期 MDN の返送先 (`Receipt-Delivery-Option`) を指定できる → 受信側が MDN 送信の接続先にその URL をそのまま使う → 受信側からの SSRF と、MDN 用の資格情報の送出 | [PR #25637](https://github.com/apache/camel/pull/25637) (commit 不明) | プロトコル仕様起因 (RFC 4130) |
| CVE-2026-79983 / -79984 / -79985 / -79986 | Apache Camel camel-ftp / mina-sftp / smb / azure-files (同上) | CWE-22 / 7.4 | サーバーが返すディレクトリ一覧のファイル名に `../` を入れられる → 共通の `GenericFileConsumer` が正規化せずに連結し retrieve / delete / rename に渡す → 監視ディレクトリ外のファイルの取得・削除・移動 | [PR #25730](https://github.com/apache/camel/pull/25730) (commit 不明) | 共通 sink で 4 プロトコルに波及 |
| CVE-2026-78162 | Apache Camel camel-hazelcast (同上) | CWE-502 / 10.0 (v4) | `ReplicatedHazelcastAggregationRepository.doStart()` が `super.doStart()` を呼ばず、以前の修正 (CVE-2026-43865) のシリアライズフィルタが付かない → ReplicatedMap の値をデシリアライズ → クラスタに届く攻撃者による RCE | [PR #25566](https://github.com/apache/camel/pull/25566) (commit 不明) | 不完全修正 |
| CVE-2026-111750 (+ -111748 / -111064) | aiohttp < 3.14.4 | CWE-444 / 6.3 | C 拡張を使わない構成で、Pure Python の HTTP/1.1 パーサが曖昧なフレーミングを受け入れる → 前段プロキシと解釈がずれる → リクエストスマグリング。-111748 では absolute-form の request-target で `Request.scheme` を偽装できる | [diff](https://github.com/aio-libs/aiohttp/commit/9b27347e61454d9f8ca2055f4c67a37dee336e83) / [diff (scheme)](https://github.com/aio-libs/aiohttp/commit/6d4e7b01f9b951aa084a75d7356e907d4ee80411) | 二重パーサの差分 |
| CVE-2026-111755 | follow-redirects 1.16.0〜1.16.1 未満 | CWE-185 / 8.2 | アプリが指定した機密ヘッダ名に `^` や `\|` が含まれる → 自作の `escapeRegex` がエスケープせずに除去用の正規表現を作る → cross-origin のリダイレクト先に資格情報ヘッダが送られる | [diff](https://github.com/follow-redirects/follow-redirects/commit/080a76d0e125b37bf81717368a61d5dc37aa56c8) | axios 経由で依存数が非常に多い |
| CVE-2026-107567 | hMailServer 6.0.0〜6.3.6 | CWE-348 / 7.5 | ホストしているドメインで DKIM 署名が有効 → 最初の配送で、送信者を確かめずに From ヘッダのドメイン鍵で署名する → 外部の第三者が偽装した From のメールが、DMARC に適合した署名付きで転送される | [compare v6.3.6...v6.3.7](https://gitlab.com/hmailserver/hmailserver/-/compare/v6.3.6...v6.3.7) (commit 不明) | 再現は容易と見られる |
| CVE-2026-103314 | Red Hat Advanced Cluster Security (Central) | CWE-294 / 7.4 | 有効期限内の署名済み SAML Response を入手できる → ACS エンドポイントが使用済みの Assertion ID を保持しない → 同じ Response を再送するたびに別の Central トークンが発行される | [Red Hat advisory](https://access.redhat.com/security/cve/CVE-2026-103314) (commit 不明) | SAML 実装の定番の見落とし |
| CVE-2026-16487 / -16460 | bootc / ostree | CWE-345 / 8.1・7.4 | 既定の署名ポリシーで対象レジストリが `insecureAcceptAnything` に落ちる → mutable tag で取り込んだイメージを OS の rootfs として staging する → tag を書き換えられる攻撃者のコードが再起動後に root で動く (-16460 はポリシー強化前に staged されたデプロイを再検証しない TOCTOU) | [Red Hat advisory](https://access.redhat.com/security/cve/CVE-2026-16487) (commit 不明) | EPSS 0.00173 / 0.00078 |
| CVE-2026-112377 | CCC attested-tls-poc (commit 731ca82 まで) | CWE-346 / 9.1 (v4) | 攻撃者が attested TLS の秘密鍵を持っている → 検証側が、TLS のハンドシェイク鍵や transcript に結び付いていない Evidence を受け入れる → 本物の attester へ nonce を中継してなりすまし、通信を傍受 | [PR #58](https://github.com/CCC-Attestation/attested-tls-poc/pull/58) (commit 不明) | プロトコル設計起因 |

**今日の CVE 所感**
- 今日の共通バグクラスは「**一方の経路にだけ掛かったチェック**」。Camunda (OR サブクエリにだけ validator がない)、Camel Hazelcast (super を呼ばないサブクラスに修正が届かない)、Camel netty-http (認可とルーティングで大文字小文字の扱いが違う)、aiohttp (C と Pure Python のパーサの差) と、同じ形の不備が並んだ。修正差分を読むときは「チェックを入れた場所」より「チェックを通らない兄弟経路」を探すのが近道になる。
- 他の実装へ水平展開しやすいのは、プロトコル仕様に起因する 3 件である。AS2 の async MDN の URL を信用する SSRF (OpenAS2、Mendelson、B2B ゲートウェイ)、From ヘッダを基準にした DKIM 署名 (Postfix の OpenDKIM 構成、Exim の `dkim_domain`)、attested TLS の Evidence が接続に結び付いていない件 (RA-TLS、Confidential Containers の KBS)。
- 「サーバー応答を信用するクライアント」(Camel の LIST 応答のファイル名、follow-redirects のヘッダ除去) は、Spring Integration の (S)FTP アダプタ、Apache Commons VFS、undici や requests のリダイレクト処理にも同じ観点で当てられる。
- 診断で優先するのは次の 3 つ。Apache Camel 4.x (25 件超の一斉公開。AS2、netty-http、file 系 consumer を使っていれば 4.18.5 / 4.22.1 へ)、Camunda 7 の engine-rest (再現手順が公開済み)、Mercury と Jupyter をラップするサービス全般 (`/api/terminals` と `/api/kernels` に匿名で届くか)。
- 参考: 同じ日に、ネストの深さに上限のないデコーダの再帰による DoS が 3 件まとめて出ている (MongoDB PHP driver CVE-2026-112368、Fleet の plist CVE-2026-111923、Cpanel::JSON::XS CVE-2026-110673)。picomatch ≤ 4.0.7 の ReDoS (CVE-2026-112366) も依存数が多い。

## 日本国内のセキュリティ動向

### 国内インシデント・事故

#### [2026-10-19] ユミルリンク、メール配信 ASP「Cuenote FC」の専用 ASP 5 システムからメールアドレスを含む延べ約 900 万件が持ち出される
- **何が起きたか**: ユミルリンク (東証スタンダード 4372) は 10/19 に第一報を出し、同日 19:05 に補足を追記した。
  - 10/16 (金) 未明に、一部のシステムへの不正アクセスに気付いた。
  - アクセス記録から確認された手順は次の 4 段階である。(I) プログラムの脆弱性を突く。(II) 自社のサポート・品質管理担当者がサービスに使う認証情報を取得する。(III) 不正なプログラムを置き、DB からデータを出力する。(IV) その担当者の認証情報で、他のシステムへの認証を試みる。
  - 対象は「Cuenote FC 専用 ASP プラン」の 5 システムで、メールアドレスを含む情報が延べ約 900 万件出力されたと同社は試算している。どの顧客企業が対象かは公表されていない。
  - 脆弱性は修正済みで、担当者の認証情報は削除し、捜査機関にも届け出た。
- **なぜ重要か**: 今回の期間で最大の件数である。メール配信 SaaS は多くの企業の会員メールアドレスを預かっているため、SpeeCAN RAIDEN や IDCF と同じく、委託先が侵害されると被害が利用企業へ広がる。今後、利用企業による公表が続くとみられる。診断の観点では、ベンダーのサポート担当者が持つ「顧客環境に横断的に入れる認証情報」が横展開に使われた点が重要である。
- 出典: [ユミルリンク (Cuenote)](https://www.cuenote.jp/information/news/unauthorizedaccess.html)

#### [2026-10-19] エイチ・ツー・オー リテイリング (阪急阪神百貨店)、予約サイト経由で共通 ID「H2O ID」の約 126 万件、ほぼ全会員分が漏えい
- **何が起きたか**: エイチ・ツー・オー リテイリング (8242) は 10/19 に適時開示し、阪急阪神百貨店と連名で公表した。
  - 10/16 に「阪急百貨店・阪神百貨店予約サイト」を経由した顧客管理システムへの不正アクセスを確認し、サイト全体を止めた。
  - 10/17 には通販の「HANKYU HANSHIN E-STORES」と「Remo Order」でも不正アクセスを確認し、両方を止めた。
  - 10/19 に、H2O ID 約 126 万件の個人情報の一部が漏えいしたことが分かった。項目は ID、氏名、性別、メールアドレス、住所、電話番号、年齢、生年月日、利用サービスである。
  - E-STORES と Remo Order から漏れたかどうかは調査中である。この 2 つは注文履歴、カードの下 4 桁・名義・有効期限、アドレス帳を保持している。パスワードの漏えいは確認されていない。
- **なぜ重要か**: 予約サイトという周辺のシステムから、グループ共通 ID の顧客管理システムに到達されている。共通 ID 基盤では、入口となる 1 つのサービスの不備が全会員の漏えいにつながることを示した。
- 出典: [H2O リテイリング (PDF)](https://data.swcms.net/file/h2o-retailing/ja/news/auto_20261019552921/pdfFile.pdf) / [阪急百貨店 (PDF)](https://www.hankyu-dept.co.jp/honten/info/detail/__icsFiles/afieldfile/2026/10/19/1019owabi1.pdf) / [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2610/19/2000002398/)

#### [2026-10-19] ニフティ、光回線の申込・受付管理システムに不正アクセス、最大 54 万 2,513 件が漏えいした可能性
- **何が起きたか**: 10/19 10:20 頃に不正アクセスを確認し、通信元を遮断した。同日中に第一報を出している。
  - 対象は 2019 年以降に、同社の Web サイト以外の経路で「@nifty 光」「@nifty MAX 光」「@nifty auひかりプラス」を申し込んだ顧客である。
  - 項目は会員 ID、氏名、性別、生年月日、住所、電話番号、メールアドレスである。口座とカードの情報は、このシステムには保存されていない。
  - 侵入されたのは社内で情報を登録するための管理ツールで、顧客が入力する申込フォームとは別のシステムである。
- **なぜ重要か**: 狙われたのは、公開フォームではなく内部の管理ツールである。JPCERT/CC が 10/8 に注意喚起した「公開 Web だけでなく管理画面や BI ツールも狙われる」という傾向に合っている。
- 出典: [ニフティ](https://www.nifty.co.jp/newsrelease/nifty202610195434.htm) / [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2610/19/2000002399/)

#### [2026-10-19] クリプトン・フューチャー・メディア、「SONICWIRE」と「D2R」に不正アクセス、会員最大約 42 万件
- **何が起きたか**: 10/17 (土) 20 時頃に不正アクセスの可能性に気付いた。侵害されたアカウントを無効にし、社内ドメインに IP 制限をかけたうえで、23:39 にサーバーを止めた。
  - 対象は SONICWIRE の会員 (ニュースレター購読者を含む) 最大約 42 万件である。項目は氏名、メールアドレス、パスワードのハッシュ値、住所 (請求書・見積書の発行時に入力した場合)、登録日などである。D2R の登録店舗は個別に連絡している。
  - 全会員のパスワードを無効にした。カード情報はシステムに保存していない。関連の EC ストアも止めている。
  - 同社は、検知後の状況把握に「Mythos を活用」したと書いている。
- **なぜ重要か**: 10/17 の週末に侵入され、2 日で公表している。最初の対応が「侵害されたアカウントの無効化」だったことから、アカウントの奪取が経路に含まれていた可能性がある。ただし、原因はまだ公表されていない。
- 出典: [クリプトン](https://www.crypton.co.jp/cfm/news/2026/10/20info)

#### [2026-10-18] 日本サッカー協会 (JFA)、公式アプリ「JFA Passport」に不正アクセス、一部の機能を停止
- **何が起きたか**: 10/17 の 3:25 頃から 19:00 頃まで不正アクセスがあった。アプリを提供している会社と連携して経路を遮断し、一部の機能を止めている。
  - 個人情報への影響は調査中である。利用者には、ログアウト、再ログイン、再インストールを当面控えるよう求めている。
- **なぜ重要か**: 約 16 時間にわたる侵入で、提供会社 (委託先) が関わっている。モバイルアプリの API を経路とする一連の事案 (ソースネクスト、バーガーキングなど) と同じ型かどうかは、まだ分からない。
- 出典: [JFA](https://www.jfa.jp/news/00036934/) / [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2610/19/2000002355/)

#### [2026-10-19] ふるさと納税サイト「ふるさとチョイス」(トラストバンク)、不正アクセスの疑いでサービスを一時停止
- **何が起きたか**: 10/19 に、不正アクセスの疑いがある事象を検知したとして、サイト全体を止めた。告知は公式 X で出ている。影響範囲と個人情報漏えいの有無は調査中で、再開時期は示されていない。
- **なぜ重要か**: 1,700 を超える自治体と契約するポータルで、寄付者の氏名、住所、決済に関する情報が集まっている。10 月はふるさと納税の需要が高まる時期であり、停止が長引けば自治体側の受付にも影響する。
- 出典: [ふるさとチョイス公式 X](https://x.com/furusato_tax/status/2112077365165900199) / [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2610/19/2000002391/) / [Impress Watch](https://www.watch.impress.co.jp/docs/news/2149387.html)

#### [2026-10-19] スクウェア・エニックス、アカウント管理システムへのパスワードリスト型攻撃を確認し、全アカウントのリセットも検討
- **何が起きたか**: 他社サービスから漏れたとみられるメールアドレスまたは ID とパスワードの組み合わせで、不正ログインが行われていることを確認した。
  - 被害が疑われるアカウントはログインを制限し、制限の解除にはパスワードの再設定を求めている。
  - 攻撃がさらに増えた場合は、全アカウントのパスワードを強制リセットする可能性があるとしている。
- **なぜ重要か**: 9 月以降の大量漏えい (ソースネクストは平文のパスワードを含む、下記の続報を参照) で、リスト型攻撃に使える組み合わせが増えている。漏えいの「二次被害」が他社のサービスで表に出てきた例である。
- 出典: [FINAL FANTASY XIV The Lodestone](https://jp.finalfantasyxiv.com/lodestone/news/detail/dbe2d8006c7907ab18e7b4335e9110c1e29309be) / [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2610/19/2000002397/)

#### [2026-10-19] ジグザグ、越境 EC「WorldShopping」で海外の顧客 301 名の個人情報が漏えい
- **何が起きたか**: ジグザグ (東証グロース 340A) が 10/19 に適時開示した。10/15〜16 に不正アクセスがあり、10/16 に検知した。
  - 漏れたのは台湾、香港、米国、韓国、中国などの顧客 301 名分で、項目はメールアドレス、氏名、住所、電話番号、注文情報である。カード情報とパスワードは含まれない。
  - 同社は「メール配信システムおよび入力フォームの不備」を修正し、攻撃者が使った認証情報を無効にして再発行した。
- **なぜ重要か**: 件数は小さい。ただ、メール配信の仕組みと入力フォームの組み合わせが侵入口になっている点は、SpeeCAN RAIDEN や Cuenote と共通する。
- 出典: [ジグザグ 適時開示 (PDF)](https://www.nikkei.com/markets/ir/irftp/data/tdnr/tdnetg3/20261019/g6s7x1/140120261019553141.pdf)

#### [2026-10-19] [続報] アルカディア (SpeeCAN RAIDEN) 第 12 報、侵入の時系列を公開。パストラバーサルから config.ini を取得し、シークレットキーでアカウントを総当たり
- **前回から何が変わったか**: 既報は件数と影響を受けた自治体だけだった。10/19 の PDF で、攻撃の手順が分単位で明らかになった。
  - 10/11 06:26 に攻撃が始まった。JS ファイルの取得、`/m/` 配下の探索、`/api2/login` でのログイン試行が続いた。10:52 にはディレクトリトラバーサル、11:04 にはセッション固定、15:49 には SQL インジェクションを順に試している。
  - 16:39 に、添付ファイルを公開するメディアサーバーのパストラバーサルを使って `config.ini` を取得した。その中のサービス間ログイン用のシークレットキーを使い、アカウント ID を総当たりしてログインした。
  - 社内で DB の異常な負荷に気付いたのは、同日 23:40 である。
  - 10/12 に WordPress のプラグインが追加されていたことが分かった。10/13 にはバックドアからの大量配信が見つかった。外部に送られた不正なメールは合計 1,423,428 通で、多くはカード会社を装ったフィッシングとみられる。
  - 10/14 には raiden3 の DB で書き換えられた箇所が見つかり、手作業で修正した。対策として、社内で動かす LLM による脆弱性診断とコードレビューを実施し、今後は外部診断と SOC の導入も検討する。
- **なぜ重要か**: 「JS の解析 → API の発見 → 各種の脆弱性チェック → 設定ファイルの取得 → 秘密鍵の悪用」という流れが、約 10 時間で自動的に進んでいる。JPCERT/CC (10/15) と GMO イエラエ (下記) が報告している AI 支援型の攻撃の特徴とよく合う。診断で優先すべきは、静的ファイルを配信するサーバーのパストラバーサルと、設定ファイルに平文で置かれたサービス間の鍵である。
- 出典: [アルカディア 第 12 報](https://raiden.site.ktaiwork.jp/archives/4597) / [経過報告 (PDF)](https://raiden.site.ktaiwork.jp/wp-content/uploads/sites/2/2026/10/2026_10_19AccessIncident.pdf)

#### [2026-10-18〜19] [続報] WASABI SWITCH 第四報・第五報、取引データを一時削除し、全アカウントのパスワードを強制変更して 2 段階認証を必須に
- **前回から何が変わったか**: 前回は第三報 (10/18 15:02 の更新) までを扱った。その後の動きは次のとおり。
  - 第四報 (10/18 12:05): 不正アクセスが何度も確認されたため、受注、買取、顧客の情報を、退避したうえでシステムから削除した。登録済みの認証情報 (各モール、FTP、メール、API) の暗号化は、予定より遅れて 10/18 中の完了を目指すとした。10/19 17:30 に方針の変更を追記したが、内容は店舗向けのチャットでだけ伝えている。
  - 第五報 (10/18 19:15): メンバー ID が利用ドメインと同じ文字列のアカウントや、推測しやすいパスワードのアカウントを狙った不正ログインが試みられていた。このため、10/18 20:30〜23:30 に全アカウントのパスワードを強制的に変え、メールによる 2 段階認証を必須にした。
- **なぜ重要か**: ID の命名規則が推測できること自体が攻撃面になっていた。SaaS の診断では、ログイン ID の規則性とレート制限を確認項目に入れたい。
- 出典: [ワサビ 第四報](https://wasabi-inc.biz/help/news/20261018-01/) / [第五報](https://wasabi-inc.biz/help/news/20261018-02/)

#### [2026-10-19] [続報] ソースネクスト、パスワードは「暗号化していたが、復号できる API が侵害され、平文で流出した」と認める
- **前回から何が変わったか**: 10/15 の発表では保存方式が分からなかった。ITmedia NEWS の取材に、同社は次のように答えた。
  - パスワードは可逆的に暗号化して保存していた。復号鍵にアクセスできるシステム (API) が不正アクセスを受け、パスワードは「復号された状態で外部に流出した」。
  - ハッシュ化しなかった理由は、システムの開発時期が古く、最新のハッシュ方式に移れていなかったためと説明した。
  - API の戻り値にパスワードを含めていた理由と、パスワード再設定後の保存方式については回答していない。
- **なぜ重要か**: 最大約 2,252 万件分の平文パスワードが出回っている可能性がある。上のスクウェア・エニックスのようなリスト型攻撃が、他社でも増えると考えられる。診断では、API のレスポンスに秘密情報が含まれていないか (過剰なデータ露出) を確認する重要性がはっきりした。
- 出典: [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2610/19/2000002372/)

#### [2026-10-19] [続報] Studio の件、利用企業の公表が続く (YAMAGATA 最大 1,463 件、TRUSTART 約 1,440 件)
- **前回から何が変わったか**: 新たに 2 社が公表した。両社が Studio から受けた説明で、次の 2 点が明らかになった。
  - 原因は「CMS の一部機能の脆弱性」である。
  - 不正アクセスは 9/30〜10/1 に確認され、データはその後、10/14 に Studio が対処するまで外部から取得できる状態だった。
- 出典: [YAMAGATA](https://yamagata-corp.jp/news/20261019) / [TRUSTART](https://www.trustart.co.jp/news/20261019)

> 参考 (新事実なし): Joshin は 10/19 に TDnet で日本語版の開示を出したが、内容は 10/17 と同じだった (停止中のサービスと漏えいの有無は未公表)。コミックシーモアとファンケル・アテニアは、Security NEXT が 10/19 に記事を出したが、既報から新しい事実はない。IDCF の最新は第 6 報 (10/18、既報)、石川コンピュータ・センターの最新は 10/17 (既報) のまま。Renta! は公式の原因説明がまだない。

### 国内の注意喚起・ガイドライン・政策

#### [2026-10-19] IPA「情報セキュリティ白書 2026」の書籍版を発刊
- **何が起きたか**: IPA は 10/19 に書籍版 (A4、208 ページ、2,200 円) を発売した。PDF 版は 9/30 に先行公開されている。
  - 構成は、序章 (2025 年度の概況)、第 1 章 (脅威の動向)、第 2 章 (サイバー安全保障、AI の安全性、偽・誤情報)、第 3 章 (国内の政策と、人材、評価認証、中小企業対策)、第 4 章 (国際的な政策と標準化) である。
  - 2025 年 5 月に成立したサイバー対処能力強化法、2025 年 12 月に閣議決定したサイバーセキュリティ戦略 (AI の安全性、AI を悪用した攻撃、AI を使った防御の 3 つの観点)、SCS 評価制度などを整理している。
- **なぜ重要か**: 2025 年度の公的な総括である。顧客に提出する報告書や提案書で、制度面の背景 (能動的サイバー防御、SCS 評価制度) を引用する際の出典として使える。9 月以降の連続漏えいは、まだ対象期間に含まれていない。
- 出典: [IPA](https://www.ipa.go.jp/publish/wp-security/2026.html)

> 上記以外に、期間内 (10/18〜20) の公的機関による新しい注意喚起やガイドラインは確認できなかった。確認したのは JPCERT/CC (注意喚起ページの最終更新は 10/14、Eyes の最新は 10/15)、国家サイバー統括室、警察庁 (最新は R8.10.16)、個人情報保護委員会、総務省、経済産業省、金融庁、JC3 (最新は 10/16) である。ScanNetSecurity が 10/19 に掲載した国家サイバー統括室と総務省の注意喚起は、いずれも 10/9 に出たもので範囲外。

### 国内製品の脆弱性 (JVN)

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| 2026-10-19 | JVNVU#93520490 / CVE-2026-104679 | VOCALOID6 Editor 6.13.2 以前 / ヤマハ | 細工したプロジェクトファイルを読み込むと XXE (CWE-611) が起き、端末の情報が取られたり、DoS になったりする。6.13.3 で修正。報告者は Zero 氏 | v3.1 7.1 (AV:L/UI:R) / v4.0 6.9 | [JVN](https://jvn.jp/vu/JVNVU93520490/) |

> 期間内に JVN で公開された国内製品の案件は上の 1 件だけだった (10/18〜19 は週末明けで、jvn.rdf の新規はこれのみ)。JVN iPedia (jvndb_new.rdf) は 10/19 に 378 件を登録したが、内訳は Microsoft 296、Adobe 22、Broadcom 9、Linux Foundation (Backstage) 8 などで、国内ベンダーの製品は 0 件だった。JVNDB-2026-038885 (CISA ICS 10/15) は JVNVU#96928590 として既報。
> 診断の観点 (VOCALOID6): XML 形式のプロジェクトファイルを読み込むデスクトップアプリで XXE が起きる典型例である。同じ種類の DTM / 音声合成ツールでも、プロジェクトファイルのパーサーに外部エンティティ参照の検証がされているかを確認する価値がある。

### 国内コミュニティ・研究・イベント

#### [2026-10-19] GMO サイバーセキュリティ by イエラエ「相次ぐ不正アクセスの攻撃元の多くが AI であることを確認」— 中国の開発者による自律型ペンテストツール「ARTEX」が使われていた
- **事実**: 10/14 の記事の続報である。日本企業を狙った侵害事案で攻撃元のインフラを調べたところ、AI による自律型ペネトレーションテストシステム「ARTEX」が使われていた。同社は、10/14 にフォレンジックのログから立てた「AI による攻撃の可能性が高い」という推定を裏付ける結果だとしている。
  - 1 つの攻撃元インフラが、日本企業の約 20 社を狙っていた。そのうち 9 社は同じ業種である。
  - 同じように日本企業を狙う AI 攻撃インフラが、ほかに 6 台見つかった。主な標的の業種は、デジタルギフト・小売、教育・ギフト・印刷、ポイント・マーケティング、保険・金融、EC・メディア・物流、EC である。
  - 標的とされた企業のうち 8 社は、9〜10 月にすでに漏えいを公表している。
  - 情報は法執行機関に共有した。CrowdStrike が報じた、韓国の金融機関を狙う ARTEX のキャンペーン (9 月下旬から) と同じ手口だとみている。
  - 日経は、日本向けの攻撃で ARTEX の使用が明らかになるのは初めてとみられると報じている。
- **評価**: 一連の事案について、「同じ攻撃グループが業種ごとにインフラを分けて、AI で自動的に攻めている」という見立てが、具体的なツール名と台数で示された。上のアルカディアの時系列とあわせて読むと、手順が分かりやすい。ただし、帰属 (どの国の、どの主体か) はまだ確定していない。
- 出典: [GMO イエラエ](https://gmo-cybersecurity.com/blog/20261019/) / [日本経済新聞](https://www.nikkei.com/article/DGXZQOUC198NI0Z11C26A0000000/)

#### [2026-10-19] MBSD-SOC「2026 年 9 月度の検知傾向」— Metabase の SQL インジェクション (CVE-2026-72898, CVSS 10.0) を狙う通信が 9 月に増加
- **事実**: 認証を回避して管理者権限を得られる Metabase の SQLi (8/6 公開、PoC あり) を狙う通信を、8/19 に初めて検知し、9 月に検知数が増えた。
  - 通信は `/api/session/reset_password` に細工した JSON を送るものである。
  - 攻撃元は、ブルガリア 24.1%、フランス 23.7%、オランダ 20.7%、米国 12.9%、ドイツ 4.0% の順だった。
  - 修正版は 58.24 / 59.21 / 60.17 / 61.11 / 62.9 / 63.5 である。
- **評価**: JPCERT/CC が「BI ツールや社内の管理画面も狙われている」と注意喚起したことを、観測データで裏付けている。国内では、Metabase の不正アカウント経由で漏えいした事案 (NEXT STAGE、既報) もある。
- 出典: [MBSD](https://www.mbsd.jp/research/20261019/20269-mbsd-soc/)

#### [2026-10-19] CODE BLUE 2026 が全プログラムを発表 (カンファレンスは 11/17〜18、ベルサール高田馬場)
- **事実**: 講演は約 42 本である。基調講演は ENISA の 2 名による「フロンティア AI 時代のサイバーセキュリティ」。主な講演は次のとおり。
  - 辻 知希氏「Agent2Shell」(Pwn2Own Berlin 2026 で 2 万ドルを獲得したとされる内容)
  - 松尾 和輝氏「Shade Core」(ハイパーバイザーで保護された PC への UEFI 攻撃)
  - Stav Cohen 氏と Michael Bargury 氏「PleaseFix」(エージェント型ブラウザーへのゼロクリック攻撃)
  - 「ソルト・タイフーンの影」(日本に隣接する攻撃拠点)
  - トレーニングは 11/11〜15。事前登録は 11/10 まで (カンファレンス 98,000 円)。
- **評価**: エージェント、ブラウザー、UEFI と、攻撃面の研究が中心の構成である。国内の研究者による Pwn2Own の成果発表もあり、バリアントハントの題材になる。
- 出典: [@Press (CODE BLUE 事務局)](https://www.atpress.ne.jp/news/641166) / [CODE BLUE](https://codeblue.jp/news/)

#### [2026-10-19] 帝国データバンク、情報漏えいの「経験あり」は企業の 16.2%、「分からない」も 14.8%
- **事実**: 10/9〜14 にインターネットで調査し、1,328 社が回答した。
  - 情報漏えいの発生が「ある」は 16.2% (直近 1 年以内は 5.5%)。大企業に限ると 30.2% だった。
  - 「分からない」は 14.8% で、専門家がいないため把握できないという声が出ている。
- **評価**: 中小企業には、検知する体制がないため漏えいに「気付けていない」層があることを示す数字である。委託先の管理や、お助け隊サービスの提案の背景説明に使える。
- 出典: [帝国データバンク](https://www.tdb.co.jp/report/economic/20261019-databreach/) / [ITmedia NEWS](https://www.itmedia.co.jp/news/article/2610/19/2000002390/)

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 180 (AI 技術 24 / AI セキュリティ 28 / セキュリティニュース 47 / CVE 5 種の API とベンダー advisory / 国内 約 55、重複を含む延べ数)
- 採用件数: AI技術=9 / AIセキュリティ=9 / セキュリティ=12 / CVE=12 (CVE ID は計 18) / 国内インシデント=12 (うち続報 4) / 国内政策=1 / JVN=1 / 国内コミュニティ=4
- 除外理由内訳: 古すぎ=約 50 / 重複=約 70 / 日付不明=約 3
  - 範囲外として外した主なもの: MITRE ATT&CK v20 (AI 関連技法の追加。公開は 10/13)、Broadcom の WPS の未修正 RCE (一次発表は 10/16)、OpenBSD の LPE「Big Fish」(10/16)、Recorded Future の TAG-217 (韓国の銀行への AI 支援攻撃。一次は 10/16)
  - 新事実がなく続報に入れなかったもの: Joshin、コミックシーモア、IDCF、石川コンピュータ・センター、Renta!
- 取得失敗ソース:
  - GitHub advisories API と github.com/advisories: 403 (このセッションの GitHub アクセスは対象リポジトリに限られる)。代替として OSV API と、NVD のうち GitHub が採番したエントリを使った。同じ理由で、Apache Camel の PR からマージコミットを取れず、PR URL を載せて「commit 不明」とした
  - CISA advisories の RSS: Access Denied。KEV は JSON で取得できた
  - GTIG、SpecterOps、Socket、Searchlight Cyber の RSS: パースエラー
  - HiddenLayer と Lakera のフィード: 404。VentureBeat: 429。DeepMind の RSS: 0 件。arXiv export API: 429 からタイムアウトし、rss.arxiv.org で代替
  - The Verge と BBC: WebFetch は失敗し、curl で取得。ITmedia は WebFetch で文字化けし、curl と iconv で取得
  - 国家サイバー統括室と個人情報保護委員会のニュース一覧: JS で描画されるため取得できず、トップページと WebSearch で代替
  - ふるさとチョイス: 一次の告知は公式 X のみ。ITmedia と Impress Watch で日付と内容を確認

</details>
