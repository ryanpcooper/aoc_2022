# python 3

from aoc_util import *

lines = getInput(__file__)

def roundScore(them, me):
	myChoice = ord(me)-87;
	theirChoice = ord(them)-64;
	resultPoints = [3, 6, 0][(myChoice-theirChoice)%3]
	return resultPoints + myChoice

scores = list(map(lambda l: roundScore(*l.split(" ")), lines))

# part 1
print(sum(scores))
