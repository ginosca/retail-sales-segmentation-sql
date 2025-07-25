# 🧼 Data Cleaning Script – Online Retail II
# 📓 Source Notebook: 1_data_cleaning_online_retail_ii.ipynb
# 📊 Description: Loads, cleans, and prepares the Online Retail II dataset for analysis.
# 🏫 School: Ironhack Puerto Rico
# 🎓 Bootcamp: Data Science and Machine Learning
# 📅 Date: December 20, 2024
# 👩‍💻 Author: Ginosca Alejandro Dávila

#!/usr/bin/env python
# coding: utf-8

# # 🧼 **Data Cleaning for E-Commerce Sales & Customer Segmentation (Online Retail II)**
# ## **Data Science and Machine Learning Bootcamp – Ironhack Puerto Rico**
# ### 📓 Notebook: `1_data_cleaning_online_retail_ii.ipynb`
# 📅 **Date:** December 20, 2024  
# 👩‍💻 **Author:** Ginosca Alejandro Dávila  
# 
# ---
# 
# ## **📌 Project Overview**
# This project analyzes transactional data from a **UK-based online retailer** to uncover insights into customer behavior, product sales, and revenue patterns.  
# The analysis culminates in a **customer segmentation model using RFM (Recency, Frequency, Monetary)** metrics.
# 
# Key business questions addressed include:
# - 📈 What are the top-selling products and monthly revenue trends?
# - 🌍 Which countries generate the most sales?
# - 👤 Who are the highest-value and most loyal customers?
# - 🧠 How can we segment customers to optimize marketing strategies?
# 
# 📓 **This notebook focuses specifically on the data preparation phase**, including:
# - Data loading and initial inspection
# - Cleaning and validation
# - Relational transformation into four structured tables
# - Exporting cleaned `.csv` files for SQL-based analysis
# 
# > 📄 For the full project instructions provided by Ironhack, see:  
# > [`reference/project_2_eda_sql_project_instructions.md`](../reference/project_2_eda_sql_project_instructions.md)
# 
# ---
# 
# ## **📂 Dataset Description**
# 
# 📁 **online_retail_II.xlsx**  
# - Source: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii)  
# - Contains two sheets:
#   - `Year 2009-2010`
#   - `Year 2010-2011`  
# - ~1 million rows across both years
# 
# | Column         | Description                                             |
# |----------------|---------------------------------------------------------|
# | `Invoice`      | Transaction ID (prefix `'C'` = cancellation)            |
# | `StockCode`    | Product ID                                              |
# | `Description`  | Product name                                            |
# | `Quantity`     | Items purchased per transaction                         |
# | `InvoiceDate`  | Date and time of the transaction                        |
# | `Price`        | Unit price in GBP                                       |
# | `Customer ID`  | Unique customer identifier (nullable)                   |
# | `Country`      | Country where the transaction occurred                  |
# 
# ---
# 
# ## **🎯 Goals**
# 
# ✔ Clean and normalize raw Excel data into a relational structure  
# ✔ Export four cleaned `.csv` files ready for SQL import and querying  
# ✔ Lay the foundation for business metric analysis and RFM segmentation  
# ✔ Ensure clean, reproducible code using `pandas`, following best practices  
# ✔ Extend into SQL queries and visual dashboards  
# 
# ---
# 
# ## 🗃️ Project Folder Structure
# 
# 📁 `retail-sales-segmentation-sql/` → Project root folder  
# ├── 📂 `cleaned_data/` → Cleaned flat file and normalized relational tables  
# │   ├── `cleaned_online_retail_II.csv`  
# │   ├── `customers.csv`  
# │   ├── `products.csv`  
# │   ├── `invoices.csv`  
# │   └── `invoice_items.csv`  
# 
# ├── 📂 `config/` → Configuration files (non-sensitive templates only)  
# │   └── `mysql_credentials_template.txt`  
# 
# ├── 📂 `dashboard/` → Optional Tableau dashboard (currently empty)  
# 
# ├── 📂 `data/` → Raw input files  
# │   └── `online_retail_II.xlsx`  
# 
# ├── 📂 `eda_outputs/` → Python-based EDA outputs  
# │   ├── 📂 `data/` → Exported tables from analysis  
# │   └── 📂 `plots/` → Visualizations (distributions, time trends, etc.)  
# 
# ├── 📂 `images/` → Static diagrams and visual assets  
# │   └── `online_retail_ii_erd.png`  
# 
# ├── 📂 `notebooks/` → All Jupyter notebooks (Google Colab-compatible)  
# │   ├── `1_data_cleaning_online_retail_ii.ipynb`  
# │   ├── `2_eda_online_retail_ii.ipynb`  
# │   ├── `3_sql_analysis_sales_performance_online_retail_ii.ipynb`  
# │   ├── `4_mysql_real_env_setup_online_retail_ii.ipynb`  
# │   ├── `export_notebooks_to_py_online_retail_ii.ipynb`  
# │   └── `test_clean_scripts_colab_online_retail_ii.ipynb`  
# 
# ├── 📂 `reference/` → Project instructions and reference materials  
# │   └── `project_2_eda_sql_project_instructions.md`  
# 
# ├── 📂 `reports/` → Markdown reports and final presentation  
# │   ├── 📂 `python/`  
# │   │   ├── `1_data_cleaning_report_online_retail_ii.md`  
# │   │   ├── `2_eda_report_online_retail_ii.md`  
# │   │   ├── `3_sql_analysis_report_online_retail_ii.md`  
# │   │   └── `4_mysql_setup_report_online_retail_ii.md`  
# │   ├── 📂 `sql/`  
# │   │   ├── `1_sql_validation_report_online_retail_ii.md`  
# │   │   └── `2_sql_business_questions_report_online_retail_ii.md`  
# │   └── 📂 `presentation/`  
# │       │└── `online_retail_ii_eda_and_sql_project_presentation.pptx`  
# 
# ├── 📂 `scripts/` → Python scripts for automation and analysis  
# │   ├── 📂 `python/`  
# │   │   ├── 📂 `annotated/` → Scripts with markdown-style comments  
# │   │   │   ├── `1_data_cleaning_online_retail_ii.py`  
# │   │   │   ├── `2_eda_online_retail_ii.py`  
# │   │   │   ├── `3_sql_analysis_sales_performance.py`  
# │   │   │   └── `4_mysql_real_env_setup_online_retail_ii.py`  
# │   │   └── 📂 `clean/` → Clean production-ready versions (no comments)  
# │   │       │├── `1_data_cleaning_online_retail_ii.py`  
# │   │       │├── `2_eda_online_retail_ii.py`  
# │   │       │├── `3_sql_analysis_sales_performance.py`  
# │   │       │└── `4_mysql_real_env_setup_online_retail_ii.py`  
# │   └── 📂 `sql/`  
# │       │└── 📂 `queries/`  
# │   │           │├── `1_validate_online_retail_ii.sql`  
# │   │           │└── `2_business_questions_online_retail_ii.sql`  
# 
# ├── 📂 `sql_outputs/` → SQL query outputs  
# │   ├── 📂 `mysql_outputs/` → Results from MySQL environment  
# │   └── 📂 `notebook_outputs/` → Results from SQL run in Jupyter notebooks  
# │
# └── 📄 `README.md` → Project overview and structure
# 
# 

# ---
# 
# ## 📂 Step 1: Mounting Google Drive
# 
# Since the dataset for this project is stored in Google Drive, the first step is to **mount Google Drive** in order to access the project files.
# 
# This notebook works in both **Google Colab** and **local environments**. When running in Colab, it will look for the dataset in:
# 
# `My Drive > Colab Notebooks > Ironhack > Week 3 > Week 3 - Day 4 > project-2-eda-sql > retail-sales-segmentation-sql > data > online_retail_II.xlsx`
# 
# The script will mount the drive, attempt to access the default path, and prompt the user for input if the default is not found.
# 
# ---
# 

# In[ ]:


import sys
import os

# ✅ Safe print for emojis in CLI environments
def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="ignore").decode())

# ✅ Check if running in Google Colab
def is_colab():
    return 'google.colab' in sys.modules

# 🔧 Set project base path depending on environment
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
        safe_print("👉 Example: 'MyDrive/Colab Notebooks/Ironhack/.../retail-sales-segmentation-sql'")
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

    # Automatically walk up until project root (contains 'data/' and 'notebooks/')
    levels_up = 0
    while levels_up < 5:
        potential_root = os.path.abspath(os.path.join(script_dir, *(['..'] * levels_up)))
        if os.path.isdir(os.path.join(potential_root, 'data')) and os.path.isdir(os.path.join(potential_root, 'notebooks')):
            project_base_path = potential_root
            break
        levels_up += 1
    else:
        raise FileNotFoundError("❌ Project root folder not found. Ensure it contains 'data' and 'notebooks' folders.")

    safe_print(f"✅ Local environment detected. Base path set to: {project_base_path}")


# ---
# 
# ## 📥 Step 2: Importing Libraries and Loading Dataset
# 
# We begin by importing the essential libraries for data processing and loading the **Online Retail II** dataset from Excel.
# 
# The dataset file contains two sheets:
# - `Year 2009-2010`
# - `Year 2010-2011`
# 
# We will merge both sheets into a single DataFrame to prepare for data cleaning and relational transformation.
# 
# ---
# 

