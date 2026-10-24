
"""
SafariLink Transport Intelligence
Milestone 2: Data Cleaning and Preparation

This script cleans the generated data and saves the results
in the data/processed folder.
"""

import pandas as pd
from pathlib import Path


# STEP 1: Set up the project folders
# --------------------------------------------------

# Find the main project folder automatically.
PROJECT_FOLDER = Path(__file__).resolve().parent.parent

RAW_FOLDER = PROJECT_FOLDER / "data" / "raw"
OUTPUT_FOLDER = PROJECT_FOLDER / "data" / "processed"

# Create the output folder if it does not exist.
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


# STEP 2: Load the raw datasets
# --------------------------------------------------

# Read the normal CSV if available; otherwise use the

# Load the latest generated bookings file
bookings_file = RAW_FOLDER / "bookings.csv.gz"

if not bookings_file.exists():
    bookings_file = RAW_FOLDER / "bookings.csv"

if not bookings_file.exists():
    raise FileNotFoundError(
        "Bookings file not found in data/raw. "
        "Check that bookings.csv.gz or bookings.csv exists."
    )

bookings = pd.read_csv(bookings_file)
print(f"Bookings source file: {bookings_file}")

customers = pd.read_csv(RAW_FOLDER / "customers.csv")
routes = pd.read_csv(RAW_FOLDER / "routes.csv")
branches = pd.read_csv(RAW_FOLDER / "branches.csv")
holidays = pd.read_csv(RAW_FOLDER / "holidays.csv")


# Store data-cleaning issues and actions
cleaning_log = []

def record_issue(issue, rows_affected, action):
    cleaning_log.append({
        "issue": issue,
        "rows_affected": int(rows_affected),
        "action": action
    })
      
# STEP 3: Remove duplicate booking records
# --------------------------------------------------

# Remove rows that are identical in every column.
duplicate_rows = bookings.duplicated().sum()

record_issue(
    "Exact duplicate rows",
    duplicate_rows,
    "Removed duplicate rows and kept the first occurrence"
)

bookings = bookings.drop_duplicates().copy()

# Check for repeated booking IDs, even if the rows differ.
duplicate_ids = bookings["booking_id"].duplicated().sum()

record_issue(
    "Repeated booking IDs",
    duplicate_ids,
    "Kept the first record for each booking ID"
)

bookings = bookings.drop_duplicates(
    subset=["booking_id"],
    keep="first"
).copy()

assert bookings["booking_id"].is_unique


# STEP 4: Clean booking dates
# --------------------------------------------------

# First, try the year-month-day format.
date_iso = pd.to_datetime(
    bookings["date"],
    format="%Y-%m-%d",
    errors="coerce"
)

# Next, try day/month/year for dates that did not parse.
date_dmy = pd.to_datetime(
    bookings["date"],
    format="%d/%m/%Y",
    errors="coerce"
)

# Use the first successful conversion.
bookings["date"] = date_iso.fillna(date_dmy)

invalid_dates = bookings["date"].isna().sum()

record_issue(
    "Missing or invalid booking dates",
    invalid_dates,
    "Removed rows with dates that could not be interpreted"
)

bookings = bookings.dropna(subset=["date"]).copy()


# STEP 5: Standardise payment methods
# --------------------------------------------------

# Remove extra spaces and convert labels to lowercase.
original_payment = bookings["payment"].copy()

bookings["payment"] = (
    bookings["payment"]
    .astype("string")
    .str.strip()
    .str.lower()
)

# Standardise common variations.
bookings["payment"] = bookings["payment"].replace({
    "m-pesa": "mpesa",
    "m pesa": "mpesa",
    "m_pesa": "mpesa",
    "mobile money": "mpesa"
})

changed_labels = (
    original_payment.notna()
    & original_payment.astype("string").ne(bookings["payment"])
).sum()

record_issue(
    "Inconsistent payment labels",
    changed_labels,
    "Standardised payment labels"
)

missing_payment = bookings["payment"].isna().sum()

record_issue(
    "Missing payment methods",
    missing_payment,
    "Labelled missing payment methods as unknown"
)

bookings["payment"] = bookings["payment"].fillna("unknown")


# STEP 6: Handle missing customer IDs
# --------------------------------------------------

# A booking without a customer ID is treated as a guest booking.
bookings["is_guest"] = bookings["customer_id"].isna()

missing_customer = bookings["is_guest"].sum()

record_issue(
    "Missing customer IDs",
    missing_customer,
    "Flagged bookings as guest bookings"
)

# Convert IDs to numeric values while preserving missing values.
bookings["customer_id"] = pd.to_numeric(
    bookings["customer_id"],
    errors="coerce"
).astype("Int64")

