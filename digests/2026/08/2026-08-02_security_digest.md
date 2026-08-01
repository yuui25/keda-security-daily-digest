# KEDA Security Daily Digest — 2026-08-02

> 採用範囲: 2026-07-31〜2026-08-02 JST に公開された情報のみ掲載。過去 7 日分との重複を除外 ([続報] 表記を除く)。

---

## 本日のサマリ

EU AI Act Article 50 (透明性義務・深偽造物開示) が 8/2 に正式施行された。Google の Big Sleep AI エージェントが Chrome 149/150 のパッチサイクルを通じて 1,072 件のバグを発見・修正したと Google Security Blog が公表した。セキュリティ面では Amgen が患者 PHI を含む侵害を SEC Form 8-K で開示、欧州最大の独立系 adtech 企業 Adform の広告 JS (trackpoint-async.js) がサプライチェーン攻撃でクリップボード暗号資産を窃取する不正コードを配布、Arch Linux が悪意あるメンテナ活動を受け AUR パッケージの採用停止を発表した。CVE 面では CodeIgniter4 と Juggle にそれぞれ CVSS 9.8 の未認証 RCE が同日公開 (2026-07-31) され、apostrophe npm に CVSS 9.1 の Prototype Pollution による認可バイパス、sanitize-html に javascript: URI 通過 XSS も確認された。

---

## AI 関連ニュース

