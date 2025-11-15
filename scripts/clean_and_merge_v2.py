# clean_and_merge.py had issues with the AI being flattened so this is v2 version
# This version fixes the issue where the AI and non-AI data got flattened
# It creates one long file with one row per question per participant so I can can add an AI split in the analysis

#initial imports and file paths
import pandas as pd
from pathlib import Path
raw_path = Path("data/raw")
out_path = Path("data/processed/responses_cleaned_v2.csv")
out_path.parent.mkdir(parents=True, exist_ok=True)

#creating a function to check what type of quiz it is and if it had AI suggestions
def get_quiz_info(df, filename):
    cols = df.columns
    quiz_type = "unknown"

    for c in cols:
        text = str(c).lower()
        if "first iphone" in text:
            quiz_type = "A"
            break
        if "planet has the shortest year" in text:
            quiz_type = "B"
            break

#checking if AI was used
    name = filename.lower()
    if "with ai" in name:
        ai_status = "AI"
    elif any("ai suggestion" in str(c).lower() for c in cols):
        ai_status = "AI"
    else:
        ai_status = "No AI"

    return quiz_type, ai_status


all_rows = []

#looping through each file in the raw folder
for file in raw_path.glob("Trivia*.csv"):
    df = pd.read_csv(file)
    quiz_type, ai_status = get_quiz_info(df, file.name)

    cols = df.columns

#going through each row
    for _, row in df.iterrows():
        timestamp = row.iloc[0]
        participant_id = row.iloc[1]

        qnum = 1
        i = 2
        # each question has three columns: question, confidence, and correctness
        while i + 2 < len(cols):
            q_col = cols[i]

            #stopping after reaching data indicator we want
            if "AI_Indicator" in q_col or "source_form" in q_col:
                break

            conf_col = cols[i + 1]
            correct_col = cols[i + 2]

            question_text = q_col
            answer = row[q_col]
            confidence = row[conf_col]
            correct = row[correct_col]

            #checking if the question had an AI suggestion in the text
            ai_suggestion = "AI Suggestion" in str(question_text)
            suggestion_text = None
            if ai_suggestion and "AI Suggestion:" in str(question_text):
                suggestion_text = str(question_text).split("AI Suggestion:", 1)[1].strip()

            all_rows.append({
                "timestamp": timestamp,
                "participant_id": participant_id,
                "quiz_type": quiz_type,
                "ai_status": ai_status,
                "question_number": qnum,
                "question_text": question_text,
                "answer": answer,
                "confidence": confidence,
                "correct": correct,
                "ai_suggestion": ai_suggestion,
                "suggestion_text": suggestion_text,
                "source_file": file.name
            })

            qnum += 1
            i += 3

#converting everything into one DataFrame and then saving
final = pd.DataFrame(all_rows)
final.to_csv(out_path, index=False)

#Validating counts and columns
print(f"Rows: {len(final)}")
print("Columns:", final.columns.tolist())

