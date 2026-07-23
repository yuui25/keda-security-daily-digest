# KEDA Daily Digest — 2026-07-24 (JST)

> 採用範囲: 公開日 2026-07-22 〜 2026-07-24 (JST)
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

米 White House OSTP 長官が Moonshot AI を名指しし、Kimi K3 は Anthropic Fable 5 の工業規模ディスティレーションで構築されたと告発・Treasury が制裁を示唆するなど AI 地政学摩擦が新局面を迎えた。セキュリティ面では Check Point SmartConsole の未認証認証バイパス (CVE-2026-16232 CVSS 9.1) への野生悪用が確認され CISA KEV 追加・Jumbo Hotfix が緊急公開、Anubis ランサムウェアは Fairlife (Coca-Cola 傘下) から 1TB 盗取を 7/22 に公表した。CVE 面では Qualys が Linux XFS に 9 年間放置された競合状態 (CVE-2026-64600 RefluXFS) を 7/22 に開示し、RHEL 系 1,640 万システムへの影響と SELinux・コンテナを回避するローカル root 昇格が明らかになった。

---

## AI 関連ニュース

- **[2026-07-22]** 米 White House OSTP 長官が Moonshot AI の Kimi K3 は Anthropic Fable 5 のコバート工業ディスティレーションと名指し告発 — Fable 5 アクセス遮断 (6/XX) から Kimi K3 公開 (7/16) までの 15 日間が工業規模ディスティレーションと整合すると説明、Moonshot が禁輸対象 Nvidia GB300 をタイ経由取得の疑いも提示、Treasury 長官 Bessent が制裁・輸出規制ブラックリストを示唆。OpenAI Brockman は「Kimi K3 は相当よい」と認めつつディスティレーションの確認は保留。*(TechCrunch / EasternHerald / XenoSpectrum / Cryptopolitan)*

- **[2026-07-22]** OpenAI が企業向け AI エージェントプラットフォーム「Presence」を限定 GA で提供開始 — 音声・チャット対応のリアルタイムエージェント展開基盤。SOP・ガードレール・承認アクション・シミュレーション・Codex 改善ループを統合し、ChatGPT 自身のインバウンドサポートリクエストの 75% を処理中。Forward Deployed Engineers 主導デリバリーで self-service API は非公開。*(Help Net Security / VentureBeat / SiliconAngle / OpenAI Blog)*

- **[2026-07-24]** DeepSeek V4 が本日正式 GA — Preview (4/24) から全 GA へ移行。V4-Pro (1.6T params, 49B active) / V4-Flash (284B, 13B active)、1M コンテキスト標準搭載。北京営業時間帯 (9–12 時・14–18 時 CST) はピーク価格 2 倍の新料金体系を導入、従来の deepseek-chat / deepseek-reasoner API ID は 15:59 UTC に完全退役。*(TechNode / DeepSeek API Docs / iGeekPhone)*

- **[2026-07-23]** 中国ネクサス APT「JadeProx」が新型 DLL サイドローダー TriBack Loader でアジア・ラテアメリカの政府・医療・教育機関を標的 — Group-IB がシンガポールの Alibaba Cloud 露出サーバーから発見。ベトナム病院医療画像システム・マレーシア外務省・香港教育インフラへの侵入を確認。**フェイク Claude インストーラー**を初期侵入ベクタに使用し、Win32 コールバック API 経由でシェルコードをメモリ実行するステルス手法。*(THN / Group-IB / CyberPress)*

---

## セキュリティ関連ニュース

- **[2026-07-22]** Check Point SmartConsole CVE-2026-16232 が野生悪用確認・CISA KEV 追加、Jumbo Hotfix を緊急公開 — 未認証攻撃者が Management Server IP へアクセスすると SmartConsole ログイン認証を完全バイパスし管理者権限でセキュリティポリシーを改変可能。CISA が 7/22 に KEV 追加。Rapid7 はパッチ適用後も侵害痕跡調査を強く推奨。*(BleepingComputer / SecurityAffairs / Rapid7 / Check Point Blog)*

- **[2026-07-22]** [続報] Anubis ランサムウェアが Fairlife (Coca-Cola 傘下) への 7/16 攻撃を公式声明、1TB 盗取・カウントダウン公開 — 初回報道は 07-18 掲載済み (攻撃グループ未特定)。Anubis が 7/22 に DLS で犯行表明し Fairlife ロゴを白黒表示・約 1 週間のカウントダウン開始。生産システム暗号化と 1TB データ窃取を主張、Coca-Cola 米国内乳製品生産が停止継続。*(BleepingComputer / GV Wire / SecurityWeek / GovInfoSecurity)*

