from flask import Flask, render_template, request
import mysql.connector
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

# MySQL Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',      # Replace with your MySQL username
    'password': '',   # Replace with your MySQL password
    'database': 'test'    # Replace with your MySQL database name
}

# Function to get MySQL connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route("/", methods=["GET", "POST"])
def search():
    top_n = 10  # Default to top 10 results
    search_results = []
    query = ""

    if request.method == "POST":
        query = request.form.get("search_query")
        top_n = int(request.form.get("top_n", 10))  # Get top N from form

        if query:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Prepare and execute the SQL query with LIKE
            sql_query = f"""
                SELECT * FROM documents 
                WHERE title LIKE %s OR santence LIKE %s 
                LIMIT %s
            """
            cursor.execute(sql_query, (f'%{query}%', f'%{query}%', top_n))
            search_results = cursor.fetchall()

            cursor.close()
            conn.close()

    return render_template("search.html", search_results=search_results, top_n=top_n, query=query)

if __name__ == "__main__":
      app.run(host="127.0.0.1", port=5001)
