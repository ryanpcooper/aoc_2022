from aoc_util import *

ROOT = "root"
HUMAN = "humn"

lines = getInput(__file__)
monkey_map = {}
for line in lines:
	name, op = line.split(": ")
	monkey_map[name] = op

def yell(monkey_map, name):
	parts = monkey_map[name].split()
	if len(parts) == 1:
		return int(parts[0])
	else: 
		return int(eval(str(yell(monkey_map, parts[0])) + parts[1] + str(yell(monkey_map, parts[2]))))

def eval_human_value(monkey_map, guess):
	monkey_map[HUMAN] = str(guess)
	return yell(monkey_map, ROOT)

# part 1
print(yell(monkey_map, ROOT))
	
# part 2
root_left  = monkey_map[ROOT].split()[0]
root_right = monkey_map[ROOT].split()[2]
monkey_map[ROOT] = root_left + " - " + root_right
if eval_human_value(monkey_map, 1) < 0:
	monkey_map[ROOT] = root_right + " - " + root_left

guess = 1
multiple = 1.0
while eval_human_value(monkey_map, guess) > 0:
	prev_guess = guess
	guess = int(guess + guess*multiple)
	if eval_human_value(monkey_map, guess) < 0: # we overshot
		guess = prev_guess # rewind
		multiple = multiple/2 # narrow down the jump between guesses
		
# multiple values satisfy the equation but AoC wants the lowest correct answer
for i in range(prev_guess+1, guess):
	if eval_human_value(monkey_map, i) == 0:
		guess = i
		break
	
print(guess)

	


