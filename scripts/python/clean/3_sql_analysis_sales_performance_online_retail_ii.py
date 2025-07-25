# 🧮 SQL-Based Sales Analysis Script – Online Retail II
# 📓 Source Notebook: 3_sql_analysis_sales_performance_online_retail_ii.ipynb
# 🧠 Description: Answers business questions using SQL on normalized retail tables.
# 🏫 School: Ironhack Puerto Rico
# 🎓 Bootcamp: Data Science and Machine Learning
# 📅 Date: December 20, 2024
# 👩‍💻 Author: Ginosca Alejandro Dávila

#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import os

# ✅ Safe print to avoid encoding issues in some terminals
def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="ignore").decode())

# ✅ Check if running inside Google Colab
def is_colab():
    return 'google.colab' in sys.modules

# ✅ Helper to find local project root based on known folders
def find_project_root(start_dir, target_subdirs=('cleaned_data', 'notebooks'), max_depth=5):
    """Search upward for a directory containing known project subfolders"""
    current = start_dir
    for _ in range(max_depth):
        if all(os.path.exists(os.path.join(current, sub)) for sub in target_subdirs):
            return current
        parent = os.path.abspath(os.path.join(current, '..'))
        if parent == current:
            break
        current = parent
    raise FileNotFoundError("❌ Could not find project root with expected structure.")

# 🔧 Set base path depending on environment
if is_colab():
    from google.colab import drive
    drive.mount('/content/drive')

    default_path = 'MyDrive/Colab Notebooks/Ironhack/Week 3/Week 3 - Day 4/project-2-eda-sql/retail-sales-segmentation-sql'
    full_default_path = os.path.join('/content/drive', default_path)

    if os.path.exists(full_default_path):
        project_base_path = full_default_path
        safe_print(f"✅ Colab project path set to: {project_base_path}")
    else:
        safe_print("\n📂 Default path not found. Please input the relative path to your project inside Google Drive.")
        safe_print("👉 Example: 'MyDrive/Colab Notebooks/Ironhack/Week 3/Week 3 - Day 4/project-2-eda-sql/retail-sales-segmentation-sql'")
        user_path = input("📥 Your path: ").strip()
        project_base_path = os.path.join('/content/drive', user_path)

        if not os.path.exists(project_base_path):
            raise FileNotFoundError(f"❌ Path does not exist: {project_base_path}\nPlease check your input.")

        safe_print(f"✅ Colab project path set to: {project_base_path}")

else:
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        script_dir = os.getcwd()

    try:
        project_base_path = find_project_root(script_dir)
        safe_print(f"✅ Local environment detected. Base path set to: {project_base_path}")
    except FileNotFoundError as e:
        safe_print(str(e))
        raise

# 📁 Path to cleaned relational data
cleaned_data_path = os.path.join(project_base_path, 'cleaned_data')

# ✅ List of expected files for validation
expected_files = [
    'customers.csv',
    'products.csv',
    'invoices.csv',
    'invoice_items.csv'
]

# 📂 Check for the presence of all expected CSV files
missing_files = []
for file in expected_files:
    full_path = os.path.join(cleaned_data_path, file)
    if not os.path.exists(full_path):
        missing_files.append(file)

# 🧾 Display results
if not missing_files:
    safe_print(f"✅ All cleaned data files found in: {cleaned_data_path}")
else:
    safe_print("❌ Missing files:")
    for mf in missing_files:
        safe_print(f" - {mf}")


# In[ ]:


# 📦 Import core libraries
import pandas as pd
import os

# 📁 Define paths to relational tables
clean_path = os.path.join(project_base_path, 'cleaned_data')
customers_path = os.path.join(clean_path, 'customers.csv')
products_path = os.path.join(clean_path, 'products.csv')
invoices_path = os.path.join(clean_path, 'invoices.csv')
invoice_items_path = os.path.join(clean_path, 'invoice_items.csv')

