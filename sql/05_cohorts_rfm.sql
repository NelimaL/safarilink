
-- RFM ANALYSIS: Score registered customers by booking behaviour

WITH customer_rfm AS (
    SELECT
        c.customer_id,
        c.segment,
        MAX(b.date) AS last_booking_date,
        CAST(
            julianday('2026-09-30') - julianday(MAX(b.date))
            AS INTEGER
        ) AS recency_days,
        COUNT(b.booking_id) AS frequency,
        ROUND(COALESCE(SUM(b.revenue), 0), 2) AS monetary_value
    FROM customers AS c
    LEFT JOIN bookings AS b
        ON c.customer_id = b.customer_id
    GROUP BY c.customer_id, c.segment
),
scored AS (
    SELECT
        *,
        NTILE(5) OVER (
            ORDER BY recency_days DESC
        ) AS recency_score,
        NTILE(5) OVER (
            ORDER BY frequency ASC
        ) AS frequency_score,
        NTILE(5) OVER (
            ORDER BY monetary_value ASC
        ) AS monetary_score
    FROM customer_rfm
    WHERE last_booking_date IS NOT NULL
)
SELECT
    customer_id,
    segment,
    last_booking_date,
    recency_days,
    frequency,
    monetary_value,
    recency_score,
    frequency_score,
    monetary_score,
    CASE
        WHEN recency_score >= 4
             AND frequency_score >= 4
             AND monetary_score >= 4
            THEN 'High-value active customers'
        WHEN recency_score >= 4
             AND frequency_score >= 3
            THEN 'Loyal active customers'
        WHEN recency_score <= 2
             AND frequency_score >= 3
            THEN 'At-risk customers'
        WHEN frequency_score <= 2
            THEN 'Low-frequency customers'
        ELSE 'Regular customers'
    END AS rfm_segment
FROM scored
ORDER BY monetary_value DESC;
