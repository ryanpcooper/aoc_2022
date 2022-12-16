from aoc_util import *
from dijkstar import Graph, find_path

lines = getInput(__file__)

class Valve:
	def __init__(self, name, rate, destinations):
		self.name = name
		self.rate = rate
		self.destinations = destinations
		self.initial_cost = 0 # cost to reach this valve from the starting point and open it
		self.costs = {} # map of indirect destination -> cost (and open it)
		
class Path:
	def __init__(self, current, length, score, opened_valves):
		self.length = length
		self.score = score
		self.opened_valves = opened_valves
	
	def visit(valve):
		self.length += 1
	
	def open():
		opened_valves.append(valve)
		score += (valve.rate * (30-2*opened_valves.size))
	
def parse_valve(line):
	parts = line.split(' has flow rate=')
	name = parts[0].replace('Valve ', '')
	parts = parts[1].replace('tunnel leads to valve', 'tunnels lead to valves').split('; tunnels lead to valves ')
	rate = int(parts[0])
	destinations = parts[1].split(', ')
	return Valve(name, rate, destinations)
	
valves = transform(lines, parse_valve)
valves_to_open = list(filter(lambda v: v.rate > 0, valves))
valves_to_open.sort(reverse=True, key=lambda v: v.rate) # sort in priority order highest rate first

# populates Valve.costs and Valve.initial_cost for all valves we want to open
graph = Graph()
for valve in valves:
	for destination in valve.destinations:
		graph.add_edge(valve.name, destination, 1)
print(graph)
for valve in valves_to_open:
	valve.initial_cost = find_path(graph, 'AA', valve.name).total_cost + 1 # +1 to open the value
for valve in valves_to_open:
	for other in valves_to_open:
		if valve.name == other.name:
			continue
		valve.costs[other.name] = find_path(graph, valve.name, other.name).total_cost + 1 # +1 to open the value
		
valve_map = { valve.name: valve for valve in valves_to_open }

max_pressure_per_min = sum(transform(valves_to_open, lambda v: v.rate))
max_pressure = max_pressure_per_min * 30
least_wasteful_so_far = max_pressure

class PathState:
	def __init__(self, opened, current, timer, waste, waste_per_minute):
		self.opened = opened
		self.current = current
		self.timer = timer
		self.waste = waste
		self.waste_per_minute = waste_per_minute
	
	def copy(self):
		return PathState(self.opened.copy(), self.current, self.timer, self.waste, self.waste_per_minute)

def find_best_path(valves, path_state, least_wasteful_so_far):
	if path_state.waste >= least_wasteful_so_far:
		return path_state.waste # no need to keep going, all paths from here are garbage
	if path_state.timer == 30:
		return path_state.waste
	if len(path_state.opened) == len(valves):
		return path_state.waste # all valves are open, no more waste to be calculated
	
	for valve in valves:
		if valve.name in path_state.opened:
			continue # not a valid next step
		cost = path_state.current.costs[valve.name]
		new_path_state = path_state.copy()
		new_path_state.opened.append(valve.name)
		new_path_state.timer += cost
		new_path_state.waste += (cost*new_path_state.waste_per_minute)
		new_path_state.waste_per_minute -= valve.rate
		new_path_state.current = valve
		best = find_best_path(valves, new_path_state, least_wasteful_so_far)
		if best < least_wasteful_so_far:
			least_wasteful_so_far = best
	return least_wasteful_so_far

for valve in valves_to_open:
	path_state = PathState([valve.name], valve, valve.initial_cost, valve.initial_cost * max_pressure_per_min, max_pressure_per_min-valve.rate)
	best_path = find_best_path(valves_to_open, path_state, least_wasteful_so_far)
	if best_path < least_wasteful_so_far:
		least_wasteful_so_far = best_path
		
# part 1
print(str(max_pressure))
print(str(least_wasteful_so_far))
print(str(max_pressure-least_wasteful_so_far))

	

