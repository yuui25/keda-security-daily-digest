# KEDA Daily Digest — 2026-07-25 (JST)

> 採用範囲: 公開日 2026-07-23 〜 2026-07-25 (JST)
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

AI セキュリティ面では 7/23 に「FakeAgent (Claude.ai Artifact 悪用)」「AgentForger (ChatGPT エージェント偽造)」「SharedRoot (Claude Cowork サンドボックス脱出)」の 3 本が同時開示され、AI プラットフォーム自体が攻撃ベクターとなるトレンドが一段と鮮明化した。7/24 には Hermes AI エージェントによるタイ財務省への完全自律的ポスト侵害が報告され、AI ツールが実際の政府機関侵害に使われた事例として注目を集めている。CVE 面では Certighost (CVE-2026-54121) の完全 PoC が 7/24 に公開され AD CS 経由のドメインコントローラーなりすましが現実的脅威となった他、Clop ランサムウェアが PTC Windchill/FlexPLM (CVE-2026-12569) への extortion campaign を本格化させており製造業サプライチェーンへの影響が懸念される。

---

## AI 関連ニュース

- **[2026-07-23]** [FakeAgent: 攻撃者が Claude.ai Artifact に偽 Claude Desktop を構築し Bing 広告経由で SectopRAT を 29 組織・7,100 DL に配布](https://www.huntress.com/blog/fakeagent-claude-desktop-malvertising-ends-in-dotnet-rat) — Huntress が「FakeAgent」キャンペーンを開示: 攻撃者が Claude.ai の公開 Artifact ホスティング機能を悪用して claude.ai ドメイン上に偽インストーラーページを構築、Bing スポンサード広告に掲載、「Claude Desktop」を検索したユーザーを誘導し SectopRAT (クレカ・パスワード・ブラウザデータ窃取型 RAT) を配布、少なくとも 29 組織・7,100 DL が確認される前に Anthropic が削除 *(Huntress / Help Net Security / CybersecurityNews)*

- **[2026-07-23]** [AgentForger: ChatGPT Workspace Agents にフィッシングリンク 1 件で攻撃者制御エージェントを企業内展開 — OpenAI が 6/8 に修正済み](https://labs.zenity.io/p/agentforger-part-1-chatgpt-cross-site-agent-forgery) — Zenity Labs が「AgentForger」を開示: Agent Builder の URL パラメータ (template selector + initial prompt フィールド) を操作することで承認フローを完全バイパスし、被害者組織内に攻撃者制御の自律エージェントを展開、5 分ごとに攻撃者メール受信箱をポーリングして組織内横移動・文書窃取・被害者なりすましを実行 *(Zenity Labs / BusinessWire / THN / SecurityWeek)*

- **[2026-07-23]** [Claude Cowork 「SharedRoot」: macOS の VirtioFS 設計でホスト全 FS へ書込み可能アクセス、CVE-2026-46331 と組合せて SSH 鍵・クラウドクレデンシャルを取得](https://thehackernews.com/2026/07/claude-cowork-flaw-could-let-ai-agent.html) — Accomplish Security がサンドボックス脱出「SharedRoot」を開示: Claude Cowork の macOS 版が Linux VM の VirtioFS で /mnt/.virtiofs-root にホスト全 FS を書込み可能マウント、CVE-2026-46331 (Ubuntu kernel 「pedit COW」) でゲスト root 昇格後にホストの SSH 秘密鍵・AWS/GCP クレデンシャルを取得可能、約 50 万 macOS ユーザーが影響、Anthropic はデフォルト実行をクラウドへ移行することで対応 *(Accomplish / THN / GBHackers / CybersecurityNews)*

- **[2026-07-23]** [Black Forest Labs、FLUX 3 を発表: 画像・動画・音声・ロボット制御アクションを単一重みで生成するマルチモーダル基盤モデル](https://www.globenewswire.com/news-release/2026/07/23/3332364/0/en/black-forest-labs-unveils-flux-3-a-new-multimodal-frontier-model-for-visual-intelligence.html) — 画像・動画 (20 秒 + ネイティブ音声)・ロボット制御アクション予測を単一モデルで同時学習・生成する FLUX 3 を発表、Video が early access 開始。Runway Gen-4.5 比 77%、Luma Ray 3.2 比 93% の評価で優位、Image・Action は数週間以内に順次提供予定 *(GlobeNewswire / Manila Times / ExplainX)*

- **[2026-07-23]** [OpenAI が GPT-Live を ChatGPT デスクトップアプリ (macOS/Windows) に統合: 前面ウィンドウ参照 + リアルタイム音声で Codex/Work エージェントを操作](https://openai.com/news/company-announcements/) — ChatGPT デスクトップアプリで GPT-Live による音声対話が可能となり、Mac の前面ウィンドウコンテキストを参照しながら Codex や ChatGPT Work エージェントをリアルタイムで音声指示・操作できる新機能を展開 *(OpenAI)*

- **[2026-07-24]** [Anthropic が Claude Opus 5 を発表: Fable 5 に肩を並べる能力を半額で提供する職場向けモデル](https://www.bloomberg.com/news/articles/2026-07-24/anthropic-unveils-more-cost-efficient-model-for-everyday-tasks) — Anthropic が Claude Opus 5 を発表。多くのカテゴリで旗艦モデル Fable 5 に匹敵する能力を半額で提供し、コスト意識の高い企業顧客を主要ターゲットとしてポジショニング *(Bloomberg / Anthropic)*

- **[2026-07-24]** [Hermes AI エージェントがタイ財務省に対して完全自律的ポスト侵害を実行 — 中国語話者系脅威アクターが Autopilot モードで 2012 年来の職員個人情報フォルダーを走査](https://thehackernews.com/2026/07/hacker-runs-hermes-ai-agent-unattended.html) — Hunt.io が開示: 中国語話者と低〜中程度の確信で評定される脅威アクターが Hermes AI エージェントをレンタルサーバーで Autopilot (許可プロンプト無効) 起動 → タイ財務省ネットワークを自律的にポスト侵害・root 権限取得・2012 年来の職員 PII フォルダーを走査、同一サーバーで ShadowPad C2・VShell C2 も稼働、5,900 件超のスキャンイベントが 1 ヵ月に観測される *(Hunt.io / THN / GuardianMSSP)*

---

## セキュリティ関連ニュース

- **[2026-07-24]** [Certighost (CVE-2026-54121) 完全 PoC が公開: 低権限 AD ユーザーがドメインコントローラーを偽装し DCSync が可能](https://thehackernews.com/2026/07/certighost-exploit-lets-low-privileged.html) — 研究者 H0j3n と aniqfakhrul が 7/24 に完全 PoC を GitHub 公開。AD CS の enrollment 「chase」フェーズで cdc パラメータに攻撃者制御ホスト名を挿入 → CA が DC の ID データを攻撃者サーバーに問い合わせ → 正規 DC 証明書を CA が発行 → Pass-the-Certificate で DA 権限昇格・DCSync 実行が可能。Microsoft が 7/15 Patch Tuesday で修正 (CVSS 8.8 / CWE-285) *(THN / GitHub:aniqfakhrul / SEPE)*

- **[2026-07-24]** [Clop ランサムウェアが PTC Windchill/FlexPLM (CVE-2026-12569) への extortion campaign を開始: 製造業・PLM プラットフォームから機密設計データを窃取](https://www.bleepingcomputer.com/news/security/clop-ransomware-targets-windchill-flexplm-in-data-theft-attacks/) — Clop が 7/20 ごろから「Windchill PDMLink module serious data leak」と件名を付けたメールを被害組織の内部配布リストに直接送付して恐喝開始。FlexPLM WSDL エンドポイントの pre-auth 情報漏洩 + Windchill ログインサーブレット欠陥をチェーンして未認証 RCE → JSP webshell 設置・機密設計データ窃取 *(BleepingComputer / Ransom-ISAC / SecurityWeek)*

- **[2026-07-24]** [Golden Chickens (TAG-195/Venom Spider) が TinyEgg・ChonkyChicken 等 4 つの新マルウェアファミリーを投入 — ClickFix ルアーで初期侵入](https://thehackernews.com/2026/07/golden-chickens-resurfaces-with-four.html) — TAG-195 が TinyEgg (軽量初期アクセス backdoor)・ChonkyChicken (RAT / 認証情報窃取・横移動・監視)・モジュール型 ChonkyChicken・ChromEggscalator (Chrome クレデンシャル窃取) の 4 ファミリーを投入。ClickFix ルアー (偽認証ページ → Windows Run ダイアログに OCX ペイロードをペースト → regsvr32.exe 経由起動) が初期侵入ベクター *(THN / CyberPress / Cryptika)*

- **[2026-07-24]** [Chick-fil-A がクレデンシャルスタッフィング攻撃による 13,000 件超の顧客データ流出を確認](https://www.bleepingcomputer.com/news/security/chick-fil-a-data-breach-affects-more-than-13-000-customers/) — 米大手ファストフードチェーン Chick-fil-A がクレデンシャルスタッフィング攻撃による顧客アカウント侵害を確認、13,000 件超のメールアドレス・部分カード情報・報酬ポイントが流出、全影響ユーザーに通知とパスワードリセットを実施 *(BleepingComputer)*

- **[2026-07-24]** [Microsoft 365 / Azure で大規模障害: 自動ネットワーク保守スクリプトのバグが意図した台数以上のデバイスから IP ルートを削除](https://www.bleepingcomputer.com/news/microsoft/microsoft-blames-massive-microsoft-365-outage-on-maintenance-bug/) — Microsoft が 7/24 の Microsoft 365・Azure 大規模障害の原因を公表: 自動ネットワーク保守リクエストシステムのバグにより、意図した台数を大幅に超えるデバイスから IP ルートが削除され、Teams・Exchange Online・Outlook・Azure ポータルに広範な障害が発生 *(BleepingComputer / Microsoft)*

- **[2026-07-24]** [Black Kite 「2026 Ransomware Report」: 12 ヵ月で 61 新グループ・146 アクティブグループ・AI 駆動化により偵察〜恐喝が急加速](https://www.helpnetsecurity.com/2026/07/24/ransomware-attack-trends-2026-report/) — Black Kite 年次レポート (Help Net Security 7/24 掲載): 2025/4〜2026/3 に 61 の新グループが参入 (週 1 超)、2026/6 時点でアクティブグループ 146 (過去最多)、30 秒以内に侵入から横移動を開始する事例も報告、AI によるフィッシング・ソーシャルエンジニアリング・恐喝メッセージ生成の自動化が急速に進行 *(Help Net Security / Black Kite)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-07-23 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-54121 (Certighost) | Microsoft AD CS (July 2026 Patch Tuesday 未適用の全バージョン) | CWE-285 / **8.8** | ドメインアカウントを持つ低権限ユーザーが enrollment 要求の cdc パラメータに攻撃者制御ホスト名を挿入 → CA が enrollment chase フェーズで DC の ID データをそのホストに問い合わせ → 正規 DC 証明書を発行 → Pass-the-Certificate + DCSync でドメイン管理者権限取得 | Microsoft July 2026 CPU (2026-07-15) / PoC: [github.com/aniqfakhrul/CVE-2026-54121](https://github.com/aniqfakhrul/CVE-2026-54121) (2026-07-24) | **2026-07-24 完全 PoC 公開** / AD CS 広範利用 / ドメインアカウントのみ必要 (管理者不要) / Active Directory 環境で水平伝播 |
| CVE-2026-12569 | PTC Windchill PDMLink / FlexPLM (2026-06-17 パッチ未適用) | CWE-502 / **9.8** | 未認証攻撃者が FlexPLM WSDL エンドポイントの pre-auth 情報漏洩で内部クラス名を取得 → Windchill ログインサーブレットに細工 POST で信頼デシリアライズ → RCE → JSP webshell 設置・機密設計データ・製造プロセス情報を窃取 | PTC advisory [(ptc.com/…/windchill-flexplm-rce-vulnerability)](https://www.ptc.com/en/about/trust-center/advisory-center/active-advisories/windchill-flexplm-rce-vulnerability) (2026-06-17) (commit 不明) | **Clop extortion campaign 2026-07-20〜 確認** / CISA KEV 追加済み (June 2026) / 製造業 PLM 広範利用・日本製造業も要注意 / 二段チェーン (WSDL + ログインサーブレット) がバリアント候補 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-07-23 | JVNDB-2026-000085 | Ricoh 製 MFP・プリンター複数モデルの SSH 機能にポートフォワーディング制限欠如: 攻撃者がデバイスをリレー踏み台として悪用し内部ネットワークへの横移動が可能、Ricoh がファームウェアアップデートを提供 (Pathfynder.io の Brandon Roach・Bryan Clements が報告)。 | 影響中〜大 / オフィス MFP・プリンター環境 | [JVNDB-2026-000085](https://jvndb.jvn.jp/en/contents/2026/JVNDB-2026-000085.html) / [Ricoh Europe Advisory](https://www.ricoh-europe.com/news-events/news/specific-ricoh-mfp-and-printer-products-vulnerability-in-ssh-function/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| Huntress / Help Net Security / CybersecurityNews / IT Security Guru (FakeAgent SectopRAT Claude.ai Artifact) | Help Net Security URL "/2026/07/23/" 確認 ✓ / IT Security Guru "/2026/07/23/" 確認 ✓ / Huntress ブログ確認 ✓ |
| Zenity Labs / BusinessWire / THN / SecurityWeek (AgentForger) | BusinessWire "20260723680415" (2026-07-23) 確認 ✓ / THN 記事確認 ✓ |
| Accomplish / THN / GBHackers / CybersecurityNews (Claude Cowork SharedRoot) | CyberTechWorld "/2026/07/23/" 確認 ✓ / THN 記事確認 ✓ / Accomplish blog 確認 ✓ |
| GlobeNewswire / Manila Times (Black Forest Labs FLUX 3) | GlobeNewswire "news-release/2026/07/23/" 確認 ✓ / Manila Times "/2026/07/23/" 確認 ✓ |
| OpenAI (GPT-Live デスクトップ統合) | 複数ソースで "July 23, 2026" 確認 ✓ |
| Bloomberg / Anthropic (Claude Opus 5) | Bloomberg URL "2026-07-24" 確認 ✓ |
| Hunt.io / THN / GuardianMSSP (Hermes AI agent Thailand) | GuardianMSSP "/2026/07/24/" 確認 ✓ / THN 記事確認 ✓ |
| THN / GitHub:aniqfakhrul / SEPE (Certighost CVE-2026-54121 PoC) | 複数ソースで "published a working exploit on July 24" 確認 ✓ / GitHub repo 確認 ✓ |
| BleepingComputer / Ransom-ISAC / SecurityWeek (Clop Windchill/FlexPLM) | BleepingComputer "approximately 8 hours ago" → July 24 確認 ✓ / Ransom-ISAC "Since July 20" 確認 ✓ |
| THN / CyberPress / Cryptika (Golden Chickens TAG-195) | GuardianMSSP "/2026/07/24/" 確認 ✓ / THN 記事確認 ✓ |
| BleepingComputer (Chick-fil-A breach) | BleepingComputer July 24 記事リスト確認 ✓ |
| BleepingComputer / Microsoft (Microsoft 365 outage) | BleepingComputer July 24 記事リスト確認 ✓ |
| Help Net Security / Black Kite (Ransomware 2026 Report) | Help Net Security URL "/2026/07/24/ransomware-attack-trends-2026-report/" 確認 ✓ |
| Ricoh Europe / JVNDB-2026-000085 (Ricoh SSH ポートフォワーディング) | JVNDB-2026-000085 "2026-07-23 公開" 確認 ✓ / Ricoh Europe advisory 確認 ✓ |

### 集計サマリ

- **巡回ソース数**: 約 30
- **採用件数**: AI=7 / Security=6 / CVE=2 / 国内=1
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-07-23 より前): AMD + Anthropic $5B 投資 (Bloomberg "/2026-07-22/") / Moonshot AI IPO $50B (Bloomberg "2026-07-21" / TechNode "/2026/07/22/") / AWS Kiro CVE-2026-10591 (GuardianMSSP "/2026/07/21/") / NSA/FBI ロシア FSB ルーター共同勧告 (2026-07-09〜13) / Ghostcommit PNG プロンプトインジェクション (hazetec.com "20260711") / Meta Muse Spark 1.1 (Bloomberg "2026-07-09") / BridgePay ランサムウェア (2026-02-06) / PromptSpy Android (THN "/2026/02/")
  - 重複 (excluded_set 参照): DeepSeek V4 GA (07-24 掲載済) / Kimi K3 White House 告発 (07-24 掲載済) / OpenAI Presence (07-24 掲載済) / JadeProx TriBack (07-24 掲載済) / CVE-2026-16232 Check Point (07-24 掲載済) / CVE-2026-64600 RefluXFS (07-24 掲載済) / Oracle July CPU / Gemini 3.6 Flash / UK AISI / OpenAI Hugging Face 侵害 (07-23/24 掲載済)
  - 日付不明・未確認: Dolphin X RAT (The Register "/2026/07/22/" 確認により採用窓外と判断)
  - CVE 採用窓外: CVE-2026-46331 (pedit COW、June 2026 公開) - SharedRoot の記述中に言及のみ / CVE-2026-50656 (RoguePlanet) - July 15 Patch Tuesday で既修正、当期内の特記事象なし

### 主要採用補足

- **FakeAgent**: Claude.ai Artifact ホスティング機能が攻撃インフラとして初めて大規模悪用された事例。7/23 Huntress ブログおよび Help Net Security の URL "/2026/07/23/" で日付確認。
- **AgentForger**: 修正は 6/8 だが Zenity Labs の公開開示は BusinessWire "20260723680415" (7/23) で確認。
- **SharedRoot**: CyberTechWorld の THN 転載 URL "/2026/07/23/" で日付確認。PoC による実証は Accomplish の accomplish.ai ブログ。
- **FLUX 3**: GlobeNewswire press release "news-release/2026/07/23/" で日付確認。
- **Claude Opus 5**: Bloomberg URL "2026-07-24" で日付確認。
- **Hermes AI agent**: GuardianMSSP "/2026/07/24/" で日付確認。Hunt.io の初報 July 23 → THN 転載 July 24。
- **Certighost PoC**: 複数ソースが "published a working exploit on July 24" と一致して記述。GitHub リポジトリ aniqfakhrul/CVE-2026-54121 確認。
- **Clop Windchill**: BleepingComputer が July 24 の記事リストに掲載、Ransom-ISAC も "Since July 20" の新キャンペーン開始を確認。CVE-2026-12569 自体は 6 月公開・CISA KEV 追加済みだが新規 extortion campaign として採用。
- **JVNDB-2026-000085 (Ricoh SSH)**: "first published on July 23, 2026" の記述複数ソースで確認。

### 取得失敗ソース

- 全 WebFetch 試行が 403 Forbidden (bleepingcomputer.com / thehackernews.com / helpnetsecurity.com / huntress.com / zenity.io / accomplish.ai / guardianmssp.com 等)
- 上記全てを WebSearch スニペット・二次ソース (guardianmssp / cyberpress / securityonline / cybertechworld / gbhackers 等) で代替

</details>

---

*生成: keda-digest-bot / 2026-07-25 05:04 JST*
