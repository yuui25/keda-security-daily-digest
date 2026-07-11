# KEDA Daily Digest — 2026-07-12 (JST)

> 採用範囲: 公開日 2026-07-10 〜 2026-07-12 (JST)
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

AI フレームワーク **PraisonAI** で公開から数時間以内に野生悪用された CVSS 10.0 の LLM コード実行欠陥 (CVE-2026-61447) が本日最大の注目点。同日 Apple が OpenAI を連邦裁判所に提訴し「あらゆるレベルでのトレードシークレット窃取」を主張、Siri の Google Gemini 移行と重なりビッグテックのAIパートナーシップの脆弱性が露わになった。Progress Software は ShareFile Storage Zone Controller に CVE 未確定の「信頼できる外部セキュリティ脅威」を受けて即時サーバーシャットダウンを全顧客へ通知、リモートファイル共有製品への警戒が再び高まっている。

## AI 関連ニュース

- **[2026-07-10]** [Apple が OpenAI と同社ハードウェア責任者 Tang Tan・元社員 Chang Liu をトレードシークレット窃取で連邦提訴](https://www.cnbc.com/2026/07/10/apple-openai-lawsuit-trade-secrets.html) — 「あらゆる階層の社員が組織的に Apple の機密情報を窃取した」と訴状に記載; 製品設計・製造プロセス・サプライチェーン戦略が対象; Apple は Siri を ChatGPT から Google Gemini に移行することを確認; OpenAI は「他社のトレードシークレットに関心はない」と声明。*(CNBC / NBC News / ProtoThema)*

- **[2026-07-11]** [Ghostcommit — PNG に埋め込んだ不可視プロンプトインジェクションで AI コードレビュアーを騙し .env ファイルを盗む PR 攻撃が公開](https://www.bleepingcomputer.com/news/security/ghostcommit-hides-prompt-injection-in-images-to-fool-ai-agents-steal-secrets/) — AGENTS.md がコーディングエージェントに PNG 参照を指示 → PNG 内テキストが「.env を ASCII 整数列に変換してモジュール定数として出力」を命令 → CodeRabbit/Bugbot はバイナリ扱いで PNG をスキャンしないため検出ゼロ → 後続セッションで開発者がエージェントに通常の機能追加を依頼すると .env 全内容が漏洩; UMKC の ASSET 研究グループが PoC を公開、Gemma 4 ベースの防御プロトタイプで 50 件中 49 件を検出。*(BleepingComputer / CybersecurityNews / Digital Trends)*

## セキュリティ関連ニュース

- **[2026-07-11]** [PraisonAI CVE-2026-61447 (CVSS 10.0) が公開後数時間以内に野生悪用 — LLM 生成コードをサンドボックスなしに実行する AI フレームワークの設計欠陥](https://cybersecuritynews.com/praisonai-vulnerability-exploited/) — CodeAgent._execute_python() が AST 検証・import 制限・サンドボックスのいずれも欠く; 攻撃者はプロンプトインジェクションで LLM 出力を操作し環境変数全体を窃取; v1.6.78 で修正済み。*(GBHackers / CybersecurityNews / TheHackerWire)*

- **[2026-07-11]** [Progress Software が ShareFile の Storage Zone Controller に「信頼できる外部セキュリティ脅威」を確認 — CVE なし・パッチなし・即時シャットダウン要求](https://www.bleepingcomputer.com/news/security/progress-urges-sharefile-customers-to-shut-down-servers-over-credible-threat/) — クラウド専用 ShareFile アカウントは非対象; オンプレミス Storage Zone Controller のみが影響範囲; Progress は脅威の性質・攻撃者・被害組織の有無を非開示; 過去の関連 CVE (CVE-2026-2699/2701) との関連性も否定; 「クラウド側での無効化だけでは不十分、物理サーバーも手動停止が必要」と通知。*(BleepingComputer / THN / TechTimes)*

- **[2026-07-10]** [CISA が iCagenda Joomla 拡張 CVE-2026-48939 (CVSS 10.0) を KEV に追加 — 未認証 PHP ファイルアップロード RCE が野生悪用中、連邦機関修正期限 2026-07-24](https://www.cisa.gov/news-events/alerts/2026/07/10/cisa-adds-two-known-exploited-vulnerabilities-catalog) — iCagenda 公開イベント投稿フォームのファイル添付エンドポイントが MIME 種別・拡張子検証を欠く; 最新安定版 iCagenda 4.0.8 (2026-06-15 リリース) への更新で修正済み; 同日 Balbooa Forms CVE-2026-56291 も KEV 追加 (07-11 digest 既掲載)。*(CISA / CVEFeed / WindowsNews.ai)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-07-10 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-61447 | PraisonAI < 1.6.78 (pip) | CWE-94 / **10.0** | 攻撃者がプロンプトインジェクションで LLM 出力を操作 → `CodeAgent._execute_python()` が生成コードを AST 検証・import 制限・サンドボックスなしに実行 → 環境変数全窃取・任意コード実行 | [praisonai 1.6.78](https://github.com/MervinPraison/PraisonAI/releases) | 2026-07-11 公開 / CVSS 10.0 / 公開後数時間以内に野生悪用確認 / AI フレームワーク LLM コード実行バイパス |
| CVE-2026-61445 | PraisonAI < 4.6.78 (pip) | CWE-78 / **9.9** | AICoder コンポーネントがカスタムコマンドテンプレートのファイルパス参照を検証しない → 任意ファイルシステムへの書込み + root/SYSTEM 権限でのシェルコマンド実行 | [praisonai 4.6.78](https://github.com/MervinPraison/PraisonAI/releases) | 2026-07-11 公開 / CVSS 9.9 / root 権限 RCE / AI コーディングエージェント基盤 |
| CVE-2026-48939 | iCagenda for Joomla ≤ 4.0.7 | CWE-434 / **10.0** | 未認証ユーザーが公開イベント投稿フォームのファイル添付エンドポイントへ POST → MIME 種別・拡張子・アクセス制御の全チェック欠如 → PHP ファイルをWebルートへ書込み → RCE | [iCagenda 4.0.8 (advisory参照)](https://www.icagenda.com/) (commit 不明) | **CISA KEV 2026-07-10** / CVSS 10.0 / 未認証 / 野生悪用確認 / Joomla 拡張 CWE-434 水平伝播候補 |
| CVE-2026-56763 / GHSA-v8w9-8mx6-g223 | Hono < 4.12.7 (npm) | CWE-1321 / **4.8** | `parseBody({dot: true})` 時に内部ヘルパー `handleParsingNestedValues` がフォームデータキーを無害化しない → `__proto__.x=y` 形式のキーで `Object.prototype` を汚染 → DoS・不正プロパティ操作 | [Hono 4.12.7](https://github.com/honojs/hono/releases/tag/v4.12.7) | 2026-07-11 GHSA 公開 / Web フレームワーク広範利用 / unsafe merge パターンとの組合せで影響拡大 / プロトタイプ汚染水平伝播候補 |

---

## 国内脆弱性・インシデント情報

> 直近2日間 (2026-07-10〜11) に JVN/JPCERT/CC/IPA/Piyolog で確認できた新規の国内脆弱性・インシデント公表はありませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| CNBC / NBC News / ProtoThema (Apple vs OpenAI) | 2026-07-10 CNBC 初報・2026-07-11 他メディア ✓ |
| BleepingComputer / CybersecurityNews (Ghostcommit) | 2026-07-11 05:03 UTC BleepingComputer 公開 ✓ |
| GBHackers / CybersecurityNews / TheHackerWire (PraisonAI CVE-2026-61447/61445) | 2026-07-11 公開・数時間以内野生悪用確認 ✓ |
| BleepingComputer / THN / TechTimes (Progress ShareFile) | TechTimes URL "20260711" 確認 / BleepingComputer 2026-07-11 ✓ |
| CISA.gov alert 2026/07/10 | CVE-2026-48939 + CVE-2026-56291 の KEV 追加 2026-07-10 確認 (URL に日付含む) ✓ |
| GitHub advisories (Hono GHSA-v8w9-8mx6-g223) | 2026-07-11 公開確認 ✓ |
| JVN.jp / JPCERT.or.jp / IPA (July 10-11 新規) | WebSearch 確認: 2026-07-10〜11 新規エントリなし |
| thehackernews.com / bleepingcomputer.com | 403 — WebSearch スニペットで代替 |
| nvd.nist.gov | 403 — WebSearch スニペット代替 |

### 集計サマリ

- **巡回ソース数**: 約 20
- **採用件数**: AI=2 / Security=3 / CVE=4 / 国内=0
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-07-10 より前): Chrome 150 update 27 vulns (2026-07-09 PiunikaWeb) / RoguePlanet CVE-2026-50656 パッチ (2026-07-09 Help Net Security) / ACSC CMS exploitation alert (2026-07-09) / Helix vishing group (2026-07-09 BleepingComputer) / Injective Labs SDK npm 汚染 (2026-07-08) / Ubiquiti SAB-066 (2026-07-02) / ImageMagick CVE-2026-53462 (2026-06-09 GHSA) / Accenture 35GB data breach (2026-07-08 Help Net Security) / DHS HSIN breach (2026-07-01-02)
  - 重複 (直近 7 ダイジェスト掲載済み): CVE-2026-56291 Balbooa Forms (07-11掲載) / CVE-2026-43499 GhostLock (07-10掲載) / CVE-2026-0288 PAN-OS (07-10掲載) / JetBrains 6 CVEs (07-11掲載) / WP-SHELLSTORM (07-11掲載) / MODBEACON (07-11掲載) / Scattered Spider court filing (07-07 公開, 採用窓外) / ChatGPT Work (07-10掲載)
  - 日付不明: 0件

### 主要除外補足

- **Chrome 150 / 27 vulns (CVE-2026-15112, CVE-2026-15129)**: PiunikaWeb 2026-07-09 公開が確認されたため窓外除外
- **RoguePlanet CVE-2026-50656**: Help Net Security / The Register が 2026-07-09 に修正発表を報道 → 窓外除外 (07-09 窓内だった 07-11 digest も未掲載だが、07-12 digest の窓は 07-10 以降のため対象外)
- **Helix data extortion group**: BleepingComputer 2026-07-09 初報 → 窓外除外
- **ACSC CMS exploitation alert**: cyber.gov.au 2026-07-09 公開 → 窓外除外
- **Injective Labs sdk-ts@1.20.21 汚染**: 2026-07-08 npm 公開 → 窓外除外
- **Accenture 35GB breach**: Help Net Security 2026-07-08 公開 → 窓外除外
- **PraisonAI CVE-2026-44338 (authentication bypass, Sysdig)**: 公開日が窓内か不確定のため CVE-2026-61447 (公開日 07-11 確認済) を優先採用

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-07-05 〜 2026-07-11) の全 CVE/GHSA/URL を除外済み。*
