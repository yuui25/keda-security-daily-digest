# KEDA Daily Digest — 2026-05-24 (JST)

> 採用範囲: 公開日 2026-05-22 〜 2026-05-24
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Laravel-lang PHP パッケージへの大規模サプライチェーン攻撃が発覚し、700+ バージョンに Composer 自動実行の RCE バックドアが混入、CI/CD トークンやクラウド認証情報が標的になった。国内企業 Victoria's Secret が Scattered Spider + DragonForce ランサムウェアによるサイバー攻撃で一時システム停止し $10M 超の損失見込みを公表。CVE 面では Nezha Monitoring の CVSS 9.9 クロステナント RCE をはじめ Critical 3 件が GitHub Advisory Database に公開された。AI 分野では Anthropic が Q2 で初の営業黒字 ($559M) を予測し、IBM が Project Glasswing に参加するなど AI × セキュリティの構造転換が加速している。

## AI 関連ニュース

- **[2026-05-22]** [Anthropic が Q2 2026 で初の営業黒字 ($559M) を予測 — 売上 $10.9B (QoQ +130%) を投資家向けに開示](https://dataconomy.com/2026/05/21/anthropic-profit-revenue-10-9-billion/) — Anthropic が Q2 に約 $559M 営業黒字と売上 $10.9B を投資家に開示、2028 年以降と見ていた黒字化が急加速し OpenAI の IPO 機運にも影響 *(Dataconomy / Bloomberg)*

- **[2026-05-22]** [IBM が AI セキュリティポートフォリオを拡張し Anthropic の Project Glasswing に参加](https://www.ibm.com/think/news/ibm-expands-ai-security-cyberattacks-accelerate) — 2026 X-Force レポートで公開アプリ脆弱性悪用が前年比 44% 増と報告、AI により exploit 開発が平均 9 時間まで短縮 *(IBM Think)*

- **[2026-05-22]** [Push Security が「Browser & Identity Attacks Matrix」を GitHub 公開 — AiTM・ClickFix・DeviceCode 認証乗っ取りなど 5 手法を MITRE ATT&CK 形式で体系化](https://pushsecurity.com/blog/introducing-the-browser-and-identity-attacks-matrix) — SaaS 環境とブラウザ経由のアイデンティティ攻撃手法を攻撃者視点でオープンソース化、AI エージェントの OAuth 乗っ取りシナリオも対象 *(Push Security)* ([GitHub](https://github.com/pushsecurity/browser-identity-attacks-matrix))

- **[2026-05-22]** [Google・Anthropic・OpenAI が Frontier AI 競争で「実質拮抗」— 各社がコスト・速度・能力でトレードオフ戦略を採用](https://www.axios.com/2026/05/21/google-ai-anthropic-openai-war) — Google は Gemini 3.5 Flash で価格効率優先、Anthropic は Mythos で攻撃能力リード、OpenAI は IPO 後の規模で追撃を計画 *(Axios)*

- **[2026-05-23]** [2026 年: AI 支援攻撃の元年 — Mandiant M-Trends で CVE 悪用まで 23 日→9 時間に短縮、28.3% の CVE が開示 24 時間以内に悪用](https://thehackernews.com/2026/05/2026-year-of-ai-assisted-attacks.html) — 攻撃者の AI 活用により exploit 開発速度が飛躍的に高速化、防御側との非対称が拡大 *(The Hacker News)*

- **[2026-05-23]** [「AI エージェントはすでに境界内にいる」— アイデンティティ暗数が可視 IAM 資産の 57% を上回る、ゾンビアカウント経由の侵入が顕在化](https://thehackernews.com/2026/05/your-ai-agents-are-already-inside.html) — 企業環境で 40% 超のアカウントが正規ユーザーを失ったゾンビ状態、AI エージェントが侵入経路として利用される懸念が拡大 *(The Hacker News)*

## セキュリティ関連ニュース

- **[2026-05-22/23]** [Laravel-lang PHP パッケージにサプライチェーン攻撃 — 4 パッケージ・700+ バージョンに Composer 自動実行の RCE バックドアが混入](https://thehackernews.com/2026/05/laravel-lang-php-packages-compromised.html) — `laravel-lang/{lang,http-statuses,attributes,actions}` が汚染、AWS/GCP/Azure 鍵・SSH 秘密鍵・CI/CD トークン・仮想通貨ウォレットを一括窃取するクロスプラットフォームフレームワークをインストール *(The Hacker News / Aikido Dev)*

- **[2026-05-24]** [Victoria's Secret がサイバー攻撃でシステムおよびウェブサイトを一時停止 — Scattered Spider + DragonForce ランサムウェアグループの関与が疑われる](https://www.bleepingcomputer.com/news/security/victorias-secret-restores-critical-systems-after-cyberattack/) — 5/24 に不正アクセスを検知してシステムを停止、Q2 営業利益に約 $10M の影響と決算発表の延期を発表 *(BleepingComputer / SecurityWeek)*

- **[2026-05-22]** [CISA KEV への追加なし確認: 5/21 に Langflow CVE-2025-34291 と Trend Micro Apex One CVE-2026-34926 の 2 件を追加](https://www.cisa.gov/news-events/alerts/2026/05/21/cisa-adds-two-known-exploited-vulnerabilities-catalog) — 直近 2 日間での KEV 新規追加は未確認、引き続き 5/20 追加の 7 件 (Microsoft Defender 含む) への対応を優先 *(CISA)*

- **[2026-05-23]** [Nezha Monitoring ダッシュボードで Critical/High の複数脆弱性が同日公開 — CVE-2026-46716 (RCE 9.9), CVE-2026-46717 (SSRF 8.8), CVE-2026-47124 (情報漏洩)](https://github.com/advisories/GHSA-99gv-2m7h-3hh9) — RoleMember 権限から全テナントサーバーへの任意コマンド実行が可能、オープンソースの監視ツールとして広く利用されているため影響範囲が懸念 *(GitHub Security Advisories)*

- **[2026-05-22]** [YesWiki に認証不要 SQL インジェクション (CVE-2026-46670, CVSS 9.8) — Bazar フォームの import 機能から全 DB を読み取り可能](https://github.com/advisories/GHSA-jwvv-qr7q-cv8j) — `FormManager::create()` の SQL クエリ構築に allowlist チェックが欠落、PHP Wiki プラットフォームの全バージョン (< 4.6.4) に影響 *(GitHub Security Advisories)*

- **[2026-05-22]** [FileBrowser Quantum に認証不要パストラバーサル (GHSA-qqqm-5547-774x, CVSS 9.3) — 公開共有リンクから外部ファイルの読み取り・移動・上書きが可能](https://github.com/advisories/GHSA-qqqm-5547-774x) — `publicPatchHandler` がパス結合後にサニタイズする処理順序の欠陥を突き、`AllowModify=true` の公開共有リンクで任意ファイル操作が可能 *(GitHub Security Advisories)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-05-22 以降 / GitHub Advisory Database 収録・修正コミット参照可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-46716 / [GHSA-99gv-2m7h-3hh9](https://github.com/advisories/GHSA-99gv-2m7h-3hh9) | Nezha Monitoring >= 1.4.0, < 1.14.15-...-d7526351cf97 | CWE-78 / **9.9** | `POST /api/v1/cron` が `commonHandler` (全認証ユーザー) で処理されるため、RoleMember が `Cover=CronCoverAll` のタスクを作成すると全テナントサーバーに任意シェルコマンドが実行される | [fix d7526351](https://github.com/nezhahq/nezha/commit/d7526351cf97) | EPSS 未取得・Critical |
| CVE-2026-46670 / [GHSA-jwvv-qr7q-cv8j](https://github.com/advisories/GHSA-jwvv-qr7q-cv8j) | YesWiki < 4.6.4 | CWE-89 / **9.8** | `FormManager::create()` の Bazar フォーム import 機能でユーザー入力を直接 SQL に結合 → 未認証で任意 SQL 実行・全 DB 漏洩 | [fix 1f485c04](https://github.com/YesWiki/yeswiki/commit/1f485c049db030b94c047ec219e63534ac81142e) (commit 不明・advisory URL で代用) | Critical |
| [GHSA-qqqm-5547-774x](https://github.com/advisories/GHSA-qqqm-5547-774x) | FileBrowser Quantum < 0.0.0-20260518193514-28e9b81e438e | CWE-22 / **9.3** | `publicPatchHandler` がパス結合後にサニタイズするため `AllowModify=true` の公開共有リンクで `../../` トラバーサルが可能 → ファイル読み取り・移動・上書き | [patch 28e9b81e](https://github.com/gtsteffaniak/filebrowser/commit/28e9b81e438e) | Critical |
| CVE-2026-46717 / [GHSA-w4g9-mxgg-j532](https://github.com/advisories/GHSA-w4g9-mxgg-j532) | Nezha Monitoring >= 1.4.0, < 1.14.15-...-d06d539d34c1 | CWE-918 / **8.8** | `POST /api/v1/notification` が `commonHandler` で処理されるため、RoleMember が攻撃者制御 URL へ HTTP リクエストを送信させ完全なレスポンスボディを反射 → イントラネット HTTP SSRF | [fix d06d539d](https://github.com/nezhahq/nezha/commit/d06d539d34c1) | High |
| CVE-2026-47124 / [GHSA-hvv7-hfrh-7gxj](https://github.com/advisories/GHSA-hvv7-hfrh-7gxj) | Nezha Monitoring >= 1.4.0 | CWE-200 / Moderate | WebSocket サーバーがストリームの認可チェックを欠如、認証済み RoleMember が他テナントのサーバーテレメトリデータを閲覧可能 | (commit 不明) | — |

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-05-22 | CVE-2026-0265 | Palo Alto PAN-OS で CAS 有効時に JWT アルゴリズム混乱攻撃により認証バイパス → GlobalProtect 等への不正アクセス | CVSS 7.2 (High) | [JPCERT注意喚起](https://www.jpcert.or.jp/at/2026.html) / [Palo Alto Advisory](https://security.paloaltonetworks.com/CVE-2026-0265) |
| 2026-05-22/23 | — (Supply Chain) | Laravel-lang Composer パッケージ汚染: 国内 PHP/Laravel 開発環境 CI/CD パイプラインへの影響を確認のこと | RCE / 認証情報窃取 | [Aikido Blog](https://www.aikido.dev/blog/supply-chain-attack-targets-laravel-lang-packages-with-credential-stealer) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 25 (WebSearch 20回+ / WebFetch 15回+)
- 採用件数: AI=6 / Security=6 / CVE=5 / 国内=2
- 除外理由内訳:
  - 古すぎ (> today-2): CVE-2026-0265 (Palo Alto, May 13) → 国内 JPCERT 注意喚起が May 22 のため国内欄に採用、CVE-2026-47138 / CVE-2026-47125 / CVE-2026-46715 (GitHub Database に May 23 と表示も、advisory 本文は May 17)、GPT-5.5 Instant (May 5)、OpenAI Daybreak (May 12)、Google AI zero-day 2FA bypass (May 11)
  - 重複 (excluded_set): CVE-2026-9082, CVE-2026-34926, CVE-2026-20223, CVE-2026-41091, CVE-2026-45498, CVE-2026-46333, CVE-2026-23918, OpenAI IPO S-1 filing (fortune.com May 22 → May 23 digest 掲載済), Drupal 積極悪用報道 (May 22/23 digest 掲載済), Trend Micro Apex One, Cisco Secure Workload, Ubiquiti UniFi OS など
  - 日付不明: CVE-2026-27740 (Discourse AI XSS), IBM article exact date (May 22 推定), Mandiant M-Trends article exact date (May 23 推定)
- 取得失敗ソース: thehackernews.com (403), bleepingcomputer.com (403), securityaffairs.com (403), ibm.com (403), nvd.nist.gov (403), jpcert.or.jp (403), paloaltonetworks.com (403) — 各サイトの検索スニペットおよびキャッシュ情報で補完

</details>
