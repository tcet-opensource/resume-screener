import json
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from skills import skills_list
from resume_data import resume_data_list

with open("resume.json", "r") as f:
    data = json.load(f)

nltk.download("stopwords")
nltk.download("wordnet")
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
vectorizer = TfidfVectorizer(stop_words="english")

resume_data = resume_data_list

skills = skills_list
project_skills = []
for project in data["projects"]:
    project_skills.extend(project["technologies"])
for skill in data["skills"]:
    project_skills.append(skill["name"])


def preprocess_text(text):
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = nltk.word_tokenize(text.lower())
    tokens = [token for token in tokens if token not in stop_words]
    stems = [stemmer.stem(token) for token in tokens]
    lemmas = [lemmatizer.lemmatize(token) for token in tokens]

    return stems, lemmas


preprocessed_resume_data = []
for resume in resume_data:
    stems, lemmas = preprocess_text(resume)
    preprocessed_resume_data.append(" ".join(lemmas))

preprocessed_skill_list = []
for skill in project_skills:
    stems, lemmas = preprocess_text(skill)
    preprocessed_skill_list.append(" ".join(lemmas))

vectorizer.fit(preprocessed_resume_data)
resume_data_vectorized = vectorizer.transform(preprocessed_resume_data)
skill_list_vectorized = vectorizer.transform(preprocessed_skill_list)
skill_vectors = vectorizer.transform(skills)


def recommend_similar_skills(skill_name, skill_vectors, tfidf_vectorizer, top_n=10):
    skill_vector = tfidf_vectorizer.transform([skill_name])
    cosine_similarities = cosine_similarity(skill_vector, skill_vectors)
    similar_skill_indices = cosine_similarities.argsort()[0][-top_n - 1 : -1][::-1]
    similar_skills = [skills[i] for i in similar_skill_indices]
    return similar_skills


similar_skills = recommend_similar_skills(
    "Civil Engineering Construction", skill_vectors, vectorizer
)
print(similar_skills)

data = {"similar_skills": similar_skills}

with open("recommend_skills.json", "w") as f:
    json.dump(data, f, indent=4)
