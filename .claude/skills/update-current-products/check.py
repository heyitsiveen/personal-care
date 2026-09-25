#!/usr/bin/env python3
"""Verify an update-current-products run.

    python3 .claude/skills/update-current-products/check.py --snapshot   # before you edit anything
    python3 .claude/skills/update-current-products/check.py              # after: rebuild and assert

--snapshot records slots.json as it stands. The check afterwards reads that baseline to prove the
alternative slots never moved and to name the product each `current` slot held before the run -
the "old product" column of the report.

The plain run rebuilds the page, then asserts what the builder does not: the slot structure, each
current product's category and the fit rules a card can be read for, the entries in
products-extra.json, and the rendered page. It closes with the stack scan - the acids, niacinamide,
fragrance, alcohol and sunscreen filters it can see across the six current products, for step 5 of
SKILL.md to settle against the real ingredient lists. One line per failure, exit 1; OK when the run
is sound.
"""
import argparse, datetime, json, os, re, subprocess, sys, tempfile

STEPS = ['cleanse', 'serum', 'moist', 'sun', 'daylip', 'lip']
SLOTS = ['current', 'intl', 'kr', 'jp', 'ph_budget', 'intl_budget', 'kr_budget', 'jp_budget']
STEP_CAT = {'cleanse': 'cleanser', 'serum': 'serum', 'moist': 'moisturizer',
            'sun': 'sunscreen', 'daylip': 'lip', 'lip': 'lip'}
LEAVE_ON = ['serum', 'moist', 'sun', 'daylip', 'lip']       # the cleanser rinses off
CURRENT_LABEL = {'en': 'Your current product', 'tl': 'Kasalukuyang produkto mo'}
REGIONS = {'ph', 'intl', 'kr', 'jp'}
CATEGORIES = {'cleanser', 'serum', 'moisturizer', 'sunscreen', 'lip'}
SHAPES = {'tube', 'dropper', 'jar', 'stick'}
NO_PHOTO_WORDS = ('photo', 'image', 'litrato', 'larawan', 'drawn label', 'guhit')
BUILD_LINE = re.compile(r'visible products: (\d+) \(of (\d+) defined\) \| '
                        r'with photo URL: (\d+) \| top picks: (\d+)')

# The stack scan. Named ingredients only - a bare "acid" catches hyaluronic and ascorbic.
ACIDS = re.compile(r'\b(aha|bha|pha|salicylic|glycolic|lactic|mandelic)\b', re.I)
NIACINAMIDE = re.compile(r'(?:(\d+(?:\.\d+)?)\s*%\s*niacinamide|niacinamide[^.;]{0,12}?(\d+(?:\.\d+)?)\s*%)', re.I)
HAS_NIACINAMIDE = re.compile(r'niacinamide', re.I)
FRAGRANCE = re.compile(r'\b(fragrance|parfum|pabango)\b', re.I)
NO_FRAGRANCE = re.compile(r'(fragrance[- ]free|unscented|walang pabango|no fragrance)', re.I)
ALCOHOL = re.compile(r'(?<!fatty )\balcohol\b(?!-free)', re.I)
NO_ALCOHOL = re.compile(r'(alcohol[- ]free|walang alcohol|no alcohol|no drying alcohol)', re.I)
FATTY_ALCOHOL = re.compile(r'\b(cetyl|cetearyl|stearyl|behenyl|myristyl)\s+alcohol\b', re.I)
OLD_FILTERS = re.compile(r'\b(oxybenzone|benzophenone)\b', re.I)
AVOBENZONE = re.compile(r'\bavobenzone\b', re.I)
STABILISERS = re.compile(r'\b(octocrylene|tinosorb|uvinul|bemotrizinol|bisoctrizole|'
                         r'meroxyl|mexoryl|methoxycrylene)\b', re.I)
HYDRATING = re.compile(r'\b(hydrat|moistur|glycerin|hyaluronic|dewy|basa|nagpapahalumigmig)', re.I)

