# KEDA Daily Digest — 2026-06-01 (JST)

> 採用範囲: 公開日 2026-05-30 〜 2026-06-01
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

AI LLM ワークフロービルダー Flowise で CVSS 9.9 の最大深刻度 RCE (CVE-2026-40933) が 5/30 に野外悪用確認。Obsidian Security が公開した PoC は MCP stdio アダプターの安全でないコマンドシリアライゼーションを突き、悪意あるチャットフローをインポートするだけでコンテナルート権限の RCE が成立する。CSV Agent 経由の非認証 RCE (CVE-2026-41264, CVSS 9.8) も同一バージョンで修正対象となり、12,000+ 露出インスタンスへの即時アップグレードが必須。GitLab は 5/27 のパッチで Duo AI ワークフローランナーのアイデンティティなりすまし (CVE-2026-4868, CVSS 8.2) を含む 7 件を修正しており、AI 開発プラットフォーム自体がサプライチェーン攻撃の新たな最前線となった。

---

## AI 関連ニュース

- **[2026-05-30]** [MCP stdio アダプター経由の 1-Click RCE が Flowise で野外悪用開始 — Obsidian Security が PoC を公開し 12,000+ 露出インスタンスが危険に](https://www.obsidiansecurity.com/blog/when-is-stdio-mcp-actually-a-vulnerability) — stdio トランスポートではチャットフロー描画時に設定コマンドが起動するため、悪意あるチャットフローのインポート一発で任意コマンドがサーバー側で実行される；Flowise は本番環境でデータベース・API・クラウドアカウントと結合されることが多くブラストラジウスが広大。修正済み 3.1.0 への即時アップグレードが必須 *(Obsidian Security / BleepingComputer / SecurityWeek)*

- **[2026-05-29/30]** [GitLab が Duo AI ワークフローランナーのアイデンティティなりすまし (CVE-2026-4868, CVSS 8.2) を含む 7 件をパッチ — 認証済みユーザーが他ユーザー ID で Duo AI ワークフローを実行可能](https://gbhackers.com/gitlab-patches-multiple-vulnerabilities-3/) — 影響バージョン: GitLab EE 18.8〜18.10.6 / 18.11〜18.11.3 / 19.0.0；修正版: 19.0.1 / 18.11.4 / 18.10.7。加えて Wiki 経由 DoS (CVE-2026-1402, CVSS 6.5)・GraphQL private プロジェクト非認証列挙 (CVE-2026-6713, CVSS 5.3) も同一リリースで解消 *(GBHackers / GitLab Docs)*

---

## セキュリティ関連ニュース

- **[2026-05-30]** [Flowise CVE-2026-40933 (CVSS 9.9) が野外悪用確認 — 悪意あるチャットフローのインポート一発でコンテナルート RCE、12,000+ 露出インスタンスに即時対応が必要](https://www.bleepingcomputer.com/news/security/max-severity-flowise-rce-vulnerability-now-exploited-in-attacks/) — 4/16 に GHSA-c9gw-hvqq-f33r として公開後、5/30 に Obsidian Security が PoC をリリースしたことで攻撃が急増；連動して CSV Agent 経由の非認証プロンプトインジェクション RCE (CVE-2026-41264, CVSS 9.8, GHSA-3hjv-c53m-58jj) も同日悪用報告。両 CVE とも Flowise 3.1.0 で修正済み *(BleepingComputer / SC Media / SecurityWeek)*

- **[2026-05-27]** [GitLab セキュリティリリース 19.0.1 / 18.11.4 / 18.10.7 — Duo AI・DoS・GraphQL 認可の 7 件を一括修正、自己ホスト型 GitLab EE は即時アップグレード推奨](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-0-1-released/) — 最高深刻度は CVE-2026-4868 (CVSS 8.2, Duo AI アイデンティティなりすまし)；認証済みユーザーが別ユーザー権限で Duo AI ワークフローを実行でき、機密データ漏洩・不正操作に繋がる可能性。研究者 ahacker1 が HackerOne 経由で責任開示 *(GitLab Docs / GBHackers / CyberSecurityNews)*

- **[2026-05-28]** [JINX-0164 が LinkedIn 偽リクルーター経由で暗号通貨企業開発者を標的 — AUDIOFIX macOS インフォスティーラー + MINIRAT Go バックドアを展開](https://thehackernews.com/2026/05/jinx-0164-targets-cryptocurrency-firms.html) *(範囲拡大: 直近7日)* — Wiz が追跡する金銭目的脅威クラスター；偽技術面接で「音声エラー修正」ダウンロードを誘導 → AUDIOFIX が SSH キー・ブラウザ認証情報・暗号ウォレット拡張機能・クリップボードを収集。4/7 に @velora-dex/sdk npm v4.9.1 をトロイ化し MINIRAT（Go 製 RAT、shell実行・ファイル操作・C2 AES 通信）をサプライチェーン経由で配布 *(The Hacker News / Wiz Blog / Infosecurity Magazine)*

- **[2026-05-28]** [Operation XENOFISCAL: パキスタン系 SideCopy が XenoRAT 1.8.7 でアフガニスタン財務省と全 34 州財務局を標的に — 完全な財務・税務ネットワーク掌握を狙う長期諜報キャンペーン](https://www.seqrite.com/blog/operation-xenofiscal-sidecopy-deploying-persistent-xenorat-targeting-the-mof-afghanistan/) *(範囲拡大: 直近7日)* — Pashto 語ファイル名付き ZIP → LNK → mshta.exe → リモート HTA の多段チェーン；XenoRAT はキーロギング・スクリーンキャプチャ・ウェブカム監視・SOCKS5 トンネリングを提供、C2 通信は AES+RTL 圧縮。SideCopy / Transparent Tribe (APT36) に中高度帰属 *(Seqrite / GBHackers / CyberPress)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-05-30 以降 (主要項目) / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-40933 / [GHSA-c9gw-hvqq-f33r](https://github.com/advisories/GHSA-c9gw-hvqq-f33r) | Flowise (npm) ≤ 3.0.13 | CWE-77 / **9.9** | 認証済みユーザーが MCP stdio アダプター設定に任意コマンドを埋め込んだ悪意あるチャットフローをインポート → stdio トランスポート起動時にサーバー側でコマンドが OS 権限で実行 → **コンテナルート RCE** | [Flowise 3.1.0](https://github.com/FlowiseAI/Flowise/releases) (flag allowlist #5741 #5943) | **野外悪用中 (2026-05-30)** / CVSS 9.9 / MCP プロトコル悪用の初実例 / Dify・Langflow 等類似実装へのバリアントハント推奨 |
| CVE-2026-41264 / [GHSA-3hjv-c53m-58jj](https://github.com/advisories/GHSA-3hjv-c53m-58jj) | Flowise (npm) ≤ 3.0.13 | CWE-1336 / **9.8** | 非認証攻撃者が CSV Agent ノードを持つチャットフローにプロンプトインジェクションを送信 → LLM が悪意ある Python コードを生成 → Flowise サーバー側で任意コード実行 → **非認証 RCE** | [Flowise 3.1.0](https://github.com/FlowiseAI/Flowise/releases) | **野外悪用中 (2026-05-30)** / CVSS 9.8 / 非認証・LLM 応答経由という新型バグクラス / CSV/Code Interpreter 機能持つ全 LLM フレームワークに水平伝播可能性 |
| CVE-2026-4868 | GitLab EE 18.8〜18.10.6 / 18.11〜18.11.3 / 19.0.0 | CWE-284 / **8.2** | 認証済みユーザーが特定の Duo AI ワークフロー API を呼び出し → サーバー側のユーザーアイデンティティ解決ロジックが誤ったユーザーの権限で実行 → 他ユーザー ID でワークフロー実行・機密データ参照 | [GitLab 19.0.1 / 18.11.4 / 18.10.7](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-0-1-released/) | HIGH / AI ワークフローランナーの ID なりすまし / EE 限定 / GitLab SaaS はアップデート済み・自己ホスト型は即時対応 |
| CVE-2026-1402 | GitLab CE/EE ≥ 17.1, < 18.10.7 | CWE-400 / **6.5** | 認証済みユーザーが特定の Wiki リクエストを繰り返し送信 → サーバー側で過剰なリソース割り当てが発生 → 全ユーザーへのサービス拒否 | [GitLab 19.0.1 / 18.11.4 / 18.10.7](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-0-1-released/) | MEDIUM / CE/EE 両方に影響 / 17.1 以降の広範なバージョンに適用 |
| CVE-2026-6713 | GitLab CE/EE (パッチ前) | CWE-200 / **5.3** | **非認証** の攻撃者が GraphQL WorkItem API に細工したクエリを送信 → 認可チェック不備でプライベートプロジェクトの存在・メタデータを列挙可能 → 偵察起点として悪用 | [GitLab 19.0.1 / 18.11.4 / 18.10.7](https://docs.gitlab.com/releases/patches/patch-release-gitlab-19-0-1-released/) | 非認証偵察 / GraphQL 認可漏れパターン / 自社 GraphQL API の WorkItem / MR / Issue エンドポイントのバリアントハント推奨 |

---

## 国内脆弱性・インシデント情報

> 直近2日間に該当する新規国内脆弱性・インシデント情報は確認できませんでした。

*備考: JPCERT/CC・JVN への直接アクセスが HTTP 403 により不可。上記 Flowise CVE・GitLab CVE はセルフホスト型 GitLab・Flowise インスタンスを運用する国内組織に直接影響する。*

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 30+（WebSearch 20+ クエリ、WebFetch 15+ 試行）
- 採用件数: AI=2 / Security=4 (うち fallback 2 件) / CVE=5 / 国内=0
- fallback 適用: セキュリティ欄の JINX-0164 (2026-05-28) と SideCopy XENOFISCAL (2026-05-28) は 3日ウィンドウ外だが直近7日以内かつ excluded_set 未収録のため範囲拡大採用
- 除外理由内訳:
  - 古すぎ (< 2026-05-30): PraisonAI CVE-2026-44338 (初報 2026-05-11) / Flowise CVE-2026-40933 初公開 (2026-04-16) → 5/30 悪用報道を新規採用 / GitLab patch 2026-05-27 → 5/29-30 報道を新規採用 / Instructure Canvas 340M (2026-05-05 初報) / 7-Eleven breach (2026-05-28 既収録)
  - 重複 (excluded_set 直近7日): CVE-2026-45697 Formie (05-31) / CVE-2026-0257 PAN-OS KEV (05-31) / CVE-2026-39987 Marimo (05-31) / Anthropic $65B (05-30) / Gogs 0-day KEV (05-30) / Charter breach (05-30) / Carnival breach (05-30) / Chrome 148 (05-30) / Claude Opus 4.8 (05-29) / Google AI Threat Defense (05-29) / Oracle CSPU (05-29) / CVE-2026-35616 FortiClient (05-29) / CVE-2026-8398 DAEMON Tools (05-29) / Yamcs CVEs (05-29) / Malware-Slop npm (05-28) / SymJack (05-28) / Gitea CVE-2026-27771 (05-28) / KnowledgeDeliver CVE-2026-5426 (05-27) / SharePoint CVE-2026-45659 (05-27) / MuddyWater DLL (05-27) / CVE-2026-48172 LiteSpeed (05-26) / Lazarus RemotePE (05-26) / CVE-2026-47138 Parse Server (05-26) / Glassworm takedown (05-25)
  - 日付不明/確認不可: 各種 roundup 記事 / Flowise CVE-2026-41268 (第3バリアント、具体的悪用日不明)
- 取得失敗ソース: BleepingComputer (403), SecurityWeek (403), The Hacker News (403), CISA.gov (403), NVD (403), SC World (403), Seqrite blog (403), GBHackers (200 but scraping limited), Infosecurity Magazine (403), CyberSecurityNews (403)

</details>
