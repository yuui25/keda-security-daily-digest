# KEDA Daily Digest — 2026-07-14 (JST)

> 採用範囲: 公開日 2026-07-12 〜 2026-07-14 (JST)
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

UK 金融規制当局 (BoE/PRA/FCA) が **Critical Third Party (CTP) 指定制度** を 7/13 に正式稼働させ、Microsoft Ireland Ops・Google Cloud EMEA・AWS EMEA SARL・Oracle UK が初の指定対象となった。AI による自動脆弱性発見の加速で 2026 年の CVE 公開数は 66,000 件超のペースに達し、本日の **Microsoft Patch Tuesday (7月分)** は ~127 CVE と過去最多水準と予測されている (生成時点 20:00 UTC では正式未発表)。CERN 科学計算基盤 **DIRAC** で CVSS 9.9 の CVE が 2 件同日公開 — SQL injection と eval() への二経路 RCE で 2013 年以降の全バージョンが影響範囲。"Nightmare-Eclipse" 研究者が予告していた 7/14 ゼロデイ一斉公開は不発に終わり、GitHub・GitLab 双方でアカウント停止を受けている。

## AI 関連ニュース

- **[2026-07-13]** [UK が金融セクター向け Critical Third Party 制度を正式稼働 — Microsoft Ireland Ops/Google Cloud EMEA/AWS EMEA SARL/Oracle UK を初指定、BoE/PRA/FCA が共同監督開始](https://www.insurancejournal.com/news/international/2026/07/13/uk-critical-third-party-regime-launch/) — 金融機関のクラウド依存リスクを規制当局が直接管理する体制が英国で初めて発効; IT サービス中断時の 72 時間以内インシデント報告・年次レジリエンス評価が CTP 各社に義務付け; EU DORA との制度的調整が今後の課題。*(Insurance Journal / harro.com)*

- **[2026-07-13]** [HHS が ChatGPT で病院監査報告を自動スキャン — エラー率非公開・異議申立て手続きなしでメディケイド資金停止判定を実施](https://www.techtimes.com/articles/321847/20260713/hhs-aero-chatgpt-medicaid-funding.htm) — 複数の医療機関が AI 判定根拠の開示請求を試みるも HHS が技術仕様の公開を拒否; Accountable.US と患者権利団体が FOIA 訴訟を準備中; 医療 AI の「ブラックボックス行政判断」として先例となる可能性。*(TechTimes)*

- **[2026-07-13]** [Google Gemini 3.5 Pro が完全再構築後に 7/17 GA を目標 — 2M トークンコンテキスト・再帰的ツール呼出しの構造的失敗を修正済みと非公式報告](https://www.techtimes.com/articles/321851/20260713/gemini-35-pro-rebuild-july17-ga.htm) — 旧版で SVG 生成・再帰ツール呼出しの壊滅的失敗が確認され非公開で全面再構築; 公式 Google 発表はなく情報筋の報告のみ; 2M トークンコンテキストは Gemini 1.5 Pro からの継続機能で信頼性向上が今回の主眼。*(TechTimes)*

- **[2026-07-13]** [AI による自動脆弱性発見で 2026 年の CVE 公開数が 66,000 件超ペース — 前年比 30% 増、本日の Microsoft Patch Tuesday も ~127 CVE と過去最多水準](https://www.darkreading.com/vulnerabilities-threats/ai-assisted-vulnerability-discovery-cve-surge-2026) — AI ファジング・コード解析ツールが研究者と攻撃者双方の脆弱性発見速度を加速; Microsoft 社内でも GitHub Copilot Autofix が脆弱なコードパターンの自動検出に活用されパッチ準備期間が短縮; 2027 年には 90,000 件超を予測する調査も。*(Dark Reading)*

## セキュリティ関連ニュース

- **[2026-07-14]** [Microsoft Patch Tuesday 2026-07 — ~127 CVE 修正予定 (生成時点 20:00 UTC で正式公開前・詳細は MSRC 参照)](https://msrc.microsoft.com/update-guide/) — 7 月第 2 火曜として定例公開予定; 修正総数は月平均 (~80〜90 件) を大幅に上回る見通し; "Nightmare-Eclipse" が 7/14 に予告していた RCE 系ゼロデイは正式公開されず、予告の 7 件のゼロデイ (RedSun/UnDefend/BlueHammer/YellowKey/GreenPlasma/MiniPlasma/RoguePlanet) はすべて既パッチ済みとコミュニティが確認。*(MSRC / security community)*

- **[2026-07-12〜13]** [Nightmare-Eclipse が 7/14 ゼロデイ一斉公開を断念 — GitHub・GitLab のアカウント停止を受け「骨砕き級」エクスプロイト公開は不発](https://www.bleepingcomputer.com/news/security/nightmare-eclipse-withdraws-july14-zero-day-dump/) — 研究者本人が SNS で「RoguePlanet の長期開発で疲弊」と説明し 7/14 一斉公開を断念; ただし 7 件のゼロデイのうち未パッチのものが外部に流出した可能性は否定できず; セキュリティコミュニティは Patch Tuesday との連動に引き続き警戒。*(BleepingComputer / security community)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-07-12 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-61667 / GHSA-m4m7-4cw8-62j6 | DIRAC ≥6.0,<8.0.79 / ≥8.1.0a1,<9.0.22 / ≥9.1.0,<9.1.10 (pip) | CWE-89+CWE-95 / **9.9** | FileCatalog DatasetManager がユーザー入力を f-string で SQL に展開し直接実行 → SQL injection; DB 結果を `eval()` に無害化なく渡す → 任意コード実行 | [v8.0.79](https://github.com/DIRACGrid/DIRAC/releases/tag/v8.0.79) / [v9.1.10](https://github.com/DIRACGrid/DIRAC/releases/tag/v9.1.10) | 2026-07-13 GHSA 公開 / CVSS 9.9 / SQLi + eval RCE 二段構え / CERN/HEP グリッド基盤全バージョン影響 |
| CVE-2026-45579 / GHSA-9jpv-c7p4-997x | DIRAC ≥6.0,<8.0.79 / ≥8.1.0a1,<9.0.22 / ≥9.1.0,<9.1.10 (pip) | CWE-95 / **9.9** | `export_getRequestCountersWeb` がユーザー指定 `groupingAttribute` を "Request." プレフィックス後に `eval()` → `__class__.__init__.__globals__` 等の dunder 経由で `os.system` → ホスト完全制御 | [v8.0.79](https://github.com/DIRACGrid/DIRAC/releases/tag/v8.0.79) / [v9.1.10](https://github.com/DIRACGrid/DIRAC/releases/tag/v9.1.10) | 2026-07-13 GHSA 公開 / CVSS 9.9 / dunder 経由 eval RCE / 科学計算グリッド水平伝播候補 |

---

## 国内脆弱性・インシデント情報

> 直近2日間 (2026-07-12〜13) に JVN/JPCERT/CC/IPA/Piyolog で確認できた新規の国内脆弱性・インシデント公表はありませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| Insurance Journal / harro.com (UK CTP 制度正式稼働) | 2026-07-13 URL "/2026/07/13/" 確認 ✓ |
| TechTimes (HHS AERO/ChatGPT メディケイド資金停止) | 2026-07-13 URL "20260713" 確認 ✓ |
| TechTimes (Gemini 3.5 Pro 完全再構築・7/17 GA 目標) | 2026-07-13 URL "20260713" 確認 ✓ |
| Dark Reading (AI 自動脆弱性発見・CVE 66,000 件超ペース) | 2026-07-13 記事確認 ✓ |
| MSRC (Microsoft Patch Tuesday 2026-07) | 2026-07-14 定例公開予定 (生成時点 20:00 UTC では未発表) — URL のみ掲載 |
| BleepingComputer / security community (Nightmare-Eclipse 断念) | 2026-07-12〜13 SNS 投稿・コミュニティ報告確認 ✓ |
| GitHub Advisories (GHSA-m4m7-4cw8-62j6 / CVE-2026-61667 DIRAC) | 2026-07-13 GHSA 公開確認 ✓ |
| GitHub Advisories (GHSA-9jpv-c7p4-997x / CVE-2026-45579 DIRAC) | 2026-07-13 GHSA 公開確認 ✓ |
| jvn.jp / jpcert.or.jp / ipa.go.jp / piyolog | WebSearch 確認: 2026-07-12〜13 新規エントリなし |
| thehackernews.com / bleepingcomputer.com | 403 — WebSearch スニペットで代替 |
| nvd.nist.gov | 403 — WebSearch スニペット代替 |

### 集計サマリ

- **巡回ソース数**: 約 20
- **採用件数**: AI=4 / Security=2 / CVE=2 / 国内=0
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-07-12 より前): GhostApproval Wiz Research (The Register 2026-07-08) / Rogue Agent Dialogflow CX (Varonis 2026-07-07) / Google Africa AI Lab (2026-07-01) / node-tar CVE-2026-59874/59873/59871 (THREATINT 確認: 元公開 2026-07-08)
  - 重複 (直近 7 ダイジェスト掲載済み): GPT-5.6 Sol Ultra CDC Conjecture (07-13掲載) / Agentic AI Runtime Security GA (07-13掲載) / FRB AI 委員会設立 (07-13掲載) / jscrambler npm supply chain (07-13掲載) / U-Boot BRLY-2026-037〜042 (07-13掲載) / Zimbra Classic XSS (07-13掲載) / File Browser CVE-2026-54088 (07-13掲載) / ImageMagick CVE-2026-61861 (07-13掲載) / PraisonAI Platform CVE-2026-61442 (07-13掲載) / PraisonAI CVE-2026-61447/61445 (07-12掲載) / Ghostcommit PNG injection (07-12掲載) / Apple vs OpenAI (07-12掲載) / Progress ShareFile 脅威 (07-12掲載)
  - ハルシネーション除外: Perplexity $500M 調達 (実際は 2025-05) / Cognition AI $300M (実際は 2026-05) / CVE-2025-47981 SPNEGO NEGOEX (CVE 番号が 2025 年、NVD で 2025-07 修正済みを確認)
  - 日付不明: 0件

### 主要除外補足

- **CVE-2025-47981 (SPNEGO NEGOEX, CVSS 9.8)**: 複数検索結果が「2026年7月 Patch Tuesday」として引用するが CVE 番号は 2025 年であり NVD 確認で 2025-07 修正済み → 除外
- **Perplexity $500M / Cognition AI $300M**: AI ニュースまとめで「2026年7月」として引用されたが検証で前年・前月の資金調達と判明 → 除外 (hallucination)
- **GhostApproval (Wiz Research)**: 7/13 週次レポートに掲載されているが元の Wiz/The Register 公開日は 2026-07-08 → 窓外除外
- **node-tar CVE-2026-59874/59873/59871**: 一部 URL に /2026/07/12/ パターンが存在するが 07-13 digest の THREATINT 調査で元公開日 2026-07-08 を確認済み → 窓外除外 (07-13 digest 除外補足と一致)
- **Microsoft Patch Tuesday 個別 CVE**: 生成時点 (2026-07-13 20:00 UTC) は 7/14 UTC 17:00 発表予定より前のため個別 CVE 詳細を取得不能 → スケジュール情報のみ掲載

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-07-07 〜 2026-07-13) の全 CVE/GHSA/URL を除外済み。*
