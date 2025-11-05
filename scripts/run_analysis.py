import pandas as pd
from pathlib import Path
from scipy import stats

PROC_DIR = Path("data/processed")
df = pd.read_csv(PROC_DIR / "responses_cleaned.csv")

agg = (
    df.groupby(["participant_id", "condition"])
    .agg(mean_confidence=("confidence", "mean"),
         accuracy=("correct", "mean"))
    .reset_index()
)

wide = agg.pivot(index="participant_id", columns="condition")
wide.columns = [f"{a}_{b}" for a, b in wide.columns]
wide = wide.reset_index()

# Paired t-tests
t_conf, p_conf = stats.ttest_rel(wide["mean_confidence_AI"], wide["mean_confidence_NoAI"])
t_acc, p_acc = stats.ttest_rel(wide["accuracy_AI"], wide["accuracy_NoAI"])

print("=== Confidence Comparison ===")
print(f"AI mean: {wide['mean_confidence_AI'].mean():.2f}")
print(f"No-AI mean: {wide['mean_confidence_NoAI'].mean():.2f}")
print(f"t = {t_conf:.2f}, p = {p_conf:.4f}")

print("\\n=== Accuracy Comparison ===")
print(f"AI mean: {wide['accuracy_AI'].mean():.2f}")
print(f"No-AI mean: {wide['accuracy_NoAI'].mean():.2f}")
print(f"t = {t_acc:.2f}, p = {p_acc:.4f}")

