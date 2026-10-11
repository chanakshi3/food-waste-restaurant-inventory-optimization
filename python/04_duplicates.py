import pandas as pd
file_path=r"C:\Users\Dell\Desktop\Food-Waste-Restaurant-Inventory-Optimization\data\raw\restaurant_food_waste_inventory_raw.csv.csv"
df =pd.read_csv(file_path)
duplicates = df.duplicated().sum()

print("Total duplicate records:", duplicates)