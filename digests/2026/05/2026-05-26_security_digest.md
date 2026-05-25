# KEDA Daily Digest — 2026-05-26 (JST)

> 採用範囲: 公開日 2026-05-24 〜 2026-05-26
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

14億人の信者を持つカトリック教会が AI 倫理に関する初の教皇勅書 "Magnifica Humanitas" を発布し、史上最大規模の制度的 AI 声明として注目を集めた。セキュリティ面では Lazarus Group による記憶常駐型 RAT (RemotePE) と TrapDoor サプライチェーン攻撃（AI コーディングツール設定ファイルへの hidden instruction 注入を含む）が同日公開され、開発者・金融機関への多角的脅威が顕在化。Anthropic は今週中にも $900B+ 評価での $30B ラウンドをクローズし OpenAI を抜いて最大 AI スタートアップに浮上する見込み。

---

## AI 関連ニュース

- **[2026-05-25]** [Pope Leo XIV が AI 時代の人間の尊厳・労働・共通善をテーマに教皇勅書 "Magnifica Humanitas" を発布](https://www.vaticannews.va/en/pope/news/2026-05/pope-leo-xiv-first-encyclical-magnifica-humanitas.html) — AI による監視・自律兵器・デジタル格差を名指しで批判し、国際的な AI 規制フレームワーク構築と倫理審査機関の設立を訴求。Anthropic 共同創業者 Christopher Olah が発表イベントに参席。 *(Vatican News / CNN)*

- **[2026-05-22〜]** [[続報] Anthropic が 2026年内2度目の $30B ラウンドを今週クローズ予定 — 評価額 $900B+ で OpenAI ($852B) を超え最大 AI スタートアップへ](https://www.bloomberg.com/news/articles/2026-05-22/anthropic-to-close-over-30-billion-round-as-soon-as-next-week) — Sequoia・Dragoneer・Altimeter・Greenoaks が各 $2B 超を共同投資；Q2 売上 $10.9B、初の営業黒字を見込む *(Bloomberg)*

- **[2026-05-25]** [TrapDoor サプライチェーン攻撃が CLAUDE.md / .cursorrules へ hidden instruction を注入し AI コーディングアシスタントを操作](https://socket.dev/blog/trapdoor-crypto-stealer-npm-pypi-crates) — npm/PyPI/Crates.io 横断で 34 パッケージ・384+ バージョンを汚染、AI ツールが malicious なプロジェクト指示を自動で解釈・実行する新攻撃手口を初確認 *(Socket)*

---

## セキュリティ関連ニュース

- **[2026-05-25]** [Lazarus Group が RemotePE 記憶常駐型 RAT を金融・暗号資産企業に展開 — DPAPILoader → RemotePELoader → C2 ポーリングの 3 段階チェーン](https://thehackernews.com/2026/05/lazarus-deploys-remotepe-memory-only.html) — RAT は C++ 製・メモリ上のみで実行しディスクへの書き込みなし、EDR 回避・フォレンジック痕跡ゼロを実現。Fox-IT が 5月22日のブログで詳細分析を公開 *(Fox-IT / The Hacker News)*

- **[2026-05-25]** [TrapDoor サプライチェーン攻撃: npm/PyPI/Crates.io の 34 パッケージ・384+ バージョンに認証情報窃取フレームワークを埋め込み](https://thehackernews.com/2026/05/trapdoor-supply-chain-attack-spreads.html) — SSH 鍵・Solana/Sui/Aptos ウォレット・AWS 認証情報・GitHub トークン・ブラウザパスワードが標的。Socket が最初の公開から中央値 5分 27秒で検出 *(Socket / The Hacker News)*

- **[2026-05-25]** [[続報] Ghost CMS CVE-2026-26980 ClickFix キャンペーン拡大: Harvard・DuckDuckGo 含む 700+ サイトが偽 Cloudflare 認証画面を表示](https://www.techtimes.com/articles/317134/20260525/ghost-cms-sql-injection-hits-700-sites-harvard-duckduckgo-serve-fake-cloudflare-malware.htm) — Admin API Key 奪取→JS 注入→FakeCaptcha (ClickFix) でマルウェア配布、被害拡大継続中。Ghost 6.19.1 未適用サイトは即時更新を *(TechTimes)*

- **[2026-05-25]** [Google が未修正 Chromium バグの PoC コードを誤公開: Background Fetch API で JS をブラウザ終了後も常駐させリモート実行が可能](https://www.bleepingcomputer.com/news/security/google-accidentally-exposed-details-of-unfixed-chromium-flaw/) — Chrome/Edge/Brave/Opera/Vivaldi/Arc 等 Chromium 系全般に影響。Safari・Firefox は非対象。悪用で tens of thousands 規模のボット化が現実的と研究者。未修正・CVE 未採番 *(BleepingComputer / Business Standard)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-05-24 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

> 直近2日間に該当する新規 CVE / Advisory は確認できませんでした。
> (直近7日分の excluded_set と照合済み; 当日範囲内の新規採番・公開 advisory が検索エンジン・GHSA・NVD から取得できなかった)

---

## 国内脆弱性・インシデント情報

> 直近2日間に該当する新規ニュースは確認できませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 30（WebSearch 35回、WebFetch 20回試行）
- 採用件数: AI=3 / Security=4 / CVE=0 / 国内=0
- 除外理由内訳:
  - 古すぎ (> today-2 = 2026-05-24): Pwn2Own Berlin (May 14-16), GitHub TeamPCP 正式確認 (May 19-20), Laravel-Lang 攻撃 (May 22-23), CVE-2026-9082 Drupal KEV 追加 (May 22), NSA MCP ガイダンス (May 20), Google I/O 発表群 (May 19), KimWolf 逮捕 (May 21), Trump AI EO キャンセル (May 21), DeepMind Contextual AI acquihire (May 19-20), OpenAI Erdős 数学証明 (May 20), Grok Build 0.1 (May 20-21), CVE-2026-46333 Linux ptrace (公開 May 20), CVE-2026-5194 wolfSSL (パッチ April 8)
  - 重複 (excluded_set): CVE-2026-26980 Ghost CMS 初回報道 (May 23 digest), CVE-2026-48172 LiteSpeed (May 25 digest), CVE-2026-34908/09/10 UniFi (May 22 digest/May 24 digest), CVE-2026-46716/46717/47124 Nezha (May 24 digest), Project Glasswing 初報 (May 25 digest), GitHub/TanStack [続報] (May 25 digest), CVE-2026-42945 NGINX Rift (excluded_set), CVE-2026-42897 Exchange XSS (excluded_set), CVE-2026-45585 YellowKey (excluded_set)
  - 日付不明 / 確認不可: GHSA-g9cw-qwhf-24jp 等 OSV.dev 新規 advisory (日付確認できず)
  - CVE section 0件の理由: 2026-05-24〜26 に NVD/GHSA で新規採番・公開された critical/high advisory を複数経路で検索したが、excluded_set に含まれないものが取得できなかった
- 取得失敗ソース: thehackernews.com (403), bleepingcomputer.com (403), nvd.nist.gov (403), cisa.gov (403), jpcert.or.jp (403), anthropic.com (403), vaticannews.va (403 → スニペット補完) — WebSearch スニペットで内容・日付を補完

</details>
