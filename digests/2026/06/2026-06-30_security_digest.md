# KEDA Daily Digest — 2026-06-30 (JST)

> 採用範囲: 2026-06-28 〜 2026-06-30 (JST) | 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

SimpleHelp が OIDC JWT 署名未検証の CVSS 10.0 脆弱性 (CVE-2026-48558) を公開——CISA KEV に同日追加され約 14,000 台の公開サーバーへの緊急対応が必要; Oracle EBS (Payments モジュール) の CVE-2026-46817 (CVSS 9.8) が 5 月 CPU 公開後も未パッチ環境で Defused が 6 月 29 日に実環境悪用を確認。google/mcp-toolbox に Critical パストラバーサル (CVE-2026-11720、CVSS 9.3) が同日 GHSA 公開され、MCP インフラのサプライチェーンリスクが Amazon Q に続いて再び顕在化。AI 側では xAI Grok 4.5 (推定 1.5T パラメーター) がプライベートベータを開始、Google は Gemini 3.5 Pro GA を 7 月以降に延期。

---

## AI ニュース

- **[2026-06-28]** xAI **Grok 4.5** (推定 1.5T パラメーター、MoE アーキテクチャ) がプライベートベータ開始 — SpaceX・Tesla 社内テスター向けにロールアウト中; 数学・コーディング・長文コンテキストの強化が主眼とされ、パブリック公開日は未定 — TechTimes / The Verge / 9to5Mac *(2026-06-28〜29 UTC 複数ソース確認)*
- **[2026-06-29]** Google **Gemini 3.5 Pro** GA 公開を **7 月以降** に延期と複数メディアが報道 — 安全評価・多言語対応テストの追加実施が理由とされ、現行 Gemini 2.5 Pro との移行スケジュールが再調整 — TechRadar / VentureBeat *(2026-06-29 UTC 確認)*

---

## セキュリティニュース

- **[2026-06-29]** **SimpleHelp CVE-2026-48558** (CVSS 10.0) が CISA KEV に同日追加——OIDC JWT 署名を検証しないため攻撃者が自己署名トークンで正規 Technician セッションを偽造; 公開サーバー約 14,000 台が対象; ≤5.5.15 および 6.0-pre に影響、5.5.16/6.0-GA で修正 — BleepingComputer / SecurityWeek / CISA *(2026-06-29 UTC)*
- **[2026-06-29]** **Oracle EBS CVE-2026-46817** (Oracle Payments ファイル転送、CVSS 9.8) の実環境悪用を Defused が確認——5 月 CPU で修正済みだが未パッチ企業が標的に; 認証不要 HTTP リクエストで RCE; Oracle は 5 月パッチ適用を改めて強調 — Defused / SecurityAffairs / BleepingComputer *(2026-06-29 UTC)*
- **[2026-06-27]** Palo Alto Unit 42、**クラウドストレージ バケット乗っ取り攻撃 (Bucket Hijacking)** の詳細手法を公開——S3/GCS バケット名の再利用を狙い、削除済みバケットを同名で再登録して依存製品の update/asset 配信を差し替える; OSS CDN・静的配信全般へのサプライチェーン攻撃として警戒推奨 — Unit 42 Blog / The Register / SecurityWeek *(2026-06-27〜28 UTC)*

---

## CVE / 脆弱性情報

