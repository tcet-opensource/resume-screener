from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Define the dataset
books = [
    "The Catcher in the Rye",
    "To Kill a Mockingbird",
    "1984",
    "Brave New World",
    "Animal Farm",
    "Pride and Prejudice",
    "Jane Eyre",
]

# Define the attributes of the item you want to recommend
target_book = "The Great Gatsby"
target_author = "F. Scott Fitzgerald"

# Define the corpus and vectorize the attributes
corpus = books + [target_book + " by " + target_author]
vectorizer = TfidfVectorizer()
vectorized_corpus = vectorizer.fit_transform(corpus)

# Calculate the cosine similarity between the target book and the other books in the corpus
similarities = cosine_similarity(vectorized_corpus[-1], vectorized_corpus[:-1])

# Rank the books based on their similarity to the target book and the user's estimated preference
ranking = similarities.argsort()[0][::-1]
recommended_books = [books[i] for i in ranking]

# Print the recommended books
print("Recommended books:")
for book in recommended_books:
    print("- " + book)
