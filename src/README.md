## py_scripts/
This folder contains sequence dinucleotide features annotation logic.
The most important files are:
### process_pals.py
Entrypoint of annotation logic. Retrieves lines from .pal (palindrome annotation) files and parallels processing of each one.
### process_line.py
Main dinucleotide features annotation logic file.
### altschulEriksonDinuclShuffle.py
Dinucleotide shuffling algorithm originally published by Altschul and Erickson
### DiProperties.csv
Dinucleotide props table from DiProDB

## shell_scripts/
Several bash utilities to make our lives easier.
There are scripts for extracting random lines from files, for cutting poly-A tails, for running sequnces dinucleotide shuffling, etc.