# In[ ]:


# 📦 Import required libraries
import pandas as pd
import numpy as np
import os

# 📁 Full path to dataset
excel_path = os.path.join(project_base_path, 'data', 'online_retail_II.xlsx')

# 🔍 Show the resolved path
safe_print(f"📄 Looking for: {excel_path}")

# 📥 Load Excel sheets
try:
    df_2009 = pd.read_excel(excel_path, sheet_name='Year 2009-2010')
    df_2010 = pd.read_excel(excel_path, sheet_name='Year 2010-2011')
    safe_print("✅ Excel sheets loaded successfully.")
except FileNotFoundError:
    safe_print("❌ Excel file not found.")
    safe_print(f"🔎 Tried: {excel_path}")
    safe_print("📌 Make sure the file exists and is named correctly.")
    raise
except Exception as e:
    safe_print("❌ An unexpected error occurred while loading the Excel file.")
    raise e

# 🔗 Combine into single DataFrame
df_raw = pd.concat([df_2009, df_2010], ignore_index=True)
safe_print(f"🧾 Combined dataset shape: {df_raw.shape}")


# ---
# 
# ### ✅ Excel Sheets Loaded Successfully
# 
# The `online_retail_II.xlsx` file was found in the expected location and both sheets — **`Year 2009-2010`** and **`Year 2010-2011`** — were successfully loaded and merged.
# 
# - 🧾 **Combined dataset shape:** 1,067,371 rows × 8 columns
# - 📁 DataFrame name: `df_raw`
# 
# We will now proceed to inspect the structure of this combined dataset to better understand its format and prepare it for cleaning and transformation.
# 
# ---
# 

# ---
# 
# ## 🔍 Step 3: Basic Structure & Overview
# 
# Before performing any data transformations, we start by inspecting the **basic structure** of the combined dataset.  
# This step provides a snapshot of the data’s format, size, and overall quality.
# 
# We will review:
# - First and last few rows
# - Dataset shape (rows × columns)
# - Column names
# - Data types and non-null counts
# 
# This initial overview helps identify missing values, inconsistent types, or formatting issues early on.
# 
# ---
# 

# In[ ]:


import io

# ✅ Define display fallback for script environments
try:
    display
except NameError:
    def display(x):
        print(x.to_string() if isinstance(x, pd.DataFrame) else x)

# 🔍 Inspect basic structure of a DataFrame with optional row previews
def inspect_basic_structure(df, name="Dataset", preview_rows=5):
    """
    Display structure, sample rows, and schema of a DataFrame.
    Compatible with both notebooks and terminal scripts.
    """
    safe_print(f"🧾 Inspecting: {name}")
    safe_print("=" * 60)

    # 👁️ Preview first N rows
    safe_print(f"🔹 First {preview_rows} Rows:")
    display(df.head(preview_rows))

    # 👁️ Preview last N rows
    safe_print(f"\n🔹 Last {preview_rows} Rows:")
    display(df.tail(preview_rows))

    # 📐 Dataset shape
    safe_print(f"\n🔹 Shape: {df.shape[0]} rows × {df.shape[1]} columns")

    # 🏷️ Column names
    safe_print("\n🔹 Column Names:")
    safe_print(df.columns.tolist())

    # 🧬 Data types and non-null counts
    safe_print("\n🔹 Data Types and Non-Null Counts:")
    buffer = io.StringIO()
    df.info(buf=buffer)
    safe_print(buffer.getvalue())

    safe_print("=" * 60 + "\n")

# 🔎 Apply inspection to the combined dataset
inspect_basic_structure(df_raw, name="Online Retail II - Raw Combined Dataset")


# ---
# 
# ### 📊 Initial Observations
# 
# The **Online Retail II dataset** has been successfully loaded and merged, resulting in **1,067,371 rows** and **8 columns**.
# 
# Key findings from the initial inspection:
# 
# - ✅ **Time span**: Data ranges from **December 1, 2009** to **December 9, 2011**.
# - ✅ **Structure**: Each row appears to represent an item-level transaction (not invoice-level).
# - ✅ **Missing data**:
#   - `Description` is missing in ~4,382 rows
#   - `Customer ID` is missing in ~243,000 rows (∼23% of the data)
# - ❗ **Column names** contain spaces and should be standardized to snake_case for consistency.
# - ✅ **Data types**:
#   - `InvoiceDate` is correctly parsed as `datetime`
#   - `Quantity` and `Price` are numeric and suitable for calculation
# 
# In the next step, we’ll:
# - Rename columns to snake_case
# - Drop rows with missing `Customer ID` (to support reliable customer segmentation)
# - Continue cleaning the dataset for further transformation
# 
# ---
# 

# ---
# 
# ## ✏️ Step 4: Column Renaming & Standardization
# 
# To follow best practices in data preparation, we will standardize all column names using **`snake_case`** and remove any embedded whitespace. This improves readability and compatibility across tools like pandas, SQL, and Tableau.
# 
# Below is a comparison of the original column names and their new standardized equivalents:
# 
# | Original Column     | Renamed Column    |
# |---------------------|-------------------|
# | `Invoice`           | `invoice_no`      |
# | `StockCode`         | `stock_code`      |
# | `Description`       | `description`     |
# | `Quantity`          | `quantity`        |
# | `InvoiceDate`       | `invoice_date`    |
# | `Price`             | `unit_price`      |
# | `Customer ID`       | `customer_id`     |
# | `Country`           | `country`         |
# 
# After renaming, we will preview the new column names to confirm the update was successful.
# 
# ---
# 

# In[ ]:


# 🔧 Rename columns to snake_case and remove spaces
df_raw.columns = [
    'invoice_no',
    'stock_code',
    'description',
    'quantity',
    'invoice_date',
    'unit_price',
    'customer_id',
    'country'
]

# ✅ Confirm updated column names
safe_print("✅ Columns renamed successfully:")
safe_print(df_raw.columns.tolist())


# ---
# 
# ## 🧩 Step 5: Initial Variable Exploration
# 
# Before classifying columns as **quantitative**, **categorical**, or **identifiers**, we explore:
# 
# - The number of **unique values** in each column
# - A preview of the first few **distinct values** per column
# 
# This helps us:
# - Identify numeric columns that behave as **IDs** (e.g., `invoice_no`, `stock_code`)
# - Detect potential **categorical features** based on low cardinality
# - Flag columns like `country` and `description` for standardization or grouping
# 
# ---
# 

# In[ ]:


def explore_unique_values(df, name="Dataset"):
    # 🔍 Begin unique value exploration
    safe_print(f"🔍 Unique Value Exploration for: {name}")
    safe_print("=" * 70)

    for col in df.columns:
        unique_vals = df[col].dropna().unique()
        num_unique = len(unique_vals)
        sample_vals = unique_vals[:5]

        safe_print(f"📌 Column: {col}")
        safe_print(f"   • Unique values: {num_unique}")
        safe_print(f"   • Sample values: {sample_vals}")

        if pd.api.types.is_numeric_dtype(df[col]) and num_unique < 15:
            safe_print("   ⚠️  Warning: Numeric column with few unique values (may be categorical)")

        safe_print("-" * 70)

# 🔎 Apply to raw dataset
explore_unique_values(df_raw, name="Online Retail II – Raw Combined Dataset")


# ---
# 
# ### 🧾 Summary of Initial Variable Exploration
# 
# The dataset includes a diverse mix of **identifiers**, **quantitative metrics**, and **categorical variables**. Here are the key takeaways:
# 
# - 🧾 `invoice_no` and `stock_code` are **identifiers**, not meant for numerical operations.
# - 🧠 `description` has ~5.7K unique values, some of which may include extra whitespace or inconsistent casing.
# - 🧮 `quantity` and `unit_price` are **numeric** fields that will be used to compute revenue.
# - 📅 `invoice_date` is in `datetime64` format — ✅ correctly parsed.
# - 👤 `customer_id` has 5.9K unique customers but **many missing values** (to be handled soon).
# - 🌍 `country` contains **43 unique values** — we’ll check which countries appear most frequently in the next step.
# 
# Next, we will:
# - Classify these columns into **identifiers, categorical, quantitative, or datetime**
# - Begin filtering invalid rows (e.g., quantity or unit price ≤ 0)
# - Handle missing and duplicate data
# 
# ---
# 

# ---
# 
# ## 🧩 Step 6: Classifying Variables
# 
# Based on our unique value exploration, we now classify each column in the Online Retail II dataset into one of the following categories:
# 
# - **📊 Quantitative**: Numeric variables used for calculations or aggregation
# - **🔤 Categorical**: Discrete labels or groups
# - **📅 Datetime**: Columns containing timestamps or dates
# - 🆔 **Identifiers**: Unique values used to join or track records (not used for analysis)
# 
# ---
# 
# ### 📄 `df_raw` — Online Retail II Dataset
# 
# | Column Name     | Variable Type |
# |------------------|----------------|
# | `invoice_no`     | Identifier     |
# | `stock_code`     | Identifier     |
# | `description`    | Categorical    |
# | `quantity`       | Quantitative   |
# | `invoice_date`   | Datetime       |
# | `unit_price`     | Quantitative   |
# | `customer_id`    | Identifier     |
# | `country`        | Categorical    |
# 
# ---
# 
# This classification will guide:
# - 🧹 Data type conversions
# - 📊 Summary statistics
# - 📈 Visualizations
# - 🧮 RFM metric calculations
# 
# ---
# 