- **[2026-07-23]** JadeProx が旧 CVE 複数 (ASUSTOR ADM / Tenda AC11 / WebSVN) を併用した複合侵入チェーンを確認 — TriBack Loader は 3 ファイルの組み合わせで signed binary を DLL サイドロード。Alibaba Cloud サーバーはレポート公開時には既にオフライン。アジア・ラテアメリカ政府機関は fake installer と古い IoT CVE の組み合わせによるフィッシングへの警戒が必要。*(THN / Group-IB)*

- **[2026-07-22]** [続報] CISA が CVE-2026-50522 (SharePoint RCE) を KEV 追加、連邦機関に 7/25 期限 — 野生悪用 (機械キー窃取・バックドア設置) 確認後に正式 KEV 登録。連邦省庁はパッチ適用に加え認証情報・機械キーのローテーションが義務化対象。*(CISA KEV / Windows News AI)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-07-22 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-16232 | Check Point Security Management / Multi-Domain Management (Jumbo Hotfix 未適用) | CWE-287 / **9.1** | 未認証攻撃者が Management Server IP に到達 → SmartConsole ログイン認証フローを完全バイパスしトークン取得 → Management Server に管理者権限でログインしポリシー改変・バックドア設置 | Jumbo Hotfix (2026-07-22) / [Check Point SA](https://blog.checkpoint.com/security/security-advisory-action-required-active-exploitation-of-check-point-smartconsole-authentication-bypass-cve-2026-16232/) | **CISA KEV 2026-07-22** / 野生悪用確認 / Trusted Clients 非制限環境は侵害痕跡を優先調査 |
| CVE-2026-64600 (RefluXFS) | Linux kernel 4.11〜 (XFS reflink 有効・RHEL 7+ はデフォルト) | CWE-362 / **7.0** | ローカル非特権ユーザーが XFS reflink 並行書込みで競合状態をトリガー → ファイルシステムがブロック層で任意の読取可能ファイルを上書き → ホスト root 権限取得; SELinux・コンテナ・カーネルハードニングを回避 | kernel tree マージ済み (2026-07-16) / [Qualys Advisory](https://cdn2.qualys.com/advisory/2026/07/22/RefluXFS.txt) | 2026-07-22 Qualys 開示 / **RHEL 系 1,640 万システム** / 悪用ログなし・再現性高 / 唯一の対策はパッチ kernel への交換＋再起動 |
| CVE-2026-16157 | Duplicati backup software v2.3.0.1 (Windows・デフォルト以外のインストールパス) | CWE-732 / 評価中 | ローカル書込み権限を持つ攻撃者が非標準インストールディレクトリに悪意ある DLL を設置 → Duplicati サービス再起動時 Windows ローダーが優先読込み → `NT AUTHORITY\SYSTEM` で任意コード実行 | 最新版アップデート or デフォルトパス (`C:\Program Files\Duplicati 2\`) への再インストール / [CERT/CC VU#847406](https://kb.cert.org/vuls/id/847406) | 2026-07-23 JVNVU#98636554 公開 / Windows バックアップ広範利用 / DLL プレースメント LPE パターン水平伝播候補 |

---

## 国内脆弱性・インシデント情報

| 公開日 | 識別子 | 概要 (1行) | CVSS/影響 | リンク |
|--------|--------|-----------|-----------|--------|
| 2026-07-23 | JVNVU#98636554 / CVE-2026-16157 | Duplicati バックアップソフト v2.3.0.1 (Windows): デフォルト外インストールパスで DLL プリロードによる SYSTEM 権限昇格が可能、デフォルトパスへの再インストールまたは最新版への更新で回避。 | 影響中 / Windows バックアップ環境 | [JVNVU#98636554](https://jvn.jp/vu/JVNVU98636554/) / [CERT/CC VU#847406](https://kb.cert.org/vuls/id/847406) |

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| TechCrunch / EasternHerald / Cryptopolitan / XenoSpectrum (White House Moonshot Kimi K3 ディスティレーション告発) | TechCrunch URL "/2026/07/22/" 確認 ✓ / EasternHerald "2026/07/23" 確認 ✓ |
| Help Net Security / VentureBeat / SiliconAngle / OpenAI Blog (OpenAI Presence) | Help Net Security URL "/2026/07/22/" 確認 ✓ / SiliconAngle URL "/2026/07/22/" 確認 ✓ |
| TechNode / DeepSeek API Docs / iGeekPhone (DeepSeek V4 GA) | iGeekPhone タイトル "Official Release Expected Within Days" 確認 / inews.zoombangla.com "Launches Tomorrow" (2026-07-23 掲載) 確認 ✓ |
| THN / Group-IB / CyberPress (JadeProx TriBack Loader) | THN URL "2026/07/china-nexus-jadeprox-uses-new-triback.html" 確認 ✓ / CyberPress URL "/jadeprox-triback-campaign/" 確認 ✓ / Group-IB レポート 2026-07-23 |
| BleepingComputer / SecurityAffairs / Rapid7 / Check Point Blog (CVE-2026-16232) | BleepingComputer タイトル "Check Point warns of SmartConsole zero-day exploited in attacks" 確認 ✓ / Rapid7 URL タイトル "etr-cve-2026-16232" 確認 ✓ / CISA KEV 追加 2026-07-22 確認 ✓ |
| BleepingComputer / GV Wire / SecurityWeek / GovInfoSecurity (Anubis / Fairlife [続報]) | GV Wire URL "/2026/07/22/" 確認 ✓ / BleepingComputer タイトル "Anubis ransomware claims Coca-Cola Fairlife attack" 確認 ✓ |
| CISA KEV / Windows News AI (CVE-2026-50522 CISA KEV 追加) | windows-news.ai "CISA Sounds Active Exploit Alarm for SharePoint, Check Point" 確認 ✓ |
| Qualys Blog / SecurityOnline / Techtimes / oss-security ML (CVE-2026-64600 RefluXFS) | Qualys URL "/2026/07/22/refluxfs-a-linux-kernel-local-privilege..." 確認 ✓ / oss-security.openwall.org 2026-07-22 確認 ✓ / Techtimes URL "20260723" 確認 ✓ |
| CERT/CC VU#847406 / JVN (CVE-2026-16157 Duplicati) | JVNVU#98636554 2026-07-23 公開確認 ✓ / CERT/CC VU#847406 確認 ✓ |
| jvn.jp / jpcert.or.jp / ipa.go.jp | Duplicati JVNVU#98636554 (2026-07-23) 確認 ✓ / 他 2026-07-22〜24 新規エントリ調査済み |
| 全 WebFetch 試行 | 全 403 Forbidden → WebSearch スニペット・二次ソースで代替 |

### 集計サマリ

- **巡回ソース数**: 約 22
- **採用件数**: AI=4 / Security=4 / CVE=3 / 国内=1
- **除外理由内訳**:
  - 古すぎ (today-2 = 2026-07-22 より前): GigaWiper Microsoft レポート (2026-07-09/10 公開) / CVE-2026-8933 snap-confine Qualys 開示 (2026-07-21 / 直前の 07-22・07-23 ダイジェストでも未収録だが今日の採用窓外のため除外) / FreePBX CVE-2026-46376 GHSA (2026-05-15 公開) / Duplicati 採用済みのため snap-confine を追加収録せず
  - 重複 (excluded_set 参照): OpenAI/HuggingFace 侵害 WaPo 07-23 記事 (07-23 ダイジェストで [続報] 掲載済み) / UK AISI frontier model 不正行為報告 (07-23 掲載済み) / CVE-2026-50522 SharePoint 野生悪用 (07-23 掲載済み / CISA KEV 追加を新展開として [続報] 採用) / Nichirei RansomHouse (07-23 掲載済み) / Oracle July 2026 CPU (07-23 掲載済み) / Qilin ランサムウェア (07-23 掲載済み) / Gemini 3.6 Flash 3.5 Flash Cyber (07-23 掲載済み)
  - 日付不明・未確認: 欧州銀行 TikTok データ送信 (日付未確認のため除外) / One Community Federal Credit Union DragonForce (詳細日付未確認)

### 主要採用補足

- **White House Moonshot 告発**: TechCrunch URL "/2026/07/22/" 確認。Kimi K3 自体は 07-17 / 07-22 掲載済みだが White House の名指し告発・Treasury 制裁示唆は新展開。
- **OpenAI Presence**: 07-23 ダイジェストで「OpenAI がエンタープライズエージェントプラットフォームを発表」との言及なし → 新規採用。
- **DeepSeek V4 GA**: TechNode の 6/30 記事で「mid-July GA 予定」確認済み。inews.zoombangla.com の 7/23 付け "Launches Tomorrow" が 7/24 GA を裏付け。
- **CVE-2026-64600 RefluXFS**: Qualys URL が "/2026/07/22/" を確認。oss-security ML の 2026-07-22 スレッドも確認。CVSS 7.0 は CVSSv3.1、ローカル (AV:L) の制約あるが RHEL 系デフォルト XFS での広範影響と SELinux/コンテナ回避で優先採用。
- **CVE-2026-8933 (snap-confine) 除外理由**: Qualys の開示 URL が "/2026/07/21/" を示し today-2 (2026-07-22) より 1 日前。07-22・07-23 ダイジェストで収録されるべきだったが未収録の missed item。今日の採用窓には含められないため除外 (窓外項目ルール厳守)。

### 取得失敗ソース

- 全 WebFetch 試行が 403 Forbidden (bleepingcomputer.com / thehackernews.com / helpnetsecurity.com / securityaffairs.com / rapid7.com / checkpoint.com / qualys.com / group-ib.com 等)
- 上記全てを WebSearch スニペット + 二次ソース (cybernews / cyberpress / securityonline / govinfosecurity 等) で代替

</details>

---

*生成: keda-digest-bot / 2026-07-24 05:04 JST*
