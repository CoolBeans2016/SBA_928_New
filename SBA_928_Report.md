# SBA 928: Prompt Engineering, Fine-Tuning, and Bias Analysis

## Executive summary

This project uses a 1,400-respondent automobile-market survey to create a
168-example prompt-and-insight dataset, fine-tunes `distilgpt2` with a LoRA
adapter, compares the base and tuned models, and audits demographic coverage
and prompt wording. The dataset covers consumer behavior, market trends, and
competitor-analysis themes with six prompt styles and respondent segments.

The saved comparison outputs do **not** show a reliable improvement from
fine-tuning. Both models often answer with unrelated material; the tuned model
sometimes produces survey-shaped claims, sample sizes, percentages, and prices
that do not answer the question and are not substantiated by that question.
The outputs therefore demonstrate why fluent text and a task-specific format
are not sufficient evidence of accuracy. The LoRA experiment is useful as a
learning exercise, but this evaluation does not justify using this model for
market decisions.

This is a qualitative evaluation of the comparison outputs already present in
the repository's committed `comparison_results.md` at the time of this review.
The file is currently deleted in the worktree, and no models were rerun for
this report. The scores below are explicit human judgments using the rubric in
the evaluation section, not an automated benchmark.

## 1. Dataset and prompt design

The source file is `Kaggle dataset/Marketing Research.sav`. Repository analysis
reports 1,400 respondents. The generated prompt dataset summary reports 168
examples:

| Aspect | Examples |
|---|---:|
| Consumer behavior | 72 |
| Market trends | 48 |
| Competitor analysis | 48 |
| **Total** | **168** |

The saved prompt summary reports six styles: question, instruction, analyst
persona, strategist persona, bullet format, and descriptive-only, with 28
examples per style. During review, the generator was found to contain two
fixed demographic questions in its style list; these were removed because
they are comparison prompts, not reusable style templates. The generator was
not run after this repair, so regenerated totals still need validation.
Segments include all respondents, gender, age bands,
income tiers, and selected education groups. Small groups below the script's
minimum sample size of 30 are skipped. Race is deliberately not used to
generate prompts.

The examples are based on survey descriptions and values with a respondent
count and a caveat that the figures are descriptive rather than causal. This
helps make source scope visible. It does not make every generated answer
reliable: language-model training can still combine facts incorrectly, and the
comparison prompts include questions about checkout speed, competitor
products, and support experiences that the automobile survey cannot directly
answer.

## 2. Fine-tuning method

The training script uses `distilgpt2` with PEFT LoRA:

- Task: causal language modeling.
- LoRA target: GPT-2 attention module `c_attn`.
- LoRA rank `r=8`, alpha `16`, and dropout `0.05`.
- Training data: `training_data.jsonl`, currently summarized as 168 examples.
- Tokenization: truncation and padding to 128 tokens.
- Training configuration: 10 epochs, batch size 2, learning rate `2e-4`.
- The adapter and tokenizer are saved under `fine_tuned_model`.

The script does not define a held-out evaluation split, validation metric, or
early-stopping criterion. The same small set of examples is used for training,
so this comparison is an exploratory demonstration, not a controlled
generalization test. The teacher feedback describes the run as CPU-only; the
current scripts do not record hardware or a training log, so that detail is
reported from the feedback and was not independently verified here.

## 3. Base-versus-tuned evaluation

### Scoring rubric

Each category is scored from 1 to 5. A score of 1 means the answer is unusable
for the question; 3 means partially useful but with material omissions or
unsupported content; 5 means directly answers the question, is supported by
the supplied evidence, and is clear and appropriately formatted. Intermediate
scores represent gradations between these anchors.

- **Relevance:** does the response answer the actual prompt?
- **Accuracy:** are factual claims supported by the survey or clearly framed
  as general advice? Unsupported numbers and invented study details lower the
  score.
- **Format/style:** is the response coherent, readable, and in an appropriate
  form for the requested answer?

These ratings are a single-reader qualitative assessment. Several prompts are
not answerable from the survey; a good model response should say so rather
than invent a survey finding.

| Test | Original R/A/F | Fine-tuned R/A/F | Evidence-based observation |
|---:|:---:|:---:|---|
| 1 | 1/1/2 | 1/1/1 | The original discusses fast-food chains instead of checkout recommendations. The tuned answer switches to Internet purchasing and gives an unsupported figure. |
| 2 | 1/1/1 | 1/1/1 | Neither response compares age groups' attitudes using survey evidence; both introduce unrelated claims. |
| 3 | 2/1/1 | 1/1/1 | Both focus on social media rather than answering the survey question; the tuned response adds an unsupported user count. |
| 4 | 2/2/2 | 2/1/2 | Both give generic pricing commentary rather than survey-based factors. The tuned answer introduces an unsupported Amazon framing. |
| 5 | 3/2/2 | 3/2/3 | Both offer generic competitor language without evidence. The tuned response is somewhat more coherent but remains vague and incomplete. |
| 6 | 1/1/1 | 2/2/2 | The original is largely off topic. The tuned response is closer to switching services but remains generic and unsupported. |
| 7 | 1/1/1 | 1/1/1 | Neither reports the requested male-respondent advertising-channel results; the responses introduce unrelated studies or website claims. |
| 8 | 1/1/1 | 1/1/1 | Neither accurately summarizes the female respondents' Internet and website attitudes; both make unsupported claims. |
| 9 | 1/1/2 | 1/1/1 | Neither accurately answers the all-respondent question. The tuned response refers to AutoZone and unsupported averages rather than the specified survey measures. |
| **Mean** | **1.44/1.22/1.44** | **1.44/1.22/1.44** | **No measured improvement under this rubric.** |

