import json
from pprint import pprint

filename = 'April2015_WifiData.json'

f = open(filename)

txt = f.read()

buildings = json.loads(txt)

# Clean up buildings
for b_id in buildings.keys():
	# Remove entries with Mac Addresses representing buildings
	if len(b_id.split(":")) == 6:
		del buildings[b_id]
	# Remove weird buildings (i.e. AP0007.7db6.01b8) 
	if len(b_id.split(".")) == 3:
		del buildings[b_id]
	# Remove Rich246_EarlsOffice
	if b_id == "Rich246_EarlsOffice,":
		del buildings[b_id]
	# Remove Survey
	if b_id == "Survey":
		del buildings[b_id]

# Clean dates
# If no one was in a building on a day, the date log does not exist
month = "04"
year = "2015"
for d in range(1, 31):
	day = str(d).zfill(2)
	date = month +'-'+ day +'-'+ year

	for b_id in buildings.keys():
		if date not in buildings[b_id].keys():
			buildings[b_id][date] = {}	

# Clean hours
# If no one was in a building on an hour, the hour log does not exist
for h in range(0, 24):
	hour = str(h).zfill(2)

	for b_id in buildings.keys():
		for date in buildings[b_id].keys():
			if hour not in buildings[b_id][date].keys():
				buildings[b_id][date][hour] = {}
				buildings[b_id][date][hour]['count_users_unique'] = 0
				buildings[b_id][date][hour]['count_users'] = 0
			if 'total' not in buildings[b_id][date]:
				buildings[b_id][date]['total'] = {}
				buildings[b_id][date]['total']['count_users_unique'] = 0

# Move all dates into 'dates' dict
for b_id in buildings.keys():
	dates = {}
	for date in buildings[b_id].keys():
		dates[date] = buildings[b_id][date]
		del buildings[b_id][date]
		buildings[b_id]['dates'] = dates

# Move all hours into 'hours' dict
for b_id in buildings.keys():
	for date in buildings[b_id]['dates'].keys():
		hours = {}
		for hour in buildings[b_id]['dates'][date].keys():
			if hour != 'total':
				hours[hour] = buildings[b_id]['dates'][date][hour]
				del buildings[b_id]['dates'][date][hour]
		buildings[b_id]['dates'][date]['hours'] = hours

# Calculate Max for each day
for b_id in buildings.keys():
	for date in buildings[b_id]['dates'].keys():
		max_users_unique = -1
		for hour in buildings[b_id]['dates'][date]['hours'].keys():
			if buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'] > max_users_unique:
				max_users_unique = buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique']
		buildings[b_id]['dates'][date]['max_users_unique'] = max_users_unique

# Calculate Min for each day
for b_id in buildings.keys():
	for date in buildings[b_id]['dates'].keys():
		min_users_unique = buildings[b_id]['dates'][date]['max_users_unique']
		for hour in buildings[b_id]['dates'][date]['hours'].keys():
			if buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'] < min_users_unique:
				min_users_unique = buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique']
		buildings[b_id]['dates'][date]['min_users_unique'] = min_users_unique

# Calculate Median for each day
for b_id in buildings.keys():
	for date in buildings[b_id]['dates'].keys():
		median = 0
		users_unique = []
		for hour in buildings[b_id]['dates'][date]['hours'].keys():
			users_unique.append(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])
		users_unique.sort()
		median = users_unique[len(users_unique) / 2]
		buildings[b_id]['dates'][date]['median_users_unique'] = median

# Calculate Average for each day
for b_id in buildings.keys():
	for date in buildings[b_id]['dates'].keys():
		average = 0
		users_unique = []
		for hour in buildings[b_id]['dates'][date]['hours'].keys():
			users_unique.append(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])
		average = sum(users_unique) / len(users_unique)
		buildings[b_id]['dates'][date]['average_users_unique'] = average

# Calculate Max for each building
for b_id in buildings.keys():
	max_users_unique = -1
	for date in buildings[b_id]['dates'].keys():
		if buildings[b_id]['dates'][date]['max_users_unique'] > max_users_unique:
			max_users_unique = buildings[b_id]['dates'][date]['max_users_unique']
	buildings[b_id]['max_users_unique'] = max_users_unique

