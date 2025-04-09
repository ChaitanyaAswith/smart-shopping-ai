# agents/product_agent.py

from memory.memory_manager import MemoryManager
from typing import List, Optional

class ProductAgent:
    def __init__(self, memory: MemoryManager):
        self.memory = memory
        self.products = self.memory.get_all_products()

    def get_all_products(self) -> List[dict]:
        return self.products

    def get_product_by_id(self, product_id: int) -> Optional[dict]:
        for product in self.products:
            if product["id"] == product_id:
                return product
        return None

    def filter_by_category(self, category: str) -> List[dict]:
        return [p for p in self.products if p["category"] == category]

    def search_products(self, keyword: str) -> List[dict]:
        keyword_lower = keyword.lower()
        return [
            p for p in self.products
            if keyword_lower in p["name"].lower() or keyword_lower in (p.get("description") or "").lower()
        ]
