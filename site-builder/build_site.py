# -*- coding: utf-8 -*-
import os, re, html, shutil, zipfile, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)  # the folder that holds index.html
src2 = open(os.path.join(HERE, 'data_v2.py'), encoding='utf-8').read()
ns = {'HERE': HERE}
exec(src2[:src2.index('# ---- CSS / JS')], ns)
for k in ('P','UI','WAKE','SLEEP','GLOSSARY','CATEGORY','REGION_COLOR','E','CAT_OF','CAT_LABEL','CAT_STEP','ORIGIN_LABEL','wrap'):
    globals()[k] = ns[k]

# ------------------------------------------------------------------ new products (≤ ₱500)
def prod(pid, **kw):
    kw['id'] = pid; kw.setdefault('budget', True); P[pid] = kw

prod('quickfx', brand='Quick FX', name='Pimple Eraser Facial Gel Cleanser', region='ph',
     img='https://medias.watsons.com.ph/publishing/WTCPH-50046791-front-zoom.jpg?version=1734328302',
     where={'en': 'Watsons (in store and online); Quick FX official Shopee and Lazada stores', 'tl': 'Watsons (tindahan at online); official Shopee at Lazada store ng Quick FX'},
     actives={'en': ['Salicylic acid (BHA)', 'Glycolic acid (AHA)', 'Niacinamide', 'Tea tree oil', 'Aloe', 'Allantoin', 'Ethyl ascorbic acid (vitamin C)'],
              'tl': ['Salicylic acid (BHA)', 'Glycolic acid (AHA)', 'Niacinamide', 'Tea tree oil', 'Aloe', 'Allantoin', 'Ethyl ascorbic acid (vitamin C)']},
     why={'en': 'A Filipino brand and Watsons’ best-selling Quick FX cleanser: BHA to clear pores, a touch of AHA to smooth, niacinamide and tea tree to calm. The 75 ml has close to 200 Watsons reviews.',
          'tl': 'Filipino brand at pinakamabiling Quick FX cleanser sa Watsons: BHA para linisin ang pores, kaunting AHA para pakinisin, niacinamide at tea tree para pakalmahin. Halos 200 review sa Watsons ang 75 ml.'},
     flag={'en': 'Contains glycolic acid, which can raise sun sensitivity, so keep the sunscreen step on daylight days. Acids twice a day plus a 10% niacinamide serum is a lot for a beginner: start with once a day and stop if your skin feels raw.',
           'tl': 'May glycolic acid, na puwedeng magpa-sensitive sa araw, kaya panatilihin ang sunscreen step sa mga araw na may araw. Sobra para sa beginner ang acids dalawang beses kada araw kasama ng 10% niacinamide serum: magsimula sa isang beses kada araw at itigil kung maging hilaw ang balat.'})

prod('simple', brand='Simple', name='Kind to Skin Refreshing Facial Wash Gel', region='intl',
     img='https://medias.watsons.com.sg/publishing/WTCSG-40033-front-zoom.jpg?version=1729492191', img_alt='https://medias.watsons.com.ph/publishing/WTCPH-50052710-front-zoom.jpg?version=1756223458',
     where={'en': 'Watsons (in store and online), Mercury Drug, supermarkets', 'tl': 'Watsons (tindahan at online), Mercury Drug, mga supermarket'},
     actives={'en': ['Panthenol (pro-vitamin B5)', 'Vitamin E', 'Glycerin', 'No perfume, no colour, soap-free'], 'tl': ['Panthenol (pro-vitamin B5)', 'Vitamin E', 'Glycerin', 'Walang pabango, walang kulay, soap-free']},
     why={'en': 'The cheapest sensible pick in this step: a UK pharmacy staple for decades, fragrance-free and soap-free, so it rinses clean without tightness.',
          'tl': 'Pinakamurang matinong pili sa step na ito: dekada nang staple sa mga botika sa UK, walang pabango at soap-free, kaya malinis ang banlaw nang hindi masikip.'},
     flag={'en': 'No oil-control actives at all. If you want more grip on oil, Simple’s Daily Skin Detox Purifying Gel Wash (₱299) is the oily-skin variant of the same range.',
           'tl': 'Wala itong kahit anong aktibong sangkap para sa langis. Kung gusto mo ng mas malakas sa langis, ang Simple Daily Skin Detox Purifying Gel Wash (₱299) ang bersyon para sa oily na balat.'})

prod('somebymi', brand='Some By Mi', name='AHA·BHA·PHA 30 Days Miracle Acne Clear Foam', region='kr',
     img='https://medias.watsons.com.ph/publishing/SOME%20BY%20MI_Image%201_50053132-33HThwGl-zoom.jpg?version=1764235822',
     where={'en': 'Watsons (in store and online)', 'tl': 'Watsons (tindahan at online)'},
     actives={'en': ['Centella asiatica', 'Salicylic acid (BHA)', 'Gluconolactone (PHA)', 'Tea tree leaf water', 'Calamine', 'Mugwort', 'Licorice'],
              'tl': ['Centella asiatica', 'Salicylic acid (BHA)', 'Gluconolactone (PHA)', 'Tea tree leaf water', 'Calamine', 'Mugwort', 'Licorice']},
     why={'en': 'The K-beauty cult cleanser for acne-prone skin: three gentle acids plus centella, tea tree and calamine, and no fragrance.',
          'tl': 'Ang K-beauty cult cleanser para sa acne-prone na balat: tatlong mabining acid kasama ng centella, tea tree at calamine, at walang pabango.'},
     flag={'en': 'Only the small 50 ml tube stays under ₱500 and it lasts about a month; the 100 ml is ₱999 at Watsons, so COSRX’s 150 ml at ₱560 is better value if you can stretch. Soap-based lather with peppermint oil, so rinse well.',
           'tl': 'Ang maliit na 50 ml lang ang mababa sa ₱500 at mga isang buwan lang ito; ₱999 ang 100 ml sa Watsons, kaya mas sulit ang COSRX 150 ml sa ₱560 kung kaya mo. Soap-based ang bula at may peppermint oil, kaya banlawan nang mabuti.'})

prod('hadalabo_dc', brand='Hada Labo (Rohto)', name='Deep Clean & Pore Refining Face Wash', region='jp', img='https://medias.watsons.com.ph/publishing/50007565-egdZcSAY-zoom.png?version=1762937335',
     where={'en': 'Watsons (in store and online)', 'tl': 'Watsons (tindahan at online)'},
     actives={'en': ['Japanese green tea extract', 'Bentonite clay', 'Hyaluronic acid', 'Fragrance-free, mineral-oil-free'], 'tl': ['Japanese green tea extract', 'Bentonite clay', 'Hyaluronic acid', 'Walang pabango, walang mineral oil']},
     why={'en': 'Hada Labo’s oily-skin cleanser: clay absorbs excess sebum, green tea helps control oil, and hyaluronic acid keeps it from stripping. With 70 Watsons PH reviews it is the brand’s most-reviewed face wash.',
          'tl': 'Cleanser ng Hada Labo para sa oily na balat: sinisipsip ng clay ang sobrang sebum, tumutulong ang green tea sa langis, at pinipigilan ng hyaluronic acid ang pagka-strip. Sa 70 review sa Watsons PH, ito ang pinaka-nirebyu na face wash ng brand.'},
     flag={'en': 'Creamy foam that can feel a little tight on sensitive skin; the Hydrating Face Wash (₱399) is the gentler sibling.',
           'tl': 'Creamy na foam na puwedeng bahagyang masikip sa sensitive na balat; ang Hydrating Face Wash (₱399) ang mas mabining kapatid. '})

prod('garnier_serum', brand='Garnier', name='Bright Complete Anti-Acne Booster Serum', region='intl', img='https://medias.watsons.com.my/publishing/WTCMY-54345-front-zoom.jpg?version=1753310447',
     where={'en': 'Watsons (in store and online), Mercury Drug, supermarkets', 'tl': 'Watsons (tindahan at online), Mercury Drug, mga supermarket'},
     actives={'en': ['Vitamin C (ascorbyl glucoside)', 'Salicylic acid + capryloyl salicylic acid (BHA/LHA)', 'Niacinamide', 'Zinc PCA', 'Fragrance'],
              'tl': ['Vitamin C (ascorbyl glucoside)', 'Salicylic acid + capryloyl salicylic acid (BHA/LHA)', 'Niacinamide', 'Zinc PCA', 'Pabango']},
     why={'en': 'The most-bought drugstore anti-pimple serum in the country (100+ Watsons reviews): BHA and zinc for oil and pores, vitamin C and niacinamide for the marks.',
          'tl': 'Pinakamabiling drugstore anti-pimple serum sa bansa (100+ review sa Watsons): BHA at zinc para sa langis at pores, vitamin C at niacinamide para sa marka.'},
     flag={'en': 'Under ₱500 only on Watsons’ frequent promo price (regular ₱699). Contains fragrance and acids: use it every other night at first, and do not pair it with the Quick FX acid cleanser on the same day.',
           'tl': 'Mababa sa ₱500 lang sa madalas na promo ng Watsons (regular ₱699). May pabango at acids: gamitin tuwing ikalawang gabi sa umpisa, at huwag ipares sa Quick FX na acid cleanser sa iisang araw. '})

prod('skin1004_amp', brand='SKIN1004', name='Madagascar Centella Ampoule', region='kr',
     img='https://medias.watsons.com.ph/publishing/SKIN1004_Image1_50054241-goEY7M7n-zoom.jpg?version=1785201440',
     where={'en': 'SKIN1004’s official Shopee and Lazada stores for the 30 ml (online only); Watsons stocks only the 100 ml at ₱1,290', 'tl': 'Official Shopee at Lazada store ng SKIN1004 para sa 30 ml (online lang); ang 100 ml lang ang nasa Watsons sa ₱1,290'},
     actives={'en': ['Centella asiatica extract 100%'], 'tl': ['Centella asiatica extract 100%']},
     why={'en': 'A single-ingredient calming ampoule, and the K-beauty standard for angry, pimple-prone skin; watery, sinks in instantly, no fragrance.',
          'tl': 'Isang-sangkap na pampakalmang ampoule, at ang pamantayan sa K-beauty para sa iritado at pimple-prone na balat; matubig, mabilis sumipsip, walang pabango.'},
     flag={'en': 'Not a niacinamide serum (it is pure centella), and the affordable 30 ml is online-only in the Philippines; make sure the seller is the official SKIN1004 store. Price is approximate.',
           'tl': 'Hindi ito niacinamide serum (purong centella), at online lang sa Pilipinas ang abot-kayang 30 ml; siguraduhing official SKIN1004 store ang nagbebenta. Tantiya ang presyo.'})

prod('hadalabo_pwl', brand='Hada Labo (Rohto)', name='Premium Whitening Lotion', region='jp', img='https://medias.watsons.com.ph/publishing/Hada%20Labo_Image%201_50030827-NoMhBeWA-zoom.jpg?version=1764124578',
     where={'en': 'Watsons (in store and online)', 'tl': 'Watsons (tindahan at online)'},
     actives={'en': ['Tranexamic acid', 'Vitamin C derivative (magnesium ascorbyl phosphate)', 'Hyaluronic acid', 'Vitamin E', 'Fragrance-free, alcohol-free'], 'tl': ['Tranexamic acid', 'Derivative ng vitamin C (magnesium ascorbyl phosphate)', 'Hyaluronic acid', 'Vitamin E', 'Walang pabango, walang alcohol']},
     why={'en': 'The Japanese way to do a light serum step: a watery “lotion” patted on after cleansing, with arbutin and vitamin C for even tone and hyaluronic acid for hydration. The ₱220 bottle lets you test it cheaply.',
          'tl': 'Ang Japanese na paraan ng magaang serum step: matubig na “lotion” na idinidiin pagkatapos maghugas, may arbutin at vitamin C para sa pantay na kulay at hyaluronic acid para sa hydration. Puwede mo itong subukan nang mura sa ₱220.'},
     flag={'en': 'It is a lotion (toner-essence), not a concentrated serum, and it has no niacinamide. The 30 ml runs out in about a month; the real buy is the 170 ml at ₱740, above your ₱500 cap.',
           'tl': 'Lotion ito (toner-essence), hindi concentrated na serum, at walang niacinamide. Mga isang buwan lang ang 30 ml; ang tunay na sulit ay ang 170 ml sa ₱740, lampas sa ₱500 na limit mo. '})

