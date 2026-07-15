import pandas as pd

# ==========================================
# LOAD DATA
# ==========================================

inventory = pd.read_csv("data/raw/inventory.csv")
products = pd.read_csv("data/raw/products.csv")

# ==========================================
# LATEST INVENTORY
# ==========================================

latest_date = inventory["date"].max()

inventory = inventory[
    inventory["date"] == latest_date
]

# ==========================================
# MERGE PRODUCT DETAILS
# ==========================================

inventory = inventory.merge(
    products[
        [
            "product_id",
            "product_name",
            "category",
            "shelf_life_days"
        ]
    ],
    on="product_id",
    how="left"
)

recommendations = []

# ==========================================
# MARKDOWN LOGIC
# ==========================================

for _, row in inventory.iterrows():

    stock = row["closing_stock"]
    sold = row["quantity_sold"]
    shelf_life = row["shelf_life_days"]

    discount = None
    reason = None
    priority = None

    # High stock + very slow sales
    if stock > 500 and sold < 10:

        discount = "30%"
        priority = "High"
        reason = "Very high stock with slow sales"

    elif stock > 400 and sold < 15:

        discount = "20%"
        priority = "Medium"
        reason = "High stock with low sales"

    elif stock > 300 and sold < 20:

        discount = "10%"
        priority = "Low"
        reason = "Moderate overstock"

    # Near expiry boost
    if shelf_life <= 7 and stock > 100:

        discount = "30%"
        priority = "High"
        reason = "Near expiry with remaining stock"

    if discount:

        recommendations.append({

            "date": latest_date,

            "store_id": row["store_id"],

            "product_id": row["product_id"],

            "product_name": row["product_name"],

            "category": row["category"],

            "closing_stock": stock,

            "quantity_sold": sold,

            "recommended_discount": discount,

            "priority": priority,

            "reason": reason

        })

# ==========================================
# SAVE OUTPUT
# ==========================================

output = pd.DataFrame(recommendations)

output.to_csv(
    "data/processed/markdown_recommendation.csv",
    index=False
)

# ==========================================
# SUMMARY
# ==========================================

print("=" * 50)
print("MARKDOWN OPTIMIZER COMPLETE")
print("=" * 50)
print("Recommendations :", len(output))
print("=" * 50)

print(output.head(10))