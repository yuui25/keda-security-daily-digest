# KEDA Daily Digest — 2026-05-19 (JST)

> 採用記事の公開日範囲: 2026-05-17〜2026-05-19  
> 直近7日分のダイジェストと照合し重複を除外済み

---

## AI関連ニュース

### 1. Google I/O 2026 開幕 — Gemini 4.0/Omni・Gemini Spark・Android XR グラスをキーノートで発表予定
**公開日**: 2026-05-19  
**ソース**: Android Central / AIxploria / Yahoo Tech

Google I/O 2026 が米太平洋時間 5月19日（火）午前10時（日本時間 5月20日 02:00）に開幕する。現地時間のキーノートは本ダイジェスト生成後のため確定内容は未反映だが、直前リーク・招待状・開発者ドキュメントから以下の発表が有力視される。

- **Gemini 4.0 / Gemini Omni**: テキスト・画像・音声・動画を単一コンテキストで処理する統合マルチモーダルモデル。従来の Gemini 1.5/2.0 系から世代が刷新。
- **Gemini Spark エージェント**: 長時間タスクを自律的にこなす「エージェント実行基盤」として Gemini Studio / Vertex AI に統合予定。コード実行・Web アクセス・外部 API 連携を組み合わせたマルチステップワークフローをノーコードで構築可能とされる。
- **Android XR グラス（実機デモ）**: Samsung と共同開発の拡張現実グラスを初の実機デモ公開。Android 17 の空間 UI と連携。
- **Aluminium OS / Googlebook**: Chromebook 系 OS のリブランド。Web・ネイティブアプリのシームレス統合を標榜。

キーノート後は公式ブログ・YouTube ストリームで詳細が順次公開される予定。

---

### 2. OpenAI × Dell Technologies — Codex をオンプレ・ハイブリッド企業環境に展開するパートナーシップ発表
**公開日**: 2026-05-18  
**ソース**: OpenAI Blog / Business Wire (リリース番号 20260518066830)

Dell Technologies World 2026（ラスベガス）にあわせ、OpenAI と Dell Technologies がエンタープライズ向けパートナーシップを発表した。

- **概要**: OpenAI Codex をオンプレミスおよびハイブリッドクラウド環境へ展開できる「Dell AI Data Platform」との統合。企業内コードベース・技術ドキュメント・社内ナレッジベースを Codex のコンテキストとして利用可能にする。
- **背景**: クラウドへのデータ送出を避けたいデータ主権要件を持つ金融・製造・公共セクターを主な対象とする。OpenAI のオンプレミス展開戦略（Microsoft Azure Arc との競合軸でも注目）の一環。

---

### 3. Synack 2026 State of Vulnerabilities Report — AI が CVE 悪用ウィンドウを平均10時間まで圧縮
**公開日**: 2026-05-18  
**ソース**: Help Net Security (/2026/05/18/)

Synack が公開した年次レポートの主要指標。

- 2025年の CVE 公開総数: **48,244件**（前年比 +20%）
- 高重大度（CVSS 7.0 以上）の脆弱性: 前年比 **+10%**
- RCE（リモートコード実行）脆弱性: 前年比 **+39%**
- **AI 支援による悪用ウィンドウ短縮**: 開示から実証コード（PoC）生成・初期スキャン開始まで平均 **10時間** に短縮（前年比大幅短縮）。パッチ適用よりも早く攻撃者が動ける状況が常態化しつつあるとレポートは警告。

---

## セキュリティ関連ニュース

### 1. Windows MiniPlasma ゼロデイ PoC 公開 — cldflt.sys の権限昇格でフルパッチ済み Windows 11 が SYSTEM に
**公開日**: 2026-05-17  
**ソース**: BleepingComputer (/2026/05/17/)

セキュリティ研究者 Nightmare-Eclipse（別名 Chaotic Eclipse）が GitHub で **Windows Cloud Filter ドライバー（cldflt.sys）** の権限昇格脆弱性 PoC を公開した。

