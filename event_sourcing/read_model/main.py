from fastapi import FastAPI
import redis
import json

app = FastAPI()
r = redis.Redis(host="redis", port=6379, decode_responses=True)

@app.get("/rebuild")
def rebuild_read_model():
    events = r.lrange("event_stream", 0, -1)
    read_model = {}

    for event_json in events:
        event = json.loads(event_json)
        item_id = event["data"].get("id")
        if event["action"] == "create":
            read_model[item_id] = event["data"]
        elif event["action"] == "delete" and item_id in read_model:
            del read_model[item_id]

    return {"read_model": read_model}
