# python

import itertools
import os

def getInput(scriptFile):
	with open(os.path.splitext(os.path.basename(scriptFile))[0] + '.txt', 'r', encoding='latin-1') as f:
		return [line.rstrip('\n') for line in f]

def split(l, delimiter):
	return [list(y) for x, y in itertools.groupby(l, lambda z: z == delimiter) if not x]