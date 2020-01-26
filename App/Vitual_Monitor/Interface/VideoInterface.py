import cv2 as cv
import numpy as np
import base64
import time
import threading
import Local_Socket
import Local_Socket_Config

class VideoOperator:
    def __init__(self, video_path):
        self.loaded = False
        video = cv.VideoCapture(video_path)
        self.frame_num = int(video.get(cv.CAP_PROP_FRAME_COUNT))
        self.frame_rate = video.get(cv.CAP_PROP_FPS)
        self.frame_time = self.frame_num / self.frame_rate
        self.video = []
        self.video_base64 = []
        print("Loading Video")
        for tmp in range(self.frame_num):
            (ret, frame) = video.read()
            if (ret):
                self.video.append(frame)
                (is_succ, img_jpg) = cv.imencode(".jpg", frame)
                jpg_bin = img_jpg.tobytes()
                jpg_base64 = base64.encodebytes(jpg_bin)
                self.video_base64.append(jpg_base64)
            else:
                break
        print("Loaded")
        video.release()
        self.loaded = True
    
    def getPtr(self, video_time_sec) -> int:
        video_time_ms = int(video_time_sec * 1000)
        frame_time_ms = int(self.frame_time * 1000)
        if (video_time_ms > frame_time_ms):
            video_time_ms = video_time_ms % frame_time_ms
        video_time_sec = video_time_ms / 1000
        video_ptr = video_time_sec * self.frame_rate
        return int(video_ptr)
    
    def getFrame(self, video_time_sec) -> np.array:
        return self.video[self.getPtr(video_time_sec)]

    def getFrame_base64(self, video_time_sec) -> str:
        return self.video_base64[self.getPtr(video_time_sec)]
    
    def reloadVideo(self, video_path):
        self.__init__(video_path)
    
    def decode_afterTrans(self, string_trans) -> bytes:
        '''
        Because after translating, the transted string is "b'xxxxxxxxxxxxxx..."

        So you should let byte_string = b'xxxxxxxxxxxxxxx...' instead byte_string = "b'xxxxxxxxxxxxxxxx..."

        Using eval() to tranfer it!
        '''
        if ("b'" in string_trans):
            byte_string = eval(string_trans)
            b = base64.decodebytes(byte_string)
            return b
        else:
            return None

class VitualMonitor_Socket_Threading(threading.Thread):
    def __init__(self, videoOperator, send_addr, recv_addr):
        threading.Thread.__init__(self)
        self.videoOperator = videoOperator
        #self.correspond = Local_Socket.Correspond(Local_Socket_Config.vitual_monitor_addr1, Local_Socket_Config.vitual_monitor_addr2)
        self.send_addr = send_addr
        self.recv_addr = recv_addr
        self.correspond = Local_Socket.Correspond(send_addr, recv_addr)
    
    def run(self):
        while (not self.correspond.start_receive_server()):
            time.sleep(0.2)
            print("[Vitual Monitor Receive]{} Waiting for connect".format(self.recv_addr))
        print("[Vitual Monitor Send]{} Waiting for connect".format(self.send_addr))
        self.correspond.start_send_server()
        print("[Vitual Monitor]{} Connected{}".format(self.send_addr, self.recv_addr))
        while (True):
            rec = self.correspond.receive()
            while (not self.videoOperator.loaded):
                time.sleep(0.1)
            if (rec == 'LoopVideo'):
                while (True):
                    if (self.videoOperator.loaded):
                        frame_base64 = self.videoOperator.getFrame_base64(time.time())
                        self.correspond.send(frame_base64)
                    time.sleep(0.033)
            elif ("Time:" in rec):
                time_sec = float(rec[5:])
                frame_base64 = self.videoOperator.getFrame_base64(time_sec)
                self.correspond.send(frame_base64)
            elif ("ChangePath:" in rec):
                f_path = rec[11:]
                self.videoOperator.reloadVideo(f_path)
                self.correspond.send("Refreshed")

def connectVI(video_opr):
    vms_t = VitualMonitor_Socket_Threading(video_opr, Local_Socket_Config.yolo_monitor_addr2, Local_Socket_Config.yolo_monitor_addr1)
    vms_t.start()

def connectServer(video_opr):
    vms_t1 = VitualMonitor_Socket_Threading(video_opr, Local_Socket_Config.server_monitor_addr2, Local_Socket_Config.server_monitor_addr1)
    vms_t2 = VitualMonitor_Socket_Threading(video_opr, Local_Socket_Config.server_monitor_addr4, Local_Socket_Config.server_monitor_addr3)
    vms_t1.start()
    vms_t2.start()

if __name__ == "__main__":
    video_path = "/Share/test_video.mp4"
    video_opr = VideoOperator(video_path)
    connectVI(video_opr)
    connectServer(video_opr)