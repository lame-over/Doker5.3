from fastapi import FastAPI
import threading
import pika
import json

app = FastAPI()

def callback(ch, method, properties, body):
    message = json.loads(body)
    print("Payment Service received:", message)
    if message["event"] == "OrderCreated":
        # simulate processing
        print("✅ Payment processed for item:", message["data"]["item"])

def listen():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='order_queue')
    channel.basic_consume(queue='order_queue', on_message_callback=callback, auto_ack=True)
    print("💬 Payment Service is waiting for messages...")
    channel.start_consuming()

threading.Thread(target=listen, daemon=True).start()
