# KEDA Daily Digest — 2026-09-26 (JST)

> 採用範囲: 公開日 2026-09-24 〜 2026-09-26
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

---

## AI ニュース

- [2026-09-24] **Google Gemini 3.8 Live with Live Avatar が GA** — 97言語対応のエンタープライズ向けリップシンクAIアバターが一般提供開始、US/EU エンドポイントで即時利用可能 *(Google Blog / Unite.AI / AndroidHeadlines)*
- [2026-09-24] **Google DeepMind が Gemini 4 の post-training フェーズ移行を公表** — Kavukcuoglu が The Information AI Agenda Summit で「結果に興奮しており可能な限り早く出荷する」と発言、リリース時期は未公表 *(9to5Google / Yahoo Finance / TechBriefly)*
- [2026-09-24] **Sakana AI が Jürgen Schmidhuber を Chief Scientific Advisor に採用、RSI Lab を設立** — LSTM 発明者による自己改善AI・再帰サイクル・物理AI・ワールドモデル研究を推進; 東京で定期勤務 *(Sakana AI Blog / The Decoder / Superpower Daily)*
- [2026-09-24] **Oregon 州が Executive Order 26-26 を発令** — 州 CIO にフロンティア AI のキルスイッチ実装可能性評価と第三者安全審査標準の 90 日以内策定を指示; 州政府 AI 調達に安全評価要件を追加 *(KTVZ / Hoodline / KQEN)*
- [2026-09-25] **White House/ONCD が英国 AI Security Institute への新モデル提供保留を OpenAI・Anthropic に要請** — Anthropic は Claude Mythos 5.1 を米国の Project Glasswing 限定に据え置き; UK AISI 局長は GPT-6 Astra は依然アクセス可と発言 *(QZ / Yahoo News / Benzinga / AI Weekly)*
- [2026-09-25] **Microsoft が Copilot をリブート、個人向け AI 競争から撤退** — 消費者版と職場版を統合し企業顧客向けに一本化; ChatGPT・Gemini・Meta Muse との個人向け競争を断念 *(Bloomberg)*
- [2026-09-25] **Anthropic が Claude Marketplace の開発者向けプラグイン提出ポータルを公開** — 有料プランの開発者がプラグインをディレクトリに申請・審査追跡・利用分析が可能に *(Anthropic / Unite.AI / Flowlines)*
- [2026-09-25] **Google が Gemini API に antigravity-preview-09-2026 ハーネスを追加** — Gemini 3.8 Flash 上でコーディングエージェント機能を AI Studio/Interactions API に提供; Google Labs が家族向けロジスティクスエージェント CC も発表 *(AI Weekly / The Neuron)*

---

## セキュリティニュース

- [2026-09-25] **CISA KEV に 4 件を同時追加** — WordPress CVE-2026-87902 (CVSS 9.2, RCE)、SharePoint CVE-2026-65660 (CVSS 8.8)、MikroTik RouterOS CVE-2026-67279 (CVSS 6.9)、Roundcube CVE-2026-48842 (CVSS 8.1); 連邦機関修正期限: 2026-09-28 *(CISA / WindowsForum / GuardianMSSP)*
- [2026-09-25] **WordPress CVE-2026-87902 — パッチ公開 2.5 時間後に野外悪用開始** — 4.7〜7.1.1 の全バージョンが対象; pagename パラメータ経由の PHP ファイルインクルード RCE; 7.1.2 への即時更新を推奨 *(Patchstack / THN / CyberKendra)*
- [2026-09-24] **ServiceNow AI Platform に未認証 SQL injection 等 5 件 (KB3159623)** — CVE-2026-13016 (CVSS 9.3, 未認証 SQL injection)・CVE-2026-86860 (CVSS 9.3, 未認証特権昇格) を含む; Yokohama/Zurich/Australia ブランチへ即時パッチ適用 *(THN / GBHackers / CyberPress)*
- [2026-09-25] **SharePoint CVE-2026-65660 が野外悪用中** — 認証済み低権限ユーザーが匿名配信バグとチェーンし暗号化ローダーをサーバーに設置; 当初 "spoofing" 分類が RCE に再分類 *(The Hacker News / WindowsForum)*
- [2026-09-25] **Pareto.com データ侵害 — 440,000 件のレコードが流出** *(BitSight / PrivacyGuides roundup)*

---

