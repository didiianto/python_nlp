from flask import Flask, render_template, request
from bertopic import BERTopic
import pandas as pd
import mysql.connector
from umap import UMAP


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

# # Inisialisasi BERTopic model
# umap_model = UMAP(n_neighbors=2)  # Kurangi nilai ini sesuai dengan ukuran data Anda
# model = BERTopic(umap_model=umap_model, min_topic_size=1)  # Pastikan model sudah diinisialisasi atau dilatih sebelumnya

# Menginisialisasi BERTopic dan melatih model pada data `texts`
def initialize_bertopic_model():
    db_conn = get_db_connection()
    cursor = db_conn.cursor(dictionary=True)

    # Query untuk mengambil semua data dari kolom yang relevan di tabel 'jurnal'
    sql_query = """
        SELECT id, title, abstract, content 
        FROM jurnal
    """
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    db_conn.close()

    # Gabungkan teks untuk pelatihan model
    texts = [f"{row['title']} {row['abstract']} {row['content']}" for row in rows]
    # print(texts)
    
    if texts:
        # Inisialisasi dan latih model BERTopic
        umap_model = UMAP(n_neighbors=3)  # Kurangi nilai ini sesuai dengan ukuran data Anda
        topic_model = BERTopic(umap_model=umap_model, min_topic_size=3)  # Pastikan model sudah diinisialisasi atau dilatih sebelumnya
        # topic_model = BERTopic()
        topic_model.fit_transform(texts)  # Latih model di luar fungsi `index`
        return topic_model
    else:
        print("Tidak ada teks yang ditemukan untuk melatih model.")
        return None
    
# Inisialisasi model sekali saat aplikasi dijalankan
model = initialize_bertopic_model()

@app.route("/", methods=["GET", "POST"])
def index():
    search_results = []
    query = ""
    
    if request.method == "POST":
        query = request.form.get("query")
        num_topics = int(request.form.get("num_topics", 10))  # Default ke 10 jika tidak ada input

        # Validasi bahwa query tidak kosong dan model tidak `None`
        if query and model:
            try:
                # Jalankan BERTopic untuk menemukan topik yang mirip dengan query
                similar_topics, similarities = model.find_topics(query, top_n=num_topics)

                # Dapatkan informasi topik untuk memperoleh jumlah dan ID topik yang tersedia
                topic_info_df = model.get_topic_info()
                topic_info = set(topic_info_df["Topic"].values)  # Tersedia ID topik

                # Proses hasil pencarian
                search_results = [
                    {
                        "topic_id": topic_id,
                        "representation": model.get_topic(topic_id),  # Representasi topik
                        "similarity": round(similarity, 3),  # Tambahkan skor similaritas
                        "count": topic_info_df[topic_info_df["Topic"] == topic_id]["Count"].values[0]  # Jumlah topik
                    }
                    for topic_id, similarity in zip(similar_topics, similarities)
                    if topic_id in topic_info
                ]
                
            except Exception as e:
                print(f"Terjadi kesalahan saat memproses query: {e}")
    
    return render_template("bertopic.html", search_results=search_results, query=query)

@app.route("/topic_detail/<int:topic_id>")
def topic_detail(topic_id):
    # Ambil kosakata untuk topik tertentu
    vocab = model.get_topic(topic_id)
    
    # Ambil dokumen representatif untuk topik tertentu
    representative_docs = model.get_representative_docs(topic_id)
    # print(len(representative_docs))  # Check the actual count

     # Select a specific number of documents to display
    num_docs_to_display = 5  # Set the desired number of documents
    representative_docs = representative_docs[:num_docs_to_display]  # Get the first 5 documents
    
    return render_template("topic_detail.html", topic_id=topic_id, vocab=vocab, representative_docs=representative_docs)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5004, debug=True)
