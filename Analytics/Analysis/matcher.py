import json
import sys
import random
from pprint import pprint

filename = 'April2015_Statistics.json'

f = open(filename)

txt = f.read()

buildings = json.loads(txt)

# Minimize buildings
b = {}
for b_id in buildings.keys():
	b[b_id] = {}
	for date in buildings[b_id]['dates'].keys():
		b[b_id][date] = []
		for hour in sorted(buildings[b_id]['dates'][date]['hours'].keys()):
			b[b_id][date].append(buildings[b_id]['dates'][date]['hours'][hour])

# # # # # # # # # # # # # # #
# Match a building and times
# # # # # # # # # # # # # # #

# arbitrary building input w/ current day
rand_building_id = 0
while rand_building_id not in b.keys():
	rand_building_id = str(random.randint(0, 250)).zfill(3)

rand_hours_length = random.randint(1, 24)
rand_hours = []
for i in range(0, rand_hours_length):
	rand_hours.append(random.randint(0, 1000))

# building_input = {
# 	'b_id' : '166',
# 	'hours' : [300, 220, 140, 80, 50]
# }

building_input = {
	'b_id' : rand_building_id,
	'hours' : rand_hours
}

b_id = building_input['b_id']
hours = building_input['hours']

# Print for testing purposes
for date in sorted(b[b_id].keys()):
	print date
	diff = 0
	for hour in range(0, len(hours)):
		print '\t' + str(b[b_id][date][hour])
		diff += abs(hours[hour] - b[b_id][date][hour])
	print '\t\t' + str(diff)

# Find least different day based off least different unique users at each hour
# rod = rest of day
least_diff, similar_date, rod, predicted_day = sys.maxint, 0, [], []
for date in sorted(b[b_id].keys()):
	diff = 0
	for hour in range(0, len(hours)):
		diff += abs(hours[hour] - b[b_id][date][hour])
	if diff < least_diff:
		least_diff = diff
		similar_date = date
		rod = b[b_id][date][len(hours):]
predicted_day = hours + rod

print similar_date + '  : is most similar date in archive.' 
print str(least_diff) + '  : population pattern differs by.'
print 'Rest of Day:'
print rod
print 'Predicted Day'
print predicted_day