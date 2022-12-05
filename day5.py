from aoc_util import *
import re

def build_stack(stack_defs, i):
	start = i*4+1
	end = i*4+2
	stack_def = transform(stack_defs, lambda line: line[start:end].strip())
	stack = list(filter(lambda i: i!= '', stack_def[:-1]))
	stack.reverse()
	return stack

def parse_stacks(stack_defs):
	stacks = []
	for i in range(0,9):
		stacks.append(build_stack(stack_defs, i))
	return stacks

def parse_instruction(instruction_str):
	return transform([instruction_str.split()[i] for i in (1,3,5)], int)

def execute_move_9000(stacks, qty, fr, to):
	for i in range(0, qty):
		stacks[to-1].append(stacks[fr-1].pop())
		
def execute_move_9001(stacks, qty, fr, to):
	stacks[to-1] = stacks[to-1] + stacks[fr-1][-qty:]
	stacks[fr-1] = stacks[fr-1][:-qty]

lines = getInput(__file__)
input_parts = split(lines, '')
stack_defs = input_parts[0]
instruction_defs = input_parts[1]

instructions = transform(instruction_defs, parse_instruction)

# part 1
stacks = parse_stacks(stack_defs)
for i in instructions:
	execute_move_9000(stacks, *i)
print("".join(transform(stacks, lambda s: s[-1])))

# part 2
stacks = parse_stacks(stack_defs)
for i in instructions:
	execute_move_9001(stacks, *i)
print("".join(transform(stacks, lambda s: s[-1])))