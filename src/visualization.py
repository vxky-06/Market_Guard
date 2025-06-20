import matplotlib.pyplot as plt
import pandas as pd
import os

def visualize_anomalies(df):
    """
    Visualizes transaction anomalies and saves the plot to a file.

    Args:
        df (pandas.DataFrame): DataFrame containing transaction data with an 'anomaly_flag' column.
    """
    if 'timestamp' not in df.columns or 'transaction_amount' not in df.columns or 'anomaly_flag' not in df.columns:
        print("DataFrame must contain 'timestamp', 'transaction_amount', and 'anomaly_flag' columns.")
        return

    # Ensure the reports directory exists
    if not os.path.exists('reports'):
        os.makedirs('reports')

    # Convert timestamp to datetime for plotting
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Separate normal and anomalous data
    normal_transactions = df[df['anomaly_flag'] == 1]
    anomalous_transactions = df[df['anomaly_flag'] == -1]

    # Create the plot
    plt.figure(figsize=(15, 7))
    plt.scatter(normal_transactions['timestamp'], normal_transactions['transaction_amount'], 
                c='blue', label='Normal', alpha=0.7)
    plt.scatter(anomalous_transactions['timestamp'], anomalous_transactions['transaction_amount'], 
                c='red', label='Anomaly', alpha=0.7, edgecolors='k', s=50)
    
    # Formatting the plot
    plt.title('Transaction Amounts Over Time with Anomaly Detection')
    plt.xlabel('Timestamp')
    plt.ylabel('Transaction Amount')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot
    save_path = 'reports/anomaly_visualization.png'
    plt.savefig(save_path)
    plt.close() # Close the plot to free up memory

    print(f"Anomaly visualization saved to {save_path}") 