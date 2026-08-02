# KEDA Security Daily Digest — 2026-08-03

> 採用範囲: 2026-08-01〜2026-08-03 JST に公開された情報のみ掲載。過去 7 日分との重複を除外 ([続報] 表記を除く)。

---

## 本日のサマリ

オープンウェイト AI モデルをめぐる競合マニフェスト論争が激化し、Nvidia・Meta 陣営の「開放=イノベーション」対 Anthropic ペーシング連合の対立構図が明確化した (Axios, 8/2)。セキュリティ面では Midnight Blizzard (APT29) がホテル Wi-Fi を悪用してゲスト端末に CornFlake RAT を配布し OAuth デバイスコードフローで MFA 済み M365 トークンを窃取する CaptiveCrunch キャンペーンが公表、Coldcard ハードウェアウォレット Mk3 の PRNG 欠陥で $70M+ 相当 Bitcoin が 7/30 に窃取されたことが 8/1 に判明した。HackerOne は全バグバウンティ提出者への政府 ID 本人確認を義務化、CISA は 7 州以上の水道・廃水処理施設への PLC 攻撃を正式警告した。CVE 面では Adobe Campaign Classic に CVSS 10.0 の未認証 RCE (CVE-2026-48449) および CVSS 8.6 の SQL インジェクション (CVE-2026-48448) が 7/29 のパッチで修正済みとして開示された。

---

## AI 関連ニュース

