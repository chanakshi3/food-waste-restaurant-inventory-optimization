import pandas as pd
import numpy as np

df = pd.read_csv(r"C:\Users\Dell\Desktop\Food-Waste-Restaurant-Inventory-Optimization\data\cleaned\restaurant_food_waste_inventory_cleaned.csv")

df["transaction_date"] = pd.to_datetime(
    df["transaction_date"]
)

#calculate average daily usage
df["average_daily_usage"] = (
    df["used_qty"]
)

#calculate lead-time demand
df["lead_time_demand"] = (
    df["average_daily_usage"] *
    df["supplier_lead_time_days"]
)

#calculate safety stock
df["safety_stock"] = (
    df["average_daily_usage"] * 2
)

#calculate recommended reorder point
df["recommended_reorder_point"] = (
    df["lead_time_demand"] +
    df["safety_stock"]
)

#create final inventory reccomendation
def inventory_recommendation(row):

    if row["days_until_expiry"] <= 2:
        return "USE FIRST"

    elif row["closing_stock"] <= 0:
        return "URGENT REORDER"

    elif (
        row["closing_stock"] <
        row["recommended_reorder_point"]
    ):
        return "REORDER SOON"

    elif (
        row["closing_stock"] >
        row["reorder_level"] * 2
    ):
        return "REDUCE PURCHASE"

    else:
        return "OPTIMAL"


df["inventory_recommendation"] = df.apply(
    inventory_recommendation,
    axis=1
)

#calculate potential savings
df["potential_savings_20pct"] = (
    df["calculated_waste_cost"] * 0.20
)
#total
total_potential_savings = (
    df["potential_savings_20pct"].sum()
)

print(
    "Potential Savings:",
    round(
        total_potential_savings,
        2
    )
)
output_file = r"C:\Users\Dell\Desktop\Food-Waste-Restaurant-Inventory-Optimization\data\cleaned\restaurant_inventory_final.csv"

df.to_csv(
    output_file,
    index=False
)

print("Final analytics dataset saved!")


print(df.shape)

print(df.columns.tolist())

print(df.head())

print(df.isnull().sum())