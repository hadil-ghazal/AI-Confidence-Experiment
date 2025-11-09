# This file was lightly refactored with ChatGPT (GPT-5 Thinking) on 2025-11-08.
# AI assistance was limited to formatting, documentation, and minor structural alignment.
# All analytical logic, data manipulation, and interpretation remain authored by the student.

#V2 of the AI confidence analysis to add volumes since we need that for comparisons
# New analysis to determine the interrelationship between AI suggestion and confidence
# No AI was used to generate this code

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

#initial setup and path directories
DATA_PATH = Path("data/processed/responses_cleaned.csv")
OUT_DIR = Path("outputs/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

#loading data
df = pd.read_csv(DATA_PATH)
df = df.rename(columns={df.columns[0]: "timestamp", df.columns[1]: "participant_id"})

#cleaning AI labels
df["AI_Indicator"] = df["AI_Indicator"].astype(str).str.strip()

#finding the confidence and correctness columns
confidence_cols = [c for c in df.columns if "confident" in c.lower()]
correct_cols = [c for c in df.columns if "Correctness_Indicator" in c]

if len(confidence_cols) == 0 or len(correct_cols) == 0:
    print("No confidence or correctness columns found.")  # for debugging
    print("confidence_cols:", confidence_cols)  # for debugging
    print("correct_cols:", correct_cols)  # for debugging
    raise SystemExit

#melt to long
conf_long = df.melt(
    id_vars=["participant_id", "AI_Indicator"],
    value_vars=confidence_cols,
    var_name="question_conf",
    value_name="confidence",
)

acc_long = df.melt(
    id_vars=["participant_id", "AI_Indicator"],
    value_vars=correct_cols,
    var_name="question_acc",
    value_name="correct",
)

#aligning and merging the two long tables
merged = pd.concat(
    [conf_long.reset_index(drop=True), acc_long["correct"]],
    axis=1
)

# cleaning numeric confidence
merged["confidence"] = pd.to_numeric(merged["confidence"], errors="coerce")

#need to drop rows missing either confidence or correctness (even though data clean, step for data expansion in the future)
merged = merged.dropna(subset=["confidence", "correct"])

#creating confidence bucketing like scorecard categorization for deeper interrelational analysis
def conf_band(x):
    if x >= 8:
        return "High (8–10)"
    elif x >= 6:
        return "Medium (6–7)"
    else:
        return "Low (0–5)"

merged["confidence_band"] = merged["confidence"].apply(conf_band)


#V2 of conditional accuracy to include volumes for better comparisons
summary = (
    merged.groupby(["AI_Indicator", "confidence_band"])
    .agg(
        mean_accuracy=("correct", "mean"),
        n=("correct", "size")
    )
    .reset_index()
    .sort_values(["AI_Indicator", "confidence_band"])
)


#visualizing step
plt.figure(figsize=(7, 5))
for cond in summary["AI_Indicator"].unique():
    subset = summary[summary["AI_Indicator"] == cond]
    plt.plot(
        subset["confidence_band"],
        subset["mean_accuracy"],
        marker="o",
        label=cond,
    )

plt.title("Accuracy by Confidence Level and AI Condition")
plt.xlabel("Confidence Band")
plt.ylabel("Proportion Correct")
plt.legend(title="Condition")
plt.ylim(0, 1)

out_path = OUT_DIR / "accuracy_by_confidence_and_AI.png"
plt.savefig(out_path, bbox_inches="tight")
plt.close()

print("=== Conditional accuracy by confidence band ===")  # for debugging
print(summary)  # for debugging
print(f"\nSaved visualization to {out_path}")  # for debugging

#exporting summary table
summary_path = OUT_DIR / "accuracy_confidence_AI_summary.csv"
summary.to_csv(summary_path, index=False)
print(f"Summary table saved to {summary_path}")  # for debugging
