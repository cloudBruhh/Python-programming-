import numpy as np
import pandas as pd

# Creating a Series
s = pd.Series(["Ashwin", "Sudin", "Bruh", ""], index=["a", "b", "c", "d"])

print(s)
s.drop("b", inplace=True)
print(s)
s.dropna()
print(s)
# Creating a DataFrame
df = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [25, 30]})
df.index = df.index + 1
print(df)
print("" + "=" * 40 + "\n")
obj = pd.Series(np.arange(5), index=["a", "b", "c", "d", "e"])
print(obj)
print("" + "=" * 40 + "\n")
obj1 = obj.drop("c")
print(obj1)
print("" + "=" * 40 + "\n")
obj2 = obj.drop(["b", "d"])
print(obj2)
