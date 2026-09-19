import numpy as np
import pandas as pd

print("--- 1. CREATING A DATAFRAME ---")
# A DataFrame is essentially an Excel spreadsheet inside Python.
# We use a dictionary (key: value) where keys become column names.
raw_data = {
    "Product": ["Laptop", "Mouse", "Monitor", "Keyboard", "Mouse"],
    "Price": [999.99, 19.99, 299.99, 49.99, 19.99],
    "Units_Sold": [
        5,
        20,
        10,
        np.nan,
        20,
    ],  # np.nan or None represents a missing blank value
}
df = pd.DataFrame(raw_data)
print("Original Data Sheet:")
df.index = df.index + 1
print(df)
print("\n" + "=" * 40 + "\n")


print("--- 2. CLEANING THE DATA ---")
# Real data is messy. Let's fix missing values and duplicates.

# Fill the missing Units_Sold value with 0
df["Units_Sold"] = df["Units_Sold"].fillna(0)

# Remove the duplicate row (the second Mouse row)
df = df.drop_duplicates()

print("Cleaned Data Sheet:")
print(df)
print("\n" + "=" * 40 + "\n")


print("--- 3. ADDING A CALCULATED COLUMN ---")
# Pandas lets you do math across entire columns instantly without 'for' loops.
df["Total_Revenue"] = df["Price"] * df["Units_Sold"]

print("Data Sheet with Revenue:")
print(df)
print("\n" + "=" * 40 + "\n")


print("--- 4. FILTERING ROWS (BOOSTING SURGERY) ---")
# Let's extract only the rows where Total_Revenue is greater than $500
high_revenue_df = df[df["Total_Revenue"] > 500]

print("High Revenue Products (> $500):")
print(high_revenue_df)
print("\n" + "=" * 40 + "\n")


print("--- 5. QUICK MATHEMATICAL SUMMARY ---")
# You can instantly calculate averages, sums, or counts.
total_sales_money = df["Total_Revenue"].sum()
average_product_price = df["Price"].mean()

print(f"Total Combined Revenue: ${total_sales_money}")
print(f"Average Product Price:  ${average_product_price:.2f}")