prod('garnier_gel', brand='Garnier', name='Bright Complete Vitamin C Water Gel', region='intl',
     img='https://medias.watsons.com.sg/publishing/WTCSG-61523-front-zoom.jpg?version=1729534394', img_alt='https://medias.watsons.com.ph/publishing/Garnier_50048143_NumberSequence_Front_Left-JNxnYIPe-zoom.jpg?version=1762590394',
     where={'en': 'Watsons (in store and online), Mercury Drug, supermarkets', 'tl': 'Watsons (tindahan at online), Mercury Drug, mga supermarket'},
     actives={'en': ['Niacinamide', 'Ascorbyl glucoside (vitamin C)', 'Phenylethyl resorcinol', 'Hyaluronic acid', 'Capryloyl salicylic acid', 'Alcohol denat.', 'Fragrance'],
              'tl': ['Niacinamide', 'Ascorbyl glucoside (vitamin C)', 'Phenylethyl resorcinol', 'Hyaluronic acid', 'Capryloyl salicylic acid', 'Alcohol denat.', 'Pabango']},
     why={'en': 'A water-light gel that vanishes on oily skin, with niacinamide and two brighteners for the price of a lunch.',
          'tl': 'Kasing gaan ng tubig na gel na natutunaw sa oily na balat, may niacinamide at dalawang pampaliwanag sa presyo ng isang tanghalian.'},
     flag={'en': 'Alcohol denat. sits high in the ingredient list, plus fragrance and lemon extract; skip it if your skin stings easily.',
           'tl': 'Mataas sa listahan ang alcohol denat., may pabango at lemon extract; laktawan kung madaling humapdi ang balat mo.'})

prod('nr_aloe', brand='Nature Republic', name='Soothing & Moisture Aloe Vera 92% Soothing Gel', region='kr', img='https://peachesandcremeshop.com/cdn/shop/files/NATURE-REPUBLIC-02-01.jpg?v=1713470002&width=1800',
     where={'en': 'Nature Republic boutiques and official Shopee and Lazada stores; some Watsons branches', 'tl': 'Mga Nature Republic boutique at official Shopee at Lazada store; ilang branch ng Watsons'},
     actives={'en': ['Aloe vera leaf extract 92%', 'Hyaluronic acid', 'Polyglutamic acid', 'Calendula', 'Alcohol', 'Fragrance'],
              'tl': ['Aloe vera leaf extract 92%', 'Hyaluronic acid', 'Polyglutamic acid', 'Calendula', 'Alcohol', 'Pabango']},
     why={'en': 'The K-beauty gel every Filipino household seems to own: cooling, weightless, cheap per millilitre and usable on face and body.',
          'tl': 'Ang K-beauty gel na parang nasa bawat bahay sa Pilipinas: malamig, magaan, mura kada mililitro at puwede sa mukha at katawan.'},
     flag={'en': 'Contains alcohol and fragrance and is mostly hydration with no barrier lipids: fine for oily skin in the heat, but not enough if your skin ever feels tight. Boutique and online rather than drugstore; price is approximate.',
           'tl': 'May alcohol at pabango at halos hydration lang ito nang walang barrier lipids: ayos para sa oily na balat sa init, pero hindi sapat kung masikip ang balat mo. Boutique at online sa halip na botika; tantiya ang presyo. '})

prod('naturie', brand='Naturie (Imju)', name='Hatomugi Skin Conditioning Gel', region='jp',
     img='https://medias.watsons.com.ph/publishing/Naturie_Image1_Watsons_50053309-CHZEv5Vn-zoom.jpg?version=1766132840',
     where={'en': 'Watsons (in store and online)', 'tl': 'Watsons (tindahan at online)'},
     actives={'en': ['Job’s tears (coix seed) extract', 'Vitamin C derivative (ascorbyl tetraisopalmitate)', 'Vitamin E', 'Glycerin', 'Fragrance-free, alcohol-free, oil-free'],
              'tl': ['Job’s tears (coix seed) extract', 'Derivative ng vitamin C (ascorbyl tetraisopalmitate)', 'Vitamin E', 'Glycerin', 'Walang pabango, alcohol at langis']},
     why={'en': 'A Japanese @cosme Hall of Fame gel: water-light, oil-free, fragrance-free, non-comedogenic and enormous value at 180 g.',
          'tl': 'Japanese @cosme Hall of Fame na gel: kasing gaan ng tubig, oil-free, walang pabango, non-comedogenic at napakasulit sa 180 g.'},
     flag={'en': 'Pure hydration with no brighteners, and it uses methylparaben as preservative (safe and well studied, but some people prefer to avoid it).',
           'tl': 'Purong hydration nang walang pampaliwanag, at methylparaben ang preservative (ligtas at mahusay na napag-aralan, pero iniiwasan ng ilan).'})

prod('garnier_uv', brand='Garnier', name='Bright Complete Vitamin C UV Serum Sunscreen SPF50+', region='intl', img='https://medias.watsons.com.ph/publishing/50046793_01-gziPjMgB-zoom.jpg?version=1786174892',
     where={'en': 'Watsons (in store and online), Mercury Drug, supermarkets', 'tl': 'Watsons (tindahan at online), Mercury Drug, mga supermarket'},
     actives={'en': ['Mexoryl XL (drometrizole trisiloxane)', 'Avobenzone', 'Ensulizole', 'Vitamin C (ascorbyl glucoside)', 'Hyaluronic acid', 'Peptides', 'Alcohol denat.', 'Fragrance'], 'tl': ['Mexoryl XL (drometrizole trisiloxane)', 'Avobenzone', 'Ensulizole', 'Vitamin C (ascorbyl glucoside)', 'Hyaluronic acid', 'Peptides', 'Alcohol denat.', 'Pabango']},
     why={'en': 'The cheapest SPF50+ PA++++ from a global brand at Watsons: a thin serum texture that layers under nothing on oily skin.',
          'tl': 'Pinakamurang SPF50+ PA++++ mula sa global brand sa Watsons: manipis na serum na parang wala kang suot sa oily na balat.'},
     flag={'en': 'Small 30 ml bottle, so it is the priciest per millilitre of the sunscreens under ₱500; contains alcohol and fragrance.',
           'tl': 'Maliit ang 30 ml, kaya ito ang pinakamahal kada mililitro sa mga sunscreen na mababa sa ₱500; may alcohol at pabango. '})

prod('nr_sun', brand='Nature Republic', name='California Aloe Daily Sun Block SPF50+ PA++++', region='kr', img='https://cdn.shopify.com/s/files/1/0682/3647/6589/files/NATURE_REPUBLIC_California_Aloe_Daily_Sun_Block_SPF50_PA_57ml_2EA.jpg?v=1761638351',
     where={'en': 'Nature Republic boutiques and official Shopee and Lazada stores (not at drugstores)', 'tl': 'Mga Nature Republic boutique at official Shopee at Lazada store (wala sa botika)'},
     actives={'en': ['Homosalate, octisalate, avobenzone', 'Titanium dioxide (pink tone-up)', 'Niacinamide', 'Adenosine', 'Aloe vera', 'Fragrance'], 'tl': ['Homosalate, octisalate, avobenzone', 'Titanium dioxide (pink tone-up)', 'Niacinamide', 'Adenosine', 'Aloe vera', 'Pabango']},
     why={'en': 'Nature Republic’s best-selling sunscreen and the cheapest full-size K-beauty SPF50+ you can buy in the Philippines.',
          'tl': 'Pinakamabiling sunscreen ng Nature Republic at ang pinakamurang full-size na K-beauty SPF50+ na mabibili sa Pilipinas.'},
     flag={'en': 'Honest warning: this is a pink-tinted tone-up cream, and Korean reviewers on Hwahae rate the renewed formula only 2.9/5, with “oily” and “breakouts” as the most common complaints, so it is a weak match for oily skin. It is here only because no Korean sunscreen under ₱500 is stocked at Philippine drugstores; if you can stretch, SKIN1004 Hyalu-Cica Water-Fit Sun Serum (₱1,050, Watsons) is the better Korean buy. Boutique and online only; price approximate; the photo shows the twin pack.',
           'tl': 'Tapat na babala: pink-tinted tone-up cream ito, at 2.9/5 lang ang rating ng mga Korean reviewer sa Hwahae sa bagong formula, na “oily” at “breakouts” ang pinakakaraniwang reklamo, kaya hindi ito gaanong bagay sa oily na balat. Nandito lang ito dahil walang Korean sunscreen na mababa sa ₱500 sa mga botika sa Pilipinas; kung kaya mo, mas mahusay na Korean na bilhin ang SKIN1004 Hyalu-Cica Water-Fit Sun Serum (₱1,050, Watsons). Boutique at online lang; tantiya ang presyo; twin pack ang nasa larawan.'})

prod('skinaqua', brand='Skin Aqua (Sunplay, Rohto)', name='UV Watery Gel SPF50 PA++++', region='jp',
     img='https://medias.watsons.com.ph/publishing/WTCPH-50026772-front-zoom.jpg?version=1734141918',
     where={'en': 'Watsons (in store and online; often 50% off at ₱249)', 'tl': 'Watsons (tindahan at online; madalas 50% off sa ₱249)'},
     actives={'en': ['Octinoxate', 'Ensulizole', 'Uvinul A Plus', 'Ethylhexyl triazone', 'Bisdisulizole disodium', 'Hyaluronic acid', 'Aloe', 'Alcohol'],
              'tl': ['Octinoxate', 'Ensulizole', 'Uvinul A Plus', 'Ethylhexyl triazone', 'Bisdisulizole disodium', 'Hyaluronic acid', 'Aloe', 'Alcohol']},
     why={'en': 'A big, cheap, water-light Japanese-brand gel that also works for arms and neck, and it goes on half-price sale at Watsons several times a year.',
          'tl': 'Malaki, mura at kasing gaan ng tubig na gel ng Japanese brand na puwede rin sa braso at leeg, at ilang beses kada taon na nagiging kalahating presyo sa Watsons.'},
     flag={'en': 'Alcohol-based like Bioré and made in China for Southeast Asia; it leans on octinoxate (an older filter) alongside modern ones. Size is listed as roughly 80 g.',
           'tl': 'Alcohol-based tulad ng Bioré at gawa sa China para sa Southeast Asia; umaasa ito sa octinoxate (lumang filter) kasama ng mga moderno. Mga 80 g ang nakalistang laki.'})

