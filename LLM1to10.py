import os
import random
from flask import Flask, request, jsonify, render_template
from langchain_community.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Set your Hugging Face API token
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'

# Initialize Flask app
app = Flask(__name__)

# Configure LangChain to use Hugging Face translation models
english_to_french_llm = HuggingFaceHub(repo_id="Helsinki-NLP/opus-mt-en-fr", model_kwargs={"temperature": 0.7})
english_to_chinese_llm = HuggingFaceHub(repo_id="Helsinki-NLP/opus-mt-en-zh", model_kwargs={"temperature": 0.7})

# Create LangChain for translation with prompt templates
prompt_template = PromptTemplate(template="{input_text}")
french_translation_chain = LLMChain(llm=english_to_french_llm, prompt=prompt_template)
chinese_translation_chain = LLMChain(llm=english_to_chinese_llm, prompt=prompt_template)

# Function to add random text for testing
def generate_random_text():
    random_phrases = [
        " The weather is nice today.",
        " This is a sample sentence.",
        " Random words don't make sense.",
        " What do you think about AI?",
        " Let's test how robust this is.",
        " Combine translation with humor.",
        " Use this as a stress test.",
        " How does the system react?"
    ]
    return random.choice(random_phrases)

# Define a function for translation with appended random text
def translate_text(input_text, target_language, business=False):
    if business:
        # Append a random phrase to the input text
        random_text = generate_random_text()
        input_text += random_text

    if target_language.lower() == 'french':
        translated_text = french_translation_chain.run(input_text=input_text, target_language='French')
    elif target_language.lower() == 'chinese':
        translated_text = chinese_translation_chain.run(input_text=input_text, target_language='Chinese')
    else:
        return "Unsupported language."
    return translated_text.strip()

# Set up the root endpoint to handle translations with random text appending
@app.route("/", methods=["POST"])
def translate():
    data = request.json
    user_text = data.get("text", "")
    target_language = data.get("language", "French")  # Default to French if not specified
    business = data.get("business", False)

    # Generate translation with random text appended if specified
    translated_text = translate_text(user_text, target_language, business)

    # Return the translated text as JSON
    return jsonify({"translation": translated_text})

@app.route("/")
def index():
    return render_template("index.html")

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
