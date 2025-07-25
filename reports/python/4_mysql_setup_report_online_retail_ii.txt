# 🛠️ 4. MySQL Environment Setup Report – Online Retail II
  
**Notebook:** `mysql_real_env_setup_online_retail_ii.ipynb`
**Notebook Location:** `notebooks/mysql_real_env_setup_online_retail_ii.ipynb`
**Script:** `mysql_real_env_setup_online_retail_ii.py`
**Script Locations:** 
- Annotated: `scripts/annotated/mysql_real_env_setup_online_retail_ii.py`  
- Clean: `scripts/clean/mysql_real_env_setup_online_retail_ii.py`    
**Environment:** Google Colab (Jupyter Notebook-based)  
**Project:** Online Retail II – Sales Analysis & Customer Segmentation  
**Bootcamp:** Data Science and Machine Learning
**School:** Ironhack Puerto Rico  
**Author:** Ginosca Alejandro Dávila 
**Date:** December 20, 2024  

---

## 📌 Overview

This script automates the setup of a **real MySQL database environment** for SQL-based retail analytics.  
It uses the cleaned outputs from the first notebook:

> 📓 `1_data_cleaning_online_retail_ii.ipynb` – responsible for cleaning and exporting the normalized relational CSVs.

The goal is to create and populate a normalized relational database that can be queried using any SQL client (e.g., MySQL Workbench, DBeaver).

---

## 🧱 Setup Workflow

The script performs the following steps:

1. 🔎 Validates presence of cleaned `.csv` files in `cleaned_data/`
2. 🔐 Loads MySQL credentials from a `.env` file (or prompts if missing)
3. 🔌 Connects to the MySQL server using `mysql-connector-python`
4. 🧱 Creates the `retail_sales` database and schema with 4 normalized tables
5. 📥 Inserts cleaned data into each table using `pandas` and `executemany()`
6. 🔍 Validates record counts in all tables
7. 🧪 Runs referential integrity checks (foreign keys, unused customers/products)

---

## 🗃️ Database Schema Created

The `retail_sales` schema includes four interrelated tables:

| Table           | Description                              |
|----------------|------------------------------------------|
| `customers`     | Customer ID and country                  |
| `products`      | Product code, description, unit price    |
| `invoices`      | Invoice number, date, customer reference |
| `invoice_items` | Line-level quantity, price, and revenue  |

All foreign key constraints are explicitly defined and enforced.

---

### 🧭 Entity Relationship Diagram

![ERD – Online Retail II](images/online_retail_ii_erd.png)

The ERD illustrates the structure of the `retail_sales` database and its relationships between tables.

---

## 📊 Inserted Row Counts

After loading, the following number of rows were confirmed in each table:

- `customers` → 5,852 rows  
- `products` → 4,624 rows  
- `invoices` → 36,607 rows  
- `invoice_items` → 766,226 rows  

✅ These values match the cleaned CSVs produced by `1_data_cleaning_online_retail_ii.ipynb`.

---

## ✅ Referential Integrity Results

All referential and business logic checks passed:

- 🧩 No orphaned `invoice_items`
- 🧾 All invoices reference valid customers
- 📪 Every invoice has line items
- 👥 No customers without invoices
- 📦 No unsold products

The schema is structurally sound and ready for SQL querying.

---

## 🎯 Final Status

The `retail_sales` MySQL database has been **successfully initialized and validated**.

It is now ready to be explored and queried using tools such as:
- **MySQL Workbench**
- **DBeaver**
- Any other MySQL-compatible client

This script acts as a **reproducible deployment tool** for setting up a clean local MySQL environment from the cleaned dataset.

---

## 🛡️ License & Attribution

© 2024 Ginosca Alejandro Dávila  
Bootcamp: Data Science and Machine Learning, Ironhack Puerto Rico  
Project: Online Retail II – Sales Analysis & Customer Segmentation  
Date: December 20, 2024  
This report and associated scripts are released under the MIT License for portfolio and educational purposes.