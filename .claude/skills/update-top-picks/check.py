#!/usr/bin/env python3
"""Verify an update-top-picks run.

Rebuilds the page, then asserts everything the builder does not assert itself.
Prints one line per failure and exits non-zero; prints OK when the run is sound.

    python3 .claude/skills/update-top-picks/check.py [--date YYYY-MM-DD] [--no-build]

--date   the run date the stamps must carry (default: today)
--no-build   check the files and the page as they stand, without rebuilding
"""
import argparse, datetime, json, os, re, subprocess, sys, tempfile

CATS = ['cleanser', 'serum', 'moisturizer', 'sunscreen', 'lipday', 'lipnight']
REGIONS = {'ph', 'intl', 'kr', 'jp'}
CATEGORIES = {'cleanser', 'serum', 'moisturizer', 'sunscreen', 'lip'}
SHAPES = {'tube', 'dropper', 'jar', 'stick'}
MONTHS = {
    'en': ['January', 'February', 'March', 'April', 'May', 'June', 'July',
           'August', 'September', 'October', 'November', 'December'],
    'tl': ['Enero', 'Pebrero', 'Marso', 'Abril', 'Mayo', 'Hunyo', 'Hulyo',
           'Agosto', 'Setyembre', 'Oktubre', 'Nobyembre', 'Disyembre'],
}
NO_PHOTO_WORDS = ('photo', 'image', 'litrato', 'larawan', 'drawn label', 'guhit')

fails, notes = [], []
def fail(msg): fails.append(msg)
def note(msg): notes.append(msg)

def month_re(lang, month_index):
    """Full month name or its three-letter start, as a whole word."""
    m = MONTHS[lang][month_index - 1]
    return re.compile(r'\b(%s|%s)\b' % (re.escape(m), re.escape(m[:3])), re.I)

def _months_alt(lang):
    ms = MONTHS[lang]
    return '(?:%s)' % '|'.join([re.escape(m) for m in ms] + [re.escape(m[:3]) for m in ms])

# A date a reader can act on: a month sitting next to a year ("12 Sep 2026", "September 2026"),
# or a fully numeric date. A bare month word is not one - Tagalog "may" is an everyday word.
DATED = {lang: re.compile(r'\b%s\b\.?,?\s*\d{0,2},?\s*(\d{4})|\d{1,2}[/-]\d{1,2}[/-](\d{4})'
                          % _months_alt(lang), re.I)
         for lang in MONTHS}


def check_build(root, run_build):
    """Rebuild and read the builder's own summary line."""
    if not run_build:
        note('build skipped (--no-build)')
        return
    r = subprocess.run([sys.executable, 'site-builder/build_site.py'], cwd=root,
                       capture_output=True, text=True)
    if r.returncode != 0:
        fail('build_site.py failed:\n' + (r.stderr.strip() or r.stdout.strip()))
        return
    line = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ''
    m = re.search(r'visible products: (\d+) \(of (\d+) defined\) \| with photo URL: (\d+) \| top picks: (\d+)', line)
    if not m:
        fail('could not read the build summary line: %r' % line)
        return
    visible, _defined, with_img, top = (int(g) for g in m.groups())
    if with_img != visible:
        fail('%d of %d visible products have no photo URL — give each one a receipted img, or '
             'explain every gap in the report' % (visible - with_img, visible))
    if top != 6:
        fail('the page rendered %d top picks, expected 6' % top)
    note(line)


def check_top_picks(root, day, month, year):
    path = os.path.join(root, 'site-builder', 'top-picks.json')
    try:
        d = json.load(open(path, encoding='utf-8'))
    except Exception as e:
        fail('top-picks.json will not parse: %s' % e)
        return
    picks = d.get('picks', d if isinstance(d, list) else [])

    for key, lang in (('updated', 'en'), ('updated_tl', 'tl')):
        s = str(d.get(key, ''))
        want = '%d %s %d' % (day, MONTHS[lang][month - 1], year)
        if not s.strip():
            fail('top-picks.json: %s is empty — stamp the run date, e.g. "%s"' % (key, want))
        elif not (re.search(r'(?<!\d)%d(?!\d)' % day, s) and month_re(lang, month).search(s)
                  and str(year) in s):
            fail('top-picks.json: %s is %r — it must carry the run date (%s)' % (key, s, want))

    got = [p.get('cat') for p in picks]
    if got != CATS:
        fail('top-picks.json: categories are %r, expected exactly %r in that order' % (got, CATS))

    for p in picks:
        cat = p.get('cat', '?')
        if not p.get('pick') or not p.get('runner'):
            fail('%s: pick and runner are both required' % cat)
        elif p['pick'] == p['runner']:
            fail('%s: pick and runner are the same product (%s)' % (cat, p['pick']))
        for field in ('why', 'rwhy', 'evidence'):
            v = p.get(field) or {}
            for lang in ('en', 'tl'):
                text = (v.get(lang) or '').strip()
                if not text:
                    fail('%s: %s.%s is empty — every text ships in both languages' % (cat, field, lang))
                    continue
                if field == 'rwhy':
                    first = next((c for c in text if c.isalpha()), '')
                    if first and first.isupper():
                        fail('%s: rwhy.%s starts upper-case (%r) — it is one lower-case clause, '
                             'so reword a leading proper noun' % (cat, lang, text[:32]))
                    if text.endswith('.'):
                        fail('%s: rwhy.%s ends with a period — the builder appends the price' % (cat, lang))
                if field == 'evidence':
                    years = {g for m in DATED[lang].finditer(text) for g in m.groups() if g}
                    if not years:
                        fail('%s: evidence.%s carries no checked-on date — write one the way the '
                             'other entries do ("checked 12 Sep 2026")' % (cat, lang))
                    elif str(year) not in years:
                        fail('%s: evidence.%s is dated %s — this run re-checks the numbers, so the '
                             'date is %d' % (cat, lang, ', '.join(sorted(years)), year))


