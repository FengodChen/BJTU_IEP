import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import cv2 as cv
import SQLiteOperator

'''
roadName = "G107"
plotArrayX = []
plotArrayY = []

plt.title("Vehicle Track")

con = sqlite3.connect("/home/fengodchen/WorkSpace/BJTU_IEP/Share/laneline_data/statistic.db")
cursors = con.execute("SELECT * FROM {};".format(roadName))
for cursor in cursors:
    (x, y) = cursor
    plotArrayX.append(x)
    plotArrayY.append(1-y)

plt.scatter(plotArrayX, plotArrayY)

plt.show()
'''

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
    def __init__(self, img_path, dt_show = 15, windowsName = "Manual Get"):
        
        self.img_orgi = cv.imread(img_path)
        self.img_mask = self.img_orgi.copy()
        self.img_copy = self.img_orgi.copy()

        (h, w, c) = np.shape(self.img_orgi)
        self.img_flag = np.zeros((h, w), dtype=np.uint8)

        self.pointlist = []
        self.lanelist = []

        self.dt_show = dt_show
        self.level = 0
        self.windowsName = windowsName

    def mouseCall(self, event, x, y, flags, param):
        if (event == cv.EVENT_LBUTTONDOWN):
            #cv.circle(self.img_copy, (x, y), 4, (0, 0, 0), 5)
            self.pointlist.append([x, y])
            if (len(self.pointlist) >= 2):
                cv.line(self.img_copy, tuple(self.pointlist[-2]), tuple(self.pointlist[-1]), (0,255,0), 3)
            cv.imshow(self.windowsName, self.img_copy)
        elif (event == cv.EVENT_RBUTTONDOWN):
            if (len(self.pointlist) >= 3):
                tri = np.array([self.pointlist], dtype=np.int32)
                deep = self.dt_show * self.level
                cv.fillPoly(self.img_mask, tri, (deep) * 3)
                cv.fillPoly(self.img_flag, tri, self.level)
                self.img_copy = self.img_mask.copy()

                self.pointlist.clear()

                cv.imshow(self.windowsName, self.img_copy)

    def getLane(self):
        cv.namedWindow(self.windowsName, cv.WINDOW_NORMAL)
        cv.setMouseCallback(self.windowsName, self.mouseCall)
        cv.imshow(self.windowsName, self.img_copy)
        while (True):
            key = cv.waitKey(1)
            if (key == 27):
                break
            elif (key >= ord("0") and key <= ord("9")):
                self.level = int(chr(key))
        cv.destroyAllWindows()
    
    def save(self, db_path, roadName):
        db = SQLiteOperator.LaneAreaOperator(db_path, True)
        db.write(roadName, self.img_flag)

def getDefaultSQLPath():
    s = "/home/fengodchen/WorkSpace/BJTU_IEP/Share/laneline_data/laneArea.db"
    return s

def getDefaultHeatMap():
    s = HeatMap("G107", "/home/fengodchen/WorkSpace/BJTU_IEP/Share/laneline_data/statistic.db", (544, 960))
    return s

def getDefaultManual():
    m = ManualGetLane("/home/fengodchen/WorkSpace/BJTU_IEP/Share/out.jpg")
    return m
