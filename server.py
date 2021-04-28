from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/ping', methods=['GET', 'POST'])
def send_text():
    number = request.args.get("phone")
    if number is None:
        print("Invalid number")
    else:
        print(number)
    return 'Your number was ' + number
