import pandas as pd
import os

def log_threats(df, predictions, scores):
    """
    Logs detected threats to a CSV file.

    Args:
        df (pandas.DataFrame): The original DataFrame with transaction data.
        predictions (numpy.ndarray): Anomaly flags from the model (-1 for anomaly, 1 for normal).
        scores (numpy.ndarray): Anomaly scores from the model.
    """
    # Create a copy to avoid modifying the original DataFrame
    log_df = df.copy()

    # Add predictions and scores to the DataFrame
    log_df['anomaly_flag'] = predictions
    log_df['anomaly_score'] = scores

    # Filter for anomalies
    threats = log_df[log_df['anomaly_flag'] == -1]

    if not threats.empty:
        # Define the log file path
        log_filepath = 'logs/threat_log.csv'
        
        # Check if the log file already exists to decide on writing the header
        # This prevents writing headers on every append
        write_header = not os.path.exists(log_filepath)

        # Save the threats to the log file, appending if the file already exists
        threats.to_csv(log_filepath, mode='a', header=write_header, index=False)
        print(f"Logged {len(threats)} new threats to {log_filepath}")
    else:
        print("No threats detected.") 