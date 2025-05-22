from fastapi import FastAPI
import httpx

app = FastAPI()

USER_SERVICE_URL = "http://user-service:8000"
ORDER_SERVICE_URL = "http://order-service:8000"

@app.get("/aggregate")
async def aggregate_data():
    async with httpx.AsyncClient() as client:
        user_response = await client.get(f"{USER_SERVICE_URL}/users")
        order_response = await client.get(f"{ORDER_SERVICE_URL}/orders")

    return {
        "users": user_response.json(),
        "orders": order_response.json()
    }
