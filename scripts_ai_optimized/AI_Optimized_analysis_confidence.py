# This file was lightly refactored with ChatGPT (GPT-5 Thinking) on 2025-11-08.
# AI assistance was limited to formatting, documentation, and minor structural alignment.
# All analytical logic, data manipulation, and interpretation remain authored by the student.

#analysis for confidence in data and responses. Does confidence vary with AI assistance?

import pandas as pd

#loading files we need

df = pd.read_csv("data/processed/responses_cleaned.csv")

#ensuring the rename of the first column to be participant id

#commented out for V2, reformatting post ID realignment
#df = df.rename(columns={df.columns[0]: "participant_id"})

#New formatting version
df = df.rename(columns={df.columns[0]: "timestamp", df.columns[1]: "participant_id"})

#Removing accidental duplicate participant_id column
df = df.loc[:, ~df.columns.duplicated()]


# cleaning up the AI labels to ensure spaces dont lead to errors

df["AI_Indicator"] = df["AI_Indicator"].str.strip()

#capturing all columns where there are confidence feedback indicators

confidence_cols = [
    c for c in df.columns
    if "confident" in c.lower()
]


#stop if there's no confidence data
if len(confidence_cols) == 0:
    print("No confidence data")  # for debugging
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

print("\nConfidence comparison (first 5 rows):")  # for debugging
print(comparison_df.head())  # for debugging
