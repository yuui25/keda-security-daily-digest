# KEDA Daily Digest — 2026-05-20 (JST)

> 採用範囲: 公開日 2026-05-18 〜 2026-05-20
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Google I/O 2026 が 5月19日（米国時間）に開幕し、Gemini 3.5 Flash・Gemini Omni Flash（動画生成）・Gemini Spark（パーソナル AI エージェント）が即日リリース。30 年ぶり最大のアップグレードとされる AI Mode in Google Search も同時展開された。セキュリティ面では、InfoGuard Labs が SEPPmail Secure E-Mail Gateway に CVSS 10.0 を含む 4 件の脆弱性を公開し、Fedora / Arch Linux 等向けの Linux カーネル LPE「DirtyDecrypt」（CVE-2026-31635）の PoC が公開。また NYC Health + Hospitals が 180 万人規模の生体情報を含む医療データ侵害を正式開示した。

## AI 関連ニュース

- **[2026-05-19]** [Google I/O 2026: Gemini 3.5 Flash を即日 GA リリース — 競合比 4 倍高速・$1.50/$9.00 per 1M トークンで API/AI Studio/Vertex AI から利用可能](https://siliconangle.com/2026/05/19/google-targets-ai-agents-video-generation-gemini-3-5-flash-omni/) — Google が Gemini 3.5 Flash を発表し即日一般提供。Terminal-Bench 2.1 で 76.2%、MCP Atlas で 83.6% を記録し前世代 Pro を速度と精度で上回る。 *(SiliconAngle)*
- **[2026-05-19]** [Google I/O 2026: Gemini Omni Flash を即日リリース — テキスト・音声・画像・動画を横断生成、全動画に SynthID 透かしを付与](https://techcrunch.com/2026/05/19/googles-gemini-omni-turns-images-audio-and-text-into-video-and-thats-just-the-start/) — 「create anything from any input」を謳う新マルチモーダルアーキテクチャの第 1 弾。生成動画への SynthID 透かし埋め込みでディープフェイク検証を可能に。Gemini App・YouTube Shorts・Flow に同日展開。 *(TechCrunch)*
- **[2026-05-19]** [Google I/O 2026: Gemini Spark 発表 — Google Cloud VM 上で 24/7 稼働するパーソナル AI エージェント、Android Halo から進捗をリアルタイム確認](https://www.tomsguide.com/news/live/google-io-2026-live-news-updates) — 受信箱整理・会議ブリーフ作成・ショッピングカート管理を自律実行。ユーザーが離席中も稼働継続し、Android Halo UI でタスク状況を表示。年内提供予定。 *(Tom's Guide)*
- **[2026-05-19]** [Google I/O 2026: AI Mode in Google Search — 30 年ぶり最大のアップグレードとして複雑クエリの多段階解決機能を展開](https://www.engadget.com/2176896/everything-google-announced-io-2026-gemini-omni-spark/) — Google Search が Gemini 3.5 Flash をバックエンドに採用した AI Mode を導入。複合条件のクエリを複数ステップに分解して回答し、結果のソースも明示。 *(Engadget)*
- **[2026-05-19]** [Google I/O 2026: Ask YouTube — YouTube を AI チャットボット化し最適動画をリアルタイム検索・要約する機能を発表](https://www.analyticsinsight.net/artificial-intelligence/google-io-2026-live-updates-gemini-android-17-xr-glasses-and-more) — テキスト・音声クエリで YouTube 動画を横断検索し、内容を要約しながら関連クリップを推薦する新機能を I/O 2026 で公開。 *(Analytics Insight)*
- **[2026-05-19]** [Google I/O 2026: Gemini for Science + Co-Scientist 発表 — 細胞シミュレーション・長期気象予測など科学研究向け AI ツール群を Labs 実験として公開](https://blog.google/innovation-and-ai/technology/research/gemini-for-science-io-2026/) — 研究者向け AI パートナー Co-Scientist をはじめ、生物・気象・材料科学領域のモデリング実験環境を Gemini Labs に追加。 *(Google Blog)*
- **[2026-05-19]** [Google I/O 2026: Project Mariner 更新 — WebVoyager ベンチ 83.5%・クラウド VM 上で 10 タスク並行処理を達成](https://thetechportal.com/2026/05/20/google-introduces-gemini-omni-gemini-3-5-flash-ai-powered-search-upgrades-and-more-at-i-o-2026/) — Gemini 2.0 ベースの Web ブラウジングエージェントが刷新され、同時実行タスク数と精度を大幅向上。 *(The Tech Portal)*
- **[2026-05-19]** [Google I/O 2026: Samsung との Android XR スマートグラス初公開 — Gemini 常時稼働の空間 UI、2026 年秋発売予定](https://www.androidauthority.com/what-to-expect-from-google-io-2026-3664979/) — Samsung と共同開発の Android XR グラスを初の実機デモ。Gemini が視界上に情報を重畳表示し、音声コマンドでエージェントを操作可能。 *(Android Authority)*
- **[2026-05-19]** [Anthropic 「Code with Claude」ロンドン大会開催 — 5月19〜20日、Claude Code / MCP のハンズオンと Anthropic エンジニアによるオフィスアワーを実施](https://claude.com/code-with-claude/london) — Anthropic 第 2 回開発者カンファレンスがロンドンで開催。Head of Claude Code・Boris Cherny をはじめとする登壇陣がエージェント型 AI 開発の実装例を紹介。20日は独立開発者向け拡張セッション。 *(Anthropic)*
- **[2026-05-18]** [OpenAI × マルタ政府: 全市民に ChatGPT Plus 1 年無料提供 — AI リテラシー講座修了が条件の世界初・国家規模 AI アクセスプログラム](https://openai.com/index/malta-chatgpt-plus-partnership/) — マルタ大学開発の無料 AI リテラシー講座を修了した市民に ChatGPT Plus を 1 年間無償付与する "AI for All" プログラムを発表。海外在住のマルタ市民も対象。 *(OpenAI Blog)*

## セキュリティ関連ニュース

- **[2026-05-19]** [SEPPmail Secure E-Mail Gateway に CVSS 10.0 含む 4 脆弱性を公開 — 認証不要 RCE・LFI・環境変数漏洩の組み合わせでメールゲートウェイを完全乗っ取り可能](https://thehackernews.com/2026/05/seppmail-secure-e-mail-gateway.html) — InfoGuard Labs が CVE-2026-2743（CVSS 10.0 / 経路系）・CVE-2026-44128（CVSS 9.3 / eval インジェクション）・CVE-2026-7864（情報漏洩）・CVE-2026-44127（LFI）を公開。15.0.4 以降で全修正。 *(The Hacker News)*
- **[2026-05-18]** [NYC Health + Hospitals が 180 万人規模の医療・生体データ侵害を開示 — 指紋・掌紋・診断記録・銀行情報が 2025 年 11 月〜2026 年 2 月に流出](https://techcrunch.com/2026/05/18/nyc-health-and-hospitals-says-hackers-stole-medical-data-and-fingerprints-during-breach-affecting-at-least-1-8-million-people/) — サードパーティベンダへの不正侵入を起点に、患者・職員の生体認証情報・社会保障番号・パスポートを含む広範なデータが約 180 万件流出。HHS への報告は 3月24日。 *(TechCrunch)*
- **[2026-05-18]** [DirtyDecrypt (CVE-2026-31635) の PoC を公開 — CONFIG_RXGK 有効の Fedora / Arch Linux / openSUSE でローカル root 昇格が可能](https://www.bleepingcomputer.com/news/security/exploit-available-for-new-dirtydecrypt-linux-root-escalation-flaw/) — Zellic / V12 チームが rxgk_decrypt_skb() の COW ガード欠落（CVSS 7.5）を報告し PoC を公開。コンテナ環境ではノード脱出の踏み台になり得る。パッチは 2026年4月25日適用済。 *(BleepingComputer)*
- **[2026-05-18]** [SOGo ウェブメール CVE-2026-8851 開示 — 認証済みユーザが ACL 管理エンドポイントの SQL インジェクションで DB から任意データを外部送出可能 (CVSS 8.6)](https://www.thehackerwire.com/vulnerability/CVE-2026-8851/) — SOGo 5.12.7 の addUserInAcls エンドポイントで uid パラメータが非サニタイズのまま SQL に挿入。sogo_acl テーブルへの書き込みを利用したアウトオブバンドデータ抽出が可能。SOGo 5.12.8 で修正予定。 *(TheHackerWire)*

## 国内脆弱性・インシデント情報

> 直近2日間に該当する新規ニュースは確認できませんでした。

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-05-18 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-2743 | SEPPmail Gateway ≤ 15.0.3 | CWE-22 / 10.0 | LFT 機能の path traversal で nobody ユーザが syslog.conf を上書き → Perl リバースシェル → 認証不要プリオース RCE | [Advisory](https://labs.infoguard.ch/posts/seppmail_secure_e-mail_gateway_rce_vulnerabilities_cve-2026-2743_cve-2026-7864_cve-2026-44127_cve-2026-44128/) (commit 不明 / closed source) | 最高 (メールゲートウェイ完全乗取・他 MTA 実装への水平伝播候補) |
| CVE-2026-44128 | SEPPmail Gateway ≤ 15.0.2 | CWE-95 / 9.3 | /api.app/template の upldd パラメータをサニタイズせず Perl eval() に渡す → 認証不要 RCE | [Advisory](https://labs.infoguard.ch/posts/seppmail_secure_e-mail_gateway_rce_vulnerabilities_cve-2026-2743_cve-2026-7864_cve-2026-44127_cve-2026-44128/) (commit 不明 / closed source) | 高 (Perl テンプレートエンジン eval() 注入バリアントの起点) |
| CVE-2026-7864 | SEPPmail Gateway ≤ 15.0.3 | CWE-200 / 6.9 | GINA UI の未認証エンドポイントがサーバ環境変数をそのまま返す → 次段攻撃の事前情報収集に悪用 | [Advisory](https://labs.infoguard.ch/posts/seppmail_secure_e-mail_gateway_rce_vulnerabilities_cve-2026-2743_cve-2026-7864_cve-2026-44127_cve-2026-44128/) (commit 不明 / closed source) | 中 (チェーン攻撃の偵察ステップ) |
| CVE-2026-44127 | SEPPmail Gateway ≤ 15.0.2 | CWE-22 / - | 未認証 LFI でメール本文・証明書・設定ファイルを直接読み取り可能 | [Advisory](https://labs.infoguard.ch/posts/seppmail_secure_e-mail_gateway_rce_vulnerabilities_cve-2026-2743_cve-2026-7864_cve-2026-44127_cve-2026-44128/) (commit 不明 / closed source) | 高 (メール内容傍受・S/MIME 秘密鍵奪取リスク) |
| CVE-2026-31635 | Linux kernel (CONFIG_RXGK 有効: Fedora / Arch / openSUSE Tumbleweed) | CWE-119 / 7.5 | rxgk_decrypt_skb() に COW ガードが欠落 → ページキャッシュへの不正書き込み → ローカル root LPE (PoC 公開済) | [BleepingComputer](https://www.bleepingcomputer.com/news/security/exploit-available-for-new-dirtydecrypt-linux-root-escalation-flaw/) (パッチ 2026-04-25 / commit 不明) | 高 (PoC 公開・コンテナノード脱出の踏み台候補) |
| CVE-2026-8851 (GHSA-7VV4-J48F-WCX7) | SOGo Webmail 5.12.7 | CWE-89 / 8.6 | addUserInAcls エンドポイントの uid パラメータが非サニタイズで SQL サブクエリを許容 → 認証済みユーザが OOB 書き込みで DB 内任意データを抽出 | [NVD](https://nvd.nist.gov/vuln/detail/CVE-2026-8851) (fix: SOGo 5.12.8 / commit 不明) | 中 (カレンダー / グループウェア運用組織は要確認) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 25
- 採用件数: AI=10 / Security=4 / CVE=6 / 国内=0
- 除外理由内訳: 古すぎ (2026-05-17以前)=19 / 重複 (前ダイジェスト収録済)=14 / 日付不明=2
- 主な除外理由の詳細:
  - **期間外**: Exim CVE-2026-45185 (2026-05-12) / Windows YellowKey・GreenPlasma (2026-05-12) / node-ipc 供給チェーン攻撃 (2026-05-14〜15 / 05-16 ダイジェスト収録済) / Google Threat Intelligence AI 生成ゼロデイ (2026-05-11) / Cisco CVE-2026-20182 (2026-05-15 / 05-16 ダイジェスト収録済) / Android 17 セキュリティ機能 (2026-05-12〜13 / The Android Show)
  - **前ダイジェスト重複**: NGINX CVE-2026-42945 / Exchange CVE-2026-42897 / MiniPlasma PoC / brace-expansion CVE-2026-45149 / webpack-dev-server CVE-2026-6402 / n8n-mcp CVE-2026-45707 / dynoxide GHSA-fvh2-gm75-j4j7 / Pwn2Own Berlin 全日程 / Linux CVE-2026-31431 系列 / Synack レポート / Google I/O 前夜プレビュー
- 取得失敗ソース: nvd.nist.gov・labs.infoguard.ch・bleepingcomputer.com・techcrunch.com・blog.google・jpcert.or.jp・jvn.jp・sentinelone.com 他 — すべて HTTP 403 Forbidden で本文取得不可。日付確認は URL 日付パターン (cypro.se `/2026/05/19/`・techcrunch.com `/2026/05/18/`・siliconangle.com `/2026/05/19/`・thetechportal.com `/2026/05/20/`)・検索スニペット・第三者ミラーサイトで実施。

</details>
