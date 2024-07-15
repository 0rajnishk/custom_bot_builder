

![Screenshot 2](https://github.com/0rajnishk/custom_bot_builder/blob/main/screenshots/chat-bot.png)

# Custom Bot Builder Project

This project is designed to create custom chatbots that users can tailor to specific domains, topics, and constraints. Users provide data, define topics that the bot should address, and specify areas the bot should avoid. The project utilizes Sentence Transformers for embedding and similarity search, along with NemoGuardrails to ensure responses remain within specified domains and prevent abuse of the language model.

## Project Structure

The project directory contains the following files and folders:

```
app
NemoGuardrails
__pycache__
email
uAgents
app.py
chatbot_details.pkl
main.py
readme.md
requirements.txt
run_celery.sh
tasks.py
test.ipynb
frontend
.env.swp
.gitignore
README.md
main.py
requirements.txt
sentence-transformers.ipynb
```

## How to Run This Project

### Frontend

1. Navigate to the frontend directory:
    ```sh
    cd frontend
    ```
2. Start the frontend server:
    ```sh
    npm start
    ```

### Backend

1. Navigate to the apps directory:
    ```sh
    cd apps
    ```
2. Set up a virtual environment and activate it:
    ```sh
    python3 -m venv env
    source env/bin/activate
    ```
3. Make the run_celery.sh script executable:
    ```sh
    chmod 777 ./run_celery.sh
    ```
4. Start the backend server:
    ```sh
    python3 app.py
    ```
5. Run the Celery worker:
    ```sh
    ./run_celery.sh
    ```
6. Navigate to the uAgents directory and start the agent:
    ```sh
    cd uAgents
    python3 agent.py
    ```

## Dependencies

The project requires the following dependencies, listed in `requirements.txt`:

```

celery==5.4.0
Flask==3.0.3
Flask-Cors==4.0.1
huggingface-hub==0.23.2
langchain-text-splitters==0.2.0
langsmith==0.1.63
numpy==1.26.4
nvidia-nvtx-cu12==12.1.105PyPDF2==3.0.1
python-dateutil==2.9.0.post0
scikit-learn==1.5.0
scipy==1.13.1
sentence-transformers==2.7.0
SQLAlchemy==2.0.30
tokenizers==0.19.1
torch==2.3.0
transformers==4.41.1
typing_extensions==4.12.0
flask[async]
```

## Technical Details

### Sentence Transformers

Sentence Transformers are used for embedding the input data into a high-dimensional space, enabling efficient similarity searches. This helps in finding the most relevant context for the chatbot to use when generating responses.

### Similarity Search

Similarity search is employed to find the most relevant pieces of information from the embedded data. This context is then provided to the language model to generate accurate and relevant responses.

### NemoGuardrails

NemoGuardrails is utilized to ensure that the chatbot's responses stay within the specified domain and prevent abuse of the language model. It acts as a protective layer, filtering out inappropriate or irrelevant responses.

### Workflow

1. **User Input**: The user provides data, defines topics, and specifies constraints for the chatbot.
2. **Embedding**: The provided data is embedded using Sentence Transformers.
3. **Similarity Search**: The most relevant context is retrieved using similarity search.
4. **Response Generation**: The context is fed into the language model (e.g., GPT-4) to generate responses.
5. **Guardrails**: NemoGuardrails ensures the responses adhere to the defined constraints and domain.

## Additional Information

- **Retrieval-Augmented Generation (RAG)**: RAG is a technique that combines retrieval and generation to enhance the chatbot's performance by providing relevant context for response generation.
- **Sentence Transformer**: A model used to transform sentences into embeddings, facilitating similarity searches.
- **NemoGuardrails**: A framework designed to ensure the safe and controlled use of language models by filtering out inappropriate or off-domain responses.

For further details on RAG, Sentence Transformers, and NemoGuardrails, please refer to their respective documentation and literature.