# In[ ]:


# 🧠 Define variable classifications for the Online Retail II dataset
variable_types = {
    'online_retail_ii': {
        'quantitative': ['quantity', 'unit_price'],
        'categorical': ['description', 'country'],
        'datetime': ['invoice_date'],
        'identifier': ['invoice_no', 'stock_code', 'customer_id']
    }
}

safe_print("✅ Variable classification completed for online_retail_ii dataset.")


# ---
# 
# ## 🕓 Step 7: Preview Invoice Date Range
# 
# We check the **earliest** and **latest** values in the `invoice_date` column to understand the full time span covered by the dataset.
# 
# This helps us confirm the historical coverage and provides context for later analysis grouped by month or year.
# 
# ---
# 

# In[ ]:


# ⏳ Check date range of invoice timestamps
min_date = df_raw['invoice_date'].min()
max_date = df_raw['invoice_date'].max()

safe_print(f"🕐 Earliest invoice date: {min_date}")
safe_print(f"🕙 Latest invoice date:   {max_date}")


# ---
# 
# ### 📆 Invoice Date Range Confirmed
# 
# The dataset spans from **December 1, 2009** to **December 9, 2011**, covering **two full years of transactions**.  
# This confirms the historical scope is consistent with expectations and provides a solid foundation for time-based analysis, such as:
# 
# - Monthly revenue trends
# - Customer acquisition by cohort
# - Recency calculations in RFM segmentation
# 
# We’ll now proceed to filter out any invalid or suspicious records based on quantity and price.
# 
# ---
# 

# ---
# 
# ## 🧹 Step 8: Filter Invalid Transactions
# 
# We now remove rows with clearly invalid or non-useful values:
# 
# - `quantity <= 0`: Often indicates a return or input error
# - `unit_price <= 0`: Invalid for revenue calculations
# 
# These rows can distort sales figures and will be excluded from the cleaned dataset.  
# Later, we may revisit negative quantities separately to analyze returns or cancellations.
# 
# ---
# 

# In[ ]:


# 🧹 Filter out rows with invalid quantity or price
initial_shape = df_raw.shape

df_raw = df_raw[(df_raw['quantity'] > 0) & (df_raw['unit_price'] > 0)]

# ✅ Show change in dataset size
safe_print(f"🧮 Rows before filtering: {initial_shape[0]}")
safe_print(f"✅ Rows after filtering:  {df_raw.shape[0]}")
safe_print(f"➖ Rows removed:          {initial_shape[0] - df_raw.shape[0]}")


# ---
# 
# ### 🧹 Invalid Transactions Removed
# 
# A total of **25,700 rows** were removed due to invalid values in `quantity` or `unit_price`.
# 
# - ✅ Final dataset shape: **1,041,671 rows**
# - These records are now clean and ready for downstream transformation and analysis.
# - We'll address additional edge cases (like cancellations and missing values) in the next steps.
# 
# ---
# 

# ---
# 
# ## 🔁 Step 9: Identify and Remove Canceled Invoices
# 
# We now check whether any remaining rows have `invoice_no` values that begin with the letter `'C'`.  
# These represent **canceled transactions**, typically used to reverse or correct previous purchases.
# 
# > 🔍 Most canceled transactions were **already removed** earlier in the cleaning process, when we filtered for:
# > - `quantity > 0`  
# > - `unit_price > 0`  
# >
# > That’s because canceled rows almost always have **negative quantities**, which were excluded in Step 8.
# 
# However, a small number of rows may still remain with a `'C'` prefix and valid quantity/price values — for example, if a cancellation included a partial restock or adjustment.
# 
# To ensure consistency and avoid skewing future analysis (such as revenue or customer frequency), we will:
# - ✅ Identify any remaining canceled invoices
# - ✅ Remove them from the dataset
# 
# ---
# 

# In[ ]:


# 🔍 Check for remaining canceled transactions
canceled_mask = df_raw['invoice_no'].astype(str).str.startswith('C')
num_canceled_remaining = canceled_mask.sum()

safe_print(f"🚫 Rows with invoice_no starting with 'C': {num_canceled_remaining}")

# 🧹 Remove them if any remain
if num_canceled_remaining > 0:
    df_raw = df_raw[~canceled_mask]
    safe_print("✅ Canceled invoices removed.")
else:
    safe_print("✅ No canceled invoices found — all previously filtered.")


# ---
# 
# ### ✅ Canceled Invoices Removed
# 
# Only **1 row** with an invoice number starting with `'C'` remained in the dataset after filtering for positive `quantity` and `unit_price`.  
# This row has now been removed to ensure the dataset contains only **confirmed sales**.
# 
# With cancellations and invalid transactions fully excluded, the data is now ready for handling missing values.
# 
# ---
# 

# ---
# 
# ## 🚫 Step 10: Handle Missing `customer_id` Values
# 
# The `customer_id` column is essential for any customer-level analysis, including:
# 
# - 📊 Calculating repeat purchase behavior
# - 💰 Aggregating spend per customer
# - 🧠 Performing RFM segmentation
# 
# However, around **23% of the dataset** is missing `customer_id`. These are likely anonymous or incomplete transactions that **cannot be tied to specific customers**, so we will remove them from the dataset.
# 
# Removing these rows ensures that all remaining records are suitable for **customer-centric metrics and segmentation**.
# 
# ---
# 

# In[ ]:


# 🚫 Drop rows with missing customer_id
initial_shape = df_raw.shape

# Drop and convert in one chain with .copy() to avoid chained assignment warnings
df_raw = df_raw.dropna(subset=['customer_id']).copy()
df_raw['customer_id'] = df_raw['customer_id'].astype('int64')

# 🧾 Summary of effect
safe_print(f"🧮 Rows before dropping missing customer_id: {initial_shape[0]}")
safe_print(f"✅ Rows after dropping:                  {df_raw.shape[0]}")
safe_print(f"➖ Rows removed:                         {initial_shape[0] - df_raw.shape[0]}")


# ---
# 
# ### ✅ Missing `customer_id` Values Removed
# 
# A total of **236,121 rows** were removed due to missing `customer_id` values.  
# These records represent approximately **23%** of the full dataset and were likely anonymous or unregistered purchases.
# 
# Removing them ensures that all remaining transactions are tied to identifiable customers — a necessary condition for:
# - RFM segmentation
# - Customer retention analysis
# - Cohort or frequency-based metrics
# 
# The cleaned dataset now contains **805,549 rows** ready for customer-level aggregation.
# 
# ---
# 

# ---
# 
# ## 🧾 Step 11: Drop Rows with Missing `description`
# 
# Each transaction in the dataset should be linked to a valid product name via the `description` column.
# 
# Rows with missing descriptions:
# - Cannot be included in **product-level analysis**
# - Disrupt grouping and aggregation
# - Add ambiguity when exporting a clean `products` table
# 
# Since these rows typically make up a **very small portion** of the dataset, we will remove them before moving forward.
# 
# ---
# 

# In[ ]:


# 🧾 Drop rows with missing product description
initial_shape = df_raw.shape
df_raw = df_raw.dropna(subset=['description'])

# 🧾 Summary of effect
safe_print(f"🧮 Rows before dropping missing description: {initial_shape[0]}")
safe_print(f"✅ Rows after dropping:                     {df_raw.shape[0]}")
safe_print(f"➖ Rows removed:                            {initial_shape[0] - df_raw.shape[0]}")


# ---
# 
# ### ✅ No Missing Descriptions Remaining
# 
# Although the original dataset contained ~4,382 rows with missing values in the `description` column,  
# those rows were already removed earlier during previous cleaning steps, such as:
# 
# - Filtering out rows with `quantity <= 0` or `unit_price <= 0`
# - Removing canceled invoices
# - Dropping rows with missing `customer_id`
# 
# As a result, there are now **zero rows** missing product descriptions.
# 
# This ensures:
# - All remaining transactions are linked to a valid product
# - Grouping and aggregation by product name can proceed without issues
# - We can safely generate a clean `products.csv` in the export phase
# 
# ---
# 

# ---
# 
# ## 🔤 Step 12: Standardizing Categorical Values
# 
# To ensure consistent grouping, clean aggregations, and tidy exports, we now standardize key categorical columns by:
# 
# - Lowercasing all text
# - Stripping unwanted leading or trailing whitespace
# 
# This is especially important for:
# - Product-level analysis using `description`
# - Country-based revenue breakdown using `country`
# 
# 📌 We only apply this to **text-based categorical fields** — not identifiers like `stock_code`, `invoice_no`, or `customer_id`.
# 
# The columns to be standardized are:
# - `description`
# - `country`
# 
# ---
# 

# In[ ]:


# 🧼 Helper function to clean string-based categorical columns
def clean_categorical_column(df, col):
    """
    Standardizes a string-based categorical column:
    - Lowercases text
    - Strips leading/trailing whitespace
    """
    df[col] = df[col].astype(str).str.lower().str.strip()
    safe_print(f"🧼 Cleaned column: {col}")

