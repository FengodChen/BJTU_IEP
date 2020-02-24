import Numpy_String
import sqlite3
import numpy as np

class BaseOperator:
    def __init__(self, db_path, rw, check_same_thread = True):
        self.db = sqlite3.connect(db_path, check_same_thread = check_same_thread)
        self.__rw = rw
    
    def execute(self, order:str):
        self.db.execute(order)
    
    def args2str(self, args):
        arg_str = ""
        for arg in args:
            arg_str = "{}, {}".format(arg_str, arg)
        arg_str = arg_str[1:]
        return arg_str
    
    def createTable(self, table_name, args):
        '''
        args = [value1, value2, ..., valueN]
        '''
        col_str = self.args2str(args)
        self.db.execute("CREATE TABLE IF NOT EXISTS {} ({})".format(table_name, col_str))

    def read(self, table_name, col = "*", condition = None) -> list:
        '''
        col = "column1, column2, ..., columnN" or "*"

        condition is what after "WHERE"
        '''
        list = []

        if (condition == None):
            cursors = self.db.execute("SELECT {} FROM {};".format(col, table_name))
        else:
            cursors = self.db.execute("SELECT {} FROM {} WHERE {};".format(col, table_name, condition))

        for cursor in cursors:
            list.append(cursor)
        
        return list

    def write(self, table_name, args, commit = True):
        '''
        args = [value1, value2, ..., valueN]
        '''
        if (self.__rw):
            args_str = self.args2str(args)
            self.db.execute("INSERT INTO {} VALUES ({});".format(table_name, args_str))
            if (commit):
                self.db.commit()
        else:
            raise Exception("Cannot write because this BaseOperator define db file read-only file")

class LaneAreaOperator(BaseOperator):
    def __init__(self, db_path, rw, check_same_thread=True):
        super().__init__(db_path, rw, check_same_thread=check_same_thread)
        self.__colList = ["RoadName TEXT NOT NULL", "Size TEXT NOT NULL", "Array TEXT NOT NULL", "Lane TEXT NOT NULL"]
    
    def createTable(self):
        super().createTable("Main", self.__colList)
    
    def read(self, roadName) -> (np.array, str):
        (size_str, array_str, lane_str) = super().read("Main", "Size, Array, Lane", "RoadName IS \"{}\"".format(roadName))[0]
        npArray = Numpy_String.str2np(array_str, size_str)
        return (npArray, lane_str)
    
    def write(self, roadName, npArray, lane, commit=True):
        (array_str, size_str) = Numpy_String.np2str(npArray)
        self.createTable()
        super().execute("DELETE FROM Main WHERE roadName is \"{}\";".format(roadName))
        super().write("Main", ["\"{}\"".format(roadName), "\"{}\"".format(size_str), "\"{}\"".format(array_str), "\"{}\"".format((lane))], commit=commit)
    
    def getRoadList(self) -> list:
        roadList = super().read("Main", "RoadName")
        l = len(roadList)
        for ptr in range(l):
            roadList[ptr] = roadList[ptr][0]
        return roadList

class VehicleOperator(BaseOperator):
    def __init__(self, db_path, laneArea_opr, rw=False, check_same_thread=True):
        super().__init__(db_path, rw, check_same_thread=check_same_thread)
        self.vehicleList = ["car", "bus", "truck"]
        self.laneArea_opr = laneArea_opr
    
    def read(self, roadName) -> (dict, str):
        '''
        Return {"car": [r1, r2, ..., rn], "bus": [...], "truck": [...]}
        '''
        locationDict = {}
        (laneArray, lane) = self.laneArea_opr.read(roadName)
        (h, w) = np.shape(laneArray)
        lineNum = np.max(laneArray)
        for vehicleName in self.vehicleList:
            locationDict[vehicleName] = np.zeros(lineNum, dtype=np.uint64)
            locationList = super().read(vehicleName)
            for location in locationList:
                (left, right, top, bottom) = location
                x = int(w * (left + right) / 2)
                y = int(h * (1 - (top + bottom) / 2))
                if (laneArray[y][x] > 0):
                    locationDict[vehicleName][laneArray[y][x] - 1] += 1
        
        return (locationDict, lane)
