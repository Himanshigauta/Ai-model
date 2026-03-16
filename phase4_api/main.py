import sys
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

# Add parent directory to sys.path to allow importing from phase2 and phase3
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from phase2_retrieval.retrieval import get_recommendations
from phase3_llm_integration.llm_agent import construct_prompt, generate_recommendation

app = FastAPI(
    title="AI Restaurant Recommendation Service",
    description="API for fetching restaurant recommendations based on constraints, formatted nicely by an LLM.",
    version="1.0.0"
)

# Pydantic schema for the request
class RecommendationRequest(BaseModel):
    place: Optional[str] = Field(default=None, description="Location to search in, e.g. 'Banashankari'")
    cuisine: Optional[str] = Field(default=None, description="Preferred cuisine, e.g. 'North Indian'")
    max_price: Optional[int] = Field(default=None, description="Maximum cost for two people")
    min_rating: Optional[float] = Field(default=None, description="Minimum rating out of 5, e.g. 4.0")
    
class RecommendationResponse(BaseModel):
    status: str
    recommendation: str
    restaurants: list = []

@app.post("/api/recommend", response_model=RecommendationResponse)
async def recommend_restaurants(req: RecommendationRequest):
    db_path = str(root_dir / "phase1_data_pipeline" / "zomato_cleaned.db")
    
    # Validation step
    if not os.path.exists(db_path):
        raise HTTPException(status_code=500, detail="Database not found. Please ensure Phase 1 has completed.")

    try:
        # Phase 2: Retrieval
        df = get_recommendations(
            db_path=db_path,
            place=req.place,
            cuisine=req.cuisine,
            max_price=req.max_price,
            min_rating=req.min_rating,
            top_n=5
        )
        
        # Convert df to dictionary format expected by LLM phase
        retrieved_docs = df.to_dict('records')
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database retrieval failed: {str(e)}")

    try:
        # Phase 3: LLM generation
        user_prefs = req.model_dump()
        prompt = construct_prompt(user_prefs, retrieved_docs)
        
        response_text = generate_recommendation(prompt)
        
        if response_text.startswith("Error:"):
            # A graceful failure if API key is somewhat messed up later
            return {"status": "error", "recommendation": response_text}
            
        return {"status": "success", "recommendation": response_text, "restaurants": retrieved_docs}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Integration failed: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
