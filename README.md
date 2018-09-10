# Transposones
A bioinformatics project related to transposons recognition
# Description:
##Folders:
###sequences
Contains raw sequences of both Alu and L1 + some random (no-transposon) pieces of genome
###ipython
Contains experiment notebooks
##Files:
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
### merge_dataframes.py
Merges .csv files into a single one
```bash
python3 ./merge_dataframes.py -output_file merged.csv -files 12345.csv,123456.csv
```
### File shuffling
```bash
head -n1 ../processed_28_04/merged_S15-30_L0-10_M5_4400.csv >> ../processed_28_04/merged_S15-30_L0-10_M5_4400_shuffled.csv
tail -n4320 ../processed_28_04/merged_S15-30_L0-10_M5_4400.csv | shuf >> ../processed_28_04/merged_S15-30_L0-10_M5_4400_shuffled.csv
```
### Cutting last n bases of sequence
Use `clean` argument to cut off poly-a tail
```bash
transposones/shell_scripts/cut_last_n_bases.sh /home/shared/L1-Alu/Alu/AluS/fasta ~/last_n_bps/AluS_50_bps_test.txt 50 clean
```