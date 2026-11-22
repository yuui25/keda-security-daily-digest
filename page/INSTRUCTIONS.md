# ページ更新の手順書

毎朝の定期タスク「KEDA Daily Digest ページ更新」が読む手順書です。
作業場所は、タスクの指示どおりに用意した `repo/` (main。手順 7 の「実践欄の追記」以外では読むだけ) と `viewer/` (page-viewer ブランチ) です。

読者はセキュリティエンジニア 1 名 (脆弱性診断・ペネトレーションテスト・ソースコード診断が本業)。スマホで朝 5 分で読む。
**英語の記事は読めないので、原文を開かなくても中身が分かる日本語で書く。** 日報の全文は GitHub に残るので、ページは「少なく・実践寄り」にする。ページにだけあって GitHub に無い内容を作らないよう、「バグバウンティ・実践」欄は手順 7 で GitHub の日報にも同じ内容を書き込む。

## 守ること

- 記事の本文は必ず自分で読んでから書く。**本文を読めなかった記事は載せない。** 中身を推測で書かない。
- 原文の長い引用・全文翻訳はしない。自分の言葉の日本語で要点を書く。関数名・ヘッダー名・エンドポイント・設定名などの短い技術要素は原文のまま載せてよい。
- **動く攻撃コードや、そのまま使える完全なペイロードは載せない。** 書くのは「原因」「どこを見るか」「何が返れば当たりか」という診断の観点。
- 有料記事の壁を回避するミラーサイト (freedium、archive 系など) は使わない。
- 日付・CVE 番号・金額は、読んだ本文で確かめたものだけ書く。

## 1. 今日の日報を見つける

- `date -u +%Y-%m-%dT%H:%M:%SZ` で現在 UTC を取り、+9 時間した JST の日付を today とする。
- `repo/digests/<YYYY>/<MM>/<today>_security_digest.md` を探す。
- 無ければ日報タスクがまだ終わっていない可能性がある。`sleep 600` してから `git -C repo pull` を **最大 2 回** 試す。それでも無ければ、いちばん新しい日報を使い、最後の報告に「今日の日報がまだ無かったので <日付> 分で作成」と書く。
- 日報を最後まで読む。

## 2. 日報から載せる項目を選ぶ (picks)

基準は「読者が今日か今週、実際に手を動かす可能性があるか」「診断の見方が変わるか」。件数を埋めにいかない。静かな日は少なくてよい。

| 欄 (キー) | 目安 | 優先するもの |
|---|---|---|
| AI 技術 (`ai`) | 1〜2 件 | 診断・自動化・エージェントの安全性に直接関わるもの。一般的な業界ニュースや資金調達は載せない |
| AI セキュリティ (`aisec`) | 2〜3 件 | 実際の侵害、再現できる攻撃手法、広く使われる AI 基盤の欠陥 |
| セキュリティ (`sec`) | 3〜4 件 | 悪用中、PoC 公開、KEV 追加、診断先によくある製品の重大な欠陥 |
| 国内 (`jp`) | 2〜3 件 | 原因や手口が分かる国内インシデント、診断に効く国内の研究記事 |
| JVN (`jvn`) | 0〜1 件 | 特に重要なときだけ |

- **CVE 表と「今日の深掘り」の欄はページに出さない** (`"hide": ["cve", "deep"]`)。深掘りの項目は、ビルド時に自動でセキュリティ欄の先頭に普通のカードとして入るので、`sec` はそれを含めて 4〜5 件になるよう 3〜4 件を選ぶ。
- 「実践」欄に載せる記事と同じものは、他の欄で選ばない。
- `viewer/page/data/<today>_picks.json` に書く。値は **日報の見出しに実際に含まれる、他と重ならない短い文字列** (JVN は識別子の一部)。

```json
{
  "hide": ["cve", "deep"],
  "ai": ["external sandbox", "Agent Host Protocol"],
  "aisec": ["Microsoft Agent Framework", "Docker Model Runner"],
  "sec": ["nginx2root", "CISA KEV に 4 件", "Apache Roller"],
  "cve": [],
  "jp": ["KARTE", "NewsPicks"],
  "jvn": []
}
```

