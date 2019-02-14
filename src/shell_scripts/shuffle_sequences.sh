#!/bin/bash

# SEQ_PATH=data/L1/data/50_last/
# RESULT_PATH=data/L1/data/shuffled_50_last/
COUNTER=0

# First arg: target path
# Second arg: result path
# Third arg: prefix for files

LEN=$(ls $1 | wc -l)

for filename in $(ls $1); do
    SEQ=$(tail -n1 $1$filename | fold -w1 | shuf | tr -d '\n')
    echo $SEQ >> "$2$3$filename"
    COUNTER=$[COUNTER + 1]
    if (($(($COUNTER%100)) == 0))
    then
        echo -ne "\r#Processing $COUNTER out of $LEN"
    fi
done;
echo -ne "\r#Done, processed $COUNTER files\n"