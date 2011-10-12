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
    len_alphabet = len(ascii_uppercase)
    res = []
    while idx >= len_alphabet:
        res.append(idx / len_alphabet - 1)
        idx %= len_alphabet

    res.append(idx)

    return ''.join(ascii_uppercase[x] for x in res)


def compute_diff(val1, val2):
    if val2 == 0:
        return 0
    return abs(abs(val1 - val2) / val1)


class ResultTuple(object):
    def __init__(self, v1, v2, rowidx, colidx):
        self.v1 = v1
        self.v2 = v2
        self.rowidx = rowidx
        self.colidx = colidx

    def __str__(self):
        return self.format()

    def format(self, excel=False):
        if excel:
            colidx = index_to_excel(self.colidx)
        else:
            colidx = self.colidx

        return ST % (self.v1, self.v2, self.rowidx, colidx)


def analyze_csv_files(f1, f2, tolerance, skip_lines):
    """Take two filenames and the tolerance and scan them through
    computing the diffs in the values
    """
    r1 = csv.reader(open(f1))
    r2 = csv.reader(open(f2))
    # skip first line
    for i in range(skip_lines):
        r1.next(); r2.next()

    result = []
    # TODO: check if the number of elements are different somehow
    for rowidx, (row1, row2) in enumerate(izip(r1, r2)):
        # otherwise the files don't have the same fields
        assert len(row1) == len(row2)

        for colidx in range(len(row1)):
            v1, v2 = float(row1[colidx]), float(row2[colidx])

            diff = compute_diff(v1, v2)
            if diff > tolerance:
                result.append(ResultTuple(v1, v2, rowidx, colidx))

    return result


def start_gui():
    from PyQt4.QtGui import QApplication
    pass


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

    try:
        ns = parser.parse_args(argv[1:])
        results = analyze_csv_files(ns.files[0], ns.files[1], ns.tolerance, ns.skip)
        for r in results:
            print r.format(excel=True)
    except:
        # if the parsing didn't work then we need to fire up the GUI
        start_gui()

if __name__ == '__main__':
    main()
