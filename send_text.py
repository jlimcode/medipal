import sys
import os
from twilio.rest import Client
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_NUMBER')
client = Client(account_sid, auth_token)


def send_text(number, message):
    """
    param: number is given without "+"
    """
    if number is None:
        print("Invalid number")
    else:
        message = client.messages.create(
            body=message,
            from_=twilio_number,
            to='+' + number
        )
        print(message.sid)
    return 0


if __name__ == "__main__":
    arg_list = sys.argv
    send_text(number=arg_list[1], message=arg_list[2])
