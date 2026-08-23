# KEDA Daily Digest — 2026-08-24 (JST)

> 採用範囲: 公開日 2026-08-22 〜 2026-08-24
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

イランに帰属する脅威アクターが英国の小規模発電所を4日間停止させたことが最大の注目点で、イランによる英国エネルギー施設への実被害を伴うサイバー攻撃が公式に確認された初の事例となった。同期間に米国12州の水道インフラへの攻撃も確認されており NCSC/GCHQ が調査中。CVE では StackGres Kubernetes オペレータで CVSS 9.9 の権限昇格 (CVE-2026-78155) が公開され、低権限データベーステナントからクラスタ管理者への昇格が可能。GitLab CE/EE の package registry にパストラバーサル RCE (CVE-2026-10053, CVSS 8.5) が公開、19.0.6/19.1.4/19.2.2 への早急なアップデートが推奨される。HTML サニタイゼーションライブラリ justhtml では to_markdown() の角括弧エスケープ漏れ (CVE-2026-8445, CVSS 9.3) と to_html() の複数サニタイズバイパス (CVE-2026-7808, CVSS 9.3) が同日公開。AI では Google Cloud Vertex AI 上の Claude 3 Haiku が 2026-08-23 付で正式に提供終了となり、Vertex AI 経由の Claude 3 Haiku ユーザーは Claude Haiku 4.5 への移行が完了していない場合リクエストが失敗する状態となっている。

---

## AI 関連ニュース

