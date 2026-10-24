
import sqlite3
import pandas as pd
from pathlib import Path

# Find the project folder automatically
PROJECT_DIR = Path(__file__).resolve().parent.parent

# File locations
CSV_FILE = PROJECT_DIR / "data" / "processed" / "bookings_clean.csv"
DB_FILE = PROJECT_DIR / "data" / "safarilink.db"

print("Starting SafariLink data import...")

# Check that the CSV exists
if not CSV_FILE.exists():
    raise FileNotFoundError(f"Could not find: {CSV_FILE}")

# Connect to the SQLite database
connection = sqlite3.connect(DB_FILE)

try:
    # Import the cleaned bookings into SQLite
    bookings = pd.read_csv(CSV_FILE)

    bookings.to_sql(
        "bookings",
        connection,
        if_exists="replace",
        index=False,
        chunksize=10000
    )

    print(f"Import complete: {len(bookings):,} bookings loaded.")
    print(f"Database location: {DB_FILE}")

finally:
    connection.close()
