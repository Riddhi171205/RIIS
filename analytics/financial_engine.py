import pandas as pd

# ==========================================
# LOAD DATA
# ==========================================

imbalance = pd.read_csv("data/processed/inventory_imbalance.csv")
transfer = pd.read_csv("data/processed/transfer_recommendation.csv")
markdown = pd.read_csv("data/processed/markdown_recommendation.csv")
reorder = pd.read_csv("data/processed/reorder_recommendation.csv")

# ==========================================
# CALCULATE KPIs
# ==========================================

overstock = len(
    imbalance[imbalance["issue_type"] == "Overstock"]
)

understock = len(
    imbalance[imbalance["issue_type"] == "Understock"]
)

transfer_count = len(transfer)

markdown_count = len(markdown)

reorder_count = len(reorder)

total_transfer_qty = transfer["transfer_quantity"].sum()

total_reorder_qty = reorder["recommended_order_qty"].sum()

# ==========================================
# BUSINESS IMPACT ESTIMATION
# ==========================================

inventory_carrying_cost_saved = total_transfer_qty * 12

markdown_revenue_recovered = markdown_count * 350

stockout_loss_prevented = total_reorder_qty * 45

total_business_impact = (
    inventory_carrying_cost_saved
    + markdown_revenue_recovered
    + stockout_loss_prevented
)

# ==========================================
# INVENTORY HEALTH SCORE
# ==========================================

total_cases = overstock + understock

if total_cases == 0:
    health_score = 100
else:
    health_score = round(
        100 - ((understock / total_cases) * 100),
        2
    )

# ==========================================
# CREATE REPORT
# ==========================================

report = pd.DataFrame({

    "Metric":[

        "Overstock Cases",
        "Understock Cases",
        "Transfer Recommendations",
        "Markdown Recommendations",
        "Reorder Recommendations",
        "Total Transfer Quantity",
        "Total Reorder Quantity",
        "Inventory Carrying Cost Saved (₹)",
        "Markdown Revenue Recovery (₹)",
        "Stockout Loss Prevented (₹)",
        "Total Estimated Business Impact (₹)",
        "Inventory Health Score"

    ],

    "Value":[

        overstock,
        understock,
        transfer_count,
        markdown_count,
        reorder_count,
        total_transfer_qty,
        total_reorder_qty,
        inventory_carrying_cost_saved,
        markdown_revenue_recovered,
        stockout_loss_prevented,
        total_business_impact,
        health_score

    ]

})

# ==========================================
# SAVE OUTPUT
# ==========================================

report.to_csv(
    "data/processed/financial_impact.csv",
    index=False
)

# ==========================================
# SUMMARY
# ==========================================

print("=" * 70)
print("FINANCIAL IMPACT ENGINE COMPLETE".center(70))
print("=" * 70)

for _, row in report.iterrows():
    print(f"{row['Metric']:<45} : {row['Value']}")

print("=" * 70)

for _, row in report.iterrows():

    value = row["Value"]

    if isinstance(value, (int, float)):
        if value % 1 == 0:
            value = f"{int(value):,}"
        else:
            value = f"{value:,.2f}"

    print(f"{row['Metric']:<45} : {value}")