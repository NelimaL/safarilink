
from pathlib import Path

import pandas as pd
from scipy import stats

# 1. Load the cleaned bookings data
DATA_FILE = Path("data/processed/bookings_clean.csv")

df = pd.read_csv(DATA_FILE, usecols=["booking_id", "payment", "fare"])

# 2. Clean the fields used in the test
df["payment"] = df["payment"].astype("string").str.strip().str.lower()
df["fare"] = pd.to_numeric(df["fare"], errors="coerce")

df = df.dropna(subset=["payment", "fare"])
df = df[df["fare"] > 0]

# 3. Select M-Pesa and cash bookings
mpesa = df.loc[df["payment"] == "mpesa", "fare"]
cash = df.loc[df["payment"] == "cash", "fare"]

# Check the actual payment labels if a group is missing
if mpesa.empty or cash.empty:
    print("Payment labels found in the data:")
    print(df["payment"].value_counts().to_string())
    raise ValueError(
        "M-Pesa or cash group is empty. Check the labels above "
        "and update the group filters."
    )

# 4. State the hypotheses
# H0: The population mean fares are equal.
# H1: The population mean fares are different.

# 5. Calculate group summaries
print("FARE COMPARISON: M-PESA VS CASH")
print("-" * 40)
print(f"M-Pesa bookings: {len(mpesa):,}")
print(f"Cash bookings:   {len(cash):,}")
print(f"M-Pesa mean fare: KES {mpesa.mean():,.2f}")
print(f"Cash mean fare:   KES {cash.mean():,.2f}")
print(f"Mean difference (M-Pesa - cash): "
      f"KES {mpesa.mean() - cash.mean():,.2f}")

# 6. Welch's independent-samples t-test
result = stats.ttest_ind(mpesa, cash, equal_var=False)
print(f"\nWelch t-statistic: {result.statistic:.4f}")
print(f"Two-sided p-value: {result.pvalue:.6g}")

# 7. Calculate a 95% confidence interval for the mean difference
mean_diff = mpesa.mean() - cash.mean()
var_mpesa = mpesa.var(ddof=1)
var_cash = cash.var(ddof=1)
n_mpesa = len(mpesa)
n_cash = len(cash)

se = ((var_mpesa / n_mpesa) + (var_cash / n_cash)) ** 0.5

df_welch = (
    (var_mpesa / n_mpesa + var_cash / n_cash) ** 2
    / (
        (var_mpesa / n_mpesa) ** 2 / (n_mpesa - 1)
        + (var_cash / n_cash) ** 2 / (n_cash - 1)
    )
)

critical_t = stats.t.ppf(0.975, df_welch)
lower = mean_diff - critical_t * se
upper = mean_diff + critical_t * se

print(f"95% confidence interval: "
      f"KES {lower:,.2f} to KES {upper:,.2f}")

# 8. Plain-language conclusion
print("\nCONCLUSION")
if result.pvalue < 0.05:
    print("There is statistically significant evidence that the "
          "average fare differs between M-Pesa and cash bookings.")
else:
    print("There is insufficient statistical evidence to conclude "
          "that the average fare differs between M-Pesa and cash bookings.")

print("This is an association, not proof that payment method causes "
      "a difference in fare.")