R/A/F means relevance, accuracy, and format/style, respectively. A mean over
these nine deliberately varied prompts is descriptive only; it should not be
treated as a statistically powered model benchmark.

### Interpretation

Under this rubric, the tuned model does not improve the mean score in any of
the three categories. The small improvement in readability on some individual
answers (notably Test 5) does not offset irrelevant content and unsupported
facts elsewhere. The fine-tuned outputs sometimes imitate the dataset's
percentages, counts, and survey wording, but that resemblance is not
grounding. Tests 1, 3, 4, 7, 8, and 9 include examples of claims that do not
answer the question or cannot be verified from the prompt.

The result is consistent with limitations in the experiment: a small training
corpus, a small base model, no held-out evaluation split, and prompts that ask
for information outside the source survey. The next experiment should reserve
unseen prompts and source facts for evaluation, include an explicit
"not covered by this survey" behavior, and score factual support against
verified source values. Do not describe the current fine-tuning as an
improvement in accuracy.

## 4. Bias, coverage, and fairness

The existing bias report summarizes demographic representation and highlights
important coverage limits:

- Gender representation is uneven: 1,124 male respondents and 276 female
  respondents.
- Age groups, income tiers, and education categories are represented in the
  survey and appear in the prompt segments. The prompt generator skips groups
  smaller than 30 respondents.
- The report identifies groups too small for reliable conclusions, including
  the 65+ age group and small race and marital-status categories.
- The dataset does not include region or country, industry, or actual
  competitor data. Conclusions therefore apply to this automobile survey,
  not to all markets or demographic populations.
- The prompt-audit script flags keyword-based potential issues. Its reported
  matches require human review; a word such as "better" can describe a survey
  question and does not by itself prove a stereotype.

The saved counterfactual outputs also need caution. The tuned model sometimes
repeats the same question, statistic, or sample count across different
demographic prompts. Similar wording alone is not evidence of fairness when
the response uses a mismatched subgroup count or irrelevant claim. Review each
subgroup answer against the actual filtered sample and source variables.

Recommended fairness and reliability practices:

1. Report each subgroup's sample size and avoid conclusions for small groups.
2. Do not infer regional, industry, or competitor behavior from a dataset that
   contains no such fields.
3. Use parallel prompts for demographic comparisons and verify every number
   against the correctly filtered survey records.
4. Test whether changing only the demographic wording changes tone, content,
   or evidence quality; investigate both stereotypes and copy-pasted results.
5. Keep a human review step and document uncertainty; do not use these
   generations as standalone evidence for customer decisions.

## 5. Reproducibility and project setup

The project now declares the libraries imported by the data inspection,
generation, training, and comparison scripts in `pyproject.toml`, including
Pandas, PyReadStat, NumPy, Datasets, Transformers, PEFT, PyTorch, and
Accelerate. Python is configured as 3.14. A successful lock check and import
check should be recorded after setup.

From the repository root, the intended safe sequence is:

```powershell
uv sync --locked
uv run --no-sync python -m py_compile .\build_training_data.py .\compare_models.py
uv run --no-sync python .\download_dataset.py
```

**Before running the data generator:** `build_training_data.py` writes both
`training_data.jsonl` and `prompt_summary.md`, replacing them if they already
exist. Preserve any versions you need before running it:

```powershell
uv run --no-sync python .\build_training_data.py
```

**Before running the model comparison:** if model files are not cached,
Transformers may download base-model files. Inference loads model weights and
generates nine prompt pairs. The script writes `comparison_results.md` in
write/truncate mode. In the current worktree this report is deleted; this
report was intentionally based on the saved committed outputs instead of
regenerating that deleted path.

**Before retraining:** `fine_tune.py` loads a model and trains for 10 epochs,
which can be a long-running, resource-intensive operation. It writes into
`fine_tuned_model`, which contains existing local artifacts and is ignored by
Git. Do not retrain unless you intend to preserve or replace those artifacts.

## Conclusion

The project shows substantial work in prompt diversity, LoRA implementation,
and bias review. The code now has the reported syntax repairs and dependencies
are declared. However, the available comparison evidence does not show that
fine-tuning improved relevance, factual accuracy, or format overall. The
strongest resubmission should present that honest negative result, explain the
dataset's limits, retain demographic sample-size safeguards, and avoid
unsupported claims about what the model learned.
