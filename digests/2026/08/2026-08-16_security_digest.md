# KEDA Daily Digest — 2026-08-16 (JST)

> 採用範囲: 公開日 2026-08-14 〜 2026-08-16
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

OpenAI が GPT-5.6 Sol を Cerebras 連携で毎秒 750 トークンという超高速 API として限定プレビュー開始、Anthropic は 2028 年 Nasdaq 上場・企業価値 $965B を目指す IPO 計画をロイターが報道しており AI 産業の動向が連日続く。セキュリティ面では watchTowr が Citrix NetScaler ADC/Gateway の nsppe ヒープオーバーフロー（CVE-2026-8452）を「DoS」から「未認証 root RCE」へエスカレーションし PoC を公開、JPCERT/CC が翌 8/15 に注意喚起を発出した。Apple macOS の Screen Sharing 脆弱性（CVE-2026-65400、CVSS 9.8）はオランダ NCSC が警告を出すほど悪用が拡大し Monero マイナーの設置が確認されている。GeoTools/GeoServer の PostGIS SQLi（GHSA-mqjf-5f49-2fjh、CVSS 9.8）は 8/15 に GitHub Advisory が公開された。

---

## AI 関連ニュース

- **[2026-08-14]** [OpenAI Previews Ultrafast API Powered by Cerebras at 750 tok/s](https://openai.com/index/previewing-ultrafast/) — OpenAI が GPT-5.6 Sol を Cerebras WSE ウェハースケールエンジンと連携させた Ultrafast API を限定プレビュー公開。750 tok/s は標準 API 比 14 倍超の速度。料金・GA 時期は未発表 *(OpenAI blog / HPC Wire)*

- **[2026-08-14]** [Anthropic IPO: $965B Valuation, Nasdaq 2028 Listing — Reuters Exclusive](https://www.reuters.com/) — ロイターが Anthropic の IPO 計画を独占報道。2028 年 Q4 Nasdaq 上場、Morgan Stanley・Goldman Sachs・JPMorgan が主幹事。2028 年売上予測 $190〜200B。Claude の企業契約拡大が収益基盤 *(Reuters / wsau.com 2026-08-14)*

- **[2026-08-14]** [US Warns 35 Countries: Join China's WAICO and You're Out of Pax Silica](https://thenextweb.com/news/pax-silica-us-letter-35-countries-china-ai-coalition) — 米国務省が 35 カ国に書簡を送付し、中国主導の WAICO（世界 AI 協力機構）への参加は米国が推進する Pax Silica AI 連合からの除外を意味すると警告。技術覇権を巡る陣営分断が先鋭化 *(The Next Web / Rappler 2026-08-14)*

- **[2026-08-14]** [Apple Partners with Alibaba to Train Custom AI Model for China — First Foreign Approval](https://www.macrumors.com/2026/08/14/) — Apple が中国政府の承認を得て Alibaba と独自 AI モデルを共同訓練したと報道。外国企業として初の中国向け固有モデルで、Apple Intelligence の中国展開が近いと見られる *(MacRumors / Japan Times 2026-08-14)*

- **[続報][2026-08-14]** [DeepSeek V4 Pro Pricing: 14× Flash Rate, Flash Peak Now $1.32/M Tokens (Effective Aug 16)](https://qz.com/) — DeepSeek API が V4 Pro を V4 Flash 比 14 倍の価格帯でローンチ。Flash 自体もピーク時 $0.28/M → $1.32/M 出力トークンへ値上げ（8/16 有効）。V4 Pro の登場は 08-14 digest 既報だが価格詳細は新規情報 *(QZ / AmericanBazaarOnline 2026-08-14)*

---

## セキュリティ関連ニュース

- **[続報][2026-08-14]** [CVE-2026-65400 Apple macOS Screen Sharing: Active Exploitation — Monero Miner Deployed, NCSC Warning](https://bleepingcomputer.com/) — オランダ NCSC が Apple macOS Screen Sharing の認証前 RCE（CVE-2026-65400、CVSS 9.8）の野生悪用について緊急警告。攻撃者は root 権限を取得後に Monero マイナーを設置。パッチは 8/6 公開（macOS Tahoe 26.6.1 / Sequoia 15.7.9 / Sonoma 14.8.9）。VNC ポート TCP 5900 をインターネット開放している環境が標的。本シリーズ初報 *(BleepingComputer / Slashdot 2026-08-14)*

- **[続報][2026-08-14]** [VMware vCenter CVE-2026-59310: QUIRSO Documents 361 Victim IPs Across 47 Countries in Global APT Campaign](https://gbhackers.com/) — QUIRSO Research が 7/29 開示の VMware vCenter 認証バイパス（CVE-2026-59310）を悪用したグローバル APT キャンペーンを追跡。361 被害 IP・47 カ国を確認。攻撃者はリバース SSH トンネルと cron ジョブバックドアで持続性を確立（初期侵入は 8/3 から）。08-13 digest 掲載の「認証バイパス侵害スキャン」から実被害ステージへ進展 *(GBHackers / DarkReading / QUIRSO Medium 2026-08-14)*

- **[続報][2026-08-14]** [CVE-2026-8452 Citrix NetScaler: watchTowr Escalates from DoS to Pre-Auth Root RCE, PoC Published](https://labs.watchtowr.com/) — watchTowr がパケット処理エンジン nsppe（root 実行）のヒープオーバーフローを詳解し、Citrix が「DoS」と分類していた CVE-2026-8452 が実際には未認証リモート root RCE であることを実証。PoC を同日公開。JPCERT/CC は 8/15 に注意喚起を発出 *(watchTowr labs / CybersecurityNews / NHS England CC-4832)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-08-14 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| GHSA-mqjf-5f49-2fjh (CVE 未採番) | GeoTools ≥33.1/<33.6, ≥34.0/<34.5, 35.0; GeoServer ≥3.0.0/<3.0.1, ≥2.28.0/<2.28.5, <2.27.6 | CWE-89 / **9.8** | 未認証攻撃者が OGC フィルタの `jsonArrayContains` 関数に細工した引数を送信 → PostGIS バックエンドへの SQL 文字列を直接連結 → 任意 SQL 実行 (認証不要、ネットワーク経由) | GeoTools 35.1/34.5/33.6 / GeoServer 3.0.1/2.28.5/2.27.6 パッチ済み; GHSA 公開 **2026-08-15** | CVSS 9.8 / 未認証 / GIS インフラ広範影響 / 8/12 から probe 確認 / GitHub Advisory 公開当日 |
| CVE-2026-8452 | Citrix NetScaler ADC/Gateway 14.1 < 14.1-72.61, 13.1 < 13.1-63.18 | CWE-122 / **9.8** (watchTowr 再評価; Citrix 元スコア 8.8/DoS) | 未認証攻撃者がパケット処理エンジン nsppe に細工したリクエストを送信 → ヒープオーバーフロー (root 実行デーモン) → 任意コマンド実行 | 公式パッチ既出 (2026-07-下旬); watchTowr PoC 公開 **2026-08-14**; JPCERT/CC 注意喚起 2026-08-15 | PoC 公開当日 / 未認証 root RCE / エッジ機器 / DoS→RCE スコア再分類 |
| CVE-2026-65400 | Apple macOS Tahoe <26.6.1 / Sequoia <15.7.9 / Sonoma <14.8.9 (Screen Sharing / SRP) | CWE-287 / **9.8** | 未認証攻撃者が TCP 5900 経由で Screen Sharing SRP ハンドシェイクに細工 → 認証バイパス → VNC セッション確立 → root 相当コード実行 | macOS 26.6.1/15.7.9/14.8.9 パッチ済み (2026-08-06); 野生悪用確認 **2026-08-14** (Monero miner) | CVSS 9.8 / 野生悪用確認 / オランダ NCSC 警告 / インターネット開放 VNC 環境 |

---

## 国内脆弱性・インシデント情報

- **[2026-08-15]** JPCERT/CC が Citrix NetScaler ADC/Gateway の CVE-2026-8452（未認証 root RCE、PoC 公開済み）について緊急注意喚起を発出。パッチ未適用環境の即時アップデートと、TCP 443/80 のアクセス制限強化を推奨 *(JPCERT/CC CC-4832 相当)*

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| openai.com/index/previewing-ultrafast/ (Ultrafast API) | URL パターン確認 ✓; HPC Wire 2026-08-14 URL 確認 ✓ |
| Reuters / wsau.com (Anthropic IPO) | wsau.com/2026/08/14/ URL パターン確認 ✓ |
| thenextweb.com / rappler.com (Pax Silica 書簡) | TNW URL 確認 ✓ |
| macrumors.com/2026/08/14/ / japantimes.co.jp/2026/08/14/ (Apple China AI) | URL パターン確認 ✓ |
| qz.com / americanbazaaronline.com/2026/08/14/ (DeepSeek V4 pricing) | URL パターン確認 ✓; 続報判定 (V4 Pro 本体は 08-14 digest 既報) |
| BleepingComputer / Slashdot "08/14/2213230" (CVE-2026-65400 exploitation) | Slashdot URL パターン 2026-08-14 確認 ✓; businessstory.org/2026/08/14/ ✓ |
| GBHackers / DarkReading / QUIRSO Medium (VMware CVE-2026-59310 campaign) | gbhackers.com CVE-2026-59310 "361 victim IPs" スニペット確認 ✓ |
| labs.watchtowr.com (CVE-2026-8452 RCE escalation) | watchTowr URL "youre-back-in-the-room-..." 確認 ✓; JPCERT/CC 2026-08-15 ✓ |
| github.com/geotools/geotools/security/advisories/GHSA-mqjf-5f49-2fjh | **WebFetch 直接取得成功** ✓; Published: August 15, 2026; CVSS 9.8 確認 ✓ |
| jvn.jp / jpcert.or.jp / ipa.go.jp | CVE-2026-8452 注意喚起 2026-08-15 確認 ✓ |

### 集計サマリ

- **巡回ソース数**: 約 22
- **採用件数**: AI=5 / Security=3 / CVE=3 / 国内=1
- **除外理由内訳**:
  - 採用窓外 (公開日 <2026-08-14): GeoServer zero-day initial disclosure 2026-08-12 (GHSA 公開は 8/15 のため CVE テーブル採用); IBM+OpenAI partnership 初報 2026-08-13 (marginal)
  - 重複 (excluded_set 参照): DeepSeek V4 Pro モデル本体リリース (08-14 digest 掲載; 価格詳細のみ続報採用) / VMware vCenter CVE-2026-59309 スキャン (08-13 digest 掲載; 実被害拡大は続報採用) / CVE-2026-59310 開示自体 (08-13 掲載)
  - GHSA-5x4f-6m9q-mg75 系 IoT CVE: 08-10 以降除外継続
  - 取得失敗ソース (EGRESS_BLOCKED): thehackernews.com, bleepingcomputer.com, securityweek.com, gbhackers.com, nvd.nist.gov, cisa.gov, portswigger.net, watchtowr.com, medium.com, cerebras.ai

</details>

---

*生成: keda-digest-bot / 2026-08-16 05:04 JST*
