from flask import Flask, redirect, render_template, request, url_for
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
gen = sqliteData.Generator()
sk = socketConnect.HostConnection('127.0.0.1', 8097)

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

print("Threading")

bytePic = b"None"

def changePic(data):
    global bytePic
    bytePic = data

@app.route('/')
def mainWeb():
    return "<h1>Hello Main</h1>"

@app.route('/searchRoad')
def searchRoad():
    return render_template('searchRoad.html')

@app.route('/video')
def videoPage():
    return render_template('videoLoop.html')

@app.route('/hello/<name>')
def hello_name(name):
    return "Hello, {}!".format(name)

@app.route('/getTree', methods=['POST'])
def getTree():
    roadkey = request.form.get("roadkey")
    page = ""
    treeList = gen.getRoadIndex(roadkey)
    for name in treeList:
        #name = setLabel(name, roadkey, "b")
        #page = "{}<p>{}</p>".format(page, name)
        page = "{}<option value=\"{}\">{}</option>".format(page, name, name)
    return page

@app.route('/videoLoop', methods=['POST'])
def videoLoop():
    webReady = request.form.get("webReady")
    #if (webReady == "OK"):
    if (True):
        Send("getVideo")
        strPic_base64 = Recv()
        if ("b'" in strPic_base64):
            byte_string = eval(strPic_base64)
            changePic(base64.decodebytes(byte_string))
        else:
            #changePic(b"None")
            changePic(strPic_base64)
        #Send('getVideo')
        #bytePic = Recv()
        return "<img src=\"/pic/{}.jpg\"/>".format(time.time())

@app.route('/pic/<randtime>.jpg')
def pic(randtime):
    return bytePic
