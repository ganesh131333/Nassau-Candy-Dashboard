import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# =========================
# 1. Load Dataset
# =========================

df = pd.read_csv("Nassau Candy Distributor (1).csv")

print("="*50)
print("DATASET LOADED SUCCESSFULLY")
print("="*50)

# =========================
# 2. Basic Information
# =========================

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)

print("\nData Types:")
print(df.info())

# =========================
# 3. Clean Column Names
# =========================

df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace(" ", "_")

print("\nUpdated Columns:")
print(df.columns)

# =========================
# 4. Check Missing Values
# =========================

print("\nMissing Values:")
print(df.isnull().sum())

# Fill numeric missing values
numeric_cols = df.select_dtypes(include=np.number).columns

for col in numeric_cols:
    df[col].fillna(df[col].median(), inplace=True)

# Fill text missing values
text_cols = df.select_dtypes(include="object").columns

for col in text_cols:
    df[col].fillna("Unknown", inplace=True)

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

# =========================
# 5. Remove Duplicate Records
# =========================

print("\nDuplicate Records:")
print(df.duplicated().sum())

df.drop_duplicates(inplace=True)

print("Duplicates After Removal:")
print(df.duplicated().sum())

# =========================
# 6. Convert Date Columns
# =========================

print("\nAvailable Columns:")
print(df.columns.tolist())

# Convert date columns
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce",
    dayfirst=False
)

df["Ship_Date"] = pd.to_datetime(
    df["Ship_Date"],
    errors="coerce",
    dayfirst=False
)

print("\nDate Conversion Successful!")
print(df[["Order_Date", "Ship_Date"]].head())

print("\nData Types:")
print(df[["Order_Date", "Ship_Date"]].dtypes)


# =========================
# 7. Create Delivery Days
# =========================

df["Delivery_Days"] = (
    df["Ship_Date"] - df["Order_Date"]
).dt.days

print("\nDelivery Days Summary:")
print(df["Delivery_Days"].describe())


# =========================
# 8. Remove Invalid Delivery Days
# =========================

negative_days = df[df["Delivery_Days"] < 0]

print("\nNegative Delivery Records:", len(negative_days))

# Remove invalid records
df = df[df["Delivery_Days"] >= 0]

# =========================
# 9. Check Sales Statistics
# =========================

if "Sales" in df.columns:
    print("\nSales Statistics:")
    print(df["Sales"].describe())

# =========================
# 10. Check Profit Statistics
# =========================

if "Gross_Profit" in df.columns:
    print("\nProfit Statistics:")
    print(df["Gross_Profit"].describe())

# =========================
# 11. Standardize Text Columns
# =========================

for col in text_cols:
    df[col] = df[col].astype(str).str.strip()

# =========================
# 12. Region Cleaning
# =========================

if "Region" in df.columns:
    df["Region"] = df["Region"].str.title()

# =========================
# 13. State Cleaning
# =========================

if "State_Province" in df.columns:
    df["State_Province"] = (
        df["State_Province"]
        .astype(str)
        .str.strip()
        .str.title()
    )
# =========================
# 14. Final Validation
# =========================

print("\nFinal Shape:")
print(df.shape)

print("\nFinal Missing Values:")
print(df.isnull().sum())

print("\nFinal Data Types:")
print(df.dtypes)

# =========================
# 15. Save Clean Dataset
# =========================

df.to_csv(
    "Nassau_Candy_Cleaned.csv",
    index=False
)

print("\nCleaned Dataset Saved Successfully!")
print("File Name: Nassau_Candy_Cleaned.csv")

print(df[["Order_Date", "Ship_Date", "Delivery_Days"]].head(10))

print("\nMinimum Delivery Days:", df["Delivery_Days"].min())
print("Maximum Delivery Days:", df["Delivery_Days"].max())
print("Average Delivery Days:", df["Delivery_Days"].mean())


# =========================
# Convert dates again before Feature Engineering
# =========================

df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
df["Ship_Date"] = pd.to_datetime(df["Ship_Date"], errors="coerce")

# =========================
# Convert dates again before Feature Engineering
# =========================

df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
df["Ship_Date"] = pd.to_datetime(df["Ship_Date"], errors="coerce")

print(df[["Order_Date", "Ship_Date"]].dtypes)


# =========================
# 16. Feature Engineering
# =========================

print("\nFEATURE ENGINEERING")

