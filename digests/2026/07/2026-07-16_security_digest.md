# KEDA Daily Digest — 2026-07-16 (JST)

> 採用範囲: 公開日 2026-07-14 〜 2026-07-16 (JST)
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

WAIC 2026 (7/17〜20・上海) が明日開幕予定の中、Google DeepMind CEO Demis Hassabis が FINRA 型 AI 規制機関の設置を提唱し、SF での AI 開発停止デモと合わせてガバナンス議論が一段と沸騰。セキュリティ面では SonicWall SMA1000 の CVSS 10.0 ゼロデイ (CVE-2026-15409) が CISA KEV に追加されて連邦機関に 7/17 期限が課せられ、ESET が 10 年以上有効だった UEFI Secure Boot バイパス shim 11 件を公開した。Microsoft Patch Tuesday の追加 CVE として VMSwitch UAF (CVE-2026-57092, CVSS 9.9)・SharePoint RCE ペア (CVE-2026-50522/58644, CVSS 9.8)・DHCP Server BOF (CVE-2026-50518, CVSS 9.8) が注目され、ws (Node.js WebSocket) の CVSS 9.6 DoS (CVE-2026-48779) も 7/15 に新規公開された。

---

## AI 関連ニュース

- **[2026-07-15]** [Anthropic が Claude for Teachers を発表 — 米国 K-12 教師向け無償プレミアムアクセスを 2027-06 まで提供](https://www.anthropic.com/news/claude-for-teachers) — 検証済み教師が Claude Pro 相当の機能・50 州カリキュラム対応 Teaching Skills ライブラリ・教育標準に沿った教材生成を 1 年間無償で利用可能; 2027-06-30 までに登録した教師が対象 *(Anthropic / TechTimes)*

- **[2026-07-14]** [Google DeepMind CEO Demis Hassabis が FINRA 型 AI 規制機関の設置を提唱 — フロンティア AI の公開 30 日前から独立機関がサイバー・バイオ・欺瞞能力を評価](https://www.cnbc.com/2026/07/14/google-deepmind-demis-hassabis-us-led-ai-standards-body.html) — 米主導の官民パートナーシップで技術専門家が独立評価を実施; 当初は任意提出・制度確立後は強制とする段階的設計; 年内稼働を目標に Trump 政権・他 AI ラボ・欧州当局と協議済みと表明 *(CNBC / Axios)*

- **[2026-07-14]** [AI 開発停止デモが SF で約 200 人規模で実施 — Stop the AI Race が OpenAI・Anthropic・Google DeepMind 前でデモ行進](https://cryptobriefing.com/protesters-demand-openai-anthropic-deepmind-halt-ai/) — AI 安全性・雇用置換・環境負荷 (データセンターの電力・水消費) を主要訴求点として開発の即時停止を要求; 7/14 に OpenAI San Francisco 本社前で集会後、Anthropic・Google DeepMind オフィスへ行進 *(CryptoBriefing / KuCoin)*

- **[2026-07-14]** [Huawei が WAIC 2026 (7/17〜・上海) で Atlas 950 超ノード (Ascend NPU × 8,192 枚) を世界初公開予定 — 中国国内 AI インフラ最大規模のデプロイ](https://www.digitimes.com/news/a20260714VL214/huawei-ascend-atlas-infrastructure-display.html) — 大規模モデル学習・推論最適化の Ascend SuperPoD として展示; Baidu は「チップ・クラウド・モデル・エージェント」フルスタック AI 製品マトリクスを同時公開予定; ZTE は世界初の AI Agent スマートフォンを発表 *(Digitimes / SCMP)*

- **[2026-07-15]** [Claude Fable 5 の無償ウィンドウが 7/19 で最終終了 (5 週間で 3 度目の延期) — GPT-5.6 Sol がベンチマーク格差縮小、Grok 4.5 は $2.49/タスクで価格攻勢](https://www.techtimes.com/articles/320528/20260715/claude-fable-5-free-window-ends-sunday-gpt-56-sol-closes-benchmark-gap.htm) — 7/19 23:59 PT 以降は $10/M 入力トークン・$50/M 出力トークンの有料制に移行; 7/19 終了後の Claude Code 週次レート制限も平常水準に戻る予定; GPT-5.6 Sol の追い上げと Grok 4.5 の低価格戦略でアンソロピックへの価格的・品質的プレッシャーが強まる *(TechTimes)*

- **[2026-07-15]** [AI 主導のバグハンティングが 2026-07 Patch Tuesday 史上最多 622 CVE を牽引 — Help Net Security が AI ファジング・コード解析の加速と月例更新規模の相関を分析](https://www.helpnetsecurity.com/2026/07/15/microsoft-patch-tuesday-sharepoint-cve-2026-56164/) — 2026 年の CVE 公開数は年換算で 66,000 件超 (前年比 +30%); AI ツールが研究者と攻撃者双方の脆弱性発見サイクルを短縮し、Microsoft 社内でも Copilot Autofix が脆弱コードパターンを自動検出; 2027 年には 90,000 件超を予測 *(Help Net Security)*

---

## セキュリティ関連ニュース

- **[2026-07-14]** [SonicWall SMA1000 ゼロデイ 2 件 (CVE-2026-15409/15410) が野生悪用確認、CISA KEV に追加 — 連邦機関は 7/17 期限までに Hotfix 12.4.3-03453 または 12.5.0-02835 へ更新必須](https://www.helpnetsecurity.com/2026/07/14/sonicwall-sma-attacks-via-cve-2026-15409-cve-2026-15410/) — CVE-2026-15409 (CVSS 10.0/SSRF) は未認証でアプライアンスを任意ホストへのリクエスト発行装置として悪用可能; CVE-2026-15410 (CVSS 7.2) は認証後 AMC でOS コマンド実行; 政府・金融機関の VPN エッジデバイスが標的 *(Help Net Security / SecurityWeek / BleepingComputer)*

- **[2026-07-14/15]** [ESET が Microsoft 署名済み UEFI shim 11 件の Secure Boot バイパスを公開 (CVE-2026-8863 / CVE-2026-10797) — 10 年超有効だったバグクラス、June 2026 KB で失効処置済み](https://www.welivesecurity.com/en/eset-research/forgotten-uefi-shims-undermining-secure-boot/) — shim v0.9 以下の旧版を攻撃者が BYOVD 的に持ち込み、Microsoft CA 2011 を信頼する全 UEFI マシンの起動前フェーズで任意コード実行・UEFI Bootkit (Bootkitty/BlackLotus 等) の展開が可能; OS 前に実行するため EDR 検知を原理的に回避; February 2026 に CERT/CC へ報告済み・June 2026 KB で失効 *(WeLiveSecurity / THN / Help Net Security)*

- **[2026-07-14]** [D1R ランサムウェアグループが Synopsys・Bosch・ARM の侵害を主張、Synopsys は全否定 — 証拠スクリーンショットは公開マニュアルの流用と疑われる](https://www.securityweek.com/synopsys-finds-no-evidence-of-data-breach-following-bosch-hack-claims/) — D1R がダークウェブリークサイトに 3 社を掲載; Synopsys は「40,000 件 DB 窃取」主張を調査し証拠なしと否定・脅威アクターからの接触もなし; Bosch エンジニアリングデータの「証拠」は公開ユーザーマニュアルと判明; EDA/IP 設計大手・防衛産業サプライチェーンへの恐喝戦術として注目 *(SecurityWeek / DataBreaches.net / Cybernews)*

- **[2026-07-14]** [KU Leuven が 85 暗号資産ウォレット拡張機能 (合計 3,500 万 DL 超) のプライバシーリスクを公開 — 2,300 万ユーザーの複数アドレスが実名と紐付け可能な構造的欠陥](https://thehackernews.com/2026/07/study-of-85-crypto-wallet-extensions.html) — ウォレットがブロックチェーンサーバーと交信する際の設計パターンにより、別々のアドレスを持つ同一ユーザーを横断追跡・実名特定が可能; 脆弱性ではなく実装設計の構造問題のため即時修正困難; 研究論文を PETS 2026 (カルガリー、7 月末) で発表予定 *(THN / KU Leuven / Coinpedia)*

- **[2026-07-15]** [Cisco が ISE・RoomOS 向けセキュリティアドバイザリを公開 — Cisco ISE に RCE を含む複数の脆弱性、RoomOS に情報漏洩の脆弱性](https://www.cisco.com/c/en/us/support/docs/csa/cisco-sa-notice-ILh3ZrP5.html) — Cisco PSIRT が 7/15 公開の Advance Notification 通り Identity Services Engine および RoomOS の脆弱性情報とパッチを同日公開; ISE は認証済み管理者が root 権限で OS コマンド実行可能な RCE 脆弱性を含む; 影響バージョン・修正版は各 PSIRT アドバイザリを参照 *(Cisco PSIRT)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-07-14 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-57092 | Windows Hyper-V VMSwitch (全 in-support 版) | CWE-416 / **9.9** | 低権限ゲスト VM が特細工ネットワークリクエストを送信 → ホスト VMSwitch が解放済みメモリを参照 (UAF) → ゲストからホストへの完全 EoP | [MSRC 2026-07-14](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-57092) | CVSS 9.9 / Patch Tuesday 2026-07 最高深刻度 / Hyper-V 環境は即時適用推奨 |
| CVE-2026-50522 | Microsoft SharePoint Server 2016/2019/SE | CWE-502 / **9.8** | 未認証攻撃者がネットワーク経由で細工 .NET オブジェクトをデシリアライズさせる → 任意コード実行 (pre-auth RCE) | [MSRC 2026-07-14](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-50522) | **Pwn2Own Berlin で実証済み** / 「Exploitation More Likely」 / SharePoint 広範稼働 |
| CVE-2026-58644 | Microsoft SharePoint Server 2016/2019/SE | CWE-502 / **9.8** | CVE-2026-50522 のペア CVE: 同一デシリアライズ欠陥コードパスを別経路で到達 → 未認証 RCE (独立した同仕様実装への水平伝播候補) | [MSRC 2026-07-14](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-58644) | 「Exploitation More Likely」 / ペア CVE でバリアント探索容易 |
| CVE-2026-50518 | Windows DHCP Server (全 in-support 版) | CWE-122 / **9.8** | 未認証攻撃者が細工ドメイン名データを送信 → DHCP Server がサイズ検証なしにヒープを破壊 (BOF) → ネットワーク越しの任意コード実行 | [MSRC 2026-07-14](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-50518) | 「Exploitation More Likely」/ 未認証 / Windows Server 全版 / CVE-2026-50370・CVE-2026-54128 も同 DHCP コンポーネント影響 |
| CVE-2026-15409 | SonicWall SMA1000 6210/7210/8200v (≤12.4.3/≤12.5.0) | CWE-918 / **10.0** | 未認証攻撃者が WorkPlace インターフェイスに POST → アプライアンスが攻撃者指定の任意ホストへリクエスト発行 (SSRF) → 内部管理サービスへの到達・情報収集 | [Hotfix 12.4.3-03453](https://www.sonicwall.com/support/notices/product-notice-sma-1000-series-affected-by-multiple-vulnerabilities/kA1VN000001nv6D0AQ) | **野生悪用確認** / **CISA KEV 追加 (2026-07-14)** / CVSS 10.0 / 連邦機関 7/17 期限 |
| CVE-2026-15410 | SonicWall SMA1000 6210/7210/8200v (≤12.4.3/≤12.5.0) | CWE-94 / **7.2** | 管理者コンソール (AMC) で認証後 POST → コードインジェクションで任意 OS コマンドを administrator 権限で実行 | [Hotfix 12.4.3-03453](https://www.sonicwall.com/support/notices/product-notice-sma-1000-series-affected-by-multiple-vulnerabilities/kA1VN000001nv6D0AQ) | **野生悪用確認** / **CISA KEV 追加 (2026-07-14)** / CVE-2026-15409 と連鎖エクスプロイト可能 |
| CVE-2026-48779 / GHSA-96hv-2xvq-fx4p | ws (Node.js WebSocket) v1.1.0〜5.2.4 / v6.0.0〜6.2.3 / v7.0.0〜7.5.10 / v8.0.0〜8.21.0 | CWE-400 / **9.6** | 攻撃者が FIN=0 の極小断片を大量連続送信 → 受信側が構造体ラッパーを際限なく heap 確保しドキュメント上の maxPayload 制限が機能せず → OOM でプロセス強制終了 (DoS) | [ws v8.21.0](https://github.com/websockets/ws/security/advisories/GHSA-96hv-2xvq-fx4p) | 2026-07-15 公開 / 週 5000 万 DL の広範 Node.js エコシステム依存 / フレームワーク横断で同類 DoS パターン水平伝播候補 |
| CVE-2026-8863 / CVE-2026-10797 | UEFI shim v0.9 以下 (Microsoft CA 2011 を信頼する全 UEFI ベースシステム) | CWE-345 / **7.8** | 管理者権限を持つ攻撃者が旧版 shim を BYOVD 的にターゲットへコピー → OS 起動前の shim 実行フェーズで任意コード/UEFI Bootkit を展開 → EDR 前の完全制御 (Bootkitty・BlackLotus 等への踏み台) | [June 2026 KB5101650 (失効リスト更新)](https://www.welivesecurity.com/en/eset-research/forgotten-uefi-shims-undermining-secure-boot/) | ESET 2026-07-14 開示 / 10 年超の長期見落とし / EDR 回避可能 / BYOVD 水平伝播候補 / June KB 未適用環境は要確認 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|---|---|---|---|---|
| 2026-07-14 | JPCERT/CC at260020 | 2026 年 7 月 Microsoft 月例セキュリティ更新プログラムに関する注意喚起を公開 — CVE-2026-56155 (ADFS EoP) / CVE-2026-56164 (SharePoint EoP) の野生悪用を明示警告 | Critical / 野生悪用 2 件含む | [at260020](https://www.jpcert.or.jp/at/2026/at260020.html) |
| 2026-07-15 | IPA セキュリティアラート | Microsoft 製品の脆弱性対策について (2026 年 7 月) — 国内企業向けに July Patch Tuesday 622 CVE の即時適用を呼びかけ | Critical 57 件含む | [IPA 0715-ms](https://www.ipa.go.jp/security/security-alert/2026/0715-ms.html) |

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| Help Net Security / SecurityWeek / BleepingComputer (SonicWall SMA1000 CVE-2026-15409/15410) | 2026-07-14 Help Net Security URL "2026/07/14" 確認 ✓ / Secarma "15-07-2026" 確認 ✓ / CISA KEV 追加日 2026-07-14 確認 ✓ |
| WeLiveSecurity / THN / LatestHackingNews (ESET UEFI shim CVE-2026-8863/10797) | Help Net Security "2026/07/14" URL 確認 ✓ / LatestHackingNews "2026/07/15" URL 確認 ✓ |
| SecurityWeek / DataBreaches.net (D1R Synopsys/Bosch/ARM) | DataBreaches.net "2026/07/14" URL 確認 ✓ |
| THN / KU Leuven (crypto wallet 85 extensions privacy study) | xloggs.com "2026/07/14 08:00 PDT" 記録確認 ✓ / arXiv 2607.06141 公開確認 ✓ |
| Cisco PSIRT (ISE / RoomOS July 15 advisories) | cisco-sa-notice-ILh3ZrP5 "July 15, 2026" 公開確認 ✓ |
| Anthropic / TechTimes (Claude for Teachers) | TechTimes URL "20260715" 確認 ✓ / Anthropic 公式 /news/claude-for-teachers 確認 ✓ |
| CNBC / Axios (Demis Hassabis FINRA 型 AI 規制機関) | CNBC "July 14" / Axios "2026/07/14" URL 確認 ✓ |
| CryptoBriefing / KuCoin (AI 開発停止デモ SF) | CryptoBriefing "July 14, 2026" 確認 ✓ |
| Digitimes / SCMP (Huawei Atlas 950 WAIC) | Digitimes URL "a20260714VL214" = 2026-07-14 確認 ✓ |
| TechTimes (Fable 5 free window ending / GPT-5.6 Sol) | TechTimes URL "20260715" 確認 ✓ |
| Help Net Security (AI bug hunting Patch Tuesday analysis) | URL "2026/07/15" 確認 ✓ |
| MSRC (CVE-2026-57092/50522/58644/50518) | ZDI 2026-07-14 Security Update Review で詳細確認 ✓ |
| GitHub Advisories / NVD (CVE-2026-48779 ws) | GHSA-96hv-2xvq-fx4p "published July 15, 2026" 確認 ✓ |
| jpcert.or.jp / ipa.go.jp | at260020 (July 14) / 0715-ms.html (July 15) 存在確認 ✓ |
| nvd.nist.gov | 403 — WebSearch スニペット代替 |
| thehackernews.com / bleepingcomputer.com | 403 — WebSearch スニペットで代替 |
| openai.com / meta.ai / google deepmind blog | July 14-16 窓内の新規一次発表なし (GPT-Live-1 は July 8 公開・窓外) |
| OAuth Client ID Spoofing (Proofpoint) | Help Net Security URL "2026/07/13" → 採用窓外で除外 |
| CISA KEV 直近確認 | SonicWall CVE-2026-15409/15410 + MSRC 2 件 (CVE-2026-56155/56164) が 2026-07-14 追加確認 ✓ |

### 集計サマリ

- **巡回ソース数**: 約 30
- **採用件数**: AI=6 / Security=5 / CVE=8 / 国内=2
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-07-14 より前): AI Safety Index FLI Summer 2026 (公開 2026-07-01、Time/Axios 2026-07-07) / OpenAI GPT-Live-1 (TechCrunch 2026-07-08) / Claude Reflect dashboard (Anthropic 2026-07-09 / TechCrunch 2026-07-09) / South Korea $576B AI chip plan (Al Jazeera 2026-06-29) / Anthropic IPO S-1 confidential filing (2026-06-01) / Karpathy Anthropic (TechCrunch 2026-05-19) / OAuth Client ID Spoofing Proofpoint (Help Net Security 2026-07-13) / Cursor IDE DuneSlide CVE-2026-50548/49 (Cato Networks 2026-07-01 / CVE June 2026) / Meta Business Agent (meta.com 2026-06-03 GA)
  - 重複 (直近 7 ダイジェスト掲載済み): CVE-2026-56155/56164/50661 (07-15掲載) / CVE-2026-44747/27690 SAP (07-15掲載) / CVE-2026-60121/61498 VITEC (07-15掲載) / CVE-2026-14934 Google Cloud (07-15掲載) / JVNVU#94203999 GNU Wget (07-15掲載) / CrashStealer (07-15掲載) / ClaudeBleed (07-15掲載) / TSMC Q2 (07-15掲載) / UK CTP (07-14掲載) / Nightmare-Eclipse (07-14掲載) / DIRAC CVE-2026-61667/45579 (07-14掲載) / Gemini 3.5 Pro 再構築 (07-14掲載) / AI CVE surge 66K (07-14掲載) / HHS ChatGPT (07-14掲載) / jscrambler npm (07-13掲載) / U-Boot BRLY-2026-037〜042 (07-13掲載) / Zimbra XSS (07-13掲載) / File Browser CVE-2026-54088 (07-13掲載) / ImageMagick CVE-2026-61861 (07-13掲載) / GPT-5.6 Sol CDC (07-13掲載) / WAIC 習近平基調講演 (07-14掲載)
  - 日付不明/取得失敗: Schneier Crypto-Gram July 15 (403) / Cisco 7/15 advisories の個別 CVE 番号・CVSS (PSIRT ページ 403)

### 主要採用補足

- **CVE-2026-57092/50522/58644/50518**: 07-15 digest は Patch Tuesday 3 つのゼロデイ (CVE-2026-56155/56164/50661) のみ採用。これら 4 CVE は「Exploitation More Likely」評価で equally 重要だが重複なし → 今回採用
- **CVE-2026-15409/15410 (SonicWall)**: 07-15 digest で「日付取得不能」として除外したが、今回 Help Net Security "2026/07/14" URL・CISA KEV 追加日 2026-07-14 を確認し採用
- **CVE-2026-48779 (ws)**: NVD / GHSA "published July 15, 2026" を確認後採用
- **JPCERT at260020 / IPA 0715-ms**: 07-15 digest の国内セクションは JVNVU#94203999 (GNU Wget) のみ。Microsoft Patch Tuesday 関連の JPCERT/IPA アラートは別個として採用

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-07-09 〜 2026-07-15) の全 CVE/GHSA/URL を除外済み。*
