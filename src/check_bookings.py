import pandas as pd

bookings = pd.read_csv("data/raw/bookings.csv")

print("\nFirst 5 bookings:")
print(bookings.head())

print("\nDataset size (rows, columns):")
print(bookings.shape)

print("\nColumn names:")
print(bookings.columns.tolist())

print("\nMissing values per column:")
print(bookings.isnull().sum())