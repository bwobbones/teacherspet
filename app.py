import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, request, jsonify
from embed import embed, save_file
from query import query
from get_vector_db import get_vector_db

TEMP_FOLDER = os.getenv('TEMP_FOLDER', './_temp')
os.makedirs(TEMP_FOLDER, exist_ok=True)

app = Flask(__name__)

@app.route('/embed', methods=['POST'])
def route_embed():
    print("Received embed request")
    print(f"Request form data: {request.form}")
    print(f"Request files: {request.files}")

    if 'file' not in request.files:
        # Check if a directory path was provided
        if 'directory' in request.form:
            directory = request.form['directory']
            print(f"Processing directory: {directory}")
            if os.path.isdir(directory):
                print(f"Directory exists, attempting to embed")
                embedded = embed(directory)
                if embedded:
                    return jsonify({"message": "Directory embedded successfully"}), 200
                return jsonify({"error": "Directory embedded unsuccessfully - no valid .docx files found"}), 400
            return jsonify({"error": f"Invalid directory path: {directory}"}), 400
        return jsonify({"error": "No file or directory provided"}), 400

    file = request.files['file']
    print(f"Processing file: {file.filename}")

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the file first
    try:
        file_path = save_file(file)
        print(f"File saved to: {file_path}")
    except Exception as e:
        print(f"Error saving file: {str(e)}")
        return jsonify({"error": f"Error saving file: {str(e)}"}), 400
    
    # Process the file
    try:
        embedded = embed(file_path)
        if embedded:
            return jsonify({"message": "File embedded successfully"}), 200
        return jsonify({"error": "File embedded unsuccessfully - not a valid .docx file"}), 400
    except Exception as e:
        print(f"Error embedding file: {str(e)}")
        return jsonify({"error": f"Error embedding file: {str(e)}"}), 400

@app.route('/query', methods=['POST'])
def route_query():
    data = request.get_json()
    response = query(data.get('query'))

    if response:
        return jsonify({"message": response}), 200

    return jsonify({"error": "Something went wrong"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)