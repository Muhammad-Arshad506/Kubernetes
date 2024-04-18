import random
import string
import os
from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel







# Use os.getenv to read environment variable for MongoDB URL
database_url = os.getenv("MONGODB_URL") if os.getenv("MONGODB_URL") else "mongodb"
database_port = os.getenv("MONGODB_PORT") if os.getenv("MONGODB_PORT") else "2701"




app = FastAPI()





# Define a Pydantic model for data validation
class Item(BaseModel):
    name: str



client = MongoClient(f"mongodb://{database_url}:{database_port}/")
db = client["testdb"]
collection = db["items"]

def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@app.get("/")
async def root():
    return {"message": f"Hello this is kubernetes v5 with enviroment variable {database_url} and port {database_port}"}


@app.get("/insert")
async def create_item():
    item = Item(
        name=random_string(10),
    )
    # Insert the item into MongoDB
    collection.insert_one(item.dict())
    return "Ok"

@app.get("/get")
async def create_item():
    items = list(collection.find({}, {'_id': 0}))  # Excluding the MongoDB '_id' from the response
    return {"message": f"{items}"}