df["Order_Year"] = df["Order_Date"].dt.year
df["Order_Month_No"] = df["Order_Date"].dt.month
df["Order_Month"] = df["Order_Date"].dt.month_name()
df["Quarter"] = df["Order_Date"].dt.quarter
df["Day_Name"] = df["Order_Date"].dt.day_name()

df["Profit_Margin"] = (df["Gross_Profit"] / df["Sales"]) * 100

print(df[[
    "Order_Date",
    "Order_Year",
    "Order_Month",
    "Quarter",
    "Day_Name",
    "Profit_Margin"
]].head())

# =========================
# BUSINESS SUMMARY
# =========================

print("=" * 50)
print("BUSINESS SUMMARY")
print("=" * 50)

print("Total Orders       :", df["Order_ID"].nunique())
print("Total Customers    :", df["Customer_ID"].nunique())
print("Total Sales        : $", round(df["Sales"].sum(), 2))
print("Total Gross Profit : $", round(df["Gross_Profit"].sum(), 2))
print("Total Units Sold   :", df["Units"].sum())

print("\nAverage Sales      : $", round(df["Sales"].mean(), 2))
print("Average Profit     : $", round(df["Gross_Profit"].mean(), 2))

# =========================
# SALES BY REGION
# =========================

region_analysis = df.groupby("Region").agg({
    "Sales":"sum",
    "Gross_Profit":"sum",
    "Units":"sum"
}).sort_values("Sales", ascending=False)

print(region_analysis)

# =========================
# SHIP MODE ANALYSIS
# =========================

ship_analysis = df.groupby("Ship_Mode").agg({
    "Sales":"sum",
    "Gross_Profit":"sum",
    "Units":"sum",
    "Delivery_Days":"mean"
})

print(ship_analysis)

# =========================
# TOP STATES
# =========================

state_analysis = df.groupby("State/Province").agg({
    "Sales":"sum",
    "Gross_Profit":"sum"
})

print(state_analysis.sort_values("Sales", ascending=False).head(10))

# =========================
# TOP PRODUCTS
# =========================

product_analysis = df.groupby("Product_Name").agg({
    "Sales":"sum",
    "Gross_Profit":"sum",
    "Units":"sum"
})

print(product_analysis.sort_values("Sales", ascending=False).head(10))

# =========================
# MONTHLY SALES
# =========================

monthly_sales = df.groupby("Order_Month")["Sales"].sum()

print(monthly_sales)

# =========================
# TOP CUSTOMERS
# =========================

customer_analysis = df.groupby("Customer_ID").agg({
    "Sales":"sum",
    "Gross_Profit":"sum"
})

print(customer_analysis.sort_values("Sales", ascending=False).head(10))
print("\nAverage Profit Margin (%)")
print(round(df["Profit_Margin"].mean(),2))



region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)

plt.figure(figsize=(8,5))
region_sales.plot(kind="bar")

plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales ($)")
plt.xticks(rotation=0)

plt.show()

profit_region = df.groupby("Region")["Gross_Profit"].sum().sort_values(ascending=False)

plt.figure(figsize=(8,5))
profit_region.plot(kind="bar")

plt.title("Gross Profit by Region")
plt.xlabel("Region")
plt.ylabel("Gross Profit ($)")
plt.xticks(rotation=0)

plt.show()

ship_mode = df["Ship_Mode"].value_counts()

plt.figure(figsize=(7,7))

plt.pie(
    ship_mode,
    labels=ship_mode.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Ship Mode Distribution")

plt.show()

monthly_sales = df.groupby("Order_Month")["Sales"].sum()

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

monthly_sales = monthly_sales.reindex(month_order)

plt.figure(figsize=(10,5))

plt.plot(monthly_sales.index, monthly_sales.values, marker="o")

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales ($)")
plt.xticks(rotation=45)

plt.grid(True)

plt.show()
top_products = (
    df.groupby("Product_Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,6))

top_products.sort_values().plot(kind="barh")

plt.title("Top 10 Products by Sales")
plt.xlabel("Sales ($)")
plt.ylabel("Product")

plt.show()

top_states = (
    df.groupby("State/Province")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,6))

top_states.sort_values().plot(kind="barh")

plt.title("Top 10 States by Sales")
plt.xlabel("Sales ($)")
plt.ylabel("State")

plt.show()

plt.figure(figsize=(8,6))

plt.scatter(
    df["Sales"],
    df["Gross_Profit"]
)

plt.title("Sales vs Gross Profit")
plt.xlabel("Sales")
plt.ylabel("Gross Profit")

plt.show()