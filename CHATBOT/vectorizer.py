from sklearn.feature_extraction.text import TfidfVectorizer
from preprocessing import clean_text

def load_dataset(file_path):
    questions = []
    answers = []

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
        if not line:
            i += 1
            continue
        
        # Process question
        if line.startswith("Question:"):
            q = line.replace("Question:", "").strip()
            i += 1
            
            # Get the answer from next non-empty line
            if i < len(lines) and lines[i].strip().startswith("Answer:"):
                a = lines[i].replace("Answer:", "").strip()
                questions.append(clean_text(q))
                answers.append(a)
                i += 1
            else:
                i += 1
        else:
            i += 1

    return questions, answers

def vectorize_data(questions):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(questions)
    return X, vectorizer
