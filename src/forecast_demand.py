
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

# 1. Load cleaned booking data
DATA_FILE = Path("data/processed/bookings_clean.csv")
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE, usecols=["date", "booking_id"])
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])

# 2.  bookings by month
monthly = (
    df.set_index("date")
    .resample("MS")
    .size()
    .rename("bookings")
    .to_frame()
)

# 3.  features creation
monthly["lag_1"] = monthly["bookings"].shift(1)
monthly["lag_2"] = monthly["bookings"].shift(2)
monthly["lag_3"] = monthly["bookings"].shift(3)
monthly["lag_12"] = monthly["bookings"].shift(12)
monthly["month"] = monthly.index.month

model_data = monthly.dropna().copy()

if len(model_data) < 18:
    raise ValueError("Not enough monthly history for this model.")

features = ["lag_1", "lag_2", "lag_3", "lag_12", "month"]
X = model_data[features]
y = model_data["bookings"]

# 4. Time-aware split: earliest 80% train, latest 20% test
split = int(len(model_data) * 0.8)
X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]

# 5. Baseline: predict the previous month's bookings
baseline_predictions = X_test["lag_1"].to_numpy()

# 6. Train the model
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=4,
    min_samples_leaf=2,
    random_state=42
)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# 7. Evaluate both methods
def evaluate(actual, predicted):
    return {
        "MAE": mean_absolute_error(actual, predicted),
        "RMSE": np.sqrt(mean_squared_error(actual, predicted)),
    }

baseline_scores = evaluate(y_test, baseline_predictions)
model_scores = evaluate(y_test, predictions)

print("MONTHLY DEMAND FORECAST")
print("-" * 40)
print(f"Training months: {len(X_train)}")
print(f"Testing months:  {len(X_test)}")
print(f"Test period: {X_test.index.min():%Y-%m} to "
      f"{X_test.index.max():%Y-%m}")

print("\nBASELINE (previous month's demand)")
print(f"MAE:  {baseline_scores['MAE']:,.0f} bookings")
print(f"RMSE: {baseline_scores['RMSE']:,.0f} bookings")

print("\nRANDOM FOREST MODEL")
print(f"MAE:  {model_scores['MAE']:,.0f} bookings")
print(f"RMSE: {model_scores['RMSE']:,.0f} bookings")

if model_scores["MAE"] < baseline_scores["MAE"]:
    print("\nThe model has lower MAE than the baseline.")
else:
    print("\nThe model did not beat the baseline on MAE.")

# 8. Save test predictions for review
results = pd.DataFrame({
    "month": X_test.index,
    "actual_bookings": y_test.to_numpy(),
    "baseline_prediction": baseline_predictions,
    "model_prediction": predictions,
})
results["model_error"] = (
    results["actual_bookings"] - results["model_prediction"]
)
results.to_csv(OUTPUT_DIR / "forecast_evaluation.csv", index=False)

print("\nSaved predictions to data/processed/forecast_evaluation.csv")
print("\nLargest model errors:")
print(
    results.assign(
        absolute_error=results["model_error"].abs()
    )
    .nlargest(5, "absolute_error")[
        ["month", "actual_bookings", "model_prediction", "model_error"]
    ].to_string(index=False)
)
