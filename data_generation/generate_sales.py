import pandas as pd
import random
from datetime import datetime, timedelta

# -----------------------------
# Load Data
# -----------------------------
stores = pd.read_csv("data/raw/stores.csv")
products = pd.read_csv("data/raw/products.csv")

# -----------------------------
# Configuration
# -----------------------------
START_DATE = datetime(2025, 1, 1)
NUM_DAYS = 365

sales = []
sale_id = 1

# -----------------------------
# Generate Sales
# -----------------------------
for day in range(NUM_DAYS):

    current_date = START_DATE + timedelta(days=day)

    for _, store in stores.iterrows():

        # Randomly choose 250–350 products sold today
        num_products_today = random.randint(
            min(50, len(products)),
            min(75, len(products))
        )

        daily_products = products.sample(n=num_products_today)

        for _, product in daily_products.iterrows():

            # Base quantity
            qty = random.randint(1, 15)

            # Weekend boost
            if current_date.weekday() in [5, 6]:
                qty = int(qty * 1.2)

            unit_price = float(product["selling_price"])

            sales.append({
                "sale_id": sale_id,
                "date": current_date.strftime("%Y-%m-%d"),
                "store_id": int(store["store_id"]),
                "product_id": product["product_id"],
                "quantity_sold": qty,
                "unit_price": unit_price,
                "total_revenue": round(qty * unit_price, 2)
            })

            sale_id += 1

# -----------------------------
# Save CSV
# -----------------------------
sales_df = pd.DataFrame(sales)

sales_df.to_csv(
    "data/raw/sales.csv",
    index=False
)

# -----------------------------
# Summary
# -----------------------------
print("=" * 40)
print("SALES GENERATION COMPLETE")
print("=" * 40)
print(f"Stores Loaded      : {len(stores)}")
print(f"Products Loaded    : {len(products)}")
print(f"Days Simulated     : {NUM_DAYS}")
print(f"Rows Generated     : {len(sales_df):,}")
print("=" * 40)