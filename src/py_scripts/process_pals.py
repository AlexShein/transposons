# Developed by AlexShein 04.2018
import argparse
import logging
import os
from datetime import datetime as dt
from functools import partial, reduce
from multiprocessing import Pool, cpu_count
from multiprocessing.dummy import Pool as d_Pool
from operator import add

import numpy as np
import pandas as pd

from .process_line import process_lines

STREAMS = cpu_count()

log = logging.getLogger('process_pals.py')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_chunks(lst, chunk_size):
    m = 0
    for i in range(0, len(lst), chunk_size):
        m += chunk_size
        yield lst[i:m]


def get_last_line(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return lines and [lines[-1]] or []


def get_first_line(filename):
    with open(filename, 'r') as file:
        line = file.readline()
        return [line] or []


def get_random_lines(filename, n_lines=0, omit_first=False, omit_last=False):
    """
    return lines
    """
    with open(filename, 'r') as file:
        lines = [line for line in filter(bool, file.readlines())]
        if lines:
            if omit_first:
                lines = lines[1:]
            if omit_last:
                lines = lines[:-1]
            if n_lines and n_lines <= len(lines):
                return [line for line in np.random.choice(lines, size=n_lines, replace=False)]
            else:
                return lines
        else:
            return []


def begin_processing(
    path,
    lines,
    omit,
    output_file=None,
    n_lines=0,
):
    start = dt.utcnow()
    results = []
    files = [
        os.path.join(
            path, filename
        ) for filename in os.listdir(path) if filename[-4:] == '.pal'
    ]
    log.info("Got {0} files".format(len(files)))

    # processing non-target files only
    if n_lines:
        file_lines = n_lines // len(files) + 1
        # TODO allow file skiping to deal with situations when there are more files, than n_lines
    else:
        file_lines = 0

    omit_last = 'l' in omit
    omit_first = 'f' in omit

    if lines == 'first':
        line_retiever_func = partial(get_first_line)
    elif lines == 'last':
        line_retiever_func = partial(get_last_line)
    elif lines == 'rand':
        line_retiever_func = partial(
            get_random_lines,
            n_lines=file_lines,
            omit_first=omit_first,
            omit_last=omit_last,
        )
    else:
        return

    # Using dummy because threading is good for io-bound operations
    with d_Pool() as d_pool:
        data_to_process = reduce(add, d_pool.map(line_retiever_func, files))

    log.info("Got {0} lines".format(len(data_to_process)))

    chunk_size = len(data_to_process) // STREAMS + 1

    log.info("Processing with chunk_size = {0}. Starting {1} workers".format(chunk_size, STREAMS))
    with Pool(processes=STREAMS) as pool:
        processed_data = pool.map(
            process_lines, get_chunks(data_to_process, chunk_size)
        )

    log.info("Combining results into single dict")
    for chunk in processed_data:
        results += chunk

    log.info("Creating df")
    result_df = pd.DataFrame(results)

    # Filling of NaN values needed
    result_df = result_df.fillna(value=0.0)
    if output_file:
        log.info("Writing df to {0}".format(output_file))
        result_df.to_csv(output_file, sep=';')
    end = dt.utcnow()
    log.info("Done! Execution time {}.{} seconds".format(
        str((end - start).seconds), str((end - start).microseconds)[:2],
    ))

    return result_df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Process *.pal files to store statistics.',
        usage='python3 process_pals.py -output_file 123456.csv -path ./temp_pal -lines rand -o f,l',
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
        help='Location of target .pal files',
        required=True,
    )
    parser.add_argument(
        '-n',
        dest='n_lines',
        help='Number of lines to process (per file)',
        required=False,
        default=0,
    )
    parser.add_argument(
        '-lines',
        dest='lines',
        help='Which lines to fetch',
        required=True,
        choices=['first', 'last', 'rand']
    )
    parser.add_argument(
        '-o',
        dest='omit',
        help='Which lines to omit, f[irst],l[ast]. Only for "-lines rand"',
        required=False,
        default='',
    )
    args = parser.parse_args()
    log.info("Started command, pid {0}, output_file {1}, path {2}, n_lines {3}, omit {4}".format(
        os.getpid(), args.output_file, args.path, args.n_lines, args.omit
    ))
    begin_processing(
        args.path,
        args.lines,
        args.omit.split(','),
        output_file=args.output_file,
        n_lines=int(args.n_lines),
    )
