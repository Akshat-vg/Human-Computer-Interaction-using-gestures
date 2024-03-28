# we first create a unique ID which is unique for each document in the collection
# And this unique ID should be unique to each device and should not change with time

import uuid
import socket
import pymongo
from dotenv import load_dotenv
import os

load_dotenv()


def get_unique_id():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    hostname = socket.gethostname()
    return f"{mac}-{hostname}"


unique_id = get_unique_id()
print(unique_id)

client = pymongo.MongoClient(os.getenv("MONGODB.URI"))

db = client["hci"]

collection = db["user-config"]

if collection.find_one({"_id": unique_id}) == None:
    print(
        "Inserted : ",
        collection.insert_one(
            {"_id": unique_id, "name": "Aditya", "count": 0}
        ).acknowledged,
    )
    print(collection.find_one({"_id": unique_id}))
else:
    print("User already exists")
    collection.update_one(
        {"_id": unique_id}, {"$set": {"name": "Aditya"}, "$inc": {"count": 1}}
    )
    print(collection.find_one({"_id": unique_id}))

client.close()
