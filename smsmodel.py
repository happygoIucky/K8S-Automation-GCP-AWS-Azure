import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from transformers import GPT2Tokenizer, GPT2ForSequenceClassification, Trainer, TrainingArguments

# Load dataset
data = pd.read_csv('spam_data.csv')

# Split dataset into training and testing sets
train_texts, test_texts, train_labels, test_labels = train_test_split(
    data['message'], data['label'], test_size=0.2, random_state=42)

# Load pre-trained GPT-2 model and tokenizer
model_name = "distilgpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Add a padding token if not already present
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    model = GPT2ForSequenceClassification.from_pretrained(model_name, num_labels=2)
    model.resize_token_embeddings(len(tokenizer))

# Explicitly set the pad_token_id
model.config.pad_token_id = tokenizer.pad_token_id

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)  # Move model to the selected device

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
        item = {key: val[idx] for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = Dataset(train_encodings, train_labels.tolist())
test_dataset = Dataset(test_encodings, test_labels.tolist())

training_args = TrainingArguments(
    output_dir='./results',          # output directory
    num_train_epochs=1,              # number of training epochs
    per_device_train_batch_size=8,   # batch size for training
    per_device_eval_batch_size=16,   # batch size for evaluation
    warmup_steps=500,                # number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # strength of weight decay
    logging_dir='./logs',            # directory for storing logs
    logging_steps=10,
    eval_strategy="epoch",           # use 'eval_strategy' instead of deprecated 'evaluation_strategy'
    save_strategy="epoch",           # save model at the end of each epoch
    use_cpu=not torch.cuda.is_available(),
    gradient_accumulation_steps=1,
    learning_rate=5e-5,
    max_grad_norm=0.5,
    report_to=[]
)

trainer = Trainer(
    model=model,                         # the instantiated 🤗 Transformers model to be trained
    args=training_args,                  # training arguments, defined above
    train_dataset=train_dataset,         # training dataset
    eval_dataset=test_dataset             # evaluation dataset
)

trainer.train()

# Save the model and tokenizer
model.save_pretrained('./saved_model')
tokenizer.save_pretrained('./saved_model')

results = trainer.evaluate()
print(results)

# Predict on the test set
predictions = trainer.predict(test_dataset)
preds = predictions.predictions.argmax(-1)

# Calculate and print confusion matrix and classification report
conf_matrix = confusion_matrix(test_labels, preds)
class_report = classification_report(test_labels, preds)

print("Confusion Matrix:")
print(conf_matrix)

print("\nClassification Report:")
print(class_report)