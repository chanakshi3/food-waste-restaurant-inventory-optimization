import pandas as pd
file_path = (r"C:\Users\Dell\Desktop\Food-Waste-Restaurant-Inventory-Optimization\data\cleaned\restaurant_food_waste_inventory_cleaned.csv")
df =pd.read_csv(file_path)
print("=" * 70)
print("CLEANED DATA VALIDATION")
print("=" * 70)

#dataset size
print("\nDataset shape:")
print(df.shape)
print(f"rows:{df.shape[0]:,}")
print(f"columns:{df.shape[1]}")

#duplicates
print("\nDuplicate records:")
duplicates= df.duplicated().sum()
print(duplicates)

#missing values
print("\nmissing values:")
missing = df.isnull().sum()
print(
    missing[
        missing > 0
    ]
)

#negative stock values
stock_columns = [
    "opening_stock",
    "received_qty",
    "used_qty",
    "wasted_qty",
    "closing_stock"
]

print("\nNegative Stock Values:")

for column in stock_columns:

    negative_count = (
        df[column] < 0
    ).sum()

    print(
        f"{column}: {negative_count}"
    )

#unique values
print("\nUnique Restaurants:")
print(df["restaurant_name"].nunique())

print("\nUnique Ingredients:")
print(df["ingredient"].nunique())

print("\nUnique Suppliers:")
print(df["supplier"].nunique())

print("\nUnique Cities:")
print(df["city"].nunique())

#data types
print("\ndata types:")
print(df.dtypes)

#stock status
print("\nStock Status:")

print(
    df["stock_status"]
    .value_counts()
)

#expiry risk
print("\nExpiry Risk:")

print(
    df["expiry_risk"]
    .value_counts()
)

#final summary
print("\n" + "=" * 70)
print("VALIDATION COMPLETED")
print("=" * 70)