| CVE / GHSA | 製品 | CWE / CVSS | バグクラス (条件 + sink + 結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-48558 | SimpleHelp Remote Support (≤5.5.15 / 6.0-pre) | CWE-347 / **10.0** | OIDC 認証で JWT 署名検証を省略 → 攻撃者が自己署名トークンを生成し Technician セッションを確立 → 完全管理権限奪取 | SimpleHelp 5.5.16 / 6.0-GA | **CISA KEV 2026-06-29 追加** / 公開サーバー ~14,000 台 / 認証不要・ネットワーク到達のみで成立 |
| CVE-2026-46817 | Oracle E-Business Suite (Payments モジュール) 12.2.x (May 2026 CPU 未適用) | CWE-200 / **9.8** | Payments ファイル転送 API がリクエスト認証なしに受付 → 任意ファイル読み取り/書き込み → RCE | Oracle CPU 2026-05 パッチ (5 月適用済み環境は修正) | **Defused が 2026-06-29 に実環境悪用確認** / CVSS 9.8 / 未パッチ EBS 環境は即時パッチ適用 |
| CVE-2026-11720 / GHSA-vwxw-jrg6-9jxv | googleapis/mcp-toolbox (MCP Toolbox for Databases) < 0.6.1 | CWE-22 / **9.3** | HTTP ツールのユーザー指定パスパラメーターを `ResolveReference` で URL 結合 → `../` が正規化されてツールボックス外ホストへ SSRF → ツールボックス認証情報がリクエストヘッダーに付与されて転送 | [PR #3218 / v0.6.1](https://github.com/googleapis/mcp-toolbox/releases) | 2026-06-29 GHSA 公開 / Google 公式 MCP サーバー / Amazon Q MCP (CVE-2026-12957) に続く IDE×MCP サプライチェーン経路 / 他 MCP サーバーの URL 結合ロジックへバリアントハント推奨 |
| CVE-2026-56782 / GHSA-65p2-39gr-3m25 | Gorse 推薦システム (zhenghaoz/gorse) < v0.5.10 | CWE-306 / **9.3** | `admin_api_key` が空 (デフォルト) の場合 `/api/dump` と `/api/restore` エンドポイントが認証なしにアクセス可能 → DB 全件ダウンロード/上書きが非認証で実行可能 | [commit 19fdcbb / v0.5.10](https://github.com/zhenghaoz/gorse/releases) | 2026-06-29 GHSA 公開 / セキュアデフォルト欠如パターン / デフォルト設定のまま公開している Gorse インスタンスは即時 API キー設定を |
| CVE-2026-57955 / GHSA-h37r-3qfp-73w6 | SigNoz (signoz/signoz) ≤ v0.130.1 | CWE-89 / **8.3** | アラート履歴エンドポイントのルール ID パラメーターをサニタイズせず ClickHouse クエリに直接結合 → 任意 SQL 実行; `url()` 関数経由で SSRF も成立 | [v0.131.0](https://github.com/signoz/signoz/releases) | 2026-06-29 GHSA 公開 / 可観測性プラットフォームゆえ本番インフラの認証情報・ログが流出するリスク大 / ClickHouse 組み込み observability ツール全般へバリアントハント推奨 |
| CVE-2026-57951 + CVE-2026-57952 + CVE-2026-57953 | Mythic C2 Framework (its-a-feature/Mythic) < v3.3.3 | CWE-285 / HIGH (batch) | エージェント登録 API の 3 つのエンドポイントが HMAC 検証前にリクエストをルーティング → 未登録エージェントが認証済みオペレーター相当のコマンド発行権を取得 → C2 インフラ乗っ取り | [Mythic v3.3.3](https://github.com/its-a-feature/Mythic/releases) | 2026-06-29 GHSA 3 件同時公開 / Mythic は OSS ペンテスト C2 として広く利用 / Cobalt Strike・Havoc 等他 C2 の同パターンへバリアントハント推奨 |
| CVE-2026-56285 / GHSA-4m2j-2x3w-gg93 | Nitter (zedeus/nitter) コミット 44b2f096 以前 | CWE-918 / **7.7** | `/video` エンドポイントがハードコードされた HMAC 鍵で署名されたパス由来 URL を外部フェッチ → URL バリデーションなし → 非認証攻撃者が Nitter サーバーに任意ホストへの SSRF を発行可能 | [commit 44b2f096](https://github.com/zedeus/nitter/commit/44b2f096) | 2026-06-29 GHSA 公開 / Nitter セルフホスト事例多 / 同パターン (ハードコード HMAC + 外部フェッチ) へのバリアントハント推奨 |

---

## 国内脆弱性 / インシデント

> 直近2日間 (2026-06-28〜30 JST) に該当する新規国内脆弱性・インシデントは確認できませんでした。

*参考: KDDI 不正ログイン被害 (14.2M メール、2026-06-24 JST 公開) は採用窓外。Yokogawa CVE-2026-11833 (2026-06-25 アドバイザリ) は採用窓外。*

---

<details>
<summary>収集メタデータ / デバッグ情報</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| github.com/advisories (Jun 28-30 filter) | GHSA-vwxw (MCP Toolbox), GHSA-65p2 (Gorse), GHSA-h37r (SigNoz), GHSA-4m2j (Nitter), CVE-2026-57951/57952/57953 (Mythic C2) 取得 ✓ |
| cisa.gov/known-exploited-vulnerabilities-catalog | 403 → WebSearch 代替; CVE-2026-48558 (SimpleHelp) KEV 2026-06-29 追加 確認 ✓ |
| BleepingComputer / SecurityWeek (SimpleHelp CVE-2026-48558) | 2026-06-29 UTC 確認 ✓ |
| Defused / SecurityAffairs (Oracle EBS CVE-2026-46817) | 2026-06-29 UTC 悪用確認 ✓ |
| Unit 42 Blog / The Register (Bucket Hijacking) | 2026-06-27〜28 UTC 確認 ✓ |
| TechTimes / The Verge (Grok 4.5) | 2026-06-28〜29 UTC 確認 ✓ |
| TechRadar / VentureBeat (Gemini 3.5 Pro 延期) | 2026-06-29 UTC 確認 ✓ |
| thehackernews.com | 403 — WebSearch スニペットで代替 |
| unit42.paloaltonetworks.com | 403 — The Register / SecurityWeek で代替確認 |
| anthropic.com/news | 403 — WebSearch で代替確認 |

### 集計サマリ

- **AI ニュース**: 2 件 (週末明け・月曜日は発表ペース低調につき目安下限)
- **セキュリティニュース**: 3 件
- **CVE エントリ**: 7 件
- **国内インシデント**: 0 件
- **除外 (採用窓外)**: KDDI (Jun 24), Yokogawa CVE-2026-11833 (Jun 25), libssh2 CVE-2026-55200 (Jun 24)
- **重複除外 (excluded_set)**: Amazon Q CVE-2026-12957/-12958 (Jun 29 digest 掲載済み), Linux CVE-2026-46331 (Jun 29 掲載済み), pnpm batch (Jun 27/28 掲載済み), Cisco UCM CVE-2026-20230 (Jun 25 掲載済み), GPT-5.6 / Mythos 5 (Jun 27 掲載済み), Claude Code v2.1.195 (Jun 29 掲載済み)

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-06-23 〜 2026-06-29) の全 CVE/GHSA/URL を除外済み。*
