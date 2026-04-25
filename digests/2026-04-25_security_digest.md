# セキュリティ日報 2026年04月25日

## 🚨 本日の注目ニュース

### 1. Microsoft Defender ゼロデイ3件 — うち2件は未パッチのまま積極悪用中
- **ソース:** The Hacker News
- **概要:** 4月10日以降、Microsoft Defenderに存在する3件のゼロデイ脆弱性が実際の攻撃で悪用されています。権限昇格とDoSを引き起こすもので、2件はいまだパッチが提供されておらず、影響を受けたシステムは隔離対応が取られています。Defenderというエンドポイント保護製品自体が攻撃対象となっている点が特に深刻です。
- **リンク:** https://thehackernews.com/2026/04/three-microsoft-defender-zero-days.html

### 2. Qilin/Warlock ランサムウェア — BYOVD手法で300以上のEDRを無効化
- **ソース:** The Hacker News
- **概要:** QilinおよびWarlockランサムウェアグループが「脆弱なドライバの持ち込み（BYOVD）」手法を使い、主要セキュリティベンダーほぼ全社の300超のEDRドライバを無効化していることが確認されました。EDRを機能停止させてから本命の攻撃を展開する手口で、既存のエンドポイント保護だけに頼る防御戦略の根本的な見直しを迫る内容です。
- **リンク:** https://thehackernews.com/2026/04/qilin-and-warlock-ransomware-use.html

### 3. Marimo CVE-2026-39987 — CVSS 9.3のRCE、わずか数日で662件の悪用
- **ソース:** The Hacker News
- **概要:** Pythonリアクティブノートブック「Marimo」にCVSS 9.3の認証不要リモートコード実行脆弱性が確認されました。バージョン0.20.4以前が対象で、4月11〜14日の4日間だけで662件の悪用イベントがSysdigにより観測されています。AI/MLツールが攻撃対象として急速に狙われていることを示す事例です。
- **リンク:** https://thehackernews.com/2026/04/marimo-rce-flaw-cve-2026-39987.html

### 4. Adobe Acrobat Reader CVE-2026-34621 — 連邦機関の対応期限は4月27日
- **ソース:** The Hacker News / CISA
- **概要:** CISAが既知悪用脆弱性カタログ（KEV）に追加したAdobe Acrobat ReaderのRCE脆弱性です。悪意あるPDFを開くだけで任意コードが実行される可能性があり、2025年12月から悪用が続いています。米連邦機関には4月27日までの修正適用が義務付けられており、企業環境でも早急な対応が求められます。
- **リンク:** https://thehackernews.com/2026/04/adobe-patches-actively-exploited.html

### 5. LMDeploy CVE-2026-33626 — 開示から13時間以内に悪用確認
- **ソース:** The Hacker News
- **概要:** LLM推論フレームワーク「LMDeploy」のビジョン言語モジュールにSSRF脆弱性が発見され、開示からわずか13時間以内に実際の悪用が確認されました。クラウドのメタデータサービスや内部ネットワークへのアクセスを許す可能性があり、AIインフラを自社で運用している環境は即時確認が必要です。
- **リンク:** https://thehackernews.com/2026/04/lmdeploy-cve-2026-33626-flaw-exploited.html

### 6. CPUID侵害 — CPU-Z/HWMonitorのトロイ化版でSTX RATを配布
- **ソース:** The Hacker News
- **概要:** PC情報ツール「CPU-Z」「HWMonitor」で知られるCPUID社の公式サイトが侵害され、トロイ化されたダウンロードファイルを通じてSTX RATが配布されていました。Kasperskyが150件以上の被害を確認しており、小売・製造・通信など複数業種の組織が影響を受けています。正規サイトからのダウンロードを過信しない姿勢が改めて重要です。
- **リンク:** https://thehackernews.com/2026/04/cpuid-breach-distributes-stx-rat-via.html

### 7. Fortinet FortiClient EMS CVE-2026-35616 — 認証前に権限昇格
- **ソース:** The Hacker News
- **概要:** FortiClient EMSのバージョン7.4.5〜7.4.6に、認証なしでAPIにアクセスできる脆弱性が発見されました（CVSS 9.1）。攻撃者は認証を一切必要とせず権限昇格が可能で、Fortinetを利用している組織は直ちにバージョンを確認し、対象バージョンを使用している場合は迅速なパッチ適用が必要です。
- **リンク:** https://thehackernews.com/2026/04/fortinet-patches-actively-exploited-cve.html

### 8. April Patch Tuesday — SAP・Adobe・Microsoft・Fortinet 横断で重大パッチ
- **ソース:** The Hacker News
- **概要:** 4月のパッチチューズデーでは、SAP・Adobe・Microsoft・Fortinetをまたぐ複数の重大脆弱性が修正されました。上記CVEを含む今月は特に悪用済み脆弱性が多く、通常より速いペースでの適用が推奨されます。パッチ管理の優先度付けにはCISA KEVの最新リストの参照が有効です。
- **リンク:** https://thehackernews.com/2026/04/april-patch-tuesday-fixes-critical.html

---

## 🇯🇵 JVN国内脆弱性情報（本日のピックアップ）

| 製品・ソフトウェア | 脆弱性の種類 | 備考 |
|---|---|---|
| Apache ActiveMQ | MQTTパケット検証不備 [AMQ-9810] | 国際的にも悪用報告あり（CVE-2026-34197） |
| DeepL Chrome拡張機能 | クロスサイトスクリプティング（XSS） | 広く使われているツールのため要注意 |
| MELSEC iQ-Fシリーズ | EtherNet/IPユニットの複数脆弱性 | OT/ICS環境に影響、産業系担当者は要確認 |
| Ziostation2 | パストラバーサル | 医療系システムのため影響範囲に注意 |
| CMS ALAYA | SQLインジェクション | Webサービス運営者は確認推奨 |
| SKYSEA Client View | 不適切なファイルアクセス権設定 | IT資産管理ツール、エンタープライズ環境で広く導入 |
| OpenSSL | TLS 1.3鍵交換グループ選択の問題 | インフラ担当者はバージョン確認を |

---

## 📌 今日のまとめ

今週は「防御ツールそのものを標的にする」攻撃が際立っています。Microsoft DefenderのゼロデイとEDR無効化BYOVDの組み合わせは、従来のエンドポイント防御だけでは不十分であることを強く示しており、ネットワーク分離・ゼロトラスト・ログ監視の多層防御がより一層重要になっています。また、LMDeployやMarimoといったAI/MLツールへの攻撃が加速しており、AIを活用するセキュリティ専門家自身の開発・運用環境も攻撃対象として意識する必要があります。

---
*生成時刻: 12:55 JST　|　モデル: Claude Haiku　|　情報源: The Hacker News / CISA / JVN*
