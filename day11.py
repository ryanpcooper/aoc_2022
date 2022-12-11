from aoc_util import *

PRIMES = [2,3,5,7,11,13,17,19,23]

class Item:
	def __init__(self, val):
		# map of prime -> remainder
		self.prime_remainders = {}
		for p in PRIMES:
			self.prime_remainders[p] = val%p
		
	def __add__(self, val):
		other = self.copy()
		for prime, remainder in other.prime_remainders.items():
			new_remainder = (remainder + val) % prime
			other.prime_remainders[prime] = new_remainder
		return other
	
	def __mul__(self, val):
		other = self.copy()
		if isinstance(val, Item): # new = old * old
			for prime, remainder in other.prime_remainders.items():
				new_remainder = (remainder * val.prime_remainders[prime]) % prime
				other.prime_remainders[prime] = new_remainder
		else: 
			for prime, remainder in other.prime_remainders.items():
				new_remainder = (remainder * val) % prime
				other.prime_remainders[prime] = new_remainder
		return other
	
	def __mod__(self, divisor):
		return self.prime_remainders[divisor]
		
	def copy(self):
		other = Item(0)
		other.prime_remainders = self.prime_remainders.copy()
		return other

class Monkey:
	def __init__(self, monkey_spec):
		self.id           = monkey_spec[0].split()[1][:-1] # 'Monkey 2:' -> '2'
		self.items        = transform(monkey_spec[1].split(': ')[1].split(', '), int)
		self.op           = monkey_spec[2].split('Operation: ')[1]
		self.test         = int(monkey_spec[3].split('divisible by ')[1])
		self.true_target  = int(monkey_spec[4].split('to monkey ')[1])
		self.false_target = int(monkey_spec[5].split('to monkey ')[1])
		self.inspection_count = 0
	
	def monkey_around(self, monkeys, reduce_worry_level):
		while len(self.items) > 0:
			item = self.items.pop(0)
			old = item
			self.inspection_count += 1
			exec(self.op) # assigns to new
			item = locals()['new']
			if reduce_worry_level:
				item = int(item/3)
			target = self.true_target if item % self.test == 0 else self.false_target
			monkeys[target].items.append(item)
	
	def smarten_up(self):
		self.items = transform(self.items, Item)
	
def monkey_business(monkeys):
	inspection_counts = transform(monkeys, lambda m: m.inspection_count)
	max_1 = max(inspection_counts)
	inspection_counts.remove(max_1)
	max_2 = max(inspection_counts)
	return max_1 * max_2
	
lines = getInput(__file__)
monkey_specs = split(lines, '')


# part 1
monkeys = transform(monkey_specs, Monkey)
for i in range(0, 20):
	for monkey in monkeys:
		monkey.monkey_around(monkeys, True)
print(monkey_business(monkeys))

# part 2
monkeys = transform(monkey_specs, Monkey)
for monkey in monkeys:
	monkey.smarten_up()
for i in range(0, 10000):
	for monkey in monkeys:
		monkey.monkey_around(monkeys, False)
print(monkey_business(monkeys))

