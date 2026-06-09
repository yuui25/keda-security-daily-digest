# KEDA Daily Digest — 2026-06-10 (JST)

> 採用範囲: 公開日 2026-06-08 〜 2026-06-10
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Anthropic が 2 ヶ月のガードレール検証を経て Claude Fable 5 (初の一般公開 Mythos クラス) を June 9 にリリース — Firefox 271 脆弱性発見と同アーキテクチャながら、サイバーセキュリティ・生物・化学クエリを Opus 4.8 にフォールバックさせる多層ガードレールを搭載し、Anthropic 自身の「AI 一時停止提案」公開からわずか 4 日後の公開として安全論争を呼んだ。同日 Microsoft June Patch Tuesday には前日 digest が「ゼロデイ 0 件」と報告したのに対し実際は 3 件 (BitLocker 物理バイパス CVE-2026-50507/YellowKey・CTFMON EoP CVE-2026-45586/GreenPlasma・HTTP/2 Bomb CVE-2026-49160) が含まれていたことが複数媒体の詳報で判明。SAP も CVSS 9.9 の SAML 署名検証欠落 (CVE-2026-44748) を含む 4 件の HotNews を同日公開し、Veeam Backup & Replication ドメインユーザー RCE (CVE-2026-44963, CVSS 9.4) のパッチも出た。

---

## AI 関連ニュース

