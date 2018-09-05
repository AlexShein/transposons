#!/bin/bash
# First arg: path
# Second arg: filename
# Third arg: int
# Example: shell_scripts/cut_last_50_bp.sh $(pwd) ./test.txt 50
echo "Writing to "$2
LEN=$(ls $1/*.fa|wc -l)
COUNTER=1
for filename in $(ls $1/*.fa); do
    POLY_A_END=$(tail -n1 $filename | rev | grep -aob '[CTG]'| head -n1 | grep -oE '[0-9]+')
    # Cut the sequence to the position of first non-A base from end
    SEQ=$(tail -c $(($3+$POLY_A_END)) $filename)
    echo $SEQ | cut -c1-$((${#SEQ}-$POLY_A_END)) >> "$2"
    if (($(($COUNTER%200)) == 0))
    then
        echo -ne "\rProcessing $COUNTER out of $LEN"
    fi
    COUNTER=$[COUNTER + 1]
done
echo -ne "\rDone, processed $LEN files\n"
