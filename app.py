from http.client import HTTPException
import json
from flask import Flask, request, jsonify
from module.constants import HttpStatus
from module.models import Rindik
from werkzeug.utils import secure_filename
import os

# Define constants
UPLOAD_FOLDER = 'upload'

# Define flask app and config
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return "Hay"

@app.route('/api/predict-bilah', methods=['POST'])
def cek_bilah():

    try:
        # Ambil file dari request
        # Upload file dari request ke storage server
        # Ambil path dari upload filenya

        audio_file = request.files['audio']
        audio_path = os.path.join(UPLOAD_FOLDER, secure_filename(audio_file.filename))
        audio_file.save(audio_path)

        expected_bilah = request.form['expected_bilah']

        rindik = Rindik(expected_bilah, audio_path)
        result = rindik.predict_bilah()

        return jsonify(
            {
                'status': HttpStatus.SUCCESS,
                'data': {
                    'expected': expected_bilah,
                    'result': result,
                    'audio_path': audio_path
                },
                'message': 'Data berhasil diambil'
            }
        )
    except HTTPException as exception:
        return jsonify(
            {
                'status': HttpStatus.ERROR,
                'data': None,
                'message': str(exception)
            }
        )
        

if __name__ == "__main__":
    app.run()