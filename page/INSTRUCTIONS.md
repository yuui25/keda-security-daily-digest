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
- 「実践」欄は Web Security Academy の深掘りなので、日報の項目とは重ならない。実践欄の「実例」に使った日報の項目は、他の欄でも普通に選んでよい。
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

## 3. 「バグバウンティ・実践」欄を作る (bounty): Web Security Academy の深掘り 3 件

PortSwigger の **Web Security Academy** (https://portswigger.net/web-security) の解説を、**1 日 3 件ずつ、トピックの順に** 日本語で深掘りする。各件には、その内容が実際の診断や報告でどう現れるかの **実例** を絡める。この欄がページの主役。
(2026-11-26 に本人の希望で、ライトアップ中心の欄から切り替えた。)

### 進み具合の管理

- `viewer/page/data/academy_progress.json` に、トピックの順番 (`order`)、済んだ範囲 (`done`)、次に読む場所のメモ (`next`) がある。**毎回これを読み、続きから 3 件を選ぶ。** 済んだ範囲は繰り返さない。
- 「1 件」は、Academy の解説ページ 1 枚、または長いページの中のまとまった 1〜3 節。3 件は同じトピックの続きにする。トピックの残りが 3 件に足りない日は、次のトピックの頭に進んでよい。
- 1 つのトピックでは、そのトピックの最初のページを開いて節と下位ページの並びを確かめ、ページの順に進む。ラボ (`/lab-...` のページ) は、解説ページの理解に要るときだけ読む。**ラボの解答手順は載せない。**
- `order` を最後まで終えたら、Academy の一覧 (https://portswigger.net/web-security/all-materials/detailed) で `order` に無いトピックを探して続ける。それも無ければ、PortSwigger Research (https://portswigger.net/research) の記事を新しい順に同じ形式で扱う。
- 書き終えたら `done` に今日の 3 件を足し、`next` を書き直す (手順 6 で一緒に push される)。同じ日にやり直す場合は、`done` から今日の日付の分を消してから選び直す。

### 読み方

- Academy のページは、WebSearch (`allowed_domains: ["portswigger.net"]`) でトピック名を検索し、結果に出た URL を、ページ取得のツールで開く。**本文を読めたページだけ書く。** 記憶で書かない。
- 3 件分を読めなかった日は、読めた件数だけ載せる。1 件も読めなかった日は `items` を空にし、`academy_progress.json` は進めず、最後の報告に「開けなかった」と書く。

### 実例の絡め方

- 各件に、その日の範囲の脆弱性が **実際に見つかった例** を 1〜2 個添える。**新しさは問わない** (古い報告でよい)。探す順:
  1. 今日の日報 (`repo/` の今日分) に、同じ種類の脆弱性やインシデントがあれば、それを使う。
  2. WebSearch で「<脆弱性の種類> writeup」「<種類> HackerOne report」「<種類> 脆弱性 報告」などを検索し、結果に出た URL を開いて本文を読む。日本語の記事があれば優先する。
- 実例も、**本文を読めたものだけ** 書く。読めた実例が無い件は、「実例で見ると」の欄を省く (推測や記憶で埋めない)。Medium は本文を読めないので使わない。
- 実例は「どのサービスの、どの入口で、何の確認が無かったか」を 2〜4 文で書き、その日の Academy の内容のどこに当たるかを 1 文でつなぐ。

### 書き方

- **載せるのは 3 件、すべて `pick: true`。** `pick: false` の項目は作らない。
- `date` は今日の日付 (`MM/DD`)。`title` は日本語で「何を、どう確かめる話か」が分かる 1 文にする。先頭にトピック名を付ける (例: 「アクセス制御 (2): …」)。
- 読者は診断が本業なので、入門の説明 (用語の定義だけの節) は 1 文で済ませ、**見落としやすい点と、確かめ方** に字数を使う。
- **短くまとめる。箇条書きを主にする** (本人の希望)。各箇条は「**太字の見出し**: 1〜2 文」の形にし、長い段落にしない。
- `fields` は次の順で書く。
  1. **今日の範囲**: Academy のどのページの、どの節か。`text` に 1 文。
  2. **仕組みの肝**: `text` に全体を 1 文、`sub` に 2〜4 個。なぜ起きるか、どのチェックが無いか。Academy が挙げる具体的な識別子 (ヘッダー名、パラメータ名、設定名、URL の形) は原文のまま載せる。
  3. **実例で見ると**: 上の「実例の絡め方」のとおり。実例が 1 つなら `text` に 2〜3 文、複数なら `sub` に 1 つずつ。読めた実例が無ければこの欄を省く。
  4. **自分の診断で試すこと**: `text` は空にし、`sub` に 3〜5 個。各箇条は「**何をするか**: 何を送り、何が返れば当たりか」を 1〜2 文で書く。
- `tags` は 1〜3 個 (トピック名や脆弱性の種類)。`sources` は Academy のページを先頭に、実例の出典を続ける (`[媒体名 (著者)](URL)` の形)。
- 原文の長い引用・全文翻訳はしない。自分の言葉で書く。動く攻撃コードや完全なペイロードは載せない。
- `viewer/page/data/<today>_bounty.json` に書く。書式の実例は `viewer/page/data/2026-11-26_bounty.json`。本文中の `**太字**`、`` `コード` ``、`[文字](URL)` は使える。JSON として正しいこと (`python3 -m json.tool` で確認)。

```json
{
  "id": "bb",
  "title": "バグバウンティ・実践",
  "items": [
    {
      "date": "11/26", "pick": true,
      "title": "アクセス制御 (1): …",
      "tags": ["アクセス制御", "権限昇格"],
      "fields": [
        {"label": "今日の範囲", "inline": false, "text": "…", "sub": []},
        {"label": "仕組みの肝", "inline": false, "text": "…", "sub": []},
        {"label": "実例で見ると", "inline": false, "text": "…", "sub": []},
        {"label": "自分の診断で試すこと", "inline": false, "text": "", "sub": ["…", "…"]}
      ],
      "sources": "[Web Security Academy: Access control](https://portswigger.net/web-security/access-control) / [媒体名 (著者)](https://…)"
    }
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
- 実践欄で扱った Web Security Academy のトピックと範囲、絡めた実例の取得先
- GitHub の日報に実践欄を書き込めたか
- 問題があった点 (取得できなかった巡回先、公開や push の失敗、実践欄が 0 件だった理由)
