import sqlite3
import time
import numpy as np

class IndexDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.db = sqlite3.connect(db_path)
        self.roadLine = None
        self.vehicleClass = ['Car', 'Bus', 'Truck']
        self.initRoadLineFlag = False
    
    def initRoadLine(self, force = False):
        '''
        Initialize self.roadLine by reading Table Road.
        '''
        if (self.initRoadLineFlag and not force):
            return
        if (self.hasTable("Road")):
            roadDict = self.getRoad()
            self.roadLine = [0] * len(roadDict)
            for index in roadDict:
                self.roadLine[index] = roadDict[index]
        self.initRoadLineFlag = True
    
    def hasTable(self, tableName):
        '''
        IndexDB.hasTable(str) -> boolean

        Judge if the table exist
        '''
        try:
            self.db.execute("SELECT * FROM {};".format(tableName))
            return True
        except:
            return False
    
    def setRoad(self, roadList):
        '''
        roadList: [roadFunction0, roadFunction1, ...]
        '''
        if (self.hasTable("Road")):
            self.db.execute("DROP TABLE Road;")
        if (self.hasTable("Car")):
            self.db.execute("DROP TABLE Car;")
        if (self.hasTable("Bus")):
            self.db.execute("DROP TABLE Bus;")
        if (self.hasTable("Truck")):
            self.db.execute("DROP TABLE Truck;")
        self.db.execute("CREATE TABLE Road(ID INT NOT NULL, FUNCTION TEXT NOT NULL);")

        roadLine = ""
        for roadFunc in roadList:
            roadLine = "{}, {} INT NOT NULL".format(roadLine, roadFunc)
        self.db.execute("CREATE TABLE Car(TIME TEXT NOT NULL {});".format(roadLine))
        self.db.execute("CREATE TABLE Bus(TIME TEXT NOT NULL {});".format(roadLine))
        self.db.execute("CREATE TABLE Truck(TIME TEXT NOT NULL {});".format(roadLine))
        id = 0
        for roadFunc in roadList:
            self.db.execute("INSERT INTO Road VALUES ({}, \"{}\")".format(id, roadFunc))
            id += 1
        self.db.commit()

    def getRoad(self):
        '''
        IndexDB.getRoad(void) -> {0: roadFunction0, 1: roadFunction1, ...}
        '''
        if (not self.hasTable("Road")):
            return None
        roadDict = {}
        roadList = self.db.execute("SELECT * FROM Road")
        for road in roadList:
            roadDict[int(road[0])] = road[1]
        return roadDict
    
    def insertData(self, carList, busList, truckList, nowTime = None, commitFlag = True):
        '''
        Insert vehicle number which is suit road function data
        '''
        if (nowTime == None):
            nowTime = time.strftime("%H:%M:%S", time.localtime())
        busDB = "INSERT INTO Bus VALUES (\"{}\"".format(nowTime)
        for tmp in busList:
            busDB = "{}, {}".format(busDB, tmp)
        busDB = "{});".format(busDB)

        carDB = "INSERT INTO Car VALUES (\"{}\"".format(nowTime)
        for tmp in carList:
            carDB = "{}, {}".format(carDB, tmp)
        carDB = "{});".format(carDB)

        truckDB = "INSERT INTO Truck VALUES (\"{}\"".format(nowTime)
        for tmp in truckList:
            truckDB = "{}, {}".format(truckDB, tmp)
        truckDB = "{});".format(truckDB)

        self.db.execute(carDB)
        self.db.execute(busDB)
        self.db.execute(truckDB)

        if (commitFlag):
            self.db.commit()
    '''
    def getData(self, s_time):
        ''''''
        IndexDB.getData(str) -> dict

        Return dataDict[Vehicle_Type][Road_Function], type: int
        ''''''
        dataDict = {}
        dataDict["Car"] = {}
        dataDict["Bus"] = {}
        dataDict["Truck"] = {}

        self.initRoadLine()

        for roadFunc in self.roadLine:
            dataDict["Car"][roadFunc] = 0
            dataDict["Bus"][roadFunc] = 0
            dataDict["Truck"][roadFunc] = 0

        carCursors = self.db.execute("SELECT * FROM Car WHERE TIME IS \"{}\"".format(s_time))
        busCursors = self.db.execute("SELECT * FROM Bus WHERE TIME IS \"{}\"".format(s_time))
        truckCursors = self.db.execute("SELECT * FROM Truck WHERE TIME IS \"{}\"".format(s_time))

        for carCursor in carCursors:
            r_ptr = 1
            for roadFunc in self.roadLine:
                dataDict["Car"][roadFunc] += int(carCursor[r_ptr])
                r_ptr += 1
        for busCursor in busCursors:
            r_ptr = 1
            for roadFunc in self.roadLine:
                dataDict["Bus"][roadFunc] += int(busCursor[r_ptr])
                r_ptr += 1
        for truckCursor in truckCursors:
            r_ptr = 1
            for roadFunc in self.roadLine:
                dataDict["Truck"][roadFunc] += int(truckCursor[r_ptr])
                r_ptr += 1

        return dataDict
    '''
    def getData(self, s_time):
        '''
        IndexDB.getData(str) -> array

        Return dataArray[Vehicle_Type][Road_Function], type: int
        [Vehicle_Type] = ["Car", "Bus", "Truck"]
        '''
        self.initRoadLine()

        roadLineLen = len(self.roadLine)
        dataArray = np.zeros((3, roadLineLen), dtype = np.int)

        carCursors = self.db.execute("SELECT * FROM Car WHERE TIME IS \"{}\"".format(s_time))
        busCursors = self.db.execute("SELECT * FROM Bus WHERE TIME IS \"{}\"".format(s_time))
        truckCursors = self.db.execute("SELECT * FROM Truck WHERE TIME IS \"{}\"".format(s_time))

        for carCursor in carCursors:
            carArray = np.array(carCursor[1:], dtype = np.int)
            dataArray[0] += carArray
        for busCursor in busCursors:
            busArray = np.array(busCursor[1:], dtype = np.int)
            dataArray[0] += busArray
        for truckCursor in truckCursors:
            truckArray = np.array(truckCursor[1:], dtype = np.int)
            dataArray[0] += truckArray

        return dataArray
    
    def getData_TimeRange(self, startTime, endTime):
        '''
        IndexDB.getData(str, str) -> array

        Return dataArray[Vehicle_Type][Road_Function], type: int
        [Vehicle_Type] = ["Car", "Bus", "Truck"]
        '''
        self.initRoadLine()

        dataArray = np.zeros((len(self.vehicleClass), len(self.roadLine)), dtype = np.int)

        vehiclePtr = 0
        for vehicleName in self.vehicleClass:
            roadPtr = 0
            for roadName in self.roadLine:
                cursors = self.db.execute("SELECT sum({}) FROM {} WHERE TIME BETWEEN \"{}\" AND \"{}\";".format(roadName, vehicleName, startTime, endTime))
                for cursor in cursors:
                    dataArray[vehiclePtr][roadPtr] += cursor[0]
                roadPtr += 1
            vehiclePtr += 1

        return dataArray
    
