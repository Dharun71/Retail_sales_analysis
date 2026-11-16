import pandas as pd
import matplotlib.pyplot as plt

# 1. Load data
df = pd.read_csv("project1.csv")
print("Rows, columns:", df.shape)
print(df.head())
print("\nMissing values:\n", df.isna().sum())
print("Duplicate rows:", df.duplicated().sum())

# 2. Clean data
df = df.drop_duplicates().copy()
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce")

if df["Discount"].max() > 1:
    df["Discount"] = df["Discount"] / 100

# Keep rows with valid dates and core numeric measures
df = df.dropna(subset=["Order_Date", "Sales", "Profit", "Quantity"])
# Missing discount is filled with median and missing categories are labeled
df["Discount"] = df["Discount"].fillna(df["Discount"].median())
for col in ["Customer_Segment", "Region"]:
    df[col] = df[col].fillna("Unknown")

# 3. KPI summary
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order_ID"].nunique()
total_units = df["Quantity"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

print(f"\nTotal sales: {total_sales:,.2f}")
print(f"Total profit: {total_profit:,.2f}")
print(f"Unique orders: {total_orders:,}")
print(f"Units sold: {total_units:,}")
print(f"Profit margin: {profit_margin:.2f}%")

# 4. Category and regional analysis
print("\nBy category:\n", df.groupby("Category")[["Sales", "Profit"]].sum().sort_values("Sales", ascending=False))
print("\nBy region:\n", df.groupby("Region")[["Sales", "Profit"]].sum().sort_values("Sales", ascending=False))
print("\nLowest-profit products:\n", df.groupby("Product_Name")[["Sales", "Profit"]].sum().sort_values("Profit").head(10))

# 5. Monthly sales trend
monthly = df.set_index("Order_Date").resample("MS")["Sales"].sum()
monthly.plot(marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("monthly_sales_trend.png", dpi=150)
plt.show()





