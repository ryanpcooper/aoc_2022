# python

import itertools
import os
import sys

def getInput(scriptFile):
	inputFileName = os.path.splitext(os.path.basename(scriptFile))[0] + '.txt'
	if len(sys.argv) > 1:
		inputFileName = sys.argv[1] + '.txt'
	with open(inputFileName, 'r', encoding='latin-1') as f:
		return [line.rstrip('\n') for line in f]

def split(l, delimiter):
	return [list(y) for x, y in itertools.groupby(l, lambda z: z == delimiter) if not x]

def flatten(list_of_lists):
	return list(itertools.chain(*list_of_lists))

def group(lst, groupSize):
	return [lst[i:i+groupSize] for i in range(0, len(lst), groupSize)]
	
def transform(lst, *argv):
	for arg in argv:
		lst = list(map(arg, lst))
	return lst

def intersection(list_of_sets):
	return set.intersection(*list_of_sets)