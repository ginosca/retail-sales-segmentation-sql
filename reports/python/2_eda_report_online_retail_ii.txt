# 📊 2. EDA Report – Online Retail II

**Notebook:** `2_eda_online_retail_ii.ipynb`
**Notebook Location:** `notebooks/2_eda_online_retail_ii.ipynb`  
**Script:** `2_eda_online_retail_ii.py`
**Script Locations:** 
- Annotated: `scripts/annotated/2_eda_online_retail_ii.py`  
- Clean: `scripts/clean/2_eda_online_retail_ii.py`    
**Dataset:** `cleaned_online_retail_II.csv`  
**Environment:** Google Colab (Jupyter Notebook-based) 
**Project:** Online Retail II – Sales Analysis & Customer Segmentation
**Bootcamp:** Data Science and Machine Learning
**School:** Ironhack Puerto Rico
**Author:** Ginosca Alejandro Dávila  
**Date:** December 20, 2024

---

## 📋 Overview

This report summarizes the Exploratory Data Analysis (EDA) performed on the cleaned transactional dataset from the Online Retail II project.

The analysis focuses on identifying patterns in sales performance, customer behavior, and product trends, while preparing the foundation for segmentation and SQL-based analysis.

We use the cleaned flat file `cleaned_online_retail_II.csv`, exported in the previous notebook `1_data_cleaning_online_retail_ii.ipynb`.

---

## 🔍 Goals of the EDA

- Analyze sales trends over time (monthly revenue)
- Identify top-performing products and invoices
- Evaluate country-level sales and customer behavior
- Understand customer loyalty and segmentation potential
- Prepare outputs for RFM modeling and SQL validation

---

## 🧾 Input Data

| File | Description |
|------|-------------|
| `cleaned_online_retail_II.csv` | Full flat cleaned dataset used for EDA |

> 📌 Normalized relational tables (`customers.csv`, `products.csv`, `invoices.csv`, `invoice_items.csv`) are excluded from this notebook and used only in the SQL notebook.

---

## 🧪 Dataset Summary

- Rows: **766,226**
- Columns: **9**
- No missing values
- Flat transactional format (each row = 1 product sold in an invoice)
- `line_revenue` computed as `quantity * unit_price`

### Variable Classification

| Variable        | Type         |
|-----------------|--------------|
| `invoice_no`    | Identifier   |
| `stock_code`    | Identifier   |
| `customer_id`   | Identifier   |
| `description`   | Categorical  |
| `country`       | Categorical  |
| `quantity`      | Quantitative |
| `unit_price`    | Quantitative |
| `line_revenue`  | Quantitative |
| `invoice_date`  | Datetime     |

---

## 🗓️ Time Range

- **Start Date:** 2009-12-01  
- **End Date:** 2011-12-09  
- **Span:** 24 months across two retail years

---

## 🧠 Business Questions Answered

The EDA answers 12 key business questions, categorized below:

### 📈 Sales Performance
1. What is the monthly revenue trend from 2009 to 2011?  
2. What are the top 10 best-selling products by total revenue?  
3. Which invoices had the highest total transaction value?

### 🌍 Country & Regional Insights
4. Which countries generate the most revenue?  
5. Do customer behaviors differ by country?

### 👤 Customer Insights
6. How many customers made only one purchase?  
7. What is the average order value per customer?  
8. Who are the top 10 customers by total spend?

### 🧠 Customer Segmentation (RFM)
9. How recently has each customer made a purchase?  
10. How frequently has each customer purchased?  
11. How much revenue has each customer generated?  
12. How can we segment customers based on RFM scores?

---

## 📊 Quantitative Variable Summary

| Metric       | `quantity` | `unit_price` | `line_revenue` |
|--------------|------------|--------------|----------------|
| **Mean**     | 13.70      | £2.95        | £22.28         |
| **Median**   | 6          | £1.95        | £12.50         |
| **Max**      | 80,995     | £649.50      | £168,469.60    |
| **Std Dev**  | 147.33     | £4.35        | £227.46        |
| **Outliers** | Yes        | Yes          | Yes            |

