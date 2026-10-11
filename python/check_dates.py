import pandas as pd
raw_file=r"C:\Users\Dell\Desktop\Food-Waste-Restaurant-Inventory-Optimization\data\raw\restaurant_food_waste_inventory_raw.csv"
df= pd.read_csv(raw_file)


print("Total rows:", len(df))

print("\nTransaction Date:")
print(df["Transaction_Date"].head(20))

print("\nMissing transaction dates:")
print(df["Transaction_Date"].isna().sum())

print("\nMissing percentage:")
print(
    round(
        df["Transaction_Date"].isna().sum() / len(df) * 100,
        2
    ),
    "%"
)