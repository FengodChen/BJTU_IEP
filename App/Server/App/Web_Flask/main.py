from flask import Flask, redirect, render_template, request, url_for
from WebLib import *
import json

app = Flask(__name__)
gen = sqliteData.Generator()

@app.route('/jq')
def jq():
    return render_template('tryJquery.html')

@app.route('/hello/<name>')
def hello_name(name):
    return "Hello, {}!".format(name)

@app.route('/getTree', methods=['POST'])
def getTree():
    roadkey = request.form.get("roadkey")
    page = ""
    treeList = gen.getRoadIndex(roadkey)
    for name in treeList:
        page = "{}<p>{}</p>".format(page, name)
    return page

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)