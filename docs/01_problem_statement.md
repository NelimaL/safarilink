# 1. Problem Statement

## Project: SafariLink Transport Intelligence

### 1.1 Background and Context

SafariLink Transport Services is a fictional Kenyan company that provides intercity passenger and parcel transport services. It operates through branches across Kenya and allows customers to purchase tickets through branch counters, agents, and M-Pesa.

As the company grows, management needs a clearer picture of how the business is performing. It needs to understand which routes generate the most revenue, when passenger demand is highest, which customers return regularly, and whether the available buses have enough seats to meet demand.

At the moment, these questions cannot be answered reliably from a single, consolidated view of the business. Without clear evidence, decisions about bus allocation, promotions, customer retention, and future capacity planning risk being based on assumptions rather than data.

### 1.2 The Business Problem

SafariLink needs a data-driven approach to understanding its bookings, revenue, routes, branches, and passengers. Management wants to identify profitable routes, recognise seasonal demand patterns, understand customer purchasing behaviour, and estimate how many bookings each route may receive in the coming month.

The goal of this project is to turn booking data into practical insights that help the company make better operational and commercial decisions. These insights should help management allocate buses more effectively, improve seat utilisation, evaluate promotions, and identify customers who may be at risk of becoming inactive.

### 1.3 Project Scope and Data

The project will use a synthetic dataset representing SafariLink's operations. The planned dataset will cover:

- **12 routes** connecting locations across Kenya.
- **10 branches** operating across 10 counties.
- Approximately **6,000 passengers**.
- Approximately **45 months of booking activity**.

All operational records, including bookings, passengers, routes, branches, and trips, will be generated using my own Python script. Publicly available contextual data, such as Kenya's public holiday calendar, will be used where appropriate and documented in the project.

Because the operational data is synthetic, the findings will demonstrate how data analytics can support transport business decisions. They should not be interpreted as evidence of the actual performance of a real transport company.

### 1.4 Business Questions and Project Objectives

The project will address six main objectives.

| No. | Objective | Business questions | Measures of success |
|---|---|---|---|
| 1 | Evaluate revenue and operational performance | Which branches, counties, and routes generate the most revenue? Which routes have low seat utilisation? | Revenue, booking volumes, average fare, seat utilisation, and revenue per kilometre by route, branch, and county |
| 2 | Understand trends and passenger behaviour | How does demand change over time? Are bookings higher during school holidays or public holidays? How is the payment-method mix changing? | Month-on-month and year-on-year growth, monthly seasonal indices, holiday demand uplift, and M-Pesa share over time |
| 3 | Segment customers using RFM analysis | Who are the most valuable passengers? Which customers are becoming less active? | Recency, frequency, and monetary scores from 1–5; segment sizes; revenue contribution by segment; and a clearly defined inactivity measure |
| 4 | Test business hypotheses statistically | Are bookings associated with promotions? Do M-Pesa customers spend more than other customers? Is payment method associated with route class? | P-values, 95% confidence intervals, effect sizes, and documented checks of statistical assumptions |
| 5 | Forecast monthly booking demand | How many bookings should each route expect in the following month? | Mean Absolute Error (MAE) and Weighted Absolute Percentage Error (WAPE) on a time-based test set, compared with a seasonal-naive baseline. The target is to reduce forecast error by at least 15% compared with the baseline |
| 6 | Build a dashboard and provide recommendations | What should managers monitor, and what actions could improve performance? | An interactive dashboard covering the key business questions and 3–5 evidence-based recommendations supported by numerical findings |

The 15% forecasting improvement is a project target, not a guaranteed outcome. If the model does not meet it, the results will be reported honestly and compared with the baseline.

### 1.5 Translating Retail Analytics into Transport Analytics

Although the original analytics framework is commonly used in retail, its concepts can be adapted to passenger transport.

| Retail concept | SafariLink equivalent |
|---|---|
| Store | Transport branch |
| Product | Route or transport service |
| Customer | Passenger |
| Transaction | Ticket booking |
| Inventory or available stock | Available seats |
| Product demand | Route booking demand |

This mapping allows established retail analytics techniques to be applied to a transport business context.

### 1.6 Key Business Definitions

To keep the analysis consistent, the following definitions will be used throughout the project.

- **Revenue:** The amount earned from completed journeys, calculated using the applicable ticket fare multiplied by the number of tickets travelled, after any applicable discount. Cancelled and no-show bookings will not count as completed-journey revenue. The analysis will distinguish gross ticket value from net realised revenue.

- **Booking:** One ticket transaction recorded in the booking dataset. Duplicate records must be identified and handled before calculating booking volumes.

- **Seat utilisation (load factor):** The number of passengers who travelled divided by the available seat capacity for the relevant trips, multiplied by 100. The denominator must reflect the trips included in the analysis.

- **Active customer:** A passenger with at least one qualifying booking in the 90 days before the analysis date. For retention analysis, qualifying bookings should be defined consistently, preferably using completed journeys.

- **Churned or inactive customer:** A passenger who previously met the activity criteria but has had no qualifying booking during the most recent 90-day period. This is a project-defined inactivity measure, not proof that the passenger has permanently stopped using the service.

- **Recency:** The number of days since a passenger's most recent qualifying booking, measured against a fixed analysis date.

- **Frequency:** The number of qualifying bookings made by a passenger during the selected analysis period.

- **Monetary value:** The total net revenue attributable to a passenger during the selected analysis period.

- **Holiday uplift:** The percentage difference in booking demand on defined holiday dates compared with an appropriate non-holiday comparison period. Calendar effects and other seasonal differences should be considered before interpreting this as a holiday effect.

### 1.7 Expected Outcome

By the end of the project, SafariLink will have a documented and reproducible analytics workflow covering data generation, data cleaning, exploratory analysis, SQL analysis, customer segmentation, hypothesis testing, demand forecasting, and dashboard development.

The final deliverables will include a cleaned and validated dataset, documented SQL queries, Python analysis and modelling notebooks, forecast evaluation results, an interactive dashboard, and practical recommendations for management.

The project will also document its assumptions, data-quality limitations, and analytical methods so that the results can be explained and evaluated during the technical defence.

### Definitions
## Revenue = fare × number of tickets actually travelled.
## Booking = one ticket transaction.
## Active customer = one or more bookings in the last 90 days.
## Churned = active before, no booking in 90 days.

**Overall goal:** To demonstrate how well-structured data analysis can help a transport company understand its performance, plan capacity, and make more informed business decisions.