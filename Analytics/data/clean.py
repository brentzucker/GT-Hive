import json

filename = '2014-15.json'

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
year = "2015"
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

print json.dumps(buildings)