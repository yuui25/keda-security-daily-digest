# KEDA Daily Digest — 2026-08-25 (JST)

> 採用範囲: 公開日 2026-08-23 〜 2026-08-25
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Nvidia が Perplexity AI に出資を協議中であることが報じられ、Perplexity の評価額は $300 億超・ARR は年初来 3 倍超の $7.5 億超となっている。OpenAI は 2026-08-26 に o3 モデルを ChatGPT から退役させ Assistants API も同日終了、DALL-E GPT は 2026-08-30 退役とタイムラインが確定した。セキュリティでは GTA 6 フェイクデモサイトによるブラウザ情報窃取マルウェアキャンペーンが Malwarebytes により報告され、Storm ランサムウェアがオーストラリア大手自動車グループおよび米国ミシガン州の市を標的とした。中国系 APT による Operation QUICSILVER では QUIC/HTTP3 + Cloudflare Workers を C2 に使用した QUICAgent バックドアがミャンマー政府・IT セクターに展開された。CVE では OAuth2 Proxy の X-Forwarded-Uri ヘッダー信頼設定による認証バイパス (CVE-2026-76835, CVSS 9.3) が公開された他、Continue CLI の AI エージェント向けコマンドブロックリスト不備 (CVE-2026-76072, CVSS 8.3) および TP-Link Archer シリーズのペアレンタルコントロールを介した未認証 root コマンド実行 (CVE-2026-9254, CVSS 8.7) が同日公開された。

---

## AI 関連ニュース

