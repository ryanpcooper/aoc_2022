from aoc_util import *
import time

ROOT = "root"
HUMAN = "humn"

lines = getInput(__file__)
monkey_map = {}
for line in lines:
	name, op = line.split(": ")
	monkey_map[name] = op

# part 1
def yell(monkey_map, name):
	parts = monkey_map[name].split()
	if len(parts) == 1:
		return int(parts[0])
	else: 
		return int(eval(str(yell(monkey_map, parts[0])) + parts[1] + str(yell(monkey_map, parts[2]))))

print(yell(monkey_map, ROOT))
	
# part 2
def delete_unreferenced(monkey_map, roots):
	to_delete = []
	for name in monkey_map:
		references = list(filter(lambda other: name in monkey_map[other], monkey_map.keys()))
		if len(references) == 0:
			to_delete.append(name)
	for name in to_delete:
		if name in roots:
			continue
		monkey_map.pop(name)

def inline_vars(monkey_map):
	for name in monkey_map:
		val = monkey_map[name]
		if val.isnumeric():
			for other in monkey_map:
				monkey_map[other] = monkey_map[other].replace(name, val)
		elif not contains_solvable_variable(val):
			for other in monkey_map:
				monkey_map[other] = monkey_map[other].replace(name, "( "+val+" )")

def try_to_eval(monkey_map):
	for name in monkey_map:
		calc = monkey_map[name]
		try:
			val = int(eval(calc))
			monkey_map[name] = str(val)
		except NameError:
			pass

def simplify(monkey_map, roots):
	inline_vars(monkey_map)
	try_to_eval(monkey_map)
	delete_unreferenced(monkey_map, roots)

def contains_solvable_variable(op):
	parts = op.split()
	for part in parts:
		if not part.isnumeric() and not part == HUMAN and not part in ['-','+','*','/','(',')']:
			return True
	return False
	
def eval_human_value(expr, guess):
	return int(eval(expr.replace(HUMAN, str(guess))))

root_left  = monkey_map[ROOT].split()[0]
root_right = monkey_map[ROOT].split()[2]
monkey_map.pop(ROOT)
monkey_map.pop(HUMAN)

# while there are outstanding non-humn variables, simplify
while len(list(filter(lambda n: contains_solvable_variable(monkey_map[n]), monkey_map.keys()))) > 0:
	simplify(monkey_map, [root_left, root_right])

guess = 1

left_expression = monkey_map[root_left]
right_expression = monkey_map[root_right]

left_val  = eval_human_value(left_expression, guess)
right_val = eval_human_value(right_expression, guess)

if eval_human_value(left_expression, guess) > eval_human_value(right_expression, guess):
	greater_expr = left_expression
	lesser_expr  = right_expression
else:
	greater_expr = right_expression
	lesser_expr  = left_expression
	
multiple = 1.0
while eval_human_value(greater_expr, guess) > eval_human_value(lesser_expr, guess):
	prev_guess = guess
	guess = int(guess + guess*multiple)
	gval  = eval_human_value(greater_expr, guess)
	lval = eval_human_value(lesser_expr, guess)
	if eval_human_value(greater_expr, guess) < eval_human_value(lesser_expr, guess): # we overshot
		guess = prev_guess # rewind
		multiple = multiple/2 # narrow down the jump between guesses
print(guess)

	


