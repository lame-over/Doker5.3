from fastapi import FastAPI
import redis
import json

app = FastAPI()
r = redis.Redis(host="redis", port=6379, decode_responses=True)

@app.get("/items")
def get_items():
    keys = r.keys("*")
    items = [json.loads(r.get(key)) for key in keys]
    return items
