import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.middleware.shared_data import SharedDataMiddleware
import json



app = Flask(__name__)




@app.route('/deployment', methods=['POST'])
def new_deployment():
    # check if the post request has the file part
    if 'file' not in request.files:
        return {"error": "No file part"}, 500

    file = request.files['file']

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return {"error": "No selected file"}, 500

    if not file or not allowed_file(file.filename):
        return {"error": "Wrong type"}, 500

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return {"file": filename}, 200

@app.route('/upload-json', methods=['POST'])
def upload_json():


    content = request.json
    filename = secure_filename(content.get("id")+".json")

    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename ), 'w') as outfile:
        json.dump(content, outfile)

    return {"file": filename}, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0')
