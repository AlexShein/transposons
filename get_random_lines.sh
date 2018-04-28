#!/bin/bash
# First arg: path
# Second arg: int
# Third arg: filename
for filename in $(ls $1*.pal); do
    shuf -n $2 $filename >> $3
done
