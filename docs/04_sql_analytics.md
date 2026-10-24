# Milestone 3: SQL Analytics — SafariLink Transport Services

## 1. Objective

The objective of this milestone was to use SQL to analyse SafariLink's cleaned booking and customer data and answer management questions about route revenue, demand, payment methods, customer segments, and customer behaviour.

## 2. Tools and data

- **SQL engine:** SQLite
- **Database:** `data/safarilink.db`
- **Booking table:** `bookings`
- **Customer table:** `customers`
- **Booking records loaded:** 690,708
- **Registered customers:** 6,000

The data was cleaned before being loaded into the database. SQL scripts are saved in the `sql/` directory.

## 3. SQL techniques demonstrated

- **Aggregations:** `COUNT`, `SUM`, `AVG`, and `GROUP BY` to summarize bookings, tickets, and revenue.
- **Sorting and ranking:** `ORDER BY` and `RANK()` to identify the highest-revenue routes.
- **Window functions:** `RANK()` and `NTILE()` to rank routes and score customers.
- **Joins:** `LEFT JOIN` to combine bookings with customer information.
- **Customer cohorts:** Grouping registered customers by signup month.
- **RFM analysis:** Ranking customers using recency, frequency, and monetary value.

## 4. Key findings

### Route performance

The Nairobi–Mombasa route generated KES 239.54 million, followed by Mombasa–Nairobi at KES 239.03 million and Nairobi–Kisumu at KES 223.70 million. Together, these three routes contributed approximately 48.7% of total booking revenue.

### Customer segments

The commuter segment generated approximately KES 825.13 million across 394,868 bookings. Business customers generated approximately KES 298.51 million, while occasional customers generated KES 305.45 million.

### Customer cohorts

The cohort query returned 44 monthly signup cohorts from January 2023 to August 2026. January 2023 recorded 1,626 sign-ups, considerably more than later months. This should be checked against the synthetic data-generation process before being interpreted as a genuine acquisition trend.

### RFM segmentation

The RFM query calculated recency in days, booking frequency, monetary value, and scores from 1 to 5. Customers were classified into groups such as high-value active, loyal active, at-risk, low-frequency, and regular customers. These classifications can help inform customer retention and engagement strategies.

## 5. Business recommendations

1. Review capacity and service reliability on the three highest-revenue routes.
2. Investigate ways to encourage occasional customers to book more frequently.
3. Develop retention campaigns for customers identified as at risk.
4. Validate signup-date patterns before using cohort results to assess acquisition performance.
5. Combine revenue with operating costs and capacity utilization before making decisions about route profitability.

## 6. Limitations

The dataset is synthetic, so findings demonstrate an analytical workflow rather than verified performance of a real transport operator. Revenue is not profit because operating costs are not included. The cohort query measures customer acquisition by signup month, not retention. RFM segments are relative to the dataset and depend on the scoring rules selected.

## 7. Evidence

Supporting SQL scripts and query results are stored in the `sql/` directory and captured in screenshots for the capstone submission.