prod('lipice', brand='Mentholatum (Rohto)', name='Lip Ice lip balm SPF15 (Natural or Fruity)', region='jp',
     img='https://medias.watsons.com.ph/publishing/WTCPH-50042100-front-zoom.jpg',
     where={'en': 'Watsons, Mercury Drug, 7-Eleven and most convenience stores', 'tl': 'Watsons, Mercury Drug, 7-Eleven at karamihan ng convenience store'},
     actives={'en': ['Vitamins A, C and E', 'Petrolatum and waxes', 'Menthol (icy mint)', 'SPF15'], 'tl': ['Vitamin A, C at E', 'Petrolatum at mga wax', 'Menthol (icy mint)', 'SPF15']},
     why={'en': 'The ₱110 Japanese-brand balm at every counter in the country: light, non-waxy, with SPF for the daytime.',
          'tl': 'Ang ₱110 na balm ng Japanese brand sa bawat counter sa bansa: magaan, hindi wax, may SPF para sa araw.'},
     flag={'en': 'Menthol tingle and flavour; for the before-sleep step choose the unscented Natural variant. It is a daily balm rather than an overnight mask, so apply it thicker at night.',
           'tl': 'May kiliti at lasa ng menthol; para sa step bago matulog, piliin ang walang amoy na Natural. Pang-araw-araw na balm ito sa halip na overnight mask, kaya lagyan ng mas makapal sa gabi.'})

prod('luxe_lipscreen', brand='Luxe Organix', name='Panthenol Therapy 24H Lipscreen Sun Lip Essence SPF50+ PA++++', region='ph', img='https://medias.watsons.com.ph/publishing/WTCPH-50047764-front-zoom.jpg?version=1734346545',
     where={'en': 'Watsons (in store and online), Luxe Organix official Shopee and Lazada stores', 'tl': 'Watsons (tindahan at online), official Shopee at Lazada store ng Luxe Organix'},
     actives={'en': ['Octinoxate, octisalate, homosalate', 'Tinosorb S', 'Shea butter', 'Panthenol (pro-vitamin B5)', 'Macadamia oil', 'Vitamin E', 'Alcohol', 'Fragrance'], 'tl': ['Octinoxate, octisalate, homosalate', 'Tinosorb S', 'Shea butter', 'Panthenol (pro-vitamin B5)', 'Macadamia oil', 'Vitamin E', 'Alcohol', 'Pabango']},
     why={'en': 'The only true lip sunscreen under ₱500 that is stocked at Watsons: SPF50+ PA++++ in a panthenol lip essence, from a Filipino brand, with 40+ Watsons reviews.',
          'tl': 'Ang tanging tunay na lip sunscreen na mababa sa ₱500 na nasa Watsons: SPF50+ PA++++ sa panthenol lip essence, mula sa Filipino brand, may 40+ review sa Watsons.'},
     flag={'en': 'A Filipino brand, but the product itself is manufactured in Korea. Contains fragrance and a little alcohol; reapply after eating or drinking, as with any lip SPF.',
           'tl': 'Filipino brand, pero sa Korea ginawa ang mismong produkto. May pabango at kaunting alcohol; mag-reapply pagkatapos kumain o uminom, tulad ng anumang lip SPF.'})
for pid in ('klued','cerave','cosrx','senka','dermorepubliq','ordinary','anua','melanocc','camou','neutrogena','skin1004','hadalabo','hikari','lrp','boj','biore','vaseline','mediheal','dhc'):
    P[pid]['budget'] = False

CATEGORY.update({'luxe_lipscreen':'stick','quickfx':'tube','simple':'tube','somebymi':'tube','hadalabo_dc':'tube','garnier_serum':'dropper','skin1004_amp':'dropper','hadalabo_pwl':'dropper',
                 'garnier_gel':'jar','nr_aloe':'jar','naturie':'jar','garnier_uv':'dropper','nr_sun':'tube','skinaqua':'tube','lipice':'stick'})
REGION_COLOR['ph'] = '#1F6F8B'
CAT_OF.update({'luxe_lipscreen':'lip','quickfx':'cleanser','simple':'cleanser','somebymi':'cleanser','hadalabo_dc':'cleanser','garnier_serum':'serum','skin1004_amp':'serum','hadalabo_pwl':'serum',
               'garnier_gel':'moisturizer','nr_aloe':'moisturizer','naturie':'moisturizer','garnier_uv':'sunscreen','nr_sun':'sunscreen','skinaqua':'sunscreen','lipice':'lip'})
ORIGIN_LABEL['ph'] = {'en': 'Filipino', 'tl': 'Filipino'}
ORIGIN_LABEL['current'] = {'en': 'Filipino (your current)', 'tl': 'Filipino (kasalukuyan mo)'}
for lang in ('en','tl'):
    UI[lang]['region']['ph'] = {'en': 'Filipino alternative', 'tl': 'Filipino na alternatibo'}[lang]

# ------------------------------------------------------------------ variants: (size, price text, numeric, lasts en, lasts tl)
V = {
 'klued': [('120 ml','about ₱300–350 (approx.)',325,'about 2 months at twice a day (≈1 ml per wash)','mga 2 buwan kung dalawang beses kada araw (≈1 ml kada hugas)')],
 'cerave': [('88 ml','₱495',495,'about 6 weeks','mga 6 linggo'),('236 ml','₱895',895,'about 3½–4 months','mga 3½–4 buwan'),('473 ml','₱1,334',1334,'about 7–8 months','mga 7–8 buwan')],
 'cosrx': [('150 ml','₱560',560,'about 2½ months','mga 2½ buwan'),('50 ml','₱280',280,'about 3–4 weeks','mga 3–4 linggo')],
 'senka': [('120 g','₱289',289,'about 2 months (a 2 cm strip ≈ 1 g)','mga 2 buwan (mga 1 g ang 2 cm)'),('50 g','₱139',139,'about 3–4 weeks','mga 3–4 linggo')],
 'dermorepubliq': [('30 ml','₱299',299,'about 3–4 months at 2–3 drops twice a day','mga 3–4 buwan kung 2–3 patak dalawang beses kada araw')],
 'ordinary': [('30 ml','₱849',849,'about 3–4 months','mga 3–4 buwan'),('60 ml','₱1,399',1399,'about 7 months','mga 7 buwan')],
 'anua': [('30 ml','₱1,500',1500,'about 3–4 months','mga 3–4 buwan')],
 'melanocc': [('20 ml','₱799',799,'about 2–3 months (a pea or a dab per use)','mga 2–3 buwan (gisantes o dab lang kada gamit)')],
 'camou': [('50 g','about ₱350–400 (approx.)',375,'about 5–7 weeks','mga 5–7 linggo')],
 'neutrogena': [('50 g','₱1,154 (often ₱856–899 on sale)',1154,'about 5–7 weeks','mga 5–7 linggo'),('50 g refill pack','₱799',799,'about 5–7 weeks','mga 5–7 linggo')],
 'skin1004': [('75 ml','₱1,150 (₱977.50 on sale)',1150,'about 2–2½ months','mga 2–2½ buwan')],
 'hadalabo': [('50 g','₱920',920,'about 5–7 weeks','mga 5–7 linggo'),('14 g trial','₱309',309,'about 2 weeks','mga 2 linggo')],
 'hikari': [('50 ml','about ₱300–400 (approx.)',350,'5–8 weeks at ¼ teaspoon per daylight day','5–8 linggo kung ¼ kutsarita kada araw na may araw')],
 'lrp': [('50 ml','about ₱1,300–1,600',1450,'5–8 weeks at ¼ teaspoon per daylight day','5–8 linggo kung ¼ kutsarita kada araw na may araw')],
 'boj': [('50 ml','₱1,050 (₱893 on sale)',1050,'5–8 weeks at ¼ teaspoon per daylight day','5–8 linggo kung ¼ kutsarita kada araw na may araw')],
 'biore': [('50 g','₱485',485,'5–8 weeks at ¼ teaspoon per daylight day','5–8 linggo kung ¼ kutsarita kada araw na may araw'),('15 g','₱198',198,'about 2 weeks (travel size)','mga 2 linggo (travel size)'),('85 g','₱655',655,'about 3 months','mga 3 buwan')],
 'vaseline': [('4.8 g stick','₱149',149,'about 6–8 weeks, thick layer nightly','mga 6–8 linggo, makapal na layer gabi-gabi')],
 'mediheal': [('10 ml tube','₱299 (₱215 earlier in 2026)',299,'about 5–7 weeks, thick layer nightly','mga 5–7 linggo, makapal na layer gabi-gabi')],
 'dhc': [('1.5 g stick','about ₱400–700',550,'about 1½–2 months nightly','mga 1½–2 buwan gabi-gabi')],
 'quickfx': [('150 ml','₱329',329,'about 2½ months','mga 2½ buwan'),('75 ml','₱199',199,'about 5 weeks','mga 5 linggo')],
 'simple': [('150 ml','₱249 (₱224 on sale)',249,'about 2½ months','mga 2½ buwan'),('50 ml','₱99',99,'about 3 weeks','mga 3 linggo')],
 'somebymi': [('50 ml','₱499 (₱400 on sale)',499,'about 3–4 weeks','mga 3–4 linggo'),('100 ml','₱999',999,'about 2 months','mga 2 buwan')],
 'hadalabo_dc': [('100 g','₱310',310,'about 2 months','mga 2 buwan')],
 'garnier_serum': [('30 ml','₱468 on promo (regular ₱699)',468,'about 3 months at 2–3 drops twice a day','mga 3 buwan kung 2–3 patak dalawang beses kada araw'),('8 ml','₱174',174,'about 3–4 weeks','mga 3–4 linggo')],
 'skin1004_amp': [('30 ml','about ₱400–500 (official online store)',450,'about 3–4 months','mga 3–4 buwan'),('100 ml','₱1,290 (Watsons)',1290,'about a year','mga isang taon')],
 'hadalabo_pwl': [('30 ml','₱220',220,'about 4–5 weeks used as the serum step','mga 4–5 linggo bilang serum step'),('170 ml','₱740',740,'about 6–7 months','mga 6–7 buwan')],
 'garnier_gel': [('50 ml','₱309 (₱254 on sale)',309,'about 5–7 weeks','mga 5–7 linggo')],
 'nr_aloe': [('300 ml','about ₱300–350 (Nature Republic stores)',325,'4–6 months if used on the face alone','4–6 buwan kung mukha lang')],
 'naturie': [('180 g','₱479 (₱431 on sale)',479,'about 3–4 months','mga 3–4 buwan')],
 'garnier_uv': [('30 ml','₱499',499,'about 4–5 weeks at ¼ teaspoon per daylight day','mga 4–5 linggo kung ¼ kutsarita kada araw na may araw')],
 'nr_sun': [('57 ml','about ₱400–450 (Nature Republic stores)',425,'6–8 weeks at ¼ teaspoon per daylight day','6–8 linggo kung ¼ kutsarita kada araw na may araw')],
 'skinaqua': [('80 g (approx.)','₱499 (often ₱249 at 50% off)',499,'about 2 months at ¼ teaspoon per daylight day','mga 2 buwan kung ¼ kutsarita kada araw na may araw')],
 'lipice': [('3.5 g','₱110',110,'about 2–3 months','mga 2–3 buwan')],
 'luxe_lipscreen': [('10 g','₱199',199,'about 2–3 months with daytime reapplication','mga 2–3 buwan kasama ang pag-reapply sa araw')],
}
assert set(V) == set(P), set(P) ^ set(V)


