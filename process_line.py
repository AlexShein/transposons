# Developed by AlexShein 04.2018
from collections import OrderedDict
from datetime import datetime as dt
from functools import reduce
from itertools import product
from operator import add
import argparse
import logging
import os
import pandas as pd
import sys

LS = ('LS0', 'LS1', 'LS2', 'LS3', 'LS4', 'LS5', 'LS6', 'LS7', 'LS8', 'LS9')
RS = ('RS0', 'RS1', 'RS2', 'RS3', 'RS4', 'RS5', 'RS6', 'RS7', 'RS8', 'RS9')
LOOP = ('LP0', 'LP1', 'LP2', 'LP3', 'LP4', 'LP5', 'LP6', 'LP7', 'LP8', 'LP9')
PROPERTIES = (
    'Shift (RNA)',
    'Slide (RNA)',
    'Rise (RNA)',
    'Tilt (RNA)',
    'Roll (RNA)',
    'Twist (RNA)',
    'Stacking energy (RNA)',
    'Enthalpy (RNA)',
    'Entropy (RNA)',
    'Free energy (RNA)',
    'GC content',
    'Purine (AG) content',
    'Keto (GT) content',
    'Adenine content',
    'Guanine content',
    'Cytosine content',
    'Thymine content',
    'Hydrophilicity (RNA)',
)
STATISTICS = ('GC precentage',)
IS_TARGET = 'is_target'

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


def get_header():
    """
    Creates header for csv file - list of combinations of positions and dinucleotides properties
    """
    positions = reduce(add, map(get_pairs, (LS, LOOP, RS)))
    combinations = product(positions, PROPERTIES)
    return list(map(lambda x: x[0][0] + x[0][1] + ' - ' + x[1], combinations)) + list(STATISTICS)


def parse_line(line):
    """
    Returns a list with left and rights parts of stem and loop and ther indexing.
    [('LS0', 'T'), ('LS1', 'A'), ('LS2', 'T'),...]
    """
    splitted_line = list(filter(bool, line.split('\t')))
    ls = splitted_line[4][::-1].upper()[:10]
    rs = splitted_line[5].upper()[:10]
    loop = splitted_line[6]
    return (
        list(zip(LS[len(ls)::-1], ls)),
        list(zip(LOOP[:len(loop)], loop)),
        list(zip(RS[:len(rs)], rs)),
        ls + loop + rs,
    )


def get_dinucleotides_properties_dict(ls, lp, rs, properties_df):
    """
    Recieves lists of pairs [('LS0', 'T'), ('LS1', 'A'), ('LS2', 'T'),...]
    Returns ordered dict with items like
    [('LS0LS1 - Shift (RNA)', -0.02), ('LS0LS1 - Slide (RNA)', -1.45), ...]
    """
    line_dict = OrderedDict(is_target=False)
    boarders = [
        (('LS', ls[-1][1]), ('LP', lp[0][1])),
        (('LP', lp[-1][1]), ('RS', rs[0][1]))
    ]
    pairs = reduce(add, map(get_pairs, (ls, lp, rs))) + boarders

    for pair in pairs:
        dinucleotide = pair[0][1] + pair[1][1]
        position = pair[0][0] + pair[1][0]
        if pair[0][1] not in NUCLEOTIDES or pair[1][1] not in NUCLEOTIDES:
            prop_values = {prop: 0 for prop in PROPERTIES}
        else:
            prop_values = properties_df[properties_df['Dinucleotide'] == dinucleotide]
        for prop in PROPERTIES:
            line_dict[(position + ' - ' + prop)] = float(prop_values[prop])
    return line_dict


def count_statistics(sequence):
    """
    returns dict of statistical features like [(('CCT', 0), ('CCG', 0), ('CCC', 0), ('GC precentage', 20.58)]
    """
    statistics_dict = OrderedDict()
    for dinucleotide in DINUCLEOTIDES:
        statistics_dict[dinucleotide] = sequence.count(dinucleotide)
    for trinucleotide in TRINUCLEOTIDES:
        statistics_dict[trinucleotide] = sequence.count(trinucleotide)
    statistics_dict['GC precentage'] = (sequence.count('G') + sequence.count('C')) * 100 / len(sequence)
    return statistics_dict


def process_lines(lines):
    """
    returns list of dicts
    """
    log = logging.getLogger(__name__ + '-' + str(os.getpid()))
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log.info("Started new worker")
    start = dt.utcnow()

    properties_df = pd.read_csv('DiPropretiesT.csv', sep=';')
    processed_lines = []
    for line, is_target in lines:
        ls, lp, rs, sequence = parse_line(line)
        line_dict = get_dinucleotides_properties_dict(ls, lp, rs, properties_df)
        line_dict.update(count_statistics(sequence))
        line_dict[IS_TARGET] = is_target
        processed_lines.append(line_dict)
    end = dt.utcnow()

    log.info("Job finished, execution time {0}".format(
        str((end - start).seconds) + '.' + str((end - start).microseconds),
    ))

    return processed_lines


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
        '-target',
        dest='target',
        type=bool,
        help='Are the sequences target ones',
        required=True,
    )
    args = parser.parse_args()

    lines = list(sys.stdin)
    data_to_process = zip(lines, [args.target] * len(lines))
    processed_lines = process_lines(data_to_process)

    result_df = pd.DataFrame(processed_lines)
    result_df.to_csv(args.output_file, sep=';')

    sys.exit(0)
