import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv(r"C:\Users\Dell\Desktop\Food-Waste-Restaurant-Inventory-Optimization\data\cleaned\restaurant_food_waste_inventory_cleaned.csv")
df["transaction_date"] = pd.to_datetime(
    df["transaction_date"]
)

print(df.head())

#basic kpis
print("\nTOTAL RECORDS:")
print(len(df))

print("\nTOTAL WASTE:")
print(df["wasted_qty"].sum())

print("\nTOTAL WASTE COST:")
print(df["calculated_waste_cost"].sum())

print("\nTOTAL FOOD SALES:")
print(df["food_sales_inr"].sum())

print("\nTOTAL INVENTORY VALUE:")
print(df["inventory_value"].sum())

print("\nTOTAL COVERS:")
print(df["covers"].sum())

#calculate overall waste rate
total_available =(df["opening_stock"].sum()+df["received_qty"].sum())
total_waste = df["wasted_qty"].sum()
overall_waste_rate = (
    total_waste /
    total_available
) * 100

print(
    "Overall Waste Rate:",
    round(overall_waste_rate, 2),
    "%"
)

#analyze waste by ingredient
waste_by_ingredient = (
    df.groupby("ingredient")
    .agg(
        waste_qty=("wasted_qty", "sum"),
        waste_cost=(
            "calculated_waste_cost",
            "sum"
        )
    )
    .sort_values(
        "waste_cost",
        ascending=False
    )
)

print(
    waste_by_ingredient.head(15)
)
#plot
plt.figure(figsize=(12, 6))

waste_by_ingredient.head(10)["waste_cost"].plot(kind="bar")

plt.title("Top 10 Ingredients by Waste Cost")
plt.xlabel("Ingredient")
plt.ylabel("Waste Cost (INR)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    r"C:\Users\Dell\Desktop\Food-Waste-Restaurant-Inventory-Optimization\images\top_10_waste_ingredients.png"
)

plt.show()

#waste by category
category_analysis = (
    df.groupby("ingredient_category")
    .agg(
        waste_qty=("wasted_qty", "sum"),
        waste_cost=(
            "calculated_waste_cost",
            "sum"
        ),
        sales=(
            "food_sales_inr",
            "sum"
        )
    )
)

category_analysis["waste_percentage"] = (
    category_analysis["waste_cost"] /
    category_analysis["sales"] *
    100
)

print(category_analysis)
#plot
plt.figure(figsize=(10, 6))

category_analysis[
    "waste_cost"
].sort_values(
    ascending=False
).plot(kind="bar")

plt.title(
    "Waste Cost by Ingredient Category"
)

plt.xlabel("Ingredient Category")
plt.ylabel("Waste Cost (INR)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    r"C:\Users\Dell\Desktop\Food-Waste-Restaurant-Inventory-Optimization\images\waste_by_category.png"
)

plt.show()

#waste by restaurant
restaurant_analysis = (
    df.groupby("restaurant_name")
    .agg(
        waste_qty=("wasted_qty", "sum"),
        waste_cost=(
            "calculated_waste_cost",
            "sum"
        ),
        sales=(
            "food_sales_inr",
            "sum"
        ),
        inventory_value=(
            "inventory_value",
            "sum"
        )
    )
)

restaurant_analysis[
    "waste_percentage"
] = (
    restaurant_analysis["waste_cost"] /
    restaurant_analysis["sales"] *
    100
)

print(
    restaurant_analysis.sort_values(
        "waste_cost",
        ascending=False
    )
)

#waste by reason
reason_analysis = (
    df.groupby("waste_reason")
    .agg(
        waste_qty=("wasted_qty", "sum"),
        waste_cost=(
            "calculated_waste_cost",
            "sum"
        )
    )
    .sort_values(
        "waste_cost",
        ascending=False
    )
)

print(reason_analysis)
#plot
plt.figure(figsize=(12, 6))

reason_analysis[
    "waste_cost"
].plot(kind="bar")

plt.title(
    "Food Waste Cost by Reason"
)

plt.ylabel("Waste Cost (INR)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
     r"C:\Users\Dell\Desktop\Food-Waste-Restaurant-Inventory-Optimization\images\waste_by_reason.png"
    
)

plt.show()

#monthly waste trend
df["month"] = (
    df["transaction_date"]
    .dt.to_period("M")
)

monthly_waste = (
    df.groupby("month")
    .agg(
        waste_qty=(
            "wasted_qty",
            "sum"
        ),
        waste_cost=(
            "calculated_waste_cost",
            "sum"
        ),
        sales=(
            "food_sales_inr",
            "sum"
        )
    )
)

print(monthly_waste)
#plot
plt.figure(figsize=(14, 6))

plt.plot(
    monthly_waste.index.astype(str),
    monthly_waste["waste_cost"],
    marker="o"
)

plt.title(
    "Monthly Food Waste Cost Trend"
)

plt.xlabel("Month")
plt.ylabel("Waste Cost (INR)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    r"C:\Users\Dell\Desktop\Food-Waste-Restaurant-Inventory-Optimization\images\monthly_waste_trend.png"
    
)

plt.show()

#weekend vs weekday analysis
day_analysis = (
    df.groupby("day_type")
    .agg(
        waste_qty=(
            "wasted_qty",
            "sum"
        ),
        waste_cost=(
            "calculated_waste_cost",
            "sum"
        ),
        sales=(
            "food_sales_inr",
            "sum"
        )
    )
)

day_analysis["waste_percentage"] = (
    day_analysis["waste_cost"] /
    day_analysis["sales"] *
    100
)

print(day_analysis)

#event analysis
event_analysis = (
    df.groupby("event_type")
    .agg(
        waste_qty=(
            "wasted_qty",
            "sum"
        ),
        waste_cost=(
            "calculated_waste_cost",
            "sum"
        ),
        sales=(
            "food_sales_inr",
            "sum"
        )
    )
)

event_analysis["waste_percentage"] = (
    event_analysis["waste_cost"] /
    event_analysis["sales"] *
    100
)

print(event_analysis)

#supplier analysis
supplier_analysis = (
    df.groupby("supplier")
    .agg(
        received_qty=(
            "received_qty",
            "sum"
        ),
        waste_qty=(
            "wasted_qty",
            "sum"
        ),
        waste_cost=(
            "calculated_waste_cost",
            "sum"
        ),
        average_lead_time=(
            "supplier_lead_time_days",
            "mean"
        )
    )
)

supplier_analysis[
    "waste_rate"
] = (
    supplier_analysis["waste_qty"] /
    supplier_analysis["received_qty"] *
    100
)

print(
    supplier_analysis.sort_values(
        "waste_rate",
        ascending=False
    )
)

#inventory status analysis
stock_analysis =(
    df.groupby("stock_status")
    .agg(
        records =("record_id", "count"),
        inventory_value=(
            "inventory_value",
            "sum"
        )
    )
)

print(stock_analysis)

#expiry risk analysis
expiry_analysis = (
    df.groupby("expiry_risk")
    .agg(
        records=("record_id", "count"),
        inventory_value=(
            "inventory_value",
            "sum"
        )
    )
)

print(expiry_analysis)