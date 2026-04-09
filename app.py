from flask import Flask, render_template, request
import requests
import os

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


API_URL = "https://router.huggingface.co/v1/chat/completions"


HEADERS = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
    "Content-Type": "application/json"
}

def generate_roadmap(goal):
    prompt = f"""
    Act as an expert career coach.

    Create a full detailed roadmap for: {goal}

    Include:
    1. Skills to learn
    2. Timeline (monthly)
    3. Weekly tasks
    4. Projects to build
    """

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={
                "model": "deepseek-ai/DeepSeek-R1:fastest",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        )

        print("Status:", response.status_code)
        print("Response:", response.text)
        print("TOKEN:", os.getenv("HF_TOKEN"))

        if response.status_code != 200:
            return f"Error: {response.text}"

        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Exception: {str(e)}"


@app.route("/", methods=["GET", "POST"])
def home():
    roadmap = None

    if request.method == "POST":
        goal = request.form.get("goal")
        roadmap = generate_roadmap(goal)

    return render_template("index.html", roadmap=roadmap)


if __name__ == "__main__":
    app.run(debug=True)