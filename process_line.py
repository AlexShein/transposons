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
    'Free energy (RNA)',
    'Enthalpy (RNA)',
    'Entropy (RNA)',
    'GC content',
    'Purine (AG) content',
    'Keto (GT) content',
    'Adenine content',
    'Guanine content',
    'Cytosine content',
    'Thymine content',
    'Hydrophilicity (RNA)',
    'Hydrophilicity (RNA)',
)
STATISTICS = ('GC precentage',)


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
    Returns 3 dicts with left and rights parts of stem and loop.
    """
    splitted_line = list(filter(bool, line.split(' ')))
    ls = splitted_line[4][::-1].upper()[:10]
    rs = splitted_line[5].upper()[:10]
    loop = splitted_line[6]
    return list(zip(LS[:len(ls)], ls)) + list(zip(RS[:len(rs)], rs)) + list(zip(LOOP[:len(loop)], loop))


def get_dinucleotides_properties_dict(nucleotides_list):
    pass


if __name__ == 'main':
    properties_df = pd.read_csv('DiPropretiesT.csv')
    processed_lines = []
    for line in sys.stdin:
        line_dict = {}
        nucleotides_list = parse_line(line)

        for nucleotide in nucleotides_list:
            for property in PROPERTIES:
                pass
                # value = properties_df[]
