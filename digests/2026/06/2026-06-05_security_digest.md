# KEDA Daily Digest — 2026-06-05 (JST)

> 採用範囲: 公開日 2026-06-03 〜 2026-06-05
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

トロント大 CleverHans Lab が LLM エージェント駆動の適応型コンピュータウイルス (arXiv 2606.03811) を公開、オープン重みモデルだけで模擬企業網の 73% を1週間以内に無人侵害し自律マルウェアの現実性を証明した。HTTP/2 Bomb (CVE-2026-49975) は単一の家庭回線から nginx/Apache/IIS/Envoy/Pingora を数秒で DoS できる複合技術として 880,000+ サイトに影響しており、Apache/IIS 等の主要サーバーが依然パッチ未適用。CVE 面では Magento 拡張 Mirasvit CVE-2026-45247 (CVSS 9.8) が PHP オブジェクトインジェクション経由の非認証 RCE として野外で積極悪用され CISA KEV 入り、連邦機関の修正期限は **本日 (2026-06-06)**。

---

## AI 関連ニュース

- **[2026-06-03]** [Google Gemini Android 音声 AI が WhatsApp・Slack・SMS 通知経由の間接プロンプトインジェクションでハイジャック可能 — SafeBreach が「二重幻想テクニック」の全技術詳細を公開](https://thehackernews.com/2026/06/whatsapp-slack-notifications-could.html) — 攻撃者が中国語の隠しコマンド「窓を開けますか？」と英語の無害な質問を連続注入し、ユーザーの "Yes" をバックエンドが悪意ある命令として実行；スマートホーム制御・Zoom 強制起動・長期記憶汚染が可能。Google は 2025-11-14 にコンテンツ分類器を更新して緩和確認済み *(The Hacker News / SecurityWeek / Tom's Guide)*

- **[2026-06-03]** [Anthropic が Claude Partner Network に Services Track (3段階ティア) と Partner Hub ポータルを追加 — 40,000 社以上が申請・10,000 名のクロード認定を取得](https://www.anthropic.com/news/services-track-partner-hub) — Select (10名認定・2顧客)・Preferred (100名・15顧客)・Global Premier (1,000名・100顧客・3地域以上) の実績ベースの階層構造；エンタープライズ AI 導入の SI パートナーエコシステムを正式化 *(Anthropic)*

- **[2026-06-03]** [Toronto CleverHans Lab が AI エージェント駆動の適応型コンピュータウイルスを実証 (arXiv:2606.03811) — オープン重み LLM が リアルタイム advisory 摂取で未知の脆弱性を自律的に利用し模擬企業網の 73% を1週間以内・人手介在なしで侵害](https://arxiv.org/abs/2606.03811) — Vector Institute・Cambridge・ServiceNow Research との共同研究；特定の CVE を修正してもウイルスが別経路に適応するため従来のパッチ対応だけでは防御困難と指摘 *(Fortune / Winbuzzer / University of Toronto)*

- **[2026-06-03]** [OpenAI が Codex をロール別プラグイン・Annotations・Sites (共有インタラクティブ Web アプリ) に拡張 — 「Codex for every role」として開発職以外の職種・ツールへのコーディングエージェント適用を推進](https://openai.com/news/) — Annotations 機能でドキュメント・スプレッドシート・スライドのインプレース精製が可能；Sites は AWS GovCloud (US-West) 含む複数クラウドから利用可能 *(OpenAI)*

- **[2026-06-04]** [OpenAI が GPT-Rosalind を更新 — ライフサイエンス研究向けエージェントコーディング強化・ゲノミクス/創薬性能向上・バイオインフォマティクスプラグイン追加で Rosalind Biodefense プログラムの実用性を拡大](https://openai.com/news/) — 生物防衛・パンデミック対策向け特別アクセスモデルとして設立されたプログラムの第一次モデルアップデート *(OpenAI)*

- **[2026-06-04]** [Apple WWDC 2026 (6/8-12 開幕) プレビュー: Siri AI を Google Gemini 基盤で大規模刷新・iOS 27 同梱 — Private Cloud Compute を謳うも Gemini クラウドインフラでのデータ処理範囲と保持ポリシーが未公開でプライバシーリスクとして指摘](https://techcrunch.com/2026/06/04/what-to-expect-from-wwdc-2026-siris-highly-anticipated-revamp-and-apple-intelligence-updates/) — Apple は「ユーザーデータは保存・ログ記録されず広告にも使われない」と主張するが Gemini 側のデータ取り扱い契約の公開は限定的；新 Siri は会話型 + 画面認識 + スマートホーム連携を統合 *(TechCrunch / MacWorld)*

- **[2026-06-03/04]** [Nightmare Eclipse 紛争波及: 第二研究者が「Secure Boot を完全バイパスして BitLocker を解除・機密 VM を侵害可能な未発表ゼロデイ」を6月中に公開予告 — Microsoft が6/4 に声明更新し研究者コミュニティへの法的措置を否定・協力姿勢を再確認](https://www.theregister.com/security/2026/06/03/another-bug-hunter-leaks-microsoft-exploits-in-defiance-of-companys-handling-of-vulnerability-disclosures/5250590) — Nightmare Eclipse ブログが「最近の出来事を受けて別の研究者が接触してきた」と予告；開示倫理論争が脆弱性研究コミュニティ全体に波及 *(The Register / The Record)*

---

## セキュリティ関連ニュース

- **[2026-06-03]** [HTTP/2 Bomb (CVE-2026-49975) 公開: 単一の 100 Mbps 家庭用回線から nginx/Apache HTTPD/Microsoft IIS/Envoy/Cloudflare Pingora を 10 秒以内で DoS 可能な HPACK 圧縮爆弾 + Slowloris 複合技術が 880,000+ サイトに影響](https://www.securityweek.com/http-2-bomb-exploit-knocks-web-servers-offline-in-seconds/) — Envoy で 5,700:1・Apache で 4,000:1 の増幅比；nginx は 1.29.8 でパッチ済み、Apache mod_http2 にも修正が存在するが未バンドル状態；IIS/Envoy/Pingora は未修正 *(SecurityWeek / The Hacker News / oss-security)*

- **[2026-06-04]** [IronWorm npm サプライチェーン攻撃: 「asteroiddao」アカウント起点に 36+ パッケージを侵害、Rust ベースの eBPF ルートキット + Tor C2 + 自己増殖機能を持ちプリインストールフックで Anthropic/OpenAI API キー・AWS/GCP/Vault 認証情報・Exodus 暗号ウォレットを標的](https://www.bleepingcomputer.com/news/security/new-ironworm-malware-hits-36-packages-in-npm-supply-chain-attack/) — npm Trusted Publishing ワークフローの OIDC トークンを悪用して被害者所有パッケージに自己増殖；Web3 開発者と CI 環境が主な標的 *(BleepingComputer / SlowMist / Aikido Security)*

- **[2026-06-03]** [Microsoft Exchange Online グローバル障害 EX1331830 — 北米・APAC・欧州で大規模なメール送受信失敗・1時間以上の遅延、2日以上継続し原因特定に難航](https://www.techtimes.com/articles/317696/20260603/exchange-online-outage-halts-email-three-continents-ex1331830-still-unresolved.htm) — エラー「リソースフォレストの同時接続数超過」と SMTP セッション強制切断が並行発生；Exchange Online が AD インフラで受信者アドレスを解決する際の障害と推定されるが公式原因は未公表 *(TechTimes / BleepingComputer)*

- **[2026-06-03]** [CISA が Mirasvit Full Page Cache Warmer CVE-2026-45247 (CVSS 9.8) を KEV に追加 — ゲーム・ビジネスサイトを中心に US/UK/仏/豪で非認証 PHP オブジェクトインジェクション RCE が積極悪用中、連邦修正期限 2026-06-06](https://thehackernews.com/2026/06/cisa-adds-exploited-magento-rce-flaw.html) — CacheWarmer Cookie に base64 エンコードされたシリアライズ PHP ガジェットチェーンを埋め込む攻撃；Imperva が大量試行を観測 *(The Hacker News / CISA / Imperva)*

- **[2026-06-04]** [Microsoft が Secure Boot 2011 証明書の最終更新期限 (2026-06-26) に向け警告 — 6/9 Patch Tuesday で dbx 更新を含む予定、期限後は新規 boot セキュリティ更新・マルウェアブラックリストを受け取れなくなりブートキット攻撃に永続的に露出](https://zecurit.com/endpoint-management/patch-tuesday/) — dbx 更新による起動失敗率は組織の 2〜5% と見積もられるため事前テストが必須；セキュリティ研究者が BitLocker バイパスの悪用連鎖として dbx の脆弱性を利用している実例もあり *(Zecurit / WindowsLatest / PCWorld)*

- **[2026-06-03]** [OpenStack Ironic に CVE-2026-48681: 細工した ISO 画像でディレクトリトラバーサル → Conductor ディスク上のファイル上書き / デプロイ対象ディスクへの任意書き込み — Metal3.io セキュリティチームが発見し OSSA-2026-018 として公開](https://security.openstack.org/ossa/OSSA-2026-018.html) — configdrive・仮想メディアブートインターフェース・anaconda デプロイインターフェースの使用ユーザーが影響を受ける；v35.0.2 以降で修正 *(OpenStack Security / OSSA)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-06-03 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-45247 | Mirasvit Full Page Cache Warmer (Magento 拡張) < 1.11.12 | CWE-502 / **9.8** | 非認証攻撃者が `CacheWarmer` Cookie に base64 + シリアライズ PHP オブジェクトを埋め込む → PHPオブジェクトデシリアライズ時に PHP ガジェットチェーンが起動 → Magento サーバーでのルートレベル RCE | [Mirasvit v1.11.12](https://marketplace.magento.com/mirasvit-module-full-page-cache-warmer.html) (commit 不明) | **KEV ✓ (2026-06-03 追加)** / CVSS 9.8 / 修正期限 2026-06-06 / PHP デシリアライズ RCE は Craft CMS・PrestaShop 等 PHP EC 全般へのバリアントハント推奨 |
| CVE-2026-49975 | Apache HTTPD / nginx (< 1.29.8) / Microsoft IIS / Envoy / Cloudflare Pingora (HTTP/2 有効環境) | CWE-400 / 未発表 | リモート攻撃者が単一 TCP コネクションで HPACK 圧縮テーブルを 5,700:1 で増幅させながら Slowloris 的フロー制御停止を維持 → サーバーがメモリを解放できず 32 GB を約 10 秒で枯渇 → **リモート DoS** | [nginx 1.29.8](https://nginx.org/en/CHANGES) / [Apache mod_http2 独立パッケージ](https://seclists.org/oss-sec/2026/q2/790) | 2026-06-03 公開 / nginx のみ修正済み / 880k+ 公開サイトへの即時影響 / HTTP/2 実装の HPACK 圧縮制限欠落パターン：Envoy・Cloudflare Pingora・Caddy 等への水平バリアントハント推奨 |
| CVE-2026-48681 | OpenStack Ironic ≥17.0.0 <26.1.7 / ≥27.0.0 <29.0.6 / ≥30.0.0 <32.0.2 / ≥33.0.0 <35.0.2 | CWE-22 / **5.9** | configdrive・仮想メディア・anaconda デプロイ権限を持つユーザーが細工した ISO イメージを提供 → Ironic Conductor がパストラバーサルをサニタイズせず ISO 内容を Conductor ディスクまたはターゲットディスクに書き込み → Conductor 上の任意ファイル上書き | [OSSA-2026-018](https://security.openstack.org/ossa/OSSA-2026-018.html) (commit 不明) | 2026-06-04 公開 / クラウドインフラのベアメタルプロビジョニング層 / Metal3.io 使用 Kubernetes on Bare Metal 環境での横断確認を推奨 |
| CVE-2026-41858 | BOSH windows-utilities-release < v0.23.0 (Cloud Foundry Windows 環境) | CWE-338 / **7.5** | `Get-RandomPassword` 関数がクロックシードの予測可能 PRNG でパスワードを生成 → VM 起動時刻を推定できるネットワーク攻撃者が候補リストを絞り込み → Windows Administrator パスワードを回復してハードニング制御を突破 | [windows-utilities-release v0.23.0](https://github.com/cloudfoundry/windows-utilities-release/releases/tag/v0.23.0) | 2026-06-04 公開 / Cloud Foundry PaaS 基盤の Windows 環境 / 同様の clock-seeded PRNG パターンは他 BOSH・Terraform プロバイダーへのバリアントハント推奨 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|

> 直近2日間に該当する新規国内脆弱性・インシデント情報は確認できませんでした。

*備考: JVN・JPCERT へのフェッチが引き続き 403 のため WebSearch 経由で確認。2026-06-03〜05 の国内向け JVN 新規アドバイザリは確認できず。上記 IronWorm・HTTP/2 Bomb・Mirasvit CVE-2026-45247 は国内の npm 開発者・EC サイト・Azure/OpenStack 運用組織にも直接影響する。*

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 35 ソース (The Hacker News, SecurityWeek, BleepingComputer, The Register, Fortune, TechCrunch, Anthropic, OpenAI, CISA, arXiv, SlowMist, Aikido Security, Winbuzzer, TechTimes, MacWorld, Zecurit, PCWorld, WindowsLatest, cyberinsider, openstack.org security, oss-security ML, GBHackers, Cryptotimes, SC Media, CyberSecurityNews 他)
- 採用件数: AI=7 / Security=6 / CVE=4 / 国内=0
- 除外理由内訳:
  - 採用窓外 (< 2026-06-03): CVE-2026-42849 authentik XSS CVSS 9.3 (06-02公開) / CVE-2026-27944 Nginx UI 非認証バックアップ+鍵開示 CVSS 9.8 (2026-03-05公開) / EU AI Act Digital Omnibus 仮合意 (05-07) / Anthropic Project Glasswing 150組織拡大 (06-02) / MongoBleed CVE-2025-14847 KEV (2025-12-29) / CVE-2026-3055 Citrix NetScaler SAML IDP (03-23) / CISA KEV 追加分 06-01・06-02 分 (CVE-2024-21182・CVE-2025-48595・CVE-2022-0492) は前日 digest 採用済み
  - 重複 (excluded_set 直近7日): OWASP GenAI Security Summit (06-04 digest 採用) / Anthropic MITRE ATT&CK report (06-04 digest) / Samsung Exynos June SA (06-04 digest) / WeedHack Minecraft (06-04 digest) / DriveSurge IAB (06-04 digest) / Trump AI EO (06-04 digest) / Sophos Claude Opus 4.5 EDR evasion (06-04 digest) / Microsoft Exchange outage補足 (06-03 digest 内でも議論) / Android June 2026 CVE-2025-48595 (06-03 digest) / GitHub Copilot Project Polaris (06-03 digest) / Dragon Weave Azure C2 (06-03 digest) / OpenAI TAC passkey (06-03 digest) / Rosalind Biodefense 初発表 (06-03 digest)
  - 日付不明/確認不可: CVE-2026-49448 authentik SourceStage bypass (公開日不明、403 エラー) / arXiv 2605.17634 "AI Agents May Always Fall for Prompt Injections" (05-17 arXiv 投稿、June 3-5 ニュース記事として確認困難)
- 取得失敗ソース (HTTP 403): thehackernews.com 個別記事 / bleepingcomputer.com 個別記事 / theregister.com 個別記事 / anthropic.com/news / openai.com/news / jvn.jp / cisa.gov 個別ページ / security.openstack.org / techcrunch.com 個別記事 / cryptotimes.io / Mirasvit marketplace — WebSearch スニペット・複数独立記事で内容と日付を補完
- 備考: CVE-2026-49975 の正式 CVSS は未発表のため「未発表」と記載。CVE-2026-41858 は Cloud Foundry BOSH 環境限定の実用的影響は限定的だが、PRNG 設計欠陥のバリアントハント価値のため採用。Toronto AI worm (arXiv 2606.03811) は arXiv 提出 2026-06-02 だが Fortune/Winbuzzer 等のニュース記事が 2026-06-03 付けで複数確認されたため採用。

</details>
