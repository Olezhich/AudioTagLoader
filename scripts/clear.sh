#!/bin/bash

DIR="$1"

rm "$DIR/tags.txt"
rm "$DIR/thumb.jpg"
mv "$DIR/cover.jpg" "$DIR/Folder.jpg"