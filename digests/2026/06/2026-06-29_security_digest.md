# KEDA Daily Digest — 2026-06-29 (JST)

> 採用範囲: 2026-06-27 〜 2026-06-29 (JST) | 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

フロンティアAI規制の転換点となった週末: Anthropic Mythos 5 が Commerce Secretary Lutnick 署名の特例書簡でサイバー防衛機関約100社向けに限定再公開され、GPT-5.6 に続いて政府承認ゲートを通過した「管理モデル」体制が具体化。開発ツール攻撃面では Wiz Research が Amazon Q Developer の MCP 設定自動ロード → AWS 認証情報窃取 (CVE-2026-12957) を公開し、IDE プラグインが新たなサプライチェーン攻撃経路として確立された。Linux ページキャッシュ汚染 LPE は DirtyClone (CVE-2026-43503) に続き pedit COW (CVE-2026-46331) の PoC も公開され連続している。

---

## AI ニュース

- **[2026-06-27]** Anthropic、国家安全保障向け限定モデル **Mythos 5** を Commerce Secretary Lutnick 署名の特例書簡付きで約100のサイバー防衛機関向けに再公開。GPT-5.6 Classified に続き「政府承認ゲート」体制が実装段階へ — CNN / NBC News
- **[2026-06-28]** Google DeepMind から著名研究者6名が相次いで退職: Denny Zhou (連鎖推論の父) → Meta、Adler・Pritzel の2名 → Anthropic。DeepMind は「採用・定着は健全」とコメント — TechTimes
- **[2026-06-27]** OpenAI が **2027年 IPO** を視野に Goldman Sachs と協議中; Anthropic は10月 NYSE 上場予定、プレIPO評価額 $965B — Bloomberg
- **[2026-06-27]** **Claude Code v2.1.195** リリース: Dynamic Workflows プレビュー、`/rewind` コマンド、非同期タスク実行の CPU 使用率37%削減 — GitHub Releases (commit: 2026-06-26 21:29 UTC)
- **[2026-06-27]** Wiz Research が **Amazon Q Developer の MCP 設定自動ロード脆弱性** を公開 (CVE-2026-12957/-12958): 悪意リポジトリを `git clone` するだけで AWS 認証情報が窃取される — Wiz Blog / SecurityWeek / The Register

---

## セキュリティニュース

- **[2026-06-27]** Amazon Q Developer (VS Code/JetBrains/Eclipse/Visual Studio) が `.amazonq/mcp.json` をワークスペース信頼確認なしに自動ロード → MCP サーバープロセスが親の AWS 環境変数を継承 → access key/session token 窃取。GitHub Copilot・Cursor 等 IDE×MCP 統合全般へバリアントハント推奨 — Wiz / SecurityWeek
- **[2026-06-27]** Linux kernel **CVE-2026-46331** "pedit COW" の PoC が公開 (June 17 初出): `act_pedit()` が COW 前に共有ページキャッシュへ OOB 書き込み → setuid バイナリ汚染 → ローカル→root。RHEL 8/9/10・Debian・Ubuntu 全般影響 — THN / Red Hat RHSB-2026-008 / TuxCare
- **[2026-06-27]** Infoblox: **DCloud Uni-App** (中国製クロスプラットフォーム OSS フレームワーク) のパブリック API が 236,000+ 詐欺ドメイン運営の中核インフラとして悪用されていることを確認 — SecurityWeek / Infoblox Blog
- **[2026-06-28]** **libssh2 CVE-2026-58051** (GHSA-c5f3-hwj2-xp5p, CVSS v4.0 8.3): `SSH2_REALLOC` による publickey list 拡張時に新エントリを初期化せず → parse failure cleanup で未初期化ポインタ解放 → 悪意 SSH サーバーへの接続だけで GUFP/潜在 RCE。curl・libgit2・WinSCP 等 libssh2 依存製品全般へ影響 — CyberNews / NVD / GHSA
- **[2026-06-28]** **RustDesk CVE-2026-58056** (GHSA-vp3r-hwqm-x826, CVSS 7.6): FileTransfer セッションが per-capability フラグをクリアせず → FileTransfer 認可のみを持つリモートピアが keyboard/mouse インジェクション + display-capture を実行可能。PoC 確認済み — RedPacket / NVD / GHSA

---

## CVE / 脆弱性情報

