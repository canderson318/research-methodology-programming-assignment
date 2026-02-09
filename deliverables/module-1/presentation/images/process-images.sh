#!/bin/zsh
setopt nullglob

echo "Making flowchart"

for f in *.dot; do
  echo "flowing $f"
  dot -Tsvg $f -o "${f%.dot}.svg" 
done

for f in *.pdf; do
  [[ $f == crpd-* ]] && continue
  echo "cropping $f" 
  pdfcrop "$f" "crpd-$f"
done

for f in *.png *.jpg *.jpeg; do
  [[ $f == crpd-* ]] && continue
  echo "trimming $f"
  magick "$f" -fuzz 2% -trim +repage "crpd-$f" 
done

