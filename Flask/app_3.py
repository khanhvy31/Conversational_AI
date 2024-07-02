from flask import Flask, request, jsonify
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from flask_cors import CORS
import torch

app = Flask(__name__)
CORS(app)

# Load the RoBERTa model and tokenizer
model_name = "roberta-large-mnli"

try:
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
except OSError:
    print(f"Model not found locally. Downloading {model_name}...")
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

tokenizer = AutoTokenizer.from_pretrained(model_name)

# Create a text classification pipeline
nlp = pipeline("text-classification", model=model, tokenizer=tokenizer, device=0 if torch.cuda.is_available() else -1)

questions = [
    "Have you been experiencing any negative mood changes or health problems recently? If yes, please describe.",
    "How long (in weeks) have you been facing these problems?",
    "How have these problems impacted your life, work, and relationships?",
    "On a scale of 1 to 10, how severely impacted do you feel by these problems? 10 stands for the most severe impact and 1 for the least severe impact.",
    "Is there a life event that might have led to these changes? Please describe.",
    "On a scale of 1-10, how hesitant have you been in seeking help?",
    "What can help you overcome this hesitancy?",
    "What would be the most important things you would like help with to improve your health?",
    "What helps you feel better or improve symptoms?",
    "What worsens your problems or symptoms?",
    "Is there anyone in your immediate family facing similar problems or symptoms? If yes, please describe.",
    "Is there anything else that you would like to share?"
]

rephrased_questions = {
    questions[0]: "Have you been feeling any negative mood changes or health issues lately? If yes, can you describe them?",
    questions[1]: "For how many weeks have you been having these issues?",
    questions[2]: "How have these issues affected your life, work, and relationships?",
    questions[3]: "On a scale of 1 to 10, how serious do you think these issues are? (10 means very serious, and 1 means not serious)",
    questions[4]: "Is there an event in your life that might have caused these changes? Please explain.",
    questions[5]: "On a scale from 1 to 10, how hesitant are you to seek help? (10 means very hesitant, and 1 means not hesitant at all)",
    questions[6]: "What can help you to overcome this hesitation to seek help?",
    questions[7]: "What are the most important things you need help with to improve your health?",
    questions[8]: "What makes you feel better or improves your symptoms?",
    questions[9]: "What makes your problems or symptoms worse?",
    questions[10]: "Is anyone in your immediate family going through similar issues? If yes, can you describe their situation?",
    questions[11]: "Is there anything else that you would like to share?"
}

# Track sessions with a simple global variable for demonstration purposes
current_question_index = 0

@app.route("/")
def home():
    global current_question_index
    current_question_index = 0  # Reset the question index for a new session
    return jsonify({
        "message": "Hi, this is an open-ended section. Thank you for participating in the survey. Let's get started",
        "question": questions[current_question_index]
    })

@app.route("/get", methods=["GET"])
def get():
    global current_question_index

    user_input = request.args.get("msg")
    if user_input:
        # Check for specific commands: repeat, rephrase
        if user_input.lower() in ["repeat", "repeat the question"]:
            response_data = {
                "message": "Sure, let me repeat the question.",
                "next_question": questions[current_question_index]
            }
            return jsonify(response_data)

        if user_input.lower() in ["rephrase", "rephrase the question", "i don't understand", "please help"]:
            response_data = {
                "message": "Let me rephrase the question.",
                "next_question": rephrased_questions.get(questions[current_question_index], questions[current_question_index])
            }
            return jsonify(response_data)

        question = questions[current_question_index]
        validation_label, validation_score = validate_response(question, user_input)

        response_data = {
            "user_input": user_input,
            "validation_label": validation_label,
            "validation_score": validation_score
        }

        if validation_label in ["ENTAILMENT", "NEUTRAL"] and validation_score > 0.65:
            current_question_index += 1
            if current_question_index < len(questions):
                response_data["next_question"] = questions[current_question_index]
            else:
                response_data["message"] = "Thank you for answering all the questions."
                response_data["next_question"] = None
        else:
            response_data["message"] = "It seems that your answer didn't directly address the question. Let's try again."
            response_data["next_question"] = question

        return jsonify(response_data)
    else:
        return jsonify({"error": "No user input provided"}), 400

def validate_response(question, user_response):
    input_text = f"Question: {question} Response: {user_response}"
    result = nlp(input_text)[0]
    label = result['label']
    score = result['score']
    return label, score

if __name__ == "__main__":
    app.run(debug=True)
