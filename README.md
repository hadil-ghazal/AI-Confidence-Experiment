# AI-Confidence-Experiment
Statistical analysis of how AI suggestions influence human reasoning accuracy and confidence in decision making tasks

##1.  Project Overview 

This project explores how AI generate suggestions can influence a user's accuracy in answering trivia and is meant to analyze whether someone is more or less confident with their answers and if their accuracy

The survey was intentionally designed with inaccuracy built into the AI suggestions - at a 50% accuracy

There are 3 categories for how participants are being assessed for confidence and accuracy:
	1. AI with correct suggestion
	2. AI with incorrect suggestion
	3. No AI
Our core question is the following: How does exposure to correct vs. incorrect AI suggestions affect human accuracy and self-reported confidence on trivia questions, compared with no AI support?


##2. Experimental Design
###2.1 Structure

The study uses a mixed design:
Within-subject factor: AI exposure (each participant completes one AI-assisted form and one non-AI form).
Between-subject factor: Which form is paired with AI.
Group 1: Trivia A with AI, Trivia B without AI
Group 2: Trivia A without AI, Trivia B with AI
This counterbalances question sets to reduce content bias while still allowing within-subject comparisons.

###2.2 Variables

Independent variable:
ai_condition_detail ∈ {AI – correct, AI – wrong, No AI}
Dependent variables:
Accuracy (correct/incorrect)
Confidence (0–10 scale)

###2.3 AI Suggestions
Misleading AI suggestions included items(such as Sydney instead of Canberra for the capital of Australia). Of the AI suggestions, 50% were intentionally incorrect. These were deliberately chosen to test susceptibility to incorrect guidance.

##3. Hypotheses
Accuracy:

Null: Accuracy does not differ across AI conditions.
Alternative: Accuracy differs across conditions (expected pattern: correct AI > no AI > wrong AI)

Confidence:

Null: Mean confidence does not differ across AI conditions.
ALternative: Confidence differs across conditions (AI tends to raise confidence even when wrong).

Calibration:

Null: The relationship between confidence and accuracy is the same across conditions.
Alternative: Calibration differs (misleading AI produces confidence that does not match accuracy)

##4. Data Collection and Processing
###4.1 Data collection Method:
Data was collected using four Google Forms:
1. Trivia A with AI
2. Trivia A without AI
3. Trivia B with AI
4. Trivia B without AI

Each contained answer selections and a 0 to 10 confidence rating

###4.2 Data Cleaning 

Attempt 1 was made to combine all google form output but accidentally merged the AI indicator and made the categorizatoin of AI in the data inaccurate 
Attempt 2 (named V2 in the scripts) created a clean long format dataset with explicit AI status for ALL responses. This expanded the data into 300+ rows but made the analysis more accurate

##5. Power Analysis

power_analysis.py uses a standard paired samples power calculation (TTestPower) assuming:

Medium effect size (d = 0.5)
a = 0.05
Power = 0.80

This estimates a required sample size of ~33 participants.
In the intitial data design of this project I planned that If the realized N fell below the required calcs, conclusions would be treated as exploratory.

###Limitations:

1. The effect size assumptions may not match the true effects - If Ai influence ended up being minimal, more participants than intiially planned for would be required to show it definitively in the final visualizations

2. Data project has more than 2 elements to compare, increasing pairwise comparisons: Since more than just A-B comparisons were made, and I was assessing AI vs nonAI IN ADDITION to accuracy and confidence, it would require much larger data than I ended up collecting to create a more compelling data story

3. Form design may have introduced mild confounding with trivia difficulty: Part of accuracy and confidence could have been due to difficulty misalignments between both forms, leading to a potential drag there. In the future, this can be patched by introducing more forms and form combos to wider groups


##6. Analysis Workflow
V1: Initial merge and cleaning, issue came up with the AI flag being flattened 
V2: Reworked the data merge to be longer format and have accurate AI to no AI mappings, also produced grouped accuracy and confidence, combined AI tools to create and AI optimized version of the script which cleaned up mappings and naming conventions
V3: Made final changes to axis to address the challenge of the pairwise comparisons.
- added visualized elements for accuracy, confidence, AI indicator, and total percentages for ease of interpretation


##7. Visualization: 
The final visualization called accuracy_vs_confidence_dualaxis_v2_pct.png compares:
A. accuracy by confidence band broken up into 3 buckets:
	- 1. 0-5 confidence
	- 2. 6-7 confidence
	- 3. 8-10 confidence
B. Confidence Averages
C. All three AI conditions

###Interpretation: 
1. AI correct: shows the highest accuracy with confidence that rises proportionally
2. AI wrong: shows significantly less accuracy while confidence remains elevated
3. No AI shows moderate performance with confidence more closely aligned to accuracy


##8. Repository Structure
3 Branches were created:
main: initial work with all final scripts, data and figures
analysis-v2: created for all rework and code enhancements
ai-enhanced: PR where ChatGPT assisted with formatting and documentation. AI usage remains <20% of the scripts and the full chat history was linked for auditing

#9.#AI Usage Disclosure
Portions of this project used ChatGPT (GPT-5.1, Nov 2025) for formatting and documentation improvements on a separate ai enhanced branch. All experimental design, statistical reasoning, data cleaning logic, and analysis is authored solely by Hadil Ghazal Nov 2025. AI contributions were <20% and did not alter analytical logic


#10. Reporoducing the results and how to run:
1. run the cleaning using python clean_and_merge_v2.py
2. Run the analysis and visuals using python analysis_confidence_AI_relationship_v2.py
3. audit the power analysis using python power_analysis.py


#11. Final Interpretations and takeaways
Correct AI improved accuracy and increased confidence proportionally.
Wrong AI produced lower accuracy but still elevated confidence, highlighting over reliance on incorrect suggestions.
No AI showed moderate accuracy and the most consistent confidence accuracy alignment.
The visualization clearly demonstrates that misleading AI disrupts calibration: participants often remained confident even when incorrect, whereas correct AI strengthened both accuracy and confidence in tandem.

This project can be built upon in the future by expanding the participants to offset the survey design limitations


