# producer.py
from confluent_kafka import Producer

def delivery_report(err, msg):
    """
    delivery_report is called (from poll() or flush()) once for each message produced,
    to indicate delivery result.
    """
    if err is not None:
        print(f"Delivery failed for record {msg.value()}: {err}")
    else:
        print(f"Record {msg.value()} successfully produced to "
              f"{msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def main():
    # Configure producer
    p = Producer({'bootstrap.servers': 'localhost:9092'})

    # The topic we want to produce to
    topic = "test_topic"

    # Our message:
    message_value = "Hello Kafka!"

    # Send message asynchronously
    p.produce(topic=topic, value=message_value.encode('utf-8'), callback=delivery_report)

    # Trigger the delivery_report callback
    p.poll(0)

    # Wait for all deliveries to be flushed
    p.flush()

if __name__ == "__main__":
    main()
