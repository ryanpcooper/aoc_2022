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

# lower left = (0,0)
ROCKS = [
	Rock((0,0),(1,0),(2,0),(3,0)),       # minus
	Rock((0,1),(1,0),(1,1),(1,2),(2,1)), # plus
	Rock((0,0),(1,0),(2,0),(2,1),(2,2)), # backwards L
	Rock((0,0),(0,1),(0,2),(0,3)),       # vertical line
	Rock((0,0),(0,1),(1,0),(1,1))        # block
]

CAVE_WIDTH = 7

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
			if point_in_cave.y >= self.height():
				continue
			elif self.map[point_in_cave.y][point_in_cave.x] == '#':
				return False
		return True
		
	def height(self):
		return len(self.map)
	
	def draw_new_rock(self, rock, rock_loc):
		for rock_rel_point in rock.points:
			point_in_cave = rock_loc.shift(rock_rel_point.x, rock_rel_point.y)
			while point_in_cave.y >= self.height():
				self.map.append([' ']*CAVE_WIDTH)
			self.map[point_in_cave.y][point_in_cave.x] = '#'
			
	def draw(self):
		for i in range(self.height()-1, -1, -1):
			print("|" + ''.join(self.map[i]) + "|")
		print("+" + '-'*CAVE_WIDTH + "+")

lines = getInput(__file__)
moves = list(lines[0])

def simulate(count, allow_shortcut=False):
	pattern_finder = {}
	cave = Cave()
	move_index = 0
	bonus_height = 0
	i = 0
	while i < count:
		rock_index = i%5
		rock = ROCKS[rock_index]
		rock_loc = Point(2, cave.height() + 3)
		landed = False

		while not landed:
			move = moves[move_index]
			move_index += 1
			if move_index >= len(moves):
				move_index = 0
		
			if move == '<':
				direction = (-1, 0)
			else:
				direction = (1, 0)
			if cave.move_is_legal(rock, rock_loc, direction):
				rock_loc = rock_loc.shift(*direction)
		
			direction = (0, -1)
			if cave.move_is_legal(rock, rock_loc, direction):
				rock_loc = rock_loc.shift(*direction)
			else:
				landed = True
				cave.draw_new_rock(rock, rock_loc)
		
		deja_vu = pattern_finder.get((rock_index, move_index))
		if allow_shortcut and deja_vu != None:
			prev_height = deja_vu[1]
			prev_iter = deja_vu[0]
			this_height = cave.height()
			
			look_back = 1
			# Look back and verify cave state matches until we find a fully blocked row.
			# This guarantees a true repeated-state scenario unlike Bront's YOLO solution.
			while cave.map[prev_height-look_back] == cave.map[this_height-look_back]:
				if cave.map[this_height-look_back] == ['#']*CAVE_WIDTH:
					repeat_interval = i-prev_iter
					height_diff = this_height-prev_height
					remaining_iters = count - i
					remainder = remaining_iters % repeat_interval
					# "fast forward" to just before the finish line and do the last few iters normally
					i = count-remainder
					repeat_count = int(remaining_iters/repeat_interval)
					bonus_height = (repeat_count * height_diff)
					allow_shortcut = False
					break
				look_back += 1
		pattern_finder[(rock_index, move_index)] = (i, cave.height())
		i += 1
	return cave.height() + bonus_height

# part 1
print(simulate(2022))

# part 2
print(simulate(1000000000000, allow_shortcut=True))
