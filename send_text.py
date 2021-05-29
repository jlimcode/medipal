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

send_text("18054051091", "Hello! This is MediPal, your Personal Health Assistant.  I am here to help you get over this little bump in life, so you can get back to doing the things you love with the people you love! If you ever want to opt out of my help reply ‘STOP’. Great meeting you, and I will be in touch soon!")
