#!/bin/bash
# Downloads the real product photos into ./images so index.html shows them offline.
# Run:  bash get-photos.sh   (or double-click get-photos.command; if macOS blocks it, right-click > Open)
cd "$(dirname "$0")" || exit 1
mkdir -p images
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
ok=0; fail=0; saved=()
get(){ local id="$1"; shift
  for u in "$@"; do
    if curl -fsSL --retry 2 --max-time 40 -A "$UA" -e "https://www.watsons.com.ph/" -o "images/$id.jpg" "$u"; then
      echo "  saved  images/$id.jpg"; ok=$((ok+1)); saved+=("$id"); return; fi
  done
  rm -f "images/$id.jpg"; echo "  FAILED $id (the page loads it from the retailer when online)"; fail=$((fail+1)); }
echo "Fetching 34 product photos..."
get klued "https://storage.skinsort.com/owajo7akkfj64y1bhb5fcxry36vv"
get cerave "https://medias.watsons.com.ph/publishing/50053257-v75cguLk-zoom.png?version=1762914671"
get cosrx "https://medias.watsons.com.ph/publishing/COSRX_Image1_50044422-eHzI0fRd-zoom.jpg?version=1785153905"
get senka "https://medias.watsons.com.ph/publishing/SENKA_IMAGE%201_50010099-w24fwJFL-zoom.jpg?version=1763367090"
get quickfx "https://medias.watsons.com.ph/publishing/WTCPH-50046791-front-zoom.jpg?version=1734328302"
get simple "https://medias.watsons.com.sg/publishing/WTCSG-40033-front-zoom.jpg?version=1729492191" "https://medias.watsons.com.ph/publishing/WTCPH-50052710-front-zoom.jpg?version=1756223458"
get somebymi "https://medias.watsons.com.ph/publishing/SOME%20BY%20MI_Image%201_50053132-33HThwGl-zoom.jpg?version=1764235822"
get hadalabo_dc "https://medias.watsons.com.ph/publishing/50007565-egdZcSAY-zoom.png?version=1762937335"
get dermorepubliq "https://medias.watsons.com.ph/publishing/WTCPH-50058805-front-zoom.jpg?version=1776455434"
get ordinary "https://medias.watsons.com.ph/publishing/50033473-Ewl4IU27-zoom.jpg?version=1761814703"
get anua "https://medias.watsons.com.ph/publishing/WTCPH-50058923-back-zoom.jpg?version=1785257474"
get melanocc "https://medias.watsons.com.ph/publishing/Melano%20CC_Image%201_50059679-uW4ABLPJ-zoom.jpg?version=1782691945"
get garnier_serum "https://medias.watsons.com.my/publishing/WTCMY-54345-front-zoom.jpg?version=1753310447"
get skin1004_amp "https://medias.watsons.com.ph/publishing/SKIN1004_Image1_50054241-goEY7M7n-zoom.jpg?version=1785201440"
get hadalabo_pwl "https://medias.watsons.com.ph/publishing/Hada%20Labo_Image%201_50030827-NoMhBeWA-zoom.jpg?version=1764124578"
get camou "https://storage.skinsort.com/y2cnx74ctauafp39f1rgsu1m7fu0"
get neutrogena "https://medias.watsons.com.ph/publishing/WTCPH-10087897-front-zoom.jpg?version=1734062328"
get skin1004 "https://medias.watsons.com.ph/publishing/SKIN1004_Image1_50054236-n5fUhiFS-zoom.jpg?version=1765450794"
get hadalabo "https://medias.watsons.com.ph/publishing/Hada%20Labo_Image%201_50043925-d3XcCuTB-zoom.jpg?version=1764128094"
get garnier_gel "https://medias.watsons.com.sg/publishing/WTCSG-61523-front-zoom.jpg?version=1729534394" "https://medias.watsons.com.ph/publishing/Garnier_50048143_NumberSequence_Front_Left-JNxnYIPe-zoom.jpg?version=1762590394"
get nr_aloe "https://peachesandcremeshop.com/cdn/shop/files/NATURE-REPUBLIC-02-01.jpg?v=1713470002&width=1800"
get naturie "https://medias.watsons.com.ph/publishing/Naturie_Image1_Watsons_50053309-CHZEv5Vn-zoom.jpg?version=1766132840"
get hikari "https://storage.skinsort.com/fpntt11o41fy2195bdtyedc7j7l9"
get lrp "https://www.laroche-posay.sg/-/media/project/loreal/brand-sites/lrp/apac/sg/products/anthelios/anthelios-uvmune-oil-control-gel-cream-spf50-plus-non-perfumed/lrp-anthelios-uvmune-400-oil-gel-cream-sp-bottle-packshot-front.png"
get boj "https://medias.watsons.com.ph/publishing/WTCPH-50042242-front-zoom.jpg" "https://medias.watsons.com.ph/publishing/WTCPH-50042242-front-prod.jpg"
get biore "https://medias.watsons.com.ph/publishing/WTCPH-50055676-front-zoom.jpg?version=1758790208"
get garnier_uv "https://medias.watsons.com.ph/publishing/50046793_01-gziPjMgB-zoom.jpg?version=1786174892"
get nr_sun "https://cdn.shopify.com/s/files/1/0682/3647/6589/files/NATURE_REPUBLIC_California_Aloe_Daily_Sun_Block_SPF50_PA_57ml_2EA.jpg?v=1761638351"
get skinaqua "https://medias.watsons.com.ph/publishing/WTCPH-50026772-front-zoom.jpg?version=1734141918"
get vaseline "https://medias.watsons.com.ph/publishing/Vaseline_Image1_50025757-9EPre93h-zoom.jpg?version=1765777079"
get mediheal "https://medias.watsons.com.ph/publishing/Mediheal_Image1_50056954-Le2gCIxv-zoom.png?version=1768214606"
get dhc "https://www.wownippon.com/cdn/shop/files/dhc-hydrating-lip-cream-1-5g-japanese-lip-balm.jpg?v=1786951718"
get luxe_lipscreen "https://medias.watsons.com.ph/publishing/WTCPH-50047764-front-zoom.jpg?version=1734346545"
get lipice "https://medias.watsons.com.ph/publishing/WTCPH-50042100-front-zoom.jpg"
json="{"; sep=""
for f in images/*.jpg; do [ -e "$f" ] || continue; id="$(basename "$f" .jpg)"; json="$json$sep\"$id\":\"$id.jpg\""; sep=","; done
json="$json}"
printf '// Written by get-photos.sh: lists the product photos that were downloaded into this folder.\nwindow.PHOTOS=%s;\n' "$json" > images/photos.js
echo "Done: $ok photos saved, $fail failed. images/photos.js updated."
echo "Now open index.html in your browser."