- **影響範囲**: 2026年5月のパッチをすべて適用したフルパッチ済み Windows 11 で動作確認済み。CVE 番号は未割当、マイクロソフト公式パッチなし（ゼロデイ）。
- **攻撃手法**: cldflt.sys の競合状態を突いて SYSTEM 権限を取得。ローカル一般ユーザーがカーネルレベルの権限昇格に成功する。
- **現状**: マイクロソフトへの事前通知有無は公表されていない。セキュリティコミュニティはランサムウェア・APT による悪用を警戒しており、監視・EDR ルールの更新を推奨している。

---

### 2. MCP ツールチェーンで DNS リバインディング/クレデンシャル漏洩の GHSA が連続公開
**公開日**: 2026-05-18  
**ソース**: GitHub Advisory Database (GHSA-jxx9-px88-pj69, GHSA-fvh2-gm75-j4j7)

Model Context Protocol（MCP）関連パッケージで重大度の高いセキュリティ勧告が同日公開された。

- **n8n-mcp（CVE-2026-45707, CVSS 8.1）**: マルチテナント環境でリクエストヘッダー `x-n8n-url` / `x-n8n-key` が欠落した場合に、プロセスレベルの環境変数 `N8N_API_URL` / `N8N_API_KEY` に無認証でフォールバックするため、テナント越境アクセスが可能。v2.51.1 以前に影響、v2.52.0 以降で修正。
- **dynoxide（GHSA-fvh2-gm75-j4j7, CVSS 7.5）**: MCP HTTP トランスポートが `Host` ヘッダーを検証しないため DNS リバインディングが成立。攻撃者はブラウザ経由でローカル MCP サーバーに CSRF/CORS バイパスリクエストを送信できる。v0.9.13 で修正。

MCP エコシステムはまだ成熟しておらず、ホスト検証・テナント分離の実装が後回しにされがちであることがあらためて示された。ローカル・クラウド問わず MCP サーバーを運用する組織は依存パッケージの GHSA を継続監視することが求められる。

---

## 国内脆弱性・インシデント情報

> 直近2日間に該当する新規ニュースは確認できませんでした。

---

## 新規 CVE / 脆弱性情報

