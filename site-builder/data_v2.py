# -*- coding: utf-8 -*-
"""Single-page build: skincare-routine.html (EN + TL in one file) + images + fetch script + zip."""
import os, re, html, shutil, zipfile

# ---- reuse the data model from build.py (everything before the CSS section)
import os as _os
_HERE = globals().get('HERE') or _os.path.dirname(_os.path.abspath(globals().get('__file__', '.')))
exec(open(_os.path.join(_HERE, 'data_base.py'), encoding='utf-8').read())

# ---- data updates -----------------------------------------------------------------
P['dermorepubliq'].update(
    img='https://medias.watsons.com.ph/publishing/WTCPH-50058805-front-zoom.jpg?version=1776455434',
    price={'en': '₱299 (30 ml)', 'tl': '₱299 (30 ml)'},
    where={'en': 'Watsons (in store and online), DermoRepubliq’s official Shopee and Lazada stores',
           'tl': 'Watsons (tindahan at online), official Shopee at Lazada store ng DermoRepubliq'})
P['klued'].update(price={'en': 'About ₱300–350 (120 ml), brand store price; approximate', 'tl': 'Mga ₱300–350 (120 ml), presyo sa brand store; tantiya'})
P['camou'].update(price={'en': 'About ₱350–400 (50 g), brand store price; approximate. Other Camou items are at Watsons but this one is not listed there.',
                         'tl': 'Mga ₱350–400 (50 g), presyo sa brand store; tantiya. Nasa Watsons ang ibang Camou pero hindi nakalista ito doon.'})
P['hikari'].update(price={'en': 'About ₱300–400 (50 ml), brand store price; approximate', 'tl': 'Mga ₱300–400 (50 ml), presyo sa brand store; tantiya'})

SIZE = {'klued': '120 ml', 'cerave': '88 ml, 236 ml or 473 ml', 'cosrx': '150 ml (also 50 ml)', 'senka': '120 g (also 50 g)',
        'dermorepubliq': '30 ml', 'ordinary': '30 ml (also 60 ml)', 'anua': '30 ml', 'melanocc': '20 ml',
        'camou': '50 g', 'neutrogena': '50 g', 'skin1004': '75 ml', 'hadalabo': '50 g (14 g trial)',
        'hikari': '50 ml', 'lrp': '50 ml', 'boj': '50 ml', 'biore': '50 g (also 15 g, 85 g)',
        'vaseline': '4.8 g stick', 'mediheal': '10 ml tube', 'dhc': '1.5 g stick'}
LASTS = {
 'klued': ('about 2 months at twice a day (roughly 1 ml per wash)', 'mga 2 buwan kung dalawang beses kada araw (mga 1 ml kada hugas)'),
 'cerave': ('88 ml lasts about 6 weeks; 236 ml about 3½–4 months; 473 ml 7–8 months', 'mga 6 linggo ang 88 ml; 3½–4 buwan ang 236 ml; 7–8 buwan ang 473 ml'),
 'cosrx': ('about 2½ months at twice a day', 'mga 2½ buwan kung dalawang beses kada araw'),
 'senka': ('about 2 months (a 2 cm strip is roughly 1 g); the 50 g tube lasts 3–4 weeks', 'mga 2 buwan (mga 1 g ang 2 cm); 3–4 linggo ang 50 g'),
 'dermorepubliq': ('about 3–4 months at 2–3 drops twice a day', 'mga 3–4 buwan kung 2–3 patak dalawang beses kada araw'),
 'ordinary': ('30 ml lasts about 3–4 months; 60 ml about 7 months', 'mga 3–4 buwan ang 30 ml; mga 7 buwan ang 60 ml'),
 'anua': ('about 3–4 months at 2–3 drops twice a day', 'mga 3–4 buwan kung 2–3 patak dalawang beses kada araw'),
 'melanocc': ('about 2–3 months; you only use a pea or a dab', 'mga 2–3 buwan; kasinlaki ng gisantes o dab lang ang gamit'),
 'camou': ('about 5–7 weeks at a pea-to-blueberry amount twice a day', 'mga 5–7 linggo kung gisantes-hanggang-blueberry dalawang beses kada araw'),
 'neutrogena': ('about 5–7 weeks; the refill pack costs less for the same 50 g', 'mga 5–7 linggo; mas mura ang refill pack para sa parehong 50 g'),
 'skin1004': ('about 2–2½ months; a pea is enough on oily nights', 'mga 2–2½ buwan; sapat na ang kasinlaki ng gisantes sa oily na gabi'),
 'hadalabo': ('about 5–7 weeks; the 14 g trial is about 2 weeks', 'mga 5–7 linggo; mga 2 linggo ang 14 g trial'),
 'hikari': ('5–8 weeks if you apply a ¼ teaspoon every daylight day; days with no daylight stretch it further', '5–8 linggo kung ¼ kutsarita kada araw na may araw; mas tumatagal kung may mga araw na walang daylight'),
 'lrp': ('5–8 weeks at a ¼ teaspoon per daylight day', '5–8 linggo kung ¼ kutsarita kada araw na may araw'),
 'boj': ('5–8 weeks at a ¼ teaspoon per daylight day', '5–8 linggo kung ¼ kutsarita kada araw na may araw'),
 'biore': ('50 g lasts 5–8 weeks; the 85 g about 3 months; the 15 g is a 2-week travel size', '5–8 linggo ang 50 g; mga 3 buwan ang 85 g; 2 linggo ang 15 g na travel size'),
 'vaseline': ('about 6–8 weeks with a thick layer every bedtime', 'mga 6–8 linggo kung makapal na layer bawat pagtulog'),
 'mediheal': ('about 5–7 weeks with a thick layer every bedtime', 'mga 5–7 linggo kung makapal na layer bawat pagtulog'),
 'dhc': ('about 1½–2 months of nightly use; a little goes far', 'mga 1½–2 buwan kung gabi-gabi; kaunti lang ang kailangan'),
}
CAT_OF = {'klued': 'cleanser', 'cerave': 'cleanser', 'cosrx': 'cleanser', 'senka': 'cleanser',
          'dermorepubliq': 'serum', 'ordinary': 'serum', 'anua': 'serum', 'melanocc': 'serum',
          'camou': 'moisturizer', 'neutrogena': 'moisturizer', 'skin1004': 'moisturizer', 'hadalabo': 'moisturizer',
          'hikari': 'sunscreen', 'lrp': 'sunscreen', 'boj': 'sunscreen', 'biore': 'sunscreen',
          'vaseline': 'lip', 'mediheal': 'lip', 'dhc': 'lip'}