# 🧼 Apply to selected columns
clean_categorical_column(df_raw, 'description')
clean_categorical_column(df_raw, 'country')

# 🔍 Preview cleaned values
safe_print("\n🔍 Sample cleaned descriptions:")
display(df_raw['description'].drop_duplicates().sort_values().head())

safe_print("\n🌍 Unique countries after standardization:")
safe_print(sorted(df_raw['country'].unique()))


# ---
# 
# ### ✅ Categorical Values Standardized
# 
# The following text-based columns were successfully cleaned:
# 
# - `description`: Lowercased and stripped of extra whitespace  
# - `country`: Lowercased to standardize for grouping and sorting
# 
# 🔍 **Sample cleaned product descriptions:**
# - `10 colour spaceboy pen`
# - `12 ass zinc christmas decorations`
# - `12 daisy pegs in wood box`
# 
# 🌍 **Unique countries (standardized):**
# 43 unique values including:
# - `united kingdom`, `germany`, `france`, `spain`, `usa`, `australia`, `sweden`, `netherlands`, `unspecified`
# 
# These clean categorical values will ensure consistency when:
# - Grouping by product or country
# - Creating relational product and customer tables
# - Building clear visualizations or dashboards
# 
# ---
# 

# ---
# 
# ## 🆔 Step 13: Normalize Identifier Columns
# 
# We now ensure all key identifier columns are stored with the appropriate data types for reliable aggregation, joining, and exporting:
# 
# - `invoice_no` → Cast to **string** (alphanumeric, may include leading zeros)
# - `stock_code` → Cast to **string** (alphanumeric product code)
# - `customer_id` → Already converted to **integer** in Step 10 (numeric-only, used in grouping and segmentation)
# 
# Although canceled invoices (which started with `'C'`) have already been removed, treating `invoice_no` as a string is still good practice to prevent data type issues when saving or displaying.
# 
# This normalization step improves:
# - Consistency across exports
# - Compatibility with SQL schema and BI tools
# - Safety during joins and merges
# 
# ---
# 

# In[ ]:


# 🆔 Normalize identifier column formats

# ✅ Convert to string and strip whitespace
df_raw['invoice_no'] = df_raw['invoice_no'].astype(str).str.strip()
df_raw['stock_code'] = df_raw['stock_code'].astype(str).str.strip()

# customer_id already converted to int in Step 10

# 🧾 Confirm resulting dtypes
safe_print("\n🔍 Identifier column data types:")
safe_print(df_raw[['invoice_no', 'stock_code', 'customer_id']].dtypes)

# 🖼️ Preview sample values
safe_print("\n🔢 Sample identifier values:")
display(df_raw[['invoice_no', 'stock_code', 'customer_id']].head())


# ---
# 
# ### ✅ Identifier Columns Normalized
# 
# All key identifiers have been successfully standardized:
# 
# - `invoice_no` → Stored as **string**
# - `stock_code` → Stored as **string**
# - `customer_id` → Stored as **integer**
# 
# This ensures consistent formatting across joins, exports, and future relational modeling.
# 
# 🔢 Sample values:
# - `invoice_no`: `489434`
# - `stock_code`: `85048`, `79323P`, `21232`
# - `customer_id`: `13085`
# 
# The dataset is now fully prepared for deduplication and export.
# 
# ---
# 

# ---
# 
# ## 🧹 Step 14: Check and Remove Duplicate Rows
# 
# We now inspect the dataset for any **fully duplicated rows** — records where every column value is exactly the same.
# 
# This can happen due to:
# - System ingestion issues
# - Accidental row duplication
# - Redundant merges during data prep
# 
# We'll first check for:
# - Total number of exact duplicates
# - (Optional) Duplicated values in a key column, such as `invoice_no`
# 
# If duplicates are found, we will retain only the **first occurrence** of each row.
# 
# ---
# 

# In[ ]:


# 🧩 Reuse helper function to inspect duplicates
def check_duplicates(df, key_column=None, name="Dataset", preview=False):
    safe_print(f"🔁 Checking Duplicates in: {name}")
    safe_print("=" * 60)

    # 🔍 Count fully duplicated rows
    total_dupes = df.duplicated().sum()
    safe_print(f"📋 Total fully duplicated rows: {total_dupes}")

    # 🖼️ Preview full duplicates if requested
    if total_dupes > 0 and preview:
        safe_print("\n🔎 Sample duplicated rows:")
        display(df[df.duplicated()].head())

    # 🔍 Duplicate check for key column
    if key_column:
        id_dupes = df[key_column].duplicated().sum()
        safe_print(f"🆔 Duplicated values in key column `{key_column}`: {id_dupes}")

        if id_dupes > 0 and preview:
            safe_print("\n🔎 Sample rows with duplicate IDs:")
            display(df[df[key_column].duplicated(keep=False)].head())
    else:
        safe_print("⚠️ No key column specified for duplicate ID check.")

    safe_print("=" * 60 + "\n")

# 🔍 Check duplicates in full dataset and optionally in invoice_no
check_duplicates(df_raw, key_column="invoice_no", name="Online Retail II", preview=True)

# 🧹 Remove full row duplicates
initial_shape = df_raw.shape
df_raw = df_raw.drop_duplicates()
safe_print(f"✅ Duplicates removed: {initial_shape[0] - df_raw.shape[0]}")
safe_print(f"📦 Final row count: {df_raw.shape[0]}")


# ---
# 
# ### ✅ Duplicate Rows Removed
# 
# A total of **26,124 fully duplicated rows** were found and removed from the dataset.  
# These were rows where **every column matched exactly** — likely caused by accidental system duplication or data merging issues.
# 
# 📦 Final dataset shape after deduplication: **779,425 rows**
# 
# 🔁 Note on `invoice_no`:
# - Over **768,000 invoice numbers** are repeated — this is expected.
# - Each invoice can have **multiple rows** (one per product line), so `invoice_no` is not unique and should not be used as a primary key.
# 
# With this step complete, the dataset is now fully cleaned and prepared for:
# - Revenue calculations
# - RFM segmentation
# - Exporting to relational tables
# 
# ---
# 

# ---
# 
# ## 💰 Step 15: Validate Revenue Calculation (`line_revenue`)
# 
# We now compute a new column, `line_revenue`, which represents the revenue generated per transaction row:
# 
# > `line_revenue = quantity × unit_price`
# 
# This value will be used in:
# - Revenue aggregation per invoice
# - Customer spend analysis
# - RFM monetary scoring
# - Exporting `invoice_items.csv`
# 
# We'll also verify that the calculated values look correct by inspecting a few sample rows.
# 
# ---
# 

# In[ ]:


# 💰 Add a new column: line_revenue
# Avoid SettingWithCopyWarning by ensuring df_raw is not a view
if 'line_revenue' not in df_raw.columns:
    df_raw = df_raw.copy()
    df_raw.loc[:, 'line_revenue'] = df_raw['quantity'] * df_raw['unit_price']

# ✅ Preview some calculated values
safe_print("\n💸 Preview of calculated line_revenue:")
display(df_raw[['invoice_no', 'stock_code', 'quantity', 'unit_price', 'line_revenue']].head())

# 📊 Summary statistics for line_revenue
safe_print("\n📊 Summary of line_revenue column:")
safe_print(df_raw['line_revenue'].describe())


# ---
# 
# ### ✅ Revenue Column Validated
# 
# A new column, `line_revenue`, has been successfully calculated for each transaction row:
# 
# > `line_revenue = quantity × unit_price`
# 
# 📊 Summary of `line_revenue`:
# - **Min**: £0.001  
# - **Max**: £168,469.60  
# - **Median**: £12.48  
# - **Mean**: ~£22.29  
# - **Std Dev**: High, due to large wholesale orders
# 
# 🔍 Sample rows confirm accurate revenue calculations across typical transactions (e.g., `quantity × unit_price`).
# 
# This field will be used throughout the analysis and when exporting `invoice_items.csv`.
# 
# ---
# 

# ---
# 
# ## 🧪 Step 16: Data Type Sanity Check (Pre-Export)
# 
# Before exporting the cleaned dataset into relational tables, we verify that all columns have the correct data types.
# 
# This sanity check ensures:
# - Identifiers (`invoice_no`, `stock_code`, `customer_id`) are in string or integer format
# - Quantities and prices are numeric
# - Dates are properly parsed as datetime
# - No unexpected object or float types in critical fields
# 
# Performing this check now helps avoid errors when writing to CSV, importing into SQL, or building dashboards.
# 
# ---
# 

# In[ ]:


# ✅ Sanity Check

# Define expected data types for validation
expected_dtypes = {
    'invoice_no': 'object',
    'stock_code': 'object',
    'description': 'object',
    'quantity': 'int64',
    'invoice_date': 'datetime64[ns]',
    'unit_price': 'float64',
    'line_revenue': 'float64',
    'customer_id': 'int64',
    'country': 'object'
}

safe_print("\n🧪 Column Type Sanity Check:")
type_mismatches = []

