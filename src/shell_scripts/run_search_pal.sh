#!/bin/bash

# First arg: target path

COUNTER=0
LEN=$(ls $1 | wc -l)
for filename in $(ls $1 | shuf | head -n$LEN); do
    /home/xelmar/Work/6_year/transp/src/cpp/search $1$filename 123.ptt 10 20 0 8 5
    COUNTER=$[COUNTER + 1]
    if (($(($COUNTER%100)) == 0))
    then
        echo -ne "\r#Processing $COUNTER out of $LEN"
    fi
done;
echo -ne "\r#Done, processed $COUNTER files\n"