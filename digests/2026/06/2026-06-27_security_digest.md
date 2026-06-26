# KEDA Daily Digest — 2026-06-27 (JST)

> 採用範囲: 公開日 2026-06-25 〜 2026-06-27
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

OpenAI が政府認可約 20 社限定で GPT-5.6「Sol/Terra/Luna」ファミリーを発表し、フロンティア AI へのアクセスが初めて政府承認機構に組み込まれた——TechCrunch は「OpenAI vs Anthropic の対立軸は崩壊した」と論評し、同日カリフォルニア州連邦地裁が Anthropic Fable 5 禁止令を一時的に差し止めた。セキュリティ面では PTC Windchill (CVE-2026-12569, CVSS 9.3) が製造・防衛 PLM として CISA KEV 史上初登録となり JSP webshell 展開が確認、Linux カーネル「DirtyClone」(CVE-2026-43503, CVSS 8.8) の PoC 公開と Incus コンテナ Critical 9.9 CVE 2 件 (CVE-2026-48755/48769) が重なりコンテナインフラへの圧力も高まっている。Google GTIG が Turla の新 .NET バックドア「STOCKSTAY」によるウクライナ軍・政府機関への標的攻撃詳細を公開し、ロシア系 APT の持続的活動を裏付けた。

## AI 関連ニュース

