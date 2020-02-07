import sys
import threading
import base64
import time
sys.path.insert(0, '/Share/PythonLib')
sys.path.insert(0, '/App/Connect_Operator')

import Connection
#import App.Server.App.Connect_Operator.Connection as Connection
class LoopMonitor:
    def __init__(self):
        self.cor = Connection.Connect_Monitor_1()
        self.cor.send("Name:G107")
        recv = self.cor.receive()
        if ("OK" in recv):
            self.cor.send("LoopVideo")
    
    def __iter__(self):
        return self
    
    def __next__(self):
        string_trans = self.cor.receive()
        return self.decode(string_trans)
    
    def decode(self, picString):
        if ("b'" in picString):
            byte_string = eval(picString)
            b = base64.decodebytes(byte_string)
            return b
        else:
            return ""

class OperateMonitor:
    def __init__(self):
        cor = Connection.Connect_Monitor_2()

class OperateLaneLine:
    def __init__(self):
        self.cor = Connection.Connect_LaneLine()

class LoopMonitor_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.flag = 1
        self.bytePic = None
    
    def __iter__(self):
        return self
    
    def __next__(self):
        while (self.flag):
            time.sleep(0.1)
        self.flag = 1
        return self.bytePic
    
    def run(self):
        cor = Connection.Connect_Monitor_1()
        # TODO
        cor.send("G107")
        cor.send("LoopVideo")
        while (True):
            if (self.flag == 1):
                string_trans = cor.receive()
                self.bytePic = self.decode(string_trans)
    
    def decode(self, picString):
        if ("b'" in picString):
            byte_string = eval(picString)
            b = base64.decodebytes(byte_string)
            return b
        else:
            return ""

class OperateMonitor_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        cor = Connection.Connect_Monitor_2()

class OperateLaneLine_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        cor = Connection.Connect_LaneLine()

loopMonitor = LoopMonitor()
operateMonitor = OperateMonitor()
operateLaneLine = OperateLaneLine()