1. [2026-07-31] **Google Chrome Big Sleep** AI エージェントが Chrome 149/150 で **1,072 件**のバグを発見・修正 — Google Project Zero の Big Sleep (元 Naptime) チームが V8/Blink/network スタック全域で自律的なファジングを実施、ゼロデイ前に 1,072 件をクローズドパッチ。詳細は Google Security Blog に公開。([Google Security Blog](https://security.googleblog.com/) / BleepingComputer)

2. [続報][2026-08-02] **EU AI Act Article 50** が本日 8/2 に正式施行 — 生成 AI / ディープフェイクへの透明性義務・開示要件が EU 全域で法的拘束力を持つ。欧州委員会が施行開始を公式声明で確認。違反時は全世界年間売上の最大 1.5% の制裁金。(EU Commission Official / [続報: 2026-07-31 digest 掲載])

---

## セキュリティ関連ニュース

1. [2026-07-31] **Amgen** が患者 PHI 含む侵害を SEC Form 8-K で開示 — 米国バイオ製薬大手が患者の PHI (Protected Health Information) を含む第三者へのデータ不正アクセスを証券当局に報告。詳細の患者数・侵害期間は未公表だが HIPAA 通知義務対象と確認。([DataBreaches.net](https://www.databreaches.net/) / BleepingComputer (2026-07-31))

2. [2026-08-01] **Adform** 広告 JS サプライチェーン攻撃でクリップボード暗号資産窃取 — 欧州最大の独立系 adtech 企業 Adform の `trackpoint-async.js` が改ざんされ、クリップボードの暗号資産ウォレットアドレスを攻撃者アドレスに差し替えるコードを配布。数百のパブリッシャーサイト経由で配信。Adform が修正済みだが影響期間中の損失は調査中。([BleepingComputer](https://www.bleepingcomputer.com/) / DoublePulsar (2026-08-01))

3. [2026-07-31] **Arch Linux AUR** パッケージ採用停止 — Arch Linux が悪意あるメンテナによる AUR (Arch User Repository) パッケージへのバックドア仕込みを受け、新規パッケージ採用プロセスを一時停止。StepSecurity および linuxiac.com が詳細を報告、既存ユーザーへの影響調査継続中。([BleepingComputer](https://www.bleepingcomputer.com/) / linuxiac.com / StepSecurity (2026-07-31))

---

## 新規 CVE / Advisory

| CVE/GHSA | 製品・バージョン | CWE / CVSS | バグクラス (条件→シンク→結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-63223 | CodeIgniter4 <4.7.4 | CWE-434 / **9.8** | 未認証攻撃者が `is_image()`・`mime_in()` の拡張子・MIME 無検証を悪用し .php ファイルをアップロード → PHP 実行 → 任意コード実行 | CodeIgniter4 4.7.4 (2026-07-31); GHSA 参照 | CVSS 9.8 / 未認証 / 人気 PHP フレームワーク / 広範デプロイ |
| CVE-2026-67208 | Juggle ≤1.6.0 (Java/Docker) | CWE-798 / **9.8** | 未認証攻撃者がデフォルト認証情報で H2 コンソール (`/h2-console`) に接続 → `CREATE ALIAS` で `Runtime.exec()` 呼び出し → コンテナ root 権限で任意コード実行 | パッチ未公開 (2026-07-31 発見); 緩和: H2 コンソール無効化 / 認証情報変更 | CVSS 9.8 / 未認証 / デフォルト認証情報 / Docker 環境 |
| CVE-2026-53609 / GHSA-6h5j-32cf-4253 | apostrophe npm <4.31.0 (Node.js CMS) | CWE-1321 / **9.1** | 認証済み攻撃者が `$pullAll` 演算子を介し `apos.util.set()` の無サニタイズ入力で `Object.prototype` を汚染 → REST API 認可チェック迂回 → 任意操作 | apostrophe 4.31.0 (2026-07-31); GHSA-6h5j-32cf-4253 | CVSS 9.1 / Prototype Pollution / Node.js CMS / REST API 認可バイパス |
| CVE-2026-53606 | sanitize-html npm <2.17.5 | CWE-79 / **5.4** | `action`・`formaction`・`data`・`poster`・`background` 属性が `naughtyHref()` チェック対象外 → `javascript:` URI がサニタイズ通過 → 被害者ブラウザで XSS 実行 | sanitize-html 2.17.5 (2026-07-31) | XSS サニタイザーライブラリのバイパスパターン / 広範 npm 利用 |

---

## 国内脆弱性・インシデント

> 直近 2 日間 (2026-07-31〜08-01) に JVN/JPCERT/CC/IPA/Piyolog で確認できた新規の国内脆弱性・インシデント公表はありませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| Google Security Blog / BleepingComputer (Big Sleep 1,072 Chrome bugs) | 2026-07-31 URL "/2026/07/31/" 確認 ✓ |
| EU Commission Official (AI Act Article 50 施行) | 2026-08-02 施行開始公式声明確認 ✓ |
| DataBreaches.net / BleepingComputer (Amgen PHI breach SEC 8-K) | 2026-07-31 "July 31, 2026" 確認 ✓ |
| BleepingComputer / DoublePulsar (Adform trackpoint-async.js) | 2026-08-01 URL "/2026/08/01/" 確認 ✓ |
| BleepingComputer / linuxiac.com / StepSecurity (Arch Linux AUR) | 2026-07-31 "July 31, 2026" 確認 ✓ |
| GitHub Advisory / GHSA (CVE-2026-63223 CodeIgniter4) | 2026-07-31 GHSA 公開確認 ✓ / CodeIgniter4 4.7.4 リリースノート確認 ✓ |
| GitHub Advisory / GHSA (CVE-2026-67208 Juggle) | 2026-07-31 GHSA 公開確認 ✓ |
| GitHub Advisory / GHSA-6h5j-32cf-4253 (CVE-2026-53609 apostrophe) | 2026-07-31 GHSA 公開確認 ✓ / apostrophe 4.31.0 確認 ✓ |
| GitHub Advisory (CVE-2026-53606 sanitize-html) | 2026-07-31 GHSA 公開確認 ✓ / sanitize-html 2.17.5 確認 ✓ |
| jvn.jp / jpcert.or.jp / ipa.go.jp / piyolog | WebSearch 確認: 2026-07-31〜08-01 新規エントリなし |
| thehackernews.com / bleepingcomputer.com / dark reading | 403 — WebSearch スニペット・PRSOL.CC・DoublePulsar 等で代替 |
| nvd.nist.gov / cisa.gov | 403 — WebSearch スニペット代替 |

### 集計サマリ

- **巡回ソース数**: 約 20
- **採用件数**: AI=2 / Security=3 / CVE=4 / 国内=0
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-07-31 より前): Ruflo CVE-2026-59726 (2026-07-29 掲載 → 窓外)
  - 重複 (直近 7 ダイジェスト掲載済み・excluded_set 参照): Anthropic cyber eval breach (08-01掲載) / GPT-5.6 Luna (08-01掲載) / Unit 42 DeepSeek+Hermes 460+ targets (08-01掲載) / Chrome 151 CVE-2026-17650〜17656 (08-01掲載) / Contagious Interview macOS ClickFix (08-01掲載) / SonicWall credential stuffing (08-01掲載) / Kaspersky OctLurk/SilkLurk (08-01掲載) / Laundry Bear CVE-2026-42897 (08-01掲載) / KT Corporation $39M (08-01掲載) / 4G/5G 84 CVEs (08-01掲載) / JVNVU#98815601/94952030/92804348 (08-01掲載) / Copilot Word XPIA worm (07-31掲載) / VMSA-2026-0006 (07-31掲載) / Cisco FMC CVE-2026-20316 (07-31掲載) / Amazon/Sapphire Sleet npm (07-31掲載) / Rails CVE-2026-66066 (07-31掲載) / 生命保険協会 3.7万件 (07-31掲載) / CosmosEscape (07-31掲載) / Claude Mythos Preview HAWK/AES (07-30掲載) / AI pacing letter 1,178 (07-30掲載) / OpenWrt CVE-2026-53921 (07-30掲載) / Apache Axis2 CVE-2026-66713 (07-30掲載) / MAI-Cyber-1-Flash (07-29掲載) / Apple iOS 26.6 CVE-2026-53264 (07-29掲載) / Arista CVE-2026-16812 CISA KEV (07-29掲載) / FortiOS CVE-2025-68686 (07-29掲載) / JetBrains CVE-2026-63077 (07-29掲載) / Kimi K3 open weights (07-27掲載) / CVE-2026-16723 Fastjson (07-27掲載) / GitLab Jupyter BOF (07-26掲載) / CVE-2026-32194/32191 Bing (07-26掲載)

### 主要除外補足

- **EU AI Act Article 50**: 07-31 digest に [2026-07-29] 記事として掲載済みだが、本日 8/2 が実際の施行開始日であり欧州委員会が施行声明を新規公表 → [続報] として採用
- **Ruflo CVE-2026-59726**: BackBox.org URL "/2026/07/29/" 確認 → 採用窓 (2026-07-31〜) 外のため除外
- **Chrome 151 CVE-2026-17650〜17656**: 08-01 digest 掲載済み → 除外。Big Sleep 1,072 件報告は独立した新規記事 (2026-07-31) として採用

</details>

---

*生成: keda-digest-bot / 2026-08-02 05:04 JST*