- **[2026-06-26]** [OpenAI が GPT-5.6「Sol / Terra / Luna」を米政府認可 約 20 社限定でプレビュー公開 — Sol が最強推論モデル (コーディング・生物学・サイバーセキュリティで GPT-5.5 比大幅向上、新「ultra」モードでサブエージェント利用可能)、Terra がバランス重視、Luna が速度・低コスト特化の 3 モデル構成; 米政府が「Mythos 類似能力」を理由に限定公開を要求しカスタマー個別承認制を導入; 今後数週間内に対象拡大予定](https://www.axios.com/2026/06/26/openai-gpt-sol-terra-luna-trump) *(Axios / VentureBeat / MacRumors / 9to5Mac)*

- **[続報][2026-06-26]** [Anthropic Fable 5 禁止令 Day 14 — 議会 4 議員が設定した商務省 Lutnick 長官への 6/26 文書回答期限が完全無回答のまま通過; カリフォルニア州連邦地裁が政府の禁止措置を一時差し止める仮差止命令を付与 (「反論したこと自体を理由に企業を潜在的敵対者と烙印できない」との 43 ページ判決); Anthropic は商務省との交渉を継続中](https://fedscoop.com/radio/district-court-judge-temporarily-blocks-the-federal-ban-on-anthropic/) *(FedScoop / ms.now / Bloomberg)*

- **[2026-06-26]** [TechCrunch: 「OpenAI と Anthropic の戦いはもはや 2 社間の競争ではない」— 政府が GPT-5.6 も Fable 5 も同じ承認機構で縛る構造となり、フロンティア AI 規制は競争ではなく集団対応を必要とする段階へ転換したと論評; 「一方が政府審査で失敗すれば双方のモデルが市場から消える」という共同リスクを指摘](https://techcrunch.com/2026/06/26/its-not-about-anthropic-vs-openai-anymore/) *(TechCrunch)*

## セキュリティ関連ニュース

- **[2026-06-26]** [Google Threat Intelligence Group (GTIG) が Turla (ロシア FSB 帰属) の新 .NET バックドア「STOCKSTAY」を詳報 — Kazuar と共通コードを持つ多コンポーネントバックドア; 外交・学術テーマのルアー + 悪意ある RDP ファイルでウクライナ軍・政府機関に投下; websocket-sharp ライブラリで WebSocket C2 を実装し正規通信に偽装; 開発活動は 2022 年 12 月遡及; イタリア・オランダ・ポーランド・ドイツも標的圏に含まれる](https://cloud.google.com/blog/topics/threat-intelligence/stockstay-turla-intelligence-gathering) *(Google Cloud Blog / The Hacker News)*

- **[2026-06-25]** [Microsoft Security Blog: ホスピタリティ業界(欧州・アジア)を標的とした Photo ZIP フィッシングキャンペーンが 4 月から継続 — Calendly・Google URL リダイレクトを経由した「認証偽装」でメール認証を突破; 宿泊予約照会・クレームを装う ZIP → 偽ショートカット → 難読化 PowerShell → Node.js インプラント + デュアルレジストリ永続化 + 非標準ポート C2 の多段チェーン; 強制シャットダウン・PE ペイロード生成が観測されており目的は不明; 帰属未確認](https://www.microsoft.com/en-us/security/blog/2026/06/25/photo-zip-campaign-targeting-hospitality-industry-delivers-node-js-implant-persistent-access/) *(Microsoft Security Blog / The Hacker News / TechRadar)*

- **[2026-06-26]** [PTC Windchill (PDMLink/FlexPLM) CVE-2026-12569 が CISA KEV に追加 — 製造・防衛・航空宇宙の PLM として CISA KEV 史上初登録; 入力検証欠落でリモート攻撃者が任意コード実行; 実証済み攻撃チェーン: HTTP リクエスト → JSP webshell 配置 → 持続的バックドア + データ漏洩; CVSS 9.3; BSI・ドイツ警察が大型工場を訪問警告するという異例対応が取られた; PTC は 6/25 時点で「脅威活動が高まっている」と IOC を公開](https://thehackernews.com/2026/06/cisa-adds-exploited-ptc-windchill-rce.html) *(The Hacker News / SecurityWeek / CISA)*

- **[続報][2026-06-26]** [Klue 侵害続報: 追加被害組織 (Recorded Future・Tanium・Jamf・Huntress 等) が Salesforce インスタンスのデータ漏洩を正式確認; Salesforce は 6/17 に Klue 連携を無効化; 恐喝グループ Icarus のリークサイトが複数日停止 (身代金支払い交渉の可能性); 第三者グループが Icarus からデータを逆に窃取する「ハッカー vs ハッカー」展開が SecurityWeek に確認](https://www.securityweek.com/more-klue-breach-victims-identified-as-hackers-get-hacked/) *(SecurityWeek / BleepingComputer / The Register)*

- **[2026-06-25]** [Mini Shai-Hulud「Miasma」新波: LeoPlatform/RStreams の 20+ npm パッケージが 6/24 の narrow window で汚染、Go エコシステム (Verana Blockchain モジュール) と GitHub Actions ワークフローへ拡大 — binding.gyp の「Phantom Gyp」パターンで node-gyp 実行時に CI/CD 認証情報を窃取; 以前の Red Hat (@redhat-cloud-services)・PyPI・Azure を経由した Shai-Hulud キャンペーンの最新波; 窃取資格情報を用いたレジストリ横断自己伝播](https://socket.dev/blog/miasma-mini-shai-hulud-hits-leoplatform-npm-packages-go-ecosystem) *(Socket Threat Research / Sonatype / safedep.io / The Hacker News)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-25 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-43503 | Linux カーネル < v7.1-rc5 (DirtyFrag 未修正の全ディストリビューション) | CWE-732 / **8.8** | ネットワークパケットをカーネル内クローン時に「ファイルマップ済み共有ページ」フラグが2つのヘルパー関数で落とされる → 攻撃者が `/usr/bin/su` 等 setuid バイナリのメモリを攻撃者制御 IPsec トンネル越しに上書きしログインチェックを無効化 → ローカル権限から root 昇格 | [commit 48f6a5356a33 (Linux v7.1-rc5, 2026-05-21 マージ)](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git) | **JFrog PoC 公開 2026-06-25 / DirtyFrag 派生「DirtyClone」/ ローカル shell 環境全般に影響** / IPsec + file-backed memory の同パターンを持つ他 OS カーネルへバリアントハント推奨 |
| CVE-2026-12569 | PTC Windchill PDMLink / FlexPLM (全バージョン、PTC 修正パッチ未適用) | CWE-20 / **9.3** | HTTP リクエストパラメーターの入力検証欠落 → ネットワーク経由でリモート任意コード実行; 実証攻撃: HTTP 送信 → JSP webshell 配置 → 持続バックドア + データ漏洩 | [PTC Trust Center パッチ (2026-06)](https://www.ptc.com/en/about/trust-center/advisory-center/active-advisories/windchill-flexplm-rce-vulnerability) | **CISA KEV 2026-06-26 追加 / PTC 製品で KEV 初登録 / JSP webshell 展開確認 / CVSS 9.3** / 製造 PLM・PDM に共通の HTTP パラメーター受け渡しパターンへバリアントハント推奨 |
| CVE-2026-48755 / GHSA-v6mj-8pf4-hhw4 | Incus (lxc/incus) < 7.2.0 (Go 製コンテナ・VM マネージャー) | CWE-20 / **9.9** | バックアップ圧縮 API の `compression_algorithm` パラメーターが先頭トークン (`zstd` 等) のみ許可リスト照合し残余フラグ/オプションを素通し → 認証済みユーザーが `zstd -d -f -o /etc/cron.d/rce` 等を指定し Incus デーモン権限でホスト上に任意ファイル書き込み → cron ジョブ等経由で RCE | [Incus v7.2.0](https://github.com/lxc/incus/releases/tag/v7.2.0) | 2026-06-25 GHSA 公開 / CVSS 9.9 / 認証済みユーザーのみで成立 / 許可リスト「先頭トークンのみ照合」パターン → Podman・containerd 等のバックアップ/エクスポート API へバリアントハント推奨 |
| CVE-2026-48769 / GHSA-f6m5-xw2g-xc4x | Incus (lxc/incus) < 7.2.0 | CWE-20 / **9.9** | 攻撃者制御の画像サーバーが返す `Incus-Image-Hash` HTTP レスポンスヘッダーをパス検証なしに `filepath.Join(destDir, fp)` のファイル名として使用 → SHA-256 チェックサム検証前にパストラバーサルで任意パスへファイル書き込み → root 権限で cron ジョブを注入し RCE | [Incus v7.2.0](https://github.com/lxc/incus/releases/tag/v7.2.0) | 2026-06-25 GHSA 公開 / CVSS 9.9 / 攻撃者が画像サーバーを制御するだけで成立 (認証不要) / コンテナ画像配信の信頼ヘッダー利用パターン → OCI イメージレジストリプロキシ等へバリアントハント推奨 |

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-06-26 | CVE-2026-8797 / JVN | NEC ExpressUpdate Agent for Windows v3.24 以前: 名前付きパイプのアクセス制御不備 (CWE-782) → ローカル悪意ユーザーが SYSTEM 権限で任意コード実行 (LAC・MASAHIRO IIDA 報告、JPCERT/CC 協調) | CVSS 7.8 / 高 | [JVN](https://jvn.jp/) |
| 2026-06-26 | CVE-2026-56129 / JVN | 東芝・Dynabook の Generic IO & Memory Access ドライバー (2009〜2016 年製 PC インストール版): IOCTL インターフェイスのアクセス制御欠落 (CWE-782) → ローカルユーザーが BIOS/スーパーバイザーパスワード設定を操作可能 | 高 (CVSS 詳細 TBD) | [JVN](https://jvn.jp/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 28 ソース (Axios / VentureBeat / MacRumors / 9to5Mac (GPT-5.6), FedScoop / ms.now / Bloomberg / FutureSearch (Anthropic injunction), TechCrunch (AI industry), Google Cloud Blog / THN / infosectoday.io / thomasharris6.wordpress.com (Turla STOCKSTAY), Microsoft Security Blog / THN / TechRadar / ibtimes.sg (Hotel phishing), THN / SecurityWeek / CISA / SecurityAffairs / gnerdsec.com (PTC Windchill KEV), SecurityWeek / BleepingComputer / The Register / Huntress (Klue 続報), Socket.dev / Sonatype / safedep.io / THN / SecurityWeek (Miasma), JFrog / THN / cybersecuritynews.com / linuxiac.com (DirtyClone), GitHub Advisory Database (Incus CVEs), JVN / JPCERT/CC / vulnerability.circl.lu (国内))
- 採用件数: AI=3 / Security=5 / CVE=4 / 国内=2
- AI 件数が目安 (8〜12) を下回った理由:
  - 採用窓 (2026-06-25〜27) は木〜土にあたり大型 AI ラボからのモデルリリースが少ない静穏期
  - macOS.Gaslight (DPRK LLM Prompt Injection バックドア): 2026-06-26 digest 掲載済み → 除外
  - Claude Tag (Anthropic Slack AI チームメンバー機能): 2026-06-25 digest 掲載済み → 除外
  - Gemini 3.5 Pro: 6/26 時点で正式 GA 未到達 (Sundar Pichai「来月まで」と発言、7 月延期報道あり、未公式)
  - NVIDIA Nemotron 3 Ultra: 2026-06-04 公開 → 採用窓外
  - OpenAI Jalapeño 推論チップ: 2026-06-26 digest 掲載済み → 除外
  - 独立した新規 AI セキュリティ研究論文: 採用窓内に確認できず
- Security 件数が目安 (8〜12) を下回った理由:
  - CISA KEV 6/26 追加は PTC Windchill 1 件 (UniFi OS/Lantronix/Cisco UCM は前回 digest 掲載済み)
  - GitLab 3 CVE / macOS ClickFix / Mistic-KongTuke / RoguePlanet [続報]: 2026-06-26 digest 掲載済み
  - Operation Endgame / StealC-Amadey: 2026-06-25 digest 掲載済み
  - GentleKiller ESET: 2026-06-21 digest 掲載済み
- 除外理由内訳:
  - 古すぎ (公開日 < 2026-06-25):
    - ServiceNow API インシデント (開示 2026-06-09)
    - Hysteria GHSA-vgrc-hq28-p3xp UDP ACL bypass (2026-05-23 公開)
    - remark42 CVE-2026-48788 XSS (2026-05-22 公開)
    - @cyclonedx/cdxgen GHSA-5vwr-qchf-q4pf Maven injection (2026-05-22 公開)
    - pydantic-ai CVE-2026-48782 SSRF bypass (2026-05-23 公開)
    - Incus CVE-2026-48753 / GHSA-ccjc-4qc3-jxqc S3 path traversal (初出 2026-05-28、最終更新 6/26 だが採用窓外)
    - NVIDIA Nemotron 3 Ultra (2026-06-04 公開)
    - Anthropic Fable 5 禁止令初報 (2026-06-12〜13) → 続報のみ採用
  - 重複 (excluded_set 直近7ダイジェスト 2026-06-20〜2026-06-26 の全 CVE/GHSA/URL):
    - CVE-2026-34908/34909/34910 UniFi OS / CVE-2025-67038 Lantronix KEV (2026-06-25 digest)
    - CVE-2026-20230 Cisco UCM webshell (2026-06-25 digest)
    - CVE-2026-20245 Cisco SD-WAN Mandiant (2026-06-26 digest)
    - CVE-2026-10712/10086/12053 GitLab (2026-06-26 digest)
    - CVE-2026-47145〜47151 EmberZNet Zigbee (2026-06-26 digest)
    - CVE-2026-8461 FFmpeg PixelSmash / CVE-2026-47729 Squidbleed / CVE-2026-41948/47 DifyTap (2026-06-24 digest)
    - CVE-2025-71351/71378/CVE-2026-56319 picklescan / CVE-2026-56403〜56412 libexpat / CVE-2026-56265 crawl4ai JWT (2026-06-22 digest)
    - AutoJack CVE / usbliter8 BootROM / CVE-2026-20253 Splunk KEV (2026-06-21 digest)
    - CVE-2026-42530/42055 NGINX / CVE-2026-48933/48618 Node.js (2026-06-20 digest)
    - Klue/Salesforce LastPass 正式開示 (2026-06-25 digest) → 今回「続報」として追加被害者・Icarus 停止を採用
  - 取得失敗ソース (HTTP 403): thehackernews.com 個別記事, bleepingcomputer.com 個別記事, securityweek.com 個別記事, jfrog.com 個別記事, nvd.nist.gov 個別 CVE, securityaffairs.com 個別記事, cvefind.com, cyfirma.com, venturebeat.com 個別記事, jvn.jp 個別アドバイザリ — WebSearch スニペット・github.com/advisories・複数独立媒体で内容・公開日を補完

</details>

---

*excluded_set 参照: 直近7ダイジェスト (2026-06-20〜2026-06-26) の全 CVE/GHSA/URL を除外済み。*
