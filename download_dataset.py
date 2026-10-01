import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(BASE_DIR, "Kaggle dataset", "customer_support_tickets.csv")


if os.path.exists(csv_file):
    print(f"Loading local CSV file: {csv_file}")

    # Read using latin1 encoding and python parsing engine
    df = pd.read_csv(
        csv_file,
        encoding="latin1",
        on_bad_lines="skip",
        engine="python"
    )

    print("\nDataset successfully loaded!")
    print("Shape:", df.shape)
    print("\nColumns:\n", list(df.columns))
    print("\nFirst 5 records:")
    print(df.head())
else:
    print(f"File not found at: {csv_file}")
