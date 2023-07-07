from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from utils.github_scrapper import fetch_user_corpus
# Import job description
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class github_analyser:
    def __init__(self):
        self.tfidf = TfidfVectorizer(lowercase=True, stop_words=stopwords.words('english'))
        self.stemmer = PorterStemmer()

    def preprocess_text(self, corpus):
        new_corpus = ' '.join(corpus)

        # Removing characters other than alphabets and whitespaces
        document = re.sub("[^a-zA-Z\s]", "", new_corpus)

        # Splitting document into words
        words = document.split(' ')

        # Stemming
        stemmed_corpus = ''
        for word in words:
            if word not in set(stopwords.words('english')):
                stemmed_corpus += ' ' + self.stemmer.stem(word)
        return [stemmed_corpus]

    def generate_word_cloud(self, text):
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

    def find_similarity(self, username, job_profile):
        user_corpus = fetch_user_corpus(username)
        job_corpus = job_profile
    
        preprocessed_user = self.preprocess_text(user_corpus)
        preprocessed_job = self.preprocess_text(job_corpus)

        job_vectors = self.tfidf.fit_transform(preprocessed_job)
        user_vectors = self.tfidf.transform(preprocessed_user)

        similarity = cosine_similarity(user_vectors, job_vectors)

        print(f"Your profile matched {similarity[0][0] * 100:.2f}% with the job description!", end='\n\n')
    
        matched_words = self.tfidf.get_feature_names_out()[job_vectors.indices]
        matched_text = ' '.join(matched_words)
        self.generate_word_cloud(matched_text)
    
        return similarity

if __name__ == '__main__':
    analyser = github_analyser()
    username = input("Enter GitHub username:")
    job_profile = ''  # Fetch and store the job description corpus to be passed into the function
    print(analyser.find_similarity(username, job_profile))
