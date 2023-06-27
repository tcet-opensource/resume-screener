from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import docx2txt
import nltk
nltk.download('stopwords')
import re
import operator
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import io


class ResumeAnalyzer:
    def __init__(self):
        nltk.download('stopwords')
        nltk.download('punkt')
        self.stop_words = stopwords.words('english')

    def preprocess_text(self, text):
        clean_text = text.lower()
        clean_text = re.sub(r'[^\w\s]', '', clean_text)
        clean_text = clean_text.strip()
        clean_text = re.sub('[0-9]+', '', clean_text)
        clean_text = word_tokenize(clean_text)
        clean_text = [w for w in clean_text if not w in self.stop_words]
        return clean_text

    def job_description(self, jd):
        clean_jd = self.preprocess_text(jd)
        return clean_jd

    def word_cloud(self, jd):
        corpus = jd
        fdist = FreqDist(corpus)

        words = ' '.join(corpus)
        words = words.split()

        data = dict()

        for word in words:
            word = word.lower()
            data[word] = data.get(word, 0) + 1

        sorted_data = dict(sorted(data.items(), key=operator.itemgetter(1), reverse=True))

        word_cloud = WordCloud(width=800, height=800, background_color='white', max_words=500)
        word_cloud.generate_from_frequencies(sorted_data)

        plt.figure(figsize=(10, 8), edgecolor='k')
        plt.imshow(word_cloud, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.show()

    def get_resume_score(self, text):
        cv = CountVectorizer(stop_words='english')
        count_matrix = cv.fit_transform(text)
        print("\nSimilarity Scores:")

        match_percentage = cosine_similarity(count_matrix)[0][1] * 100
        match_percentage = round(match_percentage, 2)

        print("Your resume matches about " + str(match_percentage) + "% of the job description.")

    def read_pdf(self, pdf_doc):
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        with open(pdf_doc, 'rb') as fh:
            for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                page_interpreter.process_page(page)
            text = fake_file_handle.getvalue()

        converter.close()
        fake_file_handle.close()
        if text:
            return text


def main():
    analyzer = ResumeAnalyzer()

    extn = input("Enter File Extension: ")
    if extn == "pdf":
        resume = analyzer.read_pdf('utils\example.pdf')

    job_description = input("\nEnter the Job Description: ")
    clean_jd = analyzer.job_description(job_description)
    text = [resume, job_description]
    analyzer.get_resume_score(text)


if __name__ == '__main__':
    main()
