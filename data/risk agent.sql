TRUNCATE TABLE risk_assessments;

INSERT INTO risk_assessments (
    action_id,
    churn_risk,
    fatigue_risk,
    delivery_risk,
    margin_risk,
    hard_block
)
SELECT
    ca.action_id,

    -- Churn risk (0–1)
    LEAST(
        1.0,
        GREATEST(
            0.0,
            (features->>'days_since_last_order')::NUMERIC / 90
        )
    ) AS churn_risk,

    -- Fatigue risk (0–1)
    LEAST(
        1.0,
        GREATEST(
            0.0,
            (features->>'orders_last_30d')::NUMERIC / 10
        )
    ) AS fatigue_risk,

    -- Delivery risk (severity-based)
    COALESCE((features->>'delivery_risk')::NUMERIC, 0) AS delivery_risk,

    -- Margin risk (v1 placeholder)
    0.0 AS margin_risk,

    -- HARD BLOCK LOGIC
    CASE
        -- High churn → no proactive selling
        WHEN (features->>'days_since_last_order')::INT > 60
             AND ca.action_type IN ('UPSELL', 'CROSS_SELL')
            THEN TRUE

        -- Over-targeting risk
        WHEN (features->>'orders_last_30d')::INT > 6
            THEN TRUE

        -- Severe delivery issues → block upsell
        WHEN COALESCE((features->>'delivery_risk')::NUMERIC, 0) > 0.6
             AND ca.action_type = 'UPSELL'
            THEN TRUE

        ELSE FALSE
    END AS hard_block

FROM candidate_actions ca
JOIN latest_customer_features lcf
  ON ca.customer_id = lcf.customer_id;

  
-- sanity

SELECT
    ca.action_type,
    ra.delivery_risk,
    ra.hard_block
FROM risk_assessments ra
JOIN candidate_actions ca
  ON ra.action_id = ca.action_id
ORDER BY ra.delivery_risk DESC
LIMIT 20;