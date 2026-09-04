# KEDA Daily Digest — 2026-09-05 (JST)

> 採用範囲: 公開日 2026-09-03 〜 2026-09-05
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

OpenAI が GPT-6 Astra（$10/$50 per 1M）を公開し Greg Brockman が「AGI 時代の幕開け」を宣言、同日に米議会では Stop Rogue AI Act（AIエージェント管理標準義務化）が超党派で提出された。CVE 面では Chrome V8 zero-day (CVE-2026-85046、CVSS 8.8) の野外悪用と Cisco Nexus 9000 (CVE-2026-20212、CVSS 9.8) の AI データセンター基幹スイッチへの root RCE が今週最大の注目脆弱性となり、WordPress プラグイン2件への 440K+ 悪用試行も Wordfence から報告された。Manchester Airports Group では FulcrumSec が身代金拒否後に 8.8M 人分データを公開、Hugging Face Transformers には trust_remote_code バイパス脆弱性 CVE-2026-80047 が CERT/CC から勧告された。

## AI 関連ニュース

- **[2026-09-03]** ['Welcome to the AGI era': OpenAI が GPT-6 Astra を発表 — コンピュータ操作型アジェンティック・$10/$50 per 1M、Daybreak Access 先行→ ChatGPT Plus/Pro/Business/Enterprise+API 展開予定](https://www.axios.com/2026/09/03/openai-astra-gpt-6-agi-brockman) — ブラウザ・スプレッドシート・デスクトップアプリを横断する multi-step ワークフローを自律実行。Greg Brockman 社長が「AGI 到来」を宣言し、サイバーセキュリティ・科学・ソフトウェアエンジニアリング分野で「世代的跳躍」と評価。価格は入力 $10/M・出力 $50/M で GPT-5.6 プロモ価格の 2.5 倍。 *(Axios / Fortune / VentureBeat / 9to5Mac)*

- **[2026-09-03]** [Stop Rogue AI Act (AI AGENT Act S.5051) を Gottheimer & Lawler が超党派提出 — NIST に AIエージェント管理標準の1年以内の策定を義務付け](https://www.axios.com/2026/09/03/house-bill-ai-agents-security) — HuggingFace 侵害を直接の契機に提出。AIエージェントの連続可読インベントリ・改ざん防止アクションログ・CISA 連携を要件化。Palo Alto Networks・GoDaddy・Infoblox・Alliance for Secure AI が支持表明。法案成立から1年以内に NIST が標準を作成する構成。 *(Axios / Congress.gov)*

- **[2026-09-03]** [Crusoe Cloud が $3B 調達・評価額 $30B に急騰 — Jane Street との $13B / 5年 GPU クラウド契約後](https://techcrunch.com/2026/09/03/crusoe-reportedly-raises-3b-at-a-30b-valuation/) — OpenAI・Microsoft・Meta に GPU インフラを供給するデータセンター事業者が Series F を完了。Atreides Management・Valor Equity Partners 共同主幹、Mubadala Capital（アブダビ SWF 傘下）も参加。前回調達（2025年10月 $1.38B/$10B）から10ヶ月で評価額3倍。 *(Bloomberg / TechCrunch)*

- **[2026-09-04]** [HUMAIN、humain-m3（428B パラメータ Arabic MoE）をリリース — Arabic 7 公開ベンチマーク首位、GPT-6 Astra・Claude Opus 5 を上回る](https://llm-stats.com/ai-news) — PIF 傘下のサウジ AI 企業 HUMAIN が中国 MiniMax アーキテクチャをベースに 1 兆トークン超の Arabic ネイティストテキストで追加学習したモデルを公開。理解・知識・言語品質・事実性・RAG を含む 7 指標で Arabic 特化ベンチマーク首位と報告。 *(Tech Startups / Bloomberg)*

- **[2026-09-03]** [Hugging Face Transformers CVE-2026-80047 — trust_remote_code 確認前にリモートコードをキャッシュ書き込み、232M DL が対象と CERT/CC が勧告](https://kb.cert.org/vuls/id/456290) — load_custom_generate() が resolve_trust_remote_code() 評価前に get_cached_module_file() でリモート Python モジュールを HF キャッシュへ書き込む。ユーザーが「信頼しない」と回答後も攻撃者制御コードがディスクに残存し、後続の信頼済みモデルロード時に実行リスクが継続。Transformers 4.49.0〜5.8.1 が対象。 *(CERT/CC VU#456290 / GBHackers / CyberSecurityNews)*

## セキュリティ関連ニュース

- **[2026-09-03]** [Chrome V8 zero-day CVE-2026-85046（CVSS 8.8）の野外悪用を確認、Stable Channel で即日パッチ — 2026年6番目の Chrome ゼロデイ](https://www.bleepingcomputer.com/news/security/google-warns-of-new-chrome-zero-day-flaw-exploited-in-attacks/) — V8 の type confusion により sandbox 内で任意コード実行が可能。Salvatore Gulizia が 8/4 に報告（Bug Bounty $1,000）。Google は追加攻撃者の逆解析を防ぐため Chromium bug report を当面非公開化、更新即時適用を強く推奨。 *(BleepingComputer / Help Net Security / The Hacker News)*

- **[2026-09-04]** [WordPress Super Forms (CVE-2026-14894 CVSS 9.8) と Elementor Pro (CVE-2026-32475 CVSS 9.8) への合計 440K+ 悪用試行 — PHP webshell 投下経由 RCE を Wordfence が報告](https://thehackernews.com/2026/09/over-440000-exploit-attempts-target.html) — Super Forms は array 形式でファイルアップロードを送信するとタイプ検証がバイパスされ `/wp-content/uploads/elementor/forms/` に PHP ファイルを書き込み実行。Elementor Pro も同経路で 200K+ 試行。uploads ディレクトリ内の不審 PHP ファイルを即時点検し最新版へアップグレードを推奨。 *(The Hacker News / Wordfence / GBHackers)*

- **[2026-09-03]** [[続報] Manchester Airports Group：FulcrumSec が身代金拒否後に 8.8M 人分・550GB データを公開 — Iterable 管理者 API キーがフロントエンド JS に平文露出していた経路で侵入](https://www.securityweek.com/manchester-airports-group-data-on-8-8-million-people-leaked-after-ransom-refusal/) — Manchester・Stansted・East Midlands の 3 空港利用者のメール・電話番号・購買・車両ナンバーが HIBP に収録。FulcrumSec は「86GB 圧縮」が実際は展開時 640GB と判明したと説明。管理者キーが各空港ルートドメインの JS に平文で埋め込まれていたことが初期侵入経路。 *(SecurityWeek / BleepingComputer)*

- **[2026-09-04]** [HPE が ArubaOS-CX の 31 脆弱性にパッチ — CVE-2026-73749 (CVSS 9.8) ほか独立した2経路の未認証 RCE を含む](https://www.techtimes.com/articles/326586/20260904/hpe-patches-arubaos-cx-two-independent-no-credentials-rce-paths-found-same-bulletin.htm) — CVE-2026-73749（バッファオーバーフロー、ネットワーク到達可・認証不要）と CVE-2026-73782（フォーマット文字列インジェクション、隣接ネットワーク・認証不要）の2経路が同一 Bulletin に収録。High (CVSS 8.1〜8.8) 計 29 件も同時修正。野外悪用は未確認。 *(TechTimes / BleepingComputer / CSA Singapore)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 today-2 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先
> ※ CVE-2026-20212 (09-02 公開) と CVE-2026-73749 (09-01 公開) は採用窓外だが過去ダイジェスト未収録のためキャッチアップ採用

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-85046 | Google Chrome (V8) ≤ Stable 09-02 以前 | CWE-843 / CVSS 8.8 | 細工した JS によって V8 の JIT 型推論が混乱→メモリオブジェクトの型を誤認識→任意読み書きから sandbox 内任意コード実行 | [Stable Channel 09-03 update](https://chromereleases.googleblog.com/) | 実エクスプロイト確認 / 2026年6番目の Chrome ゼロデイ |
| CVE-2026-20212 | Cisco Nexus 9000 シリーズ (Silicon One ASIC 搭載: N9K-C9804 / N9K-C9808 ほか計 10 機種) | CWE-? / CVSS 9.8 | Layer 3 デフォルト VRF でポート 43210/43211 に到達可能な未認証攻撃者が細工 TCP ペイロードを送信→デーモンが root 権限で実行→任意 OS コマンド実行 + S1HAL プロセスクラッシュ → DoS (スイッチリロード) | [Cisco PSIRT Advisory 09-02](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/) (commit 不明) | CVSS 9.8 / AI データセンター基幹スイッチ / 野外悪用 09-02 時点未確認 |
| CVE-2026-73749 | HPE Aruba Networking AOS-CX (複数バージョン) | CWE-120 / CVSS 9.8 | 未認証リモート攻撃者が特定デーモンに細工パケットを送信→バッファ境界検証なしで書き込み→特権コード実行 / 同 Bulletin に CVE-2026-73782 (format-string、隣接ネット) も収録 | [HPE Security Advisory](https://support.hpe.com/hpesc/public/docDisplay?docId=hpesbhf04779en_us) (commit 不明) | CVSS 9.8 / 同一 Bulletin に未認証 RCE 2 経路 / 野外悪用未確認 |
| CVE-2026-80047 | Hugging Face Transformers 4.49.0〜5.8.1 (PyPI) | CWE-273 / Medium | load_custom_generate() が resolve_trust_remote_code() 評価前に get_cached_module_file() でリモート Python モジュールを HF キャッシュへ書き込む→ユーザー拒否後も攻撃者制御コードがディスクに永続→後続の信頼済みモデルロード時に実行リスク継続 | [Transformers v5.8.2+](https://github.com/huggingface/transformers/releases) (commit 不明) | 232M DL / AI/ML パイプライン供給チェーン / CERT/CC VU#456290 / trust_remote_code バイパスパターンの他 ML フレームワークへのバリアント候補 |
| CVE-2026-14894 | WordPress Super Forms ≤ 6.3.313 (Drag & Drop Form Builder) | CWE-434 / CVSS 9.8 | ファイルアップロードフィールドで array 第1要素に空ファイル・第2要素に .php を送信→タイプ検証が最初の空要素のみ確認→PHP 実行ファイルを `/wp-content/uploads/elementor/forms/` に書き込み→RCE | [v6.3.314](https://wordpress.org/plugins/super-forms/) (commit 不明) | 440K+ 悪用試行 (Wordfence 09-04) / 2026-07-14 以降継続的に悪用 |

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-09-03 | JVNVU#92139835 (CVE-2026-54876) | OpenSSL 4.0/3.6/3.5/3.4/3.0 のOCSPレスポンス検証で悪意TLSサーバが単一エントリ欠落応答を送付するとクライアント側でメモリリークが発生 | Low | [JVNVU#92139835](https://jvn.jp/vu/JVNVU92139835/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 25+（Axios, Fortune, VentureBeat, 9to5Mac, Bloomberg, TechCrunch, CNBC, Congress.gov, BleepingComputer, The Hacker News, Help Net Security, SecurityWeek, GBHackers, Wordfence, CERT/CC kb.cert.org, TechTimes, Cisco PSIRT, HPE Security Advisory, CSA Singapore, llm-stats.com, Tech Startups, OffSeq/Threat Radar, JVN/JPCERT 各サイト）
- 採用件数: AI=5 / Security=4 / CVE=5 / 国内=1
- 除外理由内訳:
  - 重複 (excluded_set 該当): MAI-Transcribe-2（09-04 digest 済み）、Anthropic Claude Commerce Agents（09-04 digest 済み）、HuggingFace+NVIDIA Open Data for Agents（09-04 digest 済み）、Azure East US 障害（09-04 digest 済み）、Anthropic EFS（09-04 digest 済み）、Qwen3.8-Max-0902（09-04 digest 済み）、Palo Alto Networks/Console 買収（09-04 digest 済み）、Fable 5.1/Mythos 5.1（09-03 digest 済み）、AISLE/curl 6 CVEs（09-03 digest 済み）、OpenAI Astra Preparedness Critical 閾値（09-03 digest 済み）、Gemini 3.8 Flash（09-03 digest 済み）、CISA KEV 7件追加 09-02（09-04 digest 済み）、Sangoma CVE-2026-9586（09-04 digest 済み）、Kestra CVE-2026-49869（09-04 digest 済み）、Starlette CVE-2026-48710（09-04 digest 済み）、LiteLLM CVE-2026-59822（09-04 digest 済み）、SonicWall SMA1000 CVE-2026-83548/83549（09-03/04 digest 済み）、Exchange CVE-2026-62911（09-03 digest 済み）、METR API key theft（09-03 digest 済み）、PaperCut CVE-2026-82078/81578（09-03 digest 済み）、FireAnt/UNC3886（09-01 digest 済み）、Silver Fox ValleyRAT（09-01 digest 済み）
  - 窓外（公開日 < 2026-09-03）: Zimbra CVE-2026-73570 KEV 追加（08-21）、Elementor Pro CVE-2026-32475 パッチ（08-19）、OpenSSL CVE-2026-54876 元 CVE 公開（08-06）
  - キャッチアップ採用（採用窓外だが過去ダイジェスト未収録）: CVE-2026-20212 (Cisco 09-02 公開; 09-04 digest 採用窓内だが未収録)、CVE-2026-73749 (HPE 09-01 公開; 09-03 digest 採用窓内だが未収録)
  - 日付不明・検証不可: Cisco CVE-2026-20212 修正コミット hash（Cisco PSIRT advisory のみ確認）、HPE CVE-2026-73749 修正コミット（HPE HPESC advisory のみ確認）、CVE-2026-80047 修正コミット（GitHub releases タグのみ確認）
- 取得失敗ソース（EGRESS_BLOCKED）: venturebeat.com, helpnetsecurity.com, securityonline.info, techstartups.com, bleepingcomputer.com, thehackernews.com, jvn.jp, jpcert.or.jp, ipa.go.jp（WebSearch スニペット・ミラーサイト経由で情報補完）

</details>
