# KEDA Daily Digest — 2026-09-12 (JST)

> 採用範囲: 公開日 2026-09-10 〜 2026-09-12
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Anthropic が 9/10 に中国 AI 3 社（Alibaba・DeepSeek・Moonshot AI）の不正蒸留キャンペーンを固有名詞と具体的数字で公表し、Alibaba が 3,500 超の偽アカウントで 1 億 5,100 万回の Claude クエリを Qwen 訓練に利用していたことが明らかになった。AI インフラ投資面では Microsoft が 2032 年までに 38GW の DC 容量を整備する計画を発表し、Pentagon が AI サプライチェーン支援に $50 億融資交渉を開始するなど、AI は軍事・国家戦略インフラとして本格的に位置づけられた。CVE 面では Apache ActiveMQ Artemis に CVSS 9.8 の未認証セッション乗っ取り（CVE-2026-57967）が 9/10 に開示され、AI プラットフォームの Open WebUI でも OAuth SQLite 実装の認証バイパス（CVE-2026-87016）が発覚、ID 管理基盤の脆弱性が AI スタック全体に波及するリスクを示した。

## AI 関連ニュース

- **[2026-09-10] [続報]** [Anthropic、中国 AI 3 社の不正蒸留を固有名詞・規模付きで公表 — Alibaba が偽アカウント 3,500+ で Claude に 1 億 5,100 万回クエリを実行し Qwen の学習データに利用、Moonshot は Kimi ユーザーを無断で Claude にルーティングして応答を自社モデルのものとして提示](https://techcrunch.com/2026/09/10/anthropic-details-distillation-campaigns-from-alibaba-moonshot-ai-and-deepseek/) — DeepSeek も同様の「転送ステーション」経由のルーティングが確認され、いずれも API 利用規約違反。Anthropic は蒸留攻撃が「AI の最も価値あるケイパビリティを標的にする」と警告し業界内の情報共有を呼びかけ。 *(TechCrunch / CNBC)*

- **[2026-09-10]** [DeepSeek V4.1-Flash リリース — 748B パラメータ MoE（入力 8B active / 出力 16B active）、MIT ライセンスのオープンウェイト、API $0.15/M token でネイティブ画像理解を追加](https://datanorth.ai/news/deepseek-releases-deepseek-v4-1-flash) — 従来の V4 Flash・V4 Flash Vision Experimental を置き換え、Hugging Face でオープンウェイトを同時公開。価格競争力と OSS 公開の組み合わせが Western フロンティアモデルへの圧力を継続。 *(DataNorth / ProPakistani)*

- **[2026-09-10]** [OpenAI Agents API パブリックベータ公開 — Codex インフラを agent / environment / session / events の 4 プリミティブ API として全開発者に開放、OpenAI 管理サンドボックス・自前インフラ・パートナーサンドボックスの 3 形式に対応](https://openai.com/index/introducing-the-agents-api/) — 追加料金なし（使用量コストのみ）。これまで Codex のみに提供していた実行インフラを汎用 API 化した転換点。AI エージェントのセキュリティ設計（サンドボックス・セッション分離）が開発者責任として問われる局面に移行。 *(OpenAI / MarkTechPost)*

- **[2026-09-11]** [Clearview AI が顔認識を超える個人プロファイリングツール「InquiryIQ」を非公開開発 — 顔認識マッチを起点に xAI Grok で自動ウェブ調査・候補グラフを構築、年齢・性別・人種フィルターを実装](https://www.biometricupdate.com/202609/clearview-ai-prototype-points-to-next-phase-of-facial-recognition-identity-intelligence) — 公開サイトのコードに未公開プロトタイプが発見されたと WIRED が報道。当局への実提供はなく現行版のリリース計画もないと Clearview は回答。一方で AI による大量プロファイリングの自動化が既に実装段階にあることを示した。 *(WIRED / Biometric Update)*

- **[2026-09-11]** [Microsoft が 2032 年までに 38GW のグローバル AI データセンター容量を整備する計画を公表 — 現行 12GW から 3 倍超、供給不足で Temu が大型クラウド契約を Oracle へ移行する事態が先行](https://www.technology.org/2026/09/11/microsoft-38-gigawatts-data-center-capacity-2032/) — 38GW はニューヨーク州のピーク消費電力を超える規模。AI 需要急増に供給が追いつかない構造的問題が浮き彫りに。 *(technology.org / Bloomberg)*

- **[2026-09-11]** [Pentagon が AI データセンターサプライチェーン維持のため $50 億融資交渉を開始、Oracle が $6,640 億のクラウドバックログを記録 — AI インフラが軍事・国家安全保障上の重要インフラとして公式認定される動き](https://ca.finance.yahoo.com/news/microsoft-targets-38gw-data-center-150904165.html) — UAE の G42 が Stargate 連合（OpenAI・Oracle・SoftBank）と協調した AI インフラ整備も加速。 *(Yahoo Finance / Tech Startups)*

## セキュリティ関連ニュース

- **[2026-09-11]** [IDScan.net が 1 億 5,300 万件の運転免許スキャン流出を公式確認 — 身元確認 SaaS 事業者（レンタカー・小売・大麻販売店向け）からの窃取データが「Nexus」ダークウェブマーケットで売買、FBI がニューオーリンズ支局で捜査開始](https://www.helpnetsecurity.com/2026/09/11/idscan-net-data-breach-153-million-drivers-licenses/) — Krebs が 8/31 に最初に報告、IDScan は 9/4 に侵害通知を公開。氏名・ID 番号・有効期限・生年月日が含まれ、北米の大多数の成人に影響が及ぶ可能性。Nexus はその後閉鎖。 *(Help Net Security / Krebs on Security / SecurityWeek)*

- **[2026-09-11]** [FulcrumSec が「Hardcoded Horrorshow」恐喝キャンペーンを継続 — クライアントサイド JS バンドルと公開 GitHub リポジトリからハードコード認証情報を発見してラテラルムーブ、ノボ・ノルディスクから Azure DevOps + GitHub PAT 経由で 1TB 超のデータを窃取・公開](https://www.govinfosecurity.com/novo-nordisk-data-breach-tied-to-stolen-github-access-tokens-a-32802) — 他の被害組織にはマンチェスター空港グループ、Arup グループ（英）、Global Schools Group（シンガポール）が含まれる。クライアントサイドへの本番資格情報の埋め込みが組織的リスクであることを改めて示した。 *(DataBreachToday / GovInfoSecurity)*

- **[2026-09-10]** [CISA が ICS/医療機器 Advisory を 4 件公表 — NextGen Healthcare Mirth Connect の SQL インジェクション+XXE（CVE-2026-82583、CVSS 8.3）、Orthanc DICOM サーバのヒープ書き込み DoS（CVE-2026-87020、Critical）、AVEVA Pipeline Integrity Monitor のハードコード暗号化キー+MD5 ハッシュ（CVE-2026-81821/22）](https://www.cisa.gov/news-events/ics-medical-advisories/icsma-26-253-01) — 医療機器・OT インフラへの攻撃面を広げる高リスク脆弱性群。各ベンダーはパッチを提供済み。 *(CISA)*

- **[2026-09-10-11]** [Chrome 153 に含まれる WebGL/Cast の Critical UAF・OOB Write 5 件が正式 CVE 採番 — CVE-2026-87464/87488（Use-After-Free、WebGL）・CVE-2026-87438（Out-of-Bounds Write、WebGL）・CVE-2026-87527（Buffer Overflow、WebGL）・CVE-2026-87455（UAF、Cast）が CVSS 9.6 で公開](https://www.securityweek.com/chrome-153-patches-seventh-zero-day-of-2026/) — 同リリースで修正済み（153.0.8010.36+）。CVE-2026-87491（KEV 登録済み、Sep 11 digest 掲載）とは別件。未更新環境は即時アップデートが必須。 *(SecurityWeek / Malwarebytes)*

- **[2026-09-11]** [AI エージェント向け ID 管理ツールが相次ぎ GA — Orchid Security がエージェントの ID ドリフト検出とアプリレベルキルスイッチを発表、Akeyless が Agentic Runtime Authority（AI エージェントのリアルタイム ID 制御レイヤー）を一般提供開始](https://www.helpnetsecurity.com/2026/09/11/new-infosec-products-of-the-week-september-11-2026/) — AI エージェントの急増に対応した ID 制御市場が立ち上がり始めた。Zero Trust ガバナンスを AI ランタイムに拡張する方向性が業界標準として形成されつつある。 *(Help Net Security)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 today-2 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-57967 | Apache ActiveMQ Artemis (classic) ≤ 2.44.0 / (new) ≤ 2.56.0 | CWE-306 / CVSS 9.8 | 未認証リモート攻撃者が CORE プロトコルの SESSION_REATTACH パケットを細工 → ブローカーが認証済みセッションの正当性を検証せずに再接続を受け入れ → 既存の認証済みセッションを乗っ取り RCE | [v2.57.0](https://artemis.apache.org/components/artemis/security) | CVSS 9.8 / 未認証 / メッセージブローカーは金融・製造・決済系に広く使用 / RabbitMQ・ActiveMQ Classic の同様の再接続フロー確認を推奨 |
| CVE-2026-87016 / GHSA-wpmr-8h3q-fwj7 | Open WebUI 0.6.41〜0.11.0 (SQLite + OAuth/OIDC/SCIM 構成) | CWE-287 / High | 攻撃者が OAuth subject claim に % や _ のワイルドカードを含む文字列を送信 → `get_user_by_oauth_sub()` が SQLite 上で LIKE 句にコンパイルされ意図しないユーザーとマッチ → 管理者アカウントへのログイン・AI ゲートウェイ全権取得 | [v0.11.1](https://osv.dev/vulnerability/GHSA-wpmr-8h3q-fwj7) | High / AI 統合ゲートウェイ / SQLite の LIKE 照合バグは同様の OAuth Sub 検索を持つ LangChain・Ollama 管理 UI・LiteLLM への水平バリアント候補 / PostgreSQL 版は非影響 |
| CVE-2026-8778 | MIPL Grouped Checkout Fields for WooCommerce (WordPress) ≤ 1.2.1 | CWE-434 / CVSS 9.8 | 未認証攻撃者が `mipl_wc_upload_file()` 関数にファイルタイプ・MIME 検証が存在しないことを利用して任意ファイル（PHP シェル等）をアップロード → WordPress サーバで任意コード実行 | [v1.2.2](https://radar.offseq.com/threat/cve-2026-8778-cwe-434-unrestricted-upload-of-file-with-dangerous-type-in-mulika-mipl-grouped-checkout-a571f695f51796b8) | CVSS 9.8 / 未認証 / WooCommerce プラグインの無制限ファイルアップロードは PrestaShop・Magento カスタムモジュールへの水平バリアント候補 |
| CVE-2026-82583 | NextGen Healthcare Mirth Connect ≤ 4.7.1 | CWE-89+CWE-611 / CVSS 8.3 (High) | 認証済み攻撃者が Database Connector API への SQL インジェクションと XXE を組み合わせ → 接続システムの保存済み資格情報を開示・任意ファイル書き込み → 医療統合エンジン全体の侵害 | [v4.7.2](https://www.cisa.gov/news-events/ics-medical-advisories/icsma-26-253-01) | CISA ICSMA-26-253-01 / 医療統合エンジン / HL7/FHIR を処理する同類製品（Rhapsody・Mule ESB・InterSystems IRIS）への SQL+XXE バリアント調査推奨 |
| CVE-2026-81821/81822 | AVEVA Pipeline Integrity Monitor ≤ 2025_SP1_P1_build_7.1.9580.8513 | CWE-321+CWE-328 / High | 攻撃者がハードコード暗号化キー（CWE-321）で暗号化された設定ファイルを復号し内部資格情報を取得、または MD5 パスワードハッシュ（CWE-328）を GPU クラッキングで管理者パスワードを回復 → OT パイプライン整合性監視の全権限取得 | [2025 SP1 P2 Security Update](https://www.cisa.gov/news-events/ics-advisories/icsa-26-253-01) | CISA ICSA-26-253-01 / OT パイプライン監視基盤 / ハードコード鍵+MD5 の組み合わせは OSIsoft PI・Honeywell Process Controller 等 SCADA 製品への水平バリアント候補 |
| CVE-2026-87464 他 4 件 (Chrome 153 WebGL/Cast) | Google Chrome ≤ 153.0.8010.35 (Windows/macOS/Linux) | CWE-416+CWE-787 / CVSS 9.6 | 遠隔攻撃者が細工した WebGL を含むページを閲覧させる → WebGL（CVE-2026-87464/87488 UAF、CVE-2026-87438 OOB Write、CVE-2026-87527 Buffer Overflow）または Cast（CVE-2026-87455 UAF）のメモリ破壊を誘発 → レンダラーサンドボックス内で RCE（エスケープには追加 CVE 要） | [Chrome 153.0.8010.36](https://chromereleases.googleblog.com/2026/09/) | CVSS 9.6 (5 件一括) / 野外悪用未確認 / CVE-2026-87491（KEV 登録済み）と同一リリース修正 / WebGL の UAF は Firefox/WebKit にも水平バリアント候補 |

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-09-10 | ICSMA-26-253-01 (CISA) | NextGen Healthcare Mirth Connect ≤ 4.7.1 に SQL インジェクション+XXE — 医療統合エンジン経由で接続システムの資格情報開示・任意ファイル書き込みが可能 | CVSS 8.3 / 医療情報統合基盤 | [ICSMA-26-253-01](https://www.cisa.gov/news-events/ics-medical-advisories/icsma-26-253-01) |
| 2026-09-10 | ICSMA-26-253-02 (CISA) | Orthanc DICOM Server < 1.13.0 に PNG/JPEG デコード時のヒープ書き込み — 認証済み攻撃者が細工画像を送信してサーバクラッシュ（DoS） | Critical / 医療用 DICOM サーバ | [ICSMA-26-253-02](https://www.cisa.gov/news-events/ics-medical-advisories/icsma-26-253-02) |
| 2026-09-10 | ICSA-26-253-01 (CISA) | AVEVA Pipeline Integrity Monitor ≤ 2025_SP1_P1 にハードコード暗号化キー+MD5 ハッシュ — 攻撃者が設定ファイルを復号し資格情報を取得または管理者パスワードを回復 | High / 石油・ガスパイプライン OT 基盤 | [ICSA-26-253-01](https://www.cisa.gov/news-events/ics-advisories/icsa-26-253-01) |

> 直近2日間に該当する新規 JVN/JPCERT/IPA 固有アドバイザリは確認できませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 20+（TechCrunch, CNBC, OpenAI Blog, MarkTechPost, DataNorth, ProPakistani, WIRED, Biometric Update, technology.org, Bloomberg, Yahoo Finance, Help Net Security (×2), DataBreachToday, GovInfoSecurity, SecurityWeek (×2), CISA (ICSMA/ICSA ×3), Malwarebytes, Krebs on Security, Engadget, SecurityOnline, OffSeq/THREATINT (×3), OSV.dev, CVE Brief Sep 11, Senserva, Tech Startups, borecraft.com, Cyfirma）
- 採用件数: AI=6 / Security=5 / CVE=6 (5+1 グループ) / 国内=3 (CISA ICS) + 0 JVN/JPCERT
- 除外理由内訳:
  - 重複（excluded_set 該当、Sep 5〜11 digest 収録済み）: CVE-2026-20079/20316 Cisco FMC (Sep 11)、CVE-2025-25249 Fortinet FortiOS (Sep 11)、CVE-2026-87491 Chrome V8 KEV (Sep 11)、CVE-2026-69676 Windows Kerberos (Sep 11)、APSB26-141 Adobe Acrobat (Sep 11)、CVE-2026-79696 Google ADK (Sep 10)、CVE-2026-86464 Eclipse aeriOS (Sep 10)、CVE-2026-69730 Windows DNS (Sep 10)、CVE-2026-18963 Siemens IEM (Sep 10)、CVE-2026-50093 Siemens Siveillance (Sep 10)、CISA AA26-251A 中国蒸留 (Sep 10、一般記述として収録済み)、WeWorm/AdaptHealth/ShieldCrash/PivotC2 (Sep 11)、OpenAI Navier-Stokes (Sep 11)、Cisco FMC/Sandworm/Qilin (Sep 11)、PaperCut AI エージェント攻撃 (Sep 10)、Android Sep Update (Sep 10)、N0va Phishkit (Sep 10)、CVE-2026-85880/81963 Windows ゼロデイ (Sep 9)、CVE-2026-86218 N-able (Sep 9)、CVE-2026-75650 Adobe Magento (Sep 9)、WeWorm (Sep 9)
  - 採用窓外（公開日 < 2026-09-10）: CVE-2026-83548/83549 SonicWall SMA1000（Sep 1-2 公開、Sep 11 に続報が出たが初出は窓外のため除外）、Canvas LMS 教育機関大規模侵害（Apr 2026）、Gitea CVE-2026-77645（日付確認困難）
  - 日付不明・確認困難: PaperCut Sep 10 パッチリリース（予定報道は確認も実際のリリース日を 2 次ソースで裏取り不可）、Chrome 追加 CVE 87448/87512 の正式採番日（Sep 8 リリース vs Sep 11 採番の区別が付かないため代表 4 件のみ採用）
  - 取得失敗ソース（EGRESS_BLOCKED）: techstartups.com, borecraft.com, securityonline.info, malwarebytes.com, techcrunch.com (→ スニペット/ミラー経由補完), securityboulevard.com, cyfirma.com, jpcert.or.jp, ipa.go.jp, jvn.jp, bleepingcomputer.com, helpnetsecurity.com (→ スニペット経由補完)

</details>
