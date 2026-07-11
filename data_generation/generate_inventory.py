import pandas as pd
import random
from datetime import datetime, timedelta

# Load data
stores = pd.read_csv("data/raw/stores.csv")
products = pd.read_csv("data/raw/products.csv")

inventory_records = []
inventory_id = 1

START_DATE = datetime(2025, 1, 1)
NUM_DAYS = 90   # Change to 365 later

for day in range(NUM_DAYS):

    current_date = START_DATE + timedelta(days=day)

    for _, store in stores.iterrows():

        for _, product in products.iterrows():

            opening_stock = random.randint(80, 400)

            quantity_sold = random.randint(5, 50)

            closing_stock = max(
                0,
                opening_stock - quantity_sold
            )

            expiry_date = current_date + timedelta(
                days=int(product["shelf_life_days"])
            )

            inventory_records.append({
                "inventory_id": inventory_id,
                "date": current_date.strftime("%Y-%m-%d"),
                "store_id": int(store["store_id"]),
                "product_id": product["product_id"],
                "opening_stock": opening_stock,
                "quantity_sold": quantity_sold,
                "closing_stock": closing_stock,
                "expiry_date": expiry_date.strftime("%Y-%m-%d")
            })

            inventory_id += 1

inventory_df = pd.DataFrame(inventory_records)

inventory_df.to_csv(
    "data/raw/inventory.csv",
    index=False
)

print("=" * 50)
print("INVENTORY GENERATED SUCCESSFULLY")
print("=" * 50)
print("Stores Loaded :", len(stores))
print("Products Loaded :", len(products))
print("Days :", NUM_DAYS)
print("Rows Generated :", len(inventory_df))
print("=" * 50)