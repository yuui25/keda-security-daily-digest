# KEDA Daily Digest — 2026-08-23 (JST)

> 採用範囲: 公開日 2026-08-21 〜 2026-08-23
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Anthropic が Claude Mythos 5 を Claude Security (Enterprise 公開ベータ) に統合し、$35M のオープンソース防衛基金と米国重要インフラ向けの Project Glasswing を発表した。OpenAI は GPT-5.6 Sol API 価格を3ヶ月間20%超引き下げ Claude Opus 5 との競争を激化させ、Anthropic は Claude Academy を公開した。セキュリティでは Check Point が Microsoft Defender の署名済みドライバ BTR.sys を LOLBin として悪用しカーネルレベルで EDR・AV を無効化する手法 (BTR_CLI PoC, CVE なし・パッチ不可) を Black Hat/DEF CON 34 で発表した。Microsoft Entra ID に CVSS 10.0 のデシリアライゼーション RCE (CVE-2026-69836) が公開されたが Microsoft がサービス側で修正済みのためユーザー対応は不要。Google TI は Russia-nexus クラスター UNC6293/UNC7005/UNC5976 が Google OAuth・WhatsApp の正規フローを悪用して欧米の政府・学術・防衛関係者の認証トークンを窃取していると公表した。

---

## AI 関連ニュース

