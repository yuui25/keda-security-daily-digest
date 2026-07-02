# KEDA Daily Digest — 2026-07-03 (JST)

> 採用範囲: 公開日 2026-07-01 〜 2026-07-03 (JST)
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Check Point が DeepSeek に機能するブラウザランサムウェアを生成させることに成功し「フロンティア AI による攻撃自動化」の閾値が現実化、Unit 42 は LLM 幻覚ドメインを攻撃者が先取り登録して AI エージェント経由でフィッシングを展開する「Phantom Squatting」を公表した。セキュリティ面では Microsoft SharePoint CVE-2026-45659 が CISA KEV に追加 (連邦機関修正期限 7/4)、Adobe ColdFusion に CVSS 10.0 × 6件が同日公開され、Citrix NetScaler は CitrixBleed-系メモリ開示 CVE-2026-8451 を含む 6 件をパッチ。CVE テーブルでは Rancher Fleet のマルチテナント K8s 分離バイパス (CVE-2026-44935、CVSS 9.9) と Mautic の Twig SSTI (CVE-2026-9558、CVSS 9.9) が特に高リスク。

---

## AI 関連ニュース

- **[2026-07-01]** [DeepSeek がブラウザ限定の機能するランサムウェアを生成 — Chrome File System Access API でローカルファイルを暗号化](https://research.checkpoint.com/2026/browser-only-ransomware-from-llm-hallucinations-to-a-practical-attack-technique/) — Check Point が DeepSeek に依頼してブラウザ内で動作する完全機能のランサムウェアを生成; File System Access API でフォルダを読み取り・上書きし身代金メモを表示; DeepSeek は Anthropic・OpenAI・Google より悪意ある cyber リクエストへの拒否率が低く「AI が理論的ブラウザランサムウェアを実用攻撃チェーンに昇格させた初例」と評価 *(Check Point Research / The Register)*

- **[2026-07-01]** [Unit 42: Phantom Squatting — LLM が幻覚生成した 250,000 件のブランドドメインを攻撃者が先取り登録](https://unit42.paloaltonetworks.com/phantom-squatting-hallucinated-web-domains/) — 913 ブランドを対象に 685,339 プロンプトを投与し 210 万 URL を分析; 既に 13,229 件が悪意あり分類済み・250,000 件が未登録で攻撃者に狙われる状態; AI エージェントが権威を持ってリンクを提示する経路を悪用し「ゼロレピュテーション・バイパス」を実現 *(Unit 42 / THN)*

- **[2026-06-30 UTC / JST: 2026-07-01]** [Microsoft: 悪意ある MCP ツール説明 (tool poisoning) で AI エージェントが企業データを漏洩](https://thehackernews.com/2026/06/microsoft-warns-poisoned-mcp-tool.html) — Microsoft Incident Response が公開したガイダンスで、攻撃者が MCP tool description に隠し命令を埋め込み → エージェントが通常承認済みのツール呼び出しで請求書等を外部転送; 単一の汚染 OSS リポジトリが数千エンタープライズエージェントに連鎖するサプライチェーンリスクを警告 *(Microsoft Incident Response / THN)*

- **[2026-07-01]** [Apple が AI エクスプロイト加速を理由に iOS/iPadOS/macOS 26.5.2 を前倒し公開](https://www.techtimes.com/articles/319418/20260701/ai-exploit-speed-forces-apple-push-29-ios-2652-patches-before-attackers-strike.htm) — AI ツールが脆弱性開示から悪用まで「実質負の時間」に圧縮している (Mandiant 調査: CVE の 28.3% が開示 24 時間以内に悪用) ことを理由に 7 月予定分を前倒し; WebKit 23件含む 29件を修正; Apple は Project Glasswing に参加し Claude Mythos で自社製品の脆弱性を事前発見 *(TechTimes / Forbes / Notebookcheck)*

- **[2026-07-01]** [Apple「Hide My Email」: 1 年以上放置の実アドレス露出バグを 404 Media が再確認](https://www.macrumors.com/2026/07/01/hide-my-email-vulnerability-exposes-real-addresses/) — 研究者 Tyler Murphy が 2025 年 6 月に報告、2026 年 3〜5 月に Apple は「修正済み」と回答したが今月 404 Media が検証で 100% 再現; Apple の次回セキュリティ更新での修正を待つ状態; CVE 未採番 *(MacRumors / 404 Media)*

- **[2026-06-30 UTC / JST: 2026-07-01]** [Qihoo 360 が中国版 Mythos 対抗 AI 脆弱性スキャナー「Tulong Feng」を発表](https://www.forbes.com/sites/the-wiretap/2026/06/30/qihoo-360-the-cyber-giant-behind-chinas-mythos-rival/) — ISC.AI 2026 (北京) で Zhou Hongyi 氏が公開; マルチエージェント群体で脆弱性を協調探索し 3,432 件を検出、105 件が中国規制当局に確認; 制裁対象企業の発見した脆弱性は中国法律上 Beijing に優先報告義務; 第三者ベンチマークは未公開 *(Forbes / The Register / Decrypt)*

- **[2026-07-02]** [White House AI EO の 30 日期限到達: CISA が AI 対応 BOD 義務、Treasury + NSA が脆弱性情報共有クリアリングハウスを設立](https://www.whitehouse.gov/presidential-actions/2026/06/promoting-advanced-artificial-intelligence-innovation-and-security/) — 6/2 署名の EO が規定する 30 日期限が 7/2 に到達; CISA は連邦シビリアン情報システムの AI 防衛加速 BOD 発出義務; Treasury・NSA が産業界・重要インフラ事業者と協働する脆弱性スキャン共有 Clearinghouse を組成; 8/1 には「covered frontier model」事前審査フレームワーク公開予定 *(White House / Government Contracts Law / Wiley)*

---

## セキュリティ関連ニュース

- **[2026-07-01]** [CISA が Microsoft SharePoint Server CVE-2026-45659 (CVSS 8.8) を KEV に追加 — 連邦機関修正期限 7/4](https://thehackernews.com/2026/07/sharepoint-rce-cve-2026-45659-added-to.html) — サイトメンバー権限で認証済み攻撃者が BCS 経由でデシリアライズ RCE が可能; Microsoft は「悪用可能性: 低い」と評価していたが実際に悪用が確認された; SharePoint Server 2016/2019/SE に影響、Microsoft の 5 月パッチで修正 *(THN / BleepingComputer / The Register)*

- **[2026-07-01]** [[続報] CISA が Microsoft Defender BlueHammer (CVE-2026-33825) の KEV エントリをランサムウェア使用に更新](https://www.bleepingcomputer.com/news/security/cisa-windows-bluehammer-flaw-now-exploited-by-ransomware-gangs/) — 4 月のゼロデイ開示・パッチ後 CISA KEV 追加 (4/22)、今月 7/1 に ransomware campaign での利用を確認しエントリを更新; ローカル攻撃者が SAM データベースの読み取りから SYSTEM 権限に昇格; 使用ランサムウェア グループは未確定 *(BleepingComputer / SecurityWeek / Security Boulevard)*

- **[2026-07-01/02]** [Citrix が NetScaler ADC/Gateway 6件の脆弱性をパッチ — CitrixBleed 系 OOB read (CVE-2026-8451) と HTTP/2 Bomb DoS (CVE-2026-13474) が筆頭](https://cyberscoop.com/citrix-netscaler-flaw-cve-2026-8451-citrixbleed/) — CVE-2026-8451 (CVSS 8.8): SAML IDP 設定時に XML パーサーが属性値境界を超えて読み取り → HTTP 応答で制限メモリを返却 (=CitrixBleed-系メモリ漏洩); CVE-2026-13474 (CVSS 8.7): 不正形式 HTTP/2 リクエストで DoS (管理者の手動設定変更も必要); 14.1-72.61 / 13.1-63.18 で修正 *(CyberScoop / SecurityWeek / watchTowr)*

- **[2026-06-30 UTC / JST: 2026-07-01]** [Adobe が ColdFusion に CVSS 10.0 × 6件含む 11 件をパッチ (APSB26-68、Priority 1)](https://thehackernews.com/2026/07/adobe-patches-7-cvss-100-flaws-in.html) — CVE-2026-48276 / CVE-2026-48283 (CWE-434): 未認証のファイルアップロードで任意ファイル実行; CVE-2026-48277 / 48281 / 48316 (CWE-20): 入力バリデーション欠如で未認証 RCE; CVE-2026-48282 (CWE-22): パストラバーサル RCE; ColdFusion 2025 ≤Update 9 / 2023 ≤Update 20 に影響 *(THN / BleepingComputer / GBHackers)*

- **[2026-07-02]** [SUSE Rancher Fleet: Helm Deployer の valuesFrom 未検証 (CVE-2026-44935、CVSS 9.9) で Kubernetes マルチテナント分離が崩壊](https://cyberpress.org/rancher-fleet-flaw/) — GitRepo の Owner 権限テナントが fleet.yaml の `valuesFrom` で隣接テナントの任意 Namespace の Secret/ConfigMap を参照可能; fleet-agent の cluster-admin クレデンシャルで解決されるため RBAC を完全回避; 4 月公開の CVE-2026-41050 と合わせて 2 経路でマルチテナント K8s 全体が侵害対象 *(Cyberpress / DailyCVE / GBHackers)*

- **[2026-07-02]** [Mautic オープンソース MA に Critical SSTI (CVE-2026-9558、CVSS 9.9) 含む 5 件の GHSA が同時公開](https://www.thehackerwire.com/mautic-critical-ssti-cve-2026-9558-allows-rce/) — テーマエンジンが Twig テンプレートをサンドボックスなしでレンダリング → テーマアップロード権限を持つ認証済みユーザーが RCE; CVE-2026-9559 (CWE-22、Critical): キャンペーンインポートでのパストラバーサル RCE; さらに API v2 認証バイパス (CVE-2026-9808)・SQL インジェクション (CVE-2026-4776、High) も同時公開; Mautic Community 7.1.2 で修正 *(TheHackerWire / GitHub GHSA)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-07-01 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-45659 | Microsoft SharePoint Server 2016/2019/SE (May 2026 パッチ未適用) | CWE-502 / **8.8** | サイトメンバー権限の認証済み攻撃者が BCS 機能経由で信頼されていないデータをデシリアライズ → Server 上で任意コード実行 | [Microsoft May 2026 Update](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-45659) | **CISA KEV 2026-07-01 追加** / FCEB 機関修正期限 7/4 / 実悪用確認済 |
| CVE-2026-8451 | Citrix NetScaler ADC/Gateway (SAML IDP 設定時) < 14.1-72.61 / 13.1-63.18 | CWE-125 / **8.8** | SAML IDP モード時の XML パーサーが属性値の境界を超えて読み取り → HTTP レスポンスに制限メモリ内容 (セッション/トークン) を漏洩 (CitrixBleed 系) | [NetScaler 14.1-72.61 / 13.1-63.18](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX696604) | 2026-07-01 Citrix パッチ / 未認証 / SAML IDP 利用環境は即時適用 / CVE-2023-4966 (CitrixBleed 初代) バリアントとして IDP 実装全般にバリアントハント推奨 |
| CVE-2026-13474 | Citrix NetScaler ADC/Gateway (HTTP/2 有効時) < 14.1-72.61 / 13.1-63.18 | CWE-401 / **8.7** | 不正形式の HTTP/2 リクエストを受信 → HTTP profile の timeout パラメーターがデフォルト値のままだとメモリが解放されず枯渇 → サービス全体の DoS | [NetScaler 14.1-72.61 (同バッチ)](https://support.citrix.com/support-home/kbsearch/article?articleNumber=CTX696604) | 2026-07-01 Citrix パッチ / 未認証 / HTTP/2 有効インスタンス全般 / 手動の timeout 設定変更も必要 |
| CVE-2026-48276 + CVE-2026-48283 | Adobe ColdFusion 2025 ≤Update 9 / 2023 ≤Update 20 | CWE-434 / **10.0** | 未認証リモート攻撃者がファイルアップロードエンドポイントに細工ファイルを送信 → 拡張子バリデーション欠如によりサーバー上でファイルが実行 → 完全 RCE | [ColdFusion 2025 Update 10 / 2023 Update 21 (APSB26-68)](https://helpx.adobe.com/security/products/coldfusion/apsb26-68.html) | 2026-07-01 Adobe Priority 1 公開 / CVSS 10.0 × 6件 / 未認証 / 公開済み ColdFusion インスタンスは即時パッチ; 同CWE-434 は他 ColdFusion エンドポイントへのバリアントハント推奨 |
| CVE-2026-44935 | github.com/rancher/fleet (Go) (fleet ≤0.15.1 / ≤0.14.5 / ≤0.13.10 / ≤0.12.14) | CWE-863 / **9.9** | Helm Deployer の `fleet.yaml` における `valuesFrom` Secret/ConfigMap 参照が fleet-agent の cluster-admin 権限で解決 → tenant RBAC を完全バイパスして任意 Namespace の Secrets に横断アクセス → K8s クラスター全体の認証情報漏洩 | [fleet v0.15.2 / v0.14.6 / v0.13.11 / v0.12.15](https://github.com/rancher/fleet/releases) | 2026-07-02 GHSA 公開 / CVSS 9.9 / GitRepo Owner 権限のみで成立 / マルチテナント K8s 環境 (特に Rancher 利用組織) は即時アップグレード |
| CVE-2026-9558 / GHSA-9fx4-7cmj-47vg | Mautic Community < 7.1.2 | CWE-94 / **9.9** | テーマ作成・アップロード権限を持つ認証済みユーザーが悪意ある Twig テンプレートをアップロード → エンジンがサンドボックス・関数制限なしにレンダリング → サーバー側で任意コード実行 (RCE) | [Mautic Community 7.1.2 (GHSA-9fx4-7cmj-47vg)](https://github.com/mautic/mautic/releases/tag/7.1.2) | 2026-07-02 GHSA 公開 / CVSS 9.9 / 認証済み (低権限) で RCE / 同 Twig サンドボックスバイパスパターン (CVE-2026-48806〜08 系) の他 PHP テンプレートエンジン実装へバリアントハント推奨 |
| CVE-2026-50143 / GHSA-6gr2-qh89-hxwm | @apify/actors-mcp-server (npm) ≤ 0.x (修正版で対応) | CWE-20 / **High** | MCP サーバーが Actor 定義から取得した `webServerMcpPath` を検証なしに信頼済みベース URL に連結 → path authority injection で攻撃者制御パスが前段に挿入 → Apify API トークンが攻撃者の Actor インスタンスに転送され Apify アカウント全体の権限を取得 | [@apify/actors-mcp-server 修正版 (GHSA 参照)](https://github.com/advisories/GHSA-6gr2-qh89-hxwm) | 2026-07-01 GHSA 公開 / AI/MCP インフラの API トークン窃取 / Actor 定義が攻撃ベクター → MCP サーバーの Actor 取得・URL 結合ロジック全般へバリアントハント推奨 |
| CVE-2026-49998 | Centrifugo < v6.7.0 (Go) | CWE-287 / **High** | 動的 JWKS エンドポイント設定時にキャッシュが `kid` (Key ID) のみで管理 → 攻撃者がテナント A の秘密鍵で `iss` をテナント B に設定した JWT を生成し同一 `kid` でテナント A の公開鍵でヒット → 署名検証が成功しテナント B として認証される (クロスイシュア JWT バイパス) | [Centrifugo v6.7.0](https://github.com/centrifugal/centrifugo/releases/tag/v6.7.0) | 2026-07-01 GHSA 公開 / マルチテナント JWKS 認証実装の全般的なパターン欠陥 / Go/Node.js 等の他 WebSocket サーバーの `kid`-indexed JWKS キャッシュへバリアントハント推奨 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-07-01 | JVNVU#94872523 | Seiko Solutions SkyBridge MB-A100/MB-A110 および SkyBridge BASIC MB-A130 に OS コマンドインジェクション — 細工されたリクエストで認証不要のリモート攻撃者が任意コマンドを実行可能; Ver. 4.2.3 以降 (MB-A100/A110) と Ver. 1.5.7 以降 (MB-A130) が対象; ベンダーによる修正版対応済 | CVSS 9.8 / 高 (AV:N/AC:L/PR:N/UI:N) | [JVN](https://jvn.jp/en/vu/JVNVU94872523/) |

> 2026-07-01〜07-03 (JST) 期間中、新規国内インシデント公表 (新種侵害・データ漏洩等) は主要ソースで確認できませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| thehackernews.com (July 2026 filter) | SharePoint CVE-2026-45659 KEV, Adobe ColdFusion APSB26-68, Phantom Squatting, DeepSeek browser ransomware, Citrix NetScaler 6 flaws, Mautic SSTI batch 取得 (403 → WebSearch スニペット代替) ✓ |
| socradar.io / bleepingcomputer.com / cybersecuritynews.com | SharePoint CVE-2026-45659, BlueHammer ransomware CISA update 確認 ✓ |
| cyberscoop.com / securityweek.com | Citrix NetScaler CVE-2026-8451/CVE-2026-13474 詳細確認 ✓ |
| Check Point Research / theregister.com | DeepSeek browser ransomware (2026-07-01) 確認 ✓ |
| unit42.paloaltonetworks.com / thehackernews.com | Phantom Squatting (2026-07-01) 確認 ✓ |
| microsoft.com / thehackernews.com (June 30) | MCP tool poisoning warning 確認 ✓ |
| macrumors.com / 404media.co | Apple Hide My Email (2026-07-01) 確認 ✓ |
| techtimes.com / forbes.com / notebookcheck.net | Apple iOS 26.5.2 AI threat justification (2026-07-01) 確認 ✓ |
| forbes.com / theregister.com (June 30) | Qihoo 360 Tulong Feng (JST: 2026-07-01) 確認 ✓ |
| whitehouse.gov / governmentcontractslaw.com | White House AI EO July 2 deadline 確認 ✓ |
| github.com/advisories (July 1-2 filter) | CVE-2026-44935 (Rancher Fleet), CVE-2026-9558/9559 (Mautic batch), CVE-2026-50143 (Apify MCP), CVE-2026-49998 (Centrifugo) 取得 ✓ |
| dailycve.com | Apify MCP GHSA-6gr2-qh89-hxwm, Centrifugo CVE-2026-49998, Rancher Fleet CVE-2026-44935 補完 ✓ |
| jvn.jp (July 1 filter) | JVNVU#94872523 Seiko SkyBridge 取得 (403 → WebSearch スニペット代替) ✓ |
| bleepingcomputer.com / prsol.cc | BlueHammer ransomware CISA update (2026-07-01) 確認 ✓ |
| nvd.nist.gov / cisa.gov/kev | 403 → WebSearch スニペットで代替確認 |

### 集計サマリ

- **巡回ソース数**: 20+
- **採用件数**: AI=7 / Security=6 / CVE=8 / 国内=1
- **除外理由内訳**:
  - 古すぎ (今日-2 = 2026-07-01 より前): Qihoo 360 発表 (6/24)・The Register 報道 (6/26)、n8n CVE-2026-21858 (Jan 2026 発表)、Oracle CVE-2026-21992 (Mar 2026)、Rancher Fleet CVE-2026-41050 GHSA 公開日 (Apr 30)、Grok 4.3 on Bedrock (Jun 15)、Sysdig LLMjacking VAPT (Jun 12)、LLMjacking Ollama/LiteLLM キャンペーン (Mar-May 2026)、Apple iOS 26.5.2 リリース自体 (Jun 29 UTC)、White House AI EO 署名 (Jun 2)
  - 重複 (直近 7 ダイジェスト excluded_set): Claude Sonnet 5 / Fable 5 復旧 (07-02 掲載済み)、DuneSlide CVE-2026-50548/50549 (07-02)、Kemp LoadMaster CVE-2026-8037 (07-02)、Langflow CVE-2026-33017 (07-02)、SurrealDB GHSA-4vgr/GHSA-wjjj (07-02)、repomix CVE-2026-49987 (07-02)、BioShocking LayerX (07-02)、Fulcio CVE-2026-49478 (07-01)、Woodpecker CI CVE-2026-58370 (07-01)、Twig CVE-2026-48806/48807/48808 (07-01)、SimpleHelp CVE-2026-48558 / Djinn Stealer (06-30/07-01)、Oracle EBS CVE-2026-46817 (06-30)、MCP Toolbox CVE-2026-11720 (06-30)、Gorse/SigNoz/Mythic/Nitter 各CVE (06-30)、Aflac Japan 漏洩 (07-01)、RPG Maker JVNDB-2026-000093 (07-02)
  - 日付不明: 0件
  - 採用窓内だが内容不十分: Adobe Campaign Classic CVE (詳細不足)、Mautic SQL injection CVE-2026-4776 (July 2 GHSA だが詳細確認未了)、Zebra ノード批(Zcash consensus 特化で影響範囲限定)
- **取得失敗ソース**: thehackernews.com (403)、bleepingcomputer.com (403)、securityweek.com (403)、jvn.jp (403)、unit42.paloaltonetworks.com (403)、nvd.nist.gov (403)、cisa.gov/kev (403) — 全て WebSearch スニペットおよびミラーサイトで代替確認済み

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-06-26 〜 2026-07-02) の全 CVE/GHSA/URL を除外済み。*
