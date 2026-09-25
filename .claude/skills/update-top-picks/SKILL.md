---
name: update-top-picks
description: Top picks page of index.html — re-researches the currently most popular skincare products in the Philippines and rewrites site-builder/top-picks.json. Use when asked to update or refresh top picks, or when a product change leaves the picks stale.
---

# update-top-picks

Re-research the six Top picks for the Philippines, rewrite `site-builder/top-picks.json`, rebuild the page.

Schemas, file roles, build commands and the list of existing product ids live in `site-builder/README.md`. Read it; this skill does not restate it.

## Profile (changing any of it needs my yes first)

- Oily skin, worst right after waking. One or two pimples now and then. No dark spots. Beginner.
- Night shift: the page is framed **wake-up** and **before-sleep**, never AM/PM. Sunscreen only when there will be daylight.
- Metro Manila. Walk-in at Watsons, Mercury Drug or St. Joseph Drug is the default; an online-only or boutique-only product ships only with that stated plainly in `why`.
- Every text ships in English and Tagalog (`en` and `tl`).

## Receipts

A **receipt** is a page you opened during this run. Every number, ranking, price, stock status and photo URL you write carries one.

- No receipt → the fact stays out. A price you could not confirm exactly is written as approximate.
- Popularity receipts expire at 12 months — discard older ones. Formula and ingredient pages may be older when the formula is unchanged.
- Photo URLs are copied from the page, never constructed from a pattern.
- The Watsons HWB Awards honour brands and distributors — cite them as brand awards only.

## Run

### 1. Score each category

Exactly these six, in this order: `cleanser`, `serum`, `moisturizer`, `sunscreen`, `lipday` (lip balm with SPF, daytime), `lipnight` (lip treatment, bedtime). Each gets one `pick` and one `runner`.

Candidates per category: the incumbent `pick` and `runner` from `top-picks.json`, every product sitting in that step's slots in `slots.json`, plus whatever new the sources below surface.

For each candidate open its Watsons PH product page (`watsons.com.ph`) and record price per size, sizes, stock status and **review count** — the primary popularity metric, because it tracks what Filipinos actually buy. Widen with: the Watsons PH "Best Seller" sort and editorial best-of lists, Mercury Drug availability, current-year Philippine beauty press, brand launch news (a renewed formula replaces the version it succeeds), and Hwahae or @cosme rankings for Korean and Japanese items.

### 2. Rank — popularity first, fit overrides

**The incumbent holds** unless a challenger is clearly more popular (materially higher review count, or ranked above it in current lists) or the incumbent is discontinued or long out of stock.

Fit overrides popularity, and where it does, `why` says so:

- Oily, occasionally pimple-prone: gel and water textures, oil-free, non-comedogenic. Fragrance and alcohol get named.
- **Acid stacking**: acids in the cleanser pick → the serum pick carries no salicylic, glycolic or other exfoliating acid. And the reverse.
- Sunscreen: SPF50 PA++++ on modern photostable filters; note white cast, alcohol, finish.
- `lipday` carries SPF. `lipnight` is a real balm or treatment — no tint, no makeup.
- State the price, and whether the category has a budget option at ₱500 or under.

**Transparency line** — when the most-reviewed product in a category is not the pick, `evidence` names that product, gives its review count, and says why it lost. The serum entry already reads this way; match it.

### 3. Write `site-builder/top-picks.json`

- `updated` carries the run date in English, `updated_tl` the same date with Tagalog month names.
- All six entries get `pick`, `runner`, and rewritten `why`, `rwhy`, `evidence` in both languages. An unchanged pick still gets re-checked numbers and today's date.
- Tone of the existing entries: specific numbers, ₱ prices, no marketing. `rwhy` is one lower-case clause with no trailing period — the builder appends the price.
- Existing product ids keep their name and their data. An outgoing pick stops showing by itself once nothing references it; the routine and glossary still point at those ids.

A `pick` or `runner` that is not already a known id needs an entry in `products-extra.json` first → read `PRODUCT-ENTRY.md` in this folder.

### 4. Build, fetch photos, check

From the folder root:

```
python3 site-builder/build_site.py                          # --zip only when I ask for a zip
bash get-photos.sh
python3 .claude/skills/update-top-picks/check.py
```

`check.py` must print `OK`. It rebuilds, then asserts: every visible product has a photo URL, six Top picks rendered in both languages, English and Tagalog block counts equal, the inline script passes `node --check`, `updated`/`updated_tl` carry today's date, every `evidence` line carries a date and the current year, both languages filled, `rwhy` shaped right, and any new `products-extra.json` entry complete. Each failure it prints is a thing to fix or to explain in the report.

Where a browser is at hand, also open `index.html` offline and confirm the console stays empty.

Edits stay inside `top-picks.json` and `products-extra.json`. Routine steps, glossary text and CSS change only where the build cannot pass without it — and then the report describes the change.

### 5. Publish

Once `check.py` prints `OK`, put the run on the live site — a minute or two:

```
bash site-builder/publish.sh "feat(top-picks): refresh top picks, <run date>"
```

It commits the site files, pushes to GitHub, waits for the deploy and confirms https://heyitsiveen.github.io/personal-care/ serves this build: the last line reads `OK: live site updated`. The downloaded photos stay on this computer; the live page loads the retailer photos. The message is Conventional Commits — subject 50 characters at most, an optional body as the second argument, no AI attribution lines.

- A `check.py` failure still standing → no publish without my yes.
- A `publish.sh` failure → the run stands locally; the report quotes its `FAIL` line.

### 6. Report

A table: category → previous pick → new pick (or "unchanged") → one-line reason → evidence (review count, price, date checked).

Then list: products added, prices or stock that moved, anything available online-only or boutique-only, anything you could not get a receipt for, and the `publish.sh` result — the live URL with the commit, or its `FAIL` line.

## Done when

- Six entries, both languages, every `evidence` re-checked this run and dated, `updated`/`updated_tl` on the run date.
- Every new pick or runner-up present in `products-extra.json` with a receipted photo URL and full bilingual text.
- `check.py` prints `OK`.
- `publish.sh` prints `OK: live site updated`.
- The report is delivered, carrying a Transparency line wherever the most-reviewed product is not the pick.
