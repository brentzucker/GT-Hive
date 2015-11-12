import json
from pprint import pprint

filename = '../data/2014.json'

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
year = "2014"
for m in range(1, 6):
	month = str(m).zfill(2)
	for d in range(1, 29):
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

# Calculate Median for each day's daytime
for b_id in buildings.keys():
	for date in buildings[b_id]['dates'].keys():
		median = 0
		users_unique = []
		for hour in range(7,20):
			hour = str(hour).zfill(2)
			users_unique.append(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])
		users_unique.sort()
		median = users_unique[len(users_unique) / 4]
		buildings[b_id]['dates'][date]['med_day'] = median

# Calculate Median for each day's nighttime
for b_id in buildings.keys():
	for date in buildings[b_id]['dates'].keys():
		median = 0
		users_unique = []
		for hour in range(0,7):
			hour = str(hour).zfill(2)
			users_unique.append(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])
		for hour in range(20,24):
			hour = str(hour).zfill(2)
			users_unique.append(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])
		users_unique.sort()
		median = users_unique[len(users_unique) / 4]
		buildings[b_id]['dates'][date]['med_night'] = median

# Calculate Average for each day
for b_id in buildings.keys():
	for date in buildings[b_id]['dates'].keys():
		average = 0
		users_unique = []
		for hour in buildings[b_id]['dates'][date]['hours'].keys():
			users_unique.append(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])
		average = sum(users_unique) / len(users_unique)
		buildings[b_id]['dates'][date]['average_users_unique'] = average

# Calculate Average for each daytime
for b_id in buildings.keys():
	for date in buildings[b_id]['dates'].keys():
		average = 0
		users_unique = []
		for hour in range(7, 20):
			hour = str(hour).zfill(2)
			users_unique.append(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])
		average = sum(users_unique) / len(users_unique)
		buildings[b_id]['dates'][date]['average_daytime'] = average

# Calculate Average for each nighttime
for b_id in buildings.keys():
	for date in buildings[b_id]['dates'].keys():
		average = 0
		users_unique = []
		for hour in range(0, 7):
			hour = str(hour).zfill(2)
			users_unique.append(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])
		for hour in range(20, 24):
			hour = str(hour).zfill(2)
			users_unique.append(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])
		average = sum(users_unique) / len(users_unique)
		buildings[b_id]['dates'][date]['average_nighttime'] = average

# Calculate Max for each building
for b_id in buildings.keys():
	max_users_unique = -1
	for date in buildings[b_id]['dates'].keys():
		if buildings[b_id]['dates'][date]['max_users_unique'] > max_users_unique:
			max_users_unique = buildings[b_id]['dates'][date]['max_users_unique']
	buildings[b_id]['max_users_unique'] = max_users_unique

# Calculate percentiles for each building (daytime)
for b_id in buildings.keys():
	users_unique = []
	for date in buildings[b_id]['dates'].keys():
		for hour in range(7,20):
			hour = str(hour).zfill(2)
			users_unique.append(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])
	users_unique.sort()
	buildings[b_id]['p_99'] = users_unique[int(len(users_unique) * .99)]
	buildings[b_id]['p_95'] = users_unique[int(len(users_unique) * .95)]
	buildings[b_id]['p_75'] = users_unique[int(len(users_unique) * .75)]
	buildings[b_id]['p_50'] = users_unique[int(len(users_unique) * .50)]
	buildings[b_id]['p_25'] = users_unique[int(len(users_unique) * .25)]
	buildings[b_id]['p_5'] = users_unique[int(len(users_unique) * .05)]
	buildings[b_id]['p_1'] = users_unique[int(len(users_unique) * .01)]
	buildings[b_id]['iqr'] = buildings[b_id]['p_75'] - buildings[b_id]['p_25']

# Calculate Min for each building
for b_id in buildings.keys():
	min_users_unique = buildings[b_id]['max_users_unique']
	for date in buildings[b_id]['dates'].keys():
		if buildings[b_id]['dates'][date]['min_users_unique'] < min_users_unique:
			min_users_unique = buildings[b_id]['dates'][date]['min_users_unique']
	buildings[b_id]['min_users_unique'] = min_users_unique

# Calculate Min for each building (daytime)
for b_id in buildings.keys():
	min_users_unique = buildings[b_id]['max_users_unique']
	for date in buildings[b_id]['dates'].keys():
		for hour in range(7,20):
			hour = str(hour).zfill(2)
			if buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'] < min_users_unique:
				min_users_unique = buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique']
	buildings[b_id]['min_day'] = min_users_unique

