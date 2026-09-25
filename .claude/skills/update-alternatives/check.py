#!/usr/bin/env python3
"""Verify an update-alternatives run.

    python3 .claude/skills/update-alternatives/check.py --snapshot   # before you edit anything
    python3 .claude/skills/update-alternatives/check.py              # after: rebuild and assert

--snapshot records slots.json as it stands. The check afterwards reads that baseline to prove
the `current` slots never moved and to name the product each slot held before the run - the
"previous product" column of the report.

The plain run rebuilds the page, then asserts what the builder does not: the slot structure,
every slot's origin, price band and category, the fit rules that can be read off a card, the
entries in products-extra.json, and the rendered page. One line per failure, exit 1; OK when
the run is sound.
"""
import argparse, datetime, json, os, re, subprocess, sys, tempfile

STEPS = ['cleanse', 'serum', 'moist', 'sun', 'daylip', 'lip']
SLOTS = ['current', 'intl', 'kr', 'jp', 'ph_budget', 'intl_budget', 'kr_budget', 'jp_budget']
SLOT_REGION = {'intl': 'intl', 'kr': 'kr', 'jp': 'jp',
               'ph_budget': 'ph', 'intl_budget': 'intl', 'kr_budget': 'kr', 'jp_budget': 'jp'}
STEP_CAT = {'cleanse': 'cleanser', 'serum': 'serum', 'moist': 'moisturizer',
            'sun': 'sunscreen', 'daylip': 'lip', 'lip': 'lip'}
ORIGIN = {'ph': 'Filipino', 'intl': 'international (non-Asian brand)', 'kr': 'Korean', 'jp': 'Japanese'}
BAND = 500
REGIONS = {'ph', 'intl', 'kr', 'jp'}
CATEGORIES = {'cleanser', 'serum', 'moisturizer', 'sunscreen', 'lip'}
SHAPES = {'tube', 'dropper', 'jar', 'stick'}
NO_PHOTO_WORDS = ('photo', 'image', 'litrato', 'larawan', 'drawn label', 'guhit')
BUILD_LINE = re.compile(r'visible products: (\d+) \(of (\d+) defined\) \| '
                        r'with photo URL: (\d+) \| top picks: (\d+)')

# Rebuilds the page and hands back the product table the checks below need.
EXTRACT = r'''
import contextlib, io, json, sys
sys.path.insert(0, sys.argv[2])
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    import build_site as b
lines = [l for l in buf.getvalue().splitlines() if l.strip()]
json.dump({
    'build_line': lines[-1] if lines else '',
    'visible': list(b.VISIBLE),
    'top': sorted({p for t in b.TOP for p in (t['pick'], t['runner'])}),
    'products': {pid: {'region': b.P[pid].get('region'), 'cat': b.CAT_OF.get(pid),
                       'brand': b.P[pid].get('brand', ''), 'name': b.P[pid].get('name', ''),
                       'img': b.P[pid].get('img'), 'price': b.V[pid][0][2],
                       'actives': ' '.join(b.P[pid].get('actives', {}).get('en', [])),
                       'flag': b.P[pid].get('flag', {}).get('en', '')}
                 for pid in b.P},
}, open(sys.argv[1], 'w', encoding='utf-8'))
'''

fails, notes, moves = [], [], []
def fail(m): fails.append(m)
def note(m): notes.append(m)


def shortlist(ids, keep=10):
    return ', '.join(ids[:keep]) + (' and %d more' % (len(ids) - keep) if len(ids) > keep else '')


def load(path, label):
    try:
        return json.load(open(path, encoding='utf-8'))
    except Exception as e:
        fail('%s will not parse: %s' % (label, e))
        return None


def check_structure(slots):
    """The eight slots of the six steps, one id each, never the same id twice in a step."""
    if not isinstance(slots, dict):
        fail('slots.json must be one map per step')
        return
    missing = [s for s in STEPS if s not in slots]
    extra = [s for s in slots if s not in STEPS]
    if missing:
        fail('slots.json is missing step(s) %s - a step key that is not one of %s renders no '
             'cards at all' % (', '.join(missing), ', '.join(STEPS)))
    if extra:
        fail('slots.json has unknown step(s) %s - the steps are exactly %s'
             % (', '.join(extra), ', '.join(STEPS)))
    for step in STEPS:
        m = slots.get(step)
        if not isinstance(m, dict):
            continue
        for slot in SLOTS:
            if slot not in m:
                fail('%s: slot %r is missing - keep all eight slots present, `null` when empty'
                     % (step, slot))
        for slot, pid in m.items():
            if slot not in SLOTS:
                fail('%s: unknown slot %r' % (step, slot))
            elif not (pid is None or isinstance(pid, str)):
                fail('%s.%s is %r - one product id, or null' % (step, slot, pid))
        ids = [pid for pid in m.values() if pid]
        for pid in set(ids):
            if ids.count(pid) > 1:
                fail('%s: %s sits in %d slots of the same step - one product per slot'
                     % (step, pid, ids.count(pid)))


