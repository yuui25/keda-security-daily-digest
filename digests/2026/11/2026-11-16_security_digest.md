# KEDA Daily Digest — 2026-11-16 (JST)

> 採用範囲: 公開日 2026-11-14 〜 2026-11-16
> 生成: claude-opus-5-5 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

米国の土日 (11/14〜15) をはさんだ号で、ベンダーの一次発表は少なく、CISA KEV の追加と JVN の新規公開はどちらも 0 件だった。そのぶん、週末に公開された OSS の CVE と、委託先経由の情報漏えいの続報が中心になる。
CVE では、**Cyrus SASL の SRP プラグインの認証回避 (CVE-2026-129483、CVSS 9.1)** が最も重い。RFC 5054 で必須とされるクライアント公開値の検査が抜けており、パスワードを知らなくても認証が通る。上流は 2022 年からリリースが止まっていて、配布パッケージでの修正状況はばらつく見込み。今日の深掘りで扱う。ほかに、ECDH の公開鍵を検証しない create-ecdh、末尾ドットでピンニングが外れる OkHttp、BGP 属性キャッシュの UAF で bgpd が落ちる FRRouting がある。
セキュリティ側では、Expedia (恐喝グループ n0n が約 10 億件と主張)、TSMC (クラウド事業者経由で従業員データ)、仏 Maileva (2,200 万人)、Uber (Fireworks AI 経由) と、**委託先・SaaS 経由の漏えい** が同じ週末に重なった。Kaspersky は、脆弱性を使わず vCenter の管理機能だけで ESXi 基盤を全損させた BlackNevas の事例を報告した。
AI 側では、美団が 1.6 兆パラメータの LongCat-2.5 を MIT ライセンスで公開した。PostgreSQL 19 の正式版の遅れは「LLM で見つかったバグの報告が増えすぎた」ためだと報じられた。
国内では、**京阪 HD がグループ 5 社の公式 LINE から延べ最大 22 万 4,386 人分の情報が流出した可能性** を公表した (ソニックムーブの COMSBI SaaS 版の侵害)。福岡市の公式 HP は市長選の投開票日に閲覧できなくなった。
**今日まず見るべき 2 件**: (1) Cyrus SASL を使う IMAP / SMTP / LDAP の環境で、SASL の機構一覧に `SRP` が含まれていないかを確かめる (深掘り参照)。(2) LINE 連携や CRM 系の SaaS を使う顧客がいれば、ベンダー側のサポート用アカウントがテナントをまたぐ権限を持っていないかを確かめる。

## 今日の深掘り

### Cyrus SASL の SRP 機構に認証回避 (CVE-2026-129483、CVSS 9.1): クライアント公開値 `A` に `N` を送るだけで、パスワードなしで任意ユーザーとして認証できる

- **概要 (事実)**:
  - 11/15 (UTC)、Cyrus SASL 2.1.28 以前の SRP サーバー機構に、認証回避の脆弱性 CVE-2026-129483 (CWE-287、NVD の CVSS 3.1 は 9.1 / VulnCheck の CVSS 4.0 は 9.3) が公開された。発見者は afldl 氏。oss-security (2026/q4/122) と GitHub issue #896 に報告がある。
  - 欠陥は `plugins/srp.c` の `srp_server_mech_step2()` にある。SRP では、クライアントが公開値 `A` を送り、サーバーは共有秘密 `S` を導出する。このとき SRP の仕様 (RFC 5054 ほか) は「`A mod N == 0` のときは接続を中断せよ」と定めているが、Cyrus SASL はこの検査をしていなかった。
  - このため、未認証のクライアントが `A = N` (または `N` の倍数) を送ると、共有秘密が **0 に固定** される。サーバーは 0 から導いた鍵で認証に成功し、攻撃者は**任意の既存ユーザーのパスワードを知らないまま**そのユーザーとして認証でき、セッション鍵も手に入る。
  - PoC が gist で公開済み。EPSS は本稿時点で未採点、CISA KEV にも未収録。修正コミットは `fb3724f`。

- **技術的な中身**:
  - **攻撃条件**: SRP は PAKE (パスワード認証鍵交換) の一種で、本来はパスワードの平文もハッシュもネットワークに出さないのが利点。ここでの前提は「サーバーが SASL の `SRP` 機構を有効にして広告していること」だけで、認証前に到達できる。悪用の難易度は低い。
  - **sink と結果**: `A mod N == 0` を弾かないまま `S = (A · v^u)^b mod N` の計算に進むと、`A ≡ 0 (mod N)` なら `S ≡ 0` になる。鍵導出も検証もこの `S=0` で一貫して進むため、サーバー側だけで完結して認証が通る。パスワードの事前知識・総当たり・中間者のいずれも不要で、完全な認証回避になる。
  - **影響範囲**: Cyrus SASL は Cyrus IMAP / Sendmail / Postfix / OpenLDAP など多くの MTA・ディレクトリ・IMAP サーバーのバックエンドとして使われる。ただし `SRP` 機構は既定で広告されないことが多く、実際に有効にしている環境は限られるとみられる。有効な環境では深刻。

