import gzip
import shutil
from pathlib import Path

source = Path("data/raw/bookings.csv.gz")
target = Path("data/raw/bookings.csv")

if not source.exists():
    print(f"File not found: {source}")
else:
    try:
        with gzip.open(source, "rb") as compressed:
            with open(target, "wb") as extracted:
                shutil.copyfileobj(compressed, extracted)

        print("Bookings successfully extracted to bookings.csv")

    except Exception as error:
        print(f"Error: {error}")