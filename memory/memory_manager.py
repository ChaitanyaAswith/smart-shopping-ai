# memory/memory_manager.py

import sqlite3
from typing import List, Dict, Optional

class MemoryManager:
    def __init__(self, db_path: str = "data/ecommerce.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def get_customer_by_id(self, customer_id: int) -> Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_customer_history(self, customer_id: int) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM interactions 
            WHERE customer_id = ? 
            ORDER BY timestamp DESC
        """, (customer_id,))
        return [dict(row) for row in cursor.fetchall()]

    def get_all_products(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()

        products = []
        for row in rows:
            product = dict(row)
            # Generate image file name: lowercase, spaces to underscores
            image_filename = product["name"].lower().replace(" ", "_") + ".jpg"
            product["image_url"] = f"/images/{image_filename}"
            products.append(product)

        return products

    def record_interaction(self, customer_id: int, product_id: int, interaction_type: str):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO interactions (customer_id, product_id, interaction_type, timestamp) 
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (customer_id, product_id, interaction_type))
        self.conn.commit()

    def close(self):
        self.conn.close()
