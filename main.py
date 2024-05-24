###########################################################################
###########################################################################
#    upload all your pdfs ------------------------ [POST]form data--> pdf_files:file
#    http://127.0.0.1:5000/upload


#    ASK questions query prahm--> question: <your question>

# eg.
# http://127.0.0.1:5000/ask?question=tell me about rajnish
#

###########################################################################
###########################################################################







from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
# from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)

# In-memory storage for processed PDF text and vector store
processed_pdf_text = ""
vector_store = None

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    return vector_store

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details. If the answer is not available in the context, just say, "answer is not available in the context", don't provide the wrong answer.

    Context:
    {context}?

    Question:
    {question}

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

@app.route('/upload', methods=['POST'])
def upload_pdf():
    global processed_pdf_text, vector_store

    if 'pdf_files' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    pdf_files = request.files.getlist('pdf_files')

    if not pdf_files:
        return jsonify({"error": "No selected file"}), 400

    raw_text = get_pdf_text(pdf_files)
    text_chunks = get_text_chunks(raw_text)
    vector_store = get_vector_store(text_chunks)
    processed_pdf_text = raw_text

    return jsonify({"message": "PDFs processed successfully!"}), 200

@app.route('/ask', methods=['GET'])
def ask_question():
    global processed_pdf_text, vector_store

    user_question = request.args.get('question')

    if not user_question:
        return jsonify({"error": "No question provided"}), 400

    if not vector_store:
        return jsonify({"error": "No PDFs processed yet"}), 400

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    context = f"{processed_pdf_text}\n\nQuestion: {user_question}"

    response = chain({"input_documents": docs, "question": user_question, "context": context}, return_only_outputs=True)

    return jsonify({"reply": response["output_text"]}), 200

if __name__ == "__main__":
    app.run(debug=True)
