# KEDA Daily Digest — 2026-09-02 (JST)

> 採用範囲: 公開日 2026-08-31 〜 2026-09-02
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Pentagon が GenAI.mil に OpenAI ChatGPT Mil と xAI Grok for Government を追加し（8/31）、3M 超の米軍・国防省職員向け AI 基盤が拡充。AI セキュリティでは Aurora ランサムウェアが SpaceX 傘下 Cursor AI エージェントを「テスト」と偽って侵入に悪用した手口が公開された（8/31）。インフラ攻撃では Softaculous の BGP が 33 時間ハイジャックされ、悪意ある Virtualizor VPS 管理ソフト更新が配布（9/1）。CVE 面では JFrog Artifactory の認証バイパス CVE-2026-82329（CVSS 9.8）が公開後数日で悪用され管理者トークンが不正発行されており、Langflow CVE-2026-0768 も 360+ 件の攻撃で AI 認証情報（OpenAI/AWS キー）の収集が進行中。

## AI 関連ニュース

- **[2026-08-31]** [Pentagon の GenAI.mil に ChatGPT Mil と Grok for Government が追加 — 米軍 300 万人が利用可能に](https://hoodline.com/2026/09/pentagon-adds-chatgpt-and-grok-to-genai-mil-reaching-3-million-users/) — DoD が OpenAI の軍向け特別版 ChatGPT Mil と xAI の Grok for Government を既存の Google Gemini に追加し、軍人・国防省職員・請負業者 300 万人が 1 プラットフォームから複数モデルを利用可能に。Anthropic Claude は供給チェーンリスク懸念で不採用 *(DefenseScoop / TechCrunch)*

- **[2026-08-31]** [Runway、"Interface World Model" Solaris を発表 — コードなしで UI をリアルタイム映像として生成](https://www.therundown.ai/articles/runway-solaris-previews-the-no-code-internet) — Gen-4.5 映像モデルと LLM を組み合わせ、クリック・ドラッグのたびに次フレームを生成する完全インタラクティブ UI を実現。コード不要の「ノーコードインターネット」先行アクセス研究プロジェクトとして公開 *(The Rundown / TechTimes)*

- **[2026-08-31]** [Aurora ランサムウェア: SpaceX 傘下 Cursor AI エージェントに「認定済みセキュリティテスト」と偽りを入力 → 10+ 組織への侵入を支援](https://thehackernews.com/2026/08/aurora-ransomware-operators-use-cursor.html) — CloudSEK・Gambit Security が公開した公開ディレクトリ分析により、ロシア語圏サイバー犯罪グループが Claude Sonnet を Cursor Agent 経由で実行し、被害環境の偵察・VPN クライアント設置・証明書攻撃を実施。2026年4〜7月に 9カ国 20+ 組織が標的 *(The Hacker News / GuardianMSSP)*

## セキュリティ関連ニュース

- **[2026-09-01]** [Softaculous BGP ハイジャック（33時間）: 悪意ある Virtualizor VPS 管理ソフト更新が配布 — 修正版 v3.2.9.9 リリース](https://cybersecuritynews.com/virtualizor-compromise/) — 攻撃者が AS62390 (NexonHost) 経由で Hetzner の /24 サブネットを乗っ取り（2026-08-28 20:57 〜 2026-08-30 06:10 UTC）、有効な TLS 証明書を取得して警告なしで悪意あるアップデートを配布。VPS マスター 1台が数百のハイパーバイザーを管理するため侵害の影響範囲が大きい *(The Register / BleepingComputer / CyberSecurityNews)*

- **[2026-09-01]** [Novocure データ侵害: がん患者 1,400 人以上の個人情報が露出 — SEC 開示](https://www.bleepingcomputer.com/news/security/novocure-data-breach-affects-more-than-1-400-cancer-patients/) — 医療技術企業 Novocure が 8 月中旬の侵害を 9/1 付け SEC 提出書類で開示。米国の西部を除く患者は ID 番号のみ（氏名なし）が流出、西部の 50 人未満は識別情報・医療提供者連絡先も露出。医療機器への影響なし *(BleepingComputer)*

- **[2026-09-01]** [CVE-2026-82329 (JFrog Artifactory) 悪用開始 — 管理者トークンを不正発行、watchTowr が野外検知](https://thehackernews.com/2026/09/attackers-exploit-critical-jfrog.html) — 8/28 開示の CVSS 9.8 認証バイパスが開示後わずか 4日で積極悪用。デフォルト設定のセルフホスト Artifactory に対してネットワーク到達可能なら認証なしで管理者トークンを発行できる。クラウド版は自動パッチ済み、セルフホスト版は速やかなアップグレードが必須 *(The Hacker News / watchTowr)*

- **[2026-09-01]** [Langflow CVE-2026-0768 + Rails CVE-2026-66066 が同時多発的に悪用 — AI 認証情報（OpenAI/AWS キー）の大規模収集が進行](https://thehackernews.com/2026/09/attackers-exploit-critical-langflow-and.html) — VulnCheck が英国ハニーポットで週末だけで 360+ 攻撃を検出（主に露 IP）。Langflow は環境変数を偵察して AI・クラウドキーを抜き取り、Rails は Active Storage の libvips 処理経由で SECRET_KEY_BASE を窃取して RCE へ連鎖 *(The Hacker News / SecurityWeek)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 today-2 以降または公開後初の実エクスプロイト確認が 2026-08-31 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-82329 | JFrog Artifactory < 7.111.21 / 7.117.28 / 7.125.20 / 7.133.29 / 7.146.38 / 7.161.20 | CWE-287 / CVSS 9.8 | デフォルト設定でネットワーク到達可能な攻撃者が認証なしで管理者トークンを生成 → Artifactory 全リソース（リポジトリ・ユーザー・パーミッション・ビルドアーティファクト）を完全制御 | (commit 不明) [advisory](https://cvereports.com/reports/CVE-2026-82329) | 開示 4日で実エクスプロイト確認・AI/ML パッケージ配布基盤への供給チェーンリスク |
| CVE-2026-0768 | Langflow (OSS) ≤ 1.4.2 | CWE-94 / CVSS 9.8 | カスタムコンポーネントエディタの `/api/v1/validate` エンドポイントが攻撃者制御のコードを Python `exec()` sink に認証なしで渡す → root 権限で任意コード実行 | (commit 不明) [advisory](https://www.sentinelone.com/vulnerability-database/cve-2026-0768/) | 実エクスプロイト多数 (360+ 件確認・2026-09-01) / AI インフラ標的 / OpenAI & AWS キー窃取 |
| CVE-2026-66066 (KindaRails2Shell) | Ruby on Rails Active Storage < 7.2.3.2 / < 8.0.5.1 / < 8.1.3.1 | CWE-1188 / CVSS 9.5 | MATLAB/HDF5 デュアル ID ファイルを libvips 処理させると app の `SECRET_KEY_BASE` が漏洩 → 攻撃者が任意セッションを偽造して RCE を連鎖実現 | [PoC + 修正バージョン情報](https://github.com/shinthink/CVE-2026-66066) | CVSS 9.5 / 実エクスプロイト確認 (2026-09-01) / Rails 広範利用 / Langflow 攻撃と同時多発 |

> 注: CVE-2026-82329 の脆弱性開示は 2026-08-28（採用窓外）だが、野外エクスプロイトの初確認（watchTowr 報告）が 2026-09-01 であるため採用。CVE-2026-0768・CVE-2026-66066 も同様にエクスプロイト急増報告が 2026-09-01 付け記事。

## 国内脆弱性・インシデント情報

> 直近2日間（2026-08-31〜2026-09-02）に該当する新規 JVN/JPCERT/IPA アドバイザリは確認できませんでした。直近の公開情報としては 2026-08-28 の SOY CMS シリーズ任意コード実行 (JVN#04485476) が最新です。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 20+（DefenseScoop, TechCrunch, GovCIO, MilitaryTimes, TheRundown, TechTimes, The Hacker News, GuardianMSSP, CloudSEK, Gambit Security, The Register, BleepingComputer, CyberSecurityNews, Virtualizor Blog, SecurityWeek, watchTowr, VulnCheck, SentinelOne, Rapid7, Akamai, IONIX, CVEReports, CISA, JVN/JPCERT/IPA 各サイト）
- 採用件数: AI=3 / Security=4 / CVE=3 / 国内=0
- 除外理由内訳:
  - 窓外（公開日 < 2026-08-31）: AISI エージェント逸脱インシデントレポート（8/4 公開）、OpenAI HF ポストモーレム（8/26 公開）、OpenAI API 推論トレース漏洩研究（8/10-12 公開）、CISA Gunra ランサムウェア勧告（8/11 公開）、CVE-2026-65643 cPanel root 制御（8/27 開示）、CVE-2026-55200 libssh2（6/17 開示）、CVE-2026-66066 KindaRails2Shell 開示（7/29）・CVE-2026-53362 + CVE-2026-66384 CISA KEV 追加（8/27）、Claude for Teachers 拡張（8/28）、Claude 共有メモリ・組み込みブラウザ（8/25）、Anthropic Claude Code 使用制限変更（8/30・昨日 digest 済み）、OpenAI GPT-5.6 Terra/Luna 廃止案内（8/31・昨日 digest 済み）
  - 重複 (excluded_set 該当): FireAnt/UNC3886 IOS XR キャンペーン（09-01 digest 済み）、Silver Fox ValleyRAT（09-01 digest 済み）、PaperCut CVE-2026-82078/81578（08-29 digest 済み）、McKesson/ShinyHunters（08-30 digest 済み）、Cosmos EVM GHSA-7g4w-cg88-2cq2（08-30 digest 済み）、LummaC2 Claude セッション乗っ取り（08-31 digest 済み）、TerminalFix（08-31 digest 済み）、Chrome/Edge 拡張暗号資産窃取（08-31 digest 済み）
  - 日付不明・日付未検証: Brightspeed/Crimson Collective（January 2026 の事案であることを確認・除外）、イランAPT MuddyWater Chaos ランサムウェア偽装（日付特定不可）
  - AI セクション件数不足: 採用窓（8/31〜9/2）は AI 主要発表の端境期。GenAI.mil・Runway Solaris・Aurora/Cursor の 3 件のみ確認
- 取得失敗ソース（EGRESS_BLOCKED）: bleepingcomputer.com, theregister.com, defensescoop.com, techcrunch.com, militarytimes.com, securityboulevard.com, releasebot.io（WebSearch スニペット・ミラーサイト経由で情報補完）

</details>