# Compare actual vs expected types
for col, expected_type in expected_dtypes.items():
    if col in df_raw.columns:
        actual_type = df_raw[col].dtype
        if actual_type != expected_type:
            type_mismatches.append((col, expected_type, actual_type))
            safe_print(f"⚠️ Mismatch: {col} → Expected: {expected_type}, Got: {actual_type}")
        else:
            safe_print(f"✅ {col} → {actual_type}")

# Summary check
if type_mismatches:
    safe_print("\n❌ Type mismatches detected. Fix before exporting.")
    raise TypeError("Type mismatches detected. See output above.")
else:
    safe_print("\n✅ All column types are valid. Ready for export.")


# ---
# 
# ### ✅ Column Types Validated
# 
# All columns passed the data type sanity check:
# 
# | Column         | Type           |
# |----------------|----------------|
# | `invoice_no`   | object (string)|
# | `stock_code`   | object (string)|
# | `description`  | object (string)|
# | `quantity`     | int64          |
# | `invoice_date` | datetime64[ns] |
# | `unit_price`   | float64        |
# | `line_revenue`  | float64        |
# | `customer_id`  | int64          |
# | `country`      | object (string)|
# 
# The dataset is now fully ready for clean export into normalized relational tables.
# 
# ---
# 

# ## 🧩 Step 17: Remove Non-Product Stock Codes
# 
# During manual inspection of the original dataset (`online_retail_II.xlsx`), we identified several `stock_code` entries that do **not represent physical products**. These include:
# 
# - Charges (e.g., `POST`, `BANK CHARGES`)
# - Manuals (e.g., `M`)
# - Shipping fees (e.g., `C2`, `DOT`)
# - Special handling lines (e.g., `CARRIAGE`, `ADJUST`)
# 
# These entries **do not reflect inventory items** and could distort product-level and customer-level analyses. We remove them at this stage to ensure a clean, product-focused dataset.
# 
# > ⚠️ These codes were identified through domain knowledge and manual review, not discovered algorithmically.
# 
# ---

# In[ ]:


# ❌ Known non-product stock codes (manually flagged)
non_product_codes = [
    'POST', 'D', 'DOT', 'M', 'BANK CHARGES', 'ADJUST',
    'CARRIAGE', 'AMAZONFEE', 'S', 'CRUK', 'C2'
]

# 🧹 Filter out rows with non-product codes
before_rows = df_raw.shape[0]
df_raw = df_raw[~df_raw['stock_code'].isin(non_product_codes)].copy()
after_rows = df_raw.shape[0]

# 📉 Rows removed
safe_print(f"🧹 Removed non-product stock codes.")
safe_print(f"➖ Rows before: {before_rows}")
safe_print(f"➕ Rows after:  {after_rows}")
safe_print(f"📉 Rows removed: {before_rows - after_rows}")


# ---
# 
# ### ✅ Summary: Removal of Non-Product Stock Codes
# 
# We removed **2,816 rows** from the dataset that corresponded to **non-product stock codes**, such as `'POST'`, `'M'`, `'CARRIAGE'`, and other administrative or service-related codes.
# 
# These rows do not represent physical inventory and were excluded to ensure that:
# 
# - 📦 All remaining rows reflect **tangible retail products**
# - 💰 Revenue metrics are based on **actual item sales**
# - 📊 Product- and customer-level analyses remain **clean and interpretable**
# 
# This cleaning step improves the quality of product performance metrics and ensures the integrity of subsequent analyses, such as top-selling products, customer behavior, and segmentation modeling.
# 
# > 🔍 This filtering was informed by **manual inspection** of `online_retail_II.csv` and domain-specific judgment about which stock codes are valid for product-level analysis.
# 
# ---

# ---
# 
# ## 🔍 Step 18: Check for Inconsistent Product Descriptions
# 
# In preparation for accurate product-level analysis, we assess whether each `stock_code` is consistently associated with a single `description`. Inconsistent descriptions can lead to mismatches between SQL and EDA outputs — particularly in product rankings and revenue summaries.
# 
# This diagnostic step helps us identify potential discrepancies before exporting the cleaned data and normalized tables.
# 
# ---

# In[ ]:


# 🔍 Check for inconsistent product descriptions (important for EDA validation)
desc_counts = df_raw.groupby('stock_code')['description'].nunique().reset_index()
inconsistent_desc = desc_counts[desc_counts['description'] > 1]

# 🔢 Report findings
safe_print(f"❗ Found {inconsistent_desc.shape[0]} stock codes with inconsistent descriptions in cleaned dataset.")

# 💬 View examples
multi_desc_sample = (
    df_raw[df_raw['stock_code'].isin(inconsistent_desc['stock_code'])]
    [['stock_code', 'description']]
    .drop_duplicates()
    .sort_values(by='stock_code')
)

display(multi_desc_sample.head(20))


# ---
# 
# We identified **597 stock codes** with inconsistent product descriptions. This means some stock codes appear with multiple descriptions, such as:
# 
# - `15058A`: `"blue white spots garden parasol"` and `"blue polkadot garden parasol"`
# - `16161U`: `"wrap suki and friends"` and `"wrap,suki and friends"`
# - `17107D`: `"flower fairy 5 drawer liners"` and `"flower fairy,5 summer b'draw liners"`
# 
# These inconsistencies can fragment revenue metrics and make it harder to match SQL and EDA outputs. We will address this issue before exporting the relational tables.
# 

# ---
# 
# ### ✅ Summary: Inconsistent Product Descriptions
# 
# We identified **597 stock codes** in the cleaned dataset that are associated with **more than one product description**. For example:
# 
# - `15058A`: `"blue white spots garden parasol"` vs. `"blue polkadot garden parasol"`
# - `16161U`: `"wrap suki and friends"` vs. `"wrap,suki and friends"`
# - `17107D`: `"flower fairy 5 drawer liners"` vs. `"flower fairy,5 summer b'draw liners"`
# 
# These inconsistencies can lead to inaccurate product-level aggregation in EDA and cause mismatches with SQL results, where only one description per `stock_code` is typically retained.
# 
# This diagnostic step ensures we are aware of description variability and allows us to resolve it prior to exporting the relational tables, improving the integrity of product-level metrics across both Python and SQL workflows.
# 
# > 🛠️ We will standardize descriptions by using the **most frequent description per stock code** to maintain consistency in the normalized data model.
# 
# ---
# 

# ---
# 
# ## 🧼 Step 19: Standardize Product Descriptions
# 
# To resolve the inconsistencies found in the previous step, we will standardize product descriptions by selecting the **most frequent description** for each `stock_code`.
# 
# This ensures:
# 
# - 🧾 Each stock code maps to **one consistent description**
# - 📊 Product-level aggregation remains accurate in both **EDA and SQL workflows**
# - 🧩 The relational `products` table contains unique and interpretable entries
# 
# We apply this fix **before exporting** the normalized tables to ensure that all downstream analysis uses the standardized version.
# 
# ---

# In[ ]:


# 🔁 Create mapping from stock_code to most frequent description
desc_mode_map = (
    df_raw.groupby(['stock_code', 'description'])
    .size()
    .reset_index(name='count')
    .sort_values(['stock_code', 'count'], ascending=[True, False])
    .drop_duplicates('stock_code')
    .set_index('stock_code')['description']
)

# 🛠️ Apply mapping to replace all descriptions with the most frequent one
df_raw['description'] = df_raw['stock_code'].map(desc_mode_map)

# ✅ Check for remaining inconsistencies
desc_counts_after = df_raw.groupby('stock_code')['description'].nunique().reset_index()
inconsistent_desc_after = desc_counts_after[desc_counts_after['description'] > 1]

# 🔍 Show sample if issues remain (they shouldn't)
if not inconsistent_desc_after.empty:
    sample_remaining = (
        df_raw[df_raw['stock_code'].isin(inconsistent_desc_after['stock_code'])]
        [['stock_code', 'description']]
        .drop_duplicates()
        .sort_values('stock_code')
    )
    display(sample_remaining.head(10))

safe_print(f"✅ Standardized descriptions for {desc_mode_map.shape[0]} stock codes.")
safe_print(f"✅ Remaining stock codes with inconsistent descriptions after standardizing: {inconsistent_desc_after.shape[0]}")


# ---
# 
# ### ✅ Summary: Description Standardization Applied
# 
# We standardized descriptions for **all stock codes** by mapping each to its **most frequently used description**.
# 
# - 📉 Before: 597 stock codes had conflicting product names
# - ✅ After: All stock codes now have a **single consistent description**
# - 🧾 This ensures accurate aggregation for EDA and SQL metrics involving product-level analysis
# 
# This correction was applied **before exporting the relational tables**, which avoids mismatches in product performance metrics between the two environments.
# 
# ---

# ---
# 
# ## 🔍 Step 20 – Relational Integrity Preview
# 
# Before exporting the flat cleaned dataset and creating normalized relational tables, we validate the integrity of potential primary keys for:
# 
# - `customers` → `customer_id`
# - `products` → `stock_code`
# - `invoices` → `invoice_no`
# - `invoice_items` → (`invoice_no`, `stock_code`)
# 
# These checks ensure each key column or composite key uniquely identifies records, as required in a relational schema.
# 
# ---

# In[ ]:


# Relational Integrity Preview