CAT_LABEL = {'cleanser': {'en': 'Cleanser', 'tl': 'Cleanser'}, 'serum': {'en': 'Serum', 'tl': 'Serum'},
             'moisturizer': {'en': 'Moisturizer', 'tl': 'Moisturizer'}, 'sunscreen': {'en': 'Sunscreen', 'tl': 'Sunscreen'},
             'lip': {'en': 'Lip treatment', 'tl': 'Lip treatment'}}
CAT_STEP = {'cleanser': {'en': 'Step 1 of both routines', 'tl': 'Step 1 ng parehong routine'},
            'serum': {'en': 'Step 2 of both routines', 'tl': 'Step 2 ng parehong routine'},
            'moisturizer': {'en': 'Step 3 of both routines', 'tl': 'Step 3 ng parehong routine'},
            'sunscreen': {'en': 'Wake-up routine, step 4 (daylight only)', 'tl': 'Routine pag-gising, step 4 (kung may araw lang)'},
            'lip': {'en': 'Before-sleep routine, step 4', 'tl': 'Routine bago matulog, step 4'}}
ORIGIN_LABEL = {'current': {'en': 'Filipino (your current)', 'tl': 'Filipino (kasalukuyan mo)'}, 'intl': {'en': 'International', 'tl': 'International'},
                'kr': {'en': 'Korean', 'tl': 'Korean'}, 'jp': {'en': 'Japanese', 'tl': 'Japanese'}}

X = {  # extra UI strings
 'en': dict(nav_routine='Routine', nav_products='All products', filter_type='Type', filter_origin='Brand origin', all='All',
            showing='Showing {n} of 19 products', size_l='Size and how long it lasts', fits_l='Where it fits',
            products_h='All 19 products', products_sub='Every product in this plan in one place. Filter by type or by where the brand comes from. Click any photo to see it full size.',
            lb_hint='Click the photo to zoom in or out. Press Esc to close.', lb_close='Close', photo_hint='Click any product photo to see it full size.',
            legend_current='Your current product', origin_ph='Filipino brands you already use'),
 'tl': dict(nav_routine='Routine', nav_products='Lahat ng produkto', filter_type='Uri', filter_origin='Pinagmulan ng brand', all='Lahat',
            showing='Ipinapakita ang {n} sa 19 na produkto', size_l='Laki at gaano katagal', fits_l='Saan ito ginagamit',
            products_h='Lahat ng 19 produkto', products_sub='Lahat ng produkto sa planong ito sa isang lugar. I-filter ayon sa uri o sa pinagmulan ng brand. I-click ang larawan para makita ito sa buong laki.',
            lb_hint='I-click ang larawan para mag-zoom in o out. Pindutin ang Esc para isara.', lb_close='Isara', photo_hint='I-click ang larawan ng produkto para makita ito sa buong laki.',
            legend_current='Kasalukuyang produkto mo', origin_ph='Mga Filipino brand na gamit mo na'),
}
for k in UI: UI[k].update(X[k])
UI['en']['title'] = 'Your personal care routine, built around when you actually wake up and sleep'
UI['en']['img_note'] = 'Product photos: run get-photos.sh once to store the real photos in this folder; until then the drawn labels are shown.'
UI['tl']['img_note'] = 'Larawan ng produkto: patakbuhin ang get-photos.sh nang isang beses para maimbak ang totoong larawan sa folder na ito; hanggang doon, ang iginuhit na label ang ipinapakita.'
UI['en']['notes'][2] = 'Product photos load from the retailers’ websites when you are online; run get-photos.sh once to keep offline copies in the images folder. Where a photo is missing, a drawn label of the product is shown instead.'
UI['tl']['notes'][2] = 'Nagmumula sa mga website ng retailer ang mga larawan kung online ka; patakbuhin ang get-photos.sh nang isang beses para magkaroon ng offline na kopya sa images folder. Kung walang larawan, iginuhit na label ng produkto ang ipapakita.'

