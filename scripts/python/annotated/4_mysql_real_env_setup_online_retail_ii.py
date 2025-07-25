# 🛠️ MySQL Environment Setup Script – Online Retail II
# 📓 Source Notebook: 4_mysql_real_env_setup_online_retail_ii.ipynb
# ⚙️ Description: Automates MySQL DB creation and loads cleaned CSVs into tables.
# 🏫 School: Ironhack Puerto Rico
# 🎓 Bootcamp: Data Science and Machine Learning
# 📅 Date: December 20, 2024
# 👩‍💻 Author: Ginosca Alejandro Dávila

#!/usr/bin/env python
# coding: utf-8

# # 🛠️ MySQL Real Environment Setup – Online Retail II
# 
# ### 🗃️ Notebook: `4_mysql_real_env_setup_online_retail_ii.ipynb`  
# 📅 **Start Date:** December 20, 2024  
# 👩‍💻 **Author:** Ginosca Alejandro Dávila  
# 
# ---
# 
# ## 📌 Notebook Overview
# 
# This notebook sets up a **real MySQL database environment** to execute SQL queries directly within **MySQL Workbench 8.0 CE** or any other MySQL client.  
# It serves as the transition point between **notebook-based SQL analysis in Python (Colab)** and **production-ready SQL execution** in a real database engine.
# 
# We will:
# 
# - Create the `retail_sales` database and schema in MySQL
# - Automatically import cleaned `.csv` tables using Python
# - Validate the schema for referential integrity
# - Prepare the database for SQL queries developed in `3_sql_analysis_sales_performance_online_retail_ii.ipynb`
# 
# ---
# 
# ## 🗂️ Input Data Location
# 
# 📁 **Local Path**:  
# `C:\Users\Mory\Documents\Ironhack\Week 3\Week 3 - Day 4\project-2-eda-sql\retail-sales-segmentation-sql\cleaned_data\`
# 
# Includes:
# 
# | Filename           | Description                             |
# |--------------------|-----------------------------------------|
# | `customers.csv`     | 1 row per customer (ID, country)        |
# | `products.csv`      | Unique product catalog with prices      |
# | `invoices.csv`      | Each invoice with customer and date     |
# | `invoice_items.csv` | Item-level breakdown per invoice        |
# 
# These files were generated in `1_data_cleaning_online_retail_ii.ipynb`.
# 
# ---
# 
# ## 🧭 Execution Environment
# 
# > ⚠️ Unlike the rest of the project—which is built and run inside **Google Colab with Google Drive integration**—this notebook operates entirely on your **local machine**.
# >
# > The goal is to mirror a **real-world SQL deployment scenario** where Python is used to automate schema creation and data loading into a local MySQL database.
# 
# ---
# 
# ## ⚙️ MySQL Setup Tasks
# 
# The setup process will follow these steps:
# 
# 1. ✅ Drop and recreate the `retail_sales` database
# 2. ✅ Create the schema and tables using Python
# 3. ✅ Load each `.csv` file programmatically using `mysql-connector-python`
# 4. ✅ Confirm table creation and data integrity
# 5. ✅ Prepare to run SQL queries interactively in Workbench or other tools
# 
# ---
# 
# ## 🎯 Goals
# 
# ✔ Automate MySQL schema creation and data loading using Python  
# ✔ Ensure a **clean and reproducible import pipeline** for SQL analysis  
# ✔ Enable **real-world SQL validation** of analytical logic developed in prior notebooks  
# 
# ---
# 
# 📓 Next: Load environment variables and establish the MySQL connection.
# 

# ## 🗂️ Step 1: Local File Access Setup
# 
# This notebook runs in a **local environment**, so there's no need to mount Google Drive.
# 
# We'll manually define the path to the cleaned .csv files generated in 1_data_cleaning_online_retail_ii.ipynb.
# 
# 📁 **Local Path**:  
# C:\Users\Mory\Documents\Ironhack\Week 3\Week 3 - Day 4\project-2-eda-sql\retail-sales-segmentation-sql\cleaned_data\
# 
# This folder should include the four normalized relational tables:
# 
# - customers.csv
# - products.csv
# - invoices.csv
# - invoice_items.csv
# 
# > ✅ These files will be programmatically imported into the MySQL database to recreate the schema and enable real SQL query execution.

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


# ## 🔐 Step 2: Load MySQL Credentials from `.env` File or Prompt
# 
# To protect sensitive information, we recommend storing MySQL credentials in a `.env` file located in the `config/` folder.  
# This allows the script to securely load them as environment variables using the `dotenv` package.
# 
# > 🔒 This approach avoids hardcoding sensitive values directly into your source code and helps protect credentials in collaborative environments.
# 
# If the `.env` file is missing or partially filled, the script will automatically **prompt the user to manually enter any missing values**.  
# This ensures that the notebook remains fully usable on any machine, whether or not an `.env` file is present.
# 
# ---
# 
# ### 🗂️ Configuration Instructions (Optional but Recommended)
# 
# You have two options:
# 
# **Option 1 – Use Prompt Mode**  
# Let the notebook prompt you for each credential when it's needed (no setup required).
# 
# **Option 2 – Use a `.env` File (Recommended for Reuse and Safety)**
# 
# 1. Open the provided template file:  
#    `config/mysql_credentials_template.txt`
# 
# 2. Fill in your own MySQL credentials:  
#    
#     MYSQL_HOST=127.0.0.1  
#     MYSQL_PORT=3306  
#     MYSQL_USER=your_username_here  
#     MYSQL_PASSWORD=your_password_here  
#     MYSQL_DATABASE=retail_sales  
# 
#    > 💡 `MYSQL_HOST` is typically `127.0.0.1` or `localhost` if you're running MySQL locally.  
#    > 💡 `MYSQL_PORT` is usually `3306`, unless you've configured MySQL to run on a different port.
# 
# 3. Save the file, then **rename it** to:  
#    `mysql_credentials.env` (remove `.txt` extension)
# 
# > 🔐 **Optional Security Note:** If you're working in a shared or public project, make sure to add `.env` to your `.gitignore` file to prevent exposing sensitive credentials.
# 
# > 🧪 After loading or prompting, the script will display the loaded configuration (excluding password) for confirmation.
# 

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


