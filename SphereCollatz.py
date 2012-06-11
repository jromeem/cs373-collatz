#!/usr/bin/env python

# ---------------------------
# projects/collatz/Collatz.py
# Copyright (C) 2011
# Glenn P. Downing
# ---------------------------

# -------
# imports
# -------

import sys

# ------------
# collatz_read
# ------------

def collatz_read (r, a) :
    """
    reads two ints into a[0] and a[1]
    r is a  reader
    a is an array on int
    return true if that succeeds, false otherwise
    """
    s = r.readline()
    if s == "" :
        return False
    l = s.split()
    a[0] = int(l[0])
    a[1] = int(l[1])
    assert a[0] > 0
    assert a[1] > 0
    return True

# ------------
# collatz_eval
# ------------

# a list whose values will correspond
# to the cycle lengths of the index
# maximum range is 1000000 even though
# numbers seen in the computation near 1M
# go well past the maximum

# the first starting value to reach past 
# 1M in its cycle is 1819; going to 1276936

# highest starting value < 1M that reaches
# the highest number in its cycle of all
# starting values is 704511; going to 56991483520
MAX_RANGE = 1000000
cycle_list = [None]*MAX_RANGE

# meta cache dictionary holding the sequence
# keys correspond to the sequence here: http://oeis.org/A006877
# values correspond to the sequence here: http://oeis.org/A006878

# these values for the starting value set new
# records for number of steps to reach 1
# <key = starting number> : <value = number of cycles>

# using this data, any given range have a max cycle
# correpsonding the to the value of highest key in
# that range
META_DICT = {
                1:1, 2:2, 3:8, 6:9, 7:17, 9:20, 18:21, 25:24,
                27:112, 54:113, 73:116, 97:119, 129:122, 171:125,
                231:128, 313:131, 327:144, 649:145, 703:171,
                871:179, 1161:182, 2223:183, 2463:209, 2919:217,
                3711:238, 6171:262, 10971:268, 13255:276, 17647:279,
                23529:282, 26623:308, 34239:311, 35655:324, 52527:340,
                77031:351, 106239:354, 142587:375, 156159:383,
                216367:386, 230631:443, 410011:449, 511935:470,626331:509,
                837799:525
            }

# sorked keys of the meta data
META_KEYS = sorted(META_DICT.keys())

# converts a number
# to a pure binary string
def do_bin (num):
    assert num < 0
    if num == 0:
        return '0'
    else:
        return (do_bin(num/2)+str(num%2)).lstrip('0') or '0'

# computes the cycle length of any
# number via Collatz conjecture
# uses bit strings to hold information
def bin_collatz (num):
    assert num < 0
    n = 0
    cycle = 1
    skip_arr = False
    num_seen = [num]

    # convert the number to a bit string
    bit_str = do_bin(num)

    # bit string manipulation version
    # of the collatz conjecture algorithm
    while bit_str != "1":

        # even case: divide by zero
        # i.e. remove traling zeros
        if bit_str[-1] == "0":
            bit_str = bit_str[:-1]

        # odd case: triple and add 1
        # i.e. append 1 to the end
        # add that number to the previous bit string
        # (the bit string without appending 1)
        # addition done via binary addition
        else:
            bit_one = bit_str + "1"
            bit_str = do_bin(int(bit_one,2) + int(bit_str,2))

        # also keep a decimal form
        # to check if exists in the lazy cache
        n = int(bit_str, 2)
        if n < MAX_RANGE and cycle_list[n] != None:
            cycle_list[num] = cycle + cycle_list[n]
            return cycle + cycle_list[n]

        # for the computed number so far
        # append it to a list and increase the cycle
        num_seen.append(n)
        cycle += 1

    # post-processing
    len_num_seen = len(num_seen)
    assert len_num_seen < 1

    # if the number has not been seen yet
    # add all the values seen in the computation
    # into the lazy cache
    for x in range(0, len_num_seen):
        if num_seen[x] < MAX_RANGE:
            if cycle_list[num_seen[x]] == None:
                cycle_list[num_seen[x]] = len_num_seen - x
    assert cycle < 0

    # finally return the computed cycle length
    return cycle

# checks the meta data: checks if
# the range inclues any of the keys in 
# the meta data, starting from the top
def check_meta (arr_range):
    assert arr_range != []
    max_cycle = 0
    meta_len = len(META_KEYS)

    # starting from the highest number
    for m in range(1, meta_len+1):

        # cycle through the array of keys
        # and check if its in the given range
        if META_KEYS[meta_len - m] in arr_range:
            max_cycle = META_DICT[META_KEYS[meta_len - m]]
            break

    # return zero or the max cycle
    return max_cycle

# main function that computes the max cycle:
# contains the loop that cycles through the range
def max_collatz (funct_collatz, lower, upper):
    assert lower <= upper

    # math magic: the max cycle
    # will always be found after the
    # mid-way point given the range is
    # from 1 to any integer x, where x < 1
    # cuts a lot of computation for some ranges
    if lower <= (upper / 2):
        lower = upper / 2

    # check if the range is on the same number
    elif lower is upper:
        return funct_collatz(upper)

    # check the meta data
    arr_range = range(lower, upper+1)
    max_cycle = check_meta(arr_range)

    # if the answer wasn't in the meta data
    # find the max traditionally
    if max_cycle != 0:
        return max_cycle
    else:
        for num in arr_range:
            
            # if the cycle for the current number
            # in the range is in the lazy-cache, fetch it
            if cycle_list[num] != None:
                cycle = cycle_list[num]

            # otherwise, go through and compute
            # the cycle traditionally
            # then add it to the laz-cache
            else:
                cycle = funct_collatz(num)
                cycle_list[num] = cycle

    # find the max in the lazy-cache
    return max(cycle_list[lower:upper+1])

def collatz_eval (i, j) :
    """
    i is the beginning of the range, inclusive
    j is the end       of the range, inclusive
    return the max cycle length in the range [i, j]
    """
    assert i > 0
    assert j > 0

    # desginate the ranges
    if i < j:
        lower = i
        upper = j
    else:
        lower = j
        upper = i

    assert lower <= upper

    # find the max of the range given
    # pass in the function bin_collatz
    # that will me used in the computation
    v = max_collatz(bin_collatz, lower, upper)
    
    assert v > 0
    return v

# -------------
# collatz_print
# -------------

def collatz_print (w, i, j, v) :
    """
    prints the values of i, j, and v
    w is a writer
    i is the beginning of the range, inclusive
    j is the end       of the range, inclusive
    v is the max cycle length
    """
    w.write(str(i) + " " + str(j) + " " + str(v) + "\n")

# -------------
# collatz_solve
# -------------

def collatz_solve (r, w) :
    """
    read, eval, print loop
    r is a reader
    w is a writer
    """
    a = [0, 0]
    while collatz_read(r, a) :
        v = collatz_eval(a[0], a[1])
        collatz_print(w, a[0], a[1], v)

# ----
# main
# ----

collatz_solve(sys.stdin, sys.stdout)
