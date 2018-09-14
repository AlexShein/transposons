#!/bin/bash
# First arg: path
# Second arg: path
for filename in $(ls $1*.fa); do
    POLY_A_END=$(tail -n1 $filename | rev | grep -aob '[CTG]\{2,\}' | head -n1 | grep -oE '[0-9]+')
    # Cut the sequence to the position of last non-A bases pair
    SEQ=$(tail -n1 $filename)
    echo $SEQ | cut -c1-$((${#SEQ}-$POLY_A_END)) >> "$2$filename"
done;
