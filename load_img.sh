#!/bin/bash

set -euo pipefail

DIR="$1"
IFS=$'\t' read -ra f

curl -so "$DIR/thumb.jpg" "${f[6]}"
curl -so "$DIR/cover_tmp.jpg" "${f[7]}"

s=${f[9]}; t=${f[10]}; m=$s; (( t < s )) && m=$t

convert "$DIR/cover_tmp.jpg" -gravity center -crop ${m}x${m}+0+0 +repage "$DIR/cover.jpg" 2>/dev/null

rm "$DIR/cover_tmp.jpg"



printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "${f[@]:0:6}" "$DIR/thumb.jpg" "$DIR/cover.jpg"

while IFS=$'\t' read -r -a f; do
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "${f[@]:0:6}" "$DIR/thumb.jpg" "$DIR/cover.jpg"
done