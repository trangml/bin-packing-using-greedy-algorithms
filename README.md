# bin-packing-using-greedy-algorithms


## Overview
This repo contains code demonstrating bin packing using different greedy algorithms. This is intended to demonstrate
different greedy algorithms.


## How to Use
Necessary Packages:
numpy
matplotlib

Install packages using pip install
```
pip install numpy matplotlib
```


Instructions for how to run:
From inside the same directory Solver.py is in, use the following to run:

```
usage: Solver.py [-h] [--method {G1,G2,Brute,BenchmarkSmall,BenchmarkLarge,S1,S2}] [--n N] [--c C] [--seed SEED]

optional arguments:
  -h, --help            show this help message and exit
  --method {G1,G2,Brute,BenchmarkSmall,BenchmarkLarge,S1,S2}
                        which form of algorithm to run, G1: Greedy 1, G2: Greedy 2, or Brute. Pass BenchmarkSmall to run benchmark test on small n, and BenchmarkLarge to run benchmark
                        on large n. Pass S1 to run sensitivity test on C, and S2 to run sensitivity test on sorted or nonsorted
  --n N                 the number of objects to store
  --c C                 the max capacity of the bins
  --seed SEED           the random seed to use
```
ex:

```
python Solver.py --method G1 --n 400 --c 100
python Solver.py --method BenchmarkLarge
```
