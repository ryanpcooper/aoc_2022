from aoc_util import *

lines = getInput(__file__)

class Dir:
	def __init__(self, parent, path, name):
		self.parent = parent
		self.children = []
		self.path = path
		self.name = name
		self.size = 0
	
	def addChild(self, child):
		self.children.append(child)

class File:
	def __init__(self, path, name, size):
		self.children = []
		self.path = path
		self.name = name
		self.size = size

rootDir = Dir(None, '/', '/')
currentDir = rootDir

for line in lines:
	parts = line.split()
	if parts[0] == '$':
		cmd = parts[1]
		if cmd == 'cd':
			arg = parts[2]
			if arg == '..':
				currentDir = currentDir.parent
			elif arg == '/':
				currentDir = rootDir
			else:
				foundChild = next((x for x in currentDir.children if x.name == arg), None)
				if foundChild == None:
					newDir = Dir(currentDir, currentDir.path + arg + '/', arg)
					currentDir.addChild(newDir)
					currentDir = newDir
				else: 
					currentDir = foundChild
	else: # current dir listing
		name = parts[1]
		foundChild = next((x for x in currentDir.children if x.name == name), None)
		if not foundChild:
			if parts[0] == 'dir':
				newDir = Dir(currentDir, currentDir.path + parts[1] + '/', parts[1])
				currentDir.addChild(newDir)
			else:
				newFile = File(currentDir.path + parts[1], parts[1], int(parts[0]))
				currentDir.addChild(newFile)

def populate_dir_sizes(dir):
	for c in dir.children:
		populate_dir_sizes(c)
	dir.size += sum(transform(dir.children, lambda c: c.size))

populate_dir_sizes(rootDir)

# part 1
THRESHOLD = 100000

def collect_small_dirs(dir, threshold):
	if not dir.path.endswith('/'):
		return [] # it's a file, not a dir
	else:
		small_dirs = []
		for c in dir.children:
			small_dirs += collect_small_dirs(c, threshold)
		if (dir.size <= threshold):
			small_dirs.append(dir)
		return small_dirs
	
small_dirs = collect_small_dirs(rootDir, THRESHOLD)
	
print(sum(transform(small_dirs, lambda d: d.size)))

# part 2
DISK_TOTAL = 70000000
NEEDED_SPACE = 30000000
available_space = DISK_TOTAL - rootDir.size
needed_to_free = NEEDED_SPACE - available_space

def find_smallest_above(dir, threshold, smallest_so_far):
	if (dir.size < smallest_so_far.size and dir.size >= threshold):
		smallest_so_far = dir
	for c in dir.children:
		c_smallest = find_smallest_above(c, threshold, smallest_so_far)
		if (c_smallest.size < smallest_so_far.size and c_smallest.size >= threshold):
			smallest_so_far = c_smallest
	return smallest_so_far
	
best_choice = find_smallest_above(rootDir, needed_to_free, rootDir)
print(best_choice.size)


	