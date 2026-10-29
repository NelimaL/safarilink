# Milestone 7: Power BI Management Dashboard

## 1. What I Built

I developed an interactive Power BI management dashboard for SafariLink Transport Services. The dashboard presents key performance indicators, monthly booking trends, route revenue, payment-method distribution, customer churn, and monthly demand forecasts.

The dashboard includes four KPI cards:
- Total Revenue
- Total Bookings
- Average Fare
- Customer Churn Rate

It also includes charts for monthly booking demand, revenue by route, bookings by payment method, and actual versus predicted monthly bookings. Three slicers allow users to filter the report by date range, route, and payment method.

## 2. How It Works

The dashboard uses the cleaned booking and customer datasets produced during the data preparation stage. The KPI cards summarise overall business performance, while the charts help management explore booking patterns, compare route revenue, understand payment preferences, and assess customer retention.

The demand forecast visual compares actual bookings with baseline and machine-learning model predictions. The date, route, and payment-method slicers allow users to investigate performance under different selection criteria.

## 3. Testing and Validation

I tested the dashboard by selecting different date ranges, routes, and payment methods and confirming that the relevant visuals responded to the selections.

I also cleared the slicers to restore the overall dataset and checked the KPI cards against the results from the cleaned data and previous analysis.

The overall figures matched the expected results:
- Total Revenue: approximately KES 1.443 billion
- Total Bookings: 690,708
- Average Fare: approximately KES 1,287
- Customer Churn Rate: 27.90%

These checks provided evidence that the dashboard measures and data connections were working as expected.

## 4. Business Value

The dashboard gives SafariLink management a consolidated view of business performance. It can support seasonal capacity planning, route-level performance reviews, payment operations, customer retention initiatives, and demand planning.

The forecasts should be interpreted alongside historical performance and operational knowledge because the underlying dataset is synthetic and model performance on real-world transport data has not yet been established.

## 5. Deliverable

**Power BI report:** `SafariLink_Management_Dashboard.pbix`

