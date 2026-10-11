import pandas as pd
file_path = (r"C:\Users\Dell\Desktop\Food-Waste-Restaurant-Inventory-Optimization\data\cleaned\restaurant_food_waste_inventory_cleaned.csv")
df =pd.read_csv(file_path)
report =pd.DataFrame({
    "column":df.columns,
    "Data_Type": df.dtypes.astype(str).values,
    "Missing_Count": df.isnull().sum().values,
    "Missing_Percentage": (
        df.isnull().sum().values /
        len(df) * 100
    ),
    "Unique_Values": [
        df[col].nunique()
        for col in df.columns
    ]
})
report.to_csv(
    r"C:\Users\Dell\Desktop\Food-Waste-Restaurant-Inventory-Optimization\data\cleaned\data_quality_report.csv",
    index=False
)

print(report)
print("\nData quality report saved.")

