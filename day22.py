from aoc_util import *

lines = getInput(__file__)

VOID = ' '
TILE = '.'
WALL = '#'

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

DIRECTIONS = {
	RIGHT : (0, 1),
	DOWN  : (1, 0),
	LEFT  : (0, -1),
	UP    : (-1, 0)
}

class WeirdBoard:
	def __init__(self, lines):
		self.matrix = []
		for line in lines:
			self.matrix.append(list(line))
		max_width = max(transform(self.matrix, lambda row:len(row)))
		for row in self.matrix:
			while len(row) < max_width:
				row.append(VOID)
		self.position = (0, self.matrix[0].index(TILE))
		self.facing = RIGHT
	
	def do(self, instruction):
		if isinstance(instruction, int):
			for i in range(instruction):
				success = self.move_forward()
				if not success:
					break
		elif instruction == 'R':
			self.facing += 1
			self.facing = self.facing % 4
		else:
			self.facing -= 1
			self.facing = self.facing % 4
			
	def move_forward(self):
		direction = DIRECTIONS[self.facing]
		destination_y = (self.position[0] + direction[0]) % len(self.matrix)
		destination_x = (self.position[1] + direction[1]) % len(self.matrix[0])
		destination = self.matrix[destination_y][destination_x]
		if destination == WALL:
			return False
		elif destination == VOID:
			while destination == VOID:
				destination_y = (destination_y + direction[0]) % len(self.matrix)
				destination_x = (destination_x + direction[1]) % len(self.matrix[0])
				destination = self.matrix[destination_y][destination_x]
			if destination == WALL:
				return False
			else:
				self.position = (destination_y, destination_x)
		else:
			self.position = (destination_y, destination_x)
		return True
	
	def col(self):
		return self.position[1]+1
	
	def row(self):
		return self.position[0]+1
		
	def draw(self):
		facing_chars = { RIGHT: '>', DOWN: 'v', LEFT: '<', UP: '^' }
		for y in range(len(self.matrix)):
			row_str = ''.join(self.matrix[y])
			if y == self.position[0]:
				row_str = row_str[:self.position[1]] + facing_chars[self.facing] + row_str[self.position[1]+1:]
			print(row_str)

class Face:
	def __init__(self, board, x, y, face_size):
		self.name = None
		self.x = int(x/face_size)
		self.y = int(y/face_size)
		self.matrix = []
		for j in range(face_size):
			self.matrix.append([])
			for i in range(face_size):
				self.matrix[j].append(board.matrix[y+j][x+i])
		
	def draw(self, position, facing):
		print(self.name)
		facing_chars = { RIGHT: '>', DOWN: 'v', LEFT: '<', UP: '^' }
		for y in range(len(self.matrix)):
			row_str = ''.join(self.matrix[y])
			if y == position[0]:
				row_str = row_str[:position[1]] + facing_chars[facing] + row_str[position[1]+1:]
			print(row_str)
		print()

