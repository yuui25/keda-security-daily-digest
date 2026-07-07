# KEDA Daily Digest — 2026-07-08 (JST)

> 採用範囲: 公開日 2026-07-06 〜 2026-07-08 (JST)
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

AI バグハンティング (Claude Mythos / Project Glasswing) による CVE 開示急増が継続する中、Gitea Docker の認証バイパス CVE-2026-20896 (CVSS 9.8) が公開 13 日で野生悪用に移行し Sysdig が捕捉した。CERT/CC は Tenda ルーター複数機種の未文書バックドア CVE-2026-11405 を開示、ベンダー未対応・野生悪用確認済み。イランの新脅威クラスター **Cavern Manticore** が .NET モジュール型 C2 フレームワークでイスラエル IT・政府機関を標的とする作戦を継続。Esri Portal (CVE-2026-13019, CVSS 9.8) および HP Deskjet 2800 (CVE-2026-13753) の認証不備も本日新たに公開された。

---

## AI 関連ニュース

> 採用窓 (2026-07-06〜08) に公開された AI 関連記事: 確認 2 件。前日ダイジェスト (07-07) が 7/5〜7/7 を既掲載のため、7/6〜7/7 の一部は除外済み。

- **[2026-07-06]** [Claude Mythos / Project Glasswing が月間 CVE 開示を過去最高比 3.5 倍に押し上げ](https://winbuzzer.com/2026/07/06/ai-bug-hunters-coincide-with-record-cve-disclosures-xcxwbn/) — 6 月単月で主要 21 組織から高/クリティカル CVE 約 1,500 件を公開、Mythos リリース前の月間記録を大幅超過。Anthropic は Glasswing で 23,019 件スキャン中 6,202 件が高/クリティカル・真陽性率 90% 以上と報告。*(WinBuzzer / Epoch AI / Anthropic)*
- **[2026-07-07]** [White House が OpenAI・Anthropic・Google とフロンティアモデル任意事前審査フレームワークを最終協議](https://aiweekly.co/alerts/white-house-nears-voluntary-frontier-model-deal-with-top-ai-labs) — モデル公開前 30 日間の政府レビューウィンドウ設定・輸出制御適用基準等を規定予定。Trump が 6 月署名の大統領令 "Promoting AI Innovation and Security" の実施細則として策定。発表は「7 月 7 日の週」と FT が報道。*(Financial Times / AI Weekly)*

---

## セキュリティ関連ニュース

- **[2026-07-06]** [Gitea Docker 認証バイパス CVE-2026-20896 が公開 13 日で野生悪用開始 — Sysdig が in-the-wild エクスプロイト初観測](https://thehackernews.com/2026/07/threat-actors-probe-gitea-docker-flaw.html) — `REVERSE_PROXY_TRUSTED_PROXIES = *` デフォルト設定下で任意 IP から `X-WEBAUTH-USER` ヘッダーを送信し admin なりすまし可。パッチ v1.26.3 (Docker Hub) は提供済みだが未適用インスタンスへの攻撃が確認。*(THN / Sysdig / SecurityWeek)*
- **[2026-07-06]** [イラン系 Cavern Manticore が新モジュール型 C2 フレームワーク「Cavern」でイスラエル IT・政府機関を標的](https://thehackernews.com/2026/07/iran-linked-hackers-use-new-cavern-c2.html) — MOIS 系の新脅威クラスター (MuddyWater/Lyceum と戦術重複)。.NET ベースの Cavern エージェント+偵察/認証情報窃取/横移動モジュール群で構成。VirusTotal 検出率ほぼゼロで回避性能高。*(Check Point Research / THN)*
- **[2026-07-07]** [CERT/CC が Tenda ルーター複数機種 (FH1201/W15E/AC10/AC5/AC6) の未文書バックドア CVE-2026-11405 を開示](https://kb.cert.org/vuls/id/213560) — `httpd` の `login()` が認証失敗時に `sys.rzadmin.password` で裏パスワード照合し、ユーザー名任意で完全管理者アクセスを許可。Tenda は 5 月 19 日の通知以降無回答・未パッチ・野生悪用確認済み。公開 PoC (Nmap NSE スクリプト) あり。*(CERT/CC VU#213560 / THN)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-07-06 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-13019 | Esri Portal for ArcGIS ≤12.1 (Windows/Linux/k8s) | CWE-306 / **9.8** | メールパスリセット有効時に「秘密の質問」リセット API エンドポイントが未認証で到達可 → 任意アカウントのパスワードリセット → 完全乗っ取り | 2026-06-23 パッチ提供 (commit 不明) | 2026-07-07 NVD 公開 / CVSS 9.8 / 未認証 |
| CVE-2026-11405 | Tenda FH1201 / W15E / AC10 / AC5 / AC6 (複数 FW バージョン) | CWE-912 / **Critical** | `/bin/httpd` の `login()` が認証失敗時に config の `rzadmin` バックドアパスワードと照合 → ユーザー名任意で web 管理 I/F の完全管理者権限取得 | 未パッチ (CERT/CC VU#213560) | 2026-07-07 公開 / ベンダー無回答 / 野生悪用確認 / PoC 公開 |
| CVE-2026-20896 | Gitea Docker ≤1.26.2 (Docker Hub 公式イメージ) | CWE-346 / **9.8** | `REVERSE_PROXY_TRUSTED_PROXIES=*` デフォルト設定で任意送信元が `X-WEBAUTH-USER` ヘッダーで任意ユーザーとして認証バイパス → リポジトリへの完全アクセス・RCE も可 | Docker v1.26.3 リリース済み | 2026-07-06 野生悪用初観測 / CVSS 9.8 / コンテナデプロイ多数 |
| CVE-2026-13753 | HP Deskjet 2800 All-in-One Printer ≤TBP1CN2612AR | CWE-862 / **High** | Web サーバー API エンドポイントへの認可チェック欠落 → 未認証で Wi-Fi 認証情報・管理設定・セキュリティデータを読取可能 | HP セキュリティ更新待ち (JVN 参照) | 2026-07-07 JVN 公開 / 国内普及プリンター / 認証情報漏洩 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|---|---|---|---|---|
| 2026-07-07 | JVNVU#90409906 / CVE-2026-13753 | HP Deskjet 2800 プリンターシリーズの Web API 認証不備 — 未認証で Wi-Fi 認証情報・管理設定を読取可能 | High / LAN 内機器から認証情報漏洩 | [jvn.jp](https://jvn.jp/vu/JVNVU90409906/) |
| 2026-07-07 | JVNVU (Tenda) / CVE-2026-11405 | Tenda ルーター複数機種の未文書バックドア — ベンダー未対応・野生悪用確認済み | Critical / 未認証遠隔完全管理者アクセス | [kb.cert.org](https://kb.cert.org/vuls/id/213560) |

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| WinBuzzer (July 6 AI CVE spike) | Mythos CVE spike 採用 ✓ |
| AI Weekly / FT (White House AI framework) | White House voluntary AI standards 採用 ✓ |
| THN / Sysdig (Gitea CVE-2026-20896) | 野生悪用報告 (July 6) 採用 ✓ |
| THN / Check Point (Cavern Manticore) | イラン C2 フレームワーク記事 (July 6) 採用 ✓ |
| CERT/CC VU#213560 / THN (Tenda CVE-2026-11405) | バックドア開示 (July 7) 採用 ✓ |
| NVD (CVE-2026-13019 Esri Portal) | July 7 公開 / CVSS 9.8 採用 ✓ |
| JVN / JVNVU#90409906 (HP Deskjet) | July 7 公開 採用 ✓ |
| github.com/advisories | Jul 6-7 に確認した GHSA は初期公開日が窓外 (Feb-May 2026) のため除外 |
| bleepingcomputer.com | 403 — WebSearch スニペットで代替 |
| thehackernews.com | 403 — WebSearch スニペットで代替 |
| jvn.jp | 403 — WebSearch スニペットで確認 |
| cisa.gov (KEV) | 403 — WebSearch 確認: 窓内 (7/6〜7/8) の新規 KEV 追加なし |
| Google DeepMind / OpenAI Blog | 窓内の新規セキュリティ関連リリースなし |
| Sysdig JADEPUFFER | 公開 July 1 (窓外) 除外 |
| NetNut/Popa 取締り | 公開 July 2-3 (窓外) 除外 |
| Oracle EBS CVE-2026-46817 | 公開 July 2 (窓外) 除外 |
| ARToken PhaaS | 公開 July 1-3 (窓外) 除外 |
| Google FARO AI ガバナンス提案 | 原文書 June 26 公開 (窓外) 除外 |
| EchoLeak CVE-2025-32711 | 2025-06 公開 (窓外) 除外 |
| Squidbleed CVE-2026-47729 | June 23 公開 (窓外) 除外 |
| DuneSlide CVE-2026-50548/50549 (Cursor) | July 1 公開 (窓外) 除外 |

### 集計サマリ

- **巡回ソース数**: 約 25
- **採用件数**: AI=2 / Security=3 / CVE=4 / 国内=2
- **除外理由内訳**: 古すぎ (窓外)=13 / 重複 (前回 7 ダイジェスト掲載済み)=多数 / 日付不明=0
- **件数が通常より少ない理由**: 07-07 ダイジェストが 7/5〜7/7 を既掲載のため 7/6〜7/7 の多くが重複除外。7/8 は JST 午前 5 時時点のため本日公開ニュースの大半が未掲載状態。

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-07-01 〜 2026-07-07) の全 CVE/GHSA/URL を除外済み。*
