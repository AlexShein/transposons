#!/bin/bash

# SEQ_PATH=data/L1/data/50_last/
# RESULT_PATH=data/L1/data/shuffled_50_last/
COUNTER=0

# First arg: target path
# Second arg: result path
# Third arg: prefix for files
# Example: src/shell_scripts/shuffle_sequences.sh data/L1/data/50_last/ data/L1/data/shuffled_50_last/ 1_

LEN=$(ls $1 | wc -l)

for filename in $(ls $1); do
    # SEQ=$(tail -n1 $1$filename | fold -w1 | shuf | tr -d '\n')
    SEQ=$(tail -n1 $1$filename | tr -d '\n' | $(dirname $0)/../py_scripts/altschulEriksonDinuclShuffle.py)
    echo $SEQ > "$2$3$filename"
    COUNTER=$[COUNTER + 1]
    if (($(($COUNTER%100)) == 0))
    then
        echo -ne "\r#Processing $COUNTER out of $LEN"
    fi
done;
echo -ne "\r#Done, processed $COUNTER files\n"