#!/bin/bash

cmd="$1"; shift

DESTINATION="$(pwd)"

PROJECT="$(cd "$(dirname "$0")" && pwd)"



case "$cmd" in
    fba) 
        cd $PROJECT
        poetry run python main.py fba "$1" "$DESTINATION" ;;
    set) 
        cd $PROJECT
        cat "$DESTINATION/tags.txt" | load_img.sh "$DESTINATION" > "$DESTINATION/tags.tmp" && mv "$DESTINATION/tags.tmp" "$DESTINATION/tags.txt"  
        kid3.sh "$DESTINATION/tags.txt" 
        clear.sh "$DESTINATION"
        ;;
esac