import threading
import time
import ctypes
import Local_Socket
import Local_Socket_Config

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

class YoloThread(threading.Thread):
    def __init__(self, darknetThread):
        threading.Thread.__init__(self)
        self.yolo_cor = Local_Socket.Correspond(Local_Socket_Config.yolo_video_addr1, Local_Socket_Config.yolo_video_addr2)
        self.darknetThread = darknetThread
    
    def run(self):
        self.yolo_cor.start_send_server()
        while (not self.yolo_cor.start_receive_server()):
            time.sleep(1)
            print("Waiting for connect")
        print("Connected")
        while (True):
            rec = self.yolo_cor.receive()
            if (rec == 'NewImage'):
                self.darknetThread.startPredict()
                while (True):
                    time.sleep(0.2)
                    if (self.darknetThread.hadPredict()):
                        self.darknetThread.cleanPredict()
                        self.yolo_cor.send("HadPredict")
                        break



if __name__ == "__main__":
    darknetThread = DarknetThread('./libyolo.so')
    darknetThread.start()
    yoloThread = YoloThread(darknetThread)
    yoloThread.start()