class Cube:
	
	def __init__(self, board):
		self.face_size = self.get_face_size(board)
		faces = []
		for x in range(0, len(board.matrix[0]), self.face_size):
			for y in range(0, len(board.matrix), self.face_size):
				if board.matrix[y][x] != VOID:
					faces.append(Face(board, x, y, self.face_size))
		folding = sorted(transform(faces, lambda f: (f.y, f.x)))
		if folding == [(0,1),(0,2),(1,1),(2,0),(2,1),(3,0)]: # real
			self.top    = find(faces, lambda f: (f.y, f.x) == (1,1))
			self.back   = find(faces, lambda f: (f.y, f.x) == (0,1))
			self.right  = find(faces, lambda f: (f.y, f.x) == (0,2))
			self.front  = find(faces, lambda f: (f.y, f.x) == (2,1))
			self.left   = find(faces, lambda f: (f.y, f.x) == (2,0))
			self.bottom = find(faces, lambda f: (f.y, f.x) == (3,0))
			self.current_face = self.back
			self.rotations = {
				(self.top,    'FORWARD') : (self.front,  DOWN), # new_face, new_facing
				(self.top,    'BACKWARD'): (self.back,   UP),
				(self.top,    'RIGHT')   : (self.right,  UP),
				(self.top,    'LEFT')    : (self.left,   DOWN),
				(self.front,  'FORWARD') : (self.bottom, LEFT),
				(self.front,  'BACKWARD'): (self.top,    UP),
				(self.front,  'RIGHT')   : (self.right,  LEFT),
				(self.front,  'LEFT')    : (self.left,   LEFT),
				(self.bottom, 'FORWARD') : (self.right,  DOWN),
				(self.bottom, 'BACKWARD'): (self.left,   UP),
				(self.bottom, 'RIGHT')   : (self.front,  UP),
				(self.bottom, 'LEFT')    : (self.back,   DOWN),
				(self.back,   'FORWARD') : (self.top,    DOWN),
				(self.back,   'BACKWARD'): (self.bottom, RIGHT),
				(self.back,   'RIGHT')   : (self.right,  RIGHT),
				(self.back,   'LEFT')    : (self.left,   RIGHT),
				(self.right,  'FORWARD') : (self.top,    LEFT),
				(self.right,  'BACKWARD'): (self.bottom, UP),
				(self.right,  'RIGHT')   : (self.front,  LEFT),
				(self.right,  'LEFT')    : (self.back,   LEFT),
				(self.left,   'FORWARD') : (self.bottom, DOWN),
				(self.left,   'BACKWARD'): (self.top,    RIGHT),
				(self.left,   'RIGHT')   : (self.front,  RIGHT),
				(self.left,   'LEFT')    : (self.back,   RIGHT)
			}
		elif folding == [(0,2),(1,0),(1,1),(1,2),(2,2),(2,3)]: # test
			self.top    = find(faces, lambda f: (f.y, f.x) == (1,2))
			self.back   = find(faces, lambda f: (f.y, f.x) == (0,2))
			self.right  = find(faces, lambda f: (f.y, f.x) == (2,3))
			self.front  = find(faces, lambda f: (f.y, f.x) == (2,2))
			self.left   = find(faces, lambda f: (f.y, f.x) == (1,1))
			self.bottom = find(faces, lambda f: (f.y, f.x) == (1,0))
			self.current_face = self.back
			self.rotations = {
				(self.top,    'FORWARD')  : (self.front,   DOWN), # new_face, new_facing
				(self.top,    'BACKWARD') : (self.back,    UP),
				(self.top,    'RIGHT')    : (self.right,   DOWN),
				(self.top,    'LEFT')     : (self.left,    LEFT),
				(self.front,  'FORWARD')  : (self.bottom,  UP),
				(self.front,  'BACKWARD') : (self.top,     UP),
				(self.front,  'RIGHT')    : (self.right,   RIGHT),
				(self.front,  'LEFT')     : (self.left,    UP),
				(self.bottom, 'FORWARD')  : (self.front,   UP),
				(self.bottom, 'BACKWARD') : (self.back,    DOWN),
				(self.bottom, 'RIGHT')    : (self.left,    RIGHT),
				(self.bottom, 'LEFT')     : (self.right,   UP),
				(self.back,   'FORWARD')  : (self.top,    DOWN),
				(self.back,   'BACKWARD') : (self.bottom, DOWN),
				(self.back,   'RIGHT')    : (self.right,  LEFT),
				(self.back,   'LEFT')     : (self.left,   DOWN),
				(self.right,  'FORWARD')  : (self.bottom, RIGHT),
				(self.right,  'BACKWARD') : (self.top,    LEFT),
				(self.right,  'RIGHT')    : (self.back,   LEFT),
				(self.right,  'LEFT')     : (self.front,  LEFT),
				(self.left,   'FORWARD')  : (self.front,  RIGHT),
				(self.left,   'BACKWARD') : (self.back,   RIGHT),
				(self.left,   'RIGHT')    : (self.top,    RIGHT),
				(self.left,   'LEFT')     : (self.bottom, LEFT)
			}
		else:
			raise Exception("I don't know how to handle this folding.")
		self.top.name = 'Top'
		self.front.name = 'Front'
		self.bottom.name = 'Bottom'
		self.back.name = 'Back'
		self.right.name = 'Right'
		self.left.name = 'Left'
		self.position = (0, self.current_face.matrix[0].index(TILE))
		self.facing = RIGHT
	
	def get_face_size(self, board):
		width = len(board.matrix[0])
		height = len(board.matrix)
		if width*3 == height*4:
			face_size = int(width/4)
		elif width*4 == height*3:
			face_size = int(width/3)
		else:
			raise Exception("I don't know how to handle this folding.")
		return face_size
	
	def do(self, instruction):
		if isinstance(instruction, int):
			for i in range(instruction):
				success = self.move_forward()
				if not success:
					break
		elif instruction == 'R':
			self.facing += 1
			self.facing = self.facing % 4
		else:
			self.facing -= 1
			self.facing = self.facing % 4
	
	# returns (new_face, new_facing, new_x, new_y)
	def find_destination(self, direction):
		new_face, new_facing = self.rotations[(self.current_face, direction)]
		print((direction, new_facing))
		if direction == 'FORWARD':
			if new_facing == DOWN: # checked
				new_x = self.x()
				new_y = 0
			elif new_facing == UP:
				new_x = self.face_size-1 - self.x()
				new_y = self.face_size-1
			elif new_facing == RIGHT:
				new_x = 0
				new_y = self.face_size-1 - self.x()
			else: # LEFT # checked
				new_x = self.face_size-1
				new_y = self.x()
		elif direction == 'BACKWARD':
			if new_facing == DOWN:
				new_x = self.face_size-1 - self.x()
				new_y = 0
			elif new_facing == UP: # checked
				new_x = self.x()
				new_y = self.face_size-1
			elif new_facing == RIGHT: # checked
				new_x = 0
				new_y = self.x()
			else: # LEFT
				new_x = self.face_size-1
				new_y = self.face_size-1 - self.x()
		elif direction == 'RIGHT':
			if new_facing == DOWN:
				new_x = self.face_size-1 - self.y()
				new_y = 0
			elif new_facing == UP: # checked
				new_x = self.y()
				new_y = self.face_size-1
			elif new_facing == RIGHT: # checked
				new_x = 0
				new_y = self.y()
			else: # LEFT # checked
				new_x = self.face_size-1
				new_y = self.face_size-1 - self.y()
		else: # LEFT
			if new_facing == DOWN: # checked
				new_x = self.y()
				new_y = 0
			elif new_facing == UP:
				new_x = self.face_size-1 - self.y()
				new_y = self.face_size-1
			elif new_facing == RIGHT: # checked
				new_x = 0
				new_y = self.face_size-1 - self.y()
			else: # LEFT # checked
				new_x = self.face_size-1
				new_y = self.y()
		return (new_face, new_facing, new_x, new_y)
		
	def rotate(self, direction):
		new_face, new_facing, new_x, new_y = self.find_destination(direction)
		if new_face.matrix[new_y][new_x] == WALL:
			return False
		else:
			self.current_face = new_face
			self.position = (new_y, new_x)
			self.facing = new_facing
			return True
	
	def move_forward(self):
		direction = DIRECTIONS[self.facing]
		destination_y = (self.position[0] + direction[0])
		destination_x = (self.position[1] + direction[1])
		if destination_y >= self.face_size:
			return self.rotate('FORWARD')
		elif destination_y < 0:
			return self.rotate('BACKWARD')
		elif destination_x >= self.face_size:
			return self.rotate('RIGHT')
		elif destination_x < 0:
			return self.rotate('LEFT')
		else:
			destination = self.current_face.matrix[destination_y][destination_x]
			if destination == WALL:
				return False
			else:
				self.position = (destination_y, destination_x)
		return True
	
	def x(self):
		return self.position[1]
	
	def y(self):
		return self.position[0]
	
	def col(self):
		return self.position[1]+1 + (self.current_face.x*self.face_size)
	
	def row(self):
		return self.position[0]+1 + (self.current_face.y*self.face_size)
			
def parse_instructions(line):
	instructions = []
	current_word = ''
	for c in list(line):
		if c.isnumeric():
			current_word += c
		else:
			instructions.append(int(current_word))
			instructions.append(c)
			current_word = ''
	if current_word != '':
		instructions.append(int(current_word))
	return instructions

board_spec, instructions = split(lines, '')
instructions = parse_instructions(instructions[0])

# part 1
board = WeirdBoard(board_spec)
for instruction in instructions:
	board.do(instruction)
print(1000*board.row() + 4*board.col() + board.facing)

# part 2
board = WeirdBoard(board_spec)
cube = Cube(board)
for instruction in instructions:
	cube.do(instruction)
print(1000*cube.row() + 4*cube.col() + cube.facing)