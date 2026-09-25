---
name: update-current-products
description: Current products of index.html — researches the product I switched to and swaps it into the `current` slot of site-builder/slots.json as a full bilingual card. Use when I say I switched or stopped using my cleanser, serum, moisturizer, sunscreen or lip balm, or ask to update my current products.
---

# update-current-products

Swap a step's product for the one I use now: one researched card, the `current` slot repointed, the stack re-read, the page rebuilt.

Schemas, file roles, build commands and the list of existing product ids live in `site-builder/README.md`. Read it; this skill does not restate it.

## Profile (changing any of it needs my yes first)

- Oily skin, worst right after waking. One or two pimples now and then. No dark spots. Beginner.
- Night shift: the page is framed **wake-up** and **before-sleep**, never AM/PM. Sunscreen only when there will be daylight.
- Metro Manila. Walk-in at Watsons, Mercury Drug or St. Joseph Drug is the default; an online-only or boutique-only product says so plainly in `flag`.
- Every text ships in English and Tagalog (`en` and `tl`).

## The stack

The `current` slot of the six steps — `cleanse`, `serum`, `moist`, `sun`, `daylip` (lip balm with SPF, daytime), `lip` (lip treatment, bedtime) — holds what is actually on my face. Those six are the **stack**: they meet on one face, so a swap is judged against the whole of it and can make another member's card wrong.

The other seven slots of each step are alternatives — `update-alternatives` owns them, and they leave this run exactly as they arrived.

## Receipts

A **receipt** is a page you opened during this run. Every price, size, stock status, review count, ingredient and photo URL you write carries one.

- No receipt → the fact stays out. A price you could not confirm exactly is written as approximate and dated in the card.
- Prices and stock go stale fastest — confirm them this run, whatever an older page says. A formula or ingredient page may be older when the formula is unchanged.
- Photo URLs are copied from the page, never constructed from a pattern.

## Run

### 1. Confirm — no confirmed product, no edit

Record the baseline first, before anything moves:

```
python3 .claude/skills/update-current-products/check.py --snapshot
```

Then pin down the step(s) and the exact product: brand, full name, size, and which variant where a line has several (sensitive or oily formula, the SPF version, a renewed formula). One product can land in two steps — a lip balm with SPF is `daylip` and `lip` both, when I say I use it for both.

A partial name ("I'm on the CeraVe one now") is researched into a shortlist and handed back to me: the edit waits for my yes.

Three branches settle without research:

- **I stopped a step** → that step's `current` goes `null`, the step shows alternatives only, and the run picks up at step 5.
- **The id is already in the plan** → no new entry unless its price, sizes, stock or photo have moved; pick up at step 3.
- **It is already the `current` product** → say so and stop; nothing to swap.

### 2. Research the product

Open its Watsons PH product page (`watsons.com.ph`) and record price for every size, the sizes, stock status, review count, the ingredient list and the photo URL. Not carried there → Mercury Drug, then the brand's official Philippine store (Shopee or Lazada mall, or the brand site), and the card says plainly where it can actually be bought.

The full ingredient list comes off the retailer or brand page, or SkinSort. Read out of it the five things step 5 needs: the actives and their percentages, fragrance or parfum, alcohol denat, exfoliating acids (salicylic, glycolic, lactic, mandelic), and for a sunscreen the filters and whether they are modern and photostable.

### 3. Write the entry

A product new to the plan needs a complete entry in `site-builder/products-extra.json` before it can sit in a slot → `PRODUCT-ENTRY.md` in this folder. A product already in the plan gets an entry under its existing id carrying only the fields that moved.

### 4. Point the slot

`site-builder/slots.json` → the step → `current` → the new id. The rest of the file holds still: the outgoing product keeps its entry and simply stops being rendered, and the step keeps its eight slots.

Two knock-ons are settled here and named in the report:

