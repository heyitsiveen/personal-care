PERSONAL CARE  (English + Tagalog in one page)  -  researched 11 September 2026

Open:  index.html
  - Top bar: switch between "Routine", "Top picks" (one recommended product per step, with runner-ups)
    and "All products", and between English and Tagalog.
  - All products (33): filter by type, brand origin (Filipino / International / Korean / Japanese) and budget
    (₱500 and under); sort by price low-to-high or high-to-low; click any photo to view full size (click again to zoom).
  - Every product card lists each size with its price and roughly how long that size lasts.

Live:  https://heyitsiveen.github.io/personal-care/   (GitHub repo: heyitsiveen/personal-care)
  - The three skills publish by themselves at the end of a run. After editing by hand and rebuilding:
      bash site-builder/publish.sh "type(scope): summary"
    It commits the site files, pushes, waits for the deploy and confirms the live page matches index.html.
  - Downloaded photos (images/*.jpg) stay on this computer; the live page loads the retailer photos.

Images:
  images/*.svg   drawn product labels (brand, full name, size) - always display, even offline.
  images/*.jpg   real product photos - not included yet; run the script below to download them
                 (34 of 33 products have a retailer photo URL; these 0 have none and always show a drawn label:
                 ).

To add the real photos (about 1-2 MB total, from Watsons PH, La Roche-Posay, DHC/WowNippon and SkinSort):
  1. Open Terminal in this folder
  2. Run:   bash get-photos.sh
  (or double-click get-photos.command; if macOS blocks it, right-click > Open)
While online, the page also loads photos straight from the retailer sites without the script.

Maintaining the page:
  site-builder/          the generator; run  python3 site-builder/build_site.py  from this folder to rebuild
  site-builder/top-picks.json       content of the Top picks page (edit, then rebuild)
  site-builder/products-extra.json  add new products here (schema in site-builder/README.md)
  site-builder/slots.json           which product sits in which slot of each routine step (fixed structure)
  .claude/skills/update-top-picks/          built skill - say "update top picks" in Claude to re-research the Top picks page
  update-top-picks-skill-prompt.md          prompt to create a Claude skill that re-researches the Top picks page (already built)
  update-current-products-skill-prompt.md   prompt to create a skill that swaps in a product you now use
  update-alternatives-skill-prompt.md       prompt to create a skill that refreshes the alternative slots (per origin, any price and ₱500-and-under)
