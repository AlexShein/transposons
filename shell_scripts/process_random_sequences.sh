#!/bin/bash
# First arg: int - amount of files to process
COUNTER=1
LEN=$(ls $TPATH | wc -l)
TPATH=/home/shared/L1-Alu/shuffle/fasta/
for filename in $(ls $TPATH | shuf); do
    tail -n1 $TPATH$filename >> /home/alexshein/last_n_bps/random_nt_seq.txt
    COUNTER=$[COUNTER + 1]
    if (($(($COUNTER%100)) == 0))
    then
        echo -ne "\r#Processing $COUNTER out of $LEN"
    fi
    if [[ COUNTER -eq $1 ]]
    then
        break
    fi
done;
echo -ne "\r#Done, processed $COUNTER files\n"