# Calculate Median for each building
for b_id in buildings.keys():
	median = 0
	users_unique = []
	for date in buildings[b_id]['dates'].keys():
		for hour in buildings[b_id]['dates'][date]['hours'].keys():
			users_unique.append(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])
	users_unique.sort()
	median = users_unique[len(users_unique) / 2]
	buildings[b_id]['median_users_unique'] = median

# Calculate Median for each building (daytime)
for b_id in buildings.keys():
	median = 0
	users_unique = []
	for date in buildings[b_id]['dates'].keys():
		for hour in range(7,20):
			hour = str(hour).zfill(2)
			users_unique.append(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])
	users_unique.sort()
	median = users_unique[len(users_unique) / 2]
	buildings[b_id]['med_day'] = median

# Calculate Median for each building (nighttime)
for b_id in buildings.keys():
	median = 0
	users_unique = []
	for date in buildings[b_id]['dates'].keys():
		for hour in range(0,7):
				hour = str(hour).zfill(2)
				users_unique.append(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])
		for hour in range(20,24):
			hour = str(hour).zfill(2)
			users_unique.append(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])
	users_unique.sort()
	median = users_unique[len(users_unique) / 2]
	buildings[b_id]['med_night'] = median

# Calculate Average for each building
for b_id in buildings.keys():
	average = 0
	users_unique = []
	for date in buildings[b_id]['dates'].keys():
		users_unique.append(buildings[b_id]['dates'][date]['average_users_unique'])
	average = sum(users_unique) / len(users_unique)
	buildings[b_id]['average_users_unique'] = average

# Calculate Average for each building (daytime)
for b_id in buildings.keys():
	average = 0
	users_unique = []
	for date in buildings[b_id]['dates'].keys():
		users_unique.append(buildings[b_id]['dates'][date]['average_daytime'])
	average = sum(users_unique) / len(users_unique)
	buildings[b_id]['avg_day'] = average

# Calculate Average for each building (nighttime)
for b_id in buildings.keys():
	average = 0
	users_unique = []
	for date in buildings[b_id]['dates'].keys():
		users_unique.append(buildings[b_id]['dates'][date]['average_nighttime'])
	average = sum(users_unique) / len(users_unique)
	buildings[b_id]['avg_night'] = average

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
if False:
	print json.dumps(buildings_final)

# # Print in order
if True:
	for b_id in sorted(buildings.keys()):
		print '\'' + b_id + '\'' 
		print 'max: ' + str(buildings[b_id]['max_users_unique'])
		print 'p_99: ' + str(buildings[b_id]['p_99'])
		print 'p_95: ' + str(buildings[b_id]['p_95'])
		print 'p_75: ' + str(buildings[b_id]['p_75'])
		print 'p_50: ' + str(buildings[b_id]['p_50'])
		print 'p_25: ' + str(buildings[b_id]['p_25'])
		print 'p_5: ' + str(buildings[b_id]['p_5'])
		print 'p_1: ' + str(buildings[b_id]['p_1'])
		print 'min: ' + str(buildings[b_id]['min_users_unique'])
		print 'iqr: ' + str(buildings[b_id]['iqr'])
		print 'min_day: ' + str(buildings[b_id]['min_day'])
		print 'median: ' + str(buildings[b_id]['median_users_unique'])
		print 'med_day: ' + str(buildings[b_id]['med_day'])
		print 'med_night: ' + str(buildings[b_id]['med_night'])
		print 'average: ' + str(buildings[b_id]['average_users_unique'])
		print 'avg_day: ' + str(buildings[b_id]['avg_day'])
		print 'avg_night: ' + str(buildings[b_id]['avg_night'])
		for date in sorted(buildings[b_id]['dates'].keys()):
			print '\t' + date
			print '\t\t' + 'max: ' + str(buildings[b_id]['dates'][date]['max_users_unique'])
			print '\t\t' + 'min: ' + str(buildings[b_id]['dates'][date]['min_users_unique'])
			print '\t\t' + 'median: ' + str(buildings[b_id]['dates'][date]['median_users_unique'])
			print '\t\t' + 'med day: ' + str(buildings[b_id]['dates'][date]['med_day'])
			print '\t\t' + 'med night: ' + str(buildings[b_id]['dates'][date]['med_night'])
			print '\t\t' + 'average: ' + str(buildings[b_id]['dates'][date]['average_users_unique'])
			print '\t\t' + 'avg day:' + str(buildings[b_id]['dates'][date]['average_daytime'])
			print '\t\t' + 'avg night:' + str(buildings[b_id]['dates'][date]['average_nighttime'])
			for hour in sorted(buildings[b_id]['dates'][date]['hours'].keys()):
				print '\t\t\t' + hour + ': ' + str(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])
			print '\t\t' + 'total: ' + str(buildings[b_id]['dates'][date]['total']['count_users_unique'])