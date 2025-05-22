from fastapi import FastAPI
from pydantic import BaseModel
import httpx

app = FastAPI()

class Item(BaseModel):
    id: int
    value: str

def get_shard_url(item_id: int) -> str:
    return "http://shard1-service:8000" if item_id % 2 == 0 else "http://shard2-service:8000"

@app.post("/items")
async def route_item(item: Item):
    shard_url = get_shard_url(item.id)
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{shard_url}/items", json=item.dict())
        return response.json()
