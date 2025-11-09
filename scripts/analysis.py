#No AI tools were used to generate this code
#imports

import pandas as pd
from scipy import stats

#loading the file 
df = pd.read_csv("data/processed/responses_cleaned.csv")


# Fixing the duplicate ID issue from the merged file
df = df.rename(columns={df.columns[0]: "timestamp", df.columns[1]: "participant_id"})
df = df.loc[:, ~df.columns.duplicated()]  # Drop any duplicate columns



#issue in the participant ID using step to list columns for code fix
print("Columns in file:")
print(df.columns.tolist())

#removed section post particiapant ID restructuring
#noticed that participant Id is too long so step is to shorten naming convention
#orig_id_col = "Please create and enter your unique Participant ID using 2 letters + 4 digits (ex HG1997).\nUse this exact same ID in both quizzes."
#df = df.rename(columns={df.columns[0]: "participant_id"})


#check name fix
print("Renamed columns:")
print(df.columns.tolist())


#spaces causing issues so trimming here
df["AI_Indicator"] = df["AI_Indicator"].str.strip()


#check what values AI_Indicator has
print("AI_Indicator unique values:", df["AI_Indicator"].unique())

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

print("data after the combining step:")
print(comparison_df.head())

#running paired t-test using created AI indicators in data cleaning step
if "AI" in comparison_df.columns and "No AI" in comparison_df.columns:
    ai_id = comparison_df["AI"]
    noai_id = comparison_df["No AI"]
	
    t_stat, p_val = stats.ttest_rel(ai_id, noai_id)

    print("\n=== Accuracy comparison (AI vs No AI) ===")
    print("AI mean accuracy:   ", round(ai_id.mean(), 3))
    print("No AI mean accuracy:", round(noai_id.mean(), 3))
    print("t =", round(t_stat, 3), "p =", round(p_val, 4))
    print("rows used:", len(comparison_df))
else:

        print("\n️ Column names in AI_Indicator are not 'AI' and 'No AI'.")
        print("the columns locatedd:", comparison_df.columns.tolist())
        print("input values to adjust the scipt.")


