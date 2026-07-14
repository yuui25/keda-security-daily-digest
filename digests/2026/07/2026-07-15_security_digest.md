# KEDA Daily Digest — 2026-07-15 (JST)

> 採用範囲: 公開日 2026-07-13 〜 2026-07-15 (JST)
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Microsoft が 7/14 の Patch Tuesday で史上最多 569 CVE を修正 — Active Directory Federation Services (CVE-2026-56155) と SharePoint Server (CVE-2026-56164) のゼロデイ 2 件が野生悪用中で即時パッチ適用が必要。SAP も同日に CVE-2026-44747 (NetWeaver AS ABAP CVSS 9.9) と CVE-2026-27690 (Approuter HTTP Request Smuggling CVSS 9.1) を公開し、エンタープライズ基盤への重複プレッシャーが続く。AI 面では習近平が 7/17 開幕の上海 WAIC 2026 で初の基調講演に臨み中国が「世界 AI 協力機構 (WAICO)」設置を提案、一方 Anthropic は Claude for Chrome の ClaudeBleed 欠陥を 8 パッチ後も放置したまま批判を受けており、AI プロダクトのセキュリティ対応速度が問われている。

## AI 関連ニュース

- **[2026-07-14]** [Anthropic が Artifacts に公開共有・マルチプレイヤー編集を追加、Claude Tag (Slack) 経由での生成にも対応](https://cryptobriefing.com/anthropic-claude-sharing-team-editing-features/) — 公開リンクを持つ誰でも Claude アカウントなしで Artifact を閲覧可能に; チームが同一 Artifact をリアルタイムで共同編集できるマルチプレイヤー編集をサポート; Slack の Claude Tag チャンネルで @Claude をタグするだけで Artifact 生成が可能になり、個人ツールからチーム協働ツールへの転換を推進 *(CryptoBriefing / TestingCatalog)*

- **[2026-07-13]** [習近平が WAIC 2026 (7/17〜20・上海) に初参加・基調講演 — 中国が「世界 AI 協力機構 (WAICO)」の上海設置を提案し AI ガバナンスの国際規格形成へ本格参入](https://news.cgtn.com/news/2026-07-13/Xi-to-attend-and-address-opening-ceremony-of-2026-World-AI-Conference-1OKgsIkkofu/p.html) — テーマ「Intelligent Partners, Co-create the Future」で 1,100 企業以上が出展、展示フロアが初めて 10 万平方メートルを超える規模; Hinton・Bengio・Sutton を含む 9 名のノーベル/チューリング賞受賞者が参加; 並行開催の AI ガバナンス高級会合で WAICO 設置提案を正式提出予定 *(CGTN / SCMP / TheNextWeb)*

- **[2026-07-13]** [TSMC が Q2 売上 $39.62B (前年比 +36%) で過去最高を記録 — 6 月単月売上は前年同月比 +67.9% で同社 38 年史上最大、AI チップ収益が年間 $40B 超・総売上の 25% 超のペース](https://www.cnbc.com/2026/07/13/tsmc-june-revenue-rises-percent-ahead-second-quarter.html) — 上半期売上 NT$2.404 兆 (+35.6% YoY); Q2 通期決算は 7/16 公表予定; AI サーバー向け CoWoS 積層パッケージングと N3/N2 先端プロセスが主導 *(CNBC / TechTimes)*

- **[2026-07-14]** [CrowdStrike・Palo Alto Networks・Cloudflare の株価が急騰 — Anthropic Claude Mythos が「主要ソフトウェア全域で 10,000 件超の脆弱性を発見」との評価が投資家のリスク認識を変化させた結果と報道](https://www.tipranks.com/news/crwd-panw-net-heres-why-cybersecurity-stocks-are-jumping-today-july-14-2026) — Mythos は expert-level CTF タスクで成功率 73%、主要 OS・ブラウザのゼロデイを自律発見; AI 主導の脆弱性発見加速がヒューマン専門家への需要を減らすリスクとセキュリティツール需要の双方向性が市場で意識された *(TipRanks / SecurityWeek)*

## セキュリティ関連ニュース

- **[2026-07-14]** [Microsoft Patch Tuesday 2026-07 — 569 CVE 修正 (史上最多・前記録 198 を 2.8 倍更新)、ADFS/SharePoint のゼロデイ 2 件が野生悪用中で即時対応必須](https://www.bleepingcomputer.com/news/microsoft/microsoft-july-2026-patch-tuesday-fixes-massive-570-flaws-3-zero-days/) — 56 件 Critical (うち 48 件が RCE) / 510 件 Important / 3 件 Moderate; ゼロデイは CVE-2026-56155 (ADFS EoP、DART 発見) と CVE-2026-56164 (SharePoint EoP、Mandiant/Google 発見) の 2 件が野生悪用、CVE-2026-50661 (BitLocker バイパス、物理アクセス必要) は未悪用; EoP が全体の 43.8% を占める *(BleepingComputer / Tenable / Security Boulevard)*

- **[2026-07-13/14]** [CrashStealer — Apple クラッシュレポートツールに偽装した macOS インフォスティーラーが Keychain・14 種パスワードマネージャー・80 暗号資産ウォレットを窃取、正規 Developer ID で Gatekeeper も突破](https://www.helpnetsecurity.com/2026/07/14/crashstealer-macos-infostealer-password-theft/) — C++ ネイティブ実装で Atomic (AMOS)/MacSync と別系統の新マルウェアファミリー; "Werkbit Setup" という DMG として配布、公証チケット付きでインストール時 Gatekeeper の警告なし; macOS 標準のパスワード認証ダイアログを模倣してシステムログイン認証情報を窃取; Apple は使用 Developer ID を失効済み *(Jamf Threat Labs / Help Net Security / Forbes)*

- **[2026-07-14]** [SAP 7 月パッチ日 — 16 件の新規セキュリティノートで CVE-2026-44747 (NetWeaver AS ABAP CVSS 9.9) と CVE-2026-27690 (Approuter HTTP Request Smuggling CVSS 9.1) を含む多数のクリティカル欠陥を修正](https://www.securityweek.com/sap-patches-critical-vulnerabilities-in-netweaver-approuter-commerce-cloud/) — CVE-2026-44747 はカーネルレベルの修正を要するため計画停止が必要; Approuter は SAP BTP/Cloud Foundry ランドスケープの全認証フロント層として広く利用されており CVE-2026-27690 の影響範囲が広大 *(SecurityWeek / GBHackers / Cyberpress)*

- **[2026-07-14]** [ClaudeBleed 未修正 — Claude for Chrome v1.0.80 (2026-07-07 リリース) でも 2 欠陥が再現、他 Chrome 拡張が 6 行の JavaScript で Gmail・Google Docs・Google Calendar をフルリード可能な状態が 8 パッチを経ても継続](https://www.securityweek.com/unpatched-claude-for-chrome-flaw-lets-extensions-read-gmail-calendar/) — event.isTrusted チェック欠如 → 任意の chrome.ai アクセス権を持つ拡張機能が Claude のプロンプト実行を偽造; Manifold 研究者が 2026-05 に Anthropic へ報告済みだが 2 ヶ月後の最新版でも未修正; 企業環境で Claude for Chrome を利用中の場合はサードパーティ拡張機能の権限を即時審査推奨 *(SecurityWeek / THN)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-07-13 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-56155 | Windows Active Directory Federation Services (全 in-support バージョン) | CWE-269 / **7.8** | ADFS が「細粒度不十分のアクセス制御」でトークン処理 → 認証済み攻撃者がドメイン管理者権限を不正取得 → EoP | [MSRC 2026-07-14](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-56155) | **野生悪用確認** / Microsoft DART 発見 / Patch Tuesday 2026-07 |
| CVE-2026-56164 | Microsoft SharePoint Server 2016 / 2019 / SE | CWE-269 / **5.3** | SharePoint のリクエスト処理が権限昇格に対する認可チェックを欠く → 認証済み攻撃者が管理者権限取得 → EoP | [MSRC 2026-07-14](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-56164) | **野生悪用確認** / Mandiant IR・Google Cloud FLARE OTF 発見 / Patch Tuesday 2026-07 |
| CVE-2026-50661 | Windows BitLocker (全 in-support バージョン) | CWE-287 / Moderate | 物理アクセスを持つ攻撃者が特定手順で BitLocker デバイス暗号化をバイパス → 暗号化ドライブのデータに直接アクセス | [MSRC 2026-07-14](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-50661) | Patch Tuesday 2026-07 / 物理アクセス要件あり |
| CVE-2026-44747 | SAP NetWeaver AS ABAP (KRNL64NUC/UC 7.22〜7.22EXT / KERNEL 7.22〜9.20) | CWE-119 / **9.9** | 認証済み低権限ユーザーがネットワーク経由でカーネルのメモリ管理ロジックエラーをトリガー → カーネルメモリ破壊 → 不正データアクセス/改ざん/DoS (RCE ポテンシャル) | [SAP Note 3747367](https://support.sap.com/en/my-support/knowledge-base/security-notes-news/july-2026.html) | CVSS 9.9 / 広範 ERP 基盤 / カーネルパッチ要計画停止 |
| CVE-2026-27690 | SAP Approuter (node.js) < 20.10.0 | CWE-444 / **9.1** | 非 Cloud Foundry 環境の Approuter が細工 HTTP リクエストを誤処理 → HTTP Request Smuggling → 後段サービスの認証バイパス・キャッシュポイズン → 未認証アクセス | [SAP Note 3720138](https://support.sap.com/en/my-support/knowledge-base/security-notes-news/july-2026.html) | CVSS 9.1 / 未認証 / SAP BTP 広範 API GW 影響 / protocol-level バグクラスで他言語実装への水平伝播候補 |
| CVE-2026-60121 | VITEC Flamingo 4.12.2 (PHP, ビデオ管理システム) | CWE-78 / **9.8** | `admin/ajax/ping.php` が `escapeshellarg()` 後に argv 経由で未エスケープ値を第 2 の `shell_exec()` に渡す (double-eval) → 未認証 OS コマンドインジェクション → passwordless sudo で root 権限任意コマンド実行 (未パッチ) | [THREATINT](https://cve.threatint.eu/CVE/CVE-2026-60121) (未パッチ) | 2026-07-14 公開 / CVSS 9.8 / 未認証 / 未パッチ / double-eval escape-bypass パターン水平伝播候補 |
| CVE-2026-61498 | VITEC Flamingo 4.12.2 (PHP) | CWE-78 / **9.8** | `admin/ajax/gen_graphs.php` が start/end/key/format GET パラメーターをサニタイズせず `passthru()` に渡す → 未認証 OS コマンドインジェクション → root 権限任意コマンド実行 (未パッチ) | [THREATINT](https://cve.threatint.eu/CVE/CVE-2026-61498) (未パッチ) | 2026-07-14 公開 / CVSS 9.8 / 未認証 / 未パッチ / passthru() 直接渡しパターン |
| CVE-2026-14934 / GHSA-c9x2-6hqc-cm9v | Google Cloud BigQuery / Dataform / Colab Enterprise (2025-10〜2026-05-10 の全バージョン) | CWE-862 / **9.4** | リポジトリ作成機能が呼び出し元テナントの認可チェックを欠く → 認証済み攻撃者が他テナントのリポジトリを乗っ取り → cross-tenant データアクセス/改ざん (2026-05-10 Google 側パッチ済み・顧客対応不要) | [GHSA-c9x2-6hqc-cm9v](https://github.com/advisories/ghsa-c9x2-6hqc-cm9v) | 2026-07-13 CVE 公開 / CVSS 9.4 / マルチテナント認可欠如パターン / 同仕様の内部サービス全般へ水平伝播候補 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|---|---|---|---|---|
| 2026-07-13 | JVNVU#94203999 / CERT/CC VU#564823 | GNU Wget の FTP PASV レスポンス IP アドレス未検証 → 攻撃者制御 FTP サーバーが内部 IP を返すことで内部ネットワーク探索 (SSRF) が可能 | Medium / SSRF / 内部ネットワーク情報漏洩 | [JVNVU#94203999](https://jvn.jp/vu/JVNVU94203999/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| BleepingComputer / Tenable / Security Boulevard (Patch Tuesday 2026-07) | 2026-07-14 公開・569 CVE・ゼロデイ 3 件確認 ✓ |
| Help Net Security / Jamf / Forbes / BleepingComputer (CrashStealer) | 2026-07-13〜14 公開・Apple Insider 2026-07-13 初報確認 ✓ |
| SecurityWeek / GBHackers / Cyberpress (SAP July 2026 Patch Day) | 2026-07-14 SAP パッチ日確認 ✓ |
| SecurityWeek / THN (ClaudeBleed unpatched July 14) | SecurityWeek "July 14, 2026" 付き記事確認 ✓ |
| CryptoBriefing / TestingCatalog X (Anthropic Artifacts multiplayer) | TestingCatalog X post 2026-07-14 確認 ✓ |
| CGTN / SCMP / TheNextWeb (WAIC 2026 / 習近平) | CGTN 2026-07-13 公式発表確認 ✓ |
| CNBC / TechTimes (TSMC Q2 record earnings) | CNBC 2026-07-13 確認 ✓ |
| TipRanks (Cybersecurity stocks CRWD/PANW/NET) | 2026-07-14 TipRanks 記事確認 ✓ |
| THREATINT / cvebrief.com (VITEC Flamingo CVE-2026-60121 / CVE-2026-61498) | 2026-07-14 公開・CVSS 9.8 双方確認 ✓ |
| GitHub Advisories (GHSA-c9x2-6hqc-cm9v / CVE-2026-14934 Google Cloud) | 2026-07-13 CVE 公開・CVSS 9.4 確認 ✓ |
| JVN (JVNVU#94203999 GNU Wget SSRF) | 2026-07-13 11:45 JVN 公開確認 ✓ |
| CISA KEV (2026-07-13〜14) | 直近 KEV 追加は 2026-07-10 のみ (iCagenda/Balbooa Forms) — 07-14 新規追加なし確認 |
| thehackernews.com / bleepingcomputer.com | 403 — WebSearch スニペットで代替 |
| nvd.nist.gov | 403 — WebSearch スニペット代替 |
| openai.com / meta.com / google deepmind | 07-13〜14 窓内の新規発表 → 07-15 リリース前の期待記事のみで採用対象なし |

### 集計サマリ

- **巡回ソース数**: 約 25
- **採用件数**: AI=4 / Security=4 / CVE=8 / 国内=1
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-07-13 より前): Goldman Sachs 中国 AI 推奨 (CNBC 2026-07-12) / ByteDance Seedream 5.0 Pro (2026-07-08〜09) / OpenAI 米政府 5% 株式提案 (2026-07-02〜03) / Claude Mythos 10,000 件脆弱性報告 (Help Net Security 2026-05-26、赤 Anthropic 2026-04) / Project Glasswing 詳細 (Anthropic 2026-06)
  - 重複 (直近 7 ダイジェスト掲載済み): UK CTP (07-14掲載) / Nightmare-Eclipse 断念 (07-14掲載) / DIRAC CVE-2026-61667/45579 (07-14掲載) / Gemini 3.5 Pro July 17 目標 (07-13掲載) / GPT-5.6 Sol Ultra CDC Conjecture (07-13掲載) / U-Boot BRLY-2026-037〜042 (07-13掲載) / Zimbra Classic XSS (07-13掲載) / jscrambler npm supply chain (07-13掲載) / File Browser CVE-2026-54088 (07-13掲載) / ImageMagick CVE-2026-61861 (07-13掲載) / PraisonAI CVE-2026-61442/61447/61445 (07-12/13掲載) / Apple vs OpenAI (07-12掲載) / Progress ShareFile (07-12掲載)
  - 日付不明/取得失敗: SonicWall CVE-2026-15409/15410 (CVE 番号は検索スニペットで言及されたが PSIRT 等での公開日の独立裏取りが取得不能のため除外)
  - 採用見送り: Gemini 3.5 Pro + WAIC 7/17 重複イベント記事 (Gemini 3.5 Pro 部分は 07-13 掲載済みのため WAIC 単独イベントとして分離採用)

### 主要採用補足

- **Microsoft Patch Tuesday CVE-2026-56155/56164/50661**: 07-14 digest は公開前の「予定」として URL のみ掲載。本 digest では Tenable (2026-07-14) / BleepingComputer (2026-07-14) による正式公開後の詳細を採用
- **ClaudeBleed**: Lyrie Research 初報 2026-05-10 (採用窓外) だが SecurityWeek が 2026-07-14 に「v1.0.80 でも未修正」として独立報道 → 07-14 付き新報として採用
- **VITEC Flamingo CVE-2026-60121/61498**: CVEBrief "July 14, 2026" 付き掲載・THREATINT 個別 CVE ページで技術詳細確認 ✓ / ベンダーパッチ未公開
- **CVE-2026-14934**: Google Cloud が 2026-05-10 にバックエンドパッチを適用済み (顧客対応不要) だが CVE 番号および GHSA の正式公開は 2026-07-13 → 採用範囲内

</details>

---

*excluded_set 参照: 直近 7 ダイジェスト (2026-07-08 〜 2026-07-14) の全 CVE/GHSA/URL を除外済み。*
