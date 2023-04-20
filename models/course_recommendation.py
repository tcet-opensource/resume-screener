import json
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pickle
import string
from model_data.course_list import engineering_courses


def get_data(
    data_path="models/model_data/dataset/course_recommendation/preprocessed_data.csv",
    resume_path="models/json_data/resume.json",
):
    def remove_punctuations(x):
        return x.translate(str.maketrans("", "", string.punctuation))

    course_data = pd.read_csv(data_path)
    with open(resume_path, "r") as f:
        data = json.load(f)
    courses = []
    for course in data["courses"]:
        if course["title"].find("-") != -1:
            _ = course["title"][: course["title"].find("-") - 1].lower()
            courses.append(_)
            courses.extend(_.split(" "))
        else:
            _ = course["title"].lower()
            courses.append(_)
            courses.extend(_.split(" "))
    courses = list(map(remove_punctuations, courses))
    return course_data, courses


def get_model():
    course_data, courses = get_data()
    tfidf_vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_course = tfidf_vectorizer.fit_transform(course_data["Description"])
    course_vectors = tfidf_vectorizer.fit_transform(courses)
    knn_model = NearestNeighbors(metric="cosine", algorithm="auto", n_neighbors=5)
    knn_model.fit(tfidf_course)
    return knn_model, course_data, courses, tfidf_course, course_vectors


def create_course_list(courses_list, n_neighbors, top_n=5):
    similar_courses_dict = {}
    for course in courses_list:
        try:
            recommended_courses = recommend_similar_courses_knn(course, n_neighbors=5)
        except IndexError:
            try:
                recommended_courses = recommend_similar_course_sim(course, top_n=5)
            except ValueError:
                recommended_courses = ["Not available in database"]
        similar_courses_dict[course] = recommended_courses
    return similar_courses_dict


def recommend_similar_courses_knn(course_name, n_neighbors=5):
    knn_model, course_data, _, tfidf_course, _ = get_model()
    course_index = course_data[course_data["Title"] == course_name].index[0]

    course_vector = tfidf_course[course_index]
    _, indices = knn_model.kneighbors(course_vector, n_neighbors=5)
    similar_courses = []
    for index in indices[0]:
        if index != course_index:
            similar_courses.append(course_data["Title"][index])
    return similar_courses


def recommend_similar_course_sim(course_name, top_n=5):
    vectorizer = CountVectorizer()
    course_names = list(get_data()[0]["Title"])
    _ = engineering_courses
    course_names.extend(_)
    features = vectorizer.fit_transform(course_names)
    similarity_matrix = cosine_similarity(features)
    input_course_index = course_names.index(course_name)
    similarity_scores = list(enumerate(similarity_matrix[input_course_index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    top_courses = [course_names[i] for i, score in similarity_scores[1:4]]
    print(top_courses)
    return top_courses


def get_predictions(file_path="models/json_data/similar_courses.json"):
    _, _, courses, _, _ = get_model()
    similar_courses = create_course_list(courses, n_neighbors=5, top_n=5)
    print(similar_courses)
    with open(file_path, "w") as f:
        json.dump({"similar_courses": similar_courses}, f, indent=4)


def save_model(file_path="models\pickled_models\course_model.pkl"):
    knn_model, _, _, _, _ = get_model()
    pickle.dump(knn_model, open(file_path, "wb"))


if __name__ == "__main__":
    get_predictions()
    save_model()
