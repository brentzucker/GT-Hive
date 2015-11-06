import json

filename = 'April2015_WifiData.json'

f = open(filename)

txt = f.read()

buildings = json.loads(txt)

# Clean up buildings
for b_id in buildings.keys():
	# Remove Mac Addresses
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

# Move all hours into 'hours' dict
for b_id in buildings.keys():
	for date in buildings[b_id].keys():
		hours = {}
		for hour in buildings[b_id][date].keys():
			if hour != 'total':
				hours[hour] = buildings[b_id][date][hour]
				del buildings[b_id][date][hour]
		buildings[b_id][date]['hours'] = hours

# Calculate Max for each day
for b_id in buildings.keys():
	for date in buildings[b_id].keys():
		max_users_unique = -1
		for hour in buildings[b_id][date]['hours'].keys():
			if buildings[b_id][date]['hours'][hour]['count_users_unique'] > max_users_unique:
				max_users_unique = buildings[b_id][date]['hours'][hour]['count_users_unique']
		buildings[b_id][date]['max_users_unique'] = max_users_unique

for b_id in sorted(buildings.keys()):
	print '\'' + b_id + '\'' 
	for date in sorted(buildings[b_id].keys()):
		print '\t' + date
		print '\t\t' + 'max: ' + str(buildings[b_id][date]['max_users_unique'])
		for hour in sorted(buildings[b_id][date]['hours'].keys()):
			print '\t\t' + hour + ': ' + str(buildings[b_id][date]['hours'][hour]['count_users_unique'])
























