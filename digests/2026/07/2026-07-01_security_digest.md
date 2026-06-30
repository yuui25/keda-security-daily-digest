# KEDA Daily Digest — 2026-07-01 (JST)

> 採用範囲: 2026-06-29 〜 2026-07-01 (JST) | 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Anthropic が Claude Science ベータ公開・カリフォルニア州政府調達協定・Microsoft Azure GA を同日前後に実現し IPO 前夜の事業基盤を固めた一方、npm/Go パッケージのブロックチェーン Dead Drop 経由スティーラー・Edge 拡張ステガノグラフィ・AI ブランド詐称 Chrome 拡張によるサプライチェーン攻撃が集中し開発者の端末・クラウド認証情報が広範に狙われている。SimpleHelp CVE-2026-48558 悪用は Djinn Stealer + TaskWeaver 展開に発展 (連邦機関修正期限 7/7)、Sigstore Fulcio SSRF + K8s トークン漏洩 (CVE-2026-49478) と libssh2 PoC 公開 (CVE-2026-55200) が重なりパッチ優先度が上昇している。

---

## AI ニュース

- **[2026-06-30]** Anthropic、**Claude Science** ベータを公開 — 60+ 科学データベース (PubMed・arXiv・ClinicalTrials 等) を統合し生物・化学タスクの自動化を実現; 学術研究者向けに最大 $30K コンピュートクレジットを支援 — Bloomberg / STAT News *(2026-06-30 UTC)*
- **[2026-06-29]** Anthropic × カリフォルニア州: Newsom 知事が全州機関・市町村に Claude を半額提供する史上初の大規模政府 AI 調達協定を締結 — 推定 30 万人の公務員が対象; Anthropic は州のプライバシー監査に合意 — TechCrunch / gov.ca.gov *(2026-06-29 UTC)*
- **[2026-06-29]** Claude が **Microsoft Azure AI Foundry** で GA — Opus 4.8・Haiku 4.5・Sonnet 5 が NVIDIA GB300 Blackwell Ultra 上で稼働; Azure 認証・課金・データレジデンシー統合; 日本リージョン含む 15 拠点でサービス開始 — Azure Blog / Anthropic *(2026-06-29 UTC)*
- **[2026-06-29]** AI ブランド詐称型悪意 Chrome 拡張 **"Search for perplexity ai"** が検索クエリ・アドレスバー入力を全件傍受 — 偽ドメイン perplexity-ai.online で IP・UA・入力を記録し第三者サーバーへ転送; Microsoft Security Blog が公開後 Google が削除 — Microsoft Security Blog / THN *(2026-06-29 UTC)*

---

## セキュリティニュース

- **[2026-06-29]** **StegoAd**: Microsoft が 119 件の悪意 Edge 拡張機能 (累計 2.6M インストール) を一斉削除 — PNG/WOFF フォントへのステガノグラフィで JS ペイロードを隠蔽; Google 認証情報・WordPress 管理者パスワード・セッション Cookie を窃取; 同手法は Chrome 拡張にも波及 — Malwarebytes / TechRadar *(2026-06-29 UTC)*
- **[2026-06-29]** 乗っ取り **npm/Go パッケージがブロックチェーン Dead Drop** 経由で Python インフォスティーラーを展開 — JFrog が `html-to-gutenberg` 4.2.11 / `fetch-page-assets` 1.2.9 の改ざんを発見; VS Code フォルダオープン自動タスクで起動、TronGrid/Aptos を C2 コマンドドロップに使用; 同一マルウェアを含む Go パッケージ 16 件も確認 — JFrog Security / THN *(2026-06-29 UTC)*
- **[2026-06-30]** [続報] **SimpleHelp CVE-2026-48558** 悪用で **Djinn Stealer + TaskWeaver** が展開 — AWS/GCP/Azure 認証情報・AI コーディングアシスタント API キー・暗号資産ウォレットを標的とする新型クロスプラットフォームスティーラー; CISA 連邦機関修正期限 7/7 — Help Net Security / THN / BleepingComputer *(2026-06-30 UTC)*
- **[2026-06-29]** **libssh2 CVE-2026-55200** の PoC が公開 — CVSS 9.2; `ssh2_transport_read()` の `packet_length` 上限バイパスでヒープ OOB 書き込み → 悪意 SSH サーバーへの接続だけで RCE 可能; curl・Git・PHP・libgit2・WinSCP 等広範エコシステムに影響 (CVE-2026-58051 とは別 CVE) — THN / heise online *(2026-06-29 UTC)*

---

## CVE / 脆弱性情報

