-- -----------------------------------------------------------------------------
-- 📊 SQL Schema and Data Validation Script – Online Retail II
-- 📁 File: 1_validate_online_retail_ii.sql
-- 📅 Created: December 20, 2024
-- 👩‍💻 Author: Ginosca Alejandro Dávila
-- 🎓 Bootcamp: Ironhack Puerto Rico – Data Science and Machine Learning
-- 📦 Project: Online Retail II – Sales Analysis & Customer Segmentation
-- -----------------------------------------------------------------------------

-- ✅ Step 1: Show all available databases (confirm retail_sales exists)
SHOW DATABASES;

-- ✅ Step 2: Use the retail_sales database
USE retail_sales;

-- ✅ Step 3: List all tables in the schema
SHOW TABLES;

-- ✅ Step 4: Describe table structures
DESCRIBE customers;
DESCRIBE products;
DESCRIBE invoices;
DESCRIBE invoice_items;

-- ✅ Step 5: Check row counts in each table
SELECT 'customers' AS table_name, COUNT(*) AS `rows` FROM customers
UNION
SELECT 'products', COUNT(*) FROM products
UNION
SELECT 'invoices', COUNT(*) FROM invoices
UNION
SELECT 'invoice_items', COUNT(*) FROM invoice_items;

-- ✅ Step 6: Preview sample data
SELECT * FROM customers LIMIT 5;
SELECT * FROM products LIMIT 5;
SELECT * FROM invoices LIMIT 5;
SELECT * FROM invoice_items LIMIT 5;

-- ✅ Step 7: List foreign key constraints
SELECT 
    TABLE_NAME,
    CONSTRAINT_NAME,
    COLUMN_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'retail_sales'
  AND REFERENCED_TABLE_NAME IS NOT NULL;

-- =============================================================================
-- ✅ OPTIONAL DATA QUALITY CHECKS – READ-ONLY
-- =============================================================================

-- 🔍 Step 8: Count NULLs in critical fields
SELECT COUNT(*) AS null_countries FROM customers WHERE country IS NULL;
SELECT COUNT(*) AS null_unit_prices FROM products WHERE unit_price IS NULL;
SELECT COUNT(*) AS null_descriptions FROM products WHERE description IS NULL;
SELECT COUNT(*) AS null_customers FROM invoices WHERE customer_id IS NULL;
SELECT COUNT(*) AS null_invoice_dates FROM invoices WHERE invoice_date IS NULL;
SELECT COUNT(*) AS null_invoice_or_product FROM invoice_items WHERE invoice_no IS NULL OR stock_code IS NULL;
SELECT COUNT(*) AS null_quantity FROM invoice_items WHERE quantity IS NULL;
SELECT COUNT(*) AS null_unit_price FROM invoice_items WHERE unit_price IS NULL;
SELECT COUNT(*) AS null_line_revenue FROM invoice_items WHERE line_revenue IS NULL;

-- 🔍 Step 9: Check for duplicate primary keys or composite keys

-- ⚠️ Note:
-- During the data cleaning phase, full row duplicates were removed in Python using:
--     df_raw = df_raw.drop_duplicates()
-- Therefore, repeated (invoice_no, stock_code) pairs in `invoice_items`
-- reflect valid, distinct line items (e.g., same product added more than once in an invoice)
-- and should not be treated as redundant rows.

SELECT customer_id, COUNT(*) AS cnt FROM customers GROUP BY customer_id HAVING cnt > 1;
SELECT stock_code, COUNT(*) AS cnt FROM products GROUP BY stock_code HAVING cnt > 1;
SELECT invoice_no, COUNT(*) AS cnt FROM invoices GROUP BY invoice_no HAVING cnt > 1;
SELECT invoice_no, stock_code, COUNT(*) AS cnt
FROM invoice_items
GROUP BY invoice_no, stock_code
HAVING cnt > 1;

-- 🔍 Step 10: Check invoice date range (should be between 2009–2011)
SELECT 
    MIN(invoice_date) AS earliest_date,
    MAX(invoice_date) AS latest_date
FROM invoices;

-- 🔍 Step 11: Sanity checks on quantity, price, and revenue
SELECT * FROM invoice_items WHERE quantity <= 0;
SELECT * FROM invoice_items WHERE unit_price < 0;
SELECT * FROM invoice_items WHERE line_revenue < 0;