safe_print("🔎 Checking future relational primary key constraints...\n")

# 1. customer_id should map to exactly one country
multi_country_customers = (
    df_raw.groupby('customer_id')['country']
    .nunique()
    .reset_index()
    .query('country > 1')
)
safe_print(f"🧾 customer_id → country: {multi_country_customers.shape[0]} with >1 country")

# 2. stock_code should map to one description
multi_desc_products = (
    df_raw.groupby('stock_code')['description']
    .nunique()
    .reset_index()
    .query('description > 1')
)
safe_print(f"📦 stock_code → description: {multi_desc_products.shape[0]} with >1 description")

# 3. invoice_no should be unique per customer-date combo
invoice_dupes = df_raw[['invoice_no', 'invoice_date', 'customer_id']].duplicated().sum()
safe_print(f"🧾 invoice_no: {invoice_dupes} duplicated invoice entries")

# 4. invoice_items composite key
composite_dupes = df_raw[['invoice_no', 'stock_code']].duplicated().sum()
safe_print(f"🧾 invoice_items: {composite_dupes} duplicated (invoice_no, stock_code) pairs")


# ---
# 
# ### 🔍 Relational Integrity Summary
# 
# To ensure that the future relational tables meet primary key and foreign key constraints before export, we evaluated the consistency of key fields based on the expected SQL schema:
# 
# - **`customer_id` → `country`**: ❗ Found **12** customer IDs linked to more than one country. This violates the expected one-to-one relationship and may indicate entry inconsistencies (e.g., customers ordering from multiple shipping locations or data entry errors).
# - **`stock_code` → `description`**: ✅ No mismatches detected. Each product ID consistently maps to a single product description, as expected after the standardization step.
# - **`invoice_no`**: ❗ Found **739,938** duplicate invoice entries (not necessarily problematic yet, but warrants verification if `invoice_no` was expected to be unique on its own).
# - **`invoice_items` composite key (`invoice_no`, `stock_code`)**: ❗ Found **10,498** duplicate pairs. These may result from quantity-based repetitions or entry errors and need to be resolved to enforce a composite primary key in the SQL schema.
# 
# > These issues will be addressed in the next step to ensure that all exported relational tables meet the necessary uniqueness and referential integrity constraints required for MySQL insertion.
# 
# ---

# ---
# 
# ## 🧪 Step 21: Exploring Detected Integrity Issues
# 
# Before fixing the relational key violations identified earlier, we explore the nature of these issues to guide appropriate correction strategies.
# 
# ---
# 

# ### 🌍 Step 21.1a Mapping Countries per Customer
# 
# Now that we’ve identified 12 `customer_id` values linked to more than one `country`, we want to confirm **which countries** are associated with each of them.
# 
# This helps:
# - Understand if the differences are minor (e.g., case sensitivity or whitespace issues)
# - Decide how to resolve the inconsistency (e.g., keep the most common country or prioritize a specific one)
# 
# ---

# In[ ]:


# 🔍 See which countries are associated with each problematic customer_id
country_combinations = (
    df_raw[df_raw['customer_id'].isin(multi_country_customers['customer_id'])]
    .groupby('customer_id')['country']
    .apply(lambda x: sorted(x.unique()))
    .reset_index()
    .rename(columns={'country': 'countries'})
)

safe_print("📋 Customers and their associated countries:")
display(country_combinations)


# ---
# 
# ### 🧾 Summary of Country Mismatches per Customer
# 
# We identified **12 customers** linked to more than one country. These mismatches likely reflect inconsistencies in how country data was recorded rather than true multiple residencies. For example:
# 
# - `customer_id = 12422` is linked to both **Australia** and **Switzerland**
# - `customer_id = 12370` appears under both **Austria** and **Cyprus**
# 
# These conflicts must be resolved before exporting the `customers` table to ensure the `customer_id` field can act as a **valid primary key**.
# 
# In the next step, we will decide how to resolve these mismatches — for example, by keeping the **most frequent country per customer** or by using the **latest invoice record**.
# 
# ---

# ---
# 
# ### 🧮 Step 21.1b Country Frequency and Latest Assignment per Customer
# 
# To better understand the inconsistencies in country assignments, we perform a three-part analysis for each conflicting `customer_id`:
# 
# 1. Count how many times each country appears
# 2. Identify the most frequent (mode) country
# 3. Identify the most recent country based on invoice date
# 
# This information helps determine whether discrepancies are due to data entry errors or reflect valid changes in customer behavior.
# 
# ---

# In[ ]:


# ✅ Subset to conflicting customers
conflicting_df = df_raw[df_raw['customer_id'].isin(multi_country_customers['customer_id'])]

# 📋 Count how many times each country appears per customer_id
country_counts = (
    conflicting_df
    .groupby(['customer_id', 'country'])
    .size()
    .reset_index(name='count')
    .sort_values(['customer_id', 'count'], ascending=[True, False])
)

safe_print("📊 Country counts for each conflicting customer_id:")
display(country_counts)

# 📊 Most frequent (mode) country per customer_id
country_mode = (
    country_counts
    .drop_duplicates('customer_id')
    .rename(columns={'country': 'most_frequent_country'})
    [['customer_id', 'most_frequent_country']]
)

# 🕓 Most recent (latest) country per customer_id
latest_country = (
    conflicting_df
    .sort_values('invoice_date')
    .groupby('customer_id', as_index=False)
    .last()[['customer_id', 'country']]
    .rename(columns={'country': 'latest_country'})
)

# 🔗 Merge mode and latest country
country_resolution_df = pd.merge(country_mode, latest_country, on='customer_id')

safe_print("📋 Summary of most frequent vs. latest country per customer_id:")
display(country_resolution_df)


# ---
# 
# ### 📝 Insights from Country Comparison
# 
# The table above highlights customers who were associated with **multiple countries** in the dataset. We examined both:
# 
# - **Most Frequent Country**: The country that appears most often in transactions for each customer.
# - **Latest Country**: The country associated with the most recent invoice for that customer.
# 
# In most cases, the frequent and latest countries match, suggesting consistent data. However, a few mismatches (e.g., `customer_id` 12394, 12422, 12455, and 12457) raise questions about potential:
# 
# - **Data entry errors**
# - **Multiple shipping addresses per customer**
# - **Merged customer IDs or system tracking inconsistencies**
# 
# These discrepancies should be resolved before exporting the relational `customers` table. In the next step, we will decide how to handle these conflicting records—either by assigning a consistent country or excluding ambiguous entries.
# 
# ---

# ---
# 
# ### 🛠️ Step 21.1c Resolving Conflicting Country Assignments per Customer
# 
# We previously identified 12 `customer_id`s associated with more than one country, which violates the one-to-one mapping expected for our `customers` table in the relational schema.
# 
# To resolve this, we will enforce consistency by assigning each `customer_id` its **most frequent (mode) country** across all transactions. This approach helps preserve data volume and aligns with the likely default shipping location or business origin of the customer.
# 
# Once the correction is applied, we will revalidate the mapping to ensure that every customer has a single, consistent country assignment.
# 
# ---

# In[ ]:


# ✅ Create a mapping of most frequent country per customer_id
most_frequent_country = (
    df_raw.groupby(['customer_id', 'country'])
    .size()
    .reset_index(name='count')
    .sort_values(['customer_id', 'count'], ascending=[True, False])
    .drop_duplicates('customer_id')
    .set_index('customer_id')['country']
)

# ✅ Overwrite 'country' in df_raw using the most frequent country per customer
df_raw['country'] = df_raw['customer_id'].map(most_frequent_country).fillna(df_raw['country'])

# 🔍 Recheck if any customer_id is still linked to more than one country
remaining_issues = (
    df_raw.groupby('customer_id')['country']
    .nunique()
    .reset_index()
    .query('country > 1')
)

safe_print(f"✅ Country assignment conflicts remaining: {remaining_issues.shape[0]}")


# ---
# 
# ### ✅ Country Conflict Resolution Complete
# 
# We have successfully reassigned each `customer_id` to its most frequently associated country. This resolved the 12 conflicting cases and ensures a one-to-one relationship between customers and countries, which is required for enforcing primary key constraints in the future `customers` table.
# 
# No `customer_id` is now linked to more than one country in the dataset. We can confidently proceed with the relational table creation and export process.
# 
# ---
# 

# ---
# 
# ### 🔍 Step 21.2 Rechecking `stock_code` → `description` Consistency
# 
# To ensure that the future `products` table maintains integrity, we verify whether each `stock_code` is consistently associated with a single `description`. This step is necessary because duplicate or conflicting product descriptions could violate SQL uniqueness constraints.
# 
# ---
# 

# In[ ]:


# 🔍 Count number of unique descriptions per stock_code
desc_counts = (
    df_raw.groupby('stock_code')['description']
    .nunique()
    .reset_index(name='unique_descriptions')
)

# 🔎 Filter stock codes with more than 1 unique description
inconsistent_desc = desc_counts.query('unique_descriptions > 1')

# 📋 Output summary and optionally display table
if inconsistent_desc.shape[0] > 0:
    safe_print(f"❗ Stock codes with conflicting descriptions: {inconsistent_desc.shape[0]}")
    display(inconsistent_desc.head(10))  # Preview sample inconsistencies
