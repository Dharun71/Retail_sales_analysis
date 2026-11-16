import pandas as pd

df = pd.read_csv("project1_cleaned.csv")

# Convert discount into percentage format
df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce")

if df["Discount"].max() > 1:
    df["Discount"] = df["Discount"] / 100

# Group discounts
df["Discount_Band"] = pd.cut(
    df["Discount"],
    bins=[-0.001, 0.05, 0.15, 0.30, 1],
    labels=["0-5%", "5-15%", "15-30%", "30%+"]
)

# Calculate only averages and totals
discount_analysis = df.groupby(
    "Discount_Band", observed=False
).agg(
    Average_Sales=("Sales", "mean"),
    Total_Sales=("Sales", "sum"),
    Average_Profit=("Profit", "mean"),
    Total_Profit=("Profit", "sum")
).round(2)

print(discount_analysis)

discount_analysis.to_csv("discount_analysis.csv")
