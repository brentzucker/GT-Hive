# Unique Sum of users for each Building
# Total unique sum for each day (out of curiousity)
# Unique sum for every hour of the day

# To run remotely
# nohup time python get_sum.py > get_sum.out 2> get_sum.err < /dev/null &

# Log Entry Structure
# [0, 1, 2, 3] datetime
# [4] newdvlana/gtl-mower2
# [5] lawninfo: 
# [6] USER:
# [7] hashed user
# [8] MAC:
# [9] mac address
# [10] SSID:
# [11] GTwifi
# [12] VLAN:
# [13] ### <- vlan number
# [14] IP:
# [15] 0.0.0.0 - 128...
# [16] APMAC
# [17] mac address
# [18] APNAME:
# [19] building-room
# [20] AUTH:
# [21] cache

import gzip
import json
from pprint import pprint

# Used for development
test_run = 1000
count = 0

# During test read this specific file
# In production, loop through days, months, etc
year = "2015"
month = "04"
day = "06"
path = "/rawdata/wifilogs/%s/lawnmower_%s%s%s.log.gz" % (year, month, day, year)
file = gzip.open(path, "rb")
contents = file.readlines()
file.close()

ap_dict = {}
building_dict = {}

for line in contents:
	log_entry = line.split(" ")

	# Test so the file doesn't have to be completely read
	# count += 1
	# if count == test_run:
	# 	break

	# If the log_entry's length != 22 then it's a bad entry
	if len(log_entry) == 22:
		ap_id = log_entry[19]
		ap_array = ap_id.split("-")
		
		b_id = ap_array[0]

		# Mon-d-Year_hh
		date = month + '-' + day + '-' + year
		hour = log_entry[3][:2]

		# Buildings
		if b_id not in building_dict:
			building_dict[b_id] = {}

		if date not in building_dict[b_id]:
			building_dict[b_id][date] = {}
			building_dict[b_id][date][hour] = {}
			building_dict[b_id][date][hour]['count_users'] = 0
			building_dict[b_id][date][hour]['users_unique'] = []

			# Keep track of totals for the specific date
			building_dict[b_id][date]['total'] = {}
			building_dict[b_id][date]['total']['count_users'] = 0
			building_dict[b_id][date]['total']['users_unique'] = []

		if hour not in building_dict[b_id][date]:
			building_dict[b_id][date][hour] = {}
			building_dict[b_id][date][hour]['count_users'] = 0
			building_dict[b_id][date][hour]['users_unique'] = []

		# Keep track of unique visitors per hour 	
		unique_users = set(building_dict[b_id][date][hour]['users_unique'])
		unique_users.add(log_entry[7])
		building_dict[b_id][date][hour]['users_unique'] = list(unique_users) # Change set to a list because a set can not be converted to json

		# Keep track of unique visitors for date
		unique_users = set(building_dict[b_id][date]['total']['users_unique'])
		unique_users.add(log_entry[7])
		building_dict[b_id][date]['total']['users_unique'] = list(unique_users) # Change set to a list because a set can not be converted to json

		# Count
		building_dict[b_id][date][hour]['count_users'] += 1
		building_dict[b_id][date][hour]['count_users_unique'] = len(building_dict[b_id][date][hour]['users_unique'])
		building_dict[b_id][date]['total']['count_users'] += 1
		building_dict[b_id][date]['total']['count_users_unique'] = len(building_dict[b_id][date]['total']['users_unique'])

# Print with list of unique users (Proof of Concept)
print '\n\nDictionary (Exhaustive)\n\n'
pprint(building_dict)

# Remove users_unique b/c it's not necessary for output
for b_id in building_dict:
	for date in building_dict[b_id]:
		for hour in building_dict[b_id][date]:
			del building_dict[b_id][date][hour]['users_unique']

print '\n\nDictionary (Abbreviated)\n\n'
pprint(building_dict)

# Output for Application
print '\n\nJSON\n\n'
print(json.dumps(building_dict))