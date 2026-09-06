# KEDA Daily Digest — 2026-09-07 (JST)

> 採用範囲: 公開日 2026-09-05 〜 2026-09-07
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Sansec が Magento/Adobe Commerce 全バージョン対象の未修正 RCE zero-day「StyleSmuggler」を 9/5 に公開、Adobe は 9/6 現在もパッチ・CVE・アドバイザリ未提供のまま野外悪用が継続中。MikroTik RouterOS では CVE-2026-67276 と CVE-2026-86060 を連鎖させる「MikroTrick」が 9/2 から悪用継続しており、Chrome 152 の 9/6 更新（WebGL・Shared Tab Groups の Critical UAF 計 2 件含む 26 件修正）および Citrix NetScaler CVE-2026-19490（CVSS 9.3）への実悪用移行が重なり、パッチ適用の優先度が高い週となった。AI 面では米中が 9 月中旬の初二国間 AI 安全対話を発表し（9/5 Reuters）、EU AI Office が高リスク審査を 9 月から正式始動した。

## AI 関連ニュース

- **[2026-09-06]** ['Model fatigue' が本格化 — Meta/Google/OpenAI/Anthropic が 1 週間で Muse Spark 1.3 / Gemini 3.8 Flash / GPT-6 Astra / Fable 5.1 を相次ぎ投入し、企業が乗り換え評価コストを理由に採用先を絞り込む傾向が浮上](https://www.cnbc.com/2026/09/06/meta-google-openai-anthropic-ai-model-fatigue.html) — Gartner 予測 2026 年 AI 支出 $2.59T（+47%）の中でもモデル疲弊が深刻化。投資家が特定モデルへの依存リスクを懸念し始めている。 *(CNBC)*

- **[2026-09-05]** [米中、9 月中旬に初の二国間専用 AI 安全対話を開催へ — 財務長官 Bessent 主導、AI 起因サイバー攻撃の共同監視と AI ラボ自主規制スキームを議題に](https://www.cnbc.com/2026/09/05/us-china-gear-up-for-mid-september-ai-safety-talks-reuters.html) — Trump 政権下で初の AI 専用米中対話。9/24 の米中首脳会議前実施予定。ホワイトハウスは公式日程を否定するも、Reuters が準備進行を報道。サイバー攻撃に AI を使用する際の情報共有提案も含む。 *(CNBC / Reuters / Japan Times)*

- **[2026-09-05]** [EU AI Act 高リスク審査が 9 月から本格始動 — EU AI Office・CNIL・BfDI・AESIA が採用スクリーニング AI と信用評価 AI への Article 11 技術ファイル審査を開始](https://cubbbix.com/blog/ai-regulation-september-2026-global-update) — 8/2 猶予期間終了後、EU AI Office が 24 か国の市場監視当局と技術監査を正式化。高リスク AI を展開する企業は技術ファイル整備・人間監視記録・インシデント報告義務が即時適用。 *(Cubbbix / CSA)*

- **[2026-09-04]** [[Catch-up] Google Lyria 3.5 — 音楽生成モデルを Gemini アプリと Gemini API に展開、最大 3 分フルコーラス生成・44.1kHz ステレオ・テキスト/画像入力対応](https://blog.google/innovation-and-ai/models-and-research/google-labs/lyria-3-5/) — ボーカル付き歌詞・楽器演奏・タイミング構造を 1 プロンプトで生成。Google Flow Music でデビュー後、グローバル展開。Gemini API 経由での企業統合が可能に。 *(Google Blog)*

- **[2026-09-04]** [[Catch-up] Adversa AI「Agentic AI セキュリティリソース September 2026 — 37 選」公開 — 暗号化コンテキストインジェクション・静的解析による excessive agency 検出・最小権限設定の自動生成手法を網羅](https://adversa.ai/blog/top-agentic-ai-security-resources-september-2026/) — エージェントの tool capability graph から sensitive data → external tool への経路を自動 flagging するフレームワーク実装例が注目。AI 開発者向けセキュリティチェックリストとして参照価値が高い。 *(adversa.ai)*

- **[2026-09-04]** [[Catch-up] Artificial Analysis Intelligence Index v4.2 公開 — Claude Fable 5.1 が GPT-6 Astra・Meta 系モデルを抑えてトップ、セキュリティ/数理/長文処理の 5 軸評価で更新](https://artificialanalysis.ai/) — Fable 5.1 の Terminal-Bench-Science が 52.6（Fable 5: 24.7）と 2 倍超の向上。独立ベンチマーク機関による評価で Astra との性能差が可視化された。 *(Artificial Analysis)*

- **[2026-09-04]** [[Catch-up] SoundHound AI、LivePerson 買収を完了 — 音声/エージェント AI × Fortune 100 × 25 社のデジタルメッセージング基盤が統合、$500M 将来収益ポテンシャルを発表](https://blog.mean.ceo/ai-news-september-2026/) — 全負債を完済して買収完了。SoundHound の LLM-first Voice AI と LivePerson の 25 年分エンタープライズチャット資産が一体化し、コールセンター代替市場への攻勢を強化。 *(AI Startup Edition)*

## セキュリティ関連ニュース

- **[2026-09-05]** [StyleSmuggler — Magento/Adobe Commerce 全バージョン対象の未修正 RCE zero-day を Sansec が公開、9/4 から野外悪用が継続中でパッチなし](https://sansec.io/research/stylesmuggler) — 未認証攻撃者が GraphQL の styles プロパティを操作→ Magento が「Payment Transaction Failed Reminder」メールを生成した瞬間に PHP コードがサーバで実行（RCE）、メール送受信は不要。2.4.9（現行最新）を含む全バージョン確認済み。暫定対策: ヘッドレス/PWA 以外の店舗は GraphQL を無効化。 *(Sansec / The Hacker News / CyberSecurityNews)*

- **[2026-09-05]** [MikroTik RouterOS「MikroTrick」— CVE-2026-67276 と CVE-2026-86060 を連鎖して未認証で完全制御、パッチ前から悪用中](https://cert.pl/en/posts/2026/09/vulnerabilities-in-mikrotik-routeros-actively-exploited/) — CVE-2026-67276: SSH が公開鍵の RSA Modulus のみ検証し Exponent を省略するためシグネチャ偽造が可能。CVE-2026-86060: 禁止文字から始まるユーザー名で root 昇格。CERT Polska 調整開示、RouterOS 6.49.21 / 7.23.4 / 7.24.2 でパッチ済み（9/3 リリース）、未適用環境への即時適用が急務。 *(CERT Polska / AiCybr / Security Affairs)*

- **[2026-09-06]** [Chrome 152 セキュリティ更新 — 計 26 件修正、CVE-2026-84352（WebGL UAF, Critical）と CVE-2026-84353（Shared Tab Groups UAF, Critical）が最高重大度](https://chromereleases.googleblog.com/) — Google は野外悪用を未確認。9/4 バッチ（CVE-2026-85042/47/50）とは別の一斉修正。Chrome 153 は 9/8 リリース予定。即時アップデートを推奨。 *(Google Chrome Releases / Malwarebytes)*

- **[2026-09-05]** [Citrix NetScaler CVE-2026-19490（CVSS v4.0: 9.3）— PoC 公開後に実悪用フェーズへ移行、複数 IP からの攻撃トラフィックを観測](https://www.rapid7.com/blog/post/etr-cve-2026-19490-critical-vulnerability-affecting-citrix-netscaler-adc-and-netscaler-gateway/) — 8/21 公開の NetScaler ADC/Gateway 認証バイパス（CWE-288）。AAA 仮想サーバまたは Gateway（SSL VPN/ICA Proxy/RDP Proxy）設定環境が対象。Previdian が公開 PoC と一致するリクエストを複数 IP から検知。緊急パッチ適用を呼びかけ。 *(Rapid7 / Help Net Security / BleepingComputer)*

- **[2026-09-04]** [Rhysida ランサムウェア — ベルリン州政府の 5.8TB/144 万ファイルをダークウェブ公開、KRITIS 関連インフラ脆弱性分析や平文認証情報を含む](https://cybernews.com/news/stolen-berlin-government-files-dumped-on-dark-web-rhysida/) — 8/28 に 30 BTC（約€200 万）を要求・7 日間カウントダウン後、身代金不払いでデータを公開。5,000+ 人事ファイル・健康記録・パスポート・ベルリン水道の脆弱性分析を含む。初期侵入後 7 日間ネットワーク分離が遅れたことで 5.8TB の大量窃取を許した。 *(Cybernews / TechTimes)*

- **[2026-09-04]** [[Catch-up] ASUS Control Center Enterprise CVE-2026-75754（CVSS 4.0: 10.0）— 認証欠如＋SSRF＋ハードコード資格情報の 3 弱点連鎖で未認証リモート root が可能、過去ダイジェスト未収録](https://cybersecuritynews.com/asus-control-center-vulnerability/) — ACC v4.0.0.2 以前が対象、v3.1.0.9 以降へ更新を推奨。攻撃者が暗号鍵を奪取後に管理下全 PC/サーバを制御可能。ポート 2222 ブロックと管理インターフェース隔離が暫定措置。 *(CyberSecurityNews / Cryptika / OffSeq)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 today-2 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先
> ※ CVE-2026-75754 (09-04 公開)・CVE-2026-19490 (08-21 公開・09-05 実悪用確認) は採用窓外だが過去ダイジェスト未収録のためキャッチアップ採用

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| StyleSmuggler (CVE 未採番) | Magento Open Source / Adobe Commerce ≤ 2.4.9（現行最新を含む全バージョン） | CWE-94 (疑) / CVSS TBD | 未認証攻撃者が GraphQL の styles プロパティに PHP コードを注入→ Magento が Payment Transaction Failed Reminder メール生成時に内部テンプレートをレンダリング→ PHP が RCE として実行（メール送受信不要） | パッチ未公開 / [Sansec 開示](https://sansec.io/research/stylesmuggler) | 未認証 / パッチなし / 全バージョン影響 / 09-04 野外悪用確認 / メール系テンプレートエンジンへの水平バリアント候補 |
| CVE-2026-84352 | Google Chrome ≤ 152.x (09-05 以前, WebGL) | CWE-416 / Critical | 細工した HTML が WebGL レンダリング中に解放済みオブジェクトを参照させ→ GPU プロセスの任意コード実行→ sandbox 外へのエスケープ | [Chrome 152 Sep 6 Stable Update](https://chromereleases.googleblog.com/) | Critical / WebGL は Firefox/Safari/Edge 同等実装へのバリアント候補 |
| CVE-2026-84353 | Google Chrome ≤ 152.x (09-05 以前, Shared Tab Groups) | CWE-416 / Critical | 細工した HTML が Shared Tab Groups コンポーネントの UAF を誘発→ browser プロセスで任意コード実行→権限昇格の起点 | [Chrome 152 Sep 6 Stable Update](https://chromereleases.googleblog.com/) | Critical / Tab Groups は Chromium ベースの Edge/Brave へのバリアント候補 |
| CVE-2026-67276 | MikroTik RouterOS ≤ 6.49.20 / 7.23.3 / 7.24.1 | CWE-347 / CVSS 9.2 | SSH サーバが公開鍵認証時に RSA Modulus のみ検証し Exponent を省略→攻撃者が既知 Modulus を持つ別鍵ペアで有効なシグネチャを偽造→任意ユーザとして未認証 SSH セッションを確立 | [MikroTik September 2026 Security Fix](https://mikrotik.com/supportsec/september-2026-vulnerability/) | CVSS 9.2 / 09-02 から野外悪用 / MikroTrick の起点 / SSH 公開鍵検証省略バグは libssh・OpenSSH 実装へのバリアント調査推奨 |
| CVE-2026-86060 | MikroTik RouterOS ≤ 6.49.20 / 7.23.3 / 7.24.1 | CWE-269 / 未公表 | 未認証 SSH セッション確立後（CVE-2026-67276 連鎖）、SSH ログインパスに禁止文字で始まるユーザー名を送信→引数処理ロジックが特権昇格を誘発→ root 完全制御 | [MikroTik September 2026 Security Fix](https://mikrotik.com/supportsec/september-2026-vulnerability/) | MikroTrick 2段目 / ネットワーク機器の SSH 引数処理バグはルータ/スイッチ全般へのバリアント候補 |
| CVE-2026-75754 | ASUS Control Center Enterprise (ACC) ≤ v4.0.0.2 | CWE-306 + CWE-918 + CWE-798 / CVSS 4.0: 10.0 | 未認証攻撃者が SSRF で特定 HTTP リクエストを送信→ハードコード認証情報で内部認証バイパス→暗号鍵を奪取→root 権限でコマンド実行・管理下全エンドポイントを制御 | [ACC v3.1.0.9](https://www.asus.com/supportonly/asus%20control%20center%20enterprise/helpdesk_bios/) (commit 不明) | CVSS 10.0 / 未認証 / 3 弱点連鎖 / IT 資産管理製品の同類 SSRF＋ハードコード資格情報パターンへのバリアント候補 |
| CVE-2026-19490 | Citrix NetScaler ADC / NetScaler Gateway (AAA 仮想サーバまたは Gateway 設定時) | CWE-288 / CVSS v4.0: 9.3 | 未認証リモート攻撃者が Alternative Authentication Path を経由→ AAA または Gateway の認証チェックをバイパス→認証不要で内部リソースにアクセス | [Citrix Security Advisory](https://support.citrix.com/) (commit 不明) | CVSS 9.3 / 09-05 実悪用開始 (PoC 公開後) / NetScaler は大規模 VPN/AAA 基盤として広範利用 / 認証バイパス Alternate Path パターンは他 VPN 製品へのバリアント候補 |

## 国内脆弱性・インシデント情報

> 直近2日間（2026-09-05〜2026-09-07）に該当する新規 JVN/JPCERT/IPA アドバイザリは確認できませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 20+（CNBC, Reuters, Japan Times, Google Blog, adversa.ai, Artificial Analysis, SoundHound/AI Startup Edition, Sansec, CERT Polska, Google Chrome Releases, Rapid7, Help Net Security, BleepingComputer, Cybernews, CyberSecurityNews, ASUS Security, Malwarebytes, CSA, Cubbbix, MikroTik Security, OffSeq Threat Radar, JVN/JPCERT/IPA 各サイト）
- 採用件数: AI=7 / Security=6 / CVE=7 / 国内=0
- 除外理由内訳:
  - 重複 (excluded_set 該当): CVE-2026-85046 Chrome V8 (09-05 digest 済み)、GPT-6 Astra 発表 (09-05 digest 済み)、Anthropic IPO 延期 (09-06 digest 済み)、Claude Fermat 証明 (09-06 digest 済み)、Palo Alto Unit 42 AI 10 時間攻撃 (09-06 digest 済み)、OpenAI Cyber Summit (09-06 digest 済み)、F5 AI WAF / Ping Identity AI エージェントセキュリティ (09-06 digest 済み)、CrowdStrike SafeMind (Sep 1・過去窓内未収録だが Sep 7 窓外のためスキップ)、PaperCut CVE-2026-82078/81578 (09-03 digest 済み)、CISA KEV 7件 (09-04 digest 済み)、Chrome 152 Sep 4 更新 CVE-2026-85042/47/50 (09-06 digest 済み)、IBM ODM CVE-2026-18658 (09-06 digest 済み)、PostgreSQL PostGREShell CVE-2026-6471 (09-06 digest 済み)、FalconFlank (09-06 digest 済み)、WordPress Super Forms 440K 悪用 / CVE-2026-14894 (09-05 digest 済み)、Manchester Airports Group (09-05 digest 済み)
  - 窓外 (< 2026-09-05) でスキップ: Firefox 155 (Sep 1)、CVE-2026-84129 Mozilla (Sep 1)、GLM-5.3-Flash (Aug 26)、OpenAI Canada school shooting lawsuit (Sep 2)、G20 Carolina Principles (Sep 1)
  - キャッチアップ採用 (採用窓外だが過去ダイジェスト未収録): CVE-2026-75754 ASUS Control Center (Sep 4)、CVE-2026-19490 Citrix NetScaler (Aug 21 公開・Sep 5 実悪用)、Rhysida Berlin 5.8TB dump (Sep 4)、Google Lyria 3.5 (Sep 4)、Adversa AI Agentic Resources (Sep 4)、Artificial Analysis Index v4.2 (Sep 4)、SoundHound AI × LivePerson 買収完了 (Sep 4)
  - 日付不明・詳細取得不可: Chrome Sep 6 正確なバージョン番号、Firefox ESR 更新版 CVE 詳細、Forescout Project Watershed 250 公開日
- 取得失敗ソース（EGRESS_BLOCKED）: llm-stats.com, sansec.io, cert.pl, cybersecuritynews.com, gbhackers.com, cnbc.com, bleepingcomputer.com, thehackernews.com, securityonline.info, radar.offseq.com, nvd.nist.gov, cisa.gov, osv.dev, cvebrief.com, innovatecybersecurity.com, cyberpress.org, aicybr.com（WebSearch スニペット・アクセス可能ミラーサイト経由で情報補完）

</details>
