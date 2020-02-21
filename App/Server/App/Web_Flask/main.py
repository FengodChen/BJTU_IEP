from flask import Flask, redirect, render_template, request, url_for, Response
from WebLib import *
import json
import time
import base64

def setLabel(text:str, setStr:str, label:str) -> str:
    tmp = ""
    label_str = "<{}>{}</{}>".format(label, setStr, label)
    sp = text.split(setStr)
    for s in sp[:-1]:
        tmp = "{}{}{}".format(tmp, s, label_str)
    tmp = "{}{}".format(tmp, sp[-1])
    return tmp

app = Flask(__name__)
sql_gen = sqliteData.Generator()
sk = socketConnect.HostConnection('127.0.0.1', 8097)

monitor_image = b"None"

def Send(data:str) -> None:
    succ = False
    while (not succ):
        succ = sk.send(data)

def Recv() -> str:
    succ = False
    data = None
    while (not succ):
        (succ, data) = sk.recv()
    return data

def SafeSend(data:str) -> str:
    Send(data)
    return Recv()

print("Threading")

def decodeBase64Img(img:str) -> bytes:
    if ("b'" in img):
        byte_string = eval(img)
        byte_pic = base64.decodebytes(byte_string)
        return byte_pic
    else:
        return b'0'

def getMonitorImg() -> bytes:
    byte_pic = b'0'
    while (True):
        Send("getVideo")
        strPic_base64 = Recv()
        byte_pic = decodeBase64Img(strPic_base64)
        if (not byte_pic == b'0'):
            break
        time.sleep(0.1)
    return byte_pic

def frameGen():
    while (True):
        time.sleep(0.033)
        byte_pic = getMonitorImg()
        frame = b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + byte_pic + b'\r\n'
        yield frame

@app.route('/')
def mainWeb():
    return "<h1>Hello Main</h1>"

@app.route('/monitor')
def monitor():
    Send('getMonitorList')
    monitorStr = Recv()
    return "<p>{}</p>".format(monitorStr)

@app.route('/change/<roadName>')
def change(roadName):
    Send('changeMonitor:'.format(roadName))
    monitorStr = Recv()
    return monitorStr

@app.route('/searchRoad')
def searchRoad():
    return render_template('searchRoad.html')

@app.route('/video')
def videoPage():
    return render_template('videoLoop.html')

@app.route('/draw_pic')
def draw_pic():
    return render_template('draw.html')

@app.route('/hello/<name>')
def hello_name(name):
    return "Hello, {}!".format(name)

@app.route('/post/getTree', methods=['POST'])
def getTree():
    roadkey = request.form.get("roadkey")
    page = "<option value=\"--\">--</option>"
    treeList = sql_gen.getRoadIndex(roadkey)
    for name in treeList:
        page = "{}<option value=\"{}\">{}</option>".format(page, name, name)
    return page

@app.route('/post/getTimeline', methods=['POST'])
def getTimeline():
    roadname = request.form.get("roadname")
    if roadname == '--':
        return "<p>--</p>"
    else:
        list_timeline = sql_gen.getRoadTimeline(roadname)
        page = ""
        for timeline in list_timeline:
            page = "{}<p>{}</p>".format(page, timeline)
        return page

@app.route('/post/manualDraw', methods=['POST'])
def manualDraw():
    pointList_json = request.form.get("pointList_json")
    lane = request.form.get("lane")
    # 'manualDraw:<|||||> pointList_json <|||||> lane'
    Send("manualDraw:<|||||>{}<|||||>{}".format(pointList_json, lane))
    img_bytes_base64_str = Recv()
    return 'data:image/jpeg;base64, {}'.format(img_bytes_base64_str)

@app.route('/post/refreshImg', methods=['POST'])
def refreshImg():
    c_w = request.form.get("w")
    c_h = request.form.get("h")
    img_bytes = getMonitorImg()
    img_bytes_base64_bytes = base64.encodebytes(img_bytes)
    img_bytes_base64_str = bytes.decode(img_bytes_base64_bytes, 'utf-8')
    # 'newDraw:<|||||> WxH <|||||> img_bytes_base64_str'
    SafeSend("newDraw:<|||||>{}x{}<|||||>{}".format(c_w, c_h, img_bytes_base64_str))
    return 'data:image/jpeg;base64, {}'.format(img_bytes_base64_str)

@app.route('/video_feed')
def video_feed():
    return Response(frameGen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/monitor_img')
def monitor_img():
    byte_img = getMonitorImg()
    return byte_img
