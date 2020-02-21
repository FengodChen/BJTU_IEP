#! /usr/bin/python3

import sys
sys.path.insert(0, '/App/Hough')
sys.path.insert(0, '/Share/PythonLib')
sys.path.insert(0, '/App/Statistic_Recognition')

import sqlite3
import threading
import time
import numpy as np
import json
import base64

import Local_Socket
import Local_Socket_Config

import Vehicle_Tree
import Vehicle_Data
import Vehicle_Generator

import SQLiteOperator

import Log

import HeatMap

logger = Log.Log("/Share/Log/Vehicle_Statistic.log")
    
class SQLOperator:
    def __init__(self, statisticDB_path, vehicleDB_path):
        self.sDB = sqlite3.connect(statisticDB_path, check_same_thread=False)
        self.vPath = vehicleDB_path
        self.roadList = []

        roadCursors = self.sDB.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
        for roadCursor in roadCursors:
            self.roadList.append(roadCursor[0])
    
    def addRoad(self, roadName, commit=True) -> None:
        if (roadName in self.roadList):
            return
        else:
            self.roadList.append(roadName)
            self.sDB.execute("CREATE TABLE {} (X INT NOT NULL, Y INT NOT NULL);".format(roadName))
            if (commit):
                self.sDB.commit()
            return
        
    def removeRoad(self, roadName, commit=True) -> None:
        if (roadName in self.roadList):
            self.roadList.remove(roadName)
            self.sDB.execute("DROP TABLE {};".format(roadName))
            if (commit):
                self.sDB.commit()
    
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

class GetLaneStatisticThread(threading.Thread):
    def __init__(self, statisticDB_path, vehicleDB_path, clock_minute):
        threading.Thread.__init__(self)
        self.send_addr = Local_Socket_Config.laneline_yolo_addr3
        self.recv_addr = Local_Socket_Config.laneline_yolo_addr4
        self.cor = Local_Socket.Correspond(self.send_addr, self.recv_addr)
        self.clock_minute = clock_minute
        self.opr = SQLOperator(statisticDB_path, vehicleDB_path)

        self.sleepingFlag = False
        self.updatingFlag = False
    
    def run(self):
        logger.info("{} Waiting for connect".format(self.send_addr))
        self.cor.start_send_server()
        logger.info("{} Waiting for connect".format(self.recv_addr))
        self.cor.start_receive_server()
        logger.info("{} Connected{}".format(self.send_addr, self.recv_addr))
        startTime = time.time()
        endTime = time.time() + self.clock_minute * 60
        while (True):
            clock_seconds = self.clock_minute * 60
            sleep_seconds = clock_seconds - (startTime - endTime)
            if (sleep_seconds < 0):
                sleep_seconds = 0
            self.sleepingFlag = True
            time.sleep(sleep_seconds)
            while (self.updatingFlag):
                time,sleep(0.1)
            self.sleepingFlag = False

            startTime = time.time()

            for roadName in self.opr.roadList:
                logger.info("NeedPredict: {}".format(roadName))
                self.cor.send("NeedPredict:{}".format(roadName))
                rec = self.cor.receive()
                if ("ERROR:" in rec):
                    logger.error("Road \"{}\" cannot be found".format(roadName))
                else:
                    self.opr.addData(roadName)
                    logger.info("Added: {}".format(roadName))

            endTime = time.time()
    
    def addRoad(self, roadList):
        while (self.updatingFlag or not self.sleepingFlag):
            time.sleep(0.1)
        self.updatingFlag = True
        for roadName in roadList:
            self.opr.addRoad(roadName, False)
        self.opr.sDB.commit()
        self.updatingFlag = False
    
    def removeRoad(self, roadList):
        while (self.updatingFlag or not self.sleepingFlag):
            time.sleep(0.1)
        self.updatingFlag = True
        for roadName in roadList:
            self.opr.removeRoad(roadName, False)
        self.opr.sDB.commit()
        self.updatingFlag = False

