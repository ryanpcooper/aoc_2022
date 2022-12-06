from aoc_util import *

lines = getInput(__file__)
buf = lines[0]

def find_unique_series(buf, qty):
	for i in range(qty, len(buf)):
		if len(set(buf[i-qty:i])) == qty:
			return i
	return -1 # no start marker found

# part 1
print(find_unique_series(buf, 4))

# part 2
print(find_unique_series(buf, 14))