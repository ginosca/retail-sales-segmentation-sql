-- -----------------------------------------------------------------------------
-- 📈 12 Business Questions – Online Retail II (MySQL)
-- 📁 File: 2_business_questions_online_retail_ii.sql
-- 📦 Based on: 3_sql_analysis_sales_performance_online_retail_ii.ipynb
-- 📅 Created: December 20, 2024
-- 👩‍💻 Author: Ginosca Alejandro Dávila
-- 🎓 Bootcamp: Ironhack Puerto Rico – Data Science and Machine Learning
-- 📦 Project: Online Retail II – Sales Analysis & Customer Segmentation
-- -----------------------------------------------------------------------------

USE retail_sales;

-- Q1: Monthly Revenue Trend
SELECT
    DATE_FORMAT(invoice_date, '%Y-%m') AS invoice_month,
    ROUND(SUM(line_revenue), 2) AS monthly_revenue,
    COUNT(DISTINCT invoice_no) AS monthly_invoices,
    ROUND(SUM(line_revenue) / COUNT(DISTINCT invoice_no), 2) AS avg_revenue_per_invoice
FROM invoices
JOIN invoice_items USING (invoice_no)
GROUP BY invoice_month
ORDER BY invoice_month;

-- Q2: Top 10 Products by Revenue
SELECT
    p.stock_code,
    p.description,
    ROUND(SUM(ii.line_revenue), 2) AS total_revenue,
    SUM(ii.quantity) AS total_quantity,
    ROUND(AVG(ii.unit_price), 2) AS avg_unit_price
FROM invoice_items AS ii
JOIN products AS p ON ii.stock_code = p.stock_code
GROUP BY p.stock_code, p.description
ORDER BY total_revenue DESC
LIMIT 10;

-- Q3: Top 10 Invoices by Transaction Value
SELECT
    ii.invoice_no,
    ROUND(SUM(ii.line_revenue), 2) AS total_invoice_revenue,
    COUNT(ii.stock_code) AS invoice_items,
    i.customer_id,
    i.invoice_date
FROM invoice_items AS ii
JOIN invoices AS i ON ii.invoice_no = i.invoice_no
GROUP BY ii.invoice_no, i.customer_id, i.invoice_date
ORDER BY total_invoice_revenue DESC
LIMIT 10;

-- Q4a: Revenue by Country (Including UK)
SELECT
    c.country,
    ROUND(SUM(ii.line_revenue), 2) AS total_revenue,
    COUNT(DISTINCT i.invoice_no) AS num_invoices,
    ROUND(SUM(ii.line_revenue) / COUNT(DISTINCT i.invoice_no), 2) AS avg_invoice_value
FROM invoice_items AS ii
JOIN invoices AS i ON ii.invoice_no = i.invoice_no
JOIN customers AS c ON i.customer_id = c.customer_id
GROUP BY c.country
ORDER BY total_revenue DESC;

-- Q4b: Revenue by Country (Excluding UK)
SELECT
    c.country,
    ROUND(SUM(ii.line_revenue), 2) AS total_revenue,
    COUNT(DISTINCT i.invoice_no) AS num_invoices,
    ROUND(SUM(ii.line_revenue) / COUNT(DISTINCT i.invoice_no), 2) AS avg_invoice_value
FROM invoice_items AS ii
JOIN invoices AS i ON ii.invoice_no = i.invoice_no
JOIN customers AS c ON i.customer_id = c.customer_id
WHERE LOWER(TRIM(c.country)) != 'united kingdom'
GROUP BY c.country
ORDER BY total_revenue DESC;

-- Q5: Customer Behavior by Country
SELECT
    c.country,
    COUNT(DISTINCT c.customer_id) AS num_customers,
    COUNT(DISTINCT i.invoice_no) AS num_invoices,
    ROUND(SUM(ii.line_revenue), 2) AS total_revenue,
    ROUND(COUNT(DISTINCT i.invoice_no) / COUNT(DISTINCT c.customer_id), 2) AS avg_invoices_per_customer,
    ROUND(SUM(ii.line_revenue) / COUNT(DISTINCT c.customer_id), 2) AS avg_revenue_per_customer