# ---- illustration with the full label ----------------------------------------------
def wrap(text, width=26):
    words, lines, cur = text.split(), [], ''
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur); cur = w
        else:
            cur = (cur + ' ' + w).strip()
    if cur: lines.append(cur)
    return lines[:4]

def placeholder_svg(pid):
    p = P[pid]; c = REGION_COLOR[p['region']]; kind = CATEGORY[pid]
    if kind == 'tube':
        shape = (f'<polygon points="215,118 385,118 375,140 225,140" fill="{c}" opacity=".9"/>'
                 f'<rect x="212" y="136" width="176" height="196" rx="30" fill="{c}"/>'
                 f'<rect x="246" y="326" width="108" height="46" rx="10" fill="{c}" opacity=".75"/>'
                 f'<rect x="236" y="184" width="128" height="96" rx="12" fill="#fff" opacity=".85"/>')
    elif kind == 'dropper':
        shape = (f'<ellipse cx="300" cy="112" rx="34" ry="28" fill="{c}" opacity=".9"/>'
                 f'<rect x="268" y="132" width="64" height="48" rx="8" fill="{c}" opacity=".75"/>'
                 f'<rect x="222" y="172" width="156" height="184" rx="24" fill="{c}"/>'
                 f'<rect x="244" y="214" width="112" height="98" rx="12" fill="#fff" opacity=".85"/>')
    elif kind == 'jar':
        shape = (f'<rect x="178" y="128" width="244" height="56" rx="16" fill="{c}" opacity=".75"/>'
                 f'<rect x="188" y="178" width="224" height="170" rx="32" fill="{c}"/>'
                 f'<rect x="216" y="220" width="168" height="86" rx="12" fill="#fff" opacity=".85"/>')
    else:
        shape = (f'<rect x="254" y="110" width="92" height="76" rx="16" fill="{c}" opacity=".75"/>'
                 f'<rect x="262" y="180" width="76" height="180" rx="16" fill="{c}"/>'
                 f'<rect x="276" y="228" width="48" height="92" rx="10" fill="#fff" opacity=".85"/>')
    brand = p['brand'].split(' (')[0]
    name_lines = wrap(p['name'], 26)
    y = 396
    txt = f'<text x="300" y="{y}" text-anchor="middle" font-family="Fraunces,Georgia,serif" font-size="44" font-weight="600" fill="#14323A">{E(brand)}</text>'
    y += 40
    for ln in name_lines:
        txt += f'<text x="300" y="{y}" text-anchor="middle" font-family="Instrument Sans,Helvetica,Arial,sans-serif" font-size="27" fill="#14323A">{E(ln)}</text>'
        y += 33
    txt += f'<text x="300" y="{y + 6}" text-anchor="middle" font-family="Instrument Sans,Helvetica,Arial,sans-serif" font-size="22" fill="#4C656C">{E(SIZE[pid])}</text>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">'
            f'<rect width="600" height="600" fill="#F3F6F5"/>'
            f'<g transform="translate(300,180) scale(0.92) translate(-300,-225)">{shape}</g>{txt}</svg>')

