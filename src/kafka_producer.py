import time
import json
import pandas as pd
from kafka import KafkaProducer

KAFKA_BROKER = 'localhost:9092'  # Change if your broker is elsewhere
TOPIC = 'marketguard-transactions'
CSV_PATH = 'data/transactions.csv'


def main():
    # Load transactions
    df = pd.read_csv(CSV_PATH)
    
    # Initialize Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    print(f"Streaming transactions to Kafka topic '{TOPIC}'...")
    for idx, row in df.iterrows():
        message = row.to_dict()
        producer.send(TOPIC, value=message)
        print(f"Sent transaction {idx+1}/{len(df)}: {message}")
        time.sleep(1)
    producer.flush()
    print("All transactions sent.")

if __name__ == "__main__":
    main() 