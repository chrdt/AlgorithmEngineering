#!/usr/bin/env python2
from __future__ import print_function
import argparse
import os
import sys
import math

from src.hashtables.cuckoo_hashing import CuckooHash
from src.plotter.runtime_plot import PlotBox, PlotLine

from functools import wraps
from time import time


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        func(*args, **kwargs)
        end = time()
        return end-start
    return wrapper


@timer
def process_file(path):
    hashtable = CuckooHash(1000)
    with open(path, 'r') as file:
        for line in file:
            try:
                num = int(line)
            except ValueError:
                continue

            hashtable.insert(num, 1)

    # return hashtable.tosequence()


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Read benchmarks to remove duplicates')
    # parser.add_argument('input', help='input file to be processed')
    # parser.add_argument('--output', '-o', help='path for the output file')
    # args = parser.parse_args()
    #
    # if not os.path.exists(args.input):
    #     sys.stderr.writelines('file not found: {}\nabort.\n'.format(args.input))
    #     sys.exit(1)
    #
    # if not os.path.exists(args.output):
    #     sys.stderr.writelines('file not found: {}\nabort.\n'.format(args.output))
    #     sys.exit(1)

    avg_graph = PlotLine()
    extremes_graph = PlotBox()

    basic_path = "benchmarks/RandomSequencesRange256/"
    sub_paths = ["randomSeq_{}M_256_int/".format(i) for i in range(2, 11, 2)]

    average_runtimes, deviations = [], []

    for sub_path in sub_paths:
        runtimes = []
        path = basic_path + sub_path

        if not os.path.exists(path):
            sys.stderr.writelines('directory not found: {}\nabort.\n'.format(path))
            continue
        else:
            print("Processing directory {}...".format(basic_path + sub_path))
            files = os.listdir(path)
            for file in files:
                print("Analyzing file {}".format(file))
                runtimes.append(process_file(path + file))
            print(runtimes)
            average_runtime = sum(runtimes) / len(runtimes)
            variance = 0
            for runtime in runtimes:
                variance += ((runtime-average_runtime)**2)*1/len(runtimes)
            deviation = math.sqrt(variance)

            average_runtimes.append(average_runtime)
            deviations.append(deviation)

            extremes_graph.add_line(sub_path, map(int, runtimes))

    avg_graph.add_line("Erwartungswerte", average_runtimes)
    avg_graph.add_line("Standardabweichungen", deviations)

    avg_graph.finish()
    extremes_graph.finish()

    # out = process_file(args.input)
    # with open(args.output + "output", 'w') as outfile:
    #     outfile.write(out)