# ---- CSS / JS ---------------------------------------------------------------------
CSS = r"""
:root{--paper:#F3F6F5;--card:#FFFFFF;--ink:#14323A;--ink-2:#4C656C;--line:#D4DEDC;--day:#FCE9AE;--day-bg:#FFF8E7;--day-2:#A96F12;
--dusk:#D7DFF3;--dusk-bg:#EEF1FA;--dusk-2:#3C5A97;--ok:#2C7A58;--ok-bg:#E8F3EE;--flag:#84467A;--flag-bg:#F6EDF4;--chip:#EEF2F1}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:"Instrument Sans",system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;font-size:17px;line-height:1.55;-webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:Fraunces,Georgia,"Times New Roman",serif;font-weight:500;letter-spacing:-0.01em;line-height:1.15;margin:0}
h1{font-size:clamp(32px,4.6vw,46px);font-weight:600;max-width:20ch} h2{font-size:clamp(28px,3.4vw,36px)} h3{font-size:24px}
p{margin:0} a{color:var(--dusk-2)}
a:focus-visible,button:focus-visible{outline:3px solid var(--dusk-2);outline-offset:3px}
button{font:inherit;color:inherit}
.wrap{max-width:960px;margin:0 auto;padding:0 22px}
html[data-lang="en"] .l-tl{display:none!important} html[data-lang="tl"] .l-en{display:none!important}
/* top bar */
.topbar{position:sticky;top:0;z-index:20;background:rgba(243,246,245,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.topbar .wrap{display:flex;align-items:center;gap:10px 18px;flex-wrap:wrap;padding-top:10px;padding-bottom:10px}
.tb-title{font-family:Fraunces,Georgia,serif;font-size:18px;font-weight:600;margin-right:auto}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:999px;background:var(--card);padding:3px}
.seg button{border:0;background:transparent;border-radius:999px;padding:6px 14px;cursor:pointer;font-size:15px;color:var(--ink-2)}
.seg button[aria-pressed="true"]{background:var(--ink);color:#fff}
/* header */
header.top{padding:34px 0 18px}
.lede{margin-top:16px;font-size:18px;color:var(--ink-2);max-width:62ch}
.tl-card{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px 18px 12px;margin:26px 0 10px}
.tl-card h3{font-size:19px;margin-bottom:6px} .tl-card svg{width:100%;height:auto;display:block}
.tl-note{font-size:14px;color:var(--ink-2);margin-top:6px}
.how{margin:34px 0 8px} .how ul{list-style:none;padding:0;margin:14px 0 0;display:grid;gap:10px}
.how li{padding:14px 16px;background:var(--card);border:1px solid var(--line);border-radius:12px} .how li b{font-weight:600}
.photohint{margin-top:14px;font-size:14px;color:var(--ink-2)}
/* routine */
section.routine{padding:44px 0 36px;margin-top:34px}
section.routine.day{background:var(--day-bg);border-top:6px solid var(--day)}
section.routine.night{background:var(--dusk-bg);border-top:6px solid var(--dusk)}
.rsub{color:var(--ink-2);margin-top:8px;max-width:64ch}
.step{margin-top:34px;display:grid;grid-template-columns:52px 1fr;gap:16px}
.num{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;font-family:Fraunces,Georgia,serif;font-size:21px;font-weight:600;color:#fff;background:var(--ink)}
.day .num{background:var(--day-2)} .night .num{background:var(--dusk-2)} .step h3{margin-top:7px}
.howto{margin-top:12px;display:grid;gap:8px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px}
.howto div{display:grid;grid-template-columns:118px 1fr;gap:12px} .howto dt{font-weight:600;color:var(--ink-2);font-size:15px;padding-top:2px} .howto dd{margin:0}
.pick{margin-top:18px;font-weight:600;font-size:15px;color:var(--ok);background:var(--ok-bg);display:inline-block;padding:6px 12px;border-radius:8px}
.cards{display:grid;gap:14px;margin-top:12px}
/* product card */
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;display:grid;grid-template-columns:150px 1fr;gap:18px}
.card.current{border-color:var(--ok);border-width:2px}
.thumb{width:150px;height:150px;border-radius:10px;background:#fff;border:1px solid var(--line);display:grid;place-items:center;overflow:hidden;position:relative;cursor:zoom-in;padding:0}
.thumb img{width:100%;height:100%;object-fit:contain;display:block}
.thumb.no-img::before{content:attr(data-initial);font-family:Fraunces,Georgia,serif;font-size:44px;font-weight:600;color:var(--ink-2)}
.region{font-size:14px;color:var(--ink-2)} .card.current .region{color:var(--ok);font-weight:600}
.pname{font-family:Fraunces,Georgia,serif;font-size:22px;line-height:1.2;margin-top:2px}
.pname small{display:block;font-family:"Instrument Sans",system-ui,sans-serif;font-size:15px;color:var(--ink-2);margin-top:2px}
.meta{margin-top:10px;display:grid;gap:6px;font-size:15px} .meta div{display:grid;grid-template-columns:128px 1fr;gap:12px}
.meta dt{color:var(--ink-2);font-weight:600} .meta dd{margin:0}
.chips{display:flex;flex-wrap:wrap;gap:6px} .chip{font-size:13px;background:var(--chip);border-radius:6px;padding:3px 8px}
.why{margin-top:10px}
.flag{margin-top:10px;padding:10px 12px 10px 14px;border-left:3px solid var(--flag);background:var(--flag-bg);border-radius:0 10px 10px 0;font-size:15.5px} .flag b{color:var(--flag)}
.compact{margin-top:12px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px} .compact p{margin-bottom:10px}
.mini{display:grid;grid-template-columns:repeat(4,1fr);gap:10px} .mini figure{margin:0;text-align:center;font-size:13px;color:var(--ink-2)}
.mini .thumb{width:100%;aspect-ratio:1/1;height:auto;margin-bottom:6px} .mini .thumb.no-img::before{font-size:26px}
.mini figure.current .thumb{border-color:var(--ok);border-width:2px} .mini figcaption b{display:block;color:var(--ink);font-weight:600}
.pimple{margin-top:30px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px} .pimple h3{font-size:20px;margin-bottom:6px}
/* glossary */
section.gloss{padding:44px 0 30px} .gsub{color:var(--ink-2);margin-top:8px;max-width:64ch}
.ggroup{margin-top:32px} .ggroup h3{font-size:22px;padding-bottom:10px;border-bottom:2px solid var(--line)}
.term{display:grid;grid-template-columns:220px 1fr;gap:16px;padding:16px 0;border-bottom:1px solid var(--line)} .term:last-child{border-bottom:0}
.term .t{font-family:Fraunces,Georgia,serif;font-size:19px;line-height:1.25} .term .d{max-width:62ch}
.found{margin-top:8px;display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-size:13px;color:var(--ink-2)}
footer{padding:30px 0 60px;color:var(--ink-2);font-size:15px} footer h3{font-size:20px;color:var(--ink);margin-bottom:10px} footer ul{padding-left:18px;margin:0;display:grid;gap:6px}
/* products view */
section.products{padding:40px 0 60px}
.filters{margin-top:20px;display:grid;gap:12px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px}
.frow{display:flex;flex-wrap:wrap;align-items:center;gap:8px} .frow .flab{font-weight:600;color:var(--ink-2);font-size:15px;min-width:118px}
.fbtn{border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 13px;cursor:pointer;font-size:15px}
.fbtn[aria-pressed="true"]{background:var(--ink);color:#fff;border-color:var(--ink)}
.count{margin-top:14px;color:var(--ink-2);font-size:15px}
.pgrid{margin-top:12px;display:grid;grid-template-columns:1fr;gap:14px}
.pgrid .card[hidden]{display:none}
/* lightbox */
.lb{position:fixed;inset:0;background:rgba(20,50,58,.86);z-index:50;display:grid;place-items:center;padding:20px}
.lb[hidden]{display:none}
.lb figure{margin:0;max-width:94vw;max-height:88vh;overflow:auto;background:#fff;border-radius:14px;padding:12px;text-align:center}
.lb img{display:block;max-width:min(88vw,900px);max-height:74vh;margin:0 auto;cursor:zoom-in}
.lb figure.zoomed img{max-width:none;max-height:none;width:1400px;cursor:zoom-out}
.lb figcaption{padding:10px 6px 2px;font-size:15px;color:var(--ink)} .lb figcaption small{display:block;color:var(--ink-2);font-size:13px;margin-top:3px}
.lb-close{position:fixed;top:14px;right:16px;border:0;background:#fff;border-radius:999px;padding:8px 14px;cursor:pointer;font-size:15px}
@media (max-width:640px){
  .card{grid-template-columns:1fr} .thumb{width:130px;height:130px}
  .howto div,.meta div{grid-template-columns:1fr;gap:2px} .term{grid-template-columns:1fr;gap:6px}
  .step{grid-template-columns:40px 1fr;gap:12px} .num{width:36px;height:36px;font-size:18px}
  .mini{grid-template-columns:repeat(2,1fr)} .tb-title{width:100%}
}
@media print{body{background:#fff} .topbar,.lb{display:none} section.routine{background:#fff;border-top-width:2px} .card,.howto,.compact{break-inside:avoid} .l-tl{display:none}}
"""

