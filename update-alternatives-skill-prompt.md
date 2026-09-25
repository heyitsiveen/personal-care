# Prompt: create the `update-alternatives` skill

Copy everything below the line into Claude (Claude Code or Cowork, opened in the `personal-care` folder). Afterwards, trigger it with **"update alternatives"**, **"refresh the alternative products"** or **"/update-alternatives"** (optionally naming one step, e.g. "update alternatives for sunscreen only").

---

Create a skill called **`update-alternatives`** for this project. When triggered, it re-researches the alternative products on the routine page of `index.html` and **replaces** them in a **fixed slot structure** with whatever is *currently* most popular and highly recommended in the Philippines for each slot, with the same complete card structure the page already uses. It never appends: one product per slot, and a replacement takes the slot of the product it beats. The All products page is generated from the same slots, so it updates automatically. Write it as a `SKILL.md` (frontmatter `name`, `description`) plus any helper scripts, following the rules below. Read `site-builder/README.md` first: it documents `slots.json`, `products-extra.json` and the build command.

## Facts about me (do not change without asking)

Oily skin, one or two pimples now and then, no dark spots, beginner. Night-shift schedule: **wake-up** and **before-sleep** routines; sunscreen only when there will be daylight. Metro Manila; products must be purchasable at Watsons, Mercury Drug, St. Joseph Drug or similar (online-only or boutique-only allowed only if clearly flagged). Every text is bilingual (`en` and `tl`).

## The fixed slot structure (the whole point of this skill)

`site-builder/slots.json` has one map per step — `cleanse`, `serum`, `moist`, `sun`, `daylip` (lip balm with SPF, daytime), `lip` (lip treatment, bedtime) — with exactly these slots:

| Slot | Meaning | Price band |
|---|---|---|
| `current` | the product I use — **never touched by this skill** (that is the `update-current-products` skill) | — |
| `intl` | best international (non-Asian-brand) alternative | any price |
| `kr` | best Korean alternative | any price |
| `jp` | best Japanese alternative | any price |
| `ph_budget` | best Filipino alternative | ₱500 and under |
| `intl_budget` | best international alternative | ₱500 and under |
| `kr_budget` | best Korean alternative | ₱500 and under |
| `jp_budget` | best Japanese alternative | ₱500 and under |

Rules: one product id per slot, never the same product in two slots of the same step; a slot may be `null` only if, after real research, nothing suitable exists (say so in the report — an empty `ph_budget` for serum/moisturizer/sunscreen is acceptable if no Filipino product under ₱500 is genuinely popular and suitable). Aim to **fill currently empty slots** (`daylip` and `lip` are missing `intl_budget`, `kr_budget` and a `current`; that `current` stays empty until I buy one).

## Research protocol (every run, fresh numbers)

1. **Date-stamp.** Record the run date; discard popularity sources older than 12 months. Formula/ingredient pages may be older if unchanged.
2. **Popularity, measured.** For every candidate open the Watsons PH product page and record price per size, stock, **review count** (the primary metric: what Filipinos actually buy), and the photo URL. Add: Watsons PH "Best Seller" sort and editorial lists, Mercury Drug availability, current-year Philippine beauty press, launch news (a renewed formula or a new oily-skin version replaces the old one), and Hwahae/@cosme ratings for Korean/Japanese items. The Watsons HWB Awards honour brands and distributors, not products — do not cite them as product awards.
3. **Candidates per slot:** the product currently in the slot plus new contenders from the sources above, filtered by origin and price band. Origin means the brand's home country (a Filipino brand made in Korea is still `ph`). Price band uses the **main size's regular price**; a product that is under ₱500 only in a tiny size or only on promo may hold a budget slot only if the card says so plainly.
4. **Fit rules (may override popularity — and when they do, say so in `flag`):** gel/water textures, oil-free, non-comedogenic preferred; flag fragrance and alcohol; sunscreen SPF50/PA++++ with modern photostable filters preferred, note white cast and finish; `daylip` must have SPF; `lip` must be a real balm/treatment (no tint). Avoid a serum slot whose product stacks acids with my current cleanser if that cleanser has AHA/BHA.
5. **Replace only with evidence.** Keep the incumbent unless the contender is clearly more popular (materially higher review count, ranked above it in current lists, or the incumbent is discontinued/out of stock long-term) **or** a clearly better fit at a comparable popularity level. Write the reason in the report.
6. **Verify everything** from pages opened during the run; never invent counts, prices or rankings; mark approximate prices as approximate.

## What to update

### `site-builder/products-extra.json`
For every **new** product: a complete entry (schema in the README) so its card matches the existing structure — verified `img` (product photo, not the box; `…-zoom.jpg/png` from the retailer page; never a guessed pattern; `null` only if truly none exists, stated in `flag`), `brand`, `name`, `region`, `category`, `shape`, `where`, `actives`, `why` (why it suits my skin), `flag` (honest watch-out: fragrance, alcohol, acids, filters, price, availability, review caveats), and `variants` with **one row per size**: size, price text, numeric price (main size first, used for sorting and the ₱500 tag), and a duration per size using the routine's amounts (cleanser ≈1 ml per wash twice a day; serum 2–3 drops twice a day; moisturizer pea-to-blueberry; sunscreen ¼ teaspoon per daylight day; lip balm thick layer nightly). Both languages, same tone as existing cards. You may also refresh the fields of an **existing** product (price, stock note, review count in `why`) by adding an entry with its id.

### `site-builder/slots.json`
Set the new ids in the slots. Do not touch `current`. Do not delete the old product's data — it simply stops being shown once no slot or Top pick references it.

### Top picks consistency
If a replaced product is a `pick` or `runner` in `site-builder/top-picks.json`, it stays visible; tell me and offer to run `update-top-picks`. Do not change Top picks silently.

## Rebuild and verify

1. `python3 site-builder/build_site.py` from the folder root (`--zip` if I ask).
2. `bash get-photos.sh` to download new photos and refresh `images/photos.js`.
3. Checks: the build line shows every visible product has a photo URL (explain each gap); English and Tagalog block counts match (`grep -c 'class="l-en"'` = `grep -c 'class="l-tl"'`); the inline script passes `node --check`; if a headless browser is available, open the page offline with zero console errors; each step's cards appear in slot order — current, international, Korean, Japanese, then the "Budget picks" divider with Filipino, international, Korean, Japanese; the All products count equals the number of distinct products in slots plus Top picks.
4. Publish: `bash site-builder/publish.sh "feat(alternatives): refresh <all | step> alternatives"` — it commits, pushes, waits for the deploy and must end with `OK: live site updated` (Conventional Commits message, no AI attribution lines).

## Report back

A table per step: slot → previous product → new product (or "kept") → reason → evidence (review count, price, date checked). Then: new products added, empty slots and why, products only available online/boutique, prices marked approximate, anything you could not verify, and whether Top picks should be re-run.

## Guardrails

Never edit the `current` slots, never append products to steps, never remove or rename existing ids, never guess photo URLs, keep the wake-up/before-sleep framing and my skin profile, and do not edit CSS, step instructions or glossary text unless needed for the build to pass (describe any such change).

## Definition of done

Every step has its slots filled as far as real research allows, each slot's card is complete (image, brand, label, sizes with prices and durations, where to buy, actives, why, watch-out, in English and Tagalog), the routine and All products pages are rebuilt with photos fetched and a clean console, the live site is updated (`publish.sh` printed `OK: live site updated`), and the report explains every replacement and every empty slot.
