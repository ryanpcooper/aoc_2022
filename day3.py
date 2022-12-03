from aoc_util import *

lines = getInput(__file__)

def priority(ch):
	return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".index(ch)+1

def split(string):
	halfway = len(string)//2
	return (string[:halfway], string[halfway:])

def prioritySet(string):
	return set(map(lambda ch: priority(ch), string))

# part 1
rucksacks = transform(lines, lambda l: transform(split(l), prioritySet))
duplicates = transform(rucksacks, intersection)
print(sum(flatten(duplicates)))

# part 2
rucksacks = transform(lines, prioritySet)
elfGroups = group(rucksacks, 3)
duplicates = transform(elfGroups, intersection)
print(sum(flatten(duplicates)))
