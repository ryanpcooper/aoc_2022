from aoc_util import *
import time

lines = getInput(__file__)

NORTH = (-1, 0)
SOUTH = ( 1, 0)
EAST =  ( 0, 1)
WEST =  ( 0,-1)
WAIT =  ( 0, 0)

OPTIONS = [NORTH, SOUTH, EAST, WEST, WAIT]

class Point: 
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def __eq__(self, p2):
		return self.x == p2.x and self.y == p2.y
	
	def __str__(self):
		return str((self.x, self.y))
	
	def __hash__(self):
		return hash((self.x, self.y))
		
	def shift(self, direction):
		return Point(self.x + direction[1], self.y + direction[0])
	
	def copy(self):
		return Point(self.x, self.y)

class Hurricane(Point): 
	def __init__(self, x, y, direction):
		self.x = x
		self.y = y
		self.direction = direction
		
	def shift(self, direction):
		return Hurricane(self.x + direction[1], self.y + direction[0], direction)

def parse_hurricanes(lines):
	hurricanes = []
	directions  = { '^': NORTH, 'v': SOUTH, '>': EAST, '<': WEST }
	for y in range(len(lines)):
		for x in range(len(lines[0])):
			c = lines[y][x]
			if c in directions.keys():
				hurricanes.append(Hurricane(x, y, directions[c]))
	return hurricanes
	
def move_hurricanes(hurricanes, valley_height, valley_width):
	new_hurricanes = []
	for hurricane in hurricanes:
		new_loc = hurricane.shift(hurricane.direction)
		if new_loc.y == 0:
			new_loc.y = valley_height-2
		if new_loc.y == valley_height-1:
			new_loc.y = 1
		if new_loc.x == 0:
			new_loc.x = valley_width-2
		if new_loc.x == valley_width-1:
			new_loc.x = 1
		new_hurricanes.append(new_loc)
	return new_hurricanes
	
def explore(paths, hurricanes, valley_height, valley_width):
	hurricane_set = set(hurricanes)
	new_paths = []
	for path in paths:
		for option in OPTIONS:
			target = path[-1].shift(option)
			if target == destination:
				return [path + [destination]]
			elif target == Point(1,0) or (not target in hurricane_set and target.x > 0 and target.x < valley_width-1 and target.y > 0 and target.y < valley_height-1):
				duplicate = False
				for other_path in new_paths:
					if other_path[-1] == target:
						duplicate = True # we already have a path leading to the same place
				if not duplicate:
					new_paths.append(path + [target])
	return new_paths

valley_height = len(lines)
valley_width = len(lines[0])

hurricanes = parse_hurricanes(lines)



# part 1
starting_position = Point(1,0)
destination = Point(valley_width-2, valley_height-1)

best_path = None
paths = [[starting_position]]
round = 1
while best_path == None:
	hurricanes = move_hurricanes(hurricanes, valley_height, valley_width)
	paths = explore(paths, hurricanes, valley_height, valley_width)
	if paths[0][-1] == destination:
		best_path = paths[0]
	print("After round " + str(round) + " there are " + str(len(paths)) + " paths.")
	round += 1
	
distance = len(best_path)-1
print(distance)

# part 2
starting_position = destination
destination = Point(1,0)

best_path = None
paths = [[starting_position]]
round = 1
while best_path == None:
	hurricanes = move_hurricanes(hurricanes, valley_height, valley_width)
	paths = explore(paths, hurricanes, valley_height, valley_width)
	if paths[0][-1] == destination:
		best_path = paths[0]
	print("After round " + str(round) + " there are " + str(len(paths)) + " paths.")
	round += 1
distance += len(best_path)-1

destination = starting_position
starting_position = Point(1,0)

best_path = None
paths = [[starting_position]]
round = 1
while best_path == None:
	hurricanes = move_hurricanes(hurricanes, valley_height, valley_width)
	paths = explore(paths, hurricanes, valley_height, valley_width)
	if paths[0][-1] == destination:
		best_path = paths[0]
	print("After round " + str(round) + " there are " + str(len(paths)) + " paths.")
	round += 1
distance += len(best_path)-1
print(distance)


