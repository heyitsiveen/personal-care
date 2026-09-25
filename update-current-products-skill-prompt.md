# Prompt: create the `update-current-products` skill

Copy everything below the line into Claude (Claude Code or Cowork, opened in the `personal-care` folder). Afterwards, trigger it with a message like **"update my current products: I now use X for cleanser"** or **"/update-current-products"**.

---

Create a skill called **`update-current-products`** for this project. It is triggered when I tell you that a product I personally use has changed (phrases: "update my current products", "I switched my cleanser/serum/moisturizer/sunscreen/lip balm to …", "/update-current-products"). It replaces the **"Your current product"** card of the affected step(s) in `index.html` with a fully researched card for the new product, keeps everything else intact, and rebuilds. Write it as a `SKILL.md` (frontmatter `name`, `description`) plus any helper scripts, following the rules below. Read `site-builder/README.md` first: it documents `slots.json`, `products-extra.json` and the build command.

## Facts about me (do not change without asking)

Oily skin, one or two pimples now and then, no dark spots, beginner. Night-shift schedule: the page uses **wake-up** and **before-sleep** routines, sunscreen only when there will be daylight. Metro Manila; products should be purchasable at Watsons, Mercury Drug, St. Joseph Drug or similar. Every text is bilingual (`en` and `tl`).

## What "current product" means in the files

`site-builder/slots.json` has one map per step (`cleanse`, `serum`, `moist`, `sun`, `daylip`, `lip`); the `current` slot holds the id of the product I use. Product data lives in the Python data files for the original items and in `site-builder/products-extra.json` for anything added later. An entry in `products-extra.json` with an **existing** id overrides that product's fields in place; an entry with a **new** id creates a new product.

## Procedure when triggered

1. **Confirm the change.** Identify the step(s) and the exact product (brand, full name, size). If I gave only a partial name, search for it and ask me to confirm the exact product before editing. If I say I stopped using a step entirely, set that step's `current` to `null` and tell me the routine will show alternatives only.
2. **Research the new product (verify, do not assume):**
   - Watsons PH product page (`watsons.com.ph`): price for every size, stock status, review count, the ingredient list, and the product photo URL (the `…-zoom.jpg/png` image on the page). If Watsons does not carry it, use Mercury Drug, the brand's official Philippine store (Shopee/Lazada mall or website) and note availability honestly.
   - Ingredients: full list from the retailer/brand page or SkinSort; identify actives, fragrance, alcohol, acids.
   - Dates: record the date checked and write it into the card where a price is approximate.
3. **Write the product entry** in `products-extra.json` (schema in the README): `brand`, `name`, `region` (`ph` for Filipino brands, otherwise `intl`/`kr`/`jp`), `category`, `shape`, `img` (verified photo URL, never a guessed pattern), `where`, `actives`, `why`, `flag`, and `variants` with a duration per size using the routine's amounts (cleanser ≈1 ml per wash twice a day; serum 2–3 drops twice a day; moisturizer pea-to-blueberry; sunscreen ¼ teaspoon per daylight day; lip balm thick layer nightly). Write `why` as why it suits *my* skin and `flag` as an honest watch-out (fragrance, alcohol, acids, older sunscreen filters, price, availability). Both languages, same tone as the existing cards.
4. **Point the slot at it:** set `slots.json` → step → `current` to the new id. Do not delete the old product's data.
5. **Routine-coherence check across all current products** and report anything that needs my decision:
   - acid stacking (two products with AHA/BHA in the same routine),
   - total niacinamide load if several products contain it,
   - fragrance/alcohol in more than one leave-on product,
   - a sunscreen with older filters (oxybenzone/avobenzone without stabilisers) when daylight exposure is long,
   - whether the wake-up moisturizer stays optional (it is optional for oily skin when the sunscreen is hydrating).
   Update the affected `flag` text if the new product changes one of these (for example, if the new cleanser has no acids, the serum flag about acid stacking should be relaxed).
6. **Top picks consistency:** if the old current product is a `pick` or `runner` in `site-builder/top-picks.json`, keep it there (the builder keeps it visible) but tell me, and offer to run the `update-top-picks` skill; if the new product is clearly the better pick for its category, say so rather than silently changing the Top picks page.
7. **Rebuild and verify:** `python3 site-builder/build_site.py` from the folder root (add `--zip` if I ask); `bash get-photos.sh` to download the new photo and refresh `images/photos.js`; confirm the build line shows every visible product has a photo URL, English and Tagalog block counts match (`grep -c 'class="l-en"'` = `grep -c 'class="l-tl"'`), the inline script passes `node --check`, and — if a headless browser is available — the page opens offline with zero console errors and the new card shows "Your current product" in both languages. Then publish: `bash site-builder/publish.sh "feat(current): switch <step> to <brand>"` — it commits, pushes, waits for the deploy and must end with `OK: live site updated` (Conventional Commits message, no AI attribution lines).
8. **Report:** for each changed step: old product → new product, price and size, key actives, the watch-out, and the coherence findings from step 5. List anything you could not verify.

## Guardrails

- Never remove or rename existing product ids; never append products to steps (slots are fixed).
- Never guess photo URLs; never invent review counts or prices; mark approximate prices as approximate.
- Keep the wake-up/before-sleep framing and my skin profile unchanged unless I say otherwise.
- Do not edit CSS, routine step instructions or glossary text unless required for the build to pass; if you do, describe the change.

## Definition of done

The changed step(s) show the new product as "Your current product" on the routine page and on All products, its card has image, brand, label, sizes with prices and durations, where to buy, key actives, why-it-fits and watch-out in English and Tagalog; the coherence check was reported; the page rebuilt and photos fetched with a clean console; the live site updated (`publish.sh` printed `OK: live site updated`).
