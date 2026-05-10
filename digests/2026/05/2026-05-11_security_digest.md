# KEDA Daily Digest — 2026-05-11 (JST)

> 採用範囲: 公開日 2026-05-09 〜 2026-05-11
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

---

## AI 関連ニュース

> 直近2日間に該当する新規ニュースは確認できませんでした。

---

## セキュリティ関連ニュース

### [続報] Instructure (Canvas LMS) — ShinyHunters が交渉拒否を宣言・5/12 リーク期限を通告、サービスは一部復旧

- **公開日**: 2026-05-09
- **ソース**: Al Jazeera
- **要約**:
  - Canvas LMS が一部機能を復旧した一方、ShinyHunters は Instructure が身代金交渉を拒否していると公言し、**2026-05-12 を最終期限**として応じなければ 2.75 億件（3.65 TB）の全データを公開すると宣告した。ペン大学 (Penn University) が $1M の支払いを試みたが失敗に終わったとも報告されている。
  - 窃取データのサンプル（学生・教職員の PII、プライベートメッセージ等）はすでに公開済み。被害規模は教育分野史上最大級であり、世界 9,000 校超の利用機関が対応を迫られている。Instructure にとって 8 ヶ月以内 2 度目の ShinyHunters 侵害となる。
  - 5/12 の期限が目前に迫っており、Canvas 利用機関は影響を受ける可能性のある学生・教職員・保護者への通知準備、身元保護サービスの手配、ダウンタイム時の代替手段確認を今すぐ実施すること。
- **リンク**: <https://www.aljazeera.com/news/2026/5/9/hacked-educational-platform-partially-restored-for-millions-of-students>

---

### cPanel / WHM — 3 件の新規脆弱性を修正 (CVE-2026-29201 / CVE-2026-29202 / CVE-2026-29203)

- **公開日**: 2026-05-09
- **ソース**: The Hacker News
- **要約**:
  - cPanel / WHM が新たに発見された 3 件の脆弱性を修正するパッチを公開した。`CVE-2026-29201`（CVSS 4.3）は認証済みユーザーによる任意ファイル読み取り。`CVE-2026-29202`（CVSS 8.8）は認証済みユーザーによる任意 Perl コード実行。`CVE-2026-29203`（CVSS 8.8）はシムリンク処理の欠陥を突いた DoS・権限昇格。現時点で野外での悪用は確認されていない。
  - 先週 CVE-2026-41940（cPanel ゼロデイ）がグアム政府機関等を標的とする攻撃で実際に悪用されたことを受け、cPanel 環境全体への注目が高まっているタイミングでの追加 CVE 開示。CVSS 8.8 が 2 件含まれており、管理者権限を持つ攻撃者に侵害済みホストを完全制御される可能性がある。
  - 対応: cPanel / WHM を最新リリースへ即座にアップグレードし、管理者アカウントの認証情報・多要素認証・アクセス制御リストの見直しを実施すること。
- **リンク**: <https://thehackernews.com/2026/05/cpanel-whm-release-fixes-for-three-new.html>

---

## 国内脆弱性・インシデント情報

> 直近2日間に該当する新規ニュースは確認できませんでした。

---

## 本日のサマリ

採用期間 (2026-05-09〜05-11) は週末にかかるため新規報道が限定的だった。最優先の対応は **Canvas LMS 侵害の[続報]**: ShinyHunters が 2026-05-12 を最終リーク期限として設定しており、Instructure 利用機関は今日中に学生・教職員への通知体制と身元保護サービスの手配を完了させる必要がある。次いで **cPanel の新規 3 CVE**: 先週の実悪用ゼロデイ (CVE-2026-41940) に続き CVSS 8.8 級の脆弱性が追加開示された。cPanel / WHM を運用する組織は即時アップグレードを実施すること。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 22 (AI/Security/国内カテゴリ)
- 採用件数: AI=0 / Security=2 / 国内=0
- 除外理由内訳:
  - 古すぎ (採用窓外 3 日以上前): OpenAI 音声 AI モデル (05-07/08), Microsoft Semantic Kernel RCE CVE-2026-25592/26030 (05-07), FastGPT SSRF CVE-2026-44284 (05-08), Oracle/Anthropic Claude Mythos 活用発表 (05-05〜08), NHS England GitHub 非公開化命令 (05-05〜06), "Dirty Frag" Linux 特権昇格 CVE-2026-43284/43500 (05-07〜08), TCLBANKER バンキングトロイ (05-08), Sentry SAML 認証バイパス CVE-2026-42354 (05-08), Let's Encrypt 証明書発行停止 (05-08), Microsoft ASP.NET 緊急パッチ CVE-2026-40372 (04-22), "We Scanned 1M Exposed AI Services" THN (05-05), "2026: The Year of AI-Assisted Attacks" THN (05-04), Microsoft Security Blog "When prompts become shells" (05-07)
  - 重複 (過去 7 日分 excluded_set に既出): CVE-2026-6973 (Ivanti EPMM), CVE-2026-0300 (PAN-OS GlobalProtect), CVE-2026-31431 (Copy Fail), CVE-2026-23918 (Apache HTTP/2), Canvas 初報 (05-10 digest), cPanel CVE-2026-41940 (05-06 digest)
  - 日付不明・採用窓外: Suzuki cyberattack (報道に「土曜 5/10」の記述矛盾あり除外), eSecurity Planet 週次まとめ (特定日付不明のため除外)
- 取得失敗ソース (HTTP 403 等): bleepingcomputer.com, thehackernews.com (直接), securityweek.com, cisa.gov, jvn.jp — 検索スニペット・ミラーサイト URL 日付パターンで代替確認
- 備考: 採用期間が土〜月曜 (05-09〜05-11) のため週末分の新規報道が少なく AI・国内セクションは空見出しとなった。公開日は ミラーブログ URL パス (thomasharris6.wordpress.com/2026/05/09/ 等) および Al Jazeera URL パス (/news/2026/5/9/) から確認した。

</details>
