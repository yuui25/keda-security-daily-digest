# KEDA Daily Digest — 2026-09-16 (JST)

> 採用範囲: 公開日 2026-09-14 〜 2026-09-16
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

---

## AI 関連ニュース

- [2026-09-15] **Google が内部 IDE「Antigravity」経由で全エンジニアに Claude Opus 5 アクセスを開放** — 社内開発ツールを通じて Anthropic モデルを標準供与；自社 Gemini と並行して外部最前線モデルをエンジニアリング基盤に組み込む異例の二重戦略 *(Business Insider / Techmeme)*
- [2026-09-15] **Sam Altman が Fortune インタビューで OpenAI の IPO 窓を 2027 年以降に修正** — 「AI 安全に関するすべてのことを考えると、今 IPO するのは ill-advised」と発言；政府規制・安全評価プロセスの進捗待ち *(Fortune)*
- [2026-09-15] **EU AI Act GPAI：10²⁵ FLOP 超の基盤モデルプロバイダーが初の「システミックリスク評価」を EU AI Office に提出（第一回期限遵守）** — OpenAI・Google・Anthropic・Mistral 等が評価レポートを提出；義務不履行は全世界売上最大 3% の制裁金 *(EU AI Office / Legiscope)*
- [2026-09-14] **[続報] Apple Platform 27 リリース — iOS 27・macOS Golden Gate・watchOS 27 等 6 OS を一括公開；全プラットフォーム合計 261 件の CVE を修正（Apple 史上最多単一更新）** — AI・Siri 刷新の裏側で過去最大規模のセキュリティパッチを同梱；カーネル情報漏えい・IPSec 認証バイパス・APFS 権限昇格を含む重大修正多数 *(Neowin / 9to5Mac)*

---

## セキュリティ関連ニュース

- [2026-09-14] **CVE-2026-76461 (Cisco Secure Email Gateway) が CISA KEV に即日登録 — 未認証攻撃者が細工メールを送信するだけで root RCE；連邦機関に 9/17 期限でパッチ適用を指示** — SQL injection in AsyncOS メール解析ロジックによる完全なリモート侵害；Cisco は「野外での積極的悪用を確認」と明記 *(Cisco PSIRT / CISA KEV)*
- [2026-09-14] **[続報] Apple iOS 27 / macOS Golden Gate セキュリティ詳報 — iOS 27 単体で 122 件の CVE を修正；Kernel memory disclosure・APFS persistent account read・Telephony IPSec 認証バイパスによるトラフィック傍受等の重大フローを含む** — iPhone 11 以降が対象；ゼロデイ悪用の報告はないが攻撃チェーン構築に直結するプリミティブが多数 *(Neowin / 9to5Mac / Apple セキュリティリリースノート)*

---

## CVE / 脆弱性情報

| CVE ID | 製品・バージョン | CWE / CVSS | 概要 | 対応 | 備考 |
|--------|----------------|-----------|------|------|------|
| CVE-2026-76461 | Cisco Secure Email Gateway (AsyncOS ≤15.5 / 16.0 / 16.5) | CWE-89 / CVSS 9.8 | 未認証攻撃者が細工メールに SQL 文を挿入 → AsyncOS メール解析ロジックが入力を無検証で実行 → root 権限で任意 OS コマンドを実行 | [AsyncOS 15.5.5-0141+](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-esa-inj-2bLVGmhX) にアップグレード | **KEV 登録済み (2026-09-14) / 野外悪用中 / 連邦機関 Sep 17 期限** |
| CVE-2026-82429 | Apache Storm 3.0.0 (setuid-root worker-launcher) | CWE-367 / CVSS 7.8 | ローカルのトポロジーユーザーが FTS ウォーク後・lchown/chmod 実行前の窓にシンボリックリンクを置換 (TOCTOU) → root 権限でホスト上の任意ファイルのオーナー変更・モード変更 → LPE | [Storm 3.1.0](https://github.com/apache/storm/releases) | High / setuid binary TOCTOU / Yarn・HDFS 同類 launcher への水平バリアント候補 |
| CVE-2026-82430 | Apache Storm 3.0.0 (container Worker Launcher) | CWE-367 / High | コンテナワーカー起動時にオーナーシップ変更後・コマンドファイル読取前の窓でテナントがコマンドファイルをシンボリックリンクに置換 → launcher が O_NOFOLLOW なしで開き実行 → root 権限で任意コンテナコマンドを実行 → LPE | [Storm 3.1.0](https://github.com/apache/storm/releases) | High / コンテナ環境 LPE |
| CVE-2026-82428 | Apache Storm 3.0.0 (Client) | CWE-345 / CVSS 8.8 | Maven 座標のみから決定論的に導出された blob キーで依存 jar をアップロード → キーが既存の場合は無検証で再利用 → 別テナントのコードが他テナントの依存として実行 → クロステナントコード実行 | [Storm 3.1.0](https://github.com/apache/storm/releases) | CVSS 8.8 / マルチテナントクラスタで影響大 |
| CVE-2026-82426 | Apache Storm 3.0.0 (Nimbus デーモン) | CWE-22 / High | Nimbus がアップロード検証なしでユーザー指定の jar パスを開く → Kerberos keytab・Thrift/UI TLS 秘密鍵・storm.yaml (Zookeeper 認証ペイロード) 等の機密ファイルを読み取り | [Storm 3.1.0](https://github.com/apache/storm/releases) | High / 機密鍵類の窃取直結 |
| CVE-2026-43689 | Apple iOS 27 未満 (iPhone 11 以降) | CWE-200 / 未公開 | 悪意ある NFS サーバーに接続すると iOS カーネルのメモリ内容が開示される | [iOS 27 (2026-09-14)](https://support.apple.com/en-us/149034) | Kernel 情報漏えい / iOS 27 一括更新で修正済み |
| CVE-2026-65329 | Apple iOS 27 未満 (iPhone) | CWE-300 / 未公開 | 特権的ネットワーク位置の攻撃者が IPSec 認証をバイパスし Telephony 通信を傍受 | [iOS 27 (2026-09-14)](https://support.apple.com/en-us/149034) | ネットワーク傍受 / Android・VPN ライブラリへの水平調査推奨 |

---

## 国内脆弱性・インシデント情報

> 直近2日間に該当する新規ニュースは確認できませんでした。

---

## 取得状況（デバッグ）

- 巡回ソース数: 25+
- 採用件数: AI=4 / Security=2 / CVE=7（7項目）/ 国内=0
- 取得失敗ソース: thehackernews.com, bleepingcomputer.com, securityweek.com, jvn.jp, jpcert.or.jp, nvd.nist.gov, cve.org, senserva.com, vulners.com, app.opencve.io, cvebrief.com, xloggs.com, securityonline.info, cvemon.intruder.io, gbhackers.com, cybersecuritynews.com, support.apple.com, cyberpress.org, radar.offseq.com
