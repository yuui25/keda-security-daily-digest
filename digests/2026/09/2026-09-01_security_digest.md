# KEDA Daily Digest — 2026-09-01 (JST)

> 採用範囲: 公開日 2026-08-30 〜 2026-09-01
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

採用窓（2026-08-30〜09-01）は直前期間と比べてニュース密度が低く、注目案件の多くが窓外と確認されたため除外した（GitLab CVE-2026-19478 は 8/17 開示・8/21 悪用報告、Microsoft Entra ID CVSS 10.0 RCE は 8/20 開示）。セキュリティ面では中国系 UNC3886 (FireAnt) が Cisco IOS XR・TACACS・Linux ホストを横断する高度な長期潜伏キャンペーンを Sygnia が公開（8/30）し、Kaspersky が Silver Fox による ValleyRAT の署名済み中国製壁紙アプリ (QN Wallpaper) 経由 DLL サイドローディング配布を報告（8/31）した。CVE では AshSqlite の JSONPath インジェクション (GHSA-2m69-gcr7-jv3q)、Stable Diffusion WebUI の未認証クレデンシャル露出 (CVE-2026-82288、CVSS 8.7)、Admidio の RSS モジュール認証バイパス (CVE-2026-82657) が新規開示された。

## AI 関連ニュース

> 注: 採用窓（2026-08-30〜09-01）での主要 AI ニュースは少数です。GitLab CVE-2026-19478（8/17-21 窓外）、Microsoft Entra ID CVE-2026-69836（8/20 窓外）、Atlassian RovoBlast（8/7 窓外）等は窓外として除外済み。

