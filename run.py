import os
from flask import Flask, request, jsonify
from docx import Document
import logging


app = Flask(__name__)

def merge_docx(source_docx, merge_file_paths, output_path):
    # Open the source document
    doc1 = Document(source_docx)

    # Loop through each document to be merged
    for merge_file_path in merge_file_paths:
        # Open the document to be merged
        doc2 = Document(merge_file_path)

        # Loop through all elements in the document to be merged and append them to the source document
        for element in doc2.element.body:
            doc1.element.body.append(element)

    # Save the merged document to the output path
    doc1.save(output_path)

@app.route('/merge-docx', methods=['POST'])
def merge_docx_api():
    try:
        data = request.get_json()

        # Extract input parameters from the JSON data
        source_docx = data['source_docx']
        merge_file_paths = data['merge_file_paths']
        output_path = data['output_path']
       # Logging statements to check file paths
        logging.info(f'Source DOCX file: {source_docx}')
        logging.info(f'Merge file paths: {merge_file_paths}')
        logging.info(f'Output path: {output_path}')

        # Check if files exist
        for file_path in merge_file_paths:
            logging.info(f'Checking existence of file: {file_path}')
            if not os.path.exists(file_path):
                logging.error(f'File not found: {file_path}')
                return jsonify({'error': f'File not found: {file_path}'}), 404

        # Call the merge_docx function with the provided arguments
        merge_docx(source_docx, merge_file_paths, output_path)

        return jsonify({'message': 'Merge completed successfully.'}), 200
    except Exception as e:
        logging.error(f'Error occurred: {str(e)}')
        return jsonify({'error': str(e)}), 500

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == '__main__':
    app.run(debug=True)
