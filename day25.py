from aoc_util import *
import time

lines = getInput(__file__)

SNAFU_DIGITS = {
	"2":  2,
	"1":  1,
	"0":  0,
	"-": -1,
	"=": -2
}

def parse_snafu(val):
	total = 0
	for i in range(len(val)):
		c = val[i]
		digit = SNAFU_DIGITS[c]
		place = 5**(len(val)-1-i)
		part = place*digit
		total += part
	return total
	
def get_snafu_number_of_places(val):
	guess = 0
	number_of_places = None
	while number_of_places == None:
		guess += 1
		max = 0
		for i in range(guess):
			max += (2*(5**i))
		if max >= abs(val):
			return guess

def find_first_digit(val, number_of_places):
	place = (5**(number_of_places-1))
	for option in SNAFU_DIGITS.keys():
		guess = ''+option
		for i in range(number_of_places-1):
			guess += '='
		if parse_snafu(guess) <= val:
			return option

def to_snafu(val):
	snafu = ''
	remaining = val
	remaining_number_of_places = get_snafu_number_of_places(val)
	while remaining_number_of_places > 0:
		first_digit = find_first_digit(remaining, remaining_number_of_places)
		place = 5**(remaining_number_of_places-1)
		first_digit_val = SNAFU_DIGITS[first_digit]*place
		snafu += first_digit
		remaining -= first_digit_val
		remaining_number_of_places -= 1
	return snafu

# part 1
sum = 0
for line in lines:
	val = parse_snafu(line)
	sum += val
print(to_snafu(sum))
