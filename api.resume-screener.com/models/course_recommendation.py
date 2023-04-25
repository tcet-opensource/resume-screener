import json
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import string
from model_data.dataset.course_recommendation.course_list import engineering_courses


class CourseRecommendation:
    def __init__(
        self,
        data_path="models/model_data/dataset/course_recommendation/preprocessed_data.csv",
        resume_path="models/json_data/resume.json",
        model_path="models\pickled_models\course_model.pkl",
        preds_path="models/json_data/similar_courses.json",
        n_neighbors=5,
        top_n=5,
    ):
        self.data_path = data_path
        self.resume_path = resume_path
        self.n_neighbors = n_neighbors
        self.top_n = top_n
        self.model_path = model_path
        self.preds_path = preds_path

    def get_data(self):
        def remove_punctuations(x):
            return x.translate(str.maketrans("", "", string.punctuation))

        course_data = pd.read_csv(self.data_path)
        with open(self.resume_path, "r") as f:
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

    def get_model(self):
        course_data, courses = self.get_data()
        tfidf_vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_course = tfidf_vectorizer.fit_transform(course_data["Description"])
        course_vectors = tfidf_vectorizer.fit_transform(courses)
        knn_model = NearestNeighbors(metric="cosine", algorithm="auto", n_neighbors=5)
        knn_model.fit(tfidf_course)
        return knn_model, course_data, courses, tfidf_course, course_vectors

    def create_course_list(self, courses_list):
        similar_courses_dict = {}
        for course in courses_list:
            try:
                recommended_courses = self.recommend_similar_courses_knn(course)
            except IndexError:
                try:
                    recommended_courses = self.recommend_similar_course_sim(course)
                except Exception as e:
                    print(f"The following error occuerd: {e}")
                    recommended_courses = []
            similar_courses_dict[course] = recommended_courses
        return similar_courses_dict

    def recommend_similar_courses_knn(self, course_name):
        knn_model, course_data, _, tfidf_course, _ = self.get_model()
        course_index = course_data[course_data["Title"] == course_name].index[0]

        course_vector = tfidf_course[course_index]
        _, indices = knn_model.kneighbors(course_vector, self.n_neighbors)
        similar_courses = []
        for index in indices[0]:
            if index != course_index:
                similar_courses.append(course_data["Title"][index])
        return similar_courses

    def recommend_similar_course_sim(self, course_name):
        vectorizer = TfidfVectorizer()
        course_names = list(self.get_data()[0]["Title"])
        _ = engineering_courses
        course_names.extend(_)
        corpus = course_names + [course_name]
        vectorizer = TfidfVectorizer()
        vectorized_corpus = vectorizer.fit_transform(corpus)
        similarities = cosine_similarity(
            vectorized_corpus[-len(course_name) :],
            vectorized_corpus[: -len(course_name)],
        )
        ranking = similarities.argsort()[::-1]
        for i, course in enumerate(course_name):
            recommended_course = [course_names[j] for j in ranking[i]]
        return recommended_course[: self.top_n]

    def get_predictions(self):
        _, _, courses, _, _ = self.get_model()
        similar_courses = self.create_course_list(courses)
        with open(self.preds_path, "w") as f:
            json.dump({"similar_courses": similar_courses}, f, indent=4)

    def save_model(self):
        knn_model, _, _, _, _ = self.get_model()
        pickle.dump(knn_model, open(self.model_path, "wb"))


if __name__ == "__main__":
    model = CourseRecommendation()
    model.get_predictions()
    model.save_model()
