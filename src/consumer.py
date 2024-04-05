from confluent_kafka import Consumer, KafkaError, KafkaException
from common import ConfigVault
from termcolor import colored, cprint
from pymongo import MongoClient
import json
import sys


class Database:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client['air_quality']
        self.collection = self.db['readings']

    def insert(self, message):
        self.collection.insert_one(message)


class Message:
    @staticmethod
    def process(message):
        sensor_id = message['sensor_id']
        timestamp = message['timestamp']
        pollutant = message['pollutant_type']
        value = message['value']

        cprint(f"[{timestamp}]", 'blue', end='')
        cprint(f"<{sensor_id}>", 'green', end='')
        cprint(f"{pollutant}: {value}", 'red')

        sys.stdout.flush()


class TopicConsumer:
    def __init__(self, topic, override_config=None):
        self.topic = topic
        self.consumer = Consumer(override_config or ConfigVault.consumer_config())
        self.consumer.subscribe([self.topic])

    def consume(self, db):
        while True:
            message = self.consumer.poll(timeout=1.0)
            if message is None:
                continue
            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    raise KafkaException(message.error())
            else:
                message = json.loads(message.value().decode('utf-8').replace("'", '"'))
                print(message)
                Message.process(message)
                db.insert(message)

    def consume_one(self):
        while True:
            message = self.consumer.poll(timeout=1.0)
            if message is None:
                continue
            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    raise KafkaException(message.error())
            else:
                message = json.loads(message.value().decode('utf-8').replace("'", '"'))
                return message

    def close(self):
        self.consumer.close()


class App:
    def __init__(self):
        self.consumer = TopicConsumer('air-quality')
        self.db = Database(ConfigVault.mongo_uri())

    def run(self):
        try:
            self.consumer.consume(self.db)
        except KeyboardInterrupt:
            self.consumer.close()


if __name__ == '__main__':
    app = App()
    app.run()
