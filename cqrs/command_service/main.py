from fastapi import FastAPI
from pydantic import BaseModel
import redis
import uuid
import json

app = FastAPI()
r = redis.Redis(host="redis", port=6379, decode_responses=True)

class Command(BaseModel):
    item: str

@app.post("/add")
def add_item(cmd: Command):
    item_id = str(uuid.uuid4())
    event = {"id": item_id, "item": cmd.item}
    r.set(item_id, json.dumps(event))  # act as event store
    return {"status": "Item added", "id": item_id}
