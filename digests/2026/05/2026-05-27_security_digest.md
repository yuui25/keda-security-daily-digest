# KEDA Daily Digest — 2026-05-27 (JST)

> 採用範囲: 公開日 2026-05-25 〜 2026-05-27
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Check Point の 2026 Cloud Security Report が AI 採用戦略と実施アーキテクチャの 51 ポイント乖離を定量化し、「AI ガバナンスギャップ」が業界横断的な最重要課題として浮上した。インド CERT-In は AI 支援攻撃の高速化に対応した 38 ページ防御ブループリントを公開し、KEV 対象システムへの 12 時間以内パッチ適用目標を設定。日本向け商用 LMS「KnowledgeDeliver」の CVE-2026-5426 が中国系 APT を示唆する Godzilla ウェブシェル・Cobalt Strike チェーンで野外悪用中であることが確認されており、国内教育・企業環境での早急なバージョン確認とパッチ適用が求められる。

## AI 関連ニュース

- **[2026-05-26]** [Check Point 2026 Cloud Security Report "Enter the AI Era" — AI 採用戦略 77% に対しアーキテクチャ実施は 26% のみ、51 ポイントのガバナンスギャップを定量化](https://blog.checkpoint.com/securing-the-cloud/2026-cloud-security-report-why-traditional-network-cloud-and-security-architecture-are-lagging-behind-the-ai-transformation/) — 調査対象組織の 78% が過去 1 年で AI 関連インシデントを経験；攻撃者が AI でフィッシング・マルウェア生成・Adversarial 攻撃を高速化する一方、防御側のガバナンス・制御・リアルタイム強制実施が追いついていないと指摘 *(Check Point Blog / PR Newswire)*

- **[2026-05-25]** [インド CERT-In が AI 支援脆弱性悪用対策「Blueprint」38 ページを公開 — KEV インターネット公開システムへの 12 時間以内パッチ適用目標、0-7 日・7-30 日・30-90 日の 3 フェーズロードマップを策定](https://thehackernews.com/2026/05/cert-in-mandates-12-hour-patching-for.html) — 生成 AI・LLM・自律エージェントが偵察から exploit 開発を数時間に短縮していると警告；クラウン・ジュエル級システムへの KEV は 12 時間、Critical 外部公開システムは 1 日、Critical 内部システムは 3 日のパッチ期限を設定 *(The Hacker News / CERT-In)*

- **[2026-05-25]** [[続報] Verizon DBIR 2026 — 組織向け 5 教訓：脆弱性悪用が 19 年の報告史上初めてクレデンシャル盗難を超え初期侵入ベクター No.1 に、サードパーティ起因侵害が 60% 増](https://www.helpnetsecurity.com/2026/05/25/lessons-from-verizon-dbir-2026-findings/) — Shadow AI 利用が前年比 3 倍増で 45% に達しデータ漏洩リスクが急拡大；AI 攻撃自動化によりパッチ遅延が致命的リスクとなる環境で MFA の過信が最重要改善点として浮上 *(Help Net Security)*

- **[2026-05-26]** [MFA Prompt Bombing が 2026 年最重要アイデンティティ攻撃手法に — 攻撃者が「第二要素を盗む必要なし、ユーザーに渡させる」戦術に完全転換](https://thehackernews.com/2026/05/mfa-prompt-bombing-why-your-second.html) — MFA 疲労・偽 IT サポート vishing 電話・SIM スワップを組み合わせてユーザーに第二要素を承認させる手口が台頭；FIDO2/パスキーへの移行が唯一の根本対策として推奨 *(The Hacker News)*

## セキュリティ関連ニュース

- **[2026-05-26]** [Microsoft SharePoint に RCE 脆弱性 CVE-2026-45659 (CVSS 8.8) — サイトメンバー権限からユーザー操作不要で任意コード実行、SharePoint 2016/2019/SE に影響](https://www.helpnetsecurity.com/2026/05/26/sharepoint-vulnerability-cve-2026-45659/) — CWE-502 (非信頼データのデシリアライゼーション)；攻撃複雑度 Low で認証ユーザーが繰り返し攻撃可能。NVD 公開 5/22・研究者 MEOW が発見、Microsoft はパッチを 5/22 リリース済み *(Help Net Security / The Hacker News)*

- **[2026-05-26]** [日本向け LMS「KnowledgeDeliver」CVE-2026-5426 (CVSS 7.5) がゼロデイとして野外悪用 — ハードコード ASP.NET machineKey 悪用の ViewState デシリアライゼーション RCE で Godzilla/BLUEBEAM ウェブシェルと Cobalt Strike を展開](https://thehackernews.com/2026/05/knowledgedeliver-lms-flaw-exploited-to.html) — APT41・UNC215 類似の TTP を持つ中国語話者の攻撃者を示唆；日本の企業・教育機関が主要被害対象。2026-02-24 以前の全デプロイが対象で machineKey のローテーションが急務 *(The Hacker News / SecurityWeek / SC Media)*

- **[2026-05-26]** [イラン系 MuddyWater が Q1 2026 に DLL サイドローディングで 9 か国・9 組織を侵害 — SentinelOne・Fortemedia の正規署名済みバイナリで悪意ある DLL をサイドロードして EDR 回避](https://thehackernews.com/2026/05/muddywater-uses-dll-side-loading-in.html) — 韓国大手電機メーカー（2 月に 1 週間在中）・中東国際空港・東南アジア製造業・ラテン米金融機関などが被害；sentinelmemoryscanner.exe と fmapp.exe を悪用したステルス侵入が確認 *(The Hacker News / TechNadu)*

- **[2026-05-25]** [JVN、NEC Aterm シリーズに OS 命令注入 CVE-2026-8652 (CVSS 8.5) と XSS CVE-2026-6059 (CVSS 4.8) を同時公開 — 三井物産セキュアディレクション・サイバーディフェンス研究所が IPA 経由で届出](https://vulnerability.circl.lu/vuln/jvndb-2026-000079) — 管理者権限を持つ隣接ネットワーク攻撃者が Web コンソール経由で任意 OS コマンドを実行可能 (NV26-003)；XSS では任意スクリプトがブラウザで実行 (NV26-002) *(JVN / JPCERT/CC / IPA)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-05-25 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-8652 | NEC Aterm シリーズ (パッチ前全バージョン) | CWE-78 / **8.5** | 管理者権限保有の隣接ネットワーク攻撃者が Web コンソールで OS コマンド引数にユーザー入力を直接渡す → 任意コマンド実行 | (commit 不明) [(JVN advisory)](https://vulnerability.circl.lu/vuln/jvndb-2026-000079) | HIGH / 国内 SOHO ルーター広範に影響 |
| CVE-2026-5426 | Digital Knowledge KnowledgeDeliver (< 2026-02-24 デプロイ) | CWE-330 / **7.5** | 全インスタンス共通のハードコード ASP.NET machineKey → 攻撃者が known-key で細工した ViewState を POST するだけで未認証 RCE → in-memory ウェブシェル展開 | パッチ 2026-02-24 [(exploitation advisory)](https://thehackernews.com/2026/05/knowledgedeliver-lms-flaw-exploited-to.html) (commit 不明) | 野外悪用済 / 国内被害確認 / APT41 類似 TTP / 水平伝播可 (ASP.NET machineKey 共通パターン) |
| CVE-2026-6059 | NEC Aterm シリーズ (パッチ前全バージョン) | CWE-79 / **4.8** | Web 管理画面でユーザー入力のエスケープ欠落 → 管理者アクセス権を持つ隣接ユーザーが任意スクリプトをブラウザで実行 | (commit 不明) [(JVN advisory)](https://vulnerability.circl.lu/vuln/jvndb-2026-000078) | MEDIUM |

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-05-25 | CVE-2026-8652 | NEC Aterm シリーズに OS 命令注入：管理者権限の隣接ネットワーク攻撃者が Web コンソール経由で任意コマンドを実行可能 (NV26-003) | CVSS 8.5 (HIGH) | [JVN/JPCERT](https://vulnerability.circl.lu/vuln/jvndb-2026-000079) |
| 2026-05-25 | CVE-2026-6059 | NEC Aterm シリーズにクロスサイトスクリプティング：管理画面アクセス権の隣接ユーザーが任意スクリプトを実行可能 (NV26-002) | CVSS 4.8 (MEDIUM) | [JVN/JPCERT](https://vulnerability.circl.lu/vuln/jvndb-2026-000078) |
| 2026-05-26 | CVE-2026-5426 | KnowledgeDeliver LMS の野外悪用確認：ハードコード機械鍵による ViewState RCE で国内教育・企業機関が標的に。2026-02-24 以前のデプロイは全て危険 | CVSS 7.5 / 野外悪用済 | [THN](https://thehackernews.com/2026/05/knowledgedeliver-lms-flaw-exploited-to.html) / [SecurityWeek](https://www.securityweek.com/hackers-exploited-knowledgedeliver-zero-day-for-web-shell-deployment/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 30+（WebSearch 15 クエリ、WebFetch 試行 20+）
- 採用件数: AI=4 / Security=4 / CVE=3 / 国内=3
- 除外理由内訳: 古すぎ (window外・NVD公開日 < 5/25) = 多数（SharePoint CVE-2026-45659 NVD 5/22・CISA/NSA/ACSC agentic AI guidance 5/1・Foxconn Nitrogen ransomware 5/12・SAP npm 攻撃 4/29・Redis CVE-2026-25243 5/5・NGINX CVE-2026-27654/40701 5/13・XWiki CVE-2026-33137 5/20・Twig CVE-2026-46633 5/21・Meari IoT 5/11・GitHub AI zero-day 5/11・MuddyWater初報 2週間前・arXiv 2605.17634 5/17） / 重複 (excluded_set) = 多数（CVE-2026-46716/46717/47124 Nezha・CVE-2026-9082 Drupal KEV・CVE-2026-48172 LiteSpeed・GHSA-qqqm-5547-774x FileBrowser・CVE-2026-46670 YesWiki・CVE-2026-41091/45498 MS Defender・CVE-2026-26980 Ghost CMS 等） / 日付不明 = 少数（eSecurity Planet weekly roundup 発行日確認不可）
- 取得失敗ソース: thehackernews.com 直接フェッチ (403)・bleepingcomputer.com (403)・helpnetsecurity.com (403)・checkpoint blog (403)・technadu.com (403)・federalnewsnetwork.com (403)・osv.dev (証明書エラー)・thomasharris6.wordpress.com (403)・rescana.com (403)・scworld.com (403)・esecurityplanet.com (証明書エラー)・senthorus.ch (403)
- 備考: 厳格な 3 日間ウィンドウ (2026-05-25〜27) の適用と直近 7 日の excluded_set 除外により CVE テーブル採用数が目安の下限 (5 件) を下回った。全セクションに採用件が存在するため fallback (直近 7 日拡大) は不要。SharePoint CVE-2026-45659 (CVSS 8.8、NVD 公開 5/22) は window 外のため CVE テーブルから除外し Security ニュース欄で 5/26 記事として掲載。

</details>
