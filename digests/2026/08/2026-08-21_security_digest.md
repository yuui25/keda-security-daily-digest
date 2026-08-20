# KEDA Daily Digest — 2026-08-21 (JST)

> 採用範囲: 公開日 2026-08-19 〜 2026-08-21
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Anthropic が Q2 2026 に $11.6B の収益を計上し初めて OpenAI ($6.7B) を四半期収益で上回るとともに、AI 企業として初の黒字転換を達成した週の締めくくりとなった。AI セキュリティ領域では Google Mandiant の AVDH がわずか 2 日間で 100 件超の重大脆弱性を自律発見し、Adversa AI が Grok に対する「Cryptographic Context Injection」(暗号化プロンプトインジェクション) を公開した。セキュリティでは Zimbra SNMP (CVE-2026-73570、CVSS 8.9) の実エクスプロイトが 8/20 に確認され、Cisco が Crosswork・Secure Workload の CVSS 10.0 ハードニング修正を 8/19 に公開した。isolated-vm の V8 サンドボックス完全脱出 (GHSA-864f-rcv7-6rh4) が 8/20 に公開報道され、AI エージェント基盤として多数採用されるライブラリの信頼境界を揺るがす内容として注目される。

---

## AI 関連ニュース

- **[2026-08-19]** [Anthropic Surpasses OpenAI in Q2 2026 Revenue for First Time — $11.6B vs $6.7B, First Operating Profit](https://qz.com/anthropic-surpasses-openai-revenue-q2-2026-081926) — Anthropic が Q2 2026 に $11.6B (前四半期比 +145%) を計上し、初めて OpenAI の $6.7B を上回る。Anthropic は同四半期で調整後営業黒字を達成したのに対し OpenAI の Q2 営業損失は $12.3B に拡大 *(QZ / cryptonomist 2026-08-19)*

- **[2026-08-19]** [Google Mandiant AVDH: AI Agents Find 100+ Critical Vulnerabilities in Source Code in Just 2 Days](https://www.helpnetsecurity.com/2026/08/19/google-mandiant-avdh-ai-vulnerability-discovery-tool/) — Mandiant が 10 ヶ月間内部運用してきた Agentic Vulnerability Discovery Harness (AVDH) が 2 日間のライブ調査で重大・高深刻度脆弱性を 100 件超発見し公開; 累計数千万行のコードを解析し CVE-2026-13242 等 12 件の CVE を付番。構造解析・認証・ルーティング等の専門エージェントが協調動作 *(HelpNetSecurity 2026-08-19)*

- **[2026-08-19]** [OpenAI Expands ChatGPT Ads to 31 EU Markets, Updates GPT-5.6 Sol with Effort Slider](https://openai.com/news/) — OpenAI が ChatGPT 広告をドイツ・フランス・スペイン等 EU 31 ヶ国に拡大; 同日 GPT-5.6 Sol を更新し Plus/Pro ユーザー向けに思考量を調整できるスライダーを追加。CFO Sarah Friar は「2027 年 (またはそれ以前) に上場」と社員向けに言明 *(OpenAI News / Reuters 2026-08-19)*

- **[2026-08-20]** [Adversa AI Discloses "Cryptographic Context Injection" on Grok — Encrypted Payload Exfiltrates Chat History Without Warning](https://www.theregister.com/ai-and-ml/2026/08/20/grok-chat-duped-into-swallowing-injected-instructions/5290019) — Adversa AI が Grok 4.5 Fast に対しページ内の暗号化 JSON でプロンプトを隠蔽し、Grok 自身の Python 実行環境で復号→ユーザー名・位置・プラン・会話履歴を攻撃者サーバーへ送信する PoC を公開。成功率 40%、xAI は 6/3 の報告以来 8/10 まで返答なし、パッチ未提供 *(The Register / The Hacker News 2026-08-20)*

- **[2026-08-20]** [Claude Code-Assisted SAML Security Testing Uncovers Auth Bypass in Authentik and Multiple IdPs — 8 Researchers Simultaneously Discover Same Issue](https://cybersecuritynews.com/claude-ai-finds-saml-security-flaws/) — Oblique Security が Claude Code を使った自動 SAML テストハーネスで Authentik 等の認証バイパスを発見; CVE-2026-57580 は SAML NameID に XML コメントを挿入して署名検証を回避しアカウント乗っ取りを実現。同一バグを 8 名の研究者が同時発見し、AI ツールによる脆弱性発見加速を実証 *(CyberSecurityNews / GBHackers 2026-08-20)*

---

## セキュリティ関連ニュース

- **[2026-08-20]** [CVE-2026-73570 (CVSS 8.9): Zimbra SNMP Command Injection Now Actively Exploited in Wild](https://www.bleepingcomputer.com/news/security/critical-zimbra-rce-flaw-now-actively-exploited-in-attacks/) — Zimbra Collaboration の SNMP 通知パスに未認証コマンドインジェクションが実エクスプロイト確認。`snmp_notify` 有効時に細工 SMTP リクエストで zimbra ユーザーとして任意 OS コマンド実行; 2026-07-20 公開の Zimbra 10.1.20 パッチ未適用サーバーは即時更新要 *(BleepingComputer / The Hacker News 2026-08-20)*

- **[2026-08-20]** [GHSA-864f-rcv7-6rh4: Critical isolated-vm Sandbox Escape Disclosed — V8 Guest-to-Host Control Flow Hijack](https://thehackernews.com/2026/08/isolated-vm-flaw-lets-sandboxed.html) — Node.js 向け V8 Isolate サンドボックスライブラリ isolated-vm の `ExternalCopy.transferList` に型混乱が存在し、ゲストコードがホストプロセスのメモリを破壊して制御フローを奪取可能。研究者が制御アドレスクラッシュから完全ホスト脱出までをデモ。AI エージェント・LLM 基盤プロジェクトに多数採用されており 6.2.0/7.0.1 で修正済み *(Endor Labs / The Hacker News 2026-08-20)*

- **[2026-08-19]** [Cisco Releases CVSS 10.0 Security Hardening Advisories for Crosswork and Secure Workload — Multiple Internally Discovered Vulnerabilities Patched](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-hardening-crosswork-UzDTU9Vh) — Cisco が Crosswork ネットワーク自動化 (CVE-2026-20030 等 4 件、CVSS 10.0) および Secure Workload マイクロセグメント (CVE-2026-20231 等 5 件、CVSS 10.0) に対し包括的内部セキュリティ審査で発見した脆弱性への修正を同日公開。エクスプロイト未確認・ワークアラウンドなし *(Cisco PSIRT 2026-08-19)*

- **[2026-08-20]** [Cisco Warns of High-Severity ClamAV DoS Flaws (CVE-2026-20337/20338) With Public PoC — Windows Cisco Secure Endpoint at Elevated Risk](https://www.bleepingcomputer.com/news/security/cisco-warns-of-high-severity-clamav-flaws-with-public-exploits/) — ClamAV 1.5.0〜1.5.3 に細工ファイルでスキャン中断/クラッシュを引き起こす DoS 脆弱性群 (CVSS 7.5)。PoC が公開済みで Windows 上の Cisco Secure Endpoint では特権コンテキストで実行されるため影響度が増大; ClamAV 1.5.4 で修正 *(BleepingComputer / Cisco PSIRT 2026-08-20)*

- **[2026-08-20]** [[続報] GitLab CVE-2026-19478 (CVSS 9.4) Actively Exploited Within Days of Emergency Patch](https://www.securityweek.com/) — 8/17 公開の GitLab GraphQL コードインジェクション CVE-2026-19478 (未認証 CVSS 9.4) が数日以内に実エクスプロイト。セルフホスト GitLab 19.2.4 / 19.1.6 / 19.0.8 / 18.11.11 未適用組織は即時パッチ適用要 *(SecurityWeek 2026-08-20)*

- **[2026-08-20]** [CVE-2026-69414 ShieldBreak Microsoft Defender Zero-Day — CISA BOD 26-04 Mandates 14-Day Remediation With No Patch Available](https://blog.qualys.com/product-tech/2026/08/20/shieldbreak-the-windows-defender-zero-day-with-no-patch-detect-it-mitigate-it-with-qualys) — Microsoft Defender Malware Protection Engine の CFAPI ファイル水和処理における局所権限昇格ゼロデイ CVE-2026-69414 (CVSS 7.8)。8/12 に PoC 公開、パッチ未提供の状態で CISA BOD 26-04 が連邦機関に 14 日以内の緩和措置を義務付け *(Qualys 2026-08-20 / BleepingComputer)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-08-19 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-20030 | Cisco Crosswork Network Automation (2026-08-19 hardening 以前) | CWE-89 / **10.0** | 攻撃者が Crosswork REST API に SQL 文字列を直接注入 → データベース完全窃取・改ざん (内部発見、エクスプロイト未確認) | Cisco Crosswork Aug 2026 hardening release で修正; advisory [cisco-sa-hardening-crosswork](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-hardening-crosswork-UzDTU9Vh); 公開 **2026-08-19** | CVSS 10.0 / ネットワーク自動化基盤 / 4 CVE 同日公開 (CVE-2026-20030/-20357/-20358/-20359) |
| CVE-2026-20231 (et al.) | Cisco Secure Workload (Tetration; 2026-08-19 hardening 以前) | CWE-多重 / **10.0** | 攻撃者が Secure Workload の複数 API・認証パスで認可制御を回避 → マイクロセグメンテーションポリシーの完全変更・機密データ窃取 (内部発見) | Aug 2026 hardening release で修正; [cisco-sa-hardening-csw1](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-hardening-csw1-shSvndWP); 公開 **2026-08-19** | CVSS 10.0 / ゼロトラスト基盤 / 5 CVE 同日公開 (CVE-2026-20231/-20315/-20317/-20318/-20319) |
| CVE-2026-20337 / CVE-2026-20338 | ClamAV 1.5.0〜1.5.3 (Cisco Secure Endpoint 含む) | CWE-119/125 / **7.5** | 未認証リモート攻撃者が細工ファイルを送信 → スキャン時の improper boundary check → OOB 読み取り / メモリ破壊 → DoS (クラッシュ); Windows では特権プロセス動作でリスク増 | ClamAV 1.5.4 で修正; PoC 公開済み; advisory [cisco-sa-clamav-WuuvVd26](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-clamav-WuuvVd26); 公開 **2026-08-19** | PoC 公開 / 7 CVE 計 / AV 製品バリアント水平伝播起点 |
| GHSA-864f-rcv7-6rh4 | isolated-vm ≤ 7.0.0 (Node.js) | CWE-843 / **Critical** (CVE 付番待ち) | ゲストが `ivm.Reference` 経由で `ExternalCopy.transferList` の型混乱を誘発 → ホストプロセスのメモリ破壊 → 制御フロー奪取 → ホスト RCE (DoS〜完全脱出実証済み) | isolated-vm 6.2.0/7.0.1 で修正; fix 詳細: GHSA 公開 **2026-08-07** (公開報道 **2026-08-20**); [Endor Labs blog](https://www.endorlabs.com/learn/ghsa-864f-rcv7-6rh4-critical-type-confusion-vulnerability-in-isolated-vm) | AI エージェント多数採用 / ゲスト→ホスト完全脱出実証 / JS サンドボックス水平伝播起点 |
| CVE-2026-73570 | Zimbra Collaboration < 10.1.20 | CWE-78 / **8.9** | `snmp_notify` + swatchdog 有効時、細工 SMTP リクエストが SNMP 通知パスを経由 → zimbra ユーザーとして任意 OS コマンド実行 (認証不要) → webshell 設置・永続化・メールデータ完全窃取 | Zimbra 10.1.20 で修正 (2026-07-20); 実エクスプロイト確認 **2026-08-20** | **実エクスプロイト確認** / CVSS 8.9 / 未認証 / メールサーバー広範利用 (※CVE 公開 2026-07-20 で採用窓外だが実エクスプロイト情報は採用窓内) |

---

## 国内脆弱性・インシデント情報

採用窓内 (2026-08-19〜08-21) での JVN・JPCERT/CC・IPA 新規公開は確認できなかった (jvn.jp、jpcert.or.jp は EGRESS_BLOCKED により直接確認不可)。

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| qz.com/anthropic-surpasses-openai-revenue-q2-2026-081926 | URL 2026-08-19 ✓; cryptonomist.ch/2026/08/19/ 確認 ✓ |
| helpnetsecurity.com/2026/08/19/google-mandiant-avdh/ | URL 2026-08-19 ✓; GBHackers 2026-08-19 確認 ✓ |
| openai.com/news/ (ChatGPT Ads / GPT-5.6 Sol) | OpenAI News 2026-08-19 スニペット ✓ |
| theregister.com/ai-and-ml/2026/08/20/grok-chat-duped (Adversa AI) | URL 2026-08-20 ✓; GuardianMSSP 2026-08-20 確認 ✓ |
| cybersecuritynews.com (Claude SAML) | 2026-08-20 スニペット ✓; GBHackers URL ✓ |
| bleepingcomputer.com (Zimbra CVE-2026-73570 exploitation) | URL 2026-08-20 ✓; CERT Polska Alert 145/2026 Aug 17 ✓ |
| thehackernews.com/2026/08/isolated-vm-flaw (GHSA-864f-rcv7-6rh4) | GuardianMSSP 2026-08-20 URL ✓; GitHub advisory published 2026-08-07 確認 ✓ |
| sec.cloudapps.cisco.com (Crosswork hardening) | Cisco advance notice Aug 19 ✓; cisco-sa-hardening-crosswork URL ✓ |
| sec.cloudapps.cisco.com (Secure Workload hardening) | Cisco advance notice Aug 19 ✓; cisco-sa-hardening-csw1 URL ✓ |
| bleepingcomputer.com (ClamAV CVE-2026-20337/20338) | URL ✓; Cisco advisory cisco-sa-clamav-WuuvVd26 Aug 19 確認 ✓ |
| securityweek.com ([続報] GitLab CVE-2026-19478 exploitation) | スニペット 2026-08-20 ✓ |
| blog.qualys.com/product-tech/2026/08/20/shieldbreak (CVE-2026-69414) | URL 2026-08-20 ✓; CVE assigned 2026-08-14 (採用窓外) / CISA BOD 26-04 Aug 20 新報道 ✓ |
| jvn.jp / jpcert.or.jp / ipa.go.jp | EGRESS_BLOCKED — 直接確認不可 |

### 集計サマリ

- **巡回ソース数**: 約 25
- **採用件数**: AI=5 / Security=6 / CVE=5 / 国内=0
- **除外理由内訳**:
  - 採用窓外 (公開日 <2026-08-19): Anthropic Q2 revenue 初報 CNBC 2026-08-15; Forbes Q2 report 2026-08-17; CVE-2026-69414 ShieldBreak PoC/CVE 付番 2026-08-12/14; CVE-2026-73570 Zimbra fix 2026-07-20 (CVE table から除外、ニュース採用); GHSA-864f-rcv7-6rh4 advisory 2026-08-07 (CVE table で注記付き採用); Cisco SD-WAN CVE-2026-20303/20304 2026-08-05; ClamAV July 2026 advisory; DHS HSIN breach (2026-07-01)
  - 重複 (excluded_set): OpenAI Astra pacing (08-20 digest); Anthropic $6.5B ARR (08-20 digest); Citrix NetScaler CVE-2026-19490 (08-20 digest); LiteLLM supply chain (08-19 digest); Forminator CVE-2026-15748 (08-19 digest); GitLab CVE-2026-19478 初報 (08-19 digest → [続報] として採用); Stripe/OpenRouter (08-18 digest); ChatGPT for Teens (08-19 digest)
  - 日付不明/未確認: NASA AIT-GUI GHSA-p9r8-2q67-fp86 (advisory 2026-08-13 で採用窓外); Authentik CVE-2026-57580 advisory 2026-07-15 (採用窓外)
  - 取得失敗ソース (EGRESS_BLOCKED): thehackernews.com, bleepingcomputer.com, securityweek.com, helpnetsecurity.com, gbhackers.com, nvd.nist.gov, cisa.gov, sec.cloudapps.cisco.com, endorlabs.com, techzine.eu, guardianmssp.com, osv.dev, senserva.com, jvn.jp, jpcert.or.jp, ipa.go.jp

</details>

---

*生成: keda-digest-bot / 2026-08-21 05:04 JST*
