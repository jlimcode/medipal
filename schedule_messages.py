import os
import time
from pymongo import MongoClient

TIME_INTERVAL = 10 

mongo_key = os.getenv('MONGO_LOGIN')

cluster = MongoClient(mongo_key)
db = cluster["Medipal"]
Users = db["Users"] 
Meds = db["Meds"] 

meds_list = Meds.find({})

now = time.localtime(time.time())
hour = now.tm_hour
mins = now.tm_min
timeOptions = []

# calcuating and formating range of minutes in TIME_INTERVAL from current time in a list
if (mins < (60 - TIME_INTERVAL)):
    for x in range(mins, mins+ TIME_INTERVAL + 1): 
        t = str(hour) + ":" + str(x)
        timeOptions += [t]
else:
    over = mins - 60 + TIME_INTERVAL
    for x in range(mins, 60):
        t = str(hour) + ":" + str(x)
        timeOptions += [t]
    next_h = hour + 1
    if hour == 23:
        next_h = 0
    for x in range(0, over+1):
        t = str(next_h) + ":" + str(x)
        timeOptions += [t]

for m in meds_list:
        for time in m["times"]:
            if time in timeOptions:
                print("send message" + m["_id"]) # TODO: print USER id too (need to restructure db to store this)
                # call send_message.py
            if not (m["chronic"]):
                print("not chronic" + m["_id"]) # TODO: decremend remDoses here