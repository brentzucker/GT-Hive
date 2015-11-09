import json
import sys

filename = 'JanFebMarApr2015_Statistics.json'

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

print json.dumps(b)
# # # # # # # # # # # # # # #
# Match a building and times
# # # # # # # # # # # # # # #

# Find least different day based off least different unique users at each hour
def getPredictionRestOfDay(b_id, hours, test=False):
	# rod = rest of day
	least_diff, similar_date, rod, predicted_day = sys.maxint, 0, [], []
	for date in sorted(b[b_id].keys()):
		if test:
			print date

		diff = 0
		for hour in range(0, len(hours)):
			if test:
				print '\t' + str(b[b_id][date][hour])

			diff += abs(hours[hour] - b[b_id][date][hour])
		
		if test:
			print '\t\t' + str(diff)

		if diff < least_diff:
			least_diff = diff
			similar_date = date
			rod = b[b_id][date][len(hours):]

	if test:
		print similar_date
		print least_diff

	return rod

# Find least different day based off least different unique users at each hour
# Weight most recent values heavier
def getPredictionRestOfDayWeighted(b_id, hours, test=False):
	# rod = rest of day
	least_diff, similar_date, rod, predicted_day = sys.maxint, 0, [], []
	for date in sorted(b[b_id].keys()):
		if test:
			print date

		diff = 0
		for hour in range(0, len(hours)):
			if test:
				print '\t' + str(b[b_id][date][hour])

			weight = hour + 1 # index
			diff += abs(hours[hour] - b[b_id][date][hour]) * weight
		
		if test:
			print '\t\t' + str(diff)

		if diff < least_diff:
			least_diff = diff
			similar_date = date
			rod = b[b_id][date][len(hours):]
	
	if test:
		print similar_date
		print least_diff

	return rod

# Find least different day based off least different unique users at each hour
# Calculate difference as a percentage
def getPredictionRestOfDayPercentage(b_id, hours, test=False):
	# rod = rest of day
	least_diff, similar_date, rod, predicted_day = sys.maxint, 0, [], []
	for date in sorted(b[b_id].keys()):
		if test:
			print date
		
		diff = 0
		for hour in range(0, len(hours)):
			if test:
				print '\t' + str(b[b_id][date][hour])
			
			diff += abs(hours[hour] - b[b_id][date][hour]) / float(hours[hour])
		
		if test:
			print '\t\t' + str(diff)
		
		if diff < least_diff:
			least_diff = diff
			similar_date = date
			rod = b[b_id][date][len(hours):]
	
	if test:
		print similar_date
		print least_diff
	
	return rod

# Find least different day based off least different unique users at each hour
# Calculate difference as a percentage
def getPredictionRestOfDayPercentageWeighted(b_id, hours, test=False):
	# rod = rest of day
	least_diff, similar_date, rod, predicted_day = sys.maxint, 0, [], []
	for date in sorted(b[b_id].keys()):
		if test:
			print date
		
		diff = 0
		for hour in range(0, len(hours)):
			if test:
				print '\t' + str(b[b_id][date][hour])
			
			weight = hour + 1 # index
			diff += weight * abs(hours[hour] - b[b_id][date][hour]) / float(hours[hour])
		
		if test:
			print '\t\t' + str(diff)
		
		if diff < least_diff:
			least_diff = diff
			similar_date = date
			rod = b[b_id][date][len(hours):]
	
	if test:
		print similar_date
		print least_diff
	
	return rod

# Test
building_input = {
	'b_id' : '166',
	'hours' : [300, 220, 140, 80, 50, 40]
}

b_id = building_input['b_id']
hours = building_input['hours']
# print getPredictionRestOfDay(b_id, hours, test=False)
# print getPredictionRestOfDayWeighted(b_id, hours, test=False)
# print getPredictionRestOfDayPercentage(b_id, hours, test=False)
# print getPredictionRestOfDayPercentageWeighted(b_id, hours, test=False)