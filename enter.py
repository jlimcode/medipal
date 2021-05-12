import os
from pymongo import MongoClient

mongo_key = os.getenv('MONGO_LOGIN')

def enter(entry):
    cluster = MongoClient(mongo_key)
    db = cluster["Medipal"]
    Users = db["Users"] 
    Meds = db["Meds"] 

    num = entry["number"]

    u = Users.find_one({"number": num})
    
    if(u == None): # user is not already in the system, adding them
        medHashes = []
        newUser = {"number": num, "meds": []}
        Users.insert_one(newUser)
        u = Users.find_one({"number": num})
        uid = u["_id"]
        for m in entry["meds"]: 
            med = {"name": m["name"], "user": uid, "times": m["times"], 
                "chronic": m["chronic"], "food": m["withFood"], 
                "remDoses": m["doses"], "restrictions": m["restrictions"],
                "message": m["message"]}
            Meds.insert_one(med)
        userMeds = Meds.find({"user": uid})
        for m in userMeds:
            medHashes.append(m["_id"])
        Users.update_one({"_id": uid}, {"$set": {"meds": medHashes}})
    else: # updating existing user
        uid = u["_id"]
        for m in entry["meds"]:
            med = Meds.find_one({"user": uid, "name": m["name"]})
            if med == None:
                med = {"name": m["name"], "user": uid, "times": m["times"], 
                "chronic": m["chronic"], "food": m["withFood"], 
                "remDoses": m["doses"], "restrictions": m["restrictions"],
                "message": m["message"]}
                Meds.insert_one(med)
            else:
                Meds.update_one({"_id": med["_id"]}, {"$set": {"times": m["times"]}})

        
        userMeds = Meds.find({"user": uid})
        medHashes = []
        for m in userMeds:
            medHashes.append(m["_id"])
        Users.update_one({"_id": uid}, {"$set": {"meds": medHashes}})

if __name__ == "__main__":
    
    medsDict1 = {"name": "testMed", "times": ["04:13", "12:34"], 
    "chronic": False, "withFood": False, "doses": 14, "restrictions": "no calcium", 
    "message": "hi"}
    medsDict2 = {"name": "testMed2", "times": ["04:14", "12:14"], "chronic": True, 
    "withFood": True, "doses": -1, "restrictions": "need calcium", 
    "message": "hello"}
    meds = [medsDict1] + [medsDict2]
    testDict = {"number": "+1234567890", "meds": meds}
    enter(testDict)
    print("done")
 