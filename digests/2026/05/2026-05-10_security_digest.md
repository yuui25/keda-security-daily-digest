# KEDA Daily Digest — 2026-05-10 (JST)

> 採用範囲: 公開日 2026-05-08 〜 2026-05-10
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

---

## AI 関連ニュース

### OpenAI、音声 AI モデル 3 種を API 公開 — GPT-5 クラス推論で音声エージェントを刷新

- **公開日**: 2026-05-07 (発表) / 2026-05-08 (詳細解説)
- **ソース**: Dataconomy / TechCrunch
- **要約**:
  - OpenAI が `GPT-Realtime-2`・`GPT-Realtime-Translate`・`GPT-Realtime-Whisper` の 3 モデルを API 公開。`GPT-Realtime-2` は GPT-5 クラスの推論能力を音声会話に持ち込み、コンテキストウィンドウは 32K → 128K トークンに拡張。
  - 音声エージェントがツール呼び出し・文脈保持・訂正対応など「実用レベル」に到達したことを示す転換点。顧客サポート・医療・不動産・翻訳など多業種での採用が進む。
  - 開発組織は音声 AI インフラのセキュリティ評価（認証・ログ・入力検証）を急ぎ整備すべき段階に入った。GPT-Realtime-2 は音声経由のプロンプトインジェクション攻撃の新たな対象面となる。
- **リンク**: <https://dataconomy.com/2026/05/08/gpt-realtime-2-expands-openais-voice-intelligence-capabilities/>

---

### Microsoft Semantic Kernel: プロンプトインジェクション → RCE 脆弱性 (CVE-2026-25592 / CVE-2026-26030)

- **公開日**: 2026-05-07
- **ソース**: Microsoft Security Blog
- **要約**:
  - Microsoft が Semantic Kernel エージェントフレームワークに 2 件の脆弱性を公開。`CVE-2026-25592`（.NET SDK < 1.71.0）は `DownloadFileAsync` がモデルに誤公開されホストへの任意ファイル書き込みが可能。`CVE-2026-26030`（Python < 1.39.4）は `InMemoryVectorStore` のフィルタが `eval()` で評価されリモートコード実行につながる。
  - いずれも敵対的プロンプトによって引き起こされる「プロンプトインジェクション → コード実行」の典型パターン。AI エージェントがツール実行権限を持つ環境では影響が深刻。
  - 対応: 各 SDK を最新版へ更新し、エージェントに付与するツール権限の最小化・実行サンドボックス隔離を徹底すること。
- **リンク**: <https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/>

---

### FastGPT MCPツール URL に SSRF 脆弱性 (CVE-2026-44284) — AI エージェント基盤の入力検証不備

- **公開日**: 2026-05-08
- **ソース**: GitHub Security Advisory / TheHackerWire
- **要約**:
  - AI エージェント構築プラットフォーム FastGPT (< 4.14.17) の MCP ツール作成・更新エンドポイントで、内部ネットワーク URL のブロックが欠落していた。プレビュー/実行エンドポイントは保護されているが、ツール登録時に `http://localhost:3000/mcp` 等の内部 URL を保存できてしまい、バックエンドのワークフローランナーが内部サービスに接続させられる。
  - MCP ツールを介した SSRF は AI エージェント基盤特有のリスクで、既存の SSRF 対策の適用漏れが生じやすい設計パターン。CVSS 6.3 (Medium) だが認証済み攻撃者が内部インフラへのピボットに悪用できる。
  - FastGPT を自己ホストしている組織は 4.14.17 へ即座にアップグレードし、MCP ツール登録時の URL 検証ロジックを確認すること。
- **リンク**: <https://github.com/labring/FastGPT/security/advisories/GHSA-cxxj-99f7-f5wq>

---

### Oracle、Claude Mythos と OpenAI モデルを活用した脆弱性検知を強化 — 月次 CSPU を 5 月 28 日より開始

- **公開日**: 2026-05-05〜2026-05-08
- **ソース**: Oracle Security Blog / SecurityWeek
- **要約**:
  - Oracle が Anthropic Claude Mythos Preview と OpenAI の最新モデルを「Trusted Access for Cyber」経由で活用し、AI によるコード分析・脆弱性検出・テストを大幅に拡充していると発表。従来の四半期パッチ (CPU) に加え、月次 Critical Security Patch Update (CSPU) を 2026-05-28 より提供開始。
  - AI による脆弱性発見の加速（Mandiant: 28.3% の CVE が公開 24 時間以内に悪用）を受け、パッチ提供サイクルを短縮した戦略的対応。Oracle 環境を運用する組織は月次 CSPU の適用体制を整備する必要がある。
  - AI が攻撃側だけでなく防御側のパッチサイクル短縮にも活用される「AI vs AI」の構図が明確化している。
