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