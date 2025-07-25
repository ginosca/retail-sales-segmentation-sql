# 🛠️ MySQL Environment Setup Script – Online Retail II
# 📓 Source Notebook: 4_mysql_real_env_setup_online_retail_ii.ipynb
# ⚙️ Description: Automates MySQL DB creation and loads cleaned CSVs into tables.
# 🏫 School: Ironhack Puerto Rico
# 🎓 Bootcamp: Data Science and Machine Learning
# 📅 Date: December 20, 2024
# 👩‍💻 Author: Ginosca Alejandro Dávila

#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pathlib import Path
import os

# ✅ Safe print for terminal compatibility
def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="ignore").decode())

# ✅ Automatically detect the base project folder (assumes notebook is inside /notebooks)
notebook_path = Path.cwd()
project_base_path = notebook_path.parent  # assumes /notebooks/ folder
cleaned_data_path = project_base_path / 'cleaned_data'

# ✅ List expected files
expected_files = [
    'customers.csv',
    'products.csv',
    'invoices.csv',
    'invoice_items.csv'
]

# 📂 Check for presence of each file
missing_files = []
for file in expected_files:
    file_path = cleaned_data_path / file
    if not file_path.exists():
        missing_files.append(file_path)

# 🧾 Display results
if not missing_files:
    safe_print(f"✅ All cleaned data files found in: {cleaned_data_path.resolve()}")
else:
    safe_print("❌ Missing files:")
    for mf in missing_files:
        safe_print(f" - {mf.resolve()}")


# In[ ]:


# 📦 Ensure python-dotenv is installed (CLI + Jupyter compatible)
try:
    import dotenv
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
    import dotenv

# 📚 Load environment variables from .env file using pathlib
from dotenv import load_dotenv
import os
from pathlib import Path

# 🔍 Build full path to the .env file using pathlib (cross-platform safe)
env_path = (project_base_path / 'config' / 'mysql_credentials.env').resolve()

# ⚠️ Check if .env file exists before attempting to load
if not env_path.exists():
    safe_print(f"⚠️  Warning: .env file not found at: {env_path}")
    safe_print("🔄 You will be prompted to enter credentials manually.\n")

# ✅ Load environment variables if file exists
load_dotenv(dotenv_path=str(env_path))

# 🛠️ Helper function to prompt for missing values
def prompt_if_missing(value, prompt_text, cast_func=str):
    return cast_func(value) if value else cast_func(input(prompt_text))

# 🔐 Retrieve credentials from environment or prompt if missing
mysql_config = {
    'host': os.getenv('MYSQL_HOST'),
    'port': os.getenv('MYSQL_PORT'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

# ✅ Prompt for any missing credentials with fallback defaults
mysql_config['host'] = prompt_if_missing(mysql_config['host'], "Enter MySQL host (e.g., 127.0.0.1): ")
mysql_config['port'] = prompt_if_missing(mysql_config['port'], "Enter MySQL port (default 3306): ", lambda x: int(x) if x else 3306)
mysql_config['user'] = prompt_if_missing(mysql_config['user'], "Enter MySQL username: ")
mysql_config['password'] = prompt_if_missing(mysql_config['password'], "Enter MySQL password: ")
mysql_config['database'] = prompt_if_missing(mysql_config['database'], "Enter target database name: ")

# 🧪 Display loaded variables for confirmation (excluding password)
safe_print(f"✅ Host: {mysql_config['host']}")
safe_print(f"✅ Port: {mysql_config['port']}")
safe_print(f"✅ User: {mysql_config['user']}")
safe_print(f"✅ Database: {mysql_config['database']}")


# In[ ]:


# 📦 Ensure mysql-connector-python is installed (CLI + Jupyter compatible)
try:
    import mysql.connector
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mysql-connector-python"])
    import mysql.connector

from mysql.connector import connect, Error

# ✅ Attempt to connect using loaded credentials
try:
    connection = connect(
        host=mysql_config['host'],
        port=int(mysql_config['port']),  # Ensure port is int
        user=mysql_config['user'],
        password=mysql_config['password']
    )
    if connection.is_connected():
        db_info = connection.server_info
        safe_print(f"✅ Connected to MySQL Server at {mysql_config['host']}:{mysql_config['port']} as user '{mysql_config['user']}' – version {db_info}")
except Error as e:
    safe_print(f"❌ Connection failed: {e}")


# In[ ]:


# ✅ Create a cursor object to execute SQL commands
cursor = connection.cursor()

# 🧱 SQL script to drop and recreate the database and schema
schema_sql = """
DROP DATABASE IF EXISTS retail_sales;
CREATE DATABASE retail_sales;
USE retail_sales;

-- Customers table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    country VARCHAR(100)
);

-- Products table
CREATE TABLE products (
    stock_code VARCHAR(10) PRIMARY KEY,
    description TEXT,
    unit_price DECIMAL(10, 2)
);

-- Invoices table
CREATE TABLE invoices (
    invoice_no VARCHAR(10) PRIMARY KEY,
    invoice_date DATETIME,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Invoice items table
CREATE TABLE invoice_items (
    invoice_no VARCHAR(10),
    stock_code VARCHAR(10),
    quantity INT,
    unit_price DECIMAL(10, 2),
    line_revenue DECIMAL(12, 2),
    FOREIGN KEY (invoice_no) REFERENCES invoices(invoice_no),
    FOREIGN KEY (stock_code) REFERENCES products(stock_code)
);
"""

# 🏗️ Execute schema creation step by step
try:
    for statement in schema_sql.strip().split(';'):
        if statement.strip():
            cursor.execute(statement.strip() + ';')

    connection.commit()  # commit DDL changes
    safe_print("✅ Database and schema created successfully.")
except Error as e:
    safe_print(f"❌ Failed to create schema: {e}")


# In[ ]:


import pandas as pd

# ✅ Define file-to-table mapping
table_map = {
    'customers.csv': 'customers',
    'products.csv': 'products',
    'invoices.csv': 'invoices',
    'invoice_items.csv': 'invoice_items'
}

# ✅ Establish a new connection that includes the database
try:
    conn_with_db = connect(
    host=mysql_config['host'],
    port=int(mysql_config['port']),
    user=mysql_config['user'],
    password=mysql_config['password'],
    database=mysql_config['database']
)
    cursor = conn_with_db.cursor()

    for filename, table in table_map.items():
        file_path = cleaned_data_path / filename
        df = pd.read_csv(file_path)

        safe_print(f"\n📥 Loading data into table: {table}")

        if df.empty:
            safe_print(f"⚠️  Skipped `{table}` – CSV file is empty.")
            continue

        # Dynamically build the insert statement
        columns = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))
        insert_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        # Convert DataFrame rows to list of tuples and insert
        data_tuples = list(df.itertuples(index=False, name=None))
        cursor.executemany(insert_query, data_tuples)
        conn_with_db.commit()

        safe_print(f"✅ Inserted {df.shape[0]} rows into `{table}`")

