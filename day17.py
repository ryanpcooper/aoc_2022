from aoc_util import *

class Point: 
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def __eq__(self, p2):
		return self.x == p2.x and self.y == p2.y
	
	def __str__(self):
		return str((self.x, self.y))
	
	def copy(self):
		return Point(self.x, self.y)
		
	def shift(self, x, y):
		return Point(self.x+x, self.y+y)
	
class Rock:
	def __init__(self, *tuples):
		self.points = transform(tuples, lambda t: Point(*t))
		self.width = max(transform(self.points, lambda p: p.x))+1
	
	def shift(self, x, y):
		self.points = transform(self.points, lambda p: p.shift(x, y))

class Cave: 
	def __init__(self):
		self.map = [] # two-dimensional array of width CAVE_WIDTH
		
	def move_is_legal(self, rock, rock_loc, direction):
		shifted = rock_loc.shift(*direction)
		if shifted.x < 0 or shifted.x + rock.width > CAVE_WIDTH:
			return False
		if shifted.y < 0:
			return False
		for rock_rel_point in rock.points:
			point_in_cave = shifted.shift(rock_rel_point.x, rock_rel_point.y)
			#print("Checking point: " + str(point_in_cave))
			if point_in_cave.y >= self.height():
				continue
			elif self.map[point_in_cave.y][point_in_cave.x] == '#':
				#print("There's a rock there")
				return False
			#else:
				#print("All clear")
		return True
		
	def height(self):
		return len(self.map)
	
	def draw_new_rock(self, rock, rock_loc):
		#self.draw()
		#print("drawing rock at location: " + str(rock_loc))
		for rock_rel_point in rock.points:
			point_in_cave = rock_loc.shift(rock_rel_point.x, rock_rel_point.y)
			while point_in_cave.y >= self.height():
				self.map.append([' ']*CAVE_WIDTH)
			#print("Trying to draw point " + str(point_in_cave));
			self.map[point_in_cave.y][point_in_cave.x] = '#'
		#self.draw()
			
	def draw(self):
		for i in range(self.height()-1, -1, -1):
			print("|" + ''.join(self.map[i]) + "|")
		print("+" + '-'*CAVE_WIDTH + "+")

lines = getInput(__file__)
moves = list(lines[0])

# defined as lower left = (0,0)
ROCKS = [
	Rock((0,0),(1,0),(2,0),(3,0)),       # minus
	Rock((0,1),(1,0),(1,1),(1,2),(2,1)), # plus
	Rock((0,0),(1,0),(2,0),(2,1),(2,2)), # backwards L
	Rock((0,0),(0,1),(0,2),(0,3)),       # vertical line
	Rock((0,0),(0,1),(1,0),(1,1))        # block
]
ROCK_COUNT = 2022
#ROCK_COUNT = 2
CAVE_WIDTH = 7

cave = Cave()
move_index = 0
for i in range(0, ROCK_COUNT):
	print("Dropping rock " + str(i))
	rock = ROCKS[i%5]
	rock_loc = Point(2, cave.height() + 3)
	landed = False

	while not landed:
		move = moves[move_index]
		move_index += 1
		if move_index >= len(moves):
			move_index = 0
		
		if move == '<':
			#print("pushing left")
			direction = (-1, 0)
		else:
			#print("pushing right")
			direction = (1, 0)
		if cave.move_is_legal(rock, rock_loc, direction):
			rock_loc = rock_loc.shift(*direction)
		#else:
		#	print("blocked")
		#cave.draw()
		#print("falling rock at " + str(rock_loc))
		
		direction = (0, -1)
		if cave.move_is_legal(rock, rock_loc, direction):
			rock_loc = rock_loc.shift(*direction)
			#cave.draw()
			#print("rock falls to " + str(rock_loc))
		else:
			landed = True
			cave.draw_new_rock(rock, rock_loc)
			#cave.draw()
			#print("The eagle has landed")
print(cave.height())	