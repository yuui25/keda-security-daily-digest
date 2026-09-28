# KEDA Daily Digest — 2026-09-29 (JST)

> 採用範囲: 公開日 2026-09-27 〜 2026-09-29
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

---

## AI ニュース

- [2026-09-28] **Anthropic が Claude Sonnet 5.5 をリリース** — 出力速度 30% 向上、コスト最大 30% 削減; Terminal-Bench 4.0: 70.6% (Sonnet 5: 10.3% から大幅改善); Opus 5.5 並みのサイバー制限フォールバック機構を初搭載; Cyber Verification Program 同時開始 *(Anthropic / TechCrunch)*
- [2026-09-27] **Anthropic・OpenAI CEO が AI 安全性の独立規制テスト実施を公言** — 「最先端モデルは危険」; Google/OpenAI/Anthropic が SAFA (Standards Authority for Frontier AI) 自主規制体の設立計画を共同発表 *(Washington Times / Forbes)*
- [2026-09-27] **Simon Willison が "2026 in LLMs so far" 基調講演を公開** — WeAreDevelopers World Congress; "lethal trifecta" (エージェントアクセス + ツール実行権限 + 外部入力) がエージェント攻撃の主要概念として定着; 実例付きで解説 *(simonwillison.net / WeAreDevelopers)*
- [2026-09-28] **Noma がエンドポイント AI エージェントセキュリティ機能を拡張** — PC 上のエージェント・MCP・スキルを自動検出; AI-DR (AI Detection & Response) でリアルタイムの Prompt Injection 阻止; エンタープライズ向け AI リスク可視化を強化 *(PR Newswire / Help Net Security)*

---

## セキュリティニュース

- [2026-09-28] **[続報] Citrix NetScaler CVE-2026-88771/88772 — 数週間前から世界規模で野外悪用中と判明** — 攻撃者はウェブシェルを NetScaler GUI ディレクトリに設置する後続攻撃も確認; 即時パッチ適用済みでも侵害痕跡調査を推奨 *(Help Net Security / NCC Group)*
- [2026-09-28] **INC Ransomware が BYOVD を活用した 175 エンドポイント規模の攻撃を実施** — 脆弱なドライバーでセキュリティツールを無効化 → AnyDesk とスケジュールタスクで横移動 → ランサムウェア展開; Check Point が TTP 詳細を公開 *(Check Point Research)*
- [2026-09-28] **[続報] Bitget 仮想通貨窃取額が $387.5M に確定** — 9/24 攻撃・9/25 開示 (当初 $351.6M); 9/28 から Bitcoin 等の出金再開を段階的に開始; 原因調査は継続中 *(CryptoTimes / CoinGabbar)*

---

