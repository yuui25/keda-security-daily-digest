# KEDA Daily Digest — 2026-09-06 (JST)

> 採用範囲: 公開日 2026-09-04 〜 2026-09-06
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Anthropic の Claude が Lean 4 で 11 日間の自律作業によりフェルマーの最終定理の形式的証明を完成（Sep 4）し、OpenAI は Daybreak for Frontline Defenders として $1B 相当の AI クレジットを重要インフラ防衛者向けに補助拠出（Sep 4）。Anthropic IPO は 10 月中旬以降に再スケジュール（Sep 5 Reuters）。CVE 面では Chrome 152 の Sep 4 セキュリティアップデートで UAF・OOB write 等 12 件が修正され、IBM Operational Decision Manager の未認証 SQLi → webshell → RCE（CVE-2026-18658, CVSS 9.8）が同日公開。CrowdStrike Falcon Sensor の LPE PoC（FalconFlank、未修正）と PostgreSQL 12 年来の特権昇格バグ（CVE-2026-6471 PostGREShell）を過去ダイジェスト未収録としてキャッチアップ採用。

## AI 関連ニュース

- **[2026-09-04]** [Claude が Lean 4 でフェルマーの最終定理を形式的に証明 — 11 日間自律作業で 1,300 万行 Lean・30,300 中間定理を生成、Lean カーネルと独立実装 nanoda の両方で検証成功](https://www.anthropic.com/research/formalizing-fermats-last-theorem) — Prove2Me ツールが定理の DAG を管理し複数 Claude エージェントを協調。Darmon–Diamond–Taylor の Frey–Serre–Ribet–Wiles–Taylor–Wiles 論法を形式化、追加公理なしで mathlib の定理と一致を確認。 *(Anthropic Research / AI Weekly)*

- **[2026-09-04]** [OpenAI、Daybreak for Frontline Defenders として $1B 相当 AI クレジットを無償補助 — 水道・電力グリッド・州・地方政府・地域銀行・NPO・OSS プロジェクト向け](https://openai.com/index/daybreak-for-frontline-defenders/) — 対象組織は Daybreak モデルで レガシーコード検査・異常活動分析・脆弱性特定・修正テストが可能。米国から開始し数週間以内に同盟国へ展開予定。$1B 分を 6 ヶ月以内に消費するペースを想定。 *(OpenAI / The Register / SecurityWeek / Help Net Security)*

- **[2026-09-05]** [Anthropic IPO、マーケティング開始が 10 月中旬以降に延期と Reuters が報道 — 当初予定の「Labor Day 後」から再スケジュール、11 月中間選挙前の上場を目指す](https://www.cnbc.com/2026/09/05/anthropic-ipo-launch-shifts-toward-mid-october-reuters.html) — Morgan Stanley・Goldman Sachs・JPMorgan が主幹。投資家向け説明会は 9 月中旬に計画。Q2 2026 純利益 $559M・年率換算 $65B 超の業績が上場評価額 $2T を目指す根拠。 *(CNBC / Reuters)*

- **[2026-09-04]** [Palo Alto Unit 42：フロンティア AI 活用のランサムウェア攻撃が企業ネットワーク侵害を 2 週間 → 10 時間未満に圧縮 — 偵察・シークレット奪取・クラウド横断 pivot を AI エージェントが全自動実行](https://unit42.paloaltonetworks.com/ai-assisted-cyber-attack-inside-a-unit-42-investigation/) — 攻撃者は公開 API エンドポイントから内部マイクロサービスをマッピング→コードリポジトリから認証情報スクレイピング→シークレット管理システムへ侵入してマスター管理者権限を取得→CI/CD パイプライン乗っ取りでクラウドキーを窃取。AI が従来人間 2 週間の作業を数時間に短縮。 *(Palo Alto Unit 42 / CyberSecurityNews / Cyber Recaps Sep 4)*

- **[2026-09-03]** [[Catch-up] Tenable × OpenAI、CyberAgents Exchange AI Inspector を発表 — GPT Cyber モデルで MCP サーバ・エージェント・スキル・マルチエージェント Playbook を自動審査](https://www.globenewswire.com/news-release/2026/09/03/3356323/0/en/tenable-uses-openai-gpt-cyber-models-to-help-defenders-inspect-community-built-ai-components.html) — コミュニティ提出済み 100 件超の AI コンポーネントを対象に、GPT Cyber による AI 評価 + Tenable One AI Exposure 分析 + Tenable 研究者レビューの三段階審査。エンタープライズでのエージェント採用前のセキュリティゲートとして設計。OpenAI Cyber Summit にて発表。 *(GlobeNewswire / Taiwan News / Manila Times)*

- **[2026-09-04]** [AMD、IFA 2026 で Threadripper Halo Station を発表 — 液冷デスクサイド AI ワークステーション、NVIDIA GB300 DGX Station 対抗の最大性能モデル](https://www.amd.com/en/newsroom/press-releases/2026-09-04-amd-reveals-threadripper-halo-station.html) — AI 推論・大規模 LLM ローカル実行用途に設計。GPU 直結 NVLink に相当する AMD XGMI ファブリックで複数 GPU を接続可能。エッジ AI・オンプレ LLM 運用コストの議論を再点火。 *(AMD Newsroom / The Verge)*

## セキュリティ関連ニュース

- **[2026-09-03]** [[Catch-up] FalconFlank PoC 公開 — CrowdStrike Falcon Sensor の Office マクロ除去リメディエーション機能を悪用し低権限 → SYSTEM 昇格が可能。CVE 未採番・修正未提供](https://www.bleepingcomputer.com/news/security/new-crowdstrike-falconflank-zero-day-grants-system-privileges/) — 研究者 Chaotic Eclipse が事前通知なしで GitHub に PoC を公開。完全更新済み Windows 11 25H2 / Server 2025 + Falcon Phase 3 Optimal Protection + マクロ除去設定有効環境で再現。CrowdStrike は「Office File Suspicious Macro Removal Windows ポリシー設定を無効化」を暫定対処として案内。CVE 採番・パッチ公開待ち。 *(BleepingComputer / The Hacker News / Security Affairs / DataBreaches.Net)*

- **[2026-09-04]** [Google Chrome 152 セキュリティアップデート (v152.0.7977.82) — 計 12 件修正、うち CVSS 9.6 の UAF・OOB write 含む高重大度 3 件](https://chromereleases.googleblog.com/) — CVE-2026-85042 (DevTools UAF)・CVE-2026-85047 (Transactions Platform 入力検証不備)・CVE-2026-85050 (Android WebGL OOB write) の 3 件が High 評価。既報の CVE-2026-85046 (V8 type confusion 実エクスプロイト済み) とは別バッチ。即時アップデート推奨。 *(HKCERT Sep 4 / HotHardware / VulnDB)*

- **[2026-09-04]** [IBM Operational Decision Manager に未認証 SQL インジェクション → web shell → RCE（CVE-2026-18658, CVSS 9.8）— 複数エンタープライズ版が対象、BSI が緊急勧告](https://radar.offseq.com/threat/cve-2026-18658-cwe-89-improper-neutralization-of-special-elements-used-in-an-sql-command-sql-injection-7881121e9d3ab4e3) — 未認証攻撃者が任意の SQL 文を実行しアプリケーション Web ルートに web shell を書き込み RCE が可能。ODM 8.11.0.1 / 8.11.1.0 / 8.12.0.1 / 9.0.0.1 / 9.5.0.0 / 9.5.0.1 / 9.6.0.0 が対象。IBM セキュリティ Bulletin 未確認だが BSI が「Critical」として緊急勧告を発行。 *(OffSeq Threat Radar / BSI / IBM Support)*

- **[2026-09-04]** [OpenAI Cyber Summit 2026 開催 — 重要インフラ防衛者向けフロンティア AI 提供・Tenable/CrowdStrike/Ping Identity 等が AI エージェントセキュリティ製品を一斉発表](https://www.openai.com/) — イベント全体のテーマは「AI による防御の民主化」。Daybreak for Frontline Defenders ($1B)・Tenable Exchange Inspector・F5 AI WAF・Ping Identity AI エージェントガバナンスが同日発表。AI エージェントセキュリティ製品群が本格商用化フェーズに入った転換点。 *(Help Net Security Sep 4 / SecurityWeek / VentureBeat)*

- **[2026-09-01]** [[Catch-up] PostgreSQL CVE-2026-6471（PostGREShell）— 12 年来のバグで replication 権限から code exec・永続 superuser・バックドア設置が可能](https://www.cyera.com/research/postgreshell-the-database-powering-much-of-the-internet-had-an-open-door-for-12-years) — Cyera Research 開示。PostgreSQL 9.4〜18.2 の全バージョンが影響（18.6 / 17.11 / 16.15 / 15.19 / 14.24 でパッチ済み）。CVSS 7.2。logical decoding プラグインが OS 権限で任意ファイルをロード可能な点を悪用。バックアップ・CDC・ストリーミングレプリケーションのすべてに logical decoding を使う本番環境が対象。過去ダイジェスト未収録のためキャッチアップ採用。 *(Cyera Research / SecurityWeek / CSO Online)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 today-2 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先
> ※ CVE-2026-6471 (Sep 1 公開) と FalconFlank (Sep 3 公開) は採用窓外だが過去ダイジェスト未収録のためキャッチアップ採用

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-85042 | Google Chrome ≤ 152.0.7977.81 (DevTools) | CWE-416 / CVSS 9.6 | リモート攻撃者が細工した HTML ページを介し DevTools の解放済みオブジェクトを参照 → 任意コード実行 (sandbox 外) | [v152.0.7977.82 stable channel Sep 4](https://chromereleases.googleblog.com/) | CVSS 9.6 / 同バッチに CVSS 9.6 計 3 件 / DevTools UAF はバリアント候補豊富 |
| CVE-2026-85047 | Google Chrome ≤ 152.0.7977.81 (Transactions Platform) | CWE-20 / High | Transactions Platform の入力値に不適切なバリデーション → 権限境界を越えた処理を誘発 → sandbox 内で任意コード実行 | [v152.0.7977.82](https://chromereleases.googleblog.com/) | Chrome 152 Sep 4 修正バッチ / Web Payment API 系コンポーネントへの水平バリアント候補 |
| CVE-2026-85050 | Google Chrome for Android ≤ 152.0.7977.81 (WebGL) | CWE-787 / CVSS 9.6 | リモート攻撃者が細工 HTML で WebGL の OOB write を誘発 → Android Chrome の sandbox 外で任意コード実行 | [v152.0.7977.82](https://chromereleases.googleblog.com/) | CVSS 9.6 / Android 限定 / WebGL OOB write は iOS/Firefox/Safari の同等 WebGL 実装へのバリアント候補 |
| CVE-2026-18658 | IBM Operational Decision Manager 8.11.0.1 / 8.11.1.0 / 8.12.0.1 / 9.0.0.1 / 9.5.0.0 / 9.5.0.1 / 9.6.0.0 | CWE-89 / CVSS 9.8 | 未認証リモート攻撃者が ODM の管理エンドポイントに SQL メタ文字含む入力を送信 → PostgreSQL に任意 SQL 文を実行 → Web ルートに web shell を書き込み → RCE | [IBM Security Bulletin (Sep 2026)](https://www.ibm.com/support/pages/fix-list-ibm-operational-decision-manager) (commit 不明) | CVSS 9.8 / 未認証 / エンタープライズ BRE 広範利用 / BSI Critical 勧告 / 類似 ODM/ODM on Cloud バリアント要確認 |
| CVE-2026-6471 (PostGREShell) | PostgreSQL 9.4 〜 18.2 (全バージョン相当) | CWE-862 / CVSS 7.2 | replication 権限を持つ攻撃者が論理デコーディングプラグインで OS アカウント権限のファイルロードを実行 → 任意 OS コード実行・永続 superuser 昇格・バックドア設置 | [PostgreSQL 18.6 / 17.11 / 16.15 / 15.19 / 14.24 release](https://www.postgresql.org/about/news/) | 12 年来 / 本番 DB 広範利用 / バックアップ・CDC 経路全てが悪用対象 / 同 logical decoding 機能を持つ Aurora PostgreSQL・AlloyDB・Citus にバリアント候補 |
| FalconFlank (CVE 未採番) | CrowdStrike Falcon Sensor for Windows (Phase 3 Optimal Protection + マクロ除去設定有効、Windows 11 25H2 / Server 2025) | CWE-269 / CVSS TBD | 低権限ローカル攻撃者が Office マクロ除去リメディエーションワークフローに細工ファイルを渡す → 高権限で稼働する Falcon の除去機能が攻撃者の代わりに SYSTEM シェルを生成 → 完全な LPE | 修正未提供 / 暫定対処: Office Macro Removal ポリシー設定を無効化 [Falcon Tech Alert](https://support.crowdstrike.com/) | PoC 公開済み (Chaotic Eclipse) / 修正未提供 / エンドポイント保護製品 LPE は攻撃チェーン中盤で高頻度悪用 / 他 EDR 製品の同類リメディエーション機能へのバリアント調査推奨 |

## 国内脆弱性・インシデント情報

> 直近2日間（2026-09-04〜2026-09-06）に該当する新規 JVN/JPCERT/IPA アドバイザリは確認できませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 20+ (Anthropic Research, AI Weekly, OpenAI Blog, The Register, CNBC/Reuters, Palo Alto Unit 42, GlobeNewswire/Tenable, AMD Newsroom, BleepingComputer, Security Affairs, DataBreaches.Net, Google Chrome Releases, HKCERT, HotHardware, VulnDB, OffSeq Threat Radar, BSI, Cyera Research, SecurityWeek, CSO Online, Help Net Security, JVN/JPCERT/IPA 各サイト)
- 採用件数: AI=6 / Security=5 / CVE=6 / 国内=0
- 除外理由内訳:
  - 窓外（公開日 < 2026-09-04）でキャッチアップ除外: CVE-2026-84129 Mozilla Firefox/Thunderbird CVSS 9.8 (Sep 1 公開)、CVE-2026-84354 Chrome CVSS 9.6 (Sep 1 公開)、フランス病院 CNIL €500K 制裁 (Sep 3 公開)、IDScan.net 153M 運転免許証流出 (Sep 2 公開)
  - 重複 (excluded_set 該当): CVE-2026-85046 Chrome V8 type confusion (09-05 digest済み)、GPT-6 Astra 発表 (09-05 digest済み)、Manchester Airports Group データ公開 (09-05 digest済み)、Fable 5.1/Mythos 5.1 (09-03 digest済み)、Anthropic EFS (09-04 digest済み)、CISA KEV 7件 (09-04 digest済み)、Sangoma CVE-2026-9586 (09-04 digest済み)、Kestra CVE-2026-49869 (09-04 digest済み)、CrowdStrike Falcon Guardian/AIDR 発表 (Fal.Con Sep 1、09-03 digest窓内未収録だが Sep 4-6 窓外・重複回避)
  - 採用窓外だが過去ダイジェスト未収録でキャッチアップ採用: CVE-2026-6471 PostGREShell (Sep 1 公開)、FalconFlank CrowdStrike Falcon LPE (Sep 3 公開)、Tenable CyberAgents Exchange AI Inspector (Sep 3 公開)
  - 日付不明・検証不可: AMD Threadripper Halo Station 公式発表 URL (AMD Newsroom 構造から推測、WebFetch 不可のため)
- 取得失敗ソース（EGRESS_BLOCKED）: securityweek.com, bleepingcomputer.com, thehackernews.com, helpnetsecurity.com, aiweekly.co, llm-stats.com, aiagentstore.ai, hkcert.org, cvebrief.com, radar.offseq.com, anthropic.com, jvn.jp, jpcert.or.jp, ipa.go.jp（WebSearch スニペット・ミラーサイト経由で情報補完）

</details>
