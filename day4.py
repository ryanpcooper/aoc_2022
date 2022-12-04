from aoc_util import *
import re

lines = getInput(__file__)

def full_overlap(p):
	return (p[0] <= p[2] and p[1] >= p[3]) or (p[2] <= p[0] and p[3] >= p[1])
	
def partial_overlap(p):
	elf1_sections = set(range(p[0], p[1]+1)) # ranges are exclusive of end point
	elf2_sections = set(range(p[2], p[3]+1)) # ranges are exclusive of end point
	overlap = len(elf1_sections.intersection(elf2_sections)) > 0

# part 1
pairs = transform(lines, lambda l: transform(re.split(',|-', l)), strings_to_ints)
overlaps = list(filter(full_overlap, pairs))
print(len(overlaps))

# part 2
pairs = transform(lines, lambda l: transform(re.split(',|-', l)), strings_to_ints)
overlaps = list(filter(partial_overlap, pairs))
print(len(overlaps))