- **[2026-08-31]** [OpenAI、Codex での GPT-5.4 / GPT-5.4 mini を廃止し GPT-5.6 Terra・Luna へ移行](https://help.openai.com/en/articles/20001325-a-preview-of-gpt-56-sol-terra-and-luna) — Codex および Assistants API 上の GPT-5.4 系が 8/31 付で廃止となり、GPT-5.6 Terra（コスト削減・GPT-5.5 相当性能）と GPT-5.6 Luna（最軽量・最低コスト）への移行が案内された *(OpenAI)*

- **[2026-08-30]** [Anthropic、Claude Code の週次利用上限を永続的に 25% 引き上げ — 50% 増量プロモは 9/14 終了](https://releasebot.io/updates/anthropic/claude) — 先行実施中の 50% 増量キャンペーンを 2026-09-14 で終了し、以降は恒久的に 25% 引き上げた上限を維持すると発表。有料プランユーザーに追加容量を確約 *(Anthropic)*

## セキュリティ関連ニュース

- **[2026-08-30]** [FireAnt (UNC3886)：Sygnia が Cisco IOS XR + TACACS + Linux ホスト横断の長期潜伏キャンペーンを公開 — BridgeAgent が Zabbix エージェントに偽装](https://www.sygnia.co/research/unc3886-fire-ant-cisco-ios-xr/) — 中国系 APT UNC3886 が GRE トンネルで通信を秘匿し BridgeAgent バックドアを正規 Zabbix エージェントとして配置。TACACS 認証情報を収集しシステムログを抑制することで長期にわたる諜報活動を維持、通信インフラ分野が主標的 *(Sygnia)*

- **[2026-08-31]** [Silver Fox、署名済み中国製壁紙アプリ「QN Wallpaper」経由で ValleyRAT を DLL サイドローディング配布 — Kaspersky が 100,000 件超の検知を報告](https://securelist.com/silver-fox-valleyrat-via-qn-wallpaper/117632/) — libcef.dll のサイドローディングで署名済みバイナリの信頼を悪用し、中国・インドを主標的に ValleyRAT を展開。VBScript バックドアとスクリーンショット取得モジュールを追加投下する多段構成 *(Kaspersky Securelist)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-08-30 以降 / CWE・修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| GHSA-2m69-gcr7-jv3q / CVE-2026-77846 | AshSqlite (Elixir ORM) 0.1.2-rc.0〜0.2.17 | CWE-943 / Medium | `get_path/2` が受け取る JSONPath 式に攻撃者制御の特殊文字（ドット・括弧等）が含まれると SQLite JSON パス解釈が変質 → 非公開フィールドへの不正アクセスが可能 | [v0.2.18 リリース](https://github.com/fuelen/ash_sqlite/releases/tag/v0.2.18) *(commit 不明)* | Elixir Ash ORM エコシステム / JSONPath 注入 / 水平バリアント候補 |
| CVE-2026-82288 | Stable Diffusion WebUI (AUTOMATIC1111) ≤1.10.1 | CWE-200 / CVSS 8.7 | `/sdapi/v1/cmd-flags` エンドポイントが認証なしで全 CLI 引数を返却 → `--gradio_auth` / `--api_auth` の平文クレデンシャルを露出 → 認証情報窃取 | (commit 不明) [security advisory](https://github.com/AUTOMATIC1111/stable-diffusion-webui/security/advisories) | CVSS 8.7 / 未認証クレデンシャル露出 / AI 推論サーバー広範利用 |
| CVE-2026-82657 | Admidio <5.0.12 | CWE-284 / CVSS 7.5 | フォーラム・お知らせの RSS フィードエンドポイントがログイン必須モジュールの認証制限を回避 → 非認証で機密投稿一覧を取得可能 | [v5.0.12 リリース](https://github.com/Admidio/admidio/releases/tag/v5.0.12) *(commit 不明)* | オープンソース組織管理ツール / モジュール認証バイパス |

> 注: Portainer CVE-2026-55761（8/28 開示）・Atlantis CVE-2026-82282（8/28 開示）は採用窓外のため除外。GitLab CVE-2026-19478（8/17 開示）・Microsoft Entra ID CVE-2026-69836 CVSS 10.0（8/20 開示）も同様に除外。

## 国内脆弱性・インシデント情報

> 直近2日間（2026-08-30〜2026-09-01）に該当する新規 JVN/JPCERT/IPA アドバイザリは確認できませんでした。直近の公開情報としては 2026-08-28 の SOY CMS シリーズ任意コード実行 (JVN#04485476) が最新です。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 20+（Sygnia, Kaspersky Securelist, OpenAI, Anthropic, BleepingComputer, The Hacker News, SecurityWeek, CISA, GitHub Advisory DB, NVD, eSecurity Planet, this.weekinsecurity.com, aiagentstore.ai, SOCPrime, GuardianMSSP 他）
- 採用件数: AI=2 / Security=2 / CVE=3 / 国内=0
- 除外理由内訳:
  - 窓外（公開日 < 2026-08-30）: GitLab CVE-2026-19478（8/17 パッチ・8/21 積極悪用報告）、Microsoft Entra ID CVE-2026-69836 CVSS 10.0（8/20 開示）、Atlassian RovoBlast（8/7 Varonis 開示、DEF CON 34 発表後修正済み）、Portainer CVE-2026-55761（8/28 開示）、Atlantis CVE-2026-82282（8/28 開示）、Chrome CVSS 10 CVEs（8/26 開示）、Apache Tomcat CVE-2026-65905（8/25 開示）、Skyvern CVE-2026-82447（8/29 開示）
  - 重複 (excluded_set 該当): LummaC2 Claude セッション乗っ取り（08-31 digest 済み）、Sony/Warner Chappell 訴訟（08-31 digest 済み）、Chrome/Edge 拡張暗号資産窃取（08-31 digest 済み）、TerminalFix（08-31 digest 済み）、McKesson/ShinyHunters（08-30 digest 済み）、Cosmos EVM GHSA-7g4w-cg88-2cq2（08-30 digest 済み）、PaperCut ゼロデイ CVE-2026-82078/81578（08-29 digest 済み）、ServiceNow CVSS 10.0（08-29 digest 済み）
  - 注: 採用窓（2026-08-30〜09-01）は前後期間より主要 CVE・インシデント開示密度が低い時期に該当した
- 取得失敗ソース（EGRESS_BLOCKED）: bleepingcomputer.com, thehackernews.com, cisa.gov, jvn.jp, jpcert.or.jp, ipa.go.jp, securityweek.com, nvd.nist.gov, securelist.com, sygnia.co（WebSearch スニペット経由で情報補完）

</details>
