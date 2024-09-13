import sqlite3
import pandas as pd

# File paths to your CSVs
customers_path = 'C:/Users/USER/Desktop/Sales Analysis Dashboard/customers.csv'
products_path = 'C:/Users/USER/Desktop/Sales Analysis Dashboard/products.csv'
sales_path = 'C:/Users/USER/Desktop/Sales Analysis Dashboard/sales.csv'
regions_path = 'C:/Users/USER/Desktop/Sales Analysis Dashboard/regions.csv'

# Create a connection to SQLite database (or connect to another DB if needed)
conn = sqlite3.connect('C:/Users/USER/Desktop/Sales Analysis Dashboard/sales_analysis.db')  # This will create the DB if not exists

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

# Confirm successful import
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
for rows in cursor_obj.fetchall():
    print(rows)

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

# Monthly sales trend (adjust for correct date format)
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
for rows in cursor_obj.fetchall():
    print(rows)

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
for rows in cursor_obj.fetchall():
    print(rows)

# Index creation
cursor_obj.execute('CREATE INDEX idx_customer_id ON Sales (customer_id);')
cursor_obj.execute('CREATE INDEX idx_product_id ON Sales (product_id);')
cursor_obj.execute('CREATE INDEX idx_sale_date ON Sales (sale_date);')
print("Indexes created successfully.")    





