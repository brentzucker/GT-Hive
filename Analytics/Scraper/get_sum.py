# Unique Sum of users for each Building
# Total unique sum for each day (out of curiousity)
# Unique sum for every hour of the day

# To run remotely
# nohup time python get_sum.py > get_sum.out 2> get_sum.err < /dev/null &

# Log Entry Structure
# [0, 1] date
# [2] time
# [3] newdvlana/gtl-mower2
# [4] lawninfo: 
# [5] USER:
# [6] hashed user
# [7] MAC:
# [8] mac address
# [9] SSID:
# [10] GTwifi
# [11] VLAN:
# [12] ### <- vlan number
# [13] IP:
# [14] 0.0.0.0 - 128...
# [15] APMAC
# [16] mac address
# [17] APNAME:
# [18] building-room
# [19] AUTH:
# [20] cache

import gzip
import json
from pprint import pprint

# Contains data for each b_id, date, and hour 
building_dict = {}

# Used for development
test_run = 1000
test = False 

# During test read this specific file
# In production, loop through days, months, etc
year = "2015"
month_first = 1
month_last = 6

for m in range(month_first, month_last):
	month = str(m).zfill(2)
	
	day_first = 1
	day_last = 32
	for d in range(day_first, day_last):
		test_count = 0 # Used for Development
		day = str(d).zfill(2)

		# Unzip file
		path = "/rawdata/wifilogs/%s/lawnmower_%s%s%s.log.gz" % (year, month, day, year)
		contents = [] # Will hold file contents.
		try:
			file = gzip.open(path, "rb")
			contents = file.readlines()
			file.close()
			print path
		except:
			print 'Bad Path: ' + path

		# Read each line of the file
		for line in contents:
			log_entry = line.split()

			# Test so the file doesn't have to be completely read
			if test:
				test_count += 1
				if test_count == test_run:
					break

			# If the log_entry's length != 22 then it's a bad entry
			if len(log_entry) == 21:
				ap_id = log_entry[18]
				ap_array = ap_id.split("-")
				b_id = ap_array[0]

				# Mon-d-Year_hh
				date = month + '-' + day + '-' + year
				hour = log_entry[2][:2]

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
				unique_users.add(log_entry[6])
				building_dict[b_id][date][hour]['users_unique'] = list(unique_users) # Change set to a list because a set can not be converted to json

				# Keep track of unique visitors for date
				unique_users = set(building_dict[b_id][date]['total']['users_unique'])
				unique_users.add(log_entry[6])
				building_dict[b_id][date]['total']['users_unique'] = list(unique_users) # Change set to a list because a set can not be converted to json

				# Count
				building_dict[b_id][date][hour]['count_users'] += 1
				building_dict[b_id][date][hour]['count_users_unique'] = len(building_dict[b_id][date][hour]['users_unique'])
				building_dict[b_id][date]['total']['count_users'] += 1
				building_dict[b_id][date]['total']['count_users_unique'] = len(building_dict[b_id][date]['total']['users_unique'])

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