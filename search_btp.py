from flask import Flask, render_template, request
from bertopic import BERTopic
import pandas as pd

app = Flask(__name__)

# Muat dokumen dari CSV
def load_documents():
    df = pd.read_csv("bbc-news-data.csv", delimiter='\t' , encoding='latin1')
    return df['content'].tolist()

# Inisialisasi model BERTopic (pastikan model telah diinstal)
def generate_topics(documents):
    model = BERTopic()
    topics, _ = model.fit_transform(documents)
    return model, topics

# Memuat dokumen dan model topik
documents = load_documents()
model, topics = generate_topics(documents)

@app.route("/", methods=["GET", "POST"])
def index():
    search_results = []
    query = ""
    
    if request.method == "POST":
        query = request.form.get("query")
        num_topics = int(request.form.get("num_topics", 10))  # Default to 10 if not provided
        
        # Validate that query is not empty
        if query:
            try:
                # Find similar topics for the input query using BERTopic
                similar_topics, similarities = model.find_topics(query, top_n=num_topics)

                # Debugging: Print the similar topics
                print(f"Similar topics for '{query}': {similar_topics}")

                # Get topic info to retrieve counts and available topic IDs
                topic_info_df = model.get_topic_info()
                topic_info = set(topic_info_df["Topic"].values)  # Available topic IDs

                # Ensure similar_topics is not empty and process the results
                if similar_topics:
                    search_results = [
                        {
                            "topic_id": topic_id,
                            "representation": model.get_topic(topic_id),  # Representasi topik
                            "similarity": round(similarity, 3),  # Optionally add similarity score, rounded for readability
                            "count": topic_info_df[topic_info_df["Topic"] == topic_id]["Count"].values[0]  # Topic count
                        }
                        for topic_id, similarity in zip(similar_topics, similarities)
                        if topic_id in topic_info
                    ]
                else:
                    print("No similar topics found for the given query.")

            except Exception as e:
                print(f"An error occurred while processing the query: {e}")
                # Optionally, you can return an error message to the template if needed

    return render_template("bertopic.html", search_results=search_results, query=query)

@app.route("/topic_detail/<int:topic_id>")
def topic_detail(topic_id):
    # Ambil kosakata untuk topik tertentu
    vocab = model.get_topic(topic_id)
    
    # Ambil dokumen representatif untuk topik tertentu
    representative_docs = model.get_representative_docs(topic_id)

     # Select a specific number of documents to display
    num_docs_to_display = 5  # Set the desired number of documents
    representative_docs = representative_docs[:num_docs_to_display]  # Get the first 5 documents
    
    return render_template("topic_detail.html", topic_id=topic_id, vocab=vocab, representative_docs=representative_docs)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5003, debug=True)
