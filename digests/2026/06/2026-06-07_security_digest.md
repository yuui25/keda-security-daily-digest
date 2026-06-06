# KEDA Daily Digest — 2026-06-07 (JST)

> 採用範囲: 公開日 2026-06-05 〜 2026-06-07
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

AI 大手 4 社 (OpenAI/Anthropic/Google/Microsoft) が米議会に DNA 合成スクリーニング義務化を共同要請し、Anthropic は再帰的自己改善リスクを根拠に「グローバル AI 開発一時停止」機構の提案論文を公開した。セキュリティ面では Miasma ワームが Claude Code・Gemini CLI・Cursor・VS Code の自動実行フックを悪用して 73 本の Microsoft GitHub リポジトリを汚染し、AI コーディング環境が新たなサプライチェーン侵害ベクターとして確立された。depthfirst の自律 AI エージェントは FFmpeg で 15〜20 年前から潜在していた未知のヒープ/スタックオーバーフロー 21 件 (CVE-2026-39210〜39218 他) を約 1,000 ドルのコストで発見し、AI 駆動脆弱性発見のコスト曲線の急落を実証した。

---

## AI 関連ニュース

- **[2026-06-05]** [OpenAI・Anthropic・Google DeepMind・Microsoft AI 各 CEO が米議会に DNA/RNA 合成スクリーニング義務化を共同要請 — AI が生物兵器合成に必要な専門知識閾値を「5 年前には存在しなかった経路」まで引き下げたと警告し、全合成 DNA/RNA 業者への受注前スクリーニング・顧客確認・危険配列データベース照合の法制化を求める](https://fortune.com/2026/06/05/openai-anthropic-microsoft-ceos-congress-bioweapon-safeguards/) — Sam Altman (OpenAI)・Dario Amodei (Anthropic)・Demis Hassabis (Google DeepMind)・Mustafa Suleyman (Microsoft AI) が Foundation for American Innovation / Institute for Progress 主催の書簡に連名；生命科学・国家安全保障の専門家も多数署名 *(Fortune / Yellow.com / CryptoBriefing / NerdyInfo)*

- **[2026-06-05]** [Anthropic が「グローバル AI 開発一時停止」の協調検証機構を提案 — 2026 年 Q2 には Anthropic 自社コードの 80% 超が Claude によって書かれ・エンジニア 1 人あたりのマージ量が 2024 年比 8 倍と判明、再帰的自己改善が人間の監督能力を追い越す前に主要ラボが合意できる速度低減・検証スキームの設計を求める](https://www.aljazeera.com/economy/2026/6/5/anthropic-urges-ai-labs-to-pause-warns-humans-risk-losing-control) — Jack Clark (共同創業者) と Marina Favaro (Anthropic Institute 所長) が執筆；米中含む主要ラボが秘密裏に開発継続する抜け穴を塞ぐための相互検証機構が設計上の最難関と指摘 *(Al Jazeera / USNews / SiliconANGLE / RTE / CryptoBriefing)*

- **[2026-06-05]** [depthfirst の自律 AI エージェントが FFmpeg 全コード 150 万行を約 1,000 ドルで走査し 21 件のゼロデイを発見 — 9 件が CVE-2026-39210〜39218 として採番済み。2003 年に導入された TS デマクサーのヒープ OOB を筆頭に 15〜20 年前のバグが多数含まれ、再現 PoC も完備](https://depthfirst.com/research/21-zero-days-in-ffmpeg) — depthfirst はオープンソース向けに最大 500 万ドルのクレジットを提供する Bounty プログラムも発表；Anthropic Claude Mythos Preview の数千件ゼロデイ発見と独立した事例であり、AI 脆弱性発見のコスト曲線が急落している実態を示す *(The Hacker News / depthfirst.com / BusinessWire)*

- **[2026-06-05]** [Miasma ワームが Claude Code・Gemini CLI・Cursor・VS Code の自動実行フック/ルールファイルを悪用して Azure/Azure-Samples 他 73 本の Microsoft GitHub リポジトリを汚染 — フォルダを開いた開発者の AWS/Azure/GCP/Kubernetes/npm/GitHub 認証情報を窃取し、書き込み権限のある全リポジトリに `.claude`・`.cursor`・`GEMINI.md` として自己複製](https://thehackernews.com/2026/06/miasma-worm-hits-73-microsoft-github.html) — 侵害済みコントリビューターによる Azure/durabletask コミットから 105 秒で GitHub が全 73 リポジトリを無効化；Mini Shai-Hulud ワーム (TeamPCP, 2026-05) の亜種と評価され、IDE 自動実行フックがサプライチェーン侵害の新たな永続化ベクターとして確立された *(The Hacker News / StepSecurity / SafeDep / The Next Web)*

- **[2026-06-05]** [CISA Acting Director Andersen: Trump AI EO (6/2 署名) の実施措置として AI・LLM 特化の拘束的運用指令 (BOD) を「今週中」に連邦機関へ発令すると明言 — LLM への特権アクセス管理・エージェント攻撃面縮小・脆弱性緩和プロセス自動化の義務化と、AI サイバーセキュリティクリアリングハウス設立・フロンティアモデルへの 30 日前政府アクセス・官民脆弱性情報共有を 30 日以内に整備するよう各省庁に要求](https://therecord.media/cisa-directive-for-ai-exec-order-release) — BOD の重点は「LLM・AI エージェントの脆弱性特定と緩和の自動化」と発表；連邦機関が必要な場合は Claude Opus 等フロンティアモデルへのアクセスを提供する新条項も含まれる *(The Record / Federal News Network / letsdatascience.com)*

---

## セキュリティ関連ニュース

- **[2026-06-05]** [Miasma ワームが 73 本の Microsoft GitHub リポジトリを汚染 — Azure/durabletask の侵害済みコントリビューターコミットから Bun ベース 4.3 MB ステージドドロッパーが展開、盗取した GitHub トークンで書き込み可能な全リポジトリに自己増殖するまでの所要時間は 105 秒](https://thehackernews.com/2026/06/miasma-worm-hits-73-microsoft-github.html) — GitHub が 49 本の Microsoft/Azure/Azure-Samples リポジトリ含む計 73 本を自動無効化；Miasma はIDEルール/フックを滑走路にするためコード署名・CI スキャン・SAST をすべてすり抜ける点が特に危険 *(The Hacker News / StepSecurity / SafeDep / CybelAngel / Hackread)*

- **[2026-06-05]** [FIFA ワールドカップ 2026 (6/11 開幕) 向けサイバー詐欺が本格化 — Group-IB が 4,300 件超の偽 FIFA ドメイン・FortiGuard が 13,000 件超の World Cup テーマドメインを確認、AI 最適化フィッシング・バンキングマルウェア内蔵の海賊版ストリーミングアプリ・FIFA ログイン完コピ偽サイトによる 260 件の FIFA 従業員認証情報と 270,000 件超のファン認証情報が盗取済み](https://thehackernews.com/2026/06/fifa-world-cup-2026-scams-are-already.html) — チケット詐欺のみで 710 万〜4.74 億ドルの被害推定；FIFA.com と同一サーバーから画像を読み込む偽サイトがアセットスキャナーを回避するケースも確認、FBI が IC3 経由で PSA を公開 *(The Hacker News / Group-IB / FortiGuard Labs / Bitdefender / FBI IC3 / The Next Web)*

- **[2026-06-05]** [Everest Forms Pro (WordPress プラグイン, 約 4,000 インストール) の CVE-2026-3300 (CVSS 9.8) が積極悪用中 — 非認証攻撃者が Calculation Addon の `process_filter()` で `sanitize_text_field()` が単引符をエスケープしない欠陥を突き PHP `eval()` に任意コードを注入し完全サイト乗っ取り、累計 29,300 件超の試行をブロック済み](https://thehackernews.com/2026/06/hackers-exploit-critical-everest-forms.html) — 最多ペイロードは管理者アカウント「diksimarina (diksimarina@gmail.com)」の作成；パッチ v1.9.13 は 2026-03-18 リリース済みだが多数の未適用インスタンスが存在 *(The Hacker News / SentinelOne / FreshySites / Infosecurity Magazine)*

- **[2026-06-05]** [Help Net Security が June 2026 Patch Tuesday (6/9 予定) の事前予報を公開 — Exchange Server CVE-2026-42897 (OWA XSS/野外悪用中, 5/14 開示) の修正パッチと Secure Boot 2011 証明書 dbx 更新 (最終期限 6/26) を含む約 118 件の修正が予定。6/26 を過ぎると Secure Boot 新規マルウェアブラックリスト更新が永続停止するリスクあり](https://www.helpnetsecurity.com/2026/06/05/june-2026-patch-tuesday-forecast/) — dbx 更新で起動失敗する組織が 2〜5% と試算されるため事前テストが必須；Adobe Creative Cloud (inCopy/inDesign/Photoshop) の更新も同日配布予定 *(Help Net Security / Zecurit)*

- **[2026-06-05]** [CISA/FBI/NSA/エネルギー省が合同警告: 米国内 900 台超の自動タンクゲージ (ATG) がインターネット公開状態で攻撃継続中 — Shadowserver が port 10001 上に 1,061 IP を確認。ハードコードクレデンシャル・認証バイパス・SQLi・OS コマンド実行で設定改ざん・アラート無効化・燃料タンク損傷の恐れ、ガソリンスタンドや化学施設を含む重要インフラが対象](https://www.cisa.gov/resources-tools/resources/cisa-and-partners-urge-hardening-automatic-tank-gauge-systems) — 攻撃者がアラートを意図的に無効化することで燃料漏出・爆発・機器の永続破損を引き起こす可能性；VPN/ファイアウォールによる即時アクセス遮断・デフォルトパスワード変更を推奨 *(CISA / FBI / NSA / BleepingComputer / IC3)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-05 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-39210 | FFmpeg ≤ 7.1.1 (libavformat TS demuxer / `sdt_section` パーサ) | CWE-122 / TBD | TS デマクサーの `sdt_section` パーサが読み取りオフセット前に長さチェックを行わない → ヒープ境界外書き込み → クラフト .ts ファイル処理で DoS / RCE | [FFmpeg Security](https://ffmpeg.org/security.html) (patch review 中・commit 番号未確定) | 2026-06-05〜06 公開 / 2003 年導入バグが 23 年間 500 万回のテストヒットで未検出 / AI 自律エージェント発見 / libav・GStreamer・VLC への水平バリアントハント推奨 |
| CVE-2026-39211〜39218 (8件) | FFmpeg ≤ 7.1.1 (各種パーサ・デマクサー・VP9 デコーダ) | CWE-121/787 / TBD | 各パーサ/デマクサーが可変長入力サイズを検証せず固定サイズ領域に書き込む → スタック/ヒープバッファオーバーフロー → クラフトメディアファイルで DoS / RCE の可能性 | [FFmpeg Security](https://ffmpeg.org/security.html) (patch review 中・commit 番号未確定) | 2026-06-05〜06 公開 / depthfirst AI スキャン ($1,000) が一括発見 / 15〜20 年前の古いバグ群 / メディア処理 OSS 全般 (libav・GStreamer・FFmpeg フォーク) へのバリアントハント推奨 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|

> 直近2日間 (2026-06-05〜06-07) に該当する新規国内脆弱性・インシデント情報は確認できませんでした。

*備考: JPCERT/CC の 2026-06-05 公開アドバイザリ (TP-Link 複数製品の平文通信 JVN#70631953) は前日 (2026-06-06) ダイジェストに採用済みのため除外。JVN・IPA への直接フェッチは 403 のため WebSearch 経由で確認。*

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 30 ソース (Fortune, Al Jazeera, USNews, The Hacker News, The Record, Federal News Network, depthfirst.com, BusinessWire, StepSecurity, SafeDep, The Next Web, BleepingComputer, SecurityWeek, Help Net Security, CISA, FBI IC3, Group-IB, FortiGuard, SentinelOne, FreshySites, Infosecurity Magazine, Hackread, CybelAngel, Yellow.com, CryptoBriefing, SiliconANGLE, RTE, letsdatascience.com, FFmpeg Security, NVD 他)
- 採用件数: AI=5 / Security=5 / CVE=2行 (CVE-2026-39210 および 39211〜39218) / 国内=0
- 採用件数が目安 (AI/Security 各 8〜12件) を下回った理由: 採用窓 (2026-06-05〜07) が週末+WWDC 前日に重なり新規ニュースリリースが少ない。特に AI 大手の主要アナウンス (Google I/O は 5/19、WWDC は 6/8 開幕) が窓外に集中。
- CVE 件数が少ない理由: 主要 OSS/ベンダーの CVE 公開日を NVD・GHSA 等で裏取りした結果、6/5 以降に「実際に公開」されたものは FFmpeg AI 発見 CVE のみ確認可能。GHSA の「Jun 5」表示は多くがラベル更新日であり実公開日は 5 月だった (例: CVE-2026-48017 DbGate=5/22、CVE-2026-47732 Twig=5/20)。
- 除外理由内訳:
  - 採用窓外 (< 2026-06-05): Anthropic IPO S-1 提出 (06-01) / Claude Opus 4.8 リリース (05-28) / DARPA/NSF AI Forge 発表 (06-03) / FlutterShell macOS バックドア Unit42 開示 (06-02) / CVE-2026-41283 OpenStack Mistral RCE 9.9 (oss-security 06-03) / CVE-2026-42897 Exchange OWA XSS (05-14) / CVE-2026-44578 Next.js SSRF (05-11) / CVE-2026-46725 TYPO3 RCE (05-20) / CVE-2026-46670 YesWiki SQLi (5 月) / CVE-2026-47731 AIT-Core path traversal (05-19)
  - 重複 (excluded_set 直近7日): Chrome 149 429 CVE (06-06 digest) / Cisco SD-WAN CVE-2026-20245 (06-06) / Cisco Unified CM CVE-2026-20230 (06-06) / PCPJack SMTP リレー (06-06) / Adversa AI AIRQ (06-06) / MCP Security June 2026 (06-06) / TA4922 LLM マルウェア (06-06) / CISA Mirasvit CVE-2026-45247 KEV (06-05) / IronWorm npm 36パッケージ (06-05) / HTTP/2 Bomb CVE-2026-49975 (06-05) / Toronto AI worm arXiv:2606.03811 (06-05) / OpenStack Ironic CVE-2026-48681 (06-05) / Nightmare Eclipse 第二研究者 (06-05) / Anthropic Partner Network (06-05) / Google Gemini Android 間接プロンプトインジェクション (06-05) / TP-Link JVN#70631953 (06-06) / Miasma npm TeamPCP (06-02 出来事・06-05 excludedで重複判定なし但し GitHub版は別事象として採用)
  - 日付不明/確認不可: CISA BOD 発令の正確な日付 (letsdatascience が "issued" と報道するが具体日不確認) / FFmpeg CVE-2026-39210〜39218 の正式 NVD 掲載日 (403 でフェッチ不可) / 米国 ATG 関連 BleepingComputer 記事の正確な掲載日
  - 判断除外: Gemini 3.5 Pro (GA 未発表・まだ限定プレビュー) / Apple WWDC (6/8 開幕前) / Android June Bulletin 個別 CVE (Samsung Exynos/MediaTek 固有かつ Local only・低スコアのため優先度低)
- 取得失敗ソース (HTTP 403): CISA.gov 個別ページ / thehackernews.com 個別記事 / bleepingcomputer.com 個別記事 / helpnetsecurity.com 個別記事 / piyolog.hatenadiary.jp / jvn.jp / nvd.nist.gov 詳細ページ / depthfirst.com 個別記事 / fortunate.com 個別記事 / therecord.media 個別記事 — WebSearch スニペット・複数独立メディア記事で内容・日付を補完
- 備考: FFmpeg CVE-2026-39210〜39218 の CVSS/CWE は NVD 未分析のため「TBD」。depthfirst 研究ページ・THN スニペットより bug class を抽出。Miasma の Microsoft GitHub 版 (2026-06-05) は TeamPCP npm 版 (2026-06-02) と別事象として採用。FIFA World Cup 2026 詐欺記事は Group-IB/FortiGuard の研究開示が 6/5 以降に THN 等でまとめて報道されたことを確認して採用 (Group-IB 開示は 6/5)。

</details>
