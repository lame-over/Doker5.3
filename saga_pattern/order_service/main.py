from fastapi import FastAPI
import pika
import json

app = FastAPI()

def send_event(event: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='order_queue')
    channel.basic_publish(exchange='', routing_key='order_queue', body=json.dumps(event))
    connection.close()

@app.post("/create-order")
def create_order(item: str):
    event = {
        "event": "OrderCreated",
        "data": {"item": item}
    }
    send_event(event)
    return {"status": "Order created and event sent"}
