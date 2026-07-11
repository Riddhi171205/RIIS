import pandas as pd

products = [
    # Grocery
    ["P0001", "SKU001", "India Gate Basmati Rice 5kg", "Grocery", "Rice", "India Gate", "5kg", 420, 485, 365, 50],
    ["P0002", "SKU002", "Fortune Chakki Atta 10kg", "Grocery", "Atta", "Fortune", "10kg", 380, 445, 180, 40],
    ["P0003", "SKU003", "Fortune Sunflower Oil 1L", "Grocery", "Oil", "Fortune", "1L", 145, 165, 270, 30],

    # Dairy
    ["P0004", "SKU004", "Amul Toned Milk 1L", "Dairy", "Milk", "Amul", "1L", 58, 64, 7, 100],
    ["P0005", "SKU005", "Amul Butter 500g", "Dairy", "Butter", "Amul", "500g", 265, 290, 180, 30],

    # Snacks
    ["P0006", "SKU006", "Lay's Magic Masala", "Snacks", "Chips", "Lay's", "52g", 18, 20, 180, 50],
    ["P0007", "SKU007", "Kurkure Masala Munch", "Snacks", "Chips", "Kurkure", "90g", 18, 20, 180, 50],

    # Beverages
    ["P0008", "SKU008", "Tata Tea Gold 1kg", "Beverages", "Tea", "Tata", "1kg", 560, 610, 365, 20],
    ["P0009", "SKU009", "Nescafe Classic 200g", "Beverages", "Coffee", "Nescafe", "200g", 420, 470, 365, 15],

    # Personal Care
    ["P0010", "SKU010", "Dove Soap 100g", "Personal Care", "Soap", "Dove", "100g", 42, 50, 730, 40],
]

columns = [
    "product_id",
    "sku",
    "product_name",
    "category",
    "subcategory",
    "brand",
    "unit",
    "cost_price",
    "selling_price",
    "shelf_life_days",
    "reorder_level"
]

df = pd.DataFrame(products, columns=columns)

df.to_csv("data/raw/products.csv", index=False)

print(df)
print(f"\n✅ Generated {len(df)} products successfully!")