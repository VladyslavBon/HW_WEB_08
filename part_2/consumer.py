import time

import pika
from mongoengine import connect

from models import Client


connect(db='web14', host="mongodb+srv://boridka:654123@cluster0.8nz8els.mongodb.net/?retryWrites=true&w=majority")


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def send_message_to_email():
    print(f" [x] Sending message to contact's email...")
    time.sleep(1)

def callback(ch, method, properties, body):
    message = body.decode()
    print(f" [x] Received contact's id: {message}")

    send_message_to_email()

    print(f" [x] Sending done: {method.delivery_tag}")

    client = Client.objects(id=message)
    client.update(sent=True)

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()