JS = r"""
(function(){
  var root=document.documentElement;
  function setLang(l){root.setAttribute('data-lang',l);document.querySelectorAll('[data-lang-btn]').forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.langBtn===l))});save();}
  function setView(v){document.querySelectorAll('[data-view]').forEach(function(s){s.hidden=(s.dataset.view!==v)});document.querySelectorAll('[data-view-btn]').forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.viewBtn===v))});save();window.scrollTo(0,0);}
  function save(){var l=root.getAttribute('data-lang');var v=document.querySelector('[data-view]:not([hidden])');history.replaceState(null,'','#'+l+'/'+(v?v.dataset.view:'routine'));}
  var h=location.hash.replace('#','').split('/');
  setLang(h[0]==='tl'?'tl':'en'); setView(h[1]==='products'?'products':'routine');
  document.querySelectorAll('[data-lang-btn]').forEach(function(b){b.addEventListener('click',function(){setLang(b.dataset.langBtn)})});
  document.querySelectorAll('[data-view-btn]').forEach(function(b){b.addEventListener('click',function(){setView(b.dataset.viewBtn)})});
  // filters
  var fcat='all',forg='all';
  function applyFilters(){document.querySelectorAll('section.products').forEach(function(sec){var n=0;sec.querySelectorAll('.pgrid .card').forEach(function(c){var show=(fcat==='all'||c.dataset.cat===fcat)&&(forg==='all'||c.dataset.origin===forg);c.hidden=!show;if(show)n++;});
    var el=sec.querySelector('.count [data-n]');if(el)el.textContent=el.dataset.tpl.replace('{n}',n);});}
  document.querySelectorAll('[data-fcat]').forEach(function(b){b.addEventListener('click',function(){fcat=b.dataset.fcat;document.querySelectorAll('[data-fcat]').forEach(function(x){x.setAttribute('aria-pressed',String(x.dataset.fcat===fcat))});applyFilters();})});
  document.querySelectorAll('[data-forg]').forEach(function(b){b.addEventListener('click',function(){forg=b.dataset.forg;document.querySelectorAll('[data-forg]').forEach(function(x){x.setAttribute('aria-pressed',String(x.dataset.forg===forg))});applyFilters();})});
  applyFilters();
  // lightbox
  var lb=document.getElementById('lb'),lbImg=document.getElementById('lb-img'),lbCap=document.getElementById('lb-cap'),fig=lb.querySelector('figure'),lastFocus=null;
  document.addEventListener('click',function(e){var t=e.target.closest('.thumb');if(!t)return;var img=t.querySelector('img');if(!img)return;lastFocus=t;lbImg.src=img.currentSrc||img.src;lbImg.alt=img.alt;lbCap.innerHTML=t.dataset.caption||img.alt;fig.classList.remove('zoomed');lb.hidden=false;document.body.style.overflow='hidden';lb.querySelector('.lb-close').focus();});
  lbImg.addEventListener('click',function(e){e.stopPropagation();fig.classList.toggle('zoomed')});
  function closeLb(){lb.hidden=true;document.body.style.overflow='';if(lastFocus)lastFocus.focus();}
  lb.addEventListener('click',function(e){if(e.target===lb||e.target.classList.contains('lb-close'))closeLb()});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!lb.hidden)closeLb()});
})();
function imgFail(img){
  var st=img.dataset.stage||'local';
  if(st==='local' && img.dataset.remote){img.dataset.stage='remote';img.src=img.dataset.remote;return;}
  if(st==='remote' && img.dataset.remote2){img.dataset.stage='remote2';img.src=img.dataset.remote2;return;}
  if(st!=='svg' && img.dataset.svg){img.dataset.stage='svg';img.src=img.dataset.svg;return;}
  img.onerror=null; var f=img.parentNode; f.classList.add('no-img'); f.setAttribute('data-initial', img.dataset.initial||'?'); img.remove();
}
"""

