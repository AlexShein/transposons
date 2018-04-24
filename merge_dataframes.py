# Developed by AlexShein 04.2018
import argparse
import logging

import pandas as pd

log = logging.getLogger('parallel_processing_v2.py')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def merge_dataframes(files):
    dataframes = []
    for filename in files.split(','):
        dataframes.append(pd.read_csv(filename, sep=';'))
    return pd.concat(dataframes)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Process *.pal files to store statistics.',
        usage='python3 parallel_processing_v2.py -output_file 123456.csv -path ./temp_pal',
    )
    parser.add_argument(
        '-output_file',
        dest='output_file',
        help='Name of file to store results',
        required=True,
    )
    parser.add_argument(
        '-files',
        dest='files',
        help='Name of files to merge, comma separeted',
        required=True,
    )
    args = parser.parse_args()
    log.info("Starting merge")

    result_df = merge_dataframes(
        args.files,
    )
    if result_df is not None:
        log.info("Writing to file")
        result_df.to_csv(args.output_file, sep=';')
        log.info("Done")
