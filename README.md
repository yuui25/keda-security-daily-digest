# 🔐 KEDA Daily Digest — セキュリティ日報

毎朝 5 時 (JST) に Claude Code の cloud routine が自動生成する、セキュリティエンジニア向けの日本語ダイジェストです。

## 概要

- **更新頻度:** 毎日 05:00 JST (cron `0 20 * * *` UTC) に自動 commit & push
- **対象読者:** 脆弱性診断・ペネトレーションテスト・ソースコード診断・CVE 追跡を本業とするセキュリティエンジニア
- **生成モデル:** Claude Opus (claude-opus-5-5)
- **採用範囲:** 公開日が当日から 2 日前までのニュース・CVE のみ。公開日は記事本文・NVD/GHSA で裏取り
- **重複排除:** 直近 7 日分のダイジェストに載った URL / CVE / GHSA は再掲しない (続報のみ `[続報]` 付きで掲載)
- **出典:** 全項目に出典 URL を付記。事実とダイジェスト側の評価は分けて記述

## 内容

各ダイジェストは以下の構成です。

| セクション | 内容 | 目安 |
|---|---|---|
| 本日のサマリ | AI 側・セキュリティ側・国内の傾向と、まず見るべき 1〜2 件 | 5〜8 行 |
| 今日の深掘り | その日最重要の 1 件を、概要 / 技術的な中身 / 背景・経緯 / なぜ今重要か / 今日できること、で解説 | 15〜30 行 |
| AI 技術・トレンド | 新モデル・料金・エージェント/MCP・研究成果・大手の戦略・国内 AI 動向 | 8〜12 件 |
| AI セキュリティ | プロンプトインジェクション、MCP の脆弱性、AI 製品自体の脆弱性、AI を使った攻撃と防御、ガイドライン更新 | 4〜8 件 |
| セキュリティニュース | 悪用中の脆弱性 (KEV)、重大インシデント、TTP、法執行、診断ツールの変化、offensive 研究。悪用観測・PoC 有無を明記 | 10〜15 件 |
| 新規 CVE / Advisory | CVE/GHSA、製品とバージョン、CWE/CVSS、条件+sink+結果のバグクラス、修正コミット、KEV/EPSS シグナルのテーブル。末尾に「今日の CVE 所感」 | 6〜12 件 |
| 日本国内のセキュリティ動向 | 国内インシデント・事故 / 注意喚起・ガイドライン・政策 / 国内製品の脆弱性 (JVN) / 国内コミュニティ・研究・イベント の 4 小見出し | 各 2〜10 件 |
| 取得状況 (折りたたみ) | 巡回ソース数、採用・除外件数、取得失敗ソース | — |

各ニュース項目は「何が起きたか」(出典に基づく事実) と「なぜ重要か」(読者視点での評価) の 2 要素で書かれます。

## 主な情報源

- **AI:** OpenAI / Anthropic / Google DeepMind / Microsoft / Meta / Amazon / xAI / 中国系各社の公式発表、arXiv、Simon Willison、Import AI、TechCrunch、ITmedia AI+、日経クロステック
- **AI セキュリティ:** Embrace The Red、HiddenLayer、Lakera、Protect AI、OWASP GenAI、MITRE ATLAS
- **セキュリティ研究:** Project Zero、GitHub Security Lab、ZDI、Trail of Bits、PortSwigger Research、watchTowr、SpecterOps、Assetnote、Horizon3
- **脅威インテリジェンス:** Mandiant、MSRC、Talos、Unit 42、CrowdStrike、SentinelLabs、The DFIR Report
- **CVE:** NVD、MITRE CVE、GitHub Advisories、OSV.dev、oss-security、CISA KEV、EPSS、nuclei-templates
- **国内:** JPCERT/CC、IPA、JVN、NISC、警察庁、金融庁、個人情報保護委員会、JC3、piyolog、Security NEXT、ScanNetSecurity、LAC、NRI セキュア、マクニカ、GMO イエラエ、Flatt Security、JSAC / SECCON / CODE BLUE

## ダイジェスト一覧

`digests/YYYY/MM/` フォルダに `YYYY-MM-DD_security_digest.md` の形式で日々蓄積されます。

## 変更履歴

- **2026-10-10:** 構成を「厚め版」に刷新 (今日の深掘り・AI セキュリティ・国内 4 小見出し・CVE 所感を追加)。生成モデルを Claude Opus に変更
- **2026-05-18:** AI + Security + CVE のコンパクト版構成 (Claude Sonnet)
- **2026-04-25:** 運用開始

## Powered by

[Claude Code](https://claude.com/claude-code) cloud routines — Anthropic
