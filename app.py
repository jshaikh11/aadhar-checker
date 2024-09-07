from flask import Flask, request, jsonify, send_from_directory
import re

app = Flask(__name__)

# Updated function to check Aadhar number in different formats
def contains_aadhar(content):
    # Matches Aadhar numbers with or without spaces/hyphens
    aadhar_regex = r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"
    return re.search(aadhar_regex, content) is not None

# Route to serve the HTML file
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file uploaded!"}), 400

    try:
        file = request.files['file']
        content = file.read().decode('utf-8', errors='ignore')  # Handle text file

        if contains_aadhar(content):
            return jsonify({"success": True, "containsAadhar": True})
        else:
            return jsonify({"success": True, "containsAadhar": False})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
