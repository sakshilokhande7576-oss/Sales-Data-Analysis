"""
Sales Data Analysis
-------------------
Cleans and analyzes retail sales data using Pandas and NumPy.

Project structure:
sales-data-analysis/
│
├── data/
│   └── sales_data_raw.csv
│
├── scripts/
│   └── analyze.py
│
└── charts/
"""

from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

# Project root = sales-data-analysis
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

RAW_PATH = DATA_DIR / "sales_data_raw.csv"
CLEAN_PATH = DATA_DIR / "sales_data_clean.csv"


# ============================================================
# 2. CHECK INPUT FILE
# ============================================================

if not RAW_PATH.exists():
    print("\nERROR: Raw dataset was not found.")
    print(f"Expected file:\n{RAW_PATH}")
    print("\nPlease make sure sales_data_raw.csv is inside the data folder.")
    raise FileNotFoundError(RAW_PATH)


# ============================================================
# 3. LOAD DATA
# ============================================================

print("=" * 60)
print("SALES DATA ANALYSIS")
print("=" * 60)

print("\nLoading dataset...")

df = pd.read_csv(RAW_PATH, parse_dates=["date"])

print("\n=== RAW DATA OVERVIEW ===")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"Column names: {list(df.columns)}")

print("\nMissing values:")
print(df.isna().sum())


# ============================================================
# 4. DATA CLEANING
# ============================================================

print("\n" + "=" * 60)
print("DATA CLEANING")
print("=" * 60)

before = len(df)


# ------------------------------------------------------------
# 4.1 Standardize region names
# ------------------------------------------------------------

if "region" in df.columns:
    df["region"] = (
        df["region"]
        .astype(str)
        .str.strip()
        .str.title()
    )


# ------------------------------------------------------------
# 4.2 Remove duplicate transactions
# ------------------------------------------------------------

duplicate_columns = [
    "order_id",
    "product",
    "date",
    "quantity",
    "unit_price"
]

available_duplicate_columns = [
    col for col in duplicate_columns
    if col in df.columns
]

df = df.drop_duplicates(
    subset=available_duplicate_columns
)


# ------------------------------------------------------------
# 4.3 Remove invalid quantities
# ------------------------------------------------------------

if "quantity" in df.columns:
    df = df[df["quantity"] > 0]


# ------------------------------------------------------------
# 4.4 Fill missing unit prices
# ------------------------------------------------------------

if "unit_price" in df.columns and "product" in df.columns:

    df["unit_price"] = (
        df.groupby("product")["unit_price"]
        .transform(
            lambda x: x.fillna(x.median())
        )
    )


# ------------------------------------------------------------
# 4.5 Calculate revenue
# ------------------------------------------------------------

if "quantity" in df.columns and "unit_price" in df.columns:

    df["revenue"] = np.round(
        df["quantity"].to_numpy()
        * df["unit_price"].to_numpy(),
        2
    )


# ============================================================
# 5. TIME FEATURES
# ============================================================

if "date" in df.columns:

    df["year"] = df["date"].dt.year

    df["month"] = df["date"].dt.month

    df["month_name"] = df["date"].dt.strftime("%b")

    df["quarter"] = df["date"].dt.quarter

    df["weekday"] = df["date"].dt.day_name()

    df["is_weekend"] = (
        df["date"].dt.weekday >= 5
    )


# ============================================================
# 6. CLEANING SUMMARY
# ============================================================

after = len(df)

print("\n=== CLEANING SUMMARY ===")

print(f"Rows before cleaning : {before:,}")
print(f"Rows after cleaning  : {after:,}")
print(f"Rows removed         : {before - after:,}")

if "unit_price" in df.columns:
    print(
        "Missing unit_price remaining:",
        df["unit_price"].isna().sum()
    )


# ============================================================
# 7. SAVE CLEAN DATA
# ============================================================

df.to_csv(
    CLEAN_PATH,
    index=False
)

print("\nClean dataset saved successfully:")
print(CLEAN_PATH)


# ============================================================
# 8. KEY BUSINESS METRICS
# ============================================================

