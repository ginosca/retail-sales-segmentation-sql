# 🧾 SQL Validation Report – Online Retail II

**Author:** Ginosca Alejandro Dávila  
**Date:** June 2, 2025  
**Script:** `1_validate_online_retail_ii.sql`  
**Script Location:** `sql/scripts/1_validate_online_retail_ii.sql`  
**Database:** `retail_sales`  
**Environment:** MySQL Workbench 8.0 CE  
**Project:** Online Retail II – Sales Analysis & Customer Segmentation

---

## ✅ Summary

This report documents schema validation, data quality checks, and integrity assessments for the `retail_sales` MySQL database. All core tables (`customers`, `products`, `invoices`, `invoice_items`) were reviewed to ensure structural soundness and data cleanliness before beginning business analysis.

---

## 📋 Step-by-Step Results

### 1. Confirmed Database Presence
- `retail_sales` database found among existing databases.

### 2. Table Overview
Tables in schema:
- `customers`
- `products`
- `invoices`
- `invoice_items`

### 3. Table Structures

All tables were described to verify column types, primary keys, and foreign key candidates.

### 4. Row Counts
| Table          | Row Count |
|----------------|-----------|
| customers      | 5,852     |
| products       | 4,624     |
| invoices       | 36,607    |
| invoice_items  | 776,609   |

### 5. Sample Data Previewed
- `SELECT * FROM ... LIMIT 5` used for all tables.
- Confirmed expected structure and sample content.

### 6. Foreign Key Constraints
Verified via `INFORMATION_SCHEMA.KEY_COLUMN_USAGE`:

| Table         | Column        | References        |
|---------------|---------------|-------------------|
| invoices      | customer_id   | customers         |
| invoice_items | invoice_no    | invoices          |
| invoice_items | stock_code    | products          |

### 7. NULL Value Checks

All critical fields returned **0 NULLs**.

- ✅ `customers.country` – 0
- ✅ `products.unit_price` – 0
- ✅ `products.description` – 0
- ✅ `invoices.customer_id` – 0
- ✅ `invoices.invoice_date` – 0
- ✅ `invoice_items.invoice_no / stock_code / quantity / unit_price / line_revenue` – 0

### 8. Duplicate Key Checks

- No duplicates found in:
  - `customer_id`
  - `stock_code`
  - `invoice_no`

- **Note on `invoice_items`:**
  - Found repeated combinations of `(invoice_no, stock_code)` with differing quantities or revenue.
  - These are **valid** since full row duplicates were removed in the Python data cleaning phase.
  - Comment added in SQL script to document this logic.

### 9. Invoice Date Range
- `MIN(invoice_date)`: **2009-12-01**
- `MAX(invoice_date)`: **2011-12-09**

Confirmed expected 2-year window.

### 10. Sanity Checks

- ✅ No `quantity <= 0`
- ✅ No `unit_price < 0`
- ✅ No `line_revenue < 0`

### 11. Cleanup Section

- Cleanup queries for potential trailing NULL rows were prepared but **not executed** since no NULL-only records were found.

---

## 🟢 Conclusion

The MySQL version of the Online Retail II dataset passed all schema and data validation checks. The database is ready for SQL-based business analysis, starting with sales performance metrics.

---

## 📁 Script Reference

All validation queries are documented in:  
`sql/scripts/1_validate_online_retail_ii.sql`

---

## 🛡️ License & Attribution

© 2024 Ginosca Alejandro Dávila  
Bootcamp: Data Science and Machine Learning, Ironhack Puerto Rico  
Project: Online Retail II – Sales Analysis & Customer Segmentation  
Date: December 20, 2024  
This report and SQL script are released under the MIT License for portfolio and educational purposes.