import sqlite3
import os

# Path to your database
db_path = "data/ecommerce.db"

# Ensure the directory exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Clear all existing data and reset autoincrement
cursor.execute("DELETE FROM interactions")
cursor.execute("DELETE FROM customers")
cursor.execute("DELETE FROM products")
cursor.execute("DELETE FROM sqlite_sequence")  # Reset auto-increment IDs

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

# Insert sample products
products = [
    ("Wireless Earbuds", "Electronics", 49.99, "Bluetooth 5.0 earbuds with charging case", 100, "/static/images/earbuds.jpg"),
    ("Yoga Mat", "Fitness", 19.99, "Non-slip, eco-friendly yoga mat", 150, "/static/images/yoga_mat.jpg"),
    ("Smart Watch", "Electronics", 89.99, "Tracks fitness and notifications", 80, "/static/images/smart_watch.jpg"),
    ("Running Shoes", "Footwear", 59.99, "Comfortable shoes for jogging", 120, "/static/images/shoes.jpg"),
    ("Water Bottle", "Fitness", 9.99, "Stainless steel insulated bottle", 200, "/static/images/bottle.jpg"),
]
cursor.executemany("""
INSERT INTO products (name, category, price, description, stock, image_url)
VALUES (?, ?, ?, ?, ?, ?)
""", products)

# Insert sample interactions
interactions = [
    (1, 1, "view"),      # Alice views Wireless Earbuds
    (1, 2, "purchase"),  # Alice buys Yoga Mat
    (2, 3, "view"),      # Bob views Smart Watch
    (3, 4, "view"),      # Charlie views Running Shoes
    (3, 5, "purchase")   # Charlie buys Water Bottle
]
cursor.executemany("""
INSERT INTO interactions (customer_id, product_id, interaction_type)
VALUES (?, ?, ?)
""", interactions)

# Commit and close
conn.commit()

# Print DB state
print("\n📦 Products in DB:")
for row in cursor.execute("SELECT * FROM products"):
    print(row)

print("\n👥 Customers in DB:")
for row in cursor.execute("SELECT * FROM customers"):
    print(row)

print("\n🛒 Interactions in DB:")
for row in cursor.execute("SELECT * FROM interactions"):
    print(row)

conn.close()
print("\n✅ Database reset and test data inserted successfully.")
