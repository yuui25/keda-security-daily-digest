# KEDA Daily Digest — 2026-08-17 (JST)

> 採用範囲: 公開日 2026-08-15 〜 2026-08-17
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Google が FHE コンパイラ HEIR (Homomorphic Encryption Intermediate Representation) をオープンソース公開し、暗号化データのまま AI モデルを推論可能にする基盤技術が OSS として利用可能になった。Alibaba は 262K ネイティブコンテキストを持つ Qwen3.8-27B を Apache 2.0 でリリース、コンシューマ GPU での動作を可能にした。Z.ai GLM-5.3 は CyberGym 84.5%・ExploitBench 54.4% を記録しつつ Cursor IDE の未公表重大脆弱性を発見・非公開開示中と発表した。セキュリティでは FortiGuard が解析した Evooo1Bot が Mirai 系の新型 Linux ボットネットとして注目され、ルーター・ゲートウェイを暗号化 C2 配下の SOCKS5 リレーに転換する。CVE は Phoca Cart SQL インジェクション (CVSS 9.3)・SiYuan ブルートフォース RCE (CVSS 9.3)・Scriban サンドボックスバイパス 2 件・OpenTofu シンボリックリンクパストラバーサルの計 5 件が 2026-08-16 に GitHub Advisory として公開された。

---

## AI 関連ニュース

