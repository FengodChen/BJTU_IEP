from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<h1>Hello, world!</h1>"

@app.route('/test')
def test():
    return "<h1>This is a test</h1>"

@app.route('/hello/<name>')
def hello_name(name):
    return "Hello, {}!".format(name)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)