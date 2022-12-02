# python 3

from aoc_util import *

lines = getInput(__file__)
elves = split(lines, '')
cals = list(map(lambda e: sum(map(int, e)), elves))
cals = sorted(cals, reverse=True)

# part 1
print(cals[0])

# part 2
print(sum(cals[0:3]))