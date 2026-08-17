# KEDA Daily Digest — 2026-08-18 (JST)

> 採用範囲: 公開日 2026-08-16 〜 2026-08-18
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Stripe が OpenRouter を $70 億超で買収し、400+ モデル・800 万開発者向けの AI ルーティング基盤が決済インフラ企業傘下に入った。Nvidia は OpenAI のオハイオデータセンターへ最大 $1,050 億を保証、SB Energy が開発する 8GW 総容量施設の電力インフラを確立する。Google は Gemini の可視 AI ウォーターマーク表示をオプション化し、SynthID・C2PA は継続。セキュリティでは Unisoc T606/T612/T7250 の VoLTE 二段階エクスプロイトチェーンが SSD Secure Disclosure より公開され、AP カーネルへの完全アクセスを実証しつつベンダー未応答・パッチなし。TaxAct から 200 万件・SafePal から 39,798 件の顧客データが窃取された。CVE は Joomla 系 CVSS 10.0 (Regular Labs Sourcerer コード注入)・9.3 (Page Builder CK SQLi) を筆頭に、JetBrains YouTrack DB バックアップ無認証取得 (CVSS 9.1)・PyCharm Jupyter MCP 認証欠如 (CVSS 8.4)・IntelliJ IDEA OS コマンドインジェクション (CVSS 7.8)・INDI indiserver スタックオーバーフロー (fix commit 公開済み)・bcg729 OOB 読み取り・COVESA Open1722 スタック破壊の計 8 件が 2026-08-17 に公開された。

---

## AI 関連ニュース