- **The id already sits in another slot of that step** — the alternative I went and bought. `current` takes it and the slot it vacated goes `null`, so the step never shows one card twice. Offer to run `update-alternatives` to refill that slot.
- **The outgoing product is a `pick` or `runner` in `top-picks.json`** — it stays there and stays visible. Say so and offer `update-top-picks`. Where the product I now use is plainly the better pick for its category, say that too; picks do not change here.

### 5. Re-read the stack

Read the six `current` products together — a swap changes what the others' cards should say. `check.py` prints what it can see in the names, actives and flags; each line below is decided on the ingredient lists from step 2, not on card text alone.

- **Acid stacking** — an AHA or BHA in two members at once. Name both, and which to drop or alternate.
- **Niacinamide load** — add the percentages across the members that carry it and give the total.
- **Fragrance and alcohol** — in more than one leave-on (serum, moisturizer, sunscreen, lip); a rinse-off cleanser weighs lightly.
- **Sunscreen filters** — oxybenzone, or avobenzone with nothing to stabilise it, against a long daylight stretch.
- **Wake-up moisturizer** — it stays optional while the sunscreen is hydrating. A drying new sunscreen makes it needed, which puts the step's own `skip` text out of date: that text is mine to change, so report it rather than edit it.

Every `flag` the swap makes wrong is rewritten in both languages, in both directions — an acid-free new cleanser relaxes the serum's acid-stacking warning exactly as an acid one raises it. A finding that needs my decision (drop one, alternate days, keep both) comes to me in the report; it is not decided here.

### 6. Build, fetch photos, check

From the folder root:

```
python3 site-builder/build_site.py                              # --zip only when I ask for a zip
bash get-photos.sh
python3 .claude/skills/update-current-products/check.py
```

`check.py` must print `OK`. It rebuilds, then asserts: the six steps and their eight slots, one id per slot and no id twice in a step, each `current` product's category against its step, SPF in a `daylip` current and no tint in a `lip` current, every alternative slot identical to the baseline, a card carrying "Your current product" and "Kasalukuyang produkto mo" for each current id, a photo URL on every visible product, All products equal to the slots plus Top picks, English and Tagalog blocks in step, any new `products-extra.json` entry complete, and `node --check` on the inline script. It also names the `current` slots that moved — the report's old-product column — and prints the stack scan of step 5. Each failure is a thing to fix or to explain in the report.

Where a browser is at hand, also open `index.html` offline and confirm the console stays empty.

Edits stay inside `slots.json` and `products-extra.json`. Routine steps, glossary text and CSS change only where the build cannot pass without it — and then the report describes the change.

### 7. Publish

Once `check.py` prints `OK`, put the run on the live site — a minute or two:

```
bash site-builder/publish.sh "feat(current): switch <step> to <brand>"     # or "feat(current): stop <step>"
```

It commits the site files, pushes to GitHub, waits for the deploy and confirms https://heyitsiveen.github.io/personal-care/ serves this build: the last line reads `OK: live site updated`. The downloaded photos stay on this computer; the live page loads the retailer photos. The message is Conventional Commits — subject 50 characters at most, an optional body as the second argument, no AI attribution lines.

- A `check.py` failure still standing → no publish without my yes.
- A `publish.sh` failure → the run stands locally; the report quotes its `FAIL` line.

### 8. Report

Per changed step: old product → new product, sizes with prices and what each lasts, key actives, the watch-out, and where it is bought.

Then: the stack findings from step 5 and the decisions waiting on me, the `top-picks.json` knock-on, any alternative slot left `null` by the swap, prices written as approximate, everything you could not get a receipt for, and the `publish.sh` result — the live URL with the commit, or its `FAIL` line.

## Done when

- Every changed step shows the new product as "Your current product" on the routine page and on All products, in both languages, with photo, sizes, prices, durations, where to buy, actives, why-it-fits and watch-out.
- A product I named only partially was confirmed with me before anything was written.
- The stack was read as a whole, every `flag` the swap made wrong was rewritten, and the findings are in the report.
- `check.py` prints `OK`, photos fetched, console clean.
- `publish.sh` prints `OK: live site updated`.
