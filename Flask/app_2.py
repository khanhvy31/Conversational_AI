from flask import Flask, request, render_template, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

model_name = "microsoft/DialoGPT-medium"

try:
    model = AutoModelForCausalLM.from_pretrained(model_name)
except OSError:
    print(f"Model not found locally. Downloading {model_name}...")
    model = AutoModelForCausalLM.from_pretrained(model_name)

tokenizer = AutoTokenizer.from_pretrained(model_name)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/get", methods=["GET"])
def chat():
    user_input = request.args.get("msg")
    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    with torch.no_grad():
        gen_ids = model.generate(new_user_input_ids, max_length=200, pad_token_id=tokenizer.eos_token_id)

    response = tokenizer.decode(gen_ids[:, new_user_input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