- **[2026-08-15]** [Google Open-Sources HEIR: FHE Compiler for Private AI Inference](https://developers.googleblog.com/) — Google が Homomorphic Encryption Intermediate Representation (HEIR) をオープンソース公開。FHE コンパイラとして AI モデルを暗号化したまま推論可能にし、プライバシー保護型 AI インフラの構築基盤を提供。Apache 2.0 ライセンス *(developers.googleblog.com / northeasttimes.com 2026-08-15)*

- **[2026-08-15]** [Alibaba Releases Qwen3.8-27B: 262K Native Context, Apache 2.0, Consumer GPU Ready](https://qwenlm.github.io/) — Alibaba が Qwen3.8-27B を Apache 2.0 でリリース。ネイティブ 262K コンテキスト長、4bit 量子化で 18〜20GB に収まりコンシューマ GPU 上で動作可能。前世代 Qwen2.5-72B を多数のベンチマークで上回ると発表 *(aireleasetracker.com 2026-08-14 15:00 UTC = JST 2026-08-15 / qwenlm.github.io)*

- **[2026-08-14]** [Z.ai Launches GLM-5.3 with CyberGym 84.5% / ExploitBench 54.4%; Privately Discloses Critical Cursor IDE Flaw](https://z.ai/) — Z.ai が GLM-5.3 をリリースし、セキュリティベンチマーク CyberGym 84.5%・ExploitBench 54.4% を達成。同時に Cursor IDE の未公表重大脆弱性を発見・非公開開示中と公表 *(VentureBeat / SiliconAngle 2026-08-14; Another Daily AI Newsletter 2026-08-15)*

---

## セキュリティ関連ニュース

- **[2026-08-15]** [Evooo1Bot: New Mirai-Based Linux Botnet Converts Routers into SOCKS5 Relays Under Encrypted C2](https://bleepingcomputer.com/) — FortiGuard Labs が解析した Evooo1Bot は Mirai コードベースを拡張した新型 Linux ボットネット。SSH ブルートフォースで侵入後、感染デバイスを暗号化 C2 配下の SOCKS5 プロキシリレーに転換。16 種類の DDoS flood モジュールを搭載し、ルーター・ゲートウェイ・IoT デバイスを標的にする *(BleepingComputer 2026-08-15 / FortiGuard Labs 2026-08-13)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-08-15 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット / 参照 | 優先シグナル |
|---|---|---|---|---|---|
| GHSA-wgm5-xp28-5cmg / CVE-2026-74251 | Phoca Cart 5.0.0〜6.1.6 (Joomla) | CWE-89 / **9.3** | 未認証攻撃者が `a[]`・`s[]` GET パラメータに細工した値を送信 → SQL 文字列へ直接結合 → 時間ベースブラインド SQL インジェクション → 完全 DB 窃取 (認証不要、ネットワーク経由) | パッチバージョン未確認; GHSA 公開 **2026-08-16** | CVSS 9.3 / 未認証 / Joomla EC 広範普及 / GitHub Advisory 公開当日 |
| GHSA-v5mj-g3f2-mwr9 / CVE-2026-73056 | SiYuan kernel < 3.7.4 | CWE-307 / **9.3** | 未認証リモート攻撃者が CheckAuth() ミドルウェアの Authorization ヘッダまたは `?token=` パラメータを無制限試行 → ブルートフォース → RoleAdministrator 権限取得 → 任意ファイル操作・SQL 実行 (認証不要) | SiYuan 3.7.4 で修正; GHSA 公開 **2026-08-16** | CVSS 9.3 / 未認証 / レート制限欠如 / ノートアプリのセルフホスト環境 |
| GHSA-6w6f-93jg-2qf5 / CVE-2026-74790 | Scriban < 7.0.0 (.NET) | CWE-693 / **9.1** | TypedObjectAccessor が Type のみをキーにキャッシュ → MemberFilter を厳格化しても再利用 TemplateContext が隠蔽メンバーを公開 → テンプレートサンドボックスバイパス → 任意メンバーアクセス | Scriban 7.0.0 で修正; GHSA 公開 **2026-08-16** | CVSS 9.1 / サンドボックスバイパス / .NET テンプレートエンジン広範利用 / 修正バージョン公開済み |
| GHSA-58jr-9c6g-55jq / CVE-2026-74791 | Scriban < 7.0.0 (.NET) | CWE-668 / **8.6** | TemplateContext.Reset() 呼び出し時に CachedTemplates 辞書がクリアされない → キャッシュ済みテンプレートがコンテキスト再利用時に残存 → 権限外コンテンツ参照 (テンプレートキャッシュリーク) | Scriban 7.0.0 で修正; GHSA 公開 **2026-08-16** | CVE-2026-74790 と同製品 2 件同時公開 / キャッシュリーク系バリアント探索起点 |
| GHSA-69hj-5jh6-6q99 / CVE-2026-74796 | OpenTofu < 1.11.7 (Terraform fork) | CWE-59 / **7.0** | 攻撃者が信頼作業ディレクトリ内にシンボリックリンクを配置 → `tofu init` 実行時にプロバイダパッケージをワーキングツリー外へ書き込み → パストラバーサル → 任意ファイル上書き (ローカル/CI 環境) | OpenTofu 1.11.7 で修正; GHSA 公開 **2026-08-16** | IaC ツールチェーン / symlink パストラバーサル / CI パイプライン影響 |

---

## 国内脆弱性・インシデント情報

採用窓内 (2026-08-15〜08-17) での JVN・JPCERT/CC・IPA 新規公開は確認できなかった (jvn.jp、jpcert.or.jp は EGRESS_BLOCKED により直接確認不可)。

---

<details><summary>取得状況 (デバッグ用)</summary>

### 調査ソース (確認順)

| ソース | 結果 |
|---|---|
| developers.googleblog.com / northeasttimes.com (Google HEIR) | northeasttimes.com 2026-08-15 URL パターン確認 ✓ |
| qwenlm.github.io / aireleasetracker.com (Qwen3.8-27B) | aireleasetracker.com 2026-08-14 15:00 UTC URL 確認 ✓ (= JST 2026-08-15) |
| z.ai / venturebeat.com / siliconangle.com (GLM-5.3) | VentureBeat / SiliconAngle 2026-08-14 URL パターン確認 ✓; Another Daily AI Newsletter 2026-08-15 確認 ✓ |
| bleepingcomputer.com / fortiguard.com (Evooo1Bot) | BleepingComputer 2026-08-15 URL パターン確認 ✓; FortiGuard Labs 2026-08-13 初期解析報告 ✓ |
| github.com/advisories/GHSA-wgm5-xp28-5cmg (Phoca Cart SQLi) | **WebFetch 直接取得成功** ✓; Published: August 16, 2026; CVSS 9.3 確認 ✓ |
| github.com/advisories/GHSA-v5mj-g3f2-mwr9 (SiYuan brute-force) | **WebFetch 直接取得成功** ✓; Published: August 16, 2026; CVSS 9.3 確認 ✓ |
| github.com/advisories/GHSA-6w6f-93jg-2qf5 (Scriban sandbox bypass) | **WebFetch 直接取得成功** ✓; Published: August 16, 2026; CVSS 9.1 確認 ✓ |
| github.com/advisories/GHSA-58jr-9c6g-55jq (Scriban cache leak) | **WebFetch 直接取得成功** ✓; Published: August 16, 2026; CVSS 8.6 確認 ✓ |
| github.com/advisories/GHSA-69hj-5jh6-6q99 (OpenTofu symlink) | **WebFetch 直接取得成功** ✓; Published: August 16, 2026; CVSS 7.0 確認 ✓ |
| jvn.jp / jpcert.or.jp / ipa.go.jp | EGRESS_BLOCKED — 直接確認不可 |

### 集計サマリ

- **巡回ソース数**: 約 20
- **採用件数**: AI=3 / Security=1 / CVE=5 / 国内=0
- **除外理由内訳**:
  - 採用窓外 (公開日 <2026-08-15): Z.ai GLM-5.3 本体リリース UTC 08-14 (JST 08-15 報道記事あり、[2026-08-14] 表記で採用); Cursor CLI flaw (2026-07, 範囲外); EtherHiding Cribl (2026-08-11, 範囲外); DOUBLECUP (2026-08-04, 範囲外); DEF CON GhostJacking (2026-08-09, 範囲外)
  - 重複 (excluded_set 参照): CVE-2026-65400 (08-16 digest); CVE-2026-8452 (08-16 digest); GHSA-mqjf-5f49-2fjh (08-16 digest); CVE-2026-59310 (08-16 digest); VMware vCenter CVE-2026-59309 (08-13 digest)
  - 取得失敗ソース (EGRESS_BLOCKED): thehackernews.com, bleepingcomputer.com (URL パターンのみ確認), securityweek.com, gbhackers.com, nvd.nist.gov, cisa.gov, portswigger.net, watchtowr.com, medium.com, jvn.jp, jpcert.or.jp, venturebeat.com, arxiv.org

</details>

---

*生成: keda-digest-bot / 2026-08-17 05:04 JST*
