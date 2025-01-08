# consumer.py
from confluent_kafka import Consumer, KafkaError, KafkaException

def main():
    # Configure consumer
    c = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'hello-group',
        'auto.offset.reset': 'earliest'
    })

    # Subscribe to the same topic we just produced to
    topic = "test_topic"
    c.subscribe([topic])

    print("Consumer started. Waiting for messages... Press Ctrl+C to exit.")
    try:
        while True:
            msg = c.poll(1.0)  # 1 second timeout
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    continue
                else:
                    raise KafkaException(msg.error())
            else:
                # Proper message
                msg_value = msg.value().decode('utf-8')
                print(f"Received message: {msg_value}")
    except KeyboardInterrupt:
        print("Aborted by user")
    finally:
        c.close()

if __name__ == "__main__":
    main()
