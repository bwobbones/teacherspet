import os
from datetime import datetime
from werkzeug.utils import secure_filename
from langchain_docling import DoclingLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.utils import filter_complex_metadata
from get_vector_db import get_vector_db

TEMP_FOLDER = os.getenv('TEMP_FOLDER', './_temp')

# Function to check if the uploaded file is allowed (.docx or .pdf files)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'docx', 'pdf'}

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
    
    # Pre-split large documents before filtering metadata
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    # Split the raw data first
    pre_chunks = text_splitter.split_documents(data)
    print(f"Pre-split document into {len(pre_chunks)} chunks")
    
    # Now filter metadata for each chunk
    filtered_chunks = []
    for chunk in pre_chunks:
        filtered_metadata = filter_complex_metadata([chunk])
        filtered_chunks.extend(filtered_metadata)
    
    # Debug logging for chunk sizes
    for i, chunk in enumerate(filtered_chunks):
        print(f"Chunk {i+1} length: {len(chunk.page_content)} characters")
    
    print(f"Final document split into {len(filtered_chunks)} chunks")
    return filtered_chunks

# Main function to handle the embedding process
def embed(file):
    # Check if the file is valid, save it, load and split the data, add to the database, and remove the temporary file
    if file.filename != '' and file and allowed_file(file.filename):
        file_path = save_file(file)
        chunks = load_and_split_data(file_path)
        db = get_vector_db()
        db.add_documents(chunks)
        db.persist()
        os.remove(file_path)
        return True
    return False

# Function to process all .docx files in a directory
def process_directory(directory_path):
    processed_files = []
    skipped_files = []
    
    print(f"Processing directory: {directory_path}")
    
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            if not allowed_file(filename):
                print(f"Skipping non-docx file: {filename}")
                skipped_files.append(os.path.join(root, filename))
                continue
                
            file_path = os.path.join(root, filename)
            print(f"Processing file: {file_path}")
            
            try:
                chunks = load_and_split_data(file_path)
                db = get_vector_db()
                db.add_documents(chunks)
                db.persist()
                processed_files.append(file_path)
                print(f"Successfully processed: {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                skipped_files.append(file_path)
    
    return {
        'success': len(processed_files) > 0,
        'processed_files': processed_files,
        'skipped_files': skipped_files
    }