import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
from flask import Flask, request, redirect, url_for
from flask import render_template, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        error = {'error': 'No file part'}
        return jsonify(results=error)

    file = request.files['file']

    if file.filename == '':
        error = {'error': 'No selected file'}
        return jsonify(results=error)

    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        success = {'success': 'Uploaded ' + file.filename}
        return jsonify(results=success)
    else:
        error = {'error': 'File type not allowed'}
        return jsonify(results=error)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/uploads', methods=['GET'])
def uploads():
    # Joining the base and the requested path
    abs_path = os.path.join(UPLOAD_FOLDER)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template('files.html', files=files)

if __name__ == "__main__":
    app.run()