- **[2026-06-09]** [Anthropic が Claude Fable 5 (公開向け Mythos クラス) と Claude Mythos 5 (検証済みパートナー限定) を正式リリース — 「Firefox 271 脆弱性発見モデル」と同アーキテクチャをガードレール付きで一般公開; Pro/Max/Team/Enterprise は 6/22 まで追加課金なし; 価格 $10/$50 per M tokens; API は Amazon Bedrock・Vertex AI・Microsoft Foundry で即日提供](https://www.anthropic.com/news/claude-fable-5-mythos-5) *(anthropic.com / Fortune / SecurityWeek)*

- **[2026-06-09]** [TechCrunch「Anthropic が『AI が過度に危険』と警告した 4 日後に最強モデルを公開」— 6/5 の AI 開発一時停止提案論文からわずか 96 時間でリリース; 独立評価では「単一ターン有害要求の遵守ゼロ件」を確認するも、Fable 5 に共通するアーキテクチャを使えばゼロデイ発見能力が民間に開放される点について研究者からの懸念が上がる](https://techcrunch.com/2026/06/09/anthropic-released-claude-fable-5-its-most-powerful-model-publicly-days-after-warning-ai-is-getting-too-dangerous/) *(TechCrunch)*

- **[2026-06-09]** [Claude が Apple Foundation Models フレームワーク向け Swift パッケージを公開 — iOS/iPadOS/macOS/visionOS/watchOS 27 でオンデバイス AI × Claude の複合推論・コード生成・ストリーミング応答が可能に; WWDC で発表した Apple の「AI Extensions (ChatGPT/Gemini/Claude 切り替え)」技術実装の翌日提供](https://releasebot.io/updates/anthropic) *(anthropic.com / releasebot.io)*

- **[2026-06-09]** [Claude Opus 4.1 API 廃止 (2026-08-05) を発表 — Fable 5 への移行を推奨; API Messages エンドポイントが `system` を `messages` 配列内に受け入れ可能になりプロンプトキャッシュを壊さずに中間指示変更が可能に](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) *(platform.claude.com)*

- **[2026-06-08]** [[続報] Microsoft オープンソースツール群が「再侵害」確認 — 6/5 の Miasma ワーム攻撃後に復旧させた Microsoft Durable Task プロジェクトが再度侵害され AI 開発者パスワードを窃取; 70 超のリポジトリを追加オフライン化。TechCrunch が「Microsoft が初回攻撃でハッカーを完全排除できていなかった可能性」を指摘。Claude Code・Gemini CLI・VS Code 利用者への影響が継続](https://techcrunch.com/2026/06/08/microsofts-open-source-tools-were-hacked-to-steal-passwords-of-ai-developers/) *(TechCrunch)*

- **[2026-06-08]** [Google が SpaceX と AI コンピューティング向け cloud service agreement を締結 — Starlink/Starshield インフラ向けに Google Cloud の AI 処理能力を提供; 軍民デュアルユース AI クラウドインフラの統合加速が安全保障上の新たなリスク面として注目](https://aiproductivity.ai/news/date/2026-06-09/) *(各紙 2026-06-08)*

---

## セキュリティ関連ニュース

- **[2026-06-09]** [[続報] Microsoft June 2026 Patch Tuesday — 実際は 3 件のゼロデイを含む 200 脆弱性修正 (前日 digest「ゼロデイ 0 件」を訂正): CVE-2026-50507 (BitLocker 物理バイパス/YellowKey、Nightmare Eclipse 公開)・CVE-2026-45586 (CTFMON EoP/GreenPlasma、Nightmare Eclipse 公開)・CVE-2026-49160 (HTTP/2 Bomb、Calif 社公開)。加えて Hyper-V VM 脱出 (CVE-2026-47652/45641/45607) 3 件・RDP RCE (CVE-2026-44801/44799) 2 件も Critical 評価](https://www.bleepingcomputer.com/news/microsoft/microsoft-june-2026-patch-tuesday-fixes-3-zero-day-200-flaws/) *(BleepingComputer / CyberSecurityNews / MSRC)*

- **[2026-06-09]** [SAP June 2026 Security Patch Day — 15 セキュリティノートを公開、4 件が HotNews (CVSS 9.1〜9.9): CVE-2026-44748 (NetWeaver SAML XML Signature Wrapping, CVSS 9.9, SAP_BASIS 702〜919 全バージョン) / CVE-2026-27671 (ABAP Kernel RFC メモリ破壊, CVSS 9.8, 非認証 RCE, 回避策なし) / CVE-2026-22732 (Commerce Cloud Spring Security HTTP ヘッダ欠落, CVSS 9.1). 野外悪用は未確認だが国内 SAP ERP 組織は即時パッチ適用が必要](https://securityonline.info/sap-security-patch-day-june-2026/) *(SecurityOnline / SecurityWeek / RedRays / CCB Belgium)*

- **[2026-06-09]** [Veeam Backup & Replication に CVE-2026-44963 (CVSS 9.4) パッチ — ドメイン参加サーバーへの認証済みドメインユーザー RCE; WatchTowr 研究者 Sina Kheirkhah が発見。バックアップサーバーは企業インフラで特権的位置にあり侵害時のランサムウェア展開リスクが高い。v12.3.2.4854 (2026-06-09) で修正](https://www.veeam.com/kb4696) *(BleepingComputer / CyberSecurityNews / Arctic Wolf / Veeam KB4696)*

- **[2026-06-08]** [Linux kernel nf_tables の CVE-2026-23111 に完全動作エクスプロイト公開 (Exodus Intelligence) — !一文字の欠落によるコンテキスト反転 UAF でローカル非特権ユーザーが root 権限取得・コンテナ脱出が可能; 安定性 >99%, 高負荷環境でも 80% 以上。パッチは 2026-02-05 適用済みだが「大半のインフラは 4 ヶ月間再起動されていない」と Exodus が警告](https://thehackernews.com/2026/06/one-character-linux-kernel-flaw-enables.html) *(The Hacker News / Security Affairs / Exodus Intelligence)*

- **[2026-06-09]** [ランサムウェア集中攻撃 (June 9): Akira・TheGentlemen・RansomHouse・NightSpire・Morpheus の 5 グループが医療・航空・IT・製造・警備など 8 組織以上に同日侵害を報告 — 被害組織には米国の Central Arkansas Pediatrics (小児科)・Aegle Aviation・3i Infotech・HRC Sicherheitsdienste (独警備会社) 等を含む。「一日あたり 2,090 件」という 2026 年の攻撃ペースを体現する事例](https://www.breachsense.com/breaches/) *(BreachSense / BlackFog)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-08 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-44748 | SAP NetWeaver AS ABAP および ABAP Platform (SAP_BASIS 702〜919 全バージョン) | CWE-347 / **9.9** | 低権限認証済み攻撃者が有効な SAML 署名済みメッセージを取得 → XML Signature Wrapping で改ざん XML を検証者に送付 → IdP なりすまし・ユーザー属性改ざん・全 SAP システムへの権限昇格 | [SAP Note 3765134](https://support.sap.com/en/my-support/knowledge-base/security-notes-news/june-2026.html) (commit 非公開) | 2026-06-09 公開 / CVSS 9.9 / SAP_BASIS 702〜919 超広範囲 / SAML 検証欠落は Java 系 SP 全般へバリアント展開可 |
| CVE-2026-27671 | SAP Application Server ABAP (KRNL64NUC・KRNL64UC・KERNEL 7.22〜9.19) | CWE-119 / **9.8** | 非認証攻撃者が RFC リクエストに論理的メモリ管理エラーを突いた細工データを送付 → カーネルレベルメモリ破壊 → CIA 完全喪失・任意コード実行。回避策なし | [SAP Note 3748262](https://support.sap.com/en/my-support/knowledge-base/security-notes-news/june-2026.html) (commit 非公開) | 2026-06-09 公開 / **非認証 RCE** / 回避策なし・即時カーネルアップデート必須 / RFC プロトコル実装は他 ERP・S/4HANA 系に水平バリアントあり |
| CVE-2026-44963 | Veeam Backup & Replication ≤12.3.2.4465 (ドメイン参加環境のみ) | CWE-250 / **9.4** (v4) | 認証済みドメインユーザーが VBR のデシリアライズ機構に対するアクセス制御不備を悪用 → バックアップサーバー上で任意コード実行 → バックアップ全滅・ランサムウェア展開の起点化 | [KB4696](https://www.veeam.com/kb4696) (v12.3.2.4854、2026-06-09) | 2026-06-09 公開 / WatchTowr Sina Kheirkhah 発見 / バックアップ基盤は特権的位置 / v13.x は構造変更により非影響 |
| CVE-2026-23111 | Linux kernel ≤6.12 (nf_tables、slab allocator、全ディストリビューション) | CWE-416 / TBD | nf_tables Abort Phase の catchall 要素で条件式に `!` が欠落 → 非特権ローカルユーザーが UAF をトリガー → カーネルベースリーク + ヒープアドレスリーク + ROP chain → root 権限取得・コンテナ脱出。安定性 >99% | [kernel.git upstream 2026-02-05](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/) (patch: `!` の復元1文字修正) | **完全動作 PoC 公開 (2026-06-08)** / Exodus Intelligence / >99% 安定性 / 大量 Linux インフラが 4 ヶ月間未リブートのリスク |
| CVE-2026-45586 | Windows Collaborative Translation Framework (CTFMON、全 Windows バージョン) | CWE-59 / EoP | GreenPlasma エクスプロイト: 認証済みローカル攻撃者が CTF フレームワークのシンボリックリンク追従不備を悪用 → SYSTEM 権限昇格 | [MSRC June 2026 Patch Tuesday](https://msrc.microsoft.com/update-guide/) | **ゼロデイ (公開後パッチ)** / 2026-06-09 修正 / Nightmare Eclipse 研究者が公開 / CVE-2026-50507 と同一研究者・同日開示 |
| CVE-2026-50507 | Windows BitLocker (BitLocker 搭載の全 Windows バージョン) | CWE-693 / 物理バイパス | YellowKey: 物理アクセス攻撃者が USB/EFI パーティションに細工ファイルを配置 → WinRE 起動時に CTRL キー保持 → 制限なしコマンドシェルで BitLocker 暗号化ドライブに完全アクセス | [MSRC June 2026 Patch Tuesday](https://msrc.microsoft.com/update-guide/) | **ゼロデイ (公開後パッチ)** / 2026-06-09 修正 / Nightmare Eclipse 研究者が公開 / 盗難デバイス・オフライン攻撃シナリオに直結 |
| CVE-2026-47652 (+ 45641, 45607) | Windows Hyper-V (Windows Server 2019/2022/2025) | CWE-94 / **Critical** | 悪意あるゲスト VM プロセスが Hyper-V の境界チェック不備を悪用 → ゲストからホストへの VM 脱出 + ホスト上でコード実行 | [MSRC June 2026 Patch Tuesday](https://msrc.microsoft.com/update-guide/) | 2026-06-09 公開 / VM エスケープ 3 件同日パッチ / クラウド・仮想基盤の重要インフラに直接影響 |
| CVE-2026-22732 | SAP Commerce Cloud・SAP Data Hub (Spring Security 6.x を内包するバージョン) | CWE-693 / **9.1** | 特定の Spring Security HTTP セキュリティレスポンスヘッダ設定でヘッダが条件付きで欠落 → 非認証リモート攻撃者が CSRF 保護・HSTS・X-Frame-Options をバイパス → セッション乗っ取り・Clickjacking | [spring.io/security/cve-2026-22732](https://spring.io/security/cve-2026-22732/) | 2026-06-09 公開 / Spring Security 全般の設定依存バグ / SAP 以外の Spring Boot 3.x アプリへも水平バリアント要確認 |
| CVE-2026-47737 | Puma ≥5.5.0 <7.2.1 / ≥8.0.0 <8.0.2 (PROXY Protocol v1 有効環境) | CWE-349 / High | 信頼済みプロキシ経由の攻撃者が持続接続の各 keep-alive リクエスト後に 2 つ目の PROXY ヘッダを注入 → Puma が次リクエストの REMOTE_ADDR を上書き → IP 許可リスト・レート制限・監査ログのバイパス | [github.com/puma/puma v7.2.1 / v8.0.2](https://github.com/puma/puma/releases) | 2026-06-09 公開 / Unicorn・Passenger 等 Ruby 系 App サーバーの同 PROXY Protocol 実装に水平バリアントあり / CVE-2026-47736 (DoS 版、June 8) と同日ペア公開 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|

> 直近2日間 (2026-06-08〜06-10) に該当する新規国内脆弱性・インシデント情報は確認できませんでした。

*備考: JPCERT/IPA/JVN への直接フェッチは引き続き HTTP 403 のため WebSearch 経由で確認。2026-06-08〜10 の JVN 新規アドバイザリは未確認。なお CVE-2026-44748/CVE-2026-27671 は国内 SAP ERP 運用組織に、CVE-2026-44963 は国内 Veeam 利用組織に直接影響するため即時対応が必要。CVE-2026-50507 (BitLocker YellowKey) の 6/12 以降に向けた Windows Update の適用も推奨。*

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 35 ソース (anthropic.com, TechCrunch, Fortune, SecurityWeek, platform.claude.com, BleepingComputer, CyberSecurityNews, SecurityOnline, RedRays, SecurityBridge, CCB Belgium, securityonline.info, The Hacker News, Security Affairs, Exodus Intelligence, Veeam KB, MSRC, Zecurit, CyberInsider, SC Media, SOCRadar, spring.io, RubySec, GitLab Advisories, BreachSense, BlackFog, SaaSCity, digitalapplied.com, wavespeed.ai, releasebot.io, iplogger.org, thecyberthrone.in, heise.de, windowsforum.com, windowsnews.ai 他)
- 採用件数: AI=6 / Security=5 / CVE=9 / 国内=0
- 採用件数が目安 (AI/Security 各 8〜12件) を下回った理由:
  - AI ニュース: 採用窓 (2026-06-08〜10) の大半の主要 AI イベントは前日 (2026-06-09) digest に既収録 (WWDC 2026/Siri 再構築/Apple CEO 交代/OpenAI Lockdown Mode/Pentagon × Anthropic)。新規は Claude Fable 5/Mythos 5 リリース (最大ニュース) と関連 API 展開・Apple Foundation Models パッケージ・Microsoft GitHub 続報の 6 件
  - Security ニュース: 主要セキュリティイベント (Check Point CVE-2026-50751 CISA KEV・Microsoft Patch Tuesday の基本情報・Veeam など) の初報は前日 digest 収録済み。本日は「3 ゼロデイ詳報」「SAP Patch Day」「Veeam パッチ詳細」「Linux nf_tables PoC 公開」「ランサムウェア波」の 5 件
- 除外理由内訳:
  - 古すぎ (< 2026-06-08): CVE-2025-48595 Android Framework zero-day (CISA KEV 2026-06-02 追加・Android bulletin 2026-06-05 公開) / CVE-2026-42824 M365 Copilot info disclosure (2026-06-04) / CVE-2026-45497 M365 Copilot RCE (2026-06-04) / OpenAI TanStack macOS certificate 期限 (May 11 事案、2026-06-02 周知) / ChatGPT 10 億 MAU (2026-06-03 各紙) / Gemini 3.5 Flash GA (2026-05-19) / CVE-2026-45185 Exim GnuTLS UAF (NVD 2026-05-12) / agnt8x EightX Labs AI agent platform (2026-06-08 だが AI セキュリティ無関連のため優先度低・除外)
  - 重複 (excluded_set 直近7日): Check Point CVE-2026-50751/50752 (2026-06-09 digest) / Microsoft Patch Tuesday 基本情報・CVE-2026-42897 Exchange (2026-06-09 digest) / Silent Ransom Group law firms (2026-06-09 digest) / OnlyFans 3.4億件 (2026-06-09 digest) / Trump AI EO・DARPA AI Forge (2026-06-07 digest) / OpenAI Lockdown Mode (2026-06-09 digest) / Apple WWDC 2026 (2026-06-08/09 digest) / Miasma ワーム初回報告 (2026-06-07/08 digest) / SolarWinds Serv-U CVE-2026-28318 (2026-06-08 digest) / CVE-2026-49774 RD Station WP (2026-06-08 digest) / CVE-2026-50589 OpenStack Ironic (2026-06-08 digest)
  - 日付不明/確認不可: Google × SpaceX AI cloud deal の一次ソース URL 未確定 (June 8 各紙報道は確認済み・URL はダイジェスト内にセカンダリ参照で収録)
- CVE 件数: 9件 (目標 5〜10 の上限付近)。注目はパッチ済みだが PoC 公開の CVE-2026-23111 (Linux nf_tables) と、Nightmare Eclipse 研究者が同日公開した BitLocker/CTFMON ゼロデイペア
- 取得失敗ソース (HTTP 403): anthropic.com 記事 / techcrunch.com 個別記事 / fortune.com 個別記事 / securityweek.com 個別記事 / bleepingcomputer.com 個別記事 / cybersecuritynews.com 個別記事 / redrays.io 個別記事 / threat-modeling.com 個別記事 / llm-stats.com / wavespeed.ai / aiproductivity.ai / jpcert.or.jp / jvn.jp — WebSearch スニペット・複数独立媒体の記事で内容・日付を補完
- 備考: 前日 digest (2026-06-09) が Microsoft June Patch Tuesday の「ゼロデイ 0 件」と報告したのは誤報。BleepingComputer・CyberSecurityNews・MSRC 等複数独立ソースが「3 件のゼロデイ」を 2026-06-09 付けで報道。本 digest の [続報] 掲載はこの訂正を目的としている

</details>
