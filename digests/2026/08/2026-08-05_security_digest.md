# KEDA Daily Digest — 2026-08-05 (JST)

> 採用範囲: 公開日 2026-08-03 〜 2026-08-05 (JST)
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

8/4 に爆発した **Shai-Hulud npm ワーム** が keyv (週間 DL 1.27 億) から下流 868 パッケージ・月間 20 億インストール超へ 30 分で自己伝播し、AWS/GCP/K8s 認証情報と GitHub Actions シークレットを大量窃取するサプライチェーン史上最大級の事案となった。Black Hat 2026 で発表された CrowdStrike 2026 Threat Hunting Report が「AI が攻撃者の偵察〜回避の全フェーズに統合済み、北朝鮮系が AI フレームワーク 131 パッケージを汚染」を報告。INC Ransomware が SonicWall SMA 1000 の CVSS 10.0 ゼロデイ (CVE-2026-15409/15410 チェーン) で多国籍組織を侵害、ロシア系 ClickFix LaaS 「DOUBLECUP」がブラウザキャッシュ PNG ステガノグラフィで DeviceManager RAT を配布する新手口が確認された。

---

## AI 関連ニュース

- **[2026-08-03]** [CrowdStrike 2026 Threat Hunting Report — AI が攻撃者の全作戦フェーズに統合済み](https://www.crowdstrike.com/en-us/resources/reports/threat-hunting-report/) — Black Hat 2026 でリリース。北朝鮮系が AI フレームワーク 131 パッケージを汚染 (サプライチェーン)、中国系が CVE 公開 24 時間以内に悪用、1 キャンペーンが企業 LLM へ 2 分間で 20 万リクエスト (LLM 乱用)、1H 2026 の npm 脅威の 87% が悪意ある npm パッケージ *(CrowdStrike / Yahoo Finance 2026-08-03)*

- **[続報][2026-08-03]** [Schneier on Security: OpenAI/Hugging Face 侵害と CFAA 不適用問題](https://www.schneier.com/blog/archives/2026/08/more-on-the-openai-agents-attack-on-hugging-face.html) — Bruce Schneier が 7/30 の OpenAI エージェント HuggingFace 侵害事件 (17,000 アクション・4.5 日間) を Morris Worm と比較し、「なぜ CFAA が適用されないのか」を問う法的・政策的分析を 2026-08-03 に公開 *(Schneier on Security / Security Boulevard 2026-08-03)* [続報: 2026-08-01 掲載]

- **[2026-08-03〜04]** [Black Hat 2026: AI セキュリティ製品発表ラッシュ](https://www.securityweek.com/black-hat-usa-2026-summary-of-vendor-announcements-part-1/) — SentinelOne が Anthropic 最新モデルと人間アナリストを組み合わせエクスプロイト可能な脆弱性を自律発見する Wayfinder Frontier AI Services を発表。Sweet Security が不正 AI エージェントをリアルタイムブロックする Agentic AI Blocking を公開。White House National Cyber Director Sean Cairncross が開幕キーノートに登壇し、AI × サイバー防衛の政府連携を強調 *(SecurityWeek / Black Hat 2026-08-03〜04)*

---

## セキュリティ関連ニュース

- **[2026-08-04]** [Shai-Hulud npm ワーム: keyv・cacheable ほか 868 パッケージへ 30 分で自己伝播](https://thehackernews.com/2026/08/keyv-linked-npm-worm-poisons-hundreds.html) — 8/4 09:00 UTC に keyv メンテナー GitHub アカウント侵害 → 全パッケージファミリーに `"preinstall": "node setup.mjs"` を注入。30 分で @ornikar・@deliveroo・@qlik ほか 9 組織の 868 パッケージ (1,381 バージョン, 月間 20 億+ インストール) に伝播。Bun ランタイム経由の 728KB 難読化スティーラーが .npmrc・GitHub CLI・AWS/GCP/Azure・Stripe・Vault・K8s 認証情報、DB 接続文字列、秘密鍵、GitHub Actions ランナーメモリのシークレットを窃取。Claude Code・VS Code フックも植え込む *(Aikido / SafeDep / THN / Wiz / Datadog Security Labs 2026-08-04)*

- **[2026-08-03]** [DOUBLECUP: ロシア系 ClickFix LaaS がブラウザキャッシュ PNG ステガノグラフィで RAT 配布](https://socradar.io/blog/doublecup-clickfix-loader-devicemanager-rats/) — 2026-06 から稼働する Russian Loader-as-a-Service。偽 NetSuite・Odoo・HubSpot・Salesforce ログインページで CAPTCHA 偽装 → ブラウザキャッシュに悪意ある PNG をダウンロード → findstr/certutil で隠し初段ペイロードを取得・実行 → Windows/macOS 向け CountLoader + Windows 向け DeviceManager RAT (Ethereum/Polygon スマートコントラクト EtherHiding で C2 解決) を展開。被害者の IP を暗号鍵として CTR+XOR でペイロードをメモリ展開し検知回避 *(SOCRadar / THN / BleepingComputer 2026-08-03)*

- **[2026-08-03]** [INC Ransomware が SonicWall SMA 1000 SSRF+コードインジェクション (CVE-2026-15409/15410) をチェーンして多国籍組織を侵害](https://www.resecurity.com/blog/article/from-wsproxy-to-root-inc-ransomware-and-sonicwall-sma-exploit-chain) — CVSS 10.0 の SSRF (CVE-2026-15409) で内部 AMC ポートへ WebSocket トンネルを確立後、CVE-2026-15410 のパストラバーサルで root として任意コマンドを実行。認証情報データベース・セッション DB・TOTP MFA シード構成を窃取し永続化・横断移動を確立。8/2 以降 INC Ransomware の被害者掲載が急加速 (累計 885 件、対象: AU・US・UAE・CH 等の民間・政府機関) *(THN / Resecurity / SecurityWeek 2026-08-03)*

- **[続報][2026-08-04]** [CVE-2026-18577: N-able N-central が CISA KEV に追加、顧客配下エンドポイントへの横断侵害継続](https://thehackernews.com/2026/08/cisa-adds-exploited-n-able-n-central.html) — CISA が 8/4 に CVE-2026-18577 (N-central 認証バイパス, CVSS 8.2) を KEV カタログに追加。hotfix 2026.3.1.7 適用済みでも侵害済みインスタンスでの永続化確認事例あり *(THN 2026-08-04)* [続報: 2026-08-04 掲載]

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-08-03 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-15409 | SonicWall SMA 1000 <12.4.3-03453 / <12.5.0-02835 | CWE-918 / **10.0** | 未認証攻撃者が Workplace インターフェースの SSRF で localhost のみのサービスへ WebSocket トンネルを確立 → 内部 AMC ポート (8188) にアクセス → CVE-2026-15410 チェーンで root RCE | firmware 12.4.3-03453 / 12.5.0-02835 ([SonicWall Product Notice](https://www.sonicwall.com/support/notices/product-notice-sma-1000-series-affected-by-multiple-vulnerabilities/kA1VN000001nv6D0AQ)) | CVSS 10.0 / ゼロデイ悪用 (2026-06-22〜) / CISA KEV 入り / INC Ransomware 実悪用 |
| CVE-2026-15410 | SonicWall SMA 1000 AMC | CWE-77 / **7.2** | CVE-2026-15409 で確立したローカルアクセスから AMC `remove_hotfix` ワークフローのパストラバーサルで root として任意 OS コマンドを実行 → 完全なアプライアンス掌握 | firmware 12.4.3-03453 / 12.5.0-02835 (同上) | CVE-2026-15409 とチェーン / INC Ransomware 実悪用 / CVSS 7.2 |
| Shai-Hulud npm worm (CVE 未割当) | npm keyv <4.6.1 / cacheable ほか 868 パッケージ (2026-08-04 汚染バージョン) | CWE-912 / — | メンテナー GitHub アカウント侵害 → package.json に preinstall フック (setup.mjs) を注入 → npm install 時に自動起動 → Bun ランタイムで難読化スティーラーを実行し多種認証情報と Actions シークレットを窃取・下流パッケージへ自己伝播 | keyv 4.6.1 以降が安全 / npm が汚染バージョンを削除中 ([SafeDep](https://safedep.io/keyv-npm-supply-chain-compromise/)) | 月間 20 億+ インストール影響 / ワーム自己伝播 / CVE 未割当 / 9 組織に 30 分で伝播 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-08-03 | CVE-2026-57279 / JVN#72334274 | Cybozu Garoon 6.17.0〜6.17.1 スケジューラーの XSS — ログイン済みユーザーのブラウザで任意スクリプトが実行される (Garoon 5 以前はパッチなし) | CVSS 6.0/6.8 | [JVN#72334274](https://jvn.jp/en/jp/JVN72334274/) |
| 2026-08-03 | CVE-2026-13584 / ICSA-26-211-07 | Mitsubishi Electric CC-Link IE TSN (MELSEC MX Controller 等) — 同一ネットワーク上の攻撃者が特定タイミングで細工パケットを送信し通信データを改ざん・DoS を引き起こす (パッチ未公開、ネットワーク分離が緩和策) | CVSS 4.0 / ICS・OT 影響 | [CISA ICSA-26-211-07](https://www.cisa.gov/news-events/ics-advisories/icsa-26-211-07) |
| 2026-08-04 | CVE-2026-67243 / JVNDB-2026-000107 | refirio freo2 (PHP CMS) — 最高権限管理者が実行ファイルをアップロードして任意 OS コマンドを実行できる (CWE-434; 制限なしファイルアップロード) | CVSS 7.2 | [JVNDB-2026-000107](https://jvndb.jvn.jp/en/contents/2026/JVNDB-2026-000107.html) |

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| CrowdStrike Press Release / Yahoo Finance (2026 Threat Hunting Report) | 2026-08-03 公開確認 ✓ / Black Hat 2026 同時リリース確認 ✓ |
| Schneier on Security / Noise.getoto.net (More on OpenAI/HF attack) | Noise.getoto.net "/2026/08/03/" 確認 ✓ |
| SecurityWeek (Black Hat 2026 Vendor Announcements Part 1) | Black Hat USA 2026 (8/1-6) 開催確認 ✓ / SentinelOne・Sweet Security 発表確認 ✓ |
| Aikido.dev / SafeDep / THN / Wiz / Datadog Security Labs (Shai-Hulud npm worm) | 複数ソースで 2026-08-04 09:00 UTC 確認 ✓ / 868 パッケージ・9 組織・月間 20 億 DL 確認 ✓ |
| SOCRadar / THN / BleepingComputer (DOUBLECUP) | THN URL "/2026/08/" 確認 ✓ / Xloggs 2026-08-03 17:00 PDT 掲載確認 ✓ |
| THN / Resecurity / SecurityWeek (INC Ransomware + SonicWall SMA) | Thomas Harris WordPress "/2026/08/03/" 確認 ✓ / Resecurity blog 確認 ✓ |
| THN (CISA KEV CVE-2026-18577 追加) | Thomas Harris WordPress "/2026/08/04/" 確認 ✓ |
| JVN#72334274 / JVNDB-2026-000106 (Cybozu Garoon CVE-2026-57279) | JVN 2026-08-03 公開確認 ✓ / CVSS 6.0/6.8 確認 ✓ |
| CISA ICSA-26-211-07 / INCIBE (Mitsubishi Electric CC-Link IE TSN CVE-2026-13584) | CISA advisory 2026-07-30 (Julian day 211) / JVN 2026-08-03 公開 ✓ / CVSS 4.0 確認 ✓ |
| JVNDB-2026-000107 (freo2 CVE-2026-67243) | OffSeq.com radar 確認 ✓ / JVN 2026-08-04 公開確認 ✓ / CVSS 7.2 確認 ✓ |
| thehackernews.com / bleepingcomputer.com / nvd.nist.gov / cisa.gov | 403 — WebSearch スニペット・Thomas Harris WordPress・二次ソースで代替 |

### 集計サマリ

- **巡回ソース数**: 約 25
- **採用件数**: AI=3 / Security=4 / CVE=3 / 国内=3
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-08-03 より前の一次ソース):
    - CrowdStrike Global Threat Report 2026 (2026-02 公開) — 同名 Threat Hunting Report (2026-08-03) は採用
    - Meta Muse Spark 1.1 (2026-07-17 議論) / Thinking Machines Inkling (7月末) → 採用窓外
    - Windows Notepad CVE-2026-20841 (2026-02 Patch Tuesday)
    - China 伴侶 AI 初回罰則 (2026-07-15〜22) — Nspirement 2026-08-03 分析記事は一次事象が窓外のため除外
    - Mitsubishi Electric CISA advisory (ICSA-26-211-07): CISA 一次公開 2026-07-30 / INCIBE 2026-07-31 → JVN 2026-08-03 公開で採用窓内として採用 (Adobe CVE-2026-48449/48448 と同方針)
    - UK AI Regulation and Safety Bill 下院通過 (2026-08-14 予定) → 未来の事象で除外
  - 重複 (直近 7 ダイジェスト掲載済み・excluded_set 参照):
    - CVE-2026-18577 N-central (08-04掲載) → CISA KEV 追加は [続報] として採用
    - White House AI Safety Meeting (08-04掲載) / EU AI Act GPAI (08-04掲載) / Microsoft Project Perception (08-04掲載)
    - Brinks Home (08-04掲載) / DarkSword/GHOSTBLADE (08-04掲載) / BTMOB RAT (08-04掲載)
    - CVE-2026-17583 Thermo Fisher (08-04掲載) / CVE-2026-62416 Sharp (08-04掲載)
    - CVE-2026-48449/48448 Adobe Campaign Classic (08-03掲載) / Coldcard PRNG (08-03掲載)
    - CVE-2026-63223 CodeIgniter4 (08-02掲載) / CVE-2026-67208 Juggle (08-02掲載)
    - CVE-2026-53609/53606 apostrophe/sanitize-html (08-02掲載)
    - OpenAI/HuggingFace 侵害 (08-01掲載) → Schneier 2026-08-03 分析は [続報] として採用
    - Anthropic cyber eval breach (08-01掲載) / GPT-5.6 Luna (08-01掲載)
    - Unit 42 DeepSeek+Hermes (08-01掲載) / Chrome 151 CVE-2026-17650〜17656 (08-01掲載)
    - Contagious Interview macOS ClickFix (08-01掲載) / SonicWall credential stuffing (08-01掲載) — INC Ransomware SMA 1000 CVE-2026-15409/15410 は別製品・別 CVE で新規採用
    - Kaspersky OctLurk/SilkLurk (08-01掲載) / CaptiveCrunch Midnight Blizzard (08-03掲載) / CISA 水道 PLC (08-03掲載) / HackerOne 政府 ID (08-03掲載) / Coldcard PRNG (08-03掲載)
  - 日付不明 / 確認不可: なし (全採用記事はソース日付確認済み)
- **取得失敗ソース**: thehackernews.com / bleepingcomputer.com / aikido.dev / safedep.io / socradar.io / wiz.io / securityboulevard.com / jvn.jp / cisa.gov / senserva.com / scworld.com ほか多数が 403 → WebSearch スニペット・Thomas Harris WordPress・二次ソース (Xloggs / securityonline.info / cyberkendra.com / Noise.getoto.net 等) で代替

</details>

---

*生成: keda-digest-bot / 2026-08-05 05:05 JST*
