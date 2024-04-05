from unittest.mock import patch
from producer import TopicProducer, SimulatedSensor
from consumer import Database, TopicConsumer, Message
import mongomock
import unittest
import time


class TestKafkaIntegration(unittest.TestCase):
    def test_integrity(self):
        test_sensor = SimulatedSensor('test_sensor', 'PM2.5')
        test_message = test_sensor.generate()

        producer = TopicProducer()
        producer.produce('test-air-quality', str(test_message))
        producer.flush()

        consumer = TopicConsumer('test-air-quality')
        message = consumer.consume_one()

        self.assertIsNotNone(message)
        self.assertEqual(message['sensor_id'], test_message['sensor_id'])
        self.assertEqual(message['pollutant_type'], test_message['pollutant_type'])
        self.assertEqual(message['value'], test_message['value'])
        self.assertEqual(message['timestamp'], test_message['timestamp'])


class TestPersistence(unittest.TestCase):

    @patch('pymongo.MongoClient')
    def test_message_persistence(self, mock_client):
        mock_db = mongomock.MongoClient().db
        mock_collection = mock_db['readings']
        mock_client.return_value = mongomock.MongoClient()

        db = Database(uri="mongodb://mockuri:27017")

        db.collection = mock_collection

        test_message = {
            'sensor_id': 'test_sensor_001',
            'timestamp': '2024-04-05T12:34:56.789Z',
            'pollutant_type': 'PM2.5',
            'value': 22.33
        }
        db.insert(test_message)

        inserted_message = mock_collection.find_one({'sensor_id': 'test_sensor_001'})
        self.assertIsNotNone(inserted_message)
        self.assertEqual(inserted_message['timestamp'], '2024-04-05T12:34:56.789Z')
        self.assertEqual(inserted_message['pollutant_type'], 'PM2.5')
        self.assertEqual(inserted_message['value'], 22.33)


if __name__ == '__main__':
    unittest.main()
