import sqlite3
import time

class IndexDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.db = sqlite3.connect(db_path)
        self.roadLine = None
    
    def initRoadLine(self):
        '''
        Initialize self.roadLine by reading Table Road.
        '''
        if (self.hasTable("Road")):
            roadDict = self.getRoad()
            self.roadLine = [0] * len(roadDict)
            for index in roadDict:
                self.roadLine[index] = roadDict[index]
    
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
    
    def insertData(self, carList, busList, truckList, nowTime = None):
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

        self.db.commit()