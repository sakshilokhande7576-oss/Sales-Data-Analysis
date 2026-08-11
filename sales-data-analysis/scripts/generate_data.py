"""
generate_data.py
Generates a realistic synthetic retail sales dataset for the
Sales Data Analysis and Visualization project.
"""
import numpy as np
import pandas as pd

np.random.seed(42)

# --- Reference data -----------------------------------------------------
products = {
    "Wireless Mouse":        ("Electronics", 18.99),
    "Mechanical Keyboard":   ("Electronics", 64.99),
    "USB-C Hub":             ("Electronics", 29.99),
    "Bluetooth Speaker":     ("Electronics", 45.50),
    "Noise-Cancel Headphones": ("Electronics", 129.99),
    "Yoga Mat":              ("Fitness", 22.00),
    "Dumbbell Set":          ("Fitness", 89.99),
    "Resistance Bands":      ("Fitness", 14.50),
    "Running Shoes":         ("Fitness", 74.99),
    "Water Bottle":          ("Fitness", 12.99),
    "Office Chair":          ("Furniture", 149.99),
    "Standing Desk":         ("Furniture", 299.99),
    "Desk Lamp":             ("Furniture", 24.99),
    "Bookshelf":             ("Furniture", 119.99),
    "Notebook Set":          ("Stationery", 8.99),
    "Fountain Pen":          ("Stationery", 19.99),
    "Planner":               ("Stationery", 15.99),
}
regions = ["North", "South", "East", "West", "Central"]
channels = ["Online", "In-Store"]

# Seasonal multiplier per month (index 0=Jan ... 11=Dec)
# Holiday bump in Nov/Dec, summer dip, fitness spike in Jan
seasonal_factor = [1.25, 1.05, 0.95, 0.9, 0.9, 0.85,
                    0.8, 0.85, 0.95, 1.0, 1.35, 1.55]

category_seasonal_boost = {
    "Fitness": {0: 1.4, 1: 1.15},          # New Year's resolutions
    "Electronics": {10: 1.3, 11: 1.6},     # Black Friday / Christmas
    "Furniture": {},
    "Stationery": {7: 1.3, 8: 1.15},       # Back to school
}

# --- Generate transactions ----------------------------------------------
dates = pd.date_range("2023-01-01", "2024-12-31", freq="D")
rows = []
order_id = 100000

for date in dates:
    month_idx = date.month - 1
    base_factor = seasonal_factor[month_idx]
    weekday_boost = 1.2 if date.weekday() >= 5 else 1.0  # weekend bump

    n_orders = np.random.poisson(lam=14 * base_factor * weekday_boost)

    for _ in range(n_orders):
        product = np.random.choice(list(products.keys()))
        category, base_price = products[product]

        cat_boost = category_seasonal_boost.get(category, {}).get(month_idx, 1.0)
        qty = np.random.choice([1, 1, 1, 2, 2, 3, 4], p=[0.35,0.2,0.15,0.15,0.08,0.05,0.02])

        # small price noise/discounts
        price_noise = np.random.normal(1.0, 0.03)
        discount = np.random.choice([0, 0, 0, 0.1, 0.15, 0.2], p=[0.55,0.15,0.1,0.1,0.06,0.04])
        unit_price = round(base_price * price_noise * (1 - discount), 2)

        order_id += 1
        rows.append({
            "order_id": order_id,
            "date": date,
            "product": product,
            "category": category,
            "region": np.random.choice(regions, p=[0.22,0.22,0.2,0.2,0.16]),
            "channel": np.random.choice(channels, p=[0.62, 0.38]),
            "quantity": qty,
            "unit_price": unit_price,
            "discount_pct": discount,
        })

        # apply category seasonal boost as extra duplicate orders (simulate demand spike)
        if cat_boost > 1.0 and np.random.random() < (cat_boost - 1.0):
            order_id += 1
            rows.append({
                "order_id": order_id,
                "date": date,
                "product": product,
                "category": category,
                "region": np.random.choice(regions),
                "channel": np.random.choice(channels, p=[0.62, 0.38]),
                "quantity": np.random.choice([1, 1, 2]),
                "unit_price": unit_price,
                "discount_pct": discount,
            })

df = pd.DataFrame(rows)
df["revenue"] = round(df["quantity"] * df["unit_price"], 2)

# Inject a few messy-data issues on purpose, so the "cleaning" step has real work to do
messy_idx = np.random.choice(df.index, size=40, replace=False)
df.loc[messy_idx[:10], "region"] = df.loc[messy_idx[:10], "region"].str.lower()
df.loc[messy_idx[10:20], "unit_price"] = np.nan
df.loc[messy_idx[20:25], "quantity"] = -1
dup_rows = df.loc[messy_idx[25:30]]
df = pd.concat([df, dup_rows], ignore_index=True)

df = df.sort_values("date").reset_index(drop=True)
df.to_csv("/home/claude/sales_project/data/sales_data_raw.csv", index=False)
print(f"Generated {len(df)} raw transaction rows.")
print(df.head())
