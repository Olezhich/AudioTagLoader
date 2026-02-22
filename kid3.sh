#!/bin/bash

set -euo pipefail

DIR="$(dirname "$1")"

dsf=()
while IFS= read -r -d '' file; do
    dsf+=("$file")
done < <(find "$DIR" -maxdepth 1 -iname "*.dsf" -type f -print0 | sort -z)

i=0
while IFS=$'\t' read -r year artist album genre style track title thumb cover; do
    echo "[${i}] ${dsf[$i]}"

    kid3-cli -c "select \"${dsf[$i]}\"" \
             -c "remove 2" \
             -c "set artist \"$artist\"" \
             -c "set album \"$album\"" \
             -c "set title \"$title\"" \
             -c "set track \"$track\"" \
             -c "set year \"$year\"" \
             -c "set genre \"$genre\"" \
             -c "set image \"$cover\"" \
             -c "save" 2>/dev/null
    ((i++))
done < "$1"