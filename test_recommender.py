from memory.memory_manager import MemoryManager
from agents.recommender_agent import RecommenderAgent

def test_recommender():
    memory = MemoryManager()
    recommender = RecommenderAgent(customer_id=1, memory=memory)
    recommendations = recommender.recommend()
    print("Final Recommendations:", recommendations)
    memory.close()

if __name__ == "__main__":
    test_recommender()
