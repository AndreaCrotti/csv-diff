#!/usr/bin/env python2
import csv
from itertools import izip
from sys import argv, exit
from string import ascii_uppercase
import argparse

ST = "%f -> %f [%d, %s]"
DEFAULT_SKIP_LINES = 1

DEFAULT_TOLERANCE = 0.02


def index_to_excel(idx):
    assert idx > 0
    len_alphabet = len(ascii_uppercase)
    if idx < len_alphabet:
        return ascii_uppercase[idx]
    else:
        res = []
        while idx > len_alphabet:
            res.append(idx / len_alphabet)
            idx = idx % len_alphabet

        return ''.join(ascii_uppercase[x] for x in res)


def compute_diff(val1, val2):
    if val2 == 0:
        return 0
    return abs(val1 - val2) / val1


def analyze_csv_files(f1, f2, tolerance, skip_lines):
    """Take two filenames and the tolerance and scan them through
    computing the diffs in the values
    """
    r1 = csv.reader(open(f1))
    r2 = csv.reader(open(f2))
    # skip first line
    for i in range(skip_lines):
        r1.next(); r2.next()

    # TODO: check if the number of elements are different somehow
    for rowidx, (row1, row2) in enumerate(izip(r1, r2)):
        # otherwise the files don't have the same fields
        assert len(row1) == len(row2)

        for colidx in range(len(row1)):
            v1, v2 = float(row1[colidx]), float(row2[colidx])

            diff = compute_diff(v1, v2)
            if diff > tolerance:
                print(ST % (v1, v2, rowidx, index_to_excel(colidx)))


def main():
    parser = argparse.ArgumentParser(description='compute the diff between csv files')
    parser.add_argument('-t', '--tolerance', type=float,
                        default=DEFAULT_TOLERANCE,
                        help='tolerance needed')

    parser.add_argument('-f', '--files', nargs=2,
                        help='files to pass in as arguments')

    parser.add_argument('-s', '--skip',
                        default=DEFAULT_SKIP_LINES,
                        help='header rows to skip')

    ns = parser.parse_args(argv[1:])
    analyze_csv_files(ns.files[0], ns.files[1], ns.tolerance, ns.skip)


if __name__ == '__main__':
    main()
