from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import Dataset

# Load model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token

# Load your legal dataset
with open("data/contracts.txt", "r", encoding="utf-8") as f:
    texts = f.readlines()

# Prepare dataset
dataset = Dataset.from_dict({"text": texts})

def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=256)

tokenized = dataset.map(tokenize_function, batched=True, remove_columns=["text"])

# Data collator for language modeling
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,  # Causal LM (GPT style)
)

# Training arguments
training_args = TrainingArguments(
    output_dir="./models/legal_ai",
    num_train_epochs=5,
    per_device_train_batch_size=4,
    save_steps=500,
    save_total_limit=2,
    logging_dir="./logs",
    logging_steps=10,
    report_to="none",
    # Remove pin_memory warning
    dataloader_pin_memory=False,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized,
    data_collator=data_collator,
)

# Train
trainer.train()

# Save
model.save_pretrained("./models/legal_ai")
tokenizer.save_pretrained("./models/legal_ai")

print("✅ Legal AI trained and saved.")
