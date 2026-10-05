# KEDA Daily Digest — 2026-10-06 (JST)

> 採用範囲: 公開日 2026-10-04 〜 2026-10-06
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

トランプ政権が「Super Intelligence Force (SIF)」大統領令に署名しAI政策を一元化 (Oct 4)。同日 Bloomberg Intelligence が米中AI性能差が過去最低の3%に縮小と報告しDeepSeek V4.1 Flash がAnthropicトップモデルに肉薄。OpenAI 安全透明性責任者 David Robinson が「文化が壊れている」とThe Atlanticに寄稿して辞任し、Oct 5 にはNY市議会が OpenAI・Anthropic・Google・Meta 幹部を宣誓証言に召喚した。脆弱性面では Citrix NetScaler SAML ヒープオーバーフロー CVE-2026-88779 が CISA KEV 10/4 追加 (修正期限 10/7)、Anthropic Mythos AI が発見した Rejetto HFS の弱乱数起因 CVE-2026-61500 を中国系アクターが24時間以内に悪用開始した。

---

## AI 関連ニュース

- **[2026-10-04]** [トランプ大統領が "Super Intelligence Force (SIF)" 大統領令に署名 — AI用語を「Super Intelligence」に改称し、Jay Clayton DNI 主導の省庁横断タスクフォースが米国AI覇権と安全リスクを120日以内に報告](https://www.foxnews.com/politics/trump-launching-super-intelligence-force-ensure-american-dominance) — FTC委員長 Andrew Ferguson・OPM長官 Scott Kupor・国防次官 Emil Michael も主要メンバー; SpaceX AIは「SpaceXSI」へ改称方針 *(Fox News / Spokesman-Review / GovConWire)*

- **[2026-10-04]** [Bloomberg Intelligence: 米中AIパフォーマンス差が過去最低3%に縮小 — DeepSeek V4.1 Flash が LiveBench 81.1 でAnthropicの83.4に迫る](https://www.bloomberg.com/news/articles/2026-10-04/us-lead-in-ai-over-china-narrows-after-deepseek-gains-bi-says) — 5月の9%差から大幅縮小; DeepSeek V4.1 Flash を10月4日リリース; 上位15モデル中で中国モデルはまだ3本; 米国チップ輸出規制の実効性に疑問符 *(Bloomberg Intelligence / KuCoin / CryptoBriefing)*

- **[2026-10-04]** [OpenAI 安全透明性責任者 David Robinson 辞任、The Atlantic に「I quit OpenAI because its culture is broken」を寄稿 — 3名の研究者解雇後また別の幹部退職](https://startupfortune.com/openai-safety-transparency-lead-david-robinson-resigns-amid-upheaval/) — システムカードと公開リスク開示の責任者; 「核施設や航空機の安全文化に精通した同僚と一度も出会えなかった」; 過去2年間で退職した上席安全幹部は少なくとも6名に *(The Guardian / Benzinga / AI Weekly / Startup Fortune)*

- **[2026-10-05]** [NY市議会「委員会全体」公聴会: OpenAI・Anthropic・Google・Meta 幹部が宣誓証言 — AIエージェント kill switch 義務化・内部告発者報奨制度が議題](https://www.cnbc.com/2026/10/05/anthropic-openai-google-meta-execs-testify-nyc-council-ai-hearing.html) — Anthropic代表: Logan Graham (Frontier Red Team長); OpenAI: Morgan Dwyer (政策本部長); Jacob Coxon 内部告発者が「極めて無謀な開発手法」と批判; 2022年以来初の「全委員会」形式 *(CNBC / Route Fifty / CryptoBriefing)*

- **[2026-10-05]** [Sam Altman (OpenAI CEO): 「AIによるある程度の悪影響は受け入れるべき」— Anthropicとの規制スタンスの差異が鮮明に](https://fortune.com/2026/10/05/sam-altman-ai-risks-bad-things-benefits-trump-voluntary-safety-pact-openai-regulation) — NY市議会証言後の発言; トランプ自主安全協定署名と同日; 規制強化には消極的姿勢でAnthropicの慎重路線と対比 *(Fortune / QZ)*

- **[2026-10-04]** [Anthropic Mythos AI が Rejetto HTTP File Server の弱乱数起因 CVE-2026-61500 を発見、翌日に中国系 IP が米国内ホストへの悪用を開始](https://www.securityweek.com/exploitation-hits-rejetto-hfs-vulnerability-discovered-by-ai/) — AI発見→writeup公開→野外悪用の「24時間サイクル」を示す初期事例; Mythos は23,000件超の脆弱性発見実績; Horizon3.aiが技術解説公開の翌日に China Telecom IPから偵察開始 *(SecurityWeek / SecurityAffairs / DEV Community)*

---

## セキュリティ関連ニュース

- **[2026-10-04]** [Citrix NetScaler ADC/Gateway SAML ヒープオーバーフロー CVE-2026-88779 が CISA KEV 追加 — SAML SP/IdP 構成で悪用、修正期限 10/7](https://cybersecuritynews.com/cisa-citrix-netscaler-vulnerability-exploited/) — CVSS 8.7; Citrix が標的型攻撃を確認; 6回の試行でSAMLサービスがクラッシュ→アプライアンス再起動; NetScaler ADC/Gateway 14.1-73.41 未満・13.1-64.28 未満が対象 *(CyberSecurityNews / Sophos / CISA)*

- **[2026-10-04]** [CVE-2026-61500 (Rejetto HFS 3.0〜3.2.0) が野外悪用開始 — 弱乱数 Math.random() 起因のセッションキー復元→管理者クッキー偽造→RCE; China Telecom IP から米国内ホストを標的に小規模偵察](https://www.securityweek.com/exploitation-hits-rejetto-hfs-vulnerability-discovered-by-ai/) — VulnCheck CVSS 9.3; 修正版: HFS 3.2.1; PoC および技術解説が Horizon3.ai から公開済み *(SecurityWeek / VulnCheck / bellatorcyber)*

- **[2026-10-05]** [macOS HFS+ B-tree カーネルヒープオーバーフロー CVE-2026-43682 の PoC が公開 — ネットワーク越し認証不要で任意コード実行](https://cve.halosecurity.com/cve-advisory/cve-2026-43682-macos-kernel-memory-corruption-vulnerability) — CVSS 9.8; macOS Tahoe 26.6 / Sequoia 15.7.8 / Sonoma 14.8.8 で修正済み; PoC (petermalone/CVE-2026-43682) 公開によりパッチ未適用環境の悪用リスクが急増 *(HaloSecurity / SentinelOne)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 today-2 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-88779 | Citrix NetScaler ADC/Gateway < 14.1-73.41 (SAML SP/IdP 構成時) | CWE-122 / 8.7 | SAML SP/IdP として構成された NetScaler に未認証攻撃者が細工した SAML リクエストを送信 → SAML 処理コードがバッファ境界チェックなしでヒープに書き込み → DoS (6回クラッシュで再起動) / 任意コード実行の可能性 | [CTX730132 / NetScaler 14.1-73.41 (2026-10-04)](https://support.citrix.com/external/article/CTX730132) (commit 不明) | **KEV 2026-10-04 / 修正期限 10-07 / 野外悪用中** / F5 BIG-IP APM・PAN-OS GlobalProtect 等 SAML SP/IdP 実装への水平バリアント候補 |
| CVE-2026-61500 | Rejetto HFS 3.0.0 〜 3.2.0 | CWE-338 / 9.3 | サーバーが `Math.random()` でセッションクッキー署名キーを導出し未認証クライアントに同PRNG出力を複数回公開 → 攻撃者が少数の観測値でジェネレーター状態を復元してキーを回収 → 任意の管理者セッションクッキーを偽造 → `server_code` 設定機能経由で任意コード実行 | [HFS 3.2.1 (2026-10-02)](https://github.com/rejetto/hfs/releases/tag/3.2.1) | **CVSS 9.3 / 野外悪用中 / AI発見 (Anthropic Mythos)** / PHP/Python/Node.js 製ファイルサーバー・管理UIの `Math.random()` 鍵導出実装への水平バリアント候補 |
| CVE-2026-43682 | Apple macOS < Tahoe 26.6 / < Sequoia 15.7.8 / < Sonoma 14.8.8 | CWE-122 / 9.8 | HFS+ B-tree ノードのメタデータ処理で入力長検証不足のためカーネルヒープバッファをオーバーフロー → 細工した HFS+ ボリュームのマウントまたは特定ネットワークリクエストでカーネルメモリ破損 → 認証不要の任意コード実行 | [petermalone/CVE-2026-43682 PoC (2026-10-05)](https://github.com/petermalone/CVE-2026-43682) | **CVSS 9.8 / PoC 公開 (2026-10-05)** / macOS/iOS 共通 HFS+ パーサー / btrfs・ext4 等他ファイルシステム B-tree メタデータ処理への水平バリアント候補 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-10-05 | JVN#24352487 / CVE-2026-100727 | GROWI < v7.5.5 (Local ファイルアップロード設定時) にアクセス制御不備 — 未認証の第三者が非公開ページの添付ファイル・プロフィール画像・一括エクスポート等を読み取り可能 | CVSS 3.0: 5.3 / CVSS 4.0: 6.9 / 情報漏洩 | [JVN#24352487](https://jvn.jp/en/jp/JVN24352487/) |
| 2026-10-05 | 777CON-PASS 不正アクセス | eスポーツ・ゲームイベント参加者管理サービス 777CON-PASS に不正アクセス; 氏名・メールアドレス・生年月日等の個人情報流出の可能性 | 個人情報漏洩リスク | [セキュリティ対策Lab 2026-10 まとめ](https://rocket-boys.co.jp/security-measures-lab/) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 25+
- 採用件数: AI=6 / Security=3 / CVE=3 / 国内=2
- 除外理由内訳:
  - 採用窓外 (公開日 < 2026-10-04):
    - ベネフィット・ワン 個人情報漏洩 1.3万件 (Oct 2) — 窓外
    - らしんばん 不正アクセス (Oct 2) — 窓外
    - KillSec 摘発 Operation KillSwitch (Sep 30 / Oct 1 報道) — 窓外
    - CVE-2026-51870 DeepTutor (Sep 30 公開) — 窓外
    - Dell CSM CVE-2026-63688/63692 DSA-2026-448 (Oct 1 公開) — 窓外
    - Apache HTTP Server 複数 CVE (Oct 2 JVN 公開) — 窓外
    - Cl0p Oracle EBS CVE-2025-61882 — 2025年 CVE; Oct 2026 被害続報だが CVE 自体は古い
  - 重複 (直近7日 digest 既報):
    - CVE-2026-105215/105212/105211 ZITADEL (Oct 5 digest 既報)
    - Linux KVM ゼロデイ / Vercel KVM (Oct 5 digest 既報)
    - Adversa AI コーディングエージェント調査 (Oct 5 digest 既報)
    - CVE-2026-90970 GitLab AI Gateway (Oct 4 digest 既報)
    - CVE-2026-71889/85515 Bouncy Castle (Oct 4 digest 既報)
    - GHSA-9xfm-37f4-2h8g NASA-AMMOS AIT-Core (Oct 4 digest 既報)
    - GHSA-45wm-hvw4-223f OpenAM (Oct 4 digest 既報)
    - CVE-2026-92948 vm2 (Oct 3 digest 既報)
    - CVE-2026-104286 FortiMail (Oct 3 digest 既報)
    - CVE-2026-76504 Cisco SD-WAN (Oct 2 digest 既報)
    - OpenAI 安全研究者 3 名解雇 (Oct 3 digest 既報; Robinson 辞任は別件として新規採用)
    - Storm-2603 SharePoint Warlock (Oct 4 digest 既報)
    - ClickFix ChatGPT RAT (Oct 4 digest 既報)
  - 日付不明・確認不可:
    - CVE-2026-105135 InternLM MindSearch CVSS 10 — CVE番号が確認できず除外
    - CVE-2026-103500 Mozilla Thunderbird CVSS 9.8 — CVE番号が確認できず除外
    - CVE-2026-100103 Perforce P4 CVSS 10 — CVE番号が確認できず除外
    - Galileo AI マルチエージェント連鎖失敗研究 (87%伝播) — 公開日不明で除外
    - Unit42 持続的プロンプトインジェクション研究 — 公開日不明で除外
    - セーファーインターネット協会 不正アクセス (Oct 5) — 二次情報のみ; 確認不十分で除外
    - Belgium 学校・DTU 攻撃 — October 2026 の具体日付が確認できず除外
  - 取得失敗ソース (EGRESS_BLOCKED): bleepingcomputer.com, thehackernews.com (本文直接), nvd.nist.gov, jvn.jp, jpcert.or.jp, securityweek.com (一部), cisa.gov, github.com/advisories (直接アクセス一部)

</details>
