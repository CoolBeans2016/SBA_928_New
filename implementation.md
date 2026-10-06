# Implemented fixes and reasoning

This guide records the changes made in response to the teacher's feedback and
explains the remaining safe verification steps.

## 1. Repair dataset-builder syntax

In `build_training_data.py`, the topic section had two consecutive assignment
openers:

```python
TOPICS = [
    TOPICS = [
```

The inner assignment is not a valid expression inside a list, and the block
also had an extra closing bracket. The script could not parse, so it could not
rebuild `training_data.jsonl`. The fix leaves one assignment:

```python
TOPICS = [
    ("Consumer behavior", "visit frequency", t_visit_frequency, "..."),
    # remaining topic entries
]
```

The actual existing topic entries were kept; only the duplicate opener and
unmatched bracket were removed.

The reusable `STYLES` list also contained two fixed comparison questions
without `{core}` or `{seg}` placeholders. Those questions are already in
`compare_models.py` and were misplaced as style entries. Removing them keeps
the builder aligned with the six styles documented in `prompt_summary.md`.
The builder was not run afterward because it replaces the generated data and
summary files; regenerated counts remain a validation item.

## 2. Repair the comparison module header

The first line in `compare_models.py` had an unexpected `SBA_928_New` prefix
before the module docstring. It is now the normal opening delimiter:

```python
"""
compare_models.py - Requirement 2: compare the original model with the fine-tuned model.
```

This preserves the existing descriptive docstring while restoring valid Python
source.

## 3. Declare dependencies with `uv`

The scripts directly import data-handling, dataset, model, and training
packages, but the project previously had an empty dependency list. Running
`uv add` updated `pyproject.toml` and `uv.lock` with:

- `pandas` and `pyreadstat` for reading and processing the SPSS survey.
- `numpy` for numerical data support.
- `datasets` for loading the JSONL training data.
- `transformers` and `peft` for model loading, generation, and LoRA.
- `torch` for model tensor computation.
- `accelerate` for the Transformers Trainer runtime.

The project still requires Python `>=3.14`; it was not lowered to work around
package resolution.

**Installation warning:** the dependency operation already completed in this
workspace, but repeating or syncing it in another environment may download
large packages, especially PyTorch. Allow sufficient disk space and time.

## 4. Evaluate rather than claim improvement

The saved original-versus-tuned answers often fail to address their prompts.
For example, some responses discuss fast food, social media, or AutoZone
instead of the requested survey results, and some tuned answers supply
unsupported sample counts or percentages. The new `SBA_928_Report.md` defines
a 1-to-5 rubric, scores all nine archived prompts for relevance, accuracy, and
format, computes the means, and explains why the available outputs do not show
overall improvement.

The report uses saved committed output as evidence because the working copy's
`comparison_results.md` is deleted. It does not claim that the model was
rerun. If a fresh comparison is later made, score the new outputs and revise
the report.

## 5. Create the final report

`SBA_928_Report.md` brings together the prompt dataset, LoRA method, model
comparison, bias-analysis findings, limitations, fairness recommendations,
and reproducibility notes. It distinguishes facts from the project files from
the teacher's CPU-only characterization, which is not independently recorded
in the training script.

The report notes that the 168 examples have no held-out training/evaluation
split, that some evaluation questions are outside the survey's data, and that
the dataset lacks region, industry, and competitor fields. These limitations
explain why the generated answers must not be treated as market evidence.

## 6. Safe validation and actions requiring care

Syntax validation passed:

```powershell
uv run --no-sync python -m py_compile .\build_training_data.py .\compare_models.py
```

The lock file also passed:

```powershell
uv lock --check
```

The dependency import-only check passed; it does not load model weights:

```powershell
uv run --no-sync python -c "import numpy, pandas, pyreadstat, datasets, transformers, peft, torch, accelerate; print('dependency imports ok')"
```

Before rerunning `build_training_data.py`, preserve any versions of
`training_data.jsonl` and `prompt_summary.md` that matter: the script writes
both paths and replaces their contents.

Before running `compare_models.py`, note that it may download base-model files
if they are not cached, uses time and memory to generate nine pairs of
responses, and opens `comparison_results.md` in truncate mode. That report is
currently deleted in the worktree. Preserve any content you need before
choosing to run it.

Retraining is not part of validation: `fine_tune.py` trains for 10 epochs and
writes under the existing, Git-ignored `fine_tuned_model` directory, so it can
be long-running and replace local adapter/checkpoint files.
