# KEDA Security Daily Digest — 2026-07-06 (JST)

> 対象期間: 2026-07-04 〜 2026-07-06 (JST) / 生成: 2026-07-06T05:03 JST

---

## 本日のサマリ

米国独立記念日 (7/4) と日曜日 (7/5) が重なる閑散週末のため、大規模開示・ベンダーアドバイザリは少数にとどまる。一方、北朝鮮 Lazarus/Contagious Interview による **PolinRider** サプライチェーン攻撃 (npm/Packagist/Go/Chrome 拡張 108 パッケージ) が判明し、既存パッケージへの混入手法が確認された。国連では 193 加盟国参加の **AI ガバナンス対話** がジュネーブで開幕し、UN 独立科学パネルが「AIが指示に従う技術的保証なし」と警告した。CVE は cve-search の未認証 MongoDB 読み取り (CVSS 9.2)・AIL Framework パストラバーサル・Pardus 子どもフィルターの DNS スプーフィング助長バグの 3 件。

---

## AI 動向

- `[2026-07-06]` **国連 AI ガバナンス・グローバル対話が開幕** — 193 UN 加盟国が初参加する政府間 AI ガバナンス対話がジュネーブで開幕。共同議長: Egriselda López (エルサルバドル) & Rein Tammsaar (エストニア)。UN 独立科学パネルが「AI が指示に従う技術的保証は現時点では存在しない」と明示的に警告; ITU AI for Good サミット (7/7-10) / WSIS フォーラム (7/6-10) と並行開催。*(UN News / UNESCO / ITU)*

---

## セキュリティ動向

- `[2026-07-04]` **PolinRider: 北朝鮮 Lazarus が Rollup ポリフィル詐称の 108 パッケージを公開** — Contagious Interview / DEV#POPPER 作戦の延長として Socket が捕捉。npm/Packagist/Go/Chrome 拡張で 162 成果物を公開; 第 2 段階の SVG ユーティリティ偽装依存が外部 JSON ペイロードを取得し RAT を実行。GitHub メンテナーアカウントを侵害して既存パッケージに悪意コードを混入する手法も確認。開発者端末の認証情報・暗号資産ウォレット・AI コーディングツール API キーを標的とする。*(Socket / THN / GBHackers)*

---

## 新規 CVE / 脆弱性

| CVE / GHSA | 製品 / バージョン | CWE / CVSS | バグクラス概要 | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-59509 / GHSA-3fmp-59v6-4qw2 | cve-search (全バージョン) | CWE-20 / **9.2** | 未認証攻撃者が POST `/fetch_cve_data` の `collection`・`fields`・`regex` パラメーターを操作 → 任意 MongoDB コレクション読み取り → `mgmt_users` から管理者ハッシュ取得 → オフラインクラッキング | コミット未確定 (GHSA 参照) | 2026-07-05 GHSA 公開 / 未認証 CVSS 9.2 / CVE 管理ツール自体の認証情報漏洩リスク |
| CVE-2026-59510 / GHSA-jf65-fx73-9f2j | AIL Framework (全バージョン) | CWE-22 / **7.1** | 認証済み攻撃者が PDF オブジェクト識別子に `../` を含むパスを供給 → `PDF.get_filepath()` が realpath 検証なしにファイルパスを構築 → PDF_FOLDER 外の任意ファイル (設定ファイル・認証情報) にアクセス | GHSA 参照 | 2026-07-05 GHSA 公開 / サイバー脅威インテリジェンス収集プラットフォームの設定・認証情報漏洩 |
| CVE-2026-9085 / GHSA-686q-wrh7-cph5 | Pardus-Parental-Control (TUBITAK BILGEM) ≤0.5.1 | CWE-732 + CWE-284 / **8.8** | ローカル低特権攻撃者がクリティカルリソースへの不正アクセス制御を悪用 → DNS スプーフィング攻撃を実行可能; scope: Changed | 修正版未確定 (GHSA 参照) | 2026-07-05 GHSA 公開 / スコープ変更あり / 子ども向けフィルターのカーネル権限コンポーネントが対象 |

---

## 国内動向

2026-07-04 〜 07-06 (JST) 期間中、主要ソース（JPCERT/CC・IPA・JVN・Piyolog）にて新規国内脆弱性・インシデントの公表は確認できませんでした。

---

<details>
<summary>収集メタデータ / デバッグ情報</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| github.com/advisories (Jul 4-6 filter) | CVE-2026-59509/GHSA-3fmp (cve-search), CVE-2026-59510/GHSA-jf65 (AIL Framework), CVE-2026-9085/GHSA-686q (Pardus) 取得 ✓ |
| Socket / THN / GBHackers (PolinRider) | WebSearch スニペット確認 ✓ (2026-07-04 UTC) |
| UN News / UNESCO / ITU (AI ガバナンス対話) | WebSearch スニペット確認 ✓ (2026-07-06 JST) |
| bleepingcomputer.com | 403 — WebSearch スニペットで代替 |
| thehackernews.com | 403 — WebSearch スニペットで代替 |
| jvn.jp / jpcert.or.jp | 403 / 新規エントリなし (WebSearch 確認) |
| cisa.gov (KEV) | 403 — WebSearch 確認: 採用窓内の新規 KEV エントリなし |

### 集計サマリ

- **AI ニュース**: 1 件
- **セキュリティニュース**: 1 件
- **CVE エントリ**: 3 件
- **国内インシデント**: 0 件
- **件数が通常より少ない理由**: 採用窓 (2026-07-04〜07-06) が米国独立記念日 (7/4, 土) + 日曜日 (7/5) に重なる週末; 主要 US メディア・ベンダーはほぼ停止状態; 欧州/アジアソースも週末のため低調。

### 除外 (日付窓外またはexcluded_set)

- WinRAR CVE-2026-14191 (2026-07-01 UTC — 窓外)
- JetBrains Hub CVEs (2026-05〜06 公開 — 窓外)
- Anthropic jailbreak framework (2026-07-02 UTC — 窓外)
- UN AI Science Panel report (2026-07-01 UTC — 窓外)
- UN ITU AI for Good 委員会発足 (2026-07-03 JST → 2026-07-05 digest 掲載済み)
- CVE-2026-46242 Bad Epoll / CVE-2026-12166-12168 GamersFirst (2026-07-05 digest 掲載済み)
- CVE-2026-52830 / CVE-2026-45499 / CVE-2026-57100 / DSA-2026-278 (2026-07-04 digest 掲載済み)
- その他直近 7 ダイジェスト (2026-06-29〜2026-07-05) 掲載の全 CVE/GHSA/URL

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-06-29 〜 2026-07-05) の全 CVE/GHSA/URL を除外済み。*
