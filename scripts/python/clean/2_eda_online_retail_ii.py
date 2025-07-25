# 📊 Exploratory Data Analysis Script – Online Retail II
# 📓 Source Notebook: 2_eda_online_retail_ii.ipynb
# 🔍 Description: Explores trends in sales, products, customers, and revenue.
# 🏫 School: Ironhack Puerto Rico
# 🎓 Bootcamp: Data Science and Machine Learning
# 📅 Date: December 20, 2024
# 👩‍💻 Author: Ginosca Alejandro Dávila

#!/usr/bin/env python
# coding: utf-8

# In[1]:


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

# 🔧 Set base path depending on environment
if is_colab():
    from google.colab import drive
    drive.mount('/content/drive')

    # ✅ Default project path in Colab
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


# In[2]:


# 📦 Import core libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# 🧼 Aesthetic setup for plots
plt.style.use("ggplot")
sns.set_palette("pastel")

# 📁 Define path to cleaned flat dataset
clean_path = os.path.join(project_base_path, 'cleaned_data')
full_data_path = os.path.join(clean_path, 'cleaned_online_retail_II.csv')

# 📥 Load the flat dataset with error handling
try:
    cleaned_full_df = pd.read_csv(full_data_path, parse_dates=['invoice_date'])

    safe_print("✅ Cleaned flat dataset loaded successfully.")
    safe_print(f"cleaned_full_df shape: {cleaned_full_df.shape}")

except FileNotFoundError as e:
    safe_print(f"❌ File not found: {e}")
    sys.exit(1)


# In[3]:


import io

# ✅ Display fallback for script environments
try:
    display
except NameError:
    def display(x):
        print(x.to_string() if isinstance(x, pd.DataFrame) else str(x))

