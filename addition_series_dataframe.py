
import pandas as pd

# 1. Create a DataFrame representing item prices over 3 months
df = pd.DataFrame({
    'Apples': [3, 4, 5],
    'Bananas': [5, 6, 5]
}, index=['Jan', 'Feb', 'Mar'])

# 2. Create a Series representing a flat inflation tax for each item
# Note: The index names of the Series must match the column names of the DataFrame
tax = pd.Series([2, 1], index=['Apples', 'Bananas'])

# 3. Add them together
result = df + tax
print("DataFrame:")
print(df)
print("\nPlus Series:")
print(tax)
print("\nResult (Tax added to every row):")
print(result)