| CVE / GHSA | 製品 | CWE / CVSS | バグクラス (条件 + sink + 結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-49478 / GHSA-f5mr-q85p-6hh6 | sigstore/fulcio ≤ 1.8.5 | CWE-918 / **8.7** | OIDC Discovery メタデータ取得時にホスト間リダイレクトを許可 → 内部ホストへ SSRF + JWKS キャッシュ汚染 → K8s ServiceAccount トークン漏洩 | [Fulcio v1.8.6](https://github.com/sigstore/fulcio/releases/tag/v1.8.6) | 2026-06-29 GHSA 公開 / ソフトウェアサプライチェーン署名インフラ (Sigstore) への影響 / EKS・GKE・AKS 利用者は K8s token 漏洩に深刻なリスク / Rekor・cosign 等他 Sigstore コンポーネントへバリアントハント推奨 |
| CVE-2026-58370 | Woodpecker CI < 3.15.0 (GitLab forge ドライバー) | CWE-285 / **Critical** | ウェブフックペイロードの攻撃者制御コミット Author 名を `pipeline.Author` に直接代入 → `ApprovalAllowedUsers` allowlist 照合を偽造 → フォーク PR からパイプライン承認をバイパスして CI エージェント上のシークレットを漏洩 | [Woodpecker v3.15.0](https://github.com/woodpecker-ci/woodpecker/releases/tag/v3.15.0) | 2026-06-30 GHSA 公開 / CI/CD フォーク安全境界の完全破壊 / GitLab + Woodpecker 環境の CI secrets 窃取リスク大 / Forgejo・Gitea ドライバーは非影響 / GitHub Actions・Tekton 等 CI 全般へバリアントハント推奨 |
| CVE-2026-48806 + CVE-2026-48807 + CVE-2026-48808 | Twig (twig/twig) < 3.27.0 (PHP テンプレートエンジン) | CWE-693 / Moderate (3件) | (48806) 動的マッピングキーが Sandbox ポリシーチェックなしで文字列キャストを発行 → `__toString()` 無制限呼び出し; (48807) join/replace フィルターと in/not in 演算子が Traversable で `ensureToStringAllowed()` を迂回; (48808) column フィルターが SourcePolicyInterface 使用時にプロパティ許可リストを完全スキップ | [Twig 3.27.0](https://github.com/twigphp/Twig/releases/tag/v3.27.0) | 2026-06-29〜30 GHSA 3 件同時公開 / Drupal・Symfony・Laravel 等 Twig 採用フレームワーク全般のカスタムサンドボックス構成に影響 / `__toString()` バイパスパターンは他 PHP テンプレートエンジン (Smarty・Plates 等) へバリアントハント推奨 |

---

## 国内脆弱性 / インシデント

| 公開日 | 識別子 | 概要 | CVSS / 影響 | リンク |
|---|---|---|---|---|
| 2026-06-30 | インシデント | **Aflac 生命保険 Japan** が不正アクセスを公表: 6 月 15〜25 日の侵害で顧客 **438 万件** (氏名・住所・電話) と 23 万件の口座情報が漏洩; My Number・クレジットカード情報は非対象; 金融庁・警察に報告済み | 高 (個人情報・金融口座情報) | Japan Times / SecurityWeek *(2026-06-30 JST)* |

---

<details>
<summary>収集メタデータ / デバッグ情報</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| github.com/advisories (Jun 29-Jul 1 filter) | GHSA-f5mr (Fulcio/sigstore), CVE-2026-58370 (Woodpecker CI), GHSA-48806/-48807/-48808 (Twig) 取得 ✓ |
| anthropic.com / azure.microsoft.com (Claude Science / Azure GA) | 403 → WebSearch スニペットで代替確認 ✓ |
| Microsoft Security Blog (Perplexity AI 偽拡張) | WebSearch スニペット確認 ✓ |
| Malwarebytes / TechRadar (StegoAd 続報) | 2026-06-29 UTC 確認 ✓ |
| JFrog Security Blog (npm/Go Dead Drop) | WebSearch スニペット確認 ✓ |
| Help Net Security / THN (SimpleHelp Djinn Stealer 続報) | 403 → WebSearch スニペットで代替 ✓ |
| THN / heise online (libssh2 CVE-2026-55200 PoC) | WebSearch スニペット確認 ✓ |
| Japan Times / SecurityWeek (Aflac Japan) | WebSearch スニペット確認 ✓ |
| bleepingcomputer.com | 403 — WebSearch スニペットで代替 |
| thehackernews.com | 403 — WebSearch スニペットで代替 |
| securityweek.com | 403 — WebSearch スニペットで代替 |
| jvn.jp | 403 — JVN 新規エントリなし (WebSearch 確認) |

### 集計サマリ

- **AI ニュース**: 4 件
- **セキュリティニュース**: 4 件
- **CVE エントリ**: 3 グループ (5 CVE)
- **国内インシデント**: 1 件
- **AI 件数が目安 (8〜12) を下回った理由**: 採用窓 (2026-06-29〜07-01) が週明け閑散期; Mistral OCR 4 (Jun 23)・Oracle PeopleSoft CVE-2026-35273 (Jun 10-11)・GentleKiller ESET (Jun 18) は採用窓外; Colorado AI Act 改正 SB 189 は法律的複雑度高く除外; Gemini 3.5 Pro GA (7 月以降延期)・GPT-5.6 一般公開 (7 月予定) は未公式
- **除外 (採用窓外)**: Mistral OCR 4 (Jun 23), Oracle PeopleSoft CVE-2026-35273 (Jun 10-11), GentleKiller ESET Report (Jun 18), Colorado AI Act SB 189 (May 14 署名)
- **重複除外 (excluded_set)**: SimpleHelp CVE-2026-48558 本体 (Jun 30 digest 掲載済み, 今回は続報として [続報] 採用), Grok 4.5 (Jun 30), Gemini 3.5 Pro 延期 (Jun 30), Oracle EBS CVE-2026-46817 (Jun 30), Bucket Hijacking (Jun 30), MCP Toolbox CVE-2026-11720 (Jun 30), Gorse CVE-2026-56782 (Jun 30), SigNoz CVE-2026-57955 (Jun 30), Mythic C2 (Jun 30), Nitter CVE-2026-56285 (Jun 30), Amazon Q CVE-2026-12957/-12958 (Jun 29), Linux pedit COW CVE-2026-46331 (Jun 29), libssh2 CVE-2026-58051 (Jun 29), RustDesk CVE-2026-58056 (Jun 29), pnpm GHSA batch (Jun 29), Claude Code v2.1.195 (Jun 29), Anthropic Mythos 5 (Jun 29), DeepMind exodus (Jun 29), OpenAI IPO (Jun 29)

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-06-24 〜 2026-06-30) の全 CVE/GHSA/URL を除外済み。*
