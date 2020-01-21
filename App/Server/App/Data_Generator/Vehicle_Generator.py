import Vehicle_Data
import Vehicle_Tree
import json
import datetime
import numpy as np

def getDateRange(startDate, endDate, dt = 1):
    dateList = []

    dateStart = datetime.datetime.strptime(startDate, '%Y-%m-%d')
    dateEnd = datetime.datetime.strptime(endDate, '%Y-%m-%d')
     
    while (dateStart <= dateEnd):
        dateList.append(dateStart.strftime('%Y-%m-%d')) 
        dateStart += datetime.timedelta(days=dt)
    
    return dateList

def getTimeRange(startTime, endTime, dt = 1):
    timeList = []

    timeStart = datetime.datetime.strptime(startTime, '%H:%M:%S')
    timeEnd = datetime.datetime.strptime(endTime, '%H:%M:%S')
     
    while (timeStart <= timeEnd):
        timeList.append(timeStart.strftime('%H:%M:%S')) 
        timeStart += datetime.timedelta(seconds=dt)
    
    return timeList

class Vehicle_Generator:
    def __init__(self, treedb):
        '''
        Vehicle_Generator(Vehicle_Tree.TreeDB)
        '''
        self.treeDict = {}
        self.treedb = treedb
    
    def getIndexDB(self, roadName, date):
        '''
        Vehicle_Generator.getIndexDB(str, str) -> str

        Return indexDB path
        '''
        try:
            filePath = self.treedb.findData(roadName, date)
        except:
            return None
        if (filePath == "0"):
            # Have not this data
            return None
        return Vehicle_Data.IndexDB(filePath)
    
    def initData(self, roadName, date):
        '''
        Vehicle_Generator.initData(str, str) -> Successful? True:False

        date:"YYYY-MM-DD"
        '''
        indexDB = self.getIndexDB(roadName, date)
        if (indexDB == None):
            return False

        if (not roadName in self.treeDict):
            self.treeDict[roadName] = {}
        if (not date in self.treeDict[roadName]):
            self.treeDict[roadName][date] = indexDB
        return True
    
    def getData_TimeRange(self, roadName, date, startTime, endTime):
        """
        Vehicle_Generator.getData_TimeRange(str, str, str, str) -> dict

        Time Format:"HH:MM:SS"

        Return sum_dict[Vehicle_Type][Road_Function], type: int
        """
        if (not self.initData(roadName, date)):
            return None
        indexDB = self.treeDict[roadName][date]
        indexDB.initRoadLine()
        sum_array = np.zeros((3, len(indexDB.roadLine)))

        sum_dict = {}
        sum_dict["Car"] = {}
        sum_dict["Bus"] = {}
        sum_dict["Truck"] = {}
        for road in indexDB.roadLine:
            sum_dict["Car"][road] = 0
            sum_dict["Bus"][road] = 0
            sum_dict["Truck"][road] = 0

        sum_array = indexDB.getData_TimeRange(startTime, endTime)

        vehicle_ptr = 0
        for vehicle_type in sum_dict:
            road_ptr = 0
            for road in sum_dict[vehicle_type]:
                sum_dict[vehicle_type][road] = sum_array[vehicle_ptr][road_ptr]
                road_ptr += 1
            vehicle_ptr += 1

        return sum_dict
    
    def getData_DateRange(self, roadName, startDate, endDate, startTime, endTime):
        """
        Vehicle_Generator.getData_DateRange(str, str, str, str, str) -> dict

        Date Format:"YYYY-MM-DD"

        Time Format:"HH:MM:SS"

        Return sum_dict[Date][Vehicle_Type][Road_Function], type: int
        """
        sum_dict = {}
        dateList = getDateRange(startDate, endDate)
        for date in dateList:
            if (self.initData(roadName, date)):
                sum_dict[date] = self.getData_TimeRange(roadName, date, startTime, endTime)
        return sum_dict
    
    def insertData(self, roadName, date, time, vehicleArray, roadArray = None):
        indexPath = self.treedb.findData(roadName, date)
        if (indexPath == "0"):
            self.treedb.insertData(roadName, date)

        if (self.initData(roadName, date)):
            indexDB = self.treeDict[roadName][date]
            if (roadArray != None and roadArray != indexDB.roadLine):
                indexDB.setRoad(roadArray)
                indexDB.initRoadLine(force = True)
            '''
            for vehicle in vehicleArray:
                if (len(vehicle) != len(indexDB.roadLine)):
                    return False
            '''
            indexDB.insertData(vehicleArray[0], vehicleArray[1], vehicleArray[2], nowTime = time)
            return True

        return False


    
    def data2json(self, data):
        return json.dumps(data)
    