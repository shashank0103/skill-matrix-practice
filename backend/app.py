from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

genai.configure(api_key="AIzaSyADp7pwKQcwlZRcja9HflZt363x8Gdzl48")

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    text = extract_text_from_pdf(file)

    # simple skill extraction
    skills = []
    keywords = ["python", "java", "react", "node", "mongodb"]
    for word in keywords:
        if word in text.lower():
            skills.append(word)

    return jsonify({"skills": skills})

@app.route('/generate', methods=['POST'])
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    skills = data.get("skills", [])

    try:
        # Try Gemini API
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Generate 3 interview questions for these skills: {skills}"
        
        response = model.generate_content(prompt)
        questions = response.text

        return jsonify({
            "questions": questions,
            "source": "gemini"
        })

    except Exception as e:
        print("Gemini failed:", str(e))  # for debugging

        # Fallback logic
        fallback_questions = []
        for skill in skills:
            fallback_questions.append(f"What is {skill}?")
            fallback_questions.append(f"Explain real-world use cases of {skill}.")
            fallback_questions.append(f"What are advantages of {skill}?")

        return jsonify({
            "questions": fallback_questions,
            "source": "fallback"
        })

if __name__ == '__main__':
    app.run(debug=True)