import threading
import time
import ctypes
import Local_Socket
import Local_Socket_Config
import cv2 as cv
import base64

class DarknetThread(threading.Thread):
    def __init__(self, lib_path):
        threading.Thread.__init__(self)
        self.lib = ctypes.CDLL(lib_path)
        self.newImg_Flag = self.lib.getIntegerPoint(0)
        self.hadYolo_flag = self.lib.getIntegerPoint(0)
    
    def run(self):
        self.lib.predict_loop(self.newImg_Flag, self.hadYolo_flag)
    
    def startPredict(self):
        self.lib.setIntegerValue(self.newImg_Flag, 1)
    
    def cleanPredict(self):
        self.lib.setIntegerValue(self.hadYolo_flag, 0)
    
    def hadPredict(self):
        return self.lib.getIntegerValue(self.hadYolo_flag)

class MonitorThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.send_addr = Local_Socket_Config.yolo_monitor_addr1
        self.recv_addr = Local_Socket_Config.yolo_monitor_addr2
        self.monitor_cor = Local_Socket.Correspond(self.send_addr, self.recv_addr)
        self.connected = False
    
    def run(self):
        print("{} Waiting for connect".format(self.send_addr))
        self.monitor_cor.start_send_server()
        while (not self.monitor_cor.start_receive_server()):
            time.sleep(1)
            print("{} Waiting for connect".format(self.recv_addr))
        print("{} Connected{}".format(self.send_addr, self.recv_addr))
        self.connected = True

class ServerThread(threading.Thread):
    def __init__(self, darknetThread, monitorThread):
        threading.Thread.__init__(self)
        self.send_addr = Local_Socket_Config.server_yolo_addr2
        self.recv_addr = Local_Socket_Config.server_yolo_addr1
        self.yolo_cor = Local_Socket.Correspond(self.send_addr, self.recv_addr)
        self.darknetThread = darknetThread
        self.monitorThread = monitorThread
    
    def run(self):
        while (not self.yolo_cor.start_receive_server()):
            time.sleep(1)
            print("{} Waiting for connect".format(self.recv_addr))
        print("{} Waiting for connect".format(self.send_addr))
        self.yolo_cor.start_send_server()
        print("{} Connected{}".format(self.send_addr, self.recv_addr))
        while (not self.monitorThread.connected):
            time.sleep(0.1)
        while (True):
            rec = self.yolo_cor.receive()
            if (rec == 'NeedPredict'):
                self.monitorThread.monitor_cor.send("Time:{}".format(time.time()))
                string_trans = self.monitorThread.monitor_cor.receive()
                byte_image = self.decode_image(string_trans)
                self.saveImg(byte_image, "/Share/Images/main.jpg")
                self.darknetThread.startPredict()
                while (True):
                    time.sleep(0.2)
                    if (self.darknetThread.hadPredict()):
                        self.darknetThread.cleanPredict()
                        self.yolo_cor.send("HadPredict")
                        break
    
    def decode_image(self, string_trans) -> bytes:
        if ("b'" in string_trans):
            byte_string = eval(string_trans)
            b = base64.decodebytes(byte_string)
            return b
        else:
            return None
    
    def saveImg(self, byte_image, image_path):
        image_file = open(image_path, "wb")
        image_file.write(byte_image)
        image_file.close()



if __name__ == "__main__":
    darknetThread = DarknetThread('./libyolo.so')
    monitorThread = MonitorThread()
    serverThread = ServerThread(darknetThread, monitorThread)
    darknetThread.start()
    monitorThread.start()
    serverThread.start()