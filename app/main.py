from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import os
import pickle
from sentence_transformers import SentenceTransformer, util
import openai

app = Flask(__name__)
socketio = SocketIO(app)

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

@socketio.on('query_chatbot')
def handle_query_chatbot(data):
    chatbot_name = data.get('chatbot_name')
    query = data.get('query')
    embeddings_path = f'embeddings/{chatbot_name}_embeddings.pkl'
    
    if os.path.exists(embeddings_path):
        with open(embeddings_path, 'rb') as file:
            corpus, embeddings = pickle.load(file)
        
        q_embed = model.encode(query)
        sim = util.cos_sim(q_embed, embeddings)
        sorted_sim = sim.sort(descending=True)
        context = corpus[sorted_sim.indices[0][0].item()]

        response = generate_response(query, context)
        emit('chatbot_response', {"response": response})
    else:
        emit('chatbot_response', {"error": "Chatbot not found"})

def generate_response(query, context):
    prompt = f'''You are an intelligent agent who can answer a question from the context
    Question: {query} Context: {context}'''
    
    openai_api_key = "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"
    openai.api_key = openai_api_key

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3000,
        temperature=0
    )
    
    chat_resp = response.choices[0].text.strip()
    return chat_resp

if __name__ == '__main__':
    socketio.run(app, host='localhost', port=5050, debug=True)