## 3. 「バグバウンティ・実践」欄を作る (bounty)

実際の脆弱性報告・ライトアップから、**読者が次の診断で試せる学びがあるもの** を集め、日本語で解説する。この欄がページの主役。

### 集め方

- 対象: **公開から 7 日以内** のライトアップ。`viewer/page/data/*_bounty.json` の直近 14 日分を読み、**すでに載せた URL・同じ内容の記事は載せない** (`pick` が true でも false でも既出として扱う)。 ただし **今日の日付のファイル (`<today>_bounty.json`) は既出として数えない**。同じ日にやり直す場合は、今日のファイルに載っている記事をそのまま候補に含めて作り直す。
- この環境では WebFetch が失敗することがある。その場合は `curl -sSL -m 30 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/130" <URL>` で取得する。一覧は RSS が効率的。
- **Medium (medium.com、infosecwriteups.com など) は、この環境から本文を読めない。** Medium の新着一覧は「話題の手がかり」としてだけ使ってよいが、本文が読めない限り載せない。同じ著者が個人ブログや GitHub に同じ内容を公開していれば、そちらを読んで載せる。Medium の記事を何本も開こうとして時間を使わない。
- 本文を読める取得先を優先する (全部を毎回見る必要はない。**日本語の記事があれば優先**):
  - 一覧: `https://pentester.land/writeups.json` (ライトアップの一覧)、Intigriti Bug Bytes、YesWeHack・Bugcrowd・HackerOne のブログ
  - HackerOne の公開レポート: 公開済みの番号が分かれば `https://hackerone.com/reports/<番号>.json` で本文を取得できる。WebSearch で直近に公開されたレポートを探す
  - 研究チーム: PortSwigger Research (`https://portswigger.net/research/rss`)、watchTowr Labs、Assetnote / Searchlight Cyber、Doyensec、Sonar、Synacktiv、GitHub Security Lab、ProjectDiscovery、Horizon3、Rhino Security Labs、Critical Thinking (ポッドキャストの記事)
  - 個人ブログ・GitHub のライトアップ用リポジトリ (WebSearch で「bug bounty writeup」「account takeover writeup」「IDOR writeup」などと当月を組み合わせて探す)
  - 日本語: GMO Flatt Security Blog、GMO イエラエ、Zenn (`https://zenn.dev/topics/security/feed`、`https://zenn.dev/topics/bugbounty/feed`)、はてなブログ・Qiita の脆弱性報告の記事、国内研究者の個人ブログ
  - 日報 (`repo/` の今日分) に載っている研究記事のうち、原因と確認方法まで書かれた Web アプリ・API・認証認可の話は、ここで詳しく取り上げてよい (その場合は他の欄で選ばない)
- **選ぶもの**: 本人が見つけた実例で、入口・原因・影響が追えるもの。**Web アプリ・Web API・認証認可の話を中心にする。** ロジックの欠陥、認可の不備 (IDOR など)、XSS、CSRF、SSRF、SQL インジェクション、OAuth / SSO、セッション管理、競合状態、キャッシュ、リクエストスマグリング、パスの正規化の食い違いなど、読者が Web の診断にそのまま持ち帰れる種類を優先する。
- **Web 以外の扱い**: 載せる (pick: true) のは Web の話を優先し、**Web 以外 (OS やデスクトップアプリの権限昇格、メモリ破壊、カーネル、マルウェア解析、データベース単体の RCE、モバイルの端末側の欠陥、AI エージェントの権限設定など) は、Web の良い記事が足りない日に多くても 1 件まで**。クラウドの設定、モバイルや AI/LLM アプリでも、入口が HTTP のリクエストで Web の診断に通じる話 (API の認可、SSRF、プロンプト経由の情報の持ち出しなど) は Web の話として扱ってよい。Web の記事が 1 件も無い日に、Web 以外で埋めにいかない。
- **選ばないもの**: 過去の有名な報告の焼き直し、一般論や入門解説、「Top 10 Tips」の類、CTF / TryHackMe / HackTheBox の解説、宣伝、ニュースの要約、説明と証拠 (スクリーンショットやコード) が食い違っている記事。
- 本文を読み、主張に矛盾が無いかを確かめる。怪しければ載せない。

