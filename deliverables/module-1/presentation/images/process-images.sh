#!/bin/zsh
setopt nullglob

echo "Making flowchart"

dot -Tsvg flowchart.dot -o flowchart.svg

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

