#No AI was used to generate this code - authored by Hadil Ghazal on 11/15/25

#initial imports
import os
import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import chi2_contingency, f_oneway, levene, kruskal, mannwhitneyu



#paths
DATA_PATH = "data/processed/responses_cleaned_v2.csv"
STATS_DIR = "outputs/stats"

os.makedirs(STATS_DIR, exist_ok=True)


#loading data

df = pd.read_csv(DATA_PATH)

#initial cleaning and format standardization

df["ai_status"] = df["ai_status"].astype(str).str.strip()
df["suggestion_text"] = df["suggestion_text"].astype(str).str.strip()


#To capture AI incorrect suggestions
wrong_suggestions_phrases = [
    "sydney",      # capital of Australia (correct is Canberra)
    "usa",         # coffee consumption (correct is Finland)
    "egypt",       # invented paper (correct is China)
    "uganda",      # Mount Kilimanjaro (correct is Tanzania)
    "1995",        # Pulp Fiction (correct is 1994)
    "1917-1921",   # WWI (correct is 1914-1918)
    "jupiter",     # most moons (correct is Saturn)
    "amazon",      # longest river (correct is Nile)
]

def get_ai_condition(row):
    """
    Put each question into one of three buckets:
    - 'AI - correct suggestion'
    - 'AI - wrong suggestion'
    - 'No AI'
    """
    if row["ai_status"].strip().lower() != "ai":
        return "No AI"

    text = row["suggestion_text"].strip().lower()
    if any(bad in text for bad in wrong_suggestions_phrases):
        return "AI - wrong suggestion"

    return "AI - correct suggestion"

df["ai_condition_detail"] = df.apply(get_ai_condition, axis=1)

#Making sure confidence and correctness are numeric and dropping missing
df["confidence"] = pd.to_numeric(df["confidence"], errors="coerce")
df["correct"] = pd.to_numeric(df["correct"], errors="coerce")

df = df.dropna(subset=["confidence", "correct"])
df["correct"] = df["correct"].astype(int)


# DOING ACCURACY ANALYSIS HERE

#building table with rows being the conditions and columns being correct or incorrect
contingency = pd.crosstab(df["ai_condition_detail"], df["correct"])

#renaming the columns
contingency.columns = ["incorrect", "correct"]

chi2, p_chi2, dof, expected = chi2_contingency(contingency)

n_total = contingency.values.sum()

#For Cramers V will be using the smallest dimension -1
min_dim = min(contingency.shape) - 1
if min_dim > 0:
    cramers_v = np.sqrt(chi2 / (n_total * min_dim))
else:
    cramers_v = np.nan


print("Accuracy by AI category (contingency table)")
print(contingency)
print()


print("Chi-square test of independence (3x2):")
print(f"  chi2 = {chi2:.2f}")
print(f"  dof  = {dof}")
print(f"  p    = {p_chi2:.4f}")
print(f"  Cramer's V = {cramers_v:.2f}")
print()


#Saving the table for the repo
contingency.to_csv(os.path.join(STATS_DIR, "accuracy_contingency_table.csv"))


#Now doing condition level sumary for n, accuracy and avg confidence

condition_summary = (
    df.groupby("ai_condition_detail")
      .agg(
          n=("correct", "size"),
          mean_accuracy=("correct", "mean"),
          mean_confidence=("confidence", "mean"),
          sd_confidence=("confidence", "std"),
      )
      .reset_index()
)

print("Category summary (accuracy and confidence)")
print(condition_summary)
print()


condition_summary.to_csv(
    os.path.join(STATS_DIR, "condition_summary_accuracy_confidence.csv"),
    index=False
)


#COnfidence Analysis (using ANOVA, Levene and Kruskal Wallis)

#V2 realized I need to order the groups for the ability to read easier
conditions_order = ["AI - correct suggestion", "AI - wrong suggestion", "No AI"]

groups = []
for cond in conditions_order:
    g = df.loc[df["ai_condition_detail"] == cond, "confidence"]
    groups.append(g)

print("Confidence descriptive statistics by each condition")
for cond, g in zip(conditions_order, groups):
    print(
        f"{cond}: n={len(g)}, mean={g.mean():.2f}, sd={g.std(ddof=1):.2f}"
    )
print()


#Using ANOVA for reference, this is not the main test
#Using the standard flow - starting with ANOVA when assumptions are roughly met
f_stat, f_p = f_oneway(*groups)
print("One-way ANOVA on confidence (for reference):")
print(f"  F = {f_stat:.2f}, p = {f_p:.4f}")
print()

#Levene's test for variance, checking if variance across the groups are roughly equal
#Anova assumed equal variance so using this as a secondary pass to see if that is a bad assumption. 
#if the variance ends up being very different, will use the Krustal-Wallis non parameter method in place of ANOVA

lev_stat, lev_p = levene(*groups)
print("Levene's test for equal variances:")
print(f"  W = {lev_stat:.2f}, p = {lev_p:.4f}")
print()


#Kruskal Wallis - main test to drive report and narrative
# using this test because confidence is 0-10 numberic rating so doing a one way ANOVA
#will use as the main test because its foing to be more robust when the variance is shaky , will compare the confidence distributions for the 3 categories
H_stat, H_p = kruskal(*groups)
print("Kruskal–Wallis test on confidence (main test):")
print(f"  H = {H_stat:.2f}, p = {H_p:.4f}")
print()


# Paiwise tests, decided to use Mann Whit

alpha = 0.05 
m_comparisons = 3  # 3 pairwise tests
bonf_alpha = alpha / m_comparisons  #this is the adjusted significance level


pairs = [
    ("AI - correct suggestion", "AI - wrong suggestion"),
    ("AI - correct suggestion", "No AI"),
    ("AI - wrong suggestion", "No AI"),
]

pairwise_results = []

for g1_label, g2_label in pairs:
    g1 = df.loc[df["ai_condition_detail"] == g1_label, "confidence"]
    g2 = df.loc[df["ai_condition_detail"] == g2_label, "confidence"]

    stat, p_raw = mannwhitneyu(g1, g2, alternative="two-sided")
    # Bonferroni-adjusted p-value: multiply by number of comparisons and cap at 1.0
    p_bonf = min(p_raw * m_comparisons, 1.0)
    significant = p_bonf < alpha

    pairwise_results.append(
        {
            "group_1": g1_label,
            "group_2": g2_label,
            "mannwhitney_U": stat,
            "p_raw": p_raw,
            "p_bonferroni": p_bonf,
            "significant_at_0.05": significant,
        }
    )

pairwise_df = pd.DataFrame(pairwise_results)

print("Pairwise Mann–Whitney U tests On confidence")
print(pairwise_df)
print()

# Save pairwise results so they can be referenced directly in the report
pairwise_df.to_csv(
    os.path.join(STATS_DIR, "confidence_pairwise_mannwhitney.csv"),
    index=False
)

print("Saved files to:")
print(f"  {os.path.join(STATS_DIR, 'accuracy_contingency_table.csv')}")
print(f"  {os.path.join(STATS_DIR, 'condition_summary_accuracy_confidence.csv')}")
print(f"  {os.path.join(STATS_DIR, 'confidence_pairwise_mannwhitney.csv')}")