## 新規 CVE

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-13016 | ServiceNow AI Platform (Yokohama/Zurich/Australia, 2026.2.3 以前) | CWE-89 / CVSS 4.0: 9.3 | 未認証ユーザーがプラットフォームのクエリエンドポイントに細工リクエストを送信 → 入力をサニタイズせず SQL エンジンへ渡す → インスタンス全 DB データに対する任意 SELECT/UPDATE 実行 → 機密 IT/HR/ワークフローレコードの窃取・改ざん | [ServiceNow KB3159623 (2026-09-24)](https://support.servicenow.com/) | CVSS 9.3 / 未認証 SQL injection / ITSM 基盤の未認証クエリ API サニタイズ欠落パターン / Salesforce・Zendesk 等の水平バリアント候補 |
| CVE-2026-86860 | ServiceNow AI Platform (同上) | CWE-862 / CVSS 4.0: 9.3 | 未認証リモート攻撃者が認可チェックなしに内部インスタンスデータエンドポイントへ直接リクエスト → Missing Authorization でプラットフォームが意図外のデータを返却 → アクセス権限外のレコード取得・特権昇格 | [ServiceNow KB3159623 (2026-09-24)](https://support.servicenow.com/) | CVSS 9.3 / 未認証データ取得 + 特権昇格 / 同一 advisory 内 SQL injection との複合利用リスク |
| CVE-2026-87902 | WordPress Core 4.7.0〜7.1.1 | CWE-73 / CVSS 4.0: 9.2 | 未認証攻撃者が `?pagename=` パラメータにテーマ外の PHP ファイルパスを指定 → `get_page_template()` が `validate_file()` を適用せずテーマ外パスを解決 → サーバー読み取り可能な任意 .php をインクルード → テーマ・サーバー設定条件下で任意コード実行 | [WordPress 7.1.2 / 7.0.6 / 6.9.9 / 6.8.10 (2026-09-22)](https://wordpress.org/news/) | **CVSS 9.2 / KEV (2026-09-25) / 公開当日から野外悪用中** / テンプレート解決の pagename 入力検証欠落 / Drupal・Joomla 等他 CMS テンプレート解決パスへの水平バリアント候補 |
| CVE-2026-48842 | Roundcube Webmail 1.6.x < 1.6.19 / 1.7.x < 1.7.4 | CWE-89 / CVSS 8.1 | 未認証攻撃者が `virtuser_query` プラグインの LDAP クエリ構築関数にバックスラッシュシーケンスを含む細工入力を送信 → `preg_replace()` の正規表現エスケープがバックスラッシュで無効化 → SQL クエリに任意文字列が注入 → DB の認証情報・メールマッピングテーブルへの無制限アクセス | [Roundcube 1.6.19 / 1.7.4 (2026-09-06)](https://roundcube.net/) | **KEV (2026-09-25) / 野外悪用確認済** / pre-auth SQL injection / Horde・SquirrelMail 等他ウェブメールの LDAP マッピング実装への水平バリアント候補 |
| CVE-2026-15688 | Mitsubishi Electric GX Works3 全バージョン; Motion Control Setting 全バージョン | CWE-303 / CVSS 8.8 | ローカル攻撃者が製品実行中にプロセスメモリ内の認証検証ルーチンを書き換え → ブロックパスワード認証が常時成功を返すよう改ざん → 無効なパスワードでも認証が通過 → 制御プログラムの閲覧・改ざん・破壊・削除が可能 | [GX Works3 v1.096A (JVNVU#99700314 / ICSA-26-260-02, 2026-09-24)](https://jvn.jp/vu/JVNVU99700314/) | CVSS 8.8 / ICS/SCADA 認証メモリ書き換えバイパス / Siemens TIA Portal・OMRON Sysmac Studio 等他産業用プログラミングソフトの認証実装への水平バリアント候補 |
| CVE-2026-65660 | Microsoft SharePoint Server 2016 / 2019 / Subscription Edition | CWE-94 / CVSS 8.8 | 認証済み低権限ユーザーが ToolPane の Register ディレクティブに二重引用符をエスケープしないリクエストを送信 → SafeControls 型チェック通過後に追加ディレクティブが注入 → サーバーサイドでの任意コード実行 | [Microsoft August 11, 2026 Security Update](https://msrc.microsoft.com/update-guide/) | **KEV (2026-09-25) / 野外悪用中 / 認証済み→RCE チェーン** / ToolPane Register ディレクティブのクォーティング欠落 / Confluence・Liferay 等他エンタープライズ CMS の Register/Component 解析実装への水平バリアント候補 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|---|---|---|---|---|
| 2026-09-24 | CVE-2026-15688 / JVNVU#99700314 | 三菱電機 GX Works3・Motion Control Setting でプロセスメモリ改ざんによりブロックパスワード認証を回避し制御プログラムを改ざん可能 | CVSS 8.8 / 制御プログラムの改ざん・破壊・削除 | [JVN](https://jvn.jp/vu/JVNVU99700314/) |
| 2026-09-25 | JVN#21754394 | baserCMS プラグイン「BcAddonMigrator」が信頼できない制御領域からの機能取り込み (CWE-829) — 管理者権限で任意ファイルの読み取り・削除が可能 | CVSS 8.6 (v4.0) / 7.2 (v3.0) / ファイルシステムへの不正アクセス | [JVN#21754394](https://jvn.jp/en/jp/JVN21754394/) |

---

## Debug

- 巡回ソース数: 30+
- 採用件数: AI=8 / Security=5 / CVE=6 / 国内=2
- 除外理由内訳:
  - 採用窓外 (公開日 < 2026-09-24): Meta Muse Charm (Sep 23), ChatGPT voice agents (Sep 23), Claude Code cloud sessions (Sep 23), Anthropic-OpenEvidence (Sep 23), 22 countries AI declaration (Sep 21-22), US-China AI hotline (Sep 21), 26 state AGs letter (Sep 23), MemTensor supply chain (Sep 23), SonicWall SMA1000 (Sep 1), Ivanti EPMM CVE-2026-1281/1340 (Jan 2026), Chrome CVE-2026-85046 (Sep 4), Anthropic Threat Intelligence Report (Sep 10), Microsoft Patch Tuesday (Sep 8), SolarWinds CVE-2026-28324/28325 (Sep 22), MikroTik CVE-2026-67279 original publication (early Sep), Roundcube original patch (May 2026), SharePoint original patch (Aug 11)
  - 重複 (直近7日 digest 既報): Sep 23/24/25 digest の全掲載項目
- 取得失敗ソース (EGRESS_BLOCKED): cisa.gov, jvndb.jvn.jp, ivanti.com, cvebrief.com, bleepingcomputer.com, securityweek.com, nvd.nist.gov
