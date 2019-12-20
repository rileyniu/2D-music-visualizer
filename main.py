from flask import Flask, flash, request, redirect, render_template, url_for, send_from_directory
from werkzeug.utils import secure_filename
from analyzer.essentia_python import essentia_midi
import json
import os
import subprocess

UPLOAD_FOLDER = './analyzer'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'aiff', 'flac'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/upload_file/', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    if os.path.exists("./analyzer/output.json"):
        os.remove("./analyzer/output.json") #see if this works
        print("DELETED OLD JSON")
    essentia_midi(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    data = json.load(open("./analyzer/output.json"))
    return data
   
if __name__ == "__main__":
    app.run(debug=True, port=4624)