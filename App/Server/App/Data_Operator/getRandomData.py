import Vehicle_Data
import Vehicle_Tree
import Vehicle_Generator
import random
from random import randint
import numpy as np

roadList = ["NanjingRoad", "BeijingRoad", "ShenzhenRoad", "GuangzhouRoad", "ShanghaiRoad"]
roadNameList = ["Left", "AHead", "Right"]
roadMaxNum = 3
vehicleMaxNum = 10
startDate = "2020-01-23"
endDate = "2020-03-02"
startTime = "00:00:00"
endTime = "23:59:59"

def randomRoad(roadNameList, maxNum):
    roadList = []
    for road in roadNameList:
        for i in range(randint(0, maxNum)):
            roadList.append("{}{}".format(road, i))
    return roadList

def randomData(startDate, endDate, startTime, endTime, vehicle_num_max, time_sample = 15000):
    treedb = Vehicle_Tree.TreeDB('/Share/Main_Data', 'tree.db')
    dateList = Vehicle_Generator.getDateRange(startDate, endDate)
    timeList = Vehicle_Generator.getTimeRange(startTime, endTime)
    timeList = random.sample(timeList, time_sample)

    for road in roadList:
        for date in dateList:
            treedb.insertData(road, date)
            db_path = treedb.findData(road, date)
            indexDB = Vehicle_Data.IndexDB(db_path)
            indexDB.setRoad(randomRoad(roadNameList, roadMaxNum))
            roadLen = len(indexDB.getRoad())
            for time in timeList:
                carList = np.random.randint(vehicle_num_max, size=roadLen)
                busList = np.random.randint(vehicle_num_max, size=roadLen)
                truckList = np.random.randint(vehicle_num_max, size=roadLen)
                indexDB.insertData(carList, busList, truckList, nowTime = time, commitFlag = False)
            indexDB.db.commit()

if __name__ == "__main__":
    randomData(startDate, endDate, startTime, endTime, vehicleMaxNum)