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
rucksacks = list(map(lambda l: list(map(lambda c: prioritySet(c), split(l))), lines))
duplicates = flatten(list(map(lambda r: list(r[0].intersection(r[1])), rucksacks)))
print(sum(duplicates))

# part 2
rucksacks = list(map(lambda l: prioritySet(l), lines))
elfGroups = group(rucksacks, 3)
duplicates = flatten(list(map(lambda eg: list(set.intersection(*eg)), elfGroups)))
print(sum(duplicates))
