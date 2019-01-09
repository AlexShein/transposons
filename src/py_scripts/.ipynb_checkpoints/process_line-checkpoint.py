# Developed by AlexShein 04.2018
# Refactored 09.2018
import argparse
import logging
import os
import sys
from datetime import datetime as dt

import pandas as pd

PROPERTIES = (
    'Shift (RNA)',
    'Slide (RNA)',
    'Rise (RNA)',
    'Tilt (RNA)',
    'Roll (RNA)',
    'Twist (RNA)',
    'Hydrophilicity (RNA)',
    'Enthalpy (RNA)',
    'Entropy (RNA)',
    'Free energy (RNA)',
)

NUCLEOTIDES = 'AGTC'
DINUCLEOTIDES = [
    'AA', 'AT', 'AG', 'AC', 'TA', 'TT', 'TG', 'TC', 'GA', 'GT', 'GG', 'GC', 'CA', 'CT', 'CG', 'CC'
]
TRINUCLEOTIDES = [
    'AAA', 'AAT', 'AAG', 'AAC', 'ATA', 'ATT', 'ATG', 'ATC', 'AGA', 'AGT', 'AGG', 'AGC', 'ACA', 'ACT', 'ACG',
    'ACC', 'TAA', 'TAT', 'TAG', 'TAC', 'TTA', 'TTT', 'TTG', 'TTC', 'TGA', 'TGT', 'TGG', 'TGC', 'TCA', 'TCT',
    'TCG', 'TCC', 'GAA', 'GAT', 'GAG', 'GAC', 'GTA', 'GTT', 'GTG', 'GTC', 'GGA', 'GGT', 'GGG', 'GGC', 'GCA',
    'GCT', 'GCG', 'GCC', 'CAA', 'CAT', 'CAG', 'CAC', 'CTA', 'CTT', 'CTG', 'CTC', 'CGA', 'CGT', 'CGG', 'CGC',
    'CCA', 'CCT', 'CCG', 'CCC'
]


def get_triplets(lst):
    """
    [4,5,6,7,8] -> [(4, 5, 6), (5, 6, 7), (6, 7, 8)]
    """
    res = []
    for i in range(len(lst) - 2):
        res.append((lst[i], lst[i + 1], lst[i + 2]))
    return res


def get_pairs(lst):
    """
    [1,2,3] -> [(1, 2), (2, 3)]
    """
    res = []
    for i in range(len(lst) - 1):
        res.append((lst[i], lst[i + 1]))
    return res


def parse_line(line):
    """
    Returns parsed line - left and right stems, loop and bulges
    """
    splitted_line = list(filter(bool, line.split('\t')))
    ls = splitted_line[4][-10:]
    rs = splitted_line[5][:10]
    loop = splitted_line[6][:5]

    LS = {}
    LB = {}
    RB = {}
    LP = {}
    for i in range(len(ls) - 1):
        if ls[i].isupper() and ls[i + 1].isupper():
            LS[i] = ls[i] + ls[i + 1]
        else:
            LS[i] = 'NN'

    LB = dict(
        enumerate(map(lambda x: x.upper(), list(filter(lambda x: x.islower() or x == '_', ls[::-1][3:]))[:3]))
    )
    RB = dict(
        enumerate(map(lambda x: x.upper(), list(filter(lambda x: x.islower() or x == '_', rs[3:]))[:3]))
    )

    for i in range(len(loop)):
        LP[i] = loop[i]
    return (
        LS, LB, RB, LP, ls + loop + rs,
    )


def get_dinucleotides_properties_dict(pairs, name, properties_df, revert=False):
    """
    Recieves dict of dinucleotides
    """
    line_dict = {}

    length = len(pairs)
    for i in pairs:
        pair = pairs[i]
        prop_values = properties_df[properties_df['Dinucleotide'] == pair]
        for prop in PROPERTIES:
            pos = length - i - 1 if revert else i
            line_dict[
                name + str(pos) + '_' + prop.replace(' (RNA)', '')
            ] = float(prop_values[prop])
    return line_dict


def count_statistics(sequence):
    """
    returns dict of statistical features like [(('CCT', 0), ('CCG', 0), ('CCC', 0), ('GC precentage', 20.58)]
    """
    statistics_dict = {}
    for dinucleotide in DINUCLEOTIDES:
        statistics_dict[dinucleotide] = sequence.count(dinucleotide)
    for trinucleotide in TRINUCLEOTIDES:
        statistics_dict[trinucleotide] = sequence.count(trinucleotide)
    statistics_dict['GC precentage'] = (sequence.count('G') + sequence.count('C')) * 100 / len(sequence)
    return statistics_dict


def get_loop_binary_features(name, loop):
    res = {}
    for i in loop:
        for base in NUCLEOTIDES:
            if loop[i] == base:
                res[name + str(i) + base] = 1
            else:
                res[name + str(i) + base] = 0
    return res


def process_lines(lines):
    """
    returns list of dicts
    """
    log = logging.getLogger(__name__ + '-' + str(os.getpid()))
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log.info("Started new worker")
    start = dt.utcnow()

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DiPropretiesT.csv')
    properties_df = pd.read_csv(path, sep=';', header=0)
    NN_line = properties_df[
        [col for col in properties_df.columns if col != 'Dinucleotide']
    ].mean().rename(17)
    NN_line.at['Dinucleotide'] = 'NN'
    properties_df = properties_df.append(
        NN_line,
    )
    processed_lines = []
    for line in filter(lambda x: len(x.split('\t')) >= 7, lines):
        LS, LB, RB, LP, sequence = parse_line(line)
        line_dict = get_dinucleotides_properties_dict(
            LS, 'LS', properties_df, revert=True,
        )
        line_dict.update(count_statistics(sequence))
        line_dict.update(get_loop_binary_features('LP', LP))
        line_dict.update(get_loop_binary_features('LB', LB))
        line_dict.update(get_loop_binary_features('RB', RB))
        processed_lines.append(line_dict)
    end = dt.utcnow()

    log.info("Job finished, execution time {}.{} seconds".format(
        str((end - start).seconds), str((end - start).microseconds)[:2],
    ))

    return processed_lines


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Process lines of *.pal files to store data.',
        usage='cat *.pal | python3 process_line.py -output_file 123.csv',
    )
    parser.add_argument(
        '-output_file',
        dest='output_file',
        help='Name of file to store results',
        required=True,
    )
    args = parser.parse_args()

    data_to_process = list(sys.stdin)
    processed_lines = process_lines(data_to_process)

    result_df = pd.DataFrame(processed_lines)
    result_df.to_csv(args.output_file, sep=';')

    sys.exit(0)
