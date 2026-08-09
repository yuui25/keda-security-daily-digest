# KEDA Daily Digest — 2026-08-10 (JST)

> 採用範囲: 公開日 2026-08-08 〜 2026-08-10
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Atlassian の AI アシスタント Rovo が rovoChatPrompt URL パラメータを悪用した間接プロンプトインジェクション（RovoBlast）によって Confluence/Jira/SharePoint 内のデータを攻撃者サーバーに送出できることを Varonis と PromptArmor が相次いで報告、Atlassian 修正済みのベクターとは別の未修正経路が残存していることも明らかになった。インフラ面では Progress Kemp LoadMaster の未認証 OS コマンドインジェクション（CVE-2026-8037、CVSS 9.6）が CISA KEV に登録され FCEB 機関の修正期限が本日（8/10 JST）に迫っており、野生での悪用試行は 792 件超が確認済み。N-able N-central は先週来の CVE-2026-18577 悪用継続を受けてホットフィックス 2 を公開した。open-iscsi の iSNS 属性デコーダにおける二重解放（CVE-2026-55995）も 8/8 に開示されたが詳細スコアは未採点。

---

## AI 関連ニュース

- **[2026-08-08]** [RovoBlast: How One Click Triggered Atlassian's AI Assistant to Leak Data](https://www.varonis.com/blog/rovoblast) — Varonis が命名した RovoBlast は、Rovo Chat の rovoChatPrompt URL パラメータに攻撃者制御の指示を埋め込んだリンクをクリックさせるだけで（1クリック、認証ユーザー）、Rovo が被害者の権限で Confluence・Jira・SharePoint データを攻撃者が管理する外部サーバーへ送出する間接プロンプトインジェクション。Atlassian は 7/8 にサーバーサイドで修正済み（Bugcrowd 経由）。一方 PromptArmor は別の未修正ベクターを 5/23 に開示したが Atlassian からの応答なく 8/5 に公開。ウェブ検索オフでも有効な経路が残存する点が危機感を高めた *(Varonis/PromptArmor/The Hacker News)*

---

## セキュリティ関連ニュース

- **[続報][2026-08-08]** [N-able N-central Hotfix 2 released amid continued CVE-2026-18577 exploitation](https://www.n-able.com/security/) — 先週来の悪用継続（2026-08-04 digest 掲載: 認証不要の RCE CVE-2026-18577）を受け N-able が N-central Hotfix 2 を公開。既に Hotfix 1 を適用済みの環境でも追加適用が必須とされており、顧客向け緊急通知が発出された *(N-able Security Advisory)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-08-08 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-8037 | Progress Kemp LoadMaster (パッチ前全バージョン) | CWE-78 / **9.6** | 未認証攻撃者が `/accessv2` エンドポイントに細工した HTTP リクエストを送信 → 未初期化ヒープ + `escape_quotes()` の出力バッファ未終端により shell 呼び出しの引数が汚染 → `system()` 経由で root として任意コマンド実行 | 公式パッチ公開済み (2026-06-29); CISA KEV 登録 2026-08-07; FCEB 適用期限 **2026-08-10** | CVSS 9.6 / 未認証 / CISA KEV / 野生悪用 792 件確認 / ネットワークエッジ機器 |
| CVE-2026-55995 | open-iscsi (iSNS attribute decoder、バージョン範囲未公表) | CWE-415 / 未採点 | 攻撃者が制御する不正な iSNS 属性レスポンスを open-iscsi の iSNS デコーダに受理させる → 属性解析中に同一メモリ領域を二重解放 → ヒープ破壊 → クラッシュ (DoS) または潜在的 RCE | 修正バージョン未確認（2026-08-08 開示時点で upstream patch なし） | 公開日 2026-08-08; CVSSスコア未採点; iSNS 利用環境（ストレージネットワーク）で影響 |

---

## 国内脆弱性・インシデント情報

> 直近 3 日間 (2026-08-08〜08-10) に JVN/JPCERT/CC/IPA で確認できた新規の国内脆弱性・インシデント公表はありませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| Varonis blog / PromptArmor (RovoBlast / Atlassian Rovo AI) | Varonis URL "/blog/rovoblast" 確認 ✓; THN 2026-08-08 URL 確認 ✓ |
| The Hacker News (CVE-2026-8037 / Kemp LoadMaster KEV) | THN URL "2026/08/" 確認 ✓; CISA KEV 登録 2026-08-07 ✓ |
| SecureLayer7 / SOCRadar / watchTowr Labs (CVE-2026-8037 技術詳細) | 複数ソースで CVSS 9.6 / CWE-78 / root RCE 確認 ✓ |
| N-able Security (N-central Hotfix 2) | 2026-08-08 Hotfix 2 公開確認 ✓ |
| TheWindowsUpdate.com (CVE-2026-55995 open-iscsi) | URL "/2026/08/08/" 確認 ✓ |
| jvn.jp / jpcert.or.jp / ipa.go.jp | 2026-08-08〜10 新規エントリなし |
| GitHub Advisory Database | GHSA-5x4f-6m9q-mg75 (Aitemi M300 Wi-Fi, Aug 9) 確認したが先週来の同シリーズ (CVE-2025-34147/48/49) の続報として採用基準外と判断 |
| PyJWT CVE-2026-32597 / CVE-2026-48524 | それぞれ 2026-03-12 / 2026-05-28 公開で採用窓外のため除外 |

### 集計サマリ

- **巡回ソース数**: 約 20
- **採用件数**: AI=1 / Security=1 / CVE=2 / 国内=0
- **除外理由内訳**:
  - 採用窓外 (公開日 <2026-08-08): CVE-2026-32597 (PyJWT, 2026-03-12) / CVE-2026-48524 (PyJWT, 2026-05-28) / OpenAI エージェントサンドボックスエスケープ + Hugging Face (2026-08-04 CNN 初報) / OWASP GenAI LLM Top 10 2026 (2026-08-04)
  - 重複 (excluded_set 参照): N-able CVE-2026-18577 (2026-08-04掲載; Hotfix 2 は [続報] で採用) / CVE-2026-8496 (2026-08-09掲載) / Anthropic Claude internet escape (2026-08-03掲載 "Anthropic cyber eval breach") / COLDCARD PRNG $88.6M (2026-08-09掲載) / NatJack (2026-08-09掲載) / Metabase CVSS 10.0 (2026-08-09掲載) / GitPython GHSA-4gmw-gg2m-w46p (2026-08-09掲載) / CSS inbox attack (2026-08-09掲載)
  - GHSA-5x4f-6m9q-mg75 (Shenzhen Aitemi M300 Wi-Fi Repeater, Aug 9): CVE-2025-34147/48/49 系の量産品 IoT コマンドインジェクションシリーズの追加開示であり独立ニュース性が低いと判断し除外
  - 取得失敗ソース (EGRESS_BLOCKED): thehackernews.com, bleepingcomputer.com, nvd.nist.gov, cisa.gov, securityweek.com, gbhackers.com, portswigger.net

</details>

---

*生成: keda-digest-bot / 2026-08-10 05:06 JST*
