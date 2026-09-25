# Adding a product to `products-extra.json`

Reached from step 3 of `SKILL.md`, when a `pick` or `runner` is not one of the ids the data files already define.

The schema, the field list and the existing ids are in `site-builder/README.md`. This file carries what that README leaves to the skill.

## Where the new product shows up

A Top pick is rendered on the Top picks page and appended to All products automatically — no other file to edit. It joins a **routine** step only through `slots.json`, which belongs to the `update-alternatives` skill; mention it in the report rather than editing slots here.

Existing ids are never renamed and never removed: the routine, the glossary and the slots all reference them. A product that nothing references simply stops being rendered.

## `img` — the photo

Copy the URL from the page you opened. Take the largest published image of the product itself rather than its box; on Watsons sites that is the `…-zoom.jpg` or `…-zoom.png` on the product page, e.g. `https://medias.watsons.com.ph/publishing/….-zoom.jpg`.

- No page exposes a photo → `img: null`, and `flag` states that the card has no photo (it shows the brand initial).
- `img_alt` holds a second candidate URL where you have one.

## `variants` — one row per size

`[size, price text, numeric price, lasts EN, lasts TL]`, main size first. The numeric price drives sorting and the ₱500-and-under filter, so it is that size's regular price; a promo or a tiny-size price that dips under ₱500 is said plainly in `flag`.

Estimate how long a size lasts from the routine's own amounts:

| Step | Amount |
|---|---|
| cleanser | ≈1 ml per wash, twice a day |
| serum | 2–3 drops, twice a day |
| moisturizer | pea to blueberry |
| sunscreen | ¼ teaspoon per daylight day |
| lip balm | thick layer nightly |

## Text fields

`where`, `actives`, `why` and `flag` all ship `en` and `tl`, in the tone of the existing cards — specific, numbers where numbers exist, no marketing.

- `why` — why it suits *my* skin as the Profile in `SKILL.md` describes it, not why it is good in general.
- `flag` — the honest watch-out: fragrance, alcohol, acids, older sunscreen filters, price, availability, a review count too thin to lean on.
