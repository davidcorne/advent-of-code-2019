#!/usr/bin/env python
# --- Day 3: Crossed Wires ---
# The gravity assist was successful, and you're well on your way to the Venus
# refuelling station. During the rush back on Earth, the fuel management system
# wasn't completely installed, so that's next on the priority list.
# 
# Opening the front panel reveals a jumble of wires. Specifically, two wires are
# connected to a central port and extend outward on a grid. You trace the path
# each wire takes as it leaves the central port, one wire per line of text (your
# puzzle input).
# 
# The wires twist and turn, but the two wires occasionally cross paths. To fix
# the circuit, you need to find the intersection point closest to the central
# port. Because the wires are on a grid, use the Manhattan distance for this
# measurement. While the wires do technically cross right at the central port
# where they both start, this point does not count, nor does a wire count as
# crossing with itself.
# 
# For example, if the first wire's path is R8,U5,L5,D3, then starting from the
# central port (o), it goes right 8, up 5, left 5, and finally down 3:
# 
# ...........
# ...........
# ...........
# ....+----+.
# ....|....|.
# ....|....|.
# ....|....|.
# .........|.
# .o-------+.
# ...........
# Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4, and left 4:
# 
# ...........
# .+-----+...
# .|.....|...
# .|..+--X-+.
# .|..|..|.|.
# .|.-X--+.|.
# .|..|....|.
# .|.......|.
# .o-------+.
# ...........
# These wires cross at two locations (marked X), but the lower-left one is closer to the central port: its distance is 3 + 3 = 6.
# 
# Here are a few more examples:
# 
# R75,D30,R83,U83,L12,D49,R71,U7,L72
# U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
# R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
# U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135

def make_line(directions):
    '''
    Pass in a list of directions as an iterable, and get back a list of points which make up the line.
    e.g. [R5, U7, L3] -> [(0,0), (0,5), (7,5), (7,2)]
    '''
    line = [(0,0)]
    previous = (0, 0)
    for d in directions:
        number = int(d[1:])
        if d[0] == "R":
            previous = (previous[0] + number, previous[1])
        elif d[0] == "L":
            previous = (previous[0] - number, previous[1])
        elif d[0] == "U":
            previous = (previous[0], previous[1] + number)
        elif d[0] == "D":
            previous = (previous[0], previous[1] - number)
        else:
            raise RuntimeError("Unexpected direction " + d[0])
        line.append(previous)
    return line

def changing_index(a, b):
    if a[0] == b[0]:
        assert a[1] != b[1]
        return 1
    if a[1] == b[1]:
        return 0
    raise AssertionError()

def intersections(line_a, line_b):
    '''
    Finds the intersection points of the two lines
    '''
    # Do this by walking along the first line, and for each span working out if
    # there is anywhere on the second line which has the same axis value
    intersections = list()
    for i in range(0, len(line_a)-1):
        print line_a[i], line_a[i+1], changing_index(line_a[i], line_a[i+1])
    return intersections

def test(result, expected):
    assert len(result) == len(expected)
    for i, a in enumerate(result):
        assert a == expected[i]
    print("Pass")

def main():
    test(make_line(["R5", "U17", "L3"]), [(0,0), (5,0), (5,17), (2,17)])
    line_1 = make_line(["R8","U5","L5","D3"])
    line_2 = make_line(["U7","R6","D4","L4"])
    test(intersections(line_1, line_2), [(3,3), (5,5)])

main()