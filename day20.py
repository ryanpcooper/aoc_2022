from aoc_util import *
import numpy as np
import math

lines = getInput(__file__)

class Value:
	def __init__(self, v):
		self.v = int(v)
		
	def __str__(self):
		return str(self.v)
		
	def decrypt(self, key):
		self.v = self.v*key

def mix(initial_vals, vals):
	for v in initial_vals:
		#print("moving " + str(v))
		if v.v == 0:
			continue
		moving_left = v.v < 0
		old_index = vals.index(v)
		vals.remove(v)
		
		amount_to_move = abs(v.v)%len(vals)
		if moving_left:
			new_index = old_index - amount_to_move
		else:
			new_index = old_index + amount_to_move
		target_index = new_index % len(vals)	
		if moving_left:
			if target_index == 0:
				vals = vals + [v] # wrap around to end of list
			else:
				vals = vals[0:target_index] + [v] + vals[target_index:]
		else:
			if target_index == len(vals):
				vals = [v] + vals # wrap around to start of list
			else:
				vals = vals[0:target_index] + [v] + vals[target_index:]
	return vals
	
def extract_coords(vals):
	zeroes = list(filter(lambda v: v.v == 0, vals))
	zero_index = vals.index(zeroes[0])
	answer_1_index = (zero_index + 1000) % len(vals)
	answer_2_index = (zero_index + 2000) % len(vals)
	answer_3_index = (zero_index + 3000) % len(vals)
	return vals[answer_1_index].v + vals[answer_2_index].v + vals[answer_3_index].v

initial_vals = transform(lines, Value)

# part 1
vals = initial_vals.copy()
vals = mix(initial_vals, vals)
print(extract_coords(vals))
print()

# part 2
vals = initial_vals.copy()
DECRYPTION_KEY = 811589153
for v in vals:
	v.decrypt(DECRYPTION_KEY)
for i in range(10):
	vals = mix(initial_vals, vals)
print(extract_coords(vals))


	