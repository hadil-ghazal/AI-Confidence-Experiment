# This file was lightly refactored with ChatGPT (GPT-5 Thinking) on 2025-11-08.
# AI assistance was limited to formatting, documentation, and minor structural alignment.
# All analytical logic, data manipulation, and interpretation remain authored by the student.

#imports

import pandas as pd
from scipy import stats

#loading the file 
df = pd.read_csv("data/processed/responses_cleaned.csv")


# Fixing the duplicate ID issue from the merged file
df = df.rename(columns={df.columns[0]: "timestamp", df.columns[1]: "participant_id"})
df = df.loc[:, ~df.columns.duplicated()]  # Drop any duplicate columns



#issue in the participant ID using step to list columns for code fix
print("Columns in file:")  # for debugging
print(df.columns.tolist())  # for debugging

#removed section post particiapant ID restructuring
#noticed that participant Id is too long so step is to shorten naming convention
#orig_id_col = "Please create and enter your unique Participant ID using 2 letters + 4 digits (ex HG1997).\nUse this exact same ID in both quizzes."
#df = df.rename(columns={df.columns[0]: "participant_id"})


#check name fix
print("Renamed columns:")  # for debugging
print(df.columns.tolist())  # for debugging


#spaces causing issues so trimming here
df["AI_Indicator"] = df["AI_Indicator"].str.strip()


#check what values AI_Indicator has
print("AI_Indicator unique values:", df["AI_Indicator"].unique())  # for debugging

#grouping participant ID so we get one row for each
grouped = (
    df.groupby(["participant_id", "AI_Indicator"])
      .agg(
          mean_accuracy=("avg_accuracy", "mean"),
          total_correct=("total_correct", "mean")
      )
      .reset_index()
)

#adding ai or no ai to the same row to compare performance
comparison_df  = grouped.pivot(index="participant_id", columns="AI_Indicator", values="mean_accuracy")


#data cleaning here - to drop anyone who only completed one form not both 
comparison_df  = comparison_df.dropna()

print("data after the combining step:")  # for debugging
print(comparison_df.head())  # for debugging

#running paired t-test using created AI indicators in data cleaning step
if "AI" in comparison_df.columns and "No AI" in comparison_df.columns:
    ai_id = comparison_df["AI"]
    noai_id = comparison_df["No AI"]
	
    t_stat, p_val = stats.ttest_rel(ai_id, noai_id)

    print("\n=== Accuracy comparison (AI vs No AI) ===")  # for debugging
    print("AI mean accuracy:   ", round(ai_id.mean(), 3))  # for debugging
    print("No AI mean accuracy:", round(noai_id.mean(), 3))  # for debugging
    print("t =", round(t_stat, 3), "p =", round(p_val, 4))  # for debugging
    print("rows used:", len(comparison_df))  # for debugging
else:

        print("\n️ Column names in AI_Indicator are not 'AI' and 'No AI'.")  # for debugging
        print("the columns locatedd:", comparison_df.columns.tolist())  # for debugging
        print("input values to adjust the scipt.")  # for debugging

