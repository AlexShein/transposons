#!/bin/bash
# First arg: path
# Second arg: int
# Third arg: filename
COUNTER=1
LEN=$(ls $1*.pal|wc -l)
N_LINES=$(($2/$LEN+1))
echo 'Extracting '$N_LINES' from each file'
for filename in $(ls $1*.pal); do
    shuf -n $N_LINES $filename >> $3
    echo 'Processing '$COUNTER' out of '$LEN
    COUNTER=$[COUNTER + 1]
done