def run_build(root):
    """Rebuild, and return the builder's own view of the products. None when the build fails."""
    out = tempfile.NamedTemporaryFile('r', suffix='.json', delete=False, encoding='utf-8')
    out.close()
    r = subprocess.run([sys.executable, '-c', EXTRACT, out.name, os.path.join(root, 'site-builder')],
                       cwd=root, capture_output=True, text=True)
    if r.returncode != 0:
        fail('the build failed:\n' + (r.stderr.strip() or r.stdout.strip()))
        os.unlink(out.name)
        return None
    data = json.load(open(out.name, encoding='utf-8'))
    os.unlink(out.name)
    note(data['build_line'])
    m = BUILD_LINE.search(data['build_line'])
    if m:
        visible, _defined, with_img, _top = (int(g) for g in m.groups())
        if with_img != visible:
            gaps = [pid for pid in data['visible'] if not data['products'].get(pid, {}).get('img')]
            fail('%d of %d visible products carry no photo URL (%s) - give each a receipted img, '
                 'or explain every gap in the report'
                 % (visible - with_img, visible, ', '.join(gaps)))
    else:
        fail('could not read the build summary line: %r' % data['build_line'])
    return data


def check_filled(slots, data):
    """Origin, price band, category and the fit rules a card can be read for."""
    P = data['products']
    for step in STEPS:
        for slot in SLOTS:
            pid = (slots.get(step) or {}).get(slot)
            if not pid:
                if slot != 'current':
                    note('%s.%s is empty - fill it, or the report says what the research found'
                         % (step, slot))
                continue
            p = P.get(pid)
            if not p:
                fail('%s.%s: %s is not a known product id - add it to products-extra.json first'
                     % (step, slot, pid))
                continue
            label = '%s.%s (%s)' % (step, slot, pid)
            want = SLOT_REGION.get(slot)
            if want and p['region'] != want:
                fail('%s: the slot is the best %s alternative, but the brand is %s - origin is the '
                     'brand home country' % (label, ORIGIN[want], ORIGIN.get(p['region'], p['region'])))
            if p['cat'] != STEP_CAT[step]:
                fail('%s: it is a %s, and the %s step takes a %s'
                     % (label, p['cat'], step, STEP_CAT[step]))
            if slot.endswith('_budget') and p['price'] > BAND:
                if str(BAND) in (p['flag'] or ''):
                    note('%s: the main size is P%s, over the band - the card explains it, so check '
                         'the explanation still holds' % (label, p['price']))
                else:
                    fail('%s: the main size is P%s, over the P%d band - swap it, or say plainly in '
                         '`flag` which size or promo brings it under' % (label, p['price'], BAND))
            text = '%s %s' % (p['name'], p['actives'])
            if step == 'daylip' and not re.search(r'spf', text, re.I):
                fail('%s: no SPF in the name or the actives, and the daytime lip slot carries SPF - '
                     'replace it, or null the slot and say in the report what the research found'
                     % label)
            if step == 'lip' and re.search(r'\btint', text, re.I):
                fail('%s: the bedtime lip slot is a plain balm or treatment, not a tint' % label)


def check_counts(slots, data):
    """All products = the distinct ids in the slots plus the Top picks, counted independently."""
    want = {pid for m in slots.values() if isinstance(m, dict) for pid in m.values() if pid}
    want |= set(data['top'])
    got = set(data['visible'])
    if want != got:
        fail('All products holds %d products, the slots plus Top picks come to %d (only in the '
             'page: %s; only in the files: %s)'
             % (len(got), len(want), ', '.join(sorted(got - want)) or '-',
                ', '.join(sorted(want - got)) or '-'))


def check_baseline(root, here, slots):
    """The `current` slots belong to update-current-products and must come out untouched."""
    path = os.path.join(here, '.slots-before.json')
    if not os.path.exists(path):
        note('no baseline was recorded - `current` was not verified and the report has no '
             'previous-product column. Run --snapshot before editing next time.')
        return
    snap = load(path, 'the baseline') or {}
    before = snap.get('slots') or {}
    note('baseline recorded %s' % snap.get('date', '?'))
    for step in STEPS:
        b, a = (before.get(step) or {}), (slots.get(step) or {})
        if b.get('current') != a.get('current'):
            fail('%s.current went from %r to %r - `current` is the update-current-products skill\'s '
                 'slot; put it back' % (step, b.get('current'), a.get('current')))
        for slot in SLOTS:
            if slot == 'current' or b.get(slot) == a.get(slot):
                continue
            moves.append('%s.%s: %s -> %s' % (step, slot, b.get(slot) or 'empty', a.get(slot) or 'empty'))
    if not moves:
        note('no slot changed this run - every "kept" needs its receipt in the report')


