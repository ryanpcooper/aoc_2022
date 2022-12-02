# python 3

from aoc_util import *

lines = getInput(__file__)

def parseTheirChoiceAndMyChoice(them, me): 
	theirChoice = ord(them)-64; # convert A|B|C -> 1|2|3
	myChoice = ord(me)-87;      # convert X|Y|Z -> 1|2|3
	return (theirChoice, myChoice)
	
def parseTheirChoiceAndDesiredResult(them, desiredResult):
	theirChoice = ord(them)-64;                      # convert A|B|C -> 1|2|3
	desiredResult = ord(desiredResult)-89            # convert X|Y|Z -> -1|0|1
	myChoice = (theirChoice + desiredResult)%3 or 3  # figure out my choice (1|2|3)
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
