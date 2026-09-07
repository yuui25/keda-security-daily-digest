# KEDA Daily Digest — 2026-09-08 (JST)

> 採用範囲: 公開日 2026-09-06 〜 2026-09-08
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Microsoft September 2026 Patch Tuesday（9/8 リリース）は件数こそ 9 件と少ないが全件 Critical で、Azure Arc EoP（CVE-2026-65816 / CVE-2026-69555）と Exchange Online EoP（CVE-2026-65801）がいずれも CVSS 10.0 を記録した（いずれもサーバーサイド修正済み・顧客操作不要）。AI 面では OpenAI が「自動化研究インターン」マイルストーンの達成を発表（9/7）し、主任科学者 Pachocki が再帰的自己改善（RSI）実現を「強く予測」しながらも AI スローダウンを呼びかけるという矛盾をはらんだ一日となった。Anthropic が支持しているマサチューセッツ州の 120 日ごと第三者 AI 評価義務化法案（業界最厳格）を OpenAI・Google が反対に回り、AI 規制をめぐる大手間の亀裂が鮮明になった。

## AI 関連ニュース

- **[2026-09-07]** [OpenAI が「自動化研究インターン」マイルストーン到達 — 研究者 1 人日あたり AI エージェント 3.1 日分の作業を処理、月次 API 推論支出 $600+/研究者](https://www.helpnetsecurity.com/2026/09/07/openai-research-automation-intern/) — 8 月中旬時点のデータを開示。2028 年 3 月のフル AI 研究者（実験立案・実施・解釈・次サイクル改善）達成を目標に設定。研究自動化が加速する転換点として業界が注視。 *(Help Net Security / Business Standard)*

- **[2026-09-07]** [OpenAI 主任科学者 Jakub Pachocki が AI スローダウンを呼びかけ — RSI 実現を「強く予測」しながら「現在の速度で責任あるスケーリングを続けられるラボは存在しない」と発言](https://www.business-standard.com/technology/artificial-intelligence/openai-urges-caution-as-ai-development-shows-signs-of-self-improvement-126090700749_1.html) — 現在の GPT 系モデルが後継モデルの研究を支援しており RSI のループが形成中と評価。安全標準の整備と国際協調が整うまでのスローダウンを求めた。 *(Business Standard / The Neuron)*

- **[2026-09-06]** [Simon Willison が OpenAI 研究加速レポートを解説 — AI が AI 研究を加速する再帰的ループの実態、推論コスト急増と研究生産性向上の両面](https://simonwillison.net/2026/Sep/6/research-acceleration-the-view-inside-openai/) — 中間値研究者が API 推論に日額 $600+ を支出しつつエージェント活用率 3.1 日分/人日を達成。「研究加速の中心にいる人々の視点」として LLM セキュリティ観点でも参照価値が高い分析。 *(simonwillison.net)*

- **[2026-09-07]** [Anthropic が OpenAI・Google と対立、マサチューセッツ州 AI 安全規制（120 日ごと第三者評価義務化）を単独支持 — OpenAI・Google は年次監査の Illinois 型を推奨](https://cryptobriefing.com/openai-google-oppose-massachusetts-ai-safety-rules/) — マサチューセッツ州上院が 7 月末に可決した経済開発法案（AI 条項）が二院間交渉中。Anthropic は $120K 超の政治献金も実施。大手間の規制観のずれが初めて対外的に明確化した事例。 *(The Information / CryptoBriefing / PYMNTS)*

- **[2026-09-06]** [[続報] GPT-6 Astra が Code Arena WebDev で首位達成 — Claude Fable 5.1 を 35 ポイント上回る 1,797 点（Elo）、650K 票超で確定](https://cryptobriefing.com/openai-gpt6-astra-tops-code-arena/) — 9/3 リリース後わずか 3 日で首位。同一価格帯（出力 $40/M）でのウェブ開発タスク性能差が可視化された。フロントエンドコーディングはモデル評価の新主戦場。 *(CryptoBriefing)*

- **[2026-09-04] (Catch-up)** [Nscale が Anthropic との $45B コンピュート契約完了後に契約収益 $103B を公表 — IPO 前に $3.5B 追加調達を目指す NVIDIA バックの英国 AI インフラ企業](https://sg.finance.yahoo.com/news/nscale-doubles-contracted-revenue-103-222526129.html) — 前回公表 $51B から倍増（平均契約期間 5.7 年、年率換算 $18B）。Stargate や MS・Google とは独立した第三のクラウド AI インフラ枠として投資家に提示。9/4 時点で今月 IPO を目指すと報道。 *(The Information / Yahoo Finance / Quartz)*

- **[2026-09-02] (Catch-up)** [GitSpawn — Manifold Security が CLI AI コーディングエージェント 7 製品の .git/config core.fsmonitor 乗っ取り RCE を開示、4 件未修正](https://thehackernews.com/2026/09/malicious-git-configs-can-make-claude.html) — 悪意あるリポジトリを開くだけで git status がトリガーされ任意コードをユーザー権限でサンドボックス外実行。Claude Code / OpenAI Codex / Cursor / Goose / Hermes Agent / Qwen Code / Grok Build が影響。Codex と Cursor はパッチ済み、残り 4 件は未修正（9/2 時点）。 *(The Hacker News / Manifold Security Blog)*

## セキュリティ関連ニュース

- **[2026-09-08]** [Microsoft September 2026 Patch Tuesday — 9 件全件 Critical、Azure Arc EoP × 2（CVSS 10.0）・Exchange Online EoP（CVSS 10.0）・Windows RDP Client 情報漏えい（CVE-2026-50376）含む](https://senserva.com/patch-tuesday-2026-09.html) — Azure Arc / Exchange Online の 3 件はサーバーサイド修正済みで顧客操作不要。全件で公開前の開示なし・野外悪用なし（9/8 時点）。件数は少ないが Critical 比率 100% は異例。 *(Senserva / Trinetri / Microsoft MSRC)*

- **[2026-09-06]** [Roundcube 1.6.19 / 1.7.4 が 12 件修正 — ゼロクリック Stored XSS（TNEF MIME タグ→添付 URL 注入）・SSRF バイパス・メールヘッダーインジェクション 3 件を含む大型セキュリティアップデート](https://roundcube.net/news/2026/09/06/security-updates-1.6.19-and-1.7.4) — CVE 未採番。HTML メールレンダリング・CSS サニタイズ・添付ファイル処理・アドレス帳・URL バリデーション全領域に分散。1.6.x LTS と 1.7.x 両ブランチのユーザーは即時アップグレードを推奨。 *(Roundcube.net / GBHackers)*

- **[2026-09-07]** [Manacle Technologies Multi-tenant ERP System に未認証ファイルアップロード RCE（CVE-2026-84147, CVSS 10.0）ほか IDOR（CVE-2026-84148）・.git 公開（CVE-2026-84149）の 3 件が開示](https://www.ionix.io/threat-center/cve-2026-84147/) — API エンドポイントが認証・ファイルタイプ検証を欠落 → Web アクセス可能ディレクトリへの任意ファイル配置 → RCE。SaaS 型 ERP の供給チェーン全体への影響が懸念される。 *(IONIX / OffSeq Threat Radar)*

- **[2026-09-07]** [Advantech WISE-6610 産業用 IoT ゲートウェイにコマンドインジェクション 2 件（CVE-2026-79697 / CVE-2026-79698, CVSS 9.9）— 公開 PoC あり](https://vuldb.com/vuln/399512) — basicstation_apply（LTE 基地局証明書削除ハンドラ）と nodered_lib_apply（Node-RED ライブラリ）の act 引数処理に認証なしでコマンドを注入可能。Firmware 1.2.4_20260821 でパッチ済み。ICS 環境での即時更新を推奨。 *(VulDB / OffSeq / TheHackerWire)*

- **[2026-09-03] (Catch-up)** [Broadcom が VMware Workstation / Fusion の VM 脱出バグ CVE-2026-59346（CVSS 9.3）を修正 — VMXNET3 整数オーバーフローでゲスト管理者権限からホスト OS 上で任意コード実行（VMSA-2026-0007）](https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/38288) — Workstation / Fusion 25H2・26H1 が対象。ワークアラウンドなし、26H1u1 へのアップデートが必須。ZDI 経由で複数研究者が独立報告。 *(SecurityAffairs / SecurityWeek)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 today-2 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先
> ※ CVE-2026-59346 (Sep 3 公開)・GitSpawn/CVE-2026-72718 (Sep 1-2 公開) は採用窓外だが過去ダイジェスト未収録のためキャッチアップ採用

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-65816 | Microsoft Azure Arc (全テナント) | CWE-706 / CVSS 10.0 | 未認証ネットワーク攻撃者が不正解決される名前参照を経由して Azure Arc の権限ロジックをバイパス → 特権昇格 → テナント管理権限取得 | サーバーサイド修正済み (顧客操作不要) / [Sep 2026 Patch Tuesday](https://msrc.microsoft.com/) | CVSS 10.0 / Sep 8 Patch Tuesday / 顧客操作不要のため実質リスクは低 |
| CVE-2026-69555 | Microsoft Azure Arc (全テナント) | CWE-285 / CVSS 10.0 | 未認証ネットワーク攻撃者が誤った認可ロジックを利用して Azure Arc に権限昇格 → テナント管理権限取得 | サーバーサイド修正済み / [Sep 2026 Patch Tuesday](https://msrc.microsoft.com/) | CVSS 10.0 / Azure Arc EoP 同類は Entra ID・Azure PIM 等へのバリアント調査候補 |
| CVE-2026-65801 | Microsoft Exchange Server Online | CWE-? / CVSS 10.0 | 未認証ネットワーク攻撃者が Exchange Online の認可バイパスを誘発 → メール管理権限・テナント全メールボックスへのフルアクセス | サーバーサイド修正済み / [Sep 2026 Patch Tuesday](https://msrc.microsoft.com/) | CVSS 10.0 / Exchange Online EoP はハイバリュー標的 / 顧客操作不要 |
| CVE-2026-84147 | Manacle Technologies Multi-tenant ERP (修正版以前) | CWE-434 / CVSS 10.0 | 未認証攻撃者が API エンドポイントに認証・ファイルタイプ検証なしでファイルをアップロード → Web 公開ディレクトリに PHP 等の実行ファイルを配置 → RCE・テナント全データ窃取 | (commit 不明) / [IONIX advisory](https://www.ionix.io/threat-center/cve-2026-84147/) | CVSS 10.0 / 未認証 / SaaS ERP 供給チェーン影響 / CVE-2026-84148 (IDOR) と連鎖可能 |
| CVE-2026-79697 | Advantech WISE-6610-NB/EB/TB/JB/CB/EL/P (firmware ≤ 1.2.1_20251110) | CWE-77 / CVSS 9.9 | ネットワーク到達可・認証不要の攻撃者が basicstation_apply の act 引数にシェルメタ文字を注入 → LTE 基地局制御デーモンが root 権限でコマンドを実行 → 完全な IoT ゲートウェイ制御 | [firmware 1.2.4_20260821](https://vuldb.com/vuln/399512) | CVSS 9.9 / 公開 PoC / ICS/IoT 産業制御環境 / 同類 basicstation 実装への水平バリアント候補 |
| CVE-2026-79698 | Advantech WISE-6610-NB 等 (firmware ≤ 1.2.1_20251110) | CWE-77 / CVSS 9.9 | ネットワーク到達可・認証不要の攻撃者が nodered_lib_apply の act 引数を操作 → Node-RED ライブラリハンドラが OS コマンドとして実行 → ゲートウェイ全制御・センサーデータ改ざん | [firmware 1.2.4_20260821](https://vuldb.com/vuln/399513) | CVSS 9.9 / Node-RED を使用する他 IoT プラットフォームへのバリアント候補 |
| CVE-2026-59346 (Catch-up) | VMware Workstation 25H2/26H1・Fusion 25H2/26H1 (macOS) | CWE-190 / CVSS 9.3 | ゲスト VM 管理者権限の攻撃者が VMXNET3 仮想 NIC に細工パケットを送信 → 整数オーバーフローでヒープ破壊 → ホスト OS 上で任意コード実行（VM エスケープ）、ワークアラウンドなし | [VMware Workstation/Fusion 26H1u1 (VMSA-2026-0007)](https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/38288) | CVSS 9.3 / VM エスケープ / ZDI 経由複数研究者報告 / VMXNET3 は vSphere にも存在しバリアント調査推奨 |
| GitSpawn / CVE-2026-72718 (Catch-up) | Block AI Goose ≤ 1.41.0 (他: Claude Code・Codex・Cursor・Hermes Agent・Qwen Code・Grok Build も同クラスに影響、4 件未採番) | CWE-78 / CVSS 7.0 | 悪意あるリポジトリの .git/config に core.fsmonitor=<attacker command> を設定 → エージェントがリポジトリ開封時に git status を実行 → サンドボックス外でユーザー権限の任意コマンドを実行（承認プロンプトなし） | [Goose 1.44.0](https://github.com/block/goose/releases) / Codex・Cursor はパッチ済み / 他 4 件未修正 | AI コーディングエージェント 7 製品影響 / 開発環境の SSH 鍵・AWS 認証情報を標的 / VS Code は 2021 年に同クラスを修正済み→未修正エージェントへの水平バリアント最優先 |

## 国内脆弱性・インシデント情報

> 直近2日間（2026-09-06〜2026-09-08）に該当する新規 JVN/JPCERT/IPA アドバイザリは確認できませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 20+（Help Net Security, Business Standard, The Neuron, simonwillison.net, The Information, CryptoBriefing, PYMNTS, Yahoo Finance/The Information, Roundcube.net, GBHackers, IONIX, OffSeq Threat Radar, VulDB, TheHackerWire, Senserva, Trinetri, Microsoft MSRC, SecurityAffairs, SecurityWeek, Manifold Security / The Hacker News, CSA Daily Briefings, vuldb.com, JVN/JPCERT/IPA 各サイト）
- 採用件数: AI=7 / Security=5 / CVE=8 / 国内=0
- 除外理由内訳:
  - 重複 (excluded_set 該当): StyleSmuggler/Magento (09-07 digest 済み)、CVE-2026-84352/84353 Chrome UAF (09-07 digest 済み)、CVE-2026-67276/86060 MikroTick (09-07 digest 済み)、CVE-2026-75754 ASUS ACC (09-07 digest 済み)、CVE-2026-19490 Citrix NetScaler (09-07 digest 済み)、'Model fatigue' CNBC (09-07 digest 済み)、米中 AI 安全対話 (09-07 digest 済み)、EU AI Act 9 月本格始動 (09-07 digest 済み)、Rhysida Berlin 5.8TB (09-07 digest 済み)、Aurora ransomware / Cursor AI (09-02 digest 済み)、CVE-2026-85042/47/50 Chrome Sep 4 (09-06 digest 済み)、CVE-2026-18658 IBM ODM (09-06 digest 済み)、CVE-2026-6471 PostGREShell (09-06 digest 済み)、FalconFlank CrowdStrike (09-06 digest 済み)、CVE-2026-85046 Chrome V8 zero-day (09-05 digest 済み)、CVE-2026-49869 Kestra (09-04 digest 済み)、CVE-2026-9586 Sangoma (09-04 digest 済み)、Claude Fable 5.1 / Mythos 5.1 発表 (09-03 digest 済み)
  - 窓外（< 2026-09-06）でキャッチアップ除外: CVE-2026-84134 Mozilla Firefox CVSS 9.8 (Sep 1 公開 / 09-03 digest 窓内で既収録の可能性高い)、CVE-2026-69836 Microsoft Entra ID CVSS 10.0 (Aug 21 公開・Aug 21 にサーバーサイド修正済み / 09-07 digest 以前の窓内だが未収録)
  - キャッチアップ採用（採用窓外だが過去ダイジェスト未収録）: CVE-2026-59346 VMware VM 脱出 (Sep 3 公開)、GitSpawn/CVE-2026-72718 Goose 他 AI エージェント (Sep 1-2 公開)、Nscale $103B 契約収益 (Sep 4 公開)
  - 日付不明・確認不可: OpenAI "An Alien Mind" 投稿の正確な公開日（URL 確認済みだが本文取得不可）、マサチューセッツ AI 安全法案の最新進展の正確日付（大枠 Sep 6-8 想定だが一部 Aug 末の情報も混在）
- 取得失敗ソース（EGRESS_BLOCKED）: thehackernews.com, helpnetsecurity.com, securityweek.com, simonwillison.net, cryptobriefing.com, cybersecuritynews.com, bleepingcomputer.com, manifold.security, trinetriops.com, zecurit.com, senserva.com, cvebrief.com, vibe-eval.com, labs.cloudsecurityalliance.org, finance.yahoo.com, business-standard.com（WebSearch スニペット・アクセス可能ミラーサイト経由で情報補完）

</details>
