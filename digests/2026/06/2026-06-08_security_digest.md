# KEDA Security Daily Digest — 2026-06-08

> 採用範囲: 2026-06-06 〜 2026-06-08 (JST)｜前回除外済み項目はスキップ

---

## AI News

- **Trump政権、OpenAI/Anthropic/xAIへの政府持分取得を協議中** — 国家安全保障上の利益確保を名目に財務省主導で検討。業界団体は規制上の利益相反を懸念。([TechCrunch, 2026-06-06](https://techcrunch.com/2026/06/06/the-trump-administration-might-take-an-equity-stake-in-openai/))

- **WWDC 2026開幕(6/8)—SiriをGoogle Gemini 1.2Tパラメータモデルで再構築、AI ExtensionsでChatGPT/Gemini/Claude切替に対応** — AppleはオンデバイスLLMとクラウドモデルのハイブリッド構成を発表。サードパーティAI拡張はユーザー明示選択制。([TechRepublic](https://www.techrepublic.com/article/news-apple-wwdc-26-live-blog/) / [MacRumors](https://www.macrumors.com/roundup/wwdc/), 2026-06-08)

- **Claude Code GitHub Actionに権限昇格・prompt injection脆弱性(CVSS 4.0: 7.8)—v1.0.94で修正済み** — GMO Flattの RyotaK氏が発見。`checkWritePermissions`が`[bot]`サフィックスを無条件信頼する欠陥により、Issue本文経由のprompt injectionで`/proc/self/environ`からAPIキー等の環境変数を窃取可能。RyotaK氏は計50種のバイパス手法を確認。([The Hacker News, 2026-06-06](https://thehackernews.com/2026/06/claude-code-github-action-flaw-let-one.html))

---

## Security News

- **InstagramのパスワードリセットAPIが未マスクのメール/電話番号を返却—Metaが緊急ホットフィックスを当日展開** — パスワードリセットフローのレスポンスJSONに他ユーザーの連絡先情報が平文で含まれる不具合。報告から数時間以内にMetaが修正。影響範囲は調査中。([CybersecurityNews, 2026-06-06](https://cybersecuritynews.com/instagram-password-reset-user-phone/))

- **CISA KEV追加: SolarWinds Serv-U CVE-2026-28318—12,000台超がShodanで露出、修正期限6/19** — 非認証攻撃者が`Content-Encoding: deflate`POSTリクエストでデーモンをクラッシュさせるDoS脆弱性。CISA はFCEB機関に6月19日までのパッチ適用を義務付け。修正版: Serv-U 15.5.4 HF1。([BleepingComputer, 2026-06-07](https://www.bleepingcomputer.com/news/security/cisa-hackers-now-exploit-solarwinds-serv-u-flaw-to-crash-servers/))

- **Claude Code GitHub Action脆弱性—サプライチェーンリスク: 悪意あるcommitをAnthropicリポジトリ自体へpush可能** — Microsoft Threat Intelligenceが同日独立検証を公開。攻撃者はprompt injectionでCI/CDエージェントを操作し、上流リポジトリへのコード改ざんが可能。CI/CDパイプラインでの最小権限設計の重要性を改めて提起。([Microsoft Security Blog, 2026-06-05](https://www.microsoft.com/en-us/security/blog/2026/06/05/securing-ci-cd-in-agentic-world-claude-code-github-action-case/))

- **TechCrunch「2026年上半期 最悪のハック&侵害」まとめ公開** — Jan〜Jun上旬の主要インシデントを網羅。Volt TyphoonによるISP侵害、AIシステムへの攻撃増加、ランサムウェアのサプライチェーン悪用が三大トレンドとして挙げられた。([TechCrunch, 2026-06-07](https://techcrunch.com/2026/06/07/the-worst-hacks-and-breaches-of-2026-so-far/))

---

## CVE / Vulnerability

| CVE ID | 対象 | CVSS | 概要 | 参考 |
|--------|------|------|------|------|
| CVE-2026-49774 | RD Station WP Plugin ≤5.6.0 | **9.9** (Critical) | 低権限ユーザーが`process_filter()`の`eval()`シンクに任意コード注入→RCE。積極悪用確認済み。修正: v5.7.0 | [WPScan, 2026-06-06](https://wpscan.com/vulnerability/CVE-2026-49774) |
| CVE-2026-50589 (OSSN-0099) | OpenStack Ironic 32〜35.0.1 | **5.3** (Medium) | 非認証攻撃者が細工JSONでAPI/JSON-RPCエンドポイントをクラッシュ→DoS(CWE-770)。修正: Ironic 35.0.2 | [oss-security, 2026-06-06](https://security.openstack.org/ossa/OSSN-0099.html) |
| (CVE未採番) | claude-code-action \<v1.0.94 | **7.8** (High, CVSS 4.0) | GitHub App`[bot]`サフィックスを無条件信頼→prompt injection経由で環境変数窃取・下流リポジトリへの悪意あるcommit push。修正: [v1.0.94](https://github.com/anthropics/claude-code-action/releases/tag/v1.0.94) | [THN, 2026-06-06](https://thehackernews.com/2026/06/claude-code-github-action-flaw-let-one.html) |

---

## 国内セキュリティ動向

今日の採用範囲(2026-06-06〜06-08)では新規の国内固有インシデント・JVN情報は確認されませんでした。

---

<details>
<summary>除外済み項目 (採用範囲外・重複)</summary>

- Anthropic DNA letter / pause proposal (2026-06-05以前, 前回収録)
- depthfirst FFmpeg 21 0days CVE-2026-39210〜39218 (2026-06-05以前)
- Miasma worm (2026-06-05以前)
- CISA BOD AI EO (2026-06-05以前)
- Cisco SD-WAN CVE-2026-20245, VS Code 0day, Cisco UCM CVE-2026-20230 (2026-06-04〜05, 前回収録)
- Chrome 149 (2026-06-04, 前回収録)
- HTTP/2 Bomb CVE-2026-49975 (2026-06-03, 前回収録)
- IronWorm npm (2026-06-03, 前回収録)
- SymJack (2026-05-27更新), TrustFall (2026-05-07) — 採用範囲外
- "Comment and Control" blog post (2026-04-15) — 採用範囲外
- Altium Enterprise CVEs (2026-06-05) — 採用範囲外

</details>
