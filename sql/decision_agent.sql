-- SQL for decision agent
INSERT INTO decisions (
    decision_id,
    customer_id,
    chosen_action,
    expected_utility,
    explanation,
    decided_at
)
WITH scored_actions AS (
    SELECT
        ca.action_id,
        ca.customer_id,
        ca.action_type,
        ca.score,

        ra.churn_risk,
        ra.fatigue_risk,
        ra.delivery_risk,
        ra.hard_block,

        -- -------------------------
        -- Utility function
        -- -------------------------
        CASE
            WHEN ra.hard_block = TRUE THEN -1
            ELSE
                ca.score
                * (1 - ra.churn_risk)
                * (1 - ra.fatigue_risk)
                * (1 - ra.delivery_risk)
        END AS utility
    FROM candidate_actions ca
    JOIN risk_assessments ra
      ON ca.action_id = ra.action_id
),

ranked_actions AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY utility DESC
        ) AS rn
    FROM scored_actions
)

SELECT
    gen_random_uuid() AS decision_id,
    customer_id,
    action_id AS chosen_action,
    utility AS expected_utility,

    jsonb_build_object(
        'action_type', action_type,
        'base_score', score,
        'utility', utility,
        'churn_risk', churn_risk,
        'fatigue_risk', fatigue_risk,
        'delivery_risk', delivery_risk,
        'hard_block', hard_block,
        'decision_rule',
            CASE
                WHEN utility < 0 THEN 'BLOCKED_BY_RISK'
                ELSE 'MAX_UTILITY_ACTION'
            END
    ) AS explanation,

    NOW() AS decided_at
FROM ranked_actions
WHERE rn = 1;