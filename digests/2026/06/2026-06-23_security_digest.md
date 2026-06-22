# KEDA Daily Digest — 2026-06-23 (JST)

> 採用範囲: 公開日 2026-06-21 〜 2026-06-23
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

QiAnXin XLab が D-Link/QNAP デバイスを標的とするボットネット「AryStinger」を公開——4,300 台超が感染し南朝鮮 48.5% が最多; CVE-2013-3307/CVE-2016-5681 (D-Link) と CVE-2025-11837 (QNAP) を悪用しプロキシ型スパイインフラを構築。OpenAM に事前認証 XSS (CVE-2026-44203、CVSS 9.3) と LDAP インジェクション (CVE-2026-41573、CVSS 8.7)、XWiki Pro に RCE (CVE-2026-44179、CVSS 9.9) が一括公開され、IAM/Wiki 系の権限昇格リスクが改めて浮き彫りに。Anthropic Fable 5 は 6 月 22 日でサブスクリプション無料提供期間が終了し、6 月 23 日から使用クレジット課金へ移行——API は依然オフライン継続。

## AI 関連ニュース

- **[続報][2026-06-22]** [Anthropic Fable 5 / Mythos 5 輸出規制 Day 10〜11 — 6/22 でサブスクリプション (Pro/Max/Team/Enterprise) の無料提供期間が終了し、6/23 より使用クレジット方式 (入力 $10/MTok・出力 $50/MTok、キャッシュ読み取り $1/MTok) へ移行; API 上の `claude-fable-5` エンドポイントは引き続き応答なし; 米商務省との交渉継続中・正式解除発表はなし; Anthropic は「容量が確保でき次第プランに再統合する」と声明](https://www.developersdigest.tech/blog/claude-fable-5-june-22-deadline) *(Developers Digest / Claude.ai / yellow.com)*

## セキュリティ関連ニュース

- **[2026-06-22]** [QiAnXin XLab、D-Link/QNAP ルーターを標的とするボットネット「AryStinger」を公開 — D-Link DIR-850L/DIR-818LW (EoL) に CVE-2013-3307・CVE-2016-5681、QNAP NAS に CVE-2025-11837 を悪用し 4,300 台超を感染; C 亜種 (ルーター向け) と Go 亜種 (NAS 向け) が存在; Dropbear SSH バックドア設置・DNS 書き換え・内部ネットワークスキャン・トラフィックトンネリングでプロキシ型偵察インフラ化; 感染分布: 南朝鮮 48.5%・中国 32%; 帰属未確認](https://www.bleepingcomputer.com/news/security/arystinger-botnet-infected-thousands-of-d-link-routers-worldwide/) *(BleepingComputer / TechRadar / THN / SecurityAffairs / GBHackers)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-21 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| GHSA-fq9h-c788-fx73 / CVE-2026-44203 | OpenAM (openam-oauth2) 13.0.0〜16.1.0 | CWE-79 / **9.3** | OAuth2/OIDC 認可エンドポイントが `form_post` レスポンスモードで `state` パラメーターを `FormPostResponse.ftl` に無害化なし挿入 → 非認証攻撃者が OpenAM オリジン上で任意スクリプト実行・セッション窃取 | [openam 16.1.1](https://github.com/OpenIdentityPlatform/OpenAM/releases) | 2026-06-21 GHSA 公開 / 事前認証・ユーザー操作のみで成立 / Keycloak/Okta 等の form_post 実装へバリアントハント推奨 |
| GHSA-w56x-9778-rppx / CVE-2026-44179 | XWiki Pro Macros (xwiki-pro-macros) 1.13〜1.14.4 | CWE-95 / **9.9** | `excerpt-include` マクロがページタイトル・本文を昇格権限で評価 → ページ編集権限を持つ任意ユーザーが Groovy コードを注入 → RCE・DB 認証情報/暗号鍵漏洩 | [xwiki-pro-macros 1.14.5](https://github.com/xwikisas/xwiki-pro-macros/releases) | 2026-06-21 GHSA 公開 / 編集権限のみで RCE / 他 XWiki 拡張マクロ・Confluence マクロへバリアントハント推奨 |
| GHSA-2vg8-q4c2-5cw3 / CVE-2026-41573 | OpenAM (openam-core-rest) ≤ 16.0.6 | CWE-74 / **8.7** | REST API の `_queryId` パラメーターで `escapeQueryId=false` が明示設定 → 認証済みユーザーが LDAP メタ文字を注入 → ユーザー/グループ列挙・ブラインド LDAP インジェクション; CVE-2021-29156 の回帰 | [openam 16.1.1](https://github.com/OpenIdentityPlatform/OpenAM/releases) | 2026-06-21 GHSA 公開 / エスケープ意図的無効化というアンチパターン / 他 IAM REST API の _queryId 相当パラメーターへバリアントハント推奨 |
| GHSA-wf69-r4mx-43rr / CVE-2026-33692 | AVideo (wwbn/avideo) < 29.0 | CWE-538 / **7.5** | Docker Compose 設定がプロジェクトルートを Apache ドキュメントルートとしてマウント → `.env` ファイルが非認証 HTTP GET で読取可能 → DB 認証情報・管理者パスワード・ネットワーク構成情報が漏洩 | [avideo 29.0](https://github.com/WWBN/AVideo/releases) | 2026-06-22 GHSA 公開 / セキュアデフォルト欠如パターン / 他コンテナ化 Web アプリの`.env` マウント設定へバリアントハント推奨 |

## 国内脆弱性・インシデント情報

> 直近2日間に該当する新規国内ニュースは確認できませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 28 ソース (QiAnXin XLab / BleepingComputer, TechRadar, THN, SecurityAffairs, GBHackers, SecurityWeek, Cybernews, The Register, HelpNetSecurity, ESET WeLiveSecurity, Microsoft Security Blog, Developers Digest, yellow.com, AI Weekly, GitHub Advisory Database (GHSA), OSV.dev, CISA KEV, NVD, SOCRadar, Krebs on Security, Rapid7, Horizon3.ai, watchTowr Labs, security-next.com, JVN, DataBreaches.net, Infosecurity Magazine, SC Media)
- 採用件数: AI=1 / Security=1 / CVE=4 / 国内=0
- 採用件数が目安 (各 8〜12件) を下回った理由:
  - 採用窓 (2026-06-21〜23) は週末〜月曜初日にあたり、大手 AI ラボからの新規発表ペースが低調
  - Anthropic Fable 5 輸出規制 (初報〜返金ウィンドウ) は excluded_set 収録済み、本日は「無料→有償クレジット移行」という新ファクトのみ採用
  - FortiBleed 継続報道 (30,000 件 DB 構築 Cybernews 2026-06-22) は excluded_set 収録済み
  - GPT-5.6: 2026-06-22 時点で OpenAI 公式アナウンスなし、Polymarket 90% 予測市場は観測だが未確認のため除外
- 除外理由内訳:
  - 古すぎ (公開日 < 2026-06-21):
    - Novo Nordisk/FulcrumSec データリーク — DataBreaches.Net 初報 2026-06-15 (採用窓外); SecurityAffairs 記事番号 193763 は AryStinger 記事 193987 より古く 6/21 以前と推定
    - runc GHSA-xjvp-4fhw-gc47/CVE-2026-41579 — 公開 2026-06-13
    - comfyui-manager GHSA-95pq-hr8p-f5g7/CVE-2025-67303 — 公開 2026-01-11
    - NCSC「vibe coding」ブログ (2026-06-18 公開、2026-06-21 digest 掲載済み除外)
    - NCSC「patch wave」警告 — 2026-05-01 公開
    - Black Duck AI コーディング採用 97% 調査 — 2026-06-09 公開
    - Arcade AI Agent $60M Series A — 2026-06-15 BusinessWire アナウンス
    - White House AI EO (EO 14409 / 2026-06-02 署名) — excluded_set 収録済み
    - DaikyoNishikawa LockBit 侵害 — 2026-06-21 digest で「日付確認不可のため除外」と記録済み
  - 重複 (excluded_set 直近 7 ダイジェスト 2026-06-16 〜 2026-06-22):
    - FortiBleed (CISA アラート・30K DB)、AutoJack (6/21 掲載)、Apple usbliter8 (6/21 掲載)
    - Splunk CVE-2026-20253 KEV、GentleKiller ESET、Prinz Eugen ランサムウェア
    - picklescan CVE-2025-71351/71378/CVE-2026-56319、libexpat CVE-2026-56403〜56412
    - Mastra/Sapphire Sleet、Nintendo/TinyPulse、OpenAI GPT-5.6 (観測記事)
    - OpenAM SSRF GHSA-c556-q2mh-477v/CVE-2026-44202 — 2026-06-21 GHSA 公開だが Moderate 評価・OpenAM CVE-2026-44203 と同一修正バージョンのため優先度低く除外
  - 取得失敗ソース (HTTP 403): BleepingComputer 個別記事 (スニペット補完), THN 個別記事, watchTowr Labs ブログ, DataBreaches.net (個別記事)

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-06-16 〜 2026-06-22) の全 CVE/GHSA/URL を除外済み。*