print("\n" + "=" * 60)
print("KEY BUSINESS METRICS")
print("=" * 60)

total_revenue = df["revenue"].sum()


if "order_id" in df.columns:

    total_orders = df["order_id"].nunique()

    order_revenue = (
        df.groupby("order_id")["revenue"]
        .sum()
    )

    average_order_value = order_revenue.mean()

else:

    total_orders = len(df)

    average_order_value = (
        df["revenue"].mean()
    )


print(
    f"Total Revenue       : ${total_revenue:,.2f}"
)

print(
    f"Total Orders        : {total_orders:,}"
)

print(
    f"Average Order Value : ${average_order_value:,.2f}"
)


# ============================================================
# 9. TOP PRODUCTS
# ============================================================

print("\n" + "=" * 60)
print("TOP 10 PRODUCTS BY REVENUE")
print("=" * 60)

if "product" in df.columns:

    top_products = (
        df.groupby("product")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    print(top_products.round(2))


# ============================================================
# 10. CATEGORY ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("REVENUE BY CATEGORY")
print("=" * 60)

if "category" in df.columns:

    category_revenue = (
        df.groupby("category")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    print(category_revenue.round(2))

    print("\nCategory revenue percentage:")

    category_percentage = (
        category_revenue
        / total_revenue
        * 100
    )

    print(category_percentage.round(2))


# ============================================================
# 11. MONTHLY REVENUE TREND
# ============================================================

print("\n" + "=" * 60)
print("MONTHLY REVENUE TREND")
print("=" * 60)

monthly_revenue = (
    df.groupby(
        pd.Grouper(
            key="date",
            freq="MS"
        )
    )["revenue"]
    .sum()
)

print(
    monthly_revenue.round(2)
)


# ============================================================
# 12. CALENDAR MONTH ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("REVENUE BY CALENDAR MONTH")
print("=" * 60)

month_order = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec"
]

monthly_calendar = (
    df.groupby("month_name")["revenue"]
    .sum()
    .reindex(month_order)
)

print(
    monthly_calendar.round(2)
)


# ============================================================
# 13. WEEKDAY ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("AVERAGE REVENUE BY WEEKDAY")
print("=" * 60)

weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

weekday_revenue = (
    df.groupby("weekday")["revenue"]
    .mean()
    .reindex(weekday_order)
)

print(
    weekday_revenue.round(2)
)


# ============================================================
# 14. REGION ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("REVENUE BY REGION")
print("=" * 60)

if "region" in df.columns:

    region_revenue = (
        df.groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    print(
        region_revenue.round(2)
    )


# ============================================================
# 15. SALES CHANNEL ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("REVENUE BY SALES CHANNEL")
print("=" * 60)

if "channel" in df.columns:

    channel_revenue = (
        df.groupby("channel")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    print(
        channel_revenue.round(2)
    )

    print("\nChannel percentage:")

    channel_percentage = (
        channel_revenue
        / total_revenue
        * 100
    )

    print(
        channel_percentage.round(2)
    )


# ============================================================
# 16. YEAR-WISE REVENUE
# ============================================================

print("\n" + "=" * 60)
print("YEAR-WISE REVENUE")
print("=" * 60)

if "year" in df.columns:

    yearly_revenue = (
        df.groupby("year")["revenue"]
        .sum()
    )

    print(
        yearly_revenue.round(2)
    )


# ============================================================
# 17. QUARTER-WISE REVENUE
# ============================================================

print("\n" + "=" * 60)
print("QUARTER-WISE REVENUE")
print("=" * 60)

if "quarter" in df.columns:

    quarterly_revenue = (
        df.groupby("quarter")["revenue"]
        .sum()
    )

    print(
        quarterly_revenue.round(2)
    )


# ============================================================
# 18. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)

print(f"\nTotal Revenue: ${total_revenue:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(
    f"Average Order Value: ${average_order_value:,.2f}"
)

print("\nClean dataset:")
print(CLEAN_PATH)

print("\nProject completed successfully!")