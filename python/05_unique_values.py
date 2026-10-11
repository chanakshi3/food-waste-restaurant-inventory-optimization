import pandas as pd
file_path=r"C:\Users\Dell\Desktop\Food-Waste-Restaurant-Inventory-Optimization\data\raw\restaurant_food_waste_inventory_raw.csv.csv"
df =pd.read_csv(file_path)
columns_to_check = [
    "City",
    "Restaurant_Type",
    "Ingredient_Category",
    "Ingredient",
    "Supplier",
    "Unit",
    "Waste_Reason",
    "Storage_Type",
    "Stockout_Flag",
    "Quality_Status",
    "Event_Type"
]

for column in columns_to_check:

    print("\n" + "=" * 60)
    print(column)
    print("=" * 60)

    print(df[column].value_counts(dropna=False).head(30))