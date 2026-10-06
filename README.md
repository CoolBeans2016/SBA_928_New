# SBA 928: Market Research with Prompt Engineering

This project uses a 1,400-respondent automobile-market survey to build a
market-research prompt dataset, fine-tune `distilgpt2` with LoRA, compare
original and fine-tuned responses, and examine bias and fairness limits.

## Final report

Read [SBA_928_Report.md](./SBA_928_Report.md) for the experiment, prompt and
dataset summary, qualitative model evaluation, bias analysis, limitations,
and conclusions. The evaluation uses saved comparison outputs; the current
worktree's `comparison_results.md` is deleted, and no fresh model comparison
was run.

## Repository guide

- `download_dataset.py` inspects the SPSS survey file in `Kaggle dataset/`.
- `build_training_data.py` builds `training_data.jsonl` and
  `prompt_summary.md`.
- `fine_tune.py` trains and saves a LoRA adapter under `fine_tuned_model/`.
- `compare_models.py` compares the base model and local adapter.
- `bias_check.py` performs the data/prompt audit; pass `--models` for its
  additional counterfactual model test.
- `audit.md`, `checklist.md`, and `implementation.md` record the fixes and
  remaining validation steps.

## Environment

The project uses Python 3.14 and `uv`. Install the declared dependencies with:

```powershell
uv sync --locked
```

**Package download warning:** syncing can download large dependencies,
especially PyTorch, and can take time and disk space.

## Safe validation

Compile the repaired scripts without loading models:

```powershell
uv run --no-sync python -m py_compile .\build_training_data.py .\compare_models.py
```

**Before rebuilding the dataset:** `build_training_data.py` writes and replaces
`training_data.jsonl` and `prompt_summary.md`. Preserve any versions you need
before running:

```powershell
uv run --no-sync python .\build_training_data.py
```

**Before comparing models:** the Transformers libraries may download base
model files if not cached. The comparison takes time and memory and writes
`comparison_results.md` in truncate mode. Preserve any report you need before
running:

```powershell
uv run --no-sync python .\compare_models.py
```

Fine-tuning is a longer-running training operation and writes to the existing,
Git-ignored `fine_tuned_model/` directory. Do not run it unless you intend to
train again and preserve or replace those local model artifacts.
