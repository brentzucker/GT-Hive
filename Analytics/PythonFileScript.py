# {
#     b_id: {
#             rooms: [],
#             floors = [],
#             1: [],
#             2: [],
#             .
#             .
#             .
#     },
#     .
#     .
#     .
# }

def getAll():
    myDict = {}
    index = ["05", "06", "07", "08", "09", "10", "11"]
    for i in index:
        f = open("lawnmower_04{0}2015.txt".format(i))
        for line in f:
            try:
                newLine = line.split(", ")
                number = newLine[5].split()
                myEntry = number[3].split("-")
                if myEntry[0] not in list(myDict.keys()):
                    myDict[myEntry[0]] = set([myEntry[1]])
                else:
                    tempList = myDict[myEntry[0]]
                    tempList.add(myEntry[1])
                    myDict[myEntry[0]] = tempList
            except:
                do = "nothing"
        f.close()

    buildings = {}
    for key in list(myDict.keys()):
        buildings[key] = sorted(list(myDict[key]))

    building_list = []
    for b_id in list(buildings.keys()):
        building = {}
        building['b_id'] = b_id;
        building['rooms'] = buildings[b_id]
        building['floors'] = []
        for room in buildings[b_id]:
            floor = "{0}".format(room[0])
            if floor not in building:
                building['floors'].append(floor)
                building[floor] = [room]
            else:
                building[floor].append(room)
        building_list.append(building)

    json = {}
    json['buildings'] = building_list
    print json

getAll()