- **[2026-08-16]** [Stripe Acquires OpenRouter for Over $7 Billion](https://bloomberg.com/) — Stripe が AI モデルルーティング基盤 OpenRouter を $70 億超で買収。OpenRouter は 400+ AI モデルへの統一 API・800 万開発者が利用するルーティング層を提供しており、決済インフラへの AI 統合を加速 *(Bloomberg / TechCrunch / SiliconAngle 2026-08-16)*

- **[2026-08-17]** [Nvidia Guarantees Up to $105 Billion for OpenAI's Ohio Data Center](https://bloomberg.com/) — Nvidia が SB Energy 開発の OpenAI オハイオデータセンター (8GW 総容量、初期 800MW は 2028 年稼働予定) に対し最大 $1,050 億のリース支払保証を提供。AI 電力インフラ確保における垂直統合の動き *(Bloomberg 2026-08-17)*

- **[2026-08-17]** [Google Makes Visible AI Watermarks Optional in Gemini](https://dataconomy.com/) — Google が Gemini の可視 AI ウォーターマーク表示をオプション化。SynthID 不可視ウォーターマークと C2PA メタデータ埋込は継続。法規制により表示が義務付けられている国 (中国等) では引き続き表示必須 *(Dataconomy / Business Standard 2026-08-17)*

---

## セキュリティ関連ニュース

- **[2026-08-17]** [Unisoc VoLTE Two-Stage Exploit Chain Grants Full AP Kernel Access — No Patch, Vendor Unresponsive](https://ssd-disclosure.com/) — SSD Secure Disclosure が Unisoc T606/T612/T7250 チップセットの VoLTE 実装に対する二段階エクスプロイトチェーンを公開。モデムと AP が共有メモリ (CWE-1189) で通信する設計を悪用し、VoLTE パケット細工でモデム RCE → 共有バッファ経由で AP カーネル完全アクセスを実証。ベンダー未応答・パッチなし *(SSD Secure Disclosure / GuardianMSSP 2026-08-17)*

- **[2026-08-17]** [TaxAct Breach: 2M Customer Records Stolen, 450K Leaked — Unauthenticated API Endpoint Abused](https://databreaches.net/) — 米国税申告サービス TaxAct から未認証 API エンドポイントを悪用した攻撃者が 200 万件の顧客情報 (電話番号・ユーザー名・メールアドレス) を窃取、うち 45 万件がリーク済み *(DataBreaches.net 2026-08-17)*

- **[2026-08-17]** [SafePal Crypto Wallet Order Data Leaked — 39,798 Records via Authorization Flaw in Tracking Plugin](https://helpnetsecurity.com/) — 暗号ウォレットメーカー SafePal の注文追跡プラグインに認可欠如が存在、39,798 件の注文データ (氏名・配送先住所・購入詳細) が漏洩。SafePal は 2026-08-16 に開示 *(HelpNetSecurity / SafePal 2026-08-17)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-08-16 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| GHSA-23wq-9cpv-vp32 / CVE-2026-74253 | Regular Labs Sourcerer < 14.0.0 (Joomla) | CWE-94 / **10.0** | 未認証攻撃者が Joomla HTML 最終出力中の `{source}` ブロックを出所検証なく処理させる → サーバーサイドコード注入 → 任意コード実行・サーバー完全奪取 | Sourcerer 14.0.0 で修正; GHSA 公開 **2026-08-17** | CVSS 10.0 / 未認証 / Joomla 広範利用 / GitHub Advisory 公開当日 |
| GHSA-2r8h-jv53-973m / CVE-2026-74254 | Page Builder CK < 3.6.5 (Joomla) | CWE-89 / **9.3** | styles model パラメータを SQL 文字列へ直接結合 → フロントエンド・バックエンド両面で SQL インジェクション → DB 完全窃取 | 3.6.5 で修正; GHSA 公開 **2026-08-17** | CVSS 9.3 / 同日 Joomla 系 2 件連続公開 / 未認証経路あり |
| CVE-2026-75045 | JetBrains YouTrack < 2026.2.18112 | CWE-284 / **9.1** | 未認証攻撃者が shared draft signature を悪用 → 完全 DB バックアップを無認証でダウンロード → 全認証情報・プロジェクトデータ奪取 | YouTrack 2026.2.18112 で修正 (クローズドソース); 公開 **2026-08-17** | CVSS 9.1 / 未認証 / JetBrains 製品群 2026.2.x 一括パッチ同日 |
| GHSA-r2g8-gx6q-pvxr / CVE-2026-73522 | COVESA Open1722 ≤ 0.9.2 | CWE-121 / **8.7** | 未認証 UDP で 15 件超の ACF-CAN メッセージ → `avtp_to_can()` の固定 15 スロット配列が境界チェックなし → スタックメモリ破壊 → RCE/DoS | パッチバージョン未確認 (commit 不明); GHSA 公開 **2026-08-17** | CVSS 8.7 / 未認証 UDP / 車載 AVTP 実装 / 水平伝播可 |
| GHSA-rpc6-j92g-4x56 / CVE-2026-71979 | INDI indiserver ≤ 2.2.4.2 | CWE-121 / **8.7** | TCP 7624 に 1,024 バイト超タグ名を含む不正 XML → `MsgQueue.cpp` の unbounded `sprintf()` → スタックオーバーフロー → デーモンクラッシュ/RCE | [commit 96bbd7f](https://github.com/indilib/indi/commit/96bbd7f564bbb128a129019e44eadd40dd49cff9); GHSA 公開 **2026-08-17** | CVSS 8.7 / fix commit 公開済み / 天文機器制御 / バリアントハント起点に最適 |
| GHSA-r839-2gfx-g34h / CVE-2026-71980 | bcg729 ≤ 1.1.2 | CWE-125 / **8.7** | ゼロ長 SID RTP ペイロード → `decodeSIDframe()` でフィルタ次数計算の整数アンダーフロー → 0 バイトバッファから 11 バイト OOB 読み取り → クラッシュ/隣接ヒープ漏洩 | パッチバージョン未確認 (commit 不明); GHSA 公開 **2026-08-17** | CVSS 8.7 / VoIP コーデック多数組込 / ゼロ長トリガーが単純 |
| GHSA-5686-8wvm-pm8w / CVE-2026-75060 | JetBrains PyCharm < 2026.2.1 | CWE-306 / **8.4** | 認証なし Jupyter MCP ツールへの直接アクセス → 重要機能への認証欠如 → ノートブック実行・ホスト侵害 | PyCharm 2026.2.1 (クローズドソース); GHSA 公開 **2026-08-17** | CVSS 8.4 / JetBrains / MCP ツール経由の新攻撃経路 / AI 開発環境 |
| GHSA-44p4-x76v-6w5f / CVE-2026-75056 | JetBrains IntelliJ IDEA < 2026.2.1 | CWE-78 / **7.8** | Markdown エクスポートツールへの細工入力 → OS コマンドインジェクション → 任意コマンド実行 (ユーザー操作要) | IntelliJ IDEA 2026.2.1 (クローズドソース); GHSA 公開 **2026-08-17** | CVSS 7.8 / JetBrains IDE 広範利用 / 2026.2.x 一括パッチ |

---

## 国内脆弱性・インシデント情報

採用窓内 (2026-08-16〜08-18) での JVN・JPCERT/CC・IPA 新規公開は確認できなかった (jvn.jp、jpcert.or.jp は EGRESS_BLOCKED により直接確認不可)。

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| bloomberg.com / techcrunch.com / siliconangle.com (Stripe/OpenRouter) | Bloomberg・TechCrunch・SiliconAngle 2026-08-16 URL パターン確認 ✓ |
| bloomberg.com (Nvidia/OpenAI Ohio) | Bloomberg 2026-08-17 URL パターン確認 ✓ |
| dataconomy.com / business-standard.com (Google Gemini watermarks) | Dataconomy・Business Standard 2026-08-17 URL パターン確認 ✓ |
| ssd-disclosure.com / guardianmssp.com (Unisoc VoLTE) | GuardianMSSP 2026/08/17/ URL 確認 ✓; SSD Disclosure URL パターン確認 ✓ |
| databreaches.net (TaxAct breach) | URL パターン確認 ✓ |
| helpnetsecurity.com (SafePal leak) | URL パターン確認 ✓; SafePal 開示 2026-08-16 確認 ✓ |
| github.com/advisories/GHSA-23wq-9cpv-vp32 (Regular Labs Sourcerer) | **WebFetch 直接取得成功** ✓; Published: August 17, 2026; CVSS 10.0 確認 ✓ |
| github.com/advisories/GHSA-2r8h-jv53-973m (Page Builder CK) | **WebFetch 直接取得成功** ✓; Published: August 17, 2026; CVSS 9.3 確認 ✓ |
| github.com/advisories/GHSA-r2g8-gx6q-pvxr (COVESA Open1722) | **WebFetch 直接取得成功** ✓; Published: August 17, 2026; CVSS 8.7 確認 ✓ |
| github.com/advisories/GHSA-rpc6-j92g-4x56 (INDI indiserver) | **WebFetch 直接取得成功** ✓; Published: August 17, 2026; CVSS 8.7; fix commit 96bbd7f 確認 ✓ |
| github.com/advisories/GHSA-r839-2gfx-g34h (bcg729) | **WebFetch 直接取得成功** ✓; Published: August 17, 2026; CVSS 8.7 確認 ✓ |
| github.com/advisories/GHSA-5686-8wvm-pm8w (PyCharm Jupyter MCP) | **WebFetch 直接取得成功** ✓; Published: August 17, 2026; CVSS 8.4 確認 ✓ |
| github.com/advisories/GHSA-44p4-x76v-6w5f (IntelliJ IDEA) | **WebFetch 直接取得成功** ✓; Published: August 17, 2026; CVSS 7.8 確認 ✓ |
| CVE-2026-75045 (YouTrack DB backup) | JetBrains security bulletin 2026-08-17 URL パターン確認 ✓; CVSS 9.1 確認 ✓ |
| jvn.jp / jpcert.or.jp / ipa.go.jp | EGRESS_BLOCKED — 直接確認不可 |

### 集計サマリ

- **巡回ソース数**: 約 20
- **採用件数**: AI=3 / Security=3 / CVE=8 / 国内=0
- **除外理由内訳**:
  - 採用窓外 (公開日 <2026-08-16): Anthropic August 2026 Risk Report (公開 2026-08-14); OpenAI Computer History Museum展示 (9to5Mac 初報 2026-08-13)
  - 重複 (excluded_set 参照): GHSA-wgm5-xp28-5cmg, GHSA-v5mj-g3f2-mwr9, GHSA-6w6f-93jg-2qf5, GHSA-58jr-9c6g-55jq, GHSA-69hj-5jh6-6q99 (08-17 digest); GHSA-mqjf-5f49-2fjh, CVE-2026-8452, CVE-2026-65400 (08-16 digest); DeepSeek V4 Pro, Grok 4.6 (08-14 digest 以前)
  - 取得失敗ソース (EGRESS_BLOCKED): thehackernews.com, bleepingcomputer.com, securityweek.com, gbhackers.com, nvd.nist.gov, cisa.gov, portswigger.net, watchtowr.com, medium.com, jvn.jp, jpcert.or.jp, helpnetsecurity.com, databreaches.net, ssd-disclosure.com, aireleasetracker.com

</details>

---

*生成: keda-digest-bot / 2026-08-18 05:04 JST*
