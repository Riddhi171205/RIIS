import pandas as pd
import random

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
pid = 1001

for category, subcats in categories.items():
    for subcat, brands in subcats.items():
        for brand in brands:
            for i in range(1, 21):  # 20 products per brand
                cost = random.randint(20, 500)
                margin = random.uniform(1.10, 1.35)

                rows.append({
                    "product_id": pid,
                    "sku": f"SKU{pid}",
                    "product_name": f"{brand} {subcat} {i}",
                    "category": category,
                    "subcategory": subcat,
                    "brand": brand,
                    "unit": "1 Unit",
                    "cost_price": cost,
                    "selling_price": round(cost * margin, 2),
                    "shelf_life_days": random.choice([30, 90, 180, 365, 730]),
                    "reorder_level": random.randint(20, 100)
                })

                pid += 1

df = pd.DataFrame(rows)

df.to_csv("data/raw/products.csv", index=False)

print(df.head())
print(f"\n✅ Total Products Generated: {len(df)}")