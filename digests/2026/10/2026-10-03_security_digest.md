# KEDA Daily Security Digest — 2026-10-03 (JST)

> 採用ウィンドウ: 2026-10-01 〜 2026-10-03 | 生成: 2026-10-03T05:15 JST

---

## AI ニュース

- **[2026-10-02] Anthropic、$1億規模の AI エンジニアリング研修プログラムを発表** — 高校・大学生向けに AI 開発スキルを教育する官民連携プログラム。Anthropic newsroom 発表。
- **[2026-10-02] OpenAI、安全研究者 3 名を内部情報の不適切取り扱いで解雇** — 機密情報の持ち出しに関わる内部規律案件。安全チームへの影響が懸念される。
- **[2026-10-02] [続報] Google Gemini 4 Argon — OpenAI/Anthropic モデルとの性能比較分析** — フロンティア LLM のベンチマーク争い継続。CNBC 報道 (2026-10-02)。
- **[2026-10-01] Microsoft Digital Defense Report 2026 発表** — 「脅威アクターが AI 活用で防御側を上回りつつある」と警告。年次セキュリティ報告書。

---

## セキュリティニュース

- **[2026-10-02] アサヒグループホールディングス、Qilin ランサムウェア被害が継続** — 10/2 に生産再開を発表する一方、Qilin グループが 27GB のデータ窃取を主張。9/29 の初報以降初のアップデート。
- **[2026-10-01] CISA KEV 更新: CVE-2026-104286 (Fortinet FortiMail)** — パストラバーサル脆弱性が実際の攻撃で悪用されているとして Known Exploited Vulnerabilities カタログに追加。

---

## CVE / アドバイザリ

| CVE | 製品 | CWE | CVSS (v3.1 / v4.0) | 概要 | パッチ / 対応 |
|---|---|---|---|---|---|
| CVE-2026-92948 | vm2 (NodeVM) | CWE-693: 保護メカニズムの失敗 | 9.9 / 9.4 (Critical) | `node:test.run()` を利用したサンドボックスの許可リストバイパス。任意コード実行が可能。 | vm2 3.11.7 で修正 (2026-10-01 公開) |
| CVE-2026-104286 | Fortinet FortiMail | CWE-22: パストラバーサル | 未公表 (High) | 認証不要の任意ファイル書き込み。CISA KEV に 2026-10-01 追加。実攻撃確認済み。 | FortiMail 最新版へのアップデート推奨 |

---

## 国内動向

- **[2026-10-02] アサヒグループホールディングス (Qilin ランサムウェア)** — 上記「セキュリティニュース」と同件。製造業へのランサムウェア攻撃が継続。10/2 の生産再開発表後もデータ漏洩リスクが残存。

---

## 参照リンク

- Anthropic $100M プログラム: https://www.anthropic.com/news/
- CISA KEV (CVE-2026-104286): https://www.cisa.gov/known-exploited-vulnerabilities-catalog
- vm2 CVE-2026-92948: https://github.com/patriksimek/vm2/security/advisories
- Microsoft Digital Defense Report 2026: https://www.microsoft.com/en-us/security/security-insider/microsoft-digital-defense-report-2026

---

*注: thehackernews.com・bleepingcomputer.com・darkreading.com・securityaffairs.com・therecord.media・cisa.gov 等はプロキシによりアクセス不可。検索スニペット・Anthropic newsroom・GitHub Advisories 等の代替ソースを使用。*
