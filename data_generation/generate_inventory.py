import pandas as pd
import random
from datetime import datetime, timedelta

# Load master data
stores = pd.read_csv("data/raw/stores.csv")
products = pd.read_csv("data/raw/products.csv")

START_DATE = datetime(2025, 1, 1)
NUM_DAYS = 90

records = []
inventory_id = 1

# Maintain running stock for each (store, product)
stock_state = {}

for _, store in stores.iterrows():
    for _, product in products.iterrows():
        stock_state[(store["store_id"], product["product_id"])] = random.randint(150, 400)

for day in range(NUM_DAYS):

    current_date = START_DATE + timedelta(days=day)

    for _, store in stores.iterrows():

        for _, product in products.iterrows():

            key = (store["store_id"], product["product_id"])

            opening_stock = stock_state[key]

            category = str(product["category"]).lower()

            # Category-wise demand
            if "dairy" in category:
                sold = random.randint(20, 50)
            elif "grocery" in category:
                sold = random.randint(8, 20)
            elif "snack" in category:
                sold = random.randint(5, 15)
            else:
                sold = random.randint(1, 8)

            # Weekend boost
            if current_date.weekday() in [5, 6]:
                sold = int(sold * 1.2)

            sold = min(sold, opening_stock)
            closing_stock = opening_stock - sold

            # Reorder logic
            reorder_level = int(product["reorder_level"])
            if closing_stock < reorder_level:
                closing_stock += random.randint(150, 300)

            # Occasionally create dead stock
            if random.random() < 0.02:
                closing_stock += random.randint(200, 500)

            stock_state[key] = closing_stock

            expiry = current_date + timedelta(
                days=int(product["shelf_life_days"])
            )

            records.append({
                "inventory_id": inventory_id,
                "date": current_date.strftime("%Y-%m-%d"),
                "store_id": int(store["store_id"]),
                "product_id": int(product["product_id"]),
                "opening_stock": opening_stock,
                "quantity_sold": sold,
                "closing_stock": closing_stock,
                "expiry_date": expiry.strftime("%Y-%m-%d")
            })

            inventory_id += 1

inventory_df = pd.DataFrame(records)
inventory_df.to_csv("data/raw/inventory.csv", index=False)

print("✅ Inventory V2 generated successfully!")
print("Rows:", len(inventory_df))