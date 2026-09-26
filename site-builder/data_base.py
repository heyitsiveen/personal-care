# -*- coding: utf-8 -*-
# Base data model: 19 original products, UI strings, routine steps, glossary. Loaded by data_v2.py.
# -*- coding: utf-8 -*-
"""Builds skincare-routine-en.html and skincare-routine-tl.html from one data model."""
import html, os

def E(s):
    return html.escape(s, quote=False)

# --------------------------------------------------------------------------- products
P = {}

def prod(pid, **kw):
    kw['id'] = pid
    P[pid] = kw

prod('klued', brand='Klued', name='Barrier Support Hydrating Jelly Cleanser', region='current',
     img='https://storage.skinsort.com/owajo7akkfj64y1bhb5fcxry36vv',
     price={'en': 'You already own this (120 ml)', 'tl': 'Nasa iyo na ito (120 ml)'},
     where={'en': "Klued’s official Shopee and Lazada stores", 'tl': 'Official Shopee at Lazada store ng Klued'},
     actives={'en': ['Niacinamide', 'Hyaluronic acid', 'Ceramide NP', 'Glycerin', 'Squalene', 'Shea butter'],
              'tl': ['Niacinamide', 'Hyaluronic acid', 'Ceramide NP', 'Glycerin', 'Squalene', 'Shea butter']},
     why={'en': 'A low-foam jelly that cleans without stripping. The ceramide, niacinamide and hyaluronic acid trio keeps your barrier calm, which is exactly the baseline oily, occasionally pimple-prone skin needs.',
          'tl': 'Jelly na kaunti lang ang bula, naglilinis nang hindi nagpapaka-dry. Ang ceramide, niacinamide at hyaluronic acid ay nagpapanatiling kalmado ng skin barrier mo, na siyang tamang pundasyon para sa oily na balat na paminsan-minsang tinutubuan ng pimple.'},
     flag={'en': 'Uses cocamide DEA, an older foaming agent many brands have phased out. It is considered safe at cosmetic levels, but if you ever notice tightness or irritation after washing, that is a reason to try one of the alternatives.',
           'tl': 'Gumagamit ng cocamide DEA, isang lumang pampabula na tinigil na ng maraming brand. Itinuturing na ligtas sa cosmetic na dami, pero kung makaramdam ka ng paninikip o iritasyon pagkahugas, dahilan iyon para subukan ang isa sa mga alternatibo.'})

prod('cerave', brand='CeraVe', name='Foaming Cleanser', region='intl',
     img='https://medias.watsons.com.ph/publishing/50053257-v75cguLk-zoom.png?version=1762914671',
     price={'en': '₱495 (88 ml) · ₱895 (236 ml) · ₱1,334 (473 ml)', 'tl': '₱495 (88 ml) · ₱895 (236 ml) · ₱1,334 (473 ml)'},
     where={'en': 'Watsons (in store and online), Mercury Drug', 'tl': 'Watsons (tindahan at online), Mercury Drug'},
     actives={'en': ['Ceramides NP, AP, EOP', 'Niacinamide', 'Hyaluronic acid', 'Glycerin', 'Cholesterol', 'Phytosphingosine'],
              'tl': ['Ceramides NP, AP, EOP', 'Niacinamide', 'Hyaluronic acid', 'Glycerin', 'Cholesterol', 'Phytosphingosine']},
     why={'en': 'Made specifically for normal-to-oily skin and built on the same ceramide, niacinamide and hyaluronic acid logic as your Klued, so switching changes nothing about how your routine works. Dermatologist-developed, fragrance-free, and the most-reviewed cleanser of this group on Watsons PH.',
          'tl': 'Ginawa para sa normal hanggang oily na balat at nakabase sa parehong ceramide, niacinamide at hyaluronic acid na lohika ng Klued mo, kaya walang magbabago sa takbo ng routine mo kung papalit ka. Binuo kasama ng mga dermatologist, walang pabango, at ito ang may pinakamaraming review na cleanser sa grupong ito sa Watsons PH.'},
     flag={'en': 'The 355 ml pump bottle still sold in some stores is an older US formula with parabens. The 88, 236 and 473 ml sizes listed here carry the current formula.',
           'tl': 'Ang 355 ml na pump bottle na ibinebenta pa sa ilang tindahan ay lumang US formula na may parabens. Ang 88, 236 at 473 ml na nakalista dito ang may kasalukuyang formula.'})

prod('cosrx', brand='COSRX', name='Low pH Good Morning Gel Cleanser', region='kr',
     img='https://medias.watsons.com.ph/publishing/COSRX_Image1_50044422-eHzI0fRd-zoom.jpg?version=1785153905',
     price={'en': '₱560 (150 ml) · ₱280 (50 ml)', 'tl': '₱560 (150 ml) · ₱280 (50 ml)'},
     where={'en': 'Watsons (in store and online)', 'tl': 'Watsons (tindahan at online)'},
     actives={'en': ['Tea tree leaf oil', 'Betaine salicylate (gentle BHA)', 'Allantoin', 'Botanical extracts', 'pH about 5.5'],
              'tl': ['Tea tree leaf oil', 'Betaine salicylate (mabining BHA)', 'Allantoin', 'Mga botanical extract', 'pH mga 5.5']},
     why={'en': 'Its pH sits close to your skin’s own, a whisper of BHA keeps pores from clogging, and tea tree oil helps with the occasional pimple. Of the three alternatives this is the closest fit for your skin.',
          'tl': 'Malapit ang pH nito sa sariling pH ng balat mo, ang kaunting BHA ay pumipigil sa pagbara ng pores, at tumutulong ang tea tree oil sa paminsan-minsang pimple. Sa tatlong alternatibo, ito ang pinakabagay sa balat mo.'},
     flag={'en': 'Noticeable herbal tea-tree scent (from the oil itself, not added perfume). It exfoliates very lightly, which is fine daily for oily skin, but pause it if your skin ever feels raw.',
           'tl': 'May kapansin-pansing herbal na amoy ng tea tree (mula sa mismong langis, hindi dagdag na pabango). Napakabanayad ang pag-exfoliate nito, na ayos araw-araw para sa oily na balat, pero itigil muna kung maging hilaw ang pakiramdam ng balat.'})

prod('senka', brand='Senka (Shiseido)', name='Perfect Whip', region='jp',
     img='https://medias.watsons.com.ph/publishing/SENKA_IMAGE%201_50010099-w24fwJFL-zoom.jpg?version=1763367090',
     price={'en': '₱289 (120 g) · ₱139 (50 g)', 'tl': '₱289 (120 g) · ₱139 (50 g)'},
     where={'en': 'Watsons, Mercury Drug, most supermarkets', 'tl': 'Watsons, Mercury Drug, karamihan ng supermarket'},
     actives={'en': ['Glycerin', 'Dipropylene glycol', 'Soap-based lather (fatty acids + potassium hydroxide)', 'Beeswax', 'Aqua-in-Pool moisture complex (brand claim)'],
              'tl': ['Glycerin', 'Dipropylene glycol', 'Bulang soap-based (fatty acids + potassium hydroxide)', 'Beeswax', 'Aqua-in-Pool moisture complex (claim ng brand)']},
     why={'en': 'Japan’s best-selling face wash for more than a decade. The dense whipped foam removes oil very thoroughly, which is why so many oily-skinned Filipinos swear by it, and it is the cheapest option in this step.',
          'tl': 'Pinakamabiling face wash sa Japan sa loob ng mahigit isang dekada. Ang makapal na whipped foam ay lubusang nag-aalis ng langis, kaya maraming Pilipinong oily ang balat ang sumusumpa dito, at ito ang pinakamurang opsyon sa step na ito.'},
     flag={'en': 'This is a soap-based, higher-pH foam with fragrance and a little alcohol, so it is the least barrier-friendly pick here. If your face feels tight or squeaky afterwards, that is stripping: switch to the Perfect Whip Acne Care variant (₱309) or back to a gel like COSRX.',
           'tl': 'Ito ay soap-based at mas mataas ang pH, may pabango at kaunting alcohol, kaya ito ang pinakahindi barrier-friendly dito. Kung masikip o parang “squeaky” ang mukha mo pagkatapos, iyon ang pagka-strip: lumipat sa Perfect Whip Acne Care (₱309) o bumalik sa gel tulad ng COSRX.'})

prod('dermorepubliq', brand='DermoRepubliq', name='5% Niacinamide + Hyaluronic Acid Serum (Sensitive Skin Formula)', region='current',
     img='https://storage.skinsort.com/6iuksczisp2cvqcd17z4s4sgnmyx',
     price={'en': 'You already own this (30 ml)', 'tl': 'Nasa iyo na ito (30 ml)'},
     where={'en': 'DermoRepubliq’s official Shopee and Lazada stores and website', 'tl': 'Official Shopee at Lazada store at website ng DermoRepubliq'},
     actives={'en': ['Niacinamide 5%', 'Hyaluronic acid', 'Snail secretion filtrate', 'Allantoin', 'Aloe leaf juice'],
              'tl': ['Niacinamide 5%', 'Hyaluronic acid', 'Snail secretion filtrate', 'Allantoin', 'Aloe leaf juice']},
     why={'en': 'A well-judged 5%: enough to help with oil and redness without the stinging some people get at 10%. Snail filtrate and allantoin add soothing, and it is fragrance-free.',
          'tl': 'Tamang-tama ang 5%: sapat para tumulong sa langis at pamumula nang walang paghapdi na nararanasan ng ilan sa 10%. Nagdadagdag ng pampakalma ang snail filtrate at allantoin, at wala itong pabango.'},
     flag={'en': 'Nothing to flag for your skin type. If you switch, it is for variety or convenience, not because this is lacking.',
           'tl': 'Walang dapat bantayan para sa uri ng balat mo. Kung papalit ka, para lang iyon sa iba o sa kaginhawaan, hindi dahil may kulang ito.'})

