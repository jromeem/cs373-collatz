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
# to the cycle length of the index
# maximum range is 1000000 even though
# numbers seen in the computation near 1M
# go well past the maximum
MAX_RANGE = 1000000
cycle_list = [None]*MAX_RANGE

# meta cache dictionary holding the sequence
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
META_KEYS = sorted(META_DICT.keys())

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

    assert lower <= upper

    # initialize max_cyce before computing
    # anything else
    max_cycle = 0
    
    # see if the range contains
    # any of the numbers in the meta sequence
    found = False
    meta_len = len(META_KEYS)
    arr_range = range(lower, upper+1)
    for m in range(1, meta_len+1):
        if META_KEYS[meta_len - m] in arr_range:
            max_cycle = META_DICT[META_KEYS[meta_len - m]]
            found = True
            break

    # go through the range and find
    # the largest cycle length
    for num in range(lower, upper+1):
        
        # if the number was found
        # in the meta data then break out
        if found:
            break

        # implicit else if:
        # reference the dictionary if the
        # number's cycle length had been
        # previously calculated
        if cycle_list[num] != None:
            cycle_length = cycle_list[num]
            break

        # implicit else:
        # otherwise compute the 
        # cycle length normally
        
        # keep a flag to skip populating
        # the array of seen numbers
        skip_arr = False
        
        cycle_length = 1
        num_seen = [num]

        c = num

        # collatz conjecture
        while c != 1:
            
            # keep track of the skipped number
            # and keep a flag if you skipped it
            c_skip = c
            skipped_num = False
            
            # if its even: half it!
            if c % 2 == 0:
                
                # add it to what we've seen
                # and increment the cycle length
                c = c / 2
                
            # if it's odd skip two steps!
            else:
                
                # take account the number
                # that were skipped
                c_skip = (c * 3) + 1

                # skip two steps!
                # increment twice
                c = c + (c >> 1) + 1

                # flag!
                skipped_num = True

            if skipped_num:
                num_seen.append(c_skip)
                cycle_length = cycle_length + 1

            num_seen.append(c)
            cycle_length = cycle_length + 1
            
            # if the calculated number had previously been
            # computed skip the array for populating
            if c < MAX_RANGE and cycle_list[c] != None:
                cycle_list[num] = cycle_length + cycle_list[c]

                if c is 5:
                    print "num seen", num_seen
                    print "cycle_list", cycle_list[0:20]                    
                
                skip_arr = True
                break
            
            if c_skip < MAX_RANGE and cycle_list[c_skip] != None \
                 and skipped_num:
                cycle_list[num] = cycle_length + cycle_list[c_skip] - 1
                skip_arr = True
                break
            
        # populate array
        if not skip_arr:
            len_num_seen = len(num_seen)
            for x in range(0, len_num_seen):
                if num_seen[x] < MAX_RANGE:
                    if cycle_list[num_seen[x]] == None:
                        cycle_list[num_seen[x]] = len_num_seen - x

    # meta cache vs. lazy cache
    if found:
        v = max_cycle
    else:
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

# ----
# main
# ----

collatz_solve(sys.stdin, sys.stdout)
