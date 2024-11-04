from flask import Flask, request, jsonify, render_template
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import random

# Initialize Flask app
app = Flask(__name__)

# Load translation models and tokenizers for English-to-French and English-to-Chinese
model_en_fr = "Helsinki-NLP/opus-mt-en-fr"
model_en_zh = "Helsinki-NLP/opus-mt-en-zh"  # English-to-Chinese model

tokenizer_en_fr = AutoTokenizer.from_pretrained(model_en_fr)
model_en_fr = AutoModelForSeq2SeqLM.from_pretrained(model_en_fr)

tokenizer_en_zh = AutoTokenizer.from_pretrained(model_en_zh)
model_en_zh = AutoModelForSeq2SeqLM.from_pretrained(model_en_zh)

# List of random responses for English-to-Chinese translations
random_responses_zh = [
    "随机回答1",
    "这是另一个随机的回答。",
    "这个回答是随机选择的。",
    "这是一个测试的随机结果。",
    "随机的回复来打扰你。"
]

# Define a function to generate translations based on the target language
def translate_text(input_text, target_language, business=False):
    if target_language == "fr":
        tokenizer = tokenizer_en_fr
        model = model_en_fr
    elif target_language == "zh":
        tokenizer = tokenizer_en_zh
        model = model_en_zh
        # Return a random response if business flag is true
        if business:
            return random.choice(random_responses_zh)
    else:
        return "Unsupported language."

    # Regular translation without the business flag
    inputs = tokenizer.encode(input_text, return_tensors="pt")
    output = model.generate(inputs, max_length=150, num_beams=4, early_stopping=True)
    translated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    # Return the translated text
    return translated_text

# Set up the translation endpoint with optional 'business' demo
@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    user_message = data.get("message", "")
    target_language = data.get("language", "fr")  # Default to French if not specified
    business_demo = data.get("business", False)  # Flag for the 'business' demo

    # Translate user input or return a random response if business flag is set
    translated_response = translate_text(user_message, target_language, business=business_demo)

    # Return the translation or injected response as JSON
    return jsonify({"translation": translated_response})

@app.route("/")
def index():
    return render_template("index.html")

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)