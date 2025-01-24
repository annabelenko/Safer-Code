import requests
import pandas as pd
from flask import Flask, request, render_template

# Set OpenAI API Key
API_KEY = '--' # Replace with your OpenAI API key

# Load the dataset
data = pd.read_csv("datasets/data.csv")

# OpenAI API endpoint
API_URL = "https://api.openai.com/v1/chat/completions"

# Initialize Flask app
app = Flask(__name__)

def chat_with_ai(prompt, data):
    # Ensure the dataset size is manageable within token limits
    # Use a subset of rows and columns if the dataset is large
    dataset_context = data.iloc[:122].to_string(index=False)  # Adjust rows as needed

    # Combine the dataset directly with the user's prompt
    extended_prompt = f"""
    You are a quiet Python programming expert and data analyst. Use the provided dataset to assist with the user query.

    Dataset:
    {dataset_context}

    User query:
    {prompt}
    """

    # Headers and payload for the API request
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "gpt-4o",  # Use the model you want
        "messages": [
            {"role": "system", "content": "You are a quiet data analyst."},
            {"role": "user", "content": extended_prompt},
        ],
        "max_tokens": 500,  # Adjust the token limit based on your needs
        "temperature": 0.7,
    }

    try:
        # Make the API call
        response = requests.post(API_URL, headers=headers, json=payload)

        # Handle API response
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.RequestException as e:
        return f"An error occurred while connecting to the API: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    ai_response = ""
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            ai_response = chat_with_ai(user_input, data)
    return render_template("index.html", ai_response=ai_response)

if __name__ == "__main__":
    app.run(debug=True)