# ---- render helpers ---------------------------------------------------------------
def thumb(pid, lang):
    p = P[pid]
    alt = p.get('img_alt')
    alt_attr = f' data-remote2="{E(alt)}"' if alt else ''
    cap = f'<b>{E(p["brand"])}</b> {E(p["name"])}<small>{E(SIZE[pid])}</small>'
    cap = html.escape(cap, quote=True)
    return (f'<button type="button" class="thumb" data-caption="{cap}" aria-label="{E(p["brand"])} {E(p["name"])}">'
            f'<img src="images/{pid}.jpg" alt="{E(p["brand"])} {E(p["name"])}" loading="lazy" referrerpolicy="no-referrer" '
            f'data-initial="{E(p["brand"][0])}" data-remote="{E(p["img"])}"{alt_attr} data-svg="images/{pid}.svg" onerror="imgFail(this)"></button>')

def card(pid, lang, with_fit=False):
    p = P[pid]; u = UI[lang]; cat = CAT_OF[pid]
    cls = 'card current' if p['region'] == 'current' else 'card'
    chips = ''.join(f'<span class="chip">{E(a)}</span>' for a in p['actives'][lang])
    lasts = LASTS[pid][0 if lang == 'en' else 1]
    fit = f'<div><dt>{E(u["fits_l"])}</dt><dd>{E(CAT_LABEL[cat][lang])}: {E(CAT_STEP[cat][lang])}</dd></div>' if with_fit else ''
    return f'''
<article class="{cls}" data-cat="{cat}" data-origin="{p['region']}">
  {thumb(pid, lang)}
  <div>
    <div class="region">{E(u['region'][p['region']])}</div>
    <div class="pname">{E(p['brand'])} <small>{E(p['name'])}</small></div>
    <dl class="meta">
      <div><dt>{E(u['price_l'])}</dt><dd>{E(p['price'][lang])}</dd></div>
      <div><dt>{E(u['size_l'])}</dt><dd>{E(SIZE[pid])}; {E(lasts)}</dd></div>
      <div><dt>{E(u['where_l'])}</dt><dd>{E(p['where'][lang])}</dd></div>
      {fit}
      <div><dt>{E(u['actives_l'])}</dt><dd><span class="chips">{chips}</span></dd></div>
    </dl>
    <p class="why"><b>{E(u['why_l'])}.</b> {E(p['why'][lang])}</p>
    <p class="flag"><b>{E(u['flag_l'])}.</b> {E(p['flag'][lang])}</p>
  </div>
</article>'''

def howto(step, lang):
    u = UI[lang]
    rows = [(u['amount_l'], step['amount'][lang]), (u['tech_l'], step['tech'][lang]), (u['wait_l'], step['wait'][lang])]
    if step.get('skip'): rows.append((u['skip_l'], step['skip'][lang]))
    return '<dl class="howto">' + ''.join(f'<div><dt>{E(k)}</dt><dd>{E(v)}</dd></div>' for k, v in rows) + '</dl>'

def full_step(n, step, lang):
    u = UI[lang]
    pick = u['pick_one_lip'] if len(step['products']) == 3 else u['pick_one']
    return f'''<div class="step"><div class="num" aria-hidden="true">{n}</div><div>
<h3>{E(step['title'][lang])}</h3>{howto(step, lang)}<div class="pick">{E(pick)}</div>
<div class="cards">{''.join(card(pid, lang) for pid in step['products'])}</div></div></div>'''

