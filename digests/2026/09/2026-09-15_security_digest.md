# KEDA Daily Digest — 2026-09-15 (JST)

> 採用範囲: 公開日 2026-09-13 〜 2026-09-15
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

---

## AI 関連ニュース

- [2026-09-14] **OpenAI・Anthropic・Google が AI 安全基準策定の業界団体設立に向けた非公開協議を継続** — Amodei 主導、Altman が政府を待たず自主規律で推進、モデルリリース前の独立評価・共通リスク審査標準化を議論 *(Washington Post / PYMNTS)*
- [2026-09-14] **中国の二重AI立場** — 外務省が Amodei の「スローダウン」要求を「フィアモンガリング」として一蹴、一方で国家安全部長 Chen Yixin は AI が政治安全・重要インフラを脅かすと国内向け最詳細警告を中国サイバースペース誌に掲載 *(Bloomberg)*
- [2026-09-14] **Apple が iOS 27 / Siri AI ベータ版を正式リリース** — Apple Intelligence 大幅刷新、英語のみ・iPhone 15 Pro 以降対応、A20 Pro 搭載 iPhone 17 ではオンデバイス推論が前世代比 2 倍高速 *(Engadget / MacRumors)*
- [2026-09-14] **Microsoft Satya Nadella が MAI モデル向け Code of Conduct を公開コンサルテーション開始（6 週間）** — AI による WMD 支援・サイバー攻撃実行・核開発支援・ディープフェイク生成を明示禁止、「超知能が人間の制御下にないなら追求する価値はない」と表明 *(Unite.AI / Kingy AI)*
- [2026-09-13] **中国系脅威アクター UNC3569 が Sogou Input Method の CVE-2026-51990 を悪用し GRAYRABBIT バックドアを展開** — sgbiz: カスタムプロトコルハンドラ引数注入 + 無制限 URL ナビゲーション + サンドボックスなし旧版 Chromium によるワンクリック RCE の 3 要素チェーン攻撃 *(SecurityWeek / BleepingComputer)*
- [2026-09-14] **Check Point TI: 複数スパイグループが Chrome V8 + Windows 特権昇格の BlueMoon エクスプロイトチェーンを悪用** — ブラウザ侵害・サンドボックス脱出・特権昇格の 3 段階チェーンを確認、標的システムへの侵入を実現 *(Check Point Research)*

---

## セキュリティ関連ニュース

- [2026-09-14] **Chrome/Firefox 拡張機能「Twitch Enhanced Viewer | JeetBot」が 31,000 人の Twitch OAuth トークンをロシア系ボットサービスに漏えい** — 拡張機能がプレイリストリクエストをプロキシ経由でルーティングしトークンを `/set-token` エンドポイントに POST；パスワード・2FA 不要で乗っ取り可能 *(Socket Threat Research)*
- [2026-09-14] **Mathspace（豪 NZ 教育プラットフォーム）が自己ホスト型 Metabase CVE-2026-72898 経由で 100 万人超のデータ漏えいを発表** — 氏名・メール・ユーザー名・所在地が流出、SSN・金融情報は非影響 *(HaveIBeenPwned / Mathspace 公式)*

---

## CVE / 脆弱性情報

| CVE ID | 製品・バージョン | CWE / CVSS | 概要 | 対応 | 備考 |
|--------|----------------|-----------|------|------|------|
| CVE-2026-51990 | Tencent Sogou Input Method for Windows ≤ 16.2.x | CWE-88 / Critical | sgbiz: カスタムプロトコルハンドラが引数を無検証でサンドボックスなし旧版 Chromium に渡す → ワンクリック RCE → GRAYRABBIT バックドア展開 | v16.3.0.3498（自動更新済み）に更新 | 野外悪用中 / UNC3569（中国系）/ 数億ユーザー影響 |
| CVE-2026-81648 | CryptoPayment Gateway WordPress plugin 1.2.1〜1.2.2 | CWE-862 / CVSS 10.0 | 未認証攻撃者が認証・権限チェックのない AJAX エンドポイントに直接リクエスト → 任意ファイル削除・決済ゲートウェイ設定上書き・ウォレット資格情報平文取得 | 最新版へのアップグレード | CVSS 10.0 / WooCommerce 決済プラグイン |
| CVE-2026-90692 / CVE-2026-90693 | D-Link DIR-878 firmware 120B05 | CWE-121 / CVSS 9.9 | 未認証リモート攻撃者が Dynamic DNS IPv6 設定コンポーネントに細工パラメータ → スタックバッファオーバーフロー → ルーター上で任意コード実行 | パッチなし（EoL 2021年、修正予定なし） | EoL デバイス / TP-Link・ASUS 等同種 DDNS 実装への水平展開候補 |
| CVE-2026-84939 | Apache FreeMarker 2.2.0〜2.3.34 | CWE-23 / CVSS 9.1 | 悪意ある細工ロケール識別子を指定 → localized lookup がパス検証なしにベースディレクトリ外へ相対パストラバーサル → テンプレートシステムが制限外ファイルを読み込み・実行 | 2.3.35 | CVSS 9.1 / Java テンプレートエンジン パストラバーサル |
| CVE-2026-84286 | ExLlamaV3 exllamav3_ext CUDA 拡張（全バージョン ≤ 修正版） | CWE-119 / Medium | K=0 の細工入力 → カーネルテーブルディスパッチで境界チェック欠如による負インデックス → 範囲外メモリアクセス → LLM 推論サーバーの DoS | CERT/CC VU#369611 対応パッチ適用 | LLM 推論インフラ / JVNVU#94022278（2026-09-14） |

---

## 国内脆弱性・インシデント情報

| 日付 | JVN 番号 / CVE ID | 製品 | 概要 | 深刻度 |
|------|-----------------|------|------|--------|
| 2026-09-14 | JVNVU#94022278 / CVE-2026-84286 | ExLlamaV3 exllamav3_ext | K=0 入力によりカーネルディスパッチ境界チェック欠如 → DoS | Medium / LLM 推論基盤 |
| 2026-09-14 | JVN#69877538 / CVE-2026-85125 | YAMAP/ヤマップ Android v17.1.0 以前 | WebView アクセス制御不備 — アプリ内ブラウザからの情報漏えいまたは意図しないサイト遷移 | CVSS 5.1 / Android アプリ |

---

## 取得状況（デバッグ）

- 巡回ソース数: 25+
- 採用件数: AI=6 / Security=2 / CVE=5（6項目）/ 国内=2
- 取得失敗ソース: thehackernews.com, bleepingcomputer.com, securityweek.com, jvn.jp, jpcert.or.jp, senserva.com, vulners.com, app.opencve.io, cvebrief.com, xloggs.com, securityonline.info, cvemon.intruder.io, privacyneedle.com, gendigital.com, releasebot.io, qz.com
