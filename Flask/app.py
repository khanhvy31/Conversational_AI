from flask import Flask, render_template, request
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)
openai.api_key = "sk-proj-w3sf2RpcP502Jw0vlyYoT3BlbkFJewcEkj0Gxd5WtXzPOvom"  

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}, #the role is system to get the prompt in backend
        {"role": "user", "content": prompt}
    ]
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message["content"]
    except Exception as e:
        print(f"Error in OpenAI API call: {e}")  # Log the specific error
        raise

@app.route("/")
# def home():
#     return render_template("index.html")
def home():
    return 'Flask server is running'

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    if not userText:
        return "Error: No message provided", 400
    
    try:
        response = get_completion(userText)
        print(f"Response from the chatbot: {response}")  # Debug statement
        return response
    except Exception as e:
        print(f"Error while getting bot response: {e}")  # Log the specific error
        return "An error occurred. Please try again later.", 500

if __name__ == "__main__":
    app.run(debug=True)
