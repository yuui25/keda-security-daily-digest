# KEDA Daily Digest — 2026-06-12 (JST)

> 採用範囲: 公開日 2026-06-10 〜 2026-06-12
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Ivanti Sentry の CVSS 10.0 脆弱性 (CVE-2026-10520) が watchTowr PoC 公開から 24 時間以内にバックドア設置の野外悪用に移行し、Shadowserver が 2 インスタンスの実侵害を確認した。ShinyHunters は Oracle PeopleSoft のゼロデイ (CVE-2026-35273, CVSS 9.8) を「ガジェットチェーン」で悪用し 100 組織超・50 万件の学生記録を窃取; University of Nottingham が 6/11 に侵害を公式確認した。AI 面ではリリース翌日に Claude Fable 5 がジェイルブレークされて安全分類器の実効性に疑問符が付くとともに、AI エージェント構築プラットフォーム Langflow の CVE-2026-5027 が約 7,000 インスタンスで非認証 RCE として積極悪用されており、AI インフラへの直接攻撃が日常化している。

---

## AI 関連ニュース

- **[2026-06-10]** [Pliny the Liberator が Claude Fable 5 をリリース 24 時間以内でジェイルブレーク — Unicode・ホモグリフ・キリル文字代替 + 長コンテキスト追跡 + ナラティブフレーミングの多重攻撃で安全分類器を回避、スタックバッファオーバーフロー exploit コードと化学合成プロトコルを生成; Fable 5 の 12 万文字システムプロンプトが GitHub に流出](https://cyberpress.org/claude-fable-5-jailbreak/) — Fable 5 は高リスククエリを Opus 4.8 にフォールバックさせる専用分類器を搭載するが、Pliny は「分類器は悪意ある攻撃者より正規の研究者を多くブロックしている」と批判 *(Cyberpress / CyberSecurityNews / CoinTelegraph)*

- **[2026-06-10]** [Anthropic が Claude Managed Agents をパブリックベータでリリース — cron スケジュール・資格情報ボールト保存・自律 CLI ツールアクセスを備えた企業向け常駐エージェント基盤が正式公開](https://www.techtimes.com/articles/318163/20260610/claude-managed-agents-add-cron-schedules-credential-vaultsanthropic-beta-puts-agents-autopilot.htm) — 人間が不在の状態での自律実行を正式化; エージェントが MCP ツール・ブラウザ・本番サービスと永続接続する構成は攻撃面拡大の観点でも注目 *(TechTimes / Anthropic)*

- **[2026-06-10]** [AI ローコードプラットフォーム Langflow の CVE-2026-5027 (CVSS 8.8) が非認証 RCE として野外悪用開始 — 約 7,000 の公開インスタンスが対象; デフォルトの auto-login 設定でパスファイル書き込み→RCE が認証不要で成立](https://thehackernews.com/2026/06/unpatched-langflow-flaw-cve-2026-5027.html) — Langflow は LLM エージェント・RAG パイプラインを GUI で構築するプラットフォームとして利用が急拡大。修正は v1.9.0 だが多数の未更新インスタンスが残存 *(The Hacker News / BleepingComputer)*

- **[2026-06-10]** [GitHub が npm v12 でサプライチェーン攻撃対策の大規模仕様変更を予告 — preinstall/install/postinstall スクリプトのデフォルト自動実行を禁止し明示的承認を必須化; IronWorm・Hades キャンペーンが npm install フック悪用型攻撃を繰り返した直接の対応措置](https://www.bleepingcomputer.com/news/security/github-announces-npm-security-changes-to-tackle-supply-chain-attacks/) — npm 11.16.0 で事前準備用 warning を有効化済み; 既存パイプラインへの互換性影響を事前確認するよう呼びかけ *(BleepingComputer)*

- **[2026-06-11]** [OpenAI が Oracle Cloud Infrastructure (OCI) との統合を発表 — 既存の Oracle Universal Credits (UCM) で GPT-5.5・Codex 等のフロンティアモデルに新規ベンダー契約なしにアクセス可能に; 政府・金融業界の Oracle 大口顧客も即日利用可](https://openai.com/news/) — フロンティア AI モデルへの企業アクセス経路が既存エンタープライズクラウド契約の延長として統合される流れが加速 *(OpenAI / Oracle)*

- **[2026-06-10]** [Google Gemini が世界的大規模障害 — 太平洋時間 06:11 から Downdetector で報告急増、error 1076/1099 でプロンプト処理が不能に; MAU 9 億人超の直後の障害で AI サービス単一障害点リスクが再浮上](https://www.techradar.com/news/live/gemini-down-june-2026) — 根本原因は未公表; AI インフラの可用性透明性に対する批判が改めて高まる *(TechRadar)*

---

## セキュリティ関連ニュース

- **[2026-06-11]** [ShinyHunters が Oracle PeopleSoft CVE-2026-35273 (CVSS 9.8) をゼロデイ悪用し 100 組織超・50 万件の学生・従業員・医療・移民記録を窃取 — University of Nottingham が 6/11 に侵害を公式確認; Oracle が帯外 (OOB) 緊急パッチを即日公開](https://www.theregister.com/cyber-crime/2026/06/11/shinyhunters-claims-oracle-peoplesoft-0-day-hit-100-orgs/5254443) — 旧来 CVE とゼロデイを組み合わせた「ガジェットチェーン」手法; 主要標的は教育機関で 300 件の脆弱インスタンスが確認 *(The Register / Help Net Security / SecurityWeek / BleepingComputer)*

- **[2026-06-10/11]** [Ivanti Sentry CVE-2026-10520 (CVSS 10.0) が watchTowr PoC 公開から 24 時間以内に野外悪用段階に移行 — Shadowserver が 2 インスタンスの実際のバックドア設置を確認; MDM ゲートウェイ一台の侵害が企業全体の Exchange・ActiveSync 認証情報に root アクセスを可能にする](https://www.bleepingcomputer.com/news/security/max-severity-ivanti-sentry-vulnerability-now-exploited-in-attacks/) — CVE-2026-10523 (CVSS 9.9, 認証バイパス→管理者アカウント作成) と組み合わせると完全乗っ取りが成立。即時 R10.5.2/R10.6.2/R10.7.1 へのアップデートが急務 *(BleepingComputer / TechTimes / watchTowr Labs)*

- **[2026-06-11]** [Europol・DOJ/FBI が暗号資産マネーロンダリングサービス AudiA6 を閉鎖 — ランサムウェアグループが €3.36 億 ($3.89 億) を 5% 手数料で洗浄した決済インフラを摘発; 15 件以上の国際サイバー犯罪捜査との連鎖が判明; ウクライナ・ロシア国籍の 2 名をジョージア共和国バトゥミで逮捕](https://www.europol.europa.eu/media-press/newsroom/news/ransomware-gangs-cut-eur-336-million-audia6-crypto-laundering-pipeline) — FBI との合同捜査で 2022 年 12 月〜2026 年 5 月の 6 回のアンダーカバー取引を実施。ランサムウェアグループの資金インフラへの直接打撃 *(Europol / CryptoTimes / Philadelphia Inquirer)*

- **[2026-06-10]** [ServiceNow が未認証 API アクセスによる顧客データ漏洩インシデントを 4 日遅れで公開 — Scripted REST Resource の `requires_authentication=false` 設定不備で IT チケット・従業員記録・セキュリティ案件レポートが外部参照可能に; 6/5 にサーバー側でパッチ済み](https://techcrunch.com/2026/06/10/servicenow-tells-customers-a-bug-left-some-of-their-data-exposed-to-the-internet/) — 4/22 バグバウンティ報告から 6/5 パッチまで 44 日間の修正遅延; 6/5 パッチから 6/9 公告まで 4 日の通知遅延。グレード非公開とともに企業顧客から批判を受ける *(TechCrunch / BleepingComputer)*

- **[2026-06-10]** [watchTowr が Ivanti Sentry CVE-2026-10520 の完全技術解析 + PoC を公開 — `$()` シェル展開パターンによる OS コマンドインジェクションシンク・前提条件・完全攻撃チェーンを詳細解説; Ivanti の脆弱性カテゴリ分類の曖昧さも批判](https://labs.watchtowr.com/more-evidence-that-words-dont-mean-what-we-thought-they-meant-ivanti-sentry-pre-auth-os-command-injection-cve-2026-10520/) — タイトル「言葉は思っていた意味ではない」は Ivanti の分類用語に対するアイロニー; 他 MDM ベンダーの類似エンドポイントへのバリアントハントを強く推奨 *(watchTowr Labs)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-10 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-10520 | Ivanti Sentry ≤10.7.0 / 10.6.1 / 10.5.1 (MDM モバイルゲートウェイ) | CWE-78 / **10.0** | 非認証リモート攻撃者が HTTPS エンドポイントに `$()` シェル展開を含む細工リクエストを送信 → OS コマンドインジェクションシンクが root 権限コマンドを実行 → MDM ゲートウェイ完全制御 | [R10.5.2 / R10.6.2 / R10.7.1 (2026-06-09)](https://hub.ivanti.com/s/article/Security-Advisory-Ivanti-Sentry-CVE-2026-10520-CVE-2026-10523) | **野外悪用中 (Shadowserver 2026-06-11 確認)** / CVSS 10.0 / PoC から 24h 以内にバックドア / 他 MDM・EMM 製品 (MobileIron / JAMF 等) の同 API エンドポイントへのバリアントハント推奨 |
| CVE-2026-10523 | Ivanti Sentry ≤10.7.0 / 10.6.1 / 10.5.1 (同上) | CWE-306 / **9.9** | 非認証リモート攻撃者が認証チェックを欠落したエンドポイントに任意リクエストを送信 → 管理者アカウントを任意作成 → CVE-2026-10520 との連鎖でより確実な完全侵害が成立 | [R10.5.2 / R10.6.2 / R10.7.1 (2026-06-09)](https://hub.ivanti.com/s/article/Security-Advisory-Ivanti-Sentry-CVE-2026-10520-CVE-2026-10523) | **野外悪用中** / CVSS 9.9 / CVE-2026-10520 とペア公開 / 認証バイパス + RCE の組み合わせは Ivanti の過去 CVE パターンと一致 — EPMM 等への水平バリアント要確認 |
| CVE-2026-35273 | Oracle PeopleSoft Enterprise PeopleTools 8.61 / 8.62 | CWE-94 / **9.8** | 非認証リモート攻撃者が既知 CVE と本ゼロデイを「ガジェットチェーン」として連鎖させた HTTP リクエストを送信 → PeopleTools コード評価機能経由で任意コード実行 → データベース・ファイルシステム完全アクセス | [Oracle OOB Security Alert (2026-06-11)](https://www.oracle.com/security-alerts/alert-cve-2026-35273.html) (commit 不明) | **野外悪用中 (ShinyHunters, 100+ 組織侵害)** / CVSS 9.8 / 教育機関・政府機関が主標的 / 旧 CVE との chaining パターンが他 Java EE アプリサーバーに水平展開する可能性あり |
| CVE-2026-5027 | Langflow (AI エージェント/ローコードプラットフォーム) ≤1.8.4 | CWE-22 / **8.8** | 非認証攻撃者 (auto-login デフォルト有効) が `POST /api/v2/files` の `filename` パラメーターに `../../` を挿入した multipart リクエストを送信 → サーバー任意パスにファイルを書き込み → Web シェル設置 / 設定改ざんで RCE | [Langflow v1.9.0 (2026-04-15)](https://github.com/logspace-ai/langflow/releases) (commit 要確認) | **野外悪用中 (2026-06-10)** / 約 7,000 インスタンスが公開露出 / AI エージェント構築環境への直接攻撃ルート / CrewAI・n8n・Flowise 等類似 AI ローコードプラットフォームへのバリアントハント推奨 |
| CVE-2026-11645 | Google Chrome <149.0.7827.102 (V8 JavaScript エンジン) | CWE-125+787 / **8.8** | 悪意ある HTML ページが V8 の境界外読み書きを誘発 → サンドボックス内での任意コード実行 → ブラウザプロセスを通じたシステムアクセス | [Chrome 149.0.7827.102 (2026-06-08)](https://chromereleases.googleblog.com/2026/06/) | **野外悪用中 / CISA KEV 2026-06-09 追加 (修正期限 6/23)** / 2026 年 5 件目の Chrome ゼロデイ / Chromium 系全ブラウザ (Edge・Brave・Opera) へのバリアント確認推奨 *(初報 June 9 = 採用窓前日; 前号未掲載のため参考掲載)* |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-06-11 | CVE-2026-35273 (Oracle OOB) | Oracle PeopleSoft の緊急帯外パッチ公開 — 国内大学・公的機関で PeopleSoft を運用する組織は ShinyHunters の悪用キャンペーンへの即時対応が必要 | CVSS 9.8 / 非認証 RCE | [Oracle Security Alert](https://www.oracle.com/security-alerts/alert-cve-2026-35273.html) |
| 2026-06-10 | CVE-2026-10520/10523 (Ivanti Advisory) | Ivanti Sentry の CVSS 10.0 + CVSS 9.9 の 2 脆弱性が野外悪用段階に移行 — Ivanti Sentry を MDM ゲートウェイとして運用する国内企業・官公庁は即時 R10.5.2 以上へのアップグレードが急務 | CVSS 10.0 + 9.9 / 非認証 RCE・管理者権限取得 | [Ivanti Security Advisory](https://hub.ivanti.com/s/article/Security-Advisory-Ivanti-Sentry-CVE-2026-10520-CVE-2026-10523) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 35 ソース (The Hacker News, BleepingComputer, SecurityWeek, Help Net Security, The Register, TechCrunch, TechTimes, watchTowr Labs, Europol, CryptoTimes, SC Media, Rapid7, SOCRadar, TechRadar, Cyberpress, CyberSecurityNews, CoinTelegraph, GBHackers, Cyberinsider, IT-Connect, SCWorld, Technadu, NeuraCybintel, Google Cloud TI, Oracle Security Blog, Ivanti Hub, GitHub Changelog, Anthropic, OpenAI, itbrief.news, Android Gadget Hacks, pasqualepillitteri.it, socprime.com, penligent.ai 他)
- 採用件数: AI=6 / Security=5 / CVE=5 / 国内=2
- 除外理由内訳:
  - 古すぎ (< 2026-06-10 JST):
    - CVE-2026-11645 Chrome V8 ゼロデイ (初報 June 8-9 — 参考掲載として CVE テーブルに注記付きで収録)
    - CVE-2026-7473 Arista EOS no-patch (CISA KEV June 9, SecurityWeek "2 days ago" ≒ June 9-10 境界)
    - OpenClaw AI phishing (BleepingComputer June 9)
    - KnowledgeDeliver LMS CVE-2026-5426 (THN May 2026)
    - Tokyo FM breach (January 2026)
    - Android June 2026 CVE-2025-48595 (CISA KEV June 2, 前号収録)
    - Demis Hassabis AGI 2029 コメント (Google I/O May 26 発言)
  - 重複 (excluded_set 直近7日):
    - Microsoft June Patch Tuesday 詳細・ゼロデイ 6 件 (2026-06-09, 06-10, 06-11 digest)
    - Nightmare Eclipse / RoguePlanet Microsoft Defender LPE PoC (2026-06-11 digest)
    - Miasma ワームフレームワーク GitHub 公開 (2026-06-07/08 digest の延長)
    - Colorado AI Act / EU AI Act 施行期限 (2026-06-11 digest)
    - OpenAI / Anthropic 国際 AI 監視機構 (2026-06-11 digest)
    - Claude Fable 5 / Mythos 5 初報 (2026-06-10 digest)
    - Adobe Acrobat APSB26-63 (2026-06-11 digest)
    - SAP June Patch Day CVE-2026-44748/27671/22732 (2026-06-10 digest)
    - Veeam CVE-2026-44963 (2026-06-10 digest)
    - Linux nf_tables CVE-2026-23111 PoC (2026-06-10 digest)
    - Hades PyPI キャンペーン続報 (2026-06-11 digest)
  - 日付不明/確認不可:
    - ppln.co Japan 週次ダイジェスト 2nd Week of June 2026 の個別項目 (403)
    - JPCERT/CC の June 10-12 個別アラート URL (403)
- 取得失敗ソース (HTTP 403): helpnetsecurity.com 個別記事 / thehackernews.com 個別記事 / bleepingcomputer.com 個別記事 / labs.watchtowr.com 個別記事 / piyolog.hatenadiary.jp / jpcert.or.jp / jvn.jp / buildfastwithai.com 個別ページ — WebSearch スニペット・複数独立媒体の記事で内容・日付を補完
- 備考: CVE-2026-11645 (Chrome V8) は初報が June 9 で採用窓 (June 10-12) の 1 日前だが、前号未掲載かつ CISA KEV 修正期限 (6/23) が来週であるため参考掲載とした。CVE-2026-10520/10523 (Ivanti Sentry) はアドバイザリが June 9 だが野外悪用確認ニュースが June 11 であるため正規採用。

</details>
