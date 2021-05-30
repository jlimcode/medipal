import os
import time
from pymongo import MongoClient
from send_text import send_text

def remove(med, user):
    mid = m["_id"]
    newMeds = (u["meds"]).remove(mid)

    Users.update_one({"_id": u["_id"]}, {"$set": {"meds": newMeds}})
    Meds.delete_one({"_id": m["_id"]})
              

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
                u = m["user"]
                num = Users.find_one({"_id": m["user"]})
                print("send message to: " + num["number"]) 
                send_text(num["number"], m["message"])
                if not (m["chronic"]):  
                    Meds.update_one({"_id": m["_id"]}, {"$inc": {"remDoses": -1}})
                    if m["remDoses"] == 0:
                        remove(m, u)