| CVE / GHSA | 製品・バージョン | CWE / CVSS | バグクラス | 修正コミット / リリース | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-45707 / GHSA-jxx9-px88-pj69 | n8n-mcp ≤ 2.51.1 | CWE-287 / 8.1 | マルチテナント環境で `x-n8n-url`/`x-n8n-key` ヘッダー欠落時にプロセスレベル N8N_API_URL/KEY へ無認証フォールバック → テナント越境アクセス | [853015d](https://github.com/czlonkowski/n8n-mcp/commit/853015d0897be7cf2d9d4726de195c938e4395ab) | MCP 利用組織は即時更新 |
| GHSA-fvh2-gm75-j4j7 | dynoxide 0.9.3–0.9.12 | CWE-346 / 7.5 | MCP HTTP トランスポートが Host ヘッダーを検証しないため DNS リバインディング → ブラウザ経由でローカル MCP サーバーへ CSRF/CORS バイパス | v0.9.13 リリース (commit 不明) | ローカル MCP 運用組織は更新 |
| CVE-2026-45149 / GHSA-jxxr-4gwj-5jf2 | brace-expansion ≥ 5.0.0, < 5.0.6 | CWE-400 / 6.5 | `{1..10000000}` 等の大きな数値範囲で max チェック前に全要素を生成 → ~505MB メモリ消費・~800ms で DoS | [c0b095b](https://github.com/juliangruber/brace-expansion/commit/c0b095bdc52bc4c36dc88deddbadabc49f8371e5) | Node.js エコシステム広範に影響 |
| CVE-2026-6402 / GHSA-79cf-xcqc-c78w | webpack-dev-server ≤ 5.2.3 | CWE-346 / 5.3 | 非 HTTPS オリジンで `<script>` タグによるクロスオリジンリクエストを許可 → モジュールソースコードを外部に窃取可能 | fix: CORP: same-origin ヘッダー追加 (commit 不明) | 開発環境限定・本番影響なし |

---

## 本日のサマリ

- **Google I/O 2026 開幕**: 本稿生成時点でキーノートは未開始。Gemini 4.0/Omni・Gemini Spark エージェント・Android XR グラスという三本柱が年内最大の AI 発表週を飾る見込み。日本時間 5月20日 02:00 以降の公式発表に注目。
- **MCP セキュリティの死角**: n8n-mcp と dynoxide の GHSA が同日公開され、MCP エコシステムにおけるテナント分離・Host 検証の欠如が改めて浮き彫りに。AI エージェント基盤を運用する組織は依存関係の GHSA 監視体制の整備が急務。
- **Windows ゼロデイ（MiniPlasma）**: パッチなし・CVE 未割当の権限昇格 PoC がフルパッチ済み環境で動作確認済み。EDR ルール更新と異常な cldflt.sys アクセスの監視を即時推奨。

---

<details>
<summary>🔍 Debug: 情報収集メタデータ</summary>

### 収集・除外ステータス

| カテゴリ | 検索クエリ数 | 採用記事数 | 除外記事数（重複/期間外） |
|---|---|---|---|
| AI関連 | 10 | 3 | 14 |
| セキュリティ | 11 | 2 | 7 |
| 国内脆弱性・インシデント | 5 | 0 | 3 |
| CVE / GHSA | 8 | 4 | 6 |

### 採用記事と確認済み公開日

| タイトル（要約） | 公開日 | 確認方法 |
|---|---|---|
| Google I/O 2026 開幕・キーノートプレビュー | 2026-05-19 | Android Central URL パス `/20260519/` + snippet |
| OpenAI × Dell Technologies Codex オンプレ展開 | 2026-05-18 | Business Wire リリース番号 20260518066830 |
| Synack 2026 State of Vulnerabilities Report | 2026-05-18 | Help Net Security URL `/2026/05/18/` + snippet |
| Windows MiniPlasma PoC (cldflt.sys LPE) | 2026-05-17 | BleepingComputer URL `/2026/05/17/` + snippet |
| MCP n8n-mcp CVE-2026-45707 GHSA 公開 | 2026-05-18 | GitHub Advisory Database GHSA-jxx9-px88-pj69 公開日 |
| MCP dynoxide GHSA-fvh2-gm75-j4j7 公開 | 2026-05-18 | GitHub Advisory Database GHSA-fvh2-gm75-j4j7 公開日 |
| brace-expansion CVE-2026-45149 | 2026-05-18 | GHSA-jxxr-4gwj-5jf2 公開日 |
| webpack-dev-server CVE-2026-6402 | 2026-05-17 | GHSA-79cf-xcqc-c78w 公開日 |

### 主な除外理由

- **期間外（before 2026-05-17）**: Budibase CVEs (GHSA 公開 2026-05-12〜15), Ivanti EPMM CVE-2026-6973 (May 7), Grafana Pwn Request (May 16 → 05-18 ダイジェスト収録済), CVE-2026-42897 (May 15-16 → 05-17/05-18 ダイジェスト収録済)
- **直近7日重複（前ダイジェスト収録済み）**: Google I/O 前夜プレビュー (05-18 ダイジェスト), Grafana GitHub Actions 侵害 (05-18 ダイジェスト), 能動的サイバー防御法 施行準備 (05-18 ダイジェスト), Pwn2Own Berlin 全日程 (05-16/05-17 ダイジェスト), Turla/Kazuar P2P botnet (05-17 ダイジェスト), Cisco CVE-2026-20182 (05-16 ダイジェスト)
- **日付未確認 / 情報不足**: AIToolsRecap "OpenAI one app" (May 17, 二次確認不可), TechRadar "Gemini Remy" (独立検証不可), 複数セキュリティブログ (403 / パラフレーズのみ)

### WebFetch 可用性メモ

bleepingcomputer.com, thehackernews.com, securityweek.com, anthropic.com, helpnetsecurity.com, jvn.jp, androidcentral.com, letsdatascience.com — いずれも HTTP 403 Forbidden。日付確認は URL パスパターン・Business Wire タイムスタンプ・GitHub Advisory Database の公開日フィールドで実施。

</details>
