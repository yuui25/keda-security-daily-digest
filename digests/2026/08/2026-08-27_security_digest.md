# KEDA Daily Digest — 2026-08-27 (JST)

> 採用範囲: 公開日 2026-08-25 〜 2026-08-27
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

OpenAI の自社推論チップ「Jalapeño」が Nvidia Blackwell を AI work/watt で最大 1.9 倍上回るベンチマーク結果を公表し、Anthropic は IPO 投資家向けに $30 兆の TAM を提示。同時に Anthropic は Claude の記憶を Chat/Cowork 間で統一するプロダクトアップデートも公開した。セキュリティでは Gitea の diffpatch コードインジェクション (CVE-2026-60004, CVSS 9.8) が CISA KEV 追加・実エクスプロイト確認済み (攻撃所要時間11秒・クリプトマイナー投下)、FBI/DOJ が中国 APT 「QTFY」の QScan/QTRouter インフラを押収。NVIDIA AI エージェントデプロイツール NemoClaw (CVE-2026-65105) では DNS rebinding によるローカル Ollama モデル永続汚染が可能な脆弱性が公開、Ubiquiti UniFi では3件のMaxシビアリティ CVE が同日修正公開された。

---

## AI 関連ニュース

- **[2026-08-25]** [OpenAI の自社推論チップ「Jalapeño」が Nvidia Blackwell を AI work/watt で最大 1.9 倍上回る — 低レイテンシ推論 2.1〜4.1 倍高速](https://www.cnbc.com/2026/08/26/openai-jalapeno-ai-chip-nvidia.html) — OpenAI が Broadcom と共同開発した初の自社推論専用チップ Jalapeño のベンチマークを公開。GPT-OSS-120B / DeepSeek R1 / Kimi K2.5 の3モデルで Blackwell 世代比 1.5〜1.9 倍のスループット・1.7〜3.6 倍の低 E2E レイテンシを達成。2026年末に低量産開始予定、トレーニング向け Nvidia 調達は継続 *(CNBC / Yahoo Finance 2026-08-25〜26)*

- **[2026-08-25]** [Amazon が21年間運営のクラウドソーシングプラットフォーム Mechanical Turk を2026-09-30に廃止 — AI データラベリング分業の終焉](https://finance.yahoo.com/technology/ai/articles/amazon-shutting-down-mechanical-turk-110911035.html) — Amazon が Mechanical Turk の廃止を公式発表。ピーク時50万ワーカー規模のプラットフォームが Scale AI・Prolific 等のデータラベリングスタートアップ台頭と AI 能力向上を背景に撤退。新規顧客受付は2026-07時点で既に停止済み *(CNBC / Yahoo Finance / TechCrunch 2026-08-25)*

- **[2026-08-25]** [Anthropic が Claude の記憶を Chat と Cowork で統一 — トピック別の確認・編集・削除が可能に](https://techcrunch.com/2026/08/25/claude-cowork-finally-remembers-what-you-told-the-app-in-chat/) — Anthropic が Claude の記憶共有機能を更新。Chat での会話と Cowork のクラウドタスク実行で同一メモリを参照可能に。設定画面でトピック別にファイル形式で管理・削除でき、健康・政治・宗教等センシティブトピックはデフォルト非記憶。Free/Pro/Max で即日提供 *(TechCrunch / 9to5Mac / SiliconANGLE 2026-08-25)*

- **[2026-08-25]** [Google Cloud が法律業務向け「Gemini Enterprise for Legal」を発表 — Cleary・Freshfields 等大手ロー・ファームが初期導入](https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise-for-legal) — Google Cloud が初の業界特化型 Gemini Enterprise パッケージとして Gemini Enterprise for Legal を発表。契約審査・規制モニタリング・法的調査・書類作成を AI エージェントが担当し、Thomson Reuters / Harvey / LexisNexis と連携。金融サービス版も同時発表 *(Google Cloud Blog 2026-08-25)*

- **[2026-08-25]** [Anthropic が IPO 投資家に $30 兆の TAM を提示 — 評価額 $2 兆・ARR $650 億・Q2 売上 $116 億](https://finance.yahoo.com/technology/ai/articles/anthropic-pitches-ipo-investors-30-172107288.html) — Anthropic が IPO 目論見書に向けて TAM を $30 兆超と試算 (SpaceX の $285 億を超える水準)。2026-Q2 売上は前期比2倍以上の $116 億、ARR は $650 億超、2028年予測 $1,900〜2,000 億。上場は早ければ2026年9〜10月の見込みで調達額 $1,000 億を目標 *(Yahoo Finance / PYMNTS / QZ 2026-08-25)*

- **[2026-08-26]** [Mistral AI とサウジ AI 企業 HUMAIN が数億ユーロ規模の戦略的パートナーシップ — アラビア語モデル開発と中東 AI インフラ拡充へ](https://mistral.ai/news/ai-now-summit-2026/) — Mistral AI が HUMAIN (サウジ AI 国家企業) と高性能アラビア語言語モデルの共同開発・データセンターインフラ整備・中東全域への AI ソリューション展開を含む「数億ユーロ」規模の提携を発表。中東での欧州 AI エコシステムの地政学的足場確保が狙い *(Mistral AI News 2026-08-26)*

- **[2026-08-26]** [Waymo がミュンヘンへの完全自律ロボタクシー展開 (2027年予定) と新4都市 (サンディエゴ・ラスベガス・タンパ・デンバー) 開始を発表](https://electriccarsreport.com/2026/08/waymo-is-bringing-fully-autonomous-robotaxis-to-munich-in-2027/) — Waymo がミュンヘン向け HD マッピング・テストプログラムを開始し欧州初展開を宣言。同時に米国4新都市での人間監督者なし完全自律走行開始を発表。VP Srikanth Thirumalai は Axios に「カメラ/ライダー/レーダー三種協調なしに安全展開は不可能」と AI 単体依存を否定 *(Waymo Blog / Axios 2026-08-26)*

---

## セキュリティ関連ニュース

- **[2026-08-25]** [CVE-2026-60004: Gitea diffpatch コードインジェクション CISA KEV 追加 — 無登録訪問者が11秒でクリプトマイナーを投下](https://www.securityweek.com/cisa-warns-of-exploited-gitea-vulnerability/) — CISA が CVE-2026-60004 (Gitea diffpatch エンドポイント、CVSS 9.8) を KEV に追加 (2026-08-25)。デフォルトの公開登録機能でアカウントを作成しリポジトリに git hook をインストール → Gitea OS ユーザー権限で任意シェルコマンド実行。ロシアの共同ブログ Habr の事故報告では11秒でクリプトマイニングソフトが展開された。修正版は Gitea 1.27.1。連邦機関は2026-08-28 までに対処が要求される *(SecurityWeek / SOCPrime / BleepingComputer 2026-08-25〜26)*

- **[2026-08-25]** [NVIDIA NemoClaw CVE-2026-65105: 悪意ある Web ページ1回の訪問でローカル AI エージェントを乗っ取り — Ollama に永続的指示を注入](https://www.cyera.com/research/nemoclaw-one-website-visit-to-hijack-your-ai-agent) — Oasis Security が NemoClaw デプロイツールの脆弱性を公開。Ollama バックエンドが認証なしで `0.0.0.0:11434` にバインドされるため、DNS rebinding 攻撃でブラウザ経由から Ollama API が到達可能に。攻撃者はモデルのチャットテンプレートを改ざんし、以後の全会話に悪意ある指示を永続注入。修正済みバージョンにアップデート必須 (2026-08-25 時点で実エクスプロイト未確認) *(Oasis Security / Security Boulevard / GBHackers 2026-08-25)*

- **[2026-08-25]** [ShinyHunters が ReliaQuest へのソーシャルエンジニアリング成功を主張 — 従業員がなりすまし電話で偽 SSO にパスワード入力し MFA 承認](https://www.helpnetsecurity.com/2026/08/25/reliaquest-breach-social-engineering/) — 脅威アクターが ReliaQuest の lookalike ドメイン + 偽 SSO ページを構築し、「社内セキュリティ担当者」を名乗って従業員に電話。1名がパスワードと Push 通知承認を実施し、攻撃者は一時的にアイデンティティダッシュボードを閲覧。ReliaQuest は「顧客データへの横移動なし、侵害は限定的」と主張、ShinyHunters は深刻な侵害と主張して対立 *(Help Net Security / SecurityWeek 2026-08-25)*

- **[2026-08-26]** [FBI/DOJ が中国 APT 「QTFY」の QScan/QTRouter インフラを押収 — NASA・連邦準備制度・エネルギー省・HHS・上院が標的、選挙システムへの攻撃も](https://www.justice.gov/opa/pr/justice-department-and-fbi-seize-platforms-operated-and-used-china-state-sponsored-hackers) — DOJ と FBI が南京新九魏ネットワーク技術公司所属の QTFY グループが運用する偵察・プロキシ管理・運用ルーティングプラットフォーム QScan/QTRouter を押収。2026年6月に米国選挙システムへの攻撃も確認済み。Lumen Technologies は「中国系サイバー作戦の高度な産業化を示す四半マスター型インフラ」と分析 *(DOJ Press Release / THN / BleepingComputer 2026-08-26)*

- **[2026-08-26]** [Ubiquiti が UniFi Protect・Talk・OS Server で最大重要度 CVE 3件 (+18件) を修正 — 未認証リモートからの特権昇格・コマンド実行が可能](https://www.bleepingcomputer.com/news/security/ubiquiti-patches-three-max-severity-security-vulnerabilities/) — Ubiquiti が CVE-2026-77537 (UniFi Protect 不正入力検証・未認証デバイス侵害)、CVE-2026-77550 (CRLF インジェクション)、CVE-2026-77554 (UniFi Talk VoIP コマンドインジェクション) の3件をリリース。いずれも認証不要・ユーザー操作不要・低複雑度。同日に Critical 18件も修正。実エクスプロイトの有無は未開示 *(BleepingComputer / SecurityAffairs 2026-08-26)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-08-25 以降 / CISA KEV 追加 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-60004 | Gitea 1.17 〜 < 1.27.1 | CWE-94 / **9.8** | デフォルト公開登録でアカウント作成 → diffpatch エンドポイントがリポジトリ管理の git hook を無検証でインストール → Gitea OS ユーザー権限で任意シェルコマンド実行 | Gitea 1.27.1 で修正 (2026-07月末); [SecurityWeek](https://www.securityweek.com/cisa-warns-of-exploited-gitea-vulnerability/); KEV 追加 **2026-08-25** | **CISA KEV** / CVSS 9.8 / 実エクスプロイト確認済み (クリプトマイナー) / 11秒攻撃 |
| CVE-2026-65105 | NVIDIA NemoClaw (修正版に更新) | CWE-441 / High | Ollama を `0.0.0.0:11434` に認証なしバインド + Host ヘッダー検証無効化 → 悪意ある Web ページから DNS rebinding でブラウザが Ollama API へリクエスト送信 → モデルのチャットテンプレートを改ざんし以後の全対話に指示を永続注入 | 最新 NemoClaw に更新; [Oasis Security Research](https://www.cyera.com/research/nemoclaw-one-website-visit-to-hijack-your-ai-agent); 公開 **2026-08-25** | AI エージェント永続汚染 / ドライブバイ攻撃 / ローカル AI ツール普及で攻撃面拡大 |
| CVE-2026-77537 | Ubiquiti UniFi Protect < 7.2.105 | CWE-20 / **10.0** | 未認証攻撃者がネットワーク経由で不正な入力を送信 → UniFi Protect の入力検証欠如 → デバイス完全侵害 | UniFi Protect 7.2.105 以降で修正; [BleepingComputer](https://www.bleepingcomputer.com/news/security/ubiquiti-patches-three-max-severity-security-vulnerabilities/); 公開 **2026-08-26** | CVSS 10.0 / 未認証 / 家庭・企業監視カメラ基盤 / 広範普及 |
| CVE-2026-77554 | Ubiquiti UniFi Talk < 5.3.2 | CWE-78 / **10.0** | 未認証攻撃者が VoIP 管理インタフェースに特殊文字を含む入力を送信 → コマンドインジェクション → VoIP サーバーで任意 OS コマンド実行 | UniFi Talk 5.3.2 以降で修正; 同上 BleepingComputer; 公開 **2026-08-26** | CVSS 10.0 / 同メーカー同日公開バリアント / VoIP 企業インフラ標的 |
| CVE-2026-81032 / GHSA-c937-9ccf-7mq9 | NebulaGraph ≤ 3.8.0 (未修正) | CWE-306 / **9.3** | WebService デーモンがセキュリティ制御なしでルート登録 → 未認証 HTTP で実行時設定 (証明書パス・パスワードファイル位置・ログイン試行制限等) の読み取り・改ざんが可能 → セキュリティ機能の無効化・設定ハイジャック | 修正版なし (v3.8.0 時点); [GHSA-c937-9ccf-7mq9](https://github.com/advisories/GHSA-c937-9ccf-7mq9); 公開 **2026-08-26** | CVSS 9.3 / グラフDB 管理 API 無認証公開 / パッチ未公開 / ネットワーク分離で緩和 |
| CVE-2026-58474 / GHSA-hfpc-7mr4-p297 | whichllm < 0.5.16 | CWE-94 / **8.6** | 攻撃者制御の HuggingFace リポジトリが GGUF ファイル名に特殊文字を含む → `cli.py` が `rfilename` フィールドをエスケープなしで Python ソースコードに文字列補間 → モデルダウンロード前に任意コード実行 | whichllm 0.5.16 (commit 77e8dc9); [GHSA-hfpc-7mr4-p297](https://github.com/advisories/GHSA-hfpc-7mr4-p297); 公開 **2026-08-26** | CVSS 8.6 / HuggingFace リポジトリ起点のサプライチェーン攻撃 / AI ツール CLI 利用者に広範影響 / バリアントハント: 他 LLM CLI の同種補間 |
| CVE-2026-47841 / GHSA-326h-rh66-6gp9 | Spring Security 6.4.0〜6.4.18 / 6.5.0〜6.5.11 / 7.0.0〜7.0.6 / 7.1.0 | CWE-287 / **7.4** | 分散 HTTP セッションストア使用時に WebAuthn ユーザー検証状態が各ノードで独立管理 → セッションスティッキーなし環境でノード切替時に検証済みフラグが伝播せず → FIDO2 ユーザー検証バイパス | Spring Security 7.1.1 / 7.0.7 / 6.5.12 / 6.4.19 で修正; [GHSA-326h-rh66-6gp9](https://github.com/advisories/GHSA-326h-rh66-6gp9); 公開 **2026-08-26** | CVSS 7.4 / WebAuthn を採用した Java エンタープライズ広範影響 / ロードバランサー環境でのみ発現 / 同仕様の .NET/Go 実装で水平伝播確認推奨 |

---

## 国内脆弱性・インシデント情報

採用窓内 (2026-08-25〜08-27) での JVN・JPCERT/CC・IPA 新規公開は確認できなかった (2026-08-25 公開の JVN#74538868/Sakura Editor および CVE-2026-39454/SKYSEA Client View は 2026-08-26 付ダイジェスト掲載済みのため除外)。

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| openai.com / cnbc.com (Jalapeño chip) | WebSearch スニペット 2026-08-25〜26 確認 ✓; CNBC URL パターン確認 ✓; Broadcom 協業・ベンチマーク詳細確認 ✓ |
| cnbc.com / yahoo.finance.com (Amazon Mechanical Turk) | WebSearch スニペット 2026-08-25〜26 確認 ✓; QZ.com URL パターン確認 ✓; 2026-09-30 廃止確認 ✓ |
| techcrunch.com / siliconangle.com (Anthropic Claude memory) | WebSearch スニペット 2026-08-25〜26 確認 ✓; 複数独立ソース一致 ✓ |
| cloud.google.com (Gemini Enterprise for Legal) | **WebFetch 直接取得成功** 検索経由 ✓; 2026-08-25 Google Cloud Blog URL確認 ✓; Cleary/Freshfields 等導入確認 ✓ |
| yahoo.finance.com / pymnts.com (Anthropic $30T TAM) | WebSearch スニペット 2026-08-25 確認 ✓; 複数独立ソース一致 ($11.6B Q2 / $65B ARR 確認) ✓ |
| mistral.ai (HUMAIN partnership) | WebSearch スニペット 2026-08-26 確認 ✓; AI Now Summit 2026 URL確認 ✓ |
| waymo.com / axios.com (Munich + 4 US cities) | WebSearch スニペット 2026-08-26 確認 ✓; Waymo blog URL確認 ✓; Axios VP インタビュー確認 ✓ |
| cisa.gov (CVE-2026-60004 KEV) | WebSearch スニペット 2026-08-25 KEV 追加確認 ✓; CISA URL パターン確認 ✓; SOCPrime 詳細確認 ✓ (直接 WebFetch EGRESS_BLOCKED) |
| helpnetsecurity.com / securityweek.com (Gitea exploitation) | WebSearch スニペット 2026-08-26 確認 ✓; BleepingComputer / SecurityWeek 複数ソース一致 ✓ |
| cyera.com / securityboulevard.com (NemoClaw CVE-2026-65105) | WebSearch スニペット 2026-08-25 公開確認 ✓ (直接 WebFetch EGRESS_BLOCKED); explainx.ai URL 確認 ✓ |
| helpnetsecurity.com (ReliaQuest ShinyHunters) | WebSearch スニペット 2026-08-25 確認 ✓; SecurityWeek / BleepingComputer 裏取り ✓ |
| justice.gov (FBI QTFY China APT) | **WebFetch 試行**: 検索スニペットから DOJ 公式 URL 確認 ✓; THN / BleepingComputer / We Fix PC URL (2026-08-26) 確認 ✓ |
| bleepingcomputer.com (Ubiquiti max severity CVEs) | WebSearch スニペット 2026-08-26 確認 ✓ (直接 WebFetch EGRESS_BLOCKED); CVE-2026-77537/77550/77554 / 修正バージョン確認 ✓ |
| github.com/advisories/GHSA-c937-9ccf-7mq9 (NebulaGraph) | **WebFetch 直接取得成功** ✓; Published: August 26, 2026; CVSS 9.3 確認 ✓ |
| github.com/advisories/GHSA-hfpc-7mr4-p297 (whichllm) | **WebFetch 直接取得成功** ✓; Published: August 26, 2026; CVSS 8.6 確認 ✓; commit 77e8dc9 確認 ✓ |
| github.com/advisories/GHSA-326h-rh66-6gp9 (Spring Security WebAuthn) | **WebFetch 直接取得成功** ✓; Published: August 26, 2026; CVSS 7.4 確認 ✓ |
| github.com/advisories/GHSA-mcj4-mphf-j9ff (Trivy CVE-2026-55092) | **WebFetch 直接取得成功** ✓; Published: **June 15, 2026** → 採用窓外のため**除外** |
| github.com/advisories/GHSA-vwf3-4xxj-qg6h (mcp-contextforge-gateway) | **WebFetch 直接取得成功** ✓; Published: **June 15, 2026** → 採用窓外のため**除外** |
| jvn.jp / jpcert.or.jp / ipa.go.jp (国内) | EGRESS_BLOCKED — 直接確認不可; WebSearch で 2026-08-25 公開 Sakura Editor / SKYSEA は 08-26 digest 掲載済みのため除外 |

### 集計サマリ

- **巡回ソース数**: 約 35
- **採用件数**: AI=7 / Security=5 / CVE=7 / 国内=0
- **除外理由内訳**:
  - 採用窓外 (公開日 <2026-08-25): OpenAI AI 安全開発一時停止 (2026-08-24, NPR報道); NetScaler CVE-2026-19490 (2026-08-19); Hut American Group 侵害通知 (2026-08-21 テキサス州 AG); Cruciferra/Remus MaaS (eSentire 元記事 2026-07); Trivy CVE-2026-55092 / GHSA-mcj4-mphf-j9ff (2026-06-15); mcp-contextforge-gateway GHSA-vwf3-4xxj-qg6h (2026-06-15); phpMyFAQ GHSA-pg62-f8g4-4wqh (2026-06)
  - 重複 (excluded_set 参照): Anthropic Claude Tag Slack更新 (08-26 digest); Lambda $3B pre-IPO (08-26 digest); OpenAI GPT-5.6 Kiro統合 (08-26 digest); Adobe Campaign Classic CVSS 10.0 ×3 (08-26 digest); Chainlit CVE-2026-45018/45019 (08-26 digest); miniOrange SAML CVE-2026-75218 (08-26 digest); Marimo MCP CVE-2026-75149 (08-26 digest); Sakura Editor JVN#74538868 (08-26 digest); SKYSEA CVE-2026-39454 (08-26 digest)
  - 取得失敗ソース (EGRESS_BLOCKED): bleepingcomputer.com, thehackernews.com, helpnetsecurity.com, securityweek.com, cybersecuritynews.com, gbhackers.com, securityboulevard.com, cisa.gov, nvd.nist.gov, jvn.jp, jpcert.or.jp, ipa.go.jp, techstartups.com, aidapted.ro, explainx.ai, cyera.com

</details>

---

*生成: keda-digest-bot / 2026-08-27 05:05 JST*
