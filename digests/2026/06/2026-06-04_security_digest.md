# KEDA Daily Digest — 2026-06-04 (JST)

> 採用範囲: 公開日 2026-06-02 〜 2026-06-04
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Trump 大統領が AI イノベーション・セキュリティ EO「Promoting Advanced Artificial Intelligence Innovation and Security」に署名し、フロンティアモデルの 30 日前政府レビュー (任意) と AI サイバーセキュリティクリアリングハウス設立が決定。Sophos が攻撃者による Claude Opus 4.5 + Cursor エージェントを使った EDR 回避マルウェアラボ構築を公表、同日 Anthropic が 1 年分の AI 悪用攻撃 MITRE ATT&CK マッピング報告書 (高リスクアクターが 1.7 倍増) を公開し、AI による攻撃自動化が実用段階に突入したことが確認された。CVE 面では Kirki WordPress プラグイン (CVSS 9.8) の非認証アカウント乗っ取りが 500,000+ サイトで積極悪用中、また 2022 年の Linux cgroups 特権昇格が未パッチ・コンテナ環境で依然悪用されているとして CISA が KEV に追加した。

---

## AI 関連ニュース

- **[2026-06-02]** [Trump が AI EO「Promoting Advanced Artificial Intelligence Innovation and Security」に署名 — フロンティアモデルの公開 30 日前政府レビュー (任意)・AI サイバーセキュリティクリアリングハウス設立・AI 駆動の連邦サイバー防衛強化・AI 悪用刑事訴追優先化を指示](https://www.whitehouse.gov/presidential-actions/2026/06/promoting-advanced-artificial-intelligence-innovation-and-security/) — 当初案の 90 日から 30 日に短縮の妥協案；Microsoft・Google・xAI は既に任意参加を表明済み、NIST/CISA がモデル評価を担当予定 *(White House / CNBC / NPR)*

- **[2026-06-02]** [Sophos、攻撃者が Claude Opus 4.5 + Cursor エージェントを用いて Rust/Go 80 モジュール・70 回避技術を検証する EDR 回避マルウェアラボを構築したと開示](https://www.sophos.com/en-us/blog/pointing-a-cursor-at-evading-detection) — Sophos・CrowdStrike・Defender の 3 製品を VM 環境でテスト；Cobalt Strike プロファイルで正規トラフィックに偽装、Telegram bot API で C2 を隠蔽。Git リポジトリが流出して発覚 *(Sophos / Help Net Security / BleepingComputer)*

- **[2026-06-03]** [Anthropic が「1 年分の AI 活用サイバー攻撃 MITRE ATT&CK マッピング」報告書を公開 — 832 件の禁止アカウント (2025/03〜2026/03) を分析、67.3% がマルウェア作成に AI を使用、高リスク行為者割合が 33%→56% に 1.7 倍増加](https://www.anthropic.com/news/AI-enabled-cyber-threats-mitre-attack) — AI が攻撃チェーン後段 (lateral movement 6.5%) にも浸透；現行 MITRE ATT&CK は AI オーケストレーション型挙動を未収録と指摘し、フレームワーク更新を提言 *(Anthropic)*

- **[2026-06-02]** [Microsoft が Build 2026 で独自コーディングモデル MAI-Code-1-Flash を発表 — OpenAI/Anthropic 依存低減・コスト削減を目指す初の Microsoft 自社開発コード生成モデルを一般向けに提供](https://www.cnbc.com/2026/06/02/microsoft-unveils-new-ai-models-lessen-reliance-on-openai-lower-costs.html) — Copilot Project Polaris (GPT-4 代替) と並行展開；コーディング AI 市場での垂直統合が加速 *(CNBC)*

- **[2026-06-02]** [Microsoft Build 2026: Windows Platform Security for AI Agents 発表 — MXC (Microsoft Execution Containers) SDK・Agent 365 (Entra+Defender+Purview 統合エージェントガバナンス)・Windows 365 for Agents が GA](https://blogs.windows.com/windowsdeveloper/2026/06/02/windows-platform-security-for-ai-agents/) — エージェントが OS レベルのコンテナ分離と ID・DLP 制御下で動作する新アーキテクチャ；100+ エージェントが exploit チェーンを自律探索する multi-agent agentic security system も同日発表 *(Microsoft Developer Blog)*

- **[2026-06-02]** [Meta AI サポートボットが Instagram 著名ハンドル乗っ取りに悪用 — 攻撃者が AI チャットボットを欺いて攻撃者制御メールへのパスワードリセットリンクを取得、Obama ホワイトハウス・Sephora・宇宙軍 CMSgt アカウントを侵害](https://krebsonsecurity.com/2026/06/hackers-used-metas-ai-support-bot-to-seize-instagram-accounts/) — VPN で IP を詐称しジオブロックを回避；AI による human trust-and-safety チーム代替後の検証欠落が原因で Meta は翌日修正を発表 *(Krebs on Security / TechCrunch / 404Media)*

- **[2026-06-04]** [OWASP GenAI Security Project が Infosecurity Europe 2026 (本日) で GenAI Security Summit を開催 — Prompt Injection 対策・エージェントセキュリティ・EU AI Act 対応の規制フレームワークをライブ議論](https://genai.owasp.org/) — 世界各地のプロジェクトリーダー・規制当局が登壇；LLM Top 10 2026 版ドラフトも議論予定 *(OWASP)*

---

## セキュリティ関連ニュース

- **[2026-06-02]** [Kirki WordPress プラグイン CVE-2026-8206 (CVSS 9.8) が積極悪用中 — 非認証攻撃者が handle_forgot_password() の email 照合欠落を突き、管理者含む任意アカウントのパスワードリセットリンクを攻撃者メールに取得し完全乗っ取り; 500,000+ サイトに影響](https://www.bleepingcomputer.com/news/security/critical-kirki-flaw-exploited-to-hijack-wordpress-admin-accounts/) — Wordfence が 24 時間以内に 222+ 試行を検出；v6.0.7 で修正済み (2026-05-18 リリース済みだが 40% の利用者が旧バージョンのまま) *(BleepingComputer / Patchstack / Wordfence)*

- **[2026-06-02]** [DriveSurge: 新規 IAB 脅威アクターが数千サイトを侵害し ClickFix/FakeUpdates PPI モデルを運営 — zTDS 経由で偽ブラウザ更新・偽 CAPTCHA を配信し RAT・スティーラーを配布; 80+ injection ドメインを確認](https://www.silentpush.com/blog/drivesurge/) — 少なくとも 2025 年 9 月以降継続；Windows・macOS 双方を標的とし初期アクセスをダウンストリーム攻撃者に PPI で販売 *(Silent Push / Dark Reading / BleepingComputer)*

- **[2026-06-02]** [WeedHack マルウェアキャンペーンが 2026 年 1 月以降で 116,000+ Minecraft プレイヤーのシステムに感染 — 偽 Mod サイトを経由してバックドア・クレデンシャルスティーラーをサイレント配布](https://www.bleepingcomputer.com/news/security/over-116-000-minecraft-systems-infected-in-weedhack-malware-campaign/) — 複数のサードパーティ Mod 配布サイトが侵害されており、正規 Mod を装った実行ファイルが自動展開 *(BleepingComputer / Help Net Security)*

- **[2026-06-01/02]** [Dashlane がブルートフォース攻撃を開示 — 自動化ツールが TOTP 6 桁の全組み合わせを高速試行して 2FA を突破し、20 件未満のユーザーの暗号化ボルトを窃取](https://thehackernews.com/2026/06/dashlane-discloses-brute-force-attack.html) — 攻撃は 5/31 開始、大量試行検知によりアカウントを自動ロック；短命の数値 TOTP による MFA 実装の実用的脆弱点を露呈 *(The Hacker News / The Register / BleepingComputer)*

- **[2026-06-02]** [CISA が CVE-2022-0492 (Linux Kernel cgroups v1 特権昇格) を KEV に追加 — 2022 年修正後も未パッチの組み込みデバイス・レガシーサーバー・cgroups v1 コンテナホストで悪用が継続; 連邦機関修正期限 2026-06-05](https://www.cisa.gov/news-events/alerts/2026/06/02/cisa-adds-two-known-exploited-vulnerabilities-catalog) — cgroups v1 有効なコンテナホストでは非特権コンテナからホスト root 昇格のコンテナエスケープが成立 *(CISA)*

- **[2026-06-03]** [Samsung Exynos June 2026 セキュリティアドバイザリを公開 — Exynos 2400/2500/2600 および W1000 (ウェアラブル) に影響する 15 件の CVE を修正; 最高深刻度は DRM HDR ドライバの UAF (CVE-2026-23787)](https://www.sammyfans.com/2026/06/03/samsung-exynos-security-advisory-june-2026/) — CVE-2026-23790 (DMA バッファ double-free)・CVE-2026-33968 (TOCTOU→OOB)・CVE-2026-33970 (5G ベースバンド NULL deref) 等も含む *(Samsung Semiconductor / Sammy Fans)*

- **[2026-06-03]** [TechCrunch が「2026 年ワースト侵害」前半総括記事を公開 — Hasbro・Trivy/Bitwarden/Checkmarx OSS サプライチェーン攻撃・FBI サーベイランス侵害・OnlyFans 3.4 億件等、2026 年前半の主要インシデントと攻撃トレンドを整理](https://techcrunch.com/2026/06/03/the-worst-hacks-and-breaches-of-2026-so-far/) — 脆弱性エクスプロイトが資格情報窃取を抜いて最多侵害ベクターになったと分析 *(TechCrunch)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-02 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-8206 | Kirki WordPress Plugin 6.0.0〜6.0.6 (500K+ インストール) | CWE-640 / **9.8** | 非認証攻撃者がパスワードリセット REST API に任意メールアドレスを指定 → `handle_forgot_password()` がアカウント保有 email と照合せずリセットリンクを送信 → 管理者含む任意ユーザーアカウントの完全乗っ取り | [plugins.trac changeset 3530843](https://plugins.trac.wordpress.org/changeset/3530843/kirki) | **野外悪用中 (2026-06-02)** / CVSS 9.8 / 認証バイパス典型パターン / 同種 REST API エンドポイントを持つ WP プラグイン全般へのバリアントハント推奨 |
| CVE-2022-0492 | Linux Kernel (cgroups v1 有効・未パッチ環境・コンテナホスト) | CWE-287 / **7.8** | `cgroup_release_agent_write()` でアクセス制御欠落 → コンテナ内の非特権プロセスが release_agent パスを書き換え → cgroup 解放イベント発生時にホスト OS で root 権限コマンドを実行 → コンテナエスケープ | [kernel commit (2022)](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=3007098494197) (commit不明) | **KEV ✓ (2026-06-02 追加)** / 修正期限 2026-06-05 / 4 年後も実悪用継続 / cgroups v1 コンテナ運用環境は優先確認 |
| CVE-2026-44653 | LibreChat ≤ 0.8.3 (pip / AI チャットプラットフォーム) | CWE-201 / **6.5** | VIEW 権限ユーザーが `GET /api/mcp/servers` エンドポイントにアクセス → 管理者が設定した MCP サーバーの `apiKey.key`・`oauth.client_secret` が平文でレスポンスに含まれる → 低権限ユーザーが全 MCP API キーを窃取 | [LibreChat v0.8.4](https://github.com/danny-avila/LibreChat/releases/tag/v0.8.4) | 2026-06-02 公開 / AI チャットプラットフォームの MCP シークレット露出パターン / Flowise・Dify 等類似 OSS への水平伝播確認推奨 |
| CVE-2026-5509 | TP-Link Archer BE450/BE7200 v1 (firmware < 1.3.0 Build 20260416) | CWE-78 / CVSSv4 **8.5** | Web 管理 I/F がユーザー入力をバックエンドシェルコマンドにサニタイズなしで渡す → 認証済みの近接ネットワーク攻撃者が任意 OS コマンドを実行 | [TP-Link SA firmware 1.3.0](https://www.tp-link.com/us/press/security-advisory/) (commit 不明) | JVN 2026-06-02 公開 / 国内流通モデル / 隣接 SOHO ルーターへのバリアントハント推奨 |
| CVE-2026-23787 (Samsung Exynos SA 2026-06) | Samsung Exynos 2400/2500/2600、W1000 ウェアラブルチップ | CWE-416 / High | Exynos DRM HDR ドライバが解放済みカーネルメモリにアクセス (UAF) → カーネルクラッシュ・潜在的な特権昇格 | [Samsung Exynos Advisory June 2026](https://semiconductor.samsung.com/us/support/tools-resources/product-security/security-updates/) (commit 不明) | Samsung Exynos Advisory 2026-06-03 公開 / CVE-2026-23790 (double-free)・CVE-2026-33968 (TOCTOU)・CVE-2026-33970 (5G modem NULL deref) と同 SA の 15 CVE まとめて対応 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|---|---|---|---|---|
| 2026-06-02 | CVE-2026-5509 / JVN (2026-06-02) | TP-Link Archer BE450/BE7200 の Web 管理 I/F で OS コマンドインジェクション — 認証済み近接攻撃者が任意コマンド実行可能 | CVSSv4 8.5 (High) / 国内流通モデル / firmware 1.3.0 Build 20260416 で修正 | [DailyCVE DC-Jun2026-112](https://dailycve.com/tp-link-archer-be450-be7200-command-injection-cve-2026-5509-critical-dc-jun2026-112/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約30ソース (White House, CNBC, NPR, Sophos, Anthropic, Microsoft Developer Blog, Help Net Security, BleepingComputer, Krebs on Security, TechCrunch, Silent Push, Dark Reading, Patchstack, Wordfence, CISA, Samsung Semiconductor, Sammy Fans, OWASP, NVD, cvefeed.io, Threat-Modeling.com, TheHackerWire, SentinelOne, DailyCVE 他)
- 採用件数: AI=7 / Security=7 / CVE=5 / 国内=1
- 除外理由内訳:
  - 古すぎ (< 2026-06-02): CVE-2026-8501 Symantec PC Tools (6/1) / CVE-2026-8644 IBM WebSphere identity spoofing (6/1) / CVE-2026-9319 IBM WebSphere deserialization RCE (6/1) / Samsung SMR June 2026 公開 (6/1) / DARPA AI Forge RFI 投稿 (6/1) / Dutch Asocks botnet 17M devices takedown (5/28) / Forest Blizzard APT28 SOHO router DNS hijack (4/7) / AWS RES CVE-2026-5707/5708/5709 (4/6) / Mbed TLS CVE-2026-25833/25834 (4/1) / Crimson Collective Brightspeed breach (1/2026) / Cisco SD-WAN CVE-2026-20182 (5/15) / Oracle WebLogic CVE-2024-21182 KEV (6/1)
  - 重複 (excluded_set 直近7日): CVE-2025-48595 Android (06-03 digest) / Android June 2026 パッチ全体 (06-03) / DragonForce/Qilin 等ランサム 7 組織侵害 (06-03) / Operation Dragon Weave Azure C2 (06-03) / ICO AI 防衛 5 ステップ (06-03) / 23andMe California AG 訴訟 (06-03) / Nightmare Eclipse MSRC 撤回 (06-03) / CVE-2026-9311/9330 IBM WebSphere (06-03) / CVE-2026-47406/47408 praisonai (06-03) / Miasma npm @redhat-cloud-services (06-02) / CVE-2026-41089 Netlogon (06-02) / Casdoor SAML 4件 (06-02) / Anthropic IPO 申請 (06-02) / LLMShare (06-02) / Flowise CVE-2026-40933 (06-01) / GitLab CVE-2026-4868 (06-01) / CVE-2026-45697 Formie (05-31) / CVE-2026-0257 PAN-OS (05-31) / CIFSwitch (05-31) / CVE-2026-39987 Marimo (05-29) / Gogs 0-day (05-30) / Chrome CVE-2026-9872/9873 (05-30) / OpenAI Frontier Governance Framework (05-30) / Anthropic $965B (05-30) 他多数
  - 日付不明/確認不可: 各種記事は WebFetch 403 のためスニペット・複数メディア交差検証で日付を推定
- 取得失敗ソース (HTTP 403): whitehouse.gov (fact-sheets), cnbc.com, techcrunch.com, bleepingcomputer.com 個別記事, krebsonsecurity.com, silentpush.com, sophos.com blog, helpnetsecurity.com, anthropic.com/news, threat-modeling.com, securityweek.com, darkreading.com, sammyfans.com, CISA alerts 個別ページ, NVD detail pages
- 備考: Dashlane 攻撃の初報は 2026-06-01 (The Register/Help Net Security) だが The Hacker News の開示続報・Engadget 記事が 06-01/02 付けのため採用；Meta AI Instagram 乗っ取りは TechCrunch 06-01 初報に対しKrebs on Security・tech-ish.com が 06-02 付けで継続報道のため採用。CVE-2022-0492 は 2022 年原 CVE だが CISA KEV 追加日 2026-06-02 を採用基準日として採用

</details>
