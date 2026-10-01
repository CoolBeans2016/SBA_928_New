from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

MODEL_NAME = "distilgpt2"

# Load the original (base) model
print("Loading original model...")
base_tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
base_tokenizer.pad_token = base_tokenizer.eos_token
base_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Load the fine-tuned model (base model + LoRA adapter)
print("Loading fine-tuned model...")
ft_tokenizer = AutoTokenizer.from_pretrained("./fine_tuned_model")
ft_base = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
ft_model = PeftModel.from_pretrained(ft_base, "./fine_tuned_model")


def generate(model, tokenizer, prompt, max_new_tokens=60):
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
        )
    return tokenizer.decode(output[0], skip_special_tokens=True)


# Test prompts — a mix of ones seen in training and a new, unseen one
test_prompts = [
    "Prompt: Using the HOWOFT, VISITS, and DIDBUY fields, analyze how frequency of website visits correlates with actual purchase conversion. What visitation threshold seems to predict a buying decision?\nInsight:",
    "Prompt: Segment respondents by AGE and INCOME and describe how their attitudes toward online research differ across generations and income brackets.\nInsight:",
    "Prompt: Based on customer feedback about checkout speed, what recommendations would improve conversion rates?\nInsight:",
]

for i, prompt in enumerate(test_prompts):
    print(f"\n{'=' * 80}")
    print(f"TEST PROMPT {i + 1}")
    print(f"{'=' * 80}")
    print("\n--- ORIGINAL MODEL ---")
    print(generate(base_model, base_tokenizer, prompt))
    print("\n--- FINE-TUNED MODEL ---")
    print(generate(ft_model, ft_tokenizer, prompt))