| CVE / GHSA | 製品 | CWE / CVSS | バグクラス (条件 + sink + 結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-46331 | Linux kernel net/sched `act_pedit` (RHEL 8/9/10, Debian, Ubuntu) | CWE-787 / 8.8 | `tcf_pedit_act()` が COW 範囲をランタイムオフセット解決前に確定 → 共有ページキャッシュへ OOB 書き込み → setuid バイナリ汚染 → ローカル→root | [kernel.org mainline (v6.15-rc backport)](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git) | PoC 公開済み (Jun 17) / Red Hat RHSB-2026-008 / RHEL・Debian・Ubuntu 全般影響 |
| CVE-2026-12957 + CVE-2026-12958 | Amazon Q Developer VS Code / JetBrains / Eclipse / Visual Studio (≤ 2026-05-12 patch) | CWE-1188 / HIGH | `.amazonq/mcp.json` をワークスペース信頼確認なしに自動ロード → MCP サーバープロセスが親プロセスの AWS 環境変数を継承 → access key / session token 窃取 (CVE-12958 は symlink 経由ファイル読み取り) | [AWS 2026-05-12 plugin update (各 IDE マーケットプレイス)](https://github.com/aws/amazon-q-eclipse) | Wiz Research 2026-06-26 公開 / `git clone` だけで RCE+credential theft 成立 / GitHub Copilot・Cursor 等へバリアントハント推奨 |
| CVE-2026-58051 / GHSA-c5f3-hwj2-xp5p | libssh2 ≤ 1.11.1 | CWE-908 / CVSS v4.0 8.3 | `SSH2_REALLOC` で publickey list を拡張するが新エントリを zero-initialize せず → parse failure 時の cleanup パスで未初期化 attrs ポインタを解放 → 悪意 SSH サーバーへの接続だけで GUFP / 潜在 RCE | [libssh2 mainline commit (リリース版未確定)](https://github.com/libssh2/libssh2/commits/master) | 2026-06-28 GHSA 公開 / MITM 不要 (接続先が悪意 SSH サーバーであれば成立) / curl・libgit2・WinSCP 等依存ライブラリへバリアントハント推奨 |
| CVE-2026-58056 / GHSA-vp3r-hwqm-x826 | RustDesk (脆弱バージョン) | CWE-285 / CVSS 7.6 | FileTransfer セッションが per-capability フラグをクリアしないため FileTransfer 認可のみを持つピアが keyboard/mouse インジェクション + display-capture ハンドラーを呼び出し可能 → 認可境界違反 | [rustdesk/rustdesk issue #14576 対応コミット](https://github.com/rustdesk/rustdesk/commits/master) | 2026-06-28 GHSA 公開 / PoC 確認済み / AnyDesk・Parsec 等 RDP 系製品へ Capability フラグ残留パターンのバリアントハント推奨 |
| GHSA-72r4-9c5j-mj57 + GHSA-fr4h-3cph-29xv | pnpm < 11.5.3 (同バッチ残り2件) | CWE-22 / HIGH | `patch-remove` が `patches/` 外のファイル削除を許可 / hoisted install でロックファイルエイリアスが `node_modules` 外を参照 → 任意ファイル削除・サプライチェーン汚染 | [pnpm v11.5.3 リリース](https://github.com/pnpm/pnpm/releases/tag/v11.5.3) | 2026-06-27 GHSA 公開 (前日 CVE-2026-55700/-55698/GHSA-qrv3 と同バッチ残り2件) / npm エコシステム全般影響 |

---

## 国内脆弱性 / インシデント

> 直近2日間 (2026-06-27〜29 JST) に該当する新規国内脆弱性・インシデントは確認できませんでした。

*参考: KDDI 不正ログイン被害 (14.2M メール) は 2026-06-24 JST 公開で採用窓外。Yokogawa CVE-2026-11833 は 2026-06-25 アドバイザリで採用窓外。*

---

<details>
<summary>収集メタデータ / デバッグ情報</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| github.com/advisories (Jun 27-29 filter) | GHSA-c5f3 (libssh2), GHSA-vp3r (RustDesk), GHSA-72r4 + GHSA-fr4h (pnpm) 取得 ✓ |
| github.com/anthropics/claude-code/releases | v2.1.195 (2026-06-26 21:29 UTC = JST Jun 27) 確認 ✓ |
| wiz.io blog (Amazon Q CVE-2026-12957/-12958) | 2026-06-26 UTC 公開確認 ✓ |
| SecurityWeek (DCloud Uni-App, Amazon Q) | 2026-06-27 UTC 確認 ✓ |
| THN / Red Hat (pedit COW CVE-2026-46331) | 2026-06-27 UTC 公開確認 ✓ |
| Bloomberg (OpenAI IPO 2027) | 2026-06-26 UTC 確認 ✓ |
| TechTimes (DeepMind exodus) | 2026-06-28 UTC 確認 ✓ |
| CNN / NBC (Anthropic Mythos 5) | 2026-06-26〜27 UTC 確認 ✓ |
| cisa.gov/known-exploited-vulnerabilities-catalog | 403 — WebSearch で代替確認 |
| anthropic.com/news | 403 — WebSearch で代替確認 |
| openai.com/news | 403 — WebSearch で代替確認 |
| vulnerability.circl.lu | 403 — NVD / GHSA で代替確認 |

### 集計サマリ

- **AI ニュース**: 5 件
- **セキュリティニュース**: 5 件
- **CVE エントリ**: 5 件 (3 CVE + 2 GHSA バッチ)
- **国内インシデント**: 0 件
- **採用窓外として除外**: KDDI (Jun 24 JST), Yokogawa (Jun 25), libssh2 CVE-2026-55200 (Jun 24 UTC), Nezha CVE-2026-53519〜53523 (Jun 12)
- **重複除外**: GPT-5.6 / Anthropic injunction (Jun 27 digest 掲載済み) / pnpm CVE-2026-55700/-55698/GHSA-qrv3 (Jun 28 digest 掲載済み) / CVE-2026-43503 DirtyClone (Jun 27 digest 掲載済み)

</details>
