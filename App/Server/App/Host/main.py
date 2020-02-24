#! /usr/bin/python3

import sys
sys.path.insert(0, '/App/Host')
sys.path.insert(0, '/Share/PythonLib')

import threading
import base64
import time
import socketserver
import hashlib
import Connection

import Log

logger = Log.Log("/Share/Log/Host.log")

class LoopMonitor_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.nextFlag = False
        self.strPic_base64 = 'None'
        self.roadName = 'G107'
    
    def __iter__(self):
        return self
    
    def __next__(self):
        self.nextFlag = True
        return self.strPic_base64
    
    def changeRoad(self, roadName:str):
        self.roadName = roadName
    
    def run(self):
        cor = Connection.Connect_Monitor_1()
        # TODO
        while (True):
            while (True):
                cor.send("Name:{}".format(self.roadName))
                res = cor.receive()
                if ("OK" in res):
                    break
            cor.send("LoopVideo")
            while (not self.nextFlag):
                time.sleep(0.001)
            self.strPic_base64 = cor.receive()
            self.nextFlag = False
    
    def decode(self, picString):
        if ("b'" in picString):
            byte_string = eval(picString)
            b = base64.decodebytes(byte_string)
            return b
        else:
            return ""

lm = LoopMonitor_Thread()
lm.start()

class OperateMonitor_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.orderQueue = []
        self.ansDict = {}

    def run(self):
        cor = Connection.Connect_Monitor_2()
        while(True):
            if (len(self.orderQueue) == 0):
                time.sleep(1)
                continue
            (order, key) = self.takeOrder()
            if (order == 'getMonitorList'):
                cor.send('Road List')
                roadList_str = cor.receive()
                self.insertAns(roadList_str, key)
            elif ('peekMonitor:' in order):
                roadName = order[len('peekMonitor:'):]
                while (True):
                    cor.send("Name:{}".format(roadName))
                    logger.debug("peekMonitor:{}".format(roadName))
                    res = cor.receive()
                    logger.debug("Recv:{}".format(res))
                    if ("OK" in res):
                        break
                cor.send("Time:{}".format(time.time()))
                strPic_base64 = cor.receive()
                logger.debug("Recv Img:{}".format(strPic_base64))
                self.insertAns(strPic_base64, key)
    
    def insertOrder(self, order:str, key:int):
        self.orderQueue.append((order, key))
    
    def takeOrder(self) -> (str, int):
        order_key = self.orderQueue.pop(0)
        return order_key
    
    def insertAns(self, ans:str, key:int):
        self.ansDict[key] = ans
    
    def getAns(self, key:int) -> str:
        if (self.finished(key)):
            ans = self.ansDict.pop(key)
            return ans
        else:
            return ""
    
    def finished(self, key:int) -> bool:
        if (key in self.ansDict):
            return True
        else:
            return False

class OperateLaneLine_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.orderQueue = []
        self.ansDict = {}

    def run(self):
        cor = Connection.Connect_LaneLine()
        while (True):
            if (len(self.orderQueue) == 0):
                time.sleep(1)
                continue
            (order, key) = self.takeOrder()
            if ('manualDraw:' in order):
                cor.send(order)
                draw_img = cor.receive()
                self.insertAns(draw_img, key)
            elif ('newDraw:' in order):
                cor.send(order)
                self.insertAns('0', key)
            elif ('saveLane' == order):
                cor.send(order)
                self.insertAns('0', key)

    def insertOrder(self, order:str, key:int):
        self.orderQueue.append((order, key))
    
    def takeOrder(self) -> (str, int):
        order_key = self.orderQueue.pop(0)
        return order_key
    
    def insertAns(self, ans:str, key:int):
        self.ansDict[key] = ans
    
    def getAns(self, key:int) -> str:
        if (self.finished(key)):
            ans = self.ansDict.pop(key)
            return ans
        else:
            return ""
    
    def finished(self, key:int) -> bool:
        if (key in self.ansDict):
            return True
        else:
            return False

