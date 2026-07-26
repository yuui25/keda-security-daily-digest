# KEDA Security Daily Digest — 2026-07-27

> 採用範囲: 2026-07-25〜2026-07-27 JST に公開された情報のみ掲載。過去 7 日分との重複を除外 ([続報] 表記を除く)。

---

## 本日のサマリ

Moonshot AI が Kimi K3 の完全重み (2.8兆パラメータ、MXFP4 量子化で約 1.4TB) を Hugging Face で公開し史上最大のオープンウェイトリリースとなった。UK AISI/US CAISI の共同評価では同モデルがオフェンシブサイバー操作の阻止に失敗したことが確認されており、modified MIT license での自己ホスト運用により中国データルーティングリスクを排除可能な点も注目される。脆弱性面では CVE-2026-16723 (Fastjson 1.2.68〜1.2.83) が SafeMode デフォルト無効の Spring Boot 環境で未認証 RCE を可能にするゼロデイとして Alibaba 未パッチのまま実攻撃が継続。マルウェア面では 12カ国・25言語を標的とした SourTrade マルバータイジングが Bun runtime で分割マルウェア片を組み立てハッシュベース検知を設計上回避。同時期に Steam コミュニティフォーラムの偽修正スレッドを経由した ClickFix XMRig cryptominer 常駐攻撃が確認され、ShinyHunters 流出データを悪用した大規模セクストーション詐欺メールも観測された。北朝鮮では元軍事インテリジェンス・サイバー部隊員が自国銀行をハックし暗号資産で洗浄を試みたとして逮捕される異例の事態となった。

---

## AI 関連ニュース

