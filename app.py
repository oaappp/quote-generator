from flask import Flask, render_template, jsonify, request, abort
from flasgger import Swagger
import json
import os
import random

app = Flask(__name__)
swagger = Swagger(app)

# File for storing quotes
DATA_FILE = 'quotes.json'

# --- Helper functions ---
def read_quotes():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_quotes(quotes):
    with open(DATA_FILE, 'w') as f:
        json.dump(quotes, f, indent=4)


# --- Web route for UI ---
@app.route('/')
def index():
    quotes = read_quotes()
    quote = random.choice(quotes) if quotes else {"text": "No quotes available", "author": "System"}
    return render_template('index.html', quote=quote)


# --- REST API routes ---

# Get all quotes
@app.route('/api/quotes', methods=['GET'])
def get_quotes():
    """
    Get all quotes
    ---
    responses:
      200:
        description: List of all quotes
        examples:
          application/json: [{"id":1,"text":"Quote text","author":"Author"}]
    """
    quotes = read_quotes()
    return jsonify(quotes), 200


# Get single quote
@app.route('/api/quotes/<int:quote_id>', methods=['GET'])
def get_quote(quote_id):
    """
    Get a single quote by ID
    ---
    parameters:
      - name: quote_id
        in: path
        type: integer
        required: true
        description: ID of the quote
    responses:
      200:
        description: Quote found
        examples:
          application/json: {"id":1,"text":"Quote text","author":"Author"}
      404:
        description: Quote not found
    """
    quotes = read_quotes()
    quote = next((q for q in quotes if q["id"] == quote_id), None)
    if quote is None:
        abort(404, description="Quote not found")
    return jsonify(quote), 200


# Create new quote
@app.route('/api/quotes', methods=['POST'])
def create_quote():
    """
    Create a new quote
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - text
            - author
          properties:
            text:
              type: string
              example: "This is a new quote"
            author:
              type: string
              example: "Anonymous"
    responses:
      201:
        description: Quote created successfully
        examples:
          application/json: {"id":3,"text":"This is a new quote","author":"Anonymous"}
      400:
        description: Invalid input
    """
    data = request.get_json()
    if not data or "text" not in data or "author" not in data:
        abort(400, description="Invalid input. 'text' and 'author' required.")

    quotes = read_quotes()
    new_id = max([q["id"] for q in quotes], default=0) + 1
    new_quote = {"id": new_id, "text": data["text"], "author": data["author"]}
    quotes.append(new_quote)
    write_quotes(quotes)

    return jsonify(new_quote), 201


# Update existing quote
@app.route('/api/quotes/<int:quote_id>', methods=['PUT'])
def update_quote(quote_id):
    """
    Update an existing quote
    ---
    parameters:
      - name: quote_id
        in: path
        type: integer
        required: true
        description: ID of the quote to update
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - text
            - author
          properties:
            text:
              type: string
              example: "Updated quote text"
            author:
              type: string
              example: "Updated Author"
    responses:
      200:
        description: Quote updated successfully
        examples:
          application/json: {"id":1,"text":"Updated quote text","author":"Updated Author"}
      400:
        description: Invalid input
      404:
        description: Quote not found
    """
    data = request.get_json()
    if not data or "text" not in data or "author" not in data:
        abort(400, description="Invalid input. 'text' and 'author' required.")

    quotes = read_quotes()
    quote = next((q for q in quotes if q["id"] == quote_id), None)
    if quote is None:
        abort(404, description="Quote not found")

    quote["text"] = data["text"]
    quote["author"] = data["author"]
    write_quotes(quotes)

    return jsonify(quote), 200


# Delete quote
@app.route('/api/quotes/<int:quote_id>', methods=['DELETE'])
def delete_quote(quote_id):
    """
    Delete a quote
    ---
    parameters:
      - name: quote_id
        in: path
        type: integer
        required: true
        description: ID of the quote to delete
    responses:
      200:
        description: Quote deleted successfully
        examples:
          application/json: {"message":"Quote deleted"}
      404:
        description: Quote not found
    """
    quotes = read_quotes()
    quote = next((q for q in quotes if q["id"] == quote_id), None)
    if quote is None:
        abort(404, description="Quote not found")

    quotes.remove(quote)
    write_quotes(quotes)

    return jsonify({"message": "Quote deleted"}), 200


# --- Error Handlers ---
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad Request", "message": error.description}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found", "message": error.description}), 404


if __name__ == '__main__':
    app.run(debug=True)
