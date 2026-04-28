# src/data_processing/loader.py
import os
import pandas as pd

# Set the main project folder and the data folder
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_FOLDER = os.path.join(PROJECT_ROOT, "data")



def load_data(filename: str = "financial_transactions.csv"):
    """
    Load a CSV file and return it as a pandas DataFrame.

    - If the user does not give a filename, the function will load
      'financial_transactions.csv' from the data folder.
    - If the file does not exist, the function will raise a FileNotFoundError.
    """
    # If the user gives just a filename, look for it inside the data folder
    file_path = os.path.join(DATA_FOLDER, filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Load the file using pandas
    return pd.read_csv(file_path)
