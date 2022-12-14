from aoc_util import *

lines = getInput(__file__)

class Point: 
	def __init__(self, x, y=None):
		if isinstance(x, str):
			parts = x.split(',')
			self.x = int(parts[0])
			self.y = int(parts[1])
		else:
			self.x = x
			self.y = y
	
	def __eq__(self, p2):
		return self.x == p2.x and self.y == p2.y
	
	def __str__(self):
		return str((self.x, self.y))
	
	def copy(self):
		return Point(self.x, self.y)

GRID_SIZE = 1100
SAND_SOURCE = Point(500, 0)

class Cave:
	def __init__(self, lines, add_floor):
		highest_y = 0
		self.map = [ ['.']*GRID_SIZE for i in range(GRID_SIZE)]
		for line in lines:
			points = transform(line.split(' -> '), Point)
			highest_y = max(highest_y, *transform(points, lambda p: p.y))
			for i in range(0, len(points)-1):
				self.fill(points[i], points[i+1], '#')
		if add_floor:
			floor_y = highest_y + 2
			self.fill(Point(0, floor_y), Point(GRID_SIZE-1, floor_y), '#')
	
	def fill(self, p1, p2, ch):
		if p1.x < p2.x or p1.y < p2.y:
			fr = p1.copy()
			to = p2.copy()
		else: 
			fr = p2.copy()
			to = p1.copy()
		self.map[fr.y][fr.x] = ch
		while fr.x < to.x or fr.y < to.y:
			self.map[fr.y][fr.x] = ch
			if fr.x < to.x:
				fr.x += 1
			else:
				fr.y += 1
		self.map[to.y][to.x] = ch
		
	def occupied(self, y, x):
		return self.map[y][x] != '.'
		
	def pour(self):
		sand_loc = SAND_SOURCE.copy()
		resting = False
		falling_forever = False
		source_blocked = False
		while not resting and not falling_forever and not source_blocked:
			if sand_loc.y == GRID_SIZE-1:
				falling_forever = True
			elif not self.occupied(sand_loc.y+1, sand_loc.x):
				sand_loc.y += 1
			elif not self.occupied(sand_loc.y+1, sand_loc.x-1):
				sand_loc.y += 1
				sand_loc.x -= 1
			elif not self.occupied(sand_loc.y+1, sand_loc.x+1):
				sand_loc.y += 1
				sand_loc.x += 1
			else:
				self.map[sand_loc.y][sand_loc.x] = 'o'
				resting = True
				if sand_loc == SAND_SOURCE:
					source_blocked = True
		return not falling_forever and not source_blocked
		
	def pour_until_done(self):
		i = 1
		while cave.pour():
			i += 1
		return i
		
# part 1
cave = Cave(lines, False)
print(str(cave.pour_until_done()-1)) # don't count the grain of sand that falls to infinity

# part 2
cave = Cave(lines, True)
print(str(cave.pour_until_done()))
