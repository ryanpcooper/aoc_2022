from aoc_util import *

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

class Grid:
	def __init__(self, lines):
		self.grid = []
		self.distances = []
		for line in lines:
			self.grid.append(list(line))
		for y in range(0, len(self.grid)):
			self.distances.append([])
			for x in range(0, len(self.grid[y])):
				self.distances[y].append(None)
	
	def get(self, point):
		return self.grid[point.y][point.x]
	
	def set_distance(self, point, distance):
		self.distances[point.y][point.x] = distance
	
	def get_distance(self, point):
		return self.distances[point.y][point.x]
	
	def find(self, target):
		for y in range(0, len(self.grid)):
			for x in range(0, len(self.grid[y])):
				if self.grid[y][x] == target:
					return Point(x, y)
		return None
	
	def populate_all_distances(self):
		end = self.find('E')
		distance = 0
		self.set_distance(end, distance)
		new_neighbours = self.find_new_neighbours([end])
		while len(new_neighbours) > 0:
			distance += 1
			for new_neighbour in new_neighbours:
				self.set_distance(new_neighbour, distance);
			new_neighbours = self.find_new_neighbours(new_neighbours)
	
	def find_new_neighbours(self, origins):
		return list(set(flatten(transform(origins, lambda o: self.find_candidates(o)))))
	
	def find_candidates(self, origin):
		candidates = [
			Point(origin.x-1, origin.y), 
			Point(origin.x, origin.y-1), 
			Point(origin.x+1, origin.y), 
			Point(origin.x, origin.y+1)
		]
		return list(filter(lambda c: self.is_legal(c, origin), candidates))
	
	def is_legal(self, candidate, origin):
		if candidate.x < 0 or candidate.y < 0 or candidate.x >= len(self.grid[0]) or candidate.y >= len(self.grid):
			return False
		if self.get_distance(candidate) != None:
			return False
		origin_elevation = self.elevation(origin)
		candidate_elevation = self.elevation(candidate)
		return candidate_elevation >= origin_elevation - 1
	
	def elevation(self, point):
		char = self.grid[point.y][point.x]
		if char == 'S':
			return 1
		if char == 'E':
			return 26
		return ord(char)-96

lines = getInput(__file__)
grid = Grid(lines)
grid.populate_all_distances()

# part 1
start = grid.find('S')
print(grid.get_distance(start))

# part 2
best = 1000000
for y in range(0, len(grid.grid)):
	for x in range(0, len(grid.grid[0])):
		distance = grid.distances[y][x]
		if distance != None and distance < best and grid.grid[y][x] == 'a':
			best = grid.distances[y][x]
print(best)
		