# ------------------------------------------------------------------ JSON hooks (edited by the update-top-picks skill)
import json
EXTRA_JSON = os.path.join(HERE, 'products-extra.json')
TOP_JSON = os.path.join(HERE, 'top-picks.json')
if os.path.exists(EXTRA_JSON):
    for e in json.load(open(EXTRA_JSON, encoding='utf-8')):
        pid = e['id']
        base = P.get(pid, {})
        P[pid] = dict(base, id=pid, brand=e.get('brand', base.get('brand')), name=e.get('name', base.get('name')), region=e.get('region', base.get('region')),
                      img=e.get('img', base.get('img')), img_alt=e.get('img_alt', base.get('img_alt')), where=e.get('where', base.get('where')),
                      actives=e.get('actives', base.get('actives')), why=e.get('why', base.get('why')), flag=e.get('flag', base.get('flag')))
        if 'variants' in e: V[pid] = [tuple(v) for v in e['variants']]      # [size, price text, numeric price, lasts_en, lasts_tl]
        CATEGORY[pid] = e.get('shape', CATEGORY.get(pid, 'tube'))          # tube | dropper | jar | stick
        CAT_OF[pid] = e.get('category', CAT_OF.get(pid))                   # cleanser | serum | moisturizer | sunscreen | lip

# ------------------------------------------------------------------ steps with budget picks appended
WAKE[2]['title'] = {'en': 'Moisturize (optional for oily skin)', 'tl': 'Mag-moisturizer (opsyonal para sa oily na balat)'}
WAKE[2]['skip'] = {'en': 'your sunscreen already feels hydrating and your skin is not tight after cleansing. Dermatologists agree oily skin can go cleanser → serum → sunscreen in the daytime; the moisturizer becomes essential at bedtime instead. Keep it on wake-ups with no sunscreen, or if your skin ever feels tight or flaky.',
                   'tl': 'nakakahydrate na ang sunscreen mo at hindi masikip ang balat pagkahugas. Sang-ayon ang mga dermatologist na puwedeng cleanser → serum → sunscreen lang ang oily na balat sa araw; ang moisturizer ang naging pinakamahalaga bago matulog. Panatilihin ito kung walang sunscreen sa paggising, o kung masikip o nagbabalat ang balat mo.'}
WAKE.append(dict(key='daylip', products=['luxe_lipscreen','vaseline','mediheal','dhc','lipice'],
      title={'en': 'Lip balm with SPF (daytime lip care)', 'tl': 'Lip balm na may SPF (lip care sa araw)'},
      amount={'en': 'One thin, even swipe; a little more at the corners.', 'tl': 'Isang manipis at pantay na hagod; kaunti pang dagdag sa mga gilid.'},
      tech={'en': 'Apply after sunscreen, as the last step. Lips have no melanin protection to speak of, so if you will see daylight, pick the SPF option (Luxe Organix SPF50+ or Lip Ice SPF15); on no-daylight wake-ups any plain balm from the night step works. Reapply after eating or drinking. The night masks (Mediheal, DHC) can double as a thin daytime layer if you prefer one product.',
            'tl': 'I-apply pagkatapos ng sunscreen, bilang huling step. Halos walang melanin na proteksyon ang labi, kaya kung makakakita ka ng araw, piliin ang may SPF (Luxe Organix SPF50+ o Lip Ice SPF15); kung walang araw sa paggising, puwede ang anumang plain na balm mula sa night step. Mag-reapply pagkatapos kumain o uminom. Puwedeng manipis na pang-araw din ang mga night mask (Mediheal, DHC) kung isang produkto lang ang gusto mo.'},
      wait={'en': 'Nothing after this. Popular options I could not verify at a Philippine drugstore this round: Sun Bum SPF30 lip balm (international) and Laneige Lip Glowy Balm (Korean), both boutique or online buys.',
            'tl': 'Wala nang kasunod. Mga sikat na opsyon na hindi ko na-verify sa botika sa Pilipinas ngayong round: Sun Bum SPF30 lip balm (international) at Laneige Lip Glowy Balm (Korean), pareho boutique o online.'}))


# ------------------------------------------------------------------ UI strings
X = {'en': dict(pick_n='Choose one of these {n}. Do not use them together.', budget_h='Budget picks, ₱500 and under',
                sizes_l='Sizes, prices and how long each lasts', s_size='Size', s_price='Price', s_lasts='Lasts about',
                search_l='Search', search_ph='Type a brand, product or ingredient', sort_l='Sort', sort_default='Default order', sort_asc='Price: low to high', sort_desc='Price: high to low',
                filter_budget='Budget', budget_only='₱500 and under', showing='Showing {n} of 34 products', products_h='All 34 products',
                products_sub='Every product in this plan in one place. Filter by type, brand origin or budget, sort by price, and click any photo to see it full size. Prices for multi-size products are sorted by the first size listed.'),
     'tl': dict(pick_n='Pumili ng isa sa {n} na ito. Huwag gamitin nang sabay.', budget_h='Mga budget pick, ₱500 pababa',
                sizes_l='Laki, presyo at gaano katagal ang bawat isa', s_size='Laki', s_price='Presyo', s_lasts='Tatagal ng mga',
                search_l='Hanapin', search_ph='Brand, produkto o sangkap', sort_l='Ayusin', sort_default='Default na ayos', sort_asc='Presyo: mababa hanggang mataas', sort_desc='Presyo: mataas hanggang mababa',
                filter_budget='Budget', budget_only='₱500 pababa', showing='Ipinapakita ang {n} sa 34 na produkto', products_h='Lahat ng 34 produkto',
                products_sub='Lahat ng produkto sa planong ito sa isang lugar. I-filter ayon sa uri, pinagmulan ng brand o budget, ayusin ayon sa presyo, at i-click ang larawan para makita sa buong laki. Ayon sa unang nakalistang laki ang pag-aayos ng presyo ng mga produktong maraming laki.')}
for k in UI: UI[k].update(X[k])
UI['en']['notes'][2] = 'Photos: product photos come from the retailers’ and brands’ websites, mostly Watsons Philippines; if a photo cannot load, the card shows the brand’s initial instead. Retailer photos are the largest each site publishes (roughly 1,000–1,500 px); none of these products has a 4K retailer image.'
UI['tl']['notes'][2] = 'Mga larawan: galing sa mga website ng retailer at ng brand ang mga larawan ng produkto, karamihan ay mula sa Watsons Philippines; kung hindi ma-load ang isang larawan, unang titik ng brand ang lalabas sa card. Ang mga larawan ng retailer ang pinakamalaking inilathala ng bawat site (mga 1,000–1,500 px); walang 4K na larawan mula sa retailer para sa mga produktong ito.'
UI['en']['gloss_sub'] = 'All the actives and notable ingredients across the 34 products above, in plain language, with the products that contain each one.'
UI['tl']['gloss_sub'] = 'Lahat ng aktibo at kapansin-pansing sangkap sa 34 produkto sa itaas, sa simpleng salita, kasama ang mga produktong naglalaman ng bawat isa.'

# ------------------------------------------------------------------ fixed slot structure (edited by the update-alternatives / update-current skills)
SLOTS_JSON = os.path.join(HERE, 'slots.json')
SLOT_ORDER = ['current', 'intl', 'kr', 'jp', 'ph_budget', 'intl_budget', 'kr_budget', 'jp_budget']
SLOT_LABEL = {'current': {'en': 'Your current product', 'tl': 'Kasalukuyang produkto mo'},
              'intl': {'en': 'International alternative', 'tl': 'International na alternatibo'}, 'kr': {'en': 'Korean alternative', 'tl': 'Korean na alternatibo'},
              'jp': {'en': 'Japanese alternative', 'tl': 'Japanese na alternatibo'}, 'ph_budget': {'en': 'Filipino alternative', 'tl': 'Filipino na alternatibo'},
              'intl_budget': {'en': 'International alternative', 'tl': 'International na alternatibo'}, 'kr_budget': {'en': 'Korean alternative', 'tl': 'Korean na alternatibo'},
              'jp_budget': {'en': 'Japanese alternative', 'tl': 'Japanese na alternatibo'}}
DEFAULT_SLOTS = {
 'cleanse': {'current': 'klued', 'intl': 'cerave', 'kr': 'cosrx', 'jp': 'senka', 'ph_budget': 'quickfx', 'intl_budget': 'simple', 'kr_budget': 'somebymi', 'jp_budget': 'hadalabo_dc'},
 'serum':   {'current': 'dermorepubliq', 'intl': 'ordinary', 'kr': 'anua', 'jp': 'melanocc', 'ph_budget': None, 'intl_budget': 'garnier_serum', 'kr_budget': 'skin1004_amp', 'jp_budget': 'hadalabo_pwl'},
 'moist':   {'current': 'camou', 'intl': 'neutrogena', 'kr': 'skin1004', 'jp': 'hadalabo', 'ph_budget': None, 'intl_budget': 'garnier_gel', 'kr_budget': 'nr_aloe', 'jp_budget': 'naturie'},
 'sun':     {'current': 'hikari', 'intl': 'lrp', 'kr': 'boj', 'jp': 'biore', 'ph_budget': None, 'intl_budget': 'garnier_uv', 'kr_budget': 'nr_sun', 'jp_budget': 'skinaqua'},
 'daylip':  {'current': None, 'intl': 'vaseline', 'kr': 'mediheal', 'jp': 'dhc', 'ph_budget': 'luxe_lipscreen', 'intl_budget': None, 'kr_budget': None, 'jp_budget': 'lipice'},
 'lip':     {'current': None, 'intl': 'vaseline', 'kr': 'mediheal', 'jp': 'dhc', 'ph_budget': None, 'intl_budget': None, 'kr_budget': None, 'jp_budget': 'lipice'},
}
if os.path.exists(SLOTS_JSON):
    SLOTS = json.load(open(SLOTS_JSON, encoding='utf-8'))
