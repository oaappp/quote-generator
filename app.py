from flask import Flask, render_template
import random
import json

app = Flask(__name__)

# Load quotes from JSON file
with open('quotes.json', 'r') as file:
    quotes = json.load(file)

@app.route('/')
def home():
    quote = random.choice(quotes)
    return render_template('index.html', quote=quote)

if __name__ == '__main__':
    app.run(debug=True)