# Check missing customer IDs.
print("Missing customer IDs:", bookings["customer_id"].isna().sum())

# STEP 7: Check and correct fares
# --------------------------------------------------

# Attach the standard fare for each route.
bookings = bookings.merge(
    routes[["route_id", "base_fare"]],
    on="route_id",
    how="left",
    validate="many_to_one"
)

# Keep the original fare for comparison and auditing.
bookings["fare_raw"] = pd.to_numeric(
    bookings["fare"],
    errors="coerce"
)

bookings["fare"] = bookings["fare_raw"].copy()

# Convert negative fares to positive values.
negative_fares = bookings["fare"] < 0

record_issue(
    "Negative fares",
    negative_fares.sum(),
    "Converted negative fares to positive values"
)

bookings.loc[negative_fares, "fare"] = (
    bookings.loc[negative_fares, "fare"].abs()
)

# Remove zero, missing or invalid fares.
invalid_fares = (
    bookings["fare"].isna()
    | (bookings["fare"] == 0)
    | bookings["base_fare"].isna()
    | (bookings["base_fare"] <= 0)
)

record_issue(
    "Zero, missing or invalid fares",
    invalid_fares.sum(),
    "Removed records without a valid positive fare and base fare"
)

bookings = bookings.loc[~invalid_fares].copy()

# Check for fares more than three times the route's base fare.
fare_ratio = bookings["fare"] / bookings["base_fare"]
high_fares = fare_ratio > 3

record_issue(
    "Fares more than three times the base fare",
    high_fares.sum(),
    "Divided by ten as a suspected decimal-shift correction"
)

bookings.loc[high_fares, "fare"] = (
    bookings.loc[high_fares, "fare"] / 10
)

# Check again after the correction.
fare_ratio = bookings["fare"] / bookings["base_fare"]

unusual_fares = (
    (fare_ratio > 1.6)
    | (fare_ratio < 0.5)
)

record_issue(
    "Fares outside the accepted 0.5–1.6 base-fare range",
    unusual_fares.sum(),
    "Removed fares outside the chosen validation range"
)

bookings = bookings.loc[~unusual_fares].copy()

# Flag records where the fare was changed.
bookings["fare_flag_corrected"] = (
    bookings["fare"] != bookings["fare_raw"]
)

# STEP 8: Check business rules
# --------------------------------------------------

# Compare the booking branch with the route's origin branch.
branch_check = bookings.merge(
    routes[["route_id", "origin_branch_id"]],
    on="route_id",
    how="left",
    validate="many_to_one"
)

wrong_branch = (
    branch_check["branch_id"]
    != branch_check["origin_branch_id"]
)

record_issue(
    "Bookings assigned to a branch other than the route origin",
    wrong_branch.sum(),
    "Flagged for investigation"
)

# Check that the number of seats is between one and four.
bookings["seats"] = pd.to_numeric(
    bookings["seats"],
    errors="coerce"
)

invalid_seats = (
    bookings["seats"].isna()
    | (bookings["seats"] < 1)
    | (bookings["seats"] > 4)
    | (bookings["seats"] % 1 != 0)
)

record_issue(
    "Invalid seat counts",
    invalid_seats.sum(),
    "Removed records with invalid seat counts"
)

bookings = bookings.loc[~invalid_seats].copy()
bookings["seats"] = bookings["seats"].astype(int)

# Check whether each non-missing customer ID exists.
unknown_customer = (
    bookings["customer_id"].notna()
    & ~bookings["customer_id"].isin(customers["customer_id"])
)

record_issue(
    "Customer IDs missing from the customer dataset",
    unknown_customer.sum(),
    "Flagged for investigation"
)

# STEP 9: Clean customer information
# --------------------------------------------------

customers["signup_date"] = pd.to_datetime(
    customers["signup_date"],
    errors="coerce"
)

customers["churn_date"] = pd.to_datetime(
    customers["churn_date"],
    errors="coerce"
).dt.normalize()

# The dataset ends on 30 September 2026.
data_end_date = pd.Timestamp("2026-09-30")

# Future churn dates cannot confirm churn within our dataset.
future_churn = customers["churn_date"] > data_end_date

record_issue(
    "Churn dates beyond the data period",
    future_churn.sum(),
    "Set future churn dates to missing because churn is unconfirmed"
)

customers.loc[future_churn, "churn_date"] = pd.NaT

customers["churned"] = customers["churn_date"].notna()

# Calculate customer tenure up to churn or the end of the dataset.
customers["tenure_days"] = (
    customers["churn_date"]
    .fillna(data_end_date)
    - customers["signup_date"]
).dt.days


# STEP 10: Check booking dates against customer history
# --------------------------------------------------

