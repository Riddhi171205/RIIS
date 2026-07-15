import pandas as pd

# ==========================================
# LOAD DATA
# ==========================================

inventory = pd.read_csv("data/raw/inventory.csv")
products = pd.read_csv("data/raw/products.csv")
suppliers = pd.read_csv("data/raw/suppliers.csv")

# ==========================================
# LATEST INVENTORY
# ==========================================

latest_date = inventory["date"].max()

inventory = inventory[
    inventory["date"] == latest_date
]

# ==========================================
# MERGE DATA
# ==========================================

inventory = inventory.merge(
    products[
        [
            "product_id",
            "product_name",
            "category",
            "reorder_level",
            "supplier_id"
        ]
    ],
    on="product_id",
    how="left"
)

inventory = inventory.merge(
    suppliers[
        [
            "supplier_id",
            "supplier_name",
            "lead_time_days"
        ]
    ],
    on="supplier_id",
    how="left"
)

recommendations = []

# ==========================================
# REORDER LOGIC
# ==========================================

for _, row in inventory.iterrows():

    stock = row["closing_stock"]
    reorder = row["reorder_level"]

    if stock < reorder:

        shortage = reorder - stock

        recommendations.append({

            "date": latest_date,

            "store_id": row["store_id"],

            "product_id": row["product_id"],

            "product_name": row["product_name"],

            "supplier_name": row["supplier_name"],

            "current_stock": stock,

            "reorder_level": reorder,

            "recommended_order_qty": shortage + 100,

            "lead_time_days": row["lead_time_days"],

            "priority": "High" if shortage > 50 else "Medium",

            "reason": "Current stock below reorder level"

        })

# ==========================================
# SAVE OUTPUT
# ==========================================

output = pd.DataFrame(recommendations)

output.to_csv(
    "data/processed/reorder_recommendation.csv",
    index=False
)

print("="*50)
print("REORDER ENGINE COMPLETE")
print("="*50)
print("Recommendations :", len(output))
print("="*50)
print(output.head(10))