CREATE TEMP VIEW cltv_training_view AS
WITH ref AS (
    SELECT TIMESTAMP '2024-11-04 20:29:15' AS reference_date
),
base_features AS (
    SELECT
        cfs.customer_id,
        (cfs.features->>'total_orders')::INT          AS total_orders,
        (cfs.features->>'total_spend')::FLOAT         AS total_spend,
        (cfs.features->>'avg_order_value')::FLOAT     AS avg_order_value,
        (cfs.features->>'customer_tenure_days')::INT  AS customer_tenure_days,
        (cfs.features->>'orders_last_30d')::INT       AS orders_last_30d,
        (cfs.features->>'days_since_last_order')::INT AS days_since_last_order,
        (cfs.features->>'category_diversity')::INT    AS category_diversity,
        (cfs.features->>'delivery_risk')::FLOAT       AS delivery_risk
    FROM customer_feature_snapshots cfs
),
future_value AS (
    SELECT
        o.customer_id,
        SUM(o.order_total) AS future_spend_90d
    FROM orders o
    JOIN ref r ON TRUE
    WHERE o.order_date > r.reference_date
      AND o.order_date <= r.reference_date + INTERVAL '90 days'
    GROUP BY o.customer_id
)
SELECT
    bf.*,
    COALESCE(fv.future_spend_90d, 0) AS cltv_label
FROM base_features bf
LEFT JOIN future_value fv
  ON bf.customer_id = fv.customer_id;