import pika
from faker import Faker
from mongoengine import connect

from models import Client


connect(db='web14', host="mongodb+srv://boridka:654123@cluster0.8nz8els.mongodb.net/?retryWrites=true&w=majority")


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='task_mock', exchange_type='direct')
channel.queue_declare(queue='task_queue', durable=True)
channel.queue_bind(exchange='task_mock', queue='task_queue')


def main():
    fake = Faker('uk_UA')

    for _ in range(5):
        client = Client(
            fullname=fake.name(),
            email=fake.email(),
            sent=False
        )
        client.save()

        channel.basic_publish(
            exchange='task_mock',
            routing_key='task_queue',
            body=str(client.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(" [x] Sent %r" % client.id)
    connection.close()
    
    
if __name__ == '__main__':
    main()