prod('ordinary', brand='The Ordinary', name='Niacinamide 10% + Zinc 1%', region='intl',
     img='https://medias.watsons.com.ph/publishing/50033473-Ewl4IU27-zoom.jpg?version=1761814703',
     price={'en': '₱849 (30 ml) · ₱1,399 (60 ml)', 'tl': '₱849 (30 ml) · ₱1,399 (60 ml)'},
     where={'en': 'Watsons online and selected branches (the 30 ml showed “out of stock” online on 11 September 2026)', 'tl': 'Watsons online at ilang branch (nakalagay na “out of stock” online ang 30 ml noong 11 Setyembre 2026)'},
     actives={'en': ['Niacinamide 10%', 'Zinc PCA 1%'], 'tl': ['Niacinamide 10%', 'Zinc PCA 1%']},
     why={'en': 'The world’s best-known niacinamide serum, and zinc PCA adds a bit of extra oil control. Simple, fragrance-free, water-light.',
          'tl': 'Ang pinakakilalang niacinamide serum sa mundo, at nagdadagdag ng kaunting oil control ang zinc PCA. Simple, walang pabango, kasing gaan ng tubig.'},
     flag={'en': 'Double the strength of your current serum. Some people get flushing, stinging or pilling at 10%, so start every other day. The Ordinary itself states this is not an acne treatment.',
           'tl': 'Doble ng lakas ng kasalukuyang serum mo. May mga namumula, humahapdi o nag-“pilling” sa 10%, kaya magsimula sa bawat ikalawang araw. Sinasabi mismo ng The Ordinary na hindi ito acne treatment.'})

prod('anua', brand='Anua', name='Niacinamide 10% + TXA 3% Serum', region='kr',
     img='https://medias.watsons.com.ph/publishing/WTCPH-50058923-back-zoom.jpg?version=1785257474',
     price={'en': '₱1,500 (30 ml)', 'tl': '₱1,500 (30 ml)'},
     where={'en': 'Watsons (in store and online)', 'tl': 'Watsons (tindahan at online)'},
     actives={'en': ['Niacinamide 10%', 'Tranexamic acid 3%', 'Arbutin + alpha-arbutin 2%', 'Hyaluronic acids', 'Panthenol', 'Betaine salicylate', 'Ceramide NP', 'Centella'],
              'tl': ['Niacinamide 10%', 'Tranexamic acid 3%', 'Arbutin + alpha-arbutin 2%', 'Mga hyaluronic acid', 'Panthenol', 'Betaine salicylate', 'Ceramide NP', 'Centella']},
     why={'en': 'The current K-beauty favourite: one bottle covers oil control, brightening, hydration and calming, with a light watery texture that suits oily skin.',
          'tl': 'Ang kasalukuyang paborito sa K-beauty: isang bote ang sumasaklaw sa oil control, pagpapaliwanag, hydration at pagpapakalma, na may magaang matubig na texture na bagay sa oily na balat.'},
     flag={'en': 'The priciest serum here, and its brightening focus (tranexamic acid, arbutin) solves a problem you do not have. It also carries small amounts of plant oils (macadamia, olive, jojoba, grape seed): patch-test along the jaw for a week if you break out easily.',
           'tl': 'Pinakamahal na serum dito, at ang pokus nito sa pagpapaliwanag (tranexamic acid, arbutin) ay sagot sa problemang wala ka. May kaunting langis ng halaman din ito (macadamia, olive, jojoba, grape seed): mag-patch test sa panga sa loob ng isang linggo kung madali kang tubuan ng pimple.'})

prod('melanocc', brand='Melano CC (Rohto)', name='Vitamin C Brightening Essence', region='jp',
     img='https://medias.watsons.com.ph/publishing/Melano%20CC_Image%201_50059679-uW4ABLPJ-zoom.jpg?version=1782691945',
     price={'en': '₱799 (20 ml)', 'tl': '₱799 (20 ml)'},
     where={'en': 'Watsons (in store and online)', 'tl': 'Watsons (tindahan at online)'},
     actives={'en': ['Ascorbic acid (pure vitamin C)', 'Ascorbyl tetraisopalmitate', 'Vitamin E acetate', 'Dipotassium glycyrrhizate (licorice)', 'O-Cymen-5-OL (antibacterial)', 'Alpinia seed extract'],
              'tl': ['Ascorbic acid (purong vitamin C)', 'Ascorbyl tetraisopalmitate', 'Vitamin E acetate', 'Dipotassium glycyrrhizate (licorice)', 'O-Cymen-5-OL (antibacterial)', 'Alpinia seed extract']},
     why={'en': 'Japan’s number-one essence, and the most pimple-oriented serum here: an antibacterial ingredient plus vitamins C and E to fade the marks pimples leave behind. The small tube lasts because you use a tiny amount.',
          'tl': 'Number-one essence sa Japan, at ang pinaka-nakatuon sa pimple na serum dito: antibacterial na sangkap kasama ng vitamin C at E para kumupas ang markang iniiwan ng pimple. Tumatagal ang maliit na tube dahil kaunti lang ang gamit.'},
     flag={'en': 'Not a niacinamide serum; it is the closest Japanese drugstore serum for oily, pimple-prone skin. Contains alcohol and fragrance, so a light tingle is normal but stinging is not. It layers fine under your Camou moisturizer.',
           'tl': 'Hindi ito niacinamide serum; ito ang pinakamalapit na Japanese drugstore serum para sa oily at pimple-prone na balat. May alcohol at pabango, kaya normal ang bahagyang kiliti pero hindi ang paghapdi. Ayos itong ipatong sa ilalim ng Camou moisturizer mo.'})

prod('camou', brand='Camou', name='Brightening Gel Moisturizer', region='current',
     img='https://storage.skinsort.com/y2cnx74ctauafp39f1rgsu1m7fu0',
     price={'en': 'You already own this (50 g)', 'tl': 'Nasa iyo na ito (50 g)'},
     where={'en': 'Camou’s official Shopee and Lazada stores', 'tl': 'Official Shopee at Lazada store ng Camou'},
     actives={'en': ['Niacinamide 5%', 'Tranexamic acid', 'Alpha-arbutin', 'Beta-glucan', 'Hyaluronic acid', 'Licorice root water', 'Ergothioneine', 'Spirulina extract'],
              'tl': ['Niacinamide 5%', 'Tranexamic acid', 'Alpha-arbutin', 'Beta-glucan', 'Hyaluronic acid', 'Licorice root water', 'Ergothioneine', 'Spirulina extract']},
     why={'en': 'A lightweight, oil-free gel with an unusually generous set of skin-evening actives for its price. The gel texture is right for oily skin in Manila heat.',
          'tl': 'Magaan at oil-free na gel na may hindi karaniwang dami ng aktibong sangkap para pantayin ang balat, para sa presyo nito. Tamang-tama ang gel na texture para sa oily na balat sa init ng Maynila.'},
     flag={'en': 'Contains perfume (parfum). If you ever get itchiness or redness, fragrance is the first suspect; the SKIN1004 and Hada Labo options below are fragrance-free.',
           'tl': 'May pabango (parfum). Kung kumati o mamula ka, ang pabango ang unang suspek; walang pabango ang SKIN1004 at Hada Labo sa ibaba.'})

prod('neutrogena', brand='Neutrogena', name='Hydro Boost Water Gel', region='intl',
     img='https://medias.watsons.com.ph/publishing/WTCPH-10087897-front-zoom.jpg?version=1734062328',
     price={'en': '₱1,154 (50 g); often ₱856–899 on sale · refill pack ₱799', 'tl': '₱1,154 (50 g); madalas ₱856–899 kapag sale · refill pack ₱799'},
     where={'en': 'Watsons, Mercury Drug', 'tl': 'Watsons, Mercury Drug'},
     actives={'en': ['Hyaluronic acid', 'Glycerin', 'Dimethicone'], 'tl': ['Hyaluronic acid', 'Glycerin', 'Dimethicone']},
     why={'en': 'The classic oil-free water gel: instant, cooling hydration that disappears into oily skin without shine. Over a hundred Watsons PH reviews and easy to find anywhere.',
          'tl': 'Ang klasikong oil-free water gel: agad at malamig na hydration na natutunaw sa oily na balat nang walang kintab. Mahigit isandaang review sa Watsons PH at madaling mahanap kahit saan.'},
     flag={'en': 'Contains fragrance and a blue dye, and it has no skin-evening actives at all; it is pure hydration. The refill pack is the same product for about ₱350 less.',
           'tl': 'May pabango at asul na tina, at wala itong kahit anong aktibong sangkap para pantayin ang balat; purong hydration lang. Ang refill pack ay parehong produkto sa mas mababa ng mga ₱350.'})

prod('skin1004', brand='SKIN1004', name='Madagascar Centella Soothing Cream', region='kr',
     img='https://medias.watsons.com.ph/publishing/SKIN1004_Image1_50054236-n5fUhiFS-zoom.jpg?version=1765450794',
     price={'en': '₱1,150 (75 ml); ₱977.50 on sale', 'tl': '₱1,150 (75 ml); ₱977.50 kapag sale'},
     where={'en': 'Watsons (in store and online)', 'tl': 'Watsons (tindahan at online)'},
     actives={'en': ['Centella asiatica extract 72%', 'Ceramides EOP, NS, NP, AP', 'Cholesterol', 'Phytosphingosine', 'Trehalose', 'Beta-glucan', 'Hyaluronic acid', 'Tranexamic acid', 'Dipotassium glycyrrhizate'],
              'tl': ['Centella asiatica extract 72%', 'Ceramides EOP, NS, NP, AP', 'Cholesterol', 'Phytosphingosine', 'Trehalose', 'Beta-glucan', 'Hyaluronic acid', 'Tranexamic acid', 'Dipotassium glycyrrhizate']},
     why={'en': 'A light gel-cream that calms redness and rebuilds the barrier with the same ceramide, cholesterol and fatty-acid trio your skin makes. Ideal while a pimple heals. Fragrance-free.',
          'tl': 'Magaang gel-cream na nagpapakalma ng pamumula at nagbubuo muli ng barrier gamit ang parehong ceramide, cholesterol at fatty acid na ginagawa ng balat mo. Tamang-tama habang gumagaling ang pimple. Walang pabango.'},
     flag={'en': '“Cream” in the name, but it is a light gel-cream; on your oiliest nights use only a pea. The 75 ml tub lasts months, which softens the price.',
           'tl': '“Cream” ang pangalan, pero magaang gel-cream ito; sa pinaka-oily na gabi, kasinlaki ng gisantes lang. Tumatagal ng ilang buwan ang 75 ml, kaya sulit ang presyo.'})

