#No AI was used to generate this code, authored by Hadil Ghazal 11/9/25
#this is V2 of previous AI confidence analysis script because after seeing final visualizations and data results
#previous data was flattening the AI correctness suggestion so this new version builds on that
#creating new data element: "AI correct suggestion" and "AI incorrect suggestion"
#Update made on 11/14/25 by Hadil Ghazal to enhance the visualization by adding a dual axis to better show accuracy and average confidence together, and to label volumes/percents directly on the chart for clarity

#inital imports and file paths
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

DATA_PATH_V2 = Path("data/processed/responses_cleaned_v2.csv")
OUT_DIR = Path("outputs/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

#reading
df = pd.read_csv(DATA_PATH_V2)

#stripping strings to make sure everything is standardized and no issues come up later
df["ai_status"] = df["ai_status"].astype(str).str.strip()
df["suggestion_text"] = df["suggestion_text"].astype(str).str.strip()

#wrong suggestion indicators, with details of which AI suggestions were intentionally wrong
wrong_suggestions_phrases = [
    "sydney",          #"what is the capital of Australia" - correct answer was Canberry
    "usa",             #"Which country consumes the most coffee per capita?" - correct answer was Finland
    "egypt",           #"Which country invented paper?" - correct answer was China
    "uganda",          #"In which country is Mount Kilimanjaro located?" - correct answer was Tanzania
    "1995",            #"Which year was the film 'Pulp Fiction' released?" - correct answer was 1994
    "1917-1921",       #"In which years did World War I take place?" - correct answer was 1914-1918
    "jupiter",         #"Which planet has the most moons?" - correct answer was Saturn
    "amazon",          #"What is the longest river in the world?" - correct answer was Nile
]

#Categorizing all AI bucket labels
def ai_detail(row):
    #If there was no AI suggestion provided at all
    if str(row["ai_status"]).strip().lower() != "ai":
        return "No AI"
    #normalize suggestion text
    text = str(row["suggestion_text"]).strip().lower()
    #when a suggestion is provided but it is incorrect and meant to mislead the user
    if any(bad in text for bad in wrong_suggestions_phrases):
        return "AI - wrong suggestion"
    #else the remaining is AI correct suggestion
    return "AI - correct suggestion"

df["ai_condition_detail"] = df.apply(ai_detail, axis=1)

#dropping rows missing confidence or correctness
df = df.dropna(subset=["confidence","correct"])

#Bucketing volumes now
def confidence_bucket(x):
    try:
        x = float(x)
    except Exception:
        return "Unknown"
    if x >= 8:
        return "High Confidence(8-10)"
    elif x >= 6:
        return "Medium Confidence(6-7)"
    else:
        return "Low confidence(0-5)"

df["confidence_band"] = df["confidence"].apply(confidence_bucket)

#groupings are
#mean_accuracy: average correctness within each category
#n: the number of rows in each category/band
#avg_confidence: average self-reported confidence from 0-10 within each category
summary = (
    df.groupby(["ai_condition_detail", "confidence_band"])
      .agg(
          mean_accuracy=("correct","mean"),
          n=("correct","size"),
          avg_confidence=("confidence","mean")
      )
      .reset_index()
)

print("Accuracy by Ai condition and confidence V2")
print(summary)

#adding percentage helpers for context in the labels 
total_n = summary["n"].sum()
summary["pct_total"] = (summary["n"] / total_n * 100).round(1)  #percent of all rows
band_totals = summary.groupby("confidence_band")["n"].transform("sum")
summary["pct_in_band"] = (summary["n"] / band_totals * 100).round(1)  #percent within the individual section

#plotting the dual axis with left = accuracy and  right = average confidence
band_order = ["Low confidence(0-5)", "Medium Confidence(6-7)", "High Confidence(8-10)"]

plt.figure(figsize=(9,5))
ax = plt.gca()
ax2 = ax.twinx()

#using confidence explicitly as the label
for cat in ["AI - correct suggestion", "AI - wrong suggestion", "No AI"]:
    sub = summary[summary["ai_condition_detail"] == cat].copy()
    sub = sub.set_index("confidence_band").reindex(band_order).reset_index()

    #the left axis is accuracy
    ax.plot(sub["confidence_band"], sub["mean_accuracy"], marker="o", label=f"{cat} — accuracy")

    #the right axis will be average confidenc
    ax2.plot(sub["confidence_band"], sub["avg_confidence"], linestyle="--", marker="s", label=f"{cat} — avg confidence")

    #annotating each point with the volumes and percents
    for i, r in sub.iterrows():
        ax.annotate(
            f"n={int(r['n'])} ({r['pct_in_band']}%)",
            (r["confidence_band"], r["mean_accuracy"]),
            textcoords="offset points",
            xytext=(0,6),
            ha="center",
            fontsize=8
        )

ax.set_title("Accuracy and Average Confidence by Category and Confidence Band (V2)")
ax.set_xlabel("Confidence Band")
ax.set_ylabel("Accuracy (Proportion Correct)")
ax.set_ylim(0, 1)
ax2.set_ylabel("Average Confidence (0–10)")
ax2.set_ylim(0, 10)

#having two legends for clarity - attempt #3 of adjusting the legend on 11/14
#the previous version was blockign the chart so readjusting the alignment 
# leg1 = ax.legend(loc="lower left", bbox_to_anchor=(0, -0.25), title="Category")
leg1 = ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=3, title="Category")
# leg2 = ax2.legend(loc="lower right", bbox_to_anchor=(1, -0.25), title="Category")
leg2 = ax2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.30), ncol=3, title="Category")


plt.tight_layout()
plt.savefig(OUT_DIR / "accuracy_vs_confidence_dualaxis_v2_pct.png", bbox_inches="tight")
plt.close()

#saving the table for the write up and to reference
summary.to_csv(OUT_DIR / "accuracy_confidence_AI_v2_detailed_with_pct.csv", index=False)
print("saved figure and csv with percentages to outputs/figures/")