fails, notes, moves, stack = [], [], [], []
def fail(m): fails.append(m)
def note(m): notes.append(m)
def scan(m): stack.append(m)

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
                       'why': b.P[pid].get('why', {}).get('en', ''),
                       'flag': b.P[pid].get('flag', {}).get('en', '')}
                 for pid in b.P},
}, open(sys.argv[1], 'w', encoding='utf-8'))
'''


def shortlist(ids, keep=10):
    return ', '.join(ids[:keep]) + (' and %d more' % (len(ids) - keep) if len(ids) > keep else '')


def load(path, label):
    try:
        return json.load(open(path, encoding='utf-8'))
    except Exception as e:
        fail('%s will not parse: %s' % (label, e))
        return None


def name_of(data, pid):
    p = (data or {}).get('products', {}).get(pid)
    return '%s %s' % (p['brand'], p['name']) if p else pid


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
                where = sorted(s for s, p in m.items() if p == pid)
                fail('%s: %s sits in %s - a step never shows one card twice.%s'
                     % (step, pid, ' and '.join(where),
                        ' The product I use goes in `current`; null the alternative slot it came '
                        'from' if 'current' in where else
                        ' Both are alternative slots, so put them back as update-alternatives '
                        'left them'))


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


def check_current(slots, data):
    """Each current product against its step, and the fit rules a card can be read for."""
    P = data['products']
    for step in STEPS:
        pid = (slots.get(step) or {}).get('current')
        if not pid:
            note('%s.current is empty - the step shows alternatives only%s'
                 % (step, ', which is where the lip steps sit until I buy one'
                    if step in ('daylip', 'lip') else
                    '. Right when I stopped that step; otherwise the swap did not land'))
            continue
        p = P.get(pid)
        if not p:
            fail('%s.current: %s is not a known product id - add it to products-extra.json first'
                 % (step, pid))
            continue
        label = '%s.current (%s)' % (step, pid)
        if p['cat'] != STEP_CAT[step]:
            fail('%s: it is a %s, and the %s step takes a %s'
                 % (label, p['cat'], step, STEP_CAT[step]))
        text = '%s %s' % (p['name'], p['actives'])
        if step == 'daylip' and not re.search(r'spf', text, re.I):
            fail('%s: no SPF in the name or the actives, and the daytime lip slot carries SPF - '
                 'move it to the `lip` step, or say in the report that I use it without SPF' % label)
        if step == 'lip' and re.search(r'\btint', text, re.I):
            fail('%s: the bedtime lip slot is a plain balm or treatment, not a tint' % label)


def check_labels(slots, data, html):
    """The card must read "Your current product" in both languages, on the routine page and on
    All products - where the label comes from the product's first appearance in slot order."""
    articles = re.split(r'(?=<article )', html)
    for step in STEPS:
        pid = (slots.get(step) or {}).get('current')
        if not pid or pid not in data['products']:
            continue
        chunks = [a for a in articles if 'data-pid="%s"' % pid in a]
        if not chunks:
            fail('%s.current: %s sits in the slot but no card rendered for it' % (step, pid))
            continue
        for lang, text in CURRENT_LABEL.items():
            if not any(text in a for a in chunks):
                fail('%s.current (%s): no card reads %r - the %s card is not labelled as mine'
                     % (step, pid, text, lang))
        first = next(((s, sl) for s in STEPS for sl in SLOTS
                      if (slots.get(s) or {}).get(sl) == pid), None)
        if first and first[1] != 'current':
            note('%s.current (%s) also sits in %s.%s, which comes first in slot order, so its All '
                 'products card carries that alternative label instead of "Your current product". '
                 'Null the alternative slot, or say so in the report'
                 % (step, pid, first[0], first[1]))


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


def check_baseline(here, slots, data):
    """This skill owns `current`. Every other slot must come out of the run untouched."""
    path = os.path.join(here, '.slots-before.json')
    if not os.path.exists(path):
        note('no baseline was recorded - the alternative slots were not verified and the report '
             'has no old-product column. Run --snapshot before editing next time.')
        return
    snap = load(path, 'the baseline') or {}
    before = snap.get('slots') or {}
    note('baseline recorded %s' % snap.get('date', '?'))
    for step in STEPS:
        b, a = (before.get(step) or {}), (slots.get(step) or {})
        if b.get('current') != a.get('current'):
            moves.append('%s.current: %s -> %s'
                         % (step, b.get('current') or 'empty', a.get('current') or 'empty'))
        for slot in SLOTS:
            if slot == 'current' or b.get(slot) == a.get(slot):
                continue
            if a.get(slot) is None and b.get(slot) == a.get('current'):
                note('%s.%s was emptied because %s moved into `current` - offer to run '
                     'update-alternatives to refill it' % (step, slot, b.get(slot)))
            else:
                fail('%s.%s went from %r to %r - the alternatives belong to update-alternatives; '
                     'put it back' % (step, slot, b.get(slot), a.get(slot)))
    if not moves:
        note('no `current` slot changed this run - the swap never landed, unless I only asked for '
             'a re-check')
    elif data:
        for m in moves:
            step_slot, _, ids = m.partition(': ')
            old, _, new = ids.partition(' -> ')
            note('%s: %s -> %s' % (step_slot, name_of(data, old), name_of(data, new)))


def check_top_picks(root, slots, data):
    """A product that leaves `current` while it is a pick stays visible - and stays my problem."""
    path = os.path.join(root, 'site-builder', 'top-picks.json')
    if not os.path.exists(path) or not data:
        return
    top = load(path, 'top-picks.json') or {}
    picks = {p for t in top.get('picks', []) for p in (t.get('pick'), t.get('runner')) if p}
    current = {(slots.get(s) or {}).get('current') for s in STEPS}
    for m in moves:
        old = m.partition(': ')[2].partition(' -> ')[0]
        if old in picks and old not in current:
            note('%s is still a Top pick or runner-up and stays on that page, though I no longer '
                 'use it - say so in the report and offer update-top-picks' % name_of(data, old))
        new = m.rpartition(' -> ')[2]
        if new in picks:
            note('%s is also a Top pick or runner-up - the picks page already agrees with me'
                 % name_of(data, new))


def check_stack(slots, data):
    """What the six current products look like read together. Notes, not verdicts: the text of a
    card is thinner than an ingredient list, so step 5 settles each line against the real one."""
    P = data['products']
    members = [(step, (slots.get(step) or {}).get('current')) for step in STEPS]
    members = [(step, pid, P[pid]) for step, pid in members if pid and pid in P]
    if not members:
        scan('no current product is set - nothing to read as a stack')
        return
    text_of = {step: '%s %s %s' % (p['name'], p['actives'], p['flag']) for step, _pid, p in members}

    acid = {step: sorted({m.group(0).upper() for m in ACIDS.finditer(t)})
            for step, t in text_of.items() if ACIDS.search(t)}
    if len(acid) > 1:
        scan('acid stacking: %s - name both in the report, and which to drop or alternate'
             % '; '.join('%s carries %s' % (s, ', '.join(v)) for s, v in acid.items()))
    elif acid:
        step, v = next(iter(acid.items()))
        scan('one acid in the stack: %s carries %s - nothing is stacking on it yet, so a flag '
             'that says otherwise is out of date, and a second acid anywhere would'
             % (step, ', '.join(v)))
    else:
        scan('no exfoliating acid visible in the stack - relax any flag that still warns about '
             'acid stacking')

    load_pct, carriers = 0.0, []
    for step, t in text_of.items():
        if not HAS_NIACINAMIDE.search(t):
            continue
        pcts = sorted({float(a or b) for a, b in NIACINAMIDE.findall(t)})
        carriers.append('%s (%s)' % (step, ', '.join('%g%%' % p for p in pcts) if pcts else 'no % given'))
        load_pct += max(pcts) if pcts else 0.0
    if len(carriers) > 1:
        scan('niacinamide in %d members: %s - stated total about %g%%, and the report gives it'
             % (len(carriers), '; '.join(carriers), load_pct))
    elif carriers:
        scan('niacinamide in one member: %s' % carriers[0])

    for what, hit, clear in (('fragrance', FRAGRANCE, NO_FRAGRANCE), ('alcohol', ALCOHOL, NO_ALCOHOL)):
        flagged = [step for step in LEAVE_ON
                   if step in text_of and hit.search(text_of[step]) and not clear.search(text_of[step])
                   and not (what == 'alcohol' and FATTY_ALCOHOL.search(text_of[step])
                            and not ALCOHOL.search(FATTY_ALCOHOL.sub('', text_of[step])))]
        if len(flagged) > 1:
            scan('%s in %d leave-on members (%s) - check the ingredient lists and say in the '
                 'report whether that is too much on one face'
                 % (what, len(flagged), ', '.join(flagged)))
        elif flagged:
            scan('%s in one leave-on member (%s)' % (what, flagged[0]))
        if 'cleanse' in text_of and hit.search(text_of['cleanse']) and not clear.search(text_of['cleanse']):
            scan('%s in the cleanser too, though it rinses off' % what)

    sun = text_of.get('sun')
    if sun:
        if OLD_FILTERS.search(sun):
            scan('the sunscreen carries an older filter (%s) - weigh it against a long daylight '
                 'stretch in the report' % ', '.join(sorted({m.group(0).lower() for m in OLD_FILTERS.finditer(sun)})))
        elif AVOBENZONE.search(sun) and not STABILISERS.search(sun):
            scan('the sunscreen carries avobenzone with no stabiliser named - confirm against the '
                 'ingredient list before calling it photostable')
        if 'moist' in text_of:
            scan('wake-up moisturizer: it stays optional while the sunscreen is hydrating%s'
                 % ('' if HYDRATING.search(sun) else
                    ' - and nothing in the sunscreen\'s card says it is, so say in the report '
                    'whether the step is still skippable'))
    else:
        scan('no sunscreen is set - the wake-up moisturizer stops being optional')


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


def check_photos(root, data):
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

    check_labels(slots, data, html)

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
        print('baseline recorded %s%s - confirm the product with me, research it, then run this '
              'script again.' % (today, ' (replacing the one from %s)' % was if was else ''))
        return 0

    slots = load(slots_path, 'slots.json') or {}
    check_structure(slots)
    data = run_build(root)
    if data:
        check_current(slots, data)
        check_counts(slots, data)
        check_photos(root, data)
        check_page(root, slots, data)
        check_stack(slots, data)
    check_products_extra(root, data)
    check_baseline(here, slots, data)
    check_top_picks(root, slots, data)

    for m in moves:
        print('moved: %s' % m)
    for s in stack:
        print('stack: %s' % s)
    for n in notes:
        print('note: %s' % n)
    for f in fails:
        print('FAIL: %s' % f)
    if fails:
        print('\nFAILED (%d) - fix each one, or explain it in the report.' % len(fails))
        return 1
    print('\nOK - the stack is sound, page rebuilt and clean.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
