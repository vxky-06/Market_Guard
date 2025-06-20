import pandas as pd

def load_data(filepath):
    """
    Loads transaction data from a CSV file into a pandas DataFrame.

    Args:
        filepath (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: The loaded data as a DataFrame, or None if an error occurs.
    """
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"Error: The file at {filepath} was not found.")
        return None
    except pd.errors.ParserError:
        print(f"Error: The file at {filepath} is not a valid CSV file.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None 