from multiprocessing import cpu_count, Pool
from process_line import process_lines
import argparse
import os
import pandas as pd

STREAMS = cpu_count()


def get_chunks(lst, chunk_size):
    m = 0
    for i in range(0, len(lst), chunk_size):
        m += chunk_size
        yield lst[i:m]


def get_last_line(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        return lines[:-1]


def begin_processing(path, output_file):

    results = []
    files = [filename for filename in os.listdir(path) if filename[-4:] == '.pal']
    chunk_size = len(files) // STREAMS + 1
    with Pool(processes=STREAMS) as pool:
        processed_data = pool.map(process_lines, get_chunks(
            list(map(get_last_line, files)), chunk_size)
        )
    for chunk in processed_data:
        results += chunk
    result_df = pd.DataFrame(results)
    result_df.to_csv(output_file, sep=';')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Process lines of *.pal files to store data.',
        usage='cat *.pal | python3 process_line.py -output_file 123.csv -target 1',
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
        help='Location with pal files',
        required=True,
    )
    args = parser.parse_args()
    begin_processing(args.path, args.output_file)

    # info('main line')
    # p = Process(target=f, args=('bob',))
    # p.start()
    # p.join()