1. [2026-08-02] **オープンウェイト AI マニフェスト論争** 激化 — Nvidia Jensen Huang + Meta Zuckerberg がオープンウェイトこそイノベーション・反独占の担保と主張する連名マニフェストを発表、一方 Anthropic ペーシング連合はフロンティア能力の野放し拡散リスクを強調する対抗マニフェストを公開。OpenAI/Anthropic のモデル逸脱事例と Kimi K3 フロンティアオープンウェイト公開が議論の引き金に。([Axios](https://www.axios.com/2026/08/02/ai-manifesto-open-weight-models))

2. [2026-08-01] **ESET H1 2026 脅威レポート** — ESET が 90 万スキル中 3,000+ の悪意ある AI スキルを特定。ClickFix 検出数が前期比 +108% 増加、ClickFix と OAuth を組み合わせた ConsentFix が新亜種として登場。100 種以上の EDR Killer ツールを追跡、QR コードフィッシングがフィッシングメール全体の 11% を占め過去最高を更新。([BleepingComputer](https://www.bleepingcomputer.com/) / [WeLiveSecurity](https://www.welivesecurity.com/) (2026-08-01))

---

## セキュリティ関連ニュース

1. [2026-08-01] **CaptiveCrunch** — Midnight Blizzard (APT29/Storm-2945/SVR) がホテル・会議センターの Wi-Fi インフラを乗っ取り、接続企業出張者のデバイスに偽 Windows/ブラウザ更新を配信して **CornFlake RAT** を投下。同時に OAuth デバイスコード認証フローを悪用して MFA 済みの M365 アクセストークンを窃取し、被害者の企業 SaaS 環境へ永続アクセスを確立。([Microsoft Security Blog (2026-07-31)](https://www.microsoft.com/en-us/security/blog/) / Forbes (2026-08-01))

2. [2026-08-01] **Coldcard ハードウェアウォレット PRNG 欠陥で $70M+ Bitcoin 窃取** — Mk3 firmware がシード種生成時に STM32 HW-RNG の代わりに決定論的 PRNG (Yasmarang) を使用するバグにより有効エントロピーが 40 bit に低下。2026-07-30 に 1,082 BTC を 41 分で窃取 (8/1 時点 $75M 超)。2021 年以来の firmware バグで Mk3/4/5/Q が影響範囲。緊急パッチ公開済みだが既存シードは移行が必要。([CoinDesk (2026-08-01)](https://www.coindesk.com/) / Galaxy Research)

3. [2026-08-01] **HackerOne が全バグバウンティ提出者への政府 ID 本人確認を義務化** — Veriff を通じた本人確認を全バグバウンティプログラムの提出者に必須化。VDP (報酬なし脆弱性開示プログラム) は対象外。([CyberSecurityNews (2026-08-01)](https://cybersecuritynews.com/))

4. [続報][2026-08-01] **CISA が水道・廃水処理施設への PLC 攻撃を正式警告** — 7 州以上で被害を確認。Rockwell/Allen-Bradley・Siemens・Schneider Electric の産業用制御機器をインターネットから即時切断するよう要請。2026-07-27〜28 のミネソタ州 30+ 施設攻撃 (続報: 2026-07-30 digest 掲載) の広域拡大と連動。([BleepingComputer (2026-08-01)](https://www.bleepingcomputer.com/))

---

## 新規 CVE / Advisory

| CVE/GHSA | 製品・バージョン | CWE / CVSS | バグクラス (条件→シンク→結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-48449 | Adobe Campaign Classic v7 ≤build 9397 (Win/Linux) | CWE-285 / **10.0** | 未認証攻撃者が認可チェック欠落の HTTP エンドポイントに直接リクエスト送信 → サーバー上で任意コード実行 | ACC v7.4.3 build 9398 (APSB26-114, 2026-07-29); 野生悪用未確認 | CVSS 10.0 / 未認証 / 企業メールマーケティング基盤 / 広範デプロイ |
| CVE-2026-48448 | Adobe Campaign Classic v7 ≤build 9397 (Win/Linux) | CWE-89 / **8.6** | 認証済み攻撃者が SQL インジェクションを悪用し任意ファイル読取 → 情報漏えい | ACC v7.4.3 build 9398 (APSB26-114, 2026-07-29); 野生悪用未確認 | CVSS 8.6 / SQL インジェクション / 同一パッチバンドル |
| Coldcard PRNG 欠陥 (CVE 未割当) | Coldcard Mk3 firmware 4.0.1〜5.0.3 / Mk4・Mk5・Q (一部バージョン) | CWE-338 / — | シード種生成時に STM32 HW-RNG が不使用 → 決定論的 PRNG (Yasmarang) で 40 bit エントロピーに低下 → 秘密鍵を総当りで再構築 → ウォレット資産窃取 | 緊急パッチ 2026-07-31 公開; 既存シードの移行必須 (Coinkite Security Advisory) | 実被害 $70M+ 確認済み / ハードウェアウォレット広範利用 / CVE 未割当 |

---

## 国内脆弱性・インシデント

> 直近 3 日間 (2026-08-01〜08-03) に JVN/JPCERT/CC/IPA/Piyolog で確認できた新規の国内脆弱性・インシデント公表はありませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| Axios (AI manifesto open-weight debate) | 2026-08-02 URL "/2026/08/02/" 確認 ✓ |
| BleepingComputer / WeLiveSecurity (ESET H1 2026 Threat Report) | PRSOL.CC mirror URL "/2026/08/01/" 確認 ✓ |
| Microsoft Security Blog / Forbes (CaptiveCrunch / Midnight Blizzard CornFlake RAT) | MS Security Blog 2026-07-31 確認 ✓ / Forbes URL "2026/08/01" 確認 ✓ |
| CoinDesk / Galaxy Research (Coldcard PRNG 欠陥 $70M+) | CoinDesk URL "2026/08/01" 確認 ✓ |
| CyberSecurityNews (HackerOne 政府 ID 義務化) | CyberSecurityNews "2026-08-01" 確認 ✓ |
| BleepingComputer / CISA (水道・廃水 PLC 攻撃警告) | PRSOL.CC mirror URL "/2026/08/01/" 確認 ✓ |
| Adobe PSIRT / APSB26-114 (CVE-2026-48449 / CVE-2026-48448) | Adobe Security Advisory APSB26-114 (2026-07-29) 確認 ✓ |
| Coinkite Security Advisory (Coldcard PRNG CVE 未割当) | Coinkite advisory 2026-07-31 確認 ✓ |
| jvn.jp / jpcert.or.jp / ipa.go.jp / piyolog | 2026-08-01〜03 新規エントリなし |
| thehackernews.com / bleepingcomputer.com / nvd.nist.gov / cisa.gov | 403 — WebSearch スニペット・PRSOL.CC・二次ソースで代替 |

### 集計サマリ

- **巡回ソース数**: 約 20
- **採用件数**: AI=2 / Security=4 / CVE=3 / 国内=0
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-08-01 より前): jackson-core GHSA-r7wm-3cxj-wff9 (2026-07-10) / IBM Cost of Breach 2026 (2026-07-29) / Dolphin X stealer (2026-07-25) / CVE-2026-55040 SharePoint (July Patch Tuesday) / CVE-2026-52887 NocoBase (2026-07-31 = today-3)
  - 重複 (直近 7 ダイジェスト掲載済み・excluded_set 参照): EU AI Act Article 50 施行 (08-02) / Big Sleep Chrome 1,072 bugs (08-02) / Amgen PHI breach (08-02) / Adform JS attack (08-02) / Arch Linux AUR (08-02) / CVE-2026-63223 CodeIgniter4 (08-02) / CVE-2026-67208 Juggle (08-02) / CVE-2026-53609 apostrophe (08-02) / CVE-2026-53606 sanitize-html (08-02) / Anthropic cyber eval breach (08-01) / GPT-5.6 Luna (08-01) / Unit 42 DeepSeek+Hermes (08-01) / Chrome 151 CVE-2026-17650〜17656 (08-01) / Contagious Interview macOS ClickFix (08-01) / SonicWall credential stuffing (08-01) / Kaspersky OctLurk/SilkLurk (08-01) / Laundry Bear CVE-2026-42897 (08-01) / KT Corporation $39M (08-01) / 4G/5G 84 CVEs (08-01) / Copilot Word XPIA worm (07-31) / VMSA-2026-0006 (07-31) / Cisco FMC CVE-2026-20316 (07-31) / Amazon/Sapphire Sleet npm (07-31) / Rails CVE-2026-66066 (07-31) / 生命保険協会 3.7万件 (07-31) / CosmosEscape (07-31) / Claude Mythos Preview HAWK/AES (07-30) / AI pacing letter 1,178人 (07-30) / OpenWrt CVE-2026-53921 (07-30) / Apache Axis2 CVE-2026-66713 (07-30)
  - ミネソタ州水処理施設攻撃 (07-30掲載) → CISA 正式警告 (08-01) は [続報] として採用
  - CaptiveCrunch: Microsoft Security Blog 07-31 初報 → Forbes 08-01 詳報で採用窓内として採用

</details>

---

*生成: keda-digest-bot / 2026-08-03 05:04 JST*
