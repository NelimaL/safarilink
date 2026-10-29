# SafariLink: Data Science and Analytics Capstone

## 1. Project Overview

SafariLink is a fictional Kenyan intercity transport company created for a Data Science and Analytics Capstone project. The project uses synthetic data to analyze passenger bookings, revenue, route performance, customer behaviour, and transport demand.

The goal is to turn transport booking data into practical insights that can help management make informed operational decisions.

## 2. Business Objectives

- Analyze booking and revenue performance across routes.
- Identify peak travel periods and high-performing routes.
- Understand customer booking patterns and retention.
- Forecast future transport demand.
- Examine payment preferences and data quality issues.
- Develop evidence-based recommendations for management.

## 3. Project Structure

```text
safarilink/
├── data/
│   ├── raw/                 # Original generated datasets
│   ├── clean/               # Cleaned and processed datasets
│   └── safarilink.db        # SQLite database
├── sql/                     # SQL scripts for analysis
├── notebooks/               # Exploratory data analysis
├── src/                     # Reusable Python scripts
├── dashboard/               # Dashboard files and assets
├── docs/                    # Project documentation and evidence
├── environment.yml          # Python environment configuration
└── README.md                # Project instructions
```

*Note: The actual files and folders in the repository may vary slightly as the project develops.*

## 4. Tools and Technologies

- Python
- pandas and NumPy
- Jupyter Notebook
- SQL and SQLite
- scikit-learn
- Matplotlib and Seaborn
- Power BI
- Git and GitHub

## 5. Data Disclaimer

SafariLink is fictional. The transport booking and customer datasets are generated for educational purposes and do not represent actual company records. Any findings and recommendations should therefore be interpreted within the context of the synthetic dataset.

## 6. Environment Setup

Install Anaconda or Miniconda, then open a terminal in the project root directory.

Create the project environment:

```bash
conda env create -f environment.yml
```

Activate the environment:

```bash
conda activate safarilink
```

If the environment already exists and you have updated `environment.yml`, update it with:

```bash
conda env update -f environment.yml --prune
```

## 7. Running the Project

Run the project from the root directory so that relative file paths resolve correctly.

The general workflow is:

1. Generate the synthetic datasets using `src/generate_data.py`, if generation is required.
2. Inspect the raw bookings and check the data using the available validation script.
3. Clean and prepare the data using `src/clean_data.py`.
4. Run the exploratory data analysis notebook in `notebooks/`.
5. Execute the SQL scripts in `sql/` in their intended order.
6. Run the statistical analysis script.
7. Run the demand forecasting script.
8. Open the Power BI dashboard and review the findings.

For example, a Python script can be run from the project root using:

```bash
python src/generate_data.py
```

Use the actual script filenames in the repository and follow any prerequisites documented in each script. Do not regenerate the data if you intend to preserve an existing dataset without first checking the script's behaviour.

## 8. Exploratory Data Analysis

The EDA examines booking trends over time, demand around public holidays, revenue by route, payment methods, and customer retention.

Open the notebook in Jupyter Notebook or VS Code and run its cells in order. Confirm that the required cleaned data files exist before running the analysis.

## 9. SQL Analysis

The SQL scripts explore booking performance, revenue, route performance, customer behaviour, and related business questions.

The project uses SQLite for its local analytical database. Run the database import script before executing SQL queries that depend on the database. Check the database and table names in the scripts before running them in a SQL client such as DBeaver.

## 10. Statistical Analysis and Forecasting

The statistical analysis examines selected relationships in the booking data. The forecasting component compares model predictions with actual monthly bookings and a baseline forecast.

Model performance should be evaluated using the metrics reported in the project documentation. Since the dataset is synthetic and the test period is limited, forecasting results should not be treated as a guarantee of real-world transport demand.

## 11. Power BI Dashboard

The Power BI management dashboard presents key performance indicators and visual analyses of:

- Total bookings and revenue
- Average fare and customer churn
- Monthly booking demand
- Revenue by route
- Bookings by payment method
- Actual and predicted monthly demand

Use the available slicers to explore results by date, route, and payment method. Clear the slicers when checking totals against the overall cleaned dataset.

## 12. Key Findings

The analysis of the current synthetic dataset identified the following patterns:

- December recorded the highest demand, with April and August also showing strong demand.
- Nairobi–Mombasa, Mombasa–Nairobi, and Nairobi–Kisumu were among the highest-revenue routes.
- M-Pesa was the most frequently recorded payment method.
- The recorded customer churn rate was 27.90%, with occasional customers showing a churn rate of 28.87%.
- Some bookings had unknown payment methods, highlighting a data quality issue.
- The forecasting model performed better than the previous-month baseline on the selected test period.

These findings describe the generated dataset and should be revalidated if the data or analysis changes.

## 13. Management Recommendations

1. Plan additional capacity around periods of higher demand, subject to seat occupancy and operating costs.
2. Monitor high-revenue routes while considering profitability, fuel, maintenance, and other operating expenses.
3. Maintain reliable M-Pesa payment processing while retaining alternative payment options.
4. Investigate occasional-customer churn and evaluate targeted retention initiatives.
5. Improve payment-method validation and investigate records with unknown payment methods.
6. Monitor monthly demand and forecast accuracy as more data becomes available.

## 14. Limitations

- The dataset is synthetic and may not reflect actual passenger behaviour.
- Missing or inconsistent fields can affect some analyses.
- Revenue alone does not establish route profitability.
- Forecasting performance on a limited test period does not guarantee future accuracy.

## 15. Reproducibility and Evidence

The repository contains the scripts, notebook, SQL queries, and documentation used to conduct the analysis. To reproduce the results, set up the Python environment, use the correct data files, and execute the workflow in the documented order.

## Get intouch
Email:nelima.lindah@gmail.com
Linkedin: www.linkedin.com/in/linda-nelima-5ab257101

