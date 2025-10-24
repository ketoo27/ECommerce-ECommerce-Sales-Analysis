import pyodbc
import pandas as pd

# 1. Define the connection string for your local SQL Server
#    (Using Windows Authentication)
conn_str = (
    r'DRIVER={SQL Server};'  # The driver you confirmed
    r'SERVER=localhost\SQLEXPRESS;'  # The server name you provided
    r'DATABASE=OlistCommerce;'  # Our database name
    r'Trusted_Connection=yes;'  # Uses your Windows login
)

# 2. Define the SQL query you built
sql_query = """
SELECT 
    orders.order_id, 
    orders.customer_id, 
    orders.order_status, 
    orders.order_purchase_timestamp,
    orders.order_approved_at,
    orders.order_delivered_carrier_date,
    orders.order_delivered_customer_date,
    orders.order_estimated_delivery_date,
    item.order_item_id, 
    item.product_id,
    item.seller_id,
    item.price,
    prod.product_category_name,
    pay.payment_type,
    pay.payment_value
FROM 
    olist_orders_dataset as orders
JOIN 
    olist_order_items_dataset as item on orders.order_id = item.order_id 
JOIN 
    olist_products_dataset as prod on item.product_id = prod.product_id 
JOIN 
    olist_order_payments_dataset as pay on orders.order_id = pay.order_id
"""

print("Connecting to SQL Server and running query...")

# 3. Connect to the database and run the query
try:
    # Establish the connection
    with pyodbc.connect(conn_str) as conn:
        # Use pandas to execute the query and load into a DataFrame
        df = pd.read_sql_query(sql_query, conn)

    print("Successfully loaded data into DataFrame!")
    
    # 4. Show a preview of the data
    print("Data preview:")
    print(df.head())

    # 5. Save the clean data to a new CSV file for Power BI
    output_filename = 'olist_master_data.csv'
    df.to_csv(output_filename, index=False)
    
    print(f"\nSuccessfully saved clean data to '{output_filename}'")

except Exception as e:
    print(f"An error occurred: {e}")