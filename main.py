from flask import Flask, render_template
from analyzer.essentia_python import essentia_midi

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/_func/', methods=['POST'])
def _func():
    essentia_midi()
    print("received POST")
    return "success"

if __name__ == "__main__":
    app.run(debug=True, port=4623)