All three quantitative variables were found to be **right-skewed** with **extreme outliers**, justifying the use of log transformations for better visualization and segmentation prep.

---

## 🧩 RFM Segmentation Summary

Customers were scored on:

- **Recency**: Days since last purchase (lower is better)
- **Frequency**: Number of unique orders
- **Monetary**: Total revenue contributed

Each metric was scored from **1 (low)** to **4 (high)** using **quartile-based ranking**. These were then **summed** into a final **RFM score** (R + F + M), ranging from **3 to 12**.

Based on the combined RFM score and specific rules, we assigned each customer to a segment:

| Segment       | Criteria                           | Description                              |
|---------------|------------------------------------|------------------------------------------|
| High-Value    | `RFM_Score >= 9`                   | Frequent, high-spending, recent buyers   |
| Loyal         | `R >= 3 and F >= 3`                | Engaged and recurring customers          |
| At-Risk       | `R == 1`                           | Long time since last purchase            |
| One-Time      | `F == 1 and M == 1`                | Only made one small purchase             |
| Other         | All others                         | Moderate behavior or mixed signals       |

---
## 📈 Key Insights

- 📅 **Monthly revenue consistently peaks in November**, driven by **holiday season demand**. November 2010 (£1.16M) and November 2011 (£1.14M) are top-performing months.
- 📉 A noticeable **post-holiday dip** occurs each January–February. December 2011 appears lower due to **partial data only up to Dec 9**, not an actual downturn.
- 📈 **Year-over-year growth:** 2011 consistently outperformed 2010 in total revenue — signaling healthy **business expansion**.
- 🔄 Revenue trends reflect **strong seasonal patterns**, ideal for guiding **inventory planning**, **staffing**, and **campaign timing**.

- 🛍️ **Top products** follow a **mixed strategy**:
  - Low-cost, high-volume items (e.g., *white hanging t-light holders*, *jumbo bags*) drive bulk sales.
  - Mid-priced decorative items (e.g., *regency cakestands*, *bird ornaments*) generate high total revenue.
  - 🔲 **High-margin, low-volume products** (e.g., furniture and lighting) also appear in top revenue lists — suggesting **premium product opportunities**.
- 📦 This dual dynamic supports a **hybrid product strategy**: emphasize popular giftware and explore premium category expansion.

- 🧾 **Top invoices** include extreme values like a **£168K single-item invoice** (likely B2B or anomalous). Repeat entries from customers like `18102` suggest **high-value loyalty accounts**.

- 🌍 **United Kingdom dominates**, contributing ~91% of all revenue. Yet, **Netherlands, Ireland, and Germany** show **high average spend per customer**, signaling **untapped premium markets**.
- 🌐 **Country-level segmentation** reveals:
  - Balanced markets (Germany, France) ideal for scaling operations.
  - High-value, low-volume markets (Switzerland, Denmark, Australia) suitable for **targeted B2B or luxury strategies**.
  - Ireland's outlier behavior likely results from a **test/demo account** or **internal use**, not typical customer patterns.
  - 📊 Visuals confirm UK’s dominance, but international regions still generate substantial value per transaction.

- 🔁 **Repeat customers make up 72%** of the user base — a strong indicator of **moderate retention**, while **28% are one-time buyers**, representing a key segment for **re-engagement campaigns**.
- 🧠 **Customer loyalty programs** may help convert one-time buyers and increase average purchase frequency over time.

- 💳 **Average Order Value (AOV)** distribution is highly **right-skewed**:
  - 99.8% of customers have AOV under £5,600.
  - 10 customers far exceed that, including one at **£84K/order** — likely wholesale or special events.
  - AOV helps identify **whales** versus **typical customers**, supporting tiered pricing or offer strategies.