def check_products_extra(root):
    path = os.path.join(root, 'site-builder', 'products-extra.json')
    if not os.path.exists(path):
        return
    try:
        entries = json.load(open(path, encoding='utf-8'))
    except Exception as e:
        fail('products-extra.json will not parse: %s' % e)
        return
    if not entries:
        note('products-extra.json is empty (no new or overridden products)')
        return
    for e in entries:
        pid = e.get('id', '?')
        if not re.fullmatch(r'[a-z0-9_]+', str(pid)):
            fail('products-extra.json: id %r must be lower-case letters, digits and underscores' % pid)
        for field, allowed in (('region', REGIONS), ('category', CATEGORIES), ('shape', SHAPES)):
            if field in e and e[field] not in allowed:
                fail('%s: %s is %r, expected one of %s' % (pid, field, e[field], sorted(allowed)))
        for field in ('brand', 'name'):
            if not str(e.get(field, '')).strip():
                fail('%s: %s is required' % (pid, field))
        for field in ('where', 'why', 'flag'):
            v = e.get(field) or {}
            for lang in ('en', 'tl'):
                if not str(v.get(lang, '')).strip():
                    fail('%s: %s.%s is empty — every text ships in both languages' % (pid, field, lang))
        act = e.get('actives') or {}
        for lang in ('en', 'tl'):
            items = act.get(lang)
            if not isinstance(items, list) or not items or any(not str(i).strip() for i in items):
                fail('%s: actives.%s must be a non-empty list of strings' % (pid, lang))
        img = e.get('img', '')
        if img is None:
            flag_en = ((e.get('flag') or {}).get('en') or '').lower()
            if not any(w in flag_en for w in NO_PHOTO_WORDS):
                fail('%s: img is null, so flag must say the card shows a drawn label instead' % pid)
        elif not str(img).startswith('http'):
            fail('%s: img must be a URL copied from the page you opened, or null' % pid)
        variants = e.get('variants')
        if not isinstance(variants, list) or not variants:
            fail('%s: variants needs one row per size, main size first' % pid)
        else:
            for row in variants:
                if (not isinstance(row, list) or len(row) != 5
                        or not isinstance(row[2], (int, float))
                        or any(not str(row[i]).strip() for i in (0, 1, 3, 4))):
                    fail('%s: variant %r must be [size, price text, numeric price, lasts EN, lasts TL]'
                         % (pid, row))


def check_page(root):
    path = os.path.join(root, 'index.html')
    if not os.path.exists(path):
        fail('index.html is missing — run the build')
        return
    html = open(path, encoding='utf-8').read()

    en, tl = html.count('class="l-en"'), html.count('class="l-tl"')
    if en != tl:
        fail('English blocks (%d) and Tagalog blocks (%d) are out of step' % (en, tl))

    ev = html.count('class="evidence"')
    if ev != 12:
        fail('%d evidence blocks rendered, expected 12 (six top picks in two languages)' % ev)

    if not _have('node'):
        note('node is not installed — the inline script was not syntax-checked')
        return
    blocks = [(a, b) for a, b in re.findall(r'<script\b([^>]*)>(.*?)</script>', html, re.S)
              if 'src=' not in a]
    for i, (attrs, body) in enumerate(blocks):
        ext = '.mjs' if 'module' in attrs else '.js'
        with tempfile.NamedTemporaryFile('w', suffix=ext, delete=False, encoding='utf-8') as f:
            f.write(body)
            tmp = f.name
        r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
        os.unlink(tmp)
        if r.returncode != 0:
            fail('inline script %d fails node --check:\n%s' % (i + 1, r.stderr.strip()))
    note('node --check passed on %d inline script(s)' % len(blocks))


def _have(cmd):
    return subprocess.run(['which', cmd], capture_output=True).returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--date', help='run date the stamps must carry (YYYY-MM-DD, default today)')
    ap.add_argument('--no-build', action='store_true', help='check the files as they stand')
    a = ap.parse_args()

    root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
    if not os.path.exists(os.path.join(root, 'site-builder', 'build_site.py')):
        root = os.getcwd()
    if not os.path.exists(os.path.join(root, 'site-builder', 'build_site.py')):
        print('FAIL: run this from the folder that holds index.html')
        return 1

    when = (datetime.date.fromisoformat(a.date) if a.date else datetime.date.today())
    check_build(root, not a.no_build)
    check_top_picks(root, when.day, when.month, when.year)
    check_products_extra(root)
    check_page(root)

    for n in notes:
        print('note: %s' % n)
    for f in fails:
        print('FAIL: %s' % f)
    if fails:
        print('\nFAILED (%d) — fix each one, or explain it in the report.' % len(fails))
        return 1
    print('\nOK — run date %s, six picks, both languages, page rebuilt and clean.' % when.isoformat())
    return 0


if __name__ == '__main__':
    sys.exit(main())
