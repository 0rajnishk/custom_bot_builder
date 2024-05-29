import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer, util
import os
import pickle
from celery import Celery
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai
from openai import OpenAI
from dotenv import load_dotenv
import pickle
import multiprocessing
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# ============================================
from uagents.query import query
from uagents import Model
import asyncio
# ============================================


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.config['UPLOAD_FOLDER'] = './uploads'
PICKLE_FILE = 'chatbot_details.pkl'
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# ======== agent address ===========
agent_address = 'agent1qvn9xj8ejscne0mcgr4wnwmmj0zsuy56zyjfrktwh5zgtp5xcezjqfddu6d'


celery_app = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery_app.conf.update(app.config)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
multiprocessing.set_start_method('spawn', force=True)


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
smtp_pass = os.getenv("SMTP_PASS")
openai.api_key = openai_api_key


# ============= agent ===========
class AgentRequest(Model):
    name: str
    email: str
    chatbot_name: str




def load_chatbot_details():
    if os.path.exists(PICKLE_FILE):
        with open(PICKLE_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

def save_chatbot_details(details):
    with open(PICKLE_FILE, 'wb') as f:
        pickle.dump(details, f)



@celery_app.task
def generate_embeddings(chatbot_name, pdf_path, email, name):
    text = get_pdf_text(pdf_path)
    corpus = get_text_chunks(text)
    embeddings = model.encode(corpus)

    embeddings_path = f'embeddings/{chatbot_name}_embeddings.pkl'
    with open(embeddings_path, 'wb') as file:
        pickle.dump((corpus, embeddings), file)
    # sending email
    print('\n'*10, "sending email")
    send_email(email, name, chatbot_name)
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
    email = request.form['email']
    name = request.form['name']
    domain = request.form['domain']
    allowed = request.form['allowedAnswers']
    restricted = request.form['restrictedAnswers']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(pdf_path)
        generate_embeddings.delay(chatbot_name, pdf_path, email, name)

        # Load existing chatbot details
        chatbot_details = load_chatbot_details()

        # Update details with new data
        chatbot_details[chatbot_name] = {
            'domain': domain,
            'allowed': allowed,
            'restricted': restricted,
            'email': email,
            'name': name,
        }

        # Save updated details back to pickle file
        save_chatbot_details(chatbot_details)
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
        context = corpus[sorted_sim.indices[0][0].item()]

        response = generate_response(query, context, chatbot_name)
        return jsonify({"response": response}), 200
    else:
        return jsonify({"error": "Chatbot not found"}), 404


def generate_response(query, context, chatbot_name):

    with open(PICKLE_FILE, 'rb') as f:
        pk =  pickle.load(f)

    domain = pk[chatbot_name]['domain']
    restricted = pk[chatbot_name]["restricted"]
    allowed = pk[chatbot_name]["allowed"]

    prompt = f'''You are an intelligent agent who can only answer question from domain: {domain} and the given context
                    you do not answer anything related to the topic: {restricted}
                    you answer all the questions from the topic: {allowed}
                    Question: {query} Context: {context}'''
    
    openai_api_key = "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"

    client = OpenAI(api_key=openai_api_key)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        stream=True,
        temperature=0,
        max_tokens=3000
    )
    chat_resp = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            chat_resp += chunk.choices[0].delta.content
    return chat_resp



# ============== agent ======================

def send_email(email, name, chatbot_name):
    response =  asyncio.run(query(destination=agent_address,message=AgentRequest(name=name, email=email, chatbot_name=chatbot_name)))
    print("email is working !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", '\n'*10 )
    print(response)
    return response


# ======================================
if __name__ == '__main__':
    if not os.path.exists('embeddings'):
        os.makedirs('embeddings')
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