class StatisticThread(threading.Thread):
    def __init__(self, laneDB_path, vehicleDB_path, clock_minute):
        threading.Thread.__init__(self)
        self.send_addr = Local_Socket_Config.laneline_yolo_addr1
        self.recv_addr = Local_Socket_Config.laneline_yolo_addr2
        self.cor = Local_Socket.Correspond(self.send_addr, self.recv_addr)
        self.clock_minute = clock_minute

        self.treeDB = Vehicle_Tree.TreeDB("/Share/Main_Data", "tree.db")
        self.gen = Vehicle_Generator.Vehicle_Generator(self.treeDB)
        self.laneArea = SQLiteOperator.LaneAreaOperator(laneDB_path, False, False)
        self.vehicleDB = SQLiteOperator.VehicleOperator(vehicleDB_path, self.laneArea, False, False)
        
        self.roadList = self.laneArea.getRoadList()
        self.roadListTmp = None
    
    def getStatRoadList(self):
        return self.laneArea.getRoadList()
    
    def setRoadList(self, roadList:list):
        self.roadListTmp = roadList
    
    def checkChange(self):
        if (not self.roadListTmp == None):
            self.roadList = self.roadListTmp
            self.roadListTmp = None
    
    def run(self):
        logger.info("{} Waiting for connect".format(self.send_addr))
        self.cor.start_send_server()
        logger.info("{} Waiting for connect".format(self.recv_addr))
        self.cor.start_receive_server()
        logger.info("{} Connected{}".format(self.send_addr, self.recv_addr))

        while (self.roadList == None):
            time.sleep(0.1)

        startTime = time.time()
        endTime = time.time() + self.clock_minute * 60
        while (True):
            clock_seconds = self.clock_minute * 60
            sleep_seconds = clock_seconds - (endTime - startTime)
            if (sleep_seconds < 0):
                sleep_seconds = 0
            time.sleep(sleep_seconds)
            self.checkChange()

            startTime = time.time()

            for roadName in self.roadList:
                nowDate = Vehicle_Tree.getDate()
                nowTime = Vehicle_Tree.getTime()
                #print("NeedPredict: {}".format(roadName))
                self.cor.send("NeedPredict:{}".format(roadName))
                rec = self.cor.receive()
                if ("ERROR:" in rec):
                    logger.error("Road \"{}\" cannot be found".format(roadName))
                else:
                    (sticDict, lane_str) = self.vehicleDB.read(roadName)
                    sticArray = []
                    for name in ["car", "bus", "truck"]:
                        sticArray.append(sticDict[name])
                    # set lane name
                    laneArray = lane_str.split(",")[:-1]
                    self.gen.insertData(roadName, nowDate, nowTime, sticArray, laneArray)
                    logger.info("Added: {}".format(roadName))

            endTime = time.time()

class ServerThread(threading.Thread):
    def __init__(self, statisticThread):
        threading.Thread.__init__(self)
        self.send_addr = Local_Socket_Config.server_laneline_addr2
        self.recv_addr = Local_Socket_Config.server_laneline_addr1
        self.cor = Local_Socket.Correspond(self.send_addr, self.recv_addr)
        self.statisticThread = statisticThread
    
    def run(self):
        logger.info("{} Waiting for connect".format(self.recv_addr))
        self.cor.start_receive_server()
        logger.info("{} Waiting for connect".format(self.send_addr))
        self.cor.start_send_server()
        logger.info("{} Connected{}".format(self.send_addr, self.recv_addr))

        while (True):
            rec = self.cor.receive()
            if ('newDraw:' in rec):
                # TODO
                [title, size, img_bytes_base64_str] = rec.split("<|||||>")
                (w, h) = size.split("x")
                w = int(w)
                h = int(h)
                mg = HeatMap.ManualGetLane(img_bytes_base64_str, w, h)
                while (True):
                    rec = self.cor.receive()
                    if ("manualDraw:" in rec):
                        [title, pointList_json, lane] = rec.split(("<|||||>"))
                        pointList = json.loads(pointList_json)
                        mg.addLane(lane)
                        img_bytes_base64_str = mg.drawMask(pointList)
                        self.cor.send("{}".format(img_bytes_base64_str))
                    elif ("yyy" in rec):
                        pass

if __name__ == "__main__":
    s_path = "/Share/laneline_data/statistic.db"
    l_path = "/Share/laneline_data/laneArea.db"
    v_path = "/Share/vehicle_data/location.db"
    # TODO
    clock_minute = 0.1
    #sticThread = StatisticThread(s_path, v_path, clock_minute)
    sticThread = StatisticThread(l_path, v_path, clock_minute)
    serverThread = ServerThread(sticThread)
    sticThread.start()
    serverThread.start()
    #sticThread.addRoad(roadList)