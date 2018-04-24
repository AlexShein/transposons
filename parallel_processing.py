# Developed by AlexShein 04.2018
import argparse
import logging
import os
from datetime import datetime as dt
from functools import reduce
from multiprocessing import Pool, cpu_count
from multiprocessing.dummy import Pool as d_Pool
from operator import add
from random import randint

import pandas as pd

from process_line import process_lines

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
        if lines:
            return ((lines[-1], 1),)
    return ()


def get_random_line(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        if lines:
            return ((lines[randint(0, len(lines) - 1)], 0),)
    return ()


def get_lines(filename):
    """
    returns tuple of pairs like (line, 0/1), where 0/1 shows whether this sequence is target one or not
    Target one is in last line of file
    Non-target one is a random line of file
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
        if lines:
            return ((lines[-1], 1), (lines[randint(0, len(lines) - 1)], 0))
        else:
            return ()


def begin_processing(t_path, nt_path=None, output_file='sl_annotation_result.csv'):
    start = dt.utcnow()
    results = []
    if nt_path:
        # Processing both target and non-target files
        target_files = [
            os.path.join(
                t_path, filename
            ) for filename in os.listdir(t_path) if filename[-4:] == '.pal'
        ]
        non_target_files = [
            os.path.join(
                nt_path, filename
            ) for filename in os.listdir(nt_path) if filename[-4:] == '.pal'
        ]

        log.info("Got {0} files".format(len(target_files) + len(non_target_files)))
        # Using dummy because threading is good for io-bound operations
        with d_Pool() as d_pool:
            data_to_process = reduce(add, d_pool.map(get_last_line, target_files))
            data_to_process += reduce(add, d_pool.map(get_random_line, non_target_files))
        chunk_size = (len(target_files) + len(non_target_files)) // STREAMS + 1

    else:
        # processing target files only
        files = [
            os.path.join(
                t_path, filename
            ) for filename in os.listdir(t_path) if filename[-4:] == '.pal'
        ]

        log.info("Got {0} files".format(len(files)))
        # Using dummy because threading is good for io-bound operations
        with d_Pool() as d_pool:
            data_to_process = reduce(add, d_pool.map(get_lines, files))
        chunk_size = len(files) // STREAMS + 1

    log.info("Processing with chunk_size = {0}. Starting {1} workers".format(chunk_size, STREAMS))
    with Pool(processes=STREAMS) as pool:
        processed_data = pool.map(
            process_lines, get_chunks(data_to_process, chunk_size)
        )
    log.info("Combining results into single dict")
    for chunk in processed_data:
        results += chunk
    log.info("Creating df and writing to csv")
    result_df = pd.DataFrame(results)

    # Filling of NaN values needed
    result_df = result_df.fillna(value=0.0)

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
        '-t_path',
        dest='t_path',
        help='Location of target .pal files',
        required=True,
    )
    parser.add_argument(
        '-nt_path',
        dest='nt_path',
        help='Location of non-target .pal files',
        required=False,
        default='',
    )
    args = parser.parse_args()
    log.info("Started command, pid {0}, output_file {1}, path {2}, nt_path {3}".format(
        os.getpid(), args.output_file, args.t_path, args.nt_path,
    ))
    begin_processing(
        args.t_path,
        nt_path=args.nt_path,
        output_file=args.output_file,
    )
