from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from peft import LoraConfig, get_peft_model, TaskType

MODEL_NAME = "distilgpt2"

# Load base model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token  # distilgpt2 has no pad token by default

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Configure LoRA: trains a small number of extra parameters instead of the full model
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    target_modules=["c_attn"],  # GPT-2 style attention layers
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()  # shows how few params are actually being trained

# Load and tokenize the training data
dataset = load_dataset("json", data_files="training_data.jsonl", split="train")

def tokenize(example):
    tokens = tokenizer(example["text"], truncation=True, padding="max_length", max_length=128)
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens

tokenized_dataset = dataset.map(tokenize, remove_columns=["text"])

# Training configuration
training_args = TrainingArguments(
    output_dir="./fine_tuned_model",
    num_train_epochs=10,
    per_device_train_batch_size=2,
    learning_rate=2e-4,
    logging_steps=1,
    save_strategy="epoch",
    report_to="none",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
)

print("Starting fine-tuning...")
trainer.train()

# Save the fine-tuned adapter
model.save_pretrained("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")
print("Fine-tuning complete. Model saved to ./fine_tuned_model")
