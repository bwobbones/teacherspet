import os
from datetime import datetime
from werkzeug.utils import secure_filename
from langchain_docling import DoclingLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.utils import filter_complex_metadata
from get_vector_db import get_vector_db

TEMP_FOLDER = os.getenv('TEMP_FOLDER', './_temp')

# Function to check if the uploaded file is allowed (only .docx files)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'docx'}

# Function to save the uploaded file to the temporary folder
def save_file(file):
    # Save the uploaded file with a secure filename and return the file path
    ct = datetime.now()
    ts = ct.timestamp()
    filename = str(ts) + "_" + secure_filename(file.filename)
    file_path = os.path.join(TEMP_FOLDER, filename)
    file.save(file_path)
    return file_path

# Function to load and split the data from the .docx file
def load_and_split_data(file_path):
    # Load the .docx file and split the data into chunks
    loader = DoclingLoader(file_path=file_path)
    data = loader.load()
    filtered_metadata = filter_complex_metadata(data)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=100)
    chunks = text_splitter.split_documents(filtered_metadata)
    return chunks

# Main function to handle the embedding process for a directory
def embed(directory):
    if not os.path.isdir(directory):
        return False

    success = False
    for filename in os.listdir(directory):
        if allowed_file(filename):
            print(f"Processing file: {filename}")
            file_path = os.path.join(directory, filename)
            chunks = load_and_split_data(file_path)
            db = get_vector_db()
            db.add_documents(chunks)
            db.persist()
            success = True

    return success