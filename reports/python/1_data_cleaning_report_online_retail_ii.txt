# 🧼 1. Data Cleaning Report – Online Retail II
  
**Notebook:** `1_data_cleaning_online_retail_ii.ipynb`  
**Notebook Location:** `notebooks/1_data_cleaning_online_retail_ii.ipynb`  
**Script:** `1_data_cleaning_online_retail_ii.py`  
**Script Locations:** 
- Annotated: `scripts/annotated/1_data_cleaning_online_retail_ii.py`  
- Clean: `scripts/clean/1_data_cleaning_online_retail_ii.py`  
**Dataset:** `online_retail_II.xlsx` (2009–2010 and 2010–2011)  
**Environment:** Google Colab (Jupyter Notebook-based)  
**Project:** Online Retail II – Sales Analysis & Customer Segmentation
**Bootcamp:** Data Science and Machine Learning
**School:** Ironhack Puerto Rico  
**Author:** Ginosca Alejandro Dávila  
**Date:** December 20, 2024

---

## 🧾 Overview

This script loads and cleans the Online Retail II dataset to prepare it for exploratory data analysis and SQL-based segmentation. The process includes merging data from two years, resolving inconsistencies, normalizing identifiers, deduplicating records, and exporting clean files.

---

## 🔢 Column Renaming & Classification

- Renamed columns to `snake_case` for consistency  
- Classified variables as:
  - **Quantitative:** `quantity`, `unit_price`
  - **Categorical:** `description`, `country`
  - **Datetime:** `invoice_date`
  - **Identifiers:** `invoice_no`, `stock_code`, `customer_id`

---

## 🧹 Cleaning Steps

### ✅ Filtering

Removed rows with:
- Negative or zero `quantity` or `unit_price`
- Canceled transactions (identified by `invoice_no` starting with `'C'`)
- Missing `customer_id` or `description`

### ✅ Type Conversions

Converted identifiers for consistency and compatibility:
- `invoice_no`, `stock_code` → string (`object`)
- `customer_id` → integer

### ✅ Categorical Standardization

- Lowercased and stripped whitespace from `description` and `country`

### ✅ Line Revenue Calculation

- Added `line_revenue = quantity × unit_price`

---

## 🧾 Deduplication & Standardization

- Removed 23K+ fully duplicated rows
- Standardized `description` using most frequent value per `stock_code`
- Aggregated repeated `(invoice_no, stock_code)` pairs by summing `quantity` and `line_revenue`

---

## 🔗 Identifier Integrity Checks

- Verified and enforced:
  - One `country` per `customer_id` (used mode)
  - One `description` per `stock_code`
  - One `invoice_date` and `customer_id` per `invoice_no` (used earliest)

---

## 📦 Output Files

Saved under `cleaned_data/`:

| Filename                       | Description                                               |
|--------------------------------|-----------------------------------------------------------|
| `cleaned_online_retail_II.csv` | Full cleaned dataset (flat structure)                     |
| `customers.csv`                | Unique customers with `customer_id`, `country`            |
| `products.csv`                 | Unique products with `stock_code`, `description`, `unit_price` |
| `invoices.csv`                 | Unique invoices with `invoice_no`, `invoice_date`, `customer_id` |
| `invoice_items.csv`            | One row per invoice-product line with revenue and quantity |

---

## 🧩 Relational Schema Overview

The cleaned dataset was transformed into a 4-table relational model:

- `customers`: `customer_id`, `country`
- `products`: `stock_code`, `description`, `unit_price`
- `invoices`: `invoice_no`, `invoice_date`, `customer_id`
- `invoice_items`: `invoice_no`, `stock_code`, `quantity`, `unit_price`, `line_revenue`

![Relational Schema](../images/online_retail_ii_erd.png)

---

## 📉 Cleaning Impact Summary

| Cleaning Step                         | Rows Removed | Remaining Rows |
|--------------------------------------|--------------|----------------|
| Initial merge                        | —            | 1,067,371      |
| Invalid quantity/price               | 25,700       | 1,041,671      |
| Canceled transactions                | 1            | 1,041,670      |
| Missing `customer_id`                | 236,121      | 805,549        |
| Non-product stock codes              | 2,816        | 802,733        |
| Fully duplicated rows                | 23,308       | 779,425        |

---

## 🔍 Final Dataset Summary

- **Final row count:** 779,425  
- **Distinct customers:** 5,922  
- **Distinct products:** 4,065  
- **Distinct invoices:** 27,933  
- **Time range:** Dec 1, 2009 – Dec 9, 2011

---

## 💡 Notes on SQL Compatibility

- Identifiers (`invoice_no`, `stock_code`, `customer_id`) are formatted for SQL integrity
- All column names are lowercase and use `snake_case`
- Data types compatible with MySQL primary/foreign key constraints
- Ready for import via Python scripts or `LOAD DATA INFILE`

---

## ✅ Ready for Analysis

- 📊 EDA (Python)
- 💻 SQL querying
- 🧠 RFM segmentation
- 📈 Dashboard development (Tableau or similar)

---

## 🛠️ Tools Used

- **Python:** `pandas`, `numpy`, `os`, `io`
- **Environments:** Google Colab & local execution compatible
- **Export:** Overwrite-protected CSVs with versioning compatibility

---

## 🛡️ License & Attribution

© 2024 Ginosca Alejandro Dávila  
Bootcamp: Data Science and Machine Learning, Ironhack Puerto Rico  
Project: Online Retail II – Sales Analysis & Customer Segmentation  
Date: December 20, 2024  
This report and associated scripts are released under the MIT License for portfolio and educational purposes.
