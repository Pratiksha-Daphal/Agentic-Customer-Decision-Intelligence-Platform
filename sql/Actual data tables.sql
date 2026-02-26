DROP TABLE IF EXISTS delivery, order_items, orders, products, customers CASCADE;

CREATE TABLE customers (
    customer_id BIGINT PRIMARY KEY,
    customer_name TEXT,
    email TEXT,
    phone TEXT,
    area TEXT,
    pincode TEXT,
    registration_date DATE,
    customer_segment TEXT
);

CREATE TABLE products (
    product_id BIGINT PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    brand TEXT,
    price NUMERIC,
    mrp NUMERIC,
    margin_percentage NUMERIC,
    shelf_life_days INT
);

CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY,
    customer_id BIGINT REFERENCES customers(customer_id),
    order_date TIMESTAMP,
    order_total NUMERIC,
    payment_method TEXT,
    delivery_status TEXT,
    store_id BIGINT
);

CREATE TABLE order_items (
    order_item_id BIGSERIAL PRIMARY KEY,
    order_id BIGINT REFERENCES orders(order_id),
    product_id BIGINT REFERENCES products(product_id),
    quantity INT,
    unit_price NUMERIC
);

CREATE TABLE delivery (
    order_id BIGINT PRIMARY KEY REFERENCES orders(order_id),
    delivery_partner_id BIGINT,
    promised_time TIMESTAMP,
    actual_time TIMESTAMP,
    delivery_time_minutes INT,
    distance_km NUMERIC,
    delivery_status TEXT,
    reasons_if_delayed TEXT
);


INSERT INTO customers
SELECT DISTINCT
    customer_id,
    customer_name,
    email,
    phone,
    area,
    pincode,
    registration_date,
    customer_segment
FROM raw_customers;

INSERT INTO products
SELECT DISTINCT
    product_id,
    product_name,
    category,
    brand,
    price,
    mrp,
    margin_percentage,
    shelf_life_days
FROM raw_products;

INSERT INTO orders
SELECT
    order_id,
    customer_id,
    order_date,
    order_total,
    payment_method,
    delivery_status,
    store_id
FROM raw_orders
WHERE customer_id IN (SELECT customer_id FROM customers);

INSERT INTO order_items (order_id, product_id, quantity, unit_price)
SELECT
    oi.order_id,
    oi.product_id,
    oi.quantity,
    oi.unit_price
FROM raw_order_items oi
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.order_id = oi.order_id
)
AND EXISTS (
    SELECT 1
    FROM products p
    WHERE p.product_id = oi.product_id
);


SELECT COUNT(*) AS orphan_order_items
FROM raw_order_items oi
LEFT JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;



INSERT INTO delivery
SELECT
    order_id,
    delivery_partner_id,
    promised_time,
    actual_time,
    delivery_time_minutes,
    distance_km,
    delivery_status,
    reasons_if_delayed
FROM raw_delivery
WHERE order_id IN (SELECT order_id FROM orders);


CREATE INDEX idx_orders_customer_date
ON orders(customer_id, order_date);

CREATE INDEX idx_order_items_order
ON order_items(order_id);

CREATE INDEX idx_products_category
ON products(category);

CREATE INDEX idx_delivery_status
ON delivery(delivery_status);

UPDATE delivery
SET delivery_time_minutes =
    CASE
        WHEN actual_time IS NULL OR promised_time IS NULL THEN NULL
        ELSE EXTRACT(EPOCH FROM (actual_time - promised_time)) / 60
    END;


SELECT
    MIN(delivery_time_minutes),
    MAX(delivery_time_minutes),
    AVG(delivery_time_minutes)
FROM delivery;


select * from customers;