### 書き方

- **載せる (pick: true) のは 2〜4 件。** 良いものが 1 件しか無い日は 1 件でよい。読める良い記事が 1 件も無い日は `items` を空にし、最後の報告にそう書く (無理に埋めない)。
- 各件の見出し (`title`) は日本語で「何をどうしたら何ができたか」が分かる 1 文にする。原題の直訳にしない。
- `fields` は次の 4 つをこの順で書く。読者が原文を開かなくても流れが分かる具体さで書く。
  1. **対象**: どんなサービス・機能か (伏せ字ならその旨)、報告者、分かれば報奨金や重大度。1〜2 文。
  2. **手口の肝**: 入口になったパラメータや機能、原因 (どのチェックが無かったか)。2〜4 文。
  3. **影響の広げ方**: 最初の発見からどう影響を大きくしたか (他人のデータ、権限昇格など)。前提条件や、うまくいかなかった試みがあれば書く。1〜3 文。
  4. **自分の診断で試すこと**: `text` は空にし、`sub` に 2〜3 個。「どこを探し、何を確かめ、何が返れば当たりか」の粒度で書く。
- `tags` は脆弱性の種類を短く 1〜3 個 (例: `IDOR`、`DOM XSS`、`ATO`、`Race Condition`、`SSRF`、`OAuth`、`CSPT`、`Prompt Injection`)。
- `date` は記事の公開日を `MM/DD` で。`sources` は `[媒体名 (著者)](URL)` の形。
- **その他 (pick: false) は最大 4 件。** 本文を読んだうえで、上位に入らなかったもの。見出しを日本語にし、`fields` に `{"label": "ひとことで", "inline": false, "text": "<日本語 1〜2 文で何の話か>", "sub": []}` を 1 つ入れる。
- `viewer/page/data/<today>_bounty.json` に書く。書式の実例は `viewer/page/data/2026-11-19_bounty.json` の 1 件目。本文中の `**太字**`、`` `コード` ``、`[文字](URL)` は使える。JSON として正しいこと (`python3 -m json.tool` で確認)。

```json
{
  "id": "bb",
  "title": "バグバウンティ・実践",
  "items": [
    {
      "date": "11/19", "pick": true,
      "title": "決済のリダイレクト用ページの DOM XSS から、1 クリックでアカウント乗っ取り",
      "tags": ["DOM XSS", "ATO"],
      "fields": [
        {"label": "対象", "inline": false, "text": "…", "sub": []},
        {"label": "手口の肝", "inline": false, "text": "…", "sub": []},
        {"label": "影響の広げ方", "inline": false, "text": "…", "sub": []},
        {"label": "自分の診断で試すこと", "inline": false, "text": "", "sub": ["…", "…"]}
      ],
      "sources": "[GitHub (cyrusthedev)](https://github.com/…)"
    },
    {"date": "11/19", "pick": false, "title": "…", "tags": ["CSPT"], "fields": [{"label": "ひとことで", "inline": false, "text": "…", "sub": []}], "sources": "[媒体名 (著者)](https://…)"}
  ]
}
```

## 4. ページを作る

```
cd viewer
mkdir -p /tmp/keda
python3 -I page/build.py --digest ../repo/digests/<YYYY>/<MM>/<today>_security_digest.md \
  --picks page/data/<today>_picks.json --bounty page/data/<today>_bounty.json --out /tmp/keda/index.html
```

- 出力に `UNMATCHED PICK` が出たら、その文字列が日報の見出しに一致していない。picks を直して作り直す。
- `picked:` の行で、全体が **おおむね 10〜15 件** (深掘りの 1 件は数に含まれない) になっているか確かめる。多ければ減らす。
- `page/build.py` と `page/template.html` は変更しない。エラーで動かない場合だけ、原因を最後の報告に書く。

## 5. アーティファクトを上書き公開する

