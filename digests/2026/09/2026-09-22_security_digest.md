# KEDA Daily Digest — 2026-09-22 (JST)

> 採用範囲: 公開日 2026-09-20 〜 2026-09-22
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

BragJack 攻撃（Forever Security / Gal Weizman、Sep 20-21 開示）が Chrome・Edge・Opera Neon・Perplexity Comet・Claude for Chrome の 5 ブラウザ AI アシスタントに対するゼロクリックのブラウザ拡張機能乗っ取りを実証し、AI ブラウザ統合の信頼境界が新たな攻撃面として確立した。米財務長官 Bessent が米中二国間 AI インシデント通報メカニズムを提案（Sep 20）し、AI 安全保障を巡る初の正式な米中対話枠組みが浮上した一方、Reuters が Anthropic の GPT-6 Astra 対抗モデル前倒し検討を報道（Sep 19-20）し開発スローダウン宣言との矛盾が業界内で話題となった。CVE 面では Apache MINA ≤ 2.0.30 / 2.1.14 に CVE-2026-47065 修正の不完全なバックポートに起因する CVSS 9.8 Java デシリアライズ RCE（Sep 21）、MISP に認証済み SSRF・ファイルアクセス（CVSS 8.3）、Telegram Desktop に HTML エクスポート XSS（CVSS 8.3）が開示され、週末にもかかわらず OSS セキュリティ基盤への攻撃面拡大が続いた。

## AI 関連ニュース

