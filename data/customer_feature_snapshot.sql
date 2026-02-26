-- =========================================
-- CUSTOMER FEATURE SNAPSHOT (v1)
-- One row per customer per snapshot_date
-- =========================================

-- Choose snapshot date (usually today or max order date)
TRUNCATE TABLE customer_feature_snapshots;

WITH ref AS (
    SELECT TIMESTAMP '2024-11-04 20:29:15' AS reference_date
),

-- -------------------------
-- Order aggregates
-- -------------------------
order_agg AS (
    SELECT
        o.customer_id,
        COUNT(*)                                  AS total_orders,
        SUM(o.order_total)                       AS total_spend,
        AVG(o.order_total)                       AS avg_order_value,
        MIN(o.order_date)                        AS first_order_date,
        MAX(o.order_date)                        AS last_order_date,
        COUNT(*) FILTER (
            WHERE o.order_date >= (SELECT reference_date FROM ref) - INTERVAL '30 days'
        )                                        AS orders_last_30d
    FROM orders o
    GROUP BY o.customer_id
),

-- -------------------------
-- Delivery severity signals
-- -------------------------
delivery_agg AS (
    SELECT
        o.customer_id,

        -- Average delay severity (minutes)
        AVG(
            CASE
                WHEN d.actual_time > d.promised_time
                THEN EXTRACT(EPOCH FROM (d.actual_time - d.promised_time)) / 60
                ELSE 0
            END
        ) AS avg_delay_minutes,

        -- % of deliveries that were late
        COUNT(*) FILTER (
            WHERE d.actual_time > d.promised_time
        )::NUMERIC / NULLIF(COUNT(*), 0) AS late_delivery_rate

    FROM delivery d
    JOIN orders o ON d.order_id = o.order_id
    GROUP BY o.customer_id
),

-- -------------------------
-- Product signals
-- -------------------------
product_agg AS (
    SELECT
        o.customer_id,
        COUNT(DISTINCT p.category)               AS category_diversity,
        COUNT(DISTINCT p.brand)                  AS brand_diversity,
        MODE() WITHIN GROUP (ORDER BY p.category) AS top_category
    FROM order_items oi
    JOIN orders o   ON oi.order_id = o.order_id
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY o.customer_id
)

-- -------------------------
-- FINAL SNAPSHOT
-- -------------------------
INSERT INTO customer_feature_snapshots (customer_id, snapshot_date, features)
SELECT
    c.customer_id,
    (SELECT reference_date::DATE FROM ref),
    jsonb_build_object(
        -- Value / CLTV proxies
        'total_orders', oa.total_orders,
        'total_spend', oa.total_spend,
        'avg_order_value', oa.avg_order_value,
        'customer_tenure_days',
            DATE_PART('day', (SELECT reference_date FROM ref) - oa.first_order_date),
        'orders_last_30d', oa.orders_last_30d,

        -- Engagement / churn
        'days_since_last_order',
            DATE_PART('day', (SELECT reference_date FROM ref) - oa.last_order_date),

        -- Delivery risk (NEW)
        'avg_delay_minutes', da.avg_delay_minutes,
        'late_delivery_rate', da.late_delivery_rate,
        'delivery_risk',
            LEAST(
                1.0,
                COALESCE(da.avg_delay_minutes, 0) / 45
            ),

        -- Recommendation signals
        'top_category', pa.top_category,
        'category_diversity', pa.category_diversity,
        'brand_diversity', pa.brand_diversity
    )
FROM customers c
LEFT JOIN order_agg oa   ON c.customer_id = oa.customer_id
LEFT JOIN delivery_agg da ON c.customer_id = da.customer_id
LEFT JOIN product_agg pa ON c.customer_id = pa.customer_id;

SELECT
    MIN((features->>'delivery_risk')::NUMERIC),
    MAX((features->>'delivery_risk')::NUMERIC)
FROM customer_feature_snapshots;