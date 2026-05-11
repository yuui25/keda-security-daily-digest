# KEDA Daily Digest — 2026-05-12 (JST)

> 採用範囲: 公開日 2026-05-10 〜 2026-05-12
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

---

## AI 関連ニュース

### Google Threat Intelligence Group、史上初となる AI 生成ゼロデイエクスプロイトを検出・阻止

- **公開日**: 2026-05-11
- **ソース**: Bloomberg / CNBC / The Register / SecurityWeek / CyberScoop / Help Net Security
- **要約**:
  - Google の Threat Intelligence Group (GTIG) は、犯罪グループが **AI を使って生成したゼロデイエクスプロイト** を野外で使用しようとした最初の事例を検出し、大規模悪用キャンペーンを阻止したと報告した。標的は人気のオープンソース製 Web ベース管理ツール。悪用対象の脆弱性は開発者がハードコードした信頼例外に起因する **2FA バイパス**（意味論的ロジックエラー）で、有効な認証情報さえあれば認証第二要素を完全に回避できる。
  - AI 生成の証拠: エクスプロイトスクリプトには「教育的なドキュメント文字列」「LLM が架空生成した CVSS スコア」「教科書的な Pythonic 書式」「色付き出力クラス」など、大規模言語モデルの出力に特徴的なパターンが複数含まれていた。Google は Gemini・Anthropic Mythos のいずれの関与も否定しつつ、"高い確信" で AI が脆弱性発見と武器化の双方に使われたと判断。GTIG は攻撃者がこの脆弱性を使って「大規模マス悪用イベント」を計画していたと見ている。
  - Google は影響を受けたベンダーへ責任ある開示 (Coordinated Disclosure) を行い、パッチ適用後に情報を公開。AI を使った脆弱性探索・エクスプロイト生成が犯罪者レベルで現実化したことが公式に確認された初のケースとなり、防御側の脅威モデルを根本から見直す必要がある。AI 生成コードには「ハルシネーション CVSS スコア」が含まれていたことも踏まえ、AI 支援ペンテストツールの出力を鵜呑みにしないよう注意すること。
- **リンク**: <https://www.helpnetsecurity.com/2026/05/11/google-ai-vulnerability-exploitation/>

---

### OpenAI が EU に GPT-5.5-Cyber アクセスを開放 — Anthropic は Mythos の EU 提供を保留継続

- **公開日**: 2026-05-11
- **ソース**: CNBC / Benzinga / eWeek / WinBuzzer
- **要約**:
  - OpenAI は 5 月 11 日（月）、EU (欧州委員会) に対して **GPT-5.5-Cyber** の限定プレビューアクセスを付与すると発表した。GPT-5.5-Cyber は先週から厳格な審査を受けたサイバーセキュリティチームへの限定提供が始まっていたモデル。Anthropic はこれに対し、Mythos の EU 提供は「OpenAI と同じ段階ではない」として交渉の進捗差を認め、制限方針を継続。EU は OpenAI・Anthropic 両社に事前アクセスを求めていたが、両社が異なる戦略をとることが鮮明になった。
  - 英国 AI Security Institute (AISI) の評価では、GPT-5.5 は 32 ステップの模擬企業侵害シミュレーションを 10 回中 2 回完了、Mythos は 10 回中 3 回完了。OpenAI は「制限強化版」を一般提供しつつ厳格審査組に「制限緩和版」も提供する二層モデル、Anthropic は約 40 組織への厳格な制限開放のみという対照的な戦略が浮き彫りになった。
  - サイバー特化型高性能 AI モデルの各国政府・規制当局へのアクセス拡大が始まっており、攻撃側・防御側双方の国家レベルでの AI 活用が加速する。開発・運用組織は AI 利用の規制枠組み整備と、AI が関与する脆弱性開示プロセスの整備を今から進める必要がある。
- **リンク**: <https://www.cnbc.com/2026/05/11/openai-eu-cyber-model-anthropic-mythos-gpt.html>

---

## セキュリティ関連ニュース

### [続報] Instructure (Canvas LMS) — ShinyHunters が 5/12 期限後に 330 機関のログインポータルを改ざん・学校別恐喝に移行

