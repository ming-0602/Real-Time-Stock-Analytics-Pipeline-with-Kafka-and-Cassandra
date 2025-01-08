import time
import os
import requests
import json
from confluent_kafka import Producer

ALPHA_VANTAGE_API_KEY = 'YYJ4HNUD11RRCS8E'
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "stock_quotes")

def fetch_stock_quote(symbol):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    resp = requests.get(url)
    data = resp.json()
    return data

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result. """
    if err is not None:
        print(f"Delivery failed for record {msg.value()}: {err}")
    else:
        print(f"Record {msg.value()} successfully produced to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def main():
    p = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})
    symbols = ["AAPL", "AMZN", "GOOG"]

    while True:
        for symbol in symbols:
            quote_data = fetch_stock_quote(symbol)
            # Optionally parse or simplify data
            value_json = json.dumps(quote_data)
            p.produce(topic=KAFKA_TOPIC, value=value_json, callback=delivery_report)
            p.poll(0)  # triggers delivery callbacks
        p.flush()
        time.sleep(30)  # fetch every 5 seconds

if __name__ == "__main__":
    main()
