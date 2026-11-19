# page-viewer

KEDA Daily Digest を、スマホで読みやすい 1 ページ (Claude のアーティファクト) にするための道具置き場です。
日報そのもの (`digests/`) は `main` ブランチにあり、このブランチからは変更しません。

- `page/build.py` — 日報の Markdown と、その日の選定ファイルから HTML を作る
- `page/template.html` — ページの見た目
- `page/data/<日付>_picks.json` — その日ページに載せた項目 (厳選)
- `page/data/<日付>_bounty.json` — 「バグバウンティ・実践」欄の中身 (重複防止の履歴も兼ねる)

```
python3 -I page/build.py --digest <main の digests/.../YYYY-MM-DD_security_digest.md> \
    --picks page/data/YYYY-MM-DD_picks.json --bounty page/data/YYYY-MM-DD_bounty.json --out /tmp/index.html
```
