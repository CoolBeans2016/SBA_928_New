Quick setup — if you’ve done this kind of thing before
or

HTTPS

SSH
https://github.com/CoolBeans2016/SBA_928_New.git
Get started by creating a new file or uploading an existing file. We recommend every repository include a README, LICENSE, and .gitignore.

…or create a new repository on the command line
echo "# SBA_928_New" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/CoolBeans2016/SBA_928_New.git
git push -u origin main
…or push an existing repository from the command line
git remote add origin https://github.com/CoolBeans2016/SBA_928_New.git
git branch -M main
git push -u origin main

#=============================================
uv sync --group dev
uv run pytest
uv run ruff check .
uv run python -m sba_928.step_01_generate_dataset
uv run python -m sba_928.step_02_prompt_engineering --limit 12
uv run python -m sba_928.step_03_fine_tune --config config/default.json
uv run python -m sba_928.step_04_compare_models --fine-tuned-model artifacts/models/flan-t5-sba-928/final
uv run python -m sba_928.step_05_bias_audit
uv run python -m sba_928.step_06_custom_inference --model artifacts/models/flan-t5-sba-928/final --product "Wireless Mouse" --rating 3 --review "The mouse is comfortable, but it disconnects several times each day."