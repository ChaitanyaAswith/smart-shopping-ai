from agents.customer_agent import CustomerAgent
from agents.product_agent import ProductAgent
from memory.memory_manager import MemoryManager
from typing import List, Dict
from utils.ollama_interface import query_ollama  # Added import for Ollama API

class RecommenderAgent:
    def __init__(self, customer_id: int, memory: MemoryManager):
        self.customer_id = customer_id
        self.memory = memory
        self.customer_agent = CustomerAgent(customer_id, memory)
        self.product_agent = ProductAgent(memory)

    def recommend(self, top_n: int = 5) -> List[Dict]:
        """
        Generate recommendations by:
        1. Retrieving the customer's interaction history.
        2. Retrieving all products.
        3. Building a mapping from product_id to category.
        4. Computing category preferences from the history (weighting 'view' as 1, 'purchase' as 2).
        5. Scoring products that the customer has not yet interacted with based on category preference.
        """
        # Retrieve interaction history and all products
        history = self.customer_agent.get_history()
        print(f"DEBUG: Customer History: {history}")

        if not history:
            print("ERROR: No customer interaction history found.")
            return []

        all_products = self.product_agent.get_all_products()
        print(f"DEBUG: All Products in DB: {all_products}")

        if not all_products:
            print("ERROR: No products found in the database!")
            return []

        # Build a mapping: product_id -> category
        prod_category_map = {product["id"]: product["category"] for product in all_products}
        
        # Compute category preferences from history.
        # Weight: 'view' = 1, 'purchase' = 2.
        category_preferences = {}
        for record in history:
            pid = record.get("product_id")
            category = prod_category_map.get(pid)
            if category:
                weight = 1 if record["interaction_type"] == "view" else 2 if record["interaction_type"] == "purchase" else 1
                category_preferences[category] = category_preferences.get(category, 0) + weight

        print("DEBUG: Computed Category Preferences:", category_preferences)

        # Determine products already interacted with
        viewed_product_ids = {record["product_id"] for record in history}
        print(f"DEBUG: Viewed Product IDs: {viewed_product_ids}")

        # Score unviewed products based on their category preference score
        scored_products = []
        for product in all_products:
            product_id = product["id"]
            if product_id in viewed_product_ids:
                print(f"DEBUG: Skipping product {product_id} (already viewed)")
                continue

            score = category_preferences.get(product["category"], 0)
            if score > 0:
                scored_products.append((score, product))
                print(f"DEBUG: Product {product_id} in category '{product['category']}' scored {score}")

        # Sort by score in descending order and pick top_n
        scored_products.sort(key=lambda x: x[0], reverse=True)
        recommended = [prod for _, prod in scored_products[:top_n]]
        print(f"DEBUG: Final Recommended Products: {recommended}")

        # 👉 Avoid adding duplicate products before returning
        if recommended:
            unique_recommendations = []
            seen_ids = set()
            for product in recommended:
                if product['id'] not in seen_ids:
                    unique_recommendations.append(product)
                    seen_ids.add(product['id'])

            return unique_recommendations

        # If no recommendations, fallback to Ollama LLM for product recommendations
        try:
            prompt = f"""
            Customer history: {history}
            Available products: {all_products}
            Recommend up to {top_n} product IDs the customer may like.
            Return a Python list of product IDs like: [1, 2, 3]
            """

            # Send request to Ollama API
            response = query_ollama(prompt, model="llama3")  # You can change the model as needed
            print(f"DEBUG: LLM Raw Response: {response}")
            
            # Parse response from Ollama
            product_ids = eval(response) if isinstance(response, str) else []

            # Map the product IDs back to products
            id_to_product = {p['id']: p for p in all_products}
            recommended_llm = [id_to_product[pid] for pid in product_ids if pid in id_to_product]

            # Avoid adding duplicate products in the LLM fallback recommendations
            unique_recommendations = []
            seen_ids = set()
            for product in recommended_llm:
                if product['id'] not in seen_ids:
                    unique_recommendations.append(product)
                    seen_ids.add(product['id'])

            return unique_recommendations

        except Exception as e:
            print(f"LLM fallback failed: {e}")
            return []
