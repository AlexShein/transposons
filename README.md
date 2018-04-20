## Transposones
Bioinformatics project
# Description:
DiPropreties.csv - csv with physical dinucleotides properties
DiPropretiesT.csv - the same file
process_line.py - logic of .pal file's line processing - creates dict with each position dinucleotide's properties and some statistics.
```bash
cat temp | python3 process_line.py -output_file 123.csv -target 1
```
parallel_processing.py - this is a script that processes all .pal files located at provided path and places results into csv file.
```bash
python3 parallel_processing.py -path /home/dariag/RepBase_embl/ALL_LINE2/res_S15-30_L0-10_M5 -output_file test.csv
```
