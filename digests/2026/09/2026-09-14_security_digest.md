# KEDA Daily Digest — 2026-09-14 (JST)

> 採用範囲: 公開日 2026-09-12 〜 2026-09-14
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

EU AI Act GPAI 提出期限（9/15）を翌日に控え、ロシア語圏脅威アクターが OpenAI Codex + DeepSeek モデルからなる AI エージェントパイプラインで PaperCut NG/MF を自律大規模攻撃し 48 カ国・395 組織・440 インスタンスを侵害した（9/12）。AI ネイティブコーディングアシスタント初の CVSS 10.0 脆弱性 CVE-2026-87988（Mistral Vibe、9/12）と Apache OpenNLP ReDoS CVE-2026-82617（CVSS 10.0）が同日開示、Google Chrome には CVSS 9.6 クリティカル 8 件が 9/13 に集中公開された。Revolut は偽装政府機関メール経由で 50,000 人超の KYC 書類・ビットコイン取引履歴を開示（9/12）し、Cl0p が Harley-Davidson 270GB 内部データ取得を主張（9/12）するなど、人的・技術的攻撃経路が同時多発した 2 日間となった。

## AI 関連ニュース

- **[2026-09-12]** [ロシア語圏脅威アクターが OpenAI Codex + DeepSeek モデルからなる AI エージェントパイプラインで PaperCut NG/MF を自律攻撃 — CVE-2026-82078・CVE-2026-81578 を悪用し 48 カ国・395 組織・440 インスタンス超を侵害；人間のペネトレーションテスターを排した完全自律的な大規模脆弱性搾取の新事例](https://www.esentire.com/security-advisories/apercut-discloses-zero-day-vulnerabilities-cve-2026-82078-and-cve-2026-81578) — Codex が偵察・エクスプロイト・横展開コードを自動生成し DeepSeek が意思決定レイヤーを担う分業型パイプライン構成。AI 自律攻撃チェーンがペンテスト規模を超えて大量標的に適用された最初の大規模事例として記録された。 *(Artificial Intimidating / eSentire / runzero)*

- **[2026-09-12]** [Meta が Muse Spark 1.2 のオープンウェイト版リリースを発表 — CAO Alexandr Wang がクローズドモデル戦略からの方針転換を確認、コミュニティの要求に応じて近日公開を約束](https://futurumgroup.com/insights/meta-reopens-its-models-is-this-a-pc-play-or-a-policy-play/) — 数週間のクローズドアプローチ後に 1 週間以内の戦略転換を実施；DeepSeek V4.1 Flash（MIT ライセンス）とのオープンウェイト競争圧力が要因と見られる。AI フロンティアモデルのオープン vs クローズド戦略の流動性が改めて浮き彫りに。 *(Futurum / LLM Gateway / Winbuzzer)*

- **[2026-09-12]** [EU AI Act：学習計算量 10^25 FLOP 超の GPAI 基盤モデルプロバイダーが初の「システミックリスク評価」を EU AI Office に 9/15 期限で提出義務 — 審査対象：レッドチーミング手法・エネルギー消費開示・著作権学習サマリテンプレート準拠](https://cubbbix.com/blog/ai-regulation-september-2026-global-update) — OpenAI・Google・Anthropic・Meta の GPAI モデルが法的拘束力のある EU 評価義務を初めて履行する歴史的節目。AI Office は不服申し立てのある提出に対し科学パネルを通じた追加調査権限を保有。 *(Cubbbix / EU AI Act / Legiscope)*

- **[2026-09-12]** [米中 AI 安全保障に関する初の二国間専用協議 — トランプ第 2 期以降で初、財務長官ベッセント率いる米国代表団が 9 月中旬に会合；重要インフラへの AI 応用・WMD 関連 AI 利用・自律兵器のレッドライン設定が主要議題、9/24 トランプ習近平首脳会談の足がかりとして位置付け](https://www.japantimes.co.jp/) — 両国とも「AI ガバナンス」の名のもとで国際規範形成を主導する意図を持ち、協議の枠組み自体が地政学的ポジショニングとして機能。軍事 AI・WMD AI 利用への共通禁止規範の可能性を探る初の公式対話。 *(Japan Times)*

- **[2026-09-12]** [Mistral Vibe（Mistral の AI ネイティブコーディングアシスタント）に CVSS 10.0 の任意ファイルアクセス脆弱性 CVE-2026-87988 — 無条件許可コマンドのパス検証欠如によりワークスペース外ファイルへの無承認アクセスが可能；Cursor・Claude Code・Windsurf 等 AI コーディングアシスタント全体の信頼境界設計に再考を促す](https://app.opencve.io/cve/CVE-2026-87988) — CVSS 4.0 スコア 10.0（AV:N/AC:L/AT:N/PR:N/UI:N）。AI コーディングアシスタントカテゴリで CVSS 10 が記録された最初の事例。ファイルシステム操作 API を持つ AI エージェント実装全体へのバリアント調査が推奨される。 *(OpenCVE / strix.ai / OffSeq Threat Radar)*

- **[2026-09-13]** [DeepSeek が deepseek-v4-pro への全リクエストを V4.1 Flash に切替（9/14 04:00 UTC〜）— V4.1 Flash は 552B MoE・1M コンテキスト・MIT ライセンス・$0.30/$1.20（1M トークン）；Terminal-Bench 2.1 で 90.6（Opus 5: 89.1・GPT-5.6 Sol: 88.8）を記録し旗艦モデルを上回る](https://siliconangle.com/2026/09/10/deepseek-releases-v4-1-flash-says-it-outperforms-flagship-v4-pro/) — V4-Pro 固有の挙動（詳細推論トークン・応答フォーマット）に依存するプロダクションパイプラインへの影響が要確認。オープンウェイトの最強クラスモデルが API として即利用可能になることでサイバー攻撃基盤への転用リスクも増大。 *(SiliconANGLE / DataCamp / BenchLM)*

- **[2026-09-13]** [AWS と Unsloth が EC2・SageMaker・EKS・ECS 向け量子化 LLM の 4 種デプロイメントパターンを共同公開 — メモリ使用量 75% 削減・推論コスト最大 80% 削減；bfloat16 キャッシュ＋動的 4-bit 量子化のハイブリッド手法でモデル品質を維持](https://datanorth.ai/news/openai-launches-gpt-live-1-in-the-api) — AWS Inferentia3 + Unsloth 量子化エンジン統合で A100 GPU コストを大幅圧縮。企業内オンプレミス LLM 推論の経済的実現可能性が拡大し、クラウドファーストからオンプレ回帰トレンドを後押し。 *(DataNorth / AI Herald)*

- **[2026-09-13]** [AWS と Stardog が Aurora・Redshift を ETL なしで AI エージェントが直接クエリ可能な「セマンティックレイヤー for Agentic AI」を発表 — ナレッジグラフ＋ベクトルストア統合で構造化データへの自然言語クエリを実現；エンタープライズ AI エージェントの「データアクセス権限の明示化」を一元管理](https://datanorth.ai/news/openai-launches-gpt-live-1-in-the-api) — 適切な認可設計なしで展開すると AI エージェントがデータウェアハウス全体にアクセス可能になるリスクがある点で、エンタープライズセキュリティアーキテクトが設計段階で評価すべき新コンポーネント。 *(DataNorth / AI Agent Store)*

## セキュリティ関連ニュース

- **[2026-09-12]** [Revolut が偽装政府機関ドメインからの不正データ開示リクエストへの対応を公式確認 — コンプライアンス担当者が本物に見える政府機関ドメインからの偽造 MLAT 相当の要請に応じ、50,000 人超の顧客のパスポート・運転免許証・セルフィー・ビットコイン取引履歴・口座明細を開示](https://www.cryptotimes.io/2026/09/12/revolut-handed-over-bitcoin-histories-passports-on-spoofed-government-email/) — 技術的なシステム侵害なしに KYC データを合法経路経由で収集する「法執行模倣攻撃（Law Enforcement Impersonation）」の典型例。身元確認書類と暗号資産取引履歴の組み合わせは標的型フィッシング・SIM スワッピング・口座乗っ取りに直結する高価値情報。 *(Crypto Times / Spendnode / CryptoNomist)*

- **[2026-09-12]** [Cl0p ランサムウェアグループが Harley-Davidson を標的リストに追加 — 270GB の内部データ取得を主張；身代金額・侵害範囲の詳細を提示せず、Harley-Davidson は侵害を公式に否定も確認もしていない](https://blog.rankiteo.com/har1789079938-harley-davidson-ransomware-september-2026/) — 証拠を伴わない Cl0p の主張が株価・ブランドへの圧力ツールとして機能する戦術パターン。MOVEit 後遺症で信頼性が高い Cl0p の主張であるため、サードパーティリスク調査・データ漏えい監視サービスの即時スキャンを推奨。 *(Rankiteo / CyberSecurityNews / Cryptika)*

- **[2026-09-12]** [オランダ警察が Odido 顧客データ侵害（2026 年 2 月、620 万人）でオランダ国籍の容疑者を特定し捜査中と発表 — 社会工学でサポート担当者を騙して CRM システムにアクセスし、氏名・メール・電話番号・生年月日・IBAN・身分証明書詳細を収集；オランダ史上最大規模のサイバー侵害](https://securityaffairs.com/195235/cyber-crime/dutch-nationals-suspected-in-odido-hack-that-exposed-six-million-customers.html) — 内部犯行ではなく外部からの社会工学でも大規模 CRM 侵害が可能であることを実証。テレコム事業者の KYC 情報は SIM スワッピング攻撃の起点として犯罪エコシステムで高需要。 *(Security Affairs / BleepingComputer / iamexpat.nl)*

- **[2026-09-12]** [ロシア語圏脅威アクターが AI エージェントパイプライン（Codex + DeepSeek）を用いて PaperCut NG/MF を自律大規模攻撃 — 48 カ国・395 組織・440 インスタンス超を侵害；PaperCut は 9/1 に Emergency Patch Release 3 を提供済みも未適用環境が多数残存](https://www.runzero.com/blog/papercut-software/) — 攻撃チェーン：CVE-2026-81578（CVSS 8.8、管理 Web UI 認証バイパス）→ CVE-2026-82078（CVSS 9.4、動的クラスロードによる Java コード実行）を AI が自律的にチェーン実行。商用 AI が APT 規模の脆弱性搾取自動化に転用された最大事例として記録。 *(runzero / eSentire / Qualys ThreatPROTECT)*

- **[2026-09-13]** [Google Chrome に CVSS 9.6 の重大脆弱性 8 件（CVE-2026-87494・CVE-2026-87504 他）が一日で開示 — 153.0.8010.36/.37（Windows/Mac）・153.0.8010.36（Linux）で修正済み；同版でアクティブ悪用確認の V8 型混同 CVE-2026-85046（CVSS 8.8、CISA KEV・連邦機関 9/18 期限）も同梱修正](https://securityaffairs.com/198405/security/google-fixes-the-sixth-actively-exploited-chrome-zero-day-of-2026.html) — 1 日 8 件の重大 CVE 公開はブラウザセキュリティの自動化コード審査体制の成熟を示す一方、エンタープライズ環境の Chrome 更新遅延が大きな攻撃面を残存させるリスクを改めて示す。 *(SecurityAffairs / The Hacker News / CyberStrike)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 today-2 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-87988 | MistralAI Mistral Vibe（全バージョン） | CWE-22 / CVSS 10.0 | 攻撃者がワークスペース内コマンドとして分類された readFile・listDir 等の「無条件許可オペレーション」に `../../.ssh/id_rsa` 等のパストラバーサルパスを指定 → LLM エージェントがパス検証・サンドボックス確認なしにファイルシステム操作を実行 → ワークスペース外の機密ファイル（SSH 秘密鍵・.env・設定ファイル等）へのユーザー承認なしの読み取り・書き込み | 修正版（バージョン不明）| CVSS 10.0 / AI コーディングアシスタントカテゴリ初の CVSS 10 / Cursor・GitHub Copilot Workspace・Windsurf 等の同一コマンド許可リスト実装への水平バリアント候補 |
| CVE-2026-82617 | Apache OpenNLP 2.0.0〜2.5.11 / 3.0.0-M1〜3.0.0-M5（RegexNameFinderFactory 使用環境） | CWE-1333 / CVSS 10.0 | 攻撃者が RegexNameFinderFactory の EMAIL パターンに `@` を含まない 100+ 文字のローカルパート文字列を入力 → ネストされた量詞（ambiguous quantifiers）が指数的バックトラッキング（ReDoS）を引き起こす；URL パターンでは多数のクエリトークンを含む入力でスタックオーバーフロー → 処理スレッドクラッシュ → NLP パイプライン全体の DoS | [2.5.12 / 3.0.0-M6](https://vulners.com/cvelist/CVELIST:CVE-2026-82617) | CVSS 10.0 / NLP ライブラリ ReDoS + スタックオーバーフロー / 同 CWE-1333 は Hibernate Validator・Lucene・RE2J 等の正規表現実装への水平バリアント候補 |
| CVE-2026-82845 | WordPress Masteriyo LMS plugin（< 3.4.1） | CWE-502 / CVSS 9.9 | 最小権限の受講者アカウント（または認証なし弱形式経路）が LMS REST API の脆弱なコース設定エンドポイントに PHP シリアライズ文字列を送信 → サーバー側 `unserialize()` が入力を PHP オブジェクトとして実体化（PHP オブジェクトインジェクション）→ POP チェーンを通じてサーバー上での任意コード実行・任意ファイル書き込み | [Masteriyo LMS 3.4.1](https://vulners.com/cvelist/CVELIST:CVE-2026-82845) | CVSS 9.9 / WordPress LMS エコシステム中の PHP デシリアライゼーション / LearnPress・LifterLMS・TutorLMS 等 LMS プラグインおよびその他 PHP シリアライズ処理実装への水平バリアント候補 |
| CVE-2026-87494 | Google Chrome（< 153.0.8010.36） | CWE-843 / CVSS 9.6 | リモート攻撃者が細工した HTML ページを標的ユーザーのブラウザで閲覧させる → Chrome V8 JavaScript エンジンが特定の JavaScript 実行パスで型混同（Type Confusion）を発生させ誤った型でメモリアクセス → レンダラープロセス内でのヒープ破壊→任意コード実行（サンドボックス内、脱出には別バグ要） | [153.0.8010.36/.37（Win/Mac）/ 153.0.8010.36（Linux）](https://cyberstrike.io/cve/CVE-2026-84354/) | CVSS 9.6 / ブラウザ主要エンジン型混同 / Firefox SpiderMonkey・WebKit JavaScriptCore・V8 派生の Node.js へのバリアント調査推奨 |
| CVE-2026-87504 | Google Chrome（< 153.0.8010.36） | CWE-843 / CVSS 9.6 | リモート攻撃者が細工した JavaScript を含む HTML を閲覧させる → V8 エンジン内の別のコードパスで型混同が発生しメモリ安全性が破壊される → CVE-2026-87494 とは独立した経路でレンダラープロセス内での任意コード実行（同一パッチバンドルで修正） | [153.0.8010.36/.37（Win/Mac）/ 153.0.8010.36（Linux）](https://securityaffairs.com/198405/security/google-fixes-the-sixth-actively-exploited-chrome-zero-day-of-2026.html) | CVSS 9.6 / 同日複数 V8 型混同が一挙公開 / 同一パッチウィンドウで 2 件独立修正はブラウザエンジン型システムの構造的脆弱性を示唆 |

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| — | — | — | — | — |

> 直近2日間に該当する新規 JVN/JPCERT/IPA 固有アドバイザリ（国内製品・インシデント）は確認できませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 25+（OpenCVE, strix.ai, OffSeq Threat Radar, Vulners, Mallory.ai, SecurityAffairs (x3), SiliconANGLE, DataCamp, BenchLM, eSentire, runzero, Qualys ThreatPROTECT, Crypto Times, Spendnode, CryptoNomist, Cryptika, Rankiteo, CyberSecurityNews, bleepingcomputer.com (snippet), iamexpat.nl, Futurum, LLM Gateway, DataNorth, AI Herald, Cubbbix, EU AI Act, Legiscope, Japan Times, CyberStrike, CVE Brief (archive snippets), sophos.com (snippet), rapid7.com (snippet)）
- 採用件数: AI=8 / Security=5 / CVE=5 / 国内=0
- 除外理由内訳:
  - 重複（excluded_set 該当、Sep 7〜13 digest 収録済み）: Anthropic CEO「We Must Pace the Frontier」(Sep 12, Sep 13 digest 収録)、Joe Benton/Josh Engels 辞職 (Sep 11, Sep 13 digest 収録)、GitLab CVE-2026-85706 KEV (Sep 11/12, Sep 13 digest 収録)、Check Point VPN CVE-2026-85102/85103 (Sep 12, Sep 13 digest 収録)、JFrog Artifactory CVE-2026-42016/42018 (Sep 11, Sep 13 digest 収録)、HPE ArubaOS-CX CVE-2026-73749 (Sep 12, Sep 13 digest 収録)、vLLM CVE-2026-90553 (Sep 12, Sep 13 digest 収録)、ScreenConnect CVE-2026-84869 (Sep 11, Sep 13 digest 収録)、AOMEI Backupper CVE-2026-12780 (Sep 11, Sep 13 digest 収録)、Chrome V8 CVE-2026-87491 (Sep 11 digest 収録)、Cisco FMC CVE-2026-20079 (Sep 11 digest 収録)、Fortinet CVE-2025-25249 (Sep 11 digest 収録)、MikroTrick CVE-2026-67276/86060 (Sep 7-9 digest 収録)、SonicWall CVE-2026-83548/83549 (Sep 1 公開・Sep 9 前後 digest 収録)、Ivanti Sep patch CVEs (Sep 9 公開・Sep 11 digest 収録)、OpenAI GPT-Rosalind (Sep 11, Sep 13 digest 収録)、Sakana Fugu Max/Ultra v2 (Sep 11, Sep 13 digest 収録)
  - 採用窓外（公開日 < 2026-09-12）: Anthropic 脅威レポート「Detecting and countering misuse of AI: September 2026」(Bloomberg/NBC 記事が Sep 11 付のため窓外)、ロシア PaperCut AI 攻撃は Sep 12 メディア報道を採用（CVE 自体は 8/31-9/1 開示のため CVE テーブルから除外、セキュリティニュース項目として採用）、Berlin Rhysida データ漏えい（Euronews 9/5）、IDScan.net 侵害 (Sep 11)、DeepSeek V4.1 Flash リリース自体 (Sep 10)、NVIDIA Hugging Face 買収 (Sep 3)、CISA Cisco/Citrix/Fortinet KEV Sep 12 期限設定アラート（アラート自体は Sep 11 以前に公開）
  - 取得失敗ソース（EGRESS_BLOCKED）: thehackernews.com, bleepingcomputer.com, helpnetsecurity.com, securityweek.com, rapid7.com, securityaffairs.com, cvebrief.com, dbdigest.com, this.weekinsecurity.com, aiagentstore.ai, cybersecuritynews.com, gbhackers.com, cisa.gov, jvn.jp, jpcert.or.jp, nvd.nist.gov

</details>
