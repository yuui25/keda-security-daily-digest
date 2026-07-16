# KEDA Security Daily Digest — 2026-07-17

> 採用範囲: 2026-07-15〜2026-07-17 JST に公開された情報のみ掲載。過去 7 日分との重複を除外 ([続報] 表記を除く)。

---

## AI 関連ニュース

1. [2026-07-15] Anthropic・Blackstone・H&F が「Ode with Anthropic」を設立 — 企業向け AI 実装を行う $1.5B 合弁会社、Fortune 500 の既存 BH/H&F 投資先へのエンタープライズ Claude 展開を優先的に推進。([HPCWire](https://www.hpcwire.com/) / [Yahoo Finance](https://finance.yahoo.com/))

2. [2026-07-15] Microsoft が社内研修資料で Anthropic Claude を「動作が遅く精度が低い、セキュリティ統合不足」と酷評するよう営業担当者に指示していたことが判明 — 自社 Copilot との競合を意識した異例の内部批判。([TechCrunch](https://techcrunch.com/) / Bloomberg)

3. [2026-07-16] Google AI Mode にアプリ連携機能を追加 — Instacart・Canva・YouTube が初期対応パートナーとして統合され、検索結果から直接タスクを実行可能に。([TechCrunch](https://techcrunch.com/))

4. [2026-07-16] Moonshot AI が Kimi K3 (2.5T パラメーター MoE、1M コンテキスト) を WAIC 2026 (7/17〜20) で公開予定と発表 — 中国最大規模の MoE モデルで英中バイリンガル対応。([TechCrunch](https://techcrunch.com/) / FT)

5. [2026-07-15] ロシア系脅威アクター "bandcampro" がジェイルブレイクした Google Gemini CLI を C2 基盤として悪用 — わずか 6 分でボットネット C2 スクリプトを生成し、歯科クリニックの OpenDental DB に侵入したケースを Unit 42 が分析。([Help Net Security](https://www.helpnetsecurity.com/) / xloggs)

6. [2026-07-15] Unit 42 が LLM 生成 IoT ボットネット「TuxBot v3」を解析 — 17 CPU アーキテクチャ対応のクロスコンパイルフレームワークを LLM 支援で実装したが、XOR 鍵破損・Argon2id 偽装・安全免責文句の削除忘れ等の実装欠陥を残したまま公開。([Palo Alto Unit 42](https://unit42.paloaltonetworks.com/))

7. [2026-07-16] [続報] WAIC 2026 が 7/17 に北京で開幕 — 習近平が初の基調講演、中国が WAICO (World AI Cooperation Organization) をグローバルサウス向け AI ガバナンス国際機関として正式提案。([TechTimes](https://www.techtimes.com/) / Xinhua)

---

## セキュリティ関連ニュース

1. [2026-07-15] Windows ProfSvc EoP ゼロデイ「LegacyHive」が Patch Tuesday 直後に PoC 公開 — Nightmare-Eclipse (Chaotic Eclipse) が stripped PoC を公開、全 supported Windows バージョンが影響対象、CVE 未付与・未パッチ。([The Register](https://www.theregister.com/security/2026/07/15/microsofts-serial-tormentor-drops-legacyhive-0-day/5271723) / SecurityWeek)

2. [2026-07-16] Zoom CVE-2026-53412 (CVSS 9.8) — Windows クライアントの不正入力検証により未認証のネットワーク攻撃者がアカウント乗っ取り可能、Zoom Workplace for Windows <7.0.0 / VDI / Meeting SDK が対象。([BleepingComputer](https://www.bleepingcomputer.com/) / THN)

3. [2026-07-15] CISA KEV に Oracle E-Business Suite CVE-2026-46817 (CVSS 9.8) を追加 — 連邦機関は 7/18 までにパッチ適用義務、Payments コンポーネントの未認証 RCE。([CISA](https://www.cisa.gov/) / GBHackers)

4. [2026-07-15] [続報] CVE-2026-58644 (SharePoint RCE) の脅威評価が格上げ — Microsoft が 7/15 にアドバイザリを更新し "Exploitation More Likely" → "**Exploitation Detected**" に変更、野生悪用が確認された。

5. [2026-07-15] スペイン警察がサイバー犯罪組織を摘発、4 人逮捕 — 投資詐欺と BEC を組み合わせ €140M (マネロン確認 €94M + BEC €46M) を騙取した国際組織を壊滅。([Help Net Security](https://www.helpnetsecurity.com/) / BleepingComputer)

6. [2026-07-15] Firefox 152.0.6 / Chrome 150 が緊急パッチ — CVE-2026-15718 (JS/WebAssembly 無効ポインタ参照) と CVE-2026-15719 (DOM サイトアイソレーション欠陥) を修正、公開 PoC あり・野生悪用未確認。(THN)

---

## 新規 CVE / Advisory

| CVE/GHSA | 製品・バージョン | CWE / CVSS | バグクラス (条件→シンク→結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| CVE-2026-53412 | Zoom Workplace for Windows <7.0.0 / VDI Client / Meeting SDK | CWE-20 / **9.8** | 未認証攻撃者がネットワーク越しに不正入力データを送信 → Windows クライアントが検証なしに処理 → アカウント乗っ取り | [Zoom Security Bulletin](https://explore.zoom.us/en/trust/security/security-bulletin/) | CVSS 9.8 / 2026-07-16 公開 / 即時パッチ推奨 |
| CVE-2026-46817 | Oracle E-Business Suite 12.2.3〜12.2.15 (Payments) | CWE-269 / **9.8** | 未認証攻撃者が `/OA_HTML/ibytransmit` に細工 XML を POST → File Transmission コンポーネントが認可なしに処理 → Oracle Payments 完全制御・決済データ漏洩 | [Oracle CPU May 2026](https://www.oracle.com/security-alerts/) | **CISA KEV 2026-07-15 追加** / 連邦機関 7/18 期限 / CVSS 9.8 |
| CVE-2026-58659 | PyTorch Lightning ≤2.6.5 | CWE-502 / **8.4** (CVSSv4) / 7.8 (v3.1) | 攻撃者が細工チェックポイントファイルを作成 → `_load_state` が `_instantiator` ハイパーパラメーターからモジュール名を import・実行 → `weights_only=True` をバイパスして任意コード実行 | [CVE-2026-58659](https://cve.threatint.eu/CVE/CVE-2026-58659) | 2026-07-15 公開 / AI/ML パイプラインで広く利用 / チェックポイント共有リポジトリへの水平伝播リスク |
| CVE-2026-59255 | BloodHound CE ≤9.4.0 (Go) | CWE-862 / **7.1** | 有効セッショントークンを持つ認証済みユーザーが `custom-nodes` エンドポイントに POST/PUT/DELETE → 認可チェック欠如により全ユーザー・テナントに影響するグローバルグラフスキーマを改ざん | [commit 8f79035](https://github.com/SpecterOps/BloodHound) | 2026-07-15 公開 / AD 攻撃経路管理ツール / ペネトレーションテスト環境への影響 |
| LegacyHive (CVE 未付与) | Windows ProfSvc / User Profile Service (全 supported 版) | CWE-732 / 未 CVSS | 非管理者ユーザーが ProfSvc の任意 hive load パスを悪用 → 管理者ユーザーの classes レジストリ hive を改ざん → EoP (追加認証不要、UsrClass.dat 以外のパスも可) | 未パッチ / stripped PoC: [Nightmare-Eclipse](https://www.theregister.com/security/2026/07/15/microsofts-serial-tormentor-drops-legacyhive-0-day/5271723) | 2026-07-15 PoC 公開 / 全 supported Windows 対象 / **未パッチ** / 強力な EoP プリミティブ |
| [続報] CVE-2026-58644 | Microsoft SharePoint Server 2016/2019/SE | CWE-502 / **9.8** | (07-16 digest 掲載済) デシリアライズ RCE | [MSRC](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2026-58644) | **野生悪用確認 (2026-07-15 Microsoft 更新)** |

---

## 国内脆弱性・インシデント

| 日付 | 組織・製品 | 概要 | 影響度 | 参照 |
|---|---|---|---|---|
| 2026-07-15 | 日本交通株式会社 | AiLock ランサムウェアグループが 7/15 に犯行声明を公表 — 7/11 の侵入でタクシー配車・ハイヤー予約システムが停止 (8,500 台以上影響)、データ漏洩は未確認だが AiLock が近日公開を予告 | 影響大 / 国内最大手タクシー会社 | [BleepingComputer](https://www.bleepingcomputer.com/news/security/japans-largest-taxi-operator-shuts-systems-after-cyberattack/) / [ransomware.live](https://ransomware.live/) |

---

*生成: keda-digest-bot / 2026-07-17 05:04 JST*
