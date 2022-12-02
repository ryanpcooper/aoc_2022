# python 3

from aoc_util import *

lines = getInput(__file__)

# part 1
def roundScore1(them, me):
	myChoice = ord(me)-87;
	theirChoice = ord(them)-64;
	resultPoints = [3, 6, 0][(myChoice-theirChoice)%3]
	return resultPoints + myChoice
scores = list(map(lambda l: roundScore1(*l.split(" ")), lines))
print(sum(scores))

# part 2
def roundScore2(them, desiredResult):
	theirChoice = ord(them)-64;
	myChoice = (theirChoice + ord(desiredResult)-89)%3 or 3
	resultPoints = [3, 6, 0][(myChoice-theirChoice)%3]
	return resultPoints + myChoice
scores = list(map(lambda l: roundScore2(*l.split(" ")), lines))
print(sum(scores))
