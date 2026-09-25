# Adding a product to `products-extra.json`

Reached from step 3 of `SKILL.md`, when the product I switched to is not one of the ids the data files already define.

The schema, the field list and the existing ids are in `site-builder/README.md`. This file carries what that README leaves to the skill.

## What an entry is

The entry is the card. A product with no entry cannot sit in a slot — the build stops on an unknown id — and an entry alone shows nothing until `slots.json` points at it.

An entry under an id that already exists updates that product in place, so a swap onto a product already in the plan writes only the fields that moved (a new price row, a `flag` the stack made wrong) and the rest stays as it is. Ids are never renamed and never removed: the routine, the glossary and the other steps' slots all reference them. The product leaving the `current` slot keeps its entry and simply stops being rendered, unless a Top pick still points at it.

Two things an entry does not reach:

- **The glossary** chips are keyed by id inside the Python data files, so a new product joins no ingredient entry there however many actives it carries. Name that in the report instead of editing the data files.
- **The routine step text** — amounts, technique, the wake-up moisturizer's `skip` line — is mine. Report what the swap makes out of date.

## `region` — the brand's home country

`ph`, `intl`, `kr`, `jp`: a Filipino brand manufactured in Korea is still `ph`. The "Your current product" label comes from the slot, not the region, so a Korean product I use is `kr` and still reads as mine, and the origin filter on All products puts it under Korean where it belongs.

The four original current products carry a legacy fifth value, `region='current'`, which the filter treats as Filipino. Leave those as they are and do not copy the value into a new entry.

## `img` — the photo

Copy the URL off the page you opened. Take the largest published image of the product itself rather than its box; on Watsons sites that is the `…-zoom.jpg` or `…-zoom.png` on the product page, e.g. `https://medias.watsons.com.ph/publishing/….-zoom.jpg`.

- No page exposes a photo → `img: null`, and `flag` states that the card shows a drawn label instead.
- `img_alt` holds a second candidate URL where you have one; `get-photos.sh` falls back to it.
- `bash get-photos.sh` downloads what you wrote. A URL that will not download leaves that card on its drawn label — report it.

## `variants` — one row per size

`[size, price text, numeric price, lasts EN, lasts TL]`, main size first — the size I actually bought, since its numeric price drives the sorting and the ₱500-and-under tag. A price you could only approximate is said so in the price text and dated.

Estimate how long each size lasts from the routine's own amounts:

| Step | Amount |
|---|---|
| cleanser | ≈1 ml per wash, twice a day |
| serum | 2–3 drops, twice a day |
| moisturizer | pea to blueberry |
| sunscreen | ¼ teaspoon per daylight day |
| lip balm | thick layer nightly |

## Text fields

`where`, `actives`, `why` and `flag` all ship `en` and `tl`, in the tone of the existing cards — specific, numbers where numbers exist, no marketing.

- `why` — why it suits *my* skin as the Profile in `SKILL.md` describes it, not why it is good in general: the texture against oily skin, what its actives do for the odd pimple, how it sits in a night-shift routine.
- `flag` — the honest watch-out: fragrance, alcohol, acids, older sunscreen filters, price, availability, and whatever the stack re-read in step 5 turned up about this member.
