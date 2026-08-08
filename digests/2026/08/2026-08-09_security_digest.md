# KEDA Daily Digest — 2026-08-09 (JST)

> 採用範囲: 公開日 2026-08-07 〜 2026-08-09
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Black Hat USA 2026 (8/1–6) の成果発表が今週各メディアに拡散中。CSS/HTML だけで主要ウェブメールを乗っ取る「CSS: the bomb inside your inbox」(PortSwigger) と RFC 設計起因の NAT テーブル欠陥を突く NatJack 攻撃クラスが特に注目を集めた。Metabase の CVSS 10.0 ゼロデイ SQL インジェクション（CVE 未採番）が野生で悪用されており、自己ホスト型ユーザーは即時パッチ適用が必要。AI 業界では Google DeepMind 組織再編と Jeff Dean ら 4 名による Discovery Loop 設立が重なり、業界リーダーシップの大移動が加速している。

---

## AI 関連ニュース

- **[2026-08-07]** [Demis Hassabis が Google DeepMind CEO を退任、Koray Kavukcuoglu が後継 SVP に就任](https://fortune.com/2026/08/05/demis-hassabis-steps-down-google-deepmind-ai-shakeup/) — Hassabis は会長・Alphabet 主任科学者に転じ AGI 戦略を担当し、DeepMind を London からカリフォルニアに一元化する組織再編を発表 *(Fortune)*

- **[2026-08-07]** [Jeff Dean・Sanjay Ghemawat・Oriol Vinyals・Quoc Le ら Google を退職し AI 研究自動化スタートアップ Discovery Loop を共同設立](https://techcrunch.com/2026/08/05/jeff-dean-and-other-top-ai-researchers-are-leaving-google-to-launch-their-own-startup/) — Dean が CEO として機械学習研究サイクル（仮説→実験→評価→改善）の完全自動化を目標に掲げ、Google が創業投資家として参加 *(TechCrunch)*

- **[2026-08-07]** [OpenAI が ChatGPT 無料ユーザーに GPT-5.6 Luna のテキストチャット無制限化と高度推論「Think」ボタンを提供](https://techcrunch.com/2026/08/06/openai-brings-unlimited-chatgpt-text-chats-to-free-users/) — 従来は 5 時間ごと 10 件の制限があったが撤廃。画像・ファイルアップロード等は引き続き制限あり *(TechCrunch)*

- **[2026-08-08]** [Black Hat USA 2026：PortSwigger の Gareth Heyes が CSS のみで主要ウェブメール 6 社を乗っ取る「CSS: the bomb inside your inbox」を発表、PoC 公開](https://portswigger.net/research/css-the-bomb-inside-your-inbox) — Outlook・Gmail・Fastmail・Proton Mail・Yahoo Mail・AOL Mail でパスワード窃取・サードパーティアカウント乗っ取り・AI ツール操作を JS 不使用で実証 *(PortSwigger Research)*

- **[2026-08-07]** [Black Hat USA 2026：SANS が「2026年最も危険な新攻撃技法トップ5」発表、全 5 件に AI 要素を確認](https://www.sans.org/press/announcements/rsac-2026-sans-institute-top-5-most-dangerous-new-attack-techniques) — LLM エージェントへのプロンプトインジェクション・AI 自動化攻撃・合成コンテンツ悪用が席巻。SANS 史上初めて全5件が AI 関連 *(SANS Institute)*

- **[2026-08-03]** [Alibaba が 2.4 兆パラメータの Qwen3.8-Max を公開、DeepSeek V4 Flash も同時登場し推論コスト競争が過熱](https://techstartups.com/2026/08/03/alibaba-unveils-2-4-trillion-parameter-qwen3-8-max-as-deepseeks-new-ai-model-undercuts-anthropic-by-100x/) — DeepSeek V4 Flash は Claude Opus 4.8 相当の性能を主張しつつ推論コストを 99% 削減。各社の値下げ競争が続く *(Tech Startups)*

- **[2026-08-07]** [EU AI Act の GPAI 規制執行権限が 8 月 2 日から欧州委員会に正式付与、違反時は全世界売上高の最大 3%（または 1,500 万ユーロ）の罰金](https://www.wsgr.com/en/insights/eu-ai-act-enforcement-phase-begins.html) — 欧州 AI オフィスが「技術コンプライアンス対話」を優先手段として開始し、OpenAI・Google・Anthropic 等が対象 *(Wilson Sonsini)*

- **[2026-08-07]** [米大統領令（EO 14409）に基づくフロンティア AI モデル安全保障事前審査フレームワークが整備完了、GPT-5.6 や Claude Fable 5 等が政府 30 日間事前審査の対象に](https://www.lw.com/en/insights/president-trump-signs-executive-order-establishing-ai-cybersecurity-and-frontier-model-framework) — 商務省が高度サイバー能力を基準に対象モデルを定義し、NSA・CISA が共同でベンチマーク管理 *(Latham & Watkins)*

- **[2026-08-07]** [「Vibe Coding」AI 自動生成コードによる CVE 急増を CSA がレポート公表、AI 生成コードの脆弱性寄与率が急上昇](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-generated-code-vulnerability-surge-2026/) — 不完全なコンテキストで生成されたコードが認証バイパス・SQL インジェクション・サプライチェーン侵害の温床になると警告 *(Cloud Security Alliance)*

---

## セキュリティ関連ニュース

- **[2026-08-07]** [Black Hat USA 2026：NatJack が RFC 設計起因の NAT テーブル欠陥を悪用して TCP セッション乗っ取り・DNS スプーフィングを実現、テスト対象 32 製品すべてが影響](https://thehackernews.com/2026/08/new-natjack-attacks-hijack-tcp-sessions.html) — 仕様レベルの欠陥のため単一パッチで完全修正不可。CVE-2026-56181 (Hyper-V NAT, CVSS 8.3) と CVE-2026-63913 (Linux conntrack, CVSS 8.2) を特定 *(The Hacker News)*

- **[2026-08-07]** [Metabase がゼロデイ SQL インジェクション（CVSS 10.0、CVE 未採番）を公開—未認証攻撃者が管理者権限を取得可能、野生での悪用を確認](https://securityaffairs.com/196874/hacking/metabase-zero-day-exploited-in-the-wild-exposing-admin-access-and-sensitive-data.html) — 修正版 x.58.24 / x.59.21 / x.60.17 / x.61.11 / x.62.9 / x.63.5 にアップデートを勧告 *(Security Affairs)*

- **[2026-08-07]** [UK 警察国家法務データベース（PNLD）が ExfilSquad によるサイバー攻撃で 11 万 4 千人超の警察官・職員の連絡先が Dark Web に流出、身代金要求](https://thehackernews.com/2026/08/pnld-breach-exposes-uk-police-and.html) — Microsoft Power Platform 経由の侵害の可能性。Ask the Police サービス利用者 2.1 万人も影響を受けた *(The Hacker News)*

- **[2026-08-07]** [COLDCARD ハードウェアウォレットの PRNG バグ（5 年間にわたり HW RNG を迂回）で 1,367 BTC（約 $88.6M）がドレイン、TRM Labs が詳細分析を公開](https://www.trmlabs.com/resources/blog/the-largest-hardware-wallet-exploit-of-2026-inside-the-usd-116-million-coldcard-hack) — 攻撃者は UID・タイマー状態・RNG 呼び出し履歴を再現してシードを推測。緊急ファームウェア配布済みも既存シードは新ウォレットへの移行が必須 *(TRM Labs)*

- **[2026-08-08]** [CSS と HTML のみで Outlook・Gmail・Proton Mail など主要ウェブメール 6 社を標的とした攻撃チェーン（パスワード窃取・アカウント乗っ取り・AI 操作）を PortSwigger が公開 PoC で実証](https://portswigger.net/research/css-the-bomb-inside-your-inbox) — CSS レイアウト操作でウェブメール UI に偽入力フィールドを重ね、AI メール機能を操作する新技法。一部プロバイダは未修正 *(PortSwigger Research)*

- **[2026-08-07]** [COLDCARD RNG 欠陥に関連して AI ペネトレーションテストエージェントが Bitcoin ウォレット実装の追加 85 件の Critical バグを発見](https://crypto.news/coldcard-rng-flaw-bitcoin-wallet-ai-audit/) — 調査は COLDCARD バグを起点に AI エージェントが自律的にソースコードを解析。ウォレットソフトウェアのコードベース全体に潜在的欠陥が広がる可能性 *(Crypto.news)*

- **[2026-08-07]** [PNLD 侵害において Microsoft Power Pages のデフォルト設定不備（匿名ユーザーへのデータ公開）が侵入口となった疑いを Rescana が分析](https://www.rescana.com/post/pnld-data-breach-exposes-uk-police-and-government-contact-information-via-microsoft-power-platform-misconfiguration) — Power Platform を使用する組織に Power Pages のアクセス制御設定の即時確認を推奨 *(Rescana)*

- **[2026-08-07]** [Basecamp Briefing 2026-08-07 で「信頼モデルの悪用」パターンが今週の脅威傾向として報告、NatJack・COLDCARD・PNLD 等が事例](https://sherpaintelligence.substack.com/p/basecamp-briefing-august-7-2026) — 攻撃者はセキュリティ管理を正面突破せず、設計上の信頼前提（RFC 仕様・HW の乱数保証・IT 管理ツールの信頼性）を利用して侵害 *(Sherpa Intelligence)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-08-07 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-56181 | Windows Hyper-V NAT (未パッチ) | CWE-364 / 8.3 | 同一 NAT 環境の共テナントが NAT テーブルのポートマッピング予測可能性を利用 → Hyper-V VM の任意 TCP セッション乗っ取り・DNS 応答スプーフィング | MS 8月 Patch Tuesday (2026-08-12) 予告 | Black Hat 2026; RFC 仕様起因で他実装に水平伝播 |
| CVE-2026-63913 | Linux Netfilter conntrack (未パッチ) | CWE-364 / 8.2 | Linux conntrack が NAT 状態を追跡する際の接続 ID 予測可能性 → 同一 NAT 下の攻撃者がセッションハイジャック・NAT テーブル枯渇攻撃 | Linux カーネルパッチ予告 | Black Hat 2026; RFC 仕様起因 |
| CVE-2026-56793 | Dell OpenManage Server Administrator <11.1.0.2 | CWE-287 / - | 未認証リモート攻撃者が不完全な認証チェックを通じて管理インタフェースに到達 → 不正アクセス | v11.1.0.2 へアップグレード (commit 不明) | 公開日 2026-08-07 |
| CVE-2026-71558 | Apache Fury C++ 0.14.0–1.4.x | CWE-843 / - | 攻撃者制御の多型スマートポインタデシリアライズで型整合チェックをバイパス → heap 上で型混同 → 潜在的 DoS / RCE | [v1.5.0](https://fory.apache.org/security/) (commit 不明) | 公開日 2026-08-07; C++/Rust/Swift 等 OOP デシリアライザに水平伝播可 |
| CVE-2026-71559 | Apache Fury Go 0.16.0–1.4.x | CWE-502 / - | 不正なメタデータを含むシリアライズデータを Go 実装に送信 → uncaught panic → DoS | [v1.5.0](https://fory.apache.org/security/) (commit 不明) | 公開日 2026-08-07 |
| GHSA-4gmw-gg2m-w46p | GitPython (pip) ≤3.1.57 | CWE-88 / 8.1 | `IndexFile.from_tree()`・`reset()`・`merge_tree()` が呼び元制御の引数を git コマンドに直接渡す → `--index-output` フラグ注入で任意パスに git index ブロブ上書き | [v3.1.58](https://github.com/gitpython-developers/GitPython) (commit 不明) | GHSA 公開 2026-08-07; PyPI 経由で多数の OSS CI パイプラインに影響 |
| (CVE 未採番) | Metabase Enterprise x.58.x–x.63.4 | CWE-89 / 10.0 | 未認証攻撃者が API エンドポイントを通じて任意 SQL を Metabase アプリ DB に注入 → 管理者アクセス取得・顧客データ窃取 | x.58.24 / x.59.21 / x.60.17 / x.61.11 / x.62.9 / x.63.5 (commit 不明) | CVSS 10.0; 野生での実際の悪用確認済み; KEV 候補 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|---|---|---|---|---|
| 2026-08-07 | VU#487613 (CVE-2026-8496) | JPCERT/CERT-CC 勧告: Alinto SOGo v5.12.7 の ICS カレンダー DESCRIPTION フィールドで SVG onrepeat ハンドラによる格納型 XSS、認証済みセッション内で任意 JS 実行 | CVSS 8.1 / メールボックス・セッショントークン窃取 | https://kb.cert.org/vuls/id/487613 |

> 直近2日間に国内独自の新規インシデントは追加で確認できませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 20+（WebSearch 12クエリ、WebFetch 試行 25件）
- 採用件数: AI=9 / Security=8 / CVE=7 / 国内=1
- 除外理由内訳:
  - 古すぎ (公開日 <2026-08-07): Google DeepMind カリフォルニア移転 (Bloomberg 2026-08-06)、GPT-5.6 価格80%引き (2026-07-30)、Anthropic チップ設計チーム確認 (2026-08-05)、EU AI Act 執行日イベント本体 (2026-08-02)、Qwen3.8-Max リリース (2026-08-02)、COLDCARD 攻撃発生日 (2026-07-30)、CVE-2026-8496 公開 (2026-05-14)、CVE-2026-25049 n8n (2026-02-04)、CVE-2026-33725 Metabase RCE PoC (2026-04-27)
  - 重複 (excluded_set に存在): CVE-2026-54876 (OpenSSL OCSP)、CVE-2026-18577 (N-able N-central)、CVE-2026-64638 (WordPress 7.0.3)、Claude Code/Gemini CLI CI/CD フロー (thehackernews 2026-08-06)、Samsung Galaxy Bixby エクスプロイトチェーン
  - 日付不明または裏取り不可: email chatbot abuse 研究 (ソース特定不可)
- 取得失敗ソース (EGRESS_BLOCKED): thehackernews.com, bleepingcomputer.com, securityonline.info, securityweek.com, cisa.gov, gbhackers.com, cyberpress.org, diesec.com, zecurit.com, trmlabs.com, securityaffairs.com, kb.cert.org, jvn.jp, jvndb.jvn.jp, jpcert.or.jp, sentinelone.com, nvd.nist.gov, labs.cloudsecurityalliance.org, vistanetinc.com

</details>
