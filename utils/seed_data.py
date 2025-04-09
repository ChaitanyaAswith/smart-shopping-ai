import sqlite3
import os
from datetime import datetime

# Ensure the DB path exists
db_path = "data/ecommerce.db"
os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Optional: Clear tables before inserting new data (for dev/testing only)
cursor.execute("DELETE FROM customers")
cursor.execute("DELETE FROM products")
cursor.execute("DELETE FROM interactions")

# Insert sample customers
customers = [
    ("Alice", "alice@example.com", 28, "Female", "New York"),
    ("Bob", "bob@example.com", 35, "Male", "California"),
    ("Charlie", "charlie@example.com", 22, "Male", "Texas"),
]

cursor.executemany("""
INSERT INTO customers (name, email, age, gender, location)
VALUES (?, ?, ?, ?, ?)
""", customers)

# Insert sample products (with image URLs)
products = [
    ("Wireless Earbuds", "Electronics", 49.99, "Bluetooth 5.0 earbuds with charging case", 100, "/images/earbuds.jpg"),
    ("Yoga Mat", "Fitness", 19.99, "Non-slip, eco-friendly yoga mat", 150, "/images/yoga_mat.jpg"),
    ("Smart Watch", "Electronics", 89.99, "Tracks fitness and notifications", 80, "/images/smart_watch.jpg"),
    ("Running Shoes", "Footwear", 59.99, "Comfortable shoes for jogging", 120, "/images/running_shoes.jpg"),
    ("Water Bottle", "Fitness", 9.99, "Stainless steel insulated bottle", 200, "/images/water_bottle.jpg"),
]

cursor.executemany("""INSERT INTO products (name, category, price, description, stock, image_url)
VALUES (?, ?, ?, ?, ?, ?)
""", products)

# Get real customer/product IDs from the DB
cursor.execute("SELECT id FROM customers WHERE name='Alice'")
alice_id = cursor.fetchone()[0]
cursor.execute("SELECT id FROM customers WHERE name='Bob'")
bob_id = cursor.fetchone()[0]
cursor.execute("SELECT id FROM customers WHERE name='Charlie'")
charlie_id = cursor.fetchone()[0]

cursor.execute("SELECT id FROM products WHERE name='Wireless Earbuds'")
earbuds_id = cursor.fetchone()[0]
cursor.execute("SELECT id FROM products WHERE name='Yoga Mat'")
yoga_id = cursor.fetchone()[0]
cursor.execute("SELECT id FROM products WHERE name='Smart Watch'")
watch_id = cursor.fetchone()[0]
cursor.execute("SELECT id FROM products WHERE name='Running Shoes'")
shoes_id = cursor.fetchone()[0]
cursor.execute("SELECT id FROM products WHERE name='Water Bottle'")
bottle_id = cursor.fetchone()[0]

# Insert sample interactions with correct IDs
interactions = [
    (alice_id, earbuds_id, "view"),
    (alice_id, yoga_id, "purchase"),
    (bob_id, watch_id, "view"),
    (charlie_id, shoes_id, "view"),
    (charlie_id, bottle_id, "purchase"),
]

timestamp = datetime.utcnow().isoformat()

cursor.executemany("""
INSERT INTO interactions (customer_id, product_id, interaction_type, timestamp)
VALUES (?, ?, ?, ?)
""", [(c, p, t, timestamp) for c, p, t in interactions])

conn.commit()
conn.close()

print("✅ Sample data inserted successfully.")
