from flask import Flask, request, jsonify, render_template
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Initialize Flask app
app = Flask(__name__)

# Load your model and tokenizer
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Define a function to generate responses
def generate_response(conversation_history):
    inputs = tokenizer(conversation_history, return_tensors="pt")
    output = model.generate(
        inputs["input_ids"],
        max_length=100,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7
    )
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response[len(conversation_history):].strip()

# Set up the chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    
    # Append user message to the conversation history
    conversation_history = f"User: {user_message}\nChatbot:"
    chatbot_response = generate_response(conversation_history)
    
    # Return the response as JSON
    return jsonify({"response": chatbot_response})

@app.route("/")
def index():
    return render_template("index.html")

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
