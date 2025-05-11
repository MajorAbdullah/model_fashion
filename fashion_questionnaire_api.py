#!/usr/bin/env python3
"""
Fashion Recommendation Questionnaire API

This script provides a FastAPI interface for the Fashion Recommendation Questionnaire,
allowing users to answer questions and receive personalized recommendations via API endpoints.
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import uvicorn
import json
import os

from fashion_recommender import FashionRecommender
from fashion_questionnaire import FashionQuestionnaire

# Get the dataset path
current_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_dir, "fashion_dataset_updated.csv")

# Initialize the recommender and questionnaire
recommender = FashionRecommender(dataset_path)
questionnaire = FashionQuestionnaire(recommender)

# Create FastAPI app
app = FastAPI(
    title="Fashion Questionnaire API",
    description="API for collecting fashion preferences and providing personalized recommendations",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define Pydantic models for request and response

class QuestionResponse(BaseModel):
    question: str = Field(..., description="The question text")
    options: List[str] = Field(..., description="Available options for the question")
    allow_multiple: bool = Field(False, description="Whether multiple selections are allowed")
    max_selections: Optional[int] = Field(None, description="Maximum number of selections allowed if multiple")

class UserSelection(BaseModel):
    selection: List[str] = Field(..., description="User's selected option(s)")

class SpecificOccasionQuestion(BaseModel):
    id: str = "specific_occasion"
    question: str = "What's the occasion you're looking for outfit recommendations for?"
    options: List[str] = questionnaire.OCCASIONS
    allow_multiple: bool = False
    
class GenderQuestion(BaseModel):
    id: str = "gender"
    question: str = "What is your gender preference for clothing styles?"
    options: List[str] = questionnaire.GENDERS
    allow_multiple: bool = False
    
class ItemTypesQuestion(BaseModel):
    id: str = "item_types"
    question: str = "Which clothing or accessory items are you interested in? Select all that apply."
    options: List[str] = questionnaire.ITEM_TYPES
    allow_multiple: bool = True
    
class StyleVibesQuestion(BaseModel):
    id: str = "style_vibes"
    question: str = "What style vibes do you generally prefer across your wardrobe? Select up to 3."
    options: List[str] = questionnaire.STYLES
    allow_multiple: bool = True
    max_selections: int = 3
    
class ColorsQuestion(BaseModel):
    id: str = "favorite_colors"
    question: str = "What colors do you love to wear? Select up to 5."
    options: List[str] = questionnaire.COLORS
    allow_multiple: bool = True
    max_selections: int = 5
    
class MaterialsQuestion(BaseModel):
    id: str = "preferred_materials"
    question: str = "What fabrics or materials do you prefer for your clothing? Select up to 3."
    options: List[str] = questionnaire.MATERIALS
    allow_multiple: bool = True
    max_selections: int = 3
    
class OccasionsQuestion(BaseModel):
    id: str = "key_occasions"
    question: str = "For which occasions do you often need outfits? Select all that apply."
    options: List[str] = questionnaire.OCCASIONS
    allow_multiple: bool = True
    
class SeasonsQuestion(BaseModel):
    id: str = "primary_seasons"
    question: str = "Which seasons do you primarily shop for or style outfits for? Select all that apply."
    options: List[str] = questionnaire.SEASONS
    allow_multiple: bool = True
    
class CasualOutfitStyleQuestion(BaseModel):
    id: str = "casual_outfit_style"
    question: str = "For a casual occasion in your favorite season, what style vibe do you prefer for an outfit?"
    options: List[str] = questionnaire.STYLES
    allow_multiple: bool = False
    
class FormalOutfitColorQuestion(BaseModel):
    id: str = "formal_outfit_color"
    question: str = "For a formal event like a wedding or interview, what color do you prefer for your main clothing item?"
    options: List[str] = questionnaire.COLORS
    allow_multiple: bool = False

class ItemSpecificQuestion(BaseModel):
    id: str
    item: str
    question_type: str  # "styles", "colors", "materials", "occasions", "seasons"
    question: str
    options: List[str]
    allow_multiple: bool = True
    max_selections: Optional[int] = None

class OutfitComponent(BaseModel):
    category: str
    item: str

class OutfitRecommendation(BaseModel):
    outfit_number: int
    components: Dict[str, str]

class RecommendationsResponse(BaseModel):
    outfits: List[OutfitRecommendation]

class UserPreferences(BaseModel):
    gender: Optional[str] = None
    item_types: List[str] = []
    style_vibes: List[str] = []
    favorite_colors: List[str] = []
    preferred_materials: List[str] = []
    key_occasions: List[str] = []
    primary_seasons: List[str] = []
    casual_outfit_style: Optional[str] = None
    formal_outfit_color: Optional[str] = None
    specific_occasion: Optional[str] = None
    item_specific_preferences: Dict[str, Dict[str, List[str]]] = {}

# Global variable to store session state
sessions = {}

@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to the Fashion Questionnaire API",
        "version": "1.0.0",
        "endpoints": {
            "GET /questions": "Get all questionnaire questions",
            "GET /questions/{question_id}": "Get a specific question",
            "POST /answers/{question_id}": "Submit answer(s) to a specific question",
            "GET /item-specific-questions/{item_type}/{question_type}": "Get item-specific questions",
            "POST /item-specific-answers/{item_type}/{question_type}": "Submit answers to item-specific questions",
            "GET /preferences": "Get current user preferences",
            "POST /preferences": "Submit complete user preferences",
            "GET /recommendations": "Get fashion recommendations based on current preferences",
            "POST /reset": "Reset the questionnaire session"
        }
    }



@app.get("/questions", tags=["Questions"], response_model=List[Dict[str, Any]])
def get_all_questions():
    """Get all general questionnaire questions."""
    questions = [
        SpecificOccasionQuestion().dict(),
        GenderQuestion().dict(),
        ItemTypesQuestion().dict(),
        StyleVibesQuestion().dict(),
        ColorsQuestion().dict(),
        MaterialsQuestion().dict(),
        OccasionsQuestion().dict(),
        SeasonsQuestion().dict(),
        CasualOutfitStyleQuestion().dict(),
        FormalOutfitColorQuestion().dict()
    ]
    return questions

@app.get("/questions/{question_id}", tags=["Questions"])
def get_question(question_id: str):
    """Get a specific questionnaire question."""
    questions_map = {
        "specific_occasion": SpecificOccasionQuestion(),
        "gender": GenderQuestion(),
        "item_types": ItemTypesQuestion(),
        "style_vibes": StyleVibesQuestion(),
        "favorite_colors": ColorsQuestion(),
        "preferred_materials": MaterialsQuestion(),
        "key_occasions": OccasionsQuestion(),
        "primary_seasons": SeasonsQuestion(),
        "casual_outfit_style": CasualOutfitStyleQuestion(),
        "formal_outfit_color": FormalOutfitColorQuestion()
    }
    
    if question_id not in questions_map:
        raise HTTPException(status_code=404, detail=f"Question ID '{question_id}' not found")
    
    return questions_map[question_id].dict()

@app.post("/answers/{question_id}", tags=["Answers"])
def submit_answer(question_id: str, user_selection: UserSelection):
    """Submit answer(s) to a specific question."""
    # Initialize session if needed
    session_id = "default"  # In a real app, you would use proper session management
    if session_id not in sessions:
        sessions[session_id] = UserPreferences()
    
    # Validate question ID
    valid_fields = [
        "specific_occasion", "gender", "item_types", "style_vibes", 
        "favorite_colors", "preferred_materials", "key_occasions", 
        "primary_seasons", "casual_outfit_style", "formal_outfit_color"
    ]
    
    if question_id not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid question ID: {question_id}")
    
    # Validate and store the answers
    if question_id in ["gender", "casual_outfit_style", "formal_outfit_color", "specific_occasion"]:
        if len(user_selection.selection) > 1:
            raise HTTPException(status_code=400, detail=f"Question {question_id} only accepts a single selection")
        if user_selection.selection:
            setattr(sessions[session_id], question_id, user_selection.selection[0])
    else:
        # For list fields (multiple selections)
        if question_id == "style_vibes" and len(user_selection.selection) > 3:
            raise HTTPException(status_code=400, detail="Style vibes allows maximum 3 selections")
        elif question_id == "favorite_colors" and len(user_selection.selection) > 5:
            raise HTTPException(status_code=400, detail="Favorite colors allows maximum 5 selections")
        elif question_id == "preferred_materials" and len(user_selection.selection) > 3:
            raise HTTPException(status_code=400, detail="Preferred materials allows maximum 3 selections")
        
        setattr(sessions[session_id], question_id, user_selection.selection)
    
    return {"message": f"Answer for {question_id} recorded successfully", "current_preferences": sessions[session_id]}

@app.get("/item-specific-questions/{item_type}/{question_type}", tags=["Item-Specific Questions"])
def get_item_specific_question(item_type: str, question_type: str):
    """Get item-specific questions for a particular item type."""
    # Validate item type
    if item_type not in questionnaire.ITEM_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid item type: {item_type}")
    
    # Validate question type
    question_types = {"styles": questionnaire.STYLES, "colors": questionnaire.COLORS, 
                     "materials": questionnaire.MATERIALS, "occasions": questionnaire.OCCASIONS, 
                     "seasons": questionnaire.SEASONS}
    
    if question_type not in question_types:
        raise HTTPException(status_code=400, detail=f"Invalid question type: {question_type}")
    
    # Create question based on type
    question_texts = {
        "styles": f"Which style vibes do you prefer for {item_type}? Select up to 2.",
        "colors": f"Which colors do you prefer for {item_type}? Select up to 3.",
        "materials": f"Which materials do you prefer for {item_type}? Select up to 2.",
        "occasions": f"For which occasions do you wear {item_type}? Select all that apply.",
        "seasons": f"For which seasons do you wear {item_type}? Select all that apply."
    }
    
    max_selections = {"styles": 2, "colors": 3, "materials": 2, "occasions": None, "seasons": None}
    
    question = ItemSpecificQuestion(
        id=f"{item_type.lower()}_{question_type}",
        item=item_type,
        question_type=question_type,
        question=question_texts[question_type],
        options=question_types[question_type],
        allow_multiple=True,
        max_selections=max_selections[question_type]
    )
    
    return question.dict()

@app.post("/item-specific-answers/{item_type}/{question_type}", tags=["Item-Specific Answers"])
def submit_item_specific_answer(item_type: str, question_type: str, user_selection: UserSelection):
    """Submit answer(s) to an item-specific question."""
    # Initialize session if needed
    session_id = "default"
    if session_id not in sessions:
        sessions[session_id] = UserPreferences()
    
    # Validate item type
    if item_type.title() not in questionnaire.ITEM_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid item type: {item_type}")
    
    # Validate question type
    if question_type not in ["styles", "colors", "materials", "occasions", "seasons"]:
        raise HTTPException(status_code=400, detail=f"Invalid question type: {question_type}")
    
    # Validate number of selections
    max_selections = {"styles": 2, "colors": 3, "materials": 2}
    if question_type in max_selections and len(user_selection.selection) > max_selections[question_type]:
        raise HTTPException(
            status_code=400, 
            detail=f"{question_type.capitalize()} for {item_type} allows maximum {max_selections[question_type]} selections"
        )
    
    # Initialize item-specific preferences if needed
    item_key = item_type.lower()
    if "item_specific_preferences" not in sessions[session_id].dict() or not sessions[session_id].item_specific_preferences:
        sessions[session_id].item_specific_preferences = {}
    
    if item_key not in sessions[session_id].item_specific_preferences:
        sessions[session_id].item_specific_preferences[item_key] = {}
    
    # Store the answers
    sessions[session_id].item_specific_preferences[item_key][question_type] = user_selection.selection
    
    return {
        "message": f"Item-specific answer for {item_type} {question_type} recorded successfully", 
        "current_preferences": sessions[session_id]
    }

@app.get("/preferences", tags=["Preferences"], response_model=UserPreferences)
def get_preferences():
    """Get the current user preferences."""
    session_id = "default"
    if session_id not in sessions:
        sessions[session_id] = UserPreferences()
    
    return sessions[session_id]

@app.post("/preferences", tags=["Preferences"])
def set_preferences(preferences: UserPreferences):
    """Set complete user preferences."""
    session_id = "default"
    sessions[session_id] = preferences
    
    return {"message": "Preferences updated successfully", "preferences": preferences}

@app.get("/recommendations", tags=["Recommendations"], response_model=RecommendationsResponse)
def get_recommendations():
    """Get fashion recommendations based on current preferences."""
    session_id = "default"
    if session_id not in sessions:
        raise HTTPException(status_code=400, detail="No preferences set. Please answer questionnaire first.")
    
    user_preferences = sessions[session_id].dict()
    
    # Process preferences to get tags
    tags = recommender.process_user_preferences(user_preferences)
    
    # Add specific occasion if provided
    if "specific_occasion" in user_preferences and user_preferences["specific_occasion"]:
        tags.append(user_preferences["specific_occasion"].lower())
    
    # Add casual outfit style if provided
    if "casual_outfit_style" in user_preferences and user_preferences["casual_outfit_style"]:
        if "specific_occasion" in user_preferences and user_preferences["specific_occasion"] == "Casual":
            tags.append(user_preferences["casual_outfit_style"].lower())
    
    # Add formal outfit color if provided
    if "formal_outfit_color" in user_preferences and user_preferences["formal_outfit_color"]:
        if "specific_occasion" in user_preferences and user_preferences["specific_occasion"] in ["Wedding", "Interview"]:
            tags.append(user_preferences["formal_outfit_color"].lower())
    
    # Get recommendations based on tags
    outfits = recommender.get_recommendations_from_tags(tags)
    
    # Format recommendations for display
    formatted_outfits = recommender.format_outfit_recommendations(outfits)
    
    return {"outfits": formatted_outfits}

@app.post("/reset", tags=["Session"])
def reset_session():
    """Reset the questionnaire session."""
    session_id = "default"
    sessions[session_id] = UserPreferences()
    
    return {"message": "Session reset successfully"}

if __name__ == "__main__":
    uvicorn.run("fashion_questionnaire_api:app", host="0.0.0.0", port=8000, reload=True)