om = OperateMonitor_Thread()
ol = OperateLaneLine_Thread()
om.start()
ol.start()

class WebHost(socketserver.BaseRequestHandler):
    def handle(self):
        self.socket = self.request
        self.working_flag = False
        while True:
            (succ, data) = self.recv()
            if (succ):
                rsp = self.operate(data)
                self.send(rsp)
            else:
                continue

    def operate(self, order:str) -> str:
        if (order == 'getVideo'):
            n = next(lm)
            #logger.debug("Next Loop Monitor: {}".format(n))
            return n
        elif ('changeMonitor:' in order):
            roadName = order[len('changeMonitor:'):]
            logger.debug("RoadName: {}".format(roadName))
            return self.changeMonitor(roadName)
        elif ("om:" in order):
            return self.omOrder(order[3:])
        elif ('ol:' in order):
            return self.olOrder(order[3:])
        else:
            return "!"
    
    def getKey(self) -> int:
        return int(time.time()*10000000)
    
    def changeMonitor(self, roadName:str):
        lm.changeRoad(roadName)
        return '0'
    
    def omOrder(self, order:str) -> str:
        key = self.getKey()
        om.insertOrder(order, key)
        while (True):
            if (om.finished(key)):
                return om.getAns(key)
            time.sleep(0.1)
    
    def olOrder(self, order:str):
        key = self.getKey()
        ol.insertOrder(order, key)
        while (True):
            if (ol.finished(key)):
                return ol.getAns(key)
            time.sleep(0.1)
    
    def send(self, data:str) -> (bool, str):
        while (self.working_flag):
            time.sleep(0.1)
        if (not self.working_flag):
            self.working_flag = True

            data_len = len(data)

            data_bytes = bytes(data, 'utf-8')
            data_len_bytes = bytes("0{}".format(str(data_len)), 'utf-8')
            data_md5 = hashlib.md5(data_bytes).hexdigest()

            self.socket.sendall(data_len_bytes)
            self.socket.recv(8096)

            self.socket.sendall(data_bytes)
            rsp_md5_bytes = self.socket.recv(8096)
            rsp_md5 = bytes.decode(rsp_md5_bytes, 'utf-8')

            succeed = True

            if (rsp_md5 == data_md5):
                # Data Currect
                self.socket.sendall(b'0')
                succeed = True
            else:
                # Data Error
                self.socket.sendall(b'1')
                succeed = False

            self.working_flag = False
            return succeed
    
    def recv(self) -> bool:
        while (self.working_flag):
            time.sleep(0.1)
        if (not self.working_flag):
            self.working_flag = True

            self.socket.recv(1)
            time.sleep(0.01)
            data_len_bytes = self.socket.recv(8096)
            self.socket.sendall(b'0')

            data_len = int(bytes.decode(data_len_bytes, 'utf-8'))
            data = ""
            while (data_len > 0):
                data_chip_bytes = self.socket.recv(8096)
                data_chip = bytes.decode(data_chip_bytes, 'utf-8')
                data = "{}{}".format(data, data_chip)
                data_len -= len(data_chip)
            
            data_md5 = hashlib.md5(bytes(data, 'utf-8')).hexdigest()
            data_md5_bytes = bytes(data_md5, 'utf-8')
            
            self.socket.sendall(data_md5_bytes)

            rsp_bytes = self.socket.recv(8096)
            rsp = bytes.decode(rsp_bytes, 'utf-8')

            succeed = True
            if (rsp == '0'):
                succeed = True
            else:
                succeed = False

            self.working_flag = False
            return (succeed, data)

class WebHost_Thread(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
    
    def run(self):
        server = socketserver.ThreadingTCPServer(('127.0.0.1', self.port), WebHost)
        server.serve_forever()

if __name__ == "__main__":
    wt = WebHost_Thread(8097)
    wt.start()