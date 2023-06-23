from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from utils.github_scrapper import fetch_user_corpus
# Import job description
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def preprocess_text(corpus:list):
    new_corpus = ' '.join(corpus)

    # Removing characters other than alphabets and whitespaces
    document = re.sub("[^a-zA-Z\s]", "", new_corpus)

    # Splitting document into words
    words = document.split(' ')

    # Stemming
    stemmer = PorterStemmer()
    stemmed_corpus = ''
    for word in words:
        if word not in set(stopwords.words('english')):
                stemmed_corpus += ' ' + stemmer.stem(word)
    return [stemmed_corpus]

def generate_word_cloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def find_similarity(username, job_profile):
    user_corpus = fetch_user_corpus(username)
    job_corpus = job_profile
    
    preprocessed_user = preprocess_text(user_corpus)
    preprocessed_job = preprocess_text(job_corpus)

    tfidf = TfidfVectorizer(lowercase=True, stop_words=stopwords.words('english'))
    
    job_vectors = tfidf.fit_transform(preprocessed_job) # Inputs must be list
    user_vectors = tfidf.transform(preprocessed_user) # Inputs must be list

    similarity = cosine_similarity(user_vectors, job_vectors) # 2D array returned
    
    print(f"Your profile matched {similarity[0][0]*100:.2f}% with the job description!",end='\n\n')
    
    matched_words = tfidf.get_feature_names_out()[job_vectors.indices]
    matched_text = ' '.join(matched_words)
    generate_word_cloud(matched_text)
    
    return similarity

if __name__ == '__main__':
    username = input("Enter github username:")
    job_profile = '' # fetch_job_descs_corpus() Fetch and store the job description corpus to be passed into function
    print(find_similarity(username, job_profile))