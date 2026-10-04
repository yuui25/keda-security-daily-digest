# KEDA Daily Security Digest — 2026-10-05 (JST)

> 採用ウィンドウ: 2026-10-03 〜 2026-10-05 | 生成: 2026-10-05T05:15 JST

---

## 本日のサマリ

Linux KVM のゲスト→ホスト VM 脱出ゼロデイが Vercel により確認され、AI エージェントサンドボックス基盤への影響が注目されている。ZITADEL では IdP 連携フローの実装不備を突く認証乗っ取り (CVE-2026-105215, CVSS 9.1) を含む 3 件の脆弱性が一括修正された。Adversa AI の調査では主要 AI コーディングエージェント 7 製品すべてがトロイの木馬化プラグイン攻撃に対して 92.5% の成功率で侵害されることが明らかになった。

---

## AI ニュース

- **[2026-10-03] Vercel CEO が Linux KVM ゼロデイ (ゲスト→ホスト root 脱出) を公式確認** — 研究者 Paulos Yibelo が Linux KVM の VM エスケープを実証; Vercel CEO Guillermo Rauch が X 上で確認し $50K バウンティを授与; KVM を使用する AI エージェントサンドボックス全般への影響が懸念される。CVE 未割当、詳細ライトアップ公開準備中 *(CyberSecurityNews / mallory.ai)*
- **[2026-10-04] Adversa AI、主要 AI コーディングエージェント 7 製品すべてがトロイの木馬化プラグイン攻撃に脆弱と報告** — Claude Code・OpenAI Codex・Cursor・Goose・Qwen Code・Grok Build・Hermes Agent を対象に 10 の攻撃目標を試行; 平均成功率 92.5%; プラグイン署名のサイレントスワップが Claude Code・GitHub Copilot・Gemini CLI で確認 *(adversa.ai / DEV Community)*

---

## セキュリティニュース

- **[2026-10-03] Linux KVM ゼロデイ — ゲスト VM からホスト root 権限への脱出を実証** — 研究者 Paulos Yibelo が概念実証を Vercel に報告; Vercel が脆弱性を確認しパッチ適用済み; KVM ベースのクラウド・エッジ・AI サンドボックス環境での悪用リスク; 技術詳細は現時点で非公開 *(CyberSecurityNews / cryptika.com)*

---

## CVE / アドバイザリ

| CVE | 製品 | CWE | CVSS (v3.1 / v4.0) | 概要 | パッチ / 対応 |
|---|---|---|---|---|---|
| CVE-2026-105215 | ZITADEL < 3.4.14 / 4.x < 4.16.2 | CWE-287: 不適切な認証 | 9.1 / — (Critical) | 未認証攻撃者が Login V1 UI の「外部アカウント未登録」登録エンドポイントに細工した IDPConfigID+ExternalUserID を送信 → IdP コールバック完了前にアカウントを事前作成 → 被害者の正規ログイン時に攻撃者制御アカウントにセッションが紐付く → アカウント乗っ取り | ZITADEL 3.4.14 / 4.16.2 (2026-10-04 公開) |
| CVE-2026-105212 | ZITADEL | CWE-287 | 7.5 / — (High) | ZITADEL における認証バイパス。上記 CVE-2026-105215 と同一パッチバッチに含まれる。 | ZITADEL 3.4.14 / 4.16.2 (2026-10-04 公開) |
| CVE-2026-105211 | ZITADEL | CWE-200 | 8.1 / — (High) | ZITADEL における情報漏洩・認証バイパス。上記 CVE-2026-105215 と同一パッチバッチに含まれる。 | ZITADEL 3.4.14 / 4.16.2 (2026-10-04 公開) |

---

## 国内動向

> 直近2日間に該当する新規ニュースは確認できませんでした。

---

## 参照リンク

- Vercel KVM ゼロデイ: https://cybersecuritynews.com/linux-kvm-zero-day/
- Adversa AI コーディングエージェント調査: https://adversa.ai/blog/
- ZITADEL CVE-2026-105215 (GHSA-25rw-g6ff-fmg8): https://github.com/zitadel/zitadel/security/advisories/GHSA-25rw-g6ff-fmg8

---

## Debug

- 採用窓: 2026-10-03 〜 2026-10-05 (JST)
- 巡回ソース数: 30+
- 採用件数: AI=2 / Security=1 / CVE=3 / 国内=0
- 除外理由内訳:
  - 採用窓外 (公開日 < 2026-10-03 またはウィンドウ外):
    - Microsoft Titan Analytics JWT bypass (blog.faav.net: 2026-09 公開)
    - UK AISI Mythos 5 レポート (thehackernews.com URL パス: 2026/08/ 公開)
    - Dell CSM CVE-2026-63688/63692 (DSA-2026-448: 2026-10-01 公開、採用窓前)
    - Apache HTTP Server JVNVU#94648869 (2026-10-02 公開、採用窓前)
    - Check Point CVE-2026-50751 (2026-06 公開)
    - Gitea Runner CVE-2026-73802 (公開日未確認、除外)
    - @a2ui/web_core CVE-2026-10032 (実際の公開日: 2026-08-04)
  - 重複 (直近7日 digest 既報):
    - vm2 CVE-2026-92948, FortiMail CVE-2026-104286, OpenAI 安全研究者解雇, Microsoft Digital Defense Report 2026, Asahi Group Qilin (10-03 digest)
    - GitLab AI Gateway CVE-2026-90970, NASA CVE-2026-105105, OpenAM CVE-2026-105115/105119/105122, Storm-2603 (10-04 digest)
  - 取得失敗ソース (EGRESS_BLOCKED): jvn.jp, jpcert.or.jp, bleepingcomputer.com, thehackernews.com, helpnetsecurity.com, securityaffairs.com, gbhackers.com, cybernewsweekly.substack.com, darkreading.com

*注: jvn.jp・jpcert.or.jp 等はプロキシによりアクセス不可。GitHub Security Advisories・検索スニペット・公式ベンダーソース等の代替ソースを使用。*
