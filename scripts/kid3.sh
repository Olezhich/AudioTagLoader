#!/bin/bash

set -euo pipefail

DIR="$(dirname "$1")"

dsf=()
while IFS= read -r -d '' file; do
    dsf+=("$file")
done < <(find "$DIR" -maxdepth 1 \( -iname "*.dsf" -o -iname "*.flac" \) -type f -print0 | sort -z) 

i=0
while IFS=$'\t' read -r year artist album genre track title thumb cover; do
    echo "[${i}] ${dsf[$i]}"
    kid3-cli -c "select \"${dsf[$i]}\"" \
             -c "remove 2" \
             -c "set artist \"$artist\"" \
             -c "set album \"$album\"" \
             -c "set title \"$title\"" \
             -c "set track \"$track\"" \
             -c "set date \"$year\"" \
             -c "set genre \"$genre\"" \
             -c "set picture:'$cover' ''" \
             -c "save"
    ((i++))  || true
done < "$1"