from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN

def train_model(X):
    """
    Trains an Isolation Forest model on the given data.

    Args:
        X (pandas.DataFrame or numpy.ndarray): The preprocessed input data for training.

    Returns:
        sklearn.ensemble.IsolationForest: The trained Isolation Forest model.
    """
    # Initialize the Isolation Forest model
    # contamination='auto' is a good starting point. The random_state is for reproducibility.
    model = IsolationForest(contamination='auto', random_state=42)
    
    # Train the model
    model.fit(X)
    
    return model

def predict_anomalies(model, X):
    """
    Predicts anomalies using a trained Isolation Forest model.

    Args:
        model (sklearn.ensemble.IsolationForest): The trained Isolation Forest model.
        X (pandas.DataFrame or numpy.ndarray): The preprocessed data for prediction.

    Returns:
        tuple: A tuple containing:
            - numpy.ndarray: Anomaly flags (1 for normal, -1 for anomaly).
            - numpy.ndarray: Anomaly scores for each data point.
    """
    # Predict anomalies (returns -1 for outliers and 1 for inliers)
    anomaly_flags = model.predict(X)
    
    # Get anomaly scores. The lower the score, the more abnormal.
    # We negate score_samples because it returns the opposite of the anomaly score.
    anomaly_scores = -model.score_samples(X)
    
    return anomaly_flags, anomaly_scores

# DBSCAN support
def train_dbscan(X, eps=0.3, min_samples=5):
    """
    Trains a DBSCAN clustering model and assigns cluster labels.

    Args:
        X (pandas.DataFrame or numpy.ndarray): The preprocessed input data for clustering.
        eps (float): The maximum distance between two samples for one to be considered as in the neighborhood of the other.
        min_samples (int): The number of samples in a neighborhood for a point to be considered as a core point.

    Returns:
        labels (numpy.ndarray): Cluster labels for each point (-1 means anomaly/outlier).
        dbscan (sklearn.cluster.DBSCAN): The fitted DBSCAN model.
    """
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(X)
    return labels, dbscan 