customer_dates = bookings.merge(
    customers[["customer_id", "signup_date", "churn_date"]],
    on="customer_id",
    how="left",
    validate="many_to_one"
)

before_signup = (
    customer_dates["signup_date"].notna()
    & (
        customer_dates["date"]
        < customer_dates["signup_date"]
    )
)

after_churn = (
    customer_dates["churn_date"].notna()
    & (
        customer_dates["date"]
        > customer_dates["churn_date"]
    )
)

record_issue(
    "Bookings before customer signup",
    before_signup.sum(),
    "Flagged for investigation; retained for review"
)

record_issue(
    "Bookings after customer churn",
    after_churn.sum(),
    "Flagged for investigation; retained for review"
)

# Save flags against the same booking row order.
bookings["flag_pre_signup"] = before_signup.to_numpy()
bookings["flag_post_churn"] = after_churn.to_numpy()


# STEP 11: Create useful analysis columns
# --------------------------------------------------

# Revenue is fare per seat multiplied by the number of seats.
bookings["revenue"] = bookings["fare"] * bookings["seats"]

bookings["year"] = bookings["date"].dt.year
bookings["month"] = bookings["date"].dt.month

# Year and month together, e.g. 2026-09.
bookings["year_month"] = (
    bookings["date"].dt.to_period("M").astype(str)
)

bookings["day_of_week"] = bookings["date"].dt.day_name()
bookings["is_weekend"] = bookings["date"].dt.dayofweek >= 5
bookings["quarter"] = bookings["date"].dt.quarter
bookings["week"] = bookings["date"].dt.isocalendar().week.astype(int)
bookings["is_december"] = bookings["month"] == 12

bookings["price_index"] = (
    bookings["fare"] / bookings["base_fare"]
)

# Mark bookings that fall on a listed holiday.
holidays["date"] = pd.to_datetime(
    holidays["date"],
    errors="coerce"
).dt.normalize()

holiday_dates = set(holidays["date"].dropna())

bookings["is_holiday"] = (
    bookings["date"].dt.normalize().isin(holiday_dates)
)

# Mark bookings within three days before or after a holiday.
holiday_window = set()

for holiday_date in holiday_dates:
    for day_offset in range(-3, 4):
        holiday_window.add(
            holiday_date + pd.Timedelta(days=day_offset)
        )

bookings["near_holiday"] = (
    bookings["date"].dt.normalize().isin(holiday_window)
)


# STEP 12: Combine the cleaned datasets
# --------------------------------------------------

# Add route information to every booking.
clean_bookings = bookings.drop(
    columns=["base_fare"]
).merge(
    routes.drop(columns=["origin_branch_id"]),
    on="route_id",
    how="left",
    validate="many_to_one"
)

# Add branch information.
clean_bookings = clean_bookings.merge(
    branches,
    on="branch_id",
    how="left",
    validate="many_to_one"
)

# Create a readable route name.
clean_bookings["route"] = (
    clean_bookings["origin"]
    + " - "
    + clean_bookings["destination"]
)

#
# Add customer information without removing guest bookings.
bookings = bookings.merge(
    customers[
        [
            "customer_id",
            "segment",
            "home_branch_id",
            "signup_date",
            "churned"
        ]
    ],
    on="customer_id",
    how="left",
    validate="many_to_one"
)

# Label bookings with no known customer segment.
bookings["segment"] = bookings["segment"].fillna("Guest / Unknown")


# STEP 13: Save the cleaned datasets and cleaning log
# --------------------------------------------------

clean_bookings.to_csv(
    OUTPUT_FOLDER / "bookings_clean.csv",
    index=False
)

customers.to_csv(
    OUTPUT_FOLDER / "customers_clean.csv",
    index=False
)

cleaning_log_df = pd.DataFrame(cleaning_log)

cleaning_log_df.to_csv(
    OUTPUT_FOLDER / "cleaning_log.csv",
    index=False
)


# STEP 14: Print a summary
# --------------------------------------------------

print("\nDATA CLEANING COMPLETED")
print("-----------------------")

print("Cleaned bookings:", len(clean_bookings))
print("Columns:", len(clean_bookings.columns))
print("First booking date:", clean_bookings["date"].min())
print("Last booking date:", clean_bookings["date"].max())
print("Total calculated revenue:", round(clean_bookings["revenue"].sum(), 2))

print("\nCLEANING LOG")
print("------------")
print(cleaning_log_df.to_string(index=False))

print("\nMissing values in cleaned bookings:")
print(
    clean_bookings.isna().sum()[
        clean_bookings.isna().sum() > 0
    ]
)

print("\nSaved files in:", OUTPUT_FOLDER)
