import json
from kafka import KafkaConsumer
import pandas as pd
from src.preprocessing import preprocess
from src.model import train_model, predict_anomalies
from src.detection import log_threats
# from elasticsearch import Elasticsearch  # Uncomment if integrating with ELK

KAFKA_BROKER = 'localhost:9092'
TOPIC = 'marketguard-transactions'

# Optionally set up ELK integration
# es = Elasticsearch('http://localhost:9200')
# ELK_INDEX = 'marketguard-anomalies'

def main():
    # Train the model on the full dataset at startup
    df_full = pd.read_csv('data/transactions.csv')
    processed_full, preprocessor = preprocess(df_full)
    model = train_model(processed_full)

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='marketguard-group'
    )

    print(f"Listening for transactions on topic '{TOPIC}'...")
    for message in consumer:
        transaction = message.value
        print(f"Received transaction: {transaction}")
        # Convert to DataFrame for processing
        transaction_df = pd.DataFrame([transaction])
        processed, _ = preprocess(transaction_df)
        pred_flag, pred_score = predict_anomalies(model, processed)
        if pred_flag[0] == -1:
            log_threats(transaction_df, pred_flag, pred_score)
            print(f"[ALERT] Anomaly detected: {transaction} | Severity: {pred_score[0]:.4f}")
            # Optionally send to ELK
            # es.index(index=ELK_INDEX, document=transaction)
        else:
            print("Transaction is normal.")

if __name__ == "__main__":
    main() 