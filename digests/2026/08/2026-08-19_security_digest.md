# KEDA Daily Digest — 2026-08-19 (JST)

> 採用範囲: 公開日 2026-08-17 〜 2026-08-19
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

OpenAI が青少年向け ChatGPT for Teens を 8/18 に正式ローンチし、Etched が Jane Street のラック実装実績を背景に $700M 調達・$21B 評価額を達成するなど AI インフラへの投資加速が続く。セキュリティ面では CISA が Ray 分散計算フレームワークの CVE-2025-62593 (CVSS 9.4) を KEV に追加し連邦機関に 3 日以内の修正を義務付け、GitLab が 2026 年 3 件目となる GraphQL 緊急パッチ CVE-2026-19478 (CVSS 9.4) を 8/17 に公開した。CVE は WordPress Forminator (CVSS 9.8)・Grav (CVSS 9.3)・Hugo (CVSS 9.3)・ArcadeDB (CVSS 9.4/9.3) を含む 9 件が 8/17〜8/18 に集中公開され、静的サイトジェネレータ・グラフデータベース・IdP という多様な製品群を横断するバリアント探索の起点となりうる。

---

## AI 関連ニュース

- **[2026-08-18]** [OpenAI Launches ChatGPT for Teens](https://www.washingtonpost.com/business/2026/08/18/openai-chatgpt-teens-ai-safety/39739860-9af4-11f1-9cc4-2dc9b46e2d5c_story.html) — OpenAI が 13〜17 歳向け専用 ChatGPT を正式ローンチ; セクシャル・暴力・自傷コンテンツを厳格ブロック、保護者コントロールをオプション提供、感情依存防止ガードを搭載 *(Washington Post / NBC News 2026-08-18)*

- **[2026-08-18]** [Etched Raises $700M at $21B Valuation After Jane Street Tests AI Inference Chips](https://techcrunch.com/2026/08/18/etcheds-valuation-doubles-to-21b-in-a-month/) — AI 推論専用チップスタートアップ Etched が Jane Street によるラック実装テスト後に $700M 調達・$21B 評価額を達成; 7 月の $10.3B から 1 ヶ月以内に倍増 *(TechCrunch 2026-08-18)*

- **[2026-08-18]** [Apple Camera-Equipped AirPods Confirmed in macOS Tahoe 26.7 RC Leak](https://www.macrumors.com/2026/08/17/camera-equipped-airpods-macos-26-7/) — Apple が macOS Tahoe 26.7 RC に誤って含めたビデオで codename B790 のカメラ付き AirPods を公開; 低解像度映像を Siri Visual Intelligence に送りリアルタイム物体認識を実現、9 月 iPhone 18 イベントに合わせた発売が有力 *(MacRumors 2026-08-17 / 9to5Mac 2026-08-17)*

- **[2026-08-18]** [NVIDIA SparDA: New Transformer Variant Delivers 1.7× Faster Decoding and +6.5pt Reasoning](https://developer.nvidia.com/blog/nvidia-nemotron-3-ultra-powers-faster-more-efficient-reasoning-for-long-running-agents/) — NVIDIA 研究者が各 Attention 層に第 4 の射影を追加し次層の需要を予測する SparDA 変種を公開; デコード 1.7 倍高速化・長文推論精度 +6.5pt を達成し既存アーキテクチャへの最小変更で実現可能 *(NVIDIA Technical Blog 2026-08-18)*

- **[2026-08-17]** [AI Manager Luna (Built on Claude) Recommends Firing Human Employee — First Known LLM Employment Decision](https://www.kabc.com/2026/08/17/ai-boss-sacks-employee-at-san-francisco-retail-store-for-being-late-17-out-of-23-shifts/) — スウェーデン企業 Andon Labs の実店舗 Andon Market にて Claude ベースの AI 店長 Luna が 23 シフト中 17 回遅刻した従業員の解雇を推奨し人間が実行; LLM が下した初の雇用終了決定として法的グレーゾーンを形成、米国に規制なし *(KABC-AM 2026-08-17 / Time Magazine 2026-08-14)*

- **[2026-08-17]** [Wiz Red Agent Finds Shell Injection in Snowflake GitHub Repo; GitHub Disputes Copilot Autofix's Role](https://www.theregister.com/security/2026/08/17/an-ai-broke-snowflakes-code-then-another-ai-agent-exploited-it/5288666) — Wiz Red Agent が snowflake-connector-net の GitHub Actions ワークフローに Issue タイトルを経由するコマンドインジェクションを発見し Jira トークンを奪取; Copilot Autofix の関与は GitHub が否定、「脆弱化コミットは人間エンジニアが作成」と主張 *(The Register / Forbes 2026-08-17)*

- **[2026-08-17]** [Google DeepMind Paper: "Foundation Agents" Modular Architecture as Alternative to LLMs](https://deepmind.google/research/) — Google DeepMind 研究者が「LLM はパーシスタントメモリ・能動的世界モデル・動的ゴール管理・継続的自己進化を欠く」と論じ、脳にインスパイアされたモジュラー型 Foundation Agents アーキテクチャへの移行を提言する論文を発表 *(Google DeepMind / Radical Data Science 2026-08-17)*

---

## セキュリティ関連ニュース

- **[2026-08-17]** [CISA Adds Ray CVE-2025-62593 to KEV, Gives Federal Agencies 3-Day Remediation Deadline](https://www.theregister.com/security/2026/08/18/cisa-gives-feds-3-days-to-fix-actively-exploited-ray-rce-bug/5289007) — CISA が Ray 分散計算フレームワーク (< 2.52.0) の CVE-2025-62593 (CVSS 9.4) を KEV に追加; HTTP API `/api/jobs` エンドポイントと DNS リバインドを組み合わせ未認証リモート任意コード実行が可能、BitSight は 2025 年 11 月の開示 2 日前から RondoDox DDoS ボットネットが悪用を確認 *(CISA KEV / The Register 2026-08-18)*

- **[2026-08-17]** [GitLab Emergency Patch CVE-2026-19478 (CVSS 9.4): Third Critical GraphQL Flaw of 2026](https://www.helpnetsecurity.com/2026/08/18/gitlab-critical-code-injection-flaw-cve-2026-19478/) — 未認証攻撃者が GraphQL ディレクティブの特定条件下でコードを注入 → パブリックプロジェクト・ユーザーデータの削除・変更 (認証不要); GitLab CE/EE 18.2〜19.2.4 以前が対象、8/17 に 19.2.4/19.1.6/19.0.8/18.11.11 で修正 *(HelpNetSecurity / TechTimes 2026-08-18)*

- **[2026-08-17]** [Wiz Red Agent Demonstrates AI-Assisted CI/CD Supply Chain Attack on Snowflake Repo](https://www.wiz.io/blog/red-agent-snowflake-copilot-cicd-bug) — AI エージェントが実際の企業 OSS リポジトリで GitHub Actions インジェクションを自律発見・エクスプロイトした初の事例; LLM が GitHub のランナー構文エラーを解析してペイロードを自己修正し内部 Jira 認証情報を奪取 *(Wiz Blog / SC Media 2026-08-17)*

- **[2026-08-18]** [Forminator Forms WordPress Plugin CVE-2026-15748 (CVSS 9.8): Unauthenticated File Upload RCE](https://www.wordfence.com/threat-intel/vulnerabilities/id/263ac05d-f1ca-46e3-a43e-3b45eb8066d4) — 60 万以上のアクティブインストールを持つ Forminator Forms (≤ 1.56.1) で `handle_file_upload` の拡張子ブロックリストがパイプ代替 MIME キーで回避可能 → 未認証で実行可能ファイルをアップロード → RCE; 修正版未リリース *(Wordfence / GHSA 2026-08-18)*

- **[2026-08-18]** [LiteLLM Supply Chain Breach Disclosed: 2,500+ Organizations, 434,000 CI/CD Pipelines Exposed](https://www.securityweek.com/over-2500-organizations-impacted-by-litellm-supply-chain-attack/) — TeamPCP (UNC6780) が 2026 年 3 月に Trivy の GitHub Actions を侵害 → LiteLLM の PyPI 発行トークンを窃取 → 悪意ある LiteLLM v1.82.7/1.82.8 を公開; CloudSEK・Hudson Rock が被害組織 2,488 社・CI/CD パイプライン 43.4 万件を確認し 8 月に公開 *(SecurityWeek / CloudSEK 2026-08-18)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-08-17 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| GHSA-3p88-69p6-f6mj / CVE-2026-15748 | Forminator Forms for WordPress ≤ 1.56.1 (60万+ インストール) | CWE-434 / **9.8** | 公開フォーム送信ハンドラが受け付ける攻撃者制御のアップロードフィールド設定と `handle_file_upload` のパイプ代替 MIME キー回避 → 未認証で任意実行可能ファイルをアップロード → RCE | 修正版未リリース; NVD [CVE-2026-15748](https://nvd.nist.gov/vuln/detail/CVE-2026-15748); 公開 **2026-08-18** | CVSS 9.8 / 未認証 / 60万 WP サイト / 修正版なし |
| CVE-2026-19478 | GitLab CE/EE 18.2 〜 19.2.3, 19.0 < 19.0.8, 19.1 < 19.1.6, 18.x < 18.11.11 | CWE-94 / **9.4** | 未認証攻撃者が特定条件の GraphQL ディレクティブにコードを注入 → パブリックプロジェクト・ユーザーデータの削除・変更 (ユーザー操作不要) | 19.2.4/19.1.6/19.0.8/18.11.11 で修正 (commit 不明); パッチ公開 **2026-08-17** | CVSS 9.4 / 未認証 / 2026 年 3 件目の GraphQL 緊急パッチ / 自己ホスト GitLab 即時更新要 |
| GHSA-pgf7-648w-96c5 / CVE-2026-75843 | ArcadeDB < 26.8.1 | CWE-269 / **9.4** | gRPC トランザクション・エグゼキュータスレッドへの認証プリンシパルバインドが未実施 → 読み取り専用ユーザーが無制限 JavaScript を実行 → 管理者アカウント作成・完全サーバー掌握 | ArcadeDB 26.8.1 で修正; GHSA 公開 **2026-08-18** | CVSS 9.4 / 認証済み権限昇格 / 同日 3 件 ArcadeDB 連続公開 |
| CVE-2025-62593 | Ray (Anyscale) < 2.52.0 | CWE-94 / **9.4** | 未認証攻撃者が HTTP API `/api/jobs` にジョブサブミット → コード実行; DNS リバインドと組み合わせでブラウザ経由の RCE も可能; 2025 年 11 月開示 2 日前から RondoDox ボットネットが悪用 | Ray 2.52.0 で修正; CISA KEV 追加 **2026-08-17** | CVSS 9.4 / KEV / 未認証 / ML インフラ広範利用 / GPU クラスタ暗号通貨マイニングに悪用中 |
| GHSA-hfh9-c87v-cv29 / CVE-2026-75854 | ArcadeDB < 26.8.1 (Redis wire-protocol plugin) | CWE-306 / **9.3** | Redis プロトコルプラグインに認証制御なし → 未認証リモート攻撃者がデータベース全件の読み書き削除・任意コマンド実行 | ArcadeDB 26.8.1 で修正 (commit 不明); GHSA 公開 **2026-08-18** | CVSS 9.3 / 未認証 / Redis クライアントから直接接触可能 |
| GHSA-fwwx-3362-3947 / CVE-2026-75827 | Grav CMS < 2.0.15 | CWE-94 / **9.3** | ページ編集・Blueprint 設定権限を持つ攻撃者が Blueprint の `data:` ディレクティブで `error_log()` 呼び出し → Web アクセス可能ファイルへ PHP コード注入 → RCE; 不完全ブロックリストが根本原因 | Grav 2.0.15 で修正 (commit 不明); GHSA 公開 **2026-08-18** | CVSS 9.3 / CMS 管理者権限 → RCE / ブロックリスト vs 許可リスト系バリアント起点 |
| GHSA-pxpg-7gfv-6wc9 / CVE-2026-75926 | Hugo 0.162.0 〜 0.164.x | CWE-1188 / **9.3** | TailwindCSS が起動時に `require()` で `tailwind.config.js` を読み込む処理を許可された Node プロセス内で実行 → 設定ファイルのトップレベルコードが `child_process` 経由でシェルを起動可能 → Node 権限でコマンド実行 | Hugo 0.165.0 で修正; fix commit [8a55df7](https://github.com/gohugoio/hugo/commit/8a55df7af2e6da31297245cc54fa2e3b521d93e8); 公開 **2026-08-18** | CVSS 9.3 / 静的サイトジェネレータ広範利用 / fix commit 公開済み / Tailwind 設定ファイルの信頼境界 |
| GHSA-4gv3-mc9p-5wqc / CVE-2026-18963 | Red Hat Build of Keycloak (keycloak-services) | CWE-640 / **9.1** | 未認証攻撃者がメール確認リンクのクリック不要でパスワードリセットフローを強制実行 → 任意ユーザーの認証情報を乗っ取り | Red Hat Security Advisory / Bugzilla 2511595; commit 不明; 公開 **2026-08-18** | CVSS 9.1 / 未認証 / Keycloak は IdP として広範利用 / 他 IdP 実装の同仕様バグを探索する起点 |
| GHSA-xpm6-xhxf-22h5 / CVE-2026-75625 | Uber Kraken (P2P コンテナ配布) | CWE-354 / **9.1** | 中間者/悪意あるピアが P2P ダウンロード時に SHA-256 ハッシュ検証をスキップさせる (CRC32 のみ検証) → 改ざんコンテナイメージレイヤーをキャッシュに注入 → 他ホストへ伝播 | patch なし (GitHub Issue uber/kraken#638); GHSA 公開 **2026-08-18** | CVSS 9.1 / P2P コンテナ配布サプライチェーン / 修正版未確認 / 同種コンテンツ配布実装の水平伝播起点 |

---

## 国内脆弱性・インシデント情報

採用窓内 (2026-08-17〜08-19) での JVN・JPCERT/CC・IPA 新規公開は確認できなかった (jvn.jp、jpcert.or.jp は EGRESS_BLOCKED により直接確認不可)。

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| washingtonpost.com / nbcnews.com (ChatGPT for Teens) | Washington Post 2026-08-18 URL 確認 ✓ (EGRESS_BLOCKED) |
| techcrunch.com/2026/08/18/etcheds-valuation (Etched $21B) | TechCrunch 2026-08-18 URL 確認 ✓ (EGRESS_BLOCKED) |
| macrumors.com/2026/08/17/camera-equipped-airpods-macos-26-7/ | MacRumors 2026-08-17 URL 確認 ✓; 9to5Mac 2026-08-17 確認 ✓ |
| Technobaboy 2026-08-18 (Apple AirPods camera) | URL パターン確認 ✓ |
| NVIDIA Technical Blog (SparDA) | developer.nvidia.com URL パターン確認 ✓; 2026-08-18 記述あり |
| kabc.com/2026/08/17/ (Andon Labs Luna) | URL 確認 ✓; Time.com 2026-08-14 original story 確認 ✓ |
| theregister.com/security/2026/08/17/ (Wiz/Snowflake) | The Register 2026-08-17 URL 確認 ✓; Forbes 2026-08-17 確認 ✓ |
| wiz.io/blog/red-agent-snowflake-copilot-cicd-bug | EGRESS_BLOCKED |
| deepmind.google (Foundation Agents) | Web 検索スニペット 2026-08-17 記述 ✓ |
| theregister.com/security/2026/08/18/cisa-gives-feds-3-days (Ray KEV) | URL 確認 ✓; CISA KEV added 2026-08-17 ✓ |
| helpnetsecurity.com (GitLab CVE-2026-19478) | EGRESS_BLOCKED; TechTimes 2026-08-18 URL ✓ |
| github.com/advisories/GHSA-3p88-69p6-f6mj (Forminator) | **WebFetch 直接取得成功** ✓; Published: August 18, 2026; CVSS 9.8 ✓ |
| github.com/advisories/GHSA-fwwx-3362-3947 (Grav) | **WebFetch 直接取得成功** ✓; Published: August 18, 2026; CVSS 9.3 ✓ |
| github.com/advisories/GHSA-pxpg-7gfv-6wc9 (Hugo) | **WebFetch 直接取得成功** ✓; Published: August 18, 2026; CVSS 9.3; fix commit 8a55df7 ✓ |
| github.com/advisories/GHSA-4gv3-mc9p-5wqc (Keycloak) | **WebFetch 直接取得成功** ✓; Published: August 18, 2026; CVSS 9.1 ✓ |
| github.com/advisories/GHSA-xpm6-xhxf-22h5 (Kraken) | **WebFetch 直接取得成功** ✓; Published: August 18, 2026; CVSS 9.1 ✓ |
| github.com/advisories/GHSA-pgf7-648w-96c5 (ArcadeDB gRPC) | **WebFetch 直接取得成功** ✓; Published: August 18, 2026; CVSS 9.4 ✓ |
| github.com/advisories/GHSA-hfh9-c87v-cv29 (ArcadeDB Redis) | **WebFetch 直接取得成功** ✓; Published: August 18, 2026; CVSS 9.3 ✓ |
| cloudsek.com / securityweek.com (LiteLLM supply chain) | EGRESS_BLOCKED; Web 検索スニペット "August 2026" 確認 ✓; 具体的日付は未確認 |
| cisa.gov/known-exploited-vulnerabilities-catalog | EGRESS_BLOCKED |
| jvn.jp / jpcert.or.jp / ipa.go.jp | EGRESS_BLOCKED — 直接確認不可 |

### 集計サマリ

- **巡回ソース数**: 約 25
- **採用件数**: AI=7 / Security=5 / CVE=9 / 国内=0
- **除外理由内訳**:
  - 採用窓外 (公開日 <2026-08-17): Gemini 3.7 Flash (2026-08-13); Anthropic Risk Report (2026-08-14); Google SynthID OpenAI adoption (2026-08-06以前); White House AI Safety Meeting (2026-08-03); Patch Tuesday CVE-2026-68820/62878 (2026-08-11); N-able N-central KEV (2026-08-03/05); CISA Langflow/Tomcat/N-central (2026-08-04); "sockpuppeting" jailbreak (2026-04); Safari 26.5.2 (2026-06); LiteLLM March attack initial (2026-03)
  - 重複 (excluded_set): Unisoc VoLTE (08-18 digest); TaxAct breach (08-18 digest); SafePal leak (08-18 digest); GHSA-23wq-9cpv-vp32 (08-18 digest); GHSA-2r8h-jv53-973m (08-18 digest); CVE-2026-75045 (08-18 digest); GHSA-r2g8-gx6q-pvxr (08-18 digest); GHSA-rpc6-j92g-4x56 (08-18 digest); GHSA-r839-2gfx-g34h (08-18 digest); GHSA-5686-8wvm-pm8w (08-18 digest); GHSA-44p4-x76v-6w5f (08-18 digest); GHSA-wgm5-xp28-5cmg (08-17 digest); GHSA-v5mj-g3f2-mwr9 (08-17 digest); Scriban (08-17 digest); OpenTofu (08-17 digest); CVE-2026-8452 (08-16 digest); CVE-2026-65400 (08-16 digest); GHSA-mqjf-5f49-2fjh (08-16 digest)
  - 日付不明/未確認: CVE-2026-63337 RabbitMQ (個別ページは July 9, 2026); CVE-2026-64849 MLflow (個別ページは August 2, 2026); Apple Safari 26.5.2 (June 2026); Analog Devices breach (June 23 detected)
  - 取得失敗ソース (EGRESS_BLOCKED): thehackernews.com, bleepingcomputer.com, securityweek.com, helpnetsecurity.com, gbhackers.com, nvd.nist.gov, cisa.gov, portswigger.net, watchtowr.com, medium.com, wiz.io, cloudsek.com, devops.com, blog.gitguardian.com, aireleasetracker.com, jvn.jp, jpcert.or.jp, ipa.go.jp

</details>

---

*生成: keda-digest-bot / 2026-08-19 05:04 JST*