prod('hadalabo', brand='Hada Labo (Rohto)', name='Premium Whitening Water Gel', region='jp',
     img='https://medias.watsons.com.ph/publishing/Hada%20Labo_Image%201_50043925-d3XcCuTB-zoom.jpg?version=1764128094',
     price={'en': '₱920 (50 g) · ₱309 trial size (14 g)', 'tl': '₱920 (50 g) · ₱309 trial size (14 g)'},
     where={'en': 'Watsons (in store and online)', 'tl': 'Watsons (tindahan at online)'},
     actives={'en': ['Niacinamide', 'Alpha-arbutin', '3-O-ethyl ascorbic acid (vitamin C derivative)', 'Hyaluronic acid', 'Centella', 'Trehalose', 'Honey extract', 'Urea', 'Scutellaria root'],
              'tl': ['Niacinamide', 'Alpha-arbutin', '3-O-ethyl ascorbic acid (derivative ng vitamin C)', 'Hyaluronic acid', 'Centella', 'Trehalose', 'Honey extract', 'Urea', 'Scutellaria root']},
     why={'en': 'The closest match to your Camou: niacinamide, alpha-arbutin and a vitamin C derivative in an ultra-light water gel that Hada Labo labels for normal-to-oily skin. Fragrance-, alcohol- and colorant-free, and the ₱309 trial size lets you test it first.',
          'tl': 'Pinakamalapit sa Camou mo: niacinamide, alpha-arbutin at derivative ng vitamin C sa napakagaang water gel na nilagyan ng Hada Labo ng label para sa normal hanggang oily na balat. Walang pabango, alcohol at tina, at puwede mo munang subukan ang ₱309 na trial size.'},
     flag={'en': '“Whitening” here means brightening and evening tone; it does not bleach skin. This is the Southeast Asian version (made in China) and its formula differs from the Japan-market Shirojyun gel.',
           'tl': 'Ang “whitening” dito ay nangangahulugang pagpapaliwanag at pagpapantay ng kulay; hindi ito nagpapaputi ng balat. Ito ang bersyong para sa Southeast Asia (gawa sa China) at iba ang formula nito sa Shirojyun gel na ibinebenta sa Japan.'})

prod('hikari', brand='Hikari (Beauty&U)', name='UltraFresh Sunscreen SPF50 PA++++', region='current',
     img='https://storage.skinsort.com/fpntt11o41fy2195bdtyedc7j7l9',
     price={'en': 'You already own this (50 ml)', 'tl': 'Nasa iyo na ito (50 ml)'},
     where={'en': 'Beauty&U’s official Shopee and Lazada stores', 'tl': 'Official Shopee at Lazada store ng Beauty&U'},
     actives={'en': ['Octinoxate', 'Avobenzone', 'Oxybenzone', 'Titanium dioxide', 'Zinc oxide', 'Hyaluronic acid', 'Aloe', 'Vitamin E acetate'],
              'tl': ['Octinoxate', 'Avobenzone', 'Oxybenzone', 'Titanium dioxide', 'Zinc oxide', 'Hyaluronic acid', 'Aloe', 'Vitamin E acetate']},
     why={'en': 'An affordable hybrid gel-cream (chemical plus mineral filters) that gives broad-spectrum protection with a fresh finish that oily skin tolerates.',
          'tl': 'Abot-kayang hybrid gel-cream (chemical at mineral filters) na nagbibigay ng broad-spectrum na proteksyon na may sariwang finish na kaya ng oily na balat.'},
     flag={'en': 'Its filters are the older generation: avobenzone breaks down in sunlight unless stabilized, and oxybenzone is the filter most often linked to skin allergy and is being phased down in the EU. It also has a red dye. For long daylight exposure, the three alternatives use modern, photostable filters.',
           'tl': 'Lumang henerasyon ang mga filter nito: nasisira ang avobenzone sa araw kung hindi na-stabilize, at ang oxybenzone ang filter na pinakamadalas iugnay sa skin allergy at unti-unting inaalis sa EU. May pulang tina rin ito. Para sa matagal na pagkakabilad, mga moderno at photostable na filter ang gamit ng tatlong alternatibo.'})

prod('lrp', brand='La Roche-Posay', name='Anthelios UVMune 400 Oil Control Gel-Cream SPF50+', region='intl',
     img='https://www.laroche-posay.sg/-/media/project/loreal/brand-sites/lrp/apac/sg/products/anthelios/anthelios-uvmune-oil-control-gel-cream-spf50-plus-non-perfumed/lrp-anthelios-uvmune-400-oil-gel-cream-sp-bottle-packshot-front.png',
     price={'en': 'About ₱1,300–1,600 (50 ml)', 'tl': 'Mga ₱1,300–1,600 (50 ml)'},
     where={'en': 'La Roche-Posay’s official Lazada and Shopee stores; selected Watsons branches. Not found on Watsons PH online on 11 September 2026, and not sold at Mercury Drug or St. Joseph.',
            'tl': 'Official Lazada at Shopee store ng La Roche-Posay; ilang branch ng Watsons. Hindi nakita sa Watsons PH online noong 11 Setyembre 2026, at hindi ibinebenta sa Mercury Drug o St. Joseph.'},
     actives={'en': ['Mexoryl 400 (ultra-long UVA filter)', 'Mexoryl XL and SX', 'Tinosorb S', 'Uvinul T150', 'Uvinul A Plus', 'Avobenzone', 'Airlicium silica (oil absorber)', 'Zinc', 'Thermal spring water'],
              'tl': ['Mexoryl 400 (ultra-long UVA filter)', 'Mexoryl XL at SX', 'Tinosorb S', 'Uvinul T150', 'Uvinul A Plus', 'Avobenzone', 'Airlicium silica (sumisipsip ng langis)', 'Zinc', 'Thermal spring water']},
     why={'en': 'The dermatologist favourite for oily skin: dry-touch, mattifying for hours, no white cast, fragrance-free, and the only filter set here that covers ultra-long UVA (380–400 nm), the rays that reach you through windows.',
          'tl': 'Paborito ng mga dermatologist para sa oily na balat: dry-touch, matte sa loob ng ilang oras, walang white cast, walang pabango, at ito lang ang set ng filter dito na sumasaklaw sa ultra-long UVA (380–400 nm), ang mga sinag na umaabot sa iyo sa pamamagitan ng bintana.'},
     flag={'en': 'The most expensive option and the hardest to find in a physical drugstore. Some users find it more cream than gel; the “Oil Control Fluid” version is the runnier sibling if the gel-cream feels heavy.',
           'tl': 'Pinakamahal at pinakamahirap hanapin sa pisikal na botika. Para sa ilan, mas cream ito kaysa gel; ang “Oil Control Fluid” ang mas matubig na kapatid nito kung mabigat ang pakiramdam ng gel-cream.'})

prod('boj', brand='Beauty of Joseon', name='Relief Sun: Rice + Probiotics SPF50+ PA++++', region='kr',
     img='https://medias.watsons.com.ph/publishing/WTCPH-50042242-front-zoom.jpg',
     img_alt='https://medias.watsons.com.ph/publishing/WTCPH-50042242-front-prod.jpg',
     price={'en': '₱1,050 (50 ml); ₱893 on sale', 'tl': '₱1,050 (50 ml); ₱893 kapag sale'},
     where={'en': 'Watsons (in store and online)', 'tl': 'Watsons (tindahan at online)'},
     actives={'en': ['Rice extract 30%', 'Fermented grain extracts (probiotics)', 'Niacinamide', 'Uvinul A Plus', 'Ethylhexyl triazone', 'Tinosorb M', 'Iscotrizinol'],
              'tl': ['Rice extract 30%', 'Fermented grain extracts (probiotics)', 'Niacinamide', 'Uvinul A Plus', 'Ethylhexyl triazone', 'Tinosorb M', 'Iscotrizinol']},
     why={'en': 'The most talked-about K-beauty sunscreen of the decade. Feels like a light moisturizer, leaves no white cast, is fragrance-free and uses modern photostable filters.',
          'tl': 'Pinakapinag-uusapang K-beauty sunscreen ng dekada. Parang magaang moisturizer sa pakiramdam, walang white cast, walang pabango at gumagamit ng moderno at photostable na filter.'},
     flag={'en': 'Its finish is “moist” by design. On very oily skin in Manila humidity it can look dewy by mid-shift; if that bothers you, SKIN1004 Hyalu-Cica Water-Fit Sun Serum (₱1,050 at Watsons) is the lighter K-beauty pick.',
           'tl': 'Sadyang “moist” ang finish nito. Sa napaka-oily na balat sa halumigmig ng Maynila, puwedeng maging dewy sa kalagitnaan ng shift; kung nakakaabala iyon, ang SKIN1004 Hyalu-Cica Water-Fit Sun Serum (₱1,050 sa Watsons) ang mas magaang K-beauty na pili.'})

