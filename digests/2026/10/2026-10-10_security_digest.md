# KEDA Daily Security Digest — 2026-10-10 (JST)

> 採用ウィンドウ: 2026-10-08 〜 2026-10-10 | 生成: 2026-10-10T05:16 JST

---

## AI ニュース

- **[2026-10-08] Anthropic、Cyber Mission を発表 — 重要インフラ防衛に特化した AI セキュリティ取り組み** — Accenture・Booz Allen・CrowdStrike・Deloitte・Dragos・Hitachi・Insane Cyber・Nozomi・Palo Alto Networks・PwC・Rockwell Automation の 11 社を創設パートナーとして、Critical Infrastructure Defense Program + 無償 OSS Scanner を提供開始。source: cybersecuritynews.com (2026-10-08)
- **[2026-10-08] OpenAI、GPT-6 Luna を全 ChatGPT ユーザーへ展開 — "Intelligent UI" 搭載** — インタラクティブなボタン・チャート・マップを生成できる Intelligent UI 機能付き。Free/Go プランは Luna へ、有料プランは上位モデル Sol へアップグレード。source: ghacks.net (2026-10-08)
- **[2026-10-08] [続報] 解雇された OpenAI 研究者 3 名が公開警告 — 思考連鎖モニタリング廃止への懸念** — Balesni・Korbak・Wang 各氏が「解雇は安全活動への報復」と主張。chain-of-thought monitoring の廃止がモデルの欺瞞を見逃すリスクがあると警告。OpenAI は報復を否定。source: techxplore.com (2026-10-08/09)
- **[2026-10-08] Pwn2Own Ireland 2026 最終結果 — 98 件のゼロデイ、総額 $1.262M** — Ikotas Labs が Pixel 10 チェーン ($300K) で Master of Pwn を獲得。3 チームが独立して Pixel 10 を攻略 (合計 $562,500)。source: cyberinsider.com (2026-10-08)

---

## セキュリティニュース

- **[2026-10-08] FBI + DOJ、Flax Typhoon のインフラを撤去 — 7 ドメイン押収、7 カ国 10 機関が共同勧告** — MicroScan・FishHub ツールが使われた台湾大学 20 校を含む C2 ネットワークを解体。Advisory AA26-281A 公開。source: helpnetsecurity.com (2026-10-09 報道、作戦日 2026-10-08)
- **[2026-10-09] SafePay ランサムウェア、タイの化学品製造業者からデータ窃取を主張** — サムットプラーカーン県の電気めっき用化学薬品メーカーが被害。SafePay グループがリークサイトに掲載。source: cyfirma.com weekly (2026-10-09)

---

## CVE / アドバイザリ

| CVE | 製品 | CWE | CVSS (v3.1 / v4.0) | 概要 | パッチ / 対応 |
|---|---|---|---|---|---|
| CVE-2026-107406 | Citrix NetScaler ADC/Gateway (SAML IdP/SP 構成) < 14.1-73.46 / < 13.1-64.29 | CWE-119: バッファ境界外メモリ操作 | 9.5 (Critical) | SAML 処理中のメモリオーバーフロー → RCE またはサービス停止。SAML IdP/SP として構成されている場合のみ影響。回避策なし。 | CTX697191 (2026-10-08 公開)。最新版へ即時アップデート推奨。Citrix 製品は KEV 掲載履歴あり。 |
| CVE-2026-59346 | VMware Workstation/Fusion 25H2/26H1 < 26H1u1 | CWE-190: 整数オーバーフロー | 9.3 (Critical) | VMXNET3 TSO ハンドラの整数オーバーフロー → ホスト側 vmware-vmx のヒープオーバーフロー → DoS (PoC 2026-10-08 公開)。ベンダーは潜在的 RCE の可能性も言及。 | VMSA-2026-0007 (パッチ 2026-09-03 公開済み)。PoC 公開により悪用リスク上昇。未適用の場合は早急に適用。 |

---

## 国内動向

- **[2026-10-08] [続報] 日本のウェブデータ漏洩が急増 — 2024 年以降 265 件、2026 年は 119 件** — モバイル API の悪用・API キー抽出・Metabase CVE-2026-72898 の組み合わせ攻撃が増加。7 月以降だけで 81 件。JPCERT-AT-2026-0030 (10/8 既報) の広域背景。source: thehackernews.com (2026-10-08)

---

## 参照リンク

- Anthropic Cyber Mission: https://cybersecuritynews.com/anthropic-cyber-mission/
- OpenAI GPT-6 Luna: https://ghacks.net/2026/10/08/openai-brings-gpt-6-to-all-chatgpt-users-adding-intelligent-ui
- OpenAI researchers warning: https://techxplore.com/news/2026-10-accuse-openai-chilling-safety-efforts
- Pwn2Own Ireland final: https://cyberinsider.com/google-pixel-10-hacked-as-pwn2own-ireland-wraps-with-1-26-million
- FBI Flax Typhoon advisory AA26-281A: https://helpnetsecurity.com/2026/10/09/fbi-flax-typhoon-microscan-fishhub-domains/
- Citrix CTX697191: https://support.citrix.com/article/CTX697191
- VMware VMSA-2026-0007: https://www.vmware.com/security/advisories/VMSA-2026-0007.html
- Japan web data leaks: https://thehackernews.com/2026/10/japan-sees-sharp-rise-in-web-data-leaks.html

---

*注: thehackernews.com・bleepingcomputer.com・darkreading.com・securityaffairs.com・therecord.media・cisa.gov・zerodayinitiative.com・cyfirma.com 等はプロキシによりアクセス不可。検索スニペット・複数二次ソース・GitHub Advisories・ベンダーアドバイザリ等の代替ソースを使用。*
