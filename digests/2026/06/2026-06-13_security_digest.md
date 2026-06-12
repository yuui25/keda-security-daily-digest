# KEDA Daily Digest — 2026-06-13 (JST)

> 採用範囲: 公開日 2026-06-11 〜 2026-06-13
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Nightmare Eclipse がRoguePlanet 公開の翌日 (6/11) に 7 本目のゼロデイ GreatXML を公開 — Defender オフラインスキャンを一度でも実行した Windows 全機種で回復パーティションへの 2 ファイル配置だけで BitLocker が無認証で解除される物理バイパス。CVE 未採番・未パッチで TPM+PIN への切り替えが現時点唯一の緩和策となっている。AI 面では研究者 Brutecat が Claude AI で構築した MCP ファジングフレームワークで Google の内部 API 1,500 本を 3 ヶ月スキャンし VRP から $50万超を獲得、AI 支援型バグハンティングの民主化を象徴する事例となった。Google Chrome も CISA KEV 入りゼロデイ (CVE-2026-11645) の 1 週間後に Critical 4 件を含む 28 件修正の追加更新 (149.0.7827.115) を 6/12 に公開し、ブラウザの継続的パッチ適用が改めて求められている。

---

## AI 関連ニュース

- **[2026-06-11]** [Brutecat (Arvin Shivram) が Claude AI で Google VRP $50万超を獲得 — Google の 1,500 API discovery document を MCP ツール化して Claude に接続した自動ファジングフレームワークで、PII 無認証取得バグ (Google Voice 番号・回復電話番号を任意の Gaia ID から dump)・電話番号勝手割り当てなど P0/S0 クラスのアクセス制御欠陥を 3 ヶ月以内に複数発見](https://gbhackers.com/researcher-hack-google-earns-500000-bug-bounty/) — curl 1 本のみで PII を dump できる脆弱 API は数時間以内にパッチ適用・$20,000 獲得; 修正後も 60,000 以上の APK をスキャンした偵察フェーズと Claude への MCP 全接続という手法は AI 支援 API セキュリティテストのテンプレートとして業界で注目 *(GBHackers / CyberSecurityNews / Brutecat.com)*

- **[2026-06-11]** [OpenAI が Ona (旧 Gitpod) を買収して Codex をエンタープライズ対応化 — Ona が提供するプリコンフィグ済みセキュアクラウド環境を Codex に統合し、AI エージェントがオフライン中も本番 DB・CI/CD・API に非同期接続しながら長期タスクを自律実行できるようにする](https://openai.com/index/openai-to-acquire-ona/) — Ona は Gitpod が 2025 年末に AI エージェント専用にリブランド; 取得額は非公開、Ona チームは OpenAI Codex 組織と独立を保ちつつ協働。人間不在での長期エージェント実行が標準化されることで攻撃面のライフタイム長期化が懸念される *(OpenAI / TechRadar / The Next Web)*

- **[2026-06-12]** [ニューヨーク州議会が AI 7 法案を Hochul 知事に送付 — 子供向けコンパニオンチャットボット禁止 (S9051, 全会一致 137-0/60-0)・AI 訓練データ透明性法・FAIR News Act (AI 生成コンテンツへの出所データ添付・AI 生成ニュースの開示義務化)・データセンター 1 年間モラトリアム・サーベイランス価格付け禁止 等; Hochul は 2026-12-31 まで署名/拒否権行使](https://www.transparencycoalition.ai/news/ai-legislative-update-june12-2026) — EU AI Act 完全施行 (8/2) や Colorado AI Act 施行 (6/30) と並び、米国の AI 規制ポートフォリオが州レベルで急拡大している転換点; 成立すれば未成年ユーザーへの AI コンパニオン提供は米国初の州法禁止に *(Transparency Coalition / NYSenate.gov / Hochul.gov)*

> 直近2日間に該当する新規 AI ニュースは上記 3 件に留まりました。Patch Tuesday 翌週の端境期に当たるため、主要 AI ラボからの新規モデルリリースや大型発表は確認されませんでした。

---

## セキュリティ関連ニュース

- **[2026-06-11]** [Nightmare Eclipse が 7 本目のゼロデイ GreatXML を公開 — Defender オフラインスキャンを一度でも実行した Windows 全バージョンで、回復パーティションの 2 XML ファイルを配置するだけで WinRE 起動時に SYSTEM シェルを取得し BitLocker 暗号化ドライブに無認証アクセスが可能; 研究者本人が「偶然の発見で 4 時間で完成」と証言](https://www.securityweek.com/greatxml-zero-day-exploit-bypasses-bitlocker/) — 前日の RoguePlanet (Defender race condition SYSTEM 昇格) に続く連続開示。CVE 未採番・Microsoft 公式パッチなし。唯一の緩和策: BitLocker を TPM-only から **TPM+PIN に再設定** すること (TPM-only では回復環境から自動解除されるため不十分) *(SecurityWeek / CyberSecurityNews / Tom's Hardware / The Register)*

- **[2026-06-12]** [Google Chrome 149.0.7827.115 が Critical 4 件を含む 28 件のセキュリティ修正をリリース — CVE-2026-12007 (Core UAF)・CVE-2026-12008 (DigitalCredentials UAF)・CVE-2026-12009 (Accessibility 不十分なバリデーション)・CVE-2026-12010 (GPU ヒープバッファオーバーフロー) の 4 Critical 含む; CISA KEV 入りゼロデイ CVE-2026-11645 (6/5 CISA 追加) から 1 週間以内の追加更新](https://chromereleases.googleblog.com/2026/06/) — Chrome 149 はわずか 1 ヶ月に 3 バージョン (149.0.7827.53 / 149.0.7827.102 / 149.0.7827.115) のセキュリティ更新を要しており、Chromium 系ブラウザ (Edge・Brave・Opera) の追随が急務 *(Tenable / deskmodder.de)*

- **[2026-06-11]** [OnyxC2 Stealer-as-a-Service が月額 $250 で 210 以上のアプリ・ブラウザ拡張・暗号ウォレットを標的に — Cloudflare Fronted C2 + DLL Sideloading (Authenticode 署名済み正規アプリにマルウェア DLL を同梱) + インメモリ実行で EDR・AV 検出を回避; HVNC・LSASS ダンプ・SOCKS5 リバースプロキシも同梱し「ビルドが検出されたら返金」保証](https://www.securityweek.com/onyxc2-stealer-offers-cybercriminals-enterprise-grade-data-theft/) — 2026 年前半に犯罪フォーラムに登場; $250/月という低コスト MaaS が企業グレードの窃取能力を大量普及させるモデルの典型例 *(Security Affairs / SecurityWeek / GBHackers)*

- **[2026-06-11/12]** [DragonForce がスウェーデン建材大手 Areco・香港 Hong Kong Parkview に侵害を公表; 同日 TheGentlemen も UiTM Holdings・Scenic Hudson・Highwoods Properties (REIT) ほか複数組織への侵害を公表 — 建設・不動産・公共インフラが今週の標的セクター](https://www.ransomware.live/group/dragonforce) — 2026 年の年間 2,090 件/日ランサムウェア攻撃ペースが週末も継続; DragonForce は 6/10 の Sayre Associates (米土木測量) を含め今週 3 件を公表。国際的な分散標的化の継続が顕著 *(ransomware.live / DeXpose)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-11 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| GreatXML (CVE 未採番) | Windows 全バージョン (Defender オフラインスキャン実行済み環境) | CWE-693 / 未採点 (物理バイパス) | 物理アクセス攻撃者が回復パーティションに XML ファイル 2 本を配置 → WinRE 起動時 Defender Offline Scan の事前実行フラグが BitLocker 自動解除の保護制約を無効化 → SYSTEM シェルで BitLocker 暗号化ボリュームにフルアクセス | [PoC: GitHub/Nightmare-Eclipse (2026-06-11)](https://github.com/) — Microsoft 公式修正なし; 緩和策: TPM+PIN に変更 | **PoC 公開済み・未パッチ・CVE 未採番** / Nightmare Eclipse 7 本目 / YellowKey (CVE-2026-50507) 修正後も 別経路でのBitLocker 回避が残存することが実証 / 盗難ラップトップ・オフライン攻撃シナリオに直結 |
| CVE-2026-12007 | Google Chrome < 149.0.7827.115 (Windows / Core コンポーネント) | CWE-416 / **Critical** | 悪意ある HTML ページが Core の参照カウント管理不備を誘発 → Use-After-Free でレンダラープロセス内に任意コード実行 → サンドボックス脱出連鎖の起点化 | [Chrome 149.0.7827.115 (2026-06-12)](https://chromereleases.googleblog.com/2026/06/) | 2026-06-12 公開 / Critical / 今月 2 回目の Chrome セキュリティ更新 / Chromium 系全ブラウザへの即時適用推奨 |
| CVE-2026-12008 | Google Chrome < 149.0.7827.115 (DigitalCredentials API、全プラットフォーム) | CWE-416 / **Critical** | 侵害済みレンダラープロセスが DigitalCredentials の内部オブジェクト解放後参照を悪用 → サンドボックス外での任意コード実行 → デジタル認証情報 (パスポート・運転免許等) の窃取・改ざん | [Chrome 149.0.7827.115 (2026-06-12)](https://chromereleases.googleblog.com/2026/06/) | 2026-06-12 公開 / Critical / DigitalCredentials API は ID ドキュメント提示に直結するため悪用時の影響が広範 |
| CVE-2026-12009 | Google Chrome < 149.0.7827.115 (Accessibility, macOS) | CWE-20 / **Critical** | 侵害済みレンダラープロセスが Accessibility ツリーの入力バリデーション欠落を悪用 → macOS Accessibility API への不正コマンド注入 → サンドボックス脱出 | [Chrome 149.0.7827.115 (2026-06-12)](https://chromereleases.googleblog.com/2026/06/) | 2026-06-12 公開 / Critical / macOS 固有 / Safari・Firefox の macOS Accessibility 実装へのバリアントハント推奨 |
| CVE-2026-12010 | Google Chrome < 149.0.7827.115 (GPU プロセス, Android) | CWE-787 / **Critical** | 侵害済みレンダラープロセスが GPU プロセスのヒープバッファ境界検査欠落を悪用 → GPU プロセス内で任意コード実行 → Android Sandbox を段階的に脱出しシステムへ横展開 | [Chrome 149.0.7827.115 (2026-06-12)](https://chromereleases.googleblog.com/2026/06/) | 2026-06-12 公開 / Critical / Android GPU ドライバ (Qualcomm Adreno・ARM Mali) の同種 boundary check 欠落へのバリアントハント推奨 |
| CVE-2026-0273 | Palo Alto Networks PAN-OS 10.2/11.1/11.2/12.1 (PA-Series・VM-Series・Panorama、管理 UI/CLI アクセス可能環境) | CWE-88 / **6.1** (CVSS v4.0) | 認証済み管理者が CLI または WebUI の引数処理欠陥に細工コマンドを挿入 → システム制限をバイパスして root 権限で任意 OS コマンドを実行 | [PAN-OS 12.1.4-h7/11.2.4-h18/11.1.4-h34/10.2.7-h35 (2026-06-11 advisory update)](https://security.paloaltonetworks.com/CVE-2026-0273) | 2026-06-11 advisory 更新 / CVSS 6.1 (medium) / 管理者アクセス前提 / PAN-OS の CLI 引数インジェクション系は繰り返し発見されるパターン; 同系 NGFW (Fortinet FortiOS・Cisco FTD 等) の CLI パーサへのバリアントハント推奨 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-06-08 (国内開示) / 2026-06-10〜11 (国際報道) | — / 個人情報保護委員会届出済み | 九州電力送配電 (株) が顧客情報 1,090 万件を記録した外部 SSD の紛失を公表 — 4/27 にバックアップ後 5/26 に紛失発覚、暗号化・パスワード保護なしの SSD が施錠なしキャビネットに保管されていた人的管理不備; 氏名・住所・電力使用量・電話番号を含むが金融情報は非含有。経産省が 7/8 まで詳細報告を要求 | 機密性喪失 / 1,090 万件 | [BleepingComputer](https://www.bleepingcomputer.com/news/security/japanese-energy-firm-loses-drive-with-data-of-109-million-clients/) / [TechRadar](https://www.techradar.com/pro/japanese-electricity-giant-apologises-after-physical-drive-with-data-of-10-9-million-clients-goes-missing) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 30 ソース (GBHackers, CyberSecurityNews, The420.in, Brutecat.com, OpenAI newsroom, TechRadar, The Next Web, PYMNTS, SecurityWeek, CyberSecurityNews, Tom's Hardware, The Register (2026/06/11), Security Affairs, GBHackers, ransomware.live, DeXpose, Tenable, deskmodder.de, Transparency Coalition, NYSenate.gov, SC Media, BleepingComputer, MLex, DataBreaches.net, TechRadar, Palo Alto Networks, CVEFeed, itsecuritynews.info, Push Security, WebSearch aggregate 他)
- 採用件数: AI=3 / Security=4 / CVE=6 / 国内=1
- 採用件数が目安 (AI/Security 各 8〜12件) を下回った理由:
  - 採用窓 (2026-06-11〜13) は June Patch Tuesday (6/9) 直後の週末〜週初めに当たり、主要 AI ラボ・セキュリティベンダーからの新規大型アナウンスが少ない端境期
  - Patch Tuesday 収録の主要 CVE (Windows Kernel / HTTP.sys / Hyper-V / SAP / Veeam 等) は前号 (2026-06-10〜12 各 digest) 収録済み
  - OpenAI S-1 SEC 提出 (6/10) は採用窓外 (June 10)
  - Verizon DBIR 2026 は May 下旬〜June 上旬公開 (採用窓外)
  - Push Security デバイスコードフィッシング急増レポートは約 2 週間前公開 (採用窓外)
- 除外理由内訳:
  - 古すぎ (< 2026-06-11 JST):
    - OpenAI S-1 SEC 提出 (2026-06-10 各紙報道)
    - Anthropic Project Glasswing 150 組織拡大 (2026-06-02/03、前号 excluded)
    - Google Gemma 4 12B GA (2026-06-03、採用窓外)
    - Verizon DBIR 2026 (2026-05下旬〜06上旬公開)
    - CVE-2026-7473 Arista EOS (CISA KEV 2026-06-09 追加)
    - CVE-2026-42271 LiteLLM CISA KEV (2026-06-09 digest 収録)
    - device code phishing Push Security blog (2026-05下旬〜06上旬公開)
    - 九州電力 SSD 紛失 初報 (2026-06-08 日本語報道 / 2026-06-10 DataBreaches.net); 国内 ドメスティック重要度を考慮して borderline として国内セクションに日付注記付きで収録
    - New York AI 法案通過 (2026-06-03〜05 議会可決; 2026-06-12 立法アップデート記事を AI セクションに採用)
  - 重複 (excluded_set 直近7日、全 CVE):
    - CVE-2026-10520/10523 (Ivanti Sentry) / CVE-2026-35273 (Oracle PeopleSoft) / CVE-2026-5027 (Langflow) / CVE-2026-11645 (Chrome V8 KEV) / CVE-2026-42271 (LiteLLM) / CVE-2026-45657 (Windows Kernel TCP/IP) / CVE-2026-45447 (OpenSSL PKCS#7) / CVE-2026-47291 (HTTP.sys) / CVE-2026-47911 (Adobe Acrobat) / CVE-2026-48710 (Starlette) / RoguePlanet / CVE-2026-44748/27671 (SAP) / CVE-2026-44963 (Veeam) / CVE-2026-23111 (Linux nf_tables) / CVE-2026-45586/50507/49160 (Patch Tuesday ZDays) / Hyper-V CVE 群 / CVE-2026-22732 (SAP Spring) / CVE-2026-47737 (Puma) / CVE-2026-50751/50752 (Check Point) / CVE-2026-42897 (Exchange)
    - AudiA6 Europol 閉鎖 (2026-06-11 digest) / ShinyHunters Oracle PeopleSoft (2026-06-12 digest) / Ivanti Sentry 野外悪用 (2026-06-12 digest) / ServiceNow データ漏洩 (2026-06-12 digest) / Claude Fable 5 JB / Claude Managed Agents / npm v12 supply chain changes / OpenAI Oracle 統合 / Google Gemini 障害 (全て 2026-06-12 digest 収録済み)
  - 日付不明/確認不可:
    - CVE-2026-12015 (Chrome Autofill UAF): CVEFeed で確認したが詳細 CVSS 値・NVD 掲載日を 403 により裏取り不可; Chrome 149.0.7827.115 グループとして CVE テーブルに合算記述を検討したが個別採用が困難なため除外し代わりに CVE-2026-12007〜12010 の 4 件を採用
    - OceanLotus SPECTRALVIPER キャンペーン: Check Point 週次レポートに記載あるが具体的な June 11-13 新規発展の有無を確認できず採用除外
    - CVE-2026-47281 (RoguePlanet): CVSS 9.6 という値は複数媒体が言及するが NVD 未採番で信憑性不明; The Register は CVE 未採番とレポートしているため CVE テーブルへの採用除外 (GreatXML と同様の未採番扱い; RoguePlanet は 2026-06-11 digest に採録済み)
- 取得失敗ソース (HTTP 403): gbhackers.com 個別記事 / securityweek.com 個別記事 / cybersecuritynews.com 個別記事 / bleepingcomputer.com 個別記事 / openai.com 個別記事 / brutecat.com / tom's hardware 個別記事 / theregister.com 個別記事 / security.paloaltonetworks.com / chromereleases.googleblog.com / jpcert.or.jp / jvn.jp — WebSearch スニペット・複数独立媒体の記事・URL パターン (例: deskmodder.de の "2026/06/12" URL で Chrome 149.0.7827.115 の 6/12 リリースを確認) で内容・日付を補完

</details>
