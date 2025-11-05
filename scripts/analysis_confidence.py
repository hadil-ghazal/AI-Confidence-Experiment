#analysis for confidence in data and responses. Does confidence vary with AI assistance?

import pandas as pd

#loading files we need

df = pd.read_csv("data/processed/responses_cleaned.csv")

#ensuring the rename of the first column to be participant id

df = df.rename(columns={df.columns[0]: "participant_id"})

# cleaning up the AI labels to ensure spaces dont lead to errors

df["AI_Indicator"] = df["AI_Indicator"].str.strip()

#capturing all columns where there are confidence feedback indicators

confidence_cols = [
    c for c in df.columns
    if "confident" in c.lower()
]


#stop if there's no confidence data
if len(confidence_cols) == 0:
    print("No confidence data")
    exit()

# IF YOU REACH THIS STEP THEN WE HAVE CONFIDENCE DATA IN THE DATA

# calculating the average confidence
df["mean_confidence"] = df[confidence_cols].mean(axis=1)

# group by person + AI category
grouped = (
    df.groupby(["participant_id", "AI_Indicator"])
      .agg(mean_confidence=("mean_confidence", "mean"))
      .reset_index()
)


#For each person, will be comparing non AI confidence with AI confidence

comparison_df = grouped.pivot(
    index="participant_id",
    columns="AI_Indicator",
    values="mean_confidence"
).dropna()

print("\nConfidence comparison (first 5 rows):")
print(comparison_df.head())

