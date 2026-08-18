# Superstore-Automated-Data-Pipeline
An end-to-end Python data pipeline built with OOP to clean, analyze, visualize, and auto-report Superstore sales data using Pandas, Seaborn, and Jupyter.
Project Overview

Processing large-scale transactional data manually is time-consuming and error-prone. This project resolves that challenge by encapsulating data cleaning, outlier handling, statistical transformation, visualization generation, and report exporting inside a modular, reusable Python class (`SuperstoreAnalyzer`).


# Key Features & Functionality

* **Modular Architecture (OOP):** Built using a structured `SuperstoreAnalyzer` class that executes sequential execution steps cleanly.
* **Data Preprocessing & Cleaning:**
  * Standardizes column formatting and removes duplicate records.
  * Handles missing values across text and numerical metrics.
  * Applies percentile capping (1st and 99th percentiles) to neutralize extreme profit/sales outliers.
* **Feature Engineering:**
  * `shipping_duration`: Calculates total processing days from order date to ship date.
  * `profit_margin`: Measures transaction profitability percentage (`Profit / Sales`).
  * `sales_performance_category`: Segmentates orders into `Low`, `Medium`, and `High` tiers.
* **Automated Exploratory Data Analysis (EDA):** Automatically generates and exports 8 visual charts, including monthly sales trends, category performance, correlation heatmaps, and profit distribution density.
* **Executive Summary & Dataset Export:** Exports the cleaned dataset as `.csv` alongside a generated text KPI summary (`summary_report.txt`).

---

# Tech Stack & Dependencies

* **Language:** Python 3.12
* **Data Analysis & Manipulation:** Pandas, NumPy
* **Data Visualization:** Matplotlib, Seaborn
* **File Processing:** OpenPyXL, XLRD
* **Environment:** VS Code & Jupyter Notebook (`.ipynb`)


# Automated KPI Summary Output

Upon running the automated pipeline on **9,994 transaction records**, the system calculated and logged the following metrics:

*  **Total Revenue (Sales):** `$2,092,398.89`
*  **Total Net Profit:** `$262,912.48`
*  **Average Profit Margin:** `12.62%`
*  **Total Records Processed:** `9,994`


# Repository Structure

```text
├── Superstore_Project_Documentation.ipynb   # Interactive documentation & visual output
├── Python mini project.py                    # Standalone modular OOP Python script
├── Sample - Superstore 2019.xls              # Raw dataset
└── superstore_output_report/                # Generated output directory
    ├── 1_monthly_sales_trend.png             # Visualizations
    ├── 2_sales_by_category.png
    ├── ...
    ├── summary_report.txt                   # Auto-generated text summary
    └── cleaned_superstore_data.csv          # Processed dataset export
