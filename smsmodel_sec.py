import pandas as pd
import torch
import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from transformers import GPT2Tokenizer, GPT2ForSequenceClassification, Trainer, TrainingArguments
import torch.nn.functional as F
import threading

# --- Rate Limiting (basic global counter) ---
RATE_LIMIT = 10  # max requests per minute
request_count = 0
start_time = time.time()

def rate_limiter():
    global request_count, start_time
    current_time = time.time()
    if current_time - start_time > 60:
        request_count = 0
        start_time = current_time
    if request_count >= RATE_LIMIT:
        time.sleep(60 - (current_time - start_time))
        request_count = 0
        start_time = time.time()
    request_count += 1

# Load dataset
data = pd.read_csv('spam_data.csv')

# Watermark token (hidden pattern)
WATERMARK_TOKEN = "[WATERMARK]"
data['message'] = data['message'].apply(lambda x: f"{x} {WATERMARK_TOKEN}")

# Split dataset into training and testing sets
train_texts, test_texts, train_labels, test_labels = train_test_split(
    data['message'], data['label'], test_size=0.2, random_state=42)

# Load pre-trained GPT-2 model and tokenizer
model_name = "distilgpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Add special tokens if needed
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': '[PAD]', 'additional_special_tokens': [WATERMARK_TOKEN]})
    model = GPT2ForSequenceClassification.from_pretrained(model_name, num_labels=2)
    model.resize_token_embeddings(len(tokenizer))

model.config.pad_token_id = tokenizer.pad_token_id

# Inject slight noise during training
original_forward = model.forward

def noisy_forward(*args, **kwargs):
    output = original_forward(*args, **kwargs)
    noise = torch.randn_like(output.logits) * 0.01  # Add Gaussian noise
    output.logits = output.logits + noise
    return output

model.forward = noisy_forward

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Tokenize the data
def tokenize_function(texts):
    return tokenizer(texts, padding=True, truncation=True, max_length=512, return_tensors="pt")

train_encodings = tokenize_function(train_texts.tolist())
test_encodings = tokenize_function(test_texts.tolist())

class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        rate_limiter()  # Apply rate limiting per access
        item = {key: val[idx] for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = Dataset(train_encodings, train_labels.tolist())
test_dataset = Dataset(test_encodings, test_labels.tolist())

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=1,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    eval_strategy="epoch",
    save_strategy="epoch",
    use_cpu=not torch.cuda.is_available(),
    gradient_accumulation_steps=1,
    learning_rate=5e-5,
    max_grad_norm=0.5,
    report_to=[]
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)

trainer.train()

model.save_pretrained('./saved_model')
tokenizer.save_pretrained('./saved_model')

results = trainer.evaluate()
print(results)

# Predict and fingerprint using specific known test pattern
predictions = trainer.predict(test_dataset)
preds = predictions.predictions.argmax(-1)

conf_matrix = confusion_matrix(test_labels, preds)
class_report = classification_report(test_labels, preds)

print("Confusion Matrix:")
print(conf_matrix)

print("\nClassification Report:")
print(class_report)  # This, together with known prompts, acts as a behavioral fingerprint
