# KEDA Daily Digest — 2026-06-28 (JST)

> 採用範囲: 公開日 2026-06-26 〜 2026-06-28
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

週末 (土〜日) にあたり大型 AI モデルリリースは少なかったが、セキュリティ面では注目が続いた。FBI・CISA がロシア情報機関 UNC5792 による Signal バックアップリカバリキー窃取フィッシングの進化版を警告——キーを奪われると電話番号変更後も旧履歴へのアクセスが維持されるため政府関係者・ジャーナリストへの影響は深刻。OpenAI の「Poisoned Tenant」攻撃では ChatGPT 正規招待機構が武器化されサイバーセキュリティ企業が標的化、Bluekit PhaaS は BitM で MFA すら無効化する洗練度に達した。pnpm パッケージマネージャーに 6 件のレジストリ供給データ不信問題が一括公開され、サプライチェーン信頼境界の再点検が急務となっている。

## AI 関連ニュース

- **[2026-06-27]** [OpenAI「Poisoned Tenant」— 攻撃者が正規 ChatGPT 組織招待を悪用しサイバーセキュリティ企業を偽テナントに誘導](https://www.bleepingcomputer.com/news/security/cybersecurity-firms-targeted-by-fraudulent-openai-organization-invites/) — Push Security が発見; 攻撃者は Gmail で偽 OpenAI 組織を作成し noreply@tm.openai.com からの本物の招待メール (SPF/DKIM パス) を送信; 被害者に Owner 権限を付与してチャット内の機密情報・プロジェクトデータを窃取; 「組織への招待」がプラットフォーム認証をバイパスする新クラスの BEC 手法 *(BleepingComputer / Push Security)*

- **[2026-06-26]** [CNBC: OpenAI・Anthropic ユーザーが「tokenmaxxing」から ROI 優先へ転換——企業 AI 支出に急ブレーキ](https://www.cnbc.com/2026/06/26/openai-anthropic-new-ai-spending-reality-as-users-shift-to-efficiency.html) — Uber が AI ツールの月間上限を $1,500 に設定し年間予算を4ヶ月で消化したと判明; Lindy CEO が Claude から DeepSeek に 100% 移行しコストを劇的に削減; IPO 前夜に「intelligence per dollar」が企業 AI の新 KPI へ転換 *(CNBC)*

- **[2026-06-26]** [CNBC: Zhipu / Z.ai が OpenAI・Anthropic の政府規制の隙をつき急接近——GLM-5.2 が FrontierSWE で GPT-5.5 を 1/6 コストで上回る](https://www.cnbc.com/2026/06/26/china-zhipu-z-ai-open-source-anthropic-openai.html) — Z.ai GLM-5.2 (753B パラメータ, MIT ライセンス, 1M コンテキスト) が FrontierSWE ベンチマークで GPT-5.5 を上回り Opus 4.8 に迫る; GPT-5.6 Sol が政府承認ゲートに縛られる間、中国オープンモデルが企業の代替として急速に存在感を拡大 *(CNBC)*

- **[2026-06-26]** [GPT-4.5 が ChatGPT・API から退役完了——リリース4ヶ月の短命、6/27 付けで API コールがエラーに](https://openai.com/index/retiring-gpt-4o-and-older-models/) — 2026-06-26 に ChatGPT・カスタム GPT から削除、2026-06-27 に API が終了 (6/3 発表からわずか23日で実施); ChatGPT ユーザーは GPT-5/5.5 に自動移行; GPT-5.3-Codex・GPT-5 に完全代替されわずか4ヶ月の短命で退役; GPT-5.6 Sol への移行加速の布石 *(OpenAI)*

## セキュリティ関連ニュース

- **[2026-06-26]** [FBI・CISA が Signal バックアップリカバリキーを狙うロシア諜報機関の新フィッシング手口を警告](https://www.bleepingcomputer.com/news/security/fbi-russian-hackers-now-target-signal-backup-recovery-keys/) — UNC5792/UNC4221 (FSB 帰属) が Signal サポートを偽装し「必須 2FA 設定」として Signal バックアップの設定画面を開かせリカバリキーを詐取するよう誘導; キーを奪われると電話番号を変更しても攻撃者は旧メッセージ履歴にアクセス可能; 現・元政府高官・軍・ジャーナリスト・ウクライナ関係者が標的; 国務省は UNC5792 情報提供者に最大 $10M の懸賞金を設定 *(FBI/CISA / BleepingComputer / The Next Web)*

- **[2026-06-26]** [Polymarket が第三者ベンダー経由のフロントエンドスクリプト注入で $3M 流出——11ウォレットが標的に](https://www.bleepingcomputer.com/news/security/polymarket-customers-lose-3-million-in-supply-chain-attack/) — 侵害されたサードパーティプロバイダーが悪意ある JS を Polymarket のフロントエンドに注入; ウォレット接続時に PUSD への不正承認署名を誘導; PeckShield は被害額を $2.94M、Polygon → Ethereum ブリッジ経由で 1,893 ETH に変換と推定; Polymarket は依存関係を除去し全額返金を表明; 過去2ヶ月で2件目のインシデント (5月に旧秘密鍵漏洩で $700K 流出) *(BleepingComputer / The Next Web / TechCrunch)*

- **[2026-06-26]** [Bluekit PhaaS が browser-in-the-middle (BitM) 機能を追加——MFA を無効化して Microsoft 認証情報を窃取](https://www.bleepingcomputer.com/news/security/bluekit-phishing-kit-adopts-browser-in-the-middle-for-login-theft/) — Netcraft が分析; 正規 Microsoft ログインページを攻撃者制御ブラウザ内に読み込み、rrweb JS ライブラリで DOM をシリアライズして WebSocket 経由でリアルタイム中継; CSS ランダマイズ・1MB 超難読化バンドル・カスタム CAPTCHA・ブラウザフィンガープリント・WebRTC IP ミスマッチ検知で分析回避; 70+ 新ホスト名を直近1週間で確認; bluekit[.]ws・cc・su・pk が既知 C2 *(BleepingComputer / Netcraft)*

- **[2026-06-26]** [Microsoft が Windows 10 無償 ESU を予告なく 2027年10月まで1年延長——非公式に仕様変更](https://www.bleepingcomputer.com/news/microsoft/microsoft-quietly-extends-free-windows-10-esu-support-to-october-2027/) — 当初の終了予定 2026-10-13 から 2027-10-12 へ1年延長; Windows Backup 有効化または Microsoft Rewards 1,000pt 交換で無償登録可能 (別途 $30 課金プランも); 正式発表なしに文書更新のみで告知; Windows 10 22H2 デバイスが大量残存する企業環境のパッチ適用期間を延長、攻撃面管理の観点では移行圧力が緩む副作用も *(BleepingComputer / Help Net Security / PCWorld)*

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-26 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-55700 | pnpm (npm パッケージマネージャー) < 11.5.3 | CWE-22 / **8.2** | `pnpm stage download` がレジストリ提供マニフェストの `name`/`version` フィールドを検証なしにローカルファイル名として使用 → パストラバーサル (`../`) でダウンロードディレクトリ外に任意ファイル書き込み → サプライチェーン汚染・PNPM_HOME 上書き | [pnpm/pnpm commit 65443f4 (PR#12303, v11.5.3)](https://github.com/pnpm/pnpm/releases/tag/v11.5.3) | 2026-06-26 GitHub Advisory 公開 / npm エコシステム全体に影響 / レジストリ提供フィールドを未検証でファイルパスに使うパターン → yarn berry / Bun 等の同種ステージングコマンドへバリアントハント推奨 |
| CVE-2026-55698 | pnpm (npm パッケージマネージャー) < 11.5.3 | CWE-829 / **8.0** | `env` ロックファイルの `packageManager` フィールドが pnpm の正規バージョン解決をショートサーキット → 攻撃者が細工したロックファイルを注入すると指定バイト列を pnpm として実行 → 任意コード実行 | [同上 (v11.5.3 バッチ修正)](https://github.com/pnpm/pnpm/releases/tag/v11.5.3) | 2026-06-26 公開 / ロックファイルの信頼境界違反パターン / Corepack / volta 等の同種ツールチェーン選択機能へバリアントハント推奨 |
| GHSA-qrv3-253h-g69c | pnpm (npm パッケージマネージャー) < 11.5.3 | CWE-22 / **高** | `configDependencies` env ロックファイルの依存関係名をパス検証なしに `node_modules/.pnpm-config` 内のファイル名として使用 → 細工した依存関係名でディレクトリ外への symlink 作成 → 任意ファイルポインタをインジェクト | [同上 (v11.5.3 バッチ修正)](https://github.com/pnpm/pnpm/releases/tag/v11.5.3) | 2026-06-27 GitHub Advisory 公開 / pnpm 同バッチ6件のうち最もエスカレーション性が高いシムリンク攻撃 / 同種 symlink チェックを持つ Node.js パッケージマネージャー全般へバリアントハント推奨 |
| CVE-2026-49340 | sentriz/gonic (Go 製 Subsonic 互換音楽ストリーミングサーバー) < 0.21.0 | CWE-22 / **8.8** | `ServeCreateOrUpdatePlaylist` のロジックエラーにより認証済みユーザーが M3U プレイリスト内容を攻撃者指定の **絶対パス** に `0o777` パーミッションで書き込み + 中間ディレクトリを作成可能 → Web 公開の gonic ホスト上で cron 等への書き込みを経た RCE に転用可能 | [gonic commit 0824bed (v0.21.0)](https://github.com/sentriz/gonic/commit/0824bed88f6bbc490ba28bf09d28e5dfeb07b445) | 2026-06-27 GHSA 公開 / Subsonic API の `createPlaylist` エンドポイント固有; 任意ファイル書き込みから RCE への転用可能性 / Navidrome・Airsonic 等の同種 Subsonic 実装のファイルパス処理へバリアントハント推奨 |
| CVE-2026-49338 | sentriz/gonic (Go 製 Subsonic 互換音楽ストリーミングサーバー) < 0.21.0 | CWE-285 / **7.5** | `/rest/deletePlaylist.view` と `/rest/getPlaylist.view` がリソースごとの認可チェックを欠落 → 任意認証済みユーザーが他ユーザーのプレイリスト ID (base64url エンコードの `<userID>/<filename>.m3u`, 小整数 userID) を推測して削除・読取可能 | [gonic commit 0824bed (v0.21.0)](https://github.com/sentriz/gonic/commit/0824bed88f6bbc490ba28bf09d28e5dfeb07b445) | 2026-06-27 GHSA 公開 / ID 推測可能な IDOR パターン / Subsonic API 仕様を実装する他のサーバーに同種の認可チェック欠落がある可能性 → Navidrome・Airsonic・Supysonic 等へバリアントハント推奨 |

## 国内脆弱性・インシデント情報

> 直近2日間 (2026-06-27〜28) に採用基準を満たす新規国内脆弱性・インシデントは確認できませんでした。

JVN / JPCERT/CC の巡回では、NEC ExpressUpdate Agent CVE-2026-8797 (2026-06-26) および東芝 Dynabook CVE-2026-56129 (2026-06-26) が最新アドバイザリとして確認されたが、いずれも前日 (2026-06-27) ダイジェスト掲載済みのため再掲は見送った。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 25 ソース (BleepingComputer / Push Security / PRSOL.CC (OpenAI Poisoned Tenant), CNBC ×2 (tokenmaxxing/efficiency, Zhipu Z.ai), OpenAI Help Center / ghacks.net (GPT-4.5 退役), FBI/CISA / BleepingComputer / The Next Web / SecurityAffairs / GuardianMSSP (Signal UNC5792), BleepingComputer / The Next Web / TechCrunch / crypto-economy.com / bitcoinfoundation.org (Polymarket), BleepingComputer / Netcraft / CyberSecurityNews (Bluekit BitM), BleepingComputer / Help Net Security / PCWorld / Tom's Hardware (Windows 10 ESU), GitHub Advisory Database / DailyCVE / radar.offseq.com / bitninja.com (pnpm + gonic CVEs), JVN / JPCERT/CC (国内))
- 採用件数: AI=4 / Security=4 / CVE=5 / 国内=0
- AI 件数が目安 (8〜12) を下回った理由:
  - 採用窓 (2026-06-26〜28) は土〜月の週末にあたり AI ラボの大型発表が少ない閑散期
  - GPT-5.6 Sol/Terra/Luna 一般公開展開: 2026-06-27 digest 掲載済み → 除外
  - Anthropic Fable 5 禁止令仮差止命令: 2026-06-27 digest 掲載済み → 除外
  - Anthropic vs Alibaba 大規模 distillation 攻撃: Bloomberg/CNBC が 2026-06-24 初報 → 採用窓外 (< 2026-06-26)
  - OpenAI June 2026 脅威レポート (PRC 影響工作): 2026-06-10 公開 → 採用窓外
  - Gemini 3.5 Pro: 依然限定プレビューのみ (GA 未到達)、予測市場で 6/30 前 GA 確率 50-55% → 採用対象外
  - NAVER/NVIDIA 主権 AI 提携: 2026-06-07 発表 → 採用窓外
  - Qualcomm/Tenstorrent 買収交渉: 2026-06-15-16 報道、正式発表なし → 採用窓外
  - arXiv cs.CR 直近新着: 採用窓内に AI セキュリティの重要新論文を確認できず
- Security 件数が目安 (8〜12) を下回った理由:
  - CISA KEV 追加: 直近の追加は 2026-06-23 (UniFi OS/Lantronix) で採用窓内の新規追加なし
  - Device code phishing 37x spike (Huntress): Axios 初報 2026-06-23 → 採用窓外
  - OpenAI June 2026 脅威レポート: 2026-06-10 → 採用窓外
  - Unit42 Screening Serpens report: 2026-06 中旬公開 → 採用窓外
  - Turla STOCKSTAY: 2026-06-27 digest 掲載済み
  - Hotel Photo ZIP フィッシング: 2026-06-27 digest 掲載済み
  - Mistic/KongTuke: 2026-06-26 digest 掲載済み
- 除外理由内訳:
  - 古すぎ (公開日 < 2026-06-26): Anthropic/Alibaba distillation (6/24), OpenAI threat report (6/10), Unit42 Screening Serpens (6/13頃), NAVER/NVIDIA (6/7), Qualcomm/Tenstorrent (6/15-16), Nintendo ShadowByt3$ (6/12), Device code phishing Huntress (6/23), OpenAI StealC/Amadey report (6/24 - 06-25 digest 掲載済み)
  - 重複 (excluded_set 直近 7 ダイジェスト 2026-06-21〜2026-06-27):
    - CVE-2026-43503 DirtyClone (2026-06-27 digest)
    - CVE-2026-12569 PTC Windchill CISA KEV (2026-06-27 digest)
    - CVE-2026-48755/48769 Incus (2026-06-27 digest)
    - CVE-2026-8797 NEC ExpressUpdate / CVE-2026-56129 Dynabook (2026-06-27 digest)
    - CVE-2026-20245 Cisco SD-WAN / CVE-2026-10712/10086/12053 GitLab (2026-06-26 digest)
    - CVE-2026-47145〜47151 EmberZNet Zigbee (2026-06-26 digest)
    - Turla STOCKSTAY / Hotel phishing / Klue 続報 / Miasma (2026-06-27 digest)
    - macOS.Gaslight / OpenAI Jalapeño (2026-06-26 digest)
    - Operation Endgame / CISA UniFi OS KEV (2026-06-25 digest)
    - Cordyceps GitHub Actions / Claude Tag (2026-06-25 digest)
  - 取得失敗ソース (HTTP 403): unit42.paloaltonetworks.com, bleepingcomputer.com (個別記事), jvn.jp, jpcert.or.jp/wr, openai.com, cdn.openai.com (PDF) — WebSearch スニペット・複数独立媒体・GitHub Advisory Database で内容・日付を補完
  - 日付確認できず採用見送り: Polymarket は TechCrunch が 6/25 初報のため境界ライン上だが、BleepingComputer/The Next Web 等が 6/26 に確認・拡散したことを根拠に 6/26 として採用

</details>

---

*excluded_set 参照: 直近7ダイジェスト (2026-06-21〜2026-06-27) の全 CVE/GHSA/URL を除外済み。*
