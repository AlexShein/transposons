from collections import OrderedDict
from functools import reduce
from itertools import product
from operator import add
import argparse
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
    splitted_line = list(filter(bool, line.split(' ')))
    ls = splitted_line[4][::-1].upper()[:10]
    rs = splitted_line[5].upper()[:10]
    loop = splitted_line[6]
    return (
        list(zip(LS[:len(ls)], ls)) + list(zip(RS[:len(rs)], rs)) + list(zip(LOOP[:len(loop)], loop)),
        ls + loop + rs,
    )


def get_dinucleotides_properties_dict(nucleotides_list, properties_df):
    """
    Recieves list of pairs [('LS0', 'T'), ('LS1', 'A'), ('LS2', 'T'),...]
    Returns ordered dict with items like
    [('LS0LS1 - Shift (RNA)', -0.02), ('LS0LS1 - Slide (RNA)', -1.45), ...]
    """
    line_dict = OrderedDict()
    for pair in get_pairs(nucleotides_list):
        dinucleotide = pair[0][1] + pair[1][1]
        position = pair[0][0] + pair[1][0]
        if pair[0][1] == '_' or pair[1][1] == '_':
            prop_values = {prop: 0 for prop in PROPERTIES}
        else:
            prop_values = properties_df[properties_df['Dinucleotide'] == dinucleotide]
        for prop in PROPERTIES:
            line_dict[(position + ' - ' + prop)] = float(prop_values[prop])
    return line_dict


def count_statistics(sequence):
    """
    returns dict
    """
    pass


if __name__ == 'main':
    properties_df = pd.read_csv('DiPropretiesT.csv', sep=';')
    processed_lines = []
    for line in sys.stdin:
        nucleotides_list, sequence = parse_line(line)
        line_dict = get_dinucleotides_properties_dict(nucleotides_list, properties_df)
        statistics_dict = count_statistics(sequence)
