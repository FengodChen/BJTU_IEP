from flask import Flask, redirect, render_template, request, url_for
from WebLib import *
import json
import time

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
loopMonitor = socketConnect.loopMonitor
operateMonitor = socketConnect.operateMonitor
operateLaneLine = socketConnect.operateLaneLine

bytePic = b""

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
        bytePic = next(loopMonitor)
        return "<img src=\"/pic/{}\"/>".format(time.time())

@app.route('/pic/<randtime>')
def pic(randtime):
    return bytePic

if __name__ == "__main__":
    print("Run in main")
    #loopMonitor = socketConnect.LoopMonitor_Thread()
    #loopMonitor.start()

    #operateMonitor = socketConnect.OperateMonitor_Thread()
    #operateMonitor.start()

    #operateLaneLine = socketConnect.OperateLaneLine_Thread()
    #operateLaneLine.start()

    #app.run(host='0.0.0.0', port=80, threaded=True)
    app.run(host='0.0.0.0', port=80)