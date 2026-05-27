# KEDA Daily Digest — 2026-05-28 (JST)

> 採用範囲: 公開日 2026-05-26 〜 2026-05-28
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

CrowdStrike・Google・Shadowserver の協調作戦により Glassworm ボットネット (ロシア系サイバー犯罪者による開発者サプライチェーン攻撃インフラ) が壊滅した同日、Anthropic Claude の作業ディレクトリを標的にした悪意ある npm パッケージ "Malware-Slop" が発見され、開発者エコシステムへの多面的な包囲が鮮明になった。Adversa AI は AI コーディングエージェント 6 種 (Claude Code・Cursor・Antigravity CLI 等) に共通するシンボリックリンク経由 RCE 手法「SymJack」を公開し、CI 環境での完全自動悪用が可能であると警告した。4 年間見逃されていた Gitea CVE-2026-27771 (30,000+ デプロイに影響する未認証コンテナイメージ pull) と、イラン IRGC 系 Nimbus Manticore の AI 生成バックドア MiniFast が公開されるなど、本日はサプライチェーンと AI 悪用攻撃を軸にした報告が集中した。

## AI 関連ニュース

- **[2026-05-27]** [Malicious npm "mouse5212-super-formatter" (Malware-Slop) が Claude AI ツールの /mnt/user-data をターゲットに API キー・セッションファイルを GitHub へ窃取](https://thehackernews.com/2026/05/malicious-npm-package-stole-files-from.html) — npm で 676 回ダウンロード；内部 'archive deployment sync' ユーティリティを装い Claude のワークスペースファイルを GitHub プライベートリポジトリへ構造化同期。攻撃者が AI でマルウェアを生成しながら自身の GitHub トークンを漏洩させており OpSec の低さが際立つ *(The Hacker News / SafeDep)*

- **[2026-05-27]** [SymJack: Adversa AI が AI コーディングエージェント 6 種 (Claude Code・Cursor・Antigravity CLI・GitHub Copilot・Grok Build・OpenAI Codex) でシンボリックリンク経由 RCE を確認し公開](https://www.securityweek.com/symjack-attack-turns-ai-coding-agents-into-supply-chain-attack-delivery-systems/) — 攻撃者がリポジトリに無害に見えるシンボリックリンクを設置 → エージェントの承認プロンプトは表示パスを表示するがカーネルは別パスに書き込み → 次回起動時に攻撃者コードを実行。CI ランナーでは人手介入ゼロで全シークレットを流出可能 *(Adversa AI / SecurityWeek)*

- **[2026-05-27]** [イラン IRGC 系 APT Nimbus Manticore (Bohrium/APT35 系列) が AI 支援で開発した新型バックドア MiniFast を航空・ソフトウェア企業に展開](https://www.securityweek.com/iranian-apt-targets-aviation-software-companies-with-updated-tools/) — Check Point Research が公開；高速プロトタイピングに AI を活用した 64-bit DLL で Chrome を偽装してステルス持続感染・ファイル窃取・C2 通信を実現。AppDomain ハイジャックで DLL サイドローディングから移行し EDR 回避を強化 *(Check Point Research / SecurityWeek)*

- **[2026-05-26/27]** [CrowdStrike・Google・Shadowserver が Glassworm ボットネット (ロシア系) の C2 全 4 チャネルを 2026-05-26 14:00 UTC に協調して同時無効化](https://techcrunch.com/2026/05/27/crowdstrike-and-google-take-down-botnet-used-by-hackers-to-target-software-developers-in-supply-chain-attacks/) — 2025 年 10 月から GitHub/npm/PyPI/OpenVSX の 400+ リポジトリに侵入し GlassWormRAT (WebSocket 型 JavaScript RAT) を配布；開発者 35,800 人が初波で感染。ブロックチェーン・P2P・正規 Web サービスを C2 解決レイヤーとして多層化した耐テイクダウン設計を突破 *(CrowdStrike Blog / TechCrunch)*

- **[2026-05-26]** [AppOmni が Marlin AI を発表 — SaaS セキュリティアラートを自律的に相関・調査・修復するエージェント型 AI を AppOmni プラットフォームに組み込み](https://siliconangle.com/2026/05/26/appomni-launches-marlin-ai-automate-saas-security-investigation-remediation/) — Salesforce・Microsoft 365・GitHub 等のクラウド SaaS を継続監視し、アラート相関から原因特定・修復手順の生成まで人手介入なしで完結させる自律調査 AI *(SiliconANGLE / SecurityWeek)*

- **[2026-05-26]** [Varonis Atlas が Claude Compliance API と統合 — Claude Enterprise/Platform の全セッション活動を可視化し AI ガバナンス・不正使用の監査を提供開始](https://www.scworld.com/brief/varonis-integrates-claude-ai-compliance-api-into-atlas-platform) — フルセッション調査・データコンテキスト付き AI リスク評価・コンプライアンス監視を Atlas プラットフォームで実現；Anthropic Claude API を既存エンタープライズ SIEM ワークフローに接続する大規模商用統合 *(SC Media / BleepingComputer)*

## セキュリティ関連ニュース

- **[2026-05-26]** [FBI/IC3 が Silent Ransom Group (SRG/Luna Moth/UNC3753) の IT 担当者偽装・物理オフィス訪問を組み合わせた法律事務所標的型データ窃取攻撃に対するアラート (IC3 CSA-260526) を発行](https://www.ic3.gov/CSA/2026/260526.pdf) — フィッシング→遠隔アクセス確立→失敗時に実際の担当者を法律事務所に派遣し USB ストレージでデータ盗取；盗取データで被害者・顧客に直接連絡して身代金交渉。合法的な RMM ツールを悪用するため AV は検出困難 *(FBI IC3 / Help Net Security)*

- **[2026-05-26]** [7-Eleven が ShinyHunters による 18.5 万人超の個人情報漏洩を開示 — フランチャイズ採用管理用第三者ベンダー経由で SSN・運転免許証・住所・電話番号等が流出](https://techcrunch.com/2026/05/26/7-eleven-data-breach-affects-over-185000-peoples-personal-data/) — ShinyHunters が Salesforce レコード 60 万件を窃取し 4 月 21 日を期限に身代金要求。複数の州司法長官に报告済み；被害者に無償信用監視サービスを提供 *(TechCrunch / SecurityWeek)*

- **[2026-05-27]** [イラン系 Nimbus Manticore が AppDomain ハイジャック技術で航空・ソフトウェア企業を侵害 — 米国・欧州・中東の航空・ソフト企業が標的、SEO ポイズニングを APT として初採用](https://www.securityweek.com/iranian-apt-targets-aviation-software-companies-with-updated-tools/) — OnlyOffice プラットフォームから悪意ある ZIP を配布する航空企業偽装フィッシング + Zoom インストーラー偽装バックドアの二重チャネルで侵害；DLL 名に .config 拡張子を付けた XML ファイル経由の AppDomain ハイジャックで実行 *(Check Point Research / SC Media)*

- **[2026-05-26/27]** [Glassworm ボットネット壊滅 — CrowdStrike が Google・Shadowserver と協力して開発者サプライチェーン標的ボットネットの C2 インフラを一斉無効化](https://www.crowdstrike.com/en-us/blog/inside-crowdstrike-takedown-of-a-developer-targeting-botnet/) — クレデンシャル・暗号資産ウォレット・SSH 鍵を窃取する多機能フレームワークを GitHub/npm/PyPI/VSCode 拡張機能マーケットプレイス経由で配布。C2 は blockchain・P2P・正規 Web サービスを多層化した耐テイクダウン設計 *(CrowdStrike / BleepingComputer)*

- **[2026-05-27]** [CVE-2026-27771 Gitea — 未認証でプライベートコンテナイメージが pull 可能な欠陥が 4 年間見逃された、30,000+ デプロイおよび Forgejo も影響](https://thehackernews.com/2026/05/gitea-vulnerability-exposes-private.html) — 「private」コンテナリポジトリ設定が機能せず、アカウント・パスワード不要でイメージ全取得が可能。影響組織は医療・航空宇宙・小売インフラ・ISP に及ぶ。即時対処: v1.26.2 へアップグレードまたは REQUIRE_SIGNIN_VIEW=true 設定 *(Noscope / The Hacker News)*

- **[2026-05-26]** [[続報] CVE-2026-48172 LiteSpeed cPanel Plugin が CISA KEV に追加 — 連邦機関は 2026-05-29 までのパッチ適用が義務付けられ、野外悪用が継続中](https://www.cisa.gov/news-events/alerts/2026/05/26/cisa-adds-one-known-exploited-vulnerability-catalog) — cPanel ユーザーアカウントが root 権限で任意スクリプトを実行可能な特権昇格脆弱性。CISA の 3 日という短い期限設定が攻撃活発度を示す *(CISA)*

- **[2026-05-26]** [Autodesk 3ds Max に複数のファイルパーサー起因脆弱性 (CVE-2026-7450/7451/7452/7453) — 細工した WRL/TIF/PAR ファイルを開くと任意コード実行またはサービス拒否](https://www.autodesk.com/trust/security-advisories/adsk-sa-2026-0002) — v2026.3.2 以前が対象；メモリ破壊・NULL 参照・スタック枯渇の複数バグクラス。3D ファイルを扱うパイプライン (製造・映像・ゲーム) でのソーシャルエンジニアリング経由の悪用が現実的 *(Autodesk Security Advisory)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-05-26 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-27771 | Gitea v1.26.2 未満 / Forgejo (共通実装) | CWE-862 / 未採番 | コンテナレジストリへのアクセス制御チェック欠落 → 未認証ユーザーが `docker pull` のみでプライベートコンテナイメージを取得可能、4 年間見逃し | [v1.26.2 リリース / PR #37610](https://github.com/go-gitea/gitea/releases/tag/v1.26.2) | 30,000+ デプロイ影響 / Forgejo へ水平伝播確認済み / 同仕様 OCI registry 実装の他製品にも類似バグ波及可 |
| CVE-2026-9207 | Tanium Connect (パッチ前全バージョン) | CWE-78 / **8.8** | 認証済みユーザーが Connect 設定フォームにシェルメタキャラクタを注入 → サーバー上で OS コマンドが実行され完全侵害が可能 | (commit 不明) [(TheHackerWire)](https://www.thehackerwire.com/tanium-connect-unauthorized-code-execution-cve-2026-9207/) | HIGH / エンタープライズ EDR 管理ツール / 低複雑度で実用的な悪用が容易 |
| CVE-2026-35087 | Slican IPx/CCT-1668/MAC-6400/CXS-0424/NCP v6 未満 | CWE-288 / 未採番 | 管理プロトコルで認証検証なしに特定コマンド送信が可能 → 未認証で管理者権限を奪取 | (commit 不明) [(CERT Polska)](https://cert.pl/en/posts/2026/05/CVE-2026-35087/) | CVE-2026-35089 (予測可能キー生成→admin 認証情報) / CVE-2026-35090 (Caller-ID なりすましでモデム遠隔操作) と連鎖し非認証 RCE チェーン構成可 |
| CVE-2026-7452 | Autodesk 3ds Max v2026.3.2 未満 | CWE-119 / 未採番 | 細工した WRL ファイルを 3ds Max でパース → ヒープ破壊 → 現プロセスコンテキストで任意コード実行 | [Autodesk SA adsk-sa-2026-0002](https://www.autodesk.com/trust/security-advisories/adsk-sa-2026-0002) | 同 SA で CVE-2026-7450 (PAR/NULL 参照)/CVE-2026-7451 (TIF/OOB write)/CVE-2026-7453 (WRL/スタック枯渇) が連鎖；製造・映像パイプラインでのファイル共有を経由した標的型侵害に直結 |
| CVE-2026-6815 | Casdoor IAM (修正 PR 提出中) | CWE-22 / 未採番 | 認証済みユーザーが /api/upload-resource の pathPrefix に ../ を渡してストレージサンドボックス外の任意ファイルを上書き → SSH 鍵置換等を経由して RCE へ水平展開 | (PR 審査中) [(JVNVU#98011121)](https://jvn.jp/) | Casdoor は MCP/AI エージェントのアイデンティティ管理基盤として採用事例あり；File Write→ RCE への連鎖が高優先 |
| CVE-2026-35089 | Slican IPx/CCT-1668/MAC-6400/CXS-0424/NCP v6 未満 | CWE-340 / 未採番 | 電話交換機のプロパティ (認証なしで取得可能) からセキュアキーを予測可能な方法で算出 → 非認証でアドミン認証情報を導出 | (commit 不明) [(CERT Polska)](https://cert.pl/en/posts/2026/05/CVE-2026-35087/) | CVE-2026-35087 との連鎖で完全非認証侵害チェーン；同パターンが他の組み込み電話システム実装に水平伝播しやすい設計起因バグ |

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-05-27 | JVNVU#98011121 / CVE-2026-6815 | Casdoor IAM の /api/upload-resource で pathPrefix サニタイズ不足 → 認証済みユーザーが任意ファイル書き込み | HIGH 相当 (未採番) | [JVN](https://jvn.jp/) |
| 2026-05-26 | JVNVU#90845089 (VU#471747) | dnsmasq に DNS キャッシュポイズニング (CVE-2026-2291)・DoS (CVE-2026-4890/4891)・heap 書き込み root 昇格 (CVE-2026-4892) 等 6 件の脆弱性を CERT/CC が公告 | HIGH / SOHO ルーター・Linux ディストリ広範に影響 | [JVN](https://jvn.jp/) |
| 2026-05-26 | JVNVU#96879318 / CVE-2026-3059/3060 | SGLang AI 推論フレームワークの ZMQ ブローカー・並列分解モジュールで pickle.loads() を非認証デシリアライゼーション → 未認証 RCE (CVSS 9.8) | CVSS 9.8 (CRITICAL) / AI 推論インフラ広範に影響 | [JVN](https://jvn.jp/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 30+（WebSearch 25+ クエリ、WebFetch 試行 15+）
- 採用件数: AI=6 / Security=7 / CVE=6 / 国内=3
- 除外理由内訳:
  - 古すぎ (window 外 < 2026-05-26): CVE-2026-48710 BadHost Starlette (X41 advisory 5/22) / CVE-2026-20182 Cisco SD-WAN (5/14) / CVE-2026-23918 Apache HTTP/2 (5/4) / CVE-2026-33701 OpenTelemetry RMI RCE (3/23) / CVE-2026-40369 Windows kernel EoP (5/12 Patch Tuesday) / DAEMON Tools supply chain (5/5-6) / "2026: Year of AI-Assisted Attacks" (5/4) / Mandiant M-Trends 2026 (3/24) / 90-day disclosure policy dead (5/12) / Anthropic Managed Agents update (5/19) / NVIDIA agent skills verification (5/19) / Palo Alto Defender's Guide May update (5/13) / dnsmasq 6 CVEs 初報 (oss-security 5/11)
  - 重複 (excluded_set 直近7日): SharePoint CVE-2026-45659 / NEC Aterm CVE-2026-8652/6059 / KnowledgeDeliver CVE-2026-5426 (野外悪用) / MuddyWater DLL サイドローディング / Check Point 2026 Cloud Report / CERT-In AI 攻撃ブループリント / Verizon DBIR 2026 [続報] / MFA Prompt Bombing / CVE-2026-48172 LiteSpeed 初報 (5/25) / CVE-2026-9082 Drupal KEV (5/22) / TrapDoor CLAUDE.md supply chain (5/25) / Ghost CMS CVE-2026-26980 [続報] (5/25) / Lazarus RemotePE RAT (5/25) / Anthropic $30B [続報] (5/22) / Pope Leo XIV AI encyclical (5/25) / CVE-2026-42897 Exchange XSS / TanStack supply chain (5/11) / Project Glasswing Anthropic Mythos (5/22)
  - 日付不明/確認不可: CVE-2026-27740 Discourse AI LLM XSS (公開日未確認) / TanStack "hits OpenAI employee devices" (続報日付確認不可)
- 取得失敗ソース: thehackernews.com (403) / bleepingcomputer.com (403) / jvn.jp (403) / anthropic.com/news (403) / securityweek.com (403) / cert.pl (403) / helpnetsecurity.com (403) / siliconangle.com (403) — WebSearch スニペット・サードパーティ記事で内容・日付を補完
- 備考: CVE-2026-48172 LiteSpeed は excluded_set (5/25 初報) のため CVE テーブルから除外し、CISA KEV 追加 (5/26) の事実を [続報] としてセキュリティニュースに掲載。SymJack は CVE 未採番のため CVE テーブルから除外し AI/セキュリティニュース欄で記述。

</details>