## 新規 CVE

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-82384 | Apache Roller ≤6.1.5 | CWE-502 / CVSS 4.0: 9.8 | 未認証攻撃者が XML-RPC エンドポイント (XmlRpcServlet, enabledForExtensions=true) に ex:serializable 型ペイロードを送信 → Java デシリアライズが入力をそのまま ObjectInputStream に渡す → 認証前任意コード実行; XML-RPC 無効設定でもサーブレットがマッピング済みのため影響を受ける | [PR #171 / Roller 6.1.6 (2026-09-28)](https://github.com/apache/roller/pull/171) | **CVSS 9.8 / PoC 公開 (GitHub/Sploitus)** / Java XML-RPC デシリアライズ / Blojsom・Pebble 等他 Java ブログプラットフォームの XML-RPC 実装への水平バリアント候補 |
| CVE-2026-82377 | Apache Roller ≤6.1.5 | CWE-862 / CVSS 4.0: 9.9 | 認証済みユーザーが XML-RPC Blogger/MetaWeblog API ハンドラーに任意ブログの entry ID を指定 → 認証チェックは存在するが権限チェック欠落 → 他ウェブログのコンテンツを任意読取・改ざん・削除が可能 | [PR #171 / Roller 6.1.6 (2026-09-28)](https://github.com/apache/roller/pull/171) | CVSS 9.9 / 認証後 Missing Authorization / WordPress XML-RPC・Movable Type 等他ブログ API への水平バリアント候補 |
| CVE-2026-101001 | Netcore NBR200V2 v1.3.241127.071246 | CWE-78 / CVSS 4.0: 10.0 | 未認証攻撃者が Web 管理画面 `/www/cgi-bin/network_tools` の eval() 関数に QUERY_STRING 経由で OS コマンドを注入 → サニタイズなく shell に渡す → 認証前任意コマンド実行 (root 権限); ベンダー対応なし; Netcore NBR100V2 (CVE-2026-101000) にも同クラス | ベンダー未対応 / PoC 公開 | **CVSS 10.0 / PoC 公開 / ベンダー未対応** / SOHO ルーター CGI OS injection / Netcore 他モデルへの水平バリアント候補 |
| CVE-2026-100886 | Seetong T8108/T8108P/T8116/T8232 v4.6.1.4-build202604241011 | CWE-287 / CVSS 4.0: 10.0 | 未認証攻撃者が Debug Service の認証機能をバイパス → 機器フルアクセスが可能; PoC 公開; ベンダー対応なし | ベンダー未対応 / PoC 公開 | **CVSS 10.0 / PoC 公開 / ベンダー未対応** / IoT カメラ Debug Service 認証バイパス / Seetong 他機種および同系 OEM カメラへの水平バリアント候補 |
| CVE-2026-88773 | Citrix NetScaler ADC/Gateway (HTTP/SSL vServer 構成時) | CWE-444 / CVSS 4.0: 9.3 | HTTP 設定有効かつ LB/CS/VPN/Auth の HTTP または SSL 型 vServer を構成している環境で、攻撃者が細工した HTTP リクエストを送信 → HTTP Request Smuggling → バックエンドサーバーへの不正リクエスト到達 → 認可バイパス・セッションハイジャック | [CTX697096 (2026-09-27)](https://support.citrix.com/external/article/CTX697096) | CVSS 9.3 / CVE-2026-88771/88772 と同一パッチバッチ (8件中) / F5 BIG-IP・HAProxy・Nginx 等他 ADC/リバースプロキシの HTTP パーサーへの水平バリアント候補 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|---|---|---|---|---|
| 2026-09-28 | CVE-2026-19033 他 (BIND 9 複数) | ISC BIND 9 複数の脆弱性 — DoS・キャッシュ汚染等 14 CVE を含む; 修正: BIND 9.20.x 以降 | CVSS 最大 8.6 / DNS サービス停止・応答汚染 | [JVNVU (2026-09-28)](https://jvn.jp/vu/) |

---

## Debug

- 巡回ソース数: 30+
- 採用件数: AI=4 / Security=3 / CVE=5 / 国内=1
- 除外理由内訳:
  - 採用窓外 (公開日 < 2026-09-27): 直近 Sep 22–26 digest 掲載済み全項目、Anthropic Claude Sonnet 5.5 ベータ段階記事 (Sep 22), CISA KEV Sep 25 additions (Sep 25 digest 既報)
  - 重複 (直近7日 digest 既報): CVE-2026-88771/88772 (Sep 28 digest), CVE-2026-97163 (Sep 28), CVE-2026-100716/100741 (Sep 28), CVE-2026-100693/GHSA-pmrv-x7gp-2rjw Hugo (Sep 27), CVE-2026-94606/94609 authentik (Sep 27), arXiv 2609.30266/2609.30217 (Sep 27), GitHub Taskflow Agent (Sep 27)
  - 公開日不明・確認不可: 複数の新製品発表記事
- 取得失敗ソース (EGRESS_BLOCKED): cisa.gov, jvndb.jvn.jp, bleepingcomputer.com, securityweek.com, nvd.nist.gov, techcrunch.com, helpnetsecurity.com, securityboulevard.com, prnewswire.com