- **[2026-09-20/21]** [BragJack Attack: ブラウザ拡張機能が Gemini Live・Copilot・Claude for Chrome 等 5 製品の AI アシスタントをゼロクリックで乗っ取り — 悪意ある拡張が信頼コマンドチャンネルになりすまし AI に任意指示を注入、ユーザー操作なしにファイル読み取り・外部送信・画面キャプチャを実行](https://www.darkreading.com/application-security/bragjack-browser-extensions-hijack-ai-assistants/) — Forever Security の Gal Weizman が開示；拡張権限モデルの設計上の欠陥が AI ブラウザ統合のゼロクリック攻撃を可能にする構造的問題；5 ベンダーがパッチ適用（バグバウンティ $600〜$7,000） *(DarkReading / GBHackers / BleepingComputer)*
- **[2026-09-20]** [米財務長官 Bessent が米中 AI 安全インシデント通報メカニズムを提案 — 国家安全保障に影響する AI 事故の二国間通知制度、Trump–Xi 会談の議題入りを目指す](https://www.washingtontimes.com/news/2026/sep/20/us-china-ai-safety-notification-mechanism/) — 初の正式な米中 AI セキュリティ「レッドライン」対話枠組み；具体的な合意には至っておらず今後の外交交渉で詳細を詰める予定 *(Washington Times / ABC News / NBC News)*
- **[2026-09-19/20]** [Anthropic が GPT-6 Astra に対抗する新モデルの前倒しリリースを検討 — Reuters 独占；Astra が企業 AI 支出の 13% を獲得しクロード・フェーブル 8% を上回る](https://www.reuters.com/technology/anthropic-weighs-accelerating-new-model-release-gpt6-astra-competition-2026-09-19/) — GPT-6 Astra は 9/3 リリースから 3 週間でシェア急拡大；Amodei の「開発スローダウン」公開書簡（Sep 1）と相反する動きとして注目 *(Reuters / Bloomberg)*

## セキュリティ関連ニュース

- **[2026-09-20/21]** [BragJack 技術詳細: ブラウザ AI のコマンドチャンネル偽装によるゼロクリック乗っ取り — Chrome・Edge・Opera Neon・Perplexity Comet・Claude for Chrome が影響、CWE-346 (Origin Validation Error) が根本原因](https://gbhackers.com/bragjack-browser-extension-ai-hijack-technical-analysis/) — 拡張が AI コマンドチャンネルを偽装してローカルファイル読み取り・スクリーンショット・カメラ/マイクアクセスを AI 経由で実行可能；AI ブラウザ統合のアーキテクチャ上の欠陥として研究者が警鐘 *(GBHackers / BleepingComputer / SecurityWeek)*
- **[2026-09-20]** [Qilin ランサムウェアがトルコ大手 Zorlu Holding（エネルギー・防衛）とタイ ShopDunk をリークサイトに掲載 — 二重恐喝モデルで交渉圧力、被害者は未確認](https://www.infosectoday.io/2026/09/20/qilin-ransomware-zorlu-holding-shopdunk/) — Zorlu は防衛省・エネルギー省との契約を抱えるトルコ有数のコングロマリット；機密インフラデータへのアクセス懸念 *(infosectoday.io / Cybernews)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 today-2 (2026-09-20) 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-94301 / GHSA-h355-27x9-rr7r | Apache MINA < 2.0.31 / < 2.1.15 | CWE-502 / CVSS 9.8 | 未認証攻撃者が Java シリアライズエンドポイントに細工オブジェクトを送信 → CVE-2026-47065 修正の不完全バックポートにより `resolveProxyClass()` が `ObjectInputStream.readProxyDesc()` 経由で JDK デフォルトを呼び出し `Class.forName()` が各インタフェースに実行 → 受け入れクラスリストを完全バイパスして任意クラスのデシリアライズ → RCE | [MINA 2.0.31 / 2.1.15 (GHSA-h355-27x9-rr7r)](https://github.com/advisories/GHSA-h355-27x9-rr7r) | **CVSS 9.8** / Java デシリアライズ許可リストの不完全バックポートパターン / Netty・Apache NIO 等の他 Java NIO フレームワークでの `resolveProxyClass` 実装への水平バリアント候補 |
| CVE-2026-94488 / GHSA-58p4-4g24-j8vp | Telegram Desktop < 7.0.1 | CWE-79 / CVSS 8.3 | 攻撃者がグループチャットで悪意あるメッセージを転送 → HTML エクスポート機能の `button.text.toUtf8()` がユーザー入力をサニタイズせず HTML 出力へ直接書き込み → XSS → エクスポートファイルを開いたユーザー環境でスクリプト実行・情報窃取 | [commits 52c779bf / 8457d13a (GHSA-58p4-4g24-j8vp)](https://github.com/advisories/GHSA-58p4-4g24-j8vp) | CVSS 8.3 / グループチャットから HTML エクスポート経由のゼロクリック XSS / Signal・Element 等他メッセージアプリの HTML エクスポート実装への水平バリアント候補 |
| CVE-2026-94401 / GHSA-2jvm-986q-589g | MISP < 2.5.47 | CWE-73 / CVSS 8.3 | 変更権限を持つ認証済みユーザーが XML インポート機能にローカルパスまたは URL を含む任意コンテンツをアップロード → コンテンツ種別検証なしに処理 → 内部ファイルへの不正アクセスまたは内部サービスへの SSRF → IOC データベース・SIEM・SOAR 連携サービスへの横移動 | [MISP 2.5.47 commit d5f247b91 (GHSA-2jvm-986q-589g)](https://github.com/advisories/GHSA-2jvm-986q-589g) | CVSS 8.3 / 脅威インテリジェンスプラットフォームの SSRF / OpenCTI・TheHive 等他 OSINT プラットフォームの XML/JSON インポート実装への水平バリアント候補 |
| CVE-2026-75939 / GHSA-vhqx-cfmx-mjq9 | openshift/oc-mirror (全影響バージョン) | CWE-347 / CVSS 7.4 | 中間者攻撃者が PGP 署名されたリリースペイロードを傍受 → 署名検証がエラーステータスを完全な署名済みボディ処理前に評価する欠陥 → 有効な Red Hat キー ID を持つ偽造 PGP を注入 → エアギャップ環境の切り離されたレジストリに悪意ある OCI イメージを配布 | [修正コミット不明 (GHSA-vhqx-cfmx-mjq9)](https://github.com/advisories/GHSA-vhqx-cfmx-mjq9) | CVSS 7.4 / OpenShift エアギャップ環境サプライチェーン汚染 / skopeo・crane・oras 等他 OCI レジストリミラーリングツールの PGP 署名検証実装への水平バリアント候補 |

## 国内脆弱性・インシデント情報

> 直近2日間に該当する新規ニュースは確認できませんでした。（JVN / JPCERT / IPA への直接アクセス不可; 検索結果では 2026-09-20〜22 の新規 JVN アドバイザリは確認できず。Sep 19 以前のアドバイザリは前日 digest 既報のため除外）

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 20+
- 採用件数: AI=3 / Security=2 / CVE=4 / 国内=0
- AI ニュース件数が少ない理由: 2026-09-20〜22 は週末にあたり主要 AI 発表が少ない; BragJack (Sep 20-21) と Bessent 米中提案 (Sep 20) が新規主要案件
- 除外理由内訳:
  - 採用窓外または重複（直近7日 digest 既報）: Anthropic/Accenture Faculty 評価者（Sep 21 digest）、ToolHive CVE-2026-58197（Sep 21 digest）、Orkes Conductor CVE-2026-58138（Sep 21 digest）、Plugin4Shell GitHub Copilot 声明（Sep 21 digest）、TanStack npm サプライチェーン侵害（Sep 21 digest）、WordPress Click2Shell（Sep 21 digest）、SolarWinds CVE-2026-28326（Sep 21 digest）、CISA KEV 2件（Sep 21 digest）、Mongoid CVE-2026-93762/93759（Sep 21 digest）、mnemosyne-memory CVE-2026-59163（Sep 21 digest）、kcp CVE-2026-61682（Sep 20 digest）、Gravity Forms CVE-2026-84434（Sep 20 digest）、Linux KEV 3件（Sep 20 digest）、Plugin4Shell 初報（Sep 20 digest）、Google Gemini CTF 侵入（Sep 20 digest）、Gyazo 侵害（Sep 20 digest）、Cisco ASA/FMC CVE群（Sep 20 digest）、Azure AI Foundry CVE-2026-85889（Sep 19 digest）、vm2 CVE-2026-93603（Sep 19 digest）、MLflow GHSA-gqvg-gmmx-x4hm（Sep 19 digest）、Sentry Seer CVE-2026-90999（Sep 19 digest）、Hacktron Opus 5 bug bounty（Sep 19 digest）
  - 採用窓外（公開日 < 2026-09-20）: JadePuffer マルウェア（Jul 2026）、AnMed Healthcare 侵害（Jul 2026）、Shai-Hulud GNSS 攻撃（Sep 14-16）、N-central CVE-2026-86218（Sep 6-8）、F5 BIG-IP rootkit（Sep 9）、Google ADK Kotlin 1.0（Sep 9）
- 取得失敗ソース（EGRESS_BLOCKED）: thehackernews.com, bleepingcomputer.com, securityweek.com, nvd.nist.gov, jvn.jp, jpcert.or.jp, osv.dev, helpnetsecurity.com, gbhackers.com (WebFetch のみ・検索スニペット利用可), darkreading.com (一部)

</details>
