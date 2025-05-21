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

## Running the App

```bash
python app.py
```

The API will be available at `http://localhost:8080`.

## API Endpoints

### POST `/embed`

- Upload a `.docx` file to embed its content.
- Form field: `file`

### POST `/query`

- Query the embedded documents.
- JSON body: `{ "query": "your question here" }`

## Notes

- Embedded data and temporary files are stored locally and ignored by git.
- Requires [Ollama](https://ollama.com/) for local LLM inference.
