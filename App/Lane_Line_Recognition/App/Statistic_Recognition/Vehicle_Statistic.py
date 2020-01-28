import sqlite3
import threading
import time

import Local_Socket
import Local_Socket_Config

class StatisticThread(threading.Thread):
    def __init__(self, opr, clock_minute):
        threading.Thread(self)
        self.cor = Local_Socket.Correspond(Local_Socket_Config.laneline_yolo_addr1, Local_Socket_Config.laneline_yolo_addr2)
        self.clock_minute = clock_minute
        self.opr = opr

        self.sleepingFlag = False
        self.updatingFlag = False
    
    def run(self):
        startTime = time.time()
        endTime = time.time() + self.clock_minute * 60
        while (True):
            clock_seconds = self.clock_minute * 60
            sleep_seconds = clock_seconds - (startTime - endTime)
            if (sleep_seconds < 0):
                sleep_seconds = 0
            self.sleepingFlag = True
            time.sleep(sleep_seconds)
            self.sleepingFlag = False

            startTime = time.time()

            for roadName in self.opr.roadList:
                cor.send("NeedPredict:{}".format(roadName))
                rec = cor.receive()
                if ("ERROR:" in rec):
                    print("[ERROR]: Road \"{}\" cannot be found".format(roadName))
                else:
                    self.opr.addData(roadName)

            endTime = time.time()

class SQLOperator:
    def __init__(self, statisticDB_path, vehicleDB_path):
        self.sDB = sqlite3.connect(statisticDB_path)
        self.vPath = vehicleDB_path
        self.roadList = []

        roadCursors = self.sDB.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
        for roadCursor in roadCursors:
            self.roadList.append(roadCursor[0])
    
    def addRoad(self, roadName) -> None:
        if (roadName in self.roadList):
            return
        else:
            self.roadList.append(roadName)
            self.sDB.execute("CREATE TABLE {} (X INT NOT NULL, Y INT NOT NULL);".format(roadName))
            return
    
    def addData(self, roadName):
        self.addRoad(roadName)
        db = sqlite3.connect(self.vPath)
        vihicleList = ["car", "bus", "truck"]
        for vihicleName in vihicleList:
            vihicleCursors = db.execute("SELECT * FROM {};".format(vihicleName))
            for vihicleCursor in vihicleCursors:
                (left, right, top, bottom) = vihicleCursor
                pointX = (left + right) / 2
                pointY = (top + bottom) / 2
                self.sDB.execute("INSERT INTO {} VALUES ({}, {});".format(roadName, pointX, pointY))
        db.close()
        self.sDB.commit()