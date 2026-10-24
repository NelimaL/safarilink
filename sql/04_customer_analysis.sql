
-- 1: Check the customer table
SELECT *
FROM customers
LIMIT 5;


--  2: Compare customer segments
SELECT
    c.segment,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(b.booking_id) AS total_bookings,
    COALESCE(SUM(b.seats), 0) AS total_tickets,
    ROUND(COALESCE(SUM(b.revenue), 0), 2) AS total_revenue_kes,
    ROUND(
        COALESCE(SUM(b.revenue), 0) /
        NULLIF(COUNT(DISTINCT c.customer_id), 0),
        2
    ) AS revenue_per_customer_kes
FROM customers AS c
LEFT JOIN bookings AS b
    ON c.customer_id = b.customer_id
GROUP BY c.segment
ORDER BY total_revenue_kes DESC;


--3: Compare churn status by customer segment
SELECT
    segment,
    churned,
    COUNT(*) AS total_customers
FROM customers
GROUP BY segment, churned
ORDER BY segment, churned;
