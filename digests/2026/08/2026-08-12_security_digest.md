# KEDA Daily Digest — 2026-08-12 (JST)

> 採用範囲: 公開日 2026-08-10 〜 2026-08-12
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

8月11日の Microsoft Patch Tuesday が約400件の CVE を公開し、中でも Windows afd.sys の UAF ゼロデイ CVE-2026-68820 が北朝鮮 Lazarus Group の Operation Dream Job で悪用済みであり、FudModule v3.1 ルートキットによる欧州・インド航空宇宙・防衛業界への標的型攻撃が確認されたことが今週最大の注目点。同日に SAP も CVSS 10.0 の Commerce Cloud 認可欠如 (CVE-2026-58231) を含む4件のクリティカルを修正。AI 面では OpenAI が "offense-grade" の GPT-5.6-Cyber を Daybreak Red として限定公開し、北朝鮮 Kimsuky が攻撃サーバー上でオフライン LLM ラボ (Ollama/GPT4All/RAG) を運用する初の国家支援 APT 自己ホスト LLM 事例も韓国 Genians が公表した。

---

## AI 関連ニュース

- **[2026-08-11]** [OpenAI、"offense-grade" 特化型 GPT-5.6-Cyber を Daybreak Red として限定公開 — Chrome V8 heap sandbox escape (CVE-2026-15903) を事前発見・報告済み、標準 Sol 比で高度サイバータスク完了率 95% vs 1.5%](https://openai.com/index/expanding-daybreak-as-the-cyber-defense-window-narrows/) — Daybreak Blue (守備側・一般モデル) と Daybreak Red (GPT-5.6-Cyber、攻撃的セキュリティ研究用) の2段階アクセス体系を整備。GPT-5.6-Cyber は開発中に Chrome V8 の heap sandbox escape 脆弱性 2 件をチェーンする未知の欠陥を特定、Google が CVE-2026-15903 として 7 月中旬にパッチ済み。Accenture・IBM・CrowdStrike・Cisco・Sophos・Cloudflare 等がパートナーとして参加 *(OpenAI / Forbes / VentureBeat 2026-08-11)*

- **[2026-08-10]** [北朝鮮 Kimsuky が攻撃サーバー上に自前オフライン LLM ラボを構築 — Ollama/GPT4All/RAG + Cursor + Whisper でクラウド非依存の AI 支援攻撃インフラを確立、国家支援 APT 初の自己ホスト LLM 事例](https://thehackernews.com/2026/08/kimsuky-builds-offline-ai-stack-that.html) — 韓国 Genians が初報。盗んだ文書への RAG 適用・盗んだ音声の Whisper 文字起こし・C#/.NET マルウェア開発への AI コーディングアシスタント統合の3用途を確認。仮想資産保有者や金融機関向けスピアフィッシングに AI 生成文書を使用した証拠も発見 *(TechTimes / The Hacker News / The Block 2026-08-10)*

- **[2026-08-10]** [Anthropic が Macquarie Asset Management・GIC と米国 AI データセンター専用 JV「Theseus Infrastructure」を設立 — グリッドアップグレード費用全額を Anthropic が負担、長期契約で専用インフラを確保](https://www.bloomberg.com/news/articles/2026-08-10/anthropic-macquarie-and-gic-form-venture-for-ai-data-centers) — Macquarie と GIC が株式の大部分を保有・資金調達し、Anthropic に長期リース契約で施設を提供する構造。米国内の初期フォーカスで容量確保を加速 *(Bloomberg / Yahoo Finance / HPCwire 2026-08-10)*

- **[2026-08-11]** [米下院民主党が OpenAI・Anthropic に AI ハッキング事案の透明性を要求 — 上院情報委の機密報告要求 (8/10) とは別個に、下院議員グループが「国家安全保障上の深刻な懸念」として経緯の書面説明を求める書簡を送付](https://thehill.com/policy/technology/6022646-openai-anthropic-cybersecurity-incidents/) — 上院側は OpenAI・Anthropic・Google DeepMind の 3 社に 60 日以内の機密報告書を要求。下院側は公開形式での情報開示を別途要求しており、議会からの圧力が両院で同時進行する構図 *(The Hill 2026-08-11)*

---

## セキュリティ関連ニュース

- **[2026-08-11]** [Microsoft 8月 Patch Tuesday — 約400件の CVE と3件のゼロデイ: CVE-2026-68820 (Windows afd.sys UAF、Lazarus 実悪用済み)・CVE-2026-62832 (Windows User Profile Service EoP、公開済み)・CVE-2026-72971 (Container Isolation FS Filter Driver 改ざん、公開済み) を含む](https://www.securityweek.com/august-2026-patch-tuesday-microsoft-fixes-421-cves-one-exploited-zero-day/) — SharePoint デシリアライズ RCE (CVE-2026-65665) は 7 月 KEV 登録済み CVE-2026-55040 JWT バイパスとチェーン。HPC Pack に未認証 RCE (CVE-2026-59124 CVSS 9.8) も含む。Windows 236 件・Office 98 件・SharePoint 30 件・Azure 17 件・Exchange 7 件等 *(SecurityWeek / Tenable / ZDI 2026-08-11)*

- **[2026-08-11]** [Lazarus Group (Operation Dream Job) が CVE-2026-68820 を悪用し欧州・インドの航空宇宙・防衛産業を標的 — Check Point が FudModule v3.1 ルートキットと偽求人メールのチェーン攻撃を詳細分析](https://blog.checkpoint.com/research/state-sponsored-hackers-use-fake-job-offers-to-deliver-new-zero-day-exploit) — FudModule v3.1 は Windows コード整合性検証 (WHQL Driver) を無効化する新能力を追加。Check Point が 7/28 に Microsoft へ報告、Microsoft は 8/5 に CVE を割り当て 8/11 Patch Tuesday でパッチ適用。偽求人メールは採用面接を装い悪意あるペイロードを起動 *(Check Point Research 2026-08-11)*

- **[2026-08-11]** [SAP 8月セキュリティパッチデー — 28 件の新規セキュリティノート・4 件のクリティカル: CVE-2026-58231 (SAP Commerce Cloud CVSS 10.0) を筆頭に製造 OT 系 MII の CVSS 9.9 コードインジェクション (CVE-2026-44772) を含む](https://support.sap.com/en/my-support/knowledge-base/security-notes-news/august-2026.html) — CVE-2026-58231 は Data Hub Adapter の認可チェック欠如で未認証アクセスが可能。CVE-2026-34265 (SAP NetWeaver ABAP Kernel 7.22〜9.19、CVSS 9.8 メモリ破壊) も含まれる。SAP はエンタープライズ広範デプロイのため即日適用推奨 *(SAP / SecurityWeek / GBHackers 2026-08-11)*

- **[2026-08-11]** [米下院議員、Morguard へのランサムウェア攻撃 (Helix グループ)・Actini Group への KRYBIT 侵害 (2026-08-10) 等の週次インシデント増加傾向を懸念 — 北朝鮮系が Fortinet 等の未パッチ VPN/ファイアウォールを標的としたランサムウェアキャンペーンを継続](https://sherpaintelligence.substack.com/p/basecamp-briefing-august-11-2026) — Basecamp Briefing (2026-08-11) が今週のインシデント傾向を整理。Actini Group (仏産業製造) は 8/10 に KRYBIT ランサムウェアに侵害を受けたと報告、IEH Corporation (電子コネクター製造) も 8/4 フィッシングによるデータ窃取を開示 *(Sherpa Intelligence 2026-08-11)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-08-10 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-68820 | Windows Ancillary Function Driver for WinSock (afd.sys) 全サポートバージョン | CWE-416 / **7.0** | ローカル攻撃者が afd.sys の競合条件を特殊クラフトアプリで発火 → UAF によりカーネルヒープを制御 → SYSTEM 権限昇格 → FudModule v3.1 ルートキット (コード整合性無効化) をカーネルモードで展開 | 2026-08-12 Patch Tuesday KB5121003 ([Check Point](https://blog.checkpoint.com/research/state-sponsored-hackers-use-fake-job-offers-to-deliver-new-zero-day-exploit)) | Lazarus 実悪用 / CISA KEV 候補 / コード整合性バイパス / FudModule v3.1 新能力 |
| CVE-2026-59124 | Microsoft HPC Pack (全バージョン) | — / **9.8** | 未認証リモート攻撃者がネットワーク越しに認証不要経路を通じて HPC Pack 管理サービスに到達 → 任意コード実行 → HPC クラスター完全侵害 | 2026-08-11 Patch Tuesday ([Tenable](https://www.tenable.com/blog/microsofts-august-2026-patch-tuesday-addresses-398-cves-cve-2026-68820)) | CVSS 9.8 / 未認証 / ユーザー操作不要 / "exploitation more likely" / HPC 基盤に水平展開可 |
| CVE-2026-65665 | Microsoft SharePoint Server (SE/2019/2016) | CWE-502 / — | 既知の JWT 認証バイパス CVE-2026-55040 (KEV 実悪用済み) とチェーン → 認証不要で信頼されない BLOB を SharePoint デシリアライザに渡す → サーバー上で任意コード実行 | 2026-08-11 Patch Tuesday ([SecurityWeek](https://www.securityweek.com/august-2026-patch-tuesday-microsoft-fixes-421-cves-one-exploited-zero-day/)) | 未認証 RCE チェーン / 先行 CVE-2026-55040 は CISA KEV 実悪用済み / SharePoint 広範デプロイ |
| CVE-2026-58231 | SAP Commerce Cloud Data Hub Adapter (COM_CLOUD 2211 / 2211-JDK21) | CWE-285 / **10.0** | 未認証攻撃者が Data Hub Adapter の認可チェック欠如を悪用 → すべての Commerce データへの無制限アクセス・改ざん | SAP Note (2026-08-11) ([SAP Support](https://support.sap.com/en/my-support/knowledge-base/security-notes-news/august-2026.html)) | CVSS 10.0 / 未認証 / 大規模 E コマース基盤 / (commit 不明) |
| CVE-2026-44772 | SAP Manufacturing Integration and Intelligence — XMII 15.4/15.5 | CWE-94 / **9.9** | 攻撃者が XMII の入力検証不備を突いて任意コードを注入 → 製造実行環境 (MES) で任意コード実行 → 製造 OT 系への影響 | SAP Note (2026-08-11) (commit 不明) | CVSS 9.9 / 製造 OT・ICS / SAP MII 広範デプロイ / 同 CWE-94 系は他 MES に水平伝播可 |
| CVE-2026-34265 | SAP NetWeaver AS ABAP / ABAP Platform (Kernel 7.22〜9.19) | CWE-787 / **9.8** | 不正入力が ABAP カーネルのメモリ境界外書き込みを引き起こす → DoS / 潜在的な任意コード実行、全 NetWeaver テナントへ波及 | SAP Note (2026-08-11) (commit 不明) | CVSS 9.8 / SAP NetWeaver 超広範デプロイ / Kernel 7.22 は 15 年以上前のバージョンも対象 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-08-10 | JVN — LINE for Windows インストーラー DLL ローディング | LY Corporation の LINE for Windows インストーラーが安全でない方法で DLL をロード → 攻撃者が悪意ある DLL を配置した場合に任意コード実行の可能性 | CVSS 未採点 / 日本国内で広範利用 | [radar.offseq.com](https://radar.offseq.com/threat/installer-for-line-for-windows-insecurely-loads-dynamic-link-libraries-a836ea94133b21a5) |

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| SecurityWeek (August Patch Tuesday) | URL "august-2026-patch-tuesday" 確認 ✓; 3 zero-days / 421 CVE 数値確認 ✓ |
| Tenable Blog (CVE-2026-68820 / Patch Tuesday) | タイトル "microsofts-august-2026-patch-tuesday-addresses-398-cves-cve-2026-68820" 確認 ✓ |
| Check Point Research (Lazarus FudModule v3.1) | URL "state-sponsored-hackers-use-fake-job-offers" 確認 ✓; July 28 報告・Aug 5 CVE 割当・Aug 11 パッチ確認 ✓ |
| ZDI "The August 2026 Security Update Review" | URL "/2026/8/11/" 確認 ✓; 3 zero-days (CVE-2026-68820/62832/72971) 確認 ✓ |
| TechTimes / THN (Kimsuky offline AI lab) | TechTimes URL "20260810" 確認 ✓; THN URL "2026/08/kimsuky-builds" 確認 ✓; Genians 研究確認 ✓ |
| OpenAI Blog (GPT-5.6-Cyber / Daybreak) | URL "openai.com/index/expanding-daybreak-as-the-cyber-defense-window-narrows" 確認 ✓ (EGRESS_BLOCKED); Forbes URL "20260811" 確認 ✓; VentureBeat URL 確認 ✓ |
| Bloomberg / Yahoo Finance (Anthropic Theseus JV) | Bloomberg URL "2026-08-10" 確認 ✓; Macquarie Group Press Release 確認 ✓ |
| The Hill (House Democrats) | URL "6022646" 確認 ✓; 上院情報委との別行動確認 ✓ |
| SAP Support Portal (Aug 2026 Patch Day) | URL "august-2026.html" 確認 ✓; 28 新規セキュリティノート・4 クリティカル確認 ✓ |
| GBHackers / cyberpress.org (SAP CVE 詳細) | SAP MII CVE-2026-44772 (CVSS 9.9)・Commerce Cloud CVE-2026-58231 (CVSS 10.0)・NetWeaver CVE-2026-34265 (CVSS 9.8) 確認 ✓ |
| Sherpa Intelligence Basecamp Briefing 2026-08-11 | URL "august-11-2026" 確認 ✓; Actini/Helix/IEH インシデント確認 ✓ |
| radar.offseq.com (LINE for Windows DLL) | URL 確認 ✓; JVN 2026-08-10 公開確認 ✓ |

### 集計サマリ

- **巡回ソース数**: 約 30 (WebSearch 12 クエリ、WebFetch 試行 15 件)
- **採用件数**: AI=4 / Security=4 / CVE=6 / 国内=1
- **除外理由内訳**:
  - 採用窓外 (公開日 <2026-08-10): EU DMA Google Android 開放命令 (一次公開 2026-07-16); NVIDIA Open Secure AI Alliance 設立 (2026-07-27); Morguard ランサムウェア (Helix, 2026-08-07 初報); Levi Strauss データ侵害 (2026-08-07); Ceva Logistics 攻撃 (2026-08-01); DHS HSIN 侵害 (FIFA World Cup, 日付確認不可)
  - 重複 (excluded_set 参照): CVE-2026-68820 事前 Preview 言及あり (2026-08-11 digest)、本 digest は実リリース後の CVE 詳細・Lazarus 帰属を新規採用; CVE-2026-55040 (2026-08-11 digest 掲載); CVE-2026-62873 Microsoft 365 Admin Center (2026-08-06 early update で EGRESS_BLOCKED 確認できず除外); CVE-2026-62832/72971 は publicly disclosed 扱いで CVE table 採用優先度を下げ本文のみ記載
  - CISA KEV 8/11-12 追加分: Senserva によると 5 件が 7 日以内に追加とあるが個別 URL での日付確認不可のため記載保留。CVE-2026-68820 は KEV 候補として「優先シグナル」欄に明記
  - 取得失敗ソース (EGRESS_BLOCKED): thehackernews.com, bleepingcomputer.com, securityweek.com, tenable.com, zerodayinitiative.com, cybersecuritynews.com, openai.com, sec.cloudapps.cisco.com, isc.sans.edu, lansweeper.com, byteiota.com, action1.com, zecurit.com, itsecuritynews.info → WebSearch スニペット・Check Point Blog / TechTimes / Forbes / Bloomberg / SAP Support Portal / radar.offseq.com 等で代替

</details>

---

*生成: keda-digest-bot / 2026-08-12 05:07 JST*
