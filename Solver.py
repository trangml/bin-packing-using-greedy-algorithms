import os
import sys
import argparse
import numpy as np
import time
import math
import pprint
import matplotlib.pyplot as plt
from BinPacker import *

"This program solves the bin packing problem using greedy algorithms"

def generate_objects(n, c):
    # Generate random objects
    objects = np.random.randint(1, c+1, n)
    return objects

def get_optimal_bins(objects, capacity):
    # Get the optimal number of bins
    bins = math.ceil(np.sum(objects)/capacity)
    return bins

def solver(n, c,method, objects = None, verbose=True):
    if objects.any() == None:
        objects = generate_objects(n, c)

    abs_floor = get_optimal_bins(objects, c)
    if verbose:
        pprint.pprint(objects)
    print("Minimum number of bins needed >=" + str(abs_floor))

    if method == 'G1':
        start = time.time()
        bins, contents, o = greedy1(objects, c, n)
        end = time.time()
        print("Greedy 1: ", bins, " bins used in ", end - start, " seconds")
    elif method == 'G2':
        start = time.time()
        bins, contents, o = greedy2(objects, c, n)
        end = time.time()
        print("Greedy 2: ", bins, " bins used in ", end - start, " seconds")
    elif method == 'Brute':
        start = time.time()
        bins, contents, o = brute(objects, c, n, abs_floor)
        end = time.time()
        print("Brute force: ", bins, " bins used in ", end - start, " seconds")
    if verbose:
        pprint.pprint(contents)

    return end-start, bins, o


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--method', type=str, default='G1', help='which form of algorithm to run, G1: Greedy 1, G2: Greedy 2, or Brute. Pass BenchmarkSmall to run benchmark test on small n, and BenchmarkLarge to run benchmark on large n. Pass S1 to run sensitivity test on C, and S2 to run sensitivity test on sorted or nonsorted', choices=['G1', 'G2', 'Brute', 'BenchmarkSmall', 'BenchmarkLarge', 'S1', 'S2'])
    parser.add_argument('--n', type=int, default=10, help='the number of objects to store')
    parser.add_argument('--c', type=int, default=10, help='the max capacity of the bins')
    parser.add_argument('--seed', type=int, default=None, help='the random seed to use')
    args = parser.parse_args()

    if args.seed == None:
        np.random.seed()
    else:
        np.random.seed(seed)

    method = args.method

    if method == "BenchmarkSmall":
        print("Running benchmark on small n")
        times = [[], [], []]
        bins = [[], [], []]
        bigO = [[], [], []]
        optimal_bins = []
        test_c = 10
        methods = ['G1', 'G2', 'Brute']
        max_n = 15
        ns = range(0, max_n + 1, 1)

        for test_n in ns:
            print("Running test for n = " + str(test_n))
            objects = generate_objects(test_n, test_c)
            abs_floor = get_optimal_bins(objects, test_c)
            optimal_bins.append(abs_floor)
            for test_method, tpm, bpm, oh in zip(methods, times, bins, bigO):
                runtime, bin_num, o = solver(test_n, test_c, test_method, objects=objects, verbose=False)
                tpm.append(runtime)
                bpm.append(bin_num)
                oh.append(o)

        print("\n\n")
        pprint.pprint(times)
        pprint.pprint(bins)

        plt.plot(ns, times[0], label='Greedy 1', marker='o')
        plt.plot(ns, times[1], label='Greedy 2', marker='<')
        plt.plot(ns, times[2], label='Brute', marker='s')
        #plt.yscale('log')
        plt.ylim(-0.1, 2)
        plt.grid(True)
        plt.xlabel('n')
        plt.ylabel('seconds')
        plt.title("Simulation Running Time for Small-Scale Problem")
        plt.legend()
        plt.show()

        plt.plot(ns, bigO[0], label='Greedy 1', marker='o')
        plt.plot(ns, bigO[1], label='Greedy 2', marker='<')
        plt.plot(ns, bigO[2], label='Brute', marker='s')
        #plt.yscale('log')
        plt.ylim(0, 2* max_n**2)
        plt.grid(True)
        plt.xlabel('n')
        plt.ylabel('Big-O notation')
        plt.title("Asymptotic Complexity Comparison for Small-Scale Problem")
        plt.legend()
        plt.show()

        plt.plot(ns, bins[0], label='Greedy 1', marker='o')
        plt.plot(ns, bins[1], label='Greedy 2', marker='<')
        plt.plot(ns, bins[2], label='Brute', marker='s')
        #plt.plot(ns, optimal_bins, label='Optimal Lower Bound', marker='s', linestyle='--')
        #plt.yscale('log')
        plt.grid(True)
        plt.xlabel('n')
        plt.ylabel('bins')
        plt.title("Optimality Comparison for Small-Scale Problem")
        plt.legend()
        plt.show()

    elif method == "BenchmarkLarge":
        print("Running benchmark on small n")
        times = [[], []]
        bins = [[], []]
        bigO = [[],[]]
        optimal_bins = []
        test_c = 10
        methods = ['G1', 'G2']
        max_n = 1000
        ns = range(0, max_n + 1, 50)

        for test_n in ns:
            print("Running test for n = " + str(test_n))
            objects = generate_objects(test_n, test_c)
            abs_floor = get_optimal_bins(objects, test_c)
            optimal_bins.append(abs_floor)
            for test_method, tpm, bpm, oh in zip(methods, times, bins, bigO):
                runtime, bin_num, o = solver(test_n, test_c, test_method, objects=objects, verbose=False)
                tpm.append(runtime)
                bpm.append(bin_num)
                oh.append(o)

        plt.plot(ns, times[0], label='Greedy 1', marker='o')
        plt.plot(ns, times[1], label='Greedy 2', marker='<')
        #plt.yscale('log')
        #plt.ylim(-0.1, 2)
        plt.grid(True)
        plt.xlabel('n')
        plt.ylabel('seconds')
        plt.title("Simulation Running Time for Large-Scale Problem")
        plt.legend()
        plt.show()

        plt.plot(ns, bigO[0], label='Greedy 1', marker='o')
        plt.plot(ns, bigO[1], label='Greedy 2', marker='<')
        #plt.yscale('log')
        #plt.ylim(0, 2* max_n**2)
        plt.grid(True)
        plt.xlabel('n')
        plt.ylabel('Big-O notation')
        plt.title("Asymptotic Complexity Comparison for Large-Scale Problem")
        plt.legend()
        plt.show()

        plt.plot(ns, bins[0], label='Greedy 1', marker='o')
        plt.plot(ns, bins[1], label='Greedy 2', marker='<')
        plt.plot(ns, optimal_bins, label='Optimal Lower Bound', marker='s', linestyle='--')
        #plt.yscale('log')
        plt.grid(True)
        plt.xlabel('n')
        plt.ylabel('bins')
        plt.title("Optimality Comparison for Large-Scale Problem")
        plt.legend()
        plt.show()

    elif method == "S1":
        print("Running sensitivity analysis on varying capacity")
        # times = [[], []]
        # bins = [[], []]
        # bigO = [[],[]]
        # times = [[], [], [], [], [], []]
        # bins = [[], [], [], [], [], []]
        # bigO = [[],[], [], [], [], []]
        times = []
        bins = []
        bigO = []

        optimal_bins = []
        g1diff = []
        g2diff = []
        test_c = 10
        methods = ['G1', 'G2']
        max_n = 500
        ns = range(0, max_n + 1, 25)
        max_c = 1000
        #cs = range(10, max_c + 1, 50)
        #cs = [10, 10, 500, 500, 1000, 1000]
        cs = [10, 500, 1000]

        for test_c in cs:
            ctimes = [[], []]
            cbins = [[], []]
            cbigO = [[],[]]
            cdiff = [[],[]]
            coptimal_bins = []
            print("Running test for c = " + str(test_c))
            for test_n in ns:
                print("Running test for n = " + str(test_n))
                objects = generate_objects(test_n, test_c)
                #print("Running test for c = " + str(test_c))
                abs_floor = get_optimal_bins(objects, test_c)
                coptimal_bins.append(abs_floor)
                for test_method, tpm, bpm, oh, d in zip(methods, ctimes, cbins, cbigO, cdiff):
                    runtime, bin_num, o = solver(test_n, test_c, test_method, objects=objects, verbose=False)
                    d.append(bin_num - abs_floor)
                    tpm.append(runtime)
                    bpm.append(bin_num)
                    oh.append(o)
            times.extend(ctimes)
            bins.extend(cbins)
            bigO.extend(cbigO)
            g1diff.append(np.mean(cdiff[0]))
            g2diff.append(np.mean(cdiff[1]))
            optimal_bins.append(coptimal_bins)

        pprint.pprint(times)

        plt.plot(ns, times[0], label='C: 10, Greedy 1', marker='o')
        plt.plot(ns, times[1], label='C: 10, Greedy 2', marker='o')
        plt.plot(ns, times[2], label='C: 500, Greedy 1', marker='^')
        plt.plot(ns, times[3], label='C: 500, Greedy 2', marker='^')
        plt.plot(ns, times[4], label='C: 1000, Greedy 1', marker='d')
        plt.plot(ns, times[5], label='C: 1000, Greedy 2', marker='d')

        #plt.yscale('log')
        #plt.ylim(-0.1, 2)
        plt.grid(True)
        plt.xlabel('n')
        plt.ylabel('seconds')
        plt.title("Simulation Running Time for Capacity Sensitivity Analysis")
        plt.legend()
        plt.show()

        plt.plot(ns, bigO[0], label='C: 10, Greedy 1', marker='o')
        plt.plot(ns, bigO[1], label='C: 10, Greedy 2', marker='o')
        plt.plot(ns, bigO[2], label='C: 500, Greedy 1', marker='^')
        plt.plot(ns, bigO[3], label='C: 500, Greedy 2', marker='^')
        plt.plot(ns, bigO[4], label='C: 1000, Greedy 1', marker='d')
        plt.plot(ns, bigO[5], label='C: 1000, Greedy 2', marker='d')
        #plt.yscale('log')
        #plt.ylim(0, 2* max_n**2)
        plt.grid(True)
        plt.xlabel('n')
        plt.ylabel('Big-O notation')
        plt.title("Asymptotic Complexity Comparison for Capacity Sensitivity Analysis")
        plt.legend()
        plt.show()

        plt.plot(ns, bins[0], label='C: 10, Greedy 1', marker='o')
        plt.plot(ns, bins[1], label='C: 10, Greedy 2', marker='o')
        plt.plot(ns, bins[2], label='C: 500, Greedy 1', marker='^')
        plt.plot(ns, bins[3], label='C: 500, Greedy 2', marker='^')
        plt.plot(ns, bins[4], label='C: 1000, Greedy 1', marker='d')
        plt.plot(ns, bins[5], label='C: 1000, Greedy 2', marker='d')
        plt.plot(ns, optimal_bins[0], label='C:10, Optimal Lower Bound', marker='o', linestyle='--')
        plt.plot(ns, optimal_bins[1], label='C:500, Optimal Lower Bound', marker='^', linestyle='--')
        plt.plot(ns, optimal_bins[2], label='C:1000, Optimal Lower Bound', marker='d', linestyle='--')
        #plt.yscale('log')
        plt.grid(True)
        plt.xlabel('n')
        plt.ylabel('bins')
        plt.title("Optimality Comparison for Capacity Sensitivity Analysis")
        plt.legend()
        plt.show()

        # Bar graph for the differences
        x = np.arange(len(cs))
        width = 0.35
        fig, ax = plt.subplots()
        rects1 = ax.bar(x-width/2, g1diff, width, label='Greedy 1', color='b')
        rects2 = ax.bar(x+width/2, g2diff, width, label='Greedy 2', color='r')
        ax.set_ylabel('Difference in bins')
        ax.set_xlabel('Capacity')
        ax.set_title('Distance from lower optimal bound for different capacities')
        ax.set_xticks(x, cs)
        ax.legend()

        fig.tight_layout()
        plt.show()

    elif method == "S2":
        print("Running Sensitivity analysis 2 on large n")
        times = [[], [], [], []]
        bins = [[], [], [], []]
        bigO = [[],[], [], []]
        optimal_bins = []
        test_c = 10
        methods = ['G1', 'G2', 'G1', 'G2',]
        sort = [False, False, True, True]
        max_n = 500
        ns = range(0, max_n + 1, 25)

        for test_n in ns:
            print("Running test for n = " + str(test_n))
            objects = generate_objects(test_n, test_c)
            abs_floor = get_optimal_bins(objects, test_c)
            optimal_bins.append(abs_floor)
            for test_method, tpm, bpm, oh, doSort in zip(methods, times, bins, bigO, sort):
                if doSort:
                    # Now, rerun the results but reversed
                    objects = objects[np.argsort(-objects)]
                runtime, bin_num, o = solver(test_n, test_c, test_method, objects=objects, verbose=False)
                tpm.append(runtime)
                bpm.append(bin_num)
                oh.append(o)


        plt.plot(ns, times[0], label='Greedy 1', marker='o', linestyle='--')
        plt.plot(ns, times[1], label='Greedy 2', marker='<', linestyle='--')
        plt.plot(ns, times[2], label='Sorted Greedy 1', marker='X')
        plt.plot(ns, times[3], label='Sorted Greedy 2', marker='p')
        #plt.yscale('log')
        #plt.ylim(-0.1, 2)
        plt.grid(True)
        plt.xlabel('n')
        plt.ylabel('seconds')
        plt.title("Simulation Running Time for Sorting Sensitivity Analysis")
        plt.legend()
        plt.show()

        plt.plot(ns, bigO[0], label='Greedy 1', marker='o', linestyle='--')
        plt.plot(ns, bigO[1], label='Greedy 2', marker='<', linestyle='--')
        plt.plot(ns, bigO[2], label='Sorted Greedy 1', marker='X')
        plt.plot(ns, bigO[3], label='Sorted Greedy 2', marker='p')
        #plt.yscale('log')
        #plt.ylim(0, 2* max_n**2)
        plt.grid(True)
        plt.xlabel('n')
        plt.ylabel('Big-O notation')
        plt.title("Asymptotic Complexity Comparison for Sorting Sensitivity Analysis")
        plt.legend()
        plt.show()

        plt.plot(ns, bins[0], label='Greedy 1', marker='o', linestyle='--')
        plt.plot(ns, bins[1], label='Greedy 2', marker='<', linestyle='--')
        plt.plot(ns, bins[2], label='Sorted Greedy 1', marker='X')
        plt.plot(ns, bins[3], label='Sorted Greedy 2', marker='p')
        plt.plot(ns, optimal_bins, label='Optimal Lower Bound', marker='s', linestyle='--')
        #plt.yscale('log')
        plt.grid(True)
        plt.xlabel('n')
        plt.ylabel('bins')
        plt.title("Optimality Comparison for Sorting Sensitivity Analysis")
        plt.legend()
        plt.show()

    else:
        objects = generate_objects(args.n, args.c)
        solver(args.n, args.c, method, objects=objects, verbose=True)


if __name__ == "__main__":
    main()
