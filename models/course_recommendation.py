import json
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.neighbors import NearestNeighbors

course_data = pd.read_csv(
    "models/model_data/dataset/course_recommendation/preprocessed_data.csv"
)

with open("models/json_data/resume.json", "r") as f:
    data = json.load(f)


courses = []
for course in data["courses"]:
    courses.append(course["title"])
print(courses)


tfidf_vectorizer = TfidfVectorizer(stop_words="english")
tfidf_skills = tfidf_vectorizer.fit_transform(course_data["Description"])
skill_vectors = tfidf_vectorizer.fit_transform(courses)

knn_model = NearestNeighbors(metric="cosine", algorithm="brute", n_neighbors=5)
knn_model.fit(tfidf_skills)


def create_course_list(courses_list, n_neighbors):
    similar_courses_dict = {}
    for course in courses_list:
        try:
            recommended_courses = recommend_similar_courses(course, n_neighbors)
        except IndexError:
            recommended_courses = ["Not available in database"]
        similar_courses_dict[course] = recommended_courses
    return similar_courses_dict


def recommend_similar_courses(course_name, n_neighbors):
    course_index = course_data[course_data["Title"] == course_name].index[0]

    course_vector = tfidf_skills[course_index]
    _, indices = knn_model.kneighbors(course_vector, n_neighbors)
    similar_courses = []
    for index in indices[0]:
        if index != course_index:
            similar_courses.append(course_data["Title"][index])
    return similar_courses


similar_courses = create_course_list(courses, n_neighbors=5)

with open("models/json_data/similar_courses.json", "w") as f:
    json.dump({"similar_courses": similar_courses}, f, indent=4)
