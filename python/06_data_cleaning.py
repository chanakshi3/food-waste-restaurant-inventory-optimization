from pathlib import Path
import pandas as pd
import numpy as np
BASE_DIR = Path(__file__).resolve().parent.parent
input_file = BASE_DIR / "data" / "raw" / "restaurant_food_waste_inventory_raw.csv"

output_folder = BASE_DIR / "data" / "cleaned"

output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "restaurant_food_waste_inventory_cleaned.csv"

print("Input file:", input_file)
print("Output folder:", output_folder)


#1 load data
df =pd.read_csv(input_file)
print("orignal shape",df.shape)

#2 remove duplicates
duplicate_count= df.duplicated().sum()
print("duplicates found:",duplicate_count)

#3 clean column names
df.columns =(df.columns
             .str.strip()
             .str.lower()
             .str.replace(" ","_"))
print("\ncleaned column names:")
print(df.columns.tolist())

#4 clean text columns
text_columns = [
    "restaurant_name",
    "city",
    "restaurant_type",
    "ingredient_category",
    "ingredient",
    "supplier",
    "unit",
    "waste_reason",
    "storage_type",
    "stockout_flag",
    "quality_status",
    "event_type"
]

for column in text_columns:

    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
        .str.lower()
    )

#5 standarized missing values
missing_values=["","na","n/a","_","unknown","none"]
df=df.replace(missing_values,pd.NA)

#6 convert dates columns
# 6. Convert date columns

def convert_mixed_date(value):
    
    if pd.isna(value):
        return pd.NaT
    
    value = str(value).strip()
    
    # Try different date formats
    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%m-%d-%Y",
        "%d-%b-%Y",
        "%d-%B-%Y"
    ]
    
    for fmt in formats:
        try:
            return pd.to_datetime(value, format=fmt)
        except:
            pass
    
    return pd.NaT


df["transaction_date"] = df["transaction_date"].apply(
    convert_mixed_date
)

df["expiry_date"] = df["expiry_date"].apply(
    convert_mixed_date
)

print(
    "\nMissing transaction dates:",
    df["transaction_date"].isna().sum()
)

print(
    "Missing expiry dates:",
    df["expiry_date"].isna().sum()
)
#7 convert numeric columns
numeric_columns =["opening_stock",
    "received_qty",
    "used_qty",
    "wasted_qty",
    "closing_stock",
    "unit_cost_inr",
    "waste_cost_inr",
    "food_sales_inr",
    "covers",
    "prep_qty",
    "shelf_life_days",
    "storage_temperature_c",
    "supplier_lead_time_days",
    "reorder_level"
]
for column in numeric_columns:
    df[column]=pd.to_numeric(
        df[column],errors="coerce"
    )

#handle invalid negative stock values
stock_columns=[ "opening_stock",
    "received_qty",
    "used_qty",
    "wasted_qty",
    "closing_stock"]
for column in stock_columns:
    invalid_count=(df[column]<0).sum()
    print(f"{column}:{invalid_count}negative values")
    df.loc[df[column]<0,
           column] =np.nan

#9 handle missing numeric values
for column in numeric_columns:

    if df[column].isnull().sum() > 0:

        median_value = df[column].median()

        df[column] = df[column].fillna(
            median_value
        )

#10 handle missing text values
df["supplier"] = df["supplier"].fillna(
    "unknown supplier")

df["waste_reason"] = df["waste_reason"].fillna(
    "not recorded")

df["quality_status"] = df["quality_status"].fillna(
    "not recorded")

#11 standarized units
df["unit"] = df["unit"].replace({
    "kg": "kg",
    "kg ": "kg",
    "l": "litre",
    "litre": "litre",
    "pack": "pack"
})

#12 calculate waste cost
df["calculated_waste_cost"] = (
    df["wasted_qty"] *
    df["unit_cost_inr"]
)

#13 waste percentage
available_stock = (
    df["opening_stock"] +
    df["received_qty"]
)

df["waste_percentage"] = np.where(
    available_stock > 0,
    (
        df["wasted_qty"] /
        available_stock
    ) * 100,
    0
)

#14 inventory value
df["inventory_value"] = (
    df["closing_stock"] *
    df["unit_cost_inr"]
)

#15 inventory variance
df["expected_closing_stock"] = (
    df["opening_stock"] +
    df["received_qty"] -
    df["used_qty"] -
    df["wasted_qty"]
)

df["inventory_variance"] = (
    df["closing_stock"] -
    df["expected_closing_stock"]
)

#16 days until expiry
df["days_until_expiry"] = (
    df["expiry_date"] -
    df["transaction_date"]
).dt.days
df["expiry_risk"] = np.select(
    [
        df["days_until_expiry"] <= 2,
        df["days_until_expiry"] <= 5,
        df["days_until_expiry"] <= 10
    ],
    [
        "critical",
        "high",
        "medium"
    ],
    default="low"
)

#17 stock status
def get_stock_status(row):

    if row["closing_stock"] <= 0:
        return "out of stock"

    elif row["closing_stock"] <= row["reorder_level"]:
        return "reorder"

    elif row["closing_stock"] > row["reorder_level"] * 2:
        return "overstocked"

    else:
        return "optimal"


df["stock_status"] = df.apply(
    get_stock_status,
    axis=1
)

#18 day type
#18 day type

df["day_type"] = np.where(
    df["transaction_date"].dt.dayofweek >= 5,
    "weekend",
    "weekday"
)

#19 potential savings
df["potential_savings_20pct"] = (
    df["calculated_waste_cost"] * 0.20
)

#20 reorder recommendation
df["average_daily_usage"] = (
    df["used_qty"]
)

df["lead_time_demand"] = (
    df["average_daily_usage"] *
    df["supplier_lead_time_days"]
)

df["safety_stock"] = (
    df["average_daily_usage"] * 2
)

df["recommended_reorder_point"] = (
    df["lead_time_demand"] +
    df["safety_stock"]
)
def inventory_recommendation(row):

    if row["days_until_expiry"] <= 2:
        return "use first"

    elif row["closing_stock"] <= 0:
        return "urgent reorder"

    elif (
        row["closing_stock"] <
        row["recommended_reorder_point"]
    ):
        return "reorder soon"

    elif (
        row["closing_stock"] >
        row["reorder_level"] * 2
    ):
        return "reduce purchase"

    else:
        return "optimal"


df["inventory_recommendation"] = df.apply(
    inventory_recommendation,
    axis=1
)

#21 save clean data

# Save CSV file
df.to_csv(
    output_file,
    index=False
)

# Save Excel file for Power BI
final_excel_file = (
    BASE_DIR
    / "data"
    / "cleaned"
    / "inventory final.xlsx"
)

df.to_excel(
    final_excel_file,
    index=False
)

print("\nCleaning completed!")
print("Final dataset shape:", df.shape)
print("CSV saved to:", output_file)
print("Excel saved to:", final_excel_file)#21 save clean data

# Save CSV file
df.to_csv(
    output_file,
    index=False
)

# Save Excel file for Power BI
final_excel_file = (
    BASE_DIR
    / "data"
    / "cleaned"
    / "inventory final.xlsx"
)

df.to_excel(
    final_excel_file,
    index=False
)

print("\nCleaning completed!")
print("Final dataset shape:", df.shape)
print("CSV saved to:", output_file)
print("Excel saved to:", final_excel_file)