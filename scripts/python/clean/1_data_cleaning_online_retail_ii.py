# 🧼 Data Cleaning Script – Online Retail II
# 📓 Source Notebook: 1_data_cleaning_online_retail_ii.ipynb
# 📊 Description: Loads, cleans, and prepares the Online Retail II dataset for analysis.
# 🏫 School: Ironhack Puerto Rico
# 🎓 Bootcamp: Data Science and Machine Learning
# 📅 Date: December 20, 2024
# 👩‍💻 Author: Ginosca Alejandro Dávila

#!/usr/bin/env python
# coding: utf-8

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


# In[ ]:


# ⏳ Check date range of invoice timestamps
min_date = df_raw['invoice_date'].min()
max_date = df_raw['invoice_date'].max()

safe_print(f"🕐 Earliest invoice date: {min_date}")
safe_print(f"🕙 Latest invoice date:   {max_date}")


# In[ ]:


# 🧹 Filter out rows with invalid quantity or price
initial_shape = df_raw.shape

df_raw = df_raw[(df_raw['quantity'] > 0) & (df_raw['unit_price'] > 0)]

# ✅ Show change in dataset size
safe_print(f"🧮 Rows before filtering: {initial_shape[0]}")
safe_print(f"✅ Rows after filtering:  {df_raw.shape[0]}")
safe_print(f"➖ Rows removed:          {initial_shape[0] - df_raw.shape[0]}")


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


# In[ ]:


# 🧾 Drop rows with missing product description
initial_shape = df_raw.shape
df_raw = df_raw.dropna(subset=['description'])

# 🧾 Summary of effect
safe_print(f"🧮 Rows before dropping missing description: {initial_shape[0]}")
safe_print(f"✅ Rows after dropping:                     {df_raw.shape[0]}")
safe_print(f"➖ Rows removed:                            {initial_shape[0] - df_raw.shape[0]}")


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