def compact_step(n, step, lang):
    u = UI[lang]; minis = ''
    for pid in step['products']:
        p = P[pid]; c = ' class="current"' if p['region'] == 'current' else ''
        minis += f'<figure{c}>{thumb(pid, lang)}<figcaption><b>{E(p["brand"])}</b>{E(p["name"])}</figcaption></figure>'
    return f'''<div class="step"><div class="num" aria-hidden="true">{n}</div><div>
<h3>{E(step['title'][lang])}</h3><div class="compact"><p><b>{E(u['same_l'])}</b> {E(step['body'][lang])}</p><div class="mini">{minis}</div></div></div></div>'''

def timeline_svg(lang):
    u = UI[lang]
    def Xh(h): return 20 + h * 32.5
    ticks = u['tl_ticks']; tick_x = [Xh(0), Xh(5), Xh(11), Xh(17), Xh(24)]
    tick_txt = ''.join(f'<text x="{x:.1f}" y="118" text-anchor="{"start" if i==0 else ("end" if i==4 else "middle")}" class="tk">{E(t)}</text>' for i, (x, t) in enumerate(zip(tick_x, ticks)))
    return f'''<svg viewBox="0 0 820 150" role="img" aria-label="{E(u['tl_title'])}" xmlns="http://www.w3.org/2000/svg">
<style>.tk{{font-size:12px;fill:#4C656C}} .lb{{font-size:13px;fill:#14323A}} .lb2{{font-size:12px;fill:#4C656C}} .pin{{font-size:13px;font-weight:600;fill:#14323A}}</style>
<rect x="{Xh(0):.1f}" y="62" width="{Xh(5)-Xh(0):.1f}" height="30" fill="#FCE9AE"/><rect x="{Xh(5):.1f}" y="62" width="{Xh(17)-Xh(5):.1f}" height="30" fill="#D7DFF3"/><rect x="{Xh(17):.1f}" y="62" width="{Xh(24)-Xh(17):.1f}" height="30" fill="#FCE9AE"/>
<text x="{Xh(5)-8:.1f}" y="82" text-anchor="end" class="lb2">{E(u['tl_daylight'])}</text><text x="{Xh(11):.1f}" y="82" text-anchor="middle" class="lb2">{E(u['tl_night'])}</text><text x="{Xh(20.5):.1f}" y="82" text-anchor="middle" class="lb2">{E(u['tl_daylight'])}</text>
<line x1="{Xh(7):.1f}" y1="98" x2="{Xh(15):.1f}" y2="98" stroke="#14323A" stroke-width="1.5"/><text x="{Xh(11):.1f}" y="134" text-anchor="middle" class="lb">{E(u['tl_laptop'])}</text>
<line x1="{Xh(15.5):.1f}" y1="98" x2="{Xh(24):.1f}" y2="98" stroke="#14323A" stroke-width="1.5" stroke-dasharray="3 3"/><text x="{Xh(19.75):.1f}" y="134" text-anchor="middle" class="lb">{E(u['tl_sleep'])}</text>
<line x1="{Xh(1):.1f}" y1="30" x2="{Xh(1):.1f}" y2="62" stroke="#A96F12" stroke-width="2"/><circle cx="{Xh(1):.1f}" cy="77" r="7" fill="#A96F12" stroke="#fff" stroke-width="2"/><text x="{Xh(1):.1f}" y="22" text-anchor="start" class="pin">{E(u['tl_wake'])}: {E(u['tl_wakeroutine'])}</text>
<line x1="{Xh(15):.1f}" y1="30" x2="{Xh(15):.1f}" y2="62" stroke="#3C5A97" stroke-width="2"/><circle cx="{Xh(15):.1f}" cy="77" r="7" fill="#3C5A97" stroke="#fff" stroke-width="2"/><text x="{Xh(15):.1f}" y="22" text-anchor="end" class="pin">{E(u['tl_sleeproutine'])}</text>
<line x1="{Xh(17):.1f}" y1="56" x2="{Xh(17):.1f}" y2="62" stroke="#A96F12" stroke-width="1.5" stroke-dasharray="3 3"/><text x="{Xh(20.5):.1f}" y="40" text-anchor="middle" class="lb2">{E(u['tl_sunrise1'])}</text><text x="{Xh(20.5):.1f}" y="54" text-anchor="middle" class="lb2">{E(u['tl_sunrise2'])}</text>
{tick_txt}</svg>'''

