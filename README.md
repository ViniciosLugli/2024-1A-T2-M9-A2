# 2024-1A-T2-M9-A2

This project is designed to simulate and monitor air quality through a distributed system using Kafka for message passing and MongoDB for data storage. It showcases the use of a producer to generate simulated sensor data, a consumer to process and display this data, and a database interface for persistence. This system can be used as a basis for real-time environmental monitoring applications.

## Features

-   **Simulated Sensor Data Generation**: Emulates air quality sensors that produce readings for various pollutants.
-   **Kafka-Based Messaging**: Utilizes Apache Kafka for reliable, scalable, and real-time message passing between the sensors (producers) and the processing system (consumers).
-   **Data Persistence**: Stores air quality readings in MongoDB for historical analysis and querying.
-   **Real-Time Data Processing and Display**: Processes and visually displays the incoming sensor data in real-time.

## Prerequisites

-   Python 3.6 or higher
-   Docker

## Dependencies

You can install these dependencies using pip:

```bash
pip install -r requirements.txt
```

## Setup

Go to src folder

```bash
cd src
```

1. **Start Kafka and MongoDB Services**:

    Use Docker Compose to start the required services:

    ```bash
    docker-compose up -d
    ```

    This will start Kafka, Zookeeper, and MongoDB containers.

2. **Running the Producer**:

    The producer simulates sensor data and sends it to a Kafka topic. To run the producer, execute:

    ```bash
    python producer.py
    ```

3. **Running the Consumer**:

    The consumer listens for messages on the Kafka topic, processes them to display in the terminal, and stores them in MongoDB. To run the consumer, execute:

    ```bash
    python consumer.py
    ```

## Architecture

-   **Producer**: Simulates environmental sensors by generating random data for pollutants and sending this data to a Kafka topic.
-   **Consumer**: Subscribes to the Kafka topic, processes incoming messages by printing them to the console, and stores them in MongoDB for persistence.
-   **Database**: MongoDB is used to persist the sensor readings for future analysis. A simple database interface is provided for inserting documents.

## Testing

Unit tests are included to test both Kafka message passing and MongoDB persistence functionality. To run the tests, execute:

```bash
python -m unittest
```

## Example

### Producer
![image](https://github.com/ViniciosLugli/2024-1A-T2-M9-A2/assets/40807526/aea2c1be-527a-4f83-a198-1527551f488d)

### Consumer
![image](https://github.com/ViniciosLugli/2024-1A-T2-M9-A2/assets/40807526/16f86926-5503-4036-aa45-93c9a42e3247)

### Tests
![image](https://github.com/ViniciosLugli/2024-1A-T2-M9-A2/assets/40807526/edba3c0c-2b10-421c-930a-b1c136c88242)
