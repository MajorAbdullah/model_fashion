# Fashion Recommendation API

A RESTful API for collecting fashion preferences and providing personalized outfit recommendations.

## Features

- Recommends complete outfits with 3 mandatory components (topwear, bottomwear, footwear)
- Optional jewelry/accessories based on context
- Structured questionnaire-based approach to gather user preferences
- API endpoints for:
  - Getting questionnaire questions
  - Submitting answers
  - Managing user preferences
  - Generating personalized recommendations
- Fast and efficient tag-based retrieval system
- Interactive API documentation with Swagger UI

## Project Structure

```
model_fashion/
├── examples/                       # Example files
│   └── sample_preferences.json     # Sample user preferences
├── tests/                          # Test files
│   └── test_fashion_recommender.py # Unit tests
├── fashion_dataset_updated.csv     # Fashion item dataset
├── fashion_recommender.py          # Core recommendation engine
├── fashion_questionnaire_api.py    # REST API using FastAPI
├── POSTMAN_GUIDE.md                # Detailed guide for using the API with Postman
├── Fashion_API_Postman_Collection.json # Ready-to-import Postman collection
├── README.md                       # Documentation
└── requirements.txt                # Dependencies
```

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## API Usage

Start the API server:

```bash
python fashion_questionnaire_api.py
```

The API will be available at `http://0.0.0.0:8000` with the following endpoints:

### Endpoints Overview

- `GET /questions` - Get all questionnaire questions
- `GET /questions/{question_id}` - Get a specific question
- `POST /answers/{question_id}` - Submit an answer to a question
- `GET /item-specific-questions/{item_type}/{question_type}` - Get item-specific questions
- `POST /item-specific-answers/{item_type}/{question_type}` - Submit item-specific answers
- `GET /preferences` - Get current user preferences
- `POST /preferences` - Submit complete user preferences
- `GET /recommendations` - Get personalized outfit recommendations
- `POST /reset` - Reset the session

For interactive API documentation, visit:
- Swagger UI: `http://0.0.0.0:8000/docs`
- ReDoc: `http://0.0.0.0:8000/redoc`

## Postman Integration

The repository includes a comprehensive Postman collection for testing the API:

1. Import `Fashion_API_Postman_Collection.json` into Postman
2. Create an environment with variable `baseUrl` set to `http://0.0.0.0:8000`
3. Follow the workflow outlined in the [POSTMAN_GUIDE.md](./POSTMAN_GUIDE.md) document

## Example API Usage Flow

This example demonstrates a typical interaction flow with the API:

### 1. Get all questions

```bash
curl -X 'GET' 'http://0.0.0.0:8000/questions'
```

### 2. Submit an answer to a question

```bash
curl -X 'POST' 'http://0.0.0.0:8000/answers/1' \
  -H 'Content-Type: application/json' \
  -d '{"answer": "Male"}'
```

### 3. Get item-specific questions for topwear

```bash
curl -X 'GET' 'http://0.0.0.0:8000/item-specific-questions/topwear/styles'
```

### 4. Submit answers to item-specific questions

```bash
curl -X 'POST' 'http://0.0.0.0:8000/item-specific-answers/topwear/styles' \
  -H 'Content-Type: application/json' \
  -d '{"answers": ["Casual", "Formal"]}'
```

### 5. Get personalized recommendations

```bash
curl -X 'GET' 'http://0.0.0.0:8000/recommendations'
```

For more detailed examples and usage information, refer to the [Postman Guide](./POSTMAN_GUIDE.md).

## Technical Implementation

### API Architecture
- **Framework**: FastAPI for high-performance API endpoints
- **State Management**: Session-based preference tracking
- **Documentation**: Automatic generation of OpenAPI schema

### Recommendation Engine
- **Algorithm**: TF-IDF vectorization and cosine similarity for matching user preferences with fashion items
- **Approach**: Preference-based filtering with tag matching
- **Performance**: Optimized for speed with pre-computed vectors and caching

## Dataset

The dataset consists of fashion items with the following attributes:
- Item type (topwear, bottomwear, footwear, accessories)
- Style tags (casual, formal, sporty, etc.)
- Colors and materials
- Occasions and seasons
- Gender-specific attributes

## Testing the API

You can test the API using the following approaches:

1. **Using the Swagger UI**: Visit `http://0.0.0.0:8000/docs` for interactive testing
2. **Using Postman**: Follow the [Postman Guide](./POSTMAN_GUIDE.md) and import the collection
3. **Using curl**: See the example commands in this README
4. **Using a REST client**: Any REST client that can make HTTP requests

## Future Improvements

- Adding authentication for personalized user profiles
- Implementing machine learning to improve recommendations over time
- Integrating image previews for recommended items
- Adding support for user feedback on recommendations
