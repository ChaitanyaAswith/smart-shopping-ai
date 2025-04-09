# agents/customer_agent.py


from memory.memory_manager import MemoryManager  # ✅ Correct if memory/ is in the root project


class CustomerAgent:
    def __init__(self, customer_id: int, memory: MemoryManager):
        self.customer_id = customer_id
        self.memory = memory
        self.profile = self.memory.get_customer_by_id(customer_id)
        self.history = self.memory.get_customer_history(customer_id)

    def get_profile(self):
        return self.profile

    def get_history(self):
        return self.history

    def summarize_preferences(self):
        """
        Analyze interaction history to guess preferences (e.g., categories viewed/purchased most).
        """
        preferences = {}
        for record in self.history:
            product_id = record["product_id"]
            interaction_type = record["interaction_type"]
            preferences[interaction_type] = preferences.get(interaction_type, 0) + 1
        return preferences
