#!/usr/bin/env python3
"""「バグバウンティ・実践」欄を、GitHub の日報 (Markdown) にも書き込む。

使い方:
  python3 -I page/bounty_to_md.py --digest ../repo/digests/2026/11/2026-11-21_security_digest.md \
      --bounty page/data/2026-11-21_bounty.json

ページ版と同じ bounty.json から Markdown を作り、日報の末尾 (「取得状況」の折りたたみの前) に入れる。
すでに入っている場合は、目印 (<!-- bounty:start --> 〜 <!-- bounty:end -->) の間を置き換えるので、
何度実行しても 1 つだけ残る。変更があれば "updated"、無ければ "unchanged" と出力する。
"""
import argparse
import json
import os
import re
import sys

START = '<!-- bounty:start -->'
END = '<!-- bounty:end -->'


def full_date(mmdd, year, month):
    """'11/20' を '2026-11-20' にする。日報の月より先の月は前年とみなす (年またぎ)。"""
    m = re.fullmatch(r'\s*(\d{1,2})/(\d{1,2})\s*', mmdd or '')
    if not m:
        return mmdd or '日付不明'
    mo, d = int(m.group(1)), int(m.group(2))
    y = year - 1 if mo > month else year
    return f'{y:04d}-{mo:02d}-{d:02d}'


def render(bounty, year, month):
    items = bounty.get('items', [])
    picks = [i for i in items if i.get('pick')]
    others = [i for i in items if not i.get('pick')]
    out = [START, '## バグバウンティ・実践', '']
    out.append('> PortSwigger の Web Security Academy を、1 日 3 件ずつトピックの順に日本語で深掘りし、'
               '実際の報告での現れ方 (実例) を絡めて解説する欄。'
               '定期タスク「KEDA Daily Digest ページ更新」が、ページ版と同じ内容をここに追記している。')
    out.append('')
    if not picks and not others:
        out += ['> 本日は、Web Security Academy のページを開けなかったため、掲載はありません。', '']
    for it in picks:
        out.append(f"### [{full_date(it.get('date'), year, month)}] {it.get('title', '').strip()}")
        tags = it.get('tags') or []
        if tags:
            out.append('- **種類**: ' + ' / '.join(tags))
        for f in it.get('fields', []):
            text = (f.get('text') or '').strip()
            sub = f.get('sub') or []
            line = f"- **{f.get('label', '').strip()}**:"
            out.append(f'{line} {text}' if text else line)
            out += [f'  - {s.strip()}' for s in sub]
        if it.get('sources'):
            out.append(f"- 出典: {it['sources'].strip()}")
        out.append('')
    if others:
        out += ['### そのほかのライトアップ', '']
        for it in others:
            text = ' '.join((f.get('text') or '').strip() for f in it.get('fields', [])).strip()
            tags = ' / '.join(it.get('tags') or [])
            line = f"- **[{full_date(it.get('date'), year, month)}] {it.get('title', '').strip()}**"
            if tags:
                line += f' ({tags})'
            if text:
                line += f': {text}'
            if it.get('sources'):
                line += f" 出典: {it['sources'].strip()}"
            out.append(line)
        out.append('')
    out.append(END)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--digest', required=True)
    ap.add_argument('--bounty', required=True)
    args = ap.parse_args()

    m = re.match(r'(\d{4})-(\d{2})-\d{2}_', os.path.basename(args.digest))
    if not m:
        sys.exit(f'日報のファイル名から日付を読めません: {args.digest}')
    year, month = int(m.group(1)), int(m.group(2))

    with open(args.bounty, encoding='utf-8') as fh:
        bounty = json.load(fh)
    with open(args.digest, encoding='utf-8') as fh:
        original = fh.read()
    lines = original.split('\n')

    # 既存の欄を取り除く (前後の空行も 1 つにまとめる)
    if START in lines and END in lines and lines.index(START) < lines.index(END):
        a, b = lines.index(START), lines.index(END)
        lines = lines[:a] + lines[b + 1:]
        while a < len(lines) and a > 0 and lines[a] == '' and lines[a - 1] == '':
            del lines[a]

    # 入れる場所: 「取得状況」の折りたたみと、その直前の区切り線 (---) の前。無ければ末尾。
    pos = len(lines)
    for i, ln in enumerate(lines):
        if ln.startswith('<details>'):
            pos = i
            j = i - 1
            while j >= 0 and lines[j] == '':
                j -= 1
            if j >= 0 and lines[j].strip() == '---':
                pos = j
            break
    head = lines[:pos]
    tail = lines[pos:]
    while head and head[-1] == '':
        head.pop()
    while tail and tail[0] == '':
        tail.pop(0)
    block = render(bounty, year, month)
    new_lines = head + [''] + block + ['']
    if tail:
        new_lines += tail
    new = '\n'.join(new_lines)
    if not new.endswith('\n'):
        new += '\n'

    if new == original:
        print('unchanged')
        return
    with open(args.digest, 'w', encoding='utf-8') as fh:
        fh.write(new)
    n_pick = sum(1 for i in bounty.get('items', []) if i.get('pick'))
    n_other = sum(1 for i in bounty.get('items', []) if not i.get('pick'))
    print(f'updated: 実践 {n_pick} 件 / そのほか {n_other} 件 -> {args.digest}')


if __name__ == '__main__':
    main()
