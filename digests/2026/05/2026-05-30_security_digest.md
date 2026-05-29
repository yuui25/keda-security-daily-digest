# KEDA Daily Digest — 2026-05-30 (JST)

> 採用範囲: 公開日 2026-05-28 〜 2026-05-30
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Anthropic が $65B 調達で時価評価 $965B に達し OpenAI を超えると同日、OpenAI も Frontier Governance Framework を公開するなど AI ガバナンス競争が加速した。セキュリティ面では ShinyHunters が Charter Communications (Spectrum) の 1300 万件超・Carnival Corporation の 600 万人分データを相次いで公開し消費者サービスへの侵害が顕在化。Gogs の未修正ゼロデイ RCE (CVSSv4 9.4) を CISA がパッチ不在のまま KEV 追加するという異例の措置も取られ、自己ホスト型 Git インフラへの即応が求められる。

---

## AI 関連ニュース

- **[2026-05-28]** [Anthropic が Series H $65B 調達で時価評価 $965B に到達、OpenAI を超えて未上場 AI 企業最高額を更新](https://techcrunch.com/2026/05/28/anthropic-raises-65-billion-nears-1t-valuation-ahead-of-ipo/) — Altimeter/Sequoia/Dragoneer 主導、Samsung・SK Hynix・Micron も参加；ランレート収益 $47B・IPO は秋 2026 予定。$15B は Amazon など既存ハイパースケーラーからの充当で、安全性研究・Claude コンピュート拡充・顧客向けスケールアップに充当 *(TechCrunch / Bloomberg)*

- **[2026-05-29]** [OpenAI が Frontier Governance Framework を公開 — サイバーオフェンス・CBRN・有害操作・制御喪失の 4 リスクカテゴリを正式化](https://openai.com/index/openai-frontier-governance-framework/) — カリフォルニア州 Transparency in Frontier AI Act と EU AI Act Code of Practice への適合を明示；Preparedness Framework を基盤にモデルレポーティング・セキュリティリスク管理・インシデント対応・外部専門家入力の体制を法的要件以上に整備 *(OpenAI)*

- **[2026-05-28]** [OpenAI が Thrive と協力し Codex ベースの自己改善型税務 AI エージェントを公開 — 正確率 97%、評価フィードバックで反復改善](https://openai.com/index/building-self-improving-tax-agents-with-codex/) — 実行結果をスコアリングして次プロンプトへ反映する自己改善ループを確立；金融・法務 AI エージェントの信頼性向上の先行実装例として注目 *(OpenAI)*

- **[2026-05-29]** [ASAPP が AI システム向け Continuous Red Teaming を発表 — Promptfoo ベースで開発段階の AI アプリを常時テスト](https://www.helpnetsecurity.com/2026/05/29/new-infosec-products-of-the-month-may-2026/) — エンタープライズが開発中の AI アプリ (プロンプトインジェクション・越権応答・PII 漏洩) を自動継続的に検出；AI セキュリティのシフトレフトを推進する商用サービスとして提供開始 *(Help Net Security)*

---

## セキュリティ関連ニュース

- **[2026-05-29]** [Charter Communications (Spectrum) がデータ侵害を確認 — ShinyHunters が身代金期限後に 1300 万件超の顧客データを公開](https://www.bleepingcomputer.com/news/security/charter-confirms-data-breach-after-shinyhunters-extortion-threat/) — 4/1 に vishing で Microsoft Entra 認証情報を奪取 → Salesforce CRM へ横移動し顧客・従業員レコードを窃取；42M 件主張に対し独立検証で 1300 万件超（従業員 2.7 万件含む）を確認。氏名・メール・住所・サポートチケット詳細が含まれる。Charter は CPNI 漏洩を否定 *(BleepingComputer / SC Media)*

- **[2026-05-28]** [Carnival Corporation が 600 万人分データ侵害を確認 — ShinyHunters が 4/14 ソーシャルエンジニアリングで侵入し氏名・住所・パスポート番号等を窃取](https://www.helpnetsecurity.com/2026/05/28/carnival-corporation-data-breach/) — 4/18 ShinyHunters の「pay or leak」ポータルへ掲載後、Carnival が 5/27 付被害者通知書を発送開始（Maine AG 届出：5,995,277 名）；パスポート番号・運転免許証番号・生年月日が含まれ信用監視が必要 *(Help Net Security / BleepingComputer)*

- **[2026-05-28]** [Gogs 自己ホスト型 Git で未修正ゼロデイ RCE — Rapid7 が 90 日超の無応答後に CVSSv4 9.4 で強制開示、Metasploit モジュール公開](https://www.bleepingcomputer.com/news/security/new-gogs-zero-day-flaw-lets-hackers-get-remote-code-execution/) — 認証済みユーザーが PR のブランチ名に `--exec <cmd>` を埋め込み → マージ時に `git rebase --exec` として任意 OS コマンド実行 RCE；デフォルトのオープン登録設定で実質ゼロ権限アカウントから即悪用可能。2,400+ 露出サーバー中 94% がアジア・欧州所在。回避策: 「マージ前リベース」機能無効化 *(Rapid7 / BleepingComputer)*

- **[2026-05-29]** [CISA が未パッチの Gogs RCE を KEV 追加 — パッチ不在での KEV 追加という異例措置、連邦機関に代替緩和を義務化](https://www.infosecurity-magazine.com/news/cisa-flags-exploited-gogs-flaw-no/) — 野外での実際の悪用が確認されたとして追加；暫定緩和策としてオープン登録の無効化と VPN/IP 許可リストによるアクセス制限を勧告。通常は「修正済み製品のみ」KEV 掲載だがアクティブ悪用を優先 *(Infosecurity Magazine / CISA)*

- **[2026-05-29]** [Google Chrome 148 最新更新版 (148.0.7778.217) が 151 件を修正、22 件が Critical — CVE-2026-9872/9873 が最高 $43K バウンティ](https://www.securityweek.com/chrome-148-update-patches-151-vulnerabilities/) — UAF が 66 件と過半を占める大規模パッチ；レンダラー侵害後のサンドボックス脱出チェーンが大半。現時点で野外悪用は未確認だが段階的展開中のため速やかな更新が推奨 *(SecurityWeek)*

- **[2026-05-27/28]** [FBI が FIFA ワールドカップ 2026 を悪用するタイポスクワッティング詐欺について PSA (I-052726-PSA) を発行 — 4,300+ 不正ドメインを確認](https://www.bleepingcomputer.com/news/security/fbi-warns-of-fake-fifa-websites-running-world-cup-fraud-schemes/) — 個人・金融情報詐取・偽チケット販売・ホスピタリティ詐欺が横行；Group-IB が 4,300+ ドメインを特定。連邦機関は 36 ドメインをブロックリスト化。対策: URL は手入力で「fifa.com」を確認、スポンサー広告リンクを踏まない *(FBI IC3 / BleepingComputer)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-05-28 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-9872 | Google Chrome < 148.0.7778.217 | CWE-787 / **CRITICAL** | 侵害済みレンダラープロセスが GPU コンポーネント内 OOB 書き込みを誘発 → レンダラーサンドボックス外で任意コード実行 | [Chrome リリースノート](https://chromereleases.googleblog.com/2026/05/) | CRITICAL / $43K バウンティ / Chromium ベース全ブラウザ (Edge・Brave・Opera・Vivaldi) に共通影響 |
| CVE-2026-9873 | Google Chrome < 148.0.7778.217 (Windows) | CWE-416 / **CRITICAL** | 侵害済みレンダラーが Network コンポーネントの UAF を発生させ → Windows 上でサンドボックス脱出 + 特権昇格 | [Chrome リリースノート](https://chromereleases.googleblog.com/2026/05/) | CRITICAL / Windows 限定 / CVE-2026-9872 と同一 PR で修正 / 2 CVE チェーンでサンドボックス完全突破 |
| CVE-2026-42250 | bzip2 < 1.0.9 (bzip2recover) | CWE-787 / 未採番 | 細工した .bz2 ファイルを bzip2recover に渡すとオフバイワン型グローバルバッファ OOB 書き込みが発生 → メモリ破壊 / クラッシュ (DoS) | [commit 35d122a3](https://sourceware.org/git/?p=bzip2.git;a=commit;h=35d122a3df8b0cc4082a4d89fdc6ee99f375fe67) | 汎用圧縮ライブラリとして OS パッケージ・言語ランタイム多数に同梱 / バックポート漏れに注意 |
| Gogs argument injection 0-day ([Rapid7 advisory](https://www.rapid7.com/blog/post/ve-authenticated-rce-via-argument-argument-injection-gogs-unfixed/)) | Gogs ≤ 0.15.0+dev (全バージョン・**パッチなし**) | CWE-88 / CVSSv4 **9.4** | 認証済みユーザーが PR ブランチ名に `--exec <shell_cmd>` を埋め込み → `git rebase --exec` が sh -c で任意 OS コマンドを実行 → サーバー全権限 RCE | **未修正** (回避: マージ前リベース機能を無効化、open registration を無効化) | **KEV ✓** (2026-05-29 追加) / CVSSv4 9.4 / デフォルト設定で実質ゼロ権限アカウントから即悪用可 / Metasploit 対応済み / Forgejo (同仕様フォーク) にも同一バグ存在の可能性 |

---

## 国内脆弱性・インシデント情報

> 直近2日間に該当する新規国内脆弱性・インシデント情報は確認できませんでした。

*備考: JPCERT/CC・JVN への直接アクセスが HTTP 403 により不可。上記 Chrome CVE・bzip2 CVE・Gogs ゼロデイは国内自己ホスト Git・Linux 環境・Chromium ベースブラウザ全般に影響する。*

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 30+ (WebSearch 17 クエリ, WebFetch 18 試行)
- 採用件数: AI=4 / Security=6 / CVE=4 / 国内=0
- 除外理由内訳:
  - 古すぎ (< 2026-05-28): GPT-5.5 リリース (4/23), ChatGPT 個人金融機能 (5/15), Google AI 生成ゼロデイ検出 (5/11), GitHub データ侵害 (5/20), bzip2 以外の Patch Tuesday CVEs (5/13), Cisco SD-WAN CVE-2026-20182 (5/15), Microsoft Exchange CVE-2026-42897 (5/14), Adversa AI IICL bypass (4/26), n8n CVE-2026-21858/21877 (1/26), TP-Link VIGI CVE-2026-0629 (1/26), GPUマイニング via AI chatbot (5/26-27), OnlyFans 340M (5/25初報), GitHub GHES CVE-2026-3854 (4/28)
  - 重複 (excluded_set 直近7日): Claude Opus 4.8 (05-29) / Google AI Threat Defense (05-29) / Oracle CSPU (05-29) / FortiClient EMS CVE-2026-35616 (05-29) / Yamcs CVEs (05-29) / DAEMON Tools CVE-2026-8398 (05-29) / Jupyter Server JVN (05-29) / Glassworm takedown (05-28) / SymJack (05-28) / 7-Eleven breach (05-28) / Gitea CVE-2026-27771 (05-28) / Malware-Slop npm (05-28)
  - 日付不明/確認不可: ASAPP Continuous Red Teaming 詳細ページ (403)
- 取得失敗ソース: CISA advisories (403), NVD (403), BleepingComputer top-level (403), The Hacker News top-level (403), SecurityWeek top-level (403), Anthropic News top-level (403), JPCERT alerts (403), Rapid7 blog (403), Infosecurity Magazine (403), chromereleases.googleblog.com (403)

</details>