- **背景・経緯 (背景引用)**:
  - Cyrus SASL は 2022 年を最後に新しいリリースが出ておらず、ここ 1 年のコミットはドキュメント更新のみ、という指摘が 10 月に Oracle の Alan Coopersmith 氏から oss-security に出ていた (issue #891、2026/q4 の「Unfixed vulnerabilities in Cyrus SASL」)。そこでは SCRAM の GS2 ヘッダ解析の 1 バイト OOB read (#888)、DIGEST-MD5 の `add_to_challenge()` のヒープオーバーフロー (#889、Red Hat が CVE-2026-107161 を採番) など、未修正の報告が複数挙げられていた。今回の SRP の件 (#896) もその一群で、メンテナンスが停滞しているプロジェクトの「仕様で必須の入力検証の抜け」という典型に当たる。
  - 「PAKE / DH 系で公開値を検証しない」クラスは古くから繰り返されている (small-subgroup 攻撃、invalid-curve 攻撃)。同じ穴が、各言語の SRP ライブラリ・TLS-SRP の実装・Dovecot などに水平伝播していないか確認する価値がある。

- **なぜ今これが重要か (評価)**:
  - PoC が公開済みで、攻撃条件が「`A=N` を送るだけ」と極めて単純。SRP 機構を有効にしている環境なら、認証をまるごと迂回されるので実害が大きい。
  - 上流のリリースが止まっているため、ディストリ各社のバックポートに頼ることになる。修正の有無がパッケージごとにばらつく「パッチの空白期間」が生まれやすい。
  - 診断業務では、SASL の機構一覧に `SRP` が現れる環境は珍しいので、見つけたときに高優先度で潰せる分かりやすい指摘になる。

- **読者が今日できること**:
  - 手元の IMAP / SMTP / LDAP サーバーで SASL が広告する機構を確認する: 例として SMTP なら `EHLO` 後の `250-AUTH ...` 行に `SRP` が無いか、IMAP なら `a CAPABILITY` の `AUTH=SRP` を見る。`SRP` が不要なら無効化する。
  - `rpm -q cyrus-sasl` / `dpkg -l | grep sasl` でバージョンを控え、ディストリの advisory で CVE-2026-129483 のバックポート状況を追う。
  - 自前・社内の SRP / PAKE / 独自 DH 実装があれば、`A % N == 0` (および `B`、公開鍵が曲線上か・部分群に属するか) の検査が入っているかを `git grep` で横断確認する。
- 出典: [NVD CVE-2026-129483](https://nvd.nist.gov/vuln/detail/CVE-2026-129483) / [VulnCheck Advisory](https://www.vulncheck.com/advisories/cyrus-sasl-through-2.1.28-srp-authentication-bypass-via-plugins-srp-c) / [修正コミット fb3724f](https://github.com/cyrusimap/cyrus-sasl/commit/fb3724f43dc50247ff2bf02135457d6d77031654) / [oss-security (背景: 未修正脆弱性の一覧)](https://seclists.org/oss-sec/2026/q4/122)

## AI 技術・トレンド

### [2026-11-15] 美団、1.6 兆パラメータのエージェント向けモデル「LongCat-2.5」の重みを MIT で公開。NVIDIA GPU を使わず Huawei Ascend だけで学習・推論
- **何が起きたか**: 美団 (Meituan) の LongCat-2.5 は MoE で、総 1.6 兆パラメータのうち 1 トークンあたり約 480 億が動く。入力 100 万トークン・出力最大 12.8 万トークン、画像・動画も扱う。公開されたセルフホスト手順は Huawei Ascend (Atlas A2) 194 基構成で、NVIDIA 向けはない。美団は Terminal Bench v2.1 で 88.4 (Claude Opus 5 は 89.1) と主張。API は OpenAI / Anthropic 両形式に対応し、Claude Code や Codex から使える。期間限定価格は 100 万トークンあたり入力約 0.27 ユーロ / 出力約 1.07 ユーロ。
- **なぜ重要か**: 「Anthropic 互換 API をそのまま差し替えられる、安価な中国製モデル」がまた増えた。ARTEX のような攻撃基盤で中国系モデルが主に使われている (FBI の Flash) ことを踏まえると、攻撃側の選択肢が広がる。社内で Claude Code 等の接続先 (`ANTHROPIC_BASE_URL`) を勝手に差し替えられないかの確認も要る。
- 出典: [The Decoder](https://the-decoder.com/meituan-releases-a-1-6-trillion-parameter-agent-model-that-never-touched-an-nvidia-gpu/)

### [2026-11-16] PostgreSQL 19 の正式版が約 2 か月遅れ、理由は「LLM を使ったバグ報告の急増」。β4 で SQL/PGQ など主要機能を取り下げ
- **何が起きたか**: Publickey のまとめ。PostgreSQL 19 は 11/12 に RC2、11/19 に正式版の予定 (例年は 9〜10 月)。β4 で SQL/PGQ、`FOR PORTION OF`、`MERGE/SPLIT PARTITIONS` などを取り下げた。コミッターの Robert Haas 氏は「LLM で見つけたバグを報告する人が大量にいる」、Peter Eisentraut 氏は「40 件ほどの不具合の一覧を前にすることになる」と書いている。
- **なぜ重要か**: 11/12 の 52 件一括修正と同じ流れ。成熟 OSS でも AI で古いバグが大量に出る前提で、CVE 追跡とパッチ適用の体制を見直す契機になる。深掘りの第 2 候補。
- 出典: [Publickey](https://www.publickey1.jp/blog/26/postgresql_194ai.html)

### [2026-11-16] Cloudflare、AI エージェント向けの軽量ヘッドレスブラウザ「Kitesurf」を Apache 2.0 で公開。Chromium 不使用、Rust + WASM
- **何が起きたか**: Cloudflare が 11/13 に GitHub 公開 (Changelog)。HTML/レイアウトは Blitz、CSS は Stylo、JS は Boa (WASM 上)、PDF 生成は Krilla。Chrome DevTools Protocol 対応で Puppeteer から接続でき、CPU・メモリ効率が Chromium の 3〜7 倍だと主張。
- **なぜ重要か**: エージェント用ブラウザに非 Chromium 実装が加わる。JS エンジンが Boa のため、Chromium 前提のサンドボックス・サイト分離がどこまで同じに働くかは未知数。悪性ページの読み込み挙動と CDP の口の露出が、新しい診断対象になる。
- 出典: [Publickey](https://www.publickey1.jp/blog/26/cloudflareaikitesurf.html)

### [2026-11-15] [続報] NVIDIA 関連: Megaspeed が中国向けに約 120 億ドル分のチップ注文を仲介と WSJ 報道。米議会で輸出規制強化の声
- **何が起きたか**: WSJ が見た文書によると、Huang 氏の元交際相手が持つ Megaspeed が 2024 年 3 月〜2025 年 6 月に、中国企業向けに総額約 120 億ドルの注文を仲介した。Megaspeed は「合法」と反論。Schumer 上院議員らが規制強化と証言を求め、Remote Access Security Act が再注目された。TechCrunch は NVIDIA の CSO が 8 月に交代していた点にも触れた。
- **前回からの差分**: 11/15 号はアジア各国の反応だった。今回は迂回の規模と、議会の立法の動きが新しい。
- **なぜ重要か**: クラウド経由の GPU 利用 (リモートアクセス) にも規制が及べば、利用者確認 (KYC) やログ保持の義務が増え、AI 基盤構成に影響する。経営幹部が諜報の標的になる内部脅威の例でもある。
- 出典: [The Verge](https://www.theverge.com/ai-artificial-intelligence/1033984/congress-export-rules-ai-chips-china) / [TechCrunch](https://techcrunch.com/2026/11/14/where-was-nvidias-security-team/)

### [2026-11-15] 米国防総省、AI 統括部署 CDAO を「Super Intelligence Office」に改称、ドメインを SI.mil へ
- **何が起きたか**: 大統領令 14434 (政府文書で「AI」の代わりに「Super Intelligence / SI」と呼ぶよう指示) を受け、11/13 に改称。元 AWS で Project Maven を率いた Cameron Stanley 氏が Chief Super Intelligence Officer に。公開資料・調達情報・提携窓口を SI.mil に移した。
- **なぜ重要か**: 中身より呼称の変更だが、ドメイン移転は見逃せない。調達窓口が変わる時期は、類似ドメインや偽の調達メールのフィッシングが起きやすい。米政府の AI 調達を追うなら SI.mil を監視対象に。
- 出典: [SecurityWeek](https://www.securityweek.com/pentagon-renames-cdao-super-intelligence-office/)

### [2026-11-14] Stanford、凍結した LLM に「16 個のメモリトークン」で文書集合を渡すモジュール「Memorilla」を Apache 2.0 で公開
- **何が起きたか**: Jure Leskovec 氏の SNAP グループの研究。学習するのは 1.94 億パラメータのメモリモジュールのみで、エンコーダー (Qwen3-Embedding-4B) とデコーダー (Qwen3-8B) は凍結のまま。FactKG で全文書投入の 80.43% に対し 84.33%、文書トークンは 108 分の 1 と主張。コード・チェックポイントを公開。
- **なぜ重要か**: RAG と違い「何を渡したか」が人の読めるテキストとして残らない。毒入り文書を入れられたときの監査・検知が難しく、導入時は元文書への追跡性を担保する必要がある。
- 出典: [MarkTechPost](https://www.marktechpost.com/2026/11/14/stanford-memorilla-memory-system-16-memory-tokens/)

### [2026-11-14] Cmpnd、DSPy で「重み空間プログラミング」をする「dspy-wsp」を MIT で公開: 大 LLM が小モデルの重みを直接書き換える
- **何が起きたか**: 最適化機能 `WeightSpace` は勾配も学習データも使わず、文章の目標に合わせて大モデル (GPT-6-Astra) が 0.6B〜9B のモデルの層やヘッドを書き換える。5〜10 ドル分の呼び出しで判断用モデルの成績が上がり、最大は d1-omni-600M で 50.9% → 69.1%。1 回の実行に 78〜167 分。
- **なぜ重要か**: 学習記録を残さず重みを変えられるため、モデルのサプライチェーンでは「小さな差分パッチ」で振る舞いが変わりうる。重みのハッシュ確認と差分監査の重要性が増す。
- 出典: [MarkTechPost](https://www.marktechpost.com/2026/11/14/cmpnd-dspy-wsp-weight-space-programming/)

### [2026-11-15] [続報] Claude Fable 5.2 が「画像を生成せず描く」: 1,000〜2,000 行の Python で仮想の筆を動かす
- **何が起きたか**: Anthropic の Jake Eaton 氏が Fable 5.2 の作例を X に投稿。外部の画像モデルを使わず、塗料をシミュレーションするエンジンを Python で動かして描く (駐車場の絵は約 70 万回の筆の動き)。The Decoder によると社内の RoboDojo Sim で Fable 5.2 が 64.9%、GPT-6 Astra が 29.8%。実機のロボットアームでは速さ・細かさで GPT-6 Astra に劣ったという。
- **なぜ重要か**: 「長いコードを生成・実行し、結果を見て直す」動き方の例。実行権限を持つエージェントが数千行のコードを自ら書いて動かすため、サンドボックス設計が欠かせない。重要度は低め。
- 出典: [The Decoder](https://the-decoder.com/anthropics-claude-fable-5-2-doesnt-generate-images-it-paints-them/)

### [2026-11-14] Nathan Lambert 氏「Jensen のいないオープンソース AI」: 米オープンモデル陣営は最大の後ろ盾を失う
- **何が起きたか**: Interconnects の論考。Huang 氏はオープンモデルへの投資と政治的な防波堤を担ってきたが、その支えが細る見込みだという。同氏は「人気の中国製オープンウェイトモデルが原因の大きなハッキングがいつか起きる」とし、その際に雑な規制が作られることを懸念している。
- **なぜ重要か**: オープンウェイトが規制対象になるかは、社内でモデルを自前で動かす構成やモデル調達に響く。意見記事なので扱いは軽め。
- 出典: [Interconnects](https://www.interconnects.ai/p/open-source-ai-without-jensen)

### [2026-11-16] 国内: 日経クロステック「IT 業界の倒産が過去 10 年で最多、大手は好調で二極化」
- **何が起きたか**: 情報サービス業の倒産が中小中心に過去 10 年で最多のペースで増える一方、大手 SIer は好調。AI で開発効率が上がり、多重下請け構造が崩れ始めたという (本文は有料)。
- **なぜ重要か**: 委託先の倒産・縮小で、保守されないシステムや引き継ぎのない資格情報が増えうる。委託先管理と契約終了時の権限回収手順を確かめる根拠になる。
- 出典: [日経クロステック](https://xtech.nikkei.com/atcl/nxt/column/18/03792/110500001/)

## AI セキュリティ

### [2026-11-15] [続報] FBI の ARTEX 警告: ConnectWise Cloud Backup 経由の攻撃 (下流 M365 テナント 2,250 超) も事例に。MalwareMustDie が検知シグネチャ集 MMD-072 を公開
- **何が起きたか**: FBI の 13 ページの Flash Alert は、既報の攻撃を ARTEX 関与の事例として整理した。10 月の ConnectWise Cloud Backup (旧 SkyKick) のアプリ ID 悪用 (Microsoft は Storm-0940 とし 2,250 超のテナントへ認証試行)、韓国の銀行への攻撃 (ARTEX と Claude Code の併用)、Vapor Panda の 14 か国 200 超の組織への攻撃。MalwareMustDie が 11/13 に IOC と対応手順を含む検知ルール集を公開した。
- **前回からの差分**: 11/15 号は Flash Alert の概要と Amazon の報告だった。今回は、FBI が挙げた個別の攻撃と、すぐ使える検知ルールが新しい。
- **なぜ重要か**: SaaS 連携アプリの ID を乗っ取られると多数のテナントへ広がる。M365 診断ではエンタープライズアプリの権限棚卸しを必ず入れたい。検知ルールは SOC ですぐ試せる。悪用は確認済み。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/fbi-warns-artex-ai-hacking-tool-is-powering-global-cyberattacks/) / [MalwareMustDie](https://blog.malwaremustdie.org/2026/11/mmd-072-2026-artex-detection-signature.html)

### [2026-11-14] WIRED「AI でランサムウェアが急増」: 夏のリーク掲載は約 3,000 件で春比 20〜40% 増。日本では AI 生成の日本語詐欺が急増
- **何が起きたか**: Halcyon の Cynthia Kaiser 氏 (元 FBI) は「最近の増加は米国外への攻撃が中心で一部は AI のせい」と述べ、Recorded Future の Allan Liska 氏は「AI はフィッシングと交渉に使われるが、成功するグループは今も人が操作」とした。7〜9 月に被害を主張したグループは約 111。記事は、日本で AI により自然な日本語の詐欺が増えている例を挙げた。
- **なぜ重要か**: 日本の組織にとって「言葉の壁」という防御がなくなりつつある。訓練用フィッシングの文面を AI が書く水準に合わせて見直す必要がある。
- 出典: [WIRED](https://www.wired.com/story/beware-the-new-ai-fueled-ransomware-boom/)

### [2026-11-15] 週末の AI 関連 CVE: WordPress の MCP サーバープラグインで権限昇格 (CVE-2026-125771)、AI Engine で格納型 XSS (CVE-2026-125804)、vLLM で競合状態 (CVE-2026-129356)
- **何が起きたか**: AtlasAiDev の ai-workflow-automation-ai-agent-hub は 2.0.3 以前に権限昇格 (CVSS 7.2、2.0.4 で修正、Patchstack が 11/13 公開・NVD 登録 11/15)。Meow Apps の AI Engine は 3.9.3 以前に未認証の格納型 XSS。vLLM 0.30.0 / 0.31.0 は `single_type_kv_cache_manager.py` に競合状態 (0.32.0 で修正)。
- **なぜ重要か**: WordPress に MCP の口を足すプラグインは、エージェント向け API に権限境界の不備が出やすい典型。WordPress 診断で AI 系プラグインを一覧して確認する項目に入れたい。
- 出典: [Patchstack (CVE-2026-125771)](https://patchstack.com/database/wordpress/plugin/ai-workflow-automation-ai-agent-hub/vulnerability/wordpress-mcp-server-for-wordpress-plugin-2-0-3-privilege-escalation-vulnerability) / [vLLM 修正コミット](https://github.com/vllm-project/vllm/commit/e687a251bb056fa527846633f7a1b0a6c0f42374)

### [2026-11-15] 国内コミュニティ (Zenn):「見えない文字でプロンプトに指示を隠す手口と、ブラウザだけで見つける仕組み」
- **何が起きたか**: タグ文字 (U+E0000〜E007F)、ゼロ幅文字の 0/1 符号化、異体字セレクタの 3 種でプロンプトに指示を隠す手口を、復元コード付きで解説。NFKC 正規化後の正規表現照合も実装し、`\s*` を使った正規表現が 20 万字の空白で ReDoS になった失敗も共有している。
- **なぜ重要か**: プロンプトインジェクションの診断で、入力検査の観点一覧としてそのまま使える。重要度は低め。
- 出典: [Zenn](https://zenn.dev/ikasumi_works/articles/677c46799dfda4)

## セキュリティニュース

### [2026-11-14] Expedia が委託先経由のサプライチェーン侵害を認める。恐喝グループ「n0n」は約 10 億件の旅行者データを盗んだと主張
- **何が起きたか**: Security Affairs (Skift / Forbes を引用) によると、Expedia は「侵害されたサードパーティのデータ基盤事業者」経由で侵入されたと認めた。n0n の主張はロイヤルティ 8.3 億件、旅行者プロファイル 5,800 万件、トークンを含むアカウント 3.33 億件、ソースコード。Wiz と Sentra は、Google Cloud のパートナー Qubole の盗まれたベンダーキーが入口だったとした。n0n は 9 月以降 224 件の攻撃を主張する、ランサムを使わない恐喝グループ。
- **なぜ重要か**: ビッグデータ基盤事業者の長期有効キー 1 本で複数顧客の環境に入られた事例。外部データ処理 SaaS に渡すキーの権限と有効期限を確認する価値がある。侵害は確認済み、PoC は該当しない。
- 出典: [Security Affairs](https://securityaffairs.com/203062/cyber-crime/extortion-group-claims-theft-of-nearly-one-billion-expedia-traveler-records.html)

### [2026-11-15] TSMC、従業員の個人データ流出を確認。原因は「利用するクラウド事業者のシステム」
- **何が起きたか**: BleepingComputer によると、TSMC は SEC 提出書類で現・元従業員のデータ流出を認めた。流出データは「クラウド事業者のシステムに保存されたデータ」と一致し、自社システム侵害の証拠はないとする。出品者は 11/8 に 499 行のサンプルを公開、本体は 6.9GB・従業員 46,000 件 (国民 ID、住所、銀行情報) と主張した。
- **なぜ重要か**: 自社ではなく委託先 SaaS/クラウドに預けたデータからの流出で、Fireworks AI や Qubole と同型。悪用段階は「データ販売・流出」、侵入手口は不明。PoC は該当しない。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/tsmc-employee-data-breach-linked-to-cloud-provider/)

### [2026-11-15] 仏 La Poste 子会社 Maileva の侵害で 2,200 万人の氏名・住所が流出。医療費請求書の中身も読まれた可能性
- **何が起きたか**: Security Affairs (AFP / Le Monde を引用) によると、9 月中旬の侵害で、Maileva の顧客企業が文書を送った受取人 2,200 万人の氏名・住所が盗まれた。銀行情報は含まれない。医療費督促を代行する Kiwee.care の郵送物の一部は本文も読まれ、請求番号・治療日・金額が漏れた可能性。CNIL に届け出て刑事告訴、司法捜査中。
- **なぜ重要か**: 被害者の多くは Maileva を知らず、本人通知が届きにくい。医療費請求を装った精巧なフィッシングが増える恐れ。侵入手口は未公表。
- 出典: [Security Affairs](https://securityaffairs.com/203126/data-breach/data-breach-at-la-poste-subsidiary-maileva-affects-22-million-people-in-france.html)

### [2026-11-14] [続報] Fireworks AI の侵害の波及: Uber がドライバーの運転免許情報の流出を通知
- **何が起きたか**: Cyber Security News (TechCrunch を引用) によると、Uber は Fireworks AI 上の自社アカウントのデータが盗まれたとして 11/10 付で通知を開始。10/9 に Fireworks から連絡、10/13 に Uber データへのアクセスを確認。州への届け出はマサチューセッツ 2,567 人、サウスカロライナ 3,430 人、ロードアイランド約 1,873 人。全体人数は未公表。
- **前回からの差分**: Cursor・Notion に続き、同じ委託先から被害企業がまた 1 社。
- **なぜ重要か**: LLM の推論・学習事業者に渡したデータ (traces) から個人情報・資格情報が出る同じ連鎖が続く。悪用は未確認と Uber は述べる。
- 出典: [Cyber Security News](https://cybersecuritynews.com/uber-confirms-data-breach/)

### [2026-11-14] Microsoft、11/12 の M365 障害に便乗したフィッシングを観測。本物のインシデント番号 EX1550543 を引用
- **何が起きたか**: Microsoft Threat Intelligence は 11/13 から、サービス正常性通知を装い「障害中に保留されたメールは 24 時間で削除される」と復元リンクを踏ませるメールを観測。件名は「Outage – [6 文字コード]」、送信元は `moments-notice[.]com` ほか、SendGrid のクリック追跡経由で `reallifeaccounting[.]com/themelist0.html` へ転送。米国の複数業種に着弾。資格情報が実際に盗まれたかは未確認。
- **なぜ重要か**: 本物の障害の直後に本物のインシデント番号を使う手口は、検知も利用者判断も難しい。Defender の EmailEvents / UrlClickEvents で IOC をすぐ検索できる。攻撃は進行中、PoC は該当しない。
- 出典: [Cyber Security News](https://cybersecuritynews.com/active-password-stealing-attack-microsoft-365/)

### [2026-11-14 報道 / Securelist 11-13] BlackNevas が vCenter の Host Profiles で ESXi の SSH を有効化し、仮想基盤とバックアップを 10 日で全損 (Kaspersky GERT)
- **何が起きたか**: GBHackers による Securelist 報告の要約。脆弱性は未使用。攻撃者は正規アカウントで vCenter に入り、バックアップサーバーの秘密情報を抜いたうえで、MeshAgent と Ligolo-ng を設置 (systemd の `vmware-vdma.service`、通信先 `api.cloudvflare[.]com`)、Host Profiles の修復で TSM-SSH を有効化、`/tmp/esx64 ... /wipe` で各 VMDK 先頭約 2KB を上書きした。ESXi 4 台、全 VM、vCSA 2 台、バックアップを破壊。
- **なぜ重要か**: 正規の管理機能だけで仮想基盤が全損した事例で、vCenter を Tier 0 として扱う根拠になる。被害は実在、ワイパーは Trigona 系統。PoC は該当しない (手口のみ)。深掘りの候補でもある。
- 出典: [GBHackers](https://gbhackers.com/blacknevas-ransomware-attacks-vmware-esxi-servers/) / [Securelist](https://securelist.com/esxi-ransomware/121959/)

### [2026-11-15] スーパーの冷凍設備コントローラー Danfoss AK-SM800A に、未認証 RCE の 0-day が 6 件 (Midnight Blue)
- **何が起きたか**: Cyber Security News によると、Midnight Blue の Carlo Meijer 氏が 5.3.2 までの全ファームで 6 件を発見。`strcpy` による stack overflow で CVE は未採番、対象プログラムは root で動作し stack canary も PIE もない。CERT-FR の緩和策 (session control の strict) を有効にしても、ログイン処理 (`sm_fcgi_app`) の 1 件は最新ファームで通る。secure boot がなく、工場出荷時に戻しても残る implant を置けるという。
- **なぜ重要か**: ブログ題は「Don't bother patching」で、インターネット公開をやめることが唯一の対策とする。この 0-day 自体の悪用報告はなく PoC は非公開だが、同製品群への攻撃は欧州で継続中。既報の Copeland XWEB EVO (11/13) とは別件。
- 出典: [Cyber Security News](https://cybersecuritynews.com/supermarket-refrigeration-systems-0-day/) / [Midnight Blue](https://www.midnightblue.nl/blog/multiple-rce-danfoss-aksm800a)

### [2026-11-14〜15] イタリアの Garante、Meta に 8.05 億ユーロの制裁金。Android の Facebook が既定で端末のギャラリーにアクセス
- **何が起きたか**: The Hacker News と SecurityWeek (SW は 8.87 億ドルと表記) によると、写真の投稿候補を出す機能が既定で有効で、明示の同意なく写真・動画・メタデータを読んでいた。根拠はイタリアのプライバシー法 122 条 (EU の ePrivacy 指令を国内法化)。60 日以内に既定で無効化し、機能ごとに別の同意を求めるよう命じられた。Meta は控訴の方針。
- **なぜ重要か**: 「アプリ全体で 1 つの権限」を複数目的に使う設計が、それだけで違法とされた例。モバイルアプリの診断・設計レビューで、権限と目的の対応を確認する根拠になる。PoC は該当しない。
- 出典: [The Hacker News](https://thehackernews.com/2026/11/italy-fines-meta-805-million-over.html) / [SecurityWeek](https://www.securityweek.com/meta-fined-887-million-in-italy-over-android-gallery-photos-and-videos-on-facebook/)

### [2026-11-14] Perl の JSON::XS 4.05 未満に 7 件の CVE。Dancer の CVE-2015-10149 も同日公開 (CPANSec)
- **何が起きたか**: CPAN Security Group の oss-sec 投稿。JSON::XS は `incr_parse` で 1 バイト断片を追加すると heap の 1 バイト先に書く CVE-2026-129114、`allow_tags` の `encode_rv` で解放済みスタックを読む CVE-2026-129115、NUL バイトで `max_size` を素通りさせる CVE-2026-124536 など 7 件 (4.05 で修正)。Dancer 1.3400 未満の CVE-2015-10149 は、Cookie のセッション ID を検証せずセッションエンジンに渡し、エンジン次第でパストラバーサルやコマンド注入につながる。
- **なぜ重要か**: JSON::XS は Perl の Web アプリ・API で広く使われ、`incr_parse` で外部入力を逐次処理するコードは要監査。Dancer の件は HTTP::Session (CVE-2011-10042) と同じ「セッション ID 未検証」型。悪用報告はなく、exploit も未公開。
- 出典: [oss-sec (JSON-XS)](https://seclists.org/oss-sec/2026/q4/706) / [oss-sec (Dancer)](https://seclists.org/oss-sec/2026/q4/712)

### [2026-11-15] [続報] ARTEX: MalwareMustDie が公開した検知ルール一式が加わる (AI セキュリティ欄と同件)
- **何が起きたか**: 上の「AI セキュリティ」欄で詳述。FBI の Flash と合わせ、MalwareMustDie のネットワーク・ID 悪用・クラウド操作・ファイル・自動化のパターン別の検知ルールが公開された。
- **なぜ重要か**: FBI の IOC (IP など) は陳腐化しやすいが、振る舞いベースの検知ルールはそのまま試せる。悪用は確認済み。
- 出典: [BleepingComputer](https://www.bleepingcomputer.com/news/security/fbi-warns-artex-ai-hacking-tool-is-powering-global-cyberattacks/)

### [2026-11-14〜15] 短信
- **GPAC / MP4Box**: CVE-2026-124030 / -124031 は XMT 処理の型の取り違え、CVE-2026-128240 は UAF。26.07.0 まで影響し、ローカルファイルを開かせる DoS。RCE は示されていない。[oss-sec](https://seclists.org/oss-sec/2026/q4/709)
- **libdca** (VideoLAN の DTS デコーダー): scale factor の解析で配列の範囲外読み取り。開発終了で修正はないが、ディストリには残る。[oss-sec](https://seclists.org/oss-sec/2026/q4/713)
- **YARA-X 1.23.0**: 改善 4 件・バグ修正 16 件のリリース。[SANS ISC](https://isc.sans.edu/diary/rss/33496)

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-11-14 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-129483 | Cyrus SASL SRP (≤2.1.28)／11-15 | CWE-287 / 9.1 | SRP サーバーが公開値 `A mod N == 0` を拒否しない → `srp_server_mech_step2` の鍵導出に到達 → 共有秘密が 0 に固定され、パスワードなしで任意ユーザー認証 | [diff](https://github.com/cyrusimap/cyrus-sasl/commit/fb3724f43dc50247ff2bf02135457d6d77031654) | **Critical / PoC公開**、oss-sec q4/122 |
| CVE-2026-129319 / GHSA-32q7-f779-hw5r | create-ecdh (npm, ≤4.0.4)／11-14 | CWE-20 / 5.9 | 相手の公開鍵が曲線上か・素数位数の部分群かを検証しない → `computeSecret`/`setPublicKey` がそのままスカラー倍 → 静的鍵なら invalid-curve / small-subgroup で秘密鍵が漏れる | [diff](https://github.com/browserify/createECDH/commit/1cfaf332773237e5fea4b51a2ad3efab4c22bec1) | EPSS 0.0025 / 横展開しやすい |
| CVE-2026-129482 | OkHttp CertificatePinner (≤5.5.1)／11-15 | CWE-295 / 4.8 | ホスト名が末尾ドット付き (`example.com.`) → `Pin.matchesHostname` が正規化せず照合 → ピンが一致せず検査が飛び、CA 発行の別証明書で MITM | [diff](https://github.com/lysine-dev/okhttp/commit/30aa589761a9b4f5fe84c00e21e5ab44b22bd7c1) | 横展開しやすい (上流確認要) |
| CVE-2026-129456 | FRRouting bgpd (修正前)／11-14 | CWE-415,416 / 7.7 | `soft-reconfiguration inbound` の neighbor から Tunnel Encap 属性 (type 23) 受信 → intern キャッシュの再利用判定が常に真 → 参照を取らず sub-TLV 共有 → route 置換/withdraw で UAF と二重解放、bgpd が abort | [diff](https://github.com/FRRouting/frr/commit/5c241056777b27b209bc89326f0061ec6d5e0924) | eBGP から到達可能 |
| CVE-2015-10149 | Perl Dancer (<1.3400)／11-14 | CWE-1286 / – | セッション Cookie の値を文字検証なしで session id にする → エンジンがファイルパス/memcached/クエリに使う → パストラバーサルやコマンド注入 | [diff](https://github.com/PerlDancer/Dancer/commit/5a68fddbaef903fd3bd58517ce585cde986716e4) | HTTP::Session (CVE-2011-10042) と同型 |
| CVE-2026-129114 ほか 6 件 | JSON::XS (Perl, <4.05)／11-14 | CWE-787 ほか / – | `incr_parse` で 1 バイト断片を足すと heap を 1 バイト先に書く / `allow_tags` で解放済みスタック読み取り / NUL で `max_size` 素通り | [advisory](https://seclists.org/oss-sec/2026/q4/706) (commit 不明) | 広く利用 |
| CVE-2026-129477 | Assimp glTF/glTF2 importer (≤6.0.6)／11-15 | CWE-22 / 5.5 | glTF の `buffers[].uri` に `..` や絶対パス → 外部バッファ読み込み sink に到達 → ローカルファイルが頂点データに混入 | [diff](https://github.com/assimp/assimp/pull/7027) | glTF ローダー全般に横展開候補 |
| CVE-2026-129485 / GHSA-jwh8-j584-79hp | Kroki BlockDiag 系 (<0.36.0)／11-15 | CWE-918 / 5.8 | 未認証の図ソースで node の icon/background に URL/パス → レンダラがそのまま取得 → 内部サービス/メタデータへ SSRF、ローカル画像読み取り | [diff](https://github.com/yuzutech/kroki/commit/becd3b4a86754cb08d0fe54f65e92a6cab542409) | SSRF |
| CVE-2026-129355 | sigoden dufs WebDAV COPY (≤0.46.0)／11-15 | CWE-285,863 / 6.5 | WebDAV COPY の Destination パスの権限チェック不備 → `server.rs` のコピー処理に到達 → 権限外パスへ書き込み | [diff](https://github.com/sigoden/dufs/commit/fba13dffb9c65b5e5e26419f64de709200277a04) | EPSS 0.0059 (本日最高) |
| CVE-2025-71470 | MicroQuickJS (commit 99eed3f 前)／11-15 | CWE-125 / 5.5 | `JS_Call` がフレーム準備中の例外で `ctx->sp`/`fp` を更新しない → `build_backtrace` が古い fp を辿る → 境界外読み取りでクラッシュ | [diff](https://github.com/bellard/mquickjs/commit/99eed3f94cb66ea7e02fd3472ca7374dee31bb89) | PoC 公開 |
| CVE-2026-126299 / GHSA-89p3-fcch-88ph | NLTK CCG lexicon `fromstring` (PyPI)／11-14 | CWE-400,407 / High | 括弧や演算子の連鎖を含む入力 → パーサが再走査を繰り返す → 計算量が二次になり CPU DoS | [diff](https://github.com/nltk/nltk/commit/0bb5b947bd235b950cf2f90e893a498e16da0fe3) | EPSS 0.0058 |
| CVE-2026-129432 | Ettercap `dissector_mountd` (≤0.8.5.1)／11-14 | CWE-125 / 6.5 | RPC credential とディレクトリ長を終端ではなく単独で検証 → memcpy/表示処理 → ヒープ境界外読み取り | [diff](https://github.com/Ettercap/ettercap/pull/1341) | SOCKS5 版 CVE-2026-129431 も同型 |

(KEV は本日の採用期間 11/14 以降の追加なし。カタログ最新は 11/13 追加の CVE-2026-114713 (UnrealIRCd)、CVE-2026-123039 (Check Point)。いずれも既報)

### 今日の CVE 所感
- **プロトコル仕様で必須の入力検証が抜けているクラス** が目立つ。SRP の `A mod N ≠ 0` (Cyrus SASL)、ECDH の点が曲線上か・部分群に属するかの検証 (create-ecdh) は、PAKE / DH 系の独立実装へ広く横展開できる。他言語の SRP ライブラリ・TLS-SRP・Dovecot、純 JS/Python の ECC 実装 (elliptic 派生など) で `A % N == 0` や `validatePublicKey` の有無を `git grep` で確認する価値がある。最優先は Cyrus SASL。
- **ホスト名の正規化漏れによる照合回避** (OkHttp の末尾ドット) は、他の HTTP クライアントのピンニング・HSTS・許可リスト照合にも同型があり得る。
- **ファイルフォーマットの URI 参照からローカルファイルを読む / SSRF するクラス** (Assimp glTF の buffer uri、Kroki の icon) は、three.js・tinygltf・cgltf などの glTF ローダーや図レンダラに広がる候補。
- **セッション ID を検証せず保存層へ渡すクラス** (Dancer) は HTTP::Session の既出 CVE と同型。他フレームワークのファイル/memcached 型セッションストアでも確認する価値がある。
- FRR の UAF は「自分自身と比較するため常に真になる」キャッシュ判定のロジックバグで、diff として読み応えがある。GitHub API がこのセッションでは 403 のため、修正コミットの中身までは未確認 (リンクは NVD の references)。OkHttp の参照先は `lysine-dev/okhttp` で square/okhttp ではない点に注意 (上流での修正状況は要確認)。

## 日本国内のセキュリティ動向

### 国内インシデント・事故

### [2026-11-14] 京阪ホールディングス: LINE 連携 SaaS「COMSBI (SaaS 版)」の侵害で、グループ 5 社の公式 LINE から延べ最大 22 万 4,386 人分の情報が流出した可能性
- **何が起きたか**: 京阪 HD が 11/14 付 PDF で公表。11/11 に提供元のソニックムーブから報告を受けた。アカウント別の最大件数は、京阪電気鉄道「京阪電車ファン情報」が LINE 表示名・プロフィール画像 URL・LINE ユーザー ID で 26,914 名、京阪流通システムズ「京都タワーサンド」が LINE 情報 90,550 名、同「枚方モール」が生年月日・性別 35,025 名・LINE 情報 46,957 名、京阪百貨店が氏名/電話/メール/住所/生年月日/性別のいずれか 28,000 名・LINE 情報 51,223 名、京阪ホテルズ&リゾーツが計 1 万名規模。クレジットカード情報は保持せず、二次被害は未確認。ソニックムーブの公表では、11/9 23:04 に運用・サポート用の社内アカウントの認証情報で第三者が管理画面にログインし、複数顧客を操作できる権限を悪用、クラウド環境にも侵入して設定情報と認証情報を取得。7:36 に検知し 9:17 までに遮断。今後、管理画面の 2 段階認証の必須化と接続元制限を実施。
- **なぜ重要か**: 11/14 号のヒューマンアジャストと同じ COMSBI (SaaS 版) の件で、利用企業ごとの公表が続く。原因はベンダーのサポート用アカウントが複数テナントにまたがる権限を持っていたこと。マルチテナント SaaS の診断では、運用者アカウントの権限範囲と MFA・接続元制限を必ず確認したい。
- 出典: [京阪ホールディングス (2026-11-14, PDF)](https://www.keihan-holdings.co.jp/corporate/info/release/assets/261114_keihan-holdings.pdf) / [ソニックムーブ](https://sonicmoov.com/news/5ttj9ndzh) / [京都新聞 (2026-11-14)](https://www.kyoto-np.co.jp/articles/-/1826087)

### [2026-11-15] 福岡市: 市長選の投開票日に、公式ホームページと選管ページが 13 時すぎから閲覧できなくなる
- **何が起きたか**: 11/15 の 13 時すぎから福岡市の公式 HP が閲覧できなくなり、市選管の選挙関連ページもすべて見られなくなった。開票が始まる 20 時時点でも未復旧。市広報課は「HP が利用するクラウドサービスに障害が起きたとみられる」と説明し、原因は調査中。庁内システムと開票作業への影響はないとし、市は X で選挙情報を発信した。当日の市長選は 13 人が立候補し全員が法定得票に届かず再選挙に。攻撃かどうかの発表はない。
- **なぜ重要か**: 選挙の日に自治体サイトが停止した。原因が DDoS か、クラウド障害か、設定誤りかで意味が大きく変わるため続報を追う価値がある。選挙情報の発信を単一クラウドに頼るリスクの例でもある。
- 出典: [読売新聞 (2026-11-15)](https://www.yomiuri.co.jp/national/20261115-GYT1T00142/) / [朝日新聞 (Yahoo!, 2026-11-15)](https://news.yahoo.co.jp/articles/1a602a08d75e66435c4e78e2d67276d6ff4c5849)

> 補足: 11/13 公表の大型案件 (ヤマダデンキ最大約 350 万件、京成スカイライナー約 337 万件、大阪公立大第 6 報約 17 万人、読売巨人軍 CLUB GIANTS 約 80.7 万件など) は、各社の公表日が採用期間外のため本号では見送った。

### 国内の注意喚起・ガイドライン・政策

### [2026-11-14 報道] JPCERT/CC: AI を悪用した攻撃の拠点とみられるサーバーを、世界で約 1,000 台確認 (共同通信)
- **何が起きたか**: 共同通信の 11/14 報道。JPCERT/CC は 10 月上旬から海外のセキュリティ企業と共同で調べ、10 月以降に AI で Web サイトの弱点を探し侵入を図るとみられるサーバーを約 1,000 台確認した。捕捉したファイル構成と AI ツールの稼働状況を分析。きっかけは JPCERT/CC が 10 月に公表した「連続不正アクセス事案の攻撃手法に関する調査」で、APK 解析ツール (Blutter、jadx) による非公開 API の特定、SSRF の自動試行、Jenkins・MySQL への攻撃、EDR 回避などを報告している。JPCERT/CC 自身の新しい公表文は確認できなかった。
- **なぜ重要か**: 国内の連続不正アクセスの波が、モバイルアプリ解析から非公開 API を突く手口で進んでいることを、国の調整機関の調査が裏付けた形。スマホアプリのバックエンド API の認可 (IDOR/BOLA) と SSRF は、診断で優先して見るべき箇所。
- 出典: [東京新聞 (共同, 2026-11-14)](https://www.tokyo-np.co.jp/article/528200) / [JPCERT/CC ブログ (2026-10-15, 背景)](https://blogs.jpcert.or.jp/ja/2026/10/web_api_attacks.html)

### [2026-11-15] 上野厚労相が、1 月にサイバー攻撃を受けた日本医科大学武蔵小杉病院を視察。「院内の情報システム部門では対応できない事案が増える」
- **何が起きたか**: 上野厚労相は 11/15、川崎市の日本医科大学武蔵小杉病院を視察した。同病院は 1 月の攻撃で患者約 13 万人分の個人情報が流出している。上野氏は記者団に「病院の情報システム部門で対応できない事案が増える恐れがある」と述べ、外部の専門人材の活用と職員教育の徹底を訴えた。
- **なぜ重要か**: 厚労省が医療機関のセキュリティ対策を外部人材に頼る方向を示した。病院向けの診断・インシデント対応 (IR)・外部 CISO の需要につながる可能性がある。
- 出典: [読売新聞 (2026-11-15)](https://www.yomiuri.co.jp/politics/20261115-GYT1T00154/)

### [2026-11-15] 読売新聞の世論調査: サイバー攻撃への「ブロッキング」に賛成 77%、政府の対応を「十分」と思う人は 10%
- **何が起きたか**: 読売新聞は 11/13〜15 に全国世論調査を実施。流出した個人情報の悪用を防ぐため特定サイトへの接続を通信事業者が遮断する「ブロッキング」をサイバー攻撃にも使えるようにすることに 77% が賛成 (反対 11%)。政府がこれまで十分に対応してきたと「思わない」は 80%。ブロッキングは「通信の秘密」との兼ね合いでこれまで児童ポルノにしか認められておらず、10 月末には総務省が GMO の件の攻撃者サイトのブロッキングを通信各社に要請したと報じられている。
- **なぜ重要か**: 世論の後押しで、通信の秘密との調整や法改正の議論が進む可能性がある。能動的サイバー防御に関わる制度の動きとして追っておきたい。
- 出典: [読売新聞 (2026-11-15)](https://www.yomiuri.co.jp/election/yoron-chosa/20261115-GYT1T00216/)

### 国内製品の脆弱性 (JVN)

> 採用期間 (11/14〜16) に JVN / JVN iPedia で新しく公開された脆弱性は **0 件**。JVN の RSS の最新は 11/13 12:00 の JVN#76799957 (YouTrack、既報)。JVN iPedia の新着も、収録エントリの発行日は最新でも 11/13 だった。月曜 (11/17) の公開分はこの調査の後に出る見込み。

| 公開日 | 識別子 (JVN / CVE) | 製品・ベンダー | 概要 (1行) | CVSS / 影響 | リンク |
|--------|--------------------|---------------|-----------|-------------|--------|
| — | — | (採用期間内の新規公開なし) | — | — | [JVN](https://jvn.jp/) |

### 国内コミュニティ・研究・イベント

### [2026-11-15] @IT「PHP 重大脆弱性は『始まり』に過ぎない?」: php2shell の兆候は 2024 年の監査で見つかっていたのに、修正案で合意できず 2 年止まっていた
- **何が起きたか**: @IT の解説記事。php2shell (CVE-2026-109618/109619、CVSS v4 9.2) の経緯を整理している。2024 年の PHP Foundation の外部監査でメモリ不足時の問題の兆候が見つかっていたが、互換性や DoS の懸念から修正案がまとまらず対応が止まった。2026 年 8/11 に Calif と OpenAI がそれぞれ RCE を報告し修正が最優先に。公開直前には CVSS 10.0 という誤情報の拡散、攻撃実証動画の誤公開、Chainguard による修正済みイメージの先行公開が重なり、攻撃者が修正内容を先に分析できる状態になった。
- **なぜ重要か**: 協調開示 (CVD) が崩れた実例。修正済みのバイナリやイメージが先に出ると、パッチ diff から攻撃が組み立てられる。脆弱性の公開日前後の監視体制を考える材料になる。
- 出典: [@IT (2026-11-15)](https://atmarkit.itmedia.co.jp/ait/articles/2611/15/news001.html)

### [2026-11-15] Zenn「総務省が点検を求めた『IDOR』とは?」: チェックした ID と実際に書き込む ID がずれる、見落としやすい認可の抜け
- **何が起きたか**: 総務省は 10/13 の注意喚起で、公開アプリを解析してサーバーを狙う手口を取り上げ、重点的に点検する脆弱性として IDOR、SSRF、RCE、SQLi を挙げた。記事はこのうち IDOR を解説。認可はミドルウェアに集約する、最初から本人のデータだけを条件に取得する、チェックと操作に同じ ID を使う、の 3 点を原則とし、「A さんが B さんの ID で取ると 403/404 になる」テストを勧める。SonarQube Hunter Agent が見つけた「自分の BasketId で所有者を確認し、被害者の BasketId に書き込む」型の IDOR を例に、チェックの有無を探すだけでは見つからないと指摘する。
- **なぜ重要か**: 上の JPCERT/CC の調査と同じく、非公開 API の認可が国内攻撃の主な標的。「チェックした対象と操作する対象のずれ」は、手動診断で突くパターンとしてそのまま使える。
- 出典: [Zenn (2026-11-15)](https://zenn.dev/tkishioka/articles/idor-hunter-agent)

### [2026-11-15] Zenn: 使い捨て VPS にハニーポットを約 50 時間置いた観測の設計 (nftables で外向き遮断、48,874 件の記録)
- **何が起きたか**: 使い捨ての VPS に Cowrie と自作の罠を置いた観測。nftables で外向き通信を DNS と NTP 以外すべて遮断し、記録は自宅側から取りに行く設計で 48,874 件を収集。ログインを許す回数を 1〜5 回目に変えて初めてボットがログインでき、dropbear・ARM・BusyBox に見せかけるとマルウェアを書き込むところまで進むボットが多かったという。
- **なぜ重要か**: 観測環境を安全に分離する設計の具体例として参考になる。SSH ハニーポットの「許可回数」と「見せかけるバナー」が、観測できる攻撃の深さを左右する点が実務的。
- 出典: [Zenn (2026-11-15)](https://zenn.dev/yu_muimi/articles/076b92241109dd)

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 95 (4 系統の調査ワーカーで分担。RSS/Atom 約 80、NVD API、OSV の modified_id.csv 9 エコシステム + api.osv.dev 個別照会、CISA KEV JSON、EPSS、Security NEXT の ID 巡回、WebSearch 約 26 クエリ)
- 採用件数: AI技術=11 / AIセキュリティ=4 / セキュリティ=11 (短信 3 含む) / CVE=12 / 国内インシデント=2 / 国内政策=3 / JVN=0 / 国内コミュニティ=3
- 除外理由内訳: 古すぎ=約 40 (11/13 以前公表で報道だけが期間内のもの。国内: ヤマダデンキ、京成スカイライナー、大阪公立大第6報、読売巨人軍、ソースネクスト中間報告、高知市など。海外/AI: SCKit、Mior/Skyfall、PostgreSQL 52件、Trezor、IBM ContextForge MCP Gateway [11/12-13]、Jet Admin [11/13]、Flowise/@utcp [11/13]、Lovable、CrowdStrike の買収など) / 重複=約 40 (UnrealIRCd と Check Point の KEV、FaceStealer、Operation Endgame、Cursor/Fireworks の事故報告本体、ARTEX Flash 本体、M365 障害の第一報、Apple Secure Exclaves、FAA、Gemini 4 Carbon、Opus 5.5 の案内、NVIDIA 署名運動、花キューピット、JPCERT チェックリスト、マネックス証券、アットホームなど) / 日付不明=約 5 (databreaches.net の White House AI Task Force [Cloudflare 遮断・一次情報なし]、川口市ラクリザ、Lovable 英語版の公開日、ハンゲ第4報など)
- 取得失敗ソース: GitHub API / Advisories の Atom (403 / 249 バイトの空応答 → OSV の modified_id.csv と api.osv.dev で代替。修正コミットの中身は未確認でリンクは NVD の references を使用)、Dark Reading・MarkTechPost・VentureBeat・databreaches.net・セキュリティ対策Lab (Cloudflare のチャレンジ / 403 → RSS 説明文や二次ソースで代替)、Huntress RSS (XML 破損)、MSRC/Rapid7/SC Media/Socket の RSS (XML 破損 → 生データを grep)、ITmedia AI+ (期間内の新規なし)、JPCERT/CC・IPA の RSS (期間内の新規項目なし)、JVN・JVN iPedia (期間内の新規公開なし)、福岡市サイト (一部ページで接続リセット → 報道で代替)。JSON::XS・Assimp・Kroki・MP4Box・libdca の一部は修正コミットの個別特定ができず advisory URL で代用した。

</details>
