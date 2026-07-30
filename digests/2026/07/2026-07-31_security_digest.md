# KEDA Daily Digest — 2026-07-31 (JST)

> 採用範囲: 公開日 2026-07-29 〜 2026-07-31 (JST)
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Microsoft Copilot for Word の自己伝播 XPIA ワームが 144 日の調整開示を経て公開され、隠し白文字プロンプト経由で文書を汚染し連鎖伝播する AI 固有の攻撃ベクターが改めて示された。インフラ面では Broadcom が vCenter 2 件 CVSS 9.8・ESXi VM 脱出 CVSS 9.3 を含む VMSA-2026-0006 を公開し、Cisco Secure FMC のハードコード認証情報 CVE-2026-20316 が CISA KEV に追加されて連邦機関の対応期限が 8/1 に設定された。Wiz Research が Azure Cosmos DB の platform-wide 署名シークレット漏洩 CosmosEscape を公表し (Microsoft 修正済み・顧客対応不要)、国内では生命保険協会の契約照会システムで約 3.7 万件の個人情報が閲覧可能状態となっていたことが 7/29 に公式発表された。

## AI 関連ニュース

- **[2026-07-29]** [Microsoft Copilot for Word で XPIA 自己伝播ワームを Håkon Måløy が公開 — 白文字隠しプロンプトが Copilot に文書改ざんを指示し悪意ある命令を新規文書に埋め込み連鎖感染。144 日間の調整開示後、Word ワームは未修正](https://www.theregister.com/security/2026/07/29/word-worm-crawls-into-copilot-spreads-chaos/5280588) — 攻撃者が白文字・極小フォントで隠したプロンプトを Word 文書に埋め込む → Copilot が指示を受け取り財務数値の改ざん等を実行 → 悪意ある指示をそのまま生成文書に埋め込み次の被害者に伝播。Microsoft は Copilot Memory・Outlook 欠陥は修正済みも Word 経由の XPIA は 2026-07-28 時点で未対処 *(The Register / CyberNews / GBHackers / Malwarebytes)*

- **[2026-07-29]** [OpenAI が ChatGPT Academic Researchers プログラムを開始 — まず 1 万人の学術研究者に GPT-5.6 Sol Pro への無料アクセスを提供し 2027 年末までに 10 万人規模へ拡大](https://openai.com/index/chatgpt-for-academic-researchers/) — 科学・数学・工学分野の研究者を対象に選定した学術機関から公募; モデル重みの提供は対象外。OpenAI スタッフによる直接支援も提供 *(Axios / SiliconAngle / TechTimes / OpenAI Blog)*

- **[2026-07-30]** [Wiz Research が CosmosEscape を公表 — Azure Cosmos DB の Gremlin API から platform-wide 署名シークレット取得に成功し任意の Cosmos DB アカウントを掌握可能な状態だったと開示 (Microsoft は 2025/11 に修正済み・顧客対応不要)](https://www.wiz.io/blog/cosmosescape-taking-over-every-database-in-azure-cosmos-db) — 攻撃者制御 Gremlin DB への細工クエリ → マルチテナントゲートウェイで RCE → platform-wide 署名シークレット取得 → 任意アカウントのプライマリキー奪取 → 全読取/書込みアクセス。Microsoft Entra ID・Teams・Copilot バックエンドも影響範囲。Wiz の報告 (2025-11-20) から 2 日でホットフィックス、2026-07 に長期修正完了 *(Wiz Blog / THN / HackRead / CyberSecurityNews)*

- **[2026-07-29]** [EU AI Act Article 50 透明性義務が 2026-08-02 に施行 — チャットボット・合成メディア・感情認識システム等への開示義務が法的拘束力を持つ、違反罰則最大 €15M 又は年間売上の 3%](https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-article-50-transparency-20260729/) — 高リスクシステム (Annex III) の延期対象外として予定通り施行; 国内市場監視当局・AI Office・欧州データ保護監督機関が執行主体 *(CSA Labs / Sidley Data Matters / EU Digital Strategy)*

- **[2026-07-29/30]** [Amazon が 2025/9 の npm debug・chalk ハイジャックを北朝鮮系 Sapphire Sleet に帰属 — 2B+ 週間 DL の 18 パッケージにウォレット窃取スクリプトを混入、2026/3 の axios 侵害グループと中程度確信で同一評定](https://thehackernews.com/2026/07/amazon-links-debug-and-chalk-npm-hijack.html) — メンテナをルックアライク npm ドメインでフィッシング → アカウント乗っ取り → 悪意あるアップデートを公開。Amazon 脅威インテリジェンスが 2026-07-29 に公表 *(THN / AWS Security Blog / CyberScoop)*

## セキュリティ関連ニュース

- **[2026-07-29]** [Broadcom が VMSA-2026-0006 を公開 — VMware vCenter に未認証 CVSS 9.8×2・ESXi に VM 脱出 CVSS 9.3 の計 5 件の脆弱性をパッチ、回避策なし](https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/38017) — CVE-2026-59309 (vCenter Directory Service 認証バイパス CVSS 9.8)・CVE-2026-59310 (vCenter Syslog ディレクトリトラバーサル RCE CVSS 9.8)・CVE-2026-47876 (ESXi VMXNET3 VM 脱出 CVSS 9.3) が目玉。修正: VCF 9.0.2.0100 / VCF 9.1.0.0300 / vCenter 8.0 U3k。野生悪用・PoC なし *(Broadcom / Rapid7 / GBHackers / SecurityWeek)*

- **[2026-07-29]** [CVE-2026-20316 Cisco Secure FMC のハードコード認証情報が CISA KEV に追加 — 未認証リモート攻撃者が静的低権限アカウントでログインし機密情報取得、他の FMC 欠陥とチェーンで権限昇格、連邦機関対応期限 8/1](https://www.cisa.gov/news-events/alerts/2026/07/29/cisa-adds-one-known-exploited-vulnerability-catalog) — CVSS 5.3 (単体) だが Cisco は高重大度評価; Cisco が 7 月中旬にパッチ公開済み *(CISA / SecurityWeek / THN / CyberPress / RunZero)*

- **[2026-07-28/29]** [@joyfill npm ベータパッケージが DEV#POPPER RAT をサプライチェーン攻撃で配布 — import 時実行でスクリプト禁止フラグを回避、Tron/Aptos/BNB ブロックチェーン経由で暗号化 RAT を解決・展開](https://thehackernews.com/2026/07/two-compromised-joyfill-packages.html) — @joyfill/components@2.0.0-beta.13・@joyfill/layouts@2.0.0-beta.13 が対象。RAT はホスト情報収集・Socket.IO C2・クリップボード窃取・開発者認証情報ファイル改ざんが可能、CI ランナーや本番 SSR 環境にも到達しうる *(THN / GBHackers / BackBox.org / StepSecurity / Socket.dev)*

- **[2026-07-28/29]** [CubePilot (ドローン飛行制御装置メーカー) が DNS ハイジャック攻撃を受け全サブドメインの TLS 証明書を乗っ取られる — 7/24 に攻撃者が cubepilot.org DNS を制御、中間者攻撃が可能な状態に、7/24〜25 にダウンロードしたファームウェアは安全性確認まで使用禁止](https://www.bleepingcomputer.com/news/security/cubepilot-drone-software-dev-hit-by-dns-hijacking-to-intercept-traffic/) — 同日にドメイン奪還・不正証明書失効・当局へ通報済み、フォーラム/文書サイトは調査中のためオフライン継続 *(BleepingComputer / SC Media)*

- **[2026-07-29]** [ロシア系脅威アクターが Zimbra に続き Microsoft OWA を悪用 — 米欧政府機関・通信・金融・航空宇宙・ホスピタリティ分野を標的に認証情報収集キャンペーンを継続](https://www.xloggs.com/2026/07/29/breaking-news-cyber-threats-2026-07-29-0300-pdt/) — パッチ済み Zimbra と同一の脅威アクターが OWA の既知欠陥を悪用する攻撃を横展開、政府系メールインフラのパッチ適用状況の確認が急務 *(Xloggs / 各種 TI ソース)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-07-29 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-66066 (GHSA-xr9x-r78c-5hrm) | Rails Active Storage (activestorage < 7.2.3.2 / 8.0.5.x / 8.1.3.x、vips プロセッサ有効) | CWE-94 / **9.5** (CVSS v4) | 未認証攻撃者が細工画像ファイルをアップロードし variant 生成をトリガー → Active Storage が libvips に allowlist 無効のまま渡す → libvips の"unfuzzed"ローダーがファイルを実行 → 任意ファイル読取 (secret_key_base を含む環境変数) + RCE | rubyonrails.org リリース: [Rails 7.2.3.2/8.0.5.1/8.1.3.1](https://rubyonrails.org/2026/7/29/Rails-Versions-7-2-3-2-8-0-5-1-and-8-1-3-1-have-been-released) (2026-07-29) | CVSS v4 9.5 / 未認証 / Rails 広範利用 / Web アップローダー全般でのバリアント伝播候補 |
| CVE-2026-59309 | VMware vCenter Server (VCF 9.x / vCenter 8.0 U3k 未満、全バージョン) | CWE-287 / **9.8** | 未認証ネットワーク攻撃者が VMware Directory Service 認証エンドポイントにアクセス → 認証を完全バイパス → 仮想インフラ管理プレーン掌握・接続ワークロードを支配 | Broadcom SA [VMSA-2026-0006](https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/38017) / fix: vCenter 8.0 U3k (2026-07-29) | CVSS 9.8 / 未認証 / 回避策なし / vCenter 広範利用 / 野生悪用未確認 |
| CVE-2026-59310 | VMware vCenter Server Syslog コンポーネント (同上) | CWE-22 / **9.8** | 未認証ネットワーク攻撃者が Syslog サービスにパストラバーサルパスを含むリクエストを送信 → サーバー上でパス境界チェックをスキップ → 任意コード実行; CVE-2026-59309 とチェーンで完全 DC 掌握 | 同上 | CVSS 9.8 / 未認証 / CVE-2026-59309 とのチェーン悪用が高確率 |
| CVE-2026-47876 | VMware ESXi (VMXNET3 仮想 NIC 搭載全バージョン) | CWE-787 / **9.3** | VM 内管理者権限ユーザーが VMXNET3 ドライバの境界外書込みを誘発 → ゲスト→ホスト境界を越えて ESXi ホスト上で任意コード実行 (VM 脱出 / VM Escape) | Broadcom SA VMSA-2026-0006 (2026-07-29) | CVSS 9.3 / VM 脱出 / ハイパーバイザー横断バリアント伝播候補 |
| CVE-2026-20316 | Cisco Secure Firewall Management Center (FMC) Software 全対応バージョン (パッチ未適用) | CWE-798 / **5.3** | 未認証リモート攻撃者がビルトイン低権限アカウントの静的認証情報を使用し FMC Web UI にログイン → 機密設定情報を取得; 単体 CVSS は低いが他の FMC 欠陥とチェーンで権限昇格が確認済み | Cisco パッチ (2026-07-中旬) / [CISA KEV 追加 2026-07-29](https://www.cisa.gov/news-events/alerts/2026/07/29/cisa-adds-one-known-exploited-vulnerability-catalog) | **CISA KEV 2026-07-29 / 連邦機関期限 8/1 / 実エクスプロイト確認** |

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-07-29 | 生命保険協会 インシデント | 生命保険契約照会システムで 7/22 外部セキュリティ機関の指摘により発覚: 約 3.7 万件のアカウント登録者の氏名・住所・電話番号・メールアドレスが外部から特定操作で閲覧可能な状態; 保険契約内容・口座情報は対象外、実被害は未確認、WEB 申請停止中。 | 影響中 / 個人情報 3.7 万件 | [生命保険協会 第一報 PDF](https://www.seiho.or.jp/info/news/shared/mt-item/20260729.pdf) / [INTERNET Watch](https://news.yahoo.co.jp/articles/68acc5481cd35819e0d3550367c5c3fac45c2247) |
| 2026-07-28 | JVN#99975039 / CVE-2026-JVNDB-2026-000104 / てがろぐ v4.8.4 以前 | てがろぐ (Fumy Otegaru Memo Logger) v4.8.4 以前に制限が不十分な正規表現を使用している脆弱性 (CWE-625): 攻撃者が管理画面に不正ログインできる可能性。v4.9.0 で修正済み。 | CVSS 3.1: 8.6 (High) / CMS 管理者権限取得 | [JVN#99975039](https://jvn.jp/jp/JVN99975039/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| The Register / CyberNews / GBHackers / Malwarebytes (Copilot Word XPIA worm) | The Register URL "/security/2026/07/29/" 確認 ✓ / GBHackers 2026-07-29 確認 ✓ |
| Axios / SiliconAngle / TechTimes / OpenAI Blog (ChatGPT Academic Researchers) | Axios URL "2026/07/29/openai-academics-research-chatgpt-sol" 確認 ✓ / TechTimes "20260729" 確認 ✓ |
| Wiz Blog / THN / HackRead (CosmosEscape) | Thomas Harris Blog URL "2026/07/30" 確認 ✓ / Wiz Blog 公開 2026-07-30 確認 ✓ |
| CSA Labs / Sidley Data Matters (EU AI Act Article 50) | CSA Labs URL "cisa-research-note-eu-ai-act-article-50-transparency-20260729" 確認 ✓ |
| THN / AWS Security Blog / CyberScoop (Amazon Sapphire Sleet npm) | Thomas Harris Blog URL "2026/07/30" 確認 ✓ / THN 記事確認 ✓ / AWS Blog 2026-07-29 公開確認 ✓ |
| Broadcom SA / Rapid7 / GBHackers (VMSA-2026-0006) | Broadcom SA URL 確認 ✓ / Rapid7 ETR 確認 ✓ / York University UIT "July 2026" 確認 ✓ |
| CISA / SecurityWeek / THN / RunZero (CVE-2026-20316 Cisco FMC KEV) | CISA alert URL "2026/07/29" 確認 ✓ / SecurityWeek 記事確認 ✓ |
| THN / GBHackers / BackBox.org / StepSecurity (@joyfill npm DEV#POPPER) | BackBox.org URL "2026/07/29" 確認 ✓ / Socket.dev ブログ確認 ✓ |
| BleepingComputer / SC Media (CubePilot DNS hijacking) | PRSOL.CC URL "/2026/07/29/" 確認 ✓ (BleepingComputer 元記事) / SC Media brief 確認 ✓ |
| Xloggs 2026-07-29 (Russia OWA attacks) | Xloggs URL "2026/07/29/breaking-news-cyber-threats-2026-07-29-0300-pdt" 確認 ✓ |
| rubyonrails.org / GBHackers / THN (CVE-2026-66066) | rubyonrails.org URL "/2026/7/29/" 確認 ✓ / GBHackers 2026-07-29 確認 ✓ |
| 生命保険協会 PDF / INTERNET Watch / innovatopia.jp (国内インシデント) | 生命保険協会 PDF URL "20260729" 確認 ✓ / Yahoo News 配信 2026-07-29 確認 ✓ |
| JVN#99975039 / JVNDB-2026-000104 (てがろぐ) | JVNDB-2026-000104 "published on 2026/07/28" 確認 ✓ / JVN#99975039 確認 ✓ |
| thehackernews.com / bleepingcomputer.com | 403 — WebSearch スニペット・二次ソースで代替 |
| nvd.nist.gov / cisa.gov | 403 — WebSearch スニペット代替 |

### 集計サマリ

- **巡回ソース数**: 約 28
- **採用件数**: AI=5 / Security=5 / CVE=5 / 国内=2
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-07-29 より前): Cruciferra Crypter (07-27 THN 掲載) / Zoom CVE-2026-53412 (07-14 公開) / Gemma 4 (04-02 公開) / CubePilot DNS 攻撃自体は 7/24 だが報道 7/29 で採用 / JADEPUFFER 自律 AI ランサム (07-03〜07 掲載済み) / WordPress wp2shell CVE-2026-63030 (07-19 掲載済み)
  - 重複 (直近 7 ダイジェスト掲載済み・excluded_set 参照): Claude Mythos Preview 暗号 (07-30掲載) / AI pacing letter 1,178人 (07-30掲載) / OpenAI/HuggingFace + Modal Labs (07-30掲載) / Hush Security $30M (07-30掲載) / Minnesota water CyberAv3ngers (07-30掲載) / Flying Eagle Android RAT (07-30掲載) / CVE-2026-53921 OpenWrt (07-30掲載) / CVE-2026-66713 Apache Axis2 (07-30掲載) / CVE-2026-60004 Gitea (07-30掲載) / CVE-2026-54639 style-dictionary (07-30掲載) / Microsoft MAI-Cyber-1-Flash (07-29掲載) / Apple iOS 26.6 Project Glasswing (07-29掲載) / CVE-2026-53264 Linux kernel AI (07-29掲載) / Arista CVE-2026-16812 CISA KEV (07-29掲載) / FortiOS CVE-2025-68686 CISA KEV (07-29掲載) / JetBrains CVE-2026-63077 (07-29掲載) / Origin Energy 90万件 (07-29掲載) / Tengu Mirai (07-29掲載) / ELECOM JVN#56870912 (07-29掲載) / GitHub PyPI time-based defenses (07-28掲載) / Fastjson CVE-2026-16723 (07-27掲載) / SourTrade malvertising (07-27掲載) / Kimi K3 open weights (07-27掲載) / GitLab Jupyter BOF (07-26掲載) / JVNVU#99418634 Logto (07-26掲載)

### 主要採用補足

- **Copilot Word XPIA worm**: 研究者 Håkon Måløy の開示日は 7/28 (UTC)、The Register URL が "/security/2026/07/29/" で確認 → 7/29 JST として採用。Word ワームは直近 7 ダイジェスト未掲載の新規。
- **CosmosEscape**: 脆弱性は 2025/11 報告・修正済みだが Wiz Blog の公式公表が 2026-07-30。Thomas Harris 転載 "2026/07/30" 確認 ✓。顧客対応不要だが Microsoft の重要基盤全体への影響から採用。
- **CVE-2026-66066 Rails**: rubyonrails.org URL が "/2026/7/29/" でリリース日確認 ✓。activestorage 全バージョン対象で Rails エコシステム広範影響、libvips 経由の同種バグが他 Ruby gem に水平伝播の可能性。
- **生命保険協会インシデント**: 生命保険協会公式 PDF URL "20260729" 確認 ✓。7/22 外部指摘 → 7/29 公表。国内個人情報案件として優先採用。

### 取得失敗ソース

- bleepingcomputer.com / thehackernews.com / cisa.gov / nvd.nist.gov: 403 Forbidden → WebSearch スニペット + 二次ソースで代替
- Wiz Blog 本文 (wiz.io): アクセス可能なスニペットと Thomas Harris 転載で代替
- Amazon AWS Security Blog 本文: THN・CyberScoop スニペットで代替

</details>

---

*生成: keda-digest-bot / 2026-07-31 05:04 JST*