else:
    SLOTS = DEFAULT_SLOTS; json.dump(SLOTS, open(SLOTS_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for _step, _m in SLOTS.items():
    for _slot, _pid in _m.items():
        assert _slot in SLOT_ORDER, f"slots.json: unknown slot '{_slot}' in step '{_step}'"
        assert _pid is None or _pid in P, f"slots.json: unknown product id '{_pid}' in step '{_step}'/{_slot} (add it to products-extra.json first)"
PRIMARY_SLOT = {}      # product id -> (step, slot) of its first appearance, used for labels on the All products / Top picks pages
for _step in ('cleanse', 'serum', 'moist', 'sun', 'daylip', 'lip'):
    for _slot in SLOT_ORDER:
        _pid = SLOTS.get(_step, {}).get(_slot)
        if _pid and _pid not in PRIMARY_SLOT: PRIMARY_SLOT[_pid] = (_step, _slot)
for _pid in P: P[_pid]['budget'] = False
for _step, _m in SLOTS.items():
    for _slot, _pid in _m.items():
        if _pid and _slot.endswith('_budget'): P[_pid]['budget'] = True
def slot_products(step_key):
    m = SLOTS.get(step_key, {})
    return [(slot, m[slot]) for slot in SLOT_ORDER if m.get(slot)]
for _s in WAKE + SLEEP:
    _s['slots'] = slot_products(_s['key']); _s['products'] = [pid for _, pid in _s['slots']]

UI['en']['how'].append(('Moisturizer in the daytime is optional for you.', 'The cleanser-then-sunscreen routines you see in videos are a valid minimalist approach for oily skin: dermatologists say you can skip the morning moisturizer if your sunscreen feels hydrating enough. Where they all agree is that moisturizer matters at bedtime, and that sunscreen is the non-negotiable daytime step. The wake-up routine below marks the moisturizer as optional and tells you when to keep it.'))
UI['tl']['how'].append(('Opsyonal para sa iyo ang moisturizer sa araw.', 'Ang cleanser-tapos-sunscreen na routine sa mga video ay tanggap na minimalist na paraan para sa oily na balat: sabi ng mga dermatologist, puwedeng laktawan ang moisturizer sa umaga kung nakakahydrate na ang sunscreen. Ang pinagkakasunduan nila ay mahalaga ang moisturizer bago matulog, at hindi puwedeng laktawan ang sunscreen sa araw. Minarkahan bilang opsyonal ang moisturizer sa routine pag-gising sa ibaba at sinasabi kung kailan ito panatilihin.'))
UI['en']['how'].append(('Budget picks.', 'Each step now also lists one alternative at ₱500 or under per brand origin (plus a Filipino one for the cleanser). They are marked in the cards; a few are only under ₱500 in a small size or on Watsons’ promo price, and the card says so.'))
UI['tl']['how'].append(('Mga budget pick.', 'May isa na ring alternatibo sa bawat step na ₱500 pababa kada pinagmulan ng brand (at isang Filipino para sa cleanser). Nakamarka ang mga ito sa card; ang ilan ay mababa sa ₱500 lang sa maliit na laki o sa promo ng Watsons, at nakasaad iyon sa card.'))


TOP = [
 dict(cat='cleanser', pick='quickfx', runner='cosrx',
      why={'en': 'Close to 200 Watsons reviews on the 75 ml alone, ₱329 for 150 ml, and a formula built for exactly your skin: salicylic acid for pores, tea tree and niacinamide for the occasional pimple. Use it at bedtime every day; if your skin ever feels tight, keep your Klued jelly for the wake-up wash instead of washing with acids twice.',
           'tl': 'Halos 200 review sa Watsons sa 75 ml lang, ₱329 para sa 150 ml, at formula na ginawa para sa mismong balat mo: salicylic acid para sa pores, tea tree at niacinamide para sa paminsan-minsang pimple. Gamitin bago matulog araw-araw; kung masikip ang balat, gamitin ang Klued jelly mo sa paggising sa halip na acids nang dalawang beses.'},
      rwhy={'en': 'gentler low-pH gel with a whisper of BHA if acids bother you', 'tl': 'mas mabining low-pH gel na may kaunting BHA kung nakakairita ang acids'},
      evidence={'en': 'Close to 200 Watsons PH reviews on the 75 ml (checked 12 Sep 2026); named among the best acne face washes under ₱500 by Philippine beauty press; the 150 ml is ₱329 in store.', 'tl': 'Halos 200 review sa Watsons PH sa 75 ml (na-check 12 Set 2026); kabilang sa pinakamahusay na acne face wash na mababa sa ₱500 ayon sa beauty press sa Pilipinas; ₱329 ang 150 ml sa tindahan.'}),
 dict(cat='serum', pick='dermorepubliq', runner='ordinary',
      why={'en': 'Keep what you already own. At ₱299 it is the cheapest niacinamide serum in the plan, it is stocked at Watsons, and 5% is the strength dermatologists usually suggest for oily skin. It also has no acids, so it pairs safely with the Quick FX cleanser; the popular Garnier and Anua serums would stack acids or brighteners you do not need.',
           'tl': 'Panatilihin ang nasa iyo na. Sa ₱299 ito ang pinakamurang niacinamide serum sa plano, nasa Watsons, at 5% ang lakas na karaniwang inirerekomenda ng mga dermatologist para sa oily na balat. Wala rin itong acids, kaya ligtas ipares sa Quick FX cleanser; magpapatong ng acids o pampaliwanag na hindi mo kailangan ang mga sikat na Garnier at Anua.'},
      rwhy={'en': 'the world’s best-known niacinamide serum if you want a stronger 10%', 'tl': 'ang pinakakilalang niacinamide serum sa mundo kung gusto mo ng mas malakas na 10%'},
      evidence={'en': 'Transparency: the most-bought serum at Watsons PH is Garnier’s Bright Complete Vitamin C Serum (841 reviews), followed by Garnier Anti-Acne (109). Both contain salicylic acid, so they would double up on acids with the Quick FX cleanser; DermoRepubliq (₱299, Watsons) is recommended for fit, not for popularity.', 'tl': 'Transparency: ang pinakabinibiling serum sa Watsons PH ay ang Garnier Bright Complete Vitamin C Serum (841 review), sinundan ng Garnier Anti-Acne (109). Pareho may salicylic acid, kaya madodoble ang acids kasama ng Quick FX cleanser; inirerekomenda ang DermoRepubliq (₱299, Watsons) dahil sa bagay, hindi dahil sa popularidad.'}),
 dict(cat='moisturizer', pick='neutrogena', runner='naturie',
      why={'en': 'The most-reviewed moisturizer in this whole plan at Watsons PH (117 reviews) and the classic dermatologist recommendation for oily skin: an oil-free, non-comedogenic water gel that disappears without shine. The refill pack (₱799) is the same product for less, which is how most repeat buyers get it.',
           'tl': 'Ang pinaka-nirebyu na moisturizer sa buong planong ito sa Watsons PH (117 review) at ang klasikong rekomendasyon ng mga dermatologist para sa oily na balat: oil-free at non-comedogenic na water gel na natutunaw nang walang kintab. Parehong produkto ang refill pack (₱799) sa mas mababang presyo, na siyang binibili ng karamihan sa mga umuulit.'},
      rwhy={'en': 'the value pick: Japan’s @cosme Hall of Fame oil-free, fragrance-free gel, 180 g for ₱479', 'tl': 'ang value pick: @cosme Hall of Fame na oil-free at walang pabangong gel ng Japan, 180 g sa ₱479'},
      evidence={'en': '117 Watsons PH reviews, the highest of any moisturizer in this plan (checked 12 Sep 2026); Neutrogena Hydro Boost is also the moisturizer most often named in dermatologist roundups for oily skin. Naturie has 11 Watsons PH reviews but an @cosme Hall of Fame record in Japan.', 'tl': '117 review sa Watsons PH, pinakamataas sa lahat ng moisturizer sa planong ito (na-check 12 Set 2026); ang Neutrogena Hydro Boost din ang pinakamadalas banggitin ng mga dermatologist para sa oily na balat. 11 review sa Watsons PH ang Naturie pero @cosme Hall of Fame ito sa Japan.'}),
 dict(cat='sunscreen', pick='biore', runner='boj',
      why={'en': 'Japan’s best-selling sunscreen, ₱485 at Watsons and Mercury Drug, modern photostable filters, zero white cast, and it dries down in seconds on oily skin. Nothing else under ₱500 in the Philippines protects this well, and the 15 g tube is a cheap way to try it.',
           'tl': 'Pinakamabiling sunscreen sa Japan, ₱485 sa Watsons at Mercury Drug, modernong photostable na filter, walang white cast, at natutuyo sa ilang segundo sa oily na balat. Wala nang ibang mababa sa ₱500 sa Pilipinas na ganito kahusay ang proteksyon, at murang pagsubok ang 15 g.'},
      rwhy={'en': 'the most talked-about K-beauty sunscreen if you want a fragrance-free, alcohol-free formula', 'tl': 'ang pinakapinag-uusapang K-beauty sunscreen kung gusto mo ng walang pabango at walang alcohol'},
      evidence={'en': 'Japan’s long-running best-selling sunscreen; ranked no. 1 in Watsons’ own “best sunscreens for oily skin” editorial; stocked at Watsons PH (50 g ₱485, 15 g ₱198, 85 g ₱655) and Mercury Drug. Newest competitor to know: Beauty of Joseon’s 2026 Relief Sun Aqua-Fresh Rice + B5, made for oily skin, not yet confirmed at Watsons PH.', 'tl': 'Matagal nang pinakamabiling sunscreen sa Japan; no. 1 sa sariling “best sunscreens for oily skin” editorial ng Watsons; nasa Watsons PH (50 g ₱485, 15 g ₱198, 85 g ₱655) at Mercury Drug. Pinakabagong kakumpitensya: ang 2026 Relief Sun Aqua-Fresh Rice + B5 ng Beauty of Joseon, ginawa para sa oily na balat, hindi pa nakumpirma sa Watsons PH.'}),
 dict(cat='lipday', pick='luxe_lipscreen', runner='lipice',
      why={'en': 'The only real lip sunscreen (SPF50+ PA++++) under ₱500 that Watsons stocks, from a Filipino brand, with 42 reviews. Lips burn faster than the face, so on daylight wake-ups this is the step people skip and regret.',
           'tl': 'Ang tanging tunay na lip sunscreen (SPF50+ PA++++) na mababa sa ₱500 na nasa Watsons, mula sa Filipino brand, may 42 review. Mas mabilis masunog ang labi kaysa mukha, kaya ito ang step na nilalaktawan at pinagsisisihan ng mga tao sa mga araw na may araw.'},
      rwhy={'en': 'a ₱110 SPF15 balm sold at every counter if the Lipscreen is out of stock', 'tl': '₱110 na SPF15 balm sa bawat counter kung out of stock ang Lipscreen'},
      evidence={'en': '42 Watsons PH reviews and the only SPF50+ PA++++ lip product under ₱500 there. The more-reviewed alternative is Nivea Med Repair SPF15 Lip Balm (359 reviews, ₱172), but at SPF15 it protects far less; Lip Ice SPF15 (₱110) is the drugstore backup.', 'tl': '42 review sa Watsons PH at ang tanging SPF50+ PA++++ na lip product na mababa sa ₱500 doon. Mas maraming review ang Nivea Med Repair SPF15 Lip Balm (359 review, ₱172), pero mas mababa ang proteksyon sa SPF15; Lip Ice SPF15 (₱110) ang drugstore backup.'}),
 dict(cat='lipnight', pick='vaseline', runner='mediheal',
      why={'en': 'Petroleum jelly is still what dermatologists reach for on chapped lips: it cuts water loss by more than 98%, costs ₱149 and is sold everywhere. The Rosy Lips tin with 300+ Watsons reviews is the same base with a tint, so the plain stick is the pick.',
           'tl': 'Petroleum jelly pa rin ang inaabot ng mga dermatologist para sa tuyong labi: binabawasan nito ang pagkawala ng tubig ng higit 98%, ₱149 lang at nasa lahat ng tindahan. Ang Rosy Lips tin na may 300+ review sa Watsons ay parehong base na may tint, kaya ang plain na stick ang pili.'},
      rwhy={'en': 'a true overnight lip mask at ₱299 if you want a K-beauty texture', 'tl': 'tunay na overnight lip mask sa ₱299 kung gusto mo ng K-beauty na texture'},
      evidence={'en': '300+ Watsons PH reviews across the Lip Therapy line (the Rosy Lips tin alone has 300+), and petrolatum is the American Academy of Dermatology’s standard advice for chapped lips.', 'tl': '300+ review sa Watsons PH sa buong Lip Therapy line (300+ ang Rosy Lips tin lang), at petrolatum ang pamantayang payo ng American Academy of Dermatology para sa tuyong labi.'}),
]

TOP_META = {'updated': '11–12 September 2026', 'updated_tl': '11–12 Setyembre 2026'}
if os.path.exists(TOP_JSON):
    _d = json.load(open(TOP_JSON, encoding='utf-8'))
    if isinstance(_d, dict):
        TOP = _d['picks']; TOP_META.update({k: v for k, v in _d.items() if k != 'picks'})
    else:
        TOP = _d
else:
    json.dump(dict(TOP_META, picks=TOP), open(TOP_JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for _t in TOP:
    assert _t['pick'] in P and _t['runner'] in P, f"top-picks.json references an unknown product id: {_t}"

TOPCAT = {'cleanser': {'en': 'Cleanser', 'tl': 'Cleanser'}, 'serum': {'en': 'Serum', 'tl': 'Serum'}, 'moisturizer': {'en': 'Moisturizer', 'tl': 'Moisturizer'},
          'sunscreen': {'en': 'Sunscreen', 'tl': 'Sunscreen'}, 'lipday': {'en': 'Lip balm with SPF (daytime)', 'tl': 'Lip balm na may SPF (araw)'}, 'lipnight': {'en': 'Lip treatment (bedtime)', 'tl': 'Lip treatment (bago matulog)'}}
X2 = {'en': dict(nav_top='Top picks', top_h='Top picks: one product per step', top_sub='Six products chosen from the 34 in this plan. Each is the one most people in the Philippines actually buy and rate well, suits oily, occasionally pimple-prone skin, and can be picked up at Watsons. The alternatives on the routine page are there for when a top pick is out of stock or disagrees with your skin.',
                 top_badge='Top pick', why_this='Why this one over the others', runner_l='Runner-up', evidence_l='Evidence ({updated})', method_h='How these were chosen, and how sure I am', method='“Most popular” here means what Filipinos actually buy and review at Watsons PH as of {updated} (review counts checked product by product), backed by press and retailer best-seller lists. There is no public product-level “best of 2026” list for the Philippines: the Watsons HWB Awards 2026 (15 May 2026) honoured brands and distributors, not individual products, so every pick below shows its own evidence. Where the most-reviewed product is not the pick, the card says so and explains why. Popularity was then weighed against fit for oily, occasionally pimple-prone skin, price, and walk-in availability.', glance_h='Your top-pick routine at a glance',
                 glance_wake='Wake-up: Quick FX (or your Klued if skin feels tight) → DermoRepubliq → Neutrogena Hydro Boost (optional) → Bioré if you will see daylight → Luxe Organix Lipscreen.',
                 glance_sleep='Before sleep: Quick FX → DermoRepubliq → Neutrogena Hydro Boost → Vaseline.',
                 cost_l='Starter cost for all six', cost_note='at the main sizes (₱355 less with the Neutrogena refill pack); together they last roughly two months, with the serum stretching to three or four.'),
      'tl': dict(nav_top='Mga top pick', top_h='Mga top pick: isang produkto kada step', top_sub='Anim na produkto na pinili mula sa 34 sa planong ito. Bawat isa ay ang pinakabinibili at mataas ang rating sa Pilipinas, bagay sa oily at paminsan-minsang pimple-prone na balat, at mabibili sa Watsons. Nandoon ang mga alternatibo sa routine page kung out of stock ang top pick o hindi bagay sa balat mo.',
                 top_badge='Top pick', why_this='Bakit ito at hindi ang iba', runner_l='Pangalawa', evidence_l='Ebidensya ({updated})', method_h='Paano pinili ang mga ito, at gaano ako sigurado', method='Ang “pinakasikat” dito ay kung ano talaga ang binibili at nirerebyu ng mga Pilipino sa Watsons PH noong {updated} (na-check ang bilang ng review kada produkto), na sinusuportahan ng press at mga best-seller list ng retailer. Walang pampublikong “best of 2026” na listahan kada produkto para sa Pilipinas: ang Watsons HWB Awards 2026 (15 Mayo 2026) ay nagparangal sa mga brand at distributor, hindi sa indibidwal na produkto, kaya may sariling ebidensya ang bawat pick sa ibaba. Kung hindi ang pinaka-nirebyu ang pick, sinasabi iyon ng card at ipinapaliwanag kung bakit. Pagkatapos, tinimbang ang popularidad laban sa pagkabagay sa oily at paminsan-minsang pimple-prone na balat, presyo, at availability sa tindahan.', glance_h='Ang top-pick routine mo sa isang tingin',
                 glance_wake='Pag-gising: Quick FX (o Klued mo kung masikip ang balat) → DermoRepubliq → Neutrogena Hydro Boost (opsyonal) → Bioré kung makakakita ng araw → Luxe Organix Lipscreen.',
                 glance_sleep='Bago matulog: Quick FX → DermoRepubliq → Neutrogena Hydro Boost → Vaseline.',
                 cost_l='Panimulang gastos para sa anim', cost_note='sa pangunahing laki (₱355 ang mas mura kung refill pack ng Neutrogena); magkasama, mga dalawang buwan ang tagal, at umaabot sa tatlo hanggang apat ang serum.')}
for k in UI: UI[k].update(X2[k])


VISIBLE = list(PRIMARY_SLOT)                      # every product in a slot, in step/slot order
for _t in TOP:
    for _pid in (_t['pick'], _t['runner']):
        if _pid not in VISIBLE: VISIBLE.append(_pid)

# fill dates + product counts into UI strings (after all products/top picks are known)
for _lang in UI:
    _upd = TOP_META['updated'] if _lang == 'en' else TOP_META.get('updated_tl', TOP_META['updated'])
    for _k in ('evidence_l', 'method'):
        UI[_lang][_k] = UI[_lang][_k].replace('{updated}', _upd)
    for _k in ('showing', 'products_h', 'gloss_sub', 'top_sub'):
        UI[_lang][_k] = UI[_lang][_k].replace('34', str(len(VISIBLE)))

# ------------------------------------------------------------------ glossary additions / chip updates
def add_ids(term_start, ids):
    for g, entries in GLOSSARY:
        for e in entries:
            if e['name']['en'].startswith(term_start):
                for i in ids:
                    if i not in e['ids']: e['ids'].append(i)
add_ids('Hyaluronic acid', ['hadalabo_dc','hadalabo_pwl','garnier_gel','nr_aloe','skinaqua'])
add_ids('Glycerin', ['quickfx','simple','garnier_gel','naturie','nr_aloe','somebymi'])
add_ids('Panthenol', ['simple'])
add_ids('Niacinamide', ['quickfx','garnier_gel','garnier_serum'])
add_ids('Zinc', ['garnier_serum'])
add_ids('Tea tree', ['quickfx','somebymi'])
add_ids('Alpha-arbutin', ['hadalabo_pwl'])
add_ids('Vitamin C', ['quickfx','garnier_gel','garnier_serum','hadalabo_pwl','naturie','garnier_uv'])
add_ids('Vitamin E', ['simple','naturie','lipice'])
add_ids('Licorice', ['somebymi'])
add_ids('Centella', ['somebymi','skin1004_amp'])
add_ids('Allantoin', ['quickfx'])
add_ids('Aloe', ['quickfx','nr_aloe','nr_sun','skinaqua'])
add_ids('Modern photostable', ['skinaqua'])
add_ids('Octinoxate', ['skinaqua'])
add_ids('Petrolatum', ['lipice'])
add_ids('Alcohol', ['garnier_gel','nr_aloe','nr_sun','skinaqua','garnier_uv'])
add_ids('Fragrance', ['garnier_gel','garnier_serum','garnier_uv','nr_aloe','nr_sun','lipice'])
add_ids('Dimethicone', ['garnier_gel','naturie'])
add_ids('Soap-based', ['somebymi'])
for g, entries in GLOSSARY:
    for e in entries:
        if e['name']['en'].startswith('Betaine salicylate'):
            e['name'] = {'en': 'BHA: salicylic acid, capryloyl salicylic acid and betaine salicylate', 'tl': 'BHA: salicylic acid, capryloyl salicylic acid at betaine salicylate'}
            e['en'] = 'Oil-soluble exfoliants that get inside pores and loosen the plugs that become blackheads and pimples. Salicylic acid (Quick FX, Some By Mi, Garnier) is the classic; betaine salicylate (COSRX, Anua) is a softer cousin. Low levels in a cleanser are safe daily; two acid products on the same day is usually too much.'
            e['tl'] = 'Mga exfoliant na natutunaw sa langis, pumapasok sa pores at nagluluwag ng bara na nagiging blackheads at pimples. Klasiko ang salicylic acid (Quick FX, Some By Mi, Garnier); mas mabining kamag-anak ang betaine salicylate (COSRX, Anua). Ligtas araw-araw ang kaunti sa cleanser; sobra na kadalasan ang dalawang acid na produkto sa iisang araw.'
            e['ids'] = ['cosrx','anua','quickfx','somebymi','garnier_serum','garnier_gel']
G = ns['G'] if 'G' in ns else None
def Gx(name_en, name_tl, en, tl, ids): return dict(name={'en': name_en, 'tl': name_tl}, en=en, tl=tl, ids=ids)
GLOSSARY[1][1].extend([
    Gx('Glycolic acid (AHA) and gluconolactone (PHA)', 'Glycolic acid (AHA) at gluconolactone (PHA)',
       'Water-soluble exfoliants that loosen dead surface cells so skin looks smoother. Glycolic acid is the strongest and can raise sun sensitivity; PHA is the gentlest. Rinse-off cleansers keep the contact time short.',
       'Mga exfoliant na natutunaw sa tubig na nagluluwag ng patay na balat sa ibabaw para mas makinis ang balat. Pinakamalakas ang glycolic acid at puwedeng magpa-sensitive sa araw; pinakabanayad ang PHA. Maikli ang contact time sa mga cleanser na hinuhugasan.', ['quickfx','somebymi']),
    Gx('Green tea extract, bentonite clay and calamine', 'Green tea extract, bentonite clay at calamine',
       'Oil absorbers and mild astringents: clay and calamine soak up sebum, green tea polyphenols help calm and slightly reduce oil.',
       'Mga sumisipsip ng langis at mabining astringent: sinisipsip ng clay at calamine ang sebum, tumutulong ang polyphenols ng green tea na pakalmahin at bahagyang bawasan ang langis.', ['hadalabo_dc','somebymi']),
])
GLOSSARY[2][1].extend([
    Gx('Phenylethyl resorcinol', 'Phenylethyl resorcinol',
       'A potent, fast-acting brightener (related to resorcinol) used by L’Oréal brands; helps fade marks quicker than arbutin but can irritate very sensitive skin.',
       'Malakas at mabilis na pampaliwanag (kamag-anak ng resorcinol) na ginagamit ng mga brand ng L’Oréal; mas mabilis kumupas ang marka kaysa arbutin pero puwedeng mairita ang napaka-sensitive na balat.', ['garnier_gel']),
    Gx('Job’s tears (coix seed, hatomugi) extract', 'Job’s tears (coix seed, hatomugi) extract',
       'A grain extract long used in Japan for smooth, even skin; hydrating and mildly soothing.',
       'Extract ng butil na matagal nang ginagamit sa Japan para sa makinis at pantay na balat; nagpapahydrate at bahagyang nagpapakalma.', ['naturie','hadalabo']),
])
GLOSSARY[4][1].append(
    Gx('Ensulizole and bisdisulizole disodium', 'Ensulizole at bisdisulizole disodium',
       'Water-soluble UVB and UVA filters that let a sunscreen feel like a light gel rather than an oil; they are why Skin Aqua feels so thin.',
       'Mga UVB at UVA filter na natutunaw sa tubig kaya parang magaang gel ang sunscreen sa halip na langis; ito ang dahilan kung bakit napakamanipis ng Skin Aqua.', ['skinaqua']))
GLOSSARY[6][1].append(
    Gx('Menthol', 'Menthol',
       'Gives lip balms their cooling tingle. Pleasant for many, but it is a mild irritant and can leave already-chapped lips drier, so pick unscented balms for overnight repair.',
       'Nagbibigay ng malamig na kiliti sa lip balm. Kaaya-aya sa marami, pero bahagyang irritant ito at puwedeng mas matuyo ang tuyong labi, kaya piliin ang walang amoy para sa pag-repair sa gabi.', ['lipice']))

# ------------------------------------------------------------------ CSS / JS (from v2, plus additions)
CSS = re.search(r'CSS = r"""(.*?)"""', src2, re.S).group(1) + r"""
.vtab{width:100%;border-collapse:collapse;font-size:14.5px;margin-top:4px}
.vtab th{text-align:left;color:var(--ink-2);font-weight:600;padding:4px 8px 4px 0;border-bottom:1px solid var(--line)}
.vtab td{padding:5px 8px 5px 0;border-bottom:1px solid var(--line);vertical-align:top} .vtab td:first-child{white-space:nowrap} .vtab tr:last-child td{border-bottom:0}
.tag{display:inline-block;font-size:12.5px;font-weight:600;color:var(--ok);background:var(--ok-bg);border-radius:6px;padding:2px 7px;margin-left:8px;vertical-align:middle}
.card.budget{border-color:#B9D6C7}
.divider{margin:26px 0 8px;font-family:Fraunces,Georgia,serif;font-size:20px;color:var(--ink);display:flex;align-items:center;gap:12px}
.divider::after{content:"";flex:1;height:1px;background:var(--line)}
.mini{grid-template-columns:repeat(auto-fill,minmax(112px,1fr))}
.sortrow .fbtn[aria-pressed="true"]{background:var(--dusk-2);border-color:var(--dusk-2)}
section.top{padding:40px 0 60px}
.glance{margin-top:20px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;display:grid;gap:8px}
.glance h3{font-size:20px;margin-bottom:2px} .glance .cost{color:var(--ink-2)}
.toppick{margin-top:34px;display:grid;grid-template-columns:52px 1fr;gap:16px}
.topnum{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;font-family:Fraunces,Georgia,serif;font-size:21px;font-weight:600;color:#fff;background:var(--ok)}
.topcat{font-family:Fraunces,Georgia,serif;font-size:24px;margin:6px 0 12px;display:flex;align-items:center;gap:10px}
.badge{font-family:"Instrument Sans",system-ui,sans-serif;font-size:13px;font-weight:600;color:#fff;background:var(--ok);border-radius:6px;padding:3px 9px}
.method{margin-top:20px;background:var(--flag-bg);border-left:3px solid var(--flag);border-radius:0 12px 12px 0;padding:14px 16px} .method h3{font-size:19px;margin-bottom:6px;color:var(--flag)}
.evidence{margin-top:10px;padding:12px 14px;background:var(--card);border:1px dashed var(--line);border-radius:12px;font-size:15px;color:var(--ink-2)} .evidence b{color:var(--ink)}
.whythis{margin-top:12px;padding:14px 16px;background:var(--ok-bg);border-radius:12px;border:1px solid #B9D6C7} .whythis b{color:var(--ok)}
.runner{margin-top:12px;display:grid;grid-template-columns:72px 1fr;gap:12px;align-items:center;font-size:15px;color:var(--ink-2)}
.runner .thumb{width:72px;height:72px} .runner .rlab{display:block;font-size:12.5px;font-weight:600;text-transform:none;color:var(--ink-2)} .runner b{color:var(--ink)}
@media (max-width:640px){.toppick{grid-template-columns:40px 1fr;gap:12px} .topnum{width:36px;height:36px;font-size:18px}}
.search{flex:1;min-width:220px;font:inherit;font-size:15px;padding:7px 12px;border:1px solid var(--line);border-radius:999px;background:#fff}
@media (max-width:640px){.mini{grid-template-columns:repeat(2,1fr)}}
.thumb img:not([src]){display:none} .thumb.no-img{cursor:default}
"""
JS = re.search(r'JS = r"""(.*?)"""', src2, re.S).group(1)
JS = JS[:JS.index('function imgFail(img){')]  # drop the old inline-handler fallback
JS = JS.replace("var img=t.querySelector('img');if(!img)return;", "var img=t.querySelector('img');if(!img||!img.currentSrc)return;")
JS = JS.replace("history.replaceState(null,'','#'+l+'/'+(v?v.dataset.view:'routine'));",
                "try{history.replaceState(null,'','#'+l+'/'+(v?v.dataset.view:'routine'));}catch(e){}")
JS += r"""
(function(){
  // Photos: a downloaded copy listed in images/photos.js wins; otherwise, when online, the retailer photo loads
  // (then the second candidate where known). A card whose photo cannot load shows the brand initial instead.
  var have=(window.PHOTOS&&typeof window.PHOTOS==='object')?window.PHOTOS:{};
  function none(img){img.removeAttribute('src');img.parentNode.classList.add('no-img');}
  function apply(){
    var online=navigator.onLine!==false;
    document.querySelectorAll('img[data-pid]').forEach(function(img){
      var id=img.dataset.pid, target=(have[id]?'images/'+have[id]:'')||(online&&img.dataset.remote)||'';
      if(!img.dataset.bound){img.dataset.bound='1';img.addEventListener('error',function(){
        var cur=img.getAttribute('src');
        if(have[id] && cur==='images/'+have[id] && navigator.onLine!==false && img.dataset.remote){img.src=img.dataset.remote;return;}
        if(img.dataset.remote2 && cur===img.dataset.remote){img.src=img.dataset.remote2;return;}
        none(img);});}
      if(!target){none(img);return;}
      img.parentNode.classList.remove('no-img');
      if(img.getAttribute('src')!==target) img.src=target;
    });
  }
  window.addEventListener('online',apply); apply();
})();
"""
JS = JS.replace("setView(h[1]==='products'?'products':'routine');", "setView((h[1]==='products'||h[1]==='top')?h[1]:'routine');")
JS = JS.replace("var fcat='all',forg='all';", "var fcat='all',forg='all',fbud='all',fsort='default',fq='';")
JS = JS.replace("var show=(fcat==='all'||c.dataset.cat===fcat)&&(forg==='all'||c.dataset.origin===forg);",
                "var okOrg=(forg==='all')||(forg==='ph'?(c.dataset.origin==='ph'||c.dataset.origin==='current'):c.dataset.origin===forg);"
                "var okQ=!fq||(c.dataset.search||'').indexOf(fq)>-1;var show=(fcat==='all'||c.dataset.cat===fcat)&&okOrg&&(fbud==='all'||parseFloat(c.dataset.price)<=500)&&okQ;")
JS = JS.replace("  applyFilters();\n  // lightbox",
"""  document.queraySelectorAll;
  document.querySelectorAll('[data-search-input]').forEach(function(i){i.addEventListener('input',function(){fq=i.value.trim().toLowerCase();document.querySelectorAll('[data-search-input]').forEach(function(x){if(x!==i)x.value=i.value});applyFilters();})});
  document.querySelectorAll('[data-fbud]').forEach(function(b){b.addEventListener('click',function(){fbud=b.dataset.fbud;document.querySelectorAll('[data-fbud]').forEach(function(x){x.setAttribute('aria-pressed',String(x.dataset.fbud===fbud))});applyFilters();})});
  function applySort(){document.querySelectorAll('.pgrid').forEach(function(g){var cards=Array.from(g.querySelectorAll('.card'));cards.sort(function(a,b){if(fsort==='default')return (+a.dataset.order)-(+b.dataset.order);var d=parseFloat(a.dataset.price)-parseFloat(b.dataset.price);return fsort==='asc'?d:-d;});cards.forEach(function(c){g.appendChild(c)});});}
  document.querySelectorAll('[data-sort]').forEach(function(b){b.addEventListener('click',function(){fsort=b.dataset.sort;document.querySelectorAll('[data-sort]').forEach(function(x){x.setAttribute('aria-pressed',String(x.dataset.sort===fsort))});applySort();})});
  applyFilters();
  // lightbox""").replace("  document.queraySelectorAll;\n", "")

# ------------------------------------------------------------------ render
def thumb(pid):
    p = P[pid]
    cap = html.escape(f'<b>{E(p["brand"])}</b> {E(p["name"])}<small>{E(V[pid][0][0])}</small>', quote=True)
    remote = (f' data-remote="{E(p["img"])}"' if p.get('img') else '') + (f' data-remote2="{E(p["img_alt"])}"' if p.get('img_alt') else '')
    img = f'<img alt="{E(p["brand"])} {E(p["name"])}" loading="lazy" referrerpolicy="no-referrer" data-pid="{pid}"{remote}>'
    return (f'<button type="button" class="thumb" data-caption="{cap}" data-initial="{E(p["brand"][0])}" '
            f'aria-label="{E(p["brand"])} {E(p["name"])}">{img}</button>')

def vtable(pid, lang):
    u = UI[lang]
    rows = ''.join(f'<tr><td>{E(s)}</td><td>{E(pr)}</td><td>{E(le if lang=="en" else lt)}</td></tr>' for s, pr, n, le, lt in V[pid])
    return f'<table class="vtab"><thead><tr><th>{E(u["s_size"])}</th><th>{E(u["s_price"])}</th><th>{E(u["s_lasts"])}</th></tr></thead><tbody>{rows}</tbody></table>'

def card(pid, lang, with_fit=False, order=0, slot=None):
    p = P[pid]; u = UI[lang]; cat = CAT_OF[pid]
    slot = slot or (PRIMARY_SLOT.get(pid, (None, None))[1]) or ('current' if p['region'] == 'current' else p['region'])
    label = SLOT_LABEL[slot][lang] if slot in SLOT_LABEL else u['region'][p['region']]
    cls = 'card current' if slot == 'current' else ('card budget' if slot.endswith('_budget') else 'card')
    chips = ''.join(f'<span class="chip">{E(a)}</span>' for a in p['actives'][lang])
    tag = f'<span class="tag">{E(u["budget_only"])}</span>' if V[pid][0][2] <= 500 else ''
    fit = f'<div><dt>{E(u["fits_l"])}</dt><dd>{E(CAT_LABEL[cat][lang])}: {E(CAT_STEP[cat][lang])}</dd></div>' if with_fit else ''
    return f'''
<article class="{cls}" data-cat="{cat}" data-origin="{p['region']}" data-price="{V[pid][0][2]}" data-order="{order}" data-search="{html.escape((p['brand']+' '+p['name']+' '+' '.join(p['actives'][lang])+' '+ORIGIN_LABEL[p['region']][lang]+' '+CAT_LABEL[cat][lang]).lower(), quote=True)}">
  {thumb(pid)}
  <div>
    <div class="region">{E(label)}{tag}</div>
    <div class="pname">{E(p['brand'])} <small>{E(p['name'])}</small></div>
    <dl class="meta">
      <div><dt>{E(u['sizes_l'])}</dt><dd>{vtable(pid, lang)}</dd></div>
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
    u = UI[lang]; slots = step['slots']; prods = step['products']
    main = [(sl, p) for sl, p in slots if not sl.endswith('_budget')]; bud = [(sl, p) for sl, p in slots if sl.endswith('_budget')]
    cards = ''.join(card(pid, lang, slot=sl) for sl, pid in main)
    if bud: cards += f'</div><div class="divider">{E(u["budget_h"])}</div><div class="cards">' + ''.join(card(pid, lang, slot=sl) for sl, pid in bud)
    return f'''<div class="step"><div class="num" aria-hidden="true">{n}</div><div>
<h3>{E(step['title'][lang])}</h3>{howto(step, lang)}<div class="pick">{E(u['pick_n'].replace('{n}', str(len(prods))))}</div>
<div class="cards">{cards}</div></div></div>'''

def compact_step(n, step, lang):
    u = UI[lang]; minis = ''
    for sl, pid in step['slots']:
        p = P[pid]; c = ' class="current"' if sl == 'current' else ''
        minis += f'<figure{c}>{thumb(pid)}<figcaption><b>{E(p["brand"])}</b>{E(p["name"])}</figcaption></figure>'
    return f'''<div class="step"><div class="num" aria-hidden="true">{n}</div><div>
<h3>{E(step['title'][lang])}</h3><div class="compact"><p><b>{E(u['same_l'])}</b> {E(step['body'][lang])}</p><div class="mini">{minis}</div></div></div></div>'''

exec(src2[src2.index('def timeline_svg(lang):'):src2.index('def routine_block(lang):')])

def routine_block(lang):
    u = UI[lang]
    how_items = ''.join(f'<li><b>{E(a)}</b> {E(b)}</li>' for a, b in u['how'])
    wake = ''.join(full_step(i + 1, s, lang) for i, s in enumerate(WAKE))
    sleep = ''.join(compact_step(i + 1, s, lang) if s.get('compact') else full_step(i + 1, s, lang) for i, s in enumerate(SLEEP))
    gloss = ''
    for gtitle, entries in GLOSSARY:
        rows = ''
        for e in entries:
            found = ''.join(f'<span class="chip">{E(P[pid]["brand"])}</span>' for pid in e['ids'] if pid in VISIBLE)
            rows += f'<div class="term"><div class="t">{E(e["name"][lang])}</div><div><p class="d">{E(e[lang])}</p><div class="found"><span>{E(u["found_l"])}</span>{found}</div></div></div>'
        gloss += f'<div class="ggroup"><h3>{E(gtitle[lang])}</h3>{rows}</div>'
    notes = ''.join(f'<li>{E(n)}</li>' for n in u['notes'])
    return f'''<div class="l-{lang}" lang="{lang}">
<header class="top"><div class="wrap"><h1>{E(u['title'])}</h1><p class="lede">{E(u['intro'])}</p>
<div class="tl-card"><h3>{E(u['tl_title'])}</h3>{timeline_svg(lang)}<p class="tl-note">{E(u['tl_note'])}</p></div>
<div class="how"><h2>{E(u['how_h'])}</h2><ul>{how_items}</ul><p class="photohint">{E(u['photo_hint'])}</p></div></div></header>
<section class="routine day"><div class="wrap"><h2>{E(u['wake_h'])}</h2><p class="rsub">{E(u['wake_sub'])}</p>{wake}</div></section>
<section class="routine night"><div class="wrap"><h2>{E(u['sleep_h'])}</h2><p class="rsub">{E(u['sleep_sub'])}</p>{sleep}
<div class="pimple"><h3>{E(u['pimple_h'])}</h3><p>{E(u['pimple'])}</p></div></div></section>
<section class="gloss"><div class="wrap"><h2>{E(u['gloss_h'])}</h2><p class="gsub">{E(u['gloss_sub'])}</p>{gloss}</div></section>
<footer><div class="wrap"><h3>{E(u['notes_h'])}</h3><ul>{notes}</ul></div></footer></div>'''

def products_block(lang):
    u = UI[lang]
    cats = [('all', u['all'])] + [(c, CAT_LABEL[c][lang]) for c in ('cleanser','serum','moisturizer','sunscreen','lip')]
    origins = [('all', u['all'])] + [(o, ORIGIN_LABEL[o][lang]) for o in ('ph','intl','kr','jp')]
    def btns(attr, items, sel):
        return ''.join(f'<button type="button" class="fbtn" data-{attr}="{v}" aria-pressed="{"true" if v==sel else "false"}">{E(t)}</button>' for v, t in items)
    cards = ''.join(card(pid, lang, with_fit=True, order=i) for i, pid in enumerate(VISIBLE))
    return f'''<div class="l-{lang}" lang="{lang}"><section class="products"><div class="wrap">
<h2>{E(u['products_h'])}</h2><p class="gsub">{E(u['products_sub'])}</p>
<div class="filters">
<div class="frow"><label class="flab" for="q-{lang}">{E(u['search_l'])}</label><input id="q-{lang}" class="search" type="search" data-search-input placeholder="{E(u['search_ph'])}" autocomplete="off"></div>
<div class="frow"><span class="flab">{E(u['filter_type'])}</span>{btns('fcat', cats, 'all')}</div>
<div class="frow"><span class="flab">{E(u['filter_origin'])}</span>{btns('forg', origins, 'all')}</div>
<div class="frow"><span class="flab">{E(u['filter_budget'])}</span>{btns('fbud', [('all', u['all']), ('500', u['budget_only'])], 'all')}</div>
<div class="frow sortrow"><span class="flab">{E(u['sort_l'])}</span>{btns('sort', [('default', u['sort_default']), ('asc', u['sort_asc']), ('desc', u['sort_desc'])], 'default')}</div>
</div>
<p class="count"><span data-n data-tpl="{E(u['showing'])}"></span></p>
<div class="pgrid">{cards}</div></div></section></div>'''

def top_block(lang):
    u = UI[lang]; items = ''
    for i, t in enumerate(TOP):
        r = P[t['runner']]
        items += f"""<div class="toppick"><div class="topnum" aria-hidden="true">{i+1}</div><div>
<div class="topcat"><span class="badge">{E(u['top_badge'])}</span> {E(TOPCAT[t['cat']][lang])}</div>
{card(t['pick'], lang, with_fit=True)}
<div class="whythis"><b>{E(u['why_this'])}.</b> {E(t['why'][lang])}</div>
<div class="evidence"><b>{E(u['evidence_l'])}.</b> {E(t['evidence'][lang])}</div>
<div class="runner">{thumb(t['runner'])}<div><span class="rlab">{E(u['runner_l'])}</span><b>{E(r['brand'])} {E(r['name'])}</b> — {E(t['rwhy'][lang])} ({E(V[t['runner']][0][1])}).</div></div>
</div></div>"""
    total = sum(V[t['pick']][0][2] for t in TOP)
    return f"""<div class="l-{lang}" lang="{lang}"><section class="top"><div class="wrap">
<h2>{E(u['top_h'])}</h2><p class="gsub">{E(u['top_sub'])}</p>
<div class="method"><h3>{E(u['method_h'])}</h3><p>{E(u['method'])}</p></div>
<div class="glance"><h3>{E(u['glance_h'])}</h3><p>{E(u['glance_wake'])}</p><p>{E(u['glance_sleep'])}</p><p class="cost"><b>{E(u['cost_l'])}:</b> about ₱{total:,} {E(u['cost_note'])}</p></div>
{items}</div></section></div>"""

def page():
    ue, ut = UI['en'], UI['tl']
    return f'''<!DOCTYPE html>
<html lang="en" data-lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Personal care (English + Tagalog)</title>
<script>if(navigator.onLine!==false){{var l=document.createElement('link');l.rel='stylesheet';l.href='https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Instrument+Sans:wght@400;500;600&display=swap';document.head.appendChild(l);}}</script>
<style>{CSS}</style></head>
<body>
<nav class="topbar"><div class="wrap">
  <div class="tb-title">Personal care</div>
  <div class="seg" role="group" aria-label="View">
    <button type="button" data-view-btn="routine" aria-pressed="true"><span class="l-en">{E(ue['nav_routine'])}</span><span class="l-tl">{E(ut['nav_routine'])}</span></button>
    <button type="button" data-view-btn="top" aria-pressed="false"><span class="l-en">{E(ue['nav_top'])}</span><span class="l-tl">{E(ut['nav_top'])}</span></button>
    <button type="button" data-view-btn="products" aria-pressed="false"><span class="l-en">{E(ue['nav_products'])}</span><span class="l-tl">{E(ut['nav_products'])}</span></button>
  </div>
  <div class="seg" role="group" aria-label="Language">
    <button type="button" data-lang-btn="en" aria-pressed="true">English</button>
    <button type="button" data-lang-btn="tl" aria-pressed="false">Tagalog</button>
  </div>
</div></nav>
<main>
<div data-view="routine">{routine_block('en')}{routine_block('tl')}</div>
<div data-view="top" hidden>{top_block('en')}{top_block('tl')}</div>
<div data-view="products" hidden>{products_block('en')}{products_block('tl')}</div>
</main>
<div class="lb" id="lb" hidden role="dialog" aria-modal="true" aria-label="Product photo">
  <button type="button" class="lb-close"><span class="l-en">{E(ue['lb_close'])}</span><span class="l-tl">{E(ut['lb_close'])}</span></button>
  <figure><img id="lb-img" alt=""><figcaption><span id="lb-cap"></span><small><span class="l-en">{E(ue['lb_hint'])}</span><span class="l-tl">{E(ut['lb_hint'])}</span></small></figcaption></figure>
</div>
<script src="images/photos.js"></script>
<script>{JS}</script>
</body></html>
'''

# ------------------------------------------------------------------ write into the site folder (never deletes anything you downloaded)
dist = SITE
os.makedirs(os.path.join(dist, 'images'), exist_ok=True)
open(os.path.join(dist, 'index.html'), 'w', encoding='utf-8').write(page())
if not os.path.exists(os.path.join(dist, 'images', 'photos.js')):
    open(os.path.join(dist, 'images', 'photos.js'), 'w', encoding='utf-8').write('// Written by get-photos.sh: lists the product photos that were downloaded into this folder.\nwindow.PHOTOS={};\n')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'
with_img = [pid for pid in VISIBLE if P[pid].get('img')]
lines = ['#!/bin/bash', '# Downloads the real product photos into ./images so index.html shows them offline.',
         '# Run:  bash get-photos.sh   (or double-click get-photos.command; if macOS blocks it, right-click > Open)',
         'cd "$(dirname "$0")" || exit 1', 'mkdir -p images', f'UA="{UA}"', 'ok=0; fail=0; saved=()',
         'get(){ local id="$1"; shift', '  for u in "$@"; do',
         '    if curl -fsSL --retry 2 --max-time 40 -A "$UA" -e "https://www.watsons.com.ph/" -o "images/$id.jpg" "$u"; then',
         '      echo "  saved  images/$id.jpg"; ok=$((ok+1)); saved+=("$id"); return; fi', '  done',
         '  rm -f "images/$id.jpg"; echo "  FAILED $id (the page loads it from the retailer when online)"; fail=$((fail+1)); }',
         f'echo "Fetching {len(with_img)} product photos..."']
for pid in with_img:
    p = P[pid]; urls = [p['img']] + ([p['img_alt']] if p.get('img_alt') else [])
    lines.append('get ' + pid + ' ' + ' '.join(f'"{u}"' for u in urls))
lines += ['json="{"; sep=""',
          'for f in images/*.jpg; do [ -e "$f" ] || continue; id="$(basename "$f" .jpg)"; json="$json$sep\\"$id\\":\\"$id.jpg\\""; sep=","; done',
          'json="$json}"',
          'printf \'// Written by get-photos.sh: lists the product photos that were downloaded into this folder.\\nwindow.PHOTOS=%s;\\n\' "$json" > images/photos.js',
          'echo "Done: $ok photos saved, $fail failed. images/photos.js updated."', 'echo "Now open index.html in your browser."']
script = '\n'.join(lines) + '\n'
for name in ('get-photos.sh', 'get-photos.command'):
    pth = os.path.join(dist, name); open(pth, 'w', encoding='utf-8').write(script); os.chmod(pth, 0o755)
print(f'built {os.path.join(dist, "index.html")} | visible products: {len(VISIBLE)} (of {len(P)} defined) | with photo URL: {len(with_img)} | top picks: {len(TOP)}')
if '--zip' in sys.argv:
    zpath = dist.rstrip('/') + '.zip'
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(dist):
            dirs[:] = [d for d in dirs if d != '.git']
            for fn in sorted(files):
                if fn.endswith('.jpg'): continue
                full = os.path.join(root, fn); arc = os.path.relpath(full, os.path.dirname(dist))
                zi = zipfile.ZipInfo.from_file(full, arc); zi.external_attr = (0o755 if fn.endswith(('.sh', '.command')) else 0o644) << 16
                z.writestr(zi, open(full, 'rb').read(), compress_type=zipfile.ZIP_DEFLATED)
    print('zip:', zpath)
