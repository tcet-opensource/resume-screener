import json
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from model_data.dataset.skill_recommendation.skills import skills_list
from model_data.dataset.skill_recommendation.discription import discription_list
import pickle
from sklearn.metrics.pairwise import cosine_similarity


class SkillRecommendation:
    def __init__(
        self,
        resume_path="models/json-data/resume.json",
        model_path="models\pickled_models\skill_model.pkl",
        preds_path="models/json-data/similar_skills.json",
        n_neighbors=3,
        n_top=3,
    ):
        self.resume_path = resume_path
        self.model_path = model_path
        self.preds_path = preds_path
        self.n_neighbors = n_neighbors
        self.n_top = n_top

    def get_data(self):
        with open(self.resume_path, "r") as f:
            data = json.load(f)

        skills = skills_list
        discription = discription_list
        project_skills = []
        for project in data["projects"]:
            project_skills.extend(project["technologies"])
        for skill in data["skills"]:
            project_skills.append(skill["name"])
        return skills, discription, project_skills

    def get_model(self):
        skills, discription, project_skills = self.get_data()
        skill_data = pd.DataFrame({"skill": skills, "description": discription})
        tfidf_vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_skills = tfidf_vectorizer.fit_transform(skill_data["description"])
        skill_vectors = tfidf_vectorizer.fit_transform(project_skills)
        knn_model = NearestNeighbors(metric="cosine", algorithm="auto", n_neighbors=5)
        knn_model.fit(tfidf_skills)
        return knn_model, skill_data, project_skills, tfidf_skills, skill_vectors

    def create_skill_list(self, skills_list):
        similar_skills_dict = {}
        for skill in skills_list:
            try:
                recommended_skills = self.recommend_similar_skills_knn(skill)
            except IndexError:
                try:
                    recommended_skills = self.recommend_similar_skills_sim(skill)
                except Exception as e:
                    print(f"The following error occuerd: {e}")
                    recommended_skills = []
            similar_skills_dict[skill] = recommended_skills
        return similar_skills_dict

    def recommend_similar_skills_sim(self, skill_name):
        vectorizer = TfidfVectorizer()
        corpus = skills_list + [skill_name]
        vectorizer = TfidfVectorizer()
        vectorized_corpus = vectorizer.fit_transform(corpus)
        similarities = cosine_similarity(
            vectorized_corpus[-len(skill_name) :],
            vectorized_corpus[: -len(skill_name)],
        )
        ranking = similarities.argsort()[::-1]
        for i, course in enumerate(skill_name):
            recommended_course = [skill_name[j] for j in ranking[i]]
        return recommended_course[: self.top_n]

    def recommend_similar_skills_knn(self, skill_name):
        knn_model, skill_data, _, tfidf_skills, _ = self.get_model()
        skill_index = skill_data[skill_data["skill"] == skill_name].index[0]

        skill_vector = tfidf_skills[skill_index]
        _, indices = knn_model.kneighbors(skill_vector, self.n_neighbors)
        similar_skills = []
        for index in indices[0]:
            if index != skill_index:
                similar_skills.append(skill_data["skill"][index])
        return similar_skills

    def get_predictions(self):
        _, _, project_skills, _, _ = self.get_model()
        similar_skills = self.create_skill_list(project_skills)
        with open(self.preds_path, "w") as f:
            json.dump({"similar_skills": similar_skills}, f, indent=4)

    def save_model(self):
        knn_model, _, _, _, _ = self.get_model()
        pickle.dump(knn_model, open(self.model_path, "wb"))


if __name__ == "__main__":
    model = SkillRecommendation()
    model.get_predictions()
    model.save_model()
