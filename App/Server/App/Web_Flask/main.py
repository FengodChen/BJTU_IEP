from flask import Flask, redirect, render_template, request, url_for
from WebLib import *

app = Flask(__name__)
gen = sqliteData.Generator()

@app.route('/')
def hello_world():
    return "<h1>Hello, world!</h1>"

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/hello/<name>')
def hello_name(name):
    return "Hello, {}!".format(name)

@app.route('/getTree/<text>')
def getTree(text):
    page = "<h1> Found Answer: </h1>"
    treeList = gen.getRoadIndex(text)
    for name in treeList:
        page = "{}<p>{}</p>".format(page, name)
    return page

@app.route('/getInput', methods = ['POST', 'GET'])
def getInput():
    text = request.args.get('roadname_input')
    return redirect(url_for('getTree', text = text))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)