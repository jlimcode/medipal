import os
from pymongo import MongoClient
mongo_key = os.getenv('MONGO_LOGIN')

cluster = MongoClient(mongo_key)
db = cluster["Medipal"]
Users = db["Users"] # Collection of users with a list of medicines
Meds = db["Meds"] # Collection of medicines with list of times, chronic flag,
                  # decrementing doses left (-1 if chronic), and message
                  # structure can be changed

# schedule every TIME_INTERVAL minutes

    # get time here
    meds_list = Meds.find({})

    for m in meds_list:
        for time in m["times"]:
            # if time is in the interval:
                # construct message
                # call send_message accordingly
                if ! (m["chronic"]):
                    # decrement m["remDoses"]


        