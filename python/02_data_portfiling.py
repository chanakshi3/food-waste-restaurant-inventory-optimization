import pandas as pd
file_path=r"C:\Users\Dell\Desktop\Food-Waste-Restaurant-Inventory-Optimization\data\raw\restaurant_food_waste_inventory_raw.csv.csv"
df =pd.read_csv(file_path)
print("=" * 60)
print("DATASET SHAPE")
print("=" * 60)

print(df.shape)


print("\n" + "=" * 60)
print("DATA TYPES")
print("=" * 60)

print(df.dtypes)


print("\n" + "=" * 60)
print("DATASET INFORMATION")
print("=" * 60)

print(df.info())


print("\n" + "=" * 60)
print("STATISTICAL SUMMARY")
print("=" * 60)

print(df.describe())


print("\n" + "=" * 60)
print("FIRST 10 RECORDS")
print("=" * 60)

print(df.head(10))