- **[2026-08-23]** [Claude Haiku Vertex AI Shutdown: Haiku Is Gone, Opus Is Next — Audit Your Partner-Model Routing Now](https://therouter.ai/news/claude-haiku-vertex-ai-shutdown-opus-deprecation-routing/) — Google Cloud Vertex AI 上の Anthropic Claude 3 Haiku が本日 (2026-08-23) 正式に提供終了。Anthropic 直接 API はすでに 2026-04-19 に退役済みだが Vertex AI のパートナーモデルタイムラインは独立しており、Vertex AI 経由で `claude-3-haiku` を使用しているチームはリクエスト失敗に直面する可能性。Claude Haiku 4.5 または Claude Opus 4.8 への移行が必要 *(TheRouter.ai / Google Cloud Docs 2026-08-23)*

---

## セキュリティ関連ニュース

- **[2026-08-23]** [Iran-Linked Hackers Shut Down Small UK Power Plant for 4 Days — First Confirmed Iranian-Attributed Shutdown of UK Energy Facility](https://www.cnbc.com/2026/08/23/small-uk-power-plant-shut-down-after-iran-linked-cyberattack-report.html) — The Telegraph が報道したイランにリンクする脅威アクターによる英国小規模発電所へのサイバー攻撃で、施設が4日間停止。イラン革命防衛隊 (IRGC) 関係ハッカーが英国エネルギー施設を実際に停止させた初のケースとして注目される。英国政府は安全上の理由から施設の場所を非公表。同時期に米国12州の水道インフラへの攻撃も発生。NCSC (GCHQ 傘下) が調査中。DESNZ がエネルギー業界 CEO に状況を説明し、企業向けにサイバーセキュリティ規制更新を通知 *(CNBC / The Telegraph / iHeart 2026-08-23)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-08-22 以降 / CISA KEV 追加 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| GHSA-gf36-c938-gjrw / CVE-2026-78155 | StackGres Kubernetes operator (全バージョン ≤ 修正版未確定) | CWE-426 / **9.9** | 低権限データベーステナントが攻撃者制御の検索パス経由でオペレータに権限昇格 → Kubernetes クラスタ管理者権限奪取 | 修正コミット未公開; GitLab work item ongresinc/stackgres#3177; 公開 **2026-08-23** | CVSS 9.9 / Kubernetes 基盤オペレータ / マルチテナント DB 環境でのクラスタ完全掌握 |
| GHSA-wf6m-786j-gxrr / CVE-2026-8445 | justhtml ≤ 1.11.0 | CWE-79 / **9.3** | 攻撃者制御の入力が `to_markdown()` 内で角括弧・エンティティデコード後テキストをエスケープせずに出力 → Markdown を HTML レンダリングする下流で XSS | justhtml 1.12.0 で修正; 公開 **2026-08-23** | CVSS 9.3 / HTML サニタイザの Markdown 変換パスに設計欠陥 / バリアントハント起点 |
| GHSA-fj35-9vw4-h76v / CVE-2026-7808 | justhtml < 1.16.0 | CWE-79 / **9.3** | `to_html()` の複数バイパス (mutated ポリシー・大小文字混在タグ・doctype シリアライズ・SVG/MathML 外来コンテンツ) → スクリプト/スタイル注入 | justhtml 1.16.0 で修正; 公開 **2026-08-23** | CVSS 9.3 / サニタイザ設計の複数回避経路 / 同ライブラリの別バリアント |
| GHSA-2fpv-gqh2-qq5r / CVE-2026-10053 | GitLab CE/EE 18.8 〜 < 19.0.6 / < 19.1.4 / < 19.2.2 | CWE-22 / **8.5** | 認証済み攻撃者が package registry コンポーネントのパストラバーサル欠陥を特定条件下で悪用 → 任意コード実行 (GitLab プロセス権限) | 19.0.6 / 19.1.4 / 19.2.2 で修正 (GitLab work item #601596); 公開 **2026-08-23** | CVSS 8.5 / 認証済みユーザーによる RCE / GitLab セルフホスト広範利用 / 早急パッチ推奨 |

---

## 国内脆弱性・インシデント情報

採用窓内 (2026-08-22〜08-24) での JVN・JPCERT/CC・IPA 新規公開は確認できなかった (jvn.jp、jpcert.or.jp、ipa.go.jp は EGRESS_BLOCKED により直接確認不可)。

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| therouter.ai (Claude 3 Haiku Vertex AI shutdown) | WebSearch スニペット 2026-08-23 公開確認 ✓; Google Cloud Docs partner-model deprecations 確認 ✓ |
| cnbc.com / telegraph.com / iheart.com (Iran UK power plant cyberattack) | WebSearch スニペット 2026-08-23 公開確認 ✓; CNBC URL 確認 ✓; 複数ソース一致 ✓ |
| github.com/advisories/GHSA-gf36-c938-gjrw (StackGres CWE-426) | **WebFetch 直接取得成功** ✓; Published: August 23, 2026; CVSS 9.9 確認 ✓ |
| github.com/advisories/GHSA-wf6m-786j-gxrr (justhtml XSS to_markdown) | **WebFetch 直接取得成功** ✓; Published: August 23, 2026; CVSS 9.3 確認 ✓ |
| github.com/advisories/GHSA-2fpv-gqh2-qq5r (GitLab path traversal) | **WebFetch 直接取得成功** ✓; Published: August 23, 2026; CVSS 8.5 確認 ✓ |
| github.com/advisories/GHSA-fj35-9vw4-h76v (justhtml sanitizer bypass) | WebSearch スニペット 2026-08-23 公開確認 ✓ (prior research session) |
| jvn.jp / jpcert.or.jp / ipa.go.jp (国内) | EGRESS_BLOCKED — 直接確認不可 |

### 集計サマリ

- **巡回ソース数**: 約 30
- **採用件数**: AI=1 / Security=1 / CVE=4 / 国内=0
- **除外理由内訳**:
  - 採用窓外 (公開日 <2026-08-22): Anthropic protein binder study (2026-08-19/20); Anthropic Theseus Infrastructure/Macquarie/GIC (2026-08-10); xAI Grok Voice Think Fast 2.0 (2026-07-29); Anthropic Claude Security/Project Glasswing (2026-08-21, 08-23 digest 掲載済み)
  - 重複 (excluded_set 参照): OpenAI GPT-5.6 Sol price cut (2026-08-22, 08-23 digest 掲載済み); Claude Academy (2026-08-22, 08-23 digest 掲載済み); CVE-2026-69836 Entra ID (08-23 digest); BTR Reforged (08-23 digest); CVE-2026-59310 VMware vCenter (08-22 digest)
  - .NET Patch Tuesday CVE群 (GHSA-j8gr-8fp3-5q5h 等): GHSA 追加日 2026-08-22 だが CVE 初回開示は Patch Tuesday 2026-08-11 のため除外
  - 取得失敗ソース (EGRESS_BLOCKED): bloomberg.com, thehackernews.com, bleepingcomputer.com, securityweek.com, cisa.gov, nvd.nist.gov, helpnetsecurity.com, jvn.jp, jpcert.or.jp, ipa.go.jp, releasebot.io, aireleasetracker.com

</details>

---

*生成: keda-digest-bot / 2026-08-24 05:04 JST*
