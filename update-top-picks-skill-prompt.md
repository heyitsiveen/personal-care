# Prompt: create the `update-top-picks` skill

Copy everything below the line into Claude (Claude Code or Cowork, opened in the `personal-care` folder) to have it create the skill. Afterwards, trigger the skill with a message like **"update top picks"** or **"/update-top-picks"**.

---

Create a skill called **`update-top-picks`** for this project. The skill is triggered on demand (phrases: "update top picks", "refresh top picks", "/update-top-picks") and, when run, researches the *currently* most popular and highly recommended skincare products in the Philippines for each step of my routine, then updates the **Top picks** page of `index.html` by editing JSON files and rebuilding. Write it as a `SKILL.md` (with frontmatter `name` and `description`) plus any helper scripts you need, following the structure and rules below. Read `site-builder/README.md` first: it documents the builder and the two JSON files the skill edits.

## Who this is for (never change these facts without asking me)

- Me: oily skin (worst right after waking), one or two pimples now and then, no dark spots, skincare beginner.
- Night-shift schedule: the routine is framed as **wake-up** and **before-sleep**, not AM/PM; sunscreen only when there will be daylight.
- Location: Metro Manila. Products must be purchasable in the Philippines at Watsons, Mercury Drug, St. Joseph Drug or similar; online-only or boutique-only items are allowed only if clearly flagged.
- The page is bilingual: every text you write must exist in **English and Tagalog** (`en` and `tl` keys).

## Categories to research (exactly these six, in this order)

`cleanser`, `serum`, `moisturizer`, `sunscreen`, `lipday` (lip balm with SPF for daytime), `lipnight` (lip treatment at bedtime). Each gets one **pick** and one **runner-up**.

## Research protocol (do this every run, do not reuse stale numbers)

1. **Date-stamp everything.** Record the run date; every evidence line must say when the numbers were checked. Discard any source older than 12 months for popularity claims; formulas/ingredients may come from older pages if unchanged.
2. **Popularity, measured not guessed.** For each candidate, open the Watsons Philippines product page (`watsons.com.ph`) and record: current price, sizes, in-stock status, and the **review count**. Review count on Watsons PH is the primary popularity metric because it reflects what Filipinos actually buy. Supplement with: Watsons PH "Best Seller" sort and editorial "best of" lists, Mercury Drug availability, Philippine beauty press roundups from the current year, brand launch news (new versions replace old ones), and for Korean/Japanese items Hwahae or @cosme rankings and ratings. The Watsons HWB Awards honour brands/distributors, not products; do not present them as product awards.
3. **Candidate set.** Start from the products already in the page (list in `site-builder/README.md`) plus anything new that appears in the sources above. Do not drop the current pick without evidence that something else is now clearly more popular or a better fit.
4. **Fit rules (these can override popularity, and when they do, say so):**
   - Oily, occasionally pimple-prone skin: prefer gel/water textures, oil-free, non-comedogenic; flag fragrance and alcohol.
   - **No acid stacking:** if the cleanser pick contains AHA/BHA, the serum pick must not contain salicylic acid, glycolic acid or other exfoliating acids, and vice versa.
   - Sunscreen: SPF50/PA++++ with modern photostable filters preferred; note white cast, alcohol, finish.
   - `lipday` must have SPF; `lipnight` must be an actual treatment/balm (no tint, no makeup).
   - Price matters: state the price and whether a budget (₱500 and under) option exists; prefer walk-in availability.
5. **Disclosure rule.** If the most-reviewed product in a category is *not* the pick, the evidence line must name it, give its review count, and explain why it was not chosen.
6. **Verify, do not assume.** Every fact in `evidence` must come from a page you opened during this run. Mark approximate prices as approximate. Never invent review counts, awards or rankings.

## What to update

### `site-builder/top-picks.json`
- Set `updated` (English, e.g. "3–4 March 2027") and `updated_tl` (Tagalog month names).
- For each of the six categories, set `pick`, `runner`, and rewrite `why`, `rwhy` and `evidence` in both languages. Keep the tone of the existing entries: specific numbers, prices in ₱, no marketing fluff. `rwhy` is a single lower-case clause with no trailing period; the price is appended automatically.
- If a pick or runner-up stays the same, still refresh its evidence numbers and dates.

### `site-builder/products-extra.json`
- If a chosen pick or runner-up is not yet a known product id, add it here using the schema in the README, with all `en`/`tl` texts, `variants` with a per-size duration estimate (use the same amounts as the routine: cleanser ≈1 ml per wash twice a day; serum 2–3 drops twice a day; moisturizer pea-to-blueberry; sunscreen ¼ teaspoon per daylight day; lip balm nightly thick layer), and the right `steps` so it also appears in the routine.
- **Photo rule:** `img` must be a real product photo URL taken from the retailer or brand product page you opened (for Watsons sites use the `…-zoom.jpg/png` URL found on the page, e.g. `https://medias.watsons.com.ph/publishing/….-zoom.jpg`). Prefer a photo of the product itself, not the box. Never guess a URL pattern. If no page exposes a photo, set `img` to `null` and say so in `flag`.
- Never delete or rename existing products; the routine and glossary reference them.

### Rebuild and verify
1. `python3 site-builder/build_site.py` from the folder root (add `--zip` if I ask for a zip).
2. `bash get-photos.sh` so any new photos are stored locally and `images/photos.js` is refreshed.
3. Checks: the build prints `with photo URL` equal to the product count (or explain each gap); English and Tagalog block counts match (`grep -c 'class="l-en"'` = `grep -c 'class="l-tl"'`); the inline script passes `node --check`; if a headless browser is available, open the page offline and confirm zero console errors; the Top picks page shows six cards, each with an Evidence line carrying the new date.
4. Do not touch the routine steps, glossary text or CSS unless a fix is needed for the build to pass; if you must, describe the change.

## Report back (in chat, after the files are updated)

A short table: category → previous pick → new pick (or "unchanged") → one-line reason → key evidence (review count, price, date). Then list: new products added, products whose price or stock status changed, anything only available online/boutique, and anything you could not verify. Ask before making any change that alters my skin-profile assumptions or removes a product.

## Definition of done

- `top-picks.json` has six entries with fresh `evidence` for all, both languages, correct `updated` dates.
- Any new product is in `products-extra.json` with a verified photo URL and full bilingual text.
- `index.html` rebuilt, photos fetched, checks passed, console clean.
- Report delivered with the disclosure rule honoured wherever the most popular product was not chosen.
