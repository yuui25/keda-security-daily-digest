# KEDA Daily Digest — 2026-06-26 (JST)

> 採用範囲: 公開日 2026-06-24 〜 2026-06-26
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

OpenAI が Broadcom との共同開発によりカスタム AI 推論チップ「Jalapeño」を発表し、GPU 依存からの脱却と垂直統合戦略を具体化した一方、DPRK 系 Rust 製 macOS バックドア「Gaslight」は LLM マルウェアアナリストを偽エラーで欺く Prompt Injection を実装するという、AI 防御ツールそのものを攻撃面とする新段階が確認された。Mandiant が Cisco SD-WAN CVE-2026-20245 の零日悪用詳細を公開 — 悪意の CSV ファイルで root アカウントを作成するという手法が 2026 年に入り 7 番目の SD-WAN 零日として記録に加わり、通信インフラへの持続的圧力が続いている。GitLab CE/EE の非認証 XSS (CVE-2026-10712) と Symantec が公開したフィレス バックドア Mistic/KongTuke も即時対応が必要な案件。

## AI 関連ニュース

- **[2026-06-24]** [OpenAI・Broadcom が「Jalapeño」— OpenAI 初のカスタム LLM 推論 ASIC — を共同発表: GPU 比 50% コスト削減・性能/ワットで既存 GPU を上回ると主張; 設計からテープアウトまで 9 か月でハイパフォーマンス ASIC 史上最速の開発サイクルを達成; GPT-5.3-Codex-Spark がラボで production 周波数・消費電力で動作確認済み; 年内にギガワット規模データセンターへ初期展開目標; OpenAI は「チップアーキテクチャ・カーネル・メモリ・ネットワーク・デプロイ全レイヤーを自社最適化するフルスタック戦略」を明示](https://openai.com/index/openai-broadcom-jalapeno-inference-chip/) *(OpenAI / CNBC / TechCrunch / Bloomberg / Tom's Hardware)*

- **[2026-06-24]** [Google DeepMind からの AI 人材流出が加速 — Gemini 中核研究者 Jonas Adler (コーディング AI 担当) と Alexander Pritzel (モデルトレーニング担当) が Anthropic 移籍へ; 両名は AlphaFold にも貢献; John Jumper (AlphaFold ノーベル賞, 6/19) 離脱からわずか 6 日内に4人連続流出; IPO 直前エクイティを機に人材移動が加速; アルファベット株が 6/22 に 5〜6% 下落](https://www.bloomberg.com/news/articles/2026-06-24/google-poised-to-lose-two-more-high-profile-ai-staffers-to-anthropic) *(Bloomberg / TechCrunch / The Next Web / Four Week MBA)*

- **[2026-06-25]** [macOS.Gaslight — DPRK 系 Rust 製 macOS バックドアが LLM マルウェアアナリストを偽エラーで欺く Prompt Injection を実装 — 38 件の偽「システム障害」メッセージ (トークン期限切れ・OOM Kill・ディスク枯渇・分析フラグ等) を Markdown ブロックとして実行ファイルに埋め込み、LLM トリアージエージェントが分析を中断・拒否するよう誘導; 検出は 6 月初旬の Apple XProtect 更新がきっかけ; C2 は Telegram Bot API ポーリングループ (AES-GCM + certificate-pinned TLS); LaunchAgent (com.apple.system.services.activity) で永続化; 6.6 KB の Base64 エンコード Python スクリプトで Keychain・Terminal 履歴・ブラウザ認証情報 (Chrome/Brave/Firefox/Safari) を ZIP 圧縮して Telegram 経由で送信](https://www.sentinelone.com/labs/macos-gaslight-rust-backdoor-turns-prompt-injection-on-the-analyst-not-the-sandbox/) *(SentinelOne Labs / The Hacker News / BleepingComputer / Infosecurity Magazine)*

## セキュリティ関連ニュース

- **[2026-06-25]** [Mandiant が Cisco Catalyst SD-WAN CVE-2026-20245 の零日悪用詳細を公開 — 2026年3月より脅威アクターが "evil_tenant.csv" を SD-WAN Manager の tenant-upload CLI 機能へ投入し root アカウント "troot" を作成; /etc/passwd・/etc/shadow のバックアップ後に管理プレーン全体を掌握; 痕跡消去スクリプトでファイル削除・設定巻き戻しを実施; サービスプロバイダーが 2 ヶ月間防御不能状態に; 2026 年の Cisco SD-WAN 零日悪用確認は通算 7 件目](https://www.bleepingcomputer.com/news/security/mandiant-reveals-how-cisco-sd-wan-zero-day-attacks-gained-root-access/) *(BleepingComputer / SecurityWeek / Google Cloud Blog / TechTimes)*

- **[2026-06-24/25]** [Broadcom Symantec が Mistic バックドアと IAB KongTuke を公開 — 2026年4月から保険・教育・IT・専門サービス業界を標的にフィレス (ディスク書き込みなし) バックドアを展開; ClickFix 感染チェーン (偽 CAPTCHA → 多段スクリプト) または Microsoft Teams 経由の ModeloRAT ドロッパーで配送; メモリ内実行・自己消去キルスイッチ・タスクスケジューラ永続化; KongTuke (別名 Woodgnat) が Qilin/Interlock/Rhysida/Akira/8Base/Black Basta 等 RaaS グループへのアクセスを販売](https://www.bleepingcomputer.com/news/security/stealthy-mistic-backdoor-linked-to-ransomware-access-broker-kongtuke/) *(BleepingComputer / The Hacker News / Symantec TI / TechTimes)*

- **[2026-06-25]** [GitLab CE/EE 13 件の脆弱性パッチを公開 — 高重大度 3 件: CVE-2026-10712 (Web IDE workbench 非認証 XSS → 任意ユーザーセッションへのスクリプト実行) / CVE-2026-10086 (Analytics ダッシュボード XSS、developer 権限が必要) / CVE-2026-12053 (Duo Workflows の不十分な出力フィルタリング → コミット済み機密情報漏洩); GitLab Flavored Markdown / AI GraphQL エンドポイント / インポート機能 / ランナー管理にも影響; 自己ホスト版は即時アップグレード推奨](https://www.securityweek.com/gitlab-patches-code-execution-information-disclosure-vulnerabilities/) *(SecurityWeek / CybersecurityNews / Cyberpress)*

- **[2026-06-25]** [macOS ClickFix 新亜種: Terminal コマンドで DMG を静かにマウントし AMOS インフォスティーラーを起動 — Palo Alto Unit 42 が公開; 偽 CAPTCHA ページが Terminal へコマンド貼り付けを誘導 → DMG を攻撃者サーバーからダウンロード → macOS 標準の hdiutil で自動マウント → AMOS 自動起動の3ステップ; Chrome / Edge / Brave / Opera / Arc 含む 8 Chromium ブラウザの認証情報・Cookie・支払いカード・Keychain・暗号通貨ウォレットを窃取](https://www.bleepingcomputer.com/news/security/new-macos-clickfix-attack-silently-mounts-dmgs-to-push-infostealer/) *(Palo Alto Unit 42 / BleepingComputer / Security Boulevard)*

- **[続報][2026-06-25]** [Microsoft が Defender 零日 RoguePlanet (CVE-2026-50656) のパッチ開発中と正式確認 — 研究者 Nightmare Eclipse が公開した PoC は最新パッチ済み Windows 10/11 上でも SYSTEM シェルを取得可能 (Defender リアルタイム保護 ON/OFF・パッシブモード問わず動作); 同研究者は過去数ヶ月で BlueHammer・RedSun・UnDefend 等の零日も公開済み; 修正版未提供のまま野外悪用リスク継続](https://www.securityweek.com/microsoft-working-on-patch-for-rogueplanet-zero-day/) *(SecurityWeek / The Hacker News / BleepingComputer / PCWorld / Morphisec)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-24 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-20245 | Cisco Catalyst SD-WAN Manager (vManage) / Controller (vSmart) / Validator (vBond) < 20.9.9.2 / 20.12.7.2 / 20.15.4.5 等 | CWE-78 / **7.8** | CLI の tenant-upload 機能がアップロードされた CSV ファイルの内容検証なしにシェルへ渡す → 認証済み netadmin 権限から root 任意コマンド実行・不正ルートアカウント作成 | [Cisco SD-WAN 修正各バージョン (2026-06-12)](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-sdwan-privesc-4uxFrdzx) | 2026-03 から 2 ヶ月先行悪用確認 / Mandiant IOC 公開 2026-06-25 / **2026 年 SD-WAN 零日 通算 7 件目** / CSV/ファイル入力を検証なしで CLI コマンドに渡すパターン → 組み込みルーターの類似 tenant 管理機能へバリアントハント推奨 |
| CVE-2026-10712 | GitLab CE/EE (バージョン範囲は今週リリース前全版) | CWE-79 / 高 | Web IDE workbench アセットハンドラーが攻撃者制御のリソース名を HTML コンテキストに未エスケープで出力 → **非認証**攻撃者が他ユーザーのブラウザセッションで任意 JavaScript 実行; セッション乗っ取り・CSRF トークン窃取 | [GitLab 最新パッチリリース (2026-06-25)](https://about.gitlab.com/releases/) | 2026-06-25 公開 / 非認証 XSS / Web IDE は GitLab.com・自己ホスト全版に影響 / Duo AI コード補助連携環境での AI 会話内容盗聴リスクあり |
| CVE-2026-10086 | GitLab EE (Analytics ダッシュボード機能) | CWE-79 / 高 | Analytics ダッシュボードが developer ロールユーザーの入力を他ユーザーのセッションコンテキストに未エスケープで反映 → 認証済み developer が管理者を含む任意ユーザーのブラウザで任意 JavaScript 実行 | [同上](https://about.gitlab.com/releases/) | 2026-06-25 公開 / developer 権限のみで成立 / Atlassian Confluence の同種 Analytics XSS パターンへバリアントハント推奨 |
| CVE-2026-12053 | GitLab CE/EE (Duo Workflows) | CWE-200 / 高 | Duo Workflows (AI アシスタント) の出力フィルタリング不足でワークフロー実行中に機密データ (シークレット・鍵・認証情報等コミット済みコンテンツ) がレスポンスに漏洩 → プロジェクトメンバーが意図せず機密情報を取得 | [同上](https://about.gitlab.com/releases/) | 2026-06-25 公開 / AI コード補助ツール特有の出力フィルタリング欠落パターン / GitHub Copilot / Amazon Q 等の同種 LLM コード補助機能へバリアントハント推奨 |
| CVE-2026-47145〜47151 (7件) | Silicon Labs EmberZNet PRO ≤ v9.0.2 (Zigbee プロトコルスタック) | CWE-125 / CWE-787 / 未確定 | Zigbee メッシュネットワーク内の既参加デバイスからの細工済み Color Control メッセージ・OTA リクエスト・その他コマンドが OTA サーバーパーサーを OOB 読み出し / OOB 書き込み / assert 終了に誘導 → DoS または潜在 RCE; ネットワーク参加済みデバイスが前提だが IoT 環境では常態的条件 | [EmberZNet v9.0.3 (修正バージョン)](https://www.silabs.com/software-and-tools/zigbee-emberznet) | 2026-06-25 NVD 公開 / スマートホーム・産業 IoT の Zigbee デバイス全般に影響 / Matter/Thread 等隣接スタックの OTA パーサーへバリアントハント推奨 |

## 国内脆弱性・インシデント情報

> 直近2日間に該当する新規国内ニュースは確認できませんでした。

JPCERT/CC の 2026-06-24 付週次レポート (wr260624) は Zyxel GS1900 シリーズスタックバッファオーバーフロー (CVE-2026-7273、Zyxel 社アドバイザリ 2026-06-16)・Node.js・Chrome・Oracle 製品・プリンタドライバ等の脆弱性をまとめているが、いずれもアドバイザリ初出が採用窓外 (2026-06-23 以前) のため本セクションへの採用は見送った。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 30 ソース (SentinelOne Labs / The Hacker News / BleepingComputer / Infosecurity Magazine / GBHackers / Cyberpress (Gaslight), OpenAI / CNBC / TechCrunch / Bloomberg / Tom's Hardware (Jalapeño), Bloomberg / TechCrunch / The Next Web / FourWeekMBA (Google talent exodus), BleepingComputer / SecurityWeek / Google Cloud Blog / TechTimes (Cisco SD-WAN), Symantec / BleepingComputer / The Hacker News / TechTimes (Mistic/KongTuke), SecurityWeek / CybersecurityNews / Cyberpress (GitLab), Palo Alto Unit 42 / BleepingComputer / Security Boulevard (macOS ClickFix), SecurityWeek / The Hacker News / BleepingComputer / PCWorld / Morphisec (RoguePlanet), NVD / Silicon Labs (EmberZNet CVE), CISA KEV, GitHub Advisory Database, JPCERT/CC Weekly Report, JVN)
- 採用件数: AI=3 / Security=5 / CVE=5グループ (8件) / 国内=0
- AI 件数が目安 (8〜12) を下回った理由:
  - GPT-5.6: 2026-06-25 時点で OpenAI 公式発表なし (予測市場は7月に移動); 採用不可
  - Fable 5 輸出規制: 継続中だが前回 (2026-06-25 digest) に今週の進展まで網羅済み; 続報なし
  - DARPA AI Forge (DARPA + NSF): プログラム発表は 2026-06-01・RFI 締め切り 6/22 — 採用窓外
  - Anthropic $965B Series H / IPO 機密提出: 2026-05-28〜06-01 — 採用窓外
  - Claude Corps フェローシップ: 2026-06-11 発表 — 採用窓外
  - Google Search AI エージェント: 2026 I/O (5月) 発表 — 採用窓外
  - 大型モデルリリース (OpenAI / Google / Meta / Mistral 等): 採用窓内に公式発表なし
- 採用窓 (2026-06-24〜26) は木〜土に当たり、大型 AI ラボ発表のペースが低調なサイクルと重なった
- 除外理由内訳:
  - 古すぎ (公開日 < 2026-06-24):
    - Zyxel CVE-2026-7273 (Zyxel アドバイザリ 2026-06-16)
    - BeyondTrust CVE-2026-1731 (PoC 公開 2026-02-10)
    - DARPA AI Forge (2026-06-01)
    - Anthropic Claude Corps フェローシップ (2026-06-11)
    - White House AI EO (2026-06-02)
  - 重複 (excluded_set 直近 7 ダイジェスト 2026-06-19 〜 2026-06-25):
    - Cisco UCM CVE-2026-20230 (2026-06-25 digest 掲載済み)
    - Ubiquiti UniFi OS CVE-2026-34908/34909/34910 CISA KEV (2026-06-25 digest)
    - Lantronix CVE-2025-67038 (2026-06-25 digest)
    - Cordyceps / GitHub Actions supply chain (2026-06-25 digest)
    - Squidbleed CVE-2026-47729 (2026-06-24 digest)
    - DifyTap CVE-2026-41948/41947 (2026-06-24 digest)
    - FFmpeg CVE-2026-8461 (2026-06-24 digest)
    - Microsoft RoguePlanet CVE-2026-50656 初報 (2026-06-19 digest) → 今回「続報」として採用
    - AutoJack (2026-06-21 digest)
    - usbliter8 (2026-06-21 digest)
  - 取得失敗ソース (HTTP 403): sentinelone.com/labs 個別記事, thehackernews.com 個別記事, bleepingcomputer.com 個別記事, securityweek.com 個別記事, helpnetsecurity.com 個別記事, gbhackers.com 個別記事 — WebSearch スニペット・複数独立媒体で内容・日付を補完

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-06-19 〜 2026-06-25) の全 CVE/GHSA/URL を除外済み。*
