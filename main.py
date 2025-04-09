import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.recommender import router as recommender_router

app = FastAPI()

# Serve images from the /images folder
app.mount("/images", StaticFiles(directory="images"), name="images")

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(recommender_router)

# Root route for base URL
@app.get("/")
def root():
    return {"message": "Smart Shopping API is up and running 🚀"}