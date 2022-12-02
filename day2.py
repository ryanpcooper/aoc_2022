# python 3

from aoc_util import *

lines = getInput(__file__)

def parseTheirChoiceAndMyChoice(them, me): 
	myChoice = ord(me)-87;
	theirChoice = ord(them)-64;
	return (theirChoice, myChoice)
	
def parseTheirChoiceAndDesiredResult(them, desiredResult):
	theirChoice = ord(them)-64;
	myChoice = (theirChoice + ord(desiredResult)-89)%3 or 3
	return (theirChoice, myChoice)

def getRoundScore(theirChoice, myChoice):
	resultPoints = [3, 6, 0][(myChoice-theirChoice)%3]
	return resultPoints + myChoice

def getTotalScore(parseFunction, lines):
	return sum(list(map(lambda l: getRoundScore(*parseFunction(*l.split(" "))), lines)))

# part 1
print(getTotalScore(parseTheirChoiceAndMyChoice, lines))
	
# part 2
print(getTotalScore(parseTheirChoiceAndDesiredResult, lines))
