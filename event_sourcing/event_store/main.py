from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import redis
import json

app = FastAPI()
r = redis.Redis(host="redis", port=6379, decode_responses=True)

class ItemEvent(BaseModel):
    action: str
    data: dict

@app.post("/event")
def store_event(event: ItemEvent):
    event_id = str(uuid.uuid4())
    event_record = {
        "id": event_id,
        "action": event.action,
        "data": event.data
    }
    r.rpush("event_stream", json.dumps(event_record))
    return {"status": "event stored", "event": event_record}
