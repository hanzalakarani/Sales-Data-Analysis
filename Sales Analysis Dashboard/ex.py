import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# Top-selling products
cursor_obj.execute('''
    SELECT 
        p.product_name, 
        SUM(s.quantity_sold) AS total_quantity_sold
    FROM Sales s
    JOIN Products p ON s.product_id = p.product_id
    GROUP BY p.product_name
    ORDER BY total_quantity_sold DESC
    LIMIT 10;
''')
print("Top-selling products:")
top_selling_products = cursor_obj.fetchall()

# Convert the result into a DataFrame for visualization
top_products_df = pd.DataFrame(top_selling_products, columns=['Product Name', 'Total Quantity Sold'])

# Plot the bar chart
plt.figure(figsize=(10,6))
sns.barplot(x='Total Quantity Sold', y='Product Name', data=top_products_df, palette='viridis')
plt.title('Top 10 Best-Selling Products')
plt.xlabel('Total Quantity Sold')
plt.ylabel('Product Name')
plt.tight_layout()
plt.show()

# Top customers by revenue
cursor_obj.execute('''
    SELECT 
        c.customer_name, 
        SUM(s.quantity_sold * p.price) AS total_revenue
    FROM Sales s
    JOIN Customers c ON s.customer_id = c.customer_id
    JOIN Products p ON s.product_id = p.product_id
    GROUP BY c.customer_name
    ORDER BY total_revenue DESC
    LIMIT 10;
''')
print("Top customers by revenue:")
for rows in cursor_obj.fetchall():
    print(rows)

# Monthly sales trend (correct date formatting)
cursor_obj.execute('''
    SELECT 
    strftime('%Y-%m', replace(s.sale_date, '/', '-')) AS sale_month, 
    SUM(s.quantity_sold * p.price) AS total_revenue
FROM Sales s
JOIN Products p ON s.product_id = p.product_id
GROUP BY sale_month
ORDER BY sale_month;
''')
print("Monthly sales trend:")
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

# Sales by region (ensure matching country-region data)
cursor_obj.execute('''
    SELECT 
        c.country, 
        SUM(s.quantity_sold * p.price) AS total_revenue
    FROM Sales s
    JOIN Customers c ON s.customer_id = c.customer_id
    JOIN Products p ON s.product_id = p.product_id
    GROUP BY c.country
    ORDER BY total_revenue DESC;
''')
print("Sales by region:")
sales_by_region = cursor_obj.fetchall()

# Convert the result into a DataFrame for visualization
region_sales_df = pd.DataFrame(sales_by_region, columns=['Country', 'Total Revenue'])

# Plot the bar chart
plt.figure(figsize=(10,6))
sns.barplot(x='Total Revenue', y='Country', data=region_sales_df, palette='coolwarm')
plt.title('Top 10 Countries by Sales Revenue')
plt.xlabel('Total Revenue')
plt.ylabel('Country')
plt.tight_layout()
plt.show()

# Average sale amount per transaction
cursor_obj.execute('''
    SELECT AVG(s.quantity_sold * p.price) AS avg_sale_amount
    FROM Sales s
    JOIN Products p ON s.product_id = p.product_id;
''')
print("Average sale amount per transaction:")
for rows in cursor_obj.fetchall():
    print(rows)

# Top categories by revenue
cursor_obj.execute('''
    SELECT p.category, SUM(s.quantity_sold * p.price) AS total_revenue
    FROM Sales s
    JOIN Products p ON s.product_id = p.product_id
    GROUP BY p.category
    ORDER BY total_revenue DESC;
''')
print("Top categories by revenue:")
for rows in cursor_obj.fetchall():
    print(rows)


# Total revenue by product in each region
cursor_obj.execute('''
    SELECT r.region_name, p.product_name, SUM(s.quantity_sold * p.price) AS total_revenue
    FROM Sales s
    JOIN Customers c ON s.customer_id = c.customer_id
    JOIN Products p ON s.product_id = p.product_id
    JOIN Regions r ON c.country = r.region_name
    GROUP BY r.region_name, p.product_name
    ORDER BY r.region_name, total_revenue DESC;
''')
print("Total revenue by product in each region:")
for rows in cursor_obj.fetchall():
    print(rows)

# Total sales and revenue for each month
cursor_obj.execute('''
    SELECT strftime('%Y-%m', replace(s.sale_date, '/', '-')) AS sale_month, 
           COUNT(s.sale_id) AS total_sales,
           SUM(s.quantity_sold * p.price) AS total_revenue
    FROM Sales s
    JOIN Products p ON s.product_id = p.product_id
    GROUP BY sale_month
    ORDER BY sale_month;
''')
print("Total sales and revenue for each month:")
for rows in cursor_obj.fetchall():
    print(rows)

# Fetch the data for top customers by revenue
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

# Convert the result into a DataFrame for visualization
top_customers_df = pd.DataFrame(top_customers, columns=['Customer Name', 'Total Revenue'])

# Plot the horizontal bar chart
plt.figure(figsize=(10,6))
sns.barplot(x='Total Revenue', y='Customer Name', data=top_customers_df, palette='magma',legend=False,hue='y')
plt.title('Top 10 Customers by Revenue')
plt.xlabel('Total Revenue')
plt.ylabel('Customer Name')
plt.tight_layout()
plt.show()

# Fetch the data for average sale amount per transaction
cursor_obj.execute('''
    SELECT AVG(s.quantity_sold * p.price) AS avg_sale_amount
    FROM Sales s
    JOIN Products p ON s.product_id = p.product_id;
''')
avg_sale_amount = cursor_obj.fetchone()[0]

# Visualize average sale amount
plt.figure(figsize=(6,6))
plt.bar(['Average Sale Amount'], [avg_sale_amount], color='c')
plt.title('Average Sale Amount per Transaction')
plt.ylabel('Average Sale Amount')
plt.tight_layout()
plt.show()


# Index creation
cursor_obj.execute('CREATE INDEX IF NOT EXISTS idx_customer_id ON Sales (customer_id);')
cursor_obj.execute('CREATE INDEX IF NOT EXISTS idx_product_id ON Sales (product_id);')
cursor_obj.execute('CREATE INDEX IF NOT EXISTS idx_sale_date ON Sales (sale_date);')
print("Indexes created successfully.")

