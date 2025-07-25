# 🧾 SQL Business Questions Report – Online Retail II

**Author:** Ginosca Alejandro Dávila  
**Date:** December 20, 2024  
**Script:** `2_business_questions_online_retail_ii.sql`  
**Script Location:** `sql/scripts/2_business_questions_online_retail_ii.sql`  
**Database:** `retail_sales`  
**Environment:** MySQL Workbench 8.0 CE  
**Project:** Online Retail II – Sales Analysis & Customer Segmentation

---

## 🧾 Overview

This SQL script answers **12 key business questions** using the relational schema of the `retail_sales` MySQL database. Queries explore sales trends, country insights, customer behavior, and segmentation using SQL joins, aggregation, date functions, and conditional logic.

The logic mirrors the Python-based analysis in `3_sql_analysis_sales_performance.ipynb`, validating results and preparing them for dashboarding or business presentation.

---

## 🗂️ Input Tables

| Table              | Description                                                      |
|-------------------|------------------------------------------------------------------|
| `customers`        | One row per customer with `customer_id`, `country`              |
| `products`         | One row per product with `stock_code`, `description`, `unit_price` |
| `invoices`         | One row per transaction with `invoice_no`, `invoice_date`, `customer_id` |
| `invoice_items`    | One row per product line per invoice, including `quantity`, `unit_price`, `line_revenue` |

These tables were loaded from cleaned CSVs into the MySQL `retail_sales` database during setup.

---

### 🧭 Entity Relationship Diagram

![ERD – Online Retail II](images/online_retail_ii_erd.png)

The ERD shows the structure of the normalized relational database, highlighting the primary and foreign key relationships among the four main tables.

---

## 🔍 Summary of Business Questions

| #   | Focus Area                        | Description                                   |
|-----|----------------------------------|-----------------------------------------------|
| Q1  | Monthly Sales Trend              | Revenue, invoice count, and AOV per month     |
| Q2  | Product Performance              | Top 10 products by revenue and quantity       |
| Q3  | High-Value Invoices              | Top 10 invoices by total revenue              |
| Q4a | Revenue by Country (All)         | Revenue breakdown including the UK            |
| Q4b | Revenue by Country (Excl. UK)    | Revenue breakdown excluding the UK            |
| Q5  | Customer Behavior by Country     | Invoices and revenue per customer by country  |
| Q6  | One-Time vs Repeat Customers     | Customer classification by invoice count      |
| Q7  | AOV per Customer                 | Top 10 by average order value                 |
| Q8  | Total Spend per Customer         | Top 10 by total amount spent                  |
| Q9  | Recency Metric                   | Days since each customer's last purchase      |
| Q10 | Purchase Frequency               | Total orders placed by each customer          |
| Q11 | Monetary Value                   | Lifetime spend per customer                   |
| Q12 | RFM Base Table                   | Recency, Frequency, and Monetary values       |

---

## 📊 Business Insights Summary

**Q1. Monthly Revenue Trend**  
- Revenue peaked in **November** of both 2010 and 2011, confirming a **pre-holiday sales surge**.
- Notably lower revenue in **January–February** each year, consistent with a **post-holiday dip**.
- **December 2011** shows lower revenue due to partial data (up to Dec 9 only).

**Q2. Top Products by Revenue**  
- **"Regency Cakestand 3 Tier"** and **"White Hanging Heart T-Light Holder"** were top earners.
- Successful products include both **high-margin low-volume** and **low-margin high-volume** items.

**Q3. High-Value Invoices**  
- Top invoices ranged from **£22K to over £168K**, often tied to large single-item purchases.
- Several customers appear multiple times, suggesting high-spend loyal buyers.

**Q4a–b. Revenue by Country**  
- The **UK dominates** total revenue, as expected.
- Excluding the UK, **Ireland**, **Netherlands**, and **Germany** led in international sales.

**Q5. Customer Behavior by Country**  
- **UK** customers averaged 6+ orders and nearly £2.7K in spend per customer.
- Countries like **Netherlands** and **Ireland** showed high per-customer revenue, though Ireland had very few customers.

**Q6. Repeat vs. One-Time Buyers**  
- Around **72%** of customers made repeat purchases, indicating strong engagement.
- The remaining **28%** were one-time buyers, suggesting opportunities for retention campaigns.

**Q7. Highest Average Order Value (AOV)**  
- Some customers had **AOVs exceeding £80K**, mostly from 1–2 large orders.
- These high-AOV buyers may be **B2B clients or bulk purchasers**.

**Q8. Top Customers by Lifetime Spend**  
- Top customer spent over **£580K across 145 orders**.
- Others reached **£300K–£500K**, often with moderate order volumes — prime loyalty candidates.

**Q9. Customer Recency**
- The SQL output provides each customer's most recent purchase date and recency (in days) as of **2011-12-09**.
- These metrics form the foundation for evaluating **customer engagement and dormancy**.
- Further insights, including distribution analysis and visualizations, were conducted in the Python notebook `3_cohort_analysis_sales_performance.ipynb`.

**Q10. Customer Frequency**
- The SQL query returns the number of **unique orders per customer**, along with total and average revenue per order.
- This data helps identify both **one-time buyers** and **high-frequency customers**.
- Frequency distributions, outlier detection, and supporting visualizations were created in the Python analysis environment.

**Q11. Customer Monetary Value**
- This output computes each customer’s **total spend**, **number of orders**, and **average order value**.
- The resulting data supports **CLV estimation** and customer segmentation.
- Deeper statistical exploration of monetary patterns was performed in the Python notebook, using frequency tables, histograms, and boxplots.

**Q12. RFM Input Metrics (Raw Output Only)**
- The SQL output includes raw fields needed for RFM segmentation:
  - `last_purchase`
  - `frequency`
  - `monetary`
  - `recency`
- These were not scored or segmented in SQL.
- **RFM scoring and customer segmentation were completed in the Python notebook**, where logic, thresholds, and labels were applied.

---

## 📁 Output Files

All output files were exported from MySQL Workbench and saved to:  
`sql_outputs/mysql_outputs/`

```
├── 01_monthly_revenue_trend.csv
├── 02_top_products_by_revenue.csv
├── 03_top_invoices_by_value.csv
├── 04_revenue_by_country.csv
├── 04_revenue_by_country_excl_uk.csv
├── 05_customer_behavior_by_country.csv
├── 06_one_time_vs_repeat_customers.csv
├── 07_avg_order_value_per_customer.csv
├── 08_top_customers_by_total_spend.csv
├── 09_customer_recency.csv
├── 10_customer_frequency.csv
├── 11_customer_monetary_value.csv
└── 12_rfm_segmented_customers.csv
```

---

## 🛠️ Tools Used

- **SQL Engine:** MySQL 8.0  
- **Client:** MySQL Workbench CE  
- **Exports:** Manual export to CSV from Workbench  
- **Environment:** Local machine

---

## 🛡️ License & Attribution

© 2024 Ginosca Alejandro Dávila  
Bootcamp: Data Science and Machine Learning, Ironhack Puerto Rico  
Project: Online Retail II – Sales Analysis & Customer Segmentation  
Date: December 20, 2024  
This report and SQL script are released under the MIT License for portfolio and educational purposes.