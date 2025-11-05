# merging all separate trivia form response files into basic_merge_forms

import pandas as pd

# load each csv one by one
a_with_ai = pd.read_csv("data/raw/Trivia A - With AI Suggestions  (Responses) - Form Responses 1.csv")
a_no_ai = pd.read_csv("data/raw/Trivia A - Without AI Suggestions (Responses) - Form Responses 1.csv")
b_with_ai = pd.read_csv("data/raw/Trivia B - With AI Suggestions (Responses) - Form Responses 1.csv")
b_no_ai = pd.read_csv("data/raw/Trivia B - Without AI Suggestions  (Responses) - Form Responses 1.csv")

#Add Source column to indicate where each data row was pulled from
a_with_ai["source_form"] = "A_with_AI"
a_no_ai["source_form"] = "A_no_AI"
b_with_ai["source_form"] = "B_with_AI"
b_no_ai["source_form"] = "B_no_AI"

#concatenating all in the new data
combined = pd.concat([a_with_ai, a_no_ai, b_with_ai, b_no_ai], ignore_index=True)

#participant ids for uniqueness
id_col = [c for c in combined.columns if "Participant ID" in c][0]

#maintaining the same column naming conventions I earlier created in sheets
correct_cols = [c for c in combined.columns if "Correctness_Indicator" in c]
cols_to_keep = [id_col, "AI_Indicator", "source_form"] + correct_cols

clean = combined[cols_to_keep].copy()

#calculations for accuracy average and the plain total correct
clean["total_correct"] = clean[correct_cols].sum(axis=1)
clean["avg_accuracy"] = clean["total_correct"] / len(correct_cols)

#Saving version to processed
clean.to_csv("data/processed/responses_cleaned.csv", index=False)

#Some confirmations 
print(" merged and saved to data/processed/responses_cleaned.csv")
print("rows:", len(clean))
print("columns:", clean.columns.tolist())
