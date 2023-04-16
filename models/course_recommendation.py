import json
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from course_list import engineering_courses
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

engineering_courses = engineering_courses
resume_courses = []

for courses in data["courses"]:
    resume_courses.append(courses["title"])


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

preprocessed_resume_courses = []
for course in resume_courses:
    stems, lemmas = preprocess_text(course)
    preprocessed_resume_courses.append(" ".join(lemmas))

vectorizer.fit(preprocessed_resume_data)
resume_data_vectorized = vectorizer.transform(preprocessed_resume_data)
resume_courses_vectorized = vectorizer.transform(preprocessed_resume_courses)
engineering_courses_vectorized = vectorizer.transform(engineering_courses)


def recommend_similar_course(course_name, course_vectors, tfidf_vectorizer, top_n=10):
    course_vector = tfidf_vectorizer.transform([course_name])
    cosine_similarities = cosine_similarity(course_vector, course_vectors)
    similar_course_indices = cosine_similarities.argsort()[0][-top_n - 1 : -1][::-1]
    similar_courses = [engineering_courses[i] for i in similar_course_indices]
    return similar_courses


similar_course = recommend_similar_course(
    "Web Development", engineering_courses_vectorized, vectorizer
)
print(similar_course)

data = {"similar_course": similar_course}

with open("reccomended_course.json", "w") as f:
    json.dump(data, f, indent=4)
