
import sklearn

from utils import linkedln_scrapper
from data import job_title_skills_data
linkedinUrl = input("Enter your Linkedin Profile  Url :")

def linkedin_url_to_id(url):
    prefix = "https://www.linkedin.com/in/"
    suffix = "/"
    
    if url.startswith(prefix):
        url = url[len(prefix):]  # Remove the prefix
    
    if url.endswith(suffix):
        url = url[:-len(suffix)]  # Remove the trailing slash
    
    return url

linkedinid=linkedin_url_to_id(linkedinUrl)

userInfo=linkedln_scrapper.Scrapper(linkedinid)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

tfidf = TfidfVectorizer()
job_titles_vectorized = tfidf.fit_transform(job_title_skills_data.df['Job Title'])

# Function to calculate cosine similarity
def calculate_similarity(user_input,top_k=5):
    user_input = ' '.join(user_input) 
    # Vectorize the user input skills
    user_input_vectorized = tfidf.transform([user_input])

    similarity_scores = cosine_similarity(user_input_vectorized, job_titles_vectorized)
    similarity_scores_flat = similarity_scores.flatten()

    top_indices = similarity_scores_flat.argsort()[::-1][:top_k]
    recommended_job_titles = [job_title_skills_data.df['Job Title'][i] for i in top_indices]
    similarity_percentages = [similarity_scores_flat[i] * 100 for i in top_indices]

    return recommended_job_titles, similarity_percentages



recommendations,percent = calculate_similarity(userInfo)

# Print recommended job titles
print("------Top 5 Recommendations based on your Profile------\n")

for title, percent in zip(recommendations, percent):
    print(f"Your profile matches {percent} % with {title}")