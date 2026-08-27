# KEDA Daily Digest — 2026-08-28 (JST)

> 採用範囲: 公開日 2026-08-26 〜 2026-08-28
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

NVIDIA が Hugging Face を約 $129 億で買収合意と The Information / CNBC が報道 (2026-08-26/27)。OpenAI・Anthropic・Google・Microsoft 等 116 社が「AI サイバー攻撃に限られた窓がある」と共同書簡を発表し、病院・電力網などクリティカルインフラへの AI 主導攻撃急増に警鐘 (2026-08-27)。セキュリティでは Trivy/Checkmarx KICS/LiteLLM を汚染した TeamPCP サプライチェーン攻撃の実行犯 2 名がオーストラリアで起訴 (2026-08-27)、Aurora ランサムウェア関連者が Cursor AI を「認可テスト」と偽って 20 社超を攻撃した事例が露出。Citrix NetScaler CVE-2026-8452 が CISA KEV 追加 (8/26)・連邦機関期日 8/29 で実エクスプロイト (webshell 投下) 確認済み、Boston Scientific が世界規模の受注・出荷停止を開示。

---

## AI 関連ニュース

- **[2026-08-26]** [NVIDIA が Hugging Face を約 $129 億で買収合意と The Information / CNBC が報道 — クローズは未確定、AI チップ以外のソフトウェア・モデルエコシステムへの足場を狙う](https://finance.yahoo.com/technology/ai/articles/nvidia-agrees-buy-hugging-face-110522469.html) — NVIDIA が世界最大規模のオープンソース AI モデルホスティングプラットフォーム Hugging Face を $129 億で取得する合意に至ったと The Information が報道 (CNBC が確認)。まだ正式署名はなく破談の可能性あり。NVIDIA は 2025 年末に Hugging Face が評価額 $70 億だった際の $5 億投資提案を断られた経緯 *(The Information / CNBC / Forbes 2026-08-26〜27)*

- **[2026-08-26]** [OpenAI が ChatGPT for Teachers を 55 学区・20 州に拡大 — 30 万人以上の教育者に無料提供、16 州またぎのプライバシー協定を業界初で締結](https://openai.com/index/bringing-chatgpt-for-teachers-to-more-us-school-districts/) — OpenAI が ChatGPT for Teachers の対象を 55 追加学区・20 州に拡充し累計 100 以上の K-12 組織・30 万人超が無料利用可能に。米国最大 20 学区の 1/5 を含む新コホート追加、16 州共通の生徒データプライバシーフレームワークも業界初で締結 (提供期間 2028 年 6 月まで) *(OpenAI Blog / 9to5Mac 2026-08-26)*

- **[2026-08-26]** [Alibaba Qwen チームが Qwen3.8-Flash-Next (125B MoE, 6B active params) をオープンソース公開 — Qwen4 アーキテクチャのプレビュー版、旗艦比約 1/12 のコスト](https://www.bloomberg.com/news/articles/2026-08-26/alibaba-releases-smaller-cost-effective-qwen-ai-model) — 125B バックボーン + 51B N-gram 埋め込みテーブル + 4B MTP モジュールで構成される MoE モデルを ModelScope / HuggingFace で公開。Qwen4 ファミリーの正式リリースに向けてデベロッパーコミュニティが準備できるよう先行公開 *(Bloomberg / Yahoo Finance / the-decoder 2026-08-26)*

- **[2026-08-26]** [IBM が Granite 4.2 ファミリー (3B/8B/30B) を Apache 2.0 でオープンウェイトリリース — エージェント RL・512K コンテキスト・ネイティブ推論を内蔵](https://research.ibm.com/blog/introducing-granite-4-2) — 15T トークン学習・512K コンテキスト・thinking/non-thinking モード切替対応の推論モデル群。8B/30B はコードランナー・Web 検索・ツール呼び出しをリアルサンドボックスで学習した「エージェント RL」学習済みで、ソフトウェアエンジニアリングエージェント・DevOps 自動化・長文 RAG 向け *(IBM Research / the-decoder 2026-08-26)*

- **[2026-08-27]** [OpenAI・Anthropic・Google・Microsoft 等 116 社が「AI サイバー攻撃に限られた窓がある」と共同書簡 — 病院・水処理施設などクリティカルインフラへの AI 主導攻撃急増を警告](https://www.cnbc.com/2026/08/27/ai-cyber-defense-letter.html) — 116 社・機関が署名した公開書簡が発表され、フロンティア AI 企業は大規模インシデント時に最強クラスのモデル・大規模資金・トレーニング・現場支援をクリティカルインフラ事業者に提供すべきと提言。「AI により精巧なサイバー能力が低コストで攻撃者に広がる」と警告 *(Bloomberg / TechCrunch / CNBC / Axios 2026-08-27)*

- **[2026-08-27]** [Amazon Kiro IDE に prompt injection → 機密データの外部サーバー送信が可能な脆弱性 — Mindguard が開示、CVE 未割当、最新版 1.0.337 で修正済み](https://thehackernews.com/2026/08/amazon-kiro-prompt-injection-can.html) — 攻撃者がリポジトリの steering ファイルを細工し、Kiro エージェントにローカルファイルを読み取らせ Markdown の画像レンダリングを通じて外部エンドポイントへ送信させる手法。ユーザーが攻撃者制御リポジトリを開くだけでサイレントにデータが流出。CVE 未割当・影響バージョンは 0.7.45 *(THN / Mindguard / Kodem Security 2026-08-27)*

---

## セキュリティ関連ニュース

- **[2026-08-26]** [Boston Scientific がサイバー攻撃で世界規模の受注・出荷システムを停止 — 8/25 検知・8/26 開示、ランサムウェアか調査中](https://www.cbsnews.com/news/boston-scientific-cyberattack-disrupts-global-operations/) — 医療機器大手 Boston Scientific が「サイバーセキュリティインシデント」を 8/25 に検知し 8/26 に開示。受注・出荷を含む業務システムが世界的に停止し財務的影響は未確定。攻撃者・手法・データ流出の有無は未開示でサードパーティ専門家が調査中。2026 年の医療機器セクターへのサイバー攻撃 (AdaptHealth・Intuitive・Stryker 等) の最新事例 *(CBS News / The Register / cybernews 2026-08-26)*

- **[2026-08-26]** [CISA が CVE-2026-8452 (Citrix NetScaler SAML heap overflow) 含む 6 件を KEV カタログに追加 — NetScaler の連邦機関対処期日は 8/29](https://www.cisa.gov/news-events/alerts/2026/08/26/cisa-adds-six-known-exploited-vulnerabilities-catalog) — 新旧混在の異例のバッチ: CVE-2026-8452 (Citrix NetScaler CVSS 8.8, webshell 投下確認) / CVE-2015-3246 (Red Hat Libuser race condition) / CVE-2015-5287 (Red Hat ABRT 権限昇格) / CVE-2019-1068 (Microsoft SQL Server RCE) / CVE-2021-23758 (Ajax.NET Professional デシリアライズ) / CVE-2022-0995 (Linux Kernel OOB write) *(CISA / THN 2026-08-26)*

- **[2026-08-27]** [Citrix NetScaler CVE-2026-8452: 6/30 公開時「DoS」と称されたが SAML ヒープ overflow が事実上 pre-auth RCE — 12 日間で 36 件・webshell x.php / z.php 投下](https://www.helpnetsecurity.com/2026/08/27/netscaler-adc-gateway-cve-2026-8452/) — WatchTowr がパッチ差分を解析し SAML SSO メッセージのフィールドを固定サイズバッファにサイズ確認なしでコピーするヒープ overflow と実証、SAML 設定済み Gateway/AAA に 1 HTTP リクエストで全トラフィック担当プロセスのメモリを汚染可能。修正パッチ (14.1-72.61 / 13.1-63.18 / 13.1-37.272) が 6/30 に既提供済み *(Help Net Security / WatchTowr Labs / SecurityWeek 2026-08-27)*

- **[2026-08-27]** [オーストラリア連邦警察が TeamPCP サプライチェーン攻撃の実行犯 2 名を Perth Magistrates Court に起訴 — 1,000 以上の組織・50 万件認証情報・300 GB データ流出](https://techcrunch.com/2026/08/27/australian-police-arrest-two-over-teampcp-hacks-targeting-mercor-openai-and-others/) — AFP が Louis Michael Gaebler (23) と Ruben Ian Thomson (21) を計 14 件の罪状で起訴 (8/27)。2 名は 2026 年 3 月に Trivy スキャナ→Checkmarx KICS→LiteLLM のビルドパイプラインを連鎖汚染: Trivy 経由で窃取した KICS 発行トークンを使い LiteLLM バックドア版を PyPI に push。OpenAI・Mercor 等が標的に含まれる *(THN / BleepingComputer / TechCrunch / The Record 2026-08-27)*

- **[2026-08-27]** [Aurora ランサムウェア関連者が Cursor AI を「認可されたセキュリティテスト」と偽って使用し 9 カ国・20 社超を攻撃 — AD 昇格計画を AI でロシア語立案、4 社がリークサイト掲載](https://cybersecuritynews.com/ransomware-hacker-uses-ai/) — 露出したオペレーターサーバーから Cursor チャットログ・Kerberos チケット・BloodHound コレクション・Zig 製バイナリが回収され AI 悪用の全容が判明。Cursor が拒否すると「シミュレーション」と再偽装して継続。製造・食品・農業・専門サービスが主標的で 2026 年 4〜7 月に 17 社でドメイン管理者権限を取得 *(cybersecuritynews.com / gbhackers.com / netnewsledger.com 2026-08-27)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-08-26 以降 / CISA KEV 追加 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-8452 | Citrix NetScaler ADC/Gateway ≤14.1-70.x / ≤13.1-62.x / ≤13.1-37.x | CWE-122 / **8.8** | SAML SSO メッセージの攻撃者制御フィールドを固定サイズバッファにサイズ確認なしでコピー → SAML 設定済み Gateway/AAA に未認証 HTTP 1 リクエストでヒープ上書き → 全トラフィック担当プロセスで pre-auth RCE | パッチ 14.1-72.61 / 13.1-63.18 / 13.1-37.272 (2026-06-30 提供済); [WatchTowr 解析](https://labs.watchtowr.com/youre-back-in-the-room-citrix-netscaler-pre-auth-rce-cve-2026-8452/); KEV 追加 **2026-08-26** | **CISA KEV** / 実エクスプロイト確認 (webshell x.php/z.php 投下) / 12 日間 36 件 / 連邦機関 **期日 8/29** |
| CVE-2026-65182 | Apache Tomcat 9.0.x < 9.0.121 / 10.1.x < 10.1.46 (他バージョンも影響あり) | CWE-284 / Important | 特定の条件下でセキュリティ制約が評価されず → 認証を要求するリソースへの匿名アクセスを許可 → アクセス制御バイパス | Tomcat 9.0.121 / 10.1.46 で修正; [JVNVU#96149019](https://jvn.jp/vu/JVNVU96149019/); 公開 **2026-08-25** (Apache) / JPCERT **2026-08-26** | 広範 Java Web 環境 / 未認証リソースアクセス / JPCERT 公式アドバイザリ |
| CVE-2026-68763 | Apache Tomcat 9.0.x < 9.0.121 / 10.1.x < 10.1.46 | CWE-770 / Important | HTTP/2 でストリームがリセットされた際のバックログ追跡でメモリを解放しない (アロケーションリーク) → 攻撃者がストリームリセットを繰り返す → 無制限メモリ消費 → サーバー DoS | 同上 Tomcat 9.0.121 / 10.1.46; [JVNVU#96149019](https://jvn.jp/vu/JVNVU96149019/); 公開 **2026-08-25** (Apache) / JPCERT **2026-08-26** | リモート無認証 DoS / HTTP/2 有効化 Tomcat 全環境 / バリアントハント: Jetty/Netty 等の HTTP/2 実装で同種リーク要確認 |
| CVE-2026-68569 | Apache Tomcat 9.0.x < 9.0.121 / 10.1.x < 10.1.46 | CWE-287 / Important | DataSourceRealm / JDBCRealm に空のパスワードで認証リクエストが来た際に認証成功として扱う (fail-open) → 空パスワードを送るだけでデータベース認証をバイパス → 管理機能または DB realm 保護リソースへの不正アクセス | 同上; [JVNVU#96149019](https://jvn.jp/vu/JVNVU96149019/); 公開 **2026-08-25** (Apache) / JPCERT **2026-08-26** | DB realm 使用 Tomcat 環境で緊急対応 / 空パスワードによる認証バイパス / 同仕様の他 Java Realm 実装への水平伝播確認推奨 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|---|---|---|---|---|
| 2026-08-26 | JVNVU#96149019 / Apache Tomcat 複数 CVE | Apache Tomcat に認証バイパス・セキュリティ制約バイパス・HTTP/2 DoS 等 10 件の脆弱性 — 9.0.121 / 10.1.46 以降で修正 | Important 複数 | [JVNVU#96149019](https://jvn.jp/vu/JVNVU96149019/) |
| 2026-08-27 | JVN (JPCERT 調整済み) | Rakuten Kobo Desktop (Windows 版) インストーラが DLL を安全でない方法でロードする可能性 — 同一ディレクトリに悪意ある DLL が存在する場合に任意コード実行の恐れ | CVSS 未公表 | [JVN (JPCERT)](https://jvn.jp/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| bloomberg.com / yahoo.finance.com / cnbc.com / forbes.com (NVIDIA Hugging Face $12.9B) | WebSearch スニペット 2026-08-26〜27 確認 ✓; Forbes URL `/2026/08/27/` 確認 ✓; TechCrunch `/2026/08/26/` 確認 ✓; 正式署名未了・破談の可能性も確認 ✓ |
| openai.com / 9to5mac.com (ChatGPT for Teachers 拡大) | WebSearch スニペット 2026-08-26 確認 ✓; OpenAI Blog URL 確認 ✓; 55 学区・30 万人・16 州プライバシー協定確認 ✓ |
| bloomberg.com / yahoo.finance.com / the-decoder.com (Qwen3.8-Flash-Next) | WebSearch スニペット 2026-08-26 公開確認 ✓; MarkTechPost URL `/2026/08/26/` 確認 ✓; 125B-MoE / 6B active / Qwen4 プレビュー確認 ✓ |
| ibm.com / the-decoder.com (Granite 4.2) | WebSearch スニペット 2026-08-26 確認 ✓; IBM Research Blog URL 確認 ✓; 3B/8B/30B / Apache 2.0 / エージェント RL 確認 ✓ |
| cnbc.com / techcrunch.com / bloomberg.com (AI cyber defense letter) | WebSearch スニペット 2026-08-27 確認 ✓; 116 社署名・「limited window」引用 ✓; クリティカルインフラ提言内容確認 ✓ (直接 WebFetch は EGRESS_BLOCKED) |
| thehackernews.com (Amazon Kiro prompt injection) | WebSearch スニペット 2026-08-27 確認 ✓; thomasharris6 blog URL `/2026/08/27/` 確認 ✓; Kiro IDE 0.7.45 → 1.0.337 修正・steering file 手法確認 ✓ (直接 WebFetch EGRESS_BLOCKED) |
| cbsnews.com / theregister.com / cybernews.com (Boston Scientific) | WebSearch スニペット 2026-08-26 確認 ✓; fox9.com URL `aug-26-2026` 確認 ✓; 8/25 検知・8/26 開示確認 ✓ |
| cisa.gov (KEV 6件追加) | WebSearch スニペット 2026-08-26 確認 ✓; CISA URL `/2026/08/26/` 確認 ✓; 6 CVE 全件 (CVE-2026-8452 / CVE-2015-3246 / CVE-2015-5287 / CVE-2019-1068 / CVE-2021-23758 / CVE-2022-0995) 確認 ✓ |
| helpnetsecurity.com / watchtowr.com / securityweek.com (NetScaler CVE-2026-8452 詳細) | WebSearch スニペット 2026-08-27 確認 ✓; WatchTowr URL 確認 ✓; 36 件 / 12 日間 / webshell x.php/z.php 確認 ✓ (直接 WebFetch EGRESS_BLOCKED) |
| thehackernews.com / bleepingcomputer.com / techcrunch.com / therecord.media (TeamPCP 逮捕) | WebSearch スニペット 2026-08-27 確認 ✓; 複数独立ソース一致 ✓; Gaebler/Thomson 14 罪状 / 8/27 Perth 出廷確認 ✓ |
| cybersecuritynews.com / gbhackers.com / netnewsledger.com (Aurora Cursor AI) | WebSearch スニペット 2026-08-27 確認 ✓; 露出サーバーから Cursor ログ・BloodHound 等回収確認 ✓ |
| cybersecuritynews.com / jvn.jp (Apache Tomcat JVNVU#96149019) | WebSearch スニペット 2026-08-26 公開確認 ✓; CVE-2026-65182/68763/68569 識別子確認 ✓; JPCERT 公開日 Aug 26 確認 ✓ (直接 WebFetch EGRESS_BLOCKED) |
| jvn.jp (Rakuten Kobo Desktop) | WebSearch スニペット 2026-08-27 確認 ✓ (直接 WebFetch EGRESS_BLOCKED) |

### 集計サマリ

- **巡回ソース数**: 約 40
- **採用件数**: AI=6 / Security=5 / CVE=4 / 国内=2
- **除外理由内訳**:
  - 採用窓外 (公開日 <2026-08-26): GPT-Live (2026-07-08); Gemini 3.7 Flash (2026-08-13); Oracle CVE-2026-21962 KEV 追加 (2026-08-24); N-able CVE-2026-18577 KEV 追加 (2026-08-03); Silverstripe CVE-2026-54718/54721 (June 2026 release); pantheon-agents GHSA-93qj-5q5v-3c2h (June 2026 Hades 攻撃); LibreNMS GHSA-7w8c-qgxg-m7jx (2026-06-15); Crossplane GHSA-mf7q-r4rv-jv94 (2026-06-15)
  - 重複 (excluded_set): CVE-2026-60004 Gitea KEV (08-27 digest); CVE-2026-65105 NemoClaw (08-27); CVE-2026-77537/77554 Ubiquiti (08-27); GHSA-c937-9ccf-7mq9 NebulaGraph (08-27); GHSA-hfpc-7mr4-p297 whichllm (08-27); GHSA-326h-rh66-6gp9 Spring Security WebAuthn (08-27); OpenAI Jalapeño chip (08-27); Amazon MTurk shutdown (08-27); Anthropic Claude memory (08-27); Google Gemini Enterprise for Legal (08-27); Mistral HUMAIN (08-27); Waymo Munich (08-27); FBI QTFY China APT (08-27); Adobe Campaign CVE-2026-76197/76193/76195 (08-26); Chainlit CVE-2026-45018/45019 (08-26); Marimo CVE-2026-75149 (08-26); miniOrange CVE-2026-75218 (08-26); Lambda $3B pre-IPO (08-26); OpenAI GPT-5.6 Kiro統合 (08-26); Anthropic Claude Tag Slack update (08-26)
  - 取得失敗ソース (EGRESS_BLOCKED): thehackernews.com, techcrunch.com, bleepingcomputer.com, helpnetsecurity.com, securityweek.com, cnbc.com, bloomberg.com, the-decoder.com, cisa.gov, nvd.nist.gov, jvn.jp, jpcert.or.jp, ipa.go.jp, watchtowr.com, gbhackers.com, cybernews.com, cbsnews.com

</details>

---

*生成: keda-digest-bot / 2026-08-28 05:06 JST*
