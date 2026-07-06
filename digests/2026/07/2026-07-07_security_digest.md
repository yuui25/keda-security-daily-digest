# KEDA Security Daily Digest — 2026-07-07 (JST)

> 対象期間: 2026-07-05 〜 2026-07-07 (JST) / 生成: 2026-07-07T05:03 JST

---

## 本日のサマリ

米国独立記念日明けの月曜 (7/7) を迎え、ITU **AI for Good グローバルサミット**がジュネーブ Palexpo で開幕 (44 委員国連委員会は 7/8 初会合)。AI セキュリティ面では Zscaler ThreatLabz が AI コーディングエージェントを標的とした実世界の**間接プロンプトインジェクション (IPI)** キャンペーンを初確認—26 LLM テスト中 4 モデルが攻撃者の仮想通貨ウォレットへ誘導された。物理セキュリティでは山東大学が HDMI/DisplayPort ケーブルの不要輻射を悪用しエアギャップ端末からデータを盗む **TrojPix** 手法を USENIX Security 35 で公開 (8.1 Mbps / 208 m)。CVE は BeyondTrust Remote Support/PRA の CVSS 9.2 事前認証バイパス (CVE-2026-40138/40139)・Cilium Critical 情報漏洩 (CVE-2026-49445)・flyto-core MCP 未認証 RCE + SSRF バイパス (CVE-2026-55786/55787)・Formie SSTI Critical (CVE-2026-52889) の合計 6 CVE。

---

## AI 動向

- `[2026-07-06]` **Zscaler: AI コーディングエージェントを標的とした間接プロンプトインジェクション攻撃キャンペーンを初確認** — 26 LLM を検証。攻撃チェーン①: 偽 Python ライブラリドキュメントがコーディングエージェントに「$3 API ライセンス料を攻撃者の仮想通貨ウォレットへ」送金させる; ②: DeBank 仮想通貨サービスのタイポスクワッティング経由の IPI。Meta Llama・Google Gemini 系計 4 モデルが実際に操作された。*(Zscaler ThreatLabz / Infosecurity Magazine / Security Boulevard)*
- `[2026-07-07]` **ITU AI for Good グローバルサミット開幕 (ジュネーブ 7/7-10)** — Palexpo にて 44 委員国連委員会が 7/8 初会合を開催予定。国連 AI ガバナンス・グローバル対話 (WSIS フォーラム) と並行開催。ロボティクス for Good ユースチャレンジ (68 チーム・39 カ国)、AI セキュリティ標準ワークショップ等を実施。*(ITU / TechTimes)*

---

## セキュリティ動向

- `[2026-07-06]` **TrojPix — エアギャップ端末からの動画ケーブル電波漏洩による秘密データ盗取手法が公開** — 山東大学が USENIX Security 35 向けに公開。ユーザーモードマルウェアが画面上で知覚不能な微小ピクセル変化を生成 → HDMI/DisplayPort ケーブルが特定周波数の電磁波を放射 → 離れた受信機がデータを復元。最大 8.1 Mbps / 測定距離 208 m。既存の電磁シールドや Faraday ケージへの追加対策の必要性を指摘。*(GuardianMSSP / Shandong University / USENIX Security 35)*

---

## 新規 CVE / 脆弱性

