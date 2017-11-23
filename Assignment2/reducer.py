#!/usr/bin/env python3
import sys
import statistics

key = None
current_key = None
tmp_list = []

# input comes from STDIN
for line in sys.stdin:
	# remove leading and trailing whitespace
	line = line.strip()

	# parse the input we got from mapper.py
	key, value = line.split('\t', 1)

	# convert value, currently a string to float
	try:
		value = float(value)
	except ValueError:
		# value was not a number, so silently
		# ignore/discard this line
		continue

	if current_key == key:
		tmp_list.append(value)
	else:
		if current_key:
			# write result to STDOUT
			print('%s\tMax:%s\tMin:%s\tMedian:%s\tStandard Deviation:%s' % (current_key, max(tmp_list), min(tmp_list), statistics.median(tmp_list), statistics.stdev(tmp_list)))
		tmp_list = []
		tmp_list.append(value)
		current_key = key

# do not forget to output the last word if needed!
if current_key == key:
	print('%s\tMax:%s\tMin:%s\tMedian:%s\tStandard Deviation:%s' % (current_key, max(tmp_list), min(tmp_list), statistics.median(tmp_list), statistics.stdev(tmp_list)))
