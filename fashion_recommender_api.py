#!/usr/bin/env python3
"""
Fashion Recommendation System API

This script provides a FastAPI interface for the Fashion Recommendation System,
which can be used for external communication.
"""
from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import uvicorn
import json

import os
from fashion_recommender import FashionRecommender

# Get the dataset path
current_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_dir, "fashion_dataset_updated.csv")

# Initialize the recommender
recommender = FashionRecommender(dataset_path)

# Create FastAPI app
app = FastAPI(
    title="Fashion Recommendation API",
    description="API for recommending personalized fashion wardrobe pieces",
    version="1.0.0"
)

# Define Pydantic models for request and response
class TagRequest(BaseModel):
    tags: List[str] = Field(..., description="List of tags to use for recommendations")
    count: int = Field(7, description="Number of recommendations to generate")

class QuestionRequest(BaseModel):
    text: str = Field(..., description="Natural language question for fashion recommendations")
    count: int = Field(7, description="Number of recommendations to generate")

class PreferencesRequest(BaseModel):
    preferences: Dict[str, Any] = Field(..., description="User preferences for fashion recommendations")
    count: int = Field(7, description="Number of recommendations to generate")

class OutfitComponent(BaseModel):
    category: str = Field(..., description="Category of the clothing item")
    item: str = Field(..., description="Description of the clothing item")

class Outfit(BaseModel):
    outfit_number: int = Field(..., description="Number of the outfit")
    components: Dict[str, str] = Field(..., description="Components of the outfit")

class RecommendationResponse(BaseModel):
    outfits: List[Outfit] = Field(..., description="List of recommended outfits")
    source: str = Field(..., description="Source of the recommendations")


@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "name": "Fashion Recommendation API",
        "version": "1.0.0",
        "description": "API for recommending personalized fashion wardrobe pieces"
    }


@app.post("/recommendations/question", response_model=RecommendationResponse)
def get_recommendations_from_question(request: QuestionRequest):
    """Get recommendations based on a natural language question"""
    try:
        outfits = recommender.get_recommendations_from_question(request.text, request.count)
        formatted_outfits = recommender.format_outfit_recommendations(outfits)
        return {
            "outfits": formatted_outfits,
            "source": f"Question: {request.text}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.post("/recommendations/tags", response_model=RecommendationResponse)
def get_recommendations_from_tags(request: TagRequest):
    """Get recommendations based on a list of tags"""
    try:
        outfits = recommender.get_recommendations_from_tags(request.tags, request.count)
        formatted_outfits = recommender.format_outfit_recommendations(outfits)
        return {
            "outfits": formatted_outfits,
            "source": f"Tags: {', '.join(request.tags)}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.post("/recommendations/preferences", response_model=RecommendationResponse)
def get_recommendations_from_preferences(request: PreferencesRequest):
    """Get recommendations based on user preferences"""
    try:
        tags = recommender.process_user_preferences(request.preferences)
        outfits = recommender.get_recommendations_from_tags(tags, request.count)
        formatted_outfits = recommender.format_outfit_recommendations(outfits)
        return {
            "outfits": formatted_outfits,
            "source": f"User preferences with {len(tags)} extracted tags"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("fashion_recommender_api:app", host="0.0.0.0", port=8000, reload=True)
