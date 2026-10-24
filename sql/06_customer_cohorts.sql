
-- Customer acquisition cohorts by signup month

WITH customer_cohorts AS (
    SELECT
        strftime('%Y-%m', signup_date) AS cohort_month,
        customer_id,
        segment
    FROM customers
    WHERE signup_date IS NOT NULL
)
SELECT
    cohort_month,
    COUNT(DISTINCT customer_id) AS customers_acquired,
    SUM(CASE WHEN segment = 'commuter' THEN 1 ELSE 0 END)
        AS commuter_customers,
    SUM(CASE WHEN segment = 'occasional' THEN 1 ELSE 0 END)
        AS occasional_customers,
    SUM(CASE WHEN segment = 'business' THEN 1 ELSE 0 END)
        AS business_customers
FROM customer_cohorts
GROUP BY cohort_month
ORDER BY cohort_month;
