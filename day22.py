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
		self.draw()
		print("Initial position: " + str(self.position))
		print("Initial facing: " + str(self.facing))
		
	
	def do(self, instruction):
		print("Instruction: " + str(instruction))
		if isinstance(instruction, int):
			print("    Old position:  " + str(self.position))
			for i in range(instruction):
				success = self.move_forward()
				if not success:
					break
				if i == instruction-1:
					print("Full move!")
			print("    New position:  " + str(self.position))
		elif instruction == 'R':
			print("    Old facing:    " + str(self.facing))
			self.facing += 1
			self.facing = self.facing % 4
			print("    New facing:    " + str(self.facing))
		else:
			print("    Old facing:    " + str(self.facing))
			self.facing -= 1
			self.facing = self.facing % 4
			print("    New facing:    " + str(self.facing))
		self.draw()
			
	def move_forward(self):
		#print("Trying to move forward...")
		direction = DIRECTIONS[self.facing]
		destination_y = (self.position[0] + direction[0]) % len(self.matrix)
		destination_x = (self.position[1] + direction[1]) % len(self.matrix[0])
		destination = self.matrix[destination_y][destination_x]
		if destination == WALL:
			print("Blocked by wall")
			return False
		elif destination == VOID:
			while destination == VOID:
				destination_y = (destination_y + direction[0]) % len(self.matrix)
				destination_x = (destination_x + direction[1]) % len(self.matrix[0])
				destination = self.matrix[destination_y][destination_x]
			if destination == WALL:
				print("Can't wrap due to wall at destination")
				return False
			else:
				print("Wrapping")
				self.position = (destination_y, destination_x)
		else:
			print("Walking")
			self.position = (destination_y, destination_x)
		return True
	
	def col(self):
		return self.position[1]+1
		#my_row = self.matrix[self.position[0]]
		#void_count = ''.join(my_row[:self.position[1]]).count(VOID)
		#y_pos = self.position[1]+1 
		#return y_pos-void_count
	
	def row(self):
		return self.position[0]+1
		
	def draw(self):
		facing_chars = { RIGHT: '>', DOWN: 'v', LEFT: '<', UP: '^' }
		for y in range(len(self.matrix)):
			row_str = ''.join(self.matrix[y])
			if y == self.position[0]:
				row_str = row_str[:self.position[1]] + facing_chars[self.facing] + row_str[self.position[1]+1:]
			print(row_str)
			

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
board = WeirdBoard(board_spec)
instructions = parse_instructions(instructions[0])

print(instructions)

for instruction in instructions:
	board.do(instruction)
print("row: " + str(board.row()))
print("col: " + str(board.col()))
print("facing: " + str(board.facing))
print(1000*board.row() + 4*board.col() + board.facing)