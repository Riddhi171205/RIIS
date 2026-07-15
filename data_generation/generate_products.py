import pandas as pd
import random

# Number of suppliers available
NUM_SUPPLIERS = 10

categories = {
    "Grocery": {
        "Rice": ["India Gate", "Daawat", "Fortune"],
        "Atta": ["Aashirvaad", "Fortune", "Pillsbury"],
        "Oil": ["Fortune", "Saffola", "Dhara"],
        "Sugar": ["Madhur", "Trust", "Organic India"],
    },
    "Dairy": {
        "Milk": ["Amul", "Mother Dairy"],
        "Butter": ["Amul", "Britannia"],
        "Cheese": ["Amul", "Britannia"],
    },
    "Snacks": {
        "Chips": ["Lay's", "Kurkure"],
        "Biscuits": ["Britannia", "Parle"],
    },
    "Beverages": {
        "Tea": ["Tata Tea", "Red Label"],
        "Coffee": ["Nescafe", "Bru"],
    },
    "Personal Care": {
        "Soap": ["Dove", "Lux", "Lifebuoy"],
        "Shampoo": ["Clinic Plus", "Pantene", "Head & Shoulders"],
        "Toothpaste": ["Colgate", "Pepsodent"],
    },
    "Household": {
        "Detergent": ["Surf Excel", "Ariel", "Wheel"],
        "Dishwash": ["Vim", "Pril"],
    }
}

rows = []
product_id = 1001

for category, subcategories in categories.items():

    for subcategory, brands in subcategories.items():

        for brand in brands:

            for i in range(1, 21):   # 20 products per brand

                cost_price = random.randint(20, 500)
                margin = random.uniform(1.10, 1.35)

                rows.append({

                    "product_id": product_id,

                    "sku": f"SKU{product_id}",

                    "product_name": f"{brand} {subcategory} {i}",

                    "category": category,

                    "subcategory": subcategory,

                    "brand": brand,

                    "unit": "1 Unit",

                    "cost_price": cost_price,

                    "selling_price": round(cost_price * margin, 2),

                    "shelf_life_days": random.choice(
                        [30, 90, 180, 365, 730]
                    ),

                    "reorder_level": random.randint(20, 100),

                    # NEW COLUMN
                    "supplier_id": random.randint(1, NUM_SUPPLIERS)

                })

                product_id += 1

# Create DataFrame
products = pd.DataFrame(rows)

# Save CSV
products.to_csv(
    "data/raw/products.csv",
    index=False
)

# Summary
print("=" * 50)
print("PRODUCTS GENERATED SUCCESSFULLY")
print("=" * 50)
print(f"Total Products : {len(products)}")
print(f"Total Suppliers: {NUM_SUPPLIERS}")
print("=" * 50)

print("\nSample Data:\n")
print(products.head())