import pandas as pd

# Load Data
inventory = pd.read_csv("data/raw/inventory.csv")
issues = pd.read_csv("data/processed/inventory_imbalance.csv")

# Latest inventory snapshot
latest_date = inventory["date"].max()
inventory = inventory[inventory["date"] == latest_date]

recommendations = []

products = issues["product_id"].unique()

for product in products:

    product_inventory = inventory[inventory["product_id"] == product]

    overstock = product_inventory[
        product_inventory["closing_stock"] > 300
    ]

    understock = issues[
        (issues["product_id"] == product) &
        (issues["issue_type"] == "Understock")
    ]

    if overstock.empty or understock.empty:
        continue

    for _, receiver in understock.iterrows():

        shortage = receiver["reorder_level"] - receiver["closing_stock"]

        for _, sender in overstock.iterrows():

            excess = sender["closing_stock"] - 300

            if excess <= 0:
                continue

            transfer_qty = min(excess, shortage)

            if transfer_qty <= 0:
                continue

            recommendations.append({

                "date": latest_date,

                "product_id": product,

                "from_store": int(sender["store_id"]),

                "to_store": int(receiver["store_id"]),

                "available_excess": excess,

                "required_quantity": shortage,

                "transfer_quantity": transfer_qty,

                "priority": receiver["severity"],

                "reason": "Transfer excess inventory to avoid stockout"

            })

            shortage -= transfer_qty

            if shortage <= 0:
                break

recommendations_df = pd.DataFrame(recommendations)

recommendations_df.to_csv(
    "data/processed/transfer_recommendation.csv",
    index=False
)

print("=" * 50)
print("TRANSFER RECOMMENDATION ENGINE COMPLETE")
print("=" * 50)
print("Recommendations Generated :", len(recommendations_df))
print("=" * 50)
print(recommendations_df.head(10))