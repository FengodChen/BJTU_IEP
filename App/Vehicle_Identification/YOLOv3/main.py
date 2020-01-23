import threading
import time
import ctypes

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
    
    def hadPredict(self):
        return self.lib.getIntegerValue(self.hadYolo_flag)
        
if __name__ == "__main__":
    darknetThread = DarknetThread('./libyolo.so')
    darknetThread.start()