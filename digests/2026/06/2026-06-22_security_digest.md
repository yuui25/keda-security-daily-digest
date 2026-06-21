# KEDA Daily Digest — 2026-06-22 (JST)

> 採用範囲: 公開日 2026-06-20 〜 2026-06-22
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

libexpat に整数オーバーフロー 10 件 (CVE-2026-56403〜56412)・Crawl4AI に認証バイパス (CVE-2026-56265, CVSS 9.3)・picklescan の検出バイパス 3 手法 (CVE-2025-71351/71378/CVE-2026-56319) が一括公開され、AI エージェントツールチェーンのサプライチェーンリスクが改めて浮き彫りに。非 RaaS 型の新興ランサムウェア Prinz Eugen が Go 製・ランサムノートなし・最近更新ファイル優先という異例の戦術で少なくとも 5 組織を標的にした。

## AI 関連ニュース

- **[続報][2026-06-21]** [[Anthropic Fable 5 / Mythos 5 輸出禁止 Day 9 — API `claude-fable-5` 依然エラー、返金ウィンドウ (6/20) 終了、Kalshi 7/1 前解禁 57%、Trump「交渉順調」発言も正式合意なし](https://www.anthropic.com/news/fable-mythos-access)] *(Fortune / Manifold Markets)*

- **[続報][2026-06-21]** [Microsoft、Mastra npm サプライチェーン攻撃を Sapphire Sleet (北朝鮮 APT38/BlueNoroff) に帰属確認 — 単一メンテナーアカウント "ehindero" 侵害後 88 分で 144 パッケージ汚染、easy-day-js ポストインストールフック → PowerShell バックドア → scdev サービス永続化、週間 DL 110 万超の @mastra/core 含む](https://www.bleepingcomputer.com/news/security/microsoft-links-mastra-ai-supply-chain-attack-to-north-korean-hackers/) *(BleepingComputer / Microsoft Security Blog)*

- **[2026-06-21]** [OpenAI、GPT-5.6 を ChatGPT Pro に暗黙展開か — 複数開発者が「1.5M トークン相当の挙動」を観測、GPT-5.5 比で明確に高速・高精度; Polymarket が 6/22-28 リリースを 83% と算定; OpenAI 公式発表なし](https://aiweekly.co/alerts/openai-plans-june-gpt-56-as-meaningful-improvement) *(AI Weekly / explainx.ai)*

- **[2026-06-20/21]** [picklescan の ML モデルスキャン機能が 3 手法でバイパス可能と判明 — CVE-2025-71351 (timeit.timeit() 内 reduce で RCE) / CVE-2025-71378 (cProfile.runctx() 内 reduce で RCE) / CVE-2026-56319 (logging.FileHandler → ゼロバイトファイル作成・ロック)、悪意ある pickle がスキャンをすり抜け PyTorch モデル配布パイプラインで RCE を実行可能](https://github.com/advisories/GHSA-fh2f-24rh-r2vq) *(GitHub Advisory Database)*

- **[2026-06-21]** [Crawl4AI (AI エージェント向け Web クローラー) に Docker API 認証バイパス CVE-2026-56265 (CVSS 9.3) — Docker API サーバーに JWT 署名鍵をハードコード → 攻撃者がトークン偽造で認証を回避、v0.8.7 で修正](https://github.com/advisories/GHSA-8qrg-7j2f-rf2h) *(GitHub GHSA-8qrg-7j2f-rf2h)*

## セキュリティ関連ニュース

- **[2026-06-21]** [Nintendo America が TinyPulse (WebMD 子会社) への侵害を正式確認 — Shadowbyt3$ が従業員サーベイデータ約 860MB (W-9・銀行明細・HR データ 2016-2026) を窃取; $2M 身代金要求を拒否; Nintendo 本体システムは未侵害](https://www.bleepingcomputer.com/news/security/nintendo-confirms-data-stolen-in-webmd-subsidiary-cyberattack/) *(BleepingComputer)*

- **[2026-06-20]** [新興ランサムウェアグループ Prinz Eugen が ThreatDown に詳報 — Go 製・非 RaaS・ランサムノートなし・ChaCha20-Poly1305+Argon2id 暗号化・最近変更ファイルを優先暗号化; RDP 窃取資格情報で侵入後 servertool.exe 手動実行+RMM ツール乱用; 少なくとも 5 組織 (South African Standard Bank 等) を標的](https://www.bleepingcomputer.com/news/security/new-prinz-eugen-ransomware-prioritizes-recent-files-for-encryption/) *(BleepingComputer / ThreatDown)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-20 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-56403〜56412 (GHSA 10 件) | libexpat < 2.8.2 | CWE-190 / **6.9** | `storeAtts` / `addBinding` / `copyString` / `XML_ParseBuffer` 等の長さチェック欠落 → 整数オーバーフロー → ヒープ破壊 → DoS/潜在 RCE | [libexpat PR #1255 他](https://github.com/libexpat/libexpat/pulls) (v2.8.2 未リリース、修正 PR 参照) | Python/Perl/Android 等に組み込まれた libexpat へ水平伝播リスク / 2026-06-20〜21 GHSA 一括公開 |
| GHSA-8qrg-7j2f-rf2h / CVE-2026-56265 | crawl4ai < 0.8.7 | CWE-798 / **9.3** | Docker API サーバーが JWT 署名鍵をハードコード → 攻撃者が任意トークン偽造 → 認証なしで API 保護機能を回避 | [crawl4ai 0.8.7](https://github.com/unclecode/crawl4ai) | AI エージェント向けクローラーで広く採用 / 隣接ツールのハードコード鍵パターンへバリアントハント推奨 |
| GHSA-pmm4-v8f6-4vpp / CVE-2026-56382 | craftcms/cms 5.5.0〜5.9.13 | CWE-94 / **8.6** | admin が `fieldLayoutConfig` POST パラメータ経由で Yii2 イベントハンドラを注入 → `cleanseConfig()` なしで `createLayout()` に渡される → 任意 PHP コード実行・DB 認証情報/暗号鍵漏洩 | [craftcms/cms 5.9.14](https://github.com/craftcms/cms/releases) | Yii2 採用の他 CMS へバリアントハント推奨 |
| GHSA-fh2f-24rh-r2vq / CVE-2025-71351 | picklescan < 0.0.25 | CWE-184 / **7.6** | `timeit.timeit()` を reduce フックに埋め込んだ悪意ある pickle → `pickle.load()` 時に RCE → picklescan のブロックリストが不完全で検出回避 | [picklescan 0.0.25](https://github.com/mmaitre314/picklescan) | PyTorch/HuggingFace モデル配布パイプラインのスキャン前提が崩壊 |
| GHSA-fcqg-3mwf-cfcf / CVE-2025-71378 + CVE-2026-56319 | picklescan < 0.0.25 / < 1.0.1 | CWE-184 / **7.6** | `cProfile.runctx()` / `logging.FileHandler` クラスのインスタンス化を reduce フックに埋め込み → 検出バイパス経由で RCE またはファイルシステム操作 | 同上 | ML モデルスキャナー全般へバリアントハント推奨 |

## 国内脆弱性・インシデント情報

> 直近2日間に該当する新規国内ニュースは確認できませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 30 ソース (Microsoft Security Blog, BleepingComputer, ThreatDown, The Register, THN, ESET WeLiveSecurity, HelpNetSecurity, SecurityAffairs, GBHackers, SecurityWeek, Cybernews, Fortune, AI Weekly, explainx.ai, Manifold Markets, Polymarket, GitHub Advisory Database (GHSA), OSV.dev, CISA KEV, SOCRadar, Krebs on Security, Rapid7, Horizon3.ai, watchTowr Labs, security-next.com, JVN, NVD)
- 採用件数: AI=5 / Security=2 / CVE=5行 / 国内=0
- AI 件数が目安 (8〜12) を下回った理由:
  - 採用窓 (2026-06-20〜22) は週末〜月曜にあたり、大手 AI ラボからの新規発表ペースが低調
  - Google DeepMind multi-agent ロードマップ・Claude Code Artifacts・MCP Okta 安定版 (いずれも 6/18 公開) は excluded_set 収録済み
  - White House AI EO (6/2)・OpenAI Daybreak (6/10)・G7 AI連合 (6/17) 等は採用期間外
- 除外理由内訳:
  - 古すぎ (公開日 < 2026-06-20):
    - AutoJack (6/18〜19 公開, 6/21 digest 掲載済み)
    - Apple usbliter8 BootROM (6/19 公開, 6/21 digest 掲載済み)
    - Anki GHSA-869j-r97x-hx2g (6/19 GHSA公開, 6/21 digest 掲載済み)
    - LangSmith GHSA-f4xh-w4cj-qxq8 (6/19 GHSA公開, 6/21 digest 掲載済み)
    - SurrealDB GHSA-cc8f-fcx3-gpjr (6/19 GHSA公開, 6/21 digest 掲載済み)
  - 重複 (excluded_set 直近 7 ダイジェスト 2026-06-15 〜 2026-06-21):
    - Splunk CVE-2026-20253 KEV / FortiBleed / NGINX CVEs / Node.js CVEs
    - Crawl4AI GHSA-r253-r9jw-qg44 (browser_config RCE, 6/20 digest 掲載済み) ← 本日採用の GHSA-8qrg-7j2f-rf2h (JWT ハードコード) とは別脆弱性
    - SpaceX/Cursor 買収 / Accenture/Dragos 買収 / GentleKiller / Telegram BGP
  - 日付不明/確認不可:
    - CVE-2026-56235 — Nuxt XSS と Flowise info disclosure で情報源間の帰属に矛盾があり除外
  - 取得失敗ソース (HTTP 403): BleepingComputer 個別記事 (スニペット補完), ThreatDown ブログ, Adversa AI, security-next.com, JVN 個別ページ, buildfastwithai.com, unrot.co, windowsreport.com, rankiteo.com, rescana.com, vulnerability.circl.lu, esecurityplanet.com — 複数独立媒体スニペットで内容・日付を補完

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-06-15 〜 2026-06-21) の全 CVE/GHSA/URL を除外済み。*