prod('biore', brand='Bioré (Kao)', name='UV Aqua Rich Watery Essence SPF50+ PA++++', region='jp',
     img='https://medias.watsons.com.ph/publishing/WTCPH-50055676-front-zoom.jpg?version=1758790208',
     price={'en': '₱485 (50 g) · ₱198 (15 g) · ₱655 (85 g)', 'tl': '₱485 (50 g) · ₱198 (15 g) · ₱655 (85 g)'},
     where={'en': 'Watsons, Mercury Drug, most supermarkets', 'tl': 'Watsons, Mercury Drug, karamihan ng supermarket'},
     actives={'en': ['Octinoxate', 'Ethylhexyl triazone', 'Uvinul A Plus', 'Tinosorb S', 'Hyaluronic acid', 'Royal jelly extract', 'Xylitol', 'Glycerin'],
              'tl': ['Octinoxate', 'Ethylhexyl triazone', 'Uvinul A Plus', 'Tinosorb S', 'Hyaluronic acid', 'Royal jelly extract', 'Xylitol', 'Glycerin']},
     why={'en': 'Japan’s best-selling sunscreen: water-light, sets in seconds, zero cast, and the most affordable modern-filter option here. Its alcohol base is what makes it feel like nothing on oily skin.',
          'tl': 'Pinakamabiling sunscreen sa Japan: kasing gaan ng tubig, tumitigil sa ilang segundo, walang cast, at ang pinakaabot-kayang opsyon na may modernong filter dito. Ang alcohol na base nito ang nagpaparamdam na parang wala kang suot sa oily na balat.'},
     flag={'en': 'That same alcohol, plus fragrance, can sting sensitive or freshly-irritated skin, and it is not very sweat-resistant for hot commutes. It also uses octinoxate, an older filter, though it is stabilized here with Tinosorb S.',
           'tl': 'Ang alcohol na iyon, kasama ang pabango, ay puwedeng humapdi sa sensitive o bagong-iritang balat, at hindi ito gaanong sweat-resistant para sa mainit na biyahe. Gumagamit din ito ng octinoxate, isang lumang filter, bagama’t na-stabilize dito ng Tinosorb S.'})

prod('vaseline', brand='Vaseline', name='Lip Therapy Original', region='intl',
     img='https://medias.watsons.com.ph/publishing/Vaseline_Image1_50025757-9EPre93h-zoom.jpg?version=1765777079',
     price={'en': '₱149 (4.8 g stick) · Rosy Lips tin about ₱174', 'tl': '₱149 (4.8 g stick) · Rosy Lips tin mga ₱174'},
     where={'en': 'Watsons, Mercury Drug, convenience stores', 'tl': 'Watsons, Mercury Drug, mga convenience store'},
     actives={'en': ['Petrolatum', 'Vitamin E acetate', 'Panthenol', 'Shea butter', 'Castor seed oil', 'Beeswax'],
              'tl': ['Petrolatum', 'Vitamin E acetate', 'Panthenol', 'Shea butter', 'Castor seed oil', 'Beeswax']},
     why={'en': 'Petroleum jelly is still the gold standard for sealing moisture into lips overnight. Cheap, everywhere, and a dermatologist staple.',
          'tl': 'Ang petroleum jelly pa rin ang pamantayan para i-selyo ang moisture sa labi magdamag. Mura, nasa lahat ng tindahan, at staple ng mga dermatologist.'},
     flag={'en': 'The stick has a floral-vanilla fragrance. The plain Vaseline Petroleum Jelly tub (₱70) does the same job unscented.',
           'tl': 'May floral-vanilla na pabango ang stick. Pareho ang gawa ng plain na Vaseline Petroleum Jelly tub (₱70) nang walang amoy.'})

prod('mediheal', brand='Mediheal', name='Panteno Lips Sleeping Mask', region='kr',
     img='https://medias.watsons.com.ph/publishing/Mediheal_Image1_50056954-Le2gCIxv-zoom.png?version=1768214606',
     price={'en': '₱299 (listed at ₱215 earlier in 2026)', 'tl': '₱299 (₱215 ang listing nang mas maaga sa 2026)'},
     where={'en': 'Watsons (in store and online; stock comes and goes)', 'tl': 'Watsons (tindahan at online; paminsan-minsan nauubos)'},
     actives={'en': ['Panthenol 10,000 ppm', 'Shea butter', 'Castor oil', 'Jojoba and macadamia oils', 'Honey extract', 'Mixed berry extracts', 'Hyaluronic acid', 'Vitamin E'],
              'tl': ['Panthenol 10,000 ppm', 'Shea butter', 'Castor oil', 'Jojoba at macadamia oils', 'Honey extract', 'Mga berry extract', 'Hyaluronic acid', 'Vitamin E']},
     why={'en': 'A genuine overnight lip mask from a major K-beauty brand at a drugstore price: a thick, non-sticky gel that is still on your lips when you wake up.',
          'tl': 'Tunay na overnight lip mask mula sa malaking K-beauty brand sa presyong botika: makapal at hindi malagkit na gel na nasa labi mo pa paggising.'},
     flag={'en': 'Contains fragrance. The famous alternative, Laneige Lip Sleeping Mask (₱1,000 and up), is sold at Laneige boutiques and its official Lazada and Shopee stores, not at drugstores.',
           'tl': 'May pabango. Ang sikat na alternatibo, Laneige Lip Sleeping Mask (₱1,000 pataas), ay ibinebenta sa mga Laneige boutique at official Lazada at Shopee store nito, hindi sa botika.'})

prod('dhc', brand='DHC', name='Lip Cream', region='jp',
     img='https://www.wownippon.com/cdn/shop/files/dhc-hydrating-lip-cream-1-5g-japanese-lip-balm.jpg?v=1786951718',
     price={'en': 'About ₱400–700 (1.5 g), depending on the seller', 'tl': 'Mga ₱400–700 (1.5 g), depende sa nagbebenta'},
     where={'en': 'DHC’s official Lazada and Shopee stores and Japanese-import shops (online first). Not stocked at Mercury Drug or St. Joseph.',
            'tl': 'Official Lazada at Shopee store ng DHC at mga Japanese-import shop (online muna). Wala sa Mercury Drug o St. Joseph.'},
     actives={'en': ['Olive fruit oil', 'Squalane', 'Lanolin', 'Beeswax', 'Aloe leaf extract', 'Stearyl glycyrrhetinate (licorice)', 'Ginseng root extract', 'Vitamin E'],
              'tl': ['Olive fruit oil', 'Squalane', 'Lanolin', 'Beeswax', 'Aloe leaf extract', 'Stearyl glycyrrhetinate (licorice)', 'Ginseng root extract', 'Vitamin E']},
     why={'en': 'A Japanese cult classic and long-time bestseller: melts on contact, fragrance-free, deeply conditioning without a waxy feel.',
          'tl': 'Isang Japanese cult classic at matagal nang bestseller: natutunaw sa pagdampi, walang pabango, malalim na nagpapalambot nang hindi parang wax.'},
     flag={'en': 'Online-first in the Philippines and the priciest per gram here. Contains lanolin and beeswax, so skip it if you are allergic to wool or bee products. For a walk-in Japanese-brand buy, Mentholatum Lip Ice (₱89–150) is at every Watsons and Mercury Drug.',
           'tl': 'Online muna sa Pilipinas at pinakamahal kada gramo dito. May lanolin at beeswax, kaya laktawan kung allergic ka sa lana o produktong mula sa bubuyog. Para sa Japanese brand na mabibili sa tindahan, ang Mentholatum Lip Ice (₱89–150) ay nasa bawat Watsons at Mercury Drug.'})

CATEGORY = {'klued':'tube','cerave':'tube','cosrx':'tube','senka':'tube',
            'dermorepubliq':'dropper','ordinary':'dropper','anua':'dropper','melanocc':'tube',
            'camou':'jar','neutrogena':'jar','skin1004':'jar','hadalabo':'jar',
            'hikari':'tube','lrp':'tube','boj':'tube','biore':'tube',
            'vaseline':'stick','mediheal':'tube','dhc':'stick'}
REGION_COLOR = {'current':'#2C7A58','intl':'#3C5A97','kr':'#B24C6E','jp':'#A96F12'}

def placeholder_svg(pid):
    p = P[pid]; c = REGION_COLOR[p['region']]; kind = CATEGORY[pid]
    short = p['brand'].split(' (')[0]
    lines = [short] if len(short) <= 12 else short.split(' ', 1)
    shape = ''
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
    else:  # stick
        shape = (f'<rect x="254" y="110" width="92" height="76" rx="16" fill="{c}" opacity=".75"/>'
                 f'<rect x="262" y="180" width="76" height="180" rx="16" fill="{c}"/>'
                 f'<rect x="276" y="228" width="48" height="92" rx="10" fill="#fff" opacity=".85"/>')
    if len(lines) == 1:
        text = f'<text x="300" y="490" text-anchor="middle" font-family="Fraunces,Georgia,serif" font-size="54" font-weight="600" fill="#14323A">{E(lines[0])}</text>'
    else:
        text = (f'<text x="300" y="470" text-anchor="middle" font-family="Fraunces,Georgia,serif" font-size="50" font-weight="600" fill="#14323A">{E(lines[0])}</text>'
                f'<text x="300" y="526" text-anchor="middle" font-family="Fraunces,Georgia,serif" font-size="50" font-weight="600" fill="#14323A">{E(lines[1])}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">'
            f'<rect width="600" height="600" fill="#F3F6F5"/><g transform="translate(300,225) scale(1.32) translate(-300,-225)">{shape}</g>{text}</svg>')

