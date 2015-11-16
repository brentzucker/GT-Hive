import json 

filenames = {
	'2014.json',
	'2015.json'
}

buildings = {}
for filename in filenames:
	f = open(filename, 'r')

	contents = json.loads(f.read())

	for b_id in contents.keys():
		if b_id not in buildings:
			buildings[b_id] = contents[b_id]
		else:
			for date in contents[b_id].keys():
				buildings[b_id][date] = contents[b_id][date]

print json.dumps(buildings)