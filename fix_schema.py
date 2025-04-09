import sqlite3

conn = sqlite3.connect("data/ecommerce.db")
cursor = conn.cursor()

# Check if 'image_url' column exists
cursor.execute("PRAGMA table_info(products)")
columns = [col[1] for col in cursor.fetchall()]

if "image_url" not in columns:
    print("🔧 Adding 'image_url' column to products table...")
    cursor.execute("ALTER TABLE products ADD COLUMN image_url TEXT")
    conn.commit()
    print("✅ Column added.")
else:
    print("ℹ️ 'image_url' column already exists.")

conn.close()
