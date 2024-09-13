import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sqlite3

# File paths to your CSVs
customers_path = 'C:/Users/USER/Desktop/Sales Analysis Dashboard/customers.csv'
products_path = 'C:/Users/USER/Desktop/Sales Analysis Dashboard/products.csv'
sales_path = 'C:/Users/USER/Desktop/Sales Analysis Dashboard/sales_updated.csv'
regions_path = 'C:/Users/USER/Desktop/Sales Analysis Dashboard/regions.csv'

# Create a connection to SQLite database
conn = sqlite3.connect('C:/Users/USER/Desktop/Sales Analysis Dashboard/sales_analysis.db') 

# Load the CSVs into DataFrames
customers_df = pd.read_csv(customers_path)
products_df = pd.read_csv(products_path)
sales_df = pd.read_csv(sales_path)
regions_df = pd.read_csv(regions_path)

# Write the data into the SQL database as tables
customers_df.to_sql('Customers', conn, if_exists='replace', index=False)
products_df.to_sql('Products', conn, if_exists='replace', index=False)
sales_df.to_sql('Sales', conn, if_exists='replace', index=False)
regions_df.to_sql('Regions', conn, if_exists='replace', index=False)

print("Data successfully loaded into the database!")

cursor_obj = conn.cursor()
# Sample Queries
cursor_obj.execute('''SELECT * FROM Customers LIMIT 10;''')
print("Customers data:")
for rows in cursor_obj.fetchall():
    print(rows)

cursor_obj.execute('''SELECT * FROM Products LIMIT 10;''')
print("Products data:")
for rows in cursor_obj.fetchall():
    print(rows)

cursor_obj.execute('''SELECT * FROM Sales LIMIT 10;''')
print("Sales data:")
for rows in cursor_obj.fetchall():
    print(rows)

cursor_obj.execute('''SELECT * FROM Regions LIMIT 10;''')
print("Regions data:")
for rows in cursor_obj.fetchall():
    print(rows)
# --- Top-Selling Products Visualization ---
cursor_obj.execute('''
    SELECT p.product_name, SUM(s.quantity_sold) AS total_quantity_sold
    FROM Sales s
    JOIN Products p ON s.product_id = p.product_id
    GROUP BY p.product_name
    ORDER BY total_quantity_sold DESC
    LIMIT 10;
''')
top_selling_products = cursor_obj.fetchall()
top_products_df = pd.DataFrame(top_selling_products, columns=['Product Name', 'Total Quantity Sold'])

# Plot the bar chart for top-selling products
plt.figure(figsize=(10, 6))
sns.barplot(x='Total Quantity Sold', y='Product Name', data=top_products_df, hue='Product Name', palette='viridis', legend=False)
plt.title('Top 10 Best-Selling Products')
plt.xlabel('Total Quantity Sold')
plt.ylabel('Product Name')
plt.tight_layout()
plt.show()

# --- Monthly Sales Trend Visualization ---
cursor_obj.execute('''
    SELECT 
    strftime('%Y-%m', replace(s.sale_date, '/', '-')) AS sale_month, 
    SUM(s.quantity_sold * p.price) AS total_revenue
FROM Sales s
JOIN Products p ON s.product_id = p.product_id
GROUP BY sale_month
ORDER BY sale_month;
''')
monthly_sales = cursor_obj.fetchall()

# Convert the result into a DataFrame for visualization
monthly_sales_df = pd.DataFrame(monthly_sales, columns=['Month', 'Total Revenue'])

# Plot the line chart
plt.figure(figsize=(10,6))
sns.lineplot(x='Month', y='Total Revenue', data=monthly_sales_df, marker='o', color='b')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- Sales by Region Visualization ---
cursor_obj.execute('''
    SELECT c.country, SUM(s.quantity_sold * p.price) AS total_revenue
    FROM Sales s
    JOIN Customers c ON s.customer_id = c.customer_id
    JOIN Products p ON s.product_id = p.product_id
    GROUP BY c.country
    ORDER BY total_revenue DESC
    LIMIT 10;
''')
sales_by_region = cursor_obj.fetchall()
region_sales_df = pd.DataFrame(sales_by_region, columns=['Country', 'Total Revenue'])

# Plot the bar chart for sales by region
plt.figure(figsize=(10, 6))
sns.barplot(x='Total Revenue', y='Country', data=region_sales_df, hue='Country', palette='coolwarm', legend=False)
plt.title('Top 10 Countries by Sales Revenue')
plt.xlabel('Total Revenue')
plt.ylabel('Country')
plt.tight_layout()
plt.show()

# --- Top Customers by Revenue Visualization ---
cursor_obj.execute('''
    SELECT c.customer_name, SUM(s.quantity_sold * p.price) AS total_revenue
    FROM Sales s
    JOIN Customers c ON s.customer_id = c.customer_id
    JOIN Products p ON s.product_id = p.product_id
    GROUP BY c.customer_name
    ORDER BY total_revenue DESC
    LIMIT 10;
''')
top_customers = cursor_obj.fetchall()
top_customers_df = pd.DataFrame(top_customers, columns=['Customer Name', 'Total Revenue'])

# Plot the horizontal bar chart for top customers
plt.figure(figsize=(10, 6))
sns.barplot(x='Total Revenue', y='Customer Name', data=top_customers_df, hue='Customer Name', palette='magma', legend=False)
plt.title('Top 10 Customers by Revenue')
plt.xlabel('Total Revenue')
plt.ylabel('Customer Name')
plt.tight_layout()
plt.show()

# --- Average Sale Amount Visualization ---
import matplotlib.pyplot as plt

# Retrieve Average Sale Amount
cursor_obj.execute('''
    SELECT AVG(s.quantity_sold * p.price) AS avg_sale_amount
    FROM Sales s
    JOIN Products p ON s.product_id = p.product_id;
''')
avg_sale_amount = cursor_obj.fetchone()[0]

# Define a benchmark average sale amount for comparison (e.g., $1500 as an example)
benchmark_avg = 1500

# Enhanced Bar Plot for Average Sale Amount with Benchmark
plt.figure(figsize=(8, 6))

# Plot actual average sale amount
plt.bar(['Actual Avg Sale'], [avg_sale_amount], color='teal', width=0.5, label='Actual Avg Sale')

# Plot benchmark sale amount for comparison
plt.bar(['Benchmark'], [benchmark_avg], color='gray', width=0.5, label='Benchmark')

# Adding annotations for the exact values
plt.text(0, avg_sale_amount + 50, f"${avg_sale_amount:,.2f}", ha='center', fontsize=12, color='black', weight='bold')
plt.text(1, benchmark_avg + 50, f"${benchmark_avg:,.2f}", ha='center', fontsize=12, color='black', weight='bold')

# Enhancing the plot with labels and title
plt.title('Average Sale Amount vs Benchmark', fontsize=16, fontweight='bold')
plt.ylabel('Sale Amount (in $)', fontsize=12)
plt.ylim(0, max(avg_sale_amount, benchmark_avg) + 500)  # Adding some space on top for readability

# Adding gridlines for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show legend
plt.legend()

# Display the plot
plt.tight_layout()
plt.show()

conn.close()