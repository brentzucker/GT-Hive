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
	count += 1
	if count == test_run:
		break

	# If the log_entry's length != 22 then it's a bad entry
	if len(log_entry) == 22:
		ap_id = log_entry[19]
		ap_array = ap_id.split("-")
		
		b_id = ap_array[0]
		
		room = ''
		if len(ap_array) > 1:
			room = ap_array[1]
		ap = ''
		if len(ap_array) == 3:
			ap = ap_array[2]

		# Mon-d-Year_hh
		date_hour = log_entry[0] +'-'+ log_entry[2] +'-'+ year +'_'+ log_entry[3][:2]
		date_hour = month +'-'+ day +'-'+ year +'_'+ log_entry[3][:2]


		# Access Points
		if ap_id in ap_dict:
			ap_dict[ap_id] = ap_dict[ap_id] + 1
		else:
			ap_dict[ap_id] = 1

		# Buildings
		if b_id in building_dict:
			building_dict[b_id]['total']['count_users'] += 1

			# Change it to a list because a set can not be converted to json
			unique_users = set(building_dict[b_id]['total']['users_unique'])
			unique_users.add(log_entry[7])
			building_dict[b_id]['total']['users_unique'] = list(unique_users)
			building_dict[b_id]['total']['count_users_unique'] = len(building_dict[b_id]['total']['users_unique'])

		else:
			building_dict[b_id] = {}
			building_dict[b_id]['total'] = {}
			building_dict[b_id]['total']['count_users'] = 1
			building_dict[b_id]['total']['users_unique'] = list(set([log_entry[7]])) # Change it to a list because a set can not be converted to json
			building_dict[b_id]['total']['count_users_unique'] = len(building_dict[b_id]['total']['users_unique'])

		if date_hour in building_dict[b_id]:
			building_dict[b_id][date_hour]['count_users'] += 1
			
			# Change it to a list because a set can not be converted to json
			unique_users = set(building_dict[b_id][date_hour]['users_unique'])
			unique_users.add(log_entry[7])
			building_dict[b_id][date_hour]['users_unique'] = list(unique_users)
			building_dict[b_id][date_hour]['count_users_unique'] = len(building_dict[b_id][date_hour]['users_unique'])
 
		else:
			building_dict[b_id][date_hour] = {}
			building_dict[b_id][date_hour]['count_users'] = 1
			building_dict[b_id][date_hour]['users_unique'] = list(set([log_entry[7]])) # Change it to a list because a set can not be converted to json
			building_dict[b_id][date_hour]['count_users_unique'] = len(building_dict[b_id][date_hour]['users_unique'])

# Print with list of unique users (Proof of Concept)
print '\n\nDictionary (Exhaustive)\n\n'
pprint(building_dict)

# Remove users_unique b/c it's not necessary for output
for b_id in building_dict:
	for date_hour in building_dict[b_id]:
		del building_dict[b_id][date_hour]['users_unique']

print '\n\nDictionary (Abbreviated)\n\n'
# pprint(ap_dict)
pprint(building_dict)


# Output for Application
print '\n\nJSON\n\n'
print(json.dumps(building_dict))