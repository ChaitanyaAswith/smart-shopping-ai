import sqlite3

conn = sqlite3.connect("data/ecommerce.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM customers")
cursor.execute("DELETE FROM products")
cursor.execute("DELETE FROM interactions")
conn.commit()
conn.close()

print("✅ Dummy data cleared.")