- **リンク**: <https://blogs.oracle.com/security/accelerating-vulnerability-detection-and-response-at-oracle>

---

### NHS England、フロンティア AI のコード解析リスクを理由に GitHub 公開リポジトリを 5/11 までに非公開化

- **公開日**: 2026-05-05〜2026-05-06
- **ソース**: The Register / Cybernews
- **要約**:
  - NHS England が全技術リーダーに対し、公開 GitHub リポジトリを 2026-05-11 までに非公開化するよう命令。Claude Mythos 等のフロンティアモデルが大規模にコードを読み込み、アーキテクチャ・設定・内部ロジックを推論・悪用するリスクを明示的に理由として挙げた。
  - AI モデルの高度なコード理解能力が、従来「公開しても安全」とされていたオープンソースコードのリスク評価を根本から変えつつあることを示す事例。
  - 組織は公開リポジトリに含まれる内部構成情報・秘密情報・アーキテクチャ情報の棚卸しを今すぐ実施すべき。
- **リンク**: <https://www.theregister.com/software/2026/05/05/nhs-to-close-source-github-repos-over-ai-security-concerns/5224392>

---

## セキュリティ関連ニュース

### 「Dirty Frag」— Linux カーネルに PoC 付きゼロデイ特権昇格チェーン (CVE-2026-43284 / CVE-2026-43500)

- **公開日**: 2026-05-07 (PoC 公開・embargo 破り) / 2026-05-08 (Microsoft Security Blog・各社続報)
- **ソース**: BleepingComputer / Microsoft Security Blog / Wiz / AlmaLinux
- **要約**:
  - Linux カーネルの `xfrm-ESP` (IPsec) サブシステムと `RxRPC` に存在する 2 つのページキャッシュ書き込みプリミティブを連鎖させることで、非特権ローカルユーザーが root に昇格できる。Dirty Frag の名称で呼ばれ、前月報告の Copy Fail (CVE-2026-31431) の後継に位置づけられる。
  - 5 月 7 日に第三者がエンバーゴを破り PoC がインターネット上に公開。Microsoft Security Blog は 5 月 8 日に「実際の攻撃が既にポストコンプロマイズ展開に悪用されている」と警告。Ubuntu・RHEL・CentOS Stream・AlmaLinux・Fedora・openSUSE・OpenShift 全域に影響。ESP パッチは 5/7 にマージ済み、RxRPC パッチは審査中。
  - PoC 公開済みのため悪用敷居が低い。ホスト・コンテナ・Kubernetes 環境すべてで即時パッチ適用が必要。適用まで間は非特権ユーザーへのコンテナエスケープ・SUID バイナリ制限などの緩和策を実施すること。
- **リンク**: <https://www.bleepingcomputer.com/news/security/new-linux-dirty-frag-zero-day-with-poc-exploit-gives-root-privileges/>

---

### Instructure (Canvas LMS) — ShinyHunters が 275 M 件を主張する教育史上最大規模のデータ侵害

- **公開日**: 2026-05-08 (サービス復旧・Time誌解説)
- **ソース**: Time / CNN / Harvard Crimson / Wikipedia
- **要約**:
  - 世界 9,000 校超が利用する LMS「Canvas」の運営会社 Instructure が ShinyHunters ランサムグループによる不正アクセスを受けた。ShinyHunters は 2.75 億件（3.65 TB）のデータ取得を主張し、学生・教職員の氏名・メール・ID・プライベートメッセージの流出を示すサンプルを提示。5 月 12 日まで支払いを要求する公開脅迫キャンペーンを展開中。
  - 5 月 7 日に Canvas が一時オフライン、5 月 8 日に復旧。期末試験期間と重なり米国内数千の大学・高校で授業が中断された。Instructure にとって 8 ヶ月以内 2 度目の ShinyHunters 侵害。
  - 教育機関向け SaaS を利用する組織はベンダーの侵害対応体制・データ分離設計・通知ポリシーを改めて確認すること。
- **リンク**: <https://time.com/article/2026/05/08/canvas-cyber-attack-shinyhunters-hack-what-to-know/>

