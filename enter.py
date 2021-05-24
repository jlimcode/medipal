from Medication import Entry, Medication
from send_text import send_text
import os
from pymongo import MongoClient

mongo_key = os.getenv('MONGO_LOGIN')


def create_message(med: Medication) -> str:
    message = "It’s your Medipal here to remind you to take "
    if med.anonymous:
        message += "your medication"
    else:
        message += med.name
    if med.withFood:
        message += " with food!\n"
    else:
        message += " without food!\n"
    if med.restrictions != "" and med.restrictions != None:
        message += "Keep in mind these restrictions: " + med.restrictions + "!\n"
    message += med.message
    return message


def enter(entry: Entry) -> None:
    cluster = MongoClient(mongo_key, tlsAllowInvalidCertificates=True)
    db = cluster["Medipal"]
    Users = db["Users"]
    Meds = db["Meds"]

    num = entry.number

    u = Users.find_one({"number": num})

    if(u == None):  # user is not already in the system, adding them
        medHashes = []
        newUser = {"number": num, "meds": []}
        Users.insert_one(newUser)
        u = Users.find_one({"number": num})
        uid = u["_id"]

        for m in entry.meds:
            m.addMessage(create_message(m))
            m.addUID(uid)
            Meds.insert_one(m.getDBFormat())

        userMeds = Meds.find({"user": uid})
        for m in userMeds:
            medHashes.append(m["_id"])
        Users.update_one({"_id": uid}, {"$set": {"meds": medHashes}})

    else:  # updating existing user
        uid = u["_id"]
        for m in entry.meds:
            med = Meds.find_one({"user": uid, "name": m.name})
            if med == None:
                med = m.getDBFormat()
                Meds.insert_one(med)
            else:
                Meds.update_one({"_id": med["_id"]}, {
                                "$set": {"times": m.times}})

        userMeds = Meds.find({"user": uid})
        medHashes = []
        for m in userMeds:
            medHashes.append(m["_id"])
        Users.update_one({"_id": uid}, {"$set": {"meds": medHashes}})


if __name__ == "__main__":

    medsDict1 = {"name": "testMed", "times": ["04:13", "12:34"],
                 "chronic": False, "withFood": False, "doses": 14, "restrictions": "no calcium",
                 "message": "hi", "anonymous": True}
    medsDict2 = {"name": "testMed7", "times": ["04:14", "2:38"], "chronic": True,
                 "withFood": True, "doses": -1, "restrictions": "calcium",
                 "message": "hello", "anonymous": False}
    meds = [medsDict1] + [medsDict2]
    testDict = {"number": "+1234567890", "meds": meds}
    enter(Entry(**testDict))
    print("done")
