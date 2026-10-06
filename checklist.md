# Completion and resubmission checklist

## Fixes applied

- [x] Remove the duplicated/malformed `TOPICS` assignment and extra bracket in
      `build_training_data.py`.
- [x] Remove the two fixed comparison prompts that had been misplaced in the
      builder's reusable `STYLES` list.
- [x] Restore the module-docstring opener in `compare_models.py`.
- [x] Declare project dependencies with `uv add`: pandas, pyreadstat, datasets,
      transformers, PEFT, PyTorch, NumPy, and Accelerate.
- [x] Add `SBA_928_Report.md` with an evaluation rubric, per-test ratings,
      interpretation, fine-tuning method, dataset description, and bias
      discussion.
- [x] Compile both repaired scripts successfully.
- [x] Verify the dependency lock metadata with `uv lock --check`.

## Validation still to finish safely

- [x] Check that the dependencies import. This verifies imports only; it does
      not load model weights:

      ```powershell
      uv run --no-sync python -c "import numpy, pandas, pyreadstat, datasets, transformers, peft, torch, accelerate; print('dependency imports ok')"
      ```

- [ ] Preserve the current generated data files before rerunning the builder.
      It writes and replaces `training_data.jsonl` and `prompt_summary.md`.
      After preserving them, run:

      ```powershell
      uv run --no-sync python .\build_training_data.py
      ```

      Compare the resulting count and category totals with the checked-in
      `prompt_summary.md` (168 examples: 72 consumer behavior, 48 market
      trends, 48 competitor analysis).

- [ ] Decide whether to rerun the comparison. **Before running:** Transformers
      may download base model files; loading and generating 18 responses takes
      time and memory. It also truncates/replaces `comparison_results.md`,
      currently deleted in the worktree. Preserve any valued copy first.
      Command:

      ```powershell
      uv run --no-sync python .\compare_models.py
      ```

- [ ] If the comparison is rerun, review the new text against the rubric in
      `SBA_928_Report.md` and update the ratings and conclusions. Do not
      present archived-output scores as if they came from a newly run model.

- [ ] Inspect the final Git diff before submission. Preserve the pre-existing
      report deletions and `git_camands.md` edits unless you decide separately
      to change them.

## Submission review against teacher feedback

- [x] Training-data generation syntax repaired.
- [x] Runtime dependencies declared in the `uv` project.
- [x] Model-comparison evaluation completed in the new report using available
      saved comparison evidence, with unsupported outputs called out.
- [x] Professional final SBA report created.
- [ ] End-to-end generation and data regeneration remain unverified because
      they can download model files or overwrite existing outputs.
