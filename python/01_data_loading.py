import pandas as pd
file_path=r"C:\Users\Dell\Desktop\Food-Waste-Restaurant-Inventory-Optimization\data\raw\restaurant_food_waste_inventory_raw.csv.csv"
df =pd.read_csv(file_path)
print("Dataset loaded successfully!")
print()
print("Rows and Columns:")
print(df.shape)

print()
print("First 5 Rows:")
print(df.head())

print()
print("Column Names:")
print(df.columns.tolist())