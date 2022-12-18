from aoc_util import *

lines = getInput(__file__)

SPACE_SIZE = 24
DIRECTIONS = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
		
space = []
for i in range(SPACE_SIZE):
	space.append([])
	for j in range(SPACE_SIZE):
		space[i].append([])
		for k in range(SPACE_SIZE):
			space[i][j].append(False)

def count_exposed_faces(space, points):
	exposed_faces = 0
	for point in points:
		x, y, z = point
		for d in DIRECTIONS:
			if space[x + d[0]][y + d[1]][z + d[2]] == False:
				exposed_faces += 1
	return exposed_faces

def find_escape_route(space, visited):
	start_size = len(visited)
	to_add = set()
	for point in visited:
		x,y,z = point
		if x == 0 or y == 0 or z == 0 or x == SPACE_SIZE-1 or y == SPACE_SIZE-1 or z == SPACE_SIZE-1:
			return True
		if space[x][y][z] == False:
			for d in DIRECTIONS:
				new_point = (x+d[0], y+d[1], z+d[2])
				to_add.add(new_point)
	new_visited = visited.union(to_add)
	if len(new_visited) == start_size:
		return False
	return find_escape_route(space, visited.union(to_add))

def fill_in_pockets(space):
	for x in range(SPACE_SIZE):
		for y in range(SPACE_SIZE):
			for z in range(SPACE_SIZE):
				point = (x,y,z)
				if not find_escape_route(space, set([point])):
					space[x][y][z] = True


points = transform(lines, lambda l: transform(l.split(','), int))
for point in points:
	x, y, z = point
	space[x][y][z] = True
		
# part 1
print(count_exposed_faces(space, points))

# part 2
fill_in_pockets(space)
print(count_exposed_faces(space, points))