else:
    safe_print("✅ All stock codes map to a unique description.")


# ---
# 
# ### ✅ Product Description Consistency Check Passed
# 
# Each `stock_code` in the dataset maps uniquely to a single product `description`, confirming the integrity of the `products` table. This ensures that the `stock_code` column can serve reliably as a primary key when constructing the `products` table in the SQL schema.
# 
# > No further action is needed for this relationship.
# 
# ---

# ---
# 
# ### 🧾 Step 21.3a Investigating Invoices with Conflicting Metadata
# 
# To ensure consistent invoice records, we examine whether any `invoice_no` is linked to **multiple invoice dates** or **multiple customer IDs**. Ideally, each invoice should be associated with a single customer and a single timestamp.
# 
# This validation step allows us to:
# - Detect `invoice_no` values that appear with different dates.
# - Identify invoice numbers assigned to more than one customer.
# - Preview a sample of problematic rows to guide the next data cleaning step.
# 
# Understanding these inconsistencies is essential for building a reliable `invoices` table and maintaining accurate relationships between tables in the relational schema.
# 
# ---
# 
# 

# In[ ]:


# 🔍 Check if any invoice_no maps to multiple invoice_date or customer_id
invoice_conflicts = (
    df_raw.groupby('invoice_no')
    .agg({
        'invoice_date': 'nunique',
        'customer_id': 'nunique'
    })
    .query('invoice_date > 1 or customer_id > 1')
)

safe_print(f"❗ Conflicting invoice_no entries: {invoice_conflicts.shape[0]}")

if not invoice_conflicts.empty:
    display(invoice_conflicts.head(10))

    # 🧾 Sample rows from conflicting invoice_no entries
    sample_invoices = df_raw[df_raw['invoice_no'].isin(invoice_conflicts.index)]
    safe_print("\n🧾 Sample of conflicting invoice rows:")
    display(sample_invoices.sort_values('invoice_no').head(20))

    # 🔍 Separate check: How many have >1 customer_id?
    multi_customer_invoices = invoice_conflicts.query('customer_id > 1')
    safe_print(f"\n❗ Invoices with multiple customer_id entries: {multi_customer_invoices.shape[0]}")

    if not multi_customer_invoices.empty:
        display(multi_customer_invoices)
else:
    safe_print("🎉 All invoice_no entries map to consistent invoice_date and customer_id.")


# ---
# 
# ### ❗ Duplicate Invoice Metadata Detected
# 
# We identified **64 `invoice_no` values** that are associated with **multiple `invoice_date` values** in the dataset. Importantly, none of these invoice numbers are linked to multiple `customer_id` values — this confirms that each invoice belongs to a single customer, but has inconsistent timestamps across rows.
# 
# > The most common cause is line items being recorded at slightly different times (e.g., `12:28:00` vs `12:29:00`), likely due to how items were scanned or processed at checkout.
# 
# A sample of these conflicting rows shows the same `invoice_no` assigned to a single customer, but with minor differences in `invoice_date`, usually within the same minute.
# 
# To prepare for accurate relational table construction, we must ensure:
# - Each `invoice_no` is paired with **only one `invoice_date`**, and
# - The mapping from `invoice_no` to `customer_id` is **one-to-one** and consistent.
# 
# In the next step, we will build a clean invoice metadata table with one row per `invoice_no`, assigning the **earliest timestamp** as the canonical `invoice_date`.
# 
# ---
# 

# ---
# 
# 
# ### 🛠️ Step 21.3b Resolving Duplicate `invoice_no` Entries
# 
# To ensure a clean one-to-one mapping between `invoice_no` and its associated metadata (`invoice_date`, `customer_id`), we construct a **clean invoice metadata table**. For each invoice, we retain:
# 
# - The **earliest timestamp** (`invoice_date`) across all rows
# - The **unique `customer_id`** (which we previously confirmed is consistent)
# 
# This will allow us to:
# - Export the `invoices` relational table with **one row per invoice**
# - Optionally update the full dataset so that **all rows under the same `invoice_no`** share the same standardized `invoice_date` and `customer_id`
# 
# We also perform a final integrity check to confirm no remaining `invoice_no` conflicts.
# 
# ---
# 

# In[ ]:


# ✅ Step 1: Build clean invoice metadata table
invoice_metadata = (
    df_raw
    .sort_values('invoice_date')
    .groupby('invoice_no', as_index=False)
    .agg({
        'invoice_date': 'first',       # earliest timestamp
        'customer_id': 'first'         # consistent customer_id per invoice
    })
)

safe_print(f"✅ Clean invoice metadata shape: {invoice_metadata.shape}")
display(invoice_metadata.head())

# ✅ Step 2: Drop invoice_date and customer_id to avoid _x/_y merge conflicts
df_raw = df_raw.drop(columns=['invoice_date', 'customer_id'])

# ✅ Step 3: Merge clean metadata back into df_raw
df_raw = df_raw.merge(invoice_metadata, on='invoice_no', how='left')

# 🔍 Final check for remaining conflicts
invoice_conflicts_check = (
    df_raw.groupby('invoice_no')
    .agg({
        'invoice_date': 'nunique',
        'customer_id': 'nunique'
    })
    .query('invoice_date > 1 or customer_id > 1')
)

safe_print(f"✅ Remaining invoice_no conflicts after fix: {invoice_conflicts_check.shape[0]}")
if not invoice_conflicts_check.empty:
    display(invoice_conflicts_check.head())
else:
    safe_print("🎉 All invoice_no values are now consistent for customer_id and invoice_date.")


# ---
# 
# ### ✅ Invoice Metadata Successfully Standardized
# 
# We have now created a **clean invoice metadata table** that ensures:
# 
# - Each `invoice_no` is associated with exactly **one `invoice_date`** — the earliest recorded timestamp.
# - Each `invoice_no` is mapped to a **single `customer_id`** — no duplication across customers.
# 
# By merging this clean metadata back into the main dataset (`df_raw`), we have **standardized all invoice records**, eliminating previous timestamp discrepancies within the same invoice.
# 
# ✅ **Validation confirmed**: No remaining `invoice_no` entries with multiple `invoice_date` or `customer_id` values.
# 
# This step was critical to support:
# - Reliable creation of the `invoices` relational table (one row per invoice).
# - Accurate time-based analyses, customer segmentation, and RFM scoring.
# 
# We are now ready to move forward with exporting the cleaned dataset and constructing the relational tables.
# 
# ---

# ---
# 
# ### 📦 Step 21.4a Checking for Duplicate Invoice Line Items
# 
# To ensure clean relational modeling, we need to verify whether each `invoice_no` and `stock_code` pair appears **only once** in the dataset. In a well-structured invoice line table, each product should appear only once per invoice unless quantity is aggregated.
# 
# We'll check for duplicates based on the composite key:
# 
# - `invoice_no`
# - `stock_code`
# 
# This step is essential before constructing the `invoice_items` table.
# 
# ---
# 

# In[ ]:


# 🔍 Check for duplicate (invoice_no, stock_code) pairs
composite_duplicates = (
    df_raw.groupby(['invoice_no', 'stock_code'])
    .size()
    .reset_index(name='count')
    .query('count > 1')
)

safe_print(f"❗ Duplicate (invoice_no, stock_code) pairs: {composite_duplicates.shape[0]}")

# 📄 Table: Counts of duplicate line items
safe_print("\n🧾 Table: Invoice/Product pairs with multiple rows")
display(composite_duplicates.head(10))

# 📄 Table: Sample of duplicated rows from the main dataset
duplicated_keys = composite_duplicates[['invoice_no', 'stock_code']]
duplicated_rows = df_raw.merge(duplicated_keys, on=['invoice_no', 'stock_code'])

safe_print("\n📄 Sample of duplicate invoice line items:")
display(duplicated_rows.sort_values(['invoice_no', 'stock_code']).head(20))


# ---
# 
# ### ❗ Duplicate Line Items in `invoice_items`
# 
# We identified **10,147 duplicate rows** based on the composite key (`invoice_no`, `stock_code`). This means that some invoices list the same product multiple times, often with split quantities.
# 
# > This is common in transactional systems where items are scanned separately or added in multiple steps.
# 
# A sample of these entries shows that:
# 
# - The same product (`stock_code`) appears more than once in the same invoice
# - Each row may have a different quantity but the same `unit_price`
# 
# To create a **clean invoice_items table** for relational export, we need to:
# - Group these rows by `invoice_no` and `stock_code`
# - Aggregate the **total quantity** and **line_revenue**
# - Retain relevant metadata (e.g., `description`, `unit_price`)
# 
# We’ll address this in the next step.
# 
# ---
# 

# ---
# 
# ### ✅ Step 21.4b Cleaning `invoice_items` Table
# 
# We now resolve the issue of duplicate `(invoice_no, stock_code)` combinations by aggregating them into unique invoice-product line items.
# 
# For each `(invoice_no, stock_code)` pair, we group by:
# - `invoice_no`
# - `stock_code`
# - `description`
# - `unit_price`
# 
# And we aggregate:
# - `quantity` and `line_revenue` (as sums)
# - `invoice_date`, `customer_id`, and `country` (using the first value, since they’re consistent across duplicates)
# 
# This results in a clean version of the `invoice_items` table, where each row represents a distinct product line in a given invoice.
# 
# ---
# 

