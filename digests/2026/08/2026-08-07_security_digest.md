# KEDA Daily Digest — 2026-08-07 (JST)

> 採用範囲: 公開日 2026-08-05 〜 2026-08-07
> 生成: claude-sonnet-4-6 / 自動 (cron: 0 20 * * * UTC = 05:00 JST)

## 本日のサマリ

Unit 42 が Google パスワードマネージャー同期パスキーのマスターキーが Chrome メモリ上で平文になる構造的欠陥 (Pass-TA-Key) を Black Hat で開示し、盗んだキーは無効化不可能という深刻性が注目された。CISA が JetBrains TeamCity (CVE-2026-63077) を KEV 追加し期限を異例の 3 日 (8/8) に設定。Cisco が AI モデルを使った内部セキュリティテストで IOS XE から CVSS 9.8 コマンドインジェクション 12 件 (CVE-2026-20272) を発見・開示したことが AI × 脆弱性発見の新潮流として注目される。Gitea に未認証 RCE (CVE-2026-59774 / CVSS 9.8) と Paperclip AI 管理基盤に Metasploit module 付き RCE (CVE-2026-41679) が相次ぎ公開され、AI インフラの脆弱性が連日続く。

---

## AI 関連ニュース

- **[2026-08-05]** [Unit 42、Google Password Manager 同期パスキーのマスターキーが Chrome メモリ上で平文になる構造的欠陥「Pass-TA-Key」を Black Hat USA 2026 で開示 — 盗んだ 32 バイトキーは無効化不可能](https://unit42.paloaltonetworks.com/passkey-research/) — Chrome の Google パスワードマネージャー同期パスキー実装が32バイトマスターキーをプロセスメモリ上に平文で保持する構造的欠陥を発見。Pass-TA-Key (メモリ読み取りでキー窃取)・Silver Pass-TA-Key (中間者攻撃)・Golden Pass-TA-Key (ドメイン横断窃取) の3攻撃手法を実証。窃取済みキーはローテーション・無効化が不可能な点が最大の脅威。 *(Unit 42 2026-08-03 論文公開 / BleepingComputer・SecurityWeek・TechTimes 2026-08-05 報道)*

- **[2026-08-05]** [Cisco、社内で「advanced AI models」を活用した自律的セキュリティテストを実施し IOS XE から CVSS 9.8 コマンドインジェクション 12 件 (CVE-2026-20272 他) を発見・同日開示](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-iosxe-cmdinject-k3NKPKK9) — Cisco PSIRT が AI モデルを内部テストに活用し IOS XE の入力処理特殊文字サニタイズ不備を12件発見。うち最高 CVSS 9.8 の CVE-2026-20272 を含む複数が同日アドバイザリとして公開。AI を脆弱性発見に活用する組織内ユースケースの先進事例。 *(Cisco PSIRT / THN 2026-08-05)*

- **[2026-08-05]** [Samsung Galaxy S25 Bixby/Capsule インフラを悪用した $50,000 exploit chain を Black Hat USA 2026 で開示 — Bixby を強制的に悪意ある Capsule へ誘導し機密データ窃取・システム権限取得](https://www.securityweek.com/researchers-expose-samsung-galaxy-exploit-chain-targeting-bixby-capsule-at-black-hat-usa-2026/) — Pwn2Own Ireland 2025 で実証した Samsung Galaxy S25 へのフルチェーン攻撃を Black Hat 2026 で詳細開示。Bixby AI アシスタントのインフラを悪用して悪意ある Capsule を強制実行させ、機密データ窃取からシステム権限取得まで到達。 *(SecurityWeek 2026-08-05)*

- **[2026-08-05]** [Paperclip AI エージェント管理基盤 CVE-2026-41679 に Metasploit module 公開 — 未認証 6 ステップチェーンでホスト RCE](https://www.rapid7.com/blog/post/2026/08/05/cve-2026-41679-paperclip-ai-unauthenticated-rce/) — Paperclip AI の未認証自己登録→CLI auth 自己承認→company-import 認可欠如を繋ぐ 6 ステップチェーンで任意コマンド実行が可能。Rapid7 が Metasploit module を 8/5 に公開し悪用容易性が大幅上昇。 *(THN / Rapid7 2026-08-05)*

- **[2026-08-05]** [Shieldstral 3B オープンウェイト マルチモーダル安全分類器公開 — 推論時に自然言語ポリシーを受け取りテキスト・画像の安全評価を統合](https://huggingface.co/shieldstral/Shieldstral-3B) — 3B パラメータの open-weights 安全分類器で、自然言語で記述したセキュリティポリシーを推論時に受け取ってテキストと画像を統合評価できる構造。既存の固定ラベル分類器と比べポリシーの動的変更が可能。 *(AI Flash Report 2026-08-05)*

---

## セキュリティ関連ニュース

- **[2026-08-05]** [Forescout、TP-Link Omada ZTP エコシステムに 15 脆弱性チェーンを発見・Black Hat USA 2026 で開示 — ハードコード秘密鍵・TLS 証明書・予測可能 RC4 鍵等がチェーンでネットワーク完全掌握・RCE に繋がる](https://www.forescout.com/research-labs/tp-link-omada/) — Forescout が TP-Link Omada のゼロタッチプロビジョニング (ZTP) エコシステムに 15 件の脆弱性を発見し Black Hat でフルチェーン攻撃を実演。ハードコードされた秘密鍵・TLS 証明書・予測可能な RC4 セッション鍵等を組み合わせることで同一 VLAN の攻撃者がコントローラーおよびアクセスポイントを完全掌握できることを実証。 *(Help Net Security / BleepingComputer 2026-08-05)*

- **[2026-08-04〜05]** [Apple WebKit の DNS prefetch・WebAuthn Related Origin・WebTransport がプロキシ設定をバイパスして実 IP を漏洩 — iCloud Private Relay・Tor on iOS が影響、Apple は秋 2026 に修正予定](https://mysk.blog/2026/08/04/apple-webkit-ip-leak/) — iOS の WebKit が DNS prefetch・WebAuthn Related Origin Requests・WebTransport の各機能を通じてシステムプロキシ設定を無視して直接通信し実 IP アドレスを漏洩することを Mysk が実証。iCloud Private Relay および Tor on iOS に影響するが、システム VPN を使用している場合は影響なし。Apple は秋 2026 の OS アップデートで修正予定と回答。 *(Mysk Blog 2026-08-04 / Malwarebytes・Slashdot 2026-08-05)*

- **[続報][2026-08-05]** [CISA が JetBrains TeamCity (CVE-2026-63077) を KEV 追加、修正期限 2026-08-08 (異例の 3 日期限) — CI/CD パイプライン全侵害リスク](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) — JetBrains TeamCity のエージェントポーリングプロトコルにおける未認証 Java デシリアライズ RCE が KEV に追加された。修正期限が KEV では異例の 3 日設定 (8/8 期限) となっており野外悪用の深刻さを示す。CI/CD 基盤を侵害するとビルドパイプライン全体へのバックドア注入が可能。 *(CISA 2026-08-05)* ※初報: 2026-07-31 digest

- **[2026-08-06]** [Cisco IMC Web UI CVE-2026-20200 の PoC「CIMCown」が GitHub 公開 — 低権限認証で root OS コマンド実行](https://github.com/cimcown/CVE-2026-20200) — Cisco Integrated Management Controller (IMC) の Web UI 入力検証不備により低権限の認証済みユーザーが root として任意 OS コマンドを実行できる CVE-2026-20200 の PoC が CIMCown として 8/6 に公開。UCS C-Series・S-Series サーバーが対象。 *(Help Net Security 2026-08-06)*

---

## 新規 CVE / Advisory (バリアントハント起点候補)

> 採用基準: 公開日 2026-08-05 以降 / 修正コミット公開済み or バグクラスが言語化可能なものを優先

| CVE / GHSA | 製品 (脆弱バージョン) | CWE / CVSS | バグクラス概要 (条件+sink+結果) | 修正コミット | 優先シグナル |
|-----------|---------------------|-----------|---------------------------------|------------|------------|
| CVE-2026-20272 | Cisco IOS XE <17.9.10 / <17.12.8 / <17.15.6 / <17.18.4a / <26.1.2 | CWE-74 / **9.8** | 権限ユーザーが細工した入力 → 特殊文字サニタイズ不備 → IOS XE プロセス内で OS コマンド実行 → 完全な RCE | IOS XE 17.9.10 / 17.12.8 / 17.15.6 / 17.18.4a / 26.1.2 ([Cisco Advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-iosxe-cmdinject-k3NKPKK9)) | CVSS 9.8 / Cisco AI 内部テスト発見 / ワークアラウンドなし / 広範デプロイ |
| CVE-2026-41679 / GHSA-68qg-g8mg-6pr7 | Paperclip AI <2026.416.0 (AI エージェント管理基盤) | CWE-862 / **9.8** | 未認証攻撃者が自己登録 → CLI auth 自己承認 → company-import 認可欠如を 6 ステップでチェーン → ホスト上で任意コマンド実行 → 完全な RCE | Paperclip AI 2026.416.0 ([Rapid7 詳細](https://www.rapid7.com/blog/post/2026/08/05/cve-2026-41679-paperclip-ai-unauthenticated-rce/)) | CVSS 9.8 / 未認証 / Metasploit module 公開 (2026-08-05) / AI エージェント基盤 |
| CVE-2026-59774 / GHSA-6v53-hr58-556r | Gitea 1.22.1〜1.27.0 | CWE-22 / **9.8** | 未認証攻撃者が Org-mode #+INCLUDE ディレクティブで `ioutil.ReadFile()` のパス制限なし読み取り → `app.ini` の INTERNAL_TOKEN 窃取 → Git hook 注入 → 任意コマンド実行 | Gitea 1.27.1 ([GHSA](https://github.com/advisories/GHSA-6v53-hr58-556r)) | CVSS 9.8 / 未認証 RCE / XBOW AI エージェント発見 / THN 2026-08-05 報道 |
| CVE-2026-66902 / GHSA-vjmh-7f4c-cx88 | Google::Auth Perl <0.06 (GCP ADC ライブラリ) | CWE-78 / **9.8** | `GOOGLE_APPLICATION_CREDENTIALS` JSON の `executable.command` を認可チェックなしに `system($cmd)` で実行 → GCP Application Default Credentials フローから任意コマンド実行 | Google::Auth Perl 0.06+ ([GHSA](https://github.com/advisories/GHSA-vjmh-7f4c-cx88)) | CVSS 9.8 / GCP Perl 環境広範影響 / ADC フロー汚染 |
| CVE-2026-20200 | Cisco IMC Web UI (UCS C-Series / S-Series) | CWE-20 / **8.8** | 低権限認証済み攻撃者が Web UI に細工した入力 → 入力検証不備 → root として任意 OS コマンド実行 → サーバー完全侵害 | Cisco 2026-08-05 advisory ([Cisco IMC Advisory](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-imc-cmdinject)) | CVSS 8.8 / PoC CIMCown 公開 (2026-08-06) / root 権限取得 / UCS 広範デプロイ |
| [続報] CVE-2026-63077 | JetBrains TeamCity <2025.11.7 / <2026.1.3 | CWE-502 / **9.8** | 未認証攻撃者がエージェントポーリングプロトコルで Java デシリアライズペイロード送信 → OSコマンド RCE → CI/CD パイプライン全侵害 | TeamCity 2025.11.7 / 2026.1.3 ([JetBrains Advisory](https://www.jetbrains.com/security/advisory/)) | CISA KEV 追加 (2026-08-05) / 期限 2026-08-08 (3 日期限) / 野外悪用確認 |

---

## 国内脆弱性・インシデント情報

> 直近 3 日間 (2026-08-05〜08-07) に JVN/JPCERT/CC/IPA で確認できた新規の国内脆弱性・インシデント公表はありませんでした。

---

<details><summary>取得状況 (デバッグ用)</summary>

- 巡回ソース数: 約 28
- 採用件数: AI=5 / Security=4 / CVE=6 / 国内=0
- 除外理由内訳:
  - 古すぎ (today-2 = 2026-08-05 より前の一次ソース):
    - Analog Devices ICS 脆弱性 (2026-07-29 一次公開)
    - VulnCheck KEV (2026-07-28)
    - FreeScout SSRF CVE-2026-24725 (2026-03 一次公開)
    - libssh2 CVE-2026-49902 (2026-06 一次公開)
    - Nuxt SSTI CVE-2026-49810 (2026-07 一次公開)
  - 重複 (直近 7 ダイジェスト掲載済み・excluded_set 参照):
    - Shai-Hulud npm worm / ChainDrop (08-05掲載)
    - White House AI Safety Meeting (08-04掲載)
    - GPUBreach NVIDIA Rowhammer (08-06掲載)
    - UK AISI Mythos 5 インシデントレポート (08-06掲載)
    - Snyk Evo COS / Black Hat Part 1・Part 2 (08-05・08-06掲載)
    - CISA KEV Langflow/Tomcat/N-central (08-06掲載)
    - Barracuda AI email PoC (08-06掲載)
    - CrowdStrike 2026 Threat Hunting Report (08-05掲載)
    - CVE-2026-18556/18577 N-central (08-04・08-06掲載)
  - 取得失敗ソース: helpnetsecurity.com / unit42.paloaltonetworks.com / jvn.jp / jpcert.or.jp / thehackernews.com / securityweek.com (403) → WebSearch スニペット・Rapid7 Blog / Mysk Blog / Cisco PSIRT / CISA / GitHub Advisory 等で代替

</details>

---

*生成: keda-digest-bot / 2026-08-07 05:08 JST*
