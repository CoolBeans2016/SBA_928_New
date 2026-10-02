"""
download_dataset.py - Requirement 1 (Sourcing a dataset): load and inspect the
Marketing Research survey (.sav) stored in the 'Kaggle dataset' folder.

Run:  python download_dataset.py
Needs:  pip install pandas pyreadstat
"""
import os
import glob
import pyreadstat

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
matches = glob.glob(os.path.join(BASE_DIR, "Kaggle dataset", "*.sav"))
if not matches:
    raise SystemExit("No .sav file found in 'Kaggle dataset'. Put Marketing Research.sav there.")

sav_file = matches[0]
print(f"Loading survey file: {sav_file}")
df, meta = pyreadstat.read_sav(sav_file, apply_value_formats=True, formats_as_category=True)

print("\nSurvey loaded successfully!")
print("Shape (respondents, columns):", df.shape)

print("\nColumns: type | missing | survey question label | example answers")
for col in df.columns:
    question = meta.column_names_to_labels.get(col) or ""
    examples = list(df[col].dropna().unique()[:5])
    print(f"{col:10} | {str(df[col].dtype):9} | {df[col].isna().sum():4} missing | {question[:60]} | {examples}")

print("\nFirst 5 records:")
print(df.head())
