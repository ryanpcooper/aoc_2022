from aoc_util import *
import time

lines = getInput(__file__)

# y,x
NORTH = [(-1, -1),(-1,0),(-1,1)]
SOUTH = [(1, -1),(1,0),(1,1)]
WEST = [(-1,-1),(0,-1),(1,-1)]
EAST = [(-1,1),(0,1),(1,1)]
directions = [NORTH, SOUTH, WEST, EAST]	

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

def parse_elves(lines):
	elves = set()
	for y in range(len(lines)):
		line = lines[y]
		for x in range(len(line)):
			c = line[x]
			if c == '#':
				elves.add(Point(x, y))
	return elves	

def find_target(elf, elves, directions):
	alone = True
	for direction in directions:
		for subdirection in direction:
			destination = elf.shift(subdirection)
			if destination in elves:
				alone = False
	if alone:
		return elf.copy()
		
	for direction in directions:
		good = True
		for subdirection in direction:
			destination = elf.shift(subdirection)
			if destination in elves:
				good = False
		if good:
			return elf.shift(direction[1])
			
	return elf.copy()

def move(old_elves, directions):
	new_elves = set()
	targets = {}
	for elf in old_elves: 
		target = find_target(elf, old_elves, directions)
		if target in targets.keys():
			targets[target].append(elf)
		else:
			targets[target] = [elf]
	for target in targets.keys():
		movers = targets[target]
		if len(movers) == 1:
			new_elves.add(target)
		else:
			new_elves.update(movers)
	return new_elves
	
def draw(elves):
	min_x = min(transform(elves, lambda e: e.x))
	max_x = max(transform(elves, lambda e: e.x))
	min_y = min(transform(elves, lambda e: e.y))
	max_y = max(transform(elves, lambda e: e.y))
	for y in range(min_y, max_y+1):
		line = ''
		for x in range(min_x, max_x+1):
			if Point(x, y) in elves:
				line += '#'
			else:
				line += '.'
		print(line)

# part 1
new_elves = parse_elves(lines)
old_elves = set()
round = 1
while new_elves != old_elves:
	old_elves = new_elves
	new_elves = move(old_elves, directions)
	directions = directions[1:4] + directions[0:1]
	if round == 10:
		min_x = min(transform(new_elves, lambda e: e.x))
		max_x = max(transform(new_elves, lambda e: e.x))
		min_y = min(transform(new_elves, lambda e: e.y))
		max_y = max(transform(new_elves, lambda e: e.y))
		print((max_x+1-min_x)*(max_y+1-min_y)-len(new_elves))
	round += 1

# part 2
print(round)