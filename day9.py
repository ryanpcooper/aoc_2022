from aoc_util import *

lines = getInput(__file__)

class Point: 
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def shift(self, x, y):
		self.x += x
		self.y += y
		
	def diff(self, other):
		return (self.x-other.x, self.y-other.y)
	
	def __eq__(self, p2):
		return self.x == p2.x and self.y == p2.y
	
	def __str__(self):
		return str((self.x, self.y))
	
	def __hash__(self):
		return hash((self.x, self.y))
	
	def copy(self):
		return Point(self.x, self.y)

class Rope:
	
	DIRECTIONS = {
		'R': (1, 0),
		'L': (-1, 0),
		'U': (0, 1),
		'D': (0, -1)
	}
	
	def __init__(self, knot_count):
		self.knots = []
		for i in range(0, knot_count):
			self.knots.append(Point(0, 0)) # x, y
		self.tail_positions = { self.knots[-1].copy() }
		
	def move(self, direction, distance):
		distance = int(distance)
		for i in range(0, distance):
			self.knots[0].shift(*self.DIRECTIONS[direction])
			for j in range(1, len(self.knots)):
				prev = self.knots[j-1]
				this = self.knots[j]
			
				(x_diff, y_diff) = prev.diff(this)
				if (max(abs(x_diff), abs(y_diff)) <= 1):
					continue
				if y_diff == -2:
					this.y -= 1
					if abs(x_diff) != 2:
						this.x = prev.x
				if y_diff == 2:
					this.y +=1
					if abs(x_diff) != 2:
						this.x = prev.x
				if x_diff == -2:
					this.x -= 1
					if abs(y_diff) != 2:
						this.y = prev.y
				if x_diff == 2:
					this.x += 1
					if abs(y_diff) != 2:
						this.y = prev.y
			self.tail_positions.add(self.knots[-1].copy())

# part 1
rope = Rope(2)
for line in lines:
	rope.move(*line.split())
print(len(rope.tail_positions))

# part 2
rope = Rope(10)
for line in lines:
	rope.move(*line.split())
print(len(rope.tail_positions))




