#!/usr/bin/env python
# --- Day 4: Secure Container ---
# You arrive at the Venus fuel depot only to discover it's protected by a
# password. The Elves had written the password on a sticky note, but someone
# threw it out.
#
# However, they do remember a few key facts about the password:
#
# It is a six-digit number. The value is within the range given in your puzzle
# input. Two adjacent digits are the same (like 22 in 122345). Going from left
# to right, the digits never decrease; they only ever increase or stay the same
# (like 111123 or 135679). Other than the range rule, the following are true:
#
# 111111 meets these criteria (double 11, never decreases). 223450 does not meet
# these criteria (decreasing pair of digits 50). 123789 does not meet these
# criteria (no double). How many different passwords within the range given in
# your puzzle input meet these criteria?
#
# Your puzzle input is 307237-769058.

def try_range(start, end):
    assert end > start
    valid = list()
    for number in range(start, end):
        if valid_password(number):
            valid.append(number)
    return valid

def valid_password(number):
    '''
    Is this a valid password by the above rules
    '''
    split = [int(i) for i in str(number)]
    previous = split[0]
    double = False
    for i in range(1, len(split)):
        digit = split[i]
        if (previous == digit):
            double = True
        if previous > digit:
            # Digits must decrease
            return False
        previous = digit

    return double

assert valid_password(111111)
assert not valid_password(223450)

valid = try_range(307237, 769058)
print len(valid)
