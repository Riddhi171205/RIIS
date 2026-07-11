-- Product Table
CREATE TABLE IF NOT EXISTS dim_product (
    product_id INT PRIMARY KEY,
    sku VARCHAR(50),
    product_name VARCHAR(255),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    brand VARCHAR(100),
    unit VARCHAR(50),
    cost_price NUMERIC,
    selling_price NUMERIC,
    shelf_life_days INT,
    reorder_level INT
);

-- Supplier Table
CREATE TABLE IF NOT EXISTS dim_supplier (
    supplier_id INT PRIMARY KEY,
    supplier_name VARCHAR(255),
    city VARCHAR(100),
    lead_time_days INT,
    contact_email VARCHAR(255)
);

-- Sales Table
CREATE TABLE IF NOT EXISTS fact_sales (
    sale_id BIGINT PRIMARY KEY,
    date DATE,
    store_id INT,
    product_id INT,
    quantity_sold INT,
    unit_price NUMERIC,
    total_revenue NUMERIC
);

-- Inventory Table
CREATE TABLE IF NOT EXISTS fact_inventory (
    inventory_id BIGINT PRIMARY KEY,
    date DATE,
    store_id INT,
    product_id INT,
    opening_stock INT,
    quantity_sold INT,
    closing_stock INT,
    expiry_date DATE
);