- 公開先は既存のアーティファクト (slug: `c9fc14dc-c651-4fe4-bcfb-d1a589547479`、題名「KEDA Daily Digest」)。**新しいアーティファクトは作らない。** 毎朝同じリンクで最新が見られるようにするため。
- アーティファクトのツール (名前に `claude-artifacts` や `Artifact` を含む。見当たらなければ ToolSearch で `artifact publish` を探す) を使う:
  1. `get_artifact` に slug を渡し、現在の `version` を得る。
  2. `publish_files` に `files: [{"as": "index.html", "path": "/tmp/keda/index.html"}]`、`slug`、`base_version` (1 で得た version) を渡す。`title` は渡さない。get_artifact の `read` が `users` / `org` / `public` のときは `shared_live` に同じ値を渡す。
  3. conflict で断られたら、get_artifact からやり直して 1 回だけ再試行する。
- **アーティファクトのツールが無い、または公開に失敗した場合**: `/tmp/keda/index.html` を `page/latest.html` としてコピーし、次の手順で一緒に push する。最後の報告の 1 行目に「ページの公開に失敗 (理由)。page-viewer ブランチの page/latest.html に保存」と書く。

## 6. 選定データを保存する (重複防止の履歴)

```
cd viewer
git config user.email "agent@anthropic.com" && git config user.name "keda-digest-bot"
git add page/data/ && (test -f page/latest.html && git add page/latest.html || true)
git commit -m "page: <today> の選定データ"
git push origin page-viewer
```

- このブランチに push してよいのは `page/data/` (と、公開に失敗したときの `page/latest.html`) だけ。`main` への push は手順 7 の 1 回だけ。
- push が権限で断られた場合: `add_repo` というツールがあれば owner `yuui25`、repo `keda-security-daily-digest`、access `push` で呼んでから 1 回だけ再試行する。それでも駄目なら、あきらめて報告に書く。
- 競合したら `git pull --rebase origin page-viewer` してから再 push。

## 7. 日報 (GitHub の main) にも実践欄を書き込む

ページと GitHub の内容をそろえるため、手順 3 で作った実践欄を、今日の日報の Markdown にも入れる。文章は書き直さず、必ず次の道具で変換する。

```
cd viewer
python3 -I page/bounty_to_md.py --digest ../repo/digests/<YYYY>/<MM>/<today>_security_digest.md \
  --bounty page/data/<today>_bounty.json
cd ../repo
git config user.email "agent@anthropic.com" && git config user.name "keda-digest-bot"
git status --short
git add digests/<YYYY>/<MM>/<today>_security_digest.md
git commit -m "digest: <today> バグバウンティ・実践を追記"
git push origin HEAD:main
```

- 道具は、日報の末尾 (「取得状況」の折りたたみの前) に `<!-- bounty:start -->` 〜 `<!-- bounty:end -->` で囲んだ「## バグバウンティ・実践」欄を入れる。すでにあれば置き換えるので、何度実行しても 1 つだけ残る。`unchanged` と出たら commit / push は不要。
- **`main` で変更してよいのは、手順 1 で使った日報 1 ファイルの、この欄だけ。** `git status --short` にそれ以外のファイルが出たら、commit せずに原因を報告に書く。日報のほかの部分を手で直さない。`page/bounty_to_md.py` は変更しない。
- 手順 1 で「今日の日報が無く、古い日報で代用した」場合は、**この手順を飛ばす** (別の日の日報に今日の実践欄を入れない)。報告にその旨を書く。
- 実践欄が 0 件の日も実行する (「該当なし」の 1 行が入る)。
- push が競合したら `git pull --rebase origin main` してから 1 回だけ再 push。権限で断られた場合は手順 6 と同じ対処をする。force push、`--no-verify` は禁止。
- この手順は、ページの公開 (手順 5) と選定データの保存 (手順 6) のあとに行う。失敗してもページは更新済みなので、やり直さずに報告に書く。

## 8. 最後の報告 (短く)

タスクの指示に最後のメッセージの形式が書かれている場合は、そちらに従う。無ければ次だけを書く。作業経過の説明は不要。

- ページを更新できたか (どの日付の日報か)
- 載せた件数: 実践 n 件 / AI n / AI セキュリティ n / セキュリティ n / 国内 n
- 実践欄に載せたライトアップの見出し (pick: true のもの) と、その取得先
- GitHub の日報に実践欄を書き込めたか
- 問題があった点 (取得できなかった巡回先、公開や push の失敗、実践欄が 0 件だった理由)
