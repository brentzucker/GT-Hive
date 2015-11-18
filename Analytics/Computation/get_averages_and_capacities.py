import json
from datetime import datetime
from pprint import pprint

filename = '../data/2014-15.json'

f = open(filename)

txt = f.read()

buildings = json.loads(txt)

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

building_calculations = {}

# Calculate capacity and averages for each building
for b_id in buildings.keys():
	crowd_level_wk_day = []
	crowd_level_wk_night = []
	crowd_level_wknd_day = []
	crowd_level_wknd_night = []
	
	for date in buildings[b_id]['dates'].keys():
		
		# Weekdays
		if datetime(int(date[-4:]), int(date[0:2]), int(date[3:5])).weekday() < 5:
			
			# Daytime
			for hour in range(8,20):
				hour = str(hour).zfill(2)
				crowd_level_wk_day.append(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])
			
			# Nighttime
			for hour in range(0,8):
				hour = str(hour).zfill(2)
				crowd_level_wk_night.append(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])

			for hour in range(20,24):
				hour = str(hour).zfill(2)
				crowd_level_wk_night.append(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])

		# Weeknights
		if datetime(int(date[-4:]), int(date[0:2]), int(date[3:5])).weekday() >= 5:
			
			# Daytime
			for hour in range(8,20):
				hour = str(hour).zfill(2)
				crowd_level_wknd_day.append(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])
			
			# Nighttime
			for hour in range(0,8):
				hour = str(hour).zfill(2)
				crowd_level_wknd_night.append(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])

			for hour in range(20,24):
				hour = str(hour).zfill(2)
				crowd_level_wknd_night.append(buildings[b_id]['dates'][date]['hours'][hour]['count_users_unique'])
			

	crowd_level_wk_day.sort()
	crowd_level_wk_night.sort()

	# Store calculations in buildings_calculations
	building_calculations[b_id] = {}

	# capacity of each building is the 99th %
	building_calculations[b_id]['capacity'] = crowd_level_wk_day[int(len(crowd_level_wk_day) * .99)]

	building_calculations[b_id]['avg'] = {}

	# remove the bottom 10% and take the average
	top_90_wk_day = crowd_level_wk_day[int(len(crowd_level_wk_day) * .1):]
	top_90_wk_night = crowd_level_wk_night[int(len(crowd_level_wk_night) * .1):]
	top_90_wknd_day = crowd_level_wknd_day[int(len(crowd_level_wknd_day) * .1):]
	top_90_wknd_night = crowd_level_wknd_night[int(len(crowd_level_wknd_night) * .1):]

	building_calculations[b_id]['avg']['wk_d'] = sum(top_90_wk_day) / len(top_90_wk_day)
	building_calculations[b_id]['avg']['wk_n'] = sum(top_90_wk_night) / len(top_90_wk_night)
	building_calculations[b_id]['avg']['wknd_d'] = sum(top_90_wknd_day) / len(top_90_wknd_day)
	building_calculations[b_id]['avg']['wknd_n'] = sum(top_90_wknd_night) / len(top_90_wknd_night)

# pprint(building_calculations)
print json.dumps(building_calculations)