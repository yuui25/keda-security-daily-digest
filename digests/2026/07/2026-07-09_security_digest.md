# KEDA Daily Digest — 2026-07-09 (JST)

> 採用範囲: 公開日 2026-07-07 〜 2026-07-09 (JST)
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

CISA が 7/7 に Joomla 拡張 2 件 (CVSS 10.0 未認証 RCE) + Langflow IDOR + Adobe ColdFusion の計 4 CVE を KEV に緊急追加し、連邦機関修正期限を 7/10 と設定した。中国 APT **UAT-7810** が新マルウェア群 LONGLEASH/DOGLEASH/JARLEASH で ORB ネットワークを拡大中と Cisco Talos が 7/8 に公表。国内では KDDI が 6 ISP 共有メールシステムへの侵害を 7/7 に公表し、1,223 万メールアドレス・761 万パスワード漏洩という国内通信事業者史上最大規模のメール侵害が確認された。AI 面では OpenAI が完全双方向音声モデル **GPT-Live** を 7/8 に正式ローンチし、米企業が中国 AI モデル (Z.ai GLM-5.2 / DeepSeek) にコスト主導で大規模移行していることが CNBC 報道で明らかになった。

---

## AI 関連ニュース

- **[2026-07-08]** [OpenAI が完全双方向音声モデル GPT-Live を正式ローンチ — ChatGPT のデフォルト音声を GPT-Live-1 / GPT-Live-1 mini に刷新](https://openai.com/index/introducing-gpt-live/) — フルデュプレックスアーキテクチャで同時に聴取・発話; 複雑タスクはバックグラウンドで GPT-5.5 に委譲して結果を返す; 有料 Go/Plus/Pro プラン向けに iOS/Android/Web でグローバル展開開始。*(OpenAI / VentureBeat / MarkTechPost)*

- **[2026-07-07]** [CNBC: 米企業が OpenAI・Anthropic コスト増に押され中国 AI モデルへ大規模移行](https://www.cnbc.com/2026/07/07/chinese-ai-models-costs-us-openai-anthropic.html) — Z.ai GLM-5.2 は Vercel で週間トークン量 27 倍・顧客数 80 倍の初週成長を記録; OpenRouter 週間トークン使用の 30% 超が中国モデル由来; DeepSeek/GLM は US モデルより 60〜90% 安く「タスクに最安の十分なモデルを割り当てる」コスト最適化が定着。*(CNBC / ResultSense / Techstrong.ai)*

- **[2026-07-08]** [ITU AI for Good サミット Centre Stage 開幕 — 44 委員国連委員会がアジェンティック AI セキュリティ要件の国際標準化に着手](https://aiforgood.itu.int/summit26/) — セキュリティプロの 48% が「アジェンティック AI」を 2026 年最大の攻撃ベクターと指摘 (Dark Reading 調査); ITU 標準化作業で AI エージェントのセキュリティ要件が 194 加盟国向け国際勧告に組み込まれる見通し。*(ITU / TechTimes / AI for Good)*

---

## セキュリティ関連ニュース

- **[2026-07-07]** [CISA が Joomla 拡張 2 件・Langflow・Adobe ColdFusion の計 4 CVE を KEV に緊急追加 — 連邦機関修正期限 7/10](https://thehackernews.com/2026/07/cisa-adds-4-actively-exploited-adobe.html) — CVE-2026-48908 (JoomShaper, CVSS 10.0) / CVE-2026-56290 (Joomlack, CVSS 10.0) は未認証 PHP ファイルアップロード経由 RCE; CVE-2026-55255 (Langflow) は IDOR で他ユーザーの LLM プロバイダー API キー・AWS キーを盗用; CVE-2026-48282 (Adobe ColdFusion) はパストラバーサル RCE の実悪用 [続報]。*(CISA / THN / SecurityWeek)*

- **[2026-07-08]** [Cisco Talos: 中国 APT UAT-7810 が新マルウェア LONGLEASH/DOGLEASH/JARLEASH で ORB ネットワークを大規模拡大](https://blog.talosintelligence.com/uat-7810/) — LONGLEASH は SHORTLEASH の後継で中間 C2 ノード機能 (上流コントローラーからコマンドを取得しピアインプラントへ転送) を追加; JARLEASH は Java 製バックドア; 攻撃チェーンは Ruckus ルーターの既知 CVE (CVE-2020-22653/22658、CVE-2023-25717) を悪用して初期侵害 → ORB ネットワーク拡張。*(Cisco Talos / THN / BleepingComputer)*

- **[2026-07-07]** [KDDI が国内通信業者史上最大のメール侵害を公表 — 6 ISP 共有システムが被害、1,223 万メールアドレス・761 万パスワード流出](https://www.japantimes.co.jp/business/2026/07/07/companies/kddi-passwords-number/) — STNet・KDDI Web Communications・JCOM・中部テレコミュニケーション・Nifty・BIGLOBE の共有メール基盤に利用の第三者ソフトウェア脆弱性を悪用; 侵害開始は 5 月中旬、発覚は 6/17; 二次被害 (フィッシング・アカウント乗っ取り) のリスクが高く、対象者は速やかにパスワード変更が必要。*(Japan Times / nippon.com / SecurityAffairs)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-07-07 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-48908 | JoomShaper SP Page Builder (Joomla 全対象バージョン) | CWE-434 / **10.0** | 未認証攻撃者が `?option=com_sppagebuilder&task=asset.uploadCustomIcon` に POST → MIME/拡張子バリデーション欠如 → 任意 PHP ファイルを Web ルートへ書き込み → RCE | アドバイザリ参照 (commit 不明) | **CISA KEV 2026-07-07** / CVSS 10.0 / 未認証 / 連邦修正期限 7/10 / ゼロデイ悪用確認 |
| CVE-2026-56290 | Joomlack Page Builder CK < 3.6.0 (Joomla 拡張) | CWE-284 / **10.0** | 未認証でファイルアップロードエンドポイントに到達 → アクセス制御不備 → 実行可能ファイルのアップロード成功 → Web シェル経由 RCE | [Page Builder CK 3.6.0 (2026-06-27)](https://www.joomlack.fr/) | **CISA KEV 2026-07-07** / CVSS 10.0 / 未認証 / 連邦修正期限 7/10 / Joomla 拡張全般への水平伝播推奨 |
| CVE-2026-55255 | Langflow < 1.10.0 (Python/pip) | CWE-639 / **6.1** | 認証済み攻撃者が `/api/v1/responses` エンドポイントに被害者の `flow_id` を指定 → オーナー検証なし (IDOR) → 被害者の LLM プロバイダー API キー・AWS キーを盗用して任意フローを実行 | [Langflow 1.10.0](https://github.com/langflow-ai/langflow) | **CISA KEV 2026-07-07** / AI プラットフォームのマルチテナント認可欠如パターン / LLM プロバイダーキー漏洩確認 |
| CVE-2026-56437 | Fujitsu Pupsman インストーラー (全バージョン) | CWE-427 / **7.8** | 攻撃者がインストーラーと同一ディレクトリに悪意 DLL を配置 → Windows DLL 検索順序ハイジャック → インストーラー実行時に SYSTEM 権限で任意コード実行 | JVN#62347140 参照 (commit 不明) | 2026-07-07/08 JVN 公開 / DLL ハイジャック / SYSTEM 権限昇格 / 国内業務ソフト広範利用 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|---|---|---|---|---|
| 2026-07-07 | KDDI データ侵害 (インシデント) | KDDI 系 6 ISP の共有メールシステム (第三者ソフト脆弱性) 経由で 1,223 万メールアドレス・761 万パスワードが流出 — 国内通信業者史上最大規模 | 高 / フィッシング・アカウント乗っ取りリスク | [Japan Times](https://www.japantimes.co.jp/business/2026/07/07/companies/kddi-passwords-number/) |
| 2026-07-07 | JVN#87285119 / CVE-2026-58315 | Seiko Epson 複数プリンター・スキャナーの Web Config に CSRF 脆弱性 → 管理者セッション中に攻撃者が設定を無断変更 | CVSS 4.3 / 機器設定の不正変更 | [JVN](https://jvn.jp/en/jp/JVN87285119/) |
| 2026-07-07 | JVN#62347140 / CVE-2026-56437 | Fujitsu Pupsman インストーラーに DLL ハイジャッキング脆弱性 → インストーラー実行時に SYSTEM 権限で任意コード実行 | CVSS 7.8 / 高 / ローカル権限昇格 | [JVN](https://jvn.jp/en/jp/JVN62347140/) |
| 2026-07-08 | JVN#90566559 / CVE-2025-49656 他 | Apache Jena Fuseki の管理者権限でのパストラバーサル → Fuseki サーバーの指定ファイル領域外にデータベースファイルを作成可能 — JVN 2026-07-08 公開 (CVE 元発表 2025-07) | 重要 (Important) / Fuseki サーバーの完全性侵害 | [JVN](https://jvn.jp/en/jp/JVN90566559/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| openai.com / VentureBeat / MarkTechPost | GPT-Live 2026-07-08 公開 ✓ |
| cnbc.com / ResultSense | 中国 AI モデル米企業移行 2026-07-07 ✓ |
| aiforgood.itu.int / TechTimes | ITU AI for Good サミット 7/8 Centre Stage 開幕 ✓ |
| CISA / THN / SecurityWeek / TechNadu | CVE-2026-48908 / CVE-2026-56290 / CVE-2026-55255 KEV 2026-07-07 追加 ✓ |
| blog.talosintelligence.com / THN / BleepingComputer | UAT-7810 LONGLEASH 2026-07-08 公開 (403→WebSearch スニペット代替) ✓ |
| japantimes.co.jp / nippon.com / securityaffairs.com | KDDI データ侵害 2026-07-07 公表 ✓ |
| jvn.jp (JVN#87285119 / JVN#62347140 / JVN#90566559) | 2026-07-07〜08 公開 (403→WebSearch スニペット代替) ✓ |
| cybersecuritynews.com / gbhackers.com (ModSecurity) | ModSecurity CVE-2026-52747/52761 は公開日 2026-06-29 → 窓外除外 |
| google cloud blog (Oracle PeopleSoft) | 公開日 2026-06-11 → 窓外除外 |
| bleepingcomputer.com / thehackernews.com | 403 — WebSearch スニペットで代替 |
| cisa.gov (KEV) | 403 — WebSearch 確認: 7/8-9 の新規 KEV 追加は確認できず |
| f5.com/labs (weekly bulletin) | 403 — WebSearch スニペットで確認 (ModSecurity 日付窓外のため不採用) |

### 集計サマリ

- **巡回ソース数**: 約 20
- **採用件数**: AI=3 / Security=3 / CVE=4 / 国内=4
- **除外理由内訳**: 古すぎ (today-2 = 2026-07-07 より前)=4 (ModSecurity CVE 2026-06-29 / Oracle PeopleSoft 2026-06-11 / OpenAI gpt-realtime-2.1 2026-07-06 / Langflow CVE-2026-5027 2026-06 発表) / 重複 (直近 7 ダイジェスト掲載済み)=多数 / 日付不明=0

### 主要除外

- ModSecurity CVE-2026-52747/52761 (公開 2026-06-29 → 窓外 / F5 Labs 7/8 週報には掲載)
- Oracle PeopleSoft CVE-2026-35273 + Google/Mandiant 確認報告 (2026-06-11 公開 → 窓外)
- OpenAI gpt-realtime-2.1/2.1-mini (2026-07-06 公開 → 窓外; GPT-Live は 7/8 公開のため採用)
- Langflow CVE-2026-5027 path traversal (2026-06 公開、2026-07-07 BleepingComputer 記事は続報だが CVE 自体が窓外 / CVE-2026-33017 は 07-02 digest 掲載済み)
- Adobe ColdFusion CVE-2026-48282 KEV 追加 (CVE テーブルは 07-03 digest 掲載済み / セキュリティニュース欄に [続報] として記載)
- ITU AI for Good 委員会発足・UN AI ガバナンス対話 (07-05/06 digest 掲載済み)
- BeyondTrust CVE-2026-40138/40139 / Cilium CVE-2026-49445 / flyto-core CVE-2026-55786/55787 / Formie CVE-2026-52889 (07-07 digest 掲載済み)
- Tenda CVE-2026-11405 / Gitea CVE-2026-20896 / Esri Portal CVE-2026-13019 / HP Deskjet CVE-2026-13753 (07-08 digest 掲載済み)

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-07-02 〜 2026-07-08) の全 CVE/GHSA/URL を除外済み。*
