
-- 1: Revenue and bookings by route
SELECT
    route,
    COUNT(*) AS total_bookings,
    SUM(seats) AS total_tickets,
    ROUND(SUM(revenue), 2) AS total_revenue_kes
FROM bookings
GROUP BY route
ORDER BY total_revenue_kes DESC;


-- 2: Monthly demand and revenue
SELECT
    year_month,
    COUNT(*) AS total_bookings,
    SUM(seats) AS total_tickets,
    ROUND(SUM(revenue), 2) AS total_revenue_kes
FROM bookings
GROUP BY year_month
ORDER BY year_month;


-- 3: Revenue by payment method
SELECT
    payment,
    COUNT(*) AS total_bookings,
    SUM(seats) AS total_tickets,
    ROUND(SUM(revenue), 2) AS total_revenue_kes
FROM bookings
GROUP BY payment
ORDER BY total_revenue_kes DESC;


-- 4: Revenue by county
SELECT
    county,
    COUNT(*) AS total_bookings,
    ROUND(SUM(revenue), 2) AS total_revenue_kes
FROM bookings
GROUP BY county
ORDER BY total_revenue_kes DESC;


-- 5: Holiday versus ordinary-day demand
SELECT
    CASE
        WHEN is_holiday = 1 THEN 'Holiday'
        WHEN near_holiday = 1 THEN 'Near holiday'
        ELSE 'Ordinary day'
    END AS day_type,
    COUNT(*) AS total_bookings,
    SUM(seats) AS total_tickets,
    ROUND(SUM(revenue), 2) AS total_revenue_kes
FROM bookings
GROUP BY day_type
ORDER BY total_revenue_kes DESC;

-- 6: Rank routes by revenue and calculate revenue share
SELECT
    route,
    ROUND(SUM(revenue), 2) AS total_revenue_kes,

    RANK() OVER (
        ORDER BY SUM(revenue) DESC
    ) AS revenue_rank,

    ROUND(
        100.0 * SUM(revenue) /
        SUM(SUM(revenue)) OVER (),
        2
    ) AS revenue_share_pct

FROM bookings
GROUP BY route
ORDER BY revenue_rank;