---

### TCLBANKER — WhatsApp・Outlook で自己拡散するブラジル発バンキング型トロイの木馬

- **公開日**: 2026-05-08
- **ソース**: The Hacker News / Elastic Security Labs
- **要約**:
  - Elastic Security Labs が REF3076 として追跡する新種バンキングトロイ。銀行・Fintech・暗号資産プラットフォーム 59 種を標的とし、WhatsApp Web セッションをハイジャックして連絡先に拡散するワームモジュールと、Outlook を悪用した偽メール送信ボットを内包する。
  - 従来の Maverick (SORVEPOTEL) の大型アップデート版で、ローダーに強力なアンチ解析機能を備える。C2 を使わずソーシャルメッセージングを介した拡散は検知回避において有効。
  - 金融・Fintech 企業はエンドポイントでの WhatsApp Web セッション監視と、Outlook 送信アクティビティの異常検知を強化する必要がある。
- **リンク**: <https://thehackernews.com/2026/05/tclbanker-banking-trojan-targets.html>

---

### Sentry SAML SSO 認証バイパス (CVE-2026-42354) — 任意アカウント乗っ取りが CVSS 9.1

- **公開日**: 2026-05-08
- **ソース**: TheHackerWire / DailyCVE
- **要約**:
  - エラー追跡・パフォーマンス監視ツール Sentry (v21.12.0〜v26.4.1 未満) の SAML SSO 実装に認証バイパス脆弱性。攻撃者が同一 Sentry インスタンス上の組織を制御できる場合、悪意ある IdP を経由して被害者のメールアドレスを知るだけで任意のユーザーアカウントを乗っ取れる。パスワードもユーザー操作も不要。
  - Sentry はオブザーバビリティの中核に位置するため侵害の影響範囲が広い。本番環境のエラーログ・トレース・アラートが攻撃者に読まれると次の侵害のための情報源となる。
  - 対応: Sentry 26.4.1 へ即座にアップグレード。セルフホスト環境では SSO 設定と組織分離の見直しを実施すること。
- **リンク**: <https://www.thehackerwire.com/sentry-critical-account-takeover-via-saml-sso-cve-2026-42354/>

---

### Let's Encrypt が証明書発行を約 2.5 時間停止 — クロス署名証明書インシデント

- **公開日**: 2026-05-08
- **ソース**: Cybersecurity News / mySites.guru / Hacker News
- **要約**:
  - 5 月 8 日 18:37 UTC、Let's Encrypt エンジニアが Generation X から Generation Y ルートへの移行に係るクロス署名証明書で重大な問題を検知し、全証明書発行を即時停止した。21:03 UTC（約 2.5 時間後）に復旧。
  - 5 月 13 日に予定されていた ACME プロファイル変更の直前というタイミングで発生し、`acme-v02.api.letsencrypt.org` および `acme-staging-v02.api.letsencrypt.org` 両エンドポイントに影響した。
  - 今回は短時間で解消されたが、Let's Encrypt に依存する自動証明書更新パイプラインを持つ組織は障害時のフォールバック手順（手動更新・代替 CA の即時発行）を確認・整備しておくこと。
- **リンク**: <https://cybersecuritynews.com/lets-encrypt-halts-certificate-issuance/>

---

### Ivanti EPMM CVE-2026-6973 — 野外悪用中、FCEB 機関パッチ期限は本日 5/10

- **公開日**: 2026-05-07 (初期開示) / CISA KEV 追加後も各メディアで継続報道
- **ソース**: SecurityWeek / SOCRadar / The Hacker News
- **要約**:
  - Ivanti Endpoint Manager Mobile (EPMM) のオンプレ版に存在する入力検証不備 (CVE-2026-6973, CVSS 7.2)。リモート認証済み管理者権限を持つ攻撃者がリモートコード実行できる。Ivanti は一部顧客環境での限定的な悪用を確認。CISA が KEV に登録し、FCEB 機関に対して本日 **2026-05-10** までの修正を義務化。
  - Ivanti EPMM は MDM（モバイルデバイス管理）の基盤製品で、過去にも複数のゼロデイが野外で悪用されている。MDM インフラの侵害は全管理対象デバイスへの影響に波及しうる。
  - 修正版: 12.6.1.1 / 12.7.0.1 / 12.8.0.1。該当バージョンを使用している組織は今日中にパッチ適用を完了すること。