- **公開日**: 2026-05-10〜12
- **ソース**: Infosecurity Magazine / Malwarebytes / The Daily Pennsylvanian / Higher Ed Dive / Wikipedia (2026 Canvas security incident)
- **要約**:
  - ShinyHunters が設定した **5 月 12 日の最終期限** が到来したが Instructure が応じず、同グループは世界 **約 330 機関**のCanvas ログインポータルに HTML ファイルを注入・改ざんし、通常サインイン画面を身代金要求画面に置き換えた。Instructure 全体への一括交渉から、**個々の学校・大学への直接恐喝** キャンペーンへと戦術が転換された。一部の学校（ペンシルバニア大学等）が ShinyHunters と個別に交渉を試みていることも報告されている。
  - 初回攻撃（4 月 25 日侵害）から 3 週間以上が経過し、被害機関は Instructure 頼みの復旧を超え、自機関のデータ保護・通知義務・被害者支援を独立して対応しなければならない段階に入った。前回 5 月 9 日ダイジェストで報告した "5/12 期限" が現実のものとなり、教育分野史上最大規模の侵害が新フェーズに突入した。
  - Canvas 利用機関（日本国内の一部大学・専門学校も含む）は、(1) 影響を受ける可能性のある学生・教職員・保護者への法的通知義務の確認、(2) 漏洩データを利用したフィッシング・なりすましへの注意喚起、(3) Canvas 認証情報をほかのサービスで使い回していないかの確認を即座に実施すること。
- **リンク**: <https://www.infosecurity-magazine.com/news/shinyhunters-escalates-canvas/>

---

### Microsoft 2026 年 5 月 Patch Tuesday — Secure Boot 証明書期限前の最重要定期更新

- **公開日**: 2026-05-12 (リリース予定: 10:00 AM PST / 18:00 UTC)
- **ソース**: Zecurit / This Week in Security (May 10 edition)
- **要約**:
  - 本日 5 月 12 日（火）は Microsoft の 5 月 Patch Tuesday のリリース日。セキュリティ業界は今回の更新を「**Secure Boot 証明書の期限切れ (2026-06-26) 前の最後の安全な展開ウィンドウ**」と位置づけており、Windows 環境のブートセキュリティを担う証明書更新が含まれると見られている。この更新を適用しない組織は 6 月 26 日以降に「ブートレベルのセキュリティ障害」が発生するリスクがあり、歴史上最も重要な定期更新の一つと評されている。具体的な CVE 一覧は本稿生成時点（JST 05:12）では未公開のため、確認次第追跡が必要。
  - また直近の CISA 追加 KEV として **CVE-2026-32202**（Windows Protection Mechanism Failure、FCEB 機関への修正期限 5 月 12 日）が含まれており、本 Patch Tuesday での対応が見込まれる。
  - Windows を運用するすべての組織は **今日中** に 5 月 Patch Tuesday を適用し、特に Secure Boot 証明書の更新を確認すること。適用が遅れると 6 月 26 日以降に深刻な運用影響が生じる可能性がある。本記事と並行してリリースされる MSRC の更新ガイドを定期確認すること。
- **リンク**: <https://msrc.microsoft.com/update-guide>

---

### Google Cloud の最新レポートが確認 — AI が初期アクセス・脆弱性悪用・権限昇格を自動化する脅威が本格化

- **公開日**: 2026-05-11
- **ソース**: Google Cloud Blog (Threat Intelligence)
- **要約**:
  - Google Cloud が公開した脅威インテリジェンスブログ「Adversaries Leverage AI for Vulnerability Exploitation, Augmented Operations, and Initial Access」では、AI 支援型攻撃が実際のキャンペーンで確認された事例を体系的に整理した。今回の GTIG AI ゼロデイ発見と合わせて公開された本レポートは、(1) AI による脆弱性発見の自動化、(2) AI によるソーシャルエンジニアリング強化、(3) AI を使った初期アクセスベクトルの生成、の三カテゴリで実事例を収録している。
  - 攻撃者の AI 活用が研究・概念実証段階を超え、**実際のキャンペーンレベルで運用**されていることを Google の実データが裏付けた。従来の「CVE 公開 → 悪用」というサイクルが AI で圧縮されるだけでなく、**AI 自身が未公開の脆弱性を発見・悪用する** 段階に到達しつつある。
  - 組織の脅威モデルを更新し、「AI 生成エクスプロイト」を現実の脅威として扱うこと。セキュリティチームは AI 支援型侵入の痕跡（"教育的" コードコメント・架空 CVE 引用・テンプレート的 Python スクリプト等）に対する検知ルールを整備すること。
