# KEDA Daily Digest — 2026-05-23 (JST)

> 採用範囲: 公開日 2026-05-21 〜 2026-05-23
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

OpenAI が機密 S-1 を SEC に申請し、$852B〜$1T 評価での秋 IPO 競争が本格化。AI エージェントのセキュリティ統治への対応として Microsoft・Trust3 AI・ASAPP が相次いで製品・OSS ツールを投入し、エージェント安全管理基盤の整備が加速。脆弱性面では Cisco Secure Workload と Ubiquiti UniFi OS に CVSS 10.0 が同期間に公開されたほか、Langflow・Trend Micro Apex One が CISA KEV に追加され、AI ワークフロープラットフォームへの実攻撃が公式確認された。

---

## AI 関連ニュース

- **[2026-05-22]** [OpenAI が SEC に機密 S-1 を申請 — Goldman Sachs・Morgan Stanley 主幹事で 2026 年秋上場目標、評価額 $852B〜$1T](https://fortune.com/2026/05/22/openai-ipo-filing-1-trillion-may-finally-answer-these-big-questions/) — ChatGPT 月間 ARR $2B 超を背景に史上最大 IPO 候補の一つとして SEC に機密申請、15 日間のロードショー前に公開される見通し。 *(Fortune)*

- **[2026-05-21]** [Anthropic 共同創業者 Jack Clark が Oxford 講演で「AI が 1 年以内に Nobel 級科学的発見に貢献」と予測](https://www.neuralbuddies.com/p/ai-news-recap-may-22-2026) — 加えて「2 年以内に二足歩行ロボットが現場普及」「18 カ月以内に AI 単独経営で百万ドル収益企業が誕生」とも主張。 *(NeuralBuddies)*

- **[2026-05-21]** [Microsoft Purview に Anthropic Claude コネクタ (Claude Compliance API) が追加 — Claude Enterprise/Console/API の利用ログを Purview 上で横断調査・監査](https://www.microsoft.com/en-us/security/blog/2026/05/21/whats-new-in-microsoft-security-may-2026/) — シャドウ AI 対策として Claude 利用状況の一元可視化とコンプライアンス調査に対応。 *(Microsoft Security Blog)*

- **[2026-05-21]** [Microsoft Agent 365 が GA、Windows 365 for Agents プレビュー拡大でシャドウ AI エージェント (OpenClaw・Claude Code 含む) の検出・統治が追加](https://www.microsoft.com/en-us/security/blog/2026/05/21/whats-new-in-microsoft-security-may-2026/) — ローカル・クラウド双方の AI エージェントを Cloud PC 環境で監査・アクセス制御する統一プラットフォームに。 *(Microsoft Security Blog)*

- **[2026-05-21]** [Microsoft が RAMPART・Clarity を OSS 公開 — AI エージェント開発の CI/CD パイプラインに red teaming と設計安全性チェックを統合](https://www.microsoft.com/en-us/security/blog/2026/05/20/introducing-rampart-and-clarity-open-source-tools-to-bring-safety-into-agent-development-workflow/) — RAMPART は PyRIT ベースの Pytest ネイティブ安全テストフレームワーク、Clarity は実装前リスクを洗い出す構造化レビューツール。 *(Microsoft Security Blog / The Register)*

- **[2026-05-22]** [Trust3 AI が MCP Security を発表 — Model Context Protocol 準拠の企業 AI エージェントに認証・認可・監査の統一トラストレイヤーを提供](https://www.helpnetsecurity.com/2026/05/22/new-infosec-products-of-the-week-may-22-2026/) — エージェントとビジネスデータ・アプリの接続を安全に仲介する新スタンダードとして提案。 *(Help Net Security)*

- **[2026-05-22]** [ASAPP が Continuous Red Teaming を AI 評価フレームワークに統合 — 静的評価から常時対抗テストへ、本番モデルのガードレール迂回を早期検出](https://www.helpnetsecurity.com/2026/05/22/new-infosec-products-of-the-week-may-22-2026/) — 生成 AI システムへの継続的な敵対的プロービングを開発ライフサイクルに組み込む。 *(Help Net Security)*

- **[2026-05-22]** [Babel Street が Insights Investigator を発表 — アナリスト指示で AI エージェントが自律的に調査を実行する OSINT/情報分析製品](https://www.helpnetsecurity.com/2026/05/22/new-infosec-products-of-the-week-may-22-2026/) — 検索補助から AI 主導の実行型調査へのシフトを体現するセキュリティインテリジェンスプロダクト。 *(Help Net Security)*

---

## セキュリティ関連ニュース

- **[2026-05-22]** [KimWolf DDoS-for-hire ボットネット運営者カナダ人 Jacob Butler (23) が米加当局に逮捕・訴追 — 30 Tbps 超の記録的 DDoS を含む世界規模攻撃に関与](https://krebsonsecurity.com/2026/05/alleged-kimwolf-botmaster-dort-arrested-charged-in-u-s-and-canada/) — 同時に DDoS-for-hire 45 プラットフォームを標的に差押え令状が発動。 *(Krebs on Security)*

- **[2026-05-21]** [Showboat — 中国系脅威アクターが中東通信事業者を Linux 向けモジュール型ポスト侵害フレームワークで 2022 年から継続標的と判明](https://thehackernews.com/2026/05/showboat-linux-malware-hits-middle-east.html) — SOCKS5 プロキシバックドア機能を持ち、C2 ノードが中国・成都にジオロケーション。 *(The Hacker News)*

- **[2026-05-22]** [[続報] Drupal CVE-2026-9082 PostgreSQL SQL インジェクション — 公開後 65 カ国 6,000 サイト超への 15,000+ 件の攻撃試行を Imperva が観測](https://www.imperva.com/blog/imperva-customers-protected-against-cve-2026-9082-in-drupal-core/) — 未修正の匿名 SQLi は急拡大中、対象バージョン 10.4〜11.3 系は即時アップグレード推奨。 *(Imperva)*

- **[2026-05-21]** [TrendAI が Apex One ゼロデイ CVE-2026-34926 (CVSS 6.7) を修正 — CISA が KEV 追加、連邦機関は 6/4 までのパッチ適用義務化](https://www.securityweek.com/trendai-patches-apex-one-zero-day-exploited-in-the-wild/) — 管理サーバーへのディレクトリトラバーサルで鍵 DB テーブルを改ざん、配下全エンドポイントへ悪意コードを伝播。 *(SecurityWeek)*

- **[2026-05-21]** [Cisco Secure Workload に CVSS 10.0 の REST API 認証欠落 CVE-2026-20223 — 未認証で Site Admin 権限取得・クロステナント設定変更が可能](https://securityaffairs.com/192473/security/cisco-fixed-maximum-severity-flaw-cve-2026-20223-in-secure-workload.html) — 内部セキュリティテストで発見、公開時点で野放し悪用は未確認。SaaS 版はインフラレベルで修正済み。 *(Security Affairs)*

- **[2026-05-22]** [Ubiquiti UniFi OS に CVSS 10.0 の脆弱性3件 (CVE-2026-34908/34909/34910) が同時パッチ — インターネット公開約 10 万台に影響](https://cybersecuritynews.com/unifi-os-vulnerabilities-privilege-escalation/) — アクセス制御不備・パストラバーサル・コマンドインジェクションの3パターン、いずれも認証不要・低複雑度で悪用可能。 *(CyberSecurityNews)*

- **[2026-05-22]** [JPCERT/CC が Trend Micro エンドポイント製品の複数脆弱性に関する警告を発出 — CVE-2026-34926 を含む Apex One 系製品への即時パッチ対応を要請](https://www.jpcert.or.jp/english/at/) — 国内企業での利用が多い TrendAI 製品を標的とした野放し悪用を CISA が確認済み、国内法人も早急に対応を。 *(JPCERT/CC)*

- **[2026-05-21]** [Langflow CVE-2025-34291 が CISA KEV に追加 — CORS 誤設定起因の RCE、2026 年 1 月から野放し悪用が進行中](https://cybersecuritynews.com/langflow-origin-validation-flaw-exploit/) — AI エージェント・ワークフロープラットフォームとして急速普及中の Langflow (≤ v1.6.9) が標的、ゼロクリックに近い攻撃チェーン。 *(CyberSecurityNews)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-05-21 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2025-34291 | Langflow ≤ 1.6.9 | CWE-942 (CORS 過剰許可) / 9.4 | `allow_origins='*'` + `allow_credentials=True` + `SameSite=None` → 被害者が悪意ページを訪問しただけでクロスオリジンからリフレッシュエンドポイント呼び出し → 有効トークン取得 → 任意コード実行エンドポイントへアクセス | [PR #10696](https://github.com/langflow-ai/langflow/pull/10696) *(commit 不明)* | KEV (2026-05-21追加) / EPSS≥0.5 |
| CVE-2026-34926 | Trend Micro Apex One on-prem (未修正版) | CWE-23 (パストラバーサル) / 6.7 | ローカル管理者が細工パスでサーバーサイドのキー DB テーブルを書き換え → 管理配下の全エンドポイントエージェントへ悪意コードを伝播 → 組織全体 EDR インフラが攻撃踏台化 | [(KA-0023430)](https://success.trendmicro.com/en-US/solution/KA-0023430) *(commit 不明)* | KEV (2026-05-21追加) |
| CVE-2026-20223 | Cisco Secure Workload ≤ 3.10.x / ≤ 4.0.x | CWE-306 (認証機構欠落) / 10.0 | 内部 REST API エンドポイントの認証・検証不足 → 未認証リモート攻撃者が細工 HTTP リクエスト1本で Site Admin 権限取得 → クロステナント機密情報読取・設定変更 | [cisco-sa-csw-pnbsa-g8WEnuy](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-csw-pnbsa-g8WEnuy) *(commit 不明)* | CVSS 10.0 |
| CVE-2026-34908 | Ubiquiti UniFi OS (UCG/UDM/UNVR/UNAS 系) | CWE-284 (アクセス制御不備) / 10.0 | 不適切アクセス制御 → 未認証ネットワーク攻撃者がターゲットシステム設定を直接変更可能 → 完全デバイス乗っ取り (低複雑度) | [(BleepingComputer 記事)](https://www.bleepingcomputer.com/news/security/ubiquiti-patches-three-max-severity-unifi-os-vulnerabilities/) *(commit 不明)* | CVSS 10.0 / 公開端末≈10万台 |
| CVE-2026-34910 | Ubiquiti UniFi OS (UCG/UDM/UNVR/UNAS 系) | CWE-77 (コマンドインジェクション) / 10.0 | 入力検証欠落のエンドポイントから → 未認証リモート攻撃者がネットワーク越しに任意コマンドをインジェクション → RCE (同 CVE-2026-34909 パストラバーサルとチェイン可) | [(BleepingComputer 記事)](https://www.bleepingcomputer.com/news/security/ubiquiti-patches-three-max-severity-unifi-os-vulnerabilities/) *(commit 不明)* | CVSS 10.0 / 公開端末≈10万台 |
| CVE-2026-20239 | Splunk Enterprise ≤ 10.2.1 / Splunk Cloud | CWE-532 (ログ経由情報漏洩) / High | TcpChannel コンポーネントが出力バッファをログ書き込み前に未サニタイズ → `_internal` index 参照可能な低権限認証済みユーザーが生セッションクレデンシャルを抽出 → 権限昇格・横展開 | [(SVD advisory)](https://advisory.splunk.com/advisories) *(commit 不明)* | 横展開・クレデンシャル漏洩リスク高 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-05-22 | JPCERT/CC アラート | TrendAI Apex One を含む国内普及エンドポイント製品に複数脆弱性、野放し悪用を CISA が確認済み | CVE-2026-34926 (CVSSv3: 6.7) | [JPCERT/CC Alerts](https://www.jpcert.or.jp/english/at/) |
| 2026-05-21 | JVNDB-2026-016626 | Android 版「RoboForm Password Manager」に Android Intent 検証不足の脆弱性、不正アプリが任意 Intent 実行の可能性 | CVSSv3: 3.3 (Low) | [JVN iPedia](https://jvndb.jvn.jp/en/contents/2026/JVNDB-2026-016626.html) |
| 2026-05-20 | CVE-2026-44392 / JVNDB-2026-000076 | Six Apart 提供 Movable Type (v2.2 系) に Missing Authorization 脆弱性、低権限ユーザーが不正操作の可能性 | CVSSv3: 4.3 (Medium) | [JVN iPedia](https://jvndb.jvn.jp/en/contents/2026/JVNDB-2026-000076.html) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 22
- 採用件数: AI=8 / Security=8 / CVE=6 / 国内=3
- 除外理由内訳:
  - 古すぎ (公開日 < 2026-05-21 JST): CVE-2026-23918 Apache HTTP/2 (patch 2026-05-04)、Instructure/Canvas 侵害 (Apr-May 11)、Unit 42 IR Report (2026-02-23)、EchoLeak CVE-2025-32711 (patched 2025-05)、Medtronic/ShinyHunters (Apr)、Andrej Karpathy 入社 (2026-05-19)
  - 重複 (既出): Anthropic Managed Agents (05-22 既出)、Anthropic KPMG (05-21 既出)、GitHub breach 3,800 repos (05-22 既出)、Drupal SA-CORE-2026-004 (05-21 既出)、CVE-2026-46333 Linux ptrace (05-22 既出)、CVE-2026-41091/45498 Microsoft Defender KEV (05-22 既出)
  - 日付不明/不確実: Palo Alto Frontier AI Defense Guide (May 2026 月内の具体日付不明のため除外)
  - CVE 範囲外: CVE-2026-32201 SharePoint (April Patch Tuesday、CISA 期限 Apr 28)
- 取得失敗ソース: NVD direct fetch (403)、BleepingComputer direct fetch (403)、JPCERT direct fetch (403)、TheHackerNews direct fetch (403) → 全て WebSearch 経由で代替情報収集

</details>