- **[2026-08-21]** [Anthropic Brings Claude Mythos 5 to Claude Security — $35M Open-Source Fund and Project Glasswing for Critical Infrastructure](https://www.marktechpost.com/2026/08/21/anthropic-brings-claude-mythos-5-to-claude-security/) — Anthropic が Claude Mythos 5 を Claude Security (Enterprise 公開ベータ) に統合し、GitHub リポジトリ接続・データフロー追跡・CWE/重大度付き修正案返却を実現。同日 $35M のオープンソース防衛クレジット基金と、米国重要インフラ事業者向けの Mythos-class アクセスを提供する Project Glasswing を発表 *(Anthropic Blog / MarkTechPost 2026-08-21)*

- **[2026-08-22]** [OpenAI Cuts GPT-5.6 Sol API Prices by Over 20% for Three Months to Undercut Claude Opus 5](https://www.business-standard.com/technology/tech-news/openai-cuts-developer-pricing-for-gpt-5-6-sol-model-by-more-than-20-126082200107_1.html) — OpenAI がフロンティアモデル GPT-5.6 Sol の API 価格を3ヶ月間限定で20%超引き下げ。入力 $5→$4/M トークン (20%減)・出力 $30→$20/M トークン (33%減) で Anthropic Claude Opus 5 より安価に。少なくとも 2026-11-21 まで適用 *(Business Standard / ProPakistani 2026-08-22)*

- **[2026-08-22]** [Anthropic Launches Claude Academy — AI Learning Hub with Courses, Badges, and Personalized Recommendations](https://releasebot.io/updates/anthropic/claude) — Anthropic が Claude Academy を公開。AI の安全・効果的な活用を学ぶコース・チュートリアル・バッジ・パーソナライズドレコメンデーションを提供。実践的な AI フルエンシー、委任・検証・学習スキルの向上を目的 *(Anthropic / Releasebot 2026-08-22)*

---

## セキュリティ関連ニュース

- **[2026-08-21]** [Check Point Research "BTR Reforged": Microsoft Defender's BTR.sys Weaponized as Kernel Operation Primitive — No CVE, No Patch Possible](https://research.checkpoint.com/2026/btr-reforged-weaponizing-defenders-remediation-driver-as-a-kernel-operation-primitive/) — Check Point の Jiří Vinopal が Black Hat USA 2026 / DEF CON 34 で発表。Defender の署名済みブートタイム修復ドライバ BTR.sys のトランザクション形式をリバースエンジニアリングし、攻撃者制御の操作を実行するユーティリティ BTR_CLI を公開。Windows 7〜11 25H2 に対応し WDAC/Vulnerable Driver Blocklist でブロック不可 (Defender 自体が使用するため)。現時点で実悪用の報告なし *(Check Point Research / The Hacker News 2026-08-21)*

- **[2026-08-21]** [CVE-2026-69836 (CVSS 10.0): Microsoft Entra ID Deserialization RCE — "Exploited" Status Corrected — Already Fully Patched by Microsoft Server-Side](https://www.helpnetsecurity.com/2026/08/21/microsoft-entra-id-vulnerability-cve-2026-69836/) — Entra ID クラウド IAM に CVSS 10.0 のデシリアライゼーション RCE。Microsoft Principal Security Engineer Robert Fitzpatrick が発見。当初「実エクスプロイト確認」として公開されたが Microsoft が「未エクスプロイト」に訂正。Microsoft がサービス側で修正済みのためユーザー対応不要 *(HelpNetSecurity / it-learn.io 2026-08-21)*

- **[2026-08-21]** [Russia-Linked UNC6293/UNC7005/UNC5976 Abuse Google OAuth and WhatsApp Linking to Steal Auth Tokens from Government, Academic, and Defense Targets](https://cloud.google.com/blog/topics/threat-intelligence/distinct-clusters-target-individuals-of-interest-to-russia) — Google TI が Ice Relic (APT29/Cozy Bear) 傘下の 3 クラスターを公開。正規の Google/Microsoft OAuth フロー・WhatsApp アカウントリンクを悪用し、欧米の学術・外交・防衛・シンクタンク関係者の認証トークンを窃取。1 グループはフィンランド作戦センターを偽装して被害者を攻撃者制御のクラウドプロジェクトにリダイレクト *(Google Cloud TI / The Register 2026-08-21)*

- **[2026-08-21]** [SickKids Children's Hospital Discloses Data Breach via Third-Party Careers Site Vulnerability — Employee and Applicant PII Exposed](https://www.theregister.com/cyber-crime/2026/08/21/sickkids-childrens-hospital-bandages-up-careers-website-after-intruder-breaks-in/5291098) — カナダのトロント小児病院 SickKids が7月9日に第三者製採用サイトソフトウェアへの不正アクセスを検知と公表。現・元職員および求職者の個人情報が影響を受ける可能性 (患者情報への影響なし)。被害者に24ヶ月のクレジット監視を提供 *(The Register / BleepingComputer 2026-08-21)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-08-21 以降 / CISA KEV 追加 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-69836 | Microsoft Entra ID (2026-08-21 修正以前のクラウドインスタンス) | CWE-502 / **10.0** | 未認証攻撃者がネットワーク経由で非信頼データをデシリアライズさせ → 任意コード実行 (ユーザー操作不要・低複雑度) | Microsoft がクラウド側で修正済み (クローズドソース); ユーザー対応不要; 公開 **2026-08-21** | CVSS 10.0 / クラウド IAM 基盤 / 修正済みだがバグクラス (CWE-502) は派生調査起点に有効 |
| GHSA-hrwp-4hh9-c8r8 / CVE-2026-59989 | Phalcon/cphalcon ≤ 5.15.0 | CWE-94 / 未確認 | Volt テンプレートコンパイラの `join` フィルタが引数バイトをエスケープせず生成 PHP コードに直接結合 → 攻撃者制御テンプレートをコンパイル時に任意 PHP コード注入 → `require` 実行で RCE | Phalcon 5.16.0 で修正; GHSA 公開 **2026-08-21** (CVE 初回開示 2026-07-10) | コンパイラ型 SSTI/コードインジェクション / Volt テンプレートエンジン系バリアントハント起点 |
| GHSA-2cp2-2r3c-7p7r / CVE-2026-68508 | hydra-core (pip) ≤ 1.3.3 | CWE-94 / **7.8** | `hydra.utils.instantiate()` が `_target_` と引数を信頼して呼び出し → 非信頼 YAML config から任意 Python オブジェクトをインスタンス化 → コード実行 | hydra-core 1.3.4 で修正; GHSA 公開 **2026-08-21** (CVE 初回開示 2026-07-24) | CVSS 7.8 / ML 設定フレームワーク広範利用 / untrusted config 経由の ACE / fix commit 公開済み |
| GHSA-26w5-6g95-gj28 / CVE-2026-64679 | atlantis (Go) ≥ 0.19.8, < 0.45.0 | CWE-22 / **8.1** | 攻撃者制御のワークスペース値が内部パス構築前に検証されず → パストラバーサルで Atlantis プロセス権限による意図外ディレクトリ作成・削除・再利用 → IaC パイプライン完全性侵害 | atlantis 0.45.0 で修正; GHSA 公開 **2026-08-21** (CVE 初回開示 2026-07-02) | CVSS 8.1 / Terraform 自動化基盤 / IaC パイプラインへの横移動起点 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 | CVSS | 参照 |
|---|---|---|---|---|
| 2026-08-21 | JVNVU#90210212 / CVE-2026-76131, CVE-2026-76137 | Yamaha VOCALOID6 Editor: ハードコード認証情報 (CVE-2026-76131, CVSS 5.3) およびローカル名前付きパイプの認証欠如による同一ユーザーコンテキストからの権限昇格 (CVE-2026-76137, CVSS 3.3) | v3 5.3 / 3.3 | [JVNVU#90210212](https://jvn.jp/en/vu/JVNVU90210212/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| marktechpost.com (Anthropic Claude Security / Mythos 5 / Project Glasswing) | URL パターン確認 ✓; 2026-08-21 公開確認 ✓ |
| business-standard.com / propakistani.pk (OpenAI GPT-5.6 Sol price cut) | **WebFetch 直接取得成功** ✓; 2026-08-22 公開確認 ✓; 20%超値下げ確認 ✓ |
| releasebot.io/updates/anthropic/claude (Claude Academy) | WebSearch スニペット 2026-08-22 確認 ✓ |
| research.checkpoint.com (BTR Reforged / BTR.sys) | URL パターン確認 ✓; The Hacker News 2026-08-21 報道確認 ✓ |
| helpnetsecurity.com (CVE-2026-69836 Entra ID CVSS 10.0) | WebSearch スニペット 2026-08-21 公開確認 ✓; "Exploited" 訂正確認 ✓ |
| cloud.google.com (UNC6293/UNC7005/UNC5976 OAuth token theft) | **WebFetch 直接取得成功** ✓; 2026-08-21 公開確認 ✓; 3 クラスター確認 ✓ |
| theregister.com (SickKids hospital breach) | URL パターン確認 ✓; 2026-08-21 公開確認 ✓ |
| github.com/advisories/GHSA-hrwp-4hh9-c8r8 (Phalcon Volt) | **WebFetch 直接取得成功** ✓; Published: August 21, 2026; CVE-2026-59989 確認 ✓ |
| github.com/advisories/GHSA-2cp2-2r3c-7p7r (hydra-core) | **WebFetch 直接取得成功** ✓; Published: August 21, 2026; CVSS 7.8 確認 ✓ |
| github.com/advisories/GHSA-26w5-6g95-gj28 (atlantis path traversal) | **WebFetch 直接取得成功** ✓; Published: August 21, 2026; CVSS 8.1 確認 ✓ |
| jvn.jp/en/vu/JVNVU90210212/ (Yamaha VOCALOID6) | WebSearch スニペット 2026-08-21 公開確認 ✓; CVE-2026-76131/76137 確認 ✓ |
| jvn.jp / jpcert.or.jp / ipa.go.jp (その他) | EGRESS_BLOCKED — 直接確認不可 |

### 集計サマリ

- **巡回ソース数**: 約 30
- **採用件数**: AI=3 / Security=4 / CVE=4 / 国内=1
- **除外理由内訳**:
  - GHSA date mismatch (GHSA filter date ≠ 実際の公開日): GHSA-x2rj-828p-hx9m (Xinference, WebFetch で July 13, 2026 確認); JSONata 系 GHSA (同様に July 13 確認)
  - 採用窓外 (公開日 <2026-08-21): n8n Aug 20 advisories; Manic Android malware (Aug 20)
  - 重複 (excluded_set 参照): Zimbra CVE-2026-73570 KEV (08-21 digest 掲載済み); CVE-2026-59310 VMware vCenter (08-20/22 digest 掲載済み); GHSA-mqjf-5f49-2fjh GeoTools (08-16 digest 掲載済み)
  - CISA KEV 新規追加 (2026-08-22): 確認できなかった (Zimbra KEV は Aug 21 追加で excluded_set 済み)
  - 取得失敗ソース (EGRESS_BLOCKED): research.checkpoint.com, guardianmssp.com, thehackernews.com, bleepingcomputer.com, cisa.gov, nvd.nist.gov, jvn.jp, jpcert.or.jp, ipa.go.jp, securityweek.com, portswigger.net, watchtowr.com, medium.com

</details>

---

*生成: keda-digest-bot / 2026-08-23 05:04 JST*
