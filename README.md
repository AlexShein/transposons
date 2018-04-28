# Transposones
Bioinformatics project
## Description:
DiPropreties.csv - csv with physical dinucleotides properties
DiPropretiesT.csv - the same file
### process_line.py
Logic of .pal file's line processing - creates dict with each position dinucleotide's properties and some statistics.
```bash
cat temp | python3 process_line.py -output_file 123.csv -target 1
```
### parallel_processing_v2.py
This is a script that processes all .pal files located at provided path and places results into csv file. First version is deprecated
-t_path for target files path and -nt_path for non-target ones.
```bash
python3 parallel_processing_v2.py -output_file output.csv \
-path /home/dariag/RepBase_embl/ALL_LINE2/res_S15-30_L0-10_M5 \
-n 1000
```
### params_optimization.py
Prints optimal params for RandomForestClassifier
```bash
python3 params_optimization.py -dataset ./ml_dataset.csv
```
### evaluate_model.py
Print share of classifier's hits
```bash
python3 evaluate_model.py -dataset ./ml_dataset.csv
```
### get_random_lines.sh
Extracts totally n random lines and writes them into a file
```bash
./get_random_lines.sh /home/shared/STEMLOOPS/hg19/S15-30_L0-10_M5/ 2200 S15-30_L0-10_M5_rand_non-target_hg19_2200.pal
```
