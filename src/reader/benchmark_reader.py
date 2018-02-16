#!/usr/bin/env python2
from __future__ import print_function
import os
import sys
import math

from src.hashtables.cuckoo_hashing import CuckooHash
from src.hashtables.bucketized_cuckoo_hashing import BucketizedCuckooHash
from src.util.timer import timer
#from src.plotter.runtime_plot import PlotBox, PlotLine
#import argparse


@timer
def process_file(path):
    hashtable = BucketizedCuckooHash(64)
    with open(path, 'r') as file:
        for line in file:
            try:
                num = int(line.translate(None, ":.-"), 16)
                # num = int(line)
            except ValueError:
                continue

            if not hashtable.contains(num):
                hashtable.insert(num, 1)


if __name__ == '__main__':
    # TODO: argparse instead of hard-coded paths and values
    basic_path = "../../benchmarks/pcapSim/large/"
    sub_paths = ["{}M/".format(i) for i in range(2,3,2)]

    average_runtimes, deviations = [], []
    final_runtimes = dict()

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
            print("Deviation: {}, Average: {}".format(deviation, average_runtime))