FROM invoice_items AS ii
JOIN invoices AS i USING (invoice_no)
JOIN customers AS c USING (customer_id)
GROUP BY c.country
ORDER BY total_revenue DESC;

-- Q6: One-Time vs. Repeat Customers
WITH invoice_counts AS (
    SELECT customer_id, COUNT(DISTINCT invoice_no) AS num_invoices
    FROM invoices
    GROUP BY customer_id
),
tagged_customers AS (
    SELECT
        CASE
            WHEN num_invoices = 1 THEN 'Single Purchase'
            ELSE 'Repeat Customer'
        END AS customer_type
    FROM invoice_counts
)
SELECT
    customer_type,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM tagged_customers), 2) AS percent
FROM tagged_customers
GROUP BY customer_type
ORDER BY customer_type DESC;

-- Q7: Top 10 Customers by Average Order Value
SELECT
    c.customer_id,
    ROUND(SUM(ii.line_revenue), 2) AS total_spent,
    COUNT(DISTINCT i.invoice_no) AS num_orders,
    ROUND(SUM(ii.line_revenue) / COUNT(DISTINCT i.invoice_no), 2) AS avg_order_value
FROM invoice_items AS ii
JOIN invoices AS i ON ii.invoice_no = i.invoice_no
JOIN customers AS c ON i.customer_id = c.customer_id
GROUP BY c.customer_id
ORDER BY avg_order_value DESC
LIMIT 10;

-- Q8: Top 10 Customers by Total Spend
SELECT
    c.customer_id,
    ROUND(SUM(ii.line_revenue), 2) AS total_spent,
    COUNT(DISTINCT i.invoice_no) AS num_orders,
    ROUND(SUM(ii.line_revenue) / COUNT(DISTINCT i.invoice_no), 2) AS avg_order_value
FROM invoice_items AS ii
JOIN invoices AS i ON ii.invoice_no = i.invoice_no
JOIN customers AS c ON i.customer_id = c.customer_id
GROUP BY c.customer_id
ORDER BY total_spent DESC
LIMIT 10;

-- Q9: Recency (Days Since Last Purchase)
SELECT
    c.customer_id,
    MAX(i.invoice_date) AS last_purchase_date,
    DATEDIFF('2011-12-09', MAX(i.invoice_date)) AS recency_days
FROM customers AS c
JOIN invoices AS i ON c.customer_id = i.customer_id
GROUP BY c.customer_id
ORDER BY recency_days ASC;

-- Q10: Purchase Frequency
SELECT
    c.customer_id,
    COUNT(DISTINCT i.invoice_no) AS num_orders,
    ROUND(SUM(ii.line_revenue), 2) AS total_spent,
    ROUND(SUM(ii.line_revenue) / COUNT(DISTINCT i.invoice_no), 2) AS avg_order_value
FROM customers AS c
JOIN invoices AS i ON c.customer_id = i.customer_id
JOIN invoice_items AS ii ON i.invoice_no = ii.invoice_no
GROUP BY c.customer_id
ORDER BY num_orders DESC;

-- Q11: Monetary Value per Customer
SELECT
    c.customer_id,
    ROUND(SUM(ii.line_revenue), 2) AS total_spent,
    COUNT(DISTINCT i.invoice_no) AS num_orders,
    ROUND(SUM(ii.line_revenue) / COUNT(DISTINCT i.invoice_no), 2) AS avg_order_value
FROM customers AS c
JOIN invoices AS i ON c.customer_id = i.customer_id
JOIN invoice_items AS ii ON i.invoice_no = ii.invoice_no
GROUP BY c.customer_id
ORDER BY total_spent DESC;

-- Q12: RFM Segmentation Base Table (Raw Values)
SELECT
    c.customer_id,
    MAX(i.invoice_date) AS last_purchase,
    COUNT(DISTINCT i.invoice_no) AS frequency,
    ROUND(SUM(ii.line_revenue), 2) AS monetary,
    DATEDIFF('2011-12-09', MAX(i.invoice_date)) AS recency
FROM customers AS c
JOIN invoices AS i ON c.customer_id = i.customer_id
JOIN invoice_items AS ii ON i.invoice_no = ii.invoice_no
GROUP BY c.customer_id
ORDER BY monetary DESC;