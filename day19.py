from aoc_util import *
import numpy as np
import math

lines = getInput(__file__)

MAX_ORE_ROBOTS  = 5
MAX_CLAY_ROBOTS = 10
MAX_OBSIDIAN_ROBOTS = 7

ORE      = 0
CLAY     = 1
OBSIDIAN = 2
GEODE    = 3

class Route:
	def __init__(self, blueprint, robots, resources, timer, actions, time_limit):
		self.blueprint = blueprint
		self.robots = robots
		self.resources = resources
		self.timer = timer
		self.actions = actions
		self.time_limit = time_limit
		
	def children(self):
		options = []
		if self.robots[ORE] < MAX_ORE_ROBOTS:
			options.append(ORE)
		if self.robots[CLAY] < MAX_CLAY_ROBOTS:
			options.append(CLAY)
		if self.robots[CLAY] > 0 and self.robots[OBSIDIAN] < MAX_OBSIDIAN_ROBOTS:
			options.append(OBSIDIAN)
		if self.robots[OBSIDIAN] > 0:
			options.append(GEODE)
		if self.resources[OBSIDIAN] >= self.blueprint.costs[GEODE][OBSIDIAN] and self.resources[ORE] >= self.blueprint.costs[GEODE][ORE]:
			options = [GEODE]
		
		children = []
		for r in options:
			children.append(self.create_child(r))
		children = list(filter(lambda c: c != None, children))
		return children
		
	def create_child(self, target_robot):
		if self.timer >= self.time_limit:
			return None
		route = self
		while not route.has_resources(route.blueprint.costs[target_robot]):
			child_resources = route.resources.copy()
			for r in range(4):
				child_resources[r] += route.robots[r] # collect materials
			route = Route(route.blueprint, route.robots.copy(), child_resources, route.timer+1, route.actions.copy() + [None], route.time_limit)
			if route.timer == route.time_limit:
				return route
			
		child_robots = route.robots.copy()
		child_robots[target_robot] += 1
		child_resources = list(np.subtract(route.resources, route.blueprint.costs[target_robot]))
		for r in range(4):
			child_resources[r] += route.robots[r] # collect materials
		child = Route(route.blueprint, child_robots, child_resources, route.timer+1, route.actions.copy() + [target_robot], route.time_limit)
		return child
				
	def has_resources(self, resources):
		for r in range(4):
			if self.resources[r] < resources[r]:
				return False
		return True

class Blueprint:
	def __init__(self, id, costs):
		self.id = id
		self.costs = costs # [oreRobotCosts, clayRobotCosts, ...] where costs = [oreCost, clayCost, obsidianCost]
		self.score = None
		
	def best_result(self, time_limit):
		best_result = 0
		best_route = None
		old_routes = []
		routes = [Route(self, [1,0,0,0], [0,0,0,0], 0, [], time_limit)]
		while len(routes) > 0:
			old_routes = routes
			routes = flatten(transform(old_routes, lambda r: r.children()))
			finished_routes = list(filter(lambda r: r.timer == time_limit, routes))
			if len(finished_routes) > 0:
				best_route_this_round = max(routes, key=lambda r: r.resources[GEODE])
				best_result_this_round = best_route_this_round.resources[GEODE]
				if best_result_this_round > best_result:
					best_result = best_result_this_round
					best_route = best_route_this_round 
		return best_result

def parse_blueprint(line):
	parts = line.split(":")
	id = int(parts[0].replace("Blueprint ", ""))
	parts = parts[1].split(".")
	ore_costs =      [int(parts[0].split()[4]), 0, 0, 0]
	clay_costs =     [int(parts[1].split()[4]), 0, 0, 0]
	obsidian_costs = [int(parts[2].split()[4]), int(parts[2].split()[7]), 0, 0]
	geode_costs =    [int(parts[3].split()[4]), 0, int(parts[3].split()[7]), 0]
	return Blueprint(id, [ore_costs, clay_costs, obsidian_costs, geode_costs])

blueprints = transform(lines, parse_blueprint)

# part 1
score = 0
for blueprint in blueprints:
	best_result = blueprint.best_result(24)
	quality_level = blueprint.id * best_result
	print("Blueprint " + str(blueprint.id) + ": " + str(best_result))
	score += quality_level
print(score)

#part 2
score = 1
for blueprint in blueprints[0:3]:
	best_result = blueprint.best_result(32)
	print("Blueprint " + str(blueprint.id) + ": " + str(best_result))
	score *= best_result
print(score)