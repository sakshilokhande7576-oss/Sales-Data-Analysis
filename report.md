# Sales Data Analysis and Visualization

**Personal Project — Python (Pandas, NumPy, Matplotlib, Seaborn)**

## Overview
This project analyzes two years (2023–2024) of retail sales transactions to
uncover revenue trends, top-performing products, and seasonal buying
patterns — then translates those findings into visual reports for
non-technical stakeholders.

Dataset: 11,699 raw transactions across 17 products, 4 categories, 5 regions,
and 2 sales channels (Online / In-Store).

## 1. Data Cleaning & Transformation
Using Pandas and NumPy, the raw dataset was cleaned and standardized:

- Standardized inconsistent text casing in the `region` field
- Removed exact duplicate transactions
- Dropped invalid records (negative/zero quantities from entry errors)
- Imputed 10 missing `unit_price` values using each product's median price
- Recomputed `revenue` with vectorized NumPy operations after cleaning
- Engineered time-based features (month, quarter, weekday, weekend flag)
  to support trend and seasonality analysis

**Result:** 11,689 clean, analysis-ready transactions.

## 2. Key Metrics
| Metric | Value |
|---|---|
| Total Revenue | $1,060,587.65 |
| Total Transactions | 11,689 |
| Average Order Value | $90.73 |

## 3. Revenue Trend
![Monthly Revenue Trend](charts/01_monthly_revenue_trend.png)

Revenue is cyclical rather than steadily growing: it dips through the
summer months, then ramps sharply into a **November–December peak** driven
by holiday shopping — a pattern that repeats consistently in both 2023 and
2024.

## 4. Top-Performing Products
![Top 10 Products](charts/02_top_products.png)

The **Standing Desk** is the single largest revenue driver ($261.7K),
followed by **Noise-Cancel Headphones** and the **Office Chair**. Higher-priced
Furniture and Electronics items dominate the top of the list even though
Stationery and Fitness items sell in higher unit volumes — a sign that
average selling price, not just order count, is what drives revenue here.

## 5. Seasonal Sales Patterns
![Seasonal Pattern](charts/03_seasonal_pattern.png)
![Category x Month Heatmap](charts/05_category_month_heatmap.png)

Three distinct seasonal signals emerged:
- **Nov–Dec:** Broad revenue spike across all categories (holiday shopping),
  led by Electronics and Furniture gifting.
- **January:** A clear bump in **Fitness** category sales — consistent with
  New Year's resolution buying.
- **Aug–Sep:** A smaller lift in **Stationery**, aligned with back-to-school
  timing.
- **Jun–Jul:** The quietest months across nearly every category.

## 6. Category, Region & Channel Breakdown
![Category Share](charts/04_category_share.png)
![Region & Channel](charts/06_region_channel.png)

- **Furniture (49%)** and **Electronics (28%)** together make up roughly
  three-quarters of total revenue, despite Stationery and Fitness having
  more frequent, lower-value transactions.
- **South** is the top-performing region ($245.6K), though all five regions
  are fairly close, indicating balanced geographic demand.
- **Online** sales ($663.9K) outpace **In-Store** ($396.6K) by a wide
  margin across every region.

## 7. Business Opportunities / Recommendations
- **Stock up ahead of Nov–Dec** for Furniture and Electronics; these
  categories see the largest holiday lift and the biggest risk of
  stockouts.
- **Run a January fitness promotion** to capture the resolution-driven
  demand spike already visible in the data.
- **Double down on the Online channel**, which already drives ~63% of
  revenue — investigate why In-Store lags and whether it's worth the
  fixed overhead in lower-performing regions like Central.
- **Bundle high-AOV items** (Standing Desk, Office Chair) with lower-cost
  accessories (Desk Lamp, USB-C Hub) to lift average order value further.

---
*Files: `data/sales_data_clean.csv` (analysis-ready dataset),
`scripts/` (generation, cleaning, and visualization code),
`charts/` (all figures above).*
