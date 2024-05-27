from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import os
import pickle
from celery import Celery
from langchain.text_splitter import RecursiveCharacterTextSplitter

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery_app = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery_app.conf.update(app.config)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2').to("cuda")

@celery_app.task
def generate_embeddings(chatbot_name, pdf_path):
    text = get_pdf_text(pdf_path)
    corpus = get_text_chunks(text)
    embeddings = model.encode(corpus)

    embeddings_path = f'embeddings/{chatbot_name}_embeddings.pkl'
    with open(embeddings_path, 'wb') as file:
        pickle.dump((corpus, embeddings), file)

    os.remove(pdf_path)

def get_pdf_text(pdf_path):
    text = ""
    pdf_reader = PdfReader(pdf_path)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_text(text)
    return chunks

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    chatbot_name = request.form['chatbot_name']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(pdf_path)
        generate_embeddings.delay(chatbot_name, pdf_path)
        return jsonify({"message": "File uploaded and processing started", "chatbot_name": chatbot_name}), 200

@app.route('/get_chatbot/<chatbot_name>', methods=['GET'])
def get_chatbot(chatbot_name):
    embeddings_path = f'embeddings/{chatbot_name}_embeddings.pkl'
    if os.path.exists(embeddings_path):
        with open(embeddings_path, 'rb') as file:
            corpus, embeddings = pickle.load(file)
        return jsonify({"corpus": corpus, "embeddings": embeddings.tolist()}), 200
    else:
        return jsonify({"error": "Chatbot not found"}), 404

@app.route('/query_chatbot/<chatbot_name>', methods=['POST'])
def query_chatbot(chatbot_name):
    query = request.json.get('query')
    embeddings_path = f'embeddings/{chatbot_name}_embeddings.pkl'
    if os.path.exists(embeddings_path):
        with open(embeddings_path, 'rb') as file:
            corpus, embeddings = pickle.load(file)
        
        q_embed = model.encode(query)
        sim = util.cos_sim(q_embed, embeddings)
        sorted_sim = sim.sort(descending=True)
        context = corpus[sorted_sim[1][0][0]]
        return jsonify({"response": context}), 200
    else:
        return jsonify({"error": "Chatbot not found"}), 404

if __name__ == '__main__':
    if not os.path.exists('embeddings'):
        os.makedirs('embeddings')
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)

