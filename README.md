# TeachersPet

A Flask-based API for embedding and querying documents using LangChain and ChromaDB.

## Features

- Upload `.docx` files to embed their content into a vector database
- Query the embedded documents using a language model

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bwobbones/teacherspet.git
   cd teacherspet
   ```
2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set environment variables (optional):**
   - Create a `.env` file to override defaults for `TEMP_FOLDER`, `CHROMA_PATH`, `COLLECTION_NAME`, `LLM_MODEL`, `TEXT_EMBEDDING_MODEL`.
   - **Environment Variables Summary:**
     - `TEMP_FOLDER`: Directory where temporary files (e.g., uploaded documents) are stored before processing.
     - `CHROMA_PATH`: Path to the ChromaDB directory where document embeddings are persisted.
     - `COLLECTION_NAME`: Name of the collection in ChromaDB used to store and retrieve document embeddings.
     - `LLM_MODEL`: The name of the language model used for querying (e.g., "mistral").
     - `TEXT_EMBEDDING_MODEL`: The model used for generating text embeddings (e.g., "nomic-embed-text").

## Setting up Ollama

Before running this app, you need to have an Ollama server running locally to provide the language model backend.

1. **Install Ollama:**

   - Visit [Ollama's download page](https://ollama.com/download) and follow the instructions for your operating system (macOS, Linux, or Windows).

2. **Start the Ollama server:**

   - After installation, start the Ollama server by running:
     ```bash
     ollama serve
     ```
   - This will start the Ollama server on your machine, typically at `http://localhost:11434`.

3. **Pull a model (e.g., mistral):**

   - You need to pull a model that matches your `.env` or default settings. For example:
     ```bash
     ollama pull mistral
     ```
   - You can pull other models as needed (see [Ollama's model library](https://ollama.com/library)).

4. **Verify Ollama is running:**
   - You can check if Ollama is running by visiting [http://localhost:11434](http://localhost:11434) or running:
     ```bash
     curl http://localhost:11434
     ```

Once Ollama is running and the required model is pulled, you can start the Flask app as described below.

## Running the App

```bash
python app.py
```

The API will be available at `http://localhost:8080`.

## API Endpoints

### POST `/embed`

- Upload a `.docx` file to embed its content.
- Form field: `file`

**Sample curl command:**

```bash
curl --request POST \
  --url http://localhost:8080/embed \
  --header 'Content-Type: multipart/form-data' \
  --form file=@/Users/bwobbones/<docname>.docx
```

### POST `/query`

- Query the embedded documents.
- JSON body: `{ "query": "your question here" }`

**Sample curl command:**

```bash
curl --request POST \
  --url http://localhost:8080/query \
  --header 'Content-Type: application/json' \
  --data '{ "query": "Who is bwobbones?" }'
```

## Notes

- Embedded data and temporary files are stored locally and ignored by git.
- Requires [Ollama](https://ollama.com/) for local LLM inference.

---

## Acknowledgements

Special thanks to [Nasser Maronie](https://dev.to/nassermaronie/build-your-own-rag-app-a-step-by-step-guide-to-setup-llm-locally-using-ollama-python-and-chromadb-b12) for his excellent article on setting up a local RAG app with Ollama, Python, and ChromaDB, which was invaluable for this project.
