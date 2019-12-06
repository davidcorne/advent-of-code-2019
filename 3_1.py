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

def not_index(index):
    assert index == 0 or index == 1
    return 0 if index == 0 else 1

def intersections(line_a, line_b):
    '''
    Finds the intersection points of the two lines
    '''
    # Do this by walking along the first line, and for each span working out if
    # there is anywhere on the second line which has the same axis value
    intersections = list()
    for i in range(0, len(line_a) - 1):
        c_a = changing_index(line_a[i], line_a[i+1])
        for j in range(0, len(line_b) - 1):
            c_b = changing_index(line_b[j], line_b[j + 1])
            # We only care if they're going in opposite directions
            if (c_a != c_b):
                # get and sort the changing direction e.g. [5,9], [5,6] -> [6,9]
                changing_b = [line_b[j][c_b], line_b[j+1][c_b]]
                changing_b.sort()
                # Now see if the static value from line_a is inside changing_b
                static_a = line_a[i][c_b]
                if (changing_b[0] <= static_a and static_a <= changing_b[1]):
                    # Now check the lines cross in the other direction
                    changing_a = [line_a[i][c_a], line_a[i+1][c_a]]
                    changing_a.sort()
                    # Now see if the static value from line_b is inside changing_a
                    static_b = line_b[j][c_a]
                    # Remove (0, 0)
                    if (static_a == static_b == 0):
                        continue
                    if (changing_a[0] <= static_b and static_b <= changing_a[1]):
                        # These lines cross!
                        intersection = [0, 0]
                        intersection[c_b] = line_a[i][c_b]
                        intersection[c_a] = line_b[i][c_a]
                        intersections.append(intersection)
    return intersections

def find_nearest(intersections):
    distances = [abs(i[0]) + abs(i[1]) for i in intersections]
    distances.sort()
    print distances
    return distances[0]

def test(result, expected):
    assert len(result) == len(expected)
    for i, a in enumerate(result):
        if (a != expected[i]):
            print "Got \"", a, "\" Expected \"", expected[i], "\""
            raise RuntimeError("Test Failure")
    print("Pass")

def main_test():
    test(make_line(["R5", "U17", "L3"]), [(0,0), (5,0), (5,17), (2,17)])
    line_1 = make_line(["R8","U5","L5","D3"])
    line_2 = make_line(["U7","R6","D4","L4"])
    crossings = intersections(line_1, line_2)
    test(crossings, [[6,5], [3,3]])
    nearest = find_nearest(crossings)
    assert nearest == 6

def main():
    str_1 = "R1003,D138,L341,U798,L922,U153,R721,D177,L297,D559,L414,U470,L589,D179,L267,D954,R739,D414,L865,U688,R541,U242,R32,D607,L480,D401,L521,U727,L295,D154,R905,D54,L353,U840,L187,U942,R313,D143,R927,D962,R739,U152,R6,D9,L807,D67,R425,D235,L598,D107,L838,D522,L882,U780,L942,D29,R933,U129,L556,D11,L859,D455,L156,U673,L54,D141,R862,U88,R362,U742,L511,D408,R825,U622,R650,D393,L882,D969,R866,D232,L423,U371,L744,U35,L196,D189,R803,U663,R41,U741,R742,U929,L311,U30,R357,D776,L929,U85,R415,U540,R921,U599,R651,U79,R608,D620,L978,D92,L491,D310,L830,U656,R244,U72,L35,U768,R666,U356,R82,U596,L798,D455,L280,D626,R586,U668,R331,D245,L140,U3,R283,U813,R620,U975,L795,U477,L100,D94,R353,D732,R694,U702,L305,U497,R900,U810,L412,D954,R584,D444,L531,D875,R49,D328,L955,U227,L370,D548,L351,U571,R373,U743,R105,D226,L755,U325,R496,D960,L415,U262,R197,D508,R725,U930,L722,D162,L996,D610,R346,U680,L75,U211,R953,U147,R114,D48,L305,D284,L630,U575,R142,D518,R704,D820,L617,D118,R67,D674,L90,D916,L483,D598,L424,U92,R188,U413,L702,D262,R720,D995,L759,D732,L259,D814,L342,U642,L875,U726,R265,D143,R754,D235,L535,U1,R211,D720,R943,D726,L398,U636,R994,U653,L401,U877,R577,D460,L730,U889,R166,D641,L693,U490,L78,D80,R535,U551,L866,U283,L336,U586,L913,U474,R158,D220,R278,U11,R421,D661,R719,D696,R188,D735,L799,U391,R331,U581,R689,D82,R375,D125,R613,D705,L927,U18,R399,D352,L411,D777,L733,D884,R791,U973,R772,D878,R327,U215,L298,D360,R426,D872,L99,U78,L745,U59,L641,U73,L294,D247,R944,U512,L396"
    str_2 = "L1004,D252,L909,D935,R918,D981,L251,U486,R266,U613,L546,D815,L789,D692,L550,U633,R485,U955,R693,D784,R974,U529,R926,U550,L742,U88,R647,D572,R832,D345,R98,D122,R634,U943,L956,U551,R295,U122,L575,U378,R652,U97,R129,D872,R275,D492,L530,D328,R761,U738,R836,U884,R636,U776,L951,D977,R980,U526,L824,U125,R778,D818,R281,U929,R907,U234,L359,D521,R294,U137,L607,U421,L7,U582,R194,U979,L941,D999,R442,D330,L656,U410,R753,U704,R834,D61,R775,U750,R891,D989,R856,D944,R526,D44,R227,U938,R130,D280,L721,D171,R763,D677,L643,U931,L489,U250,L779,U552,R796,U220,R465,U700,L459,U766,R501,D16,R555,U257,R122,U452,L197,U905,L486,D726,L551,U487,R785,U470,L879,U149,L978,D708,R18,U211,L652,D141,L99,D190,L982,U556,R861,U745,L786,U674,R706,U986,R554,D39,R881,D626,R885,U907,R196,U532,L297,U232,L508,U283,L236,U613,L551,U647,R679,U760,L435,D475,R916,U669,R788,U922,R107,D503,R687,D282,L940,U835,L226,U421,L64,U245,R977,D958,L866,D328,R215,D532,R350,D199,R872,U373,R415,U463,L132,U225,L144,U786,R658,D535,R263,U263,R48,D420,L407,D177,L496,U521,R47,D356,L503,D557,R220,D879,L12,U853,R265,U983,L221,U235,R46,D906,L271,U448,L464,U258,R952,D976,L949,D526,L458,D753,L408,U222,R256,U885,R986,U622,R503,D5,L659,D553,R311,U783,L541,U17,R267,U767,L423,D501,R357,D160,L316,D912,R303,U648,L182,U342,L185,U743,L559,U816,R24,D203,R608,D370,R25,U883,L72,D816,L877,U990,R49,U331,L482,U37,L585,D327,R268,D106,L224,U401,L203,D734,L695,U910,L417,U105,R135,U876,L194,U723,L282,D966,R246,U447,R966,U346,L636,D9,L480,D35,R96"
    line_1 = make_line(str_1.split(","))
    line_2 = make_line(str_2.split(","))
    crossings = intersections(line_1, line_2)
    print crossings
    print find_nearest(crossings)

main_test()
main()