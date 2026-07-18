# KEDA Security Daily Digest — 2026-07-19

> 採用範囲: 2026-07-17〜2026-07-19 JST に公開された情報のみ掲載。過去 7 日分との重複を除外 ([続報] 表記を除く)。

---

## 本日のサマリ

WordPress に REST API バッチルート混乱 + SQL インジェクションを連鎖させた pre-auth RCE チェーン (CVE-2026-63030 / CVE-2026-60137) が公開され PoC が GitHub に出回っている。同日、Go 製ボットネット **NadMesh** が ComfyUI・Ollama・n8n など AI/MCP サービスの 20 種超の既知 RCE を組み合わせて 3,811 件の AWS アクセスキーを詐取したとして研究者が警告。AI 推論フレームワーク SGLang では CVSS 9.8 の未認証 Pickle デシリアライズ RCE (CVE-2026-3059) が未パッチのまま公開され JVNVU が勧告。米国では ShinyHunters グループが vishing → Entra ID SSO 侵害の手口で Abbott Laboratories と Exact Sciences の患者・従業員データを窃取した。

---

## AI 関連ニュース

1. [2026-07-17] Go 製ボットネット **NadMesh** が AI/MCP サービス 20 種超の RCE を悪用 — ComfyUI (CVE-2026-59125)・Ollama・n8n・Langflow・Gradio 等を標的に 3,811 件の AWS アクセスキーを窃取、暗号資産マイナー常駐化と横移動スクリプトを配布。([THN](https://thehackernews.com/) / GBHackers / QiAnXin XLab)

2. [2026-07-17] Microsoft が AI 脅威インテリジェンス統合プラットフォーム **Project Perception** を発表 — LLM・エージェント・MCP ツール呼出しのリアルタイム異常検知と MITRE ATLAS マッピングを一元化、Security Copilot と統合予定。([The Information](https://www.theinformation.com/) / TechRepublic)

3. [2026-07-17] **SGLang** の ZMQ ブローカーが `tcp://*:5557` に無認証バインド — Pickle シリアライズされたメッセージを認証なしに受け入れ任意コード実行が可能 (CVE-2026-3059 CVSS 9.8)、CERT/CC が緊急勧告、修正バージョン未リリース。([Orca Security](https://orca.security/) / CERT/CC / JVNVU#90968686)

---

## セキュリティ関連ニュース

1. [2026-07-17] **ViteVenom / ChainVeil** — 7 件の悪意ある `@vitejs/*` npm パッケージが 4 層ブロックチェーン C2 インフラを介して RAT を配布 — Ethereum スマートコントラクトにコマンドを格納し従来の URL ブロックを回避、Checkmarx が発見・npm への報告後 72 時間以内に削除済み。([THN](https://thehackernews.com/) / Checkmarx)

2. [2026-07-17] **WordPress** が REST API バッチルート混乱 + SQLi の pre-auth RCE チェーン (CVE-2026-63030 + CVE-2026-60137) を緊急修正 — 6.9.5 / 7.0.2 / 6.8.6 を同時リリース、GitHub に PoC 出回り即時パッチ必須、全サイトの約 43% が WordPress 利用のため広範な影響。([THN](https://thehackernews.com/) / Rapid7 / Searchlight Cyber)

3. [2026-07-18] **ShinyHunters** が vishing → Entra ID SSO 侵害で Abbott Laboratories と Exact Sciences を侵害 — 攻撃者が IT ヘルプデスクを装い多要素認証をソーシャルエンジニアリングで突破、患者記録・従業員個人情報が漏洩、Experian 24 ヶ月モニタリングを提供。([BleepingComputer](https://www.bleepingcomputer.com/) / CyberNews)

---

## 新規 CVE / Advisory

| CVE/GHSA | 製品・バージョン | CWE / CVSS | バグクラス (条件→シンク→結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-63030 / GHSA-ff9f-jf42-662q | WordPress Core <6.9.5 / <7.0.2 / <6.8.6 | CWE-918+89 / **9.8** | 未認証攻撃者が `/wp-json/batch/v1` バッチエンドポイントに細工リクエストを送信 → ルーティング検証を回避して内部 REST ルートを呼出し → SQL インジェクションで任意クエリ実行・RCE | WordPress 6.9.5 / 7.0.2 / 6.8.6 | 2026-07-17 公開 / PoC 公開済み (GitHub) / 全 WordPress の約 43% 影響 |
| CVE-2026-60137 | WordPress Core <6.9.5 / <7.0.2 / <6.8.6 | CWE-89 / **9.8** | 認証済みユーザー (Subscriber 以上) が特定の投稿メタデータフィールドに細工値を挿入 → WP_Query が非サニタイズ値を SQL に連結 → データベース全内容の読取・改ざん | WordPress 6.9.5 / 7.0.2 / 6.8.6 | 2026-07-17 公開 / CVE-2026-63030 との連鎖で pre-auth RCE に昇格 |
| CVE-2026-3059 / GHSA-rgq9-fqf5-fv58 | SGLang ≤0.4.9 (pip: sglang) | CWE-502 / **9.8** | 未認証攻撃者が ZMQ ブローカー (tcp://*:5557) に Pickle ペイロードを送信 → 認証・検証なしにデシリアライズ実行 → サーバー上で任意コード実行 | 未パッチ (Orca Security 開示 2026-07-17) | **CERT/CC VU#885548 / JVNVU#90968686 勧告** / CVSS 9.8 / 未パッチ / AI 推論フレームワーク広範利用 |
| CVE-2026-3060 | SGLang ≤0.4.9 (Encoder Parallel モード) | CWE-502 / **9.8** | Encoder Parallel デプロイ時の同一 ZMQ ブローカー未認証バインド → Pickle デシリアライズ RCE (CVE-2026-3059 と同コンポーネント・別攻撃パス) | 未パッチ (Orca Security 2026-07-17) | CVE-2026-3059 と併用で全 SGLang デプロイメントを網羅 / クラスター構成で影響拡大 |

---

## 国内脆弱性・インシデント

| 日付 | 組織・製品 | 概要 | 影響度 | 参照 |
|---|---|---|---|---|
| 2026-07-17 | SGLang (AI 推論フレームワーク) | JVNVU#90968686 — SGLang ZMQ ブローカーの未認証 Pickle デシリアライズ RCE (CVE-2026-3059/3060 CVSS 9.8) を JPCERT/CC が国内向け勧告。修正バージョン未リリース、回避策 (ZMQ ポートのファイアウォール制限) を推奨。 | 影響大 / 国内 AI 推論環境全般 | [JVNVU#90968686](https://jvn.jp/vu/JVNVU90968686/) / CERT/CC VU#885548 |
| 2026-07-17 | HTTP/2 実装複数 (NGINX / Apache / IIS / Envoy 等) | JVNVU#90338324 (VU#885548) — HTTP/2 ストールフロー制御 DoS: サーバーが WINDOW_UPDATE フレームなしにデータ送信を継続 → 接続が永遠にストール → サービス不能。RFC 9113 準拠実装に広範影響、各ベンダー対応中。 | 影響中 / Web サーバー全般 | [JVNVU#90338324](https://jvn.jp/vu/JVNVU90338324/) / [CERT/CC VU#885548](https://kb.cert.org/vuls/id/885548) |

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| THN / GBHackers / QiAnXin XLab (NadMesh AI/MCP ボットネット) | 2026-07-17 公開確認 ✓ |
| The Information / TechRepublic (Microsoft Project Perception) | 2026-07-17 発表確認 ✓ |
| Orca Security / CERT/CC / JVNVU#90968686 (SGLang ZMQ Pickle RCE) | 2026-07-17 開示確認 ✓ |
| THN / Checkmarx (ViteVenom / ChainVeil npm supply chain) | 2026-07-17 公開確認 ✓ |
| THN / Rapid7 / Searchlight Cyber (WordPress wp2shell pre-auth RCE) | 2026-07-17 公開確認 ✓ |
| BleepingComputer / CyberNews (Abbott / Exact Sciences ShinyHunters breach) | 2026-07-18 公開確認 ✓ |
| GitHub Advisories (GHSA-ff9f-jf42-662q / CVE-2026-63030 WordPress) | 2026-07-17 公開確認 ✓ |
| GitHub Advisories (GHSA-rgq9-fqf5-fv58 / CVE-2026-3059 SGLang) | 2026-07-17 公開確認 ✓ |
| jvn.jp (JVNVU#90968686 / JVNVU#90338324) | 2026-07-17 公開確認 ✓ |
| thehackernews.com / bleepingcomputer.com | 403 — WebSearch スニペットで代替 |
| nvd.nist.gov | 403 — WebSearch スニペット代替 |
| helpnetsecurity.com | 403 — WebSearch スニペット代替 |

### 集計サマリ

- **巡回ソース数**: 約 20
- **採用件数**: AI=3 / Security=3 / CVE=4 / 国内=2
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-07-17 より前): UAT-11795 Starland RAT (Talos 2026-07-16) / Suno AI breach (TechCrunch/404 Media 2026-07-15) / TSMC Q2 earnings (2026-07-16) / Adobe ColdFusion CVE-2026-48282 KEV (2026-07-07) / CVE-2026-22778 vLLM RCE (2026-02-02) / NSA MCP hardening (2026-05-20) / Claude Sonnet 5 (2026-06-30) / GhostLock CVE-2026-43499 (2026-07-08〜10)
  - 重複 (直近 7 ダイジェスト掲載済み・excluded_set 参照): CVE-2026-39808/25089 (FortiSandbox KEV, 07-18掲載) / CVE-2026-62241/62386 (clawvet/grav, 07-18掲載) / CVE-2026-53412 (Zoom, 07-17掲載) / CVE-2026-46817 (Oracle EBS, 07-17掲載) / LegacyHive Windows ProfSvc (07-17掲載) / CVE-2026-58644 (SharePoint RCE, 07-16/17掲載) / CVE-2026-57092 (VMSwitch, 07-16掲載) / CVE-2026-15409/15410 (SonicWall, 07-16掲載) / CVE-2026-56155 (ADFS, 07-15掲載)

### 主要除外補足

- **CVE-2026-59125 (ComfyUI)**: NadMesh 項目内で既知 RCE の例示として言及済みだが NadMesh 自体は 07-19 掲載。CVE 単体は 07-11 以前の開示のため CVE テーブルへの独立掲載は除外。
- **HTTP/2 Bomb CVE-2026-49975**: June 公開済み (07-15 digest 窓内に含まれる可能性) → JVNVU#90338324 (stalled flow-control) は別の勧告として 07-17 に新規公開されたため採用。
- **Abbott / Exact Sciences breach**: BleepingComputer 初報 2026-07-18 確認 → 採用窓内。

</details>

---

*生成: keda-digest-bot / 2026-07-19 05:04 JST*
