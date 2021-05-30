from termcolor import cprint
from enter import enter
from Medication import Entry, Medication
from twilio.rest import Client
import os
import csv
from flask import Flask, request, redirect, flash
app = Flask(__name__)

flask_secret = os.getenv('FLASK_SECRET', default='hashbrowns')

app.config['SECRET_KEY']='alskdjf;alkjsd;flakjs;dlfkj;aj;aoieij'

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
    number = request.args.get('phone')
    if number is None:
        print('Invalid number')
    else:
        print(number)
        message = client.messages.create(
            body='Hello world!',
            from_=twilio_number,
            to='+' + number
        )
        print(message.sid)
    return 'Your number was ' + number


ALLOWED_EXTENSIONS = {'csv'}
REQUIRED_FIELDS = {
    'name', 'times', 'chronic', 'withFood', 'doses', 'restrictions', 'anonymous', 'number'
}
PARSE_AS_TRUE = {'TRUE', 'True', 'true', 'T'}
PARSE_AS_FALSE = {'FALSE', 'False', 'false', 'F'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def parse_bool(strBool: str) -> bool:
    if strBool is bool:
        return strBool
    if strBool in PARSE_AS_TRUE:
        return True
    elif strBool in PARSE_AS_FALSE:
        return False
    else:
        return None


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            csv_text = ''.join(list(file.read().decode('utf-8')))
            csv_reader = csv.DictReader(csv_text.splitlines(), delimiter=',')
            for line_count, row in enumerate(csv_reader):
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                cprint(f'Line: {line_count + 1}', 'blue')
                if(not REQUIRED_FIELDS <= row.keys()):  # invalid
                    cprint('Invalid row! Missing: ', 'red')
                    print(REQUIRED_FIELDS - row.keys())
                else:
                    for key in ['withFood', 'chronic', 'anonymous']:
                        row[key] = parse_bool(row[key])
                    row['doses'] = int(row['doses'])
                    row['times'] = row['times'].split(', ')
                    # will almost certainly need to manage times input somehow
                    m = Medication(**row)
                    cprint('Successfully imported medication: ', 'green')
                    print(m)
                    enter(Entry(row['number'], [m]))
        cprint('All medications posted!', 'green')
        return 'Success!'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
