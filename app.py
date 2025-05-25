import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, request, jsonify
from embed import embed, process_directory
from query import query
from get_vector_db import get_vector_db

TEMP_FOLDER = os.getenv('TEMP_FOLDER', './_temp')
os.makedirs(TEMP_FOLDER, exist_ok=True)

app = Flask(__name__)

@app.route('/embed', methods=['POST'])
def route_embed():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    embedded = embed(file)

    if embedded:
        return jsonify({"message": "File embedded successfully"}), 200

    return jsonify({"error": "File embedded unsuccessfully"}), 400

@app.route('/embed-directory', methods=['POST'])
def route_embed_directory():
    if 'directory' not in request.form:
        return jsonify({"error": "No directory path provided"}), 400

    directory = request.form['directory']
    if not os.path.isdir(directory):
        return jsonify({"error": "Invalid directory path"}), 400

    results = process_directory(directory)
    if results['success']:
        return jsonify({
            "message": "Directory processed successfully",
            "processed_files": results['processed_files'],
            "skipped_files": results['skipped_files']
        }), 200

    return jsonify({"error": "Directory processing failed"}), 400

@app.route('/query', methods=['POST'])
def route_query():
    data = request.get_json()
    response = query(data.get('query'))

    if response:
        return jsonify({"message": response}), 200

    return jsonify({"error": "Something went wrong"}), 400

@app.route('/clear', methods=['POST'])
def route_clear():
    try:
        db = get_vector_db()
        # Count documents before clearing
        count = db._collection.count()
        db.delete_collection()
        db = get_vector_db()  # Recreate the collection
        return jsonify({
            "message": f"Successfully cleared {count} documents",
            "documents_cleared": count
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to clear data: {str(e)}"}), 400

@app.route('/count', methods=['GET'])
def route_count():
    try:
        db = get_vector_db()
        count = db._collection.count()
        return jsonify({
            "message": f"Found {count} documents in the database",
            "document_count": count
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to count documents: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)