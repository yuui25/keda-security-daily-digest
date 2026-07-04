# KEDA Security Daily Digest — 2026-07-05 (JST)

> 対象期間: 2026-07-03 〜 2026-07-05 (JST) / 生成: 2026-07-05T05:03 JST

---

## AI 動向

- `[2026-07-04]` **Anthropic / 国防総省訴訟書類公開** — xAI株を保有したまま Anthropic に武器ガードレール撤廃を迫ったとされる Emil Michael 氏の証言調書が unsealed。ブラックリスト確定翌日に「合意まで後一歩」と発言していたことが判明。180日解約条項に関する手続きも進行中。*(TechTimes / Gizmodo / The Next Web)*
- `[2026-07-03]` **Anthropic が中国アクセス抜け穴を閉鎖** — Ant Group シンガポール子会社・ByteDance VPN 経由のアクセスをブロック。Alibaba Qwen は最大規模の蒸留攻撃（2026年4月22日〜6月5日, 25,000アカウント, 2,880万インタラクション）として認定。*(BanklessTimes / CryptoBriefing)*
- `[2026-07-03]` **OpenAI、IPO 前に米政府へ 5% 株式提供を協議** — バリュエーション $7,300億; アラスカ永久基金方式。Trump / Lutnick / Bessent らと直接交渉中。*(ResultSense / CoinDesk / American Bazaar)*
- `[2026-07-03]` **国連・ITU「AI for Good」グローバル委員会が発足** — 共同議長: Marc Benioff + Paul Kagame 大統領。Jensen Huang・Andy Jassy・Brad Smith・Jack Clark ら参加。初回会合 7月8日ジュネーブ。*(Axios / Eastern Herald / AI Weekly)*
- `[2026-07-04]` **「Bad Epoll」CVE-2026-46242** — Anthropic Mythos AI が隣接 CVE-2026-43074 を検出したが本脆弱性は見落とし。ソウル大 Jaeyoung Chung 氏が PoC 成功率 99% の Linux epoll UAF を発見・公表。*(TechTimes / THN)*
- `[2026-07-03]` **Adobe が月 2 回セキュリティ速報体制へ移行** — 7月14日より第 2・第 4 火曜に公開予定。AI による開示→悪用ウィンドウが数日→数時間に短縮されたことを理由に挙げる。*(CSO Online / Computerworld)*

---

## セキュリティ動向

- `[2026-07-03]` **Kubota North America 侵害** — 2026年3月16日〜4月20日にかけて約1か月間不正アクセス。対象: 従業員氏名・SSN・生年月日・銀行口座情報。ランサムウェア被害宣言なし。Kroll による信用監視サービスを提供。*(BleepingComputer)*
- `[2026-07-03]` **Avalon モジュール型マルウェアフレームワーク発見** — Blackpoint APG が捕捉。Proton Drive 上の ISO ルアー → CrownX ランサムウェア（AES-GCM 暗号化）。VSS / WinRE / バックアップシステムを標的にし、認証情報収集モジュールを内蔵。*(THN / GBHackers / CyberPress)*
- `[2026-07-03]` **Pegasus がギリシャ MEP を3回ハッキング** — Citizen Lab 調査: スパイウェアが Stelios Kouloglou 議員（Pegasus 乱用調査の PEGA 委員会委員）を 2022年10月・2023年3月に計3回標的に。政府帰属なし。*(Citizen Lab / Al Jazeera / THN)*
- `[続報][2026-07-03]` **Adobe ColdFusion CVE-2026-48282 が公開直後から悪用** — 7月1日公開から数時間以内にインド発 IP から悪用試行を確認。NHS Digital アラート CC-4808 を発令。*(NHS Digital / THN)*
- `[続報][2026-07-03/04]` **SharePoint 侵害ネットワークに 2 つの脅威アクター** — Microsoft 調査で判明: Storm-2603/Warlock は Cloudflare トンネル + VS Code SSH を使用; 第 2 の不明アクターは NTDS.zip 経由で NTDS.dit を窃取し WinRM で横移動。*(CyberNews / CSO Online)*

---

## 新規 CVE / 脆弱性

| CVE / GHSA | 製品 / バージョン | CWE / CVSS | バグクラス概要 | 修正コミット | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-46242 | Linux kernel ≥6.4 (Android 6.6+ / Pixel 含む) | CWE-416 / 7.8 | `ep_remove()` がロック下で `file->f_ep` クリア後も file オブジェクトを使用 → 並行 release パスが `struct eventpoll` を解放 → UAF → 非特権ユーザーが root へ LPE | kernel mainline (2026-04-24 コミット) / ディストリビューション側バックポート多数未適用 | 2026-07-04 公開 / AI 監査ツール (Mythos) が見落とし / PoC 成功率 99% |
| CVE-2026-12166 + CVE-2026-12167 + CVE-2026-12168 (CERT VU#639124) | Little Orbit GamersFirst `GFAC_Sys_x64.sys`（全バージョン） | CWE-476 / CWE-20 / CWE-123 / High | 低特権ユーザーが minifilter 通信ポートへ直接接続可 (CVE-2026-12167) → write-what-where で任意カーネルアドレスに書き込み → プロセストークン改ざん → SYSTEM 権限昇格 (CVE-2026-12168) | ベンダー未パッチ (CERT VU#639124) | JVN 2026-07-03 公開 / ゲームアンチチートはカーネル権限で広範インストール済み |

---

## 国内動向

2026-07-03 〜 07-05 (JST) 期間中、主要ソース（JPCERT/CC・IPA・JVN・Piyolog）にて新規国内脆弱性・インシデントの公表は確認できませんでした。
