# MarketGuard

MarketGuard is a real-time and batch anomaly detection pipeline for financial transactions, featuring:
- Data ingestion from CSV and Kafka
- Preprocessing and feature engineering
- Unsupervised anomaly detection (Isolation Forest, DBSCAN)
- Threat logging and visualization
- ELK stack (Elasticsearch, Logstash, Kibana) integration for monitoring and dashboards

---

## Architecture

```
[CSV/Producer] → [Kafka] → [Consumer] → [Preprocessing] → [Anomaly Detection] → [Threat Log/ELK] → [Kibana]
```

---

## Features
- Real-time and batch anomaly detection
- Modular pipeline (data ingestion, preprocessing, modeling, logging, visualization)
- Kafka streaming support
- ELK stack for search, alerting, and dashboards
- Easily extensible for new models or data sources

---

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/MarketGuard.git
cd MarketGuard
```

### 2. Install Python Dependencies
```sh
pip install -r requirements.txt
```

### 3. Start Kafka and Zookeeper (for streaming)
```sh
docker-compose up -d zookeeper kafka
```

### 4. Start the ELK Stack (Elasticsearch, Logstash, Kibana)
```sh
docker-compose up -d elasticsearch logstash kibana
```

### 5. Configure Logstash
- Ensure `logstash.conf` and `logs/threat_log.csv` are present.
- Logstash will ingest anomalies from the CSV into Elasticsearch.

---

## Usage

### **A. Batch Pipeline**
Run the full pipeline on your CSV data:
```sh
python main.py
```
- Detects anomalies, logs threats, and generates visualizations.
- Results:
  - Threats: `logs/threat_log.csv`
  - Visualization: `reports/anomaly_visualization.png`
  - Model comparison: `reports/performance_comparison.txt`

### **B. Real-Time Streaming**
1. **Start the Kafka Consumer:**
   ```sh
   python -m src.kafka_consumer
   ```
2. **Start the Kafka Producer (in another terminal):**
   ```sh
   python -m src.kafka_producer
   ```
- Transactions are streamed, processed, and anomalies are logged in real time.

### **C. ELK Stack & Kibana Visualization**
1. Go to [http://localhost:5601](http://localhost:5601)
2. Create a data view for `marketguard-threats`.
3. Use Discover/Visualize to explore anomalies, top accounts, locations, and model performance.

---

## Step-by-Step Process

1. **Data Ingestion:**
   - Load transactions from `data/transactions.csv` or stream via Kafka.
2. **Preprocessing:**
   - Handle missing values, encode categoricals, normalize numerics.
3. **Model Training:**
   - Train Isolation Forest and DBSCAN on preprocessed data.
4. **Anomaly Detection:**
   - Predict anomalies, log threats, and compare models.
5. **Logging & Visualization:**
   - Log anomalies to CSV and Elasticsearch.
   - Visualize results in Kibana and as PNG plots.
6. **Monitoring:**
   - Use Kibana dashboards for real-time and historical analysis.

---

## Requirements
- Python 3.8+
- Docker & Docker Compose
- Kafka, Zookeeper, Elasticsearch, Logstash, Kibana (via Docker)
- Python packages: see `requirements.txt`

---

## Contributing
Pull requests and issues are welcome! Please open an issue to discuss your ideas or report bugs.

## License
[MIT License](LICENSE)
