from aoc_util import *
from dijkstar import Graph, find_path

lines = getInput(__file__)

TIMER_1 = 30
TIMER_2 = 26

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
	if path_state.timer >= TIMER_1:
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
		if new_path_state.timer + cost > TIMER_1:
			mins = TIMER_1 - new_path_state.timer
		new_path_state.timer += mins
		new_path_state.waste += (mins*new_path_state.waste_per_minute)
		new_path_state.waste_per_minute -= valve.rate
		new_path_state.current = valve
		best = find_best_path(valves, new_path_state, least_wasteful_so_far)
		if least_wasteful_so_far == None or best.waste < least_wasteful_so_far.waste:
			least_wasteful_so_far = best
	return least_wasteful_so_far
	
class PathState2:
	def __init__(self, opened, current, timer, pressure, pressure_per_minute):
		self.opened = opened
		self.current = current
		self.timer = timer
		self.pressure = pressure
		self.pressure_per_minute = pressure_per_minute
		
	def copy(self):
		return PathState2(self.opened.copy(), self.current, self.timer, self.pressure, self.pressure_per_minute)
		
	def __str__(self):
		return str(self.opened) + ": " + str(self.pressure) + " (" + str(self.timer) + ", " + str(self.pressure_per_minute)+ ")"
	
class DualPathState:
	def __init__(self, path_state_1, path_state_2, waste, waste_per_min):
		self.path_state_1 = path_state_1
		self.path_state_2 = path_state_2
		self.waste = waste
		self.waste_per_min = waste_per_min
	
	def copy(self):
		return DualPathState(self.path_state_1.copy(), self.path_state_2.copy(), self.waste, self.waste_per_minute)
		
	def __str__(self):
		return str(self.path_state_1) + "; " + str(self.path_state_2) + "; " + str(self.waste) + "; " + str(self.waste_per_minute)
	
def find_best_paths(valves, path_state_1, path_state_2, best_so_far):
	if path_state_1.timer >= TIMER_2 and path_state_2.timer >= TIMER_2:
		return [path_state_1, path_state_2] 
	if len(path_state_1.opened) + len(path_state_2.opened) == len(valves):
		print("Topping Up...")
		remaining_time_1 = TIMER_2 - path_state_1.timer
		path_state_1.timer = TIMER_2
		bonus_pressure_1 = remaining_time_1 * path_state_1.pressure_per_minute
		print(str(path_state_1))
		print("Remaining time: " + str(remaining_time_1))
		print("Bonus pressure: " + str(bonus_pressure_1))
		path_state_1.pressure += bonus_pressure_1
		print("Final presure: " + str(path_state_1.pressure))
		
		remaining_time_2 = TIMER_2 - path_state_2.timer
		path_state_2.timer = TIMER_2
		bonus_pressure_2 = remaining_time_2 * path_state_2.pressure_per_minute
		print(str(path_state_2))
		print("Remaining time: " + str(remaining_time_2))
		print("Bonus pressure: " + str(bonus_pressure_2))
		path_state_2.pressure += bonus_pressure_2
		print("Final presure: " + str(path_state_2.pressure))
		
		return [path_state_1, path_state_2]
	
	# path_state is whichever path is further behind in time; it "goes" next
	path_state = path_state_1
	other_path = path_state_2
	if path_state_2.timer < path_state_1.timer:
		path_state = path_state_2
		other_path = path_state_1
	
	#print("Active Path: " + str(path_state))
	#print("Passive Path: " + str(other_path))
	
	for valve in valves:
		if valve.name in path_state_1.opened or valve.name in path_state_2.opened:
			continue # not a valid next step
		#print("Trying: " + valve.name)
		cost = path_state.current.costs[valve.name]
		new_path_state = path_state.copy()
		new_path_state.opened.append(valve.name)
		mins = cost
		if new_path_state.timer + cost > TIMER_2:
			mins = TIMER_2 - new_path_state.timer
		new_path_state.timer += mins
		new_path_state.pressure += (mins*new_path_state.pressure_per_minute)
		new_path_state.pressure_per_minute += valve.rate
		new_path_state.current = valve
		best = find_best_paths(valves, new_path_state, other_path, best_so_far)
		if best_so_far == None or best[0].pressure + best[1].pressure > best_so_far[0].pressure + best_so_far[1].pressure:
			best_so_far = best
	return best_so_far

valves = transform(lines, parse_valve)
valves_to_open = list(filter(lambda v: v.rate > 0, valves))
valves_to_open.sort(reverse=True, key=lambda v: v.rate) # sort in priority order highest rate first

#print(commaSeparate(transform(valves_to_open, str)))

# populates Valve.costs and Valve.initial_cost for all valves we want to open
graph = Graph()
for valve in valves:
	for destination in valve.destinations:
		graph.add_edge(valve.name, destination, 1)
#print(graph)
for valve in valves_to_open:
	valve.initial_cost = find_path(graph, 'AA', valve.name).total_cost + 1 # +1 to open the value
for valve in valves_to_open:
	for other in valves_to_open:
		if valve.name == other.name:
			continue
		valve.costs[other.name] = find_path(graph, valve.name, other.name).total_cost + 1 # +1 to open the value
	#print(valve)
	#print(valve.initial_cost)
	#print(valve.costs)
valve_map = { valve.name: valve for valve in valves_to_open }

# part 1
max_pressure_per_min = sum(transform(valves_to_open, lambda v: v.rate))
max_pressure = max_pressure_per_min * TIMER_1

least_wasteful_so_far = None
for valve in valves_to_open:
	path_state = PathState([valve.name], valve, valve.initial_cost, valve.initial_cost * max_pressure_per_min, max_pressure_per_min-valve.rate)
	best_path = find_best_path(valves_to_open, path_state, None)
	if least_wasteful_so_far == None or best_path.waste < least_wasteful_so_far.waste:
		least_wasteful_so_far = best_path
		#print("new best: " + str(least_wasteful_so_far))
#print(str(max_pressure))
#print(str(least_wasteful_so_far.waste))
print(str(max_pressure-least_wasteful_so_far.waste))

# part 2
best_so_far = None
for valve_1 in valves_to_open:
	for valve_2 in valves_to_open:
		if valve_2.name == valve_1.name:
			continue
		print("Trying " + str(valve_1) + " and " + str(valve_2))
		
		path_state_1 = PathState2([valve_1.name], valve_1, valve_1.initial_cost, 0, valve_1.rate)
		path_state_2 = PathState2([valve_2.name], valve_2, valve_2.initial_cost, 0, valve_2.rate)
		best_paths = find_best_paths(valves_to_open, path_state_1, path_state_2, None)
		if best_so_far == None or best_paths[0].pressure + best_paths[1].pressure > best_so_far[0].pressure + best_so_far[1].pressure:
			best_so_far = best_paths
			#print("new best: " + str(best_so_far[0]) + ", " + str(best_so_far[1]))
		#else:
			#print("not good enough: " + str(best_paths[0]) + ", " + str(best_paths[1]))
print(str(best_so_far[0].pressure + best_so_far[1].pressure))