# --------------------------------------------------------------------------- UI strings
UI = {
 'en': dict(
    lang='en', title='Your personal care routine, built around when you actually wake up and sleep',
    other_lang_label='Basahin sa Tagalog', other_file='skincare-routine-tl.html',
    intro='For oily skin that gets the occasional pimple, on a night-shift schedule. Prices and availability were checked on 26 September 2026 at Watsons Philippines and Watsons’ Lazada store; they change often, so treat them as a guide.',
    tl_title='A typical day for you', tl_wake='You wake up', tl_laptop='At the laptop', tl_sleeproutine='Before-sleep routine', tl_sleep='Asleep',
    tl_sunrise1='Sunrise: still up near a window?', tl_sunrise2='Sunscreen goes on now', tl_daylight='Daylight', tl_night='Night',
    tl_wakeroutine='Wake-up routine', tl_note='The times are only an example. Follow your body, not the clock.',
    tl_ticks=['1 pm', '6 pm', '12 am', '6 am', '1 pm'],
    how_h='How to read this routine',
    how=[('Wake-up routine', 'is the first thing you do after getting up, usually in the afternoon.'),
         ('Before-sleep routine', 'is the last thing you do before bed, whether that is 2 am, 4 am or 9 am.'),
         ('Sunscreen depends on daylight, not the clock.', 'Wear it after waking if you will see daylight before you sleep; light through the window at your desk counts. Skip it if you wake after sunset and stay under lamps until bed. If the sun rises while you are still working by a window, apply it then. You will wash it off before bed anyway.'),
         ('Pick one product per step.', 'Your current product is listed first; the three alternatives are things you could switch to, not extra layers to add.'),
         ('Niacinamide appears in your cleanser, serum and moisturizer.', 'At these percentages that is fine and common. Only be careful if you swap to a 10% serum and keep the 5% moisturizer; stop if you get stinging or flushing.'),
         ('Introduce one new product at a time', 'and give it two weeks before judging it.')],
    wake_h='Wake-up routine', wake_sub='Do this within an hour of getting up, whatever time that is.',
    sleep_h='Before-sleep routine', sleep_sub='Do this right before you actually lie down, whether that is 2 am, 4 am or 9 am. The point is to take the day’s sunscreen, sweat and oil off before you sleep on it. If you fall asleep at the laptop, cleanse the moment you wake instead.',
    pick_one='Choose one of these four. Do not use them together.',
    pick_one_lip='Choose one of these three.',
    amount_l='How much', tech_l='How to apply', wait_l='Then wait', skip_l='Skip it when',
    same_l='Same product you chose for the wake-up routine.',
    region={'current': 'Your current product', 'intl': 'International alternative', 'kr': 'Korean alternative', 'jp': 'Japanese alternative'},
    price_l='Price', where_l='Where to buy', actives_l='Key actives', why_l='Why it fits you', flag_l='Watch out',
    gloss_h='Every active ingredient, explained', gloss_sub='All the actives and notable ingredients across the 19 products above, in plain language, with the products that contain each one.',
    found_l='Found in',
    pimple_h='If a pimple shows up', pimple='Do not squeeze it. After the moisturizer step, a hydrocolloid pimple patch (for example Acnes patches, ₱230 at Watsons) is the one extra you can safely add. Take it off when you wake.',
    notes_h='Sources and notes',
    notes=['Prices and stock: Watsons Philippines product pages on 26 September 2026, with the sale prices seen that day noted on the cards. Mercury Drug and St. Joseph Drug were not re-checked this time, so check your branch.',
           'Ingredient lists come from the Watsons PH product pages and La Roche-Posay’s own listing; for Klued, Camou and Hikari, which Watsons does not sell, from the SkinSort ingredient database.',
           'Product photos load from the retailers’ websites. If they do not appear in a preview window, open this file in a normal browser.',
           'This is a research summary, not medical advice. If anything stings, burns or breaks you out, stop using it, and see a dermatologist for anything that does not settle in two weeks.'],
    img_note='Photos load from retailer sites; open this file in a browser if they do not show.'
 ),
 'tl': dict(
    lang='tl', title='Ang personal care routine mo, nakaayon sa totoong oras ng gising at tulog mo',
    other_lang_label='Read in English', other_file='skincare-routine-en.html',
    intro='Para sa oily na balat na paminsan-minsang tinutubuan ng pimple, at para sa night-shift na iskedyul. Na-check ang mga presyo at availability noong 26 Setyembre 2026 sa Watsons Philippines at sa Lazada store ng Watsons; madalas itong magbago, kaya gawing gabay lang.',
    tl_title='Karaniwang araw mo', tl_wake='Gising ka', tl_laptop='Nasa laptop', tl_sleeproutine='Routine bago matulog', tl_sleep='Tulog',
    tl_sunrise1='Pagsikat ng araw: gising pa sa may bintana?', tl_sunrise2='Mag-sunscreen na', tl_daylight='May liwanag ng araw', tl_night='Gabi',
    tl_wakeroutine='Routine pag-gising', tl_note='Halimbawa lang ang mga oras. Sundin ang katawan mo, hindi ang orasan.',
    tl_ticks=['1 pm', '6 pm', '12 am', '6 am', '1 pm'],
    how_h='Paano basahin ang routine na ito',
    how=[('Routine pag-gising', 'ang unang gagawin mo pagkabangon, kadalasan sa hapon.'),
         ('Routine bago matulog', 'ang huling gagawin mo bago humiga, 2 am man iyon, 4 am, o 9 am.'),
         ('Nakadepende ang sunscreen sa liwanag ng araw, hindi sa oras.', 'Gamitin ito pagkagising kung makakakita ka ng liwanag ng araw bago ka matulog; kasama na ang liwanag mula sa bintana sa desk mo. Laktawan kung gumising ka pagkalubog ng araw at nasa ilalim ka lang ng ilaw hanggang matulog. Kung sumikat ang araw habang nagtatrabaho ka pa malapit sa bintana, mag-apply na noon. Huhugasan mo rin ito bago matulog.'),
         ('Pumili ng isang produkto lang bawat step.', 'Nakalista muna ang kasalukuyang produkto mo; ang tatlong alternatibo ay puwedeng ipalit, hindi idagdag na layer.'),
         ('May niacinamide ang cleanser, serum at moisturizer mo.', 'Sa ganitong porsyento, ayos lang at karaniwan iyon. Mag-ingat lang kung papalit ka sa 10% na serum at itutuloy ang 5% na moisturizer; itigil kung humapdi o namumula.'),
         ('Isa-isang ipakilala ang bagong produkto', 'at bigyan ng dalawang linggo bago husgahan.')],
    wake_h='Routine pag-gising', wake_sub='Gawin ito sa loob ng isang oras pagkabangon, anumang oras iyon.',
    sleep_h='Routine bago matulog', sleep_sub='Gawin ito bago ka talaga humiga, 2 am man iyon, 4 am, o 9 am. Ang layunin ay tanggalin ang sunscreen, pawis at langis ng buong araw bago mo ito matulugan. Kung nakatulog ka sa laptop, maglinis agad pagkagising.',
    pick_one='Pumili ng isa sa apat na ito. Huwag gamitin nang sabay.',
    pick_one_lip='Pumili ng isa sa tatlong ito.',
    amount_l='Gaano karami', tech_l='Paano i-apply', wait_l='Saka maghintay', skip_l='Laktawan kung',
    same_l='Iyon ding produktong pinili mo sa routine pag-gising.',
    region={'current': 'Kasalukuyang produkto mo', 'intl': 'International na alternatibo', 'kr': 'Korean na alternatibo', 'jp': 'Japanese na alternatibo'},
    price_l='Presyo', where_l='Saan mabibili', actives_l='Pangunahing aktibong sangkap', why_l='Bakit bagay sa iyo', flag_l='Bantayan',
    gloss_h='Bawat aktibong sangkap, ipinaliwanag', gloss_sub='Lahat ng aktibo at kapansin-pansing sangkap sa 19 produkto sa itaas, sa simpleng salita, kasama ang mga produktong naglalaman ng bawat isa.',
    found_l='Nasa',
    pimple_h='Kung may tumubong pimple', pimple='Huwag pisilin. Pagkatapos ng moisturizer, ang hydrocolloid pimple patch (halimbawa, Acnes patch, ₱230 sa Watsons) ang nag-iisang dagdag na ligtas isama. Tanggalin paggising.',
    notes_h='Mga pinagkunan at paalala',
    notes=['Presyo at stock: mga product page ng Watsons Philippines noong 26 Setyembre 2026, at nakatala sa mga card ang mga sale price na nakita noong araw na iyon. Hindi na-check muli ang Mercury Drug at St. Joseph Drug ngayon, kaya i-check ang branch mo.',
           'Ang mga listahan ng sangkap ay mula sa mga product page ng Watsons PH at sa sariling listing ng La Roche-Posay; para sa Klued, Camou at Hikari, na hindi ibinebenta sa Watsons, mula sa ingredient database ng SkinSort.',
           'Nagmumula sa mga website ng retailer ang mga larawan ng produkto. Kung hindi lumabas sa preview, buksan ang file na ito sa normal na browser.',
           'Buod ito ng pananaliksik, hindi medikal na payo. Kung may humapdi, sumunog o nagpa-breakout, itigil ang paggamit, at magpatingin sa dermatologist kung hindi humupa sa loob ng dalawang linggo.'],
    img_note='Mula sa mga website ng retailer ang mga larawan; buksan ang file sa browser kung hindi lumabas.'
 )
}

