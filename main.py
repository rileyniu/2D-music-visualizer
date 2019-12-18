from flask import Flask, render_template
from analyzer.essentia_python import essentia_midi
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/_func/', methods=['POST'])
def _func():
    print("received POST")
    essentia_midi()
    data = json.load(open("output.json"))
    return data

if __name__ == "__main__":
    app.run(debug=True, port=4621)
