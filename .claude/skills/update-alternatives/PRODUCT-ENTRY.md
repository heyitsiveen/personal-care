# Adding a product to `products-extra.json`

Reached from step 4 of `SKILL.md`, when the winner of a slot is not one of the ids the data files already define.

The schema, the field list and the existing ids are in `site-builder/README.md`. This file carries what that README leaves to the skill.

## What an entry is

The entry is the card. A product with no entry cannot sit in a slot — the build stops on an unknown id — and an entry alone shows nothing until `slots.json` points at it.

An entry under an id that already exists updates that product in place, so a refresh writes only the fields that moved (a new price row, a `why` with this run's review count) and the rest of the product stays as it is. Ids are never renamed and never removed: the routine, the glossary and the other steps' slots all reference them. A product that no slot and no Top pick references simply stops being rendered.

## `img` — the photo

Copy the URL off the page you opened. Take the largest published image of the product itself rather than its box; on Watsons sites that is the `…-zoom.jpg` or `…-zoom.png` on the product page, e.g. `https://medias.watsons.com.ph/publishing/….-zoom.jpg`.

- No page exposes a photo → `img: null`, and `flag` states that the card shows a drawn label instead.
- `img_alt` holds a second candidate URL where you have one; `get-photos.sh` falls back to it.
- `bash get-photos.sh` downloads what you wrote. A URL that will not download leaves that card on its drawn label — report it.

## `variants` — one row per size

`[size, price text, numeric price, lasts EN, lasts TL]`, main size first. The numeric price of that first row drives the sorting, the ₱500-and-under tag and the budget band, so it is that size's regular price; a promo or a small-size price that dips under ₱500 is said plainly in `flag`.

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

- `why` — why it suits *my* skin as the Profile in `SKILL.md` describes it, and what won it the slot: the review count, the price against the slot's band.
- `flag` — the honest watch-out: fragrance, alcohol, acids, older sunscreen filters, price, availability, a review count too thin to lean on.
