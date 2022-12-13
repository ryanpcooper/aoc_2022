from aoc_util import *

lines = getInput(__file__)

# returns negative if left is less than right, 0 if equal, positive otherwise
# negative means "in order", positive means "out of order"
def packet_compare(left, right):
	if isinstance(left, int) and isinstance(right, int):
		return left - right
	else:
		if isinstance(left, int):
			left = [left]
		if isinstance(right, int):
			right = [right]
		for i in range(0, len(left)):
			if len(right) <= i:
				return 1 # ran out of items in right list
			result = packet_compare(left[i], right[i])
			if result != 0:
				return result
		if len(left) < len(right):
			return -1 # ran out of items in left list
		else:
			return 0 # lists equal length

class Packet:
	def __init__(self, line):
		self.content = eval(line)
		
	def cmp(self, other):
		if other == None:
			return 1
		return packet_compare(self.content, other.content)
		
	def __lt__(self, other):
		return self.cmp(other) < 0
		
	def __le__(self, other):
		return self.cmp(other) <= 0
	
	def __gt__(self, other):
		return self.cmp(other) > 0
		
	def __ge__(self, other):
		return self.cmp(other) >= 0
	
	def __eq__(self, other):
		return self.cmp(other) == 0
	
	def __ne__(self, other):
		return self.cmp(other) != 0
		
	def __str__(self):
		return str(self.content)
		
def create_packet(line):
	if len(line) == 0:
		return None
	else:
		return Packet(line)

# part 1
packet_pairs = split(transform(lines, create_packet), None)
sum = 0
for i in range(0, len(packet_pairs)):
	if packet_pairs[i][0] < packet_pairs[i][1]:
		sum += (i+1)
print(sum)

# part 2
packets = list(filter(lambda p: p != None, transform(lines, create_packet)))
DIVIDERS = [Packet('[[2]]'), Packet('[[6]]')]
packets = packets + DIVIDERS
packets.sort()
print((packets.index(DIVIDERS[0])+1)*(packets.index(DIVIDERS[1])+1))
