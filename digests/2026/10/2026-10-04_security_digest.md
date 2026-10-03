# KEDA Daily Digest — 2026-10-04 (JST)

> 採用範囲: 公開日 2026-10-02 〜 2026-10-04
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

GitLab AI Gateway に CVSS 9.9 の Jinja2 テンプレートインジェクション (CVE-2026-90970) が 10/2 公開。自己ホスト型 AI エージェントプラットフォームへの RCE は即時パッチ適用が必要。Bouncy Castle for Java が X.509 名前制約バイパス・OpenPGP 完全性チェック欠落を含む複数 CVE バッチを 10/3 に公開し、Java ベースの幅広いアプリケーションへの影響評価が求められる。攻撃面では ChatGPT Custom GPT を C2 として悪用する ClickFix RAT キャンペーンが Huntress により 40 件超のインシデントとして確認され、AI 信頼ドメインの悪用が新たな感染ベクターとして定着しつつある。

## AI 関連ニュース

- **[2026-10-02]** [CVE-2026-90970: GitLab AI Gateway に CVSS 9.9 の Jinja2 テンプレートインジェクション公開 — 認証済み Duo Agent Platform ユーザーがサンドボックス脱出 → ホスト OS 任意コード実行](https://securityaffairs.com/200283/hacking/cve-2026-90970-critical-gitlab-ai-gateway-flaw-fixed.html) — Duo Workflow Service がフロー定義の入力を適切に中立化しないため、細工されたテンプレートでホスト OS コマンドを実行可能。修正版: AI Gateway 19.2.4/19.3.2/19.4.1 *(SecurityAffairs / GBHackers / forkast.news)*

- **[2026-10-02]** [Huntress: 悪意ある ChatGPT Custom GPT を C2 として悪用する ClickFix RAT 配布キャンペーンで 40 件超インシデント確認](https://www.huntress.com/blog/chatgpt-custom-gpts-clickfix-rat) — 攻撃者が chatgpt.com 上に悪意ある Custom GPT を公開 → Google 検索スポンサー広告で誘引 → Google Sites ClickFix ページ → PowerShell 実行 → RDP/音声・映像キャプチャ機能付き RAT インストール。OpenAI は 9/25 に第一の悪意 GPT を削除 *(Huntress / SecurityWeek / CryptoBriefing)*

- **[2026-10-02]** [ClickFix 攻撃急増 (前年比 517%): 偽 ChatGPT インストーラーが infostealer + 権限昇格ツールを配布](https://www.scworld.com/news/clickfix-attack-surge-fake-chatgpt-installers-steal-passwords) — Google 検索広告上の偽 ChatGPT Atlas インストーラーが標的にコマンドプロンプトへの貼り付け実行を誘導; パスワード反復要求で認証情報窃取後に管理者権限昇格 *(SC World / SecurityWeek)*

- **[2026-10-02]** [OpenAI、GPT-6.1 Sol 初期対応の遅延を謝罪 — 全有料 ChatGPT ユーザーの月次使用量を太平洋時間 10/2 午前 10 時にリセット](https://x.com/NeoAIForecast/article/2105966638927397167) — ChatGPT 製品責任者 Thibault Sottiaux がグローバルリセット実施を発表。GPT-6.1 Sol 展開時のキャパシティ逼迫への補償措置 *(NeoAIForecast / Daily AI Recap)*

- **[2026-10-03]** [OpenAM バッチ脆弱性公開 — 認証不要クラスインスタンス化 CVE-2026-105115 (CVSS 8.8) / PKCE 強制バイパス CVE-2026-105119 (High) / SSRF CVE-2026-105122 等 10 件超](https://github.com/advisories?query=published%3A2026-10-03+OpenAM) — AI・LLM システムが OAuth/OIDC 認証基盤として広く使用する OpenAM の認証バイパス脆弱性群。修正版: OpenAM 16.1.3 *(GitHub Advisory Database)*

- **[2026-10-03]** [Bouncy Castle for Java に X.509 名前制約バイパス (CVE-2026-71889, CVSS 8.7) および OpenPGP 完全性チェック欠落 (CVE-2026-85515, CVSS 8.2) を含む複数 CVE バッチ公開](https://github.com/bcgit/bc-java/wiki/CVE%E2%80%902026%E2%80%9085515) — Java ベースの AI/ML パイプラインや API ゲートウェイで広く使用される暗号ライブラリ。修正版: BC 1.86 / LTS 2.73.13 *(GitHub Advisory Database)*

- **[2026-10-03]** [NASA-AMMOS AIT-Core (宇宙機テレメトリ C2 サーバー) に CVSS 9.8 の認証不要 CVE-2026-105105 — ZeroMQ バスが無認証公開 → 任意宇宙機コマンド注入・テレメトリ窃取可能](https://github.com/advisories/GHSA-9xfm-37f4-2h8g) — TCP 5559/5560 番ポートへのネットワーク到達が条件のみで特権不要。修正版 3.1.2 でデフォルトバインドをループバックに変更 *(GHSA-9xfm-37f4-2h8g)*

## セキュリティ関連ニュース

- **[2026-10-02]** [Storm-2603 (中国系) が SharePoint 0-day (CVE-2025-49706/49704) 悪用を継続 — スペイン・ポルトガル語圏の政府・重要インフラ・教育機関が新たな標的に](https://www.scworld.com/news/microsoft-china-backed-storm-2603-deploys-warlock-ransomware-on-sharepoint-servers) — 7 月以来 400 件超の被害組織; GPO 変更で Warlock ランサムウェアを展開; スペイン語・ポルトガル語圏で被害拡大継続。未パッチの On-Premises SharePoint 機器に注意 *(SC World / The Record)*

- **[2026-10-02]** [GitLab AI Gateway CVE-2026-90970 緊急パッチ — 自己ホスト型 GitLab Enterprise は AI Gateway 19.2.4/19.3.2/19.4.1 に即時アップデート必須](https://gbhackers.com/critical-gitlab-ai-gateway-flaw/) — 管理対象サービス (GitLab.com) は既にパッチ済み。攻撃者に必要なのは有効なユーザーアカウントのみ。フィッシング・漏洩済み開発者認証情報でのエクスプロイトが現実的なシナリオ *(GBHackers / SecurityAffairs)*

- **[2026-10-02]** [Microsoft SQL Server をシェルコマンド実行チャンネルに悪用した Viva Aerobus 侵害事案 — MSSQL ストアドプロシージャ経由でコマンド実行・ファイル収集→外部転送](https://www.securityweek.com/) — LOTL (Living-Off-The-Land) 手法の典型。xp_cmdshell 有効化に要注意 *(SecurityWeek)*

- **[2026-10-03]** [OpenAM JAX-RPC SOAP 認証不要クラスインスタンス化 CVE-2026-105115 — `/jaxrpc/*` エンドポイントがプリオーセンティケーション段階で任意 Java クラスを反射インスタンス化 → ガジェットチェーン経由 RCE 可能性](https://github.com/advisories/GHSA-45wm-hvw4-223f) — IAM/SSO 基盤への攻撃は多数のサービスへのラテラルムーブに直結。OpenAM 16.1.3 で修正 *(GitHub GHSA-45wm-hvw4-223f)*

- **[2026-10-03]** [Bouncy Castle for Java PKIXCertPathReviewer X.509 名前制約バイパス CVE-2026-71889 — `checkNameConstraints()` のループ境界バグで末端エンティティ証明書の制約スキップ → 制約違反の証明書チェーンを正当と判定 → TLS・S/MIME 等で偽装証明書受理](https://github.com/bcgit/bc-java/commit/06dcff2f51037095de126986285c998e3455ab85) — BC 1.86/LTS 2.73.13/FIPS 最新版で修正 *(GitHub Advisory Database)*

- **[2026-10-03]** [Bouncy Castle OpenPGP 完全性チェック欠落 CVE-2026-85515 — SEIPD v1 の truncated 暗号文をエラー報告なしで受理 → 署名・認証なしで改ざん平文を正規メッセージとして配信](https://github.com/bcgit/bc-java/wiki/CVE%E2%80%902026%E2%80%9085515) — AEAD 経路でも完全性バイパス可能 (LTS のみ)。BC 1.86 で修正 *(GitHub Advisory Database)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-10-02 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-90970 | GitLab AI Gateway 18.1.6〜19.1.x | CWE-1336 / 9.9 | Duo Workflow Service がユーザー供給フロー定義の Jinja2 テンプレートプレースホルダーを適切に中立化しない → テンプレートエンジンサンドボックス脱出 → ホスト OS 上で認証済みユーザー権限で任意コマンド実行 | [GitLab AI Gateway 19.4.1 patch](https://about.gitlab.com/releases/2026/10/02/patch-release-gitlab-ai-gateway-19-4-1-released/) (commit 不明) | **CVSS 9.9** / セルフホスト GitLab Enterprise 全対象 / LangChain・AutoGen・Dify 等 Jinja2 使用 AI エージェントフレームワーク全般への水平バリアント候補 |
| GHSA-9xfm-37f4-2h8g / CVE-2026-105105 | NASA-AMMOS AIT-Core ≤ 3.1.1 | CWE-306 / 9.8 | ZeroMQ メッセージバス (TCP 5559/5560) が認証なしで外部公開 → ネットワーク到達可能な未認証攻撃者が任意の宇宙機コマンドを注入またはテレメトリデータを窃取・改ざん | [AIT-Core 3.1.2](https://github.com/NASA-AMMOS/AIT-Core) (commit 不明) | **CVSS 9.8** / ZeroMQ pub/sub バスの認証実装漏れ / 宇宙・産業 OT 系の他テレメトリシステムへの水平バリアント候補 |
| GHSA-45wm-hvw4-223f / CVE-2026-105115 | OpenAM < 16.1.3 | CWE-470 / 8.8 | 認証不要の攻撃者が legacy JAX-RPC SOAP `/jaxrpc/*` エンドポイントにセッション検証なしで任意クラス名を送信 → サーバが型検査なしにクラスをインスタンス化 → ガジェットチェーン経由 RCE またはサービス停止 | [OpenAM 16.1.3](https://github.com/openidentityplatform/openam/releases/tag/16.1.3) (commit 不明) | **CVSS 8.8** / IAM 基盤の認証前 Unsafe Reflection / Apache CXF・JAX-WS 等他 SOAP/RPC 実装の廃止予定エンドポイントへの水平バリアント候補 |
| GHSA-hqqj-v58h-gr7x / CVE-2026-71889 | Bouncy Castle for Java < 1.86 (LTS < 2.73.13, FIPS bcpkix-fips < 1.0.13/2.0.13/2.1.13) | CWE-295 / 8.7 | `PKIXCertPathReviewer.checkNameConstraints()` のループ境界バグで末端エンティティ証明書を名前制約検証からスキップ → 制約違反 (SAN/DN) の証明書チェーンが正当と判定 → TLS・S/MIME・コード署名検証における偽装証明書受理 | [bc-java@06dcff2f](https://github.com/bcgit/bc-java/commit/06dcff2f51037095de126986285c998e3455ab85) | **CVSS 8.7** / Bouncy Castle 広範使用 / BouncyCastle.NET・SpongyCastle・bcpkix-fips 等派生実装への水平バリアント候補 |
| GHSA-8hgf-w73g-3x6v / CVE-2026-85515 | Bouncy Castle for Java < 1.86 (LTS < 2.73.13, BC-FJA < bcpg-fips 1.0.14/2.0.14.1/2.1.14) | CWE-354 / 8.2 | SEIPD v1 truncated OpenPGP 暗号文を完全性検証エラー報告なしで受理 → 暗号化・署名済みと見なして平文を呼び出し元に返却 → 改ざんメッセージが未検知で通過 | [bc-java@ab7a235](https://github.com/bcgit/bc-java/commit/ab7a235) | **CVSS 8.2** / OpenPGP 完全性バイパス / GnuPG・libgcrypt・OpenPGP.js 等他 OpenPGP 実装への水平バリアント候補 |

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|

> 直近2日間に該当する新規ニュースは確認できませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 25+
- 採用件数: AI=7 / Security=6 / CVE=5 / 国内=0
- 除外理由内訳:
  - 採用窓外 (公開日 < 2026-10-02):
    - CVE-2026-21858 n8n Ni8mare (公開 2026-01-07) — 窓外; 10月に活発な悪用確認も CVE 自体は古い
    - ChatGPT Custom GPT ClickFix Huntress 一次報告 (2026-09-29) — 窓外; Oct 2 以降の追加報道 (SC World, SecurityWeek) として採用
    - SAFA (Standards Authority for Frontier AI) 設立進捗 (2026-09-24) — 窓外かつ Oct 1 digest 既報
    - CVE-2026-9862/9863 Fortra BoKS (2026-06 公開) — 窓外
    - CVE-2026-40710/40711 Dell CSM (2026-05-28) — 窓外
    - CVE-2025-49706/49704 Microsoft SharePoint (2025-07) — 窓外 (Storm-2603 の継続攻撃はセキュリティニュースとして採用)
    - Google Project Suncatcher 軌道投入確認 (2026-10-01) — today-2 = 10-02 のため窓外
    - California AG Bonta OpenAI Hugging Face 捜査開始 (2026-09 報道) — 窓外
  - 重複 (直近7日 digest 既報):
    - CVE-2026-92948 vm2 (Oct 3 digest 既報)
    - CVE-2026-104286 Fortinet FortiMail KEV (Oct 3 digest 既報)
    - Microsoft Digital Defense Report 2026 (Oct 3 digest 既報)
    - OpenAI 安全研究者 3 名解雇 (Oct 3 digest 既報)
    - アサヒグループ Qilin ランサムウェア (Oct 3 digest 既報)
    - CVE-2026-76504 Cisco SD-WAN (Oct 2 digest 既報)
    - CVE-2026-92937/40/57 vm2 バッチ (Oct 2 digest 既報)
    - 能動的サイバー防衛法施行 (Oct 2 digest 既報)
    - OpenAI Moonshot AI (Kimi) 推論抽出 (Oct 2 digest 既報)
    - SC WordPress backdoor (Oct 2 digest 既報)
    - FTC AI エージェントリスク捜査 (Oct 1 digest 既報)
    - Apple CVE-2026-86950 (Sep 30 digest 既報)
    - PAN-OS CVE-2026-0257 (Oct 1 digest 既報)
    - Citrix NetScaler CVE-2026-88771/88772 (Oct 1 digest 既報)
    - 京王電鉄ランサムウェア (Oct 1 digest 既報)
    - PixelLeak AI コーディングエージェント screenshot 漏洩 (Oct 1 digest 既報)
  - 日付不明・確認不可:
    - Apache OpenOffice October 2 CVE バッチ — CVE-2026-59265 の NVD エントリが未確認; CVE 番号が AI 生成スニペットの誤りである可能性があり除外
    - Zammad CVE-2026-102489/102490 CISA KEV — CVE 番号の NVD エントリが確認できず; CISA KEV 初回検索結果のみに登場のため信頼性不十分で除外
    - CVE-2026-92084 Beaver Builder WordPress — 詳細確認できず低優先度で除外
  - その他除外:
    - Warlock SharePoint: 根本 CVE が 2025-07; October 2-4 での新規被害報告としてセキュリティニュース採用、CVE セクションでは除外
    - n8n Ni8mare: 窓外で除外; 10 月の活発悪用状況は <details> 内に記録
- 取得失敗ソース (EGRESS_BLOCKED): thehackernews.com (本文直接), bleepingcomputer.com, orca.security, securityaffairs.com, securityboulevard.com, helpnetsecurity.com, gbhackers.com, forkast.news, thecybersecguru.com, purple-ops.io, securityonline.info, about.gitlab.com, www.cisa.gov, www.dell.com, aiweekly.co, dev.to, www.cyber.gc.ca, strix.ai, rapid7.com (本文直接)

</details>
