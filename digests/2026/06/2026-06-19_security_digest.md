# KEDA Daily Digest — 2026-06-19 (JST)

> 採用範囲: 公開日 2026-06-17 〜 2026-06-19
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

---

## AI

- **[新拠点] Anthropic、ソウルオフィス開設とMSICT MOU締結** (2026-06-17) — NAVER・Samsung SDS・LG CNS・Nexon・Hanwha・Channel Corpと提携、Choi KiYoung氏が代表取締役、アジア太平洋第3拠点。 https://www.anthropic.com/news/seoul-office-partnerships-korean-ai-ecosystem

- **[続報] Anthropic Claude / Fable 5輸出規制、数日内緩和の観測** (2026-06-18) — 米韓ワシントン協議が継続中、Digital Today Korea等が「数日内に一部解除」と報道。正式発表なし。 https://www.digitaltoday.co.kr/news/articleView.html?idxno=537881

- **[CLI廃止] Google Gemini CLI → Antigravity CLI移行、非エンタープライズユーザーを遮断** (2026-06-18) — Go製のAntigravity CLIがMCPおよびマルチエージェント並列実行をサポート、Gemini CLIは非エンタープライズユーザーへのアクセスを終了。 https://developers.googleblog.com/en/antigravity-cli-now-generally-available/

---

## Security

- **[Breach] Klue OAuthトークン盗難でSalesforce CRMデータ流出、Icarusグループが複数組織を恐喝** (2026-06-18) — OAuthトークン経由でSalesforceから競合情報SaaS Klueの顧客データを窃取、HuntressやReliaQuestを含む複数組織が被害、Salesforceは統合を無効化。 https://www.bleepingcomputer.com/news/security/klue-oauth-token-breach-icarus-extortion-salesforce-crm/

- **[RansomGroup] ShinyHunters、MSG Sports 2,600万件レコードを公開** (2026-06-17) — 期限切れ後に45GBダンプを公開、Madison Square Garden の2度目の大規模侵害。 https://www.darkreading.com/cyberattacks-data-breaches/shinyhunters-msg-sports-26m-records-published

- **[RansomGroup] SpaceBears、ECOVACS Robotics侵害を主張** (2026-06-16) — 2TBのデータ窃取を主張、中国ロボット掃除機大手への攻撃でサプライチェーンリスクを示唆。 https://www.hackread.com/spacebears-ecovacs-robotics-breach-2tb/

- **[Malware] Steam Workshop経由でDarkKomet/Lumma/Vidar/仮想通貨採掘マルウェアが拡散** (2026-06-17) — Kaspersky報告、application-type壁紙を悪用、中国・ロシアユーザーを主標的、Steamはパッケージを削除済み。 https://securelist.com/steam-workshop-malware-wallpaper-engine/

- **[EoP/NoFix] CVE-2026-50656 Microsoft Defender TOCTOU特権昇格、公開エクスプロイト存在** (2026-06-17) — CVSS 7.8 / CWE-59 シンボリックリンク競合、NT AUTHORITY\SYSTEM シェル取得可能、パッチ未提供、全パッチ済みWindows 10/11に影響。 https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-50656

---

## CVE

| CVE / GHSA | 公開日 | CVSS | CWE | 製品・バージョン | 概要 | KEV/EPSS |
|---|---|---|---|---|---|---|
| CVE-2026-20181 + CVE-2026-20190 | 2026-06-17 | 9.1 (chain) | CWE-522 / CWE-78 | Cisco ISE ≤ 3.4 | 未認証でハッシュ化済み認証情報を取得 (7.5) → admin OS コマンドインジェクション → root RCE (9.1)。フル修正は2026年8月リリース予定。 | — |
| GHSA-r8mh-x5qv-7gg2 / CVE-2026-55200 | 2026-06-17 | 9.2 | CWE-122 | libssh2 ≤ 1.11.1 | `ssh2_transport_read()` の packet_length 上限未検証によるヒープ OOB 書き込み → RCE。fix: commit `97acf3d`。 | — |
| CVE-2026-35293 | 2026-06-17 | 9.8 | CWE-306 | Oracle WebCenter Sites | Oracle CSPU June 2026 収録、未認証 HTTP RCE、完全サーバー制御。245パッチ中 100+件が未認証リモート。 | — |
| CVE-2026-12289 / CVE-2026-12328 | 2026-06-16 UTC | 8.8 / 8.1 | CWE-416 / CWE-119 | Firefox 152 (mfsa2026-57) | WebRender EoP (8.8)・メモリ安全性 RCE (8.1)、計40件修正 (高・クリティカル 13件)。 | — |
| CVE-2026-50656 | 2026-06-16 UTC | 7.8 | CWE-59 | Microsoft Defender (全パッチ済み Win10/11) | TOCTOU シンボリックリンク競合で SYSTEM 昇格、パッチ未提供・公開 PoC あり。 | — |
| GHSA-p3h9-73g9-x6m3 / CVE-2026-54388 | 2026-06-17 | 7.5 | CWE-444 | Tinyproxy ≤ 1.11.2 | 複数 Content-Length による HTTP リクエストスマグリング、パッチ未提供、キャッシュポイズニング・ACL バイパスに悪用可能。 | — |

---

## 国内

直近2日間に該当する新規ニュースは確認できませんでした。

---

*excluded_set 参照: 直近7ダイジェスト (2026-06-12 〜 2026-06-18) の全 CVE/GHSA/URL を除外済み。*
