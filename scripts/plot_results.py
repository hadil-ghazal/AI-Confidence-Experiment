#Creating plots to see what the confidence and accuracy look like in action

#imports

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_PATH = Path("data/processed/responses_cleaned.csv")
OUT_DIR = Path("outputs/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

#loading data
df = pd.read_csv(DATA_PATH)


# rename first col to participant_id (the same as the other scripts steps)
df = df.rename(columns={df.columns[0]: "participant_id"})
#df["AI_Indicator"] = df["AI_Indicator"].astype(str).strip()
df["AI_Indicator"] = df["AI_Indicator"].astype(str).str.strip()



#create a accuracy plot
#we already have the total_correct and the average accuracy calcs

acc_group = (
    df.groupby("AI_Indicator")["avg_accuracy"]
      .mean()
      .reset_index()
)

plt.figure()
plt.bar(acc_group["AI_Indicator"], acc_group["avg_accuracy"])
plt.title("Average Accuracy By Category")
plt.ylabel("Average Accuracy from 0–1")
plt.xlabel("Category")
plt.ylim(0, 1)
plt.savefig(OUT_DIR / "accuracy_by_category.png", bbox_inches="tight")
plt.close()


#create a confidence plot

conf_cols = [c for c in df.columns if "confident" in c.lower()]

if len(conf_cols) > 0:
    df["mean_confidence"] = df[conf_cols].mean(axis=1)
    conf_group = (
        df.groupby("AI_Indicator")["mean_confidence"]
          .mean()
          .reset_index()
    )

    plt.figure()
    plt.bar(conf_group["AI_Indicator"], conf_group["mean_confidence"])
    plt.title("Avrg confidence by category")
    plt.ylabel("Average confidence: 0–10")
    plt.xlabel("Category")
    plt.ylim(0, 10)
    plt.savefig(OUT_DIR / "confidence_by_category.png", bbox_inches="tight")
    plt.close()
    
