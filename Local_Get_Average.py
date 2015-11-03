from pprint import pprint
import numpy
import datetime
import calendar

myFile = open("lawnmower_04052015.txt")
contents = myFile.readlines()
myFile.close()

monthDict = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
currTimeInterval = -1
ap_dict = {}
totalDayDict = {}
for line in contents:
    log_entry = line.split(" ")

    # [0, 1, 2] datetime
    # [3] newdvlana
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

    month =  monthDict[log_entry[0]]
    day = int(log_entry[1])
    myTime = log_entry[2].split(":")
    hour = int(myTime[0])
    minute = int(myTime[1])
    second = int(myTime[2])
    curTime = datetime.datetime(2015,month,day,hour,minute, second)
    EpochTime = calendar.timegm(curTime.timetuple())

    if currTimeInterval == -1:
        firstTime = EpochTime
        currTimeInterval = EpochTime

    if EpochTime - currTimeInterval > 300:
        for key in list(ap_dict.keys()):
            if key in list(totalDayDict.keys()):
                tempList = totalDayDict[key]
                tempList.append([(currTimeInterval - firstTime) / 300, len(ap_dict[key])])
                totalDayDict[key] = tempList
            else:
                totalDayDict[key] = [[(currTimeInterval - firstTime) / 300, len(ap_dict[key])]]

            ap_dict[key] = set([])
            currTimeInterval = EpochTime

    buildingAndRoom = log_entry[18]    
    if buildingAndRoom in ap_dict:
        ap_dict[buildingAndRoom].add(log_entry[6])
    else:
        ap_dict[buildingAndRoom] = set([log_entry[6]]) 

# Going to print: 0: which 5 minute interval; 1: Length of the set of unique users
# Should be 288 different 5 minute intervals in a day if have a connection at a building beginning at 12am each day
pprint(totalDayDict)
