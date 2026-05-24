import pandas as pd
import sqlite3

# Load CSV
df = pd.read_csv("D:\practice_datasets\SaaS-Sales.csv")

# Preview
print(df.head())
print(df.columns.tolist())
print(df.shape)