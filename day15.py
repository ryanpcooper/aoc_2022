from aoc_util import *

lines = getInput(__file__)

class Point: 
	def __init__(self, x, y=None):
		if isinstance(x, str):
			parts = x.split(',')
			self.x = int(parts[0])
			self.y = int(parts[1])
		else:
			self.x = x
			self.y = y
	
	def __eq__(self, p2):
		return self.x == p2.x and self.y == p2.y
	
	def __str__(self):
		return str((self.x, self.y))
	
	def __hash__(self):
		return hash((self.x, self.y))
	
	def copy(self):
		return Point(self.x, self.y)

def parse_point(spec):
	parts = spec.split(', y=')
	return Point(int(parts[0].replace('x=', '')), int(parts[1]))
	
def parse_sensor_beacon_map():
	sensor_beacons = {}
	for line in lines:
		parts = line.split(': closest beacon is at ')
		sensor_spec = parts[0].replace('Sensor at ', '')
		beacon_spec = parts[1]
		sensor_beacons[parse_point(sensor_spec)] = parse_point(beacon_spec)
	return sensor_beacons
	
def get_invalid_x_coords(sensor_beacons, target_row):
	invalid_x_coords = set()
	for sensor in sensor_beacons.keys():
		beacon = sensor_beacons[sensor]
		beacon_x_dist = abs(sensor.x - beacon.x)
		beacon_y_dist = abs(sensor.y - beacon.y)
		beacon_dist = beacon_x_dist + beacon_y_dist
		target_y_dist = abs(sensor.y - target_row)
		target_x_dist = beacon_dist - target_y_dist
		min_x = sensor.x - target_x_dist
		max_x = sensor.x + target_x_dist
		clears = [*range(min_x, max_x)]
		invalid_x_coords = invalid_x_coords.union(set(clears))
	return invalid_x_coords
	
def find_hidden_beacon(sensor_beacons, min_coord, max_coord):
	for y in range(min_coord, max_coord+1):
		invalid_ranges = []
		for sensor in sensor_beacons.keys():
			beacon = sensor_beacons[sensor]
			beacon_x_dist = abs(sensor.x - beacon.x)
			beacon_y_dist = abs(sensor.y - beacon.y)
			beacon_dist = beacon_x_dist + beacon_y_dist
			target_y_dist = abs(sensor.y - y)
			if target_y_dist > beacon_dist:
				continue
			target_x_dist = beacon_dist - target_y_dist
			min_x = sensor.x - target_x_dist
			max_x = sensor.x + target_x_dist
			invalid_ranges.append((min_x, max_x))
		invalid_ranges.sort()
		x_coords_to_check = []
		for rng in invalid_ranges:
			x_coords_to_check.append(rng[0]-1)
			x_coords_to_check.append(rng[0])
			x_coords_to_check.append(rng[0]+1)
			x_coords_to_check.append(rng[1]-1)
			x_coords_to_check.append(rng[1])
			x_coords_to_check.append(rng[1]+1)
		for x in x_coords_to_check:
			if x < min_coord or x > max_coord:
				continue
			found_in_ranges = list(filter(lambda r: r[0] <= x and x <= r[1], invalid_ranges))
			if len(found_in_ranges) == 0:
				print('x=' + str(x) + ',y=' + str(y) + ' not found in ranges:')
				for rng in invalid_ranges:
					print(rng)
				return Point(x, y)
	return None

# part 1
TARGET_ROW = 2000000
#TARGET_ROW = 10
sensor_beacons = parse_sensor_beacon_map()
print(len(get_invalid_x_coords(sensor_beacons, TARGET_ROW)))

# part 2
MIN_COORD = 0
MAX_COORD = 4000000
#MAX_COORD = 20
distress_beacon = find_hidden_beacon(sensor_beacons, MIN_COORD, MAX_COORD)
print(distress_beacon.x*4000000+distress_beacon.y)