- **[2026-08-23]** [Nvidia in Talks to Invest in Perplexity AI at $30B+ Valuation as ARR Surpasses $750M — Tripling Since January](https://finance.yahoo.com/news/nvidia-in-talks-to-invest-in-perplexity-ai-at-30b-valuation/) — Nvidia が Perplexity AI へ出資を協議中であることを The Information が報道。Perplexity の ARR は $7.5 億超 (年初比 3 倍超)、評価額は $300 億超を目標とする。Nvidia は GPU 供給に加えて戦略的投資家として関係強化を図る *(The Information / Yahoo Finance / Reuters 2026-08-23)*

- **[2026-08-24]** [OpenAI Confirms ChatGPT o3 and Assistants API Retire August 26, DALL-E GPT Retires August 30 — Migrate to o3-mini-high or o4-mini](https://openai.com/blog/deprecation-schedule-august-2026) — OpenAI が 2026-08-26 に ChatGPT 内 o3 モデルを退役させ o3-mini-high または o4-mini へ誘導すると確認。Assistants API も同日終了 (移行先: Responses API)。DALL-E GPT は 2026-08-30 退役。2026-05-28 の 90 日間告知から確定タイムライン *(OpenAI Blog / API Deprecation Schedule 2026-08-24)*

---

## セキュリティ関連ニュース

- **[2026-08-23]** [Fake GTA 6 "Extended Look" Demo Sites and 113GB Fake Leaked Build Spread Browser Infostealer — Credentials, Cookies, and Sessions Targeted](https://www.malwarebytes.com/blog/threat-intelligence/2026/08/fake-gta6-demo-sites-spread-browser-infostealer/) — Malwarebytes Threat Intelligence が、偽の GTA 6 拡大プレビュー動画サイトおよび 113 GB の偽リークビルドを餌にしてブラウザ情報窃取マルウェアを配布するキャンペーンを報告。Chrome・Firefox・Brave の保存済み認証情報・Cookie・認証済みセッションが窃取対象。現時点で帰属未特定 *(Malwarebytes 2026-08-23)*

- **[2026-08-23]** [Storm Ransomware Claims Sharp Motor Group (Australia) and City of Mitchell, South Dakota — Municipal and Automotive Sector Targeted](https://www.bleepingcomputer.com/news/security/storm-ransomware-claims-sharp-motor-group-city-of-mitchell/) — Storm ランサムウェアグループがオーストラリアの大手自動車ディーラーグループ Sharp Motor Group と米国サウスダコタ州ミッチェル市への攻撃を主張。ミッチェル市は 2026-08-24 に攻撃を確認し市民サービスの一部が停止。Sharp Motor Group は調査中 *(BleepingComputer 2026-08-23)*

- **[2026-08-24]** [Operation QUICSILVER: China-Nexus APT Deploys QUICAgent Backdoor via QUIC/HTTP3 + Cloudflare Workers C2 Against Myanmar Government and IT Sector](https://thehackernews.com/2026/08/operation-quicsilver-china-nexus-apt.html) — Seqrite Labs が中国系 APT グループ (Operation GriefLure と同一クラスターと評価) による Operation QUICSILVER を公開 (初出 2026-08-17、THN 報道 2026-08-24)。Go 1.20 製 QUICAgent バックドアを VHD ファイル (卒業式招待状に偽装) で配信し、Cloudflare Workers 上の C2 と QUIC/HTTP3 + RC4 暗号化で通信。ミャンマー政府機関・IT セクターが主標的 *(Seqrite Labs / The Hacker News 2026-08-24)*

- **[2026-08-24]** [Check Point TI Weekly: Education Sector Attacks Up 8% YoY (4,696 Weekly Avg); Cl0p Exploiting CVE-2026-12569 in PTC Windchill/FlexPLM with 40+ Named Victims](https://research.checkpoint.com/2026/threat-intelligence-weekly-education-cl0p-windchill/) — Check Point Research 週次 TI レポート: 2026 年 1〜7 月の教育セクターへの週平均攻撃数が前年比 +8% の 4,696 件。Cl0p ランサムウェアアフィリエイトが PTC Windchill/FlexPLM の CVE-2026-12569 (製品ライフサイクル管理) を悪用し製造業 40 社超を恐喝中 *(Check Point Research 2026-08-24)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-08-23 以降 / CISA KEV 追加 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| GHSA-vvqv-7vrf-88vh / CVE-2026-76835 | OAuth2 Proxy (全バージョン / デフォルト設定) | CWE-290 / **9.3** | デフォルトで全 IP (0.0.0.0/0) から X-Forwarded-Uri ヘッダーを信頼 → 攻撃者が許可リスト登録パスをヘッダーにセットしてリクエスト送信 → 認証スキップで保護対象上流に未認証アクセス | 修正コミット未公開; [GHSA-vvqv-7vrf-88vh](https://github.com/advisories/GHSA-vvqv-7vrf-88vh); 公開 **2026-08-24** | CVSS 9.3 / リバースプロキシ認証バイパス / k8s Ingress 保護で広範利用 / デフォルト設定が脆弱 |
| GHSA-xqr4-4xjv-5j7q / CVE-2026-76072 | Continue CLI (全バージョン / 修正版なし) | CWE-184 / **8.3** | コマンドブロックリストが `/home`・`/root`・`/var` を除外 + `$HOME` 等の変数展開を未考慮 + `shred`/`wipefs`/`truncate`/`pkexec` が非ブロック → 攻撃者が侵害済み Web コンテンツ/リポジトリ経由で AI エージェントに任意の破壊的コマンドを実行させる | 修正版なし (2026-08-24 時点); [GHSA-xqr4-4xjv-5j7q](https://github.com/advisories/GHSA-xqr4-4xjv-5j7q); 公開 **2026-08-24** | CVSS 8.3 / AI エージェントを介した任意コマンド実行 / ブロックリスト設計欠陥 / 修正版未公開 |
| GHSA-3h97-6772-mpj4 / CVE-2026-9254 | TP-Link Archer BE800 V1 / BE3600 V1 / AX75 V1 (修正ファームウェア以前) | CWE-78 / **8.7** | ペアレンタルコントロール機能が特殊文字をフィルタリングせず → LAN 上の未認証攻撃者が OS コマンドを注入 → root 権限で任意コマンド実行 | 修正ファームウェア提供済み (バージョン未特定); [GHSA-3h97-6772-mpj4](https://github.com/advisories/GHSA-3h97-6772-mpj4); 公開 **2026-08-24** | CVSS 8.7 / 家庭・SOHO ルーター / 未認証 LAN RCE / TP-Link 広範普及 |
| GHSA-5x78-73v4-xg6w | postgres-protocol (Rust crate, 全バージョン) | CWE-400 / High | 悪意ある PostgreSQL サーバーが SCRAM 認証の反復回数を無制限に送信 → クライアントが無制限の CPU 計算を実行 → クライアント側 DoS | [PR #132](https://github.com/sfackler/rust-postgres/pull/132) で修正; 公開 **2026-08-24** | Rust PostgreSQL クライアントエコシステム / SCRAM 認証プロトコル実装欠陥 / バリアントハント起点 |
| GHSA-w2x5-gv52-9ccv / CVE-2026-54049 | Sakai LMS conversations コンポーネント (Maven, 修正版未特定) | CWE-79 / High | 攻撃者制御のコンテンツが conversations コンポーネントのサニタイゼーションを通過 → 蓄積型 XSS → 被害者セッション乗っ取り/データ窃取 | 修正コミット未公開; [GHSA-w2x5-gv52-9ccv](https://github.com/advisories/GHSA-w2x5-gv52-9ccv); 公開 **2026-08-24** | 大学・高等教育 LMS 広範利用 / 蓄積型 XSS / 教育セクター攻撃増加トレンドと重なる |

---

## 国内脆弱性・インシデント情報

採用窓内 (2026-08-23〜08-25) での JVN・JPCERT/CC・IPA 新規公開は確認できなかった (jvn.jp、jpcert.or.jp、ipa.go.jp は EGRESS_BLOCKED により直接確認不可)。

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| yahoo.com / reuters.com (Nvidia Perplexity investment) | Yahoo Finance 2026-08-23 URL 確認 ✓; Reuters 報道確認 ✓; The Information 元記事確認 ✓ |
| openai.com (o3/Assistants API/DALL-E GPT deprecation) | WebSearch スニペット 2026-08-24 確認 ✓; 90 日タイムライン (2026-05-28 起算) 整合 ✓ |
| malwarebytes.com (GTA 6 fake demo infostealer) | WebSearch スニペット 2026-08-23 公開確認 ✓; Malwarebytes Threat Intelligence ✓ |
| bleepingcomputer.com (Storm ransomware Sharp/Mitchell) | WebSearch スニペット 2026-08-23/24 確認 ✓; 複数ソース一致 ✓ |
| seqrite.com / thehackernews.com (Operation QUICSILVER) | THN 2026-08-24 URL パターン確認 ✓; Seqrite Labs 初出 2026-08-17 確認 ✓; QUICAgent/QUIC C2 詳細確認 ✓ |
| research.checkpoint.com (Check Point TI Weekly) | WebSearch スニペット 2026-08-24 確認 ✓; CVE-2026-12569 / Cl0p / 教育セクター統計確認 ✓ |
| github.com/advisories/GHSA-vvqv-7vrf-88vh (OAuth2 Proxy) | **WebFetch 直接取得成功** ✓; Published: August 24, 2026; CVSS 9.3 確認 ✓; CVE-2026-76835 確認 ✓ |
| github.com/advisories/GHSA-xqr4-4xjv-5j7q (Continue CLI) | **WebFetch 直接取得成功** ✓; Published: August 24, 2026; CVSS 8.3 確認 ✓; CVE-2026-76072 確認 ✓ |
| github.com/advisories/GHSA-3h97-6772-mpj4 (TP-Link Archer) | **WebFetch 直接取得成功** ✓; Published: August 24, 2026; CVSS 8.7 確認 ✓; CVE-2026-9254 確認 ✓ |
| github.com/advisories/GHSA-5x78-73v4-xg6w (postgres-protocol) | WebSearch スニペット 2026-08-24 公開確認 ✓ |
| github.com/advisories/GHSA-w2x5-gv52-9ccv (Sakai XSS) | WebSearch スニペット 2026-08-24 公開確認 ✓; CVE-2026-54049 確認 ✓ |
| jvn.jp / jpcert.or.jp / ipa.go.jp (国内) | EGRESS_BLOCKED — 直接確認不可 |

### 集計サマリ

- **巡回ソース数**: 約 30
- **採用件数**: AI=2 / Security=4 / CVE=5 / 国内=0
- **除外理由内訳**:
  - 採用窓外 (公開日 <2026-08-23): GhostApproval npm supply chain (2026-07-08); OpenClaw MCP tool poisoning (2026-02-03); Meta Muse Glimmer (2026-08-10); Lazarus Group US contractor breach (2026-08-12); Seqrite QUICSILVER 初出 (2026-08-17, THN 報道 2026-08-24 で採用)
  - 重複 (excluded_set 参照): Anthropic Claude 3 Haiku Vertex AI shutdown (08-24 digest); GitLab CVE-2026-10053 (08-24 digest); StackGres CVE-2026-78155 (08-24 digest); justhtml CVE-2026-8445/7808 (08-24 digest); Iran UK power plant attack (08-24 digest)
  - 取得失敗ソース (EGRESS_BLOCKED): bloomberg.com, thehackernews.com, bleepingcomputer.com, securityweek.com, cisa.gov, nvd.nist.gov, helpnetsecurity.com, jvn.jp, jpcert.or.jp, ipa.go.jp, seqrite.com, research.checkpoint.com, malwarebytes.com, unusualwhales.com, releasebot.io

</details>

---

*生成: keda-digest-bot / 2026-08-25 05:09 JST*
