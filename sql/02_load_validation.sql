
-- 1. Count the imported bookings
SELECT COUNT(*) AS total_bookings
FROM bookings;

-- 2. Check the booking date range
SELECT
    MIN(date) AS first_booking_date,
    MAX(date) AS last_booking_date
FROM bookings;

-- 3. Calculate total revenue
SELECT
    ROUND(SUM(revenue), 2) AS total_revenue_kes
FROM bookings;

-- 4. Check the available columns
PRAGMA table_info(bookings);

-- 5. Preview five records
SELECT *
FROM bookings
LIMIT 5;
