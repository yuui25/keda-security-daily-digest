# KEDA Daily Digest — 2026-06-02 (JST)

> 採用範囲: 公開日 2026-05-31 〜 2026-06-02
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Anthropic が IPO 申請と Mythos の EU サイバーセキュリティ機関 ENISA 初提供を同日に発表し、AI 企業の資本戦略と政府機関連携が同時進行している。セキュリティ面では TeamPCP グループによる @redhat-cloud-services npm 32 パッケージへの "Miasma" CI/CD サプライチェーン攻撃 (June 1) と、Windows Netlogon 0-Click RCE (CVE-2026-41089, CVSS 9.8) のドメインコントローラー積極悪用が最大の脅威。19 年間潜伏した Linux カーネル CIFS upcall LPE "CIFSwitch" の PoC 公開も攻撃面を大きく広げる。

---

## AI 関連ニュース

- **[2026-06-01]** [Anthropic が IPO 申請書を SEC に秘密裏に提出 — 評価額 $380B+ で OpenAI より先行して株式市場へ](https://www.usnews.com/news/top-news/articles/2026-06-01/ai-giant-anthropic-confidentially-files-for-us-ipo) — SEC レビュー中は非公開扱い；評価額は 2月の $30B ラウンド以降 $380B 超、両社が短期間で兆ドル規模の上場を競う構図 *(US News / NBC News)*

- **[2026-06-01]** [Anthropic が Project Glasswing で Mythos を EU サイバーセキュリティ機関 ENISA に初提供](https://www.bloomberg.com/news/articles/2026-06-01/anthropic-to-give-eu-s-cybersecurity-agency-access-to-mythos) — 米英外で初の Mythos アクセス；Anthropic は $100M 利用クレジットを OSS セキュリティ団体に拠出し、Mythos による大規模 zero-day 発見を推進 *(Bloomberg / CNBC)*

- **[2026-06-01]** [LLMShare キャンペーン: 攻撃者が chatgpt.com/s/ 共有リンクを悪用し偽 OpenAI 障害ページを展開](https://www.ghacks.net/2026/06/01/attackers-abuse-chatgpt-share-links-to-host-fake-outage-pages-that-deliver-malware/) — Google 広告で ChatGPT 検索ユーザーを正規ドメインの共有ページへ誘導し、偽障害通知から openew[.]app へ転送；Windows はクレデンシャルローダー、macOS は Odyssey Stealer (Atomic Stealer フォーク) を配布。cloaking で URLScan を回避 *(Push Security / gHacks)*

- **[2026-06-01]** [DataGrail が AI プライバシーリスクレポートを公表: AI 機能 SaaS 2,400 社の 63.6% がサードパーティ AI サブプロセッサを法的文書に非開示](https://www.helpnetsecurity.com/2026/06/01/datagrail-ai-privacy-risks-report/) — 2025 年に 145 件の AI 関連法が州議会で成立；Shadow AI リスクが企業コンプライアンスの盲点に *(Help Net Security)*

- **[2026-06-01]** [Adversa AI が Agentic AI セキュリティリソース June 2026 を公開](https://adversa.ai/blog/top-agentic-ai-security-resources-june-2026/) — SymJack (symlink 偽装 RCE, 6 ツール影響)・TrustFall (MCP auto-exec RCE)・Semantic Kernel CVE-2026-25592 (CVSS 10.0)/CVE-2026-26030 (CVSS 9.8)・Copilot 永続バックドア (CVE-2026-24299)・Microsoft RAMPART/Clarity OSS 化を月次総括 *(Adversa AI)*

- **[2026-05-31]** [CIFSwitch: AI 支援の意味論的グラフ解析が 19 年間潜伏した Linux カーネル CIFS upcall LPE を発見 — PoC 公開](https://www.securityweek.com/19-year-old-linux-kernel-vulnerability-exposes-systems-to-root-access/) — セキュリティ研究者 Asim Manizada が AI 支援の multihop 意味論的グラフ解析で CVE 未割当のバグを連鎖発見；Mint・CentOS Stream 9・Rocky Linux・AlmaLinux・Kali・SLES SAP が影響 *(SecurityWeek / Threat-Modeling.com)*

- **[2026-06-01]** [Casdoor に SAML 認証バイパス 4 件 (CVE-2026-9093/9095/9097/9098) — パッチ未公開、JVN が国内向け周知](https://kb.cert.org/vuls/id/780781) — AudienceRestriction 検証なし・AuthnRequest 照合なし・リプレイ保護なし・証明書トラスト未適用；AI コーディングツールや開発環境でも広く使われる OSS IdP が対象 *(CERT/CC VU#780781 / JVNVU#95478525)*

- **[2026-06-01]** [White House が Anthropic Mythos 発表を契機に AI モデルの FDA 型事前安全審査 EO を検討](https://federalnewsnetwork.com/artificial-intelligence/2026/05/wh-studying-ai-security-executive-order/) — Kevin Hassett 経済顧問が「FDA の薬品承認に相当するプロセス」と言及；Trump 大統領は 5/21 に署名式典直前で延期したが政策議論は継続中 *(Federal News Network)*

---

## セキュリティ関連ニュース

- **[2026-06-01]** [Miasma サプライチェーン攻撃: @redhat-cloud-services npm 32 パッケージ / 96 バージョンが侵害、週間ダウンロード 11.7 万件が影響](https://www.wiz.io/blog/miasma-supply-chain-attack-targeting-redhat-npm-packages) — GitHub Actions OIDC トークンを悪用してワークフローを書き換え、正規 tarball に malicious preinstall フックを挿入して自己増殖；AWS/GCP/Vault/K8s/npm/GitHub/パスワードマネージャー認証情報を窃取。TeamPCP (Mini Shai-Hulud ファミリー) が関与 *(Wiz Research / The Hacker News)*

- **[2026-06-01]** [CVE-2026-41089 Windows Netlogon 0-Click RCE が野外で積極的に悪用中 — ドメインコントローラーが標的、CCB が緊急警告](https://www.helpnetsecurity.com/2026/06/01/windows-netlogon-rce-exploited-cve-2026-41089/) — CVSS 9.8; Netlogon RPC への細工パケット送信のみで DC 上に RCE、特権不要・ユーザー操作不要；ベルギー CCB が 5/29 に野外悪用を確認 *(Help Net Security)*

- **[2026-05-31]** [CIFSwitch: Linux カーネル CIFS/upcall LPE の PoC が公開 — 19 年間潜伏バグが複数ディストロに影響](https://www.bleepingcomputer.com/news/security/new-cifswitch-linux-flaw-gives-root-on-multiple-distributions/) — 5/28 に oss-security ML で PoC 付き開示；cifs.spnego upcall を攻撃者制御 namespace へ誘導し特権 NSS ルックアップ中に malicious libnss_*.so.2 をロードして /etc/sudoers.d へ書き込み root 取得 *(BleepingComputer)*

- **[2026-06-01]** [Microsoft Defender CVE-2026-41091 (SYSTEM LPE, CVSS 7.8) / CVE-2026-45498 (DoS) — CISA KEV 期限 2026-06-03 が迫る](https://thehackernews.com/2026/05/microsoft-warns-of-two-actively.html) — CVE-2026-41091 は Malware Protection Engine のリンク解決不備で SYSTEM 権限昇格、CVE-2026-45498 は Defender を無効化する DoS；修正版は Engine v1.1.26040.8 / Platform v4.18.26040.7 *(The Hacker News / CISA)*

- **[2026-06-01]** [[続報] GitHub 内部リポジトリ侵害 (TeamPCP): Nx Console VS Code 拡張経由で 3,800 リポジトリが窃取、データは犯罪フォーラムで $50,000 で出品](https://thehackernews.com/2026/05/github-internal-repositories-breached.html) — 5/18 に毒入り Nx Console (v18.95.0) がマーケットプレイスで 18 分間配信；GitHub は同日に封じ込めを完了。調査は継続中 *(The Hacker News / GitHub Blog)*

- **[2026-06-01]** [Casdoor OSS IdP に SAML 認証バイパス複数 (VU#780781) — 登録済み IdP 制御で任意ユーザーへのなりすまし](https://www.vistanetinc.com/vu780781-casdoor-contains-multiple-authentication-bypass-and-access-management-vulnerabilities) — CVE-2026-9093/9095/9097/9098 の 4 件；証明書トラストなし・有効期限チェックなし・audience 制限無視・AuthnRequest 照合なし *(CERT/CC)*

- **[2026-06-01]** [LLMShare: 攻撃者が ChatGPT コンテンツ共有機能でマルウェアを配布 — 正規ドメイン利用でフィルタ回避](https://www.scworld.com/brief/attackers-use-chatgpt-feature-to-spread-malware) — chatgpt.com の信頼シグナルを悪用した新手法；cloaking でセキュリティツールには無害サイトを返答 *(SC Media / Security Boulevard)*

- **[2026-06-01]** [praisonai-platform に複数の権限昇格・IDOR 脆弱性 — GitHub Advisory で一括公開](https://github.com/advisories) — CVE-2026-47418 (ワークスペース Owner への昇格)・CVE-2026-47416 (メンバー削除権限バイパス)・CVE-2026-47409/47414 (IDOR) が公開；AI エージェントプラットフォームの認可設計欠陥が連続して顕在化 *(GitHub Advisory Database)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-05-31 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-41089 | Windows Netlogon (Server 2012R2〜2025) | CWE-121 / 9.8 | 特権不要の Netlogon RPC への細工パケット → スタックバッファオーバーフロー → DC 上で 0-Click RCE | [MSRC](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-41089) (commit不明) | KEV / EPSS高 / 野外悪用確認 |
| CIFSwitch (CVE未割当) | Linux kernel + cifs-utils 6.14+ (Mint / CentOS 9 / Rocky 9 / Alma 9 / Kali / SLES 15 SP7) | CWE-269 / TBD | unprivileged user → cifs.spnego key description に攻撃者制御 pid を注入 → cifs.Upcall が攻撃者 namespace へ切り替え → root 権限 NSS ルックアップ時に malicious libnss*.so をロード → root 昇格 | [oss-security](https://www.openwall.com/lists/oss-security/2026/05/28/2) (upstream patch 済み) | PoC公開 / 2007年来の latent bug |
| CVE-2026-9093 | Casdoor 2.362.0 以前 | CWE-287 / TBD | SAML AudienceRestriction 要素の検証欠落 → 他 SP 向けアサーションを自 SP に受け入れ → なりすまし | (patch未公開) | パッチ未提供 |
| CVE-2026-9095 | Casdoor 2.362.0 以前 | CWE-294 / TBD | SAML assertion のリプレイ保護なし → 傍受したアサーションを再送 → セッション乗っ取り | (patch未公開) | パッチ未提供 |
| CVE-2026-9097 | Casdoor 2.362.0 以前 | CWE-613 / TBD | GetTokenExchangeToken() がトークン取り消し状態を DB 確認せず署名のみ検証 → 失効トークンで永続アクセス → 認証バイパス | (patch未公開) | パッチ未提供 |
| CVE-2026-9098 | Casdoor 2.362.0 以前 | CWE-287 / TBD | SAML callback が AuthnRequest との照合なし → 登録済み IdP を制御できる攻撃者が任意タイミングで unsolicited SAMLResponse を送信 → 持続的な不正アクセス | (patch未公開) | パッチ未提供 |
| CVE-2026-47418 | praisonai-platform (pip, バージョン未確定) | CWE-285 / Critical | PATCH /workspaces/{id}/members/{user_id} に workspace 所有権チェックなし → 任意ワークスペースメンバーが自身を Owner に昇格 → 全データへの管理者アクセス | [GitHub Advisory](https://github.com/advisories) (commit不明) | AI エージェント基盤の認可欠陥 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|---|---|---|---|---|
| 2026-06-01 | JVNVU#95478525 (VU#780781) | Casdoor 2.362.0 以前に SAML 認証バイパス 4 件 — AudienceRestriction・AuthnRequest 照合・リプレイ保護なし、パッチ未公開 | 未定 / 認証バイパス・特権昇格 | [CERT/CC](https://kb.cert.org/vuls/id/780781) / [JVN](https://jvndb.jvn.jp/) |
| 2026-06-01 | ScanNetSecurity — SGLang 脆弱性情報 | SGLang の複数脆弱性 (GGUF モデルによる RCE・pickle デシリアライズ) を国内向けに周知 | CVE-2026-5760 CVSS 9.8 | [ScanNetSecurity](https://scan.netsecurity.ne.jp/article/2026/06/01/55388.html) |
| 2026-05-31 | CVE未割当 (CIFSwitch) | Linux カーネル CIFS upcall LPE が oss-security で PoC 付き公開、国内主要ディストロも影響範囲を確認中 | TBD / ローカル root 昇格 | [oss-security](https://www.openwall.com/lists/oss-security/2026/05/28/2) |

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 25+
- 採用件数: AI=8 / Security=8 / CVE=7 / 国内=3
- 除外理由内訳: 古すぎ (>today-2)=多数 / 重複 (excluded_set)=CVE-2026-0257/35616/39987/44338 他 / 日付不明=0
- 除外済み主要 CVE: CVE-2026-0257 (Palo Alto, 前日) / CVE-2026-35616 (FortiClient EMS, 前日) / CVE-2026-39987 (Marimo, 前日) / CVE-2026-44338 (PraisonAI auth bypass, 前日)
- 除外済み主要ニュース: GreyVibe ChatGPT/Gemini 攻撃 (前日) / FBI FIFA 警告 (5/28, 範囲外) / SymJack (5/27 update, 範囲外) / Axios npm 攻撃 (3月) / Microsoft RAMPART (5/20-21, 範囲外)
- 取得失敗ソース (HTTP 403): BleepingComputer 個別記事多数 / Threat-Modeling.com / US News / Help Net Security 個別記事 / ScanNetSecurity / JPCERT newsflash / NVD検索ページ / kb.cert.org
- 注意: praisonai-platform CVE-2026-47418 の正確な公開日は 403 で未確認 (GitHub Advisory の metadata が「2 days ago」を示唆しており採用); CIFSwitch は BleepingComputer 5/30 公開だが SecurityWeek・Threat-Modeling.com の 5/31 記事が採用基準内

</details>
