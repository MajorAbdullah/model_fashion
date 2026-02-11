# Fashion Recommendation API

**Personalized outfit recommendations powered by TF-IDF and cosine similarity**

Fashion Recommendation API is a Python-based system that suggests complete outfits (topwear, bottomwear, footwear, and optional accessories) based on user preferences, natural language questions, or tag-based queries. It exposes two FastAPI services -- a direct recommendation API and a structured questionnaire-based API -- and includes pre-trained ML models for classification.

---

## Features

- Recommends complete outfits with 3 mandatory components (topwear, bottomwear, footwear) plus optional accessories
- Three input modes: natural language questions, tag lists, or structured user preferences
- Structured questionnaire flow that collects gender, style, color, material, occasion, and season preferences
- Item-specific preference questions for granular control per clothing category
- TF-IDF vectorization with cosine similarity for fast, relevant matching
- Interactive API documentation via Swagger UI and ReDoc
- Session-based preference tracking across API calls
- CORS-enabled for cross-origin frontend integration
- Postman collection and guide included for API testing
- Deployable to Render via included configuration
- Pre-trained Random Forest, XGBoost, and LightGBM models included

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0-150458?style=for-the-badge&logo=pandas&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![Render](https://img.shields.io/badge/Render-Deploy-46E3B7?style=for-the-badge&logo=render&logoColor=white)

| Component | Technology |
|-----------|-----------|
| API Framework | FastAPI + Uvicorn |
| Recommendation Engine | TF-IDF (scikit-learn) + Cosine Similarity |
| Data Processing | Pandas, NumPy |
| ML Models | Random Forest, XGBoost, LightGBM (pre-trained .pkl files) |
| Deep Learning | TensorFlow 2.10, TensorFlow Hub |
| Validation | Pydantic 2.6 |
| Deployment | Render (Gunicorn + Flask entry point) |
| Testing | Postman collection included |

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/MajorAbdullah/model_fashion.git
cd model_fashion

# Install dependencies
pip install -r requirements.txt
```

### Running the API

**Questionnaire API** (structured preference collection + recommendations):

```bash
python fashion_questionnaire_api.py
```

**Direct Recommendation API** (question/tag/preference-based):

```bash
python fashion_recommender_api.py
```

Both APIs start at `http://0.0.0.0:8000`.

- Swagger UI: `http://0.0.0.0:8000/docs`
- ReDoc: `http://0.0.0.0:8000/redoc`

**CLI Mode** (for quick testing without an API server):

```bash
# Natural language query
python fashion_recommender.py --query "What should I wear for a casual summer event?"

# Tag-based query
python fashion_recommender.py --tags "casual,summer,blue"

# From a preferences JSON file
python fashion_recommender.py --preferences examples/sample_preferences.json

# JSON output format
python fashion_recommender.py --query "formal winter outfit" --output json
```

---

## API Endpoints

### Questionnaire API (`fashion_questionnaire_api.py`)

| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/questions` | Get all questionnaire questions |
| GET | `/questions/{question_id}` | Get a specific question |
| POST | `/answers/{question_id}` | Submit answer(s) to a question |
| GET | `/item-specific-questions/{item_type}/{question_type}` | Get item-specific questions |
| POST | `/item-specific-answers/{item_type}/{question_type}` | Submit item-specific answers |
| GET | `/preferences` | Get current session preferences |
| POST | `/preferences` | Submit complete user preferences |
| GET | `/recommendations` | Get outfit recommendations from current preferences |
| POST | `/reset` | Reset the questionnaire session |

### Direct Recommendation API (`fashion_recommender_api.py`)

| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/recommendations/question` | Get recommendations from a natural language question |
| POST | `/recommendations/tags` | Get recommendations from a list of tags |
| POST | `/recommendations/preferences` | Get recommendations from structured preferences |

---

## Example API Usage

### 1. Get all questionnaire questions

```bash
curl -X GET http://0.0.0.0:8000/questions
```

### 2. Submit an answer

```bash
curl -X POST http://0.0.0.0:8000/answers/gender \
  -H 'Content-Type: application/json' \
  -d '{"selection": ["Male"]}'
```

### 3. Get item-specific questions

```bash
curl -X GET http://0.0.0.0:8000/item-specific-questions/Shirt/styles
```

### 4. Get recommendations

```bash
curl -X GET http://0.0.0.0:8000/recommendations
```

### 5. Direct recommendation via tags

```bash
curl -X POST http://0.0.0.0:8000/recommendations/tags \
  -H 'Content-Type: application/json' \
  -d '{"tags": ["casual", "summer", "blue", "cotton"], "count": 5}'
```

---

## Project Structure

```
model_fashion/
├── fashion_recommender.py              # Core recommendation engine (TF-IDF + cosine similarity)
├── fashion_questionnaire.py            # Questionnaire logic and preference processing
├── fashion_questionnaire_api.py        # FastAPI questionnaire-based API
├── fashion_recommender_api.py          # FastAPI direct recommendation API
├── app.py                              # Flask entry point for Render deployment
├── fashion_dataset_updated.csv         # Fashion item dataset with tags
├── requirements.txt                    # Python dependencies
├── render.yaml                         # Render deployment configuration
├── models/                             # Pre-trained ML model files
│   ├── rf_item.pkl                     # Random Forest (item classification)
│   ├── rf_multilabel.pkl               # Random Forest (multi-label)
│   ├── xgb_item.pkl                    # XGBoost (item classification)
│   ├── xgb_multilabel.pkl              # XGBoost (multi-label)
│   ├── lgb_item.pkl                    # LightGBM (item classification)
│   └── lgb_multilabel.pkl              # LightGBM (multi-label)
├── examples/
│   └── sample_preferences.json         # Example user preferences input
├── tests/
│   └── test_fashion_recommender.py     # Unit tests
├── Fashion_API_Postman_Collection.json # Ready-to-import Postman collection
├── POSTMAN_GUIDE.md                    # Detailed Postman testing guide
├── DETAILED_DEPLOYMENT_GUIDE.md        # Deployment instructions
├── model_comparison.md                 # ML model evaluation and comparison
└── README.md
```

---

## Postman Integration

1. Import `Fashion_API_Postman_Collection.json` into Postman
2. Create an environment with the variable `baseUrl` set to `http://0.0.0.0:8000`
3. Follow the workflow described in [POSTMAN_GUIDE.md](./POSTMAN_GUIDE.md)

---

## Deployment

The project includes a `render.yaml` for one-click deployment to Render:

```yaml
services:
  - type: web
    name: fashion-model-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --bind 0.0.0.0:$PORT app:app
```

The `app.py` Flask entry point serves as the production gateway.

---

## Dataset

The fashion dataset (`fashion_dataset_updated.csv`) contains items tagged with:

- Item type (topwear, bottomwear, footwear, accessories)
- Style tags (casual, formal, sporty, boho, vintage, etc.)
- Colors and materials
- Occasions (office, party, wedding, date, interview, etc.)
- Seasons (spring, summer, autumn, winter)
- Gender-specific attributes

---

## License

MIT License

## Author

**Syed Abdullah Shah** -- [@MajorAbdullah](https://github.com/MajorAbdullah)
