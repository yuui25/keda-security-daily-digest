#!/usr/bin/env python3
"""KEDA Daily Digest の Markdown を、表示用ページのデータ (JSON) に変換し、
template.html に埋め込んで index.html を出力する。

使い方:
  python3 -I build.py --digest digests/2026/11/2026-11-19_security_digest.md \
      --picks data/2026-11-19_picks.json --bounty data/2026-11-19_bounty.json --out /tmp/index.html

picks.json  : 分野ごとに「載せる項目の見出しの一部」を並べる。hide に入れた欄 (cve / deep) はページに出さない。
bounty.json : 「バグバウンティ・実践」欄の中身 (日報の Markdown には無いので別ファイルで渡す)。
"""
import argparse
import json
import os
import re
import sys


def split_by(lines, prefix):
    """prefix で始まる見出しごとに (見出し, 本文行) に分ける。"""
    out, head, buf = [], None, []
    for ln in lines:
        if ln.startswith(prefix):
            if head is not None:
                out.append((head, buf))
            head, buf = ln[len(prefix):].strip(), []
        elif head is not None:
            buf.append(ln)
    if head is not None:
        out.append((head, buf))
    return out


def preamble(lines, prefix):
    """最初の見出しより前の行。"""
    out = []
    for ln in lines:
        if ln.startswith(prefix):
            break
        out.append(ln)
    return out


def parse_item(head, body):
    tags = []
    date, title = '', head
    m = re.match(r'\[(\d{4}-[^\]]+)\]\s*(.*)', head)
    if m:
        date = m.group(1)[5:].replace('-', '/')
        title = m.group(2)
    if '[続報]' in title:
        tags.append('続報')
        title = title.replace('[続報]', '').strip()
    if title.startswith('国内:'):
        tags.append('国内')
        title = title[3:].strip()

    fields, sources = [], ''
    for ln in body:
        if ln.startswith('- '):
            c = ln[2:].strip()
            if c.startswith('出典:'):
                sources = c[3:].strip()
                continue
            m = re.match(r'\*\*(.+?)\*\*(:?)\s*(.*)$', c)
            if m:
                fields.append({'label': m.group(1), 'inline': m.group(2) == '',
                               'text': m.group(3), 'sub': []})
            else:
                fields.append({'label': None, 'inline': True, 'text': c, 'sub': []})
        elif re.match(r'^\s{2,}- ', ln) and fields:
            fields[-1]['sub'].append(re.sub(r'^\s+- ', '', ln).strip())

    text = head + '\n' + '\n'.join(body)
    if 'KEV' in head:
        tags.append('KEV')
    if '悪用中' in head or '悪用観測あり' in text:
        tags.append('悪用中')
    if re.search(r'PoC\s*(が|は)?\s*公開(?!されていない)', text):
        tags.append('PoC公開')
    return {'date': date, 'title': title, 'tags': tags, 'fields': fields, 'sources': sources}


def parse_items(lines, prefix):
    return [parse_item(h, b) for h, b in split_by(lines, prefix)]


def parse_table(lines):
    rows = []
    for ln in lines:
        if not ln.startswith('|'):
            continue
        cells = [c.strip() for c in ln.strip().strip('|').split('|')]
        if all(re.fullmatch(r':?-+:?', c) for c in cells):
            continue
        rows.append(cells)
    return rows[1:]  # ヘッダー行を除く