# 📥 Load the relational datasets with error handling
try:
    customers_df = pd.read_csv(customers_path)
    products_df = pd.read_csv(products_path)
    invoices_df = pd.read_csv(invoices_path, parse_dates=['invoice_date'])
    invoice_items_df = pd.read_csv(invoice_items_path)

    safe_print("✅ All normalized relational tables loaded successfully.")
    safe_print(f"📄 customers.csv → {customers_df.shape}")
    safe_print(f"📄 products.csv → {products_df.shape}")
    safe_print(f"📄 invoices.csv → {invoices_df.shape}")
    safe_print(f"📄 invoice_items.csv → {invoice_items_df.shape}")

except FileNotFoundError as e:
    safe_print(f"❌ File not found: {e}")
    raise

except Exception as e:
    safe_print("❌ An unexpected error occurred while loading relational datasets.")
    raise


# In[ ]:


import io

# ✅ Display fallback for scripts
try:
    display
except NameError:
    def display(x):
        print(x.to_string() if isinstance(x, pd.DataFrame) else str(x))

# 🔍 Helper to inspect basic structure
def preview_table(df, name="Table", preview_rows=5):
    safe_print(f"📄 Previewing: {name}")
    safe_print("=" * 50)
    safe_print(f"🔹 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    safe_print("🔹 Column Names:")
    safe_print(df.columns.tolist())

    safe_print(f"\n🔹 First {preview_rows} rows:")
    display(df.head(preview_rows))

    safe_print("\n🔹 Data Types and Non-Null Counts:")
    buffer = io.StringIO()
    df.info(buf=buffer)
    safe_print(buffer.getvalue())
    safe_print("=" * 50 + "\n")

# 🔁 Preview each table
preview_table(customers_df, name="customers.csv")
preview_table(products_df, name="products.csv")
preview_table(invoices_df, name="invoices.csv")
preview_table(invoice_items_df, name="invoice_items.csv")


# In[ ]:


import sqlite3
from sqlalchemy import create_engine

# ✅ Create SQLite in-memory database
engine = create_engine('sqlite://', echo=False)

# 🗃️ Load DataFrames into SQL tables
try:
    customers_df.to_sql('customers', con=engine, index=False, if_exists='replace')
    products_df.to_sql('products', con=engine, index=False, if_exists='replace')
    invoices_df.to_sql('invoices', con=engine, index=False, if_exists='replace')
    invoice_items_df.to_sql('invoice_items', con=engine, index=False, if_exists='replace')
    safe_print("✅ All tables successfully loaded into SQLite in-memory database.")
except Exception as e:
    safe_print("❌ Error loading tables into SQLite:")
    safe_print(str(e))
    raise


# In[ ]:


import shutil
from IPython.display import Image, display

# ✅ Set path to ERD image inside project folder
drive_img_path = os.path.join(project_base_path, 'images', 'online_retail_ii_erd.png')

# ✅ In Colab: copy image to /content for rendering
if is_colab():
    colab_img_path = '/content/online_retail_ii_erd.png'

    if os.path.exists(drive_img_path):
        shutil.copyfile(drive_img_path, colab_img_path)
        safe_print("✅ ERD image copied to /content/")
    else:
        safe_print("❌ ERD image not found in Google Drive.")
else:
    colab_img_path = drive_img_path  # Use image directly in local/Jupyter

# 🖼️ Display the ERD image (in notebook environments)
try:
    display(Image(filename=colab_img_path))
except Exception as e:
    safe_print(f"❌ Could not display ERD image: {e}")


# In[ ]:


from sqlalchemy import text
import pandas as pd
import os

# 🔧 Setup export path
sql_output_dir = os.path.join(project_base_path, 'sql_outputs', 'notebook_outputs')
os.makedirs(sql_output_dir, exist_ok=True)

# 📝 SQL Query: Monthly revenue by month
monthly_revenue_query = text("""
SELECT
    strftime('%Y-%m', invoice_date) AS invoice_month,
    ROUND(SUM(line_revenue), 2) AS monthly_revenue,
    COUNT(DISTINCT invoice_no) AS monthly_invoices,
    ROUND(SUM(line_revenue) * 1.0 / COUNT(DISTINCT invoice_no), 2) AS avg_revenue_per_invoice
FROM invoices
JOIN invoice_items USING(invoice_no)
GROUP BY invoice_month
ORDER BY invoice_month;
""")

# 📊 Execute and load into DataFrame
monthly_revenue_df = pd.read_sql(monthly_revenue_query, con=engine)

# 👁️ Preview result
safe_print("📊 Monthly Revenue Trend:")
display(monthly_revenue_df)

# 💾 Save result to CSV
monthly_revenue_path = os.path.join(sql_output_dir, '01_monthly_revenue_trend.csv')
monthly_revenue_df.to_csv(monthly_revenue_path, index=False)
safe_print(f"✅ Saved: {monthly_revenue_path}")


# In[ ]:


# 📊 Q2: Top 10 Products by Revenue
query_top_products = """
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
"""

# 🚀 Execute query
top_products_df = pd.read_sql_query(query_top_products, engine)

# 📋 Display result
safe_print("📊 Top 10 Best-Selling Products by Revenue:")
display(top_products_df)

# 💾 Save output
top_products_path = os.path.join(project_base_path, 'sql_outputs', 'notebook_outputs', '02_top_products_by_revenue.csv')
top_products_df.to_csv(top_products_path, index=False)
safe_print(f"✅ Saved: {top_products_path}")


# In[ ]:


# 📊 Q3: Top 10 Invoices by Total Transaction Value
query_top_invoices = """
SELECT
    ii.invoice_no,
    ROUND(SUM(ii.line_revenue), 2) AS total_invoice_revenue,
    COUNT(ii.stock_code) AS invoice_items,
    c.customer_id,
    i.invoice_date
FROM invoice_items AS ii
JOIN invoices AS i ON ii.invoice_no = i.invoice_no
JOIN customers AS c ON i.customer_id = c.customer_id
GROUP BY ii.invoice_no, i.customer_id, i.invoice_date
ORDER BY total_invoice_revenue DESC
LIMIT 10;
"""

# 🚀 Execute query
top_invoices_df = pd.read_sql_query(query_top_invoices, engine)

# 📋 Display result
safe_print("📊 Top 10 Highest-Value Invoices:")
display(top_invoices_df)

# 💾 Save output
top_invoices_path = os.path.join(project_base_path, 'sql_outputs', 'notebook_outputs', '03_top_invoices_by_value.csv')
top_invoices_df.to_csv(top_invoices_path, index=False)
safe_print(f"✅ Saved: {top_invoices_path}")


# In[ ]:


# 📊 Q4a: Total Revenue by Country (Includes UK)
query_revenue_by_country = """
SELECT
    c.country,
    ROUND(SUM(ii.line_revenue), 2) AS total_revenue,
    COUNT(DISTINCT i.invoice_no) AS num_invoices,
    ROUND(SUM(ii.line_revenue) * 1.0 / COUNT(DISTINCT i.invoice_no), 2) AS avg_invoice_value
FROM invoice_items AS ii
JOIN invoices AS i ON ii.invoice_no = i.invoice_no
JOIN customers AS c ON i.customer_id = c.customer_id
GROUP BY c.country
ORDER BY total_revenue DESC;
"""

# 🚀 Execute query
revenue_by_country_df = pd.read_sql_query(query_revenue_by_country, engine)

# 📋 Display result
safe_print("📋 Top Countries by Total Revenue (Includes UK):")
display(revenue_by_country_df.head(10))

# 💾 Save output
revenue_country_path = os.path.join(project_base_path, 'sql_outputs', 'notebook_outputs', '04_revenue_by_country.csv')
revenue_by_country_df.to_csv(revenue_country_path, index=False)
safe_print(f"✅ Saved: {revenue_country_path}")

# 📊 Q4b: Total Revenue by Country (Excludes UK)
query_revenue_by_country_excl_uk = """
SELECT
    c.country,
    ROUND(SUM(ii.line_revenue), 2) AS total_revenue,
    COUNT(DISTINCT i.invoice_no) AS num_invoices,
    ROUND(SUM(ii.line_revenue) * 1.0 / COUNT(DISTINCT i.invoice_no), 2) AS avg_invoice_value
FROM invoice_items AS ii
JOIN invoices AS i ON ii.invoice_no = i.invoice_no
JOIN customers AS c ON i.customer_id = c.customer_id
WHERE TRIM(LOWER(c.country)) != 'united kingdom'
GROUP BY c.country
ORDER BY total_revenue DESC;
"""

# 🚀 Execute query
revenue_by_country_excl_uk_df = pd.read_sql_query(query_revenue_by_country_excl_uk, engine)

# 📋 Display result
safe_print("📋 Top Countries by Total Revenue (Excludes UK):")
display(revenue_by_country_excl_uk_df.head(10))

# 💾 Save output
revenue_country_excl_uk_path = os.path.join(project_base_path, 'sql_outputs', 'notebook_outputs', '04_revenue_by_country_excl_uk.csv')
revenue_by_country_excl_uk_df.to_csv(revenue_country_excl_uk_path, index=False)
safe_print(f"✅ Saved: {revenue_country_excl_uk_path}")


# In[ ]:


# 📊 Q5: Customer Behavior by Country – Matching EDA Output
query_customer_behavior_by_country = """
SELECT
    c.country,
    COUNT(DISTINCT c.customer_id) AS num_customers,
    COUNT(DISTINCT i.invoice_no) AS num_invoices,
    ROUND(SUM(ii.line_revenue), 2) AS total_revenue,
    ROUND(COUNT(DISTINCT i.invoice_no) * 1.0 / COUNT(DISTINCT c.customer_id), 2) AS avg_invoices_per_customer,
    ROUND(SUM(ii.line_revenue) * 1.0 / COUNT(DISTINCT c.customer_id), 2) AS avg_revenue_per_customer
FROM invoice_items AS ii
JOIN invoices AS i USING(invoice_no)
JOIN customers AS c USING(customer_id)
GROUP BY c.country
ORDER BY total_revenue DESC;
"""

# 🚀 Execute query
customer_behavior_df = pd.read_sql_query(query_customer_behavior_by_country, engine)

# 📋 Display result
safe_print("📊 Customer Behavior by Country (SQL Output):")
display(customer_behavior_df.head(10))

# 💾 Save output
behavior_path = os.path.join(project_base_path, 'sql_outputs', 'notebook_outputs', '05_customer_behavior_by_country.csv')
customer_behavior_df.to_csv(behavior_path, index=False)
safe_print(f"✅ Saved: {behavior_path}")


# In[ ]:


# 📝 SQL Query: Count of single vs. repeat customers with percentage
query_customer_type_summary = text("""
WITH invoice_counts AS (
    SELECT
        customer_id,
        COUNT(DISTINCT invoice_no) AS num_invoices
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
""")

# ▶️ Execute and load into DataFrame
customer_type_summary_df = pd.read_sql(query_customer_type_summary, con=engine)

# 👁️ Preview
safe_print("📊 One-Time vs. Repeat Customer Breakdown:")
display(customer_type_summary_df)

# 💾 Save the output
one_time_vs_repeat_path = os.path.join(sql_output_dir, '06_one_time_vs_repeat_customers.csv')
customer_type_summary_df.to_csv(one_time_vs_repeat_path, index=False)
safe_print(f"✅ Saved: {one_time_vs_repeat_path}")


# In[ ]:


# 📊 Q7: Top 10 Customers by Average Order Value
query_avg_order_value_per_customer = """
SELECT
    c.customer_id,
    ROUND(SUM(ii.line_revenue), 2) AS total_spent,
    COUNT(DISTINCT i.invoice_no) AS num_orders,
    ROUND(SUM(ii.line_revenue) * 1.0 / COUNT(DISTINCT i.invoice_no), 6) AS avg_order_value
FROM invoice_items AS ii
JOIN invoices AS i ON ii.invoice_no = i.invoice_no
JOIN customers AS c ON i.customer_id = c.customer_id
GROUP BY c.customer_id
ORDER BY avg_order_value DESC
LIMIT 10;
"""

# ▶️ Execute query
avg_order_value_df = pd.read_sql_query(query_avg_order_value_per_customer, engine)

# 👁️ Preview
safe_print("📋 Top 10 Customers by Avg Order Value:")
display(avg_order_value_df)

# 💾 Export to CSV
avg_order_value_path = os.path.join(project_base_path, 'sql_outputs', 'notebook_outputs', '07_avg_order_value_per_customer.csv')
avg_order_value_df.to_csv(avg_order_value_path, index=False)
safe_print(f"✅ Saved: {avg_order_value_path}")


# In[ ]:


# 🧾 Q8: Top 10 Customers by Total Spend (with avg order value)
query_top_spenders = """
SELECT
    c.customer_id,
    ROUND(SUM(ii.line_revenue), 2) AS total_spent,
    COUNT(DISTINCT i.invoice_no) AS num_orders,
    ROUND(SUM(ii.line_revenue) * 1.0 / COUNT(DISTINCT i.invoice_no), 2) AS avg_order_value
FROM invoice_items AS ii
JOIN invoices AS i ON ii.invoice_no = i.invoice_no
JOIN customers AS c ON i.customer_id = c.customer_id
GROUP BY c.customer_id
ORDER BY total_spent DESC
LIMIT 10;
"""

# ▶️ Run the query
top_spenders_df = pd.read_sql_query(query_top_spenders, engine)

# 👁️ Display the result
safe_print("📋 Top 10 Customers by Total Spend:")
display(top_spenders_df)

# 💾 Save the output
top_spenders_path = os.path.join(project_base_path, 'sql_outputs', 'notebook_outputs', '08_top_customers_by_total_spend.csv')
top_spenders_df.to_csv(top_spenders_path, index=False)
safe_print(f"✅ Saved: {top_spenders_path}")


# In[ ]:


from sqlalchemy import text
import matplotlib.pyplot as plt
import seaborn as sns

# 📅 Get the most recent invoice date in the dataset
latest_date_query = text("SELECT MAX(invoice_date) AS latest_date FROM invoices;")
latest_date_df = pd.read_sql(latest_date_query, engine)
latest_date = pd.to_datetime(latest_date_df['latest_date'].iloc[0])

safe_print(f"🗓️ Latest invoice date in dataset: {latest_date.date()}")

# Format timestamp string for SQL (with full precision)
latest_date_str = latest_date.strftime('%Y-%m-%d %H:%M:%S')

# 🧮 SQL Query: Recency per customer
query_recency = text(f"""
SELECT
    c.customer_id,
    MAX(i.invoice_date) AS invoice_date,
    CAST((strftime('%s', '{latest_date_str}') - strftime('%s', MAX(i.invoice_date))) / 86400 AS INTEGER) AS recency_days
FROM customers AS c
JOIN invoices AS i ON c.customer_id = i.customer_id
GROUP BY c.customer_id
ORDER BY recency_days ASC;
""")

# ▶️ Execute the query
recency_df = pd.read_sql(query_recency, engine)

# 👁️ Preview top and bottom 5 rows (recent and inactive)
safe_print("📋 Sample Customers by Recency (Top & Bottom):")
display(pd.concat([recency_df.head(), recency_df.tail()]))

# 💾 Export result
recency_output_path = os.path.join(project_base_path, 'sql_outputs', 'notebook_outputs', '09_customer_recency.csv')
recency_df.to_csv(recency_output_path, index=False)
safe_print(f"✅ Saved: {recency_output_path}")

# 📊 Visualize Recency Distribution
plt.figure(figsize=(14, 5))

# Histogram
plt.subplot(1, 2, 1)
sns.histplot(recency_df['recency_days'], bins=40, kde=False, color='skyblue')
plt.title("Distribution of Customer Recency")
plt.xlabel("Days Since Last Purchase")
plt.ylabel("Number of Customers")

# Boxplot
plt.subplot(1, 2, 2)
sns.boxplot(x=recency_df['recency_days'], color='lightgray')
plt.title("Boxplot of Customer Recency")
plt.xlabel("Days Since Last Purchase")

plt.tight_layout()
plt.show()


# In[ ]:


from sqlalchemy import text
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 🧮 SQL Query: Frequency per customer
query_frequency = text("""
SELECT
    c.customer_id,
    COUNT(DISTINCT i.invoice_no) AS num_orders,
    ROUND(SUM(ii.line_revenue), 2) AS total_spent,
    ROUND(SUM(ii.line_revenue) * 1.0 / COUNT(DISTINCT i.invoice_no), 2) AS avg_order_value
FROM customers AS c
JOIN invoices AS i ON c.customer_id = i.customer_id
JOIN invoice_items AS ii ON i.invoice_no = ii.invoice_no
GROUP BY c.customer_id
ORDER BY num_orders DESC;
""")

# ▶️ Run the query
frequency_df = pd.read_sql(query_frequency, engine)

# 📋 Show sample customers (top & bottom)
safe_print("📋 Sample Customers by Purchase Frequency (Top & Bottom):")
display(frequency_df.head())
display(frequency_df.tail())

# 💾 Save output
frequency_output_path = os.path.join(project_base_path, 'sql_outputs', 'notebook_outputs', '10_customer_frequency.csv')
frequency_df.to_csv(frequency_output_path, index=False)
safe_print(f"✅ Saved: {frequency_output_path}")

# 📊 Create bin edges (50 bins) and compute histogram
bin_count = 50
counts, bin_edges = np.histogram(frequency_df['num_orders'], bins=bin_count)

# 📋 Display frequency table using histogram counts
safe_print("\n📋 Frequency Table for Number of Orders:")
freq_table = pd.Series(counts, index=pd.IntervalIndex.from_breaks(bin_edges))
display(freq_table)

# 🎨 Plot histogram and boxplot
fig, axes = plt.subplots(1, 2, figsize=(16, 5))
fig.suptitle("Customer Purchase Frequency", fontsize=18, weight="bold")

# Histogram
axes[0].bar(x=bin_edges[:-1], height=counts, width=np.diff(bin_edges), color='skyblue', align='edge', edgecolor='gray')
axes[0].set_title("Distribution of Purchase Frequency")
axes[0].set_xlabel("Number of Orders")
axes[0].set_ylabel("Number of Customers")

# Boxplot
sns.boxplot(x=frequency_df['num_orders'], ax=axes[1], color='lightgray')
axes[1].set_title("Boxplot of Purchase Frequency")
axes[1].set_xlabel("Number of Orders")

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()


# In[ ]:


from sqlalchemy import text
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ✅ Ensure export directory exists
data_dir = os.path.join(project_base_path, 'sql_outputs', 'notebook_outputs')
os.makedirs(data_dir, exist_ok=True)

# 🧮 SQL query: total_spent, num_orders, avg_order_value per customer
query_monetary_full = text("""
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
""")

# ▶️ Execute the query
monetary_df = pd.read_sql(query_monetary_full, engine)

# 💾 Save to CSV
monetary_path = os.path.join(data_dir, '11_customer_monetary_value.csv')
monetary_df.to_csv(monetary_path, index=False)
safe_print(f"✅ Saved: {monetary_path}")

# 👁️ Show sample customers (top and bottom)
safe_print("\n📋 Sample Customers by Monetary Value (Top & Bottom):")
display(monetary_df[['customer_id', 'total_spent', 'num_orders', 'avg_order_value']].head())
display(monetary_df[['customer_id', 'total_spent', 'num_orders', 'avg_order_value']].tail())

# 📊 Frequency table using ~£20K bins
bin_count = 30
bin_edges = np.histogram_bin_edges(monetary_df['total_spent'], bins=bin_count)
freq_table = pd.cut(monetary_df['total_spent'], bins=bin_edges).value_counts().sort_index()
safe_print("\n📋 Frequency Table for Total Spend:")
display(freq_table.to_frame())

# 🎨 Plot histogram and boxplot
fig, axes = plt.subplots(1, 2, figsize=(16, 5))
fig.suptitle("Customer Monetary Value", fontsize=18, weight="bold")

# Histogram
sns.histplot(monetary_df['total_spent'], bins=bin_edges, ax=axes[0], color='mediumseagreen')
axes[0].set_title("Distribution of Total Spend")
axes[0].set_xlabel("Total Spend (£)")
axes[0].set_ylabel("Number of Customers")

# Boxplot
sns.boxplot(x=monetary_df['total_spent'], ax=axes[1], color='lightgray')
axes[1].set_title("Boxplot of Total Spend")
axes[1].set_xlabel("Total Spend (£)")

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()


# In[ ]:


from sqlalchemy import text
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ✅ Output path (CSV only)
rfm_export_path = os.path.join(project_base_path, 'sql_outputs', 'notebook_outputs', '12_rfm_segmented_customers.csv')

# 📅 Define dataset cutoff date
last_date = pd.to_datetime("2011-12-09")

# 🧾 SQL: Extract RFM base metrics from relational tables
query_rfm = text("""
SELECT
    c.customer_id,
    MAX(i.invoice_date) AS last_purchase,
    COUNT(DISTINCT i.invoice_no) AS frequency,
    ROUND(SUM(ii.line_revenue), 2) AS monetary
FROM customers AS c
JOIN invoices AS i ON c.customer_id = i.customer_id
JOIN invoice_items AS ii ON i.invoice_no = ii.invoice_no
GROUP BY c.customer_id
""")

# ▶️ Execute query and load into DataFrame
rfm_df = pd.read_sql(query_rfm, engine)

# 🧮 Calculate Recency (days since last purchase)
rfm_df['last_purchase'] = pd.to_datetime(rfm_df['last_purchase'])
rfm_df['recency'] = (last_date - rfm_df['last_purchase']).dt.days

# 📊 Assign RFM scores using quartiles (1 = lowest, 4 = highest)
rfm_df['R'] = pd.qcut(rfm_df['recency'], 4, labels=[4, 3, 2, 1]).astype(int)
rfm_df['F'] = pd.qcut(rfm_df['frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4]).astype(int)
rfm_df['M'] = pd.qcut(rfm_df['monetary'], 4, labels=[1, 2, 3, 4]).astype(int)

# 🧮 RFM score sum
rfm_df['RFM_Score'] = rfm_df[['R', 'F', 'M']].sum(axis=1)

# 🏷️ Segment assignment (match EDA logic)
def assign_segment(row):
    if row['RFM_Score'] >= 9:
        return 'High-Value'
    elif row['R'] >= 3 and row['F'] >= 3:
        return 'Loyal'
    elif row['R'] == 1:
        return 'At-Risk'
    elif row['F'] == 1 and row['M'] == 1:
        return 'One-Time'
    else:
        return 'Other'

rfm_df['Segment'] = rfm_df.apply(assign_segment, axis=1)

# 💾 Export CSV
rfm_df.to_csv(rfm_export_path, index=False)
safe_print(f"✅ Saved: {rfm_export_path}")

# 📋 Show preview of RFM table
safe_print("\n📋 Sample of RFM Score Table:")
display(rfm_df.head(10))

# 📊 Show segment distribution
safe_print("\n📋 RFM Segment Counts:")
segment_counts = rfm_df['Segment'].value_counts().sort_values(ascending=False)
display(segment_counts)

# 🎨 Plot segment distribution (no warning)
plt.figure(figsize=(10, 6))
sns.barplot(
    x=segment_counts.index,
    y=segment_counts.values,
    hue=segment_counts.index,       # ✅ assign x to hue
    palette='Set2',
    legend=False                    # ✅ disables redundant legend
)
plt.title("Customer Segments Based on RFM Scores", fontsize=16, weight="bold")
plt.xlabel("RFM Segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()



# In[ ]:


# ✅ Optional script execution indicator for CLI use
if __name__ == "__main__":
    safe_print("🚀 SQL analysis script executed directly as a .py file — all queries and exports have been completed.")



# ------------------------------------------------------------------------------
# 🛡️ License & Attribution
#
# © 2024 Ginosca Alejandro Dávila
# Project: Online Retail II – Sales Analysis & Customer Segmentation
# 🏫 School: Ironhack Puerto Rico
# 🎓 Bootcamp: Data Science and Machine Learning
# 📅 Date: December 20, 2024
# This work is provided for educational purposes under the MIT License.
# You may reuse, modify, or redistribute with attribution.
# ------------------------------------------------------------------------------
