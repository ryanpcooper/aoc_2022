from aoc_util import *

class Orchard:
	def __init__(self, lines):
		self.matrix = [] # y, x
		for line in lines:
			self.matrix.append(transform(list(line), int))
	
	def is_visible(self, x, y):
		height = self.matrix[y][x]
		left =  True
		right = True
		up =    True
		down =  True
		for i in range(0,x):
			if self.matrix[y][i] >= height:
				left = False
		for i in range(x+1, len(self.matrix[0])):
			if self.matrix[y][i] >= height:
				right = False
		for j in range(0,y):
			if self.matrix[j][x] >= height:
				up = False
		for j in range(y+1, len(self.matrix)):
			if self.matrix[j][x] >= height:
				down = False
		return left or right or up or down
	
	def visible_count(self):
		count = 0
		for y in range(0, len(self.matrix)):
			for x in range(0, len(self.matrix[0])):
				if self.is_visible(x, y):
					count += 1
		return count
		
	def view_score(self, x, y):
		height = self.matrix[y][x]
		left =  0
		right = 0
		up =    0
		down =  0
		for i in reversed(range(0,x)):
			left += 1
			if self.matrix[y][i] >= height:
				break
		for i in range(x+1, len(self.matrix[0])):
			right += 1
			if self.matrix[y][i] >= height:
				break
		for j in reversed(range(0,y)):
			up += 1
			if self.matrix[j][x] >= height:
				break
		for j in range(y+1, len(self.matrix)):
			down += 1
			if self.matrix[j][x] >= height:
				break
		return left * right * up * down
	
	def best_view_score(self):
		best = 0
		for y in range(0, len(self.matrix)):
			for x in range(0, len(self.matrix[0])):
				candidate = self.view_score(x, y)
				if candidate > best:
					best = candidate
		return best

lines = getInput(__file__)
orchard = Orchard(lines)
		
# part 1
print(orchard.visible_count())

# part 2 
print(orchard.best_view_score())
