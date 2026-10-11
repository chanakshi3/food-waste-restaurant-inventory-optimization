import pandas as pd
file_path=r"C:\Users\Dell\Desktop\Food-Waste-Restaurant-Inventory-Optimization\data\raw\restaurant_food_waste_inventory_raw.csv.csv"
df =pd.read_csv(file_path)
missing_count = df.isnull().sum()

missing_percentage = (
    df.isnull().sum() / len(df) * 100
)

missing_report = pd.DataFrame({
    "Missing_Count": missing_count,
    "Missing_Percentage": missing_percentage
})

missing_report = missing_report.sort_values(
    "Missing_Count",
    ascending=False
)

print(missing_report)