from twilio.rest import Client
import os
from flask import Flask
from flask import request
app = Flask(__name__)

# Download the helper library from https://www.twilio.com/docs/python/install

# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_NUMBER')
client = Client(account_sid, auth_token)


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
        message = client.messages.create(
            body="Hello world!",
            from_= twilio_number,
            to='+' + number
        )
        print(message.sid)
    return 'Your number was ' + number