# 🔍 Helper function to inspect a DataFrame’s basic structure
def inspect_basic_structure(df, name="Dataset", preview_rows=5):
    """
    Display structure, sample rows, missing values, and schema of a DataFrame.
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

    # 🧼 Missing values per column
    safe_print("🔸 Missing Values (per column):")
    missing_summary = df.isnull().sum()
    display(missing_summary[missing_summary > 0] if missing_summary.any() else "✅ No missing values.")

    safe_print("=" * 60 + "\n")


# In[4]:


# 🧪 Inspect structure and content of the cleaned_full_df DataFrame
inspect_basic_structure(cleaned_full_df, name="cleaned_online_retail_II.csv")


# In[5]:


# 🧠 Variable classification for cleaned_full_df only
variable_types = {
    'cleaned_online_retail_II': {
        'identifier': ['invoice_no', 'stock_code', 'customer_id'],
        'categorical': ['description', 'country'],
        'quantitative': ['quantity', 'unit_price', 'line_revenue'],
        'datetime': ['invoice_date']
    }
}

# ✅ Display summary
safe_print("✅ Variable classification completed:\n")

for dataset, types in variable_types.items():
    safe_print(f"📄 Dataset: {dataset}")
    for var_type, columns in types.items():
        safe_print(f"  {var_type.title()} Columns:")
        if columns:
            for col in columns:
                safe_print(f"    • {col}")
        else:
            safe_print("    (None)")
    safe_print("")


# In[6]:


# 🔢 Columns to describe
quantitative_cols = ['quantity', 'unit_price', 'line_revenue']

# 📊 Summary statistics
safe_print("📊 Summary Statistics for Quantitative Columns:\n")
display(cleaned_full_df[quantitative_cols].describe())

# 🔍 Check for zero or negative values (if any remain)
safe_print("\n🔍 Number of rows with non-positive values:")
for col in quantitative_cols:
    count = (cleaned_full_df[col] <= 0).sum()
    safe_print(f"  • {col}: {count}")


# In[7]:


import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 📦 Setup
OVERWRITE_PLOTS = True
plot_export_dir = os.path.join(project_base_path, 'eda_outputs', 'plots')
os.makedirs(plot_export_dir, exist_ok=True)

# 🔢 Quantitative columns to analyze
quant_cols = ['quantity', 'unit_price', 'line_revenue']
plot_index = 1

# 📋 Frequency table helper
def display_frequency_table(series, label, bins=15, log_scale=False):
    title = f"log1p({label})" if log_scale else label
    safe_print(f"\n📋 Frequency Table for: {title}")
    safe_print("=" * 50)

    # Transform if log
    data = np.log1p(series) if log_scale else series

    if pd.api.types.is_integer_dtype(data) and data.nunique() < 50:
        freq_table = data.value_counts().sort_index()
    else:
        freq_table = pd.cut(data, bins=bins).value_counts().sort_index()

    display(freq_table)

# 🔁 Loop through columns
for col in quant_cols:
    series = cleaned_full_df[col]

    # 📋 Raw frequency table
    display_frequency_table(series, col, bins=15, log_scale=False)

    # 📋 Log1p frequency table
    display_frequency_table(series, col, bins=15, log_scale=True)

    # 🎨 Plot setup
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f'Distribution of {col}', fontsize=16, fontweight='bold')

    # Axis label with units
    if col in ['unit_price', 'line_revenue']:
        x_label = f"{col} (GBP £)"
    else:
        x_label = col

    # Raw histogram
    sns.histplot(series, bins=100, ax=axes[0], kde=False)
    axes[0].set_title(f'{col} (Raw)', fontsize=12)
    axes[0].set_xlabel(x_label)
    axes[0].set_ylabel('Frequency')

    # Log-transformed histogram
    sns.histplot(np.log1p(series), bins=100, ax=axes[1], kde=False)
    axes[1].set_title(f'{col} (Log Scale)', fontsize=12)
    axes[1].set_xlabel(f'log1p({x_label})')
    axes[1].set_ylabel('Frequency')

    # Save plot
    plot_filename = f"{plot_index:02d}_{col}_distribution.png"
    plot_path = os.path.join(plot_export_dir, plot_filename)
    if OVERWRITE_PLOTS or not os.path.exists(plot_path):
        plt.savefig(plot_path)
        safe_print(f"✅ Saved plot: {plot_path}")
    else:
        safe_print(f"⚠️ Skipped (already exists): {plot_path}")

    plt.show()
    plot_index += 1


# In[8]:


import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.dates as mdates

# ✅ Setup export behavior
OVERWRITE_PLOTS = True
OVERWRITE_CSV = True
plot_index = 4
data_index = 1

# 📁 Define output directories
plot_dir = os.path.join(project_base_path, 'eda_outputs', 'plots')
data_dir = os.path.join(project_base_path, 'eda_outputs', 'data')
os.makedirs(plot_dir, exist_ok=True)
os.makedirs(data_dir, exist_ok=True)

# 📅 Extract invoice_month from invoice_date
cleaned_full_df['invoice_month'] = cleaned_full_df['invoice_date'].dt.to_period('M').dt.to_timestamp()
monthly_summary = cleaned_full_df.groupby('invoice_month').agg(
    monthly_revenue=('line_revenue', 'sum'),
    monthly_invoices=('invoice_no', 'nunique')
).reset_index()
monthly_summary['avg_revenue_per_invoice'] = monthly_summary['monthly_revenue'] / monthly_summary['monthly_invoices']

# 📝 Add label for partial month (December 2011)
monthly_summary['invoice_month_str'] = monthly_summary['invoice_month'].dt.strftime('%Y-%m')
monthly_summary.loc[monthly_summary['invoice_month_str'] == '2011-12', 'invoice_month_str'] += ' *'

# 💾 Export summary table
monthly_data_path = os.path.join(data_dir, f'{data_index:02d}_monthly_revenue_summary.csv')
if OVERWRITE_CSV or not os.path.exists(monthly_data_path):
    monthly_summary.to_csv(monthly_data_path, index=False)
    safe_print(f"✅ Exported summary: {monthly_data_path}")
else:
    safe_print(f"⚠️ Skipped (already exists): {monthly_data_path}")

# 📋 Show the full table
display(monthly_summary[['invoice_month_str', 'monthly_revenue', 'monthly_invoices', 'avg_revenue_per_invoice']])

# 📝 Note about partial month
safe_print("\n📝 Note: Months marked with * are partial months.")
safe_print("- 2011-12: Data available only up to December 9th.\n")

# 📊 Plot monthly revenue trend
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(monthly_summary['invoice_month'], monthly_summary['monthly_revenue'], marker='o', linewidth=2, label='Monthly Revenue')

# 🧭 Format x-axis ticks to show all months
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.xticks(rotation=45)

# 📍 Add vertical lines for each new year
for date in monthly_summary['invoice_month']:
    if date.month == 1:
        ax.axvline(date, color='gray', linestyle='--', alpha=0.7, label='Year Start' if date.year == 2010 else "")

# 📍 Mark partial month (Dec 2011)
partial_month = pd.to_datetime('2011-12-01')
ax.axvline(partial_month, color='red', linestyle='--', linewidth=1.5, label='Partial Month')

# 🏷️ Labels and legend
ax.set_title('Monthly Revenue Trend (2009–2011)', fontsize=16, fontweight='bold')
ax.set_xlabel('Invoice Month')
ax.set_ylabel('Total Revenue (GBP £)')
ax.legend()
plt.tight_layout()

# 💾 Save plot
plot_path = os.path.join(plot_dir, f'{plot_index:02d}_monthly_revenue_trend.png')
if OVERWRITE_PLOTS or not os.path.exists(plot_path):
    plt.savefig(plot_path)
    safe_print(f"✅ Saved plot: {plot_path}")
else:
    safe_print(f"⚠️ Skipped (already exists): {plot_path}")

plt.show()


# In[9]:


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# ✅ Export flags
OVERWRITE_PLOTS = True
OVERWRITE_CSV = True

# 📁 Define export paths
data_dir = os.path.join(project_base_path, 'eda_outputs', 'data')
plot_dir = os.path.join(project_base_path, 'eda_outputs', 'plots')
os.makedirs(data_dir, exist_ok=True)
os.makedirs(plot_dir, exist_ok=True)

# 📄 Output filenames
csv_path = os.path.join(data_dir, '02_top_products_by_revenue.csv')
plot_path = os.path.join(plot_dir, '05_top_products_revenue.png')

# 🧮 Aggregate top 10 products by revenue
top_products_df = (
    cleaned_full_df.groupby(['stock_code', 'description'])
    .agg(
        total_revenue=('line_revenue', 'sum'),
        total_quantity=('quantity', 'sum'),
        avg_unit_price=('unit_price', 'mean')
    )
    .reset_index()
    .sort_values(by='total_revenue', ascending=False)
    .head(10)
)

# 💾 Save CSV
if OVERWRITE_CSV or not os.path.exists(csv_path):
    top_products_df.to_csv(csv_path, index=False)
    safe_print(f"✅ Exported top products summary: {csv_path}")
else:
    safe_print(f"⚠️ Skipped (already exists): {csv_path}")

# 📋 Show top products table
display(top_products_df)

# 🎨 Plot setup
plt.figure(figsize=(12, 6))
pastel_colors = sns.color_palette("pastel", len(top_products_df))

# 📊 Draw horizontal bars manually
for i, (desc, revenue) in enumerate(zip(top_products_df["description"], top_products_df["total_revenue"])):
    plt.barh(y=i, width=revenue, color=pastel_colors[i])
    plt.text(revenue + 2000, i, f"£{revenue:,.0f}", va='center', fontsize=9)

# 🏷️ Format plot
plt.yticks(ticks=range(len(top_products_df)), labels=top_products_df["description"])
plt.title("Top 10 Best-Selling Products by Revenue", fontsize=14, fontweight='bold')
plt.xlabel("Total Revenue (GBP £)")
plt.ylabel("Product Description")
plt.tight_layout()

# 💾 Save plot
if OVERWRITE_PLOTS or not os.path.exists(plot_path):
    plt.savefig(plot_path, bbox_inches='tight')
    safe_print(f"✅ Saved plot: {plot_path}")
else:
    safe_print(f"⚠️ Skipped (already exists): {plot_path}")

# 📈 Show
plt.show()


# In[10]:


# 📦 Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 📁 Setup
OVERWRITE_PLOTS = True
plot_index = 6
data_index = 3
plot_dir = os.path.join(project_base_path, 'eda_outputs', 'plots')
data_dir = os.path.join(project_base_path, 'eda_outputs', 'data')
os.makedirs(plot_dir, exist_ok=True)
os.makedirs(data_dir, exist_ok=True)

# 🧮 Q3: Top 10 Invoices by Total Value
invoice_summary_df = (
    cleaned_full_df.groupby('invoice_no', as_index=False)
    .agg(
        total_invoice_revenue=('line_revenue', 'sum'),
        invoice_items=('stock_code', 'count'),
        customer_id=('customer_id', 'first'),
        invoice_date=('invoice_date', 'first')
    )
    .sort_values(by='total_invoice_revenue', ascending=False)
    .head(10)
)

# 💾 Export
invoice_summary_path = os.path.join(data_dir, f"{data_index:02d}_top_invoices_by_value.csv")
invoice_summary_df.to_csv(invoice_summary_path, index=False)
print(f"✅ Exported top invoice summary: {invoice_summary_path}")

# 📋 Display summary table
from IPython.display import display
display(invoice_summary_df)

# 📊 Plot
plt.figure(figsize=(12, 6))
ax = sns.barplot(
    data=invoice_summary_df,
    x='invoice_no',
    y='total_invoice_revenue',
    hue='invoice_no',       # Required to silence deprecation warning
    order=invoice_summary_df.sort_values("total_invoice_revenue", ascending=False)["invoice_no"],
    palette='pastel',
    legend=False           # Hide legend since x already encodes this
)

plt.title('Top 10 Invoices by Total Value', fontsize=14, fontweight='bold')
plt.xlabel('Invoice Number')
plt.ylabel('Total Revenue (GBP £)')

# ➕ Add labels
for p in ax.patches:
    value = p.get_height()
    ax.annotate(
        f"£{value:,.0f}",
        (p.get_x() + p.get_width() / 2, value),
        ha='center', va='bottom', fontsize=9, fontweight='bold'
    )

# 💾 Save plot
invoice_plot_path = os.path.join(plot_dir, f"{plot_index:02d}_top_invoices_by_value.png")
if OVERWRITE_PLOTS or not os.path.exists(invoice_plot_path):
    plt.savefig(invoice_plot_path, bbox_inches='tight')
    print(f"✅ Saved plot: {invoice_plot_path}")
else:
    print(f"⚠️ Skipped (already exists): {invoice_plot_path}")

plt.show()


# In[11]:


import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# 📁 Export directories
data_export_path = os.path.join(project_base_path, 'eda_outputs', 'data')
plot_export_path = os.path.join(project_base_path, 'eda_outputs', 'plots')
os.makedirs(data_export_path, exist_ok=True)
os.makedirs(plot_export_path, exist_ok=True)

# 📊 Full revenue summary by country
country_summary_df = (
    cleaned_full_df.groupby('country')
    .agg(
        total_revenue=('line_revenue', 'sum'),
        num_invoices=('invoice_no', 'nunique')
    )
    .assign(avg_invoice_value=lambda df: df.total_revenue / df.num_invoices)
    .sort_values('total_revenue', ascending=False)
    .reset_index()
)

# 💾 Export full country summary
full_country_path = os.path.join(data_export_path, '04_revenue_by_country.csv')
country_summary_df.to_csv(full_country_path, index=False)
safe_print(f"✅ Exported revenue by country: {full_country_path}")

# 📋 Display top 10 including UK
safe_print("\n📋 Top 10 Countries by Revenue (Including UK):")
display(country_summary_df.head(10))

# 📊 Plot including UK
plt.figure(figsize=(12, 6))
ax = sns.barplot(
    data=country_summary_df.head(10),
    y='country',
    x='total_revenue',
    hue='country',  # ✅ Avoid warning
    legend=False,
    palette='pastel'
)
plt.title("Top 10 Countries by Revenue (Including UK)", fontsize=14)
plt.xlabel("Total Revenue (GBP £)")
plt.ylabel("Country")

# 💬 Add labels at end of bars
for container in ax.containers:
    ax.bar_label(container, fmt='£%.0f', label_type='edge', padding=5)

plt.tight_layout()
plot_path_all = os.path.join(plot_export_path, '07_country_revenue_bar.png')
plt.savefig(plot_path_all)
safe_print(f"✅ Saved plot: {plot_path_all}")
plt.show()

# --- 🌍 Version excluding UK ---
country_excl_uk_df = country_summary_df[country_summary_df['country'].str.lower() != 'united kingdom']

# 💾 Export international summary
intl_path = os.path.join(data_export_path, '04_revenue_by_country_excl_uk.csv')
country_excl_uk_df.to_csv(intl_path, index=False)
safe_print(f"✅ Exported revenue by country (excluding UK): {intl_path}")

# 📋 Display top 10 excluding UK
safe_print("\n📋 Top 10 Countries by Revenue (Excluding UK):")
display(country_excl_uk_df.head(10))

# 📊 Plot excluding UK
plt.figure(figsize=(12, 6))
ax = sns.barplot(
    data=country_excl_uk_df.head(10),
    y='country',
    x='total_revenue',
    hue='country',  # ✅ Avoid warning
    legend=False,
    palette='pastel'
)
plt.title("Top 10 Countries by Revenue (Excluding UK)", fontsize=14)
plt.xlabel("Total Revenue (GBP £)")
plt.ylabel("Country")

# 💬 Add labels
for container in ax.containers:
    ax.bar_label(container, fmt='£%.0f', label_type='edge', padding=5)

plt.tight_layout()
plot_path_intl = os.path.join(plot_export_path, '07_country_revenue_bar_excl_uk.png')
plt.savefig(plot_path_intl)
safe_print(f"✅ Saved plot: {plot_path_intl}")
plt.show()


# In[12]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 📁 Export paths
data_dir = os.path.join(project_base_path, 'eda_outputs', 'data')
plot_dir = os.path.join(project_base_path, 'eda_outputs', 'plots')
os.makedirs(data_dir, exist_ok=True)
os.makedirs(plot_dir, exist_ok=True)

# 🔧 File paths
data_path = os.path.join(data_dir, '05_customer_behavior_by_country.csv')
plot_path = os.path.join(plot_dir, '08_country_avg_behavior_scatter.png')

# 📊 Aggregate by country
country_behavior = (
    cleaned_full_df.groupby('country')
    .agg(
        num_customers=('customer_id', 'nunique'),
        num_invoices=('invoice_no', 'nunique'),
        total_revenue=('line_revenue', 'sum')
    )
    .assign(
        avg_invoices_per_customer=lambda df: df['num_invoices'] / df['num_customers'],
        avg_revenue_per_customer=lambda df: df['total_revenue'] / df['num_customers']
    )
    .sort_values(by='total_revenue', ascending=False)
    .reset_index()
)

# 💾 Save to CSV
country_behavior.to_csv(data_path, index=False)
safe_print(f"✅ Exported: {data_path}")

# 📋 Display top 10
safe_print("\n📋 Top 10 Countries by Avg Spend & Frequency:")
display(country_behavior.head(10))

# 📈 Scatter Plot
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=country_behavior,
    x='avg_invoices_per_customer',
    y='avg_revenue_per_customer',
    size='total_revenue',
    hue='country',
    palette='pastel',
    legend=False,
    sizes=(50, 1000)
)

plt.title('Avg Spend vs Purchase Frequency by Country', fontsize=14, weight='bold')
plt.xlabel('Avg Invoices per Customer')
plt.ylabel('Avg Revenue per Customer (£)')
plt.grid(True)
plt.tight_layout()
plt.savefig(plot_path)
safe_print(f"✅ Saved plot: {plot_path}")
plt.show()


# In[13]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 📁 Define paths
data_dir = os.path.join(project_base_path, 'eda_outputs', 'data')
plot_dir = os.path.join(project_base_path, 'eda_outputs', 'plots')
os.makedirs(data_dir, exist_ok=True)
os.makedirs(plot_dir, exist_ok=True)

# 🔧 File outputs
output_csv = os.path.join(data_dir, '06_one_time_vs_repeat_customers.csv')
output_plot = os.path.join(plot_dir, '09_one_time_vs_repeat_customers.png')

# 📊 Count unique invoices per customer
invoice_counts = (
    cleaned_full_df.groupby('customer_id')
    .agg(
        total_invoices=('invoice_no', 'nunique'),
        total_revenue=('line_revenue', 'sum')
    )
    .reset_index()
)

# 🧩 Label customers
invoice_counts['customer_type'] = invoice_counts['total_invoices'].apply(
    lambda x: 'Single Purchase' if x == 1 else 'Repeat Customer'
)

# 📋 Summary counts
summary = invoice_counts['customer_type'].value_counts().reset_index()
summary.columns = ['customer_type', 'count']
summary['percent'] = (summary['count'] / summary['count'].sum()) * 100

# 💾 Export results
invoice_counts.to_csv(output_csv, index=False)
safe_print(f"✅ Exported: {output_csv}")

# 📊 Display summary
display(summary)

# 📈 Pie chart
plt.figure(figsize=(6, 6))
colors = sns.color_palette('pastel')[0:2]
plt.pie(
    summary['count'],
    labels=summary['customer_type'],
    autopct='%1.1f%%',
    colors=colors,
    startangle=140,
    textprops={'fontsize': 12}
)
plt.title('Customer Breakdown: Single vs Repeat Purchasers', fontsize=14, weight='bold')
plt.tight_layout()
plt.savefig(output_plot)
safe_print(f"✅ Saved plot: {output_plot}")
plt.show()


# In[14]:


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 📁 Output folders
data_dir = os.path.join(project_base_path, 'eda_outputs', 'data')
plot_dir = os.path.join(project_base_path, 'eda_outputs', 'plots')
os.makedirs(data_dir, exist_ok=True)
os.makedirs(plot_dir, exist_ok=True)

# 🔧 Define file paths
export_path = os.path.join(data_dir, '07_avg_order_value_per_customer.csv')
plot_path = os.path.join(plot_dir, '10_avg_order_value_distribution.png')  # adjusted index

# 📊 Compute average order value per customer
avg_order_df = (
    cleaned_full_df.groupby(['customer_id', 'invoice_no'])['line_revenue']
    .sum()
    .reset_index()
    .groupby('customer_id')
    .agg(
        total_spent=('line_revenue', 'sum'),
        num_orders=('invoice_no', 'nunique')
    )
    .assign(avg_order_value=lambda df: df['total_spent'] / df['num_orders'])
    .sort_values(by='avg_order_value', ascending=False)
    .reset_index()
)

# 💾 Save summary table
avg_order_df.to_csv(export_path, index=False)
safe_print(f"✅ Exported: {export_path}")

# 📋 Show top 10
safe_print("\n📋 Top 10 Customers by Avg Order Value:")
display(avg_order_df.head(10))

# 📊 Frequency table (raw only)
bins = 15
freq_raw = pd.cut(avg_order_df['avg_order_value'], bins=bins).value_counts().sort_index()
safe_print("\n📋 Frequency Table for Avg Order Value:")
display(freq_raw)

# 🎨 Plot: Histogram and Boxplot
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle("Average Order Value per Customer", fontsize=16, weight="bold")

# Histogram
sns.histplot(avg_order_df['avg_order_value'], bins=100, ax=axes[0], color='mediumaquamarine')
axes[0].set_title("Histogram of Avg Order Value")
axes[0].set_xlabel("Avg Order Value (£)")
axes[0].set_ylabel("Number of Customers")

# Boxplot
sns.boxplot(x=avg_order_df['avg_order_value'], ax=axes[1], color='lightgray')
axes[1].set_title("Boxplot of Avg Order Value")
axes[1].set_xlabel("Avg Order Value (£)")

# Save and show
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig(plot_path)
safe_print(f"\n✅ Saved plot: {plot_path}")
plt.show()


# In[15]:


import os
import pandas as pd
import matplotlib.pyplot as plt

# 📁 Define output paths
data_dir = os.path.join(project_base_path, 'eda_outputs', 'data')
plot_dir = os.path.join(project_base_path, 'eda_outputs', 'plots')
os.makedirs(data_dir, exist_ok=True)
os.makedirs(plot_dir, exist_ok=True)

data_output_path = os.path.join(data_dir, '08_top_customers_by_total_spend.csv')
plot_output_path = os.path.join(plot_dir, '11_top_customers_by_total_spend.png')

# 🧮 Top spenders calculation
top_spenders_df = (
    cleaned_full_df.groupby('customer_id')
    .agg(
        total_spent=('line_revenue', 'sum'),
        num_orders=('invoice_no', 'nunique')
    )
    .assign(avg_order_value=lambda df: df['total_spent'] / df['num_orders'])
    .sort_values(by='total_spent', ascending=False)
    .reset_index()
    .head(10)
)

# 💾 Save data
top_spenders_df.to_csv(data_output_path, index=False)
safe_print(f"✅ Exported: {data_output_path}")

# 📋 Display
safe_print("\n📋 Top 10 Customers by Total Spend:")
display(top_spenders_df)

# 🎨 Plot using Matplotlib directly (avoid seaborn’s layout bloat)
fig, ax = plt.subplots(figsize=(10, 6))
sorted_df = top_spenders_df.sort_values(by='total_spent')  # Plot from lowest to highest for horizontal bars

ax.barh(sorted_df['customer_id'].astype(str), sorted_df['total_spent'], color='lightblue')
ax.set_xlabel('Total Spend (GBP £)')
ax.set_ylabel('Customer ID')
ax.set_title('Top 10 Customers by Total Spend', fontsize=14, weight='bold')

# 💬 Annotate bars
for i, value in enumerate(sorted_df['total_spent']):
    ax.text(value + 1000, i, f"£{value:,.0f}", va='center', fontsize=9)

plt.tight_layout()
plt.savefig(plot_output_path)
safe_print(f"✅ Saved plot: {plot_output_path}")
plt.show()


# In[16]:


import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 📁 Define export directories
data_dir = os.path.join(project_base_path, 'eda_outputs', 'data')
plot_dir = os.path.join(project_base_path, 'eda_outputs', 'plots')
os.makedirs(data_dir, exist_ok=True)
os.makedirs(plot_dir, exist_ok=True)

# 🔧 Define file paths
recency_csv = os.path.join(data_dir, '09_customer_recency.csv')
recency_plot = os.path.join(plot_dir, '12_customer_recency_distribution.png')

# 🕒 Reference date = latest invoice date in dataset
reference_date = cleaned_full_df['invoice_date'].max()

# 🧮 Calculate recency per customer
recency_df = (
    cleaned_full_df.groupby('customer_id')['invoice_date']
    .max()
    .reset_index()
    .assign(recency_days=lambda df: (reference_date - df['invoice_date']).dt.days)
    .sort_values(by='recency_days')
)

# 💾 Save to CSV
recency_df.to_csv(recency_csv, index=False)
safe_print(f"✅ Exported: {recency_csv}")

# 📋 Show first and last 5 rows for context
safe_print("\n📋 Sample Customers by Recency (Top & Bottom):")
display(recency_df.head(5))
display(recency_df.tail(5))

# 🎨 Plot distribution
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
plt.savefig(recency_plot)
safe_print(f"✅ Saved plot: {recency_plot}")
plt.show()


# In[17]:


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ✅ Define export paths
export_path = os.path.join(data_dir, '10_customer_frequency.csv')
plot_path = os.path.join(plot_dir, '13_customer_frequency_distribution.png')

# 📊 Calculate customer frequency
frequency_df = (
    cleaned_full_df.groupby('customer_id')
    .agg(
        num_orders=('invoice_no', 'nunique'),
        total_spent=('line_revenue', 'sum')
    )
    .assign(avg_order_value=lambda df: df['total_spent'] / df['num_orders'])
    .sort_values(by='num_orders', ascending=False)
    .reset_index()
)

# 💾 Export CSV
frequency_df.to_csv(export_path, index=False)
safe_print(f"✅ Exported: {export_path}")

# 📋 Show sample customers (top & bottom)
safe_print("\n📋 Sample Customers by Frequency (Top & Bottom):")
display(frequency_df.head())
display(frequency_df.tail())

# 📊 Create bin edges (50 bins) and compute histogram
bin_count = 50
counts, bin_edges = np.histogram(frequency_df['num_orders'], bins=bin_count)

# 📋 Display frequency table using histogram counts
freq_table = pd.Series(counts, index=pd.IntervalIndex.from_breaks(bin_edges))
safe_print("\n📋 Frequency Table for Number of Orders:")
display(freq_table)

# 🎨 Plot histogram and boxplot
fig, axes = plt.subplots(1, 2, figsize=(16, 5))
fig.suptitle("Customer Purchase Frequency", fontsize=18, weight="bold")

# Histogram (manual bar plot)
axes[0].bar(x=bin_edges[:-1], height=counts, width=np.diff(bin_edges), color='skyblue', align='edge', edgecolor='gray')
axes[0].set_title("Distribution of Purchase Frequency")
axes[0].set_xlabel("Number of Orders")
axes[0].set_ylabel("Number of Customers")

# Boxplot
sns.boxplot(x=frequency_df['num_orders'], ax=axes[1], color='lightgray')
axes[1].set_title("Boxplot of Purchase Frequency")
axes[1].set_xlabel("Number of Orders")

# Save and show
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig(plot_path)
safe_print(f"✅ Saved plot: {plot_path}")
plt.show()


# In[18]:


# 📦 Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ✅ Setup paths
data_dir = os.path.join(project_base_path, 'eda_outputs', 'data')
plot_dir = os.path.join(project_base_path, 'eda_outputs', 'plots')
os.makedirs(data_dir, exist_ok=True)
os.makedirs(plot_dir, exist_ok=True)

# 🔧 File paths
export_path = os.path.join(data_dir, '11_customer_monetary_value.csv')
plot_path = os.path.join(plot_dir, '14_customer_monetary_value_distribution.png')

# 📥 Load frequency data
frequency_path = os.path.join(data_dir, '10_customer_frequency.csv')
frequency_df = pd.read_csv(frequency_path)

# ✅ Sort by total_spent descending
frequency_df = frequency_df.sort_values(by='total_spent', ascending=False).reset_index(drop=True)

# 💾 Save again under monetary value filename (for consistency)
frequency_df.to_csv(export_path, index=False)
safe_print(f"✅ Exported: {export_path}")

# 📋 Show sample rows
safe_print("\n📋 Sample Customers by Monetary Value (Top & Bottom):")
display(frequency_df[['customer_id', 'total_spent', 'num_orders', 'avg_order_value']].head())
display(frequency_df[['customer_id', 'total_spent', 'num_orders', 'avg_order_value']].tail())

# 📊 Frequency table with ~£20K bins
bin_count = 30
bin_edges = np.histogram_bin_edges(frequency_df['total_spent'], bins=bin_count)
freq_table = pd.cut(frequency_df['total_spent'], bins=bin_edges).value_counts().sort_index()
safe_print("\n📋 Frequency Table for Total Spend:")
display(freq_table.to_frame())

# 🎨 Plot histogram and boxplot
fig, axes = plt.subplots(1, 2, figsize=(16, 5))
fig.suptitle("Customer Monetary Value", fontsize=18, weight="bold")

# Histogram
sns.histplot(frequency_df['total_spent'], bins=bin_edges, ax=axes[0], color='mediumseagreen')
axes[0].set_title("Distribution of Total Spend")
axes[0].set_xlabel("Total Spend (£)")
axes[0].set_ylabel("Number of Customers")

# Boxplot
sns.boxplot(x=frequency_df['total_spent'], ax=axes[1], color='lightgray')
axes[1].set_title("Boxplot of Total Spend")
axes[1].set_xlabel("Total Spend (£)")

# Save and show plot
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig(plot_path)
safe_print(f"✅ Saved plot: {plot_path}")
plt.show()


# In[19]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# ✅ Paths
recency_csv = os.path.join(data_dir, '09_customer_recency.csv')  # from Q9
export_path = os.path.join(data_dir, '12_rfm_segmented_customers.csv')
plot_path = os.path.join(plot_dir, '15_rfm_segment_distribution.png')

# 📥 Load precomputed recency table
recency_df = pd.read_csv(recency_csv)

# 🧮 Compute frequency and monetary from original data
rfm_base = (
    cleaned_full_df.groupby('customer_id')
    .agg(
        frequency=('invoice_no', 'nunique'),
        monetary=('line_revenue', 'sum')
    )
    .reset_index()
)

# 🔗 Merge with recency
rfm_df = pd.merge(rfm_base, recency_df[['customer_id', 'recency_days']], on='customer_id')
rfm_df.rename(columns={'recency_days': 'recency'}, inplace=True)

# 🏷️ RFM Scoring (quartiles)
rfm_df['R'] = pd.qcut(rfm_df['recency'], 4, labels=[4, 3, 2, 1]).astype(int)
rfm_df['F'] = pd.qcut(rfm_df['frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4]).astype(int)
rfm_df['M'] = pd.qcut(rfm_df['monetary'], 4, labels=[1, 2, 3, 4]).astype(int)

# 🧮 RFM Score
rfm_df['RFM_Score'] = rfm_df[['R', 'F', 'M']].sum(axis=1)

# 🧠 Assign RFM Segment
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
rfm_df.to_csv(export_path, index=False)
safe_print(f"✅ Exported: {export_path}")

# ✅ Show a sample of the exported RFM scores
rfm_preview = pd.read_csv(export_path)
safe_print("\n📋 Sample of RFM Score Table:")
display(rfm_preview.head(10))  # or .sample(10) for randomness

# 📋 Show segment frequency table before chart
safe_print("\n📋 RFM Segment Counts:")
segment_counts = rfm_df['Segment'].value_counts().sort_values(ascending=False)
display(segment_counts)

# 🎨 Plot: Segment Distribution (fixes future warning)
plt.figure(figsize=(10, 6))
sns.barplot(
    x=segment_counts.index,
    y=segment_counts.values,
    hue=segment_counts.index,  # required for palette to apply
    palette='Set2',
    legend=False  # disables auto-legend
)
plt.title("Customer Segments Based on RFM Scores", fontsize=16, weight="bold")
plt.xlabel("RFM Segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(plot_path)
safe_print(f"✅ Saved plot: {plot_path}")
plt.show()


# In[20]:


# ✅ Optional script execution indicator for CLI use
if __name__ == "__main__":
    safe_print("📊 EDA script executed directly as a .py file — all analysis steps and exports have been completed.")



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
