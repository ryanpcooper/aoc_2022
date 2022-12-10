from aoc_util import *

lines = getInput(__file__)

# part 1
cycle = 1
register = 1

TARGETS = [20, 60, 100, 140, 180, 220]
target_signals = []

for line in lines:
	cycle += 1
	if line != 'noop':
		val = int(line.split()[1])
		if cycle in TARGETS:
			target_signals.append(cycle*register)
		cycle += 1
		register += val
	if cycle in TARGETS:
		target_signals.append(cycle*register)

print(sum(target_signals))

# part 2

class Communicator:
	def __init__(self):
		self.cycle = 0
		self.register = 1
		self.display = [[]]
		self.draw()
	
	def execute(self, instruction):
		self.clock_tick()
		if instruction != 'noop':
			self.register += int(instruction.split()[1])
			self.clock_tick()
	
	def clock_tick(self):
		self.cycle += 1 
		self.draw()
	
	def draw(self):
		row = int(self.cycle / 40)
		col = self.cycle % 40
		if len(self.display) <= row:
			self.display.append([])
		char = '#' if abs(self.register-col) <= 1 else '.'
		self.display[row].append(char)
		#self.print_display()
	
	def print_display(self):
		for row in self.display:
			print(''.join(row))
		print('')

comm = Communicator()
for line in lines:
	comm.execute(line)
comm.print_display()

