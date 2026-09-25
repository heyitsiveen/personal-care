---
name: update-alternatives
description: Alternative slots of index.html — re-researches the currently most popular products in the Philippines per origin and price band and rewrites site-builder/slots.json. Use when asked to update or refresh the alternatives, for every step or one named step, or when a slot's product turns out discontinued or long out of stock.
---

# update-alternatives

Re-research the alternative products of every routine step, move the winners into `site-builder/slots.json`, rebuild the page.

Schemas, file roles, build commands and the list of existing product ids live in `site-builder/README.md`. Read it; this skill does not restate it.

## Profile (changing any of it needs my yes first)

- Oily skin, worst right after waking. One or two pimples now and then. No dark spots. Beginner.
- Night shift: the page is framed **wake-up** and **before-sleep**, never AM/PM. Sunscreen only when there will be daylight.
- Metro Manila. Walk-in at Watsons, Mercury Drug or St. Joseph Drug is the default; an online-only or boutique-only product takes a slot only with that stated plainly in `flag`.
- Every text ships in English and Tagalog (`en` and `tl`).

## Slots

Six steps — `cleanse`, `serum`, `moist`, `sun`, `daylip` (lip balm with SPF, daytime), `lip` (lip treatment, bedtime) — each carrying the same eight slots:

- `current` — **not this skill's slot.** `update-current-products` owns it; it leaves the run exactly as it arrived.
- `intl`, `kr`, `jp` — the best alternative of that origin at any price. `intl` means a brand from outside Asia.
- `ph_budget`, `intl_budget`, `kr_budget`, `jp_budget` — the same, plus Filipino, at ₱500 and under.

**Origin** is the brand's home country: a Filipino brand manufactured in Korea is still `ph`. **Band** is read off the main size's regular price; a product that dips under ₱500 only in a small size or only on promo holds a budget slot only when its card says which.

One id per slot, and never the same id in two slots of one step. A challenger takes the slot of the incumbent it beats — the step never grows a ninth card, and the beaten product is left in the data, simply unreferenced.

Every empty slot is a target: fill it, or the report says what the research turned up instead. The two empty `current` slots (`daylip`, `lip`) are the exception — they stay empty until I buy one.

## Receipts

A **receipt** is a page you opened during this run. Every number, ranking, price, stock status and photo URL you write carries one.

- No receipt → the fact stays out. A price you could not confirm exactly is written as approximate.
- Popularity receipts expire at 12 months — discard older ones. Formula and ingredient pages may be older when the formula is unchanged.
- Photo URLs are copied from the page, never constructed from a pattern.
- The Watsons HWB Awards honour brands and distributors — cite them as brand awards only.

## Run

### 1. Baseline

```
python3 .claude/skills/update-alternatives/check.py --snapshot
```

Records `slots.json` before anything moves, so the check can prove `current` never moved and the report can name the product every slot held before. The date it prints is the run date: the report's, and the one the 12-month window counts back from.

Scope is all six steps, unless I name one — then only that step's eight slots, and the report covers that step alone.

### 2. Research each slot

Candidates for a slot: the incumbent sitting in it, plus everything the sources below surface that matches the slot's origin and band.

For each candidate open its Watsons PH product page (`watsons.com.ph`) and record price per size, sizes, stock status, the photo URL, and **review count** — the primary popularity metric, because it tracks what Filipinos actually buy. Widen with: the Watsons PH "Best Seller" sort and editorial best-of lists, Mercury Drug availability, current-year Philippine beauty press, brand launch news (a renewed formula or a new oily-skin version replaces the version it succeeds), and Hwahae or @cosme ratings for Korean and Japanese items.

### 3. Rank — the incumbent holds

The incumbent keeps its slot unless a challenger is clearly more popular (materially higher review count, or ranked above it in current lists), or the incumbent is discontinued or long out of stock, or the challenger is a clearly better fit at comparable popularity. Moved or kept, every slot carries its reason and its numbers into the report — a slot you did not research is not a "kept".

Fit overrides popularity, and where it does, the card's `flag` and the report say so:

- Oily, occasionally pimple-prone: gel and water textures, oil-free, non-comedogenic. Fragrance and alcohol get named.
- **Acid stacking**: while the `current` cleanser carries AHA or BHA, no serum slot carries an exfoliating acid.
- Sunscreen: SPF50 PA++++ on modern photostable filters; note white cast, alcohol, finish.
- `daylip` carries SPF. `lip` is a real balm or treatment — no tint, no makeup.

### 4. Write the files

- `site-builder/products-extra.json` — a product new to the plan needs a complete entry before it can sit in a slot → `PRODUCT-ENTRY.md` in this folder. A product already in the plan whose price, sizes, stock or review count moved gets an entry under its existing id.
- `site-builder/slots.json` — the winning ids. `current` untouched, all eight keys kept on every step, `null` where the research left a slot empty.
- Top picks: a product that leaves a slot while it is a `pick` or `runner` in `top-picks.json` stays visible and stays correct. Say so in the report and offer to run `update-top-picks`; picks do not change here.

### 5. Build, fetch photos, check

From the folder root:

```
python3 site-builder/build_site.py                          # --zip only when I ask for a zip
bash get-photos.sh
python3 .claude/skills/update-alternatives/check.py
```

`check.py` must print `OK`. It rebuilds, then asserts: the six steps and their eight slots, one id per slot and no id twice in a step, each slot's origin and category, budget slots at ₱500 and under, SPF in `daylip` and no tint in `lip`, `current` identical to the baseline, a photo URL on every visible product, All products equal to the slots plus Top picks, English and Tagalog blocks in step, and `node --check` on the inline script. It also prints every slot that moved — the report's previous-product column — and every slot still empty. Each failure it prints is a thing to fix or to explain in the report.

Where a browser is at hand, also open `index.html` offline and confirm the console stays empty.

Edits stay inside `slots.json` and `products-extra.json`. Routine steps, glossary text and CSS change only where the build cannot pass without it — and then the report describes the change.

### 6. Publish

Once `check.py` prints `OK`, put the run on the live site — a minute or two:

```
bash site-builder/publish.sh "feat(alternatives): refresh <all | step> alternatives"
```

It commits the site files, pushes to GitHub, waits for the deploy and confirms https://heyitsiveen.github.io/personal-care/ serves this build: the last line reads `OK: live site updated`. The downloaded photos stay on this computer; the live page loads the retailer photos. The message is Conventional Commits — subject 50 characters at most, an optional body as the second argument listing the slots that moved, no AI attribution lines.

- A `check.py` failure still standing → no publish without my yes.
- A `publish.sh` failure → the run stands locally; the report quotes its `FAIL` line.

### 7. Report

One table per step: slot → previous product → new product (or "kept") → reason → evidence (review count, price, date checked).

Then: products added, slots left empty and what the research found there, anything online-only or boutique-only, prices written as approximate, anything you could not get a receipt for, whether `update-top-picks` should be re-run, and the `publish.sh` result — the live URL with the commit, or its `FAIL` line.

## Done when

- Every slot in scope is filled as far as the research allows, and every remaining `null` is explained in the report.
- Every product new to a slot is complete in `products-extra.json` — receipted photo URL, sizes with prices and durations, where to buy, actives, why, watch-out, both languages.
- `check.py` prints `OK`, photos fetched, console clean.
- `publish.sh` prints `OK: live site updated`.
- The report accounts for all eight slots of every step in scope, moved or kept.