- 💰 **Top-spending customers** like `18102` (lifetime spend >£580K) and `16446` (high spend with only 2 orders) reinforce a **Pareto distribution** — a small cohort generates a large share of revenue.
- 🧠 These top customers should be prioritized for **VIP loyalty programs**, **personalized retention**, or even **account-based marketing (ABM)** strategies.
- 📊 Revenue distribution confirms that **~20% of customers account for ~80% of revenue**, validating **Pareto principle application**.

- ⏱️ **Recency analysis** shows many users active in the last 100 days, but some haven’t purchased in **700+ days**, suggesting **churn** or **inactive segments**.
- 🔢 **Frequency distribution** shows most users placed **1–8 orders**, but power users made **100+ purchases**. This helps distinguish **occasional shoppers** from **core repeat buyers**.

- 💸 **Monetary value** is also highly skewed:
  - Most customers spent under **£20K**, but a handful exceeded **£100K–£500K+**.
  - These high-spend customers can distort mean values — emphasizing the need for **median-based strategies** and **outlier detection** in reporting.

- 🧩 **RFM segmentation** divides customers into 5 behavior-based groups:
  - **High-Value** (top spenders and frequent buyers) and **Loyal** users should receive premium offers and early access promotions.
  - **At-Risk** and **One-Time** users can be re-engaged via tailored messaging, reminders, or discounts.
  - **Other** customers may benefit from nurturing and behavioral analysis to determine optimal engagement paths.
- 📊 The RFM plot revealed a **diverse customer base**, supporting **tiered marketing** and **personalized outreach** strategies.

> These insights together form the foundation for a **targeted customer strategy**, informed **campaign planning**, and **international growth expansion** through behavioral, temporal, and value-based segmentation.


---

## 📁 Output Files Summary

```
eda_outputs/
├── plots/
│   ├── 01_quantity_distribution.png
│   ├── 02_unit_price_distribution.png
│   ├── 03_line_revenue_distribution.png
│   ├── 04_monthly_revenue_trend.png
│   ├── 05_top_products_revenue.png
│   ├── 06_top_invoices_by_value.png
│   ├── 07_country_revenue_bar_excl_uk.png
│   ├── 07_country_revenue_bar.png
│   ├── 08_country_avg_behavior_scatter.png
│   ├── 09_one_time_vs_repeat_customers.png
│   ├── 10_avg_order_value_distribution.png
│   ├── 11_top_customers_by_total_spend.png
│   ├── 12_customer_recency_distribution.png
│   ├── 13_customer_frequency_distribution.png
│   ├── 14_customer_monetary_value_distribution.png
│   └── 15_rfm_segment_distribution.png
└── data/
    ├── 01_monthly_revenue_trend.csv
    ├── 02_top_products_by_revenue.csv
    ├── 03_top_invoices_by_value.csv
    ├── 04_revenue_by_country_excl_uk.csv
    ├── 04_revenue_by_country.csv
    ├── 05_customer_behavior_by_country.csv
    ├── 06_one_time_vs_repeat_customers.csv
    ├── 07_avg_order_value_per_customer.csv
    ├── 08_top_customers_by_total_spend.csv
    ├── 09_customer_recency.csv
    ├── 10_customer_frequency.csv
    ├── 11_customer_monetary_value.csv
    └── 12_rfm_scores.csv
```

---

## 🛠️ Tools Used

- **Python:** `pandas`, `matplotlib`, `seaborn`, `plotly`, `os`
- **Environment:** Jupyter Notebook & Google Colab compatible
- **Exports:** Versioned plots and CSVs saved under `eda_outputs/`

---

## 🔭 Future Exploration

- Analyze customer retention cohorts and repeat behavior over time.
- Segment products into categories (e.g., lighting, decor, seasonal).
- Study basket size and product bundling behavior.
- Compare SQL vs Python results in upcoming analysis phases.

---

## 🛡️ License & Attribution

© 2024 Ginosca Alejandro Dávila  
Bootcamp: Data Science and Machine Learning, Ironhack Puerto Rico  
Project: Online Retail II – Sales Analysis & Customer Segmentation  
Date: December 20, 2024  
This report and associated scripts are released under the MIT License for portfolio and educational purposes.