def routine_block(lang):
    u = UI[lang]
    how_items = ''.join(f'<li><b>{E(a)}</b> {E(b)}</li>' for a, b in u['how'])
    wake = ''.join(full_step(i + 1, s, lang) for i, s in enumerate(WAKE))
    sleep = ''.join(compact_step(i + 1, s, lang) if s.get('compact') else full_step(i + 1, s, lang) for i, s in enumerate(SLEEP))
    gloss = ''
    for gtitle, entries in GLOSSARY:
        rows = ''
        for e in entries:
            found = ''.join(f'<span class="chip">{E(P[pid]["brand"])}</span>' for pid in e['ids'])
            rows += f'<div class="term"><div class="t">{E(e["name"][lang])}</div><div><p class="d">{E(e[lang])}</p><div class="found"><span>{E(u["found_l"])}</span>{found}</div></div></div>'
        gloss += f'<div class="ggroup"><h3>{E(gtitle[lang])}</h3>{rows}</div>'
    notes = ''.join(f'<li>{E(n)}</li>' for n in u['notes'])
    return f'''<div class="l-{lang}" lang="{lang}">
<header class="top"><div class="wrap">
<h1>{E(u['title'])}</h1><p class="lede">{E(u['intro'])}</p>
<div class="tl-card"><h3>{E(u['tl_title'])}</h3>{timeline_svg(lang)}<p class="tl-note">{E(u['tl_note'])}</p></div>
<div class="how"><h2>{E(u['how_h'])}</h2><ul>{how_items}</ul><p class="photohint">{E(u['photo_hint'])}</p></div>
</div></header>
<section class="routine day"><div class="wrap"><h2>{E(u['wake_h'])}</h2><p class="rsub">{E(u['wake_sub'])}</p>{wake}</div></section>
<section class="routine night"><div class="wrap"><h2>{E(u['sleep_h'])}</h2><p class="rsub">{E(u['sleep_sub'])}</p>{sleep}
<div class="pimple"><h3>{E(u['pimple_h'])}</h3><p>{E(u['pimple'])}</p></div></div></section>
<section class="gloss"><div class="wrap"><h2>{E(u['gloss_h'])}</h2><p class="gsub">{E(u['gloss_sub'])}</p>{gloss}</div></section>
<footer><div class="wrap"><h3>{E(u['notes_h'])}</h3><ul>{notes}</ul></div></footer>
</div>'''

def products_block(lang):
    u = UI[lang]
    cats = [('all', u['all'])] + [(c, CAT_LABEL[c][lang]) for c in ('cleanser', 'serum', 'moisturizer', 'sunscreen', 'lip')]
    origins = [('all', u['all'])] + [(o, ORIGIN_LABEL[o][lang]) for o in ('current', 'intl', 'kr', 'jp')]
    fcat = ''.join(f'<button type="button" class="fbtn" data-fcat="{c}" aria-pressed="{"true" if c=="all" else "false"}">{E(t)}</button>' for c, t in cats)
    forg = ''.join(f'<button type="button" class="fbtn" data-forg="{o}" aria-pressed="{"true" if o=="all" else "false"}">{E(t)}</button>' for o, t in origins)
    cards = ''.join(card(pid, lang, with_fit=True) for pid in P)
    return f'''<div class="l-{lang}" lang="{lang}"><section class="products"><div class="wrap">
<h2>{E(u['products_h'])}</h2><p class="gsub">{E(u['products_sub'])}</p>
<div class="filters"><div class="frow"><span class="flab">{E(u['filter_type'])}</span>{fcat}</div><div class="frow"><span class="flab">{E(u['filter_origin'])}</span>{forg}</div></div>
<p class="count"><span data-n data-tpl="{E(u['showing'])}"></span></p>
<div class="pgrid">{cards}</div>
</div></section></div>'''

def page():
    ue, ut = UI['en'], UI['tl']
    return f'''<!DOCTYPE html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Skincare routine (English + Tagalog)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<nav class="topbar"><div class="wrap">
  <div class="tb-title"><span class="l-en">Skincare routine</span><span class="l-tl">Skincare routine</span></div>
  <div class="seg" role="group" aria-label="View">
    <button type="button" data-view-btn="routine" aria-pressed="true"><span class="l-en">{E(ue['nav_routine'])}</span><span class="l-tl">{E(ut['nav_routine'])}</span></button>
    <button type="button" data-view-btn="products" aria-pressed="false"><span class="l-en">{E(ue['nav_products'])}</span><span class="l-tl">{E(ut['nav_products'])}</span></button>
  </div>
  <div class="seg" role="group" aria-label="Language">
    <button type="button" data-lang-btn="en" aria-pressed="true">English</button>
    <button type="button" data-lang-btn="tl" aria-pressed="false">Tagalog</button>
  </div>
</div></nav>
<main>
<div data-view="routine">{routine_block('en')}{routine_block('tl')}</div>
<div data-view="products" hidden>{products_block('en')}{products_block('tl')}</div>
</main>
<div class="lb" id="lb" hidden role="dialog" aria-modal="true" aria-label="Product photo">
  <button type="button" class="lb-close"><span class="l-en">{E(ue['lb_close'])}</span><span class="l-tl">{E(ut['lb_close'])}</span></button>
  <figure><img id="lb-img" alt=""><figcaption><span id="lb-cap"></span><small><span class="l-en">{E(ue['lb_hint'])}</span><span class="l-tl">{E(ut['lb_hint'])}</span></small></figcaption></figure>
</div>
<script>{JS}</script>
</body>
</html>
'''

# (output section removed: data_v2.py is only used as a data/CSS/JS source by build_site.py)
