def getAll():
    myDict = {}
    index = ["05", "06", "07", "08", "09", "10", "11"]
    index = ["05"]
    for i in index:
        f = open("lawnmower_04{0}2015.txt".format(i))
        for line in f:
           newLine = line.split(",")
            number = newLine[5].split()
            myEntry = number[3].split("-")
            if myEntry[0] not in list(myDict.keys()):
                myDict[myEntry[0]] = set([myEntry[1]])
            else:
                tempList = myDict[myEntry[0]]
                tempList.add(myEntry[1])
                myDict[myEntry[0]] = tempList
        f.close()

    # Print dict
    for key in list(myDict.keys()):
        curStr = key
        curList = sorted(list(myDict[key]))
        for item in curList:
            curStr = curStr + " " + item
        print curStr

getAll()