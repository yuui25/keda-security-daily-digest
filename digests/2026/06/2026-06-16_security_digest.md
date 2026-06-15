# KEDA Daily Digest — 2026-06-16 (JST)

> 採用範囲: 公開日 2026-06-14 〜 2026-06-16
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Patch Tuesday (6/9) から1週間が経ち、新規公開が落ち着いた端境期にあっても、ShinyHunters による欧州評議会 (Council of Europe) への Oracle PeopleSoft ゼロデイ悪用侵害 (297 GB・職員 1 万人超の給与明細・銀行口座等) が 6/14 に公表され、CVE-2026-35273 の被害がロシア／中国外交を監視する国際機関まで波及した。AI セキュリティ面では「推論ループ延長型 DoS」が初公開 — 単一の毒入りドキュメントが LangGraph の安全ガードレールを 148 倍の処理時間に引き込み、共有エージェントインフラを麻痺させる可能性を示した。Awesome Motive CDN API キーの流出による 1.2M WordPress サイトへのバックドア供給チェーン攻撃 (6/12-14 発生・6/14 公開) も同日明らかになり、人気 WordPress プラグインエコシステムのインフラ信頼性に疑問符がついた。

## AI 関連ニュース

- **[2026-06-15]** [AI エージェントのガードレール自体が DoS の標的に — 単一の毒入りドキュメントが推論型安全検査を無限ループに引き込む「推論ループ延長型 DoS」を香港科技大チームが公開](https://www.csoonline.com/article/4185051/attackers-can-turn-ai-agent-guardrails-into-denial-of-service-weapons.html) — 4 エージェントフレームワークで検証; LangGraph: 148 倍・BrowserGym: 131 倍・OpenHands: 36 倍・OSWorld: 18 倍の処理時間増加を確認。既存の完全性攻撃 (プロンプトインジェクション・ジェイルブレーク) と異なり「可用性」を狙った新クラスの脅威; ガードレールインフラをエージェントコンピュートから分離することを推奨 *(CSO Online)*

- **[2026-06-14]** [AI エージェントのセキュリティが「岐路」に — プロンプトインジェクションは永続的欠陥でパッチ不可能の可能性と専門家が警告](https://www.techtimes.com/articles/318361/20260614/ai-agent-security-hits-its-reckoning-prompt-injection-may-permanent-flaw-not-patchable-bug.htm) — NIST の Apostol Vassilev が IEEE Security & Privacy に発表した数学的証明 (Gödel 不完全性定理の AI ガードレールへの適用: 有限のルール集合は全ての敵対的プロンプトを網羅できない) を踏まえ、AI エージェント開発者がプロンプトインジェクション対策を「パッチ適用可能な実装バグ」ではなく「永続的な設計制約」として捉え直す必要性を論じる *(TechTimes)*

> 直近2日間 (2026-06-14〜16) の新規 AI 関連ニュースは上記 2 件に留まりました。June Patch Tuesday (6/9) および Anthropic 輸出規制 (6/12) の後処理週間として AI ラボからの大型リリース・政策発表が少ない端境期に当たります。

## セキュリティ関連ニュース

- **[2026-06-14/15]** [ShinyHunters が欧州評議会 (Council of Europe) への Oracle PeopleSoft ゼロデイ経由侵害を公表 — 297 GB の HR・給与データ (職員 1 万人超の 2011〜2026 年分給与明細 40 万件以上・人事ファイル 3,700 件超・履歴書 1.4 万件・銀行口座・社会保障番号・医療記録を含む 42.9 万件) を窃取したと主張; 6/16 を身代金支払期限と予告](https://www.theregister.com/2026/06/15/council-of-europe-hacked-in-shinyhunters-peoplesoft-heist/) — CVE-2026-35273 (PeopleSoft 非認証 RCE, CVSS 9.8) を利用した「100 組織超侵害キャンペーン」の一環; 欧州評議会は調査中 *(The Register / Cybernews / BleepingComputer)*

- **[2026-06-14]** [Awesome Motive CDN API キー漏洩で WordPress プラグイン 3 件 (OptinMonster・TrustPulse・PushEngage) の供給チェーン攻撃が判明 — 1.2M サイト影響](https://www.bleepingcomputer.com/news/security/optinmonster-wordpress-plugin-hacked-in-cdn-supply-chain-attack/) — 6/12 22:17 UTC に api.min.js が改ざんされ、管理者セッションを悪用してダミードメイン tidio.cc に認証情報を送信しつつバックドア管理者アカウント + 自己隠蔽プラグインをサイレントインストール; Awesome Motive は CDN API キーをローテーション済みだが侵害期間中に攻撃者がダウンロードした認証情報への対処が急務 *(BleepingComputer / Patchstack / Sansec / THN)*

- **[2026-06-14/15]** [Socket 研究チームが 152 件の Chrome「ライブ壁紙」拡張機能を IP ロギング・Ad クリック不正計上・Google 自然検索流量の偽装で摘発 — 38 出版社アカウント・3 ブランド (tabplugins.com, yowgames.com, chromewallpaper.com) から単一コードベースで配布、延べ 10.5 万人ユーザーが影響](https://thehackernews.com/2026/06/152-chrome-wallpaper-extensions-with.html) — ユーザーのプライバシーポリシーは「データ収集なし」と記載しつつ実際は IP・ISP・クリック・リファラーを Google AdSense / DoubleClick に送信 *(The Hacker News / CybersecurityNews / Socket)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-14 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| GHSA-ff9g-85jq-r3g3 (CVE 未採番) | Wazuh Manager 5.0.0-beta1〜beta2 (Python, SIEM) | CWE-74 / **10.0** | 登録済みエージェントが FlatBuffer の `DataValue.index` フィールドに CRLF を注入 → OpenSearch `_bulk` NDJSON リクエストに任意操作 (delete/index/update) を挿入 → SIEM アラート改ざん・ログ消去・証拠隠滅; 非認証・ユーザー操作不要 | [Wazuh 5.0.0-beta3](https://github.com/wazuh/wazuh/security/advisories/GHSA-ff9g-85jq-r3g3) | 2026-06-14 公開 / **CVSS 10.0** / SIEM インフラを盲点化する高影響 / 他 SIEM バックエンド (Elastic Security・Splunk ES 等) の同種 _bulk API インジェクション経路へのバリアントハント推奨 |
| CVE-2026-5482 | Responsive FileManager ≤9.14.0 (PHP、WordPress/CMS ファイルマネージャー) | CWE-434 / **9.3** | 非認証攻撃者が `dialog.php` エンドポイントに任意拡張子ファイルをアップロード → 拡張子・MIME 検証完全欠落 → PHP スクリプト配置 → RCE; プロジェクト開発停止 (unmaintained) | **修正パッチなし** (unmaintained) — プラグイン無効化・エンドポイントブロックが唯一の緩和策 | 2026-06-15 NVD 公開 / **CVSS 9.3・パッチ存在しない** / 同種の unrestricted upload sink は ActiveStorage・Shrine 等 Ruby/PHP ファイル処理ライブラリに広く存在 |
| CVE-2026-11860 | Open Source Script Quick.CMS ≤6.8 (PHP、軽量 CMS) | CWE-502 / 高 | 管理者パネルアクセス時に HTTP レスポンスを平文受信 → MITM 攻撃者が PHP シリアライズオブジェクトを注入 → デシリアライズ時に gadget chain 実行 → サーバー上で任意コード実行 | [Quick.CMS 6.8 HTTPS 限定パッチ (2026-05-14)](https://opensourcescripts.com/quick.cms.html) | 2026-06-15 NVD 公開 / PHP デシリアライズ gadget chain / 同パターン (平文 HTTP セッション上のデシリアライズ) は WordPress プラグイン・Magento 1.x 系へのバリアントハント推奨 |

> 直近2日間 (2026-06-14〜16) の CVE 採用件数は 3 件に留まりました。June Patch Tuesday (6/9) の翌週は主要ベンダーからの新規アドバイザリ公開が少ない端境期です。当期間の最重要採用候補は SIEM 監視インフラを完全に盲点化する GHSA-ff9g-85jq-r3g3 (Wazuh CVSS 10.0) です。

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|

> 直近2日間に該当する新規ニュースは確認できませんでした。JVN/JPCERT/IPA への直接アクセスは引き続き HTTP 403 のため WebSearch 経由で確認。欧州評議会侵害 (CVE-2026-35273 経由) は国内外資系教育機関・公的組織が PeopleSoft を運用している場合に影響が及ぶ可能性があるため、JPCERT/CC からの追加アラートに注意が必要。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 30 ソース (BleepingComputer, The Hacker News, The Register, CSO Online, TechTimes, CybersecurityNews, Socket, NVD, GitHub Advisory Database, JVNDB, CISA KEV 等)
- 採用件数: AI=2 / Security=3 / CVE=3 / 国内=0
- 除外 (採用窓外・重複): Starlette NTLM SSRF GHSA-wqp7-x3pw-xc5r (2026-05-21 公開), Cisco CVE-2026-20230 (2026-06-04 公開), Sophos AI EDR evasion (2026-06-02 公開), Nightmare Eclipse "bone shattering" (7/14 予定、6/14 未発表), vitest GHSA-g8mr-85jm-7xhm (2026-06-01 公開), CCA jailbreak (2025-03-14 公開)
- HTTP 403 対象サイト (WebSearch スニペット経由で補完): BleepingComputer, The Hacker News, CSO Online, TechTimes, JVN, JPCERT, IPA

</details>
