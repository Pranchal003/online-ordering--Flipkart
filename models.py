# models.py
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123456",  # change if needed
        database="flipkart_clone"
    )

def add_product(name, description, price, stock):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, description, price, stock) VALUES (%s, %s, %s, %s)",
                   (name, description, price, stock))
    conn.commit()
    conn.close()

def view_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

def place_order(customer_id, items):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (customer_id) VALUES (%s)", (customer_id,))
    order_id = cursor.lastrowid
    for product_id, quantity in items:
        cursor.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)",
                       (order_id, product_id, quantity))
        cursor.execute("UPDATE products SET stock = stock - %s WHERE id = %s", (quantity, product_id))
    conn.commit()
    conn.close()
    return order_id
