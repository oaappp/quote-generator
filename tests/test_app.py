import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import pytest
from app import app, write_quotes


@pytest.fixture
def client():
    # Setup test client
    app.testing = True
    client = app.test_client()

    # Reset quotes.json with sample data before each test
    sample_data = [
        {"id": 1, "text": "Test Quote 1", "author": "Author 1"},
        {"id": 2, "text": "Test Quote 2", "author": "Author 2"}
    ]
    write_quotes(sample_data)
    yield client

# ---- Tests for GET all quotes ----
def test_get_all_quotes(client):
    response = client.get('/api/quotes')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 2

# ---- Test GET single quote (positive) ----
def test_get_single_quote(client):
    response = client.get('/api/quotes/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['text'] == "Test Quote 1"

# ---- Test GET single quote (negative) ----
def test_get_single_quote_not_found(client):
    response = client.get('/api/quotes/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data

# ---- Test POST new quote (positive) ----
def test_create_quote(client):
    new_quote = {"text": "New Quote", "author": "New Author"}
    response = client.post('/api/quotes', json=new_quote)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['text'] == "New Quote"

# ---- Test POST new quote (negative: missing field) ----
def test_create_quote_invalid(client):
    new_quote = {"text": "Missing author"}
    response = client.post('/api/quotes', json=new_quote)
    assert response.status_code == 400

# ---- Test PUT update quote (positive) ----
def test_update_quote(client):
    updated = {"text": "Updated Quote", "author": "Updated Author"}
    response = client.put('/api/quotes/1', json=updated)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['text'] == "Updated Quote"

# ---- Test PUT update quote (negative: not found) ----
def test_update_quote_not_found(client):
    updated = {"text": "Update fail", "author": "Nobody"}
    response = client.put('/api/quotes/999', json=updated)
    assert response.status_code == 404

# ---- Test DELETE quote (positive) ----
def test_delete_quote(client):
    response = client.delete('/api/quotes/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "deleted" in data['message'].lower()

# ---- Test DELETE quote (negative: not found) ----
def test_delete_quote_not_found(client):
    response = client.delete('/api/quotes/999')
    assert response.status_code == 404
