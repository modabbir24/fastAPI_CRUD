from fastapi import FastAPI
from pydantic import BaseModel
import pymongo

app = FastAPI()

path = "mongodb+srv://modabbir7032:onlyIIT#2018@bepeepcode.onwwoq5.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(path)
db=client["Projects"]
collection = db["FastAPIDB"]

class Item(BaseModel):
    id: int
    name: str
    price: float

# Create Item
@app.post("/items/")
def create_item(item: Item):
    item_data = item.dict()
    result = collection.insert_one(item_data)
    return item

# Get all items
@app.get("/items/")
def get_items():
    items = collection.find()
    return list(items)

# Get any specific item
@app.get("/items/{item_id}")
def get_item(item_id: str):
    item = collection.find_one({"id": item_id})
    if item:
        return item
    return {"error": "Item not found"}

# Update an item
@app.put("/items/{item_id}")
def update_item(item_id: str, item: Item):
    updated_item = item.dict()
    result = collection.update_one({"id": item_id}, {"$set": updated_item})
    if result.modified_count > 0:
        return {"message": "Item updated successfully"}
    return {"error": "Item not found"}

# delete an item
@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    result = collection.delete_one({"id": item_id})
    if result.deleted_count > 0:
        return {"message": "Item deleted successfully"}
    return {"error": "Item not found"}

