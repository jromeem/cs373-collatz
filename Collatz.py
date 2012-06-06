#!/usr/bin/env python

# ---------------------------
# projects/collatz/Collatz.py
# Copyright (C) 2011
# Glenn P. Downing
# ---------------------------

# ------------
# collatz_read
# ------------

import sys, math

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

# hold a dictionary of
# cycle lengths already seen
cycle_dict = {}
def collatz_eval (i, j) :
    """
    i is the beginning of the range, inclusive
    j is the end       of the range, inclusive
    return the max cycle length in the range [i, j]
    """
    assert i > 0
    assert j > 0

    # check ranges
    if i < j:
        lower = i
        upper = j
    else:
        lower = j
        upper = i
    
    # go through range and find max cycle length
    max_cycle = 0
    for num in range(lower, upper+1):
        
        # reference the dictionary if the
        # number's cycle length had been
        # previously calculated
        if num in cycle_dict:
            cycle_length = cycle_dict[num]
            max_cycle = max(max_cycle, cycle_length)
            continue

        # implicit else:
        cycle_length = 1
        
        # for each number in the range
        # keep track of all the numbers
        # seen in the calculations
        num_seen = [num]
        
        # collatz conjecture
        while num != 1:
            if num % 2 == 0:
                num = num / 2
            else:
                num = (3*num) + 1
            cycle_length = cycle_length + 1
            num_seen.append(num)
            
        # assign cycle lengths to number seen
        len_num_seen = len(num_seen)
        for x in range(0, len_num_seen):
            if not num_seen[x] in cycle_dict:
                cycle_dict[num_seen[x]] = len_num_seen - x

        # what is the max so far
        max_cycle = max(max_cycle, cycle_length)
        
    v = max_cycle
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