def check_products_extra(root, data):
    path = os.path.join(root, 'site-builder', 'products-extra.json')
    if not os.path.exists(path):
        return
    entries = load(path, 'products-extra.json')
    if entries is None:
        return
    if not entries:
        note('products-extra.json is empty (no new or refreshed products)')
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
                    fail('%s: %s.%s is empty - every text ships in both languages' % (pid, field, lang))
        act = e.get('actives') or {}
        for lang in ('en', 'tl'):
            items = act.get(lang)
            if not isinstance(items, list) or not items or any(not str(i).strip() for i in items):
                fail('%s: actives.%s must be a non-empty list of strings' % (pid, lang))
        img = e.get('img', '')
        if img is None:
            if not any(w in ((e.get('flag') or {}).get('en') or '').lower() for w in NO_PHOTO_WORDS):
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
    if data:
        missing = [e['id'] for e in entries if e.get('id') and e['id'] not in data['visible']]
        if missing:
            note('in products-extra.json but in no slot and no Top pick, so not rendered: %s'
                 % ', '.join(missing))


def check_photos(root, slots, data):
    """get-photos.sh keeps the page working offline."""
    want = [pid for pid in data['visible'] if data['products'].get(pid, {}).get('img')]
    gone = [pid for pid in want if not os.path.exists(os.path.join(root, 'images', pid + '.jpg'))]
    if gone:
        note('%d of %d photos are not in images/ yet - run `bash get-photos.sh`, and report the '
             'ones that will not download: %s' % (len(gone), len(want), shortlist(gone)))


def check_page(root, slots, data):
    path = os.path.join(root, 'index.html')
    if not os.path.exists(path):
        fail('index.html is missing - run the build')
        return
    html = open(path, encoding='utf-8').read()

    en, tl = html.count('class="l-en"'), html.count('class="l-tl"')
    if en != tl:
        fail('English blocks (%d) and Tagalog blocks (%d) are out of step' % (en, tl))

    for pid in sorted({pid for m in slots.values() if isinstance(m, dict) for pid in m.values() if pid}):
        if 'data-pid="%s"' % pid not in html:
            fail('%s sits in a slot but no card rendered for it' % pid)

    shown = ([int(n) for n in re.findall(r'All (\d+) products', html)]
             + [int(n) for n in re.findall(r'Lahat ng (\d+) produkto', html)])
    off = [n for n in shown if n != len(data['visible'])]
    if off:
        fail('the page says %s products where %d are rendered'
             % (', '.join(str(n) for n in sorted(set(off))), len(data['visible'])))

    if subprocess.run(['which', 'node'], capture_output=True).returncode != 0:
        note('node is not installed - the inline script was not syntax-checked')
        return
    blocks = [(a, b) for a, b in re.findall(r'<script\b([^>]*)>(.*?)</script>', html, re.S)
              if 'src=' not in a]
    for i, (attrs, body) in enumerate(blocks):
        with tempfile.NamedTemporaryFile('w', suffix='.mjs' if 'module' in attrs else '.js',
                                         delete=False, encoding='utf-8') as f:
            f.write(body)
            tmp = f.name
        r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
        os.unlink(tmp)
        if r.returncode != 0:
            fail('inline script %d fails node --check:\n%s' % (i + 1, r.stderr.strip()))
    note('node --check passed on %d inline script(s)' % len(blocks))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--snapshot', action='store_true',
                    help='record slots.json as the baseline, before any edit')
    a = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, '..', '..', '..'))
    if not os.path.exists(os.path.join(root, 'site-builder', 'build_site.py')):
        root = os.getcwd()
    if not os.path.exists(os.path.join(root, 'site-builder', 'build_site.py')):
        print('FAIL: run this from the folder that holds index.html')
        return 1
    slots_path = os.path.join(root, 'site-builder', 'slots.json')
    snap_path = os.path.join(here, '.slots-before.json')

    if a.snapshot:
        slots = load(slots_path, 'slots.json')
        if slots is None:
            print('FAIL: %s' % fails[0])
            return 1
        was = json.load(open(snap_path, encoding='utf-8')).get('date') if os.path.exists(snap_path) else None
        today = datetime.date.today().isoformat()
        json.dump({'date': today, 'slots': slots}, open(snap_path, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        print('baseline recorded %s%s - research the slots now, then run this script again.'
              % (today, ' (replacing the one from %s)' % was if was else ''))
        return 0

    slots = load(slots_path, 'slots.json') or {}
    check_structure(slots)
    data = run_build(root)
    if data:
        check_filled(slots, data)
        check_counts(slots, data)
        check_photos(root, slots, data)
        check_page(root, slots, data)
    check_products_extra(root, data)
    check_baseline(root, here, slots)

    for m in moves:
        print('moved: %s' % m)
    for n in notes:
        print('note: %s' % n)
    for f in fails:
        print('FAIL: %s' % f)
    if fails:
        print('\nFAILED (%d) - fix each one, or explain it in the report.' % len(fails))
        return 1
    print('\nOK - slots sound, page rebuilt and clean.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
