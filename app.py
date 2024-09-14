import os
import time
from flask import Flask, request, jsonify
import redis
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import warnings


os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'




warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__)


cache = redis.Redis(host='redis', port=6379, db=0)


model = SentenceTransformer('all-MiniLM-L6-v2')


index = faiss.IndexFlatL2(384)


documents = []
document_embeddings = []


def load_documents():
    global documents, document_embeddings
    documents = ["Document 1", "Document 2", "Document 3"]
    document_embeddings = model.encode(documents)
    index.add(document_embeddings)


load_documents()


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "API is active!"})


@app.route('/search', methods=['POST'])
def search():
    start_time = time.time()


    user_id = request.json.get('user_id')
    query_text = request.json.get('text', "")
    top_k = request.json.get('top_k', 3)
    threshold = request.json.get('threshold', 0.5)


    request_count = cache.get(user_id)
    if request_count and int(request_count) > 5:
        return jsonify({"error": "Too many requests"}), 429

   
    cache.incr(user_id)
    if not cache.exists(user_id):
        cache.setex(user_id, 3600, 1)

    query_embedding = model.encode([query_text])
    distances, indices = index.search(query_embedding, top_k)


    results = []
    for idx, dist in zip(indices[0], distances[0]):
        if dist < threshold:
            results.append(documents[idx])

    inference_time = time.time() - start_time
    return jso
