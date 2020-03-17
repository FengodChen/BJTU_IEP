from random import randint

import numpy as np
import sqlite3
import cv2 as cv
import base64
import SQLiteOperator

class HeatMap:
    def __init__(self, roadName, db_path, img_size=(800, 800), multiple=1):
        '''
        img_size = (w, h)
        '''
        img_size = (int(img_size[0]*multiple), int(img_size[1]*multiple))
        self.img_org = np.zeros(img_size, dtype=np.uint8)

        con = sqlite3.connect(db_path)
        cursors = con.execute("SELECT * FROM {};".format(roadName))
        for cursor in cursors:
            (x, y) = cursor
            x = int(x * img_size[1])
            y = int(y * img_size[0])
            if (self.img_org[y, x] < 255):
                self.img_org[y, x] += 15

        self.img = self.img_org.copy()
    
    def restore(self):
        self.img = self.img_org.copy()
    
    def cvShow(self):
        cv.namedWindow('Heat Map', cv.WINDOW_NORMAL)
        cv.imshow('Heat Map', self.img)
        cv.waitKey(0)
        cv.destroyAllWindows()
    
    def getRectKernel(self, kernel_size):
        kernel = cv.getStructuringElement(cv.MORPH_RECT, kernel_size)
        return kernel
    
    def opening(self, kernel):
        self.img = cv.erode(self.img, kernel)
        self.img = cv.dilate(self.img, kernel)
    
    def threading(self, min_t, max_t):
        (ret, self.img) = cv.threshold(self.img, min_t, max_t, cv.THRESH_BINARY)

class ManualGetLane:
    def __init__(self, roadName, img_bytes_base64_str:str, img_w:int, img_h:int, dt_show = 15):
        self.img_w = img_w
        self.img_h = img_h
        self.roadName = roadName

        img_bytes_base64_bytes = bytes(img_bytes_base64_str, encoding='utf-8')
        img_bytes = base64.decodebytes(img_bytes_base64_bytes)

        img_array = np.frombuffer(img_bytes, dtype=np.uint8)
        self.img_orgi = cv.imdecode(img_array, cv.IMREAD_COLOR)
        self.img_orgi = cv.resize(self.img_orgi, (img_w, img_h))
        self.img_mask = self.img_orgi.copy()

        (h, w, c) = np.shape(self.img_orgi)
        self.img_flag = np.zeros((h, w), dtype=np.uint8)

        self.lanelist = ""
        self.lanedict = {}

        self.randomRGBList = []

        self.dt_show = dt_show
        self.color_level_each = int(255 / dt_show)
        self.level = 0
    
    def getRandomRGB(self):
        while True:
            r = int(randint(0, self.color_level_each) * self.dt_show)
            g = int(randint(0, self.color_level_each) * self.dt_show)
            b = int(randint(0, self.color_level_each) * self.dt_show)
            if (not (r, g, b) in self.randomRGBList):
                self.randomRGBList.append((r, g, b))
                return (r, g, b)

    def drawMask(self, pointList:list) -> str:
        pointlist = []
        for point in pointList:
            pointlist.append([point['x'], point['y']])
        tri = np.array([pointlist], dtype=np.int32)
        cv.fillPoly(self.img_mask, tri, self.getRandomRGB())
        cv.fillPoly(self.img_flag, tri, self.level)
        img_mix = cv.addWeighted(self.img_orgi, 0.3, self.img_mask, 0.7, 0)

        (is_succ, img_bytes) = cv.imencode(".jpg", img_mix)
        img_bytes_base64_bytes = base64.encodebytes(img_bytes.tobytes())
        img_bytes_base64_str = str(img_bytes_base64_bytes, encoding='utf-8')

        return img_bytes_base64_str
    
    def addLane(self, laneName:str):
        self.level += 1
        if (not laneName in self.lanedict):
            self.lanedict[laneName] = 0
        self.lanedict[laneName] += 1
        self.lanelist = "{}{} {},".format(self.lanelist, laneName, self.lanedict[laneName])

    def save(self, db_path):
        db = SQLiteOperator.LaneAreaOperator(db_path, True)
        db.write(self.roadName, self.img_flag, self.lanelist)

def getDefaultSQLPath():
    s = "/home/fengodchen/WorkSpace/BJTU_IEP/Share/laneline_data/laneArea.db"
    return s

def getDefaultHeatMap():
    s = HeatMap("G107", "/home/fengodchen/WorkSpace/BJTU_IEP/Share/laneline_data/statistic.db", (544, 960))
    return s
