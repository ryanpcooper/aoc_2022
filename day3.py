from aoc_util import *

lines = getInput(__file__)

def priority(ch):
	return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".index(ch)+1

def split(string):
	halfway = len(string)//2
	return (string[:halfway], string[halfway:])

def priorities(string):
	return list(map(lambda ch: priority(ch), string))

# part 1
rucksacks = transform(lines, priorities, split)
duplicates = transform(rucksacks, intersection)
print(sum(flatten(duplicates)))

# part 2
rucksacks = transform(lines, priorities)
elfGroups = group(rucksacks, 3)
duplicates = transform(elfGroups, intersection)
print(sum(flatten(duplicates)))
