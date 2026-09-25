# site-builder — how index.html is generated

Run from the folder that contains `index.html`:

    python3 site-builder/build_site.py          # rebuilds index.html + images/*.svg + get-photos.sh
    python3 site-builder/build_site.py --zip    # same, and writes ../personal-care.zip (photos excluded)
    bash get-photos.sh                          # downloads the real product photos into images/ and updates images/photos.js
    bash site-builder/publish.sh "type(scope): summary"   # puts the build on the live site (see Publishing)

The builder never deletes anything in the folder; downloaded photos and `images/photos.js` are kept.

## Files

| File | What it is | Edit it? |
|---|---|---|
| `data_base.py` | The 19 original products, UI strings, routine steps, ingredient glossary | Rarely (structure) |
| `data_v2.py` | Product updates, sizes, CSS/JS, Top-picks-independent layout | Rarely (structure) |
| `build_site.py` | Budget products, glossary additions, Top picks view, rendering, output | Rarely (structure) |
| `slots.json` | **Which product sits in which slot of each routine step** (current, intl, kr, jp, ph_budget, intl_budget, kr_budget, jp_budget). The routine page and the All products page are generated from this. | **Yes — edited by the update-alternatives and update-current-products skills** |
| `top-picks.json` | **The Top picks page content** (one entry per category) | **Yes — edited by the update-top-picks skill** |
| `products-extra.json` | New products, or field overrides for existing ids (same id = update in place) | **Yes** |

## slots.json

```json
{
  "cleanse": {"current": "klued", "intl": "cerave", "kr": "cosrx", "jp": "senka",
              "ph_budget": "quickfx", "intl_budget": "simple", "kr_budget": "somebymi", "jp_budget": "hadalabo_dc"},
  "serum":   {...}, "moist": {...}, "sun": {...}, "daylip": {...}, "lip": {...}
}
```
Steps: `cleanse`, `serum`, `moist`, `sun` (wake-up and before-sleep share the first three), `daylip` (wake-up step 5), `lip` (before-sleep step 4).
Slots render in this fixed order: current, intl, kr, jp, then the "Budget picks" divider with ph_budget, intl_budget, kr_budget, jp_budget.
A slot may be `null`. The card label ("Your current product", "Korean alternative", …) comes from the slot; the origin filter on All products comes from the product's `region`.
Products that are in no slot and not a Top pick are kept in the data but not shown. The All products count is computed from what is shown.

## top-picks.json

```json
{
  "updated": "11–12 September 2026",          // shown as "Evidence (…)" and inside the methods box
  "updated_tl": "11–12 Setyembre 2026",
  "picks": [
    {
      "cat": "cleanser",                       // cleanser | serum | moisturizer | sunscreen | lipday | lipnight (exactly these six, in this order)
      "pick": "quickfx",                       // product id (must exist in the data files or products-extra.json)
      "runner": "cosrx",                       // product id
      "why":      {"en": "...", "tl": "..."},  // why this one over the others (2–4 sentences)
      "rwhy":     {"en": "...", "tl": "..."},  // one clause about the runner-up, lower-case start, no trailing period
      "evidence": {"en": "...", "tl": "..."}   // the facts: review counts, dates checked, rankings, prices; disclose if the most-reviewed product is NOT the pick
    }
  ]
}
```

## products-extra.json (list; one object per new product)

```json
{
  "id": "brand_product",                       // lower-case, letters/digits/underscore, unique
  "brand": "Brand (Parent)",                   // display brand; text in parentheses is dropped on the drawn label
  "name": "Full product name",
  "region": "ph | intl | kr | jp",             // Filipino / International / Korean / Japanese
  "category": "cleanser | serum | moisturizer | sunscreen | lip",
  "shape": "tube | dropper | jar | stick",     // drawn-label silhouette
  "img": "https://…-zoom.jpg",                 // VERIFIED retailer product photo (see skill prompt); null only if truly none exists
  "img_alt": null,                             // optional second candidate URL
  "where":   {"en": "...", "tl": "..."},
  "actives": {"en": ["..."], "tl": ["..."]},
  "why":     {"en": "...", "tl": "..."},
  "flag":    {"en": "...", "tl": "..."},
  "variants": [["150 ml", "₱329", 329, "about 2½ months", "mga 2½ buwan"]]   // [size, price text, numeric price for sorting, lasts EN, lasts TL]; first row = main size
}
```

Existing product ids: klued, cerave, cosrx, senka, quickfx, simple, somebymi, hadalabo_dc, dermorepubliq, ordinary, anua, melanocc,
garnier_serum, skin1004_amp, hadalabo_pwl, camou, neutrogena, skin1004, hadalabo, garnier_gel, nr_aloe, naturie, hikari, lrp, boj,
biore, garnier_uv, nr_sun, skinaqua, vaseline, mediheal, dhc, lipice, luxe_lipscreen.

## Skills

- `.claude/skills/update-top-picks/` — **built.** Re-researches the Top picks page (`top-picks.json`, plus `products-extra.json` when a pick is new). Say “update top picks”. Its `check.py` verifies a run.
- `.claude/skills/update-current-products/` — **built.** Replaces the product I use in a step (`slots.json` → `current`, plus `products-extra.json`) and re-reads the six current products together. Say “I switched my cleanser to …”. Its `check.py --snapshot` records the baseline before the run; `check.py` verifies it and prints the stack scan.
- `.claude/skills/update-alternatives/` — **built.** Re-researches the alternative slots per origin and price band (`slots.json`, plus `products-extra.json` when a slot's winner is new). Say “update alternatives”. Its `check.py --snapshot` records the baseline before the run; `check.py` verifies it.

Each skill ends by publishing to the live site with `publish.sh` (see Publishing).

## Checks after a rebuild

- `node --check` on the inline script (or open the page: the console must stay empty).
- Every product must have `data-remote` (a photo URL): `grep -c 'data-remote=' index.html` should be > 0 and no card should show a drawn label unless documented.
- English and Tagalog blocks must stay in step: `grep -c 'class="l-en"'` equals `grep -c 'class="l-tl"'`.

`python3 .claude/skills/update-top-picks/check.py` runs all of these, plus the Top picks content checks.

## Publishing

Live site: https://heyitsiveen.github.io/personal-care/ (GitHub Pages, repo `heyitsiveen/personal-care`). `.github/workflows/deploy.yml` publishes `index.html` + `images/` on every push to `main`.

    bash site-builder/publish.sh "type(scope): summary" ["body"]

commits the site files (`index.html`, `images/`, `site-builder/`, `get-photos.*`), pushes, waits for the deploy run and confirms the live page is byte-identical to `index.html`; the last line reads `OK: live site updated`. Every skill ends its run with it. Other changed files are listed and left uncommitted.

Local only (`.gitignore`): downloaded photos (`images/*.jpg`), `images/photos.js`, and the skills' `.slots-before.json` baselines. The deploy writes an empty `photos.js`, so the live page loads the retailer photos.
