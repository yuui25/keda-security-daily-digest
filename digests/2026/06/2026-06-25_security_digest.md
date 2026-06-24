# KEDA Daily Digest — 2026-06-25 (JST)

> 採用範囲: 公開日 2026-06-23 〜 2026-06-25
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Anthropic が Claude Tag を Slack に投入し「AI をチームメイトとして統合する」路線を具体的製品で加速させた一方、Novee Security が「Cordyceps」として命名した GitHub Actions サプライチェーン脆弱性パターンで Microsoft・Google・Apache を含む 300+ リポジトリが完全悪用可能と判明——AI コーディングツールが同一の不安全設定を量産し脆弱性を拡散させている実態も浮き彫りに。CISA が Ubiquiti UniFi OS の CVSS 10.0 三連チェーン CVE (CVE-2026-34908/34909/34910) と Lantronix EDS5000 (CVE-2025-67038) を KEV に追加し連邦機関修正期限を 6/26 と設定、Cisco UCM では CVE-2026-20230 の Tor 経由 webshell 投下が観測されており IoT/通信インフラへの圧力が続いている。

## AI 関連ニュース

- **[2026-06-23]** [Anthropic、Slack 向け「Claude Tag」を発表 — @Claude をチャンネルでタグ付けし作業を非同期委任できる AI チームメンバー機能; タスクをステップに分解し単独実行・コンテキスト継続保持・プロアクティブ通知に対応; 65% の Anthropic 製品チームコードはすでに社内 Claude Tag が生成; Claude Enterprise/Team ユーザー向けにリサーチプレビューとして提供開始](https://www.anthropic.com/news/introducing-claude-tag) *(Anthropic / TechCrunch / Fortune / Bloomberg / IT Pro)*

- **[2026-06-23]** [「Cordyceps」: AI コーディングツールが脆弱な GitHub Actions パターンを量産と Novee Security が警告 — 開発者が Copilot/Claude Code 等で CI/CD 設定を生成すると `pull_request_target` の誤用・信頼境界を越えるトークン伝播など同一クラスの欠陥が繰り返しリポジトリに植え付けられる; AI が脆弱性を人間より高速に拡散する新局面と指摘; Novee は 30,000+ リポジトリを走査し 300+ 件を完全悪用可能と確認](https://novee.security/blog/cordyceps/) *(Novee Security / The Hacker News / Dark Reading / HackRead)*

- **[2026-06-24]** [Microsoft DCU が Copilot で StealC/Amadey マルウェアを解析し史上初の2サービス同時 RICO 訴追を実現 — 平易な英語で問い合わせるだけでマルウェアコードの難読化解除・隠しデータ抽出・証拠検証が完了; 200+ の C2 ドメイン/IP を差し押さえ; 2週間の作戦で 27M 件の盗難認証情報を回収・4,700 万ドル相当の暗号資産を凍結; Europol/Bitsight/ESET/Bitdefender と共同](https://www.microsoft.com/en-us/security/blog/2026/06/24/stealc-and-amadey-breaking-down-infostealers-and-the-cybercrime-services-that-deliver-them/) *(Microsoft Security Blog / The Hacker News / SecurityWeek / CyberScoop / The Register)*

## セキュリティ関連ニュース

- **[2026-06-23]** [「Cordyceps」: GitHub Actions CI/CD ワークフローの組み合わせ脆弱性で Microsoft・Google・Apache・Cloudflare・Python Software Foundation 等のリポジトリが非認証パイプライン乗っ取りにさらされていたと Novee Security が公開 — 無料 GitHub アカウント1つで承認偽造・コード push・認証情報窃取が可能; 個別 CVE は未採番 (設定ミスパターンのため); 各組織に連絡し修正確認済み; GitHub は 6/18 に actions/checkout v7 でパターンの一部をブロック](https://novee.security/blog/cordyceps/) *(Novee Security / The Hacker News / SecurityWeek / Dark Reading)*

- **[2026-06-23]** [GitHub、`actions/checkout` v7 を公開し `pull_request_target` + fork head チェックアウトの pwn request パターンをデフォルトブロック — Mastra 144 パッケージ侵害 (6/16) や Nx build system s1ngularity 事案など多数のサプライチェーン侵害の根本原因パターンを遮断; 2026-07-16 に既存全メジャーバージョンへバックポート予定](https://thehackernews.com/2026/06/github-updates-actionscheckout-to-block.html) *(The Hacker News / GuardianMSSP / Cyberpress)*

- **[2026-06-23]** [悪意ある npm パッケージ群が PostCSS ツールを偽装し Windows RAT を配布 — "postcss-minify-selector"(256 DL)・"aes-decode-runner-pro"・"postcss-minify-selector-parser"(615 DL) の3パッケージが多段 PowerShell ドロッパー経由でリモートシェル・ファイル転送・Chrome DPAPI 認証情報窃取機能を持つ RAT を展開; JFrog が発見し npm は当該パッケージを削除済み](https://thehackernews.com/2026/06/malicious-npm-packages-pose-as-postcss.html) *(The Hacker News / Infosecurity Magazine / GBHackers)*

- **[2026-06-23]** [CISA が Ubiquiti UniFi OS 3 CVE (CVE-2026-34908/34909/34910) と Lantronix EDS5000 (CVE-2025-67038) を KEV に追加、連邦機関修正期限 2026-06-26 — UniFi OS は認可バイパス→パストラバーサル→コマンドインジェクションの3段チェーンで非認証 root RCE を Bishop Fox が実証 (CVSS 10.0); Lantronix は HTTP RPC ログコマンドへの username 無害化欠落で root OS コマンドインジェクション (CVSS 9.8); いずれも野外悪用確認済み](https://www.cisa.gov/news-events/alerts/2026/06/23/cisa-adds-four-known-exploited-vulnerabilities-catalog) *(CISA / BleepingComputer / SecurityWeek / GBHackers)*

- **[2026-06-24]** [Operation Endgame Phase 2: StealC・Amadey インフォスティーラー基盤を国際共同オペレーションで撲滅 — Microsoft DCU・Europol・Bitdefender・ESET が 200+ の C2 ドメイン/IP を差し押さえ; 4,700 万ドル超の暗号資産凍結・27M 件の盗難認証情報を回収; 2 週間の作戦期間中 StealC/Amadey は 14 万台以上のデバイスに感染; RICO を用いた2サービス同時標的は史上初](https://www.helpnetsecurity.com/2026/06/24/operation-endgame-stealc-amadey-malware-disrupted/) *(Help Net Security / Infosecurity Magazine / ESET / Bitsight)*

- **[2026-06-24]** [Cisco Unified CM/SME の CVE-2026-20230 が野外悪用フェーズに移行 — Tor 経由の自動スウィープが蜜罐に到達し WebDialer SSRF を悪用してスプリアス Apache Axis サービスを展開・コマンド実行 webshell を設置; PoC 公開 (6/3) からわずか 3 週間で大規模な自動化エクスプロイトへ; 修正版: Unified CM 14SU6 / 15SU5 (COP パッチ)](https://www.helpnetsecurity.com/2026/06/24/cisco-unified-cm-flaw-exploited-to-drop-webshells-cve-2026-20230/) *(Help Net Security / BleepingComputer / SecurityWeek / TechTimes)*

- **[続報][2026-06-24]** [LastPass が Klue 経由の Salesforce 侵害でセールスデータ流出を確認 — Klue に侵入した Icarus 恐喝グループが OAuth トークンを窃取し LastPass・Gong・Jamf・HackerOne・Snyk・Huntress など 12 組織の Salesforce/Gong データに横断アクセス; 窃取データに顧客名・メール・電話・住所・サポートケースを含む (パスワード保管庫への影響なし); 今回が LastPass による正式確認・開示 (Klue 初報は 2026-06-18)](https://www.helpnetsecurity.com/2026/06/24/lastpass-klue-data-breach-salesforce-environment/) *(Help Net Security / SecurityWeek / TechRadar)*

- **[2026-06-24]** [米医療 AI 企業 Xsolis が 2026-01 のフィッシング被害を開示 — AI 活用病院向け診療管理 SaaS への不正アクセスで 140 万人分の氏名・生年月日・健康保険情報・社会保障番号・医療情報が漏洩; Xsolis は 600 超の病院・医療保険者を顧客に持つ; 過去 1 か月で医療テクノロジー企業 3 社目の侵害開示 (iRhythm・Novo Nordisk に続く)](https://www.helpnetsecurity.com/2026/06/24/xsolis-data-breach-phishing-attack/) *(Help Net Security / HIPAA Journal / SecurityWeek / TechRadar)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-23 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-34908 / CVE-2026-34909 / CVE-2026-34910 | Ubiquiti UniFi OS Server < 5.0.8 / Cloud Gateway < 5.1.12 (UDM/UDM-Pro/UNVR/UCK/Cloud Key 等全製品) | CWE-284 / CWE-22 / CWE-78 / **10.0** | (34908) 管理インターフェイスの認可チェック欠落 → 非認証変更; (34909) 同パス上でパストラバーサルによる認証情報等ファイル読み出し; (34910) 取得済み入力を検証なしでシェルコマンドに渡す → root 任意コマンド実行; 3段チェーンで Bishop Fox が非認証 root RCE を実証 | [UniFi OS Server 5.0.8 / Cloud Gateway 5.1.12](https://community.ui.com/releases/Security-Advisory-Bulletin-064-064/84811c09-4cf4-42ab-bd61-cc994445963b) | **CISA KEV 2026-06-23 追加 / CVSS 10.0 / 野外悪用確認 / 連邦機関期限 2026-06-26** / UDM-Pro を含む全 Ubiquiti ゲートウェイ製品に影響 / 同種の EmbOS/OpenWRT ベース管理 UI への3段チェーンバリアントハント推奨 |
| CVE-2025-67038 | Lantronix EDS5000 ≤ 2.1.0.0R3 (シリアル-Ethernet 変換 IoT デバイス) | CWE-78 / **9.8** | HTTP RPC モジュールが認証失敗時のログコマンドで `username` パラメーターを無害化なしにシェルコマンドへ直接結合 → 非認証攻撃者が root 権限で任意 OS コマンドを実行 | [EDS5000 v2.2.0.0R1](https://www.cisa.gov/news-events/ics-advisories/icsa-26-069-02) | **CISA KEV 2026-06-23 追加 / CVSS 9.8 / 野外悪用確認 / 連邦機関期限 2026-06-26** / ログ機能での認証情報シェル結合パターン → 組み込み機器の他 RPC エンドポイントへバリアントハント推奨 |
| CVE-2026-20230 | Cisco Unified CM / Unified CM SME 14.x < 14SU6 / 15.x < 15SU5 | CWE-918 / **8.6** (Cisco は Critical と評価) | WebDialer サービスが HTTP リクエストの入力を未検証で内部ルーティングに使用 → 非認証 SSRF; file:// ペイロードでホスト OS への任意ファイル書き込み → rogue Apache Axis サービス経由で webshell 設置 → root 昇格 | [Unified CM 14SU6 / 15SU5 または COP パッチ](https://www.cisco.com/c/en/us/support/docs/csa/cisco-sa-cucm-ssrf-cXPnHcW.html) | **野外悪用確認 2026-06-24 / Tor 経由自動スウィープで webshell 投下観測 / PoC 公開から 3 週で大規模自動化** / WebDialer 有効な全 CUCM 環境に影響 / SIP/VoIP スタックの SSRF + ファイル書き込み合成パターンへバリアントハント推奨 |

## 国内脆弱性・インシデント情報

> 直近2日間に該当する新規国内ニュースは確認できませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 30 ソース (Anthropic Blog / TechCrunch / Fortune / Bloomberg / IT Pro, Novee Security / THN / Dark Reading / HackRead / SecurityWeek / GuardianMSSP (Cordyceps/GitHub checkout), JFrog / THN / Infosecurity Magazine (npm RAT), Microsoft Security Blog / ESET / Bitsight / Europol / CyberScoop / Help Net Security (Operation Endgame), CISA / BleepingComputer / SecurityWeek / GBHackers (UniFi/Lantronix KEV), Help Net Security / BleepingComputer / TechTimes (Cisco CVE-2026-20230), Help Net Security / SecurityWeek / TechRadar (LastPass/Klue), Help Net Security / HIPAA Journal / SecurityWeek (Xsolis), JVN / JPCERT, NVD, GitHub Advisory Database)
- 採用件数: AI=3 / Security=8 / CVE=3 / 国内=0
- 採用件数が目安 (各 8〜12件) を下回った理由 (AI):
  - OpenAI GPT-5.6: 6/25 時点で公式アナウンスなし (Polymarket 90% だが未発表のため除外)
  - Gemini 3.5 Pro: cryptobriefing.com が「Google は July 2026 にリリース延期」と報道、GA 未到達のため除外
  - Grok 5: 6/25 時点で未リリース (Q2 ウィンドウ通過済み)
  - White House AI EO「Promoting Advanced Artificial Intelligence Innovation and Security」: 6/2 署名・NSPM-11 は 6/5 — いずれも採用窓外
  - Exim CVE-2026-45185 (Dead.Letter) BleepingComputer: 5/13 公開 — 採用窓外
  - M365 Copilot SearchLeak CVE-2026-42824: Varonis 開示 6/15・MS 修正 6/9 — 採用窓外
  - Veeam CVE-2026-44963: BleepingComputer 報告 ≈6/9〜10 — 採用窓外
  - GreatXML BitLocker PoC: 6/11 公開 — 採用窓外
- 除外理由内訳:
  - 古すぎ (公開日 < 2026-06-23): 上記参照 + GitHub RCE CVE-2026-3854 (April 2026), Ghost CMS CVE-2026-26980, Starlette CVE-2026-54282, fast-xml-parser CVE-2026-44664 (日付不確定)
  - 重複 (excluded_set 直近 7 ダイジェスト 2026-06-18 〜 2026-06-24):
    - Five Eyes AI共同警告 / OpenAI Patch the Planet / Samsung ChatGPT全社展開 / Squidbleed / DifyTap (2026-06-24 digest)
    - FFmpeg PixelSmash CVE-2026-8461 / ShapedPlugin バックドア CVE-2026-10735 / FastStone CVE-2026-30040/30041 (2026-06-24 digest)
    - AryStinger botnet / OpenAM CVE-2026-44203/41573/44179 / AVideo CVE-2026-33692 (2026-06-23 digest)
    - libexpat CVE-2026-56403〜56412 / crawl4ai CVE-2026-56265 / picklescan CVEs (2026-06-22 digest)
    - AutoJack CVE / usbliter8 BootROM / Splunk CVE-2026-20253 (2026-06-21 digest)
    - NGINX CVE-2026-42530/42055 / Node.js CVE-2026-48933/48618 (2026-06-20 digest)
    - Mastra npm supply chain (初報 6/16〜18, Microsoft 北朝鮮帰属確認は 2026-06-21 digest) / Klue OAuth breach 初報 (2026-06-19 digest) — LastPass 正式開示は新規として採用
    - FortiBleed 全般 (2026-06-18〜24 digest 掲載済み)
  - 日付不明/確認不可: OpenAI GPT-5.6 (官発表なし), Gemini 3.5 Pro GA (遅延確定)
  - 取得失敗ソース (HTTP 403): anthropic.com/news 個別記事, microsoft.com security blog 個別 (スニペット補完), bleepingcomputer.com 個別記事, xbow.com ブログ, jvn.jp 個別ページ, cisa.gov 個別アドバイザリ — WebSearch スニペット・複数独立媒体で内容・日付を補完

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-06-18 〜 2026-06-24) の全 CVE/GHSA/URL を除外済み。*
