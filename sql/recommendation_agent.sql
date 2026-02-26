-- SQL for recommendation agent
CREATE OR REPLACE VIEW latest_customer_features AS
SELECT DISTINCT ON (customer_id)
    customer_id,
    snapshot_date,
    features
FROM customer_feature_snapshots
ORDER BY customer_id, snapshot_date DESC;

INSERT INTO candidate_actions (
    action_id,
    customer_id,
    action_type,
    target_category,
    score,
    generated_at
)
SELECT
    gen_random_uuid()                        AS action_id,
    lcf.customer_id,
    CASE
        WHEN (features->>'days_since_last_order')::INT > 45
            THEN 'NO_ACTION'
        WHEN (features->>'orders_last_30d')::INT >= 2
             AND (features->>'avg_order_value')::NUMERIC >= 500
            THEN 'UPSELL'
        WHEN (features->>'orders_last_30d')::INT >= 1
             AND (features->>'category_diversity')::INT <= 2
            THEN 'CROSS_SELL'
        ELSE 'NO_ACTION'
    END                                      AS action_type,
    CASE
        WHEN (features->>'category_diversity')::INT <= 2
            THEN features->>'top_category'
        ELSE NULL
    END                                      AS target_category,
    -- simple confidence score
    LEAST(
        1.0,
        GREATEST(
            0.1,
            (features->>'orders_last_30d')::NUMERIC / 5
        )
    )                                        AS score,
    NOW()                                    AS generated_at
FROM latest_customer_features lcf;






