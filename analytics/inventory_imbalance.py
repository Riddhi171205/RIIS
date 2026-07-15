import pandas as pd

# ==========================================
# LOAD DATA
# ==========================================

inventory = pd.read_csv("data/raw/inventory.csv")
products = pd.read_csv("data/raw/products.csv")

# ==========================================
# USE LATEST INVENTORY SNAPSHOT
# ==========================================

latest_date = inventory["date"].max()

inventory = inventory[
    inventory["date"] == latest_date
]

# ==========================================
# MERGE PRODUCT INFORMATION
# ==========================================

inventory = inventory.merge(
    products[
        ["product_id", "product_name", "category", "reorder_level"]
    ],
    on="product_id",
    how="left"
)

# ==========================================
# FIND INVENTORY ISSUES
# ==========================================

results = []

for _, row in inventory.iterrows():

    stock = row["closing_stock"]
    reorder_level = row["reorder_level"]

    issue_type = None
    severity = None
    recommendation = None
    reason = None

    # --------------------------------------
    # OVERSTOCK
    # --------------------------------------

    if stock > 300:

        issue_type = "Overstock"

        if stock <= 400:
            severity = "Low"
        elif stock <= 500:
            severity = "Medium"
        else:
            severity = "High"

        recommendation = "Transfer Excess Inventory"

        reason = (
            f"Closing stock ({stock}) exceeds overstock threshold (300)"
        )

    # --------------------------------------
    # UNDERSTOCK
    # --------------------------------------

    elif stock < reorder_level:

        issue_type = "Understock"

        difference = reorder_level - stock

        if difference <= 20:
            severity = "Low"
        elif difference <= 50:
            severity = "Medium"
        else:
            severity = "High"

        recommendation = "Reorder / Receive Inventory"

        reason = (
            f"Closing stock ({stock}) below reorder level ({reorder_level})"
        )

    # --------------------------------------
    # SAVE ONLY ISSUES
    # --------------------------------------

    if issue_type is not None:

        results.append({

            "date": row["date"],

            "store_id": row["store_id"],

            "product_id": row["product_id"],

            "product_name": row["product_name"],

            "category": row["category"],

            "closing_stock": stock,

            "reorder_level": reorder_level,

            "issue_type": issue_type,

            "severity": severity,

            "recommendation": recommendation,

            "reason": reason

        })

# ==========================================
# SAVE RESULTS
# ==========================================

output = pd.DataFrame(results)

output.to_csv(
    "data/processed/inventory_imbalance.csv",
    index=False
)

# ==========================================
# SUMMARY
# ==========================================

print("=" * 50)
print("INVENTORY IMBALANCE ANALYSIS COMPLETE")
print("=" * 50)

print(f"Latest Inventory Date : {latest_date}")
print(f"Total Issues Found    : {len(output)}")

print()

print(output["issue_type"].value_counts())

print()

print(output["severity"].value_counts())

print("=" * 50)

print("\nSample Recommendations:\n")

print(output.head(10))