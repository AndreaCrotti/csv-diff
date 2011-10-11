#!/usr/bin/env python2
import csv
import logging
from itertools import izip
from sys import argv, exit
import argparse

# TODO: make it configurable
# - number of header lines to skip
# - output format
# - files to give in input
# - show the coordinate in excel style for the output

ST = "Value %f in file 1 (line %d) differs by %d from %f in file 2"
DEFAULT_SKIP_LINES = 1

DEFAULT_TOLERANCE = 0.02

def excel_rows():
    # probably the first two iterations would be enough
    pass


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

    for val1, val2 in izip(r1, r2):
        for i in range(len(val1)):
            v1, v2 = float(val1[i]), float(val2[i])
            diff = compute_diff(v1, v2)

            if diff > tolerance:
                print(ST % (v1, i, diff * 100, v2))


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
