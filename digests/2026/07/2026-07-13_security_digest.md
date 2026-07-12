# KEDA Daily Digest — 2026-07-13 (JST)

> 採用範囲: 公開日 2026-07-11 〜 2026-07-13 (JST)
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

OpenAI の **GPT-5.6 Sol Ultra** が 64 サブエージェントを並列動作させ、50 年来の未解決難問「Cycle Double Cover Conjecture」を 1 時間未満で証明した。AI による本格的な数学定理証明として世界的注目を集め、数学コミュニティのピアレビューが進行中。サプライチェーン面では公式 npm パッケージ **jscrambler** CLI の 5 バージョン (週間 DL 6 万超) が Rust 製インフォスティーラーに汚染されており、Socket が公開後 6 分で検出したが既に多数の CI/CD 環境への侵入が懸念される。インフラ面では **Zimbra Classic Web Client** の Stored XSS を Google TAG が報告し国家系 APT による悪用が示唆、**U-Boot** FIT 署名検証の 6 脆弱性 (2013 年以来の全バージョン影響・うち 2 件が RCE ポテンシャル) が公開されベアメタル・BMC 経路での悪用が可能となっている。

## AI 関連ニュース

- **[2026-07-11]** [OpenAI GPT-5.6 Sol Ultra が 50 年来の難問「Cycle Double Cover Conjecture」を 64 エージェントで証明 — 1 時間未満・証明 PDF と 700 語プロンプトを公開](https://openai.com/index/gpt-5-6-sol-ultra-cdc-conjecture/) — 1973 年 Szekeres・1979 年 Seymour が提唱した未解決グラフ理論問題を Sol Ultra が自律的に解決; 700 語の問題説明を入力し 64 サブエージェントが並列で反証検索・証明構築を実施; 数学者コミュニティは現在ピアレビュー中で「形式的に正しければ Fields Medal 級」と評価。*(OpenAI / AI Weekly / Nature News)*

- **[2026-07-12]** [アジェンティック AI ランタイムセキュリティが企業スタックへ本格普及 — First Recon が AI Security Runtime を GA・「Agent Zero Trust」が支配的概念に](https://www.adversa.ai/blog/agentic-ai-security-runtime-2026/) — 全 AI エージェントアクションをリアルタイム検査する専用ランタイムセキュリティ層が商用 GA; 調査では 54% の組織が AI エージェントセキュリティインシデントを既経験; ツール呼出し・メモリアクセス・外部 API 通信を最小権限原則で制御する「Agent Zero Trust」アーキテクチャが標準化へ。*(Adversa AI / First Recon)*

- **[2026-07-11]** [米連邦準備制度が AI の経済的影響を研究する専門委員会を設立 — a16z 共同創業者 Marc Andreessen が共同議長、雇用・金融政策への影響を正式調査](https://aiweekly.co/alerts/fed-ai-economic-impact-committee/) — FRB 初の AI 専任組織として雇用置換・生産性向上・金融政策波及を定量調査; Andreessen 共同議長就任は AI 楽観論者と中央銀行の異例の協働として注目。*(AI Weekly / Reuters)*

## セキュリティ関連ニュース

- **[2026-07-11]** [jscrambler 公式 npm CLI (週間 6 万 DL) の 5 バージョン (8.14.0〜8.20.0) が Rust 製インフォスティーラーで汚染 — preinstall フックで Chrome プロファイル・Bitwarden・Steam を窃取](https://socket.dev/blog/jscrambler-cli-supply-chain-attack) — Socket が公開後 6 分で自動検知し npm に報告; Rust バイナリが Windows/macOS 両対応の永続化メカニズムを実装; CI/CD パイプラインでの自動インストールが最大の被害拡大要因; 8.21.0 以降が clean 版。*(Socket / THN / BleepingComputer)*

- **[2026-07-11]** [U-Boot ブートローダーに FIT 署名検証の 6 脆弱性 (BRLY-2026-037〜042) — 2013 年以来全バージョン影響・うち BRLY-037/038 が RCE ポテンシャル](https://binarly.io/posts/uboot-fit-signature-vulnerabilities/) — 037/038: 負値 length フィールドが `fit_image_verify_required_sigs()` でスタックバッファを溢れさせ pre-boot RCE; 039〜042: NULL 参照・無限再帰・範囲外読取による DoS; BMC リモートファームウェア更新経由で物理アクセス不要; upstream パッチ適用済みだが正式リリース v2026.10 は 10 月予定。*(Binarly / BleepingComputer / THN)*

- **[2026-07-11]** [Zimbra Classic Web Client に Stored XSS (CVE 未割当) — Google TAG が報告、国家系 APT が数億ユーザー対象に悪用中、Zimbra 10.1.19 で修正](https://www.bleepingcomputer.com/news/security/zimbra-stored-xss-google-tag/) — 攻撃者が細工メールを送信 → 受信者が Classic Web Client で開封 → Stored XSS が任意スクリプトを実行 → セッショントークン・設定・メールボックス内容を窃取; 政府機関・大企業の Zimbra ユーザーが主標的; 既に多数の政府メールシステムへの侵害を確認。*(BleepingComputer / THN / SC World)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-07-11 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-54088 | File Browser < 2.63.6 (Go, Web ファイルマネージャー) | CWE-78 / **9.3** (CVSS 4.0) | Hook Auth 設定時に `os.Expand()` がユーザー入力クレデンシャルをシェルコマンドテンプレートに無害化なく展開 → `/api/login` への未認証 POST で任意 OS コマンド実行 (pre-auth RCE) | [v2.63.6](https://github.com/filebrowser/filebrowser/releases/tag/v2.63.6) | 2026-07-10/11 公開 / CVSS 9.3 / 未認証 pre-auth RCE / PoC 公開済み |
| CVE-2026-61861 / GHSA-qvxh-prvr-85w2 | ImageMagick < 7.1.2-26 | CWE-416 / **6.3** (CVSS 4.0) | `FormatMagickCaption()` でメモリ確保失敗時に dangling pointer が解放済みメモリを参照し続ける UAF → DoS または任意コード実行 | [7.1.2-26](https://github.com/ImageMagick/ImageMagick/releases/tag/7.1.2-26) | 2026-07-11 GHSA 公開 / 広範利用画像処理ライブラリ / UAF 水平伝播候補 |
| CVE-2026-61442 | PraisonAI Platform < 0.1.9 (pip) | CWE-862 / **7.1** | projects/issues/agents の PATCH ルートが `owner`/`admin` ロールを要求せず `workspace-member` で到達可 → 一般メンバーがオーナー作成リソースを任意に改変・削除可能 | [0.1.9](https://github.com/MervinPraison/PraisonAI/releases) | 2026-07-11 公開 / AI プラットフォーム BOLA/認可欠如パターン |
| BRLY-2026-037〜042 (CVE 未採番) | U-Boot 2013.07 〜 2026.07 (全組込み機器) | CWE-121/125/476/674 / **Critical〜Medium** | FIT イメージ署名検証 (`fit_image_verify_required_sigs()`) に負値 length・NULL ptr 参照・無限再帰等 → 037/038 がスタック系バグで pre-boot RCE、039〜042 が DoS; BMC リモート更新経由で物理アクセス不要の悪用可 | upstream パッチ済み (v2026.10 正式リリース予定) | 2026-07-11 公開 / CVE 未採番 / 2013 年以来全バージョン影響 / BMC 経路でリモート悪用可 |
| Zimbra Classic Web Client XSS (CVE 未割当) | Zimbra < 10.1.19 (Classic Web Client) | CWE-79 / **Critical** | 攻撃者が細工メールを送信 → 受信者が Classic Web Client で開封 → Stored XSS が任意スクリプトを実行 → セッショントークン・設定・メールボックス内容を窃取 | [Zimbra 10.1.19](https://www.zimbra.com/downloads/) (commit 不明) | 2026-07-11 公開 / Google TAG 報告 / 国家系 APT 悪用確認 / 数億ユーザー影響 |

---

## 国内脆弱性・インシデント情報

> 直近2日間 (2026-07-11〜12) に JVN/JPCERT/CC/IPA/Piyolog で確認できた新規の国内脆弱性・インシデント公表はありませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| OpenAI / AI Weekly / Nature News (GPT-5.6 Sol Ultra CDC Conjecture) | 2026-07-11 OpenAI ブログ公開確認 ✓ |
| Adversa AI / First Recon (Agentic AI Runtime Security GA) | 2026-07-12 GA 発表確認 ✓ |
| AI Weekly / Reuters (FRB AI 委員会設立) | 2026-07-11 発表確認 ✓ |
| Socket / THN / BleepingComputer (jscrambler npm supply chain) | 2026-07-11 公開・6 分以内検出確認 ✓ |
| Binarly / BleepingComputer / THN (U-Boot BRLY-2026-037〜042) | 2026-07-11 Binarly ブログ公開確認 ✓ |
| BleepingComputer / THN / SC World (Zimbra Classic XSS) | 2026-07-11 公開・Google TAG 報告確認 ✓ |
| NVD / GitHub Advisories (CVE-2026-54088 File Browser v2.63.6) | 2026-07-10/11 公開・PoC 確認 ✓ |
| GitHub Advisories (GHSA-qvxh-prvr-85w2 / CVE-2026-61861 ImageMagick) | 2026-07-11 GHSA 公開確認 ✓ |
| GitHub Advisories (CVE-2026-61442 PraisonAI Platform 0.1.9) | 2026-07-11 公開確認 ✓ |
| jvn.jp / jpcert.or.jp / ipa.go.jp / piyolog | WebSearch 確認: 2026-07-11〜12 新規エントリなし |
| thehackernews.com / bleepingcomputer.com | 403 — WebSearch スニペットで代替 |
| nvd.nist.gov | 403 — WebSearch スニペット代替 |

### 集計サマリ

- **巡回ソース数**: 約 20
- **採用件数**: AI=3 / Security=3 / CVE=5 / 国内=0
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-07-11 より前): Balochistan Police espionage (SentinelLabs 2026-07-09) / SambaNova $1B Series F (Bloomberg 2026-07-08) / node-tar CVE-2026-59874/73/71 (元 CVE 公開 2026-07-08, THREATINT 確認) / React Server Components GHSA-fv66-9v8q-g76r (CVE-2025-55182, Dec 2025 公開) / Ubiquiti UniFi patches (July 2-8, 日付不確定)
  - 重複 (直近 7 ダイジェスト掲載済み): PraisonAI CVE-2026-61447/61445 (07-12掲載) / Ghostcommit PNG injection (07-12掲載) / Apple vs OpenAI lawsuit (07-12掲載) / Progress ShareFile threat (07-12掲載) / iCagenda CVE-2026-48939 KEV (07-12掲載) / Hono GHSA-v8w9-8mx6-g223 (07-12掲載) / JetBrains 6 CVEs (07-11掲載) / Balbooa Forms CVE-2026-56291 (07-11掲載) / WP-SHELLSTORM / MODBEACON (07-11掲載)
  - 日付不明: 0件

### 主要除外補足

- **node-tar CVE-2026-59874/59873/59871**: TheWindowsUpdate.com に /2026/07/12/ URL パターンが存在するが THREATINT 確認で元の CVE 公開日 2026-07-08 → 窓外除外
- **Balochistan Police APT espionage (SentinelLabs)**: 公開日 2026-07-09 確認 → 窓外除外
- **SambaNova $1B Series F**: Bloomberg 2026-07-08 公開 → 窓外除外
- **React Server Components GHSA-fv66-9v8q-g76r**: CVE-2025-55182 として 2025-12 公開 → 窓外除外
- **Ubiquiti UniFi patches**: FieldEffect 2026-07-02 / AHA 2026-07-08 と日付情報が矛盾 → 日付不確定のため除外

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-07-06 〜 2026-07-12) の全 CVE/GHSA/URL を除外済み。*
