
import sqlite3
import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_DIR / "data" / "processed" / "customers_clean.csv"
DB_FILE = PROJECT_DIR / "data" / "safarilink.db"

if not CSV_FILE.exists():
    raise FileNotFoundError(f"Could not find: {CSV_FILE}")

customers = pd.read_csv(CSV_FILE)

with sqlite3.connect(DB_FILE) as connection:
    customers.to_sql(
        "customers",
        connection,
        if_exists="replace",
        index=False
    )

    print(f"Imported {len(customers):,} customers successfully.")
    print("Customer table created in safarilink.db.")
