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
#
# --- Part Two --- 
# 
# An Elf just remembered one more important detail: the two
# adjacent matching digits are not part of a larger group of matching digits.
#
# Given this additional criterion, but still ignoring the range rule, the
# following are now true:
#
# 112233 meets these criteria because the digits never decrease and all repeated
# digits are exactly two digits long. 123444 no longer meets the criteria (the
# repeated 44 is part of a larger group of 444). 111122 meets the criteria (even
# though 1 is repeated more than twice, it still contains a double 22). How many
# different passwords within the range given in your puzzle input meet all of
# the criteria?

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
    double_mode = True
    equal_count = 1
    run_length = 1
    for i in range(1, len(split)):
        digit = split[i]
        if previous == digit:
            double = True
            double_mode = True
            equal_count += 1
        elif previous > digit:
            # Digits must decrease
            return False
        else:
            if double_mode:
                double_mode = False
                # A non-even number of the same digit in a row is not allowed
                if equal_count % 2 != 0:
                    return False
                equal_count = 1
        previous = digit

    return double

assert valid_password(111122)
assert not valid_password(123444)
assert valid_password(112233)
assert not valid_password(333346)


valid = try_range(307237, 769058)
print valid
print len(valid)
