from confluent_kafka import Producer
from common import ConfigVault
import random
import datetime
import time


class SimulatedSensor:
    def __init__(self, sensor_id, pollutant):
        self.sensor_id = sensor_id
        self.pollutant = pollutant

    def generate(self):
        timestamp = datetime.datetime.now().isoformat()
        value = random.uniform(0, 100)
        return {
            'sensor_id': self.sensor_id,
            'timestamp': timestamp,
            'pollutant_type': self.pollutant,
            'value': round(value, 2)
        }


class TopicProducer:
    def __init__(self, override_config=None):
        self.producer = Producer(override_config or ConfigVault.producer_config())

    def delivery_callback(self, err, msg):
        if err:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    def produce(self, topic, message):
        self.producer.produce(topic, message.encode('utf-8'), callback=self.delivery_callback)

    def flush(self):
        self.producer.flush()


class App:
    def __init__(self):
        self.producer = TopicProducer()
        self.sensor = SimulatedSensor(sensor_id='sensor_001', pollutant='PM2.5')

    def run(self):
        while True:
            message = self.sensor.generate()
            self.producer.produce('air-quality', str(message))
            self.producer.flush()

            time.sleep(1)


if __name__ == '__main__':
    app = App()
    app.run()
