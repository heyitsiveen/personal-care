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
echo "Fetching 39 product photos..."
get klued "https://storage.skinsort.com/owajo7akkfj64y1bhb5fcxry36vv"
get cetaphil_gfc "https://medias.watsons.com.ph/publishing/Watson%20BAU%20PDP-GFC-236ml-2-3nCAd9Gh-zoom.png?version=1776840986" "https://medias.watsons.com.ph/publishing/Watson%20BAU%20PDP-GFC-236ml-3-L8xNfwhg-zoom.png?version=1776840993"
get facerep_acne "https://medias.watsons.com.ph/publishing/Face%20Republic_Image%201_50034124-F2tQNxaM-zoom.png?version=1763529894" "https://medias.watsons.com.ph/publishing/Face%20Republic_Image%205_50034124-xdEuHq0h-zoom.png?version=1763529901"
get senka "https://medias.watsons.com.ph/publishing/SENKA_IMAGE%201_50010099-w24fwJFL-zoom.jpg?version=1763367090"
get quickfx "https://medias.watsons.com.ph/publishing/WTCPH-50046791-front-zoom.jpg?version=1734328302"
get simple "https://medias.watsons.com.sg/publishing/WTCSG-40033-front-zoom.jpg?version=1729492191" "https://medias.watsons.com.ph/publishing/WTCPH-50052710-front-zoom.jpg?version=1756223458"
get somebymi "https://medias.watsons.com.ph/publishing/SOME%20BY%20MI_Image%201_50053132-33HThwGl-zoom.jpg?version=1764235822"
get hadalabo_dc "https://medias.watsons.com.ph/publishing/50007565-egdZcSAY-zoom.png?version=1762937335"
get dermorepubliq "https://medias.watsons.com.ph/publishing/WTCPH-50058805-front-zoom.jpg?version=1776455434"
get ponds_niasorcinol "https://medias.watsons.com.ph/publishing/WTCPH-50033142-front-zoom.jpg?version=1734332335" "https://medias.watsons.com.ph/publishing/WTCPH-50033142-side-zoom.jpg?version=1721949495"
get skin1004_amp "https://medias.watsons.com.ph/publishing/SKIN1004_Image1_50054241-goEY7M7n-zoom.jpg?version=1785201440"
get hadalabo_hl "https://medias.watsons.com.ph/publishing/Hada%20Labo_Image%201_50007564-hW8ysUSM-zoom.jpg?version=1764137721" "https://medias.watsons.com.ph/publishing/50007563_Hada%20Labo%20Hydrating%20Lotion%20Rich%2030ml-pU7xsXAz-zoom.png?version=1754011009"
get luxe_nia10 "https://medias.watsons.com.ph/publishing/50028463_LOWhiteningRepairSerum_%20%20%281%29-ZnDNkmbR-zoom.jpg?version=1772588713" "https://medias.watsons.com.ph/publishing/50028463_LOWhiteningRepairSerum_%20%20%283%29-8OWNAarE-zoom.jpg?version=1772588629"
get garnier_serum "https://medias.watsons.com.ph/publishing/50039335_01_OP-m2WfhZUo-zoom.png?version=1789444090" "https://medias.watsons.com.my/publishing/WTCMY-54345-front-zoom.jpg?version=1753310447"
get hadalabo_pwl "https://medias.watsons.com.ph/publishing/Hada%20Labo_Image%201_50030827-NoMhBeWA-zoom.jpg?version=1764124578"
get camou "https://storage.skinsort.com/y2cnx74ctauafp39f1rgsu1m7fu0"
get neutrogena "https://medias.watsons.com.ph/publishing/WTCPH-10087897-front-zoom.jpg?version=1734062328"
get skin1004 "https://medias.watsons.com.ph/publishing/SKIN1004_Image1_50054236-n5fUhiFS-zoom.jpg?version=1765450794"
get hadalabo "https://medias.watsons.com.ph/publishing/Hada%20Labo_Image%201_50043925-d3XcCuTB-zoom.jpg?version=1764128094"
get celeteque_moist "https://medias.watsons.com.ph/publishing/WTCPH-10081411-front-zoom.jpg?version=1733995085" "https://medias.watsons.com.ph/publishing/WTCPH-10081410-front-zoom.jpg?version=1733994861"
get ponds_hydra "https://medias.watsons.com.ph/publishing/WTCPH-50054015-front-zoom.jpg?version=1750265451" "https://medias.watsons.com.ph/publishing/WTCPH-50054015-side-zoom.jpg?version=1750265456"
get facerep_cica "https://medias.watsons.com.ph/publishing/Face%20Republic_Image1_50014273-yHpaycgW-zoom.png?version=1764754978" "https://medias.watsons.com.ph/publishing/Face%20Republic_Image2_50014273-AT2r6GLD-zoom.png?version=1764754964"
get naturie "https://medias.watsons.com.ph/publishing/Naturie_Image1_Watsons_50053309-CHZEv5Vn-zoom.jpg?version=1766132840"
get hikari "https://storage.skinsort.com/fpntt11o41fy2195bdtyedc7j7l9"
get lrp "https://www.laroche-posay.sg/-/media/project/loreal/brand-sites/lrp/apac/sg/products/anthelios/anthelios-uvmune-oil-control-gel-cream-spf50-plus-non-perfumed/lrp-anthelios-uvmune-400-oil-gel-cream-sp-bottle-packshot-front.png"
get boj "https://medias.watsons.com.ph/publishing/WTCPH-50042242-front-zoom.jpg" "https://medias.watsons.com.ph/publishing/WTCPH-50042242-front-prod.jpg"
get biore "https://medias.watsons.com.ph/publishing/WTCPH-50055676-front-zoom.jpg?version=1758790208"
get luxe_zeroshine "https://medias.watsons.com.ph/publishing/50046323_SPF100-qtgatqgJ-zoom.jpg?version=1741828825" "https://medias.watsons.com.ph/publishing/50046323_front-qtgatqgJ-zoom.jpg?version=1741828819"
get garnier_uv "https://medias.watsons.com.ph/publishing/50046793_01-gziPjMgB-zoom.jpg?version=1786174892"
get facerep_sungel "https://medias.watsons.com.ph/publishing/WTCPH-50021005-front-zoom.jpg?version=1734131231" "https://medias.watsons.com.ph/publishing/WTCPH-50021005-side-zoom.jpg?version=1721925829"
get skinaqua "https://medias.watsons.com.ph/publishing/WTCPH-50026772-front-zoom.jpg?version=1734141918"
get nivea_medrepair "https://medias.watsons.com.ph/publishing/10037672-4EIV1WN1-zoom.JPG?version=1763175280" "https://medias.watsons.com.ph/publishing/WTCPH-10037672-side-zoom.jpg?version=1721932313"
get luxe_lipscreen "https://medias.watsons.com.ph/publishing/WTCPH-50047764-front-zoom.jpg?version=1734346545"
get carmex_spf "https://medias.watsons.com.ph/publishing/WTCPH-10099919-front-zoom.jpg?version=1734046588" "https://medias.watsons.com.ph/publishing/WTCPH-10099919-side-zoom.jpg?version=1720803857"
get vaseline "https://medias.watsons.com.ph/publishing/Vaseline_Image1_50025757-9EPre93h-zoom.jpg?version=1765777079"
get drjart_lip "https://medias.watsons.com.ph/publishing/drjart_50052655_01-mUgLoNGJ-zoom.png?version=1764215079" "https://medias.watsons.com.ph/publishing/drjart_50052655_02-bfx4Yw0g-zoom.png?version=1764215072"
get nivea_lip "https://medias.watsons.com.ph/publishing/10026702-5D20c0JI-zoom.JPG?version=1763175290" "https://medias.watsons.com.ph/publishing/WTCPH-10026702-side-zoom.jpg?version=1721932289"
get mediheal "https://medias.watsons.com.ph/publishing/Mediheal_Image1_50056954-Le2gCIxv-zoom.png?version=1768214606"
get beachhut_lip "https://medias.watsons.com.ph/publishing/Beach%20Hut_Image1_50046460-MQYXsMuB-zoom.png?version=1762571547" "https://medias.watsons.com.ph/publishing/Beach%20Hut_Image3_50046460-srevf1tE-zoom.png?version=1762571553"
json="{"; sep=""
for f in images/*.jpg; do [ -e "$f" ] || continue; id="$(basename "$f" .jpg)"; json="$json$sep\"$id\":\"$id.jpg\""; sep=","; done
json="$json}"
printf '// Written by get-photos.sh: lists the product photos that were downloaded into this folder.\nwindow.PHOTOS=%s;\n' "$json" > images/photos.js
echo "Done: $ok photos saved, $fail failed. images/photos.js updated."
echo "Now open index.html in your browser."