except Error as e:
    safe_print(f"❌ Error inserting data: {e}")

finally:
    if cursor:
        cursor.close()
    if conn_with_db.is_connected():
        conn_with_db.close()
        safe_print("🔌 MySQL connection closed.")


# In[ ]:


# ✅ Validate inserted row counts
try:
    conn_check = connect(
        host=mysql_config['host'],
        port=int(mysql_config['port']),
        user=mysql_config['user'],
        password=mysql_config['password'],
        database=mysql_config['database']
    )
    cursor = conn_check.cursor()

    for table in table_map.values():
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        safe_print(f"🔎 Table `{table}` contains {count:,} rows")

    safe_print("✅ All table row counts verified successfully.")

except Error as e:
    safe_print(f"❌ Validation failed: {e}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if conn_check.is_connected():
        conn_check.close()


# In[ ]:


# ✅ Sample referential integrity and sanity checks
try:
    conn_check = connect(**mysql_config)
    cursor = conn_check.cursor()

    # Store results for optional export/logging
    integrity_results = {}

    # 1. Orphaned rows in invoice_items
    cursor.execute("""
        SELECT COUNT(*) FROM invoice_items
        WHERE invoice_no NOT IN (SELECT invoice_no FROM invoices)
           OR stock_code NOT IN (SELECT stock_code FROM products)
    """)
    orphan_items = cursor.fetchone()[0]
    integrity_results["orphan_invoice_items"] = orphan_items
    if orphan_items == 0:
        safe_print("🧩 OK – No orphaned rows in `invoice_items` (foreign keys to invoices/products)")
    else:
        safe_print(f"⚠️ {orphan_items:,} orphaned rows in `invoice_items`")

    # 2. Invoices with missing customers
    cursor.execute("""
        SELECT COUNT(*) FROM invoices
        WHERE customer_id NOT IN (SELECT customer_id FROM customers)
    """)
    orphan_invoices = cursor.fetchone()[0]
    integrity_results["orphan_invoices"] = orphan_invoices
    if orphan_invoices == 0:
        safe_print("🧾 OK – All invoices reference valid customers")
    else:
        safe_print(f"⚠️ {orphan_invoices:,} invoices with missing customer_id")

    # 3. Invoices with no items
    cursor.execute("""
        SELECT COUNT(*) FROM invoices
        WHERE invoice_no NOT IN (SELECT DISTINCT invoice_no FROM invoice_items)
    """)
    empty_invoices = cursor.fetchone()[0]
    integrity_results["empty_invoices"] = empty_invoices
    if empty_invoices == 0:
        safe_print("📪 OK – All invoices have at least one line item")
    else:
        safe_print(f"⚠️ {empty_invoices:,} invoices with no line items")

    # 4. Customers with no invoices
    cursor.execute("""
        SELECT COUNT(*) FROM customers
        WHERE customer_id NOT IN (SELECT DISTINCT customer_id FROM invoices)
    """)
    inactive_customers = cursor.fetchone()[0]
    integrity_results["inactive_customers"] = inactive_customers
    safe_print(f"👥 Info – {inactive_customers:,} customers with no invoices")

    # 5. Products never sold
    cursor.execute("""
        SELECT COUNT(*) FROM products
        WHERE stock_code NOT IN (SELECT DISTINCT stock_code FROM invoice_items)
    """)
    unsold_products = cursor.fetchone()[0]
    integrity_results["unsold_products"] = unsold_products
    safe_print(f"📦 Info – {unsold_products:,} products never sold")

    safe_print("✅ Referential integrity and sanity checks completed successfully.")

except Error as e:
    safe_print(f"❌ Referential integrity check failed: {e}")

finally:
    if cursor:
        cursor.close()
    if conn_check.is_connected():
        conn_check.close()
        safe_print("🔌 MySQL connection closed")


# In[ ]:






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
