from pymongo import MongoClient
from termcolor import cprint
import os

mongo_key = os.getenv('MONGO_LOGIN')

cluster = MongoClient(mongo_key, tlsAllowInvalidCertificates=True)
db = cluster["Medipal"]
Users = db["Users"]
Meds = db["Meds"]

dead_users = Users.delete_many({})

cprint(f'{dead_users.deleted_count} users deleted', 'red')

flushed_meds = Meds.delete_many({})

cprint(f'{flushed_meds.deleted_count} medications deleted', 'red')