1. [2026-07-27] **Kimi K3 オープンウェイト公開** — Moonshot AI が 2.8 兆パラメータ Kimi K3 の完全重みを Hugging Face で公開 (00:00 UTC 7/27、MXFP4 量子化で約 1.4TB、modified MIT license)。史上最大のオープンウェイトリリース。UK AISI/US CAISI の共同安全評価でオフェンシブサイバー操作の阻止に失敗を確認。自己ホスト運用により中国データルーティングリスクの排除が可能。([TechTimes](https://www.techtimes.com/) / techi.com / Kimi Blog)

---

## セキュリティ関連ニュース

1. [2026-07-25] **SourTrade マルバータイジング** — 偽 TradingView・Solana・Luno 広告がブラウザ内で分割マルウェア片を動的に組み立て、Bun runtime 経由で Windows 実行ファイルを生成。ハッシュベース検知を設計上回避し 12カ国・25言語を標的。感染端末は暗号資産ウォレット・取引所認証情報を窃取される。([THN](https://thehackernews.com/) / Confiant Blog (初報 2026-07-23) / BackBox)

2. [2026-07-25] **ShinyHunters 流出データを悪用したセクストーション詐欺** — 過去の ShinyHunters による漏洩メールアドレスを名簿として利用した $2,000 Bitcoin 要求のセクストーション詐欺メールが大規模送信。被害者の実在パスワードを件名に含む手口で信ぴょう性を偽装。([BleepingComputer](https://www.bleepingcomputer.com/))

3. [2026-07-25] **Steam フォーラム ClickFix / XMRig 常駐攻撃** — Steam コミュニティフォーラムに「ゲームクラッシュ修正」等を装った偽スレッドを投稿し PowerShell 実行を誘導、XMRig cryptominer を `C:\Windows\Background\` 隠しディレクトリに展開しタスクスケジューラで SYSTEM 権限永続化。ゲーマーコミュニティを標的にしたソーシャルエンジニアリング。([BleepingComputer](https://www.bleepingcomputer.com/))

4. [2026-07-25] **北朝鮮、元国家ハッカーを自国銀行ハッキングで逮捕** — 元軍事インテリジェンス・サイバー部隊員が朝鮮中央銀行および外国貿易銀行をハックして暗号資産で資金洗浄を試みたとして 7/12 に逮捕・端末没収。北朝鮮内部からの国家系ハッカーによる自国金融機関攻撃という異例の事案。([CoinDesk](https://www.coindesk.com/) (2026-07-25))

---

## 新規 CVE / Advisory

| CVE/GHSA | 製品・バージョン | CWE / CVSS | バグクラス (条件→シンク→結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-16723 | Fastjson (Alibaba) 1.2.68〜1.2.83 (SafeMode デフォルト無効・Spring Boot fat-JAR 環境) | CWE-502 / **9.0** | 未認証攻撃者が任意 JSON エンドポイントに細工リクエスト送信 → SafeMode 無効・AutoType 迂回でFastjson が悪意あるクラスをデシリアライズ → Java プロセス権限で RCE; 金融・医療・小売等の Spring Boot アプリが主な影響範囲 | パッチなし (2026-07-25 時点); 緩和: SafeMode 強制有効化 または Fastjson 2.x 移行 / 発見: FearsOff Cybersecurity / 報道: THN・Imperva・ThreatBook (2026-07-25) | **実攻撃確認・パッチなし** / 中国・Java エコシステム広範利用 / AI サービスバックエンド多用 / 水平伝播候補 (Jackson/Gson 等類似デシリアライザへの注目) |

---

## 国内脆弱性・インシデント

> 直近 2 日間 (2026-07-25〜26) に JVN/JPCERT/CC/IPA/Piyolog で確認できた新規の国内脆弱性・インシデント公表はありませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| TechTimes / techi.com / Kimi Blog (Kimi K3 open weights) | 2026-07-25〜27 URL 確認 ✓ (weights 公開 00:00 UTC 7/27 / UK AISI/US CAISI 評価確認 ✓) |
| THN / Confiant Blog / BackBox (SourTrade マルバータイジング) | 2026-07-25 URL "/2026/07/25/" 確認 ✓ (Confiant 初報 2026-07-23、THN 掲載 2026-07-25) |
| BleepingComputer (ShinyHunters セクストーション) | 2026-07-25 "July 25, 2026" 確認 ✓ |
| BleepingComputer (Steam ClickFix XMRig) | 2026-07-25 "July 25, 2026" 確認 ✓ |
| CoinDesk (北朝鮮元ハッカー逮捕) | 2026-07-25 URL "/2026/07/25/" 確認 ✓ (逮捕日: 7/12) |
| THN / Imperva / ThreatBook (CVE-2026-16723 Fastjson) | 2026-07-25 URL "/2026/07/25/" 確認 ✓ (FearsOff Cybersecurity 発見、Alibaba 未パッチ確認 ✓) |
| jvn.jp / jpcert.or.jp / ipa.go.jp / piyolog | WebSearch 確認: 2026-07-25〜26 新規エントリなし |
| thehackernews.com / bleepingcomputer.com | 403 — WebSearch スニペットで代替 |
| nvd.nist.gov / cisa.gov | 403 — WebSearch スニペット代替 |
| helpnetsecurity.com / guardianmssp.com | 403 — WebSearch スニペット代替 |

### 集計サマリ

- **巡回ソース数**: 約 20
- **採用件数**: AI=1 / Security=4 / CVE=1 / 国内=0
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-07-25 より前): Confiant SourTrade 初報 (2026-07-23) → THN・BackBox の 2026-07-25 掲載日基準で採用
  - 重複 (直近 7 ダイジェスト掲載済み・excluded_set 参照): Kimi K3 Redis ゼロデイ (07-26掲載) / XBOW Bing CVE-2026-32194/32191 (07-26掲載) / Aikido NodeBB (07-26掲載) / ChatGPT 4回目障害 (07-26掲載) / GitLab Jupyter Heap BOF RCE PoC (07-26掲載) / OnTrac PII 流出 (07-26掲載) / Qilin Stryker (07-26掲載) / EMEA ヘルスケアランサムウェア (07-26掲載) / Logto JVNVU#99418634 (07-26掲載) / FakeAgent SectopRAT (07-25掲載) / AgentForger ChatGPT (07-25掲載) / SharedRoot CVE-2026-46331 (07-25掲載) / Certighost CVE-2026-54121 (07-25掲載) / Clop Windchill CVE-2026-12569 (07-25掲載) / Chick-fil-A breach (07-25掲載) / MS365 outage (07-25掲載) / Ricoh MFP JVNDB (07-25掲載) / JadeProx TriBack (07-24掲載) / OpenAI Presence (07-24掲載) / DeepSeek V4 GA (07-24掲載) / SharePoint CVE-2026-50522 KEV (07-24掲載) / Qilin 1,358件 (07-23掲載) / Oracle July CPU (07-23掲載) / JADEPUFFER ENCFORGE (07-22掲載) / Pillar Sandbox Escapes (07-22掲載) / SleeperGem (07-21掲載) / ServiceNow CVE-2026-6875 (07-21掲載) / nginx CVE-2026-42533 (07-21掲載) / 7-Zip CVE-2026-14266 (07-21掲載) / Claude Fable 5 (07-20掲載) / VMware Avi CVE-2026-47865〜71 (07-20掲載)

### 主要除外補足

- **Kimi K3 open weights**: Kimi K3 の API サービス提供 (WAIC 2026後) は 07-22 掲載済み。今回の「完全重み Hugging Face 公開 (00:00 UTC 7/27)」は独立した新規イベントとして採用。UK AISI/US CAISI 評価結果も同時公表
- **SourTrade**: Confiant 初報は 2026-07-23 (採用窓外) だが THN・BackBox の主要掲載が 2026-07-25 に集中確認 → VMware Avi / 7-Zip と同様のニュースサイト掲載日基準で採用
- **CVE-2026-16723 (Fastjson)**: NVD 未登録 (2026-07-25 時点) だが FearsOff Cybersecurity の発見報告・Imperva/ThreatBook の実攻撃観測レポートが THN に 2026-07-25 掲載確認 → パッチなし実攻撃として最優先採用

</details>

---

*生成: keda-digest-bot / 2026-07-27 05:04 JST*
