# KEDA Daily Digest — 2026-10-09 (JST)

> 採用範囲: 公開日 2026-10-07 〜 2026-10-09
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

LMCache (vLLM KV キャッシュレイヤー) に CVSS 9.8 の未パッチ RCE が 2 件同時公開された—ZeroMQ pickle deserialization (CVE-2026-105192) と `/run_script` 未認証実行 (CVE-2026-107204)—vLLM ベースの推論インフラを持つ組織は即時ネットワーク隔離が必要。Pydantic AI のローカル chat エンドポイントでも CSRF + DNS rebinding の 2 件 (CVE-2026-107295/107292) が公開されるなど、AI エージェントフレームワーク固有の攻撃面が 1 日で 4 CVE 増加した。国内では JPCERT/CC が API 悪用・Metabase SQLi (CVE-2026-72898 CVSS 10.0) を含む不正アクセス多発を受けて注意喚起 AT-2026-0030 を発出、大阪公立大学のランサムウェア攻撃でも約 500 サーバーが停止し最大 13 万人分の情報漏洩が懸念される。

---

## AI 関連ニュース

- **[2026-10-08]** [Pydantic AI ローカル chat エンドポイントに CSRF (CVE-2026-107295, CVSS 7.6) + DNS rebinding (CVE-2026-107292, CVSS 6.4) が同時公開 — 開発者が悪意あるサイトを訪問するだけで AI エージェントが任意ツールを実行](https://github.com/advisories/GHSA-h4xc-3qfq-jf93) — CSRF: loopback bind でも防げない; DNS rebinding: Host ヘッダ無検証; 修正版 1.107.4 / 2.28.0 へ即時更新必須 *(GitHub Advisory Database / VulDB / Strix.ai)*

- **[2026-10-07]** [LMCache CVE-2026-105192 (CVSS 9.8): JFrog が ZeroMQ ソケット上の pickle deserialization RCE を公開、**現時点でパッチなし / PoC 公開済み**](https://gbhackers.com/critical-lmcache-rce-vulnerability/) — port 5555 認証なし ZeroMQ に任意 pickle データを送信 → 任意クラスをインスタンス化 → root コンテナでシステム完全侵害; 影響範囲 0.3.9〜0.5.5; デフォルト localhost だが `--host` 設定時は外部から到達可能 *(JFrog / GBHackers / Forkast / ByteIOTA)*

- **[2026-10-08]** [LMCache CVE-2026-107204 (CVSS 9.8): `/run_script` エンドポイントへ未認証 POST で Python コードが実行](https://www.thehackerwire.com/cve-2026-107204-critical-lmcache-rce-exposes-systems-to-unauthenticated-python-code-execution/) — FastAPI アプリオブジェクト経由で `__builtins__` を復元・サンドボックス脱出 → `import os` で OS コマンド実行; ≤ 0.5.5 が対象; **修正なし** (GitHub Issue #5510 追跡中) *(The Hacker Wire / Strix.ai)*

- **[2026-10-07]** [Anthropic CEO Dario Amodei が Fox News ライブブログで「先端 AI モデルをさらに多くのセキュリティチームに提供する」と発言 — Cyber Verification Program 発足後 1 週間で 129,000 件超の脆弱性発見と公表](https://foxnews.com/live-news/open-ai-anthropic-us-tech-security-october-7) — JPMorgan Dimon は同日「Mythos 公開後に AI サイバーリスクが劇的に増大した」と発言; AI 力の非対称拡大が金融セクターに波及 *(Fox News)*

- **[2026-10-08]** [OpenAI、内部モデルによる未解決数学問題 ~5% 解答実験を公表 — 約 8,000 問・1 問あたり約 3 時間計算; 数学者は「自然言語形式の解説品質が不十分」と批判](https://foxnews.com/live-news/open-ai-anthropic-us-tech-security-october-7) — 形式的証明でなく自然言語出力; AGI 到達指標としての数学ベンチマーク活用の限界と妥当な測定基準について議論が活発化 *(Fox News / AI Weekly)*

- **[2026-10-07]** [India Mobile Congress 2026 (Oct 7-9, New Delhi) 開幕 — Fortinet India 代表が「AI for security, security for AI が 2026 年最大のサイバー戦場」と発言、インド企業の AI 攻撃対策需要が急増](https://www.business-standard.com/technology/tech-news/imc-2026-ai-for-security-security-for-ai-becomes-new-cyber-battleground-126100800968_1.html) — deepfake ソーシャルエンジニアリング・AI 支援フィッシングへの対策が最優先課題として浮上 *(Business Standard)*

- **[2026-10-08]** [GitHub Advisory DB が Excelize (Go スプレッドシートライブラリ) の DoS 2 件を公開: CVE-2026-107212 (行反復無限ループ) + CVE-2026-107213 (`GetSlicers` nil pointer panic)](https://github.com/advisories) — Go 製バックエンドの Excel ファイル処理パイプライン全般に影響; xlsxwriter (Python) ・Apache POI 等他実装への水平バリアント候補 *(GitHub Advisory Database)*

---

## セキュリティ関連ニュース

- **[2026-10-08]** [JPCERT/CC JPCERT-AT-2026-0030 発出: 国内組織への不正アクセス多発 — スマートフォンアプリ解析による API キー抽出・バックアップファイル窃取・Metabase CVE-2026-72898 SQLi (CVSS 10.0) の 3 攻撃手法を実例付きで解説](https://www.jpcert.or.jp/at/2026/at260030.html) — 既知脆弱性への未パッチ公開が主因; 対策として不要な管理インタフェースのインターネット遮断・定期的なアップデート適用を推奨 *(JPCERT/CC / Impress Watch / MyNavi Tech+)*

- **[2026-10-07]** [大阪公立大学 (OMU) にランサムウェア攻撃 — 約 500 サーバーおよびバックアップが同時暗号化・最大 13 万人分の学生・教職員情報の漏洩懸念](https://therecord.media/osaka-university-cancels-classes-ransomware) — Oct 2 発生; 授業・図書館・給与・人事システム全停止; バックアップも標的にする「二重ロック」戦術が国内大学でも観測 *(The Record / Hendryadrian)*

- **[2026-10-08]** [Oracle Health (旧 Cerner) 2025 年侵害の規模判明: テキサス AG 申告書で **約 2,000 万人分** の社会保障番号・住所・医療情報の漏洩を開示 — Oracle は当初「クラウド侵害ではない」と否定し内部通知に留めていた](https://www.techzine.eu/news/security/144761/oracle-medical-data-breach-affected-nearly-20-million-people/) — 攻撃者はランサムとして医療機関に直接要求; Cerner 移行未完了の legacy server が侵害経路 *(Bloomberg / TechZine / DrWeb.de)*

- **[2026-10-08]** [MonsterCloud (米) 経営者を連邦起訴: ランサムウェア被害企業から「専門復号ツール費用」として $11M 超を詐取 — 実際には攻撃者にランサムを支払い差額を請求する詐欺スキーム](https://securityweek.com/fake-decryption-tools-masked-11m-markup-in-ransomware-recovery-scheme) — 被害企業は「ランサムウェア専門業者」として全信頼を置いていた; インシデントレスポンス業者のベッティングが課題として浮上 *(SecurityWeek)*

- **[2026-10-07]** [SafePay ランサムウェアグループが T-Systems (ドイツ大手通信 IT) への侵害を主張 — データ公開を脅迫; T-Systems は調査中と発表](https://konbriefing.com/en-topics/cyber-attacks.html) — SafePay は近年欧州大企業・重要インフラへの攻撃を拡大; ドイツ政府・産業インフラへの潜在的波及が懸念される *(Konbriefing)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 today-2 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-105192 | LMCache (pip) 0.3.9〜0.5.5 (multiprocess mode / `--host` routable 設定時) | CWE-502 / 9.8 | 認証なし ZeroMQ ソケット (port 5555) が pickle データを無検証でデシリアライズ → 攻撃者制御の任意クラスをインスタンス化 → root コンテナでは全システム侵害 | [JFrog advisory / GBHackers PoC (2026-10-07)](https://gbhackers.com/critical-lmcache-rce-vulnerability/) (**パッチなし / PoC 公開**) | **CVSS 9.8 / PoC 公開 / vLLM+LMCache スタック全体影響** / LMDeploy・TensorRT-LLM・SGLang 等 ZeroMQ KV キャッシュ実装への水平バリアント候補 |
| CVE-2026-107204 | LMCache (pip) ≤ 0.5.5 | CWE-306 / 9.8 | `/run_script` エンドポイントが認証なしで受け付けた Python 文字列を exec → FastAPI アプリオブジェクト経由で `__builtins__` を復元しサンドボックス脱出 → `import os` で OS コマンド実行 | [GitHub Issue #5510 (2026-10-08)](https://www.thehackerwire.com/cve-2026-107204-critical-lmcache-rce-exposes-systems-to-unauthenticated-python-code-execution/) (**パッチなし**) | **CVSS 9.8 / 未認証 / AI 推論 API に `/run_script` 系エンドポイントを持つ実装全般** |
| CVE-2026-107295 | pydantic-ai / pydantic-ai-slim 1.34.0〜1.107.3, 2.0.0b1〜2.27.x | CWE-352 / 7.6 | 開発者が悪意サイトを訪問 → ブラウザが loopback chat エンドポイントへブラウザ互換 CSRF リクエストを送信 (localhost bind では防げない) → エージェントが credentials・ファイルシステム・MCP ツールを含む任意ツールをローカル権限で実行 | [GHSA-h4xc-3qfq-jf93 / 修正: 1.107.4 または 2.28.0 (2026-10-08)](https://github.com/advisories/GHSA-h4xc-3qfq-jf93) | **AI エージェント開発ツール全般 / ローカルポートをリスンする LangGraph・AutoGen 等フレームワークへの水平バリアント候補** |
| CVE-2026-107292 | pydantic-ai / pydantic-ai-slim 1.34.0〜1.107.3, 2.0.0b1〜2.27.x | CWE-350 / 6.4 | chat エンドポイントが `Host` ヘッダを検証しない → DNS rebinding で外部サイトが loopback アドレスに bind し SOP を回避 → エージェントをリモート操作可能 | [同 GHSA / 修正: 1.107.4 または 2.28.0 (2026-10-08)](https://github.com/advisories/) | **DNS rebinding / ローカル chat UI をリスンする全 AI フレームワーク** / Ollama・LM Studio 等ローカル LLM UI サーバーへの水平バリアント候補 |
| CVE-2026-107212 | Excelize (Go) `github.com/xuri/excelize/v2` < 修正版 | CWE-835 / 高 | `SetRowHeight` に `math.MaxInt32` 等の無制限行番号を渡す → 行反復処理が無限ループ → CPU 枯渇・DoS | [GHSA (2026-10-08)](https://github.com/advisories) (commit 不明) | **Go 製 Excel 処理バックエンド / Python xlrd・xlsxwriter、Java Apache POI 等他言語実装への水平バリアント候補** |
| CVE-2026-107213 | Excelize (Go) < 修正版 | CWE-476 / 高 | `GetSlicers` がスライサー設定なしシートに対し nil ポインタを返す → 呼び出し元がデリファレンスして panic → DoS | [同 GHSA (2026-10-08)](https://github.com/advisories) (commit 不明) | **Go Excel ライブラリ全採用サービス** |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-10-08 | JPCERT-AT-2026-0030 | 国内組織で API 悪用・バックアップ窃取・Metabase CVE-2026-72898 SQLi (CVSS 10.0) による不正アクセスが多発; JPCERT/CC が 3 手法を実例付きで解説 | 多組織 / 情報漏洩 | [JPCERT/CC](https://www.jpcert.or.jp/at/2026/at260030.html) |
| 2026-10-07 | 大阪公立大学 (OMU) | ランサムウェアで約 500 サーバー・バックアップ同時暗号化、最大 13 万人分の学生・教職員情報漏洩の疑い (Oct 2 発生) | 大規模 / 授業停止 | [The Record](https://therecord.media/osaka-university-cancels-classes-ransomware) |
| 2026-10-07 | JVN 公開 / Movable Type | Movable Type に複数の脆弱性 — 詳細は JVN サイト参照 | 調査中 | [JVN](https://jvn.jp/) |
| 2026-10-07 | CVE-2026-82918 / JVNDB-2026-031532 | キーエンス XG/XG-X VisionTerminal ≤ 3.6.0000 に XXE — 細工した設定ファイルで機密情報漏洩 | CVSS 5.5 / 情報漏洩 | [JVNDB](https://jvndb.jvn.jp/en/contents/2026/JVNDB-2026-031532.html) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 採用ウィンドウ: 2026-10-07 〜 2026-10-09 (JST)
- 巡回ソース数: 30+
- 採用件数: AI=7 / Security=5 / CVE=6 / 国内=4
- 除外理由内訳:
  - 採用窓外 (公開日 < 2026-10-07):
    - PraisonAI CVE-2026-60090 (Jul 11, 2026 公開) — 窓外
    - OsmAnd CVE-2026-65995/65996/65997 (Oct 1, 2026 GitHub Security Lab 公開) — 窓外
    - LMDeploy CVE-2026-76850 (Aug 19, 2026 公開) — 窓外
    - JFrog Artifactory CVE-2026-69105/69106 (Aug 12, 2026 公開) — 窓外
    - Microsoft Patch Tuesday Oct 2026 (Oct 13 予定・未公開)
    - AI brand phishing Microsoft report (Jun 8, 2026 公開) — 窓外
    - Advantest データ漏洩 (Oct 6 通知) — 窓外 (境界)
    - Osaka Metropolitan University 攻撃発生日 (Oct 2) — 発生は窓外だが Oct 7 以降報道が広まったため国内セクションに採用
  - 重複 (直近7日 digest 既報):
    - CVE-2026-21589 Atlassian (Oct 7 digest 既報)
    - CVE-2026-96940 Microsoft Exchange (Oct 8 digest 既報)
    - CVE-2026-41510/41508/41504 Coraza WAF (Oct 8 digest 既報)
    - CVE-2026-105851 Payload CMS (Oct 8 digest 既報)
    - CVE-2026-104850 MCP TypeScript SDK (Oct 8 digest 既報)
    - CVE-2026-104286 FortiMail (既報複数回)
    - CVE-2026-88779 Citrix NetScaler (Oct 6 digest 既報)
    - CVE-2026-61500 Rejetto HFS (Oct 6 digest 既報)
    - CVE-2026-43682 macOS kernel (Oct 6 digest 既報)
    - CVE-2026-105752/105753 vLLM (Oct 7 digest 既報)
    - CVE-2026-96749/96748 PyMongo (Oct 7 digest 既報)
    - Pwn2Own Ireland Days 1 & 2 (Oct 7 & 8 digests 既報)
    - Artex AI 韓国金融機関攻撃 (Oct 7 digest 既報)
    - ATB Ukraine DataSuckers (Oct 7 digest 既報)
    - Azazel ランサムウェア AI 悪用 (Oct 8 digest 既報)
    - NCC Group ランサムウェア Aug 最多記録 (Oct 8 digest 既報)
    - Anthropic Cyber Verification Program 再編 (Oct 8 digest 既報)
    - Mistral Large 4 "le Chonk" (Oct 8 digest 既報)
  - 日付不明・確認不可:
    - OpenAI GPT-6 Oct 8 ロールアウト — 複数ソースで矛盾 (GPT-5.6 が最新; GPT-6 未発表との説が有力); 除外
    - Claude Haiku 5.5 Oct 8 リリース — Sep 28「coming weeks」予告のみで Oct 8 リリース確認できず; 除外
    - FortiBleed FBI/Secret Service 注意喚起 — Oct 7 付与否を確認できず除外
    - LMCache CVE-2026-105192 JFrog 一次 advisory URL — 直接 fetch 不可; GBHackers/Forkast/ByteIOTA 複数二次ソースで採用
    - Oracle Health 20M 漏洩の Bloomberg 報道正確日付 — "early October 2026" 確認のみ; Oct 7 前後と推定し採用
    - Pwn2Own Ireland Day 3 (Oct 8) 結果 — ZDI ブログ投稿を確認できず除外
  - 取得失敗ソース: github.com/advisories (直接 fetch), nvd.nist.gov, jvn.jp, jpcert.or.jp (本文), zerodayinitiative.com/blog, bleepingcomputer.com, thehackernews.com, securityweek.com (直接), anthropic.com/news

</details>
