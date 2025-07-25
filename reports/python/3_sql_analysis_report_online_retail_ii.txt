# 🧮 3. SQL Analysis Report – Online Retail II

**Notebook:** `3_sql_analysis_sales_performance.ipynb`
**Notebook Location:** `notebooks/3_sql_analysis_sales_performance.ipynb`  
**Script:** `3_sql_analysis_sales_performance.py`
**Script Locations:** 
- Annotated: `scripts/annotated/3_sql_analysis_sales_performance.py`  
- Clean: `scripts/clean/3_sql_analysis_sales_performance.py`    
**Environment:** Google Colab (Jupyter Notebook-based) 
**Project:** Online Retail II – Sales Analysis & Customer Segmentation    
**Bootcamp:** Data Science and Machine Learning
**School:** Ironhack Puerto Rico
**Author:** Ginosca Alejandro Dávila 
**Date:** December 20, 2024  

---

## 🧾 Overview

This SQL-driven analysis builds on the relational structure created during data cleaning, querying four normalized tables (`customers`, `products`, `invoices`, `invoice_items`) to answer 12 key business questions.

We used **SQL joins, window functions, aggregations, and conditional logic** to analyze:

- Revenue trends and product performance  
- Country-specific sales insights  
- Customer loyalty and purchase behavior  
- RFM segmentation for marketing strategy

---

## 🗂️ Input Tables

| Table              | Description                                     |
|-------------------|-------------------------------------------------|
| `customers.csv`    | One row per customer with `customer_id`, `country` |
| `products.csv`     | One row per product with `stock_code`, `description`, `unit_price` |
| `invoices.csv`     | One row per transaction with `invoice_no`, `invoice_date`, `customer_id` |
| `invoice_items.csv`| One row per product line in each invoice, including `quantity` and `line_revenue` |

These tables were loaded into an in-memory **SQLite** database to perform SQL queries directly from Python.

---

### 🧭 Entity Relationship Diagram

![ERD – Online Retail II](images/online_retail_ii_erd.png)

The ERD illustrates the structure of the `retail_sales` database and its relationships between tables.

---

## 📊 Business Questions & Insights

### 📈 Sales Performance

**Q1. Monthly Revenue Trend**  
- Revenue follows a clear seasonal pattern: **peaks in November**, drops in January–February.  
- December 2011 shows lower revenue because the dataset ends on **Dec 9, 2011**.  
- SQL aggregates closely matched EDA output.  
📁 `01_monthly_revenue_trend.csv`

**Q2. Top Products by Revenue**  
- Top-selling items include:  
  - `REGENCY CAKESTAND 3 TIER` (£277K)  
  - `WHITE HANGING HEART T-LIGHT HOLDER` (91K units sold)  
- High-revenue items were either **premium or high-volume decorative goods**.  
📁 `02_top_products_by_revenue.csv`

**Q3. Highest-Value Invoices**  
- Invoice `581483` totaled **£168K** from a single item — likely a bulk or anomalous transaction.  
- Some customers placed **>100 items in a single invoice**.  
📁 `03_top_invoices_by_value.csv`

---

### 🌍 Country & Regional Insights

**Q4. Revenue by Country**  
- 🇬🇧 **UK** accounts for **~90% of all revenue**.  
- Excluding UK, **Ireland** and **Netherlands** lead in revenue.  
- Netherlands had the **highest average invoice value** (~£2.5K).  
📁  
- `04_revenue_by_country.csv`  
- `04_revenue_by_country_excl_uk.csv`

**Q5. Customer Behavior by Country**  
- UK customers are balanced (avg. 6.2 orders, £2.7K revenue).  
- Ireland (3 customers) showed **very high spend per user** — an outlier.  
- Netherlands, Germany, France show consistent engagement.  
📁 `05_customer_behavior_by_country.csv`

---

### 👥 Customer Behavior

**Q6. One-Time vs. Repeat Buyers**  
- **27.65%** of customers purchased **only once**.  
- **72.35%** made multiple purchases — a strong indicator of loyalty.  
📁 `06_one_time_vs_repeat_customers.csv`

**Q7. Average Order Value per Customer**  
- Top customers (e.g., ID `16446`) placed only 2 orders but had **AOVs over £84K**.  
- Most high-AOV customers had **few, large purchases**.  
📁 `07_avg_order_value_per_customer.csv`

**Q8. Top Customers by Total Spend**  
- Customer `18102` spent **£580K** across **145 orders** — top LTV.  
- Others had high total spend with lower order frequency.  
📁 `08_top_customers_by_total_spend.csv`

---

### 🧠 Customer Segmentation (RFM)

**Q9. Recency (days since last order)**  
- Most recent buyers: `recency = 0`  
- Long tail includes dormant users with `recency > 300 days`  
📁 `09_customer_recency.csv`

**Q10. Frequency (purchase count)**  
- Most customers placed **1–8 orders**  
- A few power users had **100–373 orders**  
📁 `10_customer_frequency.csv`

**Q11. Monetary (total spend)**  
- ~75% of customers spent **under £20K**  
- Top customers were heavy outliers — some over **£500K**  
📁 `11_customer_monetary_value.csv`

**Q12. RFM Segmentation**  
- Segment breakdown:  
  - 🟡 **High-Value**: 1,248 customers  
  - 🟢 **Loyal**: 726 customers  
  - 🔴 **At-Risk**: 1,218 customers  
  - 🔵 **One-Time**: 1,608 customers  
  - ⚪ **Other**: Remaining segment  
📁 `12_rfm_segmented_customers.csv`

---

## 📁 Output Files Summary

All output saved under: `sql_outputs/notebook_outputs/`

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

## 💼 Business Recommendations

1. **Prioritize High-Value Segments**  
   Offer tailored experiences to top spenders (AOV > £5K, 100+ orders), such as early access or exclusive product lines.

2. **Re-engage At-Risk and One-Time Customers**  
   Use reactivation campaigns for 27% one-time buyers and customers inactive for >6 months.

3. **Leverage Holiday Peaks**  
   Reinforce marketing before November — the most profitable month in both 2010 and 2011.

4. **Country-Specific Strategies**  
   - **Ireland/Netherlands**: Target for premium or bulk sales  
   - **Germany/France**: Strengthen retention for loyal customer base  
   - **Australia/Switzerland**: Small base, high per-order value — test high-end offers

5. **Expand High-Performing SKUs**  
   Restock, bundle, or promote best-sellers like *Cakestands* and *T-Light Holders*.

6. **Use RFM Segments in Email & Ads**  
   - 🟢 Loyal: Encourage cross-sell  
   - 🟡 High-Value: Maintain premium service  
   - 🔴 At-Risk: Send “We miss you” campaigns  
   - 🔵 One-Time: Offer discounts or onboarding guides

---

## 🛠️ Tools Used

- **Languages:** Python, SQL (SQLite via SQLAlchemy)  
- **Libraries:** `pandas`, `matplotlib`, `seaborn`, `sqlalchemy`, `os`  
- **Environment:** Jupyter Notebook & Google Colab  
- **Exports:** CSVs saved to `sql_outputs/notebook_outputs/`

---

## 🛡️ License & Attribution

© 2024 Ginosca Alejandro Dávila  
Bootcamp: Data Science and Machine Learning, Ironhack Puerto Rico  
Project: Online Retail II – Sales Analysis & Customer Segmentation  
Date: December 20, 2024  
This report and associated scripts are released under the MIT License for portfolio and educational purposes.