# --------------------------------------------------------------------------- steps
WAKE = [
 dict(key='cleanse', products=['klued', 'cerave', 'cosrx', 'senka'],
      title={'en': 'Cleanse', 'tl': 'Linisin ang mukha'},
      amount={'en': 'Pea- to nickel-sized. For Perfect Whip, about 2 cm.', 'tl': 'Kasinlaki ng gisantes hanggang barya. Para sa Perfect Whip, mga 2 cm.'},
      tech={'en': 'Wet your face with lukewarm water, never hot. Lather gel or foam types between your palms first, then massage for a full 60 seconds, spending extra time on the forehead, nose and chin where oil pools while you sleep. Rinse well, then pat with a clean towel until your skin is damp, not fully dry.',
            'tl': 'Basain ang mukha ng maligamgam na tubig, huwag mainit. Bulain muna sa palad ang gel o foam, saka i-masahe ng buong 60 segundo, dagdagan ang oras sa noo, ilong at baba kung saan nagkukumpol ang langis habang natutulog ka. Banlawan nang mabuti, saka dampian ng malinis na tuwalya hanggang mamasa-masa pa ang balat, hindi tuyong-tuyo.'},
      wait={'en': 'No wait. Go straight to the serum while your skin is still slightly damp.', 'tl': 'Walang paghihintay. Dumiretso sa serum habang bahagyang mamasa-masa pa ang balat.'}),
 dict(key='serum', products=['dermorepubliq', 'ordinary', 'anua', 'melanocc'],
      title={'en': 'Serum', 'tl': 'Serum'},
      amount={'en': '2–3 drops, about half a dropper. The Hada Labo lotions are patted in by hand instead.', 'tl': '2–3 patak, mga kalahating dropper. Idinidiin naman sa balat gamit ang kamay ang mga Hada Labo lotion.'},
      tech={'en': 'Drop it into your palm, then press onto damp skin with flat fingers: forehead, both cheeks, chin. Press, do not rub.', 'tl': 'Ipatak sa palad, saka idiin sa mamasa-masang balat gamit ang nakalapat na mga daliri: noo, magkabilang pisngi, baba. Idiin, hindi kuskusin.'},
      wait={'en': '30–60 seconds, until it no longer feels wet.', 'tl': '30–60 segundo, hanggang hindi na basa sa pakiramdam.'}),
 dict(key='moist', products=['camou', 'neutrogena', 'skin1004', 'hadalabo'],
      title={'en': 'Moisturize', 'tl': 'Mag-moisturizer'},
      amount={'en': 'Pea- to blueberry-sized.', 'tl': 'Kasinlaki ng gisantes hanggang blueberry.'},
      tech={'en': 'Warm it between two fingertips, press onto the cheeks first and smooth outward and upward, then finish the forehead, nose and chin with whatever is left. Oily skin wants a thin, even layer, not a thick one.',
            'tl': 'Painitin muna sa pagitan ng dalawang daliri, idiin muna sa pisngi at ihaplos palabas at pataas, saka tapusin ang noo, ilong at baba gamit ang natira. Manipis at pantay na layer ang kailangan ng oily na balat, hindi makapal.'},
      wait={'en': '2–3 minutes before sunscreen, so the sunscreen can form an even film on top.', 'tl': '2–3 minuto bago mag-sunscreen, para pantay ang pagkalatag ng sunscreen sa ibabaw.'}),
 dict(key='sun', products=['hikari', 'lrp', 'boj', 'biore'],
      title={'en': 'Sunscreen, only if you will see daylight', 'tl': 'Sunscreen, kung makakakita ka lang ng liwanag ng araw'},
      amount={'en': 'Two full finger-lengths, about a quarter teaspoon, for the face and neck.', 'tl': 'Dalawang buong haba ng daliri, mga isang-kapat na kutsarita, para sa mukha at leeg.'},
      tech={'en': 'Dot it on the forehead, both cheeks, nose and chin, then spread with flat fingers until even. Lay it down rather than rubbing it in like a lotion; rubbing thins the protective film. Include the ears and the back of the neck if you are going outside.',
            'tl': 'Tuldukan ang noo, magkabilang pisngi, ilong at baba, saka ikalat gamit ang nakalapat na mga daliri hanggang pumantay. Ilatag ito sa halip na kuskusin na parang lotion; nagpapanipis ng proteksiyon ang pagkuskos. Isama ang tenga at batok kung lalabas ka.'},
      wait={'en': '10–15 minutes before going out or sitting in direct window light. Reapply every 2 hours in direct sun or after sweating; indoors by a window, one application per waking period is enough.',
            'tl': '10–15 minuto bago lumabas o umupo sa direktang liwanag mula sa bintana. Mag-reapply tuwing 2 oras kung nasa direktang araw o pagkatapos pawisan; kung nasa loob lang malapit sa bintana, sapat ang isang apply bawat gising.'},
      skip={'en': 'you will have no daylight at all before you sleep.', 'tl': 'wala ka talagang makikitang liwanag ng araw bago matulog.'}),
]

SLEEP = [
 dict(key='cleanse', products=['klued', 'cerave', 'cosrx', 'senka'], compact=True,
      title={'en': 'Cleanse', 'tl': 'Linisin ang mukha'},
      body={'en': 'One gentle cleanse is enough to remove these gel sunscreens. If you used a lot of sunscreen and still feel a film, cleanse a second time with the same product instead of buying a separate oil cleanser.',
            'tl': 'Sapat na ang isang mabining paghuhugas para matanggal ang mga gel na sunscreen na ito. Kung marami kang ginamit na sunscreen at may natitira pang film, maghugas ulit gamit ang parehong produkto sa halip na bumili ng hiwalay na oil cleanser.'}),
 dict(key='serum', products=['dermorepubliq', 'ordinary', 'anua', 'melanocc'], compact=True,
      title={'en': 'Serum', 'tl': 'Serum'},
      body={'en': 'Same 2–3 drops pressed onto damp skin. Wait 30–60 seconds.', 'tl': '2–3 patak din, idiin sa mamasa-masang balat. Maghintay ng 30–60 segundo.'}),
 dict(key='moist', products=['camou', 'neutrogena', 'skin1004', 'hadalabo'], compact=True,
      title={'en': 'Moisturize', 'tl': 'Mag-moisturizer'},
      body={'en': 'At bedtime you can go slightly more generous, blueberry-sized, because nothing goes on top. If you wake up greasy, go back to a pea.', 'tl': 'Bago matulog, puwedeng bahagyang dagdagan, kasinlaki ng blueberry, dahil wala nang ipapatong. Kung malagkit ka paggising, bumalik sa kasinlaki ng gisantes.'}),
 dict(key='lip', products=['vaseline', 'mediheal', 'dhc'], compact=False,
      title={'en': 'Lip treatment, the last thing before sleep', 'tl': 'Lip treatment, ang pinakahuli bago matulog'},
      amount={'en': 'A thick layer, more than you would wear during the day.', 'tl': 'Makapal na layer, higit sa isusuot mo sa araw.'},
      tech={'en': 'Wait a minute after your moisturizer so it is not sliding around, then apply with a clean fingertip, or the spatula for the tub types, from the centre of the lips outward. Do not rub it in and do not lick it off; go to bed. Wipe any residue off with a tissue when you wake. If your lips are flaky, a soft damp towel rubbed gently once a week is enough; skip sugar scrubs.',
            'tl': 'Maghintay ng isang minuto pagkatapos ng moisturizer para hindi ito dumudulas, saka i-apply gamit ang malinis na dulo ng daliri, o ang spatula para sa tub, mula gitna ng labi palabas. Huwag kuskusin at huwag dilaan; matulog na. Punasan ng tissue ang natira paggising. Kung nagbabalat ang labi, sapat na ang mabining pagkuskos ng basang malambot na tuwalya isang beses kada linggo; laktawan ang sugar scrub.'},
      wait={'en': 'Nothing else goes on after this. Lights out.', 'tl': 'Wala nang ipapatong pagkatapos nito. Matulog na.'}),
]

# --------------------------------------------------------------------------- glossary
def G(name, en, tl, ids):
    return dict(name=name, en=en, tl=tl, ids=ids)

