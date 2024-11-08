from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import fasttext
import mysql.connector

app = Flask(__name__)

# FastText model loading (make sure to replace with your model path)
fasttext_model = fasttext.load_model(r"D:\ProjectData\Python-project\env1\cc.id.300.bin\cc.id.300.bin")

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


@app.route('/')
def index():
    db_conn = get_db_connection()
    cursor = db_conn.cursor(dictionary=True)
    cursor.execute("SELECT id, title FROM jurnal")
    records = cursor.fetchall()
    db_conn.close()
    return render_template("word_vector.html", records=records)

@app.route('/word_vector/<int:record_id>')
def word_vector(record_id):
    db_conn = get_db_connection()
    cursor = db_conn.cursor(dictionary=True)
    cursor.execute("SELECT content FROM jurnal WHERE id = %s", (record_id,))
    record = cursor.fetchone()
    db_conn.close()

    if record:
        # Get word vector representations for the selected record using FastText
        words = record['content'].split()
        word_vectors = {word: fasttext_model.get_word_vector(word).tolist() for word in words}

        return render_template("word_vector_detail.html", record=record, word_vectors=word_vectors)
    else:
        return "Record not found", 404

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5005, debug=True)