# Calculate Min for each building
for b_id in buildings.keys():
	min_users_unique = buildings[b_id]['max_users_unique']
	for date in buildings[b_id]['dates'].keys():
		if buildings[b_id]['dates'][date]['min_users_unique'] < min_users_unique:
			min_users_unique = buildings[b_id]['dates'][date]['min_users_unique']
	buildings[b_id]['min_users_unique'] = min_users_unique

# Calculate Median for each building
for b_id in buildings.keys():
	median = 0
	users_unique = []
	for date in buildings[b_id]['dates'].keys():
		users_unique.append(buildings[b_id]['dates'][date]['median_users_unique'])
	users_unique.sort()
	median = users_unique[len(users_unique) / 2]
	buildings[b_id]['median_users_unique'] = median

# Calculate Average for each building
for b_id in buildings.keys():
	average = 0
	users_unique = []
	for date in buildings[b_id]['dates'].keys():
		users_unique.append(buildings[b_id]['dates'][date]['average_users_unique'])
	average = sum(users_unique) / len(users_unique)
	buildings[b_id]['average_users_unique'] = average

# Create a reformatted dictionary to export in json
buildings_final = {}
for b_id in sorted(buildings.keys()):
	buildings_final[b_id] = {}
	buildings_final[b_id]['max'] = buildings[b_id]['max_users_unique']
	buildings_final[b_id]['min'] = buildings[b_id]['min_users_unique']
	buildings_final[b_id]['median'] = buildings[b_id]['median_users_unique']
	buildings_final[b_id]['average'] = buildings[b_id]['average_users_unique']
	buildings_final[b_id]['dates'] = {}
	for date in sorted(buildings[b_id]['dates'].keys()):
		buildings_final[b_id]['dates'][date] = {}
		buildings_final[b_id]['dates'][date]['max'] = buildings[b_id]['dates'][date]['max_users_unique']
		buildings_final[b_id]['dates'][date]['min'] = buildings[b_id]['dates'][date]['min_users_unique']
		buildings_final[b_id]['dates'][date]['median'] = buildings[b_id]['dates'][date]['median_users_unique']
		buildings_final[b_id]['dates'][date]['average'] = buildings[b_id]['dates'][date]['average_users_unique']
		buildings_final[b_id]['dates'][date]['total'] = buildings[b_id]['dates'][date]['total']['count_users_unique']
		buildings_final[b_id]['dates'][date]['hours'] = {}
		for hour in sorted(buildings[b_id]['dates'][date]['hours'].keys()):
			buildings_final[b_id]['dates'][date]['hours'][hour] = buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique']

# pprint(buildings_final)
print json.dumps(buildings_final)

# # Print in order
# for b_id in sorted(buildings.keys()):
# 	print '\'' + b_id + '\'' 
# 	print 'max: ' + str(buildings[b_id]['max_users_unique'])
# 	print 'min: ' + str(buildings[b_id]['min_users_unique'])
# 	print 'median: ' + str(buildings[b_id]['median_users_unique'])
# 	print 'average: ' + str(buildings[b_id]['average_users_unique'])
# 	for date in sorted(buildings[b_id]['dates'].keys()):
# 		print '\t' + date
# 		print '\t\t' + 'max: ' + str(buildings[b_id]['dates'][date]['max_users_unique'])
# 		print '\t\t' + 'min: ' + str(buildings[b_id]['dates'][date]['min_users_unique'])
# 		print '\t\t' + 'median: ' + str(buildings[b_id]['dates'][date]['median_users_unique'])
# 		print '\t\t' + 'average: ' + str(buildings[b_id]['dates'][date]['average_users_unique'])
# 		for hour in sorted(buildings[b_id]['dates'][date]['hours'].keys()):
# 			print '\t\t\t' + hour + ': ' + str(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])
# 		print '\t\t' + 'total: ' + str(buildings[b_id]['dates'][date]['total']['count_users_unique'])