# KEDA Daily Digest — 2026-05-22 (JST)

> 採用範囲: 公開日 2026-05-20 〜 2026-05-22
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Drupal Core の PostgreSQL 環境向け匿名 SQL インジェクション (CVE-2026-9082) と Linux カーネルの 9 年越し ptrace 競合 (CVE-2026-46333 / ssh-keysign-pwn) が 5/20 に同時公開され、いずれも低権限から root 相当の影響を持つ。CISA は Microsoft Defender の野外悪用中ゼロデイ 2 件 (CVE-2026-41091/45498 = RedSun/UnDefend) を含む計 7 CVE を KEV に一括追加。AI 面では Anthropic が Managed Agents に MCP Tunnels をベータ提供、Fox Tempest マルウェア署名 MaaS の解体と First VPN の Europol 摘発によりランサムウェアインフラ撲滅が加速した。

---

## AI 関連ニュース

- **[2026-05-20]** [Anthropic が Managed Agents に MCP Tunnels (リサーチプレビュー) とセルフホスト・サンドボックス (ベータ) を提供開始](https://the-decoder.com/anthropic-launches-managed-infrastructure-for-autonomous-ai-agents/) — Code with Claude London (5/20–21) に合わせ、企業内部の MCP サーバーへのトンネル接続と AI エージェント実行環境の分離をサポート、プライベートインフラへの安全なエージェント展開を実現 *(the-decoder.com)*

- **[2026-05-20]** [Microsoft の DCU が Fox Tempest マルウェア署名 MaaS を解体](https://www.microsoft.com/en-us/security/blog/2026/05/19/exposing-fox-tempest-a-malware-signing-service-operation/) — Microsoft Artifact Signing を悪用して短命コード署名証明書を 1,000 件超発行・販売、Rhysida/Akira/Qilin/BlackByte RaaS に提供していた signspace[.]cloud をドメイン差し押さえと VM 停止で壊滅 *(Microsoft Security Blog)*

- **[2026-05-20]** [Verizon DBIR 2026: 脆弱性悪用が 19 年ぶりに認証情報窃取を抜き侵害起点 No.1 に](https://www.helpnetsecurity.com/2026/05/20/verizon-2026-dbir-findings/) — 全侵害の 31% が脆弱性悪用起因 (前回 13%)、AI が既知 CVE の攻撃自動化を加速しパッチ適用中央値は 43 日に増加。第三者起因の侵害は前年比 60% 増 *(Help Net Security)*

- **[2026-05-21]** [GitHub が TanStack npm サプライチェーン攻撃経由で内部リポジトリ 3,800 件が侵害されたと確認](https://www.bleepingcomputer.com/news/security/github-confirms-breach-of-3-800-repos-via-malicious-vscode-extension/) — TeamPCP が悪意ある Nx Console v18.95.0 (VS Code 拡張) を 18 分間 Marketplace に公開、npm/AWS/GCP/GitHub 認証情報を窃取する AI 開発ツールサプライチェーン攻撃と判明 *(BleepingComputer)*

- **[2026-05-21]** [Microsoft が Edge 148 でパスワード平文メモリ読み込みを廃止](https://www.malwarebytes.com/blog/news/2026/05/microsoft-is-changing-edges-plaintext-password-behavior) — 起動時に全保存パスワードを平文でメモリにロードする設計を「意図的」と弁明後に方針転換、次回安定版で全チャネルに反映し他 Chromium ブラウザ並みの保護へ移行 *(Malwarebytes)*

- **[2026-05-20]** [Europol が Operation Saffron で First VPN サービスを解体、ウクライナで管理者を逮捕](https://www.helpnetsecurity.com/2026/05/21/operation-saffron-first-vpn-takedown/) — ランサムウェア犯罪者が多用していた VPN サービス First VPN の 33 サーバーを 27 か国で押収、数千人の犯罪ユーザーを特定しランサムウェア攻撃インフラを直撃 *(Help Net Security)*

---

## セキュリティ関連ニュース

- **[2026-05-20]** [CISA が 7 CVE を KEV に追加、Microsoft Defender ゼロデイ 2 件に 6/3 まで対応期限](https://www.cisa.gov/news-events/alerts/2026/05/20/cisa-adds-seven-known-exploited-vulnerabilities-catalog) — CVE-2026-41091 (Defender LPE) + CVE-2026-45498 (Defender DoS) の RedSun/UnDefend ペアを含む 7 件を一括追加、連邦機関に 2026-06-03 までのパッチ適用を義務付け *(CISA)*

- **[2026-05-20]** [Drupal SA-CORE-2026-004: 高度に深刻な SQL インジェクション (CVE-2026-9082) を緊急修正](https://www.drupal.org/sa-core-2026-004) — PostgreSQL 使用サイトで匿名ユーザーが任意 SQL を注入可能。Drupal Core 10.4.x/10.5.x/10.6.x/11.x 全ブランチが影響、サポートバージョンは即時アップデートが必要 *(Drupal.org)*

- **[2026-05-20]** [SonicWall Gen6 SSL-VPN が CVE-2024-12802 の不完全パッチ悪用で大規模 MFA バイパス攻撃に](https://www.bleepingcomputer.com/news/security/hackers-bypass-sonicwall-vpn-mfa-due-to-incomplete-patching/) — Gen6 では firmware 更新後に 6 つの手動設定手順が必要だが見落とされやすく、自動ツールで 13 回の試行でも VPN 突破成功、30 分以内にランサムウェア展開準備が完了 *(BleepingComputer)*

- **[2026-05-21]** [Microsoft が Defender ゼロデイ CVE-2026-41091 + CVE-2026-45498 をアウトオブバンドパッチ適用](https://www.helpnetsecurity.com/2026/05/21/microsoft-defender-vulnerabilities-cve-2026-41091-cve-2026-45498/) — 野外悪用開始から 6 週間を経てパッチ提供。DoS で Defender を無力化 (CVE-2026-45498) → LPE で SYSTEM 権限奪取 (CVE-2026-41091) の 2 段攻撃が Huntress により観測済み *(Help Net Security)*

- **[2026-05-20]** [Qualys が Linux カーネル CVE-2026-46333 (ssh-keysign-pwn) の詳細と PoC を公開](https://blog.qualys.com/vulnerabilities-threat-research/2026/05/20/cve-2026-46333-local-root-privilege-escalation-and-credential-disclosure-in-the-linux-kernel-ptrace-path) — 9 年越しの ptrace 競合が SSH 秘密鍵・/etc/shadow 漏洩・root RCE を可能に。4 種類の動作するエクスプロイトが公開済み、ptrace_scope=2 設定がすぐに使える緩和策 *(Qualys Blog)*

- **[2026-05-21]** [cPanel CVE-2026-41940 が政府機関・MSP を標的とした攻撃に拡大](https://thehackernews.com/2026/05/critical-cpanel-vulnerability.html) — フィリピン・ラオスの政府・軍ドメインおよび MSP/ホスティングに向けた攻撃が継続中、ファイルマネージャーバックドアと "Sorry" ランサムウェアの 2 系統が観測 *(The Hacker News)*

- **[2026-05-21]** [Europol の First VPN 解体で数千件のランサムウェア攻撃との接続が判明](https://www.bleepingcomputer.com/news/security/police-seize-first-vpn-service-used-in-ransomware-data-theft-attacks/) — Rhysida/INC 等に使われていた First VPN の管理者を逮捕、サービス利用の犯罪者に対して当局が個人特定済みと通知 *(BleepingComputer)*

- **[2026-05-21]** [Microsoft が Fox Tempest 解体の詳細を公開、Qilin/BlackByte を含む主要 RaaS との接続を明示](https://www.bleepingcomputer.com/news/security/cybercrime-service-disrupted-for-abusing-microsoft-platform-to-sign-malware/) — 72 時間有効な短命証明書を $5,000〜$9,000/BTC で販売、AnyDesk/Teams/PuTTY に偽装したマルウェアが正規署名付きで配布されていた *(BleepingComputer)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-05-20 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-9082 | Drupal Core 8.9.0 〜 10.4.9 / 10.5.x〜9 / 10.6.x〜8 / 11.x〜 (PostgreSQL 使用サイト) | CWE-89 / 6.5 | DB API の `$values` 配列キーに `array_values()` が欠落 → ユーザー制御の PHP キーが SQL プレースホルダに到達 → 匿名ユーザーが任意 SQLi → RCE/権限昇格可能 | [SA-CORE-2026-004](https://www.drupal.org/sa-core-2026-004) (commit 不明) | Drupal 「Highly Critical」 |
| CVE-2026-46333 | Linux kernel 5.6 〜 7.0.7 以前 (Nov 2016 で導入) / 主要 distro デフォルト構成 | CWE-362 / 5.5 | `__ptrace_may_access()` が `mm==NULL` のタスクに対して dumpable チェックをスキップ → `pidfd_getfd(2)` で exit 中 SUID プロセスの fd を窃取 → `/etc/shadow` + SSH ホスト秘密鍵の漏洩、SYSTEM 経由で任意コマンド実行 | [commit 31e62c2ebbfd](https://git.kernel.org/linus/31e62c2ebbfd) (stable 6.18.31/6.12.89 等に反映) | PoC 公開済み・攻撃容易 |
| CVE-2026-41091 | Microsoft Defender Malware Protection Engine ≤ 1.1.26030.3008 | CWE-59 / 7.8 | スキャンエンジンがシンボリックリンクを検証前に辿る (link-following) → 低権限攻撃者が symlink を非保護パスから `SAM` 等に張ることで SYSTEM 権限でファイルアクセス/書換え → LPE | MMPE 1.1.26040.8 (Windows Update 自動配布、commit 非公開) | KEV ✓ / EPSS 高 |
| CVE-2026-45498 | Microsoft Defender Antimalware Platform ≤ 4.18.26030.3011 | CWE-400 / 4.0 | 特定入力で Defender を DoS 状態に → アンチマルウェア保護が無音で停止 → CVE-2026-41091 と連鎖し 2 段攻撃 (blindside+escalate) を形成 | Antimalware Platform 4.18.26040.7 (自動配布、commit 非公開) | KEV ✓ / 連鎖悪用確認済み |
| GHSA-c9j4-9m59-847w [続報] | Nx Console VS Code 拡張 v18.95.0 (npmconsole/nx-console) | CWE-506 / — | 悪意ある公式パッケージを Marketplace 経由で配布 → 開発者端末の npm/AWS/GCP/GitHub 認証情報を外部へ送信 → GitHub 内部リポジトリ 3,800 件侵害に連鎖 | [v18.96.0](https://github.com/nrwl/nx-console/security/advisories/GHSA-c9j4-9m59-847w) | サプライチェーン・実被害確認 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|---|---|---|---|---|
| 2026-05-20 | CVE-2026-9082 (国内影響) | PostgreSQL 構成の国内 Drupal サイトに SQLi → RCE リスク、即時バージョンアップが必要 | 6.5 (Drupal: Highly Critical) | [SA-CORE-2026-004](https://www.drupal.org/sa-core-2026-004) |
| 2026-05-20 | CVE-2026-46333 (国内影響) | 国内データセンター・クラウド上の Ubuntu/Debian/RHEL Linux サーバー全般に ssh-keysign-pwn 影響、ptrace_scope 設定と kernel 更新を急ぐ | 5.5 / PoC 公開 | [Qualys Blog](https://blog.qualys.com/vulnerabilities-threat-research/2026/05/20/cve-2026-46333-local-root-privilege-escalation-and-credential-disclosure-in-the-linux-kernel-ptrace-path) |
| 2026-05-21 | TanStack npm 侵害 (国内影響) | TanStack Query/Router 等を使用する国内 Node.js 開発者は CI/CD シークレット漏洩を確認、Nx Console v18.95.0 使用者は即時アンインストールを | — / 開発インフラ全体に波及 | [BleepingComputer](https://www.bleepingcomputer.com/news/security/github-confirms-breach-of-3-800-repos-via-malicious-vscode-extension/) |

> 直近2日間に日本固有の JVN/JPCERT 新規アドバイザリは検索エンジン経由では確認できませんでした。JPCERT/CC の Drupal・Defender 関連アドバイザリが 5/20–21 に発行された可能性が高く、[jpcert.or.jp/at/](https://www.jpcert.or.jp/english/at/) を直接確認してください。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 15+ (THN, BleepingComputer, CISA, Qualys Blog, Microsoft Security Blog, HelpNetSecurity, SecurityWeek, Drupal.org, Verizon, Malwarebytes, Help Net Security, the-decoder.com, Europol/CyberScoop, Unit 42, PPLN Japan)
- 採用件数: AI=6 / Security=8 / CVE=5 / 国内=3 (一部グローバル)
- 除外理由内訳:
  - 古すぎ (today-3 以前): Boggy Serpens (3/27), Palo Alto Defenders Guide May (5/13), WEF report (5/4-5), CVE-2026-29201/29202/29203 (5/8), OpenAI GPT-5.5-Cyber (5/1), Anthropic Mythos 金融規制当局ブリーフィング (5/18), Verizon DBIR (5/19→5/20 報道で採用), ClaudeBleed (5/7), Microsoft MDASH blog (5/12)
  - 重複 (excluded_set に存在): CVE-2026-42945 (NGINX), CVE-2026-45585 (YellowKey), CVE-2026-42897 (Exchange), CVE-2026-20182 (Cisco SD-WAN), CVE-2026-41940 (cPanel auth bypass), GHSA-c9j4-9m59-847w (Nx Console、続報として採用)
  - 日付不明: 一部 Palo Alto ブログ記事 (パス /2026/05/ だが日付特定不可)
- 取得失敗ソース: thehackernews.com (直接 fetch 403), bleepingcomputer.com (直接 fetch 403), drupal.org/sa-core-2026-004 (403), nvd.nist.gov (403), jvn.jp (403), jpcert.or.jp (403), infoq.com (403) — WebSearch 経由で補完

</details>