def bullets(lines):
    return [ln[2:].strip() for ln in lines if ln.startswith('- ')]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--digest', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--picks')
    ap.add_argument('--bounty')
    ap.add_argument('--template', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template.html'))
    ap.add_argument('--repo-url', default='https://github.com/yuui25/keda-security-daily-digest')
    args = ap.parse_args()
    md_path, tpl_path, out_path = args.digest, args.template, args.out
    m = re.search(r'(digests/\d{4}/\d{2}/[^/]+\.md)$', md_path.replace(os.sep, '/'))
    source_url = f"{args.repo_url}/blob/main/{m.group(1)}" if m else ''
    lines = open(md_path, encoding='utf-8').read().split('\n')

    data = {'source_url': source_url}
    m = re.search(r'(\d{4}-\d{2}-\d{2})', lines[0])
    data['date'] = m.group(1) if m else ''
    data['range'] = ''
    for ln in lines[:6]:
        if ln.startswith('> 採用範囲:'):
            data['range'] = ln.split(':', 1)[1].strip()

    # 末尾のデバッグ欄を切り離す
    debug = []
    if '<details>' in '\n'.join(lines):
        idx = next(i for i, ln in enumerate(lines) if ln.startswith('<details>'))
        debug = bullets(lines[idx:])
        lines = lines[:idx]
    data['debug'] = debug

    secs = dict(split_by(lines, '## '))

    def find(key):
        for k, v in secs.items():
            if key in k:
                return v
        return []

    # サマリ
    summ = [ln for ln in find('本日のサマリ') if ln.strip() and not ln.startswith('>')]
    first = []
    rest = []
    for ln in summ:
        if ln.startswith('**今日まず見るべき'):
            body = ln.split(':', 1)[1] if ':' in ln else ln
            first = [p.strip() for p in re.split(r'\(\d+\)\s*', body) if p.strip()]
        else:
            rest.append(ln)
    data['summary'] = rest
    data['first'] = first

    # 深掘り
    deep = parse_items(find('今日の深掘り'), '### ')
    data['deep'] = deep[0] if deep else None

    # ニュース 3 セクション
    data['sections'] = []
    for sid, key, label in (('ai', 'AI 技術', 'AI 技術・トレンド'),
                            ('aisec', 'AI セキュリティ', 'AI セキュリティ'),
                            ('sec', 'セキュリティニュース', 'セキュリティニュース')):
        body = find(key)
        data['sections'].append({'id': sid, 'title': label,
                                 'items': parse_items(body, '### ')})

    # CVE
    cve_lines = find('新規 CVE')
    cves = []
    for c in parse_table(cve_lines):
        if len(c) < 6:
            continue
        sm = re.search(r'/\s*(\d+(?:\.\d+)?)', c[2])
        tags = []
        cid = c[0]
        if '[続報]' in cid:
            tags.append('続報')
            cid = cid.replace('[続報]', '').strip()
        if '悪用観測' in c[5] or 'KEV' in c[5]:
            tags.append('悪用中')
        if re.search(r'PoC.*公開', c[5]):
            tags.append('PoC公開')
        cves.append({'id': cid, 'product': c[1], 'class': c[2],
                     'score': float(sm.group(1)) if sm else None,
                     'summary': c[3], 'fix': c[4], 'signal': c[5], 'tags': tags})
    data['cves'] = cves
    notes, on = [], False
    for ln in cve_lines:
        if ln.startswith('**今日の CVE 所感'):
            on = True
        elif on and ln.startswith('- '):
            notes.append(ln[2:].strip())
    data['cve_notes'] = notes

    # 国内
    jp = []
    jvn = []
    jvn_note = ''
    for head, body in split_by(find('日本国内'), '### '):
        if 'JVN' in head:
            for c in parse_table(body):
                if len(c) >= 6:
                    jvn.append({'date': c[0][5:].replace('-', '/'), 'id': c[1], 'product': c[2],
                                'summary': c[3], 'cvss': c[4], 'link': c[5]})
            q = [ln[2:].strip() for ln in body if ln.startswith('> ')]
            jvn_note = ' '.join(q)
        else:
            jp.append({'title': head, 'items': parse_items(body, '#### ')})
    data['jp'] = jp
    data['jvn'] = jvn
    data['jvn_note'] = jvn_note

    # 厳選 (picks): 指定があれば該当だけ pick=True、無ければ全件
    picks = json.load(open(args.picks, encoding='utf-8')) if args.picks else None
    unmatched = []

    def mark(items, keys, attr):
        for it in items:
            it['pick'] = True if picks is None else any(k in it[attr] for k in keys)
        for k in keys:
            if not any(k in it[attr] for it in items):
                unmatched.append(k)

    for s in data['sections']:
        mark(s['items'], (picks or {}).get(s['id'], []), 'title')
    mark(cves, (picks or {}).get('cve', []), 'id')
    mark([it for s in jp for it in s['items']], (picks or {}).get('jp', []), 'title')
    mark(jvn, (picks or {}).get('jvn', []), 'id')

    data['hide'] = (picks or {}).get('hide', [])
    # 追加セクション (バグバウンティなど、日報の Markdown に無いもの) を先頭に入れる
    if args.bounty:
        data['sections'].insert(0, json.load(open(args.bounty, encoding='utf-8')))

    payload = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    tpl = open(tpl_path, encoding='utf-8').read()
    assert '/*DATA*/null' in tpl
    open(out_path, 'w', encoding='utf-8').write(tpl.replace('/*DATA*/null', payload))

    for k in unmatched:
        print('UNMATCHED PICK (見出しに一致なし):', k)
    np_ = lambda s: sum(1 for i in s['items'] if i.get('pick'))
    print('picked:', ' '.join(f"{s['id']}={np_(s)}" for s in data['sections']), 'jp=' + str(sum(np_(s) for s in jp)), 'jvn=' + str(sum(1 for j in jvn if j.get('pick'))))
    n = lambda s: len(s['items'])
    print('date', data['date'], '| first', len(first), '| deep', bool(data['deep']),
          '|', ' '.join(f"{s['id']}={n(s)}" for s in data['sections']),
          '| cve', len(cves), '| jp', ' '.join(str(n(s)) for s in jp), '| jvn', len(jvn))


if __name__ == '__main__':
    main()
