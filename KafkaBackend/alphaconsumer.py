import json
from confluent_kafka import Consumer, KafkaError, KafkaException
from cassandra.cluster import Cluster
from datetime import datetime, time

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "stock_quotes"
KAFKA_GROUP = "my-cassandra-consumer"


def main():
    # 1) Connect to Cassandra
    cluster = Cluster(["localhost"], port='9042')  # or the container name, e.g., "my-cassandra"
    session = cluster.connect("stock_data")  # use the keyspace "stock_data"

    # 2) Prepare an INSERT statement
    insert_stmt = session.prepare("""
      INSERT INTO stock_prices (symbol, ts, open, high, low, price, volume)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    """)

    # 3) Kafka Consumer Setup
    c = Consumer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': KAFKA_GROUP,
        'auto.offset.reset': 'earliest'
    })
    c.subscribe([KAFKA_TOPIC])

    print("Starting consumer. Press Ctrl+C to exit.")
    try:
        while True:
            msg = c.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    continue
                else:
                    raise KafkaException(msg.error())
            else:
                # 4) Parse message
                data = json.loads(msg.value().decode('utf-8'))

                # Example if alpha vantage: data["Global Quote"]["05. price"]
                # Might need to safely parse to float, handle missing fields, etc.
                if "Global Quote" in data:
                    quote = data["Global Quote"]
                    symbol = quote.get("01. symbol", "UNKNOWN")
                    price_str = quote.get("05. price", "0.0")
                    open_price = float(quote.get("02. open", "0.0"))
                    high_price = float(quote.get("03. high", "0.0"))
                    low_price = float(quote.get("04. low", "0.0"))
                    volume = int(quote.get("06. volume", "0"))
                    try:
                        price = float(price_str)
                    except:
                        price = 0.0

                    # We'll use current time as ts, or parse "07. latest trading day" if needed
                    now = datetime.utcnow()

                    # 5) Insert into Cassandra
                    session.execute(insert_stmt, (symbol, now, open_price, high_price, low_price, price, volume))
                    print(f"Inserted {symbol} - {price} at {now}")
                # time.sleep(30)
    except KeyboardInterrupt:
        print("Aborted by user")
    finally:
        c.close()
        session.shutdown()


if __name__ == "__main__":
    main()
