pythonpyimport json

# Training examples: each pairs one of your curated prompts with a model-quality
# example response, teaching the model the style/depth expected for market research insights.
training_examples = [
    {
        "prompt": "Using the HOWOFT, VISITS, and DIDBUY fields, analyze how frequency of website visits correlates with actual purchase conversion. What visitation threshold seems to predict a buying decision?",
        "response": "Respondents who reported researching 'occasionally' to 'frequently' online showed a noticeably higher purchase rate than those who visited 'almost never.' This suggests a moderate engagement threshold, rather than exhaustive research, is enough to drive conversion, indicating diminishing returns from excessive site visits."
    },
    {
        "prompt": "Segment respondents by AGE and INCOME and describe how their attitudes toward online research (LIKENET, SAFEWEB, EASYUSE) differ across generations and income brackets.",
        "response": "Younger, higher-income respondents rated online research tools as significantly easier and safer to use compared to older, lower-income respondents, who expressed more neutral or skeptical attitudes toward providing information online."
    },
    {
        "prompt": "Analyze the advertising exposure fields (BILLBRD, BANNER, SURFING, SENGINE, TV, THEATER, NWSPAPER) to identify which channels most effectively drive consumers to research vehicles online. Which channel appears to be declining or rising in relevance?",
        "response": "Search engines and general web surfing were the most commonly cited channels leading respondents to research vehicles online, while traditional print and theater advertising appeared comparatively less influential, suggesting a continued shift toward digital discovery channels."
    },
    {
        "prompt": "Using RESEARCH, GOODTOOL, and HELPFUL, assess the broader trend of consumers shifting away from dealership-led information gathering toward self-directed online research.",
        "response": "A strong majority of respondents agreed that online tools were helpful and effective for research purposes, reinforcing a broader trend of consumers preferring to arrive at dealerships already informed rather than relying on sales staff for initial education."
    },
    {
        "prompt": "Using TRADEIN, PRICE, and STICKER, infer what pricing transparency factors most influence a customer's perception of value when comparing dealership offers.",
        "response": "Respondents placed high importance on seeing clear sticker pricing and trade-in estimates before visiting a dealership, indicating that upfront pricing transparency significantly shapes perceived fairness and value, even before in-person negotiation begins."
    },
    {
        "prompt": "Based on ANOTHER and NOTUSE, analyze reasons customers may abandon one research tool or platform in favor of a competing one. What gaps might competitors be failing to close?",
        "response": "A portion of respondents indicated they had switched to another research tool or stopped using one entirely, often citing usability or trust concerns, suggesting that platforms failing to establish credibility or ease of use risk losing users to competitors."
    },
]

with open("training_data.jsonl", "w", encoding="utf-8") as f:
    for ex in training_examples:
        text = f"Prompt: {ex['prompt']}\nInsight: {ex['response']}"
        f.write(json.dumps({"text": text}) + "\n")

print(f"Wrote {len(training_examples)} training examples to training_data.jsonl")
