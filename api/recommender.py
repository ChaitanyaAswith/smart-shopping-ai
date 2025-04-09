from fastapi import APIRouter, HTTPException
from agents.recommender_agent import RecommenderAgent
from memory.memory_manager import MemoryManager
from agents.customer_agent import CustomerAgent

router = APIRouter()

@router.get("/recommend/{customer_id}")
async def get_recommendations(customer_id: int):
    memory = MemoryManager()

    # Ensure that the customer exists in the database
    customer = memory.get_customer_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Create the recommender agent
    recommender = RecommenderAgent(customer_id, memory)

    # Get recommended product IDs (check if recommend() returns product IDs or full product details)
    recommended_products = recommender.recommend()

    # Extract only product IDs if full products are returned by the recommender
    recommended_ids = [
        p['id'] if isinstance(p, dict) else p  # If the product is a dict, extract the 'id'
        for p in recommended_products
    ]

    # Get the full product details from memory
    all_products = memory.get_all_products()
    product_dict = {product['id']: product for product in all_products}

    # Ensure that we handle invalid or missing products gracefully
    detailed_recommendations = [
        product_dict[pid]
        for pid in recommended_ids
        if pid in product_dict  # Ensure the product ID exists in the database
    ]

    # Check if recommendations are found, if not return a message
    if not detailed_recommendations:
        raise HTTPException(status_code=404, detail="No products found for recommendations")

    # Close the memory manager to free up resources
    memory.close()

    return {
        "customer_id": customer_id,
        "recommendations": detailed_recommendations
    }
