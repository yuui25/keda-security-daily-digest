# KEDA Daily Digest — 2026-08-14 (JST)

> 採用範囲: 公開日 2026-08-12 〜 2026-08-14
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

中国系ハッカーが台湾政府機関に対してイスラエル企業 Dream が確認した史上初のエンド・ツー・エンド自律型 AI エージェントサイバー攻撃を実行し、4日間で21政府システムをマッピング・85アカウントを侵害・2,500件の人事記録を窃取後、原子力安全委員会・7社以上のエネルギー企業に拡大した。AI モデル面では xAI が Grok 4.6、DeepSeek が V4 Pro 0813 をそれぞれ Aug 12/13 にリリースし、エージェント能力競争が加速。セキュリティ面では Microsoft Defender の RoguePlanet パッチを 100% 成功率でバイパスする ShieldBreak (CVE-2026-50656) の PoC が公開されており、Adobe Commerce CVE-2026-71362 の即日野生悪用・ColdFusion CVSS 10.0 の 3 件が同時に対応を迫っている。

---

## AI 関連ニュース

- **[2026-08-12/13]** [China Used AI Agents to Hack Taiwan Government in History's First Autonomous Cyberattack](https://www.cnn.com/2026/08/13/tech/china-taiwan-ai-agent-cyberattack-intl-hnk) — イスラエルのサイバーインテリジェンス企業 Dream が分析した史上初のエンド・ツー・エンド自律型 AI エージェントサイバー攻撃。中国系攻撃者が Hermes + OpenClaw フレームワーク上の 8 エージェントを 4 日間稼働させ、台湾政府21システムをマッピング・85アカウント侵害・人事記録 2,500 件を窃取後、原子力安全委員会および7社以上のエネルギー企業へ横断侵害。人間のオペレーターは指令送信のみで実行全体を AI が完遂 *(CNN 2026-08-13; The Register 2026-08-12)*

- **[2026-08-12]** [xAI Releases Flagship Grok 4.6 Model with Advanced Reasoning Capabilities](https://siliconangle.com/2026/08/12/spacexai-releases-flagship-grok-4-6-model-advanced-reasoning-capabilities/) — xAI が Grok 4.6 を API 提供開始（入力 $2/出力 $6 per million tokens）。最大 500K コンテキスト、xhigh 推論レベルを新設、長期エージェント実行向けに最適化。Artificial Analysis Intelligence Index で GPT-5.6 Sol と同等スコアを記録 *(SiliconAngle; Marktechpost 2026-08-12)*

- **[2026-08-13]** [DeepSeek Releases V4 Pro 0813 with Massive MoE Architecture](https://www.globaltimes.cn/page/202608/1368125.shtml) — DeepSeek V4 Pro 0813 を公開（MIT ライセンス）。1.6T パラメータ MoE / 49B 活性化、1M コンテキスト。CyberGym ベンチマーク 52.7→83.3、DeepSWE 12.8→62.7 へ向上。近日中の価格改定予告あり *(Global Times; Artificial Analysis 2026-08-13)*

- **[2026-08-13]** [Claude Will Now Leave a Watermark on Everything It Writes](https://www.forbes.com/sites/anishasircar/2026/08/13/claude-will-now-leave-a-watermark-on-everything-it-writes-what-does-that-mean/) — Anthropic が EU AI Act 第50条対応として Claude の全テキスト出力に不可視電子透かしを実装（C2PA メタデータは画像向け）。透かしはコピー＆ペースト後も保持、世界展開済み *(Forbes 2026-08-13)*

- **[2026-08-12]** [Google Gemini Reaches 1 Billion Monthly Active Users](https://www.techtimes.com/articles/324095/20260812/gemini-reaches-1-billion-users-subscriber-count-left-out-announcement.htm) — Google Gemini の月間アクティブユーザーが 10 億人到達（Google 製品中最速成長）。音声利用率 63%、画像生成 1.5 億枚/日。有料購読者数は非開示 *(TechTimes 2026-08-12)*

- **[2026-08-13]** [OpenAI Expands ChatGPT Ads to UK, Japan, South Korea, Mexico and Brazil](https://www.ghacks.net/2026/08/13/openai-expands-chatgpt-ads-test-to-uk-mexico-brazil-japan-and-south-korea/) — OpenAI が ChatGPT の広告テストを英・日・韓・墨・伯に拡大。Free/Go プランが対象、広告には明示ラベル付与、広告主への個人情報提供なし。収益多角化の一環 *(gHacks 2026-08-13)*

- **[2026-08-13]** [LiteLLM Breach: 153GB of Stolen Credentials from March 2026 Supply Chain Attack Surface](https://www.helpnetsecurity.com/2026/08/13/litellm-breach-stolen-credentials-leak/) — 2026年3月の TeamPCP による PyPI サプライチェーン攻撃（LiteLLM 1.82.7/1.82.8 を 40 分間汚染）で窃取された認証情報 153GB が犯罪フォーラムに流出。434K CI/CD パイプラインが侵害対象となり、AWS・Cisco・Samsung を含む 2,500 以上の組織に影響 *(Help Net Security 2026-08-13)*

---

## セキュリティ関連ニュース

- **[2026-08-12]** [ShieldBreak: PoC Bypasses Microsoft Defender RoguePlanet Patch with 100% Success Rate](https://arcticwolf.com/resources/blog/cve-2026-50656-rogueplanet-shieldbreak/) — Chaotic Eclipse グループが ShieldBreak として CVE-2026-50656 (RoguePlanet) の公式パッチを完全バイパスする PoC を公開。mpengine.dll の TOCTOU 競合を突き標準ユーザーが NT AUTHORITY\SYSTEM に昇格、Windows 11 25H2 および Server 2025 で 100% 成功率を確認。公式修正はなく Defender がデフォルト有効なため全 Windows 環境が対象 *(Arctic Wolf; BleepingComputer 2026-08-12)*

- **[続報][2026-08-12]** [Sansec Detects Immediate Exploitation of Adobe Commerce CVE-2026-71362 Session Hijack](https://runtimewire.com/article/sansec-adobe-commerce-account-takeover-apsb26-92) — Adobe が APSB26-92 (2026-08-11) で修正した Adobe Commerce / Magento の認可バイパス (CVE-2026-71362, CVSS 9.1) に対し、Sansec が翌 8/12 に WAF での悪用試行をブロック検出。未認証攻撃者が任意顧客セッションを奪取し注文履歴・住所・個人情報にアクセス可能。修正バージョンへの即時更新が必要 *(RuntimeWire; Sansec 2026-08-12)*

- **[2026-08-12]** [Adobe Patches Three CVSS 10.0 ColdFusion Flaws and Critical Campaign Classic Vulnerabilities](https://helpx.adobe.com/security/products/coldfusion/apsb26-90.html) — Adobe が APSB26-90 (2026-08-11) で ColdFusion の CVSS 10.0 脆弱性 3 件（CVE-2026-48362: OS コマンドインジェクション / CVE-2026-48365: 不正入力検証 / CVE-2026-48371: 無制限ファイルアップロード）を修正。Adobe は Priority 1 として「72時間以内のパッチ適用」を強く勧告 *(Adobe Security; The Hacker News 2026-08-12)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-08-12 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-50656 (ShieldBreak) | Microsoft Defender Malware Protection Engine (mpengine.dll、全サポートバージョン) | CWE-362 / — | 標準ユーザーが mpengine.dll の TOCTOU 競合条件を発火 → 不完全な symlink 解決パスで NT AUTHORITY\SYSTEM に昇格 → RoguePlanet 修正のバイパス | 公式修正なし / PoC 公開 2026-08-12 ([Arctic Wolf](https://arcticwolf.com/resources/blog/cve-2026-50656-rogueplanet-shieldbreak/)) | 100% PoC 成功率 / Windows 11 25H2・Server 2025 確認済み / 公式修正なし / Defender デフォルト有効 |
| CVE-2026-71362 | Adobe Commerce / Magento Open Source 2.4.4〜2.4.9 (APSB26-92 適用前) | CWE-285 / **9.1** | 未認証攻撃者が認可チェック不備を悪用してセッション切替 → 任意顧客アカウントにセッション奪取 → カート・住所・注文履歴・個人情報にフルアクセス | APSB26-92 (2026-08-11) / 即日野生悪用確認 (Sansec 2026-08-12) | CVSS 9.1 / 未認証 / ユーザー操作不要 / 即日野生悪用検出 / Eコマース広範利用 |
| CVE-2026-48362 | Adobe ColdFusion 2025.x < 2025.0.12 / 2023.x < 2023.0.23 | CWE-78 / **10.0** | 未認証リモート攻撃者が ColdFusion サーバーに細工したリクエストを送信 → OS コマンドインジェクション → 任意コマンド実行 → ホステッドアプリ・接続システムへの横断侵害 | APSB26-90 (2026-08-11) ([Adobe Security](https://helpx.adobe.com/security/products/coldfusion/apsb26-90.html)) | CVSS 10.0 / 未認証 / Priority 1 "72時間以内パッチ" |
| CVE-2026-62815 | Microsoft QUIC (MsQuic HTTP/3 ライブラリ、全 Windows / Azure サービス) | CWE-416 / **9.8** | 未認証攻撃者がネットワーク越しに細工パケットを送信 → QUIC セッション処理の Use-After-Free → 任意コード実行 → 約 1,350 万ウェブサイトが影響圏 | 2026-08-11 Patch Tuesday ([windowsforum](https://windowsforum.com/security-alerts.84/cve-2026-62815-patch-microsoft-quic-remote-code-execution.442636/)) | CVSS 9.8 / 未認証 / HTTP/3 広範実装 / 過去事例では diff 解析後数日で兵器化 |
| CVE-2026-54917 | SeaweedFS S3 / Iceberg REST gateway < 4.30 (Go) | CWE-22 / AV:N/AC:L/PR:L/UI:N/C:H/I:H/A:N | 1バケット権限の攻撃者が `GET /bucket-A/../evil-bucket/key` を送信 → `mux.NewRouter().SkipClean(true)` で `..` が保持 → `util.JoinPath` がサーバー側で evil-bucket へ解決 → IAM 境界を越えた任意バケットへの読み書き | SeaweedFS v4.30 ([GHSA](https://github.com/advisories) / [GitLab Advisory](https://advisories.gitlab.com/golang/github.com/seaweedfs/seaweedfs/CVE-2026-54917/)) 公開 2026-08-12 | S3 互換ストレージ広範利用 / IAM バイパス / バリアント水平伝播可 (他 S3 実装の SkipClean 設定) |

---

## 国内脆弱性・インシデント情報

> 直近 3 日間 (2026-08-12〜08-14) に JVN/JPCERT/CC/IPA で確認できた新規の国内固有脆弱性・インシデント公表はありませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| CNN / The Register (Taiwan AI cyberattack) | CNN URL "2026/08/13/" 確認 ✓; TheRegister "security/2026/08/12/" 確認 ✓ |
| SiliconAngle / Marktechpost (Grok 4.6) | SiliconAngle URL "2026/08/12/" 確認 ✓ |
| Global Times / Artificial Analysis (DeepSeek V4 Pro 0813) | globaltimes.cn "202608/" 確認 ✓; artificialanalysis.ai Aug 13 リスト確認 ✓ |
| Forbes (Anthropic Claude watermarks) | Forbes URL "anishasircar/2026/08/13/" 確認 ✓ |
| TechTimes (Gemini 1B users) | techtimes.com URL "20260812/" 確認 ✓ |
| gHacks (OpenAI ChatGPT ads) | ghacks.net URL "2026/08/13/" 確認 ✓ |
| Help Net Security (LiteLLM 153GB) | helpnetsecurity.com URL "2026/08/13/" 確認 ✓ (EGRESS_BLOCKED; WebSearch スニペット確認) |
| Arctic Wolf / BleepingComputer (ShieldBreak) | arcticwolf.com URL 確認 ✓; bleepingcomputer.com "2026/08/" URL 確認 ✓ (EGRESS_BLOCKED; WebSearch 確認) |
| RuntimeWire / Sansec (CVE-2026-71362) | runtimewire.com 確認 ✓; sansec.io (EGRESS_BLOCKED; WebSearch 確認) |
| Adobe Security / THN (ColdFusion CVSS 10.0) | helpx.adobe.com APSB26-90 確認 ✓; thehackernews.com (EGRESS_BLOCKED; WebSearch 確認) |
| windowsforum (CVE-2026-62815) | windowsforum.com URL 確認 ✓ |
| GitLab Advisory (CVE-2026-54917) | advisories.gitlab.com URL 確認 ✓ |
| jvn.jp / jpcert.or.jp / ipa.go.jp | 2026-08-12〜14 新規エントリなし |

### 集計サマリ

- **巡回ソース数**: 約 35 (WebSearch 25クエリ, WebFetch試行 10件)
- **採用件数**: AI=7 / Security=3 / CVE=5 / 国内=0
- **除外理由内訳**:
  - 採用窓外 (公開日 <2026-08-12): Anthropic-Riot Platforms $9.1B 調達 (CNBC/Bloomberg 2026-08-11) / Gunra ランサムウェア合同アドバイザリ (therecord.media 2026-08-11) / Gemini 1B ユーザー原報 (Sundar Pichai ツイート 2026-08-11) / Claude 透かし原報 (SiliconAngle 2026-08-11) / LiteLLM CloudSEK 原報 (en.cryptonomist.ch 2026-08-11) / DeepSeek 460自律ターゲット (Forbes 2026-08-03) / MAI-Cyber-1-Flash (2026-07-27)
  - 重複 (excluded_set): CVE-2026-62873 (2026-08-12 digest 除外注記に記載) / SonicWall CVE-2026-15409/15410 (2026-08-05 digest 掲載) / N-able CVE-2026-18577 (2026-08-10 digest 掲載)
  - 日付確認不可: StormEncryptor (公開日不明)
- **取得失敗ソース (EGRESS_BLOCKED)**: sansec.io, helpnetsecurity.com, securityweek.com, bleepingcomputer.com, thehackernews.com, nvd.nist.gov, sherpaintelligence.substack.com

</details>

---

*生成: keda-digest-bot / 2026-08-14 05:13 JST*