GLOSSARY = [
 ({'en': 'Hydrators and barrier builders', 'tl': 'Pampahydrate at pampatibay ng skin barrier'}, [
   G({'en': 'Hyaluronic acid (sodium hyaluronate)', 'tl': 'Hyaluronic acid (sodium hyaluronate)'},
     'A sugar molecule that holds many times its weight in water. It pulls moisture into the top layer of skin so it feels plump rather than tight. Works best applied to damp skin and sealed with a moisturizer.',
     'Isang molekulang asukal na humahawak ng tubig na ilang ulit sa sarili nitong timbang. Hinihila nito ang moisture papunta sa itaas na layer ng balat para maging malusog sa halip na masikip ang pakiramdam. Pinakaepektibo kung ipapahid sa mamasa-masang balat at sasaraduhan ng moisturizer.',
     ['klued', 'cerave', 'hikari', 'dermorepubliq', 'anua', 'camou', 'neutrogena', 'skin1004', 'hadalabo', 'biore', 'mediheal']),
   G({'en': 'Glycerin', 'tl': 'Glycerin'},
     'The most reliable humectant in skincare; your skin makes it too. It draws water in and keeps it there, which is why nearly every product here uses it.',
     'Pinakamaaasahang humectant sa skincare; ginagawa rin ito ng balat mo. Humihila ito ng tubig at pinananatili ito, kaya halos lahat ng produkto dito ay gumagamit nito.',
     ['klued', 'cerave', 'senka', 'hikari', 'lrp', 'boj', 'biore', 'camou', 'neutrogena', 'skin1004', 'hadalabo', 'anua', 'vaseline']),
   G({'en': 'Ceramides (NP, AP, EOP, NS)', 'tl': 'Ceramides (NP, AP, EOP, NS)'},
     'Fats your skin uses like mortar between bricks. Topping them up seals the barrier, so skin loses less water and gets irritated less, which matters when you cleanse twice a day.',
     'Mga taba na ginagamit ng balat na parang semento sa pagitan ng mga brick. Ang pagdagdag nito ay sumasara ng barrier, kaya mas kaunting tubig ang nawawala at mas hindi naiirita ang balat, na mahalaga kung dalawang beses kang naghuhugas kada araw.',
     ['klued', 'cerave', 'skin1004', 'anua']),
   G({'en': 'Cholesterol and phytosphingosine', 'tl': 'Cholesterol at phytosphingosine'},
     'The two partners of ceramides in the skin barrier. Formulas that include all three repair the barrier better than ceramides alone.',
     'Ang dalawang kapareha ng ceramides sa skin barrier. Mas mahusay na nakakapag-repair ng barrier ang mga formula na may lahat ng tatlo kaysa ceramides lamang.',
     ['cerave', 'skin1004']),
   G({'en': 'Trehalose', 'tl': 'Trehalose'},
     'A plant sugar that protects cells from drying out; a gentle extra humectant.',
     'Asukal mula sa halaman na pumoprotekta sa mga cell laban sa pagkatuyo; mabining dagdag na humectant.',
     ['skin1004', 'hadalabo']),
   G({'en': 'Beta-glucan', 'tl': 'Beta-glucan'},
     'A sugar from oats or yeast that hydrates and calms at the same time; often used to soothe skin after acne treatments.',
     'Asukal mula sa oats o yeast na sabay na nagpapahydrate at nagpapakalma; madalas gamitin para pakalmahin ang balat pagkatapos ng acne treatment.',
     ['camou', 'skin1004']),
   G({'en': 'Panthenol (pro-vitamin B5)', 'tl': 'Panthenol (pro-vitamin B5)'},
     'Converts to vitamin B5 in the skin. Softens, hydrates and speeds up the recovery of irritated skin and chapped lips.',
     'Nagiging vitamin B5 sa balat. Nagpapalambot, nagpapahydrate at nagpapabilis ng paggaling ng iritadong balat at tuyong labi.',
     ['anua', 'mediheal', 'vaseline']),
   G({'en': 'Snail secretion filtrate', 'tl': 'Snail secretion filtrate'},
     'A hydrating, soothing extract rich in glycoproteins and a little hyaluronic acid; a K-beauty staple for calming skin.',
     'Pampahydrate at pampakalmang extract na mayaman sa glycoproteins at kaunting hyaluronic acid; staple sa K-beauty para pakalmahin ang balat.',
     ['dermorepubliq']),
   G({'en': 'Squalane and squalene', 'tl': 'Squalane at squalene'},
     'A lightweight oil identical to part of your own sebum; it softens without feeling greasy. Squalane is the stable form; squalene (in the Klued cleanser) is the unstable one, but it rinses off.',
     'Magaang langis na kapareho ng bahagi ng sarili mong sebum; nagpapalambot nang hindi malagkit. Squalane ang matatag na anyo; squalene (sa Klued cleanser) ang hindi matatag, pero nahuhugasan naman ito.',
     ['klued', 'dhc']),
 ]),
 ({'en': 'Oil, pores and pimple helpers', 'tl': 'Para sa langis, pores at pimples'}, [
   G({'en': 'Niacinamide (vitamin B3)', 'tl': 'Niacinamide (vitamin B3)'},
     'The workhorse of your routine. It regulates oil production, calms redness, strengthens the barrier and slowly evens tone. 2–5% is plenty; 10% adds little for most people and raises the chance of stinging.',
     'Ang pinakamasipag na sangkap ng routine mo. Nagre-regulate ito ng produksyon ng langis, nagpapakalma ng pamumula, nagpapatibay ng barrier at unti-unting nagpapantay ng kulay. Sapat na ang 2–5%; kaunti lang ang dagdag ng 10% para sa karamihan at mas malaki ang tsansa ng paghapdi.',
     ['klued', 'cerave', 'dermorepubliq', 'ordinary', 'anua', 'camou', 'hadalabo', 'boj']),
   G({'en': 'Zinc (zinc PCA, zinc gluconate)', 'tl': 'Zinc (zinc PCA, zinc gluconate)'},
     'A mineral salt that helps reduce shine and has a mild antibacterial effect.',
     'Asin ng mineral na tumutulong bawasan ang kintab at may bahagyang antibacterial na epekto.',
     ['ordinary', 'lrp']),
   G({'en': 'Betaine salicylate (gentle BHA)', 'tl': 'Betaine salicylate (mabining BHA)'},
     'A softer cousin of salicylic acid. Oil-soluble, so it can loosen the plugs inside pores. At the low levels here it exfoliates very lightly and is safe daily.',
     'Mas mabining kamag-anak ng salicylic acid. Natutunaw sa langis, kaya kayang lumuwag ng bara sa loob ng pores. Sa mababang dami dito, napakabanayad ang pag-exfoliate at ligtas araw-araw.',
     ['cosrx', 'anua']),
   G({'en': 'Tea tree leaf oil', 'tl': 'Tea tree leaf oil'},
     'A plant oil with proven activity against acne bacteria, found in the Quick FX cleanser. Good for pimple-prone skin, though a few people are sensitive to it.',
     'Langis ng halaman na napatunayang tumatalab laban sa acne bacteria, at nasa Quick FX cleanser ito. Mainam para sa pimple-prone na balat, bagama’t may ilang sensitive dito.',
     ['cosrx']),
   G({'en': 'O-Cymen-5-OL (isopropyl methylphenol)', 'tl': 'O-Cymen-5-OL (isopropyl methylphenol)'},
     'An antibacterial common in Japanese medicated skincare that targets the bacteria involved in pimples; the reason Melano CC is marketed for acne marks and prevention.',
     'Antibacterial na karaniwan sa Japanese medicated skincare na tumatarget sa bacteria ng pimples; ang dahilan kung bakit ibinebenta ang Melano CC para sa acne marks at pag-iwas.',
     ['melanocc']),
   G({'en': 'Silica (Airlicium) and starches', 'tl': 'Silica (Airlicium) at mga starch'},
     'Porous particles that soak up sebum so skin stays matte for hours.',
     'Mga butil na may butas-butas na sumisipsip ng sebum para manatiling matte ang balat sa loob ng ilang oras.',
     ['lrp']),
 ]),
 ({'en': 'Brighteners and antioxidants', 'tl': 'Pampaliwanag at antioxidant'}, [
   G({'en': 'Tranexamic acid (TXA)', 'tl': 'Tranexamic acid (TXA)'},
     'Blocks the signal that tells skin to make excess pigment, so post-pimple marks and dark spots fade over months. It does not make skin sun-sensitive.',
     'Hinaharang ang signal na nagsasabi sa balat na gumawa ng sobrang pigment, kaya kumukupas ang marka ng pimple at dark spots sa loob ng ilang buwan. Hindi nito ginagawang sensitive sa araw ang balat.',
     ['camou', 'anua', 'skin1004']),
   G({'en': 'Alpha-arbutin', 'tl': 'Alpha-arbutin'},
     'A gentle, well-studied pigment blocker, related to hydroquinone but far milder. Evens tone slowly and is safe at up to 2%.',
     'Mabini at mahusay na napag-aralang tagaharang ng pigment, kamag-anak ng hydroquinone pero mas banayad. Dahan-dahang nagpapantay ng kulay at ligtas hanggang 2%.',
     ['camou', 'anua', 'hadalabo']),
   G({'en': 'Vitamin C (ascorbic acid, 3-O-ethyl ascorbic acid, ascorbyl tetraisopalmitate)', 'tl': 'Vitamin C (ascorbic acid, 3-O-ethyl ascorbic acid, ascorbyl tetraisopalmitate)'},
     'An antioxidant that brightens and helps fade the red-brown marks pimples leave. Pure ascorbic acid is the most active form but can tingle; the derivatives in Garnier and Hada Labo are gentler and slower.',
     'Antioxidant na nagpapaliwanag at tumutulong kumupas ang pula-kayumangging marka na iniiwan ng pimple. Ang purong ascorbic acid ang pinakaaktibong anyo pero puwedeng kumiliti; mas mabini at mas mabagal ang mga derivative sa Garnier at Hada Labo.',
     ['melanocc', 'anua', 'hadalabo']),
   G({'en': 'Vitamin E (tocopherol, tocopheryl acetate)', 'tl': 'Vitamin E (tocopherol, tocopheryl acetate)'},
     'An oil-soluble antioxidant that protects skin fats and lips from oxidation and makes other actives, such as vitamin C and sunscreen filters, more stable.',
     'Antioxidant na natutunaw sa langis na pumoprotekta sa taba ng balat at labi laban sa oxidation at nagpapatatag sa ibang aktibong sangkap tulad ng vitamin C at mga sunscreen filter.',
     ['hikari', 'melanocc', 'biore', 'boj', 'hadalabo', 'lrp', 'vaseline', 'dhc', 'mediheal']),
   G({'en': 'Licorice (root water, dipotassium glycyrrhizate, glycyrrhetinate)', 'tl': 'Licorice (root water, dipotassium glycyrrhizate, glycyrrhetinate)'},
     'Calms redness and mildly brightens; one of the few soothing agents that also helps with the marks inflammation leaves behind.',
     'Nagpapakalma ng pamumula at bahagyang nagpapaliwanag; isa sa ilang pampakalma na tumutulong din sa markang iniiwan ng pamamaga.',
     ['camou', 'melanocc', 'skin1004', 'dhc']),
   G({'en': 'Ergothioneine and spirulina extract', 'tl': 'Ergothioneine at spirulina extract'},
     'Antioxidants from mushrooms and algae that mop up the free radicals generated by UV and pollution.',
     'Antioxidant mula sa kabute at algae na nagliligpit ng free radicals na dulot ng UV at polusyon.',
     ['camou']),
   G({'en': 'Rice extract and fermented grains (“probiotics”)', 'tl': 'Rice extract at fermented grains (“probiotics”)'},
     'Rich in amino acids and B vitamins; hydrates and soothes. In Relief Sun this is why the sunscreen feels like skincare.',
     'Mayaman sa amino acids at B vitamins; nagpapahydrate at nagpapakalma. Sa Relief Sun, ito ang dahilan kung bakit parang skincare ang sunscreen.',
     ['boj']),
   G({'en': 'Royal jelly, honey and xylitol', 'tl': 'Royal jelly, honey at xylitol'},
     'Sugars and bee-derived extracts used as humectants; honey also has mild antibacterial properties.',
     'Mga asukal at extract mula sa bubuyog na ginagamit bilang humectant; may bahagyang antibacterial ding katangian ang honey.',
     ['biore', 'mediheal', 'hadalabo']),
 ]),
 ({'en': 'Soothers', 'tl': 'Pampakalma'}, [
   G({'en': 'Centella asiatica (cica: asiaticoside, madecassic acid)', 'tl': 'Centella asiatica (cica: asiaticoside, madecassic acid)'},
     'A herb with decades of wound-healing research. It reduces redness, supports collagen and helps pimples heal without leaving marks. 72% of the SKIN1004 cream is centella extract.',
     'Halamang may dekada ng pananaliksik sa pagpapagaling ng sugat. Nagbabawas ito ng pamumula, sumusuporta sa collagen at tumutulong gumaling ang pimple nang walang iniiwang marka. 72% ng SKIN1004 cream ay centella extract.',
     ['skin1004', 'anua', 'hadalabo']),
   G({'en': 'Allantoin', 'tl': 'Allantoin'},
     'A soothing agent that softens rough skin and reduces irritation; often paired with stronger actives.',
     'Pampakalma na nagpapalambot ng magaspang na balat at nagbabawas ng iritasyon; madalas ipares sa mas malalakas na aktibong sangkap.',
     ['cosrx', 'dermorepubliq']),
   G({'en': 'Aloe leaf extract or juice', 'tl': 'Aloe leaf extract o juice'},
     'Cooling polysaccharides that calm and hydrate; the classic after-sun ingredient.',
     'Malamig na polysaccharides na nagpapakalma at nagpapahydrate; ang klasikong sangkap pagkatapos maarawan.',
     ['dermorepubliq', 'hikari', 'dhc']),
   G({'en': 'Scutellaria (Baikal skullcap) root', 'tl': 'Scutellaria (Baikal skullcap) root'},
     'An antioxidant, anti-redness botanical common in Asian formulas.',
     'Antioxidant at anti-pamumulang halaman na karaniwan sa mga Asian formula.',
     ['hadalabo', 'lrp']),
 ]),
 ({'en': 'Sunscreen filters', 'tl': 'Mga sunscreen filter'}, [
   G({'en': 'Modern photostable filters: Tinosorb S, Tinosorb M, Uvinul A Plus (DHHB), Uvinul T150 (ethylhexyl triazone), iscotrizinol', 'tl': 'Mga modernong photostable filter: Tinosorb S, Tinosorb M, Uvinul A Plus (DHHB), Uvinul T150 (ethylhexyl triazone), iscotrizinol'},
     'Newer-generation UV filters that cover both UVB (burning) and UVA (ageing and darkening) and do not break down in sunlight. They are why the Korean and Japanese sunscreens feel light yet protect well. Tinosorb M also scatters light the way a mineral filter does.',
     'Mga bagong henerasyong UV filter na sumasaklaw sa UVB (pagkasunog) at UVA (pagtanda at pangingitim) at hindi nasisira sa araw. Ito ang dahilan kung bakit magaan pero mahusay ang proteksyon ng mga Korean at Japanese na sunscreen. Nagkakalat din ng liwanag ang Tinosorb M tulad ng mineral filter.',
     ['lrp', 'boj', 'biore']),
   G({'en': 'Mexoryl 400, Mexoryl XL and Mexoryl SX', 'tl': 'Mexoryl 400, Mexoryl XL at Mexoryl SX'},
     'L’Oréal’s patented filters. Mexoryl 400 is the only filter on the market that absorbs ultra-long UVA (380–400 nm), the rays that penetrate deepest and reach you through glass.',
     'Mga patented na filter ng L’Oréal. Ang Mexoryl 400 ang tanging filter sa merkado na sumisipsip ng ultra-long UVA (380–400 nm), ang mga sinag na pinakamalalim tumagos at umaabot sa iyo sa pamamagitan ng salamin.',
     ['lrp']),
   G({'en': 'Octinoxate (ethylhexyl methoxycinnamate)', 'tl': 'Octinoxate (ethylhexyl methoxycinnamate)'},
     'An old but effective UVB filter. It loses some strength in sunlight unless stabilized; Bioré pairs it with Tinosorb S, Hikari does not.',
     'Luma pero epektibong UVB filter. Nawawalan ng lakas sa araw kung hindi na-stabilize; ipinares ito ng Bioré sa Tinosorb S, hindi ng Hikari.',
     ['hikari', 'biore']),
   G({'en': 'Avobenzone (butyl methoxydibenzoylmethane)', 'tl': 'Avobenzone (butyl methoxydibenzoylmethane)'},
     'A strong UVA filter that degrades quickly in sunlight unless stabilized, which is the main reason to reapply Hikari when you are outside.',
     'Malakas na UVA filter na mabilis nasisira sa araw kung hindi na-stabilize, na siyang pangunahing dahilan para mag-reapply ng Hikari kung nasa labas ka.',
     ['hikari', 'lrp']),
   G({'en': 'Oxybenzone (benzophenone-3)', 'tl': 'Oxybenzone (benzophenone-3)'},
     'An older UVB and short-UVA filter. It absorbs into skin more than other filters and is the most common cause of sunscreen allergy; EU regulators flagged it as hormone-active in 2025 and it is banned in Hawaii. Not dangerous at cosmetic levels, but the modern filters are simply better.',
     'Mas lumang UVB at short-UVA filter. Mas sumisipsip sa balat kaysa ibang filter at pinakakaraniwang sanhi ng sunscreen allergy; binantayan ito ng EU regulators bilang hormone-active noong 2025 at ipinagbabawal sa Hawaii. Hindi mapanganib sa cosmetic na dami, pero mas mahusay lang talaga ang mga modernong filter.',
     ['hikari']),
   G({'en': 'Titanium dioxide and zinc oxide', 'tl': 'Titanium dioxide at zinc oxide'},
     'Mineral filters that mostly absorb UV rather than reflect it. Very gentle, but they are the cause of white cast. Hikari uses small amounts alongside its chemical filters.',
     'Mineral na filter na kadalasang sumisipsip ng UV sa halip na nagre-reflect. Napakabini, pero ito ang sanhi ng white cast. Gumagamit ang Hikari ng kaunti kasama ng mga chemical filter nito.',
     ['hikari', 'lrp']),
 ]),
 ({'en': 'Lip sealers and emollients', 'tl': 'Pang-selyo at pampalambot ng labi'}, [
   G({'en': 'Petrolatum (petroleum jelly)', 'tl': 'Petrolatum (petroleum jelly)'},
     'The most effective moisture sealer known; it cuts water loss from skin by more than 98%. It does not add water, it stops the water you already have from escaping, which is exactly what chapped lips need overnight.',
     'Pinakaepektibong pang-selyo ng moisture; binabawasan nito ang pagkawala ng tubig sa balat ng higit 98%. Hindi ito nagdadagdag ng tubig, pinipigilan nitong tumakas ang tubig na nasa iyo na, na eksaktong kailangan ng tuyong labi sa gabi.',
     ['vaseline']),
   G({'en': 'Shea butter', 'tl': 'Shea butter'},
     'A rich plant butter full of fatty acids and anti-inflammatory compounds; softens and seals. Fine on lips, heavier than most oily faces want.',
     'Mayamang butter mula sa halaman na puno ng fatty acids at anti-inflammatory compounds; nagpapalambot at sumasara. Ayos sa labi, mas mabigat kaysa gusto ng karamihan sa oily na mukha.',
     ['vaseline', 'mediheal', 'klued']),
   G({'en': 'Castor, jojoba, macadamia and olive oils', 'tl': 'Castor, jojoba, macadamia at olive oils'},
     'Plant oils that soften and add slip. Excellent in lip products; on an oily face they are the ingredients to watch if a new serum breaks you out.',
     'Mga langis ng halaman na nagpapalambot at nagpapadulas. Mahusay sa lip products; sa oily na mukha, ito ang mga sangkap na bantayan kung may bagong serum na nagpapa-breakout sa iyo.',
     ['vaseline', 'mediheal', 'dhc', 'anua']),
   G({'en': 'Lanolin and beeswax', 'tl': 'Lanolin at beeswax'},
     'Animal-derived waxes that hold moisture on the lips for hours; lanolin is the closest thing to skin’s own lipids. Avoid if you are allergic to wool or bee products.',
     'Mga wax mula sa hayop na humahawak ng moisture sa labi sa loob ng ilang oras; ang lanolin ang pinakamalapit sa sariling lipids ng balat. Iwasan kung allergic ka sa lana o produktong mula sa bubuyog.',
     ['dhc', 'vaseline', 'senka']),
 ]),
 ({'en': 'Worth knowing', 'tl': 'Dapat malaman'}, [
   G({'en': 'Alcohol (ethanol)', 'tl': 'Alcohol (ethanol)'},
     'Makes sunscreens and serums feel weightless and dry fast, a plus for oily skin, but it can sting broken or freshly-irritated skin. It is why Bioré and Skin Aqua feel so light.',
     'Nagpaparamdam ng gaan at mabilis na pagkatuyo sa sunscreen at serum, plus para sa oily na balat, pero puwedeng humapdi sa may sugat o bagong-iritang balat. Ito ang dahilan kung bakit napakagaan ng Bioré at Skin Aqua.',
     ['biore', 'melanocc', 'senka']),
   G({'en': 'Fragrance (parfum)', 'tl': 'Pabango (parfum)'},
     'Adds scent and nothing else. It is the most common cause of skincare irritation; not a problem for most people, but if your skin ever itches or reddens, the scented products are the first to remove.',
     'Nagdadagdag ng amoy at wala nang iba. Ito ang pinakakaraniwang sanhi ng iritasyon sa skincare; hindi problema sa karamihan, pero kung kumati o mamula ang balat mo, ang mga may pabango ang unang alisin.',
     ['camou', 'neutrogena', 'senka', 'biore', 'melanocc', 'vaseline', 'mediheal']),
   G({'en': 'Dimethicone and other silicones', 'tl': 'Dimethicone at iba pang silicone'},
     'Give products their smooth, silky glide and form a breathable film that reduces water loss. Non-comedogenic, whatever the internet says.',
     'Nagbibigay ng makinis at silky na dulas at bumubuo ng breathable na film na nagbabawas ng pagkawala ng tubig. Hindi nakakabara ng pores, anuman ang sabi sa internet.',
     ['neutrogena', 'hikari', 'hadalabo', 'biore', 'lrp']),
   G({'en': 'Soap-based cleansing agents (fatty acids + potassium hydroxide)', 'tl': 'Soap-based na panlinis (fatty acids + potassium hydroxide)'},
     'What gives Perfect Whip its dense foam. Cleans oil very well but sits at a higher pH than skin, which is why it can feel tight afterwards.',
     'Ito ang nagbibigay ng makapal na bula sa Perfect Whip. Mahusay maglinis ng langis pero mas mataas ang pH kaysa balat, kaya puwedeng masikip ang pakiramdam pagkatapos.',
     ['senka']),
 ]),
]

