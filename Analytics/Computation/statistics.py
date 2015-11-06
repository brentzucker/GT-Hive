import json

filename = 'April2015_WifiData.json'

f = open(filename)

txt = f.read()

buildings = json.loads(txt)

# Remove Mac Addresses
for b_id in buildings.keys():
	if len(b_id.split(":")) == 6:
		del buildings[b_id]

for b_id in sorted(buildings.keys()):
	print b_id 
	for date in sorted(buildings[b_id].keys()):
		print '\t' + date
		hours = []
		for hour in sorted(buildings[b_id][date].keys()):
			print '\t\t' + hour + ': ' + str(buildings[b_id][date][hour]['count_users_unique'])