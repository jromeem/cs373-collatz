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

# a list whose values will correspond
# to the cycle length of the index
# maximum range is 1000000 even though
# numbers seen in the computation near 1M
# go well past the maximum
MAX_RANGE = 1000000
cycle_list = [None]*MAX_RANGE

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
        if num < MAX_RANGE and cycle_list[num] != None:
            cycle_length = cycle_list[num]

        # otherwise compute the cycle length normally
        else:
            # keep a flag to skip populating the array of seen numbers
            skip_arr = False
            
            cycle_length = 1
            num_seen = [num]

            c = num
            # collatz conjecture
            while c != 1:
                if c % 2 == 0:
                    c = c / 2
                else:
                    c = (3*c) + 1

                # if the calculated number had previously been
                # computed skip the array for populating
                if c < MAX_RANGE and num < MAX_RANGE and cycle_list[c] != None:
                    cycle_list[num] = cycle_length + cycle_list[c]
                    skip_arr = True
                    break

                # implicit else:
                num_seen.append(c)
                cycle_length = cycle_length + 1
                
            # populate array
            if not skip_arr:
                len_num_seen = len(num_seen)
                for x in range(0, len_num_seen):
                    if num_seen[x] < MAX_RANGE:
                        if cycle_list[num_seen[x]] == None:
                            cycle_list[num_seen[x]] = len_num_seen - x
        
    v = max(cycle_list[lower:upper+1])
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
