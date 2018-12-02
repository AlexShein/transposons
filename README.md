# Transposons
A bioinformatics project related to Alu and L1 transposons stem-loop structures recognition
# Description:
## Folders:
### src
Contains source code of annotation logic
### ipython
Contains experiment notebooks
ipython/Experiments_summary.ipynb - summary over ROC AUC, Precision-Recall and Feature Importances.
## Useful utils Files:
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
