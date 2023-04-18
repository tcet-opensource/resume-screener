import json
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import pickle


def get_data(
    data_path="models/model_data/dataset/course_recommendation/preprocessed_data.csv",
    resume_path="models/json_data/resume.json",
):
    course_data = pd.read_csv(data_path)
    with open(resume_path, "r") as f:
        data = json.load(f)
    courses = []
    for course in data["courses"]:
        if course["title"].find("-") != -1:
            courses.append(course["title"][: course["title"].find("-") - 1])
        else:
            courses.append(course["title"])
    print("courses: ", courses)
    return course_data, courses


def get_model():
    course_data, courses = get_data()
    tfidf_vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_skills = tfidf_vectorizer.fit_transform(course_data["Description"])
    skill_vectors = tfidf_vectorizer.fit_transform(courses)
    knn_model = NearestNeighbors(metric="cosine", algorithm="brute", n_neighbors=5)
    knn_model.fit(tfidf_skills)
    return knn_model, course_data, courses, tfidf_skills, skill_vectors


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
    knn_model, course_data, _, tfidf_skills, _ = get_model()
    course_index = course_data[course_data["Title"] == course_name].index[0]

    course_vector = tfidf_skills[course_index]
    _, indices = knn_model.kneighbors(course_vector, n_neighbors)
    similar_courses = []
    for index in indices[0]:
        if index != course_index:
            similar_courses.append(course_data["Title"][index])
    return similar_courses


def get_predictions(file_path="models/json_data/similar_courses.json"):
    _, _, courses, _, _ = get_model()
    similar_courses = create_course_list(courses, n_neighbors=5)
    with open(file_path, "w") as f:
        json.dump({"similar_courses": similar_courses}, f, indent=4)


def save_model(file_path="models\pickled_models\course_model.pkl"):
    knn_model, _, _, _, _ = get_model()
    pickle.dump(knn_model, open(file_path, "wb"))


if __name__ == "__main__":
    get_predictions()
    save_model()