- **リンク**: <https://www.securityweek.com/ivanti-patches-epmm-zero-day-exploited-in-targeted-attacks/>

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 | 影響/CVSS | リンク |
|--------|--------|------|-----------|--------|
| 2026-05-08 | JPCERT/JVN 注意喚起 (Apache HTTP Server 2.4) | Apache HTTP Server 2.4.67 で 11 件の脆弱性を修正。新規: CVE-2026-33006 (mod_auth_digest タイミング攻撃による認証バイパス, CVSS 8.8)、CVE-2026-24072 (CVSS 8.8)、CVE-2026-29169/34059 (各 CVSS 7.5) 等。2.4.67 へのアップグレードを推奨。 | CVSS 最大 8.8 | <https://www.jpcert.or.jp/newsflash/> |
| 2026-05-07〜08 | CVE-2026-43284 / CVE-2026-43500 (Dirty Frag) | Linux カーネル特権昇格チェーン。PoC 公開済み。Ubuntu/RHEL/AlmaLinux 等国内広範に影響。ESP パッチはカーネルツリーにマージ済み、RxRPC は対応中。 | 高 | <https://www.wiz.io/blog/dirty-frag-linux-kernel-local-privilege-escalation-via-esp-and-rxrpc> |
| 2026-05-07 (CISA KEV) / 期限 2026-05-10 | CVE-2026-6973 (Ivanti EPMM) | リモート認証管理者によるコード実行。オンプレ版 EPMM のみ影響。Ivanti Neurons for MDM（クラウド）は対象外。本日が FCEB 機関の修正期限。 | CVSS 7.2 (High) | <https://www.cisa.gov/known-exploited-vulnerabilities-catalog> |
| 2026-05-08 | CVE-2026-42354 (Sentry) | SAML SSO 認証バイパスによるアカウント乗っ取り。国内でも Sentry セルフホスト導入組織は要確認。修正版: 26.4.1 | CVSS 9.1 (Critical) | <https://www.thehackerwire.com/vulnerability/CVE-2026-42354/> |

---

## 本日のサマリ

PoC 公開済みの「Dirty Frag」Linux カーネル特権昇格と、Ivanti EPMM の本日期限パッチ対応が最優先のオペレーション課題。Sentry SAML 認証バイパス (CVSS 9.1) も運用環境での被害が予想されるため即時アップグレードが必要。Canvas/Instructure 事件は 275M 件規模で教育 SaaS 全般のデータ分離設計を問い直す契機となった。AI 領域では OpenAI の音声 AI モデルが GPT-5 クラス推論を獲得し音声エージェント実用化が加速する一方、Semantic Kernel・FastGPT 等の AI フレームワーク自体が新たな脆弱性対象面となっており、AI エージェント導入組織は入力検証・ツール権限の最小化・実行サンドボックス隔離を今すぐ実装段階に引き上げる必要がある。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 25 (AI/Security/国内カテゴリ)
- 採用件数: AI=5 / Security=6 / 国内=4
- 除外理由内訳:
  - 古すぎ (3日以上前): Snap AI 人員削減 (Apr 15), Novo Nordisk+OpenAI (Apr 14), Google Deep Research Max (Apr 21-22), WEF AI Cybersecurity Report (May 4), Eclipse BaSyx ICS CVE (May 5), Microsoft Edge 平文パスワード (Apr 29〜May 4), China-linked hackers (May 1), MuddyWater Microsoft Teams (May 6), Anthropic managed agents dreaming (May 6), Anthropic finance agents (May 5), Anthropic $200B Google 契約 (May 5), US CAISI AI 事前テスト協定 (May 5)
  - 重複 (過去7日分に既出): CVE-2026-31431 (Copy Fail), CVE-2026-0300 (Palo Alto), CVE-2026-23918 mod_http2 (個別 CVE として既出; JPCERT 注意喚起は新規として採用)
  - 日付不明: 0 件
- 取得失敗ソース (HTTP 403 等): bleepingcomputer.com, thehackernews.com, tenable.com, jvn.jp (直接アクセス), llm-stats.com, marketingprofs.com, theregister.com (WebFetch), tenable.com — 検索スニペット・URL パターン・ミラーサイト日付で代替確認
- 備考: WebFetch の 403 エラーが多発したため、記事公開日は URL 内日付文字列・ミラーブログ URL・検索スニペット記述から推定した。厳密な本文 裏取りを実施できていないソースが含まれる点に留意。

</details>
