# Quote Manager (Enhanced Quote Generator)

## Overview
This project is an **enhanced version** of the original Quote Generator app.  
The original app only displayed a random quote.  
I upgraded it into a **Quote Manager** where users can **add, edit, and delete quotes** via a user-friendly web interface, and also access the same functionality through a REST API.

---

## Features
- View all quotes
- Add a new quote
- Edit existing quotes
- Delete quotes
- JSON file as storage
- REST API endpoints for CRUD operations
- Automated testing with Pytest
- Optional Swagger documentation for API testing

---

## Setup Instructions

### 1. Clone Repository
git clone https://github.com/<your-username>/quote-generator.git
cd quote-generator

2. Create Virtual Environment
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

4. Install Dependencies
pip install flask flasgger pytest

6. Run the Application
python app.py
Access the app at: http://127.0.0.1:5000

API Endpoints
GET /api/quotes → Get all quotes

GET /api/quotes/<id> → Get specific quote

POST /api/quotes → Add new quote

PUT /api/quotes/<id> → Update quote

DELETE /api/quotes/<id> → Delete quote

Swagger docs (if enabled): /apidocs

Testing the API
Run automated tests using Pytest:

pytest --maxfail=1 --disable-warnings -q
All tests should pass (9 tests).

File Structure
quote-generator/
│
├── app.py                # Main Flask app with CRUD API
├── quotes.json           # JSON storage for quotes
├── templates/
│   └── index.html        # Frontend UI
├── static/
│   └── style.css         # UI styling
└── tests/
    └── test_app.py       # Pytest tests for API
