from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
data_store = {}

class Item(BaseModel):
    id: int
    value: str

@app.post("/items")
def add_item(item: Item):
    data_store[item.id] = item.value
    return {"status": "stored in shard1", "item": item}

@app.get("/items")
def get_items():
    return data_store
