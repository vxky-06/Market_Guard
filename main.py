import pandas as pd
from src.data_ingestion import load_data
from src.preprocessing import preprocess
from src.model import train_model, predict_anomalies, train_dbscan
from src.detection import log_threats
from src.visualization import visualize_anomalies
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_score, recall_score
import numpy as np

if __name__ == "__main__":
    # Load the full dataset
    DATA_PATH = 'data/transactions.csv'
    df = load_data(DATA_PATH)

    if df is None or df.empty:
        print("No data available to process.")
        exit(1)

    # Preprocess the entire dataset
    processed_df, preprocessor = preprocess(df)
    if processed_df is None:
        print("Preprocessing failed.")
        exit(1)

    # --- Isolation Forest Grid Search ---
    iso_results = []
    for contamination in [0.05, 0.1, 0.2]:
        model = IsolationForest(contamination=contamination, random_state=42)
        model.fit(processed_df)
        pred_flags = model.predict(processed_df)
        anomaly_count = np.sum(pred_flags == -1)
        iso_results.append((contamination, anomaly_count))
        print(f"Isolation Forest (contamination={contamination}): {anomaly_count} anomalies")

    # --- DBSCAN Grid Search ---
    dbscan_results = []
    for eps in [0.5, 1.0, 2.0]:
        for min_samples in [2, 3, 5]:
            labels, dbscan_model = train_dbscan(processed_df, eps=eps, min_samples=min_samples)
            anomaly_count = np.sum(labels == -1)
            dbscan_results.append((eps, min_samples, anomaly_count))
            print(f"DBSCAN (eps={eps}, min_samples={min_samples}): {anomaly_count} anomalies")

    # --- Select best settings (for demonstration, pick the setting with anomaly count closest to 1/10th of data) ---
    target = max(1, len(df) // 10)
    best_iso = min(iso_results, key=lambda x: abs(x[1] - target))
    best_dbscan = min(dbscan_results, key=lambda x: abs(x[2] - target))

    # --- Output comparison ---
    comparison_lines = [
        "Isolation Forest grid search results:",
        *(f"  contamination={c}: {a} anomalies" for c, a in iso_results),
        "",
        "DBSCAN grid search results:",
        *(f"  eps={e}, min_samples={m}: {a} anomalies" for e, m, a in dbscan_results),
        "",
        f"Best Isolation Forest: contamination={best_iso[0]}, anomalies={best_iso[1]}",
        f"Best DBSCAN: eps={best_dbscan[0]}, min_samples={best_dbscan[1]}, anomalies={best_dbscan[2]}"
    ]
    comparison_report = '\n'.join(comparison_lines)
    print(comparison_report)
    with open('reports/performance_comparison.txt', 'w') as f:
        f.write(comparison_report)

    # Continue with the rest of the pipeline using best Isolation Forest
    model = IsolationForest(contamination=best_iso[0], random_state=42)
    model.fit(processed_df)
    pred_flags = model.predict(processed_df)
    pred_scores = -model.score_samples(processed_df)
    log_threats(df, pred_flags, pred_scores)
    df['anomaly_flag'] = pred_flags
    df['anomaly_score'] = pred_scores
    visualize_anomalies(df)
    print("Pipeline completed. Threats logged and visualization saved.")
