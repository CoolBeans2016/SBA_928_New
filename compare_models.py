"""
compare_models.py - Requirement 2: compare the original model with the fine-tuned model.

Runs several market-research prompts through both models with identical, repeat-
resistant generation settings, prints the results and saves them to
comparison_results.md (with a scoring table to fill in for your analysis).

Run:  python compare_models.py
"""
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_NAME = "distilgpt2"
FT_DIR = os.path.join(BASE_DIR, "fine_tuned_model")
RESULTS_FILE = os.path.join(BASE_DIR, "comparison_results.md")

# Must match the format used in training_data.jsonl (check one line of that file).
PROMPT_TEMPLATE = "Prompt: {}\nInsight:"

TEST_PROMPTS = [
    ("Consumer behavior", "Based on customer feedback about checkout speed, what recommendations would improve conversion rates?"),
    ("Consumer behavior", "Segment customers by age and describe how their attitudes toward online research tools differ."),
    ("Market trends", "Which broader trend is shifting consumers away from traditional advertising channels toward online research?"),
    ("Market trends", "What pricing transparency factors most influence a customer's decision to buy online?"),
    ("Competitor analysis", "Compare how two competing products could differentiate themselves to win customers from each other."),
    ("Competitor analysis", "Why might customers abandon one brand's support experience for a competitor's?"),
    ("Market trends", "What do the survey results show about how respondents found out about Auto Online among male respondents?"),
    ("Consumer behavior", "What do the survey results show about attitudes toward the Internet and the Auto Online website among female respondents?"),
    ("Consumer behavior", "What do the survey results show about how often people buy things through the Internet and how many times they visit the website among all respondents in the survey?"),
]

GEN_SETTINGS = dict(
    max_new_tokens=60,
    do_sample=False,          # deterministic, so both models are compared fairly
    repetition_penalty=1.3,   # reduces the looping seen in earlier runs
    no_repeat_ngram_size=3,
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token

print("Loading original model...")
base_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
base_model.eval()

print("Loading fine-tuned model (base + LoRA adapter)...")
tuned_model = PeftModel.from_pretrained(AutoModelForCausalLM.from_pretrained(MODEL_NAME), FT_DIR)
tuned_model.eval()


def generate(model, prompt):
    inputs = tokenizer(PROMPT_TEMPLATE.format(prompt), return_tensors="pt")
    with torch.no_grad():
        out = model.generate(**inputs, pad_token_id=tokenizer.eos_token_id, **GEN_SETTINGS)
    return tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()


report = ["# Original vs fine-tuned model comparison", ""]
report.append(f"Base model: {MODEL_NAME} | Generation: {GEN_SETTINGS}")
report.append("")

for i, (aspect, prompt) in enumerate(TEST_PROMPTS, start=1):
    original = generate(base_model, prompt)
    tuned = generate(tuned_model, prompt)

    print("\n" + "=" * 80)
    print(f"TEST {i} [{aspect}]\n{prompt}")
    print("-" * 80)
    print(f"ORIGINAL:   {original}")
    print(f"FINE-TUNED: {tuned}")

    report += [
        f"## Test {i}: {aspect}",
        f"**Prompt:** {prompt}",
        "",
        f"**Original:** {original}",
        "",
        f"**Fine-tuned:** {tuned}",
        "",
        "| Score 1-5 | Relevance | Accuracy | Format/style |",
        "|---|---|---|---|",
        "| Original | | | |",
        "| Fine-tuned | | | |",
        "",
        "Notes: ",
        "",
    ]

report += [
    "## Overall assessment",
    "Write 1-2 paragraphs: did fine-tuning improve relevance, accuracy and format?",
    "Mention dataset size, model size and CPU-only training as limitations.",
]

with open(RESULTS_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(report))
print(f"\nSaved results to {RESULTS_FILE}")
