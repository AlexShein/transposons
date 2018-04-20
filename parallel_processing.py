# Developed by AlexShein 04.2018
from datetime import datetime as dt
from functools import reduce
from multiprocessing import cpu_count, Pool
from operator import add
from process_line import process_lines
from random import randint
import argparse
import logging
import os
import pandas as pd

STREAMS = cpu_count()

log = logging.getLogger('parallel_processing.py')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_chunks(lst, chunk_size):
    m = 0
    for i in range(0, len(lst), chunk_size):
        m += chunk_size
        yield lst[i:m]


def get_last_line(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return lines[-1]


def get_lines(filename):
    """
    returns tuple of pairs like (line, 0/1), where 0/1 shows whether this sequence is target one or not
    Target one is in last line of file
    Non-target one is a random line of file
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
        return ((lines[-1], 1), (lines[randint(0, len(lines) - 1)], 0))


def begin_processing(path, output_file):
    start = dt.utcnow()
    results = []
    files = [os.path.join(path, filename) for filename in os.listdir(path) if filename[-4:] == '.pal']
    log.info("Got {0} files".format(len(files)))
    chunk_size = len(files) // STREAMS + 1
    log.info("Processing with chunk_size = {0}. Starting {1} workers".format(chunk_size, STREAMS))
    with Pool(processes=STREAMS) as pool:
        processed_data = pool.map(
            process_lines, get_chunks(reduce(add, map(get_lines, files)), chunk_size)
        )
    log.info("Combining results into single dict")
    for chunk in processed_data:
        results += chunk
    log.info("Creating df and writing to csv")
    result_df = pd.DataFrame(results)
    result_df.to_csv(output_file, sep=';')
    end = dt.utcnow()
    log.info("Done! Execution time {0}".format(
        str((end - start).seconds) + '.' + str((end - start).microseconds),
    ))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Process *.pal files to store statistics.',
        usage='python3 parallel_processing.py -output_file 12345.csv -path ./',
    )
    parser.add_argument(
        '-output_file',
        dest='output_file',
        help='Name of file to store results',
        required=True,
    )
    parser.add_argument(
        '-path',
        dest='path',
        help='Location of .pal files',
        required=True,
    )
    args = parser.parse_args()
    log.info("Started command, pid {0}"
             "path {1}, output_file {2}".format(os.getppid(), args.path, args.output_file))
    begin_processing(args.path, args.output_file)
