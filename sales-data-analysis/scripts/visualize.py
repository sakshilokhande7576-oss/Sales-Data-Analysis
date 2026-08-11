"""
visualize.py
Builds visual reports/charts for the Sales Data Analysis project.
Designed to communicate findings clearly to non-technical stakeholders.
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CLEAN_PATH = PROJECT_ROOT / "data" / "sales_data_clean.csv"
OUT = PROJECT_ROOT / "charts"

# Create charts folder if it does not exist
OUT.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. CHECK DATASET
# ============================================================

if not CLEAN_PATH.exists():
    print("ERROR: Clean dataset not found.")
    print(f"Expected file: {CLEAN_PATH}")
    raise FileNotFoundError(CLEAN_PATH)


# ============================================================
# 3. LOAD DATA
# ============================================================

print("=" * 60)
print("SALES DATA VISUALIZATION")
print("=" * 60)

print("\nLoading cleaned dataset...")

df = pd.read_csv(
    CLEAN_PATH,
    parse_dates=["date"]
)

print(f"Rows loaded: {len(df):,}")


# ============================================================
# 4. VISUALIZATION SETTINGS
# ============================================================

sns.set_theme(
    style="whitegrid",
    font_scale=1.05
)

PALETTE = "viridis"

month_order = [
    "Jan", "Feb", "Mar", "Apr",
    "May", "Jun", "Jul", "Aug",
    "Sep", "Oct", "Nov", "Dec"
]

df["month_name"] = pd.Categorical(
    df["month_name"],
    categories=month_order,
    ordered=True
)


# ============================================================
# HELPER FUNCTION
# ============================================================

def money(ax, axis="y"):
    """Format an axis as currency."""

    formatter = mtick.FuncFormatter(
        lambda x, _: f"${x:,.0f}"
    )

    if axis == "y":
        ax.yaxis.set_major_formatter(formatter)
    else:
        ax.xaxis.set_major_formatter(formatter)


def save_chart(fig, filename):
    """Save chart to the charts folder."""

    output_path = OUT / filename

    fig.tight_layout()

    fig.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close(fig)

    print(f"Created: {output_path}")


# ============================================================
# 1. MONTHLY REVENUE TREND
# ============================================================

monthly = (
    df.groupby(
        pd.Grouper(
            key="date",
            freq="MS"
        )
    )["revenue"]
    .sum()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(11, 5))

ax.plot(
    monthly["date"],
    monthly["revenue"],
    marker="o",
    linewidth=2
)

ax.fill_between(
    monthly["date"],
    monthly["revenue"],
    alpha=0.08
)

ax.set_title(
    "Monthly Revenue Trend (2023–2024)",
    fontsize=15,
    fontweight="bold"
)

ax.set_xlabel("")
ax.set_ylabel("Revenue")

money(ax)

fig.autofmt_xdate()

save_chart(
    fig,
    "01_monthly_revenue_trend.png"
)


# ============================================================
# 2. TOP 10 PRODUCTS BY REVENUE
# ============================================================

top_products = (
    df.groupby("product")["revenue"]
    .sum()
    .sort_values(ascending=True)
    .tail(10)
)

fig, ax = plt.subplots(figsize=(9, 6))

colors = sns.color_palette(
    PALETTE,
    len(top_products)
)

ax.barh(
    top_products.index,
    top_products.values,
    color=colors
)

ax.set_title(
    "Top 10 Products by Revenue",
    fontsize=15,
    fontweight="bold"
)

ax.set_xlabel("Revenue")
ax.set_ylabel("Product")

money(
    ax,
    axis="x"
)

for i, value in enumerate(top_products.values):

    ax.text(
        value,
        i,
        f"  ${value:,.0f}",
        va="center",
        fontsize=9
    )

save_chart(
    fig,
    "02_top_products.png"
)


# ============================================================
# 3. SEASONAL PATTERN
# ============================================================

by_month = (
    df.groupby(
        "month_name",
        observed=True
    )["revenue"]
    .sum()
)

fig, ax = plt.subplots(figsize=(10, 5))

colors = [
    "#C0504D"
    if month in ("Nov", "Dec", "Jan")
    else "#4472C4"
    for month in by_month.index
]

ax.bar(
    by_month.index,
    by_month.values,
    color=colors
)

ax.set_title(
    "Seasonal Sales Pattern — Revenue by Month",
    fontsize=14,
    fontweight="bold"
)

ax.set_ylabel("Revenue")

money(ax)

save_chart(
    fig,
    "03_seasonal_pattern.png"
)


# ============================================================
# 4. REVENUE BY CATEGORY
# ============================================================

by_category = (
    df.groupby("category")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(7, 7))

colors = sns.color_palette(
    PALETTE,
    len(by_category)
)

wedges, texts, autotexts = ax.pie(
    by_category.values,
    labels=by_category.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors,
    pctdistance=0.8,
    wedgeprops=dict(
        width=0.4,
        edgecolor="white"
    )
)

ax.set_title(
    "Revenue Share by Category",
    fontsize=15,
    fontweight="bold"
)

save_chart(
    fig,
    "04_category_share.png"
)


# ============================================================
# 5. CATEGORY-MONTH HEATMAP
# ============================================================

pivot = (
    df.pivot_table(
        index="category",
        columns="month_name",
        values="revenue",
        aggfunc="sum",
        observed=True
    )
    .reindex(columns=month_order)
)

fig, ax = plt.subplots(
    figsize=(12, 4.5)
)

sns.heatmap(
    pivot,
    cmap="YlGnBu",
    annot=False,
    cbar_kws={
        "label": "Revenue"
    },
    ax=ax
)

ax.set_title(
    "Revenue by Category and Month",
    fontsize=15,
    fontweight="bold"
)

ax.set_xlabel("")
ax.set_ylabel("")

save_chart(
    fig,
    "05_category_month_heatmap.png"
)


# ============================================================
# 6. REGION AND CHANNEL
# ============================================================

region_channel = (
    df.groupby(
        ["region", "channel"]
    )["revenue"]
    .sum()
    .unstack()
)

fig, ax = plt.subplots(
    figsize=(10, 5.5)
)

region_channel.plot(
    kind="bar",
    ax=ax,
    color=["#4472C4", "#ED7D31"]
)

ax.set_title(
    "Revenue by Region and Sales Channel",
    fontsize=15,
    fontweight="bold"
)

ax.set_xlabel("")
ax.set_ylabel("Revenue")

money(ax)

plt.xticks(
    rotation=0
)

ax.legend(
    title="Channel"
)

save_chart(
    fig,
    "06_region_channel.png"
)


# ============================================================
# 7. REVENUE BY REGION
# ============================================================

region_revenue = (
    df.groupby("region")["revenue"]
    .sum()
    .sort_values(ascending=True)
)

fig, ax = plt.subplots(
    figsize=(9, 5)
)

ax.barh(
    region_revenue.index,
    region_revenue.values
)

ax.set_title(
    "Revenue by Region",
    fontsize=15,
    fontweight="bold"
)

ax.set_xlabel("Revenue")
ax.set_ylabel("Region")

money(
    ax,
    axis="x"
)

save_chart(
    fig,
    "07_revenue_by_region.png"
)


# ============================================================
# 8. ONLINE VS IN-STORE
# ============================================================

channel_revenue = (
    df.groupby("channel")["revenue"]
    .sum()
)

fig, ax = plt.subplots(
    figsize=(7, 7)
)

ax.pie(
    channel_revenue.values,
    labels=channel_revenue.index,
    autopct="%1.1f%%",
    startangle=90
)

ax.set_title(
    "Revenue by Sales Channel",
    fontsize=15,
    fontweight="bold"
)

save_chart(
    fig,
    "08_revenue_by_channel.png"
)


# ============================================================
# 9. YEAR-WISE REVENUE
# ============================================================

year_revenue = (
    df.groupby("year")["revenue"]
    .sum()
)

fig, ax = plt.subplots(
    figsize=(7, 5)
)

ax.bar(
    year_revenue.index.astype(str),
    year_revenue.values
)

ax.set_title(
    "Revenue Comparison: 2023 vs 2024",
    fontsize=15,
    fontweight="bold"
)

ax.set_xlabel("Year")
ax.set_ylabel("Revenue")

money(ax)

save_chart(
    fig,
    "09_year_wise_revenue.png"
)


# ============================================================
# 10. QUARTER-WISE REVENUE
# ============================================================

quarter_revenue = (
    df.groupby("quarter")["revenue"]
    .sum()
)

fig, ax = plt.subplots(
    figsize=(8, 5)
)

ax.bar(
    quarter_revenue.index.astype(str),
    quarter_revenue.values
)

ax.set_title(
    "Revenue by Quarter",
    fontsize=15,
    fontweight="bold"
)

ax.set_xlabel("Quarter")
ax.set_ylabel("Revenue")

money(ax)

save_chart(
    fig,
    "10_quarter_wise_revenue.png"
)


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("VISUALIZATION COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nAll charts saved to:")
print(OUT)