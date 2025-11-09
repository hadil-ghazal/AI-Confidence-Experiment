#No AI tools were used for this code

#starting imports first
import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
PROC_DIR = Path("data/processed")
PROC_DIR.mkdir(parents=True, exist_ok=True)

# listing  all 4 google form files
files = [
    "Trivia A - With AI Suggestions  (Responses) - Form Responses 1.csv",
    "Trivia A - Without AI Suggestions (Responses) - Form Responses 1.csv",
    "Trivia B - With AI Suggestions (Responses) - Form Responses 1.csv",
    "Trivia B - Without AI Suggestions  (Responses) - Form Responses 1.csv",
]

parts = []
for f in files:
    df = pd.read_csv(RAW_DIR / f)
    df["source_form"] = f  # keep track
    parts.append(df)

# merge everything
merged = pd.concat(parts, ignore_index=True)

# THIS WAS MISSING BEFORE:need to fix the first two columns because they were a duplicate of participant ID twice
cols = list(merged.columns)
if len(cols) >= 2:
    merged = merged.rename(
        columns={
            cols[0]: "timestamp",
            cols[1]: "participant_id",
        }
    )
    # clean IDs
    merged["participant_id"] = merged["participant_id"].astype(str).str.strip()

# figure out correctness columns
correct_cols = [c for c in merged.columns if "Correctness_Indicator" in c]

if len(correct_cols) > 0:
    merged["total_correct"] = merged[correct_cols].sum(axis=1)
    merged["avg_accuracy"] = merged["total_correct"] / len(correct_cols)
else:
    print(" no correctness data is found")

# saving now
out_path = PROC_DIR / "responses_cleaned.csv"
merged.to_csv(out_path, index=False)

print("the merged file saved to", out_path)
print("Rows:", merged.shape[0])
print("Columns:", merged.columns.tolist())