# ## 🔌 Step 3: Connect to MySQL Server
# 
# Now that we’ve securely loaded our MySQL credentials, we’ll attempt to establish a connection to the server using `mysql-connector-python`.
# 
# > ⚙️ This connection enables us to create the database schema and load data into MySQL directly from the cleaned `.csv` files.
# >
# > 🧪 If the connection is successful, we’ll print the server version as confirmation.
# 

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


# ## 🧱 Step 4: Create the `retail_sales` Database and Schema
# 
# Now that the MySQL connection is established, we will create the `retail_sales` database and define its schema.
# 
# This schema consists of four interrelated tables:
# 
# - `customers` — customer ID and country
# - `products` — product catalog and unit prices
# - `invoices` — invoice metadata with timestamps
# - `invoice_items` — line-level purchase details with quantities and revenue
# 
# > ⚠️ This step will **drop the database if it already exists**, then recreate it from scratch to ensure a clean setup.  
# > Use caution if re-running this cell in a production environment.
# 

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


# ## 🧮 Step 5: Load Cleaned CSV Files into MySQL Tables
# 
# Now that the `retail_sales` schema is ready, we will load each of the cleaned `.csv` files into their corresponding tables:
# 
# - `customers.csv` → `customers`
# - `products.csv` → `products`
# - `invoices.csv` → `invoices`
# - `invoice_items.csv` → `invoice_items`
# 
# > 🔁 We’ll use `pandas` to read each CSV and `mysql.connector` to insert the records into MySQL.  
# > 💾 Each insertion is committed after successful execution.  
# > ✅ At the end, we’ll print the number of rows inserted into each table.
# 

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


# ### 🧾 Inserted Rows Per Table
# 
# The output confirms that each CSV file was successfully read and inserted into its respective MySQL table:
# 
# - `customers` → 5,852 rows  
# - `products` → 4,624 rows  
# - `invoices` → 36,607 rows  
# - `invoice_items` → 766,226 rows
# 
# ✅ All records were loaded without error, and the connection was properly closed.  
# Next, we will re-establish a connection to verify the actual contents of each table with a row count check.
# 

# ## 🔍 Step 6: Validate Inserted Row Counts
# 
# To confirm that the data was successfully loaded into the MySQL tables,  
# we reconnect to the database and run `SELECT COUNT(*)` queries on each table.
# 
# This acts as a post-insertion sanity check to ensure all expected rows were inserted and committed correctly.
# 

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


# ### 🧾 Confirmed Row Counts
# 
# The output below shows the number of rows found in each table **after reconnection**, confirming data integrity in the MySQL database.
# 
# ```
# 🔎 Table `customers` contains 5,852 rows  
# 🔎 Table `products` contains 4,624 rows  
# 🔎 Table `invoices` contains 36,607 rows  
# 🔎 Table `invoice_items` contains 766,226 rows  
# ```
# 
# ✅ These values match the number of rows inserted earlier, indicating successful data loading.
# 

# ## 🧪 Step 7: Validate Referential Integrity
# 
# To ensure the MySQL database was set up correctly and all relationships between tables are preserved, we run several integrity checks:
# 
# - All `invoice_items` entries must reference existing `invoice_no` and `stock_code` in `invoices` and `products`
# - All `invoices` must reference valid `customer_id` from `customers`
# - Optional sanity checks:
#   - Invoices with no line items
#   - Customers or products that were never used
# 
# These checks confirm the relational structure is sound and ready for SQL querying.
# 

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


# ### 🧩 Referential Integrity Validation
# 
# The output confirms that all foreign key relationships and expected business rules are satisfied:
# 
# - 🧩 Every `invoice_item` references a valid `invoice_no` and `stock_code` from the `invoices` and `products` tables.
# - 🧾 Each `invoice` is associated with a valid `customer_id`, confirming the integrity of customer relationships.
# - 📪 Every invoice has at least one corresponding line item in `invoice_items`.
# - 👥 No customers exist without invoices, indicating that all customers in the dataset were active.
# - 📦 Every product listed was sold at least once, meaning there are no unused entries in the product catalog.
# 
# ✅ These checks confirm that the **relational structure is intact**, and the dataset is ready for reliable SQL analysis.
# 

# ## ✅ Setup Complete – MySQL Environment Ready
# 
# All setup steps have been successfully completed:
# 
# - ✅ Credentials loaded securely from `.env` file
# - ✅ Connected to local MySQL Server (v8.0.40)
# - ✅ Created `retail_sales` schema and 4 relational tables
# - ✅ Inserted cleaned data from CSVs
# - ✅ Verified table row counts and foreign key relationships
# - ✅ Passed all referential integrity and sanity checks
# 
# 🎯 **Next Steps:**
# 
# The `retail_sales` MySQL database is now ready for querying using:
# - The SQL scripts and logic developed in `3_sql_analysis_sales_performance_online_retail_ii.ipynb`
# - Or any external SQL client (e.g., MySQL Workbench, DBeaver)
# 
# This notebook serves as a **reproducible deployment tool** for initializing a clean, validated database environment from the cleaned dataset.
# 

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
