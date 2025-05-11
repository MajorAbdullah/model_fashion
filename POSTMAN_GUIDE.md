# Fashion Recommendation API - Postman Usage Guide

This guide explains how to use the Fashion Recommendation API with Postman to interact with its endpoints.

## Getting Started

1. **Install and Set Up the API**:
   - Make sure you have the required dependencies installed: `pip install -r requirements.txt`
   - Run the API server: `python fashion_questionnaire_api.py`
   - The server will start on `http://localhost:8000` by default

2. **Launch Postman**:
   - Download Postman from [https://www.postman.com/downloads/](https://www.postman.com/downloads/) if you don't have it
   - Open Postman and create a new request collection for the Fashion API

## API Endpoints

### 1. Getting All Questions

**Request**:
- **Method**: GET
- **URL**: `http://localhost:8000/questions`
- **Description**: Retrieves all general questionnaire questions

**Example Response**:
```json
[
  {
    "id": "specific_occasion",
    "question": "What's the occasion you're looking for outfit recommendations for?",
    "options": ["Casual", "Concert", "Date", "Indoor", "Interview", "Office", "Outdoor", "Party", "Wedding"],
    "allow_multiple": false
  },
  {
    "id": "gender",
    "question": "What is your gender preference for clothing styles?",
    "options": ["Men", "Women", "Prefer not to say"],
    "allow_multiple": false
  },
  ...
]
```

### 2. Getting a Specific Question

**Request**:
- **Method**: GET
- **URL**: `http://localhost:8000/questions/{question_id}`
- **Path Parameters**:
  - `question_id`: ID of the question (e.g., "gender", "item_types", "style_vibes")

**Example Request**:
```
GET http://localhost:8000/questions/gender
```

**Example Response**:
```json
{
  "id": "gender",
  "question": "What is your gender preference for clothing styles?",
  "options": ["Men", "Women", "Prefer not to say"],
  "allow_multiple": false
}
```

### 3. Submitting Answers

**Request**:
- **Method**: POST
- **URL**: `http://localhost:8000/answers/{question_id}`
- **Path Parameters**:
  - `question_id`: ID of the question being answered
- **Headers**:
  - `Content-Type`: `application/json`
- **Body**:
  ```json
  {
    "selection": ["option1", "option2"]
  }
  ```

**Example Request for Single Selection**:
```
POST http://localhost:8000/answers/gender
Content-Type: application/json

{
  "selection": ["Men"]
}
```

**Example Request for Multiple Selections**:
```
POST http://localhost:8000/answers/item_types
Content-Type: application/json

{
  "selection": ["Jacket", "Pants", "Sneakers"]
}
```

**Example Response**:
```json
{
  "message": "Answer for gender recorded successfully",
  "current_preferences": {
    "gender": "Men",
    "item_types": [],
    "style_vibes": [],
    "favorite_colors": [],
    "preferred_materials": [],
    "key_occasions": [],
    "primary_seasons": [],
    "item_specific_preferences": {}
  }
}
```

### 4. Getting Item-Specific Questions

**Request**:
- **Method**: GET
- **URL**: `http://localhost:8000/item-specific-questions/{item_type}/{question_type}`
- **Path Parameters**:
  - `item_type`: Type of item (e.g., "Jacket", "Pants")
  - `question_type`: Type of question (e.g., "styles", "colors", "materials", "occasions", "seasons")

**Example Request**:
```
GET http://localhost:8000/item-specific-questions/Jacket/colors
```

**Example Response**:
```json
{
  "id": "jacket_colors",
  "item": "Jacket",
  "question_type": "colors",
  "question": "Which colors do you prefer for Jacket? Select up to 3.",
  "options": ["Black", "Blue", "Brown", "Gray", "Green", "Pink", "Purple", "Red", "White", "Yellow"],
  "allow_multiple": true,
  "max_selections": 3
}
```

### 5. Submitting Item-Specific Answers

**Request**:
- **Method**: POST
- **URL**: `http://localhost:8000/item-specific-answers/{item_type}/{question_type}`
- **Path Parameters**:
  - `item_type`: Type of item (e.g., "Jacket", "Pants")
  - `question_type`: Type of question (e.g., "styles", "colors", "materials", "occasions", "seasons")
- **Headers**:
  - `Content-Type`: `application/json`
- **Body**:
  ```json
  {
    "selection": ["option1", "option2"]
  }
  ```

**Example Request**:
```
POST http://localhost:8000/item-specific-answers/Jacket/colors
Content-Type: application/json

{
  "selection": ["Black", "Blue"]
}
```

**Example Response**:
```json
{
  "message": "Item-specific answer for Jacket colors recorded successfully",
  "current_preferences": {
    "gender": "Men",
    "item_types": ["Jacket", "Pants", "Sneakers"],
    "style_vibes": [],
    "favorite_colors": [],
    "preferred_materials": [],
    "key_occasions": [],
    "primary_seasons": [],
    "item_specific_preferences": {
      "jacket": {
        "colors": ["Black", "Blue"]
      }
    }
  }
}
```

### 6. Getting Current Preferences

**Request**:
- **Method**: GET
- **URL**: `http://localhost:8000/preferences`

**Example Response**:
```json
{
  "gender": "Men",
  "item_types": ["Jacket", "Pants", "Sneakers"],
  "style_vibes": ["Casual", "Preppy"],
  "favorite_colors": ["Black", "Blue", "Gray"],
  "preferred_materials": ["Cotton", "Denim"],
  "key_occasions": ["Casual", "Office"],
  "primary_seasons": ["Autumn", "Winter"],
  "casual_outfit_style": "Casual",
  "formal_outfit_color": null,
  "specific_occasion": "Office",
  "item_specific_preferences": {
    "jacket": {
      "colors": ["Black", "Blue"],
      "materials": ["Cotton"]
    },
    "pants": {
      "colors": ["Black", "Gray"],
      "materials": ["Denim"]
    }
  }
}
```

### 7. Setting Complete Preferences

**Request**:
- **Method**: POST
- **URL**: `http://localhost:8000/preferences`
- **Headers**:
  - `Content-Type`: `application/json`
- **Body**:
  ```json
  {
    "gender": "Men",
    "item_types": ["Jacket", "Pants", "Sneakers"],
    "style_vibes": ["Casual", "Preppy"],
    "favorite_colors": ["Black", "Blue", "Gray"],
    "preferred_materials": ["Cotton", "Denim"],
    "key_occasions": ["Casual", "Office"],
    "primary_seasons": ["Autumn", "Winter"],
    "casual_outfit_style": "Casual",
    "formal_outfit_color": null,
    "specific_occasion": "Office",
    "item_specific_preferences": {
      "jacket": {
        "colors": ["Black", "Blue"],
        "materials": ["Cotton"]
      }
    }
  }
  ```

**Example Response**:
```json
{
  "message": "Preferences updated successfully",
  "preferences": {
    "gender": "Men",
    "item_types": ["Jacket", "Pants", "Sneakers"],
    "style_vibes": ["Casual", "Preppy"],
    "favorite_colors": ["Black", "Blue", "Gray"],
    "preferred_materials": ["Cotton", "Denim"],
    "key_occasions": ["Casual", "Office"],
    "primary_seasons": ["Autumn", "Winter"],
    "casual_outfit_style": "Casual",
    "formal_outfit_color": null,
    "specific_occasion": "Office",
    "item_specific_preferences": {
      "jacket": {
        "colors": ["Black", "Blue"],
        "materials": ["Cotton"]
      }
    }
  }
}
```

### 8. Getting Recommendations

**Request**:
- **Method**: GET
- **URL**: `http://localhost:8000/recommendations`

**Example Response**:
```json
{
  "outfits": [
    {
      "outfit_number": 1,
      "components": {
        "topwear": "Blue cotton jacket with minimalist design",
        "bottomwear": "Dark gray slim-fit jeans",
        "footwear": "Black leather sneakers with white sole"
      }
    },
    {
      "outfit_number": 2,
      "components": {
        "topwear": "Black denim jacket with minimal branding",
        "bottomwear": "Light blue straight-cut jeans",
        "footwear": "Gray canvas sneakers"
      }
    }
  ]
}
```

### 9. Resetting the Session

**Request**:
- **Method**: POST
- **URL**: `http://localhost:8000/reset`

**Example Response**:
```json
{
  "message": "Session reset successfully"
}
```

## Creating a Postman Collection

You can set up a Postman collection to easily test all API endpoints:

1. Create a new collection named "Fashion Recommendation API"
2. Create folders for different types of requests (Questions, Answers, Preferences, Recommendations)
3. Add requests for each endpoint
4. Create environment variables:
   - `baseUrl`: `http://localhost:8000`
   - Use this variable in your requests as `{{baseUrl}}/questions` etc.

## Sample Workflow

Here's a typical workflow for using the API:

1. Get all questions (`GET /questions`)
2. Answer questions one by one:
   - Answer specific occasion (`POST /answers/specific_occasion`)
   - Answer gender preference (`POST /answers/gender`)
   - Answer item types (`POST /answers/item_types`)
   - Answer style vibes (`POST /answers/style_vibes`)
   - Answer favorite colors (`POST /answers/favorite_colors`)
   - Answer preferred materials (`POST /answers/preferred_materials`)
   - Answer key occasions (`POST /answers/key_occasions`)
   - Answer primary seasons (`POST /answers/primary_seasons`)
3. For each selected item type (e.g., Jacket), answer item-specific questions:
   - Answer item styles (`POST /item-specific-answers/Jacket/styles`)
   - Answer item colors (`POST /item-specific-answers/Jacket/colors`)
   - Answer item materials (`POST /item-specific-answers/Jacket/materials`)
   - Answer item occasions (`POST /item-specific-answers/Jacket/occasions`)
   - Answer item seasons (`POST /item-specific-answers/Jacket/seasons`)
4. Get recommendations (`GET /recommendations`)
5. Reset session when done (`POST /reset`)

## Troubleshooting

1. **Connection Refused**: Make sure the API server is running at the specified address
2. **Invalid Request Body**: Double-check the JSON format of your request bodies
3. **404 Not Found**: Verify the URL and endpoint paths
4. **400 Bad Request**: Check that your selections match the allowed values for each question
5. **500 Server Error**: Look at the server logs for more details

## API Walkthrough Video

For a visual guide on how to use this API with Postman, check out our walkthrough video at [link to video].
