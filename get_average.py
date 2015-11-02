import gzip
from pprint import pprint

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

	# [0, 1, 2, 3] datetime
	# [4] newdvlana
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

	try:
		ap_id = log_entry[19]
		ap_array = ap_id.split("-")
		b_id = ap_array[0]
		room = ap_array[1]
		if len(ap_array) == 3:
			ap = ap_array[2]
		
		if ap_id in ap_dict:
			ap_dict[ap_id] = ap_dict[ap_id] + 1
		else:
			ap_dict[ap_id] = 1

		if b_id in building_dict:
			# building_dict[b_id] = building_dict[b_id] + 1
			building_dict[b_id]['users'].update(log_entry[7])
			building_dict[b_id]['uniqueVisits'] = len(building_dict[b_id].users)

		else:
			# building_dict[b_id] = 1
			building_dict[b_id] = {}
			building_dict[b_id]['users'] = set([log_entry[7]])
			building_dict[b_id]['uniqueVisits'] = len(building_dict[b_id].users)

	except:
		do = 'something'
		# print 'bad'

# pprint(ap_dict)
pprint(building_dict)