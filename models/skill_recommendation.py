import json
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from model_data.skills import skills_list
from model_data.discription import discription_list

with open("models/json_data/resume.json", "r") as f:
    data = json.load(f)

skills = skills_list
discription = discription_list
project_skills = []
for project in data["projects"]:
    project_skills.extend(project["technologies"])
for skill in data["skills"]:
    project_skills.append(skill["name"])
print(project_skills)


skill_data = pd.DataFrame({"skill": skills, "description": discription})

tfidf_vectorizer = TfidfVectorizer(stop_words="english")
tfidf_skills = tfidf_vectorizer.fit_transform(skill_data["description"])
skill_vectors = tfidf_vectorizer.fit_transform(project_skills)

knn_model = NearestNeighbors(metric="cosine", algorithm="brute", n_neighbors=5)
knn_model.fit(tfidf_skills)


def create_skill_list(skills_list, n_neighbors):
    similar_skills_dict = {}
    for skill in skills_list:
        try:
            recommended_skills = recommend_similar_skills(skill, n_neighbors)
        except IndexError:
            recommended_skills = ["Not available in database"]
        similar_skills_dict[skill] = recommended_skills
    return similar_skills_dict


def recommend_similar_skills(skill_name, n_neighbors):
    skill_index = skill_data[skill_data["skill"] == skill_name].index[0]

    skill_vector = tfidf_skills[skill_index]
    _, indices = knn_model.kneighbors(skill_vector, n_neighbors)
    similar_skills = []
    for index in indices[0]:
        if index != skill_index:
            similar_skills.append(skill_data["skill"][index])
    return similar_skills


similar_skills = create_skill_list(project_skills, n_neighbors=5)

with open("models/json_data/similar_skills.json", "w") as f:
    json.dump({"similar_skills": similar_skills}, f, indent=4)
