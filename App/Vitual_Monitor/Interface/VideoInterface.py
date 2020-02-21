#! /usr/bin/python3

import sys
sys.path.insert(0, '/Share/PythonLib')

import cv2 as cv
import numpy as np
import base64
import time
import threading
import Local_Socket
import Local_Socket_Config
import Log
import os
import copy

logger = Log.Log("/Share/Log/Vitual_Monitor.log")

class VideoOperator:
    def __init__(self):
        self.loaded = {}
        self.video_base64 = {}
        self.frame_num = {}
        self.frame_rate = {}
        self.frame_time = {}
    
    def loadVideo(self, video_path) -> bool:
        road_name = video_path.split("/")[-1].split(".")[-2]
        self.loaded[road_name] = False
        video = cv.VideoCapture(video_path)

        self.frame_num[road_name] = int(video.get(cv.CAP_PROP_FRAME_COUNT))
        if (self.frame_num[road_name] == 0):
            del(self.loaded[road_name])
            del(self.frame_num[road_name])
            return False

        self.frame_rate[road_name] = video.get(cv.CAP_PROP_FPS)
        self.frame_time[road_name] = self.frame_num[road_name] / self.frame_rate[road_name]

        self.video_base64[road_name] = []

        logger.info("Loading Video")
        for tmp in range(self.frame_num[road_name]):
            (ret, frame) = video.read()
            (is_succ, img_jpg) = cv.imencode(".jpg", frame)
            jpg_bin = img_jpg.tobytes()
            jpg_base64 = base64.encodebytes(jpg_bin)
            self.video_base64[road_name].append(jpg_base64)
        logger.info("Loaded")

        video.release()
        self.loaded[road_name] = True
        return True
    
    def getPtr(self, road_name, video_time_sec) -> int:
        video_time_ms = int(video_time_sec * 1000)
        frame_time_ms = int(self.frame_time[road_name] * 1000)
        if (video_time_ms > frame_time_ms):
            video_time_ms = video_time_ms % frame_time_ms
        video_time_sec = video_time_ms / 1000
        video_ptr = video_time_sec * self.frame_rate[road_name]
        return int(video_ptr)
    
    def getFrame_base64(self, road_name, video_time_sec) -> str:
        return self.video_base64[road_name][self.getPtr(road_name, video_time_sec)]
    
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
        logger.info("[Vitual Monitor Receive]{} Waiting for connect".format(self.recv_addr))
        self.correspond.start_receive_server()
        logger.info("[Vitual Monitor Send]{} Waiting for connect".format(self.send_addr))
        self.correspond.start_send_server()
        logger.info("[Vitual Monitor]{} Connected{}".format(self.send_addr, self.recv_addr))
        while (True):
            rec = self.correspond.receive()
            if ("Name:" in rec):
                road_name = rec[5:]
                if (not road_name in self.videoOperator.video_base64):
                    video_path = "/Share/Vitual_Monitor_Video/{}.mp4".format(road_name)
                    if (not self.videoOperator.loadVideo(video_path)):
                        self.correspond.send("[ERROR]:Not Such A Road")
                        continue
                while (not self.videoOperator.loaded[road_name]):
                    logger.info("Waiting for Loaded")
                    time.sleep(0.2)
                self.correspond.send("[OK]:Road Connected")
                rec = self.correspond.receive()
                if (rec == 'LoopVideo'):
                    if (self.videoOperator.loaded[road_name]):
                        frame_base64 = self.videoOperator.getFrame_base64(road_name, time.time())
                        self.correspond.send(frame_base64)
                elif ("Time:" in rec):
                    time_sec = float(rec[5:])
                    frame_base64 = self.videoOperator.getFrame_base64(road_name, time_sec)
                    self.correspond.send(frame_base64)
            if (rec == 'Road List'):
                roadList = os.listdir("/Share/Vitual_Monitor_Video/")
                roadList_str = ""
                for road in roadList:
                    if (".mp4" == road[-4:]):
                        roadList_str = "{}{},".format(roadList_str, road[:-4])
                self.correspond.send(roadList_str[:-1])


def connectVI(video_opr):
    vms_t = VitualMonitor_Socket_Threading(video_opr, Local_Socket_Config.yolo_monitor_addr2, Local_Socket_Config.yolo_monitor_addr1)
    vms_t.start()

def connectServer(video_opr):
    vms_t1 = VitualMonitor_Socket_Threading(video_opr, Local_Socket_Config.server_monitor_addr2, Local_Socket_Config.server_monitor_addr1)
    vms_t2 = VitualMonitor_Socket_Threading(video_opr, Local_Socket_Config.server_monitor_addr4, Local_Socket_Config.server_monitor_addr3)
    vms_t1.start()
    vms_t2.start()

if __name__ == "__main__":
    video_opr = VideoOperator()
    connectVI(video_opr)
    connectServer(video_opr)