import numpy as np
import math
from itertools import permutations


def greedy1(objects, capacity, n):
    """
    Greedy algorithm 1:
    - For each object, put the object in the bin it fits the best, ie, leaves the smallest remaining space
    - If it doesn't fit, create a new bin
    """
    total_bins = 0
    rem_bins = [0] * n
    bins = []
    oh = 0
    for obj in objects:
        # Find the bin with the smallest remaining space
        smallest_rem_space = capacity + 1
        smallest_rem_space_idx = 0
        oh += 1
        for j in range(total_bins):
            oh += 1
            if rem_bins[j] >= obj and rem_bins[j] - obj < smallest_rem_space:
                smallest_rem_space = rem_bins[j] - obj
                smallest_rem_space_idx = j

        # If the object doesn't fit, create a new bin
        if capacity + 1 == smallest_rem_space:
            rem_bins[total_bins] =  capacity - obj
            bins.append([obj])
            total_bins += 1
        # If the object fits, put it in the bin
        else:
            rem_bins[smallest_rem_space_idx] -= obj
            bins[smallest_rem_space_idx].append(obj)

    #return total_bins + 1, bins, oh
    return total_bins + 1, bins, n**2


def greedy2(objects, capacity, n):
    """Greedy algorithm 2

    Put the object in the bin that was last used to put something into, ie the next bin, otherwise
    if it doesn't fit, create a new bin

    Parameters
    ----------
    objects : _type_
        _description_
    capacity : _type_
        _description_
    """
    total_bins = 0
    rem = capacity
    bins = [[]]
    oh = 0
    for obj in objects:
        oh += 1
        if obj <= rem:
            rem -= obj
            bins[-1].append(obj)
        else:
            total_bins += 1
            rem = capacity - obj
            bins.append([obj])
    #return total_bins + 1, bins, oh
    return total_bins + 1, bins, n

def brute(objects, capacity, n, abs_floor, early_exit=True):
    """Brute force algorithm

    Try every permutation of objects in bins and see what the minimum number of bins is

    Parameters
    ----------
    objects : _type_
        _description_
    capacity : _type_
        _description_
    """
    # worst possible case is n bins
    total_bins = n
    rem = capacity
    ideal_bins = []

    perm_objs = permutations(objects)
    for perm in perm_objs:
        bins = 0
        contents = [[]]
        for obj in perm:
            if obj <= rem:
                rem -= obj
                contents[-1].append(obj)
            else:
                bins += 1
                rem = capacity - obj
                contents.append([obj])

        if bins < total_bins:
            total_bins = bins
            ideal_bins = contents.copy()
            if total_bins + 1 == abs_floor and early_exit:
                return total_bins + 1, ideal_bins, math.factorial(n)


    return total_bins + 1, ideal_bins, math.factorial(n)

