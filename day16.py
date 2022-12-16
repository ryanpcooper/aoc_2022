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
		
	def __str__(self):
		return self.name + ': ' + str(self.rate)

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

print(commaSeparate(transform(valves_to_open, str)))

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
	print(valve)
	print(valve.initial_cost)
	print(valve.costs)
valve_map = { valve.name: valve for valve in valves_to_open }

max_pressure_per_min = sum(transform(valves_to_open, lambda v: v.rate))
max_pressure = max_pressure_per_min * 30

class PathState:
	def __init__(self, opened, current, timer, waste, waste_per_minute):
		self.opened = opened
		self.current = current
		self.timer = timer
		self.waste = waste
		self.waste_per_minute = waste_per_minute
	
	def copy(self):
		return PathState(self.opened.copy(), self.current, self.timer, self.waste, self.waste_per_minute)
		
	def __str__(self):
		return str(self.opened) + ": " + str(self.waste) + " (" + str(self.timer) + ", " + str(self.waste_per_minute)+ ")"

def find_best_path(valves, path_state, least_wasteful_so_far):
	if least_wasteful_so_far != None and path_state.waste >= least_wasteful_so_far.waste:
		return path_state # no need to keep going, all paths from here are garbage
	if path_state.timer >= 30:
		return path_state
	if len(path_state.opened) == len(valves):
		return path_state # all valves are open, no more waste to be calculated
	
	for valve in valves:
		if valve.name in path_state.opened:
			continue # not a valid next step
		cost = path_state.current.costs[valve.name]
		new_path_state = path_state.copy()
		new_path_state.opened.append(valve.name)
		mins = cost
		if new_path_state.timer + cost > 30:
			mins = 30 - new_path_state.timer
		new_path_state.timer += mins
		new_path_state.waste += (mins*new_path_state.waste_per_minute)
		new_path_state.waste_per_minute -= valve.rate
		new_path_state.current = valve
		best = find_best_path(valves, new_path_state, least_wasteful_so_far)
		if least_wasteful_so_far == None or best.waste < least_wasteful_so_far.waste:
			least_wasteful_so_far = best
	return least_wasteful_so_far

least_wasteful_so_far = None
for valve in valves_to_open:
	path_state = PathState([valve.name], valve, valve.initial_cost, valve.initial_cost * max_pressure_per_min, max_pressure_per_min-valve.rate)
	best_path = find_best_path(valves_to_open, path_state, None)
	if least_wasteful_so_far == None or best_path.waste < least_wasteful_so_far.waste:
		least_wasteful_so_far = best_path
		print("new best: " + str(least_wasteful_so_far))
		
# part 1
print(str(max_pressure))
print(str(least_wasteful_so_far.waste))
print(str(max_pressure-least_wasteful_so_far.waste))

	