- **リンク**: <https://cloud.google.com/blog/topics/threat-intelligence/ai-vulnerability-exploitation-initial-access>

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 | 影響/CVSS | リンク |
|--------|--------|------|-----------|--------|
| 2026-05-11 | Apache HTTP Server 2.4 複数脆弱性 (ScanNetSecurity) | ScanNetSecurity が 5 月 11 日付で Apache HTTP Server 2.4 の複数脆弱性に関する注意喚起を掲載。CVE-2026-23918 (mod_http2 double-free, CVSS 8.8) を中心とする 2.4.67 での修正内容を国内向けに解説。国内の Apache 2.4.66 以前を運用する組織は 2.4.67 へのアップグレードを要確認。 | CVSS 最大 8.8 | <https://scan.netsecurity.ne.jp/article/2026/05/11/55225.html> |
| 〜2026-05-12 | Canvas LMS 侵害の国内教育機関影響 | 日本国内でも Canvas LMS を採用している大学・専門学校が存在する。ShinyHunters の 5/12 期限到来により約 330 機関のポータルが改ざんされており、国内採用機関も今すぐ影響確認と学生・教職員への通知体制を整備すること。JVN / JPCERT からの個別注意喚起は未確認。 | 高 (データ漏洩) | <https://www.infosecurity-magazine.com/news/shinyhunters-escalates-canvas/> |
| 2026-05-12 (予定) | Microsoft 5 月 Patch Tuesday — Secure Boot 証明書更新を含む最重要更新 | 日本時間深夜 (2026-05-13 03:00 JST) にリリース予定。Windows 環境を運用するすべての国内組織は早急な適用計画を策定すること。Secure Boot 証明書の更新が含まれ、未適用の場合 2026-06-26 以降に起動障害が生じるリスクがある。JPCERT/CC からの対応勧告を待たずに WSUS / Intune / SCCM での展開準備を開始すること。 | 高 | <https://msrc.microsoft.com/update-guide> |

---

## 本日のサマリ

本日の最大トピックは **Google GTIG による「史上初の AI 生成ゼロデイエクスプロイト検出」**（5/11）。犯罪グループが AI を使って人気オープンソース管理ツールの 2FA バイパスゼロデイを発見・武器化し、大規模攻撃を計画していた。Google が事前に阻止したため被害は免れたが、AI がエクスプロイト開発ツールとして実用段階に達したことが公式に確認された。AI 開発組織は脅威モデルの根本的な更新が急務。同日には **OpenAI の EU 向け GPT-5.5-Cyber 開放と Anthropic の Mythos 制限継続**も明らかになり、サイバー特化型高性能 AI の管理・規制の国際的な分断が進んでいる。セキュリティ面では **Canvas/ShinyHunters** が本日（5/12）の最終期限到来で 330 機関のポータル改ざんに踏み切り、日本国内の利用機関を含め即時の確認・通知が必要。また今日は **Microsoft Patch Tuesday** のリリース日でもあり、Secure Boot 証明書更新を含む歴史的重要度の高い更新が配信される予定であるため、Windows 環境の管理者は迅速な適用計画を立てること。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 30 (AI/Security/国内カテゴリ、WebSearch + WebFetch)
- 採用件数: AI=2 (+ Google Cloud Blog で補足 1) / Security=2 / 国内=3 (テーブル形式)
- 除外理由内訳:
  - 古すぎ (採用窓外 3 日以上前): GPT-5.5 Instant リリース (05-05), Braintrust AWS 侵害 (05-06), Vibe Coding/RedAccess (05-07/08), CallPhantom (05-07), Cushman & Wakefield ShinyHunters (05-08), MuddyWater Teams (05-06), MetInfo CMS CVE-2026-29014 (05-05 THN ミラー確認), Pack2TheRoot CVE-2026-41651 (04末), EmoCheck CVE-2026-28704 JVN (04-10), baserCMS JVN#20837860 (03-31), Tokyo FM 侵害 (2026-01), MongoBleed CVE-2025-14847 (2025-12), Fortinet 2FA bypass CVE-2020-12812
  - 重複 (過去 7 日分 excluded_set に既出): CVE-2026-0300 (PAN-OS), CVE-2026-6973 (Ivanti EPMM), CVE-2026-43284/43500 (Dirty Frag), CVE-2026-31431 (Copy Fail), CVE-2026-42354 (Sentry), CVE-2026-23918 (Apache HTTP/2) ※ScanNetSecurity の 5/11 記事は国内ドメスティック情報として参照掲載, Canvas 初報・5/9-11 続報 (過去 digest 掲載済み, 5/12 展開は新規として採用)
  - 日付不明・採用窓外: AiFrame Chrome 拡張 (02-2026 確認), Suzuki Motorcycle India (2023 確認)
  - データ取得失敗 (HTTP 403 等): thehackernews.com, bleepingcomputer.com, securityweek.com (一部), helpnetsecurity.com (一部), sharkstriker.com, jvn.jp, jpcert.or.jp, bloomberg.com, malwarebytes.com, infosecurity-magazine.com, zecurit.com, venturebeat.com — 検索スニペット・複数ミラーの整合確認で代替
- Microsoft 5 月 Patch Tuesday: JST 05:12 時点では未公開のため具体的 CVE は記載不可。本稿生成後（日本時間 5/13 03:00 頃リリース）に追跡要
- 取得済みソースで日付確認: Bloomberg URL パターン (/2026-05-11/), CNBC URL (/2026/05/11/), Google Cloud Blog WebFetch 直接確認 (Publication Date: May 11, 2026)

</details>
