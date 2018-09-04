#!/bin/bash
# First arg: path
# Second arg: filename
# Third arg: int
# Example: shell_scripts/cut_last_50_bp.sh $(pwd) ./test.txt 50
echo "Writing to "$2
LEN=$(ls $1*.fa|wc -l)
COUNTER=1
for filename in $(ls $1/*.fa); do
    tail -n50 $filename >> "$2"
    echo '' >> "$2"
    echo "Processing $COUNTER out of $LEN"
    COUNTER=$[COUNTER + 1]
done
