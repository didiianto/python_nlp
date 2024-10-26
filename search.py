from flask import Flask, render_template, request
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re
import string
import numpy as np

app = Flask(__name__)

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Function to preprocess text
def preprocess_text(text):
    text = text.lower()  # Lowercase
    text = text.translate(str.maketrans("", "", string.punctuation))  # Remove punctuation
    text = re.sub(r'\W', ' ', text)  # Replace non-word characters with spaces
    words = word_tokenize(text)  # Tokenize words
    stop_words = set(stopwords.words('indonesian'))  # Use Indonesian stopwords
    words = [word for word in words if word not in stop_words]  # Remove stopwords
    stemmer = PorterStemmer()  # Initialize stemmer
    words = [stemmer.stem(word) for word in words]  # Stemming
    return ' '.join(words)

# Function to calculate cosine similarity
def calculate_similarity(input_text, sentences, top_n=10):
    preprocessed_sentences = [preprocess_text(sentence) for sentence in sentences]
    preprocessed_input = preprocess_text(input_text)

    # Create the bag-of-words model
    vectorizer = CountVectorizer().fit_transform([preprocessed_input] + preprocessed_sentences)
    vectors = vectorizer.toarray()

    # Compute cosine similarity between input and other sentences
    cosine_sim = cosine_similarity(vectors[0:1], vectors[1:])

    # Flatten the similarity scores array
    cosine_sim_flat = cosine_sim.flatten()

    # Get the indices of top N similarity scores
    top_indices = np.argsort(cosine_sim_flat)[-top_n:][::-1]

    # Get the top N sentences and their similarity scores
    top_sentences = [(sentences[i], cosine_sim_flat[i]) for i in top_indices]

    return top_sentences

# Function to read sentences from CSV file
# file_path = r'D:\ProjectData\Python-project\env1\Latihan\documents_indonesia.csv'
def get_sentences_from_csv(file_path):
    df = pd.read_csv(file_path)
    # Assuming the CSV has a column named 'sentence'
    return df['santence'].tolist()

@app.route("/", methods=["GET", "POST"])
def index():
    top_n = 10  # Default to top 10 results
    top_results = []
    sentences = get_sentences_from_csv('documents_indonesia.csv')  # Path to your CSV file
    input_text = ""

    if request.method == "POST":
        input_text = request.form.get("input_text")
        top_n = int(request.form.get("top_n", 10))  # Get top N from form

        if input_text:
            # Calculate similarity
            top_results = calculate_similarity(input_text, sentences, top_n)
            
    return render_template("index.html", top_results=top_results, top_n=top_n, input_text=input_text)

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="127.0.0.1", port=5000)