| CVE / GHSA | 製品 / バージョン | CWE / CVSS | バグクラス概要 | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-40138 + CVE-2026-40139 | BeyondTrust Remote Support / Privileged Remote Access (全対象バージョン) | CWE-287 / **9.2** | 特定の認証設定下で認証検証の不備を悪用 → Remote Support・PRA への事前認証アクセス取得 | アドバイザリ BT26-02 参照 | 2026-07-06 公開 / CVSS 9.2 / 未認証 / 特権リモートアクセス製品 |
| CVE-2026-49445 | Cilium (Go) | CWE-200 / **Critical** | ローカルホスト上の Envoy 管理ソケットへの不正アクセス → クラスター内の機密情報漏洩・サービス妨害 (クラスター障害) | GHSA 参照 (credit: 0xch4z, moemen) | 2026-07-05〜07 GHSA 公開 / Kubernetes ネットワーク基盤 Critical |
| CVE-2026-55786 + CVE-2026-55787 | flyto-core (pip) | CWE-78 + CWE-918 / **High** | CVE-55786: HTTP MCP エンドポイント経由の未認証コマンド実行; CVE-55787: IPv6 遷移アドレス (::ffff:127.0.0.1 等) による SSRF ガード回避 | GHSA 参照 | 2026-07-05 公開 / MCP サーバー未認証 RCE + SSRF バイパス |
| CVE-2026-52889 | Formie (Composer) | CWE-94 / **Critical** | 非表示フィールドのデフォルト値に悪意テンプレート構文を挿入 → SSTI → 任意コード実行 | GHSA 参照 | 2026-07-05〜07 GHSA 公開 / Craft CMS 向けフォームプラグイン / Critical |

---

## 国内動向

2026-07-05 〜 07-07 (JST) 期間中、主要ソース（JPCERT/CC・IPA・JVN・Piyolog）にて新規国内脆弱性・インシデントの公表は確認できませんでした。

---

<details>
<summary>収集メタデータ / デバッグ情報</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| github.com/advisories (Jul 5-7 filter) | CVE-2026-49445 (Cilium), CVE-2026-55786/55787 (flyto-core), CVE-2026-52889 (Formie) 取得 ✓ |
| BeyondTrust BT26-02 | CVE-2026-40138/40139 (CVSS 9.2) — アドバイザリ 403 / WebSearch・threat-modeling.com スニペットで確認 ✓ |
| Zscaler ThreatLabz (IPI) | WebSearch スニペット確認 ✓ (2026-07-06 UTC) |
| GuardianMSSP / Thomas Harris blog (TrojPix) | WebSearch スニペット確認 ✓ (2026-07-06 UTC) |
| ITU (AI for Good Summit) | WebSearch スニペット確認 ✓ (2026-07-07 JST) |
| bleepingcomputer.com | 403 — WebSearch スニペットで代替 |
| thehackernews.com | 403 — WebSearch スニペットで代替 |
| jvn.jp / jpcert.or.jp | 403 / 新規エントリなし (WebSearch 確認) |
| cisa.gov (KEV) | 403 — WebSearch 確認: 採用窓内の新規 KEV エントリなし |

### 集計サマリ

- **AI ニュース**: 2 件
- **セキュリティニュース**: 1 件
- **CVE エントリ**: 6 件 (4 行、複数 CVE 含む)
- **国内インシデント**: 0 件
- **件数が通常より少ない理由**: 採用窓 (2026-07-05〜07-07) の前半 (7/5-6) は米国独立記念日連休の週末続き; 主要 US メディア・ベンダーの公開ペースが回復途上。

### 除外 (日付窓外または excluded_set)

- WatchGuard CVE-2026-13368 (2026-07-02 公開 — 窓外)
- Operation DragonReturn (2026-07-04 THN — 窓外)
- FatFs CVE-2026-6682〜6688 (runZero 2026-07-01〜03 開示 — 窓外)
- curl/libcurl CVEs (2026-06-24 リリース — 窓外)
- Google DeepMind $10M マルチエージェント資金 (2026-06-11 — 窓外)
- Scriban GHSA-7jvp-hj45-2f2m (2026-05-30 GHSA 公開 — 窓外)
- UN AI ガバナンス対話開幕 / PolinRider / CVE-2026-59509 / CVE-2026-59510 / CVE-2026-9085 (2026-07-06 digest 掲載済み)
- CVE-2026-46242 Bad Epoll / CVE-2026-12166-12168 (2026-07-05 digest 掲載済み)
- その他直近 7 ダイジェスト (2026-06-30〜2026-07-06) 掲載の全 CVE/GHSA/URL

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-06-30 〜 2026-07-06) の全 CVE/GHSA/URL を除外済み。*