# In[ ]:


# ✅ Re-identify duplicate (invoice_no, stock_code) pairs
duplicate_counts = (
    df_raw
    .groupby(['invoice_no', 'stock_code'])
    .size()
    .reset_index(name='count')
    .query('count > 1')
)

# ✅ Group and aggregate duplicate invoice-product line items
invoice_items_cleaned = (
    df_raw
    .groupby(['invoice_no', 'stock_code', 'description', 'unit_price'], as_index=False)
    .agg({
        'quantity': 'sum',
        'line_revenue': 'sum',
        'invoice_date': 'first',    # consistent per invoice
        'customer_id': 'first',     # already cleaned
        'country': 'first'          # already standardized
    })
)

# ✅ Sort for consistent export order
invoice_items_cleaned.sort_values(by=['invoice_date', 'invoice_no', 'stock_code'], inplace=True)

# ✅ Preview shape and top rows
safe_print(f"✅ invoice_items_cleaned shape: {invoice_items_cleaned.shape}")
safe_print("🧾 Table: First rows from invoice_items_cleaned")
display(invoice_items_cleaned.head())

# 🧾 Preview: Aggregated rows that were duplicated before
duplicated_keys = duplicate_counts[['invoice_no', 'stock_code']].drop_duplicates()
duplicated_aggregated = invoice_items_cleaned.merge(duplicated_keys, on=['invoice_no', 'stock_code'])

safe_print("📄 Aggregated versions of previously duplicated rows:")
display(duplicated_aggregated.head(15))

# ✅ Final assignment for exporting and consistency with EDA/SQL workflows
raw_cleaned_df = invoice_items_cleaned.copy()
safe_print(f"✅ Final cleaned flat dataset assigned to: raw_cleaned_df → shape: {raw_cleaned_df.shape}")


# ### ✅ Aggregation of Duplicate Invoice Line Items Completed
# 
# We identified and aggregated **10,147 duplicate (invoice_no, stock_code) pairs** in the dataset. These duplicates likely represented the same product being recorded multiple times on the same invoice, potentially due to separate scans or order modifications.
# 
# As a result:
# 
# - Quantities were **summed** per invoice-product pair
# - Line revenues were **recomputed** accordingly
# - Associated metadata such as `invoice_date`, `customer_id`, and `country` were **preserved consistently**
# 
# The table below displays a sample of the affected invoice line items after aggregation, confirming that rows have been properly collapsed into unique entries.
# 
# This cleaned version of invoice line items will now serve as the base for both:
# - The **final flat cleaned dataset**, and
# - The **invoice_items relational table**
# 

# ## 💾 Step 22: Export Full Cleaned Dataset
# 
# Before creating normalized tables, we export the entire cleaned dataset as a single `.csv` file.  
# This file preserves the complete transactional structure and can be used for:
# 
# - Exploratory analysis (Python notebooks)
# - Dashboard integration (e.g., Tableau, Power BI)
# - Backup and reproducibility of the cleaning process
# 
# 📄 **File name:** `cleaned_online_retail_II.csv`  
# 📁 **Location:** `/cleaned_data/` under the main project folder
# 
# ---

# In[ ]:


# ✅ Toggle overwrite behavior (if not already defined)
OVERWRITE_CSV = True  # Set to False to avoid overwriting existing files

# 📁 Define cleaned data folder
export_path = os.path.join(project_base_path, 'cleaned_data')
os.makedirs(export_path, exist_ok=True)

# 📄 Export full cleaned dataset
full_clean_path = os.path.join(export_path, 'cleaned_online_retail_II.csv')
if OVERWRITE_CSV or not os.path.exists(full_clean_path):
    raw_cleaned_df.to_csv(full_clean_path, index=False)
    safe_print(f"✅ Saved full cleaned dataset: {full_clean_path}")
else:
    safe_print(f"⚠️ Skipped (already exists): {full_clean_path}")


# ---
# 
# ## 💾 Step 23: Export to Relational Tables
# 
# With the data fully cleaned and validated, we now export the dataset into **four normalized relational tables** in `.csv` format.
# 
# This enables SQL analysis, BI dashboarding, and future data science modeling.
# 
# | Table              | Description                                                   |
# |-------------------|---------------------------------------------------------------|
# | `customers.csv`    | One row per customer: `customer_id`, `country`               |
# | `products.csv`     | One row per product: `stock_code`, `description`, `unit_price`|
# | `invoices.csv`     | One row per invoice: `invoice_no`, `invoice_date`, `customer_id`|
# | `invoice_items.csv`| One row per item line: `invoice_no`, `stock_code`, `quantity`, `unit_price`, `line_revenue` |
# 
# 📁 All files will be saved inside:  
# `/cleaned_data/` under the main project folder
# 
# ---
# 

# In[ ]:


import os

# ✅ Toggle overwrite behavior
OVERWRITE_CSV = True  # Set to False to avoid overwriting existing files

# 📁 Define clean export folder
export_path = os.path.join(project_base_path, 'cleaned_data')
os.makedirs(export_path, exist_ok=True)

# 📄 Define file paths
customers_path = os.path.join(export_path, 'customers.csv')
products_path = os.path.join(export_path, 'products.csv')
invoices_path = os.path.join(export_path, 'invoices.csv')
invoice_items_path = os.path.join(export_path, 'invoice_items.csv')

# 💾 Save Customers
customers_df = raw_cleaned_df[['customer_id', 'country']].drop_duplicates()
if OVERWRITE_CSV or not os.path.exists(customers_path):
    customers_df.to_csv(customers_path, index=False)
    safe_print(f"✅ Saved: {customers_path}")
else:
    safe_print(f"⚠️ Skipped (already exists): {customers_path}")

# 💾 Save Products
products_df = (
    raw_cleaned_df
    .sort_values(by=['stock_code', 'description'])
    .drop_duplicates(subset='stock_code', keep='first')
    [['stock_code', 'description', 'unit_price']]
)
if OVERWRITE_CSV or not os.path.exists(products_path):
    products_df.to_csv(products_path, index=False)
    safe_print(f"✅ Saved: {products_path}")
else:
    safe_print(f"⚠️ Skipped (already exists): {products_path}")

# 💾 Save Invoices
invoices_df = raw_cleaned_df[['invoice_no', 'invoice_date', 'customer_id']].drop_duplicates()
if OVERWRITE_CSV or not os.path.exists(invoices_path):
    invoices_df.to_csv(invoices_path, index=False)
    safe_print(f"✅ Saved: {invoices_path}")
else:
    safe_print(f"⚠️ Skipped (already exists): {invoices_path}")

# 💾 Save Invoice Items (from deduplicated group)
invoice_items_df = invoice_items_cleaned[['invoice_no', 'stock_code', 'quantity', 'unit_price', 'line_revenue']]
if OVERWRITE_CSV or not os.path.exists(invoice_items_path):
    invoice_items_df.to_csv(invoice_items_path, index=False)
    safe_print(f"✅ Saved: {invoice_items_path}")
else:
    safe_print(f"⚠️ Skipped (already exists): {invoice_items_path}")


# ---
# 
# ## ✅ Notebook Complete: Cleaned Dataset Ready
# 
# This notebook successfully loaded, cleaned, validated, and exported the **Online Retail II** dataset.
# 
# Key steps completed:
# - 🧹 Removed invalid values, missing fields, and duplicates
# - 🚫 **Removed non-product stock codes** (e.g., `POST`, `CARRIAGE`, `S`, `M`) that do not represent tangible inventory
# - 🔤 Standardized categorical and identifier columns
# - 💰 Calculated total transaction-level revenue
# - 🧾 **Standardized product descriptions** to ensure consistent product-level analysis
# - 🔍 Checked and resolved **description inconsistencies** across stock codes
# - 🧪 Verified data types across all critical fields
# - 💾 Exported both the full cleaned dataset and **normalized relational tables** for SQL, BI, and modeling
# 
# 📁 **Output location**:  
# All files were saved to:  
# `/cleaned_data/` under the main project directory
# 
# ---
# 
# ### 📊 Next Steps
# 
# We can now proceed to:
# 
# 1. **Exploratory Data Analysis (EDA)**  
#    Analyze revenue trends, top countries, top-selling products, etc.
# 
# 2. **Customer Segmentation (RFM)**  
#    Segment customers by Recency, Frequency, and Monetary behavior using SQL or Python
# 
# 3. **SQL Integration**  
#    Load the cleaned `.csv` files into a relational database and create queries or dashboards
# 
# 4. **Optional Dashboards**  
#    Build a Tableau, Power BI, or Streamlit dashboard for business insights
# 
# ---
# 

# ---
# 
# ## 🧩 Optional Script Entry Point
# 
# This block allows the notebook to function as a standalone script when exported as `.py`.  
# If executed directly via command line or terminal, the cleaning process will run automatically.
# 
# This is useful for automating workflows in production or development environments.
# 
# ---
# 

# In[ ]:


# ✅ Optional script execution indicator for CLI use
if __name__ == "__main__":
    safe_print("🚀 Script executed directly as a .py file — all notebook steps above have been run sequentially.")



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
