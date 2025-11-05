import pandas as pd
from pathlib import Path

# Step 1: Define folders
RAW_DIR = Path("data/raw")
PROC_DIR = Path("data/processed")
PROC_DIR.mkdir(parents=True, exist_ok=True)

# Step 2: Load raw CSV
raw_path = RAW_DIR / "sample_responses.csv"
df = pd.read_csv(raw_path)

# Step 3: Basic check
print(" Loaded data shape:", df.shape)
print("Columns:", df.columns.tolist())

# Step 4: Save cleaned version
out_path = PROC_DIR / "responses_cleaned.csv"
df.to_csv(out_path, index=False)
print(f" Cleaned file saved to {out_path}")



