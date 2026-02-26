DROP TABLE IF EXISTS raw_customers, raw_products, raw_orders, raw_order_items, raw_delivery CASCADE;

CREATE TABLE raw_customers (
    customer_id BIGINT,
    customer_name TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    area TEXT,
    pincode TEXT,
    registration_date DATE,
    customer_segment TEXT,
    total_orders INT,
    avg_order_value NUMERIC
);

CREATE TABLE raw_products (
    product_id BIGINT,
    product_name TEXT,
    category TEXT,
    brand TEXT,
    price NUMERIC,
    mrp NUMERIC,
    margin_percentage NUMERIC,
    shelf_life_days INT,
    min_stock_level INT,
    max_stock_level INT
);

CREATE TABLE raw_orders (
    order_id BIGINT,
    customer_id BIGINT,
    order_date TIMESTAMP,
    promised_delivery_time TIMESTAMP,
    actual_delivery_time TIMESTAMP,
    delivery_status TEXT,
    order_total NUMERIC,
    payment_method TEXT,
    delivery_partner_id BIGINT,
    store_id BIGINT
);

CREATE TABLE raw_order_items (
    order_id BIGINT,
    product_id BIGINT,
    quantity INT,
    unit_price NUMERIC
);

CREATE TABLE raw_delivery (
    order_id BIGINT,
    delivery_partner_id BIGINT,
    promised_time TIMESTAMP,
    actual_time TIMESTAMP,
    delivery_time_minutes INT,
    distance_km NUMERIC,
    delivery_status TEXT,
    reasons_if_delayed TEXT
);




SELECT COUNT(*) FROM raw_customers;
SELECT COUNT(*) FROM raw_products;
SELECT COUNT(*) FROM raw_orders;
SELECT COUNT(*) FROM raw_order_items;
SELECT COUNT(*) FROM raw_delivery;